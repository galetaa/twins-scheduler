"""Independent witness oracle for the Gate 4' locking kernel.

This module intentionally does not call ``kernel.deliver``, ``emit_stage`` or
``complete_stage``. It parses the serialized witness trace into a separate
mutable state representation and re-evaluates the protocol guards. The duplicate
implementation is small enough to audit and reduces common-mode errors between
the exact explorer and witness validation.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from schedcheck.locking.cases import ExperimentCase
from schedcheck.locking.model import HONEST_NODES, QUORUM, KernelWitness, Variant

_TOKEN = re.compile(
    r"^v(?P<view>\d+):s(?P<stage>\d+):[^:]+:"
    r"(?P<sender>[^-:]+)->(?P<receiver>[^:]+):"
    r"(?P<kind>[A-Z_]+)(?:\[(?P<payload>.*)\])?$"
)


@dataclass(slots=True)
class _Replica:
    locked_value: int | None = None
    locked_view: int = 0
    decision: int | None = None


@dataclass(frozen=True, slots=True)
class _Message:
    token: str
    view: int
    stage: int
    sender: str
    receiver: str
    kind: str
    value: int | None
    justify_view: int | None
    justify_value: int | None
    signers: int | None


def _parse(token: str) -> _Message:
    match = _TOKEN.match(token)
    if match is None:
        raise AssertionError(f"unparseable witness token: {token}")
    payload: dict[str, str] = {}
    raw_payload = match.group("payload")
    if raw_payload:
        for field in raw_payload.split(","):
            key, value = field.split("=", 1)
            payload[key] = value
    justify_view: int | None = None
    justify_value: int | None = None
    if "justify" in payload:
        left, right = payload["justify"].split(":", 1)
        justify_view, justify_value = int(left), int(right)
    return _Message(
        token=token,
        view=int(match.group("view")),
        stage=int(match.group("stage")),
        sender=match.group("sender"),
        receiver=match.group("receiver"),
        kind=match.group("kind"),
        value=int(payload["value"]) if "value" in payload else None,
        justify_view=justify_view,
        justify_value=justify_value,
        signers=int(payload["signers"]) if "signers" in payload else None,
    )


def _proposal_safe(
    replica: _Replica,
    value: int,
    justify_view: int | None,
    justify_value: int | None,
    variant: Variant,
) -> bool:
    if replica.decision is not None and replica.decision != value:
        return False
    if justify_view is not None and variant.check_justify_value:
        if justify_value != value:
            return False
    if replica.locked_value is None or replica.locked_value == value:
        return True
    if justify_view is None:
        return False
    return (
        justify_view > replica.locked_view
        if variant.strict_unlock_view
        else justify_view >= replica.locked_view
    )


def _quorum(receipts: list[str], variant: Variant) -> bool:
    count = len(set(receipts)) if variant.count_unique_voters else len(receipts)
    return 1 + count >= QUORUM


def _lock(replica: _Replica, value: int, view: int) -> None:
    if view >= replica.locked_view:
        replica.locked_value = value
        replica.locked_view = view


def _decide(replica: _Replica, value: int, view: int) -> None:
    if replica.decision is None:
        replica.decision = value
        replica.locked_value = value
        replica.locked_view = max(replica.locked_view, view)


def verify_witness(
    case: ExperimentCase,
    variant: Variant,
    witness: KernelWitness,
) -> tuple[int | None, ...]:
    plans = {plan.view: plan for plan in case.plans}
    replicas = {node: _Replica() for node in HONEST_NODES}
    pending: dict[str, _Message] = {}

    for view_trace in witness.views:
        plan = plans[view_trace.view]
        accepted = {node: False for node in HONEST_NODES}
        ready = {node: False for node in HONEST_NODES}
        prevotes: list[str] = []
        precommits: list[str] = []
        prepare_qc = False
        commit_qc = False
        current_deferred: dict[str, _Message] = {}

        for stage_trace in view_trace.stages:
            if stage_trace.stage not in range(5):
                raise AssertionError(f"invalid stage: {stage_trace.stage}")
            emitted = set(stage_trace.emitted)
            for token in stage_trace.delivered + stage_trace.deferred:
                if token not in emitted:
                    raise AssertionError(f"token was not emitted at stage: {token}")
            if set(stage_trace.delivered) & set(stage_trace.deferred):
                raise AssertionError("message cannot be delivered and deferred together")

            for token in stage_trace.delivered:
                message = _parse(token)
                if message.view != plan.view or message.stage != stage_trace.stage:
                    raise AssertionError(f"view/stage mismatch: {token}")
                value = message.value if message.value is not None else plan.value

                if message.kind == "PROPOSAL":
                    if _proposal_safe(
                        replicas[message.receiver],
                        value,
                        message.justify_view,
                        message.justify_value,
                        variant,
                    ):
                        accepted[message.receiver] = True
                elif message.kind == "PREVOTE":
                    prevotes.append(message.sender)
                elif message.kind in ("PRECOMMIT_QC", "TIMEOUT_QC"):
                    if message.kind == "PRECOMMIT_QC" and not prepare_qc:
                        raise AssertionError("precommit QC without a formed prepare quorum")
                    if not accepted[message.receiver]:
                        continue
                    timeout_path = message.kind == "TIMEOUT_QC"
                    if timeout_path and not variant.timeout_qc_acts_as_precommit:
                        continue
                    ready[message.receiver] = True
                    should_lock = (
                        variant.timeout_path_updates_lock
                        if timeout_path
                        else variant.lock_on_precommit_qc
                    )
                    if should_lock:
                        _lock(replicas[message.receiver], value, plan.view)
                elif message.kind == "PRECOMMIT":
                    precommits.append(message.sender)
                elif message.kind in ("COMMIT_QC", "FORGED_COMMIT_QC"):
                    if message.kind == "COMMIT_QC" and not commit_qc:
                        raise AssertionError("commit QC without a formed precommit quorum")
                    valid = (message.signers or 0) >= QUORUM
                    if not valid and variant.receiver_validation_omission != message.receiver:
                        continue
                    _decide(replicas[message.receiver], value, message.view)
                else:
                    raise AssertionError(f"unsupported oracle message kind: {message.kind}")

            for token in stage_trace.deferred:
                current_deferred[token] = _parse(token)

            if stage_trace.stage == 1:
                prepare_qc = _quorum(prevotes, variant)
            elif stage_trace.stage == 3:
                commit_qc = _quorum(precommits, variant)

        if set(view_trace.late_delivered) != set(pending):
            raise AssertionError(
                "a delay-1 trace must deliver exactly the previous view's pending set"
            )
        for token in view_trace.late_delivered:
            message = pending[token]
            valid = (message.signers or 0) >= QUORUM
            if not valid and variant.receiver_validation_omission != message.receiver:
                continue
            value = message.value if message.value is not None else 0
            _decide(replicas[message.receiver], value, message.view)
        pending = current_deferred

    observation = tuple(replicas[node].decision for node in HONEST_NODES)
    if observation != witness.observation:
        raise AssertionError(
            f"independent oracle mismatch: expected {witness.observation}, got {observation}"
        )
    return observation
