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
uv run python scripts/run_repair_frontier.py | tee "$TWINS_LOG_DIR/repair_frontier.log"
uv run python scripts/run_concrete_trace.py | tee "$TWINS_LOG_DIR/concrete_trace.log"
uv run python scripts/run_refinement_synthesis.py --study | tee "$TWINS_LOG_DIR/refinement_synthesis.log"
uv run python scripts/check_synthesis_order_oracle.py | tee "$TWINS_LOG_DIR/synthesis_order_oracle.log"
./scripts/run_native_conformance.sh
uv run --extra native-audit python experiments/native_cometbft/audit_evidence.py | tee "$TWINS_LOG_DIR/native_signature_audit.log"
python3 experiments/native_cometbft/check_repeatability.py | tee "$TWINS_LOG_DIR/native_repeatability.log"
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
  echo "repair_frontier_exhaustive_checks=PASS"
  echo "concrete_trace_legality_timing_fifo=PASS"
  echo "minimum_cost_synthesis_and_independent_certificates=PASS"
  echo "independent_arbitrary_order_oracle=PASS"
  echo "unchanged_native_conformance_and_signature_audit=PASS"
  echo "native_semantic_repeatability_and_race_detector=PASS"
  echo "official_lipics_build=PASS"
  echo "page_budget=PASS"
  echo "provenance_and_reference_manifests=PASS"
} | tee "$TWINS_LOG_DIR/reproduction_summary.log"
