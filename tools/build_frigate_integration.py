#!/usr/bin/env python3
"""Install the approved eight-direction Frigate into the HD2/HD4 packs."""

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
REVIEW = ROOT / "artifacts" / "frigate_review_v1"
OUTPUT_ROOT = ROOT / "artifacts" / "frigate_integration_v1"
OUTPUT_DATA = OUTPUT_ROOT / "data"
BACKUP_DATA = OUTPUT_ROOT / "backup"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"

UNIT_SOURCE = REVIEW / "UNIT_FRIGATE_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "UNIT_FRIGATE_SHADOW_HD4_PREVIEW.png"
UNIT_ID = 135
SHADOW_ID = 136
FRAME_COUNT = 8
HD4_FRAME = (256, 256)
HD2_FRAME = (128, 128)
RESOURCE_NAMES = {
    UNIT_ID: "UNIT_FRIGATE",
    SHADOW_ID: "UNIT_FRIGATE_SHADOW",
}
DIRECTION_ORDER = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def split_frames(
    atlas: Image.Image,
    frame_size: tuple[int, int],
) -> list[Image.Image]:
    return [
        atlas.crop(
            (
                index * frame_size[0],
                0,
                (index + 1) * frame_size[0],
                frame_size[1],
            )
        )
        for index in range(FRAME_COUNT)
    ]


def stack_frames(
    frames: list[Image.Image],
    frame_size: tuple[int, int],
) -> Image.Image:
    atlas = Image.new(
        "RGBA",
        (frame_size[0] * len(frames), frame_size[1]),
        (0, 0, 0, 0),
    )
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * frame_size[0], 0))
    return atlas


def downscale_atlas(atlas4: Image.Image) -> Image.Image:
    frames2 = [
        frame.resize(HD2_FRAME, Image.Resampling.LANCZOS)
        for frame in split_frames(atlas4, HD4_FRAME)
    ]
    return stack_frames(frames2, HD2_FRAME)


def validate_source(unit: Image.Image, shadow: Image.Image) -> None:
    expected = (HD4_FRAME[0] * FRAME_COUNT, HD4_FRAME[1])
    for name, image in (("Frigate", unit), ("shadow", shadow)):
        if image.size != expected:
            raise AssertionError(f"{name}: expected {expected}, got {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")
    frames = split_frames(unit, HD4_FRAME)
    if len({frame.tobytes() for frame in frames}) != FRAME_COUNT:
        raise AssertionError("Frigate does not contain eight unique directions")


def patch_pack(
    source: Path,
    output: Path,
    unit: Image.Image,
    shadow: Image.Image,
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
    patched[UNIT_ID] = replacement(entries[UNIT_ID], unit)
    patched[SHADOW_ID] = replacement(entries[SHADOW_ID], shadow)
    write_pack(output, patched)

    packed = read_pack(output)
    if len(packed) != len(entries):
        raise AssertionError("entry count changed while patching Frigate")
    changed = {UNIT_ID, SHADOW_ID}
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
    for resource_id, image in ((UNIT_ID, unit), (SHADOW_ID, shadow)):
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


def validate_density_pair(path2: Path, path4: Path) -> None:
    pack2 = read_pack(path2)
    pack4 = read_pack(path4)
    for resource_id in RESOURCE_NAMES:
        image2 = decode_image(pack2[resource_id].payload)
        image4 = decode_image(pack4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode resource {resource_id}")
        frames2 = split_frames(image2.convert("RGBA"), HD2_FRAME)
        frames4 = split_frames(image4.convert("RGBA"), HD4_FRAME)
        for index, (frame2, frame4) in enumerate(
            zip(frames2, frames4, strict=True)
        ):
            derivative = frame4.resize(HD2_FRAME, Image.Resampling.LANCZOS)
            alpha_difference = ImageChops.difference(
                frame2.getchannel("A"),
                derivative.getchannel("A"),
            )
            pixels2 = np.asarray(frame2, dtype=np.int16)
            pixels4 = np.asarray(derivative, dtype=np.int16)
            visible = (pixels2[:, :, 3] > 0) | (pixels4[:, :, 3] > 0)
            visible_rgb_differs = bool(
                np.any(pixels2[:, :, :3][visible] != pixels4[:, :, :3][visible])
            )
            # PNG encoders may discard RGB values under alpha=0.  Those bytes
            # are invisible and are intentionally excluded from validation.
            if visible_rgb_differs or alpha_difference.getbbox():
                raise AssertionError(
                    f"HD2 resource {resource_id}, frame {index} "
                    f"is not the HD4 derivative"
                )


def install_atomically(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".frigate.tmp")
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

    for path in (UNIT_SOURCE, SHADOW_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    unit4 = Image.open(UNIT_SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    validate_source(unit4, shadow4)
    unit2 = downscale_atlas(unit4)
    shadow2 = downscale_atlas(shadow4)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    unit4.save(MASTER_DIR / "0135_UNIT_FRIGATE.png", optimize=True)
    shadow4.save(MASTER_DIR / "0136_UNIT_FRIGATE_SHADOW.png", optimize=True)

    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DATA / "sdl_data_hd2.dat",
            unit2,
            shadow2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DATA / "sdl_data_hd4.dat",
            unit4,
            shadow4,
        ),
    ]
    validate_density_pair(
        OUTPUT_DATA / "sdl_data_hd2.dat",
        OUTPUT_DATA / "sdl_data_hd4.dat",
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
        "direction_order": DIRECTION_ORDER,
        "logical_frame": [64, 64],
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
    (OUTPUT_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
