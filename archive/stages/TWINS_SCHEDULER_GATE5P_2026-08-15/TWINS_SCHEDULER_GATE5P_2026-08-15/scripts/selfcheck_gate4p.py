from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gate4p"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    decision = json.loads((OUT / "gate4p_decision.json").read_text(encoding="utf-8"))
    require(
        decision["status"] == "PASS / CONDITIONAL GO TO GATE 5'",
        "Gate 4' decision is not PASS",
    )
    require(decision["checks_pass"], "formal checks did not pass")
    require(decision["conformance_pass"], "conformance did not pass")

    checks = json.loads((OUT / "theorem_checks.json").read_text(encoding="utf-8"))
    require(all(checks.values()), f"failed theorem checks: {checks}")

    conformance = json.loads(
        (OUT / "conformance_summary.json").read_text(encoding="utf-8")
    )
    require(conformance["status"] == "PASS", "Go/Python conformance failed")
    require(conformance["cases"] == 134, "unexpected conformance corpus size")
    require(conformance["seed"] == 20260815, "unexpected conformance seed")
    require(
        conformance["source_sha256"]
        == "4419845a04729c23ba31cd2fb37daf792e1c1a10fba32f29163f60c6506f3c55",
        "pinned network.go hash changed",
    )
    require(
        sha256(ROOT / "inputs" / "hotstuff_snapshot" / "network.go")
        == conformance["source_sha256"],
        "local source snapshot does not match conformance metadata",
    )

    with (OUT / "language_matrix.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 60, "language matrix must contain 5 cases x 2 roles x 6 grammars")
    index = {(row["case_id"], row["variant"], row["grammar"]): row for row in rows}

    def unsafe(case: str, variant: str, grammar: str) -> int:
        return int(index[(case, variant, grammar)]["unsafe_observations"])

    for row in rows:
        if row["role"] == "baseline":
            require(int(row["unsafe_observations"]) == 0, f"unsafe baseline: {row}")

    require(unsafe("LOCK_OMISSION", "MISSING_LOCK_UPDATE", "G_D_DIRECTED_VIEW") == 0, "lock mutant visible too early")
    require(unsafe("LOCK_OMISSION", "MISSING_LOCK_UPDATE", "G_D1_DIRECTED_DELAY1") == 12, "lock delay separation changed")
    require(unsafe("LOCK_OMISSION", "MISSING_LOCK_UPDATE", "G_T_TYPE_SPECIFIC") == 9, "lock type separation changed")
    require(unsafe("QC_GUARD", "WRONG_QC_GUARD", "G_D1_DIRECTED_DELAY1") == 12, "QC delay separation changed")
    require(unsafe("TIMEOUT_CLASSIFICATION", "TIMEOUT_AS_PRECOMMIT", "G_D1_DIRECTED_DELAY1") == 0, "timeout should resist commit-delay-only model")
    require(unsafe("TIMEOUT_CLASSIFICATION", "TIMEOUT_AS_PRECOMMIT", "G_T_TYPE_SPECIFIC") == 9, "timeout phase separation changed")
    require(unsafe("DUPLICATE_REPLAY", "DUPLICATE_VOTE_COUNTING", "G_M_PER_MESSAGE") == 0, "duplicate mutant visible without replay")
    require(unsafe("DUPLICATE_REPLAY", "DUPLICATE_VOTE_COUNTING", "G_R_PER_MESSAGE_REPLAY1") == 12, "replay separation changed")
    require(unsafe("VALIDATION_OMISSION_CONTROL", "RECEIVER_VALIDATION_OMISSION", "G_P_PARTITION") == 1, "partition positive control changed")

    closures = json.loads(
        (OUT / "closure_counterfactuals.json").read_text(encoding="utf-8")
    )
    require(len(closures) == 6, "unexpected closure check count")
    require(
        all(item["mechanism_confirmed"] and not item["closed_unsafe"] for item in closures),
        "a closure did not destroy its selected witness",
    )

    witnesses = [
        json.loads(line)
        for line in (OUT / "witnesses.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    require(len(witnesses) == 18, "unexpected witness count")
    require(
        all(
            item["replay_status"] == "PASS"
            and item["independent_oracle_status"] == "PASS"
            for item in witnesses
        ),
        "a serialized witness failed validation",
    )

    print("SELF-CHECK PASS")
    print(
        "claims=baseline_safety,natural_phase_separation,delay_boundary,"
        "replay_boundary,positive_control,closures,independent_oracle,go_conformance"
    )


if __name__ == "__main__":
    main()
