#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import product
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from schedcheck.formal.vote_processing import LogicalVote, process_votes  # noqa: E402


def run(output: Path, max_length: int = 5) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    validators = ("B", "H1", "H2")
    requests: list[dict[str, object]] = []
    expected: list[dict[str, object]] = []
    sequences: list[tuple[str, ...]] = [()]
    for length in range(1, max_length + 1):
        sequences.extend(product(validators, repeat=length))

    for unique in (True, False):
        for sequence in sequences:
            votes = tuple(LogicalVote(1, 1, "PREVOTE", 0, v) for v in sequence)
            result = process_votes(
                votes, quorum=3, unique_by_logical_vote=unique
            )
            requests.append({"unique": unique, "quorum": 3, "votes": list(sequence)})
            expected.append(
                {
                    "contributions": result.contributions,
                    "quorum": result.quorum,
                    "accepted": [vote.validator for vote in result.accepted_sequence],
                }
            )

    payload = "".join(json.dumps(request, sort_keys=True) + "\n" for request in requests)
    completed = subprocess.run(
        ["go", "run", "."],
        cwd=ROOT / "conformance" / "comet_vote_fixture",
        input=payload,
        text=True,
        capture_output=True,
        check=True,
    )
    actual = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    if len(actual) != len(expected):
        raise AssertionError(f"fixture returned {len(actual)} rows; expected {len(expected)}")

    mismatches: list[dict[str, object]] = []
    for index, (request, want, got) in enumerate(zip(requests, expected, actual, strict=True)):
        if got != want:
            mismatches.append(
                {"index": index, "request": request, "expected": want, "actual": got}
            )

    summary: dict[str, object] = {
        "status": "PASS" if not mismatches else "FAIL",
        "source_model": "CometBFT v0.40.0 VoteSet duplicate handling",
        "controlled_mutation": "count message instances instead of unique logical validators",
        "max_sequence_length": max_length,
        "sequences_per_mode": len(sequences),
        "cases_checked": len(requests),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:20],
    }
    (output / "comet_vote_conformance.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    result = run(ROOT / "results" / "gate5p")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
