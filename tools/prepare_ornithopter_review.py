#!/usr/bin/env python3
"""Build an approval-ready 8x4 HD4 Ornithopter atlas.

The generated master is a strict top-down render.  All directions and wing
positions are derived from that one master so the fuselage scale, pivot and
heading cannot drift between frames.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "ornithopter_review_v1"
SOURCE = OUTPUT / "ornithopter_topdown_alpha.png"
CLASSIC = OUTPUT / "0143_UNIT_ORNITHOPTER_CLASSIC.png"

FRAME = 192
CLASSIC_FRAME = 48
ATLAS_SIZE = (FRAME * 8, FRAME * 4)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
DIRECTION_ANGLES = (-90, -45, 0, 45, 90, 135, 180, -135)

# The source was requested with the nose at 12 o'clock.  These cuts are at
# the articulated wing roots.  The outer layers slide below the fixed
# fuselage, imitating the foreshortening of the original four wing phases.
LEFT_HINGE = 430
RIGHT_HINGE = 822
WING_PHASES = (
    ("СЛОЖЕНЫ", 242, 0),
    ("СРЕДНЕЕ ВЕРХНЕЕ", 145, -18),
    ("РАСКРЫТЫ", 0, 0),
    ("СРЕДНЕЕ НИЖНЕЕ", 145, 18),
)

BASE_OUT = OUTPUT / "UNIT_ORNITHOPTER_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_ORNITHOPTER_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "UNIT_ORNITHOPTER_SHADOW_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_ORNITHOPTER_REVIEW.png"
GIF_OUT = OUTPUT / "UNIT_ORNITHOPTER_WING_ANIMATION.gif"
VALIDATION_OUT = OUTPUT / "validation.json"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def smoothstep(low: float, high: float, value: np.ndarray) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def neutral_and_mask(source: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(source.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))

    raw_selection = (
        (green > 42.0)
        & (green > red * 1.16)
        & (green > blue * 1.12)
        & (alpha > 8.0)
    )
    selection_image = Image.fromarray(
        raw_selection.astype(np.uint8) * 255,
        "L",
    ).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.15))
    selection = (
        np.asarray(selection_image, dtype=np.float32)
        / 255.0
        * (alpha / 255.0)
    )

    luminance = red * 0.299 + green * 0.587 + blue * 0.114
    neutral_target = np.dstack(
        (
            luminance * 0.72,
            luminance * 0.77,
            luminance * 0.84,
        )
    )
    amount = np.clip(selection * 1.12, 0.0, 1.0)[:, :, None]
    neutral = rgba.copy()
    neutral[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - amount)
        + neutral_target * amount
    )
    neutral[alpha == 0] = 0

    mask_alpha = np.clip(selection * 255.0, 0, 255).astype(np.uint8)
    mask = np.full((*mask_alpha.shape, 4), 255, dtype=np.uint8)
    mask[:, :, 3] = mask_alpha
    mask[mask_alpha == 0, :3] = 0

    return (
        Image.fromarray(np.clip(neutral, 0, 255).astype(np.uint8), "RGBA"),
        Image.fromarray(mask, "RGBA"),
    )


def split_layers(image: Image.Image) -> tuple[Image.Image, Image.Image, Image.Image]:
    width, height = image.size
    left = Image.new("RGBA", image.size)
    left.alpha_composite(image.crop((0, 0, LEFT_HINGE, height)), (0, 0))

    body = Image.new("RGBA", image.size)
    body.alpha_composite(
        image.crop((LEFT_HINGE, 0, RIGHT_HINGE, height)),
        (LEFT_HINGE, 0),
    )

    right = Image.new("RGBA", image.size)
    right.alpha_composite(
        image.crop((RIGHT_HINGE, 0, width, height)),
        (RIGHT_HINGE, 0),
    )
    return left, body, right


def compose_phase(
    layers: tuple[Image.Image, Image.Image, Image.Image],
    inward: int,
    vertical: int,
) -> Image.Image:
    left, body, right = layers
    frame = Image.new("RGBA", body.size)
    frame.alpha_composite(left, (inward, vertical))
    frame.alpha_composite(right, (-inward, vertical))
    frame.alpha_composite(body)
    return frame


def centered_canvas(image: Image.Image, size: int = 1600) -> Image.Image:
    canvas = Image.new("RGBA", (size, size))
    x = (size - image.width) // 2
    y = (size - image.height) // 2
    canvas.alpha_composite(image, (x, y))
    return canvas


def rotate_frames(phases: list[Image.Image]) -> list[list[Image.Image]]:
    padded = [centered_canvas(phase) for phase in phases]
    rotated = [
        [
            phase.rotate(
                angle,
                resample=Image.Resampling.BICUBIC,
                expand=False,
            )
            for angle in DIRECTION_ANGLES
        ]
        for phase in padded
    ]

    center = padded[0].width // 2
    extent = 0
    for row in rotated:
        for image in row:
            box = image.getchannel("A").getbbox()
            if box is None:
                raise AssertionError("empty Ornithopter direction")
            extent = max(
                extent,
                center - box[0],
                box[2] - center,
                center - box[1],
                box[3] - center,
            )

    # One shared crop and one shared scale preserve the exact pivot and make
    # apparent size independent of direction.
    extent += 8
    shared_box = (
        center - extent,
        center - extent,
        center + extent,
        center + extent,
    )
    result: list[list[Image.Image]] = []
    for row in rotated:
        output_row = []
        for image in row:
            crop = image.crop(shared_box).resize(
                (184, 184),
                Image.Resampling.LANCZOS,
            )
            frame = Image.new("RGBA", (FRAME, FRAME))
            frame.alpha_composite(crop, (4, 4))
            output_row.append(frame)
        result.append(output_row)
    return result


def assemble_atlas(rows: list[list[Image.Image]]) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS_SIZE)
    for row_index, row in enumerate(rows):
        for column_index, frame in enumerate(row):
            atlas.alpha_composite(
                frame,
                (column_index * FRAME, row_index * FRAME),
            )
    return atlas


def atlas_frame(atlas: Image.Image, column: int, row: int) -> Image.Image:
    return atlas.crop(
        (
            column * FRAME,
            row * FRAME,
            (column + 1) * FRAME,
            (row + 1) * FRAME,
        )
    )


def build_shadow(base: Image.Image) -> Image.Image:
    shadow = Image.new("RGBA", ATLAS_SIZE)
    for row in range(4):
        for column in range(8):
            frame = atlas_frame(base, column, row)
            alpha = frame.getchannel("A").filter(
                ImageFilter.GaussianBlur(2.2)
            ).point(lambda value: round(value * 0.20))
            sprite = Image.new("RGBA", (FRAME, FRAME), (4, 4, 5, 0))
            sprite.putalpha(alpha)
            tile = Image.new("RGBA", (FRAME, FRAME))
            tile.alpha_composite(sprite, (5, 7))
            shadow.alpha_composite(tile, (column * FRAME, row * FRAME))
    return shadow


def tint_house(
    base: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    base_array = np.asarray(base.convert("RGBA"), dtype=np.float32)
    mask_alpha = np.asarray(mask.getchannel("A"), dtype=np.float32) / 255.0
    luminance = (
        base_array[:, :, 0] * 0.299
        + base_array[:, :, 1] * 0.587
        + base_array[:, :, 2] * 0.114
    )
    tint = np.dstack(
        tuple(
            np.clip(luminance * (channel / 150.0), 0, 255)
            for channel in color
        )
    )
    amount = (mask_alpha * 0.92)[:, :, None]
    output = base_array.copy()
    output[:, :, :3] = output[:, :, :3] * (1.0 - amount) + tint * amount
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8), "RGBA")


def checkerboard(size: tuple[int, int], cell: int = 16) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    colors = ((36, 39, 45), (49, 53, 61))
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            draw.rectangle(
                (x, y, x + cell - 1, y + cell - 1),
                fill=colors[((x // cell) + (y // cell)) & 1],
            )
    return image


def paste_sprite(
    board: Image.Image,
    sprite: Image.Image,
    center: tuple[int, int],
    scale: float = 1.0,
) -> None:
    if scale != 1.0:
        sprite = sprite.resize(
            (
                max(1, round(sprite.width * scale)),
                max(1, round(sprite.height * scale)),
            ),
            Image.Resampling.LANCZOS,
        )
    x = center[0] - sprite.width // 2
    y = center[1] - sprite.height // 2
    board.alpha_composite(sprite, (x, y))


def build_review(
    base: Image.Image,
    mask: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    board = checkerboard((2240, 1510)).convert("RGBA")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 2240, 96), fill=(13, 16, 22, 245))
    draw.text(
        (44, 24),
        "ОРНИТОПТЕР · HD4 · 8 НАПРАВЛЕНИЙ × 4 ПОЛОЖЕНИЯ КРЫЛЬЕВ",
        fill=(238, 219, 163),
        font=font(33, True),
    )

    draw.text(
        (44, 116),
        "Направления · раскрытые крылья · единый масштаб и центр",
        fill=(232, 232, 236),
        font=font(24, True),
    )
    for column, direction in enumerate(DIRECTIONS):
        x = 150 + column * 270
        paste_sprite(board, atlas_frame(base, column, 2), (x, 245), 1.12)
        text_box = draw.textbbox((0, 0), direction, font=font(20, True))
        draw.text(
            (x - (text_box[2] - text_box[0]) // 2, 350),
            direction,
            fill=(255, 214, 96),
            font=font(20, True),
        )

    draw.text(
        (44, 405),
        "Цикл крыльев · корпус и опорная точка неподвижны",
        fill=(232, 232, 236),
        font=font(24, True),
    )
    for row, (label, _, _) in enumerate(WING_PHASES):
        x = 285 + row * 510
        paste_sprite(board, atlas_frame(base, 2, row), (x, 560), 1.35)
        box = draw.textbbox((0, 0), label, font=font(18, True))
        draw.text(
            (x - (box[2] - box[0]) // 2, 682),
            label,
            fill=(197, 220, 241),
            font=font(18, True),
        )

    draw.text(
        (44, 745),
        "Маска Домов · окрашиваются только небольшие технические панели",
        fill=(232, 232, 236),
        font=font(24, True),
    )
    house_colors = (
        ("АТРЕЙДЕСЫ", (64, 120, 245)),
        ("ХАРКОННЕНЫ", (225, 47, 42)),
        ("ОРДОС", (48, 205, 92)),
        ("ФРЕМЕНЫ", (220, 177, 72)),
        ("САРДАУКАРЫ", (126, 80, 190)),
        ("НАЁМНИКИ", (52, 190, 195)),
    )
    sample_base = atlas_frame(base, 1, 2)
    sample_mask = atlas_frame(mask, 1, 2)
    for index, (label, color) in enumerate(house_colors):
        x = 205 + index * 355
        paste_sprite(
            board,
            tint_house(sample_base, sample_mask, color),
            (x, 900),
            1.12,
        )
        box = draw.textbbox((0, 0), label, font=font(16, True))
        draw.text(
            (x - (box[2] - box[0]) // 2, 1010),
            label,
            fill=(238, 238, 238),
            font=font(16, True),
        )

    draw.text(
        (44, 1080),
        "Полный игровой атлас · строки 0–3, столбцы E → SE",
        fill=(232, 232, 236),
        font=font(24, True),
    )
    atlas_preview = base.resize((1536, 768), Image.Resampling.LANCZOS)
    atlas_preview = atlas_preview.resize((1152, 576), Image.Resampling.LANCZOS)
    board.alpha_composite(atlas_preview, (44, 1140))

    classic_preview = classic.resize(
        (classic.width * 3, classic.height * 3),
        Image.Resampling.NEAREST,
    )
    board.alpha_composite(classic_preview, (1260, 1140))
    draw.text(
        (1260, 1110),
        "КЛАССИЧЕСКИЙ КОНТРАКТ 48×48",
        fill=(255, 214, 96),
        font=font(17, True),
    )
    return board.crop((0, 0, 2240, 1500))


def build_animation(base: Image.Image) -> None:
    frames = []
    for row in (2, 1, 0, 3):
        frame = atlas_frame(base, 2, row).resize(
            (384, 384),
            Image.Resampling.NEAREST,
        )
        background = checkerboard(frame.size, 32).convert("RGBA")
        background.alpha_composite(frame)
        frames.append(background.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        GIF_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=130,
        loop=0,
        disposal=2,
    )


def validate(
    base: Image.Image,
    mask: Image.Image,
    shadow: Image.Image,
    classic: Image.Image,
) -> dict[str, object]:
    if base.size != ATLAS_SIZE:
        raise AssertionError(f"invalid atlas size: {base.size}")
    if mask.size != ATLAS_SIZE or shadow.size != ATLAS_SIZE:
        raise AssertionError("mask/shadow atlas size mismatch")
    if classic.size != (CLASSIC_FRAME * 8, CLASSIC_FRAME * 4):
        raise AssertionError(f"invalid classic atlas: {classic.size}")

    frame_hashes = set()
    boxes: list[list[list[int]]] = []
    centers: list[list[list[float]]] = []
    for row in range(4):
        row_boxes = []
        row_centers = []
        for column in range(8):
            sprite = atlas_frame(base, column, row)
            box = sprite.getchannel("A").getbbox()
            if box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if box[0] <= 0 or box[1] <= 0 or box[2] >= FRAME or box[3] >= FRAME:
                raise AssertionError(f"clipped frame {column},{row}: {box}")
            frame_hashes.add(sprite.tobytes())
            row_boxes.append(list(box))
            alpha = np.asarray(sprite.getchannel("A"), dtype=np.float64)
            y, x = np.indices(alpha.shape)
            weight = max(alpha.sum(), 1.0)
            row_centers.append(
                [
                    round(float((x * alpha).sum() / weight), 3),
                    round(float((y * alpha).sum() / weight), 3),
                ]
            )
        boxes.append(row_boxes)
        centers.append(row_centers)

    if len(frame_hashes) != 32:
        raise AssertionError("the 32 Ornithopter frames are not unique")

    mask_alpha = np.asarray(mask.getchannel("A"), dtype=np.float64)
    base_alpha = np.asarray(base.getchannel("A"), dtype=np.float64)
    ratio = float(mask_alpha.sum() / max(base_alpha.sum(), 1.0))
    if not 0.015 <= ratio <= 0.24:
        raise AssertionError(f"implausible house-mask coverage: {ratio:.4f}")

    return {
        "resource_id": 143,
        "shadow_id": 144,
        "classic_frame": [48, 48],
        "hd4_frame": [192, 192],
        "atlas": list(base.size),
        "direction_order": list(DIRECTIONS),
        "wing_rows": [item[0] for item in WING_PHASES],
        "unique_frames": len(frame_hashes),
        "frame_boxes": boxes,
        "alpha_centers": centers,
        "house_mask_coverage": round(ratio, 5),
        "installed": False,
    }


def main() -> int:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    if not CLASSIC.is_file():
        raise FileNotFoundError(CLASSIC)

    source = Image.open(SOURCE).convert("RGBA")
    classic = Image.open(CLASSIC).convert("RGBA")
    neutral, house_mask = neutral_and_mask(source)

    neutral_layers = split_layers(neutral)
    mask_layers = split_layers(house_mask)
    neutral_phases = [
        compose_phase(neutral_layers, inward, vertical)
        for _, inward, vertical in WING_PHASES
    ]
    mask_phases = [
        compose_phase(mask_layers, inward, vertical)
        for _, inward, vertical in WING_PHASES
    ]

    base_rows = rotate_frames(neutral_phases)
    mask_rows = rotate_frames(mask_phases)
    base = assemble_atlas(base_rows)
    mask = assemble_atlas(mask_rows)
    shadow = build_shadow(base)

    validation = validate(base, mask, shadow, classic)
    base.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    build_review(base, mask, classic).save(REVIEW_OUT, optimize=True)
    build_animation(base)
    VALIDATION_OUT.write_text(
        json.dumps(validation, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
