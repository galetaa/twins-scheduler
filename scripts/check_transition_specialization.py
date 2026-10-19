#!/usr/bin/env python3
"""Compare the pivot specialization, explicit LTS, and raw policy/order oracle.

All directed repair graphs with one or two vertices are included, including
self-loops.  Two weight profiles have every quota pair through total weight+1.
Additional allowed/required profiles and all 219 labelled four-event posets
exercise permissions, arbitrary order constraints and suppressed opportunities.
The exporter and raw oracle do not use the repair graph/capacity characterization.

Run: uv run python scripts/check_transition_specialization.py
"""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product
import json
import os
from pathlib import Path
from typing import Any

from twins_scheduler.refinement_synthesis import Problem as PivotProblem
from twins_scheduler.refinement_synthesis import synthesize as structured_synthesize
from twins_scheduler.refinement_synthesis import verify_certificate as verify_structured
from twins_scheduler.repair_frontier import Domain, execute, from_graph
from twins_scheduler.transition_pivot_adapter import build_pivot_model, normalize_witness
from twins_scheduler.transition_synthesis import synthesize as general_synthesize
from twins_scheduler.transition_synthesis import verify_certificate as verify_general


CONFIG = {
    "directed_graphs": {
        "pivot_counts": [1, 2], "all_directed_graphs_including_self_loops": True,
        "one_pivot_profiles": [{"weights": [1], "costs": [2]}, {"weights": [2], "costs": [0]}],
        "two_pivot_profiles": [{"weights": [1, 1], "costs": [3, 1]},
                               {"weights": [1, 2], "costs": [5, 0]}],
        "quota_range": "every pair in 0..sum(weights)+1 inclusive",
        "allowed_split": "all", "required_split": [],
    },
    "permission_controls": {
        "weights": "(1,..,k)", "costs": "(4,) for k=1, (5,2) for k=2",
        "quotas": "(W,W) and (W-1,W)",
        "profiles": ["allow none; require none", "allow only 0; require none",
                     "allow all; require last", "allow all; require all"],
    },
    "arbitrary_posets": {
        "events": [["R", 0], ["R", 1], ["V", 0], ["V", 1]],
        "enumeration": "all topological orders and subsets of their six forward pairs; unique transitive closures reduced to covers",
        "poset_count": 219, "weights": [1, 2], "costs": [5, 2],
        "quotas": [[3, 3], [1, 3], [3, 1]], "allowed_split": [0, 1], "required_split": [],
    },
    "raw_oracle": "every legal event permutation; every total E/R Boolean policy (all four per-pivot patterns); every allowed/required split subset",
}


def digest(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True).encode()).hexdigest()


def all_four_event_posets():
    events = tuple(tuple(event) for event in CONFIG["arbitrary_posets"]["events"])
    closures = set()
    for order in permutations(events):
        forward = tuple((order[i], order[j]) for i in range(4) for j in range(i + 1, 4))
        for mask in range(1 << len(forward)):
            relation = {edge for index, edge in enumerate(forward) if mask >> index & 1}
            for middle in events:
                relation |= {(a, b) for a in events for b in events
                             if (a, middle) in relation and (middle, b) in relation}
            closures.add(tuple(sorted(relation)))
    if len(closures) != CONFIG["arbitrary_posets"]["poset_count"]:
        raise AssertionError("four-event poset enumeration is incomplete")
    for relation in sorted(closures):
        relation = set(relation)
        covers = frozenset((a, b) for a, b in relation if not any(
            (a, middle) in relation and (middle, b) in relation for middle in events))
        yield Domain((1, 2), covers)


def cases():
    for k in (1, 2):
        arcs = tuple(product(range(k), repeat=2))
        for graph_mask in range(1 << len(arcs)):
            graph = tuple(edge for index, edge in enumerate(arcs) if graph_mask >> index & 1)
            profiles = CONFIG["directed_graphs"]["one_pivot_profiles" if k == 1 else "two_pivot_profiles"]
            for profile in profiles:
                domain = from_graph(k, graph, weights=profile["weights"])
                for a, b in product(range(sum(domain.weights) + 2), repeat=2):
                    yield "all_graph_quotas", PivotProblem(domain, a, b, tuple(profile["costs"]))
            domain = from_graph(k, graph, weights=tuple(range(1, k + 1)))
            all_keys = frozenset(range(k))
            permissions = ((frozenset(), frozenset()), (frozenset({0}), frozenset()),
                           (all_keys, frozenset({k - 1})), (all_keys, all_keys))
            for allowed, required in permissions:
                for quotas in ((sum(domain.weights), sum(domain.weights)),
                               (sum(domain.weights) - 1, sum(domain.weights))):
                    yield "permission_controls", PivotProblem(domain, *quotas, (4,) if k == 1 else (5, 2),
                                                               allowed, required)
    for domain in all_four_event_posets():
        for a, b in CONFIG["arbitrary_posets"]["quotas"]:
            yield "arbitrary_posets", PivotProblem(domain, a, b, (5, 2))


def raw_observations(k, precedence):
    """Actual first/second signer masks from raw slots and four-pattern policies."""
    events = tuple((kind, i) for kind in ("R", "V") for i in range(k))
    rows = set()
    legal_orders = executions = 0
    for order in permutations(events):
        positions = {event: index for index, event in enumerate(order)}
        if any(positions[a] >= positions[b] for a, b in precedence):
            continue
        legal_orders += 1
        for policy in product((False, True), repeat=2 * k):
            first = sum(1 << i for i in range(k) if policy[2 * i])
            repaired, issued = set(), set()
            for kind, i in order:
                if kind == "R" and policy[2 * i + 1]:
                    repaired.add(i)
                if kind == "V" and i not in repaired:
                    issued.add(i)
            second = sum(1 << i for i in issued)
            rows.add((first, second, policy))
            executions += 1
    return tuple(sorted(rows)), legal_orders, executions


def raw_minimum(source, observations):
    best = None
    k = source.domain.k
    for mask in range(1 << k):
        split = {i for i in range(k) if mask >> i & 1}
        if not source.required_split <= split <= source.allowed_split:
            continue
        cost = sum(source.costs[i] for i in split)
        for first, second, policy in observations:
            if any(i not in split and policy[2 * i] != policy[2 * i + 1] for i in range(k)):
                continue
            first_weight = sum(w for i, w in enumerate(source.domain.weights) if first >> i & 1)
            second_weight = sum(w for i, w in enumerate(source.domain.weights) if second >> i & 1)
            if first_weight >= source.deficit0 and second_weight >= source.deficit1:
                best = cost if best is None else min(best, cost)
    return best


def run_oracle():
    models, raw = {}, {}
    counts = {
        "cases": 0, "directed_graphs_including_loops": 18, "arbitrary_four_event_posets": 219,
        "raw_order_domains": 0, "raw_legal_orders": 0, "raw_policy_order_executions": 0,
        "structured_optimum_comparisons": 0, "general_optimum_comparisons": 0,
        "structured_certificates_checked": 0, "general_certificates_checked": 0,
        "normalized_general_witnesses_checked": 0, "optimal_cases": 0, "infeasible_cases": 0,
        "maximum_exported_states": 0, "maximum_exported_transitions": 0,
        "minimum_cost_mismatches": 0, "certificate_failures": 0, "normalization_failures": 0,
    }
    families = {}
    inputs, outcomes, mismatches = [], [], []
    for family, source in cases():
        counts["cases"] += 1
        families[family] = families.get(family, 0) + 1
        inputs.append({"family": family, "problem": source.to_dict()})
        raw_key = source.domain.k, tuple(sorted(source.domain.precedence))
        if raw_key not in raw:
            observations, orders, executions = raw_observations(*raw_key)
            raw[raw_key] = observations
            counts["raw_order_domains"] += 1
            counts["raw_legal_orders"] += orders
            counts["raw_policy_order_executions"] += executions
        expected = raw_minimum(source, raw[raw_key])
        counts["optimal_cases" if expected is not None else "infeasible_cases"] += 1
        if source.domain not in models:
            models[source.domain] = build_pivot_model(source)
        model = models[source.domain].with_objective(source)
        counts["maximum_exported_states"] = max(counts["maximum_exported_states"], len(model.states))
        counts["maximum_exported_transitions"] = max(counts["maximum_exported_transitions"], len(model.problem.transitions))
        structured = structured_synthesize(source)
        general = general_synthesize(model.problem)
        for name, result in (("structured", structured), ("general", general)):
            counts[f"{name}_optimum_comparisons"] += 1
            if result["minimum_cost"] != expected:
                counts["minimum_cost_mismatches"] += 1
                mismatches.append({"family": family, "case": counts["cases"] - 1, "kind": name,
                                   "expected": expected, "actual": result["minimum_cost"]})
        try:
            if verify_structured(structured, source)["status"] != "PASS":
                raise ValueError("structured certificate failed")
            counts["structured_certificates_checked"] += 1
            if verify_general(general, model.problem)["status"] != "PASS":
                raise ValueError("general certificate failed")
            counts["general_certificates_checked"] += 1
        except ValueError as error:
            counts["certificate_failures"] += 1
            mismatches.append({"family": family, "kind": "certificate", "error": str(error)})
        if general["witness"] is not None:
            normalized = normalize_witness(model, general["witness"]["transitions"])
            run = execute(source.domain, normalized["opened"], map(tuple, normalized["order"]), normalized["split"])
            if (not run.violates(source.deficit0, source.deficit1)
                    or normalized["cost"] != general["minimum_cost"]
                    or not source.required_split <= set(normalized["split"]) <= source.allowed_split):
                counts["normalization_failures"] += 1
                mismatches.append({"family": family, "kind": "normalization"})
            counts["normalized_general_witnesses_checked"] += 1
        outcomes.append({"family": family, "source_sha256": digest(source.to_dict()),
                         "exported_sha256": model.problem.digest(), "oracle_minimum_cost": expected,
                         "structured_minimum_cost": structured["minimum_cost"],
                         "general_minimum_cost": general["minimum_cost"]})
    failed = sum(counts[field] for field in ("minimum_cost_mismatches", "certificate_failures", "normalization_failures"))
    return {
        "schema": "pivot-transition-specialization-oracle/v1", "status": "PASS" if not failed else "FAIL",
        "config": CONFIG, "counts": counts, "families": families,
        "input_sha256": digest(inputs), "outcome_sha256": digest(outcomes),
        "mismatches": failed, "mismatch_examples": mismatches[:10],
        "scope": "exact equality on declared initially-ready independent-pivot inputs; general LTS additionally permits reversed mixed E/R patterns, normalized without higher cost",
        "independence": "exporter uses raw predecessor masks and explicit immutable signature/repair state; raw oracle enumerates policies and event permutations; neither calls repair graph extraction, capacity formulas or the structured optimizer",
        "runtime": "excluded from deterministic output",
    }


def main():
    report = run_oracle()
    output_root = Path(os.environ.get("TWINS_OUTPUT_ROOT", Path(__file__).resolve().parents[1]))
    output = output_root / "results" / "transition_bridge" / "specialization_oracle.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "counts": report["counts"],
                      "mismatches": report["mismatches"], "output": str(output)}, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
