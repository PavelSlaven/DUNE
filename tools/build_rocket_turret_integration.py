#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved rocket turret."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "rocket_turret_review_v1"
TURRET_SOURCE = REVIEW / "BUILD_RTURRET_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "BUILD_RTURRET_SHADOW_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
OUTPUT_DIR = ROOT / "artifacts" / "rocket_turret_integration_v1" / "data"

TURRET_ID = 32
SHADOW_ID = 33
HD4_SIZE = (128, 1024)
HD2_SIZE = (64, 512)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement_entry(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=encode_png(image),
    )


def patch_pack(
    base_path: Path,
    output_path: Path,
    turret: Image.Image,
    shadow: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected_names = {
        TURRET_ID: "BUILD_RTURRET",
        SHADOW_ID: "BUILD_RTURRET_SHADOW",
    }
    for resource_id, expected_name in expected_names.items():
        if resource_id >= len(entries):
            raise AssertionError(f"resource ID {resource_id} is absent")
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"resource ID {resource_id} is not {expected_name}"
            )

    output_entries = list(entries)
    output_entries[TURRET_ID] = replacement_entry(
        entries[TURRET_ID],
        turret,
    )
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        shadow,
    )
    write_pack(output_path, output_entries)

    packed = read_pack(output_path)
    if len(packed) != len(entries):
        raise AssertionError("resource count changed")
    changed_ids = {TURRET_ID, SHADOW_ID}
    for before, after in zip(entries, packed, strict=True):
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
        TURRET_ID: turret.size,
        SHADOW_ID: shadow.size,
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
        "changed_ids": sorted(changed_ids),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    for path in (TURRET_SOURCE, SHADOW_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)

    turret4 = Image.open(TURRET_SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    if turret4.size != HD4_SIZE or shadow4.size != HD4_SIZE:
        raise AssertionError("approved HD4 atlas dimensions changed")
    if (
        turret4.getchannel("A").getbbox() is None
        or shadow4.getchannel("A").getbbox() is None
    ):
        raise AssertionError("approved atlas is empty")

    turret2 = turret4.resize(HD2_SIZE, Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize(HD2_SIZE, Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    turret4.save(MASTER_DIR / "0032_BUILD_RTURRET.png", optimize=True)
    shadow4.save(
        MASTER_DIR / "0033_BUILD_RTURRET_SHADOW.png",
        optimize=True,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            turret2,
            shadow2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            turret4,
            shadow4,
        ),
    ]

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    for resource_id in (TURRET_ID, SHADOW_ID):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(
                f"unable to decode packed resource {resource_id}"
            )
        expected2 = image4.resize(HD2_SIZE, Image.Resampling.LANCZOS)
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
        "resources": {
            "turret": {"id": TURRET_ID, "name": "BUILD_RTURRET"},
            "shadow": {
                "id": SHADOW_ID,
                "name": "BUILD_RTURRET_SHADOW",
            },
        },
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "frames": 8,
        "logical_frame": [32, 32],
        "hd2_atlas": list(HD2_SIZE),
        "hd4_atlas": list(HD4_SIZE),
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
