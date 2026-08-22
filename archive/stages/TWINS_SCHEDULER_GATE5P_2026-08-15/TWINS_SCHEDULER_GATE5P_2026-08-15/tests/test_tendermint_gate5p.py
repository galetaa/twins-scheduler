from __future__ import annotations

from functools import lru_cache
import os

import pytest

from schedcheck.tendermint.cases import case_by_id
from schedcheck.tendermint.explorer import explore_case
from schedcheck.tendermint.model import Grammar, VARIANTS, VariantName
from schedcheck.tendermint.oracle import verify_witness

pytestmark = pytest.mark.skipif(
    os.environ.get("SCHEDCHECK_FAST_REPRO") == "1",
    reason="Gate 5' runner already regenerated and checked the exact state spaces",
)


@lru_cache(maxsize=None)
def _result(case_id: str, variant: VariantName, grammar: Grammar):
    return explore_case(case_by_id(case_id), VARIANTS[variant], grammar)


def _unsafe_count(case_id: str, variant: VariantName, grammar: Grammar) -> int:
    return len(_result(case_id, variant, grammar).unsafe_observations)


def test_tendermint_baseline_is_safe_under_richest_grammar() -> None:
    for case_id in (
        "TM_LOCK_OMISSION",
        "TM_VALID_ROUND_GUARD",
        "TM_DUPLICATE_REPLAY",
        "TM_VALIDATION_CONTROL",
    ):
        assert _unsafe_count(case_id, VariantName.BASELINE, Grammar.PER_MESSAGE_REPLAY1) == 0


def test_phase_specific_and_delay_boundaries() -> None:
    for case_id, variant in (
        ("TM_LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE),
        ("TM_VALID_ROUND_GUARD", VariantName.WRONG_VALID_ROUND_GUARD),
    ):
        assert _unsafe_count(case_id, variant, Grammar.DIRECTED) == 0
        assert _unsafe_count(case_id, variant, Grammar.DIRECTED_DELAY1) == 12
        assert _unsafe_count(case_id, variant, Grammar.TYPE_SPECIFIC) == 9


def test_replay_and_positive_control_boundaries() -> None:
    assert _unsafe_count(
        "TM_DUPLICATE_REPLAY",
        VariantName.DUPLICATE_VOTE_COUNTING,
        Grammar.PER_MESSAGE,
    ) == 0
    assert _unsafe_count(
        "TM_DUPLICATE_REPLAY",
        VariantName.DUPLICATE_VOTE_COUNTING,
        Grammar.PER_MESSAGE_REPLAY1,
    ) == 12
    assert _unsafe_count(
        "TM_VALIDATION_CONTROL",
        VariantName.RECEIVER_VALIDATION_OMISSION,
        Grammar.PARTITION,
    ) == 1


def test_minimal_typed_witness_passes_independent_oracle() -> None:
    case = case_by_id("TM_LOCK_OMISSION")
    variant = VARIANTS[VariantName.MISSING_LOCK_UPDATE]
    result = _result(case.case_id, variant.name, Grammar.TYPE_SPECIFIC)
    witness = min(
        (result.witnesses[observation] for observation in result.unsafe_observations),
        key=lambda item: item.rank(),
    )
    assert verify_witness(case, variant, witness) == witness.observation
