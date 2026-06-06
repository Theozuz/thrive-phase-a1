#!/usr/bin/env bash
# Verify the 5-scenario discrimination matrix.
# Requires scripts/run_smoke_tests.sh to have produced the verdict JSONs.
set -euo pipefail
python scripts/verify_discrimination_matrix.py \
    results/smoke/ expected_discrimination_matrix.json
