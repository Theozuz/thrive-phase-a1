"""
Phase A-0 Preflight Reference Pipeline
=======================================

Reproduces the MOABB Riemannian-tangent reference pipeline (TangentSpace +
L2 Logistic Regression on covariance matrices) on two motor-imagery
datasets:

  - PhysioNet EEGMMIDB (Schalk et al., 2004; Varbu et al., 2024 curation)
    Binary LeftRightImagery paradigm, 109 subjects
    Gate: grand-average accuracy >= 0.633
        (67.28% MOABB-published TS+LR - 4 pp tolerance; published sigma ~19 pp)
        Source: Chevallier et al. (2024) arXiv:2404.15319 Appendix D
        + https://moabb.neurotechx.com/docs/paper_results.html

  - BCI Competition IV-2a (Brunner et al., 2008)
    Four-class MotorImagery paradigm, 9 subjects
    Gate: grand-average accuracy >= 0.68
        (71.97% MOABB-published TS+LR - 4 pp tolerance; published sigma ~15 pp)
        Source: same as above

The script is the *gate* for the entire Phase A-1 programme. If neither
dataset reproduces, the H1-H10 confirmatory tests cannot be interpreted
because the reference baseline is not validated. Output JSON contains the
pass/fail verdict explicitly.

Locked invariants (cannot modify post-registration):
  - MOABB WithinSession evaluation, 5-fold stratified within-subject CV
  - Oracle Approximating Shrinkage covariance (pyriemann default)
  - Riemannian tangent-space mapping at the Frechet mean
  - L2 Logistic Regression, C=1.0, max_iter=1000
  - MOABB default paradigm settings (8-32 Hz, tmin=0, tmax=4 s)
  - Master seed 42
  - Gate thresholds (verified May 2026 against Chevallier et al. 2024):
      0.633 (PhysionetMI L/R binary), 0.68 (BCI IV-2a 4-class)

Author: Theodore Zuzarte (under direction with Claude, Anthropic)
Licence: MIT
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

import numpy as np


# =============================================================================
# Locked parameters
# =============================================================================

MASTER_SEED = 42

# Gate thresholds (from §3 of (C)-Phase-A-Experiment-Revised; verified
# against the MOABB official benchmark results page and Chevallier et al.
# (2024) arXiv:2404.15319 Appendix D, Tables 6-10, May 2026)
GATE_THRESHOLD_PHYSIONET    = 0.633  # 67.28% MOABB-published TS+LR (LeftRightImagery) - 4 pp tolerance
GATE_THRESHOLD_BCI_IV_2A    = 0.68   # 71.97% MOABB-published TS+LR (4-class)        - 4 pp tolerance

# MOABB-published TS+LR reference values (Chevallier et al. 2024, Appendix D)
MOABB_PUBLISHED = {
    "physionet": 0.6728,   # Left vs Right Hand binary; std ~0.1919 across 109 subjects
    "bci_iv_2a": 0.7197,   # All-classes 4-way; std ~0.1546 across 9 subjects
}

# MOABB paradigm settings (defaults; not overridden)
PHYSIONET_PARADIGM_NAME = "LeftRightImagery"
BCI_IV_2A_PARADIGM_NAME = "MotorImagery"

# Cross-validation
N_FOLDS = 5

# Classifier
LOGISTIC_C        = 1.0
LOGISTIC_MAX_ITER = 1000
LOGISTIC_PENALTY  = "l2"
LOGISTIC_SOLVER   = "liblinear"   # deterministic, no multithreading variance


# =============================================================================
# Smoke test (no MOABB dependency; runs offline)
# =============================================================================

def smoke_test() -> dict:
    """
    Verify the TangentSpace + LogisticRegression pipeline assembles and
    runs on synthetic Gaussian SPD-matrix data. Does not touch real EEG.
    """
    from pyriemann.tangentspace import TangentSpace
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline

    rng = np.random.default_rng(MASTER_SEED)

    # Synthetic 2-class SPD problem: class 0 = identity + noise,
    # class 1 = identity + class-specific perturbation + noise
    n_per_class = 100
    n_channels  = 8

    def make_class(perturb: np.ndarray, rng_: np.random.Generator) -> np.ndarray:
        out = np.empty((n_per_class, n_channels, n_channels))
        for i in range(n_per_class):
            noise = 0.1 * rng_.standard_normal((n_channels, n_channels))
            base  = np.eye(n_channels) + perturb + noise @ noise.T
            out[i] = base
        return out

    perturb_0 = np.zeros((n_channels, n_channels))
    perturb_1 = 0.5 * np.diag(np.linspace(1, 2, n_channels))

    X = np.concatenate([
        make_class(perturb_0, rng),
        make_class(perturb_1, rng),
    ], axis=0).astype(np.float64)
    y = np.concatenate([np.zeros(n_per_class), np.ones(n_per_class)]).astype(int)

    pipe = make_pipeline(
        TangentSpace(metric="riemann"),
        LogisticRegression(
            C=LOGISTIC_C,
            max_iter=LOGISTIC_MAX_ITER,
            penalty=LOGISTIC_PENALTY,
            solver=LOGISTIC_SOLVER,
            random_state=MASTER_SEED,
        ),
    )

    # 5-fold stratified CV via sklearn
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    cv = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=MASTER_SEED)
    scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")

    return {
        "smoke_test_passed": bool(scores.mean() > 0.95),  # easy synthetic problem
        "fold_accuracies":   scores.tolist(),
        "mean_accuracy":     float(scores.mean()),
        "n_samples":         int(X.shape[0]),
        "n_channels":        int(X.shape[1]),
    }


# =============================================================================
# Real-data evaluation via MOABB
# =============================================================================

def build_pipeline() -> "Pipeline":
    """The locked TangentSpace + L2 LogReg pipeline applied to covariance inputs."""
    from pyriemann.estimation import Covariances
    from pyriemann.tangentspace import TangentSpace
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline

    return make_pipeline(
        Covariances(estimator="oas"),
        TangentSpace(metric="riemann"),
        LogisticRegression(
            C=LOGISTIC_C,
            max_iter=LOGISTIC_MAX_ITER,
            penalty=LOGISTIC_PENALTY,
            solver=LOGISTIC_SOLVER,
            random_state=MASTER_SEED,
        ),
    )


def evaluate_dataset(
    dataset_name: str,
    single_subject: Optional[int] = None,
) -> dict:
    """
    Run MOABB WithinSession evaluation on the specified dataset using the
    locked TS+LR pipeline. Returns per-subject and grand-average accuracies
    plus the gate-pass verdict.
    """
    # Import MOABB lazily so smoke-test mode does not require it
    from moabb.datasets import PhysionetMI, BNCI2014_001
    from moabb.evaluations import WithinSessionEvaluation
    from moabb.paradigms import LeftRightImagery, MotorImagery

    if dataset_name == "physionet":
        dataset       = PhysionetMI()
        paradigm      = LeftRightImagery()
        gate_threshold = GATE_THRESHOLD_PHYSIONET
        paradigm_name = PHYSIONET_PARADIGM_NAME
        n_classes     = 2
    elif dataset_name == "bci_iv_2a":
        dataset       = BNCI2014_001()
        paradigm      = MotorImagery(n_classes=4)
        gate_threshold = GATE_THRESHOLD_BCI_IV_2A
        paradigm_name = BCI_IV_2A_PARADIGM_NAME
        n_classes     = 4
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    if single_subject is not None:
        dataset.subject_list = [single_subject]

    pipeline_dict = {"TS+LR": build_pipeline()}

    evaluation = WithinSessionEvaluation(
        paradigm=paradigm,
        datasets=[dataset],
        overwrite=False,                   # cache MOABB downloads
        n_jobs=1,                           # deterministic
        random_state=MASTER_SEED,
        hdf5_path=None,                    # in-memory results
    )

    results = evaluation.process(pipeline_dict)
    # results is a pandas DataFrame with columns: pipeline, dataset, subject,
    # session, score, time, n_samples, n_channels

    grand_avg = float(results["score"].mean())
    per_subject = (
        results.groupby("subject")["score"].mean().to_dict()
    )

    return {
        "dataset":            dataset_name,
        "paradigm":           paradigm_name,
        "n_classes":          n_classes,
        "n_subjects":         int(len(per_subject)),
        "per_subject":        {str(k): float(v) for k, v in per_subject.items()},
        "grand_average":      grand_avg,
        "gate_threshold":     gate_threshold,
        "gate_passed":        bool(grand_avg >= gate_threshold),
        "moabb_published":    MOABB_PUBLISHED[dataset_name],
        "delta_from_published": float(
            grand_avg - MOABB_PUBLISHED[dataset_name]
        ),
    }


# =============================================================================
# Manifest emission
# =============================================================================

def _script_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _try_git_revision() -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return None


def emit_manifest(
    dataset_name: str,
    output_path: Path,
    result: dict,
) -> dict:
    return {
        "schema_version": "a0_preflight_v1",
        "timestamp_utc":  datetime.datetime.utcnow().isoformat(),
        "script_sha256":  _script_sha256(),
        "git_revision":   _try_git_revision(),
        "python_version": sys.version,
        "platform":       platform.platform(),
        "master_seed":    MASTER_SEED,
        "locked_parameters": {
            "n_folds":            N_FOLDS,
            "logistic_C":         LOGISTIC_C,
            "logistic_max_iter":  LOGISTIC_MAX_ITER,
            "logistic_penalty":   LOGISTIC_PENALTY,
            "logistic_solver":    LOGISTIC_SOLVER,
            "covariance_estimator": "oas",
            "tangent_space_metric": "riemann",
            "gate_threshold_physionet": GATE_THRESHOLD_PHYSIONET,
            "gate_threshold_bci_iv_2a": GATE_THRESHOLD_BCI_IV_2A,
        },
        "dataset_evaluated": dataset_name,
        "result":            result,
        "output_path":       str(output_path),
    }


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Phase A-0 Preflight: MOABB Riemannian-tangent reference pipeline. "
            "Gates the entire Phase A-1 programme."
        ),
    )
    parser.add_argument(
        "--dataset",
        choices=["physionet", "bci_iv_2a"],
        help="Dataset to evaluate (omit for --smoke-test only)",
    )
    parser.add_argument(
        "--single-subject", type=int, default=None,
        help="Restrict evaluation to a single subject (for fast sanity check)",
    )
    parser.add_argument(
        "--smoke-test", action="store_true",
        help="Run synthetic-data smoke test only (no MOABB, no real EEG)",
    )
    parser.add_argument(
        "--output", type=Path, required=True,
        help="Path for JSON result output",
    )
    parser.add_argument(
        "--manifest", type=Path, default=None,
        help="Path for JSON manifest (script hash + locked config)",
    )
    args = parser.parse_args()

    np.random.seed(MASTER_SEED)

    if args.smoke_test:
        result = smoke_test()
        result["mode"] = "smoke_test"
    else:
        if args.dataset is None:
            print("ERROR: --dataset is required unless --smoke-test", file=sys.stderr)
            return 2
        result = evaluate_dataset(
            dataset_name=args.dataset,
            single_subject=args.single_subject,
        )
        result["mode"] = (
            "single_subject" if args.single_subject is not None else "full"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True))

    if args.manifest is not None:
        manifest = emit_manifest(
            dataset_name=args.dataset or "smoke_test",
            output_path=args.output,
            result=result,
        )
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True))

    # Human-readable summary to stderr
    print(f"[A-0] mode={result.get('mode')} dataset={args.dataset}", file=sys.stderr)
    if "grand_average" in result:
        print(
            f"[A-0] grand_avg={result['grand_average']:.4f} "
            f"(threshold={result['gate_threshold']:.2f}, "
            f"published={result['moabb_published']:.2f}, "
            f"delta={result['delta_from_published']:+.4f})",
            file=sys.stderr,
        )
        print(
            f"[A-0] gate_passed={result['gate_passed']}",
            file=sys.stderr,
        )
        return 0 if result["gate_passed"] else 1
    else:
        print(f"[A-0] smoke_test_passed={result['smoke_test_passed']}", file=sys.stderr)
        return 0 if result["smoke_test_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())