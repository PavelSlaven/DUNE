#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved WOR Barracks."""

from __future__ import annotations

from pathlib import Path

import build_barracks_integration as build


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "artifacts" / "wor_barracks_review_v1"

build.REVIEW = REVIEW
build.SOURCE = REVIEW / "BUILD_WOR_HD4_PREVIEW.png"
build.SHADOW_SOURCE = REVIEW / "BUILD_WOR_SHADOW_HD4_PREVIEW.png"
build.FLAG_SOURCE = REVIEW / "BUILD_WOR_FLAG_HD4_PREVIEW.png"
build.MASK_SOURCE = REVIEW / "HM_BUILD_WOR_FLAG_HD4_PREVIEW.png"
build.OUTPUT_DIR = ROOT / "artifacts" / "wor_barracks_integration_v1" / "data"

build.BARRACKS_ID = 42
build.SHADOW_ID = 43
build.BUILDING_NAME = "BUILD_WOR"
build.SHADOW_NAME = "BUILD_WOR_SHADOW"
build.FLAG_NAME = "BUILD_WOR_FLAG"
build.MASK_NAME = "HM_BUILD_WOR_FLAG"


if __name__ == "__main__":
    raise SystemExit(build.main())
