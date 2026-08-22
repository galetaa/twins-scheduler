#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0
export PYTHONPATH="$ROOT/src"

CORE_BASELINE="$(mktemp)"
ARTIFACT_BASELINE="$(mktemp)"
cp CORE_RESULTS.sha256 "$CORE_BASELINE"
cp ARTIFACT_MANIFEST.sha256 "$ARTIFACT_BASELINE"

cleanup() {
  rm -f "$CORE_BASELINE" "$ARTIFACT_BASELINE" "$ROOT/proofs_smt/z3cli"
  find "$ROOT" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
  find "$ROOT" -type d -name .pytest_cache -prune -exec rm -rf {} + 2>/dev/null || true
}
trap cleanup EXIT

# Verify the received archive before executing any generated code.
sha256sum -c "$ARTIFACT_BASELINE" >/dev/null

python3 scripts/run_gate7p.py
rm -f proofs_smt/z3cli
python3 scripts/selfcheck_gate7p.py

# Compare regenerated decisive files and the complete non-transient payload to
# the frozen manifests copied before the run.  Do not rewrite either baseline.
sha256sum -c "$CORE_BASELINE" >/dev/null
sha256sum -c "$ARTIFACT_BASELINE" >/dev/null

echo "CORE MANIFEST PASS"
echo "ARTIFACT MANIFEST PASS"
echo "GATE 7' REPRODUCTION PASS"
