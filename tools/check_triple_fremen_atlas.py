#!/usr/bin/env python3
"""Validate an 8x4 infantry-squad atlas, animation and House mask."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from hd_assets import decode_image, read_pack


UNIT_ID = 164
UNIT_NAME = "UNIT_TRIPLEFREMEN"
MASK_NAME = "HM_UNIT_TRIPLEFREMEN"
COLUMNS = 8
ROWS = 4
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


def logical_alpha(atlas: Image.Image, column: int, row: int) -> np.ndarray:
    width = atlas.width // COLUMNS
    height = atlas.height // ROWS
    frame = atlas.crop(
        (column * width, row * height, (column + 1) * width, (row + 1) * height)
    )
    return np.asarray(
        frame.getchannel("A").resize((32, 32), Image.Resampling.LANCZOS),
        dtype=np.float32,
    ) / 255.0


def centroid(alpha: np.ndarray) -> tuple[float, float]:
    total = float(alpha.sum())
    y, x = np.indices(alpha.shape)
    return float((x * alpha).sum() / total), float((y * alpha).sum() / total)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, required=True)
    parser.add_argument("--classic", type=Path, required=True)
    parser.add_argument("--resource-id", type=int, default=UNIT_ID)
    parser.add_argument("--resource-name", default=UNIT_NAME)
    parser.add_argument("--mask-name", default=MASK_NAME)
    args = parser.parse_args()

    entries = read_pack(args.pack)
    if entries[args.resource_id].name != args.resource_name:
        raise AssertionError(
            f"resource {args.resource_id} is {entries[args.resource_id].name}"
        )
    unit = decode_image(entries[args.resource_id].payload)
    masks = [entry for entry in entries if entry.name == args.mask_name]
    if unit is None or len(masks) != 1:
        raise AssertionError("triple-Fremen unit or House mask is missing")
    mask = decode_image(masks[0].payload)
    if mask is None or mask.size != unit.size:
        raise AssertionError("invalid triple-Fremen House mask")

    unit_alpha = np.asarray(unit.getchannel("A"))
    mask_alpha = np.asarray(mask.getchannel("A"))
    failures: list[str] = []
    if np.any((mask_alpha > 0) & (unit_alpha == 0)):
        failures.append("House mask extends outside the unit silhouette")

    frame_width = unit.width // COLUMNS
    frame_height = unit.height // ROWS
    frames = [
        unit.crop(
            (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
        )
        for row in range(ROWS)
        for column in range(COLUMNS)
    ]
    if len({frame.tobytes() for frame in frames}) != 32:
        failures.append("not all 32 frames are unique")

    widths: list[float] = []
    heights: list[float] = []
    density = frame_width / 32.0
    for index, frame in enumerate(frames):
        alpha = np.asarray(frame.getchannel("A"))
        y, x = np.where(alpha > 2)
        if not len(x):
            failures.append(f"empty frame {index}")
            continue
        widths.append((float(x.max() - x.min() + 1)) / density)
        heights.append((float(y.max() - y.min() + 1)) / density)

    classic = Image.open(args.classic).convert("RGBA")
    classic_widths: list[int] = []
    classic_heights: list[int] = []
    for row in range(ROWS):
        for column in range(COLUMNS):
            frame = classic.crop(
                (column * 32, row * 32, (column + 1) * 32, (row + 1) * 32)
            )
            rgb = np.asarray(frame)[:, :, :3]
            y, x = np.where(rgb.max(axis=2) > 10)
            classic_widths.append(int(x.max() - x.min() + 1))
            classic_heights.append(int(y.max() - y.min() + 1))

    median_width = float(np.median(widths))
    median_height = float(np.median(heights))
    classic_width = float(np.median(classic_widths))
    classic_height = float(np.median(classic_heights))
    if abs(median_width - classic_width) > 1.5:
        failures.append(f"median width differs: {median_width:.2f} vs {classic_width:.2f}")
    if abs(median_height - classic_height) > 1.5:
        failures.append(f"median height differs: {median_height:.2f} vs {classic_height:.2f}")

    motion: dict[str, dict[str, float | list[float]]] = {}
    for column, direction in enumerate(DIRECTIONS):
        alpha_frames = [logical_alpha(unit, column, row) for row in range(ROWS)]
        centers = [centroid(alpha) for alpha in alpha_frames]
        span_x = max(center[0] for center in centers) - min(center[0] for center in centers)
        span_y = max(center[1] for center in centers) - min(center[1] for center in centers)
        transitions = [
            float(np.mean(np.abs(alpha_frames[(index + 1) % ROWS] - alpha_frames[index])))
            for index in range(ROWS)
        ]
        unevenness = max(transitions) / max(min(transitions), 0.0001)
        motion[direction] = {
            "centroid_span_x": span_x,
            "centroid_span_y": span_y,
            "transition_unevenness": unevenness,
            "transitions": transitions,
        }
        if span_x > 1.25 or span_y > 1.25:
            failures.append(f"{direction}: anchor jump {span_x:.2f}x{span_y:.2f}")
        if unevenness > 1.8:
            failures.append(f"{direction}: uneven transitions {unevenness:.2f}")

    report = {
        "pack": str(args.pack),
        "resource": {"id": args.resource_id, "name": args.resource_name},
        "mask_id": masks[0].index,
        "frames": len(frames),
        "median_logical_size": [median_width, median_height],
        "classic_median_size": [classic_width, classic_height],
        "motion": motion,
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        print(f"triple-Fremen validation failed: {len(failures)}", file=sys.stderr)
        return 1
    print(f"{args.resource_name} atlas is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
