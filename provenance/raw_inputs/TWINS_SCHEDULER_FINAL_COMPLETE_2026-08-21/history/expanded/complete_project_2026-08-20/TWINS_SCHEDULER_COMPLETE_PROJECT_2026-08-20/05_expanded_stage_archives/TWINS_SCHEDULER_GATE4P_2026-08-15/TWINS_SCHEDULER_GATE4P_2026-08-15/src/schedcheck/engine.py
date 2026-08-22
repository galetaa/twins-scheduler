from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

from schedcheck.grammars import (
    DirectedPolicy,
    PartitionPolicy,
    StaticPolicy,
    TypeSpecificPolicy,
    directed_policies,
    partition_policies,
    type_specific_policies,
)
from schedcheck.model import Event, Message, Observation, Witness
from schedcheck.protocols.base import FiniteProtocol


@dataclass(slots=True)
class LanguageResult:
    protocol: str
    grammar: str
    policy_count: int
    execution_count: int
    observations: set[Observation]
    witnesses: dict[Observation, Witness]

    @property
    def unsafe(self) -> set[Observation]:
        return {obs for obs in self.observations if obs.unsafe()}

    def record(self, witness: Witness) -> None:
        self.observations.add(witness.observation)
        previous = self.witnesses.get(witness.observation)
        if previous is None or witness.rank() < previous.rank():
            self.witnesses[witness.observation] = witness


def simulate_static(protocol: FiniteProtocol, policy: StaticPolicy) -> Witness:
    state: Hashable = protocol.initial_state()
    events: list[Event] = []
    delivered_by_phase: list[tuple[str, ...]] = []

    for phase in range(protocol.phase_count):
        messages = protocol.emit(state, phase)
        protocol.validate_messages(messages, phase)
        delivered: list[str] = []
        for message in sorted(messages, key=lambda msg: (msg.ordinal, msg.uid)):
            events.append(Event("EMIT", phase, message.token()))
            if policy.allows(message):
                state = protocol.deliver(state, message)
                delivered.append(message.uid)
                events.append(Event("DELIVER", phase, message.token()))
            else:
                events.append(Event("DROP", phase, message.token()))
        state = protocol.barrier(state, phase)
        events.append(Event("BARRIER", phase, protocol.observation(state).canonical_id()))
        delivered_by_phase.append(tuple(delivered))

    observation = protocol.observation(state)
    return Witness(
        grammar=policy.grammar,
        protocol=protocol.name,
        schedule_id=policy.schedule_id(),
        observation=observation,
        events=tuple(events),
        delivered_by_phase=tuple(delivered_by_phase),
        schedule_data=policy.schedule_data(),
    )


def enumerate_static_language(
    protocol: FiniteProtocol,
    grammar: str,
) -> LanguageResult:
    if grammar == "G_P_PARTITION":
        policies: Iterable[StaticPolicy] = partition_policies(protocol.nodes)
    elif grammar == "G_D_DIRECTED_VIEW":
        policies = directed_policies(protocol.edge_universe())
    elif grammar == "G_T_TYPE_SPECIFIC":
        policies = type_specific_policies(protocol.message_types, protocol.edge_universe())
    else:
        raise ValueError(f"unsupported static grammar: {grammar}")

    result = LanguageResult(protocol.name, grammar, 0, 0, set(), {})
    for policy in policies:
        result.policy_count += 1
        result.execution_count += 1
        result.record(simulate_static(protocol, policy))
    return result


def enumerate_per_message_language(protocol: FiniteProtocol) -> LanguageResult:
    grammar = "G_M_PER_MESSAGE"
    result = LanguageResult(protocol.name, grammar, 0, 0, set(), {})
    state0: Hashable = protocol.initial_state()

    def finish(
        state: Hashable,
        events: tuple[Event, ...],
        delivered_by_phase: tuple[tuple[str, ...], ...],
    ) -> None:
        result.execution_count += 1
        schedule_id = "/".join(
            f"p{phase}:[{','.join(messages)}]"
            for phase, messages in enumerate(delivered_by_phase)
        )
        result.record(
            Witness(
                grammar=grammar,
                protocol=protocol.name,
                schedule_id=schedule_id,
                observation=protocol.observation(state),
                events=events,
                delivered_by_phase=delivered_by_phase,
                schedule_data=(("delivery_sequence", schedule_id),),
            )
        )

    def explore_phase(
        phase: int,
        state: Hashable,
        events: tuple[Event, ...],
        delivered_by_phase: tuple[tuple[str, ...], ...],
    ) -> None:
        if phase >= protocol.phase_count:
            finish(state, events, delivered_by_phase)
            return

        messages = protocol.emit(state, phase)
        protocol.validate_messages(messages, phase)
        emit_events = tuple(Event("EMIT", phase, msg.token()) for msg in messages)

        def explore_pending(
            current_state: Hashable,
            remaining: tuple[Message, ...],
            current_events: tuple[Event, ...],
            delivered: tuple[str, ...],
        ) -> None:
            # Stop now: all remaining instances are dropped at the phase barrier.
            drop_events = tuple(Event("DROP", phase, msg.token()) for msg in remaining)
            barrier_state = protocol.barrier(current_state, phase)
            barrier_event = Event("BARRIER", phase, protocol.observation(barrier_state).canonical_id())
            explore_phase(
                phase + 1,
                barrier_state,
                current_events + drop_events + (barrier_event,),
                delivered_by_phase + (delivered,),
            )

            # Deliver any remaining instance next. This enumerates every ordered subset.
            for index, message in enumerate(remaining):
                next_state = protocol.deliver(current_state, message)
                next_remaining = remaining[:index] + remaining[index + 1 :]
                explore_pending(
                    next_state,
                    next_remaining,
                    current_events + (Event("DELIVER", phase, message.token()),),
                    delivered + (message.uid,),
                )

        explore_pending(state, messages, events + emit_events, ())

    explore_phase(0, state0, (), ())
    result.policy_count = result.execution_count
    return result


def enumerate_all_grammars(protocol: FiniteProtocol) -> dict[str, LanguageResult]:
    grammars = (
        "G_P_PARTITION",
        "G_D_DIRECTED_VIEW",
        "G_T_TYPE_SPECIFIC",
    )
    results = {grammar: enumerate_static_language(protocol, grammar) for grammar in grammars}
    results["G_M_PER_MESSAGE"] = enumerate_per_message_language(protocol)
    return results


def partition_to_directed(policy: PartitionPolicy) -> DirectedPolicy:
    edges: set[tuple[str, str]] = set()
    for block in policy.blocks:
        for sender in block:
            for receiver in block:
                if sender != receiver:
                    edges.add((sender, receiver))
    return DirectedPolicy(frozenset(edges))


def directed_to_type(policy: DirectedPolicy, message_types: tuple[str, ...]) -> TypeSpecificPolicy:
    return TypeSpecificPolicy(
        frozenset((kind, sender, receiver) for kind in message_types for sender, receiver in policy.edges)
    )
