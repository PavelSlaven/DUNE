#!/usr/bin/env python3
"""Regression audit for Deviator direction scale and HD building markers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

from hd_assets import decode_image, read_pack


GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
DEVIATOR_ID = 134
MAX_AREA_RATIO_OVER_CLASSIC = 0.15
MAX_NEAREST_SIMILARITY = 0.985
FORBIDDEN_HOUSE_BEACONS = (
    "HOUSE_BEACON_ATREIDES",
    "HOUSE_BEACON_HARKONNEN",
    "HOUSE_BEACON_ORDOS",
)
SPECIAL_FLAGS = (
    "BUILD_WINDTRAP_FLAG",
    "BUILD_REFINERY_FLAG",
    "BUILD_CONSTYARD_FLAG",
    "BUILD_SILO_FLAG",
    "BUILD_BARRACKS_FLAG",
    "BUILD_RADAR_FLAG",
    "BUILD_STARPORT_FLAG",
    "BUILD_PALACE_FLAG",
    "BUILD_IX_FLAG",
    "BUILD_LIGHTFACTORY_FLAG",
    "BUILD_WOR_FLAG",
    "BUILD_HIGHTECH_FLAG",
)
GENERIC_FLAGS = (
    (44, "BUILDING_FLAG_LARGE", "HM_BUILDING_FLAG_LARGE"),
    (45, "BUILDING_FLAG_SMALL", "HM_BUILDING_FLAG_SMALL"),
)
ROOT = Path(__file__).resolve().parents[1]


def alpha_major(frame: Image.Image, density: int) -> float:
    box = frame.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("transparent frame")
    return max(box[2] - box[0], box[3] - box[1]) / density


def direction_scales(classic: Image.Image, hd4: Image.Image) -> list[float]:
    classic_width = classic.width // 8
    hd_width = hd4.width // 8
    return [
        alpha_major(
            hd4.crop((index * hd_width, 0, (index + 1) * hd_width, hd4.height)),
            4,
        )
        / alpha_major(
            classic.crop(
                (
                    index * classic_width,
                    0,
                    (index + 1) * classic_width,
                    classic.height,
                )
            ),
            1,
        )
        for index in range(8)
    ]


def direction_areas(atlas: Image.Image, frames: int, alpha_threshold: int) -> list[int]:
    frame_width = atlas.width // frames
    return [
        int(
            np.count_nonzero(
                np.asarray(
                    atlas.crop(
                        (
                            index * frame_width,
                            0,
                            (index + 1) * frame_width,
                            atlas.height,
                        )
                    ).getchannel("A")
                )
                > alpha_threshold
            )
        )
        for index in range(frames)
    ]


def area_ratio(areas: list[int]) -> float:
    if not areas or min(areas) <= 0:
        raise AssertionError("transparent Deviator direction")
    return max(areas) / min(areas)


def block_similarity(hd4: Image.Image) -> float:
    logical = hd4.convert("RGBA").resize(
        (hd4.width // 4, hd4.height // 4), Image.Resampling.NEAREST
    )
    nearest = logical.resize(hd4.size, Image.Resampling.NEAREST)
    difference = np.asarray(
        ImageChops.difference(nearest, hd4.convert("RGBA")), dtype=np.float32
    )
    return 1.0 - float(difference.mean() / 255.0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=GAME / "data")
    args = parser.parse_args()
    classic_entries = read_pack(args.data_dir / "sdl_data.dat")
    hd_entries = read_pack(args.data_dir / "sdl_data_hd4.dat")
    classic_deviator = decode_image(classic_entries[DEVIATOR_ID].payload)
    hd_deviator = decode_image(hd_entries[DEVIATOR_ID].payload)
    if classic_deviator is None or hd_deviator is None:
        raise AssertionError("cannot decode Deviator")
    scales = direction_scales(
        classic_deviator.convert("RGBA"), hd_deviator.convert("RGBA")
    )
    spread = max(scales) - min(scales)
    classic_areas = direction_areas(classic_deviator.convert("RGBA"), 8, 0)
    hd_areas = direction_areas(hd_deviator.convert("RGBA"), 8, 12)
    classic_area_ratio = area_ratio(classic_areas)
    hd_area_ratio = area_ratio(hd_areas)
    failures: list[str] = []
    if hd_area_ratio > classic_area_ratio + MAX_AREA_RATIO_OVER_CLASSIC:
        failures.append(
            f"Deviator apparent area ratio {hd_area_ratio:.3f} exceeds "
            f"classic allowance {classic_area_ratio + MAX_AREA_RATIO_OVER_CLASSIC:.3f}"
        )

    names = {entry.name: entry for entry in hd_entries}
    forbidden_markers = sorted(
        name for name in FORBIDDEN_HOUSE_BEACONS if name in names
    )
    if forbidden_markers:
        failures.append(
            "forbidden siren markers are installed: "
            + ", ".join(forbidden_markers)
        )

    generic_flags: list[dict[str, object]] = []
    for resource_id, name, mask_name in GENERIC_FLAGS:
        entry = hd_entries[resource_id]
        mask_entry = names.get(mask_name)
        image = decode_image(entry.payload)
        if entry.name != name or image is None:
            failures.append(f"invalid generic HD flag {name}")
            continue
        similarity = block_similarity(image)
        if similarity > MAX_NEAREST_SIMILARITY:
            failures.append(
                f"{name} is a nearest-neighbour logical upscale "
                f"({similarity:.4f})"
            )
        if mask_entry is None:
            failures.append(f"missing house mask {mask_name}")
        else:
            mask = decode_image(mask_entry.payload)
            if mask is None or mask.size != image.size:
                failures.append(f"invalid house mask {mask_name}")
        generic_flags.append(
            {
                "id": entry.index,
                "name": name,
                "hd4_size": list(image.size),
                "block_similarity": round(similarity, 5),
                "mask": mask_name if mask_entry is not None else None,
            }
        )

    flag_pairs: list[dict[str, object]] = []
    for name in SPECIAL_FLAGS:
        base = names.get(name)
        mask = names.get("HM_" + name)
        if base is None:
            failures.append(f"missing special HD flag {name}")
            continue
        if mask is None:
            failures.append(f"missing house mask HM_{name}")
            continue
        base_image = decode_image(base.payload)
        mask_image = decode_image(mask.payload)
        if (
            base_image is None
            or mask_image is None
            or base_image.size != mask_image.size
        ):
            failures.append(f"invalid special HD flag pair {name}")
            continue
        flag_pairs.append(
            {
                "name": name,
                "base_id": base.index,
                "mask_id": mask.index,
                "size": list(base_image.size),
            }
        )

    drawer_source = (
        ROOT / "src" / "drawers" / "cStructureDrawer.cpp"
    ).read_text(encoding="utf-8")
    if "skipHdHeavyFactoryOutline" not in drawer_source:
        failures.append("HD Heavy Factory outline suppression is missing")

    report = {
        "deviator_direction_scales": [round(value, 4) for value in scales],
        "deviator_spread": round(spread, 4),
        "deviator_classic_areas": classic_areas,
        "deviator_hd4_areas": hd_areas,
        "deviator_classic_area_ratio": round(classic_area_ratio, 4),
        "deviator_hd4_area_ratio": round(hd_area_ratio, 4),
        "forbidden_house_markers": forbidden_markers,
        "generic_flags": generic_flags,
        "special_flag_pairs": flag_pairs,
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
