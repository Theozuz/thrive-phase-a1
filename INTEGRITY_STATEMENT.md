# Pre-Registration Integrity Statement — thrIVE Phase A-1

**Study:** Sheaf-Coherence Falsification on Motor Imagery EEG — thrIVE Phase A-1
**Dataset:** PhysioNet EEG Motor Movement/Imagery Dataset (EEGMMIDB; Schalk et al., 2004)
**Registration target:** OSF Preregistration
**Locked commit:** `728f860` (tag `v0.1.2-preregistration-lock`)
**CI verification:** GitHub Actions run 28292574335 — 4/4 gates passed (syntax, hash, smoke, discrimination matrix)

---

I, the undersigned Principal Investigator, attest to the following as of the signing date below:

### 1. No bulk data analysis for the registered hypotheses
I have **not** analysed the PhysioNet EEGMMIDB dataset for any of the confirmatory hypotheses H1–H10 prior to this registration. No per-subject, per-condition accuracy results bearing on H1–H10 have been computed on the full dataset (N = 103 subjects after the Varbu et al. 2024 exclusions of subjects 88, 89, 92, 100, 104, 106).

### 2. No PhysioNet data accessed in any form
No PhysioNet EEGMMIDB data has been accessed, downloaded for analysis, or touched in any form prior to this registration — not even a single-subject pipeline sanity check. All Phase A-0 gating is deferred entirely to the post-DOI execution phase. The pre-registration rests exclusively on synthetic-data verification of the analysis pipeline (claim 4). Zero biological data has informed any registered choice — no script, threshold, hyperparameter, or hypothesis.

### 3. Analysis scripts locked before any data contact
All thirteen locked Python scripts (`a0_preflight.py`, `rfm_features.py`, `rjepa_features.py`, `rjepa_brain_features.py`, `rgl_features.py`, `analyse_a1_factorial.py`, `analyse_a7_factorial.py`, `analyse_b2_h8.py`, `synth_a1.py`, `phase_b1_simulator.py`, `phase_a7_acp_twin.py`, `phase_a7_ensemble.py`, `phase_b2_stage3.py`), together with `environment.yml` and `expected_discrimination_matrix.json`, were finalised and their SHA-256 hashes registered (`registered_hashes.json`, 15 entries) before any analysis was run. CI run 28292574335 verified all 15 hashes match at the locked commit `728f860`.

### 4. Analysis pipeline verified only on synthetic data
The H1–H10 analysis logic has been verified exclusively against synthetic data produced by the locked generator (`synth_a1.py`) across the discrimination scenarios. The 8/8 synthetic-scenario discrimination matrix passed in CI. No real EEG data was used to develop, tune, or verify the analysis pipeline.

### 5. Foundation-model selection discipline
No EEG foundation-model checkpoint (LCM or EEGFormer) has been downloaded, hashed, or selected on the basis of which produces better results. The model-selection contingency is locked in the registered `rfm_features.py` specification: LCM primary, EEGFormer fallback, no third substitution. Checkpoint MD5 hashes will be computed after the DOI is issued.

### 6. No optional stopping or peeking
Sample size is fixed at N = 103 before data acquisition. The only data-dependent stopping rules are the two pre-registered halt criteria (Phase A-0 gate failure; H1 BF₁₀ ≤ 3). No interim analyses have been or will be performed that could inform a stopping decision.

### 7. Prior knowledge disclosure
I disclose prior knowledge of the approximate Riemannian baseline (~67% binary L/R MI, MOABB benchmark, Chevallier et al. 2024), reflected only in the Phase A-0 gate threshold (≥ 0.633) and not biasing the H1–H10 contrasts.

### 8. Commitment to publish the surviving result
I commit to publishing the surviving architectural identity regardless of outcome cluster — including the no-sheaf, IVE-only-sheaf, graph-Laplacian-spectral, domain-specific-JEPA, mainstream-ensemble, or fundamental-halt fall-backs. This pre-registration is designed to falsify the thrIVE architecture's load-bearing claims if they are wrong.

---

**Principal Investigator:** Theodore Zuzarte
**Signature:** Theodore Zuzarte
**Date (UTC):** 2028-06-26
**ORCID:** 0009-0004-2404-6019