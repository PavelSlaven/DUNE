#!/usr/bin/env python3
"""Reorder the supplied soldier sheet into the D2TM UNIT_SOLDIER contract."""

from __future__ import annotations

import json
import shutil
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from prepare_soldiers_review import apply_engine_tint


ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(
    "C:/Users/Slaven/AppData/Local/Temp/"
    "codex-clipboard-bd77fb1c-5b51-4e65-bd29-b7c0f929e2f2.png"
)
OUTPUT = ROOT / "artifacts" / "soldier_review_v2"
SOURCE_COPY = OUTPUT / "source_reference.png"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0155_UNIT_SOLDIER.png"
)

SOURCE_GRID = (8, 4)
FRAME = (128, 128)
ATLAS = (1024, 512)
TARGET_HEIGHT = 44
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROW_LABELS = ("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")
TARGET_TO_SOURCE_ROW = (1, 2, 3, 0)
# The supplied north-facing source cell in row 0 actually faces south.
# Reuse the neutral north phase in the fourth slot so the engine's
# 0->1->2->3 walk cycle keeps the weapon in the same hand and reads as
# stride A -> neutral -> stride B -> neutral.
NORTH_SOURCE_ROWS = (1, 2, 3, 2)
WEAPON_CANONICAL_ROWS = {
    "N": 1,
}
HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}

BASE_OUT = OUTPUT / "UNIT_SOLDIER_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SOLDIER_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "UNIT_SOLDIER_HD2_PREVIEW.png"
RED_OUT = OUTPUT / "UNIT_SOLDIER_HARKONNEN_HD4_PREVIEW.png"
BLUE_OUT = OUTPUT / "UNIT_SOLDIER_ATREIDES_HD4_PREVIEW.png"
GREEN_OUT = OUTPUT / "UNIT_SOLDIER_ORDOS_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SOLDIER_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SOLDIER_ANIMATION_PREVIEW.gif"
ALL_ANIMATION_OUT = (
    OUTPUT / "UNIT_SOLDIER_ALL_DIRECTIONS_ANIMATION_PREVIEW.gif"
)
HAND_CHECK_OUT = OUTPUT / "UNIT_SOLDIER_NORTH_HAND_CHECK.png"
ALL_HANDS_CHECK_OUT = OUTPUT / "UNIT_SOLDIER_ALL_HANDS_CHECK.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def frame(
    atlas: Image.Image,
    column: int,
    row: int,
) -> Image.Image:
    return atlas.crop(
        (
            column * FRAME[0],
            row * FRAME[1],
            (column + 1) * FRAME[0],
            (row + 1) * FRAME[1],
        )
    )


def exterior_background_mask(rgb: np.ndarray) -> np.ndarray:
    """Return black background connected to a cell border."""
    height, width, _ = rgb.shape
    eligible = np.max(rgb, axis=2) <= 30
    exterior = np.zeros((height, width), dtype=np.uint8)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        for y in (0, height - 1):
            if eligible[y, x] and not exterior[y, x]:
                exterior[y, x] = 1
                queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if eligible[y, x] and not exterior[y, x]:
                exterior[y, x] = 1
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        for next_x, next_y in (
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ):
            if (
                0 <= next_x < width
                and 0 <= next_y < height
                and eligible[next_y, next_x]
                and not exterior[next_y, next_x]
            ):
                exterior[next_y, next_x] = 1
                queue.append((next_x, next_y))
    return exterior.astype(bool)


def remove_connected_black(cell: Image.Image) -> Image.Image:
    rgba = np.asarray(cell.convert("RGBA"), dtype=np.uint8).copy()
    rgb = rgba[:, :, :3]
    exterior = exterior_background_mask(rgb)
    brightest = np.max(rgb, axis=2).astype(np.float32)
    soft_alpha = np.clip((brightest - 1.0) * (255.0 / 29.0), 0, 255)
    alpha = np.full(exterior.shape, 255.0, dtype=np.float32)
    alpha[exterior] = soft_alpha[exterior]
    rgba[:, :, 3] = alpha.astype(np.uint8)

    subject = Image.fromarray(rgba, "RGBA")
    box = subject.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("source cell has no visible soldier")
    return subject.crop(box)


def foot_anchor_x(subject: Image.Image) -> float:
    alpha = np.asarray(subject.getchannel("A"), dtype=np.float32) / 255.0
    height, _ = alpha.shape
    start = max(0, round(height * 0.72))
    weights = alpha.copy()
    weights[:start, :] = 0
    if float(weights.sum()) < 1.0:
        weights = alpha
    _, x_grid = np.indices(weights.shape)
    return float((weights * x_grid).sum() / weights.sum())


def fitted_source_cell(
    source: Image.Image,
    column: int,
    source_row: int,
) -> tuple[Image.Image, float]:
    left = round(column * source.width / SOURCE_GRID[0])
    right = round((column + 1) * source.width / SOURCE_GRID[0])
    top = round(source_row * source.height / SOURCE_GRID[1])
    bottom = round((source_row + 1) * source.height / SOURCE_GRID[1])
    cell = source.crop(
        (
            left,
            top,
            right,
            bottom,
        )
    )
    subject = remove_connected_black(cell)
    scale = TARGET_HEIGHT / subject.height
    width = max(1, round(subject.width * scale))
    subject = subject.resize(
        (width, TARGET_HEIGHT),
        Image.Resampling.LANCZOS,
    )
    return subject, foot_anchor_x(subject)


def classic_anchors(classic: Image.Image) -> list[tuple[float, int]]:
    anchors: list[tuple[float, int]] = []
    for column in range(8):
        centers = []
        baselines = []
        for row in range(4):
            old = classic.crop(
                (
                    column * 32,
                    row * 32,
                    (column + 1) * 32,
                    (row + 1) * 32,
                )
            )
            box = old.getchannel("A").getbbox()
            if box is None:
                raise AssertionError(f"empty classic frame {column},{row}")
            centers.append((box[0] + box[2]) * 2)
            baselines.append(box[3] * 4)
        anchors.append((float(np.median(centers)), max(baselines)))
    return anchors


def build_colored_atlas(
    source: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS)
    anchors = classic_anchors(classic)
    for target_row, default_source_row in enumerate(TARGET_TO_SOURCE_ROW):
        for column in range(8):
            source_row = (
                NORTH_SOURCE_ROWS[target_row]
                if DIRECTIONS[column] == "N"
                else default_source_row
            )
            subject, source_anchor_x = fitted_source_cell(
                source,
                column,
                source_row,
            )
            target_anchor_x, target_anchor_y = anchors[column]
            output = Image.new("RGBA", FRAME)
            output.alpha_composite(
                subject,
                (
                    round(target_anchor_x - source_anchor_x),
                    target_anchor_y - subject.height,
                ),
            )
            atlas.alpha_composite(
                output,
                (column * FRAME[0], target_row * FRAME[1]),
            )
    atlas = add_missing_north_pistol(atlas, anchors)
    return stabilize_weapon_arms(atlas, anchors)


def add_missing_north_pistol(
    atlas: Image.Image,
    anchors: list[tuple[float, int]],
) -> Image.Image:
    """Restore the pistol omitted by the supplied north-facing reference."""
    column = DIRECTIONS.index("N")
    row = WEAPON_CANONICAL_ROWS["N"]
    output = atlas.copy()
    north = frame(output, column, row)
    box = north.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("north canonical frame is empty")
    draw = ImageDraw.Draw(north)
    hand_x = round(anchors[column][0] + 10)
    hand_y = box[1] + round((box[3] - box[1]) * 0.43)
    draw.line(
        (hand_x - 2, hand_y + 2, hand_x + 2, hand_y + 4),
        fill=(30, 34, 42, 255),
        width=3,
    )
    draw.polygon(
        (
            (hand_x, hand_y),
            (hand_x + 6, hand_y + 2),
            (hand_x + 6, hand_y + 3),
            (hand_x - 1, hand_y + 2),
        ),
        fill=(46, 55, 68, 255),
    )
    draw.line(
        (hand_x + 1, hand_y, hand_x + 5, hand_y + 2),
        fill=(108, 121, 136, 255),
        width=1,
    )
    draw.line(
        (hand_x + 1, hand_y + 2, hand_x, hand_y + 6),
        fill=(28, 31, 38, 255),
        width=2,
    )
    output.paste(
        north,
        (column * FRAME[0], row * FRAME[1]),
    )
    return output


def weapon_arm_blend_mask(
    canonical: Image.Image,
    anchor_x: float,
    direction: str,
) -> Image.Image:
    box = canonical.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("canonical soldier frame is empty")
    height = box[3] - box[1]
    vertical_solid_end = box[1] + round(height * 0.48)
    vertical_feather_end = box[1] + round(height * 0.66)

    # The anatomical right hand appears on different screen sides when
    # viewed from the front and from behind.
    weapon_on_right = direction in ("E", "NE", "N", "SE")
    x_grid, y_grid = np.meshgrid(
        np.arange(FRAME[0], dtype=np.float32),
        np.arange(FRAME[1], dtype=np.float32),
    )
    horizontal_feather = 7.0
    if weapon_on_right:
        horizontal = np.clip(
            (x_grid - (anchor_x - horizontal_feather))
            / horizontal_feather,
            0.0,
            1.0,
        )
    else:
        horizontal = np.clip(
            ((anchor_x + horizontal_feather) - x_grid)
            / horizontal_feather,
            0.0,
            1.0,
        )
    vertical = np.ones_like(y_grid, dtype=np.float32)
    vertical[y_grid > vertical_solid_end] = np.clip(
        (
            vertical_feather_end
            - y_grid[y_grid > vertical_solid_end]
        )
        / max(1, vertical_feather_end - vertical_solid_end),
        0.0,
        1.0,
    )
    vertical[y_grid > vertical_feather_end] = 0.0
    mask = np.clip(horizontal * vertical * 255.0, 0, 255)
    return Image.fromarray(mask.astype(np.uint8), "L")


def stabilize_weapon_arms(
    atlas: Image.Image,
    anchors: list[tuple[float, int]],
) -> Image.Image:
    """Keep the armed forearm while preserving each full-body gait phase."""
    result = Image.new("RGBA", ATLAS)
    for column, direction in enumerate(DIRECTIONS):
        canonical_row = WEAPON_CANONICAL_ROWS.get(direction, 0)
        canonical = frame(atlas, column, canonical_row)
        mask = weapon_arm_blend_mask(
            canonical,
            anchors[column][0],
            direction,
        )
        for row in range(4):
            current = frame(atlas, column, row)
            stabilized = (
                canonical
                if row == canonical_row
                else Image.composite(canonical, current, mask)
            )
            result.alpha_composite(
                stabilized,
                (column * FRAME[0], row * FRAME[1]),
            )
    return result


def red_selection(image: Image.Image) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (
        rgba[:, :, channel] for channel in range(4)
    )
    dominance = red - np.maximum(green, blue)
    saturation = (
        np.max(rgba[:, :, :3], axis=2)
        - np.min(rgba[:, :, :3], axis=2)
    )
    selection = np.clip((dominance - 12.0) / 88.0, 0.0, 1.0)
    selection *= np.clip((saturation - 18.0) / 100.0, 0.0, 1.0)
    selection *= alpha / 255.0
    return selection


def build_neutral_and_mask(
    colored: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(colored.convert("RGBA"), dtype=np.float32)
    selection = red_selection(colored)
    blend = selection[:, :, None] * 0.92
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    )
    neutral_rgb = np.stack(
        (
            np.clip(luminance * 0.94 + 10, 0, 255),
            np.clip(luminance * 0.98 + 12, 0, 255),
            np.clip(luminance * 1.04 + 14, 0, 255),
        ),
        axis=2,
    )
    output = rgba.copy()
    output[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - blend)
        + neutral_rgb * blend
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


def downscale_atlas(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", (512, 256))
    for row in range(4):
        for column in range(8):
            reduced = frame(atlas, column, row).resize(
                (64, 64),
                Image.Resampling.LANCZOS,
            )
            result.alpha_composite(reduced, (column * 64, row * 64))
    return result


def draw_frame_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    label: str,
) -> None:
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle(
        (x, y, x + 156, y + 182),
        radius=7,
        fill=(22, 26, 31, 255),
        outline=(138, 105, 48, 255),
        width=2,
    )
    board.alpha_composite(
        sprite.resize((156, 156), Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.text(
        (x + 8, y + 157),
        label,
        font=font(15, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    neutral: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    red = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Харконнены"],
    )
    blue = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Атрейдесы"],
    )
    green = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Ордос"],
    )
    board = Image.new("RGBA", (1460, 1130), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Одиночный солдат — правильный атлас 8×4",
        font=font(32, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 67),
        "Строки нового эталона переставлены: 1, 2, 3, 0",
        font=font(18),
        fill=(187, 193, 201, 255),
    )

    for row, row_name in enumerate(ROW_LABELS):
        draw.text(
            (10, 130 + row * 205),
            row_name,
            font=font(13, True),
            fill=(225, 188, 98, 255),
        )
        for column, direction in enumerate(DIRECTIONS):
            draw_frame_card(
                board,
                frame(red, column, row),
                85 + column * 170,
                105 + row * 205,
                direction,
            )

    draw.text(
        (34, 940),
        "Проверка маски фракции",
        font=font(23, True),
        fill=(225, 188, 98, 255),
    )
    for index, (name, atlas) in enumerate(
        (
            ("Харконнены", red),
            ("Атрейдесы", blue),
            ("Ордос", green),
        )
    ):
        draw_frame_card(
            board,
            frame(atlas, 7, 1),
            330 + index * 250,
            900,
            name,
        )
    return board


def build_animation(colored: Image.Image) -> None:
    phases = (0, 1, 2, 3)
    frames = []
    for row in phases:
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            frame(colored, 0, row).resize(
                (512, 512),
                Image.Resampling.LANCZOS,
            )
        )
        frames.append(
            shown.convert("P", palette=Image.Palette.ADAPTIVE)
        )
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=150,
        loop=0,
        disposal=2,
    )


def build_all_directions_animation(colored: Image.Image) -> None:
    animation_frames = []
    for row in range(4):
        shown = Image.new("RGBA", (1024, 512), (16, 20, 26, 255))
        draw = ImageDraw.Draw(shown)
        for column, direction in enumerate(DIRECTIONS):
            x = (column % 4) * 256
            y = (column // 4) * 256
            shown.alpha_composite(
                frame(colored, column, row).resize(
                    (256, 256),
                    Image.Resampling.LANCZOS,
                ),
                (x, y),
            )
            draw.text(
                (x + 12, y + 10),
                direction,
                font=font(18, True),
                fill=(225, 188, 98, 255),
            )
        animation_frames.append(
            shown.convert("P", palette=Image.Palette.ADAPTIVE)
        )
    animation_frames[0].save(
        ALL_ANIMATION_OUT,
        save_all=True,
        append_images=animation_frames[1:],
        duration=180,
        loop=0,
        disposal=2,
    )


def build_north_hand_check(colored: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1040, 330), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (24, 18),
        "Север: оружие остаётся в правой руке",
        font=font(27, True),
        fill=(236, 219, 182, 255),
    )
    for row in range(4):
        sprite = frame(colored, 2, row)
        box = sprite.getchannel("A").point(
            lambda value: 255 if value > 8 else 0
        ).getbbox()
        if box is None:
            raise AssertionError(f"empty north frame {row}")
        padding = 8
        crop = sprite.crop(
            (
                max(0, box[0] - padding),
                max(0, box[1] - padding),
                min(FRAME[0], box[2] + padding),
                min(FRAME[1], box[3] + padding),
            )
        )
        shown = crop.resize((220, 220), Image.Resampling.LANCZOS)
        x = 20 + row * 255
        board.alpha_composite(shown, (x, 72))
        draw.text(
            (x + 74, 294),
            str(row + 1),
            font=font(18, True),
            fill=(225, 188, 98, 255),
        )
    return board


def build_all_hands_check(colored: Image.Image) -> Image.Image:
    cell_size = 150
    board = Image.new(
        "RGBA",
        (80 + cell_size * 4, 60 + cell_size * 8),
        (9, 12, 16, 255),
    )
    draw = ImageDraw.Draw(board)
    draw.text(
        (16, 14),
        "Покадровая проверка вооружённой руки",
        font=font(23, True),
        fill=(236, 219, 182, 255),
    )
    for column, direction in enumerate(DIRECTIONS):
        y = 54 + column * cell_size
        draw.text(
            (12, y + 62),
            direction,
            font=font(17, True),
            fill=(225, 188, 98, 255),
        )
        for row in range(4):
            sprite = frame(colored, column, row)
            box = sprite.getchannel("A").point(
                lambda value: 255 if value > 8 else 0
            ).getbbox()
            if box is None:
                raise AssertionError(
                    f"empty hand-check frame {column},{row}"
                )
            padding = 6
            crop = sprite.crop(
                (
                    max(0, box[0] - padding),
                    max(0, box[1] - padding),
                    min(FRAME[0], box[2] + padding),
                    min(FRAME[1], box[3] + padding),
                )
            )
            shown = crop.resize(
                (cell_size, cell_size),
                Image.Resampling.LANCZOS,
            )
            board.alpha_composite(
                shown,
                (70 + row * cell_size, y),
            )
    return board


def validate(
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    for name, atlas in (
        ("colored", colored),
        ("neutral", neutral),
        ("mask", mask),
    ):
        if atlas.size != ATLAS:
            raise AssertionError(f"{name} atlas has size {atlas.size}")
    if ImageChops.difference(
        colored.getchannel("A"),
        neutral.getchannel("A"),
    ).getbbox():
        raise AssertionError("neutralization changed alpha")

    bounds = []
    gait_centers: dict[str, list[list[float]]] = {}
    unique = set()
    for row in range(4):
        row_bounds = []
        for column in range(8):
            output = frame(neutral, column, row)
            box = output.getchannel("A").point(
                lambda value: 255 if value > 8 else 0
            ).getbbox()
            if box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if box[0] < 2 or box[1] < 2 or box[2] > 126 or box[3] > 126:
                raise AssertionError(
                    f"frame {column},{row} touches boundary: {box}"
                )
            row_bounds.append(box)
            unique.add(output.tobytes())
        bounds.append(row_bounds)
    if len(unique) != 32:
        raise AssertionError(f"expected 32 unique frames, got {len(unique)}")

    for column, direction in enumerate(DIRECTIONS):
        baselines = []
        centers = []
        for row in range(4):
            output = frame(neutral, column, row)
            box = bounds[row][column]
            baselines.append(box[3])
            alpha = np.asarray(
                output.getchannel("A"),
                dtype=np.float32,
            ) / 255.0
            lower_start = box[1] + round(
                (box[3] - box[1]) * 0.68
            )
            alpha[:lower_start, :] = 0
            weight = float(alpha.sum())
            if weight <= 0:
                raise AssertionError(
                    f"missing feet in {direction} phase {row}"
                )
            y_grid, x_grid = np.indices(alpha.shape)
            centers.append(
                [
                    round(float((x_grid * alpha).sum() / weight), 2),
                    round(float((y_grid * alpha).sum() / weight), 2),
                ]
            )
        if len(set(baselines)) != 1:
            raise AssertionError(
                f"walking baseline jumps in {direction}: {baselines}"
            )
        x_spread = max(item[0] for item in centers) - min(
            item[0] for item in centers
        )
        y_spread = max(item[1] for item in centers) - min(
            item[1] for item in centers
        )
        if x_spread > 5.0 or y_spread > 2.5:
            raise AssertionError(
                f"feet jump in {direction}: {centers}"
            )
        gait_centers[direction] = centers

    anchors = classic_anchors(
        Image.open(CLASSIC).convert("RGBA")
    )
    for column, direction in enumerate(DIRECTIONS):
        canonical_row = WEAPON_CANONICAL_ROWS.get(direction, 0)
        canonical = frame(colored, column, canonical_row)
        arm_mask = weapon_arm_blend_mask(
            canonical,
            anchors[column][0],
            direction,
        )
        solid_mask = arm_mask.point(
            lambda value: 255 if value == 255 else 0
        )
        canonical_arm = Image.new("RGBA", FRAME)
        canonical_arm.paste(canonical, mask=solid_mask)
        for row in range(4):
            if row == canonical_row:
                continue
            candidate_arm = Image.new("RGBA", FRAME)
            candidate_arm.paste(
                frame(colored, column, row),
                mask=solid_mask,
            )
            if ImageChops.difference(
                canonical_arm,
                candidate_arm,
            ).getbbox():
                raise AssertionError(
                    f"weapon arm changed in "
                    f"{direction} phase {row}"
                )
    return {
        "resource_id": 155,
        "resource": "UNIT_SOLDIER",
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "direction_order": list(DIRECTIONS),
        "target_rows": list(ROW_LABELS),
        "source_row_order": list(TARGET_TO_SOURCE_ROW),
        "north_source_row_order": list(NORTH_SOURCE_ROWS),
        "weapon_hand_rule": (
            "weapon remains in the soldier's right hand in all four phases"
        ),
        "weapon_hand_validation": (
            "direction-specific armed forearm is pixel-identical "
            "through all four gait phases"
        ),
        "target_height_hd4": TARGET_HEIGHT,
        "target_height_logical": TARGET_HEIGHT // 4,
        "unique_frames": len(unique),
        "frame_bounds": bounds,
        "gait_foot_centers_hd4": gait_centers,
        "mask_pixels": int(
            np.count_nonzero(np.asarray(mask.getchannel("A")) > 8)
        ),
    }


def main() -> None:
    if not INPUT.is_file():
        raise FileNotFoundError(INPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(INPUT, SOURCE_COPY)
    source = Image.open(SOURCE_COPY).convert("RGBA")
    expected_ratio = SOURCE_GRID[0] / SOURCE_GRID[1]
    actual_ratio = source.width / source.height
    if abs(actual_ratio - expected_ratio) > 0.01:
        raise AssertionError(
            f"unexpected source aspect ratio {source.size}"
        )
    classic = Image.open(CLASSIC).convert("RGBA")
    if classic.size != (256, 128):
        raise AssertionError(f"unexpected classic size {classic.size}")

    colored = build_colored_atlas(source, classic)
    neutral, mask = build_neutral_and_mask(colored)
    validation = validate(colored, neutral, mask)
    red = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Харконнены"],
    )
    blue = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Атрейдесы"],
    )
    green = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Ордос"],
    )

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    downscale_atlas(neutral).save(HD2_OUT, optimize=True)
    red.save(RED_OUT, optimize=True)
    blue.save(BLUE_OUT, optimize=True)
    green.save(GREEN_OUT, optimize=True)
    build_review(neutral, mask).save(REVIEW_OUT, optimize=True)
    build_animation(red)
    build_all_directions_animation(red)
    build_north_hand_check(red).save(HAND_CHECK_OUT, optimize=True)
    build_all_hands_check(red).save(
        ALL_HANDS_CHECK_OUT,
        optimize=True,
    )
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source": str(SOURCE_COPY),
        "classic_contract": str(CLASSIC),
        "operation": (
            "deterministic crop, connected-black extraction, "
            "row reorder 1,2,3,0, north correction 1,2,3,2, "
            "fixed-size anchor alignment, localized direction-specific "
            "weapon-arm stabilization, restored north-facing pistol"
        ),
        "image_generation": "not used; supplied pixels preserved",
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
