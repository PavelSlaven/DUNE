#!/usr/bin/env python3
"""Normalize an alpha crest into deterministic 4x and 2x HUD assets."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter


MASTER_SIZE = 384
HD2_SIZE = 192
PADDING = 16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--master-output", required=True, type=Path)
    parser.add_argument("--hd4-output", required=True, type=Path)
    parser.add_argument("--hd2-output", required=True, type=Path)
    return parser.parse_args()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def main() -> None:
    args = parse_args()
    with Image.open(args.input) as source:
        rgba = source.convert("RGBA")

    alpha = rgba.getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError(f"No opaque pixels in {args.input}")

    crest = rgba.crop(bounds)
    target = MASTER_SIZE - PADDING * 2
    scale = min(target / crest.width, target / crest.height)
    resized = crest.resize(
        (
            max(1, round(crest.width * scale)),
            max(1, round(crest.height * scale)),
        ),
        Image.Resampling.LANCZOS,
    )
    master = Image.new("RGBA", (MASTER_SIZE, MASTER_SIZE), (0, 0, 0, 0))
    master.alpha_composite(
        resized,
        (
            (MASTER_SIZE - resized.width) // 2,
            (MASTER_SIZE - resized.height) // 2,
        ),
    )
    master = master.filter(ImageFilter.UnsharpMask(1, 105, 2))
    hd2 = master.resize((HD2_SIZE, HD2_SIZE), Image.Resampling.LANCZOS)

    save(master, args.master_output)
    save(master, args.hd4_output)
    save(hd2, args.hd2_output)
    print(
        f"{args.input.name}: master={master.size}, hd2={hd2.size}, "
        f"alpha={master.getchannel('A').getbbox()}"
    )


if __name__ == "__main__":
    main()
