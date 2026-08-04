from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage


DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
SOURCE_COLUMNS = 8
SOURCE_ROWS = 5
OUTPUT_ROWS = 4
FRAME_SIZE = (320, 208)
LOGICAL_FRAME_SIZE = (80, 52)


def chroma_to_rgba(image: Image.Image) -> Image.Image:
    rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    green_excess = rgb[:, :, 1] - np.maximum(rgb[:, :, 0], rgb[:, :, 2])
    alpha = np.clip(
        (55.0 - green_excess.astype(np.float32)) * 255.0 / 40.0,
        0,
        255,
    ).astype(np.uint8)

    # Remove residual green from antialiased edge pixels before resampling.
    clean = rgb.copy()
    dominant_green = np.maximum(clean[:, :, 0], clean[:, :, 2])
    spill = np.maximum(clean[:, :, 1] - dominant_green, 0).astype(np.float32)
    clean[:, :, 1] -= (
        spill * (255.0 - alpha.astype(np.float32)) / 255.0
    ).astype(np.int16)
    clean = np.clip(clean, 0, 255).astype(np.uint8)
    clean[alpha == 0] = 0
    return Image.fromarray(np.dstack((clean, alpha)), "RGBA")


def grid_bounds(length: int, count: int) -> list[int]:
    return [round(index * length / count) for index in range(count + 1)]


def detect_row_bounds(source: Image.Image) -> list[int]:
    rgb = np.asarray(source.convert("RGB"), dtype=np.int16)
    green_excess = rgb[:, :, 1] - np.maximum(rgb[:, :, 0], rgb[:, :, 2])
    foreground_per_row = np.count_nonzero(green_excess < 45, axis=1)
    active = foreground_per_row > 100
    runs: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(active):
        if value and start is None:
            start = index
        elif not value and start is not None:
            runs.append((start, index - 1))
            start = None
    if start is not None:
        runs.append((start, len(active) - 1))
    if len(runs) != SOURCE_ROWS:
        raise ValueError(f"Expected {SOURCE_ROWS} sprite rows, found {len(runs)}")
    return [
        0,
        *[round((runs[index][1] + runs[index + 1][0]) / 2) for index in range(SOURCE_ROWS - 1)],
        source.height,
    ]


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    mask = alpha > 72
    columns = np.count_nonzero(mask, axis=0)
    rows = np.count_nonzero(mask, axis=1)
    xs = np.flatnonzero(columns >= 4)
    ys = np.flatnonzero(rows >= 4)
    if not len(xs) or not len(ys):
        raise ValueError("Empty sprite cell")
    return int(xs[0]), int(ys[0]), int(xs[-1] + 1), int(ys[-1] + 1)


def chassis_anchor(image: Image.Image) -> tuple[float, float]:
    rgba = np.asarray(image, dtype=np.int16)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    armor = (
        (alpha > 128)
        & (red > 70)
        & (red > green * 1.35)
        & (red > blue * 1.25)
    )
    ys, xs = np.nonzero(armor)
    if len(xs) < 40:
        left, top, right, bottom = alpha_bbox(image)
        return (left + right) / 2, (top + bottom) / 2
    return (float(np.median(xs)), float(np.median(ys)))


def filter_foreign_components(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image, dtype=np.uint8).copy()
    anchor = chassis_anchor(image)
    mask = rgba[:, :, 3] > 48
    labels, count = ndimage.label(mask, structure=np.ones((3, 3), dtype=np.uint8))
    keep = np.zeros_like(mask)
    for label_id in range(1, count + 1):
        ys, xs = np.nonzero(labels == label_id)
        if not len(xs):
            continue
        size = len(xs)
        distance = float(np.hypot(xs.mean() - anchor[0], ys.mean() - anchor[1]))
        red = rgba[ys, xs, 0].astype(np.int16)
        green = rgba[ys, xs, 1].astype(np.int16)
        blue = rgba[ys, xs, 2].astype(np.int16)
        contains_armor = bool(
            np.any((red > 70) & (red > green * 1.35) & (red > blue * 1.25))
        )
        if contains_armor or (size >= 12 and distance <= 118):
            keep[ys, xs] = True
    rgba[~keep] = 0
    return Image.fromarray(rgba, "RGBA")


def composite_resized_cell(
    cell: Image.Image,
    anchor: tuple[float, float],
    target_anchor: tuple[float, float],
    scale: float,
) -> Image.Image:
    resized = cell.resize(
        (round(cell.width * scale), round(cell.height * scale)),
        Image.Resampling.LANCZOS,
    )
    frame = Image.new("RGBA", FRAME_SIZE)
    destination = (
        round(target_anchor[0] - anchor[0] * scale),
        round(target_anchor[1] - anchor[1] * scale),
    )
    frame.alpha_composite(resized, destination)
    return frame


def build_atlas(source: Image.Image) -> tuple[Image.Image, float]:
    rgba = chroma_to_rgba(source)
    xs = grid_bounds(rgba.width, SOURCE_COLUMNS)
    ys = detect_row_bounds(source)
    cells: list[list[Image.Image]] = []
    for row in range(OUTPUT_ROWS):
        cells.append(
            [
                filter_foreign_components(
                    rgba.crop((xs[column], ys[row], xs[column + 1], ys[row + 1]))
                )
                for column in range(SOURCE_COLUMNS)
            ]
        )

    anchors = [
        [chassis_anchor(cells[row][column]) for column in range(SOURCE_COLUMNS)]
        for row in range(OUTPUT_ROWS)
    ]
    extents: list[tuple[float, float, float, float]] = []
    scale = 1.3
    for column in range(SOURCE_COLUMNS):
        left = right = up = down = 0.0
        for row in range(OUTPUT_ROWS):
            box = alpha_bbox(cells[row][column])
            anchor = anchors[row][column]
            left = max(left, anchor[0] - box[0])
            right = max(right, box[2] - anchor[0])
            up = max(up, anchor[1] - box[1])
            down = max(down, box[3] - anchor[1])
        extents.append((left, right, up, down))
        scale = min(
            scale,
            (FRAME_SIZE[0] - 16) / (left + right),
            (FRAME_SIZE[1] - 16) / (up + down),
        )

    target_anchors: list[tuple[float, float]] = []
    for left, right, up, down in extents:
        min_x = 8 + left * scale
        max_x = FRAME_SIZE[0] - 8 - right * scale
        min_y = 8 + up * scale
        max_y = FRAME_SIZE[1] - 8 - down * scale
        target_anchors.append(
            (
                min(max(FRAME_SIZE[0] / 2, min_x), max_x),
                min(max(FRAME_SIZE[1] / 2, min_y), max_y),
            )
        )

    atlas = Image.new(
        "RGBA",
        (FRAME_SIZE[0] * SOURCE_COLUMNS, FRAME_SIZE[1] * OUTPUT_ROWS),
    )
    for row in range(OUTPUT_ROWS):
        for column in range(SOURCE_COLUMNS):
            frame = composite_resized_cell(
                cells[row][column],
                anchors[row][column],
                target_anchors[column],
                scale,
            )
            atlas.alpha_composite(
                frame,
                (column * FRAME_SIZE[0], row * FRAME_SIZE[1]),
            )
    return atlas, scale


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def draw_panel(
    board: Image.Image,
    sprite: Image.Image,
    position: tuple[int, int],
    label: str,
    display_size: tuple[int, int],
    terrain: bool = False,
) -> None:
    x, y = position
    width, height = display_size
    draw = ImageDraw.Draw(board)
    panel_color = (181, 136, 75, 255) if terrain else (25, 28, 32, 255)
    draw.rounded_rectangle(
        (x - 8, y - 8, x + width + 8, y + height + 34),
        radius=8,
        fill=panel_color,
        outline=(176, 132, 52, 255),
        width=2,
    )
    if terrain:
        for offset in range(0, width + height, 14):
            draw.line(
                (x + offset, y, x, y + offset),
                fill=(190, 145, 80, 70),
                width=1,
            )
    shown = sprite.resize(display_size, Image.Resampling.LANCZOS)
    board.alpha_composite(shown, (x, y))
    label_font = load_font(18, bold=True)
    label_box = draw.textbbox((0, 0), label, font=label_font)
    label_width = label_box[2] - label_box[0]
    draw.text(
        (x + (width - label_width) / 2, y + height + 6),
        label,
        font=label_font,
        fill=(245, 221, 167, 255),
    )


def frame_from_atlas(atlas: Image.Image, column: int, row: int) -> Image.Image:
    x = column * FRAME_SIZE[0]
    y = row * FRAME_SIZE[1]
    return atlas.crop((x, y, x + FRAME_SIZE[0], y + FRAME_SIZE[1]))


def build_review_board(atlas: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1780, 940), (10, 12, 15, 255))
    draw = ImageDraw.Draw(board)
    title_font = load_font(34, bold=True)
    section_font = load_font(23, bold=True)
    body_font = load_font(18)

    draw.text(
        (40, 26),
        "Харвестер — предварительный HD4-мастер",
        font=title_font,
        fill=(228, 67, 52, 255),
    )
    draw.text(
        (40, 72),
        "Строгий порядок направлений движка; без интеграции до утверждения",
        font=body_font,
        fill=(205, 206, 208, 255),
    )

    draw.text((40, 112), "Направления — кадр 0 (HD4 показан в 50%)", font=section_font, fill=(226, 190, 100, 255))
    for column, direction in enumerate(DIRECTIONS):
        draw_panel(
            board,
            frame_from_atlas(atlas, column, 0),
            (50 + column * 215, 155),
            direction,
            (160, 104),
        )

    draw.text((40, 320), "Реальный игровой кадр 80×52 (для просмотра увеличен в 2 раза)", font=section_font, fill=(226, 190, 100, 255))
    logical_frames: list[Image.Image] = []
    for column, direction in enumerate(DIRECTIONS):
        logical = frame_from_atlas(atlas, column, 0).resize(
            LOGICAL_FRAME_SIZE,
            Image.Resampling.LANCZOS,
        )
        logical_frames.append(logical)
        draw_panel(
            board,
            logical,
            (50 + column * 215, 363),
            direction,
            (160, 104),
            terrain=True,
        )

    draw.text((40, 528), "Четыре фазы — направления E и S", font=section_font, fill=(226, 190, 100, 255))
    animation_columns = ((0, "E"), (6, "S"))
    for group, (column, direction) in enumerate(animation_columns):
        group_x = 50 + group * 860
        for row in range(OUTPUT_ROWS):
            logical = frame_from_atlas(atlas, column, row).resize(
                LOGICAL_FRAME_SIZE,
                Image.Resampling.LANCZOS,
            )
            draw_panel(
                board,
                logical,
                (group_x + row * 205, 575),
                f"{direction} · фаза {row}",
                (160, 104),
                terrain=True,
            )

    draw.text(
        (40, 790),
        "Контракт: 2560×832 RGBA · 8×4 · кадр HD4 320×208 · логический кадр 80×52",
        font=body_font,
        fill=(205, 206, 208, 255),
    )
    draw.text(
        (40, 822),
        "Палитра: красная броня, графитовый корпус, янтарные огни, песок исходной гаммы.",
        font=body_font,
        fill=(205, 206, 208, 255),
    )

    # A literal 1:1 strip lets the user inspect the size when opening the board at 100%.
    draw.text((40, 862), "Буквальный масштаб 1:1:", font=body_font, fill=(205, 206, 208, 255))
    strip_x = 240
    for logical in logical_frames:
        board.alpha_composite(logical, (strip_x, 852))
        strip_x += LOGICAL_FRAME_SIZE[0] + 8
    return board


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    source = Image.open(args.source)
    atlas, scale = build_atlas(source)
    atlas_path = args.output_dir / "UNIT_HARVESTER_HD4_PREVIEW.png"
    atlas.save(atlas_path)

    hd2 = atlas.resize(
        (atlas.width // 2, atlas.height // 2),
        Image.Resampling.LANCZOS,
    )
    hd2.save(args.output_dir / "UNIT_HARVESTER_HD2_PREVIEW.png")

    review = build_review_board(atlas)
    review.save(args.output_dir / "UNIT_HARVESTER_REVIEW.png")

    manifest = {
        "resource": "UNIT_HARVESTER",
        "resource_id": 137,
        "status": "preview_not_integrated",
        "direction_order": list(DIRECTIONS),
        "frames": OUTPUT_ROWS,
        "logical_frame": list(LOGICAL_FRAME_SIZE),
        "hd2_frame": [value * 2 for value in LOGICAL_FRAME_SIZE],
        "hd4_frame": list(FRAME_SIZE),
        "hd4_atlas": list(atlas.size),
        "normalization_scale": round(scale, 6),
        "source_rows_used": [0, 1, 2, 3],
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
