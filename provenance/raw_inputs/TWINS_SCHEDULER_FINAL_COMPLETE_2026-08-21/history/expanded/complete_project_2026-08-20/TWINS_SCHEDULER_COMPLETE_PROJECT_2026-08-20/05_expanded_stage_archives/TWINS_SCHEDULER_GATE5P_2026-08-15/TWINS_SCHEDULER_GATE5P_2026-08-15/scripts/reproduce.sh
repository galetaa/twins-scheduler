#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0
export PYTHONPATH="src:."

python scripts/run_gate5p.py
SCHEDCHECK_FAST_REPRO=1 pytest -q
python scripts/selfcheck_gate5p.py

if [[ -f CORE_RESULTS.sha256 ]]; then
  sha256sum -c CORE_RESULTS.sha256
fi

echo "GATE 5' REPRODUCTION PASS"
