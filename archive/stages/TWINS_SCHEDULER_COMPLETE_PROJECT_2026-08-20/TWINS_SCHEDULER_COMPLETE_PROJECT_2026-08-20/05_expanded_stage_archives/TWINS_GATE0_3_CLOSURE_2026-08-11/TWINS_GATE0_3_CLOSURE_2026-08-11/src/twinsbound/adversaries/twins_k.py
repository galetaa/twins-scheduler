from __future__ import annotations

from enum import StrEnum
from itertools import combinations

from twinsbound.adversaries.byzantine import all_subsets


class Lifecycle(StrEnum):
    GENESIS_STATIC = "genesis_static"
    SNAPSHOT_TOTAL_CAP = "snapshot_total_cap"
    SNAPSHOT_ACTIVE_REUSE = "snapshot_active_reuse"


def finite_clone_branch_sets(
    value_count: int,
    k: int,
    lifecycle: Lifecycle,
) -> tuple[frozenset[int], ...]:
    if k < 0:
        raise ValueError("k must be non-negative")
    values = tuple(range(value_count))

    if lifecycle in {Lifecycle.GENESIS_STATIC, Lifecycle.SNAPSHOT_TOTAL_CAP}:
        subsets: list[frozenset[int]] = []
        for size in range(min(k, value_count) + 1):
            subsets.extend(frozenset(c) for c in combinations(values, size))
        return tuple(subsets)

    if lifecycle is Lifecycle.SNAPSHOT_ACTIVE_REUSE:
        # With unbounded asynchronous delay and replay from genesis/snapshot,
        # one active slot can execute the required finite branch histories in
        # sequence. k=0 permits only the empty branch set.
        return all_subsets(value_count) if k >= 1 else (frozenset(),)

    raise AssertionError(f"unsupported lifecycle: {lifecycle}")
