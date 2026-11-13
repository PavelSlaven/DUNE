#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved High-Tech Factory."""

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
REVIEW = ROOT / "artifacts" / "hitech_review_v1"
SOURCE = REVIEW / "BUILD_HIGHTECH_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "BUILD_HIGHTECH_SHADOW_HD4_PREVIEW.png"
FLAG_SOURCE = REVIEW / "BUILD_HIGHTECH_FLAG_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_BUILD_HIGHTECH_FLAG_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
OUTPUT_DIR = ROOT / "artifacts" / "hitech_integration_v1" / "data"

BUILDING_ID = 8
SHADOW_ID = 9
FLAG_NAME = "BUILD_HIGHTECH_FLAG"
MASK_NAME = "HM_BUILD_HIGHTECH_FLAG"
FRAME_SIZE = (384, 256)
BUILDING_ATLAS_SIZE = (384, 1792)
FLAG_ATLAS_SIZE = (384, 2048)
BUILDING_FRAME_COUNT = 7
FLAG_FRAME_COUNT = 8


def patch_pack(
    base_path: Path,
    output_path: Path,
    building: Image.Image,
    shadow: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected_names = {
        BUILDING_ID: "BUILD_HIGHTECH",
        SHADOW_ID: "BUILD_HIGHTECH_SHADOW",
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
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        shadow,
    )
    flag_id = upsert_named_entry(output_entries, FLAG_NAME, flag)
    mask_id = upsert_named_entry(output_entries, MASK_NAME, mask)
    write_pack(output_path, output_entries)

    packed = read_pack(output_path)
    changed_ids = {BUILDING_ID, SHADOW_ID, flag_id, mask_id}
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
        SHADOW_ID: shadow.size,
        flag_id: flag.size,
        mask_id: mask.size,
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
        "changed_ids": sorted(changed_ids),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def downscale_atlas(
    image: Image.Image,
    source_frame: tuple[int, int],
    target_frame: tuple[int, int],
    frame_count: int,
) -> Image.Image:
    result = Image.new(
        "RGBA",
        (target_frame[0], target_frame[1] * frame_count),
        (0, 0, 0, 0),
    )
    for frame_index in range(frame_count):
        frame = image.crop(
            (
                0,
                frame_index * source_frame[1],
                source_frame[0],
                (frame_index + 1) * source_frame[1],
            )
        )
        resized = frame.resize(target_frame, Image.Resampling.LANCZOS)
        result.alpha_composite(
            resized,
            (0, frame_index * target_frame[1]),
        )
    return result


def main() -> int:
    for path in (SOURCE, SHADOW_SOURCE, FLAG_SOURCE, MASK_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)

    building4 = Image.open(SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    flag4 = Image.open(FLAG_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    if building4.size != BUILDING_ATLAS_SIZE:
        raise AssertionError("approved High-Tech Factory dimensions changed")
    if shadow4.size != BUILDING_ATLAS_SIZE:
        raise AssertionError("approved High-Tech Factory shadow dimensions changed")
    if flag4.size != FLAG_ATLAS_SIZE or mask4.size != FLAG_ATLAS_SIZE:
        raise AssertionError("approved High-Tech Factory flag dimensions changed")

    building2 = downscale_atlas(
        building4,
        FRAME_SIZE,
        (192, 128),
        BUILDING_FRAME_COUNT,
    )
    shadow2 = downscale_atlas(
        shadow4,
        FRAME_SIZE,
        (192, 128),
        BUILDING_FRAME_COUNT,
    )
    flag2 = downscale_atlas(
        flag4,
        FRAME_SIZE,
        (192, 128),
        FLAG_FRAME_COUNT,
    )
    mask2 = downscale_atlas(
        mask4,
        FRAME_SIZE,
        (192, 128),
        FLAG_FRAME_COUNT,
    )

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    building4.save(MASTER_DIR / "0008_BUILD_HIGHTECH.png", optimize=True)
    shadow4.save(MASTER_DIR / "0009_BUILD_HIGHTECH_SHADOW.png", optimize=True)
    flag4.save(EXTRA_DIR / f"{FLAG_NAME}.png", optimize=True)
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            building2,
            shadow2,
            flag2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            building4,
            shadow4,
            flag4,
            mask4,
        ),
    ]
    if builds[0]["flag_id"] != builds[1]["flag_id"]:
        raise AssertionError("HD2 and HD4 High-Tech Factory flag IDs differ")
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 High-Tech Factory mask IDs differ")

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    resource_ids = (
        BUILDING_ID,
        SHADOW_ID,
        int(builds[0]["flag_id"]),
        int(builds[0]["mask_id"]),
    )
    for resource_id in resource_ids:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"unable to decode resource {resource_id}")
        source_frame = (
            image4.width,
            image4.height // (
                BUILDING_FRAME_COUNT
                if resource_id in (BUILDING_ID, SHADOW_ID)
                else FLAG_FRAME_COUNT
            ),
        )
        target_frame = (
            image2.width,
            image2.height // (
                BUILDING_FRAME_COUNT
                if resource_id in (BUILDING_ID, SHADOW_ID)
                else FLAG_FRAME_COUNT
            ),
        )
        expected2 = downscale_atlas(
            image4,
            source_frame,
            target_frame,
            (
                BUILDING_FRAME_COUNT
                if resource_id in (BUILDING_ID, SHADOW_ID)
                else FLAG_FRAME_COUNT
            ),
        )
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
        "shadow_id": SHADOW_ID,
        "flag_name": FLAG_NAME,
        "flag_id": builds[0]["flag_id"],
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "building_frames": BUILDING_FRAME_COUNT,
        "flag_frames": FLAG_FRAME_COUNT,
        "logical_frame": [96, 64],
        "hd2_frame": [192, 128],
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
