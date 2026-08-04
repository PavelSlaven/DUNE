#!/usr/bin/env python3
"""Verify that every Mentat HD2 frame is derived from its HD4 master."""

from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "artifacts" / "mentat_hd_v1" / "data"
MENTAT_IDS = (*range(10, 20), 39)
SCENES = ("platr", "plhar", "plord")


def assert_half_size(hd2, hd4, label: str) -> None:
    small_image = decode_image(hd2.payload)
    master_image = decode_image(hd4.payload)
    if small_image is None or master_image is None:
        raise AssertionError(f"{label}: resource is not a decodable image")
    small = small_image.convert("RGBA")
    master = master_image.convert("RGBA")
    expected = master.resize(small.size, Image.Resampling.LANCZOS)
    if ImageChops.difference(small, expected).getbbox() is not None:
        raise AssertionError(f"{label}: HD2 differs from the HD4 Lanczos derivative")


def main() -> int:
    mentat2 = read_pack(DATA / "sdl_mentat_hd2.dat")
    mentat4 = read_pack(DATA / "sdl_mentat_hd4.dat")
    for resource_id in MENTAT_IDS:
        assert_half_size(mentat2[resource_id], mentat4[resource_id], f"mentat:{resource_id}")

    for scene in SCENES:
        hd2 = read_pack(DATA / "scenes" / "hd2" / f"sdl_{scene}.dat")
        hd4 = read_pack(DATA / "scenes" / "hd4" / f"sdl_{scene}.dat")
        if len(hd2) != len(hd4):
            raise AssertionError(f"{scene}: frame count differs")
        for frame, (small, master) in enumerate(zip(hd2, hd4, strict=True)):
            assert_half_size(small, master, f"{scene}:{frame}")

    print("PASS: all Mentat HD2 frames are exact Lanczos derivatives of HD4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
