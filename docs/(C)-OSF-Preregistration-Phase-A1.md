# OSF Preregistration — thrIVE Phase A-1

**Form:** OSF Standard Pre-Data Collection Registration v1.0
**Status:** Draft for review and submission to osf.io
**Date prepared:** April 2026
**Submission target:** [https://osf.io/registries/](https://osf.io/registries/) → "Create new preregistration" → "OSF Preregistration"

---

## Instructions for Submission (Read First)

1. Create a free OSF account at [https://osf.io/](https://osf.io/) using ORCID or email.
2. Create a new project titled exactly as in §1 below.
3. From the project, click **Registrations → New registration → OSF Preregistration**.
4. Paste each numbered section's content into the matching OSF form field. Field names below are the exact OSF labels as of April 2026.
5. Upload the [[(C)-Phase-A-Experiment-Revised]] document, [[(C)-Phase-A-Experiment-Code-Revised]] code scaffold, and this preregistration as supplementary materials before clicking **Register**.
6. After submission, OSF assigns a permanent DOI. Record it in [[(C)-Phase-A-Experiment-Revised]] §0 and in the project's `manifest_*.json`.
7. **Do not download data or run any code that touches data until the DOI is issued.** This is the integrity guarantee.

---

## §1 — Title

> Sheaf-Coherence Falsification on Motor Imagery EEG: A Multi-Stressor Factorial Test of the thrIVE Architecture's Load-Bearing Claims, with EEG Foundation Model, Dual JEPA (LeWorldModel cross-domain + Brain-/Signal-JEPA domain-specific), Graph-Laplacian Cohomology-Isolation, BCI Mainstream Ensemble, and Dynamical-Architecture Streaming Baselines

---

## §2 — Description

This study tests whether unsupervised TTSA learning of restriction maps on the predictive-coding energy of a cellular sheaf produces sheaf coherence that discriminates motor imagery states on real EEG, recovers information lost by eigenvalue channel selection, and degrades gracefully under channel dropout and EMG artefact injection — three load-bearing claims of the thrIVE Brain-Computer Interface architecture (Cognat, 2026).

The sheaf-theoretic predictive-coding framework follows Seely et al. (2025), who proved $E_{\mathrm{PC}} = \mathbf{x}^\top L_\mathcal{F} \mathbf{x}$ for linear predictive coding networks. thrIVE's Phase A-1 is the first empirical test on biological EEG of whether this equivalence yields discriminative coherence under the unsupervised TTSA learning rule (Borkar, 2008).

The experiment uses a 5 × 4 within-subject factorial design (representation × stressor) on PhysioNet EEG Motor Movement/Imagery Dataset (Schalk et al., 2004; Varbu et al. 2024 curation) with all 109 subjects. Five representations are tested: Riemannian tangent space at $d=32$ (R32, ceiling), Riemannian tangent at $d=8$ after eigenvalue channel selection (R8, baseline), random-restriction-map sheaf coherence (S-rand, null), unsupervised-TTSA sheaf coherence (S-TTSA, hypothesis), and concatenated R8 + S-TTSA features (R8+S, value-add test). Four stressors are tested: clean (S0), 2-of-32 channel dropout per epoch (S1), 0 dB EMG contamination on 25% of epochs (S2), and leave-one-subject-out cross-validation (S3).

Three confirmatory hypotheses test the five load-bearing claims. Pre-registered Bayesian and frequentist analysis plans, fixed bootstrap and BEST procedures, and explicit halt conditions for each hypothesis are specified. All code, raw data, and analysis scripts will be released under MIT licence at experiment completion.

### Amendment summary table (Amendments 1, 2, 3, 4)

The original preregistration (H1–H3 above) has been extended by four pre-submission amendments. Each adds factor levels and hypotheses without modifying the original Phase A-1 5 × 4 design:

| Amendment | Section | Adds | Hypothesis | Locked artefact |
|---|---|---|---|---|
| **1** — EEG Foundation Model Baseline | §9 | R_FM, R_FM+S factor levels (foundation-model features at d = 8) | **H4**: (R_FM + S) > R_FM at S0; sheaf adds value over modern SOTA representation baseline | [[(C)-R_FM-Feature-Extraction]] |
| **2** — LeWorldModel End-to-End JEPA Baseline (cross-domain control) | §10 | R_JEPA, R_JEPA+S factor levels (minimal-prior end-to-end JEPA from vision domain) | **H5**: (R8 + S) > R_JEPA at S0; sheaf structure earns its representational complexity against cross-domain JEPA | [[(C)-R_JEPA-Feature-Extraction]] |
| **3a** — Phase A-7 Dynamical Comparison vs LeWM | §11.2 | 2 × 4 × 5 streaming-mode factorial; thrIVE-dynamic vs R_JEPA-streaming | **H6**: thrIVE's dynamical architecture beats LeWM on streaming endpoints E1′ / E2 / E3′ / E4 / E6 / E7′ | [[(C)-Phase-A7-Digital-ACP-Twin]] |
| **3b** — Phase A-7′ Comparison vs BCI Mainstream Ensemble | §11.3 | 2 × 4 × 4 streaming-mode factorial; thrIVE-composite vs locked mainstream ensemble | **H7**: thrIVE's dynamical architecture beats the actual deployable BCI alternative (SPRT-Liu + TSFNet + T-TIME + ST-EEGFormer features + memory-buffer continual) | [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]] |
| **3c** — Phase B-2 §2.16 Component Validation (optional) | §11.4 | Three components (curiosity reward, equilibration trigger, autopoietic monitor) added to ACP twin | **H8 (optional)**: §2.16.3 / §2.16.5 / §2.16.6 mechanisms work as designed on streaming data | Phase B-2 extension of [[(C)-Phase-A7-Digital-ACP-Twin]] |
| **4** — Brain-JEPA / Signal-JEPA Domain-Specific Baseline | §12 | R_JEPA_brain, R_JEPA_brain+S factor levels (domain-specific JEPA with spatial / channel-wise masking and pre-local processing) | **H9**: (R8 + S) > R_JEPA_brain at S0; sheaf structure earns complexity against domain-appropriate JEPA (the harder test than H5) | [[(C)-R_JEPA-Brain-Feature-Extraction]] |
| **5** — Graph Laplacian Baseline (the cohomology-isolation test) | §13 | R_GL, R_GL+S factor levels (same graph topology, identity restriction maps, no cohomology) | **H10**: (R8 + S) > R_GL at S0; cellular cohomology — not just graph topology — earns empirical value | [[(C)-R_GL-Feature-Extraction]] |

The original H1 halt condition (sheaf has no value at d = 8) still terminates the experiment if it fails. H4 through H8 are evaluated independently if H1 passes; their joint outcomes determine the full architectural verdict via the five-hypothesis interpretation matrix (§11.6).

**Reviewer note:** the amendments are designed to be **independently revocable**. If Amendment 3b (mainstream ensemble) is judged too costly, sub-§11.3 can be deferred without affecting Amendments 1, 2, or 3a. Each amendment has self-contained gate criteria and integrity statements.

### Alternative-architectural-identity outcome paths (what this study can falsify)

This preregistration is designed so that **every plausible outcome — including total failure of the sheaf claim — produces a well-defined alternative architectural identity** for the thrIVE BCI. The architecture is not "all-or-nothing"; each hypothesis failure corresponds to a specific, pre-committed downgrade path, not an arbitrary post-hoc rescue. The five paths below are the *only* architectural identities the PI commits to in advance:

| Outcome cluster | Alternative architectural identity thrIVE collapses to |
|---|---|
| **H1 fails** (S-TTSA ≤ S-rand at S0) | **No-sheaf identity.** The sheaf layer is removed entirely. thrIVE Stage 1 becomes a Riemannian-tangent + IVE-without-Evidence-1 BCI. §2.1–§2.13 of the spec are deprecated; Phase A-2/3/4 are not run. Published as a null result. |
| **H1 passes, H2 fails** (sheaf discriminates but does not augment R8) | **IVE-only-sheaf identity.** Sheaf coherence is retained but only as IVE Evidence 1 (the safety verification channel), not as a primary classifier feature. The §4.5 IVE architecture is preserved; the §3 classification spine reverts to Riemannian-only. |
| **H10 fails alone** (sheaf > all other baselines but ≤ R_GL on same topology) | **Graph-Laplacian-spectral identity.** Cellular cohomology is operationally decorative for the Phase A-1 motor-imagery task. Stage 1 uses graph-Laplacian eigenmode features on the same Yeo-17-scale topology; the sheaf is restricted to IVE Evidence channels only (where higher cohomology $H^1$ is justified by the obstruction-class semantics, not classification accuracy). This is the **cohomology-isolation** outcome flagged by the external audit (May 2026). |
| **H5 and H9 both fail** (sheaf ≤ both JEPA families) | **Domain-specific-JEPA identity.** The sheaf representational claim does not survive against end-to-end learned encoders. Stage 1 representation becomes a Brain-/Signal-JEPA-style encoder (Yi et al., 2024; Guetschel et al., 2024); the dynamical-architecture commitments (H6 / H7) and the IVE safety architecture are evaluated independently. |
| **H6 and H7 both fail** (dynamical architecture loses on streaming) | **Mainstream-ensemble identity.** The dynamical spine collapses to the locked BCI mainstream ensemble (SPRT-Liu + TSFNet + T-TIME + ST-EEGFormer + memory-buffer continual learning) operationalised in Amendment 3b. The representational claims (H1 / H2 / H4 / H5 / H9 / H10) are evaluated independently of this collapse. |
| **All confirmatory hypotheses fail** | **Fundamental halt.** Both representational and dynamical commitments are unjustified. Major spec revision required before any Stage 2 (prosthetics) or Stage 3 (AGI substrate) work proceeds. Published as a comprehensive negative result with the full alternative-identity table as the value-delivery. |

The PI commits to **publishing the surviving alternative identity** regardless of which outcome cluster occurs. The architectural value of this preregistration is not "the sheaf works"; it is **a falsifiable, pre-committed sequence of architectural fall-backs** that ensures the BCI architecture is decided by the data and not by post-hoc selection. Reviewers should treat the joint interpretation matrices in §9.6, §10.5, §11.6, §12.5, and §13.5 as the *formal* outcome logic; this table is the high-level reviewer-facing summary of the same logic for the OSF Description.

---

## §3 — Hypotheses

The study tests three confirmatory hypotheses, each corresponding to a thrIVE load-bearing claim. **Halt criteria are pre-specified** — failure of H1 terminates the experiment without further analysis.

### H1 (Claim C1) — Sheaf coherence is discriminative

Unsupervised TTSA learning on the predictive-coding energy produces sheaf coherence values $C(t)$ that discriminate left-hand from right-hand motor imagery on PhysioNet EEGMMIDB more accurately than random Stiefel-manifold restriction maps, on clean data (Stressor S0).

- **Directional prediction:** mean classification accuracy of S-TTSA > mean classification accuracy of S-rand at S0
- **Strength criterion:** Bayes factor $\mathrm{BF}_{10} > 3$ via paired BEST (Kruschke, 2013)
- **Halt condition:** if H1 fails, the experiment terminates. Phase A-2, A-3, A-4 are not run. The sheaf layer provides no measurable value on real EEG and should be removed from the thrIVE architecture.

### H2 (Claim C2) — The sheaf layer recovers information

Sheaf coherence augments per-node Riemannian tangent features rather than merely reproducing them: classification using concatenated R8 tangent vectors and S-TTSA coherence outperforms classification using R8 tangent vectors alone, on clean data (S0).

- **Directional prediction:** mean accuracy of (R8+S) > mean accuracy of R8 at S0
- **Strength criterion:** paired Cohen's $d > 0.2$ (small effect threshold), one-sided $\alpha = 0.05$
- **Failure interpretation:** sheaf coherence is auxiliary, not primary. Architecture proceeds with sheaf coherence only as IVE Evidence 1, not as a classifier feature.

### H3 (Claim C4) — Sheaf coherence degrades gracefully

Sheaf coherence is more robust to channel dropout and EMG contamination than the Riemannian tangent baseline. The accuracy decrement from S0 to S1 (channel dropout) and from S0 to S2 (EMG injection) is significantly smaller for S-TTSA than for R8.

- **Directional prediction:** $\mathrm{accuracy}(\mathrm{S\_TTSA}, \mathrm{S0}) - \mathrm{accuracy}(\mathrm{S\_TTSA}, \mathrm{S}_k) < \mathrm{accuracy}(\mathrm{R8}, \mathrm{S0}) - \mathrm{accuracy}(\mathrm{R8}, \mathrm{S}_k)$ for $k \in \{1, 2\}$
- **Strength criterion:** representation × stressor interaction, $F$-test from rmANOVA, $p < 0.05$ (uncorrected); pairwise contrasts via Holm-Bonferroni
- **Failure interpretation:** the IVE's graceful-degradation claim (§4.5.5 of [[../03-Architecture/02-Cellular-Sheaf-Architecture]]) is not supported. Documentation revises that section; architecture proceeds without graceful-degradation guarantees.

### Exploratory questions (not preregistered hypotheses)

- E1: Does R32 outperform R8 (cost of eigenvalue channel selection)? — informs channel selection threshold (OQ 11.19).
- E2: Does S-TTSA accuracy correlate with sheaf graph topology choice (physical / functional / SCGL / fully-connected / permuted-null)?
- E3: Does the LOSO stressor (S3) produce systematically lower accuracy than within-subject stressors (S0–S2)? — informs the calibration-free claim (§7.7 of [[../07-Implementation/01-Calibration-Deployment]]).
- E4: Subject-level analysis — what fraction of the 109 subjects achieve $C(t)$ separability $>0.6$ AUC at S0?

---

## §4 — Design Plan

### Study type
**Observational** with experimental manipulation of preprocessing pipeline. No human intervention. Re-analysis of an existing public dataset (PhysioNet EEGMMIDB).

### Blinding
**No blinding required** — all conditions are computational. The analyst (PI) does not see any test-fold accuracy until all conditions for all 109 subjects are computed and the full results table is finalised. Per-subject results are written to JSON sequentially and not aggregated until the analysis script runs at the end.

**Blinding-equivalent procedure:** the analysis script (`analyse_a1_factorial`) is fixed in the GitHub repository **before** any test-fold accuracy is computed. The script's hash is logged in the run manifest. Any modification to the analysis script after results are computed must be documented as a deviation in the OSF registration.

### Study design

5 × 4 × 5 within-subject factorial:
- **Factor 1 (Representation):** R32, R8, S-rand, S-TTSA, R8+S — 5 levels
- **Factor 2 (Stressor):** S0 (clean), S1 (channel dropout), S2 (EMG contamination), S3 (LOSO generalisation) — 4 levels
- **Factor 3 (Fold):** 5-fold chronological cross-validation within subject (S0–S2) or LOSO across subjects (S3) — 5 folds

Fully crossed within-subject: every subject contributes one observation to each of the 20 (representation × stressor) cells.

### Randomisation

- **Random seeds:** master seed = 42, logged in run manifest. All sub-procedures (TTSA initialisation, S-rand orthogonal initialisation, S2 stressor injection, bootstrap resampling, LOSO subject ordering) derive deterministic seeds from the master via SHA-256 of `{master_seed}|{procedure_name}|{subject_id}|{fold}`.
- **Subject order:** processed in ascending subject ID (1, 2, …, 109) to ensure deterministic execution; no per-subject randomisation since within-subject design.
- **Fold construction:** chronological 5-fold (test = strictly later in time than training) to approximate pseudo-online evaluation (Carrara & Aristimunha, 2023).

---

## §5 — Sampling Plan

### Existing data
**Yes, existing data.** PhysioNet EEG Motor Movement/Imagery Dataset (Schalk et al., 2004), publicly hosted at [https://physionet.org/content/eegmmidb/1.0.0/](https://physionet.org/content/eegmmidb/1.0.0/). License: Open Data Commons Open Database License (ODbL).

The dataset has been available since 2004; the PI has not yet downloaded the dataset for this study and has not analysed it for the registered hypotheses. **The PI has previously read published results on this dataset** (MOABB benchmark, Chevallier et al., 2024) and has knowledge of approximate Riemannian-baseline accuracy (~67% binary left/right MI; corrected May 2026 from the earlier ~92% figure which applies to the right-hand-vs-feet paradigm). This knowledge is reflected in §6's Phase A-0 preflight gate criterion (within 4 percentage points of published) and does not bias the registered H1, H2, H3 contrasts.

### Explanation of existing data

- **Why this dataset:** largest open MI dataset (109 subjects), most commonly benchmarked, MOABB-compatible. Limitations: known annotation errors corrected via Varbu et al. (2024); 6 subjects with anomalies (88, 89, 92, 100, plus 2 others per Varbu) excluded per Varbu's published exclusion list.
- **Why not BCI Competition IV-2a:** smaller (9 subjects), four-class. Used in Phase A-0 preflight only.
- **Why not Lee et al. (2019):** reserved for Phase A-3 cross-session transfer (not preregistered here).

### Data collection procedures
Not applicable — no new data collection. Data downloaded via `mne.datasets.eegbci.load_data()` to local storage. Varbu et al. (2024) annotation corrections applied programmatically per their published `apply_curation()` script.

### Sample size
**N = 103 subjects** (109 total minus 6 Varbu et al. exclusions: subjects 88, 89, 92, 100, 104, 106).

Within each subject: approximately 45 left-hand and 45 right-hand motor imagery epochs from runs 4, 8, 12 (Schalk et al. 2004 protocol).

Total observations: 103 subjects × 5 representations × 4 stressors × 5 folds = 10,300 paired observations.

### Sample size rationale

**Two complementary calculations are reported for completeness.**

**(A) Concentration-of-measure bound (rigorous).** For each subject the paired difference $\Delta_i = \mathrm{acc}_i^{\mathrm{TTSA}} - \mathrm{acc}_i^{\mathrm{rand}}$ is bounded in $[-1, 1]$. Hoeffding's inequality (§2.10.7 of [[../02-Theory/(C)-09-Concentration-of-Measure]]) gives:

$$\Pr(|\bar{\Delta} - \mathbb{E}\Delta| \geq \varepsilon) \leq 2\exp(-N\varepsilon^2 / 2)$$

For $N = 103$ and one-sided $\alpha = 0.05$, the minimum detectable mean difference is $\varepsilon = \sqrt{2\log(1/\alpha)/N} \approx 0.024$ — i.e., **a 2.4 percentage-point difference in mean accuracy** is detectable with 95% confidence. This is a distribution-free bound that uses only the bounded support of accuracy values; no Gaussian assumptions.

**(B) G*Power 3.1 (variance-aware).** Paired t-test, one-sided, $\alpha = 0.05$, power $= 0.80$, $N = 103$ → minimum detectable Cohen's $d = 0.12$ (very small effect). For typical paired-difference SD ≈ 0.05, this corresponds to detecting a mean difference of $\approx 0.6$ pp.

The two bounds answer different questions: G*Power is tighter when paired-difference variance is small, Hoeffding is rigorous without distributional assumptions. Reporting both gives reviewers the spread. Typical BCI paradigm-comparison effect sizes are $d \in [0.3, 0.5]$ (medium to large); the design is therefore overpowered for primary contrasts under either bound.

For the rmANOVA interaction effect (H3), G*Power calculates: 5 × 4 design, 103 subjects, Cohen's $f = 0.15$ (small), $\alpha = 0.05$ → achieved power $> 0.99$. McDiarmid's inequality applied to the interaction F-statistic (§2.10.5 of [[../02-Theory/(C)-09-Concentration-of-Measure]]) gives a corresponding distribution-free bound. Interaction detection is not the bottleneck under either approach.

For the bootstrap CIs on FPR (Phase A-2, not preregistered here), CI half-width at 95% confidence is typically ±3 percentage points for sample sizes >100. Note: per §2.10.3 of [[../02-Theory/(C)-09-Concentration-of-Measure]], direct empirical verification of the deployment-time 1 FP/hour target is infeasible at any practical sample size; A-2 reports calibration-time empirical bounds and Weibull-extrapolated deployment-time predictions as separate quantities.

### Stopping rule

**Halt criterion 1 (Phase A-0 preflight):** if MOABB Riemannian baseline reproduction fails (>4 percentage points from published ~67% on EEGMMIDB binary left/right MI; corrected May 2026), halt. The pipeline has a bug; experiment is invalid.

**Halt criterion 2 (H1 falsification):** if H1's $\mathrm{BF}_{10} \leq 3$ at the planned sample size, halt without analysing H2 or H3. Report null result.

**No data-dependent stopping otherwise.** Sample size is fixed at $N = 103$ before data acquisition. No optional stopping, no peeking.

---

## §6 — Variables

### Manipulated variables
- **Representation** (5 levels): R32, R8, S-rand, S-TTSA, R8+S — defined operationally in §4 of [[(C)-Phase-A-Experiment-Revised]]
- **Stressor** (4 levels): S0 (clean), S1 (channel dropout, $n=2$), S2 (EMG injection at 0 dB SNR on 25% of epochs), S3 (LOSO)
- **Fold** (5 levels): chronological CV (S0–S2) or LOSO ordering (S3)

### Measured variables
- **Primary:** classification accuracy (mean of 5 folds per subject per condition)
- **Secondary:** AUC-ROC, Cohen's $\kappa$, $d'$ (sensitivity index)
- **Tertiary:** information transfer rate (Wolpaw et al., 2002) at decision time = 4 s
- **Diagnostic (not for hypothesis testing):** TTSA convergence iteration count, final predictive-coding energy $\mathbb{E}_t[\mathbf{x}^\top L_\mathcal{F} \mathbf{x}]$, sheaf Laplacian spectral gap $\lambda_1$, sheaf coherence distribution histograms

### Indices

The five primary contrasts are pre-defined as differences between paired condition means:

| Contrast | Cells compared | Tests |
|----------|----------------|-------|
| Δ_C1 | S-TTSA, S0 minus S-rand, S0 | H1 |
| Δ_C2 | (R8+S), S0 minus R8, S0 | H2 |
| Δ_C4_dropout | S-TTSA Δ(S0→S1) minus R8 Δ(S0→S1) | H3 |
| Δ_C4_emg | S-TTSA Δ(S0→S2) minus R8 Δ(S0→S2) | H3 |
| Δ_LOSO | (S-TTSA, S3) − (S-TTSA, S0) — exploratory | E3 |

---

## §7 — Analysis Plan

### Statistical models

**Primary model (H1, H3 supporting):** linear mixed-effects model
```
accuracy ~ representation * stressor + (1 | subject) + (1 | fold)
```
fitted via `lme4::lmer` in R (`pingouin.linear_regression` in Python via `statsmodels.MixedLM` for cross-platform reproducibility). Contrasts extracted via `emmeans::contrast` with Holm-Bonferroni correction across all H1, H2, H3 pairwise tests.

**H1 Bayesian test:** paired BEST (Kruschke, 2013) on subject-level mean accuracy of S-TTSA vs S-rand at S0. Computed via `pingouin.bayesfactor_ttest(t_statistic, nx=103, paired=True)`. $\mathrm{BF}_{10}$ thresholds: $> 10$ strong evidence, $> 3$ moderate evidence (preregistered threshold), $> 1$ anecdotal.

**H2 frequentist test:** paired Cohen's $d$ for (R8+S, S0) vs (R8, S0); one-sided test, $\alpha = 0.05$.

**H3 interaction test:** repeated-measures ANOVA via `pingouin.rm_anova` with `dv='accuracy'`, `within=['representation','stressor']`, `subject='subject'`. Greenhouse-Geisser correction applied automatically.

### Transformations

- Accuracy values are bounded in [0, 1]; for the linear mixed model, accuracy is logit-transformed: $\mathrm{logit}(p) = \log(p / (1-p))$.
- For BEST and Cohen's $d$, raw accuracies are used (no transformation) since paired differences are approximately Gaussian in [-1, 1].
- ITR values are reported in raw bits/minute.

### Inference criteria

- **H1:** confirmed if $\mathrm{BF}_{10} > 3$ AND mean(S-TTSA, S0) > mean(S-rand, S0). Refuted otherwise.
- **H2:** confirmed if Cohen's $d > 0.2$ AND one-sided $p < 0.05$. Refuted otherwise.
- **H3:** confirmed if rmANOVA representation × stressor interaction $F$-test $p < 0.05$ AND post-hoc S-TTSA degradation < R8 degradation for both S1 and S2. Refuted otherwise.

Multiple-comparisons correction via Holm-Bonferroni applied across H1, H2, H3 family ($m = 3$): adjusted $\alpha$ = 0.0167, 0.025, 0.05 in order of ascending $p$-value. H4 is tested independently with its own one-sided test per §9.8; no additional cross-hypothesis correction is applied because H4 was added by Amendment 1 with its own pre-registered $\alpha$.

### Executable analysis script

The deterministic implementation of H1–H4, the §9.6 joint H2/H4 interpretation grid, and the §3 H1 halt-condition is locked in [[(C)-A1-Factorial-Analysis-Script]]. The script's SHA-256 hash is recorded in the OSF manifest at registration time as `a1_analysis_script_sha256`; any post-registration modification requires an OSF registration update. Reviewers can verify reproducibility by checking: registered DOI → tagged commit → script hash → bit-exact deterministic run on the per-subject accuracy CSVs → identical `a1_results.json`.

### Synthetic smoke-test verification of the analysis pipeline

Before any real-data results are computed, the analysis script is verified by running it against five synthetic scenarios produced by the locked generator [[(C)-A1-Synthetic-Smoke-Test-Generator]]. The five scenarios are: `all_pass` (all hypotheses pass), `h1_fail`, `h2_fail`, `h3_fail`, `h4_fail` (each hypothesis flipped to fail in turn). The expected discrimination matrix is published in §9.8 below and as the table in the generator document. **The five smoke-test `results.json` files are committed to the repository at the `pre-registration-locked` git tag, with SHA-256 hashes recorded in the OSF manifest.** Any reviewer can re-run the generator and analysis script and confirm bit-exact agreement, proving the analysis pipeline correctly discriminates known effects before being applied to real data.

### Data exclusion

**Pre-specified exclusions:**
- Subjects 88, 89, 92, 100, 104, 106 (Varbu et al. 2024 anomalies)
- Epochs with peak-to-peak voltage > 150 μV in any channel (artefact rejection per §8.1 of [[../07-Implementation/02-Real-Time-Pipeline]])
- Subjects with fewer than 30 valid epochs of either class after artefact rejection (no a priori expectation of how many subjects this excludes; report exact count in results)

**No post-hoc exclusions.** Outliers in the accuracy distribution are reported but retained in primary analysis.

### Missing data

PhysioNet EEGMMIDB has no missing data per se. If `mne.datasets.eegbci.load_data()` fails to download a subject (network error), retry up to 3 times; if persistent failure, exclude that subject and report the exclusion in results. No imputation is performed.

For TTSA convergence failures (energy diverges, NaN appears in restriction maps), the affected subject's S-TTSA condition is marked as NaN and excluded from the H1 contrast for that subject only. Robustness check: re-run H1 with these subjects' S-rand condition also excluded (paired exclusion). Report both numbers; if they differ by > 5 pp, flag as a data integrity concern.

### Exploratory analysis

Beyond H1–H3, the following analyses are explicitly **exploratory** (not preregistered, no multiple-comparisons correction reported as confirmatory):

- E1: R32 vs R8 paired comparison
- E2: representation × topology (physical / functional / SCGL / FC / permuted-null) factorial — secondary 5 × 5 design within S0
- E3: S3 (LOSO) vs S0 (within-subject) for S-TTSA only — informs Lee 2019 transfer pre-screening
- E4: subject-level $C(t)$ AUC distribution
- TTSA convergence diagnostics
- Spectral gap $\lambda_1$ distribution
- ITR decision-time tradeoff curves

Results from exploratory analyses are reported in a separate "Exploratory Findings" section of the final write-up, clearly labelled as such.

---

## §8 — Other (Optional)

### Software environment

- Python 3.11
- `mne` ≥ 1.6, `moabb` ≥ 1.1, `pyriemann` ≥ 0.5
- `geoopt` ≥ 0.5 (Stiefel manifold optimisation)
- `iisignature` ≥ 0.24 (signature kernel computation)
- `clifford` ≥ 1.4 (rotor parameterisation, ablation only)
- `scikit-learn` ≥ 1.3, `scipy` ≥ 1.11, `numpy` ≥ 1.24
- `pingouin` ≥ 0.5 (statistics)

Environment pinned in `environment.yml` committed to GitHub at registration time. Hash of the environment file logged in run manifest.

### Hardware

Standard laptop CPU (Intel Core i7-class or AMD Ryzen 7-class, 16 GB RAM). No GPU required. Estimated wall-clock time for full Phase A-1 factorial: 30–50 hours single-threaded, 8–15 hours with 4-way parallelism via `joblib`.

### Reproducibility commitment

- All code on GitHub at [URL TBD], MIT licence, with the exact commit hash referenced in OSF registration as `git_commit_at_registration`.
- All seeds logged in run manifest.
- All raw results (per-subject, per-condition CSVs) released as supplementary files at experiment completion.
- Analysis script `analyse_a1_factorial` cannot be modified after registration without an OSF registration update; the script's hash is logged.

### Conflicts of interest

PI declares no financial conflicts of interest. The thrIVE architecture is the PI's foundational research project for a future commercial venture; this preregistration is designed precisely to falsify the architecture's load-bearing claims if they are wrong, with explicit halt criteria and pre-registered null hypotheses. The PI commits to publishing the result regardless of outcome.

### Acknowledgements

This preregistration was drafted in collaboration with an AI assistant (Claude, Anthropic). The PI is the sole human signatory and assumes full responsibility for the registered analysis plan.

---

## §9 — Pre-Submission Amendment 1: EEG Foundation Model Baseline

> **Status:** Drafted May 2026. To be incorporated into the initial OSF submission **before** the registration DOI is issued. If the original preregistration has already been registered, this section must be submitted as an OSF "Registration Update" with full reviewer notification; in that case, all hypotheses below are non-confirmatory (exploratory) until the update DOI issues.

### §9.1 Motivation for the amendment

Between v5.4 of the thrIVE specification (April 2026) and v5.5 (May 2026), EEG foundation models matured from speculation to validated state-of-the-art front-end technology. Specifically:

- **ST-EEGFormer** (KU Leuven, 2025–2026) won the NeurIPS 2025 EEG Challenge using a spatiotemporal masked-autoencoder pretraining on 8 million EEG segments. (https://www.vscentrum.be/post/scaling-eeg-foundation-models-on-vsc-an-iclr-2026-benchmark-and-a-neurips-2025-eeg-challenge-win)
- **Large Cognition Model (LCM)** (Wang et al., 2025, *arXiv:2502.17464*) demonstrates cross-subject and cross-task generalisation on multiple BCI benchmarks including motor imagery.
- **BrainPro** (2025, *arXiv:2509.22050*) was pre-trained on ~60,000 hours of EEG across 25,000 subjects — the largest EEG pre-training effort to date.

The original §4 design uses the Riemannian tangent at $d = 8$ (R8) as the baseline against which the sheaf layer must demonstrate added value. R8 is a 2023-era baseline; it does not reflect the actual state of the field as of Phase A execution. Running Phase A-1 unchanged would produce a misleading result: even if the sheaf layer beats R8, it might lose to a foundation model alone, making the architectural claim weak.

This amendment adds **R_FM** (foundation-model features at $d = 8$) and **R_FM+S** (foundation model + S-TTSA sheaf coherence) as factor levels, so that the Phase A-1 outcome answers the right question — *does the sheaf-on-SPD-manifold architecture add value over the actual best available pretrained representation?* — rather than a strawman version of it.

The amendment is **conservative**: it adds two factor levels to the existing 5 × 4 = 20-condition design (becoming 7 × 4 = 28 conditions per subject), affects no existing hypothesis (H1, H2, H3 remain pre-registered as in §3), and introduces one new confirmatory hypothesis (H4) with explicit gate criterion.

### §9.2 New factor level definitions

| Level | Definition |
|---|---|
| **R_FM** | Frozen features from a publicly released EEG foundation model, projected to $d = 8$ |
| **R_FM+S** | Concatenated R_FM features + S-TTSA sheaf coherence, logistic regression |

### §9.3 Foundation model specification (locked at registration)

The amendment locks the exact model, checkpoint, and feature-extraction procedure to prevent silent post-hoc selection.

**Primary model:** Large Cognition Model (LCM), Wang et al. (2025), *arXiv:2502.17464*. Public checkpoint released at the URL provided in the paper's GitHub repository (URL recorded in OSF submission as a static link). MD5 hash of the checkpoint file recorded in the run manifest at first download.

**Fallback model:** If the LCM public checkpoint is unavailable at Phase A execution time (e.g., URL has lapsed), the fallback is the **EEGFormer** checkpoint (Jiang et al., 2024, *arXiv:2401.10278*) — earlier transformer-based foundation model with documented motor-imagery transfer. The fallback is locked at registration to prevent post-hoc model selection.

**Rejection criterion (no further substitution):** If neither LCM nor EEGFormer checkpoints are available, R_FM and R_FM+S levels are dropped from the analysis (reported as "could not be tested") and the original 5 × 4 design proceeds as registered. H4 is not tested. No third model is substituted post-hoc.

### §9.4 Feature extraction procedure

1. Each PhysioNet EEGMMIDB epoch (4-second motor-imagery trial) is preprocessed via the §4 pipeline through the bandpass filter + notch filter + artefact rejection + common average referencing stages (identical to the R32/R8/S branches).
2. The 64-channel preprocessed epoch is passed through the frozen foundation model. No fine-tuning. No per-subject adaptation. Model weights are read-only throughout.
3. The foundation model's last-hidden-layer output is extracted: a tensor of shape (time_steps, hidden_dim). For LCM this is approximately (1000, 256); for the EEGFormer fallback approximately (250, 192).
4. Mean-pool over the time axis to produce a hidden_dim-dimensional vector per epoch.
5. PCA-project to $d = 8$ using the within-subject training-fold projection matrix. The PCA projection is computed per-subject on training-fold epochs only and applied to test-fold epochs — never the reverse. This matches the per-fold isolation discipline of the R8 channel selection in §4.1.
6. R_FM is the resulting 8-dimensional vector per epoch.

**Executable implementation:** the deterministic procedure above is realised in the locked script [[(C)-R_FM-Feature-Extraction]]. The script's SHA-256 hash is logged in the OSF manifest alongside the LCM and EEGFormer checkpoint MD5 hashes at registration. Any post-registration modification to the script requires an OSF registration update.

### §9.5 New hypothesis H4 — Sheaf adds value over the actual SOTA baseline

**Hypothesis (Claim C2 strengthened):** Sheaf coherence adds value over the EEG foundation model baseline. Classification using concatenated R_FM features and S-TTSA coherence outperforms classification using R_FM features alone, on clean data (S0).

- **Directional prediction:** mean accuracy of (R_FM+S) > mean accuracy of R_FM at S0
- **Strength criterion:** paired Cohen's $d > 0.2$ (small effect threshold), one-sided $\alpha = 0.05$
- **Halt condition:** if H4 fails *and* H2 passes (i.e., sheaf beats R8 but not R_FM), the architectural conclusion is: the sheaf layer is valuable only when starting from a weak baseline. Stage 1 hardware should adopt the foundation model where compute allows; sheaf layer is justified only by its Stage 2/3 federated-atlas role (per §7.7a.4 of [[../07-Implementation/01-Calibration-Deployment]]).
- **Failure with H2 pass interpretation:** Phase A-2 (IVE evidence integration) still runs, but the architecture's "novel contribution" claim is narrower than v5.5 supposes.

### §9.6 H4 alongside H2 — joint interpretation matrix

The amendment introduces a joint-interpretation grid for H2 and H4 outcomes:

| | H4 passes (sheaf > R_FM) | H4 fails (sheaf ≤ R_FM) |
|---|---|---|
| **H2 passes (sheaf > R8)** | Strongest result: sheaf adds value over both old and new baselines. Proceed with full v5.5 architecture. | Sheaf beats weak baseline only. Architecture viable but value-claim narrower; consider foundation-model front-end with sheaf as IVE Evidence 1 only. |
| **H2 fails (sheaf ≤ R8)** | Inconsistent — investigate; flag as unresolved before Phase A-2. | Sheaf has no measurable value at d = 8. Halt Phase A as per H2 original halt condition. |

### §9.7 Compute and timeline impact

| Aspect | Original (5 × 4) | Amended (7 × 4) |
|---|---|---|
| Conditions per subject | 20 | 28 |
| Total paired observations (109 subjects) | 2,180 | 3,052 |
| Per-subject wall-clock (single-threaded) | ~25 min | ~35 min |
| Foundation model inference | n/a | ~6 min per subject (LCM, CPU) |
| Total wall-clock (4-way `joblib`) | 8–15 h | 12–22 h |
| Hoeffding detectable $\varepsilon_{\min}$ at $N = 103$ paired | 0.024 | 0.024 (unchanged) |
| G*Power detectable Cohen's $d$ | 0.12 | 0.12 (unchanged) |

The detectability bounds are unchanged because they depend on subject count (109 → 103 retained), not on factor level count. The amendment is power-neutral.

### §9.8 Statistical analysis amendments

Add to §7 (Analysis Plan):

- H4 test: paired BEST (Kruschke, 2013) on per-subject accuracies (R_FM+S) − (R_FM), one-sided alternative, $\alpha = 0.05$, Bayes factor reported via `pingouin.ttest`.
- The H2-vs-H4 joint interpretation grid (§9.6) is reported as a 2×2 outcome table.
- No multiple-comparison correction beyond the existing Holm-Bonferroni on the pairwise contrasts in H3; H1, H2, H3, H4 are pre-registered as independent confirmatory hypotheses with explicit gate criteria.
- The R_FM ablation arm (R_FM at all four stressors) generates a parallel C4-equivalent graceful-degradation comparison for the foundation model. Result reported but not pre-registered as a confirmatory hypothesis.

**Expected smoke-test discrimination matrix** (verified before registration via [[(C)-A1-Synthetic-Smoke-Test-Generator]]):

| Synthetic scenario | H1 | H2 | H3 | H4 | Joint H2/H4 verdict |
|---|---|---|---|---|---|
| `all_pass` | PASS | PASS | PASS | PASS | STRONGEST |
| `h1_fail`  | FAIL | (halt: not tested) | (halt: not tested) | (halt: not tested) | (halt: not tested) |
| `h2_fail`  | PASS | FAIL | PASS | PASS | INCONSISTENT |
| `h3_fail`  | PASS | PASS | FAIL | PASS | STRONGEST |
| `h4_fail`  | PASS | PASS | PASS | FAIL | NARROWER |

If [[(C)-A1-Factorial-Analysis-Script]] does not produce these verdicts on the five smoke-test scenario inputs, the analysis script has a bug that must be fixed before OSF registration.

### §9.9 Pre-registration integrity statement

The PI declares that, at the time of this amendment:

- No EEG data has been downloaded.
- No analysis code has been run on PhysioNet EEGMMIDB.
- No foundation model has been applied to PhysioNet EEGMMIDB.
- The LCM and EEGFormer checkpoint MD5 hashes have not been logged against any analysis output.
- The R_FM PCA projection has not been computed for any subject.

Further, the PI commits:

- Not to modify [[(C)-R_FM-Feature-Extraction]], [[(C)-R_JEPA-Feature-Extraction]], [[(C)-A1-Factorial-Analysis-Script]], [[(C)-A1-Synthetic-Smoke-Test-Generator]], or [[(C)-CI-Workflow-Preregistration-Verify]] after the OSF registration DOI issues, except via a recorded OSF registration update.
- Not to disable, bypass, or override the CI workflow defined in `.github/workflows/preregistration-verify.yml`. If the workflow fails on a commit, that commit will not be used to produce registered results.
- To preserve the GitHub branch protection rules that require CI to pass before any merge to `main`.
- For the R_JEPA arm specifically (Amendment 2): not to tune SIGReg M, β, λ_sig, learning rate, weight decay, training-epoch count, or batch size post-registration; not to substitute the SIGReg regulariser with alternatives (VICReg, Barlow Twins, etc.); not to disable the SIGReg term to test a "collapse-allowed" baseline. The hard architectural test of sheaf-vs-end-to-end-JEPA must be conducted under the locked R_JEPA configuration.
- For the Phase A-7 ACP twin (Amendment 3): not to tune TTSA timescales / learning rates, SPRT α / β, sensory-anchored inhibition constants (σ_DN, n, β_sensory, γ_h), hyperdirect latency cap, modelled noise parameters (σ, τ_OU), or critical-period reopen threshold post-registration. The dynamical-architecture comparison must be conducted under the locked simulator configuration. Any post-registration modification to the simulator requires an OSF registration update.
- For the Phase A-7′ Mainstream-Ensemble Baseline (Amendment 3 sibling): not to substitute alternative published methods for any of the five composed components (SPRT-Liu, TSFNet attention, T-TIME, memory-buffer continual, ST-EEGFormer/LCM features). Not to tune attention hyperparameters, SPRT thresholds, T-TIME learning rate or step count, or memory-buffer size post-registration. The architecturally honest comparison must use the locked composition under the locked parameters. If a component reference paper is later withdrawn or corrected, the substitution must be recorded as an OSF registration update with explicit rationale.
- For the R_JEPA_brain arm (Amendment 4): not to modify the script's locked hyperparameters (channel groups, mask probability, transformer dimensions, SIGReg weights matched to R_JEPA, learning rate, training-epoch count, batch size) post-registration. Not to substitute alternative JEPA architectures from the Brain/Signal-JEPA family. Not to apply post-hoc selection between R_JEPA and R_JEPA_brain outcomes — both must be reported regardless of which favours the sheaf. PI commits to verifying the Brain-JEPA / Signal-JEPA architectural principles in the published papers before final OSF lock.
- For the R_GL arm (Amendment 5): not to modify the locked graph topology generator, top-K eigenmodes, channels-per-neural-node, or PCA target dimension post-registration. The R_GL script must produce identical graph topology to the Phase A-7 ACP twin for the same master seed — verified by checksum of the edge list at the lock-in stage. Any divergence is a registration integrity violation requiring an OSF registration update. R_GL outcomes must be reported even if they favour the simpler graph-Laplacian alternative over the sheaf.

This amendment is therefore a *pre-data* amendment, not a *post-hoc* analysis decision. It carries the same scientific weight as the original preregistration.

### §9.10 Cross-references

| Section | Connection |
|---|---|
| §3, §4 of this preregistration | Original H1–H3 hypotheses; original 5 × 4 design |
| [[(C)-Phase-A-Experiment-Revised]] §4.1 | Pre-registration amendment block noting candidate R_FM level |
| [[../07-Implementation/01-Calibration-Deployment]] §7.7a | Three integration paths for EEG foundation models; Option C is what this amendment implements |
| [[../10-Analysis/02-Open-Questions]] OQ 11.81 | Foundation model baseline open question (this amendment resolves the "should we?" question with "yes, as a Phase A-1 factor level") |
| [[../🎯-thrIVE-Hub-v5.5]] Key Validated Results | EEG foundation models entry |

---

## §10 — Pre-Submission Amendment 2: LeWorldModel End-to-End JEPA Baseline (Hard Architectural Test)

> **Status:** Drafted May 2026. Must be incorporated into the initial OSF submission **before** the registration DOI is issued. This is a **hard architectural test** — it can fail, and the spec has pre-committed to acknowledging the consequences.

### §10.1 Motivation for Amendment 2

Between v5.5 of the thrIVE specification (April 2026) and the OSF submission (May 2026), the LeWorldModel paper appeared:

- **LeWorldModel (LeWM)** (Maes et al., 2026, [arXiv:2603.19312](https://arxiv.org/abs/2603.19312); LeCun + Mila + AMI Labs). First end-to-end JEPA-from-pixels that trains stably with only two loss terms (next-embedding prediction + Sketched Isotropic Gaussian Regularization) and one hyperparameter. ~15M parameters, single-GPU, hours of training. Explicitly addresses JEPA collapse.

LeWM raises a hard architectural question for thrIVE: **does thrIVE's structured architecture (sheaf + canonical microcircuit + multi-timescale TTSA + ...) empirically outperform a minimal-prior end-to-end JEPA on the same task?** If not, the structured architecture does not earn its complexity for the Phase A-1 motor-imagery classification task, and §2.1–§2.13 commitments require re-evaluation.

The original H2 ("sheaf adds value over R8 baseline") and the Amendment 1 H4 ("sheaf adds value over R_FM foundation-model baseline") both test the sheaf against *external* baselines that pre-date or are independent of LeWM. Neither test addresses the harder question of whether **structured priors of any kind earn their keep** against minimal-prior end-to-end alternatives. Amendment 2 closes this gap.

### §10.2 New factor levels

| Level | Definition |
|---|---|
| **R_JEPA** | LeWM-style end-to-end encoder + predictor with SIGReg regularisation, trained jointly on the same training-fold data, output projected to $d = 8$ via per-fold PCA |
| **R_JEPA+S** | Concatenated R_JEPA features + S-TTSA sheaf coherence, logistic regression |

Adds 2 × 4 = 8 conditions per subject, raising the total from 3,052 (with Amendment 1) to ~3,920 paired observations. Hoeffding detectability bound (§14) unaffected — only the level count changes.

### §10.3 Locked R_JEPA specification

The R_JEPA architecture is locked in [[(C)-R_JEPA-Feature-Extraction]] with the following non-negotiable hyperparameters:

| Parameter | Locked value | Rationale |
|---|---|---|
| Encoder architecture | 4-block 1D convolutional, hidden_dim = 256 | Mirrors LeWM's small-conv encoder |
| Predictor architecture | 2-layer MLP, hidden width = 512 | Matches LeWM's lightweight predictor |
| SIGReg projections (M) | 1024 | LeWM default; sub-linear cost |
| SIGReg β | 1.0 | Henze-Zirkler weighting |
| SIGReg weight (λ_sig) | **1.0** — the single hyperparameter | LeWM achieves stability with this value |
| Learning rate | 1e-3 | AdamW default |
| Weight decay | 1e-4 | AdamW default |
| Training epochs | 50 | Convergence empirically achieved within this budget |
| Batch size | 32 | Standard |
| Master seed | 42 | Determinism |

No post-registration tuning of any of these parameters is permitted. No substitution of SIGReg with alternative regularisers (VICReg, Barlow Twins, etc.). No ablation of SIGReg to test "collapse-allowed" baseline. The hard architectural test must be conducted under the locked configuration.

### §10.4 New hypothesis H5 — Sheaf adds value over minimal-prior end-to-end JEPA

**Hypothesis (the hard architectural test):** Sheaf coherence adds value over a minimal-prior end-to-end JEPA baseline. Classification using concatenated R8 tangent features and S-TTSA coherence outperforms classification using R_JEPA features alone, on clean data (S0).

- **Directional prediction:** mean accuracy of (R8 + S) > mean accuracy of R_JEPA at S0
- **Strength criterion:** paired Cohen's $d > 0.2$ (small effect threshold), one-sided $\alpha = 0.05$
- **Halt condition:** if H5 fails (R_JEPA ≥ R8 + S), the architectural conclusion is: **thrIVE's structured priors (sheaf, canonical microcircuit, multi-timescale TTSA) do not earn their complexity for the Phase A-1 motor-imagery task.** §2.1–§2.13 commitments require re-evaluation; Stage 1 deployment should consider whether minimal-prior end-to-end architectures should become the default. The architecture's complexity for Stage 2.5 / 3 may still be justified by domain-specific factors (multi-modal integration, cross-subject transfer, safety verification, Ethics Core auditability) — but the *primary* empirical claim that the sheaf earns its keep would be falsified for the simplest BCI task.
- **Failure-with-H2-pass interpretation:** if H2 passes (R8+S > R8) but H5 fails (R_JEPA ≥ R8+S), the sheaf adds value *only* against a weak baseline. This is a substantially narrower claim than the spec currently makes. Phase A-2 still runs, but architectural communications about thrIVE must be revised to acknowledge this narrower scope.

### §10.5 Joint H2 / H4 / H5 interpretation matrix

The §9.6 grid extends to a 2 × 2 × 2 cube:

| H2 | H4 | H5 | Verdict | Action |
|---|---|---|---|---|
| ✓ | ✓ | ✓ | **STRONGEST**: sheaf beats R8, R_FM, and R_JEPA | Proceed with full v5.5 architecture; sheaf earns keep against all baselines |
| ✓ | ✓ | ✗ | **MIXED**: sheaf beats foundation model but not end-to-end JEPA | Investigate R_JEPA architecture for ablation; possibly the SIGReg+conv combination captures something the sheaf does not |
| ✓ | ✗ | ✓ | **NARROW (foundation-model-blocked)**: sheaf beats R8 and R_JEPA but loses to R_FM | Stage 1 viable with sheaf; Stage 2/3 should consider foundation-model front-end |
| ✓ | ✗ | ✗ | **NARROW (weak-baseline-only)**: sheaf only beats R8 | Architecture claim substantially narrowed; consider whether Stage 1 should adopt R_JEPA or R_FM as front-end and use sheaf only for IVE Evidence |
| ✗ | * | * | **HALT** per H2 halt condition: sheaf has no measurable value at d=8 against any baseline (H2 fails by definition before testing H5) |

### §10.6 Statistical analysis amendments

Add to §7 (Analysis Plan):

- **H5 test:** paired BEST on per-subject accuracies (R8+S) − R_JEPA, one-sided alternative, $\alpha = 0.05$. Bayes factor reported via `pingouin.ttest`.
- The 2 × 2 × 2 joint-interpretation cube (§10.5) is reported as a structured outcome table.
- No additional cross-hypothesis correction beyond Holm-Bonferroni on the H3 pairwise contrasts. H1, H2, H3, H4, H5 are pre-registered as independent confirmatory hypotheses with explicit gate criteria.
- R_JEPA ablation arm (R_JEPA at all four stressors) generates a parallel C4-equivalent graceful-degradation comparison for end-to-end JEPA. Result reported; not pre-registered as confirmatory.

### §10.7 Pre-registration integrity statement extension

Already incorporated into §9.9: the PI commits not to tune R_JEPA hyperparameters post-registration, not to substitute SIGReg with alternative regularisers, not to disable SIGReg to test a "collapse-allowed" baseline. The hard architectural test must be conducted under the locked configuration.

### §10.8 Cross-references

| Section | Connection |
|---|---|
| §3, §4, §9, §10 of this preregistration | H1–H5 hypotheses; original + amended factorial design |
| [[(C)-Phase-A-Experiment-Revised]] §4.1 second amendment | Phase A-1 design factor extension with R_JEPA and R_JEPA+S |
| [[(C)-R_JEPA-Feature-Extraction]] | Locked executable implementation |
| [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]] §2.14.2.0 | LeWorldModel as primary reference for Stage 2.5 world-model component |
| [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]] §2.14.2.3 | JEPA collapse prevention as first-class concern |
| [[../02-Theory/(C)-14-Representational-Substrate-Engrams-Cognitive-Maps-Slots]] §2.15.2.5 | Architectural sibling: SIGReg-style regularisation for engram bank |
| [[../06-Prediction/01-Prediction-Engine-Architecture]] §15.5 | JEPA collapse caveat for current Mamba SSM |
| [[../10-Analysis/02-Open-Questions]] OQ 11.107, 11.108, 11.109 | Open questions addressed by Amendment 2 |

---

## §11 — Pre-Submission Amendment 3: Dynamical-Architecture Comparison and Stage 3 Component Validation

> **Status:** Drafted May 2026. Bundles three closely-related extensions to the Phase A test programme into a single submittable amendment: (a) Phase A-7 dynamical comparison vs LeWM (sub-§11.2), (b) Phase A-7′ comparison vs the BCI mainstream ensemble (sub-§11.3), (c) optional Phase B-2 partial validation of §2.16 active-learning components (sub-§11.4). The amendments are coupled because they share the locked Digital ACP Twin simulator and the locked mainstream-ensemble baseline. Must be incorporated into the OSF submission before any A-7 / A-7′ / B-2 data is touched.

### §11.1 Motivation for Amendment 3

Amendments 1 (R_FM foundation-model baseline) and 2 (R_JEPA end-to-end JEPA baseline) extended the Phase A-1 representation-arm comparison. They test **whether the sheaf structure is a useful static feature** against two external baselines. They do **not** test:

1. **The dynamical architecture** (multi-timescale TTSA, SPRT IVE, hyperdirect pathway, sensory-anchored inhibition, THINK mode, V/S/K cross-modal integration). Phase A-1 is offline batch classification; these mechanisms are deployment-regime properties that batch testing cannot evaluate.

2. **The architecturally honest comparison against the BCI mainstream**. R_JEPA (Amendment 2) tests against LeWorldModel — a research model from a different domain (vision). The actual deployable alternative is the ensemble of published BCI methods (SPRT-Liu + TSFNet + T-TIME + ST-EEGFormer features + memory-buffer continual learning).

3. **The Stage 3 active-learning components** specified in §2.16 of the theory ([[../02-Theory/(C)-15-Stage-3-Self-Sufficient-Learning-Loops]]). Three of these — intrinsic curiosity reward, Piagetian equilibration trigger, autopoietic-coherence monitor — can begin partial validation in simulation against existing Phase A-1 data, without any new data collection or IRB requirement.

Amendment 3 closes these gaps with three coupled sub-amendments.

### §11.2 Phase A-7 — Dynamical-Architecture Comparison vs LeWorldModel

**Hypothesis (H6, Claim C9):** thrIVE's dynamical architecture (multi-timescale TTSA + SPRT IVE + sensory-anchored inhibition + hyperdirect pathway + critical-period plasticity) confers measurable streaming-mode advantages over LeWM-style end-to-end JEPA running on the same streaming EEG + V/S/K data.

**Six endpoints (slimmed after May 2026 literature audit; see §7.7a.4 of [[(C)-Phase-A-Experiment-Revised]]):**

| Endpoint | Tests | Gate |
|---|---|---|
| **E1′** — Multi-evidence SPRT vs single-evidence SPRT latency | Evidence-channel-multiplicity advantage | $d > 0.3$, $p < 0.05$ |
| **E2** — Mid-trajectory stressor recovery | Composite of sensory-anchored inhibition + Lipschitz restriction maps | thrIVE recovers faster than R_JEPA |
| **E3′** — Multi-timescale TTSA + critical-period vs T-TIME | Additional contribution beyond T-TIME baseline | thrIVE wins or matches at lower per-cycle cost |
| **E4** — V/S/K cross-modal evidence convergence in IVE | IVE evidence-stack mechanism specifically | Cross-modal contribution measurable |
| **E6** — Hyperdirect-pathway safety-stop latency | thrIVE-specific architecture | $\leq 2$ cycles (8 ms) |
| **E7′** — Sheaf-coherence-based fusion vs attention-based fusion baselines | Sheaf-fusion mechanism specifically | thrIVE wins or matches |

**Locked R_JEPA configuration** (per Amendment 2 / [[(C)-R_JEPA-Feature-Extraction]]) is reused.

**Locked Digital ACP Twin** ([[(C)-Phase-A7-Digital-ACP-Twin]]) implements the thrIVE side; SHA-256 logged as `phase_a7_script_sha256`.

**Factorial design:** 2 (architecture) × 4 (stressor) × 5 (mode) × 103 subjects × 5 folds = 20,600 paired observations.

### §11.3 Phase A-7′ — Architecturally Honest Comparison vs BCI Mainstream Ensemble

**Hypothesis (H7, Claim C9′):** thrIVE's dynamical architecture beats the **ensemble of mainstream BCI methods that thrIVE would actually replace if deployed** — not just a research model from a different domain.

**Mainstream-ensemble composition** (locked in [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]]):

- ST-EEGFormer / LCM foundation-model features (Wang et al., 2025; KU Leuven 2025) — reuses Amendment 1 R_FM extraction outputs
- TSFNet-style multi-head attention fusion (Li et al., 2025) — 4 heads, hidden 64
- SPRT-Liu single-channel sequential decision (Liu et al., 2017) — α=1e-3, β=0.1 matched to ACP twin
- Wu T-TIME entropy-minimisation adaptation (Wu et al., 2024) — lr=1e-4, 5 steps/session
- Memory-buffer continual learning (Pena Pereira et al., 2024) — 200 epochs, class-balanced

**Endpoints:** same E1′ / E2 / E3′ / E4 as Phase A-7, but with the mainstream ensemble as the comparator. E6 (hyperdirect) and E7′ (sheaf-fusion-ratio) are **reported as N/A by design** — the mainstream has no equivalents. **thrIVE wins these by default; the test is whether it also competes on the four endpoints where the mainstream has established methods.**

**Gate criterion:** thrIVE-composite ≥ mainstream-ensemble at matched detectability, with at least one endpoint $d > 0.3$ advantage. If failure: the architectural complexity is unjustified relative to deployable alternatives; the spec must acknowledge this directly.

**Locked mainstream ensemble** ([[(C)-Phase-A7-Mainstream-Ensemble-Baseline]]); SHA-256 logged as `phase_a7_ensemble_script_sha256`.

**Factorial design:** 2 × 4 × 4 = 32 conditions × 103 subjects × 5 folds = 16,480 paired observations (identical input streams to A-7 for direct paired comparison).

### §11.4 Phase B-2 — Optional Partial Validation of §2.16 Stage 3 Components

**Status:** optional pre-registration; can be deferred to a separate amendment if Phase A-7 / A-7′ are deemed sufficient for the initial OSF DOI.

**Hypothesis (H8, optional):** three of the five §2.16 active-learning components (§2.16.3 curiosity reward, §2.16.5 equilibration trigger, §2.16.6 autopoietic-coherence monitor) work as designed on the existing Phase A-1 streaming trajectories — i.e., the mechanisms can be ruled in or out at simulation level before committing to the larger Phase B-3 closed-loop synthetic-environment work.

**Three sub-endpoints (per §2.16.8a.2 of theory):**

- **E_curiosity** — $r_{\mathrm{int}}(t)$ correlates with subsequent prediction-error reduction within next 100 cycles, correlation > 0.3
- **E_equilibration** — Under drift stressor, equilibration trigger fires ≥ 50 cycles before IVE accuracy drops below 80 % of baseline
- **E_autopoietic** — Coherence monitor detects ≥ 90 % of injected structural breaches at < 5 % false-alarm rate

**Locked configuration:** the Phase A-7 ACP twin is extended with the three components per §2.16.3 / §2.16.5 / §2.16.6 specifications. Hyperparameters locked at spec defaults: $(\alpha_{\mathrm{nov}}, \alpha_{\mathrm{lp}}, \alpha_{\mathrm{symm}}) = (0.2, 0.6, 0.2)$ for the curiosity reward; $\theta_{\mathrm{eq}} = 0.3$ for the equilibration trigger; standard isotropy / Lipschitz / SPRT bounds for the autopoietic monitor.

**Resources:** ~1 week of additional simulation runs on the locked Phase A-7 infrastructure. No new data, no IRB.

**Why this is "optional" pre-registration:** sub-§11.4 tests Stage 3 components that are not architecturally required for Stage 1 / 2 deployment. Failure to validate them in Phase B-2 does not affect the Phase A-1 / A-7 / A-7′ outcomes; it only affects the Stage 3 roadmap. The amendment is included here because it can be run cheaply alongside the Phase A-7 simulator, but it can equally be deferred to a later registration.

**Executable implementation:** the locked Phase B-2 extension is at [[(C)-Phase-B2-Stage3-Component-Validation]]. SHA-256 logged as `phase_b2_extension_sha256`. Implements the three §2.16 components (curiosity reward, equilibration tracker, autopoietic monitor) as instrumentation on the existing Phase A-7 ACP twin — no modification to twin dynamics. Three endpoints produced per run: E_curiosity (correlation > 0.3), E_equilibration (lead ≥ 50 cycles before IVE accuracy drop), E_autopoietic (detection ≥ 90 % at FA ≤ 5 %). All hyperparameters and breach-injection rates locked at registration values; smoke test runs end-to-end on synthetic EEG before any PhysioNet data is touched.

### §11.5 Locked specifications inventory

| Script | SHA-256 manifest field | Locked parameters |
|---|---|---|
| [[(C)-R_JEPA-Feature-Extraction]] (Amendment 2) | `r_jepa_script_sha256` | SIGReg M=1024, β=1, λ_sig=1, lr=1e-3, 50 train epochs, batch 32, seed 42 |
| [[(C)-Phase-A7-Digital-ACP-Twin]] (Amendment 3, sub-§11.2) | `phase_a7_script_sha256` | TTSA timescales (50ms/30s/5min/30min/1h), SPRT α=1e-3 / β=0.1, sensory-anchored inhibition constants (σ_DN=0.1, n=2, β_sens=0.3, γ_h=0.5), hyperdirect cap=2 cycles, noise σ=0.05 + τ_OU=100ms, critical-period reopen threshold=0.3 BW, seed 42 |
| [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]] (Amendment 3, sub-§11.3) | `phase_a7_ensemble_script_sha256` | Attention 4-head, hidden 64; SPRT α=1e-3 / β=0.1; T-TIME lr=1e-4, 5 steps; memory buffer 200, class-balanced; seed 42 |
| Phase B-2 §2.16 extension (Amendment 3, sub-§11.4, optional) | `phase_b2_extension_sha256` | $(\alpha_{\mathrm{nov}}, \alpha_{\mathrm{lp}}, \alpha_{\mathrm{symm}}) = (0.2, 0.6, 0.2)$; $\theta_{\mathrm{eq}}=0.3$; structural-breach injection rates locked at registration |

### §11.6 Joint H2 / H4 / H5 / H6 / H7 verdict matrix

The original Amendment 1 grid (H2 / H4) and Amendment 2 grid (H2 / H4 / H5) extend to a five-hypothesis grid:

| H2 (sheaf vs R8) | H4 (sheaf vs R_FM) | H5 (sheaf vs R_JEPA static) | H6 (thrIVE-dynamic vs LeWM streaming) | H7 (thrIVE-composite vs mainstream ensemble) | Architectural verdict |
|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | ✓ | **STRONGEST**: full justification across all baselines and both regimes |
| ✓ | ✓ | ✓ | ✓ | ✗ | Beats research models but not the deployable mainstream — complexity unjustified |
| ✓ | * | ✗ | ✓ | ✓ | **Architecture is a control system, not a representation system**: dynamical claims survive, representational claims at parity with end-to-end JEPA |
| ✓ | ✓ | * | ✗ | ✗ | Representation good but dynamics no better — revise §2.13–§2.14 |
| ✗ | * | * | ✓ | ✓ | Sheaf representation no advantage; architecture justified solely by control-system properties — narrowed architectural identity |
| ✗ | * | * | ✗ | ✗ | **FUNDAMENTAL HALT** — no measurable architectural advantage |

Six representative outcomes shown; the full $2^5 = 32$-cell matrix is available in the analysis script's interpretation logic.

### §11.7 Statistical analysis amendments

Add to §7 (Analysis Plan):

- **H6 test:** per-endpoint comparison (thrIVE-dynamic vs R_JEPA-streaming) via paired BEST on per-subject per-condition aggregates. One-sided $\alpha = 0.05$.
- **H7 test:** same as H6 but against the locked mainstream-ensemble baseline. Same statistical procedure.
- **Joint H6 / H7 reporting:** the dynamical claim is established only when **both** H6 (against research baseline) and H7 (against deployable baseline) at least partially pass. If H6 ✓ but H7 ✗, thrIVE beats LeWM but not the mainstream — reported as architecturally narrower claim than initial scope.
- **H8 (optional):** three sub-endpoints (E_curiosity, E_equilibration, E_autopoietic) reported as triple of pass/fail; no aggregate. Each is independent; partial passes are valid outcomes.

### §11.8 Pre-registration integrity statement extension

Already incorporated into §9.9; this sub-section explicitly confirms the additional commitments for Amendment 3:

- Not to modify the Phase A-7 ACP twin or the Phase A-7′ Mainstream-Ensemble Baseline scripts after the OSF registration DOI issues, except via a recorded OSF registration update
- Not to tune any locked hyperparameter in either script (TTSA timescales, SPRT thresholds, attention sizes, T-TIME steps, memory buffer, curiosity weights, equilibration threshold, etc.)
- Not to substitute alternative mainstream methods for the locked ensemble composition (SPRT-Liu, TSFNet, T-TIME, memory buffer, foundation-model features). If a reference paper is later retracted, substitution must be a recorded OSF registration update with explicit rationale
- E6 (hyperdirect-pathway latency) and E7′ (sheaf-fusion-ratio) **are reported as N/A by design** for the mainstream-ensemble baseline. This is not a script failure; the mainstream BCI literature has no equivalents to thrIVE's hyperdirect and sheaf-coherence-based fusion mechanisms
- For sub-§11.4 Phase B-2 (if pre-registered): not to tune the curiosity weights, equilibration threshold, or breach-injection rates; not to substitute alternative formulations of the §2.16.3 / §2.16.5 / §2.16.6 mechanisms

### §11.9 Cross-references

| Section | Connection |
|---|---|
| §3, §4 of this preregistration | Original H1–H3 hypotheses |
| §9 (Amendment 1) | H4 R_FM foundation-model baseline |
| §10 (Amendment 2) | H5 R_JEPA end-to-end JEPA baseline |
| [[(C)-Phase-A-Experiment-Revised]] §7.7a | Phase A-7 protocol — Digital ACP twin |
| [[(C)-Phase-A-Experiment-Revised]] §7.7a.9a | Phase A-7′ protocol — Mainstream-ensemble comparison |
| [[(C)-Phase-A7-Digital-ACP-Twin]] | Locked simulator implementation |
| [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]] | Locked mainstream-ensemble baseline |
| [[../02-Theory/(C)-15-Stage-3-Self-Sufficient-Learning-Loops]] §2.16 | Stage 3 active-learning components for optional sub-§11.4 |
| [[../02-Theory/(C)-15-Stage-3-Self-Sufficient-Learning-Loops]] §2.16.8a | Phase B-2 / B-3 / C-1 / D validation chain |
| [[../10-Analysis/02-Open-Questions]] OQ 11.110, 11.111 | Open questions Amendment 3 addresses |
| [[../10-Analysis/02-Open-Questions]] OQ 11.112–11.118 | Open questions sub-§11.4 partially addresses |

### §11.10 Submission instructions

To submit Amendment 3 as a unified OSF registration update:

1. Confirm the locked-script SHA-256 hashes for [[(C)-Phase-A7-Digital-ACP-Twin]] and [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]] are recorded in `registered_hashes.json`
2. Run the synthetic smoke tests on both scripts (`--smoke-test` mode); commit smoke-test JSONs to the repository
3. Tag the repository as `amendment-3-locked` (separate tag from `pre-registration-locked` to keep amendments orderable)
4. Submit the amendment via OSF's "Registration Update" workflow with explicit reference to Amendments 1 (R_FM) and 2 (R_JEPA) as prerequisites
5. Record the new registration DOI in the project manifest as `osf_doi_amendment_3`
6. Update the CI workflow's `registered_hashes.json` and `expected_discrimination_matrix.json` to include H6, H7, and (optionally) H8 outcomes

The amendment is then operationally locked. Phase A-7 and A-7′ execution can begin against PhysioNet EEG data; the locked scripts produce bit-exact reproducible endpoints, and any reviewer can verify the chain end-to-end.

---

## §12 — Pre-Submission Amendment 4: Brain-JEPA / Signal-JEPA Domain-Specific Baseline

> **Status:** Drafted May 2026 following external reviewer audit. Adds R_JEPA_brain as a domain-appropriate JEPA baseline alongside the existing R_JEPA (LeWM-based) cross-domain control. Together they form the dual-baseline JEPA comparison the reviewer audit recommends.

### §12.1 Motivation for Amendment 4

Amendment 2 (R_JEPA, §10) tests thrIVE's sheaf representation against LeWorldModel — a JEPA architecture from the **vision domain**. An external reviewer audit (May 2026) correctly identified this as a cross-domain proxy: LeWM was designed for video pixels, not EEG. The audit recommended supplementing R_JEPA with **Brain-JEPA / Signal-JEPA** — JEPA architectures developed for brain signals specifically.

The architecturally relevant differences:

- **Brain-JEPA** (Yi et al., 2024) — fMRI-domain JEPA with brain-region positional encoding and domain-specific masking
- **Signal-JEPA** (Guetschel et al., 2024) — EEG-specific JEPA whose central finding is that **spatial filtering and pre-local architectures are crucial for downstream performance**
- **ECG-JEPA** — analogous to Signal-JEPA for cardiac signals

The cross-domain R_JEPA arm answers "does sheaf beat a vision-research JEPA?"; the domain-specific R_JEPA_brain arm answers "does sheaf beat a JEPA designed for brain signals?". **Both are needed for the architecturally honest comparison.** A pass on R_JEPA but failure on R_JEPA_brain would indicate that JEPA-on-EEG is competitive when the domain is respected, and that thrIVE's representational complexity does not earn its keep against domain-appropriate JEPA.

### §12.2 New factor levels

| Level | Definition |
|---|---|
| **R_JEPA_brain** | Brain-JEPA / Signal-JEPA-inspired end-to-end JEPA with spatial (channel-wise) masking and per-channel-group pre-local processing, trained jointly on the same training fold data, output projected to $d = 8$ via per-fold PCA |
| **R_JEPA_brain+S** | Concatenated R_JEPA_brain features + S-TTSA sheaf coherence, logistic regression |

Adds 2 × 4 = 8 conditions per subject, raising the total from 3,920 (with Amendments 1, 2) to ~4,792 paired observations. Hoeffding detectability bound unaffected.

### §12.3 Locked R_JEPA_brain configuration

The architecture is locked in [[(C)-R_JEPA-Brain-Feature-Extraction]] with non-negotiable hyperparameters:

| Parameter | Locked value | Rationale |
|---|---|---|
| Channel groups | 8 (each = 8 channels) | Spatial-first decomposition (Signal-JEPA) |
| Spatial mask probability | 0.25 | Signal-JEPA training innovation; per-group independent |
| Pre-local transformer dim / heads / layers | 64 / 4 / 2 | Pre-local processing before global pooling |
| Global transformer dim / heads / layers | 256 / 4 / 1 | Cross-group attention with [GLOBAL] token |
| Electrode positional encoding | Learnable, initialised from 10-10 coordinates | Brain-JEPA domain-specific positional encoding |
| Predictor hidden dim | 512 | **Matched to R_JEPA for fair comparison** |
| SIGReg (M, β, λ_sig) | (1024, 1.0, 1.0) | **Matched to R_JEPA for fair collapse-prevention comparison** |
| Learning rate / weight decay | 1e-3 / 1e-4 | Matched to R_JEPA |
| Training epochs / batch size | 50 / 32 | Matched to R_JEPA |
| Master seed | 42 | Determinism |

**No post-registration tuning of any of these parameters is permitted.** No substitution of alternative regularisers or alternative masking strategies. The dual-baseline JEPA comparison must be conducted under the locked configurations.

### §12.4 New hypothesis H9 — Sheaf adds value over domain-appropriate JEPA

**Hypothesis:** Sheaf coherence adds value over a Brain-JEPA / Signal-JEPA-inspired domain-specific JEPA baseline. Classification using (R8 + S) outperforms classification using R_JEPA_brain features alone, on clean data (S0).

- **Directional prediction:** mean accuracy of (R8 + S) > mean accuracy of R_JEPA_brain at S0
- **Strength criterion:** paired Cohen's $d > 0.2$, one-sided $\alpha = 0.05$
- **Halt condition:** if H9 fails *and* H5 (R_JEPA / LeWM) passes, the architectural conclusion is: **thrIVE beats cross-domain research JEPA but not domain-appropriate JEPA**. The sheaf's representational complexity is unjustified against the JEPA family when the domain is respected; consider whether Stage 1 should adopt Brain-JEPA / Signal-JEPA features as the front-end and use sheaf only for IVE Evidence 1.
- **Failure with H5 pass interpretation:** Phase A-2 (IVE) still runs; the architecture's "novel representational contribution" claim is substantially narrower than the LeWM-only-comparison would suggest.

### §12.5 Five-amendment joint interpretation matrix (H2 / H4 / H5 / H6 / H7 / H9)

Extending the §11.6 matrix with H9:

| Outcome cluster | Architectural verdict |
|---|---|
| **All pass** (H2, H4, H5, H6, H7, H9 all ✓) | **STRONGEST**: sheaf beats every baseline (R8, R_FM, R_JEPA, R_JEPA_brain) and the dynamical architecture beats both LeWM-streaming and mainstream ensemble |
| **H9 fails alone** (others pass) | Sheaf beats cross-domain JEPA but loses to domain-appropriate JEPA — investigate spatial-masking interaction; possible Stage 1 architectural simplification |
| **H5 and H9 both fail** (H4 passes) | Sheaf representational claim fails against any JEPA family; control-system claims (H6, H7) may still survive |
| **H9 passes, H5 fails** | Anomalous — investigate whether R_JEPA encoder is broken vs R_JEPA_brain. Likely a specification or implementation issue in R_JEPA |
| **All fail** | **FUNDAMENTAL HALT**: representational and dynamical architectures both unjustified; major revision required |

The full $2^6 = 64$-cell matrix is in the locked analysis script's interpretation logic.

### §12.6 Statistical analysis amendments

Add to §7 (Analysis Plan):

- **H9 test**: paired BEST on per-subject accuracies (R8+S) − R_JEPA_brain, one-sided alternative, $\alpha = 0.05$. Bayes factor via `pingouin.ttest`.
- **R_JEPA_brain ablation arm**: R_JEPA_brain at all four stressors generates a parallel C4-equivalent graceful-degradation comparison. Reported but not pre-registered as confirmatory.
- **Comparison reporting**: H5 (R_JEPA / LeWM) and H9 (R_JEPA_brain) reported side-by-side as the dual-baseline JEPA comparison. The relative outcome (sheaf beats one but not the other, both, or neither) is the architectural-identity diagnostic.

### §12.7 Pre-registration integrity statement extension

Already incorporated into §9.9; this sub-section confirms the additional commitments for Amendment 4:

- Not to modify the R_JEPA_brain script post-registration except via OSF registration update
- Not to tune any of the locked R_JEPA_brain hyperparameters (mask probability, transformer dimensions, SIGReg weights, learning rate, etc.)
- Not to substitute alternative JEPA architectures (e.g., a different Brain-JEPA variant) post-registration
- Not to apply post-hoc selection between R_JEPA and R_JEPA_brain outcomes; both must be reported regardless of which favours the sheaf
- **The PI commits to verifying the Brain-JEPA / Signal-JEPA architectural principles in the published papers** (Yi et al. 2024; Guetschel et al. 2024) before final OSF lock; the locked script's hyperparameters are reasonable defaults consistent with the published principles but the PI assumes responsibility for final verification

### §12.8 Cross-references

| Section | Connection |
|---|---|
| §10 (Amendment 2) | H5 R_JEPA (LeWM) baseline — cross-domain control; retained alongside R_JEPA_brain |
| [[(C)-Phase-A-Experiment-Revised]] §4.1 (third amendment) | Phase A-1 factor extension to include R_JEPA_brain |
| [[(C)-R_JEPA-Brain-Feature-Extraction]] | Locked executable implementation |
| [[(C)-R_JEPA-Feature-Extraction]] | Sibling cross-domain JEPA baseline |
| [[../02-Theory/(C)-13-Stage-2.5-Developmental-Cogitation-Substrate]] §2.14.2 | JEPA component spec; Brain-JEPA / Signal-JEPA are domain-specific alternatives |

---

## §13 — Pre-Submission Amendment 5: Graph Laplacian Baseline (Cohomology-Isolation Test)

> **Status:** Drafted May 2026 following external reviewer audit. Adds R_GL as the **controlled single-variable test** of whether cellular cohomology — not just graph topology — earns empirical value beyond standard graph spectral methods.

### §13.1 Motivation for Amendment 5

Amendments 1–4 test the sheaf against external baselines that use *no* graph structure (R_FM foundation model), or *different* graph structure (R_JEPA / R_JEPA_brain learned encoders), or *no* sheaf-specific properties at all (R8 Riemannian tangent). **None of them controls for graph topology as the only varying factor.** The external reviewer audit (May 2026) correctly identified this as a structural gap in the test design: without a same-topology + no-cohomology baseline, the spec cannot empirically isolate the contribution of cellular cohomology specifically.

The R_GL arm closes this gap with a **strict single-variable contrast**:

| Property | R_GL (this amendment) | S-TTSA (current spec) |
|---|---|---|
| Graph topology | 40-node Yeo-17-scale, 80 edges | **Same** (matched generator + seed) |
| EEG preprocessing | Bandpass + notch + artefact reject + CAR | **Same** |
| Output dimension | $d = 8$ via per-fold PCA | **Same** |
| Vector-valued stalks | **No (scalar projections)** | Yes ($d = 8$) |
| Restriction maps | **Identity (by definition — graph Laplacian)** | Orthogonal rotors in $\mathrm{O}(d)$ |
| Higher cohomology | **$H^k = 0$ for $k > 0$ by definition** | $H^1(\mathcal{F})$ potentially non-trivial |

If the sheaf's architectural advantage is **cellular cohomology specifically**, then S-TTSA should beat R_GL. If the advantage is just *graph topology*, they should perform equivalently. The R_GL ↔ S-TTSA comparison is therefore the **architecturally diagnostic test** that the spec has been missing.

The theoretical motivation for this amendment is §2.1.6 of [[../02-Theory/02-Cellular-Sheaves-SPD-Manifolds]] (added in this amendment cycle).

### §13.2 New factor levels

| Level | Definition |
|---|---|
| **R_GL** | Top-16 graph-Laplacian eigenmode spectral features on the same 40-node Yeo-17-scale graph topology, with identity restriction maps and scalar (mean signal-energy) per-node projections, output projected to $d = 8$ via per-fold PCA |
| **R_GL+S** | Concatenated R_GL features + S-TTSA sheaf coherence, logistic regression — tests whether graph spectral features and sheaf coherence are complementary or redundant |

Adds 2 × 4 = 8 conditions per subject, raising the total from 4,792 (with Amendments 1, 2, 4) to ~5,664 paired observations. Hoeffding detectability unaffected.

### §13.3 Locked R_GL configuration

The configuration is locked in [[(C)-R_GL-Feature-Extraction]] with non-negotiable parameters:

| Parameter | Locked value | Rationale |
|---|---|---|
| Graph topology | 40 nodes, 80 edges (small-world, matched to sheaf via shared seed) | Same topology, isolates cohomology as variable |
| Channels per neural node | 2 (64 channels / 32 neural nodes) | Per-node electrode grouping |
| Per-node projection | Mean squared signal across channels | Scalar (no vector-valued stalk; identity restriction) |
| Top-K eigenmodes | 16 | Standard graph spectral feature count |
| Context nodes (V/S/K) | Zero-valued in R_GL formulation | Honest minimal baseline — graph Laplacian's scalar formulation has no natural V/S/K projection |
| PCA target dim | $d = 8$ | Matched to R_FM / R_JEPA / R_JEPA_brain |
| Master seed | 42 | Matches Phase A-7 ACP twin for identical graph topology |

**Topology consistency check:** the `build_graph_topology()` function in `rgl_features.py` and the equivalent in `phase_a7_simulator.py` must produce **identical edge lists for the same seed**. This is verified at registration time and listed as a pre-registration checklist item.

### §13.4 New hypothesis H10 — Cellular cohomology earns its keep

**Hypothesis:** Sheaf coherence adds value over a pure graph-Laplacian baseline on the same graph topology. Classification using (R8 + S) outperforms classification using R_GL alone, on clean data (S0).

- **Directional prediction:** mean accuracy of (R8 + S) > mean accuracy of R_GL at S0
- **Strength criterion:** paired Cohen's $d > 0.2$, one-sided $\alpha = 0.05$
- **Halt condition:** if H10 fails, the **architecturally diagnostic conclusion** is: *cellular cohomology does not add measurable empirical value beyond graph-Laplacian alone for the Phase A-1 motor-imagery task.* The §2.1.5 Clifford-rotor structure + §2.1.6 higher-cohomology argument are mathematically defensible but empirically decorative for this task. Stage 1 deployment should consider whether graph-Laplacian features can replace the sheaf, with sheaf reserved for IVE Evidence channels only (or for tasks where cohomological obstructions are more architecturally relevant — e.g., multi-modal Stage 2 prosthetics where the integration cohomology is non-trivial).
- **Failure with H5 / H9 pass interpretation:** if H10 fails but H5 (sheaf > LeWM cross-domain JEPA) and H9 (sheaf > Brain-JEPA domain-specific) both pass, the conclusion is *sheaf beats every JEPA family but not graph Laplacian* — the architecture's empirical value lives in **graph structure + Riemannian feature extraction**, not in cohomology specifically. The Stage 1 architectural simplification would be substantial.

### §13.5 Six-amendment joint interpretation outcomes

Extending the §12.5 matrix with H10:

| Cluster | Verdict |
|---|---|
| **All 6 pass** (H2 ✓, H4 ✓, H5 ✓, H9 ✓, H10 ✓, plus H6 / H7 for dynamics) | **STRONGEST**: sheaf earns every comparison — full architectural justification across all representational and dynamical claims |
| **H10 fails alone** | Cellular cohomology does not add value over graph Laplacian; consider whether Stage 1 should use graph-Laplacian features as the front-end with sheaf reserved for IVE Evidence channels |
| **H10 + H9 both fail (H5 passes)** | The sheaf's empirical advantage is against cross-domain JEPA (LeWM) only; both domain-appropriate JEPA and graph Laplacian on the same topology match the sheaf. **Strong architectural simplification signal** |
| **H10 + H5 + H9 all fail (H2 / H4 pass)** | The sheaf representation is at parity with every alternative baseline. The IVE / control-system / dynamical claims (H6, H7) may still survive — sheaf is then justified only for those roles |
| **All representational claims fail (H2 fails)** | Original H1 halt condition applies; Phase A terminates |

The most informative single outcome is **H10 failing alone** — it cleanly identifies the cohomological structure as the unjustified complexity, while preserving the validity of the JEPA-family comparisons. This is exactly the diagnostic the audit asked for.

### §13.6 Statistical analysis amendments

Add to §7 (Analysis Plan):

- **H10 test:** paired BEST on per-subject accuracies (R8+S) − R_GL, one-sided alternative, $\alpha = 0.05$. Bayes factor via `pingouin.ttest`.
- **R_GL ablation arm:** R_GL at all four stressors generates the parallel graceful-degradation comparison for the graph-Laplacian baseline. Reported but not pre-registered confirmatory.
- **Side-by-side reporting:** H5 (sheaf vs LeWM), H9 (sheaf vs Brain-JEPA), H10 (sheaf vs graph Laplacian) reported in the same table as the **three-way external-baseline comparison** that the audit recommends. Relative outcomes are the architectural-identity diagnostic.

### §13.7 Pre-registration integrity statement extension

Already incorporated into §9.9; this sub-section confirms additional Amendment 5 commitments:

- Not to modify the R_GL script post-registration except via OSF registration update
- Not to tune the locked R_GL parameters (graph topology generator, top-K eigenmodes, channels-per-neural-node, PCA target dimension)
- Not to apply post-hoc selection between R_GL and the sheaf outcomes
- The R_GL script must produce **identical graph topology** to the Phase A-7 ACP twin for the same master seed (verified by checksum of the edge list); any divergence is a registration integrity violation

### §13.8 Cross-references

| Section | Connection |
|---|---|
| §11.6, §12.5 of this preregistration | Joint interpretation matrices extended with H10 |
| [[../02-Theory/02-Cellular-Sheaves-SPD-Manifolds]] §2.1.6 | Theoretical motivation: what cellular cohomology adds beyond graph Laplacian |
| [[(C)-R_GL-Feature-Extraction]] | Locked executable implementation |
| [[(C)-Phase-A7-Digital-ACP-Twin]] | Shared graph topology generator (same seed → same edges) |
| [[(C)-A1-Factorial-Analysis-Script]] | Analysis script consuming R_GL outputs alongside R_FM / R_JEPA / R_JEPA_brain |

---

## Appendix A — Pre-Registration Checklist

Before submitting to OSF:

- [ ] OSF account created
- [ ] Project created with title from §1
- [ ] All §1–§8 fields completed in OSF form
- [ ] [[(C)-Phase-A-Experiment-Revised]] uploaded as supplementary
- [ ] [[(C)-Phase-A-Experiment-Code-Revised]] uploaded as supplementary
- [ ] This document uploaded as supplementary
- [ ] **Code repository public on GitHub with master `environment.yml` and per-script subset YAMLs.** Master `environment.yml` consolidated in [[(C)-Master-Environment]] §1 (the dependency union of all 12 locked artefacts). Per-script `environment_<script>.yml` files (10 of them, one per locked artefact except the CI workflow and the synthetic smoke-test generator) ship in the script docs and remain valid as partial environments. Master SHA-256 logged as `master_env_yml_sha256`. One version reconciliation documented in [[(C)-Master-Environment]] §2: A-0 originally pinned pandas 2.1 → master pins 2.2 (changelog-verified, no breaking changes for A-0 operations).
- [ ] Master seed (42) and analysis script hash documented
- [ ] No data downloaded, no analysis run, no test-fold accuracy seen
- [x] **Seely equivalence paper-check completed (§0 of revised protocol)** — closed May 2026 by [[../02-Theory/(C)-16-Seely-Equivalence-Independent-Derivation]]. Two independent derivations (algebraic Rao–Ballard in §3, categorical St Clere Smithe 2023 in §4) agree under five shared qualifications, all satisfied for the Phase A-1 architecture. §0 of [[(C)-Phase-A-Experiment-Revised]] marked complete.
- [ ] **§9 Amendment 1 incorporated** (LCM URL/MD5 logged; EEGFormer fallback URL/MD5 logged; PCA projection procedure locked)
- [ ] §9.9 integrity statement signed (no foundation model run on EEGMMIDB)
- [ ] **R_FM extraction script locked.** [[(C)-R_FM-Feature-Extraction]] committed at a tagged `pre-registration-locked` git tag. Script SHA-256 hash and git commit hash logged in OSF manifest. Smoke test on synthetic Gaussian noise committed to repository (no PhysioNet data touched)
- [ ] **A1 analysis script locked.** [[(C)-A1-Factorial-Analysis-Script]] committed at the same `pre-registration-locked` git tag. Script SHA-256 hash logged in OSF manifest as `a1_analysis_script_sha256`
- [ ] **A1 synthetic smoke-test generator locked.** [[(C)-A1-Synthetic-Smoke-Test-Generator]] committed at the same tag. Script SHA-256 logged as `a1_synthetic_script_sha256`. All five scenarios (`all_pass`, `h1_fail`, `h2_fail`, `h3_fail`, `h4_fail`) generated; `analyse_a1_factorial.py` run on each; **discrimination matrix verified** — five results.json files match the expected verdict table. Each `results.json` SHA-256 recorded in OSF manifest as `smoke_<scenario>_sha256`
- [ ] **CI workflow locked and green.** [[(C)-CI-Workflow-Preregistration-Verify]] committed at `.github/workflows/preregistration-verify.yml`. Helper scripts `verify_script_hashes.py`, `verify_discrimination_matrix.py`, `expected_discrimination_matrix.json` committed under `scripts/`. `registered_hashes.json` populated with all three locked scripts' SHA-256s. CI workflow triggered on a test branch, **all three gates pass** (hash, smoke-test execution, discrimination matrix). GitHub branch protection enabled requiring CI green before merge to `main`
- [ ] **Phase B-1 harmonic simulator locked (optional pre-registration for §7.8).** [[(C)-Phase-B1-Harmonic-Simulator]] committed at a `phase-b1-locked` git tag. Script SHA-256 logged as `phase_b1_script_sha256`. Smoke test run (`--smoke-test --n-seeds 3`); smoke-test JSON committed to repository. Full factorial result JSON committed if the simulator has been executed. (Phase B-1 is simulation-only and can be locked independently of the A-1 pre-registration.)
- [ ] **R_JEPA feature extraction locked (Amendment 2 to Phase A-1).** [[(C)-R_JEPA-Feature-Extraction]] committed at the same `pre-registration-locked` git tag. Script SHA-256 logged as `r_jepa_script_sha256`. **All locked hyperparameters confirmed unchanged from spec defaults**: SIGReg M = 1024, β = 1.0, λ_sig = 1.0, lr = 1e-3, weight decay = 1e-4, 50 train epochs, batch size 32, master seed 42. Smoke test on synthetic Gaussian data (`--smoke-test`) runs end-to-end without error; smoke-test outputs (`rjepa_smoke.npz`, `rjepa_smoke_manifest.json`) committed to repository. Per-fold isolation discipline verified: PCA fit only on training latents; encoder + predictor trained only on training fold; test fold never seen during training. §9.9 integrity statement extended to cover R_JEPA: no PhysioNet EEGMMIDB data touched by this script before registration.
- [ ] **R_JEPA_brain feature extraction locked (Amendment 4 to Phase A-1).** [[(C)-R_JEPA-Brain-Feature-Extraction]] committed at the same `pre-registration-locked` git tag (alongside R_JEPA). Script SHA-256 logged as `r_jepa_brain_script_sha256`. **All locked hyperparameters confirmed unchanged**: 8 channel groups × 8 channels each, spatial mask probability 0.25, pre-local transformer (dim 64 / 4 heads / 2 layers), global transformer (dim 256 / 4 heads / 1 layer), predictor hidden 512, SIGReg matched to R_JEPA (M=1024, β=1, λ_sig=1), lr=1e-3, wd=1e-4, 50 epochs, batch 32, seed 42. **PI has verified Brain-JEPA (Yi et al., 2024) and Signal-JEPA (Guetschel et al., 2024) architectural principles in the published papers** before final lock. Smoke test runs end-to-end on synthetic Gaussian data; smoke-test outputs committed. **PI has substituted actual PhysioNet EEGMMIDB 64-channel 10-10 coordinates** for the placeholder Fibonacci-sphere positional encoding (or has explicitly documented why the placeholder is retained as adequate). No PhysioNet data touched by this script before registration.
- [ ] **R_GL feature extraction locked (Amendment 5 to Phase A-1).** [[(C)-R_GL-Feature-Extraction]] committed at the same `pre-registration-locked` git tag. Script SHA-256 logged as `r_gl_script_sha256`. **All locked parameters confirmed unchanged**: 40-node 80-edge graph topology (small-world, seed 42), top-K = 16 eigenmodes, 2 channels per neural node, V/S/K context nodes zero-valued in R_GL formulation (honest minimal baseline), PCA target dim = 8 (matched to R_FM / R_JEPA / R_JEPA_brain). **Topology checksum verified**: the edge list produced by `build_graph_topology()` in `rgl_features.py` is **bit-identical to** the edge list produced by the corresponding function in [[(C)-Phase-A7-Digital-ACP-Twin]] for master seed 42 — verified by SHA-256 of the edge-list bytes, recorded in the OSF manifest as `shared_graph_topology_sha256`. Any divergence is a registration integrity violation. Smoke test (`--smoke-test`) runs end-to-end on synthetic Gaussian data; smoke-test outputs committed. No PhysioNet data touched before registration.
- [ ] **A-0 preflight reference pipeline locked (the load-bearing gate).** [[(C)-A0-Preflight-Reference-Pipeline]] committed at the same `pre-registration-locked` git tag. Script SHA-256 logged as `a0_script_sha256`. **All locked parameters confirmed unchanged**: 5-fold MOABB `WithinSession` evaluation, `Covariances(estimator="oas")` + `TangentSpace(metric="riemann")` + `LogisticRegression(C=1.0, penalty="l2", solver="liblinear", max_iter=1000)`, MOABB ≥ 1.4 paradigms (`LeftRightImagery` for PhysioNetMI, `MotorImagery` 4-class for BCI IV-2a) at defaults (8–32 Hz, tmin=0, tmax=4 s), master seed 42, **corrected gate thresholds ≥ 0.633 (PhysionetMI L/R binary) and ≥ 0.68 (BCI IV-2a 4-class)**. **MOABB-published reference value cross-check COMPLETED May 2026** — verified TS+LR accuracies are 67.28 ± 19.19% (PhysionetMI Left-vs-Right; not 92% — the 92% number in the v2.0 draft was a confusion with the Right-Hand-vs-Feet paradigm at 93.15%) and 71.97 ± 15.46% (BCI IV-2a 4-class; not 78%). Cross-checked against [the MOABB official benchmark results page](https://moabb.neurotechx.com/docs/paper_results.html) and Chevallier et al. (2024) arXiv:2404.15319 Appendix D, Tables 6–10. §3 of [[(C)-Phase-A-Experiment-Revised]] updated with corrected gates + errata note before this checklist item was signed off. The 4-pp tolerance (vs original 2-pp) is one σ/5 of the published cross-subject distribution. Smoke test (`--smoke-test`) runs end-to-end on synthetic SPD data; mean accuracy > 0.95; smoke-test JSON committed. Single-subject sanity check (`--single-subject 1` on PhysioNetMI) run; output committed. **A-0 is the only locked script for which a subsequent failed gate run terminates the entire programme** until the reference pipeline is repaired — H1–H10 results are uninterpretable against an unvalidated baseline. No bulk PhysioNet data analysis beyond the MOABB cache download before registration.
- [ ] **Phase A-7 Digital ACP Twin locked (Amendment 3 to Phase A-1).** [[(C)-Phase-A7-Digital-ACP-Twin]] committed at a `phase-a7-locked` git tag (can be a separate tag from Phase A-1 if Phase A-7 is deferred). Script SHA-256 logged as `phase_a7_script_sha256`. **All locked parameters confirmed unchanged**: TTSA timescales (fast=50ms, int=30s, slow=5min, uslow=30min, LTP=1h) and rates, SPRT α=1e-3 / β=0.1, sensory-anchored inhibition constants (σ_DN=0.1, n=2, β_sensory=0.3, γ_h=0.5), hyperdirect-latency cap = 2 cycles, modelled noise (σ=0.05, τ_OU=100ms), critical-period reopen-threshold = 0.3 BW. Smoke test (`--smoke-test`) runs end-to-end on synthetic EEG and produces valid endpoint JSON. **No PhysioNet data touched by this script before registration.** Full per-condition runs (2 × 4 × 4 = 32 conditions × 103 subjects × 5 folds = 16,480 paired observations) committed to repository as endpoint JSONs.
- [ ] **Phase A-7′ Mainstream-Ensemble Baseline locked (Amendment 3 sibling).** [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]] committed at the same `phase-a7-locked` git tag. Script SHA-256 logged as `phase_a7_ensemble_script_sha256`. **All composition components confirmed identical to published methods**: SPRT-Liu 2017 (single-channel, α=1e-3 / β=0.1 matched to ACP twin), TSFNet-style attention fusion (4 heads, hidden=64), Wu T-TIME 2024 (lr=1e-4, 5 steps per session), memory-buffer continual learning (200 epochs, class-balanced sampling), foundation-model features reuse the locked [[(C)-R_FM-Feature-Extraction]] outputs (no re-extraction). Smoke test runs end-to-end on synthetic data; smoke-test JSON committed. **E6 (hyperdirect latency) and E7′ (sheaf-fusion-ratio) reported as N/A by design** — explicitly documented as the architectural-identity test that the mainstream cannot match. No PhysioNet data touched before registration. Runs the same 2 × 4 × 4 conditions as the ACP twin on identical input streams for direct paired comparison.
- [ ] **§6.4.5 IVE signal-quality channel (May 2026 addition).** The signal-quality channel specified in §6.4.5 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] is a Stage-2/Stage-3 dependency, **not** a Phase A-1 confirmatory test. For OSF lock, confirm: (a) the prerequisite-gate + threshold-modulator architecture (not a sixth multiplicative product term) is unchanged; (b) the four sub-indicator definitions ($q_{\mathrm{channel}}, q_{\mathrm{emg}}, q_{\mathrm{distshift}}, q_{\mathrm{adv}}$) match the §4.1 stressor literature citations of [[(C)-Phase-A-Experiment-Revised]]; (c) the Phase A-2 IVE Evidence Integration experiment is extended to include $q(t)$ as a sixth **diagnostic output** (not a product term), so the empirical correlation with Evidence 1–4 can be quantified before $q_{\min}$ and $\kappa_q$ are locked at Stage-2 deployment time. Implementation lock for Phase A-2 deferred to Stage 2; the architectural commitment is locked now.
- [ ] **§7.5a Phase 5b subject-eligibility gate (May 2026 addition).** The 0.60 per-subject A-0-equivalent eligibility threshold from §7.5a of [[../07-Implementation/01-Calibration-Deployment]] is pre-registered. Confirm: (a) threshold value 0.60 unchanged (one σ below the MOABB-published 0.6728 population mean); (b) the per-subject 5-fold within-session CV protocol matches the locked A-0 pipeline; (c) the `subject_passed_a0: bool` field is signed by the Ethics Core PUF key; (d) the three stage-specific failure modes (Stage 1 raised-threshold, Stage 2 motion-command withholding, Stage 3 zero federated weight) are unchanged. Pre-registration lock prevents post-hoc threshold tuning.
- [ ] **[[../11-Integration-Future/(C)-10-Quality-Weighted-Federation-Spec]] (May 2026 addition).** The Stage-3 federation spec is **not** a Phase A-1 confirmatory test — Stage 3 federation does not go live during Phase A. Confirm for lock: (a) the spec's reliance on §6.4.5 IVE signal-quality and §7.5a eligibility gate is unchanged; (b) the §2.4 convex-combination global update rule is unchanged; (c) the privacy/integrity tier (secure aggregation, DP, no-federation) defaults match [[../09-Cybersecurity/02-Fleet-Defence-Federated-Learning]]. The two new OQs (11.119, 11.120) are pre-registered as Stage-3 deployment-readiness questions. Stage-3 operational parameters ($\gamma$, $q_{\mathrm{fed,min}}$, $q_{\mathrm{tier,A}}$) are NOT locked at Phase A-1 OSF lock — they are deferred to the Stage-3 OSF supplementary registration.
- [ ] **PI signature equivalent:** click "Register" on OSF
- [ ] DOI recorded in [[(C)-Phase-A-Experiment-Revised]] §0 and in `manifest_A1.json`

After DOI issuance:

- [ ] Run Phase A-0 preflight via [[(C)-A0-Preflight-Reference-Pipeline]] on both datasets; verify `gate_passed: true` in both output JSONs (**PhysionetMI L/R binary grand-average ≥ 0.633; BCI IV-2a 4-class grand-average ≥ 0.68 — corrected May 2026 from earlier draft values 0.90 / 0.76; see §3 of [[(C)-Phase-A-Experiment-Revised]] errata note**). The script writes the verdict explicitly; no manual interpretation. Manifest SHA-256 cross-verified against the locked `a0_script_sha256`.
- [ ] If A-0 fails on either dataset, follow the failure decision tree in [[(C)-A0-Preflight-Reference-Pipeline]] (subject-outlier inspection → MOABB cache clear → paradigm-default verification → pipeline-misconfiguration repair). **Document the failure, the repair, and the SHA-256 of any modified file as a recorded OSF registration update before re-attempting the gate.**
- [ ] If A-0 passes on both datasets, proceed to A-1 factorial execution
- [ ] No modifications to analysis script
- [ ] No modifications to inclusion criteria
- [ ] No additional analyses substituted for preregistered ones

---

## Appendix B — What Counts as a Deviation

Deviations from this preregistration must be documented as an OSF registration update (publicly visible, with timestamps). The following are examples of what count as deviations:

| Action | Deviation? |
|--------|------------|
| Changing $\mathrm{BF}_{10}$ threshold from 3 to 10 | Yes |
| Adding a 6th representation condition after seeing results | Yes |
| Excluding a subject for any reason not in §7 | Yes |
| Switching from rmANOVA to permutation test for H3 | Yes |
| Computing additional exploratory analyses | No (clearly labelled exploratory) |
| Fixing a discovered bug in the code that changes results | Yes |
| Re-running with a different random seed because the first looked weird | Yes (and is integrity-violating) |
| Adding a sentence to the discussion section of the paper | No |

The principle: anything that changes what would have been the registered analysis plan is a deviation. Anything that adds material clearly labelled exploratory is not.

---

## Appendix C — Failure Modes the Preregistration Locks Out

This preregistration prevents the following common integrity failures:

1. **HARKing (Hypothesising After Results are Known):** H1, H2, H3 are stated before data is touched.
2. **Optional stopping:** sample size fixed at $N = 103$ in §5; no peeking.
3. **Cherry-picking conditions:** all 5 × 4 cells are reported regardless of which look favourable.
4. **Shifting goalposts:** $\mathrm{BF}_{10}$ threshold, Cohen's $d$ threshold, and $\alpha$ are fixed in §7.
5. **Selective seed search:** master seed = 42, all sub-seeds derived deterministically.
6. **Outcome switching:** primary outcome is accuracy; AUC and $\kappa$ are pre-specified secondary.
7. **Post-hoc exclusion:** exclusion criteria fixed in §7 before data download.
8. **Garden of forking paths:** analysis script hash logged; modifications visible.
9. **Spinning a null result:** halt condition 2 in §5 commits to publishing the null.
10. **Preregistration-publication mismatch:** OSF registration is timestamped and publicly comparable to the eventual paper.

The preregistration is the integrity guarantee. Its purpose is not to prevent you from learning anything new — exploratory analyses are explicitly allowed in §7 — but to ensure that what you call confirmatory is genuinely confirmatory.

---

## End of Preregistration

After OSF submission and DOI issuance, this document is the binding analysis plan for Phase A-1. Subsequent phases (A-2 IVE evidence integration, A-3 cross-session transfer, A-4 quantisation) require their own separate preregistrations once Phase A-1 results inform their design.
