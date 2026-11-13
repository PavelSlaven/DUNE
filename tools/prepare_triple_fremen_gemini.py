#!/usr/bin/env python3
"""Prepare the supplied 8x4 three-Fremen sheet for the HD packs."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "triple_fremen_gemini_v1"
FRAME4 = 128
FRAME2 = 64
COLUMNS = 8
ROWS = 4
ANCHOR = (64, 126)
TARGET_MAX = (124, 124)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


def resize_rgba(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3] / 255.0
    premultiplied = rgba[:, :, :3] * alpha[:, :, None]
    resized_alpha = cv2.resize(alpha, size, interpolation=cv2.INTER_LANCZOS4)
    resized_rgb = cv2.resize(premultiplied, size, interpolation=cv2.INTER_LANCZOS4)
    resized_alpha = np.clip(resized_alpha, 0.0, 1.0)
    visible = resized_alpha > (1.0 / 255.0)
    result = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    result[:, :, 3] = np.round(resized_alpha * 255.0).astype(np.uint8)
    result[visible, :3] = np.clip(
        resized_rgb[visible] / resized_alpha[visible, None], 0, 255
    ).astype(np.uint8)
    return Image.fromarray(result, "RGBA")


def white_background_alpha(rgb: np.ndarray) -> np.ndarray:
    distance = 255 - rgb.min(axis=2).astype(np.int32)
    alpha = np.clip((distance - 8) * 255 / 12, 0, 255).astype(np.uint8)
    return alpha


def decontaminate_edge_colors(rgba: np.ndarray) -> np.ndarray:
    """Replace white-matte RGB at antialiased edges with nearby sprite colors."""
    cleaned = rgba.copy()
    alpha = cleaned[:, :, 3]
    alpha[alpha <= 8] = 0

    known = alpha >= 224
    pending = (alpha > 0) & ~known
    if np.any(pending) and not np.any(known):
        raise AssertionError("sprite has no opaque pixels for edge decontamination")

    kernel = np.ones((3, 3), dtype=np.float32)
    colors = cleaned[:, :, :3].astype(np.float32)
    while np.any(pending):
        weights = cv2.filter2D(
            known.astype(np.float32), -1, kernel, borderType=cv2.BORDER_CONSTANT
        )
        frontier = pending & (weights > 0)
        if not np.any(frontier):
            raise AssertionError("cannot propagate sprite colors to the alpha edge")
        for channel in range(3):
            totals = cv2.filter2D(
                colors[:, :, channel] * known,
                -1,
                kernel,
                borderType=cv2.BORDER_CONSTANT,
            )
            colors[:, :, channel][frontier] = totals[frontier] / weights[frontier]
        known[frontier] = True
        pending[frontier] = False

    cleaned[:, :, :3] = np.clip(colors, 0, 255).astype(np.uint8)
    cleaned[alpha == 0] = 0
    return cleaned


def clean_cell(cell: Image.Image) -> Image.Image:
    rgb = np.asarray(cell.convert("RGB"))
    alpha = white_background_alpha(rgb)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (alpha > 24).astype(np.uint8), 8
    )
    keep = np.zeros(alpha.shape, dtype=bool)
    for component in range(1, count):
        if stats[component, cv2.CC_STAT_AREA] >= 1800:
            keep |= labels == component
    alpha[~keep] = 0
    corrected = rgb.astype(np.float32)
    partial = (alpha > 0) & (alpha < 255)
    strength = alpha[partial].astype(np.float32) / 255.0
    corrected[partial] = (
        corrected[partial] - (1.0 - strength[:, None]) * 255.0
    ) / strength[:, None]
    corrected = np.clip(corrected, 0, 255).astype(np.uint8)
    rgba = decontaminate_edge_colors(np.dstack((corrected, alpha)))
    return Image.fromarray(rgba, "RGBA")


def component_labels(cell: Image.Image) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rgb = np.asarray(cell.convert("RGB"))
    alpha = white_background_alpha(rgb)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(
        (alpha > 24).astype(np.uint8), 8
    )
    return labels, stats, centroids


def repair_last_frame_artifact(cell: Image.Image, donor: Image.Image) -> Image.Image:
    target_labels, target_stats, target_centroids = component_labels(cell)
    donor_labels, donor_stats, donor_centroids = component_labels(donor)

    target_candidates = [
        index
        for index in range(1, len(target_stats))
        if target_stats[index, cv2.CC_STAT_AREA] >= 1800
        and target_centroids[index, 0] < 180
        and target_centroids[index, 1] < 180
    ]
    donor_candidates = [
        index
        for index in range(1, len(donor_stats))
        if donor_stats[index, cv2.CC_STAT_AREA] >= 1800
        and donor_centroids[index, 0] > 180
        and donor_centroids[index, 1] < 180
    ]
    if len(target_candidates) != 1 or len(donor_candidates) != 1:
        raise AssertionError("cannot isolate the damaged triple-Fremen component")

    target_id = target_candidates[0]
    donor_id = donor_candidates[0]
    target_box = target_stats[target_id, :4]
    donor_box = donor_stats[donor_id, :4]

    repaired = np.asarray(cell.convert("RGB")).copy()
    repaired[target_labels == target_id] = 255

    donor_rgb = np.asarray(donor.convert("RGB"))
    donor_alpha = white_background_alpha(donor_rgb)
    donor_alpha[donor_labels != donor_id] = 0
    dx, dy, dw, dh = (int(value) for value in donor_box)
    donor_rgba = Image.fromarray(
        np.dstack((donor_rgb[dy : dy + dh, dx : dx + dw], donor_alpha[dy : dy + dh, dx : dx + dw])),
        "RGBA",
    )
    tx, ty = int(target_box[0]), int(target_box[1])
    result = Image.fromarray(repaired, "RGB").convert("RGBA")
    result.alpha_composite(donor_rgba, (tx, ty))
    return result.convert("RGB")


def normalize(cell: Image.Image) -> Image.Image:
    bbox = cell.getchannel("A").getbbox()
    if bbox is None:
        raise AssertionError("empty source cell")
    sprite = cell.crop(bbox)
    scale = min(
        TARGET_MAX[0] / sprite.width,
        TARGET_MAX[1] / sprite.height,
    )
    size = (
        max(1, round(sprite.width * scale)),
        max(1, round(sprite.height * scale)),
    )
    sprite = resize_rgba(sprite, size)
    frame = Image.new("RGBA", (FRAME4, FRAME4), (0, 0, 0, 0))
    frame.alpha_composite(
        sprite,
        (ANCHOR[0] - size[0] // 2, ANCHOR[1] - size[1]),
    )
    return frame


def build_mask(atlas: Image.Image) -> Image.Image:
    rgba = np.asarray(atlas.convert("RGBA"))
    rgb = rgba[:, :, :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    dominance = red - np.maximum(green, blue)
    selected = (
        (rgba[:, :, 3] > 0)
        & ((hsv[:, :, 0] <= 12) | (hsv[:, :, 0] >= 176))
        & (hsv[:, :, 1] >= 88)
        & (hsv[:, :, 2] >= 45)
        & (dominance >= 24)
    )
    alpha = np.zeros(selected.shape, dtype=np.uint8)
    alpha[selected] = np.clip(
        150 + (dominance[selected] - 24) * 4, 150, 255
    ).astype(np.uint8)
    alpha = cv2.morphologyEx(
        alpha, cv2.MORPH_CLOSE, np.ones((3, 3), dtype=np.uint8)
    )
    alpha = np.minimum(alpha, rgba[:, :, 3])
    result = np.full(rgba.shape, 255, dtype=np.uint8)
    result[:, :, 3] = alpha
    return Image.fromarray(result, "RGBA")


def build_review(atlas: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (atlas.width, atlas.height + 56), (18, 20, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 12), "UNIT_TRIPLEFREMEN — E NE N NW W SW S SE", fill=(240, 220, 178))
    checker = Image.new("RGBA", atlas.size, (32, 35, 38, 255))
    cdraw = ImageDraw.Draw(checker)
    for y in range(0, atlas.height, 16):
        for x in range(0, atlas.width, 16):
            if (x // 16 + y // 16) % 2:
                cdraw.rectangle((x, y, x + 15, y + 15), fill=(45, 48, 51, 255))
    checker.alpha_composite(atlas)
    canvas.paste(checker.convert("RGB"), (0, 56))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    image = Image.open(source).convert("RGB")
    if image.size != (2880, 1440):
        raise AssertionError(f"expected 2880x1440 source, got {image.size}")

    source_cell = (image.width // COLUMNS, image.height // ROWS)
    donor = image.crop(
        (
            7 * source_cell[0],
            0,
            8 * source_cell[0],
            source_cell[1],
        )
    )
    frames: list[Image.Image] = []
    component_counts: list[int] = []
    for row in range(ROWS):
        for column in range(COLUMNS):
            cell = image.crop(
                (
                    column * source_cell[0],
                    row * source_cell[1],
                    (column + 1) * source_cell[0],
                    (row + 1) * source_cell[1],
                )
            )
            if row == 3 and column == 7:
                cell = repair_last_frame_artifact(cell, donor)
            cleaned = clean_cell(cell)
            if cleaned.getchannel("A").getbbox() is None:
                raise AssertionError(f"empty cleaned source cell {row},{column}")
            binary = (np.asarray(cleaned.getchannel("A")) > 24).astype(np.uint8)
            count, _, stats, _ = cv2.connectedComponentsWithStats(binary, 8)
            component_counts.append(
                int(
                    sum(
                        stats[index, cv2.CC_STAT_AREA] >= 1800
                        for index in range(1, count)
                    )
                )
            )
            frames.append(normalize(cleaned))

    atlas4 = Image.new(
        "RGBA", (FRAME4 * COLUMNS, FRAME4 * ROWS), (0, 0, 0, 0)
    )
    for index, frame in enumerate(frames):
        atlas4.alpha_composite(
            frame, ((index % COLUMNS) * FRAME4, (index // COLUMNS) * FRAME4)
        )
    atlas2 = resize_rgba(atlas4, (FRAME2 * COLUMNS, FRAME2 * ROWS))
    mask4 = build_mask(atlas4)
    mask2 = mask4.resize(atlas2.size, Image.Resampling.LANCZOS)

    bboxes = []
    for index, frame in enumerate(frames):
        bbox = frame.getchannel("A").getbbox()
        if bbox is None or bbox[3] != ANCHOR[1]:
            raise AssertionError(f"invalid frame {index}: {bbox}")
        bboxes.append(bbox)
    if len({frame.tobytes() for frame in frames}) != 32:
        raise AssertionError("the atlas does not contain 32 unique frames")
    if np.any(
        (np.asarray(mask4.getchannel("A")) > 0)
        & (np.asarray(atlas4.getchannel("A")) == 0)
    ):
        raise AssertionError("house mask extends outside the unit silhouette")

    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, OUT / "source_reference.png")
    atlas4.save(OUT / "UNIT_TRIPLEFREMEN_HD4.png", optimize=True)
    atlas2.save(OUT / "UNIT_TRIPLEFREMEN_HD2.png", optimize=True)
    mask4.save(OUT / "HM_UNIT_TRIPLEFREMEN_HD4.png", optimize=True)
    mask2.save(OUT / "HM_UNIT_TRIPLEFREMEN_HD2.png", optimize=True)
    build_review(atlas4).save(OUT / "UNIT_TRIPLEFREMEN_REVIEW.png", optimize=True)
    manifest = {
        "format": 1,
        "source": str(source),
        "source_grid": [COLUMNS, ROWS],
        "direction_order": list(DIRECTIONS),
        "animation_rows": ["MOVE_0", "MOVE_1", "MOVE_2", "ATTACK"],
        "logical_frame": [32, 32],
        "hd4_frame": [FRAME4, FRAME4],
        "anchor_hd4": list(ANCHOR),
        "target_max_hd4": list(TARGET_MAX),
        "component_counts": component_counts,
        "frame_bboxes": [list(bbox) for bbox in bboxes],
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
