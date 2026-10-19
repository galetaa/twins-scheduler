"""Finite repair/issuance semantics and an independently usable order model.

This is a certificate schema, not a production consensus implementation.
All enabling deliveries and first-vote opportunities precede the events here.
An admitted repair disables *future* issuance; it never deletes a signed vote.
By default a pivot can issue its second vote without first being enabled.
That initial readiness matches the missing-lock example's edge-off behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator

Event = tuple[str, int]


def subsets(k: int) -> Iterator[frozenset[int]]:
    for mask in range(1 << k):
        yield frozenset(i for i in range(k) if mask & (1 << i))


def acyclic(vertices: Iterable, edges: Iterable[tuple]) -> bool:
    vertices = frozenset(vertices)
    outgoing = {v: set() for v in vertices}
    indegree = dict.fromkeys(vertices, 0)
    for u, v in set(edges):
        if u in vertices and v in vertices:
            outgoing[u].add(v)
            indegree[v] += 1
    ready = [v for v in vertices if indegree[v] == 0]
    consumed = 0
    while ready:
        u = ready.pop()
        consumed += 1
        for v in outgoing[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    return consumed == len(vertices)


@dataclass(frozen=True)
class Domain:
    """Order constraints on repairs R_i and irreversible vote issues V_i."""

    weights: tuple[int, ...]
    precedence: frozenset[tuple[Event, Event]] = frozenset()
    initially_ready: bool = True

    def __post_init__(self) -> None:
        if not self.weights or any(type(w) is not int or w <= 0 for w in self.weights):
            raise ValueError("weights must be a nonempty tuple of positive integers")
        if any(u not in self.events or v not in self.events for u, v in self.precedence):
            raise ValueError("precedence references an unknown event")
        if not acyclic(self.events, self.precedence):
            raise ValueError("the execution domain must be acyclic")

    @property
    def k(self) -> int:
        return len(self.weights)

    @property
    def events(self) -> tuple[Event, ...]:
        return tuple((kind, i) for kind in ("R", "V") for i in range(self.k))

    def orders(self) -> Iterator[tuple[Event, ...]]:
        predecessors = {v: set() for v in self.events}
        for u, v in self.precedence:
            predecessors[v].add(u)

        def visit(prefix: tuple[Event, ...], remaining: frozenset[Event]):
            if not remaining:
                yield prefix
                return
            for v in sorted(remaining):
                if not (predecessors[v] & remaining):
                    yield from visit(prefix + (v,), remaining - {v})

        yield from visit((), frozenset(self.events))

    def repair_graph(self) -> frozenset[tuple[int, int]]:
        """i -> j exactly when P forces delivery R_i before issuance V_j."""
        reach = {v: set() for v in self.events}
        for u, v in self.precedence:
            reach[u].add(v)
        for middle in self.events:
            for source in self.events:
                if middle in reach[source]:
                    reach[source].update(reach[middle])
        return frozenset(
            (i, j) for i in range(self.k) for j in range(self.k)
            if ("V", j) in reach[("R", i)]
        )

    def acyclic_capacity(self) -> int:
        graph = self.repair_graph()
        return max(len(s) for s in subsets(self.k) if acyclic(s, graph))


@dataclass(frozen=True)
class Run:
    opened: frozenset[int]
    phase_split: frozenset[int]
    order: tuple[Event, ...]
    first_signers: frozenset[int]
    second_signers: frozenset[int]
    repaired_at_end: frozenset[int]
    first_weight: int
    second_weight: int

    def violates(self, deficit0: int, deficit1: int) -> bool:
        return self.first_weight >= deficit0 and self.second_weight >= deficit1


def execute(
    domain: Domain,
    opened: Iterable[int],
    order: Iterable[Event],
    phase_split: Iterable[int] = (),
) -> Run:
    """Process events, with once-only delivery and irreversible output sets.

    A split channel admits E and withholds R. Closed channels admit neither.
    R slots for suppressed envelopes are silent opportunities, not deliveries.
    Decisions are collected after the order; repair may thus precede a decision
    while still being too late to prevent the corresponding signed output.
    """
    opened, split = frozenset(opened), frozenset(phase_split)
    valid = frozenset(range(domain.k))
    if not opened <= valid or not split <= opened:
        raise ValueError("split channels must be opened, and all indices must exist")
    order = tuple(order)
    if len(order) != len(domain.events) or frozenset(order) != frozenset(domain.events):
        raise ValueError("each event opportunity must occur exactly once")
    positions = {v: i for i, v in enumerate(order)}
    if any(positions[u] >= positions[v] for u, v in domain.precedence):
        raise ValueError("the event order is not a legal linear extension")

    # Enabling envelopes were emitted in the common prefix. Delivering each
    # admitted E_i permits one first signature; no closed channel can create it.
    enabled: set[int] = set()
    first: set[int] = set()
    for i in range(domain.k):
        if i in opened:
            enabled.add(i)
        if i in enabled:
            first.add(i)
    repaired: set[int] = set()
    second: set[int] = set()
    for kind, i in order:
        if kind == "R":
            if i in opened and i not in split:
                repaired.add(i)
        elif i not in repaired and (domain.initially_ready or i in enabled):
            second.add(i)
    return Run(
        opened, split, order, frozenset(first), frozenset(second),
        frozenset(repaired), sum(domain.weights[i] for i in first),
        sum(domain.weights[i] for i in second),
    )


def from_graph(k: int, edges: Iterable[tuple[int, int]], weights=None) -> Domain:
    """Realize any directed graph by an acyclic R-layer -> V-layer order."""
    return Domain(
        tuple(weights) if weights is not None else (1,) * k,
        frozenset((("R", i), ("V", j)) for i, j in edges),
    )


def common_deadline(k: int, forced: Iterable[int], weights=None) -> Domain:
    """Construct a support-equivalent order domain for a shared vote barrier.

    Forced repairs precede every V. The caller may choose a consecutive V block
    for barrier runs; the returned partial order also permits interleavings.
    These do not increase the attainable certificate-support region because
    all unforced repairs can already jointly follow the entire V block.
    """
    forced = frozenset(forced)
    edges = {(("R", i), ("V", j)) for i in forced for j in range(k)}
    return Domain(tuple(weights) if weights is not None else (1,) * k, frozenset(edges))


def coarse_boundary(k: int, capacity: int, deficit0: int, deficit1: int) -> bool:
    if not (0 <= capacity <= k and deficit0 >= 0 and deficit1 >= 0):
        raise ValueError("invalid capacity or deficit")
    return max(deficit0, deficit1) <= k and deficit0 + deficit1 <= k + capacity


def minimum_phase_splits(k: int, capacity: int, deficit0: int, deficit1: int) -> int | None:
    if max(deficit0, deficit1) > k:
        return None
    return max(0, deficit0 + deficit1 - k - capacity)


def weighted_common_boundary(weights, forced, deficit0: int, deficit1: int) -> bool:
    """Exact subset-interval criterion; total capacity alone is insufficient."""
    weights = tuple(weights)
    forced = frozenset(forced)
    total = sum(weights)
    late = sum(w for i, w in enumerate(weights) if i not in forced)
    if max(deficit0, deficit1) > total:
        return False
    return any(
        max(0, deficit0 - late) <= sum(weights[i] for i in s) <= total - deficit1
        for s in subsets(len(weights)) if s <= forced
    )
