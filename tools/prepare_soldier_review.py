#!/usr/bin/env python3
"""Build an approval and integration-ready HD4 UNIT_SOLDIER atlas."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

from prepare_soldiers_review import (
    ATLAS,
    DIRECTIONS,
    FRAME,
    HOUSE_COLORS,
    SOURCE_COLUMN,
    apply_engine_tint,
    build_neutral_and_mask,
    frame,
    source_cell_with_anchor,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "soldier_review_v1"
SOURCE = (
    ROOT
    / "artifacts"
    / "soldiers_review_v1"
    / "soldier_pose_sheet_alpha.png"
)
CLASSIC = (
    ROOT
    / "artifacts"
    / "soldiers_review_v1"
    / "0155_UNIT_SOLDIER_CLASSIC.png"
)
GROUP = (
    ROOT
    / "artifacts"
    / "soldiers_review_v1"
    / "UNIT_SOLDIERS_ORDOS_HD4_PREVIEW.png"
)
HARVESTER = (
    ROOT
    / "artifacts"
    / "harvester_faction_preview_v1"
    / "variants"
    / "UNIT_HARVESTER_ORDOS_HD4_PREVIEW.png"
)

TARGET_HEIGHT = 44
BASE_OUT = OUTPUT / "UNIT_SOLDIER_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SOLDIER_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SOLDIER_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SOLDIER_ANIMATION_PREVIEW.gif"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def build_colored_soldier(
    sheet: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS)
    anchors: list[tuple[float, int]] = []
    for column in range(len(DIRECTIONS)):
        centers = []
        baselines = []
        for row in range(4):
            classic_frame = classic.crop(
                (
                    column * 32,
                    row * 32,
                    (column + 1) * 32,
                    (row + 1) * 32,
                )
            )
            classic_box = classic_frame.getchannel("A").getbbox()
            if classic_box is None:
                raise AssertionError(f"empty classic frame {column},{row}")
            centers.append((classic_box[0] + classic_box[2]) * 2)
            baselines.append(classic_box[3] * 4)
        anchors.append(
            (
                float(np.median(np.asarray(centers))),
                max(baselines),
            )
        )

    for row in range(4):
        for column, direction in enumerate(DIRECTIONS):
            source_column, mirror = SOURCE_COLUMN[direction]
            soldier, soldier_anchor_x = source_cell_with_anchor(
                sheet,
                source_column,
                row,
                mirror,
                TARGET_HEIGHT,
            )
            anchor_x, anchor_y = anchors[column]
            output_frame = Image.new("RGBA", FRAME)
            output_frame.alpha_composite(
                soldier,
                (
                    round(anchor_x - soldier_anchor_x),
                    anchor_y - soldier.height,
                ),
            )
            atlas.alpha_composite(
                output_frame,
                (column * FRAME[0], row * FRAME[1]),
            )
    return atlas


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
        (x, y, x + size, y + size + 38),
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
        (x + 8, y + size + 7),
        label,
        font=font(17, True),
        fill=(231, 214, 177, 255),
    )


def build_review(neutral: Image.Image, mask: Image.Image) -> Image.Image:
    green = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    red = apply_engine_tint(neutral, mask, HOUSE_COLORS["Харконнены"])
    blue = apply_engine_tint(neutral, mask, HOUSE_COLORS["Атрейдесы"])
    board = Image.new("RGBA", (1780, 1300), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Одиночный солдат — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "Опорные точки и 32 кадра повторяют оригинальный UNIT_SOLDIER",
        font=font(19),
        fill=(187, 193, 201, 255),
    )
    for column, direction in enumerate(DIRECTIONS):
        draw_card(
            board,
            frame(green, column),
            34 + column * 216,
            110,
            190,
            direction,
        )

    draw.text(
        (34, 360),
        "Четыре фазы движения — направление SE",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for row in range(4):
        draw_card(
            board,
            frame(green, 7, row),
            34 + row * 260,
            405,
            230,
            f"фаза {row}",
        )

    draw.text(
        (1100, 360),
        "Цвет фракции",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    draw_card(board, frame(red, 7), 1100, 405, 190, "Харконнены")
    draw_card(board, frame(blue, 7), 1315, 405, 190, "Атрейдесы")
    draw_card(board, frame(green, 7), 1530, 405, 190, "Ордос")

    draw.text(
        (34, 715),
        "Реальный игровой масштаб",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    panel = Image.new("RGBA", (1500, 360), (22, 26, 31, 255))
    panel_draw = ImageDraw.Draw(panel)
    for y in range(0, 360, 32):
        for x in range(0, 1500, 32):
            shade = 40 if (x // 32 + y // 32) % 2 else 32
            panel_draw.rectangle(
                (x, y, x + 31, y + 31),
                fill=(shade, shade, shade, 255),
            )
    panel.alpha_composite(frame(green, 7), (90, 140))
    if GROUP.is_file():
        group = Image.open(GROUP).convert("RGBA")
        panel.alpha_composite(frame(group, 7), (350, 140))
    if HARVESTER.is_file():
        harvester_atlas = Image.open(HARVESTER).convert("RGBA")
        panel.alpha_composite(
            harvester_atlas.crop((6 * 320, 0, 7 * 320, 208)),
            (760, 100),
        )
    board.alpha_composite(panel, (34, 760))
    draw.text(
        (55, 1085),
        f"Одиночный: {TARGET_HEIGHT // 4} px",
        font=font(18, True),
        fill=(220, 210, 185, 255),
    )
    draw.text(
        (350, 1085),
        "Отряд: бойцы по 12 px",
        font=font(18, True),
        fill=(220, 210, 185, 255),
    )
    draw.text(
        (800, 1085),
        "Харвестер: кадр 80×52 px",
        font=font(18, True),
        fill=(220, 210, 185, 255),
    )
    draw.text(
        (34, 1190),
        "Предварительный просмотр собран из утверждённого ImageGen-листа; новых свободных поз не добавлено.",
        font=font(20),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(green: Image.Image) -> None:
    frames = []
    for row in range(4):
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            frame(green, 7, row).resize(
                (512, 512),
                Image.Resampling.LANCZOS,
            )
        )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=160,
        loop=0,
        disposal=2,
    )


def validate(
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("colored", colored),
        ("neutral", neutral),
        ("mask", mask),
    ):
        if image.size != ATLAS:
            raise AssertionError(f"{name} atlas has size {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} atlas is empty")
    if ImageChops.difference(
        colored.getchannel("A"),
        neutral.getchannel("A"),
    ).getbbox():
        raise AssertionError("neutralization changed alpha")

    unique_frames = set()
    for row in range(4):
        for column in range(8):
            output_frame = frame(neutral, column, row)
            box = output_frame.getchannel("A").getbbox()
            if box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if box[0] < 2 or box[1] < 2 or box[2] > 126 or box[3] > 126:
                raise AssertionError(
                    f"frame {column},{row} touches boundary: {box}"
                )
            unique_frames.add(output_frame.tobytes())
    if len(unique_frames) != 32:
        raise AssertionError("UNIT_SOLDIER frames are not unique")
    return {
        "resource": "UNIT_SOLDIER",
        "resource_id": 155,
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "columns": list(DIRECTIONS),
        "animation_rows": 4,
        "individual_height_logical": TARGET_HEIGHT // 4,
        "nonempty_unique_frames": len(unique_frames),
        "mask_pixels": int(
            np.count_nonzero(np.asarray(mask.getchannel("A")) > 8)
        ),
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.open(SOURCE).convert("RGBA")
    classic = Image.open(CLASSIC).convert("RGBA")
    colored = build_colored_soldier(sheet, classic)
    neutral, mask = build_neutral_and_mask(colored)
    validation = validate(colored, neutral, mask)
    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    neutral.resize((512, 256), Image.Resampling.LANCZOS).save(
        OUTPUT / "UNIT_SOLDIER_HD2_PREVIEW.png",
        optimize=True,
    )
    green = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    green.save(OUTPUT / "UNIT_SOLDIER_ORDOS_HD4_PREVIEW.png", optimize=True)
    build_review(neutral, mask).save(REVIEW_OUT, optimize=True)
    build_animation(green)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source": str(SOURCE),
        "classic_contract": str(CLASSIC),
        "anchor_method": (
            "stable per-direction classic baseline plus armor-centroid "
            "alignment across all four walking phases"
        ),
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
