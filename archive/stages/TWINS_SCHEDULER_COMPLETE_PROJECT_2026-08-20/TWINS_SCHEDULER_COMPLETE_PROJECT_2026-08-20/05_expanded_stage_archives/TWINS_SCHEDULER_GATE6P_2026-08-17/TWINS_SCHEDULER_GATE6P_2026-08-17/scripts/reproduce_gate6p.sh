#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0
export PYTHONPATH="src:."

python scripts/run_gate6p.py
SCHEDCHECK_FAST_REPRO=1 pytest -ra
python scripts/selfcheck_gate6p.py

if [[ -f CORE_RESULTS.sha256 ]]; then
  sha256sum -c CORE_RESULTS.sha256
fi

echo "GATE 6' REPRODUCTION PASS"
