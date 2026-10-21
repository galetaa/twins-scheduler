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
  results/generated/lean_verification.json
  formal/smt/results.csv
  formal/smt/summary.json
  results/new/concrete_trace.json
  results/new/concrete_trace.csv
  results/revision/frontier_summary.json
  results/revision/frontier_graph_cases.csv
  results/revision/frontier_common_cases.csv
  results/revision/frontier_weighted_cases.csv
  results/native/native_summary.json
)
# All synthesis/transition outputs are deterministic, including gzip headers. Native raw
# signatures and receipts retain wall-clock timestamps; compare their semantic
# summary and validate their current signatures/provenance in reproduce.sh.
for relative in "${files[@]}"; do
  cmp "$ROOT/$relative" "$OUTPUT_ROOT/$relative"
done
SYNTHESIS_COUNT=$(python3 - "$ROOT" "$OUTPUT_ROOT" <<'PY'
from pathlib import Path
import sys

root, output = map(Path, sys.argv[1:])
files = sorted(path for directory in ("results/synthesis", "results/transition", "results/transition_bridge", "results/scaled")
               for path in (root / directory).rglob("*") if path.is_file())
for reference in files:
    relative = reference.relative_to(root)
    if reference.read_bytes() != (output / relative).read_bytes():
        raise SystemExit(f"SYNTHESIS RESULT MISMATCH: {relative}")
print(len(files))
PY
)
# PDF bytes vary with the TeX engine and font packages. The reference manifest
# authenticates the committed PDF; a fresh build has separate layout/content gates.
grep -qx 'status=PASS' "$OUTPUT_ROOT/build_logs/lipics_page_budget.log"
grep -qx 'status=PASS' "$OUTPUT_ROOT/build_logs/lipics_warnings.log"
grep -qx 'status=PASS' "$OUTPUT_ROOT/build_logs/review_lipics_page_budget.log"
grep -qx 'status=PASS' "$OUTPUT_ROOT/build_logs/review_lipics_warnings.log"
python "$ROOT/scripts/check_manuscript_consistency.py"
echo "RESULTS MATCH reference_count=$((${#files[@]} + SYNTHESIS_COUNT))"
