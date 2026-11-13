#!/usr/bin/env python3
"""Build the oblique-camera Quad HD4 review atlas from a direction sheet."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "quad_review_v2"
SOURCE = OUT / "QUAD_DIRECTIONS_RGBA.png"

FRAME = 128
LOGICAL_FRAME = 32
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


def largest_component(image: Image.Image) -> Image.Image:
    rgba = np.array(image.convert("RGBA"))
    binary = (rgba[:, :, 3] > 20).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(binary, 8)
    if count <= 1:
        raise AssertionError("Quad cell is empty")
    component = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    rgba[labels != component] = 0
    return Image.fromarray(rgba, "RGBA")


def source_cells(sheet: Image.Image) -> list[Image.Image]:
    width = sheet.width // 4
    height = sheet.height // 2
    cells: list[Image.Image] = []
    for index in range(8):
        x = (index % 4) * width
        y = (index // 4) * height
        cell = largest_component(sheet.crop((x, y, x + width, y + height)))
        bbox = cell.getchannel("A").getbbox()
        if bbox is None:
            raise AssertionError(f"Quad source cell {index} is empty")
        cells.append(cell.crop(bbox))
    return cells


def ordered_sources(cells: list[Image.Image]) -> list[Image.Image]:
    # The generated sheet follows W, SW, S, SE / W, NE, N, NW.  The clean
    # side-on W frame is mirrored for E because the Quad is bilaterally
    # symmetric. This produces the engine contract E..SE without rotating a
    # flat top-down sprite or changing the fixed camera elevation.
    west = cells[4]
    east = west.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return [east, cells[5], cells[6], cells[7], west, cells[1], cells[2], cells[3]]


def normalize_frames(sources: list[Image.Image]) -> list[Image.Image]:
    max_width = max(source.width for source in sources)
    max_height = max(source.height for source in sources)
    scale = min(112 / max_width, 106 / max_height)
    frames: list[Image.Image] = []
    for source in sources:
        width = max(1, round(source.width * scale))
        height = max(1, round(source.height * scale))
        resized = source.resize((width, height), Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", (FRAME, FRAME), (0, 0, 0, 0))
        frame.alpha_composite(resized, ((FRAME - width) // 2, (FRAME - height) // 2))
        frames.append(frame)
    return frames


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
            red_bias = r - max(g, b)
            if red_bias <= 18 or r < 70:
                continue
            strength = min(235, 70 + red_bias * 3)
            target[x, y] = (255, 255, 255, a * strength // 255)
    return output.filter(ImageFilter.GaussianBlur(0.35))


def shadow(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(2.0))
    alpha = alpha.point(lambda value: value * 88 // 255)
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
        x = (index % 4) * cell
        y = (index // 4) * (cell + label_height)
        backdrop = Image.new("RGBA", (FRAME, FRAME), (44, 47, 51, 255))
        backdrop.alpha_composite(frame)
        output.paste(backdrop.convert("RGB").resize((cell, cell), Image.Resampling.LANCZOS), (x, y))
        draw.rectangle((x, y, x + cell - 1, y + cell - 1), outline=(104, 91, 54))
        draw.text((x + 10, y + cell + 8), direction, fill=(238, 218, 151))
    return output


def validate(frames: list[Image.Image], masks: list[Image.Image]) -> dict[str, object]:
    if len(frames) != 8 or len({frame.tobytes() for frame in frames}) != 8:
        raise AssertionError("Quad must contain eight unique directions")
    bboxes = [frame.getchannel("A").getbbox() for frame in frames]
    if any(bbox is None for bbox in bboxes):
        raise AssertionError("a Quad direction is empty")
    for bbox in bboxes:
        assert bbox is not None
        if bbox[0] < 4 or bbox[1] < 4 or bbox[2] > FRAME - 4 or bbox[3] > FRAME - 4:
            raise AssertionError(f"Quad is too close to frame edge: {bbox}")
    if any(mask.getchannel("A").getbbox() is None for mask in masks):
        raise AssertionError("a Quad house mask is empty")
    return {
        "directions": list(DIRECTIONS),
        "logical_frame": [LOGICAL_FRAME, LOGICAL_FRAME],
        "hd4_frame": [FRAME, FRAME],
        "atlas": [FRAME * 8, FRAME],
        "camera": "fixed elevated oblique RTS camera",
        "alpha_bboxes": [list(bbox) for bbox in bboxes if bbox is not None],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cells = source_cells(Image.open(SOURCE).convert("RGBA"))
    frames = normalize_frames(ordered_sources(cells))
    masks = [house_mask(frame) for frame in frames]
    shadows = [shadow(frame) for frame in frames]
    report = validate(frames, masks)

    atlas(frames).save(OUT / "UNIT_QUAD_HD4_PREVIEW.png", optimize=True)
    atlas(masks).save(OUT / "HM_UNIT_QUAD_HD4_PREVIEW.png", optimize=True)
    atlas(shadows).save(OUT / "UNIT_QUAD_SHADOW_HD4_PREVIEW.png", optimize=True)
    review_sheet(frames).save(OUT / "UNIT_QUAD_REVIEW_SHEET.png", optimize=True)
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
