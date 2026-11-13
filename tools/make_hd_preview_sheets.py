#!/usr/bin/env python3
"""Build deterministic review sheets for the ru3 HD vertical slice."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


BACKGROUND = (16, 19, 22)
PANEL = (27, 31, 35)
TEXT = (236, 229, 202)
ACCENT = (181, 139, 57)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("C:/Windows/Fonts/seguisb.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS)


def add_panel(
    canvas: Image.Image,
    image: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
) -> None:
    x, y, width, height = box
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=12,
        fill=PANEL,
        outline=ACCENT,
        width=2,
    )
    font = load_font(28)
    draw.text((x + 16, y + 12), title, font=font, fill=TEXT)
    content = fit(image, (width - 32, height - 64))
    canvas.paste(content, (x + 16, y + 50))


def build_overview(style_dir: Path, output_dir: Path) -> None:
    entries = (
        ("gameplay_ui_wide_v1.png", "HUD — широкий режим, 3 карточки"),
        ("gameplay_ui_4x3_v1.png", "HUD — узкий режим, 2 карточки"),
        ("main_menu_background_v1.png", "Главное меню"),
        ("mentat_atreides_v1.png", "Ментат Атрейдесов"),
        ("campaign_map_v1.png", "Карта кампании"),
        ("story_victory_v1.png", "Сюжетный кадр"),
        ("terrain_board_v1.png", "Песок, скалы и пряность"),
        ("explosion_sheet_v1.png", "Эффект взрыва"),
        ("card_harvester_v1.png", "Харвестер"),
        ("card_tank_v1.png", "Танк"),
        ("card_windtrap_v1.png", "Ветряная ловушка"),
        ("card_refinery_v1.png", "Перерабатывающий завод"),
        ("card_constyard_v1.png", "Строительный двор"),
        ("card_heavyfactory_v1.png", "Тяжёлый завод"),
        ("card_siegetank_v1.png", "Осадный танк"),
        ("card_ornithopter_v1.png", "Орнитоптер"),
    )
    row_count = (len(entries) + 1) // 2
    canvas = Image.new(
        "RGB",
        (2400, 140 + row_count * 500),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (60, 36),
        "D2TM v0.8.0-ru3 — эталонный набор HD",
        font=load_font(48),
        fill=TEXT,
    )
    for index, (name, title) in enumerate(entries):
        row, column = divmod(index, 2)
        with Image.open(style_dir / name) as image:
            add_panel(
                canvas,
                image,
                (60 + column * 1170, 120 + row * 500, 1110, 450),
                title,
            )
    canvas.save(output_dir / "style_reference_overview.png", optimize=True)


def build_density_sheet(
    classic_card: Path,
    master4_card: Path,
    output_dir: Path,
) -> None:
    with Image.open(classic_card) as classic_source:
        classic = classic_source.convert("RGB")
    with Image.open(master4_card) as master_source:
        hd4 = master_source.convert("RGB")
    hd2 = hd4.resize((128, 96), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (1500, 430), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (40, 28),
        "Карточка харвестера — физические пиксели при одинаковом игровом размере 64×48",
        font=load_font(30),
        fill=TEXT,
    )
    samples = (
        ("Классика 1× — 64×48", classic),
        ("HD2 — 128×96", hd2),
        ("HD4 — 256×192", hd4),
    )
    x_positions = (60, 330, 650)
    for (label, image), x in zip(samples, x_positions):
        draw.text((x, 110), label, font=load_font(24), fill=TEXT)
        canvas.paste(image, (x, 160))
        draw.rectangle(
            (x - 1, 159, x + image.width, 160 + image.height),
            outline=ACCENT,
            width=1,
        )
    canvas.save(output_dir / "card_density_100pct.png", optimize=True)


def build_viewport_fragments(style_dir: Path, output_dir: Path) -> None:
    with Image.open(style_dir / "gameplay_ui_wide_v1.png") as source:
        wide = source.convert("RGB")
    for width, height, label in (
        (1920, 1080, "1080p"),
        (2560, 1440, "1440p"),
        (3840, 2160, "4K"),
    ):
        viewport = fit(wide, (width, height))
        crop_width = min(1100, width)
        crop_height = min(720, height)
        fragment = viewport.crop(
            (
                width - crop_width,
                max(0, (height - crop_height) // 2),
                width,
                max(0, (height - crop_height) // 2) + crop_height,
            )
        )
        canvas = Image.new(
            "RGB",
            (fragment.width, fragment.height + 64),
            BACKGROUND,
        )
        canvas.paste(fragment, (0, 64))
        ImageDraw.Draw(canvas).text(
            (20, 16),
            f"{label}: фрагмент интерфейса в масштабе 100%",
            font=load_font(28),
            fill=TEXT,
        )
        canvas.save(
            output_dir / f"gameplay_fragment_{label.lower()}.png",
            optimize=True,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style-dir", required=True, type=Path)
    parser.add_argument("--classic-card", required=True, type=Path)
    parser.add_argument("--master4-card", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    build_overview(args.style_dir, args.output_dir)
    build_density_sheet(
        args.classic_card,
        args.master4_card,
        args.output_dir,
    )
    build_viewport_fragments(args.style_dir, args.output_dir)
    print(f"Preview sheets written to {args.output_dir}")


if __name__ == "__main__":
    main()
