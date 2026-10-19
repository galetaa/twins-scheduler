#!/usr/bin/env bash
# The main reproduction entry point includes the repair-frontier revision.
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
exec "$ROOT/reproduce.sh" "$@"
