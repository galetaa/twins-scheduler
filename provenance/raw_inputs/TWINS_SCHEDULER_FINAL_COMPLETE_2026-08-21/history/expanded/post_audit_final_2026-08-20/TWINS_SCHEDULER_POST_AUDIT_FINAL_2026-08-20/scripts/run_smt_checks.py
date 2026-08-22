#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, shutil, subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "formal" / "smt_post_audit"
z3 = shutil.which("z3")
if not z3:
    raise SystemExit("z3 not found")
rows = []
for kind, expected in (("positive", "unsat"), ("negative_controls", "sat")):
    for path in sorted((root / kind).glob("*.smt2")):
        cp = subprocess.run([z3, str(path)], text=True, capture_output=True)
        output = (cp.stdout + cp.stderr).strip()
        first = output.splitlines()[0].strip() if output.splitlines() else ""
        passed = cp.returncode == 0 and first == expected
        rows.append({
            "file": str(path.relative_to(root)),
            "expected": expected,
            "observed": first,
            "exit_status": cp.returncode,
            "pass": passed,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
        if not passed:
            print(output, file=sys.stderr)
            raise SystemExit(f"unexpected Z3 result for {path}")
with (root / "results.csv").open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)
summary = {
    "z3_version": subprocess.check_output([z3, "--version"], text=True).strip(),
    "positive_unsat": sum(r["observed"] == "unsat" for r in rows if r["expected"] == "unsat"),
    "negative_sat": sum(r["observed"] == "sat" for r in rows if r["expected"] == "sat"),
    "total": len(rows),
    "status": "PASS",
}
(root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
