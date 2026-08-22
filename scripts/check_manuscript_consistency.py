#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = (ROOT / "manuscript/markdown/manuscript.md").read_text(encoding="utf-8")
LATEX = (ROOT / "manuscript/lipics/body.tex").read_text(encoding="utf-8")

required_markdown = [
    "Premises 1--10",
    r"\mathsf{UnsafeObs}_{G_D}(P_f,B_f)=\varnothing",
    r"\mathsf{UnsafeObs}_{G_T}(P_f,B_f)\neq\varnothing",
    "state congruence",
    "output congruence",
    "X,X,Y",
    r"C(\tau)\in L_{G_D}(P,B)",
    r"S_2\land D\land T\land E_d\land X\land(S_1\lor R_q)",
    "MISSING_LOCK_UPDATE",
]
required_latex = [
    "Premises 1--10",
    r"\mathsf{UnsafeObs}_{G_D}(P_f,B_f)=\varnothing",
    r"\mathsf{UnsafeObs}_{G_T}(P_f,B_f)\neq\varnothing",
    "state congruence",
    "output congruence",
    "X,X,Y",
    r"C(\tau)\in L_{G_D}(P,B)",
    r"S_2\land D\land T\land E_d\land X\land(S_1\lor R_q)",
    r"MISSING\allowbreak\_LOCK\allowbreak\_UPDATE",
]
missing = [f"markdown:{x}" for x in required_markdown if x not in MARKDOWN]
missing += [f"latex:{x}" for x in required_latex if x not in LATEX]

markdown_theorems = re.findall(r"\*\*Theorem ([0-9]+)", MARKDOWN)
latex_theorems = re.findall(r"\\textbf\{Theorem ([0-9]+)", LATEX)
if markdown_theorems != ["1", "2", "3"]:
    missing.append(f"markdown theorem sequence={markdown_theorems}")
if latex_theorems != ["1", "2", "3"]:
    missing.append(f"latex theorem sequence={latex_theorems}")
for stale in ("mature-prover step as unavailable", "kernel build remains a release condition"):
    if stale in MARKDOWN or stale in LATEX:
        missing.append(f"stale assurance text:{stale}")

result = {
    "status": "PASS" if not missing else "FAIL",
    "markdown_theorems": markdown_theorems,
    "latex_theorems": latex_theorems,
    "missing_or_inconsistent": missing,
}
print(json.dumps(result, indent=2, sort_keys=True))
if missing:
    raise SystemExit(1)
