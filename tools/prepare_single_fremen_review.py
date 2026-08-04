from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "single_fremen_review_v1" / "single_fremen_imagegen_alpha.png"
ORIGINAL = ROOT / "resources" / "hd" / "classic" / "sdl_data" / "0154_UNIT_SINGLEFREMEN.png"
OUT = ROOT / "artifacts" / "single_fremen_review_v1"

COLUMNS = 8
ROWS = 4
HD4_FRAME = 128
HD2_FRAME = 64
TARGET_HEIGHT_HD4 = 64
TARGET_MAX_WIDTH_HD4 = 72
ANCHOR_HD4 = (64, 100)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROW_NAMES = ("ШАГ A", "ПРОХОД", "ШАГ B", "АТАКА")
HOUSE_COLORS = {
    "Красный": (238, 42, 35),
    "Синий": (38, 112, 232),
    "Зелёный": (45, 205, 72),
    "Бирюзовый": (40, 197, 190),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def clean_key_fringe(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    cleaned: list[tuple[int, int, int, int]] = []
    for red, green, blue, alpha in image.get_flattened_data():
        if alpha and green > 96 and green > red * 1.08 and green > blue * 1.18:
            cleaned.append((0, 0, 0, 0))
        elif alpha < 4:
            cleaned.append((0, 0, 0, 0))
        else:
            cleaned.append((red, green, blue, alpha))
    result = Image.new("RGBA", image.size)
    result.putdata(cleaned)
    return result


def largest_component(image: Image.Image) -> Image.Image:
    rgba = np.array(image.convert("RGBA"))
    alpha = rgba[:, :, 3]
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (alpha > 8).astype(np.uint8),
        8,
    )
    if count < 2:
        raise RuntimeError("empty Fremen source cell")
    component = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    rgba[labels != component] = 0
    return Image.fromarray(rgba, "RGBA")


def source_cells(source: Image.Image) -> list[list[Image.Image]]:
    width, height = source.size
    cells: list[list[Image.Image]] = []
    for row in range(ROWS):
        line = []
        for column in range(COLUMNS):
            box = (
                round(column * width / COLUMNS),
                round(row * height / ROWS),
                round((column + 1) * width / COLUMNS),
                round((row + 1) * height / ROWS),
            )
            cell = largest_component(source.crop(box))
            bbox = cell.getchannel("A").getbbox()
            if bbox is None:
                raise RuntimeError(f"empty Fremen frame {row},{column}")
            line.append(cell.crop(bbox))
        cells.append(line)
    return cells


def normalize_frame(source: Image.Image) -> Image.Image:
    scale = min(
        TARGET_HEIGHT_HD4 / source.height,
        TARGET_MAX_WIDTH_HD4 / source.width,
    )
    size = (max(1, round(source.width * scale)), max(1, round(source.height * scale)))
    sprite = clean_key_fringe(source.resize(size, Image.Resampling.LANCZOS))
    frame = Image.new("RGBA", (HD4_FRAME, HD4_FRAME), (0, 0, 0, 0))
    left = ANCHOR_HD4[0] - size[0] // 2
    top = ANCHOR_HD4[1] - size[1]
    frame.alpha_composite(sprite, (left, top))
    return frame


def stack(frames: list[list[Image.Image]], frame_size: int) -> Image.Image:
    atlas = Image.new(
        "RGBA",
        (frame_size * COLUMNS, frame_size * ROWS),
        (0, 0, 0, 0),
    )
    for row, line in enumerate(frames):
        for column, frame in enumerate(line):
            atlas.alpha_composite(frame, (column * frame_size, row * frame_size))
    return atlas


def downscale(frames4: list[list[Image.Image]]) -> list[list[Image.Image]]:
    return [
        [
            clean_key_fringe(frame.resize((HD2_FRAME, HD2_FRAME), Image.Resampling.LANCZOS))
            for frame in line
        ]
        for line in frames4
    ]


def build_house_mask(atlas: Image.Image) -> Image.Image:
    rgba = np.asarray(atlas.convert("RGBA"))
    rgb = rgba[:, :, :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    hue = hsv[:, :, 0]
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    dominance = red - np.maximum(green, blue)

    # The armour is saturated crimson.  The warmer brown cloth and pouches
    # intentionally fall outside this narrow red hue range.
    selected = (
        (rgba[:, :, 3] > 0)
        & ((hue <= 10) | (hue >= 176))
        & (saturation >= 92)
        & (value >= 58)
        & (dominance >= 28)
    )
    alpha = np.zeros(selected.shape, dtype=np.uint8)
    alpha[selected] = np.clip(
        160 + (dominance[selected] - 28) * 4,
        160,
        255,
    ).astype(np.uint8)
    alpha = cv2.morphologyEx(
        alpha,
        cv2.MORPH_CLOSE,
        np.ones((3, 3), dtype=np.uint8),
    )
    alpha = np.minimum(alpha, rgba[:, :, 3])
    mask = np.full(rgba.shape, 255, dtype=np.uint8)
    mask[:, :, 3] = alpha
    return Image.fromarray(mask, "RGBA")


def tint_with_house_mask(
    atlas: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    base = np.asarray(atlas.convert("RGBA")).astype(np.float32)
    overlay = np.asarray(mask.convert("RGBA")).astype(np.float32)
    strength = (overlay[:, :, 3] / 255.0) * (
        np.max(overlay[:, :, :3], axis=2) / 255.0
    )
    luminance = (
        0.299 * base[:, :, 0]
        + 0.587 * base[:, :, 1]
        + 0.114 * base[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        coloured = np.minimum(255.0, target * luminance)
        base[:, :, channel] = (
            base[:, :, channel] * (1.0 - strength)
            + coloured * strength
        )
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGBA")


def build_house_review(atlas: Image.Image, mask: Image.Image) -> Image.Image:
    sample_box = (0, 0, HD4_FRAME * COLUMNS, HD4_FRAME)
    samples = [
        tint_with_house_mask(atlas, mask, color).crop(sample_box)
        for color in HOUSE_COLORS.values()
    ]
    width = atlas.width
    header = 58
    review = checkerboard((width, header + HD4_FRAME * len(samples)), 16)
    draw = ImageDraw.Draw(review)
    draw.rectangle((0, 0, width, header), fill=(10, 13, 15, 255))
    draw.text(
        (20, 13),
        "Проверка маски фракций — первый ряд атласа",
        font=font(24, True),
        fill=(238, 218, 173, 255),
    )
    for row, (name, sample) in enumerate(zip(HOUSE_COLORS, samples, strict=True)):
        y = header + row * HD4_FRAME
        review.alpha_composite(sample, (0, y))
        draw.rectangle((8, y + 8, 150, y + 38), fill=(10, 13, 15, 210))
        draw.text((16, y + 12), name, font=font(16, True), fill=(245, 245, 245, 255))
    return review


def checkerboard(size: tuple[int, int], cell: int = 16) -> Image.Image:
    result = Image.new("RGBA", size, (25, 29, 32, 255))
    draw = ImageDraw.Draw(result)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(36, 41, 45, 255))
    return result


def build_review(atlas4: Image.Image) -> Image.Image:
    scale = 2
    grid = checkerboard(atlas4.size)
    grid.alpha_composite(atlas4)
    grid = grid.resize(
        (atlas4.width * scale, atlas4.height * scale),
        Image.Resampling.NEAREST,
    )

    left = 130
    top = 94
    review = Image.new("RGB", (left + grid.width + 24, top + grid.height + 42), (10, 13, 15))
    review.paste(grid.convert("RGB"), (left, top))
    draw = ImageDraw.Draw(review)
    draw.text(
        (24, 18),
        "Одиночный фримен — полный HD4-атлас",
        font=font(28, True),
        fill=(238, 218, 173),
    )
    draw.text(
        (24, 55),
        "8 направлений × 4 фазы • игровой рост 16 логических пикселей • единая опорная точка",
        font=font(15),
        fill=(165, 174, 180),
    )
    for column, direction in enumerate(DIRECTIONS):
        x = left + column * HD4_FRAME * scale + HD4_FRAME
        bounds = draw.textbbox((0, 0), direction, font=font(18, True))
        draw.text(
            (x - (bounds[2] - bounds[0]) // 2, top - 26),
            direction,
            font=font(18, True),
            fill=(239, 213, 158),
        )
    for row, name in enumerate(ROW_NAMES):
        y = top + row * HD4_FRAME * scale + HD4_FRAME - 10
        draw.text((18, y), name, font=font(16, True), fill=(196, 202, 206))
    for column in range(COLUMNS + 1):
        x = left + column * HD4_FRAME * scale
        draw.line((x, top, x, top + grid.height), fill=(132, 94, 28), width=2)
    for row in range(ROWS + 1):
        y = top + row * HD4_FRAME * scale
        draw.line((left, y, left + grid.width, y), fill=(132, 94, 28), width=2)
    return review


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source = clean_key_fringe(Image.open(SOURCE))
    source.save(OUT / "single_fremen_imagegen_alpha_final.png")
    generated = source_cells(source)
    frames4 = [[normalize_frame(frame) for frame in line] for line in generated]
    frames2 = downscale(frames4)
    atlas4 = stack(frames4, HD4_FRAME)
    atlas2 = stack(frames2, HD2_FRAME)
    mask4 = build_house_mask(atlas4)
    mask2 = mask4.resize(atlas2.size, Image.Resampling.LANCZOS)
    atlas4.save(OUT / "UNIT_SINGLEFREMEN_HD4.png")
    atlas2.save(OUT / "UNIT_SINGLEFREMEN_HD2.png")
    mask4.save(OUT / "HM_UNIT_SINGLEFREMEN_HD4.png")
    mask2.save(OUT / "HM_UNIT_SINGLEFREMEN_HD2.png")
    build_review(atlas4).save(OUT / "UNIT_SINGLEFREMEN_REVIEW.png")
    build_house_review(atlas4, mask4).save(
        OUT / "UNIT_SINGLEFREMEN_HOUSE_COLORS_REVIEW.png"
    )

    original = Image.open(ORIGINAL)
    if original.size != (32 * COLUMNS, 32 * ROWS):
        raise AssertionError(f"unexpected original atlas: {original.size}")
    print(f"HD4: {atlas4.size}; HD2: {atlas2.size}; frames: {COLUMNS * ROWS}")
    print(
        "house mask: "
        f"{np.count_nonzero(np.asarray(mask4)[:, :, 3])} coloured pixels"
    )
    for row, line in enumerate(frames4):
        heights = []
        for frame in line:
            bbox = frame.getchannel("A").getbbox()
            if bbox is None:
                raise AssertionError("empty normalized frame")
            heights.append(bbox[3] - bbox[1])
        print(f"row {row}: heights={heights}")


if __name__ == "__main__":
    main()
