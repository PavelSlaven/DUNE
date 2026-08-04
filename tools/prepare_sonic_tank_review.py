#!/usr/bin/env python3
"""Build a deterministic eight-direction Sonic Tank HD4 review atlas."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "sonic_tank_review_v1"
SOURCE = OUT / "SONICTANK_TOP_MASTER_RGBA.png"

FRAME = 128
LOGICAL_FRAME = 32
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ANGLES = (180, -135, -90, -45, 0, 45, 90, 135)


def centered_master(source: Image.Image) -> Image.Image:
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise AssertionError("Sonic Tank source is fully transparent")
    source = source.crop(bbox)
    # Keep the longest rotated bounding box below 120 px. This leaves a safe
    # margin while retaining the original 32x32 unit's substantial footprint.
    target_width = 100
    target_height = max(1, round(source.height * target_width / source.width))
    if target_height > 67:
        target_height = 67
        target_width = max(1, round(source.width * target_height / source.height))
    source = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", (FRAME, FRAME), (0, 0, 0, 0))
    output.alpha_composite(
        source,
        ((FRAME - target_width) // 2, (FRAME - target_height) // 2),
    )
    return output


def rotate_frames(master: Image.Image) -> list[Image.Image]:
    return [
        master.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
        for angle in ANGLES
    ]


def house_mask(frame: Image.Image) -> Image.Image:
    rgba = frame.convert("RGBA")
    output = Image.new("RGBA", rgba.size, (255, 255, 255, 0))
    source = rgba.load()
    target = output.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = source[x, y]
            if a == 0:
                continue
            green_bias = g - max(r, b)
            if green_bias <= 10 or g < 70:
                continue
            strength = min(225, 65 + green_bias * 4)
            target[x, y] = (255, 255, 255, a * strength // 255)
    return output.filter(ImageFilter.GaussianBlur(0.35))


def shadow(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(2.0))
    alpha = alpha.point(lambda value: value * 92 // 255)
    silhouette = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    silhouette.putalpha(alpha)
    output = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    output.alpha_composite(silhouette, (3, 4))
    return output


def atlas(frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (FRAME * len(frames), FRAME), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        output.alpha_composite(frame, (index * FRAME, 0))
    return output


def review_sheet(frames: list[Image.Image]) -> Image.Image:
    scale = 2
    cell = FRAME * scale
    label_height = 34
    output = Image.new("RGB", (cell * 4, (cell + label_height) * 2), (20, 22, 25))
    draw = ImageDraw.Draw(output)
    for index, (direction, frame) in enumerate(zip(DIRECTIONS, frames)):
        col = index % 4
        row = index // 4
        x = col * cell
        y = row * (cell + label_height)
        backdrop = Image.new("RGBA", (FRAME, FRAME), (44, 47, 51, 255))
        backdrop.alpha_composite(frame)
        output.paste(
            backdrop.convert("RGB").resize((cell, cell), Image.Resampling.LANCZOS),
            (x, y),
        )
        draw.rectangle((x, y, x + cell - 1, y + cell - 1), outline=(104, 91, 54))
        draw.text((x + 10, y + cell + 8), direction, fill=(238, 218, 151))
    return output


def validate(frames: list[Image.Image], masks: list[Image.Image]) -> dict[str, object]:
    if len(frames) != 8 or len(masks) != 8:
        raise AssertionError("Sonic Tank must contain exactly eight directions")
    if len({frame.tobytes() for frame in frames}) != 8:
        raise AssertionError("Sonic Tank directions are not unique")
    bboxes = [frame.getchannel("A").getbbox() for frame in frames]
    if any(bbox is None for bbox in bboxes):
        raise AssertionError("a Sonic Tank direction is empty")
    for bbox in bboxes:
        assert bbox is not None
        if bbox[0] < 3 or bbox[1] < 3 or bbox[2] > FRAME - 3 or bbox[3] > FRAME - 3:
            raise AssertionError(f"Sonic Tank is too close to frame edge: {bbox}")
    coverage = []
    for frame in frames:
        histogram = frame.getchannel("A").histogram()
        coverage.append(sum(histogram[17:]))
    if max(coverage) / min(coverage) > 1.03:
        raise AssertionError("Sonic Tank changes apparent area between directions")
    if any(mask.getchannel("A").getbbox() is None for mask in masks):
        raise AssertionError("a Sonic Tank house mask is empty")
    return {
        "directions": list(DIRECTIONS),
        "angles": list(ANGLES),
        "logical_frame": [LOGICAL_FRAME, LOGICAL_FRAME],
        "hd4_frame": [FRAME, FRAME],
        "atlas": [FRAME * 8, FRAME],
        "alpha_bboxes": [list(bbox) for bbox in bboxes if bbox is not None],
        "opaque_coverage": coverage,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    master = centered_master(Image.open(SOURCE).convert("RGBA"))
    frames = rotate_frames(master)
    masks = [house_mask(frame) for frame in frames]
    shadows = [shadow(frame) for frame in frames]
    report = validate(frames, masks)

    master.save(OUT / "SONICTANK_TOP_MASTER_CENTERED_HD4.png", optimize=True)
    atlas(frames).save(OUT / "UNIT_SONICTANK_HD4_PREVIEW.png", optimize=True)
    atlas(masks).save(OUT / "HM_UNIT_SONICTANK_HD4_PREVIEW.png", optimize=True)
    atlas(shadows).save(
        OUT / "UNIT_SONICTANK_SHADOW_HD4_PREVIEW.png", optimize=True
    )
    review_sheet(frames).save(OUT / "UNIT_SONICTANK_REVIEW_SHEET.png", optimize=True)
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
