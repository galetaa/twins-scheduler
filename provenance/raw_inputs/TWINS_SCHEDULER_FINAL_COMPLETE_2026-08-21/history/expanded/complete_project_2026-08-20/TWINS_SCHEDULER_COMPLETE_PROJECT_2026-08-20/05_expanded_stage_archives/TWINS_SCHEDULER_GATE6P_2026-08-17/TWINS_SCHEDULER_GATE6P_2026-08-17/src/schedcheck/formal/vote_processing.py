from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
from itertools import product
from typing import Iterable


@dataclass(frozen=True, order=True, slots=True)
class LogicalVote:
    height: int
    round: int
    phase: str
    value: int
    validator: str

    def replay_key(self) -> tuple[int, int, str, int, str]:
        """Identity of one exact signed protocol action."""
        return (self.height, self.round, self.phase, self.value, self.validator)

    def contribution_key(self) -> tuple[int, int, str, str]:
        """Validator slot that may contribute voting power at most once."""
        return (self.height, self.round, self.phase, self.validator)

    # Backward-compatible alias used by serialized diagnostics.
    def key(self) -> tuple[int, int, str, int, str]:
        return self.replay_key()


@dataclass(frozen=True, slots=True)
class VoteProcessingResult:
    contributions: int
    quorum: bool
    accepted_sequence: tuple[LogicalVote, ...]


def erase_replays(sequence: Iterable[LogicalVote]) -> tuple[LogicalVote, ...]:
    """Retain the first occurrence of every logical signed vote."""
    seen: set[tuple[int, int, str, int, str]] = set()
    result: list[LogicalVote] = []
    for vote in sequence:
        if vote.replay_key() in seen:
            continue
        seen.add(vote.replay_key())
        result.append(vote)
    return tuple(result)


def process_votes(
    sequence: Iterable[LogicalVote],
    *,
    quorum: int,
    unique_by_logical_vote: bool,
) -> VoteProcessingResult:
    accepted: list[LogicalVote] = []
    seen: set[tuple[int, int, str, str]] = set()
    for vote in sequence:
        contribution = vote.contribution_key()
        if unique_by_logical_vote and contribution in seen:
            continue
        seen.add(contribution)
        accepted.append(vote)
    return VoteProcessingResult(
        contributions=len(accepted),
        quorum=len(accepted) >= quorum,
        accepted_sequence=tuple(accepted),
    )


def replay_erasure_holds(
    sequence: Iterable[LogicalVote],
    *,
    quorum: int,
) -> bool:
    original = tuple(sequence)
    left = process_votes(original, quorum=quorum, unique_by_logical_vote=True)
    right = process_votes(
        erase_replays(original), quorum=quorum, unique_by_logical_vote=True
    )
    return (
        left.contributions == right.contributions
        and left.quorum == right.quorum
        and left.accepted_sequence == right.accepted_sequence
    )


def enumerate_vote_sequences(
    alphabet: tuple[LogicalVote, ...], max_length: int
) -> Iterable[tuple[LogicalVote, ...]]:
    yield ()
    for length in range(1, max_length + 1):
        yield from product(alphabet, repeat=length)


def exhaustive_replay_check(max_length: int = 5) -> dict[str, object]:
    # B supplies the Byzantine vote in the n=4, q=3 witness; H1/H2 are
    # honest validator identities. H3 is unnecessary for this minimal trace.
    alphabet = tuple(
        LogicalVote(1, 1, "PREVOTE", 0, validator)
        for validator in ("B", "H1", "H2")
    )
    checked = 0
    counterexamples: list[list[str]] = []
    mutant_separations: list[list[str]] = []
    for sequence in enumerate_vote_sequences(alphabet, max_length):
        checked += 1
        if not replay_erasure_holds(sequence, quorum=3):
            counterexamples.append([vote.validator for vote in sequence])
        correct = process_votes(sequence, quorum=3, unique_by_logical_vote=True)
        mutant = process_votes(sequence, quorum=3, unique_by_logical_vote=False)
        labels = [vote.validator for vote in sequence]
        counts = Counter(labels)
        duplicate_instances = len(labels) - len(counts)
        duplicated_honest = any(
            validator != "B" and multiplicity == 2
            for validator, multiplicity in counts.items()
        )
        # Match G_R: one additional delivery of one already delivered logical
        # vote, while retaining at least two logical contributors.
        if (
            mutant.quorum
            and not correct.quorum
            and duplicate_instances == 1
            and len(counts) >= 2
            and duplicated_honest
        ):
            mutant_separations.append(labels)
    minimal = min(mutant_separations, key=lambda seq: (len(seq), seq))
    return {
        "max_sequence_length": max_length,
        "alphabet_size": len(alphabet),
        "sequences_checked": checked,
        "replay_erasure_holds_for_idempotent_processing": not counterexamples,
        "counterexamples": counterexamples,
        "non_idempotent_processing_has_strict_separation": bool(mutant_separations),
        "minimal_non_idempotent_separation": minimal,
    }
