#!/usr/bin/env python3
"""Remove legacy/generated title strips from HD card masters."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter

from import_hd_card_master import remove_generated_footer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--master-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    changed = 0
    checked = 0
    for path in sorted(args.master_dir.glob("*.png")):
        try:
            entry_id = int(path.name[:4])
        except ValueError:
            continue
        if not 29 <= entry_id <= 71:
            continue
        with Image.open(path) as source:
            master = source.convert("RGB")
        if master.size != (256, 192):
            raise ValueError(f"{path} has unexpected size {master.size}")
        normalized = remove_generated_footer(master)
        checked += 1
        if normalized.tobytes() == master.tobytes():
            continue
        normalized = normalized.filter(ImageFilter.UnsharpMask(1, 105, 2))
        normalized.save(path, optimize=True)
        changed += 1
    print(f"Normalized HD cards: changed={changed}, checked={checked}")


if __name__ == "__main__":
    main()
