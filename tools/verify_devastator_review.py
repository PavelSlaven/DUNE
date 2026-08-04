#!/usr/bin/env python3
"""Validate the approval-ready HD Devastator atlas."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "devastator_review_v1"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0132_UNIT_DEVASTATOR.png"
)
HD4 = OUTPUT / "UNIT_DEVASTATOR_HD4_PREVIEW.png"
HD2 = OUTPUT / "UNIT_DEVASTATOR_HD2_PREVIEW.png"
MASK = OUTPUT / "HM_UNIT_DEVASTATOR_HD4_PREVIEW.png"
SHADOW = OUTPUT / "UNIT_DEVASTATOR_SHADOW_HD4_PREVIEW.png"

FRAME = (152, 192)
ATLAS = (1216, 192)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
DIRECTION_AXIS_LIMITS = {
    "NE": 8.0,
    "N": 2.0,
    "NW": 8.0,
    "SW": 7.0,
    "S": 8.0,
    "SE": 7.0,
}
MIN_TRACK_FACE_DOWNWARD_OFFSET = 3.5
MIN_DIAGONAL_TRACK_FACE_DOWNWARD_OFFSET = 1.5
MAX_DIAGONAL_TRACK_FACE_HORIZONTAL_OFFSET = 4.0


def frame(
    atlas: Image.Image,
    index: int,
    width: int,
    height: int,
) -> Image.Image:
    return atlas.crop(
        (index * width, 0, (index + 1) * width, height)
    )


def principal_axis(image: Image.Image) -> float:
    alpha = np.asarray(image.convert("RGBA"))[:, :, 3] > 32
    yy, xx = np.nonzero(alpha)
    if xx.size < 10:
        raise AssertionError("empty direction frame")
    points = np.column_stack((xx - xx.mean(), yy - yy.mean()))
    _, vectors = np.linalg.eigh(np.cov(points, rowvar=False))
    vector = vectors[:, -1]
    return math.degrees(math.atan2(vector[1], vector[0]))


def axis_difference(left: float, right: float) -> float:
    return abs(((left - right + 90.0) % 180.0) - 90.0)


def track_face_offset(image: Image.Image) -> tuple[float, float]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3] > 64
    yy, xx = np.nonzero(alpha)
    center_x = float(xx.mean())
    center_y = float(yy.mean())
    luminance = (
        rgba[:, :, 0] * 0.299
        + rgba[:, :, 1] * 0.587
        + rgba[:, :, 2] * 0.114
    )
    maximum = rgba[:, :, :3].max(axis=2)
    minimum = rgba[:, :, :3].min(axis=2)
    saturation = (maximum - minimum) / np.maximum(maximum, 1.0)
    track_face = (
        alpha
        & (luminance < 65.0)
        & (saturation < 0.35)
    )
    track_y, track_x = np.nonzero(track_face)
    if track_x.size < 100:
        raise AssertionError("unable to identify visible track faces")
    return (
        float(track_x.mean() - center_x),
        float(track_y.mean() - center_y),
    )


def main() -> int:
    base4 = Image.open(HD4).convert("RGBA")
    base2 = Image.open(HD2).convert("RGBA")
    mask = Image.open(MASK).convert("RGBA")
    shadow = Image.open(SHADOW).convert("RGBA")
    classic = Image.open(CLASSIC).convert("RGBA")
    if base4.size != ATLAS:
        raise AssertionError(f"unexpected HD4 atlas: {base4.size}")
    if base2.size != (608, 96):
        raise AssertionError(f"unexpected HD2 atlas: {base2.size}")
    for name, image in (("mask", mask), ("shadow", shadow)):
        if image.size != ATLAS:
            raise AssertionError(f"unexpected {name} atlas: {image.size}")

    expected2 = base4.resize(base2.size, Image.Resampling.LANCZOS)
    if ImageChops.difference(base2, expected2).getbbox():
        raise AssertionError("HD2 is not the deterministic HD4 derivative")

    frames = [
        frame(base4, index, FRAME[0], FRAME[1])
        for index in range(8)
    ]
    if len({item.tobytes() for item in frames}) != 8:
        raise AssertionError("the eight directions are not unique")
    if np.count_nonzero(np.asarray(mask)[:, :, 3] > 8) < 1000:
        raise AssertionError("house-colour mask is unexpectedly small")

    axis_details = []
    track_details = []
    for index, direction in enumerate(DIRECTIONS):
        hd_frame = frames[index]
        classic_frame = frame(classic, index, 38, 48)
        hd_box = hd_frame.getchannel("A").getbbox()
        classic_box = classic_frame.getchannel("A").getbbox()
        if hd_box is None or classic_box is None:
            raise AssertionError(f"{direction} is empty")
        target_box = tuple(value * 4 for value in classic_box)
        hd_center = (
            (hd_box[0] + hd_box[2]) / 2.0,
            (hd_box[1] + hd_box[3]) / 2.0,
        )
        target_center = (
            (target_box[0] + target_box[2]) / 2.0,
            (target_box[1] + target_box[3]) / 2.0,
        )
        center_offset = math.hypot(
            hd_center[0] - target_center[0],
            hd_center[1] - target_center[1],
        )
        if center_offset > 2.0:
            raise AssertionError(
                f"{direction} anchor offset is {center_offset:.2f}px"
            )
        if (
            hd_box[0] < target_box[0] - 1
            or hd_box[1] < target_box[1] - 1
            or hd_box[2] > target_box[2] + 1
            or hd_box[3] > target_box[3] + 1
        ):
            raise AssertionError(
                f"{direction} exceeds its classic contract box"
            )
        if direction in DIRECTION_AXIS_LIMITS:
            difference = axis_difference(
                principal_axis(hd_frame),
                principal_axis(classic_frame),
            )
            if difference > DIRECTION_AXIS_LIMITS[direction]:
                raise AssertionError(
                    f"{direction} axis differs by {difference:.2f} degrees"
                )
            axis_details.append(f"{direction}={difference:.1f}°")
        track_x, track_y = track_face_offset(hd_frame)
        minimum_track_y = (
            MIN_DIAGONAL_TRACK_FACE_DOWNWARD_OFFSET
            if direction in ("NE", "NW")
            else MIN_TRACK_FACE_DOWNWARD_OFFSET
        )
        if track_y < minimum_track_y:
            raise AssertionError(
                f"{direction} rotates the fixed camera: visible track "
                f"face offset is ({track_x:.1f},{track_y:.1f})"
            )
        if (
            direction in ("NE", "NW")
            and abs(track_x) > MAX_DIAGONAL_TRACK_FACE_HORIZONTAL_OFFSET
        ):
            raise AssertionError(
                f"{direction} rotates the fixed camera: visible track "
                f"face offset is ({track_x:.1f},{track_y:.1f})"
            )
        track_details.append(f"{direction}={track_y:.1f}px")

    print(
        "Devastator review is valid: ID 132, 8 directions, "
        "38x48 logical, HD4 152x192; axes "
        + ", ".join(axis_details)
        + "; track faces "
        + ", ".join(track_details)
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
