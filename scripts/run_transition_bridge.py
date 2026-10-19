#!/usr/bin/env python3
"""Reproduce or independently verify general transition-abstraction certificates."""
from __future__ import annotations

import argparse
import gzip
import json
import os
from pathlib import Path
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/python"))

from twins_scheduler.coupled_protocol import (
    build_model, exhaustive_policy_oracle, quotient_audit_order,
    replay_protocol_witness, semantic_examples,
)
from twins_scheduler.transition_abstraction import (
    synthesize_via_abstraction, verify_abstraction_run,
)
from twins_scheduler.transition_synthesis import Problem, SynthesisLimit


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode()
    if path.suffix == ".gz":
        data = gzip.compress(data, mtime=0)
    path.write_bytes(data)


def read_json(path: Path):
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    return json.loads(data)


def study() -> dict:
    output = Path(os.environ.get("TWINS_OUTPUT_ROOT", ROOT))
    log = Path(os.environ.get("TWINS_LOG_DIR", output / "build_logs"))
    target = output / "results/transition_bridge"
    rows, timings = [], []

    def run_case(name, problem, *, initial_map=None, model=None):
        started = perf_counter()
        result = synthesize_via_abstraction(problem, initial_map)
        audit = verify_abstraction_run(result, expected_concrete=problem)
        elapsed = perf_counter() - started
        oracle = exhaustive_policy_oracle(problem)
        if audit["minimum_cost"] != oracle["minimum_cost"]:
            raise AssertionError(f"abstraction/total-policy optimum mismatch: {name}")
        row = {
            "case": name, "status": audit["claim"], "minimum_cost": audit["minimum_cost"],
            "concrete_states": len(problem.states), "concrete_transitions": len(problem.transitions),
            "iterations": audit["iterations"], "eliminated_policies": audit["eliminated_policies"],
            "final_abstract_states": audit["final_abstract_states"],
            "final_abstract_transitions": len(result["iterations"][-1]["abstract"]["transitions"]),
            "lower_bounds": [item["abstract_certificate"]["minimum_cost"] for item in result["iterations"]],
            "state_counts": [len(item["abstract"]["states"]) for item in result["iterations"]],
            "total_policies_checked_by_oracle": oracle["total_policies"],
            "certificate": f"certificates/{name}.json.gz",
            "problem_sha256": problem.digest(),
        }
        if model is not None and result["bridge"]["concrete_witness"] is not None:
            witness = result["bridge"]["concrete_witness"]
            replay = replay_protocol_witness(model, witness["transitions"], witness["policy"])
            if not replay["unsafe"] or not all(replay["audit"].values()):
                raise AssertionError("concrete guarded replay failed")
            write_json(target / f"replays/{name}.json.gz", replay)
            row["guarded_replay"] = {
                "unsafe": replay["unsafe"], "decisions": replay["decisions"],
                "audit_checks": len(replay["audit"]), "transition_count": len(replay["schedule"]),
            }
        write_json(target / row["certificate"], result)
        rows.append(row)
        timings.append({"case": name, "seconds": round(elapsed, 6)})

    for name, problem in semantic_examples().items():
        run_case(name, problem)
    mutant = build_model()
    run_case("coupled_quorum_from_coarsest", mutant.problem, model=mutant)
    _, audit_map = quotient_audit_order(mutant)
    run_case("coupled_quorum_audit_quotient", mutant.problem, initial_map=audit_map, model=mutant)
    baseline = build_model("BASELINE")
    run_case("coupled_quorum_baseline", baseline.problem)
    try:
        synthesize_via_abstraction(mutant.problem, max_refinements=0)
    except SynthesisLimit as error:
        cutoff = {"status": "unknown", "reason": str(error)}
    else:
        raise AssertionError("configured zero-refinement limit should be reached")
    summary = {
        "status": "PASS", "model_scope": "complete supplied finite transition systems; static Boolean admission",
        "cases": rows, "optimum_mismatches": 0,
        "all_edge_simulations_checked": len(rows),
        "all_iterations_independently_checked": sum(row["iterations"] for row in rows),
        "total_eliminated_policies": sum(row["eliminated_policies"] for row in rows),
        "resource_limit_control": cutoff,
        "native_client_refinement": False,
    }
    write_json(target / "bridge_summary.json", summary)
    write_json(log / "transition_bridge_timings.json", timings)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--study", action="store_true")
    mode.add_argument("--input", type=Path)
    mode.add_argument("--verify", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect-input", type=Path)
    parser.add_argument("--max-refinements", type=int)
    parser.add_argument("--max-product-states", type=int, default=2_000_000)
    args = parser.parse_args()
    if args.study:
        result = study()
        print(json.dumps({"status": result["status"], "cases": len(result["cases"]),
                          "iterations": result["all_iterations_independently_checked"],
                          "optimum_mismatches": result["optimum_mismatches"]}, sort_keys=True))
        return
    if args.verify:
        expected = None if args.expect_input is None else Problem.from_dict(read_json(args.expect_input))
        print(json.dumps(verify_abstraction_run(read_json(args.verify), expected_concrete=expected), sort_keys=True))
        return
    if args.output is None:
        parser.error("--input requires --output")
    problem = Problem.from_dict(read_json(args.input))
    try:
        result = synthesize_via_abstraction(problem, max_refinements=args.max_refinements,
                                           max_product_states=args.max_product_states)
    except SynthesisLimit as error:
        write_json(args.output, {"status": "unknown", "reason": str(error), "problem_sha256": problem.digest()})
        print(json.dumps({"status": "unknown", "reason": str(error)}, sort_keys=True))
        return
    write_json(args.output, result)
    print(json.dumps(verify_abstraction_run(result, expected_concrete=problem), sort_keys=True))


if __name__ == "__main__":
    main()
