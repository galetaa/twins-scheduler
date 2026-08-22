"""Python reference for the pinned relab/hotstuff Twins network semantics.

The model covers only the two source-level decisions relevant to Gate 4':
message admission by view partitions/drop types and the pending queue's global
view gate. It does not model node event loops or a consensus implementation.
"""
from __future__ import annotations

from typing import Any


def should_drop(case: dict[str, Any], message: dict[str, Any]) -> bool:
    index = int(message["view"]) - 1
    if index < 0:
        return False
    views = case["views"]
    if index >= len(views):
        return True
    sender = message["sender"]
    receiver = message["receiver"]
    for partition in views[index]["partitions"]:
        if sender in partition and receiver in partition:
            return False
    return message["type"] in case["drop_types"]


def execute_case(case: dict[str, Any]) -> dict[str, Any]:
    global_view = int(case["global_view"])
    pending: list[dict[str, Any]] = []
    dropped: list[str] = []

    for message in case["messages"]:
        if should_drop(case, message):
            dropped.append(message["id"])
        else:
            pending.append(message)

    delivered_by_tick: list[list[str]] = []
    for _ in range(int(case["ticks"])):
        next_pending: list[dict[str, Any]] = []
        delivered: list[str] = []
        for message in pending:
            if int(message["view"]) > global_view:
                next_pending.append(message)
            else:
                delivered.append(message["id"])
        if len(pending) == len(next_pending):
            global_view += 1
        pending = next_pending
        delivered_by_tick.append(delivered)

    return {
        "id": case["id"],
        "dropped_ids": sorted(dropped),
        "delivered_by_tick": delivered_by_tick,
        "pending_ids": sorted(message["id"] for message in pending),
        "final_global_view": global_view,
    }


def execute_corpus(payload: dict[str, Any]) -> dict[str, Any]:
    return {"results": [execute_case(case) for case in payload["cases"]]}
