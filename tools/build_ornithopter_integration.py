#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved Ornithopter."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "ornithopter_review_v1"
SOURCE = REVIEW / "UNIT_ORNITHOPTER_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "UNIT_ORNITHOPTER_SHADOW_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_UNIT_ORNITHOPTER_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "ornithopter_integration_v1" / "data"

UNIT_ID = 143
SHADOW_ID = 144
UNIT_NAME = "UNIT_ORNITHOPTER"
SHADOW_NAME = "UNIT_ORNITHOPTER_SHADOW"
MASK_NAME = "HM_UNIT_ORNITHOPTER"
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
WING_ROWS = (
    "FOLDED",
    "MID_UP",
    "EXTENDED",
    "MID_DOWN",
)
LOGICAL_FRAME = (48, 48)
HD4_FRAME = (192, 192)
HD4_ATLAS = (1536, 768)
FRAME_COUNT = 32


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


def upsert_named_entry(
    entries: list[PackEntry],
    name: str,
    image: Image.Image,
) -> int:
    indices = [entry.index for entry in entries if entry.name == name]
    if len(indices) > 1:
        raise AssertionError(f"multiple resources named {name}")
    payload = encode_png(image)
    if indices:
        index = indices[0]
        entries[index] = PackEntry(index, name, "PNG", payload)
        return index
    index = len(entries)
    entries.append(PackEntry(index, name, "PNG", payload))
    return index


def atlas_frame(
    atlas: Image.Image,
    column: int,
    row: int,
    frame_size: tuple[int, int],
) -> Image.Image:
    width, height = frame_size
    return atlas.crop(
        (
            column * width,
            row * height,
            (column + 1) * width,
            (row + 1) * height,
        )
    )


def validate_master(
    unit: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("Ornithopter", unit),
        ("shadow", shadow),
        ("house mask", mask),
    ):
        if image.size != HD4_ATLAS:
            raise AssertionError(
                f"{name}: expected {HD4_ATLAS}, got {image.size}"
            )
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    hashes: set[bytes] = set()
    frame_boxes: list[list[list[int]]] = []
    for row in range(4):
        boxes = []
        for column in range(8):
            frame = atlas_frame(unit, column, row, HD4_FRAME)
            box = frame.getchannel("A").getbbox()
            shadow_box = atlas_frame(
                shadow,
                column,
                row,
                HD4_FRAME,
            ).getchannel("A").getbbox()
            if box is None or shadow_box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if (
                box[0] <= 0
                or box[1] <= 0
                or box[2] >= HD4_FRAME[0]
                or box[3] >= HD4_FRAME[1]
            ):
                raise AssertionError(
                    f"frame {column},{row} touches boundary: {box}"
                )
            hashes.add(frame.tobytes())
            boxes.append(list(box))
        frame_boxes.append(boxes)
    if len(hashes) != FRAME_COUNT:
        raise AssertionError("Ornithopter does not contain 32 unique frames")

    mask_alpha = np.asarray(mask.getchannel("A"), dtype=np.float64)
    unit_alpha = np.asarray(unit.getchannel("A"), dtype=np.float64)
    coverage = float(mask_alpha.sum() / max(unit_alpha.sum(), 1.0))
    if not 0.015 <= coverage <= 0.24:
        raise AssertionError(
            f"implausible Ornithopter mask coverage: {coverage:.4f}"
        )

    return {
        "frame_boxes_hd4": frame_boxes,
        "mask_coverage": round(coverage, 5),
    }


def patch_pack(
    base_path: Path,
    output_path: Path,
    unit: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected_names = {
        UNIT_ID: UNIT_NAME,
        SHADOW_ID: SHADOW_NAME,
    }
    for resource_id, expected_name in expected_names.items():
        if resource_id >= len(entries):
            raise AssertionError(f"resource ID {resource_id} is absent")
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"resource ID {resource_id} is not {expected_name}"
            )

    output_entries = list(entries)
    output_entries[UNIT_ID] = replacement_entry(entries[UNIT_ID], unit)
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        shadow,
    )
    mask_id = upsert_named_entry(output_entries, MASK_NAME, mask)
    write_pack(output_path, output_entries)

    packed = read_pack(output_path)
    if len(packed) != len(output_entries):
        raise AssertionError("unexpected output entry count")

    changed_ids = {UNIT_ID, SHADOW_ID, mask_id}
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

    for resource_id, expected_size in (
        (UNIT_ID, unit.size),
        (SHADOW_ID, shadow.size),
        (mask_id, mask.size),
    ):
        packed_image = decode_image(packed[resource_id].payload)
        if packed_image is None or packed_image.size != expected_size:
            raise AssertionError(
                f"packed resource {resource_id} has invalid dimensions"
            )

    return {
        "base": str(base_path),
        "output": str(output_path),
        "entries": len(packed),
        "mask_id": mask_id,
        "changed_ids": sorted(changed_ids),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    for path in (SOURCE, SHADOW_SOURCE, MASK_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    for density in (2, 4):
        pack = GAME / "data" / f"sdl_data_hd{density}.dat"
        if not pack.is_file():
            raise FileNotFoundError(pack)

    unit4 = Image.open(SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    validation = validate_master(unit4, shadow4, mask4)

    hd2_size = (HD4_ATLAS[0] // 2, HD4_ATLAS[1] // 2)
    unit2 = unit4.resize(hd2_size, Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize(hd2_size, Image.Resampling.LANCZOS)
    mask2 = mask4.resize(hd2_size, Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    unit4.save(
        MASTER_DIR / f"{UNIT_ID:04d}_{UNIT_NAME}.png",
        optimize=True,
    )
    shadow4.save(
        MASTER_DIR / f"{SHADOW_ID:04d}_{SHADOW_NAME}.png",
        optimize=True,
    )
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)

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
        raise AssertionError("HD2 and HD4 Ornithopter mask IDs differ")

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    resource_ids = (
        UNIT_ID,
        SHADOW_ID,
        int(builds[0]["mask_id"]),
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
        "resources": {
            "unit": {"id": UNIT_ID, "name": UNIT_NAME},
            "shadow": {"id": SHADOW_ID, "name": SHADOW_NAME},
            "mask": {
                "id": builds[0]["mask_id"],
                "name": MASK_NAME,
            },
        },
        "direction_order": list(DIRECTIONS),
        "wing_rows": list(WING_ROWS),
        "frames": FRAME_COUNT,
        "logical_frame": list(LOGICAL_FRAME),
        "hd2_frame": [96, 96],
        "hd2_atlas": list(hd2_size),
        "hd4_frame": list(HD4_FRAME),
        "hd4_atlas": list(HD4_ATLAS),
        "validation": validation,
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
