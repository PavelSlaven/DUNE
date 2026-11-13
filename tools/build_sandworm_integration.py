#!/usr/bin/env python3
"""Install the approved five-frame Sandworm into the HD2/HD4 packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

from PIL import Image

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "sandworm_review_v1"
OUTPUT_ROOT = ROOT / "artifacts" / "sandworm_integration_v1"
OUTPUT_DATA = OUTPUT_ROOT / "data"
BACKUP_DATA = OUTPUT_ROOT / "backup"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"

SOURCE_HD2 = REVIEW / "UNIT_SANDWORM_HD2.png"
SOURCE_HD4 = REVIEW / "UNIT_SANDWORM_HD4.png"
RESOURCE_ID = 150
RESOURCE_NAME = "UNIT_SANDWORM"
FRAME_COUNT = 5
LOGICAL_FRAME = (48, 48)
HD2_FRAME = (96, 96)
HD4_FRAME = (192, 192)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_vertical(
    atlas: Image.Image,
    frame_size: tuple[int, int],
) -> list[Image.Image]:
    return [
        atlas.crop(
            (
                0,
                index * frame_size[1],
                frame_size[0],
                (index + 1) * frame_size[1],
            )
        )
        for index in range(FRAME_COUNT)
    ]


def validate_source(image: Image.Image, frame_size: tuple[int, int], label: str) -> None:
    expected = (frame_size[0], frame_size[1] * FRAME_COUNT)
    if image.size != expected:
        raise AssertionError(f"{label}: expected {expected}, got {image.size}")
    frames = split_vertical(image, frame_size)
    if any(frame.getchannel("A").getbbox() is None for frame in frames):
        raise AssertionError(f"{label} contains an empty frame")
    if len({frame.tobytes() for frame in frames}) != FRAME_COUNT:
        raise AssertionError(f"{label} does not contain five unique stages")
    for index, frame in enumerate(frames, start=1):
        corners = (
            (0, 0),
            (frame_size[0] - 1, 0),
            (0, frame_size[1] - 1),
            (frame_size[0] - 1, frame_size[1] - 1),
        )
        if any(frame.getpixel(point)[3] != 0 for point in corners):
            raise AssertionError(f"{label} frame {index} has non-transparent corners")


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def patch_pack(source: Path, output: Path, image: Image.Image) -> dict[str, object]:
    entries = read_pack(source)
    if RESOURCE_ID >= len(entries):
        raise AssertionError(f"pack has no resource {RESOURCE_ID}")
    if entries[RESOURCE_ID].name != RESOURCE_NAME:
        raise AssertionError(
            f"resource {RESOURCE_ID} is {entries[RESOURCE_ID].name}, "
            f"expected {RESOURCE_NAME}"
        )

    patched = list(entries)
    patched[RESOURCE_ID] = replacement(entries[RESOURCE_ID], image)
    write_pack(output, patched)

    packed = read_pack(output)
    if len(packed) != len(entries):
        raise AssertionError("entry count changed while patching Sandworm")
    for before, after in zip(entries, packed, strict=True):
        if before.index == RESOURCE_ID:
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

    decoded = decode_image(packed[RESOURCE_ID].payload)
    if decoded is None or decoded.size != image.size:
        raise AssertionError("packed Sandworm has invalid dimensions")
    return {
        "source": str(source),
        "output": str(output),
        "entries": len(packed),
        "changed_ids": [RESOURCE_ID],
        "sha256": sha256(output),
        "bytes": output.stat().st_size,
    }


def validate_packed(path: Path, expected: Image.Image) -> None:
    packed = read_pack(path)
    decoded = decode_image(packed[RESOURCE_ID].payload)
    if decoded is None:
        raise AssertionError(f"cannot decode Sandworm from {path}")
    if decoded.convert("RGBA").tobytes() != expected.convert("RGBA").tobytes():
        raise AssertionError(f"packed Sandworm differs from approved source: {path}")


def install_atomically(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".sandworm.tmp")
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

    for path in (SOURCE_HD2, SOURCE_HD4):
        if not path.is_file():
            raise FileNotFoundError(path)
    image2 = Image.open(SOURCE_HD2).convert("RGBA")
    image4 = Image.open(SOURCE_HD4).convert("RGBA")
    validate_source(image2, HD2_FRAME, "Sandworm HD2")
    validate_source(image4, HD4_FRAME, "Sandworm HD4")

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    image4.save(MASTER_DIR / "0150_UNIT_SANDWORM.png", optimize=True)

    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DATA / "sdl_data_hd2.dat",
            image2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DATA / "sdl_data_hd4.dat",
            image4,
        ),
    ]
    validate_packed(OUTPUT_DATA / "sdl_data_hd2.dat", image2)
    validate_packed(OUTPUT_DATA / "sdl_data_hd4.dat", image4)

    status = "built_not_installed"
    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install_atomically(
                OUTPUT_DATA / filename,
                GAME / "data" / filename,
                BACKUP_DATA / filename,
            )
        validate_packed(GAME / "data" / "sdl_data_hd2.dat", image2)
        validate_packed(GAME / "data" / "sdl_data_hd4.dat", image4)
        status = "installed"

    manifest = {
        "format": 1,
        "status": status,
        "game": str(GAME),
        "resource": {"id": RESOURCE_ID, "name": RESOURCE_NAME},
        "frames": FRAME_COUNT,
        "animation_order": [
            "fully_emerged",
            "retracting",
            "closing",
            "almost_submerged",
            "submerged",
        ],
        "logical_frame": list(LOGICAL_FRAME),
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
