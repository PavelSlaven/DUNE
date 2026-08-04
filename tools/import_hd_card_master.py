#!/usr/bin/env python3
"""Import an approved ImageGen card as a deterministic 4x master."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps, ImageStat


MASTER_SIZE = (256, 192)
ART_HEIGHT = 152


def remove_generated_footer(master: Image.Image) -> Image.Image:
    """Expand artwork when ImageGen returned the requested empty footer."""
    footer = master.crop((0, 160, master.width, master.height))
    statistics = ImageStat.Stat(footer)
    mean = sum(statistics.mean) / 3
    deviation = sum(statistics.stddev) / 3
    if mean < 60 and deviation < 3:
        artwork = master.crop((0, 0, master.width, ART_HEIGHT))
        return artwork.resize(MASTER_SIZE, Image.Resampling.LANCZOS)
    return master


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--reference-output", required=True, type=Path)
    parser.add_argument("--master-output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.reference_output.parent.mkdir(parents=True, exist_ok=True)
    args.master_output.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(args.input, args.reference_output)
    with Image.open(args.input) as source:
        master = ImageOps.fit(
            source.convert("RGB"),
            MASTER_SIZE,
            Image.Resampling.LANCZOS,
        )
    master = remove_generated_footer(master)
    master = master.filter(ImageFilter.UnsharpMask(1, 105, 2))
    master.save(args.master_output, optimize=True)
    print(
        f"Imported {args.reference_output.name} -> "
        f"{args.master_output} ({master.width}x{master.height})"
    )


if __name__ == "__main__":
    main()
