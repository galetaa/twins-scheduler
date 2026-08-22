#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RELEASE_DIR="$ROOT/release"
RELEASE_DATE=${SOURCE_RELEASE_DATE:-$(date -I)}
TAG=${SOURCE_RELEASE_TAG:-v1.0.0-reproducible}
GIT_ZIP="$RELEASE_DIR/TWINS_SCHEDULER_GIT_PROJECT_${RELEASE_DATE}.zip"
SOURCE_TAR="$RELEASE_DIR/TWINS_SCHEDULER_SOURCE_RELEASE_${RELEASE_DATE}.tar.gz"
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

git -C "$ROOT" diff --quiet
git -C "$ROOT" diff --cached --quiet
git -C "$ROOT" rev-parse -q --verify "refs/tags/$TAG" >/dev/null
mkdir -p "$RELEASE_DIR"

git clone --quiet --no-hardlinks --branch "$TAG" "$ROOT" "$STAGE/twins-scheduler-closure"
git -C "$STAGE/twins-scheduler-closure" fsck --full
(cd "$STAGE" && zip -qr "$GIT_ZIP" twins-scheduler-closure)
git -C "$ROOT" archive --format=tar.gz --prefix=twins-scheduler-closure/ \
  -o "$SOURCE_TAR" "$TAG"

unzip -t "$GIT_ZIP" >"$RELEASE_DIR/zip_integrity.log"
unzip -l "$GIT_ZIP" | grep -q 'twins-scheduler-closure/.git/HEAD'
tar -tzf "$SOURCE_TAR" >"$RELEASE_DIR/source_integrity.log"
if tar -tzf "$SOURCE_TAR" | grep -q '/\.git/'; then
  echo "SOURCE RELEASE FAIL contains .git" >&2
  exit 1
fi
sha256sum "$GIT_ZIP" "$SOURCE_TAR" >"$RELEASE_DIR/SHA256SUMS"
echo "RELEASE PASS tag=$TAG date=$RELEASE_DATE"
