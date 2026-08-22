#!/usr/bin/env python3
"""Check the frozen Gate 7′ artifact without regenerating it."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"SELF-CHECK FAIL: {message}")


def main() -> int:
    decision = load("results/gate7p/gate7p_decision.json")
    core = load("results/gate7p/core_evidence_summary.json")
    extraction = load("results/gate7p/extraction_equivalence.json")
    smt = load("proof_outputs/smt_proof_report.json")
    theorem = load("results/gate7p/gate7p_theorem_ledger.json")
    paper = load("paper_assets/MANIFEST.json")
    premises = load("results/gate7p/premise_characterization.json")
    conformance = load("results/gate7p/full_event_loop_conformance.json")
    order = load("results/gate7p/event_order_sensitivity.json")

    require(decision["status"] == "PASS_GO_TO_GATE8_MANUSCRIPT_SUBMISSION_HOLD", "gate decision")
    require(decision["submission_ready"] is False, "submission hold must remain explicit")
    require(core["status"] == "PASS", "core evidence")
    require(extraction["status"] == "PASS" and extraction["files_checked"] == 15, "Gate 6 byte equivalence")
    require(smt["status"] == "PASS", "SMT migration")
    require(theorem["status"] == "PASS" and len(theorem["theorems"]) == 4, "theorem ledger")
    require(premises["assignments_checked"] == 128 and not premises["mismatches"], "premise boundary")
    require(conformance["status"] == "PASS" and conformance["cases_checked"] == 6, "Go/Python conformance")
    require(order["status"] == "PASS" and order["case_runs_checked"] == 1548, "order sensitivity")
    require(paper["status"] == "PASS" and len(paper["outputs"]) == 24, "paper assets")
    for row in paper["outputs"]:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing paper asset {row['path']}")
        require(sha256(path) == row["sha256"], f"paper asset digest {row['path']}")
    lean_readme = (ROOT / "formal/lean/README.md").read_text(encoding="utf-8").upper()
    require("NOT" in lean_readme and "KERNEL" in lean_readme and "CHECK" in lean_readme, "Lean status warning")
    print("GATE 7' SELF-CHECK PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
