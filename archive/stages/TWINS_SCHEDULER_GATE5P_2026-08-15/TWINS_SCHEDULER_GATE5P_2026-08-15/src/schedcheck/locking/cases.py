from __future__ import annotations

from dataclasses import dataclass

from schedcheck.locking.model import Justification, VariantName, ViewPlan


@dataclass(frozen=True, slots=True)
class ExperimentCase:
    case_id: str
    title: str
    variant: VariantName
    plans: tuple[ViewPlan, ...]
    mechanism: str
    falsifier: str


TWO_CONFLICTING_VIEWS = (
    ViewPlan(view=1, leader="T0", value=0),
    ViewPlan(view=2, leader="T1", value=1),
)

CASES: tuple[ExperimentCase, ...] = (
    ExperimentCase(
        case_id="LOCK_OMISSION",
        title="Lock update omitted on valid precommit certificate",
        variant=VariantName.MISSING_LOCK_UPDATE,
        plans=TWO_CONFLICTING_VIEWS,
        mechanism=(
            "A type-specific scheduler can deliver PRECOMMIT_QC but suppress "
            "COMMIT_QC on the same leader-to-replica edge. The mutant sends "
            "precommits without retaining a lock, so the same honest voters can "
            "support a conflicting later value."
        ),
        falsifier=(
            "No unsafe observation exists outside the directed language, or every "
            "candidate witness disappears when lock/decision guards are replayed "
            "by the independent oracle."
        ),
    ),
    ExperimentCase(
        case_id="QC_GUARD",
        title="QC guard ignores certified value and uses a non-strict view comparison",
        variant=VariantName.WRONG_QC_GUARD,
        plans=(
            ViewPlan(view=1, leader="T0", value=0),
            ViewPlan(
                view=2,
                leader="T1",
                value=1,
                justification=Justification(view=1, value=0),
            ),
        ),
        mechanism=(
            "The mutant treats a certificate for value 0 in view 1 as sufficient "
            "to unlock a replica for conflicting value 1 at the same lock view."
        ),
        falsifier=(
            "The malformed justification is rejected in every path, or the richer "
            "scheduler adds no unsafe observation beyond the directed grammar."
        ),
    ),
    ExperimentCase(
        case_id="TIMEOUT_CLASSIFICATION",
        title="Timeout certificate misclassified as precommit evidence without a lock",
        variant=VariantName.TIMEOUT_AS_PRECOMMIT,
        plans=(
            ViewPlan(view=1, leader="T0", value=0, emit_timeout_qc=True),
            ViewPlan(view=2, leader="T1", value=1, emit_timeout_qc=True),
        ),
        mechanism=(
            "A valid timeout certificate is incorrectly interpreted as value-specific "
            "precommit evidence. The timeout path emits a precommit but does not "
            "establish the corresponding lock."
        ),
        falsifier=(
            "Timeout delivery cannot create a commit certificate without the normal "
            "locking path, or any resulting violation is already expressible by the "
            "directed grammar."
        ),
    ),
    ExperimentCase(
        case_id="DUPLICATE_REPLAY",
        title="Replayed votes counted as distinct quorum members",
        variant=VariantName.DUPLICATE_VOTE_COUNTING,
        plans=TWO_CONFLICTING_VIEWS,
        mechanism=(
            "With one bounded replay, a leader that counts message instances rather "
            "than logical signer identities can form a quorum from its own vote and "
            "two copies of one honest vote. Disjoint honest replicas can then certify "
            "conflicting values in consecutive views."
        ),
        falsifier=(
            "Signer de-duplication makes replay observationally inert, or one replay "
            "per vote remains insufficient to reach conflicting decisions."
        ),
    ),
    ExperimentCase(
        case_id="VALIDATION_OMISSION_CONTROL",
        title="One receiver accepts a forged commit certificate",
        variant=VariantName.RECEIVER_VALIDATION_OMISSION,
        plans=(
            ViewPlan(
                view=1,
                leader="T0",
                value=0,
                emit_forged_commit_qc=True,
            ),
            ViewPlan(view=2, leader="T1", value=1),
        ),
        mechanism=(
            "H3 omits quorum validation for a forged certificate. This control is "
            "expected to be visible even to the weakest partition grammar and checks "
            "that the oracle does not manufacture a scheduler-specific conclusion."
        ),
        falsifier=(
            "The forged certificate is rejected by H3 or the exact partition search "
            "cannot combine it with a later valid conflicting decision."
        ),
    ),
)


def case_by_id(case_id: str) -> ExperimentCase:
    for case in CASES:
        if case.case_id == case_id:
            return case
    raise KeyError(case_id)
