#!/usr/bin/env python3
"""Build HD2/HD4 world packs containing the approved combat tank."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "tank_review_v1"
BODY_SOURCE = REVIEW / "UNIT_TANKBASE_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "UNIT_TANKBASE_SHADOW_HD4_PREVIEW.png"
TOP_SOURCE = REVIEW / "UNIT_TANKTOP_HD4_PREVIEW.png"
BODY_MASK_SOURCE = REVIEW / "HM_UNIT_TANKBASE_HD4_PREVIEW.png"
TOP_MASK_SOURCE = REVIEW / "HM_UNIT_TANKTOP_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "tank_integration_v1" / "data"

BODY_ID = 159
SHADOW_ID = 160
TOP_ID = 161
BODY_NAME = "UNIT_TANKBASE"
SHADOW_NAME = "UNIT_TANKBASE_SHADOW"
TOP_NAME = "UNIT_TANKTOP"
BODY_MASK_NAME = "HM_UNIT_TANKBASE"
TOP_MASK_NAME = "HM_UNIT_TANKTOP"
FRAME_SIZE = (128, 128)
ATLAS_SIZE = (1024, 128)
FRAME_COUNT = 8
LOGICAL_FRAME = (32, 32)
PIVOT_LOGICAL = (16, 16)


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


def patch_pack(
    base_path: Path,
    output_path: Path,
    body: Image.Image,
    shadow: Image.Image,
    top: Image.Image,
    body_mask: Image.Image,
    top_mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    expected_names = {
        BODY_ID: BODY_NAME,
        SHADOW_ID: SHADOW_NAME,
        TOP_ID: TOP_NAME,
    }
    for resource_id, expected_name in expected_names.items():
        if resource_id >= len(entries):
            raise AssertionError(f"resource ID {resource_id} is absent")
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"resource ID {resource_id} is not {expected_name}"
            )

    output_entries = list(entries)
    output_entries[BODY_ID] = replacement_entry(entries[BODY_ID], body)
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        shadow,
    )
    output_entries[TOP_ID] = replacement_entry(entries[TOP_ID], top)
    body_mask_id = upsert_named_entry(
        output_entries,
        BODY_MASK_NAME,
        body_mask,
    )
    top_mask_id = upsert_named_entry(
        output_entries,
        TOP_MASK_NAME,
        top_mask,
    )

    write_pack(output_path, output_entries)
    packed = read_pack(output_path)
    if len(packed) != len(output_entries):
        raise AssertionError("unexpected output entry count")

    changed_ids = {
        BODY_ID,
        SHADOW_ID,
        TOP_ID,
        body_mask_id,
        top_mask_id,
    }
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
        BODY_ID: body.size,
        SHADOW_ID: shadow.size,
        TOP_ID: top.size,
        body_mask_id: body_mask.size,
        top_mask_id: top_mask.size,
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
        "body_mask_id": body_mask_id,
        "top_mask_id": top_mask_id,
        "changed_ids": sorted(changed_ids),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


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
    body: Image.Image,
    shadow: Image.Image,
    top: Image.Image,
    body_mask: Image.Image,
    top_mask: Image.Image,
) -> None:
    for name, image in (
        ("body", body),
        ("shadow", shadow),
        ("turret", top),
        ("body mask", body_mask),
        ("turret mask", top_mask),
    ):
        if image.size != ATLAS_SIZE:
            raise AssertionError(
                f"{name}: expected {ATLAS_SIZE}, got {image.size}"
            )
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")
    for name, image in (("body", body), ("turret", top)):
        frames = [frame(image, index) for index in range(FRAME_COUNT)]
        if len({item.tobytes() for item in frames}) != FRAME_COUNT:
            raise AssertionError(f"{name} does not have 8 unique frames")
        for index, item in enumerate(frames):
            box = item.getchannel("A").getbbox()
            if (
                box is None
                or box[0] < 2
                or box[1] < 2
                or box[2] > FRAME_SIZE[0] - 2
                or box[3] > FRAME_SIZE[1] - 2
            ):
                raise AssertionError(
                    f"{name} frame {index} touches its boundary: {box}"
                )


def main() -> int:
    required = (
        BODY_SOURCE,
        SHADOW_SOURCE,
        TOP_SOURCE,
        BODY_MASK_SOURCE,
        TOP_MASK_SOURCE,
    )
    if not all(path.is_file() for path in required):
        raise FileNotFoundError("approved tank preview is incomplete")

    body4 = Image.open(BODY_SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    top4 = Image.open(TOP_SOURCE).convert("RGBA")
    body_mask4 = Image.open(BODY_MASK_SOURCE).convert("RGBA")
    top_mask4 = Image.open(TOP_MASK_SOURCE).convert("RGBA")
    validate_master(body4, shadow4, top4, body_mask4, top_mask4)

    hd2_size = (ATLAS_SIZE[0] // 2, ATLAS_SIZE[1] // 2)
    body2 = body4.resize(hd2_size, Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize(hd2_size, Image.Resampling.LANCZOS)
    top2 = top4.resize(hd2_size, Image.Resampling.LANCZOS)
    body_mask2 = body_mask4.resize(hd2_size, Image.Resampling.LANCZOS)
    top_mask2 = top_mask4.resize(hd2_size, Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    body4.save(
        MASTER_DIR / f"{BODY_ID:04d}_{BODY_NAME}.png",
        optimize=True,
    )
    shadow4.save(
        MASTER_DIR / f"{SHADOW_ID:04d}_{SHADOW_NAME}.png",
        optimize=True,
    )
    top4.save(
        MASTER_DIR / f"{TOP_ID:04d}_{TOP_NAME}.png",
        optimize=True,
    )
    body_mask4.save(
        EXTRA_DIR / f"{BODY_MASK_NAME}.png",
        optimize=True,
    )
    top_mask4.save(
        EXTRA_DIR / f"{TOP_MASK_NAME}.png",
        optimize=True,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            body2,
            shadow2,
            top2,
            body_mask2,
            top_mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            body4,
            shadow4,
            top4,
            body_mask4,
            top_mask4,
        ),
    ]
    if builds[0]["body_mask_id"] != builds[1]["body_mask_id"]:
        raise AssertionError("HD2 and HD4 body-mask IDs differ")
    if builds[0]["top_mask_id"] != builds[1]["top_mask_id"]:
        raise AssertionError("HD2 and HD4 turret-mask IDs differ")

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    resource_ids = (
        BODY_ID,
        SHADOW_ID,
        TOP_ID,
        int(builds[0]["body_mask_id"]),
        int(builds[0]["top_mask_id"]),
    )
    for resource_id in resource_ids:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError("unable to decode packed tank resource")
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
            "body": {"id": BODY_ID, "name": BODY_NAME},
            "shadow": {
                "id": SHADOW_ID,
                "name": SHADOW_NAME,
            },
            "turret": {"id": TOP_ID, "name": TOP_NAME},
            "body_mask": {
                "id": builds[0]["body_mask_id"],
                "name": BODY_MASK_NAME,
            },
            "turret_mask": {
                "id": builds[0]["top_mask_id"],
                "name": TOP_MASK_NAME,
            },
        },
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "frames": FRAME_COUNT,
        "logical_frame": list(LOGICAL_FRAME),
        "classic_atlas": [
            LOGICAL_FRAME[0] * FRAME_COUNT,
            LOGICAL_FRAME[1],
        ],
        "hd2_frame": [
            FRAME_SIZE[0] // 2,
            FRAME_SIZE[1] // 2,
        ],
        "hd2_atlas": [
            ATLAS_SIZE[0] // 2,
            ATLAS_SIZE[1] // 2,
        ],
        "hd4_frame": list(FRAME_SIZE),
        "hd4_atlas": list(ATLAS_SIZE),
        "pivot_logical": list(PIVOT_LOGICAL),
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
