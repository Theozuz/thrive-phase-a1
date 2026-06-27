"""
Phase A-7 Factorial Analysis Script
====================================

Computes H6 (Amendment 3a) and H7 (Amendment 3b) verdicts from the per-
condition endpoint JSONs produced by the Phase A-7 ACP twin and Mainstream-
Ensemble simulators.

Statistical test: paired BEST via pingouin.ttest(paired=True) per endpoint.
H6: thrIVE-twin vs LeWM-baseline (paired per (subject, stressor, mode))
H7: thrIVE-twin vs Mainstream-Ensemble (E6, E7' N/A by design for ensemble)
Holm-Bonferroni applied across the per-endpoint p-values per hypothesis.

Endpoint sign convention (direction of "better"):
    e1_latency_ms       smaller is better
    e2_recovery_cycles  smaller is better
    e3_fpr_drift        closer-to-zero is better (compare |drift|)
    e4_cross_modal_mean larger is better
    e6_halt_latency_ms  smaller is better (twin only; N/A for ensemble)
    e7_fusion_ratio     larger is better (twin only; N/A for ensemble)

Locked invariants:
    - α = 0.05 (one-sided) per §11.7 of (C)-OSF-Preregistration-Phase-A1
    - BF10 threshold = 3.0 for primary-endpoint reporting
    - Master seed 42
    - Holm-Bonferroni correction across per-hypothesis endpoint p-values
    - Joint H6/H7 verdict per §11.6 of the OSF prereg

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
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import pingouin as pg


# =============================================================================
# Locked configuration
# =============================================================================

MASTER_SEED = 42
ALPHA       = 0.05    # one-sided
BF10_THRESHOLD = 3.0

# Endpoints tested per hypothesis. Direction sign: +1 means larger is better,
# -1 means smaller is better.
H6_ENDPOINTS = {
    "e1_latency_ms":       -1,
    "e2_recovery_cycles":  -1,
    "e3_fpr_drift":        -1,    # tested on absolute value (|drift|)
    "e4_cross_modal_mean": +1,
    "e6_halt_latency_ms":  -1,
    "e7_fusion_ratio":     +1,
}
H7_ENDPOINTS = {
    "e1_latency_ms":       -1,
    "e2_recovery_cycles":  -1,
    "e3_fpr_drift":        -1,
    "e4_cross_modal_mean": +1,
    # e6 and e7' are N/A by design — no hyperdirect-pathway equivalent,
    # no sheaf-fusion ratio in the mainstream ensemble.
}


# =============================================================================
# Statistical helpers (mirroring (C)-A1-Factorial-Analysis-Script.md)
# =============================================================================

def paired_cohens_d(x: np.ndarray, y: np.ndarray) -> float:
    diff = x - y
    return float(diff.mean() / (diff.std(ddof=1) + 1e-12))


def paired_bf10(x: np.ndarray, y: np.ndarray, direction_sign: int) -> float:
    """Paired-samples Bayes Factor (one-sided per direction_sign).

    Uses the Morey & Wagenmakers (2014) two-sided-to-one-sided adjustment
    (same pattern as (C)-A1-Factorial-Analysis-Script.md::paired_bf10).
    direction_sign = +1 means H_A: mean(x) > mean(y); -1 means mean(x) < mean(y).
    """
    bf10_two = float(pg.ttest(x, y, paired=True).BF10.iloc[0])
    diff = np.asarray(x) - np.asarray(y)
    p_dir = float((diff * direction_sign > 0).mean())
    return 2.0 * bf10_two * p_dir


def paired_one_sided_p(x: np.ndarray, y: np.ndarray, direction_sign: int) -> float:
    """One-sided paired p-value in the specified direction.

    pingouin 0.5.x uses 'p-val' (hyphen); 0.6+ uses 'p_val' (underscore).
    Handle both for cross-version compatibility.
    """
    alternative = "greater" if direction_sign >= 0 else "less"
    result = pg.ttest(x, y, paired=True, alternative=alternative)
    col = "p_val" if "p_val" in result.columns else "p-val"
    return float(result[col].iloc[0])


def holm_bonferroni(p_values: List[float]) -> Tuple[List[float], List[bool]]:
    """Holm-Bonferroni adjustment across a list of p-values."""
    arr = np.asarray(p_values)
    rejected, p_adj = pg.multicomp(arr, method="holm")
    return list(p_adj), [bool(r) for r in rejected]


# =============================================================================
# Endpoint loading
# =============================================================================

def load_endpoint_dir(dir_path: Path) -> pd.DataFrame:
    """Load all *.json endpoint files in a directory into a long DataFrame.

    Each file is expected to contain the dict produced by aggregate_endpoints()
    in the upstream simulator, plus optional "subject" / "subject_id" keys.
    """
    rows = []
    for p in sorted(dir_path.glob("*.json")):
        data = json.loads(p.read_text())
        subject = data.get("subject", data.get("subject_id", p.stem))
        rows.append({
            "subject":            str(subject),
            "stressor":           data.get("stressor", "unknown"),
            "mode":               data.get("mode", "unknown"),
            "e1_latency_ms":      float(data.get("e1_latency_ms", float("nan"))),
            "e2_recovery_cycles": float(data.get("e2_recovery_cycles", float("nan"))),
            "e3_fpr_drift":       float(data.get("e3_fpr_drift", float("nan"))),
            "e4_cross_modal_mean": float(data.get("e4_cross_modal_mean", float("nan"))),
            "e6_halt_latency_ms": float(data.get("e6_halt_latency_ms", float("nan"))),
            "e7_fusion_ratio":    float(data.get("e7_fusion_ratio", float("nan"))),
        })
    return pd.DataFrame(rows)


def aggregate_per_subject(df: pd.DataFrame) -> pd.DataFrame:
    """Mean endpoint value per (subject, condition)."""
    return df.groupby(["subject", "stressor", "mode"], as_index=False).mean(numeric_only=True)


# =============================================================================
# H6 / H7 verdict computation
# =============================================================================

def transform_for_test(endpoint: str, values: np.ndarray) -> np.ndarray:
    """Apply endpoint-specific transformations before paired test.

    e3_fpr_drift is tested on absolute value (closer to zero is better).
    Replace +inf E1 latency with the maximum finite value + 1 (penalty for
    no-decision conditions).
    """
    if endpoint == "e3_fpr_drift":
        return np.abs(values)
    if endpoint == "e1_latency_ms":
        finite = values[np.isfinite(values)]
        if len(finite) == 0:
            return values
        cap = float(finite.max()) + 1.0
        return np.where(np.isfinite(values), values, cap)
    return values


def compare_endpoint(twin_vals: np.ndarray, baseline_vals: np.ndarray,
                     endpoint: str, direction_sign: int) -> Dict:
    """Paired test on one endpoint."""
    t = transform_for_test(endpoint, twin_vals)
    b = transform_for_test(endpoint, baseline_vals)
    mask = np.isfinite(t) & np.isfinite(b)
    t, b = t[mask], b[mask]
    if len(t) < 5:
        return {
            "endpoint": endpoint,
            "n_paired": int(len(t)),
            "skipped":  True,
            "reason":   "fewer than 5 paired observations after NaN filter",
            "passed_endpoint": False,
        }
    d   = paired_cohens_d(t, b)
    p   = paired_one_sided_p(t, b, direction_sign)
    bf  = paired_bf10(t, b, direction_sign)
    return {
        "endpoint":         endpoint,
        "n_paired":         int(len(t)),
        "mean_twin":        float(t.mean()),
        "mean_baseline":    float(b.mean()),
        "diff":             float((t - b).mean()),
        "cohen_d":          d,
        "p_one_sided":      p,
        "BF10":             bf,
        "direction_sign":   direction_sign,
        "passed_endpoint":  bool((p < ALPHA) and (bf > BF10_THRESHOLD)),
    }


def test_h6(twin_df: pd.DataFrame, lewm_df: pd.DataFrame) -> Dict:
    """H6 — paired BEST per endpoint across all (subject, stressor, mode)."""
    merged = pd.merge(
        twin_df, lewm_df,
        on=["subject", "stressor", "mode"],
        suffixes=("_twin", "_lewm"),
        how="inner",
    )
    per_endpoint: Dict[str, Dict] = {}
    p_values: List[float] = []
    for endpoint, sign in H6_ENDPOINTS.items():
        col_twin = f"{endpoint}_twin"
        col_lewm = f"{endpoint}_lewm"
        if col_twin not in merged.columns or col_lewm not in merged.columns:
            per_endpoint[endpoint] = {
                "endpoint": endpoint, "skipped": True,
                "reason": "endpoint missing from input data", "passed_endpoint": False,
            }
            continue
        result = compare_endpoint(
            merged[col_twin].values, merged[col_lewm].values, endpoint, sign,
        )
        per_endpoint[endpoint] = result
        if not result.get("skipped"):
            p_values.append(result["p_one_sided"])

    p_adj, rejected = holm_bonferroni(p_values) if p_values else ([], [])
    # Map adjusted p-values back to endpoint entries (in order)
    j = 0
    for endpoint in H6_ENDPOINTS:
        e = per_endpoint[endpoint]
        if not e.get("skipped"):
            e["p_holm"]   = p_adj[j]
            e["rejected_holm"] = rejected[j]
            j += 1

    n_passing = sum(1 for e in per_endpoint.values()
                    if e.get("rejected_holm", False) and e.get("passed_endpoint", False))
    return {
        "hypothesis":             "H6 (§11.7) — thrIVE-dynamic > LeWM-streaming on streaming endpoints",
        "test":                   "Paired BEST per endpoint, Holm-Bonferroni corrected",
        "n_paired_conditions":    int(len(merged)),
        "n_subjects":             int(merged["subject"].nunique()),
        "per_endpoint":           per_endpoint,
        "n_endpoints_passing":    int(n_passing),
        "passed":                 bool(n_passing >= 1),
    }


def test_h7(twin_df: pd.DataFrame, ensemble_df: pd.DataFrame) -> Dict:
    """H7 — paired BEST per endpoint vs mainstream ensemble.

    E6 (hyperdirect halt) and E7' (sheaf-fusion ratio) reported as N/A by
    design; ensemble has no equivalent and the spec §11.3 commits to this
    explicitly.
    """
    merged = pd.merge(
        twin_df, ensemble_df,
        on=["subject", "stressor", "mode"],
        suffixes=("_twin", "_ens"),
        how="inner",
    )
    per_endpoint: Dict[str, Dict] = {}
    p_values: List[float] = []
    for endpoint, sign in H7_ENDPOINTS.items():
        col_twin = f"{endpoint}_twin"
        col_ens  = f"{endpoint}_ens"
        if col_twin not in merged.columns or col_ens not in merged.columns:
            per_endpoint[endpoint] = {
                "endpoint": endpoint, "skipped": True,
                "reason": "endpoint missing from input data", "passed_endpoint": False,
            }
            continue
        result = compare_endpoint(
            merged[col_twin].values, merged[col_ens].values, endpoint, sign,
        )
        per_endpoint[endpoint] = result
        if not result.get("skipped"):
            p_values.append(result["p_one_sided"])

    p_adj, rejected = holm_bonferroni(p_values) if p_values else ([], [])
    j = 0
    for endpoint in H7_ENDPOINTS:
        e = per_endpoint[endpoint]
        if not e.get("skipped"):
            e["p_holm"]   = p_adj[j]
            e["rejected_holm"] = rejected[j]
            j += 1

    # E6, E7' reported as N/A by design (spec §11.3)
    per_endpoint["e6_halt_latency_ms"] = {
        "endpoint": "e6_halt_latency_ms", "n_a": True,
        "reason":   "mainstream ensemble has no hyperdirect-pathway equivalent (§11.3)",
        "passed_endpoint": False,
    }
    per_endpoint["e7_fusion_ratio"] = {
        "endpoint": "e7_fusion_ratio", "n_a": True,
        "reason":   "mainstream ensemble has no sheaf-fusion ratio (§11.3)",
        "passed_endpoint": False,
    }

    n_passing = sum(1 for e in per_endpoint.values()
                    if e.get("rejected_holm", False) and e.get("passed_endpoint", False))
    return {
        "hypothesis":             "H7 (§11.7) — thrIVE-composite > mainstream-ensemble on streaming endpoints",
        "test":                   "Paired BEST per endpoint, Holm-Bonferroni corrected",
        "n_paired_conditions":    int(len(merged)),
        "n_subjects":             int(merged["subject"].nunique()),
        "per_endpoint":           per_endpoint,
        "n_endpoints_passing":    int(n_passing),
        "passed":                 bool(n_passing >= 1),
    }


def joint_h6_h7_verdict(h6: Dict, h7: Dict) -> Dict:
    """§11.6 joint H6/H7 interpretation matrix."""
    h6p = bool(h6.get("passed", False))
    h7p = bool(h7.get("passed", False))
    if h6p and h7p:
        return {
            "verdict": "STRONGEST",
            "action":  "Full dynamical-architecture justification; H6+H7 both pass.",
        }
    if h6p and not h7p:
        return {
            "verdict": "NARROWED",
            "action":  ("thrIVE beats LeWM but not the mainstream ensemble. "
                        "Architectural claim is narrower than original scope: "
                        "the dynamical complexity is unjustified relative to "
                        "deployable BCI alternatives. Spec must be revised."),
        }
    if (not h6p) and h7p:
        return {
            "verdict": "INVERTED",
            "action":  ("Suspect outcome — thrIVE beats mainstream but loses "
                        "to LeWM (LeWM is a research model that the mainstream "
                        "ensemble does not beat in the published literature). "
                        "Investigate before publishing."),
        }
    return {
        "verdict": "FALLBACK",
        "action":  ("Mainstream-ensemble identity per §2 of (C)-OSF-Pre"
                    "registration-Phase-A1: dynamical spine collapses to "
                    "the locked mainstream ensemble; representational claims "
                    "(H1-H10) evaluated independently."),
    }


# =============================================================================
# Smoke test
# =============================================================================

def _make_synthetic_df(n_subjects: int, label: str, twin_bias: float, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for sub in range(n_subjects):
        for stressor in ("clean", "channel_dropout", "emg", "drift"):
            for mode in ("static", "pseudo_streaming", "full_streaming", "sensory_absent"):
                rows.append({
                    "subject":             f"S{sub+1:03d}",
                    "stressor":            stressor,
                    "mode":                mode,
                    "e1_latency_ms":       float(np.clip(120 - 20*twin_bias + rng.normal(0, 15), 10, 500)),
                    "e2_recovery_cycles":  float(np.clip(40 - 5*twin_bias + rng.normal(0, 8), 0, 200)),
                    "e3_fpr_drift":        float(rng.normal(0.0, 0.05) - 0.01*twin_bias),
                    "e4_cross_modal_mean": float(np.clip(0.5 + 0.15*twin_bias + rng.normal(0, 0.05), 0.0, 1.0)),
                    "e6_halt_latency_ms":  float(np.clip(60 - 10*twin_bias + rng.normal(0, 5), 5, 200)) if label == "twin" else float("nan"),
                    "e7_fusion_ratio":     float(np.clip(0.4 + 0.2*twin_bias + rng.normal(0, 0.05), 0.0, 2.0)) if label == "twin" else float("nan"),
                })
    return pd.DataFrame(rows)


def smoke_test() -> Dict:
    """Generate synthetic twin/lewm/ensemble dataframes where twin is
    moderately better. Verify H6 and H7 both pass."""
    twin     = _make_synthetic_df(20, "twin",     twin_bias=+1.0, seed=MASTER_SEED + 0)
    lewm     = _make_synthetic_df(20, "lewm",     twin_bias=-1.0, seed=MASTER_SEED + 1)
    ensemble = _make_synthetic_df(20, "ensemble", twin_bias=-0.5, seed=MASTER_SEED + 2)
    h6 = test_h6(twin, lewm)
    h7 = test_h7(twin, ensemble)
    joint = joint_h6_h7_verdict(h6, h7)
    return {
        "mode":     "smoke_test",
        "h6_passed": h6["passed"],
        "h7_passed": h7["passed"],
        "joint":     joint,
        "smoke_test_passed": bool(h6["passed"] and h7["passed"] and joint["verdict"] == "STRONGEST"),
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
        description="Phase A-7 H6/H7 verdict computation (registered analysis)"
    )
    parser.add_argument("--twin-dir",     type=Path, default=None,
                        help="Directory of Phase A-7 ACP twin endpoint JSONs")
    parser.add_argument("--lewm-dir",     type=Path, default=None,
                        help="Directory of Phase A-7 LeWM-baseline endpoint JSONs")
    parser.add_argument("--ensemble-dir", type=Path, default=None,
                        help="Directory of Phase A-7 mainstream-ensemble JSONs")
    parser.add_argument("--output",       type=Path, required=True,
                        help="Output verdict JSON")
    parser.add_argument("--smoke-test",   action="store_true",
                        help="Run synthetic smoke test (no real Phase A-7 data needed)")
    args = parser.parse_args(argv)

    np.random.seed(MASTER_SEED)

    if args.smoke_test:
        result = smoke_test()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2))
        print(f"OK: smoke test wrote {args.output}", file=sys.stderr)
        print(f"[A-7] smoke_test_passed={result['smoke_test_passed']}", file=sys.stderr)
        return 0 if result["smoke_test_passed"] else 1

    if args.twin_dir is None or args.lewm_dir is None or args.ensemble_dir is None:
        print("ERROR: --twin-dir, --lewm-dir, --ensemble-dir are required for non-smoke mode",
              file=sys.stderr)
        return 2

    twin_df     = aggregate_per_subject(load_endpoint_dir(args.twin_dir))
    lewm_df     = aggregate_per_subject(load_endpoint_dir(args.lewm_dir))
    ensemble_df = aggregate_per_subject(load_endpoint_dir(args.ensemble_dir))

    h6 = test_h6(twin_df, lewm_df)
    h7 = test_h7(twin_df, ensemble_df)
    joint = joint_h6_h7_verdict(h6, h7)

    results = {
        "provenance": {
            "git_commit":     _git_commit_hash(),
            "script_sha256":  _script_sha256(__file__),
            "timestamp_utc":  datetime.datetime.now(datetime.UTC).isoformat(),
            "n_twin_rows":     int(len(twin_df)),
            "n_lewm_rows":     int(len(lewm_df)),
            "n_ensemble_rows": int(len(ensemble_df)),
        },
        "h6": h6,
        "h7": h7,
        "joint_h6_h7_verdict": joint,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2))
    print(f"OK: wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())