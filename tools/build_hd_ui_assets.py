#!/usr/bin/env python3
"""Build deterministic HD UI assets from approved ru3 references."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


MENU_BACKGROUND_HD4_SIZE = (5120, 1440)
MENU_BACKGROUND_HD2_SIZE = (2560, 720)
MENU_BACKGROUND_SAFE_SIZE = (2560, 1440)
MENU_LOGO_HD4_SIZE = (1792, 320)
MENU_LOGO_HD2_SIZE = (896, 160)


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def build_menu_background(
    source_path: Path,
    master_path: Path,
    hd2_path: Path,
    hd4_path: Path,
) -> None:
    with Image.open(source_path) as source:
        safe_background = ImageOps.fit(
            source.convert("RGB"),
            MENU_BACKGROUND_SAFE_SIZE,
            Image.Resampling.LANCZOS,
        )
    safe_background = safe_background.filter(
        ImageFilter.UnsharpMask(1.5, 108, 3)
    )

    ambient = safe_background.resize(
        MENU_BACKGROUND_HD4_SIZE,
        Image.Resampling.LANCZOS,
    ).filter(ImageFilter.GaussianBlur(24))
    ambient = ImageEnhance.Color(ambient).enhance(0.68)
    ambient = ImageEnhance.Brightness(ambient).enhance(0.42)

    safe_x = (
        MENU_BACKGROUND_HD4_SIZE[0] - MENU_BACKGROUND_SAFE_SIZE[0]
    ) // 2
    feather = 80
    mask = Image.new("L", MENU_BACKGROUND_SAFE_SIZE, 255)
    mask_draw = ImageDraw.Draw(mask)
    for offset in range(feather):
        alpha = round(255 * (offset + 1) / feather)
        mask_draw.line(
            (offset, 0, offset, mask.height),
            fill=alpha,
        )
        mask_draw.line(
            (mask.width - 1 - offset, 0, mask.width - 1 - offset, mask.height),
            fill=alpha,
        )
    ambient.paste(safe_background, (safe_x, 0), mask)

    save_png(ambient, master_path)
    save_png(ambient, hd4_path)
    save_png(
        ambient.resize(
            MENU_BACKGROUND_HD2_SIZE,
            Image.Resampling.LANCZOS,
        ),
        hd2_path,
    )


def build_menu_logo(
    source_path: Path,
    master_path: Path,
    hd2_path: Path,
    hd4_path: Path,
) -> None:
    with Image.open(source_path) as source:
        logo = source.convert("RGBA")

    alpha = logo.getchannel("A")
    if alpha.getextrema() == (255, 255):
        red, green, blue, _ = logo.split()
        brightness = Image.merge("RGB", (red, green, blue)).convert("L")
        alpha = brightness.point(
            lambda value: 0 if value <= 8 else min(255, (value - 8) * 8)
        )
        logo.putalpha(alpha)
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError(f"No visible logo pixels found in {source_path}")

    left, top, right, bottom = bounds
    padding = max(8, round((bottom - top) * 0.035))
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(logo.width, right + padding)
    bottom = min(logo.height, bottom + padding)
    logo = logo.crop((left, top, right, bottom))

    available_width = MENU_LOGO_HD4_SIZE[0] - 32
    available_height = MENU_LOGO_HD4_SIZE[1] - 24
    scale = min(
        available_width / logo.width,
        available_height / logo.height,
    )
    fitted = logo.resize(
        (
            max(1, round(logo.width * scale)),
            max(1, round(logo.height * scale)),
        ),
        Image.Resampling.LANCZOS,
    )
    hd4 = Image.new("RGBA", MENU_LOGO_HD4_SIZE)
    hd4.alpha_composite(
        fitted,
        (
            (hd4.width - fitted.width) // 2,
            (hd4.height - fitted.height) // 2,
        ),
    )
    hd2 = hd4.resize(
        MENU_LOGO_HD2_SIZE,
        Image.Resampling.LANCZOS,
    )
    save_png(hd4, master_path)
    save_png(hd4, hd4_path)
    save_png(hd2, hd2_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--background", required=True, type=Path)
    parser.add_argument("--logo", required=True, type=Path)
    parser.add_argument("--master-dir", required=True, type=Path)
    parser.add_argument("--hd2-dir", required=True, type=Path)
    parser.add_argument("--hd4-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_menu_background(
        args.background,
        args.master_dir / "main_menu_background.png",
        args.hd2_dir / "main_menu_background.png",
        args.hd4_dir / "main_menu_background.png",
    )
    build_menu_logo(
        args.logo,
        args.master_dir / "main_menu_logo.png",
        args.hd2_dir / "main_menu_logo.png",
        args.hd4_dir / "main_menu_logo.png",
    )
    print("HD menu background and logo built")


if __name__ == "__main__":
    main()
