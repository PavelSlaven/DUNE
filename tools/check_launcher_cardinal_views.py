#!/usr/bin/env python3
"""Lock all eight launcher directions to the approved user atlas."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from hd_assets import decode_image, read_pack


RESOURCE_ID = 139
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
EXPECTED_HD4 = {
    "E": "224fc10663ffc529",
    "NE": "565a2dfeb426f42a",
    "N": "129a3ee90395c5fd",
    "NW": "4c0919c2035a1efe",
    "W": "5840644a7809c97e",
    "SW": "61e6e6690242271a",
    "S": "a4671701f4b3dddb",
    "SE": "90b37495037d799c",
}


def frame_signature(image, column: int) -> str:
    frame_width = image.width // len(DIRECTIONS)
    frame = image.crop(
        (column * frame_width, 0, (column + 1) * frame_width, image.height)
    ).convert("RGBA")
    return hashlib.sha256(frame.tobytes()).hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data_dir",
        nargs="?",
        type=Path,
        default=Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data"),
    )
    args = parser.parse_args()

    path = args.data_dir / "sdl_data_hd4.dat"
    entries = read_pack(path)
    image = decode_image(entries[RESOURCE_ID].payload)
    failures: list[str] = []
    if image is None or image.size != (1024, 128):
        failures.append(
            f"UNIT_LAUNCHER: expected HD4 atlas 1024x128, got "
            f"{None if image is None else image.size}"
        )
    else:
        for column, direction in enumerate(DIRECTIONS):
            signature = frame_signature(image, column)
            if signature != EXPECTED_HD4[direction]:
                failures.append(
                    f"{direction}: unexpected frame {signature}, "
                    f"expected {EXPECTED_HD4[direction]}"
                )

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: launcher uses the approved E, NE, N, NW, W, SW, S, SE atlas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
