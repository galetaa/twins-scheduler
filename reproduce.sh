#!/usr/bin/env bash
set -euo pipefail
set -o pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
mkdir -p "$ROOT/.cache"
if [[ -n "${TWINS_REPRODUCTION_RUN_ROOT:-}" ]]; then
  mkdir -p "$TWINS_REPRODUCTION_RUN_ROOT"
  RUN_ROOT=$(cd "$TWINS_REPRODUCTION_RUN_ROOT" && pwd)
else
  RUN_ROOT=$(mktemp -d "$ROOT/.cache/reproduction.XXXXXX")
fi
export TWINS_OUTPUT_ROOT="$RUN_ROOT"
export TWINS_LOG_DIR="$RUN_ROOT/build_logs"
mkdir -p "$TWINS_LOG_DIR"
START_SECONDS=$SECONDS

cd "$ROOT"
./scripts/bootstrap.sh 2>&1 | tee "$TWINS_LOG_DIR/bootstrap.log"
./scripts/test_all.sh
./scripts/build_formal.sh
./scripts/build_paper.sh 2>&1 | tee "$TWINS_LOG_DIR/paper_command.log"
./scripts/verify_provenance.sh >"$TWINS_LOG_DIR/provenance.log" 2>&1
./scripts/verify_results.sh >"$TWINS_LOG_DIR/result_comparison.log" 2>&1

ELAPSED_SECONDS=$((SECONDS - START_SECONDS))
{
  echo "TWINS SCHEDULER REPRODUCTION: PASS"
  echo "runtime_seconds=$ELAPSED_SECONDS"
  echo "output_root=$RUN_ROOT"
  echo "python_tests=PASS"
  echo "go_tests=PASS"
  echo "cross_language=PASS"
  echo "independent_proof_checks=PASS"
  echo "project_local_kernel=PASS"
  echo "negative_controls=PASS"
  echo "smt_positive_negative=PASS"
  echo "lean_build_axioms_leanchecker=PASS"
  echo "official_lipics_build=PASS"
  echo "page_budget=PASS"
  echo "provenance_and_reference_manifests=PASS"
} | tee "$TWINS_LOG_DIR/reproduction_summary.log"
