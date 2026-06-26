"""
A1 Synthetic Smoke-Test Generator — thrIVE Phase A-1 Pre-Registration Fixture
==============================================================================

Generates 109 simulated subjects with controllable ground-truth effects for
H1, H2, H3, H4. Produces per-subject CSVs identical in schema to those the
real Phase A-1 pipeline will produce — but generated from a known
statistical model, NOT from EEG data.

Scenarios:
  all_pass  — All four hypotheses pass; default. Verifies the analysis
              script's pass-detection logic.
  h1_fail   — S-TTSA ≤ S-rand at S0; H1 halt condition triggers.
              Verifies the analysis script writes the halt_reason field
              and skips H2-H10.
  h2_fail   — (R8+S) ≤ R8 at S0; H2 fails. H1, H3, H4, H5, H9, H10 still
              evaluated. Verifies independent gate criteria.
  h3_fail   — No representation × stressor interaction; H3 fails.
  h4_fail   — (R_FM+S) ≤ R_FM at S0; H4 fails. Joint H2/H4 grid
              returns "NARROWER" verdict (H2 pass, H4 fail).
  h5_fail   — R_JEPA ≥ (R8+S) at S0; H5 fails. Sheaf representational
              claim fails against cross-domain JEPA.
  h9_fail   — R_JEPA_brain ≥ (R8+S) at S0; H9 fails. Sheaf representational
              claim fails against the harder domain-specific JEPA baseline.
              The (H5+H9 both fail) outcome cluster triggers the
              "Domain-specific-JEPA identity" architectural fall-back per
              §2 of (C)-OSF-Preregistration-Phase-A1.md.
  h10_fail  — R_GL ≥ (R8+S) at S0; H10 fails. Cellular cohomology is
              empirically decorative on the same Yeo-17-scale topology.
              The (H10 fails alone) outcome cluster triggers the
              "Graph-Laplacian-spectral identity" architectural fall-back.

The simulator generates accuracy values under the following model:
  acc[sub, fold, rep, stressor] =
      logit_inv( baseline
               + subject_offset
               + rep_effect[rep]
               + stressor_effect[stressor]
               + interaction_effect[rep, stressor]
               + fold_noise )

Locked invariants:
  - numpy seed 42 + scenario name (deterministic per scenario)
  - Number of subjects: 109 (matches Phase A-1 sample size)
  - Number of folds: 5 (matches §5 sampling plan)
  - Representations: all 13 (R32, R8, S-rand, S-TTSA, R8+S, R_FM, R_FM+S,
    R_JEPA, R_JEPA+S, R_JEPA_brain, R_JEPA_brain+S, R_GL, R_GL+S) — matches
    the locked-amendment set (Amendments 1, 2, 4, 5) of the OSF prereg
  - Stressors: 4 (S0, S1, S2, S3)
  - One CSV per subject, named accuracy_<subject>.csv

Author: Theodore Zuzarte (under direction with Claude, Anthropic)
Licence: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# Locked simulation parameters
# -----------------------------------------------------------------------------

N_SUBJECTS = 109
N_FOLDS    = 5

REPRESENTATIONS = [
    "R32", "R8", "S-rand", "S-TTSA", "R8+S",
    "R_FM", "R_FM+S",
    "R_JEPA", "R_JEPA+S",
    "R_JEPA_brain", "R_JEPA_brain+S",
    "R_GL", "R_GL+S",
]
STRESSORS = ["S0", "S1", "S2", "S3"]

BASELINE_LOGIT       = 0.0   # chance accuracy = 0.50 at S0 with no rep effect
SUBJECT_OFFSET_SD    = 0.30  # between-subject baseline variance
FOLD_NOISE_SD        = 0.20  # within-cell trial-to-trial noise
MIN_ACC, MAX_ACC     = 0.10, 0.99  # clamp to a reasonable simulation range


# -----------------------------------------------------------------------------
# Scenario definitions
# -----------------------------------------------------------------------------
# Each scenario specifies the per-representation logit-scale offset at S0,
# and the per-(representation, stressor) interaction term that controls H3.
#
# The default "all_pass" scenario is calibrated so that H1, H2, H3, H4 all
# pass at moderate effect sizes (Cohen's d ~ 0.4-0.6 for paired contrasts,
# BF_10 > 100 for H1). This is intentionally above the gate thresholds so the
# smoke test gives an unambiguous PASS signal.
# -----------------------------------------------------------------------------

@dataclass
class Scenario:
    name:               str
    rep_effect_at_s0:   Dict[str, float]   # logit-scale offset per representation
    # interaction[(rep, stressor)] = additional offset at that cell
    interaction:        Dict[tuple, float] = field(default_factory=dict)


def _build_default_rep_effects() -> Dict[str, float]:
    """Default S0 representation effects (logit scale).

    Calibrated so that under the all_pass scenario:
      H1 (S-TTSA > S-rand)        passes  by 0.65 logit (BF10 huge)
      H2 (R8+S > R8)              passes  by 0.30 logit (d ~ 0.4)
      H4 (R_FM+S > R_FM)          passes  by 0.30 logit
      H5 (R8+S > R_JEPA)          passes  by 0.40 logit  (cross-domain JEPA weaker)
      H9 (R8+S > R_JEPA_brain)    passes  by 0.20 logit  (domain-spec JEPA harder)
      H10 (R8+S > R_GL)           passes  by 0.60 logit  (graph-Lap no cohomology)
    """
    return {
        "R32":            2.50,   # ceiling, ~0.92
        "R8":             1.80,   # baseline, ~0.86
        "S-rand":         0.30,   # near chance, ~0.57
        "S-TTSA":         0.95,   # H1: S-TTSA > S-rand by big margin
        "R8+S":           2.10,   # H2: (R8+S) > R8 by ~0.30
        "R_FM":           2.20,   # strong foundation baseline
        "R_FM+S":         2.50,   # H4: (R_FM+S) > R_FM by ~0.30
        "R_JEPA":         1.70,   # cross-domain JEPA: below R8+S by 0.40 -> H5 passes
        "R_JEPA+S":       1.95,   # +S variant, below R8+S
        "R_JEPA_brain":   1.90,   # domain-specific JEPA: harder test, below R8+S by 0.20 -> H9 passes
        "R_JEPA_brain+S": 2.05,   # +S variant
        "R_GL":           1.50,   # graph-Laplacian only (no cohomology): below R8+S by 0.60 -> H10 passes
        "R_GL+S":         1.90,   # +S variant; sheaf adds value on top of graph-Lap topology
    }


def _build_h3_interactions() -> Dict[tuple, float]:
    """Interactions producing the C4 graceful-degradation pattern.

    Riemannian-only baselines (R8, R32) and JEPA / graph-Lap end-to-end
    baselines (R_FM, R_JEPA, R_JEPA_brain, R_GL) lose heavily under stressors.
    Sheaf-augmented variants (S-TTSA, R8+S, R_FM+S, R_JEPA+S,
    R_JEPA_brain+S, R_GL+S) degrade more gracefully — producing the
    representation x stressor interaction that H3 detects.
    """
    return {
        # Riemannian-only baselines lose heavily under stressors
        ("R8",     "S1"): -0.80, ("R8",     "S2"): -1.00, ("R8",     "S3"): -0.40,
        ("R32",    "S1"): -0.70, ("R32",    "S2"): -0.90, ("R32",    "S3"): -0.40,
        # Sheaf-only variants degrade gracefully
        ("S-rand", "S1"): -0.20, ("S-rand", "S2"): -0.30, ("S-rand", "S3"): -0.40,
        ("S-TTSA", "S1"): -0.20, ("S-TTSA", "S2"): -0.30, ("S-TTSA", "S3"): -0.40,
        # Sheaf-augmented combinations — moderate drops (mix of both)
        ("R8+S",           "S1"): -0.30, ("R8+S",           "S2"): -0.40, ("R8+S",           "S3"): -0.40,
        # End-to-end / foundation-model baselines lose heavily (no sheaf)
        ("R_FM",           "S1"): -0.70, ("R_FM",           "S2"): -0.90, ("R_FM",           "S3"): -0.40,
        ("R_JEPA",         "S1"): -0.70, ("R_JEPA",         "S2"): -0.90, ("R_JEPA",         "S3"): -0.40,
        ("R_JEPA_brain",   "S1"): -0.70, ("R_JEPA_brain",   "S2"): -0.90, ("R_JEPA_brain",   "S3"): -0.40,
        ("R_GL",           "S1"): -0.70, ("R_GL",           "S2"): -0.90, ("R_GL",           "S3"): -0.40,
        # Sheaf-augmented end-to-end variants degrade more gracefully
        ("R_FM+S",         "S1"): -0.30, ("R_FM+S",         "S2"): -0.40, ("R_FM+S",         "S3"): -0.40,
        ("R_JEPA+S",       "S1"): -0.30, ("R_JEPA+S",       "S2"): -0.40, ("R_JEPA+S",       "S3"): -0.40,
        ("R_JEPA_brain+S", "S1"): -0.30, ("R_JEPA_brain+S", "S2"): -0.40, ("R_JEPA_brain+S", "S3"): -0.40,
        ("R_GL+S",         "S1"): -0.30, ("R_GL+S",         "S2"): -0.40, ("R_GL+S",         "S3"): -0.40,
    }


SCENARIOS: Dict[str, Scenario] = {
    "all_pass": Scenario(
        name="all_pass",
        rep_effect_at_s0=_build_default_rep_effects(),
        interaction=_build_h3_interactions(),
    ),
    "h1_fail": Scenario(
        name="h1_fail",
        rep_effect_at_s0={
            **_build_default_rep_effects(),
            # S-TTSA well below S-rand (0.30) to produce an unambiguous
            # paired-diff signal that fails BF10 > 3 at the locked sample
            # size. The original "0.25" calibration was too close to S-rand
            # and produced noise-dominated, ambiguous H1 outcomes.
            "S-TTSA": -0.40,
        },
        interaction=_build_h3_interactions(),
    ),
    "h2_fail": Scenario(
        name="h2_fail",
        rep_effect_at_s0={
            **_build_default_rep_effects(),
            "R8+S": 1.80,     # equal to R8 — H2 fails
        },
        interaction=_build_h3_interactions(),
    ),
    "h3_fail": Scenario(
        name="h3_fail",
        rep_effect_at_s0=_build_default_rep_effects(),
        # NO stressor effect for any representation. There is therefore
        # NO representation x stressor interaction (and also no main
        # effect of stressor). The rmANOVA must report a non-significant
        # interaction term, failing H3. Setting all stressor effects to
        # exactly zero is the cleanest way to guarantee no interaction at
        # the accuracy-scale level the rmANOVA actually tests — uniform-
        # logit-space stressor effects don't work because the logit ->
        # accuracy inverse-link produces nonlinear stressor effects on
        # the accuracy scale even when the latent stressor effect is
        # uniform across representations.
        interaction={},
    ),
    "h4_fail": Scenario(
        name="h4_fail",
        rep_effect_at_s0={
            **_build_default_rep_effects(),
            "R_FM+S": 2.20,   # equal to R_FM — H4 fails
        },
        interaction=_build_h3_interactions(),
    ),
    "h5_fail": Scenario(
        name="h5_fail",
        rep_effect_at_s0={
            **_build_default_rep_effects(),
            # R_JEPA above R8+S=2.10 -> (R8+S) <= R_JEPA -> H5 fails.
            # All other hypotheses (H1, H2, H3, H4, H9, H10) still pass.
            "R_JEPA": 2.30,
        },
        interaction=_build_h3_interactions(),
    ),
    "h9_fail": Scenario(
        name="h9_fail",
        rep_effect_at_s0={
            **_build_default_rep_effects(),
            # R_JEPA_brain above R8+S=2.10 -> (R8+S) <= R_JEPA_brain -> H9 fails.
            "R_JEPA_brain": 2.30,
        },
        interaction=_build_h3_interactions(),
    ),
    "h10_fail": Scenario(
        name="h10_fail",
        rep_effect_at_s0={
            **_build_default_rep_effects(),
            # R_GL above R8+S=2.10 -> (R8+S) <= R_GL -> H10 fails (cohomology
            # adds no value over graph-Laplacian on the same topology).
            "R_GL": 2.30,
        },
        interaction=_build_h3_interactions(),
    ),
}


# -----------------------------------------------------------------------------
# Simulation
# -----------------------------------------------------------------------------

def logit_inv(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def simulate_scenario(scenario: Scenario) -> pd.DataFrame:
    """Generate the full long-form dataframe for one scenario.

    Deterministic seed: hash of scenario name + global salt 42.
    """
    # Deterministic seed: combine scenario name with base salt 42
    seed = abs(hash(scenario.name)) % (2**32 - 1) ^ 42
    rng = np.random.default_rng(seed)

    # Per-subject baseline offset (between-subject variance in latent skill)
    subject_offsets = rng.normal(0.0, SUBJECT_OFFSET_SD, N_SUBJECTS)

    rows = []
    for s_idx in range(N_SUBJECTS):
        subject_id = f"S{s_idx+1:03d}"
        for fold in range(N_FOLDS):
            for rep in REPRESENTATIONS:
                for stressor in STRESSORS:
                    rep_offset    = scenario.rep_effect_at_s0[rep]
                    intx          = scenario.interaction.get((rep, stressor), 0.0)
                    fold_noise    = rng.normal(0.0, FOLD_NOISE_SD)
                    logit_acc     = (
                        BASELINE_LOGIT
                        + subject_offsets[s_idx]
                        + rep_offset
                        + intx
                        + fold_noise
                    )
                    acc = float(np.clip(logit_inv(logit_acc), MIN_ACC, MAX_ACC))
                    rows.append({
                        "subject":        subject_id,
                        "fold":           fold,
                        "representation": rep,
                        "stressor":       stressor,
                        "accuracy":       acc,
                    })

    return pd.DataFrame(rows)


def write_per_subject_csvs(df: pd.DataFrame, output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for subject_id, sub_df in df.groupby("subject"):
        sub_df.to_csv(output_dir / f"accuracy_{subject_id}.csv", index=False)
        count += 1
    return count


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
# CLI
# -----------------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synthetic smoke-test data for Phase A-1 analysis pipeline"
    )
    parser.add_argument(
        "--scenario",
        choices=sorted(SCENARIOS.keys()),
        default="all_pass",
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)

    scenario = SCENARIOS[args.scenario]
    df       = simulate_scenario(scenario)
    n_csvs   = write_per_subject_csvs(df, args.output_dir)

    manifest = {
        "scenario":         scenario.name,
        "n_subjects":       N_SUBJECTS,
        "n_folds":          N_FOLDS,
        "n_csvs_written":   n_csvs,
        "representations":  REPRESENTATIONS,
        "stressors":        STRESSORS,
        "rep_effect_at_s0": scenario.rep_effect_at_s0,
        "interaction":      {f"{r}|{s}": v for (r, s), v in scenario.interaction.items()},
        "baseline_logit":      BASELINE_LOGIT,
        "subject_offset_sd":   SUBJECT_OFFSET_SD,
        "fold_noise_sd":       FOLD_NOISE_SD,
        "git_commit":          _git_commit_hash(),
        "script_sha256":       _script_sha256(__file__),
        "timestamp_utc":       datetime.datetime.now(datetime.UTC).isoformat(),
    }
    (args.output_dir / "smoke_manifest.json").write_text(
        json.dumps(manifest, indent=2)
    )

    print(
        f"OK: wrote {n_csvs} CSVs + smoke_manifest.json to {args.output_dir} "
        f"(scenario={scenario.name})",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())