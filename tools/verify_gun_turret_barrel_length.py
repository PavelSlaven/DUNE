#!/usr/bin/env python3
"""Regression check for consistent visible gun-turret barrel length."""

from pathlib import Path

from PIL import Image

from prepare_gun_turret_review import (
    BARREL_JOIN_RADII,
    DIRECTIONS,
    atlas_frame,
    measure_barrel_reach,
)


ROOT = Path(__file__).resolve().parents[1]
ATLAS = (
    ROOT
    / "artifacts"
    / "gun_turret_review_v1"
    / "BUILD_TURRET_HD4_PREVIEW.png"
)
MAX_SPREAD = 2.0


def main() -> None:
    atlas = Image.open(ATLAS).convert("RGBA")
    tips = [
        measure_barrel_reach(atlas_frame(atlas, index), index)
        for index in range(8)
    ]
    lengths = [
        tip - join
        for tip, join in zip(tips, BARREL_JOIN_RADII, strict=True)
    ]
    spread = max(lengths) - min(lengths)
    details = ", ".join(
        f"{direction}={length:.2f}"
        for direction, length in zip(DIRECTIONS, lengths, strict=True)
    )
    if spread > MAX_SPREAD:
        raise AssertionError(
            f"visible barrel length spread {spread:.2f}px exceeds "
            f"{MAX_SPREAD:.2f}px: {details}"
        )
    print(f"Visible gun-turret barrel length is consistent: {details}")


if __name__ == "__main__":
    main()
