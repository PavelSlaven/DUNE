#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved second combat tank."""

from __future__ import annotations

from pathlib import Path

import build_tank_integration as build


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "artifacts" / "tank_review_v2"

build.REVIEW = REVIEW
build.BODY_SOURCE = REVIEW / "UNIT_TANKBASE_HD4_PREVIEW.png"
build.SHADOW_SOURCE = REVIEW / "UNIT_TANKBASE_SHADOW_HD4_PREVIEW.png"
build.TOP_SOURCE = REVIEW / "UNIT_TANKTOP_HD4_PREVIEW.png"
build.BODY_MASK_SOURCE = REVIEW / "HM_UNIT_TANKBASE_HD4_PREVIEW.png"
build.TOP_MASK_SOURCE = REVIEW / "HM_UNIT_TANKTOP_HD4_PREVIEW.png"
build.OUTPUT_DIR = ROOT / "artifacts" / "tank_integration_v2" / "data"


if __name__ == "__main__":
    raise SystemExit(build.main())
