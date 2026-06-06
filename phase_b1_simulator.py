"""
Phase B-1 Harmonic-Mode-Duration Simulator
============================================

Implements §7.8 of the Phase A revised proposal: 3 × 4 × 3 factorial
simulation testing whether THINK-mode harmonic preservation produces
stable sustained dynamics over the COGITATE-relevant 200-1500 ms
sustained-activity timescale.

Factorial:
  λ_harm:       0.0, 0.5, 1.0, 2.0           (4 levels)
  Init harm. mass:  low=0.1, medium=0.3, high=0.5  (3 levels)
  Perturbation:     none=0.00, small=0.01, medium=0.05  (3 levels)

3 × 4 × 3 = 36 conditions × 100 seeds = 3,600 simulation runs.

Each run:
  1. Generate a 40-node 80-edge sheaf graph with random orthogonal
     restriction maps. Eigendecompose to find ker(L_F).
  2. Initialise state x(0) with the specified harmonic-mass fraction
     allocated to ker(L_F) and the remainder in the gradient + curl
     components.
  3. Integrate state + restriction-map dynamics for 5000 ms at 250 Hz
     (1250 cycles).
       State:  dx/dt = -L_F(t) x + λ_harm * P_kerL(t) * x
       Maps:   θ(t+dt) = θ(t) + dt * perturb * N(0, I) (small random walk)
  4. Log harmonic mass m(t) = ||P_kerL x||² / ||x||² per cycle.

Endpoints:
  E1: m(1000ms) / m(0) >= 0.5
  E2: 0.1 <= m(t) / m(0) <= 2.0 for all t in [0, 5000] ms
  E3: λ_harm window identification (E1 + E2 both pass)
  E4: Robustness — does (E1, E2) hold at perturb = 0.05?

Locked invariants:
  - Master seed: 42
  - Per-condition seeds: 42 + condition_index*1000 + seed_index
  - Graph topology: deterministic 40-node small-world
  - Stalk dim: d = 8 per node; total state dim = 320
  - Integration: explicit Euler, dt = 4 ms (250 Hz)

Author: Theo Cognat (under direction with Claude, Anthropic)
Licence: MIT
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple

import numpy as np

# -----------------------------------------------------------------------------
# Locked simulation parameters (§7.8 of the protocol)
# -----------------------------------------------------------------------------

N_NODES = 40
N_EDGES = 80
STALK_DIM = 8

DT_MS = 4.0              # 250 Hz
T_TOTAL_MS = 5000.0      # 5-second window
N_CYCLES = int(T_TOTAL_MS / DT_MS)  # 1250 cycles
E1_CYCLE = int(1000.0 / DT_MS)       # 250 cycles = 1000 ms

# Factor levels — locked
LAMBDA_HARM_LEVELS  = (0.0, 0.5, 1.0, 2.0)
INIT_HARM_MASS_LEVELS = {"low": 0.1, "medium": 0.3, "high": 0.5}
PERTURB_LEVELS = {"none": 0.0, "small": 0.01, "medium": 0.05}

# Gate criteria — locked
E1_RATIO_THRESHOLD = 0.5
E2_RATIO_BOUNDS = (0.1, 2.0)

MASTER_SEED = 42


# -----------------------------------------------------------------------------
# Sheaf graph construction
# -----------------------------------------------------------------------------

def build_sheaf_graph(rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build a deterministic 40-node small-world sheaf graph with 80 edges.

    Returns
    -------
    edges : (N_EDGES, 2) array of (source, target) node indices
    rotors : (N_EDGES, STALK_DIM, STALK_DIM) array of orthogonal restriction maps
    laplacian : (N_NODES*STALK_DIM, N_NODES*STALK_DIM) sheaf Laplacian
    """
    # Small-world topology: ring + random shortcuts
    edges = []
    for i in range(N_NODES):
        # Local ring connection
        edges.append((i, (i + 1) % N_NODES))
        # Long-range shortcut
        j = rng.integers(0, N_NODES)
        while j == i or j == (i + 1) % N_NODES:
            j = rng.integers(0, N_NODES)
        edges.append((i, j))
    edges = np.array(edges[:N_EDGES])

    # Random orthogonal restriction maps (one per edge)
    rotors = np.empty((N_EDGES, STALK_DIM, STALK_DIM))
    for k in range(N_EDGES):
        H = rng.standard_normal((STALK_DIM, STALK_DIM))
        Q, _ = np.linalg.qr(H)
        rotors[k] = Q

    laplacian = assemble_laplacian(edges, rotors)
    return edges, rotors, laplacian


def assemble_laplacian(edges: np.ndarray, rotors: np.ndarray) -> np.ndarray:
    """Construct the sheaf Laplacian L_F from restriction-map rotors."""
    total_dim = N_NODES * STALK_DIM
    L = np.zeros((total_dim, total_dim))
    for k, (u, v) in enumerate(edges):
        Q = rotors[k]
        # Block diagonals
        L[u*STALK_DIM:(u+1)*STALK_DIM, u*STALK_DIM:(u+1)*STALK_DIM] += np.eye(STALK_DIM)
        L[v*STALK_DIM:(v+1)*STALK_DIM, v*STALK_DIM:(v+1)*STALK_DIM] += Q.T @ Q
        # Off-diagonals
        L[u*STALK_DIM:(u+1)*STALK_DIM, v*STALK_DIM:(v+1)*STALK_DIM] -= Q.T
        L[v*STALK_DIM:(v+1)*STALK_DIM, u*STALK_DIM:(u+1)*STALK_DIM] -= Q
    return L


# -----------------------------------------------------------------------------
# Kernel projection
# -----------------------------------------------------------------------------

def kernel_projection(laplacian: np.ndarray, tol: float = 1e-8) -> np.ndarray:
    """Return P_kerL — the projection matrix onto the kernel of L_F.

    Computed via eigendecomposition; eigenvectors with eigenvalues below tol
    are in the kernel.
    """
    eigvals, eigvecs = np.linalg.eigh(laplacian)
    kernel_mask = eigvals < tol
    V0 = eigvecs[:, kernel_mask]
    P = V0 @ V0.T
    return P


def harmonic_mass(x: np.ndarray, P_ker: np.ndarray) -> float:
    """Compute ||P_ker x||² / ||x||²."""
    proj = P_ker @ x
    return float((proj @ proj) / (x @ x + 1e-12))


# -----------------------------------------------------------------------------
# Initial state with controlled harmonic-mass fraction
# -----------------------------------------------------------------------------

def initialise_state(
    P_ker: np.ndarray,
    init_harm_fraction: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Initialise x(0) with specified fraction of energy in ker(L_F)."""
    total_dim = P_ker.shape[0]
    # Random vector decomposed into kernel and orthogonal complement
    raw = rng.standard_normal(total_dim)
    x_ker = P_ker @ raw
    x_perp = raw - x_ker
    # Normalise each component, then scale to the target fractions
    x_ker /= (np.linalg.norm(x_ker) + 1e-12)
    x_perp /= (np.linalg.norm(x_perp) + 1e-12)
    x = (np.sqrt(init_harm_fraction) * x_ker
         + np.sqrt(1 - init_harm_fraction) * x_perp)
    return x


# -----------------------------------------------------------------------------
# Dynamics integration
# -----------------------------------------------------------------------------

def integrate_dynamics(
    x0: np.ndarray,
    edges: np.ndarray,
    rotors0: np.ndarray,
    lambda_harm: float,
    perturb_sigma: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Integrate state and restriction-map dynamics for N_CYCLES.

    State:  dx/dt = -L_F(t) x + λ_harm * P_kerL(t) * x
    Maps:   θ(t+dt) = θ(t) + dt * perturb * N(0, I), projected back to SO(d)

    Returns
    -------
    harmonic_traj : (N_CYCLES + 1,) array of m(t) = ||P_ker x||² / ||x||²
    """
    rotors = rotors0.copy()
    x = x0.copy()
    L = assemble_laplacian(edges, rotors)
    P_ker = kernel_projection(L)

    traj = np.empty(N_CYCLES + 1)
    traj[0] = harmonic_mass(x, P_ker)

    dt_s = DT_MS / 1000.0  # convert to seconds for natural scaling

    for t in range(N_CYCLES):
        # State update — explicit Euler
        x = x + dt_s * (-L @ x + lambda_harm * (P_ker @ x))
        # Optional state renormalisation to prevent unbounded growth
        # (matches the bounded-state requirement of biological neural systems)
        norm = np.linalg.norm(x)
        if norm > 10.0:
            x = x * (10.0 / norm)

        # Restriction-map perturbation — small Gaussian drift
        if perturb_sigma > 0.0:
            for k in range(N_EDGES):
                noise = rng.standard_normal((STALK_DIM, STALK_DIM)) * perturb_sigma * dt_s
                perturbed = rotors[k] + noise
                # Re-orthogonalise
                Q, _ = np.linalg.qr(perturbed)
                rotors[k] = Q
            L = assemble_laplacian(edges, rotors)
            P_ker = kernel_projection(L)

        traj[t + 1] = harmonic_mass(x, P_ker)

    return traj


# -----------------------------------------------------------------------------
# Endpoint evaluation
# -----------------------------------------------------------------------------

@dataclass
class RunResult:
    lambda_harm: float
    init_harm_label: str
    init_harm_fraction: float
    perturb_label: str
    perturb_sigma: float
    seed: int
    m0: float
    m_1000ms: float
    m_max: float
    m_min: float
    e1_pass: bool
    e2_pass: bool


def evaluate_run(
    trajectory: np.ndarray,
    lambda_harm: float,
    init_harm_label: str,
    init_harm_fraction: float,
    perturb_label: str,
    perturb_sigma: float,
    seed: int,
) -> RunResult:
    """Compute E1 and E2 outcomes for a single run."""
    m0 = trajectory[0]
    m_1000 = trajectory[E1_CYCLE]
    m_max = float(trajectory.max())
    m_min = float(trajectory.min())
    if m0 > 1e-12:
        ratio_1000 = m_1000 / m0
        ratio_max = m_max / m0
        ratio_min = m_min / m0
    else:
        ratio_1000 = 0.0
        ratio_max = 0.0
        ratio_min = 0.0

    e1 = ratio_1000 >= E1_RATIO_THRESHOLD
    e2 = (ratio_min >= E2_RATIO_BOUNDS[0]) and (ratio_max <= E2_RATIO_BOUNDS[1])

    return RunResult(
        lambda_harm=lambda_harm,
        init_harm_label=init_harm_label,
        init_harm_fraction=init_harm_fraction,
        perturb_label=perturb_label,
        perturb_sigma=perturb_sigma,
        seed=seed,
        m0=float(m0),
        m_1000ms=float(m_1000),
        m_max=m_max,
        m_min=m_min,
        e1_pass=bool(e1),
        e2_pass=bool(e2),
    )


# -----------------------------------------------------------------------------
# Aggregation across seeds → per-condition statistics
# -----------------------------------------------------------------------------

def aggregate_condition(runs: List[RunResult]) -> dict:
    """Aggregate run results per condition into pass-rate statistics."""
    n = len(runs)
    e1_rate = sum(r.e1_pass for r in runs) / n
    e2_rate = sum(r.e2_pass for r in runs) / n
    both_rate = sum(r.e1_pass and r.e2_pass for r in runs) / n
    m_1000_mean = float(np.mean([r.m_1000ms for r in runs]))
    m_1000_std = float(np.std([r.m_1000ms for r in runs]))

    return {
        "n_seeds":       n,
        "e1_pass_rate":  e1_rate,
        "e2_pass_rate":  e2_rate,
        "both_pass_rate": both_rate,
        "m_1000ms_mean": m_1000_mean,
        "m_1000ms_std":  m_1000_std,
    }


# -----------------------------------------------------------------------------
# Endpoint 3 + 4 evaluation across the full factorial
# -----------------------------------------------------------------------------

def evaluate_e3_lambda_window(condition_results: dict) -> dict:
    """E3: identify λ_harm window where E1 + E2 both pass with rate >= 0.80."""
    lambda_windows = {}
    for init_label in INIT_HARM_MASS_LEVELS:
        for perturb_label in PERTURB_LEVELS:
            passing_lambdas = []
            for lam in LAMBDA_HARM_LEVELS:
                key = f"lam={lam}/init={init_label}/perturb={perturb_label}"
                stats = condition_results[key]
                if stats["both_pass_rate"] >= 0.80:
                    passing_lambdas.append(lam)
            window_key = f"init={init_label}/perturb={perturb_label}"
            lambda_windows[window_key] = passing_lambdas
    return lambda_windows


def evaluate_e4_robustness(condition_results: dict) -> dict:
    """E4: does (E1 + E2) hold at perturb = medium (5%)?"""
    robustness = {}
    for init_label in INIT_HARM_MASS_LEVELS:
        for lam in LAMBDA_HARM_LEVELS:
            key_med = f"lam={lam}/init={init_label}/perturb=medium"
            key_none = f"lam={lam}/init={init_label}/perturb=none"
            both_rate_med = condition_results[key_med]["both_pass_rate"]
            both_rate_none = condition_results[key_none]["both_pass_rate"]
            robust = both_rate_med >= 0.80 and both_rate_none >= 0.80
            robustness[f"lam={lam}/init={init_label}"] = {
                "robust":        robust,
                "rate_none":     both_rate_none,
                "rate_medium":   both_rate_med,
                "degradation":   both_rate_none - both_rate_med,
            }
    return robustness


# -----------------------------------------------------------------------------
# Top-level factorial loop
# -----------------------------------------------------------------------------

def run_factorial(n_seeds: int, smoke_test: bool = False) -> dict:
    """Execute the full 3 × 4 × 3 × n_seeds factorial."""
    n_cycles_actual = N_CYCLES if not smoke_test else 50  # 200 ms for smoke

    condition_index = 0
    all_runs: List[RunResult] = []
    condition_results: dict = {}

    for lam in LAMBDA_HARM_LEVELS:
        for init_label, init_frac in INIT_HARM_MASS_LEVELS.items():
            for perturb_label, perturb_sigma in PERTURB_LEVELS.items():
                condition_runs = []
                for seed_index in range(n_seeds):
                    seed = MASTER_SEED + condition_index * 1000 + seed_index
                    rng = np.random.default_rng(seed)
                    edges, rotors, _ = build_sheaf_graph(rng)
                    L0 = assemble_laplacian(edges, rotors)
                    P_ker0 = kernel_projection(L0)
                    x0 = initialise_state(P_ker0, init_frac, rng)
                    traj = integrate_dynamics(
                        x0, edges, rotors, lam, perturb_sigma, rng
                    )
                    if smoke_test:
                        traj = traj[:n_cycles_actual + 1]
                    result = evaluate_run(
                        traj, lam, init_label, init_frac,
                        perturb_label, perturb_sigma, seed,
                    )
                    condition_runs.append(result)
                    all_runs.append(result)

                key = f"lam={lam}/init={init_label}/perturb={perturb_label}"
                condition_results[key] = aggregate_condition(condition_runs)
                print(
                    f"  {key}: E1={condition_results[key]['e1_pass_rate']:.2f} "
                    f"E2={condition_results[key]['e2_pass_rate']:.2f}",
                    file=sys.stderr,
                )
                condition_index += 1

    return {
        "condition_results": condition_results,
        "e3_lambda_windows": evaluate_e3_lambda_window(condition_results),
        "e4_robustness":     evaluate_e4_robustness(condition_results),
        "n_total_runs":      len(all_runs),
    }


# -----------------------------------------------------------------------------
# Provenance + report
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


def markdown_report(results: dict) -> str:
    lines = [
        "# Phase B-1 Harmonic-Mode-Duration Simulator — Results Report",
        "",
        f"Generated: {results['provenance']['timestamp_utc']}",
        f"Git commit: `{results['provenance']['git_commit']}`",
        f"Script SHA-256: `{results['provenance']['script_sha256']}`",
        f"Total runs: {results['n_total_runs']}",
        "",
        "## E3 — λ_harm window where E1 + E2 both pass with rate ≥ 0.80",
        "",
        "```json",
        json.dumps(results["e3_lambda_windows"], indent=2),
        "```",
        "",
        "## E4 — Robustness to 5% restriction-map perturbation",
        "",
        "```json",
        json.dumps(results["e4_robustness"], indent=2),
        "```",
        "",
        "## Per-condition pass rates",
        "",
        "| Condition | E1 rate | E2 rate | Both rate |",
        "|---|---|---|---|",
    ]
    for key, stats in results["condition_results"].items():
        lines.append(
            f"| `{key}` | "
            f"{stats['e1_pass_rate']:.2f} | "
            f"{stats['e2_pass_rate']:.2f} | "
            f"{stats['both_pass_rate']:.2f} |"
        )
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase B-1 harmonic-mode-duration simulator"
    )
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-md",   required=True, type=Path)
    parser.add_argument("--n-seeds",     type=int, default=100)
    parser.add_argument("--smoke-test",  action="store_true",
                        help="Short cycles + few seeds for smoke testing")
    args = parser.parse_args(argv)

    if args.smoke_test and args.n_seeds > 5:
        args.n_seeds = 3

    print(f"Running factorial with n_seeds={args.n_seeds}, "
          f"smoke_test={args.smoke_test}", file=sys.stderr)

    results = run_factorial(args.n_seeds, args.smoke_test)
    results["provenance"] = {
        "git_commit":     _git_commit_hash(),
        "script_sha256":  _script_sha256(__file__),
        "timestamp_utc":  datetime.datetime.utcnow().isoformat() + "Z",
        "n_seeds":        args.n_seeds,
        "smoke_test":     bool(args.smoke_test),
        "master_seed":    MASTER_SEED,
        "lambda_levels":  list(LAMBDA_HARM_LEVELS),
        "init_levels":    INIT_HARM_MASS_LEVELS,
        "perturb_levels": PERTURB_LEVELS,
        "n_nodes":        N_NODES,
        "n_edges":        N_EDGES,
        "stalk_dim":      STALK_DIM,
        "dt_ms":          DT_MS,
        "t_total_ms":     T_TOTAL_MS,
        "n_cycles":       N_CYCLES,
        "e1_cycle":       E1_CYCLE,
        "e1_ratio_threshold": E1_RATIO_THRESHOLD,
        "e2_ratio_bounds":    list(E2_RATIO_BOUNDS),
    }

    args.output_json.write_text(json.dumps(results, indent=2))
    args.output_md.write_text(markdown_report(results))
    print(f"OK: wrote {args.output_json} and {args.output_md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())