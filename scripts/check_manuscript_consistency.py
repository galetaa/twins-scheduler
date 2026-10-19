#!/usr/bin/env python3
"""Check the generated LaTeX and the revised paper's declared proof scope."""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
problems: list[str] = []
documents: dict[str, str] = {}
for stem, target in (("manuscript", "body"), ("appendices", "appendices")):
    source = ROOT / f"manuscript/markdown/{stem}.md"
    generated = ROOT / f"manuscript/lipics/{target}.tex"
    documents[stem] = source.read_text(encoding="utf-8")
    expected = subprocess.check_output(
        ["pandoc", str(source), "-f", "markdown+raw_tex", "-t", "latex",
         "--top-level-division=section"], text=True,
    )
    if expected != generated.read_text(encoding="utf-8"):
        problems.append(f"{generated.relative_to(ROOT)} differs from Pandoc output")

main = documents["manuscript"]
theorems = re.findall(r"\*\*Theorem ([0-9]+)", main)
if theorems != ["1", "2", "3", "4", "5", "6"]:
    problems.append(f"main theorem sequence={theorems}")
required = {
    "behavioral contract": "Explicit persistence",
    "immutable outputs": "cannot withdraw signed output",
    "order coverage": "all** linear extensions",
    "transitive precedence": "Use transitive precedence",
    "weighted boundary": r"w(I\setminus A)+w(J)\ge d_1",
    "phase budget": r"t_* = \max(0,d_0+d_1-k-\alpha(H))",
    "source pin": "49b82838fcca442b2445f76605c101609ed04130",
    "scope of Lean": "completeness of the Python checker",
    "distinct event kinds": r"R_i\ne V_j",
    "cost synthesis": "weighted refinement characterization",
    "independent optimality": "certificate soundness",
    "resource scope": "returns unknown",
    "native scope": "not a native reproduction of the mutant disagreement",
    "transport scope": "FIFO-compatible admitted vote-envelope order",
    "static policy completion": "exact trace refinement",
    "general transition optimum": "general minimum-cost synthesis",
    "model coverage": "control-completeness",
    "abstraction transfer": "implementation-model optimality transfer",
    "whole-policy refinement": "policy elimination and finite progress",
    "observer integrity": "two unmutated observers",
}
full_text = main + "\n" + documents["appendices"]
for name, phrase in required.items():
    if phrase not in full_text:
        problems.append(f"missing revision obligation: {name}")
if "% STATEFUL_TABLE" in main:
    problems.append("stateful results table has not been populated")
if "Supporting proposition (replay erasure)" not in documents["appendices"]:
    problems.append("supporting replay result absent from appendix")

print(json.dumps({"status": "FAIL" if problems else "PASS",
                  "synchronized_pairs": 2, "main_theorems": theorems,
                  "problems": problems}, indent=2, sort_keys=True))
if problems:
    raise SystemExit(1)
