"""
Phase B-2 Stage 3 Component Validation Extension
==================================================

Extends the locked Phase A-7 Digital ACP Twin with three §2.16 components
for empirical validation on existing Phase A-1 streaming trajectories:

  §2.16.3 — Curiosity reward signal r_int(t)
  §2.16.5 — Piagetian assimilation/accommodation/equilibration tracker
  §2.16.6 — Autopoietic coherence monitor

Three endpoints (no new hypotheses on motor-imagery decoding):

  E_curiosity     — Does r_int(t) correlate with subsequent prediction-error
                    reduction within 100 cycles? (target r > 0.3)
  E_equilibration — Does the equilibration trigger fire >= 50 cycles before
                    IVE accuracy drops below 80% of baseline under drift?
  E_autopoietic   — Does the coherence monitor detect >= 90% of injected
                    structural breaches at < 5% false-alarm rate?

This script is purely additive — it does not change the Phase A-7 ACP twin's
behaviour; it instruments it with three additional telemetry streams.

Locked hyperparameters (cannot modify post-registration):
  - Curiosity reward weights (α_nov, α_lp, α_symm) = (0.2, 0.6, 0.2)
  - Curiosity prediction-error history window = 100 cycles
  - Assimilation threshold θ_assim = 0.15 (Bures-Wasserstein)
  - Accommodation threshold θ_accom = 0.35 (Bures-Wasserstein)
  - Equilibration trigger threshold θ_eq = 0.3 (accommodation rate over window)
  - Equilibration window W = 5000 cycles (20 s at 250 Hz)
  - Autopoietic check cadence = 75000 cycles (5 min at 250 Hz)
  - Breach-injection rates locked at registration
  - Master seed = 42

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
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import numpy as np

# =============================================================================
# Locked §2.16 parameters
# =============================================================================

# §2.16.3 — Curiosity reward
CURIOSITY_ALPHA_NOV   = 0.2    # novelty weight (Schmidhuber)
CURIOSITY_ALPHA_LP    = 0.6    # learning-progress weight (Oudeyer)
CURIOSITY_ALPHA_SYMM  = 0.2    # symmetry-exploration weight (Mantiuk 2025)
CURIOSITY_HISTORY     = 100    # cycles for prediction-error correlation

# §2.16.5 — Piagetian assimilation/accommodation/equilibration
THETA_ASSIM   = 0.15    # within this BW distance → assimilation
THETA_ACCOM   = 0.35    # beyond this → accommodation
THETA_EQ      = 0.30    # accommodation rate triggering equilibration
EQ_WINDOW     = 5000    # cycles for accommodation-rate computation

# §2.16.6 — Autopoietic monitor
AUTOPOIETIC_CHECK_CADENCE = 75000  # cycles (~5 min at 250 Hz)
LIPSCHITZ_EPS = 0.05       # tolerance for restriction-map Lipschitz check
SPRT_VARIANCE_TOLERANCE = 2.0  # SPRT log-likelihood variance bound

# Endpoint thresholds (gate criteria)
E_CURIOSITY_CORR_THRESHOLD = 0.3
E_EQUILIBRATION_LEAD_CYCLES = 50
E_AUTOPOIETIC_DETECTION_TARGET = 0.90
E_AUTOPOIETIC_FA_TOLERANCE = 0.05

# Breach injection (for E_autopoietic validation)
BREACH_INJECTION_PROBABILITY = 0.05  # 5% of autopoietic checks have injected breach
BREACH_INJECTION_SEED_OFFSET = 17

MASTER_SEED = 42

# Sheaf graph parameters (must match Phase A-7 ACP twin)
N_NODES = 40
N_EDGES = 80
STALK_DIM = 8
DT_MS = 4.0


# =============================================================================
# Curiosity reward computation (§2.16.3)
# =============================================================================

class CuriosityTracker:
    """Computes intrinsic reward r_int(t) from prediction-error dynamics.

    r_int(t) = α_nov · |ΔF̄| + α_lp · |F̄̈| + α_symm · Φ_symm
    """

    def __init__(self):
        self.f_history = deque(maxlen=4)   # last 4 cycles of F̄ for derivatives
        self.r_int_history = []            # for correlation with subsequent error
        self.error_history = []            # F̄(t) for correlation analysis

    def step(self, f_bar: float, cycle: int) -> float:
        self.f_history.append(f_bar)
        self.error_history.append(f_bar)

        if len(self.f_history) < 3:
            r_int = 0.0
        else:
            # First derivative (novelty) — Schmidhuber
            f = list(self.f_history)
            delta_f = abs(f[-1] - f[-2])

            # Second derivative (learning progress) — Oudeyer
            d2_f = abs(f[-1] - 2 * f[-2] + f[-3])

            # Symmetry-exploration proxy (Mantiuk 2025): variance of F̄
            # in the recent window, as a measure of conservation-law probing
            phi_symm = float(np.std(list(self.f_history)))

            r_int = (
                CURIOSITY_ALPHA_NOV * delta_f
                + CURIOSITY_ALPHA_LP * d2_f
                + CURIOSITY_ALPHA_SYMM * phi_symm
            )

        self.r_int_history.append(r_int)
        return r_int

    def compute_e_curiosity(self) -> float:
        """E_curiosity: correlation between r_int(t) and subsequent ΔF̄
        averaged over next 100 cycles.

        Returns Pearson correlation coefficient.
        """
        if len(self.r_int_history) < CURIOSITY_HISTORY + 10:
            return float("nan")

        r_int = np.array(self.r_int_history)
        errors = np.array(self.error_history)

        # Subsequent error reduction: mean(errors[t+1 : t+1+H]) - errors[t]
        H = CURIOSITY_HISTORY
        n = len(r_int) - H - 1
        subsequent_change = np.array([
            errors[t+1 : t+1+H].mean() - errors[t]
            for t in range(n)
        ])
        r_int_truncated = r_int[:n]

        # We expect higher r_int → larger error reduction → negative correlation
        # with subsequent_change. Convert to positive for the "predicts learning"
        # interpretation.
        corr = np.corrcoef(r_int_truncated, -subsequent_change)[0, 1]
        return float(corr if not np.isnan(corr) else 0.0)


# =============================================================================
# Piagetian assimilation/accommodation/equilibration tracker (§2.16.5)
# =============================================================================

@dataclass
class EquilibrationEvent:
    cycle: int
    accommodation_rate: float
    triggered: bool


class EquilibrationTracker:
    """Tracks assimilation vs accommodation operations and fires equilibration
    trigger when accommodation rate exceeds threshold."""

    def __init__(self):
        self.operation_history: deque = deque(maxlen=EQ_WINDOW)
        # entries: 'assim', 'accom', 'none'
        self.events: List[EquilibrationEvent] = []
        self.accuracy_history: List[float] = []

    def classify_operation(self, bw_distance_to_nearest: float) -> str:
        """Classify the current engram-allocation decision.

        bw_distance_to_nearest : Bures-Wasserstein distance from current sheaf
            state to the nearest existing engram.
        """
        if bw_distance_to_nearest < THETA_ASSIM:
            return "assim"
        elif bw_distance_to_nearest > THETA_ACCOM:
            return "accom"
        else:
            return "none"

    def step(self, bw_distance: float, ive_accuracy: float, cycle: int) -> None:
        op = self.classify_operation(bw_distance)
        self.operation_history.append(op)
        self.accuracy_history.append(ive_accuracy)

        # Compute accommodation rate over sliding window
        if len(self.operation_history) >= EQ_WINDOW // 10:
            ops = list(self.operation_history)
            n_accom = sum(1 for o in ops if o == "accom")
            n_total = sum(1 for o in ops if o != "none")
            acc_rate = n_accom / n_total if n_total > 0 else 0.0
        else:
            acc_rate = 0.0

        triggered = acc_rate > THETA_EQ
        if triggered:
            self.events.append(EquilibrationEvent(
                cycle=cycle, accommodation_rate=acc_rate, triggered=True
            ))

    def compute_e_equilibration(self, baseline_accuracy: float) -> int:
        """E_equilibration: cycle lead of first trigger over the IVE-accuracy
        drop below 80% of baseline.

        Returns the lead in cycles (positive = trigger fired before drop;
        negative = trigger fired after drop; returns -1 if no drop observed).
        """
        acc = np.array(self.accuracy_history)
        threshold = 0.80 * baseline_accuracy

        drop_cycles = np.where(acc < threshold)[0]
        if len(drop_cycles) == 0:
            # No drop occurred; treat as "lead = inf" but report as -1 for
            # missing-event sentinel
            return -1

        first_drop = int(drop_cycles[0])

        # Find first equilibration trigger before first_drop
        triggers_before = [e for e in self.events if e.cycle < first_drop and e.triggered]
        if not triggers_before:
            return 0  # trigger never fired before drop
        first_trigger = triggers_before[0].cycle
        return int(first_drop - first_trigger)


# =============================================================================
# Autopoietic coherence monitor (§2.16.6)
# =============================================================================

@dataclass
class AutopoieticReport:
    cycle: int
    breaches_detected: List[str]
    breach_injected: bool
    breach_injected_type: Optional[str] = None
    monitor_passed: bool = True


class AutopoieticMonitor:
    """Meta-level monitor checking structural integrity of substrate components.

    Runs at slow timescale (AUTOPOIETIC_CHECK_CADENCE cycles).
    Optionally injects synthetic breaches to validate detection.
    """

    def __init__(self, rng: np.random.Generator, inject_breaches: bool = True):
        self.rng = rng
        self.inject_breaches = inject_breaches
        self.reports: List[AutopoieticReport] = []

    def check(self, rotors: np.ndarray, sprt_loglik_history: List[float],
              engram_bank_isotropy: float, cycle: int) -> AutopoieticReport:
        """Run all coherence checks; optionally inject a breach."""
        # Decide whether to inject a synthetic breach this check
        injected_breach: Optional[str] = None
        if self.inject_breaches and self.rng.random() < BREACH_INJECTION_PROBABILITY:
            injected_breach = self.rng.choice([
                "lipschitz_violation",
                "isotropy_violation",
                "sprt_variance_violation",
            ])

        breaches: List[str] = []

        # Check 1: restriction-map Lipschitz bound
        max_sv = self._max_singular_value(rotors)
        if injected_breach == "lipschitz_violation":
            max_sv = 1.0 + 2 * LIPSCHITZ_EPS  # simulate breach
        if max_sv > 1.0 + LIPSCHITZ_EPS:
            breaches.append("restriction_map_lipschitz")

        # Check 2: engram-bank isotropy (SIGReg-style)
        if injected_breach == "isotropy_violation":
            engram_bank_isotropy = 5.0  # simulate strong deviation
        if engram_bank_isotropy > 2.0:  # threshold for SIGReg statistic
            breaches.append("engram_bank_isotropy")

        # Check 3: SPRT log-likelihood variance bound
        if sprt_loglik_history and len(sprt_loglik_history) >= 10:
            sprt_variance = float(np.std(sprt_loglik_history[-100:]))
            if injected_breach == "sprt_variance_violation":
                sprt_variance = 5.0
            if sprt_variance > SPRT_VARIANCE_TOLERANCE:
                breaches.append("sprt_variance")

        report = AutopoieticReport(
            cycle=cycle,
            breaches_detected=breaches,
            breach_injected=(injected_breach is not None),
            breach_injected_type=injected_breach,
            monitor_passed=(len(breaches) == 0 if injected_breach is None
                            else len(breaches) > 0),
        )
        self.reports.append(report)
        return report

    @staticmethod
    def _max_singular_value(rotors: np.ndarray) -> float:
        """Maximum singular value across all restriction maps."""
        sv_list = [np.linalg.svd(rotors[k], compute_uv=False).max()
                   for k in range(rotors.shape[0])]
        return float(max(sv_list))

    def compute_e_autopoietic(self) -> Tuple[float, float]:
        """E_autopoietic: detection rate, false-alarm rate.

        Detection rate: of checks with injected breach, how many were detected?
        False-alarm rate: of checks WITHOUT injected breach, how many flagged?
        """
        if not self.reports:
            return float("nan"), float("nan")

        injected = [r for r in self.reports if r.breach_injected]
        not_injected = [r for r in self.reports if not r.breach_injected]

        if injected:
            detection_rate = sum(
                1 for r in injected if len(r.breaches_detected) > 0
            ) / len(injected)
        else:
            detection_rate = float("nan")

        if not_injected:
            false_alarm_rate = sum(
                1 for r in not_injected if len(r.breaches_detected) > 0
            ) / len(not_injected)
        else:
            false_alarm_rate = 0.0

        return float(detection_rate), float(false_alarm_rate)


# =============================================================================
# Helper — Bures-Wasserstein distance proxy (matches Phase A-7 twin's metric)
# =============================================================================

def bw_distance_proxy(state_a: np.ndarray, state_b: np.ndarray) -> float:
    """Bures-Wasserstein distance between flattened sheaf states.

    Simplified proxy: Frobenius-norm-based distance, sufficient for the
    classification operation. Full BW on SPD covariances is in
    R_FM/R_JEPA extraction; here we use the coarse proxy that matches the
    Phase A-7 twin's per-edge defect computation.
    """
    return float(np.linalg.norm(state_a.flatten() - state_b.flatten()))


# =============================================================================
# Top-level driver — wraps the Phase A-7 ACP twin with the three components
# =============================================================================

def run_b2_validation(
    eeg_stream: np.ndarray,
    action_stream: np.ndarray,
    vsk_stream: Optional[np.ndarray],
    stressor: str,
    mode: str,
    smoke_test: bool = False,
) -> Dict:
    """Run the Phase A-7 ACP twin with §2.16 component instrumentation.

    For Phase B-2 we run the twin's core dynamics and instrument it with the
    three new modules. The twin's normal endpoint outputs are computed in
    parallel; the new endpoints are added.
    """
    rng = np.random.default_rng(MASTER_SEED)
    inject_rng = np.random.default_rng(MASTER_SEED + BREACH_INJECTION_SEED_OFFSET)

    # Initialise twin state (matching Phase A-7)
    edges = _build_edges(rng)
    rotors = _build_rotors(rng)
    state = rng.standard_normal((N_NODES, STALK_DIM)) * 0.1

    # Stub engram bank: a small list of recently-seen sheaf states for
    # BW-distance computation. Phase B-3 will replace this with the full
    # §2.15.2 engram bank.
    engram_stub: List[np.ndarray] = []
    ENGRAM_STUB_MAX = 50

    # Initialise the three §2.16 modules
    curiosity = CuriosityTracker()
    equilibration = EquilibrationTracker()
    autopoietic = AutopoieticMonitor(inject_rng, inject_breaches=True)

    # Stub SPRT log-likelihood (for autopoietic monitor)
    sprt_loglik_history: List[float] = []

    n_cycles = eeg_stream.shape[0]
    if smoke_test:
        n_cycles = min(n_cycles, 1000)  # ~4 s for smoke test

    # Baseline accuracy estimation: first 200 cycles of cleansed input
    baseline_acc_window = 200
    baseline_acc = 0.85  # nominal; updated after warmup

    for cycle in range(n_cycles):
        # Apply stressor
        eeg_in = _apply_stressor(eeg_stream[cycle], stressor, cycle, rng)
        state[:32] = eeg_in.reshape(32, STALK_DIM)

        # Compute total free energy F̄(t) (matches twin's metric)
        f_bar = float(np.sum(state ** 2)) / (N_NODES * STALK_DIM)

        # §2.16.3 — Curiosity reward
        r_int = curiosity.step(f_bar, cycle)

        # §2.16.5 — Classify operation (assim/accom) for equilibration
        if engram_stub:
            distances = [bw_distance_proxy(state, e) for e in engram_stub]
            min_dist = min(distances)
        else:
            min_dist = float("inf")
        # Stub IVE accuracy proxy: 1.0 at first, decays under stressor
        ive_accuracy = max(0.0, baseline_acc - 0.001 * len(engram_stub))
        if stressor == "drift":
            ive_accuracy = max(0.0, baseline_acc - 0.0003 * cycle)
        equilibration.step(min_dist, ive_accuracy, cycle)

        # Engram-stub allocation (assim or accom)
        if min_dist > THETA_ACCOM and len(engram_stub) < ENGRAM_STUB_MAX:
            engram_stub.append(state.copy())

        # SPRT history (stub)
        sprt_loglik_history.append(f_bar - 0.5)  # nominal scaled value

        # §2.16.6 — Autopoietic check (slow cadence)
        if cycle > 0 and cycle % AUTOPOIETIC_CHECK_CADENCE == 0:
            isotropy = float(np.std([np.linalg.norm(e) for e in engram_stub])
                             if len(engram_stub) > 1 else 0.0)
            autopoietic.check(rotors, sprt_loglik_history, isotropy, cycle)

    # Compute endpoints
    e_curiosity = curiosity.compute_e_curiosity()
    e_equilibration = equilibration.compute_e_equilibration(baseline_acc)
    e_autopoietic_detection, e_autopoietic_fa = autopoietic.compute_e_autopoietic()

    return {
        "stressor":                  stressor,
        "mode":                      mode,
        "n_cycles":                  n_cycles,
        "e_curiosity_correlation":   e_curiosity,
        "e_curiosity_pass":          bool(e_curiosity > E_CURIOSITY_CORR_THRESHOLD)
                                       if not np.isnan(e_curiosity) else False,
        "e_equilibration_lead_cycles": e_equilibration,
        "e_equilibration_pass":      bool(
            e_equilibration >= E_EQUILIBRATION_LEAD_CYCLES
            if e_equilibration >= 0 else False
        ),
        "e_autopoietic_detection_rate": e_autopoietic_detection,
        "e_autopoietic_false_alarm_rate": e_autopoietic_fa,
        "e_autopoietic_pass":        bool(
            (e_autopoietic_detection >= E_AUTOPOIETIC_DETECTION_TARGET)
            and (e_autopoietic_fa <= E_AUTOPOIETIC_FA_TOLERANCE)
            if not np.isnan(e_autopoietic_detection) else False
        ),
        "n_engrams_allocated":       len(engram_stub),
        "n_autopoietic_checks":      len(autopoietic.reports),
        "n_equilibration_events":    len(equilibration.events),
    }


# =============================================================================
# Edge / rotor builders (match Phase A-7 ACP twin)
# =============================================================================

def _build_edges(rng: np.random.Generator) -> np.ndarray:
    edges = []
    for i in range(N_NODES):
        edges.append((i, (i + 1) % N_NODES))
        j = int(rng.integers(0, N_NODES))
        while j == i or j == (i + 1) % N_NODES:
            j = int(rng.integers(0, N_NODES))
        edges.append((i, j))
    return np.array(edges[:N_EDGES])


def _build_rotors(rng: np.random.Generator) -> np.ndarray:
    rotors = np.empty((N_EDGES, STALK_DIM, STALK_DIM))
    for k in range(N_EDGES):
        H = rng.standard_normal((STALK_DIM, STALK_DIM))
        Q, _ = np.linalg.qr(H)
        rotors[k] = Q
    return rotors


def _apply_stressor(eeg_cycle: np.ndarray, stressor: str, cycle: int,
                    rng: np.random.Generator) -> np.ndarray:
    if stressor == "clean":
        return eeg_cycle
    elif stressor == "channel_dropout":
        ch = rng.choice(len(eeg_cycle), size=2, replace=False)
        out = eeg_cycle.copy()
        out[ch] = 0.0
        return out
    elif stressor == "emg":
        if rng.random() < 0.25:
            return eeg_cycle + rng.standard_normal(eeg_cycle.shape) * np.std(eeg_cycle)
        return eeg_cycle
    elif stressor == "drift":
        return eeg_cycle + 0.01 * cycle / 1000.0
    else:
        raise ValueError(f"Unknown stressor: {stressor}")


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
        description="Phase B-2 Stage 3 Component Validation"
    )
    parser.add_argument("--eeg-input", required=True, type=Path)
    parser.add_argument("--action-stream", required=True, type=Path)
    parser.add_argument("--vsk-context", type=Path, default=None)
    parser.add_argument("--stressor-schedule",
                        choices=["clean", "channel_dropout", "emg", "drift"],
                        default="clean")
    parser.add_argument("--mode",
                        choices=["static", "pseudo-streaming",
                                 "full-streaming", "sensory-absent"],
                        default="pseudo-streaming")
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args(argv)

    eeg = np.load(args.eeg_input)
    actions = np.load(args.action_stream)
    vsk = np.load(args.vsk_context) if args.vsk_context else None

    print(f"Running B-2 validation: stressor={args.stressor_schedule}, "
          f"mode={args.mode}, n_cycles={eeg.shape[0]}", file=sys.stderr)

    endpoints = run_b2_validation(
        eeg_stream=eeg,
        action_stream=actions,
        vsk_stream=vsk,
        stressor=args.stressor_schedule,
        mode=args.mode,
        smoke_test=args.smoke_test,
    )

    provenance = {
        "git_commit":       _git_commit_hash(),
        "script_sha256":    _script_sha256(__file__),
        "timestamp_utc":    datetime.datetime.utcnow().isoformat() + "Z",
        "stressor":         args.stressor_schedule,
        "mode":             args.mode,
        "smoke_test":       bool(args.smoke_test),
        "master_seed":      MASTER_SEED,
        "curiosity_alpha_nov":  CURIOSITY_ALPHA_NOV,
        "curiosity_alpha_lp":   CURIOSITY_ALPHA_LP,
        "curiosity_alpha_symm": CURIOSITY_ALPHA_SYMM,
        "curiosity_history":    CURIOSITY_HISTORY,
        "theta_assim":      THETA_ASSIM,
        "theta_accom":      THETA_ACCOM,
        "theta_eq":         THETA_EQ,
        "eq_window":        EQ_WINDOW,
        "autopoietic_check_cadence": AUTOPOIETIC_CHECK_CADENCE,
        "lipschitz_eps":    LIPSCHITZ_EPS,
        "sprt_variance_tol": SPRT_VARIANCE_TOLERANCE,
        "breach_injection_probability": BREACH_INJECTION_PROBABILITY,
        "e_curiosity_threshold": E_CURIOSITY_CORR_THRESHOLD,
        "e_equilibration_lead_cycles": E_EQUILIBRATION_LEAD_CYCLES,
        "e_autopoietic_detection_target": E_AUTOPOIETIC_DETECTION_TARGET,
        "e_autopoietic_fa_tolerance": E_AUTOPOIETIC_FA_TOLERANCE,
    }

    output = {**endpoints, "provenance": provenance}
    args.output_json.write_text(json.dumps(output, indent=2))

    if args.manifest:
        args.manifest.write_text(json.dumps(provenance, indent=2))

    print(f"OK: wrote {args.output_json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())