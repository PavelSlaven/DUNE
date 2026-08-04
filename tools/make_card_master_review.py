#!/usr/bin/env python3
"""Create a compact review sheet for all HD construction cards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--master-dir", required=True, type=Path)
    parser.add_argument("--names", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--font", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cards = json.loads(args.names.read_text(encoding="utf-8"))["cards"]
    font = (
        ImageFont.truetype(str(args.font), 18)
        if args.font and args.font.is_file()
        else ImageFont.load_default()
    )
    columns = 5
    cell_width = 272
    cell_height = 236
    rows = (len(cards) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (columns * cell_width, rows * cell_height),
        (13, 16, 18),
    )
    draw = ImageDraw.Draw(sheet)

    for index, card in enumerate(cards):
        entry_id = card["id"]
        matches = sorted(args.master_dir.glob(f"{entry_id:04d}_*.png"))
        if len(matches) != 1:
            raise ValueError(f"expected one master for ID {entry_id}: {matches}")
        with Image.open(matches[0]) as source:
            image = source.convert("RGB")
        if image.size != (256, 192):
            raise ValueError(f"{matches[0]} has size {image.size}")

        x = (index % columns) * cell_width + 8
        y = (index // columns) * cell_height + 8
        sheet.paste(image, (x, y))
        label = f"{entry_id}: {card['name']}"
        draw.text((x, y + 198), label, font=font, fill=(232, 220, 188))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, optimize=True)
    print(f"Created {args.output} ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
