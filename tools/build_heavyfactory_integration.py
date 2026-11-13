#!/usr/bin/env python3
"""Install the approved 11-frame Heavy Factory into the HD2/HD4 packs."""

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


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "heavyfactory_review_v1"
OUTPUT_ROOT = ROOT / "artifacts" / "heavyfactory_integration_v1"
OUTPUT_DATA = OUTPUT_ROOT / "data"
BACKUP_DATA = OUTPUT_ROOT / "backup"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"

BUILDING_SOURCE = REVIEW / "BUILD_HEAVYFACTORY_HD4_PREVIEW.png"
FLASH_SOURCE = REVIEW / "BUILD_HEAVYFACTORY_FLASH_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "BUILD_HEAVYFACTORY_SHADOW_HD4_PREVIEW.png"

BUILDING_ID = 5
FLASH_ID = 6
SHADOW_ID = 7
FRAME_COUNT = 11
LOGICAL_FRAME = (96, 64)
HD4_FRAME = (384, 256)
HD2_FRAME = (192, 128)
RESOURCE_NAMES = {
    BUILDING_ID: "BUILD_HEAVYFACTORY",
    FLASH_ID: "BUILD_HEAVYFACTORY_FLASH",
    SHADOW_ID: "BUILD_HEAVYFACTORY_SHADOW",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def load_sources() -> tuple[Image.Image, Image.Image, Image.Image]:
    for path in (BUILDING_SOURCE, FLASH_SOURCE, SHADOW_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    return (
        Image.open(BUILDING_SOURCE).convert("RGBA"),
        Image.open(FLASH_SOURCE).convert("RGBA"),
        Image.open(SHADOW_SOURCE).convert("RGBA"),
    )


def validate_sources(
    building: Image.Image,
    flash: Image.Image,
    shadow: Image.Image,
) -> None:
    expected_atlas = (HD4_FRAME[0], HD4_FRAME[1] * FRAME_COUNT)
    if building.size != expected_atlas:
        raise AssertionError(
            f"Heavy Factory atlas: expected {expected_atlas}, got {building.size}"
        )
    if shadow.size != expected_atlas:
        raise AssertionError(
            f"Heavy Factory shadow: expected {expected_atlas}, got {shadow.size}"
        )
    if flash.size != HD4_FRAME:
        raise AssertionError(
            f"Heavy Factory flash: expected {HD4_FRAME}, got {flash.size}"
        )
    for name, image in (
        ("building", building),
        ("flash", flash),
        ("shadow", shadow),
    ):
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    frames = [
        building.crop(
            (0, index * HD4_FRAME[1], HD4_FRAME[0], (index + 1) * HD4_FRAME[1])
        )
        for index in range(FRAME_COUNT)
    ]
    if len({frame.tobytes() for frame in frames}) != FRAME_COUNT:
        raise AssertionError("Heavy Factory does not contain 11 unique frames")

    # Only the manufacturing cradle may change.  Everything outside this
    # rectangle must remain identical to prevent visual jitter in game.
    animation_bounds = (252, 73, 329, 190)
    static = np.ones((HD4_FRAME[1], HD4_FRAME[0]), dtype=bool)
    x0, y0, x1, y1 = animation_bounds
    static[y0:y1, x0:x1] = False
    baseline = np.asarray(frames[0], dtype=np.int16)
    for index, frame in enumerate(frames[1:], 1):
        delta = np.max(
            np.abs(np.asarray(frame, dtype=np.int16) - baseline),
            axis=2,
        )
        if int(delta[static].max(initial=0)) != 0:
            raise AssertionError(
                f"stationary Heavy Factory pixels changed in frame {index}"
            )


def patch_pack(
    source: Path,
    output: Path,
    replacements: dict[int, Image.Image],
) -> dict[str, object]:
    entries = read_pack(source)
    for resource_id, expected_name in RESOURCE_NAMES.items():
        if resource_id >= len(entries):
            raise AssertionError(f"pack has no resource {resource_id}")
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"resource {resource_id} is {entries[resource_id].name}, "
                f"expected {expected_name}"
            )

    patched = list(entries)
    for resource_id, image in replacements.items():
        patched[resource_id] = replacement(entries[resource_id], image)
    write_pack(output, patched)

    packed = read_pack(output)
    if len(packed) != len(entries):
        raise AssertionError("entry count changed while patching Heavy Factory")
    changed = set(replacements)
    for before, after in zip(entries, packed, strict=True):
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
    for resource_id, image in replacements.items():
        decoded = decode_image(packed[resource_id].payload)
        if decoded is None or decoded.size != image.size:
            raise AssertionError(
                f"packed resource {resource_id} has invalid dimensions"
            )

    return {
        "source": str(source),
        "output": str(output),
        "entries": len(packed),
        "changed_ids": sorted(changed),
        "sha256": sha256(output),
        "bytes": output.stat().st_size,
    }


def install_atomically(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".heavyfactory.tmp")
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
    parser.add_argument(
        "--install",
        action="store_true",
        help="atomically replace the game packs after validation",
    )
    args = parser.parse_args()

    building4, flash4, shadow4 = load_sources()
    validate_sources(building4, flash4, shadow4)
    building2 = building4.resize(
        (HD2_FRAME[0], HD2_FRAME[1] * FRAME_COUNT),
        Image.Resampling.LANCZOS,
    )
    flash2 = flash4.resize(HD2_FRAME, Image.Resampling.LANCZOS)
    shadow2 = shadow4.resize(
        (HD2_FRAME[0], HD2_FRAME[1] * FRAME_COUNT),
        Image.Resampling.LANCZOS,
    )

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    building4.save(MASTER_DIR / "0005_BUILD_HEAVYFACTORY.png", optimize=True)
    flash4.save(MASTER_DIR / "0006_BUILD_HEAVYFACTORY_FLASH.png", optimize=True)
    shadow4.save(MASTER_DIR / "0007_BUILD_HEAVYFACTORY_SHADOW.png", optimize=True)

    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    builds = []
    for density, building, flash, shadow in (
        (2, building2, flash2, shadow2),
        (4, building4, flash4, shadow4),
    ):
        builds.append(
            patch_pack(
                GAME / "data" / f"sdl_data_hd{density}.dat",
                OUTPUT_DATA / f"sdl_data_hd{density}.dat",
                {
                    BUILDING_ID: building,
                    FLASH_ID: flash,
                    SHADOW_ID: shadow,
                },
            )
        )

    # HD2 must be an exact deterministic derivative of the accepted HD4 master.
    packed2 = read_pack(OUTPUT_DATA / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DATA / "sdl_data_hd4.dat")
    for resource_id in RESOURCE_NAMES:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode resource {resource_id}")
        derivative = image4.resize(image2.size, Image.Resampling.LANCZOS)
        difference = ImageChops.difference(
            image2.convert("RGB"),
            derivative.convert("RGB"),
        )
        alpha_difference = ImageChops.difference(
            image2.getchannel("A"),
            derivative.getchannel("A"),
        )
        if difference.getbbox() or alpha_difference.getbbox():
            raise AssertionError(
                f"HD2 resource {resource_id} is not the HD4 derivative"
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
        "resources": [
            {"id": resource_id, "name": name}
            for resource_id, name in RESOURCE_NAMES.items()
        ],
        "frames": FRAME_COUNT,
        "logical_frame": list(LOGICAL_FRAME),
        "hd2_frame": list(HD2_FRAME),
        "hd4_frame": list(HD4_FRAME),
        "animation": "vehicle assembly frames 0 through 10",
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
    (OUTPUT_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
