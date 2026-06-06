#!/usr/bin/env python3
"""Extract the first ```python``` fenced block from a Markdown spec into a .py file.

This is the canonical extraction tool referenced by §3.2 of
(C)-OSF-Engineering-Runbook.md. The spec content lives in the (C)-prefixed
Markdown files in the vault; the .py files at the repository root are
*outputs* of this extraction step.

Usage:
    python scripts/extract_python.py <md_path> <out_path>

If the extracted Python fails to compile, fix the spec (the Markdown), not
the .py file. The spec is the source of truth.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def extract(md_path: str, out_path: str) -> int:
    text = Path(md_path).read_text(encoding="utf-8")
    matches = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    if not matches:
        print(f"ERROR: No ```python block in {md_path}", file=sys.stderr)
        return 1
    if len(matches) > 1:
        print(
            f"NOTE: {md_path} has {len(matches)} python blocks; "
            f"extracting the first only ({len(matches[0])} chars).",
            file=sys.stderr,
        )
    Path(out_path).write_text(matches[0], encoding="utf-8")
    print(f"OK  {md_path}  ->  {out_path}  ({len(matches[0])} chars)")
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    return extract(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    raise SystemExit(main())
