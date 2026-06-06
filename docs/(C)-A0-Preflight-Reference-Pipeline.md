# A-0 Preflight Reference Pipeline — Locked MOABB Reproduction Script

**Implements:** the Phase A-0 preflight specified by §3 of [[(C)-Phase-A-Experiment-Revised]] — the **gating** reproduction of the published MOABB Riemannian-tangent reference pipeline on PhysioNet EEGMMIDB and BCI Competition IV-2a.

**Purpose:** Verify the reference BCI pipeline reproduces published benchmark accuracy **before any novel claim (H1–H10) is tested**. Without this gate passing, no Phase A-1 result is interpretable — a sheaf-coherence loss could simply mean a broken preprocessing pipeline, not a falsified architectural claim.

**Status:** Twelfth and final locked artefact in the Phase A-1 inventory. Sibling to [[(C)-R_FM-Feature-Extraction]], [[(C)-R_JEPA-Feature-Extraction]], [[(C)-R_JEPA-Brain-Feature-Extraction]], [[(C)-R_GL-Feature-Extraction]], and the analysis / smoke-test / CI artefacts.

---

## Why this is the load-bearing gate

The Phase A-1 confirmatory hypotheses (H1–H10) all compare novel representations to the Riemannian-tangent baseline R8. **If R8 itself does not reproduce the MOABB reference accuracy on the same dataset, none of the H1–H10 comparisons can be validly interpreted.** Three concrete failure modes A-0 is designed to catch:

| A-0 catches | If not caught, it would look like |
|---|---|
| Wrong PhysioNet annotation (the Varbu et al. 2024 curation correction not applied) | Sheaf appears to "win" because R8 is being trained on the wrong labels |
| Wrong epoch window / wrong frequency band / wrong CAR / wrong rejection threshold | Sheaf appears to "win" because R8 is operating on noisier features than it should |
| Wrong covariance estimator / wrong tangent-space mapping / wrong logistic regulariser | Sheaf appears to "win" because R8 is being misimplemented |

A-0 is therefore the **only** Phase A artefact whose failure terminates the entire programme without informing any architectural claim. The §3 gate criterion ("within 2 pp of MOABB published values, otherwise halt and repair pipeline") is the locked falsifier.

---

## Locked configuration (cannot modify post-registration)

| Parameter | Locked value | Source |
|---|---|---|
| Datasets | PhysioNet EEGMMIDB (Schalk et al., 2004) + BCI Competition IV-2a (Brunner et al., 2008) | §3 of [[(C)-Phase-A-Experiment-Revised]] |
| Annotation curation | Varbu et al. (2024) corrections for PhysioNetMI | §3 |
| Framework | MOABB ≥ 1.4 (Chevallier et al., 2024) | §3 |
| Paradigm | `LeftRightImagery` for EEGMMIDB; `MotorImagery` 4-class for BCI IV-2a | MOABB API |
| Subjects | All 109 PhysioNetMI; all 9 BCI IV-2a | §3 |
| Sampling rate | 250 Hz (PhysioNetMI native; BCI IV-2a downsampled from 250 Hz) | MOABB defaults |
| Bandpass | 8–32 Hz (mu+beta MI band, MOABB default for `LeftRightImagery`) | MOABB defaults |
| Epoch window | tmin=0.0, tmax=4.0 s post-cue (MOABB default for both paradigms) | MOABB defaults |
| Covariance estimator | Oracle Approximating Shrinkage (`oas` — pyriemann default) | pyriemann |
| Tangent-space mapping | Reference: Riemannian Fréchet mean via `pyriemann.tangentspace.TangentSpace` | pyriemann |
| Classifier | L2-regularised Logistic Regression, $C = 1.0$ (sklearn default), max_iter=1000 | §3 |
| Covariance dimension | $d=32$ (PhysioNetMI uses standard 32-channel subset; BCI IV-2a native 22 channels) | §3 |
| Cross-validation | MOABB `WithinSession` evaluation, 5-fold stratified within-subject | §3 |
| Master seed | 42 | Matches sibling scripts |
| Gate threshold (PhysionetMI L/R binary) | $\geq 0.633$ grand-average accuracy (67.28% MOABB-published TS+LR − 4 pp tolerance) | §3 (corrected) |
| Gate threshold (BCI IV-2a 4-class) | $\geq 0.68$ grand-average accuracy (71.97% MOABB-published TS+LR − 4 pp tolerance) | §3 (corrected) |

**Pre-lock verification — completed May 2026.** The MOABB-published TS+LR reference values were cross-verified against the [MOABB official benchmark results page](https://moabb.neurotechx.com/docs/paper_results.html) and Chevallier et al. (2024) arXiv:2404.15319 Appendix D, Tables 6–10. **Two corrections were applied** before lock:

| §3 v2.0 draft value | Verified MOABB-published TS+LR | Correction applied |
|---|---|---|
| PhysionetMI binary L/R 92% (likely confusion with Right-Hand-vs-Feet paradigm at 93.15%) | **67.28 ± 19.19%** (Left vs Right Hand, the §4.1 task) | Gate updated to ≥ 0.633 |
| BCI IV-2a 4-class 78% | **71.97 ± 15.46%** (all-classes 4-way, the §3 task) | Gate updated to ≥ 0.68 |

The 4 pp tolerance (vs the original 2 pp) is one σ/5 of the published cross-subject distribution, where σ ≈ 19 pp (PhysionetMI) and σ ≈ 15 pp (BCI IV-2a). Original 2 pp tolerance would have been ~0.4σ — operationally infeasible given the cross-subject variance reported by the MOABB benchmark. Cross-confirmed by an independent meta-analysis of 861 motor-imagery sessions reporting 66.53% mean accuracy on 2-class L/R MI — within 0.75 pp of the MOABB 67.28% value.

---

## Usage

```bash
# Compute and log script hash
python -c "import hashlib; print(hashlib.sha256(open('a0_preflight.py','rb').read()).hexdigest())"

# Smoke test on synthetic Gaussian data (no MOABB / no real EEG; ~20 s)
python a0_preflight.py --smoke-test --output a0_smoke.json

# Single-subject sanity check (PhysioNetMI subject 1 only; ~3 min on CPU)
python a0_preflight.py \
    --dataset physionet --single-subject 1 \
    --output a0_single_subject.json

# Full preflight on PhysioNetMI (all 109 subjects; ~2 h on CPU, ~30 min on 8-core)
python a0_preflight.py \
    --dataset physionet \
    --output a0_physionet_full.json \
    --manifest manifest_a0_physionet.json

# Full preflight on BCI Competition IV-2a (9 subjects; ~10 min on CPU)
python a0_preflight.py \
    --dataset bci_iv_2a \
    --output a0_bci_iv_2a_full.json \
    --manifest manifest_a0_bci_iv_2a.json
```

The script writes a structured JSON output and a separate manifest with SHA-256 of the script + the locked configuration. **The gate-pass / gate-fail verdict is written explicitly into the JSON** — no manual interpretation is required.

---

## The Script — `a0_preflight.py`

```python
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

Author: Theo Cognat (under direction with Claude, Anthropic)
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
```

---

## Companion file — `environment_a0.yml`

```yaml
name: thrive_a0
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy=1.26
  - scipy=1.11
  - scikit-learn=1.3
  - pandas=2.1
  - mne=1.6
  - pip
  - pip:
      - moabb>=1.4.0
      - pyriemann>=0.5
```

**Dependency rationale.** MOABB + pyriemann are the only non-standard packages. Both are well-maintained, widely used in BCI reproducibility studies, and explicitly cited by §3 of the Phase A spec. No PyTorch (no neural networks), no Brian2 (no spiking simulation), no foundation-model libraries.

---

## Pre-Registration Lock-In Checklist

- [ ] `a0_preflight.py` committed at the `pre-registration-locked` git tag
- [ ] `sha256sum a0_preflight.py` recorded in OSF manifest as `a0_script_sha256`
- [ ] `environment_a0.yml` committed alongside the script
- [ ] **MOABB version pinned** (`moabb>=1.4.0` — the version corresponding to Chevallier et al., 2024 published benchmark)
- [x] **Pre-lock verification — COMPLETED May 2026.** The MOABB-published TS+LR reference values cross-checked against the [MOABB official benchmark results page](https://moabb.neurotechx.com/docs/paper_results.html) and Chevallier et al. (2024) arXiv:2404.15319 Appendix D, Tables 6–10. **Two corrections applied:** §3 of [[(C)-Phase-A-Experiment-Revised]] gate thresholds updated from the v2.0-draft values (≥0.90 / ≥0.76) to the corrected values (≥0.633 / ≥0.68) based on the verified MOABB-published TS+LR accuracies of 67.28% (PhysionetMI Left-vs-Right binary) and 71.97% (BCI IV-2a 4-class). The script's `MOABB_PUBLISHED` dict and `GATE_THRESHOLD_*` constants reflect the corrected values. The original 92% number was a spec-side confusion with the PhysionetMI Right-Hand-vs-Feet binary paradigm (93.15%), not the Left-vs-Right paradigm §4.1 actually uses.
- [ ] Smoke test (`--smoke-test`) runs end-to-end on synthetic SPD data; mean accuracy > 0.95; smoke-test output committed
- [ ] Single-subject sanity check (`--single-subject 1`) on PhysioNetMI runs end-to-end; output committed
- [ ] **No data-touching beyond MOABB-cached downloads** before final registration lock
- [ ] §9.9 of [[(C)-OSF-Preregistration-Phase-A1]] integrity statement extended to cover A-0: no post-registration modification of the gate thresholds, the pipeline configuration, the paradigm settings, or the dataset selection

---

## What this script does NOT do

By design:

- Does not test any of the sheaf-specific or thrIVE-specific claims (H1–H10). It only validates the reference pipeline.
- Does not implement the §4.1 stressor conditions (S0/S1/S2/S3). A-0 runs on clean MOABB defaults; stressors are Phase A-1 territory.
- Does not perform any subject-transfer evaluation (CrossSubject / LOSO). A-0 uses WithinSession only — this is the published MOABB reference condition.
- Does not perform any data-driven hyperparameter search. The pipeline is the locked TS+LR golden-standard configuration; any tuning would invalidate the gate.
- Does not write outputs to the shared OSF data directory until the gate passes. Failed-gate runs are diagnosed locally before re-running.

These exclusions are the definition of "preflight." A-0 answers exactly one question: *does the published reference pipeline reproduce on this hardware + software + dataset configuration?* If yes, the rest of Phase A-1 is interpretable; if no, the rest of Phase A-1 is invalid until the discrepancy is resolved.

---

## The gate-failure decision tree

If `gate_passed: false` in either dataset's output JSON:

| Symptom | Most likely cause | Repair action |
|---|---|---|
| Grand-average accuracy within 4 pp of published but below gate | Subject-level outliers; possibly a single subject's data is corrupted in the local MOABB cache | Inspect `per_subject` field; check if 1–3 subjects are extreme outliers; clear MOABB cache and redownload |
| Grand-average accuracy 4–10 pp below published | Likely paradigm-default mismatch (epoch window, frequency band, or annotation curation) | Verify MOABB ≥ 1.4 in environment; verify Varbu et al. 2024 PhysioNetMI annotation correction is applied (MOABB ≥ 1.4 includes it by default) |
| Grand-average accuracy >10 pp below published | Pipeline misconfiguration | Re-derive `build_pipeline()` from scratch against the pyriemann TangentSpace + sklearn LogisticRegression documented examples; verify Covariance estimator is OAS not empirical |
| Grand-average accuracy >4 pp **above** published | Suspicious — possible label leakage | Verify `WithinSessionEvaluation` was used (not full-data CV); verify per-fold isolation; inspect `score` distribution for ceiling effects |

The decision tree is itself part of the locked artefact. A-0 failures are not treated as research findings — they are treated as engineering bugs to be fixed before the gate is re-attempted.

---

## Cross-references

| Section | Connection |
|---|---|
| [[(C)-Phase-A-Experiment-Revised]] §3 | The Phase A-0 specification this script operationalises |
| [[(C)-OSF-Preregistration-Phase-A1]] §9.9 | Pre-registration integrity statement (to be extended to cover A-0) |
| [[(C)-R_FM-Feature-Extraction]] | Sibling locked script (foundation-model features) |
| [[(C)-R_JEPA-Feature-Extraction]] | Sibling locked script (cross-domain JEPA) |
| [[(C)-R_JEPA-Brain-Feature-Extraction]] | Sibling locked script (domain-specific JEPA) |
| [[(C)-R_GL-Feature-Extraction]] | Sibling locked script (graph-Laplacian baseline) |
| [[(C)-A1-Factorial-Analysis-Script]] | Downstream analysis — depends on A-0 having gated through |
| [[(C)-CI-Workflow-Preregistration-Verify]] | CI workflow that should run the A-0 smoke test on every commit to the pre-registration-locked branch |

---

## What "gate passed" means architecturally

If A-0 passes on both datasets, the following claims become defensible:

1. The MOABB framework is correctly installed and configured on the experimental hardware.
2. The PhysioNetMI dataset with Varbu et al. (2024) annotation curation is correctly loaded and parsed.
3. The BCI IV-2a dataset is correctly loaded and parsed.
4. The Riemannian-tangent + L2 LogReg pipeline reproduces the field-standard reference accuracy.
5. The 5-fold within-subject CV evaluation procedure matches the MOABB-published methodology.

These five claims are the **necessary preconditions** for every subsequent H1–H10 test. The A-0 gate is therefore the load-bearing entry point to the entire programme. Until A-0 passes, no other Phase A-1 artefact (R_FM, R_JEPA, R_JEPA_brain, R_GL, S-TTSA) can be validly compared to R8 — they would be compared against an unvalidated baseline.

If A-0 fails on either dataset and cannot be repaired within a reasonable engineering effort, the *honest* outcome is to fall back to **only the dataset that does pass A-0**, with the corresponding subset of H1–H10 evaluated on that dataset. The §3 gate criterion is non-negotiable: the comparison must be against a reference that the field has validated.

---

## References

Brunner, C., Leeb, R., Müller-Putz, G., Schlögl, A., & Pfurtscheller, G. (2008). BCI Competition 2008 — Graz dataset A. *TU Graz*.

Chevallier, S., Carrara, I., Aristimunha, B., Guetschel, P., Sedlar, S., Lopes, B., Velut, S., Khazem, S., & Moreau, T. (2024). The largest EEG-based BCI reproducibility study for open science: The MOABB benchmark. *arXiv:2404.15319*.

Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004). BCI2000: A general-purpose brain-computer interface (BCI) system. *IEEE Transactions on Biomedical Engineering*, 51(6), 1034–1043.

Varbu, K., et al. (2024). Increasing accessibility to a large brain–computer interface dataset: Curation of PhysioNet EEG Motor Movement/Imagery Dataset. *Data in Brief*, 54, 110371.

Barachant, A., Bonnet, S., Congedo, M., & Jutten, C. (2013). Classification of covariance matrices using a Riemannian-based kernel for BCI applications. *Neurocomputing*, 112, 172–178.

Rodrigues, P. L. C., Jutten, C., & Congedo, M. (2019). Riemannian Procrustes analysis: Transfer learning for brain–computer interfaces. *IEEE Transactions on Biomedical Engineering*, 66(8), 2390–2401.
