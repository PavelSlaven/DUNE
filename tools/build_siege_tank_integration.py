#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved siege tank."""

from __future__ import annotations

from pathlib import Path

import build_tank_integration as build


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "artifacts" / "siege_tank_review_v1"

build.REVIEW = REVIEW
build.BODY_SOURCE = REVIEW / "UNIT_SIEGEBASE_HD4_PREVIEW.png"
build.SHADOW_SOURCE = REVIEW / "UNIT_SIEGEBASE_SHADOW_HD4_PREVIEW.png"
build.TOP_SOURCE = REVIEW / "UNIT_SIEGETOP_HD4_PREVIEW.png"
build.BODY_MASK_SOURCE = REVIEW / "HM_UNIT_SIEGEBASE_HD4_PREVIEW.png"
build.TOP_MASK_SOURCE = REVIEW / "HM_UNIT_SIEGETOP_HD4_PREVIEW.png"
build.OUTPUT_DIR = (
    ROOT / "artifacts" / "siege_tank_integration_v1" / "data"
)

build.BODY_ID = 151
build.SHADOW_ID = 152
build.TOP_ID = 153
build.BODY_NAME = "UNIT_SIEGEBASE"
build.SHADOW_NAME = "UNIT_SIEGEBASE_SHADOW"
build.TOP_NAME = "UNIT_SIEGETOP"
build.BODY_MASK_NAME = "HM_UNIT_SIEGEBASE"
build.TOP_MASK_NAME = "HM_UNIT_SIEGETOP"
build.FRAME_SIZE = (144, 152)
build.ATLAS_SIZE = (1152, 152)
build.FRAME_COUNT = 8
build.LOGICAL_FRAME = (36, 38)
build.PIVOT_LOGICAL = (18, 19)


if __name__ == "__main__":
    raise SystemExit(build.main())
