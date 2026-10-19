#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT/provenance"
sha256sum -c RAW_INPUTS_SHA256SUMS
cd "$ROOT"
(cd models/tendermint_style/upstream_v0393 && sha256sum -c MANIFEST.sha256)
while IFS= read -r archive_path; do
  unzip -t "$archive_path" >/dev/null
done < <(find provenance/source_archives -maxdepth 1 -type f -name '*.zip' | sort)
python - <<'PY'
import csv
import subprocess
from pathlib import Path
root = Path.cwd()
with (root / "provenance/RAW_INPUTS_MANIFEST.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 1567, len(rows)
with (root / "provenance/CANONICAL_FILE_MAP.csv").open(newline="", encoding="utf-8") as handle:
    canonical = list(csv.DictReader(handle))
assert canonical
tracked = set(subprocess.check_output(["git", "ls-files", "-z"], text=True).split("\0"))
for row in canonical:
    assert (root / row["new_path"]).is_file(), row["new_path"]
    assert row["new_path"] in tracked, f"canonical path is not tracked: {row['new_path']}"
print(f"manifest_rows={len(rows)} canonical_rows={len(canonical)}")
PY
echo "PROVENANCE PASS"
