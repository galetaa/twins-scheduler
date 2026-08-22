from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Iterable

from twinsbound.model import Event, Observation
from twinsbound.protocols.toy_locking import BranchExploration, ToyTwoPhaseLocking


@dataclass(slots=True)
class LanguageResult:
    model: str
    value_count: int
    observations: set[Observation]
    witnesses: dict[Observation, tuple[frozenset[int], tuple[Event, ...]]]
    branch_explorations: dict[frozenset[int], BranchExploration]
    elapsed_seconds: float

    @property
    def unsafe(self) -> set[Observation]:
        return {o for o in self.observations if o.unsafe()}

    @property
    def total_states(self) -> int:
        return sum(x.states_explored for x in self.branch_explorations.values())

    @property
    def total_transitions(self) -> int:
        return sum(x.transitions_explored for x in self.branch_explorations.values())


def enumerate_language(
    protocol: ToyTwoPhaseLocking,
    model: str,
    value_count: int,
    branch_sets: Iterable[frozenset[int]],
    *,
    validate_quotient: bool,
) -> LanguageResult:
    start = perf_counter()
    observations: set[Observation] = set()
    witnesses: dict[Observation, tuple[frozenset[int], tuple[Event, ...]]] = {}
    branch_explorations: dict[frozenset[int], BranchExploration] = {}

    for branch_set in sorted(set(branch_sets), key=lambda s: (len(s), tuple(sorted(s)))):
        result = protocol.explore(branch_set)
        if validate_quotient:
            protocol.validate_quotient(branch_set)
        branch_explorations[branch_set] = result
        observations.update(result.observations)
        for obs, events in result.witness_events.items():
            candidate = (branch_set, events)
            previous = witnesses.get(obs)
            if previous is None or (len(events), len(branch_set), tuple(sorted(branch_set))) < (
                len(previous[1]), len(previous[0]), tuple(sorted(previous[0]))
            ):
                witnesses[obs] = candidate

    return LanguageResult(
        model=model,
        value_count=value_count,
        observations=observations,
        witnesses=witnesses,
        branch_explorations=branch_explorations,
        elapsed_seconds=perf_counter() - start,
    )
