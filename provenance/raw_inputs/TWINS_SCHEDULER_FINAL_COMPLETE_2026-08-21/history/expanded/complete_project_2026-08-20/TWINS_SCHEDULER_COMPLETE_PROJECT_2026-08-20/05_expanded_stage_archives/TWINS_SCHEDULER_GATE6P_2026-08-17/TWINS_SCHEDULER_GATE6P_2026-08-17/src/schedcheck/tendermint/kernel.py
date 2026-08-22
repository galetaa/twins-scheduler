from __future__ import annotations

from dataclasses import replace

from schedcheck.tendermint.model import (
    BYZANTINE_IDENTITY,
    HONEST_NODES,
    QUORUM,
    KernelMessage,
    KernelState,
    MessageKind,
    ReplicaState,
    ValidRoundProof,
    Variant,
    ViewPlan,
    ViewRuntime,
)

STAGE_COUNT = 5
STAGE_NAMES: tuple[str, ...] = (
    "proposal",
    "prevote",
    "polka-evidence",
    "precommit",
    "commit-evidence",
)


def _message(
    plan: ViewPlan,
    stage: int,
    kind: MessageKind,
    sender: str,
    receiver: str,
    *,
    value: int | None = None,
    valid_round_proof: ValidRoundProof | None = None,
    signer_count: int | None = None,
    suffix: str = "",
) -> KernelMessage:
    uid = f"r{plan.view}-{kind.value.lower()}-{sender}-{receiver}{suffix}"
    return KernelMessage(
        uid=uid,
        view=plan.view,
        stage=stage,
        kind=kind,
        sender=sender,
        receiver=receiver,
        value=value,
        valid_round_proof=valid_round_proof,
        signer_count=signer_count,
    )


def initial_runtime(state: KernelState) -> ViewRuntime:
    return ViewRuntime(persistent=state)


def proposal_is_safe(
    replica: ReplicaState,
    proposal_value: int,
    proof: ValidRoundProof | None,
    variant: Variant,
) -> bool:
    """Tendermint-style valid-round proposal guard.

    A replica accepts an unlocked proposal or one matching its current lock. A
    conflicting proposal requires evidence for the proposed value from a round
    strictly greater than the local lock round. The controlled guard mutation
    erases the value equality test and admits equality of rounds.
    """

    if replica.decision is not None and replica.decision != proposal_value:
        return False

    if replica.locked_value is None or replica.locked_value == proposal_value:
        return True

    if proof is None:
        return False
    if variant.check_valid_round_value and proof.value != proposal_value:
        return False
    if variant.strict_valid_round:
        return proof.round > replica.locked_round
    return proof.round >= replica.locked_round


def quorum_reached(receipts: tuple[str, ...], variant: Variant) -> bool:
    voter_count = len(set(receipts)) if variant.count_unique_voters else len(receipts)
    # The Byzantine proposer contributes one logical vote. T0 and T1 share one
    # signing identity and never count as two validators.
    return 1 + voter_count >= QUORUM


def emit_stage(
    runtime: ViewRuntime,
    plan: ViewPlan,
    stage: int,
    variant: Variant,
) -> tuple[KernelMessage, ...]:
    if stage == 0:
        return tuple(
            _message(
                plan,
                stage,
                MessageKind.PROPOSAL,
                plan.leader,
                receiver,
                value=plan.value,
                valid_round_proof=plan.valid_round_proof,
            )
            for receiver in HONEST_NODES
        )

    if stage == 1:
        return tuple(
            _message(
                plan,
                stage,
                MessageKind.PREVOTE,
                sender,
                plan.leader,
                value=plan.value,
            )
            for sender, accepted in zip(HONEST_NODES, runtime.accepted, strict=True)
            if accepted
        )

    if stage == 2:
        if not runtime.polka:
            return ()
        return tuple(
            _message(
                plan,
                stage,
                MessageKind.POLKA,
                plan.leader,
                receiver,
                value=plan.value,
                signer_count=QUORUM,
            )
            for receiver in HONEST_NODES
        )

    if stage == 3:
        return tuple(
            _message(
                plan,
                stage,
                MessageKind.PRECOMMIT,
                sender,
                plan.leader,
                value=plan.value,
            )
            for sender, ready in zip(
                HONEST_NODES, runtime.ready_to_precommit, strict=True
            )
            if ready
        )

    if stage == 4:
        messages: list[KernelMessage] = []
        if runtime.commit:
            messages.extend(
                _message(
                    plan,
                    stage,
                    MessageKind.COMMIT,
                    plan.leader,
                    receiver,
                    value=plan.value,
                    signer_count=QUORUM,
                )
                for receiver in HONEST_NODES
            )
        if plan.emit_forged_commit:
            messages.extend(
                _message(
                    plan,
                    stage,
                    MessageKind.FORGED_COMMIT,
                    plan.leader,
                    receiver,
                    value=plan.value,
                    signer_count=1,
                    suffix="-forged",
                )
                for receiver in HONEST_NODES
            )
        return tuple(messages)

    raise ValueError(f"invalid stage {stage}")


def _honest_index(node: str) -> int:
    try:
        return HONEST_NODES.index(node)
    except ValueError as error:
        raise ValueError(f"not an honest replica: {node}") from error


def _set_tuple_flag(values: tuple[bool, ...], index: int, value: bool) -> tuple[bool, ...]:
    updated = list(values)
    updated[index] = value
    return tuple(updated)


def _on_polka(
    replica: ReplicaState,
    value: int,
    round_number: int,
    variant: Variant,
) -> ReplicaState:
    updated = replace(replica, valid_value=value, valid_round=round_number)
    if variant.lock_on_polka and round_number >= updated.locked_round:
        updated = replace(
            updated,
            locked_value=value,
            locked_round=round_number,
        )
    return updated


def _decide(replica: ReplicaState, value: int, round_number: int) -> ReplicaState:
    if replica.decision is not None:
        return replica
    return replace(
        replica,
        locked_value=value,
        locked_round=max(replica.locked_round, round_number),
        valid_value=value,
        valid_round=max(replica.valid_round, round_number),
        decision=value,
    )


def deliver(
    runtime: ViewRuntime,
    message: KernelMessage,
    plan: ViewPlan,
    variant: Variant,
) -> ViewRuntime:
    if message.view != plan.view:
        raise ValueError("this bounded kernel only delivers same-round messages")

    if message.kind == MessageKind.PROPOSAL:
        index = _honest_index(message.receiver)
        replica = runtime.persistent.replicas[index]
        if proposal_is_safe(replica, plan.value, plan.valid_round_proof, variant):
            return runtime.with_fields(
                accepted=_set_tuple_flag(runtime.accepted, index, True)
            )
        return runtime

    if message.kind == MessageKind.PREVOTE:
        if message.receiver != plan.leader:
            raise ValueError("prevote sent to non-leader")
        return runtime.with_fields(
            prevote_receipts=tuple(sorted(runtime.prevote_receipts + (message.sender,)))
        )

    if message.kind == MessageKind.POLKA:
        index = _honest_index(message.receiver)
        if not runtime.accepted[index]:
            return runtime
        ready = _set_tuple_flag(runtime.ready_to_precommit, index, True)
        updated = runtime.with_fields(ready_to_precommit=ready)
        replica = updated.persistent.replicas[index]
        return updated.replace_replica(
            index, _on_polka(replica, plan.value, plan.view, variant)
        )

    if message.kind == MessageKind.PRECOMMIT:
        if message.receiver != plan.leader:
            raise ValueError("precommit sent to non-leader")
        return runtime.with_fields(
            precommit_receipts=tuple(
                sorted(runtime.precommit_receipts + (message.sender,))
            )
        )

    if message.kind in (MessageKind.COMMIT, MessageKind.FORGED_COMMIT):
        index = _honest_index(message.receiver)
        valid = (message.signer_count or 0) >= QUORUM
        if not valid and variant.receiver_validation_omission != message.receiver:
            return runtime
        replica = runtime.persistent.replicas[index]
        return runtime.replace_replica(index, _decide(replica, plan.value, plan.view))

    raise ValueError(f"unsupported message kind: {message.kind}")


def complete_stage(runtime: ViewRuntime, stage: int, variant: Variant) -> ViewRuntime:
    if stage == 1:
        return runtime.with_fields(polka=quorum_reached(runtime.prevote_receipts, variant))
    if stage == 3:
        return runtime.with_fields(
            commit=quorum_reached(runtime.precommit_receipts, variant)
        )
    return runtime


def finish_view(runtime: ViewRuntime) -> KernelState:
    return runtime.persistent


def logical_identity(physical_node: str) -> str:
    if physical_node in ("T0", "T1"):
        return BYZANTINE_IDENTITY
    return physical_node


def deliver_late_certificate(
    state: KernelState,
    message: KernelMessage,
    variant: Variant,
) -> KernelState:
    if message.kind not in (MessageKind.COMMIT, MessageKind.FORGED_COMMIT):
        raise ValueError("only terminal commit evidence is delayable")
    index = _honest_index(message.receiver)
    valid = (message.signer_count or 0) >= QUORUM
    if not valid and variant.receiver_validation_omission != message.receiver:
        return state
    replicas = list(state.replicas)
    replicas[index] = _decide(replicas[index], int(message.value), message.view)
    return KernelState(tuple(replicas))
