#!/usr/bin/env python3
"""Prepare the supplied 8x4 UNIT_TROOPER sheet for approval."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy.ndimage import distance_transform_edt

import prepare_soldier_ready_sheet as soldier
from prepare_soldiers_ready_sheet_hq import enhance_squad_details


ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(
    "C:/Users/Slaven/Downloads/"
    "Gemini_Generated_Image_9lxeif9lxeif9lxe.png"
)
OUTPUT = ROOT / "artifacts" / "trooper_review_ready_hq"
SOURCE_COPY = OUTPUT / "source_reference.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0165_UNIT_TROOPER.png"
)

SOURCE_SIZE = (2880, 1440)
ATLAS_SIZE = (1024, 512)
FRAME_SIZE = (128, 128)
TARGET_HEIGHT = 44
RESOURCE_ID = 165
RESOURCE_NAME = "UNIT_TROOPER"

BASE_OUT = OUTPUT / "UNIT_TROOPER_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_TROOPER_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "UNIT_TROOPER_HD2_PREVIEW.png"
RED_OUT = OUTPUT / "UNIT_TROOPER_HARKONNEN_HD4_PREVIEW.png"
BLUE_OUT = OUTPUT / "UNIT_TROOPER_ATREIDES_HD4_PREVIEW.png"
GREEN_OUT = OUTPUT / "UNIT_TROOPER_ORDOS_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_TROOPER_READY_HQ_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_TROOPER_READY_HQ_ANIMATION.gif"


def resize_premultiplied(
    image: Image.Image,
    size: tuple[int, int],
) -> Image.Image:
    """Resize RGBA without pulling the white source matte into the edge."""
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    premultiplied = rgba[:, :, :3] * alpha
    resized_alpha = cv2.resize(
        alpha,
        size,
        interpolation=cv2.INTER_LANCZOS4,
    )
    if resized_alpha.ndim == 2:
        resized_alpha = resized_alpha[:, :, None]
    resized_premultiplied = cv2.resize(
        premultiplied,
        size,
        interpolation=cv2.INTER_LANCZOS4,
    )
    resized_alpha = np.clip(resized_alpha, 0.0, 1.0)
    safe_alpha = np.maximum(resized_alpha, 1.0 / 255.0)
    rgb = np.where(
        resized_alpha > 0.0,
        resized_premultiplied / safe_alpha,
        0.0,
    )
    output = np.concatenate(
        (
            np.clip(rgb, 0.0, 255.0),
            resized_alpha * 255.0,
        ),
        axis=2,
    ).astype(np.uint8)
    return Image.fromarray(output, "RGBA")


def fit_subject(cell: Image.Image) -> tuple[Image.Image, float]:
    subject = soldier.remove_white_background(cell)
    width = max(1, round(subject.width * TARGET_HEIGHT / subject.height))
    subject = resize_premultiplied(subject, (width, TARGET_HEIGHT))
    box = subject.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("resized trooper is empty")
    subject = subject.crop(box)
    if subject.height != TARGET_HEIGHT:
        width = max(1, round(subject.width * TARGET_HEIGHT / subject.height))
        subject = resize_premultiplied(subject, (width, TARGET_HEIGHT))
    rgba = np.asarray(subject.convert("RGBA"), dtype=np.uint8).copy()
    core = soldier.largest_component(rgba[:, :, 3] > 8)
    support = np.asarray(
        Image.fromarray(core, "L").filter(ImageFilter.MaxFilter(3)),
        dtype=np.uint8,
    ) > 0
    rgba[~support] = 0
    subject = Image.fromarray(rgba, "RGBA")
    return subject, soldier.foot_anchor_x(subject)


def build_colored_atlas(
    source: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    anchors = soldier.classic_anchors(classic)
    atlas = Image.new("RGBA", ATLAS_SIZE)
    for row in range(4):
        for column in range(8):
            subject, subject_anchor_x = fit_subject(
                soldier.source_cell(source, column, row)
            )
            anchor_x, baseline = anchors[column]
            output = Image.new("RGBA", FRAME_SIZE)
            output.alpha_composite(
                subject,
                (
                    round(anchor_x - subject_anchor_x),
                    baseline - subject.height,
                ),
            )
            atlas.alpha_composite(
                output,
                (column * FRAME_SIZE[0], row * FRAME_SIZE[1]),
            )
    return atlas


def clean_translucent_edge_colors(atlas: Image.Image) -> Image.Image:
    """Fill matte-contaminated pixels from the nearest valid armor pixel."""
    output = Image.new("RGBA", ATLAS_SIZE)
    for row in range(4):
        for column in range(8):
            sprite = soldier.frame(atlas, column, row)
            rgba = np.asarray(sprite.convert("RGBA"), dtype=np.uint8).copy()
            alpha = rgba[:, :, 3]
            minimum_channel = np.min(rgba[:, :, :3], axis=2)
            seed = (alpha >= 180) & (minimum_channel < 170)
            if not np.any(seed):
                raise AssertionError(f"no opaque seed in {column},{row}")
            nearest = distance_transform_edt(
                ~seed,
                return_distances=False,
                return_indices=True,
            )
            edge = (
                ((alpha > 0) & (alpha < 225))
                | ((alpha > 0) & (minimum_channel > 185))
            )
            nearest_rgb = rgba[nearest[0], nearest[1], :3]
            rgba[edge, :3] = nearest_rgb[edge]
            cleaned = Image.fromarray(rgba, "RGBA")
            output.alpha_composite(
                cleaned,
                (column * FRAME_SIZE[0], row * FRAME_SIZE[1]),
            )
    if ImageChops.difference(
        atlas.getchannel("A"),
        output.getchannel("A"),
    ).getbbox():
        raise AssertionError("edge cleanup changed trooper geometry")
    return output


def build_review(colored: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (2048, 1082), (12, 15, 19, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (18, 13),
        "UNIT_TROOPER — улучшенный атлас 8×4",
        font=soldier.font(25, True),
        fill=(236, 219, 182, 255),
    )
    for row in range(4):
        for column in range(8):
            shown = soldier.frame(colored, column, row).resize(
                (256, 256),
                Image.Resampling.LANCZOS,
            )
            board.alpha_composite(shown, (column * 256, 58 + row * 256))
            draw.text(
                (column * 256 + 8, 64 + row * 256),
                f"{soldier.DIRECTIONS[column]} / {row}",
                font=soldier.font(15, True),
                fill=(225, 188, 98, 255),
            )
    return board


def build_animation(colored: Image.Image) -> None:
    frames = []
    for row in range(4):
        shown = Image.new("RGBA", (1024, 512), (16, 20, 26, 255))
        draw = ImageDraw.Draw(shown)
        for column, direction in enumerate(soldier.DIRECTIONS):
            x = (column % 4) * 256
            y = (column // 4) * 256
            shown.alpha_composite(
                soldier.frame(colored, column, row).resize(
                    (256, 256),
                    Image.Resampling.LANCZOS,
                ),
                (x, y),
            )
            draw.text(
                (x + 12, y + 10),
                direction,
                font=soldier.font(18, True),
                fill=(225, 188, 98, 255),
            )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=170,
        loop=0,
        disposal=2,
    )


def validate(
    original: Image.Image,
    enhanced: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    for name, atlas in (
        ("original", original),
        ("enhanced", enhanced),
        ("neutral", neutral),
        ("mask", mask),
    ):
        if atlas.size != ATLAS_SIZE:
            raise AssertionError(f"{name} atlas size is {atlas.size}")
    if ImageChops.difference(
        original.getchannel("A"),
        enhanced.getchannel("A"),
    ).getbbox():
        raise AssertionError("quality pass changed trooper poses")
    if ImageChops.difference(
        enhanced.getchannel("A"),
        neutral.getchannel("A"),
    ).getbbox():
        raise AssertionError("faction neutralization changed trooper poses")

    unique: set[bytes] = set()
    bounds: list[list[list[int]]] = []
    for row in range(4):
        row_bounds = []
        for column in range(8):
            sprite = soldier.frame(neutral, column, row)
            alpha = sprite.getchannel("A")
            box = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
            if box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if box[0] < 2 or box[1] < 2 or box[2] > 126 or box[3] > 126:
                raise AssertionError(
                    f"frame touches boundary {column},{row}: {box}"
                )
            if soldier.component_count(alpha) != 1:
                raise AssertionError(
                    f"detached artifact in frame {column},{row}"
                )
            row_bounds.append(list(box))
            unique.add(sprite.tobytes())
        bounds.append(row_bounds)
    if len(unique) != 32:
        raise AssertionError(f"expected 32 unique frames, got {len(unique)}")

    for column, direction in enumerate(soldier.DIRECTIONS):
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
    enhanced_rgba = np.asarray(enhanced.convert("RGBA"), dtype=np.uint8)
    enhanced_rgb = enhanced_rgba[:, :, :3]
    enhanced_alpha = enhanced_rgba[:, :, 3]
    white_edge_pixels = int(
        np.count_nonzero(
            (enhanced_alpha > 0)
            & (enhanced_alpha < 225)
            & (np.min(enhanced_rgb, axis=2) > 185)
        )
    )
    if white_edge_pixels:
        raise AssertionError(
            f"white matte remains on {white_edge_pixels} edge pixels"
        )
    return {
        "resource_id": RESOURCE_ID,
        "resource": RESOURCE_NAME,
        "source_size": list(SOURCE_SIZE),
        "source_grid": [8, 4],
        "source_cell": [360, 360],
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME_SIZE),
        "atlas_size": list(ATLAS_SIZE),
        "direction_order": list(soldier.DIRECTIONS),
        "animation_rows": list(soldier.ROW_LABELS),
        "target_height_hd4": TARGET_HEIGHT,
        "individual_height_logical": TARGET_HEIGHT // 4,
        "unique_frames": len(unique),
        "frame_bounds": bounds,
        "mask_pixels": mask_pixels,
        "white_edge_pixels": white_edge_pixels,
        "detached_artifacts": 0,
        "pose_geometry_changed": False,
        "alpha_pixels_changed": 0,
    }


def main() -> None:
    for required in (INPUT, CLASSIC):
        if not required.is_file():
            raise FileNotFoundError(required)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(INPUT, SOURCE_COPY)
    source = Image.open(SOURCE_COPY).convert("RGBA")
    if source.size != SOURCE_SIZE:
        raise AssertionError(f"unexpected source size {source.size}")
    classic = Image.open(CLASSIC).convert("RGBA")
    if classic.size != (256, 128):
        raise AssertionError(f"unexpected classic size {classic.size}")

    original = build_colored_atlas(source, classic)
    cleaned = clean_translucent_edge_colors(original)
    enhanced = clean_translucent_edge_colors(
        enhance_squad_details(cleaned)
    )
    neutral, mask = soldier.build_neutral_and_mask(enhanced)
    validation = validate(original, enhanced, neutral, mask)
    red = soldier.apply_engine_tint(
        neutral,
        mask,
        soldier.HOUSE_COLORS["Харконнены"],
    )
    blue = soldier.apply_engine_tint(
        neutral,
        mask,
        soldier.HOUSE_COLORS["Атрейдесы"],
    )
    green = soldier.apply_engine_tint(
        neutral,
        mask,
        soldier.HOUSE_COLORS["Ордос"],
    )

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    soldier.downscale_atlas(neutral).save(HD2_OUT, optimize=True)
    red.save(RED_OUT, optimize=True)
    blue.save(BLUE_OUT, optimize=True)
    green.save(GREEN_OUT, optimize=True)
    build_review(red).save(REVIEW_OUT, optimize=True)
    build_animation(red)

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source": str(SOURCE_COPY),
        "classic_contract": str(CLASSIC),
        "operation": (
            "exact 8x4 extraction, largest-component artifact removal, "
            "premultiplied-alpha Lanczos resize, nearest-opaque edge-color "
            "reconstruction, alpha-locked HD material enhancement, "
            "fixed-height classic-anchor placement, faction-mask build"
        ),
        "image_generation": (
            "not used because the supplied 32 poses must remain exact; "
            "deterministic alpha-locked restoration"
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
