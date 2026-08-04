#!/usr/bin/env python3
"""Build an approval-ready HD4 UNIT_SABOTEUR atlas."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from check_saboteur_scale_stability import metrics as scale_metrics
from prepare_soldiers_review import apply_engine_tint


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "saboteur_review_v1"
SOURCE = OUTPUT / "saboteur_walk_sheet_alpha.png"
CLASSIC = OUTPUT / "UNIT_SABOTEUR_classic.png"

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROWS = 4
SOURCE_COLUMNS = 9
FRAME = (128, 128)
ATLAS = (1024, 512)
TARGET_HEIGHT = 44

# The generated design sheet follows the clockwise turn used by the supplied
# reference. One near-duplicate oblique column is intentionally skipped.
SOURCE_COLUMN = {
    "E": 3,
    "NE": 4,
    "N": 5,
    "NW": 6,
    "W": 7,
    "SW": 8,
    "S": 0,
    "SE": 2,
}

PHASE_LOWER_BODY_OFFSETS = (-2, 0, 2, 0)

BASE_OUT = OUTPUT / "UNIT_SABOTEUR_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SABOTEUR_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SABOTEUR_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SABOTEUR_ANIMATION_PREVIEW.gif"
MANIFEST_OUT = OUTPUT / "manifest.json"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
    "Император": (125, 0, 125),
    "Наёмники": (200, 200, 200),
    "Фримены": (0, 205, 205),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def source_cell(sheet: Image.Image, column: int, row: int) -> Image.Image:
    left = round(column * sheet.width / SOURCE_COLUMNS)
    right = round((column + 1) * sheet.width / SOURCE_COLUMNS)
    top = round(row * sheet.height / ROWS)
    bottom = round((row + 1) * sheet.height / ROWS)
    cell = sheet.crop((left, top, right, bottom))
    alpha_box = cell.getchannel("A").getbbox()
    if alpha_box is None:
        raise AssertionError(f"empty source cell {column},{row}")
    cell = cell.crop(alpha_box)
    scale = TARGET_HEIGHT / cell.height
    width = max(1, round(cell.width * scale))
    return cell.resize((width, TARGET_HEIGHT), Image.Resampling.LANCZOS)


def stable_walk_cell(
    sheet: Image.Image,
    column: int,
    phase: int,
) -> Image.Image:
    """Animate the legs without regenerating or rescaling the torso."""
    source = source_cell(sheet, column, 0)
    base = Image.new("RGBA", (source.width + 8, source.height))
    base.alpha_composite(source, (4, 0))
    offset = PHASE_LOWER_BODY_OFFSETS[phase]
    if offset == 0:
        return base

    split_y = round(base.height * 0.62)
    output = base.copy()
    clear = Image.new("RGBA", (base.width, base.height - split_y))
    output.paste(clear, (0, split_y))
    lower_body = base.crop((0, split_y, base.width, base.height))
    output.alpha_composite(lower_body, (offset, split_y))
    return output


def classic_anchors(classic: Image.Image) -> list[tuple[float, int]]:
    anchors: list[tuple[float, int]] = []
    for column in range(len(DIRECTIONS)):
        centers: list[float] = []
        bottoms: list[int] = []
        for row in range(ROWS):
            cell = classic.crop(
                (
                    column * 32,
                    row * 32,
                    (column + 1) * 32,
                    (row + 1) * 32,
                )
            )
            box = cell.getchannel("A").getbbox()
            if box is None:
                raise AssertionError(f"empty classic frame {column},{row}")
            centers.append((box[0] + box[2]) * 2.0)
            bottoms.append(box[3] * 4)
        anchors.append((float(np.median(centers)), max(bottoms)))
    return anchors


def build_colored_atlas(
    sheet: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    anchors = classic_anchors(classic)
    atlas = Image.new("RGBA", ATLAS)
    for row in range(ROWS):
        for column, direction in enumerate(DIRECTIONS):
            sprite = stable_walk_cell(
                sheet,
                SOURCE_COLUMN[direction],
                row,
            )
            anchor_x, anchor_y = anchors[column]
            output = Image.new("RGBA", FRAME)
            output.alpha_composite(
                sprite,
                (
                    round(anchor_x - sprite.width / 2.0),
                    anchor_y - sprite.height,
                ),
            )
            atlas.alpha_composite(
                output,
                (column * FRAME[0], row * FRAME[1]),
            )
    return atlas


def red_selection(image: Image.Image) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    dominance = red - np.maximum(green, blue)
    saturation = (
        np.max(rgba[:, :, :3], axis=2)
        - np.min(rgba[:, :, :3], axis=2)
    )
    selection = np.clip((dominance - 12.0) / 90.0, 0.0, 1.0)
    selection *= np.clip((saturation - 18.0) / 100.0, 0.0, 1.0)
    selection *= np.clip((red - 35.0) / 90.0, 0.0, 1.0)
    selection *= np.clip((red * 0.52 - green + 12.0) / 35.0, 0.0, 1.0)
    selection *= alpha / 255.0
    return selection


def build_neutral_and_mask(
    colored: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(colored.convert("RGBA"), dtype=np.float32)
    selection = red_selection(colored)
    blend = selection[:, :, None] * 0.93
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    )
    neutral_rgb = np.stack(
        (
            np.clip(luminance * 0.92 + 14, 0, 255),
            np.clip(luminance * 0.97 + 16, 0, 255),
            np.clip(luminance * 1.04 + 19, 0, 255),
        ),
        axis=2,
    )
    output = rgba.copy()
    output[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - blend) + neutral_rgb * blend
    )
    neutral = Image.fromarray(
        np.clip(output, 0, 255).astype(np.uint8),
        "RGBA",
    )
    mask_alpha = np.clip(selection * 205.0, 0, 205).astype(np.uint8)
    mask = Image.new("RGBA", colored.size, (255, 255, 255, 0))
    mask.putalpha(
        Image.fromarray(mask_alpha, "L").filter(
            ImageFilter.GaussianBlur(0.45)
        )
    )
    return neutral, mask


def atlas_frame(
    atlas: Image.Image,
    column: int,
    row: int = 0,
) -> Image.Image:
    return atlas.crop(
        (
            column * FRAME[0],
            row * FRAME[1],
            (column + 1) * FRAME[0],
            (row + 1) * FRAME[1],
        )
    )


def logical_alpha(
    atlas: Image.Image,
    column: int,
    row: int,
) -> np.ndarray:
    return np.asarray(
        atlas_frame(atlas, column, row)
        .getchannel("A")
        .resize((32, 32), Image.Resampling.LANCZOS),
        dtype=np.float32,
    ) / 255.0


def centroid(alpha: np.ndarray) -> tuple[float, float]:
    total = float(alpha.sum())
    if total <= 0:
        raise AssertionError("empty animation frame")
    y_grid, x_grid = np.indices(alpha.shape)
    return (
        float((x_grid * alpha).sum() / total),
        float((y_grid * alpha).sum() / total),
    )


def animation_metrics(atlas: Image.Image) -> dict[str, object]:
    report: dict[str, object] = {}
    for column, direction in enumerate(DIRECTIONS):
        frames = [logical_alpha(atlas, column, row) for row in range(ROWS)]
        centers = [centroid(item) for item in frames]
        transitions = [
            float(
                np.mean(
                    np.abs(frames[(row + 1) % ROWS] - frames[row])
                )
            )
            for row in range(ROWS)
        ]
        nonzero = [value for value in transitions if value > 0.0005]
        unevenness = (
            max(nonzero) / max(min(nonzero), 0.0035)
            if nonzero
            else 0.0
        )
        report[direction] = {
            "centroid_span_x": round(
                max(item[0] for item in centers)
                - min(item[0] for item in centers),
                4,
            ),
            "centroid_span_y": round(
                max(item[1] for item in centers)
                - min(item[1] for item in centers),
                4,
            ),
            "transitions": [round(item, 6) for item in transitions],
            "transition_unevenness": round(unevenness, 4),
        }
    return report


def validate(
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    failures: list[str] = []
    if colored.size != ATLAS or neutral.size != ATLAS or mask.size != ATLAS:
        failures.append("atlas size must be 1024x512")
    if colored.mode != "RGBA" or neutral.mode != "RGBA" or mask.mode != "RGBA":
        failures.append("all atlases must use RGBA")

    bounds: dict[str, object] = {}
    for column, direction in enumerate(DIRECTIONS):
        direction_bounds: list[list[int]] = []
        for row in range(ROWS):
            box = atlas_frame(colored, column, row).getchannel("A").getbbox()
            if box is None:
                failures.append(f"empty frame {direction}:{row}")
                continue
            direction_bounds.append(list(box))
            height = box[3] - box[1]
            if not 42 <= height <= 45:
                failures.append(
                    f"{direction}:{row} height {height} is outside 42..45"
                )
        bounds[direction] = direction_bounds

    metrics = animation_metrics(colored)
    for direction, values in metrics.items():
        span_x = float(values["centroid_span_x"])
        span_y = float(values["centroid_span_y"])
        unevenness = float(values["transition_unevenness"])
        if span_x > 1.35 or span_y > 1.35:
            failures.append(
                f"{direction} anchor jump {span_x:.2f}x{span_y:.2f}"
            )
        if unevenness > 2.8:
            failures.append(
                f"{direction} uneven transitions {unevenness:.2f}"
            )

    down2 = neutral.resize((512, 256), Image.Resampling.LANCZOS)
    roundtrip = down2.resize(ATLAS, Image.Resampling.NEAREST)
    if ImageChops.difference(neutral, roundtrip).getbbox() is None:
        failures.append("HD4 appears to be a nearest-neighbour upscale")

    scale_report = scale_metrics(colored)
    return {
        "status": "approved_preview" if not failures else "failed",
        "resource_id": 149,
        "resource": "UNIT_SABOTEUR",
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "columns": 8,
        "rows": 4,
        "direction_order": list(DIRECTIONS),
        "target_character_height_hd4": TARGET_HEIGHT,
        "target_character_height_logical": TARGET_HEIGHT / 4,
        "anchor": "classic per-direction center and lower baseline",
        "source_columns": SOURCE_COLUMN,
        "animation": {
            "source_pose_per_direction": 0,
            "lower_body_offsets_hd4": PHASE_LOWER_BODY_OFFSETS,
            "torso_scale_is_constant": True,
        },
        "bounds": bounds,
        "animation_metrics": metrics,
        "scale_stability": {
            "max_area_ratio": max(
                float(value["area_ratio"])
                for value in scale_report.values()
            ),
            "max_upper_body_area_ratio": max(
                float(value["upper_body_area_ratio"])
                for value in scale_report.values()
            ),
            "max_height_span_hd4": max(
                int(value["height_span"])
                for value in scale_report.values()
            ),
        },
        "house_mask_colors": list(HOUSE_COLORS),
        "failures": failures,
        "installed": False,
    }


def draw_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    size: int,
    label: str,
) -> None:
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle(
        (x, y, x + size, y + size + 34),
        radius=7,
        fill=(22, 26, 31, 255),
        outline=(138, 105, 48, 255),
        width=2,
    )
    board.alpha_composite(
        sprite.resize((size, size), Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.text(
        (x + 8, y + size + 5),
        label,
        font=font(16, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
    manifest: dict[str, object],
) -> Image.Image:
    ordos = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    board = Image.new("RGBA", (1780, 1420), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Диверсант — UNIT_SABOTEUR HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "8 направлений × 4 фазы, кадр 32×32 логических пикселя",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    for column, direction in enumerate(DIRECTIONS):
        draw_card(
            board,
            atlas_frame(ordos, column),
            34 + column * 216,
            110,
            190,
            direction,
        )

    draw.text(
        (34, 350),
        "Плавный цикл движения — направление SE",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for row in range(ROWS):
        draw_card(
            board,
            atlas_frame(ordos, 7, row),
            34 + row * 260,
            395,
            230,
            f"фаза {row + 1}",
        )

    draw.text(
        (1110, 350),
        "Маска фракции",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    draw_card(board, atlas_frame(colored, 7), 1110, 395, 190, "эталон")
    draw_card(board, atlas_frame(neutral, 7), 1325, 395, 190, "основа")
    draw_card(board, atlas_frame(mask, 7), 1540, 395, 190, "маска")

    draw.text(
        (34, 705),
        "Реальный игровой масштаб и шесть цветов",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    panel = Image.new("RGBA", (1710, 235), (25, 27, 25, 255))
    panel_draw = ImageDraw.Draw(panel)
    for y in range(0, panel.height, 32):
        for x in range(0, panel.width, 32):
            shade = 48 if (x // 32 + y // 32) % 2 else 39
            panel_draw.rectangle(
                (x, y, x + 31, y + 31),
                fill=(shade, shade, shade, 255),
            )
    for index, (label, color) in enumerate(HOUSE_COLORS.items()):
        tinted = apply_engine_tint(neutral, mask, color)
        panel.alpha_composite(atlas_frame(tinted, 7), (70 + index * 270, 48))
        panel_draw.text(
            (65 + index * 270, 180),
            label,
            font=font(17, True),
            fill=(226, 218, 194, 255),
        )
    board.alpha_composite(panel, (34, 750))

    draw.text(
        (34, 1025),
        "Контроль",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    draw.text(
        (34, 1070),
        "• высота: 44 HD4 px = 11 логических px;",
        font=font(20),
        fill=(205, 210, 216, 255),
    )
    draw.text(
        (34, 1105),
        "• опорная точка и порядок направлений взяты из классического атласа;",
        font=font(20),
        fill=(205, 210, 216, 255),
    )
    draw.text(
        (34, 1140),
        "• нижняя граница одинакова во всех четырёх фазах каждого направления;",
        font=font(20),
        fill=(205, 210, 216, 255),
    )
    max_span = max(
        max(
            float(value["centroid_span_x"]),
            float(value["centroid_span_y"]),
        )
        for value in manifest["animation_metrics"].values()
    )
    max_unevenness = max(
        float(value["transition_unevenness"])
        for value in manifest["animation_metrics"].values()
    )
    scale_stability = manifest["scale_stability"]
    draw.text(
        (34, 1175),
        f"• максимальный сдвиг центра: {max_span:.2f} лог. px; "
        f"неравномерность переходов: {max_unevenness:.2f}.",
        font=font(20),
        fill=(205, 210, 216, 255),
    )
    draw.text(
        (34, 1210),
        "• масштаб корпуса по фазам: "
        f"{float(scale_stability['max_upper_body_area_ratio']):.3f}; "
        "разброс высоты: "
        f"{int(scale_stability['max_height_span_hd4'])} HD4 px.",
        font=font(20),
        fill=(205, 210, 216, 255),
    )
    draw.text(
        (34, 1260),
        "Предпросмотр: в игровые пакеты пока не установлен.",
        font=font(22, True),
        fill=(235, 176, 76, 255),
    )
    return board


def build_animation(atlas: Image.Image) -> None:
    frames: list[Image.Image] = []
    for row in range(ROWS):
        canvas = Image.new("RGBA", (1280, 260), (16, 20, 26, 255))
        draw = ImageDraw.Draw(canvas)
        for column, direction in enumerate(DIRECTIONS):
            sprite = atlas_frame(atlas, column, row).resize(
                (144, 144),
                Image.Resampling.LANCZOS,
            )
            x = 18 + column * 156
            canvas.alpha_composite(sprite, (x, 30))
            draw.text(
                (x + 58, 190),
                direction,
                font=font(17, True),
                fill=(230, 216, 184, 255),
            )
        frames.append(
            canvas.convert("P", palette=Image.Palette.ADAPTIVE)
        )
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=145,
        loop=0,
        disposal=2,
    )


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.open(SOURCE).convert("RGBA")
    classic = Image.open(CLASSIC).convert("RGBA")
    colored = build_colored_atlas(sheet, classic)
    neutral, mask = build_neutral_and_mask(colored)
    manifest = validate(colored, neutral, mask)
    if manifest["failures"]:
        raise AssertionError("\n".join(manifest["failures"]))

    colored.save(OUTPUT / "UNIT_SABOTEUR_RED_REFERENCE_HD4.png")
    neutral.save(BASE_OUT)
    mask.save(MASK_OUT)
    ordos = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    build_review(colored, neutral, mask, manifest).save(REVIEW_OUT)
    build_animation(ordos)
    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
