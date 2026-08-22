from __future__ import annotations

from itertools import combinations


def all_subsets(value_count: int) -> tuple[frozenset[int], ...]:
    values = tuple(range(value_count))
    subsets: list[frozenset[int]] = []
    for size in range(value_count + 1):
        subsets.extend(frozenset(c) for c in combinations(values, size))
    return tuple(subsets)


def accepted_message_byzantine_branch_sets(value_count: int) -> tuple[frozenset[int], ...]:
    """All validator-admissible correct-history branches in the bounded model."""
    return all_subsets(value_count)
