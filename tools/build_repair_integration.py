#!/usr/bin/env python3
"""Build HD2/HD4 world packs containing the approved Repair Facility."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "repair_review_v1"
SOURCE = REVIEW / "BUILD_REPAIR_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "BUILD_REPAIR_SHADOW_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
OUTPUT_DIR = ROOT / "artifacts" / "repair_integration_v1" / "data"

REPAIR_ID = 30
SHADOW_ID = 31
FRAME_COUNT = 8
HD4_FRAME = (384, 256)
HD2_FRAME = (192, 128)
HD4_ATLAS = (384, 2048)
HD2_ATLAS = (192, 1024)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atlas_frame(
    atlas: Image.Image,
    index: int,
    frame_size: tuple[int, int],
) -> Image.Image:
    return atlas.crop(
        (
            0,
            index * frame_size[1],
            frame_size[0],
            (index + 1) * frame_size[1],
        )
    )


def downscale_atlas(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", HD2_ATLAS)
    for index in range(FRAME_COUNT):
        frame = atlas_frame(atlas, index, HD4_FRAME)
        result.alpha_composite(
            frame.resize(HD2_FRAME, Image.Resampling.LANCZOS),
            (0, index * HD2_FRAME[1]),
        )
    return result


def replacement_entry(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=encode_png(image),
    )


def validate_source(building: Image.Image, shadow: Image.Image) -> None:
    if building.size != HD4_ATLAS or shadow.size != HD4_ATLAS:
        raise AssertionError("approved Repair Facility dimensions changed")

    frames = [
        atlas_frame(building, index, HD4_FRAME)
        for index in range(FRAME_COUNT)
    ]
    bounds = [frame.getchannel("A").getbbox() for frame in frames]
    if len(set(bounds)) != 1:
        raise AssertionError(f"Repair Facility anchors differ: {bounds}")

    shadow_frames = [
        atlas_frame(shadow, index, HD4_FRAME)
        for index in range(FRAME_COUNT)
    ]
    if any(
        ImageChops.difference(shadow_frames[0], frame).getbbox()
        for frame in shadow_frames[1:]
    ):
        raise AssertionError("Repair Facility shadow moves between frames")


def patch_pack(
    base_path: Path,
    output_path: Path,
    building: Image.Image,
    shadow: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected = {
        REPAIR_ID: "BUILD_REPAIR",
        SHADOW_ID: "BUILD_REPAIR_SHADOW",
    }
    for resource_id, name in expected.items():
        if resource_id >= len(entries) or entries[resource_id].name != name:
            raise AssertionError(
                f"resource {resource_id} is not {name}"
            )

    output_entries = list(entries)
    output_entries[REPAIR_ID] = replacement_entry(
        entries[REPAIR_ID],
        building,
    )
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        shadow,
    )
    write_pack(output_path, output_entries)

    packed = read_pack(output_path)
    if len(packed) != len(entries):
        raise AssertionError("unexpected output entry count")
    changed = {REPAIR_ID, SHADOW_ID}
    for before, after in zip(entries, packed, strict=True):
        if before.index in changed:
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

    for resource_id, expected_size in (
        (REPAIR_ID, building.size),
        (SHADOW_ID, shadow.size),
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
        "changed_ids": sorted(changed),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def validate_pair(hd2_path: Path, hd4_path: Path) -> None:
    packed2 = read_pack(hd2_path)
    packed4 = read_pack(hd4_path)
    for resource_id in (REPAIR_ID, SHADOW_ID):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"unable to decode resource {resource_id}")
        if image2.size != HD2_ATLAS or image4.size != HD4_ATLAS:
            raise AssertionError(
                f"resource {resource_id} has invalid packed dimensions"
            )
        expected2 = downscale_atlas(image4)
        if ImageChops.difference(
            image2.convert("RGBA"),
            expected2,
        ).getbbox():
            raise AssertionError(
                f"HD2 resource {resource_id} is not the HD4 derivative"
            )


def main() -> int:
    for path in (SOURCE, SHADOW_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)

    building4 = Image.open(SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    validate_source(building4, shadow4)
    building2 = downscale_atlas(building4)
    shadow2 = downscale_atlas(shadow4)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    building4.save(MASTER_DIR / "0030_BUILD_REPAIR.png", optimize=True)
    shadow4.save(
        MASTER_DIR / "0031_BUILD_REPAIR_SHADOW.png",
        optimize=True,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            building2,
            shadow2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            building4,
            shadow4,
        ),
    ]
    validate_pair(
        OUTPUT_DIR / "sdl_data_hd2.dat",
        OUTPUT_DIR / "sdl_data_hd4.dat",
    )

    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "resource_id": REPAIR_ID,
        "shadow_id": SHADOW_ID,
        "changed_ids": [REPAIR_ID, SHADOW_ID],
        "frames": FRAME_COUNT,
        "logical_frame": [96, 64],
        "hd2_frame": list(HD2_FRAME),
        "hd4_frame": list(HD4_FRAME),
        "animation": "door 0 to 7, hold, then 7 to 0",
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
