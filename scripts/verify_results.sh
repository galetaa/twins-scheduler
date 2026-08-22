#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUTPUT_ROOT=${TWINS_OUTPUT_ROOT:-"$ROOT"}
(cd "$ROOT" && sha256sum -c results/manifests/REFERENCE_SHA256SUMS)
files=(
  results/generated/cometbft_refinement_results.json
  results/generated/cometbft_refinement_results_go.json
  results/generated/cometbft_refinement_summary.json
  results/generated/cometbft_cross_language_check.txt
  results/generated/independent_proof_checks.json
  results/generated/certificate_verification.json
  results/generated/smt_summary.json
  results/generated/formal_source_hygiene.json
  results/generated/formal_verification.json
  formal/smt/results.csv
  formal/smt/summary.json
  manuscript/pdf/final_lipics_manuscript.pdf
)
for relative in "${files[@]}"; do
  cmp "$ROOT/$relative" "$OUTPUT_ROOT/$relative"
done
echo "RESULTS MATCH reference_count=${#files[@]}"
