#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv run python -m unittest discover -s tests -v 2>&1 | tee results/pilot/test_run.log
PYTHONHASHSEED=0 uv run python scripts/run_pilot.py --config configs/pilot.toml
sha256sum -c results/pilot/manifest.sha256
