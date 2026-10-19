"""Embed the independent-pivot contract in the general transition semantics.

The exporter uses raw predecessor constraints and executable repair/signature
state.  It does not call a repair-graph extractor, acyclic-capacity formula,
four-role optimizer, or event-order enumerator.  Every suppressed repair still
consumes its complete opportunity slot.  This is an explicit specialization
bridge between two declared models, not extraction from arbitrary client code.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from typing import Any, Iterable

from .refinement_synthesis import Problem as PivotProblem
from .repair_frontier import Event
from .transition_synthesis import Problem, SynthesisLimit, Transition, replay_trace


class AdapterLimit(SynthesisLimit):
    """The pivot transition graph is incomplete; feasibility remains unknown."""


@dataclass(frozen=True)
class PivotState:
    prefix: int
    first: int
    completed: int
    repaired: int
    second: int


def _unsafe(source: PivotProblem, states: tuple[PivotState, ...]) -> frozenset[int]:
    k = source.domain.k
    complete = (1 << (2 * k)) - 1
    result = set()
    for index, state in enumerate(states):
        if state.prefix != k or state.completed != complete:
            continue
        first = sum(weight for i, weight in enumerate(source.domain.weights) if state.first >> i & 1)
        second = sum(weight for i, weight in enumerate(source.domain.weights) if state.second >> i & 1)
        if first >= source.deficit0 and second >= source.deficit1:
            result.add(index)
    return frozenset(result)


@dataclass(frozen=True)
class PivotModel:
    source: PivotProblem
    problem: Problem
    states: tuple[PivotState, ...]
    edge_events: tuple[Event, ...]

    def with_objective(self, source: PivotProblem) -> PivotModel:
        """Reuse unchanged protocol transitions for another cost/quota query.

        The complete Domain, including weights and opportunity constraints,
        must be identical.  Costs and split permissions filter policies, not
        the exported underlying protocol graph.
        """
        if source.domain.initially_ready is not True:
            raise ValueError("the specialization bridge requires initial readiness")
        if source.domain != self.source.domain:
            raise ValueError("changing the pivot domain requires a fresh exported model")
        problem = replace(self.problem, unsafe=_unsafe(source, self.states),
                          costs=source.costs, allowed_split=source.allowed_split,
                          required_split=source.required_split)
        return PivotModel(source, problem, self.states, self.edge_events)


def build_pivot_model(source: PivotProblem, *, max_states: int = 100_000) -> PivotModel:
    """Generate every E-prefix and every legal complete R/V opportunity order.

    E_i and R_i are distinct fine keys 2*i and 2*i+1 in coarse fibre i.
    Each R_i has both Boolean transitions, even if E_i was false.  This permits
    the general interface's reversed mixed pattern (E_i=False,R_i=True).
    That pattern is dominated by (True,False) under this independent contract,
    which is part of the optimum-preserving normalization proof.
    """
    if source.domain.initially_ready is not True:
        raise ValueError("the specialization bridge requires initial readiness")
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be a positive integer")
    k = source.domain.k
    events = tuple((kind, i) for kind in ("R", "V") for i in range(k))
    event_index = {event: index for index, event in enumerate(events)}
    predecessor_masks = [0] * len(events)
    for earlier, later in source.domain.precedence:
        predecessor_masks[event_index[later]] |= 1 << event_index[earlier]
    initial = PivotState(0, 0, 0, 0, 0)
    states = [initial]
    identifiers = {initial: 0}
    pending = deque([initial])
    transitions = []
    edge_events = []

    def add(state: PivotState, following: PivotState, event: Event,
            key: int | None, value: bool | None) -> None:
        target = identifiers.get(following)
        if target is None:
            if len(states) >= max_states:
                raise AdapterLimit("pivot-export state limit exhausted; no complete model; result remains unknown")
            target = len(states)
            identifiers[following] = target
            states.append(following)
            pending.append(following)
        suffix = "" if value is None else f"={int(value)}"
        transitions.append(Transition(identifiers[state], target, key, value,
                                      f"{event[0]}_{event[1]}{suffix}"))
        edge_events.append(event)

    while pending:
        state = pending.popleft()
        if state.prefix < k:
            i = state.prefix
            for admitted in (False, True):
                following = PivotState(i + 1, state.first | ((1 << i) if admitted else 0), 0, 0, 0)
                add(state, following, ("E", i), 2 * i, admitted)
            continue
        for index, (kind, i) in enumerate(events):
            if state.completed >> index & 1 or predecessor_masks[index] & ~state.completed:
                continue
            completed = state.completed | (1 << index)
            if kind == "R":
                for admitted in (False, True):
                    following = replace(state, completed=completed,
                                        repaired=state.repaired | ((1 << i) if admitted else 0))
                    add(state, following, (kind, i), 2 * i + 1, admitted)
            else:
                following = replace(state, completed=completed,
                                    second=state.second | (0 if state.repaired >> i & 1 else 1 << i))
                add(state, following, (kind, i), None, None)
    frozen_states = tuple(states)
    names = tuple(f"p{state.prefix}:f{state.first}:d{state.completed}:r{state.repaired}:v{state.second}"
                  for state in states)
    problem = Problem(names, 0, _unsafe(source, frozen_states), tuple(transitions),
                      tuple(i for i in range(k) for _ in range(2)), source.costs,
                      source.allowed_split, source.required_split)
    return PivotModel(source, problem, frozen_states, tuple(edge_events))


def normalize_witness(model: PivotModel, transitions: Iterable[int]) -> dict[str, Any]:
    """Normalize a general unsafe path to the independent contract's policy.

    Required or trace-mixed fibres become E=True,R=False.  Unsplit fibres keep
    their common value.  No opportunity is deleted or reordered.  Independent
    contributions then imply that first and second signer sets can only grow.
    The result is an input for repair_frontier.execute, not a claim about
    protocol implementations outside the independent contract.
    """
    replayed = replay_trace(model.problem, transitions)
    if replayed["terminal"] not in model.problem.unsafe:
        raise ValueError("normalization requires a complete unsafe pivot path")
    split = frozenset(replayed["split"])
    state = model.states[replayed["terminal"]]
    opened = split | frozenset(i for i in range(model.source.domain.k) if state.first >> i & 1)
    order = tuple(model.edge_events[index] for index in replayed["transitions"]
                  if model.edge_events[index][0] != "E")
    return {"opened": sorted(opened), "split": sorted(split),
            "order": [list(event) for event in order], "cost": replayed["cost"]}
