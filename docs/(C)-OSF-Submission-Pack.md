# OSF Submission Pack — Phase A-1 Pre-Registration

> **Status:** Drafted May 2026 as the reviewer-facing front-matter for the Phase A-1 OSF pre-registration. Contains:
> - **§1** — the public-repo `README.md` (copy directly to the repository root)
> - **§2** — the OSF cover description (paste into the OSF "Project Description" field at submission time)
> - **§3** — the OSF §1–§8 field map (which content from [[(C)-OSF-Preregistration-Phase-A1]] goes into which OSF web form field)
> - **§4** — the post-DOI manifest fields (one-line-per-field list for the run-time JSON)
>
> All four are pre-OSF deliverables. Engineering execution (commit, tag, SHA-256, smoke runs, CI green, OSF account, register) consumes this pack as input.

---

## §1 Public-Repo `README.md` — copy to repository root

The README is reviewer-facing: a researcher arriving from the OSF DOI should be able to read this single file and understand (a) what the pre-registration tests, (b) where every locked artefact lives, (c) how to reproduce any result, and (d) what each outcome means for the architecture. Three minutes of reading time, plus links into the specifications for depth.

```markdown
# thrIVE Phase A-1 — Pre-Registered Sheaf-Coherence Falsification Test

[![CI](https://github.com/<user>/<repo>/actions/workflows/preregistration-verify.yml/badge.svg)](https://github.com/<user>/<repo>/actions/workflows/preregistration-verify.yml)
[![DOI](https://img.shields.io/badge/OSF-DOI:%20%3CTBD%3E-blue)](https://doi.org/<DOI>)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](LICENSE)

**What this is.** A pre-registered factorial test of whether unsupervised
Two-Timescale Stochastic Approximation (TTSA) learning on the predictive-coding
energy of a cellular sheaf produces motor-imagery-discriminative coherence on
real EEG. Six baselines, ten confirmatory hypotheses (H1–H10), five amendments,
six pre-committed alternative-architectural-identity outcome paths, all locked
at OSF before any data is touched.

**The headline result this experiment can deliver.** Either thrIVE's sheaf /
IVE / dynamical architectural commitments earn their representational complexity
against the field's strongest baselines, or one of the six pre-committed
fall-back identities (no-sheaf, IVE-only-sheaf, graph-Laplacian-spectral,
domain-specific-JEPA, mainstream-ensemble, fundamental-halt) is the architecture
the data actually supports. The PI commits to publishing the surviving identity
regardless of which outcome cluster occurs.

---

## 30-second tour

| You want to | Open |
|---|---|
| Read the full pre-registration | `docs/(C)-OSF-Preregistration-Phase-A1.md` |
| Read the experimental design | `docs/(C)-Phase-A-Experiment-Revised.md` |
| Read the joint-interpretation outcome matrices | §9.6, §10.5, §11.6, §12.5, §13.5 of the OSF pre-registration |
| See what each H1–H10 failure means architecturally | §2 "Alternative-architectural-identity outcome paths" of the OSF pre-registration |
| Verify a script SHA-256 against the registered hash | `python scripts/verify_script_hashes.py` |
| Run the gating preflight on PhysionetMI | `python a0_preflight.py --dataset physionet --output a0_physionet.json` |
| Run the gating preflight on BCI Competition IV-2a | `python a0_preflight.py --dataset bci_iv_2a --output a0_bci_iv_2a.json` |
| Run all five synthetic smoke-test scenarios | `bash scripts/run_smoke_tests.sh` |
| Verify the H1–H10 discrimination matrix | `python scripts/verify_discrimination_matrix.py` |
| Re-derive the Seely equivalence | `docs/(C)-16-Seely-Equivalence-Independent-Derivation.md` |

---

## What we test

Phase A-1 is a 5 × 4 within-subject factorial design extended by five
pre-submission amendments to a 14-level Factor 1 × 4-level Factor 2 = 56
conditions per subject, evaluated on 109 subjects of the PhysioNet
EEG Motor Movement/Imagery Dataset (Schalk et al., 2004) under the Varbu
et al. (2024) annotation curation. **Ten confirmatory hypotheses** (H1–H10),
each with a pre-registered strength criterion (BF₁₀ > 3 or Cohen's d > 0.2),
test the load-bearing architectural claims:

| H | Tests | What success means |
|---|---|---|
| **H1** | S-TTSA > S-rand at S0 | Unsupervised predictive-coding-energy TTSA produces discriminative sheaf coherence |
| **H2** | (R8+S) > R8 at S0 | Sheaf augments Riemannian tangent features |
| **H3** | Sheaf graceful-degradation under S1/S2 stressors | Sheaf is more robust than R8 |
| **H4** | (R_FM+S) > R_FM | Sheaf adds value over an EEG foundation model |
| **H5** | (R8+S) > R_JEPA (LeWM cross-domain) | Sheaf beats cross-domain JEPA |
| **H6** | thrIVE-dynamic > R_JEPA-streaming | Dynamical architecture beats streaming LeWM |
| **H7** | thrIVE-composite > BCI mainstream ensemble | Dynamical architecture beats deployable BCI baseline |
| **H8 (optional)** | Stage-3 §2.16 components work as designed | Curiosity / equilibration / autopoietic mechanisms validate |
| **H9** | (R8+S) > R_JEPA_brain (domain-specific) | Sheaf beats domain-appropriate JEPA |
| **H10** | (R8+S) > R_GL (same topology, no cohomology) | Cellular cohomology — not just graph topology — earns empirical value |

If H1 fails, the experiment halts and the sheaf layer is removed from the
thrIVE architecture. Phase A-2, A-3, A-4 are not run. Published as a null
result.

---

## The locked-artefact set (12 scripts)

Every script in this repository carries a SHA-256 logged in the OSF manifest
at registration time. Any post-registration modification requires a recorded
OSF registration update. The CI workflow at `.github/workflows/preregistration-verify.yml`
gates all three: hash verification, smoke-test execution, and discrimination-matrix
verification — branch protection on `main` requires CI green before merge.

| # | Script | Role | Smoke-test command |
|---|---|---|---|
| 1 | `a0_preflight.py` | MOABB Riemannian-tangent reference-pipeline **gate** | `python a0_preflight.py --smoke-test --output a0_smoke.json` |
| 2 | `rfm_features.py` | Pre-trained EEG foundation-model features (R_FM) | `python rfm_features.py --smoke-test` |
| 3 | `rjepa_features.py` | LeWM-style cross-domain JEPA (R_JEPA) | `python rjepa_features.py --smoke-test` |
| 4 | `rjepa_brain_features.py` | Brain-/Signal-JEPA domain-specific (R_JEPA_brain) | `python rjepa_brain_features.py --smoke-test` |
| 5 | `rgl_features.py` | Graph-Laplacian-only (R_GL — cohomology-isolation test) | `python rgl_features.py --smoke-test` |
| 6 | `analyse_a1_factorial.py` | H1–H10 hypothesis tests + joint interpretation matrix | (driven by `synth_a1.py`) |
| 7 | `synth_a1.py` | Synthetic A-1 scenarios for analysis-pipeline verification | `bash scripts/run_smoke_tests.sh` |
| 8 | `.github/workflows/preregistration-verify.yml` | CI workflow — hash + smoke + matrix | runs on every commit |
| 9 | `phase_b1_simulator.py` | THINK-mode harmonic-preservation simulator | `python phase_b1_simulator.py --smoke-test --n-seeds 3` |
| 10 | `phase_a7_acp_twin.py` | Core dynamical-architecture digital twin | `python phase_a7_acp_twin.py --smoke-test` |
| 11 | `phase_a7_ensemble.py` | Locked BCI mainstream ensemble baseline | `python phase_a7_ensemble.py --smoke-test` |
| 12 | `phase_b2_stage3.py` | Stage-3 §2.16 component validation (optional) | `python phase_b2_stage3.py --smoke-test` |

The SHA-256s shipped at registration are in `registered_hashes.json`. Verify
locally with:

\`\`\`bash
python scripts/verify_script_hashes.py registered_hashes.json
\`\`\`

---

## The Phase A-0 gate (the load-bearing entry)

Before any H1–H10 result can be interpreted, the Riemannian-tangent reference
pipeline must reproduce the MOABB-published benchmark:

| Dataset | Gate threshold | MOABB-published TS+LR | Tolerance |
|---|---|---|---|
| PhysionetMI binary L/R MI | **grand-average ≥ 0.633** | 67.28 ± 19.19 % | 4 pp (~σ/5) |
| BCI Competition IV-2a 4-class | **grand-average ≥ 0.68** | 71.97 ± 15.46 % | 4 pp (~σ/5) |

**Run the gate:**

\`\`\`bash
python a0_preflight.py --dataset physionet --output a0_physionet.json
python a0_preflight.py --dataset bci_iv_2a --output a0_bci_iv_2a.json
\`\`\`

Both JSONs must contain `"gate_passed": true`. If either fails, the H1–H10
results are uninterpretable until the reference pipeline is repaired per the
decision tree in `docs/(C)-A0-Preflight-Reference-Pipeline.md` §"Gate-failure
decision tree". Any repair must be recorded as an OSF registration update
before re-attempting the gate.

> **Errata note (May 2026).** The originally-drafted gate thresholds (≥0.90 /
> ≥0.76, on the assumption of 92 % / 78 % published baselines) were spec-side
> errors that confused the easier right-hand-vs-feet binary paradigm
> (MOABB-published 93.15 %) with the standard left-vs-right binary paradigm
> the experiment actually uses (67.28 %). The corrected gates were verified
> against [the official MOABB results page](https://moabb.neurotechx.com/docs/paper_results.html)
> and Chevallier et al. (2024) arXiv:2404.15319 Appendix D, Tables 6–10, before
> OSF lock. Full errata in `docs/(C)-Phase-A-Experiment-Revised.md` §3 and
> in the Stage-Dependency Trace at `docs/(C)-09-Stage-Dependency-Trace-Post-MOABB-Correction.md`.

---

## Environment

Master conda environment at the repository root:

\`\`\`bash
conda env create -f environment.yml
conda activate thrive_phase_a1
\`\`\`

Per-script subset environments (`environment_<script>.yml`) are kept available
for partial-environment reproduction on minimal CI runners. See
`docs/(C)-Master-Environment.md` for the dependency map.

---

## What this study can falsify

Six pre-committed alternative architectural identities, one per outcome
cluster. Reviewers should read §2 of the OSF pre-registration for the formal
mapping; the high-level summary:

| Outcome | Alternative identity thrIVE collapses to |
|---|---|
| H1 fails | **No-sheaf** — Riemannian-only Stage 1 + IVE-without-Evidence-1 |
| H1 passes, H2 fails | **IVE-only-sheaf** — sheaf retained only as IVE Evidence 1 |
| H10 fails alone | **Graph-Laplacian-spectral** — cohomology decorative; flagged by external audit |
| H5 + H9 both fail | **Domain-specific-JEPA** — Brain-/Signal-JEPA encoder spine |
| H6 + H7 both fail | **Mainstream-ensemble** — SPRT-Liu + TSFNet + T-TIME + ST-EEGFormer |
| All confirmatory hypotheses fail | **Fundamental halt** — major spec revision required |

The PI commits to publishing the surviving alternative identity regardless of
which outcome cluster occurs.

---

## Citation

If you use this pre-registration, please cite:

\`\`\`bibtex
@misc{cognat_thrive_phase_a1_2026,
  author       = {Cognat, Théo},
  title        = {{thrIVE Phase A-1: Sheaf-Coherence Falsification on Motor Imagery EEG}},
  year         = {2026},
  doi          = {10.17605/OSF.IO/<DOI>},
  url          = {https://doi.org/10.17605/OSF.IO/<DOI>},
  note         = {Pre-registration with five amendments}
}
\`\`\`

---

## Licence

All code: MIT. Specifications and analyses: CC-BY-4.0.

---

## Repository structure

\`\`\`
.
├── README.md                              # this file
├── LICENSE
├── environment.yml                        # master conda env
├── environment_<script>.yml               # per-script subset envs
├── a0_preflight.py                        # the gating script
├── rfm_features.py
├── rjepa_features.py
├── rjepa_brain_features.py
├── rgl_features.py
├── analyse_a1_factorial.py
├── synth_a1.py
├── phase_b1_simulator.py
├── phase_a7_acp_twin.py
├── phase_a7_ensemble.py
├── phase_b2_stage3.py
├── registered_hashes.json                 # SHA-256s at OSF registration
├── expected_discrimination_matrix.json    # H1–H10 expected verdicts on synth
├── manifest_A1.json                       # OSF manifest (DOI, hashes, run state)
├── .github/
│   └── workflows/
│       └── preregistration-verify.yml     # CI workflow
├── scripts/
│   ├── verify_script_hashes.py
│   ├── verify_discrimination_matrix.py
│   ├── run_smoke_tests.sh
│   └── compute_master_env_sha256.sh
├── docs/
│   ├── (C)-OSF-Preregistration-Phase-A1.md
│   ├── (C)-Phase-A-Experiment-Revised.md
│   ├── (C)-A0-Preflight-Reference-Pipeline.md
│   ├── (C)-Master-Environment.md
│   ├── (C)-16-Seely-Equivalence-Independent-Derivation.md
│   ├── (C)-09-Stage-Dependency-Trace-Post-MOABB-Correction.md
│   └── (C)-10-Quality-Weighted-Federation-Spec.md
└── results/
    ├── raw/                               # per-script per-subject outputs
    ├── smoke/                             # synthetic-scenario outputs
    └── a1_results.json                    # H1–H10 analysis verdicts
\`\`\`
```

---

## §2 OSF Cover Description — paste into OSF "Project Description" field

The cover description is what appears at the top of the OSF project page. It mirrors §2 of [[(C)-OSF-Preregistration-Phase-A1]] but condensed to ~600 words for the OSF "Description" field (which has a soft limit reviewers actually read). The §2 of the full pre-registration is the canonical version — what follows is a paste-ready condensed extract.

---

This study tests whether unsupervised Two-Timescale Stochastic Approximation (TTSA) learning of restriction maps on the predictive-coding energy of a cellular sheaf produces sheaf coherence that discriminates motor-imagery states on real EEG, recovers information lost by eigenvalue channel selection, and degrades gracefully under channel dropout and EMG artefact injection — three load-bearing claims of the thrIVE Brain-Computer Interface architecture (Cognat, 2026).

The sheaf-theoretic predictive-coding framework follows Seely et al. (2025), who proved $E_{\mathrm{PC}} = \mathbf{x}^\top L_\mathcal{F} \mathbf{x}$ for linear predictive coding networks. thrIVE's Phase A-1 is the first empirical test on biological EEG of whether this equivalence yields discriminative coherence under the unsupervised TTSA learning rule (Borkar, 2008). The Seely equivalence has been independently re-derived from the Rao–Ballard (1999) prediction-error formulation and cross-verified via the St Clere Smithe (2023) categorical route under five shared qualifications, all satisfied by the Phase A-1 architecture (see supplementary `docs/(C)-16-Seely-Equivalence-Independent-Derivation.md`).

The experiment uses a 5 × 4 within-subject factorial design (representation × stressor) on PhysioNet EEG Motor Movement/Imagery Dataset (Schalk et al., 2004; Varbu et al., 2024 curation) with all 109 subjects, extended by five pre-submission amendments to 14 representation levels × 4 stressor levels = 56 conditions per subject. The representation factor spans Riemannian-only baselines (R32, R8), sheaf variants (S-rand, S-TTSA, R8+S), an EEG foundation-model baseline (R_FM, R_FM+S), two JEPA baselines (R_JEPA cross-domain, R_JEPA_brain domain-specific, each with +S), a graph-Laplacian cohomology-isolation baseline (R_GL, R_GL+S), and Phase A-7 streaming variants (thrIVE-dynamic, BCI mainstream ensemble). The stressor factor covers clean data, 2-of-32 channel dropout, 0 dB EMG contamination at 25 % epoch prevalence, and leave-one-subject-out cross-validation. Stressor literature grounding: Gómez-Morales et al. (2025), Khanam et al. (2025), Whitham et al. (2007), Muthukumaraswamy (2013), Mullen et al. (2015), Jayaram et al. (2016), Wu et al. (2022).

Ten confirmatory hypotheses (H1–H10) test the architectural claims. Pre-registered Bayesian and frequentist analysis plans, fixed bootstrap and BEST (Kruschke, 2013) procedures, and explicit halt conditions for each hypothesis are specified. Phase A-0 preflight gates the entire programme: the locked Riemannian-tangent + L2 logistic-regression reference pipeline must reproduce the MOABB-published TS+LR baseline within 4 percentage points (PhysionetMI binary L/R ≥ 0.633 from MOABB-published 67.28 ± 19.19 %; BCI IV-2a 4-class ≥ 0.68 from MOABB-published 71.97 ± 15.46 %, both verified May 2026 against Chevallier et al. 2024).

The study's architectural value is its falsifiability: six pre-committed alternative-architectural-identity outcome paths (no-sheaf, IVE-only-sheaf, graph-Laplacian-spectral, domain-specific-JEPA, mainstream-ensemble, fundamental halt) are formally specified in §2 of the supplementary pre-registration. The PI commits to publishing the surviving identity regardless of outcome cluster. All twelve locked artefact scripts carry SHA-256 hashes registered in the OSF manifest; the GitHub CI workflow gates hash verification, smoke-test execution, and discrimination-matrix verification on every commit. All code, raw data, and analysis scripts will be released under MIT licence at experiment completion.

---

## §3 OSF §1–§8 Field Map — what content goes into which OSF web form field

The OSF web form has named fields; the [[(C)-OSF-Preregistration-Phase-A1]] document has matching §1–§8 sections. The mapping is direct:

| OSF web field | Source section in [[(C)-OSF-Preregistration-Phase-A1]] | Notes |
|---|---|---|
| **Title** | §1 | Long title — copy verbatim |
| **Description** | §2 (condensed) | Use the §2 extract from §2 of this doc, *not* the full §2 of the pre-reg |
| **Hypotheses** | §3 (H1–H3 confirmatory; cite §9.5 for H4, §10.4 for H5, §11 for H6–H8, §12.4 for H9, §13.4 for H10) | Three confirmatory primary, ten total including amendments |
| **Design Plan / Study Type** | §4 | "Observational study with experimental analysis" |
| **Blinding** | §4 (sub-section) | "Analyst blinding via locked CI-verified discrimination matrix" |
| **Study Design** | §4 (sub-section) | 5 × 4 within-subject factorial extended by 5 amendments |
| **Randomisation** | §4 (sub-section) | Master seed 42; CV fold randomisation locked in scripts |
| **Sampling Plan / Existing Data** | §5 | "Yes — PhysioNet EEGMMIDB (publicly available since 2004)" |
| **Data Collection** | §5 (sub-section) | Curated by Varbu et al. (2024) |
| **Sample Size** | §5 (sub-section) | 109 subjects; 103 after Varbu exclusions |
| **Sample Size Rationale** | §5 (sub-section) | Hoeffding 2.4 pp + G*Power d = 0.12; full §14 power analysis as supplementary |
| **Stopping Rule** | §5 (sub-section) | Halt criterion 1: A-0 gate failure; halt criterion 2: H1 BF₁₀ ≤ 3 |
| **Variables** | §6 | Representation × stressor; per-subject accuracy as primary measured variable |
| **Statistical Models** | §7 | LMM `accuracy ~ rep × stressor + (1|subject) + (1|dataset)`; per-H BEST + Cohen's d |
| **Transformations** | §7 (sub-section) | No transformations on accuracy (paired diff in [-1, 1] is approximately Gaussian) |
| **Inference Criteria** | §7 (sub-section) | BF₁₀ > 3 for H1; Cohen's d > 0.2 for H2 / H4 / H5 / H9 / H10; d > 0.3 for H6 / H7 endpoints |
| **Executable Analysis Script** | §7 (sub-section) | [[(C)-A1-Factorial-Analysis-Script]]; SHA-256 in manifest |
| **Data Exclusion** | §7 (sub-section) | Varbu et al. (2024) per-subject exclusion list; no post-hoc exclusions |
| **Missing Data** | §7 (sub-section) | Listwise deletion at the (subject × condition × fold) cell level |
| **Exploratory Analysis** | §7 (sub-section) | Explicitly labelled as exploratory; not used to revise H1–H10 |
| **Other / Software Environment** | §8 + [[(C)-Master-Environment]] | Master `environment.yml` + 10 per-script subset YAMLs |
| **Hardware** | §8 (sub-section) | CPU-only; ~30 h for full Phase A-1 + ~24 h for Phase A-7 simulation |
| **Reproducibility Commitment** | §8 (sub-section) | All code MIT; spec content CC-BY-4.0; CI green required before merge |
| **Conflicts of Interest** | §8 (sub-section) | None declared |
| **Acknowledgements** | §8 (sub-section) | Topos Institute (St Clere Smithe categorical lead via OQ 11.42, 11.43, 11.117, 11.120 mapping); MOABB benchmark team for the published reference values that enabled the May 2026 baseline correction |

All seven amendments (§9–§13 of the pre-reg + the §2 alternative-identity addendum) are pasted into the OSF "Amendments" field as the chronological list. The post-DOI manifest (§4 below) is uploaded as `manifest_A1.json`.

---

## §4 Post-DOI Manifest Fields — `manifest_A1.json`

Single JSON file at the repository root, produced at OSF DOI issuance and updated only as recorded OSF registration updates. One field per line for readability:

```json
{
  "schema_version":                 "phase_a1_manifest_v1",
  "osf_doi":                        "10.17605/OSF.IO/<DOI>",
  "registration_timestamp_utc":     "<ISO 8601>",
  "git_commit_at_registration":     "<HEAD SHA at pre-registration-locked tag>",
  "git_tag":                        "pre-registration-locked",
  "master_seed":                    42,
  "master_env_yml_sha256":          "<SHA-256 of environment.yml>",
  "pandas_reconciliation_log":      "A-0 originally pinned pandas 2.1; master pins 2.2; changelog-verified safe for A-0 operations.",

  "a0_script_sha256":               "<SHA-256 of a0_preflight.py>",
  "r_fm_script_sha256":             "<SHA-256 of rfm_features.py>",
  "r_jepa_script_sha256":           "<SHA-256 of rjepa_features.py>",
  "r_jepa_brain_script_sha256":     "<SHA-256 of rjepa_brain_features.py>",
  "r_gl_script_sha256":             "<SHA-256 of rgl_features.py>",
  "a1_analysis_script_sha256":      "<SHA-256 of analyse_a1_factorial.py>",
  "a1_synthetic_script_sha256":     "<SHA-256 of synth_a1.py>",
  "phase_b1_script_sha256":         "<SHA-256 of phase_b1_simulator.py>",
  "phase_a7_script_sha256":         "<SHA-256 of phase_a7_acp_twin.py>",
  "phase_a7_ensemble_script_sha256":"<SHA-256 of phase_a7_ensemble.py>",
  "phase_b2_extension_sha256":      "<SHA-256 of phase_b2_stage3.py>",

  "shared_graph_topology_sha256":   "<SHA-256 of R_GL/Phase-A-7 shared edge-list>",
  "lcm_checkpoint_md5":             "<MD5 of LCM at first download>",
  "eegformer_checkpoint_md5":       "<MD5 of EEGFormer at first download>",

  "smoke_all_pass_sha256":          "<SHA-256 of results.json>",
  "smoke_h1_fail_sha256":           "<SHA-256 of results.json>",
  "smoke_h2_fail_sha256":           "<SHA-256 of results.json>",
  "smoke_h3_fail_sha256":           "<SHA-256 of results.json>",
  "smoke_h4_fail_sha256":           "<SHA-256 of results.json>",

  "gate_threshold_physionet":       0.633,
  "gate_threshold_bci_iv_2a":       0.68,
  "moabb_published_physionet":      0.6728,
  "moabb_published_bci_iv_2a":      0.7197,
  "moabb_baseline_correction_log":  "v2.0-draft errata of May 2026: original 92% / 78% gate values were row-confusions with PhysionetMI right-hand-vs-feet (93.15%) and were corrected to the verified MOABB-published TS+LR values 67.28% / 71.97% before OSF lock. See §3 of (C)-Phase-A-Experiment-Revised.md for the full errata note.",

  "phase_a_zero_paper_check_doc":   "docs/(C)-16-Seely-Equivalence-Independent-Derivation.md",
  "phase_a_zero_completed_utc":     "<ISO 8601 timestamp of §0 sign-off>",

  "ci_workflow_path":               ".github/workflows/preregistration-verify.yml",
  "ci_last_green_commit":           "<SHA at last passing CI green build>"
}
```

The manifest is the single document a reviewer can use to verify, end-to-end, that the OSF DOI corresponds to a specific git state, a specific environment, and a specific set of script hashes. Any deviation between the manifest and the runtime state is a registration integrity violation.

---

## §5 Cross-references

| Section | Connection |
|---|---|
| §1 of this doc | The reviewer-facing README ships in the repository root; not in the OSF supplementary |
| §2 of this doc | The OSF web "Description" field content — paste-ready |
| §3 of this doc | The OSF §1–§8 field map — paste from sections of the pre-reg |
| §4 of this doc | The `manifest_A1.json` template — fill at registration time |
| [[(C)-OSF-Preregistration-Phase-A1]] | The canonical source for all the content this pack extracts and condenses |
| [[(C)-Master-Environment]] | The master `environment.yml` and per-script subset YAMLs |
| [[(C)-16-Seely-Equivalence-Independent-Derivation]] | §0 of Phase A protocol — completion artefact |
| Appendix A of [[(C)-OSF-Preregistration-Phase-A1]] | The lock-in checklist this pack supports |
