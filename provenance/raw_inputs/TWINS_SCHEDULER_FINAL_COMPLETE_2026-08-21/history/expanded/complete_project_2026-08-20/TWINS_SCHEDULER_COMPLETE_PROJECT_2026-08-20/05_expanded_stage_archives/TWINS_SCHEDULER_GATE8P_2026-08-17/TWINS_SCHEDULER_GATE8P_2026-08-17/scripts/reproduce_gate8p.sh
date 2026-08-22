#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0
export SOURCE_DATE_EPOCH=1786924800
export TZ=UTC

G8_BASELINE=""
if [[ -f GATE8P_MANIFEST.sha256 ]]; then
  G8_BASELINE="$(mktemp)"
  cp GATE8P_MANIFEST.sha256 "$G8_BASELINE"
fi
TMP_BUILD="$(mktemp -d)"
TMP_LEGACY=""
cleanup() {
  rm -rf "$TMP_BUILD"
  [[ -z "$TMP_LEGACY" ]] || rm -rf "$TMP_LEGACY"
  [[ -z "$G8_BASELINE" ]] || rm -f "$G8_BASELINE"
  find "$ROOT" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
  find "$ROOT" -type d -name .pytest_cache -prune -exec rm -rf {} + 2>/dev/null || true
}
trap cleanup EXIT

printf '\n== Gate 7 core evidence ==\n'
./scripts/reproduce_gate7p.sh

if [[ "${GATE8_SKIP_LEGACY:-0}" != "1" ]]; then
  printf '\n== Gate 5 legacy exact kernels ==\n'
  (
    cd legacy_evidence
    sha256sum -c TWINS_SCHEDULER_GATE5P_2026-08-15.zip.sha256
  )
  TMP_LEGACY="$(mktemp -d)"
  unzip -q legacy_evidence/TWINS_SCHEDULER_GATE5P_2026-08-15.zip -d "$TMP_LEGACY"
  "$TMP_LEGACY/TWINS_SCHEDULER_GATE5P_2026-08-15/scripts/reproduce.sh"
else
  echo 'Legacy exact-kernel route skipped by GATE8_SKIP_LEGACY=1.'
fi

printf '\n== Claim and decision validation ==\n'
python3 scripts/validate_gate8p.py

printf '\n== Deterministic manuscript build ==\n'
python3 - <<'PY'
from pathlib import Path
root=Path.cwd()
src=(root/'manuscript/FULL_MANUSCRIPT.md').read_text(encoding='utf-8')
for name in ('figure1_scheduler_grammar','figure2_quorum_pivot','figure3_premise_boundary'):
    src=src.replace(f'figures/{name}.svg',f'figures/{name}.pdf')
(root/'manuscript/latex/FULL_MANUSCRIPT_PDF.md').write_text(src, encoding='utf-8')
PY
(
  cd manuscript
  pandoc latex/FULL_MANUSCRIPT_PDF.md \
    --from=markdown+yaml_metadata_block+tex_math_dollars+pipe_tables+link_attributes \
    --to=latex --standalone --citeproc --bibliography=references.bib \
    --resource-path=. --template=latex/template.tex --no-highlight \
    -o "$TMP_BUILD/main.tex"
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$TMP_BUILD" "$TMP_BUILD/main.tex" > "$TMP_BUILD/build1.log" 2>&1
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$TMP_BUILD" "$TMP_BUILD/main.tex" > "$TMP_BUILD/build2.log" 2>&1
)
if grep -Eq '! LaTeX Error|Overfull \\hbox' "$TMP_BUILD/build2.log"; then
  cat "$TMP_BUILD/build2.log"
  echo 'Manuscript build has a blocking LaTeX error or overfull box.' >&2
  exit 1
fi
cp "$TMP_BUILD/main.tex" manuscript/latex/main.tex
cp "$TMP_BUILD/main.pdf" manuscript/TWINS_SCHEDULER_FULL_MANUSCRIPT_2026-08-17.pdf
pdftotext manuscript/TWINS_SCHEDULER_FULL_MANUSCRIPT_2026-08-17.pdf "$TMP_BUILD/manuscript.txt"
for phrase in \
  'Relational closure lifting' \
  'Parametric quorum-pivot separation' \
  'Exact seven-premise boundary' \
  'Replay erasure' \
  'does not claim' \
  'AI-use disclosure draft'; do
  grep -Fq "$phrase" "$TMP_BUILD/manuscript.txt"
done
pages="$(pdfinfo manuscript/TWINS_SCHEDULER_FULL_MANUSCRIPT_2026-08-17.pdf | awk '/^Pages:/ {print $2}')"
size="$(pdfinfo manuscript/TWINS_SCHEDULER_FULL_MANUSCRIPT_2026-08-17.pdf | awk -F: '/^Page size:/ {sub(/^ +/,"",$2); print $2}')"
[[ "$pages" == "17" ]]
[[ "$size" == 595.28* ]] || [[ "$size" == 595.276* ]]
python3 scripts/validate_gate8p.py

echo "MANUSCRIPT BUILD PASS pages=$pages"

if [[ -n "$G8_BASELINE" ]]; then
  sha256sum -c "$G8_BASELINE" >/dev/null
  echo 'GATE 8 MANIFEST PASS'
fi

echo "GATE 8' REPRODUCTION PASS"
