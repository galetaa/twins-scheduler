#!/usr/bin/env bash
set -euo pipefail
set -o pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUTPUT_ROOT=${TWINS_OUTPUT_ROOT:-"$ROOT"}
LOG_DIR=${TWINS_LOG_DIR:-"$OUTPUT_ROOT/build_logs"}
GENERATED="$OUTPUT_ROOT/results/generated"
mkdir -p "$LOG_DIR" "$GENERATED"
cd "$ROOT"

uv run python -m pytest -q 2>&1 | tee "$LOG_DIR/python_tests.log"
go test ./... 2>&1 | tee "$LOG_DIR/go_tests.log"
uv run python -m twins_scheduler.bounded 2>&1 | tee "$LOG_DIR/python_bounded_refinement.log"
go run ./src/go/cometbft_refinement 2>&1 | tee "$LOG_DIR/go_bounded_refinement.log"
uv run python scripts/compare_bounded_results.py 2>&1 | tee "$LOG_DIR/cross_language_bounded.log"
uv run python scripts/independent_proof_checks.py 2>&1 \
  | tee "$GENERATED/independent_proof_checks.json" "$LOG_DIR/independent_proof_checks.log"
PYTHONHASHSEED=0 uv run python scripts/run_certificate_checks.py 2>&1 \
  | tee "$LOG_DIR/certificate_checks.log"
uv run python scripts/run_smt_checks.py 2>&1 | tee "$LOG_DIR/smt_checks.log"
uv run python scripts/check_formal_source_hygiene.py 2>&1 \
  | tee "$LOG_DIR/formal_source_hygiene_command.log"
uv run python scripts/assemble_formal_report.py 2>&1 | tee "$LOG_DIR/formal_verification.log"

echo "TEST_ALL PASS"
