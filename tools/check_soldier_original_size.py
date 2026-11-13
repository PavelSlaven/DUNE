#!/usr/bin/env python3
"""Regression check: HD soldier must preserve the classic apparent size."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from hd_assets import decode_image, read_pack


def frame_metrics(atlas: Image.Image, frame_width: int, frame_height: int) -> list[dict[str, float]]:
    metrics = []
    for row in range(4):
        for column in range(8):
            cell = atlas.crop(
                (
                    column * frame_width,
                    row * frame_height,
                    (column + 1) * frame_width,
                    (row + 1) * frame_height,
                )
            )
            alpha = np.asarray(cell.getchannel("A"), dtype=np.uint8)
            ys, xs = np.nonzero(alpha > 8)
            if not len(xs):
                raise AssertionError(f"empty frame {column},{row}")
            metrics.append(
                {
                    "width": float(xs.max() - xs.min() + 1),
                    "height": float(ys.max() - ys.min() + 1),
                    "area": float(np.count_nonzero(alpha > 8)),
                }
            )
    return metrics


def summary(metrics: list[dict[str, float]], density: int) -> dict[str, float]:
    return {
        key: float(np.median([frame[key] / (density * density if key == "area" else density) for frame in metrics]))
        for key in ("width", "height", "area")
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--classic", required=True, type=Path)
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--height-ratio", type=float, default=0.95)
    parser.add_argument("--area-ratio", type=float, default=0.80)
    args = parser.parse_args()

    classic = Image.open(args.classic).convert("RGBA")
    entries = read_pack(args.pack)
    current = decode_image(entries[155].payload)
    if current is None:
        raise AssertionError("UNIT_SOLDIER is not decodable")
    current = current.convert("RGBA")
    density = current.width // classic.width
    if density not in (2, 4):
        raise AssertionError(f"unexpected density {density}")

    old = summary(frame_metrics(classic, 32, 32), 1)
    new = summary(frame_metrics(current, 32 * density, 32 * density), density)
    ratios = {key: new[key] / old[key] for key in old}
    failures = []
    if ratios["height"] < args.height_ratio:
        failures.append(f"height ratio {ratios['height']:.3f} is below {args.height_ratio:.3f}")
    if ratios["area"] < args.area_ratio:
        failures.append(f"area ratio {ratios['area']:.3f} is below {args.area_ratio:.3f}")
    report = {"classic": old, "current": new, "ratios": ratios, "failures": failures}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        print("UNIT_SOLDIER is smaller than the original", file=sys.stderr)
        return 1
    print("UNIT_SOLDIER preserves the original apparent size")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
