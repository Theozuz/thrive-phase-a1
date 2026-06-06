# Quality-Weighted Federated Learning Spec — Stage 3 Substrate

> **Status:** Drafted May 2026 as the direct architectural consequence of [[(C)-09-Stage-Dependency-Trace-Post-MOABB-Correction]] §3 — the corrected ~67 % MOABB-published per-cycle baseline with cross-subject σ ≈ 19 pp forces explicit per-subject quality weighting in the Stage-3 federated-learning architecture. Without this, naïve FedAvg (McMahan et al., 2017) over a heterogeneous consented-user population would converge to a worse representation than any single high-quality contributor's local model.

> **Companion specs:** §6.4.5 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] (the runtime $q(t)$ signal-quality channel that this spec consumes); §7.5a of [[../07-Implementation/01-Calibration-Deployment]] (the per-subject A-0-equivalent eligibility gate that produces the calibration-time analogue of $q$); [[(C)-09-Stage-Dependency-Trace-Post-MOABB-Correction]] §3 (the architectural rationale).

---

## §1 Why Stage-3 federation requires explicit quality weighting

The implicit assumption in the pre-correction Stage-3 vision was that consented users produce roughly comparable training signal. The corrected MOABB baseline (Chevallier et al., 2024, arXiv:2404.15319 Appendix D) makes this assumption fail by design:

| Population statistic | Value | Source |
|---|---|---|
| TS+LR mean accuracy on PhysionetMI L/R MI | 67.28 % | MOABB-published |
| Cross-subject standard deviation | 19.19 pp | MOABB-published |
| Lower-tail fraction at sub-chance (< 50 %) | ≈ 16 % | Implied by Gaussian-tail of σ on mean |
| Lower-tail fraction below eligibility threshold (< 60 %) | ≈ 35 % | One σ below mean |
| Upper-tail fraction near ceiling (> 85 %) | ≈ 18 % | One σ above mean |

A naïve FedAvg update weighting all users equally would let the bottom 35 % of contributors (who are at or near chance accuracy on the foundation task) dilute the top 18 % of contributors (who are at near-ceiling accuracy) — the federated-averaging equivalent of garbage-in-garbage-out, a documented failure mode (Karimireddy et al., 2020 SCAFFOLD).

**The architectural fix is not optional.** It is the direct condition under which Stage 3's AGI-substrate vision — *"federated learning on consented human data"* — can produce a model that is better than the best individual contributor rather than worse than the average.

---

## §2 The quality-weighted federation protocol

### §2.1 Per-subject quality scalar

Each user $u$ produces a per-session time-averaged quality scalar:

$$\bar{q}_u^{(s)} = \frac{1}{T_s} \int_0^{T_s} q_u(t) \, \mathrm{d}t$$

where $q_u(t) \in [0, 1]$ is the per-cycle runtime signal-quality scalar from §6.4.5 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] and $T_s$ is the session duration. The integration is performed on-device; only the scalar $\bar{q}_u^{(s)}$ leaves the device, never the raw $q_u(t)$ trajectory.

**Calibration-time bootstrap:** for the user's first federated contribution (before any session-time $\bar{q}_u^{(s)}$ exists), the bootstrap value is the Phase 5 calibration accuracy $a_u$ from §7.5a of [[../07-Implementation/01-Calibration-Deployment]] (the per-subject A-0-equivalent). Subsequent contributions use the running exponential moving average over completed sessions.

### §2.2 Eligibility filter (hard threshold)

If $\bar{q}_u^{(s)} < q_{\mathrm{fed,min}}$, the user's contribution to the global federated update is set to **zero**. The user can still receive global model updates and use them as their local adapter prior, but their gradient is not pooled. Default: $q_{\mathrm{fed,min}} = q_{\min}^{\mathrm{Stage 1}}$ (the IVE prerequisite-gate cutoff), pre-registered at lock-in.

This is the federated-learning analogue of the Stage-2 prosthetic-command withholding rule (§7.5a of [[../07-Implementation/01-Calibration-Deployment]] §7.5a.2). Same architectural mechanism, different scale.

### §2.3 Quality weight (soft scaling)

For contributors above the eligibility threshold, the federated weight is:

$$w_u^{(s)} = \frac{f(\bar{q}_u^{(s)})}{\sum_{v \in \mathcal{U}_s} f(\bar{q}_v^{(s)})}, \quad f(\bar{q}) = \max\!\left(0, \frac{\bar{q} - q_{\mathrm{fed,min}}}{q_{\mathrm{nom}} - q_{\mathrm{fed,min}}}\right)^{\gamma}$$

where $\mathcal{U}_s$ is the set of session-$s$ eligible contributors, $q_{\mathrm{nom}}$ is the population-mean quality (initialised to 0.67 from the MOABB-published TS+LR mean, updated as session data accumulates), and $\gamma$ is the quality-emphasis exponent (default 1.0; configurable per-round). $\gamma > 1$ down-weights marginal contributors more aggressively; $\gamma = 0$ recovers uniform FedAvg.

### §2.4 The global update rule

$$\theta_{\mathrm{global}}^{(t+1)} = \theta_{\mathrm{global}}^{(t)} + \eta \sum_{u \in \mathcal{U}_s} w_u^{(s)} \, \Delta\theta_u^{(s)}$$

where $\Delta\theta_u^{(s)}$ is the user's local gradient update and $\eta$ is the server-side learning rate. Note that $\sum_u w_u^{(s)} = 1$ by construction (§2.3), so the update is a convex combination of per-user gradients — preserving the basic federated-averaging convergence properties under the standard assumptions (Karimireddy et al., 2020).

### §2.5 Tiered federation as an alternative path

When the population's $\bar{q}_u$ distribution is sharply bimodal (e.g., a deployment that mixes high-quality clinical-grade users with low-quality consumer-wearable users on different hardware), a **two-tier federation** may outperform single-tier quality weighting:

- **Tier A (high quality):** users with $\bar{q}_u \geq q_{\mathrm{tier,A}}$ contribute to a "high-quality global model" $\theta_A$
- **Tier B (low quality):** users with $\bar{q}_u \in [q_{\mathrm{fed,min}}, q_{\mathrm{tier,A}})$ contribute to a "calibration-prior model" $\theta_B$ used only to bootstrap their own local adapters

This is a configurable deployment option, not a default. The single-tier quality-weighted FedAvg of §2.4 is the default.

---

## §3 Privacy and integrity

### §3.1 What leaves the device

| Item | On-device | Transmitted to aggregator | Justification |
|---|---|---|---|
| Raw EEG | ✓ | ✗ | Never leaves the device (Tier-A on-device default per [[../09-Cybersecurity/00-Cybersecurity-Index]]) |
| Per-cycle $q_u(t)$ | ✓ | ✗ | Could reveal session-level cognitive state |
| Time-averaged $\bar{q}_u^{(s)}$ scalar | ✓ | ✓ | Single scalar per session; minimal information leakage |
| Local gradient $\Delta\theta_u^{(s)}$ | ✓ | ✓ (with quality weight) | The actual federated payload |
| Identity token | ✓ | ✗ (replaced by ephemeral session pseudonym) | Standard FL anonymisation |

### §3.2 Gradient inversion risk

Gradient inversion attacks on physiological data have been demonstrated to achieve > 92 % participant identification on retinal imaging (ScienceDirect 2025, cited in [[../09-Cybersecurity/02-Fleet-Defence-Federated-Learning]] §14.1.3). EEG's lower dimensionality may make inversion easier. This spec inherits the [[../09-Cybersecurity/02-Fleet-Defence-Federated-Learning]] three-tier options for gradient-update privacy:

1. **No federation** (most restrictive — gradient updates remain on-device)
2. **Secure-aggregation federation** (default — additive secret-sharing prevents the aggregator from seeing individual gradients)
3. **Differential-privacy federation** (alternative — Gaussian noise on gradients with calibrated $\varepsilon$-budget)

The quality-weighted aggregation of §2.4 is **compatible with all three options**. Under secure aggregation, the quality weights $w_u^{(s)}$ are computed by the aggregator from the transmitted $\bar{q}_u^{(s)}$ scalars and applied to the secret-shared gradient pieces before reconstruction — preserving the privacy guarantee.

### §3.3 PUF-binding of the quality scalar

To prevent on-device tampering with $\bar{q}_u^{(s)}$ (which could be used to spoof a higher quality weight than the user actually merits), the scalar is signed by the hardware Ethics Core's PUF key alongside the gradient payload — per the same cryptographic-integrity rule as the IVE outputs (§6.4.5 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] and §13 of [[../09-Cybersecurity/00-Cybersecurity-Index]]). The aggregator verifies the signature before applying the weight; a tampered scalar fails verification and the contribution is dropped.

---

## §4 Convergence properties

### §4.1 The good news — quality weighting preserves FedAvg convergence

The convex-combination structure of §2.4 means the convergence theorems of FedAvg under bounded gradient heterogeneity (Karimireddy et al., 2020; Li et al., 2020 *FedAvg* analysis) apply directly with the modified weights $w_u^{(s)}$. The proof requires only that the weights sum to 1 (satisfied) and that they are bounded (satisfied: $w_u^{(s)} \in [0, 1]$). The convergence rate may be slower or faster than uniform FedAvg depending on whether the quality-weighting concentrates updates on the lower-variance contributors (faster) or excludes legitimate diversity (slower).

### §4.2 The interesting question — does quality weighting reduce gradient heterogeneity?

The Karimireddy et al. (2020) SCAFFOLD analysis identifies *gradient heterogeneity* as the principal failure mode of FedAvg under non-IID data. Quality weighting addresses this empirically: if low-quality contributors produce gradients that are noisy estimates of a degraded local objective, down-weighting them reduces the effective heterogeneity seen by the aggregator. **Open empirical question:** does this reduction exceed the variance increase from non-uniform weighting? The answer depends on the population $\bar{q}_u$ distribution.

The proposed Phase A-1 H1–H10 data (109 subjects on PhysionetMI) is the natural source for an initial answer — the per-subject calibration accuracies serve as a population sample, and a simulation of quality-weighted FedAvg vs uniform FedAvg on synthetic-task gradients across that population would settle the convergence-rate question before Stage 3 deployment.

### §4.3 Topos-Institute framework lead

The compositional active inference framework (St Clere Smithe 2021, 2022; Tull, Kleiner, & St Clere Smithe 2023) provides the formal language for transferring active-learning dynamics across users — as the morphism in the category of polynomial coalgebras (see [[../10-Analysis/(C)-09-Topos-Institute-Research-Mapping]] §3.2 OQ 11.117). The quality-weighted aggregation of §2.4 is the operational instantiation of this morphism in the special case where contributors are heterogeneous in signal quality. The Classificatory Topos work (Springer 2025) on multi-agent knowledge evolution is the closest published framework for the convergence question of §4.2 above.

---

## §5 Deployment phasing

| Stage | Federation behaviour |
|---|---|
| **Stage 1 (BCI for HCI)** | No federation by default. Tier-A on-device processing per the Ethics Core's T1.3. Federation opt-in only for research-consented users, with secure aggregation. |
| **Stage 2 (prosthetics)** | Federation only for non-safety-critical model components (e.g., user-preference adapters, common UI components). Safety-critical decoders remain on-device per device-specific certification. |
| **Stage 3 (AGI substrate)** | Quality-weighted federation per §2.4 is the default mechanism for aggregating the brain-prior sheaf-geometry data that seeds the AGI internal architecture. The eligibility filter (§2.2) and quality weighting (§2.3) operate at population scale. |

The Stage-1/2 conservative defaults reflect that federation is not a Stage-1 architectural requirement — it is a Stage-3 enabler that can be exercised at Stage-1 scale only with explicit opt-in. This matches CLAUDE.md's framing: *"AGI development fed by federated learning on consented human data"* — consented being the operational word.

---

## §6 Open questions this spec creates

The Topos comparison's OQ catalogue ([[../10-Analysis/02-Open-Questions]]) gains two new entries directly from this spec (proposed for OQ catalogue addition in the next OQ-update pass):

- **OQ 11.119 (proposed)** — What is the empirical population $\bar{q}_u$ distribution under the operational quality-channel definitions of §6.4.5 of [[../04-Safety-Verification/02-Intent-Verification-Engine]]? Is it approximately Gaussian (justifying the σ-based threshold in §2.2), or sharply bimodal (justifying the tiered federation of §2.5)?
- **OQ 11.120 (proposed)** — Under the proposed §2.3 quality weighting, what is the empirical gradient-heterogeneity reduction at Stage-3-scale population sizes (≥ 10⁴ contributors)? Does it exceed the variance increase from non-uniform weighting?

These are pre-Stage-3 empirical questions whose answers determine the operational parameters of the §2.3 weighting function (the exponent $\gamma$ and the threshold $q_{\mathrm{fed,min}}$). Both are tractable in simulation using the Phase A-1 data as a population sample.

---

## §7 Cross-references

| Section | Connection |
|---|---|
| §6.4.5 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] | The runtime $q(t)$ signal-quality channel this spec consumes |
| §7.5a of [[../07-Implementation/01-Calibration-Deployment]] | The calibration-time per-subject eligibility gate; runtime analogue of $q_{\mathrm{fed,min}}$ |
| [[(C)-09-Stage-Dependency-Trace-Post-MOABB-Correction]] §3 | Architectural rationale for non-optionality of quality weighting |
| [[../09-Cybersecurity/02-Fleet-Defence-Federated-Learning]] | Privacy tier options this spec composes with |
| §13 of [[../09-Cybersecurity/00-Cybersecurity-Index]] | PUF binding of the quality scalar |
| §3 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] | Verified MOABB baseline that motivates the σ ≈ 19 pp population statistic |
| [[../10-Analysis/(C)-09-Topos-Institute-Research-Mapping]] §3.2 (OQ 11.117) | Topos framework for the categorical structure of cross-user transfer |

---

## §8 References

Karimireddy, S. P., Kale, S., Mohri, M., Reddi, S., Stich, S., & Suresh, A. T. (2020). SCAFFOLD: Stochastic controlled averaging for federated learning. *Proceedings of the 37th International Conference on Machine Learning*, 5132–5143.

Li, T., Sahu, A. K., Talwalkar, A., & Smith, V. (2020). Federated learning: Challenges, methods, and future directions. *IEEE Signal Processing Magazine*, 37(3), 50–60.

McMahan, B., Moore, E., Ramage, D., Hampson, S., & y Arcas, B. A. (2017). Communication-efficient learning of deep networks from decentralized data. *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics*, 1273–1282.

St Clere Smithe, T. (2021). Compositional active inference I: Bayesian lenses. Statistical games. *arXiv:2109.04461*.

St Clere Smithe, T. (2022). Compositional active inference II: Polynomial dynamics. Approximate inference doctrines. *arXiv:2208.12173*.

Tull, S., Kleiner, J., & St Clere Smithe, T. (2023). Compositional active inference. *arXiv:2308.00861*.

Chevallier, S., Carrara, I., Aristimunha, B., Guetschel, P., Sedlar, S., Lopes, B., Velut, S., Khazem, S., & Moreau, T. (2024). The largest EEG-based BCI reproducibility study for open science: The MOABB benchmark. *arXiv:2404.15319*.
