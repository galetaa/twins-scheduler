from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "gate4p")
    parser.add_argument("--seed", type=int, default=20260815)
    parser.add_argument("--random-cases", type=int, default=128)
    args = parser.parse_args()

    if shutil.which("go") is None:
        raise RuntimeError("Go is required for executable conformance")

    # Local imports keep the artifact dependency-free and avoid installation.
    import sys

    sys.path.insert(0, str(ROOT))
    from conformance.corpus import generate_corpus
    from conformance.python_harness import execute_corpus

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    payload = generate_corpus(args.seed, args.random_cases)
    executable_payload = {"cases": payload["cases"]}
    expected = execute_corpus(executable_payload)

    with tempfile.TemporaryDirectory(prefix="schedcheck-go-") as tmp:
        binary = Path(tmp) / "harness_fixture"
        _run(
            ["go", "build", "-trimpath", "-o", str(binary), "."],
            cwd=ROOT / "conformance" / "go_harness",
            capture_output=True,
        )
        completed = _run(
            [str(binary)],
            input=json.dumps(executable_payload, sort_keys=True),
            capture_output=True,
        )
        actual = json.loads(completed.stdout)

    if actual != expected:
        expected_by_id = {item["id"]: item for item in expected["results"]}
        actual_by_id = {item["id"]: item for item in actual["results"]}
        mismatches = [
            case_id
            for case_id in sorted(set(expected_by_id) | set(actual_by_id))
            if expected_by_id.get(case_id) != actual_by_id.get(case_id)
        ]
        raise AssertionError(f"Go/Python conformance mismatch: {mismatches[:10]}")

    go_version = _run(["go", "version"], capture_output=True).stdout.strip()
    source = ROOT / "inputs" / "hotstuff_snapshot" / "network.go"
    import hashlib

    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    summary = {
        "status": "PASS",
        "source_commit": "3179c6e62929294961acbfd9bf8445769716a121",
        "source_file": "inputs/hotstuff_snapshot/network.go",
        "source_sha256": source_sha256,
        "cases": len(payload["cases"]),
        "fixed_cases": len(payload["cases"]) - args.random_cases,
        "random_cases": args.random_cases,
        "seed": args.seed,
        "go_version": go_version,
        "python_version": platform.python_version(),
        "claims_checked": [
            "same-partition bypass",
            "drop-type filtering across partitions",
            "out-of-scenario drop-all rule",
            "sender-view message admission",
            "future-view pending queue",
            "idle-tick global-view advancement",
        ],
        "scope_limit": (
            "The fixture checks pinned network admission and queue semantics only; "
            "it does not execute the consensus event loops."
        ),
    }

    (output / "conformance_cases.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "conformance_results.json").write_text(
        json.dumps(actual, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "conformance_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
