#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved three-soldier squad."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "soldiers_review_ready_hq"
SOURCE = REVIEW / "UNIT_SOLDIERS_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_UNIT_SOLDIERS_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "soldiers_integration_hq_v2" / "data"

SOLDIERS_ID = 156
MASK_NAME = "HM_UNIT_SOLDIERS"
FRAME_SIZE = (128, 128)
ATLAS_SIZE = (1024, 512)
FRAME_COUNT = 32


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


def patch_pack(
    base_path: Path,
    output_path: Path,
    soldiers: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    if len(entries) < 167:
        raise AssertionError(
            f"{base_path}: expected at least 167 entries, got {len(entries)}"
        )
    if entries[SOLDIERS_ID].name != "UNIT_SOLDIERS":
        raise AssertionError("resource ID 156 is not UNIT_SOLDIERS")

    mask_indices = [
        entry.index
        for entry in entries
        if entry.name in (MASK_NAME, "HOUSEMASK_UNIT_SOLDIERS")
    ]
    if len(mask_indices) > 1:
        raise AssertionError("multiple UNIT_SOLDIERS House masks")
    mask_index = mask_indices[0] if mask_indices else len(entries)

    output_entries = list(entries)
    output_entries[SOLDIERS_ID] = replace_entry(
        entries[SOLDIERS_ID],
        encode_png(soldiers),
    )
    if mask_indices:
        output_entries[mask_index] = PackEntry(
            index=mask_index,
            name=MASK_NAME,
            extension="PNG",
            payload=encode_png(mask),
        )
    else:
        output_entries.append(
            PackEntry(
                index=mask_index,
                name=MASK_NAME,
                extension="PNG",
                payload=encode_png(mask),
            )
        )

    write_pack(output_path, output_entries)
    packed = read_pack(output_path)
    if len(packed) != len(entries) + (0 if mask_indices else 1):
        raise AssertionError("unexpected output entry count")
    for before, after in zip(entries, packed, strict=False):
        if before.index in (SOLDIERS_ID, mask_index):
            continue
        if (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {before.index}:{before.name}"
            )

    expected = {
        SOLDIERS_ID: soldiers.size,
        mask_index: mask.size,
    }
    for resource_id, size in expected.items():
        image = decode_image(packed[resource_id].payload)
        if image is None or image.size != size:
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
    for path in (SOURCE, MASK_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)

    soldiers4 = Image.open(SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    for name, image in (
        ("soldiers", soldiers4),
        ("mask", mask4),
    ):
        if image.size != ATLAS_SIZE:
            raise AssertionError(f"{name} size is {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    soldiers2 = soldiers4.resize((512, 256), Image.Resampling.LANCZOS)
    mask2 = mask4.resize((512, 256), Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    soldiers4.save(MASTER_DIR / "0156_UNIT_SOLDIERS.png", optimize=True)
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            soldiers2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            soldiers4,
            mask4,
        ),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    for resource_id in (
        SOLDIERS_ID,
        int(builds[0]["mask_id"]),
    ):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError("unable to decode packed squad resource")
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
        "resource_id": SOLDIERS_ID,
        "shadow": "not used by the original UNIT_SOLDIERS contract",
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "direction_order": [
            "E",
            "NE",
            "N",
            "NW",
            "W",
            "SW",
            "S",
            "SE",
        ],
        "animation_rows": 4,
        "frames": FRAME_COUNT,
        "members_per_frame": 3,
        "logical_frame": [32, 32],
        "hd2_frame": [64, 64],
        "hd4_frame": list(FRAME_SIZE),
        "changed_ids": [
            SOLDIERS_ID,
            builds[0]["mask_id"],
        ],
        "builds": builds,
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
