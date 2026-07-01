"""
R_JEPA Feature Extraction — thrIVE Phase A-1 Amendment 2
==========================================================

Implements §4.1 second pre-registration amendment: a LeWorldModel-style
end-to-end JEPA (encoder + predictor + SIGReg) trained per-fold on
PhysioNet EEGMMIDB training epochs, with feature extraction via the
frozen encoder + mean-pool + per-fold PCA to d = 8.

This is the HARD ARCHITECTURAL TEST: does sheaf structure (R8+S) beat
a minimal-prior end-to-end JEPA (R_JEPA) on the same data?

Locked architectural choices (cannot be modified post-registration):
  - Encoder: 4-block 1D convolutional, output hidden_dim = 256
  - Predictor: 2-layer MLP, hidden width 512
  - SIGReg: M = 1024 random one-dimensional projections + Henze-Zirkler-
    style normality test against N(0, 1). β = 1.0 weighting parameter
  - Loss: L_total = L_pred + λ_sig * L_sigreg
  - λ_sig = 1.0 (single hyperparameter, locked)
  - Training: AdamW, lr = 1e-3, 50 epochs, batch size 32
  - Per-fold PCA fit on training fold only, applied to test fold
  - Deterministic seeding: torch + numpy both at seed 42

Implementation reference:
  Maes, L., et al. (2026). LeWorldModel: Stable End-to-End Joint-Embedding
  Predictive Architecture from Pixels. arXiv:2603.19312.

Author: Theodore Zuzarte (under direction with Claude, Anthropic)
Licence: MIT
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from scipy.signal import butter, filtfilt, iirnotch
from sklearn.decomposition import PCA


# -----------------------------------------------------------------------------
# Locked hyperparameters (§4.1 second amendment of Phase A revised proposal)
# -----------------------------------------------------------------------------

# Architecture
N_CHANNELS_IN   = 32
N_SAMPLES_IN    = 1000          # 4 s × 250 Hz
HIDDEN_DIM      = 256
PREDICTOR_HIDDEN = 512
RJEPA_TARGET_DIM = 8            # Match R8 / R_FM dimensionality for fair test

# SIGReg
SIGREG_N_PROJECTIONS = 1024
SIGREG_BETA          = 1.0      # Henze-Zirkler weighting
SIGREG_WEIGHT        = 1.0      # λ_sig — the single hyperparameter

# Training
LEARNING_RATE        = 1e-3
WEIGHT_DECAY         = 1e-4
N_TRAIN_EPOCHS       = 50
BATCH_SIZE           = 32

# Preprocessing (must match §4 pipeline + R_FM extraction)
SAMPLING_RATE_HZ        = 250.0
BANDPASS_LOW_HZ         = 0.5
BANDPASS_HIGH_HZ        = 45.0
NOTCH_HZ                = 50.0
NOTCH_Q                 = 30.0
ARTEFACT_THRESHOLD_UV   = 150.0

# Seed
MASTER_SEED = 42


# -----------------------------------------------------------------------------
# Preprocessing — mirror the §4 pipeline (same as R_FM extraction)
# -----------------------------------------------------------------------------

def preprocess_epoch(raw_epoch_uv: np.ndarray) -> np.ndarray:
    """Apply the §4 preprocessing pipeline to a single epoch."""
    nyq = SAMPLING_RATE_HZ / 2.0
    b_bp, a_bp = butter(
        N=4,
        Wn=[BANDPASS_LOW_HZ / nyq, BANDPASS_HIGH_HZ / nyq],
        btype="band",
    )
    filtered = filtfilt(b_bp, a_bp, raw_epoch_uv, axis=1)

    b_n, a_n = iirnotch(w0=NOTCH_HZ / nyq, Q=NOTCH_Q)
    filtered = filtfilt(b_n, a_n, filtered, axis=1)

    threshold_mask = np.abs(filtered) > ARTEFACT_THRESHOLD_UV
    if threshold_mask.any():
        for ch in range(filtered.shape[0]):
            bad = np.where(threshold_mask[ch])[0]
            for idx in bad:
                filtered[ch, idx] = filtered[ch, idx - 1] if idx > 0 else 0.0

    car = filtered - filtered.mean(axis=0, keepdims=True)
    return car.astype(np.float32)


# -----------------------------------------------------------------------------
# JEPA encoder — 4-block 1D conv
# -----------------------------------------------------------------------------

class JEPAEncoder(nn.Module):
    """4-block 1D convolutional encoder for 32-channel EEG epochs.

    Input shape:  (batch, 32 channels, 1000 samples)
    Output shape: (batch, HIDDEN_DIM = 256)
    """
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(N_CHANNELS_IN, 32, kernel_size=15, stride=2, padding=7),
            nn.BatchNorm1d(32),
            nn.GELU(),
            nn.Conv1d(32, 64, kernel_size=15, stride=2, padding=7),
            nn.BatchNorm1d(64),
            nn.GELU(),
            nn.Conv1d(64, 128, kernel_size=15, stride=2, padding=7),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Conv1d(128, 256, kernel_size=15, stride=2, padding=7),
            nn.BatchNorm1d(256),
            nn.GELU(),
        )
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.proj = nn.Linear(256, HIDDEN_DIM)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.conv(x)
        h = self.pool(h).squeeze(-1)
        z = self.proj(h)
        return z


# -----------------------------------------------------------------------------
# JEPA predictor — 2-layer MLP, action-conditioned
# -----------------------------------------------------------------------------

class JEPAPredictor(nn.Module):
    """Action-conditioned predictor: (z_t, action_t) → ẑ_{t+1}.

    For Phase A-1's classification task, action is the trial-class label
    one-hot encoded. In a continuous-control setting (Stage 2), action
    would be the IVE intent state vector.
    """
    def __init__(self, n_action_dims: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(HIDDEN_DIM + n_action_dims, PREDICTOR_HIDDEN),
            nn.GELU(),
            nn.Linear(PREDICTOR_HIDDEN, HIDDEN_DIM),
        )

    def forward(self, z: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        return self.net(torch.cat([z, action], dim=-1))


# -----------------------------------------------------------------------------
# SIGReg — Sketched Isotropic Gaussian Regularization (LeWM)
# -----------------------------------------------------------------------------

def sigreg_loss(z: torch.Tensor, n_projections: int = SIGREG_N_PROJECTIONS,
                beta: float = SIGREG_BETA) -> torch.Tensor:
    """Sketched Isotropic Gaussian Regularization.

    Implements the LeWM regulariser: project the batch latent representations
    onto random unit-norm directions, then test each projection for
    N(0, 1) normality via a Henze-Zirkler-style statistic.

    Parameters
    ----------
    z : (batch, hidden_dim) latent representations
    n_projections : number of random projections (M in LeWM paper)
    beta : Gaussian-weighting parameter for the normality test

    Returns
    -------
    scalar loss — higher when batch distribution deviates from N(0, I)
    """
    batch_size, hidden_dim = z.shape
    device = z.device

    # Sample M random projection directions, normalised to unit sphere
    u = torch.randn(n_projections, hidden_dim, device=device)
    u = u / (u.norm(dim=1, keepdim=True) + 1e-12)

    # Project: y[m, b] = <u[m], z[b]>
    y = z @ u.T  # (batch, n_projections)
    y = y.T  # (n_projections, batch)

    # Standardise each projection (Henze-Zirkler tests against N(0,1))
    # Standardisation prevents trivial scale-related issues
    y_mean = y.mean(dim=1, keepdim=True)
    y_std = y.std(dim=1, keepdim=True) + 1e-6
    y_norm = (y - y_mean) / y_std

    # Henze-Zirkler-style statistic per projection
    # T(y) = Σ_jk exp(-||y_j - y_k||² / (2(1+2β²))) / (n²√(1+2β²))
    #      - 2 Σ_j exp(-||y_j||² / (2(1+β²))) / (n√(1+β²))
    #      + 1 / √(1+2β²)
    # Closed form for the Gaussian-weighted characteristic-function discrepancy

    n = y_norm.shape[1]
    one_plus_2beta_sq = 1.0 + 2 * beta * beta
    one_plus_beta_sq  = 1.0 + beta * beta

    # Pairwise differences within each projection
    diff = y_norm.unsqueeze(2) - y_norm.unsqueeze(1)  # (proj, n, n)
    term1 = torch.exp(-diff**2 / (2 * one_plus_2beta_sq))
    term1 = term1.sum(dim=(1, 2)) / (n * n * math.sqrt(one_plus_2beta_sq))

    term2 = -2.0 * torch.exp(-y_norm**2 / (2 * one_plus_beta_sq))
    term2 = term2.sum(dim=1) / (n * math.sqrt(one_plus_beta_sq))

    term3 = 1.0 / math.sqrt(one_plus_2beta_sq)

    per_projection_stat = term1 + term2 + term3
    # Aggregate over projections — SIGReg averages over the M projections
    return per_projection_stat.mean()


# -----------------------------------------------------------------------------
# Action encoding — class label as one-hot for Phase A-1's classification setting
# -----------------------------------------------------------------------------

def encode_action(labels: np.ndarray, n_classes: int = 2) -> np.ndarray:
    """One-hot encode class labels for the action variable.

    For Phase A-1 motor-imagery (left/right), n_classes = 2. In Stage 2
    this would be the continuous IVE intent state vector.
    """
    n = labels.shape[0]
    onehot = np.zeros((n, n_classes), dtype=np.float32)
    onehot[np.arange(n), labels] = 1.0
    return onehot


# -----------------------------------------------------------------------------
# End-to-end JEPA training on training fold
# -----------------------------------------------------------------------------

def train_jepa(
    train_epochs: np.ndarray,
    train_labels: np.ndarray,
    n_classes: int,
    device: str,
    smoke_test: bool = False,
) -> Tuple[JEPAEncoder, dict]:
    """Train encoder + predictor jointly with MSE + SIGReg.

    Returns the trained (frozen) encoder and a training-history dict.
    """
    # Determinism
    torch.manual_seed(MASTER_SEED)
    np.random.seed(MASTER_SEED)
    if device == "cuda":
        torch.cuda.manual_seed_all(MASTER_SEED)

    # Preprocess all training epochs
    train_pp = np.stack([preprocess_epoch(e) for e in train_epochs])
    train_actions = encode_action(train_labels, n_classes)

    # Pair adjacent epochs as (t, t+1) for next-embedding prediction
    # Trial order within the training fold defines temporal succession
    n_train = train_pp.shape[0]
    if n_train < 2:
        raise ValueError(f"Need at least 2 training epochs; got {n_train}")
    x_t = torch.from_numpy(train_pp[:-1])
    x_t1 = torch.from_numpy(train_pp[1:])
    a_t = torch.from_numpy(train_actions[:-1])

    dataset = TensorDataset(x_t, a_t, x_t1)
    loader = DataLoader(
        dataset, batch_size=BATCH_SIZE, shuffle=True,
        generator=torch.Generator().manual_seed(MASTER_SEED),
    )

    encoder = JEPAEncoder().to(device)
    predictor = JEPAPredictor(n_action_dims=n_classes).to(device)
    params = list(encoder.parameters()) + list(predictor.parameters())
    optimiser = torch.optim.AdamW(params, lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    n_epochs = 3 if smoke_test else N_TRAIN_EPOCHS
    history = {"loss_pred": [], "loss_sigreg": [], "loss_total": []}

    encoder.train(); predictor.train()
    for epoch in range(n_epochs):
        epoch_pred = []; epoch_sigreg = []; epoch_total = []
        for batch_x, batch_a, batch_x1 in loader:
            batch_x = batch_x.to(device); batch_a = batch_a.to(device); batch_x1 = batch_x1.to(device)
            z_t = encoder(batch_x)
            z_t1_target = encoder(batch_x1).detach()  # No grad through target encoder
            z_t1_pred = predictor(z_t, batch_a)

            # Loss 1: MSE next-embedding prediction
            loss_pred = ((z_t1_pred - z_t1_target) ** 2).mean()

            # Loss 2: SIGReg on current-step latents
            loss_sigreg = sigreg_loss(z_t)

            loss_total = loss_pred + SIGREG_WEIGHT * loss_sigreg

            optimiser.zero_grad()
            loss_total.backward()
            optimiser.step()

            epoch_pred.append(loss_pred.item())
            epoch_sigreg.append(loss_sigreg.item())
            epoch_total.append(loss_total.item())

        history["loss_pred"].append(float(np.mean(epoch_pred)))
        history["loss_sigreg"].append(float(np.mean(epoch_sigreg)))
        history["loss_total"].append(float(np.mean(epoch_total)))
        if (epoch + 1) % 10 == 0 or epoch == n_epochs - 1:
            print(
                f"  Epoch {epoch+1}/{n_epochs}: "
                f"pred={history['loss_pred'][-1]:.4f} "
                f"sigreg={history['loss_sigreg'][-1]:.4f}",
                file=sys.stderr,
            )

    encoder.eval()
    return encoder, history


# -----------------------------------------------------------------------------
# Feature extraction via frozen encoder + PCA to d = 8
# -----------------------------------------------------------------------------

def extract_features(
    encoder: JEPAEncoder, epochs: np.ndarray, device: str,
) -> np.ndarray:
    """Apply the frozen encoder to epochs and return HIDDEN_DIM-dim latents."""
    pp = np.stack([preprocess_epoch(e) for e in epochs])
    x = torch.from_numpy(pp).to(device)
    encoder.eval()
    with torch.no_grad():
        z = encoder(x)
    return z.cpu().numpy()


def fit_pca_on_training_fold(train_latents: np.ndarray) -> PCA:
    """Fit PCA on training-fold latents only (§9.4 per-fold discipline)."""
    pca = PCA(n_components=RJEPA_TARGET_DIM, random_state=MASTER_SEED)
    pca.fit(train_latents)
    return pca


# -----------------------------------------------------------------------------
# Top-level orchestration
# -----------------------------------------------------------------------------

def extract_rjepa_for_fold(
    train_epochs_raw: np.ndarray,
    train_labels: np.ndarray,
    test_epochs_raw: np.ndarray,
    n_classes: int = 2,
    device: str = "cpu",
    smoke_test: bool = False,
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """Run the full LeWM-style end-to-end training + extraction for one fold.

    Returns
    -------
    rjepa_train : (n_train, 8) training-fold R_JEPA features
    rjepa_test  : (n_test, 8) test-fold R_JEPA features
    provenance  : dict for the manifest
    """
    encoder, history = train_jepa(
        train_epochs_raw, train_labels, n_classes, device, smoke_test,
    )

    train_latents = extract_features(encoder, train_epochs_raw, device)
    test_latents  = extract_features(encoder, test_epochs_raw, device)

    pca = fit_pca_on_training_fold(train_latents)
    rjepa_train = pca.transform(train_latents)
    rjepa_test  = pca.transform(test_latents)

    provenance = {
        "architecture":      "LeWM-style end-to-end JEPA",
        "encoder_class":     "JEPAEncoder (4-block 1D conv, hidden=256)",
        "predictor_class":   "JEPAPredictor (2-layer MLP, hidden=512)",
        "sigreg_n_projections": SIGREG_N_PROJECTIONS,
        "sigreg_beta":       SIGREG_BETA,
        "sigreg_weight":     SIGREG_WEIGHT,
        "learning_rate":     LEARNING_RATE,
        "weight_decay":      WEIGHT_DECAY,
        "n_train_epochs":    int(train_epochs_raw.shape[0]),
        "n_test_epochs":     int(test_epochs_raw.shape[0]),
        "training_iters":    len(history["loss_pred"]),
        "final_loss_pred":   history["loss_pred"][-1],
        "final_loss_sigreg": history["loss_sigreg"][-1],
        "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "git_commit":        _git_commit_hash(),
        "script_sha256":     _script_sha256(__file__),
        "torch_version":     torch.__version__,
        "numpy_version":     np.__version__,
        "deterministic":     True,
        "seed":              MASTER_SEED,
        "smoke_test":        bool(smoke_test),
    }
    return rjepa_train, rjepa_test, provenance


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
        description="R_JEPA feature extraction (Phase A-1 Amendment 2)"
    )
    parser.add_argument("--subject",      required=True, help="Subject ID")
    parser.add_argument("--fold",         required=True, type=int, help="Fold index")
    parser.add_argument("--train-epochs", required=True, type=Path)
    parser.add_argument("--train-labels", required=True, type=Path)
    parser.add_argument("--test-epochs",  required=True, type=Path)
    parser.add_argument("--output",       required=True, type=Path)
    parser.add_argument("--manifest",     required=True, type=Path)
    parser.add_argument("--n-classes",    type=int, default=2)
    parser.add_argument("--device",       choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--smoke-test",   action="store_true")
    args = parser.parse_args(argv)

    train_raw = np.load(args.train_epochs)
    train_lbl = np.load(args.train_labels)
    test_raw  = np.load(args.test_epochs)

    rjepa_train, rjepa_test, provenance = extract_rjepa_for_fold(
        train_raw, train_lbl, test_raw, args.n_classes, args.device, args.smoke_test,
    )

    np.savez_compressed(
        args.output,
        rjepa_train=rjepa_train,
        rjepa_test=rjepa_test,
    )

    provenance.update({
        "subject":      args.subject,
        "fold":         args.fold,
        "input_train":  str(args.train_epochs),
        "input_labels": str(args.train_labels),
        "input_test":   str(args.test_epochs),
        "output":       str(args.output),
        "device":       args.device,
        "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
    })
    args.manifest.write_text(json.dumps(provenance, indent=2))

    print(f"OK: wrote {args.output} and {args.manifest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())