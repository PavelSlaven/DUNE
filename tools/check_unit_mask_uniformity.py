#!/usr/bin/env python3
"""Verify that faction unit masks have a solid core and only edge antialiasing."""

from __future__ import annotations

import argparse
from pathlib import Path

from hd_assets import decode_image, read_pack


def core_pixels(image):
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    for y in range(1, rgba.height - 1):
        for x in range(1, rgba.width - 1):
            if pixels[x, y][3] == 0:
                continue
            if all(
                pixels[x + dx, y + dy][3] > 0
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
            ):
                yield pixels[x, y]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pack",
        nargs="?",
        type=Path,
        default=Path("resources/bin/data/sdl_data_hd4.dat"),
    )
    args = parser.parse_args()

    failures: list[str] = []
    checked = 0
    for entry in read_pack(args.pack):
        if not entry.name.startswith("HM_"):
            continue
        image = decode_image(entry.payload)
        if image is None:
            failures.append(f"{entry.name}: image cannot be decoded")
            continue
        core = list(core_pixels(image))
        if not core:
            failures.append(f"{entry.name}: no faction-mask core pixels")
            continue
        checked += 1
        inconsistent = sum(
            1 for red, green, blue, alpha in core
            if (red, green, blue) != (255, 255, 255) or alpha != 255
        )
        if inconsistent:
            failures.append(
                f"{entry.name}: {inconsistent}/{len(core)} core pixels change faction tone"
            )

    if failures:
        print("FAIL: faction masks contain internal opacity or color gradients")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS: {checked} faction masks use one solid tone with edge antialiasing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
