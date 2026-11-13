#!/usr/bin/env python3
"""Build corrected oblique-camera Deviator and Sonic Tank HD4 atlases."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


@dataclass(frozen=True)
class Asset:
    name: str
    out: Path
    frame: tuple[int, int]
    logical_frame: tuple[int, int]
    sources: Callable[[], list[Image.Image]]
    mask_kind: str


def largest_component(image: Image.Image) -> Image.Image:
    rgba = np.array(image.convert("RGBA"))
    binary = (rgba[:, :, 3] > 20).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(binary, 8)
    if count <= 1:
        raise AssertionError("direction cell is empty")
    component = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    rgba[labels != component] = 0
    output = Image.fromarray(rgba, "RGBA")
    bbox = output.getchannel("A").getbbox()
    if bbox is None:
        raise AssertionError("direction component is empty")
    return output.crop(bbox)


def cells(path: Path, columns: int, rows: int) -> list[Image.Image]:
    sheet = Image.open(path).convert("RGBA")
    width = sheet.width // columns
    height = sheet.height // rows
    output: list[Image.Image] = []
    for index in range(columns * rows):
        x = index % columns * width
        y = index // columns * height
        output.append(largest_component(sheet.crop((x, y, x + width, y + height))))
    return output


def deviator_sources() -> list[Image.Image]:
    out = ROOT / "artifacts" / "deviator_review_v2"
    main = cells(out / "DEVIATOR_MAIN_RGBA.png", 4, 2)
    rear = cells(out / "DEVIATOR_REAR_RGBA.png", 3, 1)
    west = main[4]
    east = west.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return [east, rear[0], rear[1], rear[2], west, main[1], main[2], main[0]]


def sonic_sources() -> list[Image.Image]:
    out = ROOT / "artifacts" / "sonic_tank_review_v2"
    main = cells(out / "SONIC_DIRECTIONS_RGBA.png", 4, 2)
    west = main[4]
    east = west.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    northwest = main[7]
    northeast = northwest.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return [east, northeast, main[6], northwest, west, main[1], main[2], main[0]]


def normalize(sources: list[Image.Image], frame: tuple[int, int]) -> list[Image.Image]:
    frame_width, frame_height = frame
    max_width = max(source.width for source in sources)
    max_height = max(source.height for source in sources)
    scale = min((frame_width - 12) / max_width, (frame_height - 16) / max_height)
    output: list[Image.Image] = []
    for source in sources:
        width = max(1, round(source.width * scale))
        height = max(1, round(source.height * scale))
        resized = source.resize((width, height), Image.Resampling.LANCZOS)
        image = Image.new("RGBA", frame, (0, 0, 0, 0))
        image.alpha_composite(resized, ((frame_width - width) // 2, (frame_height - height) // 2))
        output.append(image)
    return output


def house_mask(frame: Image.Image, kind: str) -> Image.Image:
    rgba = frame.convert("RGBA")
    output = Image.new("RGBA", rgba.size, (255, 255, 255, 0))
    source = rgba.load()
    target = output.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = source[x, y]
            if a == 0:
                continue
            if kind == "blue":
                bias = b - max(r, g)
                selected = b > 65 and bias > 6
            else:
                bias = g - max(r, b)
                selected = g > 65 and bias > 8
            if selected:
                strength = min(230, 70 + max(0, bias) * 4)
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


def atlas(frames: list[Image.Image], frame: tuple[int, int]) -> Image.Image:
    width, height = frame
    output = Image.new("RGBA", (width * 8, height), (0, 0, 0, 0))
    for index, image in enumerate(frames):
        output.alpha_composite(image, (index * width, 0))
    return output


def review_sheet(frames: list[Image.Image], frame: tuple[int, int]) -> Image.Image:
    frame_width, frame_height = frame
    cell_width = max(256, frame_width * 2)
    cell_height = max(256, frame_height * 2)
    label_height = 34
    output = Image.new("RGB", (cell_width * 4, (cell_height + label_height) * 2), (20, 22, 25))
    draw = ImageDraw.Draw(output)
    for index, (direction, image) in enumerate(zip(DIRECTIONS, frames)):
        x = index % 4 * cell_width
        y = index // 4 * (cell_height + label_height)
        backdrop = Image.new("RGBA", frame, (44, 47, 51, 255))
        backdrop.alpha_composite(image)
        rendered = backdrop.convert("RGB").resize((cell_width, cell_height), Image.Resampling.LANCZOS)
        output.paste(rendered, (x, y))
        draw.rectangle((x, y, x + cell_width - 1, y + cell_height - 1), outline=(104, 91, 54))
        draw.text((x + 10, y + cell_height + 8), direction, fill=(238, 218, 151))
    return output


def validate(asset: Asset, frames: list[Image.Image], masks: list[Image.Image]) -> dict[str, object]:
    if len(frames) != 8 or len({image.tobytes() for image in frames}) != 8:
        raise AssertionError(f"{asset.name} must contain eight unique directions")
    bboxes = [image.getchannel("A").getbbox() for image in frames]
    if any(bbox is None for bbox in bboxes):
        raise AssertionError(f"an {asset.name} direction is empty")
    if any(mask.getchannel("A").getbbox() is None for mask in masks):
        raise AssertionError(f"an {asset.name} house mask is empty")
    return {
        "name": asset.name,
        "directions": list(DIRECTIONS),
        "logical_frame": list(asset.logical_frame),
        "hd4_frame": list(asset.frame),
        "atlas": [asset.frame[0] * 8, asset.frame[1]],
        "camera": "fixed elevated oblique RTS camera",
        "alpha_bboxes": [list(bbox) for bbox in bboxes if bbox is not None],
    }


def build(asset: Asset) -> None:
    asset.out.mkdir(parents=True, exist_ok=True)
    frames = normalize(asset.sources(), asset.frame)
    masks = [house_mask(image, asset.mask_kind) for image in frames]
    shadows = [shadow(image) for image in frames]
    report = validate(asset, frames, masks)

    atlas(frames, asset.frame).save(asset.out / f"{asset.name}_HD4_PREVIEW.png", optimize=True)
    atlas(masks, asset.frame).save(asset.out / f"HM_{asset.name}_HD4_PREVIEW.png", optimize=True)
    atlas(shadows, asset.frame).save(asset.out / f"{asset.name}_SHADOW_HD4_PREVIEW.png", optimize=True)
    review_sheet(frames, asset.frame).save(asset.out / f"{asset.name}_REVIEW_SHEET.png", optimize=True)
    (asset.out / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))


def main() -> int:
    build(
        Asset(
            name="UNIT_DEVIATOR",
            out=ROOT / "artifacts" / "deviator_review_v2",
            frame=(128, 128),
            logical_frame=(32, 32),
            sources=deviator_sources,
            mask_kind="blue",
        )
    )
    build(
        Asset(
            name="UNIT_SONICTANK",
            out=ROOT / "artifacts" / "sonic_tank_review_v2",
            frame=(128, 128),
            logical_frame=(32, 32),
            sources=sonic_sources,
            mask_kind="green",
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
