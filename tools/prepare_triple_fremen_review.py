from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = (
    ROOT / "artifacts" / "triple_fremen_review_v1" / "source_strips"
)
OUT = ROOT / "artifacts" / "triple_fremen_review_v1"

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
PHASES = ("ШАГ A", "ПРОХОД", "ШАГ B", "ПРИЦЕЛ")
COLUMNS = 8
ROWS = 4
HD4_FRAME = 128
HD2_FRAME = 64
TARGET_MAX_WIDTH = 108
TARGET_MAX_HEIGHT = 98
ANCHOR = (64, 113)
HOUSE_COLORS = {
    "Красный": (238, 42, 35),
    "Синий": (38, 112, 232),
    "Зелёный": (45, 205, 72),
    "Бирюзовый": (40, 197, 190),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def remove_tiny_components(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA")).copy()
    alpha = rgba[:, :, 3]
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (alpha > 8).astype(np.uint8),
        8,
    )
    keep = np.zeros(alpha.shape, dtype=bool)
    for component in range(1, count):
        if stats[component, cv2.CC_STAT_AREA] >= 100:
            keep |= labels == component
    rgba[~keep] = 0
    return Image.fromarray(rgba, "RGBA")


def extract_phases(direction: str) -> list[Image.Image]:
    source = Image.open(SOURCE_DIR / f"{direction}_alpha.png").convert("RGBA")
    phases: list[Image.Image] = []
    for phase in range(ROWS):
        left = round(phase * source.width / ROWS)
        right = round((phase + 1) * source.width / ROWS)
        cell = remove_tiny_components(source.crop((left, 0, right, source.height)))
        bbox = cell.getchannel("A").getbbox()
        if bbox is None:
            raise AssertionError(f"{direction} phase {phase} is empty")
        phases.append(cell.crop(bbox))
    return phases


def normalize(source: Image.Image) -> Image.Image:
    scale = min(
        TARGET_MAX_WIDTH / source.width,
        TARGET_MAX_HEIGHT / source.height,
    )
    size = (
        max(1, round(source.width * scale)),
        max(1, round(source.height * scale)),
    )
    sprite = source.resize(size, Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", (HD4_FRAME, HD4_FRAME), (0, 0, 0, 0))
    frame.alpha_composite(
        sprite,
        (
            ANCHOR[0] - size[0] // 2,
            ANCHOR[1] - size[1],
        ),
    )
    return frame


def stack(frames: list[list[Image.Image]], frame_size: int) -> Image.Image:
    atlas = Image.new(
        "RGBA",
        (frame_size * COLUMNS, frame_size * ROWS),
        (0, 0, 0, 0),
    )
    for row in range(ROWS):
        for column in range(COLUMNS):
            atlas.alpha_composite(
                frames[row][column],
                (column * frame_size, row * frame_size),
            )
    return atlas


def build_house_mask(atlas: Image.Image) -> Image.Image:
    rgba = np.asarray(atlas.convert("RGBA"))
    rgb = rgba[:, :, :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    dominance = red - np.maximum(green, blue)
    selected = (
        (rgba[:, :, 3] > 0)
        & ((hsv[:, :, 0] <= 10) | (hsv[:, :, 0] >= 176))
        & (hsv[:, :, 1] >= 92)
        & (hsv[:, :, 2] >= 58)
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


def tint(
    atlas: Image.Image,
    mask: Image.Image,
    house_color: tuple[int, int, int],
) -> Image.Image:
    base = np.asarray(atlas.convert("RGBA")).astype(np.float32)
    overlay = np.asarray(mask.convert("RGBA")).astype(np.float32)
    strength = overlay[:, :, 3] / 255.0
    luminance = (
        0.299 * base[:, :, 0]
        + 0.587 * base[:, :, 1]
        + 0.114 * base[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(house_color):
        coloured = np.minimum(255.0, target * luminance)
        base[:, :, channel] = (
            base[:, :, channel] * (1.0 - strength)
            + coloured * strength
        )
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGBA")


def checkerboard(size: tuple[int, int], cell: int = 16) -> Image.Image:
    result = Image.new("RGBA", size, (25, 29, 32, 255))
    draw = ImageDraw.Draw(result)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle(
                    (x, y, x + cell - 1, y + cell - 1),
                    fill=(36, 41, 45, 255),
                )
    return result


def build_review(atlas: Image.Image) -> Image.Image:
    scale = 2
    grid = checkerboard(atlas.size)
    grid.alpha_composite(atlas)
    grid = grid.resize(
        (atlas.width * scale, atlas.height * scale),
        Image.Resampling.NEAREST,
    )
    left = 130
    top = 94
    review = Image.new(
        "RGB",
        (left + grid.width + 24, top + grid.height + 42),
        (10, 13, 15),
    )
    review.paste(grid.convert("RGB"), (left, top))
    draw = ImageDraw.Draw(review)
    draw.text(
        (24, 18),
        "Отряд фрименов — полный HD4-атлас",
        font=font(28, True),
        fill=(238, 218, 173),
    )
    draw.text(
        (24, 55),
        "8 направлений × 4 фазы • три бойца • единый масштаб и опорная точка",
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
    for row, phase in enumerate(PHASES):
        y = top + row * HD4_FRAME * scale + HD4_FRAME - 10
        draw.text((18, y), phase, font=font(16, True), fill=(196, 202, 206))
    for column in range(COLUMNS + 1):
        x = left + column * HD4_FRAME * scale
        draw.line((x, top, x, top + grid.height), fill=(132, 94, 28), width=2)
    for row in range(ROWS + 1):
        y = top + row * HD4_FRAME * scale
        draw.line((left, y, left + grid.width, y), fill=(132, 94, 28), width=2)
    return review


def build_house_review(atlas: Image.Image, mask: Image.Image) -> Image.Image:
    samples = [
        tint(atlas, mask, color).crop((0, 0, atlas.width, HD4_FRAME))
        for color in HOUSE_COLORS.values()
    ]
    header = 58
    review = checkerboard(
        (atlas.width, header + HD4_FRAME * len(samples)),
        16,
    )
    draw = ImageDraw.Draw(review)
    draw.rectangle((0, 0, atlas.width, header), fill=(10, 13, 15, 255))
    draw.text(
        (20, 13),
        "Проверка маски фракций — первый ряд",
        font=font(24, True),
        fill=(238, 218, 173, 255),
    )
    for row, (name, sample) in enumerate(
        zip(HOUSE_COLORS, samples, strict=True)
    ):
        y = header + row * HD4_FRAME
        review.alpha_composite(sample, (0, y))
        draw.rectangle((8, y + 8, 150, y + 38), fill=(10, 13, 15, 210))
        draw.text(
            (16, y + 12),
            name,
            font=font(16, True),
            fill=(245, 245, 245, 255),
        )
    return review


def main() -> None:
    direction_phases = {
        direction: extract_phases(direction) for direction in DIRECTIONS
    }
    frames4 = [
        [
            normalize(direction_phases[direction][phase])
            for direction in DIRECTIONS
        ]
        for phase in range(ROWS)
    ]
    atlas4 = stack(frames4, HD4_FRAME)
    atlas2 = atlas4.resize(
        (HD2_FRAME * COLUMNS, HD2_FRAME * ROWS),
        Image.Resampling.LANCZOS,
    )
    mask4 = build_house_mask(atlas4)
    mask2 = mask4.resize(atlas2.size, Image.Resampling.LANCZOS)

    atlas4.save(OUT / "UNIT_TRIPLEFREMEN_HD4.png")
    atlas2.save(OUT / "UNIT_TRIPLEFREMEN_HD2.png")
    mask4.save(OUT / "HM_UNIT_TRIPLEFREMEN_HD4.png")
    mask2.save(OUT / "HM_UNIT_TRIPLEFREMEN_HD2.png")
    build_review(atlas4).save(OUT / "UNIT_TRIPLEFREMEN_REVIEW.png")
    build_house_review(atlas4, mask4).save(
        OUT / "UNIT_TRIPLEFREMEN_HOUSE_COLORS_REVIEW.png"
    )

    frames = [
        atlas4.crop(
            (
                column * HD4_FRAME,
                row * HD4_FRAME,
                (column + 1) * HD4_FRAME,
                (row + 1) * HD4_FRAME,
            )
        )
        for row in range(ROWS)
        for column in range(COLUMNS)
    ]
    if len({frame.tobytes() for frame in frames}) != COLUMNS * ROWS:
        raise AssertionError("atlas frames are not all unique")
    for index, frame in enumerate(frames):
        bbox = frame.getchannel("A").getbbox()
        if bbox is None:
            raise AssertionError(f"empty frame {index}")
        if bbox[3] != ANCHOR[1]:
            raise AssertionError(f"invalid bottom anchor in frame {index}: {bbox}")
    print(
        f"HD4={atlas4.size}; HD2={atlas2.size}; "
        f"unique_frames={len({frame.tobytes() for frame in frames})}"
    )


if __name__ == "__main__":
    main()
