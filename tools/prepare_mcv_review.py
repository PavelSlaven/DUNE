#!/usr/bin/env python3
"""Prepare the approved eight-direction MCV sheet for D2TM."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "artifacts" / "mcv_review_v1"
SOURCE = REVIEW / "source_turnaround_transparent.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0141_UNIT_MCV.png"
)

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
CLASSIC_FRAME = (48, 50)
HD4_FRAME = (192, 200)
HD4_ATLAS = (HD4_FRAME[0] * len(DIRECTIONS), HD4_FRAME[1])

BASE_OUT = REVIEW / "UNIT_MCV_HD4_PREVIEW.png"
MASK_OUT = REVIEW / "HM_UNIT_MCV_HD4_PREVIEW.png"
SHADOW_OUT = REVIEW / "UNIT_MCV_SHADOW_HD4_PREVIEW.png"


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
        if area < 20_000:
            continue
        center_x, center_y = centroids[label]
        components.append(
            (center_y, center_x, label, x, y, width, height)
        )
    if len(components) != len(DIRECTIONS):
        raise AssertionError(
            f"expected 8 MCV subjects, found {len(components)}"
        )

    components.sort(key=lambda item: item[0])
    ordered = sorted(components[:4], key=lambda item: item[1])
    ordered += sorted(components[4:], key=lambda item: item[1])

    subjects: dict[str, Image.Image] = {}
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

        # ImageGen supplied a soft contact shadow on the chroma key. D2TM
        # already renders a dedicated shadow resource, so remove only the
        # translucent dark shadow while preserving antialiased body edges.
        alpha = crop[:, :, 3]
        luminance = (
            crop[:, :, 0].astype(np.float32) * 0.299
            + crop[:, :, 1].astype(np.float32) * 0.587
            + crop[:, :, 2].astype(np.float32) * 0.114
        )
        source_shadow = (alpha < 250) & (luminance < 45.0)
        crop[source_shadow] = 0
        crop[crop[:, :, 3] == 0, :3] = 0
        subjects[direction] = clean_alpha(
            Image.fromarray(crop, "RGBA")
        )
    return subjects


def classic_boxes() -> dict[str, tuple[int, int, int, int]]:
    classic = Image.open(CLASSIC).convert("RGBA")
    result: dict[str, tuple[int, int, int, int]] = {}
    for index, direction in enumerate(DIRECTIONS):
        frame = classic.crop(
            (
                index * CLASSIC_FRAME[0],
                0,
                (index + 1) * CLASSIC_FRAME[0],
                CLASSIC_FRAME[1],
            )
        )
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"classic MCV frame {direction} is empty")
        result[direction] = box
    return result


def trim(image: Image.Image) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("empty MCV direction")
    return image.crop(box)


def place_subject(
    subject: Image.Image,
    classic_box: tuple[int, int, int, int],
) -> Image.Image:
    subject = trim(subject)
    target_box = tuple(value * 4 for value in classic_box)
    available_width = max(1, target_box[2] - target_box[0] - 8)
    available_height = max(1, target_box[3] - target_box[1] - 8)
    scale = min(
        available_width / subject.width,
        available_height / subject.height,
    )
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    x = round((target_box[0] + target_box[2] - size[0]) / 2)
    y = round((target_box[1] + target_box[3] - size[1]) / 2)
    frame = Image.new("RGBA", HD4_FRAME)
    frame.alpha_composite(subject, (x, y))
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
        (luminance * 0.79, luminance * 0.84, luminance * 0.91)
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


def atlas_frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop(
        (
            index * HD4_FRAME[0],
            0,
            (index + 1) * HD4_FRAME[0],
            HD4_FRAME[1],
        )
    )


def build_shadow(base: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", HD4_ATLAS)
    for index in range(len(DIRECTIONS)):
        frame = atlas_frame(base, index)
        alpha = (
            frame.getchannel("A")
            .filter(ImageFilter.GaussianBlur(2.2))
            .point(lambda value: round(value * 0.20))
        )
        shadow = Image.new("RGBA", HD4_FRAME, (5, 4, 3, 0))
        shadow.putalpha(alpha)
        shifted = Image.new("RGBA", HD4_FRAME)
        shifted.alpha_composite(shadow, (5, 5))
        atlas.alpha_composite(shifted, (index * HD4_FRAME[0], 0))
    return atlas


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
        if image.size != HD4_ATLAS:
            raise AssertionError(
                f"{name}: expected {HD4_ATLAS}, got {image.size}"
            )
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    boxes: list[list[int]] = []
    mask_coverage: list[float] = []
    frames: list[bytes] = []
    for index, direction in enumerate(DIRECTIONS):
        frame = atlas_frame(base, index)
        mask_frame = atlas_frame(mask, index)
        box = frame.getchannel("A").getbbox()
        mask_box = mask_frame.getchannel("A").getbbox()
        if box is None or mask_box is None:
            raise AssertionError(f"{direction}: empty sprite or house mask")
        if (
            box[0] <= 0
            or box[1] <= 0
            or box[2] >= HD4_FRAME[0]
            or box[3] >= HD4_FRAME[1]
        ):
            raise AssertionError(
                f"{direction}: sprite touches frame edge: {box}"
            )
        boxes.append(list(box))
        mask_coverage.append(
            round(
                np.asarray(
                    mask_frame.getchannel("A"),
                    dtype=np.uint8,
                ).sum()
                / max(
                    1,
                    np.asarray(
                        frame.getchannel("A"),
                        dtype=np.uint8,
                    ).sum(),
                ),
                4,
            )
        )
        frames.append(frame.tobytes())
    if len(set(frames)) != len(DIRECTIONS):
        raise AssertionError("MCV atlas does not contain 8 unique directions")
    if not all(0.08 <= value <= 0.85 for value in mask_coverage):
        raise AssertionError(
            f"unexpected MCV mask coverage: {mask_coverage}"
        )
    return {
        "direction_order": list(DIRECTIONS),
        "logical_frame": list(CLASSIC_FRAME),
        "hd4_frame": list(HD4_FRAME),
        "frame_boxes_hd4": boxes,
        "mask_coverage": mask_coverage,
    }


def main() -> int:
    if not SOURCE.is_file() or not CLASSIC.is_file():
        raise FileNotFoundError("MCV source or classic atlas is missing")

    subjects = extract_subjects(Image.open(SOURCE))
    boxes = classic_boxes()
    colored = Image.new("RGBA", HD4_ATLAS)
    for index, direction in enumerate(DIRECTIONS):
        colored.alpha_composite(
            place_subject(subjects[direction], boxes[direction]),
            (index * HD4_FRAME[0], 0),
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
