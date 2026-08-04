#!/usr/bin/env python3
"""Verify the combat tank's visible turret socket and in-game size."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
GAME_PACK = Path(
    "C:/Users/Slaven/Desktop/"
    "D2TM-v0.8.0.windows.ru/data/sdl_data_hd4.dat"
)
WORLD_SCALE_HEADER = ROOT / "src" / "utils" / "WorldObjectScale.hpp"
CLASSIC_DIR = ROOT / "resources" / "hd" / "classic" / "sdl_data"
OUTPUT = ROOT / "artifacts" / "tank_alignment_fix_v3"

BODY_ID = 159
TURRET_ID = 161
HD_FRAME = 128
CLASSIC_FRAME = 32
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
MAX_SOCKET_OFFSET = 1.5
MIN_RUNTIME_WIDTH_RATIO = 0.85
MAX_RUNTIME_WIDTH_RATIO = 1.15


def horizontal_frames(image: Image.Image, size: int) -> list[Image.Image]:
    if image.size != (size * 8, size):
        raise AssertionError(f"unexpected atlas dimensions: {image.size}")
    return [
        image.crop((index * size, 0, (index + 1) * size, size))
        for index in range(8)
    ]


def visual_socket_center(frame: Image.Image) -> tuple[float, float]:
    """Locate the dark turret socket inside its brighter metal annulus."""
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.float32)
    luminance = (
        rgba[:, :, 0] * 0.299
        + rgba[:, :, 1] * 0.587
        + rgba[:, :, 2] * 0.114
    )
    alpha = rgba[:, :, 3] > 32
    yy, xx = np.mgrid[: frame.height, : frame.width]
    best: tuple[float, float, float] | None = None
    for center_y in range(42, 79):
        for center_x in range(48, 81):
            inner_radius = (
                ((xx - center_x) / 12.0) ** 2
                + ((yy - center_y) / 8.0) ** 2
            )
            outer_radius = (
                ((xx - center_x) / 22.0) ** 2
                + ((yy - center_y) / 14.0) ** 2
            )
            inner = (inner_radius <= 1.0) & alpha
            annulus = (
                (inner_radius > 1.0)
                & (outer_radius <= 1.0)
                & alpha
            )
            if np.count_nonzero(inner) < 100:
                continue
            if np.count_nonzero(annulus) < 200:
                continue
            score = (
                float(luminance[annulus].mean())
                - float(luminance[inner].mean())
                - abs(center_x - 64.0) * 0.15
            )
            candidate = (score, float(center_x), float(center_y))
            if best is None or candidate[0] > best[0]:
                best = candidate
    if best is None:
        raise AssertionError("unable to locate the visible turret socket")
    return best[1], best[2]


def alpha_width(frame: Image.Image) -> int:
    box = frame.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("empty tank frame")
    return box[2] - box[0]


def runtime_tank_scale() -> float:
    source = WORLD_SCALE_HEADER.read_text(encoding="utf-8")
    match = re.search(
        r"hd(?:Combat)?TankMultiplier\s*=\s*([0-9.]+)F",
        source,
    )
    return float(match.group(1)) if match is not None else 1.0


def build_diagnostic(
    body_frames: list[Image.Image],
    turret_frames: list[Image.Image],
    centers: list[tuple[float, float]],
    path: Path,
) -> None:
    scale = 2
    cell = HD_FRAME * scale
    board = Image.new("RGBA", (cell * 4, cell * 2), (18, 20, 24, 255))
    for index, (body, turret, center) in enumerate(
        zip(body_frames, turret_frames, centers, strict=True)
    ):
        composite = body.copy()
        composite.alpha_composite(turret)
        x = index % 4 * cell
        y = index // 4 * cell
        board.alpha_composite(
            composite.resize((cell, cell), Image.Resampling.NEAREST),
            (x, y),
        )
        draw = ImageDraw.Draw(board)
        socket_x = x + round(center[0] * scale)
        socket_y = y + round(center[1] * scale)
        pivot_x = x + HD_FRAME
        pivot_y = y + HD_FRAME
        draw.ellipse(
            (
                socket_x - 5,
                socket_y - 5,
                socket_x + 5,
                socket_y + 5,
            ),
            outline=(255, 70, 50, 255),
            width=2,
        )
        draw.line(
            (pivot_x - 6, pivot_y, pivot_x + 6, pivot_y),
            fill=(60, 255, 100, 255),
            width=2,
        )
        draw.line(
            (pivot_x, pivot_y - 6, pivot_x, pivot_y + 6),
            fill=(60, 255, 100, 255),
            width=2,
        )
        draw.text(
            (x + 8, y + 8),
            DIRECTIONS[index],
            fill=(255, 230, 185, 255),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    board.save(path, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, default=GAME_PACK)
    args = parser.parse_args()

    entries = read_pack(args.pack)
    body = decode_image(entries[BODY_ID].payload)
    turret = decode_image(entries[TURRET_ID].payload)
    if body is None or turret is None:
        raise AssertionError("installed tank resources cannot be decoded")
    body_frames = horizontal_frames(body.convert("RGBA"), HD_FRAME)
    turret_frames = horizontal_frames(turret.convert("RGBA"), HD_FRAME)
    centers = [visual_socket_center(frame) for frame in body_frames]
    build_diagnostic(
        body_frames,
        turret_frames,
        centers,
        OUTPUT / "tank_registration_diagnostic.png",
    )

    socket_offsets = [
        float(np.hypot(center_x - 64.0, center_y - 64.0))
        for center_x, center_y in centers
    ]
    classic = Image.open(
        CLASSIC_DIR / "0159_UNIT_TANKBASE.png"
    ).convert("RGBA")
    classic_frames = horizontal_frames(classic, CLASSIC_FRAME)
    runtime_scale = runtime_tank_scale()
    width_ratios = [
        alpha_width(hd) * runtime_scale
        / (alpha_width(original) * 4.0)
        for hd, original in zip(
            body_frames,
            classic_frames,
            strict=True,
        )
    ]
    details = ", ".join(
        f"{direction}:socket=({center[0]:.0f},{center[1]:.0f}),"
        f"offset={offset:.1f},width={width:.3f}"
        for direction, center, offset, width in zip(
            DIRECTIONS,
            centers,
            socket_offsets,
            width_ratios,
            strict=True,
        )
    )
    errors = []
    if max(socket_offsets) > MAX_SOCKET_OFFSET:
        errors.append(
            f"visible socket offset {max(socket_offsets):.1f}px exceeds "
            f"{MAX_SOCKET_OFFSET:.1f}px"
        )
    if min(width_ratios) < MIN_RUNTIME_WIDTH_RATIO:
        errors.append(
            f"runtime width ratio {min(width_ratios):.3f} is below "
            f"{MIN_RUNTIME_WIDTH_RATIO:.3f}"
        )
    if max(width_ratios) > MAX_RUNTIME_WIDTH_RATIO:
        errors.append(
            f"runtime width ratio {max(width_ratios):.3f} exceeds "
            f"{MAX_RUNTIME_WIDTH_RATIO:.3f}"
        )
    if errors:
        raise AssertionError("; ".join(errors) + ": " + details)
    print("Combat-tank visual registration is correct: " + details)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
