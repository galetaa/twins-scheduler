#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/results/final"
mkdir -p "$OUT"
LOG="$OUT/reproduction_final.log"
: > "$LOG"
exec > >(tee -a "$LOG") 2>&1
export PYTHONHASHSEED=0
export LC_ALL=C.UTF-8

status() { printf '%-44s %s\n' "$1" "$2"; }
run() { local label="$1"; shift; echo "--- $label ---"; "$@"; status "$label" PASS; }

run "independent theorem checks" python "$ROOT/proof_review/final_independent_checks.py"
python "$ROOT/proof_review/final_independent_checks.py" > "$OUT/final_independent_checks.json"
run "bounded CometBFT Python refinement" python "$ROOT/src/cometbft_bounded.py"
run "bounded CometBFT Go refinement" bash -lc "cd '$ROOT/go/cometbft_refinement' && go run ."
run "Python/Go terminal-row comparison" python "$ROOT/scripts/compare_cometbft_results.py"
run "bounded refinement pytest" pytest -q "$ROOT/tests/test_cometbft_bounded.py"
run "project-local proof certificate" python "$ROOT/formal/project_kernel/proof_kernel.py" "$ROOT/formal/project_kernel/certificate.json" --json-output "$OUT/project_kernel_result_final.json" --negative-controls
run "SMT obligations and controls" python "$ROOT/scripts/run_smt_checks.py"
run "formal source hygiene" python "$ROOT/scripts/check_formal_source_hygiene.py"

if command -v pandoc >/dev/null && command -v xelatex >/dev/null; then
  run "A4 review PDF build" "$ROOT/scripts/build_review_pdf.sh"
else
  status "A4 review PDF build" NOT_RUN_TOOLCHAIN_UNAVAILABLE
fi

LEAN_STATUS=NOT_RUN_TOOLCHAIN_UNAVAILABLE
COQ_STATUS=NOT_RUN_TOOLCHAIN_UNAVAILABLE
if command -v lake >/dev/null && command -v lean >/dev/null; then
  run "Lean pinned project build" bash -lc "cd '$ROOT/formal/lean' && lake build"
  run "Lean axiom audit" bash -lc "cd '$ROOT/formal/lean' && lake env lean AxiomAudit.lean"
  LEAN_STATUS=PASS
elif [[ "${STRICT_MATURE_PROVER:-0}" == "1" ]]; then
  echo "Lean toolchain unavailable in strict mode" >&2
  exit 3
else
  status "Lean pinned project build" "$LEAN_STATUS"
fi
if command -v coqc >/dev/null; then
  run "Coq source build" bash -lc "cd '$ROOT/formal/coq' && coqc T1ReplayErasure.v && coqc T2ClosureLifting.v && coqc T3QuorumPivot.v && coqc T6PremiseBoundary.v && coqc AxiomAudit.v"
  COQ_STATUS=PASS
else
  status "Coq source build" "$COQ_STATUS"
fi

LIPICS_STATUS=NOT_RUN_CLASS_UNAVAILABLE
if kpsewhich lipics-v2021.cls >/dev/null 2>&1 && command -v bibtex >/dev/null; then
  run "official LIPIcs class build" bash -lc "cd '$ROOT/manuscript/lipics' && latexmk -pdf -interaction=nonstopmode -halt-on-error main_lipics.tex"
  LIPICS_STATUS=PASS
else
  status "official LIPIcs class build" "$LIPICS_STATUS"
fi

cat > "$OUT/external_tool_status.json" <<JSON
{
  "lean_kernel_build": "$LEAN_STATUS",
  "coq_kernel_build": "$COQ_STATUS",
  "official_lipics_class_build": "$LIPICS_STATUS",
  "strict_mature_prover_requested": "${STRICT_MATURE_PROVER:-0}"
}
JSON

echo
status "T1 replay erasure with output congruence" PASS
status "T2 legal relational closure" PASS
status "structural quorum-pivot criterion" PASS
status "parametric P_f/B_f family" PASS
status "diagnostic seven-premise boundary" PASS
status "bounded CometBFT rule-level refinement" PASS
status "negative controls" PASS
status "final reproduction" PASS_WITH_EXPLICIT_EXTERNAL_BLOCKERS
