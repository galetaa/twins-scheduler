from __future__ import annotations

from dataclasses import replace

from schedcheck.locking.model import (
    BYZANTINE_IDENTITY,
    HONEST_NODES,
    QUORUM,
    Justification,
    KernelMessage,
    KernelState,
    MessageKind,
    ReplicaState,
    Variant,
    ViewPlan,
    ViewRuntime,
)

STAGE_COUNT = 5
STAGE_NAMES: tuple[str, ...] = (
    "proposal",
    "prevote",
    "precommit-evidence",
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
    justification: Justification | None = None,
    signer_count: int | None = None,
    suffix: str = "",
) -> KernelMessage:
    uid = f"v{plan.view}-{kind.value.lower()}-{sender}-{receiver}{suffix}"
    return KernelMessage(
        uid=uid,
        view=plan.view,
        stage=stage,
        kind=kind,
        sender=sender,
        receiver=receiver,
        value=value,
        justification=justification,
        signer_count=signer_count,
    )


def initial_runtime(state: KernelState) -> ViewRuntime:
    return ViewRuntime(persistent=state)


def proposal_is_safe(
    replica: ReplicaState,
    proposal_value: int,
    justification: Justification | None,
    variant: Variant,
) -> bool:
    """Validate a single-decree locking proposal.

    A non-genesis justification is a proof-of-lock certificate. Correct code
    requires it to certify the proposed value. A conflicting proposal can only
    unlock a replica when the certificate view is strictly greater than the
    local lock view. The WRONG_QC_GUARD mutant drops the value check and uses a
    non-strict comparison.
    """

    if replica.decision is not None and replica.decision != proposal_value:
        return False

    if justification is not None:
        if variant.check_justify_value and justification.value != proposal_value:
            return False

    if replica.locked_value is None or replica.locked_value == proposal_value:
        return True

    if justification is None:
        return False

    if variant.strict_unlock_view:
        return justification.view > replica.locked_view
    return justification.view >= replica.locked_view


def quorum_reached(receipts: tuple[str, ...], variant: Variant) -> bool:
    if variant.count_unique_voters:
        voter_count = len(set(receipts))
    else:
        voter_count = len(receipts)
    # The Byzantine leader contributes its own logical vote. T0 and T1 share
    # one identity and therefore never count as two signers.
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
                justification=plan.justification,
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
        messages: list[KernelMessage] = []
        if runtime.prepare_qc:
            messages.extend(
                _message(
                    plan,
                    stage,
                    MessageKind.PRECOMMIT_QC,
                    plan.leader,
                    receiver,
                    value=plan.value,
                    signer_count=QUORUM,
                )
                for receiver in HONEST_NODES
            )
        if plan.emit_timeout_qc:
            messages.extend(
                _message(
                    plan,
                    stage,
                    MessageKind.TIMEOUT_QC,
                    plan.leader,
                    receiver,
                    value=plan.value,
                    signer_count=QUORUM,
                    suffix="-timeout",
                )
                for receiver in HONEST_NODES
            )
        return tuple(messages)

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
        messages = []
        if runtime.commit_qc:
            messages.extend(
                _message(
                    plan,
                    stage,
                    MessageKind.COMMIT_QC,
                    plan.leader,
                    receiver,
                    value=plan.value,
                    signer_count=QUORUM,
                )
                for receiver in HONEST_NODES
            )
        if plan.emit_forged_commit_qc:
            messages.extend(
                _message(
                    plan,
                    stage,
                    MessageKind.FORGED_COMMIT_QC,
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


def _lock_replica(replica: ReplicaState, value: int, view: int) -> ReplicaState:
    if view < replica.locked_view:
        return replica
    return replace(replica, locked_value=value, locked_view=view)


def _decide_replica(replica: ReplicaState, value: int, view: int) -> ReplicaState:
    if replica.decision is not None:
        return replica
    return ReplicaState(locked_value=value, locked_view=max(view, replica.locked_view), decision=value)


def deliver(
    runtime: ViewRuntime,
    message: KernelMessage,
    plan: ViewPlan,
    variant: Variant,
) -> ViewRuntime:
    if message.view != plan.view:
        raise ValueError("this bounded kernel only delivers same-view messages")

    if message.kind == MessageKind.PROPOSAL:
        index = _honest_index(message.receiver)
        replica = runtime.persistent.replicas[index]
        if proposal_is_safe(replica, plan.value, plan.justification, variant):
            return runtime.with_fields(
                accepted=_set_tuple_flag(runtime.accepted, index, True)
            )
        return runtime

    if message.kind == MessageKind.PREVOTE:
        if message.receiver != plan.leader:
            raise ValueError("prevote sent to non-leader")
        return runtime.with_fields(
            prevote_receipts=tuple(
                sorted(runtime.prevote_receipts + (message.sender,))
            )
        )

    if message.kind in (MessageKind.PRECOMMIT_QC, MessageKind.TIMEOUT_QC):
        index = _honest_index(message.receiver)
        if not runtime.accepted[index]:
            return runtime

        timeout_path = message.kind == MessageKind.TIMEOUT_QC
        if timeout_path and not variant.timeout_qc_acts_as_precommit:
            return runtime

        ready = _set_tuple_flag(runtime.ready_to_precommit, index, True)
        updated = runtime.with_fields(ready_to_precommit=ready)

        should_lock = (
            variant.lock_on_precommit_qc
            if not timeout_path
            else variant.timeout_path_updates_lock
        )
        if should_lock:
            replica = updated.persistent.replicas[index]
            updated = updated.replace_replica(
                index, _lock_replica(replica, plan.value, plan.view)
            )
        return updated

    if message.kind == MessageKind.PRECOMMIT:
        if message.receiver != plan.leader:
            raise ValueError("precommit sent to non-leader")
        return runtime.with_fields(
            precommit_receipts=tuple(
                sorted(runtime.precommit_receipts + (message.sender,))
            )
        )

    if message.kind in (MessageKind.COMMIT_QC, MessageKind.FORGED_COMMIT_QC):
        index = _honest_index(message.receiver)
        valid = (message.signer_count or 0) >= QUORUM
        if not valid and variant.receiver_validation_omission != message.receiver:
            return runtime
        replica = runtime.persistent.replicas[index]
        return runtime.replace_replica(
            index, _decide_replica(replica, plan.value, plan.view)
        )

    raise ValueError(f"unsupported message kind: {message.kind}")


def complete_stage(
    runtime: ViewRuntime,
    stage: int,
    variant: Variant,
) -> ViewRuntime:
    if stage == 1:
        return runtime.with_fields(
            prepare_qc=quorum_reached(runtime.prevote_receipts, variant)
        )
    if stage == 3:
        return runtime.with_fields(
            commit_qc=quorum_reached(runtime.precommit_receipts, variant)
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
    """Deliver a previously admitted certificate after a later view completes.

    The certificate retains its original value, view, signer count, and receiver.
    Only self-contained commit evidence is delayable in the Gate 4 temporal
    extension. Proposal and vote replay use separate rules.
    """
    if message.kind not in (
        MessageKind.COMMIT_QC,
        MessageKind.FORGED_COMMIT_QC,
    ):
        raise ValueError(f"message is not a delayable certificate: {message.kind}")
    index = _honest_index(message.receiver)
    valid = (message.signer_count or 0) >= QUORUM
    if not valid and variant.receiver_validation_omission != message.receiver:
        return state
    replica = state.replicas[index]
    replicas = list(state.replicas)
    replicas[index] = _decide_replica(
        replica,
        message.value if message.value is not None else 0,
        message.view,
    )
    return KernelState(tuple(replicas))
