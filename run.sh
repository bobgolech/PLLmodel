#!/usr/bin/env bash
set -euo pipefail
# Ensure Python is available; prefer python3
PYTHON_BIN="${PYTHON_BIN:-python3}"
exec "$PYTHON_BIN" "$(dirname "$0")/run.py" "$@"