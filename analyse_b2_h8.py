"""
Phase B-2 H8 Verdict Script
============================

Computes the optional H8 triple verdict from the per-sub-endpoint output of
phase_b2_stage3.py. Each sub-endpoint has its own gate threshold; no
aggregate verdict by design (§11.7 of (C)-OSF-Preregistration-Phase-A1).

Locked invariants:
    - E_curiosity threshold:     correlation > 0.3 (§11.4)
    - E_equilibration threshold: lead >= 50 cycles (§11.4)
    - E_autopoietic threshold:   detect >= 0.90 at FA <= 0.05 (§11.4)
    - Master seed 42

Author: Theodore Zuzarte (under direction with Claude, Anthropic)
Licence: MIT
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

import numpy as np


# =============================================================================
# Locked configuration
# =============================================================================

MASTER_SEED = 42

E_CURIOSITY_THRESHOLD      = 0.3
E_EQUILIBRATION_THRESHOLD  = 50    # cycles
E_AUTOPOIETIC_DETECT_THR   = 0.90
E_AUTOPOIETIC_FA_THR       = 0.05


# =============================================================================
# Sub-endpoint evaluators
# =============================================================================

def evaluate_e_curiosity(block: Dict) -> Dict:
    if not block or "correlation" not in block:
        return {
            "sub_endpoint": "E_curiosity", "skipped": True,
            "reason": "missing 'correlation' field", "passed": False,
        }
    value = float(block["correlation"])
    return {
        "sub_endpoint": "E_curiosity",
        "value":     value,
        "threshold": E_CURIOSITY_THRESHOLD,
        "test":      "Pearson(r_int(t), DeltaF_bar(t+1)) > 0.3",
        "passed":    bool(value > E_CURIOSITY_THRESHOLD),
    }


def evaluate_e_equilibration(block: Dict) -> Dict:
    if not block or "lead_cycles" not in block:
        return {
            "sub_endpoint": "E_equilibration", "skipped": True,
            "reason": "missing 'lead_cycles' field", "passed": False,
        }
    value = float(block["lead_cycles"])
    return {
        "sub_endpoint":  "E_equilibration",
        "value":         value,
        "threshold":     E_EQUILIBRATION_THRESHOLD,
        "trigger_cycle": block.get("trigger_cycle"),
        "ive_drop_cycle": block.get("ive_drop_cycle"),
        "test":          "trigger fires >= 50 cycles before IVE accuracy drop",
        "passed":        bool(value >= E_EQUILIBRATION_THRESHOLD),
    }


def evaluate_e_autopoietic(block: Dict) -> Dict:
    if not block or "detect_rate" not in block or "false_alarm_rate" not in block:
        return {
            "sub_endpoint": "E_autopoietic", "skipped": True,
            "reason": "missing 'detect_rate' or 'false_alarm_rate' field",
            "passed": False,
        }
    detect = float(block["detect_rate"])
    fa     = float(block["false_alarm_rate"])
    return {
        "sub_endpoint":     "E_autopoietic",
        "value":            detect,
        "threshold":        E_AUTOPOIETIC_DETECT_THR,
        "false_alarm_rate": fa,
        "fa_threshold":     E_AUTOPOIETIC_FA_THR,
        "n_breaches":       block.get("n_breaches"),
        "test":             "structural-breach detection >= 0.90 at FA <= 0.05",
        "passed":           bool(detect >= E_AUTOPOIETIC_DETECT_THR
                                 and fa <= E_AUTOPOIETIC_FA_THR),
    }


def compute_h8(data: Dict) -> Dict:
    ec = evaluate_e_curiosity(data.get("E_curiosity", {}))
    ee = evaluate_e_equilibration(data.get("E_equilibration", {}))
    ea = evaluate_e_autopoietic(data.get("E_autopoietic", {}))
    n_skipped = sum(1 for x in (ec, ee, ea) if x.get("skipped"))
    n_passing = sum(1 for x in (ec, ee, ea) if x.get("passed"))
    return {
        "hypothesis":      "H8 (§11.4) — Stage-3 §2.16 components work as designed (optional)",
        "test":            "Triple pass/fail per sub-endpoint, no aggregate (§11.7)",
        "E_curiosity":     ec,
        "E_equilibration": ee,
        "E_autopoietic":   ea,
        "n_passing":       int(n_passing),
        "n_skipped":       int(n_skipped),
    }


# =============================================================================
# Smoke test
# =============================================================================

def smoke_test() -> Dict:
    """Synthetic E_*; verify the verdict logic returns the expected pass triple."""
    synthetic = {
        "E_curiosity":     {"correlation": 0.42, "n_cycles": 5000},
        "E_equilibration": {"lead_cycles": 73, "trigger_cycle": 1450, "ive_drop_cycle": 1523},
        "E_autopoietic":   {"detect_rate": 0.93, "false_alarm_rate": 0.04, "n_breaches": 25},
    }
    h8 = compute_h8(synthetic)
    return {
        "mode":              "smoke_test",
        "h8":                h8,
        "smoke_test_passed": bool(h8["n_passing"] == 3 and h8["n_skipped"] == 0),
    }


# =============================================================================
# Provenance + CLI
# =============================================================================

def _git_commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "unknown"


def _script_sha256(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase B-2 H8 triple verdict (optional pre-registration)"
    )
    parser.add_argument("--input",      type=Path, default=None,
                        help="Input JSON from phase_b2_stage3.py")
    parser.add_argument("--output",     type=Path, required=True,
                        help="Output verdict JSON")
    parser.add_argument("--smoke-test", action="store_true",
                        help="Run synthetic smoke test")
    args = parser.parse_args(argv)

    np.random.seed(MASTER_SEED)

    if args.smoke_test:
        result = smoke_test()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2))
        print(f"OK: smoke test wrote {args.output}", file=sys.stderr)
        print(f"[B-2] smoke_test_passed={result['smoke_test_passed']}", file=sys.stderr)
        return 0 if result["smoke_test_passed"] else 1

    if args.input is None:
        print("ERROR: --input is required for non-smoke mode", file=sys.stderr)
        return 2

    data = json.loads(args.input.read_text())
    h8 = compute_h8(data)

    result = {
        "provenance": {
            "git_commit":     _git_commit_hash(),
            "script_sha256":  _script_sha256(__file__),
            "timestamp_utc":  datetime.datetime.now(datetime.UTC).isoformat(),
            "input_path":     str(args.input),
        },
        "h8": h8,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"OK: wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())