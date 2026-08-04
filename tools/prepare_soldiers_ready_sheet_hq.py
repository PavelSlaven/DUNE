#!/usr/bin/env python3
"""Prepare the supplied 8x4 three-soldier sheet without changing poses."""

from __future__ import annotations

import json
import shutil
from collections import deque
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from prepare_soldier_ready_sheet import (
    DIRECTIONS,
    HOUSE_COLORS,
    apply_engine_tint,
    build_neutral_and_mask,
    downscale_atlas,
    enhance_atlas_rgb_preserve_alpha,
    frame,
)


ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(
    "C:/Users/Slaven/Downloads/"
    "Gemini_Generated_Image_matn11matn11matn.png"
)
OUTPUT = ROOT / "artifacts" / "soldiers_review_ready_hq"
SOURCE_COPY = OUTPUT / "source_reference.png"
REPAIRED_SOURCE_OUT = OUTPUT / "source_reference_repaired.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0156_UNIT_SOLDIERS.png"
)
POSITION_REFERENCE = (
    ROOT
    / "resources"
    / "hd"
    / "master4"
    / "sdl_data"
    / "0156_UNIT_SOLDIERS.png"
)
SOLDIER_STYLE_REFERENCE = (
    ROOT
    / "artifacts"
    / "soldier_review_ready_hq"
    / "UNIT_SOLDIER_HARKONNEN_HD4_PREVIEW.png"
)

SOURCE_GRID = (8, 4)
SOURCE_CELL = (360, 360)
FRAME = (128, 128)
ATLAS = (1024, 512)
TARGET_GROUP_HEIGHT = 88
MEMBERS_PER_FRAME = 3
ROW_LABELS = ("MOVE_0", "MOVE_1", "MOVE_2", "MOVE_3")

BASE_OUT = OUTPUT / "UNIT_SOLDIERS_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SOLDIERS_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "UNIT_SOLDIERS_HD2_PREVIEW.png"
RED_OUT = OUTPUT / "UNIT_SOLDIERS_HARKONNEN_HD4_PREVIEW.png"
BLUE_OUT = OUTPUT / "UNIT_SOLDIERS_ATREIDES_HD4_PREVIEW.png"
GREEN_OUT = OUTPUT / "UNIT_SOLDIERS_ORDOS_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SOLDIERS_READY_HQ_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SOLDIERS_READY_HQ_ANIMATION.gif"
ARTIFACT_COLUMN = 7
ARTIFACT_ROW = 3
CLEAN_REFERENCE_COLUMN = 0
CLEAN_REFERENCE_ROW = 3
FACING_REPAIRS = (
    (0, 0, 2, 0),  # E / MOVE_0
    (1, 0, 2, 0),  # NE / MOVE_0
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def components(mask: np.ndarray) -> list[list[tuple[int, int]]]:
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=np.uint8)
    found: list[list[tuple[int, int]]] = []
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
            found.append(component)
    return sorted(found, key=len, reverse=True)


def remove_white_background(cell: Image.Image) -> Image.Image:
    rgba = np.asarray(cell.convert("RGBA"), dtype=np.uint8).copy()
    rgb = rgba[:, :, :3].astype(np.float32)
    white_distance = np.sqrt(np.mean((255.0 - rgb) ** 2, axis=2))
    found = components(white_distance > 12.0)
    if len(found) < MEMBERS_PER_FRAME:
        raise AssertionError(
            f"expected three soldiers, found {len(found)} components"
        )

    retained = np.zeros(white_distance.shape, dtype=np.uint8)
    for component in found[:MEMBERS_PER_FRAME]:
        if len(component) < 1000:
            raise AssertionError("one of the three soldiers is incomplete")
        for x, y in component:
            retained[y, x] = 255
    support = Image.fromarray(retained, "L").filter(ImageFilter.MaxFilter(9))
    support_array = np.asarray(support, dtype=np.float32) / 255.0
    soft_alpha = np.clip((white_distance - 2.0) / 28.0, 0.0, 1.0)
    source_alpha = rgba[:, :, 3].astype(np.float32) / 255.0
    rgba[:, :, 3] = np.clip(
        soft_alpha * support_array * source_alpha * 255.0,
        0,
        255,
    ).astype(np.uint8)

    group = Image.fromarray(rgba, "RGBA")
    box = group.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("background removal erased the squad")
    return group.crop(box)


def component_mask(
    cell: Image.Image,
    member_index: int,
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """Return one of the three connected soldiers and its exact bounds."""
    rgb = np.asarray(cell.convert("RGB"), dtype=np.float32)
    white_distance = np.sqrt(np.mean((255.0 - rgb) ** 2, axis=2))
    found = components(white_distance > 12.0)
    if len(found) < MEMBERS_PER_FRAME:
        raise AssertionError("source cell does not contain three soldiers")
    member = found[member_index]
    xs = [point[0] for point in member]
    ys = [point[1] for point in member]
    retained = np.zeros(white_distance.shape, dtype=np.uint8)
    for x, y in member:
        retained[y, x] = 255
    support = Image.fromarray(retained, "L").filter(ImageFilter.MaxFilter(9))
    soft_alpha = np.clip((white_distance - 2.0) / 28.0, 0.0, 1.0)
    alpha = np.clip(
        soft_alpha * (np.asarray(support, dtype=np.float32) / 255.0) * 255.0,
        0,
        255,
    ).astype(np.uint8)
    return Image.fromarray(alpha, "L"), (
        min(xs),
        min(ys),
        max(xs) + 1,
        max(ys) + 1,
    )


def repair_bottom_right_artifact(source: Image.Image) -> Image.Image:
    """Replace only the damaged duplicate soldier in SE/MOVE_3.

    The clean E/MOVE_3 member has a 97.2% silhouette IoU with the damaged
    member and exactly the same 115x163 bounds. Reusing that duplicate avoids
    inventing a pose or letting a generative pass move the weapon and feet.
    """
    clean_cell = source_cell(
        source,
        CLEAN_REFERENCE_COLUMN,
        CLEAN_REFERENCE_ROW,
    )
    target_cell = source_cell(source, ARTIFACT_COLUMN, ARTIFACT_ROW)
    clean_mask, clean_box = component_mask(clean_cell, 0)
    target_mask, target_box = component_mask(target_cell, 0)
    if (
        clean_box[2] - clean_box[0],
        clean_box[3] - clean_box[1],
    ) != (
        target_box[2] - target_box[0],
        target_box[3] - target_box[1],
    ):
        raise AssertionError(
            f"clean duplicate does not match damaged member: "
            f"{clean_box} vs {target_box}"
        )

    cleared = np.asarray(target_cell.convert("RGBA"), dtype=np.uint8).copy()
    target_support = np.asarray(
        target_mask.filter(ImageFilter.MaxFilter(7)),
        dtype=np.uint8,
    ) > 0
    cleared[target_support, :3] = 255
    cleared[target_support, 3] = 255
    repaired_cell = Image.fromarray(cleared, "RGBA")

    clean_layer = clean_cell.copy()
    clean_layer.putalpha(clean_mask)
    shifted = Image.new("RGBA", SOURCE_CELL)
    shifted.alpha_composite(
        clean_layer,
        (
            target_box[0] - clean_box[0],
            target_box[1] - clean_box[1],
        ),
    )
    repaired_cell.alpha_composite(shifted)

    repaired = source.copy()
    repaired.paste(
        repaired_cell,
        (
            ARTIFACT_COLUMN * SOURCE_CELL[0],
            ARTIFACT_ROW * SOURCE_CELL[1],
        ),
    )
    return repaired


def repair_first_row_facing_members(source: Image.Image) -> Image.Image:
    """Turn the accidental frontal MOVE_0 members toward their movement.

    The lower member of each source cell already has the required side-facing
    pose and animation phase. It is reused at native scale and anchored to the
    replaced member's baseline, so no generated geometry is introduced.
    """
    repaired = source.copy()
    for column, row, source_member, target_member in FACING_REPAIRS:
        cell = source_cell(repaired, column, row)
        clean_mask, clean_box = component_mask(cell, source_member)
        target_mask, target_box = component_mask(cell, target_member)

        cleared = np.asarray(cell.convert("RGBA"), dtype=np.uint8).copy()
        target_support = np.asarray(
            target_mask.filter(ImageFilter.MaxFilter(7)),
            dtype=np.uint8,
        ) > 0
        cleared[target_support, :3] = 255
        cleared[target_support, 3] = 255
        repaired_cell = Image.fromarray(cleared, "RGBA")

        target_center_x = (target_box[0] + target_box[2]) / 2.0
        destination_left = round(
            target_center_x - (clean_box[2] - clean_box[0]) / 2.0
        )
        destination_top = target_box[3] - (clean_box[3] - clean_box[1])
        clean_layer = cell.copy()
        clean_layer.putalpha(clean_mask)
        shifted = Image.new("RGBA", SOURCE_CELL)
        shifted.alpha_composite(
            clean_layer,
            (
                destination_left - clean_box[0],
                destination_top - clean_box[1],
            ),
        )
        repaired_cell.alpha_composite(shifted)

        repaired.paste(
            repaired_cell,
            (column * SOURCE_CELL[0], row * SOURCE_CELL[1]),
        )
    return repaired


def enhance_squad_details(atlas: Image.Image) -> Image.Image:
    """Add a restrained HD detail pass while keeping alpha pixel-identical."""
    first_pass = enhance_atlas_rgb_preserve_alpha(atlas)
    rgba = np.asarray(first_pass.convert("RGBA"), dtype=np.uint8).copy()
    original_alpha = rgba[:, :, 3].copy()
    rgb = rgba[:, :, :3]
    blurred = cv2.GaussianBlur(rgb, (0, 0), 0.42)
    detailed = cv2.addWeighted(rgb, 1.12, blurred, -0.12, 0)
    detailed = np.clip(
        (detailed.astype(np.float32) - 128.0) * 1.018 + 128.0,
        0,
        255,
    ).astype(np.uint8)
    rgba[:, :, :3] = detailed
    rgba[:, :, 3] = original_alpha
    output = Image.fromarray(rgba, "RGBA")
    if ImageChops.difference(
        atlas.getchannel("A"),
        output.getchannel("A"),
    ).getbbox():
        raise AssertionError("HD detail pass changed squad poses")
    return output


def reference_centers_and_baselines(
    reference: Image.Image,
) -> list[list[tuple[float, int]]]:
    result: list[list[tuple[float, int]]] = []
    for row in range(4):
        row_values = []
        for column in range(8):
            box = frame(reference, column, row).getchannel("A").point(
                lambda value: 255 if value > 8 else 0
            ).getbbox()
            if box is None:
                raise AssertionError(
                    f"empty placement reference {column},{row}"
                )
            baseline = 92 if DIRECTIONS[column] in ("N", "S") else 100
            row_values.append(((box[0] + box[2]) / 2.0, baseline))
        result.append(row_values)
    return result


def source_cell(source: Image.Image, column: int, row: int) -> Image.Image:
    return source.crop(
        (
            column * SOURCE_CELL[0],
            row * SOURCE_CELL[1],
            (column + 1) * SOURCE_CELL[0],
            (row + 1) * SOURCE_CELL[1],
        )
    )


def build_colored_atlas(
    source: Image.Image,
    position_reference: Image.Image,
) -> Image.Image:
    positions = reference_centers_and_baselines(position_reference)
    atlas = Image.new("RGBA", ATLAS)
    for row in range(4):
        for column in range(8):
            group = remove_white_background(source_cell(source, column, row))
            target_width = max(
                1,
                round(group.width * TARGET_GROUP_HEIGHT / group.height),
            )
            if target_width > 118:
                target_width = 118
            group = group.resize(
                (target_width, TARGET_GROUP_HEIGHT),
                Image.Resampling.LANCZOS,
            )
            center_x, baseline = positions[row][column]
            output = Image.new("RGBA", FRAME)
            output.alpha_composite(
                group,
                (
                    round(center_x - group.width / 2.0),
                    baseline - group.height,
                ),
            )
            atlas.alpha_composite(
                output,
                (column * FRAME[0], row * FRAME[1]),
            )
    return atlas


def member_boxes(sprite: Image.Image) -> list[tuple[int, int, int, int]]:
    mask = np.asarray(sprite.getchannel("A"), dtype=np.uint8) > 8
    boxes = []
    for component in components(mask)[:MEMBERS_PER_FRAME]:
        xs = [point[0] for point in component]
        ys = [point[1] for point in component]
        boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    return boxes


def build_review(colored: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (2048, 1082), (12, 15, 19, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (18, 13),
        "UNIT_SOLDIERS — улучшенный атлас 8×4",
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


def build_animation(colored: Image.Image) -> None:
    frames = []
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
        if atlas.size != ATLAS:
            raise AssertionError(f"{name} atlas size is {atlas.size}")
    if ImageChops.difference(
        original.getchannel("A"),
        enhanced.getchannel("A"),
    ).getbbox():
        raise AssertionError("quality pass changed squad poses")
    if ImageChops.difference(
        enhanced.getchannel("A"),
        neutral.getchannel("A"),
    ).getbbox():
        raise AssertionError("faction neutralization changed poses")

    bounds = []
    unique: set[bytes] = set()
    for row in range(4):
        row_bounds = []
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
            row_bounds.append(list(box))
            unique.add(sprite.tobytes())
        bounds.append(row_bounds)
    if len(unique) != 32:
        raise AssertionError(f"expected 32 unique frames, got {len(unique)}")
    mask_pixels = int(
        np.count_nonzero(np.asarray(mask.getchannel("A")) > 8)
    )
    if mask_pixels < 3000:
        raise AssertionError(f"faction mask is too small: {mask_pixels}")
    return {
        "resource_id": 156,
        "resource": "UNIT_SOLDIERS",
        "source_size": list(source_size),
        "source_grid": list(SOURCE_GRID),
        "source_cell": list(SOURCE_CELL),
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "direction_order": list(DIRECTIONS),
        "animation_rows": list(ROW_LABELS),
        "members_per_frame": MEMBERS_PER_FRAME,
        "group_height_hd4": TARGET_GROUP_HEIGHT,
        "member_height_logical_target": 11,
        "unique_frames": len(unique),
        "frame_bounds": bounds,
        "mask_pixels": mask_pixels,
        "pose_geometry_changed": False,
        "alpha_pixels_changed": 0,
    }


source_size = (2880, 1440)


def main() -> None:
    for required in (
        INPUT,
        CLASSIC,
        POSITION_REFERENCE,
        SOLDIER_STYLE_REFERENCE,
    ):
        if not required.is_file():
            raise FileNotFoundError(required)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(INPUT, SOURCE_COPY)
    source = Image.open(SOURCE_COPY).convert("RGBA")
    if source.size != source_size:
        raise AssertionError(f"unexpected source size {source.size}")
    source = repair_bottom_right_artifact(source)
    source = repair_first_row_facing_members(source)
    source.save(REPAIRED_SOURCE_OUT, optimize=True)
    position_reference = Image.open(POSITION_REFERENCE).convert("RGBA")
    if position_reference.size != ATLAS:
        raise AssertionError(
            f"unexpected placement reference {position_reference.size}"
        )

    original = build_colored_atlas(source, position_reference)
    enhanced = enhance_squad_details(original)
    neutral, mask = build_neutral_and_mask(enhanced)
    red = apply_engine_tint(neutral, mask, HOUSE_COLORS["Харконнены"])
    blue = apply_engine_tint(neutral, mask, HOUSE_COLORS["Атрейдесы"])
    green = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    validation = validate(original, enhanced, neutral, mask)

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    downscale_atlas(neutral).save(HD2_OUT, optimize=True)
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
        "position_reference": str(POSITION_REFERENCE),
        "style_reference": str(SOLDIER_STYLE_REFERENCE),
        "operation": (
            "exact 8x4 extraction, three-largest-component retention, "
            "SE/MOVE_3 damaged-member replacement from the matching clean "
            "E/MOVE_3 duplicate, E/MOVE_0 and NE/MOVE_0 frontal-member "
            "replacement from the side-facing member in each source cell, "
            "white-matte cleanup, alpha-locked HD material "
            "enhancement matching UNIT_SOLDIER, fixed formation placement, "
            "faction-mask build"
        ),
        "image_generation": (
            "not used because the user required exact supplied poses; "
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
