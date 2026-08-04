#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved saboteur walk cycle."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "saboteur_review_v2"
SOURCE = REVIEW / "UNIT_SABOTEUR_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_UNIT_SABOTEUR_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "saboteur_integration_v1" / "data"

SABOTEUR_ID = 149
RESOURCE_NAME = "UNIT_SABOTEUR"
MASK_NAME = "HM_UNIT_SABOTEUR"
ATLAS_HD4_SIZE = (1024, 512)
ATLAS_HD2_SIZE = (512, 256)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replace_entry(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=encode_png(image),
    )


def patch_pack(
    base_path: Path,
    output_path: Path,
    saboteur: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    if len(entries) < 167:
        raise AssertionError(
            f"{base_path}: expected at least 167 entries, got {len(entries)}"
        )
    if entries[SABOTEUR_ID].name != RESOURCE_NAME:
        raise AssertionError(
            f"resource ID {SABOTEUR_ID} is not {RESOURCE_NAME}"
        )

    mask_indices = [
        entry.index
        for entry in entries
        if entry.name in (MASK_NAME, f"HOUSEMASK_{RESOURCE_NAME}")
    ]
    if len(mask_indices) > 1:
        raise AssertionError("multiple UNIT_SABOTEUR House masks")
    mask_index = mask_indices[0] if mask_indices else len(entries)

    output_entries = list(entries)
    output_entries[SABOTEUR_ID] = replace_entry(
        entries[SABOTEUR_ID],
        saboteur,
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
            f"unexpected output entry count: {len(packed)} != {expected_count}"
        )

    changed = {SABOTEUR_ID, mask_index}
    for before, after in zip(entries, packed, strict=False):
        if before.index in changed:
            continue
        if (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {before.index}:{before.name}"
            )

    expected_sizes = {
        SABOTEUR_ID: saboteur.size,
        mask_index: mask.size,
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
        "mask_id": mask_index,
        "unchanged_entries": len(entries) - 1 - int(bool(mask_indices)),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    for path in (SOURCE, MASK_SOURCE, REVIEW / "manifest.json"):
        if not path.is_file():
            raise FileNotFoundError(path)

    review_manifest = json.loads(
        (REVIEW / "manifest.json").read_text(encoding="utf-8")
    )
    if review_manifest["status"] != "approval_preview":
        raise AssertionError("saboteur review has not passed validation")
    if review_manifest["failures"]:
        raise AssertionError("saboteur review contains validation failures")

    saboteur4 = Image.open(SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    for name, image in (("saboteur", saboteur4), ("mask", mask4)):
        if image.size != ATLAS_HD4_SIZE:
            raise AssertionError(f"{name} size is {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    saboteur2 = saboteur4.resize(
        ATLAS_HD2_SIZE,
        Image.Resampling.LANCZOS,
    )
    mask2 = mask4.resize(ATLAS_HD2_SIZE, Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    saboteur4.save(
        MASTER_DIR / f"{SABOTEUR_ID:04d}_{RESOURCE_NAME}.png",
        optimize=True,
    )
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            saboteur2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            saboteur4,
            mask4,
        ),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    mask_id = int(builds[0]["mask_id"])
    for resource_id in (SABOTEUR_ID, mask_id):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError("unable to decode packed saboteur resource")
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
        "resource_id": SABOTEUR_ID,
        "resource": RESOURCE_NAME,
        "mask_name": MASK_NAME,
        "mask_id": mask_id,
        "direction_order": review_manifest["direction_order"],
        "animation_rows": review_manifest["rows"],
        "frames": review_manifest["columns"] * review_manifest["rows"],
        "character_height_logical": (
            review_manifest["target_character_height_logical"]
        ),
        "logical_frame": review_manifest["logical_frame"],
        "hd2_frame": [64, 64],
        "hd4_frame": review_manifest["hd4_frame"],
        "changed_ids": [SABOTEUR_ID, mask_id],
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
    except (OSError, AssertionError, ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
