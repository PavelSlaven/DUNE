#!/usr/bin/env python3
"""Normalize HD4 faction masks and install them without changing sprite geometry."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageFilter

from hd_assets import decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data_hd4.dat"
GAME_ROOT = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
GAME_PACK = GAME_ROOT / "data" / "sdl_data_hd4.dat"
MASTER_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
OUTPUT = ROOT / "artifacts" / "faction_masks_uniform_v1"
GAME_BACKUP = GAME_ROOT / "backup_before_uniform_faction_masks_20260806"
HOUSE_COLORS = {
    "Harkonnen": (255, 0, 0),
    "Atreides": (0, 0, 255),
    "Ordos": (0, 255, 0),
}
PREVIEW_NAMES = (
    "UNIT_TANKBASE",
    "UNIT_LAUNCHER",
    "UNIT_MCV",
    "UNIT_DEVASTATOR",
    "UNIT_QUAD",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_mask(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    occupied = alpha.point(lambda value: 255 if value else 0)
    core = occupied.filter(ImageFilter.MinFilter(3))
    solid = Image.new("L", rgba.size, 255)
    normalized_alpha = Image.composite(solid, alpha, core)
    white = Image.new("L", rgba.size, 255)
    return Image.merge("RGBA", (white, white, white, normalized_alpha))


def apply_tint(
    base: Image.Image,
    mask: Image.Image,
    target: tuple[int, int, int],
) -> Image.Image:
    result = base.convert("RGBA").copy()
    source = result.load()
    mask_pixels = mask.convert("RGBA").load()
    luminances = []
    for y in range(result.height):
        for x in range(result.width):
            red, green, blue, alpha = source[x, y]
            mask_red, mask_green, mask_blue, mask_alpha = mask_pixels[x, y]
            strength = (mask_alpha / 255.0) * (
                max(mask_red, mask_green, mask_blue) / 255.0
            )
            if strength >= 0.99 and alpha:
                luminances.append((0.299 * red + 0.587 * green + 0.114 * blue) / 128.0)
    average_luminance = (
        sum(luminances) / len(luminances)
        if luminances
        else 166.0 / 255.0
    )
    correction = (166.0 / 255.0) / max(0.01, average_luminance)
    for y in range(result.height):
        for x in range(result.width):
            red, green, blue, alpha = source[x, y]
            mask_red, mask_green, mask_blue, mask_alpha = mask_pixels[x, y]
            strength = (mask_alpha / 255.0) * (
                max(mask_red, mask_green, mask_blue) / 255.0
            )
            if strength <= 0.0 or alpha == 0:
                continue
            luminance = (0.299 * red + 0.587 * green + 0.114 * blue) / 128.0
            colored = tuple(
                min(255.0, channel * luminance * correction)
                for channel in target
            )
            source[x, y] = (
                int(red * (1.0 - strength) + colored[0] * strength),
                int(green * (1.0 - strength) + colored[1] * strength),
                int(blue * (1.0 - strength) + colored[2] * strength),
                alpha,
            )
    return result


def first_direction(image: Image.Image) -> Image.Image:
    frame_width = image.width // 8
    return image.crop((0, 0, frame_width, image.height))


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (18, 20, 22, 255))
    canvas.alpha_composite(
        copy,
        ((size[0] - copy.width) // 2, (size[1] - copy.height) // 2),
    )
    return canvas


def build_review(entries, normalized: dict[int, Image.Image]) -> Image.Image:
    by_name = {entry.name: entry for entry in entries}
    cell_width = 190
    cell_height = 175
    header = 28
    row_label = 100
    rows = (
        ("Before Ordos", "Ordos", False),
        ("After Ordos", "Ordos", True),
        ("After Atreides", "Atreides", True),
        ("After Harkonnen", "Harkonnen", True),
    )
    review = Image.new(
        "RGB",
        (row_label + cell_width * len(PREVIEW_NAMES), header + cell_height * len(rows)),
        (10, 12, 14),
    )
    draw = ImageDraw.Draw(review)
    for column, name in enumerate(PREVIEW_NAMES):
        draw.text((row_label + column * cell_width + 6, 8), name.removeprefix("UNIT_"), fill=(235, 225, 190))
    for row, (label, house, uniform) in enumerate(rows):
        y = header + row * cell_height
        draw.text((6, y + 70), label, fill=(235, 225, 190))
        for column, name in enumerate(PREVIEW_NAMES):
            base_entry = by_name[name]
            mask_entry = by_name["HM_" + name]
            base = first_direction(decode_image(base_entry.payload))
            original_mask = first_direction(decode_image(mask_entry.payload))
            mask = first_direction(normalized[mask_entry.index]) if uniform else original_mask
            tinted = apply_tint(base, mask, HOUSE_COLORS[house])
            preview = fit(tinted, (cell_width - 8, cell_height - 8))
            review.paste(preview.convert("RGB"), (row_label + column * cell_width + 4, y + 4))
    return review


def build_normalized(entries) -> dict[int, Image.Image]:
    result: dict[int, Image.Image] = {}
    for entry in entries:
        if not entry.name.startswith("HM_"):
            continue
        image = decode_image(entry.payload)
        if image is None:
            raise ValueError(f"cannot decode {entry.name}")
        result[entry.index] = normalize_mask(image)
    return result


def patch_pack(path: Path, normalized: dict[int, Image.Image]) -> None:
    entries = read_pack(path)
    for index, image in normalized.items():
        if not entries[index].name.startswith("HM_"):
            raise AssertionError(f"resource {index} is no longer a faction mask")
        entries[index] = replace(entries[index], extension="PNG", payload=encode_png(image))
    temporary = path.with_suffix(path.suffix + ".uniform-masks.tmp")
    write_pack(temporary, entries)
    os.replace(temporary, path)


def backup_once(entries) -> tuple[Path, Path]:
    source_backup = OUTPUT / "backup" / "source"
    if source_backup.exists() != GAME_BACKUP.exists():
        raise FileExistsError("uniform-mask backup is incomplete")
    if not source_backup.exists():
        source_backup.mkdir(parents=True)
        GAME_BACKUP.mkdir(parents=True)
        shutil.copy2(SOURCE_PACK, source_backup / SOURCE_PACK.name)
        shutil.copy2(GAME_PACK, GAME_BACKUP / GAME_PACK.name)
        master_backup = source_backup / "masters"
        master_backup.mkdir()
        for path in sorted(MASTER_DIR.glob("HM_*.png")) + sorted(MASTER_DIR.glob("HOUSEMASK_*.png")):
            shutil.copy2(path, master_backup / path.name)
    return source_backup, GAME_BACKUP


def update_masters(normalized: dict[int, Image.Image], entries) -> int:
    updated = 0
    by_name = {entry.name: entry for entry in entries}
    for index, image in normalized.items():
        name = entries[index].name
        image.save(MASTER_DIR / f"{name}.png", optimize=True)
        updated += 1
        legacy = MASTER_DIR / f"HOUSEMASK_{name.removeprefix('HM_')}.png"
        if legacy.exists():
            image.save(legacy, optimize=True)
            updated += 1
    for legacy in MASTER_DIR.glob("HOUSEMASK_*.png"):
        modern_name = "HM_" + legacy.stem.removeprefix("HOUSEMASK_")
        if modern_name in by_name:
            continue
        normalize_mask(Image.open(legacy)).save(legacy, optimize=True)
        updated += 1
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    if sha256(SOURCE_PACK) != sha256(GAME_PACK):
        raise AssertionError("source and installed HD4 packs differ before mask normalization")
    entries = read_pack(SOURCE_PACK)
    normalized = build_normalized(entries)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_review(entries, normalized).save(OUTPUT / "FACTION_MASKS_REVIEW.png", optimize=True)

    result: dict[str, object] = {
        "mask_resources": len(normalized),
        "output": str(OUTPUT),
        "installed": False,
    }
    if args.install:
        source_backup, game_backup = backup_once(entries)
        updated_masters = update_masters(normalized, entries)
        patch_pack(SOURCE_PACK, normalized)
        shutil.copy2(SOURCE_PACK, GAME_PACK)
        if sha256(SOURCE_PACK) != sha256(GAME_PACK):
            raise AssertionError("installed HD4 pack differs after mask normalization")
        result.update({
            "installed": True,
            "updated_masters": updated_masters,
            "source_pack_sha256": sha256(SOURCE_PACK),
            "source_backup": str(source_backup),
            "game_backup": str(game_backup),
        })
    (OUTPUT / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
