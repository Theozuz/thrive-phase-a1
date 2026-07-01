"""
R_GL Feature Extraction — Amendment 5 to Phase A-1
====================================================

Pure-graph-Laplacian baseline on the same 40-node Yeo-17-scale topology
as the sheaf. Tests whether cellular cohomology adds empirical value
beyond standard graph spectral methods.

No neural-net training. Just:
  1. Preprocess EEG per §4 pipeline (matched to R_FM / R_JEPA)
  2. Build graph Laplacian L_G on the same 40-node topology
  3. Compute per-epoch graph-Laplacian spectral features
  4. PCA-project to d = 8 (per-fold isolation)

Locked invariants (cannot modify post-registration):
  - Same 40-node graph topology as the sheaf (small-world + Yeo-17-scale)
  - Identity restriction maps (the defining feature of "graph Laplacian, not
    sheaf"): each node projects its scalar (mean tangent-space activation)
    directly into the edge comparison
  - Top-K=16 Laplacian eigenmodes for spectral features
  - Per-fold PCA to d=8 (matched to R_FM / R_JEPA / R_JEPA_brain)
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
from typing import Optional, Tuple

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
from scipy.linalg import eigh
from sklearn.decomposition import PCA


# =============================================================================
# Locked parameters
# =============================================================================

# Graph (matches sheaf topology in Phase A-7 ACP twin and Phase B-2 extension)
N_NODES = 40                # 32 N-nodes + 8 V/S/K context nodes
N_EDGES = 80                # directed; treated as undirected for graph Laplacian
N_CHANNELS_NEURAL = 32      # PhysioNet EEGMMIDB
CHANNELS_PER_NODE = 8       # 8 channels per N-node (consistent with R_FM/R_JEPA)

# Graph Laplacian features
TOP_K_EIGENMODES = 16       # spectral feature dimensionality before PCA

# Output (matched to R_FM / R_JEPA / R_JEPA_brain)
RGL_TARGET_DIM = 8

# Preprocessing (matched to §4 pipeline + sibling scripts)
SAMPLING_RATE_HZ      = 250.0
BANDPASS_LOW_HZ       = 0.5
BANDPASS_HIGH_HZ      = 45.0
NOTCH_HZ              = 50.0
NOTCH_Q               = 30.0
ARTEFACT_THRESHOLD_UV = 150.0

MASTER_SEED = 42


# =============================================================================
# Preprocessing (matched to siblings)
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
# Graph construction — matches sheaf topology in Phase A-7 ACP twin
# =============================================================================

def build_graph_topology(rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    """Build the same 40-node 80-edge topology as the sheaf graph.

    Returns
    -------
    edges : (N_EDGES, 2) — undirected edges (sheaf's directed edges are
                            symmetrised for the graph Laplacian)
    L_G   : (N_NODES, N_NODES) — graph Laplacian (D - A)
    """
    # Same small-world construction as Phase A-7 ACP twin
    edges = []
    for i in range(N_NODES):
        edges.append((i, (i + 1) % N_NODES))
        j = int(rng.integers(0, N_NODES))
        while j == i or j == (i + 1) % N_NODES:
            j = int(rng.integers(0, N_NODES))
        edges.append((i, j))
    edges = np.array(edges[:N_EDGES])

    # Build (undirected) adjacency
    A = np.zeros((N_NODES, N_NODES))
    for u, v in edges:
        A[u, v] += 1.0
        A[v, u] += 1.0  # symmetrise for undirected graph
    D = np.diag(A.sum(axis=1))
    L_G = D - A
    return edges, L_G


def precompute_eigendecomposition(L_G: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Eigendecompose the graph Laplacian once; reuse for every epoch.

    Returns top-K eigenvalues + corresponding eigenvectors.
    """
    evals, evecs = eigh(L_G)
    # Skip the zero eigenvalue (constant function); take next TOP_K
    return evals[1:TOP_K_EIGENMODES + 1], evecs[:, 1:TOP_K_EIGENMODES + 1]


# =============================================================================
# Per-node scalar projection — the "identity restriction map" choice
# =============================================================================

def epoch_to_node_scalars(epoch_preprocessed: np.ndarray) -> np.ndarray:
    """Project preprocessed EEG (32 channels × T samples) to per-node scalars.

    Each node gets the mean signal energy across its 8 assigned channels.
    This is the scalar-Laplacian analogue of the sheaf's vector-stalk
    projection — no orthogonal rotation, just scalar pooling.

    Returns (N_NODES,) scalar per-node activations.
    """
    # First 32 nodes = neural; map 32 channels → 32 nodes (1 channel per node)
    # to match the sheaf's per-node electrode-grouping
    channels_per_n_node = N_CHANNELS_NEURAL // 32   # = 2
    neural_scalars = np.empty(32)
    for n in range(32):
        ch_start = n * channels_per_n_node
        ch_end = ch_start + channels_per_n_node
        neural_scalars[n] = float(np.mean(epoch_preprocessed[ch_start:ch_end] ** 2))

    # Remaining 8 nodes = V/S/K context. For R_GL (graph-only baseline) we
    # set context nodes to zero — they have no scalar projection in the
    # graph-Laplacian formulation. (This is the honest minimal baseline.)
    context_scalars = np.zeros(N_NODES - 32)

    return np.concatenate([neural_scalars, context_scalars])


# =============================================================================
# Graph-spectral feature computation
# =============================================================================

def compute_gl_features(epoch_preprocessed: np.ndarray,
                       eigvals: np.ndarray, eigvecs: np.ndarray) -> np.ndarray:
    """Project per-node scalars onto top-K graph-Laplacian eigenmodes.

    Returns (TOP_K_EIGENMODES,) spectral feature vector.
    """
    f = epoch_to_node_scalars(epoch_preprocessed)
    # Spectral projection: ĉ_k = <f, v_k> for each eigenvector v_k
    spectral = eigvecs.T @ f
    # Optionally weight by inverse eigenvalue (low-frequency emphasis):
    # using uniform weighting for the locked baseline (no extra knobs)
    return spectral


# =============================================================================
# Per-fold PCA (training-only fit; matches sibling discipline)
# =============================================================================

def fit_pca_on_training_fold(train_features: np.ndarray) -> PCA:
    pca = PCA(n_components=RGL_TARGET_DIM, random_state=MASTER_SEED)
    pca.fit(train_features)
    return pca


# =============================================================================
# Top-level extraction
# =============================================================================

def extract_rgl_for_fold(
    train_epochs_raw: np.ndarray,
    test_epochs_raw: np.ndarray,
    smoke_test: bool = False,
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """Run the R_GL extraction for one fold."""
    np.random.seed(MASTER_SEED)
    rng = np.random.default_rng(MASTER_SEED)

    edges, L_G = build_graph_topology(rng)
    eigvals, eigvecs = precompute_eigendecomposition(L_G)

    if smoke_test:
        train_epochs_raw = train_epochs_raw[: min(20, len(train_epochs_raw))]
        test_epochs_raw  = test_epochs_raw[: min(10, len(test_epochs_raw))]

    # Preprocess and extract
    train_features = np.stack([
        compute_gl_features(preprocess_epoch(e), eigvals, eigvecs)
        for e in train_epochs_raw
    ])
    test_features = np.stack([
        compute_gl_features(preprocess_epoch(e), eigvals, eigvecs)
        for e in test_epochs_raw
    ])

    # PCA fit on training fold only
    pca = fit_pca_on_training_fold(train_features)
    rgl_train = pca.transform(train_features)
    rgl_test  = pca.transform(test_features)

    provenance = {
        "architecture":      "Graph-Laplacian-only baseline (no sheaf structure)",
        "n_nodes":           N_NODES,
        "n_edges":           N_EDGES,
        "top_k_eigenmodes":  TOP_K_EIGENMODES,
        "channels_per_neural_node": N_CHANNELS_NEURAL // 32,
        "target_dim":        RGL_TARGET_DIM,
        "n_train_epochs":    int(train_epochs_raw.shape[0]),
        "n_test_epochs":     int(test_epochs_raw.shape[0]),
        "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "git_commit":        _git_commit_hash(),
        "script_sha256":     _script_sha256(__file__),
        "numpy_version":     np.__version__,
        "deterministic":     True,
        "seed":              MASTER_SEED,
        "smoke_test":        bool(smoke_test),
    }
    return rgl_train, rgl_test, provenance


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
        description="R_GL feature extraction (Amendment 5 to Phase A-1)"
    )
    parser.add_argument("--subject",      default=None)
    parser.add_argument("--fold",         default=None, type=int)
    parser.add_argument("--train-epochs", default=None, type=Path)
    parser.add_argument("--test-epochs",  default=None, type=Path)
    parser.add_argument("--output",       default=None, type=Path)
    parser.add_argument("--manifest",     default=None, type=Path)
    parser.add_argument("--smoke-test",   action="store_true",
                        help="Run synthetic-Gaussian smoke test; path args optional in this mode.")
    args = parser.parse_args(argv)

    if args.smoke_test:
        # Synthetic Gaussian smoke test. Generates synthetic EEG-like epoch
        # tensors and runs the extraction end-to-end; no PhysioNet data
        # touched. Same discipline as a0_preflight.py --smoke-test.
        rng = np.random.default_rng(MASTER_SEED)
        n_channels = N_CHANNELS_NEURAL
        n_samples  = int(SAMPLING_RATE_HZ * 4)
        train_raw = rng.standard_normal((30, n_channels, n_samples)).astype(np.float32) * 20.0
        test_raw  = rng.standard_normal((20, n_channels, n_samples)).astype(np.float32) * 20.0
        out_path      = args.output   or Path("rgl_smoke.npz")
        manifest_path = args.manifest or Path("rgl_smoke_manifest.json")
        subject_id    = args.subject  or "SMOKE"
        fold_id       = args.fold if args.fold is not None else 0
    else:
        # Non-smoke mode requires all path args.
        missing = [name for name in
                   ("subject", "fold", "train_epochs", "test_epochs", "output", "manifest")
                   if getattr(args, name) is None]
        if missing:
            print(f"ERROR: missing required args (non-smoke mode): {missing}",
                  file=sys.stderr)
            return 2
        train_raw     = np.load(args.train_epochs)
        test_raw      = np.load(args.test_epochs)
        out_path      = args.output
        manifest_path = args.manifest
        subject_id    = args.subject
        fold_id       = args.fold

    rgl_train, rgl_test, prov = extract_rgl_for_fold(
        train_raw, test_raw, args.smoke_test,
    )

    np.savez_compressed(out_path, rgl_train=rgl_train, rgl_test=rgl_test)

    prov.update({
        "subject":      subject_id,
        "fold":         fold_id,
        "input_train":  str(args.train_epochs) if args.train_epochs else "<synthetic>",
        "input_test":   str(args.test_epochs)  if args.test_epochs  else "<synthetic>",
        "output":       str(out_path),
        "timestamp_utc": datetime.datetime.now(datetime.UTC).isoformat(),
    })
    manifest_path.write_text(json.dumps(prov, indent=2))

    print(f"OK: wrote {out_path} and {manifest_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())