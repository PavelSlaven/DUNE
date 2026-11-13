#!/usr/bin/env python3
"""Compare the HD harvester camera orientation with the classic atlas."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


def armor_offset(
    atlas: Image.Image,
    column: int,
) -> tuple[float, float]:
    frame_width = atlas.width // 8
    frame_height = atlas.height // 4
    frame = np.asarray(
        atlas.crop(
            (
                column * frame_width,
                0,
                (column + 1) * frame_width,
                frame_height,
            )
        ).convert("RGBA"),
        dtype=np.float32,
    )
    red, green, blue, alpha = (frame[:, :, index] for index in range(4))
    opaque = alpha > 30
    armor = (
        opaque
        & (red > 60)
        & (red > green * 1.4)
        & (red > blue * 1.3)
    )
    body_y, body_x = np.nonzero(opaque)
    armor_y, armor_x = np.nonzero(armor)
    if not len(body_x) or not len(armor_x):
        raise AssertionError(f"unable to measure column {column}")
    return (
        (float(armor_x.mean()) - float(body_x.mean())) / frame_width,
        (float(armor_y.mean()) - float(body_y.mean())) / frame_height,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("classic", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    classic = Image.open(args.classic)
    candidate = Image.open(args.candidate)
    if classic.size != (640, 208):
        print(f"FAIL: classic atlas has unexpected size {classic.size}")
        return 1
    if candidate.size != (2560, 832):
        print(f"FAIL: candidate atlas has unexpected size {candidate.size}")
        return 1

    errors: list[str] = []
    for column, direction in enumerate(DIRECTIONS):
        expected_x, expected_y = armor_offset(classic, column)
        actual_x, actual_y = armor_offset(candidate, column)
        if expected_y * actual_y <= 0:
            errors.append(
                f"{direction}: vertical camera orientation is inverted "
                f"(classic={expected_y:.4f}, candidate={actual_y:.4f})"
            )
        if abs(expected_x) >= 0.008 and expected_x * actual_x <= 0:
            errors.append(
                f"{direction}: lateral camera orientation is mirrored "
                f"(classic={expected_x:.4f}, candidate={actual_x:.4f})"
            )

    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        return 1
    print("PASS: all eight HD headings match the classic camera orientation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
