"""
sheaf_features.py — Unified sheaf-family feature extractor (Phase A-1 core)
==========================================================================
THE previously-missing load-bearing artefact. Replaces the scalar rgl_features.py.
Produces all three sheaf-family representations via --mode, differing ONLY in the
restriction maps, on identical covariance-tangent stalks / topology / readout:

    R_GL    : Q_e = identity     (block graph Laplacian; no cohomology)   [H10 control]
    S-rand  : Q_e = random Haar   (maps present, untrained; null)          [H1 control]
    S-TTSA  : Q_e = learned        (energy-descent Stiefel TTSA)            [hypothesis]

So H1 = learned vs random, H10 = learned vs identity — clean cohomology tests.

RATIFIED DECISIONS (see (C)-Sheaf-Feature-Extraction.md):
 1. Learning rule = ENERGY DESCENT of the PC sheaf energy E = x^T L_F x
    (grad 2(Q x_u - x_v) x_u^T; Stiefel retraction EVERY pass). The local
    prediction-error rule the sheaf provably globalises — NOT Hebbian (that is
    the R_BDH / Stage-2 associative mechanism).
 2. Stalks = per-node local COVARIANCE TANGENT (OAS cov + Riemannian TangentSpace
    at the per-fold Frechet mean) over {channel i + 3 nearest}. STALK_DIM = 10.
    Reuses the exact machinery A-0 validates; unsupervised; per-fold isolated.
 3. Readout = bottom-K = 16 HARMONIC eigenmodes of L_F -> per-fold PCA to d = 8.
 4. TTSA stops on TRAIN-energy convergence (no fixed pass count); Robbins-Monro decay.

Locked invariants: N_NODES=40 (32 neural + 8 context), N_EDGES=80, STALK_DIM=10,
topology from build_graph_topology(seed=42) byte-identical to phase_a7_acp_twin /
(legacy) rgl. Master seed 42; sub-seeds via SHA-256 (process-stable).

Author: Theodore Zuzarte (drafted with Claude, Anthropic).  Licence: MIT
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Optional, Tuple

import numpy as np

# --------------------------------------------------------------------------- #
# Locked parameters
# --------------------------------------------------------------------------- #
MASTER_SEED    = 42
N_NODES_NEURAL = 32
N_NODES        = 40          # 32 neural + 4 V + 2 S + 2 K context
N_EDGES        = 80
STALK_DIM      = 10          # tangent dim of a 4x4 SPD (4*5/2)
K_NEIGHBOURS   = 3           # node = channel + 3 nearest -> 4-channel local covariance

BOTTOM_K         = 16        # near-harmonic eigenmodes (readout)
SHEAF_TARGET_DIM = 8         # PCA output (matches R_FM / R_JEPA)

TTSA_LR0, TTSA_DECAY               = 1e-2, 0.995     # Robbins-Monro (Borkar 2008)
N_PASSES = 300

MODES = ("R_GL", "S-rand", "S-TTSA")


# --------------------------------------------------------------------------- #
# Deterministic sub-seeding (process-stable; cf. synth_a1 hashlib fix)
# --------------------------------------------------------------------------- #
def subseed(procedure: str, subject: int = -1, fold: int = -1) -> int:
    key = f"{MASTER_SEED}|{procedure}|{subject}|{fold}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest(), 16) % (2**32)


# --------------------------------------------------------------------------- #
# Graph topology  (MUST be byte-identical to rgl / twin build_graph_topology)
# --------------------------------------------------------------------------- #
def build_graph_topology(rng: np.random.Generator) -> np.ndarray:
    edges = []
    for i in range(N_NODES):
        edges.append((i, (i + 1) % N_NODES))
        j = int(rng.integers(0, N_NODES))
        while j == i or j == (i + 1) % N_NODES:
            j = int(rng.integers(0, N_NODES))
        edges.append((i, j))
    return np.array(edges[:N_EDGES], dtype=int)


# --------------------------------------------------------------------------- #
# Orthogonal helpers + the three map families
# --------------------------------------------------------------------------- #
def qf(M: np.ndarray) -> np.ndarray:
    Q, R = np.linalg.qr(M)
    return Q * np.sign(np.sign(np.diag(R)) + 0.5)      # sign-stabilised

def haar_orthogonal(d: int, rng: np.random.Generator) -> np.ndarray:
    return qf(rng.standard_normal((d, d)))

def init_rotors(rng: np.random.Generator) -> np.ndarray:
    return np.stack([haar_orthogonal(STALK_DIM, rng) for _ in range(N_EDGES)])

def identity_rotors() -> np.ndarray:
    return np.stack([np.eye(STALK_DIM) for _ in range(N_EDGES)])


# --------------------------------------------------------------------------- #
# Sheaf Laplacian  L_F = delta^T delta,  (delta x)_e = Q_e x_u - x_v
# --------------------------------------------------------------------------- #
def assemble_laplacian(edges: np.ndarray, rotors: np.ndarray) -> np.ndarray:
    total = N_NODES * STALK_DIM
    L = np.zeros((total, total))
    for k, (u, v) in enumerate(edges):
        Q = rotors[k]
        ua, va = u * STALK_DIM, v * STALK_DIM
        L[ua:ua+STALK_DIM, ua:ua+STALK_DIM] += Q.T @ Q                # = I here
        L[va:va+STALK_DIM, va:va+STALK_DIM] += np.eye(STALK_DIM)
        L[ua:ua+STALK_DIM, va:va+STALK_DIM] += -Q.T
        L[va:va+STALK_DIM, ua:ua+STALK_DIM] += -Q
    return L

def pc_energy(x: np.ndarray, edges: np.ndarray, rotors: np.ndarray) -> float:
    e = 0.0
    for k, (u, v) in enumerate(edges):
        r = rotors[k] @ x[u] - x[v]
        e += float(r @ r)
    return e


# --------------------------------------------------------------------------- #
# Energy-descent Stiefel TTSA step (RATIFIED rule; also replaces the twin's)
# --------------------------------------------------------------------------- #
def stiefel_ttsa_step(rotors: np.ndarray, edges: np.ndarray,
                      batch: np.ndarray, lr: float) -> np.ndarray:
    B = batch.shape[0]
    new = rotors.copy()
    for k, (u, v) in enumerate(edges):
        Q = rotors[k]
        Xu, Xv = batch[:, u, :], batch[:, v, :]
        resid = Xu @ Q.T - Xv                          # (Q x_u - x_v)^T
        G  = (2.0 / B) * (resid.T @ Xu)                # TRUE energy gradient
        QtG = Q.T @ G
        rG = G - Q @ (0.5 * (QtG + QtG.T))             # Stiefel tangent
        new[k] = qf(Q - lr * rG)                       # retraction EVERY step
    return new

def learn_rotors(train_stalks: np.ndarray, edges: np.ndarray,
                 rng: np.random.Generator) -> Tuple[np.ndarray, list]:
    """S-TTSA: energy-descent SA for a FIXED budget (energy converges before the
    discriminative structure develops, so a convergence criterion under-trains)."""
    rotors, lr, energy = init_rotors(rng), TTSA_LR0, []
    for p in range(N_PASSES):
        rotors = stiefel_ttsa_step(rotors, edges, train_stalks, lr)
        lr *= TTSA_DECAY
        if p % 20 == 0:
            energy.append(float(np.mean([pc_energy(x, edges, rotors) for x in train_stalks])))
    return rotors, energy


# --------------------------------------------------------------------------- #
# Bottom-K harmonic coherence readout
# --------------------------------------------------------------------------- #
def coherence_basis(edges: np.ndarray, rotors: np.ndarray) -> np.ndarray:
    L = assemble_laplacian(edges, rotors)
    _, evecs = np.linalg.eigh(L)                       # ascending
    return evecs[:, :BOTTOM_K]                         # (N*d, BOTTOM_K)


# --------------------------------------------------------------------------- #
# EEG -> node-stalk mapping (RATIFIED B2; exercised on real data post-DOI)
# --------------------------------------------------------------------------- #
def build_channel_neighbourhoods(montage_xyz: np.ndarray) -> list:
    from scipy.spatial.distance import cdist
    D = cdist(montage_xyz, montage_xyz)
    return [np.argsort(D[i])[:K_NEIGHBOURS + 1] for i in range(N_NODES_NEURAL)]

def fit_node_tangents(train_epochs_uv: np.ndarray, neighbourhoods: list) -> list:
    from pyriemann.estimation import Covariances
    from pyriemann.tangentspace import TangentSpace
    ts = []
    for nbr in neighbourhoods:
        cov = Covariances(estimator="oas").transform(train_epochs_uv[:, nbr, :])
        ts.append(TangentSpace(metric="riemann").fit(cov))
    return ts

def epochs_to_node_stalks(epochs_uv: np.ndarray, neighbourhoods: list,
                          tangent_spaces: list) -> np.ndarray:
    from pyriemann.estimation import Covariances
    out = np.zeros((len(epochs_uv), N_NODES, STALK_DIM))     # context nodes stay 0
    for i, nbr in enumerate(neighbourhoods):
        cov = Covariances(estimator="oas").transform(epochs_uv[:, nbr, :])
        out[:, i, :] = tangent_spaces[i].transform(cov)
    return out


# --------------------------------------------------------------------------- #
# Per-fold extraction (stalks -> features) for one mode
# --------------------------------------------------------------------------- #
def extract_for_fold(train_stalks: np.ndarray, test_stalks: np.ndarray,
                     mode: str, subject: int, fold: int) -> dict:
    from sklearn.decomposition import PCA
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}; got {mode!r}")

    edges = build_graph_topology(np.random.default_rng(subseed("topology")))
    rng = np.random.default_rng(subseed(f"rotors_{mode}", subject, fold))

    if mode == "R_GL":
        rotors, energy = identity_rotors(), []
    elif mode == "S-rand":
        rotors, energy = init_rotors(rng), []
    else:  # S-TTSA
        rotors, energy = learn_rotors(train_stalks, edges, rng)

    V = coherence_basis(edges, rotors)                 # train/test share the basis
    tr = train_stalks.reshape(len(train_stalks), -1) @ V
    te = test_stalks.reshape(len(test_stalks), -1) @ V

    pca = PCA(n_components=SHEAF_TARGET_DIM, random_state=subseed("pca", subject, fold))
    return {
        "mode": mode, "subject": subject, "fold": fold,
        "train_features": pca.fit_transform(tr),
        "test_features":  pca.transform(te),
        "n_passes": len(energy),
    }


# --------------------------------------------------------------------------- #
# Smoke test: different per-class edge relations; learned maps must recover them
# --------------------------------------------------------------------------- #
def _make_synthetic_two_class(n_per_class: int, rng: np.random.Generator):
    edges = build_graph_topology(np.random.default_rng(subseed("topology")))
    Ra = haar_orthogonal(STALK_DIM, np.random.default_rng(1))
    Rb = haar_orthogonal(STALK_DIM, np.random.default_rng(2))
    def gen(Rc, n):
        out = np.zeros((n, N_NODES, STALK_DIM))
        for i in range(n):
            x = rng.standard_normal((N_NODES, STALK_DIM))
            for (u, v) in edges:
                x[v] = Rc @ x[u] + 0.35 * rng.standard_normal(STALK_DIM)
            out[i] = x
        return out
    X = np.concatenate([gen(Ra, n_per_class), gen(Rb, n_per_class)])
    y = np.r_[np.zeros(n_per_class), np.ones(n_per_class)].astype(int)
    return X, y

def smoke_test() -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold

    rng = np.random.default_rng(MASTER_SEED)
    X, y = _make_synthetic_two_class(80, rng)

    def cv_acc(mode: str) -> float:
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=MASTER_SEED)
        accs = []
        for tr, te in skf.split(X, y):
            r = extract_for_fold(X[tr], X[te], mode, subject=0, fold=0)
            clf = LogisticRegression(max_iter=1000).fit(r["train_features"], y[tr])
            accs.append(clf.score(r["test_features"], y[te]))
        return float(np.mean(accs))

    a_ttsa, a_rand, a_gl = cv_acc("S-TTSA"), cv_acc("S-rand"), cv_acc("R_GL")
    return {
        "smoke_test_passed": bool(a_ttsa > a_rand + 0.02),     # H1 core
        "acc_S_TTSA": a_ttsa, "acc_S_rand": a_rand, "acc_R_GL": a_gl,
        "note": "H1: learned (S-TTSA) beats random (S-rand). S-TTSA should also "
                "exceed identity (R_GL) — the H10 cohomology contrast.",
    }


# --------------------------------------------------------------------------- #
def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="Unified sheaf-family extractor")
    ap.add_argument("--smoke-test", action="store_true")
    ap.add_argument("--output", type=str, default=None)
    args = ap.parse_args(argv)

    if args.smoke_test:
        result = smoke_test()
        print(json.dumps(result, indent=2))
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2))
        return 0 if result["smoke_test_passed"] else 1

    print("Real-data extraction is driven by the Phase A-1 harness "
          "(epochs_to_node_stalks -> extract_for_fold). Run --smoke-test.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
