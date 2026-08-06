#!/usr/bin/env python3
"""Make the launcher north frame the exact vertical mirror of south."""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import replace
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import decode_image, encode_png, read_pack, sha256, write_pack


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data_hd4.dat"
GAME_ROOT = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
GAME_PACK = GAME_ROOT / "data" / "sdl_data_hd4.dat"
OUTPUT = ROOT / "artifacts" / "launcher_north_mirror_fix"
SOURCE_BACKUP = OUTPUT / "backup" / "source"
GAME_BACKUP = GAME_ROOT / "backup_before_launcher_north_mirror_20260806"

FRAME = 128
NORTH = 2
SOUTH = 6
PACK_RESOURCES = {
    139: "UNIT_LAUNCHER",
    140: "UNIT_LAUNCHER_SHADOW",
    179: "HM_UNIT_LAUNCHER",
}
MASTER_FILES = (
    ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0139_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0140_UNIT_LAUNCHER_SHADOW.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HM_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HOUSEMASK_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HV_A_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HV_H_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HV_O_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HOUSEVARIANT_ATREIDES_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HOUSEVARIANT_HARKONNEN_UNIT_LAUNCHER.png",
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HOUSEVARIANT_ORDOS_UNIT_LAUNCHER.png",
)
REVIEW_FILES = (
    ROOT / "artifacts" / "launcher_review_v1" / "UNIT_LAUNCHER_HD4_PREVIEW.png",
    ROOT / "artifacts" / "launcher_review_v1" / "UNIT_LAUNCHER_SHADOW_HD4_PREVIEW.png",
    ROOT / "artifacts" / "launcher_review_v1" / "HM_UNIT_LAUNCHER_HD4_PREVIEW.png",
)


def mirror_north(atlas: Image.Image) -> Image.Image:
    if atlas.size != (FRAME * 8, FRAME):
        raise ValueError(f"Unexpected launcher atlas size: {atlas.size}")
    result = atlas.convert("RGBA").copy()
    south = result.crop(
        (SOUTH * FRAME, 0, (SOUTH + 1) * FRAME, FRAME)
    )
    north = south.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    result.paste(north, (NORTH * FRAME, 0))
    return result


def is_mirrored(atlas: Image.Image) -> bool:
    north = atlas.crop(
        (NORTH * FRAME, 0, (NORTH + 1) * FRAME, FRAME)
    ).convert("RGBA")
    south = atlas.crop(
        (SOUTH * FRAME, 0, (SOUTH + 1) * FRAME, FRAME)
    ).transpose(Image.Transpose.FLIP_TOP_BOTTOM).convert("RGBA")
    return ImageChops.difference(north, south).getbbox() is None


def patch_pack(path: Path) -> dict[str, object]:
    before = read_pack(path)
    after = list(before)
    for resource_id, expected_name in PACK_RESOURCES.items():
        entry = before[resource_id]
        if entry.name != expected_name:
            raise ValueError(
                f"ID {resource_id}: expected {expected_name}, got {entry.name}"
            )
        image = decode_image(entry.payload)
        if image is None:
            raise ValueError(f"{expected_name} is not an image")
        fixed = mirror_north(image)
        after[resource_id] = replace(
            entry,
            extension="PNG",
            payload=encode_png(fixed),
        )

    temporary = path.with_suffix(path.suffix + ".launcher-north.tmp")
    write_pack(temporary, after)
    packed = read_pack(temporary)
    changed = []
    for original, current in zip(before, packed, strict=True):
        if original.index not in PACK_RESOURCES:
            if original != current:
                raise AssertionError(
                    f"Unrelated pack entry changed: {original.index}:{original.name}"
                )
            continue
        image = decode_image(current.payload)
        if image is None or not is_mirrored(image):
            raise AssertionError(
                f"North frame is still wrong: {current.index}:{current.name}"
            )
        changed.append({"id": current.index, "name": current.name})
    os.replace(temporary, path)
    return {"path": str(path), "changed": changed, "sha256": sha256(path.read_bytes())}


def backup(path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination / path.name)


def patch_png(path: Path) -> None:
    with Image.open(path) as image:
        fixed = mirror_north(image)
    fixed.save(path, "PNG", optimize=True)
    with Image.open(path) as installed:
        if not is_mirrored(installed):
            raise AssertionError(f"Master was not fixed: {path}")


def main() -> int:
    if SOURCE_BACKUP.exists() or GAME_BACKUP.exists():
        raise FileExistsError("Launcher north-frame backup already exists")
    if sha256(SOURCE_PACK.read_bytes()) != sha256(GAME_PACK.read_bytes()):
        raise AssertionError("Source and installed HD4 data packs differ before the fix")

    backup(SOURCE_PACK, SOURCE_BACKUP)
    backup(GAME_PACK, GAME_BACKUP)
    for path in MASTER_FILES:
        if path.is_file():
            backup(path, SOURCE_BACKUP / "masters")

    report = patch_pack(SOURCE_PACK)
    shutil.copy2(SOURCE_PACK, GAME_PACK)
    if sha256(SOURCE_PACK.read_bytes()) != sha256(GAME_PACK.read_bytes()):
        raise AssertionError("Installed HD4 data pack differs from source")

    updated_masters = []
    for path in (*MASTER_FILES, *REVIEW_FILES):
        if path.is_file():
            patch_png(path)
            updated_masters.append(str(path))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = {
        "format": 1,
        "purpose": "Launcher north frame mirrors south vertically",
        "pack": report,
        "updated_masters": updated_masters,
        "source_backup": str(SOURCE_BACKUP),
        "game_backup": str(GAME_BACKUP),
    }
    (OUTPUT / "install_report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
