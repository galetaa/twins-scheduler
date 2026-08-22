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
    PRECOMMIT_QC = "PRECOMMIT_QC"
    TIMEOUT_QC = "TIMEOUT_QC"
    PRECOMMIT = "PRECOMMIT"
    COMMIT_QC = "COMMIT_QC"
    FORGED_COMMIT_QC = "FORGED_COMMIT_QC"


class Grammar(StrEnum):
    PARTITION = "G_P_PARTITION"
    DIRECTED = "G_D_DIRECTED_VIEW"
    DIRECTED_DELAY1 = "G_D1_DIRECTED_DELAY1"
    TYPE_SPECIFIC = "G_T_TYPE_SPECIFIC"
    PER_MESSAGE = "G_M_PER_MESSAGE"
    PER_MESSAGE_REPLAY1 = "G_R_PER_MESSAGE_REPLAY1"


class VariantName(StrEnum):
    BASELINE = "BASELINE"
    MISSING_LOCK_UPDATE = "MISSING_LOCK_UPDATE"
    WRONG_QC_GUARD = "WRONG_QC_GUARD"
    TIMEOUT_AS_PRECOMMIT = "TIMEOUT_AS_PRECOMMIT"
    DUPLICATE_VOTE_COUNTING = "DUPLICATE_VOTE_COUNTING"
    RECEIVER_VALIDATION_OMISSION = "RECEIVER_VALIDATION_OMISSION"


@dataclass(frozen=True, slots=True)
class Variant:
    name: VariantName
    lock_on_precommit_qc: bool = True
    check_justify_value: bool = True
    strict_unlock_view: bool = True
    timeout_qc_acts_as_precommit: bool = False
    timeout_path_updates_lock: bool = True
    count_unique_voters: bool = True
    receiver_validation_omission: str | None = None


VARIANTS: dict[VariantName, Variant] = {
    VariantName.BASELINE: Variant(VariantName.BASELINE),
    VariantName.MISSING_LOCK_UPDATE: Variant(
        VariantName.MISSING_LOCK_UPDATE,
        lock_on_precommit_qc=False,
    ),
    VariantName.WRONG_QC_GUARD: Variant(
        VariantName.WRONG_QC_GUARD,
        check_justify_value=False,
        strict_unlock_view=False,
    ),
    VariantName.TIMEOUT_AS_PRECOMMIT: Variant(
        VariantName.TIMEOUT_AS_PRECOMMIT,
        timeout_qc_acts_as_precommit=True,
        timeout_path_updates_lock=False,
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
    locked_value: int | None = None
    locked_view: int = 0
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
class Justification:
    view: int
    value: int


@dataclass(frozen=True, order=True, slots=True)
class ViewPlan:
    view: int
    leader: str
    value: int
    justification: Justification | None = None
    emit_timeout_qc: bool = False
    emit_forged_commit_qc: bool = False

    def __post_init__(self) -> None:
        if self.leader not in TWIN_NODES:
            raise ValueError("bounded kernel uses one active Byzantine twin per view")
        if self.value not in (0, 1):
            raise ValueError("bounded kernel values are binary")
        if self.view < 1:
            raise ValueError("views start at one")


@dataclass(frozen=True, order=True, slots=True)
class KernelMessage:
    uid: str
    view: int
    stage: int
    kind: MessageKind
    sender: str
    receiver: str
    value: int | None = None
    justification: Justification | None = None
    signer_count: int | None = None

    def token(self) -> str:
        payload: list[str] = []
        if self.value is not None:
            payload.append(f"value={self.value}")
        if self.justification is not None:
            payload.append(
                f"justify={self.justification.view}:{self.justification.value}"
            )
        if self.signer_count is not None:
            payload.append(f"signers={self.signer_count}")
        suffix = "" if not payload else "[" + ",".join(payload) + "]"
        return (
            f"v{self.view}:s{self.stage}:{self.uid}:"
            f"{self.sender}->{self.receiver}:{self.kind.value}{suffix}"
        )


@dataclass(frozen=True, order=True, slots=True)
class ViewRuntime:
    persistent: KernelState
    accepted: tuple[bool, ...] = (False, False, False)
    ready_to_precommit: tuple[bool, ...] = (False, False, False)
    prevote_receipts: tuple[str, ...] = ()
    precommit_receipts: tuple[str, ...] = ()
    prepare_qc: bool = False
    commit_qc: bool = False

    def replace_replica(self, index: int, replica: ReplicaState) -> "ViewRuntime":
        replicas = list(self.persistent.replicas)
        replicas[index] = replica
        return ViewRuntime(
            persistent=KernelState(tuple(replicas)),
            accepted=self.accepted,
            ready_to_precommit=self.ready_to_precommit,
            prevote_receipts=self.prevote_receipts,
            precommit_receipts=self.precommit_receipts,
            prepare_qc=self.prepare_qc,
            commit_qc=self.commit_qc,
        )

    def with_fields(self, **changes: Any) -> "ViewRuntime":
        values = {
            "persistent": self.persistent,
            "accepted": self.accepted,
            "ready_to_precommit": self.ready_to_precommit,
            "prevote_receipts": self.prevote_receipts,
            "precommit_receipts": self.precommit_receipts,
            "prepare_qc": self.prepare_qc,
            "commit_qc": self.commit_qc,
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
        return (
            sum(stage.delivered_count for stage in self.stages)
            + len(self.late_delivered)
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
                    "view": view.view,
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
