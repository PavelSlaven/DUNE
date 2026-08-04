#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved Trike."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "trike_review_v2"
SOURCE = REVIEW / "UNIT_TRIKE_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "UNIT_TRIKE_SHADOW_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_UNIT_TRIKE_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
OUTPUT_DIR = ROOT / "artifacts" / "trike_integration_v2" / "data"

UNIT_ID = 162
SHADOW_ID = 163
MASK_NAME = "HM_UNIT_TRIKE"
MASK_ALIASES = (MASK_NAME, "HOUSEMASK_UNIT_TRIKE")
VARIANT_NAMES = (
    "HV_A_UNIT_TRIKE",
    "HV_H_UNIT_TRIKE",
    "HV_O_UNIT_TRIKE",
    "HOUSEVARIANT_ATREIDES_UNIT_TRIKE",
    "HOUSEVARIANT_HARKONNEN_UNIT_TRIKE",
    "HOUSEVARIANT_ORDOS_UNIT_TRIKE",
)
FRAME = (112, 104)
ATLAS = (896, 104)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def upsert_mask(entries: list[PackEntry], image: Image.Image) -> int:
    indices = [
        entry.index for entry in entries if entry.name in MASK_ALIASES
    ]
    if len(indices) > 1:
        raise AssertionError("multiple Trike house masks")
    payload = encode_png(image)
    if indices:
        index = indices[0]
        entries[index] = PackEntry(index, MASK_NAME, "PNG", payload)
        return index
    index = len(entries)
    entries.append(PackEntry(index, MASK_NAME, "PNG", payload))
    return index


def patch_pack(
    base_path: Path,
    output_path: Path,
    unit: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected = {
        UNIT_ID: "UNIT_TRIKE",
        SHADOW_ID: "UNIT_TRIKE_SHADOW",
    }
    for resource_id, name in expected.items():
        if resource_id >= len(entries) or entries[resource_id].name != name:
            raise AssertionError(f"resource {resource_id} is not {name}")

    output = list(entries)
    output[UNIT_ID] = replacement(entries[UNIT_ID], unit)
    output[SHADOW_ID] = replacement(entries[SHADOW_ID], shadow)
    variant_ids = []
    for entry in entries:
        if entry.name in VARIANT_NAMES:
            output[entry.index] = replacement(entry, unit)
            variant_ids.append(entry.index)
    mask_id = upsert_mask(output, mask)
    write_pack(output_path, output)

    packed = read_pack(output_path)
    changed = {UNIT_ID, SHADOW_ID, mask_id, *variant_ids}
    for before, after in zip(entries, packed, strict=False):
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

    expected_sizes = {
        UNIT_ID: unit.size,
        SHADOW_ID: shadow.size,
        mask_id: mask.size,
    }
    for resource_id, size in expected_sizes.items():
        decoded = decode_image(packed[resource_id].payload)
        if decoded is None or decoded.size != size:
            raise AssertionError(
                f"packed resource {resource_id} has invalid dimensions"
            )
    return {
        "base": str(base_path),
        "output": str(output_path),
        "entries": len(packed),
        "mask_id": mask_id,
        "variant_ids": variant_ids,
        "changed_ids": sorted(changed),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def validate_master(
    unit: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> None:
    for name, image in (
        ("Trike", unit),
        ("shadow", shadow),
        ("house mask", mask),
    ):
        if image.size != ATLAS:
            raise AssertionError(
                f"{name}: expected {ATLAS}, got {image.size}"
            )
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")
    frames = [
        unit.crop((index * FRAME[0], 0, (index + 1) * FRAME[0], FRAME[1]))
        for index in range(8)
    ]
    if len({item.tobytes() for item in frames}) != 8:
        raise AssertionError("Trike does not contain 8 unique directions")


def main() -> int:
    unit4 = Image.open(SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    validate_master(unit4, shadow4, mask4)

    hd2_size = (ATLAS[0] // 2, ATLAS[1] // 2)
    unit2 = unit4.resize(hd2_size, Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize(hd2_size, Image.Resampling.LANCZOS)
    mask2 = mask4.resize(hd2_size, Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    unit4.save(MASTER_DIR / "0162_UNIT_TRIKE.png", optimize=True)
    shadow4.save(
        MASTER_DIR / "0163_UNIT_TRIKE_SHADOW.png",
        optimize=True,
    )
    for name in MASK_ALIASES:
        mask4.save(EXTRA_DIR / f"{name}.png", optimize=True)
    for name in VARIANT_NAMES:
        path = EXTRA_DIR / f"{name}.png"
        if path.exists():
            unit4.save(path, optimize=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            unit2,
            shadow2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            unit4,
            shadow4,
            mask4,
        ),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    for resource_id in (UNIT_ID, SHADOW_ID, int(builds[0]["mask_id"])):
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode resource {resource_id}")
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
        "resources": {
            "unit": {"id": UNIT_ID, "name": "UNIT_TRIKE"},
            "shadow": {"id": SHADOW_ID, "name": "UNIT_TRIKE_SHADOW"},
            "house_mask": {
                "id": builds[0]["mask_id"],
                "name": MASK_NAME,
            },
        },
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "frames": 8,
        "logical_frame": [28, 26],
        "hd2_frame": [56, 52],
        "hd4_frame": list(FRAME),
        "builds": builds,
    }
    (OUTPUT_DIR.parent / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
