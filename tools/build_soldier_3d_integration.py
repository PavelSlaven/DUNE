#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved GLB-based soldier."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageChops

from build_soldier_integration import patch_pack, sha256
from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "soldier_3d_review_v1"
SOURCE = REVIEW / "UNIT_SOLDIER_3D_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_UNIT_SOLDIER_3D_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
OUTPUT = ROOT / "artifacts" / "soldier_3d_integration"
OUTPUT_DATA = OUTPUT / "data"
BACKUP = OUTPUT / "backup_current"
TONE_BACKUP = OUTPUT / "backup_before_tone_fix"
SIZE_BACKUP = OUTPUT / "backup_before_size_fix"

SOLDIER_ID = 155
MASK_NAME = "HM_UNIT_SOLDIER"


def main() -> int:
    for path in (SOURCE, MASK_SOURCE, REVIEW / "manifest.json"):
        if not path.is_file():
            raise FileNotFoundError(path)
    soldier4 = Image.open(SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    if soldier4.size != (1024, 512) or mask4.size != soldier4.size:
        raise AssertionError("invalid HD4 soldier contract")
    review_manifest = json.loads((REVIEW / "manifest.json").read_text(encoding="utf-8"))
    if review_manifest.get("resource_id") != SOLDIER_ID:
        raise AssertionError("review manifest is not UNIT_SOLDIER")

    soldier2 = soldier4.resize((512, 256), Image.Resampling.LANCZOS)
    mask2 = mask4.resize((512, 256), Image.Resampling.LANCZOS)
    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(parents=True, exist_ok=True)
    TONE_BACKUP.mkdir(parents=True, exist_ok=True)
    SIZE_BACKUP.mkdir(parents=True, exist_ok=True)
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)

    source_packs = {
        "hd2": GAME / "data" / "sdl_data_hd2.dat",
        "hd4": GAME / "data" / "sdl_data_hd4.dat",
    }
    for source in source_packs.values():
        if not source.is_file():
            raise FileNotFoundError(source)
        if not (BACKUP / source.name).is_file():
            shutil.copy2(source, BACKUP / source.name)
        if not (TONE_BACKUP / source.name).is_file():
            shutil.copy2(source, TONE_BACKUP / source.name)
        shutil.copy2(source, SIZE_BACKUP / source.name)

    soldier4.save(MASTER_DIR / "0155_UNIT_SOLDIER.png", optimize=True)
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)
    builds = [
        patch_pack(source_packs["hd2"], OUTPUT_DATA / "sdl_data_hd2.dat", soldier2, mask2),
        patch_pack(source_packs["hd4"], OUTPUT_DATA / "sdl_data_hd4.dat", soldier4, mask4),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")

    packed2 = read_pack(OUTPUT_DATA / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DATA / "sdl_data_hd4.dat")
    for resource_id in (SOLDIER_ID, int(builds[0]["mask_id"])):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"resource {resource_id} is not decodable")
        expected2 = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(image2.convert("RGBA"), expected2.convert("RGBA")).getbbox():
            raise AssertionError(f"HD2 resource {resource_id} is not derived from HD4")

    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "resource_id": SOLDIER_ID,
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "logical_frame": [32, 32],
        "hd2_frame": [64, 64],
        "hd4_frame": [128, 128],
        "direction_order": review_manifest["direction_order"],
        "animation_rows": review_manifest["animation_rows"],
        "target_height_hd4": review_manifest["target_height_hd4"],
        "individual_height_logical": round(review_manifest["target_height_hd4"] / 4),
        "changed_ids": [SOLDIER_ID, builds[0]["mask_id"]],
        "backup": {
            name: {"path": str(BACKUP / path.name), "sha256": sha256(BACKUP / path.name)}
            for name, path in source_packs.items()
        },
        "backup_before_tone_fix": {
            name: {
                "path": str(TONE_BACKUP / path.name),
                "sha256": sha256(TONE_BACKUP / path.name),
            }
            for name, path in source_packs.items()
        },
        "backup_before_size_fix": {
            name: {
                "path": str(SIZE_BACKUP / path.name),
                "sha256": sha256(SIZE_BACKUP / path.name),
            }
            for name, path in source_packs.items()
        },
        "builds": builds,
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
