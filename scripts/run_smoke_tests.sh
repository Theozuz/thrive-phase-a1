#!/usr/bin/env bash
# Run all 11 locked-artefact smoke tests + 5 synthetic A-1 scenarios.
# Pre-requisite: conda env `thrive_phase_a1` activated.
#
# Usage:
#     bash scripts/run_smoke_tests.sh
#
# Exits non-zero if any smoke test fails. Outputs land in results/smoke/.

set -euo pipefail
mkdir -p results/smoke

echo "=== 1/11  a0_preflight smoke test ==="
python a0_preflight.py --smoke-test --output results/smoke/a0_smoke.json

echo "=== 2/11  rfm_features smoke test ==="
python rfm_features.py --smoke-test

echo "=== 3/11  rjepa_features smoke test ==="
python rjepa_features.py --smoke-test

echo "=== 4/11  rjepa_brain_features smoke test ==="
python rjepa_brain_features.py --smoke-test

echo "=== 5/11  rgl_features smoke test ==="
python rgl_features.py --smoke-test

echo "=== 6/11  synth_a1 -- eight scenarios ==="
for scenario in all_pass h1_fail h2_fail h3_fail h4_fail h5_fail h9_fail h10_fail; do
    echo "    scenario=$scenario"
    python synth_a1.py --scenario "$scenario" \
        --output "results/smoke/a1_${scenario}"
done

echo "=== 7/11  analyse_a1_factorial on each synthetic scenario ==="
for scenario in all_pass h1_fail h2_fail h3_fail h4_fail h5_fail h9_fail h10_fail; do
    echo "    scenario=$scenario"
    python analyse_a1_factorial.py \
        --input-dir "results/smoke/a1_${scenario}" \
        --output-json "results/smoke/a1_${scenario}_verdict.json" \
        --output-md   "results/smoke/a1_${scenario}_report.md"
done

echo "=== 8/11  phase_b1_simulator smoke test ==="
python phase_b1_simulator.py --smoke-test --n-seeds 3 \
    --output results/smoke/phase_b1_smoke.json

echo "=== 9/11  phase_a7_acp_twin smoke test ==="
python phase_a7_acp_twin.py --smoke-test \
    --output results/smoke/phase_a7_smoke.json

echo "=== 10/11 phase_a7_ensemble smoke test ==="
python phase_a7_ensemble.py --smoke-test \
    --output results/smoke/phase_a7_ensemble_smoke.json

echo "=== 11/13 phase_b2_stage3 smoke test ==="
python phase_b2_stage3.py --smoke-test \
    --output results/smoke/phase_b2_smoke.json

echo "=== 12/13 analyse_a7_factorial (H6/H7) smoke test ==="
python analyse_a7_factorial.py --smoke-test \
    --output results/smoke/a7_h6_h7_smoke.json

echo "=== 13/13 analyse_b2_h8 (optional H8) smoke test ==="
python analyse_b2_h8.py --smoke-test \
    --output results/smoke/b2_h8_smoke.json

echo
echo "================================================"
echo "All 13 smoke tests + 8 synthetic scenarios passed"
echo "Verdict JSONs:    results/smoke/a1_*_verdict.json"
echo "                  results/smoke/a7_h6_h7_smoke.json"
echo "                  results/smoke/b2_h8_smoke.json"
echo "Next step:        bash scripts/verify_discrimination.sh"
echo "================================================"
