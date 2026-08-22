#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/results/reproduction}"
BASE="$ROOT/results/pilot"

rm -rf "$OUT"
mkdir -p "$OUT"

export PYTHONHASHSEED=0
export PYTHONPATH="$ROOT/src"

python -m schedcheck.cli --root "$ROOT" --output "$OUT"
python "$ROOT/scripts/selfcheck.py" --output "$OUT"

if command -v pytest >/dev/null 2>&1; then
  (cd "$ROOT" && pytest -q) | tee "$OUT/pytest.log"
else
  printf 'pytest unavailable; stdlib self-check completed\n' > "$OUT/pytest.log"
fi

CORE_FILES=(
  language_summary.csv
  protocol_observations.csv
  adjacent_separations.csv
  witnesses.jsonl
  suite_hierarchy.json
  closure_counterfactuals.json
  gate_decision.json
  DECISION.md
  run_log.txt
)

for file in "${CORE_FILES[@]}"; do
  cmp "$BASE/$file" "$OUT/$file"
done

{
  echo "REPRODUCTION PASS"
  echo "baseline=$BASE"
  echo "output=$OUT"
  echo "python=$(python --version 2>&1)"
  echo "core_files_byte_identical=${#CORE_FILES[@]}"
} | tee "$OUT/reproduction.log"
