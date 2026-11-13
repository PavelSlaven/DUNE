#!/usr/bin/env python3
"""Compare installed HD unit silhouettes with their classic logical sizes."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from hd_assets import decode_image, read_pack
from check_all_infantry_original_scale import (
    GROUP_SINGLE,
    individual_heights,
    visible_areas,
)


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
CLASSIC_PACK = GAME / "data" / "sdl_data.dat"
HD4_PACK = GAME / "data" / "sdl_data_hd4.dat"
WORLD_SCALE_HEADER = ROOT / "src" / "utils" / "WorldObjectScale.hpp"
OUTPUT = ROOT / "artifacts" / "unit_size_audit" / "report.json"
TOLERANCE = 0.12


@dataclass(frozen=True)
class UnitSpec:
    resource_id: int
    frame_width: int
    frame_height: int
    columns: int
    rows: int
    metric: str = "major"
    excluded: bool = False


UNITS = (
    UnitSpec(130, 48, 48, 8, 2, excluded=True),  # Carryall/transport
    UnitSpec(132, 38, 48, 8, 1),
    UnitSpec(134, 32, 32, 8, 1),
    UnitSpec(135, 64, 64, 8, 1),
    UnitSpec(137, 80, 52, 8, 4, excluded=True),  # Harvester
    UnitSpec(139, 32, 32, 8, 1),
    UnitSpec(141, 48, 50, 8, 1),
    UnitSpec(143, 48, 48, 8, 4),
    UnitSpec(145, 32, 32, 8, 1),
    UnitSpec(147, 28, 26, 8, 1),
    UnitSpec(149, 32, 32, 8, 4, metric="height"),
    UnitSpec(150, 48, 48, 1, 5),
    UnitSpec(151, 36, 38, 8, 1),
    UnitSpec(153, 36, 38, 8, 1),
    UnitSpec(154, 32, 32, 8, 4, metric="height"),
    UnitSpec(155, 32, 32, 8, 4, metric="height"),
    UnitSpec(156, 32, 32, 8, 4, metric="member_height"),
    UnitSpec(157, 32, 32, 8, 1),
    UnitSpec(159, 32, 32, 8, 1),
    UnitSpec(161, 32, 32, 8, 1),
    UnitSpec(162, 28, 26, 8, 1),
    UnitSpec(164, 32, 32, 8, 4, metric="member_height"),
    UnitSpec(165, 32, 32, 8, 4, metric="height"),
    UnitSpec(166, 32, 32, 8, 4, metric="member_height"),
)


def tank_runtime_multiplier() -> float:
    source = WORLD_SCALE_HEADER.read_text(encoding="utf-8")
    match = re.search(r"hd(?:Combat)?TankMultiplier\s*=\s*([0-9.]+)F", source)
    if match is None:
        return 1.0
    return float(match.group(1))


def frame_measurements(image, spec: UnitSpec, density: int) -> np.ndarray:
    expected = (
        spec.frame_width * spec.columns * density,
        spec.frame_height * spec.rows * density,
    )
    if image.size != expected:
        raise AssertionError(
            f"{spec.resource_id}: atlas {image.size}, expected {expected}"
        )
    measurements: list[tuple[float, float, float]] = []
    for row in range(spec.rows):
        for column in range(spec.columns):
            left = column * spec.frame_width * density
            top = row * spec.frame_height * density
            frame = image.crop(
                (
                    left,
                    top,
                    left + spec.frame_width * density,
                    top + spec.frame_height * density,
                )
            )
            bounds = frame.getchannel("A").getbbox()
            if bounds is None:
                continue
            width = (bounds[2] - bounds[0]) / density
            height = (bounds[3] - bounds[1]) / density
            measurements.append((width, height, width * height))
    if not measurements:
        raise AssertionError(f"{spec.resource_id}: all frames are transparent")
    return np.asarray(measurements, dtype=np.float64)


def median_scale(classic: np.ndarray, hd: np.ndarray, metric: str) -> float:
    count = min(len(classic), len(hd))
    classic = classic[:count]
    hd = hd[:count]
    if metric in ("height", "member_height"):
        ratios = hd[:, 1] / classic[:, 1]
    elif metric == "major":
        ratios = np.maximum(hd[:, 0], hd[:, 1]) / np.maximum(
            classic[:, 0], classic[:, 1]
        )
    else:
        ratios = np.sqrt(hd[:, 2] / classic[:, 2])
    return float(np.median(ratios))


def infantry_member_scale(
    classic_entries,
    hd_entries,
    classic,
    hd,
    spec: UnitSpec,
) -> float:
    classic_heights = individual_heights(classic, 1, True)
    hd_heights = individual_heights(hd, 4, True)
    classic_median = float(np.median(classic_heights))
    if hd_heights:
        return float(np.median(hd_heights)) / classic_median

    # Some group frames intentionally overlap all three people. Reuse the
    # corresponding single unit and derive the per-person size from area.
    single_id = GROUP_SINGLE[spec.resource_id]
    single_hd = decode_image(hd_entries[single_id].payload)
    if single_hd is None:
        raise AssertionError(f"{single_id}: resource cannot be decoded")
    single_height = float(
        np.median(individual_heights(single_hd.convert("RGBA"), 4, False))
    )
    area_ratio = float(
        np.median(
            visible_areas(hd)
            / (3.0 * visible_areas(single_hd.convert("RGBA")))
        )
    )
    return float(single_height * np.sqrt(area_ratio) / classic_median)


def main() -> int:
    classic_entries = read_pack(CLASSIC_PACK)
    hd_entries = read_pack(HD4_PACK)
    tank_multiplier = tank_runtime_multiplier()
    failures: list[str] = []
    results: list[dict[str, object]] = []
    for spec in UNITS:
        classic = decode_image(classic_entries[spec.resource_id].payload)
        hd = decode_image(hd_entries[spec.resource_id].payload)
        if classic is None or hd is None:
            raise AssertionError(f"{spec.resource_id}: resource cannot be decoded")
        classic_size = frame_measurements(classic.convert("RGBA"), spec, 1)
        hd_size = frame_measurements(hd.convert("RGBA"), spec, 4)
        if spec.metric == "member_height":
            atlas_scale = infantry_member_scale(
                classic_entries,
                hd_entries,
                classic.convert("RGBA"),
                hd.convert("RGBA"),
                spec,
            )
        else:
            atlas_scale = median_scale(classic_size, hd_size, spec.metric)
        runtime_scale = (
            tank_multiplier
            if spec.resource_id in (151, 153, 159, 161)
            else 1.0
        )
        effective_scale = atlas_scale * runtime_scale
        passed = spec.excluded or abs(effective_scale - 1.0) <= TOLERANCE
        name = classic_entries[spec.resource_id].name
        if not passed:
            failures.append(
                f"{spec.resource_id}:{name} effective scale {effective_scale:.3f}"
            )
        results.append(
            {
                "id": spec.resource_id,
                "name": name,
                "metric": spec.metric,
                "excluded": spec.excluded,
                "atlas_scale": round(atlas_scale, 4),
                "runtime_scale": round(runtime_scale, 4),
                "effective_scale": round(effective_scale, 4),
                "passed": passed,
            }
        )
    report = {
        "tolerance": TOLERANCE,
        "excluded_ids": [130, 137],
        "failures": failures,
        "units": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
