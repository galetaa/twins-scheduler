#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUTPUT_ROOT=${TWINS_OUTPUT_ROOT:-"$ROOT"}
mkdir -p "$OUTPUT_ROOT"
OUTPUT_ROOT=$(cd "$OUTPUT_ROOT" && pwd)
LOG_DIR=${TWINS_LOG_DIR:-"$OUTPUT_ROOT/build_logs"}
CACHE_ROOT=${TWINS_CACHE_ROOT:-"$ROOT/.cache"}
TEXMF_DIST="$CACHE_ROOT/texlive-overlay/usr/share/texlive/texmf-dist"
# Reproduction uses the pinned overlay. A local installed TeX distribution is
# sufficient for an explicitly logged layout check when no overlay is present.
if [[ ! -f "$TEXMF_DIST/tex/latex/microtype/microtype.sty" ]]; then
  kpsewhich microtype.sty >/dev/null || { echo 'PAPER FAIL microtype missing' >&2; exit 1; }
  TEXMF_DIST=$(kpsewhich -var-value=TEXMFDIST)
fi
WORK_PARENT="$OUTPUT_ROOT/.work"
FINAL_DIR="$OUTPUT_ROOT/manuscript/pdf"
mkdir -p "$LOG_DIR" "$WORK_PARENT" "$FINAL_DIR"
export SOURCE_DATE_EPOCH=1787390000 FORCE_SOURCE_DATE=1
[[ "$(sha256sum "$ROOT/vendor/lipics/lipics-v2021.cls" | cut -d' ' -f1)" == \
  'ecae53dfd29c7b22d02a9065327c104760fb726a028b146d556732021a5977f0' ]]
BIBTEX=$(command -v bibtex || command -v bibtex.original) || { echo 'PAPER FAIL BibTeX missing'; exit 1; }
for TARGET in main review; do
  BUILD_DIR=$(mktemp -d "$WORK_PARENT/lipics-$TARGET.XXXXXX")
  RAW_LOG="$BUILD_DIR/lipics_build.log"
  (
    cd "$ROOT/manuscript/lipics"
    export TEXINPUTS=.:"$ROOT/vendor/lipics"//::"$TEXMF_DIST"//
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$BUILD_DIR" "$TARGET.tex" || exit $?
    cd "$BUILD_DIR"
    export BIBINPUTS="$ROOT/manuscript/lipics":
    export BSTINPUTS="$TEXMF_DIST/bibtex/bst"//:
    "$BIBTEX" "$TARGET" || exit $?
    cd "$ROOT/manuscript/lipics"
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$BUILD_DIR" "$TARGET.tex" || exit $?
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$BUILD_DIR" "$TARGET.tex" || exit $?
  ) >"$RAW_LOG" 2>&1 || { tail -60 "$RAW_LOG"; exit 1; }
  grep -q 'Document Class: lipics-v2021 2023/05/12 v3.1.3' "$RAW_LOG"
  if grep -Eq 'Overfull|undefined references|Citation .* undefined|LaTeX Error|Fatal error' "$BUILD_DIR/$TARGET.log"; then
    grep -n -E 'Overfull|undefined|Error' "$BUILD_DIR/$TARGET.log"
    echo "PAPER FAIL $TARGET unresolved LaTeX diagnostic" >&2; exit 1
  fi
  ! grep -Eq '^Warning--|BibTeX.*Warning' "$BUILD_DIR/$TARGET.blg"
  PHYSICAL_PAGES=$(pdfinfo "$BUILD_DIR/$TARGET.pdf" | awk '/^Pages:/ {print $2}')
  MAIN_FIRST=$(sed -n 's/^TWINS-MAIN-FIRST:\([0-9][0-9]*\)$/\1/p' "$BUILD_DIR/$TARGET.log")
  MAIN_END=$(sed -n 's/^TWINS-MAIN-END-EXCLUSIVE:\([0-9][0-9]*\)$/\1/p' "$BUILD_DIR/$TARGET.log")
  MAIN_TEXT_PAGES=$((MAIN_END - MAIN_FIRST))
  [[ "$MAIN_TEXT_PAGES" -gt 0 && "$MAIN_TEXT_PAGES" -le 15 ]] || { echo "PAPER FAIL $TARGET page budget $MAIN_TEXT_PAGES"; exit 1; }
  pdffonts "$BUILD_DIR/$TARGET.pdf" | awk 'NR>2 && $6!="yes" {bad=1} END {exit bad}'
  pdftotext "$BUILD_DIR/$TARGET.pdf" "$BUILD_DIR/$TARGET.txt"
  python "$ROOT/scripts/check_pdf_text.py" "$BUILD_DIR/$TARGET.pdf" "$TARGET"
  if [[ "$TARGET" == main ]]; then
    PREFIX=lipics
    NAME=final_lipics_manuscript.pdf
  else
    PREFIX=review_lipics
    NAME=review_lipics_manuscript.pdf
  fi
  cp "$BUILD_DIR/$TARGET.pdf" "$FINAL_DIR/$NAME"
  cp "$RAW_LOG" "$LOG_DIR/${PREFIX}_build.log"
  cp "$BUILD_DIR/$TARGET.aux" "$LOG_DIR/${PREFIX}_references.aux"
  {
    echo 'status=PASS'
    echo "physical_pages=$PHYSICAL_PAGES"
    echo 'cover_pages=1'
    echo "main_text_pages=$MAIN_TEXT_PAGES"
    echo "main_starts_on_numbered_page=$MAIN_FIRST"
    echo "main_ends_before_numbered_page=$MAIN_END"
    echo 'opodis_2026_main_text_limit=15'
    echo 'class=lipics-v2021 v3.1.3'
    echo "variant=$TARGET"
    echo "texmf_dist=$TEXMF_DIST"
    pdflatex --version | head -1
    pandoc --version | head -1
  } >"$LOG_DIR/${PREFIX}_page_budget.log"
  {
    echo 'status=PASS'
    echo 'overfull_boxes=0'
    echo 'undefined_references=0'
    echo 'undefined_citations=0'
    echo 'bibtex_warnings=0'
    echo 'literal_reference_tildes=0'
  } >"$LOG_DIR/${PREFIX}_warnings.log"
  echo "PAPER PASS variant=$TARGET pages=$PHYSICAL_PAGES main_text_pages=$MAIN_TEXT_PAGES"
done
python "$ROOT/scripts/check_manuscript_consistency.py" >"$LOG_DIR/manuscript_consistency.log"
