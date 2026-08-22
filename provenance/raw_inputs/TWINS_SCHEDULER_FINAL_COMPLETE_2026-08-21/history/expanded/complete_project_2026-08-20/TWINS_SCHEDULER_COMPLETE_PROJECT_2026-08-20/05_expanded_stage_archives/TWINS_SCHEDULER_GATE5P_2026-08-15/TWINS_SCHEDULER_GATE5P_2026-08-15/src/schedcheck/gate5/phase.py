from __future__ import annotations

from dataclasses import dataclass
from itertools import product

HONEST = ("H1", "H2", "H3")
QUORUM_HONEST = 2  # Byzantine coordinator contributes one logical vote.


@dataclass(frozen=True, order=True, slots=True)
class Replica:
    constrained_value: int | None = None
    decision: int | None = None


@dataclass(frozen=True, order=True, slots=True)
class State:
    replicas: tuple[Replica, ...] = (Replica(), Replica(), Replica())

    def observation(self) -> tuple[int | None, ...]:
        return tuple(replica.decision for replica in self.replicas)

    def unsafe(self) -> bool:
        return len({value for value in self.observation() if value is not None}) > 1


def _bit(mask: int, index: int) -> bool:
    return bool(mask & (1 << index))


def _run_round(
    state: State,
    *,
    value: int,
    evidence_mask: int,
    action_mask: int,
    terminal_mask: int,
    retain_constraint: bool,
) -> State:
    replicas = list(state.replicas)
    supporters: list[int] = []
    for index, replica in enumerate(replicas):
        if not _bit(evidence_mask, index):
            continue
        if replica.decision is not None and replica.decision != value:
            continue
        if replica.constrained_value not in (None, value):
            continue
        if retain_constraint:
            replicas[index] = Replica(constrained_value=value, decision=replica.decision)
        if _bit(action_mask, index):
            supporters.append(index)

    terminal_exists = len(supporters) >= QUORUM_HONEST
    if terminal_exists:
        for index, replica in enumerate(replicas):
            if _bit(terminal_mask, index) and replica.decision is None:
                replicas[index] = Replica(constrained_value=value, decision=value)
    return State(tuple(replicas))


def _round_outcomes(state: State, value: int, grammar: str, retain_constraint: bool) -> set[State]:
    outcomes: set[State] = set()
    if grammar == "DIRECTED":
        # One outbound mask couples evidence and terminal messages; one inbound
        # mask controls actions sent back to the coordinator.
        for outbound, inbound in product(range(8), repeat=2):
            outcomes.add(
                _run_round(
                    state,
                    value=value,
                    evidence_mask=outbound,
                    action_mask=inbound,
                    terminal_mask=outbound,
                    retain_constraint=retain_constraint,
                )
            )
    elif grammar == "TYPE_SPECIFIC":
        for evidence, action, terminal in product(range(8), repeat=3):
            outcomes.add(
                _run_round(
                    state,
                    value=value,
                    evidence_mask=evidence,
                    action_mask=action,
                    terminal_mask=terminal,
                    retain_constraint=retain_constraint,
                )
            )
    else:
        raise ValueError(grammar)
    return outcomes


def explore(grammar: str, *, retain_constraint: bool) -> set[State]:
    frontier = {State()}
    for value in (0, 1):
        next_frontier: set[State] = set()
        for state in frontier:
            next_frontier |= _round_outcomes(state, value, grammar, retain_constraint)
        frontier = next_frontier
    return frontier


def check_phase_coupled_separation() -> dict[str, object]:
    baseline_directed = explore("DIRECTED", retain_constraint=True)
    baseline_typed = explore("TYPE_SPECIFIC", retain_constraint=True)
    defect_directed = explore("DIRECTED", retain_constraint=False)
    defect_typed = explore("TYPE_SPECIFIC", retain_constraint=False)
    unsafe = lambda states: sorted(
        {state.observation() for state in states if state.unsafe()},
        key=str,
    )
    return {
        "baseline": {
            "directed_states": len(baseline_directed),
            "typed_states": len(baseline_typed),
            "directed_unsafe": unsafe(baseline_directed),
            "typed_unsafe": unsafe(baseline_typed),
        },
        "constraint_omission": {
            "directed_states": len(defect_directed),
            "typed_states": len(defect_typed),
            "directed_unsafe": unsafe(defect_directed),
            "typed_unsafe": unsafe(defect_typed),
            "strict_safety_separation": bool(unsafe(defect_typed)) and not bool(unsafe(defect_directed)),
        },
    }
