#!/usr/bin/env python3
"""Generate the independently guarded n=4 Tendermint trace and timing controls."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

from twins_scheduler.concrete_trace import evaluate_suite  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(os.environ.get("TWINS_OUTPUT_ROOT", ROOT)) / "results" / "new",
    )
    arguments = parser.parse_args()
    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    suite = evaluate_suite()
    json_path = arguments.output_dir / "concrete_trace.json"
    json_path.write_text(json.dumps(suite, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    csv_path = arguments.output_dir / "concrete_trace.csv"
    fields = ["grammar", "variant", "repair_timing", "round1_b_prevote_route", "unsafe", "unmutated_observers_disagree",
              "A_decision", "P_decision", "C_decision", "signed_votes", "trace_events", "legality_audit",
              "admitted_vote_envelopes_fifo"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for case in suite["cases"]:
            row = {key: case[key] for key in fields[:6]}
            row.update({f"{name}_decision": case["decisions"].get(name, "none") for name in ("A", "P", "C")})
            row["signed_votes"] = sum(message["kind"] in ("PREVOTE", "PRECOMMIT") for message in case["messages"])
            row["trace_events"] = len(case["log"])
            row["legality_audit"] = "PASS" if all(case["audit"].values()) else "FAIL"
            row["admitted_vote_envelopes_fifo"] = case["vote_channel_order"]["admitted_vote_envelopes_fifo"]
            writer.writerow(row)
    print(json.dumps({"status": suite["status"], "checks": suite["checks"],
                      "cases": len(suite["cases"]), "json": str(json_path), "csv": str(csv_path)}, indent=2))
    if suite["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
