#!/usr/bin/env python3
"""Build and optionally install the user-supplied HD4 launcher atlas."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from dataclasses import replace
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

from hd_assets import decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(r"C:\Users\Slaven\Downloads\Ракетная установка.png")
GAME_ROOT = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
OUTPUT = ROOT / "artifacts" / "launcher_user_reference_v2"

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
FRAME_SIZE = 128
ATLAS_SIZE = (FRAME_SIZE * len(DIRECTIONS), FRAME_SIZE)
RESOURCE_IDS = {
    139: "UNIT_LAUNCHER",
    140: "UNIT_LAUNCHER_SHADOW",
    179: "HM_UNIT_LAUNCHER",
}
HOUSE_COLORS = {
    "Atreides": (30, 105, 245),
    "Harkonnen": (235, 28, 28),
    "Ordos": (20, 220, 70),
}
DIRECTION_SCALES = {
    "E": 1.06,
    "N": 0.86,
    "W": 1.04,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def smoothstep(low: float, high: float, value: np.ndarray) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def largest_component(mask: np.ndarray) -> np.ndarray:
    labels, count = ndimage.label(mask)
    if count < 1:
        raise AssertionError("launcher extraction is empty")
    sizes = ndimage.sum(mask, labels, range(1, count + 1))
    return labels == int(np.argmax(sizes)) + 1


def extract_subject(source: Image.Image) -> Image.Image:
    rgba = np.asarray(source.convert("RGBA"), dtype=np.uint8)
    rgb = rgba[:, :, :3]
    height, width = rgb.shape[:2]
    pad = max(24, round(min(width, height) * 0.055))
    padded = cv2.copyMakeBorder(
        rgb,
        pad,
        pad,
        pad,
        pad,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )
    padded_alpha = cv2.copyMakeBorder(
        rgba[:, :, 3],
        pad,
        pad,
        pad,
        pad,
        cv2.BORDER_CONSTANT,
        value=0,
    )
    mask = np.full(padded.shape[:2], cv2.GC_PR_BGD, dtype=np.uint8)
    mask[:pad, :] = cv2.GC_BGD
    mask[-pad:, :] = cv2.GC_BGD
    mask[:, :pad] = cv2.GC_BGD
    mask[:, -pad:] = cv2.GC_BGD
    mask[padded_alpha == 0] = cv2.GC_BGD

    hsv = cv2.cvtColor(padded, cv2.COLOR_RGB2HSV)
    value = hsv[:, :, 2]
    saturation = hsv[:, :, 1]
    # The reference uses bright sandstone paint over a nearly black studio
    # background. These seeds identify the vehicle without declaring its dark
    # tracks, vents, or windows to be background.
    foreground_seed = (
        (value > 62)
        | ((value > 42) & (saturation > 24))
    ) & (padded_alpha > 0)
    foreground_seed = ndimage.binary_erosion(foreground_seed, iterations=1)
    mask[foreground_seed] = cv2.GC_FGD

    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(
        cv2.cvtColor(padded, cv2.COLOR_RGB2BGR),
        mask,
        None,
        background_model,
        foreground_model,
        7,
        cv2.GC_INIT_WITH_MASK,
    )
    solid = (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)
    solid = largest_component(solid)
    solid = ndimage.binary_closing(solid, iterations=1)
    soft = ndimage.gaussian_filter(solid.astype(np.float32), 0.72)
    alpha = np.clip(soft * 255.0, 0, 255).astype(np.uint8)

    extracted = np.dstack((padded, alpha))[pad:-pad, pad:-pad]
    extracted[extracted[:, :, 3] == 0, :3] = 0
    return Image.fromarray(extracted, "RGBA")


def normalize_frame(image: Image.Image, scale_multiplier: float = 1.0) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("launcher frame is empty")
    subject = image.crop(box)
    scale = min(116 / subject.width, 116 / subject.height) * scale_multiplier
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    frame.alpha_composite(
        subject,
        ((FRAME_SIZE - size[0]) // 2, (FRAME_SIZE - size[1]) // 2),
    )
    return frame


def build_colored_atlas(source: Image.Image) -> tuple[Image.Image, list[Image.Image]]:
    if source.width % len(DIRECTIONS) != 0:
        raise ValueError(
            f"source width {source.width} is not divisible by {len(DIRECTIONS)}"
        )
    source_frame_width = source.width // len(DIRECTIONS)
    atlas = Image.new("RGBA", ATLAS_SIZE)
    frames = []
    for index, direction in enumerate(DIRECTIONS):
        crop = source.crop(
            (
                index * source_frame_width,
                0,
                (index + 1) * source_frame_width,
                source.height,
            )
        )
        frame = normalize_frame(
            extract_subject(crop),
            DIRECTION_SCALES.get(direction, 1.0),
        )
        atlas.alpha_composite(frame, (index * FRAME_SIZE, 0))
        frames.append(frame)
        if frame.getchannel("A").getbbox() is None:
            raise AssertionError(f"empty direction: {direction}")
    return atlas, frames


def neutral_and_mask(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    maximum = np.maximum(np.maximum(red, green), blue)
    minimum = np.minimum(np.minimum(red, green), blue)
    saturation = (maximum - minimum) / np.maximum(maximum, 1.0)
    warmth = (red - blue) / 255.0
    sand_balance = (green - blue) / 255.0
    selection = (
        smoothstep(0.045, 0.22, warmth)
        * smoothstep(0.012, 0.12, sand_balance)
        * smoothstep(0.045, 0.22, saturation)
        * smoothstep(34.0, 104.0, maximum)
        * (alpha / 255.0)
    )
    # Keep faction colour as readable armour accents instead of replacing the
    # whole sandstone vehicle with a flat, neon house colour.
    selection = np.clip(selection * 0.58, 0.0, 0.58)

    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    neutral_rgb = np.dstack(
        (luminance * 0.76, luminance * 0.80, luminance * 0.86)
    )
    amount = (selection * 0.82)[:, :, None]
    neutral = rgba.copy()
    neutral[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - amount) + neutral_rgb * amount
    )
    neutral[alpha == 0] = 0

    mask_alpha = np.clip(selection * 255.0, 0, 255).astype(np.uint8)
    mask_rgba = np.full((*mask_alpha.shape, 4), 255, dtype=np.uint8)
    mask_rgba[:, :, 3] = mask_alpha
    mask_rgba[mask_alpha == 0, :3] = 0
    return (
        Image.fromarray(np.clip(neutral, 0, 255).astype(np.uint8), "RGBA"),
        Image.fromarray(mask_rgba, "RGBA"),
    )


def atlas_frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop(
        (index * FRAME_SIZE, 0, (index + 1) * FRAME_SIZE, FRAME_SIZE)
    )


def build_shadow(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", ATLAS_SIZE)
    for index in range(len(DIRECTIONS)):
        frame = atlas_frame(atlas, index)
        alpha = frame.getchannel("A").filter(
            ImageFilter.GaussianBlur(1.7)
        ).point(lambda value: round(value * 0.22))
        shadow = Image.new("RGBA", frame.size, (7, 6, 5, 0))
        shadow.putalpha(alpha)
        shifted = Image.new("RGBA", frame.size)
        shifted.alpha_composite(shadow, (2, 3))
        result.alpha_composite(shifted, (index * FRAME_SIZE, 0))
    return result


def apply_tint(
    image: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32).copy()
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    strength = (
        mask_rgba[:, :, 3] / 255.0
        * np.max(mask_rgba[:, :, :3], axis=2) / 255.0
    )
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        colored = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - strength)
            + colored * strength
        )
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def checker(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGBA", size, (48, 52, 58, 255))
    draw = ImageDraw.Draw(image)
    step = 16
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle(
                    (x, y, x + step - 1, y + step - 1),
                    fill=(72, 76, 82, 255),
                )
    return image


def build_review(
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
    shadow: Image.Image,
) -> Image.Image:
    rows = {
        "Source": colored,
        "Neutral": neutral,
        "Atreides": apply_tint(neutral, mask, HOUSE_COLORS["Atreides"]),
        "Harkonnen": apply_tint(neutral, mask, HOUSE_COLORS["Harkonnen"]),
        "Ordos": apply_tint(neutral, mask, HOUSE_COLORS["Ordos"]),
        "Mask": mask,
        "Shadow": shadow,
    }
    cell = 150
    label_width = 160
    header = 88
    board = Image.new(
        "RGBA",
        (label_width + cell * len(DIRECTIONS), header + cell * len(rows)),
        (14, 17, 22, 255),
    )
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 19)
    bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 21)
    draw.text(
        (14, 12),
        "New rocket launcher — HD4 production preview",
        font=bold,
        fill=(239, 221, 180, 255),
    )
    for column, direction in enumerate(DIRECTIONS):
        x = label_width + column * cell
        text_box = draw.textbbox((0, 0), direction, font=font)
        draw.text(
            (x + (cell - (text_box[2] - text_box[0])) // 2, 52),
            direction,
            font=font,
            fill=(220, 224, 230, 255),
        )
    for row, (name, atlas) in enumerate(rows.items()):
        y = header + row * cell
        draw.text((12, y + 62), name, font=bold, fill=(235, 220, 188, 255))
        for column in range(len(DIRECTIONS)):
            x = label_width + column * cell
            tile = checker((cell, cell))
            frame = atlas_frame(atlas, column).resize(
                (cell, cell), Image.Resampling.LANCZOS
            )
            tile.alpha_composite(frame)
            board.alpha_composite(tile, (x, y))
            draw.rectangle(
                (x, y, x + cell - 1, y + cell - 1),
                outline=(139, 106, 50, 255),
            )
    return board


def validate(atlas: Image.Image, mask: Image.Image, shadow: Image.Image) -> dict:
    result = {"directions": list(DIRECTIONS), "frames": {}}
    visible_areas: dict[str, int] = {}
    for name, image in (("atlas", atlas), ("mask", mask), ("shadow", shadow)):
        if image.size != ATLAS_SIZE:
            raise AssertionError(f"{name}: expected {ATLAS_SIZE}, got {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is empty")
    for index, direction in enumerate(DIRECTIONS):
        frame = atlas_frame(atlas, index)
        box = frame.getchannel("A").getbbox()
        if box is None or box[0] < 2 or box[1] < 2 or box[2] > 126 or box[3] > 126:
            raise AssertionError(f"{direction} touches frame boundary: {box}")
        alpha = np.asarray(frame.getchannel("A"), dtype=np.uint8)
        opaque = alpha > 24
        visible_areas[direction] = int(opaque.sum())
        component = largest_component(opaque)
        coverage = float(component.sum() / max(1, opaque.sum()))
        if coverage < 0.985:
            raise AssertionError(
                f"{direction} contains detached extraction artifacts: {coverage:.4f}"
            )
        result["frames"][direction] = {
            "bbox": list(box),
            "connected_coverage": round(coverage, 5),
            "visible_area": visible_areas[direction],
        }
    comparison_areas = [
        area for direction, area in visible_areas.items() if direction != "N"
    ]
    median_area = float(np.median(comparison_areas))
    north_ratio = visible_areas["N"] / median_area
    if north_ratio > 1.12:
        raise AssertionError(
            f"N frame is visually oversized: area ratio {north_ratio:.3f}"
        )
    result["north_area_ratio"] = round(north_ratio, 5)
    side_comparison = float(np.median([
        area
        for direction, area in visible_areas.items()
        if direction not in ("E", "W")
    ]))
    side_ratios = {
        direction: visible_areas[direction] / side_comparison
        for direction in ("E", "W")
    }
    undersized = {
        direction: ratio
        for direction, ratio in side_ratios.items()
        if ratio < 0.92
    }
    if undersized:
        details = ", ".join(
            f"{direction}={ratio:.3f}"
            for direction, ratio in undersized.items()
        )
        raise AssertionError(f"side frames are visually undersized: {details}")
    result["side_area_ratios"] = {
        direction: round(ratio, 5)
        for direction, ratio in side_ratios.items()
    }
    mask_pixels = int(
        np.count_nonzero(np.asarray(mask.getchannel("A"), dtype=np.uint8) > 8)
    )
    if mask_pixels < 1200:
        raise AssertionError(f"house mask is unexpectedly small: {mask_pixels}")
    result["mask_pixels"] = mask_pixels
    return result


def save_outputs(
    source: Path,
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
    shadow: Image.Image,
    validation: dict,
) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, OUTPUT / "user_reference.png")
    colored.save(OUTPUT / "UNIT_LAUNCHER_COLORED_SOURCE_HD4.png", optimize=True)
    neutral.save(OUTPUT / "UNIT_LAUNCHER_HD4.png", optimize=True)
    mask.save(OUTPUT / "HM_UNIT_LAUNCHER_HD4.png", optimize=True)
    shadow.save(OUTPUT / "UNIT_LAUNCHER_SHADOW_HD4.png", optimize=True)
    for house, color in HOUSE_COLORS.items():
        apply_tint(neutral, mask, color).save(
            OUTPUT / f"UNIT_LAUNCHER_{house.upper()}_HD4.png",
            optimize=True,
        )
    build_review(colored, neutral, mask, shadow).save(
        OUTPUT / "UNIT_LAUNCHER_REVIEW.png", optimize=True
    )
    (OUTPUT / "validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def patch_pack(path: Path, atlas: Image.Image, shadow: Image.Image, mask: Image.Image) -> None:
    entries = read_pack(path)
    replacements = {139: atlas, 140: shadow, 179: mask}
    for resource_id, expected_name in RESOURCE_IDS.items():
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"{path}: ID {resource_id} is {entries[resource_id].name}, expected {expected_name}"
            )
        entries[resource_id] = replace(
            entries[resource_id],
            extension="PNG",
            payload=encode_png(replacements[resource_id]),
        )
    temporary = path.with_suffix(path.suffix + ".launcher-v2.tmp")
    write_pack(temporary, entries)
    packed = read_pack(temporary)
    for resource_id, expected in replacements.items():
        image = decode_image(packed[resource_id].payload)
        if image is None or image.size != expected.size:
            raise AssertionError(f"packed resource {resource_id} is invalid")
    os.replace(temporary, path)


def install(neutral: Image.Image, mask: Image.Image, shadow: Image.Image) -> dict:
    source_pack = ROOT / "resources" / "bin" / "data" / "sdl_data_hd4.dat"
    game_pack = GAME_ROOT / "data" / "sdl_data_hd4.dat"
    if sha256(source_pack) != sha256(game_pack):
        raise AssertionError("source and installed HD4 packs differ before launcher install")

    source_backup = OUTPUT / "backup" / "source"
    game_backup = GAME_ROOT / "backup_before_launcher_reference_v2_20260806"
    if source_backup.exists() != game_backup.exists():
        raise FileExistsError("launcher v2 backup is incomplete")
    create_backup = not source_backup.exists()
    if create_backup:
        source_backup.mkdir(parents=True)
        game_backup.mkdir(parents=True)
        shutil.copy2(source_pack, source_backup / source_pack.name)
        shutil.copy2(game_pack, game_backup / game_pack.name)

    masters = {
        ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0139_UNIT_LAUNCHER.png": neutral,
        ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0140_UNIT_LAUNCHER_SHADOW.png": shadow,
        ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HM_UNIT_LAUNCHER.png": mask,
        ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HOUSEMASK_UNIT_LAUNCHER.png": mask,
    }
    for path, image in masters.items():
        if create_backup and path.exists():
            destination = source_backup / "masters" / path.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path, optimize=True)
    for house, code in (("Atreides", "A"), ("Harkonnen", "H"), ("Ordos", "O")):
        variant = apply_tint(neutral, mask, HOUSE_COLORS[house])
        for name in (
            f"HV_{code}_UNIT_LAUNCHER.png",
            f"HOUSEVARIANT_{house.upper()}_UNIT_LAUNCHER.png",
        ):
            path = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / name
            if create_backup and path.exists():
                destination = source_backup / "masters" / path.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
            variant.save(path, optimize=True)

    patch_pack(source_pack, neutral, shadow, mask)
    shutil.copy2(source_pack, game_pack)
    if sha256(source_pack) != sha256(game_pack):
        raise AssertionError("installed HD4 pack differs from source after install")
    return {
        "source_pack": str(source_pack),
        "game_pack": str(game_pack),
        "sha256": sha256(source_pack),
        "source_backup": str(source_backup),
        "game_backup": str(game_backup),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    source = Image.open(args.source).convert("RGBA")
    colored, _ = build_colored_atlas(source)
    neutral, mask = neutral_and_mask(colored)
    shadow = build_shadow(neutral)
    validation = validate(neutral, mask, shadow)
    save_outputs(args.source, colored, neutral, mask, shadow, validation)

    result = {
        "source": str(args.source),
        "output": str(OUTPUT),
        "validation": validation,
        "installed": False,
    }
    if args.install:
        result["install"] = install(neutral, mask, shadow)
        result["installed"] = True
    (OUTPUT / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
