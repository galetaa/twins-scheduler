from __future__ import annotations

from dataclasses import dataclass, replace

from schedcheck.model import Message, Observation
from schedcheck.protocols.base import FiniteProtocol


@dataclass(frozen=True, slots=True)
class InstanceOrderState:
    decision_a: int | None = None
    decision_b: int | None = None


class InstanceOrderProtocol(FiniteProtocol):
    """Minimal same-type message-instance/order safety separator.

    Two certificate instances of the same type are broadcast in canonical order.
    Static partition, directed, and type-specific grammars preserve FIFO order on
    each enabled link. A per-message scheduler can choose and reorder instances,
    making different replicas accept different first certificates.
    """

    name = "INSTANCE_ORDER"
    nodes = ("L", "A", "B")
    observed_nodes = ("A", "B")
    message_types = ("CERT",)
    phase_count = 1

    def initial_state(self) -> InstanceOrderState:
        return InstanceOrderState()

    def emit(self, state: InstanceOrderState, phase: int) -> tuple[Message, ...]:
        if phase != 0:
            raise ValueError(f"invalid phase {phase}")
        return (
            Message("cert0-a", 0, 0, "CERT", "L", "A", 0),
            Message("cert0-b", 0, 1, "CERT", "L", "B", 0),
            Message("cert1-a", 0, 2, "CERT", "L", "A", 1),
            Message("cert1-b", 0, 3, "CERT", "L", "B", 1),
        )

    def deliver(self, state: InstanceOrderState, message: Message) -> InstanceOrderState:
        if message.receiver == "A" and state.decision_a is None:
            return replace(state, decision_a=message.value)
        if message.receiver == "B" and state.decision_b is None:
            return replace(state, decision_b=message.value)
        return state

    def barrier(self, state: InstanceOrderState, phase: int) -> InstanceOrderState:
        return state

    def observation(self, state: InstanceOrderState) -> Observation:
        return Observation(self.observed_nodes, (state.decision_a, state.decision_b))
