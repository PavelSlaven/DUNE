#!/usr/bin/env python3
"""Detect visible jumps in the four-frame infantry walking loop."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from hd_assets import decode_image, read_pack


RESOURCE_IDS = {
    "soldier": 155,
    "squad": 156,
}
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
LOGICAL_FRAME = 32
ROWS = 4


def logical_alpha(
    atlas: Image.Image,
    column: int,
    row: int,
) -> np.ndarray:
    frame_width = atlas.width // len(DIRECTIONS)
    frame_height = atlas.height // ROWS
    frame = atlas.crop(
        (
            column * frame_width,
            row * frame_height,
            (column + 1) * frame_width,
            (row + 1) * frame_height,
        )
    )
    alpha = frame.getchannel("A").resize(
        (LOGICAL_FRAME, LOGICAL_FRAME),
        Image.Resampling.LANCZOS,
    )
    return np.asarray(alpha, dtype=np.float32) / 255.0


def centroid(alpha: np.ndarray) -> tuple[float, float]:
    total = float(alpha.sum())
    if total <= 0:
        raise AssertionError("infantry animation contains an empty frame")
    y_grid, x_grid = np.indices(alpha.shape)
    return (
        float((x_grid * alpha).sum() / total),
        float((y_grid * alpha).sum() / total),
    )


def direction_metrics(
    atlas: Image.Image,
    column: int,
    transition_floor: float,
) -> dict[str, object]:
    frames = [
        logical_alpha(atlas, column, row)
        for row in range(ROWS)
    ]
    centroids = [centroid(frame) for frame in frames]
    transitions = [
        float(np.mean(np.abs(frames[(index + 1) % ROWS] - frames[index])))
        for index in range(ROWS)
    ]
    nonzero = [value for value in transitions if value > 0.0005]
    unevenness = (
        max(nonzero) / max(min(nonzero), transition_floor)
        if nonzero
        else float("inf")
    )
    return {
        "centroid_span_x": max(item[0] for item in centroids)
        - min(item[0] for item in centroids),
        "centroid_span_y": max(item[1] for item in centroids)
        - min(item[1] for item in centroids),
        "transitions": transitions,
        "transition_unevenness": unevenness,
    }


def check_resource(
    atlas: Image.Image,
    resource: str,
) -> tuple[dict[str, object], list[str]]:
    metrics: dict[str, object] = {}
    failures: list[str] = []
    for column, direction in enumerate(DIRECTIONS):
        result = direction_metrics(
            atlas,
            column,
            0.0035 if resource == "soldier" else 0.0,
        )
        metrics[direction] = result
        span_x = float(result["centroid_span_x"])
        span_y = float(result["centroid_span_y"])
        unevenness = float(result["transition_unevenness"])
        max_span_x = 2.25 if resource == "soldier" else 1.25
        max_span_y = 1.50 if resource == "soldier" else 1.25
        max_unevenness = 2.60 if resource == "soldier" else 1.80
        if span_x > max_span_x or span_y > max_span_y:
            failures.append(
                f"{resource}:{direction}: anchor jump "
                f"{span_x:.2f}x{span_y:.2f} logical pixels"
            )
        if unevenness > max_unevenness:
            failures.append(
                f"{resource}:{direction}: uneven frame transitions "
                f"{unevenness:.2f}"
            )
    return metrics, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pack",
        type=Path,
        default=Path(
            "C:/Users/Slaven/Desktop/"
            "D2TM-v0.8.0.windows.ru/data/sdl_data_hd4.dat"
        ),
    )
    parser.add_argument("--soldier-image", type=Path)
    parser.add_argument("--squad-image", type=Path)
    args = parser.parse_args()

    entries = None
    if args.soldier_image is None or args.squad_image is None:
        entries = read_pack(args.pack)
    report: dict[str, object] = {
        "pack": str(args.pack),
        "resources": {},
    }
    failures: list[str] = []
    for resource, resource_id in RESOURCE_IDS.items():
        image_path = (
            args.soldier_image
            if resource == "soldier"
            else args.squad_image
        )
        image = (
            Image.open(image_path)
            if image_path is not None
            else decode_image(entries[resource_id].payload)
        )
        if image is None:
            raise AssertionError(f"resource {resource_id} is not an image")
        metrics, resource_failures = check_resource(
            image.convert("RGBA"),
            resource,
        )
        report["resources"][resource] = metrics
        failures.extend(resource_failures)

    report["failures"] = failures
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        print(
            f"infantry walk is jerky: {len(failures)} checks failed",
            file=sys.stderr,
        )
        return 1
    print("infantry walk loop is smooth")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
