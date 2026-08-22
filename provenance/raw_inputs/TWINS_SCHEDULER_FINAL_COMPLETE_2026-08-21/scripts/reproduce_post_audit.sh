#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUT="$ROOT/results/reproduction"
mkdir -p "$OUT"

python "$ROOT/proof_review/independent_proof_checks.py" | tee "$OUT/independent.log"
python "$ROOT/formal/project_kernel/proof_kernel.py" \
  "$ROOT/formal/project_kernel/certificate.json" \
  "$OUT/project_kernel_result.json" | tee "$OUT/project_kernel.log"
python "$ROOT/scripts/run_smt_checks.py" | tee "$OUT/smt.log"

set +e
grep -RInE '(^|[^[:alnum:]_])(sorry|admit|Admitted)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|Axiom)[[:space:]]|^[[:space:]]*unsafe[[:space:]]+def[[:space:]]' \
  "$ROOT/formal/lean" "$ROOT/formal/coq" > "$OUT/source_hygiene_hits.log"
HRC=$?
set -e
[ "$HRC" -eq 1 ] || { echo "formal source hygiene failed" >&2; cat "$OUT/source_hygiene_hits.log" >&2; exit 1; }
echo "formal_source_hygiene=PASS" | tee "$OUT/source_hygiene.log"

if command -v pandoc >/dev/null && command -v xelatex >/dev/null; then
  "$ROOT/scripts/build_review_pdf.sh" | tee "$OUT/review_pdf.log"
else
  echo "review_pdf_build=SKIPPED_MISSING_PANDOC_OR_XELATEX" | tee "$OUT/review_pdf.log"
fi

if kpsewhich lipics-v2021.cls >/dev/null 2>&1; then
  (cd "$ROOT/manuscript/lipics" && latexmk -pdf -interaction=nonstopmode -halt-on-error main_lipics.tex) \
    > "$OUT/official_lipics.log" 2>&1
  echo "official_lipics_build=PASS" | tee -a "$OUT/official_lipics.log"
else
  echo "official_lipics_build=NOT_RUN_CLASS_UNAVAILABLE" | tee "$OUT/official_lipics.log"
fi

LEAN_STATUS=NOT_RUN_TOOLCHAIN_UNAVAILABLE
COQ_STATUS=NOT_RUN_TOOLCHAIN_UNAVAILABLE
if command -v lake >/dev/null && command -v lean >/dev/null; then
  (cd "$ROOT/formal/lean" && lake build) > "$OUT/lean_build.log" 2>&1
  LEAN_STATUS=PASS
fi
if command -v coqc >/dev/null; then
  (cd "$ROOT/formal/coq" && coqc T1ReplayErasure.v && coqc T2ClosureLifting.v && coqc T3QuorumPivot.v && coqc T6PremiseBoundary.v && coqc AxiomAudit.v) > "$OUT/coq_build.log" 2>&1
  COQ_STATUS=PASS
fi
printf 'lean_kernel_build=%s\ncoq_kernel_build=%s\n' "$LEAN_STATUS" "$COQ_STATUS" | tee "$OUT/mature_provers.log"

echo "post_audit_reproduction=PASS_WITH_RECORDED_EXTERNAL_BLOCKERS"
