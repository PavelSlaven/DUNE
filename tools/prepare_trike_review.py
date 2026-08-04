#!/usr/bin/env python3
"""Prepare the approved eight-direction Trike sheet for D2TM."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "artifacts" / "trike_review_v2"
SOURCE = REVIEW / "source_turnaround_transparent.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0162_UNIT_TRIKE.png"
)

FRAME = (112, 104)
ATLAS = (FRAME[0] * 8, FRAME[1])
CLASSIC_FRAME = (28, 26)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
SOURCE_DIRECTIONS = ("W", "SW", "S", "SE", "E", "NE", "N", "NW")

BASE_OUT = REVIEW / "UNIT_TRIKE_HD4_PREVIEW.png"
MASK_OUT = REVIEW / "HM_UNIT_TRIKE_HD4_PREVIEW.png"
SHADOW_OUT = REVIEW / "UNIT_TRIKE_SHADOW_HD4_PREVIEW.png"


def clean_alpha(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgba[rgba[:, :, 3] < 4] = 0
    return Image.fromarray(rgba, "RGBA")


def extract_subjects(sheet: Image.Image) -> dict[str, Image.Image]:
    rgba = np.asarray(sheet.convert("RGBA"), dtype=np.uint8)
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        (rgba[:, :, 3] > 8).astype(np.uint8),
        8,
    )
    components: list[tuple[float, float, int, int, int, int, int]] = []
    for label in range(1, count):
        x, y, width, height, area = stats[label]
        if area < 5_000:
            continue
        center_x, center_y = centroids[label]
        components.append(
            (center_y, center_x, label, x, y, width, height)
        )
    if len(components) != 8:
        raise AssertionError(
            f"expected 8 Trike subjects, found {len(components)}"
        )

    components.sort(key=lambda item: item[0])
    ordered = sorted(components[:4], key=lambda item: item[1])
    ordered += sorted(components[4:], key=lambda item: item[1])

    subjects: dict[str, Image.Image] = {}
    for direction, (_, _, label, x, y, width, height) in zip(
        SOURCE_DIRECTIONS,
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
        subjects[direction] = clean_alpha(
            Image.fromarray(crop, "RGBA")
        )
    return subjects


def classic_boxes() -> dict[str, tuple[int, int, int, int]]:
    classic = Image.open(CLASSIC)
    result: dict[str, tuple[int, int, int, int]] = {}
    for index, direction in enumerate(DIRECTIONS):
        item = classic.crop(
            (
                index * CLASSIC_FRAME[0],
                0,
                (index + 1) * CLASSIC_FRAME[0],
                CLASSIC_FRAME[1],
            )
        )
        box = item.getbbox()
        if box is None:
            raise AssertionError(f"classic Trike frame {direction} is empty")
        result[direction] = box
    return result


def place_subject(
    subject: Image.Image,
    classic_box: tuple[int, int, int, int],
) -> Image.Image:
    source_box = subject.getchannel("A").getbbox()
    if source_box is None:
        raise AssertionError("empty Trike direction")
    subject = subject.crop(source_box)

    target_box = tuple(value * 4 for value in classic_box)
    width = max(1, target_box[2] - target_box[0] - 8)
    height = max(1, target_box[3] - target_box[1] - 8)
    # The supplied turnaround uses a lower camera pitch than D2TM.
    # Matching the classic silhouette contract prevents visible size jumps.
    subject = subject.resize((width, height), Image.Resampling.LANCZOS)
    x = round((target_box[0] + target_box[2] - width) / 2)
    y = round((target_box[1] + target_box[3] - height) / 2)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(subject, (x, y))
    return clean_alpha(result)


def smoothstep(low: float, high: float, value: np.ndarray) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def neutral_and_mask(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    blue_dominance = (blue - red) / 255.0
    blueness = blue / np.maximum(red + green + blue, 1.0)
    selection = (
        smoothstep(0.10, 0.32, blue_dominance)
        * smoothstep(0.38, 0.54, blueness)
        * smoothstep(36.0, 112.0, blue)
        * (alpha / 255.0)
    )

    luminance = red * 0.299 + green * 0.587 + blue * 0.114
    neutral_target = np.dstack(
        (luminance * 0.86, luminance * 0.91, luminance * 0.98)
    )
    amount = np.clip(selection * 1.30, 0.0, 1.0)[:, :, None]
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
        Image.fromarray(np.clip(neutral, 0, 255).astype(np.uint8), "RGBA"),
        Image.fromarray(mask_rgba, "RGBA"),
    )


def atlas_frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop(
        (
            index * FRAME[0],
            0,
            (index + 1) * FRAME[0],
            FRAME[1],
        )
    )


def build_shadow(base: Image.Image) -> Image.Image:
    shadow_atlas = Image.new("RGBA", ATLAS)
    for index in range(8):
        item = atlas_frame(base, index)
        alpha = (
            item.getchannel("A")
            .filter(ImageFilter.GaussianBlur(1.6))
            .point(lambda value: round(value * 0.22))
        )
        shadow = Image.new("RGBA", FRAME, (5, 4, 3, 0))
        shadow.putalpha(alpha)
        shifted = Image.new("RGBA", FRAME)
        shifted.alpha_composite(shadow, (3, 3))
        shadow_atlas.alpha_composite(
            shifted,
            (index * FRAME[0], 0),
        )
    return shadow_atlas


def validate(
    base: Image.Image,
    mask: Image.Image,
    shadow: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("base", base),
        ("mask", mask),
        ("shadow", shadow),
    ):
        if image.size != ATLAS:
            raise AssertionError(f"{name}: expected {ATLAS}, got {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    boxes = []
    mask_coverage = []
    frames = []
    for index, direction in enumerate(DIRECTIONS):
        item = atlas_frame(base, index)
        mask_item = atlas_frame(mask, index)
        box = item.getchannel("A").getbbox()
        mask_box = mask_item.getchannel("A").getbbox()
        if box is None or mask_box is None:
            raise AssertionError(f"{direction}: empty image or house mask")
        if box[0] <= 0 or box[1] <= 0 or box[2] >= FRAME[0] or box[3] >= FRAME[1]:
            raise AssertionError(f"{direction}: sprite touches frame edge: {box}")
        boxes.append(list(box))
        mask_coverage.append(
            round(
                np.asarray(mask_item.getchannel("A"), dtype=np.uint8).sum()
                / max(
                    1,
                    np.asarray(item.getchannel("A"), dtype=np.uint8).sum(),
                ),
                4,
            )
        )
        frames.append(item.tobytes())
    if len(set(frames)) != 8:
        raise AssertionError("Trike atlas does not contain 8 unique frames")

    hd2 = base.resize((ATLAS[0] // 2, ATLAS[1] // 2), Image.Resampling.LANCZOS)
    if ImageChops.difference(
        hd2,
        base.resize(hd2.size, Image.Resampling.LANCZOS),
    ).getbbox():
        raise AssertionError("HD2 determinism check failed")
    return {
        "direction_order": list(DIRECTIONS),
        "source_direction_order": list(SOURCE_DIRECTIONS),
        "frame_boxes_hd4": boxes,
        "mask_coverage": mask_coverage,
    }


def main() -> int:
    if not SOURCE.is_file() or not CLASSIC.is_file():
        raise FileNotFoundError("Trike source or classic atlas is missing")

    subjects = extract_subjects(Image.open(SOURCE))
    boxes = classic_boxes()
    colored = Image.new("RGBA", ATLAS)
    for index, direction in enumerate(DIRECTIONS):
        colored.alpha_composite(
            place_subject(subjects[direction], boxes[direction]),
            (index * FRAME[0], 0),
        )

    base, mask = neutral_and_mask(colored)
    shadow = build_shadow(base)
    validation = validate(base, mask, shadow)

    base.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    (REVIEW / "prepare_manifest.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
