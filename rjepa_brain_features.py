"""
R_JEPA_brain Feature Extraction — Amendment 4 to Phase A-1
============================================================

Brain-JEPA / Signal-JEPA-inspired end-to-end JEPA tailored to EEG with
spatial (channel-wise) masking and pre-local (per-channel-group)
processing before global pooling.

The architectural principles are taken from:
  - Brain-JEPA (Yi et al., 2024) — domain-specific positional encoding + masking
  - Signal-JEPA (Guetschel et al., 2024) — spatial filtering and pre-local
                                          architectures crucial for downstream
  - LeWorldModel (Maes et al., 2026) — SIGReg collapse prevention

Locked architectural choices (cannot be modified post-registration):
  - Spatial-first encoder: per-channel-group (8 groups of 8 channels) attention
  - Spatial / channel-wise masking: 25% of channel groups masked per training step
  - Pre-local block: 2-layer transformer per channel group, dim=64
  - Global aggregation: cross-group attention with learnable [GLOBAL] token
  - Predictor: 2-layer MLP, hidden=512 (matched to R_JEPA for fair comparison)
  - SIGReg: M=1024 projections, β=1.0, λ_sig=1.0 (matched to R_JEPA)
  - Training: AdamW lr=1e-3, wd=1e-4, 50 epochs, batch 32
  - Per-fold PCA to d=8 fit on training latents only
  - Electrode positional encoding: 64-channel standard 10-10 coordinates,
    learnable refinement
  - Master seed: 42

Author: Theo Cognat (under direction with Claude, Anthropic)
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


# =============================================================================
# Locked hyperparameters
# =============================================================================

# Input
N_CHANNELS_IN  = 64
N_SAMPLES_IN   = 1000              # 4 s × 250 Hz
N_CHANNEL_GROUPS = 8               # 8 groups × 8 channels each
CHANNELS_PER_GROUP = N_CHANNELS_IN // N_CHANNEL_GROUPS  # 8

# Encoder
PRE_LOCAL_DIM     = 64
PRE_LOCAL_HEADS   = 4
PRE_LOCAL_LAYERS  = 2
GLOBAL_DIM        = 256
GLOBAL_HEADS      = 4
GLOBAL_LAYERS     = 1

# Predictor (matched to R_JEPA for fair comparison)
PREDICTOR_HIDDEN  = 512

# Spatial masking (Signal-JEPA finding)
MASK_PROBABILITY  = 0.25   # mask 25% of channel groups per training step

# SIGReg (matched to R_JEPA for fair comparison)
SIGREG_N_PROJECTIONS = 1024
SIGREG_BETA          = 1.0
SIGREG_WEIGHT        = 1.0

# Training (matched to R_JEPA)
LEARNING_RATE  = 1e-3
WEIGHT_DECAY   = 1e-4
N_TRAIN_EPOCHS = 50
BATCH_SIZE     = 32

# Output (matched to R_FM and R_JEPA)
RJEPA_BRAIN_TARGET_DIM = 8

# Preprocessing (must match §4 pipeline + R_FM + R_JEPA)
SAMPLING_RATE_HZ      = 250.0
BANDPASS_LOW_HZ       = 0.5
BANDPASS_HIGH_HZ      = 45.0
NOTCH_HZ              = 50.0
NOTCH_Q               = 30.0
ARTEFACT_THRESHOLD_UV = 150.0

MASTER_SEED = 42


# =============================================================================
# Preprocessing — mirror the §4 pipeline (same as R_FM / R_JEPA)
# =============================================================================

def preprocess_epoch(raw_epoch_uv: np.ndarray) -> np.ndarray:
    nyq = SAMPLING_RATE_HZ / 2.0
    b_bp, a_bp = butter(
        N=4, Wn=[BANDPASS_LOW_HZ / nyq, BANDPASS_HIGH_HZ / nyq], btype="band"
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


# =============================================================================
# Electrode positional encoding (Brain-JEPA-inspired)
# =============================================================================

# Approximate standard 10-10 electrode coordinates (sphere projection)
# These are 64-channel-system normalised positions; for the actual
# PhysioNet EEGMMIDB system the PI may need to substitute the
# correct electrode coordinates at registration time.
def default_electrode_positions(n_channels: int = N_CHANNELS_IN) -> np.ndarray:
    """Return (n_channels, 3) normalised 3-D positions on unit sphere.

    Placeholder layout: Fibonacci-sphere sampling for reproducibility.
    PI must replace with actual 10-10 coordinates for the system at
    registration time. The Fibonacci layout below is a deterministic
    default that allows the script to run without electrode metadata.
    """
    indices = np.arange(n_channels, dtype=np.float64) + 0.5
    phi = np.arccos(1 - 2 * indices / n_channels)
    theta = np.pi * (1 + 5 ** 0.5) * indices  # golden-angle spiral
    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)
    return np.stack([x, y, z], axis=1).astype(np.float32)


# =============================================================================
# Per-channel-group pre-local encoder (Signal-JEPA finding)
# =============================================================================

class PreLocalEncoder(nn.Module):
    """Process each channel group locally before global pooling.

    Signal-JEPA: pre-local architectures crucial for downstream performance.
    """
    def __init__(self):
        super().__init__()
        # Project each channel's time-series to PRE_LOCAL_DIM
        self.channel_proj = nn.Conv1d(
            CHANNELS_PER_GROUP, PRE_LOCAL_DIM,
            kernel_size=15, stride=8, padding=7,
        )
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=PRE_LOCAL_DIM, nhead=PRE_LOCAL_HEADS,
            dim_feedforward=PRE_LOCAL_DIM * 2,
            dropout=0.1, batch_first=True,
        )
        self.pre_local_transformer = nn.TransformerEncoder(
            encoder_layer, num_layers=PRE_LOCAL_LAYERS,
        )
        self.pool = nn.AdaptiveAvgPool1d(1)

    def forward(self, group_x: torch.Tensor) -> torch.Tensor:
        """group_x : (batch, CHANNELS_PER_GROUP, N_SAMPLES_IN)
        Returns: (batch, PRE_LOCAL_DIM)
        """
        h = self.channel_proj(group_x)   # (batch, dim, time')
        h = h.transpose(1, 2)             # (batch, time', dim)
        h = self.pre_local_transformer(h)
        h = h.transpose(1, 2)
        return self.pool(h).squeeze(-1)   # (batch, dim)


class BrainJEPAEncoder(nn.Module):
    """Brain-JEPA / Signal-JEPA-inspired encoder with:
     - Per-channel-group pre-local processing
     - Electrode positional encoding
     - Cross-group attention with [GLOBAL] token
     - Output GLOBAL_DIM-dim latent

    Input shape:  (batch, N_CHANNELS_IN, N_SAMPLES_IN)
    Output shape: (batch, GLOBAL_DIM)
    """
    def __init__(self, electrode_positions: np.ndarray):
        super().__init__()
        self.pre_local = PreLocalEncoder()

        # Group positional encoding from electrode coordinates
        group_positions = electrode_positions.reshape(
            N_CHANNEL_GROUPS, CHANNELS_PER_GROUP, 3
        ).mean(axis=1)
        self.register_buffer(
            "group_pos", torch.from_numpy(group_positions).float()
        )
        self.pos_proj = nn.Linear(3, PRE_LOCAL_DIM)

        # Learnable [GLOBAL] aggregation token
        self.global_token = nn.Parameter(
            torch.zeros(1, 1, PRE_LOCAL_DIM)
        )
        nn.init.normal_(self.global_token, std=0.02)

        # Project pre-local dim to global dim
        self.dim_project = nn.Linear(PRE_LOCAL_DIM, GLOBAL_DIM)

        # Cross-group transformer
        global_encoder_layer = nn.TransformerEncoderLayer(
            d_model=GLOBAL_DIM, nhead=GLOBAL_HEADS,
            dim_feedforward=GLOBAL_DIM * 2,
            dropout=0.1, batch_first=True,
        )
        self.global_transformer = nn.TransformerEncoder(
            global_encoder_layer, num_layers=GLOBAL_LAYERS,
        )

    def forward(self, x: torch.Tensor,
                spatial_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """x : (batch, N_CHANNELS_IN, N_SAMPLES_IN)
        spatial_mask : (batch, N_CHANNEL_GROUPS) Boolean mask
            (True = mask out for prediction objective)
        Returns: (batch, GLOBAL_DIM)
        """
        batch = x.shape[0]

        # Split into channel groups
        groups = x.reshape(batch, N_CHANNEL_GROUPS, CHANNELS_PER_GROUP, -1)

        # Per-group pre-local encoding (parallel over groups)
        group_embeddings = []
        for g in range(N_CHANNEL_GROUPS):
            group_embeddings.append(self.pre_local(groups[:, g]))
        group_embeddings = torch.stack(group_embeddings, dim=1)
        # (batch, N_CHANNEL_GROUPS, PRE_LOCAL_DIM)

        # Add electrode positional encoding
        pos_enc = self.pos_proj(self.group_pos)  # (N_CHANNEL_GROUPS, PRE_LOCAL_DIM)
        group_embeddings = group_embeddings + pos_enc.unsqueeze(0)

        # Apply spatial masking if provided (zero out masked groups)
        if spatial_mask is not None:
            group_embeddings = group_embeddings * (~spatial_mask).unsqueeze(-1).float()

        # Project to global dim
        group_embeddings = self.dim_project(group_embeddings)

        # Prepend [GLOBAL] token
        global_tok = self.dim_project(
            self.global_token.expand(batch, -1, -1)
        )
        tokens = torch.cat([global_tok, group_embeddings], dim=1)
        # (batch, 1 + N_CHANNEL_GROUPS, GLOBAL_DIM)

        # Cross-group attention
        out = self.global_transformer(tokens)

        # Extract [GLOBAL] token's representation
        return out[:, 0]  # (batch, GLOBAL_DIM)


# =============================================================================
# Predictor (matched to R_JEPA for fair comparison)
# =============================================================================

class JEPAPredictor(nn.Module):
    def __init__(self, n_action_dims: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(GLOBAL_DIM + n_action_dims, PREDICTOR_HIDDEN),
            nn.GELU(),
            nn.Linear(PREDICTOR_HIDDEN, GLOBAL_DIM),
        )

    def forward(self, z: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        return self.net(torch.cat([z, action], dim=-1))


# =============================================================================
# SIGReg (matched to R_JEPA for fair collapse-prevention comparison)
# =============================================================================

def sigreg_loss(z: torch.Tensor,
                n_projections: int = SIGREG_N_PROJECTIONS,
                beta: float = SIGREG_BETA) -> torch.Tensor:
    """Same SIGReg as R_JEPA. See [[(C)-R_JEPA-Feature-Extraction]] for full derivation."""
    batch_size, hidden_dim = z.shape
    device = z.device

    u = torch.randn(n_projections, hidden_dim, device=device)
    u = u / (u.norm(dim=1, keepdim=True) + 1e-12)
    y = (z @ u.T).T  # (n_projections, batch)

    y_mean = y.mean(dim=1, keepdim=True)
    y_std = y.std(dim=1, keepdim=True) + 1e-6
    y_norm = (y - y_mean) / y_std

    n = y_norm.shape[1]
    one_plus_2beta_sq = 1.0 + 2 * beta * beta
    one_plus_beta_sq = 1.0 + beta * beta

    diff = y_norm.unsqueeze(2) - y_norm.unsqueeze(1)
    term1 = torch.exp(-diff ** 2 / (2 * one_plus_2beta_sq))
    term1 = term1.sum(dim=(1, 2)) / (n * n * math.sqrt(one_plus_2beta_sq))

    term2 = -2.0 * torch.exp(-y_norm ** 2 / (2 * one_plus_beta_sq))
    term2 = term2.sum(dim=1) / (n * math.sqrt(one_plus_beta_sq))

    term3 = 1.0 / math.sqrt(one_plus_2beta_sq)

    return (term1 + term2 + term3).mean()


# =============================================================================
# Spatial mask generation (Signal-JEPA's key training innovation)
# =============================================================================

def sample_spatial_mask(batch_size: int, rng: torch.Generator) -> torch.Tensor:
    """Per-step random spatial mask: each channel group masked with probability
    MASK_PROBABILITY independently per batch element.
    """
    mask = torch.rand(batch_size, N_CHANNEL_GROUPS, generator=rng) < MASK_PROBABILITY
    # Ensure at least one group is NOT masked per batch element
    all_masked = mask.all(dim=1)
    if all_masked.any():
        # Unmask a random group for those examples
        unmask_indices = torch.randint(0, N_CHANNEL_GROUPS, (batch_size,),
                                       generator=rng)
        for b in range(batch_size):
            if all_masked[b]:
                mask[b, unmask_indices[b]] = False
    return mask


# =============================================================================
# Action encoding (matched to R_JEPA)
# =============================================================================

def encode_action(labels: np.ndarray, n_classes: int = 2) -> np.ndarray:
    n = labels.shape[0]
    onehot = np.zeros((n, n_classes), dtype=np.float32)
    onehot[np.arange(n), labels] = 1.0
    return onehot


# =============================================================================
# Train the Brain-JEPA-style end-to-end on the training fold
# =============================================================================

def train_brain_jepa(
    train_epochs: np.ndarray,
    train_labels: np.ndarray,
    n_classes: int,
    device: str,
    smoke_test: bool = False,
) -> Tuple[BrainJEPAEncoder, dict]:
    torch.manual_seed(MASTER_SEED)
    np.random.seed(MASTER_SEED)
    if device == "cuda":
        torch.cuda.manual_seed_all(MASTER_SEED)

    train_pp = np.stack([preprocess_epoch(e) for e in train_epochs])
    train_actions = encode_action(train_labels, n_classes)

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

    electrode_pos = default_electrode_positions()
    encoder = BrainJEPAEncoder(electrode_pos).to(device)
    predictor = JEPAPredictor(n_action_dims=n_classes).to(device)
    params = list(encoder.parameters()) + list(predictor.parameters())
    optimiser = torch.optim.AdamW(params, lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    mask_rng = torch.Generator()
    mask_rng.manual_seed(MASTER_SEED)

    n_epochs = 3 if smoke_test else N_TRAIN_EPOCHS
    history = {"loss_pred": [], "loss_sigreg": [], "loss_total": []}

    encoder.train(); predictor.train()
    for epoch in range(n_epochs):
        epoch_pred = []; epoch_sigreg = []; epoch_total = []
        for batch_x, batch_a, batch_x1 in loader:
            batch_x = batch_x.to(device); batch_a = batch_a.to(device); batch_x1 = batch_x1.to(device)
            batch_size = batch_x.shape[0]

            # Spatial masking (Signal-JEPA training innovation)
            spatial_mask = sample_spatial_mask(batch_size, mask_rng).to(device)

            z_t = encoder(batch_x, spatial_mask=spatial_mask)
            z_t1_target = encoder(batch_x1, spatial_mask=None).detach()  # no mask on target
            z_t1_pred = predictor(z_t, batch_a)

            loss_pred = ((z_t1_pred - z_t1_target) ** 2).mean()
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


# =============================================================================
# Extraction via frozen encoder + PCA to d = 8
# =============================================================================

def extract_features(encoder: BrainJEPAEncoder, epochs: np.ndarray,
                     device: str) -> np.ndarray:
    pp = np.stack([preprocess_epoch(e) for e in epochs])
    x = torch.from_numpy(pp).to(device)
    encoder.eval()
    with torch.no_grad():
        # No spatial masking at inference
        z = encoder(x, spatial_mask=None)
    return z.cpu().numpy()


def fit_pca_on_training_fold(train_latents: np.ndarray) -> PCA:
    pca = PCA(n_components=RJEPA_BRAIN_TARGET_DIM, random_state=MASTER_SEED)
    pca.fit(train_latents)
    return pca


# =============================================================================
# Top-level orchestration
# =============================================================================

def extract_rjepa_brain_for_fold(
    train_epochs_raw: np.ndarray,
    train_labels: np.ndarray,
    test_epochs_raw: np.ndarray,
    n_classes: int = 2,
    device: str = "cpu",
    smoke_test: bool = False,
) -> Tuple[np.ndarray, np.ndarray, dict]:
    encoder, history = train_brain_jepa(
        train_epochs_raw, train_labels, n_classes, device, smoke_test,
    )

    train_latents = extract_features(encoder, train_epochs_raw, device)
    test_latents = extract_features(encoder, test_epochs_raw, device)

    pca = fit_pca_on_training_fold(train_latents)
    rjepa_brain_train = pca.transform(train_latents)
    rjepa_brain_test = pca.transform(test_latents)

    provenance = {
        "architecture":          "Brain-JEPA / Signal-JEPA-inspired end-to-end",
        "encoder_class":         "BrainJEPAEncoder (8 channel groups; pre-local + global transformer)",
        "predictor_class":       "JEPAPredictor (2-layer MLP, hidden=512; matched to R_JEPA)",
        "n_channel_groups":      N_CHANNEL_GROUPS,
        "channels_per_group":    CHANNELS_PER_GROUP,
        "pre_local_dim":         PRE_LOCAL_DIM,
        "global_dim":            GLOBAL_DIM,
        "mask_probability":      MASK_PROBABILITY,
        "sigreg_n_projections":  SIGREG_N_PROJECTIONS,
        "sigreg_beta":           SIGREG_BETA,
        "sigreg_weight":         SIGREG_WEIGHT,
        "learning_rate":         LEARNING_RATE,
        "weight_decay":          WEIGHT_DECAY,
        "n_train_epochs":        int(train_epochs_raw.shape[0]),
        "n_test_epochs":         int(test_epochs_raw.shape[0]),
        "training_iters":        len(history["loss_pred"]),
        "final_loss_pred":       history["loss_pred"][-1],
        "final_loss_sigreg":     history["loss_sigreg"][-1],
        "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "git_commit":            _git_commit_hash(),
        "script_sha256":         _script_sha256(__file__),
        "torch_version":         torch.__version__,
        "numpy_version":         np.__version__,
        "deterministic":         True,
        "seed":                  MASTER_SEED,
        "smoke_test":            bool(smoke_test),
    }
    return rjepa_brain_train, rjepa_brain_test, provenance


# =============================================================================
# Provenance + CLI
# =============================================================================

def _git_commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "GIT_UNAVAILABLE"


def _script_sha256(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        description="R_JEPA_brain feature extraction (Amendment 4 to Phase A-1)"
    )
    parser.add_argument("--subject",      required=True, help="Subject ID")
    parser.add_argument("--fold",         required=True, type=int)
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

    rjb_train, rjb_test, prov = extract_rjepa_brain_for_fold(
        train_raw, train_lbl, test_raw, args.n_classes, args.device, args.smoke_test,
    )

    np.savez_compressed(args.output, rjepa_brain_train=rjb_train,
                                     rjepa_brain_test=rjb_test)

    prov.update({
        "subject": args.subject, "fold": args.fold,
        "input_train": str(args.train_epochs),
        "input_labels": str(args.train_labels),
        "input_test": str(args.test_epochs),
        "output": str(args.output),
        "device": args.device,
        "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
    })
    args.manifest.write_text(json.dumps(prov, indent=2))

    print(f"OK: wrote {args.output} and {args.manifest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())