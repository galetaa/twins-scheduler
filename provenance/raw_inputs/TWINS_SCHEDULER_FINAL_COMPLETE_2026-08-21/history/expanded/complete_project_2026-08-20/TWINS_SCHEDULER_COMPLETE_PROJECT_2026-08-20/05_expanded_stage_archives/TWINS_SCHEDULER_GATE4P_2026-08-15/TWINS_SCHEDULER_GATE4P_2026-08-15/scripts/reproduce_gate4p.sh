#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0
export PYTHONPATH="src:."

rm -rf results/gate4p
mkdir -p results/gate4p

python scripts/run_conformance.py --output results/gate4p --seed 20260815 --random-cases 128
python scripts/run_gate4p.py
SCHEDCHECK_FAST_REPRO=1 pytest -q
python scripts/selfcheck_gate4p.py

printf '%s\n' "REPRODUCTION PASS"
