#!/usr/bin/env python3
"""Build HD2/HD4 world packs containing the approved wind trap."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "windtrap_review_v1"
SOURCE = REVIEW / "BUILD_WINDTRAP_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "BUILD_WINDTRAP_SHADOW_HD4_PREVIEW.png"
FLAG_SOURCE = REVIEW / "BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "windtrap_integration_v1" / "data"

WINDTRAP_ID = 40
SHADOW_ID = 41
FLAG_NAME = "BUILD_WINDTRAP_FLAG"
MASK_NAME = "HM_BUILD_WINDTRAP_FLAG"
FRAME_SIZE = (256, 256)
ATLAS_SIZE = (256, 2048)
FRAME_COUNT = 8


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement_entry(entry: PackEntry, payload: bytes) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=payload,
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
    building: Image.Image,
    shadow: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    if len(entries) < 167:
        raise AssertionError(
            f"{base_path}: expected at least 167 entries, got {len(entries)}"
        )
    if entries[WINDTRAP_ID].name != "BUILD_WINDTRAP":
        raise AssertionError("resource ID 40 is not BUILD_WINDTRAP")
    if entries[SHADOW_ID].name != "BUILD_WINDTRAP_SHADOW":
        raise AssertionError("resource ID 41 is not BUILD_WINDTRAP_SHADOW")

    output_entries = list(entries)
    output_entries[WINDTRAP_ID] = replacement_entry(
        entries[WINDTRAP_ID],
        encode_png(building),
    )
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        encode_png(shadow),
    )
    flag_id = upsert_named_entry(output_entries, FLAG_NAME, flag)
    mask_id = upsert_named_entry(output_entries, MASK_NAME, mask)

    write_pack(output_path, output_entries)
    packed = read_pack(output_path)
    if len(packed) != len(output_entries):
        raise AssertionError("unexpected output entry count")

    changed_ids = {WINDTRAP_ID, SHADOW_ID, flag_id, mask_id}
    before_by_name = {entry.name: entry for entry in entries}
    after_by_name = {entry.name: entry for entry in packed}
    for name, before in before_by_name.items():
        after = after_by_name.get(name)
        if after is None:
            raise AssertionError(f"resource disappeared: {name}")
        if before.index in changed_ids:
            continue
        if (
            before.index != after.index
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {before.index}:{name}"
            )

    expected = {
        WINDTRAP_ID: building.size,
        SHADOW_ID: shadow.size,
        flag_id: flag.size,
        mask_id: mask.size,
    }
    for index, size in expected.items():
        image = decode_image(packed[index].payload)
        if image is None or image.size != size:
            raise AssertionError(
                f"packed resource {index} has invalid dimensions"
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


def main() -> int:
    required = (SOURCE, SHADOW_SOURCE, FLAG_SOURCE, MASK_SOURCE)
    if not all(path.is_file() for path in required):
        raise FileNotFoundError("approved wind trap preview is incomplete")

    building4 = Image.open(SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    flag4 = Image.open(FLAG_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    if building4.size != FRAME_SIZE or shadow4.size != FRAME_SIZE:
        raise AssertionError("approved wind trap dimensions changed")
    if flag4.size != ATLAS_SIZE or mask4.size != ATLAS_SIZE:
        raise AssertionError("approved flag atlas dimensions changed")
    for name, image in (
        ("building", building4),
        ("shadow", shadow4),
        ("flag", flag4),
        ("mask", mask4),
    ):
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"approved {name} is fully transparent")

    building2 = building4.resize((128, 128), Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize((128, 128), Image.Resampling.LANCZOS)
    flag2 = flag4.resize((128, 1024), Image.Resampling.LANCZOS)
    mask2 = mask4.resize((128, 1024), Image.Resampling.LANCZOS)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    building4.save(MASTER_DIR / "0040_BUILD_WINDTRAP.png", optimize=True)
    shadow4.save(
        MASTER_DIR / "0041_BUILD_WINDTRAP_SHADOW.png",
        optimize=True,
    )
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

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    ids = (
        WINDTRAP_ID,
        SHADOW_ID,
        int(builds[0]["flag_id"]),
        int(builds[0]["mask_id"]),
    )
    if builds[0]["flag_id"] != builds[1]["flag_id"]:
        raise AssertionError("HD2 and HD4 flag IDs differ")
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")
    for resource_id in ids:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError("unable to decode packed wind trap resource")
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
        "resource_id": WINDTRAP_ID,
        "shadow_id": SHADOW_ID,
        "flag_name": FLAG_NAME,
        "flag_id": builds[0]["flag_id"],
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "frames": FRAME_COUNT,
        "logical_frame": [64, 64],
        "hd2_frame": [128, 128],
        "hd4_frame": list(FRAME_SIZE),
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
