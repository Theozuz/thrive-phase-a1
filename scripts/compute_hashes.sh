#!/usr/bin/env bash
# Compute SHA-256 for each locked artefact + master env.
# Writes a manifest-shaped JSON to registered_hashes.json.
set -euo pipefail

python <<'PY'
import hashlib, json
from pathlib import Path

LOCKED = [
    "a0_preflight.py",
    "rfm_features.py",
    "rjepa_features.py",
    "rjepa_brain_features.py",
    "rgl_features.py",
    "analyse_a1_factorial.py",
    "analyse_a7_factorial.py",
    "analyse_b2_h8.py",
    "synth_a1.py",
    "phase_b1_simulator.py",
    "phase_a7_acp_twin.py",
    "phase_a7_ensemble.py",
    "phase_b2_stage3.py",
    "environment.yml",
    "expected_discrimination_matrix.json",
]

manifest = {}
for fn in LOCKED:
    p = Path(fn)
    if not p.exists():
        print(f"WARN: missing {fn}")
        manifest[fn] = ""
        continue
    # Content-only hash: normalise line endings so the hash is deterministic
    # across Windows (CRLF) and Unix (LF). Must match verify_script_hashes.py.
    raw = p.read_bytes()
    normalised = raw.replace(b"\r\n", b"\n")
    h = hashlib.sha256(normalised).hexdigest()
    manifest[fn] = h
    print(f"{h}  {fn}")

Path("registered_hashes.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
print()
print(f"Wrote registered_hashes.json with {len(manifest)} entries.")
PY
