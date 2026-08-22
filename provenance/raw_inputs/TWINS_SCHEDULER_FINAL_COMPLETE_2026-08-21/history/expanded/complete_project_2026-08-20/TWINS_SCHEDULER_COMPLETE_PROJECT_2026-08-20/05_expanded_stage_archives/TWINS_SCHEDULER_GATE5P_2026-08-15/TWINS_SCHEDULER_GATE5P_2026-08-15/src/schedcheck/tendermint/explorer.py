from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from typing import Iterable

from schedcheck.tendermint.cases import ExperimentCase
from schedcheck.tendermint.kernel import (
    STAGE_COUNT,
    complete_stage,
    deliver,
    deliver_late_certificate,
    emit_stage,
    finish_view,
    initial_runtime,
)
from schedcheck.tendermint.model import (
    HONEST_NODES,
    Grammar,
    KernelMessage,
    KernelState,
    KernelWitness,
    MessageKind,
    StageDelivery,
    Variant,
    VariantName,
    ViewPlan,
    ViewRuntime,
    ViewTrace,
)


@dataclass(frozen=True, slots=True)
class PolicyMemory:
    partition_mask: int | None = None
    outbound_mask: int | None = None
    inbound_mask: int | None = None
    defer_commit_mask: int | None = None
    type_masks: tuple[tuple[str, int], ...] = ()

    def type_mask(self, kind: MessageKind) -> int | None:
        key = kind.value
        for stored_kind, mask in self.type_masks:
            if stored_kind == key:
                return mask
        return None

    def with_type_mask(self, kind: MessageKind, mask: int) -> "PolicyMemory":
        mapping = dict(self.type_masks)
        mapping[kind.value] = mask
        return PolicyMemory(
            partition_mask=self.partition_mask,
            outbound_mask=self.outbound_mask,
            inbound_mask=self.inbound_mask,
            defer_commit_mask=self.defer_commit_mask,
            type_masks=tuple(sorted(mapping.items())),
        )

    def descriptor(self, grammar: Grammar, leader: str) -> str:
        if grammar == Grammar.PARTITION:
            return f"connected({leader})={_mask_nodes(self.partition_mask or 0)}"
        if grammar == Grammar.DIRECTED:
            return (
                f"out({leader})={_mask_nodes(self.outbound_mask or 0)};"
                f"in({leader})={_mask_nodes(self.inbound_mask or 0)}"
            )
        if grammar == Grammar.DIRECTED_DELAY1:
            return (
                f"out({leader})={_mask_nodes(self.outbound_mask or 0)};"
                f"in({leader})={_mask_nodes(self.inbound_mask or 0)};"
                f"defer_commit={_mask_nodes(self.defer_commit_mask or 0)}"
            )
        if grammar == Grammar.TYPE_SPECIFIC:
            return ";".join(
                f"{kind}={_mask_nodes(mask)}" for kind, mask in self.type_masks
            ) or "EMPTY"
        return grammar.value


@dataclass(frozen=True, slots=True)
class ViewSearchNode:
    runtime: ViewRuntime
    memory: PolicyMemory
    stages: tuple[StageDelivery, ...]
    deferred: tuple[KernelMessage, ...] = ()

    def rank(self) -> tuple[int, int, tuple[str, ...]]:
        delivered = sum(stage.delivered_count for stage in self.stages)
        tokens = tuple(
            token
            for stage in self.stages
            for token in (
                stage.delivered
                + tuple(f"DEFER:{item}" for item in stage.deferred)
            )
        )
        return (delivered, len(tokens), tokens)


@dataclass(frozen=True, slots=True)
class ViewOutcome:
    state: KernelState
    trace: ViewTrace
    deferred: tuple[KernelMessage, ...] = ()

    def rank(self) -> tuple[int, int, tuple[str, ...]]:
        tokens = tuple(
            token
            for stage in self.trace.stages
            for token in (
                stage.delivered
                + tuple(f"DEFER:{item}" for item in stage.deferred)
            )
        )
        return (self.trace.delivered_count, len(tokens), tokens)


@dataclass(slots=True)
class SearchStats:
    view_calls: int = 0
    symbolic_nodes: int = 0
    delivery_choices: int = 0
    view_outcomes: int = 0

    def add(self, other: "SearchStats") -> None:
        self.view_calls += other.view_calls
        self.symbolic_nodes += other.symbolic_nodes
        self.delivery_choices += other.delivery_choices
        self.view_outcomes += other.view_outcomes


@dataclass(slots=True)
class CaseResult:
    case_id: str
    variant: VariantName
    grammar: Grammar
    states: set[KernelState]
    observations: set[tuple[int | None, ...]]
    witnesses: dict[tuple[int | None, ...], KernelWitness]
    stats: SearchStats

    @property
    def unsafe_observations(self) -> set[tuple[int | None, ...]]:
        return {
            observation
            for observation in self.observations
            if len({value for value in observation if value is not None}) > 1
        }


def _mask_nodes(mask: int) -> str:
    nodes = [node for index, node in enumerate(HONEST_NODES) if mask & (1 << index)]
    return "{" + ",".join(nodes) + "}" if nodes else "{}"


def _message_honest_index(message: KernelMessage, leader: str) -> int:
    node = message.receiver if message.sender == leader else message.sender
    try:
        return HONEST_NODES.index(node)
    except ValueError as error:
        raise ValueError(f"message is not on the leader/honest star: {message}") from error


def _message_allowed_by_memory(
    message: KernelMessage,
    grammar: Grammar,
    leader: str,
    memory: PolicyMemory,
) -> bool:
    index = _message_honest_index(message, leader)
    bit = 1 << index
    outbound = message.sender == leader

    if grammar == Grammar.PARTITION:
        return bool((memory.partition_mask or 0) & bit)
    if grammar in (Grammar.DIRECTED, Grammar.DIRECTED_DELAY1):
        mask = memory.outbound_mask if outbound else memory.inbound_mask
        return bool((mask or 0) & bit)
    if grammar == Grammar.TYPE_SPECIFIC:
        return bool((memory.type_mask(message.kind) or 0) & bit)
    raise ValueError(f"grammar has no static memory predicate: {grammar}")


def _initial_memories(grammar: Grammar) -> Iterable[PolicyMemory]:
    if grammar == Grammar.PARTITION:
        for mask in range(8):
            yield PolicyMemory(partition_mask=mask)
        return
    if grammar == Grammar.DIRECTED:
        for outbound_mask in range(8):
            for inbound_mask in range(8):
                yield PolicyMemory(
                    outbound_mask=outbound_mask,
                    inbound_mask=inbound_mask,
                )
        return
    if grammar == Grammar.DIRECTED_DELAY1:
        for outbound_mask in range(8):
            for inbound_mask in range(8):
                for defer_commit_mask in range(8):
                    if defer_commit_mask & ~outbound_mask:
                        continue
                    yield PolicyMemory(
                        outbound_mask=outbound_mask,
                        inbound_mask=inbound_mask,
                        defer_commit_mask=defer_commit_mask,
                    )
        return
    yield PolicyMemory()


def _assign_type_masks(
    memory: PolicyMemory,
    messages: tuple[KernelMessage, ...],
) -> Iterable[PolicyMemory]:
    unassigned = tuple(
        sorted(
            {
                message.kind
                for message in messages
                if memory.type_mask(message.kind) is None
            },
            key=lambda kind: kind.value,
        )
    )
    if not unassigned:
        yield memory
        return
    for masks in product(range(8), repeat=len(unassigned)):
        updated = memory
        for kind, mask in zip(unassigned, masks, strict=True):
            updated = updated.with_type_mask(kind, mask)
        yield updated


def _subset_sequences(messages: tuple[KernelMessage, ...]) -> Iterable[tuple[KernelMessage, ...]]:
    ordered = tuple(sorted(messages, key=lambda message: message.uid))
    for mask in range(1 << len(ordered)):
        yield tuple(
            message
            for index, message in enumerate(ordered)
            if mask & (1 << index)
        )


def _replay_sequences(messages: tuple[KernelMessage, ...]) -> Iterable[tuple[KernelMessage, ...]]:
    ordered = tuple(sorted(messages, key=lambda message: message.uid))
    if ordered and all(
        message.kind in (MessageKind.PREVOTE, MessageKind.PRECOMMIT)
        for message in ordered
    ):
        for multiplicities in product(range(3), repeat=len(ordered)):
            delivered: list[KernelMessage] = []
            for message, multiplicity in zip(ordered, multiplicities, strict=True):
                delivered.extend([message] * multiplicity)
            yield tuple(delivered)
        return
    yield from _subset_sequences(ordered)


def _delivery_choices(
    node: ViewSearchNode,
    messages: tuple[KernelMessage, ...],
    grammar: Grammar,
    leader: str,
) -> Iterable[
    tuple[PolicyMemory, tuple[KernelMessage, ...], tuple[KernelMessage, ...]]
]:
    if grammar in (Grammar.PARTITION, Grammar.DIRECTED):
        delivered = tuple(
            message
            for message in sorted(messages, key=lambda item: item.uid)
            if _message_allowed_by_memory(message, grammar, leader, node.memory)
        )
        yield node.memory, delivered, ()
        return

    if grammar == Grammar.DIRECTED_DELAY1:
        admitted = tuple(
            message
            for message in sorted(messages, key=lambda item: item.uid)
            if _message_allowed_by_memory(message, grammar, leader, node.memory)
        )
        delivered: list[KernelMessage] = []
        deferred: list[KernelMessage] = []
        for message in admitted:
            index = _message_honest_index(message, leader)
            can_defer = message.kind in (
                MessageKind.COMMIT,
                MessageKind.FORGED_COMMIT,
            )
            should_defer = bool(
                (node.memory.defer_commit_mask or 0) & (1 << index)
            )
            if can_defer and should_defer:
                deferred.append(message)
            else:
                delivered.append(message)
        yield node.memory, tuple(delivered), tuple(deferred)
        return

    if grammar == Grammar.TYPE_SPECIFIC:
        for memory in _assign_type_masks(node.memory, messages):
            delivered = tuple(
                message
                for message in sorted(messages, key=lambda item: item.uid)
                if _message_allowed_by_memory(message, grammar, leader, memory)
            )
            yield memory, delivered, ()
        return

    if grammar == Grammar.PER_MESSAGE:
        for delivered in _subset_sequences(messages):
            yield node.memory, delivered, ()
        return

    if grammar == Grammar.PER_MESSAGE_REPLAY1:
        for delivered in _replay_sequences(messages):
            yield node.memory, delivered, ()
        return

    raise ValueError(grammar)


def _apply_delivery_sequence(
    runtime: ViewRuntime,
    sequence: tuple[KernelMessage, ...],
    plan: ViewPlan,
    variant: Variant,
) -> ViewRuntime:
    current = runtime
    for message in sequence:
        current = deliver(current, message, plan, variant)
    return current


def explore_view(
    state: KernelState,
    plan: ViewPlan,
    variant: Variant,
    grammar: Grammar,
) -> tuple[
    dict[tuple[KernelState, tuple[KernelMessage, ...]], ViewOutcome],
    SearchStats,
]:
    stats = SearchStats(view_calls=1)
    frontier: dict[
        tuple[ViewRuntime, PolicyMemory, tuple[KernelMessage, ...]],
        ViewSearchNode,
    ] = {}
    for memory in _initial_memories(grammar):
        node = ViewSearchNode(initial_runtime(state), memory, ())
        frontier[(node.runtime, node.memory, node.deferred)] = node

    for stage in range(STAGE_COUNT):
        next_frontier: dict[
            tuple[ViewRuntime, PolicyMemory, tuple[KernelMessage, ...]],
            ViewSearchNode,
        ] = {}
        for node in frontier.values():
            stats.symbolic_nodes += 1
            messages = emit_stage(node.runtime, plan, stage, variant)
            emitted_tokens = tuple(message.token() for message in messages)
            for memory, sequence, deferred in _delivery_choices(
                node, messages, grammar, plan.leader
            ):
                stats.delivery_choices += 1
                runtime = _apply_delivery_sequence(
                    node.runtime, sequence, plan, variant
                )
                runtime = complete_stage(runtime, stage, variant)
                delivery = StageDelivery(
                    stage=stage,
                    emitted=emitted_tokens,
                    delivered=tuple(message.token() for message in sequence),
                    deferred=tuple(message.token() for message in deferred),
                )
                candidate = ViewSearchNode(
                    runtime=runtime,
                    memory=memory,
                    stages=node.stages + (delivery,),
                    deferred=node.deferred + deferred,
                )
                key = (candidate.runtime, candidate.memory, candidate.deferred)
                previous = next_frontier.get(key)
                if previous is None or candidate.rank() < previous.rank():
                    next_frontier[key] = candidate
        frontier = next_frontier

    outcomes: dict[
        tuple[KernelState, tuple[KernelMessage, ...]], ViewOutcome
    ] = {}
    for node in frontier.values():
        end_state = finish_view(node.runtime)
        trace = ViewTrace(
            view=plan.view,
            leader=plan.leader,
            value=plan.value,
            policy=node.memory.descriptor(grammar, plan.leader),
            stages=node.stages,
        )
        candidate = ViewOutcome(end_state, trace, node.deferred)
        key = (end_state, node.deferred)
        previous = outcomes.get(key)
        if previous is None or candidate.rank() < previous.rank():
            outcomes[key] = candidate
    stats.view_outcomes = len(outcomes)
    return outcomes, stats


def _witness_rank(witness: KernelWitness) -> tuple[int, int, tuple[str, ...]]:
    return witness.rank()


def explore_case(
    case: ExperimentCase,
    variant: Variant,
    grammar: Grammar,
) -> CaseResult:
    if grammar == Grammar.DIRECTED_DELAY1:
        return _explore_case_delay1(case, variant)

    initial = KernelState()
    initial_witness = KernelWitness(
        case_id=case.case_id,
        variant=variant.name,
        grammar=grammar,
        observation=initial.observation(),
        views=(),
    )
    frontier: dict[KernelState, KernelWitness] = {initial: initial_witness}
    stats = SearchStats()

    for plan in case.plans:
        next_frontier: dict[KernelState, KernelWitness] = {}
        cache: dict[
            KernelState,
            tuple[
                dict[tuple[KernelState, tuple[KernelMessage, ...]], ViewOutcome],
                SearchStats,
            ],
        ] = {}
        for state, prefix in frontier.items():
            if state not in cache:
                cache[state] = explore_view(state, plan, variant, grammar)
            outcomes, view_stats = cache[state]
            stats.add(view_stats)
            for outcome in outcomes.values():
                if outcome.deferred:
                    raise AssertionError(
                        f"non-delay grammar produced deferred messages: {grammar}"
                    )
                end_state = outcome.state
                witness = KernelWitness(
                    case_id=case.case_id,
                    variant=variant.name,
                    grammar=grammar,
                    observation=end_state.observation(),
                    views=prefix.views + (outcome.trace,),
                )
                previous = next_frontier.get(end_state)
                if previous is None or _witness_rank(witness) < _witness_rank(previous):
                    next_frontier[end_state] = witness
        frontier = next_frontier

    observations = {state.observation() for state in frontier}
    witnesses: dict[tuple[int | None, ...], KernelWitness] = {}
    for state, witness in frontier.items():
        observation = state.observation()
        previous = witnesses.get(observation)
        if previous is None or _witness_rank(witness) < _witness_rank(previous):
            witnesses[observation] = witness

    return CaseResult(
        case_id=case.case_id,
        variant=variant.name,
        grammar=grammar,
        states=set(frontier),
        observations=observations,
        witnesses=witnesses,
        stats=stats,
    )


def _explore_case_delay1(
    case: ExperimentCase,
    variant: Variant,
) -> CaseResult:
    """Explore one-view delayed commit evidence under a directed view graph.

    A certificate admitted in view ``v`` may be held and is delivered only
    after the normal stages of view ``v+1``. This deliberately isolates the
    temporal power of bounded late delivery from message-type filtering. A
    certificate deferred in the last bounded view remains pending and is not
    observed within the experiment horizon.
    """

    grammar = Grammar.DIRECTED_DELAY1
    initial = KernelState()
    initial_witness = KernelWitness(
        case_id=case.case_id,
        variant=variant.name,
        grammar=grammar,
        observation=initial.observation(),
        views=(),
    )
    frontier: dict[
        tuple[KernelState, tuple[KernelMessage, ...]], KernelWitness
    ] = {(initial, ()): initial_witness}
    stats = SearchStats()

    for plan in case.plans:
        next_frontier: dict[
            tuple[KernelState, tuple[KernelMessage, ...]], KernelWitness
        ] = {}
        cache: dict[
            KernelState,
            tuple[
                dict[tuple[KernelState, tuple[KernelMessage, ...]], ViewOutcome],
                SearchStats,
            ],
        ] = {}
        for (state, pending), prefix in frontier.items():
            if state not in cache:
                cache[state] = explore_view(state, plan, variant, grammar)
            outcomes, view_stats = cache[state]
            stats.add(view_stats)
            for outcome in outcomes.values():
                end_state = outcome.state
                for message in pending:
                    end_state = deliver_late_certificate(end_state, message, variant)
                trace = replace(
                    outcome.trace,
                    late_delivered=tuple(message.token() for message in pending),
                )
                witness = KernelWitness(
                    case_id=case.case_id,
                    variant=variant.name,
                    grammar=grammar,
                    observation=end_state.observation(),
                    views=prefix.views + (trace,),
                )
                key = (end_state, outcome.deferred)
                previous = next_frontier.get(key)
                if previous is None or _witness_rank(witness) < _witness_rank(previous):
                    next_frontier[key] = witness
        frontier = next_frontier

    states = {state for state, _pending in frontier}
    observations = {state.observation() for state in states}
    witnesses: dict[tuple[int | None, ...], KernelWitness] = {}
    for (state, _pending), witness in frontier.items():
        observation = state.observation()
        previous = witnesses.get(observation)
        if previous is None or _witness_rank(witness) < _witness_rank(previous):
            witnesses[observation] = witness

    return CaseResult(
        case_id=case.case_id,
        variant=variant.name,
        grammar=grammar,
        states=states,
        observations=observations,
        witnesses=witnesses,
        stats=stats,
    )


def replay_witness(
    case: ExperimentCase,
    variant: Variant,
    witness: KernelWitness,
) -> KernelState:
    state = KernelState()
    pending: dict[str, KernelMessage] = {}
    plans = {plan.view: plan for plan in case.plans}
    for view_trace in witness.views:
        plan = plans[view_trace.view]
        runtime = initial_runtime(state)
        current_deferred: dict[str, KernelMessage] = {}
        for stage_delivery in view_trace.stages:
            messages = emit_stage(runtime, plan, stage_delivery.stage, variant)
            by_token = {message.token(): message for message in messages}
            delivered: list[KernelMessage] = []
            for token in stage_delivery.delivered:
                if token not in by_token:
                    raise AssertionError(f"witness token not emitted: {token}")
                delivered.append(by_token[token])
            for token in stage_delivery.deferred:
                if token not in by_token:
                    raise AssertionError(
                        f"deferred witness token not emitted: {token}"
                    )
                if token in stage_delivery.delivered:
                    raise AssertionError(f"token both delivered and deferred: {token}")
                current_deferred[token] = by_token[token]
            runtime = _apply_delivery_sequence(
                runtime, tuple(delivered), plan, variant
            )
            runtime = complete_stage(runtime, stage_delivery.stage, variant)
        state = finish_view(runtime)
        for token in view_trace.late_delivered:
            if token not in pending:
                raise AssertionError(f"late token was not pending: {token}")
            state = deliver_late_certificate(state, pending[token], variant)
        if set(view_trace.late_delivered) != set(pending):
            raise AssertionError(
                "delay-1 witness must deliver exactly the previous view's pending certificates"
            )
        pending = current_deferred
    return state


def stage_delivery_commutes(
    runtime: ViewRuntime,
    messages: tuple[KernelMessage, ...],
    plan: ViewPlan,
    variant: Variant,
) -> bool:
    """Check the declared order-reduction condition for one emitted stage.

    The Gate 4 kernel emits at most one protocol message per honest endpoint for
    each kind. Vote collection is completed only at the stage barrier. Therefore
    all permutations of a chosen subset should reach the same runtime.
    """
    from itertools import permutations

    for subset in _subset_sequences(messages):
        outcomes = {
            _apply_delivery_sequence(runtime, tuple(order), plan, variant)
            for order in permutations(subset)
        }
        if len(outcomes) > 1:
            return False
    return True
