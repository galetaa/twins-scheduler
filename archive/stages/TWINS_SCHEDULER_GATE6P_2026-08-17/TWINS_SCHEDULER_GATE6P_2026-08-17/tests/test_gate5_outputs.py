from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gate5p"


def _json(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def test_gate5_machine_checks_and_decision_are_pass() -> None:
    checks = _json("gate5p_machine_checks.json")
    assert checks["status"] == "PASS"
    assert all(value for key, value in checks.items() if key != "status")
    decision = _json("gate5p_decision.json")
    assert decision["status"] == "PASS"
    assert decision["decision"] == "PASS / GO TO GATE 6'"


def test_tendermint_kernel_exact_counts_match_declared_boundaries() -> None:
    with (OUT / "tendermint_language_matrix.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    index = {
        (row["case_id"], row["role"], row["grammar"]): int(row["unsafe_observations"])
        for row in rows
    }
    for case in (
        "TM_LOCK_OMISSION",
        "TM_VALID_ROUND_GUARD",
        "TM_DUPLICATE_REPLAY",
        "TM_VALIDATION_CONTROL",
    ):
        for grammar in (
            "G_P_PARTITION",
            "G_D_DIRECTED_VIEW",
            "G_D1_DIRECTED_DELAY1",
            "G_T_TYPE_SPECIFIC",
            "G_M_PER_MESSAGE",
            "G_R_PER_MESSAGE_REPLAY1",
        ):
            assert index[(case, "baseline", grammar)] == 0

    assert index[("TM_LOCK_OMISSION", "mutant", "G_D_DIRECTED_VIEW")] == 0
    assert index[("TM_LOCK_OMISSION", "mutant", "G_T_TYPE_SPECIFIC")] == 9
    assert index[("TM_VALID_ROUND_GUARD", "mutant", "G_D_DIRECTED_VIEW")] == 0
    assert index[("TM_VALID_ROUND_GUARD", "mutant", "G_T_TYPE_SPECIFIC")] == 9
    assert index[("TM_DUPLICATE_REPLAY", "mutant", "G_M_PER_MESSAGE")] == 0
    assert index[("TM_DUPLICATE_REPLAY", "mutant", "G_R_PER_MESSAGE_REPLAY1")] == 12
    assert index[("TM_VALIDATION_CONTROL", "mutant", "G_P_PARTITION")] == 1


def test_cross_protocol_matrix_preserves_detection_classes() -> None:
    with (OUT / "cross_protocol_result_matrix.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 24
    assert all(row["same_zero_nonzero_class"] == "True" for row in rows)


def test_all_second_kernel_witnesses_replay_and_pass_independent_oracle() -> None:
    rows = [
        json.loads(line)
        for line in (OUT / "tendermint_witnesses.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]
    assert rows
    assert all(row["replay_status"] == "PASS" for row in rows)
    assert all(row["independent_oracle_status"] == "PASS" for row in rows)
