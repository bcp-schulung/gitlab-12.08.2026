#!/usr/bin/env bash
# Run the end-to-end test suite against a live Uvicorn server.
# Usage: ./scripts/run_e2e.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"

echo "Running end-to-end tests..."
pytest tests/e2e -v

echo "End-to-end tests passed."
