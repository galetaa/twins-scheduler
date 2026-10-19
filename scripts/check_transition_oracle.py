#!/usr/bin/env python3
"""Independently audit direct and abstraction-based finite-LTS synthesis.

The oracle enumerates total Boolean fine policies and split subsets, then uses
plain reachability on raw protocol edges.  It never calls product successors,
partial-policy inference, certificate replay, or an optimizer to obtain its
answer.  Both optimizers and their independent certificates are comparison
targets.  The report has no timings and is reproducible from the explicit seed
and finite family definitions below.

Run: uv run python scripts/check_transition_oracle.py
Output: ${TWINS_OUTPUT_ROOT:-repository}/results/transition_bridge/random_oracle.json
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
from random import Random
from typing import Any

from twins_scheduler.transition_abstraction import synthesize_via_abstraction, verify_abstraction_run
from twins_scheduler.transition_examples import set_cover_problem
from twins_scheduler.transition_synthesis import Problem, Transition, synthesize, verify_certificate


CONFIG = {
    "random": {
        "seed": 20261020,
        "cases": 400,
        "state_count_inclusive_range": [1, 6],
        "fine_key_count_inclusive_range": [0, 4],
        "coarse_fibre_count_inclusive_range": [1, 3],
        "input_edge_count_inclusive_range": [0, 14],
        "cost_inclusive_range": [0, 4],
        "initial_state": 0,
        "unsafe_state_probability": "1/3 independently per state",
        "internal_edge_probability": "1/4, or 1 when there are no fine keys",
        "allowed_split_probability": "2/3 independently per fibre",
        "required_given_allowed_probability": "1/4 independently per allowed fibre in sorted order",
        "other_draws": "independent uniform source, target, fine key, Boolean value and coarse fibre",
        "parallel_edges_and_cycles": True,
    },
    "edge_family": {
        "states": ["initial", "middle", "unsafe"],
        "initial": 0, "unsafe": [2], "key_fibres": [0, 0, 1],
        "candidate_edges": [
            [0, 1, 0, False], [0, 1, 0, True],
            [1, 2, 1, False], [1, 2, 1, True],
            [1, 0, 0, False], [1, 0, 0, True],
            [2, 1, None, None], [0, 0, None, None],
        ],
        "cost_vectors": [[2, 3], [0, 3]],
        "constraints": [
            {"allowed": [], "required": []},
            {"allowed": [0], "required": []},
            {"allowed": [0, 1], "required": [1]},
            {"allowed": [0, 1], "required": [0, 1]},
        ],
        "enumeration": "all 256 edge subsets times two cost vectors times four constraints",
    },
    "set_cover": {
        "universe": [0, 1, 2], "set_count": 3, "costs": [4, 2, 1],
        "enumeration": "all 512 ordered triples drawn from the eight universe subsets",
    },
}


def digest(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True).encode("utf-8")).hexdigest()


def raw_minimum(data: dict[str, Any]) -> tuple[int | None, int, int]:
    """Reference answer from raw total policies and ordinary graph closure."""
    fibres, costs = data["key_fibres"], data["costs"]
    allowed, required = set(data["allowed_split"]), set(data["required_split"])
    unsafe = set(data["unsafe"])
    best = None
    enumerated_pairs = admissible_pairs = 0
    for selected in product((False, True), repeat=len(costs)):
        split = {i for i, present in enumerate(selected) if present}
        if not required <= split <= allowed:
            continue
        paid = sum(costs[i] for i in split)
        for policy in product((False, True), repeat=len(fibres)):
            enumerated_pairs += 1
            if any(fibres[i] == fibres[j] and fibres[i] not in split and policy[i] != policy[j]
                   for i in range(len(fibres)) for j in range(len(fibres))):
                continue
            admissible_pairs += 1
            reachable = {data["initial"]}
            while True:
                later = reachable | {
                    edge["target"] for edge in data["transitions"]
                    if edge["source"] in reachable
                    and (edge["key"] is None or policy[edge["key"]] == edge["value"])
                }
                if later == reachable:
                    break
                reachable = later
            if reachable & unsafe:
                best = paid if best is None else min(best, paid)
    return best, enumerated_pairs, admissible_pairs


def cases():
    rng = Random(CONFIG["random"]["seed"])
    for case in range(CONFIG["random"]["cases"]):
        n, f, m = rng.randrange(1, 7), rng.randrange(5), rng.randrange(1, 4)
        fibres = tuple(rng.randrange(m) for _ in range(f))
        costs = tuple(rng.randrange(5) for _ in range(m))
        allowed = frozenset(i for i in range(m) if rng.randrange(3))
        required = frozenset(i for i in sorted(allowed) if rng.randrange(4) == 0)
        edges = []
        for _ in range(rng.randrange(15)):
            key = None if not f or rng.randrange(4) == 0 else rng.randrange(f)
            # Keep this draw order fixed: source, target, then Boolean value.
            edges.append(Transition(rng.randrange(n), rng.randrange(n), key,
                                    None if key is None else bool(rng.randrange(2))))
        problem = Problem(tuple(map(str, range(n))), 0,
                          frozenset(i for i in range(n) if rng.randrange(3) == 0),
                          tuple(edges), fibres, costs, allowed, required)
        yield "random", case, problem, None

    config = CONFIG["edge_family"]
    edges = tuple(Transition(*edge) for edge in config["candidate_edges"])
    case = 0
    for mask in range(1 << len(edges)):
        selected = tuple(edge for index, edge in enumerate(edges) if mask >> index & 1)
        for costs, constraint in product(config["cost_vectors"], config["constraints"]):
            problem = Problem(tuple(config["states"]), config["initial"], frozenset(config["unsafe"]),
                              selected, tuple(config["key_fibres"]), tuple(costs),
                              frozenset(constraint["allowed"]), frozenset(constraint["required"]))
            yield "edge_family", case, problem, None
            case += 1

    config = CONFIG["set_cover"]
    universe = frozenset(config["universe"])
    subsets = tuple(frozenset(i for i in universe if mask >> i & 1) for mask in range(8))
    for case, chosen in enumerate(product(range(8), repeat=3)):
        family = tuple(subsets[index] for index in chosen)
        # This reduction-specific answer does not even use protocol reachability.
        best = None
        for selected in product((False, True), repeat=3):
            cover = frozenset().union(*(members for members, yes in zip(family, selected) if yes))
            if cover == universe:
                paid = sum(c for c, yes in zip(config["costs"], selected) if yes)
                best = paid if best is None else min(best, paid)
        problem = set_cover_problem(len(universe), family, config["costs"])
        yield "set_cover", case, problem, {"minimum_cost": best, "subsets_checked": 8}


def run_oracle():
    families: dict[str, dict[str, Any]] = {}
    inputs = []
    outcomes = []
    mismatch_examples = []
    for family, case, problem, cover in cases():
        data = problem.to_dict()
        inputs.append({"family": family, "case": case, "problem": data})
        expected, enumerated, admissible = raw_minimum(data)
        counts = families.setdefault(family, {
            "cases": 0, "optimal_cases": 0, "infeasible_cases": 0,
            "enumerated_policy_split_pairs": 0, "admissible_policy_split_pairs": 0,
            "direct_minimum_comparisons": 0, "abstraction_minimum_comparisons": 0,
            "direct_certificate_checks": 0, "abstraction_run_checks": 0,
            "abstract_iterations_checked": 0, "eliminated_policies_checked": 0,
            "max_abstraction_iterations": 0, "set_cover_subset_checks": 0,
            "minimum_cost_mismatches": 0, "certificate_failures": 0,
            "set_cover_mismatches": 0,
        })
        counts["cases"] += 1
        counts["optimal_cases" if expected is not None else "infeasible_cases"] += 1
        counts["enumerated_policy_split_pairs"] += enumerated
        counts["admissible_policy_split_pairs"] += admissible
        if cover is not None:
            counts["set_cover_subset_checks"] += cover["subsets_checked"]
            if cover["minimum_cost"] != expected:
                counts["set_cover_mismatches"] += 1
                mismatch_examples.append({"family": family, "case": case, "kind": "set-cover reduction"})
        direct = synthesize(problem)
        run = synthesize_via_abstraction(problem)
        counts["direct_minimum_comparisons"] += 1
        counts["abstraction_minimum_comparisons"] += 1
        counts["direct_certificate_checks"] += 1
        counts["abstraction_run_checks"] += 1
        try:
            direct_audit = verify_certificate(direct, expected_problem=problem)
            abstraction_audit = verify_abstraction_run(run, expected_concrete=problem)
            if direct_audit["status"] != "PASS" or abstraction_audit["status"] != "PASS":
                raise ValueError("a certificate checker did not return PASS")
        except ValueError as error:
            counts["certificate_failures"] += 1
            mismatch_examples.append({"family": family, "case": case, "kind": "certificate", "error": str(error)})
            continue
        actual_abstract = abstraction_audit["minimum_cost"]
        for target, actual in (("direct", direct["minimum_cost"]), ("abstraction", actual_abstract)):
            if actual != expected:
                counts["minimum_cost_mismatches"] += 1
                mismatch_examples.append({"family": family, "case": case, "kind": target,
                                          "expected": expected, "actual": actual})
        iterations = abstraction_audit["iterations"]
        counts["abstract_iterations_checked"] += iterations
        counts["eliminated_policies_checked"] += abstraction_audit["eliminated_policies"]
        counts["max_abstraction_iterations"] = max(counts["max_abstraction_iterations"], iterations)
        if iterations > len(problem.states):
            raise AssertionError("strict-refinement termination bound failed")
        outcomes.append({"family": family, "case": case, "oracle_minimum_cost": expected,
                         "direct_minimum_cost": direct["minimum_cost"],
                         "abstract_minimum_cost": actual_abstract,
                         "abstract_iterations": iterations,
                         "final_abstract_states": abstraction_audit["final_abstract_states"]})
    additive_fields = set(next(iter(families.values()))) - {"max_abstraction_iterations"}
    counts = {field: sum(family[field] for family in families.values()) for field in sorted(additive_fields)}
    counts["max_abstraction_iterations"] = max(family["max_abstraction_iterations"] for family in families.values())
    mismatches = sum(counts[key] for key in ("minimum_cost_mismatches", "certificate_failures", "set_cover_mismatches"))
    return {
        "schema": "transition-synthesis-independent-oracle/v1",
        "status": "PASS" if mismatches == 0 else "FAIL",
        "config": CONFIG, "counts": counts, "families": families,
        "input_sha256": digest(inputs), "outcome_sha256": digest(outcomes),
        "mismatches": mismatches, "mismatch_examples": mismatch_examples[:10],
        "scope": "400 seeded arbitrary finite LTSs, 2048 members of an exhaustive edge/cost/constraint family, and 512 exhaustive Set Cover reductions; no claim of exhaustive arbitrary-LTS coverage",
        "oracle": "total static Boolean policies times allowed/required split subsets, followed by raw protocol graph reachability; independent of product and abstraction algorithms",
        "costs_and_runtime": "exact nonnegative integers; no runtime measurements in this deterministic report",
    }


def main():
    report = run_oracle()
    output_root = Path(os.environ.get("TWINS_OUTPUT_ROOT", Path(__file__).resolve().parents[1]))
    output = output_root / "results" / "transition_bridge" / "random_oracle.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "counts": report["counts"],
                      "mismatches": report["mismatches"], "output": str(output)}, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
