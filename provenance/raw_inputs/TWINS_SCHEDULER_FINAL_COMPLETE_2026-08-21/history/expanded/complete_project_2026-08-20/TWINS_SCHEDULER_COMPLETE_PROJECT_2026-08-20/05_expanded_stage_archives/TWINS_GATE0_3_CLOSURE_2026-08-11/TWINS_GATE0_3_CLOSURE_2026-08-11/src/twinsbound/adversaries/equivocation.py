from __future__ import annotations

from twinsbound.adversaries.byzantine import all_subsets


def dynamic_equivocation_branch_sets(value_count: int) -> tuple[frozenset[int], ...]:
    """Dynamic copies can realize every finite subset of distinct local histories."""
    return all_subsets(value_count)
