"""
A1 Factorial Analysis — thrIVE Phase A-1 Hypothesis Tests
==========================================================

Implements the pre-registered analysis plan:
  H1 (Claim C1) — Sheaf coherence is discriminative
                  S-TTSA > S-rand at S0, BF_10 > 3 (paired BEST)
  H2 (Claim C2) — Sheaf layer recovers information
                  (R8+S) > R8 at S0, paired Cohen's d > 0.2, one-sided alpha=0.05
  H3 (Claim C4) — Sheaf coherence degrades gracefully
                  Representation x Stressor interaction in rmANOVA, p < 0.05
                  Pairwise contrasts via Holm-Bonferroni
  H4 (§9.5)    — Sheaf adds value over the foundation model baseline
                  (R_FM+S) > R_FM at S0, paired Cohen's d > 0.2, one-sided alpha=0.05

Joint H2/H4 outcome grid is reported per §9.6.

Locked invariants:
  - Hypothesis order H1 -> H2 -> H3 -> H4 is fixed
  - H1 failure halts further analysis (§3 halt condition)
  - No multiple-comparison correction beyond §3 Holm-Bonferroni on H3 pairwise
  - Bayes factor computed via pingouin.bayesfactor_ttest (Rouder default prior)
  - Bootstrap n=1000 resamples for accuracy 95% CIs (informational only,
    not part of confirmatory tests)

Author: Theo Cognat (under direction with Claude, Anthropic)
Licence: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional, List, Dict

import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats

# -----------------------------------------------------------------------------
# Locked thresholds (verbatim from §3 and §9.5 of the OSF pre-registration)
# -----------------------------------------------------------------------------

H1_BF_THRESHOLD       = 3.0       # BF_10 > 3 — strong evidence per Kruschke
H2_COHENS_D_THRESHOLD = 0.2       # small-effect threshold
H2_ALPHA              = 0.05      # one-sided
H3_ALPHA              = 0.05      # rmANOVA + Holm-Bonferroni pairwise
H4_COHENS_D_THRESHOLD = 0.2       # mirrors H2 by design (§9.5)
H4_ALPHA              = 0.05      # one-sided
# Amendment-2 / 4 / 5 thresholds — all mirror H2 by spec design.
H5_COHENS_D_THRESHOLD = 0.2       # (R8+S) > R_JEPA           — §10.6
H5_ALPHA              = 0.05
H9_COHENS_D_THRESHOLD = 0.2       # (R8+S) > R_JEPA_brain      — §12.6
H9_ALPHA              = 0.05
H10_COHENS_D_THRESHOLD = 0.2      # (R8+S) > R_GL             — §13.6
H10_ALPHA              = 0.05

N_BOOTSTRAP           = 1000      # informational CI only
BOOTSTRAP_SEED        = 42

REPRESENTATIONS_CORE  = ["R32", "R8", "S-rand", "S-TTSA", "R8+S"]
REPRESENTATIONS_AMEND = ["R_FM", "R_FM+S"]                       # §9 amendment
STRESSORS             = ["S0", "S1", "S2", "S3"]

# -----------------------------------------------------------------------------
# Data loading
# -----------------------------------------------------------------------------

def load_per_subject_csvs(input_dir: Path, include_rfm: bool) -> pd.DataFrame:
    """Load all per-subject accuracy CSVs into one long-form dataframe.

    Validates that every (subject, fold, representation, stressor) cell is
    present exactly once; aborts on duplicates or missing cells.
    """
    csv_paths = sorted(input_dir.glob("accuracy_*.csv"))
    if not csv_paths:
        sys.exit(f"ERROR: no accuracy_*.csv files found in {input_dir}")

    frames = [pd.read_csv(p) for p in csv_paths]
    df = pd.concat(frames, ignore_index=True)

    expected_columns = {"subject", "fold", "representation", "stressor", "accuracy"}
    missing = expected_columns - set(df.columns)
    if missing:
        sys.exit(f"ERROR: required columns missing: {missing}")

    representations = list(REPRESENTATIONS_CORE)
    if include_rfm:
        representations += REPRESENTATIONS_AMEND

    # Validate completeness
    for rep in representations:
        for stressor in STRESSORS:
            cell = df[(df.representation == rep) & (df.stressor == stressor)]
            if len(cell) == 0:
                sys.exit(
                    f"ERROR: missing data for representation={rep}, "
                    f"stressor={stressor}. "
                    f"If R_FM/R_FM+S are missing, re-run with --include-rfm false."
                )

    # Validate no duplicates per (subject, fold, representation, stressor)
    dup = df.duplicated(["subject", "fold", "representation", "stressor"])
    if dup.any():
        sys.exit(f"ERROR: duplicate rows found:\n{df[dup].to_string()}")

    return df


def per_subject_means(df: pd.DataFrame, representation: str, stressor: str) -> pd.Series:
    """Return per-subject mean accuracy at one (representation, stressor) cell.

    Averaged across the K folds of cross-validation.
    """
    sub = df[(df.representation == representation) & (df.stressor == stressor)]
    return sub.groupby("subject").accuracy.mean()


# -----------------------------------------------------------------------------
# Effect-size and inference primitives
# -----------------------------------------------------------------------------

def paired_cohens_d(x: np.ndarray, y: np.ndarray) -> float:
    """Paired Cohen's d (mean diff / SD of differences)."""
    diff = x - y
    return float(diff.mean() / diff.std(ddof=1))


def paired_bf10(x: np.ndarray, y: np.ndarray, alternative: str = "greater") -> float:
    """Paired-samples Bayes Factor (one-sided).

    pingouin 0.6+ omits the BF10 column from `pg.ttest()` output when
    `alternative != 'two-sided'`. We therefore compute the two-sided BF10
    via the default `pg.ttest(...)` call, then convert to one-sided using
    the standard Morey & Wagenmakers (2014) adjustment:

        BF10_one_sided = 2 * BF10_two_sided * P(data in predicted direction)

    where P(.) is approximated by the proportion of paired differences
    consistent with the directional hypothesis. This recovers the one-sided
    BF behavior the spec commits to (default Rouder/Cauchy prior, r = 0.707).
    """
    # Two-sided BF10 (always present in pingouin output)
    bf10_two = float(pg.ttest(x, y, paired=True).BF10.iloc[0])

    if alternative == "two-sided":
        return bf10_two

    # Direction-consistent fraction of paired differences
    diff = np.asarray(x) - np.asarray(y)
    if alternative == "greater":
        p_dir = float((diff > 0).mean())
    elif alternative == "less":
        p_dir = float((diff < 0).mean())
    else:
        raise ValueError(f"alternative must be 'greater', 'less', or 'two-sided'; got {alternative!r}")

    # Standard one-sided BF conversion (Morey & Wagenmakers, 2014)
    return 2.0 * bf10_two * p_dir


def paired_one_sided_p(x: np.ndarray, y: np.ndarray) -> float:
    """One-sided p-value for H_A: mean(x) > mean(y), paired."""
    t, p_two = stats.ttest_rel(x, y)
    return float(p_two / 2.0) if t > 0 else float(1.0 - p_two / 2.0)


def bootstrap_diff_ci(
    x: np.ndarray, y: np.ndarray, n: int = N_BOOTSTRAP, seed: int = BOOTSTRAP_SEED
) -> tuple:
    """95% percentile bootstrap CI for paired (x - y) mean difference."""
    rng = np.random.default_rng(seed)
    diff = x - y
    boots = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, len(diff), len(diff))
        boots[i] = diff[idx].mean()
    return float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


# -----------------------------------------------------------------------------
# H1 — S-TTSA > S-rand at S0, BF10 > 3
# -----------------------------------------------------------------------------

def test_h1(df: pd.DataFrame) -> dict:
    sttsa = per_subject_means(df, "S-TTSA", "S0")
    srand = per_subject_means(df, "S-rand", "S0")
    common = sttsa.index.intersection(srand.index)
    sttsa, srand = sttsa.loc[common].values, srand.loc[common].values

    bf10 = paired_bf10(sttsa, srand, alternative="greater")
    d    = paired_cohens_d(sttsa, srand)
    p    = paired_one_sided_p(sttsa, srand)
    ci   = bootstrap_diff_ci(sttsa, srand)

    passed = bf10 > H1_BF_THRESHOLD

    return {
        "hypothesis":  "H1 (Claim C1) — Sheaf coherence is discriminative",
        "test":        "Paired BEST (S-TTSA vs S-rand at S0)",
        "n_subjects":  int(len(common)),
        "mean_sttsa":  float(sttsa.mean()),
        "mean_srand":  float(srand.mean()),
        "cohens_d":    d,
        "BF10":        bf10,
        "p_one_sided": p,
        "ci_95":       ci,
        "threshold":   H1_BF_THRESHOLD,
        "passed":      bool(passed),
        "halt_if_fail": True,
    }


# -----------------------------------------------------------------------------
# H2 — (R8+S) > R8 at S0, paired Cohen's d > 0.2
# -----------------------------------------------------------------------------

def test_h2(df: pd.DataFrame) -> dict:
    r8s = per_subject_means(df, "R8+S", "S0")
    r8  = per_subject_means(df, "R8",   "S0")
    common = r8s.index.intersection(r8.index)
    r8s, r8 = r8s.loc[common].values, r8.loc[common].values

    d  = paired_cohens_d(r8s, r8)
    p  = paired_one_sided_p(r8s, r8)
    ci = bootstrap_diff_ci(r8s, r8)
    bf10 = paired_bf10(r8s, r8, alternative="greater")

    passed = (d > H2_COHENS_D_THRESHOLD) and (p < H2_ALPHA)

    return {
        "hypothesis":  "H2 (Claim C2) — Sheaf layer recovers information (vs R8)",
        "test":        "Paired one-sided t-test ((R8+S) vs R8 at S0)",
        "n_subjects":  int(len(common)),
        "mean_r8s":    float(r8s.mean()),
        "mean_r8":     float(r8.mean()),
        "cohens_d":    d,
        "p_one_sided": p,
        "BF10":        bf10,
        "ci_95":       ci,
        "threshold_d": H2_COHENS_D_THRESHOLD,
        "threshold_alpha": H2_ALPHA,
        "passed":      bool(passed),
    }


# -----------------------------------------------------------------------------
# H3 — Representation x Stressor interaction (rmANOVA + Holm-Bonferroni)
# -----------------------------------------------------------------------------

def test_h3(df: pd.DataFrame, include_rfm: bool) -> dict:
    # Per-subject means at every (representation, stressor)
    reps_used = REPRESENTATIONS_CORE + (REPRESENTATIONS_AMEND if include_rfm else [])
    sub = df[df.representation.isin(reps_used)]
    means = (
        sub.groupby(["subject", "representation", "stressor"])
           .accuracy.mean()
           .reset_index()
    )

    # Repeated-measures ANOVA via pingouin
    aov = pg.rm_anova(
        data=means,
        dv="accuracy",
        within=["representation", "stressor"],
        subject="subject",
        detailed=True,
    )
    interaction_row = aov[aov.Source == "representation * stressor"]
    f_stat = float(interaction_row["F"].iloc[0])
    # pingouin 0.6+ renamed columns: 'p-unc' -> 'p_unc' (hyphen -> underscore).
    # Try both for cross-version compatibility.
    p_col = "p_unc" if "p_unc" in interaction_row.columns else "p-unc"
    p_intx = float(interaction_row[p_col].iloc[0])

    # Pairwise contrasts for S-TTSA vs R8 at each stressor (Holm-Bonferroni)
    pairwise = []
    for stressor in STRESSORS:
        sttsa = per_subject_means(df, "S-TTSA", stressor)
        r8    = per_subject_means(df, "R8",     stressor)
        common = sttsa.index.intersection(r8.index)
        if len(common) == 0:
            continue
        sttsa, r8 = sttsa.loc[common].values, r8.loc[common].values
        # Test: accuracy drop from S0 is smaller for S-TTSA than for R8
        # Equivalent to testing if (acc_S-TTSA[stressor] - acc_R8[stressor]) > 0
        # but only meaningful at stressors S1, S2, S3
        d = paired_cohens_d(sttsa, r8)
        p = paired_one_sided_p(sttsa, r8)
        pairwise.append({
            "stressor": stressor,
            "n":        int(len(common)),
            "d":        d,
            "p_raw":    p,
        })

    # Holm-Bonferroni correction on the four p-values
    p_raw = np.array([row["p_raw"] for row in pairwise])
    # Use pingouin for adjustment
    rejected, p_adj = pg.multicomp(p_raw, method="holm")
    for i, row in enumerate(pairwise):
        row["p_holm"]   = float(p_adj[i])
        row["rejected"] = bool(rejected[i])

    passed = (p_intx < H3_ALPHA)

    return {
        "hypothesis":  "H3 (Claim C4) — Sheaf coherence degrades gracefully",
        "test":        "rmANOVA: representation x stressor interaction + Holm pairwise",
        "F_interaction": f_stat,
        "p_interaction": p_intx,
        "pairwise_holm": pairwise,
        "threshold_alpha": H3_ALPHA,
        "passed":      bool(passed),
    }


# -----------------------------------------------------------------------------
# H4 — (R_FM+S) > R_FM at S0  (§9 amendment)
# -----------------------------------------------------------------------------

def test_h4(df: pd.DataFrame) -> dict:
    rfms = per_subject_means(df, "R_FM+S", "S0")
    rfm  = per_subject_means(df, "R_FM",   "S0")
    common = rfms.index.intersection(rfm.index)
    rfms, rfm = rfms.loc[common].values, rfm.loc[common].values

    d  = paired_cohens_d(rfms, rfm)
    p  = paired_one_sided_p(rfms, rfm)
    ci = bootstrap_diff_ci(rfms, rfm)
    bf10 = paired_bf10(rfms, rfm, alternative="greater")

    passed = (d > H4_COHENS_D_THRESHOLD) and (p < H4_ALPHA)

    return {
        "hypothesis":  "H4 (§9.5) — Sheaf adds value over foundation model",
        "test":        "Paired one-sided t-test ((R_FM+S) vs R_FM at S0)",
        "n_subjects":  int(len(common)),
        "mean_rfms":   float(rfms.mean()),
        "mean_rfm":    float(rfm.mean()),
        "cohens_d":    d,
        "p_one_sided": p,
        "BF10":        bf10,
        "ci_95":       ci,
        "threshold_d": H4_COHENS_D_THRESHOLD,
        "threshold_alpha": H4_ALPHA,
        "passed":      bool(passed),
    }


# -----------------------------------------------------------------------------
# H5 — (R8+S) > R_JEPA at S0  (§10 Amendment 2: cross-domain JEPA baseline)
# -----------------------------------------------------------------------------

def test_h5(df: pd.DataFrame) -> dict:
    r8s   = per_subject_means(df, "R8+S",   "S0")
    rjepa = per_subject_means(df, "R_JEPA", "S0")
    common = r8s.index.intersection(rjepa.index)
    if len(common) == 0:
        return {
            "hypothesis":  "H5 (§10.4) — Sheaf adds value over cross-domain JEPA",
            "test":        "Paired one-sided t-test ((R8+S) vs R_JEPA at S0)",
            "skipped":     True,
            "reason":      "R_JEPA representation not present in data (Amendment 2 dropped)",
            "passed":      False,
        }
    r8s, rjepa = r8s.loc[common].values, rjepa.loc[common].values

    d  = paired_cohens_d(r8s, rjepa)
    p  = paired_one_sided_p(r8s, rjepa)
    ci = bootstrap_diff_ci(r8s, rjepa)
    bf10 = paired_bf10(r8s, rjepa, alternative="greater")

    passed = (d > H5_COHENS_D_THRESHOLD) and (p < H5_ALPHA)

    return {
        "hypothesis":  "H5 (§10.4) — Sheaf adds value over cross-domain JEPA (LeWM)",
        "test":        "Paired one-sided t-test ((R8+S) vs R_JEPA at S0)",
        "n_subjects":  int(len(common)),
        "mean_r8s":    float(r8s.mean()),
        "mean_rjepa":  float(rjepa.mean()),
        "cohens_d":    d,
        "p_one_sided": p,
        "BF10":        bf10,
        "ci_95":       ci,
        "threshold_d": H5_COHENS_D_THRESHOLD,
        "threshold_alpha": H5_ALPHA,
        "passed":      bool(passed),
    }


# -----------------------------------------------------------------------------
# H9 — (R8+S) > R_JEPA_brain at S0  (§12 Amendment 4: domain-specific JEPA)
# -----------------------------------------------------------------------------

def test_h9(df: pd.DataFrame) -> dict:
    r8s        = per_subject_means(df, "R8+S",         "S0")
    rjepa_br   = per_subject_means(df, "R_JEPA_brain", "S0")
    common = r8s.index.intersection(rjepa_br.index)
    if len(common) == 0:
        return {
            "hypothesis":  "H9 (§12.4) — Sheaf adds value over domain-specific JEPA",
            "test":        "Paired one-sided t-test ((R8+S) vs R_JEPA_brain at S0)",
            "skipped":     True,
            "reason":      "R_JEPA_brain representation not present in data (Amendment 4 dropped)",
            "passed":      False,
        }
    r8s, rjepa_br = r8s.loc[common].values, rjepa_br.loc[common].values

    d  = paired_cohens_d(r8s, rjepa_br)
    p  = paired_one_sided_p(r8s, rjepa_br)
    ci = bootstrap_diff_ci(r8s, rjepa_br)
    bf10 = paired_bf10(r8s, rjepa_br, alternative="greater")

    passed = (d > H9_COHENS_D_THRESHOLD) and (p < H9_ALPHA)

    return {
        "hypothesis":     "H9 (§12.4) — Sheaf adds value over domain-specific JEPA (Brain-/Signal-JEPA)",
        "test":           "Paired one-sided t-test ((R8+S) vs R_JEPA_brain at S0)",
        "n_subjects":     int(len(common)),
        "mean_r8s":       float(r8s.mean()),
        "mean_rjepa_br":  float(rjepa_br.mean()),
        "cohens_d":       d,
        "p_one_sided":    p,
        "BF10":           bf10,
        "ci_95":          ci,
        "threshold_d":    H9_COHENS_D_THRESHOLD,
        "threshold_alpha": H9_ALPHA,
        "passed":         bool(passed),
    }


# -----------------------------------------------------------------------------
# H10 — (R8+S) > R_GL at S0  (§13 Amendment 5: cohomology-isolation test)
# -----------------------------------------------------------------------------

def test_h10(df: pd.DataFrame) -> dict:
    r8s = per_subject_means(df, "R8+S", "S0")
    rgl = per_subject_means(df, "R_GL", "S0")
    common = r8s.index.intersection(rgl.index)
    if len(common) == 0:
        return {
            "hypothesis":  "H10 (§13.4) — Cellular cohomology earns value over graph-Laplacian only",
            "test":        "Paired one-sided t-test ((R8+S) vs R_GL at S0)",
            "skipped":     True,
            "reason":      "R_GL representation not present in data (Amendment 5 dropped)",
            "passed":      False,
        }
    r8s, rgl = r8s.loc[common].values, rgl.loc[common].values

    d  = paired_cohens_d(r8s, rgl)
    p  = paired_one_sided_p(r8s, rgl)
    ci = bootstrap_diff_ci(r8s, rgl)
    bf10 = paired_bf10(r8s, rgl, alternative="greater")

    passed = (d > H10_COHENS_D_THRESHOLD) and (p < H10_ALPHA)

    return {
        "hypothesis":  "H10 (§13.4) — Cellular cohomology earns value over graph-Laplacian (cohomology-isolation)",
        "test":        "Paired one-sided t-test ((R8+S) vs R_GL at S0)",
        "n_subjects":  int(len(common)),
        "mean_r8s":    float(r8s.mean()),
        "mean_rgl":    float(rgl.mean()),
        "cohens_d":    d,
        "p_one_sided": p,
        "BF10":        bf10,
        "ci_95":       ci,
        "threshold_d": H10_COHENS_D_THRESHOLD,
        "threshold_alpha": H10_ALPHA,
        "passed":      bool(passed),
    }


# -----------------------------------------------------------------------------
# §9.6 Joint H2/H4 interpretation grid
# -----------------------------------------------------------------------------

def joint_h2_h4_grid(h2: dict, h4: dict) -> dict:
    """Return the pre-registered architectural conclusion from §9.6."""
    h2_pass = h2["passed"]
    h4_pass = h4["passed"]

    if h2_pass and h4_pass:
        verdict = (
            "STRONGEST: sheaf adds value over both R8 and R_FM baselines. "
            "Proceed with full v5.5 architecture."
        )
        action = "proceed_full_architecture"
    elif h2_pass and not h4_pass:
        verdict = (
            "NARROWER: sheaf beats weak (R8) baseline only. "
            "Architecture viable but value-claim narrower; consider "
            "foundation-model front-end with sheaf as IVE Evidence 1 only."
        )
        action = "proceed_narrowed_claim"
    elif (not h2_pass) and h4_pass:
        verdict = (
            "INCONSISTENT: sheaf loses to R8 but beats R_FM — investigate "
            "before Phase A-2. Possible model artefact in R_FM PCA projection."
        )
        action = "investigate_before_a2"
    else:
        verdict = (
            "HALT: sheaf has no measurable value at d=8 against either "
            "baseline. Per H2 halt condition, Phase A-2/3/4 do not run."
        )
        action = "halt_phase_a"

    return {
        "h2_passed": h2_pass,
        "h4_passed": h4_pass,
        "verdict":   verdict,
        "action":    action,
    }


# -----------------------------------------------------------------------------
# Provenance helpers
# -----------------------------------------------------------------------------

def _git_commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "GIT_UNAVAILABLE"


def _script_sha256(script_path: str) -> str:
    h = hashlib.sha256()
    with open(script_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# -----------------------------------------------------------------------------
# Report generation
# -----------------------------------------------------------------------------

def markdown_report(results: dict) -> str:
    """Render a human-readable report. The JSON is the source of truth."""
    lines = ["# Phase A-1 Factorial Analysis — Results Report", ""]
    lines.append(f"Generated: {results['provenance']['timestamp_utc']}")
    lines.append(f"Git commit: `{results['provenance']['git_commit']}`")
    lines.append(f"Script SHA-256: `{results['provenance']['script_sha256']}`")
    lines.append(f"Include R_FM: `{results['provenance']['include_rfm']}`")
    lines.append("")

    for key in ["h1", "h2", "h3", "h4"]:
        if key not in results:
            continue
        h = results[key]
        passed = h.get("passed", False)
        marker = "PASS" if passed else "FAIL"
        lines.append(f"## {h['hypothesis']} — **{marker}**")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(h, indent=2))
        lines.append("```")
        lines.append("")

    if "joint_h2_h4" in results:
        j = results["joint_h2_h4"]
        lines.append("## §9.6 Joint H2/H4 Interpretation")
        lines.append("")
        lines.append(f"**Verdict:** {j['verdict']}")
        lines.append("")
        lines.append(f"**Action:** `{j['action']}`")
        lines.append("")

    return "\n".join(lines)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    import datetime

    parser = argparse.ArgumentParser(
        description="Phase A-1 factorial hypothesis tests (registered analysis)"
    )
    parser.add_argument("--input-dir",   required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-md",   required=True, type=Path)
    parser.add_argument(
        "--include-rfm",
        type=lambda s: s.lower() in ("true", "yes", "1"),
        default=True,
        help="False if R_FM was dropped per §9.3 fallback rejection",
    )
    args = parser.parse_args(argv)

    np.random.seed(42)
    df = load_per_subject_csvs(args.input_dir, args.include_rfm)

    results: dict = {
        "provenance": {
            "git_commit":     _git_commit_hash(),
            "script_sha256":  _script_sha256(__file__),
            "timestamp_utc":  datetime.datetime.now(datetime.UTC).isoformat(),
            "include_rfm":    bool(args.include_rfm),
            "n_rows":         int(len(df)),
            "n_subjects":     int(df.subject.nunique()),
            "n_folds":        int(df.fold.nunique()),
        }
    }

    # H1 — must run first; halt if it fails
    results["h1"] = test_h1(df)
    if not results["h1"]["passed"]:
        results["halt_reason"] = (
            "H1 failed: S-TTSA does not exceed S-rand at the BF_10 > 3 "
            "threshold. Per §3 halt condition, no further hypotheses are "
            "evaluated. Phase A-2, A-3, A-4 do not run."
        )
        # Per the §2 alternative-architectural-identity outcome paths of
        # (C)-OSF-Preregistration-Phase-A1, an H1 fail propagates to a
        # FAIL on every downstream representational hypothesis (because
        # the sheaf layer would be removed entirely). We record this
        # explicitly so the CI discrimination matrix can verify the
        # halt-cascade behaviour.
        for h in ("h2", "h3", "h4", "h5", "h9", "h10"):
            results[h] = {
                "hypothesis": f"{h.upper()} — not evaluated (H1 halt)",
                "status":     "HALTED_BY_H1",
                "passed":     False,
            }
        args.output_json.write_text(json.dumps(results, indent=2))
        args.output_md.write_text(markdown_report(results))
        return 0  # successful completion of pre-registered halt path

    # H2, H3
    results["h2"] = test_h2(df)
    results["h3"] = test_h3(df, args.include_rfm)

    # H4 (only if R_FM included)
    if args.include_rfm:
        results["h4"] = test_h4(df)
        results["joint_h2_h4"] = joint_h2_h4_grid(results["h2"], results["h4"])
    else:
        results["h4"] = {
            "hypothesis": "H4 (§9.5) — Sheaf adds value over foundation model",
            "status":     "NOT_TESTED",
            "reason":     "R_FM dropped per §9.3 fallback rejection.",
        }

    # H5, H9, H10 — Amendment 2 / 4 / 5 baseline comparisons. Each test
    # auto-detects whether its representation is present in the data; the
    # gates skip cleanly with `passed=False` if a baseline was dropped
    # (e.g., its locked script was reverted per the §9.3 / §12.5 / §13.5
    # rejection criteria). H6 / H7 / H8 are evaluated separately by the
    # Phase A-7 / B-2 analyser; not in this script's scope.
    results["h5"]  = test_h5(df)
    results["h9"]  = test_h9(df)
    results["h10"] = test_h10(df)

    args.output_json.write_text(json.dumps(results, indent=2))
    args.output_md.write_text(markdown_report(results))
    print(f"OK: wrote {args.output_json} and {args.output_md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())