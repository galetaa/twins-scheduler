from __future__ import annotations

import random
from typing import Any

NODES = ("T0", "T1", "H1", "H2", "H3")
TYPES = ("PROPOSE", "VOTE", "HASH", "NEW_VIEW", "TIMEOUT", "UNCONTROLLED")


def _partitions(rng: random.Random) -> list[list[str]]:
    groups: dict[int, list[str]] = {}
    for node in NODES:
        groups.setdefault(rng.randrange(1, 4), []).append(node)
    return [groups[key] for key in sorted(groups)]


def fixed_cases() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_partition_controlled_passes",
            "views": [{"partitions": [["T0", "H1"], ["H2", "H3", "T1"]]}],
            "drop_types": ["PROPOSE", "VOTE"],
            "global_view": 1,
            "messages": [
                {"id": "m0", "sender": "T0", "receiver": "H1", "type": "PROPOSE", "view": 1}
            ],
            "ticks": 1,
        },
        {
            "id": "cross_partition_controlled_drops",
            "views": [{"partitions": [["T0"], ["H1", "H2", "H3", "T1"]]}],
            "drop_types": ["PROPOSE", "VOTE"],
            "global_view": 1,
            "messages": [
                {"id": "m0", "sender": "T0", "receiver": "H1", "type": "PROPOSE", "view": 1}
            ],
            "ticks": 1,
        },
        {
            "id": "cross_partition_uncontrolled_passes",
            "views": [{"partitions": [["T0"], ["H1", "H2", "H3", "T1"]]}],
            "drop_types": ["PROPOSE", "VOTE"],
            "global_view": 1,
            "messages": [
                {"id": "m0", "sender": "T0", "receiver": "H1", "type": "UNCONTROLLED", "view": 1}
            ],
            "ticks": 1,
        },
        {
            "id": "future_message_waits_for_idle_ticks",
            "views": [
                {"partitions": [list(NODES)]},
                {"partitions": [list(NODES)]},
                {"partitions": [list(NODES)]},
            ],
            "drop_types": ["PROPOSE", "VOTE", "HASH", "NEW_VIEW", "TIMEOUT"],
            "global_view": 1,
            "messages": [
                {"id": "now", "sender": "T0", "receiver": "H1", "type": "PROPOSE", "view": 1},
                {"id": "future", "sender": "T1", "receiver": "H2", "type": "PROPOSE", "view": 3},
            ],
            "ticks": 4,
        },
        {
            "id": "out_of_scenario_drops_every_type",
            "views": [{"partitions": [list(NODES)]}],
            "drop_types": [],
            "global_view": 1,
            "messages": [
                {"id": "m0", "sender": "T0", "receiver": "H1", "type": "UNCONTROLLED", "view": 2}
            ],
            "ticks": 1,
        },
        {
            "id": "nonpositive_view_is_not_filtered",
            "views": [],
            "drop_types": list(TYPES),
            "global_view": 0,
            "messages": [
                {"id": "m0", "sender": "T0", "receiver": "H1", "type": "PROPOSE", "view": 0}
            ],
            "ticks": 1,
        },
    ]


def generate_corpus(seed: int = 20260815, random_cases: int = 128) -> dict[str, Any]:
    rng = random.Random(seed)
    cases = fixed_cases()
    for case_index in range(random_cases):
        view_count = rng.randint(1, 4)
        views = [{"partitions": _partitions(rng)} for _ in range(view_count)]
        drop_types = sorted(rng.sample(TYPES, rng.randint(0, len(TYPES))))
        messages: list[dict[str, Any]] = []
        for message_index in range(rng.randint(0, 16)):
            sender = rng.choice(NODES)
            receiver = rng.choice(tuple(node for node in NODES if node != sender))
            messages.append(
                {
                    "id": f"r{case_index:03d}-m{message_index:02d}",
                    "sender": sender,
                    "receiver": receiver,
                    "type": rng.choice(TYPES),
                    "view": rng.randint(0, view_count + 2),
                }
            )
        cases.append(
            {
                "id": f"random_{case_index:03d}",
                "views": views,
                "drop_types": drop_types,
                "global_view": rng.randint(0, view_count + 1),
                "messages": messages,
                "ticks": rng.randint(0, 8),
            }
        )
    return {"seed": seed, "random_cases": random_cases, "cases": cases}
