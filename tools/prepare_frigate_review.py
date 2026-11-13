#!/usr/bin/env python3
"""Prepare a stable eight-direction HD Frigate atlas from one top-down master."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


DIRECTIONS = (
    ("E", 0),
    ("NE", 45),
    ("N", 90),
    ("NW", 135),
    ("W", 180),
    ("SW", 225),
    ("S", 270),
    ("SE", 315),
)
HD4_FRAME = (256, 256)
HD2_FRAME = (128, 128)


def prepare_square(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("the Frigate master is fully transparent")
    subject = source.crop(bbox)

    # A 45-degree turn has the largest axis-aligned bounds.  Use that exact
    # diagonal extent to retain one physical scale in all eight directions.
    diagonal = math.ceil((subject.width + subject.height) / math.sqrt(2.0))
    side = max(subject.width, subject.height, diagonal) + 48
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.alpha_composite(
        subject,
        ((side - subject.width) // 2, (side - subject.height) // 2),
    )
    return canvas


def render_directions(square: Image.Image) -> list[Image.Image]:
    frames: list[Image.Image] = []
    for _, angle in DIRECTIONS:
        rotated = square.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=False,
            center=(square.width / 2.0, square.height / 2.0),
        )
        frame = rotated.resize(HD4_FRAME, Image.Resampling.LANCZOS)
        frames.append(frame)
    return frames


def make_shadow(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(2.2))
    shifted = Image.new("L", frame.size, 0)
    shifted.paste(alpha, (5, 7))
    shadow = Image.new("RGBA", frame.size, (7, 8, 12, 0))
    shadow.putalpha(shifted.point(lambda value: value * 88 // 255))
    return shadow


def stack_horizontal(
    frames: list[Image.Image],
    frame_size: tuple[int, int],
) -> Image.Image:
    atlas = Image.new(
        "RGBA",
        (frame_size[0] * len(frames), frame_size[1]),
        (0, 0, 0, 0),
    )
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * frame_size[0], 0))
    return atlas


def make_review(frames: list[Image.Image]) -> Image.Image:
    columns, rows = 4, 2
    sheet = Image.new(
        "RGBA",
        (HD4_FRAME[0] * columns, HD4_FRAME[1] * rows),
        (19, 21, 24, 255),
    )
    draw = ImageDraw.Draw(sheet)
    for index, ((label, _), frame) in enumerate(zip(DIRECTIONS, frames, strict=True)):
        x = (index % columns) * HD4_FRAME[0]
        y = (index // columns) * HD4_FRAME[1]
        sheet.alpha_composite(frame, (x, y))
        draw.rounded_rectangle(
            (x + 7, y + 7, x + 51, y + 31),
            radius=5,
            fill=(0, 0, 0, 190),
        )
        draw.text((x + 14, y + 11), label, fill=(255, 218, 88, 255))
    return sheet


def make_rotation_gif(frames: list[Image.Image], output: Path) -> None:
    background = Image.new("RGB", HD4_FRAME, (45, 47, 52))
    images = []
    for frame in frames:
        image = background.copy()
        image.paste(frame.convert("RGB"), (0, 0), frame.getchannel("A"))
        images.append(image)
    images[0].save(
        output,
        save_all=True,
        append_images=images[1:],
        duration=180,
        loop=0,
        disposal=2,
    )


def validate(frames: list[Image.Image]) -> dict[str, object]:
    if len(frames) != len(DIRECTIONS):
        raise AssertionError(f"expected 8 directions, got {len(frames)}")
    if any(frame.size != HD4_FRAME for frame in frames):
        raise AssertionError("one or more Frigate frames have an invalid size")
    if len({frame.tobytes() for frame in frames}) != len(DIRECTIONS):
        raise AssertionError("Frigate directions are not unique")

    centers = []
    coverages = []
    for index, frame in enumerate(frames):
        alpha = np.asarray(frame.getchannel("A"), dtype=np.float64)
        weights = alpha / 255.0
        total = float(weights.sum())
        if total <= 0.0:
            raise AssertionError(f"direction {DIRECTIONS[index][0]} is empty")
        yy, xx = np.indices(weights.shape)
        centers.append(
            (
                float((xx * weights).sum() / total),
                float((yy * weights).sum() / total),
            )
        )
        coverages.append(total)

    center_error = max(
        max(abs(x - 127.5), abs(y - 127.5)) for x, y in centers
    )
    # The engine-heavy stern makes the alpha centroid differ from the fixed
    # geometric pivot.  Opposite directions mirror that mass around the same
    # 127.5 px rotation anchor, so a small centroid orbit is expected.
    if center_error > 7.5:
        raise AssertionError(
            f"Frigate alpha-centroid orbit is too large: {center_error:.3f}px"
        )
    coverage_variation = (
        max(coverages) - min(coverages)
    ) / (sum(coverages) / len(coverages))
    if coverage_variation > 0.025:
        raise AssertionError(
            f"Frigate scale/coverage variation is {coverage_variation:.3%}"
        )

    return {
        "frame_count": len(frames),
        "direction_order": [direction for direction, _ in DIRECTIONS],
        "logical_frame": [64, 64],
        "hd4_frame": list(HD4_FRAME),
        "hd4_atlas": [HD4_FRAME[0] * len(frames), HD4_FRAME[1]],
        "hd2_frame": list(HD2_FRAME),
        "hd2_atlas": [HD2_FRAME[0] * len(frames), HD2_FRAME[1]],
        "fixed_rotation_anchor": [127.5, 127.5],
        "maximum_alpha_centroid_orbit_px": round(center_error, 4),
        "coverage_variation": round(coverage_variation, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    source = Image.open(args.source).convert("RGBA")
    square = prepare_square(source)
    frames4 = render_directions(square)
    report = validate(frames4)
    frames2 = [
        frame.resize(HD2_FRAME, Image.Resampling.LANCZOS)
        for frame in frames4
    ]
    shadows4 = [make_shadow(frame) for frame in frames4]
    shadows2 = [
        shadow.resize(HD2_FRAME, Image.Resampling.LANCZOS)
        for shadow in shadows4
    ]

    stack_horizontal(frames4, HD4_FRAME).save(
        args.out / "UNIT_FRIGATE_HD4_PREVIEW.png"
    )
    stack_horizontal(frames2, HD2_FRAME).save(
        args.out / "UNIT_FRIGATE_HD2_PREVIEW.png"
    )
    stack_horizontal(shadows4, HD4_FRAME).save(
        args.out / "UNIT_FRIGATE_SHADOW_HD4_PREVIEW.png"
    )
    stack_horizontal(shadows2, HD2_FRAME).save(
        args.out / "UNIT_FRIGATE_SHADOW_HD2_PREVIEW.png"
    )
    make_review(frames4).save(args.out / "frigate_8directions_review.png")
    make_rotation_gif(frames4, args.out / "frigate_rotation_preview.gif")
    (args.out / "validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
