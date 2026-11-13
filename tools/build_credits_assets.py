#!/usr/bin/env python3
"""Build density-aware credits artwork from the preserved original assets."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "classic" / "sdl_inter"
OUTPUT = ROOT / "resources" / "bin" / "data"
ASSETS = {
    "credits_team.png": SOURCE / "0021_CREDITS_DUNE2_CORE_TEAM.png",
    "credits_title.png": SOURCE / "0022_D2TM_TITLE.png",
}


def main() -> int:
    for density in (2, 4):
        destination = OUTPUT / f"hd{density}"
        destination.mkdir(parents=True, exist_ok=True)
        for name, source in ASSETS.items():
            with Image.open(source) as original:
                image = original.convert("RGBA").resize(
                    (original.width * density, original.height * density),
                    Image.Resampling.LANCZOS,
                )
            image.save(destination / name, optimize=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
