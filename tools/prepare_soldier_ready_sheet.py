#!/usr/bin/env python3
"""Convert the supplied ready 8x4 soldier sheet to the D2TM HD contract."""

from __future__ import annotations

import json
import shutil
from collections import deque
from pathlib import Path

import numpy as np
import cv2
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from prepare_soldier_review_v2 import (
    build_neutral_and_mask,
    classic_anchors,
    downscale_atlas,
    foot_anchor_x,
    frame,
)
from prepare_soldiers_review import apply_engine_tint


ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(
    "C:/Users/Slaven/Downloads/"
    "Gemini_Generated_Image_r1cjz0r1cjz0r1cj.png"
)
OUTPUT = ROOT / "artifacts" / "soldier_review_ready_hq"
SOURCE_COPY = OUTPUT / "source_reference.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0155_UNIT_SOLDIER.png"
)

SOURCE_GRID = (8, 4)
FRAME = (128, 128)
ATLAS = (1024, 512)
TARGET_HEIGHT = 44
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROW_LABELS = ("MOVE_0", "MOVE_1", "MOVE_2", "MOVE_3")
HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}

BASE_OUT = OUTPUT / "UNIT_SOLDIER_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SOLDIER_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "UNIT_SOLDIER_HD2_PREVIEW.png"
RED_OUT = OUTPUT / "UNIT_SOLDIER_HARKONNEN_HD4_PREVIEW.png"
BLUE_OUT = OUTPUT / "UNIT_SOLDIER_ATREIDES_HD4_PREVIEW.png"
GREEN_OUT = OUTPUT / "UNIT_SOLDIER_ORDOS_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SOLDIER_READY_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SOLDIER_READY_ANIMATION.gif"
COMPARISON_OUT = OUTPUT / "UNIT_SOLDIER_HQ_COMPARISON.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def largest_component(mask: np.ndarray) -> np.ndarray:
    """Keep the connected sprite and discard detached background artifacts."""
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=np.uint8)
    best: list[tuple[int, int]] = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            queue: deque[tuple[int, int]] = deque([(x, y)])
            visited[y, x] = 1
            component: list[tuple[int, int]] = []
            while queue:
                current_x, current_y = queue.popleft()
                component.append((current_x, current_y))
                for next_x, next_y in (
                    (current_x - 1, current_y - 1),
                    (current_x, current_y - 1),
                    (current_x + 1, current_y - 1),
                    (current_x - 1, current_y),
                    (current_x + 1, current_y),
                    (current_x - 1, current_y + 1),
                    (current_x, current_y + 1),
                    (current_x + 1, current_y + 1),
                ):
                    if (
                        0 <= next_x < width
                        and 0 <= next_y < height
                        and mask[next_y, next_x]
                        and not visited[next_y, next_x]
                    ):
                        visited[next_y, next_x] = 1
                        queue.append((next_x, next_y))
            if len(component) > len(best):
                best = component
    if not best:
        raise AssertionError("source cell has no visible soldier")
    result = np.zeros_like(mask, dtype=np.uint8)
    for x, y in best:
        result[y, x] = 255
    return result


def remove_white_background(cell: Image.Image) -> Image.Image:
    rgba = np.asarray(cell.convert("RGBA"), dtype=np.uint8).copy()
    rgb = rgba[:, :, :3].astype(np.float32)
    white_distance = np.sqrt(np.mean((255.0 - rgb) ** 2, axis=2))

    core = largest_component(white_distance > 12.0)
    support = Image.fromarray(core, "L").filter(ImageFilter.MaxFilter(9))
    support_array = np.asarray(support, dtype=np.float32) / 255.0
    soft_alpha = np.clip((white_distance - 2.0) / 28.0, 0.0, 1.0)
    source_alpha = rgba[:, :, 3].astype(np.float32) / 255.0
    rgba[:, :, 3] = np.clip(
        soft_alpha * support_array * source_alpha * 255.0,
        0,
        255,
    ).astype(np.uint8)

    subject = Image.fromarray(rgba, "RGBA")
    box = subject.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("background removal erased the soldier")
    return subject.crop(box)


def source_cell(source: Image.Image, column: int, row: int) -> Image.Image:
    cell_width = source.width // SOURCE_GRID[0]
    cell_height = source.height // SOURCE_GRID[1]
    return source.crop(
        (
            column * cell_width,
            row * cell_height,
            (column + 1) * cell_width,
            (row + 1) * cell_height,
        )
    )


def fit_subject(cell: Image.Image) -> tuple[Image.Image, float]:
    subject = remove_white_background(cell)
    subject = subject.resize(
        (
            max(1, round(subject.width * TARGET_HEIGHT / subject.height)),
            TARGET_HEIGHT,
        ),
        Image.Resampling.LANCZOS,
    )
    box = subject.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("resized soldier is empty")
    subject = subject.crop(box)
    if subject.height != TARGET_HEIGHT:
        subject = subject.resize(
            (
                max(1, round(subject.width * TARGET_HEIGHT / subject.height)),
                TARGET_HEIGHT,
            ),
            Image.Resampling.LANCZOS,
        )
    return subject, foot_anchor_x(subject)


def build_colored_atlas(
    source: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    anchors = classic_anchors(classic)
    atlas = Image.new("RGBA", ATLAS)
    for row in range(4):
        for column in range(8):
            subject, subject_anchor_x = fit_subject(
                source_cell(source, column, row)
            )
            anchor_x, baseline = anchors[column]
            output = Image.new("RGBA", FRAME)
            output.alpha_composite(
                subject,
                (
                    round(anchor_x - subject_anchor_x),
                    baseline - subject.height,
                ),
            )
            atlas.alpha_composite(
                output,
                (column * FRAME[0], row * FRAME[1]),
            )
    return atlas


def decontaminate_white_matte(
    rgb: np.ndarray,
    alpha: np.ndarray,
) -> np.ndarray:
    """Recover edge color while keeping the supplied alpha unchanged."""
    alpha_float = alpha.astype(np.float32) / 255.0
    safe_alpha = np.maximum(alpha_float, 0.06)
    recovered = (
        rgb.astype(np.float32)
        - 255.0 * (1.0 - alpha_float[:, :, None])
    ) / safe_alpha[:, :, None]
    recovered = np.clip(recovered, 0, 255)
    blend = np.clip(
        (245.0 - alpha.astype(np.float32)) / 180.0,
        0.0,
        0.82,
    )[:, :, None]
    output = (
        rgb.astype(np.float32) * (1.0 - blend)
        + recovered * blend
    )
    return np.clip(output, 0, 255).astype(np.uint8)


def enhance_frame_rgb_preserve_alpha(sprite: Image.Image) -> Image.Image:
    """Improve material definition without moving a single alpha pixel."""
    rgba = np.asarray(sprite.convert("RGBA"), dtype=np.uint8).copy()
    original_alpha = rgba[:, :, 3].copy()
    rgb = decontaminate_white_matte(rgba[:, :, :3], original_alpha)

    smoothed = cv2.bilateralFilter(
        rgb,
        d=0,
        sigmaColor=5,
        sigmaSpace=1.15,
    )
    blurred = cv2.GaussianBlur(smoothed, (0, 0), 0.56)
    sharpened = cv2.addWeighted(smoothed, 1.22, blurred, -0.22, 0)
    sharpened = np.clip(
        (sharpened.astype(np.float32) - 128.0) * 1.045 + 128.0,
        0,
        255,
    ).astype(np.uint8)

    hsv = cv2.cvtColor(sharpened, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = np.clip(
        hsv[:, :, 1].astype(np.float32) * 1.012,
        0,
        255,
    ).astype(np.uint8)
    enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    coverage = np.clip(
        original_alpha.astype(np.float32) / 96.0,
        0.0,
        1.0,
    )[:, :, None]
    rgba[:, :, :3] = np.clip(
        rgb.astype(np.float32) * (1.0 - coverage)
        + enhanced.astype(np.float32) * coverage,
        0,
        255,
    ).astype(np.uint8)
    rgba[:, :, 3] = original_alpha
    return Image.fromarray(rgba, "RGBA")


def enhance_atlas_rgb_preserve_alpha(atlas: Image.Image) -> Image.Image:
    output = Image.new("RGBA", ATLAS)
    for row in range(4):
        for column in range(8):
            output.alpha_composite(
                enhance_frame_rgb_preserve_alpha(frame(atlas, column, row)),
                (column * FRAME[0], row * FRAME[1]),
            )
    if ImageChops.difference(
        atlas.getchannel("A"),
        output.getchannel("A"),
    ).getbbox():
        raise AssertionError("quality pass changed sprite geometry")
    return output


def build_review(colored: Image.Image) -> Image.Image:
    scale = 2
    board = Image.new("RGBA", (8 * 128 * scale, 4 * 128 * scale + 58))
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, board.width, board.height), fill=(12, 15, 19, 255))
    draw.text(
        (18, 13),
        "UNIT_SOLDIER — итоговая карта 8×4",
        font=font(25, True),
        fill=(236, 219, 182, 255),
    )
    for row in range(4):
        for column in range(8):
            shown = frame(colored, column, row).resize(
                (256, 256),
                Image.Resampling.LANCZOS,
            )
            board.alpha_composite(shown, (column * 256, 58 + row * 256))
            draw.text(
                (column * 256 + 8, 64 + row * 256),
                f"{DIRECTIONS[column]} / {row}",
                font=font(15, True),
                fill=(225, 188, 98, 255),
            )
    return board


def build_comparison(
    before: Image.Image,
    after: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1050, 850), (12, 15, 19, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (20, 15),
        "UNIT_SOLDIER — качество до / после",
        font=font(26, True),
        fill=(236, 219, 182, 255),
    )
    for index, (title, atlas) in enumerate(
        (("ДО", before), ("ПОСЛЕ", after))
    ):
        x_offset = 15 + index * 520
        draw.text(
            (x_offset + 220, 55),
            title,
            font=font(21, True),
            fill=(225, 188, 98, 255),
        )
        for row in range(4):
            for column in range(2):
                source_column = (0, 2, 4, 6)[row]
                source_row = column * 2
                shown = frame(atlas, source_column, source_row).resize(
                    (240, 240),
                    Image.Resampling.LANCZOS,
                )
                board.alpha_composite(
                    shown,
                    (x_offset + column * 250, 95 + row * 185),
                )
    return board


def build_animation(colored: Image.Image) -> None:
    animation_frames = []
    for row in range(4):
        shown = Image.new("RGBA", (1024, 512), (16, 20, 26, 255))
        draw = ImageDraw.Draw(shown)
        for column, direction in enumerate(DIRECTIONS):
            x = (column % 4) * 256
            y = (column // 4) * 256
            shown.alpha_composite(
                frame(colored, column, row).resize(
                    (256, 256),
                    Image.Resampling.LANCZOS,
                ),
                (x, y),
            )
            draw.text(
                (x + 12, y + 10),
                direction,
                font=font(18, True),
                fill=(225, 188, 98, 255),
            )
        animation_frames.append(
            shown.convert("P", palette=Image.Palette.ADAPTIVE)
        )
    animation_frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=animation_frames[1:],
        duration=170,
        loop=0,
        disposal=2,
    )


def component_count(alpha: Image.Image) -> int:
    mask = np.asarray(alpha, dtype=np.uint8) > 8
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=np.uint8)
    count = 0
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            count += 1
            queue: deque[tuple[int, int]] = deque([(x, y)])
            visited[y, x] = 1
            while queue:
                current_x, current_y = queue.popleft()
                for next_x, next_y in (
                    (current_x - 1, current_y - 1),
                    (current_x, current_y - 1),
                    (current_x + 1, current_y - 1),
                    (current_x - 1, current_y),
                    (current_x + 1, current_y),
                    (current_x - 1, current_y + 1),
                    (current_x, current_y + 1),
                    (current_x + 1, current_y + 1),
                ):
                    if (
                        0 <= next_x < width
                        and 0 <= next_y < height
                        and mask[next_y, next_x]
                        and not visited[next_y, next_x]
                    ):
                        visited[next_y, next_x] = 1
                        queue.append((next_x, next_y))
    return count


def validate(
    original: Image.Image,
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    if colored.size != ATLAS or neutral.size != ATLAS or mask.size != ATLAS:
        raise AssertionError("invalid UNIT_SOLDIER atlas dimensions")
    if ImageChops.difference(
        original.getchannel("A"),
        colored.getchannel("A"),
    ).getbbox():
        raise AssertionError("quality enhancement changed poses or silhouettes")
    if ImageChops.difference(
        colored.getchannel("A"),
        neutral.getchannel("A"),
    ).getbbox():
        raise AssertionError("neutralization changed sprite alpha")

    bounds: list[list[list[int]]] = []
    unique: set[bytes] = set()
    for row in range(4):
        row_bounds: list[list[int]] = []
        for column in range(8):
            sprite = frame(neutral, column, row)
            box = sprite.getchannel("A").point(
                lambda value: 255 if value > 8 else 0
            ).getbbox()
            if box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if box[0] < 2 or box[1] < 2 or box[2] > 126 or box[3] > 126:
                raise AssertionError(
                    f"frame touches boundary {column},{row}: {box}"
                )
            if component_count(sprite.getchannel("A")) != 1:
                raise AssertionError(
                    f"detached artifact in frame {column},{row}"
                )
            row_bounds.append(list(box))
            unique.add(sprite.tobytes())
        bounds.append(row_bounds)
    if len(unique) != 32:
        raise AssertionError(f"expected 32 unique frames, got {len(unique)}")

    for column, direction in enumerate(DIRECTIONS):
        baselines = [bounds[row][column][3] for row in range(4)]
        heights = [
            bounds[row][column][3] - bounds[row][column][1]
            for row in range(4)
        ]
        if len(set(baselines)) != 1:
            raise AssertionError(
                f"baseline jumps in {direction}: {baselines}"
            )
        if max(heights) - min(heights) > 1:
            raise AssertionError(
                f"scale jumps in {direction}: {heights}"
            )

    mask_pixels = int(
        np.count_nonzero(np.asarray(mask.getchannel("A")) > 8)
    )
    if mask_pixels < 1000:
        raise AssertionError(f"faction mask is too small: {mask_pixels}")
    return {
        "resource_id": 155,
        "resource": "UNIT_SOLDIER",
        "source_size": [2880, 1440],
        "source_grid": [8, 4],
        "source_cell": [360, 360],
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "direction_order": list(DIRECTIONS),
        "animation_rows": list(ROW_LABELS),
        "target_height_hd4": TARGET_HEIGHT,
        "individual_height_logical": TARGET_HEIGHT // 4,
        "unique_frames": len(unique),
        "frame_bounds": bounds,
        "mask_pixels": mask_pixels,
        "detached_artifacts": 0,
        "pose_geometry_changed": False,
        "alpha_pixels_changed": 0,
    }


def main() -> None:
    if not INPUT.is_file():
        raise FileNotFoundError(INPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(INPUT, SOURCE_COPY)
    source = Image.open(SOURCE_COPY).convert("RGBA")
    if source.size != (2880, 1440):
        raise AssertionError(f"unexpected source size {source.size}")
    if (
        source.width % SOURCE_GRID[0]
        or source.height % SOURCE_GRID[1]
    ):
        raise AssertionError("source sheet is not an exact 8x4 grid")

    classic = Image.open(CLASSIC).convert("RGBA")
    if classic.size != (256, 128):
        raise AssertionError(f"unexpected classic size {classic.size}")

    original = build_colored_atlas(source, classic)
    colored = enhance_atlas_rgb_preserve_alpha(original)
    neutral, mask = build_neutral_and_mask(colored)
    validation = validate(original, colored, neutral, mask)
    red = apply_engine_tint(neutral, mask, HOUSE_COLORS["Харконнены"])
    blue = apply_engine_tint(neutral, mask, HOUSE_COLORS["Атрейдесы"])
    green = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    downscale_atlas(neutral).save(HD2_OUT, optimize=True)
    red.save(RED_OUT, optimize=True)
    blue.save(BLUE_OUT, optimize=True)
    green.save(GREEN_OUT, optimize=True)
    build_review(red).save(REVIEW_OUT, optimize=True)
    original_neutral, original_mask = build_neutral_and_mask(original)
    original_red = apply_engine_tint(
        original_neutral,
        original_mask,
        HOUSE_COLORS["Харконнены"],
    )
    build_comparison(original_red, red).save(COMPARISON_OUT, optimize=True)
    build_animation(red)

    manifest = {
        "format": 1,
        "status": "ready_for_integration",
        "source": str(SOURCE_COPY),
        "classic_contract": str(CLASSIC),
        "operation": (
            "exact 8x4 extraction, detached-artifact removal, "
            "white-matte edge decontamination, alpha-locked local contrast "
            "and controlled sharpening, fixed-height scaling, "
            "classic foot-anchor and baseline alignment, faction-mask build"
        ),
        "image_generation": (
            "built-in edit was evaluated and rejected because it changed "
            "geometry; installed asset uses deterministic alpha-locked "
            "restoration of the supplied sheet"
        ),
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
