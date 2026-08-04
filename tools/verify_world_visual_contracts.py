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


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

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


def resource(resource_id: int) -> Path:
    return next(MASTER.glob(f"{resource_id:04d}_*.png"))


def verify_building_margins() -> None:
    """WorldScale must not push building pixels outside their footprint."""
    minimum_margin = 12
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
            assert left >= minimum_margin, (resource_id, frame_index, bounds)
            assert right <= frame_width - minimum_margin, (
                resource_id,
                frame_index,
                bounds,
            )
            assert top >= minimum_margin, (resource_id, frame_index, bounds)
            assert bottom <= frame_height - 4, (
                resource_id,
                frame_index,
                bounds,
            )


def verify_infantry_scale() -> None:
    """A standing soldier is 7–9 logical pixels, well below vehicle height."""
    for resource_id, expected_height in INFANTRY.items():
        image = Image.open(resource(resource_id)).convert("RGBA")
        frame = image.crop((0, 0, 128, 128))
        bounds = frame.getchannel("A").getbbox()
        assert bounds is not None
        physical_height = bounds[3] - bounds[1]
        assert expected_height[0] <= physical_height <= expected_height[1], (
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
        assert max(row_jump, col_jump) < 1.35, (
            variant_index,
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
    assert "structureWorldScaleFactor" in abstract_source
    assert (EXTRA / "BUILDING_FOUNDATION_HD.png").is_file()


def main() -> None:
    verify_building_margins()
    verify_infantry_scale()
    verify_terrain_variants_are_soft()
    verify_runtime_hooks()
    print("HD world visual contracts: OK")


if __name__ == "__main__":
    main()
