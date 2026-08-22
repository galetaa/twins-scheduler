#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gate6p"
sys.path.insert(0, str(ROOT / "src"))

from schedcheck.gate6.event_loop import evaluate_suite, order_sensitivity  # noqa: E402
from schedcheck.gate6.necessity import (  # noqa: E402
    exhaustive_premise_characterization,
    parameter_sensitivity,
)
from schedcheck.gate6.proof_kernel import (  # noqa: E402
    check_induction_certificate,
    check_quorum_pivot_certificate,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def verify_manifest(path: Path) -> None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        target = path.parent / relative
        require(target.exists(), f"manifest target missing: {relative}")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        require(actual == digest, f"hash mismatch: {relative}")


def main() -> None:
    decision = load("gate6p_decision.json")
    require(decision["status"] == "PASS", "Gate 6 decision is not PASS")
    require(
        decision["decision"] == "PASS / GO TO GATE 7'",
        "wrong Gate 6 decision",
    )

    checks = load("gate6p_machine_checks.json")
    require(checks["status"] == "PASS", "aggregate checks failed")
    require(
        all(value for key, value in checks.items() if key != "status"),
        "a Gate 6 machine check is false",
    )

    proof_dir = ROOT / "proofs_checked"
    require(
        check_induction_certificate(
            proof_dir / "t1_rules.json",
            proof_dir / "t1_replay_erasure_certificate.json",
        )["status"]
        == "PASS",
        "T1 proof certificate failed",
    )
    require(
        check_induction_certificate(
            proof_dir / "t2_rules.json",
            proof_dir / "t2_closure_lifting_certificate.json",
        )["status"]
        == "PASS",
        "T2 proof certificate failed",
    )
    require(
        check_quorum_pivot_certificate(
            proof_dir / "t3_quorum_pivot_certificate.json"
        )["status"]
        == "PASS",
        "T3 certificate failed",
    )

    characterization = exhaustive_premise_characterization()
    require(characterization["status"] == "PASS", "premise theorem failed")
    require(characterization["assignments_checked"] == 128, "truth table size")
    require(
        characterization["strict_patterns_in_field_order"]
        == ["0111111", "1101111", "1111111"],
        "unexpected strict premise patterns",
    )

    sensitivity = parameter_sensitivity(256, 256, 60617)
    require(sensitivity["status"] == "PASS", "parameter sensitivity failed")
    require(sensitivity["cases_checked"] == 512, "parameter corpus size")

    require(evaluate_suite()["status"] == "PASS", "Python event loop failed")
    order = order_sensitivity(random_seeds=256, first_seed=0)
    require(order["status"] == "PASS", "event-order sensitivity failed")
    require(order["case_runs_checked"] == 1548, "event-order corpus size")

    require(
        load("full_event_loop_conformance.json")["status"] == "PASS",
        "Go/Python event-loop conformance failed",
    )
    bigint = load("t3_bigint_crosscheck.json")
    require(bigint["status"] == "PASS", "Go big-int cross-check failed")
    require(bigint["cases_checked"] == 1028, "big-int corpus size")
    require(len(bigint["largest_f"]) == 400, "largest big-int size")

    with (OUT / "full_event_loop_matrix.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        matrix = list(csv.DictReader(handle))
    require(len(matrix) == 6, "unexpected event-loop case count")
    unsafe = [row for row in matrix if row["unsafe"] == "True"]
    require(
        [(row["grammar"], row["mutation"]) for row in unsafe]
        == [("G_T_TYPE_SPECIFIC", "MISSING_LOCK_UPDATE")],
        "unexpected unsafe event-loop cases",
    )

    if (ROOT / "CORE_RESULTS.sha256").exists():
        verify_manifest(ROOT / "CORE_RESULTS.sha256")
    if (ROOT / "ARTIFACT_MANIFEST.sha256").exists():
        verify_manifest(ROOT / "ARTIFACT_MANIFEST.sha256")

    print("GATE 6' SELF-CHECK PASS")
    print("checked_proofs=T1,T2,T3")
    print("premise_assignments=128")
    print("parameter_cases=512")
    print("bigint_cases=1028")
    print("event_loop_conformance=6/6")
    print("event_order_case_runs=1548")


if __name__ == "__main__":
    main()
