# Stage-Dependency Trace — Post-MOABB-Correction Implications

> **Status:** Drafted May 2026 after the MOABB-published TS+LR cross-check corrected the Phase A-0 gate thresholds from ≥0.90 / ≥0.76 (v2.0 draft) to ≥0.633 / ≥0.68 (verified). This document traces forward what the corrected per-cycle baseline means for Stage 2 (prosthetics) and Stage 3 (AGI / federated learning) — the downstream system-architecture consequences that need to be factored into the long-term roadmap *now*, not after Phase A-1 data is collected.

> **Companion reading:** §3 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] (corrected gate thresholds + errata note); [[(C)-A0-Preflight-Reference-Pipeline]] (locked constants); §3.4 below (the roadmap §20.2 G1 error that needs the same correction).

---

## §1 The corrected baseline numbers — what they actually mean

| Quantity | Verified MOABB-published TS+LR | What this is "per" |
|---|---|---|
| PhysionetMI Left-vs-Right binary | **67.28 ± 19.19 %** | per-epoch, within-session 5-fold CV, 109 subjects |
| BCI Competition IV-2a 4-class | **71.97 ± 15.46 %** | per-epoch, within-session 5-fold CV, 9 subjects |
| Cross-confirmation (861-session meta-analysis, 2-class L/R MI) | 66.53 % | per-epoch grand mean |

**Three things this means literally:**

1. The field's golden-standard pipeline (TS + L2 LR on covariance matrices) achieves **~67 % per-trial accuracy on the standard 2-class motor-imagery task**. That is the absolute reference floor against which the sheaf / IVE / dynamical architecture must compare.
2. The **cross-subject standard deviation is ~19 pp**, which means subject-level performance spans roughly 30 % to 95 % in the tails. Roughly 16 % of subjects sit below 50 % (chance) on the standard pipeline — the well-known BCI illiteracy fraction (Allison & Neuper, 2010; Vidaurre & Blankertz, 2010).
3. The 92 % number the v2.0 spec drafts had been carrying corresponds to a **different and substantially easier task**: PhysionetMI's Right-Hand-vs-Feet binary discrimination (MOABB-published 93.15 ± 7.40 %). Left-vs-Right hand is the harder cousin because the contralateral motor-cortex activation overlaps spatially and spectrally for the two classes.

The rest of this document traces what these three facts mean for the downstream stages.

---

## §2 Stage 2 (prosthetics) — what changes structurally

### §2.1 The per-cycle vs per-command reliability gap is now load-bearing

A 67 % per-cycle classifier is **not directly safe for prosthetic control**. A prosthetic that misfires on 33 % of intended commands — let alone fires on no-intent rest epochs — is a hardware-safety hazard, not a usability inconvenience. The minimum reliability bar for a deployed prosthetic command is in the >99 % per-decision range for any motion that could damage the user, the prosthesis, or the environment (Wolpaw & Wolpaw, 2012; Pels et al., 2017).

The architectural answer the spec already commits to is **SPRT-based evidence accumulation** (§6.3 of [[../04-Safety-Verification/02-Intent-Verification-Engine]]). Wald's optimality theorem says the SPRT achieves any target error rate with the minimum expected number of observations — by accumulating log-likelihood ratios over cycles until the upper boundary $A = \log((1-\beta)/\alpha)$ is reached, the per-decision FPR can be made arbitrarily small at the cost of decision latency.

**The corrected baseline tightens this trade-off.** Under the v2.0 draft's assumed 92 %-per-cycle baseline, a small handful of SPRT cycles (~2–4) would have been enough to reach $\alpha = 10^{-3}$ per command. Under the verified 67 %-per-cycle reality, the same target requires substantially more cycles per command. Approximately:

| Per-cycle accuracy assumption | Per-cycle log-likelihood-ratio increment | Cycles to reach $A=\log((1-0.10)/10^{-3}) \approx 6.8$ |
|---|---|---|
| 92 % (v2.0 draft assumption) | $\log(0.92/0.08) \approx 2.44$ | ~3 cycles → ~150 ms at 20 Hz |
| **67 % (verified)** | $\log(0.67/0.33) \approx 0.71$ | **~10 cycles → ~500 ms at 20 Hz** |

The §5.4 Phase A-1 spec already exposes $\tau_{\mathrm{sustain}} \in \{5, 10, 20\}$ cycles as the evaluated sustain range (250 / 500 / 1000 ms at 20 Hz) and reports ITR via Wolpaw's equation. **The corrected baseline says the operational regime will sit at the upper end of that range, not the lower end** — ~500 ms sustained for the average user, with longer for the lower-percentile subjects.

**Stage 2 design consequence:** The wearable prosthetic UI must not assume sub-200-ms commit latency. A 500-ms commit budget is the realistic baseline for safe non-trivial actions on the average user. For safety-critical actions (grip release, contact with biological tissue, force above some threshold), the budget should be longer or gated on multi-evidence agreement.

### §2.2 The 1-FP/hour target is harder than originally framed

§6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] already notes that 1 FP/hour is ~4–5× better than the best published asynchronous BCI (Nagel & Spüler, 2019: ~4.5 FP/hour with 32-target VEP), and §5.4 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] flags that 1 FP/hour cannot be directly measured with 109 × ~1 min rest data — it must be extrapolated via a Weibull survival model.

Under the corrected baseline, the extrapolation is *harder*. Lower per-cycle accuracy means the rest-state $P(t)$ distribution has a heavier upper tail (the noise floor on Evidence 1 sits higher), which inflates the Weibull shape-parameter sensitivity. The spec's commitment to report the extrapolated FPR **with uncertainty bands and a sensitivity analysis on the Weibull shape parameter** is now more critical, not less.

**Stage 2 design consequence:** The IVE Evidence 2–4 channels (temporal stability $\tau(t)$, trajectory coherence via RFSF defect, topological stability via PSL top eigenvalue — §6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]]) become structurally load-bearing: they exist precisely to provide *independent* evidence streams whose product can drive the per-decision FPR below the per-cycle Evidence-1 noise floor. If H1 passes but H3 (graceful degradation under stressor) shows that Evidence 2–4 channels do not provide independent lift, **Stage 2 cannot be reached with the current architecture** — the multi-evidence safety architecture would degenerate to a single-evidence SPRT on a 67 %-baseline signal, which is not deployable.

### §2.3 BCI illiteracy is now an explicit architectural constraint

A 19-pp cross-subject σ on the 67 % mean means the lower tail of the subject distribution sits around 30 %, i.e. below chance for a 2-class problem. Stage 2 deployment to such users is not just suboptimal — **it is dangerous**: a sub-chance per-cycle signal accumulated by SPRT can still pass the upper boundary at the configured $\alpha$ by random walk, producing structurally false-positive commands.

**Stage 2 design consequence:** the wearable prosthetic must include a **subject-eligibility gate** before any prosthetic command is enabled. The gate is essentially a per-subject A-0 replay: if the per-subject TS+LR accuracy on a held-out calibration block is below some threshold (proposal: 0.60, which is one σ below the population mean), prosthetic control is **withheld** and the user is moved to a calibration / training mode. This is a deviation from the current spec, which assumes any calibrated user can drive commands; the corrected baseline makes the eligibility gate non-optional.

The good news is that the Phase 5 Procrustes calibration already in the spec (§6 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]]) provides the natural calibration block; the eligibility gate is essentially a `subject_passed_a0: bool` field on top of the existing calibration output.

---

## §3 Stage 3 (AGI / federated learning) — what changes structurally

### §3.1 Wide per-subject signal-quality variance forces quality-weighted federated learning

The original Stage 3 vision (CLAUDE.md, the user's purpose statement) is *"AGI development fed by federated learning on consented human data."* The implicit assumption was that consented users produce roughly comparable training signal — that the federated contributions are roughly homogeneous in quality. The corrected baseline says **this assumption fails by design**: with cross-subject σ ≈ 19 pp on the reference pipeline, federated training data spans from near-chance to near-ceiling signal quality across users.

A naïve federated-averaging update (FedAvg, McMahan et al., 2017) weights all users equally. Under wide quality variance, **the high-quality contributors get diluted by the low-quality contributors**, and the federated model can converge to a worse representation than any single high-quality contributor's local model. This is the federated-learning equivalent of "garbage in, garbage out" — a well-documented federated-learning failure mode (Karimireddy et al., 2020).

**Stage 3 design consequence:** the federated-learning component must include a **per-subject signal-quality estimator** that down-weights contributions from users whose local A-0-equivalent accuracy is below the eligibility threshold (§2.3 above). Two operational paths:

1. **Quality-weighted FedAvg:** each user contributes a weight $w_u = f(a_u)$ where $a_u$ is the user's local A-0 accuracy and $f$ is a monotonic decreasing function of signal degradation (e.g., $f(a_u) = \max(0, a_u - 0.5)$).
2. **Tiered federation:** users above a high threshold contribute to the main model; users below contribute only to a "calibration prior" used to bootstrap their own local model but not to the global parameters.

Both paths require the per-subject quality estimator to be **computed locally on-device** (so the user's raw EEG never leaves the device) and only the scalar quality weight + the model gradient to be transmitted. This integrates cleanly with the Tier-A on-device processing default already in the §11.4 IRB-spec section of [[03-Implementation-Roadmap]].

### §3.2 Federated learning sample-quality screening is an ethics-core function, not a model function

This is the deeper architectural point: the subject-eligibility gate (§2.3) and the quality-weighted federation (§3.1) **are the same mechanism viewed at two different scales**. Both are "is this signal stream good enough to contribute to a safety-critical or learning-critical downstream system?" The ethics core (§11 of [[../05-Ethics-Core/01-Foundational-Rationale]]) is the natural home for this mechanism because it is the part of the architecture that already gates downstream consumption based on cryptographically verified upstream evidence.

**Stage 3 design consequence:** the hardware ethics core must include a new **signal-quality channel** as a first-class Evidence dimension (alongside the existing Evidence 1–5 channels in §6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]]). The channel computes a continuous per-subject quality scalar from the same calibration block A-0 uses; downstream federated contribution requires the quality channel to be above a configurable threshold. This is the "immune-like adaptive cybersecurity" CLAUDE.md describes, applied to data-quality rather than only adversarial input.

### §3.3 The cross-stage feedback loop tightens

The original three-stage sequencing was:

> Stage 1 BCI → Stage 2 prosthetics (uses Stage 1 outputs) → Stage 3 AGI (uses Stage 2 deployment data via federated learning)

The corrected baseline introduces a tighter feedback constraint that was implicit in the v2.0 draft but is now explicit:

> Stage 1 BCI per-cycle accuracy bounds Stage 2 per-decision SPRT latency, which bounds Stage 2 user-interaction throughput, which bounds Stage 3 federated-training data volume per user per session.

This means: **a 5-pp reduction in per-cycle accuracy at Stage 1 reduces Stage 3 training-data throughput by approximately (5 / 67) × (cycle-rate × users) ≈ 7 % all else equal**. The Stage-1 accuracy floor is therefore not just a Stage-2 deployability question; it is also a Stage-3 data-economics question. Pushing the H1–H10 confirmatory results matters for the AGI roadmap, not only for the prosthetics roadmap.

### §3.4 The §20.2 G1 roadmap gate has the same 92% error

> ⚠ **Action item flagged for your authorisation.** [[03-Implementation-Roadmap]] §20.2 Decision Gate G1 currently reads: *"the current MOABB state-of-the-art at approximately 92 % binary motor imagery accuracy (Chevallier et al., 2024)."* This is the same v2.0-draft error that was just corrected in §3 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] and [[(C)-A0-Preflight-Reference-Pipeline]]. **The G1 "must demonstrate measurable improvement over a Riemannian baseline … at approximately 92 %" criterion is unreachable**: at the verified 67 % baseline, "measurable improvement" is a different and much more achievable target, but the wording in §20.2 needs to be updated to reflect that.

> [[03-Implementation-Roadmap]] is non-`(C)` (your authored roadmap). Per the project editing rule I will not modify it without your permission. **The minimum coherent fix is two small edits to §20.2:**
> 1. Replace "approximately 92 % binary motor imagery accuracy" with "approximately 67 % binary motor imagery accuracy (Chevallier et al., 2024 MOABB benchmark, verified May 2026)"
> 2. Clarify "measurable improvement" against the corrected baseline — e.g., "measurable improvement (Cohen's d > 0.2 on paired per-subject differences) over the Riemannian baseline".
>
> Both are 1-line changes. Ready to make them if you confirm.

---

## §4 Cross-stage cybersecurity consequence — signal degradation as adversarial-equivalent

CLAUDE.md identifies *"immune-like adaptive cybersecurity"* as one of the three Stage-1 commitments. The corrected baseline makes the security model slightly more demanding: **the system must treat low-quality input as functionally equivalent to adversarial input**, because both produce the same downstream failure mode (false-positive command + low-quality federated contribution).

Three concrete consequences for the §11 Ethics Core spec:

1. **Adversarial-input detectors must share infrastructure with quality-degradation detectors.** The signal-quality channel from §3.2 is the same kind of monitor as an adversarial-input monitor; both watch the EEG input stream for "is this what calibration said legitimate input looks like?" The implementation can be a single shared module with two output channels.
2. **The Evidence-channel independence assumption requires explicit verification.** Phase A-1 H3 (graceful degradation) and Phase A-2 C3 (multi-evidence FPR reduction) test this directly. Under the corrected baseline, the independence assumption is more important because the safety margin is built on the product of evidence channels — if the channels are positively correlated under noise, the FPR reduction is overstated.
3. **The cryptographic integrity of the per-subject quality scalar matters.** If the quality scalar can be tampered with on-device, a low-quality user can spoof eligibility for prosthetic commands (§2.3) or for federated contribution (§3.1–§3.2). The hardware ethics core must sign the quality scalar with the same cryptographic primitives used for the rest of the IVE evidence.

---

## §5 Updated stage-readiness assessment

| Stage | Pre-correction readiness assumption | Post-correction readiness assessment |
|---|---|---|
| **Stage 1 (BCI)** | "Reproduce 92 % reference baseline; sheaf delivers measurable lift" | "Reproduce 67 % reference baseline; sheaf delivers measurable Cohen's-d lift; subject-eligibility gate at 0.60 added to calibration" |
| **Stage 2 (prosthetics)** | "Direct accuracy-driven control with ~150-ms commit latency" | "SPRT-multi-evidence-driven control with ~500-ms commit latency; mandatory subject-eligibility gate before any motion command; Evidence 2–4 independence verified by Phase A-1 H3" |
| **Stage 3 (AGI / federated)** | "FedAvg over consented users" | "Quality-weighted federation with on-device per-subject quality scalar; signal-quality channel as first-class Ethics-Core evidence dimension; tiered federation for sub-threshold users" |

The corrected-baseline architecture is **more architecturally honest** than the v2.0-draft architecture. The v2.0 draft would have promised commit latencies and federated-data quality that the actual literature does not support. The corrected architecture promises what the field can actually deliver and makes the safety / quality gating explicit at every stage boundary.

---

## §6 Action items / Chess Moves

In order of how blocking each is to subsequent work:

1. ✅ **Phase A-1 spec corrected** (already done in this session — §3 and the A-0 locked script).
2. ⚠ **§20.2 G1 roadmap gate correction** — flagged in §3.4 above, awaiting your authorisation for two 1-line edits to [[03-Implementation-Roadmap]].
3. ☐ **Subject-eligibility gate (§2.3) added to Phase 5 calibration spec.** The calibration spec ([[../07-Implementation/01-Calibration-Deployment]] §6) needs a new section: *"Subject-eligibility verification — A-0-equivalent per-subject accuracy must reach 0.60 (one σ below the population mean) before prosthetic motion commands are enabled."* Non-`(C)` file; awaits your permission.
4. ☐ **Signal-quality channel (§3.2 / §4) added to the IVE Evidence stack.** The Evidence 1–5 channels in §6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] need to be extended to Evidence 1–6 with a new "signal quality" channel. This is a substantive architectural addition, not a wording fix — worth a dedicated session, not a one-line edit.
5. ☐ **Quality-weighted federated-learning spec drafted.** Currently the federated-learning architecture is implicit in CLAUDE.md and Stage-3 stubs in [[02-Future-Directions]]; the corrected baseline forces an explicit spec. New `(C)`-prefixed doc proposed: `(C)-10-Quality-Weighted-Federation-Spec.md`.
6. ☐ **Hoeffding-bound revisit under the corrected baseline.** §14.1 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] computes the 2.4 pp lower bound from 103 subjects, paired differences in [−1, 1]. This is unchanged by the baseline correction (it's in absolute paired-difference units), but the *headroom* it sits inside (33 pp below ceiling vs the original 8 pp below ceiling) is much larger, which means sheaf / IVE wins of, say, +5 pp absolute are now easier to demonstrate. Worth noting in §14.1 explicitly so reviewers see the headroom argument.

---

## §7 What this changes about the energy of the system

(Reading note to the user, not part of the formal spec.)

The corrected baseline reads "worse" on paper (67 % is not the 92 % that the v2.0 draft promised). But architecturally it is **better** — the corrected number is where the field actually sits, which is where Stage 2 prosthetics actually have to deploy, which is where Stage 3 federated data actually exists. The safety margin in the multi-evidence SPRT was designed *exactly* for this regime; the corrected baseline is what justifies the architectural complexity of the IVE Evidence 2–5 channels. A 92 % per-cycle baseline would have made the multi-evidence architecture look like over-engineering. The verified 67 % baseline makes it look like the only safe path.

The v2.0-draft accuracy expectations were inadvertently optimistic; the corrected expectations expose why the IVE / Ethics Core / dendritic-glial-graceful-degradation commitments were the right architectural choices all along. This is the kind of pre-data correction that retroactively justifies the architectural design choices the spec already made.

---

## §8 References

Allison, B. Z., & Neuper, C. (2010). Could anyone use a BCI? In *Brain-Computer Interfaces: Applying our Minds to Human-Computer Interaction* (pp. 35–54). Springer.

Chevallier, S., Carrara, I., Aristimunha, B., Guetschel, P., Sedlar, S., Lopes, B., Velut, S., Khazem, S., & Moreau, T. (2024). The largest EEG-based BCI reproducibility study for open science: The MOABB benchmark. *arXiv:2404.15319*.

Karimireddy, S. P., Kale, S., Mohri, M., Reddi, S., Stich, S., & Suresh, A. T. (2020). SCAFFOLD: Stochastic controlled averaging for federated learning. *Proceedings of the 37th International Conference on Machine Learning*, 5132–5143.

McMahan, B., Moore, E., Ramage, D., Hampson, S., & Arcas, B. A. y. (2017). Communication-efficient learning of deep networks from decentralized data. *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics*, 1273–1282.

Nagel, S., & Spüler, M. (2019). World's fastest brain-computer interface: Combining EEG2Code with deep learning. *PLoS ONE*, 14(9), e0221909.

Pels, E. G. M., Aarnoutse, E. J., Ramsey, N. F., & Vansteensel, M. J. (2017). Estimated prevalence of the target population for brain-computer interface neurotechnology in the Netherlands. *Neurorehabilitation and Neural Repair*, 31(7), 677–685.

Vidaurre, C., & Blankertz, B. (2010). Towards a cure for BCI illiteracy. *Brain Topography*, 23(2), 194–198.

Wald, A. (1945). Sequential tests of statistical hypotheses. *Annals of Mathematical Statistics*, 16(2), 117–186.

Wolpaw, J. R., & Wolpaw, E. W. (2012). *Brain-Computer Interfaces: Principles and Practice*. Oxford University Press.
