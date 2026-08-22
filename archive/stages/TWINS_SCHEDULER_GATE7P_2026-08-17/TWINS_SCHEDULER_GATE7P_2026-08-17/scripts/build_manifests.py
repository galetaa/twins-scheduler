#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = [
    "GATE_STATUS.csv",
    "results/gate7p/gate7p_decision.json",
    "results/gate7p/gate7p_theorem_ledger.json",
    "results/gate7p/core_evidence_summary.json",
    "results/gate7p/extraction_equivalence.json",
    "proof_outputs/smt_proof_report.json",
    "results/gate7p/premise_characterization.json",
    "results/gate7p/premise_truth_table.csv",
    "results/gate7p/full_event_loop_matrix.csv",
    "results/gate7p/full_event_loop_conformance.json",
    "results/gate7p/t3_bigint_crosscheck.json",
    "results/gate7p/event_order_sensitivity.json",
    "paper_assets/MANIFEST.json",
]
EXCLUDED_PARTS = {".build", "__pycache__", ".pytest_cache", ".git"}
EXCLUDED_NAMES = {
    "ARTIFACT_MANIFEST.sha256",
    "CORE_RESULTS.sha256",
    "z3cli",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(path: Path, relative_paths: list[str]) -> None:
    lines = [f"{digest(ROOT / item)}  {item}" for item in sorted(relative_paths)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    for item in CORE:
        if not (ROOT / item).is_file():
            raise SystemExit(f"missing core file: {item}")
    write_manifest(ROOT / "CORE_RESULTS.sha256", CORE)
    all_files: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.name in EXCLUDED_NAMES:
            continue
        all_files.append(rel.as_posix())
    write_manifest(ROOT / "ARTIFACT_MANIFEST.sha256", all_files)
    print(f"MANIFESTS PASS core={len(CORE)} artifact={len(all_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
