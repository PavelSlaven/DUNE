#!/usr/bin/env python3
"""Verify installed Trike and Raider Trike direction masters."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
EXPECTED = ROOT / "artifacts" / "trike_direction_fix_v3" / "UNIT_TRIKE_HD4_FIXED.png"
FRAME = (112, 104)


def frame(image: Image.Image, index: int) -> Image.Image:
    return image.crop((index * FRAME[0], 0, (index + 1) * FRAME[0], FRAME[1]))


def main() -> int:
    expected = Image.open(EXPECTED).convert("RGBA")
    failures: list[str] = []
    installed_by_density: dict[int, dict[int, Image.Image]] = {}
    for density in (2, 4):
        entries = read_pack(GAME / "data" / f"sdl_data_hd{density}.dat")
        installed_by_density[density] = {}
        expected_density = expected if density == 4 else expected.resize(
            (expected.width // 2, expected.height // 2),
            Image.Resampling.LANCZOS,
        )
        for resource_id, name in ((162, "Trike"), (147, "Raider Trike")):
            installed = decode_image(entries[resource_id].payload)
            if installed is None:
                failures.append(f"HD{density} {name}: resource cannot be decoded")
                continue
            installed = installed.convert("RGBA")
            installed_by_density[density][resource_id] = installed
            if ImageChops.difference(installed, expected_density).getbbox():
                failures.append(f"HD{density} {name}: atlas differs from corrected master")
        if all(resource_id in installed_by_density[density] for resource_id in (147, 162)):
            if ImageChops.difference(
                installed_by_density[density][147],
                installed_by_density[density][162],
            ).getbbox():
                failures.append(f"HD{density}: Trike and Raider Trike differ")

    for resource_id, name in ((162, "Trike"), (147, "Raider Trike")):
        installed = installed_by_density.get(4, {}).get(resource_id)
        if installed is None:
            continue
        for index, direction in ((1, "NE/13h"), (3, "NW/11h")):
            item = frame(installed, index)
            box = item.getchannel("A").getbbox()
            if box is None or min(box[0], box[1]) < 1:
                failures.append(f"{name}: {direction} frame is empty or clipped")
            if ImageChops.difference(item, frame(expected, index)).getbbox():
                failures.append(f"{name}: incorrect {direction} frame")
    if failures:
        raise AssertionError("; ".join(failures))
    print("Trike direction audit passed: NE/13h and NW/11h are correct for both units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
