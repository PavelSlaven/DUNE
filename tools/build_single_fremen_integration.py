#!/usr/bin/env python3
"""Install the approved single Fremen atlas into the HD2/HD4 packs."""

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
REVIEW = ROOT / "artifacts" / "single_fremen_review_v1"
OUTPUT_ROOT = ROOT / "artifacts" / "single_fremen_integration_v1"
OUTPUT_DATA = OUTPUT_ROOT / "data"
BACKUP_DATA = OUTPUT_ROOT / "backup"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

UNIT_SOURCE = REVIEW / "UNIT_SINGLEFREMEN_HD4.png"
MASK_SOURCE = REVIEW / "HM_UNIT_SINGLEFREMEN_HD4.png"
UNIT_ID = 154
UNIT_NAME = "UNIT_SINGLEFREMEN"
MASK_NAME = "HM_UNIT_SINGLEFREMEN"
MASK_ALIASES = (MASK_NAME, "HOUSEMASK_UNIT_SINGLEFREMEN")
HD4_FRAME = (128, 128)
HD2_FRAME = (64, 64)
COLUMNS = 8
ROWS = 4
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
                column * frame_size[0],
                row * frame_size[1],
                (column + 1) * frame_size[0],
                (row + 1) * frame_size[1],
            )
        )
        for row in range(ROWS)
        for column in range(COLUMNS)
    ]


def validate_source(unit: Image.Image, mask: Image.Image) -> None:
    expected = (HD4_FRAME[0] * COLUMNS, HD4_FRAME[1] * ROWS)
    for name, image in (("single Fremen", unit), ("house mask", mask)):
        if image.size != expected:
            raise AssertionError(f"{name}: expected {expected}, got {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    frames = split_frames(unit, HD4_FRAME)
    if len({frame.tobytes() for frame in frames}) != COLUMNS * ROWS:
        raise AssertionError("single Fremen does not contain 32 unique frames")
    for index, frame in enumerate(frames):
        bbox = frame.getchannel("A").getbbox()
        if bbox is None:
            raise AssertionError(f"single Fremen frame {index} is empty")
        if bbox[3] != 100 or bbox[3] - bbox[1] != 64:
            raise AssertionError(
                f"single Fremen frame {index} has invalid anchor/height: {bbox}"
            )

    unit_alpha = np.asarray(unit.getchannel("A"))
    mask_alpha = np.asarray(mask.getchannel("A"))
    if np.any((mask_alpha > 0) & (unit_alpha == 0)):
        raise AssertionError("house mask extends outside the Fremen silhouette")


def downscale(atlas4: Image.Image) -> Image.Image:
    return atlas4.resize(
        (HD2_FRAME[0] * COLUMNS, HD2_FRAME[1] * ROWS),
        Image.Resampling.LANCZOS,
    )


def patch_pack(
    source: Path,
    output: Path,
    unit: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    entries = read_pack(source)
    if UNIT_ID >= len(entries) or entries[UNIT_ID].name != UNIT_NAME:
        actual = entries[UNIT_ID].name if UNIT_ID < len(entries) else "<missing>"
        raise AssertionError(
            f"resource {UNIT_ID} is {actual}, expected {UNIT_NAME}"
        )

    mask_indices = [
        entry.index for entry in entries if entry.name in MASK_ALIASES
    ]
    if len(mask_indices) > 1:
        raise AssertionError("multiple single Fremen house masks")
    mask_id = mask_indices[0] if mask_indices else len(entries)

    patched = list(entries)
    patched[UNIT_ID] = replacement(entries[UNIT_ID], unit)
    mask_entry = PackEntry(mask_id, MASK_NAME, "PNG", encode_png(mask))
    if mask_indices:
        patched[mask_id] = mask_entry
    else:
        patched.append(mask_entry)
    write_pack(output, patched)

    packed = read_pack(output)
    expected_count = len(entries) + (0 if mask_indices else 1)
    if len(packed) != expected_count:
        raise AssertionError(
            f"entry count is {len(packed)}, expected {expected_count}"
        )
    changed = {UNIT_ID, mask_id}
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

    for resource_id, image in ((UNIT_ID, unit), (mask_id, mask)):
        decoded = decode_image(packed[resource_id].payload)
        if decoded is None or decoded.size != image.size:
            raise AssertionError(
                f"packed resource {resource_id} has invalid dimensions"
            )
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
    for resource_id in (UNIT_ID, mask_id):
        image2 = decode_image(pack2[resource_id].payload)
        image4 = decode_image(pack4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode resource {resource_id}")
        derivative = image4.resize(image2.size, Image.Resampling.LANCZOS)
        pixels2 = np.asarray(image2.convert("RGBA"), dtype=np.int16)
        pixels4 = np.asarray(derivative.convert("RGBA"), dtype=np.int16)
        visible = (pixels2[:, :, 3] > 0) | (pixels4[:, :, 3] > 0)
        if (
            np.any(pixels2[:, :, :3][visible] != pixels4[:, :, :3][visible])
            or ImageChops.difference(
                image2.getchannel("A"),
                derivative.getchannel("A"),
            ).getbbox()
        ):
            raise AssertionError(
                f"HD2 resource {resource_id} is not the HD4 derivative"
            )


def install_atomically(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".single-fremen.tmp")
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

    for path in (UNIT_SOURCE, MASK_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    unit4 = Image.open(UNIT_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    validate_source(unit4, mask4)
    unit2 = downscale(unit4)
    mask2 = downscale(mask4)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    unit4.save(MASTER_DIR / "0154_UNIT_SINGLEFREMEN.png", optimize=True)
    mask4.save(EXTRA_DIR / f"{MASK_NAME}.png", optimize=True)

    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DATA / "sdl_data_hd2.dat",
            unit2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DATA / "sdl_data_hd4.dat",
            unit4,
            mask4,
        ),
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")
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
        "resource": {"id": UNIT_ID, "name": UNIT_NAME},
        "mask": {"id": mask_id, "name": MASK_NAME},
        "frames": COLUMNS * ROWS,
        "direction_order": DIRECTION_ORDER,
        "animation_rows": ROWS,
        "logical_frame": [32, 32],
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
