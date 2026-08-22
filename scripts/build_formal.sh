#!/usr/bin/env bash
set -euo pipefail
set -o pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUTPUT_ROOT=${TWINS_OUTPUT_ROOT:-"$ROOT"}
LOG_DIR=${TWINS_LOG_DIR:-"$OUTPUT_ROOT/build_logs"}
ELAN_HOME=${ELAN_HOME:-"$ROOT/.cache/elan"}
export ELAN_HOME
export PATH="$ELAN_HOME/bin:$PATH"
mkdir -p "$LOG_DIR"
cd "$ROOT"

lake build 2>&1 | tee "$LOG_DIR/lean_build.log"
lake env lean formal/lean/AxiomAudit.lean 2>&1 | tee "$LOG_DIR/lean_axiom_audit.log"
lake env leanchecker SchedulerClosure 2>&1 | tee "$LOG_DIR/leanchecker.log"
uv run python scripts/check_formal_source_hygiene.py 2>&1 | tee "$LOG_DIR/formal_source_hygiene_command.log"

echo "BUILD_FORMAL PASS"
