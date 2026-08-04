#!/usr/bin/env python3
"""Check the HD harvester mask and harvesting-frame visual contracts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

from hd_assets import decode_image, read_pack


FRAME = (320, 208)
ATLAS = (2560, 832)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


def resource(entries, name: str):
    for entry in entries:
        if entry.name == name:
            image = decode_image(entry.payload)
            if image is None:
                raise AssertionError(f"{name} is not a decodable image")
            return image.convert("RGBA")
    raise AssertionError(f"missing resource: {name}")


def crop_frame(atlas, column: int, row: int):
    x = column * FRAME[0]
    y = row * FRAME[1]
    return atlas.crop((x, y, x + FRAME[0], y + FRAME[1]))


def verify_pack(path: Path) -> list[str]:
    entries = read_pack(path)
    harvester = resource(entries, "UNIT_HARVESTER")
    mask = resource(entries, "HM_UNIT_HARVESTER")
    errors: list[str] = []

    if harvester.size != ATLAS or mask.size != ATLAS:
        return [f"{path.name}: atlas dimensions differ from {ATLAS}"]

    base_rgba = np.asarray(harvester, dtype=np.uint8)
    mask_rgba = np.asarray(mask, dtype=np.uint8)
    mask_alpha = mask_rgba[:, :, 3]
    visible_mask = (mask_alpha > 8) & (base_rgba[:, :, 3] > 8)
    if not np.any(visible_mask):
        errors.append(f"{path.name}: House mask is empty")
    else:
        peak = int(mask_alpha[visible_mask].max())
        if peak < 250:
            errors.append(
                f"{path.name}: House mask peak alpha is {peak}; expected >= 250"
            )

        strength = mask_alpha.astype(np.float32) / 255.0
        luminance = (
            0.299 * base_rgba[:, :, 0]
            + 0.587 * base_rgba[:, :, 1]
            + 0.114 * base_rgba[:, :, 2]
        ) / 128.0
        red = base_rgba[:, :, :3].astype(np.float32).copy()
        targets = (255, 0, 0)
        for channel, target in enumerate(targets):
            colored = np.minimum(255.0, target * luminance)
            red[:, :, channel] = (
                red[:, :, channel] * (1.0 - strength)
                + colored * strength
            )
        active = visible_mask & (mask_alpha > 20)
        ratio = float(
            np.median(red[:, :, 1][active] / np.maximum(red[:, :, 0][active], 1))
        )
        if ratio > 0.28:
            errors.append(
                f"{path.name}: simulated Harkonnen green/red ratio is "
                f"{ratio:.3f}; expected <= 0.280"
            )

    for column, direction in enumerate(DIRECTIONS):
        base = np.asarray(crop_frame(harvester, column, 0))[:, :, 3] > 32
        distance = ndimage.distance_transform_edt(~base)
        expanded = ndimage.binary_dilation(base, iterations=2)
        for row in range(1, 4):
            current = (
                np.asarray(crop_frame(harvester, column, row))[:, :, 3] > 32
            )
            extra = current & ~expanded
            labels, count = ndimage.label(extra)
            for component in range(1, count + 1):
                region = labels == component
                area = int(np.count_nonzero(region))
                if area < 500:
                    continue
                gap = float(distance[region].min())
                if gap > 12.0:
                    errors.append(
                        f"{path.name}: detached harvesting effect at "
                        f"{direction}, phase {row}: area={area}, gap={gap:.1f}px"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True, type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    for density in (2, 4):
        path = args.data_dir / f"sdl_data_hd{density}.dat"
        if density == 2:
            # Analyze the HD4 master; HD2 identity is checked by the pack builder.
            continue
        errors.extend(verify_pack(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Harvester visual contract is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
