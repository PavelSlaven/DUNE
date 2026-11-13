#!/usr/bin/env python3
"""Lock the independent north/south launcher views from the user atlas."""

from __future__ import annotations

import hashlib
from pathlib import Path

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "resources" / "bin" / "data" / "sdl_data_hd4.dat"
FRAME = 128
NORTH = 2
SOUTH = 6
EXPECTED = {
    139: {
        "name": "UNIT_LAUNCHER",
        "N": "129a3ee90395c5fd",
        "S": "a4671701f4b3dddb",
    },
    179: {
        "name": "HM_UNIT_LAUNCHER",
        "N": "566082401d9c9583",
        "S": "184a011c8f526eef",
    },
}


def signature(atlas, index: int) -> str:
    frame = atlas.crop(
        (index * FRAME, 0, (index + 1) * FRAME, FRAME)
    ).convert("RGBA")
    return hashlib.sha256(frame.tobytes()).hexdigest()[:16]


def main() -> int:
    entries = read_pack(PACK)
    failures: list[str] = []
    for resource_id, expected in EXPECTED.items():
        entry = entries[resource_id]
        if entry.name != expected["name"]:
            failures.append(
                f"ID {resource_id}: expected {expected['name']}, got {entry.name}"
            )
            continue
        atlas = decode_image(entry.payload)
        if atlas is None or atlas.size != (FRAME * 8, FRAME):
            failures.append(f"{expected['name']}: invalid atlas")
            continue
        for label, index in (("N", NORTH), ("S", SOUTH)):
            actual = signature(atlas, index)
            if actual != expected[label]:
                failures.append(
                    f"{expected['name']} {label}: {actual}, expected {expected[label]}"
                )

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: launcher N/S body and mask match the approved independent views")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
