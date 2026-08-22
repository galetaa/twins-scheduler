from __future__ import annotations

from pathlib import Path

from schedcheck.formal.source_mapping import verify_source_mapping
from schedcheck.formal.vote_processing import exhaustive_replay_check
from schedcheck.gate5.closure import closure_theorem_checks
from schedcheck.gate5.phase import check_phase_coupled_separation
from schedcheck.gate5.phase_coupled import phase_coupled_separation_check

ROOT = Path(__file__).resolve().parents[1]


def test_replay_erasure_and_one_replay_boundary() -> None:
    result = exhaustive_replay_check(max_length=5)
    assert result["replay_erasure_holds_for_idempotent_processing"]
    assert result["non_idempotent_processing_has_strict_separation"]
    assert result["minimal_non_idempotent_separation"] == ["B", "H1", "H1"]
    assert result["sequences_checked"] == 364


def test_relational_closure_theorem_has_positive_and_negative_examples() -> None:
    result = closure_theorem_checks()
    assert result["status"] == "PASS"
    assert result["monotone_example"]["conditions"]["status"] == "PASS"
    assert result["monotone_example"]["unsafe_preserved"]
    fragile = result["locking_fragility_counterexample"]
    assert fragile["conditions"]["status"] == "FAIL"
    assert fragile["unsafe_before"]
    assert not fragile["unsafe_after"]


def test_phase_coupled_finite_and_parametric_checks() -> None:
    finite = check_phase_coupled_separation()
    assert not finite["baseline"]["directed_unsafe"]
    assert not finite["baseline"]["typed_unsafe"]
    assert finite["constraint_omission"]["strict_safety_separation"]

    family = phase_coupled_separation_check(max_f=8)
    assert family["status"] == "PASS"
    assert family["checked_fault_bounds"] == list(range(1, 9))
    for row in family["rows"]:
        assert row["q0_size"] == row["quorum"]
        assert row["q1_size"] == row["quorum"]
        assert len(row["intersection"]) == row["f"] + 1
        assert row["type_specific_unsafe"]
        assert not row["directed_unsafe"]
        assert row["delay1_unsafe"]


def test_pinned_cometbft_source_obligations() -> None:
    result = verify_source_mapping(ROOT)
    assert result["status"] == "PASS"
    assert result["tag_commit"] == "0880b4d378f347ab16e54ec677ff50d803f37d62"
    assert all(row["status"] == "PASS" for row in result["obligations"])
