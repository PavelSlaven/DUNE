#!/usr/bin/env python3
"""Build a deterministic eight-direction Deviator HD4 review atlas."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "deviator_review_v1"
SOURCE = OUT / "DEVIATOR_TOP_MASTER_RGBA.png"

FRAME = 128
LOGICAL_FRAME = 32
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
# The accepted source points west. Pillow angles below rotate it into the
# engine's established E, NE, N, NW, W, SW, S, SE order.
ANGLES = (180, -135, -90, -45, 0, 45, 90, 135)


def trim(image: Image.Image) -> Image.Image:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise AssertionError("Deviator source is fully transparent")
    return image.crop(bbox)


def centered_master(source: Image.Image) -> Image.Image:
    source = trim(source)
    target_width = 104
    target_height = max(1, round(source.height * target_width / source.width))
    if target_height > 62:
        target_height = 62
        target_width = max(1, round(source.width * target_height / source.height))
    source = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (FRAME, FRAME), (0, 0, 0, 0))
    canvas.alpha_composite(
        source,
        ((FRAME - target_width) // 2, (FRAME - target_height) // 2),
    )
    return canvas


def rotate_frames(master: Image.Image) -> list[Image.Image]:
    return [
        master.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
        for angle in ANGLES
    ]


def house_mask(frame: Image.Image) -> Image.Image:
    rgba = frame.convert("RGBA")
    mask = Image.new("RGBA", rgba.size, (255, 255, 255, 0))
    source = rgba.load()
    target = mask.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = source[x, y]
            if a == 0:
                continue
            # Select the lavender/blue armor only. Tan plates, tracks and
            # acid-green lamps remain neutral and retain their material color.
            blue_bias = b - max(r, g)
            if blue_bias <= 5 or b < 75 or g > b * 1.08:
                continue
            strength = min(230, max(0, 70 + blue_bias * 5))
            target[x, y] = (255, 255, 255, a * strength // 255)
    return mask.filter(ImageFilter.GaussianBlur(0.35))


def shadow(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(2.0))
    opacity = alpha.point(lambda value: value * 92 // 255)
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    silhouette = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    silhouette.putalpha(opacity)
    result.alpha_composite(silhouette, (3, 4))
    return result


def atlas(frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (FRAME * len(frames), FRAME), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        output.alpha_composite(frame, (index * FRAME, 0))
    return output


def review_sheet(frames: list[Image.Image]) -> Image.Image:
    scale = 2
    cell = FRAME * scale
    label_height = 34
    output = Image.new(
        "RGB",
        (cell * 4, (cell + label_height) * 2),
        (20, 22, 25),
    )
    draw = ImageDraw.Draw(output)
    for index, (direction, frame) in enumerate(zip(DIRECTIONS, frames)):
        col = index % 4
        row = index // 4
        x = col * cell
        y = row * (cell + label_height)
        checker = Image.new("RGBA", (FRAME, FRAME), (44, 47, 51, 255))
        checker.alpha_composite(frame)
        output.paste(
            checker.convert("RGB").resize((cell, cell), Image.Resampling.LANCZOS),
            (x, y),
        )
        draw.rectangle((x, y, x + cell - 1, y + cell - 1), outline=(104, 91, 54))
        draw.text((x + 10, y + cell + 8), direction, fill=(238, 218, 151))
    return output


def validate(frames: list[Image.Image], masks: list[Image.Image]) -> dict[str, object]:
    if len(frames) != 8 or len(masks) != 8:
        raise AssertionError("Deviator must contain exactly eight directions")
    if len({frame.tobytes() for frame in frames}) != 8:
        raise AssertionError("Deviator directions are not unique")
    bboxes = [frame.getchannel("A").getbbox() for frame in frames]
    if any(bbox is None for bbox in bboxes):
        raise AssertionError("a Deviator direction is empty")
    for bbox in bboxes:
        assert bbox is not None
        if bbox[0] < 4 or bbox[1] < 4 or bbox[2] > FRAME - 4 or bbox[3] > FRAME - 4:
            raise AssertionError(f"Deviator direction is too close to frame edge: {bbox}")
    coverage = [
        sum(1 for value in frame.getchannel("A").getdata() if value > 16)
        for frame in frames
    ]
    if max(coverage) / min(coverage) > 1.03:
        raise AssertionError("Deviator changes apparent area between directions")
    if any(mask.getchannel("A").getbbox() is None for mask in masks):
        raise AssertionError("a Deviator house mask is empty")
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
    source = Image.open(SOURCE).convert("RGBA")
    master = centered_master(source)
    frames = rotate_frames(master)
    masks = [house_mask(frame) for frame in frames]
    shadows = [shadow(frame) for frame in frames]
    report = validate(frames, masks)

    master.save(OUT / "DEVIATOR_TOP_MASTER_CENTERED_HD4.png", optimize=True)
    atlas(frames).save(OUT / "UNIT_DEVIATOR_HD4_PREVIEW.png", optimize=True)
    atlas(masks).save(OUT / "HM_UNIT_DEVIATOR_HD4_PREVIEW.png", optimize=True)
    atlas(shadows).save(
        OUT / "UNIT_DEVIATOR_SHADOW_HD4_PREVIEW.png", optimize=True
    )
    review_sheet(frames).save(OUT / "UNIT_DEVIATOR_REVIEW_SHEET.png", optimize=True)
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
