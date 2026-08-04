#!/usr/bin/env python3
"""Replace only the false front grilles on the harvester's upper headings."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "artifacts"
    / "harvester_review_v1"
    / "UNIT_HARVESTER_HD4_PREVIEW.png"
)
REFERENCE = (
    ROOT
    / "artifacts"
    / "harvester_direction_fix_v3"
    / "imagegen_rear_reference.png"
)
OUTPUT_DIR = ROOT / "artifacts" / "harvester_direction_fix_v3"
OUTPUT = OUTPUT_DIR / "UNIT_HARVESTER_HD4_FIXED.png"
REVIEW = OUTPUT_DIR / "UNIT_HARVESTER_DIRECTION_FIX_REVIEW.png"

FRAME = (320, 208)
ATLAS = (2560, 832)
ROWS = 4
DIRECTIONS = {
    1: {
        "name": "NE",
        "reference_column": 3,
        "mirror": True,
        "polygon": [(70, 77), (145, 69), (177, 110), (151, 165), (82, 163), (63, 112)],
    },
    2: {
        "name": "N",
        "reference_column": 2,
        "mirror": False,
        "polygon": [(104, 97), (216, 97), (220, 169), (100, 169)],
    },
    3: {
        "name": "NW",
        "reference_column": 3,
        "mirror": False,
        "polygon": [(175, 69), (250, 77), (257, 112), (238, 163), (169, 165), (143, 110)],
    },
}


def atlas_frame(atlas: Image.Image, column: int, row: int) -> Image.Image:
    left = column * FRAME[0]
    top = row * FRAME[1]
    return atlas.crop((left, top, left + FRAME[0], top + FRAME[1]))


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def sand_mask(frame: Image.Image) -> np.ndarray:
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.int16)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    strong = (
        (alpha > 24)
        & (red > 135)
        & (green > 90)
        & (blue > 35)
        & (red > blue * 1.15)
        & (green > blue * 1.05)
    )
    broad = (
        (alpha > 12)
        & (red > 72)
        & (green > 52)
        & (blue > 28)
        & (red > green * 1.02)
        & (green > blue * 1.03)
        & (red > blue * 1.18)
    )
    labels, count = ndimage.label(
        broad,
        structure=np.ones((3, 3), dtype=np.uint8),
    )
    result = np.zeros_like(broad)
    for label_id in range(1, count + 1):
        component = labels == label_id
        if (
            np.count_nonzero(component) >= 80
            and np.count_nonzero(component & strong) >= 28
        ):
            result |= component
    return result


def red_anchor(frame: Image.Image, generated: bool = False) -> tuple[float, float]:
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.int16)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    armor = (
        (alpha > 64)
        & (red > (55 if generated else 70))
        & (red > green * 1.35)
        & (red > blue * 1.22)
    )
    ys, xs = np.nonzero(armor)
    if not len(xs):
        raise AssertionError("unable to locate the red armor")
    return float(np.median(xs)), float(np.median(ys))


def keyed_reference(frame: Image.Image) -> Image.Image:
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.uint8).copy()
    rgb = rgba[:, :, :3]
    brightness = rgb.max(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    foreground = (brightness > 14) | ((brightness > 7) & (chroma > 5))
    foreground = ndimage.binary_fill_holes(foreground)
    foreground = ndimage.binary_opening(
        foreground,
        structure=np.ones((2, 2), dtype=bool),
    )
    alpha = np.where(foreground, 255, 0).astype(np.uint8)
    rgba[:, :, 3] = alpha
    return Image.fromarray(rgba, "RGBA")


def translate(image: Image.Image, dx: int, dy: int) -> Image.Image:
    shifted = Image.new("RGBA", image.size)
    shifted.alpha_composite(image, (dx, dy))
    return shifted


def make_patch_mask(
    source: Image.Image,
    reference: Image.Image,
    polygon: list[tuple[int, int]],
) -> Image.Image:
    mask = Image.new("L", FRAME)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))

    source_alpha = np.asarray(source.getchannel("A"), dtype=np.uint8)
    reference_alpha = np.asarray(reference.getchannel("A"), dtype=np.uint8)
    protected_sand = sand_mask(source)
    mask_array = np.asarray(mask, dtype=np.uint8).copy()
    mask_array[source_alpha < 16] = 0
    mask_array[reference_alpha < 16] = 0
    mask_array[protected_sand] = 0
    return Image.fromarray(mask_array, "L")


def replace_rear(
    source: Image.Image,
    reference: Image.Image,
    polygon: list[tuple[int, int]],
) -> tuple[Image.Image, Image.Image]:
    source_anchor = red_anchor(source)
    reference_anchor = red_anchor(reference, generated=True)
    aligned = translate(
        reference,
        round(source_anchor[0] - reference_anchor[0]),
        round(source_anchor[1] - reference_anchor[1]),
    )
    mask = make_patch_mask(source, aligned, polygon)
    result = Image.composite(aligned, source, mask)
    result.putalpha(source.getchannel("A"))
    return result, mask


def draw_panel(
    board: Image.Image,
    sprite: Image.Image,
    position: tuple[int, int],
    label: str,
) -> None:
    x, y = position
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle(
        (x - 8, y - 8, x + 248, y + 184),
        radius=8,
        fill=(25, 29, 34, 255),
        outline=(142, 108, 48, 255),
        width=2,
    )
    board.alpha_composite(
        sprite.resize((240, 156), Image.Resampling.LANCZOS),
        (x, y),
    )
    box = draw.textbbox((0, 0), label, font=font(18, True))
    draw.text(
        (x + (240 - (box[2] - box[0])) / 2, y + 160),
        label,
        font=font(18, True),
        fill=(237, 218, 174, 255),
    )


def build_review(before: Image.Image, after: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1760, 760), (10, 12, 15, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (38, 24),
        "Харвестер: исправлена корма без поворота спрайтов",
        font=font(32, True),
        fill=(235, 218, 180, 255),
    )
    draw.text(
        (38, 68),
        "Порядок движка: E · NE · N · NW · W · SW · S · SE",
        font=font(19),
        fill=(188, 194, 202, 255),
    )
    draw.text(
        (38, 110),
        "Было: кормовая сторона похожа на переднюю",
        font=font(22, True),
        fill=(224, 104, 87, 255),
    )
    draw.text(
        (908, 110),
        "Стало: бронепанель, выхлоп и кормовые огни",
        font=font(22, True),
        fill=(110, 208, 133, 255),
    )

    for index, column in enumerate(DIRECTIONS):
        label = DIRECTIONS[column]["name"]
        draw_panel(
            board,
            atlas_frame(before, column, 0),
            (50 + index * 280, 158),
            str(label),
        )
        draw_panel(
            board,
            atlas_frame(after, column, 0),
            (920 + index * 280, 158),
            str(label),
        )

    draw.text(
        (38, 392),
        "NE: все четыре фазы; песок остаётся строго сзади",
        font=font(22, True),
        fill=(226, 190, 100, 255),
    )
    for row in range(ROWS):
        draw_panel(
            board,
            atlas_frame(after, 1, row),
            (50 + row * 280, 438),
            f"фаза {row + 1}",
        )

    draw.text(
        (38, 715),
        "Корпус, камера и опорная точка не вращались и не зеркалились.",
        font=font(18),
        fill=(188, 194, 202, 255),
    )
    return board


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != ATLAS:
        raise AssertionError(f"source size {source.size}, expected {ATLAS}")
    reference = Image.open(REFERENCE).convert("RGBA").resize(
        ATLAS,
        Image.Resampling.LANCZOS,
    )
    corrected = source.copy()
    changed_masks: dict[tuple[int, int], Image.Image] = {}

    for row in range(ROWS):
        for column, spec in DIRECTIONS.items():
            reference_frame = atlas_frame(
                reference,
                int(spec["reference_column"]),
                row,
            )
            if spec["mirror"]:
                reference_frame = reference_frame.transpose(
                    Image.Transpose.FLIP_LEFT_RIGHT
                )
            reference_frame = keyed_reference(reference_frame)
            source_frame = atlas_frame(source, column, row)
            replacement, mask = replace_rear(
                source_frame,
                reference_frame,
                list(spec["polygon"]),
            )
            corrected.paste(
                replacement,
                (column * FRAME[0], row * FRAME[1]),
            )
            changed_masks[(column, row)] = mask

    if corrected.size != source.size:
        raise AssertionError("atlas dimensions changed")
    if corrected.getchannel("A").tobytes() != source.getchannel("A").tobytes():
        raise AssertionError("atlas alpha or silhouette changed")

    for row in range(ROWS):
        for column in range(8):
            before = atlas_frame(source, column, row)
            after = atlas_frame(corrected, column, row)
            difference = ImageChops.difference(before, after)
            if column not in DIRECTIONS:
                if difference.getbbox() is not None:
                    raise AssertionError(
                        f"unrelated heading changed: column={column}, row={row}"
                    )
                continue
            changed = np.asarray(difference.convert("RGBA")).max(axis=2) > 0
            allowed = np.asarray(changed_masks[(column, row)]) > 0
            if np.any(changed & ~allowed):
                raise AssertionError(
                    f"pixels outside the rear mask changed: column={column}, row={row}"
                )
            protected_sand = sand_mask(before)
            if np.any(changed & protected_sand):
                raise AssertionError(
                    f"sand trail changed: column={column}, row={row}"
                )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    corrected.save(OUTPUT)
    build_review(source, corrected).save(REVIEW)
    manifest = {
        "resource": "UNIT_HARVESTER",
        "resource_id": 137,
        "status": "fixed_not_integrated",
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "fixed_columns": ["NE", "N", "NW"],
        "operation": (
            "replace only the false front-grille pixels with rear armor; "
            "preserve the approved body orientation, alpha silhouette, anchors, "
            "and sand trails"
        ),
        "rows": ROWS,
        "hd4_size": list(corrected.size),
    }
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
