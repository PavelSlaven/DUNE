#!/usr/bin/env python3
"""Regression check: single soldier must match the squad's faction tone."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from hd_assets import decode_image, read_pack
from prepare_soldiers_review import apply_engine_tint


RESOURCES = {
    "soldier": (155, "HM_UNIT_SOLDIER"),
    "squad": (156, "HM_UNIT_SOLDIERS"),
}
HOUSES = {
    "harkonnen": (255, 0, 0),
    "atreides": (0, 90, 255),
    "ordos": (0, 255, 0),
}


def weighted_luminance(image, mask) -> float:
    rgb = np.asarray(image.convert("RGBA"), dtype=np.float32)[:, :, :3]
    weight = np.asarray(mask.getchannel("A"), dtype=np.float32) / 255.0
    weight[weight < 0.20] = 0.0
    if float(weight.sum()) < 1.0:
        raise AssertionError("empty faction mask")
    luminance = 0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]
    return float((luminance * weight).sum() / weight.sum())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--tolerance", type=float, default=8.0)
    args = parser.parse_args()
    entries = read_pack(args.pack)
    by_name = {entry.name: entry for entry in entries}
    results: dict[str, object] = {}
    failures: list[str] = []

    decoded = {}
    for key, (resource_id, mask_name) in RESOURCES.items():
        image = decode_image(entries[resource_id].payload)
        mask_entry = by_name.get(mask_name)
        mask = decode_image(mask_entry.payload) if mask_entry else None
        if image is None or mask is None:
            raise AssertionError(f"cannot decode {key} or {mask_name}")
        decoded[key] = (image.convert("RGBA"), mask.convert("RGBA"))

    for house, color in HOUSES.items():
        tones = {}
        for key, (image, mask) in decoded.items():
            tinted = apply_engine_tint(image, mask, color)
            tones[key] = weighted_luminance(tinted, mask)
        difference = tones["soldier"] - tones["squad"]
        results[house] = {**tones, "difference": difference}
        if abs(difference) > args.tolerance:
            failures.append(
                f"{house}: UNIT_SOLDIER differs from UNIT_SOLDIERS by {difference:+.2f} luminance"
            )

    report = {"pack": str(args.pack), "tolerance": args.tolerance, "houses": results, "failures": failures}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        print("soldier/squad faction tones do not match", file=sys.stderr)
        return 1
    print("soldier/squad faction tones match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
