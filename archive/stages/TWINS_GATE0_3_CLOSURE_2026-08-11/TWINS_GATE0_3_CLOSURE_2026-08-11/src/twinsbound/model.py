from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


class StatusKind(StrEnum):
    NONE = "N"
    PROPOSAL = "P"
    DECISION = "D"


@dataclass(frozen=True, order=True, slots=True)
class NodeStatus:
    kind: StatusKind
    value: int | None = None

    def __post_init__(self) -> None:
        if self.kind is StatusKind.NONE and self.value is not None:
            raise ValueError("NONE status cannot carry a value")
        if self.kind is not StatusKind.NONE and self.value is None:
            raise ValueError("P/D status must carry a value")
        if self.value is not None and self.value < 0:
            raise ValueError("values must be non-negative")

    @classmethod
    def none(cls) -> "NodeStatus":
        return cls(StatusKind.NONE, None)

    @classmethod
    def proposal(cls, value: int) -> "NodeStatus":
        return cls(StatusKind.PROPOSAL, value)

    @classmethod
    def decision(cls, value: int) -> "NodeStatus":
        return cls(StatusKind.DECISION, value)

    def token(self) -> str:
        return self.kind.value if self.value is None else f"{self.kind.value}{self.value}"


@dataclass(frozen=True, order=True, slots=True)
class Observation:
    """Labeled correct-replica terminal observation.

    P(v) means the replica received the Byzantine leader's causally valid
    proposal, locked/voted v, but did not receive a commit certificate.
    D(v) means it additionally received a valid commit certificate and decided v.
    """

    statuses: tuple[NodeStatus, ...]

    def used_values(self) -> frozenset[int]:
        return frozenset(s.value for s in self.statuses if s.value is not None)

    def decided_values(self) -> frozenset[int]:
        return frozenset(
            s.value for s in self.statuses
            if s.kind is StatusKind.DECISION and s.value is not None
        )

    def width(self) -> int:
        """Incompatibility width in this pilot: number of distinct branch histories."""
        return len(self.used_values())

    def unsafe(self) -> bool:
        return len(self.decided_values()) >= 2

    def canonical_id(self) -> str:
        return "|".join(s.token() for s in self.statuses)

    def decision_projection(self) -> "Observation":
        return Observation(tuple(
            s if s.kind is StatusKind.DECISION else NodeStatus.none()
            for s in self.statuses
        ))

    def minimal_pair_core(self) -> "Observation | None":
        """Return a two-decision sub-observation witnessing agreement violation."""
        chosen: list[tuple[int, int]] = []
        seen: set[int] = set()
        for idx, status in enumerate(self.statuses):
            if status.kind is StatusKind.DECISION and status.value is not None:
                if status.value not in seen:
                    chosen.append((idx, status.value))
                    seen.add(status.value)
                if len(chosen) == 2:
                    break
        if len(chosen) < 2:
            return None
        out = [NodeStatus.none() for _ in self.statuses]
        for idx, value in chosen:
            out[idx] = NodeStatus.decision(value)
        return Observation(tuple(out))

    @classmethod
    def from_tokens(cls, tokens: Iterable[str]) -> "Observation":
        statuses: list[NodeStatus] = []
        for token in tokens:
            if token == "N":
                statuses.append(NodeStatus.none())
            elif token.startswith("P"):
                statuses.append(NodeStatus.proposal(int(token[1:])))
            elif token.startswith("D"):
                statuses.append(NodeStatus.decision(int(token[1:])))
            else:
                raise ValueError(f"invalid token: {token}")
        return cls(tuple(statuses))


@dataclass(frozen=True, slots=True)
class Event:
    kind: str
    node: int | None = None
    value: int | None = None

    def as_dict(self) -> dict[str, int | str | None]:
        return {"kind": self.kind, "node": self.node, "value": self.value}
