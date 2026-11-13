from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "sandworm_review_v1" / "sandworm_imagegen_alpha_clean.png"
ORIGINAL = ROOT / "resources" / "hd" / "classic" / "sdl_data" / "0150_UNIT_SANDWORM.png"
OUT = ROOT / "artifacts" / "sandworm_review_v1"

FRAME_COUNT = 5
LOGICAL_FRAME = 48
HD4_FRAME = LOGICAL_FRAME * 4
HD2_FRAME = LOGICAL_FRAME * 2

# The first three stages keep the same head diameter. The last two stages
# shrink only the visible creature while the disturbed sand remains readable.
TARGET_EXTENTS_HD4 = ((176, 176), (176, 176), (176, 176), (184, 176), (168, 168))


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def clean_key_fringe(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    pixels = list(image.get_flattened_data())
    cleaned: list[tuple[int, int, int, int]] = []
    for red, green, blue, alpha in pixels:
        # The generated subject intentionally contains no green. Remove
        # remaining chroma-key grains instead of tinting the sand edge.
        if alpha and green > 96 and green > red * 1.08 and green > blue * 1.18:
            cleaned.append((0, 0, 0, 0))
        elif alpha < 4:
            cleaned.append((0, 0, 0, 0))
        else:
            cleaned.append((red, green, blue, alpha))
    result = Image.new("RGBA", image.size)
    result.putdata(cleaned)
    return result


def remove_boundary_fragments(image: Image.Image) -> Image.Image:
    rgba = np.array(image.convert("RGBA"))
    alpha = rgba[:, :, 3]
    count, labels, stats, _ = cv2.connectedComponentsWithStats((alpha > 8).astype(np.uint8), 8)
    height, width = alpha.shape
    for component in range(1, count):
        x, y, box_width, box_height, area = (int(value) for value in stats[component])
        touches_edge = x == 0 or y == 0 or x + box_width == width or y + box_height == height
        if touches_edge and area < 1000:
            rgba[labels == component] = 0
    return Image.fromarray(rgba, "RGBA")


def split_generated_frames(source: Image.Image) -> list[Image.Image]:
    width, height = source.size
    frames: list[Image.Image] = []
    for index in range(FRAME_COUNT):
        left = round(index * width / FRAME_COUNT)
        right = round((index + 1) * width / FRAME_COUNT)
        band = remove_boundary_fragments(source.crop((left, 0, right, height)))
        alpha_bbox = band.getchannel("A").getbbox()
        if alpha_bbox is None:
            raise RuntimeError(f"Generated sandworm frame {index + 1} is empty")
        frames.append(band.crop(alpha_bbox))
    return frames


def fit_centered(source: Image.Image, extent: tuple[int, int]) -> Image.Image:
    max_width, max_height = extent
    scale = min(max_width / source.width, max_height / source.height)
    size = (max(1, round(source.width * scale)), max(1, round(source.height * scale)))
    sprite = clean_key_fringe(source.resize(size, Image.Resampling.LANCZOS))
    frame = Image.new("RGBA", (HD4_FRAME, HD4_FRAME), (0, 0, 0, 0))
    position = ((HD4_FRAME - size[0]) // 2, (HD4_FRAME - size[1]) // 2)
    frame.alpha_composite(sprite, position)
    return frame


def stack_vertical(frames: list[Image.Image]) -> Image.Image:
    width = frames[0].width
    result = Image.new("RGBA", (width, frames[0].height * len(frames)), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        result.alpha_composite(frame, (0, index * frame.height))
    return result


def downscale_frames(frames: list[Image.Image]) -> list[Image.Image]:
    return [
        clean_key_fringe(frame.resize((HD2_FRAME, HD2_FRAME), Image.Resampling.LANCZOS))
        for frame in frames
    ]


def checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (24, 28, 31, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(34, 39, 43, 255))
    return image


def build_review(frames: list[Image.Image]) -> Image.Image:
    panel_width = 248
    gap = 18
    margin = 28
    width = margin * 2 + panel_width * FRAME_COUNT + gap * (FRAME_COUNT - 1)
    height = 650
    review = Image.new("RGB", (width, height), (10, 13, 15))
    draw = ImageDraw.Draw(review)
    title_font = font(28, bold=True)
    label_font = font(18, bold=True)
    note_font = font(15)

    draw.text((margin, 18), "Песчаный червь — переработанный цикл HD4", fill=(238, 218, 173), font=title_font)
    draw.text(
        (margin, 57),
        "5 стадий погружения • 48×48 логических пикселей • единый центр и масштаб",
        fill=(164, 174, 180),
        font=note_font,
    )

    original = Image.open(ORIGINAL).convert("RGBA")
    for index, frame in enumerate(frames):
        x = margin + index * (panel_width + gap)
        top = 104
        draw.rounded_rectangle(
            (x, top, x + panel_width, top + 478),
            radius=8,
            fill=(16, 20, 23),
            outline=(130, 94, 28),
            width=2,
        )

        hd_area = checkerboard((HD4_FRAME, HD4_FRAME))
        hd_area.alpha_composite(frame)
        review.paste(hd_area.convert("RGB"), (x + 28, top + 34))

        classic_frame = original.crop((0, index * LOGICAL_FRAME, LOGICAL_FRAME, (index + 1) * LOGICAL_FRAME))
        classic_frame = classic_frame.resize((LOGICAL_FRAME * 3, LOGICAL_FRAME * 3), Image.Resampling.NEAREST)
        classic_area = checkerboard((LOGICAL_FRAME * 3, LOGICAL_FRAME * 3), cell=9)
        classic_area.alpha_composite(classic_frame)
        review.paste(classic_area.convert("RGB"), (x + 52, top + 282))

        draw.text((x + 18, top + 10), f"КАДР {index + 1}", fill=(239, 213, 158), font=label_font)
        draw.text((x + 18, top + 238), "НОВЫЙ HD4", fill=(205, 210, 214), font=note_font)
        draw.text((x + 18, top + 444), "ОРИГИНАЛ ×3", fill=(132, 142, 148), font=note_font)

    draw.text(
        (margin, 607),
        "Кадры 1–3 сохраняют диаметр головы; кадры 4–5 показывают уход под песок без смещения опорной точки.",
        fill=(174, 182, 187),
        font=note_font,
    )
    return review


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source = clean_key_fringe(Image.open(SOURCE))
    source.save(OUT / "sandworm_imagegen_alpha_final.png")

    generated = split_generated_frames(source)
    hd4_frames = [
        fit_centered(frame, extent)
        for frame, extent in zip(generated, TARGET_EXTENTS_HD4, strict=True)
    ]
    hd2_frames = downscale_frames(hd4_frames)

    hd4_atlas = stack_vertical(hd4_frames)
    hd2_atlas = stack_vertical(hd2_frames)
    hd4_atlas.save(OUT / "UNIT_SANDWORM_HD4.png")
    hd2_atlas.save(OUT / "UNIT_SANDWORM_HD2.png")
    build_review(hd4_frames).save(OUT / "UNIT_SANDWORM_REVIEW.png")

    print(f"HD4: {hd4_atlas.size}")
    print(f"HD2: {hd2_atlas.size}")
    for index, frame in enumerate(hd4_frames, start=1):
        print(f"frame {index}: bbox={frame.getchannel('A').getbbox()}")


if __name__ == "__main__":
    main()
