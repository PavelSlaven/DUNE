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


def render(page, width, height, query=""):
    target = OUT / f"{page.stem}-{width}x{height}.png"
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            "--allow-file-access-from-files", "--virtual-time-budget=4000",
            f"--window-size={width},{height}", f"--user-data-dir={profile}",
            f"--screenshot={target}", page.as_uri() + query,
        ], check=True, capture_output=True, timeout=120)
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
