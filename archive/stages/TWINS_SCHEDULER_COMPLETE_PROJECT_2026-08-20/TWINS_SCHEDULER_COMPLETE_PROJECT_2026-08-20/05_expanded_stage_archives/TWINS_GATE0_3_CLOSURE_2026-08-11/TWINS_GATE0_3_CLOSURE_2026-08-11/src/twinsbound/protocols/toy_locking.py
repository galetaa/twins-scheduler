from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import product
from typing import Iterable

from twinsbound.model import Event, NodeStatus, Observation, StatusKind


@dataclass(frozen=True, slots=True)
class ProtocolState:
    locks: tuple[int | None, ...]
    decisions: tuple[int | None, ...]
    commit_available: frozenset[int]


@dataclass(slots=True)
class BranchExploration:
    branch_values: frozenset[int]
    observations: set[Observation]
    witness_events: dict[Observation, tuple[Event, ...]]
    states_explored: int
    transitions_explored: int


class ToyTwoPhaseLocking:
    """Small deterministic authenticated two-phase protocol.

    One Byzantine protocol identity is the leader. A correct-code branch first
    accepts exactly one external input value and emits PROPOSE(value). A correct
    replica accepts its first proposal, locks and emits VOTE(value). A branch that
    receives a matching correct vote emits COMMIT(value, vote-reference). A locked
    replica decides only after the matching commit. The quorum is deliberately weak
    (leader plus one correct vote), so equivocation exposes an agreement violation.

    This is a diagnostic protocol, not a production-safe BFT design. It exists to
    compare adversary languages under exact finite semantics.
    """

    def __init__(self, correct_replicas: int) -> None:
        if correct_replicas < 2:
            raise ValueError("at least two correct replicas are required")
        self.correct_replicas = correct_replicas

    def initial_state(self) -> ProtocolState:
        return ProtocolState(
            locks=(None,) * self.correct_replicas,
            decisions=(None,) * self.correct_replicas,
            commit_available=frozenset(),
        )

    @staticmethod
    def observation(state: ProtocolState) -> Observation:
        statuses: list[NodeStatus] = []
        for lock, decision in zip(state.locks, state.decisions, strict=True):
            if decision is not None:
                statuses.append(NodeStatus.decision(decision))
            elif lock is not None:
                statuses.append(NodeStatus.proposal(lock))
            else:
                statuses.append(NodeStatus.none())
        return Observation(tuple(statuses))

    def successors(
        self,
        state: ProtocolState,
        branch_values: frozenset[int],
    ) -> Iterable[tuple[Event, ProtocolState]]:
        # Deliver a causally valid proposal to an unlocked correct replica.
        for node, lock in enumerate(state.locks):
            if lock is None:
                for value in sorted(branch_values):
                    locks = list(state.locks)
                    locks[node] = value
                    yield (
                        Event("DELIVER_PROPOSAL", node=node, value=value),
                        ProtocolState(tuple(locks), state.decisions, state.commit_available),
                    )

        # Deliver one matching correct vote to the corresponding leader branch.
        # Once any vote arrives, the branch deterministically emits a commit proof.
        for node, lock in enumerate(state.locks):
            if lock is not None and lock not in state.commit_available:
                yield (
                    Event("DELIVER_VOTE_TO_BRANCH", node=node, value=lock),
                    ProtocolState(
                        state.locks,
                        state.decisions,
                        state.commit_available | {lock},
                    ),
                )

        # Deliver a valid commit to a replica locked on the same value.
        for node, (lock, decision) in enumerate(zip(state.locks, state.decisions, strict=True)):
            if decision is None and lock is not None and lock in state.commit_available:
                decisions = list(state.decisions)
                decisions[node] = lock
                yield (
                    Event("DELIVER_COMMIT_AND_DECIDE", node=node, value=lock),
                    ProtocolState(state.locks, tuple(decisions), state.commit_available),
                )

    def explore(self, branch_values: frozenset[int]) -> BranchExploration:
        initial = self.initial_state()
        queue: deque[ProtocolState] = deque([initial])
        parent: dict[ProtocolState, tuple[ProtocolState, Event] | None] = {initial: None}
        observations: set[Observation] = set()
        witness_state: dict[Observation, ProtocolState] = {}
        transitions = 0

        while queue:
            state = queue.popleft()
            obs = self.observation(state)
            observations.add(obs)
            witness_state.setdefault(obs, state)
            for event, nxt in self.successors(state, branch_values):
                transitions += 1
                if nxt not in parent:
                    parent[nxt] = (state, event)
                    queue.append(nxt)

        witness_events: dict[Observation, tuple[Event, ...]] = {}
        for obs, state in witness_state.items():
            events: list[Event] = []
            cursor = state
            while parent[cursor] is not None:
                prev, event = parent[cursor]  # type: ignore[misc]
                events.append(event)
                cursor = prev
            witness_events[obs] = tuple(reversed(events))

        return BranchExploration(
            branch_values=branch_values,
            observations=observations,
            witness_events=witness_events,
            states_explored=len(parent),
            transitions_explored=transitions,
        )

    def quotient_language(self, branch_values: frozenset[int]) -> set[Observation]:
        """Closed-form terminal quotient used as an independent BFS check."""
        options = [NodeStatus.none()]
        for value in sorted(branch_values):
            options.extend((NodeStatus.proposal(value), NodeStatus.decision(value)))
        return {Observation(tuple(statuses)) for statuses in product(options, repeat=self.correct_replicas)}

    def validate_quotient(self, branch_values: frozenset[int]) -> None:
        bfs = self.explore(branch_values).observations
        closed = self.quotient_language(branch_values)
        if bfs != closed:
            missing = sorted(o.canonical_id() for o in closed - bfs)
            extra = sorted(o.canonical_id() for o in bfs - closed)
            raise AssertionError(f"quotient mismatch: missing={missing[:5]}, extra={extra[:5]}")
