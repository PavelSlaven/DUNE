#!/usr/bin/env python3
"""Regression checks for the ru4 directional sprites and terrain masters."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageStat

from build_dune2000_units import eight_directions


ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"


def resource(folder: Path, index: int) -> Path:
    return next(folder.glob(f"{index:04d}_*.png"))


def wrapped_error(left: float, right: float) -> float:
    return abs((left - right + 180.0) % 360.0 - 180.0)


def subject_angle(frame: Image.Image) -> float:
    alpha = frame.convert("RGBA").getchannel("A")
    points = [
        (x, y, alpha.getpixel((x, y)))
        for y in range(alpha.height)
        for x in range(alpha.width)
        if alpha.getpixel((x, y)) > 64
    ]
    if not points:
        raise AssertionError("directional frame is empty")

    total = sum(weight for _x, _y, weight in points)
    center_x = sum(x * weight for x, _y, weight in points) / total
    center_y = sum(y * weight for _x, y, weight in points) / total
    points.sort(
        key=lambda point: (
            (point[0] - center_x) ** 2 + (point[1] - center_y) ** 2
        ),
        reverse=True,
    )
    far = points[: max(1, len(points) // 8)]
    far_total = sum(weight for _x, _y, weight in far)
    far_x = sum(x * weight for x, _y, weight in far) / far_total
    far_y = sum(y * weight for _x, y, weight in far) / far_total
    return math.degrees(math.atan2(far_y - center_y, far_x - center_x))


def atlas_angles(
    path: Path,
    frame_width: int,
    frame_height: int,
    columns: int,
) -> list[float]:
    atlas = Image.open(path).convert("RGBA")
    return [
        subject_angle(
            atlas.crop(
                (
                    column * frame_width,
                    0,
                    (column + 1) * frame_width,
                    frame_height,
                )
            )
        )
        for column in range(columns)
    ]


def verify_direction_selector() -> None:
    synthetic = [
        Image.new("L", (1, 1), index)
        for index in range(32)
    ]
    selected = [
        frame.getpixel((0, 0))
        for frame in eight_directions(synthetic)
    ]
    assert selected == [8, 4, 0, 28, 24, 20, 16, 12], (
        "Dune 2000 frames are not converted to D2TM's "
        "E, NE, N, NW, W, SW, S, SE order"
    )


def verify_tank_turret_directions() -> None:
    classic_angles = atlas_angles(resource(CLASSIC, 161), 32, 32, 8)
    hd_angles = atlas_angles(resource(MASTER, 161), 128, 128, 8)
    errors = [
        round(wrapped_error(classic_angle, hd_angle))
        for classic_angle, hd_angle in zip(classic_angles, hd_angles)
    ]
    assert max(errors) <= 25, (
        f"tank turret frame order differs from classic D2TM: {errors}"
    )


def verify_large_rocket_directions() -> None:
    classic_angles = atlas_angles(resource(CLASSIC, 50), 48, 48, 16)
    hd_angles = atlas_angles(resource(MASTER, 50), 192, 192, 16)
    errors = [
        round(wrapped_error(classic_angle, hd_angle))
        for classic_angle, hd_angle in zip(classic_angles, hd_angles)
    ]
    assert max(errors) <= 18, (
        f"large rocket frames do not match the engine's 16 directions: {errors}"
    )


def edge_error(image: Image.Image) -> float:
    rgb = image.convert("RGB")
    left = rgb.crop((0, 0, 1, rgb.height))
    right = rgb.crop((rgb.width - 1, 0, rgb.width, rgb.height))
    top = rgb.crop((0, 0, rgb.width, 1))
    bottom = rgb.crop((0, rgb.height - 1, rgb.width, rgb.height))
    return max(
        *ImageStat.Stat(ImageChops.difference(left, right)).mean,
        *ImageStat.Stat(ImageChops.difference(top, bottom)).mean,
    )


def high_frequency_error(image: Image.Image) -> float:
    rgb = image.convert("RGB")
    blurred = rgb.filter(ImageFilter.GaussianBlur(2.0))
    return max(ImageStat.Stat(ImageChops.difference(rgb, blurred)).mean)


def verify_sand_variants() -> None:
    variants = [resource(MASTER, 121)]
    variants.extend(sorted(EXTRA.glob("TERRAIN_SAND_VAR_*.png")))
    assert len(variants) >= 5, "sand needs a base texture and four variants"

    opened = [Image.open(path).convert("RGB") for path in variants]
    for path, image in zip(variants, opened):
        assert image.size == (128, 128), (
            f"{path.name}: expected one 32x32 logical HD4 tile"
        )
        assert edge_error(image) <= 6.0, (
            f"{path.name}: opposite edges are visibly discontinuous"
        )
        assert high_frequency_error(image) <= 10.0, (
            f"{path.name}: terrain contains too much high-frequency detail"
        )

    base = opened[0]
    assert all(
        ImageStat.Stat(ImageChops.difference(base, variant)).rms[0] >= 2.0
        for variant in opened[1:]
    ), "sand variants are visually identical"

    base_edges = (
        base.crop((0, 0, 1, 128)),
        base.crop((127, 0, 128, 128)),
        base.crop((0, 0, 128, 1)),
        base.crop((0, 127, 128, 128)),
    )
    for path, variant in zip(variants[1:], opened[1:]):
        variant_edges = (
            variant.crop((0, 0, 1, 128)),
            variant.crop((127, 0, 128, 128)),
            variant.crop((0, 0, 128, 1)),
            variant.crop((0, 127, 128, 128)),
        )
        mismatch = max(
            max(ImageStat.Stat(ImageChops.difference(a, b)).mean)
            for a, b in zip(base_edges, variant_edges)
        )
        assert mismatch <= 1.0, (
            f"{path.name}: variants do not share a common seamless border"
        )


def main() -> None:
    verify_direction_selector()
    verify_tank_turret_directions()
    verify_large_rocket_directions()
    verify_sand_variants()
    print("ru4 world assets: direction, projectile and terrain checks passed")


if __name__ == "__main__":
    main()
