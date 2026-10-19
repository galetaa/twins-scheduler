#!/usr/bin/env python3
"""Compare synthesis against raw executions of arbitrary event-order DAGs.

This preserves the independent 48-case review oracle. It includes R→R, V→V
and V→R dependencies, heterogeneous weights and costs, restricted available
keys, required splits, zero costs and quota values beyond total weight. The
oracle enumerates event permutations and three admission modes directly; it
does not call repair-graph extraction, SCC decomposition, the event interpreter
or a capacity formula. Synthesis and certificate verification are comparison
targets, not part of the oracle.

Run with the project environment:
  uv run python scripts/check_synthesis_order_oracle.py

The deterministic report is written below TWINS_OUTPUT_ROOT when set, otherwise
below the repository root. This is a seeded finite check, not an exhaustive
enumeration of every six-event partial order.
"""

from __future__ import annotations

import hashlib
from itertools import permutations, product
import json
import os
from pathlib import Path
from random import Random

from twins_scheduler.repair_frontier import Domain
from twins_scheduler.refinement_synthesis import Problem, synthesize, verify_certificate


CONFIG = {
    "seed": 20261019,
    "cases": 48,
    "pivots": 3,
    "forward_edge_probability": 0.27,
    "weight_inclusive_range": [1, 3],
    "cost_inclusive_range": [0, 7],
    "allowed_split_probability": 0.7,
    "required_given_allowed_probability": 0.2,
    "quota_inclusive_range": "0..total_weight+1",
    "admission_modes": ["closed", "coarse_open", "phase_split"],
}


def raw_support_costs(events, edges, weights, costs, allowed, required):
    """Observe minimum costs per support pair, using only raw opportunity steps."""
    achievable = {}
    legal_orders = executions = 0
    for order in permutations(events):
        index = {event: j for j, event in enumerate(order)}
        if any(index[a] >= index[b] for a, b in edges):
            continue
        legal_orders += 1
        for mode in product(range(3), repeat=len(weights)):
            if any((mode[i] == 2 and i not in allowed)
                   or (i in required and mode[i] != 2) for i in range(len(weights))):
                continue
            repaired = set()
            issued = set()
            for kind, i in order:
                if kind == "R" and mode[i] == 1:
                    repaired.add(i)
                elif kind == "V" and i not in repaired:
                    issued.add(i)
            first = sum(weights[i] for i in range(len(weights)) if mode[i] != 0)
            second = sum(weights[i] for i in issued)
            cost = sum(costs[i] for i in range(len(weights)) if mode[i] == 2)
            support = (first, second)
            achievable[support] = min(cost, achievable.get(support, cost))
            executions += 1
    return achievable, legal_orders, executions


def run_oracle():
    rng = Random(CONFIG["seed"])
    k = CONFIG["pivots"]
    events = tuple((kind, i) for kind in ("R", "V") for i in range(k))
    cases = []
    counts = {
        "domains": 0,
        "raw_legal_permutations": 0,
        "raw_admission_executions": 0,
        "minimum_cost_comparisons": 0,
        "certificate_checks": 0,
        "minimum_cost_mismatches": 0,
        "certificate_failures": 0,
    }
    edge_kind_cases = {"R->R": 0, "R->V": 0, "V->R": 0, "V->V": 0}
    mismatch_examples = []
    for case in range(CONFIG["cases"]):
        shuffled = list(events)
        rng.shuffle(shuffled)
        edges = frozenset(
            (a, b) for i, a in enumerate(shuffled) for b in shuffled[i + 1:]
            if rng.random() < CONFIG["forward_edge_probability"]
        )
        weights = tuple(rng.randrange(1, 4) for _ in range(k))
        costs = tuple(rng.randrange(0, 8) for _ in range(k))
        allowed = frozenset(i for i in range(k) if rng.random() < CONFIG["allowed_split_probability"])
        required = frozenset(
            i for i in allowed if rng.random() < CONFIG["required_given_allowed_probability"]
        )
        cases.append({
            "weights": weights,
            "costs": costs,
            "precedence": sorted(edges),
            "allowed_split": sorted(allowed),
            "required_split": sorted(required),
        })
        for kind in {f"{a[0]}->{b[0]}" for a, b in edges}:
            edge_kind_cases[kind] += 1
        achievable, legal_orders, executions = raw_support_costs(
            events, edges, weights, costs, allowed, required
        )
        counts["domains"] += 1
        counts["raw_legal_permutations"] += legal_orders
        counts["raw_admission_executions"] += executions
        # Domain is used only by the comparison target; the oracle above has
        # already obtained its answers directly from the generated input.
        domain = Domain(weights, edges)
        total = sum(weights)
        for d0 in range(total + 2):
            for d1 in range(total + 2):
                candidates = [cost for (a, b), cost in achievable.items() if a >= d0 and b >= d1]
                expected = min(candidates) if candidates else None
                problem = Problem(domain, d0, d1, costs, allowed, required)
                result = synthesize(problem)
                counts["minimum_cost_comparisons"] += 1
                if result["minimum_cost"] != expected:
                    counts["minimum_cost_mismatches"] += 1
                    if len(mismatch_examples) < 10:
                        mismatch_examples.append({
                            "case": case, "deficits": [d0, d1], "kind": "minimum_cost",
                            "expected": expected, "actual": result["minimum_cost"],
                        })
                counts["certificate_checks"] += 1
                try:
                    checked = verify_certificate(result, problem)
                    if checked["status"] != "PASS":
                        raise ValueError("certificate did not return PASS")
                except ValueError as error:
                    counts["certificate_failures"] += 1
                    if len(mismatch_examples) < 10:
                        mismatch_examples.append({
                            "case": case, "deficits": [d0, d1], "kind": "certificate",
                            "error": str(error),
                        })
    mismatches = counts["minimum_cost_mismatches"] + counts["certificate_failures"]
    canonical_inputs = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema": "phase-refinement-order-oracle/v1",
        "status": "PASS" if mismatches == 0 else "FAIL",
        "config": CONFIG,
        "input_sha256": hashlib.sha256(canonical_inputs).hexdigest(),
        "counts": counts,
        "domains_with_direct_edge_kind": edge_kind_cases,
        "mismatches": mismatches,
        "mismatch_examples": mismatch_examples,
        "scope": "48 seeded arbitrary event DAGs; all permutations, admissible modes and quota pairs per DAG",
    }


def main():
    report = run_oracle()
    output_root = Path(os.environ.get("TWINS_OUTPUT_ROOT", Path(__file__).resolve().parents[1]))
    output = output_root / "results" / "synthesis" / "order_oracle.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"], "counts": report["counts"],
        "mismatches": report["mismatches"], "output": str(output),
    }, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
