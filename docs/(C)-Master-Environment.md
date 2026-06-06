# Master `environment.yml` — Phase A-1 Locked-Artefact Superset

> **Status:** Drafted May 2026 to close **S2** of the [[(C)-OSF-Preregistration-Phase-A1]] Appendix-A lock-in punch list. Consolidates the per-script dependency blocks from the 10 locked artefacts that ship Python environments (CI workflow and synthetic smoke-test generator have no per-script env beyond the master) into a single `environment.yml` for the repository root. Per-script subset YAMLs remain in each locked-artefact doc for partial environments.

> **Companion reading:** the per-script environment blocks listed in §3 below; the OSF Appendix-A lock-in checklist of [[(C)-OSF-Preregistration-Phase-A1]] item 7.

---

## §1 Master `environment.yml` — copy to repository root

```yaml
name: thrive_phase_a1
channels:
  - pytorch
  - conda-forge
dependencies:
  # Core scientific Python stack — required by every locked artefact
  - python=3.11
  - numpy=1.26
  - scipy=1.11

  # ML / classification — required by R_FM, R_JEPA, R_JEPA_brain, R_GL,
  #                       A-0 preflight, A-1 analysis, A-7 ensemble
  - scikit-learn=1.3

  # Data handling — required by A-0 preflight and A-1 analysis
  - pandas=2.2

  # EEG / BCI domain — required by A-0 preflight
  - mne=1.6

  # Statistics — required by A-1 analysis (BEST + Bayes factor + rmANOVA)
  - pingouin=0.5

  # Deep learning — required by R_FM, R_JEPA, R_JEPA_brain, A-7 ensemble
  - pytorch=2.1
  - cpuonly        # GPU optional throughout the locked-artefact set;
                   # smoke tests + 109-subject Phase A-1 fit on CPU
                   # in hours per fold. Swap for `pytorch-cuda=12.1`
                   # under conda-forge if GPU available.

  # Build tooling
  - pip

  # Pip-only packages — MOABB + pyriemann are not on conda-forge
  - pip:
      - moabb>=1.4.0
      - pyriemann>=0.5

      # Foundation-model package for R_FM extraction — choose ONE
      # of the two below at OSF lock time, per §9.3 of
      # (C)-OSF-Preregistration-Phase-A1. The {COMMIT_HASH} placeholder
      # MUST be replaced with the actual git rev at registration time;
      # locking the commit prevents silent post-hoc model substitution.
      - "lcm-public @ git+https://github.com/<author>/lcm@{COMMIT_HASH}"
      # - "eegformer @ git+https://github.com/<author>/eegformer@{COMMIT_HASH}"
```

That single file covers the dependency superset of all 12 locked artefacts. Activate with `conda env create -f environment.yml`, then `conda activate thrive_phase_a1`.

---

## §2 Version reconciliation log

One version mismatch surfaced during consolidation:

| Package | A-0 preflight pin | A-1 analysis pin | Master pin | Rationale |
|---|---|---|---|---|
| `pandas` | `2.1` | `2.2` | **`2.2`** | The newer minor release is API-compatible with `2.1` for the columns / operations used by either script (`groupby`, `merge`, `to_dict`, basic DataFrame I/O). Pinning to `2.2` brings A-0 forward; no functional change required to the A-0 script |

Cross-checked against the pandas 2.x changelog: between 2.1 and 2.2 there are no breaking changes affecting the operations the locked scripts use. Move is safe.

All other package versions are identical across the per-script YAMLs. No further reconciliation needed.

---

## §3 Per-script dependency map — what each locked artefact actually needs

The master env is a superset; each individual locked script needs only a subset. The per-script YAMLs already shipped in each locked-artefact doc remain valid as partial environments for selective execution (e.g., running A-0 only on a minimal CI runner without PyTorch).

| Locked artefact | Per-script env name | Subset packages beyond core (python+numpy+scipy) | Per-script YAML location |
|---|---|---|---|
| [[(C)-A0-Preflight-Reference-Pipeline]] | `thrive_a0` | `scikit-learn`, `pandas=2.1` (→ 2.2 in master), `mne`, pip: `moabb`, `pyriemann` | §Companion file in script doc |
| [[(C)-R_FM-Feature-Extraction]] | `thrive_rfm` | `scikit-learn`, `pytorch+cpuonly`, pip: foundation model | §Companion file in script doc |
| [[(C)-R_JEPA-Feature-Extraction]] | `thrive_rjepa` | `scikit-learn`, `pytorch+cpuonly` | §Companion file in script doc |
| [[(C)-R_JEPA-Brain-Feature-Extraction]] | `thrive_rjepa_brain` | `scikit-learn`, `pytorch+cpuonly` | §Companion file in script doc |
| [[(C)-R_GL-Feature-Extraction]] | `thrive_rgl` | `scikit-learn` | §Companion file in script doc |
| [[(C)-A1-Factorial-Analysis-Script]] | `thrive_analysis` | `pandas=2.2`, `pingouin` | §Companion file in script doc |
| [[(C)-A1-Synthetic-Smoke-Test-Generator]] | (no separate env) | core only | uses master |
| [[(C)-CI-Workflow-Preregistration-Verify]] | (GitHub Actions, no conda env) | — | YAML in `.github/workflows/` |
| [[(C)-Phase-B1-Harmonic-Simulator]] | `thrive_b1` | core only | §Companion file in script doc |
| [[(C)-Phase-A7-Digital-ACP-Twin]] | `thrive_a7` | core only | §Companion file in script doc |
| [[(C)-Phase-A7-Mainstream-Ensemble-Baseline]] | `thrive_a7_ensemble` | `scikit-learn`, `pytorch+cpuonly` | §Companion file in script doc |
| [[(C)-Phase-B2-Stage3-Component-Validation]] | `thrive_b2` | core only | §Companion file in script doc |

The CI workflow runs the smoke tests across the locked-script set under the **master env** — that's the integration test. Per-script envs are kept available so partial environments can be reproduced on minimal CI runners if a future reviewer wants to verify a specific script in isolation.

---

## §4 What goes into the OSF manifest

| Field | Value |
|---|---|
| `master_env_yml_sha256` | SHA-256 of the master `environment.yml` after the `{COMMIT_HASH}` placeholders are replaced at registration |
| `master_env_yml_filename` | `environment.yml` (repository root) |
| `per_script_env_filenames` | `environment_a0.yml`, `environment_rfm.yml`, …, `environment_b2.yml` — one per locked artefact except CI workflow + synthetic smoke-test |
| `pandas_reconciliation_log` | "A-0 originally specified pandas 2.1; master pins 2.2; cross-checked changelog and confirmed no breaking changes for A-0 operations. Logged here to document the reconciliation." |

The `master_env_yml_sha256` is the single hash that proves the master environment at OSF lock matches the environment used at A-0 / A-1 / A-7 execution time. Any deviation between the OSF-registered hash and the runtime env file is a registration integrity violation.

---

## §5 What this does NOT change

To prevent scope creep, this consolidation **does not** modify any of the following:

- Per-script SHA-256 hashes of the locked scripts themselves (unchanged)
- Per-script smoke-test JSON outputs (unchanged)
- The `pre-registration-locked` git tag (unchanged — the master `environment.yml` lives at repository root and is included in the same tag)
- The CI workflow gates (still hash + smoke-test execution + discrimination matrix)
- The pin choices in the per-script YAMLs already shipped in each locked-artefact doc, except for the pandas 2.1 → 2.2 promotion in A-0 documented in §2

The master env is **additive** infrastructure on top of the existing locked-artefact set, not a modification of it.

---

## §6 Cross-references

| Section | Connection |
|---|---|
| Appendix A item 7 of [[(C)-OSF-Preregistration-Phase-A1]] | The lock-in checklist item this document closes |
| Per-script `environment_<script>.yml` files | Listed in §3 above; remain valid as partial environments |
| [[(C)-CI-Workflow-Preregistration-Verify]] | The CI workflow runs the smoke tests under the master env |
| §9.9 of [[(C)-OSF-Preregistration-Phase-A1]] | Pre-registration integrity statement — extended implicitly to cover the master env reconciliation |
