#!/usr/bin/env python3
"""Run solver-checked SMT/CHC obligations and falsifying controls."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SMT = ROOT / "proofs_smt"
OUT = ROOT / "proof_outputs"
BINARY = SMT / "z3cli"
SOURCE = SMT / "z3cli.c"
PINNED_VERSION = "4.13.3.0"

POSITIVE: tuple[tuple[str, int, str, str], ...] = (
    (
        "T1_REPLAY_ERASURE.horn.smt2",
        1,
        "HORN",
        "Unbounded finite-prefix equality invariant under stable-key stuttering.",
    ),
    (
        "T2_LOCAL_VCS.smt2",
        4,
        "AUFLIA",
        "Transitivity, increasing insertion, forward simulation, and upward closure.",
    ),
    (
        "T2_PREFIX_RELATION.horn.smt2",
        1,
        "HORN",
        "Finite-prefix induction skeleton, composed with the local VCs and the separate certificate proof.",
    ),
    (
        "T3_QUORUM_PIVOT.smt2",
        1,
        "QF_LIA",
        "Exact parametric quorum arithmetic and both directed branches for every f>=1.",
    ),
    (
        "T6_PREMISE_CHARACTERIZATION.smt2",
        1,
        "QF_LIA",
        "Exact symbolic equivalence of the operational and Boolean seven-flag models.",
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_count(text: str, token: str) -> int:
    return len(re.findall(rf"(?m)^{re.escape(token)}$", text))


def build_wrapper() -> dict[str, str]:
    compiler = shutil.which("cc") or shutil.which("gcc")
    if compiler is None:
        raise RuntimeError("C compiler not found")
    command = [
        compiler,
        "-O2",
        "-std=c11",
        "-Wall",
        "-Wextra",
        str(SOURCE),
        "-Wl,-l:libz3.so.4",
        "-o",
        str(BINARY),
    ]
    process = subprocess.run(command, text=True, capture_output=True, check=False)
    if process.returncode != 0:
        raise RuntimeError(f"wrapper build failed\n{process.stdout}\n{process.stderr}")
    version = subprocess.run(
        [str(BINARY), "--version"], text=True, capture_output=True, check=True
    ).stdout.strip()
    compiler_version = subprocess.run(
        [compiler, "--version"], text=True, capture_output=True, check=True
    ).stdout.splitlines()[0]
    return {
        "z3_full_version": version,
        "compiler": compiler_version,
        "source_sha256": sha256(SOURCE),
        "binary_sha256": sha256(BINARY),
    }


def run_file(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(BINARY), str(path)],
        text=True,
        capture_output=True,
        timeout=40,
        check=False,
    )


def persist_output(path: Path, process: subprocess.CompletedProcess[str]) -> tuple[Path, Path]:
    stem = path.stem.replace(".horn", "_horn")
    stdout_path = OUT / f"{stem}.out"
    stderr_path = OUT / f"{stem}.err"
    stdout_path.write_text(process.stdout, encoding="utf-8")
    stderr_path.write_text(process.stderr, encoding="utf-8")
    return stdout_path, stderr_path


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for path in OUT.iterdir():
        if path.is_file():
            path.unlink()

    build = build_wrapper()
    rows: list[dict[str, object]] = []

    for name, expected_unsat, logic, purpose in POSITIVE:
        source = SMT / name
        process = run_file(source)
        stdout_path, stderr_path = persist_output(source, process)
        unsat = result_count(process.stdout, "unsat")
        sat = result_count(process.stdout, "sat")
        unknown = result_count(process.stdout, "unknown")
        status = (
            "PASS"
            if process.returncode == 0
            and unsat == expected_unsat
            and sat == 0
            and unknown == 0
            and "(error" not in process.stdout
            and build["z3_full_version"] == PINNED_VERSION
            else "FAIL"
        )
        rows.append(
            {
                "kind": "positive_obligation",
                "name": name,
                "logic": logic,
                "purpose": purpose,
                "expected": ["unsat"] * expected_unsat,
                "observed_unsat_count": unsat,
                "source_sha256": sha256(source),
                "stdout_sha256": sha256(stdout_path),
                "stdout_bytes": stdout_path.stat().st_size,
                "stderr_sha256": sha256(stderr_path),
                "status": status,
            }
        )

    for source in sorted((SMT / "negative_controls").glob("*.smt2")):
        process = run_file(source)
        stdout_path, stderr_path = persist_output(source, process)
        sat = result_count(process.stdout, "sat")
        unknown = result_count(process.stdout, "unknown")
        status = (
            "PASS"
            if process.returncode == 0 and sat == 1 and unknown == 0 and "(error" not in process.stdout
            else "FAIL"
        )
        rows.append(
            {
                "kind": "negative_control",
                "name": source.name,
                "logic": "HORN" if ".horn." in source.name else "QF_LIA",
                "purpose": source.read_text(encoding="utf-8").splitlines()[1].lstrip("; "),
                "expected": ["sat"],
                "observed_sat_count": sat,
                "source_sha256": sha256(source),
                "stdout_sha256": sha256(stdout_path),
                "stdout_bytes": stdout_path.stat().st_size,
                "stderr_sha256": sha256(stderr_path),
                "status": status,
            }
        )

    report = {
        "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
        "prover": "Microsoft Z3",
        "version": build["z3_full_version"],
        "pinned_version": PINNED_VERSION,
        "invocation": "SMT-LIB 2 through a minimal Z3 C-API loader",
        "wrapper_build": build,
        "checks": rows,
        "scope": {
            "discharged": [
                "T1 unbounded finite-prefix equality invariant under explicit replay premises",
                "T2 local first-order VCs and finite-prefix induction skeleton",
                "T3 exact parametric quorum arithmetic",
                "T6 exact seven-flag symbolic equivalence",
            ],
            "not_discharged": [
                "full production-client refinement",
                "liveness, timers, weighted quorums, or resource-visible replay",
                "universal scheduler minimality or incompleteness",
            ],
        },
        "trust_boundary": [
            "Z3 4.13.3.0 runtime and SMT/CHC engines",
            "SMT/CHC encodings and statement-to-encoding mapping",
            "minimal C loader",
            "for T2 generic induction composition: the separate small certificate kernel",
        ],
        "external_review": "NOT_PERFORMED",
    }
    (OUT / "z3_version.txt").write_text(build["z3_full_version"] + "\n", encoding="utf-8")
    (OUT / "smt_proof_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
