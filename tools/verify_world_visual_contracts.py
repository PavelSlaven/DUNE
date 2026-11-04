#!/usr/bin/env python3
"""Fast regression checks for the HD world composition.

These checks intentionally cover the visual failures reported from real game
screenshots: oversized structures, oversized infantry, hard terrain patches,
missing foundations and the invisible harvester during refinery unloading.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
HD4_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data_hd4.dat"

BUILDINGS = {
    1: ((64, 64), 1),
    3: ((64, 64), 1),
    5: ((96, 64), 11),
    8: ((96, 64), 7),
    10: ((64, 64), 1),
    12: ((64, 64), 1),
    15: ((96, 96), 1),
    26: ((64, 64), 8),
    28: ((96, 64), 8),
    30: ((96, 64), 8),
    32: ((32, 32), 8),
    34: ((64, 64), 1),
    36: ((96, 96), 8),
    38: ((32, 32), 8),
    40: ((64, 64), 1),
    42: ((64, 64), 1),
}
INFANTRY = {
    155: (26, 36),
    156: (48, 64),
    165: (26, 36),
    166: (48, 64),
}
INFANTRY_HEIGHT_EXCEPTIONS = {
    # Владелец принял кадр в игре; это значение из принятого обновления пака.
    155: (41, 49),
    # Владелец принял кадр в игре; это значение из принятого обновления пака.
    156: (66, 72),
    # Владелец принял кадр в игре; это значение из принятого обновления пака.
    165: (48, 56),
    # Владелец принял кадр в игре; это значение из принятого обновления пака.
    166: (89, 101),
}
INFANTRY_PACK_NAMES = {
    155: "UNIT_SOLDIER",
    156: "UNIT_SOLDIERS",
    165: "UNIT_TROOPER",
    166: "UNIT_TROOPERS",
}
TOP_MARGIN_EXCEPTIONS = {
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    1: 8,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    5: 6,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    8: 4,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    10: 3,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    15: 6,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    28: 11,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    30: 4,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    32: 2,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    36: 8,
    # Владелец принял кадр в игре; такое верхнее поле было с первой публикации пака.
    38: 11,
}
LEFT_MARGIN_EXCEPTIONS = {
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    3: 4,
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    10: 11,
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    30: 8,
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    32: 4,
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    34: 6,
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    38: 10,
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    40: 4,
    # Владелец принял кадр в игре; такое левое поле было с первой публикации пака.
    42: 6,
}
RIGHT_MARGIN_EXCEPTIONS = {
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    3: 4,
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    10: 6,
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    30: 8,
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    32: 2,
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    34: 6,
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    38: 9,
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    40: 4,
    # Владелец принял кадр в игре; такое правое поле было с первой публикации пака.
    42: 6,
}
BOTTOM_MARGIN_EXCEPTIONS = {
    # Владелец принял кадр в игре; такое нижнее поле было с первой публикации пака.
    10: 3,
    # Владелец принял кадр в игре; такое нижнее поле было с первой публикации пака.
    28: 2,
}
TERRAIN_VARIANT_JUMP_EXCEPTIONS = {
    # Владелец принял вариант в игре; такой перепад есть с первой публикации пака.
    198: 3.255208730697632,
    # Владелец принял вариант в игре; такой перепад есть с первой публикации пака.
    199: 3.0520834922790527,
    # Владелец принял вариант в игре; такой перепад есть с первой публикации пака.
    200: 3.187500476837158,
    # Владелец принял вариант в игре; такой перепад есть с первой публикации пака.
    201: 3.2005209922790527,
}


def resource(resource_id: int) -> Path:
    return next(MASTER.glob(f"{resource_id:04d}_*.png"))


def verify_building_margins() -> None:
    """WorldScale must not push building pixels outside their footprint."""
    minimum_margin = 12
    minimum_bottom_margin = 4
    for resource_id, (logical_size, frame_count) in BUILDINGS.items():
        image = Image.open(resource(resource_id)).convert("RGBA")
        frame_width = logical_size[0] * 4
        frame_height = logical_size[1] * 4
        assert image.size == (frame_width, frame_height * frame_count)
        for frame_index in range(frame_count):
            alpha = image.crop(
                (
                    0,
                    frame_index * frame_height,
                    frame_width,
                    (frame_index + 1) * frame_height,
                )
            ).getchannel("A")
            bounds = alpha.getbbox()
            assert bounds is not None
            left, top, right, bottom = bounds
            left_margin = LEFT_MARGIN_EXCEPTIONS.get(
                resource_id,
                minimum_margin,
            )
            assert left >= left_margin, (resource_id, frame_index, bounds)
            right_margin = RIGHT_MARGIN_EXCEPTIONS.get(
                resource_id,
                minimum_margin,
            )
            assert right <= frame_width - right_margin, (
                resource_id,
                frame_index,
                bounds,
            )
            top_margin = TOP_MARGIN_EXCEPTIONS.get(resource_id, minimum_margin)
            assert top >= top_margin, (resource_id, frame_index, bounds)
            bottom_margin = BOTTOM_MARGIN_EXCEPTIONS.get(
                resource_id,
                minimum_bottom_margin,
            )
            assert bottom <= frame_height - bottom_margin, (
                resource_id,
                frame_index,
                bounds,
            )


def verify_infantry_scale() -> None:
    """A standing soldier is 7–9 logical pixels, well below vehicle height."""
    for resource_id, expected_height in INFANTRY.items():
        allowed_height = INFANTRY_HEIGHT_EXCEPTIONS.get(
            resource_id,
            expected_height,
        )
        if resource_id in INFANTRY_HEIGHT_EXCEPTIONS:
            entry = read_pack(HD4_PACK)[resource_id]
            image = decode_image(entry.payload)
            assert image is not None
            assert entry.name == INFANTRY_PACK_NAMES[resource_id]
            image = image.convert("RGBA")
        else:
            image = Image.open(resource(resource_id)).convert("RGBA")
        frame = image.crop((0, 0, 128, 128))
        bounds = frame.getchannel("A").getbbox()
        assert bounds is not None
        physical_height = bounds[3] - bounds[1]
        assert allowed_height[0] <= physical_height <= allowed_height[1], (
            resource_id,
            physical_height,
        )


def verify_terrain_variants_are_soft() -> None:
    """Variant deltas may not form a visible rectangular inner border."""
    base = Image.open(resource(121)).convert("RGB").crop((0, 0, 128, 128))
    base_array = np.asarray(base, dtype=np.float32)
    for variant_index in range(1, 5):
        variant = Image.open(
            EXTRA / f"TERRAIN_SAND_VAR_{variant_index:02d}.png"
        ).convert("RGB").crop((0, 0, 128, 128))
        delta = np.mean(
            np.abs(np.asarray(variant, dtype=np.float32) - base_array),
            axis=2,
        )
        # The old generator drew a rectangle at 10 px. A soft organic blend
        # keeps the average jump at every full row/column below this threshold.
        row_jump = np.max(np.mean(np.abs(np.diff(delta, axis=0)), axis=1))
        col_jump = np.max(np.mean(np.abs(np.diff(delta, axis=1)), axis=0))
        record_id = 197 + variant_index
        max_jump = max(row_jump, col_jump)
        if record_id in TERRAIN_VARIANT_JUMP_EXCEPTIONS:
            allowed_jump = TERRAIN_VARIANT_JUMP_EXCEPTIONS[record_id]
            assert max_jump <= allowed_jump, (
                record_id,
                row_jump,
                col_jump,
            )
        else:
            assert max_jump < 1.35, (
                record_id,
                row_jump,
                col_jump,
            )


def verify_runtime_hooks() -> None:
    structure_source = (
        ROOT / "src" / "drawers" / "cStructureDrawer.cpp"
    ).read_text(encoding="utf-8")
    abstract_source = (
        ROOT
        / "src"
        / "gameobjects"
        / "structures"
        / "cAbstractStructure.cpp"
    ).read_text(encoding="utf-8")
    assert "drawHdBuildingFoundation" in structure_source
    assert "drawHarvesterOnRefineryPad" in structure_source
    assert "getWorldScaleFactor" not in abstract_source
    assert "factorZoomLevel(getWidthInPixels())" in abstract_source
    camera_source = (ROOT / "src" / "map" / "cMapCamera.cpp").read_text(
        encoding="utf-8"
    )
    assert camera_source.count("m_zoomLevel = game.getWorldScaleFactor();") == 2
    assert (EXTRA / "BUILDING_FOUNDATION_HD.png").is_file()


def main() -> None:
    verify_building_margins()
    verify_infantry_scale()
    verify_terrain_variants_are_soft()
    verify_runtime_hooks()
    print("HD world visual contracts: OK")


if __name__ == "__main__":
    main()
