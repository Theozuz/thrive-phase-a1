#!/usr/bin/env python3
"""CI hash gate — verify each locked script's SHA-256 matches registered_hashes.json.

Returns exit code 0 if all hashes match, non-zero otherwise. Used by the
preregistration-verify.yml GitHub Actions workflow.

Usage:
    python scripts/verify_script_hashes.py registered_hashes.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    """Content-only SHA-256: normalises line endings to LF before hashing.

    This makes the hash deterministic across platforms (Windows CRLF vs
    Unix LF). The hash is still tamper-detection for the file's logical
    content; the only thing it intentionally ignores is line-ending
    encoding, which has no semantic effect on Python / YAML / JSON.
    """
    raw = path.read_bytes()
    normalised = raw.replace(b"\r\n", b"\n")
    return hashlib.sha256(normalised).hexdigest()


def main(manifest_path: str) -> int:
    manifest = json.loads(Path(manifest_path).read_text())
    failures: list[str] = []
    for filename, expected_hash in manifest.items():
        if not expected_hash or expected_hash.startswith("<"):
            # Placeholder — skip for pre-lock state
            print(f"SKIP  {filename} (placeholder)")
            continue
        actual_hash = sha256_file(Path(filename))
        if actual_hash != expected_hash:
            failures.append(
                f"FAIL  {filename}\n"
                f"      expected: {expected_hash}\n"
                f"      actual:   {actual_hash}"
            )
        else:
            print(f"OK    {filename}  {actual_hash[:16]}...")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        print(f"\n{len(failures)} hash mismatch(es)", file=sys.stderr)
        return 1
    print(f"\nAll registered hashes verified.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
