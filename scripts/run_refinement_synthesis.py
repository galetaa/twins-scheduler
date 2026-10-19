#!/usr/bin/env python3
"""Synthesize/verify one portable problem, or reproduce the exact synthesis study.

Examples (run with the project's Python environment):
  python scripts/run_refinement_synthesis.py --input problem.json --output proof.json
  python scripts/run_refinement_synthesis.py --verify proof.json --expect-input problem.json
  python scripts/run_refinement_synthesis.py --study

The tiny oracle enumerates raw event permutations and three-state admissions;
it does not call the optimizer, capacity formula, graph extractor or execute().
Study outputs are deterministic. Observational wall times go to TWINS_LOG_DIR.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import random
import sys
from time import perf_counter

from twins_scheduler.repair_frontier import Domain, common_deadline, from_graph
from twins_scheduler.refinement_synthesis import (
    Problem, SynthesisLimit, fixed_split_capacity, fixed_split_feasible,
    synthesize, verify_certificate,
)


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def write_json(path, value, *, compact=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json_bytes(value) if compact else (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".gz" else raw)


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def raw_oracle(domain):
    """Return actual first/second/split bitsets from all legal raw executions."""
    outcomes = set()
    legal_orders = executions = 0
    modes = tuple(itertools.product(range(3), repeat=domain.k))
    for order in itertools.permutations(domain.events):
        positions = {event: j for j, event in enumerate(order)}
        if any(positions[u] >= positions[v] for u, v in domain.precedence):
            continue
        legal_orders += 1
        for admission in modes:
            first = sum(1 << i for i, mode in enumerate(admission) if mode != 0)
            split = sum(1 << i for i, mode in enumerate(admission) if mode == 2)
            repaired = [False] * domain.k
            emitted = [False] * domain.k
            for kind, i in order:
                if kind == "R" and admission[i] == 1:
                    repaired[i] = True
                if kind == "V" and not repaired[i]:
                    emitted[i] = True
            second = sum(1 << i for i, signed in enumerate(emitted) if signed)
            outcomes.add((first, second, split))
            executions += 1
    return tuple(sorted(outcomes)), legal_orders, executions


def oracle_cost_grid(outcomes, weights, costs, allowed=None):
    """Aggregate raw observations; no combinatorial feasibility theorem is used."""
    k, total = len(weights), sum(weights)
    allowed_mask = (1 << k) - 1 if allowed is None else sum(1 << i for i in allowed)
    grid = [[None] * (total + 2) for _ in range(total + 2)]
    for first_mask, second_mask, split_mask in outcomes:
        if split_mask & ~allowed_mask:
            continue
        first = sum(w for i, w in enumerate(weights) if first_mask >> i & 1)
        second = sum(w for i, w in enumerate(weights) if second_mask >> i & 1)
        cost = sum(c for i, c in enumerate(costs) if split_mask >> i & 1)
        for a in range(first + 1):
            for b in range(second + 1):
                grid[a][b] = cost if grid[a][b] is None else min(grid[a][b], cost)
    return grid


def all_four_event_orders():
    """Generate labelled posets from forward DAGs, independently of H."""
    events = (("R", 0), ("R", 1), ("V", 0), ("V", 1))
    closures = set()
    for order in itertools.permutations(events):
        forward = tuple((order[i], order[j]) for i in range(4) for j in range(i + 1, 4))
        for mask in range(1 << len(forward)):
            reached = {edge for j, edge in enumerate(forward) if mask >> j & 1}
            for middle in events:
                reached |= {(a, b) for a in events for b in events
                            if (a, middle) in reached and (middle, b) in reached}
            closures.add(tuple(sorted(reached)))
    assert len(closures) == 219
    for closure in sorted(closures):
        reached = set(closure)
        covers = frozenset((a, b) for a, b in reached if not any(
            (a, middle) in reached and (middle, b) in reached for middle in events
        ))
        yield Domain((1, 1), covers)


def exhaustive_study(out_dir):
    counts = {
        "directed_graphs": 0, "graph_linear_extensions": 0, "graph_raw_executions": 0,
        "prescribed_split_boundary_checks": 0, "weighted_all_quota_optima": 0,
        "weighted_three_pivot_optima": 0, "restricted_key_optima": 0,
        "arbitrary_partial_orders": 0, "arbitrary_linear_extensions": 0,
        "arbitrary_raw_executions": 0, "arbitrary_weighted_optima": 0,
        "independently_verified_certificates": 0, "mismatches": 0,
    }
    rows, raw_records = [], []
    boundary_digest = hashlib.sha256()

    def compare(family, instance, problem, expected):
        result = synthesize(problem)
        assert result["minimum_cost"] == expected, (family, instance, problem.to_dict(), expected, result)
        receipt = verify_certificate(result, problem)
        assert receipt["status"] == "PASS"
        counts["independently_verified_certificates"] += 1
        rows.append({
            "family": family, "instance": instance,
            "weights": "-".join(map(str, problem.domain.weights)),
            "costs": "-".join(map(str, problem.costs)),
            "allowed": "-".join(map(str, sorted(problem.allowed_split))),
            "deficit0": problem.deficit0, "deficit1": problem.deficit1,
            "oracle_cost": expected, "synthesized_cost": result["minimum_cost"],
            "split": "-".join(map(str, result["witness"]["split"])) if result["witness"] else "",
            "certificate_status": receipt["status"],
        })

    for k in range(1, 4):
        arcs = tuple(itertools.product(range(k), repeat=2))
        for graph_mask in range(1 << len(arcs)):
            domain = from_graph(k, (edge for j, edge in enumerate(arcs) if graph_mask >> j & 1))
            outcomes, orders, executions = raw_oracle(domain)
            counts["directed_graphs"] += 1
            counts["graph_linear_extensions"] += orders
            counts["graph_raw_executions"] += executions
            raw_records.append({"family": "directed", "k": k, "instance": graph_mask,
                                "precedence": Problem(domain, 0, 0, (1,) * k).to_dict()["precedence"],
                                "legal_orders": orders, "executions": executions, "outcomes": outcomes})
            for available_mask in range(1 << k):
                available = frozenset(i for i in range(k) if available_mask >> i & 1)
                observed = oracle_cost_grid(outcomes, (1,) * k, (0,) * k, available)
                for d0, d1 in itertools.product(range(k + 2), repeat=2):
                    actual = observed[d0][d1] is not None
                    predicted = fixed_split_feasible(domain, available, d0, d1)
                    assert actual == predicted, (k, graph_mask, available, d0, d1)
                    counts["prescribed_split_boundary_checks"] += 1
                    boundary_digest.update(json_bytes([k, graph_mask, available_mask, d0, d1, actual]))
            if k <= 2:
                profiles = ((1,), (3,), (0,)) if k == 1 else ((1, 1), (1, 3), (3, 1), (0, 2))
                for weights in itertools.product((1, 2, 3), repeat=k):
                    weighted_domain = Domain(weights, domain.precedence)
                    for costs in profiles:
                        observed = oracle_cost_grid(outcomes, weights, costs)
                        for d0, d1 in itertools.product(range(sum(weights) + 2), repeat=2):
                            problem = Problem(weighted_domain, d0, d1, costs)
                            compare("weighted_all_quotas", f"{k}:{graph_mask}", problem, observed[d0][d1])
                            counts["weighted_all_quota_optima"] += 1
                if k == 2:
                    weights, costs = (1, 2), (3, 1)
                    for mask in range(1 << k):
                        allowed = frozenset(i for i in range(k) if mask >> i & 1)
                        observed = oracle_cost_grid(outcomes, weights, costs, allowed)
                        for d0, d1 in ((3, 3), (1, 2)):
                            problem = Problem(Domain(weights, domain.precedence), d0, d1, costs, allowed)
                            compare("restricted_keys", str(graph_mask), problem, observed[d0][d1])
                            counts["restricted_key_optima"] += 1
            else:
                weights = tuple(1 + ((graph_mask >> i) + i) % 3 for i in range(k))
                costs = tuple(1 + ((graph_mask >> (i + 1)) + 2 * i) % 5 for i in range(k))
                total, middle = sum(weights), (sum(weights) + 1) // 2
                observed = oracle_cost_grid(outcomes, weights, costs)
                for d0, d1 in ((total, total), (total, middle), (middle, total),
                               (middle, middle), (total + 1, 0)):
                    problem = Problem(Domain(weights, domain.precedence), d0, d1, costs)
                    compare("weighted_three_pivots", str(graph_mask), problem, observed[d0][d1])
                    counts["weighted_three_pivot_optima"] += 1
        print(f"raw oracle: all directed graphs on {k} pivots checked", flush=True)
    for instance, domain in enumerate(all_four_event_orders()):
        outcomes, orders, executions = raw_oracle(domain)
        counts["arbitrary_partial_orders"] += 1
        counts["arbitrary_linear_extensions"] += orders
        counts["arbitrary_raw_executions"] += executions
        raw_records.append({"family": "arbitrary_poset", "k": 2, "instance": instance,
                            "precedence": Problem(domain, 0, 0, (1, 1)).to_dict()["precedence"],
                            "legal_orders": orders, "executions": executions, "outcomes": outcomes})
        weights, costs = (2, 3), (4, 1)
        observed = oracle_cost_grid(outcomes, weights, costs)
        for d0, d1 in itertools.product(range(7), repeat=2):
            problem = Problem(Domain(weights, domain.precedence), d0, d1, costs)
            compare("arbitrary_weighted_order", str(instance), problem, observed[d0][d1])
            counts["arbitrary_weighted_optima"] += 1
    counts["prescribed_split_checks_sha256"] = boundary_digest.hexdigest()
    write_csv(out_dir / "synthesis_oracle_cases.csv", rows)
    write_json(out_dir / "synthesis_raw_observations.json.gz", raw_records, compact=True)
    return counts


def marginal_greedy(domain, costs, d0, d1):
    """Specific one-step positive marginal/cost policy; not every greedy method.

    Stops with STALLED if all remaining marginal gains are zero.  Ties choose
    the smallest index. Costs here must be positive and pivots unit-weight.
    """
    if any(cost <= 0 for cost in costs):
        raise ValueError("this baseline is defined only for positive costs")
    target = max(0, d0 + d1 - domain.k)
    chosen = set()
    while fixed_split_capacity(domain, chosen) < target:
        before = fixed_split_capacity(domain, chosen)
        candidates = []
        for i in range(domain.k):
            if i not in chosen:
                gain = fixed_split_capacity(domain, chosen | {i}) - before
                if gain > 0:
                    candidates.append((Fraction(gain, costs[i]), -i, i))
        if not candidates:
            return {"status": "STALLED", "split": sorted(chosen),
                    "cost": sum(costs[i] for i in chosen)}
        chosen.add(max(candidates)[2])
    return {"status": "FEASIBLE", "split": sorted(chosen), "cost": sum(costs[i] for i in chosen)}


def fixture_study(out_dir):
    bowtie = from_graph(3, [(0, 1), (1, 0), (0, 2), (2, 0)])
    problems = {
        "one_pivot_forced_repair": Problem(from_graph(1, [(0, 0)]), 1, 1, (1,)),
        "one_pivot_post_signature": Problem(Domain((1,), frozenset({(("V", 0), ("R", 0))})), 1, 1, (1,)),
        "crossed_deadlines": Problem(from_graph(2, [(0, 1), (1, 0)]), 2, 2, (3, 1)),
        "bow_tie_cost": Problem(bowtie, 3, 3, (10, 1, 1)),
        "weighted_granularity": Problem(from_graph(2, [(0, 0), (1, 1)], weights=(2, 2)), 1, 3, (7, 1)),
    }
    fixtures = {}
    for name, problem in problems.items():
        result = synthesize(problem)
        receipt = verify_certificate(result, problem)
        write_json(out_dir / "examples" / f"{name}.input.json", problem.to_dict())
        write_json(out_dir / "examples" / f"{name}.certificate.json", result)
        fixtures[name] = {"minimum_cost": result["minimum_cost"], "split": result["witness"]["split"],
                          "order": result["witness"]["order"], "verification": receipt}
    prescribed = from_graph(3, [(0, 1), (1, 0)])
    fixtures["equal_cardinality_different_effect"] = {
        "k": 3, "deficits": [3, 3], "edges": [[0, 1], [1, 0]],
        "ineffective_split": [2], "ineffective_capacity": fixed_split_capacity(prescribed, {2}),
        "effective_split": [1], "effective_capacity": fixed_split_capacity(prescribed, {1}),
    }
    fixtures["non_submodular_capacity"] = {
        "empty": fixed_split_capacity(bowtie, set()),
        "leaf1": fixed_split_capacity(bowtie, {1}),
        "leaf2": fixed_split_capacity(bowtie, {2}),
        "both_leaves": fixed_split_capacity(bowtie, {1, 2}),
    }
    traps = []
    for center_cost in (3, 10, 100, 1000):
        problem = Problem(bowtie, 3, 3, (center_cost, 1, 1))
        result = synthesize(problem)
        verify_certificate(result, problem)
        baseline = marginal_greedy(bowtie, problem.costs, 3, 3)
        assert result["minimum_cost"] == 2 and baseline["cost"] == center_cost
        traps.append({"center_cost": center_cost, "optimal_cost": 2,
                      "optimal_split": result["witness"]["split"],
                      "greedy": baseline, "ratio": str(Fraction(center_cost, 2))})
    fixtures["specified_myopic_greedy_trap"] = traps
    return fixtures


def benchmark_problems():
    seed = 20261019
    rng = random.Random(seed)
    # Large k with small strongly coupled blocks, plus deliberately large SCCs.
    for k in (12, 48):
        edges = [(i, j) for i in range(k) for j in range(i + 1, k) if rng.random() < 0.08]
        yield f"sparse_dag_k{k}", seed, Problem(from_graph(k, edges), k, k, tuple(1 + i % 7 for i in range(k)))
    for k in (12, 48):
        edges = [(i, i ^ 1) for i in range(k)]
        yield f"crossed_pairs_k{k}", seed, Problem(from_graph(k, edges), k, k, tuple(1 + i % 7 for i in range(k)))
    for k in (12, 30):
        edges = []
        for center in range(0, k, 3):
            edges.extend((center, leaf) for leaf in (center + 1, center + 2))
            edges.extend((leaf, center) for leaf in (center + 1, center + 2))
        costs = tuple(100 if i % 3 == 0 else 1 for i in range(k))
        yield f"bow_tie_blocks_k{k}", seed, Problem(from_graph(k, edges), k, k, costs)
    for k in (24, 48):
        weights = tuple(1 + i % 3 for i in range(k))
        total = sum(weights)
        domain = common_deadline(k, range(3 * k // 4), weights)
        yield f"weighted_common_deadline_k{k}", seed, Problem(domain, (3 * total + 3) // 4,
                                                              (4 * total + 4) // 5,
                                                              tuple(1 + (3 * i) % 11 for i in range(k)))
    for k in (8, 10, 12):
        edges = [(i, (i + 1) % k) for i in range(k)]
        edges += [(i, j) for i in range(k) for j in range(k) if i != j and rng.random() < 0.55]
        yield f"dense_scc_k{k}", seed, Problem(from_graph(k, edges), k, k, tuple(1 + i % 7 for i in range(k)))
    for k in (10, 24):
        edges = [(i, (i + 1) % k) for i in range(k)]
        yield f"single_cycle_k{k}", seed, Problem(from_graph(k, edges), k, k, tuple(1 + i % 7 for i in range(k)))
    # Unequal weights and incomplete quotas inside several coupled blocks.
    k = 24
    weights = tuple(rng.randint(1, 5) for _ in range(k))
    costs = tuple(rng.randint(1, 9) for _ in range(k))
    edges = [(base + i, base + (i + 1) % 4) for base in range(0, k, 4) for i in range(4)]
    total = sum(weights)
    yield "weighted_quota_cycles_k24", seed, Problem(from_graph(k, edges, weights),
                                                    (4 * total + 4) // 5, (9 * total + 9) // 10, costs)
    yield "weighted_quota_cycles_tight_k24", seed, Problem(from_graph(k, edges, weights),
                                                          total - 1, total - 2, costs)


def benchmark_study(out_dir):
    rows, timings = [], []
    for name, seed, problem in benchmark_problems():
        started = perf_counter()
        try:
            result = synthesize(problem, max_component_size=10)
        except SynthesisLimit as error:
            rows.append({"case": name, "seed": seed, "k": problem.domain.k,
                         "total_weight": sum(problem.domain.weights), "deficit0": problem.deficit0,
                         "deficit1": problem.deficit1, "status": "RESOURCE_LIMIT",
                         "minimum_cost": "", "split_count": "", "components": "",
                         "largest_component": "", "local_assignments": "", "potential_cells": "",
                         "bellman_transitions": "", "verified_inequalities": "", "greedy_cost": "",
                         "certificate_bytes": "", "certificate_sha256": "", "detail": str(error)})
            timings.append({"case": name, "solver_seconds": perf_counter() - started,
                            "checker_seconds": None, "status": "RESOURCE_LIMIT"})
            continue
        solved = perf_counter()
        receipt = verify_certificate(result, problem)
        checked = perf_counter()
        encoded = json_bytes(result)
        certificate_name = f"certificates/{name}.json.gz"
        write_json(out_dir / certificate_name, result, compact=True)
        stats = result["statistics"]
        baseline_cost = ""
        if all(weight == 1 for weight in problem.domain.weights):
            baseline = marginal_greedy(problem.domain, problem.costs, problem.deficit0, problem.deficit1)
            baseline_cost = baseline["cost"] if baseline["status"] == "FEASIBLE" else baseline["status"]
        rows.append({"case": name, "seed": seed, "k": problem.domain.k,
                     "total_weight": sum(problem.domain.weights), "deficit0": problem.deficit0,
                     "deficit1": problem.deficit1, "status": "OPTIMAL",
                     "minimum_cost": result["minimum_cost"], "split_count": len(result["witness"]["split"]),
                     "components": stats["components"], "largest_component": stats["largest_component"],
                     "local_assignments": stats["local_assignments"], "potential_cells": stats["potential_cells"],
                     "bellman_transitions": stats["bellman_transitions"],
                     "verified_inequalities": receipt["verified_inequalities"],
                     "greedy_cost": baseline_cost, "certificate_bytes": len(encoded),
                     "certificate_sha256": hashlib.sha256(encoded).hexdigest(), "detail": certificate_name})
        timings.append({"case": name, "solver_seconds": solved - started,
                        "checker_seconds": checked - solved, "status": "OPTIMAL"})
        print(f"benchmark {name}: optimum {result['minimum_cost']}, certificate PASS", flush=True)
    write_csv(out_dir / "synthesis_benchmarks.csv", rows)
    return {
        "cases": len(rows), "optimal_and_independently_checked": sum(row["status"] == "OPTIMAL" for row in rows),
        "resource_limited_unknown": sum(row["status"] == "RESOURCE_LIMIT" for row in rows),
        "largest_solved_k": max(row["k"] for row in rows if row["status"] == "OPTIMAL"),
        "configured_max_component_size": 10,
        "interpretation": "Deterministic synthetic opportunity domains; resource cutoffs are unknown, not infeasible.",
    }, timings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--input", type=Path)
    mode.add_argument("--verify", type=Path)
    mode.add_argument("--study", action="store_true")
    parser.add_argument("--expect-input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--out-dir", type=Path,
                        default=Path(os.environ.get("TWINS_OUTPUT_ROOT", ".")) / "results/synthesis")
    parser.add_argument("--max-component-size", type=int, default=10)
    parser.add_argument("--time-budget", type=float)
    args = parser.parse_args()
    if args.verify:
        expected = Problem.from_dict(read_json(args.expect_input)) if args.expect_input else None
        receipt = verify_certificate(read_json(args.verify), expected)
        print(json.dumps(receipt, sort_keys=True, indent=2))
        return
    if args.input:
        if args.output is None:
            parser.error("--input requires --output for the portable certificate")
        problem = Problem.from_dict(read_json(args.input))
        try:
            result = synthesize(problem, max_component_size=args.max_component_size,
                                time_budget_seconds=args.time_budget)
        except SynthesisLimit as error:
            print(json.dumps({"status": "RESOURCE_LIMIT", "detail": str(error)}))
            sys.exit(2)
        receipt = verify_certificate(result, problem)
        write_json(args.output, result)
        print(json.dumps({"status": result["status"], "minimum_cost": result["minimum_cost"],
                          "verification": receipt, "output": str(args.output)}, indent=2, sort_keys=True))
        return
    args.out_dir.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    oracle_counts = exhaustive_study(args.out_dir)
    after_oracle = perf_counter()
    fixtures = fixture_study(args.out_dir)
    benchmark_counts, timings = benchmark_study(args.out_dir)
    summary = {
        "status": "PASS", "mismatch_count": 0, "schema": "phase-refinement-study/v1",
        "contract": "Initially-ready independent pivots; positive integer weights; nonnegative integer split costs; immutable votes; full opportunity order retained.",
        "oracle": oracle_counts, "fixtures": fixtures, "benchmarks": benchmark_counts,
        "certificate": "Concrete replay plus SCC Bellman lower-bound potentials; separate checker never invokes global optimizer.",
        "scope": "The corpus checks a finite certificate schema. It is not a production-client test or a prevalence estimate.",
    }
    write_json(args.out_dir / "synthesis_summary.json", summary)
    log_dir = Path(os.environ.get("TWINS_LOG_DIR", "build_logs"))
    write_json(log_dir / "refinement_synthesis_timings.json", {
        "informational_only": True, "repetitions": 1,
        "not_a_performance_comparison": "Single observed run; excludes synthesis output files and greedy baseline from solver/checker intervals.",
        "python": platform.python_version(), "platform": platform.platform(),
        "machine": platform.machine(), "oracle_seconds": after_oracle - start,
        "total_seconds": perf_counter() - start, "cases": timings,
    })
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
