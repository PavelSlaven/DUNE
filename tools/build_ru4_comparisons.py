#!/usr/bin/env python3
"""Build review sheets for the ru4-preview1 approval gate."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "source_references" / "ru4"
GENERATED = ROOT / "resources" / "hd" / "generated" / "ru4_preview1"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
OUTPUT = ROOT / "resources" / "hd" / "comparisons" / "ru4_preview1"
FONT = ROOT / "resources" / "bin" / "data" / "PTSansNarrow-Regular.ttf"

BACKGROUND = (17, 20, 22)
PANEL = (28, 32, 34)
BORDER = (154, 116, 48)
TEXT = (236, 224, 195)
MUTED = (174, 169, 154)


def open_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def classic(index: int) -> Path:
    return next(CLASSIC.glob(f"{index:04d}_*.png"))


def master(index: int) -> Path:
    return next(MASTER.glob(f"{index:04d}_*.png"))


def checker(size: tuple[int, int], step: int = 16) -> Image.Image:
    canvas = Image.new("RGBA", size, (41, 44, 46, 255))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle(
                    (x, y, min(x + step, size[0]), min(y + step, size[1])),
                    fill=(55, 58, 60, 255),
                )
    return canvas


def fit(image: Image.Image, size: tuple[int, int], transparent: bool = False) -> Image.Image:
    fitted = ImageOps.contain(image.convert("RGBA"), size, Image.Resampling.LANCZOS)
    background = checker(size) if transparent else Image.new("RGBA", size, PANEL)
    background.alpha_composite(
        fitted,
        ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2),
    )
    return background


def montage(
    images: list[Image.Image],
    size: tuple[int, int],
    columns: int,
    transparent: bool = True,
) -> Image.Image:
    rows = (len(images) + columns - 1) // columns
    cell = (size[0] // columns, size[1] // rows)
    canvas = checker(size) if transparent else Image.new("RGBA", size, PANEL)
    for index, image in enumerate(images):
        fitted = ImageOps.contain(
            image.convert("RGBA"),
            (cell[0] - 12, cell[1] - 12),
            Image.Resampling.LANCZOS,
        )
        x = (index % columns) * cell[0] + (cell[0] - fitted.width) // 2
        y = (index // columns) * cell[1] + (cell[1] - fitted.height) // 2
        canvas.alpha_composite(fitted, (x, y))
    return canvas


def atlas_frames(
    path: Path,
    frame_size: tuple[int, int],
    count: int,
    columns: int,
) -> list[Image.Image]:
    atlas = open_rgba(path)
    frames = []
    for index in range(count):
        x = index % columns * frame_size[0]
        y = index // columns * frame_size[1]
        frames.append(atlas.crop((x, y, x + frame_size[0], y + frame_size[1])))
    return frames


def panel(
    canvas: Image.Image,
    xy: tuple[int, int],
    size: tuple[int, int],
    title: str,
    image: Image.Image,
    note: str = "",
) -> None:
    x, y = xy
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(str(FONT), 26)
    note_font = ImageFont.truetype(str(FONT), 18)
    draw.rounded_rectangle(
        (x, y, x + size[0], y + size[1]),
        radius=8,
        fill=PANEL,
        outline=BORDER,
        width=2,
    )
    draw.text((x + 14, y + 8), title, font=title_font, fill=TEXT)
    image_y = y + 44
    image_height = size[1] - 62 - (22 if note else 0)
    content = fit(image, (size[0] - 24, image_height), transparent=True)
    canvas.alpha_composite(content, (x + 12, image_y))
    if note:
        draw.text(
            (x + 14, y + size[1] - 28),
            note,
            font=note_font,
            fill=MUTED,
        )


def build_world_chain() -> None:
    width, height = 1920, 570
    canvas = Image.new("RGBA", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    heading = ImageFont.truetype(str(FONT), 34)
    draw.text(
        (24, 14),
        "D2TM ru4-preview1 — цепочка интеграции игрового мира",
        font=heading,
        fill=TEXT,
    )

    classic_terrain = montage(
        [open_rgba(classic(index)) for index in (121, 120, 123)],
        (430, 390),
        1,
    )
    concept = open_rgba(GENERATED / "terrain_materials.png")
    hd4_terrain = montage(
        [
            open_rgba(master(121)),
            open_rgba(master(120)).crop((0, 0, 512, 128)),
            open_rgba(master(123)).crop((0, 0, 512, 128)),
        ],
        (430, 390),
        1,
    )
    game = open_rgba(OUTPUT / "in_game_1280x720.jpg").crop((0, 70, 850, 745))
    titles = (
        ("1. Исходная геометрия", classic_terrain, "Классические маски D2TM"),
        ("2. Дизайн-лист ImageGen", concept, "Новые материалы и освещение"),
        ("3. Мастер HD4", hd4_terrain, "Размеры и ID атласов сохранены"),
        ("4. Реальный кадр игры", game, "HD2, логический холст 1280×720"),
    )
    for column, (title, image, note) in enumerate(titles):
        panel(canvas, (24 + column * 474, 70), (450, 476), title, image, note)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(
        OUTPUT / "ru4_preview1_world_chain.jpg",
        quality=94,
        subsampling=0,
    )


def build_asset_sheet() -> None:
    width, height = 1800, 1670
    canvas = Image.new("RGBA", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    heading = ImageFont.truetype(str(FONT), 34)
    draw.text(
        (24, 14),
        "D2TM ru4-preview1 — эталонные объекты",
        font=heading,
        fill=TEXT,
    )
    column_titles = ("Источник", "Редизайн ImageGen", "Готовый мастер HD4")
    column_font = ImageFont.truetype(str(FONT), 27)
    for column, title in enumerate(column_titles):
        draw.text((28 + column * 592, 62), title, font=column_font, fill=(220, 171, 72))

    rows: list[tuple[str, list[Image.Image], list[str]]] = []

    rows.append(
        (
            "Харвестер — 8 направлений и 4 ряда анимации",
            [
                open_rgba(SOURCE / "dune2000_harvester.png"),
                open_rgba(GENERATED / "harvester_sheet.png"),
                montage(
                    atlas_frames(master(137), (320, 208), 8, 8),
                    (540, 300),
                    4,
                ),
            ],
            [
                "Dune 2000: форма и ракурсы",
                "Полуреалистичные материалы",
                "8 игровых направлений, точные опоры",
            ],
        )
    )

    tank_sources = montage(
        [
            open_rgba(SOURCE / "dune2000_tank_atreides.png"),
            open_rgba(SOURCE / "dune2000_tank_harkonnen.png"),
            open_rgba(SOURCE / "dune2000_tank_ordos.png"),
        ],
        (540, 300),
        3,
        False,
    )
    tank_designs = montage(
        [
            open_rgba(GENERATED / "tank_atreides_sheet.png"),
            open_rgba(GENERATED / "tank_harkonnen_sheet.png"),
            open_rgba(GENERATED / "tank_ordos_sheet.png"),
        ],
        (540, 300),
        3,
    )
    tank_masters = montage(
        [
            open_rgba(EXTRA / f"HOUSEVARIANT_{house}_UNIT_TANKBASE.png")
            for house in ("ATREIDES", "HARKONNEN", "ORDOS")
        ],
        (540, 300),
        1,
    )
    rows.append(
        (
            "Боевой танк — отдельные варианты трёх Домов",
            [tank_sources, tank_designs, tank_masters],
            [
                "Корпуса Dune 2000",
                "Единый свет и материалы",
                "Корпус/башня раздельно, 8 направлений",
            ],
        )
    )

    building_sources = montage(
        [
            open_rgba(SOURCE / "dune2000_windtrap.png"),
            open_rgba(SOURCE / "dune2000_refinery.png"),
        ],
        (540, 300),
        2,
        False,
    )
    building_designs = montage(
        [
            open_rgba(GENERATED / "windtrap.png"),
            open_rgba(GENERATED / "refinery.png"),
        ],
        (540, 300),
        2,
    )
    building_masters = montage(
        [
            open_rgba(master(40)),
            open_rgba(master(28)).crop((0, 0, 384, 256)),
        ],
        (540, 300),
        2,
    )
    rows.append(
        (
            "Здания — ветряная ловушка и перерабатывающий завод",
            [building_sources, building_designs, building_masters],
            [
                "Dune 2000: композиция",
                "Новые края, свет, цветовые зоны",
                "Прозрачность, маски Домов и тени",
            ],
        )
    )

    action_sources = montage(
        [
            open_rgba(SOURCE / "dune2_infantry.png"),
            open_rgba(SOURCE / "dune2_explosions.png"),
        ],
        (540, 300),
        1,
        False,
    )
    action_designs = montage(
        [
            open_rgba(GENERATED / "infantry_sheet.png"),
            open_rgba(GENERATED / "explosion_sheet.png"),
            open_rgba(GENERATED / "effects_sheet.png"),
        ],
        (540, 300),
        3,
    )
    action_masters = montage(
        [
            open_rgba(master(155)),
            open_rgba(master(68)),
            open_rgba(master(50)),
            open_rgba(master(100)),
        ],
        (540, 300),
        2,
    )
    rows.append(
        (
            "Пехота и эффекты",
            [action_sources, action_designs, action_masters],
            [
                "Dune II: позы и порядок кадров",
                "Цельные управляемые листы",
                "HD4, альфа и аддитивное свечение",
            ],
        )
    )

    row_font = ImageFont.truetype(str(FONT), 25)
    for row_index, (row_title, images, notes) in enumerate(rows):
        y = 102 + row_index * 386
        draw.text((28, y), row_title, font=row_font, fill=TEXT)
        for column in range(3):
            panel(
                canvas,
                (24 + column * 592, y + 38),
                (568, 330),
                column_titles[column],
                images[column],
                notes[column],
            )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(
        OUTPUT / "ru4_preview1_asset_sheet.jpg",
        quality=94,
        subsampling=0,
    )


def main() -> None:
    build_world_chain()
    build_asset_sheet()
    print(OUTPUT)


if __name__ == "__main__":
    main()
