#!/usr/bin/env python3
"""Validate PixVoxel infantry atlases, masks, proportions and naming."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
SOURCE = (
    ROOT
    / "resources"
    / "hd"
    / "source_references"
    / "pixvoxel_infantry"
)
FRAME_SIZE = 128
RESOURCES = {
    155: ("UNIT_SOLDIER", False),
    156: ("UNIT_SOLDIERS", True),
    165: ("UNIT_TROOPER", False),
    166: ("UNIT_TROOPERS", True),
}


def atlas_path(resource_id: int) -> Path:
    return next(MASTER.glob(f"{resource_id:04d}_*.png"))


def frame_metrics(image: Image.Image) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for animation in range(4):
        for direction in range(8):
            frame = image.crop(
                (
                    direction * FRAME_SIZE,
                    animation * FRAME_SIZE,
                    (direction + 1) * FRAME_SIZE,
                    (animation + 1) * FRAME_SIZE,
                )
            )
            alpha = frame.getchannel("A")
            bounds = alpha.getbbox()
            if bounds is None:
                raise AssertionError(
                    f"empty frame direction={direction} animation={animation}"
                )
            opaque_area = sum(
                1 for value in alpha.get_flattened_data() if value > 24
            )
            result.append((bounds[3] - bounds[1], opaque_area))
    return result


def verify_source() -> None:
    source_frames = [
        path
        for projection in ("orthogonal", "isometric")
        for path in (SOURCE / projection).glob("*.png")
    ]
    if len(source_frames) != 64:
        raise AssertionError(
            f"expected 64 selected source frames, found {len(source_frames)}"
        )
    manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    if manifest["d2tm_direction_order"] != [
        "E",
        "NE",
        "N",
        "NW",
        "W",
        "SW",
        "S",
        "SE",
    ]:
        raise AssertionError("D2TM direction order changed")
    if manifest["license"] != "CC0 1.0 / public domain dedication":
        raise AssertionError("PixVoxel license metadata changed")


def verify_atlases() -> None:
    metrics: dict[int, list[tuple[int, int]]] = {}
    for resource_id, (resource_name, is_group) in RESOURCES.items():
        atlas = Image.open(atlas_path(resource_id)).convert("RGBA")
        if atlas.size != (1024, 512):
            raise AssertionError(
                f"{resource_name}: {atlas.size}, expected (1024, 512)"
            )
        mask_path = EXTRA / f"HOUSEMASK_{resource_name}.png"
        mask = Image.open(mask_path).convert("RGBA")
        if mask.size != atlas.size:
            raise AssertionError(
                f"{mask_path.name}: {mask.size}, expected {atlas.size}"
            )
        if mask.getchannel("A").getbbox() is None:
            raise AssertionError(f"{mask_path.name}: empty house-color mask")

        role_metrics = frame_metrics(atlas)
        metrics[resource_id] = role_metrics
        heights = [height for height, _area in role_metrics]
        if is_group:
            if min(heights) < 64 or max(heights) > 90:
                raise AssertionError(
                    f"{resource_name}: group height range {min(heights)}.."
                    f"{max(heights)} is outside 64..90"
                )
        elif min(heights) < 48 or max(heights) > 54:
            raise AssertionError(
                f"{resource_name}: single height range {min(heights)}.."
                f"{max(heights)} is outside 48..54"
            )

    for single_id, group_id in ((155, 156), (165, 166)):
        single_area = sum(area for _height, area in metrics[single_id])
        group_area = sum(area for _height, area in metrics[group_id])
        ratio = group_area / single_area
        if not 2.0 <= ratio <= 3.2:
            raise AssertionError(
                f"group/single opaque-area ratio {ratio:.2f} outside 2.0..3.2"
            )


def verify_runtime_changes() -> None:
    unit_source = (
        ROOT / "src" / "gameobjects" / "units" / "cUnit.cpp"
    ).read_text(encoding="utf-8")
    if "game.getWorldScaleFactor()" not in unit_source:
        raise AssertionError("adaptive HD world scale is not used for units")
    world_scale_source = (
        ROOT / "src" / "utils" / "WorldScale.cpp"
    ).read_text(encoding="utf-8")
    for expected in ("return 100;", "return 110;", "return 125;", "return 150;"):
        if expected not in world_scale_source:
            raise AssertionError(f"missing Auto world scale step: {expected}")

    resource_source = (
        ROOT / "src" / "utils" / "cIniGameRessouces.cpp"
    ).read_text(encoding="utf-8")
    for expected in (
        '"Солдат"',
        '"Отряд автоматчиков"',
        '"Гранатомётчик"',
        '"Отряд гранатомётчиков"',
    ):
        if expected not in resource_source:
            raise AssertionError(f"missing Russian role name {expected}")


def verify_built_packs() -> None:
    for density in (2, 4):
        pack_path = (
            ROOT
            / "resources"
            / "bin"
            / "data"
            / f"sdl_data_hd{density}.dat"
        )
        entries = read_pack(pack_path)
        entries_by_name = {entry.name: entry for entry in entries}
        for resource_id, (resource_name, _is_group) in RESOURCES.items():
            packed = decode_image(entries[resource_id].payload)
            if packed is None:
                raise AssertionError(
                    f"HD{density} {resource_name}: invalid PNG payload"
                )
            master = Image.open(atlas_path(resource_id)).convert("RGBA")
            expected = (
                master
                if density == 4
                else master.resize(
                    (master.width // 2, master.height // 2),
                    Image.Resampling.LANCZOS,
                )
            )
            if ImageChops.difference(
                packed.convert("RGBA"),
                expected,
            ).getbbox():
                raise AssertionError(
                    f"HD{density} {resource_name}: differs from HD4 master"
                )

            mask_name = f"HOUSEMASK_{resource_name}"
            mask_entry = entries_by_name.get(mask_name)
            if mask_entry is None:
                raise AssertionError(
                    f"HD{density}: missing appended resource {mask_name}"
                )
            packed_mask = decode_image(mask_entry.payload)
            if packed_mask is None:
                raise AssertionError(
                    f"HD{density} {mask_name}: invalid PNG payload"
                )


def main() -> None:
    verify_source()
    verify_atlases()
    verify_runtime_changes()
    verify_built_packs()
    print(
        "PixVoxel infantry verified: 4 roles, 8 directions, 4 rows, "
        "smaller people, adaptive HD object scale"
    )


if __name__ == "__main__":
    main()
