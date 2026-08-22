#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CORE = [
    "GATE_STATUS.csv",
    "results/gate6p/environment.json",
    "results/gate6p/event_order_sensitivity.json",
    "results/gate6p/full_event_loop_conformance.json",
    "results/gate6p/full_event_loop_go.json",
    "results/gate6p/full_event_loop_matrix.csv",
    "results/gate6p/full_event_loop_python.json",
    "results/gate6p/gate6p_decision.json",
    "results/gate6p/gate6p_machine_checks.json",
    "results/gate6p/gate6p_theorem_ledger.json",
    "results/gate6p/parameter_sensitivity.json",
    "results/gate6p/pinned_source_recheck.json",
    "results/gate6p/premise_ablation.csv",
    "results/gate6p/premise_ablation.json",
    "results/gate6p/premise_characterization.json",
    "results/gate6p/premise_truth_table.csv",
    "results/gate6p/proof_kernel_report.json",
    "results/gate6p/t1_replay_erasure_proof_check.json",
    "results/gate6p/t2_closure_lifting_proof_check.json",
    "results/gate6p/t3_bigint_crosscheck.json",
    "results/gate6p/t3_quorum_pivot_proof_check.json",
]

EXCLUDED_NAMES = {
    "ARTIFACT_MANIFEST.sha256",
}
EXCLUDED_PARTS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(path: Path, files: list[Path]) -> None:
    lines = [f"{digest(file)}  {file.relative_to(ROOT).as_posix()}" for file in files]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def include_artifact(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if path.name in EXCLUDED_NAMES:
        return False
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    if path.name == "run_log.txt" or path.name.endswith(".log"):
        return False
    return path.is_file()


def main() -> None:
    core_files = [ROOT / relative for relative in CORE]
    missing = [str(path.relative_to(ROOT)) for path in core_files if not path.exists()]
    if missing:
        raise SystemExit(f"missing core files: {missing}")
    write_manifest(ROOT / "CORE_RESULTS.sha256", core_files)

    artifact_files = sorted(
        (path for path in ROOT.rglob("*") if include_artifact(path)),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    write_manifest(ROOT / "ARTIFACT_MANIFEST.sha256", artifact_files)
    print(f"core_files={len(core_files)}")
    print(f"artifact_files={len(artifact_files)}")
    print(f"core_manifest_sha256={digest(ROOT / 'CORE_RESULTS.sha256')}")
    print(f"artifact_manifest_sha256={digest(ROOT / 'ARTIFACT_MANIFEST.sha256')}")


if __name__ == "__main__":
    main()
