#!/usr/bin/env python3
"""Build volumetric HD mountain atlases without changing autotile masks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont
from scipy import ndimage

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
GAME_DATA = Path(
    "C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru/data"
)
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
OUTPUT = ROOT / "artifacts" / "mountain_relief_review_v1"
SOURCE = OUTPUT / "mountain_material_imagegen.png"
HD4_DIR = OUTPUT / "masters_hd4" / "sdl_data"
HD2_DIR = OUTPUT / "masters_hd2" / "sdl_data"
EXTRA4_DIR = OUTPUT / "extras_hd4" / "sdl_data"
EXTRA2_DIR = OUTPUT / "extras_hd2" / "sdl_data"

RESOURCE_ID = 119
RESOURCE_NAME = "TERRAIN_MOUNTAIN"
VARIANT_NAMES = tuple(
    f"TERRAIN_MOUNTAIN_VAR_{index:02d}" for index in range(1, 5)
)
TILE = 128
FRAME_COUNT = 17
ATLAS_SIZE = (TILE * FRAME_COUNT, TILE)


def classic_frames(resource_id: int) -> list[Image.Image]:
    path = next(CLASSIC.glob(f"{resource_id:04d}_*.png"))
    atlas = Image.open(path).convert("RGB")
    return [
        atlas.crop((left, 0, left + 32, 32))
        for left in range(0, atlas.width, 32)
    ]


def material_center(image: Image.Image) -> np.ndarray:
    array = np.asarray(image.convert("RGB"), dtype=np.float32)
    return np.median(array.reshape(-1, 3), axis=0)


def transition_mask(
    frame: Image.Image,
    background_reference: Image.Image,
    foreground_reference: Image.Image,
) -> np.ndarray:
    enlarged = frame.resize((TILE, TILE), Image.Resampling.NEAREST)
    array = np.asarray(enlarged, dtype=np.float32)
    background = material_center(background_reference)
    foreground = material_center(foreground_reference)
    distance_background = np.linalg.norm(array - background, axis=2)
    distance_foreground = np.linalg.norm(array - foreground, axis=2)
    score = distance_background / np.maximum(
        0.001,
        distance_background + distance_foreground,
    )
    score = np.clip((score - 0.38) / 0.30, 0.0, 1.0)
    score = cv2.GaussianBlur(score.astype(np.float32), (0, 0), 2.1)
    return score * score * (3.0 - 2.0 * score)


def matching_edges(array: np.ndarray, guard: int = 14) -> np.ndarray:
    result = array.astype(np.float32).copy()
    height, width = result.shape[:2]
    for offset in range(guard):
        amount = 1.0 - offset / guard
        left = offset
        right = width - 1 - offset
        average = (result[:, left] + result[:, right]) * 0.5
        result[:, left] = result[:, left] * (1.0 - amount) + average * amount
        result[:, right] = result[:, right] * (1.0 - amount) + average * amount
    for offset in range(guard):
        amount = 1.0 - offset / guard
        top = offset
        bottom = height - 1 - offset
        average = (result[top] + result[bottom]) * 0.5
        result[top] = result[top] * (1.0 - amount) + average * amount
        result[bottom] = (
            result[bottom] * (1.0 - amount) + average * amount
        )
    result = np.clip(result, 0, 255)
    # Lock the final sampling row/column exactly; interpolation above makes
    # the approach gradual, these assignments guarantee a zero-delta seam.
    result[:, -1] = result[:, 0]
    result[-1] = result[0]
    return result


def color_match(source: Image.Image, target: Image.Image) -> Image.Image:
    side = min(source.size)
    source = source.crop(
        (
            (source.width - side) // 2,
            (source.height - side) // 2,
            (source.width + side) // 2,
            (source.height + side) // 2,
        )
    ).resize((TILE, TILE), Image.Resampling.LANCZOS)
    source_array = np.asarray(source.convert("RGB"), dtype=np.float32)
    target_array = np.asarray(target.convert("RGB"), dtype=np.float32)
    source_mean = source_array.reshape(-1, 3).mean(axis=0)
    target_mean = target_array.reshape(-1, 3).mean(axis=0)
    source_std = source_array.reshape(-1, 3).std(axis=0)
    target_std = target_array.reshape(-1, 3).std(axis=0)
    scale = np.clip(target_std / np.maximum(source_std, 1.0), 0.65, 1.15)
    matched = (
        (source_array - source_mean[None, None, :])
        * scale[None, None, :]
        + target_mean[None, None, :]
    )
    # Keep the accepted terrain's low-frequency palette while retaining the
    # ImageGen rock planes that provide the missing micro-relief.
    matched = matched * 0.68 + target_array * 0.32
    matched = matching_edges(matched)
    return Image.fromarray(matched.astype(np.uint8), "RGB")


def edge_safe_variant(base: Image.Image, shift: tuple[int, int]) -> Image.Image:
    base_array = np.asarray(base.convert("RGB"), dtype=np.float32)
    alternate = np.roll(base_array, shift=shift, axis=(0, 1))
    yy, xx = np.mgrid[0:TILE, 0:TILE]
    distance = np.minimum.reduce(
        (xx, yy, TILE - 1 - xx, TILE - 1 - yy)
    ).astype(np.float32)
    blend = np.clip((distance - 15.0) / 22.0, 0.0, 1.0)
    blend = blend * blend * (3.0 - 2.0 * blend)
    result = (
        base_array * (1.0 - blend[..., None])
        + alternate * blend[..., None]
    )
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8), "RGB")


def apply_relief(
    rock: Image.Image,
    mountain: Image.Image,
    mask: np.ndarray,
) -> Image.Image:
    rock_array = np.asarray(rock.convert("RGB"), dtype=np.float32)
    mountain_array = np.asarray(mountain.convert("RGB"), dtype=np.float32)
    mask = np.clip(mask.astype(np.float32), 0.0, 1.0)
    result = (
        rock_array * (1.0 - mask[..., None])
        + mountain_array * mask[..., None]
    )

    # Light comes from upper-left. The plateau therefore gets a thin bright
    # lip on that side, an inner occlusion rim on the opposite side, and a
    # soft cast shadow onto the lower-right rocky ground.
    shifted_down_right = ndimage.shift(
        mask,
        shift=(4.8, 4.8),
        order=1,
        mode="nearest",
    )
    shifted_up_left = ndimage.shift(
        mask,
        shift=(-2.2, -2.2),
        order=1,
        mode="nearest",
    )
    outer_shadow = np.clip(shifted_down_right - mask, 0.0, 1.0)
    outer_shadow = ndimage.gaussian_filter(outer_shadow, 1.8)
    inner_shadow = np.clip(mask - shifted_up_left, 0.0, 1.0)
    inner_shadow = ndimage.gaussian_filter(inner_shadow, 0.85)
    upper_lip = np.clip(mask - shifted_down_right, 0.0, 1.0)
    upper_lip = ndimage.gaussian_filter(upper_lip, 0.65)

    # Do not introduce mismatched pixels at tile borders. Adjacent autotiles
    # keep the exact classic transition there; relief fades in just inside.
    yy, xx = np.mgrid[0:TILE, 0:TILE]
    border_distance = np.minimum.reduce(
        (xx, yy, TILE - 1 - xx, TILE - 1 - yy)
    ).astype(np.float32)
    guard = np.clip((border_distance - 1.0) / 5.0, 0.0, 1.0)
    guard = guard * guard * (3.0 - 2.0 * guard)

    result *= (
        1.0
        - outer_shadow[..., None] * guard[..., None] * 0.52
        - inner_shadow[..., None] * guard[..., None] * 0.24
    )
    result += upper_lip[..., None] * guard[..., None] * 35.0

    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8), "RGB")


def horizontal_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame.convert("RGBA"), (index * TILE, 0))
    return atlas


def build_atlas(
    current: Image.Image,
    mountain: Image.Image,
    masks: list[np.ndarray],
) -> Image.Image:
    rock = current.crop((16 * TILE, 0, 17 * TILE, TILE)).convert("RGB")
    frames = [
        apply_relief(rock, mountain, mask)
        for mask in masks
    ]
    return horizontal_atlas(frames)


def review_sheet(before: Image.Image, after: Image.Image) -> Image.Image:
    columns = 4
    selected = (0, 1, 3, 5, 7, 9, 11, 13, 15, 16)
    margin = 20
    label_height = 34
    width = margin * 2 + columns * TILE
    rows = (len(selected) + columns - 1) // columns
    section_height = label_height + rows * TILE
    sheet = Image.new(
        "RGB",
        (width, margin * 3 + section_height * 2),
        (20, 21, 22),
    )
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    draw = ImageDraw.Draw(sheet)
    for section, (title, atlas) in enumerate(
        (("ДО", before), ("ПОСЛЕ", after))
    ):
        top = margin + section * (section_height + margin)
        draw.text((margin, top), title, fill=(235, 222, 188), font=font)
        for position, frame_index in enumerate(selected):
            x = margin + (position % columns) * TILE
            y = top + label_height + (position // columns) * TILE
            frame = atlas.crop(
                (
                    frame_index * TILE,
                    0,
                    (frame_index + 1) * TILE,
                    TILE,
                )
            ).convert("RGB")
            sheet.paste(frame, (x, y))
            draw.text(
                (x + 4, y + 3),
                str(frame_index),
                fill=(255, 255, 255),
                font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14),
                stroke_width=1,
                stroke_fill=(0, 0, 0),
            )
    return sheet


def validate(
    base4: Image.Image,
    variants4: dict[str, Image.Image],
    base2: Image.Image,
    variants2: dict[str, Image.Image],
    masks: list[np.ndarray],
) -> None:
    if base4.size != ATLAS_SIZE:
        raise AssertionError("HD4 mountain atlas dimensions changed")
    if base2.size != (ATLAS_SIZE[0] // 2, ATLAS_SIZE[1] // 2):
        raise AssertionError("HD2 mountain atlas dimensions changed")
    for name, atlas4 in ((RESOURCE_NAME, base4), *variants4.items()):
        atlas2 = base2 if name == RESOURCE_NAME else variants2[name]
        expected2 = atlas4.resize(atlas2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(atlas2, expected2).getbbox():
            raise AssertionError(f"{name}: HD2 is not the HD4 derivative")
        if atlas4.getchannel("A").getbbox() != (0, 0, *ATLAS_SIZE):
            raise AssertionError(f"{name}: unexpected transparent pixels")

    base_frame = base4.crop((0, 0, TILE, TILE)).convert("RGB")
    array = np.asarray(base_frame)
    if not np.array_equal(array[:, 0], array[:, -1]):
        raise AssertionError("mountain material left/right edges differ")
    if not np.array_equal(array[0], array[-1]):
        raise AssertionError("mountain material top/bottom edges differ")

    frames = [
        np.asarray(
            base4.crop(
                (index * TILE, 0, (index + 1) * TILE, TILE)
            ).convert("RGB")
        )
        for index in range(FRAME_COUNT)
    ]
    for left in range(FRAME_COUNT):
        for right in range(FRAME_COUNT):
            if np.allclose(masks[left][:, -1], masks[right][:, 0]):
                delta = np.abs(
                    frames[left][:, -1].astype(np.int16)
                    - frames[right][:, 0].astype(np.int16)
                )
                if int(delta.max()) > 1:
                    raise AssertionError(
                        f"horizontal seam differs: {left}->{right}"
                    )
            if np.allclose(masks[left][-1], masks[right][0]):
                delta = np.abs(
                    frames[left][-1].astype(np.int16)
                    - frames[right][0].astype(np.int16)
                )
                if int(delta.max()) > 1:
                    raise AssertionError(
                        f"vertical seam differs: {left}->{right}"
                    )


def main() -> int:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    entries = read_pack(GAME_DATA / "sdl_data_hd4.dat")
    by_name = {entry.name: entry for entry in entries}
    current = decode_image(by_name[RESOURCE_NAME].payload)
    if current is None or current.size != ATLAS_SIZE:
        raise AssertionError("installed mountain atlas is unavailable")
    current = current.convert("RGBA")
    current_variants = {
        name: decode_image(by_name[name].payload).convert("RGBA")
        for name in VARIANT_NAMES
    }

    target = current.crop((0, 0, TILE, TILE)).convert("RGB")
    material = color_match(Image.open(SOURCE), target)
    materials = {
        RESOURCE_NAME: material,
        **{
            name: edge_safe_variant(material, shift)
            for name, shift in zip(
                VARIANT_NAMES,
                ((19, -27), (-24, 31), (33, 17), (-35, -21)),
                strict=True,
            )
        },
    }

    mountain_classic = classic_frames(119)
    rock_classic = classic_frames(120)
    masks = []
    for index, frame in enumerate(mountain_classic):
        if index == 0:
            masks.append(np.ones((TILE, TILE), dtype=np.float32))
        elif index == 16:
            masks.append(np.zeros((TILE, TILE), dtype=np.float32))
        else:
            masks.append(
                transition_mask(
                    frame,
                    rock_classic[0],
                    mountain_classic[0],
                )
            )

    base4 = build_atlas(current, materials[RESOURCE_NAME], masks)
    variants4 = {
        name: build_atlas(current_variants[name], materials[name], masks)
        for name in VARIANT_NAMES
    }
    base2 = base4.resize(
        (base4.width // 2, base4.height // 2),
        Image.Resampling.LANCZOS,
    )
    variants2 = {
        name: atlas.resize(
            (atlas.width // 2, atlas.height // 2),
            Image.Resampling.LANCZOS,
        )
        for name, atlas in variants4.items()
    }
    validate(base4, variants4, base2, variants2, masks)

    for folder in (HD4_DIR, HD2_DIR, EXTRA4_DIR, EXTRA2_DIR):
        folder.mkdir(parents=True, exist_ok=True)
    base4.save(HD4_DIR / "0119_TERRAIN_MOUNTAIN.png", optimize=True)
    base2.save(HD2_DIR / "0119_TERRAIN_MOUNTAIN.png", optimize=True)
    for name, atlas in variants4.items():
        atlas.save(EXTRA4_DIR / f"{name}.png", optimize=True)
        variants2[name].save(EXTRA2_DIR / f"{name}.png", optimize=True)
    material.save(OUTPUT / "MOUNTAIN_MATERIAL_HD4.png", optimize=True)
    review_sheet(current, base4).save(
        OUTPUT / "MOUNTAIN_RELIEF_BEFORE_AFTER.png",
        optimize=True,
    )

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "resource_id": RESOURCE_ID,
        "resource_name": RESOURCE_NAME,
        "frames": FRAME_COUNT,
        "hd4_atlas": list(base4.size),
        "hd2_atlas": list(base2.size),
        "variants": list(VARIANT_NAMES),
        "lighting": "upper-left",
        "edge_shadow": "lower-right cast shadow with inner occlusion",
        "imagegen_source": str(SOURCE),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
