#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved UNIT_TROOPER atlas."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "trooper_from_triple_fremen_v1"
SOURCE = REVIEW / "UNIT_TROOPER_HD4.png"
MASK_SOURCE = REVIEW / "HM_UNIT_TROOPER_HD4.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "trooper_integration_hq_v1" / "data"

RESOURCE_ID = 165
RESOURCE_NAME = "UNIT_TROOPER"
MASK_NAME = "HM_UNIT_TROOPER"
ATLAS_SIZE = (1024, 512)


def resize_atlas(image: Image.Image, density: int) -> Image.Image:
    frame = 128
    target_frame = 32 * density
    output = Image.new("RGBA", (target_frame * 8, target_frame * 4))
    for row in range(4):
        for column in range(8):
            source = image.crop(
                (
                    column * frame,
                    row * frame,
                    (column + 1) * frame,
                    (row + 1) * frame,
                )
            )
            output.alpha_composite(
                source.resize(
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replace_entry(entry: PackEntry, payload: bytes) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=payload,
    )


def install(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".trooper.tmp")
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


def patch_pack(
    base_path: Path,
    output_path: Path,
    trooper: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    if entries[RESOURCE_ID].name != RESOURCE_NAME:
        raise AssertionError(
            f"resource ID {RESOURCE_ID} is not {RESOURCE_NAME}"
        )
    mask_indices = [
        entry.index
        for entry in entries
        if entry.name in (MASK_NAME, "HOUSEMASK_UNIT_TROOPER")
    ]
    if len(mask_indices) > 1:
        raise AssertionError("multiple UNIT_TROOPER house masks")
    mask_index = mask_indices[0] if mask_indices else len(entries)

    output_entries = list(entries)
    output_entries[RESOURCE_ID] = replace_entry(
        entries[RESOURCE_ID],
        encode_png(trooper),
    )
    mask_entry = PackEntry(
        index=mask_index,
        name=MASK_NAME,
        extension="PNG",
        payload=encode_png(mask),
    )
    if mask_indices:
        output_entries[mask_index] = mask_entry
    else:
        output_entries.append(mask_entry)

    write_pack(output_path, output_entries)
    packed = read_pack(output_path)
    expected_count = len(entries) + (0 if mask_indices else 1)
    if len(packed) != expected_count:
        raise AssertionError(
            f"unexpected output entry count {len(packed)}"
        )
    for before, after in zip(entries, packed, strict=False):
        if before.index in (RESOURCE_ID, mask_index):
            continue
        if (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {before.index}:{before.name}"
            )

    for resource_id, expected_size in (
        (RESOURCE_ID, trooper.size),
        (mask_index, mask.size),
    ):
        decoded = decode_image(packed[resource_id].payload)
        if decoded is None or decoded.size != expected_size:
            raise AssertionError(
                f"packed resource {resource_id} has invalid dimensions"
            )
    return {
        "base": str(base_path),
        "output": str(output_path),
        "entries": len(packed),
        "mask_id": mask_index,
        "unchanged_entries": len(entries) - 1 - int(bool(mask_indices)),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()
    for path in (SOURCE, MASK_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    trooper4 = Image.open(SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    for name, image in (("trooper", trooper4), ("mask", mask4)):
        if image.size != ATLAS_SIZE:
            raise AssertionError(f"{name} size is {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    trooper2 = resize_atlas(trooper4, 2)
    mask2 = clamp_mask(resize_atlas(mask4, 2), trooper2)
    mask4 = clamp_mask(mask4, trooper4)
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    trooper4.save(MASTER_DIR / "0165_UNIT_TROOPER.png", optimize=True)
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            trooper2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            trooper4,
            mask4,
        ),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    for resource_id in (RESOURCE_ID, int(builds[0]["mask_id"])):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError("unable to decode packed trooper resource")
        expected2 = resize_atlas(image4, 2)
        if resource_id == int(builds[0]["mask_id"]):
            expected2 = clamp_mask(expected2, trooper2)
        if ImageChops.difference(
            image2.convert("RGBA"),
            expected2.convert("RGBA"),
        ).getbbox():
            raise AssertionError(
                f"HD2 resource {resource_id} is not the HD4 derivative"
            )

    status = "built_not_installed"
    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install(
                OUTPUT_DIR / filename,
                GAME / "data" / filename,
                OUTPUT_DIR.parent / "backup" / filename,
            )
        status = "installed"

    manifest = {
        "format": 1,
        "status": status,
        "resource_id": RESOURCE_ID,
        "resource": RESOURCE_NAME,
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "animation_rows": 4,
        "frames": 32,
        "logical_frame": [32, 32],
        "hd2_frame": [64, 64],
        "hd4_frame": [128, 128],
        "changed_ids": [RESOURCE_ID, builds[0]["mask_id"]],
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
    manifest_path = OUTPUT_DIR.parent / "manifest.json"
    manifest_path.write_text(
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
