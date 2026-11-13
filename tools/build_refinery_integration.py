#!/usr/bin/env python3
"""Build HD2/HD4 world packs containing the approved refinery."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "refinery_review_v1"
SOURCE = REVIEW / "BUILD_REFINERY_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HOUSEMASK_BUILD_REFINERY_HD4_PREVIEW.png"
FLAG_SOURCE = REVIEW / "BUILD_REFINERY_FLAG_HD4_PREVIEW.png"
FLAG_MASK_SOURCE = (
    REVIEW / "HOUSEMASK_BUILD_REFINERY_FLAG_HD4_PREVIEW.png"
)
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "refinery_integration_v1" / "data"

REFINERY_ID = 28
SHADOW_ID = 29
MASK_NAME = "HM_BUILD_REFINERY"
FLAG_NAME = "BUILD_REFINERY_FLAG"
FLAG_MASK_NAME = "HM_BUILD_REFINERY_FLAG"
FRAME_SIZE = (384, 256)
ATLAS_SIZE = (384, 2048)
FRAME_COUNT = 8


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_shadow(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", ATLAS_SIZE)
    for frame_index in range(FRAME_COUNT):
        top = frame_index * FRAME_SIZE[1]
        frame = atlas.crop((0, top, FRAME_SIZE[0], top + FRAME_SIZE[1]))
        alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(2.2))
        alpha = alpha.point(lambda value: round(value * 0.18))
        silhouette = Image.new("RGBA", FRAME_SIZE, (7, 5, 3, 0))
        silhouette.putalpha(alpha)
        shadow_frame = Image.new("RGBA", FRAME_SIZE)
        shadow_frame.alpha_composite(silhouette, (7, 7))
        result.alpha_composite(shadow_frame, (0, top))
    return result


def replacement_entry(
    entry: PackEntry,
    payload: bytes,
) -> PackEntry:
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
    refinery: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
    flag: Image.Image,
    flag_mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(base_path)
    if len(entries) < 167:
        raise AssertionError(
            f"{base_path}: expected at least 167 entries, got {len(entries)}"
        )
    if entries[REFINERY_ID].name != "BUILD_REFINERY":
        raise AssertionError("resource ID 28 is not BUILD_REFINERY")
    if entries[SHADOW_ID].name != "BUILD_REFINERY_SHADOW":
        raise AssertionError("resource ID 29 is not BUILD_REFINERY_SHADOW")

    mask_indices = [
        entry.index
        for entry in entries
        if entry.name in (MASK_NAME, "HOUSEMASK_BUILD_REFINERY")
    ]
    if len(mask_indices) > 1:
        raise AssertionError("multiple refinery House masks in base pack")

    output_entries = list(entries)
    output_entries[REFINERY_ID] = replacement_entry(
        entries[REFINERY_ID],
        encode_png(refinery),
    )
    output_entries[SHADOW_ID] = replacement_entry(
        entries[SHADOW_ID],
        encode_png(shadow),
    )
    if mask_indices:
        mask_index = mask_indices[0]
        output_entries[mask_index] = PackEntry(
            index=mask_index,
            name=MASK_NAME,
            extension="PNG",
            payload=encode_png(mask),
        )
    else:
        mask_index = len(output_entries)
        output_entries.append(
            PackEntry(
                index=mask_index,
                name=MASK_NAME,
                extension="PNG",
                payload=encode_png(mask),
            )
        )
    flag_index = upsert_named_entry(output_entries, FLAG_NAME, flag)
    flag_mask_index = upsert_named_entry(
        output_entries,
        FLAG_MASK_NAME,
        flag_mask,
    )

    write_pack(output_path, output_entries)
    packed = read_pack(output_path)
    if len(packed) != len(output_entries):
        raise AssertionError("unexpected output entry count")
    changed_ids = {
        REFINERY_ID,
        SHADOW_ID,
        mask_index,
        flag_index,
        flag_mask_index,
    }
    for before, after in zip(entries, packed, strict=False):
        if before.index in changed_ids:
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
        REFINERY_ID: refinery.size,
        SHADOW_ID: shadow.size,
        mask_index: mask.size,
        flag_index: flag.size,
        flag_mask_index: flag_mask.size,
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
        "mask_id": mask_index,
        "flag_id": flag_index,
        "flag_mask_id": flag_mask_index,
        "changed_ids": sorted(changed_ids),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    required = (SOURCE, MASK_SOURCE, FLAG_SOURCE, FLAG_MASK_SOURCE)
    if not all(path.is_file() for path in required):
        raise FileNotFoundError("approved refinery preview is incomplete")

    refinery4 = Image.open(SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    flag4 = Image.open(FLAG_SOURCE).convert("RGBA")
    flag_mask4 = Image.open(FLAG_MASK_SOURCE).convert("RGBA")
    if any(
        image.size != ATLAS_SIZE
        for image in (refinery4, mask4, flag4, flag_mask4)
    ):
        raise AssertionError("approved refinery atlas dimensions changed")
    if refinery4.getchannel("A").getbbox() is None:
        raise AssertionError("approved refinery is fully transparent")
    if mask4.getchannel("A").getbbox() is None:
        raise AssertionError("approved refinery House mask is empty")
    if flag4.getchannel("A").getbbox() is None:
        raise AssertionError("approved refinery flag is empty")
    if flag_mask4.getchannel("A").getbbox() is None:
        raise AssertionError("approved refinery flag mask is empty")

    shadow4 = build_shadow(refinery4)
    refinery2 = refinery4.resize((192, 1024), Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize((192, 1024), Image.Resampling.LANCZOS)
    mask2 = mask4.resize((192, 1024), Image.Resampling.LANCZOS)
    flag2 = flag4.resize((192, 1024), Image.Resampling.LANCZOS)
    flag_mask2 = flag_mask4.resize(
        (192, 1024),
        Image.Resampling.LANCZOS,
    )

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    refinery4.save(MASTER_DIR / "0028_BUILD_REFINERY.png", optimize=True)
    shadow4.save(
        MASTER_DIR / "0029_BUILD_REFINERY_SHADOW.png",
        optimize=True,
    )
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)
    flag4.save(EXTRA_DIR / f"{FLAG_NAME}.png", optimize=True)
    flag_mask4.save(
        EXTRA_DIR / f"{FLAG_MASK_NAME}.png",
        optimize=True,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            refinery2,
            shadow2,
            mask2,
            flag2,
            flag_mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            refinery4,
            shadow4,
            mask4,
            flag4,
            flag_mask4,
        ),
    ]

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    ids = {
        "refinery": REFINERY_ID,
        "shadow": SHADOW_ID,
        "mask": builds[0]["mask_id"],
        "flag": builds[0]["flag_id"],
        "flag_mask": builds[0]["flag_mask_id"],
    }
    if builds[0]["flag_id"] != builds[1]["flag_id"]:
        raise AssertionError("HD2 and HD4 flag IDs differ")
    if builds[0]["flag_mask_id"] != builds[1]["flag_mask_id"]:
        raise AssertionError("HD2 and HD4 flag-mask IDs differ")
    for resource_id in ids.values():
        image2 = decode_image(packed2[int(resource_id)].payload)
        image4 = decode_image(packed4[int(resource_id)].payload)
        if image2 is None or image4 is None:
            raise AssertionError("unable to decode packed refinery resource")
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
        "resource_id": REFINERY_ID,
        "shadow_id": SHADOW_ID,
        "mask_name": MASK_NAME,
        "mask_id": builds[0]["mask_id"],
        "flag_name": FLAG_NAME,
        "flag_id": builds[0]["flag_id"],
        "flag_mask_name": FLAG_MASK_NAME,
        "flag_mask_id": builds[0]["flag_mask_id"],
        "frames": FRAME_COUNT,
        "logical_frame": [96, 64],
        "hd2_frame": [192, 128],
        "hd4_frame": list(FRAME_SIZE),
        "changed_ids": builds[0]["changed_ids"],
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
