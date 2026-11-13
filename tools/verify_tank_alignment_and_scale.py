#!/usr/bin/env python3
"""Regression check for combat-tank pivot alignment and stable scale."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from hd_assets import decode_image, read_pack
from verify_tank_visual_registration import (
    runtime_tank_scale,
    visual_socket_center,
)


ROOT = Path(__file__).resolve().parents[1]
GAME_PACK = Path(
    "C:/Users/Slaven/Desktop/"
    "D2TM-v0.8.0.windows.ru/data/sdl_data_hd4.dat"
)
CLASSIC_DIR = ROOT / "resources" / "hd" / "classic" / "sdl_data"
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
DIRECTION_VECTORS = (
    (1.0, 0.0),
    (2**-0.5, -(2**-0.5)),
    (0.0, -1.0),
    (-(2**-0.5), -(2**-0.5)),
    (-1.0, 0.0),
    (-(2**-0.5), 2**-0.5),
    (0.0, 1.0),
    (2**-0.5, 2**-0.5),
)
BODY_ID = 159
TURRET_ID = 161
HD_FRAME = 128
CLASSIC_FRAME = 32
MAX_EXTENT_RATIO_ERROR = 0.07
MAX_HUB_OFFSET = 1.25
MAX_BODY_TOP_HUB_OFFSET = 1.50
EXPECTED_EXTENT_RATIO = 1.28


def horizontal_frames(image: Image.Image, size: int) -> list[Image.Image]:
    if image.size != (size * 8, size):
        raise AssertionError(f"unexpected atlas dimensions: {image.size}")
    return [
        image.crop((index * size, 0, (index + 1) * size, size))
        for index in range(8)
    ]


def oriented_extents(
    image: Image.Image,
    direction_index: int,
) -> tuple[float, float]:
    alpha = np.asarray(image.convert("RGBA"))[:, :, 3]
    yy, xx = np.nonzero(alpha > 24)
    if xx.size == 0:
        raise AssertionError("empty tank frame")
    dx, dy = DIRECTION_VECTORS[direction_index]
    offset_x = xx - image.width / 2.0
    offset_y = yy - image.height / 2.0
    forward = offset_x * dx + offset_y * dy
    lateral = -offset_x * dy + offset_y * dx
    return (
        float(forward.max() - forward.min() + 1.0),
        float(lateral.max() - lateral.min() + 1.0),
    )


def turret_hub_center(frame: Image.Image) -> tuple[float, float]:
    alpha = np.asarray(frame.convert("RGBA"))[:, :, 3] > 24
    # Remove the thin gun barrel and small edge details, leaving the dome.
    core = ndimage.binary_erosion(alpha, iterations=7)
    labels, count = ndimage.label(core)
    if count < 1:
        raise AssertionError("unable to isolate tank turret hub")
    sizes = ndimage.sum(core, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    center_y, center_x = ndimage.center_of_mass(core, labels, largest)
    return float(center_x), float(center_y)


def body_turret_center(frame: Image.Image) -> tuple[float, float]:
    return visual_socket_center(frame)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, default=GAME_PACK)
    args = parser.parse_args()
    entries = read_pack(args.pack)
    body_hd = decode_image(entries[BODY_ID].payload)
    turret_hd = decode_image(entries[TURRET_ID].payload)
    if body_hd is None or turret_hd is None:
        raise AssertionError("installed tank resources cannot be decoded")

    body_classic = Image.open(
        CLASSIC_DIR / "0159_UNIT_TANKBASE.png"
    ).convert("RGBA")
    turret_classic = Image.open(
        CLASSIC_DIR / "0161_UNIT_TANKTOP.png"
    ).convert("RGBA")
    body_frames_hd = horizontal_frames(body_hd.convert("RGBA"), HD_FRAME)
    body_frames_classic = horizontal_frames(body_classic, CLASSIC_FRAME)
    turret_frames_hd = horizontal_frames(
        turret_hd.convert("RGBA"),
        HD_FRAME,
    )
    turret_frames_classic = horizontal_frames(
        turret_classic,
        CLASSIC_FRAME,
    )
    combat_tank_runtime_scale = runtime_tank_scale()

    body_extent_ratios = [
        tuple(
            hd_extent / (classic_extent * 4.0)
            for hd_extent, classic_extent in zip(
                (
                    extent * combat_tank_runtime_scale
                    for extent in oriented_extents(hd, index)
                ),
                oriented_extents(classic, index),
                strict=True,
            )
        )
        for index, (hd, classic) in enumerate(
            zip(
                body_frames_hd,
                body_frames_classic,
                strict=True,
            )
        )
    ]
    turret_extent_ratios = [
        tuple(
            hd_extent / (classic_extent * 4.0)
            for hd_extent, classic_extent in zip(
                (
                    extent * combat_tank_runtime_scale
                    for extent in oriented_extents(hd, index)
                ),
                oriented_extents(classic, index),
                strict=True,
            )
        )
        for index, (hd, classic) in enumerate(
            zip(
                turret_frames_hd,
                turret_frames_classic,
                strict=True,
            )
        )
    ]
    extent_errors = [
        abs(ratio - EXPECTED_EXTENT_RATIO)
        for ratios in body_extent_ratios + turret_extent_ratios
        for ratio in ratios
    ]

    expected_center = HD_FRAME / 2.0
    hub_offsets = []
    hub_centers = []
    body_hub_centers = []
    body_top_offsets = []
    for body_frame, turret_frame in zip(
        body_frames_hd,
        turret_frames_hd,
        strict=True,
    ):
        body_center_x, body_center_y = body_turret_center(body_frame)
        center_x, center_y = turret_hub_center(turret_frame)
        body_hub_centers.append((body_center_x, body_center_y))
        hub_centers.append((center_x, center_y))
        hub_offsets.append(
            float(
                np.hypot(
                    center_x - expected_center,
                    center_y - expected_center,
                )
            )
        )
        body_top_offsets.append(
            float(
                np.hypot(
                    center_x - body_center_x,
                    center_y - body_center_y,
                )
            )
        )

    details = ", ".join(
        f"{direction}:body=({body_ratio[0]:.3f},"
        f"{body_ratio[1]:.3f}),"
        f"turret=({turret_ratio[0]:.3f},"
        f"{turret_ratio[1]:.3f}),"
        f"bodyhub=({body_center[0]:.2f},{body_center[1]:.2f}),"
        f"tophub=({center[0]:.2f},{center[1]:.2f}),"
        f"center-offset={offset:.2f},"
        f"body-top-offset={body_top_offset:.2f}"
        for (
            direction,
            body_ratio,
            turret_ratio,
            body_center,
            center,
            offset,
            body_top_offset,
        ) in zip(
            DIRECTIONS,
            body_extent_ratios,
            turret_extent_ratios,
            body_hub_centers,
            hub_centers,
            hub_offsets,
            body_top_offsets,
            strict=True,
        )
    )
    errors = []
    if max(extent_errors) > MAX_EXTENT_RATIO_ERROR:
        errors.append(
            f"atlas extent error {max(extent_errors):.3f} exceeds "
            f"{MAX_EXTENT_RATIO_ERROR:.3f}"
        )
    if max(hub_offsets) > MAX_HUB_OFFSET:
        errors.append(
            f"turret hub offset {max(hub_offsets):.2f}px exceeds "
            f"{MAX_HUB_OFFSET:.2f}px"
        )
    if max(body_top_offsets) > MAX_BODY_TOP_HUB_OFFSET:
        errors.append(
            f"body/turret hub offset {max(body_top_offsets):.2f}px "
            f"exceeds {MAX_BODY_TOP_HUB_OFFSET:.2f}px"
        )
    if errors:
        raise AssertionError("; ".join(errors) + ": " + details)
    print("Combat-tank alignment and scale are consistent: " + details)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
