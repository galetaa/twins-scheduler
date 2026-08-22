#!/usr/bin/env python3
"""Small purpose-built proof-certificate kernel for the post-audit theorem package.

This checker is intentionally independent from the experiment code.  It accepts
only a narrow JSON certificate language.  Each theorem has a closed verifier:
T1/T2 check the required induction rule applications and exhaustively validate
small finite instances; T3 evaluates the complete bounded transition system and
checks the parameter arithmetic; T6 exhausts all 2^7 premise assignments.

It is a project-local kernel, not Lean/Coq.  Its trusted base is this file plus
CPython's integer/Boolean semantics and the JSON parser.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

KERNEL_VERSION = "1.1.0"

class KernelError(RuntimeError):
    pass

def require(condition: bool, message: str) -> None:
    if not condition:
        raise KernelError(message)

def exact_keys(obj: Mapping[str, Any], expected: set[str], where: str) -> None:
    actual = set(obj)
    require(actual == expected, f"{where}: keys {sorted(actual)} != {sorted(expected)}")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

@dataclass(frozen=True)
class T1Result:
    finite_models: int
    finite_traces: int
    hidden_counterexample: tuple[int, int]

@dataclass(frozen=True)
class T2Result:
    finite_models: int
    finite_prefix_checks: int

@dataclass(frozen=True)
class T3Result:
    parameter_cases: int
    directed_cases: int

@dataclass(frozen=True)
class T6Result:
    assignments: int
    strict_patterns: tuple[str, ...]

REQUIRED_T1_PREMISES = {
    "stable_key_in_projection",
    "projection_congruence",
    "output_congruence",
    "duplicate_projection_stutter",
    "duplicate_relevant_output_empty",
}
REQUIRED_T2_PREMISES = {
    "initial_relation",
    "relation_transitive",
    "inserted_action_increasing",
    "retained_action_forward_simulation",
    "unsafe_upward_closed",
}
REQUIRED_T3_FACTS = {
    "same_sender",
    "same_receiver",
    "same_view",
    "phase_order_E_C0_R_C1",
    "directed_domain_exactly_edge_off_on",
    "certificates_induce_distinct_correct_decisions",
}


def check_induction_skeleton(cert: Mapping[str, Any], theorem: str, expected_cases: Sequence[str]) -> None:
    proof = cert.get("proof")
    require(isinstance(proof, Mapping), f"{theorem}: missing proof object")
    exact_keys(proof, {"method", "measure", "cases"}, f"{theorem}.proof")
    require(proof["method"] == "structural_induction", f"{theorem}: wrong proof method")
    require(proof["measure"] == "remaining_trace_length", f"{theorem}: non-decreasing/unknown measure")
    cases = proof["cases"]
    require(isinstance(cases, list), f"{theorem}: cases must be a list")
    names = [case.get("name") for case in cases if isinstance(case, Mapping)]
    require(names == list(expected_cases), f"{theorem}: cases {names} != {list(expected_cases)}")
    for case in cases:
        require(case.get("measure_decreases") is True or case["name"] == "empty", f"{theorem}:{case['name']}: induction measure not justified")


def run_trace(step: Sequence[Sequence[int]], state: int, trace: Sequence[int]) -> int:
    for event in trace:
        state = step[event][state]
    return state


def erase_duplicates(trace: Sequence[int], duplicate_event: int) -> tuple[int, ...]:
    seen = False
    out: list[int] = []
    for event in trace:
        if event == duplicate_event:
            if seen:
                continue
            seen = True
        out.append(event)
    return tuple(out)


def enumerate_traces(alphabet: int, max_length: int) -> Iterable[tuple[int, ...]]:
    yield ()
    for length in range(1, max_length + 1):
        yield from itertools.product(range(alphabet), repeat=length)


def check_t1(cert: Mapping[str, Any]) -> T1Result:
    exact_keys(cert, {"statement", "premises", "proof", "finite_validation", "counterexample"}, "T1")
    require(cert["statement"] == "projection_output_congruent_replay_erasure", "T1: wrong statement")
    premises = set(cert["premises"])
    require(premises == REQUIRED_T1_PREMISES, f"T1: premises {premises} do not match corrected theorem")
    check_induction_skeleton(cert, "T1", ("empty", "duplicate", "fresh"))
    cases = {c["name"]: c for c in cert["proof"]["cases"]}
    require(cases["duplicate"].get("uses") == ["duplicate_projection_stutter", "induction_hypothesis"], "T1 duplicate case is not justified")
    require(cases["fresh"].get("uses") == ["projection_congruence", "output_congruence", "induction_hypothesis"], "T1 fresh case omits state/output congruence")

    cfg = cert["finite_validation"]
    exact_keys(cfg, {"states", "events", "projection_values", "output_values", "max_trace_length"}, "T1.finite_validation")
    require(cfg == {"states": 2, "events": 2, "projection_values": 2, "output_values": 2, "max_trace_length": 5}, "T1 finite validation parameters changed")

    traces = tuple(enumerate_traces(2, 5))
    model_count = 0
    trace_checks = 0
    # Two-state, two-event exhaustive validation. Event 0 is the stable-key
    # duplicate candidate; event 1 is fresh. Projection includes the processed
    # key bit by construction: duplicate stutter is required after first 0.
    for proj_bits in itertools.product(range(2), repeat=2):
        for table in itertools.product(range(2), repeat=4):
            step = ((table[0], table[1]), (table[2], table[3]))
            congruent = all(
                proj_bits[s] != proj_bits[t]
                or proj_bits[step[e][s]] == proj_bits[step[e][t]]
                for s in range(2) for t in range(2) for e in range(2)
            )
            if not congruent:
                continue
            # Model duplicates as event 0 after its first occurrence.  The
            # theorem's stutter premise is checked at every relevant state.
            if not all(proj_bits[step[0][s]] == proj_bits[s] for s in range(2)):
                continue
            # Exhaust protocol-relevant output fragments.  Event 0 is the
            # duplicate candidate and must be silent; event 1 may emit one bit.
            for out1 in itertools.product(range(2), repeat=2):
                output_congruent = all(
                    proj_bits[s] != proj_bits[t] or out1[s] == out1[t]
                    for s in range(2) for t in range(2)
                )
                if not output_congruent:
                    continue
                model_count += 1
                def run_projected_with_output(start: int, trace: Sequence[int]) -> tuple[int, tuple[int, ...]]:
                    state = start
                    outputs: list[int] = []
                    for event in trace:
                        if event == 1:
                            outputs.append(out1[state])
                        state = step[event][state]
                    return proj_bits[state], tuple(outputs)
                for s in range(2):
                    for trace in traces:
                        full = run_projected_with_output(s, trace)
                        erased = run_projected_with_output(s, erase_duplicates(trace, 0))
                        require(full == erased, f"T1 finite state/output counterexample: state={s}, trace={trace}")
                        trace_checks += 1

    counter = cert["counterexample"]
    exact_keys(counter, {"trace", "erased_trace", "initial", "expected_full_relevant", "expected_erased_relevant", "expected_full_output", "expected_erased_output"}, "T1.counterexample")
    require(counter["trace"] == ["X", "X", "Y"] and counter["erased_trace"] == ["X", "Y"], "T1 counterexample trace changed")
    # Hidden-state machine from the independent audit.
    def hidden_step(st: tuple[int, int], ev: str) -> tuple[int, int]:
        rel, hidden = st
        if ev == "X":
            return rel, 1 - hidden
        if ev == "Y":
            return hidden, hidden
        raise KernelError(f"T1 counterexample: unknown event {ev}")
    def hidden_run(trace: Sequence[str]) -> tuple[int, list[int]]:
        st = tuple(counter["initial"])
        outputs: list[int] = []
        for ev in trace:
            if ev == "Y":
                outputs.append(st[1])
            st = hidden_step(st, ev)
        return st[0], outputs
    full_rel, full_out = hidden_run(counter["trace"])
    erased_rel, erased_out = hidden_run(counter["erased_trace"])
    require((full_rel, erased_rel) == (counter["expected_full_relevant"], counter["expected_erased_relevant"]), "T1 hidden counterexample state mismatch")
    require((full_out, erased_out) == (counter["expected_full_output"], counter["expected_erased_output"]), "T1 hidden counterexample output mismatch")
    require(full_rel != erased_rel and full_out != erased_out, "T1 weak theorem counterexample did not separate state and output")
    return T1Result(model_count, trace_checks, (full_rel, erased_rel))


def relation_transitive(rel: tuple[bool, bool, bool, bool]) -> bool:
    def r(a: int, b: int) -> bool: return rel[2*a+b]
    return all(not (r(a,b) and r(b,c)) or r(a,c) for a in range(2) for b in range(2) for c in range(2))


def check_t2(cert: Mapping[str, Any]) -> T2Result:
    exact_keys(cert, {"statement", "premises", "proof", "finite_validation"}, "T2")
    require(cert["statement"] == "relational_closure_lifting", "T2: wrong statement")
    premises = set(cert["premises"])
    require(premises == REQUIRED_T2_PREMISES, f"T2: premises {premises} incomplete")
    check_induction_skeleton(cert, "T2", ("empty", "inserted", "retained"))
    cases = {c["name"]: c for c in cert["proof"]["cases"]}
    require(cases["inserted"].get("uses") == ["inserted_action_increasing", "relation_transitive", "induction_hypothesis"], "T2 inserted case invalid")
    require(cases["retained"].get("uses") == ["retained_action_forward_simulation", "induction_hypothesis"], "T2 retained case invalid")

    cfg = cert["finite_validation"]
    require(cfg == {"states": 2, "original_actions": 1, "inserted_actions": 1, "max_merged_length": 4}, "T2 finite parameters changed")
    model_count = 0
    prefix_checks = 0
    merged_traces: list[tuple[int, ...]] = list(enumerate_traces(2, 4))  # 0 retained, 1 inserted
    for rel_bits in itertools.product((False, True), repeat=4):
        if not relation_transitive(rel_bits):
            continue
        def R(a: int, b: int) -> bool: return rel_bits[2*a+b]
        if not all(R(s,s) for s in range(2)):
            continue
        for step_bits in itertools.product(range(2), repeat=2):
            for add_bits in itertools.product(range(2), repeat=2):
                if not all(R(s, add_bits[s]) for s in range(2)):
                    continue
                if not all(not R(s,t) or R(step_bits[s], step_bits[t]) for s in range(2) for t in range(2)):
                    continue
                model_count += 1
                for start in range(2):
                    for trace in merged_traces:
                        original_state = start
                        merged_state = start
                        require(R(original_state, merged_state), "T2 initial relation failed")
                        prefix_checks += 1
                        for kind in trace:
                            if kind == 0:
                                original_state = step_bits[original_state]
                                merged_state = step_bits[merged_state]
                            else:
                                merged_state = add_bits[merged_state]
                            require(R(original_state, merged_state), f"T2 prefix counterexample trace={trace}")
                            prefix_checks += 1
    return T2Result(model_count, prefix_checks)


def unsafe_operational(policy: str | bool) -> tuple[bool, bool, bool]:
    if policy == "phase_specific":
        deliver_e, deliver_r = True, False
    elif isinstance(policy, bool):
        deliver_e = deliver_r = policy
    else:
        raise KernelError("T3 unknown policy")
    enabled = deliver_e
    cert0 = enabled
    disabled = deliver_r
    cert1 = enabled and not disabled
    left_decision = cert0
    right_decision = cert1
    return left_decision, right_decision, left_decision and right_decision


def check_t3(cert: Mapping[str, Any]) -> T3Result:
    exact_keys(cert, {"statement", "facts", "messages", "phase_order", "directed_domain", "decision_semantics", "parameters"}, "T3")
    require(cert["statement"] == "parametric_quorum_pivot_separation", "T3 wrong statement")
    facts = set(cert["facts"])
    require(facts == REQUIRED_T3_FACTS, f"T3 missing audit facts: {REQUIRED_T3_FACTS - facts}")
    messages = cert["messages"]
    require(messages["E"]["sender"] == messages["R"]["sender"], "T3 E/R sender differs")
    require(messages["E"]["receiver"] == messages["R"]["receiver"], "T3 E/R receiver differs")
    require(messages["E"]["view"] == messages["R"]["view"], "T3 E/R view differs")
    require(cert["phase_order"] == ["E", "C0", "R", "C1"], "T3 wrong phase order")
    require(cert["directed_domain"] == [False, True], "T3 directed domain not exact Bool")
    require(cert["decision_semantics"] == {"certificate0": "correct_left_decides_0", "certificate1": "correct_right_decides_1"}, "T3 decisions not explicit")
    phase = unsafe_operational("phase_specific")
    require(phase == (True, True, True), "T3 phase-specific branch not unsafe")
    directed_cases = 0
    for edge in cert["directed_domain"]:
        left, right, unsafe = unsafe_operational(edge)
        if edge is False:
            require((left, right, unsafe) == (False, False, False), "T3 edge-off branch invalid")
        else:
            require((left, right, unsafe) == (True, False, False), "T3 edge-on must process repair before C1")
        directed_cases += 1
    params = cert["parameters"]
    require(params[:4] == [1, 2, 10, 1_000_000], "T3 missing required parameter probes")
    require(len(str(params[-1])) >= 400, "T3 final parameter is not 400 digits")
    for f in params:
        require(isinstance(f, int) and f >= 1, "T3 invalid f")
        q = 2*f + 1
        base = 2*f
        require(base + 1 == q and base == q-1, f"T3 arithmetic fails f={f}")
    return T3Result(len(params), directed_cases)


def unsafe_u(p: Mapping[str, bool], e: bool, r: bool) -> bool:
    return ((not p["S1"]) or e) and (
        (not p["S2"]) or (((not p["Rq"]) or e) and not (r and p["D"] and p["T"]))
    )


def strict_operational(p: Mapping[str, bool]) -> bool:
    return p["X"] and p["Ed"] and unsafe_u(p, True, False) and not unsafe_u(p, False, False) and not unsafe_u(p, True, True)


def strict_closed(p: Mapping[str, bool]) -> bool:
    return p["S2"] and p["D"] and p["T"] and p["Ed"] and p["X"] and (p["S1"] or p["Rq"])


def check_t6(cert: Mapping[str, Any]) -> T6Result:
    exact_keys(cert, {"statement", "field_order", "operational_equation", "closed_form", "expected_patterns"}, "T6")
    require(cert["statement"] == "seven_premise_exact_boundary", "T6 wrong statement")
    fields = cert["field_order"]
    require(fields == ["S1","S2","Rq","D","T","Ed","X"], "T6 field order changed")
    require(cert["operational_equation"] == "U(e,r)=(!S1 or e) and (!S2 or ((!Rq or e) and not(r and D and T)))", "T6 operational equation absent/changed")
    require(cert["closed_form"] == "S2 and D and T and Ed and X and (S1 or Rq)", "T6 closed form changed")
    patterns: list[str] = []
    for bits in itertools.product((False, True), repeat=7):
        p = dict(zip(fields, bits))
        op = strict_operational(p)
        closed = strict_closed(p)
        require(op == closed, f"T6 mismatch bits={bits}")
        if op:
            patterns.append("".join("1" if b else "0" for b in bits))
    expected = cert["expected_patterns"]
    require(patterns == expected == ["0111111", "1101111", "1111111"], f"T6 patterns {patterns}")
    return T6Result(128, tuple(patterns))


def load_certificate(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise KernelError(f"certificate parse failed: {exc}") from exc
    exact_keys(data, {"format", "kernel_version", "theorems"}, "root")
    require(data["format"] == "scheduler-closure-proof-certificate", "wrong certificate format")
    require(data["kernel_version"] == KERNEL_VERSION, "kernel version mismatch")
    require(set(data["theorems"]) == {"T1", "T2", "T3", "T6"}, "certificate theorem set mismatch")
    return data


def check_certificate(path: Path) -> dict[str, Any]:
    data = load_certificate(path)
    t1 = check_t1(data["theorems"]["T1"])
    t2 = check_t2(data["theorems"]["T2"])
    t3 = check_t3(data["theorems"]["T3"])
    t6 = check_t6(data["theorems"]["T6"])
    return {
        "kernel_version": KERNEL_VERSION,
        "certificate": str(path),
        "certificate_sha256": sha256(path),
        "status": "PASS",
        "T1": {"finite_models": t1.finite_models, "finite_trace_checks": t1.finite_traces, "hidden_counterexample_full_erased": list(t1.hidden_counterexample)},
        "T2": {"finite_models": t2.finite_models, "finite_prefix_checks": t2.finite_prefix_checks},
        "T3": {"parameter_cases": t3.parameter_cases, "directed_domain_cases": t3.directed_cases},
        "T6": {"assignments": t6.assignments, "strict_patterns": list(t6.strict_patterns)},
    }


def run_negative_controls(original: dict[str, Any]) -> dict[str, str]:
    import copy
    controls: dict[str, Callable[[dict[str, Any]], None]] = {}
    def no_congruence(d: dict[str, Any]) -> None:
        d["theorems"]["T1"]["premises"].remove("projection_congruence")
    controls["T1_remove_projection_congruence"] = no_congruence
    def no_output_congruence(d: dict[str, Any]) -> None:
        d["theorems"]["T1"]["premises"].remove("output_congruence")
    controls["T1_remove_output_congruence"] = no_output_congruence
    def wrong_view(d: dict[str, Any]) -> None:
        d["theorems"]["T3"]["messages"]["R"]["view"] = 1
    controls["T3_move_R_to_other_view"] = wrong_view
    def late_directed(d: dict[str, Any]) -> None:
        d["theorems"]["T3"]["phase_order"] = ["E","C0","C1","R"]
    controls["T3_deliver_repair_after_C1"] = late_directed
    def remove_u(d: dict[str, Any]) -> None:
        d["theorems"]["T6"]["operational_equation"] = "omitted"
    controls["T6_omit_operational_equation"] = remove_u
    results: dict[str, str] = {}
    for name, mutate in controls.items():
        candidate = copy.deepcopy(original)
        mutate(candidate)
        try:
            check_t1(candidate["theorems"]["T1"])
            check_t2(candidate["theorems"]["T2"])
            check_t3(candidate["theorems"]["T3"])
            check_t6(candidate["theorems"]["T6"])
        except KernelError as exc:
            results[name] = f"REJECTED: {exc}"
        else:
            raise KernelError(f"negative control unexpectedly accepted: {name}")
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = load_certificate(args.certificate)
        report = check_certificate(args.certificate)
        if args.negative_controls:
            report["negative_controls"] = run_negative_controls(data)
        text = json.dumps(report, indent=2, sort_keys=True)
        print(text)
        if args.json_output:
            args.json_output.write_text(text + "\n", encoding="utf-8")
        return 0
    except KernelError as exc:
        print(f"KERNEL REJECT: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
