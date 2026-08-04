#!/usr/bin/env python3
"""Build an approval-ready HD4 Devastator atlas from the supplied sheet."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "devastator_review_v1"
REFERENCE = OUTPUT / "user_reference.png"
NORTH_EAST_FIXED = OUTPUT / "devastator_ne_fixed_alpha.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0132_UNIT_DEVASTATOR.png"
)

FRAME = (152, 192)
ATLAS = (FRAME[0] * 8, FRAME[1])
CLASSIC_FRAME = (38, 48)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
REFERENCE_CROPS = {
    "SW": (0, 205, 372, 585),
    "W": (350, 215, 725, 570),
    "S": (700, 215, 1015, 570),
    "E": (980, 215, 1350, 575),
    "N": (1325, 215, 1600, 570),
    "NE": (1570, 215, 1916, 590),
}

BASE_OUT = OUTPUT / "UNIT_DEVASTATOR_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_DEVASTATOR_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "UNIT_DEVASTATOR_SHADOW_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_DEVASTATOR_REVIEW.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def clean_alpha(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgba[rgba[:, :, 3] < 4] = 0
    return Image.fromarray(rgba, "RGBA")


def largest_component(mask: np.ndarray) -> np.ndarray:
    labels, count = ndimage.label(mask)
    if count < 1:
        raise AssertionError("foreground extraction produced no subject")
    sizes = ndimage.sum(mask, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    return labels == largest


def extract_reference_subject(
    reference: Image.Image,
    box: tuple[int, int, int, int],
) -> Image.Image:
    crop = np.asarray(reference.crop(box).convert("RGB"), dtype=np.uint8)
    height, width = crop.shape[:2]
    hsv = cv2.cvtColor(crop, cv2.COLOR_RGB2HSV)

    edge_samples = np.concatenate(
        (
            crop[:, :8].reshape(-1, 3),
            crop[:, -8:].reshape(-1, 3),
        ),
        axis=0,
    )
    background = np.median(edge_samples, axis=0)
    difference = np.linalg.norm(
        crop.astype(np.float32) - background[None, None, :],
        axis=2,
    )
    saturation = hsv[:, :, 1].astype(np.float32)

    grab_mask = np.full((height, width), cv2.GC_PR_BGD, dtype=np.uint8)
    grab_mask[:5] = cv2.GC_BGD
    grab_mask[-5:] = cv2.GC_BGD
    grab_mask[:, :5] = cv2.GC_BGD
    grab_mask[:, -5:] = cv2.GC_BGD
    grab_mask[(difference < 14.0) & (saturation < 14.0)] = cv2.GC_BGD
    grab_mask[
        (difference > 58.0)
        | (saturation > 58.0)
    ] = cv2.GC_FGD

    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(
        crop,
        grab_mask,
        None,
        background_model,
        foreground_model,
        6,
        cv2.GC_INIT_WITH_MASK,
    )
    foreground = (
        (grab_mask == cv2.GC_FGD)
        | (grab_mask == cv2.GC_PR_FGD)
    )
    foreground &= (difference > 19.0) | (saturation > 24.0)
    foreground = largest_component(foreground)
    foreground = ndimage.binary_fill_holes(foreground)
    foreground = ndimage.binary_closing(foreground, iterations=1)

    alpha = (
        ndimage.gaussian_filter(foreground.astype(np.float32), 0.55)
        * 255.0
    ).astype(np.uint8)
    alpha[alpha < 8] = 0
    rgba = np.dstack((crop, alpha))
    rgba[alpha == 0, :3] = 0
    return clean_alpha(Image.fromarray(rgba, "RGBA"))


def trim(image: Image.Image) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("empty Devastator direction")
    return image.crop(box)


def atlas_frame(
    atlas: Image.Image,
    index: int,
    frame_size: tuple[int, int],
) -> Image.Image:
    return atlas.crop(
        (
            index * frame_size[0],
            0,
            (index + 1) * frame_size[0],
            frame_size[1],
        )
    )


def classic_boxes(classic: Image.Image) -> list[tuple[int, int, int, int]]:
    boxes = []
    for index in range(8):
        box = atlas_frame(classic, index, CLASSIC_FRAME).getbbox()
        if box is None:
            raise AssertionError("classic Devastator contains empty frame")
        boxes.append(box)
    return boxes


def place_using_classic_contract(
    subject: Image.Image,
    classic_box: tuple[int, int, int, int],
) -> Image.Image:
    subject = trim(subject)
    target_box = tuple(value * 4 for value in classic_box)
    target_width = target_box[2] - target_box[0]
    target_height = target_box[3] - target_box[1]
    scale = min(
        target_width / subject.width,
        target_height / subject.height,
    )
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    x = round((target_box[0] + target_box[2] - size[0]) / 2)
    y = round((target_box[1] + target_box[3] - size[1]) / 2)
    frame = Image.new("RGBA", FRAME)
    frame.alpha_composite(subject, (x, y))
    return clean_alpha(frame)


def smoothstep(
    low: float,
    high: float,
    value: np.ndarray,
) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def neutral_and_mask(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    red_dominance = (red - np.maximum(green, blue)) / 255.0
    redness = red / np.maximum(red + green + blue, 1.0)
    orange_rejection = 1.0 - smoothstep(
        0.42,
        0.62,
        green / np.maximum(red, 1.0),
    )
    selection = (
        smoothstep(0.06, 0.24, red_dominance)
        * smoothstep(0.42, 0.62, redness)
        * orange_rejection
        * smoothstep(35.0, 90.0, red)
        * (alpha / 255.0)
    )

    luminance = red * 0.299 + green * 0.587 + blue * 0.114
    neutral_target = np.dstack(
        (
            luminance * 0.78,
            luminance * 0.82,
            luminance * 0.88,
        )
    )
    amount = np.clip(selection * 1.25, 0.0, 1.0)[:, :, None]
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


def build_shadow(base: Image.Image) -> Image.Image:
    shadow = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas_frame(base, index, FRAME)
        alpha = frame.getchannel("A").filter(
            ImageFilter.GaussianBlur(2.0)
        ).point(lambda value: round(value * 0.18))
        sprite = Image.new("RGBA", FRAME, (5, 4, 3, 0))
        sprite.putalpha(alpha)
        shadow.alpha_composite(
            sprite,
            (index * FRAME[0] + 4, 4),
        )
    return shadow


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


def build_review(
    base: Image.Image,
    mask: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    card_width = 206
    board = Image.new("RGBA", (1690, 760), (10, 13, 17, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (28, 22),
        "Девастатор — HD4, восемь направлений",
        font=font(31, True),
        fill=(238, 219, 177, 255),
    )
    draw.text(
        (28, 63),
        "Контракт D2TM: ID 132, кадр 38×48 → HD4 152×192",
        font=font(18),
        fill=(182, 190, 200, 255),
    )

    harkonnen = apply_tint(base, mask, (255, 0, 0))
    for index, direction in enumerate(DIRECTIONS):
        x = 24 + index * card_width
        y = 105
        draw.rounded_rectangle(
            (x, y, x + 184, y + 226),
            radius=7,
            fill=(22, 27, 33, 255),
            outline=(145, 108, 49, 255),
            width=2,
        )
        frame = atlas_frame(harkonnen, index, FRAME)
        board.alpha_composite(frame, (x + 16, y + 6))
        draw.text(
            (x + 12, y + 198),
            direction,
            font=font(18, True),
            fill=(238, 220, 180, 255),
        )

    draw.text(
        (28, 355),
        "Проверка маски Домов",
        font=font(25, True),
        fill=(230, 196, 104, 255),
    )
    colors = (
        ("Харконнены", (255, 0, 0)),
        ("Атрейдесы", (0, 90, 255)),
        ("Ордос", (0, 255, 0)),
    )
    for index, (label, color) in enumerate(colors):
        x = 28 + index * 260
        y = 395
        tinted = apply_tint(base, mask, color)
        sprite = atlas_frame(tinted, 6, FRAME).resize(
            (190, 240),
            Image.Resampling.LANCZOS,
        )
        board.alpha_composite(sprite, (x, y))
        draw.text(
            (x, 655),
            label,
            font=font(17, True),
            fill=(230, 214, 180, 255),
        )

    draw.text(
        (840, 355),
        "Классический порядок",
        font=font(25, True),
        fill=(230, 196, 104, 255),
    )
    classic_scaled = classic.convert("RGBA").resize(
        (1216, 192),
        Image.Resampling.NEAREST,
    )
    classic_strip = classic_scaled.crop((0, 0, 800, 192))
    board.alpha_composite(classic_strip, (840, 410))
    return board


def main() -> int:
    for path in (REFERENCE, NORTH_EAST_FIXED, CLASSIC):
        if not path.is_file():
            raise FileNotFoundError(path)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    reference = Image.open(REFERENCE).convert("RGB")
    subjects = {
        direction: extract_reference_subject(reference, box)
        for direction, box in REFERENCE_CROPS.items()
    }
    north_east = Image.open(NORTH_EAST_FIXED).convert("RGBA")
    subjects["NE"] = north_east
    subjects["NW"] = north_east.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    subjects["SE"] = subjects["SW"].transpose(
        Image.Transpose.FLIP_LEFT_RIGHT
    )

    classic = Image.open(CLASSIC).convert("RGBA")
    contract_boxes = classic_boxes(classic)
    atlas = Image.new("RGBA", ATLAS)
    for index, direction in enumerate(DIRECTIONS):
        frame = place_using_classic_contract(
            subjects[direction],
            contract_boxes[index],
        )
        atlas.alpha_composite(frame, (index * FRAME[0], 0))
        frame.save(
            OUTPUT / f"{index}_{direction}_HD4.png",
            optimize=True,
        )

    neutral, mask = neutral_and_mask(atlas)
    shadow = build_shadow(neutral)
    if len(
        {
            atlas_frame(neutral, index, FRAME).tobytes()
            for index in range(8)
        }
    ) != 8:
        raise AssertionError("Devastator directions are not unique")
    for name, image in (
        ("base", neutral),
        ("mask", mask),
        ("shadow", shadow),
    ):
        if image.size != ATLAS:
            raise AssertionError(f"{name} atlas dimensions changed")
        for index in range(8):
            box = atlas_frame(image, index, FRAME).getchannel("A").getbbox()
            if box is None:
                raise AssertionError(f"{name} frame {index} is empty")

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    neutral.resize((608, 96), Image.Resampling.LANCZOS).save(
        OUTPUT / "UNIT_DEVASTATOR_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(neutral, mask, classic).save(REVIEW_OUT, optimize=True)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "resource": {
            "id": 132,
            "name": "UNIT_DEVASTATOR",
            "shadow_id": 133,
            "shadow_name": "UNIT_DEVASTATOR_SHADOW",
            "mask_name": "HM_UNIT_DEVASTATOR",
        },
        "direction_order": list(DIRECTIONS),
        "logical_frame": list(CLASSIC_FRAME),
        "hd4_frame": list(FRAME),
        "hd4_atlas": list(ATLAS),
        "generated_directions": [
            "NE (reference-guided redraw with fixed camera)",
        ],
        "derived_directions": [
            "NW (horizontal mirror of corrected NE)",
            "SE (horizontal mirror of SW)",
        ],
        "reference_directions": ["E", "N", "W", "SW", "S"],
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
