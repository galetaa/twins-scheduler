#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
MAN="$ROOT/manuscript"
BUILD="$MAN/build"
LAT="$MAN/latex"
mkdir -p "$BUILD" "$LAT"
for tool in pandoc xelatex pdfinfo pdftotext; do
  command -v "$tool" >/dev/null || { echo "$tool not found" >&2; exit 127; }
done
cp "$MAN/FULL_MANUSCRIPT_REVISED_2026-08-20.md" "$LAT/FULL_MANUSCRIPT_PDF.md"
python - "$LAT/FULL_MANUSCRIPT_PDF.md" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
for name in ('figure1_scheduler_grammar','figure2_quorum_pivot','figure3_premise_boundary'):
    s=s.replace(f'figures/{name}.svg', f'figures/{name}.pdf')
p.write_text(s,encoding='utf-8')
PY
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/figures"
cp -a "$MAN/figures/." "$TMP/figures/"
(
  cd "$MAN"
  pandoc latex/FULL_MANUSCRIPT_PDF.md \
    --from=markdown+yaml_metadata_block+tex_math_dollars+pipe_tables+link_attributes \
    --to=latex --standalone --citeproc --bibliography=references.bib \
    --resource-path=. --template=latex/template.tex --no-highlight \
    -o "$TMP/main.tex"
)
(
  cd "$TMP"
  xelatex -interaction=nonstopmode -halt-on-error main.tex > "$BUILD/xelatex_pass1.log" 2>&1
  xelatex -interaction=nonstopmode -halt-on-error main.tex > "$BUILD/xelatex_pass2.log" 2>&1
)
cp "$TMP/main.tex" "$LAT/main_review.tex"
cp "$TMP/main.pdf" "$MAN/TWINS_SCHEDULER_LIPICS_REVIEW_2026-08-20.pdf"
cp "$TMP/main.pdf" "$MAN/TWINS_SCHEDULER_FULL_MANUSCRIPT_2026-08-20.pdf"
pdfinfo "$TMP/main.pdf" > "$BUILD/pdfinfo.log"
pdftotext "$TMP/main.pdf" "$BUILD/manuscript_text.txt"
{
  echo BLOCKING_WARNINGS
  grep -E '! LaTeX Error|Overfull \\hbox|Undefined control sequence|Citation .* undefined|There were undefined references' "$BUILD/xelatex_pass2.log" || true
  echo UNDERFULL_COUNT
  grep -c 'Underfull \\hbox' "$BUILD/xelatex_pass2.log" || true
} > "$BUILD/latex_warning_summary.log"
PAGES=$(awk '/^Pages:/ {print $2}' "$BUILD/pdfinfo.log")
[ "$PAGES" = 17 ] || { echo "unexpected page count: $PAGES" >&2; exit 1; }
if sed -n '/BLOCKING_WARNINGS/,/UNDERFULL_COUNT/p' "$BUILD/latex_warning_summary.log" | sed '1d;$d' | grep -q .; then
  echo "blocking LaTeX warning" >&2; cat "$BUILD/latex_warning_summary.log" >&2; exit 1
fi
for phrase in 'Fully bounded operational schema' 'Projection congruence' 'hidden-state counterexample' 'project-local proof-certificate kernel'; do
  grep -Fiq "$phrase" "$BUILD/manuscript_text.txt" || { echo "missing PDF phrase: $phrase" >&2; exit 1; }
done
echo "review_pdf_build=PASS"
echo "physical_pages=$PAGES"
