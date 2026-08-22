from __future__ import annotations

"""Premise-ablation and parameter-sensitivity checks for the T3 construction."""

from dataclasses import asdict, dataclass, replace
from random import Random


@dataclass(frozen=True, slots=True)
class SeparationPremises:
    f: int = 1
    first_base_short_by_one: bool = True
    second_base_short_by_one: bool = True
    second_pivot_requires_enabling_evidence: bool = True
    repair_disables_pivot: bool = True
    repair_precedes_second_quorum_opportunity: bool = True
    enabling_and_repair_share_endpoint_edge: bool = True
    phase_specific_grammar_can_split_E_and_R: bool = True


@dataclass(frozen=True, slots=True)
class BranchOutcome:
    deliver_E: bool
    deliver_R: bool
    first_support: int
    second_support: int
    first_certificate: bool
    second_certificate: bool
    unsafe: bool


def _outcome(
    premises: SeparationPremises,
    *,
    deliver_E: bool,
    deliver_R: bool,
) -> BranchOutcome:
    if premises.f < 1:
        raise ValueError("f must be positive")
    quorum = 2 * premises.f + 1
    first_base = quorum - 1 if premises.first_base_short_by_one else quorum
    second_base = quorum - 1 if premises.second_base_short_by_one else quorum

    first_pivot = int(deliver_E)
    first_support = first_base + first_pivot
    first_certificate = first_support >= quorum

    pivot_enabled_for_second = (
        deliver_E or not premises.second_pivot_requires_enabling_evidence
    )
    repaired_in_time = (
        deliver_R
        and premises.repair_disables_pivot
        and premises.repair_precedes_second_quorum_opportunity
        and first_certificate
    )
    second_pivot = int(pivot_enabled_for_second and not repaired_in_time)
    second_support = second_base + second_pivot
    second_certificate = second_support >= quorum

    return BranchOutcome(
        deliver_E=deliver_E,
        deliver_R=deliver_R,
        first_support=first_support,
        second_support=second_support,
        first_certificate=first_certificate,
        second_certificate=second_certificate,
        unsafe=first_certificate and second_certificate,
    )


def _policies(premises: SeparationPremises, grammar: str) -> tuple[tuple[bool, bool], ...]:
    if grammar == "G_T":
        if premises.phase_specific_grammar_can_split_E_and_R:
            return ((True, False),)
        # If phase labels are erased, the purported stronger grammar has the
        # same endpoint-uniform choices as G_D.
        return ((False, False), (True, True))
    if grammar == "G_D":
        if premises.enabling_and_repair_share_endpoint_edge:
            return ((False, False), (True, True))
        # Different endpoint edges can be selected independently by an ordinary
        # directed graph. In particular, E can pass while R is blocked.
        return ((False, False), (False, True), (True, False), (True, True))
    raise ValueError(grammar)


def evaluate_separation(premises: SeparationPremises) -> dict[str, object]:
    typed = tuple(_outcome(premises, deliver_E=e, deliver_R=r) for e, r in _policies(premises, "G_T"))
    directed = tuple(_outcome(premises, deliver_E=e, deliver_R=r) for e, r in _policies(premises, "G_D"))
    typed_unsafe = any(row.unsafe for row in typed)
    directed_unsafe = any(row.unsafe for row in directed)
    return {
        "premises": asdict(premises),
        "type_specific": [asdict(row) for row in typed],
        "directed": [asdict(row) for row in directed],
        "type_specific_unsafe": typed_unsafe,
        "directed_unsafe": directed_unsafe,
        "strict_separation": typed_unsafe and not directed_unsafe,
    }


def premise_ablation_matrix() -> dict[str, object]:
    baseline = SeparationPremises()
    baseline_result = evaluate_separation(baseline)
    if not baseline_result["strict_separation"]:
        raise AssertionError("baseline T3 premises do not yield strict separation")

    fields = (
        "first_base_short_by_one",
        "second_base_short_by_one",
        "second_pivot_requires_enabling_evidence",
        "repair_disables_pivot",
        "repair_precedes_second_quorum_opportunity",
        "enabling_and_repair_share_endpoint_edge",
        "phase_specific_grammar_can_split_E_and_R",
    )
    rows: list[dict[str, object]] = []
    for field in fields:
        mutated = replace(baseline, **{field: False})
        result = evaluate_separation(mutated)
        rows.append(
            {
                "ablated_premise": field,
                "strict_separation_after_ablation": result["strict_separation"],
                "type_specific_unsafe": result["type_specific_unsafe"],
                "directed_unsafe": result["directed_unsafe"],
                "classification": (
                    "NECESSARY_FOR_THIS_CONSTRUCTION"
                    if not result["strict_separation"]
                    else "REDUNDANT_IN_THIS_CONSTRUCTION"
                ),
                "diagnosis": (
                    "G_D gains the unsafe witness"
                    if result["directed_unsafe"]
                    else "G_T loses the unsafe witness"
                    if not result["type_specific_unsafe"]
                    else "separation survives"
                ),
            }
        )

    necessary = [
        row["ablated_premise"]
        for row in rows
        if row["classification"] == "NECESSARY_FOR_THIS_CONSTRUCTION"
    ]
    redundant = [
        row["ablated_premise"]
        for row in rows
        if row["classification"] == "REDUNDANT_IN_THIS_CONSTRUCTION"
    ]
    return {
        "status": "PASS",
        "scope": "necessity for the supplied two-branch construction, not universal protocol-class necessity",
        "baseline": baseline_result,
        "ablations": rows,
        "necessary_premises": necessary,
        "redundant_premises": redundant,
    }


def parameter_sensitivity(max_f: int = 256, random_cases: int = 256, seed: int = 60617) -> dict[str, object]:
    if max_f < 1 or random_cases < 0:
        raise ValueError("invalid sensitivity bounds")
    deterministic = list(range(1, max_f + 1))
    rng = Random(seed)
    random_values = [rng.randrange(1, 10**18) for _ in range(random_cases)]
    values = deterministic + random_values
    failures: list[dict[str, object]] = []
    for f in values:
        result = evaluate_separation(SeparationPremises(f=f))
        if not result["strict_separation"]:
            failures.append({"f": f, "result": result})
    return {
        "status": "PASS" if not failures else "FAIL",
        "deterministic_range": [1, max_f],
        "random_cases": random_cases,
        "random_seed": seed,
        "largest_random_f": max(random_values, default=None),
        "cases_checked": len(values),
        "failures": failures,
    }


def exhaustive_premise_characterization() -> dict[str, object]:
    """Exhaustively characterize strict separation in the seven-flag model.

    This is stronger than one-at-a-time ablation.  It checks all 2^7 truth
    assignments and verifies the exact Boolean characterization

        S2 ∧ D ∧ T ∧ E ∧ X ∧ (S1 ∨ Rq)

    where:
      S1: first base is one below quorum;
      S2: second base is one below quorum;
      Rq: second pivot requires the enabling evidence;
      D: repair disables the pivot;
      T: repair is effective before the second quorum opportunity;
      E: enabling and repair share one endpoint edge;
      X: phase-specific grammar can split enabling and repair.

    The characterization is only for this supplied two-branch Boolean model.
    It is not a universal necessary-and-sufficient theorem for all BFT
    protocols.
    """

    from itertools import product

    fields = (
        "first_base_short_by_one",
        "second_base_short_by_one",
        "second_pivot_requires_enabling_evidence",
        "repair_disables_pivot",
        "repair_precedes_second_quorum_opportunity",
        "enabling_and_repair_share_endpoint_edge",
        "phase_specific_grammar_can_split_E_and_R",
    )
    rows: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []
    strict_patterns: list[str] = []
    for bits in product((False, True), repeat=len(fields)):
        values = dict(zip(fields, bits, strict=True))
        premises = SeparationPremises(**values)
        actual = bool(evaluate_separation(premises)["strict_separation"])
        predicted = bool(
            values["second_base_short_by_one"]
            and values["repair_disables_pivot"]
            and values["repair_precedes_second_quorum_opportunity"]
            and values["enabling_and_repair_share_endpoint_edge"]
            and values["phase_specific_grammar_can_split_E_and_R"]
            and (
                values["first_base_short_by_one"]
                or values["second_pivot_requires_enabling_evidence"]
            )
        )
        pattern = "".join("1" if value else "0" for value in bits)
        row = {
            "pattern": pattern,
            **values,
            "actual_strict_separation": actual,
            "characterization_predicts": predicted,
        }
        rows.append(row)
        if actual:
            strict_patterns.append(pattern)
        if actual != predicted:
            mismatches.append(row)

    globally_necessary = [
        field
        for field in fields
        if all(row[field] for row in rows if row["actual_strict_separation"])
    ]
    return {
        "status": "PASS" if not mismatches else "FAIL",
        "assignments_checked": len(rows),
        "strict_assignments": len(strict_patterns),
        "strict_patterns_in_field_order": strict_patterns,
        "field_order": list(fields),
        "exact_characterization": (
            "second_base_short_by_one AND repair_disables_pivot AND "
            "repair_precedes_second_quorum_opportunity AND "
            "enabling_and_repair_share_endpoint_edge AND "
            "phase_specific_grammar_can_split_E_and_R AND "
            "(first_base_short_by_one OR "
            "second_pivot_requires_enabling_evidence)"
        ),
        "globally_necessary_in_boolean_model": globally_necessary,
        "mismatches": mismatches,
        "truth_table": rows,
        "scope": (
            "exact for the supplied seven-flag two-branch model; not a universal "
            "protocol-class characterization"
        ),
    }
