from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, order=True, slots=True)
class Message:
    """A single emitted message instance in the bounded pilot."""

    uid: str
    phase: int
    ordinal: int
    kind: str
    sender: str
    receiver: str
    value: int | None = None

    @property
    def edge(self) -> tuple[str, str]:
        return (self.sender, self.receiver)

    @property
    def type_edge(self) -> tuple[str, str, str]:
        return (self.kind, self.sender, self.receiver)

    def token(self) -> str:
        value = "" if self.value is None else f"={self.value}"
        return f"{self.uid}:{self.sender}->{self.receiver}:{self.kind}{value}"


@dataclass(frozen=True, slots=True)
class Event:
    action: str
    phase: int
    detail: str

    def token(self) -> str:
        return f"p{self.phase}:{self.action}:{self.detail}"


@dataclass(frozen=True, order=True, slots=True)
class Observation:
    """Safety-relevant decisions of correct replicas, in a fixed node order."""

    nodes: tuple[str, ...]
    decisions: tuple[int | None, ...]

    def __post_init__(self) -> None:
        if len(self.nodes) != len(self.decisions):
            raise ValueError("nodes and decisions must have equal length")

    def unsafe(self) -> bool:
        decided = {value for value in self.decisions if value is not None}
        return len(decided) > 1

    def canonical_id(self) -> str:
        parts = []
        for node, value in zip(self.nodes, self.decisions, strict=True):
            parts.append(f"{node}={'-' if value is None else value}")
        return "|".join(parts)


@dataclass(frozen=True, slots=True)
class Witness:
    grammar: str
    protocol: str
    schedule_id: str
    observation: Observation
    events: tuple[Event, ...]
    delivered_by_phase: tuple[tuple[str, ...], ...]
    schedule_data: tuple[tuple[str, str], ...] = ()

    @property
    def delivered_count(self) -> int:
        return sum(len(x) for x in self.delivered_by_phase)

    def rank(self) -> tuple[int, int, tuple[str, ...]]:
        return (
            self.delivered_count,
            len(self.events),
            tuple(event.token() for event in self.events),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "grammar": self.grammar,
            "protocol": self.protocol,
            "schedule_id": self.schedule_id,
            "observation": self.observation.canonical_id(),
            "unsafe": self.observation.unsafe(),
            "delivered_by_phase": [list(x) for x in self.delivered_by_phase],
            "schedule_data": dict(self.schedule_data),
            "events": [event.token() for event in self.events],
        }
