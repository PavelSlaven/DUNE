#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved Devastator."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "devastator_review_v1"
SOURCE = REVIEW / "UNIT_DEVASTATOR_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "UNIT_DEVASTATOR_SHADOW_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_UNIT_DEVASTATOR_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "devastator_integration_v1" / "data"

UNIT_ID = 132
SHADOW_ID = 133
MASK_NAME = "HM_UNIT_DEVASTATOR"
FRAME_SIZE = (152, 192)
ATLAS_SIZE = (1216, 192)
FRAME_COUNT = 8


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop(
        (
            index * FRAME_SIZE[0],
            0,
            (index + 1) * FRAME_SIZE[0],
            FRAME_SIZE[1],
        )
    )


def validate_master(
    devastator: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("Devastator", devastator),
        ("shadow", shadow),
        ("house mask", mask),
    ):
        if image.size != ATLAS_SIZE:
            raise AssertionError(
                f"{name}: expected {ATLAS_SIZE}, got {image.size}"
            )
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    frames = [frame(devastator, index) for index in range(FRAME_COUNT)]
    if len({item.tobytes() for item in frames}) != FRAME_COUNT:
        raise AssertionError("Devastator does not contain 8 unique directions")

    boxes: list[list[int]] = []
    for index, item in enumerate(frames):
        box = item.getchannel("A").getbbox()
        shadow_box = frame(shadow, index).getchannel("A").getbbox()
        if box is None or shadow_box is None:
            raise AssertionError(f"Devastator frame {index} is empty")
        if (
            box[0] < 0
            or box[1] < 0
            or box[2] > FRAME_SIZE[0]
            or box[3] > FRAME_SIZE[1]
        ):
            raise AssertionError(
                f"Devastator frame {index} touches boundary: {box}"
            )
        boxes.append(list(box))

    return {"frame_boxes_hd4": boxes}


def replacement_entry(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=encode_png(image),
    )


def upsert_mask(
    entries: list[PackEntry],
    image: Image.Image,
) -> int:
    aliases = (MASK_NAME, "HOUSEMASK_UNIT_DEVASTATOR")
    indices = [entry.index for entry in entries if entry.name in aliases]
    if len(indices) > 1:
        raise AssertionError("multiple Devastator house masks")
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
    devastator: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected_names = {
        UNIT_ID: "UNIT_DEVASTATOR",
        SHADOW_ID: "UNIT_DEVASTATOR_SHADOW",
    }
    for resource_id, expected_name in expected_names.items():
        if resource_id >= len(entries):
            raise AssertionError(f"resource ID {resource_id} is absent")
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"resource ID {resource_id} is not {expected_name}"
            )

    output_entries = list(entries)
    output_entries[UNIT_ID] = replacement_entry(
        entries[UNIT_ID],
        devastator,
    )
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        shadow,
    )
    mask_id = upsert_mask(output_entries, mask)

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

    expected_sizes = {
        UNIT_ID: devastator.size,
        SHADOW_ID: shadow.size,
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
        "mask_id": mask_id,
        "changed_ids": sorted(changed_ids),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    required = (SOURCE, SHADOW_SOURCE, MASK_SOURCE)
    if not all(path.is_file() for path in required):
        raise FileNotFoundError("approved Devastator preview is incomplete")

    devastator4 = Image.open(SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    size_validation = validate_master(devastator4, shadow4, mask4)

    hd2_size = (ATLAS_SIZE[0] // 2, ATLAS_SIZE[1] // 2)
    devastator2 = devastator4.resize(hd2_size, Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize(hd2_size, Image.Resampling.LANCZOS)
    mask2 = mask4.resize(hd2_size, Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    devastator4.save(
        MASTER_DIR / "0132_UNIT_DEVASTATOR.png",
        optimize=True,
    )
    shadow4.save(
        MASTER_DIR / "0133_UNIT_DEVASTATOR_SHADOW.png",
        optimize=True,
    )
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            devastator2,
            shadow2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            devastator4,
            shadow4,
            mask4,
        ),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")

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
            raise AssertionError(
                "unable to decode packed Devastator resource"
            )
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
            "unit": {"id": UNIT_ID, "name": "UNIT_DEVASTATOR"},
            "shadow": {
                "id": SHADOW_ID,
                "name": "UNIT_DEVASTATOR_SHADOW",
            },
            "house_mask": {
                "id": builds[0]["mask_id"],
                "name": MASK_NAME,
            },
        },
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "frames": FRAME_COUNT,
        "logical_frame": [38, 48],
        "classic_atlas": [304, 48],
        "hd2_frame": [76, 96],
        "hd2_atlas": [608, 96],
        "hd4_frame": list(FRAME_SIZE),
        "hd4_atlas": list(ATLAS_SIZE),
        "pivot_logical": [19, 24],
        "size_validation": size_validation,
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
