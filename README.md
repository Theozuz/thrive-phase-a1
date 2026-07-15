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
| 5 | `sheaf_features.py` | Graph-Laplacian-only (R_GL — cohomology-isolation test) | `python sheaf_features.py --smoke-test` |
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
@misc{zuzarte_thrive_phase_a1_2026,
  author       = {Zuzarte, Theodore},
  title        = {{thrIVE Phase A-1: Sheaf-Coherence Falsification on Motor Imagery EEG}},
  year         = {2026},
  doi          = {TBD},
  url          = {TBD},
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
├── sheaf_features.py
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
