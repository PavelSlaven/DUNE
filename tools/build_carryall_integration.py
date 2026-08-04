#!/usr/bin/env python3
"""Build and atomically install the approved Carryall in HD2/HD4 packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack
from prepare_carryall_review import build_shadow, neutral_and_mask


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
SOURCE = (
    ROOT
    / "artifacts"
    / "carryall_review_v2"
    / "UNIT_CARRYALL_TOPDOWN_HD4_PREVIEW.png"
)
OUTPUT_ROOT = ROOT / "artifacts" / "carryall_integration_v1"
OUTPUT_DATA = OUTPUT_ROOT / "data"
BACKUP_DATA = OUTPUT_ROOT / "backup"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

UNIT_ID = 130
SHADOW_ID = 131
MASK_NAME = "HM_UNIT_CARRYALL"
MASK_ALIASES = (MASK_NAME, "HOUSEMASK_UNIT_CARRYALL")
RESOURCE_NAMES = {
    UNIT_ID: "UNIT_CARRYALL",
    SHADOW_ID: "UNIT_CARRYALL_SHADOW",
}
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROWS = 2
HD4_FRAME = (192, 192)
HD2_FRAME = (96, 96)
HD4_ATLAS = (1536, 384)
HD2_ATLAS = (768, 192)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frames(atlas: Image.Image, frame: tuple[int, int]) -> list[Image.Image]:
    return [
        atlas.crop(
            (
                column * frame[0],
                row * frame[1],
                (column + 1) * frame[0],
                (row + 1) * frame[1],
            )
        )
        for row in range(ROWS)
        for column in range(len(DIRECTIONS))
    ]


def downscale(atlas: Image.Image) -> Image.Image:
    return atlas.resize(HD2_ATLAS, Image.Resampling.LANCZOS)


def validate_master(
    base: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> None:
    for name, image in (("base", base), ("shadow", shadow), ("mask", mask)):
        if image.size != HD4_ATLAS:
            raise AssertionError(f"{name}: expected {HD4_ATLAS}, got {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")
    base_frames = frames(base, HD4_FRAME)
    if len({frame.tobytes() for frame in base_frames[:8]}) != 8:
        raise AssertionError("empty Carryall row does not have eight directions")
    if len({frame.tobytes() for frame in base_frames[8:]}) != 8:
        raise AssertionError("loaded Carryall row does not have eight directions")
    for index, frame in enumerate(base_frames):
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"Carryall frame {index} is empty")
        if box[0] <= 0 or box[1] <= 0 or box[2] >= 192 or box[3] >= 192:
            raise AssertionError(f"Carryall frame {index} touches boundary: {box}")


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def upsert_mask(entries: list[PackEntry], image: Image.Image) -> int:
    indices = [entry.index for entry in entries if entry.name in MASK_ALIASES]
    if len(indices) > 1:
        raise AssertionError("multiple Carryall house masks")
    if indices:
        index = indices[0]
        entries[index] = PackEntry(index, MASK_NAME, "PNG", encode_png(image))
        return index
    index = len(entries)
    entries.append(PackEntry(index, MASK_NAME, "PNG", encode_png(image)))
    return index


def patch_pack(
    source: Path,
    output: Path,
    base: Image.Image,
    shadow: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(source)
    for resource_id, expected_name in RESOURCE_NAMES.items():
        if resource_id >= len(entries) or entries[resource_id].name != expected_name:
            actual = entries[resource_id].name if resource_id < len(entries) else "missing"
            raise AssertionError(
                f"resource {resource_id} is {actual}, expected {expected_name}"
            )

    patched = list(entries)
    patched[UNIT_ID] = replacement(entries[UNIT_ID], base)
    patched[SHADOW_ID] = replacement(entries[SHADOW_ID], shadow)
    mask_id = upsert_mask(patched, mask)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_pack(output, patched)

    packed = read_pack(output)
    changed = {UNIT_ID, SHADOW_ID, mask_id}
    if len(packed) != len(patched):
        raise AssertionError("entry count changed while patching Carryall")
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
    for resource_id, expected in (
        (UNIT_ID, base),
        (SHADOW_ID, shadow),
        (mask_id, mask),
    ):
        decoded = decode_image(packed[resource_id].payload)
        if decoded is None or decoded.size != expected.size:
            raise AssertionError(f"packed resource {resource_id} is invalid")
    return {
        "source": str(source),
        "output": str(output),
        "entries": len(packed),
        "mask_id": mask_id,
        "changed_ids": sorted(changed),
        "sha256": sha256(output),
        "bytes": output.stat().st_size,
    }


def validate_density_pair(path2: Path, path4: Path, mask_id: int) -> None:
    pack2 = read_pack(path2)
    pack4 = read_pack(path4)
    for resource_id in (UNIT_ID, SHADOW_ID, mask_id):
        image2 = decode_image(pack2[resource_id].payload)
        image4 = decode_image(pack4[resource_id].payload)
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


def install_atomically(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".carryall.tmp")
    try:
        shutil.copy2(source, temporary)
        if sha256(temporary) != sha256(source):
            raise AssertionError(f"temporary copy differs from {source}")
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    if sha256(target) != sha256(source):
        raise AssertionError(f"installed pack differs from {source}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    color4 = Image.open(SOURCE).convert("RGBA")
    if color4.size != HD4_ATLAS:
        raise AssertionError(f"source: expected {HD4_ATLAS}, got {color4.size}")
    base4, mask4 = neutral_and_mask(color4)
    shadow4 = build_shadow(base4)
    validate_master(base4, shadow4, mask4)
    base2, shadow2, mask2 = map(downscale, (base4, shadow4, mask4))

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    base4.save(MASTER_DIR / "0130_UNIT_CARRYALL.png", optimize=True)
    shadow4.save(MASTER_DIR / "0131_UNIT_CARRYALL_SHADOW.png", optimize=True)
    for name in MASK_ALIASES:
        mask4.save(EXTRA_DIR / f"{name}.png", optimize=True)

    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DATA / "sdl_data_hd2.dat",
            base2,
            shadow2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DATA / "sdl_data_hd4.dat",
            base4,
            shadow4,
            mask4,
        ),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 Carryall mask IDs differ")
    mask_id = int(builds[0]["mask_id"])
    validate_density_pair(
        OUTPUT_DATA / "sdl_data_hd2.dat",
        OUTPUT_DATA / "sdl_data_hd4.dat",
        mask_id,
    )

    status = "built_not_installed"
    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install_atomically(
                OUTPUT_DATA / filename,
                GAME / "data" / filename,
                BACKUP_DATA / filename,
            )
        status = "installed"

    manifest = {
        "format": 1,
        "status": status,
        "game": str(GAME),
        "resources": {
            "unit": {"id": UNIT_ID, "name": RESOURCE_NAMES[UNIT_ID]},
            "shadow": {"id": SHADOW_ID, "name": RESOURCE_NAMES[SHADOW_ID]},
            "house_mask": {"id": mask_id, "name": MASK_NAME},
        },
        "direction_order": list(DIRECTIONS),
        "rows": ["empty", "loaded_harvester"],
        "logical_frame": [48, 48],
        "hd2_frame": list(HD2_FRAME),
        "hd4_frame": list(HD4_FRAME),
        "builds": builds,
        "installed_sha256": (
            {
                f"hd{density}": sha256(
                    GAME / "data" / f"sdl_data_hd{density}.dat"
                )
                for density in (2, 4)
            }
            if args.install
            else {}
        ),
    }
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
