#!/usr/bin/env python3
"""Build UNIT_SABOTEUR from eight true articulated walk strips."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import prepare_saboteur_review as base
from check_saboteur_scale_stability import metrics as scale_metrics
from check_saboteur_walk_articulation import (
    direction_metrics as articulation_metrics,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "saboteur_review_v2"
STRIPS = OUTPUT / "source_strips"
CLASSIC = (
    ROOT
    / "artifacts"
    / "saboteur_review_v1"
    / "UNIT_SABOTEUR_classic.png"
)

DIRECTIONS = base.DIRECTIONS
ROWS = base.ROWS
FRAME = base.FRAME
ATLAS = base.ATLAS
TARGET_HEIGHT = base.TARGET_HEIGHT

BASE_OUT = OUTPUT / "UNIT_SABOTEUR_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SABOTEUR_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SABOTEUR_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SABOTEUR_ANIMATION_PREVIEW.gif"
MANIFEST_OUT = OUTPUT / "manifest.json"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def projection_intervals(image: Image.Image) -> list[tuple[int, int]]:
    alpha = np.asarray(image.getchannel("A"))
    active = np.count_nonzero(alpha > 12, axis=0) > 0
    intervals: list[tuple[int, int]] = []
    start: int | None = None
    for x, value in enumerate(active):
        if value and start is None:
            start = x
        if start is not None and (not value or x == len(active) - 1):
            end = x if not value else x + 1
            if end - start > 10:
                intervals.append((start, end))
            start = None
    if len(intervals) != ROWS:
        raise AssertionError(
            f"expected four figures, found {len(intervals)}"
        )
    return intervals


def strip_frames(path: Path) -> list[Image.Image]:
    strip = Image.open(path).convert("RGBA")
    frames: list[Image.Image] = []
    for left, right in projection_intervals(strip):
        cell = strip.crop((left, 0, right, strip.height))
        box = cell.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"empty strip cell in {path}")
        frames.append(cell.crop(box))
    return frames


def head_width(image: Image.Image) -> int:
    active = np.asarray(image.getchannel("A")) > 12
    height = active.shape[0]
    top = active[: max(1, round(height * 0.25))]
    _, xs = np.where(top)
    if len(xs) == 0:
        raise AssertionError("head region is empty")
    return int(xs.max() - xs.min() + 1)


def upper_body_area(image: Image.Image) -> float:
    """Measure the torso/head mass without the changing leg pose."""
    alpha = np.asarray(image.getchannel("A"), dtype=np.float32) / 255.0
    active = alpha > 0.05
    ys, _ = np.where(active)
    if len(ys) == 0:
        raise AssertionError("empty character")
    top = int(ys.min())
    bottom = int(ys.max()) + 1
    split = top + round((bottom - top) * 0.62)
    return float(alpha[top:split].sum())


def normalize_direction(frames: list[Image.Image]) -> list[Image.Image]:
    """Normalize rigid upper-body mass, then apply one direction scale."""
    upper_areas = [upper_body_area(frame) for frame in frames]
    target_upper_area = float(np.median(np.asarray(upper_areas)))
    upper_normalized: list[Image.Image] = []
    for frame, area in zip(frames, upper_areas, strict=True):
        scale = (target_upper_area / area) ** 0.5
        upper_normalized.append(
            frame.resize(
                (
                    max(1, round(frame.width * scale)),
                    max(1, round(frame.height * scale)),
                ),
                Image.Resampling.LANCZOS,
            )
        )

    common_scale = TARGET_HEIGHT / max(
        frame.height for frame in upper_normalized
    )
    return [
        frame.resize(
            (
                max(1, round(frame.width * common_scale)),
                max(1, round(frame.height * common_scale)),
            ),
            Image.Resampling.LANCZOS,
        )
        for frame in upper_normalized
    ]


def build_colored_atlas(classic: Image.Image) -> Image.Image:
    anchors = base.classic_anchors(classic)
    atlas = Image.new("RGBA", ATLAS)
    for column, direction in enumerate(DIRECTIONS):
        frames = normalize_direction(
            strip_frames(STRIPS / f"{direction}_alpha.png")
        )
        anchor_x, anchor_y = anchors[column]
        for row, sprite in enumerate(frames):
            output = Image.new("RGBA", FRAME)
            output.alpha_composite(
                sprite,
                (
                    round(anchor_x - sprite.width / 2.0),
                    anchor_y - sprite.height,
                ),
            )
            atlas.alpha_composite(
                output,
                (column * FRAME[0], row * FRAME[1]),
            )
    return atlas


def validate(atlas: Image.Image) -> dict[str, object]:
    failures: list[str] = []
    bounds: dict[str, object] = {}
    for column, direction in enumerate(DIRECTIONS):
        records: list[list[int]] = []
        for row in range(ROWS):
            box = base.atlas_frame(
                atlas,
                column,
                row,
            ).getchannel("A").getbbox()
            if box is None:
                failures.append(f"empty frame {direction}:{row}")
                continue
            records.append(list(box))
            if box[2] > FRAME[0] or box[3] > FRAME[1]:
                failures.append(f"frame overflow {direction}:{row}")
        bounds[direction] = records

    motion = base.animation_metrics(atlas)
    for direction, values in motion.items():
        span_x = float(values["centroid_span_x"])
        span_y = float(values["centroid_span_y"])
        unevenness = float(values["transition_unevenness"])
        if span_x > 1.5 or span_y > 1.5:
            failures.append(
                f"{direction} anchor jump {span_x:.2f}x{span_y:.2f}"
            )
        if unevenness > 5.0:
            failures.append(
                f"{direction} uneven transitions {unevenness:.2f}"
            )

    scale = scale_metrics(atlas)
    articulation: dict[str, object] = {}
    for column, direction in enumerate(DIRECTIONS):
        scale_values = scale[direction]
        if float(scale_values["head_width_ratio"]) > 1.40:
            failures.append(
                f"{direction} head scale ratio "
                f"{float(scale_values['head_width_ratio']):.3f}"
            )
        if float(scale_values["area_ratio"]) > 1.30:
            failures.append(
                f"{direction} silhouette ratio "
                f"{float(scale_values['area_ratio']):.3f}"
            )
        values = articulation_metrics(atlas, column)
        articulation[direction] = values
        if float(values["upper_mean"]) < 0.0007:
            failures.append(f"{direction} rigid upper body")
        if float(values["lower_mean"]) < 0.0015:
            failures.append(f"{direction} no leg articulation")
        if float(values["lower_to_upper_ratio"]) > 7.0:
            failures.append(f"{direction} floating lower body")

    return {
        "status": "approval_preview" if not failures else "failed",
        "resource_id": 149,
        "resource": "UNIT_SABOTEUR",
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "columns": 8,
        "rows": 4,
        "direction_order": list(DIRECTIONS),
        "target_character_height_hd4": TARGET_HEIGHT,
        "target_character_height_logical": TARGET_HEIGHT / 4,
        "anchor": "classic per-direction center and lower baseline",
        "animation": "four true articulated poses per direction",
        "bounds": bounds,
        "animation_metrics": motion,
        "scale_metrics": scale,
        "articulation_metrics": articulation,
        "scale_stability": {
            "max_area_ratio": max(
                float(value["area_ratio"]) for value in scale.values()
            ),
            "max_upper_body_area_ratio": max(
                float(value["upper_body_area_ratio"])
                for value in scale.values()
            ),
            "max_head_width_ratio": max(
                float(value["head_width_ratio"])
                for value in scale.values()
            ),
            "max_height_span_hd4": max(
                int(value["height_span"]) for value in scale.values()
            ),
        },
        "house_mask_colors": list(base.HOUSE_COLORS),
        "failures": failures,
        "installed": False,
    }


def build_animation(atlas: Image.Image) -> None:
    frames: list[Image.Image] = []
    for row in range(ROWS):
        canvas = Image.new("RGBA", (1280, 260), (16, 20, 26, 255))
        draw = ImageDraw.Draw(canvas)
        for column, direction in enumerate(DIRECTIONS):
            sprite = base.atlas_frame(atlas, column, row).resize(
                (144, 144),
                Image.Resampling.LANCZOS,
            )
            x = 18 + column * 156
            canvas.alpha_composite(sprite, (x, 30))
            draw.text(
                (x + 58, 190),
                direction,
                font=font(17, True),
                fill=(230, 216, 184, 255),
            )
        frames.append(
            canvas.convert("P", palette=Image.Palette.ADAPTIVE)
        )
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=145,
        loop=0,
        disposal=2,
    )


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    classic = Image.open(CLASSIC).convert("RGBA")
    colored = build_colored_atlas(classic)
    neutral, mask = base.build_neutral_and_mask(colored)
    manifest = validate(colored)
    if manifest["failures"]:
        MANIFEST_OUT.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        raise AssertionError("\n".join(manifest["failures"]))

    colored.save(OUTPUT / "UNIT_SABOTEUR_RED_REFERENCE_HD4.png")
    neutral.save(BASE_OUT)
    mask.save(MASK_OUT)
    ordos = base.apply_engine_tint(
        neutral,
        mask,
        base.HOUSE_COLORS["Ордос"],
    )
    base.build_review(colored, neutral, mask, manifest).save(REVIEW_OUT)
    build_animation(ordos)
    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
