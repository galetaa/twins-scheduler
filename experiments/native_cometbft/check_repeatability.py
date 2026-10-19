#!/usr/bin/env python3
"""Repeat the native conformance scripts and compare their semantic summaries."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    out_root = Path(os.environ.get("TWINS_OUTPUT_ROOT", ROOT))
    evidence_dir = out_root / "results/native"
    reference = json.loads((evidence_dir / "native_summary.json").read_text())
    work = ROOT / ".cache/native_repeatability"
    receipts = []
    for attempt in range(4):
        race = attempt == 3
        root = work / ("race" if race else f"repeat_{attempt + 1}")
        env = dict(os.environ)
        env["TWINS_OUTPUT_ROOT"] = str(root)
        env["TWINS_LOG_DIR"] = str(root / "build_logs")
        command = [sys.executable, str(Path(__file__).with_name("run.py"))]
        if race:
            command.append("--race")
        result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(f"Repeat {attempt + 1} failed:\n{result.stdout}\n{result.stderr}")
        generated = root / "results/native"
        summary = json.loads((generated / "native_summary.json").read_text())
        normalized = dict(summary, race_detector=reference["race_detector"])
        assert normalized == reference, "native semantic outcome changed between repetitions"
        assert (root / "build_logs/native_conformance.log").is_file(), "TWINS_LOG_DIR was not honored"
        provenance = json.loads((generated / "native_provenance.json").read_text())
        events = [json.loads(line) for line in (generated / "native_test_events.jsonl").read_text().splitlines()]
        receipts.append({
            "attempt": attempt + 1,
            "race_detector": race,
            "command_exit_code": result.returncode,
            "semantic_summary_identical": True,
            "raw_evidence_sha256": sha(generated / "native_conformance.json"),
            "go_test_receipt_sha256": sha(generated / "native_test_events.jsonl"),
            "go_test_pass_events": [event for event in events if event.get("Action") == "pass"],
            "upstream_source_unchanged": provenance["tracked_source_clean_before_and_after"],
            "go_version": provenance["go_version"],
            "runner_sha256": provenance["runner_sha256"],
            "harness_sha256": provenance["harness_sha256"],
        })
    report = {
        "status": "PASS",
        "normal_repetitions": 3,
        "race_detector_repetitions": 1,
        "scenarios_per_run": reference["scenarios_passed"],
        "all_semantic_summaries_identical": True,
        "race_detector_reported_no_race": True,
        "output_and_log_routing_verified": True,
        "reference_summary_sha256": sha(evidence_dir / "native_summary.json"),
        "script_sha256": sha(Path(__file__)),
        "receipts": receipts,
        "scope": "Three additional fixed-script repetitions and one race-detector run; no random schedule coverage or native safety proof is claimed.",
    }
    (evidence_dir / "native_repeatability.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "normal_repetitions", "race_detector_repetitions", "all_semantic_summaries_identical", "output_and_log_routing_verified")}, indent=2))


if __name__ == "__main__":
    main()
