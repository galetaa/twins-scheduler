#!/usr/bin/env bash
set -euo pipefail
set -o pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUTPUT_ROOT=${TWINS_OUTPUT_ROOT:-"$ROOT"}
mkdir -p "$OUTPUT_ROOT"
OUTPUT_ROOT=$(cd "$OUTPUT_ROOT" && pwd)
LOG_DIR=${TWINS_LOG_DIR:-"$OUTPUT_ROOT/build_logs"}
CACHE_ROOT=${TWINS_CACHE_ROOT:-"$ROOT/.cache"}
TEXMF_DIST="$CACHE_ROOT/texlive-overlay/usr/share/texlive/texmf-dist"
WORK_PARENT="$OUTPUT_ROOT/.work"
FINAL_DIR="$OUTPUT_ROOT/manuscript/pdf"
mkdir -p "$LOG_DIR" "$WORK_PARENT" "$FINAL_DIR"
BUILD_DIR=$(mktemp -d "$WORK_PARENT/lipics.XXXXXX")
RAW_LOG="$BUILD_DIR/lipics_build.log"
export SOURCE_DATE_EPOCH=1787390000
export FORCE_SOURCE_DATE=1

[[ -f "$TEXMF_DIST/tex/latex/microtype/microtype.sty" ]] || {
  echo "PAPER FAIL TeX overlay missing; run scripts/bootstrap.sh" >&2
  exit 1
}
[[ "$(sha256sum "$ROOT/vendor/lipics/lipics-v2021.cls" | cut -d' ' -f1)" == \
  "ecae53dfd29c7b22d02a9065327c104760fb726a028b146d556732021a5977f0" ]] || {
  echo "PAPER FAIL official class checksum mismatch" >&2
  exit 1
}

(
  set -e
  cd "$ROOT/manuscript/lipics"
  # Keep packages shipped with the host format before the supplementary overlay:
  # a 2024 array.sty cannot be loaded into a 2023 LaTeX format.
  export TEXINPUTS=.:"$ROOT/vendor/lipics"//::"$TEXMF_DIST"//
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory="$BUILD_DIR" main.tex
  cd "$BUILD_DIR"
  export BIBINPUTS="$ROOT/manuscript/lipics":
  export BSTINPUTS="$TEXMF_DIST/bibtex/bst"//:
  bibtex main
  cd "$ROOT/manuscript/lipics"
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory="$BUILD_DIR" main.tex
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory="$BUILD_DIR" main.tex
) >"$RAW_LOG" 2>&1

grep -q "Document Class: lipics-v2021 2023/05/12 v3.1.3" "$RAW_LOG"
if grep -Eq "Overfull|undefined references|Citation .* undefined|LaTeX Error|Fatal error" "$BUILD_DIR/main.log"; then
  echo "PAPER FAIL unresolved LaTeX diagnostic" >&2
  exit 1
fi
if grep -Eq "^Warning--|BibTeX.*Warning" "$BUILD_DIR/main.blg"; then
  echo "PAPER FAIL bibliography warning" >&2
  exit 1
fi

PHYSICAL_PAGES=$(pdfinfo "$BUILD_DIR/main.pdf" | awk '/^Pages:/ {print $2}')
BIBLIOGRAPHY_START=$(sed -n 's/.*@pageNumberStartBibliography{\([0-9][0-9]*\)}.*/\1/p' "$BUILD_DIR/main.aux")
[[ -n "$BIBLIOGRAPHY_START" ]]
MAIN_FIRST=$(sed -n 's/^TWINS-MAIN-FIRST:\([0-9][0-9]*\)$/\1/p' "$BUILD_DIR/main.log")
MAIN_END=$(sed -n 's/^TWINS-MAIN-END-EXCLUSIVE:\([0-9][0-9]*\)$/\1/p' "$BUILD_DIR/main.log")
[[ -n "$MAIN_FIRST" && -n "$MAIN_END" ]]
MAIN_TEXT_PAGES=$((MAIN_END - MAIN_FIRST))
[[ "$MAIN_TEXT_PAGES" -gt 0 ]]
[[ "$MAIN_TEXT_PAGES" -le 15 ]]
pdfinfo "$BUILD_DIR/main.pdf" | grep -Eq '^Author:[[:space:]]+Anonymous author\(s\)'
pdffonts "$BUILD_DIR/main.pdf" | awk 'NR > 2 && $6 != "yes" {bad=1} END {exit bad}'
pdftotext "$BUILD_DIR/main.pdf" "$BUILD_DIR/main.txt"
if grep -q '�' "$BUILD_DIR/main.txt"; then
  echo "PAPER FAIL replacement glyph found" >&2
  exit 1
fi

cp "$BUILD_DIR/main.pdf" "$FINAL_DIR/final_lipics_manuscript.pdf"
cp "$RAW_LOG" "$LOG_DIR/lipics_build.log"
{
  echo "status=PASS"
  echo "physical_pages=$PHYSICAL_PAGES"
  echo "cover_pages=1"
  echo "main_text_pages=$MAIN_TEXT_PAGES"
  echo "main_starts_on_numbered_page=$MAIN_FIRST"
  echo "main_ends_before_numbered_page=$MAIN_END"
  echo "bibliography_starts_on_numbered_page=$BIBLIOGRAPHY_START"
  echo "opodis_2026_main_text_limit=15"
  echo "class=lipics-v2021 v3.1.3"
  pdflatex --version | head -1
  pandoc --version | head -1
} >"$LOG_DIR/lipics_page_budget.log"
{
  echo "status=PASS"
  echo "overfull_boxes=0"
  echo "undefined_references=0"
  echo "undefined_citations=0"
  echo "bibtex_warnings=0"
  echo "class_fallback_warnings=1"
  echo "class_fallback_detail=fontawesome5 absent; official class uses documented text-symbol fallback"
} >"$LOG_DIR/lipics_warnings.log"

python "$ROOT/scripts/check_manuscript_consistency.py" >"$LOG_DIR/manuscript_consistency.log"
echo "PAPER PASS pages=$PHYSICAL_PAGES main_text_pages=$MAIN_TEXT_PAGES"
