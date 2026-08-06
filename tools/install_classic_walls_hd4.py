#!/usr/bin/env python3
"""Install classic wall pixels into density-correct HD4 resources."""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import replace
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import decode_image, encode_png, read_pack, sha256, write_pack


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATA = ROOT / "resources" / "bin" / "data"
GAME_DATA = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data")
OUTPUT = ROOT / "artifacts" / "classic_walls_hd4"
SOURCE_BACKUP = OUTPUT / "backup" / "source"
GAME_BACKUP = (
    Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
    / "backup_before_classic_walls_20260806"
)

RESOURCES = {
    "sdl_data": {
        111: ("PLACE_WALL", ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0111_PLACE_WALL.png"),
        125: ("TERRAIN_WALL", ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0125_TERRAIN_WALL.png"),
    },
    "sdl_inter": {
        48: ("ICON_STR_WALL", ROOT / "resources" / "hd" / "master4" / "sdl_inter" / "0048_ICON_STR_WALL.png"),
    },
}


def classic_hd4_images(pack_stem: str) -> dict[int, Image.Image]:
    classic = read_pack(SOURCE_DATA / f"{pack_stem}.dat")
    hd4 = read_pack(SOURCE_DATA / f"{pack_stem}_hd4.dat")
    result: dict[int, Image.Image] = {}
    for resource_id, (expected_name, _) in RESOURCES[pack_stem].items():
        classic_entry = classic[resource_id]
        hd4_entry = hd4[resource_id]
        if classic_entry.name != expected_name or hd4_entry.name != expected_name:
            raise ValueError(
                f"Resource {resource_id} is not {expected_name}: "
                f"{classic_entry.name}/{hd4_entry.name}"
            )
        source = decode_image(classic_entry.payload)
        current = decode_image(hd4_entry.payload)
        if source is None or current is None:
            raise ValueError(f"Resource {resource_id}:{expected_name} is not an image")
        result[resource_id] = source.convert("RGBA").resize(
            current.size,
            Image.Resampling.NEAREST,
        )
    return result


def patch_pack(
    source: Path,
    destination: Path,
    replacements: dict[int, Image.Image],
) -> dict[str, object]:
    before = read_pack(source)
    after = list(before)
    for resource_id, image in replacements.items():
        entry = before[resource_id]
        after[resource_id] = replace(
            entry,
            extension="PNG",
            payload=encode_png(image),
        )

    temporary = destination.with_suffix(destination.suffix + ".classic-walls.tmp")
    write_pack(temporary, after)
    packed = read_pack(temporary)
    if len(packed) != len(before):
        raise AssertionError(f"Entry count changed in {destination.name}")

    changed: list[dict[str, object]] = []
    for original, current in zip(before, packed, strict=True):
        if original.index not in replacements:
            if original != current:
                raise AssertionError(
                    f"Unrelated resource changed: {destination.name}:{original.index}"
                )
            continue
        expected = replacements[original.index]
        installed = decode_image(current.payload)
        if installed is None or installed.size != expected.size:
            raise AssertionError(
                f"Invalid replacement: {destination.name}:{original.index}"
            )
        if ImageChops.difference(
            installed.convert("RGBA"), expected.convert("RGBA")
        ).getbbox() is not None:
            raise AssertionError(
                f"Pixel mismatch: {destination.name}:{original.index}"
            )
        changed.append(
            {
                "id": original.index,
                "name": original.name,
                "size": list(installed.size),
                "payload_sha256": sha256(current.payload),
            }
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    os.replace(temporary, destination)
    return {
        "path": str(destination),
        "sha256": sha256(destination.read_bytes()),
        "changed": changed,
    }


def backup(path: Path, root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, root / path.name)


def main() -> int:
    if SOURCE_BACKUP.exists() or GAME_BACKUP.exists():
        raise FileExistsError("Classic-wall backup already exists; refusing to overwrite it")

    builds: dict[str, dict[int, Image.Image]] = {
        pack_stem: classic_hd4_images(pack_stem) for pack_stem in RESOURCES
    }

    for pack_stem in RESOURCES:
        pack_name = f"{pack_stem}_hd4.dat"
        backup(SOURCE_DATA / pack_name, SOURCE_BACKUP)
        backup(GAME_DATA / pack_name, GAME_BACKUP)
        for _, master in RESOURCES[pack_stem].values():
            backup(master, SOURCE_BACKUP / "masters")

    reports = []
    for pack_stem, replacements in builds.items():
        pack_name = f"{pack_stem}_hd4.dat"
        source_pack = SOURCE_DATA / pack_name
        reports.append(patch_pack(source_pack, source_pack, replacements))
        game_pack = GAME_DATA / pack_name
        shutil.copy2(source_pack, game_pack)
        if sha256(source_pack.read_bytes()) != sha256(game_pack.read_bytes()):
            raise AssertionError(f"Installed pack differs: {pack_name}")
        for resource_id, image in replacements.items():
            _, master = RESOURCES[pack_stem][resource_id]
            image.save(master, "PNG", optimize=True)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {
        "format": 1,
        "purpose": "Classic concrete-wall visuals in HD4 density-aware packs",
        "method": "Nearest-neighbour 4x scaling; all unrelated pack entries preserved",
        "source_backup": str(SOURCE_BACKUP),
        "game_backup": str(GAME_BACKUP),
        "packs": reports,
    }
    (OUTPUT / "install_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
