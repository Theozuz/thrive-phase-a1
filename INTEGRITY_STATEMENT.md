# Pre-Registration Integrity Statement — thrIVE Phase A-1

**Study:** Sheaf-Coherence Falsification on Motor Imagery EEG — thrIVE Phase A-1
**Dataset:** PhysioNet EEG Motor Movement/Imagery Dataset (EEGMMIDB; Schalk et al., 2004)
**Registration target:** OSF Preregistration
**Locked commit:** `1cacb64` (tag `v0.1.4-preregistration-lock`)
**CI verification:** GitHub Actions run `28510120270` — 4/4 gates passed (syntax, hash, smoke, discrimination matrix)

---

I, the undersigned Principal Investigator, attest to the following as of the signing date below:

### 1. No bulk data analysis for the registered hypotheses
I have **not** analysed the PhysioNet EEGMMIDB dataset for any of the confirmatory hypotheses H1–H10 prior to this registration. No per-subject, per-condition accuracy results bearing on H1–H10 have been computed on the full dataset (N = 103 subjects after the Varbu et al. 2024 exclusions of subjects 88, 89, 92, 100, 104, 106).

### 2. No PhysioNet data accessed in any form
No PhysioNet EEGMMIDB data has been accessed, downloaded for analysis, or touched in any form prior to this registration — **not even a single-subject pipeline sanity check**. All Phase A-0 gating is deferred entirely to the post-DOI execution phase. The pre-registration rests exclusively on synthetic-data verification of the analysis pipeline (claim 4). Zero biological data has informed any registered choice — no script, threshold, hyperparameter, or hypothesis.

### 3. Analysis scripts locked before any data contact
All thirteen locked Python scripts (`a0_preflight.py`, `rfm_features.py`, `rjepa_features.py`, `rjepa_brain_features.py`, `rgl_features.py`, `analyse_a1_factorial.py`, `analyse_a7_factorial.py`, `analyse_b2_h8.py`, `synth_a1.py`, `phase_b1_simulator.py`, `phase_a7_acp_twin.py`, `phase_a7_ensemble.py`, `phase_b2_stage3.py`), together with `environment.yml`, `expected_discrimination_matrix.json`, and the locked 32-channel montage definition `montage_a1_32ch.json`, were finalised and their SHA-256 hashes registered (`registered_hashes.json`, **16 entries**) before any analysis was run. The CI workflow (GitHub Actions run `28510120270`) verified all 16 hashes match at the locked commit `1cacb64`.

### 4. Analysis pipeline verified only on synthetic data
The H1–H10 analysis logic (`analyse_a1_factorial.py`) has been verified **exclusively against synthetic data** produced by the locked generator (`synth_a1.py`) across the discrimination scenarios (`all_pass`, `h1_fail`, `h2_fail`, `h3_fail`, `h4_fail`, and the additional `h5/h9/h10` fail scenarios). The 8/8 synthetic-scenario discrimination matrix passed in CI. No real EEG data was used to develop, tune, or verify the analysis pipeline.

### 5. Foundation-model selection discipline (§9.3)
No EEG foundation-model checkpoint (LCM or EEGFormer) has been downloaded, hashed, or selected on the basis of which produces better results. The model-selection contingency is locked in the registered `rfm_features.py` specification: LCM primary, EEGFormer fallback, no third substitution. The actual checkpoint MD5 hashes will be computed **after** the DOI is issued and recorded as `lcm_checkpoint_md5` / `eegformer_checkpoint_md5` in the manifest at that time.

### 6. No optional stopping or peeking
The sample size is fixed at N = 103 before data acquisition. There is no data-dependent stopping rule other than the two pre-registered halt criteria (Phase A-0 gate failure; H1 BF₁₀ ≤ 3). No interim analyses have been or will be performed that could inform a stopping decision.

### 7. Prior knowledge disclosure
I disclose that I have prior knowledge of the approximate Riemannian-baseline accuracy on this dataset (~67% binary left/right motor imagery, from the published MOABB benchmark, Chevallier et al. 2024). This knowledge is reflected only in the Phase A-0 preflight gate threshold (≥ 0.633, set 4 percentage points below the MOABB-published 67.28%) and does **not** bias the H1–H10 contrasts, which compare representations against each other within the same dataset.

### 8. Commitment to publish the surviving result
I commit to publishing the surviving architectural identity regardless of which outcome cluster the data supports — including the no-sheaf, IVE-only-sheaf, graph-Laplacian-spectral, domain-specific-JEPA, mainstream-ensemble, or fundamental-halt fall-back identities specified in §2 of the pre-registration. This pre-registration is designed to falsify the thrIVE architecture's load-bearing claims if they are wrong.

---

**Principal Investigator:** Theodore Zuzarte
**Signature:** Theodore Zuzarte
**Date (UTC):** 2026-07-01
**ORCID:** 0009-0004-2404-6019
