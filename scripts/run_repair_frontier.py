#!/usr/bin/env python3
"""Exhaustive, deterministic validation of the repair-frontier contracts.

The oracle executes each legal order and admission/split policy. It does not
use the capacity formula to generate the observed outcomes. The formula and
graph calculation are compared only after the executions have been collected.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import os
from pathlib import Path

from twins_scheduler.repair_frontier import (
    Domain, acyclic, coarse_boundary, common_deadline, execute, from_graph,
    minimum_phase_splits, subsets, weighted_common_boundary,
)


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def graph_suite():
    rows = []
    counts = dict(graphs=0, linear_extensions=0, executed_policies=0,
                  joint_delay_checks=0, boundary_checks=0, phase_budget_checks=0)
    examples = {}
    for k in range(1, 4):
        arcs = tuple(itertools.product(range(k), repeat=2))
        choices = tuple(subsets(k))
        for graph_mask in range(1 << len(arcs)):
            edges = frozenset(arcs[j] for j in range(len(arcs)) if graph_mask >> j & 1)
            domain = from_graph(k, edges)
            assert domain.repair_graph() == edges
            alpha = domain.acyclic_capacity()
            orders = tuple(domain.orders())
            counts["graphs"] += 1
            counts["linear_extensions"] += len(orders)
            achievable_late = []
            support_costs = {}
            for order in orders:
                positions = {v: i for i, v in enumerate(order)}
                achievable_late.append(frozenset(
                    i for i in range(k) if positions[("V", i)] < positions[("R", i)]
                ))
                for opened in choices:
                    for split in choices:
                        if not split <= opened:
                            continue
                        run = execute(domain, opened, order, split)
                        counts["executed_policies"] += 1
                        support = (run.first_weight, run.second_weight)
                        support_costs[support] = min(support_costs.get(support, k + 1), len(split))
            for desired in choices:
                observed = any(desired <= late for late in achievable_late)
                augmented = domain.precedence | frozenset(
                    (("V", i), ("R", i)) for i in desired
                )
                assert observed == acyclic(domain.events, augmented) == acyclic(desired, edges)
                counts["joint_delay_checks"] += 1
            for d0, d1 in itertools.product(range(k + 2), repeat=2):
                possible = [cost for (s0, s1), cost in support_costs.items() if s0 >= d0 and s1 >= d1]
                actual_minimum = min(possible) if possible else None
                observed_coarse = actual_minimum == 0
                predicted_coarse = coarse_boundary(k, alpha, d0, d1)
                predicted_minimum = minimum_phase_splits(k, alpha, d0, d1)
                assert observed_coarse == predicted_coarse, (k, edges, d0, d1)
                assert actual_minimum == predicted_minimum, (k, edges, d0, d1, actual_minimum)
                assert (actual_minimum is not None) == (max(d0, d1) <= k)
                counts["boundary_checks"] += 1
                counts["phase_budget_checks"] += 1
                rows.append(dict(k=k, graph_mask=graph_mask, arcs=len(edges), alpha=alpha,
                                 deficit0=d0, deficit1=d1, coarse_unsafe=observed_coarse,
                                 fine_unsafe=actual_minimum is not None,
                                 minimum_phase_splits=actual_minimum))
            if k == 2 and edges == frozenset({(0, 1), (1, 0)}):
                examples["crossed_deadlines"] = dict(
                    k=k, edges=sorted(edges), alpha=alpha, linear_extensions=len(orders),
                    individually_late_possible=[any(i in x for x in achievable_late) for i in range(k)],
                    jointly_late_possible=any(len(x) == k for x in achievable_late),
                    minimum_splits_for_two_full_quorums=minimum_phase_splits(k, alpha, k, k),
                )
    return rows, counts, examples


def common_suite():
    rows = []
    counts = dict(domains=0, executed_policies=0, boundary_checks=0)
    for k in range(1, 9):
        for late_count in range(k + 1):
            forced = frozenset(range(k - late_count))
            movable = tuple(range(k - late_count, k))
            domain = common_deadline(k, forced)
            attainable = set()
            for early_positions in subsets(len(movable)):
                early = forced | frozenset(movable[j] for j in early_positions)
                order = (tuple(("R", i) for i in sorted(early))
                         + tuple(("V", i) for i in range(k))
                         + tuple(("R", i) for i in range(k) if i not in early))
                for opened in subsets(k):
                    run = execute(domain, opened, order)
                    attainable.add((run.first_weight, run.second_weight))
                    counts["executed_policies"] += 1
            counts["domains"] += 1
            for d0, d1 in itertools.product(range(k + 2), repeat=2):
                observed = any(a >= d0 and b >= d1 for a, b in attainable)
                assert observed == coarse_boundary(k, late_count, d0, d1)
                counts["boundary_checks"] += 1
                rows.append(dict(k=k, late_capacity=late_count, deficit0=d0, deficit1=d1,
                                 coarse_unsafe=observed, fine_feasible_by_contract=max(d0, d1) <= k))
    return rows, counts


def weighted_suite():
    rows = []
    counts = dict(domains=0, executed_policies=0, boundary_checks=0)
    for k in range(1, 4):
        for weights in itertools.product((1, 2, 3), repeat=k):
            for forced in subsets(k):
                domain = common_deadline(k, forced, weights)
                # Every unforced repair can jointly occur after the shared
                # vote barrier. Earlier repair only removes second signatures,
                # so this order is a complete extremal order for reachability.
                order = (tuple(("R", i) for i in sorted(forced))
                         + tuple(("V", i) for i in range(k))
                         + tuple(("R", i) for i in range(k) if i not in forced))
                attainable = set()
                for opened in subsets(k):
                    run = execute(domain, opened, order)
                    attainable.add((run.first_weight, run.second_weight))
                    counts["executed_policies"] += 1
                counts["domains"] += 1
                for d0, d1 in itertools.product(range(sum(weights) + 2), repeat=2):
                    observed = any(a >= d0 and b >= d1 for a, b in attainable)
                    assert observed == weighted_common_boundary(weights, forced, d0, d1)
                    counts["boundary_checks"] += 1
                    rows.append(dict(weights="-".join(map(str, weights)),
                                     forced="-".join(map(str, sorted(forced))),
                                     deficit0=d0, deficit1=d1, coarse_unsafe=observed))
    return rows, counts


def arbitrary_order_suite():
    """Every labelled partial order on two repairs and two vote opportunities.

    Unlike the graph-realisation sweep, this includes V->R, R->R, V->V,
    and constraints implied only transitively. Suppressed slots retain their
    opportunity order. This checks the order-to-graph mapping independently.
    """
    events = (("R", 0), ("R", 1), ("V", 0), ("V", 1))
    arcs = tuple((a, b) for a in events for b in events if a != b)
    closures = set()
    for mask in range(1 << len(arcs)):
        edges = frozenset(arcs[j] for j in range(len(arcs)) if mask >> j & 1)
        if not acyclic(events, edges):
            continue
        reach = set(edges)
        while True:
            expanded = reach | {(a, d) for a, b in reach for c, d in reach if b == c}
            if expanded == reach:
                break
            reach = expanded
        closures.add(frozenset(reach))
    counts = dict(partial_orders=len(closures), linear_extensions=0,
                  executed_policies=0, joint_delay_checks=0, boundary_checks=0)
    assert len(closures) == 219
    for edges in closures:
        covers = frozenset((u, v) for u, v in edges if not any(
            (u, middle) in edges and (middle, v) in edges for middle in events
        ))
        domain = Domain((1, 1), covers)
        graph = domain.repair_graph()
        expected_graph = frozenset((i, j) for i in range(2) for j in range(2)
                                   if (("R", i), ("V", j)) in edges)
        assert graph == expected_graph
        orders = tuple(domain.orders())
        counts["linear_extensions"] += len(orders)
        supports = set()
        for order in orders:
            for opened in subsets(2):
                run = execute(domain, opened, order)
                supports.add((run.first_weight, run.second_weight))
                counts["executed_policies"] += 1
        for desired in subsets(2):
            witnessed = any(all(order.index(("V", i)) < order.index(("R", i))
                                for i in desired) for order in orders)
            assert witnessed == acyclic(desired, graph)
            counts["joint_delay_checks"] += 1
        for d0, d1 in itertools.product(range(4), repeat=2):
            observed = any(a >= d0 and b >= d1 for a, b in supports)
            assert observed == coarse_boundary(2, domain.acyclic_capacity(), d0, d1)
            counts["boundary_checks"] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path,
                        default=Path(os.environ.get("TWINS_OUTPUT_ROOT", ".")) / "results/revision")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    graph_rows, graph_counts, examples = graph_suite()
    common_rows, common_counts = common_suite()
    weighted_rows, weighted_counts = weighted_suite()
    arbitrary_counts = arbitrary_order_suite()
    late = execute(from_graph(1, []), {0}, (("V", 0), ("R", 0)))
    examples["repair_before_decision_after_signature"] = dict(
        first_signers=sorted(late.first_signers), second_signers=sorted(late.second_signers),
        repaired_at_end=sorted(late.repaired_at_end), unsafe=late.violates(1, 1),
    )
    examples["weighted_granularity"] = dict(
        weights=[2, 2], forced=[0, 1], deficit0=1, deficit1=3,
        coarse_unsafe=weighted_common_boundary((2, 2), {0, 1}, 1, 3),
        incorrect_total_capacity_test=(1 + 3 <= 4),
    )
    summary = dict(
        status="PASS", mismatch_count=0,
        semantics="initial-ready pivots; immutable signed outputs; fixed opportunity partial order",
        general_directed_graphs=graph_counts,
        arbitrary_four_event_orders=arbitrary_counts,
        common_deadline_sweep=common_counts,
        weighted_common_deadline=weighted_counts,
        controls=examples,
        scope="Finite certificate schema. New event-level n=4 protocol trace is checked separately.",
    )
    write_csv(args.out_dir / "frontier_graph_cases.csv", graph_rows)
    write_csv(args.out_dir / "frontier_common_cases.csv", common_rows)
    write_csv(args.out_dir / "frontier_weighted_cases.csv", weighted_rows)
    (args.out_dir / "frontier_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
