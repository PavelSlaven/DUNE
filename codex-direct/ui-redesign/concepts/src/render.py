#!/usr/bin/env python3
"""Render concept HTML pages to PNG with headless Chrome: python render.py [name ...]"""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SIZES = ((800, 600), (1920, 1080))
# Menus are laid out on a reference canvas 600 points high and scaled as a whole (SYSTEM-ui.md, section 2),
# so their 1920x1080 picture is the 1067x600 layout at scale 1.8. The battle screen and the parts sheet use true canvas points.
TRUE_POINTS = ("6-battle", "9-components")


def render(page, width, height, query=""):
    target = OUT / f"{page.stem}-{width}x{height}.png"
    scale = 1.0
    view = (width, height)
    if height > 600 and page.stem not in TRUE_POINTS:
        scale = height / 600
        view = (round(width / scale), 600)
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
            "--allow-file-access-from-files", "--virtual-time-budget=4000",
            f"--window-size={view[0]},{view[1]}", f"--user-data-dir={profile}",
            f"--screenshot={target}", page.as_uri() + query,
        ], check=True, capture_output=True, timeout=120)
    if scale != 1.0:
        from PIL import Image
        image = Image.open(target)
        if image.size != (width, height):
            image.crop((0, 0, width, height)).save(target)
    return target


def main(names):
    sizes = SIZES
    if "--size" in names:
        index = names.index("--size")
        sizes = tuple(tuple(int(part) for part in item.split("x")) for item in names[index + 1].split(","))
        names = names[:index] + names[index + 2:]
    pages = sorted(HERE.glob("[0-9]*.html"))
    if names:
        pages = [page for page in pages if any(page.stem.startswith(name) for name in names)]
    for page in pages:
        for width, height in sizes:
            print(render(page, width, height).name, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
