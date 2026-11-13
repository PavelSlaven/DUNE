#!/usr/bin/env python3
"""Validate the second approval-ready combat-tank preview."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

import prepare_tank_review as tank
from verify_tank_alignment_and_scale import turret_hub_center
from verify_tank_visual_registration import visual_socket_center


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "tank_review_v2"
BODY4 = OUTPUT / "UNIT_TANKBASE_HD4_PREVIEW.png"
BODY_ALIGNMENT = OUTPUT / "UNIT_TANKBASE_ALIGNMENT_REFERENCE.png"
BODY2 = OUTPUT / "UNIT_TANKBASE_HD2_PREVIEW.png"
BODY_MASK = OUTPUT / "HM_UNIT_TANKBASE_HD4_PREVIEW.png"
SHADOW = OUTPUT / "UNIT_TANKBASE_SHADOW_HD4_PREVIEW.png"
TOP4 = OUTPUT / "UNIT_TANKTOP_HD4_PREVIEW.png"
TOP2 = OUTPUT / "UNIT_TANKTOP_HD2_PREVIEW.png"
TOP_MASK = OUTPUT / "HM_UNIT_TANKTOP_HD4_PREVIEW.png"

FRAME = 128
CLASSIC_FRAME = 32
MAX_EXTENT_ERROR = 0.055
MAX_PIVOT_OFFSET = 1.5


def frames(image: Image.Image, size: int) -> list[Image.Image]:
    expected = (size * 8, size)
    if image.size != expected:
        raise AssertionError(
            f"unexpected atlas dimensions {image.size}, expected {expected}"
        )
    return [
        image.crop((index * size, 0, (index + 1) * size, size))
        for index in range(8)
    ]


def main() -> int:
    body4 = Image.open(BODY4).convert("RGBA")
    Image.open(BODY_ALIGNMENT).verify()
    body2 = Image.open(BODY2).convert("RGBA")
    body_mask = Image.open(BODY_MASK).convert("RGBA")
    shadow = Image.open(SHADOW).convert("RGBA")
    top4 = Image.open(TOP4).convert("RGBA")
    top2 = Image.open(TOP2).convert("RGBA")
    top_mask = Image.open(TOP_MASK).convert("RGBA")

    if ImageChops.difference(
        body2,
        body4.resize(body2.size, Image.Resampling.LANCZOS),
    ).getbbox():
        raise AssertionError("HD2 body is not the HD4 derivative")
    if ImageChops.difference(
        top2,
        top4.resize(top2.size, Image.Resampling.LANCZOS),
    ).getbbox():
        raise AssertionError("HD2 turret is not the HD4 derivative")

    for name, image in (
        ("body mask", body_mask),
        ("shadow", shadow),
        ("turret mask", top_mask),
    ):
        if image.size != (1024, 128):
            raise AssertionError(f"{name} dimensions changed: {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is empty")

    body_frames = frames(body4, FRAME)
    top_frames = frames(top4, FRAME)
    classic_body_frames = frames(
        Image.open(tank.CLASSIC_BODY).convert("RGBA"),
        CLASSIC_FRAME,
    )
    classic_top_frames = frames(
        Image.open(tank.CLASSIC_TOP).convert("RGBA"),
        CLASSIC_FRAME,
    )
    for name, items in (("body", body_frames), ("turret", top_frames)):
        if len({item.tobytes() for item in items}) != 8:
            raise AssertionError(f"{name} directions are not unique")

    extent_details = []
    pivot_details = []
    for index, direction in enumerate(tank.DIRECTIONS):
        body_extents = tank.oriented_extents(body_frames[index], index)
        top_extents = tank.oriented_extents(top_frames[index], index)
        classic_body_extents = tank.oriented_extents(
            classic_body_frames[index],
            index,
        )
        classic_top_extents = tank.oriented_extents(
            classic_top_frames[index],
            index,
        )
        body_ratios = tuple(
            actual / (classic * 4.0)
            for actual, classic in zip(
                body_extents,
                classic_body_extents,
                strict=True,
            )
        )
        top_ratios = tuple(
            actual / (classic * 4.0)
            for actual, classic in zip(
                top_extents,
                classic_top_extents,
                strict=True,
            )
        )
        for ratio in body_ratios + top_ratios:
            if abs(ratio - tank.CLASSIC_EXTENT_SCALE) > MAX_EXTENT_ERROR:
                raise AssertionError(
                    f"{direction} extent ratio {ratio:.3f} differs from "
                    f"{tank.CLASSIC_EXTENT_SCALE:.3f}"
                )

        body_center = visual_socket_center(body_frames[index])
        top_center = turret_hub_center(top_frames[index])
        body_offset = float(
            np.hypot(body_center[0] - 64.0, body_center[1] - 64.0)
        )
        top_offset = float(
            np.hypot(top_center[0] - 64.0, top_center[1] - 64.0)
        )
        body_top_offset = float(
            np.hypot(
                body_center[0] - top_center[0],
                body_center[1] - top_center[1],
            )
        )
        if max(body_offset, top_offset, body_top_offset) > MAX_PIVOT_OFFSET:
            raise AssertionError(
                f"{direction} pivot mismatch: body={body_center}, "
                f"turret={top_center}"
            )
        extent_details.append(
            f"{direction}:body=({body_ratios[0]:.3f},"
            f"{body_ratios[1]:.3f}),top=({top_ratios[0]:.3f},"
            f"{top_ratios[1]:.3f})"
        )
        pivot_details.append(
            f"{direction}=({body_center[0]:.1f},{body_center[1]:.1f})"
        )

    print(
        "Combat-tank v2 review is valid: "
        + "; ".join(extent_details)
        + "; pivots "
        + ", ".join(pivot_details)
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
