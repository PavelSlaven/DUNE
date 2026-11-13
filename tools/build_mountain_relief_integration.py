#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved volumetric mountains."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "mountain_relief_review_v1"
MASTER4 = REVIEW / "masters_hd4" / "sdl_data"
MASTER2 = REVIEW / "masters_hd2" / "sdl_data"
EXTRA4 = REVIEW / "extras_hd4" / "sdl_data"
EXTRA2 = REVIEW / "extras_hd2" / "sdl_data"
RESOURCE_MASTER = "0119_TERRAIN_MOUNTAIN.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT = ROOT / "artifacts" / "mountain_relief_integration_v1"
OUTPUT_DATA = OUTPUT / "data"
BACKUP = OUTPUT / "backup_before_install"

RESOURCE_ID = 119
RESOURCE_NAME = "TERRAIN_MOUNTAIN"
VARIANT_NAMES = tuple(
    f"TERRAIN_MOUNTAIN_VAR_{index:02d}" for index in range(1, 5)
)
HD4_SIZE = (2176, 128)
HD2_SIZE = (1088, 64)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=encode_png(image),
    )


def load_sources(
    density: int,
) -> tuple[Image.Image, dict[str, Image.Image]]:
    if density == 4:
        master_folder, extra_folder, expected = MASTER4, EXTRA4, HD4_SIZE
    elif density == 2:
        master_folder, extra_folder, expected = MASTER2, EXTRA2, HD2_SIZE
    else:
        raise AssertionError(f"unsupported density {density}")
    master = Image.open(master_folder / RESOURCE_MASTER).convert("RGBA")
    variants = {
        name: Image.open(extra_folder / f"{name}.png").convert("RGBA")
        for name in VARIANT_NAMES
    }
    for name, image in ((RESOURCE_NAME, master), *variants.items()):
        if image.size != expected:
            raise AssertionError(
                f"{name}: size {image.size}, expected {expected}"
            )
        if image.getchannel("A").getbbox() != (0, 0, *expected):
            raise AssertionError(f"{name}: unexpected transparent pixels")
    return master, variants


def patch_pack(
    base_path: Path,
    output_path: Path,
    master: Image.Image,
    variants: dict[str, Image.Image],
    density: int,
) -> dict[str, object]:
    before = read_pack(base_path)
    if before[RESOURCE_ID].name != RESOURCE_NAME:
        raise AssertionError(
            f"HD{density} ID {RESOURCE_ID} is "
            f"{before[RESOURCE_ID].name}, expected {RESOURCE_NAME}"
        )
    by_name = {entry.name: entry.index for entry in before}
    missing = [name for name in VARIANT_NAMES if name not in by_name]
    if missing:
        raise AssertionError(f"HD{density} variants are absent: {missing}")

    entries = list(before)
    entries[RESOURCE_ID] = replacement(entries[RESOURCE_ID], master)
    changed_ids = {RESOURCE_ID}
    for name, image in variants.items():
        index = by_name[name]
        entries[index] = replacement(entries[index], image)
        changed_ids.add(index)
    write_pack(output_path, entries)

    packed = read_pack(output_path)
    if len(packed) != len(before):
        raise AssertionError("mountain patch changed entry count")
    for old, new in zip(before, packed, strict=True):
        if old.index in changed_ids:
            continue
        if (
            old.index != new.index
            or old.name != new.name
            or old.extension != new.extension
            or old.payload != new.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {old.index}:{old.name}"
            )
    expected_images = {RESOURCE_NAME: master, **variants}
    packed_by_name = {entry.name: entry for entry in packed}
    for name, expected in expected_images.items():
        actual = decode_image(packed_by_name[name].payload)
        if actual is None or ImageChops.difference(
            actual.convert("RGBA"),
            expected,
        ).getbbox():
            raise AssertionError(f"packed HD{density} {name} differs")
    return {
        "density": density,
        "base": str(base_path),
        "base_sha256": sha256(base_path),
        "output": str(output_path),
        "output_sha256": sha256(output_path),
        "entries": len(packed),
        "changed_ids": sorted(changed_ids),
    }


def verify_density_pair(
    master2: Image.Image,
    variants2: dict[str, Image.Image],
    master4: Image.Image,
    variants4: dict[str, Image.Image],
) -> None:
    for name, image4 in ((RESOURCE_NAME, master4), *variants4.items()):
        image2 = master2 if name == RESOURCE_NAME else variants2[name]
        expected2 = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(image2, expected2).getbbox():
            raise AssertionError(f"{name}: HD2 is not the HD4 derivative")


def main() -> int:
    master2, variants2 = load_sources(2)
    master4, variants4 = load_sources(4)
    verify_density_pair(master2, variants2, master4, variants4)

    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(parents=True, exist_ok=True)
    for density in (2, 4):
        source = GAME / "data" / f"sdl_data_hd{density}.dat"
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, BACKUP / source.name)

    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DATA / "sdl_data_hd2.dat",
            master2,
            variants2,
            2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DATA / "sdl_data_hd4.dat",
            master4,
            variants4,
            4,
        ),
    ]

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    master4.save(MASTER_DIR / RESOURCE_MASTER, optimize=True)
    for name, image in variants4.items():
        image.save(EXTRA_DIR / f"{name}.png", optimize=True)

    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "resource_id": RESOURCE_ID,
        "resource_name": RESOURCE_NAME,
        "frames": 17,
        "variants": list(VARIANT_NAMES),
        "hd2_size": list(HD2_SIZE),
        "hd4_size": list(HD4_SIZE),
        "builds": builds,
        "backup": str(BACKUP),
    }
    (OUTPUT / "manifest.json").write_text(
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
