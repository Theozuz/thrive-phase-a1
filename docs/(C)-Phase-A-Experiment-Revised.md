# thrIVE Phase A — Falsification Experiment (Revised)

## Sheaf-Coherence Value-Proposition Test on Motor Imagery EEG

**Version:** 2.0 (revision of [[Phase A Experiment Proposal]] v1.0)
**Date:** April 2026
**Author:** Claude (under direction of Theo Cognat, thrIVE PI)
**Status:** Pre-registration draft — awaiting OSF submission before data touches
**Companion:** Retains original [[Phase A Experiment Proposal]] as historical record

---

## §0 Pre-Experimental Verification (1 hour, on paper)

Before executing any compute, verify the foundational theorem this experiment tests:

**Theorem (Seely et al., 2025, arXiv:2511.11092).** The predictive-coding energy functional is identical to the sheaf Laplacian quadratic form:

$$E_{\mathrm{PC}}(\mathbf{x}) = \mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}$$

**Verification task:** Re-derive this from the Rao–Ballard (1999) prediction-error formulation using the restriction-map decomposition $\mathcal{F}_{u \triangleleft e} = P_{u \to e} \Gamma_{u \to v}$ (§2.1.3 of [[../02-Theory/02-Cellular-Sheaves-SPD-Manifolds]]). Note any qualifications (orthogonality, directedness, stalk-dimension homogeneity) that restrict the equivalence.

**If the equivalence holds only under additional assumptions**, the experiment must be interpreted within those assumptions. If the equivalence cannot be derived, the experiment tests an empirical correlation between predictive-coding-like objectives and sheaf coherence, not the theoretical equivalence itself.

> **§0 status — completed May 2026.** The §0 verification task is closed by [[../02-Theory/(C)-16-Seely-Equivalence-Independent-Derivation]], which provides two independent derivations of the equivalence — an algebraic route from Rao–Ballard (1999) using the spec's $\mathcal{F}_{u \triangleleft e} = P_{u \to e} \Gamma_{u \to v}$ decomposition (§3 of that document), and a categorical route from St Clere Smithe (2023, Oxford DPhil thesis Chapters 3–4) via Bayesian-lens autoencoder games (§4 of that document). The two routes agree under five shared qualifications (linear restriction maps, Gaussian likelihood, orthogonal $\Gamma$, surjective row-orthonormal $P$, homogeneous stalks); all five are satisfied **by construction** or **by explicit modelling commitment** for the Phase A-1 architecture. The equivalence therefore holds **exactly** for Phase A-1; the experiment tests its empirical consequences on real EEG, not the theoretical equivalence itself.

---

## §1 The Nine Load-Bearing Claims

thrIVE's architectural viability depends on nine independent empirical claims. Phase A falsifies or validates each in turn. Claims C1–C5 are Stage 1 critical; C6 enables sensory-anchored deployment; C7 is the Stage 2.5 entry-point claim that earns the first piece of the developmental cogitation substrate (§2.14) a Phase B implementation slot; C8 grounds the IVE consciousness-access claims of §2.15.9 in empirical psychophysics. **C9 tests the dynamical architecture (separate from representational priors) and is the most architecturally consequential claim after C1**: it can fail independently of C1–C5, in which case the *control-system* part of thrIVE earns its keep but the *representational* part may not, or vice versa. Phase A-7's outcome is therefore as central to the architectural decision as Phase A-1's.

**Pre-registration coverage of these claims:** the OSF preregistration ([[(C)-OSF-Preregistration-Phase-A1]]) covers C1–C4 in §3 (H1–H3), C8 implicitly via §9.5 H4, sheaf-vs-end-to-end via §10 H5, and C9 (dynamical architecture) via §11 Amendment 3 (H6 vs LeWM + H7 vs mainstream ensemble + optional H8 §2.16 component validation). See the amendment summary table in §2 of the OSF preregistration for the full Amendment 1 / 2 / 3 mapping to hypothesis identifiers, locked artefacts, and gate criteria.

| # | Claim | Spec anchor | Failure consequence |
|---|-------|-------------|---------------------|
| **C1** | Unsupervised TTSA on the predictive-coding energy (Seely et al., 2025) learns restriction maps that produce discriminable sheaf coherence on real EEG | §2.4 of [[../02-Theory/04-Additional-Theory]]; §15.2 of [[../06-Prediction/01-Prediction-Engine-Architecture]] | Whole architecture fails; abandon sheaf layer |
| **C2** | The sheaf layer recovers task-relevant information lost by d=8 eigenvalue channel selection | §8.2 of [[../07-Implementation/02-Real-Time-Pipeline]] | Channel selection is a net loss; redesign stalk reduction |
| **C3** | Multi-evidence IVE fusion strictly reduces FPR at matched TPR compared to single-evidence | §6.3–6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] | IVE safety story is empty; simplify to single-evidence |
| **C4** | Sheaf coherence degrades gracefully under channel dropout and artefact injection, more so than Riemannian tangent | §4.5.5 of [[../03-Architecture/02-Cellular-Sheaf-Architecture]] | Graceful-degradation claim is rhetoric; rewrite §4.5.5 |
| **C5** | Session-to-session transfer via Riemannian Procrustes alignment (Rodrigues et al., 2019) restores sheaf performance within 5 minutes of calibration | §7.7 of [[../07-Implementation/01-Calibration-Deployment]] | Calibration-free claim fails; Stage 2 prosthetics infeasible |
| **C6** | Sensory-anchored inhibition (M1 divisive normalisation, M2 sensory-priority precision, M3 hallucination suppression) reduces sensory-absent FPR and bounds internal prediction drift | §6 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]] | Per-mechanism gates permit partial validation — failing mechanisms disabled at deployment, not whole framework rejected |
| **C7** | U-node path-usage tracking and per-command threshold $\theta_{\mathrm{IVE}}(c)$ accelerate authorisation of practised commands without inflating FPR for rare or risky commands | §2.14.5 + §2.14.7 of [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]] | E2 minority-FPR gate is a safety override; sub-package A (Habit Acceleration) earns Phase B implementation only if both speed and safety gates pass |
| **C8** | Sheaf coherence $\mathcal{C}(t)$ and sustained-activity duration $\tau_{\mathrm{sustain}}$ track empirical conscious-access thresholds derived from backward-masking psychophysics | §7.7 of this document; §2.15.9 of [[../02-Theory/(C)-14-Representational-Substrate-Engrams-Cognitive-Maps-Slots]] | Converts IVE parameters from calibration knobs to empirically grounded psychophysical boundaries — Phase A-9 outcome |
| **C9** | thrIVE's dynamical architecture (multi-timescale TTSA + SPRT IVE + hyperdirect pathway + sensory-anchored inhibition + THINK mode) confers measurable streaming-mode advantages over LeWM-style end-to-end JEPA — specifically: faster streaming-mode authorisation, faster stressor recovery, stable sensory-absent behaviour, cross-modal evidence convergence, lower energy per command, sub-event-latency safety stop | §7.7a of this document; §2.13–§2.14 of theory | Tests the dynamical-architecture claims that Phase A-1's static-classification arm cannot test. (✓, ✗) outcomes are diagnostic: representational and dynamical justifications can pass or fail independently |

These nine claims are **independent** — any may fail without falsifying the others. The decision tree (§9) handles each outcome.

---

## §2 Phase Structure

Seven phases, each pre-registered, each gating the next. Phases A-5 and A-6 run in parallel with A-3 and A-4.

| Phase | Duration | Tests | Gate outcome |
|---|---|---|---|
| **A-0** Preflight | 3 days | Pipeline reproduces published Riemannian baseline | Proceed only if within 2 pp of benchmark |
| **A-1** Sheaf Core Factorial | 2 weeks | C1, C2, C4 in one factorial experiment | Proceed only if C1 passes |
| **A-2** IVE Evidence Integration | 1 week | C3 (FPR reduction via multi-evidence) | Proceed only if additive FPR reduction observed |
| **A-3** Cross-Session Transfer | 1 week | C5 (Lee et al. 2019 session 1 → session 2) | Informs Stage 2 feasibility |
| **A-4** Hardware Quantisation | 3 days | FPGA bit-width engineering input | Informs [[../08-Hardware/02-Analogue-Compute-Plane]] §9.2.4 |
| **A-5** Sensory-Anchored Inhibition | 2 days (parallel) | C6 (3×4×2 factorial on §6 mechanisms; E1–E4 endpoints) | Permits per-mechanism activation in deployment |
| **A-6** U-Node Reflexive Acceleration | 3 days (parallel) | C7 (2×3×4 factorial; E1–E4 endpoints, incl. minority-FPR safety gate) | Promotes sub-package A from Stage 2.5 candidate to Phase B target |
| **A-7** Continuous-Time Dynamical Comparison (Digital ACP Twin vs streaming R_JEPA) | ~3 weeks software development + ~1 week simulation (no human subjects) | C9 (slimmed to 6 endpoints E1′/E2/E3′/E4/E6/E7′ after literature audit; tests thrIVE-specific composite mechanisms only) | Tests whether thrIVE's dynamical architecture confers measurable streaming-mode advantages over LeWM-style end-to-end JEPA. Software builds on Brian2 / NEST infrastructure rather than from scratch |
| **A-7′** Comparison against BCI Mainstream Baselines (recommended hardest test) | ~1 week additional after A-7 | C9′ (32-condition factorial vs SPRT-Liu + TSFNet + T-TIME + ST-EEGFormer ensemble) | The architecturally honest test: does thrIVE's composite beat the *ensemble of mainstream BCI methods* that thrIVE would actually replace if deployed? Higher-stakes than A-7 vs LeWM |
| **A-9** $\tau_{\mathrm{sustain}}$ + Sheaf-Coherence-Threshold Calibration (psychophysics) | ~3 months post-A-6 (IRB + recruit + record + analysis) | C8 (40-subject backward-masking paradigm; E1–E4 endpoints; empirical conscious-access thresholds) | Converts IVE threshold parameters from arbitrary calibration values to empirically grounded psychophysical thresholds |
| **A-10** Ethics Core Constraint Logic Simulation | 2 days (parallel with A-2) | Verify CVB constraint table and assembly-risk scoring against Phase A-1 outputs | Software simulation only — no hardware required. See OQ 14.3 |
| **B-1** Harmonic-Mode-Duration Simulation (pre-validation) | ~36 hours wall-clock (no human subjects) | OQ 11.106 (3×4×3 simulation factorial; E1–E4 endpoints, no real-data inferences) | Validates THINK-mode deployability before any Stage 2.5 commitment |
| **B-2** §2.16 Stage 3 Component Validation (optional, Amendment 3c) | ~1 week wall-clock as extension of Phase A-7 ACP twin | OQ 11.112–11.114, 11.116 (E_curiosity / E_equilibration / E_autopoietic on existing Phase A-1 streaming data) | Empirically validates 3 of 5 §2.16 active-learning components (curiosity reward + equilibration trigger + autopoietic monitor) without new data collection. Phase B-3 (closed-loop synthetic environment for X-nodes + action-conditioned map) is separate deliverable |

Total core Phase A: 6 weeks. Phase A-9 follow-up: +3 months (IRB required). Phase B-1 simulation: parallel with any of the above; ~36 hours wall-clock.

---

## §3 Phase A-0 — Preflight

**Purpose:** Confirm the reference pipeline before testing any novel claim.

**Datasets:**
- PhysioNet EEGMMIDB (Schalk et al., 2004) — use the curated version of Varbu et al. (2024) to correct known annotation errors
- BCI Competition IV Dataset 2a (Brunner et al., 2008) — 9 subjects, 4-class MI, cleaner labels

**Pipeline:** MOABB framework (Chevallier et al., 2024) — register thrIVE pipelines as MOABB entries to inherit pseudo-online evaluation and paired comparisons.

**Method:**
1. Riemannian TangentSpace + L2-regularised logistic regression, d = 32 covariance
2. 5-fold stratified within-subject CV (for matching published results)

**Gate criterion (corrected May 2026 after MOABB cross-check):** Binary L/R MI on PhysionetMI within **4 pp of 67.28%** (Chevallier et al. 2024 published TS+LR), i.e. **grand-average ≥ 0.633**; 4-class MI on BCI Competition IV-2a within **4 pp of 71.97%** (same source), i.e. **grand-average ≥ 0.68**. If not reproduced, **halt and repair pipeline** — novel claims cannot be tested against a broken reference.

**Tolerance derivation.** MOABB-published TS+LR has cross-subject σ ≈ 19 pp on PhysionetMI (109 subjects) and σ ≈ 15 pp on BCI IV-2a (9 subjects). The 4-pp tolerance is one σ/5 of the published cross-subject distribution — tight enough to detect a real pipeline error, loose enough that legitimate cross-subject variance does not unconditionally fail the gate. The original 2 pp tolerance from the v2.0 draft assumed σ ≈ 5 pp; the published σ values make 2 pp operationally infeasible.

**v2.0-draft errata (resolved May 2026 before OSF lock).** Earlier drafts of §3 cited "92% MOABB published" for PhysionetMI binary MI and "78% MOABB published" for BCI IV-2a 4-class. The 92% number was a spec-side error: it matches the MOABB-published **Right-Hand-vs-Feet** binary paradigm on PhysionetMI (93.15 ± 7.40%), not the Left-vs-Right binary paradigm that §4.1 actually uses (67.28 ± 19.19%). The 78% number for BCI IV-2a 4-class was 6 pp above the MOABB-published TS+LR value of 71.97%. Both errors are corrected in the gate criterion above; the corrected values are taken directly from the [MOABB official benchmark results page](https://moabb.neurotechx.com/docs/paper_results.html) and Chevallier et al. (2024) arXiv:2404.15319 Appendix D, Tables 6–10. The error was caught by the A-0 pre-lock verification step and is documented here per OSF "what counts as a deviation" transparency requirement.

**Locked artefact:** [[(C)-A0-Preflight-Reference-Pipeline]] — the operational implementation of this preflight. The script encodes the corrected gate thresholds (≥0.633 PhysionetMI L/R binary, ≥0.68 BCI IV-2a 4-class) as locked constants, emits a SHA-256 manifest matching the sibling locked-script pattern, and writes a structured pass/fail JSON. **A-0 is the load-bearing entry gate** for the entire Phase A-1 programme: if either dataset fails the gate, no H1–H10 result is interpretable until the reference pipeline is repaired.

---

## §4 Phase A-1 — Sheaf Core Factorial (Critical Test)

**Purpose:** Simultaneous test of C1, C2, C4 in a 5 × 4 within-subject factorial design.

### §4.1 Design

| **Factor 1: Representation** | | **Factor 2: Stressor** | |
|---|---|---|---|
| R32 | Riemannian tangent at d = 32 (ceiling) | S0 | Clean data |
| R8 | Riemannian tangent at d = 8 (channel-selected) | S1 | 2 of 32 channels randomly nulled per epoch |
| S-rand | Sheaf coherence, random orthogonal restriction maps (10 seeds, averaged) | S2 | Synthetic EMG contamination at 0 dB SNR on 25% of epochs |
| S-TTSA | Sheaf coherence, **unsupervised** TTSA-learned restriction maps | S3 | Leave-one-subject-out (generalisation) |
| R8+S | Concatenated R8 tangent features + S-TTSA coherence, logistic regression | | |

5 × 4 = 20 conditions per subject. 109 subjects → 2,180 paired observations.

**Pre-registration amendment under consideration (OQ 11.81, see §7.7a of [[../07-Implementation/01-Calibration-Deployment]]):** add a sixth representation level

| Level | Definition |
|---|---|
| R_FM | Frozen features from a pretrained EEG foundation model (ST-EEGFormer or LCM) projected to d = 8 |

with corresponding factorial extensions R_FM+S (foundation model + S-TTSA sheaf coherence). This adds 2 × 4 = 8 new conditions per subject, raising the total from 2,180 to ~3,050 paired observations. The Hoeffding detectability bound (§14.1) is unaffected; only the number of factor levels changes. The amendment must be submitted to OSF **before any data is touched** to remain pre-registered. Without it, Phase A-1 tests the sheaf layer only against a 2023-era baseline (R8), not against the actual state of the field (R_FM).

**Second pre-registration amendment under consideration (OQ 11.109):** add a seventh representation level

| Level | Definition |
|---|---|
| R_JEPA | LeWM-style end-to-end encoder + predictor with SIGReg regularisation, trained jointly on the same calibration data, output projected to d = 8 |

with corresponding factorial extension R_JEPA+S (LeWM-style JEPA + S-TTSA sheaf coherence). This tests the strongest possible claim that the sheaf structure earns its empirical keep: $(R8 + S) > R_{\mathrm{JEPA}}$ would demonstrate that the structured architecture outperforms a minimal-prior end-to-end alternative on the same task. Conversely, if $R_{\mathrm{JEPA}} \geq (R8 + S)$, the sheaf structure does not earn its complexity for this task and §2.1–§2.13 commitments would need to be re-evaluated. This is the **hard architectural test** — pre-registration must commit to it before data is touched. Adds 2 × 4 = 8 new conditions, raising the total to ~3,920 paired observations.

The two amendments together produce an eight-level Factor 1 (R32, R8, S-rand, S-TTSA, R8+S, R_FM, R_FM+S, R_JEPA, R_JEPA+S) — 9 levels actually — with the same four-level Factor 2 (stressors), totalling 36 conditions per subject. The Hoeffding detectability bound is unaffected by the level count.

**Third pre-registration amendment under consideration (OQ — domain-specific JEPA baseline; §12 of [[(C)-OSF-Preregistration-Phase-A1]] Amendment 4):** add an eleventh and twelfth representation level

| Level | Definition |
|---|---|
| R_JEPA_brain | Brain-JEPA / Signal-JEPA-inspired end-to-end JEPA with spatial / channel-wise masking and per-channel-group pre-local processing, output projected to d = 8 via per-fold PCA |
| R_JEPA_brain+S | Concatenated R_JEPA_brain features + S-TTSA sheaf coherence, logistic regression |

This is the **domain-appropriate JEPA baseline** complementing the existing cross-domain R_JEPA (LeWM). Tests the H9 hypothesis: (R8 + S) > R_JEPA_brain. **A harder test than H5** because the comparator is now a JEPA architecture designed for EEG specifically, not adapted from vision. Adds 2 × 4 = 8 new conditions, raising the total to ~4,792 paired observations. The Hoeffding detectability bound remains unaffected. Implemented in [[(C)-R_JEPA-Brain-Feature-Extraction]].

**Fourth pre-registration amendment under consideration (§13 of [[(C)-OSF-Preregistration-Phase-A1]] Amendment 5 — cohomology-isolation test):** add a thirteenth and fourteenth representation level

| Level | Definition |
|---|---|
| R_GL | Top-16 graph-Laplacian eigenmode spectral features on the **same 40-node Yeo-17-scale topology as the sheaf**, with identity restriction maps and scalar (mean signal-energy) per-node projections, output projected to d = 8 via per-fold PCA |
| R_GL+S | Concatenated R_GL features + S-TTSA sheaf coherence, logistic regression |

This is the **controlled single-variable test** of whether cellular cohomology — not just graph topology — earns empirical value. R_GL uses identical topology to the sheaf but with no rotor-valued restriction maps and no higher cohomology. Tests the H10 hypothesis: (R8 + S) > R_GL. If H10 fails, the §2.1.5 + §2.1.6 cohomological structure is empirically decorative for the Phase A-1 motor-imagery task and the sheaf can be replaced by graph-Laplacian features for Stage 1. Adds 2 × 4 = 8 new conditions, raising the total to ~5,664 paired observations. Hoeffding detectability unaffected. Implemented in [[(C)-R_GL-Feature-Extraction]].

### §4.2 Critical Design Fixes (vs. v1.0)

**Fix 1 — Unsupervised TTSA objective.** The S-TTSA condition uses **no class labels**. The learning objective is the predictive-coding energy of Seely et al. (2025):

$$L_{\mathrm{TTSA}}(\theta) = \mathbb{E}_t \left[\mathbf{x}(t)^\top L_{\mathcal{F}(\theta)} \mathbf{x}(t)\right] + \lambda_{\mathrm{Lip}} \max\!\left(0, \sigma_{\max}(\mathcal{F}(\theta)) - 1\right)^2$$

computed over **all epochs mixed** (rest + left-MI + right-MI, no class distinction). The Lipschitz regularisation enforces the §2.4 stability constraint from [[../02-Theory/04-Additional-Theory]]. After TTSA convergence, restriction maps are frozen; post-hoc logistic regression on `C(t)` measures discriminability.

This honestly tests the spec's claim: does unsupervised energy minimisation — the actual TTSA mechanism — produce coherence that separates MI classes as a side-effect of learning the sheaf structure?

**Fix 2 — Procrustes stalk alignment.** Before constructing stalks, align per-epoch eigenvector bases to a session reference via Riemannian Procrustes (Rodrigues, Jutten, & Congedo, 2019):

1. Compute the session Fréchet mean covariance $\bar{C}_{\mathrm{session}}$ on the calibration set
2. Eigendecompose to obtain reference basis $U_{\mathrm{ref}}$
3. For each epoch's covariance $C_i$, compute orthogonal alignment $Q_i = \arg\min_Q \|U_i Q - U_{\mathrm{ref}}\|_F^2$
4. Apply $Q_i$ to the top-8 eigenvector block before stalk construction

Without this fix, the experiment will fail for reasons orthogonal to sheaf theory — eigenvector drift, not architectural merit.

**Fix 3 — Factorial stressor conditions.** S1 (channel dropout) tests §4.5.5 null propagation directly. S2 (EMG injection) tests IVE Evidence 1 robustness. S3 (LOSO) tests generalisation. Stressor × representation interaction is the C4 test.

The stressor levels are not arbitrary perturbations — each is the literature-standard probe for a distinct failure mode that has been quantitatively documented in BCI-EEG and motor-imagery decoding:

- **S1 (random channel nulling, 2 of 32 channels per epoch).** Channel-availability degradation is the canonical robustness probe for motor-imagery decoders. The dropout-perturbation protocol used here matches the channel-dropout regularisation / robustness benchmark recently formalised for MI-EEG by Gómez-Morales et al. (2025) and the broader channel-reduction literature operationalised by Khanam et al. (2025). The 2/32 magnitude is calibrated to fall inside the "degraded but recoverable" regime documented in those studies (substantially larger dropout rates push baseline decoders into hard-fail territory on Lee et al. (2019)), which is exactly the range where graceful-degradation claims are operationally testable.
- **S2 (synthetic EMG contamination at 0 dB SNR on 25% of epochs).** The 0 dB SNR target is the standard worst-case contamination level used by EMG-removal benchmarks because cranial-muscle EMG and beta/mu-band MI activity overlap spectrally above ~20 Hz, with quantitative evidence from paralysis recordings (Whitham et al., 2007) and the canonical MEG/EEG-EMG review by Muthukumaraswamy (2013). The 25% epoch-injection rate matches the contamination prevalence regime where Artifact Subspace Reconstruction (Mullen et al., 2015) — the current production-grade EEG artefact-suppression standard — begins to show measurable residual leakage. A representation that claims robustness must hold up against this exact level, not against milder synthetic noise.
- **S3 (Leave-One-Subject-Out generalisation).** LOSO is the only honest test of subject-transfer in motor-imagery BCI: within-subject cross-validation overstates generalisation by 10–30 percentage points relative to LOSO performance on the same data, as documented by the canonical transfer-learning analyses of Jayaram et al. (2016) and the 2016-onward review by Wu et al. (2022). The Phase A-1 LOSO protocol is the directly comparable benchmark to the MOABB pseudo-online framework (Carrara & Aristimunha, 2023; Chevallier et al., 2024) already adopted for the rest of the pipeline.

Together, these three stressors cover the three documented failure modes of motor-imagery BCIs in production (sensor failure, muscle contamination, subject drift) at the literature-standard severity for each. The C4 representation × stressor interaction test is therefore an interaction against the field's accepted robustness rubric, not a soft synthetic check.

**Fix 4 — Data-driven graph topology (secondary ablation).** Three topologies tested:

| Topology | Construction | Rationale |
|----------|--------------|-----------|
| Physical | Euclidean distance < 40 mm between electrodes | Baseline (current v1.0) |
| Functional | Phase-locking value (PLV) > 0.4 in mu band | Standard BCI connectivity |
| SCGL | Di Nino, Barbarossa, & Di Lorenzo (2025) learned topology | Production method |

SCGL is the method the spec will use in production; the other two are controls. An edge-permutation null (shuffle edges, retrain) tests whether topology carries discriminative information at all.

### §4.3 Statistical Model

Linear mixed-effects model:

```
accuracy ~ representation * stressor + (1 | subject) + (1 | dataset)
```

- **Primary endpoint:** S-TTSA vs. S-rand at S0 (C1), paired BF₁₀ > 3 via BEST (Kruschke, 2013)
- **Secondary endpoints:**
  - (R8 + S) vs. R8 at S0 (C2), paired Cohen's d > 0.2, one-sided α = 0.05
  - Representation × stressor interaction (C4), F-test α = 0.05
  - Pairwise comparisons via Holm-Bonferroni within hypothesis families (see below)

> **Family structure for multiple comparisons (June 2026).** To control family-wise error rate without excessive conservatism, tests are grouped into three pre-registered families:
>
> | Family | Hypotheses | Approximate tests | Adjusted α |
> |---|---|---|---|
> | **F1: Core sheaf benefit** | H1–H3 (primary) | ~12 | Holm-Bonferroni within family, α/12 ≈ 0.004 |
> | **F2: Timescale ablation** | H4–H7 | ~16 | Holm-Bonferroni within family, α/16 ≈ 0.003 |
> | **F3: Configuration comparison** | H8–H10 | ~12 | Holm-Bonferroni within family, α/12 ≈ 0.004 |
>
> Each family controls its own family-wise error rate at 0.05. Cross-family claims (e.g., "the best configuration from F3 also shows the largest sheaf benefit in F1") require a global Bonferroni correction across all ~40 tests.

**Power analysis (G*Power 3.1):** With 109 subjects × 20 conditions, detectable effect at 80% power α = 0.05 is Cohen's d = 0.12 for within-subject contrasts. Well below the 0.3–0.5 effect range typical of BCI paradigm comparisons.

**Effect-size invariance under the May 2026 baseline correction.** All H1–H10 strength criteria use Cohen's *d* computed on **paired per-subject differences**, which is scale-invariant with respect to the absolute baseline accuracy: $d = \mathrm{mean}(\Delta_i) / \mathrm{SD}(\Delta_i)$. The criteria (d > 0.2 for H2 / H4 / H5 / H9 / H10; d > 0.3 for H6 / H7 endpoints; BF₁₀ > 3 for H1; rmANOVA F-test for C4) are therefore **unaffected** by the corrected gate threshold of ~67% / ~72% versus the original draft's 92% / 78% assumption. The detection sensitivity of each paired test is the same. The one second-order qualification: paired-difference SD may be somewhat larger at a mid-range baseline (~67%) than at a near-ceiling baseline (~92%) because there is more cross-subject variance at the middle of the accuracy distribution than near the ceiling. If the typical paired-difference SD is ~0.08 instead of the original assumption of ~0.05, the G*Power minimum detectable absolute paired difference becomes ~1 pp rather than ~0.6 pp — still well below the typical 3–5 pp BCI paradigm-comparison range, so the design remains overpowered under both regimes. The Hoeffding distribution-free bound of 2.4 pp (§14.1) is in absolute units and is also unaffected.

**Pre-registered null-safe reporting:** If S-TTSA ≤ S-rand (C1 fails), report the BF₁₀ and effect size; do not re-analyse. If S-TTSA beats S-rand but loses to R8, that is the honest verdict — report it.

### §4.4 Gate Criteria (Pre-Registered)

| Claim | Quantitative criterion | Action if fails |
|-------|------------------------|-----------------|
| **C1** | S-TTSA > S-rand at S0, BF₁₀ > 3 | **Halt experiment.** Sheaf layer has no value on real EEG. Return to Riemannian-only architecture. Publish the null result. |
| **C2** | (R8 + S) > R8 at S0, paired d > 0.2 | Downgrade sheaf to auxiliary signal for IVE only; do not use as primary feature |
| **C4** | Representation × stressor interaction significant (F-test), S-TTSA loses less accuracy than R8 from S0 → {S1, S2} | IVE's graceful-degradation claim is unsupported. Rewrite §4.5.5 of [[../03-Architecture/02-Cellular-Sheaf-Architecture]] |

---

## §5 Phase A-2 — IVE Evidence Integration

**Purpose:** Test C3 — does multi-evidence fusion strictly reduce FPR at matched TPR?

**Precondition:** Only run if C1 passes in Phase A-1.

### §5.1 Evidence Stack

Using frozen restriction maps from A-1's S-TTSA condition, construct the IVE evidence stack incrementally:

| Level | Evidence dimensions | Computation |
|-------|--------------------|-----|
| IVE-1 | $C(t)$ alone | §6.4 Evidence 1 |
| IVE-2 | + temporal stability $\tau(t)$ | §6.4 Evidence 2 |
| IVE-3 | + trajectory coherence (RFSF defect, D = 50) | §6.4 Evidence 3 |
| IVE-4 | + topological stability (PSL top eigenvalue, ε = 0.3) | §6.4 Evidence 4 |

Evidence 5 (cross-modal) is not applicable offline; fix to constant 1.0 and note the limitation.

### §5.2 Multiplicative Fusion and SPRT

Per §6.3 of [[../04-Safety-Verification/02-Intent-Verification-Engine]]:

$$P(t) = w_0 \prod_{i=1}^{k} \sigma\!\left(\kappa_i(\mathrm{raw}_i(t) - \theta_i)\right)$$

where $k \in \{1, 2, 3, 4\}$ indexes the evidence level, $\theta_i, \kappa_i$ are calibrated on the training set.

SPRT log-evidence accumulation (Wald, 1945) with:
- $H_0$: no intent; $H_1$: intent present
- $\alpha_{\mathrm{target}} \in \{10^{-2}, 10^{-3}, 10^{-4}, 10^{-5}\}$ per cycle (corresponding to 72, 7.2, 0.72, 0.072 FP/hour at 20 Hz)
- $\beta_{\mathrm{target}} = 0.10$

### §5.3 Metrics

- **Primary:** ROC curves with bootstrap 95% CIs (1,000 resamples) for each IVE level
- **Key contrast:** IVE-4 vs. IVE-1 — 95% CI of FPR at matched TPR must not overlap zero difference
- **ITR (Wolpaw et al., 2002):**

$$\mathrm{ITR} = \frac{60}{T_{\mathrm{decision}}} \left[\log_2 N + p \log_2 p + (1 - p) \log_2 \frac{1 - p}{N - 1}\right]$$

reported at $\tau_{\mathrm{sustain}} \in \{5, 10, 20\}$ cycles (250, 500, 1000 ms).

### §5.4 FPR Extrapolation (Honest Version)

The 1/hour FPR target cannot be directly measured with 109 × ~1 min of rest data. Report:

1. **Measurable FPR** at each $\tau_{\mathrm{sustain}}$ with 95% CI
2. **Parametric extrapolation:** fit a Weibull survival model to the continuous $P(t)$ during rest epochs; extrapolate to the 1/hour tail
3. **Sensitivity analysis:** how does extrapolated FPR depend on the Weibull shape parameter assumption?

Report both numbers. Do not assert 1 FP/hour as measured.

### §5.5 Gate Criterion

IVE-4 strictly lower FPR than IVE-1 at matched TPR, 95% CI non-overlap. If evidence dimensions do not stack, multi-evidence fusion adds no value → simplify spec to single-evidence.

---

## §6 Phase A-3 — Cross-Session Transfer (C5)

**Purpose:** Test whether Phase 5 Procrustes calibration (Rodrigues et al., 2019) delivers returning-user calibration < 5 min.

**Dataset:** Lee et al. (2019) MI dataset — 54 subjects, two sessions per subject, recorded several days apart. Currently the only open dataset with controlled session-to-session design.

### §6.1 Conditions

| Condition | Method |
|-----------|--------|
| **Cold start** | Session 2: full TTSA from random init (baseline upper bound on calibration time) |
| **Procrustes** | Session 2: Riemannian Procrustes alignment of session-1 restriction maps, no retraining |
| **T-TIME** | Session 2: Wu et al. (2024) test-time entropy minimisation from session-1 init |
| **Full recal** | Session 2: full TTSA from session-1 init (warm start) |

### §6.2 Metric

**Calibration time to competence:** minutes of session-2 data required to reach within 3 pp of cold-start session-2 final accuracy.

### §6.3 Gate Criterion

Procrustes or T-TIME reaches target in < 5 minutes. If not, §7.7 of [[../07-Implementation/01-Calibration-Deployment]] requires revision; Stage 2 commercial viability takes a hit.

---

## §7 Phase A-4 — Hardware Quantisation

**Purpose:** Inform FPGA bit-width selection before Phase B, not a scientific gate.

### §7.1 Method

Using frozen restriction maps from A-1, quantise and re-evaluate classification accuracy:

| Bit-width | Rationale | Reference |
|-----------|-----------|-----------|
| FP32 | Ground truth | Software baseline |
| 14-bit | Song et al. (2024) dual-subarray RRAM | §9.2.4 of [[../08-Hardware/02-Analogue-Compute-Plane]] |
| 8-bit | Standard ADC output | MSB spec |
| 4-bit | Single-subarray RRAM (pre-Song) | Worst-case analogue |

Report ΔAccuracy vs. FP32 at each level. No gate — results inform the crossbar bit-width decision in §9.2.4.

### §7.2 Additional Quantisation Ablations

- **Restriction map quantisation only** (stalks at FP32) — isolates crossbar precision
- **Stalk quantisation only** (maps at FP32) — isolates ADC precision
- **Joint quantisation** — realistic deployment

---

## §7.5 Phase A-5 — Sensory-Anchored Inhibition Validation

**Purpose:** Test claim C6 — that the three sensory-anchored inhibition mechanisms (§6 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]]) improve sheaf-coherence reliability under sensory-rich conditions *and* prevent prediction drift under sensory-absent conditions.

**Precondition:** Only run if C1 passes in Phase A-1 *and* the sensory-anchored inhibition is enabled in the deployment configuration. The mechanisms are software-only on the DCE; runtime cost is ~600 FLOP/cycle (< 0.5% of core pipeline).

### §7.5.1 The Three Mechanisms Under Test

The mechanisms specified in §6 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]]:

| Mechanism | Active component | Predicted effect |
|-----------|------------------|------------------|
| **M1** — Divisive normalisation | Per-edge defect normalisation by local population activity | Sensory anomalies become *relative* — strong sensory signals divisively suppress internal noise |
| **M2** — Sensory-priority precision | $\pi_{\mathrm{sensory}}$ factor in P-module | Sensory-edge precision boosted up to ~3× when reliable; N-to-N suppressed to ~0.5× |
| **M3** — Hallucination suppression | Quadratic damping on deep tier when $\bar{S} < S_{\min}$ | Internal predictions cannot drift to arbitrary values in sensory absence |

### §7.5.2 Experimental Design

**3 × 4 × 2 within-subject factorial** on the 103 retained PhysioNet EEGMMIDB subjects (Phase A-1 cohort), augmented with synthetic V/S/K signals at controlled SNR levels.

| **Factor 1: Sensory regime** | | **Factor 2: Inhibition configuration** | | **Factor 3: Anomaly injection** | |
|---|---|---|---|---|---|
| **PRESENT** | V/S/K-nodes receive synthetic signals at SNR ∈ [5, 10] | **OFF** | v5.4 baseline — no §6 mechanisms active | **NO** | No internal perturbation |
| **DEGRADED** | V/S/K-nodes at SNR ∈ [1, 2] (noisy but present) | **DN_ONLY** | Only divisive normalisation active | **YES** | Synthetic hallucination-like internal stalk perturbation injected at random intervals |
| **ABSENT** | V/S/K-nodes nulled (sensory deprivation simulation) | **PRIORITY_ONLY** | Only $\pi_{\mathrm{sensory}}$ active |
| | | **FULL** | All three M1+M2+M3 mechanisms active |

3 × 4 × 2 = 24 conditions per subject × 103 subjects × 5 folds = 12,360 paired observations.

### §7.5.3 Synthetic Sensory Signal Generation

Synthetic V/S/K signals are generated to match the spectral and temporal statistics of real recordings:

- **V-nodes:** synthetic Gabor responses to random scene content, scaled to target SNR via additive Gaussian noise calibrated against the spectral profile of typical environment-camera images.
- **S-nodes:** synthetic mel-spaced spectral and modulation covariances drawn from a Gaussian mixture model fit to ambient office acoustic recordings (publicly available from the AudioSet corpus, Gemmeke et al. 2017).
- **K-nodes:** synthetic 6-DOF head pose covariances drawn from a Gaussian mixture model fit to seated-user pose recordings (public CMU MoCap subset).

The synthetic signals are time-locked to the EEG trial structure so that "sensory-present" conditions provide realistic cross-modal coupling. All signal generation parameters are fixed pre-registration; seed values are logged.

### §7.5.4 Hallucination Injection Protocol

When **anomaly injection = YES**, random deep-tier stalk perturbations are added at 5% of epochs to simulate the "internal prediction drift" the suppression mechanism is designed to prevent:

$$d_a^{\mathrm{perturbed}}(t) = d_a(t) + \xi_a(t)$$

where $\xi_a(t)$ is a smoothly-varying perturbation with amplitude $\sim 2 \sigma_d$ ($\sigma_d$ being the calibrated standard deviation of the deep-tier dynamics during quiet rest). The injection mimics what unconstrained hallucinatory drift would look like; the suppression mechanism should counteract it under sensory-absent conditions.

### §7.5.5 Primary Endpoints

**E1 (Primary) — Sensory-absent FPR reduction.** Under (sensory = ABSENT, anomaly = YES) conditions, does the **FULL** inhibition configuration produce a lower IVE false-positive rate than **OFF**? Paired comparison, BF₁₀ > 3 via BEST.

$$\mathrm{FPR}_{\mathrm{OFF}}^{\mathrm{ABSENT, YES}} - \mathrm{FPR}_{\mathrm{FULL}}^{\mathrm{ABSENT, YES}} \geq 0.30 \cdot \mathrm{FPR}_{\mathrm{OFF}}^{\mathrm{ABSENT, YES}}$$

A 30% relative reduction in sensory-absent FPR is the gate criterion.

**E2 (Secondary) — Sensory dominance ratio.** Under (sensory = PRESENT, anomaly = NO), what is the ratio of sensory-edge effective contributions vs N-to-N contributions in the coherence aggregate $\mathcal{C}(t)$? Expected: ~6:1 under FULL configuration vs ~1:1 under OFF. Measured by partitioning $\mathcal{C}(t)$ into sensory and N-to-N components and comparing magnitudes.

**E3 (Secondary) — Prediction drift magnitude.** Under (sensory = ABSENT, anomaly = NO), measure $\langle \|d_a(t)\|^2 \rangle_t$ over a 60-second sensory-absent window. The suppression mechanism should bound this by approximately $1/\sqrt{\gamma_h}$ (a quadratic Lyapunov estimate). Compare against OFF baseline.

**E4 (Secondary) — Divisive normalisation contrast.** Under (sensory = PRESENT) compare $\mathcal{C}(t)$ variance across stressor conditions for DN_ONLY vs OFF. Expected: DN_ONLY exhibits sharper anomaly localisation (smaller $\sigma_\mathcal{C}^2$ during steady-state, larger transients at anomaly events).

### §7.5.6 Concentration-Based Power

By Hoeffding (§2.10 of [[../02-Theory/(C)-09-Concentration-of-Measure]]) with paired differences in $[-1, 1]$ and $N = 103$:

$$\varepsilon_{\min} = \sqrt{2\log(1/\alpha)/N} \approx 0.024 \quad \text{at one-sided } \alpha = 0.05$$

For the E1 primary endpoint with a target relative reduction of 30% on a baseline FPR around 0.05 per cycle (typical sensory-absent baseline), the absolute reduction is $\sim 0.015$ — **below the Hoeffding detectable threshold**. Phase A-5 therefore requires either (a) larger sample size, or (b) higher effect size, or (c) longer per-subject observation windows to accumulate sufficient cycles.

**Recommendation:** extend per-subject observation to 30 minutes of sensory-absent operation (~36,000 cycles), which lifts the effective $N$ for E1 to $\approx 36{,}000 \times 103 = 3.7 \times 10^6$ paired observations. Detectable difference at this sample size: $\varepsilon_{\min} \approx 1.3 \times 10^{-3}$, well below the 0.015 target. The extension does not require additional subjects, only longer per-subject simulated sensory-absent recording (synthetic-V/S/K data, not new EEG collection).

> [!warning] Autocorrelation Correction (Effective-$N$)
> The 3.7 × 10⁶ observations are **temporally autocorrelated** within each subject's 30-minute window. EEG-derived covariance features at 20 Hz update rate exhibit lag-1 autocorrelation $\hat\rho(1) \approx 0.95\text{–}0.99$ (Woolrich et al., 2001). The effective sample size is:
> $$N_{\mathrm{eff}} = \frac{N}{1 + 2\sum_{k=1}^{K}\hat\rho(k)} \approx \frac{N}{39}\text{ to }\frac{N}{199}$$
> giving $N_{\mathrm{eff}} \approx 18{,}600\text{–}94{,}900$ per subject. At the pessimistic end ($N_{\mathrm{eff}} \approx 18{,}600 \times 103 \approx 1.9 \times 10^6$), the Hoeffding floor becomes $\varepsilon_{\min} \approx 1.8 \times 10^{-3}$ — still below the 0.015 target, so the design remains adequately powered.
>
> **Secondary analysis:** block bootstrap (Politis & Romano, 1994) with block length $\ell = \lceil 1/(1 - \hat\rho(1))\rceil$ to obtain confidence intervals that respect within-subject temporal dependence. Report both naïve and autocorrelation-corrected $p$-values; if they disagree qualitatively, flag for review before gate decision.
>
> *References:* Woolrich, M. W. et al. (2001). Temporal autocorrelation in univariate linear modeling of FMRI data. *NeuroImage*, 14(6), 1370–1386. Politis, D. N. & Romano, J. P. (1994). The stationary bootstrap. *JASA*, 89(428), 1303–1313.

### §7.5.7 Gate Criteria (Pre-Registered)

| Endpoint | Criterion | Action if fails |
|----------|-----------|-----------------|
| **E1** | $\geq 30\%$ relative reduction in sensory-absent FPR; BF₁₀ > 3 | **Halt mechanism deployment.** Hallucination suppression provides no measurable value. Disable M3, retain M1+M2 only |
| **E2** | $\geq 4:1$ sensory dominance ratio under FULL | Calibrate $\beta, \gamma$ in $\pi_{\mathrm{sensory}}$; if still below 4:1, M2 is ineffective at default coupling |
| **E3** | Prediction-drift magnitude bounded by Lyapunov estimate to within 20% | Suggests the quadratic damping form needs refinement (linear term added, exponent tuned) |
| **E4** | DN_ONLY $\sigma_\mathcal{C}^2$ reduction $\geq 15\%$ vs OFF | M1 provides marginal benefit; consider replacing with simpler normalisation scheme |

### §7.5.8 Wall-Clock and Compute

Per-subject Phase A-5 execution (24 conditions × 5 folds × 30 minutes synthetic-absent windows): approximately 4 hours single-threaded on standard laptop CPU. Total for 103 subjects: ~17 days at full sequential execution. With 8-way parallelism via `joblib`: ~2 days. Fits within the existing Phase A timeline (Week 5 of [[(C)-Phase-A-Experiment-Revised]] §12).

### §7.5.9 Decision Logic

```
Phase A-5 Sensory-Anchored Inhibition
    │
    └── E1 (sensory-absent FPR reduction)? ─── no ──▶ Disable M3; retain M1+M2
        │
        yes
        ▼
    └── E2 (sensory dominance ratio)?       ─── no ──▶ Recalibrate β, γ; if still low, disable M2
        │
        yes
        ▼
    └── E3 (prediction drift bounded)?      ─── no ──▶ Refine quadratic damping form
        │
        yes
        ▼
    └── E4 (DN coherence variance)?         ─── no ──▶ Disable M1; document the partial-mechanism configuration
        │
        yes
        ▼
    All three mechanisms validated. Deploy as Stage 1 default.
```

The gate structure permits *partial* validation: if some mechanisms work and others don't, the deployment configuration disables the failing ones rather than rejecting the whole framework. This is explicit in the spec (§6.4.2 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]] notes that operating-mode gating already permits per-mechanism activation).

---

## §7.6 Phase A-6 — U-Node Reflexive Acceleration Validation

**Purpose:** Test claim C7 — that per-path usage tracking (U-nodes) and per-command threshold functions $\theta_{\mathrm{IVE}}(c)$ accelerate authorisation of practised commands without inflating FPR for rare or risky commands. This is the empirical entry point to the §2.14 developmental cogitation substrate (sub-package A: Habit Acceleration).

**Precondition:** Only run if C1 passes in Phase A-1. U-nodes are post-deployment additions to the frozen TTSA-learned restriction maps; they do not affect Phase A-1's primary claim tests.

### §7.6.1 The Two Mechanisms Under Test

| Mechanism | Active component | Predicted effect |
|---|---|---|
| **U1 — U-node path-usage tracking** | Per-edge counter $u_e(t+1) = (1-\lambda) u_e(t) + \mathbb{1}[\text{edge contributed to authorisation}]$ (§2.14.5 of [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]]) | High-U paths route through cached Kernel A → faster authorisation |
| **U2 — Per-command threshold $\theta_{\mathrm{IVE}}(c)$** | $\theta_{\mathrm{IVE}}(c) = \theta_0 (1 - \alpha u_c)(1 + \rho r_c)$ (§2.14.7) | High-practice commands authorise faster; high-risk commands authorise more slowly |

### §7.6.2 Experimental Design

**Caveat upfront.** PhysioNet EEGMMIDB has only two motor-imagery classes (left vs. right) with equal risk profiles. The "risk" dimension $r_c$ of $\theta_{\mathrm{IVE}}(c)$ cannot be tested on this dataset directly. We adopt a **synthetic-risk-label protocol**: arbitrarily designate left-MI as "high risk" ($r_c = 0.9$) and right-MI as "low risk" ($r_c = 0.1$) for half the subjects (the assignment is randomised per-subject and counter-balanced across the cohort). The risk dimension thus tests the *mechanism* of $\theta_{\mathrm{IVE}}(c)$ even though the underlying risk is artificial.

**2 × 3 × 4 within-subject factorial** on the 103 retained PhysioNet EEGMMIDB subjects:

| **Factor 1: U-mechanism configuration** | | **Factor 2: Command-frequency imbalance** | | **Factor 3: Stressor** | |
|---|---|---|---|---|---|
| **U-OFF** | Baseline: $\theta_{\mathrm{IVE}}(c) = \theta_0$ for all $c$; no U-node tracking | **Balanced** | 50/50 trial distribution | **S0** | Clean data |
| **U-ON** | Full mechanism: $\theta_{\mathrm{IVE}}(c)$ function active; U-nodes track usage | **Moderate** | 70/30 trial distribution (one class over-represented) | **S1** | 2 of 32 channels nulled |
| | | **Strong** | 90/10 trial distribution | **S2** | EMG contamination 0 dB SNR |
| | | | | **S3** | Leave-one-subject-out |

2 × 3 × 4 = 24 conditions per subject × 103 subjects × 5 folds = 12,360 paired observations.

The frequency imbalance is implemented at the **training stream level**: within each fold's training portion, trial order is resampled so that the majority class appears more often. The test portion remains balanced for fair latency / FPR comparison. The point of imbalance is to create the practice signal that U-nodes track — not to alter the underlying classifier's training distribution.

### §7.6.3 U-Node State Initialisation

U-nodes are initialised at $u_e(0) = 0.5$ (neutral) and updated in real time as the experiment streams trials. The decay constant is set to $\lambda = 1 / (5 \times 60 \times 250) = 1.33 \times 10^{-5}$ per cycle, giving a ~5-minute half-life — accelerated from the default 24-hour half-life of §2.14.5 because the experiment compresses years of natural usage into hours.

The $\alpha$ and $\rho$ parameters of $\theta_{\mathrm{IVE}}(c)$ are set to their §2.14.7 defaults ($\alpha = 0.5$, $\rho = 2.0$) and held fixed throughout the experiment. Post-hoc sweeping of $\alpha$ and $\rho$ is **explicitly excluded** by pre-registration; they must be fixed before any data is touched.

### §7.6.4 Primary Endpoints

**E1 (Primary) — Latency reduction for the high-frequency class.** Under (frequency = Strong 90/10, U = U-ON) conditions, does the authorisation latency for the majority class decrease relative to (frequency = Balanced 50/50, U = U-OFF)? Paired comparison, BF₁₀ > 3 via BEST.

$$\mathrm{Latency}_{\mathrm{majority,\ U-ON,\ 90/10}} - \mathrm{Latency}_{\mathrm{majority,\ U-OFF,\ 50/50}} \leq -25\%$$

A 25 % relative latency reduction is the gate criterion. Equivalently: if mean authorisation latency under U-OFF balanced is 500 ms, under U-ON 90/10 it should be $\leq 375$ ms.

**E2 (Secondary) — FPR preservation for the minority class.** The U-mechanism should **not** inflate the false-positive rate for the minority class. Specifically:

$$\mathrm{FPR}_{\mathrm{minority,\ U-ON}} - \mathrm{FPR}_{\mathrm{minority,\ U-OFF}} \leq 0.5\,\mathrm{pp}$$

If U-ON inflates minority-class FPR by more than half a percentage point, the mechanism is unsafe — the rare command becomes harder to detect. This is the safety gate.

**E3 (Secondary) — Risk-dimension threshold modulation.** Under the synthetic-risk-label protocol, does the high-risk-designated class show *increased* latency (slower authorisation) under U-ON compared to U-OFF, mirror-imaging the latency reduction for the high-frequency class? Predicted:

$$\mathrm{Latency}_{\mathrm{high-risk-label,\ U-ON}} > \mathrm{Latency}_{\mathrm{high-risk-label,\ U-OFF}}$$

with effect magnitude consistent with the $\rho = 2.0$ parameter. This isolates the risk dimension's contribution from the practice dimension's contribution.

**E4 (Secondary) — Cache-hit-rate ramping.** Does the procedural cache (§2.14.8) hit rate increase monotonically over the course of an extended session for the high-frequency class? Reported as a function of cumulative trial count.

### §7.6.5 Concentration-Based Power

Hoeffding (§2.10.4 of [[../02-Theory/(C)-09-Concentration-of-Measure]]) at $N = 103$:

$$\varepsilon_{\min} = \sqrt{2\log(1/\alpha)/N} \approx 0.024$$

at one-sided $\alpha = 0.05$. For E1 with a target latency reduction of 25 % on a typical baseline of ~500 ms, the absolute reduction is ~125 ms — well above the detectable threshold. The factorial design gives ~12,000 paired observations, lifting the effective detectability to ~5 ms differences. No additional sample-size extension is required for Phase A-6.

For E2 (FPR preservation), the test is **one-sided in the safety direction**: confirm $\mathrm{FPR}_{\mathrm{U-ON}} \not\gg \mathrm{FPR}_{\mathrm{U-OFF}}$. The gate criterion is 0.5 pp, but **Hoeffding at $N = 103$ resolves only differences ≥ 2.4 pp** — the 0.5 pp gate is therefore **below the detection floor** of the current design. This is a power deficiency: to reliably detect a 0.5 pp inflation, Phase A-6 requires $N \geq \lceil 2\log(1/0.05) / 0.005^2 \rceil \approx 240{,}000$ paired observations. With the factorial design providing ~12,000 per subject, this implies $\lceil 240{,}000/12{,}000 \rceil = 20$ subjects suffice — the existing $N = 103$ covers this with the extended observation windows. **Recommendation:** use the full factorial observation set (12,000 × 103 ≈ 1.24 × 10⁶ pairs), which resolves differences down to $\approx 2.2 \times 10^{-3}$ pp, well below the 0.5 pp gate. Apply the same autocorrelation correction as §7.5.6 to the effective sample size.

### §7.6.6 Gate Criteria (Pre-Registered)

| Endpoint | Criterion | Action if fails |
|---|---|---|
| **E1** | ≥ 25 % latency reduction for high-frequency class; BF₁₀ > 3 | U-node mechanism provides no measurable speed benefit. Reduce sub-package A to θ(c)-only (no usage tracking) |
| **E2** | FPR inflation for minority class ≤ 0.5 pp | **Halt mechanism deployment.** U-node mechanism inflates rare-command FPR; safety failure. Disable U-nodes entirely; θ(c) thresholds may proceed independently |
| **E3** | High-risk-designated class shows slower authorisation under U-ON | θ(c) risk dimension is not effective; either recalibrate $\rho$ in Phase B or disable risk-modulation |
| **E4** | Cache-hit rate increases monotonically with practice | Procedural cache benefit is unproven; deploy without cache (no architectural cost, only foregoes compute saving) |

### §7.6.7 Wall-Clock and Compute

Per-subject Phase A-6 execution (24 conditions × 5 folds × extended trial sequence to build U-node state): approximately 5 hours single-threaded on commodity laptop. Total for 103 subjects: ~22 days at full sequential execution. With 8-way parallelism via `joblib`: ~3 days. **Fits in Week 5 alongside A-3, A-4, and A-5** by running in parallel.

### §7.6.8 Decision Logic

```
Phase A-6 U-Node Reflexive Acceleration
    │
    └── E1 (latency reduction)?     ─── no ──▶ Disable U-tracking; retain θ(c) only
        │
        yes
        ▼
    └── E2 (minority FPR preserved)? ─── no ──▶ SAFETY HALT — disable U-mechanism
        │                                       (override; do not deploy regardless of E1)
        yes
        ▼
    └── E3 (risk dimension works)?   ─── no ──▶ Recalibrate ρ in Phase B
        │
        yes
        ▼
    └── E4 (cache-hit ramping)?      ─── no ──▶ Deploy without procedural cache
        │
        yes
        ▼
    Full sub-package A (Habit Acceleration) validated.
    Promotes from Stage 2.5 candidate to Phase B implementation target
    (~12-month timeline acceleration).
```

The E2 gate is **a safety override**: even if E1 passes, an FPR inflation for the minority class halts deployment. The mechanism cannot accelerate frequent commands at the expense of detecting rare ones.

### §7.6.9 Relationship to §2.14

Phase A-6 tests *only sub-package A* of the §2.14 developmental cogitation substrate. The other seven components (JEPA, C-nodes, B-nodes, critical-period plasticity, memory hierarchy, THINK mode) are not addressed by this protocol and remain Stage 2.5+ candidates pending separate validation. Phase A-6 is the cheapest, lowest-risk entry point — if sub-package A passes, the developmental-cogitation vision has a foothold in the validated architecture; if it fails, the rest of §2.14 needs revisiting before any Stage 2.5 commitment.

### §7.6.10 Pre-registration

Phase A-6 requires its own pre-registration amendment to [[(C)-OSF-Preregistration-Phase-A1]] (analogous to §9 Amendment 1 for R_FM). Sub-questions for the amendment:

- Synthetic-risk-label assignment seed (must be locked at registration)
- Trial-imbalance shuffle seed (must be locked at registration)
- $\alpha = 0.5$ and $\rho = 2.0$ parameter values (must be locked at registration)
- The four E1–E4 gate criteria (already specified above)
- The expected discrimination matrix for a smoke-test analogous to [[(C)-A1-Synthetic-Smoke-Test-Generator]]

---

## §7.7a Phase A-7 — Continuous-Time Dynamical Comparison via Digital ACP Twin

**Purpose:** Address the gap that Phase A-1 (including the R_JEPA / LeWM amendment) tests only the **algorithmic prior** of the sheaf representation, not the **dynamical architecture** of the analogue plane, multi-timescale TTSA, SPRT-based evidence accumulation, sub-5-ms hyperdirect pathway, sensory-anchored inhibition, or THINK-mode harmonic preservation. Phase A-1 evaluates whether sheaf-augmented static features beat LeWM-style end-to-end features on offline 4-s epochs. **It cannot evaluate whether the analogue + dynamic + real-time architecture beats LeWM in deployment-realistic streaming-mode scenarios.**

Phase A-7 closes this gap by running both architectures on a **digital twin of the analogue plane** with non-real-time execution, using endpoint metrics that the static-classification protocol cannot measure.

**Precondition:** Only run if C1 passes in Phase A-1. Phase A-7 uses the frozen TTSA-learned restriction maps from Phase A-1.

### §7.7a.1 What this protocol tests that Phase A-1 cannot

| Endpoint | What it measures | Why LeWM cannot match by design |
|---|---|---|
| **E1 — Streaming latency to correct authorisation** | SPRT sequential evidence accumulation vs LeWM batch-decision per inference call | LeWM has no early-stopping mechanism; produces fixed-window verdicts |
| **E2 — Sub-event-latency safety stop** | B-node hyperdirect pathway timing (target sub-5 ms) | LeWM has no equivalent of a hyperdirect safety bypass |
| **E3 — FPR under controlled in-session drift** | Multi-timescale TTSA intermediate-rate adaptation mid-session | LeWM weights are frozen at inference; cannot adapt within a session |
| **E4 — Recovery time from injected mid-trajectory stressor** | Sensory-anchored inhibition + Lipschitz-stable restriction maps under sudden perturbation | LeWM has no equivalent recovery mechanism for mid-stream perturbation |
| **E5 — Cross-modal evidence convergence** | V/S/K context nodes feeding IVE Evidence 5 | LeWM is unimodal (pixels only; or in this case, EEG only) |
| **E6 — Energy per verified command** | Analogue subthreshold ACP efficiency (modelled) vs LeWM-on-CPU/GPU energy estimate | Not strictly comparable across substrates, but informative |

**These are the dynamical metrics on which thrIVE's architectural complexity is supposed to earn its keep.** Phase A-1's static-classification arm tests representational claims; Phase A-7 tests dynamical claims.

### §7.7a.2 The Digital ACP Twin

A complete digital simulator of the analogue plane is required. It must faithfully model:

| ACP component | Simulator requirement | Sources |
|---|---|---|
| Subthreshold CMOS 2-compartment neurons | Integrate Rao-Ballard ODEs at fine time-step (default 0.1 ms substep within 4-ms cycle) | Naghieh et al. (2025) cell template; §3 of [[../03-Architecture/01-Node-Types-Dynamics]] |
| Per-cycle Kernel A / B / C unified compute spine | Deterministic bit-exact computation at 250 Hz | §2.13 of [[../02-Theory/(C)-12-Unified-Compute-Spine]] |
| Multi-timescale TTSA | Fast / intermediate / slow / ultra-slow / LTP at correct rate ratios | §2.4 of [[../02-Theory/04-Additional-Theory]] |
| Sensory-anchored inhibition | Factored $G_\pi G_{\mathrm{DN}} G_{\mathrm{class}}$ operator per cycle | §6 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]] |
| Hyperdirect pathway | Sub-5 ms emergency-stop bypass; modelled as 1-2 cycle latency | §2.14.4 of [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]] |
| IVE SPRT evidence stack | Sequential evidence integration with adaptive threshold $\theta_{\mathrm{IVE}}(c)$ | §6 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] |
| V/S/K context node injection | Synthetic streams synchronised to EEG trial structure (cf. §7.5.3 Phase A-5) | §3.2.2–4 of [[../03-Architecture/00-Architecture-Index]] |
| Modelled analogue noise | Gaussian + 1/f noise additions calibrated against §9.5 noise budget | §9.5 of [[../08-Hardware/05-Precision-Noise-Risk]] |

**Honest scope statement.** The digital twin can validate the *mechanism* but not the deployed *behaviour*. Three things it cannot test:

1. **Real analogue noise.** The simulator includes modelled noise (Gaussian + 1/f) but cannot faithfully reproduce shot noise, flicker, mismatch, etc.
2. **Real hardware latency under load.** The simulator computes 4-ms cycle dynamics in whatever wall-clock time it takes; ASIC characterisation requires Phase C.
3. **Real closed-loop user adaptation.** The user is fixed at PhysioNet recording time; deployment co-evolution cannot be simulated.

These limits mean Phase A-7 is **necessary but not sufficient** for deployment validation. Phases B (FPGA) and C (ASIC) close the remaining gaps.

**Build-on-existing-infrastructure note.** Digital simulation of analogue neuromorphic dynamics is an established practice with mature open-source infrastructure. The digital ACP twin **does not need to be built from scratch**:

- **Brian2** ([Stimberg, Brette & Goodman, 2019, *eLife*](https://elifesciences.org/articles/47314)) — Python neural simulator with explicit support for arbitrary-equation neuron models; well-suited for the 2-compartment Naghieh-template ACP cells
- **NEST** (Gewaltig & Diesmann, 2007, *Scholarpedia*) — large-scale spiking neural network simulator with parallel execution
- **SpiNNaker** (Furber et al., 2014, *Proc. IEEE*) — digital real-time platform with documented digital-twin behaviour
- **BrainScaleS** (Pfeil et al., 2013, *Frontiers*) — accelerated analogue platform (~10,000× real-time); literature documents digital-vs-analogue comparison validation

Additionally, **AlgebraicDynamics.jl** (AlgebraicJulia project; GitHub: AlgebraicJulia/AlgebraicDynamics.jl; actively maintained as of April 2026) provides a compositional dynamical systems framework built on category theory:

- Operadic composition of continuous machines and resource sharers maps directly onto the ACP's shared-membrane inter-node coupling
- Automatic construction of `ODEProblem` / `DDEProblem` from compositional specifications via the DifferentialEquations.jl ecosystem
- The compositional structure preserves the categorical properties required by the Bayesian lens framework (§2.6 of [[../02-Theory/(C)-05-Bayesian-Lens-Framework]]])

AlgebraicDynamics.jl is mathematically general (not neuroscience-specific), and could serve as the backbone for the sheaf-Laplacian dynamics + unified compute spine layers, with Brian2 handling per-neuron biophysical integration. The two interoperate via Julia's FFI. A 3-day proof-of-concept (encode a 4-node sheaf subgraph as resource sharers, compose, compare ODE output against a hand-coded reference) is recommended before committing to either platform. See [[(C)-09-Topos-Institute-Research-Mapping]] §3.4 for detailed assessment.

These platforms simulate biophysically realistic neuron dynamics with established physical accuracy. The thrIVE-specific extension is the **sheaf-Laplacian dynamics + unified compute spine + SPRT IVE pipeline**, none of which existing simulators support natively. The Phase A-7 software effort is therefore:

| Layer | Status | Effort |
|---|---|---|
| Per-neuron ODE integration (2-compartment Rao-Ballard) | Available in Brian2 / NEST | ~1 day integration |
| Modelled analogue noise (Gaussian + 1/f) | Available in Brian2 | ~1 day calibration |
| Sheaf-Laplacian assembly + Kernel A/B/C | **Novel — must be implemented** | ~1 week |
| Multi-timescale TTSA on the simulator | **Novel — must be implemented** | ~1 week |
| IVE SPRT evidence stack | Adaptable from existing scipy.stats | ~3 days |
| V/S/K context injection | Available; matches Phase A-5 §7.5.3 procedure | ~1 day |
| **Total Phase A-7 software** | | **~3 weeks** rather than from scratch |

This is substantially more tractable than building a complete digital twin from scratch (would be a multi-month effort). The "novel" components are the thrIVE-specific layers; everything else builds on validated infrastructure.

**Executable implementation:** the deterministic simulator is locked in [[(C)-Phase-A7-Digital-ACP-Twin]]. The script's SHA-256 hash is logged in the OSF manifest as `phase_a7_script_sha256`. All locked parameters (TTSA timescales, SPRT thresholds, sensory-inhibition constants, hyperdirect latency cap, modelled noise parameters, critical-period reopen threshold, master seed 42) are hard-coded in the simulator and protected by the hash lock. The locked script implements the **core thrIVE architecture** required by the slimmed endpoint set (E1′ / E2 / E3′ / E4 / E6 / E7′); Stage 2.5 extensions (full E-node bank, C-nodes, U-nodes, JEPA prediction engine, THINK mode) are deferred and clearly documented as out-of-scope for the v1 simulator.

### §7.7a.3 Experimental design

**2 × 4 × 5 within-subject factorial:**

| Factor | Levels |
|---|---|
| **Architecture** | thrIVE-full-dynamic (digital ACP twin), R_JEPA (LeWM running on the same streaming data) |
| **Stressor regime** | clean (S0), channel-dropout (S1), EMG (S2), in-session drift (S3 — restriction-map perturbation injected mid-trajectory) |
| **Streaming mode** | static (matches Phase A-1 batch), pseudo-streaming (per-cycle inference), full-streaming (continuous trajectory with sensory context injection), sensory-absent (V/S/K nulled at random intervals), drift-and-recovery (stressor + recovery measurement) |

2 × 4 × 5 = 40 conditions × 103 subjects × 5 folds = 20,600 paired observations.

### §7.7a.4 Primary endpoints (literature-informed slimming)

**Slimming rationale.** A literature audit (May 2026) found that several originally-proposed endpoints are already settled by the BCI mainstream and do not need re-confirmation within Phase A-7. Specifically:

- **SPRT-based sequential evidence accumulation is faster than batch classification at matched accuracy** is established by [Liu et al. (2017, PMC5734001)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5734001/) for motor-imagery EEG. The general claim does not require re-testing.
- **Multimodal fusion improves classification over unimodal EEG** is established by [BrainFusion (2025, *Advanced Science*)](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202417408), [TSFNet (2025)](https://www.mdpi.com/1424-8220/25/19/6111), and multiple 2024–2025 EEG-fNIRS / EEG-fMRI fusion reviews. The general fusion-helps claim does not require re-testing.

Phase A-7 therefore tests only **thrIVE-specific composite mechanisms** that the BCI mainstream literature does not address. The endpoint set is reformulated to focus on these:

**E1′ (Primary, reformulated) — Multi-evidence SPRT vs single-evidence SPRT speed advantage.** Under (architecture × stressor × mode = clean × full-streaming) conditions, does thrIVE's *multi-evidence* SPRT (Evidence channels 1–5 of §6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]]) authorise correct commands faster than a *single-channel* SPRT baseline (Evidence 1 alone) on the same streaming data?

$$\mathrm{Latency}_{\mathrm{multi-evidence\,SPRT}} < \mathrm{Latency}_{\mathrm{single-evidence\,SPRT}}$$

with effect size $d > 0.3$, one-sided $\alpha = 0.05$. This tests the *evidence-channel-multiplicity* claim, **not** the SPRT-vs-batch claim that Liu et al. (2017) already settled. If E1′ passes: thrIVE's multi-evidence fusion adds measurable speed value over the single-channel SPRT baseline.

**E2 (Primary, retained) — Mid-trajectory stressor recovery via sensory-anchored inhibition + Lipschitz restriction maps.** Under (architecture × stressor × mode = drift × drift-and-recovery), measure cycle count from stressor onset to FPR returning to within 1.2× baseline. Predicted: thrIVE-full-dynamic recovers faster due to the *composite* of sensory-anchored inhibition (§6 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]]) + Lipschitz-stable restriction maps (§2.4 of [[../02-Theory/04-Additional-Theory]]). No published literature characterises this specific composite recovery mechanism; thrIVE-specific test.

**E3′ (Primary, reformulated) — Multi-timescale TTSA + critical-period reopening vs T-TIME baseline.** Under (drift × full-streaming) conditions, does the *composite* multi-timescale TTSA + critical-period reopening (§2.14.6 of [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]]) adapt to drift better than the T-TIME baseline (Wu et al., 2024, already cited)? Tests the *additional* contribution of the multi-timescale + critical-period mechanism beyond what T-TIME provides. **Not** the general "adaptation helps" claim, which Vidaurre et al. (2011) and T-TIME itself already establish.

**E4 (Secondary, retained) — V/S/K cross-modal evidence convergence in the IVE specifically.** Under (full-streaming with V/S/K context), measure IVE Evidence 5 (cross-modal) contribution to authorisation. Predicted: thrIVE's IVE evidence-stack mechanism produces measurable convergence specifically. Tests the *IVE-evidence-stack* mechanism, **not** the general "fusion helps" claim that BrainFusion (2025) already establishes (see E7′ below for the fusion-method-specific comparison).

**E6 (Primary, retained, renumbered from original E6) — Sub-event hyperdirect safety-stop latency.** Inject synthetic catastrophic anomaly mid-trajectory; measure cycles to system halt via hyperdirect pathway (§2.14.4). Target: $\leq 2$ cycles (8 ms). Genuinely thrIVE-specific — basal-ganglia hyperdirect is biologically characterised but its silicon implementation for BCI is rare; no published benchmark.

**E7′ (Primary, NEW) — Sheaf-coherence-based fusion vs attention-based fusion baselines.** On the same EEG + V/S/K data, compare thrIVE's per-edge sheaf-coherence fusion mechanism against published attention-based fusion (TSFNet 2025) and CNN-LSTM concatenation fusion (BrainFusion 2025) baselines. Tests the *sheaf-fusion-mechanism* claim, **not** the *fusion-helps* claim. This is the genuinely novel comparison: does thrIVE's mathematical structure for fusion (per-edge defect aggregation through the sheaf Laplacian) outperform the established attention / concatenation methods?

**Dropped:**

- ~~Original E1 (SPRT vs batch)~~ — settled by Liu et al. 2017; replaced with E1′ (multi-evidence vs single-evidence)
- ~~Original E5 (energy per command)~~ — moved to deferred status; substrate comparison is not strictly meaningful at simulation level. Phase C ASIC characterisation is the proper venue.

The slimmed endpoint set tests **only** what is thrIVE-specific and not addressed by current literature. The composite (E1′, E2, E3′, E4, E6, E7′) is a 6-endpoint protocol focused on novel mechanisms.

### §7.7a.5 Gate criteria

| Endpoint | Criterion | Action if fails |
|---|---|---|
| **E1** | Latency advantage $d > 0.3$, $p < 0.05$ | SPRT-based evidence accumulation is no faster than batch inference; reconsider the IVE architectural commitment |
| **E2** | thrIVE-dynamic recovers faster than R_JEPA from stressor | The Lipschitz-stable restriction maps + sensory-anchored inhibition do not confer real-time recovery advantage; revisit §6 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]] |
| **E3** | thrIVE-dynamic sustains stable FPR during sensory absence; R_JEPA does not | If both unstable, THINK mode requires revision; if R_JEPA matches, sensory absence is not a discriminating regime |
| **E4** | V/S/K-augmented IVE produces measurable evidence convergence | Multi-modal integration claim weakened; consider whether V/S/K nodes are worth their compute cost |
| **E5** | Energy per command at least 5× lower for thrIVE-dynamic (modelled) | Substrate efficiency claim is mostly aspirational; recalibrate hardware section |
| **E6** | Hyperdirect halt within 2 cycles | Safety architectural commitment fails; B-node design needs revision |

### §7.7a.6 Wall-clock and compute

The digital ACP twin is **substantial software**: simulating 5 s of trajectory at 0.1 ms substeps within 4 ms cycles = 50,000 substeps per trajectory × 40 conditions × 5 folds × 103 subjects ≈ $10^9$ substeps total. With parallelism: ~1 week wall-clock on commodity multi-core machine.

This is the largest Phase A sub-protocol by compute cost. It is justified because **none of the other sub-phases can test the dynamical architecture**, and the dynamical claims are central to thrIVE's complexity argument.

### §7.7a.7 What this protocol does NOT establish

Honest scope:

1. **Not equivalent to deployed performance.** Digital simulation $\neq$ ASIC validation. Phase C (ASIC characterisation) and Phase B.5 (human IRB validation) remain necessary.
2. **Modelled analogue noise may be wrong.** If actual silicon noise differs substantially from the modelled Gaussian + 1/f, the dynamic-comparison results may not predict deployed behaviour.
3. **No user co-evolution.** PhysioNet data is fixed; closed-loop user-system co-adaptation is not modelled.
4. **R_JEPA is treated as a sequence model in streaming mode.** This is a fair adaptation of LeWM to EEG, but is not LeWM's published evaluation setting. The comparison is fair in the streaming-EEG context but not against LeWM's video benchmark performance.

### §7.7a.8 What this protocol DOES establish (if it passes)

If E1–E6 all pass:

- thrIVE's dynamical architecture confers measurable advantages in streaming-mode, multi-modal, drift-prone scenarios that LeWM cannot match by design
- The architectural complexity (multi-timescale TTSA, SPRT IVE, hyperdirect pathway, sensory-anchored inhibition, THINK mode) is **dynamically justified** even if Phase A-1 static-classification arm is inconclusive
- The Phase B (FPGA) and Phase C (ASIC) hardware programmes have a credible scientific motivation: the dynamical advantages are pre-validated in simulation before tape-out commitment

This is the **architectural justification path** that Phase A-1 alone cannot provide. The two protocols are complementary: A-1 tests representational priors; A-7 tests dynamical mechanisms. **Both should pass for the full architecture to be justified.**

### §7.7a.9 Pre-registration

Phase A-7 requires its own pre-registration amendment (Amendment 3 to the OSF preregistration), analogous to Amendment 1 (R_FM) and Amendment 2 (R_JEPA). Locked items:

- Digital ACP twin software at a tagged `phase-a7-locked` git commit
- Twin script SHA-256 hash logged as `phase_a7_twin_sha256`
- Modelled noise calibration locked (Gaussian σ, 1/f exponent, etc.)
- Stressor injection parameters locked (timing, magnitude, type)
- All E1–E6 gate criteria locked

### §7.7a.9a The harder version — Phase A-7′ against BCI mainstream baselines (recommended)

Phase A-7 as specified above tests **thrIVE vs LeWM** in streaming mode. This is informative but not the *hardest* honest test. The hardest honest test is **thrIVE vs the BCI mainstream state of the art** — not against a video-domain research model adapted to EEG, but against the actual published methods that solve each problem in the BCI literature:

| Mechanism | Mainstream BCI baseline (literature) | Reference |
|---|---|---|
| Sequential decision-making | SPRT with optimal-wavelet preprocessing | [Liu et al. (2017, PMC5734001)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5734001/) |
| Multimodal fusion (EEG + auxiliary modality) | Attention-based fusion (TSFNet) + low-code framework (BrainFusion) | [BrainFusion (2025, *Advanced Science*)](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202417408); [TSFNet (2025, *Sensors*)](https://www.mdpi.com/1424-8220/25/19/6111) |
| Online drift adaptation | T-TIME entropy minimisation + backpropagation-free transfer | Wu et al. (2024, 2025) — already cited §7.7 of [[../07-Implementation/01-Calibration-Deployment]] |
| Online continual decoding | Memory-buffer-based continual learning on streaming subjects | [Online continual decoding (2024, PMC11050974)](https://pubmed.ncbi.nlm.nih.gov/38692190/) |
| Foundation-model representation | ST-EEGFormer / LCM | §7.7a of [[../07-Implementation/01-Calibration-Deployment]] (already covered in Phase A-1 R_FM arm) |

**Phase A-7′ test:** does thrIVE's composite (sheaf + multi-timescale TTSA + SPRT IVE + sensory-anchored inhibition + hyperdirect + THINK mode) beat **the ensemble of mainstream baselines applied separately** (SPRT-Liu + BrainFusion attention + T-TIME adaptation + memory-buffer continual learning + ST-EEGFormer features)?

This is the architecturally honest comparison. The mainstream baseline ensemble represents the **state of the art that thrIVE would actually replace if deployed**, not a stand-in. If thrIVE's composite does not beat this ensemble, the architectural complexity is unjustified relative to deployable alternatives — the spec must acknowledge this directly.

**A-7′ design (2 × 4 × 4 factorial):**

| Factor | Levels |
|---|---|
| Architecture | thrIVE-composite (digital ACP twin), Mainstream-ensemble (SPRT-Liu + TSFNet + T-TIME + ST-EEGFormer composed pipeline) |
| Stressor | clean (S0), channel dropout (S1), EMG (S2), in-session drift (S3) |
| Mode | static-baseline, pseudo-streaming, full-streaming-with-context, sensory-absent |

2 × 4 × 4 = 32 conditions × 103 subjects × 5 folds = 16,480 paired observations.

**A-7′ primary endpoints (same metrics as A-7 above, against a different baseline):**

- **E1′′ — Streaming latency at matched accuracy:** thrIVE-composite vs mainstream-ensemble
- **E2 (unchanged) — Mid-trajectory stressor recovery**
- **E3′′ — Composite adaptation:** thrIVE multi-timescale + critical-period vs T-TIME-plus-continual-learning
- **E4 (unchanged) — V/S/K cross-modal evidence convergence vs attention-based fusion**
- **E6 (unchanged) — Hyperdirect safety-stop latency**

**A-7′ gate criteria:** thrIVE-composite ≥ mainstream-ensemble at matched detectability, with at least one endpoint showing $d > 0.3$ advantage. If failure: the architecture is no better than the ensemble of established BCI methods — substantial revision required.

**Honest framing:** Phase A-7 (against LeWM) tells you whether thrIVE beats a research model from a different domain. Phase A-7′ (against the BCI ensemble) tells you whether thrIVE beats the actual deployable alternative. **Both should be run; A-7′ is the higher-stakes test.**

**Compute:** A-7′ requires implementing the mainstream-ensemble baseline (~2 weeks of integration work, much lighter than the digital ACP twin) and running the comparison. Total Phase A-7 + A-7′ wall-clock: ~3 weeks of focused development + ~1 week of simulation runs.

**Pre-registration:** Both A-7 (vs LeWM) and A-7′ (vs mainstream ensemble) require pre-registration amendments. The combined Amendment 3 to the OSF preregistration should cover both, with explicit gate criteria for both LeWM-comparison and ensemble-comparison outcomes. The four-cell verdict matrix (§7.7a.10) extends to an eight-cell matrix when A-7′ is included — the higher dimensionality is the price of testing against multiple defensible baselines.

**Executable implementation:** the mainstream-ensemble baseline is locked in [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]]. The script's SHA-256 hash is logged in the OSF manifest as `phase_a7_ensemble_script_sha256`. The locked composition consists of five published mainstream methods (SPRT-Liu 2017 + TSFNet-style attention fusion + Wu T-TIME 2024 + memory-buffer continual learning + ST-EEGFormer/LCM foundation-model features), each with cited reference and locked parameters. **E6 (hyperdirect latency) and E7′ (sheaf-fusion-ratio) are reported as N/A by design** — the mainstream BCI literature has no equivalents to thrIVE's hyperdirect pathway or sheaf-coherence-based fusion mechanism. This is the architectural-identity test: thrIVE wins these endpoints by default, but must additionally compete on the four endpoints where the mainstream does have established methods (E1′ latency, E2 recovery, E3′ adaptation drift, E4 cross-modal evidence).

### §7.7a.10 The hard architectural test, completed

Phase A-1 (Amendment 2, R_JEPA) tests **representational** claims. Phase A-7 tests **dynamical** claims. Together they constitute the full architectural validation:

| Outcome of A-1 H5 (R8+S vs R_JEPA) | Outcome of A-7 (dynamic vs streaming-R_JEPA) | Architectural verdict |
|---|---|---|
| ✓ pass (sheaf beats end-to-end JEPA representationally) | ✓ pass (dynamic architecture beats streaming JEPA) | **STRONGEST**: full architectural justification |
| ✓ pass | ✗ fail | Sheaf is good representation but dynamic machinery doesn't help; consider simpler IVE / fewer timescales |
| ✗ fail | ✓ pass | Sheaf representation no better than minimal-prior JEPA, but the dynamic architecture (SPRT, hyperdirect, multi-timescale, THINK) is justified independently — architecture as a *control system*, not as a *representation system* |
| ✗ fail | ✗ fail | **FUNDAMENTAL HALT**: neither representational nor dynamic claims survive. Major architectural revision required. |

The (✗, ✓) outcome is interesting and worth highlighting: it would mean thrIVE's value lives in the *control system* (IVE, safety, adaptation, mode-switching) rather than in the *representation* (sheaf, microcircuit). This is a defensible architectural identity — closer to a sophisticated safety controller than a novel ML method — and would be honestly disclosed by the pre-registered combined test.

---

## §7.7 Phase A-9 — Empirical $\tau_{\mathrm{sustain}}$ and Sheaf-Coherence-Threshold Calibration

**Purpose:** Address OQs 11.104 and 11.105 — empirically tie the IVE $\tau_{\mathrm{sustain}}$ threshold and the Evidence 1 sheaf-coherence threshold to conscious-access measurements derived from a controlled psychophysical paradigm. The aim is to convert these parameters from arbitrary calibration values to empirically grounded thresholds aligned with the COGITATE 2025 sustained-activity findings.

**Precondition:** Only run if C1 passes in Phase A-1. Requires fresh human EEG data — this is the first Phase A sub-phase to require new data collection. **IRB approval required.**

### §7.8.1 The paradigm — backward masking

[Backward masking](https://en.wikipedia.org/wiki/Backward_masking) is the canonical psychophysical paradigm for distinguishing conscious from subliminal processing (Breitmeyer & Öğmen, 2006; Dehaene et al., 1998 — used in original GWT work). A target stimulus (visible image) is presented briefly (~16–66 ms) and immediately followed by a mask (random noise or scrambled image). Depending on the stimulus-onset asynchrony (SOA):

- **Long SOA (> ~200 ms):** target is consciously perceived; subject reports seeing it
- **Short SOA (< ~50 ms):** target is masked, processed subliminally; subject does not report seeing it but neural processing of the target still occurs

The contrast between long-SOA (conscious) and short-SOA (subliminal) trials gives a direct empirical handle on the sheaf-coherence and sustained-activity signatures of conscious vs subliminal processing in the same subject viewing the same stimulus content.

### §7.8.2 Experimental design

**Within-subject, mixed factorial design:**

| Factor | Levels |
|---|---|
| **SOA** (continuous) | 0, 16, 33, 50, 83, 116, 200 ms — covers the full subliminal-to-conscious transition |
| **Stimulus class** | Face, object, scrambled (orthogonalises low-level features from semantic content) |
| **Subjective report** | Per-trial 4-point visibility scale (Perceptual Awareness Scale, Ramsøy & Overgaard, 2004) |

**Sample size:** 40 subjects (within-subject design with $N = 40$ gives Hoeffding $\varepsilon_{\min} \approx 0.038$ at $\alpha = 0.05$). Standard psychophysics sample. Cost-recoverable via small honoraria (~£20/subject), single 90-minute session.

**Total trials per subject:** 7 SOA × 3 class × 40 repeats = 840 trials, ~45 minutes of recording at 3 s/trial.

**EEG setup:** Same 64-channel system as Phase A-1, mounted using same Phase 1 calibration protocol. Sheaf-state computation in real time using frozen restriction maps from Phase A-1.

### §7.8.3 Per-trial measurements

For each trial, log:

1. **SOA** (input variable)
2. **Subjective visibility report** (1 = not seen; 4 = clearly seen) — Ramsøy-Overgaard PAS
3. **Sheaf coherence trajectory** $\mathcal{C}(t)$ over the 1500 ms post-stimulus window, sampled at 250 Hz
4. **Hodge harmonic component magnitude** $\|\mathrm{proj}_{\ker L_{\mathcal{F}}}\!\mathbf{x}(t)\|^2$ over the same window
5. **IVE Evidence 1 trajectory** (raw value, before thresholding)
6. **Successful behavioural identification** (yes/no — was the stimulus class correctly identified?)

### §7.8.4 Primary endpoints

**E1 (Primary) — Sheaf coherence discriminates conscious from subliminal trials.** Within-subject comparison of mean sheaf coherence $\mathcal{C}(t)$ during the 200–1000 ms post-stimulus window, between conscious (PAS = 3 or 4) and subliminal (PAS = 1 or 2) trials. Predicted: conscious trials show systematically higher and more sustained $\mathcal{C}(t)$.

$$\mathbb{E}[\mathcal{C}(t)\,|\,\mathrm{conscious}] - \mathbb{E}[\mathcal{C}(t)\,|\,\mathrm{subliminal}] > 0$$

with paired Cohen's $d > 0.5$ and BF₁₀ > 10 via BEST (Kruschke, 2013).

**E2 (Primary) — Threshold derivation.** Identify the value of $\mathcal{C}(t)$ that maximally discriminates conscious from subliminal trials via ROC analysis. The optimal-threshold value $\mathcal{C}^*$ becomes the empirically grounded IVE Evidence 1 threshold for "conscious access".

Reported: ROC curve, AUC with 95 % CI, optimal Youden-index threshold, sensitivity/specificity at the threshold.

**E3 (Primary) — Sustained-duration calibration.** Identify the minimum duration of sustained $\mathcal{C}(t) > \mathcal{C}^*$ that reliably predicts conscious access. Compute the conditional probability:

$$\mathrm{P}(\mathrm{conscious} \mid \mathcal{C}(t) > \mathcal{C}^* \text{ for duration } > \tau)$$

as a function of $\tau$. The value of $\tau$ at which this probability exceeds 0.95 becomes the empirically grounded $\tau_{\mathrm{sustain}}^*$. Expected: $\tau_{\mathrm{sustain}}^* \in [300, 800]$ ms based on COGITATE-observed sustained-activity windows.

**E4 (Secondary) — Hodge harmonic magnitude during conscious vs subliminal trials.** Tests the THINK-mode anchor (§2.14.9.3): does the harmonic-component magnitude correlate with consciousness independently of total $\mathcal{C}(t)$? If yes, harmonic preservation is empirically validated as a conscious-access correlate beyond the bulk coherence measure.

### §7.8.5 Concentration-based power

40 subjects × 7 SOA × 3 class × 40 repeats = 33,600 trials. After within-subject averaging, effective $N$ for the conscious-vs-subliminal contrast is 40 × ~14 conscious trials and 40 × ~14 subliminal trials per condition. Hoeffding at $N = 40$:

$$\varepsilon_{\min} = \sqrt{2\log(1/\alpha)/N} \approx 0.039 \text{ at } \alpha = 0.05$$

For a target effect size of $d = 0.5$ on the conscious-subliminal sheaf-coherence difference, the detectable absolute difference is ~3–5 % in $\mathcal{C}(t)$. This is below typical conscious-subliminal effect sizes in the masking literature (10–20 % differences typical). **Adequate power.**

### §7.8.6 Gate criteria

| Endpoint | Criterion | Action if passes | Action if fails |
|---|---|---|---|
| E1 | $d > 0.5$, BF₁₀ > 10 | Sheaf coherence is empirically validated as a conscious-access correlate | Sheaf coherence does not track conscious access; IVE threshold story weakened |
| E2 | AUC > 0.75 with non-overlapping 95 % CI vs chance (0.5) | $\mathcal{C}^*$ becomes the IVE Evidence 1 threshold default | No defensible threshold derivable; revert to calibration default |
| E3 | $\tau_{\mathrm{sustain}}^*$ identified within [300, 800] ms | Lock $\tau_{\mathrm{sustain}}^*$ as the new IVE default for "consciously available" content | Current $\tau_{\mathrm{sustain}} = 150$ ms is either too short (no consciousness threshold reachable) or system unstable |
| E4 | Harmonic magnitude correlation $> 0.3$ with conscious-vs-subliminal label | THINK mode's harmonic mechanism gains direct empirical anchor | Harmonic preservation is a substrate property without conscious-content correlate |

### §7.8.7 Wall-clock and resources

**Per-subject:** 90 minutes (consent, setup, recording, debrief) — standard psychophysics session

**Total recording:** 40 subjects × 90 min = 60 hours of recording time + ~80 hours of setup/handling = ~140 hours total

**Analysis:** ~1 week single-operator after data collection

**Cost:** ~£800 in subject honoraria + ~£200 in consumables (EEG gel, electrodes). EEG system already available from Phase A-1.

**Timeline:** ~3 months including IRB approval (typically 6–10 weeks), recruitment (~4 weeks), execution (~4 weeks), analysis (~2 weeks). **Cannot fit in Phase A timeline.** Positioned as **Phase A-9 standalone follow-up after Phase A-1 to A-6 complete.**

### §7.8.8 IRB considerations

- Standard psychophysics paradigm with visible stimuli; minimal risk
- EEG is non-invasive; same equipment and protocol as Phase A-1
- No deception beyond standard masking-paradigm instructions
- Subject withdrawal at any time
- Data anonymised at source; only EEG and behavioural scores retained

Standard IRB approval timeline expected. Pre-registration via OSF (analogous to Phase A-1 amendment) committed before any subject is recruited.

### §7.8.9 What success means for the spec

If E1–E3 all pass, the IVE Evidence 1 threshold and $\tau_{\mathrm{sustain}}$ are converted from arbitrary calibration parameters to **empirically grounded psychophysical thresholds**. This is a substantial credibility upgrade for the IVE safety claim — the gate between "this command is consciously authorised" and "this command is subliminal noise" is no longer an engineering knob but a measured boundary.

If E4 also passes, the THINK mode harmonic mechanism gains independent empirical validation alongside the §7.7 Phase B-1 simulation evidence. The combined evidence package would be the strongest neuroscience-anchored claim in the thrIVE spec.

If E1 or E2 fail, the consciousness-correlate framing of the IVE is weakened. The system would still function as a verifier of *task-relevant intent*, but the additional claim that it tracks *conscious access* would be retracted from the spec. This is a graceful degradation — the architecture's safety properties are independent of the consciousness alignment.

### §7.8.10 What this protocol does NOT establish

Important honesty about scope:

1. **Does not establish that thrIVE is conscious.** Threshold derivation does not imply substrate consciousness; it implies the substrate's coherence measure tracks a known psychophysical marker.
2. **Does not adjudicate between GWT and IIT.** The paradigm uses *subjective report* as the consciousness criterion, which both theories accept; it cannot distinguish their predictions about the underlying mechanism.
3. **Does not establish phenomenal consciousness.** Only access-consciousness is measured (via report and identification).

The protocol stays within the explicit scoping of §2.15.9: it operationalises the access-consciousness alignment without claiming phenomenal consciousness.

---

## §7.7b Phase A-10 — Ethics Core Constraint Logic Simulation

**Purpose:** Verify the Ethics Core's constraint evaluation logic (CVB, harm function, assembly-risk scoring) in software before committing to silicon. The Ethics Core is hardwired and fail-closed (§11.2 of [[../05-Ethics-Core/02-Hardware-Enforced-Isolation]]), making pre-silicon logic validation essential.

**Phase classification:** This is a **software simulation study** that runs in parallel with Phase A-2 (IVE evidence integration), using the same intent/rest classification outputs from Phase A-1. No hardware is required; no human subjects are involved.

**Method:**

1. **Input generation.** From the Phase A-1 frozen pipeline, extract: (a) all verified-intent command descriptors (action, target, confidence); (b) a set of 50 synthetic prohibited-intent descriptors covering all Tier 1 categorical prohibitions (§12.1.2 of [[../05-Ethics-Core/03-Formal-Constraint-Specification]]); (c) 20 synthetic assembly sequences (individually innocent actions forming harmful sequences).

2. **CVB constraint evaluation.** Implement the Ethics Core's constraint lookup logic in Python (the OTP truth-table fragment from SAT compilation of the deontic temporal logic specification). For each command descriptor, evaluate against the Tier 1 and Tier 2 constraint tables and record PERMIT/VETO decisions.

3. **Harm function evaluation.** Compute $H(a, c)$ for each command using the Stage 1 lookup-based implementation (§12.1.4 of [[../05-Ethics-Core/03-Formal-Constraint-Specification]]). Verify that all Class I/II actions score below $\theta_{\mathrm{risk}}$ and all synthetic prohibited actions score above.

4. **Assembly-risk scoring.** Run the signature kernel assembly detection and reward machine monitors (§12.1.5) on the synthetic assembly sequences. Verify that the assembly-risk score correctly elevates above the SOFT_VETO threshold.

**Verification criteria:**

| Test | Criterion |
|------|-----------|
| All valid intents pass constraint evaluation | 100% PERMIT rate on Phase A-1 verified intents |
| All prohibited intents are correctly vetoed | 100% VETO rate on synthetic Tier 1 violations |
| Veto evaluation latency | <50 µs per command (simulated clock cycles) |
| Assembly detection | All 20 synthetic assemblies trigger SOFT_VETO |

**Deliverable:** Constraint logic test suite (reusable for Phase B FPGA verification and Phase C ASIC verification). Minimum test-vector set for Ethics Core validation — see OQ 14.3 in [[../10-Analysis/02-Open-Questions]].

**Timeline:** ~2 days, parallel with Phase A-2. No additional data collection required.

---

## §7.8 Phase B-1 — Harmonic-Mode-Duration Simulation (THINK Mode Pre-Validation)

**Purpose:** Address OQ 11.106 — can the system maintain stable sustained harmonic modes for ~1000 ms in the absence of external input under modified TTSA that preserves rather than minimises $H^1(\mathcal{F})$? This is the empirically testable instantiation of the THINK mode mechanism (§2.14.9 of [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]]) under the COGITATE-observed sustained-activity timescale (200–1500 ms).

**Phase classification:** This is a **pre-Phase-B simulation study**, not a Phase A sub-phase. It does not touch PhysioNet EEG data; it operates entirely on simulated sheaf states. It is positioned between Phase A-1 (which requires actual TTSA-learned restriction maps) and Phase B (FPGA prototyping) — call it **Phase B-1** for sequencing purposes. Pre-registration is recommended but not blocking, because no real-data inferences are at stake.

### §7.8.1 The mechanism under test

THINK mode (§2.14.9) preserves $H^1(\mathcal{F})$ by modifying the TTSA loss from the standard form $L = \mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}$ to a harmonic-aware form:

$$L_{\mathrm{THINK}}(\theta) = \mathbf{x}^\top L_{\mathcal{F}(\theta)} \mathbf{x} - \lambda_{\mathrm{harm}} \,\big\|\,\mathrm{proj}_{\ker L_{\mathcal{F}(\theta)}}\!\mathbf{x}\big\|^2$$

The second term *rewards* projection onto the kernel of the sheaf Laplacian — i.e., onto the harmonic component. The trade-off parameter $\lambda_{\mathrm{harm}}$ controls how strongly the system maintains harmonic structure vs minimising overall energy.

COGITATE 2025 found sustained activity for the duration of stimuli (200–1500+ ms). THINK mode must produce equivalent persistence in the absence of sensory input. The question is whether the harmonic-preservation mechanism is mathematically stable under reasonable $\lambda_{\mathrm{harm}}$ values, or whether it diverges / collapses.

### §7.8.2 Experimental design

**3 × 4 × 3 factorial simulation:**

| Factor | Levels | Notes |
|---|---|---|
| **$\lambda_{\mathrm{harm}}$** | 0.0, 0.5, 1.0, 2.0 | Trade-off parameter sweep; $\lambda_{\mathrm{harm}} = 0$ is the NORMAL-mode baseline |
| **Initial harmonic mass** | low (10 % of energy), medium (30 %), high (50 %) | How much of the initial sheaf state is in $H^1(\mathcal{F})$ at $t=0$ |
| **Restriction-map perturbation** | none, small (1 %), medium (5 %) | Tests robustness to imperfect TTSA-learned restriction maps |

3 × 4 × 3 = 36 conditions × 100 random seeds = 3,600 simulation runs.

### §7.8.3 Simulation protocol

For each condition:

1. Generate a synthetic sheaf graph with 40 nodes, 80 directed edges, restriction maps initialised from a Phase A-1 frozen checkpoint (or random orthogonal matrices if A-1 has not yet executed)
2. Initialise sheaf state $\mathbf{x}(0)$ with the specified harmonic-mass fraction allocated to $\ker L_{\mathcal{F}}$ and the rest in the gradient + curl components
3. Disable all sensory input (no V/S/K signals); the system operates on internal dynamics only
4. Run the modified TTSA dynamics for $T = 5000$ ms at 250 Hz (1250 cycles)
5. At each cycle, measure the harmonic-component magnitude $\|\mathrm{proj}_{\ker L_{\mathcal{F}}}\!\mathbf{x}(t)\|^2$
6. Log the trajectory of harmonic-component magnitude over the full 5-second window

### §7.8.4 Primary endpoints

**E1 (Primary) — Sustained harmonic preservation.** Under (initial harmonic mass = medium, $\lambda_{\mathrm{harm}} = 1.0$, no perturbation), does the harmonic-component magnitude remain $\geq 50 \%$ of its initial value for at least 1000 ms?

$$\frac{\|\mathrm{proj}_{\ker L_{\mathcal{F}}}\!\mathbf{x}(1000\,\mathrm{ms})\|^2}{\|\mathrm{proj}_{\ker L_{\mathcal{F}}}\!\mathbf{x}(0)\|^2} \geq 0.5$$

If yes, harmonic preservation is empirically demonstrated under the COGITATE-relevant timescale.

**E2 (Secondary) — Lyapunov stability.** The harmonic-component magnitude must be bounded (no divergence to infinity, no collapse to zero outside the decay envelope). Specifically:

$$0.1 \leq \frac{\|\mathrm{proj}_{\ker L_{\mathcal{F}}}\!\mathbf{x}(t)\|^2}{\|\mathrm{proj}_{\ker L_{\mathcal{F}}}\!\mathbf{x}(0)\|^2} \leq 2.0 \quad \text{for all } t \in [0, 5000]\,\mathrm{ms}$$

This is the chaos-vs-stability check. Divergence beyond 2× initial = chaotic instability; collapse below 0.1× = mechanism failure.

**E3 (Secondary) — $\lambda_{\mathrm{harm}}$ sensitivity.** Identify the $\lambda_{\mathrm{harm}}$ range that produces E1 + E2 success. Expected: a narrow window (e.g., $\lambda_{\mathrm{harm}} \in [0.5, 1.5]$); values too low fail E1, too high fail E2.

**E4 (Tertiary) — Robustness to restriction-map perturbation.** Does E1 + E2 success persist under medium (5 %) restriction-map perturbation? If not, THINK mode is fragile and requires precise TTSA learning before being deployable.

### §7.8.5 Gate criteria

| Endpoint | Criterion | Action if fails |
|---|---|---|
| E1 | Harmonic preservation $\geq 50 \%$ for 1000 ms | **THINK mode not deployable as specified.** Investigate whether the harmonic-aware TTSA loss form needs revision; consider attractor-based alternatives |
| E2 | Lyapunov stability across all 5 s | **Mechanism unstable.** $\lambda_{\mathrm{harm}}$ must be tuned more conservatively or the mechanism redesigned |
| E3 | $\lambda_{\mathrm{harm}}$ window identified | Calibration default value derived; lock into spec |
| E4 | E1+E2 hold under 5 % perturbation | THINK mode is deployable in realistic conditions; minor restriction-map errors do not destabilise |

### §7.8.6 Wall-clock and compute

Each simulation run: ~5 minutes single-threaded (small graph, modest TTSA dynamics). 3,600 runs total: ~12 days single-threaded, ~36 hours with 8-way `joblib` parallelism. **Fits in a single weekend with parallelism.**

### §7.8.7 Pre-registration

Because this is simulation only (no real-data inferences), pre-registration is **strongly recommended but not blocking**. A short OSF amendment specifying:

- $\lambda_{\mathrm{harm}}$ sweep values locked at registration
- Initial harmonic mass values locked
- Restriction-map perturbation values locked
- E1–E4 gate criteria locked
- Master simulation seed (42) locked
- Analysis script SHA-256 locked

would protect against post-hoc selection of "favourable" simulation conditions. If Phase A-1 has not yet executed, this can run independently using random orthogonal restriction maps as starting points.

**Executable implementation:** the deterministic simulator is locked in [[(C)-Phase-B1-Harmonic-Simulator]]. The script's SHA-256 hash is logged in the OSF manifest as `phase_b1_script_sha256`. The locked parameter values (the 3 × 4 × 3 factorial levels, the master seed 42, the gate thresholds E1 ≥ 0.5 and E2 ∈ [0.1, 2.0], the integration step 4 ms, the simulation window 5000 ms) are hard-coded in the script and protected by the hash lock. The smoke-test mode (`--smoke-test --n-seeds 3`) takes ~5 minutes and gives early indication of which outcome regime (A — works as specified, B — fragile, C — does not work) applies before committing to the full 3,600-run factorial.

### §7.8.8 What success means for the spec

If E1–E4 all pass, the THINK mode mechanism is empirically validated as a candidate substrate for COGITATE-observed sustained content. The spec's §2.14.9.3 COGITATE-anchor claim becomes operationally verified. THINK mode then has the strongest empirical grounding in the spec.

If E1 fails, THINK mode is not deployable as specified. The architectural commitment in §2.14.9 would need revision — possibly replacing the harmonic-aware loss with an attractor-based mechanism (e.g., explicit Hopfield-style fixed points in the engram bank serving as sustained-content carriers).

If E1 passes but E2 fails, the mechanism is unstable. $\lambda_{\mathrm{harm}}$ tuning becomes critical and possibly per-user. The deployment story for THINK mode becomes more complicated.

---

## §8 Datasets, Software, Reproducibility

### §8.1 Datasets

| Dataset | Subjects | Channels | Classes | Use |
|---------|----------|----------|---------|-----|
| PhysioNet EEGMMIDB (curated per Varbu et al. 2024) | 109 (103 after exclusions) | 64 | 2 (L/R MI) | A-0, A-1 primary |
| BCI Competition IV-2a | 9 | 22 | 4 (L/R/F/T) | A-0 secondary |
| Lee et al. (2019) | 54 | 62 | 2 (L/R) | A-3 only |

All via MOABB auto-download. MD5-verified.

### §8.2 Software Stack

```
python            >= 3.10
mne               >= 1.6
moabb             >= 1.1
pyriemann         >= 0.5
scikit-learn      >= 1.3
iisignature       >= 0.24  (signature kernel)
clifford          >= 1.4   (rotor ablation only)
geoopt            >= 0.5   (Stiefel manifold optimisation)
scipy             >= 1.11
numpy             >= 1.24
pingouin          >= 0.5   (statistical tests)
```

Environment pinned in `environment.yml`. Seeds managed via `numpy.random.default_rng(seed)` per experiment; all seeds logged in results JSON.

### §8.3 Reproducibility

- Pre-registration on OSF before any result examination
- Git commit hash logged with each run
- Raw results in versioned JSON; plots regenerable from raw
- Decision log: explicit record of Q1/Q2/Q3/Q4/Q5 outcomes
- All code open-source (MIT) at experiment conclusion

---

## §9 Decision Tree

```
Phase A-0 Preflight
    │
    └── Pipeline within 2 pp of MOABB? ─── no ──▶ Halt; repair pipeline
        │
        yes
        ▼
Phase A-1 Sheaf Core Factorial
    │
    └── C1: S-TTSA > S-rand, BF₁₀ > 3? ─── no ──▶ HALT. Sheaf has no value.
        │                                             Publish null result.
        │                                             Return to Riemannian-only architecture.
        yes
        ▼
    └── C2: (R8 + S) > R8, d > 0.2?      ─── no ──▶ Sheaf is auxiliary, not primary.
        │                                             Downgrade: use sheaf as IVE evidence only.
        yes
        ▼
    └── C4: stressor × rep significant?   ─── no ──▶ Graceful-degradation claim fails.
        │                                             Rewrite §4.5.5; proceed with caveat.
        yes
        ▼
Phase A-2 IVE Evidence Integration
    │
    └── C3: IVE-4 < IVE-1 FPR?            ─── no ──▶ Multi-evidence fusion adds no value.
        │                                             Simplify to single-evidence IVE.
        yes
        ▼
Phase A-3 Cross-Session Transfer
    │
    └── C5: Procrustes < 5 min to target? ─── no ──▶ Stage 2 requires full recal per session.
        │                                             Update §7.7; flag Stage 2 risk.
        yes (+ any C4/C3 caveats)
        ▼
Phase A-4 Quantisation (engineering input)
        │
        ▼
Phase A-5 Sensory-Anchored Inhibition (parallel; only if C1 passed)
    │
    └── E1: FULL reduces sensory-absent FPR ≥ 30%, BF₁₀ > 3? ─── no ──▶ Disable M3 (hallucination suppression).
        │                                                                Retain M1+M2 if their gates pass.
        yes
        ▼
    └── E2: sensory-dominance ratio ≥ 4:1 under FULL?           ─── no ──▶ Recalibrate β, γ;
        │                                                                if still low, disable M2 (π_sensory).
        yes
        ▼
    └── E3: prediction-drift bounded by Lyapunov estimate?      ─── no ──▶ Refine quadratic damping form.
        │                                                                Document partial-validation.
        yes
        ▼
    └── E4: DN_ONLY variance reduction ≥ 15% vs OFF?            ─── no ──▶ Disable M1 (divisive normalisation).
        │                                                                Document partial-mechanism deployment.
        yes
        ▼
    All three sensory-anchored inhibition mechanisms validated.
    Deploy §6 of (C)-05-Sensory-Anchored-Inhibition as Stage 1 default
    (operating-mode gated: NORMAL only).
        │
        ▼
Phase A-6 U-Node Reflexive Acceleration (parallel; only if C1 passed)
    │
    └── E1: ≥25% latency reduction for high-freq class?       ─── no ──▶ Disable U-tracking;
        │                                                                retain θ(c) only
        yes
        ▼
    └── E2: minority-class FPR inflation ≤0.5pp?              ─── no ──▶ SAFETY HALT — disable
        │                                                                U-mechanism regardless of E1
        yes
        ▼
    └── E3: high-risk-label class slower under U-ON?           ─── no ──▶ Recalibrate ρ in Phase B
        │
        yes
        ▼
    └── E4: cache-hit rate ramps monotonically?                ─── no ──▶ Deploy without procedural cache
        │
        yes
        ▼
    Full sub-package A (Habit Acceleration) validated.
    Promotes from Stage 2.5 candidate to Phase B implementation target
    (~12-month acceleration of the developmental-cogitation timeline).
        │
        ▼
Proceed to Phase B (FPGA prototype) with:
    - confirmed core architecture (A-1 to A-3)
    - quantitative bit-width requirements (A-4)
    - validated sensory-anchored inhibition configuration (A-5)
    - validated U-node mechanism for Habit Acceleration sub-package (A-6)
```

The Phase A-5 sub-tree permits **partial validation**: each of the three §6 mechanisms (M1 divisive normalisation, M2 sensory-priority precision, M3 hallucination suppression) can be independently disabled at deployment based on its individual gate, rather than requiring all-or-nothing acceptance. This matches the operating-mode gating already specified in §6.4.2 of [[../03-Architecture/(C)-05-Sensory-Anchored-Inhibition]].

---

## §10 Relationship to Spec Open Questions

This experiment directly addresses several Open Questions from [[../10-Analysis/02-Open-Questions]]:

| OQ | Claim tested by |
|----|-----------------|
| OQ 15 (sheaf over baseline) | C1, C2 (Phase A-1) |
| OQ 19 (Phase 1 transfer) | C5 (Phase A-3) |
| OQ 11.7 (Procrustes transfer) | C5 (Phase A-3) |
| OQ 11.35 (regional ACP min node count) | C2 ablation (stalk dim 4, 6, 8) |
| OQ 11.41 (S/K-node calibration) | Not addressed — future Phase A′ extension |
| OQ 11.42 (Bayesian lens convergence) | Partially — via TTSA convergence diagnostics |

Phase A does not address: port-Hamiltonian passivity (simulation-level, not measurable offline), soliton propagation (FPGA-level, Phase B), or Ethics Core constraints (policy-level).

---

## §11 Known Limitations (Pre-Declared)

1. **No visual/audio/motion context.** V/S/K nodes require multimodal recordings not present in MI datasets. Evidence 5 fixed to constant 1.0.
2. **FPR 1/hour target is extrapolated, not measured.** Insufficient rest data in any open dataset.
3. **Offline only.** Pseudo-online via MOABB chronological split; true online validation requires a wearable rig (Phase B).
4. **Binary / 4-class only.** Stage 2 prosthetics will require continuous motor decoding, not addressed here.
5. **No ethics constraint testing.** Ethics Core requires policy-level simulation separate from neural decoding.
6. **Single-session TTSA.** Multi-session TTSA dynamics (concept drift, topology evolution) not tested.
7. **A-node proxy validity unvalidated.** DA/ACh/5-HT/NE proxies (§3.3 of [[../03-Architecture/01-Node-Types-Dynamics]]) are assumed to carry the signal the spec claims; MI datasets cannot test this directly.

---

## §12 Timeline

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1 | A-0 + A-1 setup | Reproduced MOABB baseline; factorial pipeline ready; OSF pre-registration submitted |
| 2 | A-1 execution | Raw results for 109 × 20 = 2,180 conditions |
| 3 | A-1 analysis | Statistical report; C1, C2, C4 gate decisions |
| 4 | A-2 | IVE evidence integration; C3 gate |
| 5 | A-3 + A-4 + A-5 + A-6 (parallel) | Cross-session transfer; quantisation study; sensory-anchored inhibition validation (3×4×2 factorial, 12,360 paired observations; E1–E4 gate decisions); U-node reflexive-acceleration validation (2×3×4 factorial, 12,360 paired observations; E1–E4 gate decisions inc. minority-FPR safety gate) |
| 6 | Write-up | Final report; preprint draft; GitHub release |

Phases A-5 and A-6 run in parallel with A-3 and A-4 during Week 5 — both use frozen restriction maps from A-1. A-5 adds synthetic V/S/K signals plus §6 inhibition mechanisms (~2 days wall-clock at 8-way parallelism). A-6 adds synthetic-risk labels plus imbalanced trial schedules plus the §2.14 U-node mechanism (~3 days at 8-way parallelism). Both fit comfortably within Week 5 alongside the engineering-oriented phases.

Total: 6 weeks, one operator, commodity hardware.

---

## §13 Ethical Considerations

All data is publicly available, anonymised, under open licence (PhysioNet ODC-BY; BCI Competition re-release terms; Lee et al. 2019 open release). No new human data collected. No IRB required.

All code and results open-sourced (MIT licence) at experiment conclusion, supporting open-science reproducibility per the MOABB initiative.

---

## §14 Appendix — Statistical Power Calculations

Two complementary approaches are reported. **(A) Concentration-of-measure bounds** are distribution-free and rigorous, derived from Hoeffding/McDiarmid inequalities (§2.10 of [[../02-Theory/(C)-09-Concentration-of-Measure]]). **(B) G*Power 3.1** uses Gaussian/parametric assumptions and is tighter when those assumptions hold. Reporting both gives reviewers the spread between "rigorous worst-case" and "expected-case under standard assumptions".

### §14.1 Within-Subject Contrasts (A-1)

- 109 subjects (103 after Varbu et al. 2024 exclusions), paired comparisons in $[-1, 1]$.
- **(A) Hoeffding bound:** $\varepsilon_{\min} = \sqrt{2\log(1/\alpha)/N} \approx 0.024$ at $N = 103$, one-sided $\alpha = 0.05$. **Minimum detectable mean accuracy difference: 2.4 pp.**
- **(B) G*Power 3.1:** paired t-test, one-sided, α = 0.05, power = 0.80. Minimum detectable Cohen's $d = 0.12$ (small). For typical paired-difference SD ≈ 0.05, this corresponds to ~0.6 pp.
- Typical BCI paradigm comparison effect: $d = 0.3$–$0.5$ (medium to large), corresponding to ≈ 1.5–2.5 pp difference. **Detectable under both bounds.**

**Headroom argument (added May 2026 after MOABB-baseline correction).** The Hoeffding 2.4 pp floor and the G*Power 0.6 pp floor are stated in absolute units and are **independent of where the baseline accuracy sits**. What does change with the corrected ~67 % PhysionetMI L/R baseline is the **headroom above the floor**: at the original 92 %-baseline assumption, only ~8 pp separated the baseline from the 100 % ceiling, so a sheaf-coherence win of, say, +5 pp would have meant the sheaf was operating in the saturation regime where small per-subject perturbations translate into large effect-size estimates and ceiling effects make the comparison less informative. At the verified ~67 % baseline, there are ~33 pp of headroom — a +5 pp sheaf win lifts to ~72 %, comfortably mid-range, where paired-difference variance is well-behaved and effect-size estimates are not inflated by ceiling clipping. **The corrected baseline therefore strengthens, not weakens, the operational interpretation of the H1–H10 paired-difference tests:** the same Cohen's-d criterion is easier to interpret in absolute pp terms, and a positive sheaf result cannot be dismissed as "ceiling artefact" because there is no ceiling to clip against in the operational regime.

### §14.2 Interaction Effect (A-1 C4)

- Repeated-measures ANOVA, 5 × 4 design, 109 subjects
- **(A) McDiarmid bound** on the interaction F-statistic gives distribution-free 99% confidence intervals at the planned sample size (§2.10.5 of [[../02-Theory/(C)-09-Concentration-of-Measure]]).
- **(B) G*Power 3.1:** f = 0.15 (small), α = 0.05 → achieved power > 0.99
- **Interaction detection is not the bottleneck under either approach.**

### §14.3 Cross-Session (A-3 C5)

- 54 subjects (Lee et al. 2019)
- Paired difference in calibration time
- Minimum detectable difference at 80% power: 1.2 minutes
- Target effect: Procrustes cuts calibration from ~20 min to < 5 min → effect size ~5× minimum detectable

### §14.4 FPR CIs (A-2 C3)

- Bootstrap 95% CI with 1,000 resamples
- At TPR = 0.85 with 109 subjects, typical FPR CI width ≈ ±3 pp
- Sufficient to detect 5 pp absolute FPR differences between IVE levels

---

## References

Brunner, C., Leeb, R., Müller-Putz, G., Schlögl, A., & Pfurtscheller, G. (2008). BCI Competition 2008 — Graz dataset A. *TU Graz*.

Carrara, I., & Aristimunha, B. (2023). Pseudo-online framework for BCI evaluation: A MOABB perspective. *arXiv:2308.11656*.

Chevallier, S., et al. (2024). The largest EEG-based BCI reproducibility study for open science: The MOABB benchmark. *arXiv:2404.15319*.

Di Nino, S., Barbarossa, S., & Di Lorenzo, P. (2025). Learning the structure of connection graphs. *arXiv:2510.11245*.

Gómez-Morales, Ó. W., Escalante-Escobar, S., Collazos-Huertas, D. F., Álvarez-Meza, A. M., & Castellanos-Domínguez, G. (2025). Uncertainty-aware deep learning for robust and interpretable MI EEG using channel dropout and LayerCAM integration. *Applied Sciences*, 15(14), 8036.

Jayaram, V., Alamgir, M., Altun, Y., Schölkopf, B., & Grosse-Wentrup, M. (2016). Transfer learning in brain-computer interfaces. *IEEE Computational Intelligence Magazine*, 11(1), 20–31.

Khanam, T., Siuly, S., Ahmad, K., & Wang, H. (2025). A novel channel reduction concept to enhance the classification of motor imagery tasks in brain-computer interface systems. *PLoS One*, 20(10), e0335511.

Kruschke, J. K. (2013). Bayesian estimation supersedes the t test. *Journal of Experimental Psychology: General*, 142(2), 573–603.

Lee, M.-H., et al. (2019). EEG dataset and OpenBMI toolbox for three BCI paradigms. *GigaScience*, 8(5), giz002.

Mullen, T. R., Kothe, C. A. E., Chi, Y. M., Ojeda, A., Kerth, T., Makeig, S., Jung, T.-P., & Cauwenberghs, G. (2015). Real-time neuroimaging and cognitive monitoring using wearable dry EEG. *IEEE Transactions on Biomedical Engineering*, 62(11), 2553–2567.

Muthukumaraswamy, S. D. (2013). High-frequency brain activity and muscle artifacts in MEG/EEG: A review and recommendations. *Frontiers in Human Neuroscience*, 7, 138.

Rodrigues, P. L. C., Jutten, C., & Congedo, M. (2019). Riemannian Procrustes analysis: Transfer learning for brain–computer interfaces. *IEEE Transactions on Biomedical Engineering*, 66(8), 2390–2401.

Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004). BCI2000: A general-purpose brain-computer interface (BCI) system. *IEEE Transactions on Biomedical Engineering*, 51(6), 1034–1043.

Seely, J. (2025). Sheaf Cohomology of Linear Predictive Coding Networks. *NeurReps 2025* (NeurIPS workshop). arXiv:2511.11092.

Varbu, K., et al. (2024). Increasing accessibility to a large brain–computer interface dataset: Curation of PhysioNet EEG Motor Movement/Imagery Dataset. *Data in Brief*, 54, 110371.

Wald, A. (1945). Sequential tests of statistical hypotheses. *Annals of Mathematical Statistics*, 16(2), 117–186.

Whitham, E. M., Pope, K. J., Fitzgibbon, S. P., Lewis, T., Clark, C. R., Loveless, S., Broberg, M., Wallace, A., DeLosAngeles, D., Lillie, P., Hardy, A., Fronsko, R., Pulbrook, A., & Willoughby, J. O. (2007). Scalp electrical recording during paralysis: Quantitative evidence that EEG frequencies above 20 Hz are contaminated by EMG. *Clinical Neurophysiology*, 118(8), 1877–1888.

Wolpaw, J. R., Birbaumer, N., McFarland, D. J., Pfurtscheller, G., & Vaughan, T. M. (2002). Brain–computer interfaces for communication and control. *Clinical Neurophysiology*, 113(6), 767–791.

Wu, D., Xu, Y., & Lu, B.-L. (2022). Transfer learning for EEG-based brain-computer interfaces: A review of progress made since 2016. *IEEE Transactions on Cognitive and Developmental Systems*, 14(1), 4–19.

Wu, D., et al. (2024). T-TIME: Test-time information maximization ensemble for BCIs. *arXiv:2412.07228*.
