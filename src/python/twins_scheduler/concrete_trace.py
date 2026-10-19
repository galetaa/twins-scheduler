"""A four-validator, authenticated, rule-level Tendermint trace.

This module is independent of ``bounded`` and ``event_loop``.  Quorums are
sets of votes actually signed, emitted, and delivered in this execution.
There are no synthetic POLKA/COMMIT network messages or preloaded base votes.

The deliberately small model follows the published proposal, prevote,
precommit, mixed-vote timeout, valid-block, and commit rules exercised by the
trace.  It is not an execution of the CometBFT client.  Authentication uses
deterministic test-only HMAC tags, not production validator keys or Ed25519.
Only P's round-0 lock assignment is optionally omitted; its round-1 lock
update and every A/C update remain unmutated.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import hmac
import json
from typing import Any, Literal


Validator = Literal["A", "P", "C", "B"]
VoteType = Literal["PREVOTE", "PRECOMMIT"]
GRAMMARS = ("G_T_PHASE_SPECIFIC", "G_D_EDGE_OFF", "G_D_EDGE_ON")
VARIANTS = ("BASELINE", "MISSING_LOCK_UPDATE")
REPAIR_TIMINGS = (
    "before_round_1",
    "after_pivot_prevote",
    "after_pivot_precommit",
)
VALIDATORS = ("A", "P", "C", "B")
CORRECT = ("A", "P", "C")
QUORUM = 3
SOURCE_COMMIT = "49b82838fcca442b2445f76605c101609ed04130"
SOURCE_URL = f"https://github.com/cometbft/cometbft/blob/{SOURCE_COMMIT}/consensus/state.go"
FIXED_ACTIVE_EDGES = {
    0: frozenset({("B", "A"), ("A", "P"), ("A", "C"),
                  ("P", "A"), ("P", "C"), ("C", "P")}),
    1: frozenset({("B", "P"), ("B", "C"), ("C", "P"), ("P", "C")}),
}


class IllegalAction(ValueError):
    """An action lacks its protocol guard or its emitted envelope."""


def _value_label(value: int | None) -> str:
    return "nil" if value is None else str(value)


@dataclass(frozen=True, slots=True)
class SignedMessage:
    id: str
    signer: str
    height: int
    round: int
    kind: str
    value: int | None
    valid_round: int = -1
    signature: str = ""

    def sign_bytes(self) -> bytes:
        data = asdict(self)
        data.pop("signature")
        return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()


@dataclass(slots=True)
class Envelope:
    id: str
    sender: str
    receiver: str
    message_id: str
    emitted_at: int
    status: str = "BUFFERED"


@dataclass(slots=True)
class Replica:
    name: str
    height: int = 1
    round: int = 0
    step: str = "PROPOSE"
    locked_value: int | None = None
    locked_round: int = -1
    valid_value: int | None = None
    valid_round: int = -1
    proposal_id: str | None = None
    proposal_block: int | None = None
    known_blocks: set[int] = field(default_factory=set)
    commit_value: int | None = None
    commit_round: int | None = None
    committed: int | None = None
    # Histories survive height advancement for independent audit.
    signed_votes: dict[tuple[int, int, str], str] = field(default_factory=dict)
    received_votes: dict[tuple[int, int, str, str], str] = field(default_factory=dict)
    received_messages: set[str] = field(default_factory=set)
    timers: set[tuple[int, str]] = field(default_factory=lambda: {(0, "PROPOSE")})


class ConcreteTrace:
    """Small guarded transition system with an explicit network buffer.

    Correct votes can only be emitted by guarded transitions.  B is the one
    explicitly Byzantine identity: its votes are authenticated but need not
    have an honest justification.  The supplied trace does not require B to
    double-sign within a height/round/vote-type slot.
    """

    def __init__(
        self,
        grammar: str = "G_T_PHASE_SPECIFIC",
        variant: str = "MISSING_LOCK_UPDATE",
        *,
        repair_timing: str = "before_round_1",
        proposers: tuple[str, str] = ("B", "C"),
        round1_b_prevote_route: str = "direct",
    ) -> None:
        if grammar not in GRAMMARS or variant not in VARIANTS:
            raise ValueError("unknown scheduler grammar or mutation")
        if repair_timing not in REPAIR_TIMINGS:
            raise ValueError("unknown repair timing")
        if any(name not in VALIDATORS for name in proposers):
            raise ValueError("unknown designated proposer")
        if round1_b_prevote_route not in ("direct", "via_C"):
            raise ValueError("unknown round-1 vote route")
        self.grammar, self.variant, self.repair_timing = grammar, variant, repair_timing
        self.proposers = proposers
        self.round1_b_prevote_route = round1_b_prevote_route
        self.replicas = {name: Replica(name) for name in VALIDATORS}
        self.replicas["B"].step = "BYZANTINE"
        self.replicas["B"].timers.clear()
        self.messages: dict[str, SignedMessage] = {}
        self.envelopes: dict[str, Envelope] = {}
        self.log: list[dict[str, Any]] = []
        self.certificates: list[dict[str, Any]] = []
        self.milestones: list[dict[str, Any]] = []
        self._certificate_keys: set[tuple[str, int, str, int | None]] = set()
        self._keys = {
            name: hashlib.sha256(f"concrete-trace-test-key:{name}".encode()).digest()
            for name in VALIDATORS
        }
        self._record("INITIAL", detail="height 1, round 0; empty vote sets and locks")

    def _snapshot(self) -> dict[str, Any]:
        return {
            name: {
                "height": state.height,
                "round": state.round,
                "step": state.step,
                "locked_value": state.locked_value,
                "locked_round": state.locked_round,
                "valid_value": state.valid_value,
                "valid_round": state.valid_round,
                "proposal_id": state.proposal_id,
                "proposal_block": state.proposal_block,
                "known_blocks": sorted(state.known_blocks),
                "commit_value": state.commit_value,
                "commit_round": state.commit_round,
                "committed": state.committed,
                "signed_votes": list(state.signed_votes.values()),
                "received_votes": list(state.received_votes.values()),
                "timers": [list(timer) for timer in sorted(state.timers)],
            }
            for name, state in self.replicas.items()
        }

    def _record(self, action: str, **details: Any) -> None:
        self.log.append(
            {"index": len(self.log), "action": action, **details, "states": self._snapshot()}
        )

    def milestone(self, name: str) -> None:
        self.milestones.append(
            {
                "name": name,
                "after_event": len(self.log) - 1,
                "states": self._snapshot(),
                "buffered": [key for key, envelope in self.envelopes.items()
                             if envelope.status == "BUFFERED"],
            }
        )

    def _authenticate(self, message: SignedMessage) -> bool:
        if message.signer not in self._keys:
            return False
        expected = hmac.new(self._keys[message.signer], message.sign_bytes(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, message.signature)

    def _new_signed(
        self, signer: str, round_: int, kind: str, value: int | None, valid_round: int = -1
    ) -> SignedMessage:
        key = f"{signer}:H1:R{round_}:{kind}:{_value_label(value)}:VR{valid_round}"
        unsigned = SignedMessage(key, signer, 1, round_, kind, value, valid_round)
        message = SignedMessage(
            **{**asdict(unsigned), "signature": hmac.new(
                self._keys[signer], unsigned.sign_bytes(), hashlib.sha256
            ).hexdigest()}
        )
        if key in self.messages:
            raise IllegalAction("message was already signed; relay its existing record")
        self.messages[key] = message
        self.replicas[signer].received_messages.add(key)
        return message

    def _emit_envelope(self, sender: str, receiver: str, message: SignedMessage) -> str:
        if sender not in VALIDATORS or receiver not in VALIDATORS:
            raise IllegalAction("unknown transport endpoint")
        if message.id not in self.messages or not self._authenticate(message):
            raise IllegalAction("an envelope must carry an already emitted authentic message")
        if message.id not in self.replicas[sender].received_messages:
            raise IllegalAction("a relay cannot forward a message it does not possess")
        key = f"tx{len(self.envelopes) + 1:04d}"
        self.envelopes[key] = Envelope(key, sender, receiver, message.id, len(self.log))
        self._record("EMIT", envelope=key, sender=sender, receiver=receiver, message=message.id)
        return key

    def _multicast(self, message: SignedMessage, recipients: tuple[str, ...]) -> None:
        local: str | None = None
        for receiver in recipients:
            key = self._emit_envelope(message.signer, receiver, message)
            if receiver == message.signer:
                local = key
        # Self-votes are explicitly emitted before local delivery and count once.
        if local is not None:
            self.deliver(local)

    def _live(self, name: str) -> Replica:
        if name not in CORRECT:
            raise IllegalAction("a correct transition needs a non-Byzantine validator")
        state = self.replicas[name]
        if state.height != 1 or state.step == "COMMIT" or state.committed is not None:
            raise IllegalAction("validator already entered commit or advanced height")
        return state

    def byzantine_vote(self, round_: int, kind: VoteType, value: int | None) -> str:
        if kind not in ("PREVOTE", "PRECOMMIT") or round_ not in (0, 1):
            raise IllegalAction("unsupported Byzantine vote")
        state = self.replicas["B"]
        slot = (1, round_, kind)
        if slot in state.signed_votes:
            raise IllegalAction("this bounded trace uses one B vote per slot")
        message = self._new_signed("B", round_, kind, value)
        state.round = round_
        state.signed_votes[slot] = message.id
        self._record("SIGN", actor="B", message=message.id,
                     rule="authenticated Byzantine action; honest vote guard exempt")
        self._multicast(message, CORRECT)
        return message.id

    def propose(self, name: str, candidate: int, recipients: tuple[str, ...]) -> str:
        state = self.replicas[name]
        if state.round not in (0, 1) or self.proposers[state.round] != name:
            raise IllegalAction("only the designated proposer can produce an accepted proposal")
        if name != "B":
            self._live(name)
            if state.step != "PROPOSE":
                raise IllegalAction("correct proposal must be made at the propose step")
            value = state.valid_value if state.valid_value is not None else candidate
            valid_round = state.valid_round
        else:
            value, valid_round = candidate, -1
        if value not in (0, 1):
            raise IllegalAction("only the two fixed valid blocks belong to the bound")
        message = self._new_signed(name, state.round, "PROPOSAL", value, valid_round)
        state.known_blocks.add(value)
        self._record("SIGN", actor=name, message=message.id,
                     rule="designated proposer; reuse valid block if present",
                     requested_candidate=candidate, actual_value=value, valid_round=valid_round)
        self._multicast(message, recipients)
        return message.id

    def relay(self, sender: str, receiver: str, message_id: str) -> str:
        if message_id not in self.messages:
            raise IllegalAction("cannot relay an unemitted message")
        return self._emit_envelope(sender, receiver, self.messages[message_id])

    def send_block(self, sender: str, receiver: str, value: int) -> str:
        if value not in self.replicas[sender].known_blocks:
            raise IllegalAction("cannot send a block not locally known")
        message = self._new_signed(sender, 0, "BLOCK", value)
        self._record("BLOCK_SEND", actor=sender, message=message.id,
                     rule="forward a locally received, validated block")
        return self._emit_envelope(sender, receiver, message)

    def _admitted(self, envelope: Envelope, message: SignedMessage) -> bool:
        controlled = (envelope.sender, envelope.receiver, message.height, message.round) == (
            "B", "P", 1, 0
        )
        if not controlled:
            return (envelope.sender == envelope.receiver
                    or (envelope.sender, envelope.receiver) in FIXED_ACTIVE_EDGES[message.round])
        if self.grammar == "G_D_EDGE_OFF":
            return False
        if self.grammar == "G_D_EDGE_ON":
            return True
        return message.kind != "PRECOMMIT"

    def deliver(self, envelope_id: str) -> bool:
        if envelope_id not in self.envelopes:
            raise IllegalAction("no synthesis: the envelope was never emitted")
        envelope = self.envelopes[envelope_id]
        if envelope.status != "BUFFERED":
            raise IllegalAction("an envelope instance can be resolved only once")
        message = self.messages[envelope.message_id]
        if not self._authenticate(message):
            raise IllegalAction("message authentication failed")
        if not self._admitted(envelope, message):
            envelope.status = "DROPPED"
            self._record("DROP", envelope=envelope_id, message=message.id,
                         rule="controlled transport edge admission")
            return False
        envelope.status = "DELIVERED"
        self._record("DELIVER", envelope=envelope_id, message=message.id,
                     sender=envelope.sender, receiver=envelope.receiver,
                     rule="authentic, already emitted, buffered, admitted, once-only")
        self._receive(envelope.receiver, message)
        return True

    def vote_envelope(self, sender: str, receiver: str, round_: int, kind: VoteType) -> str | None:
        for key, envelope in self.envelopes.items():
            message = self.messages[envelope.message_id]
            if (envelope.status == "BUFFERED" and envelope.sender == sender
                    and envelope.receiver == receiver and message.signer == sender
                    and message.round == round_ and message.kind == kind):
                return key
        return None

    def deliver_vote(self, sender: str, receiver: str, round_: int, kind: VoteType) -> bool:
        key = self.vote_envelope(sender, receiver, round_, kind)
        if key is None:
            raise IllegalAction("requested vote envelope is not buffered")
        return self.deliver(key)

    def opportunity(self, sender: str, receiver: str, round_: int, kind: VoteType) -> None:
        """Fixed delivery opportunity; an unproduced vote is never synthesized."""
        key = self.vote_envelope(sender, receiver, round_, kind)
        if key is None:
            self._record("NO_EMITTED_VOTE", sender=sender, receiver=receiver,
                         round=round_, kind=kind,
                         detail="fixed delivery opportunity has no generated envelope")
        else:
            self.deliver(key)

    def _votes(self, name: str, round_: int, kind: str, value: Any = ...) -> list[SignedMessage]:
        state = self.replicas[name]
        return [
            self.messages[key] for (height, round_number, vote_kind, _), key in state.received_votes.items()
            if height == 1 and round_number == round_ and vote_kind == kind
            and (value is ... or self.messages[key].value == value)
        ]

    def _majority(self, name: str, round_: int, kind: str) -> tuple[bool, int | None]:
        for value in (0, 1, None):
            if len(self._votes(name, round_, kind, value)) >= QUORUM:
                return True, value
        return False, None

    def _certificate(self, name: str, round_: int, kind: str, value: int | None) -> dict[str, Any]:
        votes = self._votes(name, round_, kind, value)
        if len({message.signer for message in votes}) < QUORUM:
            raise IllegalAction("certificate lacks three distinct delivered signers")
        certificate = {
            "receiver": name, "height": 1, "round": round_, "kind": kind,
            "value": value, "signers": sorted(message.signer for message in votes),
            "vote_ids": sorted(message.id for message in votes), "threshold": QUORUM,
        }
        key = (name, round_, kind, value)
        if key not in self._certificate_keys:
            self._certificate_keys.add(key)
            certificate["formed_at"] = len(self.log)
            self.certificates.append(certificate)
            self._record("LOCAL_CERTIFICATE", **certificate)
        return certificate

    def _receive(self, name: str, message: SignedMessage) -> None:
        state = self.replicas[name]
        if name == "B":
            state.received_messages.add(message.id)
            self._record("BYZANTINE_RECEIVE", actor=name, message=message.id)
            return
        if state.height != message.height:
            self._record("IGNORE_HEIGHT", actor=name, message=message.id)
            return
        state.received_messages.add(message.id)
        if message.kind == "BLOCK":
            if message.value not in (0, 1):
                raise IllegalAction("invalid block")
            state.known_blocks.add(message.value)
            if state.step == "COMMIT" and message.value == state.commit_value:
                state.proposal_block = message.value
                self._record("BLOCK_RECEIVED", actor=name, message=message.id)
                self._finalize_commit(name)
            return
        if state.step == "COMMIT":
            self._record("IGNORE_COMMIT_STEP", actor=name, message=message.id)
            return
        if message.kind == "PROPOSAL":
            if message.round != state.round:
                self._record("IGNORE_PROPOSAL_ROUND", actor=name, message=message.id)
                return
            if message.signer != self.proposers[state.round]:
                raise IllegalAction("proposal was not signed by the designated proposer")
            if not (-1 <= message.valid_round < message.round):
                raise IllegalAction("invalid proposal valid round")
            if state.proposal_id is not None:
                self._record("DUPLICATE_PROPOSAL", actor=name, message=message.id)
                return
            state.proposal_id = message.id
            state.proposal_block = message.value
            if message.value is not None:
                state.known_blocks.add(message.value)
            self._record("ACCEPT_PROPOSAL", actor=name, message=message.id,
                         rule="designated signature, current round, valid complete block")
            if self._proposal_complete(name) and state.step == "PROPOSE":
                self._enter_prevote(name)
            return
        if message.kind not in ("PREVOTE", "PRECOMMIT"):
            raise IllegalAction("unknown message type")
        slot = (message.height, message.round, message.kind, message.signer)
        if slot in state.received_votes:
            previous = state.received_votes[slot]
            self._record("DUPLICATE_VOTE" if previous == message.id else "REJECT_EQUIVOCATION",
                         actor=name, message=message.id,
                         rule="a signer contributes at most once per vote slot")
            return
        state.received_votes[slot] = message.id
        self._record("ACCEPT_VOTE", actor=name, message=message.id,
                     signers=sorted(v.signer for v in self._votes(name, message.round, message.kind)))
        self._after_vote(name, message.round, message.kind)

    def _proposal_complete(self, name: str) -> bool:
        state = self.replicas[name]
        if state.proposal_id is None or state.proposal_block is None:
            return False
        proposal = self.messages[state.proposal_id]
        # isProposalComplete checks a majority at the advertised POLRound;
        # the block identity is not an extra guard in that source function.
        return proposal.valid_round == -1 or self._majority(name, proposal.valid_round, "PREVOTE")[0]

    def _sign_correct_vote(self, name: str, kind: VoteType, value: int | None, rule: str) -> None:
        state = self._live(name)
        slot = (state.height, state.round, kind)
        if slot in state.signed_votes:
            raise IllegalAction("correct identity cannot sign a second vote in one slot")
        if state.step != kind:
            raise IllegalAction("correct vote must match the current protocol step")
        message = self._new_signed(name, state.round, kind, value)
        state.signed_votes[slot] = message.id
        self._record("SIGN", actor=name, message=message.id, rule=rule)
        self._multicast(message, VALIDATORS)

    def _enter_prevote(self, name: str) -> None:
        state = self._live(name)
        if state.step != "PROPOSE":
            raise IllegalAction("prevote entry requires the propose step")
        state.step = "PREVOTE"
        state.timers.discard((state.round, "PROPOSE"))
        if state.locked_value is not None:
            value, rule = state.locked_value, "prevote persistent locked block"
        elif state.proposal_block is not None:
            value, rule = state.proposal_block, "prevote received valid proposal block while unlocked"
        else:
            value, rule = None, "proposal timeout without complete proposal: prevote nil"
        self._sign_correct_vote(name, "PREVOTE", value, rule)

    def _enter_precommit(self, name: str, *, timeout_kind: str | None = None) -> None:
        state = self._live(name)
        if state.step not in ("PROPOSE", "PREVOTE"):
            raise IllegalAction("already entered precommit")
        has_polka, value = self._majority(name, state.round, "PREVOTE")
        if not has_polka and timeout_kind is None:
            raise IllegalAction("non-timeout precommit entry requires a PoLC")
        if not has_polka:
            required_kind = "PREVOTE" if timeout_kind == "PREVOTE" else "PRECOMMIT"
            if len(self._votes(name, state.round, required_kind)) < QUORUM:
                raise IllegalAction("timeout precommit requires a received any-vote quorum")
            value, rule = None, "expired quorum-enabled timeout without PoLC: precommit nil"
        elif value is None:
            state.locked_value, state.locked_round = None, -1
            rule = "nil PoLC: unlock and precommit nil"
        elif value == state.proposal_block or value == state.locked_value:
            self._certificate(name, state.round, "PREVOTE", value)
            if name == "P" and state.round == 0 and self.variant == "MISSING_LOCK_UPDATE":
                rule = "PoLC: omit only P round-0 lock assignment; still sign precommit"
            else:
                state.locked_value, state.locked_round = value, state.round
                rule = "PoLC: persist locked value and round before signing precommit"
        else:
            state.locked_value, state.locked_round = None, -1
            value, rule = None, "PoLC for unavailable block: unlock and precommit nil"
        state.step = "PRECOMMIT"
        state.timers.discard((state.round, "PROPOSE"))
        state.timers.discard((state.round, "PREVOTE"))
        self._record("PRECOMMIT_ENTRY", actor=name, value=value, rule=rule)
        self._sign_correct_vote(name, "PRECOMMIT", value, rule)

    def _after_vote(self, name: str, round_: int, kind: str) -> None:
        state = self.replicas[name]
        has_majority, value = self._majority(name, round_, kind)
        any_count = len(self._votes(name, round_, kind))
        if round_ > state.round:
            if any_count >= QUORUM:
                raise IllegalAction("future-round skip is outside this two-round trace's transition subset")
            return
        if kind == "PRECOMMIT":
            if has_majority and round_ == state.round and state.step in ("PROPOSE", "PREVOTE"):
                raise IllegalAction("precommit-majority auto entry before own precommit is outside this trace subset")
            if has_majority and value is not None:
                self._start_commit(name, round_, value)
            elif round_ == state.round and any_count >= QUORUM:
                timer = (round_, "PRECOMMIT")
                if timer not in state.timers:
                    state.timers.add(timer)
                    self._record("ARM_TIMEOUT", actor=name, timer="PRECOMMIT", round=round_,
                                 evidence=[v.id for v in self._votes(name, round_, kind)],
                                 rule="three distinct precommits, possibly for mixed values")
            return
        if has_majority:
            self._certificate(name, round_, kind, value)
            if (state.locked_value is not None and state.locked_round < round_ <= state.round
                    and state.locked_value != value):
                state.locked_value, state.locked_round = None, -1
                self._record("UNLOCK", actor=name, rule="strictly newer PoLC for another value")
            if (round_ == state.round and value is not None and state.valid_round < round_
                    and state.proposal_block == value):
                state.valid_value, state.valid_round = value, round_
                self._record("VALID_BLOCK", actor=name, value=value, round=round_,
                             rule="PoLC updates ValidBlock even when lock assignment is mutated")
        if round_ != state.round:
            if (state.step == "PROPOSE" and state.proposal_id is not None
                    and self.messages[state.proposal_id].valid_round == round_
                    and self._proposal_complete(name)):
                raise IllegalAction("late old-round proposal POL completion is outside this trace subset")
            return
        if state.step == "PROPOSE" and self._proposal_complete(name):
            self._enter_prevote(name)
        if state.step == "PREVOTE":
            if has_majority and (value is None or self._proposal_complete(name)):
                self._enter_precommit(name)
            elif any_count >= QUORUM:
                timer = (round_, "PREVOTE")
                if timer not in state.timers:
                    state.timers.add(timer)
                    self._record("ARM_TIMEOUT", actor=name, timer="PREVOTE", round=round_,
                                 evidence=[v.id for v in self._votes(name, round_, kind)],
                                 rule="three distinct prevotes, possibly for mixed values")

    def timeout(self, name: str, kind: str) -> None:
        state = self._live(name)
        timer = (state.round, kind)
        if timer not in state.timers:
            raise IllegalAction("timeout was not armed by its protocol guard")
        if kind == "PROPOSE" and state.step != "PROPOSE":
            raise IllegalAction("stale propose timeout")
        if kind == "PREVOTE" and state.step != "PREVOTE":
            raise IllegalAction("stale prevote timeout")
        if kind not in ("PROPOSE", "PREVOTE", "PRECOMMIT"):
            raise IllegalAction("unknown timeout")
        if kind != "PROPOSE" and len(self._votes(name, state.round, kind)) < QUORUM:
            raise IllegalAction("timeout lacks three distinct delivered votes")
        state.timers.remove(timer)
        self._record("TIMEOUT", actor=name, timer=kind, round=state.round,
                     rule="previously armed timeout expires")
        if kind == "PROPOSE":
            self._enter_prevote(name)
        elif kind == "PREVOTE":
            self._enter_precommit(name, timeout_kind=kind)
        else:
            if state.step in ("PROPOSE", "PREVOTE"):
                self._enter_precommit(name, timeout_kind=kind)
            self._enter_next_round(name)

    def timeout_opportunity(self, name: str, kind: str) -> None:
        state = self.replicas[name]
        if state.height == 1 and state.step != "COMMIT" and (state.round, kind) in state.timers:
            self.timeout(name, kind)
        else:
            self._record("NO_ENABLED_TIMEOUT", actor=name, timer=kind,
                         detail="fixed timeout opportunity is disabled in this execution")

    def _enter_next_round(self, name: str) -> None:
        state = self._live(name)
        if state.round != 0:
            raise IllegalAction("only the round-0 to round-1 timeout belongs to this trace")
        if len(self._votes(name, 0, "PRECOMMIT")) < QUORUM:
            raise IllegalAction("round advance lacks an any-precommit quorum")
        state.round = 1
        state.step = "PROPOSE"
        state.proposal_id, state.proposal_block = None, None
        state.timers = {(1, "PROPOSE")}
        self._record("ROUND_ADVANCE", actor=name, rule="expired any-precommit-quorum timeout",
                     evidence=[v.id for v in self._votes(name, 0, "PRECOMMIT")])

    def _start_commit(self, name: str, round_: int, value: int) -> None:
        state = self._live(name)
        certificate = self._certificate(name, round_, "PRECOMMIT", value)
        state.commit_value, state.commit_round, state.step = value, round_, "COMMIT"
        state.timers.clear()
        if state.locked_value == value:
            state.proposal_block = state.locked_value
        if state.proposal_block != value:
            # Match enterCommit: a previous round's block must be fetched again
            # when neither the current proposal nor the locked block matches.
            state.proposal_block = None
        self._record("COMMIT_ENTRY", actor=name, value=value, round=round_,
                     evidence=certificate["vote_ids"],
                     rule="three matching precommits; stop signing at this height")
        self._finalize_commit(name)

    def _finalize_commit(self, name: str) -> None:
        state = self.replicas[name]
        if state.step != "COMMIT":
            raise IllegalAction("finalization needs the commit step")
        if state.proposal_block != state.commit_value:
            self._record("WAIT_COMMIT_BLOCK", actor=name, value=state.commit_value,
                         rule="commit vote quorum does not synthesize missing block data")
            return
        if state.committed is not None:
            raise IllegalAction("decision is irreversible")
        state.committed = state.commit_value
        state.height, state.round, state.step = 2, 0, "NEW_HEIGHT"
        state.locked_value, state.locked_round = None, -1
        state.valid_value, state.valid_round = None, -1
        state.proposal_id, state.proposal_block = None, None
        self._record("DECIDE", actor=name, value=state.committed,
                     decision_round=state.commit_round,
                     rule="matching precommit quorum and received complete block; advance height")

    def audit(self) -> dict[str, bool]:
        delivered = [row for row in self.log if row["action"] == "DELIVER"]
        emitted_before_delivery = all(
            row["envelope"] in self.envelopes
            and self.envelopes[row["envelope"]].emitted_at < row["index"]
            for row in delivered
        )
        once_only = len(delivered) == len({row["envelope"] for row in delivered})
        authenticated = all(self._authenticate(message) for message in self.messages.values())
        other_edge_outcomes: dict[tuple[int, int, str, str], set[bool]] = {}
        for envelope in self.envelopes.values():
            message = self.messages[envelope.message_id]
            edge = (message.height, message.round, envelope.sender, envelope.receiver)
            if edge == (1, 0, "B", "P"):
                continue
            other_edge_outcomes.setdefault(edge, set()).add(envelope.status == "DELIVERED")
        other_edges_uniform = all(len(outcomes) == 1 for outcomes in other_edge_outcomes.values())
        accepted_at = {
            (row["actor"], row["message"]): row["index"]
            for row in self.log if row["action"] == "ACCEPT_VOTE"
        }
        certificates_valid = True
        certificates_received = True
        for certificate in self.certificates:
            votes = [self.messages[key] for key in certificate["vote_ids"]]
            certificates_valid &= (
                len({vote.signer for vote in votes}) >= QUORUM
                and sorted(vote.signer for vote in votes) == certificate["signers"]
                and all((vote.height, vote.round, vote.kind, vote.value) == (
                    certificate["height"], certificate["round"], certificate["kind"], certificate["value"]
                ) for vote in votes)
            )
            certificates_received &= all(
                (certificate["receiver"], vote.id) in accepted_at
                and accepted_at[(certificate["receiver"], vote.id)] < certificate["formed_at"]
                for vote in votes
            )
        correct_single_vote = all(
            len([message for message in self.messages.values() if message.signer == name
                 and message.kind in ("PREVOTE", "PRECOMMIT")]) == len(state.signed_votes)
            for name, state in self.replicas.items() if name in CORRECT
        )
        decisions_justified = all(
            any(certificate["receiver"] == name and certificate["kind"] == "PRECOMMIT"
                and certificate["value"] == state.committed for certificate in self.certificates)
            for name, state in self.replicas.items() if state.committed is not None
        )
        correct_vote_guards = True
        timers_guarded = True
        for row in self.log:
            if row["action"] == "ARM_TIMEOUT":
                evidence = [self.messages[key] for key in row["evidence"]]
                timers_guarded &= (
                    len({vote.signer for vote in evidence}) >= QUORUM
                    and all(vote.kind == row["timer"] and vote.round == row["round"]
                            and accepted_at.get((row["actor"], vote.id), len(self.log)) < row["index"]
                            for vote in evidence)
                )
            if row["action"] != "SIGN" or row["actor"] not in CORRECT:
                continue
            vote = self.messages[row["message"]]
            if vote.kind not in ("PREVOTE", "PRECOMMIT"):
                continue
            state = row["states"][row["actor"]]
            correct_vote_guards &= state["height"] == vote.height and state["round"] == vote.round
            correct_vote_guards &= state["step"] == vote.kind and state["committed"] is None
            if vote.kind == "PREVOTE":
                expected = (state["locked_value"] if state["locked_value"] is not None
                            else state["proposal_block"])
                correct_vote_guards &= vote.value == expected
            elif vote.value is not None:
                prior_prevotes = [self.messages[key] for key in state["received_votes"]]
                support = [previous for previous in prior_prevotes
                           if previous.kind == "PREVOTE" and previous.round == vote.round
                           and previous.value == vote.value]
                correct_vote_guards &= len({previous.signer for previous in support}) >= QUORUM
                correct_vote_guards &= all(
                    accepted_at.get((row["actor"], previous.id), len(self.log)) < row["index"]
                    for previous in support
                )
                if row["actor"] != "P" or vote.round != 0 or self.variant == "BASELINE":
                    correct_vote_guards &= (state["locked_value"], state["locked_round"]) == (
                        vote.value, vote.round
                    )
            else:
                received = [self.messages[key] for key in state["received_votes"]]
                prevotes = [previous for previous in received
                            if previous.kind == "PREVOTE" and previous.round == vote.round]
                precommits = [previous for previous in received
                              if previous.kind == "PRECOMMIT" and previous.round == vote.round]
                nil_polka = len({previous.signer for previous in prevotes if previous.value is None}) >= QUORUM
                prior_timeouts = {previous["timer"] for previous in self.log[:row["index"]]
                                  if previous["action"] == "TIMEOUT" and previous["actor"] == row["actor"]
                                  and previous["round"] == vote.round}
                quorum_timeout = (
                    "PREVOTE" in prior_timeouts and len({previous.signer for previous in prevotes}) >= QUORUM
                ) or (
                    "PRECOMMIT" in prior_timeouts and len({previous.signer for previous in precommits}) >= QUORUM
                )
                unavailable_polka = any(
                    len({previous.signer for previous in prevotes if previous.value == value}) >= QUORUM
                    and state["proposal_block"] != value and state["locked_value"] != value
                    for value in (0, 1)
                )
                correct_vote_guards &= nil_polka or quorum_timeout or unavailable_polka
        return {
            "every_delivery_has_prior_emission": emitted_before_delivery,
            "once_only_envelope_delivery": once_only,
            "all_messages_authenticate": authenticated,
            "all_other_transport_edges_have_type_uniform_delivery": other_edges_uniform,
            "all_certificates_have_distinct_actual_signed_votes": bool(certificates_valid),
            "certificate_votes_received_before_certificate_formation": bool(certificates_received),
            "correct_identities_sign_once_per_height_round_type": correct_single_vote,
            "correct_vote_and_lock_guards_hold_at_signing": bool(correct_vote_guards),
            "vote_timeouts_have_prior_distinct_received_quorums": bool(timers_guarded),
            "all_decisions_have_local_precommit_certificates": decisions_justified,
        }

    def result(self) -> dict[str, Any]:
        decisions = {name: state.committed for name, state in self.replicas.items()
                     if name in CORRECT and state.committed is not None}
        observers = {name: value for name, value in decisions.items() if name in ("A", "C")}
        return {
            "grammar": self.grammar, "variant": self.variant, "repair_timing": self.repair_timing,
            "round1_b_prevote_route": self.round1_b_prevote_route,
            "vote_channel_order": self.vote_channel_order(),
            "unsafe": len(set(decisions.values())) > 1,
            "unmutated_observers_disagree": len(set(observers.values())) > 1,
            "decisions": decisions,
            "mutated_identities": ["P"] if self.variant == "MISSING_LOCK_UPDATE" else [],
            "mutated_lock_assignments": [{"validator": "P", "height": 1, "round": 0}]
            if self.variant == "MISSING_LOCK_UPDATE" else [],
            "proposers": list(self.proposers), "audit": self.audit(),
            "states": self._snapshot(), "certificates": self.certificates,
            "messages": [asdict(message) for message in self.messages.values()],
            "envelopes": [asdict(envelope) for envelope in self.envelopes.values()],
            "milestones": self.milestones, "log": self.log,
        }

    def vote_channel_order(self) -> dict[str, Any]:
        """Diagnose FIFO for admitted vote envelopes on each directed peer edge.

        Excludes proposals/blocks (different production channels) and envelopes
        rejected by the fixed graph/phase policy before transmission.  This is
        an ordering check on this trace, not a model of a TCP implementation.
        """
        delivered_at = {row["envelope"]: row["index"] for row in self.log if row["action"] == "DELIVER"}
        channels: dict[tuple[str, str], list[Envelope]] = {}
        for envelope in self.envelopes.values():
            message = self.messages[envelope.message_id]
            if message.kind in ("PREVOTE", "PRECOMMIT") and self._admitted(envelope, message):
                channels.setdefault((envelope.sender, envelope.receiver), []).append(envelope)
        violations = []
        for channel, envelopes in channels.items():
            for offset, earlier in enumerate(envelopes):
                for later in envelopes[offset + 1:]:
                    if later.id not in delivered_at:
                        continue
                    if earlier.id not in delivered_at or delivered_at[earlier.id] > delivered_at[later.id]:
                        violations.append({"sender": channel[0], "receiver": channel[1],
                                           "earlier_emitted": earlier.id, "later_emitted": later.id,
                                           "earlier_message": earlier.message_id,
                                           "later_message": later.message_id})
        return {"admitted_vote_envelopes_fifo": not violations, "violations": violations}


def _repair(loop: ConcreteTrace) -> None:
    loop.opportunity("B", "P", 0, "PRECOMMIT")
    state = loop.replicas["P"]
    if state.step == "COMMIT" and state.proposal_block is None:
        # A has already decided 0 in edge-on executions.  Forward actual block
        # data, rather than treating the old-round precommit as block data.
        loop.deliver(loop.send_block("A", "P", 0))
    loop.milestone("after_repair_opportunity")


def run_trace(
    grammar: str,
    variant: str,
    *,
    repair_timing: str = "before_round_1",
    stop_after_round_0: bool = False,
    proposers: tuple[str, str] = ("B", "C"),
    round1_b_prevote_route: str = "direct",
) -> ConcreteTrace:
    """Execute the same fixed delivery opportunities under one edge policy.

    Different guards cause different actual emissions; unavailable messages
    are recorded as unavailable, never injected.  Delaying repair is a
    separate change to the bounded ordering, not a fourth admission grammar.
    """
    loop = ConcreteTrace(grammar, variant, repair_timing=repair_timing, proposers=proposers,
                         round1_b_prevote_route=round1_b_prevote_route)
    proposal0 = loop.propose("B", 0, ("A",))
    proposal_envelope = next(iter(loop.envelopes))
    loop.deliver(proposal_envelope)
    loop.deliver(loop.relay("A", "P", proposal0))
    loop.timeout("C", "PROPOSE")  # C lawfully prevotes nil without block 0.
    # Both controlled envelopes exist before E is attempted.  Only Byzantine
    # B uses the adversarial signing primitive; all other votes follow guards.
    loop.byzantine_vote(0, "PREVOTE", 0)
    loop.byzantine_vote(0, "PRECOMMIT", 0)

    loop.opportunity("P", "A", 0, "PREVOTE")
    loop.opportunity("B", "A", 0, "PREVOTE")
    loop.opportunity("A", "P", 0, "PREVOTE")
    loop.opportunity("B", "P", 0, "PREVOTE")  # E: last value-0 prevote at P.
    loop.milestone("after_enabling_opportunity")

    loop.opportunity("C", "P", 0, "PREVOTE")
    loop.opportunity("P", "C", 0, "PREVOTE")
    loop.opportunity("A", "C", 0, "PREVOTE")
    loop.timeout_opportunity("P", "PREVOTE")
    loop.timeout_opportunity("C", "PREVOTE")

    loop.opportunity("A", "P", 0, "PRECOMMIT")
    loop.opportunity("A", "C", 0, "PRECOMMIT")
    loop.opportunity("P", "A", 0, "PRECOMMIT")
    loop.opportunity("P", "C", 0, "PRECOMMIT")
    loop.opportunity("B", "A", 0, "PRECOMMIT")  # C0: A obtains {A,P,B}:0 if P signed it.
    loop.opportunity("C", "P", 0, "PRECOMMIT")
    loop.milestone("after_first_certificate_opportunity")

    if repair_timing == "before_round_1":
        _repair(loop)
    else:
        loop._record("DEFER_REPAIR", detail="admitted R remains buffered; relaxed ordering")
    loop.timeout_opportunity("P", "PRECOMMIT")
    loop.timeout_opportunity("C", "PRECOMMIT")
    loop.milestone("round_1_entry")
    if stop_after_round_0:
        return loop

    # C has no value-0 PoLC, so its unchanged valid-block rule permits a new
    # block 1.  P would instead have to reuse its cached ValidBlock=0.
    proposer = proposers[1]
    state = loop.replicas[proposer]
    if state.height == 1 and state.round == 1 and state.step == "PROPOSE":
        proposal1 = loop.propose(proposer, 1, (proposer,))
        other = "P" if proposer == "C" else "C"
        loop.deliver(loop.relay(proposer, other, proposal1))
    else:
        loop._record("NO_ENABLED_PROPOSER", actor=proposer)
    b_prevote1 = loop.byzantine_vote(1, "PREVOTE", 1)
    loop.byzantine_vote(1, "PRECOMMIT", 1)
    loop.milestone("after_second_proposal_and_pivot_prevote")
    if repair_timing == "after_pivot_prevote":
        _repair(loop)

    # The pivot's precommit is the irreversible enabling action for C1.
    loop.opportunity("C", "P", 1, "PREVOTE")
    if round1_b_prevote_route == "via_C":
        # A separate fixed gossip skeleton avoids overtaking R on B->P's
        # vote channel.  C already possesses B's signed vote before relaying.
        loop.opportunity("B", "C", 1, "PREVOTE")
        loop.deliver(loop.relay("C", "P", b_prevote1))
    else:
        loop.opportunity("B", "P", 1, "PREVOTE")
    loop.milestone("after_pivot_precommit_opportunity")
    if repair_timing == "after_pivot_precommit":
        _repair(loop)
    if round1_b_prevote_route == "via_C":
        # The original direct copy is now delivered after R, respecting its
        # position in that peer channel.  It may be stale/duplicate locally.
        loop.opportunity("B", "P", 1, "PREVOTE")
    loop.opportunity("P", "C", 1, "PREVOTE")
    if round1_b_prevote_route == "direct":
        loop.opportunity("B", "C", 1, "PREVOTE")
    loop.timeout_opportunity("P", "PREVOTE")
    loop.timeout_opportunity("C", "PREVOTE")

    loop.opportunity("P", "C", 1, "PRECOMMIT")
    loop.opportunity("B", "C", 1, "PRECOMMIT")  # C1 uses buffered P vote even after repair.
    loop.opportunity("C", "P", 1, "PRECOMMIT")
    loop.opportunity("B", "P", 1, "PRECOMMIT")
    loop.milestone("after_second_certificate_opportunity")
    return loop


def evaluate_suite() -> dict[str, Any]:
    cases = [run_trace(grammar, variant).result() for variant in VARIANTS for grammar in GRAMMARS]
    cases.extend(
        run_trace("G_D_EDGE_ON", variant, repair_timing=timing).result()
        for timing in REPAIR_TIMINGS[1:] for variant in VARIANTS
    )
    by_key = {(case["grammar"], case["variant"], case["repair_timing"]): case for case in cases}
    relay_cases = [
        run_trace("G_D_EDGE_ON", variant, repair_timing="after_pivot_precommit",
                  round1_b_prevote_route="via_C").result()
        for variant in VARIANTS
    ]
    cases.extend(relay_cases)
    checks = {
        "all_trace_legality_audits_pass": all(all(case["audit"].values()) for case in cases),
        "all_baselines_safe": all(not case["unsafe"] for case in cases if case["variant"] == "BASELINE"),
        "fine_mutant_has_two_unmutated_conflicting_observers": by_key[
            ("G_T_PHASE_SPECIFIC", "MISSING_LOCK_UPDATE", "before_round_1")
        ]["unmutated_observers_disagree"],
        "both_fixed_order_coarse_mutants_safe": all(not by_key[
            (grammar, "MISSING_LOCK_UPDATE", "before_round_1")
        ]["unsafe"] for grammar in GRAMMARS[1:]),
        "repair_after_pivot_prevote_still_prevents_second_commit": not by_key[
            ("G_D_EDGE_ON", "MISSING_LOCK_UPDATE", "after_pivot_prevote")
        ]["unsafe"],
        "repair_after_pivot_precommit_fails_even_before_second_commit": by_key[
            ("G_D_EDGE_ON", "MISSING_LOCK_UPDATE", "after_pivot_precommit")
        ]["unmutated_observers_disagree"],
        "canonical_six_traces_respect_admitted_vote_channel_fifo": all(
            case["vote_channel_order"]["admitted_vote_envelopes_fifo"]
            for case in cases if case["repair_timing"] == "before_round_1"
        ),
        "direct_late_control_identifies_its_non_fifo_assumption": not by_key[
            ("G_D_EDGE_ON", "MISSING_LOCK_UPDATE", "after_pivot_precommit")
        ]["vote_channel_order"]["admitted_vote_envelopes_fifo"],
        "both_relay_controls_respect_admitted_vote_channel_fifo": all(
            case["vote_channel_order"]["admitted_vote_envelopes_fifo"] for case in relay_cases
        ),
        "fifo_relay_late_mutant_still_has_conflicting_unmutated_observers": relay_cases[1][
            "unmutated_observers_disagree"
        ],
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "n=4, one Byzantine B, equal voting power, height 1, rounds 0 and 1",
        "authentication": "deterministic test-only HMAC, not production Ed25519",
        "mutation": "only P's round-0 persistent lock assignment is omitted; valid-block and round-1 lock updates are retained",
        "source": {"tag": "v0.39.3", "commit": SOURCE_COMMIT, "state_url": SOURCE_URL,
                   "local_snapshot": "models/tendermint_style/upstream_v0393"},
        "fixed_active_edges": {str(round_): [list(edge) for edge in sorted(edges)]
                               for round_, edges in FIXED_ACTIVE_EDGES.items()},
        "checks": checks, "cases": cases,
    }
