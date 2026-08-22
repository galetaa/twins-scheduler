from __future__ import annotations

from dataclasses import dataclass

from schedcheck.tendermint.model import ValidRoundProof, VariantName, ViewPlan


@dataclass(frozen=True, slots=True)
class ExperimentCase:
    case_id: str
    title: str
    variant: VariantName
    plans: tuple[ViewPlan, ...]
    mechanism: str
    falsifier: str


TWO_CONFLICTING_ROUNDS = (
    ViewPlan(view=1, leader="T0", value=0),
    ViewPlan(view=2, leader="T1", value=1),
)


CASES: tuple[ExperimentCase, ...] = (
    ExperimentCase(
        case_id="TM_LOCK_OMISSION",
        title="PoLC observed but persistent lock update omitted",
        variant=VariantName.MISSING_LOCK_UPDATE,
        plans=TWO_CONFLICTING_ROUNDS,
        mechanism=(
            "A phase-specific schedule delivers the round-1 POLKA to a validator "
            "but withholds the terminal COMMIT on the same proposer-to-validator "
            "edge. The mutant precommits without retaining the lock and can later "
            "prevote a conflicting proposal."
        ),
        falsifier=(
            "No agreement-violating observation is reachable outside the directed "
            "round-graph language, or the witness disappears under independent replay."
        ),
    ),
    ExperimentCase(
        case_id="TM_VALID_ROUND_GUARD",
        title="Proposal guard ignores the value certified by valid-round evidence",
        variant=VariantName.WRONG_VALID_ROUND_GUARD,
        plans=(
            ViewPlan(view=1, leader="T0", value=0),
            ViewPlan(
                view=2,
                leader="T1",
                value=1,
                valid_round_proof=ValidRoundProof(round=1, value=0),
            ),
        ),
        mechanism=(
            "A locked validator incorrectly treats a prior-round PoLC for value 0 as "
            "justification for a conflicting value 1. A phase-specific schedule can "
            "separate POLKA from COMMIT and preserve the conflicting voter."
        ),
        falsifier=(
            "The mismatched valid-round proof is rejected on every path, or directed "
            "round graphs expose exactly the same unsafe observations."
        ),
    ),
    ExperimentCase(
        case_id="TM_DUPLICATE_REPLAY",
        title="Replayed prevotes counted as distinct voting-power contributions",
        variant=VariantName.DUPLICATE_VOTE_COUNTING,
        plans=TWO_CONFLICTING_ROUNDS,
        mechanism=(
            "One replay lets a non-idempotent vote set count the same validator twice. "
            "The Byzantine proposer plus two instances of one honest prevote can form "
            "a false PoLC and, symmetrically, conflicting commits in two rounds."
        ),
        falsifier=(
            "Deduplication by validator identity makes replay observationally inert, "
            "or a single replay remains insufficient to reach conflicting decisions."
        ),
    ),
    ExperimentCase(
        case_id="TM_VALIDATION_CONTROL",
        title="One receiver accepts a forged commit as a positive control",
        variant=VariantName.RECEIVER_VALIDATION_OMISSION,
        plans=(
            ViewPlan(view=1, leader="T0", value=0, emit_forged_commit=True),
            ViewPlan(view=2, leader="T1", value=1),
        ),
        mechanism=(
            "H3 omits commit quorum validation. The defect should already be visible "
            "under a partition grammar and therefore guards against a checker that "
            "manufactures only richer-scheduler conclusions."
        ),
        falsifier=(
            "The forged commit is rejected or no partition schedule can combine it "
            "with a later valid conflicting commit."
        ),
    ),
)


def case_by_id(case_id: str) -> ExperimentCase:
    for case in CASES:
        if case.case_id == case_id:
            return case
    raise KeyError(case_id)
