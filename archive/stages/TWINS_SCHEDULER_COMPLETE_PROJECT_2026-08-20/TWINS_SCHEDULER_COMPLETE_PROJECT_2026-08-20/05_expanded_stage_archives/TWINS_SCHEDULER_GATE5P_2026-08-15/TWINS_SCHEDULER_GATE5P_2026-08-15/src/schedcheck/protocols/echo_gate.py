from __future__ import annotations

from dataclasses import dataclass, replace

from schedcheck.model import Message, Observation
from schedcheck.protocols.base import FiniteProtocol


@dataclass(frozen=True, slots=True)
class EchoGateState:
    started_a: bool = False
    started_b: bool = False
    echo_at_a: bool = False
    echo_at_b: bool = False
    decision_a: int | None = None
    decision_b: int | None = None


class EchoGateProtocol(FiniteProtocol):
    """Minimal asymmetric-link safety separator.

    A coordinator starts A and B. A started replica emits an echo carrying its
    local preference. At the end of the view, a started replica that did not see
    the peer echo decides its own preference. The machine is intentionally
    unsafe under one-way or non-transitive delivery; it is a diagnostic model,
    not a production consensus protocol.
    """

    name = "ECHO_GATE"
    nodes = ("L", "A", "B")
    observed_nodes = ("A", "B")
    message_types = ("START", "ECHO")
    phase_count = 2

    def initial_state(self) -> EchoGateState:
        return EchoGateState()

    def emit(self, state: EchoGateState, phase: int) -> tuple[Message, ...]:
        if phase == 0:
            return (
                Message("start-a", 0, 0, "START", "L", "A"),
                Message("start-b", 0, 1, "START", "L", "B"),
            )
        if phase == 1:
            messages: list[Message] = []
            if state.started_a:
                messages.append(Message("echo-a-b", 1, 0, "ECHO", "A", "B", 0))
            if state.started_b:
                messages.append(Message("echo-b-a", 1, 1, "ECHO", "B", "A", 1))
            return tuple(messages)
        raise ValueError(f"invalid phase {phase}")

    def deliver(self, state: EchoGateState, message: Message) -> EchoGateState:
        if message.kind == "START" and message.receiver == "A":
            return replace(state, started_a=True)
        if message.kind == "START" and message.receiver == "B":
            return replace(state, started_b=True)
        if message.kind == "ECHO" and message.receiver == "A":
            return replace(state, echo_at_a=True)
        if message.kind == "ECHO" and message.receiver == "B":
            return replace(state, echo_at_b=True)
        raise ValueError(f"unexpected message {message}")

    def barrier(self, state: EchoGateState, phase: int) -> EchoGateState:
        if phase != 1:
            return state
        decision_a = state.decision_a
        decision_b = state.decision_b
        if state.started_a and not state.echo_at_a and decision_a is None:
            decision_a = 0
        if state.started_b and not state.echo_at_b and decision_b is None:
            decision_b = 1
        return replace(state, decision_a=decision_a, decision_b=decision_b)

    def observation(self, state: EchoGateState) -> Observation:
        return Observation(self.observed_nodes, (state.decision_a, state.decision_b))
