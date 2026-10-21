"""Seven-validator guarded experiment with six dependent admission fibres.

The compact explorer is replayed independently through parameterized
``ConcreteTrace`` rules.  A bound consists of 16 stages and 23 once-only
opportunities; fixed batches retain the explicitly listed delivery order.
All permutations within a stage are exported, including repair/timeout races.
A state bound raises EnumerationLimit: it never yields a truncated safe graph.
This is a finite model with injected lock omissions, not a client vulnerability.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .concrete_trace import ConcreteTrace, IllegalAction
from .coupled_protocol import EnumerationLimit
from .transition_synthesis import Problem, Transition

VALIDATORS = ("A", "P0", "P1", "C", "D", "B0", "B1")
CORRECT = VALIDATORS[:5]
BYZANTINE = VALIDATORS[5:]
PIVOTS = ("P0", "P1")
QUORUM = 5
FIBRES = tuple(f"{s}->{r}:H1:R0" for r in PIVOTS for s in ("A", "B0", "B1"))
FINE_KEYS = tuple(f"{f}:{k}" for f in FIBRES for k in ("PREVOTE", "PRECOMMIT"))
KEY_FIBRES = tuple(i // 2 for i in range(12))
VARIANTS = ("BASELINE", "ONLY_P0_MUTATED", "MISSING_LOCK_UPDATE")
DEPENDENCIES = ("NONE", "NO_CROSS_PREVOTE", "NO_NIL_TIMEOUT_SUPPORT", "NO_ROUND1_P1_PREVOTE")
INDEX = {v: i for i, v in enumerate(VALIDATORS)}
ABSENT, NIL = -2, -1
PROPOSE, PREVOTE, PRECOMMIT, COMMIT, DECIDED = range(5)
# Replica fields; all guard-observable state is retained in the finite export.
R, STEP, LOCK, LR, VALID, VR, PROP, PVR, KNOWN, CV, CR, DEC, RECV, TIMERS = range(14)


def mutation_set(variant: str) -> frozenset[str]:
    if variant not in VARIANTS:
        raise ValueError("unknown variant")
    return frozenset(() if variant == "BASELINE" else ("P0",) if variant == "ONLY_P0_MUTATED" else PIVOTS)


@dataclass(frozen=True)
class Action:
    kind: str
    args: tuple[Any, ...] = ()

    @property
    def label(self) -> str:
        return ":".join((self.kind, *(str(x) for x in self.args)))


def vote(sender: str, receiver: str, round_: int, kind: str) -> Action:
    return Action("vote", (sender, receiver, round_, kind))


STAGES = (
    (Action("bootstrap"),),
    (Action("round0_fixed_prevotes"),),
    tuple(vote("A", p, 0, "PREVOTE") for p in PIVOTS),
    tuple(vote("B0", p, 0, "PREVOTE") for p in PIVOTS),
    tuple(vote("B1", p, 0, "PREVOTE") for p in PIVOTS),
    (Action("round0_mixed_prevotes_and_timeouts"),),
    (Action("round0_fixed_precommits"),),
    tuple(vote("A", p, 0, "PRECOMMIT") for p in PIVOTS),
    tuple(vote("B0", p, 0, "PRECOMMIT") for p in PIVOTS),
    (vote("B1", "P0", 0, "PRECOMMIT"), Action("timeout", ("P0", 0, "PRECOMMIT"))),
    (vote("B1", "P1", 0, "PRECOMMIT"), Action("timeout", ("P1", 0, "PRECOMMIT"))),
    (Action("timeout", ("C", 0, "PRECOMMIT")),),
    (Action("round1_proposal_and_byzantine_votes"),),
    (Action("round1_prevotes"),),
    (Action("round1_prevote_timeouts"),),
    (Action("round1_precommits"),),
)
OPPORTUNITY_BOUND = sum(map(len, STAGES))


class Engine:
    """Compact operational rules: integer vote sets, never preloaded quorums."""
    def __init__(self, variant: str, dependency: str = "NONE", frozen=None):
        self.mutated = mutation_set(variant)
        if dependency not in DEPENDENCIES:
            raise ValueError("unknown dependency control")
        self.variant, self.dependency = variant, dependency
        if frozen is None:
            # r,step,lock,lock-r,valid,valid-r,proposal,pol-r,known,commit,commit-r,decision,votes,timers
            self.nodes = [[0, PROPOSE, NIL, -1, NIL, -1, ABSENT, -1, 0, NIL, -1, NIL, [0]*4, 1]
                          for _ in CORRECT]
            self.signed = [ABSENT] * (4 * len(VALIDATORS))
        else:
            nodes, signed = frozen
            self.nodes = [list(n[:RECV]) + [list(n[RECV]), n[TIMERS]] for n in nodes]
            self.signed = list(signed)

    def freeze(self):
        return (tuple(tuple(n[:RECV]) + (tuple(n[RECV]), n[TIMERS]) for n in self.nodes), tuple(self.signed))

    @staticmethod
    def slot(round_: int, kind: str) -> int:
        return 2 * round_ + (kind == "PRECOMMIT")

    def votes(self, actor: str, round_: int, kind: str, value=None) -> tuple[int, ...]:
        slot = self.slot(round_, kind)
        mask = self.nodes[INDEX[actor]][RECV][slot]
        return tuple(i for i in range(7) if mask >> i & 1 and
                     (value is None or self.signed[slot * 7 + i] == value))

    def majority(self, actor: str, round_: int, kind: str):
        for value in (0, 1, NIL):
            if len(self.votes(actor, round_, kind, value)) >= QUORUM:
                return value
        return ABSENT

    def sign(self, actor: str, round_: int, kind: str, value: int) -> None:
        slot, who = self.slot(round_, kind), INDEX[actor]
        if self.signed[slot * 7 + who] != ABSENT:
            raise IllegalAction("a signer cannot issue a second vote for its slot")
        self.signed[slot * 7 + who] = value
        if actor in CORRECT:
            self.deliver(actor, actor, round_, kind)

    def proposal(self, receiver: str, value: int, round_: int, valid_round: int = -1) -> None:
        n = self.nodes[INDEX[receiver]]
        if n[DEC] != NIL or n[STEP] == COMMIT or n[R] != round_ or n[PROP] != ABSENT:
            return
        n[PROP], n[PVR] = value, valid_round
        n[KNOWN] |= 1 << value
        if n[STEP] == PROPOSE and (valid_round == -1 or self.majority(receiver, valid_round, "PREVOTE") != ABSENT):
            self.prevote(receiver)

    def prevote(self, actor: str) -> None:
        n = self.nodes[INDEX[actor]]
        if n[STEP] != PROPOSE or n[DEC] != NIL:
            raise IllegalAction("prevote entry needs a live proposal step")
        value = n[LOCK] if n[LOCK] != NIL else n[PROP] if n[PROP] != ABSENT else NIL
        n[STEP], n[TIMERS] = PREVOTE, n[TIMERS] & ~1
        self.sign(actor, n[R], "PREVOTE", value)

    def precommit(self, actor: str, timeout: str | None = None) -> None:
        n = self.nodes[INDEX[actor]]
        if n[STEP] not in (PROPOSE, PREVOTE):
            raise IllegalAction("invalid precommit entry")
        value = self.majority(actor, n[R], "PREVOTE")
        if value == ABSENT:
            if timeout is None or len(self.votes(actor, n[R], timeout)) < QUORUM:
                raise IllegalAction("no PoLC or quorum-enabled timeout")
            value = NIL
        elif value == NIL:
            n[LOCK], n[LR] = NIL, -1
        elif value == n[PROP] or value == n[LOCK]:
            if not (n[R] == 0 and actor in self.mutated):
                n[LOCK], n[LR] = value, n[R]
        else:
            n[LOCK], n[LR], value = NIL, -1, NIL
        n[STEP], n[TIMERS] = PRECOMMIT, n[TIMERS] & ~3
        self.sign(actor, n[R], "PRECOMMIT", value)

    def deliver(self, sender: str, receiver: str, round_: int, kind: str) -> None:
        slot, who = self.slot(round_, kind), INDEX[sender]
        if self.signed[slot * 7 + who] == ABSENT:
            return  # missing production is not replaced by synthetic evidence
        n = self.nodes[INDEX[receiver]]
        if n[DEC] != NIL or n[STEP] == COMMIT or n[RECV][slot] >> who & 1:
            return
        n[RECV][slot] |= 1 << who
        value = self.majority(receiver, round_, kind)
        count = len(self.votes(receiver, round_, kind))
        if round_ > n[R]:
            if count >= QUORUM:
                raise IllegalAction("future-round skip outside this declared language")
            return
        if kind == "PRECOMMIT":
            if value != ABSENT and round_ == n[R] and n[STEP] in (PROPOSE, PREVOTE):
                raise IllegalAction("early precommit auto-entry outside declared language")
            if value >= 0:
                n[CV], n[CR], n[STEP], n[TIMERS] = value, round_, COMMIT, 0
                if n[LOCK] == value:
                    n[PROP] = value
                if n[PROP] != value:
                    n[PROP] = ABSENT
                else:
                    n[DEC], n[STEP], n[R] = value, DECIDED, 0
                    n[LOCK], n[LR], n[VALID], n[VR], n[PROP], n[PVR] = NIL, -1, NIL, -1, ABSENT, -1
            elif round_ == n[R] and count >= QUORUM:
                n[TIMERS] |= 4
            return
        if value != ABSENT:
            if n[LOCK] != NIL and n[LR] < round_ <= n[R] and n[LOCK] != value:
                n[LOCK], n[LR] = NIL, -1
            if round_ == n[R] and value >= 0 and n[VR] < round_ and n[PROP] == value:
                n[VALID], n[VR] = value, round_
        if round_ != n[R]:
            return
        if n[STEP] == PREVOTE:
            if value != ABSENT and (value == NIL or n[PROP] != ABSENT):
                self.precommit(receiver)
            elif count >= QUORUM:
                n[TIMERS] |= 2

    def timeout(self, actor: str, round_: int, kind: str) -> None:
        n = self.nodes[INDEX[actor]]
        timer = {"PROPOSE": 1, "PREVOTE": 2, "PRECOMMIT": 4}[kind]
        if n[DEC] != NIL or n[STEP] == COMMIT or n[R] != round_ or not n[TIMERS] & timer:
            return
        if kind != "PROPOSE" and len(self.votes(actor, round_, kind)) < QUORUM:
            raise IllegalAction("timeout without a local quorum")
        n[TIMERS] &= ~timer
        if kind == "PROPOSE":
            self.prevote(actor)
        elif kind == "PREVOTE":
            self.precommit(actor, kind)
        else:
            if n[STEP] in (PROPOSE, PREVOTE):
                self.precommit(actor, kind)
            if round_ != 0:
                raise IllegalAction("no round 2 in the bound")
            n[R], n[STEP], n[PROP], n[PVR], n[TIMERS] = 1, PROPOSE, ABSENT, -1, 1

    def bootstrap(self):
        for actor in ("C", "D"):
            self.timeout(actor, 0, "PROPOSE")
        for actor in ("A", "P0", "P1", "D"):
            self.proposal(actor, 0, 0)
        for actor in BYZANTINE:
            for kind in ("PREVOTE", "PRECOMMIT"):
                self.sign(actor, 0, kind, 0)

    def round1(self):
        n = self.nodes[INDEX["C"]]
        if n[DEC] == NIL and n[R] == 1 and n[STEP] == PROPOSE:
            value = n[VALID] if n[VALID] != NIL else 1
            vr = n[VR]
            for actor in ("C", "P0", "P1"):
                self.proposal(actor, value, 1, vr)
        for actor in BYZANTINE:
            for kind in ("PREVOTE", "PRECOMMIT"):
                self.sign(actor, 1, kind, 1)

    def control_key(self, action: Action) -> int | None:
        if action.kind != "vote":
            return None
        sender, receiver, round_, kind = action.args
        if self.signed[self.slot(round_, kind) * 7 + INDEX[sender]] == ABSENT:
            return None
        name = f"{sender}->{receiver}:H1:R{round_}:{kind}"
        return FINE_KEYS.index(name) if name in FINE_KEYS else None

    def apply(self, action: Action, answer: bool | None = None) -> None:
        key = self.control_key(action)
        if (key is None) != (answer is None) or answer is not None and type(answer) is not bool:
            raise ValueError("only an emitted controlled envelope requires a Boolean")
        if action.kind == "vote":
            if key is None or answer:
                self.deliver(*action.args)
        elif action.kind == "timeout":
            self.timeout(*action.args)
        else:
            run_batch(self, action.kind)

    def unsafe(self) -> bool:
        a, c = self.nodes[INDEX["A"]][DEC], self.nodes[INDEX["C"]][DEC]
        return a != NIL and c != NIL and a != c


def run_batch(loop, kind: str) -> None:
    """Fixed macro steps; every internal operation still checks protocol guards."""
    if kind == "bootstrap":
        loop.bootstrap()
    elif kind == "round0_fixed_prevotes":
        for sender in ("P0", "P1", "B0", "B1"):
            loop.deliver(sender, "A", 0, "PREVOTE")
        if loop.dependency != "NO_CROSS_PREVOTE":
            loop.deliver("P0", "P1", 0, "PREVOTE")
            loop.deliver("P1", "P0", 0, "PREVOTE")
    elif kind == "round0_mixed_prevotes_and_timeouts":
        for receiver in PIVOTS:
            for sender in ("C", "D"):
                loop.deliver(sender, receiver, 0, "PREVOTE")
        for receiver in ("C", "D"):
            for sender in ("A", "B0", "B1", "D" if receiver == "C" else "C"):
                loop.deliver(sender, receiver, 0, "PREVOTE")
        for receiver in ("P0", "P1", "C", "D"):
            loop.timeout(receiver, 0, "PREVOTE")
    elif kind == "round0_fixed_precommits":
        for sender in ("P0", "P1", "B0", "B1"):
            loop.deliver(sender, "A", 0, "PRECOMMIT")
        for receiver, peer in (("P0", "P1"), ("P1", "P0")):
            loop.deliver(peer, receiver, 0, "PRECOMMIT")
            if loop.dependency != "NO_NIL_TIMEOUT_SUPPORT":
                for sender in ("C", "D"):
                    loop.deliver(sender, receiver, 0, "PRECOMMIT")
        for sender in ("A", "P0", "P1", "D"):
            loop.deliver(sender, "C", 0, "PRECOMMIT")
    elif kind == "round1_proposal_and_byzantine_votes":
        loop.round1()
    elif kind == "round1_prevotes":
        for receiver in ("C", "P0", "P1"):
            for sender in ("C", "P0", "P1", "B0", "B1"):
                if sender == receiver or (sender == "P1" and loop.dependency == "NO_ROUND1_P1_PREVOTE"):
                    continue
                loop.deliver(sender, receiver, 1, "PREVOTE")
    elif kind == "round1_prevote_timeouts":
        for actor in ("P0", "P1", "C"):
            loop.timeout(actor, 1, "PREVOTE")
    elif kind == "round1_precommits":
        for receiver in ("C", "P0", "P1"):
            for sender in ("C", "P0", "P1", "B0", "B1"):
                if sender != receiver:
                    loop.deliver(sender, receiver, 1, "PRECOMMIT")
    else:
        raise ValueError(f"unknown batch {kind}")


def advance(stage: int, remaining: int, slot: int):
    remaining &= ~(1 << slot)
    if remaining == 0:
        stage += 1
        remaining = (1 << len(STAGES[stage])) - 1 if stage < len(STAGES) else 0
    return stage, remaining


@dataclass
class ModelGraph:
    problem: Problem
    variant: str
    dependency: str
    semantic_states: tuple
    edge_actions: tuple[tuple[int, int], ...]


def build_model(variant="MISSING_LOCK_UPDATE", *, dependency="NONE", costs=(1,)*6,
                allowed_split=None, max_states=150_000) -> ModelGraph:
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be positive")
    initial = (0, 1, Engine(variant, dependency).freeze())
    states, seen, queue = [initial], {initial: 0}, deque([0])
    edges, actions, bad = [], [], set()
    while queue:
        source = queue.popleft()
        stage, remaining, frozen = states[source]
        loop = Engine(variant, dependency, frozen)
        if loop.unsafe():
            bad.add(source)
        if stage == len(STAGES):
            continue
        for slot, action in enumerate(STAGES[stage]):
            if not remaining >> slot & 1:
                continue
            key = loop.control_key(action)
            for answer in ((None,) if key is None else (False, True)):
                nxt = Engine(variant, dependency, frozen)
                nxt.apply(action, answer)
                end = (*advance(stage, remaining, slot), nxt.freeze())
                if end not in seen:
                    if len(states) >= max_states:
                        raise EnumerationLimit("unknown: complete scaled graph exceeds state limit")
                    seen[end] = len(states)
                    states.append(end)
                    queue.append(seen[end])
                target = seen[end]
                edges.append(Transition(source, target, key, answer, f"stage{stage}:{action.label}"))
                actions.append((stage, slot))
    names = tuple(f"q{i}:" + sha256(repr(s).encode()).hexdigest()[:16] for i, s in enumerate(states))
    problem = Problem(names, 0, frozenset(bad), tuple(edges), KEY_FIBRES, tuple(costs), allowed_split)
    return ModelGraph(problem, variant, dependency, tuple(states), tuple(actions))


class GuardedReplay:
    """Independent dictionary/HMAC execution; no compact transition code is used."""
    def __init__(self, variant: str, dependency: str, policy):
        self.variant, self.dependency = variant, dependency
        self.policy = tuple(policy)
        class FullTrace(ConcreteTrace):
            def _admitted(inner, envelope, message):
                key = f"{envelope.sender}->{envelope.receiver}:H{message.height}:R{message.round}:{message.kind}"
                return self.policy[FINE_KEYS.index(key)] if key in FINE_KEYS else True
        self.loop = FullTrace(variant="BASELINE" if variant == "BASELINE" else "MISSING_LOCK_UPDATE",
                              validators=VALIDATORS, byzantine=BYZANTINE,
                              mutated=tuple(mutation_set(variant)), quorum=5, proposers=("B0", "C"))

    def deliver(self, sender, receiver, round_, kind):
        self.loop.opportunity(sender, receiver, round_, kind)

    def timeout(self, actor, round_, kind):
        state = self.loop.replicas[actor]
        if state.height == 1 and state.round == round_:
            self.loop.timeout_opportunity(actor, kind)

    def bootstrap(self):
        for actor in ("C", "D"):
            self.loop.timeout(actor, "PROPOSE")
        msg = self.loop.propose("B0", 0, ("A", "P0", "P1", "D"))
        for key, env in list(self.loop.envelopes.items()):
            if env.message_id == msg:
                self.loop.deliver(key)
        for actor in BYZANTINE:
            for kind in ("PREVOTE", "PRECOMMIT"):
                self.loop.byzantine_vote(0, kind, 0, signer=actor)

    def round1(self):
        n = self.loop.replicas["C"]
        if n.height == 1 and n.round == 1 and n.step == "PROPOSE":
            msg = self.loop.propose("C", 1, ("C", "P0", "P1"))
            for key, env in list(self.loop.envelopes.items()):
                if env.message_id == msg and env.status == "BUFFERED":
                    self.loop.deliver(key)
        for actor in BYZANTINE:
            for kind in ("PREVOTE", "PRECOMMIT"):
                self.loop.byzantine_vote(1, kind, 1, signer=actor)

    def freeze(self):
        nodes, signed = [], [ABSENT] * 28
        step_map = {"PROPOSE": PROPOSE, "PREVOTE": PREVOTE, "PRECOMMIT": PRECOMMIT,
                    "COMMIT": COMMIT, "NEW_HEIGHT": DECIDED}
        for name in VALIDATORS:
            state = self.loop.replicas[name]
            for (_, r, kind), mid in state.signed_votes.items():
                msg = self.loop.messages[mid]
                signed[Engine.slot(r, kind) * 7 + INDEX[name]] = NIL if msg.value is None else msg.value
            if name not in CORRECT:
                continue
            received = [0]*4
            for _, r, kind, sender in state.received_votes:
                received[Engine.slot(r, kind)] |= 1 << INDEX[sender]
            timer = sum({"PROPOSE": 1, "PREVOTE": 2, "PRECOMMIT": 4}[k]
                        for r, k in state.timers if r == state.round)
            value = lambda x: NIL if x is None else x
            proposal = ABSENT if state.proposal_block is None else state.proposal_block
            pvr = -1 if state.proposal_id is None else self.loop.messages[state.proposal_id].valid_round
            nodes.append((state.round, step_map[state.step], value(state.locked_value), state.locked_round,
                          value(state.valid_value), state.valid_round, proposal, pvr,
                          sum(1 << x for x in state.known_blocks), value(state.commit_value),
                          -1 if state.commit_round is None else state.commit_round,
                          value(state.committed), tuple(received), timer))
        return tuple(nodes), tuple(signed)

    def apply(self, action: Action):
        if action.kind == "vote":
            self.deliver(*action.args)
        elif action.kind == "timeout":
            self.timeout(*action.args)
        else:
            run_batch(self, action.kind)


def replay(model: ModelGraph, transitions, policy) -> dict:
    if len(policy) != len(FINE_KEYS) or any(type(x) is not bool for x in policy):
        raise ValueError("one strict Boolean per fine key is required")
    full = GuardedReplay(model.variant, model.dependency, policy)
    source, schedule = model.problem.initial, []
    for index in transitions:
        if type(index) is not int or not 0 <= index < len(model.problem.transitions):
            raise ValueError("invalid replay edge")
        edge = model.problem.transitions[index]
        if edge.source != source or edge.key is not None and policy[edge.key] != edge.value:
            raise ValueError("path or persistent policy mismatch")
        stage, slot = model.edge_actions[index]
        action = STAGES[stage][slot]
        full.apply(action)
        if full.freeze() != model.semantic_states[edge.target][2]:
            raise AssertionError(f"independent guarded replay differs after {action.label}")
        source = edge.target
        schedule.append({"edge": index, "stage": stage, "slot": slot, "action": action.label,
                         "key": edge.key, "value": edge.value})
    audits = full.loop.audit()
    audits.pop("all_other_transport_edges_have_type_uniform_delivery", None)
    audits["independent_guarded_replay_matches_each_compact_successor"] = True
    audits["every_resolved_envelope_matches_declared_policy"] = all(
        (e.status == "DELIVERED") == full.loop._admitted(e, full.loop.messages[e.message_id])
        for e in full.loop.envelopes.values() if e.status != "BUFFERED")
    if not all(audits.values()):
        raise AssertionError(audits)
    from dataclasses import asdict
    return {"variant": model.variant, "dependency": model.dependency,
            "validators": VALIDATORS, "quorum": QUORUM, "policy": list(policy),
            "unsafe": source in model.problem.unsafe,
            "decisions": {n: s.committed for n, s in full.loop.replicas.items() if s.committed is not None},
            "audit": audits, "schedule": schedule, "certificates": full.loop.certificates,
            "messages": [asdict(m) for m in full.loop.messages.values()], "log": full.loop.log}


def initial_partition(model: ModelGraph) -> tuple[int, ...]:
    """Guard-aware overapproximation, selected after a coarse-seed pilot.

    Keep control progress, unsafe observation, and each pivot's round-zero
    value-zero prevote count and emitted precommit. Forget signer sets,
    precommit evidence, timers, locks and commit-wait state. The selector is
    heuristic; checked edge coverage, not the seed, justifies lower bounds.
    """
    classes, partition = {}, []
    for stage, remaining, frozen in model.semantic_states:
        nodes, signed = frozen
        unsafe = nodes[0][DEC] != NIL and nodes[3][DEC] != NIL and nodes[0][DEC] != nodes[3][DEC]
        pivots = tuple((sum(bool(nodes[INDEX[p]][RECV][0] >> i & 1) and signed[i] == 0
                             for i in range(7)), signed[7 + INDEX[p]]) for p in PIVOTS)
        key = (stage, remaining, unsafe, pivots)
        partition.append(classes.setdefault(key, len(classes)))
    return tuple(partition)


def flow_partition(model: ModelGraph) -> tuple[int, ...]:
    """Coarser, guard-blind seed used only for the declared pilot control."""
    classes = {}
    return tuple(classes.setdefault((s[0], s[1], i in model.problem.unsafe), len(classes))
                 for i, s in enumerate(model.semantic_states))
