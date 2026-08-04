#!/usr/bin/env python3
"""Remove white-source halos from UNIT_TROOPERS and patch the HD packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack
from prepare_trooper_from_triple_fremen import (
    despill_bright_boundary,
    refine_white_matte,
)


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
OUT = ROOT / "artifacts" / "troopers_edge_cleanup_v1"
RESOURCE_ID = 166
RESOURCE_NAME = "UNIT_TROOPERS"
MASK_NAME = "HM_UNIT_TROOPERS"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_atlas(atlas: Image.Image) -> Image.Image:
    frame_width = atlas.width // 8
    frame_height = atlas.height // 4
    if frame_width != frame_height:
        raise AssertionError("UNIT_TROOPERS frames are not square")
    output = Image.new("RGBA", atlas.size)
    frames: list[Image.Image] = []
    for row in range(4):
        for column in range(8):
            box = (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
            rgba = np.asarray(atlas.crop(box).convert("RGBA")).copy()
            cleaned = Image.fromarray(
                despill_bright_boundary(refine_white_matte(rgba)), "RGBA"
            )
            frames.append(cleaned)
            output.alpha_composite(cleaned, (box[0], box[1]))
    if len({frame.tobytes() for frame in frames}) != 32:
        raise AssertionError("cleaned UNIT_TROOPERS frames are not unique")
    return output


def resize_atlas(atlas: Image.Image, density: int) -> Image.Image:
    source_frame = atlas.width // 8
    target_frame = 32 * density
    output = Image.new("RGBA", (target_frame * 8, target_frame * 4))
    for row in range(4):
        for column in range(8):
            frame = atlas.crop(
                (
                    column * source_frame,
                    row * source_frame,
                    (column + 1) * source_frame,
                    (row + 1) * source_frame,
                )
            )
            output.alpha_composite(
                frame.resize(
                    (target_frame, target_frame), Image.Resampling.LANCZOS
                ),
                (column * target_frame, row * target_frame),
            )
    return output


def clamp_mask(mask: Image.Image, unit: Image.Image) -> Image.Image:
    mask_rgba = np.asarray(mask.convert("RGBA")).copy()
    unit_alpha = np.asarray(unit.convert("RGBA"))[:, :, 3]
    mask_rgba[:, :, 3] = np.minimum(mask_rgba[:, :, 3], unit_alpha)
    mask_rgba[mask_rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(mask_rgba, "RGBA")


def halo_count(atlas: Image.Image) -> int:
    count = 0
    frame = atlas.width // 8
    for row in range(4):
        for column in range(8):
            rgba = np.asarray(
                atlas.crop(
                    (
                        column * frame,
                        row * frame,
                        (column + 1) * frame,
                        (row + 1) * frame,
                    )
                ).convert("RGBA")
            )
            visible = rgba[:, :, 3] > 0
            distance = cv2.distanceTransform(
                visible.astype(np.uint8), cv2.DIST_L2, 5
            )
            rgb = rgba[:, :, :3]
            count += int(
                (
                    visible
                    & (distance <= 2.8)
                    & (rgb.min(axis=2) >= 170)
                    & ((rgb.max(axis=2) - rgb.min(axis=2)) <= 48)
                ).sum()
            )
    return count


def patch_pack(
    source: Path, output: Path, unit: Image.Image, mask: Image.Image
) -> dict[str, object]:
    entries = read_pack(source)
    if entries[RESOURCE_ID].name != RESOURCE_NAME:
        raise AssertionError(f"resource {RESOURCE_ID} is {entries[RESOURCE_ID].name}")
    masks = [entry for entry in entries if entry.name == MASK_NAME]
    if len(masks) != 1:
        raise AssertionError(f"expected one {MASK_NAME}, got {len(masks)}")
    mask_id = masks[0].index
    patched = list(entries)
    patched[RESOURCE_ID] = PackEntry(
        RESOURCE_ID, RESOURCE_NAME, "PNG", encode_png(unit)
    )
    patched[mask_id] = PackEntry(mask_id, MASK_NAME, "PNG", encode_png(mask))
    write_pack(output, patched)

    packed = read_pack(output)
    for before, after in zip(entries, packed, strict=True):
        if before.index in (RESOURCE_ID, mask_id):
            continue
        if (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(f"unrelated entry changed: {before.index}:{before.name}")
    return {
        "source": str(source),
        "output": str(output),
        "entries": len(packed),
        "mask_id": mask_id,
        "sha256": sha256(output),
    }


def install(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".troopers-edge.tmp")
    try:
        shutil.copy2(source, temporary)
        if sha256(source) != sha256(temporary):
            raise AssertionError("temporary pack copy differs")
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    if sha256(source) != sha256(target):
        raise AssertionError("installed pack differs")


def build_review(atlas: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (atlas.width, atlas.height + 48), (18, 20, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 12), "UNIT_TROOPERS — cleaned alpha edge", fill=(240, 220, 178))
    background = Image.new("RGBA", atlas.size, (42, 43, 40, 255))
    background.alpha_composite(atlas)
    canvas.paste(background.convert("RGB"), (0, 48))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    hd4_path = GAME / "data" / "sdl_data_hd4.dat"
    backup_hd4_path = OUT / "backup" / "sdl_data_hd4.dat"
    artistic_source_hd4 = backup_hd4_path if backup_hd4_path.exists() else hd4_path
    hd4_entries = read_pack(artistic_source_hd4)
    masks = [entry for entry in hd4_entries if entry.name == MASK_NAME]
    if len(masks) != 1:
        raise AssertionError(f"expected one {MASK_NAME}, got {len(masks)}")
    unit4_before = decode_image(hd4_entries[RESOURCE_ID].payload)
    mask4 = decode_image(masks[0].payload)
    if unit4_before is None or mask4 is None or unit4_before.size != mask4.size:
        raise AssertionError("invalid UNIT_TROOPERS HD4 resources")

    unit4 = clean_atlas(unit4_before)
    unit_alpha = np.asarray(unit4.getchannel("A"))
    mask_array = np.asarray(mask4.convert("RGBA")).copy()
    mask_array[:, :, 3] = np.minimum(mask_array[:, :, 3], unit_alpha)
    mask4 = clamp_mask(Image.fromarray(mask_array, "RGBA"), unit4)
    unit2 = resize_atlas(unit4, 2)
    mask2 = clamp_mask(resize_atlas(mask4, 2), unit2)

    data = OUT / "data"
    data.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / f"sdl_data_hd{density}.dat",
            data / f"sdl_data_hd{density}.dat",
            unit2 if density == 2 else unit4,
            mask2 if density == 2 else mask4,
        )
        for density in (2, 4)
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2/HD4 mask IDs differ")

    master = ROOT / "resources" / "hd" / "master4" / "sdl_data"
    extra = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
    master.mkdir(parents=True, exist_ok=True)
    extra.mkdir(parents=True, exist_ok=True)
    unit4.save(master / "0166_UNIT_TROOPERS.png", optimize=True)
    mask4.save(extra / f"{MASK_NAME}.png", optimize=True)
    unit4.save(OUT / "UNIT_TROOPERS_HD4.png", optimize=True)
    mask4.save(OUT / "HM_UNIT_TROOPERS_HD4.png", optimize=True)
    build_review(unit4).save(OUT / "UNIT_TROOPERS_EDGE_REVIEW.png", optimize=True)

    status = "built_not_installed"
    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install(
                data / filename,
                GAME / "data" / filename,
                OUT / "backup" / filename,
            )
        status = "installed"

    report = {
        "format": 1,
        "status": status,
        "resource": {"id": RESOURCE_ID, "name": RESOURCE_NAME},
        "mask": {"id": builds[0]["mask_id"], "name": MASK_NAME},
        "artistic_source_hd4": str(artistic_source_hd4),
        "bright_boundary_pixels_before": halo_count(unit4_before),
        "bright_boundary_pixels_after": halo_count(unit4),
        "builds": builds,
        "installed_sha256": (
            {
                f"hd{density}": sha256(
                    GAME / "data" / f"sdl_data_hd{density}.dat"
                )
                for density in (2, 4)
            }
            if args.install
            else {}
        ),
    }
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
