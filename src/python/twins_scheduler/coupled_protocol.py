"""A finite, exhaustively enumerable, state-coupled BFT test environment.

This adapter executes the guarded rules in :mod:`concrete_trace`; it does not
replace quorum assembly by a pivot count.  Its explicit environment bound is
two rounds and twelve finite groups of delivery/timeout opportunities.  Every
permutation within a group is included.  This is a bounded rule-level model,
not all executions of the CometBFT client.

Two round-0 endpoint/view fibres, B->P and A->P, are controlled.  The latter
includes the proposal relay as well as both vote types: no message is exempted
from coarse uniformity because it is useful to the witness.  Both prevote
deliveries jointly enable P's first precommit, while both precommit deliveries
jointly cause its repair.  The same signed vote also contributes to another
replica's quorum, and later emissions depend on timeout, valid-block and lock
state.  These dependencies do not satisfy independent-pivot assumptions.
"""

from __future__ import annotations

from collections import deque
from copy import deepcopy
from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import itertools
import json
from typing import Any, Iterable

from .concrete_trace import ConcreteTrace, CORRECT, IllegalAction
from .transition_synthesis import Problem, Transition


FINE_KEYS = (
    "B->P:H1:R0:PREVOTE", "B->P:H1:R0:PRECOMMIT",
    "A->P:H1:R0:PROPOSAL", "A->P:H1:R0:PREVOTE",
    "A->P:H1:R0:PRECOMMIT", "A->P:H1:R0:BLOCK",
)
KEY_FIBRES = (0, 0, 1, 1, 1, 1)
FIBRES = ("B->P:H1:R0", "A->P:H1:R0")


class EnumerationLimit(RuntimeError):
    """The explicit graph is incomplete: no safety/optimality claim follows."""


@dataclass(frozen=True)
class Action:
    kind: str
    args: tuple[Any, ...] = ()

    @property
    def label(self) -> str:
        return ":".join((self.kind, *(str(arg) for arg in self.args)))


def _vote(sender: str, receiver: str, round_: int, kind: str) -> Action:
    return Action("vote", (sender, receiver, round_, kind))


# This list is the complete environment language, not a search heuristic.
# A slot whose envelope/timer does not exist is recorded as an opportunity
# without a protocol transition.  Such a slot cannot synthesize a vote/timer.
STAGES = (
    (Action("bootstrap"),),
    (Action("proposal0_relay"),),
    tuple(_vote(a, b, 0, "PREVOTE") for a, b in
          (("P", "A"), ("B", "A"), ("A", "P"), ("B", "P"))),
    tuple(_vote(a, b, 0, "PREVOTE") for a, b in
          (("C", "P"), ("P", "C"), ("A", "C"))),
    (Action("timeout", ("P", 0, "PREVOTE")), Action("timeout", ("C", 0, "PREVOTE"))),
    tuple(_vote(a, b, 0, "PRECOMMIT") for a, b in
          (("A", "P"), ("A", "C"), ("P", "A"), ("P", "C"),
           ("B", "A"), ("C", "P"))),
    (_vote("B", "P", 0, "PRECOMMIT"),
     Action("timeout", ("P", 0, "PRECOMMIT")), Action("timeout", ("C", 0, "PRECOMMIT"))),
    (Action("block_catchup"),),
    (Action("proposal1_and_byzantine_votes"),),
    tuple(_vote(a, b, 1, "PREVOTE") for a, b in
          (("C", "P"), ("B", "P"), ("P", "C"), ("B", "C"))),
    (Action("timeout", ("P", 1, "PREVOTE")), Action("timeout", ("C", 1, "PREVOTE"))),
    tuple(_vote(a, b, 1, "PRECOMMIT") for a, b in
          (("P", "C"), ("B", "C"), ("C", "P"), ("B", "P"))),
)
OPPORTUNITY_BOUND = sum(len(stage) for stage in STAGES)


class CoupledTrace(ConcreteTrace):
    """The existing guarded protocol with an explicit, external admission bit."""

    def __init__(self, variant: str, *, retain_log: bool = False) -> None:
        self.retain_log = retain_log
        self.admission: tuple[int, bool] | None = None
        self.total_policy: tuple[bool, ...] | None = None
        # An actual audit-history field, never consulted by protocol guards.
        self.first_round0_prevote_peer: str | None = None
        super().__init__("G_T_PHASE_SPECIFIC", variant)

    def _record(self, action: str, **details: Any) -> None:
        if self.retain_log:
            super()._record(action, **details)
        else:
            # Existing rules use len(log) only for observation timestamps.
            # Full audit snapshots are reconstructed on the selected witness.
            self.log.append({})

    @staticmethod
    def fine_key(envelope, message) -> int | None:
        if (message.height, message.round, envelope.receiver) != (1, 0, "P"):
            return None
        name = f"{envelope.sender}->P:H1:R0:{message.kind}"
        if name in FINE_KEYS:
            return FINE_KEYS.index(name)
        if envelope.sender in ("A", "B"):
            raise IllegalAction("a controlled message kind is outside the declared fine-key alphabet")
        return None

    def _admitted(self, envelope, message) -> bool:
        key = self.fine_key(envelope, message)
        if key is not None:
            if self.total_policy is not None:
                return self.total_policy[key]
            if self.admission is None or self.admission[0] != key:
                raise IllegalAction("a controlled envelope lacks its explicit admission decision")
            return self.admission[1]
        return super()._admitted(envelope, message)

    def _receive(self, name, message) -> None:
        if (name == "P" and message.round == 0 and message.kind == "PREVOTE"
                and message.signer in ("A", "B")
                and self.first_round0_prevote_peer is None):
            self.first_round0_prevote_peer = message.signer
        super()._receive(name, message)


def _proposal_envelope(loop: CoupledTrace) -> str:
    matches = [key for key, envelope in loop.envelopes.items()
               if envelope.status == "BUFFERED" and envelope.sender == "A"
               and envelope.receiver == "P"
               and loop.messages[envelope.message_id].kind == "PROPOSAL"]
    if len(matches) != 1:
        raise IllegalAction("the once-only round-0 proposal relay must exist")
    return matches[0]


def action_key(loop: CoupledTrace, action: Action) -> int | None:
    envelope_id = None
    if action.kind == "proposal0_relay":
        envelope_id = _proposal_envelope(loop)
    elif action.kind == "vote":
        envelope_id = loop.vote_envelope(*action.args)
    elif action.kind == "block_catchup":
        # This environment slot first sends locally known block data, then
        # resolves its newly emitted envelope under the BLOCK admission bit.
        return FINE_KEYS.index("A->P:H1:R0:BLOCK") if _block_catchup_enabled(loop) else None
    if envelope_id is None:
        return None
    envelope = loop.envelopes[envelope_id]
    return loop.fine_key(envelope, loop.messages[envelope.message_id])


def _block_catchup_enabled(loop: CoupledTrace) -> bool:
    pivot = loop.replicas["P"]
    return (pivot.height == 1 and pivot.step == "COMMIT" and pivot.commit_value == 0
            and pivot.proposal_block is None and 0 in loop.replicas["A"].known_blocks)


def apply_action(loop: CoupledTrace, action: Action, value: bool | None = None) -> None:
    """Execute guarded rules; all unproduced opportunities remain unproduced."""
    key = action_key(loop, action)
    if (key is None) != (value is None):
        raise ValueError("exactly the enabled controlled delivery requires a Boolean decision")
    if value is not None and type(value) is not bool:
        raise ValueError("an admission decision must be a strict Boolean")
    loop.admission = None if key is None else (key, value)
    try:
        if action.kind == "bootstrap":
            proposal = loop.propose("B", 0, ("A",))
            loop.deliver(next(iter(loop.envelopes)))
            loop.relay("A", "P", proposal)  # Buffered: resolution is a controlled slot.
            loop.timeout("C", "PROPOSE")
            loop.byzantine_vote(0, "PREVOTE", 0)
            loop.byzantine_vote(0, "PRECOMMIT", 0)
        elif action.kind == "proposal0_relay":
            loop.deliver(_proposal_envelope(loop))
        elif action.kind == "vote":
            loop.opportunity(*action.args)
        elif action.kind == "timeout":
            actor, round_, kind = action.args
            state = loop.replicas[actor]
            if state.height == 1 and state.round == round_:
                loop.timeout_opportunity(actor, kind)
            else:
                loop._record("NO_ENABLED_TIMEOUT", actor=actor, round=round_, timer=kind)
        elif action.kind == "block_catchup":
            if _block_catchup_enabled(loop):
                # send_block checks local block possession, creates an actual
                # authenticated payload, and emits before deliver resolves it.
                loop.deliver(loop.send_block("A", "P", 0))
            else:
                loop._record("NO_ENABLED_BLOCK_CATCHUP", actor="A", receiver="P", value=0)
        elif action.kind == "proposal1_and_byzantine_votes":
            state = loop.replicas["C"]
            if state.height == 1 and state.round == 1 and state.step == "PROPOSE":
                proposal = loop.propose("C", 1, ("C",))
                loop.deliver(loop.relay("C", "P", proposal))
            else:
                loop._record("NO_ENABLED_PROPOSER", actor="C")
            loop.byzantine_vote(1, "PREVOTE", 1)
            loop.byzantine_vote(1, "PRECOMMIT", 1)
        else:
            raise ValueError(f"unknown model action {action.kind}")
    finally:
        loop.admission = None


def protocol_state(loop: CoupledTrace) -> dict[str, Any]:
    """Canonical complete guard state, without opaque IDs or audit timestamps.

    Envelope numbers depend on emission order but no protocol guard observes
    those numbers.  Their semantic endpoints/message/status are preserved,
    including the multiplicity of copies.  A message ID encodes its complete
    signed payload, and signatures are deterministic functions of that payload.
    """
    replicas = {}
    for name, state in loop.replicas.items():
        replicas[name] = {
            "height": state.height, "round": state.round, "step": state.step,
            "lock": (state.locked_value, state.locked_round),
            "valid": (state.valid_value, state.valid_round),
            "proposal": (state.proposal_id, state.proposal_block),
            "known_blocks": sorted(state.known_blocks),
            "commit": (state.commit_value, state.commit_round, state.committed),
            "signed_votes": sorted(state.signed_votes.values()),
            "received_votes": sorted(state.received_votes.values()),
            "received_messages": sorted(state.received_messages),
            "timers": sorted(state.timers),
        }
    return {
        "replicas": replicas,
        "messages": sorted(loop.messages),
        "envelopes": sorted((envelope.sender, envelope.receiver, envelope.message_id, envelope.status)
                            for envelope in loop.envelopes.values()),
    }


def _canonical(stage: int, remaining: int, loop: CoupledTrace, *, audit_order: bool) -> str:
    state = {"stage": stage, "remaining": remaining, "protocol": protocol_state(loop)}
    if audit_order:
        state["first_round0_prevote_peer"] = loop.first_round0_prevote_peer
    return json.dumps(state, sort_keys=True, separators=(",", ":"))


def unsafe(loop: CoupledTrace) -> bool:
    # P contains the declared lock-update mutation.  The observation requires
    # the two unmutated observers themselves to disagree; P alone cannot make
    # this goal true.
    values = {loop.replicas[name].committed for name in ("A", "C")
              if loop.replicas[name].committed is not None}
    return len(values) > 1


def advance(stage: int, remaining: int, action_index: int) -> tuple[int, int]:
    remaining &= ~(1 << action_index)
    if remaining == 0:
        stage += 1
        remaining = (1 << len(STAGES[stage])) - 1 if stage < len(STAGES) else 0
    return stage, remaining


@dataclass
class ModelGraph:
    problem: Problem
    variant: str
    semantic_keys: tuple[str, ...]
    snapshots: tuple[dict[str, Any], ...]
    edge_actions: tuple[tuple[int, int], ...]
    stage_counts: tuple[int, ...]

    def summary(self) -> dict[str, Any]:
        return {
            "variant": self.variant, "states": len(self.problem.states),
            "transitions": len(self.problem.transitions), "unsafe_states": len(self.problem.unsafe),
            "stages": len(STAGES), "opportunity_bound": OPPORTUNITY_BOUND,
            "states_by_stage": list(self.stage_counts), "complete": True,
            "fine_keys": list(FINE_KEYS), "coarse_fibres": list(FIBRES),
            "input_sha256": self.problem.digest(),
        }


def build_model(variant: str = "MISSING_LOCK_UPDATE", *, costs: tuple[int, int] = (5, 2),
                max_states: int = 100_000, retain_audit_order: bool = True) -> ModelGraph:
    """Enumerate every successor in the declared domain, or raise unknown.

    No protocol frontier is interpreted as a safe terminal.  Only exhaustion
    of all 32 declared opportunity slots reaches the final environment stage.
    The state limit is a resource limit and never returns a partial Problem.
    """
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be a positive integer")
    if len(costs) != len(FIBRES):
        raise ValueError("the coupled model declares exactly two coarse-fibre costs")
    initial = CoupledTrace(variant)
    first_remaining = (1 << len(STAGES[0])) - 1
    seen = {_canonical(0, first_remaining, initial, audit_order=retain_audit_order): 0}
    queue = deque([(0, 0, first_remaining, initial)])
    names = ["q0:" + sha256(next(iter(seen)).encode()).hexdigest()[:16]]
    semantic_keys = [_canonical(0, first_remaining, initial, audit_order=False)]
    snapshots = [{"stage": 0, "remaining": first_remaining, "protocol": protocol_state(initial),
                  "first_round0_prevote_peer": initial.first_round0_prevote_peer}]
    stages = [0] * (len(STAGES) + 1)
    stages[0] = 1
    bad = set()
    transitions = []
    edge_actions = []
    while queue:
        source, stage, remaining, loop = queue.popleft()
        if unsafe(loop):
            bad.add(source)
        if stage == len(STAGES):
            continue
        for action_index, action in enumerate(STAGES[stage]):
            if not remaining >> action_index & 1:
                continue
            key = action_key(loop, action)
            for value in ((None,) if key is None else (False, True)):
                target_loop = deepcopy(loop)
                apply_action(target_loop, action, value)
                target_stage, target_remaining = advance(stage, remaining, action_index)
                canonical = _canonical(target_stage, target_remaining, target_loop,
                                       audit_order=retain_audit_order)
                target = seen.get(canonical)
                if target is None:
                    if len(seen) >= max_states:
                        raise EnumerationLimit(
                            f"unknown: {max_states} state limit; {len(queue) + 1} unexpanded states; "
                            "no complete transition graph was returned")
                    target = len(names)
                    seen[canonical] = target
                    names.append(f"q{target}:" + sha256(canonical.encode()).hexdigest()[:16])
                    semantic_keys.append(_canonical(target_stage, target_remaining, target_loop,
                                                    audit_order=False))
                    snapshots.append({"stage": target_stage, "remaining": target_remaining,
                                      "protocol": protocol_state(target_loop),
                                      "first_round0_prevote_peer": target_loop.first_round0_prevote_peer})
                    stages[target_stage] += 1
                    queue.append((target, target_stage, target_remaining, target_loop))
                suffix = "" if value is None else (":admit" if value else ":suppress")
                transitions.append(Transition(source, target, key, value,
                                              f"stage{stage}:{action.label}{suffix}"))
                edge_actions.append((stage, action_index))
    return ModelGraph(Problem(tuple(names), 0, frozenset(bad), tuple(transitions),
                              KEY_FIBRES, costs), variant, tuple(semantic_keys),
                      tuple(snapshots), tuple(edge_actions), tuple(stages))


def quotient_audit_order(model: ModelGraph) -> tuple[Problem, tuple[int, ...]]:
    """Forget only the irrelevant first-prevote-peer audit field."""
    classes: dict[str, int] = {}
    state_map = []
    for key in model.semantic_keys:
        state_map.append(classes.setdefault(key, len(classes)))
    edges = sorted({(state_map[edge.source], state_map[edge.target],
                    -1 if edge.key is None else edge.key,
                    -1 if edge.value is None else int(edge.value), edge.label)
                   for edge in model.problem.transitions})
    abstract = Problem(
        tuple(f"a{i}:" + sha256(key.encode()).hexdigest()[:16] for key, i in classes.items()),
        state_map[model.problem.initial], frozenset(state_map[state] for state in model.problem.unsafe),
        tuple(Transition(a, b, None if key == -1 else key,
                         None if bit == -1 else bool(bit), label)
              for a, b, key, bit, label in edges), model.problem.key_fibres, model.problem.costs,
        model.problem.allowed_split, model.problem.required_split)
    return abstract, tuple(state_map)


def replay_protocol_witness(model: ModelGraph, edge_indices: Iterable[int],
                            policy: Iterable[bool]) -> dict[str, Any]:
    """Re-execute the selected schedule with full signatures and guard audits."""
    loop = CoupledTrace(model.variant, retain_log=True)
    loop.total_policy = tuple(policy)
    if len(loop.total_policy) != len(FINE_KEYS) or any(type(bit) is not bool for bit in loop.total_policy):
        raise ValueError("the witness must supply one Boolean per fine key")
    source = model.problem.initial
    stage, remaining = 0, 1
    schedule = []
    for edge_index in edge_indices:
        if (type(edge_index) is not int or edge_index < 0
                or edge_index >= len(model.problem.transitions)):
            raise ValueError("witness transition indices must be nonnegative integers in range")
        edge = model.problem.transitions[edge_index]
        if edge.source != source:
            raise ValueError("noncontiguous witness path")
        action_stage, action_index = model.edge_actions[edge_index]
        if action_stage != stage or not remaining >> action_index & 1:
            raise ValueError("witness leaves the declared opportunity language")
        action = STAGES[stage][action_index]
        actual_key = action_key(loop, action)
        if actual_key != edge.key or (actual_key is not None
                                     and loop.total_policy[actual_key] != edge.value):
            raise ValueError("witness admission is not its fixed fine-key policy")
        apply_action(loop, action, edge.value)
        stage, remaining = advance(stage, remaining, action_index)
        canonical = _canonical(stage, remaining, loop, audit_order=False)
        if canonical != model.semantic_keys[edge.target]:
            raise ValueError("protocol replay does not reproduce the graph's successor")
        schedule.append({"edge": edge_index, "action": action.label, "key": actual_key,
                         "value": edge.value})
        source = edge.target
    record = execution_record(loop)
    record["audit"]["replayed_protocol_state_matches_every_graph_successor"] = True
    record["schedule"] = schedule
    return record


def execution_record(loop: CoupledTrace) -> dict[str, Any]:
    """Export actual signed evidence and audits for a fully logged execution."""
    if not loop.retain_log or loop.total_policy is None:
        raise ValueError("a full protocol audit needs its log and total policy")
    audits = loop.audit()
    # That original trace audit assumes only B->P is controlled.  This model
    # controls A->P too, so state this replacement explicitly.
    audits.pop("all_other_transport_edges_have_type_uniform_delivery")
    audits["every_resolved_envelope_matches_full_declared_admission_policy"] = all(
        (envelope.status == "DELIVERED") == loop._admitted(envelope, loop.messages[envelope.message_id])
        for envelope in loop.envelopes.values() if envelope.status != "BUFFERED")
    observed: dict[int, set[bool]] = {}
    for envelope in loop.envelopes.values():
        if envelope.status == "BUFFERED":
            continue
        key = loop.fine_key(envelope, loop.messages[envelope.message_id])
        if key is not None:
            observed.setdefault(key, set()).add(envelope.status == "DELIVERED")
    audits["each_observed_fine_key_has_one_static_value"] = all(len(values) == 1
                                                               for values in observed.values())
    decisions = {name: loop.replicas[name].committed for name in CORRECT
                 if loop.replicas[name].committed is not None}
    return {"unsafe": unsafe(loop), "decisions": decisions, "audit": audits,
            "certificates": loop.certificates,
            "messages": [asdict(message) for message in loop.messages.values()],
            "log": loop.log}


def run_policy_schedule(policy: tuple[bool, ...], *, variant: str = "MISSING_LOCK_UPDATE",
                        stage_orders: dict[int, tuple[int, ...]] | None = None) -> CoupledTrace:
    """Run a declared ordering for state/order boundary controls."""
    if len(policy) != len(FINE_KEYS) or any(type(bit) is not bool for bit in policy):
        raise ValueError("one strict Boolean per fine key is required")
    orders = {} if stage_orders is None else stage_orders
    if any(type(stage) is not int or stage < 0 or stage >= len(STAGES) for stage in orders):
        raise ValueError("stage order names a nonexistent stage")
    loop = CoupledTrace(variant, retain_log=True)
    loop.total_policy = policy
    for stage, actions in enumerate(STAGES):
        order = orders.get(stage, tuple(range(len(actions))))
        if (len(order) != len(actions) or any(type(index) is not int for index in order)
                or set(order) != set(range(len(actions)))):
            raise ValueError("a stage order must permute all of its opportunity slots")
        for index in order:
            action = actions[index]
            key = action_key(loop, action)
            apply_action(loop, action, None if key is None else policy[key])
    return loop


def exhaustive_policy_oracle(problem: Problem) -> dict[str, Any]:
    """Enumerate total policies AND split subsets, then ordinary reachability.

    Independent of product states, their cost function, and the optimizer.  A
    coarse fibre is legal precisely when its TOTAL policy is uniform or the
    explicitly enumerated split set contains that fibre.  Reachability uses
    only edge-labelled graph adjacency and the total assignment.
    """
    outgoing = [[] for _ in problem.states]
    for edge in problem.transitions:
        outgoing[edge.source].append(edge)
    minimum = None
    policy_count = compatible_pairs = feasible_pairs = 0
    reachable_counts = []
    for bits in itertools.product((False, True), repeat=len(problem.key_fibres)):
        policy_count += 1
        reached = {problem.initial}
        pending = [problem.initial]
        while pending:
            state = pending.pop()
            for edge in outgoing[state]:
                if edge.key is not None and bits[edge.key] != edge.value:
                    continue
                if edge.target not in reached:
                    reached.add(edge.target)
                    pending.append(edge.target)
        is_unsafe = not problem.unsafe.isdisjoint(reached)
        reachable_counts.append(len(reached))
        for mask in range(1 << len(problem.costs)):
            split = {index for index in range(len(problem.costs)) if mask >> index & 1}
            if not problem.required_split <= split <= problem.allowed_split:
                continue
            uniform = True
            for fibre in range(len(problem.costs)):
                if fibre not in split:
                    values = {bits[key] for key, owner in enumerate(problem.key_fibres)
                              if owner == fibre}
                    if len(values) > 1:
                        uniform = False
                        break
            if not uniform:
                continue
            compatible_pairs += 1
            if is_unsafe:
                feasible_pairs += 1
                cost = sum(problem.costs[index] for index in split)
                minimum = cost if minimum is None else min(minimum, cost)
    return {"minimum_cost": minimum, "total_policies": policy_count,
            "compatible_policy_split_pairs": compatible_pairs,
            "unsafe_policy_split_pairs": feasible_pairs,
            "minimum_reachable_states": min(reachable_counts),
            "maximum_reachable_states": max(reachable_counts)}


def direct_policy_reachability(variant: str, policy: tuple[bool, ...], *,
                               max_states: int = 100_000) -> dict[str, int | bool]:
    """Check one total policy by generating guarded successors afresh.

    This check does not traverse the exported graph or call the optimizer.
    It validates graph construction separately from policy/cost optimization.
    """
    if len(policy) != len(FINE_KEYS) or any(type(bit) is not bool for bit in policy):
        raise ValueError("one Boolean per fine key is required")
    loop = CoupledTrace(variant)
    loop.total_policy = policy
    pending = deque([(0, 1, loop)])
    seen = {_canonical(0, 1, loop, audit_order=False)}
    bad = False
    transitions = 0
    while pending:
        stage, remaining, current = pending.popleft()
        bad |= unsafe(current)
        if stage == len(STAGES):
            continue
        for index, action in enumerate(STAGES[stage]):
            if not remaining >> index & 1:
                continue
            following = deepcopy(current)
            key = action_key(current, action)
            apply_action(following, action, None if key is None else policy[key])
            next_stage, next_remaining = advance(stage, remaining, index)
            canonical = _canonical(next_stage, next_remaining, following, audit_order=False)
            transitions += 1
            if canonical not in seen:
                if len(seen) >= max_states:
                    raise EnumerationLimit("unknown: direct-policy enumeration reached its state limit")
                seen.add(canonical)
                pending.append((next_stage, next_remaining, following))
    return {"unsafe": bad, "states": len(seen), "transitions": transitions}


def graph_policy_reachability(problem: Problem, policy: tuple[bool, ...]) -> dict[str, int | bool]:
    """Plain graph reachability for comparison with direct protocol execution."""
    outgoing = [[] for _ in problem.states]
    for edge in problem.transitions:
        outgoing[edge.source].append(edge)
    seen = {problem.initial}
    pending = [problem.initial]
    transitions = 0
    while pending:
        for edge in outgoing[pending.pop()]:
            if edge.key is not None and policy[edge.key] != edge.value:
                continue
            transitions += 1
            if edge.target not in seen:
                seen.add(edge.target)
                pending.append(edge.target)
    return {"unsafe": not problem.unsafe.isdisjoint(seen), "states": len(seen),
            "transitions": transitions}


def semantic_examples() -> dict[str, Problem]:
    """Small non-pivot boundaries, including cycles and repeated fine keys."""
    return {
        "static_key_cycle": Problem(
            ("start", "after_admit", "unsafe"), 0, frozenset({2}),
            (Transition(0, 1, 0, True, "first use admits"),
             Transition(1, 2, 0, False, "same fine key would need to suppress"),
             Transition(1, 0, label="retry cycle")), (0,), (4,)),
        "three_phase_paid_once": Problem(
            ("start", "prepared", "repair_suppressed", "repeated", "unsafe"), 0, frozenset({4}),
            (Transition(0, 1, 0, True), Transition(1, 2, 1, False),
             Transition(2, 3, 2, True), Transition(3, 4, 0, True)), (0, 0, 0), (7,)),
        "dependent_cost_choice": Problem(
            ("start", "a_ready", "both_ready", "left_suppressed", "right_suppressed", "unsafe"),
            0, frozenset({5}),
            (Transition(0, 1, 0, True, "first contribution"),
             Transition(1, 2, 2, True, "second contribution enables shared certificate"),
             Transition(2, 3, 1, False, "suppress left repair"),
             Transition(2, 4, 3, False, "suppress right repair"),
             Transition(3, 5, 3, True, "right contribution enables timeout"),
             Transition(4, 5, 1, True, "left contribution enables timeout")),
            (0, 0, 1, 1), (5, 2)),
        "required_unused_fibre": Problem(
            ("start", "unsafe"), 0, frozenset({1}), (Transition(0, 1),),
            (0, 0, 1), (3, 8), required_split=frozenset({1})),
        "zero_cost_split": Problem(
            ("start", "enabled", "unsafe"), 0, frozenset({2}),
            (Transition(0, 1, 0, True), Transition(1, 2, 1, False)), (0, 0), (0,)),
        "spurious_state_merge": Problem(
            ("start", "prepared", "unsafe"), 0, frozenset({2}),
            (Transition(0, 1, 0, True, "prepare"),
             Transition(1, 2, 1, False, "suppress repair")), (0, 0), (3,)),
    }


def spurious_quotient(problem: Problem) -> tuple[Problem, tuple[int, ...]]:
    """A legal overapproximation that loses the prepare-before-repair guard."""
    if problem != semantic_examples()["spurious_state_merge"]:
        raise ValueError("this demonstrator expects its declared three-state input")
    return Problem(("start_or_prepared", "unsafe"), 0, frozenset({1}),
                   (Transition(0, 0, 0, True, "prepare"),
                    Transition(0, 1, 1, False, "suppress repair")), (0, 0), (3,)), (0, 0, 1)


def restrict_problem(problem: Problem, *, allowed: frozenset[int] | None = None,
                     required: frozenset[int] = frozenset()) -> Problem:
    return replace(problem, allowed_split=problem.allowed_split if allowed is None else allowed,
                   required_split=required)
