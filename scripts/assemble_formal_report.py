#!/usr/bin/env python3
"""Assemble deterministic evidence from the independently executed checkers."""
from __future__ import annotations

import json
import os
from pathlib import Path
from record_lean_verification import source_hashes


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = Path(os.environ.get("TWINS_OUTPUT_ROOT", ROOT))
GENERATED = OUTPUT_ROOT / "results" / "generated"


def load(name: str) -> object:
    return json.loads((GENERATED / name).read_text(encoding="utf-8"))


def main() -> None:
    lean = load("lean_verification.json")
    if lean["status"] != "PASS" or lean["source_sha256"] != source_hashes():
        raise SystemExit("Missing or stale Lean command evidence; run scripts/build_formal.sh")
    for command in ("lake_build_exit", "axiom_audit_exit", "leanchecker_exit"):
        if lean[command] != 0:
            raise SystemExit(f"Lean command failed: {command}")
    report = {
        "schema_version": 2,
        "status": "PASS",
        "primary_mature_prover": {
            "prover": "Lean",
            "toolchain": "leanprover/lean4:v4.33.0",
            "lake_build": "PASS",
            "axiom_audit": "PASS",
            "leanchecker": "PASS",
            "report": "formal/lean/AXIOM_REPORT.md",
            "receipt": "results/generated/lean_verification.json",
            "scope": lean["scope"],
        },
        "supporting_checks": {
            "smt": load("smt_summary.json"),
            "certificates": load("certificate_verification.json"),
            "independent_checker": load("independent_proof_checks.json"),
            "source_hygiene": load("formal_source_hygiene.json"),
        },
    }
    (GENERATED / "formal_verification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
