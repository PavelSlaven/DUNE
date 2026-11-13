#!/usr/bin/env python3
"""Prepare empty and Harvester-loaded Carryall frames for review."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "carryall_review_v1"
SOURCE = OUTPUT / "empty_turnaround_transparent.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0130_UNIT_CARRYALL.png"
)
HARVESTER = (
    ROOT
    / "artifacts"
    / "harvester_review_v1"
    / "UNIT_HARVESTER_HD4_PREVIEW.png"
)

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
CLASSIC_FRAME = (48, 48)
HD4_FRAME = (192, 192)
HD4_ATLAS = (HD4_FRAME[0] * len(DIRECTIONS), HD4_FRAME[1] * 2)
HARVESTER_FRAME = (320, 208)

COLOR_OUT = OUTPUT / "UNIT_CARRYALL_COLOR_HD4_PREVIEW.png"
BASE_OUT = OUTPUT / "UNIT_CARRYALL_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_CARRYALL_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "UNIT_CARRYALL_SHADOW_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_CARRYALL_REVIEW.png"


def clean_alpha(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgba[rgba[:, :, 3] < 4] = 0
    return Image.fromarray(rgba, "RGBA")


def trim(image: Image.Image) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("empty Carryall or Harvester frame")
    return image.crop(box)


def extract_carryalls(sheet: Image.Image) -> dict[str, Image.Image]:
    rgba = np.asarray(sheet.convert("RGBA"), dtype=np.uint8)
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        (rgba[:, :, 3] > 8).astype(np.uint8),
        8,
    )
    components: list[tuple[float, float, int, int, int, int, int]] = []
    for label in range(1, count):
        x, y, width, height, area = stats[label]
        if area < 20_000:
            continue
        center_x, center_y = centroids[label]
        components.append(
            (center_y, center_x, label, x, y, width, height)
        )
    if len(components) != len(DIRECTIONS):
        raise AssertionError(
            f"expected 8 Carryall subjects, found {len(components)}"
        )

    components.sort(key=lambda item: item[0])
    ordered = sorted(components[:4], key=lambda item: item[1])
    ordered += sorted(components[4:], key=lambda item: item[1])

    result: dict[str, Image.Image] = {}
    for direction, (_, _, label, x, y, width, height) in zip(
        DIRECTIONS,
        ordered,
        strict=True,
    ):
        component_alpha = (
            (labels[y : y + height, x : x + width] == label)
            .astype(np.uint8)
            * 255
        )
        crop = rgba[y : y + height, x : x + width].copy()
        crop[:, :, 3] = np.minimum(crop[:, :, 3], component_alpha)
        crop[crop[:, :, 3] == 0, :3] = 0
        result[direction] = clean_alpha(
            Image.fromarray(crop, "RGBA")
        )
    return result


def classic_boxes() -> list[list[tuple[int, int, int, int]]]:
    classic = Image.open(CLASSIC).convert("RGBA")
    rows: list[list[tuple[int, int, int, int]]] = []
    for row in range(2):
        boxes: list[tuple[int, int, int, int]] = []
        for index in range(len(DIRECTIONS)):
            frame = classic.crop(
                (
                    index * CLASSIC_FRAME[0],
                    row * CLASSIC_FRAME[1],
                    (index + 1) * CLASSIC_FRAME[0],
                    (row + 1) * CLASSIC_FRAME[1],
                )
            )
            box = frame.getchannel("A").getbbox()
            if box is None:
                raise AssertionError(
                    f"classic Carryall frame {row}:{index} is empty"
                )
            boxes.append(box)
        rows.append(boxes)
    return rows


def place_in_contract(
    subject: Image.Image,
    box: tuple[int, int, int, int],
    padding: int = 8,
) -> Image.Image:
    subject = trim(subject)
    target = tuple(value * 4 for value in box)
    available_width = max(1, target[2] - target[0] - padding)
    available_height = max(1, target[3] - target[1] - padding)
    scale = min(
        available_width / subject.width,
        available_height / subject.height,
    )
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    x = round((target[0] + target[2] - size[0]) / 2)
    y = round((target[1] + target[3] - size[1]) / 2)
    frame = Image.new("RGBA", HD4_FRAME)
    frame.alpha_composite(subject, (x, y))
    return clean_alpha(frame)


def harvester_frames() -> dict[str, Image.Image]:
    atlas = Image.open(HARVESTER).convert("RGBA")
    expected = (HARVESTER_FRAME[0] * len(DIRECTIONS), HARVESTER_FRAME[1] * 4)
    if atlas.size != expected:
        raise AssertionError(
            f"Harvester atlas must be {expected}, got {atlas.size}"
        )
    return {
        direction: atlas.crop(
            (
                index * HARVESTER_FRAME[0],
                0,
                (index + 1) * HARVESTER_FRAME[0],
                HARVESTER_FRAME[1],
            )
        )
        for index, direction in enumerate(DIRECTIONS)
    }


def loaded_frame(
    aircraft: Image.Image,
    harvester: Image.Image,
    loaded_box: tuple[int, int, int, int],
) -> Image.Image:
    # The Harvester is carried under the fuselage. Draw it first so the
    # aircraft body and cargo arms naturally occlude the suspended vehicle.
    cargo = place_in_contract(harvester, loaded_box, padding=12)
    frame = Image.new("RGBA", HD4_FRAME)
    frame.alpha_composite(cargo)
    frame.alpha_composite(aircraft)
    return clean_alpha(frame)


def smoothstep(low: float, high: float, value: np.ndarray) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def neutral_and_mask(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    red_dominance = (red - np.maximum(green, blue)) / 255.0
    redness = red / np.maximum(red + green + blue, 1.0)
    selection = (
        smoothstep(0.06, 0.23, red_dominance)
        * smoothstep(0.43, 0.62, redness)
        * smoothstep(34.0, 92.0, red)
        * (alpha / 255.0)
    )

    luminance = red * 0.299 + green * 0.587 + blue * 0.114
    neutral_target = np.dstack(
        (luminance * 0.80, luminance * 0.85, luminance * 0.92)
    )
    amount = np.clip(selection * 1.28, 0.0, 1.0)[:, :, None]
    neutral = rgba.copy()
    neutral[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - amount)
        + neutral_target * amount
    )
    neutral[alpha == 0] = 0

    mask_alpha = np.clip(selection * 255.0, 0, 255).astype(np.uint8)
    mask_rgba = np.full((*mask_alpha.shape, 4), 255, dtype=np.uint8)
    mask_rgba[:, :, 3] = mask_alpha
    mask_rgba[mask_alpha == 0, :3] = 0
    return (
        Image.fromarray(
            np.clip(neutral, 0, 255).astype(np.uint8),
            "RGBA",
        ),
        Image.fromarray(mask_rgba, "RGBA"),
    )


def atlas_frame(atlas: Image.Image, row: int, index: int) -> Image.Image:
    return atlas.crop(
        (
            index * HD4_FRAME[0],
            row * HD4_FRAME[1],
            (index + 1) * HD4_FRAME[0],
            (row + 1) * HD4_FRAME[1],
        )
    )


def build_shadow(base: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", HD4_ATLAS)
    for row in range(2):
        for index in range(len(DIRECTIONS)):
            frame = atlas_frame(base, row, index)
            alpha = (
                frame.getchannel("A")
                .filter(ImageFilter.GaussianBlur(2.0))
                .point(lambda value: round(value * 0.18))
            )
            shadow = Image.new("RGBA", HD4_FRAME, (5, 4, 3, 0))
            shadow.putalpha(alpha)
            shifted = Image.new("RGBA", HD4_FRAME)
            shifted.alpha_composite(shadow, (4, 4))
            atlas.alpha_composite(
                shifted,
                (index * HD4_FRAME[0], row * HD4_FRAME[1]),
            )
    return atlas


def apply_tint(
    base: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    rgba = np.asarray(base.convert("RGBA"), dtype=np.float32).copy()
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    strength = (
        mask_rgba[:, :, 3] / 255.0
        * np.max(mask_rgba[:, :, :3], axis=2) / 255.0
    )
    luminance = (
        rgba[:, :, 0] * 0.299
        + rgba[:, :, 1] * 0.587
        + rgba[:, :, 2] * 0.114
    ) / 128.0
    for channel, target in enumerate(color):
        tinted = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - strength)
            + tinted * strength
        )
    return Image.fromarray(
        np.clip(rgba, 0, 255).astype(np.uint8),
        "RGBA",
    )


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def build_review(base: Image.Image, mask: Image.Image) -> Image.Image:
    tinted = apply_tint(base, mask, (255, 0, 0))
    board = Image.new("RGBA", (1580, 520), (10, 13, 17, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (20, 14),
        "Транспортник — пустой и с харвестером",
        font=font(28, True),
        fill=(236, 216, 174, 255),
    )
    draw.text(
        (20, 53),
        "Порядок D2TM: E, NE, N, NW, W, SW, S, SE",
        font=font(17),
        fill=(176, 187, 199, 255),
    )
    labels = ("ПУСТОЙ", "ХАРВЕСТЕР")
    for row in range(2):
        y = 92 + row * 205
        draw.text(
            (20, y + 75),
            labels[row],
            font=font(17, True),
            fill=(225, 190, 104, 255),
        )
        for index, direction in enumerate(DIRECTIONS):
            x = 120 + index * 180
            draw.rounded_rectangle(
                (x, y, x + 168, y + 190),
                radius=6,
                fill=(22, 27, 33, 255),
                outline=(137, 104, 48, 255),
                width=2,
            )
            frame = atlas_frame(tinted, row, index).resize(
                (168, 168),
                Image.Resampling.LANCZOS,
            )
            board.alpha_composite(frame, (x, y))
            draw.text(
                (x + 8, y + 169),
                direction,
                font=font(15, True),
                fill=(238, 218, 176, 255),
            )
    return board


def validate(
    color: Image.Image,
    base: Image.Image,
    mask: Image.Image,
    shadow: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("color", color),
        ("base", base),
        ("mask", mask),
        ("shadow", shadow),
    ):
        if image.size != HD4_ATLAS:
            raise AssertionError(
                f"{name}: expected {HD4_ATLAS}, got {image.size}"
            )
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    boxes: list[list[list[int]]] = []
    for row in range(2):
        row_boxes: list[list[int]] = []
        unique: list[bytes] = []
        for index, direction in enumerate(DIRECTIONS):
            frame = atlas_frame(base, row, index)
            box = frame.getchannel("A").getbbox()
            if box is None:
                raise AssertionError(f"{row}:{direction} is empty")
            if (
                box[0] <= 0
                or box[1] <= 0
                or box[2] >= HD4_FRAME[0]
                or box[3] >= HD4_FRAME[1]
            ):
                raise AssertionError(
                    f"{row}:{direction} touches frame edge: {box}"
                )
            row_boxes.append(list(box))
            unique.append(frame.tobytes())
        if len(set(unique)) != len(DIRECTIONS):
            raise AssertionError(f"Carryall row {row} repeats a direction")
        boxes.append(row_boxes)
    return {
        "direction_order": list(DIRECTIONS),
        "rows": ["empty", "loaded_harvester"],
        "logical_frame": list(CLASSIC_FRAME),
        "hd4_frame": list(HD4_FRAME),
        "frame_boxes_hd4": boxes,
        "harvester_source": str(HARVESTER),
    }


def main() -> int:
    for path in (SOURCE, CLASSIC, HARVESTER):
        if not path.is_file():
            raise FileNotFoundError(path)

    carryalls = extract_carryalls(Image.open(SOURCE))
    harvesters = harvester_frames()
    boxes = classic_boxes()

    color = Image.new("RGBA", HD4_ATLAS)
    for index, direction in enumerate(DIRECTIONS):
        empty = place_in_contract(
            carryalls[direction],
            boxes[0][index],
        )
        loaded = loaded_frame(
            empty,
            harvesters[direction],
            boxes[1][index],
        )
        color.alpha_composite(empty, (index * HD4_FRAME[0], 0))
        color.alpha_composite(
            loaded,
            (index * HD4_FRAME[0], HD4_FRAME[1]),
        )

    base, mask = neutral_and_mask(color)
    shadow = build_shadow(base)
    validation = validate(color, base, mask, shadow)

    color.save(COLOR_OUT, optimize=True)
    base.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    build_review(base, mask).save(REVIEW_OUT, optimize=True)
    (OUTPUT / "prepare_manifest.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
