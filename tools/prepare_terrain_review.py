#!/usr/bin/env python3
"""Build approval-ready HD terrain atlases from the user material reference."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "terrain_review_v1"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MATERIAL_KIT = OUT / "terrain_material_kit.png"
BLOOM_SOURCE = OUT / "spice_bloom_source.png"
HD4_DIR = OUT / "masters_hd4" / "sdl_data"
HD2_DIR = OUT / "masters_hd2" / "sdl_data"
EXTRA4_DIR = OUT / "extras_hd4" / "sdl_data"
EXTRA2_DIR = OUT / "extras_hd2" / "sdl_data"

TILE = 128
EDGE_GUARD = 12
MATERIAL_NAMES = ("sand", "spice", "rock", "mountain", "slab", "wall")
RESOURCE_NAMES = {
    117: ("TERRAIN_BLOOM", "Цветение пряности"),
    118: ("TERRAIN_HILL", "Песчаные холмы"),
    119: ("TERRAIN_MOUNTAIN", "Горы"),
    120: ("TERRAIN_ROCK", "Каменистая поверхность"),
    121: ("TERRAIN_SAND", "Песок"),
    122: ("TERRAIN_SLAB", "Бетонные плиты"),
    123: ("TERRAIN_SPICE", "Пряность"),
    124: ("TERRAIN_SPICEHILL", "Пряные холмы"),
    125: ("TERRAIN_WALL", "Стены"),
}
VARIANT_RESOURCES = {
    118: "TERRAIN_HILL",
    119: "TERRAIN_MOUNTAIN",
    120: "TERRAIN_ROCK",
    121: "TERRAIN_SAND",
    123: "TERRAIN_SPICE",
    124: "TERRAIN_SPICEHILL",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classic_path(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def classic_frames(resource_id: int) -> list[Image.Image]:
    image = Image.open(classic_path(resource_id)).convert("RGB")
    return [
        image.crop((left, 0, left + 32, 32))
        for left in range(0, image.width, 32)
    ]


def extract_material_swatches() -> dict[str, Image.Image]:
    atlas = Image.open(MATERIAL_KIT).convert("RGB")
    array = np.asarray(atlas)
    magenta = (
        (array[:, :, 0] > 215)
        & (array[:, :, 1] < 70)
        & (array[:, :, 2] > 170)
    )
    labels, count = ndimage.label(~magenta)
    components: list[tuple[int, int, int, int, int]] = []
    for label_id in range(1, count + 1):
        yy, xx = np.nonzero(labels == label_id)
        if xx.size < 50_000:
            continue
        components.append(
            (
                int(xx.min()),
                int(yy.min()),
                int(xx.max()) + 1,
                int(yy.max()) + 1,
                int(xx.size),
            )
        )
    if len(components) != 6:
        raise AssertionError(
            f"expected six material swatches, found {len(components)}"
        )
    components.sort(key=lambda box: (box[1] // 400, box[0]))
    return {
        name: atlas.crop(box[:4])
        for name, box in zip(MATERIAL_NAMES, components, strict=True)
    }


def matching_edges(image: Image.Image, guard: int = 16) -> Image.Image:
    array = np.asarray(image.convert("RGB"), dtype=np.float32).copy()
    height, width = array.shape[:2]
    for offset in range(guard):
        amount = 1.0 - offset / guard
        left = offset
        right = width - 1 - offset
        average = (array[:, left] + array[:, right]) * 0.5
        array[:, left] = array[:, left] * (1.0 - amount) + average * amount
        array[:, right] = array[:, right] * (1.0 - amount) + average * amount
    for offset in range(guard):
        amount = 1.0 - offset / guard
        top = offset
        bottom = height - 1 - offset
        average = (array[top] + array[bottom]) * 0.5
        array[top] = array[top] * (1.0 - amount) + average * amount
        array[bottom] = array[bottom] * (1.0 - amount) + average * amount
    return Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), "RGB")


def material_tile(
    source: Image.Image,
    offset_x: int = 0,
    offset_y: int = 0,
) -> Image.Image:
    side = min(source.size) - 70
    center_x = source.width // 2 + offset_x
    center_y = source.height // 2 + offset_y
    left = max(0, min(source.width - side, center_x - side // 2))
    top = max(0, min(source.height - side, center_y - side // 2))
    crop = source.crop((left, top, left + side, top + side))
    crop = crop.resize((TILE, TILE), Image.Resampling.LANCZOS)
    crop = ImageEnhance.Contrast(crop).enhance(0.88)
    return matching_edges(crop)


def edge_safe_variant(
    base: Image.Image,
    alternate: Image.Image,
) -> Image.Image:
    base_array = np.asarray(base.convert("RGB"), dtype=np.float32)
    alt_array = np.asarray(alternate.convert("RGB"), dtype=np.float32)
    yy, xx = np.mgrid[0:TILE, 0:TILE]
    distance = np.minimum.reduce(
        (xx, yy, TILE - 1 - xx, TILE - 1 - yy)
    ).astype(np.float32)
    blend = np.clip((distance - EDGE_GUARD) / 20.0, 0.0, 1.0)
    blend = blend * blend * (3.0 - 2.0 * blend)
    blend = blend[..., None]
    result = base_array * (1.0 - blend) + alt_array * blend
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8), "RGB")


def classic_material_center(image: Image.Image) -> np.ndarray:
    array = np.asarray(image.convert("RGB"), dtype=np.float32)
    return np.median(array.reshape(-1, 3), axis=0)


def transition_mask(
    frame: Image.Image,
    background_reference: Image.Image,
    foreground_reference: Image.Image,
    blur: float = 2.1,
) -> Image.Image:
    enlarged = frame.resize((TILE, TILE), Image.Resampling.NEAREST)
    array = np.asarray(enlarged, dtype=np.float32)
    background = classic_material_center(background_reference)
    foreground = classic_material_center(foreground_reference)
    distance_background = np.linalg.norm(array - background, axis=2)
    distance_foreground = np.linalg.norm(array - foreground, axis=2)
    score = distance_background / np.maximum(
        0.001,
        distance_background + distance_foreground,
    )
    score = np.clip((score - 0.38) / 0.30, 0.0, 1.0)
    score = cv2.GaussianBlur(score.astype(np.float32), (0, 0), blur)
    score = score * score * (3.0 - 2.0 * score)
    return Image.fromarray(
        np.round(np.clip(score, 0.0, 1.0) * 255).astype(np.uint8),
        "L",
    )


def relief_frame(
    material: Image.Image,
    classic_frame: Image.Image,
    strength: float,
) -> Image.Image:
    gray = np.asarray(
        classic_frame.resize((TILE, TILE), Image.Resampling.BICUBIC)
        .convert("L"),
        dtype=np.float32,
    )
    broad = cv2.GaussianBlur(gray, (0, 0), 5.2)
    broad -= float(np.median(broad))
    maximum = max(1.0, float(np.max(np.abs(broad))))
    relief = 1.0 + broad / maximum * strength
    array = np.asarray(material.convert("RGB"), dtype=np.float32)
    result = array * relief[..., None]
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8), "RGB")


def composite(
    background: Image.Image,
    foreground: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    return Image.composite(
        foreground.convert("RGB"),
        background.convert("RGB"),
        mask,
    )


def spice_hill_material(
    mountain: Image.Image,
    spice: Image.Image,
) -> Image.Image:
    spice_array = np.asarray(spice.convert("RGB"), dtype=np.uint8)
    dark = tuple(
        int(value)
        for value in np.percentile(spice_array.reshape(-1, 3), 18, axis=0)
    )
    light = tuple(
        int(value)
        for value in np.percentile(spice_array.reshape(-1, 3), 82, axis=0)
    )
    colored = ImageOps.colorize(mountain.convert("L"), dark, light)
    return ImageEnhance.Contrast(colored).enhance(1.08)


def bloom_tile(sand: Image.Image) -> Image.Image:
    source = Image.open(BLOOM_SOURCE).convert("RGB")
    # ImageGen deliberately left a wide clean-sand margin around the bloom.
    # Crop the central third so the hazard keeps the readable footprint of
    # the classic 32x32 sprite instead of shrinking to a nearly invisible dot.
    side = max(1, min(source.size) // 3)
    source = source.crop(
        (
            (source.width - side) // 2,
            (source.height - side) // 2,
            (source.width + side) // 2,
            (source.height + side) // 2,
        )
    ).resize((TILE, TILE), Image.Resampling.LANCZOS)
    source_array = np.asarray(source, dtype=np.float32)
    sand_array = np.asarray(sand, dtype=np.float32)
    border = np.concatenate(
        (
            source_array[:14].reshape(-1, 3),
            source_array[-14:].reshape(-1, 3),
            source_array[:, :14].reshape(-1, 3),
            source_array[:, -14:].reshape(-1, 3),
        )
    )
    correction = np.mean(sand_array.reshape(-1, 3), axis=0) - np.mean(
        border,
        axis=0,
    )
    source_array = np.clip(source_array + correction, 0, 255)
    yy, xx = np.mgrid[0:TILE, 0:TILE]
    radius = np.sqrt((xx - 63.5) ** 2 + (yy - 63.5) ** 2)
    mask = np.clip((53.0 - radius) / 22.0, 0.0, 1.0)
    mask = mask * mask * (3.0 - 2.0 * mask)
    result = (
        sand_array * (1.0 - mask[..., None])
        + source_array * mask[..., None]
    )
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8), "RGB")


def build_materials() -> tuple[dict[str, Image.Image], dict[str, Image.Image]]:
    swatches = extract_material_swatches()
    bases = {
        name: material_tile(source)
        for name, source in swatches.items()
    }
    bases["spicehill"] = spice_hill_material(
        bases["mountain"],
        bases["spice"],
    )
    variants: dict[str, Image.Image] = {}
    offsets = ((-38, 31), (34, -29), (-23, -37), (39, 34))
    for name, source in swatches.items():
        if name not in {"sand", "spice", "rock", "mountain"}:
            continue
        for index, (offset_x, offset_y) in enumerate(offsets, start=1):
            alternate = material_tile(source, offset_x, offset_y)
            variants[f"{name}_{index}"] = edge_safe_variant(
                bases[name],
                alternate,
            )
    for index in range(1, 5):
        variants[f"spicehill_{index}"] = spice_hill_material(
            variants[f"mountain_{index}"],
            variants[f"spice_{index}"],
        )
        variants[f"spicehill_{index}"] = edge_safe_variant(
            bases["spicehill"],
            variants[f"spicehill_{index}"],
        )
    return bases, variants


def build_atlases(
    materials: dict[str, Image.Image],
) -> tuple[dict[int, Image.Image], dict[int, list[Image.Image]]]:
    classic = {
        resource_id: classic_frames(resource_id)
        for resource_id in RESOURCE_NAMES
    }
    atlases: dict[int, Image.Image] = {}
    masks: dict[int, list[Image.Image]] = {}

    atlases[117] = bloom_tile(materials["sand"]).convert("RGBA")

    hill_frames = [
        relief_frame(materials["sand"], frame, 0.12).convert("RGBA")
        for frame in classic[118]
    ]
    atlases[118] = horizontal_atlas(hill_frames)

    transition_specs = {
        119: (120, 119, "rock", "mountain", {0: 255, 16: 0}),
        120: (121, 120, "sand", "rock", {0: 255}),
        123: (121, 123, "sand", "spice", {0: 255}),
        124: (123, 124, "spice", "spicehill", {0: 255}),
        125: (121, 125, "sand", "wall", {}),
    }
    for resource_id, (
        background_id,
        foreground_id,
        background_name,
        foreground_name,
        forced,
    ) in transition_specs.items():
        resource_masks: list[Image.Image] = []
        frames: list[Image.Image] = []
        for index, frame in enumerate(classic[resource_id]):
            if index in forced:
                mask = Image.new("L", (TILE, TILE), forced[index])
            else:
                mask = transition_mask(
                    frame,
                    classic[background_id][0],
                    classic[foreground_id][0],
                    blur=0.9 if resource_id == 125 else 2.1,
                )
            rebuilt = composite(
                materials[background_name],
                materials[foreground_name],
                mask,
            )
            frames.append(rebuilt.convert("RGBA"))
            resource_masks.append(mask)
        atlases[resource_id] = horizontal_atlas(frames)
        masks[resource_id] = resource_masks

    slab_frames = [
        relief_frame(
            material_tile(
                extract_material_swatches()["slab"],
                (index - 2) * 19,
                (2 - index) * 13,
            ),
            frame,
            0.035,
        ).convert("RGBA")
        for index, frame in enumerate(classic[122])
    ]
    atlases[122] = horizontal_atlas(slab_frames)
    atlases[121] = materials["sand"].convert("RGBA")
    return atlases, masks


def horizontal_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", (len(frames) * TILE, TILE), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame.convert("RGBA"), (index * TILE, 0))
    return atlas


def build_variant_atlas(
    base_atlas: Image.Image,
    replacement_frame: Image.Image,
) -> Image.Image:
    result = base_atlas.copy()
    result.paste(replacement_frame.convert("RGBA"), (0, 0))
    return result


def save_assets(
    atlases: dict[int, Image.Image],
    materials: dict[str, Image.Image],
    variants: dict[str, Image.Image],
) -> dict[int, list[Path]]:
    for folder in (HD4_DIR, HD2_DIR, EXTRA4_DIR, EXTRA2_DIR):
        folder.mkdir(parents=True, exist_ok=True)
    saved: dict[int, list[Path]] = {}
    for resource_id, atlas in atlases.items():
        filename = classic_path(resource_id).name
        hd4_path = HD4_DIR / filename
        hd2_path = HD2_DIR / filename
        atlas.save(hd4_path, optimize=True)
        atlas.resize(
            (atlas.width // 2, atlas.height // 2),
            Image.Resampling.LANCZOS,
        ).save(hd2_path, optimize=True)
        saved[resource_id] = [hd4_path, hd2_path]

    material_by_resource = {
        118: "sand",
        119: "mountain",
        120: "rock",
        121: "sand",
        123: "spice",
        124: "spicehill",
    }
    for resource_id, resource_name in VARIANT_RESOURCES.items():
        material_name = material_by_resource[resource_id]
        base_frame = atlases[resource_id].crop((0, 0, TILE, TILE))
        for index in range(1, 5):
            candidate = variants[f"{material_name}_{index}"]
            if resource_id == 118:
                candidate = relief_frame(
                    candidate,
                    classic_frames(118)[0],
                    0.12,
                )
                candidate = edge_safe_variant(base_frame, candidate)
            variant_atlas = build_variant_atlas(
                atlases[resource_id],
                candidate,
            )
            filename = f"{resource_name}_VAR_{index:02d}.png"
            variant_atlas.save(EXTRA4_DIR / filename, optimize=True)
            variant_atlas.resize(
                (
                    variant_atlas.width // 2,
                    variant_atlas.height // 2,
                ),
                Image.Resampling.LANCZOS,
            ).save(EXTRA2_DIR / filename, optimize=True)
    return saved


def validate(
    atlases: dict[int, Image.Image],
    saved: dict[int, list[Path]],
) -> dict[str, object]:
    records: dict[str, object] = {}
    for resource_id, atlas in atlases.items():
        classic = Image.open(classic_path(resource_id))
        expected = (classic.width * 4, classic.height * 4)
        if atlas.size != expected:
            raise AssertionError(
                f"{resource_id}: expected {expected}, got {atlas.size}"
            )
        if atlas.getchannel("A").getbbox() != (0, 0, *atlas.size):
            raise AssertionError(f"{resource_id}: atlas is not fully opaque")
        hd2 = Image.open(saved[resource_id][1]).convert("RGBA")
        expected2 = atlas.resize(hd2.size, Image.Resampling.LANCZOS)
        if np.any(
            np.asarray(hd2, dtype=np.int16)
            != np.asarray(expected2, dtype=np.int16)
        ):
            raise AssertionError(
                f"{resource_id}: HD2 is not the exact HD4 derivative"
            )
        records[str(resource_id)] = {
            "name": RESOURCE_NAMES[resource_id][0],
            "frames": classic.width // 32,
            "logical_size": list(classic.size),
            "hd4_size": list(atlas.size),
            "hd2_size": list(hd2.size),
            "hd4_sha256": sha256(saved[resource_id][0]),
            "hd2_sha256": sha256(saved[resource_id][1]),
        }

    for resource_id, resource_name in VARIANT_RESOURCES.items():
        base = atlases[resource_id].crop((0, 0, TILE, TILE))
        base_array = np.asarray(base)
        for index in range(1, 5):
            path = EXTRA4_DIR / f"{resource_name}_VAR_{index:02d}.png"
            variant = Image.open(path).convert("RGBA").crop(
                (0, 0, TILE, TILE)
            )
            array = np.asarray(variant)
            if not (
                np.array_equal(
                    array[:EDGE_GUARD],
                    base_array[:EDGE_GUARD],
                )
                and np.array_equal(
                    array[-EDGE_GUARD:],
                    base_array[-EDGE_GUARD:],
                )
                and np.array_equal(
                    array[:, :EDGE_GUARD],
                    base_array[:, :EDGE_GUARD],
                )
                and np.array_equal(
                    array[:, -EDGE_GUARD:],
                    base_array[:, -EDGE_GUARD:],
                )
            ):
                raise AssertionError(
                    f"{resource_name} variant {index} changed a seam edge"
                )
    return records


def labeled_review(atlases: dict[int, Image.Image]) -> Path:
    display_tile = 82
    gap = 5
    width = 1660
    top = 110
    row_heights: dict[int, int] = {}
    for resource_id, atlas in atlases.items():
        count = atlas.width // TILE
        lines = (count + 15) // 16
        row_heights[resource_id] = 58 + lines * (display_tile + 26)
    height = top + sum(row_heights.values()) + 90
    sheet = Image.new("RGBA", (width, height), (10, 12, 14, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text(
        (34, 24),
        "ПОВЕРХНОСТЬ D2TM — РАЗМЕЧЕННЫЙ HD4-АТЛАС",
        font=font(32, True),
        fill=(241, 222, 178, 255),
    )
    draw.text(
        (34, 67),
        "Кадр 128×128; порядок и количество кадров полностью повторяют классический атлас.",
        font=font(18),
        fill=(180, 187, 185, 255),
    )
    y = top
    for resource_id in RESOURCE_NAMES:
        atlas = atlases[resource_id]
        name, russian = RESOURCE_NAMES[resource_id]
        count = atlas.width // TILE
        draw.rounded_rectangle(
            (24, y, width - 24, y + row_heights[resource_id] - 10),
            radius=12,
            fill=(24, 27, 29, 255),
            outline=(145, 111, 45, 255),
            width=2,
        )
        draw.text(
            (42, y + 14),
            f"ID {resource_id}  {name} — {russian} — {count} кадр.",
            font=font(20, True),
            fill=(234, 221, 191, 255),
        )
        for index in range(count):
            column = index % 16
            line = index // 16
            x = 42 + column * (display_tile + gap)
            frame_y = y + 55 + line * (display_tile + 26)
            frame = atlas.crop(
                (
                    index * TILE,
                    0,
                    (index + 1) * TILE,
                    TILE,
                )
            ).resize((display_tile, display_tile), Image.Resampling.LANCZOS)
            sheet.alpha_composite(frame, (x, frame_y))
            draw.rectangle(
                (x, frame_y, x + display_tile, frame_y + display_tile),
                outline=(91, 96, 94, 255),
                width=1,
            )
            draw.text(
                (x + 3, frame_y + display_tile + 3),
                str(index),
                font=font(14, True),
                fill=(223, 226, 222, 255),
            )
        y += row_heights[resource_id]
    draw.text(
        (34, height - 50),
        "СТАТУС: ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР — В ИГРУ НЕ УСТАНОВЛЕНО",
        font=font(20, True),
        fill=(233, 101, 80, 255),
    )
    output = OUT / "TERRAIN_HD4_LABELED_REVIEW.png"
    sheet.convert("RGB").save(output, quality=94)
    return output


def material_review(
    materials: dict[str, Image.Image],
    variants: dict[str, Image.Image],
) -> Path:
    names = (
        ("sand", "Песок"),
        ("spice", "Пряность"),
        ("rock", "Камень"),
        ("mountain", "Горная порода"),
        ("slab", "Плиты"),
        ("wall", "Стена"),
    )
    sheet = Image.new("RGBA", (1440, 920), (11, 13, 15, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text(
        (34, 24),
        "МАТЕРИАЛЫ И БЕСШОВНЫЕ ВАРИАНТЫ",
        font=font(31, True),
        fill=(241, 222, 178, 255),
    )
    for index, (name, label) in enumerate(names):
        row = index // 3
        column = index % 3
        x = 34 + column * 464
        y = 88 + row * 386
        draw.rounded_rectangle(
            (x, y, x + 430, y + 354),
            radius=12,
            fill=(24, 27, 29, 255),
            outline=(145, 111, 45, 255),
            width=2,
        )
        draw.text(
            (x + 16, y + 12),
            label,
            font=font(21, True),
            fill=(234, 221, 191, 255),
        )
        tile = materials[name]
        mosaic = Image.new("RGBA", (384, 256))
        variant_names = [name] + [
            f"{name}_{variant_index}"
            for variant_index in range(1, 5)
            if f"{name}_{variant_index}" in variants
        ]
        for tile_y in range(2):
            for tile_x in range(3):
                selected = variant_names[
                    (tile_y * 3 + tile_x) % len(variant_names)
                ]
                image = (
                    materials[selected]
                    if selected in materials
                    else variants[selected]
                )
                mosaic.alpha_composite(
                    image.convert("RGBA"),
                    (tile_x * 128, tile_y * 128),
                )
        sheet.alpha_composite(mosaic, (x + 23, y + 58))
        draw.text(
            (x + 16, y + 326),
            "стыки показаны без рамок",
            font=font(15),
            fill=(166, 173, 171, 255),
        )
    output = OUT / "TERRAIN_MATERIALS_AND_SEAMS.png"
    sheet.convert("RGB").save(output, quality=94)
    return output


def main() -> None:
    for path in (MATERIAL_KIT, BLOOM_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    materials, variants = build_materials()
    atlases, masks = build_atlases(materials)
    saved = save_assets(atlases, materials, variants)
    records = validate(atlases, saved)
    atlas_review = labeled_review(atlases)
    materials_review = material_review(materials, variants)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str((OUT / "user_reference.png").relative_to(ROOT)),
        "generated_material_kit": str(MATERIAL_KIT.relative_to(ROOT)),
        "generated_bloom_source": str(BLOOM_SOURCE.relative_to(ROOT)),
        "tile_contract": {
            "logical": [32, 32],
            "hd2": [64, 64],
            "hd4": [128, 128],
            "transition_topology": "classic atlas frame masks",
            "variant_edge_guard_hd4": EDGE_GUARD,
        },
        "resources": records,
        "variants": {
            RESOURCE_NAMES[resource_id][0]: 4
            for resource_id in VARIANT_RESOURCES
        },
        "transition_masks": {
            str(resource_id): len(resource_masks)
            for resource_id, resource_masks in masks.items()
        },
        "reviews": [
            str(atlas_review.relative_to(ROOT)),
            str(materials_review.relative_to(ROOT)),
        ],
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
