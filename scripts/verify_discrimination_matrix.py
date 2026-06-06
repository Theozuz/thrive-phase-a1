#!/usr/bin/env python3
"""CI discrimination-matrix gate — verify 8 synthetic-scenario verdicts.

Runs `analyse_a1_factorial.py` on each of the 8 pre-generated synthetic
scenarios (all_pass, h1_fail, h2_fail, h3_fail, h4_fail, h5_fail, h9_fail,
h10_fail) and compares the H1, H2, H3, H4, H5, H9, H10 verdicts to the
truth table in expected_discrimination_matrix.json.

Returns exit code 0 if all 8 scenarios produce the expected verdicts,
non-zero otherwise.

Usage:
    python scripts/verify_discrimination_matrix.py \
        results/smoke/ expected_discrimination_matrix.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def verdict_label(passed: bool) -> str:
    return "PASS" if passed else "FAIL"


def main(smoke_dir: str, expected_path: str) -> int:
    expected = json.loads(Path(expected_path).read_text())
    smoke_root = Path(smoke_dir)

    failures: list[str] = []
    scenarios_checked = 0
    for scenario_name, expected_verdicts in expected.items():
        if scenario_name.startswith("_"):
            continue  # metadata key
        verdict_file = smoke_root / f"a1_{scenario_name}_verdict.json"
        if not verdict_file.exists():
            failures.append(f"MISSING  {verdict_file}")
            continue
        actual = json.loads(verdict_file.read_text())
        scenarios_checked += 1
        scenario_failures = []
        for h, expected_outcome in expected_verdicts.items():
            if h.startswith("_"):
                continue  # metadata / annotation key, not a hypothesis
            # analyse_a1_factorial.py keys hypotheses as "h1" .. "h10"
            actual_block = actual.get(h.lower())
            if actual_block is None:
                scenario_failures.append(f"MISSING_KEY {h}")
                continue
            actual_outcome = verdict_label(bool(actual_block.get("passed", False)))
            if actual_outcome != expected_outcome:
                scenario_failures.append(
                    f"{h}: expected={expected_outcome}, actual={actual_outcome}"
                )
        if scenario_failures:
            failures.append(
                f"FAIL  scenario={scenario_name}\n      " +
                "\n      ".join(scenario_failures)
            )
        else:
            print(f"OK    scenario={scenario_name} (7/7 hypotheses match)")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"\nDiscrimination matrix: {scenarios_checked}/{scenarios_checked} scenarios verified.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
