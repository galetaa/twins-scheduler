#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gate5p"
sys.path.insert(0, str(ROOT / "src"))

from schedcheck.formal.source_mapping import verify_source_mapping  # noqa: E402
from schedcheck.formal.vote_processing import exhaustive_replay_check  # noqa: E402
from schedcheck.gate5.closure import closure_theorem_checks  # noqa: E402
from schedcheck.gate5.phase_coupled import phase_coupled_separation_check  # noqa: E402


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
    decision = load("gate5p_decision.json")
    require(decision["status"] == "PASS", "Gate 5 decision is not PASS")
    require(decision["decision"] == "PASS / GO TO GATE 6'", "wrong gate decision")

    checks = load("gate5p_machine_checks.json")
    require(checks["status"] == "PASS", "aggregate checks failed")
    require(all(v for k, v in checks.items() if k != "status"), "a machine check is false")

    theorem = load("gate5p_theorem_ledger.json")
    require(theorem["T1_replay_erasure"]["executable_status"] == "PASS", "T1 failed")
    require(theorem["T2_local_closure_lifting"]["executable_status"] == "PASS", "T2 failed")
    require(theorem["T3_phase_coupled_separation"]["family_check_status"] == "PASS", "T3 family failed")
    require(theorem["T4_bounded_terminal_delay"]["executable_status"] == "PASS", "T4 failed")
    require(theorem["T5_non_idempotent_replay_separation"]["executable_status"] == "PASS", "T5 failed")

    require(closure_theorem_checks()["status"] == "PASS", "closure theorem self-check failed")
    require(phase_coupled_separation_check(8)["status"] == "PASS", "phase family self-check failed")
    replay = exhaustive_replay_check(5)
    require(replay["sequences_checked"] == 364, "unexpected replay state space")
    require(replay["replay_erasure_holds_for_idempotent_processing"], "replay erasure failed")
    require(verify_source_mapping(ROOT)["status"] == "PASS", "source mapping failed")

    witnesses = [
        json.loads(line)
        for line in (OUT / "tendermint_witnesses.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    require(len(witnesses) == 15, "unexpected witness count")
    require(all(w["replay_status"] == "PASS" for w in witnesses), "witness replay failed")
    require(all(w["independent_oracle_status"] == "PASS" for w in witnesses), "oracle failed")

    with (OUT / "cross_protocol_result_matrix.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 24, "unexpected cross-protocol row count")
    require(all(row["same_zero_nonzero_class"] == "True" for row in rows), "transfer mismatch")

    require(load("comet_vote_conformance.json")["cases_checked"] == 728, "Go corpus size mismatch")
    require(load("comet_vote_conformance.json")["status"] == "PASS", "Go conformance failed")
    require(load("implementation_correspondence.json")["status"] == "PASS", "implementation fixture failed")

    verify_manifest(ROOT / "archive" / "gate4p_frozen" / "MANIFEST.sha256")
    if (ROOT / "CORE_RESULTS.sha256").exists():
        verify_manifest(ROOT / "CORE_RESULTS.sha256")

    print("GATE 5' SELF-CHECK PASS")
    print("formal_results=T1,T2,T3,T4,T5")
    print("second_kernel_witnesses=15")
    print("go_python_cases=728")
    print("phase_family=f1..f8")


if __name__ == "__main__":
    main()
