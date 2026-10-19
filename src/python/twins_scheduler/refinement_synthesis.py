"""Certifying minimum-cost phase refinement for the repair-frontier contract.

The optimizer selects keys, admissions and an event order.  Its certificate
contains a concrete immutable-output execution and Bellman *lower-bound*
potentials.  ``verify_certificate`` uses separate graph traversal, local
enumeration and event replay code; it never invokes the optimizer or the
repair-frontier capacity formula.  All costs and weights are exact integers.

This is synthesis for a declared finite certificate schema, not extraction of
such a schema from an arbitrary implementation.  In particular, pivots must be
initially ready, their contributions independent, and withheld event slots
retain the original opportunity order.  See REFINEMENT_SYNTHESIS.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from time import monotonic
from typing import Any, Iterable

from .repair_frontier import Domain, Event, acyclic, execute

# A vertex's canonical contribution: split/both; reversible/both; first only;
# second only.  The names are part of the portable certificate format.
LABELS = ("split", "reversible", "first", "second")


@dataclass(frozen=True)
class Problem:
    domain: Domain
    deficit0: int
    deficit1: int
    costs: tuple[int, ...]
    allowed_split: frozenset[int] | None = None
    required_split: frozenset[int] = frozenset()

    def __post_init__(self) -> None:
        if not self.domain.initially_ready:
            raise ValueError("synthesis requires the initially-ready contract")
        if any(type(d) is not int or d < 0 for d in (self.deficit0, self.deficit1)):
            raise ValueError("deficits must be nonnegative integers")
        if len(self.costs) != self.domain.k or any(type(c) is not int or c < 0 for c in self.costs):
            raise ValueError("one nonnegative integer cost is required for each key")
        indices = frozenset(range(self.domain.k))
        if self.allowed_split is None:
            object.__setattr__(self, "allowed_split", indices)
        if not self.required_split <= self.allowed_split <= indices:
            raise ValueError("required keys must be allowed and all keys must exist")

    def to_dict(self) -> dict[str, Any]:
        return {
            "weights": list(self.domain.weights), "costs": list(self.costs),
            "deficits": [self.deficit0, self.deficit1],
            "precedence": [[list(u), list(v)] for u, v in sorted(self.domain.precedence)],
            "allowed_split": sorted(self.allowed_split),
            "required_split": sorted(self.required_split),
            "initially_ready": True,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Problem:
        if data.get("initially_ready") is not True:
            raise ValueError("certificate does not declare initial readiness")
        domain = Domain(tuple(data["weights"]), frozenset(
            (tuple(u), tuple(v)) for u, v in data["precedence"]
        ))
        return cls(domain, *data["deficits"], tuple(data["costs"]),
                   frozenset(data["allowed_split"]), frozenset(data["required_split"]))


class SynthesisLimit(RuntimeError):
    """Resource exhaustion is not an infeasibility result."""


def _components(k: int, graph: frozenset[tuple[int, int]]) -> tuple[tuple[int, ...], ...]:
    """Tarjan SCCs after self-loop vertices are made separate forced-out blocks.

    A self-loop vertex can never be reversible, so its graph arcs do not couple
    the remaining reversible choices.  They are removed only *after* H was
    built from the full event-order transitive closure.
    """
    loops = {i for i in range(k) if (i, i) in graph}
    vertices = set(range(k)) - loops
    outgoing = {i: sorted(j for a, j in graph if a == i and j in vertices)
                for i in vertices}
    number: dict[int, int] = {}
    low: dict[int, int] = {}
    stack: list[int] = []
    stacked: set[int] = set()
    blocks: list[tuple[int, ...]] = [(i,) for i in sorted(loops)]

    def visit(v: int) -> None:
        number[v] = low[v] = len(number)
        stack.append(v)
        stacked.add(v)
        for w in outgoing[v]:
            if w not in number:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in stacked:
                low[v] = min(low[v], number[w])
        if low[v] == number[v]:
            block = []
            while True:
                w = stack.pop()
                stacked.remove(w)
                block.append(w)
                if w == v:
                    break
            blocks.append(tuple(sorted(block)))

    for v in sorted(vertices):
        if v not in number:
            visit(v)
    return tuple(sorted(blocks))


def _topological(events: Iterable[Event], edges: Iterable[tuple[Event, Event]]) -> tuple[Event, ...]:
    remaining = set(events)
    incoming = {v: set() for v in remaining}
    for u, v in edges:
        incoming[v].add(u)
    order = []
    while remaining:
        ready = sorted(v for v in remaining if not (incoming[v] & remaining))
        if not ready:
            raise AssertionError("the synthesized augmented event order is cyclic")
        event = ready[0]
        order.append(event)
        remaining.remove(event)
    return tuple(order)


def fixed_split_capacity(domain: Domain, split: Iterable[int]) -> int:
    """Unit-weight double-contribution capacity for a prescribed available set.

    Its value is |S| + alpha(H[I\\S]), not alpha(H) + |S|.  Exact subset search
    is local to the components of the remaining repair graph.
    """
    if not domain.initially_ready or any(w != 1 for w in domain.weights):
        raise ValueError("fixed split capacity uses initially-ready unit-weight pivots")
    split = frozenset(split)
    if not split <= frozenset(range(domain.k)):
        raise ValueError("unknown split key")
    graph = frozenset((i, j) for i, j in domain.repair_graph()
                      if i not in split and j not in split)
    capacity = 0
    for block in _components(domain.k, graph):
        if block[0] in split:
            continue
        local = 0
        for mask in range(1 << len(block)):
            chosen = {block[j] for j in range(len(block)) if mask >> j & 1}
            if len(chosen) > local and acyclic(chosen, graph):
                local = len(chosen)
        capacity += local
    return len(split) + capacity


def fixed_split_feasible(domain: Domain, split: Iterable[int], deficit0: int, deficit1: int) -> bool:
    if any(type(d) is not int or d < 0 for d in (deficit0, deficit1)):
        raise ValueError("deficits must be nonnegative integers")
    capacity = fixed_split_capacity(domain, split)
    return (max(deficit0, deficit1) <= domain.k
            and deficit0 + deficit1 <= domain.k + capacity)


def synthesize(
    problem: Problem, *, max_component_size: int = 10,
    max_potential_cells: int = 2_000_000, time_budget_seconds: float | None = None,
) -> dict[str, Any]:
    """Return an optimal policy/order and a portable exact lower-bound proof.

    Local four-state configurations are enumerated per SCC.  The dynamic
    program ranges over residual quotas, with local support clipped at those
    quotas.  Enumeration is exponential in the largest nontrivial component;
    the quota dependence is pseudo-polynomial, not polynomial in binary input
    length.  Explicit limits raise SynthesisLimit and never report UNSAT.
    """
    if max_component_size < 1 or max_potential_cells < 1:
        raise ValueError("resource limits must be positive")
    if time_budget_seconds is not None and time_budget_seconds <= 0:
        raise ValueError("time budget must be positive")
    deadline = None if time_budget_seconds is None else monotonic() + time_budget_seconds

    def check_time() -> None:
        if deadline is not None and monotonic() > deadline:
            raise SynthesisLimit("wall-clock budget exhausted; feasibility remains unknown")

    domain, d0, d1 = problem.domain, problem.deficit0, problem.deficit1
    result: dict[str, Any] = {"schema": "phase-refinement-certificate/v1", "problem": problem.to_dict()}
    total = sum(domain.weights)
    if max(d0, d1) > total:
        result.update(status="infeasible", minimum_cost=None, witness=None,
                      proof={"kind": "total-weight", "total_weight": total},
                      statistics={"local_assignments": 0, "potential_cells": 0,
                                  "bellman_transitions": 0, "components": 0, "largest_component": 0})
        return result
    graph = domain.repair_graph()
    blocks = _components(domain.k, graph)
    largest = max(map(len, blocks))
    if largest > max_component_size:
        raise SynthesisLimit(f"largest component {largest} exceeds configured limit {max_component_size}")
    width, cells = d1 + 1, (d0 + 1) * (d1 + 1)
    if (len(blocks) + 1) * cells > max_potential_cells:
        raise SynthesisLimit("Bellman-potential table exceeds configured cell limit")
    # A row is (first support, second support, cost, tuple of local labels).
    options: list[tuple[tuple[int, int, int, tuple[int, ...]], ...]] = []
    enumerated = 0
    valid_assignments = 0
    for block in blocks:
        best: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
        allowed = []
        for i in block:
            if i in problem.required_split:
                allowed.append((0,))
            else:
                allowed.append(tuple(label for label in range(4)
                                     if (label != 0 or i in problem.allowed_split)
                                     and (label != 1 or (i, i) not in graph)))
        for labels in product(*allowed):
            enumerated += 1
            if enumerated % 256 == 0:
                check_time()
            reversible = {i for i, label in zip(block, labels) if label == 1}
            if not acyclic(reversible, graph):
                continue
            valid_assignments += 1
            first = min(d0, sum(domain.weights[i] for i, label in zip(block, labels) if label != 3))
            second = min(d1, sum(domain.weights[i] for i, label in zip(block, labels) if label != 2))
            cost = sum(problem.costs[i] for i, label in zip(block, labels) if label == 0)
            key, candidate = (first, second), (cost, labels)
            if key not in best or candidate < best[key]:
                best[key] = candidate
        options.append(tuple((a, b, cost, labels) for (a, b), (cost, labels) in sorted(best.items())))
    # None denotes +infinity.  L_j(a,b) is a lower bound on the cost of meeting
    # residual quotas (a,b) with blocks j..m-1.  Exact minima make tight bounds.
    potentials: list[list[int | None]] = [[None] * cells for _ in range(len(blocks) + 1)]
    potentials[-1][0] = 0
    transitions = 0
    for j in range(len(blocks) - 1, -1, -1):
        following, current = potentials[j + 1], potentials[j]
        for a in range(d0 + 1):
            check_time()
            for b in range(d1 + 1):
                value = None
                for support0, support1, cost, _ in options[j]:
                    transitions += 1
                    residual = following[max(0, a - support0) * width + max(0, b - support1)]
                    if residual is not None and (value is None or cost + residual < value):
                        value = cost + residual
                current[a * width + b] = value
    minimum = potentials[0][d0 * width + d1]
    result.update(
        status="infeasible" if minimum is None else "optimal", minimum_cost=minimum, witness=None,
        proof={"kind": "scc-bellman-v1", "components": [list(block) for block in blocks],
               "potentials": potentials},
        statistics={"components": len(blocks), "largest_component": largest,
                    "local_assignments": enumerated, "valid_local_assignments": valid_assignments,
                    "compressed_local_options": sum(map(len, options)),
                    "potential_cells": (len(blocks) + 1) * cells,
                    "bellman_transitions": transitions},
    )
    if minimum is None:
        return result
    chosen = [None] * domain.k
    a, b = d0, d1
    for j, block in enumerate(blocks):
        for support0, support1, cost, labels in options[j]:
            after_a, after_b = max(0, a - support0), max(0, b - support1)
            residual = potentials[j + 1][after_a * width + after_b]
            if residual is not None and cost + residual == potentials[j][a * width + b]:
                for i, label in zip(block, labels):
                    chosen[i] = label
                a, b = after_a, after_b
                break
        else:
            raise AssertionError("a tight Bellman transition is missing")
    split = frozenset(i for i, label in enumerate(chosen) if label == 0)
    reversible = frozenset(i for i, label in enumerate(chosen) if label == 1)
    opened = frozenset(i for i, label in enumerate(chosen) if label != 3)
    augmented = domain.precedence | frozenset((("V", i), ("R", i)) for i in reversible)
    order = _topological(domain.events, augmented)
    run = execute(domain, opened, order, split)
    if not run.violates(d0, d1):
        raise AssertionError("synthesized witness fails its quotas")
    result["witness"] = {
        "labels": [LABELS[label] for label in chosen],
        "split": sorted(split), "opened": sorted(opened), "reversible": sorted(reversible),
        "order": [list(event) for event in order],
        "first_signers": sorted(run.first_signers), "second_signers": sorted(run.second_signers),
        "repaired_at_end": sorted(run.repaired_at_end),
        "first_weight": run.first_weight, "second_weight": run.second_weight,
    }
    return result


def verify_certificate(certificate: dict[str, Any], expected_problem: Problem | None = None) -> dict[str, Any]:
    """Independently check a policy's cost and a lower bound on *all* policies.

    This routine is intentionally separate from the solver's Tarjan, Kahn,
    local-support compression, optimizer and ``execute`` implementation.  It
    checks Bellman inequalities, not whether a solver-reported optimum is
    plausible.  Replaying one witness alone would certify no optimality.
    """
    if certificate.get("schema") != "phase-refinement-certificate/v1":
        raise ValueError("unsupported certificate schema")
    problem = Problem.from_dict(certificate["problem"])
    if expected_problem is not None and problem.to_dict() != expected_problem.to_dict():
        raise ValueError("certificate describes a different problem")
    domain, d0, d1 = problem.domain, problem.deficit0, problem.deficit1
    proof = certificate["proof"]
    total = sum(domain.weights)
    if proof["kind"] == "total-weight":
        if (max(d0, d1) <= total or proof["total_weight"] != total
                or certificate["status"] != "infeasible"
                or certificate["minimum_cost"] is not None or certificate["witness"] is not None):
            raise ValueError("invalid total-weight infeasibility certificate")
        return {"status": "PASS", "kind": "total-weight", "verified_inequalities": 0,
                "replayed_events": 0}
    if proof["kind"] != "scc-bellman-v1" or max(d0, d1) > total:
        raise ValueError("invalid Bellman certificate kind or quota range")

    # Independent reachability uses repeated source DFS, not Domain.repair_graph.
    event_out = {event: [] for event in domain.events}
    for u, v in domain.precedence:
        event_out[u].append(v)
    graph = set()
    for i in range(domain.k):
        pending, reached = list(event_out[("R", i)]), set()
        while pending:
            event = pending.pop()
            if event not in reached:
                reached.add(event)
                pending.extend(event_out[event])
        graph.update((i, j) for j in range(domain.k) if ("V", j) in reached)
    loops = {i for i in range(domain.k) if (i, i) in graph}
    eligible = set(range(domain.k)) - loops
    graph_out = {i: [j for a, j in graph if a == i and j in eligible] for i in eligible}
    reach = {}
    for source in eligible:
        pending, reached = list(graph_out[source]), {source}
        while pending:
            node = pending.pop()
            if node not in reached:
                reached.add(node)
                pending.extend(graph_out[node])
        reach[source] = reached
    checker_blocks = {tuple(sorted(j for j in eligible if j in reach[i] and i in reach[j]))
                      for i in eligible}
    checker_blocks.update((i,) for i in loops)
    blocks = tuple(tuple(block) for block in proof["components"])
    if blocks != tuple(sorted(checker_blocks)):
        raise ValueError("certificate component decomposition is incorrect")

    width, cells = d1 + 1, (d0 + 1) * (d1 + 1)
    table = proof["potentials"]
    if (len(table) != len(blocks) + 1 or any(len(row) != cells for row in table)
            or any(value is not None and (type(value) is not int or value < 0)
                   for row in table for value in row)):
        raise ValueError("malformed potential table")
    if table[-1] != [0] + [None] * (cells - 1):
        raise ValueError("incorrect terminal potentials")

    # A separate DFS cycle test; omitted vertices still occur in the full
    # opportunity reachability above, even though not in this induced graph.
    def no_cycle(selected: set[int]) -> bool:
        colors = dict.fromkeys(selected, 0)

        def visit(v: int) -> bool:
            colors[v] = 1
            for u in selected:
                if (v, u) in graph:
                    if colors[u] == 1 or (colors[u] == 0 and not visit(u)):
                        return False
            colors[v] = 2
            return True

        return all(colors[v] != 0 or visit(v) for v in sorted(selected))

    inequalities = 0
    checked_assignments = 0
    for j, block in enumerate(blocks):
        # Enumerate integer encodings independently from the solver's product.
        # For equal supports only the cheapest transition need be checked:
        # it is exactly the strongest inequality among those transitions.
        transitions: dict[tuple[int, int], int] = {}
        for encoding in range(4 ** len(block)):
            labels, encoded = {}, encoding
            for i in block:
                labels[i], encoded = encoded % 4, encoded // 4
            if any((label == 0 and i not in problem.allowed_split)
                   or (i in problem.required_split and label != 0)
                   for i, label in labels.items()):
                continue
            reversible = {i for i, label in labels.items() if label == 1}
            if not no_cycle(reversible):
                continue
            checked_assignments += 1
            a = b = cost = 0
            for i, label in labels.items():
                if label in (0, 1, 2):
                    a += domain.weights[i]
                if label in (0, 1, 3):
                    b += domain.weights[i]
                if label == 0:
                    cost += problem.costs[i]
            support = (min(d0, a), min(d1, b))
            transitions[support] = min(cost, transitions.get(support, cost))
        for a in range(d0 + 1):
            for b in range(d1 + 1):
                potential = table[j][a * width + b]
                for (support0, support1), cost in transitions.items():
                    following = table[j + 1][max(0, a - support0) * width + max(0, b - support1)]
                    inequalities += 1
                    if following is not None and (potential is None or potential > cost + following):
                        raise ValueError("Bellman lower-bound inequality is violated")
    lower = table[0][d0 * width + d1]
    if lower is None:
        if (certificate["status"] != "infeasible" or certificate["minimum_cost"] is not None
                or certificate["witness"] is not None):
            raise ValueError("infeasibility status disagrees with its lower bound")
        return {"status": "PASS", "kind": "scc-bellman-v1", "verified_inequalities": inequalities,
                "checked_local_assignments": checked_assignments, "replayed_events": 0}
    witness = certificate["witness"]
    if certificate["status"] != "optimal" or certificate["minimum_cost"] != lower or witness is None:
        raise ValueError("optimal status disagrees with its lower bound")
    labels = witness["labels"]
    if len(labels) != domain.k or any(label not in LABELS for label in labels):
        raise ValueError("invalid canonical assignment")
    split = {i for i, label in enumerate(labels) if label == "split"}
    opened = {i for i, label in enumerate(labels) if label != "second"}
    reversible = {i for i, label in enumerate(labels) if label == "reversible"}
    if (not problem.required_split <= split <= problem.allowed_split
            or witness["split"] != sorted(split) or witness["opened"] != sorted(opened)
            or witness["reversible"] != sorted(reversible)
            or not no_cycle(reversible)
            or sum(problem.costs[i] for i in split) != lower):
        raise ValueError("witness keys or cost are invalid")
    order = tuple(tuple(event) for event in witness["order"])
    if len(order) != 2 * domain.k or set(order) != set(domain.events):
        raise ValueError("witness omits or duplicates an opportunity slot")
    position = {event: index for index, event in enumerate(order)}
    if any(position[u] >= position[v] for u, v in domain.precedence):
        raise ValueError("witness violates opportunity precedence")
    if any(position[("V", i)] >= position[("R", i)] for i in reversible):
        raise ValueError("reversible witness emits its vote too late")
    repaired, second = set(), set()
    for kind, i in order:
        if kind == "R" and i in opened - split:
            repaired.add(i)
        elif kind == "V" and i not in repaired:
            second.add(i)
    first_weight = sum(domain.weights[i] for i in opened)
    second_weight = sum(domain.weights[i] for i in second)
    if (first_weight < d0 or second_weight < d1
            or witness["first_signers"] != sorted(opened)
            or witness["second_signers"] != sorted(second)
            or witness["repaired_at_end"] != sorted(repaired)
            or witness["first_weight"] != first_weight or witness["second_weight"] != second_weight):
        raise ValueError("independent replay contradicts the claimed certificate supports")
    return {"status": "PASS", "kind": "scc-bellman-v1", "verified_inequalities": inequalities,
            "checked_local_assignments": checked_assignments, "replayed_events": len(order)}
