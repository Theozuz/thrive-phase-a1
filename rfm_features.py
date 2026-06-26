"""
R_FM Feature Extraction — thrIVE Phase A-1 Amendment 1
========================================================

Implements §9.4 of the OSF pre-registration: the six-step deterministic
procedure for extracting d=8 features from a frozen EEG foundation model.

Six-step procedure (verbatim from pre-registration §9.4):
  1. Preprocess via the §4 pipeline (bandpass + notch + reject + CAR)
  2. Pass through frozen foundation model (no fine-tuning, no adaptation)
  3. Extract last-hidden-layer output (time_steps, hidden_dim)
  4. Mean-pool over the time axis
  5. PCA-project to d=8 using *training-fold-only* projection matrix
  6. Return R_FM = 8-dimensional vector per epoch

Locked invariants:
  - Frozen model (no gradient, no fine-tuning)
  - PCA fit on training fold only; never refit on test fold
  - Deterministic: torch.use_deterministic_algorithms(True)
  - Model checkpoint MD5 verified against registered hash before use

Author: Theodore Zuzarte (under direction with Claude, Anthropic)
Licence: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import torch
from scipy.signal import butter, filtfilt, iirnotch
from sklearn.decomposition import PCA

# -----------------------------------------------------------------------------
# §9.3 Locked model specification
# -----------------------------------------------------------------------------
# Primary model: LCM (Wang et al., 2025, arXiv:2502.17464)
# Fallback model: EEGFormer (Jiang et al., 2024, arXiv:2401.10278)
#
# URLs and MD5 hashes are filled in at OSF registration time.
# REPLACE_AT_REGISTRATION_TIME placeholders MUST be replaced before commit.
# The PI is responsible for verifying the downloaded checkpoint's MD5
# matches the value logged at registration.
#
# If neither LCM nor EEGFormer checkpoints are available at execution time,
# the script EXITS WITH AN ERROR rather than substituting a third model.
# This enforces §9.3 "no post-hoc substitution" discipline.
# -----------------------------------------------------------------------------

MODEL_REGISTRY = {
    "lcm": {
        "name":     "Large Cognition Model",
        "paper":    "Wang et al. (2025), arXiv:2502.17464",
        "url":      "REPLACE_AT_REGISTRATION_TIME",  # paper GitHub release URL
        "md5":      "REPLACE_AT_REGISTRATION_TIME",  # 32-char hex
        "hidden_dim":      256,
        "input_samples":  1000,  # 4 s @ 250 Hz
        "input_channels":   64,
    },
    "eegformer": {
        "name":     "EEGFormer",
        "paper":    "Jiang et al. (2024), arXiv:2401.10278",
        "url":      "REPLACE_AT_REGISTRATION_TIME",
        "md5":      "REPLACE_AT_REGISTRATION_TIME",
        "hidden_dim":      192,
        "input_samples":  1000,
        "input_channels":   64,
    },
}

# -----------------------------------------------------------------------------
# §9.4 Step 1 — Preprocessing pipeline (mirror the §4 pipeline)
# -----------------------------------------------------------------------------

SAMPLING_RATE_HZ = 250.0
BANDPASS_LOW_HZ  = 0.5
BANDPASS_HIGH_HZ = 45.0
NOTCH_HZ         = 50.0  # mains; use 60.0 for North-America datasets
NOTCH_Q          = 30.0
ARTEFACT_THRESHOLD_UV = 150.0


def preprocess_epoch(raw_epoch_uv: np.ndarray) -> np.ndarray:
    """Apply the §4 preprocessing pipeline to a single epoch.

    Parameters
    ----------
    raw_epoch_uv : (n_channels, n_samples) array in microvolts.

    Returns
    -------
    (n_channels, n_samples) preprocessed array.
    """
    # 1a. Bandpass filter (4th-order Butterworth, zero-phase)
    nyq = SAMPLING_RATE_HZ / 2.0
    b_bp, a_bp = butter(
        N=4,
        Wn=[BANDPASS_LOW_HZ / nyq, BANDPASS_HIGH_HZ / nyq],
        btype="band",
    )
    filtered = filtfilt(b_bp, a_bp, raw_epoch_uv, axis=1)

    # 1b. Notch filter at mains
    b_n, a_n = iirnotch(w0=NOTCH_HZ / nyq, Q=NOTCH_Q)
    filtered = filtfilt(b_n, a_n, filtered, axis=1)

    # 1c. Artefact rejection — clamp >150 µV samples to previous valid
    threshold_mask = np.abs(filtered) > ARTEFACT_THRESHOLD_UV
    if threshold_mask.any():
        for ch in range(filtered.shape[0]):
            bad = np.where(threshold_mask[ch])[0]
            for idx in bad:
                # Use the previous in-bounds sample (or 0 at the start)
                filtered[ch, idx] = filtered[ch, idx - 1] if idx > 0 else 0.0

    # 1d. Common average referencing
    car = filtered - filtered.mean(axis=0, keepdims=True)

    return car.astype(np.float32)


# -----------------------------------------------------------------------------
# §9.4 Step 2 — Frozen foundation model forward pass
# -----------------------------------------------------------------------------

@dataclass
class ModelSpec:
    name:   str
    paper:  str
    url:    str
    md5:    str
    hidden_dim: int
    input_samples: int
    input_channels: int


def verify_md5(path: Path, expected_md5: str) -> bool:
    """Verify the MD5 hash of a downloaded checkpoint matches the registered value."""
    if expected_md5 == "REPLACE_AT_REGISTRATION_TIME":
        sys.exit("ERROR: model MD5 not registered. Replace placeholder before use.")
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest() == expected_md5


def load_frozen_model(model_key: str, checkpoint_dir: Path) -> Tuple[torch.nn.Module, ModelSpec]:
    """Load the named foundation model in frozen eval mode.

    Implements §9.3 fallback logic:
      - Primary: LCM
      - Fallback: EEGFormer
      - No third model is substituted.
    """
    if model_key not in MODEL_REGISTRY:
        sys.exit(
            f"ERROR: unknown model '{model_key}'. "
            f"Per §9.3 no third model may be substituted. "
            f"Valid keys: {list(MODEL_REGISTRY.keys())}"
        )

    spec = ModelSpec(**MODEL_REGISTRY[model_key])
    ckpt_path = checkpoint_dir / f"{model_key}.pt"

    if not ckpt_path.exists():
        sys.exit(
            f"ERROR: checkpoint not found at {ckpt_path}. "
            f"Download from {spec.url} and place at this path. "
            f"Per §9.3, if neither LCM nor EEGFormer is available, "
            f"drop R_FM from the analysis — do NOT substitute another model."
        )

    if not verify_md5(ckpt_path, spec.md5):
        sys.exit(
            f"ERROR: MD5 mismatch for {model_key} checkpoint. "
            f"Expected {spec.md5}; checkpoint may be modified or corrupted. "
            f"Refusing to proceed."
        )

    # Load and freeze. The exact import path depends on the publishing
    # repository; here we use torch.load on a state_dict and assume the
    # model class is importable. PI must edit the import below to match
    # the released checkpoint format.
    state_dict = torch.load(ckpt_path, map_location="cpu", weights_only=True)
    # PLACEHOLDER: load the model class from the upstream repository.
    # e.g.   from lcm.model import LargeCognitionModel
    #        model = LargeCognitionModel(...); model.load_state_dict(state_dict)
    raise NotImplementedError(
        "PI must replace this stub with the actual model class import "
        "from the upstream foundation-model repository, locked at "
        "registration time. The replacement is mechanical (instantiate "
        "the published model class and load_state_dict) and does not "
        "introduce post-hoc analytical choices."
    )


def extract_hidden_states(
    model: torch.nn.Module,
    epoch_preprocessed: np.ndarray,
    spec: ModelSpec,
) -> np.ndarray:
    """§9.4 Steps 2-3: forward pass through frozen model, extract last hidden layer.

    Returns
    -------
    (time_steps, hidden_dim) numpy array.
    """
    assert epoch_preprocessed.shape == (spec.input_channels, spec.input_samples), (
        f"Epoch shape {epoch_preprocessed.shape} does not match "
        f"expected ({spec.input_channels}, {spec.input_samples})"
    )

    model.eval()
    x = torch.from_numpy(epoch_preprocessed).unsqueeze(0)  # (1, C, T)
    with torch.no_grad():
        # PLACEHOLDER: the actual call depends on the model's forward signature.
        # The contract is: return the final hidden-layer activations BEFORE
        # any task-specific classification head, with shape (1, T', hidden_dim).
        hidden = model.encode_hidden(x)  # PI implements per upstream model
    return hidden.squeeze(0).cpu().numpy()


# -----------------------------------------------------------------------------
# §9.4 Step 4 — Time-axis mean pool
# -----------------------------------------------------------------------------

def mean_pool_time(hidden_states: np.ndarray) -> np.ndarray:
    """Mean over the time axis. Returns (hidden_dim,) vector."""
    assert hidden_states.ndim == 2, "Expected (time_steps, hidden_dim)"
    return hidden_states.mean(axis=0)


# -----------------------------------------------------------------------------
# §9.4 Step 5 — Per-fold PCA projection to d=8
# -----------------------------------------------------------------------------

RFM_TARGET_DIM = 8


def fit_pca_on_training_fold(train_hidden_pooled: np.ndarray) -> PCA:
    """Fit PCA on training-fold epochs ONLY.

    Per §9.4, the PCA projection matrix is computed per-subject on training-fold
    epochs only and applied to test-fold epochs — never the reverse. This
    prevents test-fold leakage that would inflate R_FM apparent accuracy.

    Parameters
    ----------
    train_hidden_pooled : (n_train_epochs, hidden_dim) array.
    """
    assert train_hidden_pooled.ndim == 2
    assert train_hidden_pooled.shape[1] >= RFM_TARGET_DIM, (
        f"hidden_dim ({train_hidden_pooled.shape[1]}) must be >= "
        f"RFM_TARGET_DIM ({RFM_TARGET_DIM})"
    )

    pca = PCA(n_components=RFM_TARGET_DIM, random_state=42)
    pca.fit(train_hidden_pooled)
    return pca


def project_to_rfm(pca: PCA, hidden_pooled: np.ndarray) -> np.ndarray:
    """Apply the training-fold PCA projection to (any) hidden_pooled epochs."""
    return pca.transform(hidden_pooled)


# -----------------------------------------------------------------------------
# Top-level orchestration
# -----------------------------------------------------------------------------

def extract_rfm_for_fold(
    train_epochs_raw: np.ndarray,
    test_epochs_raw:  np.ndarray,
    model_key: str,
    checkpoint_dir: Path,
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """Run the full six-step procedure for one (subject, fold) pair.

    Parameters
    ----------
    train_epochs_raw : (n_train, n_channels, n_samples) raw EEG in µV
    test_epochs_raw  : (n_test,  n_channels, n_samples) raw EEG in µV
    model_key        : 'lcm' or 'eegformer'
    checkpoint_dir   : directory containing locked checkpoints

    Returns
    -------
    rfm_train : (n_train, 8) array of R_FM features for the training fold
    rfm_test  : (n_test,  8) array of R_FM features for the test fold
    provenance: dict containing all hashes and configuration for the manifest
    """
    # Determinism
    np.random.seed(42)
    torch.manual_seed(42)
    torch.use_deterministic_algorithms(True, warn_only=False)

    model, spec = load_frozen_model(model_key, checkpoint_dir)

    # Step 1: preprocess
    train_pp = np.stack([preprocess_epoch(e) for e in train_epochs_raw])
    test_pp  = np.stack([preprocess_epoch(e) for e in test_epochs_raw])

    # Steps 2-4: forward + extract + pool
    train_hidden = np.stack([
        mean_pool_time(extract_hidden_states(model, e, spec))
        for e in train_pp
    ])
    test_hidden  = np.stack([
        mean_pool_time(extract_hidden_states(model, e, spec))
        for e in test_pp
    ])

    # Step 5: PCA on training fold only
    pca = fit_pca_on_training_fold(train_hidden)

    # Step 6: project both folds with the training-fold PCA
    rfm_train = project_to_rfm(pca, train_hidden)
    rfm_test  = project_to_rfm(pca, test_hidden)

    # Provenance
    provenance = {
        "model_key":       model_key,
        "model_name":      spec.name,
        "model_paper":     spec.paper,
        "model_md5":       spec.md5,
        "rfm_target_dim":  RFM_TARGET_DIM,
        "n_train_epochs":  int(train_epochs_raw.shape[0]),
        "n_test_epochs":   int(test_epochs_raw.shape[0]),
        "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "git_commit":      _git_commit_hash(),
        "script_sha256":   _script_sha256(__file__),
        "torch_version":   torch.__version__,
        "numpy_version":   np.__version__,
        "deterministic":   True,
        "seed":            42,
    }
    return rfm_train, rfm_test, provenance


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
        description="R_FM feature extraction (Phase A-1 Amendment 1)"
    )
    parser.add_argument("--subject",      required=True, help="Subject ID")
    parser.add_argument("--fold",         required=True, type=int, help="Fold index")
    parser.add_argument("--train-epochs", required=True, type=Path)
    parser.add_argument("--test-epochs",  required=True, type=Path)
    parser.add_argument("--output",       required=True, type=Path)
    parser.add_argument("--manifest",     required=True, type=Path)
    parser.add_argument("--model",        choices=["lcm", "eegformer"], default="lcm")
    parser.add_argument(
        "--checkpoint-dir",
        type=Path,
        default=Path(os.environ.get("THRIVE_CKPT_DIR", "checkpoints/")),
    )
    args = parser.parse_args(argv)

    train_raw = np.load(args.train_epochs)
    test_raw  = np.load(args.test_epochs)

    rfm_train, rfm_test, provenance = extract_rfm_for_fold(
        train_raw, test_raw, args.model, args.checkpoint_dir
    )

    np.savez_compressed(
        args.output,
        rfm_train=rfm_train,
        rfm_test=rfm_test,
    )

    provenance.update({
        "subject":     args.subject,
        "fold":        args.fold,
        "input_train": str(args.train_epochs),
        "input_test":  str(args.test_epochs),
        "output":      str(args.output),
    })
    args.manifest.write_text(json.dumps(provenance, indent=2))

    print(f"OK: wrote {args.output} and {args.manifest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())