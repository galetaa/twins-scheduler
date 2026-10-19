#!/usr/bin/env python3
"""Execute normal-operation conformance checks in unmodified pinned CometBFT.

The source checkout is disposable and must have no modified tracked files.
An added upstream-package test reaches internal State methods without replacing
them. All four validators execute the original program. No network peers,
reactor, client mutation, fabricated honest vote, or disagreement is involved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
COMMIT = "49b82838fcca442b2445f76605c101609ed04130"
GO_TOOLCHAIN = "go1.25.0"
REPOSITORY = "https://github.com/cometbft/cometbft.git"
PACKAGE = "github.com/cometbft/cometbft/consensus"
SOURCE_FILES = (
    "consensus/state.go",
    "consensus/common_test.go",
    "types/vote.go",
    "types/vote_set.go",
    "types/priv_validator.go",
    "state/execution.go",
    "go.mod",
    "go.sum",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(command)}\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return result.stdout.strip()


def source_is_clean(source: Path) -> None:
    actual = run(["git", "rev-parse", "HEAD"], cwd=source)
    if actual != COMMIT:
        raise RuntimeError(f"Source revision is {actual}; expected {COMMIT}")
    modified = run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=source)
    if modified:
        raise RuntimeError(f"Refusing modified upstream source:\n{modified}")
    unexpected = [
        name for name in run(["git", "ls-files", "--others", "--exclude-standard"], cwd=source).splitlines()
        if name.endswith(".go") and name != "consensus/native_conformance_test.go"
    ]
    if unexpected:
        raise RuntimeError(f"Refusing unexpected untracked Go source: {unexpected}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=ROOT / ".cache/native_cometbft")
    output_root = Path(os.environ.get("TWINS_OUTPUT_ROOT", ROOT))
    parser.add_argument("--output-dir", type=Path, default=output_root / "results/native")
    parser.add_argument("--go", default=os.environ.get("GO", "go"))
    parser.add_argument("--race", action="store_true", help="also run the Go race detector")
    args = parser.parse_args()
    source, output = args.source_dir.resolve(), args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    log_dir = Path(os.environ.get("TWINS_LOG_DIR", output)).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--depth", "1", "--branch", "v0.39.3", REPOSITORY, str(source)], cwd=ROOT)
    source_is_clean(source)

    env = dict(os.environ)
    env["GOMODCACHE"] = str(ROOT / ".cache/go-mod")
    env["GOCACHE"] = str(ROOT / ".cache/go-build")
    env["GOWORK"] = "off"
    env["GOFLAGS"] = ""
    env["GOTOOLCHAIN"] = GO_TOOLCHAIN
    env["NATIVE_CONFORMANCE_OUTPUT"] = str(output / "native_conformance.json")
    # A populated module cache alone may not have a Go executable in PATH.
    go = args.go
    if shutil.which(go) is None and not Path(go).is_file():
        candidates = sorted((ROOT / ".cache/go-mod").glob("golang.org/toolchain@*/bin/go"))
        if not candidates:
            raise RuntimeError("Go is required. Install Go 1.25+ or pass --go /absolute/path/to/go")
        go = str(candidates[-1])
    version = run([go, "version"], cwd=source, env=env)
    environment = run([go, "env", "-json", "GOOS", "GOARCH", "GOVERSION", "CGO_ENABLED", "GOTOOLCHAIN"], cwd=source, env=env)

    harness = Path(__file__).with_name("native_conformance_test.go.txt")
    injected = source / "consensus/native_conformance_test.go"
    tracked = run(["git", "ls-files", "consensus/native_conformance_test.go"], cwd=source)
    if tracked:
        raise RuntimeError("Harness path collides with tracked upstream code")
    if injected.exists() and injected.read_bytes() != harness.read_bytes():
        raise RuntimeError(f"Refusing to overwrite a different untracked test: {injected}")
    injected.write_bytes(harness.read_bytes())
    source_hashes = {name: sha256(source / name) for name in SOURCE_FILES}

    command = [go, "test", "./consensus", "-run", "^TestNativeConformance$", "-count=1", "-timeout=120s", "-json"]
    if args.race:
        command.insert(2, "-race")
    try:
        test_run = subprocess.run(command, cwd=source, env=env, text=True, capture_output=True)
        (output / "native_test_events.jsonl").write_text(test_run.stdout)
        (output / "native_test_stderr.txt").write_text(test_run.stderr)
        if log_dir != output:
            (log_dir / "native_conformance_events.jsonl").write_text(test_run.stdout)
            (log_dir / "native_conformance_stderr.txt").write_text(test_run.stderr)
        if test_run.returncode:
            raise RuntimeError(f"Native test failure:\n{test_run.stdout}\n{test_run.stderr}")
        source_is_clean(source)
        if source_hashes != {name: sha256(source / name) for name in SOURCE_FILES}:
            raise RuntimeError("Production source changed during the run")
    finally:
        injected.unlink()

    evidence = json.loads((output / "native_conformance.json").read_text())
    events = [json.loads(line) for line in test_run.stdout.splitlines() if line.strip()]
    passed_tests = sorted(event["Test"] for event in events if event.get("Action") == "pass" and "Test" in event)
    if len(passed_tests) != 5 or not any(event.get("Action") == "pass" and event.get("Package") == PACKAGE and "Test" not in event for event in events):
        raise RuntimeError("Expected four passing scenarios and the passing parent/package receipts")
    if len(evidence["scenarios"]) != 4 or not all(scenario["passed"] for scenario in evidence["scenarios"]):
        raise RuntimeError("Native scenario evidence is incomplete")
    summary = {
        "schema": "native-cometbft-conformance-summary-v1",
        "upstream_commit": COMMIT,
        "pinned_go_toolchain": GO_TOOLCHAIN,
        "production_source_modified": False,
        "go_tests_passed_including_parent": len(passed_tests),
        "scenarios_passed": len(evidence["scenarios"]),
        "checks_passed": sum(len(item["checks"]) for item in evidence["scenarios"]),
        "native_signed_votes": sum(len(item["native_signed_votes"]) for item in evidence["scenarios"]),
        "scheduled_events": sum(len(item["events"]) for item in evidence["scenarios"]),
        "all_recorded_signatures_verified": all(vote["signature_verified"] for item in evidence["scenarios"] for vote in item["native_signed_votes"]),
        "race_detector": args.race,
        "scenarios": [{"name": item["name"], "checks": item["checks"], "native_signed_votes": len(item["native_signed_votes"]), "scheduled_events": len(item["events"])} for item in evidence["scenarios"]],
        "limits": [
            "Unmodified-source normal-operation conformance, not a fault-injection witness or native disagreement experiment.",
            "In-process State message/timeout dispatch and official local application fixture; no reactor, sockets, persistent validator signer, or WAL receive loop.",
            "Actual Ed25519 with deterministic test keys via upstream MockPV; no production key material.",
            "A fixed deterministic event order; native wall-clock timestamps/signatures are retained and need not be byte-identical across reruns.",
            "Four finite scenarios validate exercised guards; they are neither exhaustive verification nor a refinement proof.",
        ],
    }
    (output / "native_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    provenance = {
        "upstream_repository": REPOSITORY,
        "upstream_tag": "v0.39.3",
        "upstream_commit": COMMIT,
        "upstream_tree": run(["git", "rev-parse", "HEAD^{tree}"], cwd=source),
        "tracked_source_clean_before_and_after": True,
        "production_patch": None,
        "source_sha256": source_hashes,
        "harness_sha256": sha256(harness),
        "runner_sha256": sha256(Path(__file__)),
        "go_version": version,
        "go_environment": json.loads(environment),
        "command": ["go", *command[1:]],
        "command_exit_code": test_run.returncode,
        "passed_tests": passed_tests,
        "result_sha256": {name: sha256(output / name) for name in ("native_conformance.json", "native_summary.json", "native_test_events.jsonl", "native_test_stderr.txt")},
    }
    (output / "native_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    receipt = json.dumps({key: summary[key] for key in ("scenarios_passed", "checks_passed", "native_signed_votes", "scheduled_events", "all_recorded_signatures_verified", "race_detector")}, indent=2)
    if log_dir != output:
        (log_dir / "native_conformance.log").write_text(receipt + "\n")
    print(receipt)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
