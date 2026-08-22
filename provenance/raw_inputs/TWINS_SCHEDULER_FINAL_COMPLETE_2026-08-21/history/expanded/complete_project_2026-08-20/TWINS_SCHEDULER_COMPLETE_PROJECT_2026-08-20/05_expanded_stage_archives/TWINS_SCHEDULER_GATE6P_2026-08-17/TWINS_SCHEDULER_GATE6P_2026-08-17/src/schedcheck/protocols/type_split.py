from __future__ import annotations

from dataclasses import dataclass, replace

from schedcheck.model import Message, Observation
from schedcheck.protocols.base import FiniteProtocol


@dataclass(frozen=True, slots=True)
class TypeSplitState:
    decision_a: int | None = None
    decision_b: int | None = None


class TypeSplitProtocol(FiniteProtocol):
    """Minimal message-type safety separator.

    The coordinator emits a primary and a fallback certificate to both replicas.
    Each replica accepts the first certificate it receives. FIFO delivery of all
    messages on an enabled edge yields the primary value at every connected node;
    a type-specific scheduler can expose different certificate types to A and B.
    """

    name = "TYPE_SPLIT"
    nodes = ("L", "A", "B")
    observed_nodes = ("A", "B")
    message_types = ("PRIMARY_CERT", "FALLBACK_CERT")
    phase_count = 1

    def initial_state(self) -> TypeSplitState:
        return TypeSplitState()

    def emit(self, state: TypeSplitState, phase: int) -> tuple[Message, ...]:
        if phase != 0:
            raise ValueError(f"invalid phase {phase}")
        return (
            Message("primary-a", 0, 0, "PRIMARY_CERT", "L", "A", 0),
            Message("primary-b", 0, 1, "PRIMARY_CERT", "L", "B", 0),
            Message("fallback-a", 0, 2, "FALLBACK_CERT", "L", "A", 1),
            Message("fallback-b", 0, 3, "FALLBACK_CERT", "L", "B", 1),
        )

    def deliver(self, state: TypeSplitState, message: Message) -> TypeSplitState:
        if message.receiver == "A" and state.decision_a is None:
            return replace(state, decision_a=message.value)
        if message.receiver == "B" and state.decision_b is None:
            return replace(state, decision_b=message.value)
        return state

    def barrier(self, state: TypeSplitState, phase: int) -> TypeSplitState:
        return state

    def observation(self, state: TypeSplitState) -> Observation:
        return Observation(self.observed_nodes, (state.decision_a, state.decision_b))
