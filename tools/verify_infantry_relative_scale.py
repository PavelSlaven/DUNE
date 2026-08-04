#!/usr/bin/env python3
"""Regression check for single-vs-squad infantry visual scale."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def logical_height(manifest_path: Path) -> int:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return int(manifest["validation"]["individual_height_logical"])


def main() -> int:
    single = logical_height(
        ROOT / "artifacts" / "soldier_review_v1" / "manifest.json"
    )
    squad_member = logical_height(
        ROOT / "artifacts" / "soldiers_review_v1" / "manifest.json"
    )
    print(
        f"single_soldier_height={single}; "
        f"squad_member_height={squad_member}"
    )
    if single >= squad_member:
        print(
            "single soldier must be visually smaller than a squad member",
            file=sys.stderr,
        )
        return 1
    print("Infantry relative scale is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
