#!/usr/bin/env python3
"""Validate density-first world masters and their packed HD2/HD4 copies."""

from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import read_pack


ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
DATA = ROOT / "resources" / "bin" / "data"

BUILDING_IDS = (
    1, 3, 5, 8, 10, 12, 15, 26, 28, 30, 32, 34, 36, 38, 40, 42,
)
UNIT_IDS = (
    130, 132, 134, 137, 139, 141, 143, 145, 147, 150, 151, 153,
    155, 156, 157, 159, 161, 162, 165, 166,
)
DETAIL_IDS = BUILDING_IDS + UNIT_IDS


def classic_path(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def master_path(resource_id: int) -> Path:
    return MASTER / classic_path(resource_id).name


def decode(payload: bytes) -> Image.Image:
    return Image.open(io.BytesIO(payload)).convert("RGBA")


def has_fractional_alpha(image: Image.Image) -> bool:
    extrema = image.getchannel("A").getextrema()
    if extrema == (0, 0) or extrema == (255, 255):
        return False
    return any(0 < value < 255 for value in image.getchannel("A").getdata())


def is_nearest_neighbour_4x(image: Image.Image) -> bool:
    logical = image.resize(
        (image.width // 4, image.height // 4),
        Image.Resampling.NEAREST,
    )
    block_copy = logical.resize(image.size, Image.Resampling.NEAREST)
    return ImageChops.difference(image, block_copy).getbbox() is None


def verify_masters(errors: list[str]) -> None:
    for resource_id in DETAIL_IDS:
        classic = Image.open(classic_path(resource_id))
        master = Image.open(master_path(resource_id)).convert("RGBA")
        expected = (classic.width * 4, classic.height * 4)
        if master.size != expected:
            errors.append(
                f"ID {resource_id}: master {master.size}, expected {expected}"
            )
            continue
        if is_nearest_neighbour_4x(master):
            errors.append(f"ID {resource_id}: master is still a 4x pixel block copy")
        if not has_fractional_alpha(master):
            errors.append(f"ID {resource_id}: master has no antialiased alpha edge")


def verify_packs(errors: list[str]) -> None:
    hd4 = read_pack(DATA / "sdl_data_hd4.dat")
    hd2 = read_pack(DATA / "sdl_data_hd2.dat")
    for resource_id in DETAIL_IDS:
        master = Image.open(master_path(resource_id)).convert("RGBA")
        packed4 = decode(hd4[resource_id].payload)
        if ImageChops.difference(master, packed4).getbbox() is not None:
            errors.append(f"ID {resource_id}: HD4 pack differs from master")

        expected2 = master.resize(
            (master.width // 2, master.height // 2),
            Image.Resampling.LANCZOS,
        )
        packed2 = decode(hd2[resource_id].payload)
        if ImageChops.difference(expected2, packed2).getbbox() is not None:
            errors.append(f"ID {resource_id}: HD2 is not the master4 Lanczos copy")


def main() -> int:
    errors: list[str] = []
    verify_masters(errors)
    verify_packs(errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(
        "ru4-preview2 assets valid: density-first HD4, antialiased edges, "
        "deterministic HD2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
