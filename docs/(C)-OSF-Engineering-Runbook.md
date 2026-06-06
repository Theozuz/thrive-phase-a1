# OSF Lock-in Engineering Runbook — Phase A-1

> **Status:** Drafted May 2026. This document is the **practical execution sequence** that takes the spec-complete vault state to a registered OSF DOI. Every spec-tier dependency has been cleared (per the dry-run of [[(C)-OSF-Preregistration-Phase-A1]] Appendix A — see the punch-list summary I produced earlier in the audit run). What remains is git tagging, SHA-256 computation, smoke-test execution, CI green verification, OSF web actions, and DOI recording. This runbook orders those steps so you do not re-derive the dependency graph each time you sit down.

> **Total time budget:** ~30 hours of focused engineering + ~24 hours of asynchronous Phase A-7 simulation compute + ~1 hour of OSF web actions + ~1 hour of post-DOI verification = **~3 working days** if executed sequentially without context-switching.

> **Reading order:** §1 prerequisites → §2–§11 sequential steps. Each step has a "what to do", a "verification criterion", and a "what to do if it fails" sub-block. Do not skip ahead — later steps assume earlier ones have passed.

---

## §1 Prerequisites — confirm before starting

Run through this list in one sitting. If any item is `[ ]`, address it before proceeding.

- [ ] **§0 Seely paper-check completed** — [[../02-Theory/(C)-16-Seely-Equivalence-Independent-Derivation]] is in the vault. Cross-check item 10 of Appendix A of [[(C)-OSF-Preregistration-Phase-A1]] is `[x]`.
- [ ] **MOABB baseline cross-check completed** — §3 of [[(C)-Phase-A-Experiment-Revised]] uses corrected gates (≥0.633 / ≥0.68). Cross-check item is marked `[x]` in Appendix A.
- [ ] **Master `environment.yml` content drafted** — [[(C)-Master-Environment]] §1 is the source. Appendix-A item 7 is referenced.
- [ ] **OSF Submission Pack drafted** — [[(C)-OSF-Submission-Pack]] §1 (README) and §2 (cover) and §4 (manifest template) are in the vault.
- [ ] **GitHub account ready** — username + 2FA enabled; recommended: `gh` CLI installed and authenticated.
- [ ] **OSF account ready** — email + ORCID linked.
- [ ] **Local working directory** — a clean directory outside the Obsidian vault. The Obsidian vault is the *specification source*; the GitHub repo is the *execution target*. Keep them separate.

If all six are checked, proceed to §2.

---

## §2 Repository scaffold (≈ 30 min)

### §2.1 Create the directory structure

Locally, in your chosen working directory:

```bash
mkdir -p thrive-phase-a1
cd thrive-phase-a1
git init
mkdir -p scripts docs results/{raw,smoke} .github/workflows
```

### §2.2 Copy the supplementary docs into `docs/`

The Markdown specifications that ship with the OSF submission live under `docs/`. From the Obsidian vault root (treat the vault as read-only for this step — never edit specs through the repository):

```bash
VAULT="/path/to/Obsidian/vault/thrIVE"
cp "$VAULT/Phase A Experiment/(C)-OSF-Preregistration-Phase-A1.md" docs/
cp "$VAULT/Phase A Experiment/(C)-Phase-A-Experiment-Revised.md"   docs/
cp "$VAULT/Phase A Experiment/(C)-Master-Environment.md"            docs/
cp "$VAULT/Phase A Experiment/(C)-OSF-Submission-Pack.md"           docs/
cp "$VAULT/12-Research/(C)-A0-Preflight-Reference-Pipeline.md"      docs/
cp "$VAULT/02-Theory/(C)-16-Seely-Equivalence-Independent-Derivation.md" docs/
cp "$VAULT/11-Integration-Future/(C)-09-Stage-Dependency-Trace-Post-MOABB-Correction.md" docs/
cp "$VAULT/11-Integration-Future/(C)-10-Quality-Weighted-Federation-Spec.md" docs/
```

That's the eight specifications a reviewer needs. Locked-artefact specs (one per script) are also worth copying to `docs/` for transparency.

### §2.3 Verification

```bash
ls docs/
# Should show 8 .md files (or 8 + the locked-artefact specs)
```

### §2.4 If it fails

If a file is missing from the vault, return to spec work — do not proceed with a missing supplementary. The vault is the source of truth.

---

## §3 Extract Python from the (C) script specifications (≈ 4–6 hours)

Each locked-artefact `(C)-*.md` spec contains the Python source inside fenced code blocks. The engineering step is **extract each into its own .py file at the repository root**, preserving the content verbatim.

### §3.1 The 11 scripts to extract

| Source spec (vault path) | Target file (repo root) |
|---|---|
| `12-Research/(C)-A0-Preflight-Reference-Pipeline.md` | `a0_preflight.py` |
| `Phase A Experiment/(C)-R_FM-Feature-Extraction.md` | `rfm_features.py` |
| `Phase A Experiment/(C)-R_JEPA-Feature-Extraction.md` | `rjepa_features.py` |
| `Phase A Experiment/(C)-R_JEPA-Brain-Feature-Extraction.md` | `rjepa_brain_features.py` |
| `Phase A Experiment/(C)-R_GL-Feature-Extraction.md` | `rgl_features.py` |
| `Phase A Experiment/(C)-A1-Factorial-Analysis-Script.md` | `analyse_a1_factorial.py` |
| `Phase A Experiment/(C)-A1-Synthetic-Smoke-Test-Generator.md` | `synth_a1.py` |
| `Phase A Experiment/(C)-Phase-B1-Harmonic-Simulator.md` | `phase_b1_simulator.py` |
| `Phase A Experiment/(C)-Phase-A7-Digital-ACP-Twin.md` | `phase_a7_acp_twin.py` |
| `Phase A Experiment/(C)-Phase-A7-Mainstream-Ensemble-Baseline.md` | `phase_a7_ensemble.py` |
| `Phase A Experiment/(C)-Phase-B2-Stage3-Component-Validation.md` | `phase_b2_stage3.py` |

### §3.2 Helper extraction script

Save as `scripts/extract_python.py`:

```python
"""Extract the first ```python``` block from a Markdown spec into a .py file."""
import re, sys, pathlib

def extract(md_path: str, out_path: str) -> None:
    text = pathlib.Path(md_path).read_text(encoding="utf-8")
    m = re.search(r"```python\n(.*?)\n```", text, re.DOTALL)
    if not m:
        sys.exit(f"No ```python block in {md_path}")
    pathlib.Path(out_path).write_text(m.group(1), encoding="utf-8")
    print(f"{md_path}  →  {out_path}  ({len(m.group(1))} chars)")

if __name__ == "__main__":
    extract(sys.argv[1], sys.argv[2])
```

Run for each spec → script mapping:

```bash
python scripts/extract_python.py "docs/(C)-A0-Preflight-Reference-Pipeline.md" a0_preflight.py
python scripts/extract_python.py "docs/(C)-R_FM-Feature-Extraction.md"          rfm_features.py
# ... 9 more
```

### §3.3 Verification

```bash
python -m py_compile a0_preflight.py rfm_features.py rjepa_features.py \
                     rjepa_brain_features.py rgl_features.py \
                     analyse_a1_factorial.py synth_a1.py \
                     phase_b1_simulator.py phase_a7_acp_twin.py \
                     phase_a7_ensemble.py phase_b2_stage3.py
# Should print no errors. Syntax-checks all 11 scripts.
```

### §3.4 If it fails

If `py_compile` reports a syntax error, **do not fix it in the .py file**. The error is a spec error. Return to the (C) spec in the vault, fix it there, then re-extract. The spec is the source of truth.

---

## §4 Environment files (≈ 30 min)

### §4.1 Master `environment.yml`

Copy the YAML block from [[(C)-Master-Environment]] §1 verbatim into `environment.yml` at the repository root. The block uses `{COMMIT_HASH}` placeholders for the foundation-model package; **fill these with the actual commit hashes only after the OSF Register step** (see §10.5).

### §4.2 Per-script subset YAMLs (10 files)

From each locked-artefact spec's "Companion file" section, copy the YAML into the named per-script file:

```
environment_a0.yml          environment_rfm.yml         environment_rjepa.yml
environment_rjepa_brain.yml environment_rgl.yml         environment_analysis.yml
environment_b1.yml          environment_a7.yml          environment_a7_ensemble.yml
environment_b2.yml
```

(`environment_analysis.yml` is from the A-1 factorial-analysis script; the synthetic generator and CI workflow have no separate env beyond the master.)

### §4.3 Verification

```bash
conda env create -f environment.yml
conda activate thrive_phase_a1
python -c "import numpy, scipy, sklearn, pandas, mne, pingouin, torch; import moabb, pyriemann; print('all imports OK')"
```

### §4.4 If it fails

- If a package version conflict surfaces, **do not edit the YAML to silently change a version**. Document the conflict, fix the version in the master YAML, then update the [[(C)-Master-Environment]] §2 reconciliation log to record the change.
- If `moabb>=1.4.0` is not installable, check the PyPI version listing. The 1.4 baseline is the Chevallier-et-al-2024 published benchmark version; earlier versions would invalidate the gate-threshold cross-check.

---

## §5 Smoke tests (≈ 3–4 hours)

### §5.1 The 11 per-script smoke tests

```bash
# Each runs in seconds-to-minutes on synthetic data; no PhysioNet data touched.
python a0_preflight.py            --smoke-test --output results/smoke/a0_smoke.json
python rfm_features.py            --smoke-test
python rjepa_features.py          --smoke-test
python rjepa_brain_features.py    --smoke-test
python rgl_features.py            --smoke-test
python synth_a1.py                --scenario all_pass --output results/smoke/a1_all_pass.json
python synth_a1.py                --scenario h1_fail  --output results/smoke/a1_h1_fail.json
python synth_a1.py                --scenario h2_fail  --output results/smoke/a1_h2_fail.json
python synth_a1.py                --scenario h3_fail  --output results/smoke/a1_h3_fail.json
python synth_a1.py                --scenario h4_fail  --output results/smoke/a1_h4_fail.json
python phase_b1_simulator.py      --smoke-test --n-seeds 3
python phase_a7_acp_twin.py       --smoke-test
python phase_a7_ensemble.py       --smoke-test
python phase_b2_stage3.py         --smoke-test
```

### §5.2 The 5-scenario discrimination matrix

Run the analysis script against each synthetic scenario:

```bash
python analyse_a1_factorial.py --input results/smoke/a1_all_pass.json --output results/smoke/a1_all_pass_verdict.json
python analyse_a1_factorial.py --input results/smoke/a1_h1_fail.json  --output results/smoke/a1_h1_fail_verdict.json
python analyse_a1_factorial.py --input results/smoke/a1_h2_fail.json  --output results/smoke/a1_h2_fail_verdict.json
python analyse_a1_factorial.py --input results/smoke/a1_h3_fail.json  --output results/smoke/a1_h3_fail_verdict.json
python analyse_a1_factorial.py --input results/smoke/a1_h4_fail.json  --output results/smoke/a1_h4_fail_verdict.json
```

Then verify each verdict matches the expected outcome row in `expected_discrimination_matrix.json` (which lives at the repository root and is the *truth table* for the analysis pipeline):

```bash
python scripts/verify_discrimination_matrix.py results/smoke/ expected_discrimination_matrix.json
# Should print "5/5 verdicts match expected discrimination matrix"
```

### §5.3 The A-0 single-subject sanity check (≈ 3 min on PhysioNetMI subject 1)

```bash
python a0_preflight.py --dataset physionet --single-subject 1 \
    --output results/smoke/a0_physionet_subject1.json
```

Check the JSON contains a `grand_average` field. **This is the only place during pre-lock where MOABB cache data is touched** — subject 1's data only. Verify the JSON does not contain any other subject's data.

### §5.4 Verification

```bash
ls results/smoke/
# Should show: a0_smoke.json, a0_physionet_subject1.json,
#              5 synthetic JSONs, 5 verdict JSONs,
#              phase_b1_smoke.json, phase_a7_smoke.json, etc.
```

All 11 smoke outputs + 5 verdicts + the 1 single-subject sanity = 17 JSONs.

### §5.5 If it fails

- If any smoke test errors, fix the *spec* — extract again per §3.
- If a discrimination-matrix verdict mismatches, **do not modify either the analysis script or the synthetic scenario to make them match**. The mismatch is the analysis logic disagreeing with the spec's intended outcome; investigate which side is wrong. The truth table in `expected_discrimination_matrix.json` is the locked spec; the analysis script must conform to it.

---

## §6 Compute the SHA-256 hashes (≈ 15 min)

### §6.1 Per-script hashes

```bash
sha256sum a0_preflight.py             > registered_hashes.txt
sha256sum rfm_features.py            >> registered_hashes.txt
sha256sum rjepa_features.py          >> registered_hashes.txt
sha256sum rjepa_brain_features.py    >> registered_hashes.txt
sha256sum rgl_features.py            >> registered_hashes.txt
sha256sum analyse_a1_factorial.py    >> registered_hashes.txt
sha256sum synth_a1.py                >> registered_hashes.txt
sha256sum phase_b1_simulator.py      >> registered_hashes.txt
sha256sum phase_a7_acp_twin.py       >> registered_hashes.txt
sha256sum phase_a7_ensemble.py       >> registered_hashes.txt
sha256sum phase_b2_stage3.py         >> registered_hashes.txt
sha256sum environment.yml            >> registered_hashes.txt
sha256sum expected_discrimination_matrix.json >> registered_hashes.txt
```

### §6.2 Smoke-test output hashes

```bash
sha256sum results/smoke/a1_all_pass_verdict.json >> registered_hashes.txt
sha256sum results/smoke/a1_h1_fail_verdict.json  >> registered_hashes.txt
sha256sum results/smoke/a1_h2_fail_verdict.json  >> registered_hashes.txt
sha256sum results/smoke/a1_h3_fail_verdict.json  >> registered_hashes.txt
sha256sum results/smoke/a1_h4_fail_verdict.json  >> registered_hashes.txt
```

### §6.3 R_GL ↔ Phase A-7 topology checksum cross-check

The spec requires that the 40-node 80-edge graph topology produced by `rgl_features.py:build_graph_topology()` is **bit-identical** to the same function in `phase_a7_acp_twin.py`. The cross-check helper:

```bash
python scripts/verify_topology_checksum.py rgl_features.py phase_a7_acp_twin.py \
    --output shared_graph_topology_sha256.txt
# Should print: "MATCH: SHA-256 of edge list = <hash>"
```

The output hash is logged as `shared_graph_topology_sha256` in the manifest. Any mismatch is a registration integrity violation — return to the spec, do not silently fix.

### §6.4 Convert the hash list to JSON

Transform `registered_hashes.txt` into the structured `registered_hashes.json` that the CI workflow consumes. The format is documented in [[(C)-CI-Workflow-Preregistration-Verify]] — one entry per locked artefact, keyed by manifest field name.

### §6.5 Verification

```bash
python scripts/verify_script_hashes.py registered_hashes.json
# Should print "13/13 hashes verified" (or however many entries are in the manifest)
```

### §6.6 If it fails

If a hash does not match, the script was modified after the hash was logged. Either:
- The script was modified (re-compute the hash, re-log)
- The hash was logged incorrectly (re-compute)

Do not proceed to OSF lock with a mismatch. The CI workflow gates this and will block the merge to `main`.

---

## §7 CI workflow setup (≈ 2–3 hours)

### §7.1 Extract the workflow YAML

From [[(C)-CI-Workflow-Preregistration-Verify]], extract the GitHub Actions YAML and the three helper scripts:

```bash
# Workflow file
python scripts/extract_yaml.py "docs/(C)-CI-Workflow-Preregistration-Verify.md" \
    .github/workflows/preregistration-verify.yml

# Helper scripts (also in the same spec)
python scripts/extract_python.py "docs/(C)-CI-Workflow-Preregistration-Verify.md" \
    scripts/verify_script_hashes.py
# (repeat for verify_discrimination_matrix.py if it's a separate code block)
```

### §7.2 Commit and test on a branch

```bash
git checkout -b ci-verify-test
git add .github/workflows/preregistration-verify.yml scripts/ registered_hashes.json
git commit -m "Add CI workflow + hash + discrimination-matrix verification"
git push -u origin ci-verify-test  # or `gh repo create` first if not pushed
```

Watch the CI workflow run on GitHub Actions. **All three gates must pass green:**
- Hash gate: every script's SHA-256 matches `registered_hashes.json`
- Smoke-test gate: every smoke test runs end-to-end without error
- Discrimination-matrix gate: 5/5 synthetic scenarios produce the expected verdict

### §7.3 Branch protection on `main`

In the GitHub repo Settings → Branches:

- Add a branch protection rule for `main`
- Require: "Require status checks to pass before merging"
- Required check: the CI workflow's three gates
- Enforce: "Include administrators" (so even the PI cannot push directly to main)

### §7.4 Verification

```bash
# After protection is in place, this should fail:
git push origin main
# Expected: "remote: error: GH006: Protected branch update failed for refs/heads/main."
```

Then merge the test branch:

```bash
gh pr create --base main --head ci-verify-test \
    --title "CI workflow + hashes + discrimination matrix" \
    --body "Pre-OSF-lock infrastructure"
gh pr merge --merge   # only succeeds if CI green
```

### §7.5 If it fails

- If a CI gate fails, **do not bypass the protection** to merge. The failure is the system working as designed. Fix the underlying issue.
- If the workflow YAML has a syntax error, re-extract from the (C) spec; do not hand-edit.

---

## §8 Phase A-7 simulation runs (≈ 24 hours compute, asynchronous)

This step runs in the background. Phase A-1 OSF lock-in can proceed without waiting for A-7 simulation to complete, but the A-7 JSONs are part of the supplementary materials.

```bash
# 2 × 4 × 4 = 32 conditions × 103 subjects × 5 folds = 16,480 paired observations
# ACP twin
nohup python phase_a7_acp_twin.py --full-run \
    --output results/phase_a7/twin_full.json &

# Mainstream ensemble baseline
nohup python phase_a7_ensemble.py --full-run \
    --output results/phase_a7/ensemble_full.json &
```

Both runs to be committed when complete (separate `phase-a7-locked` git tag — see §10.4).

### §8.1 Verification

```bash
# Check progress periodically:
ls -la results/phase_a7/
tail -f nohup.out
```

### §8.2 If it fails

- If a run crashes mid-way, log the failure mode + restart. The simulator is checkpointed per-condition; restart from the last successful condition.

---

## §9 PI process commitments (≈ 4 hours over 1–2 sittings)

These are PI sign-off items, not engineering. They block the OSF Register step.

- [ ] **§9.9 integrity statement signed** — the PI confirms in writing that no PhysioNetMI EEG data has been touched by any locked script beyond the §5.3 single-subject sanity check. Documented as a `INTEGRITY_STATEMENT.md` at the repository root.
- [ ] **R_JEPA_brain published-principles verification** — PI has read Yi et al. (2024) Brain-JEPA and Guetschel et al. (2024) Signal-JEPA papers; documents the principle-by-principle correspondence between published work and the locked R_JEPA_brain hyperparameters in a `RJEPA_BRAIN_VERIFICATION.md`.
- [ ] **R_JEPA_brain coord substitution** — PI has either substituted actual PhysioNet 64-channel 10-10 coordinates for the placeholder Fibonacci-sphere positional encoding, or has explicitly documented why the placeholder is retained as adequate. Document in `RJEPA_BRAIN_VERIFICATION.md`.

---

## §10 Git tagging and final repository state (≈ 30 min)

### §10.1 Commit the manifest template

Create `manifest_A1.json` at the repository root from [[(C)-OSF-Submission-Pack]] §4 template. Fill in:
- `master_seed`: 42
- All script SHA-256s from `registered_hashes.json`
- `master_env_yml_sha256`
- `shared_graph_topology_sha256`
- The 5 smoke-verdict SHA-256s
- `gate_threshold_physionet`: 0.633
- `gate_threshold_bci_iv_2a`: 0.68
- `moabb_published_physionet`: 0.6728
- `moabb_published_bci_iv_2a`: 0.7197
- `moabb_baseline_correction_log`: copy from the template
- `phase_a_zero_paper_check_doc`: "docs/(C)-16-Seely-Equivalence-Independent-Derivation.md"
- `phase_a_zero_completed_utc`: ISO-8601 timestamp

Leave the following blank — they're filled at OSF Register time:
- `osf_doi`
- `registration_timestamp_utc`
- `lcm_checkpoint_md5`, `eegformer_checkpoint_md5`

### §10.2 Commit + tag pre-registration-locked

```bash
git checkout main
git pull origin main  # latest after CI merge
git add manifest_A1.json
git commit -m "Pre-OSF-lock manifest template"
git push origin main

# Now tag:
git tag -a pre-registration-locked -m "Phase A-1 OSF pre-registration locked"
git push origin pre-registration-locked
```

### §10.3 Record `git_commit_at_registration`

```bash
git rev-parse pre-registration-locked
# Copy this SHA into manifest_A1.json field `git_commit_at_registration`
```

### §10.4 Phase A-7 separate tag (when A-7 simulation completes)

```bash
git add results/phase_a7/
git commit -m "Phase A-7 ACP twin + mainstream ensemble full runs"
git tag -a phase-a7-locked -m "Phase A-7 simulation outputs locked"
git push origin phase-a7-locked
```

### §10.5 Replace foundation-model `{COMMIT_HASH}` placeholders

In `environment.yml`, replace the `{COMMIT_HASH}` placeholders for the LCM or EEGFormer pip URL. Then re-compute the master env SHA-256 and update the manifest:

```bash
sha256sum environment.yml
# Update master_env_yml_sha256 in manifest_A1.json
git add environment.yml manifest_A1.json
git commit -m "Lock foundation-model commit hash in master env"
git push origin main
git tag -a pre-registration-locked --force -m "Phase A-1 OSF pre-registration locked (env updated)"
git push origin pre-registration-locked --force
```

(The single force-push of a tag is acceptable here because the tag has not yet been referenced from OSF — once the DOI is issued, this becomes immutable.)

### §10.6 Verification

```bash
git tag -l
# Should show: pre-registration-locked, phase-a7-locked (if A-7 complete)

gh release view pre-registration-locked
# Should show the tag at the expected commit
```

---

## §11 OSF submission (≈ 1 hour)

### §11.1 Create the OSF project

- Log in to OSF
- New project: title = §1 of [[(C)-OSF-Preregistration-Phase-A1]] (the long sheaf-coherence-falsification title)
- Set licence: MIT for code, CC-BY-4.0 for spec content
- Add public link to the GitHub repository

### §11.2 Fill in the §1–§8 fields

Use the **field map** in [[(C)-OSF-Submission-Pack]] §3. Each OSF web field corresponds to a specific section of the pre-registration document. Paste content verbatim from those sections — except for the Description field, which uses the **condensed version** in [[(C)-OSF-Submission-Pack]] §2.

### §11.3 Upload supplementaries

Upload as OSF "supplementary materials":

- `docs/(C)-OSF-Preregistration-Phase-A1.md`
- `docs/(C)-Phase-A-Experiment-Revised.md`
- `docs/(C)-16-Seely-Equivalence-Independent-Derivation.md`
- `docs/(C)-A0-Preflight-Reference-Pipeline.md`
- `docs/(C)-Master-Environment.md`
- `docs/(C)-09-Stage-Dependency-Trace-Post-MOABB-Correction.md`
- `docs/(C)-10-Quality-Weighted-Federation-Spec.md`
- `manifest_A1.json`
- `registered_hashes.json`
- `environment.yml`
- `expected_discrimination_matrix.json`
- README screenshot or PDF rendering (optional but reviewer-friendly)

### §11.4 Final pre-Register check (the ten Cs)

Before clicking Register, confirm in order:

1. **C**heckmark on every Appendix A item that has spec backing (all should be `[x]` except items 1–3 which are OSF web actions you've just performed)
2. **C**ross-verify: `manifest_A1.json` `master_env_yml_sha256` matches the actual `environment.yml`
3. **C**ross-verify: every script's SHA-256 in `registered_hashes.json` matches its file on the `pre-registration-locked` tag
4. **C**ross-verify: discrimination matrix's 5/5 verdicts match the truth table
5. **C**ross-verify: A-0 single-subject sanity returned a valid `grand_average` field
6. **C**onfirm: CI is green on `main` at the `pre-registration-locked` commit
7. **C**onfirm: branch protection is enabled on `main`
8. **C**onfirm: no foundation-model checkpoint MD5s have been computed yet (these are post-DOI per §9.3 of the pre-registration)
9. **C**onfirm: §9.9 integrity statement signed
10. **C**onfirm: no PhysioNet bulk data analysis has been run

### §11.5 Click Register

This is the formal pre-registration commitment. After this point, modifying any spec, script, threshold, hyperparameter, or hypothesis requires a recorded OSF registration update.

### §11.6 Record the DOI

OSF will issue a DOI. Update `manifest_A1.json`:

```json
"osf_doi": "10.17605/OSF.IO/<DOI>",
"registration_timestamp_utc": "2026-..."
```

Update §0 of [[(C)-Phase-A-Experiment-Revised]] to record the DOI.

Commit + push:

```bash
git add manifest_A1.json docs/(C)-Phase-A-Experiment-Revised.md
git commit -m "Record OSF DOI"
git push origin main
git tag -a osf-doi-issued -m "OSF DOI <DOI> issued"
git push origin osf-doi-issued
```

---

## §12 Post-DOI verification (≈ 1 hour)

### §12.1 Run A-0 preflight on both datasets

```bash
python a0_preflight.py --dataset physionet --output results/a0_physionet.json \
    --manifest results/a0_physionet_manifest.json

python a0_preflight.py --dataset bci_iv_2a --output results/a0_bci_iv_2a.json \
    --manifest results/a0_bci_iv_2a_manifest.json
```

**Both must contain `"gate_passed": true`.**

### §12.2 If A-0 fails on either dataset

Per the locked failure decision tree in [[(C)-A0-Preflight-Reference-Pipeline]]:

| Symptom | Repair action |
|---|---|
| Within 4 pp of published but below gate | Inspect `per_subject` outliers; clear MOABB cache; redownload |
| 4–10 pp below published | Verify MOABB ≥ 1.4; verify Varbu et al. 2024 annotation curation is applied |
| > 10 pp below published | Re-derive pipeline from pyriemann + sklearn docs from scratch; verify OAS covariance estimator |
| > 4 pp **above** published | Suspicious — verify WithinSessionEvaluation was used; check per-fold isolation |

**Document any repair as a recorded OSF registration update before re-attempting the gate.**

### §12.3 If A-0 passes on both datasets

Proceed to Phase A-1 factorial execution. The H1–H10 confirmatory tests can begin.

---

## §13 The runbook is done

After §12.3, the OSF pre-registration is operational. Phase A-1 data collection and analysis proceed independently per [[(C)-Phase-A-Experiment-Revised]] §4 (Phase A-1) and downstream sections.

The remaining open items in the architecture are all *post-Phase-A-1* work — Stage 2 prosthetic deployment (gated on H1–H10 outcomes), Stage 3 federation deployment (gated on the [[(C)-11-Topos-Collaboration-Proposal-OQ-11-120]] result + Phase A-1 population data), and the Phase B/C hardware roadmap per [[../11-Integration-Future/03-Implementation-Roadmap]].

---

## §14 Time budget summary

| Step | Estimated time | Mode |
|---|---|---|
| §1 Prerequisites | 30 min | Pre-flight check |
| §2 Repository scaffold | 30 min | Active |
| §3 Extract Python | 4–6 hours | Active |
| §4 Environment files | 30 min | Active |
| §5 Smoke tests | 3–4 hours | Active |
| §6 SHA-256 hashes | 15 min | Active |
| §7 CI workflow setup | 2–3 hours | Active |
| §8 Phase A-7 simulation | ~24 hours | **Async background** |
| §9 PI commitments | 4 hours | PI-side |
| §10 Git tagging | 30 min | Active |
| §11 OSF submission | 1 hour | OSF web actions |
| §12 Post-DOI A-0 gate | 1 hour | Active |
| **Total active engineering** | **~21 hours** | over ~3 working days |
| **Total wall-clock** | **~3 working days** | with §8 running in parallel |

The bottleneck is §3 (Python extraction). Everything else is fast.

---

## §15 Cross-references

| Section | Connection |
|---|---|
| [[(C)-OSF-Preregistration-Phase-A1]] Appendix A | The checklist this runbook executes |
| [[(C)-OSF-Submission-Pack]] §1, §2, §3, §4 | The README, cover, field map, and manifest template this runbook uses |
| [[(C)-Master-Environment]] | The `environment.yml` content for §4 |
| [[(C)-A0-Preflight-Reference-Pipeline]] | The A-0 gate the §12 post-DOI step runs |
| [[(C)-16-Seely-Equivalence-Independent-Derivation]] | §0 pre-experimental verification — already complete, referenced from the manifest |
| [[(C)-CI-Workflow-Preregistration-Verify]] | The CI workflow this runbook extracts and deploys in §7 |
| [[../11-Integration-Future/(C)-11-Topos-Collaboration-Proposal-OQ-11-120]] | Independent track — can be sent in parallel with OSF execution |
