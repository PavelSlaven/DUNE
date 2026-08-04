#!/usr/bin/env python3
"""Build HD packs containing the approved neutral, House-tinted harvester."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
SOURCE = (
    ROOT
    / "artifacts"
    / "harvester_faction_preview_v1"
    / "UNIT_HARVESTER_NEUTRAL_HD4_PREVIEW.png"
)
MASK_SOURCE = (
    ROOT
    / "artifacts"
    / "harvester_faction_preview_v1"
    / "HM_UNIT_HARVESTER_HD4_PREVIEW.png"
)
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "harvester_integration_v1" / "data"

HARVESTER_ID = 137
SHADOW_ID = 138
MASK_NAME = "HM_UNIT_HARVESTER"
FRAME_SIZE = (320, 208)
ATLAS_SIZE = (2560, 832)
ROWS = 4
COLUMNS = 8


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_shadow(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", ATLAS_SIZE)
    for row in range(ROWS):
        for column in range(COLUMNS):
            left = column * FRAME_SIZE[0]
            top = row * FRAME_SIZE[1]
            frame = atlas.crop(
                (
                    left,
                    top,
                    left + FRAME_SIZE[0],
                    top + FRAME_SIZE[1],
                )
            )
            alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(2.4))
            alpha = alpha.point(lambda value: round(value * 0.20))
            shadow = Image.new("RGBA", FRAME_SIZE, (7, 5, 3, 0))
            shadow.putalpha(alpha)
            result.alpha_composite(shadow, (left + 7, top + 7))
    return result


def patch_pack(
    base_path: Path,
    output_path: Path,
    harvester: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    if len(entries) < 167:
        raise AssertionError(
            f"{base_path}: expected at least 167 entries, "
            f"got {len(entries)}"
        )
    if entries[HARVESTER_ID].name != "UNIT_HARVESTER":
        raise AssertionError("resource ID 137 is not UNIT_HARVESTER")
    if entries[SHADOW_ID].name != "UNIT_HARVESTER_SHADOW":
        raise AssertionError("resource ID 138 is not UNIT_HARVESTER_SHADOW")

    mask_indices = [
        entry.index
        for entry in entries
        if entry.name in (MASK_NAME, "HOUSEMASK_UNIT_HARVESTER")
    ]
    if len(mask_indices) > 1:
        raise AssertionError("multiple harvester House masks in base pack")

    replacements: dict[int, bytes] = {
        HARVESTER_ID: encode_png(harvester),
        SHADOW_ID: encode_png(shadow),
    }
    mask_index = mask_indices[0] if mask_indices else len(entries)
    if mask_indices:
        replacements[mask_index] = encode_png(mask)
    output_entries = [
        PackEntry(
            index=entry.index,
            name=MASK_NAME if entry.index == mask_index else entry.name,
            extension="PNG" if entry.index in replacements else entry.extension,
            payload=replacements.get(entry.index, entry.payload),
        )
        for entry in entries
    ]
    if not mask_indices:
        output_entries.append(
            PackEntry(
                index=mask_index,
                name=MASK_NAME,
                extension="PNG",
                payload=encode_png(mask),
            )
        )
    write_pack(output_path, output_entries)

    result = read_pack(output_path)
    if len(result) != len(entries) + (0 if mask_indices else 1):
        raise AssertionError("unexpected output entry count")
    for before, after in zip(entries, result, strict=False):
        if before.index in replacements:
            continue
        if (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {before.index}:{before.name}"
            )

    packed_harvester = decode_image(result[HARVESTER_ID].payload)
    packed_shadow = decode_image(result[SHADOW_ID].payload)
    packed_mask = decode_image(result[mask_index].payload)
    if (
        packed_harvester is None
        or packed_shadow is None
        or packed_mask is None
    ):
        raise AssertionError("replacement payload is not a valid image")
    if packed_harvester.size != harvester.size:
        raise AssertionError("packed harvester size changed")
    if packed_shadow.size != shadow.size:
        raise AssertionError("packed harvester shadow size changed")
    if packed_mask.size != mask.size:
        raise AssertionError("packed harvester mask size changed")

    return {
        "base": str(base_path),
        "output": str(output_path),
        "entries": len(result),
        "mask_id": mask_index,
        "unchanged_entries": len(entries) - len(replacements),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    if not SOURCE.is_file() or not MASK_SOURCE.is_file():
        raise FileNotFoundError("approved harvester base or mask is missing")
    master4 = Image.open(SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    if master4.size != ATLAS_SIZE:
        raise AssertionError(
            f"approved atlas has size {master4.size}, expected {ATLAS_SIZE}"
        )
    if master4.getchannel("A").getbbox() is None:
        raise AssertionError("approved atlas is fully transparent")
    if mask4.size != ATLAS_SIZE or mask4.getchannel("A").getbbox() is None:
        raise AssertionError("approved House mask is invalid")

    shadow4 = build_shadow(master4)
    master2 = master4.resize((1280, 416), Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize((1280, 416), Image.Resampling.LANCZOS)
    mask2 = mask4.resize((1280, 416), Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    master4.save(MASTER_DIR / "0137_UNIT_HARVESTER.png")
    shadow4.save(MASTER_DIR / "0138_UNIT_HARVESTER_SHADOW.png")
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            master2,
            shadow2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            master4,
            shadow4,
            mask4,
        ),
    ]

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")
    for resource_id in (
        HARVESTER_ID,
        SHADOW_ID,
        int(builds[0]["mask_id"]),
    ):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError("unable to decode packed harvester resource")
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
        "resource_id": HARVESTER_ID,
        "shadow_id": SHADOW_ID,
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "frames": ROWS,
        "logical_frame": [80, 52],
        "hd2_frame": [160, 104],
        "hd4_frame": list(FRAME_SIZE),
        "changed_ids": [
            HARVESTER_ID,
            SHADOW_ID,
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
