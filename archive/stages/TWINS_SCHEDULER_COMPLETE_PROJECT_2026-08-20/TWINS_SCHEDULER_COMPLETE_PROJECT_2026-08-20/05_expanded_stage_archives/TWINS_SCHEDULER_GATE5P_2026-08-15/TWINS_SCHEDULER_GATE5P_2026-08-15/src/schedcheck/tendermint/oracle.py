"""Independent mutable-state oracle for serialized Tendermint-style witnesses."""
from __future__ import annotations

from dataclasses import dataclass
import re

from schedcheck.tendermint.cases import ExperimentCase
from schedcheck.tendermint.model import HONEST_NODES, QUORUM, KernelWitness, Variant

_TOKEN = re.compile(
    r"^r(?P<view>\d+):s(?P<stage>\d+):[^:]+:"
    r"(?P<sender>[^-:]+)->(?P<receiver>[^:]+):"
    r"(?P<kind>[A-Z_]+)(?:\[(?P<payload>.*)\])?$"
)


@dataclass(slots=True)
class Replica:
    locked_value: int | None = None
    locked_round: int = 0
    valid_value: int | None = None
    valid_round: int = 0
    decision: int | None = None


@dataclass(frozen=True, slots=True)
class Message:
    token: str
    view: int
    stage: int
    sender: str
    receiver: str
    kind: str
    value: int | None
    proof_round: int | None
    proof_value: int | None
    signers: int | None


def parse(token: str) -> Message:
    match = _TOKEN.match(token)
    if match is None:
        raise AssertionError(f"unparseable token: {token}")
    payload: dict[str, str] = {}
    raw = match.group("payload")
    if raw:
        for field in raw.split(","):
            key, value = field.split("=", 1)
            payload[key] = value
    proof_round = proof_value = None
    if "valid_round" in payload:
        left, right = payload["valid_round"].split(":", 1)
        proof_round, proof_value = int(left), int(right)
    return Message(
        token=token,
        view=int(match.group("view")),
        stage=int(match.group("stage")),
        sender=match.group("sender"),
        receiver=match.group("receiver"),
        kind=match.group("kind"),
        value=int(payload["value"]) if "value" in payload else None,
        proof_round=proof_round,
        proof_value=proof_value,
        signers=int(payload["signers"]) if "signers" in payload else None,
    )


def proposal_safe(replica: Replica, value: int, proof_round: int | None, proof_value: int | None, variant: Variant) -> bool:
    if replica.decision is not None and replica.decision != value:
        return False
    if replica.locked_value is None or replica.locked_value == value:
        return True
    if proof_round is None:
        return False
    if variant.check_valid_round_value and proof_value != value:
        return False
    return proof_round > replica.locked_round if variant.strict_valid_round else proof_round >= replica.locked_round


def quorum(receipts: list[str], variant: Variant) -> bool:
    count = len(set(receipts)) if variant.count_unique_voters else len(receipts)
    return 1 + count >= QUORUM


def decide(replica: Replica, value: int, view: int) -> None:
    if replica.decision is not None:
        return
    replica.decision = value
    replica.locked_value = value
    replica.locked_round = max(replica.locked_round, view)
    replica.valid_value = value
    replica.valid_round = max(replica.valid_round, view)


def verify_witness(case: ExperimentCase, variant: Variant, witness: KernelWitness) -> tuple[int | None, ...]:
    plans = {plan.view: plan for plan in case.plans}
    replicas = {node: Replica() for node in HONEST_NODES}
    pending: dict[str, Message] = {}

    for view_trace in witness.views:
        plan = plans[view_trace.view]
        accepted = {node: False for node in HONEST_NODES}
        ready = {node: False for node in HONEST_NODES}
        prevotes: list[str] = []
        precommits: list[str] = []
        polka = False
        commit = False
        current_deferred: dict[str, Message] = {}

        for stage_trace in view_trace.stages:
            emitted = set(stage_trace.emitted)
            for token in stage_trace.delivered + stage_trace.deferred:
                if token not in emitted:
                    raise AssertionError(f"token not emitted: {token}")
            for token in stage_trace.delivered:
                msg = parse(token)
                value = msg.value if msg.value is not None else plan.value
                if msg.kind == "PROPOSAL":
                    replica = replicas[msg.receiver]
                    if proposal_safe(replica, value, msg.proof_round, msg.proof_value, variant):
                        accepted[msg.receiver] = True
                elif msg.kind == "PREVOTE":
                    prevotes.append(msg.sender)
                elif msg.kind == "POLKA":
                    if not polka:
                        raise AssertionError("POLKA delivered without formed prevote quorum")
                    if not accepted[msg.receiver]:
                        continue
                    ready[msg.receiver] = True
                    replica = replicas[msg.receiver]
                    replica.valid_value = value
                    replica.valid_round = plan.view
                    if variant.lock_on_polka and plan.view >= replica.locked_round:
                        replica.locked_value = value
                        replica.locked_round = plan.view
                elif msg.kind == "PRECOMMIT":
                    precommits.append(msg.sender)
                elif msg.kind in ("COMMIT", "FORGED_COMMIT"):
                    if msg.kind == "COMMIT" and not commit:
                        raise AssertionError("COMMIT delivered without formed precommit quorum")
                    valid = (msg.signers or 0) >= QUORUM
                    if not valid and variant.receiver_validation_omission != msg.receiver:
                        continue
                    decide(replicas[msg.receiver], value, msg.view)
                else:
                    raise AssertionError(f"unsupported kind: {msg.kind}")
            for token in stage_trace.deferred:
                current_deferred[token] = parse(token)
            if stage_trace.stage == 1:
                polka = quorum(prevotes, variant)
            elif stage_trace.stage == 3:
                commit = quorum(precommits, variant)

        if set(view_trace.late_delivered) != set(pending):
            raise AssertionError("late deliveries must equal prior pending set")
        for token in view_trace.late_delivered:
            msg = pending[token]
            valid = (msg.signers or 0) >= QUORUM
            if not valid and variant.receiver_validation_omission != msg.receiver:
                continue
            decide(replicas[msg.receiver], msg.value if msg.value is not None else 0, msg.view)
        pending = current_deferred

    observation = tuple(replicas[node].decision for node in HONEST_NODES)
    if observation != witness.observation:
        raise AssertionError(f"oracle mismatch: expected {witness.observation}, got {observation}")
    return observation
