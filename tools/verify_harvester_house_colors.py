#!/usr/bin/env python3
"""Verify that installed HD harvesters resolve to the requested House color."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

from hd_assets import decode_image, read_pack


HOUSE_VARIANTS = {
    "atreides": ("A", (0, 90, 255)),
    "harkonnen": ("H", (255, 0, 0)),
    "ordos": ("O", (0, 255, 0)),
}


def resolve(entries, house_code: str, resource_name: str):
    by_name = {entry.name: entry for entry in entries}
    base_name = resource_name
    selected_name = f"HV_{house_code}_{base_name}"
    selected = by_name.get(selected_name, by_name[base_name])
    mask = by_name.get(f"HM_{selected.name}")
    if mask is None:
        mask = by_name.get(f"HOUSEMASK_{selected.name}")
    if mask is None and selected.name != base_name:
        mask = by_name.get(f"HM_{base_name}")
    if mask is None and selected.name != base_name:
        mask = by_name.get(f"HOUSEMASK_{base_name}")
    return selected, mask


def tint(image, mask, color: tuple[int, int, int]):
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32).copy()
    if mask is None:
        return rgba.astype(np.uint8), np.zeros(rgba.shape[:2], dtype=bool)
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    strength = (
        mask_rgba[:, :, 3] / 255.0
        * np.max(mask_rgba[:, :, :3], axis=2) / 255.0
    )
    visible = rgba[:, :, 3] > 0
    active = (strength > 0.08) & visible
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        colored = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - strength)
            + colored * strength
        )
    return np.clip(rgba, 0, 255).astype(np.uint8), active


def verify_pack(path: Path, resource_name: str) -> list[str]:
    entries = read_pack(path)
    errors: list[str] = []
    for house, (code, color) in HOUSE_VARIANTS.items():
        selected_entry, mask_entry = resolve(entries, code, resource_name)
        selected = decode_image(selected_entry.payload)
        mask = decode_image(mask_entry.payload) if mask_entry else None
        if selected is None:
            errors.append(f"{path.name}: {house}: selected image is invalid")
            continue
        if mask is not None and mask.size != selected.size:
            errors.append(f"{path.name}: {house}: mask dimensions differ")
            continue
        output, active = tint(selected, mask, color)
        visible = output[:, :, 3] > 16
        if not np.any(visible):
            errors.append(f"{path.name}: {house}: sprite is transparent")
            continue

        red_dominance = float(
            np.mean(
                output[:, :, 0][visible].astype(np.float32)
                - output[:, :, 1][visible].astype(np.float32)
            )
        )
        green_pixels = int(
            np.count_nonzero(
                visible
                & (output[:, :, 1] > output[:, :, 0] + 24)
                & (output[:, :, 1] > output[:, :, 2] + 12)
            )
        )
        print(
            f"{path.name}: {house}: selected={selected_entry.name}, "
            f"mask={mask_entry.name if mask_entry else 'NONE'}, "
            f"mask_pixels={int(np.count_nonzero(active))}, "
            f"green_pixels={green_pixels}, "
            f"red_minus_green={red_dominance:.2f}"
        )
        if house == "ordos" and (
            mask_entry is None
            or not np.any(active)
            or green_pixels == 0
            or red_dominance > 8.0
        ):
            errors.append(
                f"{path.name}: Ordos {resource_name} remains red "
                "after resolution"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument(
        "--resource",
        default="UNIT_HARVESTER",
        choices=("UNIT_HARVESTER", "UNIT_SOLDIER", "UNIT_SOLDIERS"),
    )
    args = parser.parse_args()
    errors: list[str] = []
    for density in (2, 4):
        errors.extend(
            verify_pack(
                args.data_dir / f"sdl_data_hd{density}.dat",
                args.resource,
            )
        )
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"{args.resource} House-color resolution is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
