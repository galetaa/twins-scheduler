from __future__ import annotations

from dataclasses import dataclass, replace

from schedcheck.model import Message, Observation
from schedcheck.protocols.base import FiniteProtocol


@dataclass(frozen=True, slots=True)
class TwinBranchState:
    decision_a: int | None = None
    decision_b: int | None = None


class TwinBranchProtocol(FiniteProtocol):
    """Positive control: a classic branch-separable Twins-style witness.

    Two physical clones sharing a logical identity expose conflicting branch
    certificates. A view partition can isolate T0 with A and T1 with B, so the
    weakest grammar already reaches the agreement violation.
    """

    name = "TWIN_BRANCH_CONTROL"
    nodes = ("T0", "T1", "A", "B")
    observed_nodes = ("A", "B")
    message_types = ("CERT",)
    phase_count = 1

    def initial_state(self) -> TwinBranchState:
        return TwinBranchState()

    def emit(self, state: TwinBranchState, phase: int) -> tuple[Message, ...]:
        if phase != 0:
            raise ValueError(f"invalid phase {phase}")
        return (
            Message("t0-a", 0, 0, "CERT", "T0", "A", 0),
            Message("t0-b", 0, 1, "CERT", "T0", "B", 0),
            Message("t1-a", 0, 2, "CERT", "T1", "A", 1),
            Message("t1-b", 0, 3, "CERT", "T1", "B", 1),
        )

    def deliver(self, state: TwinBranchState, message: Message) -> TwinBranchState:
        if message.receiver == "A" and state.decision_a is None:
            return replace(state, decision_a=message.value)
        if message.receiver == "B" and state.decision_b is None:
            return replace(state, decision_b=message.value)
        return state

    def barrier(self, state: TwinBranchState, phase: int) -> TwinBranchState:
        return state

    def observation(self, state: TwinBranchState) -> Observation:
        return Observation(self.observed_nodes, (state.decision_a, state.decision_b))
