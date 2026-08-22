#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

project = Path(__file__).resolve().parents[1]
root = project / "formal" / "smt"
output_root = Path(os.environ.get("TWINS_OUTPUT_ROOT", project))
results_dir = output_root / "results" / "generated"
formal_results = output_root / "formal" / "smt"
results_dir.mkdir(parents=True, exist_ok=True)
formal_results.mkdir(parents=True, exist_ok=True)

def find_or_build_z3() -> str:
    found = shutil.which("z3")
    if found:
        return found
    lib_candidates = [
        Path("/usr/lib/x86_64-linux-gnu/libz3.so.4"),
        Path("/usr/lib/libz3.so.4"),
        Path("/usr/local/lib/libz3.so"),
    ]
    lib = next((p for p in lib_candidates if p.exists()), None)
    cc = shutil.which("cc") or shutil.which("gcc")
    src = project / "scripts" / "z3cli.c"
    out = project / ".cache" / "z3cli"
    out.parent.mkdir(parents=True, exist_ok=True)
    if lib and cc and src.exists():
        cp = subprocess.run([cc, "-O2", str(src), str(lib), "-o", str(out)], text=True, capture_output=True)
        if cp.returncode != 0:
            raise SystemExit(f"could not compile z3cli:\n{cp.stdout}{cp.stderr}")
        return str(out)
    raise SystemExit("z3 executable unavailable and local libz3 wrapper cannot be built")

z3 = find_or_build_z3()
rows = []
for kind, expected in (("positive", "unsat"), ("negative_controls", "sat")):
    for path in sorted((root / kind).glob("*.smt2")):
        cp = subprocess.run([z3, str(path)], text=True, capture_output=True)
        output = (cp.stdout + cp.stderr).strip()
        observed_lines = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
        first = observed_lines[0] if observed_lines else ""
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
with (formal_results / "results.csv").open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)
version = subprocess.check_output([z3, "--version"], text=True, stderr=subprocess.STDOUT).strip().splitlines()[-1]
summary = {
    "z3_version": version,
    "runner": os.path.relpath(z3, project) if str(z3).startswith(str(project)) else z3,
    "positive_unsat": sum(r["observed"] == "unsat" for r in rows if r["expected"] == "unsat"),
    "negative_sat": sum(r["observed"] == "sat" for r in rows if r["expected"] == "sat"),
    "total": len(rows),
    "status": "PASS",
}
(formal_results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
(results_dir / "smt_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
