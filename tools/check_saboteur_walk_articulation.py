#!/usr/bin/env python3
"""Reject fake walk cycles where only the lower sprite fragment moves."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROWS = 4


def frame_rgba(
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
    ).resize((32, 32), Image.Resampling.LANCZOS)
    return np.asarray(frame, dtype=np.float32) / 255.0


def direction_metrics(
    atlas: Image.Image,
    column: int,
) -> dict[str, object]:
    frames = [frame_rgba(atlas, column, row) for row in range(ROWS)]
    union_alpha = np.maximum.reduce([frame[:, :, 3] for frame in frames])
    ys, _ = np.where(union_alpha > 0.05)
    if len(ys) == 0:
        raise AssertionError("empty saboteur direction")
    top = int(ys.min())
    bottom = int(ys.max()) + 1
    split = top + round((bottom - top) * 0.62)
    upper_mask = np.zeros((32, 32), dtype=np.float32)
    lower_mask = np.zeros((32, 32), dtype=np.float32)
    upper_mask[top:split] = 1.0
    lower_mask[split:bottom] = 1.0

    upper_changes: list[float] = []
    lower_changes: list[float] = []
    for row in range(ROWS):
        current = frames[row]
        following = frames[(row + 1) % ROWS]
        difference = np.mean(np.abs(current - following), axis=2)
        upper_changes.append(
            float((difference * upper_mask).sum() / upper_mask.sum())
        )
        lower_changes.append(
            float((difference * lower_mask).sum() / lower_mask.sum())
        )

    upper_mean = float(np.mean(upper_changes))
    lower_mean = float(np.mean(lower_changes))
    return {
        "upper_changes": upper_changes,
        "lower_changes": lower_changes,
        "upper_mean": upper_mean,
        "lower_mean": lower_mean,
        "lower_to_upper_ratio": lower_mean / max(upper_mean, 1e-6),
    }


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
    parser.add_argument("--min-upper-change", type=float, default=0.0007)
    parser.add_argument("--min-lower-change", type=float, default=0.0015)
    parser.add_argument("--max-lower-upper-ratio", type=float, default=7.0)
    args = parser.parse_args()

    atlas = Image.open(args.atlas).convert("RGBA")
    directions: dict[str, object] = {}
    failures: list[str] = []
    for column, direction in enumerate(DIRECTIONS):
        values = direction_metrics(atlas, column)
        directions[direction] = values
        upper_mean = float(values["upper_mean"])
        lower_mean = float(values["lower_mean"])
        ratio = float(values["lower_to_upper_ratio"])
        if upper_mean < args.min_upper_change:
            failures.append(
                f"{direction}: rigid upper body {upper_mean:.6f}"
            )
        if lower_mean < args.min_lower_change:
            failures.append(
                f"{direction}: no leg articulation {lower_mean:.6f}"
            )
        if ratio > args.max_lower_upper_ratio:
            failures.append(
                f"{direction}: legs float independently, ratio {ratio:.2f}"
            )

    report = {
        "atlas": str(args.atlas),
        "directions": directions,
        "limits": {
            "min_upper_change": args.min_upper_change,
            "min_lower_change": args.min_lower_change,
            "max_lower_upper_ratio": args.max_lower_upper_ratio,
        },
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        print(f"walk articulation failed: {len(failures)} checks")
        return 1
    print("saboteur walk articulation is plausible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
