#!/usr/bin/env python3
"""Record successful Lean commands; called only by the fail-fast build script."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source_hashes() -> dict[str, str]:
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((ROOT / "formal/lean").rglob("*.lean"))}


if __name__ == "__main__":
    generated = Path(os.environ.get("TWINS_OUTPUT_ROOT", ROOT)) / "results/generated"
    generated.mkdir(parents=True, exist_ok=True)
    receipt = {"status": "PASS", "toolchain": (ROOT / "lean-toolchain").read_text().strip(),
               "lake_build_exit": 0, "axiom_audit_exit": 0, "leanchecker_exit": 0,
               "source_sha256": source_hashes(),
               "scope": "Imported Lean declarations include static-policy completion and least trace refinement, persistent-memory query guards, closed-sublevel certificates, labelled local simulation and cost-bound transfer, invariant-guided quotient refinement, graph/event-order realization, and Bellman certificate soundness. Python implementations, the protocol exporter, and production-client correspondence are not mechanized."}
    (generated / "lean_verification.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
