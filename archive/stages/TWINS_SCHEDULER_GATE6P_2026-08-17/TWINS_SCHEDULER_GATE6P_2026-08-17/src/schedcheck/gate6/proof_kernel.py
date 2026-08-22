from __future__ import annotations

"""Small auditable proof-certificate kernel used by Gate 6'.

The kernel deliberately supports only what the paper needs:

* finite Horn-style derivations;
* one well-founded natural-number induction schema;
* exact normalization of univariate integer polynomials;
* a dedicated checker for the quorum-pivot branch construction.

It is not a replacement for Lean/Coq/Isabelle.  Its purpose is to make every
trusted rule and every proof dependency explicit, reproducible, and small enough
to audit independently.  No network access or third-party runtime dependency is
required.
"""

from dataclasses import dataclass
from fractions import Fraction
import ast
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence


class ProofFailure(AssertionError):
    """Raised when a proof certificate is malformed or does not check."""


@dataclass(frozen=True, slots=True)
class HornRule:
    name: str
    requires: tuple[str, ...]
    concludes: str
    category: str


@dataclass(frozen=True, slots=True)
class DerivationStep:
    identifier: str
    rule: str
    conclusion: str


@dataclass(frozen=True, slots=True)
class Polynomial:
    """Univariate polynomial in f with exact rational coefficients."""

    coefficients: tuple[tuple[int, Fraction], ...]

    @staticmethod
    def from_dict(values: Mapping[int, Fraction]) -> "Polynomial":
        cleaned = tuple(
            sorted((degree, coeff) for degree, coeff in values.items() if coeff != 0)
        )
        return Polynomial(cleaned)

    @staticmethod
    def constant(value: int | Fraction) -> "Polynomial":
        fraction = Fraction(value)
        return Polynomial.from_dict({0: fraction})

    @staticmethod
    def variable() -> "Polynomial":
        return Polynomial.from_dict({1: Fraction(1)})

    def as_dict(self) -> dict[int, Fraction]:
        return dict(self.coefficients)

    def __add__(self, other: "Polynomial") -> "Polynomial":
        result = self.as_dict()
        for degree, coeff in other.coefficients:
            result[degree] = result.get(degree, Fraction(0)) + coeff
        return Polynomial.from_dict(result)

    def __neg__(self) -> "Polynomial":
        return Polynomial.from_dict({d: -c for d, c in self.coefficients})

    def __sub__(self, other: "Polynomial") -> "Polynomial":
        return self + (-other)

    def __mul__(self, other: "Polynomial") -> "Polynomial":
        result: dict[int, Fraction] = {}
        for d1, c1 in self.coefficients:
            for d2, c2 in other.coefficients:
                degree = d1 + d2
                result[degree] = result.get(degree, Fraction(0)) + c1 * c2
        return Polynomial.from_dict(result)

    def is_zero(self) -> bool:
        return not self.coefficients

    def is_constant(self) -> bool:
        return all(degree == 0 for degree, _ in self.coefficients)

    def constant_value(self) -> Fraction:
        if not self.is_constant():
            raise ProofFailure(f"polynomial is not constant: {self}")
        return dict(self.coefficients).get(0, Fraction(0))

    def canonical(self) -> str:
        if not self.coefficients:
            return "0"
        parts: list[str] = []
        for degree, coeff in sorted(self.coefficients, reverse=True):
            if degree == 0:
                term = str(coeff)
            elif degree == 1:
                term = "f" if coeff == 1 else "-f" if coeff == -1 else f"{coeff}*f"
            else:
                term = (
                    f"f^{degree}"
                    if coeff == 1
                    else f"-f^{degree}"
                    if coeff == -1
                    else f"{coeff}*f^{degree}"
                )
            parts.append(term)
        return " + ".join(parts).replace("+ -", "- ")


_ALLOWED_AST = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.USub,
    ast.UAdd,
    ast.Constant,
    ast.Name,
    ast.Load,
)


def parse_polynomial(expression: str) -> Polynomial:
    try:
        node = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ProofFailure(f"invalid polynomial expression {expression!r}: {exc}") from exc

    for item in ast.walk(node):
        if not isinstance(item, _ALLOWED_AST):
            raise ProofFailure(
                f"unsupported syntax in polynomial expression {expression!r}: "
                f"{type(item).__name__}"
            )

    def evaluate(item: ast.AST) -> Polynomial:
        if isinstance(item, ast.Expression):
            return evaluate(item.body)
        if isinstance(item, ast.Constant):
            if not isinstance(item.value, int) or isinstance(item.value, bool):
                raise ProofFailure(f"only integer constants are allowed: {expression!r}")
            return Polynomial.constant(item.value)
        if isinstance(item, ast.Name):
            if item.id != "f":
                raise ProofFailure(f"only variable 'f' is allowed: {item.id!r}")
            return Polynomial.variable()
        if isinstance(item, ast.UnaryOp):
            value = evaluate(item.operand)
            if isinstance(item.op, ast.USub):
                return -value
            if isinstance(item.op, ast.UAdd):
                return value
        if isinstance(item, ast.BinOp):
            left = evaluate(item.left)
            right = evaluate(item.right)
            if isinstance(item.op, ast.Add):
                return left + right
            if isinstance(item.op, ast.Sub):
                return left - right
            if isinstance(item.op, ast.Mult):
                return left * right
        raise ProofFailure(f"unsupported polynomial node: {ast.dump(item)}")

    return evaluate(node)


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProofFailure(f"cannot load JSON proof asset {path}: {exc}") from exc


def _require_mapping(value: object, name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ProofFailure(f"{name} must be an object")
    return value


def _require_string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ProofFailure(f"{name} must be a non-empty string")
    return value


def _require_string_list(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ProofFailure(f"{name} must be a list of strings")
    return tuple(value)


def load_rules(path: Path) -> dict[str, HornRule]:
    raw = _require_mapping(_load_json(path), "rule file")
    rules_raw = raw.get("rules")
    if not isinstance(rules_raw, list):
        raise ProofFailure("rule file must contain a 'rules' list")
    result: dict[str, HornRule] = {}
    for index, item in enumerate(rules_raw):
        row = _require_mapping(item, f"rules[{index}]")
        name = _require_string(row.get("name"), f"rules[{index}].name")
        if name in result:
            raise ProofFailure(f"duplicate rule name: {name}")
        rule = HornRule(
            name=name,
            requires=_require_string_list(row.get("requires", []), f"{name}.requires"),
            concludes=_require_string(row.get("concludes"), f"{name}.concludes"),
            category=_require_string(row.get("category"), f"{name}.category"),
        )
        if rule.concludes in rule.requires:
            raise ProofFailure(f"circular one-step rule: {name}")
        result[name] = rule
    return result


def check_horn_derivation(
    *,
    available: Iterable[str],
    rules: Mapping[str, HornRule],
    steps: Sequence[object],
    target: str,
) -> dict[str, object]:
    facts = set(available)
    initial = sorted(facts)
    checked: list[DerivationStep] = []
    identifiers: set[str] = set()
    for index, raw_step in enumerate(steps):
        row = _require_mapping(raw_step, f"steps[{index}]")
        identifier = _require_string(row.get("id"), f"steps[{index}].id")
        rule_name = _require_string(row.get("rule"), f"steps[{index}].rule")
        if identifier in identifiers:
            raise ProofFailure(f"duplicate proof-step id: {identifier}")
        identifiers.add(identifier)
        if rule_name not in rules:
            raise ProofFailure(f"unknown rule {rule_name!r} in step {identifier}")
        rule = rules[rule_name]
        missing = [fact for fact in rule.requires if fact not in facts]
        if missing:
            raise ProofFailure(
                f"step {identifier} cannot apply {rule_name}; missing facts: {missing}"
            )
        claimed = row.get("conclusion", rule.concludes)
        if claimed != rule.concludes:
            raise ProofFailure(
                f"step {identifier} claims {claimed!r}, but {rule_name} concludes "
                f"{rule.concludes!r}"
            )
        facts.add(rule.concludes)
        checked.append(DerivationStep(identifier, rule_name, rule.concludes))
    if target not in facts:
        raise ProofFailure(f"target {target!r} was not derived")
    return {
        "status": "PASS",
        "initial_facts": initial,
        "derived_facts": sorted(facts - set(initial)),
        "target": target,
        "steps_checked": len(checked),
        "step_ids": [step.identifier for step in checked],
    }


def check_induction_certificate(rule_path: Path, certificate_path: Path) -> dict[str, object]:
    rules = load_rules(rule_path)
    cert = _require_mapping(_load_json(certificate_path), "induction certificate")
    theorem = _require_string(cert.get("theorem"), "theorem")
    premises = _require_string_list(cert.get("premises", []), "premises")
    definitions = _require_string_list(cert.get("definitions", []), "definitions")
    if theorem in premises or theorem in definitions:
        raise ProofFailure("the theorem may not be assumed as a premise or definition")

    induction = _require_mapping(cert.get("induction"), "induction")
    measure = _require_string(induction.get("measure"), "induction.measure")
    base = _require_mapping(induction.get("base"), "induction.base")
    step = _require_mapping(induction.get("step"), "induction.step")

    base_target = _require_string(base.get("target"), "induction.base.target")
    base_result = check_horn_derivation(
        available=(*premises, *definitions),
        rules=rules,
        steps=base.get("steps", []),
        target=base_target,
    )

    ih = _require_string(step.get("induction_hypothesis"), "induction.step.induction_hypothesis")
    decrease = _require_string(step.get("measure_decrease_fact"), "induction.step.measure_decrease_fact")
    step_target = _require_string(step.get("target"), "induction.step.target")
    step_result = check_horn_derivation(
        available=(*premises, *definitions, ih),
        rules=rules,
        steps=step.get("steps", []),
        target=step_target,
    )
    if decrease not in set(step_result["derived_facts"]) | set(step_result["initial_facts"]):
        raise ProofFailure(
            f"induction step does not establish declared decrease fact {decrease!r}"
        )

    induction_result = _require_string(induction.get("result"), "induction.result")
    if induction_result == base_target or induction_result == step_target:
        raise ProofFailure("induction result must be a universal conclusion, not a case fact")

    final = _require_mapping(cert.get("final", {}), "final")
    final_target = _require_string(final.get("target", induction_result), "final.target")
    final_steps = final.get("steps", [])
    if final_steps:
        final_result = check_horn_derivation(
            available=(*premises, *definitions, induction_result),
            rules=rules,
            steps=final_steps,
            target=final_target,
        )
    else:
        if final_target != induction_result:
            raise ProofFailure("empty final proof must target the induction result")
        final_result = {
            "status": "PASS",
            "initial_facts": [induction_result],
            "derived_facts": [],
            "target": final_target,
            "steps_checked": 0,
            "step_ids": [],
        }

    if final_target != theorem:
        raise ProofFailure(
            f"certificate theorem {theorem!r} does not match final target {final_target!r}"
        )

    return {
        "status": "PASS",
        "theorem": theorem,
        "measure": measure,
        "trusted_induction_rule": "well_founded_induction_on_Nat",
        "base": base_result,
        "step": step_result,
        "final": final_result,
        "rules_loaded": len(rules),
        "premises": list(premises),
        "definitions": list(definitions),
        "rule_file_sha256": hashlib.sha256(rule_path.read_bytes()).hexdigest(),
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
    }


def check_polynomial_obligations(certificate_path: Path) -> dict[str, object]:
    cert = _require_mapping(_load_json(certificate_path), "polynomial certificate")
    equalities = cert.get("equalities", [])
    positive_differences = cert.get("positive_differences", [])
    if not isinstance(equalities, list) or not isinstance(positive_differences, list):
        raise ProofFailure("polynomial certificate lists are malformed")

    equality_results: list[dict[str, object]] = []
    for index, raw in enumerate(equalities):
        row = _require_mapping(raw, f"equalities[{index}]")
        lhs_text = _require_string(row.get("lhs"), f"equalities[{index}].lhs")
        rhs_text = _require_string(row.get("rhs"), f"equalities[{index}].rhs")
        difference = parse_polynomial(lhs_text) - parse_polynomial(rhs_text)
        if not difference.is_zero():
            raise ProofFailure(
                f"polynomial equality failed: {lhs_text} = {rhs_text}; "
                f"difference {difference.canonical()}"
            )
        equality_results.append(
            {
                "id": row.get("id", f"eq_{index}"),
                "lhs": lhs_text,
                "rhs": rhs_text,
                "normal_form_difference": difference.canonical(),
                "status": "PASS",
            }
        )

    positivity_results: list[dict[str, object]] = []
    for index, raw in enumerate(positive_differences):
        row = _require_mapping(raw, f"positive_differences[{index}]")
        larger_text = _require_string(row.get("larger"), f"positive_differences[{index}].larger")
        smaller_text = _require_string(row.get("smaller"), f"positive_differences[{index}].smaller")
        expected_text = _require_string(row.get("difference"), f"positive_differences[{index}].difference")
        actual = parse_polynomial(larger_text) - parse_polynomial(smaller_text)
        expected = parse_polynomial(expected_text)
        if actual != expected:
            raise ProofFailure(
                f"difference certificate failed: {larger_text} - {smaller_text}; "
                f"actual {actual.canonical()}, expected {expected.canonical()}"
            )
        if not expected.is_constant() or expected.constant_value() <= 0:
            raise ProofFailure(
                f"certified positive difference is not a positive constant: {expected.canonical()}"
            )
        positivity_results.append(
            {
                "id": row.get("id", f"pos_{index}"),
                "larger": larger_text,
                "smaller": smaller_text,
                "difference": expected.canonical(),
                "status": "PASS",
            }
        )

    return {
        "status": "PASS",
        "equalities": equality_results,
        "positive_differences": positivity_results,
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
    }


def check_quorum_pivot_certificate(certificate_path: Path) -> dict[str, object]:
    cert = _require_mapping(_load_json(certificate_path), "quorum-pivot certificate")
    arithmetic = check_polynomial_obligations(certificate_path)

    construction = _require_mapping(cert.get("construction"), "construction")
    expected = {
        "n": "3*f+1",
        "q": "2*f+1",
        "B": "f",
        "A": "f",
        "C": "f",
        "pivot": "1",
        "Q0": "2*f+1",
        "Q1": "2*f+1",
        "intersection": "f+1",
        "base_support": "2*f",
    }
    for name, expression in expected.items():
        actual = _require_string(construction.get(name), f"construction.{name}")
        if parse_polynomial(actual) != parse_polynomial(expression):
            raise ProofFailure(
                f"construction field {name} has {actual}, expected polynomial {expression}"
            )

    branches = _require_mapping(cert.get("branches"), "branches")
    typed = _require_mapping(branches.get("phase_specific"), "branches.phase_specific")
    off = _require_mapping(branches.get("directed_edge_absent"), "branches.directed_edge_absent")
    on = _require_mapping(branches.get("directed_edge_present"), "branches.directed_edge_present")

    q = parse_polynomial(construction["q"])
    base = parse_polynomial(construction["base_support"])

    def support(row: Mapping[str, object], key: str) -> Polynomial:
        return parse_polynomial(_require_string(row.get(key), f"branch.{key}"))

    typed_first = support(typed, "first_support")
    typed_second = support(typed, "second_support")
    if typed_first != q or typed_second != q:
        raise ProofFailure("phase-specific branch must reach both quorums exactly")
    if typed.get("deliver_E") is not True or typed.get("deliver_R") is not False:
        raise ProofFailure("phase-specific branch must deliver E and omit R")

    off_first = support(off, "first_support")
    if off_first != base or not (q - off_first).is_constant() or (q - off_first).constant_value() != 1:
        raise ProofFailure("directed edge-absent branch must miss first quorum by one")
    if off.get("deliver_E") is not False or off.get("deliver_R") is not False:
        raise ProofFailure("edge-absent branch must omit both E and R")

    on_first = support(on, "first_support")
    on_second = support(on, "second_support")
    if on_first != q:
        raise ProofFailure("directed edge-present branch must reach first quorum")
    if on_second != base or not (q - on_second).is_constant() or (q - on_second).constant_value() != 1:
        raise ProofFailure("directed edge-present branch must miss second quorum by one")
    if on.get("deliver_E") is not True or on.get("deliver_R") is not True:
        raise ProofFailure("edge-present branch must deliver both E and R")
    if on.get("repair_disables_pivot") is not True:
        raise ProofFailure("edge-present branch must explicitly apply pivot repair")

    conclusion = _require_string(cert.get("conclusion"), "conclusion")
    expected_conclusion = "UnsafeObs(G_D)=empty_and_UnsafeObs(G_T)=nonempty"
    if conclusion != expected_conclusion:
        raise ProofFailure(f"unexpected T3 conclusion: {conclusion}")

    return {
        "status": "PASS",
        "theorem": "T3_parametric_quorum_pivot_separation",
        "domain": "all natural f >= 1 under the explicit protocol-schema premises",
        "arithmetic": arithmetic,
        "branch_results": {
            "phase_specific": "two conflicting quorums reachable",
            "directed_edge_absent": "first quorum short by one",
            "directed_edge_present": "second quorum short by one after repair",
        },
        "conclusion": conclusion,
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
