#!/usr/bin/env python3
"""Create clean 4x card masters for classic cards without an AI override.

The classic 64x48 cards contain a baked ten-pixel English title strip.  HD
cards render localized names at runtime, so fallback masters keep only the
38-pixel illustration and reserve a clean graphite footer.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


FIRST_CARD_ID = 29
LAST_CARD_ID = 71
MASTER_SIZE = (256, 192)
ART_SIZE = (256, 152)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--classic-dir", required=True, type=Path)
    parser.add_argument("--master-dir", required=True, type=Path)
    parser.add_argument("--status-output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.master_dir.mkdir(parents=True, exist_ok=True)
    approved = []
    generated = []

    for source in sorted(args.classic_dir.glob("*.png")):
        try:
            entry_id = int(source.name[:4])
        except ValueError:
            continue
        if entry_id < FIRST_CARD_ID or entry_id > LAST_CARD_ID:
            continue

        destination = args.master_dir / source.name
        if destination.is_file():
            approved.append(source.name)
            continue

        with Image.open(source) as image:
            rgb = image.convert("RGB")
        if rgb.size != (64, 48):
            raise ValueError(f"{source} has unexpected size {rgb.size}")

        illustration = rgb.crop((0, 0, 64, 38)).resize(
            ART_SIZE,
            Image.Resampling.LANCZOS,
        )
        illustration = ImageEnhance.Contrast(illustration).enhance(1.08)
        illustration = ImageEnhance.Color(illustration).enhance(1.06)
        illustration = illustration.filter(
            ImageFilter.UnsharpMask(1, 115, 2)
        )

        master = Image.new("RGB", MASTER_SIZE, (18, 22, 25))
        master.paste(illustration, (0, 0))
        master.save(destination, optimize=True)
        generated.append(source.name)

    status = {
        "format": 1,
        "card_range": [FIRST_CARD_ID, LAST_CARD_ID],
        "approved_ai_masters": approved,
        "clean_fallback_masters": generated,
        "total": len(approved) + len(generated),
    }
    args.status_output.parent.mkdir(parents=True, exist_ok=True)
    args.status_output.write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Card masters: {len(approved)} AI, "
        f"{len(generated)} clean fallback, total={status['total']}"
    )


if __name__ == "__main__":
    main()
