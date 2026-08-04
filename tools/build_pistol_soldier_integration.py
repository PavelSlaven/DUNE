#!/usr/bin/env python3
"""Install the approved pistol soldier and squad into HD2/HD4 packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
SOURCE = ROOT / "artifacts" / "pistol_soldier_reference_v1"
OUT = ROOT / "artifacts" / "pistol_soldier_integration_v1"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

RESOURCES = {
    155: ("UNIT_SOLDIER", "HM_UNIT_SOLDIER"),
    156: ("UNIT_SOLDIERS", "HM_UNIT_SOLDIERS"),
}
FRAME = 128
ATLAS_SIZE = (1024, 512)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resize_atlas(atlas: Image.Image, density: int) -> Image.Image:
    target_frame = 32 * density
    result = Image.new("RGBA", (target_frame * 8, target_frame * 4))
    for row in range(4):
        for column in range(8):
            frame = atlas.crop(
                (
                    column * FRAME,
                    row * FRAME,
                    (column + 1) * FRAME,
                    (row + 1) * FRAME,
                )
            )
            result.alpha_composite(
                frame.resize(
                    (target_frame, target_frame), Image.Resampling.LANCZOS
                ),
                (column * target_frame, row * target_frame),
            )
    return result


def clamp_mask(mask: Image.Image, unit: Image.Image) -> Image.Image:
    rgba = np.asarray(mask.convert("RGBA"), dtype=np.uint8).copy()
    unit_alpha = np.asarray(unit.getchannel("A"), dtype=np.uint8)
    rgba[:, :, 3] = np.minimum(rgba[:, :, 3], unit_alpha)
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def load_assets() -> dict[int, tuple[Image.Image, Image.Image]]:
    assets: dict[int, tuple[Image.Image, Image.Image]] = {}
    for resource_id, (name, mask_name) in RESOURCES.items():
        unit = Image.open(SOURCE / f"{name}_HD4_PREVIEW.png").convert("RGBA")
        mask = Image.open(SOURCE / f"{mask_name}_HD4_PREVIEW.png").convert("RGBA")
        if unit.size != ATLAS_SIZE or mask.size != ATLAS_SIZE:
            raise AssertionError(f"{name}: invalid HD4 dimensions")
        if unit.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name}: empty atlas")
        assets[resource_id] = (unit, clamp_mask(mask, unit))
    return assets


def patch_pack(
    source: Path,
    output: Path,
    assets: dict[int, tuple[Image.Image, Image.Image]],
) -> dict[str, object]:
    entries = read_pack(source)
    changed: set[int] = set()
    patched = list(entries)
    masks: dict[str, int] = {}
    for resource_id, (name, mask_name) in RESOURCES.items():
        if entries[resource_id].name != name:
            raise AssertionError(
                f"resource {resource_id} is {entries[resource_id].name}, not {name}"
            )
        matches = [entry.index for entry in entries if entry.name == mask_name]
        if len(matches) != 1:
            raise AssertionError(f"expected one {mask_name}, got {len(matches)}")
        mask_id = matches[0]
        unit, mask = assets[resource_id]
        patched[resource_id] = PackEntry(
            resource_id, name, "PNG", encode_png(unit)
        )
        patched[mask_id] = PackEntry(
            mask_id, mask_name, "PNG", encode_png(mask)
        )
        changed.update((resource_id, mask_id))
        masks[mask_name] = mask_id

    output.parent.mkdir(parents=True, exist_ok=True)
    write_pack(output, patched)
    packed = read_pack(output)
    if len(packed) != len(entries):
        raise AssertionError("pack entry count changed")
    for before, after in zip(entries, packed, strict=True):
        if before.index in changed:
            continue
        if (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated entry changed: {before.index}:{before.name}"
            )
    for resource_id, (name, mask_name) in RESOURCES.items():
        unit, mask = assets[resource_id]
        for entry_id, expected, expected_name in (
            (resource_id, unit, name),
            (masks[mask_name], mask, mask_name),
        ):
            decoded = decode_image(packed[entry_id].payload)
            if decoded is None or decoded.size != expected.size:
                raise AssertionError(f"invalid packed resource {expected_name}")
    return {
        "source": str(source),
        "output": str(output),
        "entries": len(packed),
        "changed_ids": sorted(changed),
        "masks": masks,
        "sha256": sha256(output),
    }


def install(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".pistol-soldier.tmp")
    try:
        shutil.copy2(source, temporary)
        if sha256(source) != sha256(temporary):
            raise AssertionError("temporary pack differs from build")
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    if sha256(source) != sha256(target):
        raise AssertionError("installed pack differs from build")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    assets4 = load_assets()
    assets2 = {
        resource_id: (
            resize_atlas(unit, 2),
            clamp_mask(resize_atlas(mask, 2), resize_atlas(unit, 2)),
        )
        for resource_id, (unit, mask) in assets4.items()
    }
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    for resource_id, (name, mask_name) in RESOURCES.items():
        unit4, mask4 = assets4[resource_id]
        unit4.save(MASTER / f"{resource_id:04d}_{name}.png", optimize=True)
        mask4.save(EXTRA / f"{mask_name}.png", optimize=True)

    data = OUT / "data"
    builds = []
    for density, assets in ((2, assets2), (4, assets4)):
        filename = f"sdl_data_hd{density}.dat"
        builds.append(
            patch_pack(GAME / "data" / filename, data / filename, assets)
        )

    status = "built_not_installed"
    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install(
                data / filename,
                GAME / "data" / filename,
                OUT / "backup" / filename,
            )
        status = "installed"

    report = {
        "format": 1,
        "status": status,
        "resources": {
            str(resource_id): {"name": name, "mask": mask_name}
            for resource_id, (name, mask_name) in RESOURCES.items()
        },
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
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
