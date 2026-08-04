#!/usr/bin/env python3
"""Create a neutral harvester, its House mask, and color previews."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "artifacts"
    / "harvester_direction_fix_v3"
    / "UNIT_HARVESTER_HD4_FIXED.png"
)
OUTPUT = ROOT / "artifacts" / "harvester_faction_preview_v1"
VARIANTS = OUTPUT / "variants"

FRAME = (320, 208)
ATLAS = (2560, 832)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")

HOUSES = (
    ("HARKONNEN", "Харконнены", (255, 0, 0)),
    ("ATREIDES", "Атрейдесы", (0, 0, 255)),
    ("ORDOS", "Ордос", (0, 255, 0)),
    ("MERCENARY", "Наёмники", (214, 121, 16)),
    ("SARDAUKAR", "Сардаукары", (255, 0, 255)),
    ("FREMEN", "Фримены", (194, 125, 60)),
    ("CORRINO", "Коррино", (192, 192, 192)),
)


def smoothstep(low: float, high: float, value: np.ndarray) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def remove_tiny_components(mask: np.ndarray) -> np.ndarray:
    cleaned = np.zeros_like(mask)
    frame_width, frame_height = FRAME
    for row in range(4):
        for column in range(8):
            y = row * frame_height
            x = column * frame_width
            frame = mask[y : y + frame_height, x : x + frame_width]
            labels, count = ndimage.label(
                frame > 0.12,
                structure=np.ones((3, 3), dtype=np.uint8),
            )
            keep = np.zeros_like(frame, dtype=bool)
            for label_id in range(1, count + 1):
                component = labels == label_id
                if np.count_nonzero(component) >= 18:
                    keep |= component
            cleaned[y : y + frame_height, x : x + frame_width] = np.where(
                keep,
                frame,
                0.0,
            )
    return cleaned


def build_selection(source: Image.Image) -> np.ndarray:
    rgba = np.asarray(source.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    maximum_other = np.maximum(green, blue)
    red_dominance = (red - maximum_other) / 255.0
    red_purity = (red - maximum_other) / np.maximum(red, 1.0)

    selection = (
        smoothstep(0.08, 0.30, red_dominance)
        * smoothstep(0.24, 0.55, red_purity)
        * smoothstep(38.0, 88.0, red)
        * (alpha / 255.0)
    )
    selection = remove_tiny_components(selection)
    softened = Image.fromarray(
        np.clip(selection * 255.0, 0, 255).astype(np.uint8),
        "L",
    ).filter(ImageFilter.GaussianBlur(0.75))
    return np.asarray(softened, dtype=np.float32) / 255.0


def build_neutral_base(source: Image.Image, selection: np.ndarray) -> Image.Image:
    rgba = np.asarray(source.convert("RGBA"), dtype=np.float32)
    rgb = rgba[:, :, :3]
    value = np.max(rgb, axis=2)

    steel = np.clip(value * 0.82 + 24.0, 0.0, 255.0)
    neutral = np.dstack(
        (
            steel * 1.01,
            steel * 1.015,
            steel * 1.04,
        )
    )
    neutral = np.clip(neutral, 0.0, 255.0)
    material_strength = np.clip(selection * 1.55, 0.0, 1.0)[:, :, None]
    output = rgba.copy()
    output[:, :, :3] = (
        rgb * (1.0 - material_strength) + neutral * material_strength
    )
    output[:, :, 3] = rgba[:, :, 3]
    output[rgba[:, :, 3] == 0] = 0
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8), "RGBA")


def build_house_mask(source: Image.Image, selection: np.ndarray) -> Image.Image:
    source_alpha = np.asarray(source.getchannel("A"), dtype=np.float32) / 255.0
    # A 52% maximum keeps House identity clear without painting the entire
    # vehicle as one flat saturated color.
    strength = np.clip(selection * source_alpha * 0.52, 0.0, 1.0)
    alpha = np.clip(strength * 255.0, 0, 255).astype(np.uint8)
    rgba = np.full((*alpha.shape, 4), 255, dtype=np.uint8)
    rgba[:, :, 3] = alpha
    rgba[alpha == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def apply_engine_tint(
    neutral: Image.Image,
    mask: Image.Image,
    target: tuple[int, int, int],
) -> Image.Image:
    base = np.asarray(neutral.convert("RGBA"), dtype=np.float32)
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    mask_rgb = np.max(mask_rgba[:, :, :3], axis=2) / 255.0
    strength = (mask_rgba[:, :, 3] / 255.0) * mask_rgb
    luminance = (
        0.299 * base[:, :, 0]
        + 0.587 * base[:, :, 1]
        + 0.114 * base[:, :, 2]
    ) / 128.0

    colored = np.empty_like(base[:, :, :3])
    for channel, target_value in enumerate(target):
        colored[:, :, channel] = np.minimum(255.0, target_value * luminance)
    output = base.copy()
    output[:, :, :3] = (
        base[:, :, :3] * (1.0 - strength[:, :, None])
        + colored * strength[:, :, None]
    )
    output[base[:, :, 3] == 0] = 0
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8), "RGBA")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def frame(atlas: Image.Image, direction: int) -> Image.Image:
    x = direction * FRAME[0]
    return atlas.crop((x, 0, x + FRAME[0], FRAME[1]))


def draw_sprite(
    board: Image.Image,
    sprite: Image.Image,
    position: tuple[int, int],
    size: tuple[int, int],
) -> None:
    shown = sprite.resize(size, Image.Resampling.LANCZOS)
    board.alpha_composite(shown, position)


def build_review(
    neutral: Image.Image,
    mask: Image.Image,
    house_variants: list[tuple[str, str, tuple[int, int, int], Image.Image]],
) -> Image.Image:
    board = Image.new("RGBA", (1920, 1040), (10, 12, 15, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (38, 24),
        "Харвестер — нейтральная основа и цвета фракций",
        font=font(34, True),
        fill=(235, 218, 180, 255),
    )
    draw.text(
        (38, 70),
        "Окрашиваются только бронепанели; ходовая часть, огни и песок неизменны",
        font=font(19),
        fill=(188, 194, 202, 255),
    )

    cards: list[tuple[str, tuple[int, int, int], Image.Image]] = [
        ("Нейтральный", (145, 150, 160), neutral),
        *[(label, color, image) for _, label, color, image in house_variants],
    ]
    card_width = 445
    card_height = 405
    for index, (label, color, atlas) in enumerate(cards):
        column = index % 4
        row = index // 4
        x = 35 + column * 470
        y = 118 + row * 445
        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=12,
            fill=(24, 28, 33, 255),
            outline=(122, 101, 60, 255),
            width=2,
        )
        draw.rounded_rectangle(
            (x + 18, y + 18, x + 54, y + 54),
            radius=6,
            fill=(*color, 255),
            outline=(225, 220, 205, 255),
            width=1,
        )
        draw.text(
            (x + 68, y + 20),
            label,
            font=font(24, True),
            fill=(235, 218, 180, 255),
        )

        draw_sprite(board, frame(atlas, 0), (x + 22, y + 76), (224, 146))
        draw_sprite(board, frame(atlas, 2), (x + 270, y + 74), (144, 94))
        draw_sprite(board, frame(atlas, 7), (x + 270, y + 174), (144, 94))
        draw.text((x + 110, y + 226), "E", font=font(17, True), fill=(180, 185, 190, 255))
        draw.text((x + 332, y + 166), "N", font=font(17, True), fill=(180, 185, 190, 255))
        draw.text((x + 326, y + 268), "SE", font=font(17, True), fill=(180, 185, 190, 255))

        if index == 0:
            mask_frame = frame(mask, 0)
            backdrop = Image.new("RGBA", FRAME, (45, 47, 50, 255))
            backdrop.alpha_composite(mask_frame)
            draw_sprite(board, backdrop, (x + 292, y + 292), (120, 78))
            draw.text(
                (x + 24, y + 326),
                "Белое — зона\nмягкой окраски",
                font=font(17),
                fill=(185, 190, 196, 255),
            )
        else:
            draw.text(
                (x + 24, y + 323),
                "Маска: 52% · материалы сохранены",
                font=font(17),
                fill=(185, 190, 196, 255),
            )

    draw.text(
        (38, 1010),
        "Предварительный просмотр: в игру не установлено.",
        font=font(18),
        fill=(177, 181, 187, 255),
    )
    return board


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    VARIANTS.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != ATLAS:
        raise AssertionError(f"source atlas has size {source.size}, expected {ATLAS}")

    selection = build_selection(source)
    neutral = build_neutral_base(source, selection)
    mask = build_house_mask(source, selection)
    neutral_path = OUTPUT / "UNIT_HARVESTER_NEUTRAL_HD4_PREVIEW.png"
    mask_path = OUTPUT / "HM_UNIT_HARVESTER_HD4_PREVIEW.png"
    neutral.save(neutral_path)
    mask.save(mask_path)

    variants: list[tuple[str, str, tuple[int, int, int], Image.Image]] = []
    for key, label, color in HOUSES:
        tinted = apply_engine_tint(neutral, mask, color)
        tinted.save(VARIANTS / f"UNIT_HARVESTER_{key}_HD4_PREVIEW.png")
        variants.append((key, label, color, tinted))

    review = build_review(neutral, mask, variants)
    review.save(OUTPUT / "UNIT_HARVESTER_FACTION_REVIEW.png")

    alpha_equal = np.array_equal(
        np.asarray(source.getchannel("A")),
        np.asarray(neutral.getchannel("A")),
    )
    manifest = {
        "resource": "UNIT_HARVESTER",
        "resource_id": 137,
        "status": "preview_not_integrated",
        "base": "neutral titanium/steel",
        "mask": "large red armor panels only",
        "mask_max_strength_percent": 52,
        "house_colors": {
            key: list(color) for key, _, color in HOUSES
        },
        "geometry_and_alpha_preserved": alpha_equal,
        "hd4_size": list(neutral.size),
        "direction_order": list(DIRECTIONS),
        "frames": 4,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
