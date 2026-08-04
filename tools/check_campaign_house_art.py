#!/usr/bin/env python3
"""Reject pixel-doubled classic House art in the HD interface packs."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import ImageChops, Image

from hd_assets import decode_image, read_pack


HOUSE_IDS = {
    11: "Atreides",
    12: "Harkonnen",
    13: "Ordos",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data_dir",
        nargs="?",
        type=Path,
        default=Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data"),
    )
    parser.add_argument(
        "--classic-data-dir",
        type=Path,
        default=None,
        help="Directory containing sdl_inter.dat when checking staged HD packs",
    )
    args = parser.parse_args()

    classic_dir = args.classic_data_dir or args.data_dir
    classic = read_pack(classic_dir / "sdl_inter.dat")
    errors: list[str] = []
    for density in (2, 4):
        hd = read_pack(args.data_dir / f"sdl_inter_hd{density}.dat")
        for resource_id, house in HOUSE_IDS.items():
            # Image.getbbox() on an RGBA difference may report an empty box
            # when RGB differs but the alpha difference is zero.  The check is
            # about visible artwork, so compare the visible RGB channels.
            source = decode_image(classic[resource_id].payload).convert("RGB")
            actual = decode_image(hd[resource_id].payload).convert("RGB")
            nearest = source.resize(actual.size, Image.Resampling.NEAREST)
            if ImageChops.difference(actual, nearest).getbbox() is None:
                errors.append(
                    f"HD{density} {house}: exact nearest-neighbour upscale "
                    f"of classic {source.size} art"
                )

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: campaign House art contains real HD detail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
