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
if theorems != ["1", "2", "3"]:
    problems.append(f"main theorem sequence={theorems}")
required = {
    "behavioral contract": "Explicit persistence",
    "immutable outputs": "cannot withdraw signed output",
    "order coverage": "all** linear extensions",
    "transitive precedence": "Use transitive precedence",
    "weighted boundary": r"w(I\setminus A)+w(J)\ge d_1",
    "phase budget": r"t_* = \max(0,d_0+d_1-k-\alpha(H))",
    "source pin": "49b82838fcca442b2445f76605c101609ed04130",
    "scope of Lean": "not** claimed to be fully mechanized",
    "transport scope": "FIFO-compatible admitted vote-envelope order",
}
for name, phrase in required.items():
    if phrase not in main:
        problems.append(f"missing revision obligation: {name}")
if "Supporting proposition (replay erasure)" not in documents["appendices"]:
    problems.append("supporting replay result absent from appendix")

print(json.dumps({"status": "FAIL" if problems else "PASS",
                  "synchronized_pairs": 2, "main_theorems": theorems,
                  "problems": problems}, indent=2, sort_keys=True))
if problems:
    raise SystemExit(1)
