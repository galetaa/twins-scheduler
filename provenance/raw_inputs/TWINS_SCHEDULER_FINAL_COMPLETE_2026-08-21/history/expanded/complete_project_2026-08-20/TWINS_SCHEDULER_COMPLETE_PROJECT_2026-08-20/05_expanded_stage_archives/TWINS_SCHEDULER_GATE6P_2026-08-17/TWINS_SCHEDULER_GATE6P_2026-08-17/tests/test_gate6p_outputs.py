from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gate6p"


def load(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def test_gate6_decision_and_machine_checks_pass() -> None:
    checks = load("gate6p_machine_checks.json")
    assert checks["status"] == "PASS"
    assert all(value for key, value in checks.items() if key != "status")
    decision = load("gate6p_decision.json")
    assert decision["status"] == "PASS"
    assert decision["decision"] == "PASS / GO TO GATE 7'"
    assert "NOT_YET_SUBMISSION_READY" in decision["publication_readiness"]


def test_gate6_theorem_ledger_is_narrow_and_complete() -> None:
    ledger = load("gate6p_theorem_ledger.json")
    assert ledger["T1_replay_erasure"]["status"] == (
        "CHECKED_BY_SMALL_TRUSTED_PROOF_SCRIPT"
    )
    assert ledger["T2_relational_closure_lifting"]["status"] == (
        "CHECKED_BY_SMALL_TRUSTED_PROOF_SCRIPT"
    )
    assert ledger["T3_parametric_quorum_pivot_separation"]["status"] == (
        "CHECKED_CERTIFICATE_PLUS_INDEPENDENT_BIGINT_CROSSCHECK"
    )
    assert ledger["T6_boolean_premise_characterization"][
        "assignments_checked"
    ] == 128


def test_full_event_loop_matrix_has_six_cases_and_one_unsafe_mutant() -> None:
    with (OUT / "full_event_loop_matrix.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6
    unsafe = [
        row
        for row in rows
        if row["unsafe"] == "True"
    ]
    assert [(row["grammar"], row["mutation"]) for row in unsafe] == [
        ("G_T_TYPE_SPECIFIC", "MISSING_LOCK_UPDATE")
    ]


def test_complete_truth_table_is_serialized() -> None:
    with (OUT / "premise_truth_table.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 128
    assert sum(row["actual_strict_separation"] == "True" for row in rows) == 3
    assert all(
        row["actual_strict_separation"]
        == row["characterization_predicts"]
        for row in rows
    )
