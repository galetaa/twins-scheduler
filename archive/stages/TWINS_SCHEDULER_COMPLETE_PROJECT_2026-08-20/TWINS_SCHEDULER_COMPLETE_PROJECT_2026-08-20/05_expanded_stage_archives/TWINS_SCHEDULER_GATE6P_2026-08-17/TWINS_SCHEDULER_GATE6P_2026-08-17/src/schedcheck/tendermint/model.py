from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

HONEST_NODES: tuple[str, ...] = ("H1", "H2", "H3")
TWIN_NODES: tuple[str, ...] = ("T0", "T1")
PHYSICAL_NODES: tuple[str, ...] = TWIN_NODES + HONEST_NODES
BYZANTINE_IDENTITY = "B"
QUORUM = 3


class MessageKind(StrEnum):
    PROPOSAL = "PROPOSAL"
    PREVOTE = "PREVOTE"
    POLKA = "POLKA"
    PRECOMMIT = "PRECOMMIT"
    COMMIT = "COMMIT"
    FORGED_COMMIT = "FORGED_COMMIT"


class Grammar(StrEnum):
    PARTITION = "G_P_PARTITION"
    DIRECTED = "G_D_DIRECTED_VIEW"
    DIRECTED_DELAY1 = "G_D1_DIRECTED_DELAY1"
    TYPE_SPECIFIC = "G_T_TYPE_SPECIFIC"
    PER_MESSAGE = "G_M_PER_MESSAGE"
    PER_MESSAGE_REPLAY1 = "G_R_PER_MESSAGE_REPLAY1"


class VariantName(StrEnum):
    BASELINE = "TM_BASELINE"
    MISSING_LOCK_UPDATE = "TM_MISSING_LOCK_UPDATE"
    WRONG_VALID_ROUND_GUARD = "TM_WRONG_VALID_ROUND_GUARD"
    DUPLICATE_VOTE_COUNTING = "TM_DUPLICATE_VOTE_COUNTING"
    RECEIVER_VALIDATION_OMISSION = "TM_RECEIVER_VALIDATION_OMISSION"


@dataclass(frozen=True, slots=True)
class Variant:
    name: VariantName
    lock_on_polka: bool = True
    check_valid_round_value: bool = True
    strict_valid_round: bool = True
    count_unique_voters: bool = True
    receiver_validation_omission: str | None = None


VARIANTS: dict[VariantName, Variant] = {
    VariantName.BASELINE: Variant(VariantName.BASELINE),
    VariantName.MISSING_LOCK_UPDATE: Variant(
        VariantName.MISSING_LOCK_UPDATE,
        lock_on_polka=False,
    ),
    VariantName.WRONG_VALID_ROUND_GUARD: Variant(
        VariantName.WRONG_VALID_ROUND_GUARD,
        check_valid_round_value=False,
        strict_valid_round=False,
    ),
    VariantName.DUPLICATE_VOTE_COUNTING: Variant(
        VariantName.DUPLICATE_VOTE_COUNTING,
        count_unique_voters=False,
    ),
    VariantName.RECEIVER_VALIDATION_OMISSION: Variant(
        VariantName.RECEIVER_VALIDATION_OMISSION,
        receiver_validation_omission="H3",
    ),
}


@dataclass(frozen=True, order=True, slots=True)
class ReplicaState:
    """Persistent Tendermint-style state for one honest validator."""

    locked_value: int | None = None
    locked_round: int = 0
    valid_value: int | None = None
    valid_round: int = 0
    decision: int | None = None


@dataclass(frozen=True, order=True, slots=True)
class KernelState:
    replicas: tuple[ReplicaState, ...] = (
        ReplicaState(),
        ReplicaState(),
        ReplicaState(),
    )

    def __post_init__(self) -> None:
        if len(self.replicas) != len(HONEST_NODES):
            raise ValueError("kernel state must contain exactly three honest replicas")

    def observation(self) -> tuple[int | None, ...]:
        return tuple(replica.decision for replica in self.replicas)

    def observation_id(self) -> str:
        return "|".join(
            f"{node}={'-' if value is None else value}"
            for node, value in zip(HONEST_NODES, self.observation(), strict=True)
        )

    def unsafe(self) -> bool:
        decisions = {value for value in self.observation() if value is not None}
        return len(decisions) > 1


@dataclass(frozen=True, order=True, slots=True)
class ValidRoundProof:
    """A proposal's disclosed proof-of-lock-change (PoLC) round and value."""

    round: int
    value: int


@dataclass(frozen=True, order=True, slots=True)
class ViewPlan:
    view: int
    leader: str
    value: int
    valid_round_proof: ValidRoundProof | None = None
    emit_forged_commit: bool = False

    def __post_init__(self) -> None:
        if self.leader not in TWIN_NODES:
            raise ValueError("bounded kernel uses one active Byzantine twin per round")
        if self.value not in (0, 1):
            raise ValueError("bounded kernel values are binary")
        if self.view < 1:
            raise ValueError("rounds start at one")
        if self.valid_round_proof is not None:
            if self.valid_round_proof.round >= self.view:
                raise ValueError("valid round must precede proposal round")
            if self.valid_round_proof.round < 1:
                raise ValueError("valid round proof must refer to a positive round")


@dataclass(frozen=True, order=True, slots=True)
class KernelMessage:
    uid: str
    view: int
    stage: int
    kind: MessageKind
    sender: str
    receiver: str
    value: int | None = None
    valid_round_proof: ValidRoundProof | None = None
    signer_count: int | None = None

    def token(self) -> str:
        payload: list[str] = []
        if self.value is not None:
            payload.append(f"value={self.value}")
        if self.valid_round_proof is not None:
            payload.append(
                f"valid_round={self.valid_round_proof.round}:"
                f"{self.valid_round_proof.value}"
            )
        if self.signer_count is not None:
            payload.append(f"signers={self.signer_count}")
        suffix = "" if not payload else "[" + ",".join(payload) + "]"
        return (
            f"r{self.view}:s{self.stage}:{self.uid}:"
            f"{self.sender}->{self.receiver}:{self.kind.value}{suffix}"
        )


@dataclass(frozen=True, order=True, slots=True)
class ViewRuntime:
    persistent: KernelState
    accepted: tuple[bool, ...] = (False, False, False)
    ready_to_precommit: tuple[bool, ...] = (False, False, False)
    prevote_receipts: tuple[str, ...] = ()
    precommit_receipts: tuple[str, ...] = ()
    polka: bool = False
    commit: bool = False

    def replace_replica(self, index: int, replica: ReplicaState) -> "ViewRuntime":
        replicas = list(self.persistent.replicas)
        replicas[index] = replica
        return ViewRuntime(
            persistent=KernelState(tuple(replicas)),
            accepted=self.accepted,
            ready_to_precommit=self.ready_to_precommit,
            prevote_receipts=self.prevote_receipts,
            precommit_receipts=self.precommit_receipts,
            polka=self.polka,
            commit=self.commit,
        )

    def with_fields(self, **changes: Any) -> "ViewRuntime":
        values = {
            "persistent": self.persistent,
            "accepted": self.accepted,
            "ready_to_precommit": self.ready_to_precommit,
            "prevote_receipts": self.prevote_receipts,
            "precommit_receipts": self.precommit_receipts,
            "polka": self.polka,
            "commit": self.commit,
        }
        values.update(changes)
        return ViewRuntime(**values)


@dataclass(frozen=True, slots=True)
class StageDelivery:
    stage: int
    emitted: tuple[str, ...]
    delivered: tuple[str, ...]
    deferred: tuple[str, ...] = ()

    @property
    def delivered_count(self) -> int:
        return len(self.delivered)


@dataclass(frozen=True, slots=True)
class ViewTrace:
    view: int
    leader: str
    value: int
    policy: str
    stages: tuple[StageDelivery, ...]
    late_delivered: tuple[str, ...] = ()

    @property
    def delivered_count(self) -> int:
        return sum(stage.delivered_count for stage in self.stages) + len(
            self.late_delivered
        )


@dataclass(frozen=True, slots=True)
class KernelWitness:
    case_id: str
    variant: VariantName
    grammar: Grammar
    observation: tuple[int | None, ...]
    views: tuple[ViewTrace, ...]

    @property
    def delivered_count(self) -> int:
        return sum(view.delivered_count for view in self.views)

    def rank(self) -> tuple[int, int, tuple[str, ...]]:
        tokens: list[str] = []
        for view in self.views:
            tokens.append(view.policy)
            for stage in view.stages:
                tokens.extend(stage.delivered)
                tokens.extend(f"DEFER:{token}" for token in stage.deferred)
            tokens.extend(f"LATE:{token}" for token in view.late_delivered)
        return (self.delivered_count, len(tokens), tuple(tokens))

    def observation_id(self) -> str:
        return "|".join(
            f"{node}={'-' if value is None else value}"
            for node, value in zip(HONEST_NODES, self.observation, strict=True)
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "variant": self.variant.value,
            "grammar": self.grammar.value,
            "observation": self.observation_id(),
            "unsafe": len({v for v in self.observation if v is not None}) > 1,
            "delivered_count": self.delivered_count,
            "views": [
                {
                    "round": view.view,
                    "leader": view.leader,
                    "value": view.value,
                    "policy": view.policy,
                    "late_delivered": list(view.late_delivered),
                    "stages": [
                        {
                            "stage": stage.stage,
                            "emitted": list(stage.emitted),
                            "delivered": list(stage.delivered),
                            "deferred": list(stage.deferred),
                        }
                        for stage in view.stages
                    ],
                }
                for view in self.views
            ],
        }
