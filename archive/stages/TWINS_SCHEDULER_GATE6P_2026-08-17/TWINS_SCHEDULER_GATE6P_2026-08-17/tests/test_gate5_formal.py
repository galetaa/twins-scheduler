from __future__ import annotations

from pathlib import Path

from schedcheck.formal.source_mapping import verify_source_mapping
from schedcheck.formal.vote_processing import exhaustive_replay_check
from schedcheck.gate5.closure import closure_theorem_checks
from schedcheck.gate5.phase_coupled import phase_coupled_separation_check

ROOT = Path(__file__).resolve().parents[1]


def test_relational_closure_theorem_has_positive_and_negative_boundary() -> None:
    result = closure_theorem_checks()
    assert result["status"] == "PASS"
    assert result["monotone_example"]["unsafe_preserved"]
    counterexample = result["locking_fragility_counterexample"]
    assert counterexample["unsafe_before"]
    assert not counterexample["unsafe_after"]
    assert counterexample["conditions"]["status"] == "FAIL"


def test_phase_coupled_family_is_parametric_through_f8() -> None:
    result = phase_coupled_separation_check(max_f=8)
    assert result["status"] == "PASS"
    assert result["checked_fault_bounds"] == list(range(1, 9))
    for row in result["rows"]:
        assert row["q0_size"] == row["quorum"]
        assert row["q1_size"] == row["quorum"]
        assert len(row["intersection"]) == row["f"] + 1
        assert row["type_specific_unsafe"]
        assert not row["directed_unsafe"]
        assert row["delay1_unsafe"]


def test_replay_erasure_and_strict_non_idempotent_boundary() -> None:
    result = exhaustive_replay_check(max_length=5)
    assert result["replay_erasure_holds_for_idempotent_processing"]
    assert result["non_idempotent_processing_has_strict_separation"]
    assert result["minimal_non_idempotent_separation"] == ["B", "H1", "H1"]
    assert result["sequences_checked"] == 364


def test_pinned_cometbft_source_obligations_all_match() -> None:
    result = verify_source_mapping(ROOT)
    assert result["status"] == "PASS"
    assert all(row["status"] == "PASS" for row in result["obligations"])
    assert all(not row["missing_fragments"] for row in result["obligations"])
