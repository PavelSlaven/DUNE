#!/usr/bin/env python3
"""Detect truncated W/SW silhouettes in the installed pistol infantry atlases."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from hd_assets import decode_image, read_pack


RESOURCES = (155, 156)
PAIRS = ((0, 4, "E/W"), (7, 5, "SE/SW"))
ROWS = 4


def frame_alpha(atlas: Image.Image, column: int, row: int) -> np.ndarray:
    frame_width = atlas.width // 8
    frame_height = atlas.height // ROWS
    alpha = np.asarray(
        atlas.crop(
            (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
        ).getchannel("A"),
        dtype=np.uint8,
    )
    visible = alpha > 0
    coordinates = np.argwhere(visible)
    if not len(coordinates):
        raise AssertionError(f"empty frame at column {column}, row {row}")
    top, left = coordinates.min(axis=0)
    bottom, right = coordinates.max(axis=0) + 1
    return alpha[top:bottom, left:right]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, required=True)
    args = parser.parse_args()

    entries = read_pack(args.pack)
    failures: list[str] = []
    for resource_id in RESOURCES:
        atlas = decode_image(entries[resource_id].payload)
        if atlas is None:
            failures.append(f"{resource_id}: image cannot be decoded")
            continue
        for source_column, target_column, label in PAIRS:
            for row in range(ROWS):
                source = np.fliplr(frame_alpha(atlas, source_column, row))
                target = frame_alpha(atlas, target_column, row)
                source_visible = source > 8
                target_visible = target > 8
                area_ratio = target_visible.sum() / source_visible.sum()
                height_delta = abs(source.shape[0] - target.shape[0])
                width_delta = abs(source.shape[1] - target.shape[1])
                # HD2 is derived with a per-cell Lanczos reduction.  A mirrored
                # subject can therefore gain one antialiased boundary pixel,
                # while a genuinely truncated direction loses 15-30% of its
                # silhouette.  Keep the assertion tolerant only to that
                # resampling footprint.
                if not (
                    0.94 <= area_ratio <= 1.06
                    and height_delta == 0
                    and width_delta <= 2
                ):
                    failures.append(
                        f"{resource_id}:{label}:row{row} silhouette is truncated "
                        f"(area={area_ratio:.3f}, width_delta={width_delta}, "
                        f"height_delta={height_delta})"
                    )

    if failures:
        print("\n".join(failures))
        return 1
    print("W/SW silhouettes are complete and mirror their opposite facings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
