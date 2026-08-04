#!/usr/bin/env python3
"""Add coordinate labels to a regular sprite sheet for visual mapping."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cell", type=int, default=32)
    parser.add_argument(
        "--crop",
        help="Optional left,top,right,bottom crop before labelling",
    )
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--no-label", action="store_true")
    args = parser.parse_args()

    image = Image.open(args.source).convert("RGBA")
    if args.crop:
        image = image.crop(tuple(int(value) for value in args.crop.split(",")))
    if not args.no_label:
        draw = ImageDraw.Draw(image, "RGBA")
        for y in range(0, image.height, args.cell):
            for x in range(0, image.width, args.cell):
                draw.rectangle(
                    (x, y, min(x + 25, image.width - 1), min(y + 9, image.height - 1)),
                    fill=(0, 0, 0, 190),
                )
                draw.text((x + 1, y), f"{x // args.cell},{y // args.cell}", fill="white")
                draw.rectangle(
                    (x, y, min(x + args.cell - 1, image.width - 1), min(y + args.cell - 1, image.height - 1)),
                    outline=(255, 0, 255, 160),
                )
    if args.scale > 1:
        image = image.resize(
            (image.width * args.scale, image.height * args.scale),
            Image.Resampling.NEAREST,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)


if __name__ == "__main__":
    main()
