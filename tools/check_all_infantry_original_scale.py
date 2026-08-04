#!/usr/bin/env python3
"""Check that every HD infantry atlas preserves its classic apparent scale."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
INFANTRY = {
    149: "UNIT_SABOTEUR",
    154: "UNIT_SINGLEFREMEN",
    155: "UNIT_SOLDIER",
    156: "UNIT_SOLDIERS",
    164: "UNIT_TRIPLEFREMEN",
    165: "UNIT_TROOPER",
    166: "UNIT_TROOPERS",
}
ROWS = 4
COLUMNS = 8
GROUPS = {156, 164, 166}
GROUP_SINGLE = {156: 155, 164: 154, 166: 165}


def individual_heights(
    atlas: Image.Image,
    density: int,
    grouped: bool,
    threshold: int = 32,
) -> list[float]:
    frame_width = atlas.width // COLUMNS
    frame_height = atlas.height // ROWS
    heights: list[float] = []
    for row in range(ROWS):
        for column in range(COLUMNS):
            alpha = np.asarray(
                atlas.crop(
                    (
                        column * frame_width,
                        row * frame_height,
                        (column + 1) * frame_width,
                        (row + 1) * frame_height,
                    )
                ).getchannel("A"),
                dtype=np.uint8,
            )
            visible = (alpha > threshold).astype(np.uint8)
            count, _, stats, _ = cv2.connectedComponentsWithStats(visible, 8)
            components = [
                (int(height), int(area))
                for _, _, _, height, area in stats[1:count]
                if area >= 2 * density * density
            ]
            if not components:
                raise AssertionError(f"empty infantry frame {column},{row}")
            if grouped:
                # Overlapping squad members sometimes form one tall component.
                # Ignore those merged silhouettes and measure the separated
                # people present in the other directions/phases.
                heights.extend(
                    height / density
                    for height, _ in components
                    if height / density <= 20.0
                )
            else:
                heights.append(max(components)[0] / density)
    if not heights and not grouped:
        raise AssertionError("no individual infantry silhouettes found")
    return heights


def visible_areas(atlas: Image.Image, threshold: int = 32) -> np.ndarray:
    frame_width = atlas.width // COLUMNS
    frame_height = atlas.height // ROWS
    alpha = np.asarray(atlas.getchannel("A"), dtype=np.uint8)
    return np.asarray(
        [
            int(
                (
                    alpha[
                        row * frame_height : (row + 1) * frame_height,
                        column * frame_width : (column + 1) * frame_width,
                    ]
                    > threshold
                ).sum()
            )
            for row in range(ROWS)
            for column in range(COLUMNS)
        ],
        dtype=np.float64,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=0.6)
    args = parser.parse_args()

    entries = read_pack(args.pack)
    report: list[dict[str, object]] = []
    failures: list[str] = []
    for resource_id, name in INFANTRY.items():
        classic_path = CLASSIC / f"{resource_id:04d}_{name}.png"
        classic = Image.open(classic_path).convert("RGBA")
        hd = decode_image(entries[resource_id].payload)
        if hd is None:
            failures.append(f"{name}: cannot decode installed resource")
            continue
        density_x = hd.width / classic.width
        density_y = hd.height / classic.height
        if density_x != density_y or density_x not in (2, 4):
            failures.append(
                f"{name}: invalid atlas density {density_x:g}x{density_y:g}"
            )
            continue
        grouped = resource_id in GROUPS
        classic_heights = np.asarray(
            individual_heights(classic, 1, grouped), dtype=np.float64
        )
        hd_heights = np.asarray(
            individual_heights(hd, int(density_x), grouped), dtype=np.float64
        )
        classic_median = float(np.median(classic_heights))
        if len(hd_heights):
            hd_median = float(np.median(hd_heights))
        else:
            single_id = GROUP_SINGLE[resource_id]
            single_name = INFANTRY[single_id]
            single_hd = decode_image(entries[single_id].payload)
            if single_hd is None:
                raise AssertionError(f"cannot decode {single_name}")
            single_heights = individual_heights(
                single_hd, int(density_x), False
            )
            per_member_area_ratio = float(
                np.median(
                    visible_areas(hd)
                    / (3.0 * visible_areas(single_hd))
                )
            )
            hd_median = float(np.median(single_heights)) * np.sqrt(
                per_member_area_ratio
            )
        delta = hd_median - classic_median
        report.append(
            {
                "id": resource_id,
                "name": name,
                "classic_median": classic_median,
                "hd_median": hd_median,
                "delta": delta,
                "scale_ratio": hd_median / classic_median,
            }
        )
        if abs(delta) > args.tolerance:
            failures.append(
                f"{name}: HD median {hd_median:.2f}px differs from "
                f"classic {classic_median:.2f}px by {delta:+.2f}px"
            )

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        print("\n".join(failures))
        return 1
    print("all infantry preserve their classic apparent scale")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
