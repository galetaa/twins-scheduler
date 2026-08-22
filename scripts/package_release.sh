#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RELEASE_DIR="$ROOT/release"
RELEASE_DATE=${SOURCE_RELEASE_DATE:-$(date -I)}
TAG=${SOURCE_RELEASE_TAG:-v1.0.0-reproducible}
GIT_ZIP="$RELEASE_DIR/TWINS_SCHEDULER_GIT_PROJECT_${RELEASE_DATE}.zip"
SOURCE_TAR="$RELEASE_DIR/TWINS_SCHEDULER_SOURCE_RELEASE_${RELEASE_DATE}.tar.gz"
STAGE=$(mktemp -d)
STAGED_ZIP="$STAGE/git-project.zip"
STAGED_TAR="$STAGE/source-release.tar.gz"
trap 'rm -rf "$STAGE"' EXIT

git -C "$ROOT" diff --quiet
git -C "$ROOT" diff --cached --quiet
git -C "$ROOT" rev-parse -q --verify "refs/tags/$TAG" >/dev/null
mkdir -p "$RELEASE_DIR"

git clone --quiet --no-hardlinks --branch "$TAG" "$ROOT" "$STAGE/twins-scheduler-closure"
git -C "$STAGE/twins-scheduler-closure" fsck --full
(cd "$STAGE" && zip -qr "$STAGED_ZIP" twins-scheduler-closure)
git -C "$ROOT" archive --format=tar.gz --prefix=twins-scheduler-closure/ \
  -o "$STAGED_TAR" "$TAG"

unzip -t "$STAGED_ZIP" >/dev/null
unzip -Z1 "$STAGED_ZIP" >"$STAGE/zip_entries.txt"
grep -Fxq 'twins-scheduler-closure/.git/HEAD' "$STAGE/zip_entries.txt"
tar -tzf "$STAGED_TAR" >"$STAGE/source_entries.txt"
if grep -q '/\.git/' "$STAGE/source_entries.txt"; then
  echo "SOURCE RELEASE FAIL contains .git" >&2
  exit 1
fi
mv -f "$STAGED_ZIP" "$GIT_ZIP"
mv -f "$STAGED_TAR" "$SOURCE_TAR"
(
  cd "$RELEASE_DIR"
  unzip -t "$(basename "$GIT_ZIP")" >zip_integrity.log
  tar -tzf "$(basename "$SOURCE_TAR")" >source_integrity.log
  sha256sum "$(basename "$GIT_ZIP")" "$(basename "$SOURCE_TAR")" >SHA256SUMS
)
echo "RELEASE PASS tag=$TAG date=$RELEASE_DATE"
