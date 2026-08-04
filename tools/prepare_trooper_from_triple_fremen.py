#!/usr/bin/env python3
"""Derive a single UNIT_TROOPER from the approved triple-Fremen atlas."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "artifacts" / "triple_fremen_gemini_v1"
OUT = ROOT / "artifacts" / "trooper_from_triple_fremen_v1"
UNIT_SOURCE = SOURCE_DIR / "UNIT_TRIPLEFREMEN_HD4.png"
MASK_SOURCE = SOURCE_DIR / "HM_UNIT_TRIPLEFREMEN_HD4.png"
REFERENCE = Path(
    "C:/Users/Slaven/Downloads/Gemini_Generated_Image_ieshphieshphiesh.png"
)

COLUMNS = 8
ROWS = 4
FRAME = 128
SELECTION = (32, 64, 96, 128)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


def refine_white_matte(rgba: np.ndarray) -> np.ndarray:
    """Remove the remaining white-source fringe without hollowing bright metal."""
    refined = rgba.copy()
    alpha = refined[:, :, 3]
    visible = alpha > 48

    # White highlights enclosed by the silhouette are sprite detail, not the
    # white source background. Keep those regions fully opaque.
    inverse = (~visible).astype(np.uint8)
    count, labels, _, _ = cv2.connectedComponentsWithStats(inverse, 8)
    border_labels = set(labels[0, :]) | set(labels[-1, :])
    border_labels |= set(labels[:, 0]) | set(labels[:, -1])
    holes = np.zeros(alpha.shape, dtype=bool)
    for label in range(1, count):
        if label not in border_labels:
            holes |= labels == label

    contracted = np.clip(
        (alpha.astype(np.int32) - 48) * 255 / (255 - 48), 0, 255
    ).astype(np.uint8)
    contracted[holes] = 255
    refined[:, :, 3] = contracted
    refined[contracted == 0] = 0
    return refined


def despill_bright_boundary(rgba: np.ndarray) -> np.ndarray:
    """Replace opaque white fringe pixels with adjacent interior colors."""
    cleaned = rgba.copy()
    alpha = cleaned[:, :, 3]
    visible = alpha > 0
    distance = cv2.distanceTransform(visible.astype(np.uint8), cv2.DIST_L2, 5)
    rgb = cleaned[:, :, :3].astype(np.float32)
    channel_min = rgb.min(axis=2)
    channel_max = rgb.max(axis=2)
    suspect = (
        visible
        & (distance <= 2.8)
        & (channel_min >= 170)
        & ((channel_max - channel_min) <= 48)
    )

    known = visible & ~suspect
    pending = suspect.copy()
    kernel = np.ones((3, 3), dtype=np.float32)
    while np.any(pending):
        weights = cv2.filter2D(
            known.astype(np.float32), -1, kernel, borderType=cv2.BORDER_CONSTANT
        )
        frontier = pending & (weights > 0)
        if not np.any(frontier):
            break
        for channel in range(3):
            totals = cv2.filter2D(
                rgb[:, :, channel] * known,
                -1,
                kernel,
                borderType=cv2.BORDER_CONSTANT,
            )
            rgb[:, :, channel][frontier] = totals[frontier] / weights[frontier]
        known[frontier] = True
        pending[frontier] = False

    cleaned[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    cleaned[alpha == 0] = 0
    return cleaned


def isolate_lower_soldier(
    unit_frame: Image.Image, mask_frame: Image.Image, row: int, column: int
) -> tuple[Image.Image, Image.Image]:
    unit = np.asarray(unit_frame.convert("RGBA")).copy()
    mask = np.asarray(mask_frame.convert("RGBA")).copy()
    x0, y0, x1, y1 = SELECTION
    # The three-soldier composition overlaps by a few source pixels in the
    # vertical N/S views. Tighten those two selections around the lower actor.
    if column == 2:
        x1 = 92
    elif column == 6:
        x0 = 40
        if row == 0:
            y0 = 67
    allowed = np.zeros((FRAME, FRAME), dtype=np.uint8)
    allowed[y0:y1, x0:x1] = unit[y0:y1, x0:x1, 3]

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (allowed > 8).astype(np.uint8), 8
    )
    candidates = [
        index
        for index in range(1, count)
        if stats[index, cv2.CC_STAT_AREA] >= 80
    ]
    if not candidates:
        raise AssertionError("cannot isolate the lower soldier")
    selected = max(candidates, key=lambda index: stats[index, cv2.CC_STAT_AREA])
    keep = labels == selected
    # Preserve the antialiased fringe adjoining the selected opaque component.
    keep = cv2.dilate(keep.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    keep &= allowed > 0

    unit[~keep] = 0
    mask[~keep] = 0
    unit = despill_bright_boundary(refine_white_matte(unit))
    mask[:, :, 3] = np.minimum(mask[:, :, 3], unit[:, :, 3])
    return Image.fromarray(unit, "RGBA"), Image.fromarray(mask, "RGBA")


def build_review(atlas: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (atlas.width, atlas.height + 56), (18, 20, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (12, 12),
        "UNIT_TROOPER — E NE N NW W SW S SE",
        fill=(240, 220, 178),
    )
    checker = Image.new("RGBA", atlas.size, (31, 34, 37, 255))
    checker_draw = ImageDraw.Draw(checker)
    for y in range(0, atlas.height, 16):
        for x in range(0, atlas.width, 16):
            if (x // 16 + y // 16) % 2:
                checker_draw.rectangle(
                    (x, y, x + 15, y + 15), fill=(45, 48, 51, 255)
                )
    checker.alpha_composite(atlas)
    canvas.paste(checker.convert("RGB"), (0, 56))
    return canvas


def main() -> int:
    unit_source = Image.open(UNIT_SOURCE).convert("RGBA")
    mask_source = Image.open(MASK_SOURCE).convert("RGBA")
    expected_size = (FRAME * COLUMNS, FRAME * ROWS)
    if unit_source.size != expected_size or mask_source.size != expected_size:
        raise AssertionError("unexpected triple-Fremen atlas dimensions")

    unit_atlas = Image.new("RGBA", expected_size, (0, 0, 0, 0))
    mask_atlas = Image.new("RGBA", expected_size, (0, 0, 0, 0))
    bboxes: list[list[int]] = []
    logical_sizes: list[list[float]] = []
    frames: list[Image.Image] = []
    for row in range(ROWS):
        for column in range(COLUMNS):
            box = (
                column * FRAME,
                row * FRAME,
                (column + 1) * FRAME,
                (row + 1) * FRAME,
            )
            unit_frame, mask_frame = isolate_lower_soldier(
                unit_source.crop(box), mask_source.crop(box), row, column
            )
            bbox = unit_frame.getchannel("A").point(
                lambda value: 255 if value > 8 else 0
            ).getbbox()
            if bbox is None:
                raise AssertionError(f"empty frame {row},{column}")
            if bbox[3] not in (126, 127):
                raise AssertionError(f"invalid foot anchor {row},{column}: {bbox}")
            bboxes.append(list(bbox))
            logical_sizes.append(
                [round((bbox[2] - bbox[0]) / 4, 2), round((bbox[3] - bbox[1]) / 4, 2)]
            )
            frames.append(unit_frame)
            unit_atlas.alpha_composite(unit_frame, (box[0], box[1]))
            mask_atlas.alpha_composite(mask_frame, (box[0], box[1]))

    if len({frame.tobytes() for frame in frames}) != COLUMNS * ROWS:
        raise AssertionError("UNIT_TROOPER does not contain 32 unique frames")
    unit_alpha = np.asarray(unit_atlas.getchannel("A"))
    mask_alpha = np.asarray(mask_atlas.getchannel("A"))
    if np.any((mask_alpha > 0) & (unit_alpha == 0)):
        raise AssertionError("House mask extends outside UNIT_TROOPER")

    OUT.mkdir(parents=True, exist_ok=True)
    unit_atlas.save(OUT / "UNIT_TROOPER_HD4.png", optimize=True)
    mask_atlas.save(OUT / "HM_UNIT_TROOPER_HD4.png", optimize=True)
    build_review(unit_atlas).save(OUT / "UNIT_TROOPER_REVIEW.png", optimize=True)
    manifest = {
        "format": 1,
        "resource": {"id": 165, "name": "UNIT_TROOPER"},
        "source": str(UNIT_SOURCE),
        "visual_reference": str(REFERENCE),
        "derivation": "lower-center soldier from every approved triple-Fremen frame",
        "direction_order": list(DIRECTIONS),
        "animation_rows": ["MOVE_0", "MOVE_1", "MOVE_2", "ATTACK"],
        "logical_frame": [32, 32],
        "hd4_frame": [FRAME, FRAME],
        "selection_hd4": list(SELECTION),
        "frame_bboxes": bboxes,
        "logical_sizes": logical_sizes,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
