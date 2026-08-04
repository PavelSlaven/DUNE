#!/usr/bin/env python3
"""Build an approval-ready HD4 UNIT_SOLDIERS atlas from the pose sheet."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "soldiers_review_v1"
SOURCE = OUTPUT / "soldier_pose_sheet_alpha.png"
CLASSIC = OUTPUT / "0156_UNIT_SOLDIERS_CLASSIC.png"
HARVESTER = (
    ROOT
    / "artifacts"
    / "harvester_faction_preview_v1"
    / "variants"
    / "UNIT_HARVESTER_ORDOS_HD4_PREVIEW.png"
)

FRAME = (128, 128)
ATLAS = (1024, 512)
SOURCE_FRAME = (192, 256)
ROWS = 4
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
TARGET_HEIGHT = 48

BASE_OUT = OUTPUT / "UNIT_SOLDIERS_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SOLDIERS_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "UNIT_SOLDIERS_SHADOW_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SOLDIERS_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SOLDIERS_ANIMATION_PREVIEW.gif"

# Use the cleanest generated poses, then mirror only opposite pairs.  This
# makes the direction contract deterministic instead of trusting generated
# near-duplicate diagonals.
SOURCE_COLUMN = {
    "E": (0, False),
    "NE": (3, False),
    "N": (2, False),
    "NW": (3, True),
    "W": (0, True),
    "SW": (5, True),
    "S": (6, False),
    "SE": (5, False),
}

# Foot anchors of the three-person triangular formation.  The first point is
# the leader in the direction of travel; members are drawn in screen-depth
# order so their silhouettes do not incorrectly overlap.
FORMATION = {
    "E": ((86, 65), (55, 48), (55, 83)),
    "NE": ((82, 49), (48, 55), (70, 86)),
    "N": ((64, 43), (43, 79), (85, 79)),
    "NW": ((46, 49), (80, 55), (58, 86)),
    "W": ((42, 65), (73, 48), (73, 83)),
    "SW": ((46, 84), (80, 76), (58, 47)),
    "S": ((64, 87), (43, 53), (85, 53)),
    "SE": ((82, 84), (48, 76), (70, 47)),
}

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def source_cell(
    sheet: Image.Image,
    column: int,
    row: int,
    mirror: bool,
    target_height: int = TARGET_HEIGHT,
) -> Image.Image:
    return source_cell_with_anchor(
        sheet,
        column,
        row,
        mirror,
        target_height,
    )[0]


def source_cell_with_anchor(
    sheet: Image.Image,
    column: int,
    row: int,
    mirror: bool,
    target_height: int = TARGET_HEIGHT,
) -> tuple[Image.Image, float]:
    cell = sheet.crop(
        (
            column * SOURCE_FRAME[0],
            row * SOURCE_FRAME[1],
            (column + 1) * SOURCE_FRAME[0],
            (row + 1) * SOURCE_FRAME[1],
        )
    )
    alpha_box = cell.getchannel("A").getbbox()
    if alpha_box is None:
        raise AssertionError(f"empty source cell {column},{row}")
    cell = cell.crop(alpha_box)
    if mirror:
        cell = cell.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    scale = target_height / cell.height
    width = max(1, round(cell.width * scale))
    cell = cell.resize((width, target_height), Image.Resampling.LANCZOS)

    rgba = np.asarray(cell, dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    armor = np.clip(
        (green - np.maximum(red, blue) - 4.0) / 80.0,
        0.0,
        1.0,
    )
    weights = armor * (alpha / 255.0)
    if float(weights.sum()) < 1.0:
        weights = alpha / 255.0
    _, x_grid = np.indices(weights.shape)
    anchor_x = float((x_grid * weights).sum() / weights.sum())
    return cell, anchor_x


def build_colored_squad(sheet: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS)
    for row in range(ROWS):
        for column, direction in enumerate(DIRECTIONS):
            source_column, mirror = SOURCE_COLUMN[direction]
            members = [
                source_cell_with_anchor(
                    sheet,
                    source_column,
                    (row + phase_offset) % ROWS,
                    mirror,
                )
                for phase_offset in (0, 1, 3)
            ]
            frame = Image.new("RGBA", FRAME)
            placements = sorted(
                zip(FORMATION[direction], members, strict=True),
                key=lambda item: item[0][1],
            )
            for (anchor_x, anchor_y), member in placements:
                member_image, member_anchor_x = member
                anchor_y += 8
                frame.alpha_composite(
                    member_image,
                    (
                        round(anchor_x - member_anchor_x),
                        anchor_y - member_image.height,
                    ),
                )
            atlas.alpha_composite(
                frame,
                (column * FRAME[0], row * FRAME[1]),
            )
    return atlas


def green_selection(image: Image.Image) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    dominance = green - np.maximum(red, blue)
    saturation = (
        np.max(rgba[:, :, :3], axis=2)
        - np.min(rgba[:, :, :3], axis=2)
    )
    selection = np.clip((dominance - 10.0) / 75.0, 0.0, 1.0)
    selection *= np.clip((saturation - 16.0) / 90.0, 0.0, 1.0)
    selection *= alpha / 255.0
    return selection


def build_neutral_and_mask(
    colored: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(colored.convert("RGBA"), dtype=np.float32)
    selection = green_selection(colored)
    blend = selection[:, :, None] * 0.90
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    )
    neutral_rgb = np.stack(
        (
            np.clip(luminance * 0.92 + 10, 0, 255),
            np.clip(luminance * 0.96 + 12, 0, 255),
            np.clip(luminance * 1.02 + 15, 0, 255),
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
    mask.putalpha(Image.fromarray(mask_alpha, "L").filter(
        ImageFilter.GaussianBlur(0.45)
    ))
    return neutral, mask


def apply_engine_tint(
    image: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32).copy()
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    strength = (
        mask_rgba[:, :, 3] / 255.0
        * np.max(mask_rgba[:, :, :3], axis=2) / 255.0
    )
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        colored = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - strength)
            + colored * strength
        )
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def build_shadow(atlas: Image.Image) -> Image.Image:
    shadow = Image.new("RGBA", ATLAS)
    for row in range(ROWS):
        for column in range(8):
            frame = atlas.crop(
                (
                    column * FRAME[0],
                    row * FRAME[1],
                    (column + 1) * FRAME[0],
                    (row + 1) * FRAME[1],
                )
            )
            alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(1.4))
            alpha = alpha.point(lambda value: round(value * 0.18))
            silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
            silhouette.putalpha(alpha)
            shadow.alpha_composite(
                silhouette,
                (column * FRAME[0] + 3, row * FRAME[1] + 3),
            )
    return shadow


def frame(atlas: Image.Image, column: int, row: int = 0) -> Image.Image:
    return atlas.crop(
        (
            column * FRAME[0],
            row * FRAME[1],
            (column + 1) * FRAME[0],
            (row + 1) * FRAME[1],
        )
    )


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


def build_review(
    neutral: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    green = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    red = apply_engine_tint(neutral, mask, HOUSE_COLORS["Харконнены"])
    blue = apply_engine_tint(neutral, mask, HOUSE_COLORS["Атрейдесы"])
    board = Image.new("RGBA", (1780, 1390), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Отряд солдат — HD4, три бойца",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "32 кадра: E, NE, N, NW, W, SW, S, SE × 4 фазы",
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
        "Четыре фазы движения — направление S",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for row in range(ROWS):
        draw_card(
            board,
            frame(green, 6, row),
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
        "Реальный масштаб относительно харвестера",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    scale_panel = Image.new("RGBA", (1000, 380), (22, 26, 31, 255))
    checker = ImageDraw.Draw(scale_panel)
    for y in range(0, 380, 32):
        for x in range(0, 1000, 32):
            shade = 40 if (x // 32 + y // 32) % 2 else 32
            checker.rectangle((x, y, x + 31, y + 31), fill=(shade,) * 3 + (255,))
    squad = frame(green, 7)
    scale_panel.alpha_composite(squad, (85, 145))
    if HARVESTER.is_file():
        harvester_atlas = Image.open(HARVESTER).convert("RGBA")
        harvester = harvester_atlas.crop((6 * 320, 0, 7 * 320, 208))
        scale_panel.alpha_composite(harvester, (410, 100))
    board.alpha_composite(scale_panel, (34, 760))
    draw.text(
        (52, 1110),
        "Отряд: кадр 32×32 логических px",
        font=font(18, True),
        fill=(220, 210, 185, 255),
    )
    draw.text(
        (445, 1110),
        "Харвестер: кадр 80×52 логических px",
        font=font(18, True),
        fill=(220, 210, 185, 255),
    )

    draw.text(
        (1080, 715),
        "Маска и исходный контракт",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    draw_card(board, frame(mask, 7), 1080, 760, 250, "белое = цвет Дома")
    if CLASSIC.is_file():
        classic = Image.open(CLASSIC).convert("RGBA").crop((7 * 32, 0, 8 * 32, 32))
        draw_card(board, classic, 1360, 760, 250, "оригинал: SE")

    draw.text(
        (34, 1215),
        "Размер бойца: 12 логических px; ноги выровнены, формация вращается вместе с направлением.",
        font=font(20),
        fill=(188, 194, 202, 255),
    )
    draw.text(
        (34, 1260),
        "Без установки в игру — предварительный просмотр для утверждения.",
        font=font(20),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(green: Image.Image) -> None:
    frames: list[Image.Image] = []
    for row in range(ROWS):
        sprite = frame(green, 7, row)
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            sprite.resize((512, 512), Image.Resampling.LANCZOS)
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
    shadow: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("colored", colored),
        ("neutral", neutral),
        ("mask", mask),
        ("shadow", shadow),
    ):
        if image.size != ATLAS:
            raise AssertionError(f"{name} atlas size changed: {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} atlas is empty")
    if not ImageChops.difference(
        colored.getchannel("A"),
        neutral.getchannel("A"),
    ).getbbox() is None:
        raise AssertionError("neutralization changed sprite alpha")

    frame_boxes = []
    for row in range(ROWS):
        for column in range(8):
            box = frame(neutral, column, row).getchannel("A").getbbox()
            if box is None:
                raise AssertionError(f"empty output frame {column},{row}")
            if box[0] < 2 or box[1] < 2 or box[2] > 126 or box[3] > 126:
                raise AssertionError(
                    f"frame {column},{row} touches its boundary: {box}"
                )
            frame_boxes.append(box)
    mask_pixels = int(
        np.count_nonzero(np.asarray(mask.getchannel("A")) > 8)
    )
    return {
        "resource": "UNIT_SOLDIERS",
        "resource_id": 156,
        "shadow_id": 157,
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "columns": list(DIRECTIONS),
        "animation_rows": ROWS,
        "members_per_frame": 3,
        "individual_height_logical": TARGET_HEIGHT // 4,
        "mask_pixels": mask_pixels,
        "nonempty_frames": len(frame_boxes),
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.open(SOURCE).convert("RGBA")
    if sheet.size != (1536, 1024):
        raise AssertionError(f"unexpected generated sheet size: {sheet.size}")
    colored = build_colored_squad(sheet)
    neutral, mask = build_neutral_and_mask(colored)
    shadow = build_shadow(neutral)
    validation = validate(colored, neutral, mask, shadow)

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    green = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    green.save(OUTPUT / "UNIT_SOLDIERS_ORDOS_HD4_PREVIEW.png", optimize=True)
    apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Харконнены"],
    ).save(OUTPUT / "UNIT_SOLDIERS_HARKONNEN_HD4_PREVIEW.png", optimize=True)
    apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Атрейдесы"],
    ).save(OUTPUT / "UNIT_SOLDIERS_ATREIDES_HD4_PREVIEW.png", optimize=True)
    neutral.resize((512, 256), Image.Resampling.LANCZOS).save(
        OUTPUT / "UNIT_SOLDIERS_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(neutral, mask).save(REVIEW_OUT, optimize=True)
    build_animation(green)

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "generated_pose_sheet": str(SOURCE),
        "classic_contract": str(CLASSIC),
        "direction_method": (
            "accepted E/NE/N/SE sources plus deterministic mirrored "
            "opposites; original D2TM column order; every member aligned "
            "by armor centroid and foot baseline"
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
