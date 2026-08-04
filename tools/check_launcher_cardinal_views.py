#!/usr/bin/env python3
"""Regression check for the launcher east/west frames.

The preview2 launcher first used oblique renders for the cardinal side views,
then put the west-facing render in the east slot.  Keep both failures and the
accepted signatures here so neither mistake can silently return.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from hd_assets import decode_image, read_pack


RESOURCE_ID = 139
DIRECTIONS = {0: "E", 4: "W"}
KNOWN_BAD = {
    2: {"E": "3401ecb0dd80e370", "W": "450ebacb8fa79682"},
    4: {"E": "5ad197b90980f8df", "W": "4fc442cc77862b32"},
}
KNOWN_REVERSED = {
    2: {"E": "18fda4f0c3fe037e", "W": "e55319b8cfc0d5c4"},
    4: {"E": "06b2a4c1758ebac5", "W": "9dde1740581ef14a"},
}
KNOWN_GOOD = {
    2: {"E": "e55319b8cfc0d5c4", "W": "18fda4f0c3fe037e"},
    4: {"E": "9dde1740581ef14a", "W": "06b2a4c1758ebac5"},
}


def frame_signature(image, column: int) -> str:
    frame_width = image.width // 8
    frame = image.crop(
        (column * frame_width, 0, (column + 1) * frame_width, image.height)
    ).convert("RGBA")
    return hashlib.sha256(frame.tobytes()).hexdigest()[:16]


def check_pack(path: Path, density: int) -> list[str]:
    entries = read_pack(path)
    image = decode_image(entries[RESOURCE_ID].payload)
    expected_size = (256 * density, 32 * density)
    errors: list[str] = []
    if image.size != expected_size:
        errors.append(f"HD{density}: atlas {image.size}, expected {expected_size}")
        return errors

    for column, direction in DIRECTIONS.items():
        signature = frame_signature(image, column)
        if signature == KNOWN_BAD[density][direction]:
            errors.append(
                f"HD{density} {direction}: still uses the known oblique frame "
                f"({signature}) instead of a side view"
            )
        elif signature == KNOWN_REVERSED[density][direction]:
            errors.append(
                f"HD{density} {direction}: side-view nose and tail are reversed "
                f"({signature})"
            )
        elif signature != KNOWN_GOOD[density][direction]:
            errors.append(
                f"HD{density} {direction}: unexpected side-view frame "
                f"({signature})"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data_dir",
        nargs="?",
        type=Path,
        default=Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data"),
    )
    args = parser.parse_args()

    errors = []
    errors.extend(check_pack(args.data_dir / "sdl_data_hd2.dat", 2))
    errors.extend(check_pack(args.data_dir / "sdl_data_hd4.dat", 4))
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: launcher E/W side views face the correct directions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
