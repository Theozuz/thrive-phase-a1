# thrIVE Phase A-1 — Pre-Registered Sheaf-Coherence Falsification Test

[![Licence](https://img.shields.io/badge/licence-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-pre--OSF--lock-yellow)]()

**What this is.** A pre-registered factorial test of whether unsupervised
Two-Timescale Stochastic Approximation (TTSA) learning on the predictive-coding
energy of a cellular sheaf produces motor-imagery-discriminative coherence on
real EEG. Six baselines, ten confirmatory hypotheses (H1–H10), five
amendments, six pre-committed alternative-architectural-identity outcome
paths, all locked at OSF before any data is touched.

**Headline.** Either thrIVE's sheaf / IVE / dynamical architectural
commitments earn their complexity against the field's strongest baselines, or
one of the six pre-committed fall-back identities (no-sheaf, IVE-only-sheaf,
graph-Laplacian-spectral, domain-specific-JEPA, mainstream-ensemble,
fundamental-halt) is the architecture the data actually supports. The PI
commits to publishing the surviving identity regardless of which outcome
cluster occurs.

---

## Status — what's here now

This repository was assembled from the canonical Markdown specifications in
the parent vault on **2026-06-04**. All 11 locked-artefact Python scripts
were extracted via `scripts/extract_python.py` and confirmed to compile
cleanly with `python -m py_compile`.

| Item | Status |
|---|---|
| **All 13 locked-artefact scripts extracted** (11 + new A-7 / B-2 analysers) | ✅ |
| All 13 scripts compile (`py_compile`) | ✅ |
| `environment.yml` master conda env | ✅ |
| A-0 smoke test execution-verified | ✅ |
| **8-scenario discrimination matrix verified end-to-end (8/8)** | ✅ |
| A-7 H6/H7 verdict analyser smoke-test passed | ✅ |
| B-2 H8 verdict analyser smoke-test passed | ✅ |
| Conda env created | ✅ (run `conda env create -f environment.yml`) |
| SHA-256 hashes computed | ✅ (run `bash scripts/compute_hashes.sh`) |
| CI workflow on GitHub Actions | ⏳ (push to GitHub first) |
| OSF DOI | ⏳ |
| Phase A-7 full simulation | ⏳ |

---

## 30-second tour

| You want to | Open / run |
|---|---|
| Read the full pre-registration | `docs/(C)-OSF-Preregistration-Phase-A1.md` |
| Read the experimental design | `docs/(C)-Phase-A-Experiment-Revised.md` |
| Read the engineering execution sequence | `docs/(C)-OSF-Engineering-Runbook.md` |
| Verify all 11 scripts compile | `python -m py_compile *.py` |
| Run all synthetic smoke tests | `bash scripts/run_smoke_tests.sh` |
| Run the A-0 preflight smoke test | `python a0_preflight.py --smoke-test --output results/smoke/a0_smoke.json` |
| Run the A-0 single-subject sanity (touches MOABB cache for PhysionetMI subject 1) | `python a0_preflight.py --dataset physionet --single-subject 1 --output results/smoke/a0_physionet_subject1.json` |
| Verify the 5-scenario discrimination matrix | `bash scripts/verify_discrimination.sh` |
| Compute SHA-256s for the OSF manifest | `bash scripts/compute_hashes.sh` |

---

## Setup (Windows / macOS / Linux)

```bash
# 1. Install miniconda or mambaforge if not already installed.
# 2. Create the master env:
conda env create -f environment.yml
conda activate thrive_phase_a1

# 3. Verify everything is wired up:
python -c "import numpy, scipy, sklearn, pandas, mne, pingouin, torch; \
           import moabb, pyriemann; print('all imports OK')"

# 4. Smoke-test the architecture (no PhysioNet data touched):
bash scripts/run_smoke_tests.sh
```

On Windows, prefer **Miniforge3** over Anaconda for the conda channel
defaults to match `environment.yml`.

---

## Repository structure

```
.
├── README.md                              # this file
├── LICENSE
├── environment.yml                        # master conda env
├── a0_preflight.py                        # the load-bearing gate
├── rfm_features.py                        # R_FM (foundation-model baseline)
├── rjepa_features.py                      # R_JEPA (cross-domain JEPA)
├── rjepa_brain_features.py                # R_JEPA_brain (domain-specific JEPA)
├── rgl_features.py                        # R_GL (graph-Laplacian cohomology-isolation)
├── analyse_a1_factorial.py                # H1, H2, H3, H4, H5, H9, H10 verdicts
├── analyse_a7_factorial.py                # H6, H7 verdicts (Phase A-7 twin + ensemble + LeWM)
├── analyse_b2_h8.py                       # H8 triple verdict (optional, Phase B-2)
├── synth_a1.py                            # synthetic-scenario generator (8 scenarios x 13 reps)
├── phase_b1_simulator.py                  # THINK-mode harmonic preservation
├── phase_a7_acp_twin.py                   # dynamical-architecture twin (telemetry source)
├── phase_a7_ensemble.py                   # BCI mainstream ensemble baseline (telemetry source)
├── phase_b2_stage3.py                     # Stage-3 component validation (optional, telemetry source)
├── scripts/
│   ├── extract_python.py                  # extract Python from (C) specs
│   ├── verify_script_hashes.py            # CI hash gate
│   ├── verify_discrimination_matrix.py    # CI discrimination-matrix gate
│   ├── compute_hashes.sh                  # one-shot hash computation
│   ├── run_smoke_tests.sh                 # one-shot smoke-test driver
│   └── verify_discrimination.sh           # one-shot 5-scenario verifier
├── docs/                                  # OSF supplementary materials (Markdown specs)
├── results/
│   ├── raw/                               # per-script per-subject outputs
│   └── smoke/                             # synthetic-scenario outputs
├── registered_hashes.json                 # SHA-256s at OSF lock time
├── expected_discrimination_matrix.json    # truth table for H1–H10 on synth
├── manifest_A1.json                       # OSF manifest (DOI, hashes, run state)
└── .github/
    └── workflows/
        └── preregistration-verify.yml     # CI workflow
```

---

## What this repository can do *right now*

Even before the conda env is created, you can:

```bash
# Confirm all 11 scripts are syntactically valid:
python -m py_compile *.py && echo "all 11 compile"
```

After `conda env create -f environment.yml`:

```bash
# Synthetic smoke tests (no PhysioNet, no GPU, runs in minutes):
bash scripts/run_smoke_tests.sh

# Single-subject A-0 sanity on real PhysioNetMI data (~3 min):
python a0_preflight.py --dataset physionet --single-subject 1 \
       --output results/smoke/a0_physionet_subject1.json
```

If the single-subject sanity returns `grand_average` in the 0.55–0.85 range,
the MOABB pipeline is operationally validated for the one subject and the
architecture is **execution-ready for the Scope-A milestone** (synthetic
smoke tests + single-subject sanity).

---

## What this repository cannot yet do

| | Why |
|---|---|
| Full Phase A-1 H1–H10 on PhysioNetMI | Pre-OSF-lock per §9.9 integrity statement; gated on OSF DOI |
| Phase A-7 ACP twin full run | ~24 hours compute; run after OSF lock |
| Real-time online inference | Specified for Phase B FPGA prototype (months out) |
| Stage 2 prosthetic deployment | Gated on Phase A-1 H1 passing + Phase B hardware |

---

## License

Code: MIT. Specifications (the `docs/` Markdown files): CC-BY-4.0.

---

## Citation

If you use this pre-registration, please cite (DOI to be filled at OSF
registration time):

```bibtex
@misc{cognat_thrive_phase_a1_2026,
  author       = {Cognat, Theo},
  title        = {{thrIVE Phase A-1: Sheaf-Coherence Falsification on Motor Imagery EEG}},
  year         = {2026},
  doi          = {10.17605/OSF.IO/<DOI>},
  note         = {Pre-registration with five amendments and an
                  alternative-architectural-identity outcome framework}
}
```
