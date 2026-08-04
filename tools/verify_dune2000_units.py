#!/usr/bin/env python3
"""Verify direct Dune 2000 imports before packing them into D2TM."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "source_references" / "ru4"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

DIRECT_IDS = (
    130, 131, 132, 133, 134, 137, 138, 139, 140, 141, 142,
    143, 144, 145, 146, 147, 148, 150, 151, 152, 153, 157,
    158, 159, 160, 161, 162, 163,
)

FRAME_LAYOUTS = {
    130: (8, 2),
    132: (8, 1),
    134: (8, 1),
    137: (8, 4),
    139: (8, 1),
    141: (8, 1),
    143: (8, 4),
    145: (8, 1),
    147: (8, 1),
    150: (1, 5),
    151: (8, 1),
    153: (8, 1),
    157: (8, 1),
    159: (8, 1),
    161: (8, 1),
    162: (8, 1),
}


def classic(index: int) -> Path:
    return next(CLASSIC.glob(f"{index:04d}_*.png"))


def master(index: int) -> Path:
    return MASTER / classic(index).name


def frame_extents(
    image: Image.Image,
    columns: int,
    rows: int,
) -> list[tuple[int, int]]:
    frame_width = image.width // columns
    frame_height = image.height // rows
    result = []
    for index in range(columns * rows):
        x = index % columns * frame_width
        y = index // columns * frame_height
        box = image.crop(
            (x, y, x + frame_width, y + frame_height)
        ).getchannel("A").getbbox()
        if not box:
            result.append((0, 0))
        else:
            result.append((box[2] - box[0], box[3] - box[1]))
    return result


def verify_sources(errors: list[str]) -> None:
    manifest = json.loads((SOURCE / "manifest.json").read_text("utf-8"))
    for entry in manifest["sources"]:
        if not entry["file"].startswith("dune2000_"):
            continue
        path = SOURCE / entry["file"]
        if not path.is_file():
            errors.append(f"missing source: {path.name}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            errors.append(f"source hash mismatch: {path.name}")


def verify_masters(errors: list[str]) -> None:
    for index in DIRECT_IDS:
        classic_image = Image.open(classic(index))
        path = master(index)
        if not path.is_file():
            errors.append(f"missing master for ID {index}")
            continue
        image = Image.open(path).convert("RGBA")
        expected = (classic_image.width * 4, classic_image.height * 4)
        if image.size != expected:
            errors.append(
                f"ID {index}: {image.size}, expected {expected}"
            )
        if any(
            r >= 248 and b >= 248 and g <= 8 and a
            for r, g, b, a in image.getdata()
        ):
            errors.append(f"ID {index}: keyed magenta remains")

    for index, (columns, rows) in FRAME_LAYOUTS.items():
        image = Image.open(master(index)).convert("RGBA")
        extents = frame_extents(image, columns, rows)
        if any(width == 0 or height == 0 for width, height in extents):
            errors.append(f"ID {index}: empty gameplay frame")


def verify_tanks_and_scale(errors: list[str]) -> None:
    for house in ("ATREIDES", "HARKONNEN", "ORDOS"):
        for suffix in ("BASE", "TOP"):
            path = (
                EXTRA
                / f"HOUSEVARIANT_{house}_UNIT_TANK{suffix}.png"
            )
            if not path.is_file():
                errors.append(f"missing tank variant: {path.name}")
                continue
            image = Image.open(path).convert("RGBA")
            if image.size != (1024, 128):
                errors.append(f"{path.name}: unexpected size {image.size}")
            extents = frame_extents(image, 8, 1)
            if any(width == 0 or height == 0 for width, height in extents):
                errors.append(f"{path.name}: empty direction")

    atreides = Image.open(
        EXTRA / "HOUSEVARIANT_ATREIDES_UNIT_TANKBASE.png"
    ).convert("RGBA").resize((256, 32), Image.Resampling.NEAREST)
    tank_max = max(
        max(extent)
        for extent in frame_extents(atreides, 8, 1)
    )
    soldier = Image.open(master(155)).convert("RGBA").resize(
        (256, 128),
        Image.Resampling.NEAREST,
    )
    soldier_height = max(
        height for _width, height in frame_extents(soldier, 8, 4)
    )
    if tank_max < 29:
        errors.append(f"combat tank is too small: {tank_max}px")
    if soldier_height > 16:
        errors.append(f"infantry is too large: {soldier_height}px")
    if tank_max <= soldier_height:
        errors.append("vehicle/infantry relative scale is invalid")


def main() -> int:
    errors: list[str] = []
    verify_sources(errors)
    verify_masters(errors)
    verify_tanks_and_scale(errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(
        "Dune 2000 vehicle masters valid: "
        "14 unit types, 3 combat-tank variants, 8 directions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
