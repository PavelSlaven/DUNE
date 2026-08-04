#!/usr/bin/env python3
"""Fix the harvester's pale House tint and malformed spice plumes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
OUTPUT = ROOT / "artifacts" / "harvester_harvesting_fix_v1"
DATA_OUTPUT = OUTPUT / "data"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
FRAME = (320, 208)
ATLAS = (2560, 832)
ROWS = 4
COLUMNS = 8
HARVESTER_ID = 137
SHADOW_ID = 138
MASK_NAME = "HM_UNIT_HARVESTER"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def crop_frame(atlas: Image.Image, column: int, row: int) -> Image.Image:
    x = column * FRAME[0]
    y = row * FRAME[1]
    return atlas.crop((x, y, x + FRAME[0], y + FRAME[1]))


def sand_mask(frame: Image.Image) -> np.ndarray:
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.int16)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    strong = (
        (alpha > 24)
        & (red > 135)
        & (green > 90)
        & (blue > 35)
        & (red > blue * 1.15)
        & (green > blue * 1.05)
    )
    broad = (
        (alpha > 4)
        & (red > 72)
        & (green > 52)
        & (blue > 28)
        & (red > green * 1.02)
        & (green > blue * 1.03)
        & (red > blue * 1.18)
    )
    labels, count = ndimage.label(broad, np.ones((3, 3), dtype=np.uint8))
    result = np.zeros_like(broad)
    for label_id in range(1, count + 1):
        component = labels == label_id
        if (
            np.count_nonzero(component) >= 80
            and np.count_nonzero(component & strong) >= 28
        ):
            result |= component
    return result


def masked_sprite(frame: Image.Image, selection: np.ndarray) -> Image.Image:
    expanded = ndimage.binary_dilation(selection, iterations=2)
    alpha = Image.fromarray((expanded * 255).astype(np.uint8), "L")
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.75))
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.uint8).copy()
    rgba[:, :, 3] = np.minimum(
        rgba[:, :, 3],
        np.asarray(alpha, dtype=np.uint8),
    )
    return Image.fromarray(rgba, "RGBA")


def clear_selection(frame: Image.Image, selection: np.ndarray) -> Image.Image:
    expanded = ndimage.binary_dilation(selection, iterations=2)
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.uint8).copy()
    rgba[expanded] = 0
    return Image.fromarray(rgba, "RGBA")


def repair_west_plumes(atlas: Image.Image) -> None:
    """Use the approved east plume mirrored across the vertical axis."""
    for row in range(1, ROWS):
        east = crop_frame(atlas, 0, row)
        west = crop_frame(atlas, 4, row)
        west_clean = clear_selection(west, sand_mask(west))
        mirrored_plume = masked_sprite(east, sand_mask(east)).transpose(
            Image.Transpose.FLIP_LEFT_RIGHT
        )
        west_clean.alpha_composite(mirrored_plume)
        atlas.paste(west_clean, (4 * FRAME[0], row * FRAME[1]))


def remove_sw_duplicate_plumes(atlas: Image.Image) -> None:
    """Remove the isolated left plume while preserving the attached rear plume."""
    for row in range(1, ROWS):
        frame = crop_frame(atlas, 5, row)
        alpha = np.asarray(frame.getchannel("A"), dtype=np.uint8) > 0
        labels, count = ndimage.label(alpha, np.ones((3, 3), dtype=np.uint8))
        remove = np.zeros_like(alpha)
        for label_id in range(1, count + 1):
            component = labels == label_id
            area = int(np.count_nonzero(component))
            if area < 500:
                continue
            ys, xs = np.nonzero(component)
            if int(xs.max()) < 90:
                remove |= component
        if not np.any(remove):
            raise AssertionError(f"SW phase {row}: detached plume not found")
        rgba = np.asarray(frame, dtype=np.uint8).copy()
        rgba[remove] = 0
        repaired = Image.fromarray(rgba, "RGBA")
        atlas.paste(repaired, (5 * FRAME[0], row * FRAME[1]))


def remove_detached_specks(atlas: Image.Image) -> None:
    """Keep only the vehicle and its connected plume in repaired headings."""
    for column in (4, 5):
        for row in range(1, ROWS):
            frame = crop_frame(atlas, column, row)
            rgba = np.asarray(frame, dtype=np.uint8).copy()
            visible = rgba[:, :, 3] > 0
            labels, count = ndimage.label(
                visible,
                np.ones((3, 3), dtype=np.uint8),
            )
            if count <= 1:
                continue
            sizes = ndimage.sum(visible, labels, range(1, count + 1))
            main_label = int(np.argmax(sizes)) + 1
            rgba[labels != main_label] = 0
            atlas.paste(
                Image.fromarray(rgba, "RGBA"),
                (column * FRAME[0], row * FRAME[1]),
            )


def strengthen_mask(mask: Image.Image) -> Image.Image:
    rgba = np.asarray(mask.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    peak = int(alpha.max())
    if peak <= 0:
        raise AssertionError("House mask is empty")
    rgba[:, :, 3] = np.clip(
        np.rint(alpha.astype(np.float32) * 255.0 / peak),
        0,
        255,
    ).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def build_shadow(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", ATLAS)
    for row in range(ROWS):
        for column in range(COLUMNS):
            frame = crop_frame(atlas, column, row)
            alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(2.4))
            alpha = alpha.point(lambda value: round(value * 0.20))
            shadow = Image.new("RGBA", FRAME, (7, 5, 3, 0))
            shadow.putalpha(alpha)
            result.alpha_composite(
                shadow,
                (column * FRAME[0] + 7, row * FRAME[1] + 7),
            )
    return result


def tint_red(image: Image.Image, mask: Image.Image) -> Image.Image:
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
    for channel, target in enumerate((255, 0, 0)):
        colored = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - strength)
            + colored * strength
        )
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def patch_pack(
    source: Path,
    target: Path,
    harvester: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(source)
    mask_ids = [entry.index for entry in entries if entry.name == MASK_NAME]
    if len(mask_ids) != 1:
        raise AssertionError(f"expected one {MASK_NAME}, found {len(mask_ids)}")
    mask_id = mask_ids[0]
    replacements = {
        HARVESTER_ID: encode_png(harvester),
        SHADOW_ID: encode_png(shadow),
        mask_id: encode_png(mask),
    }
    output_entries = [
        PackEntry(
            index=entry.index,
            name=entry.name,
            extension="PNG" if entry.index in replacements else entry.extension,
            payload=replacements.get(entry.index, entry.payload),
        )
        for entry in entries
    ]
    target.parent.mkdir(parents=True, exist_ok=True)
    write_pack(target, output_entries)
    packed = read_pack(target)
    for before, after in zip(entries, packed, strict=True):
        if before.index not in replacements and before.payload != after.payload:
            raise AssertionError(f"unrelated resource changed: {before.index}")
    return {
        "source": str(source),
        "output": str(target),
        "mask_id": mask_id,
        "changed_ids": sorted(replacements),
        "sha256": sha256(target),
    }


def font(size: int, bold: bool = False):
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def build_review(
    before: Image.Image,
    after: Image.Image,
    mask_before: Image.Image,
    mask_after: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1500, 920), (13, 16, 19, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (32, 24),
        "Харвестер: исправление маски и сбора пряности",
        font=font(30, True),
        fill=(235, 219, 182, 255),
    )
    draw.text((50, 76), "Было", font=font(22, True), fill=(225, 110, 96, 255))
    draw.text((770, 76), "Стало", font=font(22, True), fill=(105, 211, 137, 255))
    for group, (column, label) in enumerate(((4, "W"), (5, "SW"))):
        y = 120 + group * 285
        draw.text((32, y + 84), label, font=font(22, True), fill=(210, 190, 140, 255))
        for row in range(1, 4):
            left = crop_frame(before, column, row).resize((192, 125), Image.Resampling.LANCZOS)
            right = crop_frame(after, column, row).resize((192, 125), Image.Resampling.LANCZOS)
            board.alpha_composite(left, (80 + (row - 1) * 210, y))
            board.alpha_composite(right, (800 + (row - 1) * 210, y))
            draw.text(
                (145 + (row - 1) * 210, y + 132),
                f"фаза {row}",
                font=font(15),
                fill=(190, 195, 200, 255),
            )

    red_before = tint_red(before, mask_before)
    red_after = tint_red(after, mask_after)
    y = 700
    draw.text((32, y + 50), "Красная маска", font=font(20, True), fill=(210, 190, 140, 255))
    board.alpha_composite(crop_frame(red_before, 0, 0).resize((240, 156), Image.Resampling.LANCZOS), (230, y))
    board.alpha_composite(crop_frame(red_after, 0, 0).resize((240, 156), Image.Resampling.LANCZOS), (950, y))
    return board


def main() -> None:
    hd4_entries = read_pack(GAME / "data" / "sdl_data_hd4.dat")
    before = decode_image(hd4_entries[HARVESTER_ID].payload)
    mask_entry = next(entry for entry in hd4_entries if entry.name == MASK_NAME)
    mask_before = decode_image(mask_entry.payload)
    if before is None or mask_before is None:
        raise AssertionError("installed harvester resources are invalid")
    before = before.convert("RGBA")
    mask_before = mask_before.convert("RGBA")
    if before.size != ATLAS or mask_before.size != ATLAS:
        raise AssertionError("installed harvester atlas dimensions changed")

    after = before.copy()
    repair_west_plumes(after)
    remove_sw_duplicate_plumes(after)
    remove_detached_specks(after)
    mask_after = strengthen_mask(mask_before)
    shadow_after = build_shadow(after)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    after.save(MASTER_DIR / "0137_UNIT_HARVESTER.png")
    shadow_after.save(MASTER_DIR / "0138_UNIT_HARVESTER_SHADOW.png")
    mask_after.save(EXTRA_DIR / f"{MASK_NAME}.png")

    DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    hd4 = patch_pack(
        GAME / "data" / "sdl_data_hd4.dat",
        DATA_OUTPUT / "sdl_data_hd4.dat",
        after,
        shadow_after,
        mask_after,
    )
    hd2_after = after.resize((1280, 416), Image.Resampling.LANCZOS)
    hd2_shadow = shadow_after.resize((1280, 416), Image.Resampling.LANCZOS)
    hd2_mask = mask_after.resize((1280, 416), Image.Resampling.LANCZOS)
    hd2 = patch_pack(
        GAME / "data" / "sdl_data_hd2.dat",
        DATA_OUTPUT / "sdl_data_hd2.dat",
        hd2_after,
        hd2_shadow,
        hd2_mask,
    )

    for resource_id in (HARVESTER_ID, SHADOW_ID, int(hd4["mask_id"])):
        packed4 = decode_image(read_pack(Path(hd4["output"]))[resource_id].payload)
        packed2 = decode_image(read_pack(Path(hd2["output"]))[resource_id].payload)
        if packed4 is None or packed2 is None:
            raise AssertionError(f"unable to decode resource {resource_id}")
        expected = packed4.resize(packed2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(expected.convert("RGBA"), packed2.convert("RGBA")).getbbox():
            raise AssertionError(f"HD2 resource {resource_id} is not derived from HD4")

    after.save(OUTPUT / "UNIT_HARVESTER_HD4_FIXED.png")
    mask_after.save(OUTPUT / "HM_UNIT_HARVESTER_HD4_FIXED.png")
    build_review(before, after, mask_before, mask_after).save(
        OUTPUT / "HARVESTER_HARVESTING_FIX_REVIEW.png"
    )
    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "changes": [
            "saturated House mask",
            "mirrored full W harvesting plume",
            "removed duplicate detached SW plume",
        ],
        "logical_frame": [80, 52],
        "hd4_frame": list(FRAME),
        "atlas": list(ATLAS),
        "hd2": hd2,
        "hd4": hd4,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
