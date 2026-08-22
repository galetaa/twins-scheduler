from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Iterable

State = Hashable
Message = str
Transition = Callable[[State, Message], State]
Related = Callable[[State, State], bool]
Unsafe = Callable[[State], bool]


@dataclass(frozen=True, slots=True)
class FiniteSystem:
    states: tuple[State, ...]
    original_messages: tuple[Message, ...]
    added_messages: tuple[Message, ...]
    transition: Transition
    related: Related
    unsafe: Unsafe


def run_trace(initial: State, trace: Iterable[Message], transition: Transition) -> State:
    state = initial
    for message in trace:
        state = transition(state, message)
    return state


def check_action_monotone_conditions(system: FiniteSystem) -> dict[str, object]:
    """Check the local premises of the closure-preservation theorem.

    Premise A: every closure-added message moves upward in relation R.
    Premise B: every original message is forward-simulated under R.
    Premise C: unsafety is upward closed under R.
    These are independent local obligations; they do not assume the conclusion
    that a particular closed trace is unsafe.
    """
    added_failures: list[dict[str, object]] = []
    simulation_failures: list[dict[str, object]] = []
    unsafe_failures: list[dict[str, object]] = []

    for state in system.states:
        for message in system.added_messages:
            target = system.transition(state, message)
            if not system.related(state, target):
                added_failures.append(
                    {"state": repr(state), "message": message, "target": repr(target)}
                )

    for left in system.states:
        for right in system.states:
            if not system.related(left, right):
                continue
            if system.unsafe(left) and not system.unsafe(right):
                unsafe_failures.append({"left": repr(left), "right": repr(right)})
            for message in system.original_messages:
                left_next = system.transition(left, message)
                right_next = system.transition(right, message)
                if not system.related(left_next, right_next):
                    simulation_failures.append(
                        {
                            "left": repr(left),
                            "right": repr(right),
                            "message": message,
                            "left_next": repr(left_next),
                            "right_next": repr(right_next),
                        }
                    )

    status = not added_failures and not simulation_failures and not unsafe_failures
    return {
        "status": "PASS" if status else "FAIL",
        "added_message_failures": added_failures,
        "forward_simulation_failures": simulation_failures,
        "unsafe_upward_failures": unsafe_failures,
    }


@dataclass(frozen=True, order=True, slots=True)
class MonotoneState:
    decisions: frozenset[int] = frozenset()
    evidence: frozenset[str] = frozenset()


def _monotone_transition(state: MonotoneState, message: str) -> MonotoneState:
    if message == "D0":
        return MonotoneState(state.decisions | {0}, state.evidence)
    if message == "D1":
        return MonotoneState(state.decisions | {1}, state.evidence)
    if message == "EXTRA":
        return MonotoneState(state.decisions, state.evidence | {"extra"})
    return state


def _monotone_related(left: MonotoneState, right: MonotoneState) -> bool:
    return left.decisions <= right.decisions and left.evidence <= right.evidence


@dataclass(frozen=True, order=True, slots=True)
class FragileState:
    decisions: frozenset[int] = frozenset()
    prepared0: bool = False
    prepared1: bool = False
    pivot_available: bool = True


def _fragile_transition(state: FragileState, message: str) -> FragileState:
    if message == "E0":
        return FragileState(state.decisions, True, state.prepared1, state.pivot_available)
    if message == "D0" and state.prepared0:
        return FragileState(state.decisions | {0}, state.prepared0, state.prepared1, state.pivot_available)
    if message == "E1" and state.pivot_available:
        return FragileState(state.decisions, state.prepared0, True, state.pivot_available)
    if message == "D1" and state.prepared1:
        return FragileState(state.decisions | {1}, state.prepared0, state.prepared1, state.pivot_available)
    if message == "R0":
        return FragileState(state.decisions | {0}, state.prepared0, state.prepared1, False)
    return state


def _fragile_related(left: FragileState, right: FragileState) -> bool:
    # A useful relation must preserve decisions and availability of all original
    # safety-relevant actions. Repair R0 violates the availability component.
    return (
        left.decisions <= right.decisions
        and (not left.prepared0 or right.prepared0)
        and (not left.prepared1 or right.prepared1)
        and (not left.pivot_available or right.pivot_available)
    )


def closure_theorem_checks() -> dict[str, object]:
    monotone_states = tuple(
        MonotoneState(frozenset(decisions), frozenset(evidence))
        for decisions in ((), (0,), (1,), (0, 1))
        for evidence in ((), ("extra",))
    )
    monotone = FiniteSystem(
        states=monotone_states,
        original_messages=("D0", "D1"),
        added_messages=("EXTRA",),
        transition=_monotone_transition,
        related=_monotone_related,
        unsafe=lambda s: len(s.decisions) > 1,
    )
    monotone_conditions = check_action_monotone_conditions(monotone)
    original = ("D0", "D1")
    closed = ("D0", "EXTRA", "D1")
    monotone_original_state = run_trace(MonotoneState(), original, _monotone_transition)
    monotone_closed_state = run_trace(MonotoneState(), closed, _monotone_transition)

    fragile_states = tuple(
        FragileState(frozenset(decisions), p0, p1, available)
        for decisions in ((), (0,), (1,), (0, 1))
        for p0 in (False, True)
        for p1 in (False, True)
        for available in (False, True)
    )
    fragile = FiniteSystem(
        states=fragile_states,
        original_messages=("E0", "D0", "E1", "D1"),
        added_messages=("R0",),
        transition=_fragile_transition,
        related=_fragile_related,
        unsafe=lambda s: len(s.decisions) > 1,
    )
    fragile_conditions = check_action_monotone_conditions(fragile)
    fragile_original = ("E0", "D0", "E1", "D1")
    fragile_closed = ("E0", "R0", "D0", "E1", "D1")
    fragile_original_state = run_trace(FragileState(), fragile_original, _fragile_transition)
    fragile_closed_state = run_trace(FragileState(), fragile_closed, _fragile_transition)

    return {
        "status": "PASS" if (
            monotone_conditions["status"] == "PASS"
            and len(monotone_original_state.decisions) > 1
            and len(monotone_closed_state.decisions) > 1
            and fragile_conditions["status"] == "FAIL"
            and len(fragile_original_state.decisions) > 1
            and len(fragile_closed_state.decisions) <= 1
        ) else "FAIL",
        "theorem": (
            "If closure-added messages are R-increasing, every original transition "
            "is forward-simulated by R, and the unsafe predicate is upward closed "
            "under R, then inserting any finite sequence of closure-added messages "
            "while preserving the order of original messages preserves unsafety."
        ),
        "monotone_example": {
            "conditions": monotone_conditions,
            "original_trace": original,
            "closed_trace": closed,
            "original_state": repr(monotone_original_state),
            "closed_state": repr(monotone_closed_state),
            "unsafe_preserved": len(monotone_closed_state.decisions) > 1,
        },
        "locking_fragility_counterexample": {
            "conditions": fragile_conditions,
            "original_trace": fragile_original,
            "closed_trace": fragile_closed,
            "original_state": repr(fragile_original_state),
            "closed_state": repr(fragile_closed_state),
            "unsafe_before": len(fragile_original_state.decisions) > 1,
            "unsafe_after": len(fragile_closed_state.decisions) > 1,
            "failed_premise": "R0 removes the pivot's future conflicting action",
        },
    }
