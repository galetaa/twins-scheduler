from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


def _line_of(lines: list[str], needle: str, start: int = 0) -> int:
    for index in range(start, len(lines)):
        if needle in lines[index]:
            return index + 1
    raise AssertionError(f"source pattern not found: {needle}")


def run(root: Path, output: Path) -> dict[str, object]:
    source_dir = root / "inputs" / "cometbft_v0.40.0"
    state_lines = (source_dir / "state.go").read_text(encoding="utf-8").splitlines()
    vote_lines = (source_dir / "vote_set.go").read_text(encoding="utf-8").splitlines()
    spec_lines = (source_dir / "consensus.md").read_text(encoding="utf-8").splitlines()

    lock_line = _line_of(state_lines, "cs.LockedRound = round")
    precommit_line = _line_of(
        state_lines,
        "cs.signAddVote(cmtproto.PrecommitType",
        start=lock_line - 1,
    )
    duplicate_contract_line = _line_of(
        vote_lines, "Duplicate votes return added=false, err=nil."
    )
    duplicate_return_line = _line_of(vote_lines, "return false, nil // duplicate")
    precommit_spec_line = _line_of(spec_lines, "### Precommit Step")

    source_checks = {
        "lock_assignment_precedes_precommit_call": lock_line < precommit_line,
        "duplicate_vote_contract_present": duplicate_contract_line > 0,
        "duplicate_vote_return_present": duplicate_return_line > 0,
        "precommit_step_specified": precommit_spec_line > 0,
    }

    fixture = root / "implementation_fixture" / "go_harness"
    test = subprocess.run(
        ["go", "test", "./..."],
        cwd=fixture,
        check=False,
        capture_output=True,
        text=True,
    )
    if test.returncode != 0:
        raise AssertionError(test.stdout + test.stderr)
    execution = subprocess.run(
        ["go", "run", "."],
        cwd=fixture,
        check=False,
        capture_output=True,
        text=True,
    )
    if execution.returncode != 0:
        raise AssertionError(execution.stdout + execution.stderr)
    fixture_result = json.loads(execution.stdout)
    fixture_checks = {
        "unique_vote_replay_is_inert": (
            fixture_result["unique_first_added"]
            and not fixture_result["unique_replay_added"]
            and not fixture_result["unique_quorum_after_replay"]
        ),
        "instance_counting_replay_reaches_spurious_quorum": fixture_result[
            "instance_quorum_after_replay"
        ],
        "lock_established_before_precommit": fixture_result[
            "baseline_locked_before_precommit"
        ],
        "baseline_lock_blocks_conflict": fixture_result[
            "baseline_rejects_conflict"
        ],
        "controlled_lock_omission_enables_conflict": fixture_result[
            "mutation_supports_conflict"
        ],
    }

    source_hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(source_dir.iterdir())
        if path.is_file()
    }
    result: dict[str, object] = {
        "status": "PASS" if all(source_checks.values()) and all(fixture_checks.values()) else "FAIL",
        "scope": (
            "Executable correspondence for vote de-duplication and lock-before-"
            "precommit ordering only; not a full CometBFT consensus conformance test."
        ),
        "source": json.loads((source_dir / "SOURCE.json").read_text(encoding="utf-8")),
        "source_hashes": source_hashes,
        "source_locations": {
            "lock_assignment_line": lock_line,
            "subsequent_precommit_call_line": precommit_line,
            "duplicate_contract_line": duplicate_contract_line,
            "duplicate_return_line": duplicate_return_line,
            "precommit_spec_line": precommit_spec_line,
        },
        "source_checks": source_checks,
        "go_test_status": "PASS",
        "go_test_command": "go test ./...",
        "fixture_result": fixture_result,
        "fixture_checks": fixture_checks,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "implementation_correspondence.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(run(root, root / "results" / "gate5p"), indent=2, sort_keys=True))
