#!/usr/bin/env python3
"""Solve or independently check minimum refinement of a finite transition model."""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/python"))
from twins_scheduler.transition_synthesis import Problem, SynthesisLimit, synthesize, verify_certificate


def read(path: Path):
    content = path.read_bytes()
    return json.loads(gzip.decompress(content) if path.suffix == ".gz" else content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--input", type=Path)
    mode.add_argument("--verify", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect-input", type=Path)
    parser.add_argument("--max-product-states", type=int, default=2_000_000)
    parser.add_argument("--time-budget-seconds", type=float)
    args = parser.parse_args()
    if args.verify:
        expected = None if args.expect_input is None else Problem.from_dict(read(args.expect_input))
        print(json.dumps(verify_certificate(read(args.verify), expected_problem=expected,
                                           max_checked_states=args.max_product_states,
                                           time_budget_seconds=args.time_budget_seconds), sort_keys=True))
        return
    if args.output is None:
        parser.error("--input requires --output")
    problem = Problem.from_dict(read(args.input))
    try:
        result = synthesize(problem, max_product_states=args.max_product_states,
                            time_budget_seconds=args.time_budget_seconds)
        audit = verify_certificate(result, expected_problem=problem)
    except SynthesisLimit as error:
        result = {"status": "unknown", "reason": str(error), "problem_sha256": problem.digest()}
        audit = result
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    args.output.write_bytes(gzip.compress(data, mtime=0) if args.output.suffix == ".gz" else data)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
