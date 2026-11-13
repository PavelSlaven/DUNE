#!/usr/bin/env python3
"""Reject UNIT_SABOTEUR walk cycles whose apparent scale changes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROWS = 4


def frame_alpha(
    atlas: Image.Image,
    column: int,
    row: int,
) -> np.ndarray:
    width = atlas.width // len(DIRECTIONS)
    height = atlas.height // ROWS
    frame = atlas.crop(
        (
            column * width,
            row * height,
            (column + 1) * width,
            (row + 1) * height,
        )
    )
    return np.asarray(frame.getchannel("A"), dtype=np.float32) / 255.0


def metrics(atlas: Image.Image) -> dict[str, object]:
    report: dict[str, object] = {}
    for column, direction in enumerate(DIRECTIONS):
        areas: list[float] = []
        heights: list[int] = []
        upper_areas: list[float] = []
        head_widths: list[int] = []
        for row in range(ROWS):
            alpha = frame_alpha(atlas, column, row)
            active = alpha > 0.05
            ys, _ = np.where(active)
            if len(ys) == 0:
                raise AssertionError(f"empty frame {direction}:{row}")
            top = int(ys.min())
            bottom = int(ys.max()) + 1
            split = top + round((bottom - top) * 0.62)
            head_bottom = top + round((bottom - top) * 0.25)
            head_ys, head_xs = np.where(active[top:head_bottom])
            if len(head_xs) == 0:
                raise AssertionError(f"empty head region {direction}:{row}")
            areas.append(float(alpha.sum()))
            heights.append(bottom - top)
            upper_areas.append(float(alpha[top:split].sum()))
            head_widths.append(int(head_xs.max() - head_xs.min() + 1))
        report[direction] = {
            "area_ratio": max(areas) / min(areas),
            "upper_body_area_ratio": max(upper_areas) / min(upper_areas),
            "head_width_ratio": max(head_widths) / min(head_widths),
            "height_span": max(heights) - min(heights),
            "areas": areas,
            "upper_body_areas": upper_areas,
            "head_widths": head_widths,
            "heights": heights,
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--atlas",
        type=Path,
        default=Path(
            "artifacts/saboteur_review_v1/"
            "UNIT_SABOTEUR_HD4_PREVIEW.png"
        ),
    )
    parser.add_argument("--max-area-ratio", type=float, default=1.30)
    parser.add_argument(
        "--max-upper-body-ratio",
        type=float,
        default=1.12,
    )
    parser.add_argument("--max-head-width-ratio", type=float, default=1.40)
    parser.add_argument("--max-height-span", type=int, default=5)
    args = parser.parse_args()

    atlas = Image.open(args.atlas).convert("RGBA")
    report = metrics(atlas)
    failures: list[str] = []
    for direction, values in report.items():
        area_ratio = float(values["area_ratio"])
        upper_ratio = float(values["upper_body_area_ratio"])
        head_ratio = float(values["head_width_ratio"])
        height_span = int(values["height_span"])
        if area_ratio > args.max_area_ratio:
            failures.append(
                f"{direction}: silhouette area ratio {area_ratio:.4f}"
            )
        if upper_ratio > args.max_upper_body_ratio:
            failures.append(
                f"{direction}: upper-body area ratio {upper_ratio:.4f}"
            )
        if head_ratio > args.max_head_width_ratio:
            failures.append(
                f"{direction}: head width ratio {head_ratio:.4f}"
            )
        if height_span > args.max_height_span:
            failures.append(
                f"{direction}: height span {height_span} HD4 pixels"
            )

    output = {
        "atlas": str(args.atlas),
        "directions": report,
        "limits": {
            "area_ratio": args.max_area_ratio,
            "upper_body_area_ratio": args.max_upper_body_ratio,
            "head_width_ratio": args.max_head_width_ratio,
            "height_span": args.max_height_span,
        },
        "failures": failures,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if failures:
        print(f"scale stability failed: {len(failures)} checks")
        return 1
    print("saboteur apparent scale is stable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
