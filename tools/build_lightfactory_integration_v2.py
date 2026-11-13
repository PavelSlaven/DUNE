#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved Light Factory v2."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from build_palace_integration import (
    replacement_entry,
    sha256,
    upsert_named_entry,
)
from hd_assets import decode_image, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "lightfactory_review_v2"
SOURCE = REVIEW / "BUILD_LIGHTFACTORY_HD4_PREVIEW.png"
FLASH_SOURCE = REVIEW / "BUILD_LIGHTFACTORY_FLASH_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "BUILD_LIGHTFACTORY_SHADOW_HD4_PREVIEW.png"
FLAG_SOURCE = REVIEW / "BUILD_LIGHTFACTORY_FLAG_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_BUILD_LIGHTFACTORY_FLAG_HD4_PREVIEW.png"
PRODUCTION_SOURCE = REVIEW / "BUILD_LIGHTFACTORY_PRODUCTION_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
OUTPUT_DIR = ROOT / "artifacts" / "lightfactory_integration_v2" / "data"

BUILDING_ID = 12
FLASH_ID = 13
SHADOW_ID = 14
FLAG_NAME = "BUILD_LIGHTFACTORY_FLAG"
MASK_NAME = "HM_BUILD_LIGHTFACTORY_FLAG"
PRODUCTION_NAME = "BUILD_LIGHTFACTORY_PRODUCTION"
FRAME_SIZE = (256, 256)
ATLAS_SIZE = (256, 2048)
FRAME_COUNT = 8


def patch_pack(
    base_path: Path,
    output_path: Path,
    building: Image.Image,
    flash: Image.Image,
    shadow: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
    production: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected_names = {
        BUILDING_ID: "BUILD_LIGHTFACTORY",
        FLASH_ID: "BUILD_LIGHTFACTORY_FLASH",
        SHADOW_ID: "BUILD_LIGHTFACTORY_SHADOW",
    }
    for resource_id, expected_name in expected_names.items():
        if resource_id >= len(entries):
            raise AssertionError(f"resource ID {resource_id} is absent")
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"resource ID {resource_id} is not {expected_name}"
            )

    output_entries = list(entries)
    output_entries[BUILDING_ID] = replacement_entry(
        entries[BUILDING_ID],
        building,
    )
    output_entries[FLASH_ID] = replacement_entry(entries[FLASH_ID], flash)
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        shadow,
    )
    flag_id = upsert_named_entry(output_entries, FLAG_NAME, flag)
    mask_id = upsert_named_entry(output_entries, MASK_NAME, mask)
    production_id = upsert_named_entry(
        output_entries,
        PRODUCTION_NAME,
        production,
    )
    write_pack(output_path, output_entries)

    packed = read_pack(output_path)
    changed_ids = {
        BUILDING_ID,
        FLASH_ID,
        SHADOW_ID,
        flag_id,
        mask_id,
        production_id,
    }
    if len(packed) != len(output_entries):
        raise AssertionError("unexpected output entry count")
    for before, after in zip(entries, packed, strict=False):
        if before.index in changed_ids:
            continue
        if (
            before.index != after.index
            or before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {before.index}:{before.name}"
            )

    expected_sizes = {
        BUILDING_ID: building.size,
        FLASH_ID: flash.size,
        SHADOW_ID: shadow.size,
        flag_id: flag.size,
        mask_id: mask.size,
        production_id: production.size,
    }
    for resource_id, expected_size in expected_sizes.items():
        image = decode_image(packed[resource_id].payload)
        if image is None or image.size != expected_size:
            raise AssertionError(
                f"packed resource {resource_id} has invalid dimensions"
            )
    return {
        "base": str(base_path),
        "output": str(output_path),
        "entries": len(packed),
        "flag_id": flag_id,
        "mask_id": mask_id,
        "production_id": production_id,
        "changed_ids": sorted(changed_ids),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    for path in (
        SOURCE,
        FLASH_SOURCE,
        SHADOW_SOURCE,
        FLAG_SOURCE,
        MASK_SOURCE,
        PRODUCTION_SOURCE,
    ):
        if not path.is_file():
            raise FileNotFoundError(path)

    building4 = Image.open(SOURCE).convert("RGBA")
    flash4 = Image.open(FLASH_SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    flag4 = Image.open(FLAG_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    production4 = Image.open(PRODUCTION_SOURCE).convert("RGBA")
    if (
        building4.size != FRAME_SIZE
        or flash4.size != FRAME_SIZE
        or shadow4.size != FRAME_SIZE
    ):
        raise AssertionError("approved Light Factory dimensions changed")
    if (
        flag4.size != ATLAS_SIZE
        or mask4.size != ATLAS_SIZE
        or production4.size != ATLAS_SIZE
    ):
        raise AssertionError("approved Light Factory atlas dimensions changed")

    building2 = building4.resize((128, 128), Image.Resampling.LANCZOS)
    flash2 = flash4.resize((128, 128), Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize((128, 128), Image.Resampling.LANCZOS)
    flag2 = flag4.resize((128, 1024), Image.Resampling.LANCZOS)
    mask2 = mask4.resize((128, 1024), Image.Resampling.LANCZOS)
    production2 = production4.resize(
        (128, 1024),
        Image.Resampling.LANCZOS,
    )

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    building4.save(
        MASTER_DIR / "0012_BUILD_LIGHTFACTORY.png",
        optimize=True,
    )
    flash4.save(
        MASTER_DIR / "0013_BUILD_LIGHTFACTORY_FLASH.png",
        optimize=True,
    )
    shadow4.save(
        MASTER_DIR / "0014_BUILD_LIGHTFACTORY_SHADOW.png",
        optimize=True,
    )
    flag4.save(EXTRA_DIR / f"{FLAG_NAME}.png", optimize=True)
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)
    production4.save(
        EXTRA_DIR / f"{PRODUCTION_NAME}.png",
        optimize=True,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            building2,
            flash2,
            shadow2,
            flag2,
            mask2,
            production2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            building4,
            flash4,
            shadow4,
            flag4,
            mask4,
            production4,
        ),
    ]
    if builds[0]["flag_id"] != builds[1]["flag_id"]:
        raise AssertionError("HD2 and HD4 Light Factory flag IDs differ")
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 Light Factory mask IDs differ")
    if builds[0]["production_id"] != builds[1]["production_id"]:
        raise AssertionError(
            "HD2 and HD4 Light Factory production IDs differ"
        )

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    resource_ids = (
        BUILDING_ID,
        FLASH_ID,
        SHADOW_ID,
        int(builds[0]["flag_id"]),
        int(builds[0]["mask_id"]),
        int(builds[0]["production_id"]),
    )
    for resource_id in resource_ids:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"unable to decode resource {resource_id}")
        expected2 = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(
            image2.convert("RGBA"),
            expected2.convert("RGBA"),
        ).getbbox():
            raise AssertionError(
                f"HD2 resource {resource_id} is not the HD4 derivative"
            )

    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "resource_id": BUILDING_ID,
        "flash_id": FLASH_ID,
        "shadow_id": SHADOW_ID,
        "flag_name": FLAG_NAME,
        "flag_id": builds[0]["flag_id"],
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "production_name": PRODUCTION_NAME,
        "production_id": builds[0]["production_id"],
        "frames": FRAME_COUNT,
        "logical_frame": [64, 64],
        "hd2_frame": [128, 128],
        "hd4_frame": list(FRAME_SIZE),
        "builds": builds,
    }
    (OUTPUT_DIR.parent / "manifest.json").write_text(
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
