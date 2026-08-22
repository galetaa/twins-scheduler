from __future__ import annotations

from functools import lru_cache
import os

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("SCHEDCHECK_FAST_REPRO") == "1",
    reason=(
        "the exhaustive runner already regenerated and self-checked the same "
        "state spaces in fast reproduction mode"
    ),
)

from schedcheck.locking.cases import CASES, case_by_id
from schedcheck.locking.explorer import (
    _apply_delivery_sequence,
    explore_case,
    replay_witness,
    stage_delivery_commutes,
)
from schedcheck.locking.kernel import complete_stage, emit_stage, initial_runtime
from schedcheck.locking.model import Grammar, KernelState, VARIANTS, VariantName
from schedcheck.locking.oracle import verify_witness

STANDARD_LATTICE = (
    Grammar.PARTITION,
    Grammar.DIRECTED,
    Grammar.TYPE_SPECIFIC,
    Grammar.PER_MESSAGE,
    Grammar.PER_MESSAGE_REPLAY1,
)
ALL_GRAMMARS = (
    Grammar.PARTITION,
    Grammar.DIRECTED,
    Grammar.DIRECTED_DELAY1,
    Grammar.TYPE_SPECIFIC,
    Grammar.PER_MESSAGE,
    Grammar.PER_MESSAGE_REPLAY1,
)


@lru_cache(maxsize=None)
def _result(case_id: str, variant_name: VariantName, grammar: Grammar):
    return explore_case(case_by_id(case_id), VARIANTS[variant_name], grammar)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.case_id)
def test_correct_baseline_is_safe_in_every_checked_grammar(case) -> None:
    for grammar in ALL_GRAMMARS:
        assert not _result(
            case.case_id, VariantName.BASELINE, grammar
        ).unsafe_observations


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.case_id)
def test_standard_observation_language_inclusions(case) -> None:
    for variant_name in (VariantName.BASELINE, case.variant):
        results = [
            _result(case.case_id, variant_name, grammar)
            for grammar in STANDARD_LATTICE
        ]
        for weaker, stronger in zip(results, results[1:], strict=False):
            assert weaker.observations <= stronger.observations


def test_directed_is_embedded_in_directed_delay1() -> None:
    for case in CASES:
        for variant_name in (VariantName.BASELINE, case.variant):
            directed = _result(case.case_id, variant_name, Grammar.DIRECTED)
            delayed = _result(case.case_id, variant_name, Grammar.DIRECTED_DELAY1)
            assert directed.observations <= delayed.observations


@pytest.mark.parametrize(
    ("case_id", "variant_name"),
    [
        ("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE),
        ("QC_GUARD", VariantName.WRONG_QC_GUARD),
        ("TIMEOUT_CLASSIFICATION", VariantName.TIMEOUT_AS_PRECOMMIT),
    ],
)
def test_natural_phase_specific_separations(case_id, variant_name) -> None:
    directed = _result(case_id, variant_name, Grammar.DIRECTED)
    typed = _result(case_id, variant_name, Grammar.TYPE_SPECIFIC)
    per_message = _result(case_id, variant_name, Grammar.PER_MESSAGE)
    assert not directed.unsafe_observations
    assert typed.unsafe_observations
    assert typed.observations == per_message.observations
    assert typed.unsafe_observations == per_message.unsafe_observations


def test_one_view_commit_delay_is_a_minimal_extension_for_two_mutants() -> None:
    for case_id, variant_name in (
        ("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE),
        ("QC_GUARD", VariantName.WRONG_QC_GUARD),
    ):
        delayed = _result(case_id, variant_name, Grammar.DIRECTED_DELAY1)
        assert delayed.unsafe_observations

    # Timeout misclassification still requires distinguishing inbound phases:
    # delaying only commit evidence cannot suppress PREVOTE while admitting
    # PRECOMMIT on the same directed edge.
    timeout = _result(
        "TIMEOUT_CLASSIFICATION",
        VariantName.TIMEOUT_AS_PRECOMMIT,
        Grammar.DIRECTED_DELAY1,
    )
    assert not timeout.unsafe_observations


def test_replay_is_necessary_for_duplicate_vote_counting_mutant() -> None:
    per_message = _result(
        "DUPLICATE_REPLAY",
        VariantName.DUPLICATE_VOTE_COUNTING,
        Grammar.PER_MESSAGE,
    )
    replay = _result(
        "DUPLICATE_REPLAY",
        VariantName.DUPLICATE_VOTE_COUNTING,
        Grammar.PER_MESSAGE_REPLAY1,
    )
    assert not per_message.unsafe_observations
    assert replay.unsafe_observations


def test_partition_positive_control_exposes_non_scheduler_specific_bug() -> None:
    result = _result(
        "VALIDATION_OMISSION_CONTROL",
        VariantName.RECEIVER_VALIDATION_OMISSION,
        Grammar.PARTITION,
    )
    assert result.unsafe_observations


@pytest.mark.parametrize(
    ("case_id", "variant_name", "grammar"),
    [
        ("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.TYPE_SPECIFIC),
        ("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.DIRECTED_DELAY1),
        ("QC_GUARD", VariantName.WRONG_QC_GUARD, Grammar.TYPE_SPECIFIC),
        ("TIMEOUT_CLASSIFICATION", VariantName.TIMEOUT_AS_PRECOMMIT, Grammar.TYPE_SPECIFIC),
        ("DUPLICATE_REPLAY", VariantName.DUPLICATE_VOTE_COUNTING, Grammar.PER_MESSAGE_REPLAY1),
        ("VALIDATION_OMISSION_CONTROL", VariantName.RECEIVER_VALIDATION_OMISSION, Grammar.PARTITION),
    ],
)
def test_minimal_unsafe_witnesses_replay_in_two_oracles(
    case_id, variant_name, grammar
) -> None:
    case = case_by_id(case_id)
    variant = VARIANTS[variant_name]
    result = _result(case_id, variant_name, grammar)
    observation = min(result.unsafe_observations, key=str)
    witness = result.witnesses[observation]
    assert replay_witness(case, variant, witness).observation() == observation
    assert verify_witness(case, variant, witness) == observation


def test_stage_order_reduction_is_sound_on_a_full_baseline_view() -> None:
    case = case_by_id("LOCK_OMISSION")
    plan = case.plans[0]
    variant = VARIANTS[VariantName.BASELINE]
    runtime = initial_runtime(KernelState())
    for stage in range(5):
        messages = emit_stage(runtime, plan, stage, variant)
        assert stage_delivery_commutes(runtime, messages, plan, variant)
        runtime = _apply_delivery_sequence(runtime, messages, plan, variant)
        runtime = complete_stage(runtime, stage, variant)
