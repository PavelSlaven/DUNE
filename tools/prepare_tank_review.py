#!/usr/bin/env python3
"""Build approval-ready HD4 combat-tank body and turret atlases."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "tank_review_v1"
BODY_SOURCE = OUTPUT / "tankbase_alpha.png"
BODY_NORTH = OUTPUT / "tankbase_N_alpha_v2.png"
BODY_NORTH_EAST = OUTPUT / "tankbase_NE_alpha_v2.png"
BODY_NORTH_WEST = OUTPUT / "tankbase_NW_alpha_v2.png"
BODY_WEST = OUTPUT / "tankbase_W_alpha_v2.png"
TOP_SOURCE = OUTPUT / "tanktop_alpha.png"
CLASSIC_BODY = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0159_UNIT_TANKBASE.png"
)
CLASSIC_TOP = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0161_UNIT_TANKTOP.png"
)

FRAME = (128, 128)
ATLAS = (1024, 128)
GRID = (4, 2)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
DIRECTION_VECTORS = (
    (1.0, 0.0),
    (2**-0.5, -(2**-0.5)),
    (0.0, -1.0),
    (-(2**-0.5), -(2**-0.5)),
    (-1.0, 0.0),
    (-(2**-0.5), 2**-0.5),
    (0.0, 1.0),
    (2**-0.5, 2**-0.5),
)
PIVOT = (64, 64)
# Preserve the classic directional proportions while retaining a safe
# transparent border for linear filtering inside each 128x128 HD4 cell.
CLASSIC_EXTENT_SCALE = 0.90

BODY_OUT = OUTPUT / "UNIT_TANKBASE_HD4_PREVIEW.png"
BODY_MASK_OUT = OUTPUT / "HM_UNIT_TANKBASE_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "UNIT_TANKBASE_SHADOW_HD4_PREVIEW.png"
TOP_OUT = OUTPUT / "UNIT_TANKTOP_HD4_PREVIEW.png"
TOP_MASK_OUT = OUTPUT / "HM_UNIT_TANKTOP_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_TANK_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_TANK_TURRET_ROTATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def clean_alpha(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    transparent = rgba[:, :, 3] < 4
    rgba[transparent] = 0
    weak_magenta = (
        (rgba[:, :, 3] < 128)
        & (rgba[:, :, 0] > 170)
        & (rgba[:, :, 2] > 150)
        & (rgba[:, :, 1] < 90)
    )
    rgba[weak_magenta] = 0
    return Image.fromarray(rgba, "RGBA")


def grid_frames(image: Image.Image) -> list[Image.Image]:
    image = clean_alpha(image)
    cell_width = image.width // GRID[0]
    cell_height = image.height // GRID[1]
    frames = []
    for row in range(GRID[1]):
        for column in range(GRID[0]):
            frame = image.crop(
                (
                    column * cell_width,
                    row * cell_height,
                    (column + 1) * cell_width,
                    (row + 1) * cell_height,
                )
            )
            alpha = np.asarray(
                frame.getchannel("A"),
                dtype=np.uint8,
            )
            labels, count = ndimage.label(alpha > 8)
            if count < 1:
                raise AssertionError("generated grid contains an empty cell")
            sizes = ndimage.sum(
                alpha > 8,
                labels,
                range(1, count + 1),
            )
            largest = int(np.argmax(sizes)) + 1
            keep = ndimage.binary_dilation(
                labels == largest,
                iterations=2,
            )
            rgba = np.asarray(frame, dtype=np.uint8).copy()
            rgba[~keep] = 0
            frames.append(Image.fromarray(rgba, "RGBA"))
    return frames


def single_subject(image: Image.Image) -> Image.Image:
    image = clean_alpha(image)
    alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
    labels, count = ndimage.label(alpha > 8)
    if count < 1:
        raise AssertionError("generated direction contains no tank body")
    sizes = ndimage.sum(alpha > 8, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    keep = ndimage.binary_dilation(labels == largest, iterations=2)
    rgba = np.asarray(image, dtype=np.uint8).copy()
    rgba[~keep] = 0
    return Image.fromarray(rgba, "RGBA")


def body_direction_frames(image: Image.Image) -> list[Image.Image]:
    generated = grid_frames(image)
    # The original generation contains four correct camera-facing views.
    # The other four must be independently rendered: rotating a fixed-camera
    # sprite by 180 degrees also rotates its perspective and puts the tracks
    # above the hull.
    east, south_west, south, south_east = generated[:4]
    return [
        east,
        single_subject(Image.open(BODY_NORTH_EAST).convert("RGBA")),
        single_subject(Image.open(BODY_NORTH).convert("RGBA")),
        single_subject(Image.open(BODY_NORTH_WEST).convert("RGBA")),
        single_subject(Image.open(BODY_WEST).convert("RGBA")),
        south_west,
        south,
        south_east,
    ]


def body_pivot(image: Image.Image) -> tuple[float, float]:
    alpha = np.asarray(image.getchannel("A"), dtype=np.uint8) > 32
    labels, count = ndimage.label(~alpha)
    candidates: list[tuple[int, float, float]] = []
    height, width = alpha.shape
    for label_id in range(1, count + 1):
        component = labels == label_id
        ys, xs = np.nonzero(component)
        if len(xs) < 80:
            continue
        if (
            np.any(xs == 0)
            or np.any(xs == width - 1)
            or np.any(ys == 0)
            or np.any(ys == height - 1)
        ):
            continue
        center_x = float(xs.mean())
        center_y = float(ys.mean())
        if (
            width * 0.25 < center_x < width * 0.75
            and height * 0.22 < center_y < height * 0.72
        ):
            candidates.append((len(xs), center_x, center_y))
    if candidates:
        _, center_x, center_y = max(candidates)
        return center_x, center_y
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("empty tank-body cell")
    return (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0


def visual_body_socket_center(
    frame: Image.Image,
) -> tuple[float, float]:
    """Find the dark turret socket inside its brighter metal annulus."""
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.float32)
    luminance = (
        rgba[:, :, 0] * 0.299
        + rgba[:, :, 1] * 0.587
        + rgba[:, :, 2] * 0.114
    )
    alpha = rgba[:, :, 3] > 32
    yy, xx = np.mgrid[: frame.height, : frame.width]
    best: tuple[float, float, float] | None = None
    for center_y in range(42, 79):
        for center_x in range(48, 81):
            inner_radius = (
                ((xx - center_x) / 12.0) ** 2
                + ((yy - center_y) / 8.0) ** 2
            )
            outer_radius = (
                ((xx - center_x) / 22.0) ** 2
                + ((yy - center_y) / 14.0) ** 2
            )
            inner = (inner_radius <= 1.0) & alpha
            annulus = (
                (inner_radius > 1.0)
                & (outer_radius <= 1.0)
                & alpha
            )
            if np.count_nonzero(inner) < 100:
                continue
            if np.count_nonzero(annulus) < 200:
                continue
            score = (
                float(luminance[annulus].mean())
                - float(luminance[inner].mean())
                - abs(center_x - PIVOT[0]) * 0.15
            )
            candidate = (score, float(center_x), float(center_y))
            if best is None or candidate[0] > best[0]:
                best = candidate
    if best is None:
        raise AssertionError("unable to locate the visible turret socket")
    return best[1], best[2]


def turret_pivot(image: Image.Image) -> tuple[float, float]:
    alpha = np.asarray(image.getchannel("A"), dtype=np.uint8) > 48
    if not np.any(alpha):
        raise AssertionError("empty tank-turret cell")
    distance = ndimage.distance_transform_edt(alpha)
    threshold = distance.max() * 0.82
    core = distance >= threshold
    ys, xs = np.nonzero(core)
    return float(xs.mean()), float(ys.mean())


def assemble(
    source_frames: list[Image.Image],
    pivots: list[tuple[float, float]],
    normalize_each: bool = False,
) -> Image.Image:
    extents = []
    for frame, (pivot_x, pivot_y) in zip(
        source_frames,
        pivots,
        strict=True,
    ):
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise AssertionError("generated atlas contains an empty cell")
        extents.append(
            (
                pivot_x - box[0],
                box[2] - pivot_x,
                pivot_y - box[1],
                box[3] - pivot_y,
            )
        )
    max_left = max(item[0] for item in extents)
    max_right = max(item[1] for item in extents)
    max_top = max(item[2] for item in extents)
    max_bottom = max(item[3] for item in extents)
    margin = 5
    common_scale = min(
        (PIVOT[0] - margin) / max_left,
        (FRAME[0] - PIVOT[0] - margin) / max_right,
        (PIVOT[1] - margin) / max_top,
        (FRAME[1] - PIVOT[1] - margin) / max_bottom,
    )
    atlas = Image.new("RGBA", ATLAS)
    for index, (frame, (pivot_x, pivot_y)) in enumerate(
        zip(source_frames, pivots, strict=True)
    ):
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise AssertionError("generated atlas contains an empty cell")
        if normalize_each:
            left = pivot_x - box[0]
            right = box[2] - pivot_x
            top = pivot_y - box[1]
            bottom = box[3] - pivot_y
            scale = min(
                (PIVOT[0] - margin) / left,
                (FRAME[0] - PIVOT[0] - margin) / right,
                (PIVOT[1] - margin) / top,
                (FRAME[1] - PIVOT[1] - margin) / bottom,
            )
        else:
            scale = common_scale
        subject = frame.crop(box)
        size = (
            max(1, round(subject.width * scale)),
            max(1, round(subject.height * scale)),
        )
        subject = subject.resize(size, Image.Resampling.LANCZOS)
        pivot_in_crop = (
            (pivot_x - box[0]) * scale,
            (pivot_y - box[1]) * scale,
        )
        position = (
            round(index * FRAME[0] + PIVOT[0] - pivot_in_crop[0]),
            round(PIVOT[1] - pivot_in_crop[1]),
        )
        atlas.alpha_composite(subject, position)
    return clean_alpha(atlas)


def smoothstep(
    low: float,
    high: float,
    value: np.ndarray,
) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def neutral_and_mask(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, i] for i in range(4))
    dominance = (green - np.maximum(red, blue)) / 255.0
    purity = (green - np.maximum(red, blue)) / np.maximum(green, 1.0)
    selection = (
        smoothstep(0.025, 0.18, dominance)
        * smoothstep(0.06, 0.40, purity)
        * smoothstep(20.0, 70.0, green)
        * (alpha / 255.0)
    )
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    target = np.dstack(
        (luminance * 0.72, luminance * 0.78, luminance * 0.86)
    )
    amount = np.clip(selection * 1.35, 0.0, 1.0)[:, :, None]
    neutral = rgba.copy()
    neutral[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - amount) + target * amount
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


def build_shadow(body: Image.Image) -> Image.Image:
    shadow = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas_frame(body, index)
        alpha = frame.getchannel("A").filter(
            ImageFilter.GaussianBlur(1.8)
        ).point(lambda value: round(value * 0.20))
        silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
        silhouette.putalpha(alpha)
        shadow.alpha_composite(
            silhouette,
            (index * FRAME[0] + 4, 4),
        )
    return shadow


def atlas_frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop(
        (
            index * FRAME[0],
            0,
            (index + 1) * FRAME[0],
            FRAME[1],
        )
    )


def classic_atlas_frame(
    atlas: Image.Image,
    index: int,
) -> Image.Image:
    return atlas.crop((index * 32, 0, (index + 1) * 32, 32))


def oriented_extents(
    image: Image.Image,
    direction_index: int,
) -> tuple[float, float]:
    alpha = np.asarray(image.convert("RGBA"))[:, :, 3]
    yy, xx = np.nonzero(alpha > 24)
    if xx.size == 0:
        raise AssertionError("empty tank frame")
    dx, dy = DIRECTION_VECTORS[direction_index]
    offset_x = xx - image.width / 2.0
    offset_y = yy - image.height / 2.0
    forward = offset_x * dx + offset_y * dy
    lateral = -offset_x * dy + offset_y * dx
    return (
        float(forward.max() - forward.min() + 1.0),
        float(lateral.max() - lateral.min() + 1.0),
    )


def transform_frame_axes(
    frame: Image.Image,
    direction_index: int,
    forward_scale: float,
    lateral_scale: float,
) -> Image.Image:
    dx, dy = DIRECTION_VECTORS[direction_index]
    inverse_forward = 1.0 / forward_scale
    inverse_lateral = 1.0 / lateral_scale
    a = inverse_forward * dx * dx + inverse_lateral * dy * dy
    b = (inverse_forward - inverse_lateral) * dx * dy
    d = b
    e = inverse_forward * dy * dy + inverse_lateral * dx * dx
    c = PIVOT[0] - a * PIVOT[0] - b * PIVOT[1]
    f = PIVOT[1] - d * PIVOT[0] - e * PIVOT[1]
    return frame.transform(
        FRAME,
        Image.Transform.AFFINE,
        (a, b, c, d, e, f),
        resample=Image.Resampling.BICUBIC,
    )


def normalize_atlas_to_classic(
    atlas: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    normalized = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas_frame(atlas, index)
        target_forward, target_lateral = oriented_extents(
            classic_atlas_frame(classic, index),
            index,
        )
        target_forward *= 4.0 * CLASSIC_EXTENT_SCALE
        target_lateral *= 4.0 * CLASSIC_EXTENT_SCALE
        for _ in range(3):
            current_forward, current_lateral = oriented_extents(
                frame,
                index,
            )
            frame = transform_frame_axes(
                frame,
                index,
                target_forward / current_forward,
                target_lateral / current_lateral,
            )
        normalized.alpha_composite(
            clean_alpha(frame),
            (index * FRAME[0], 0),
        )
    return clean_alpha(normalized)


def turret_hub_center(frame: Image.Image) -> tuple[float, float]:
    alpha = np.asarray(frame.convert("RGBA"))[:, :, 3] > 24
    core = ndimage.binary_erosion(alpha, iterations=7)
    labels, count = ndimage.label(core)
    if count < 1:
        raise AssertionError("unable to isolate tank turret hub")
    sizes = ndimage.sum(core, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    center_y, center_x = ndimage.center_of_mass(core, labels, largest)
    return float(center_x), float(center_y)


def center_turret_hubs(atlas: Image.Image) -> Image.Image:
    centered = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas_frame(atlas, index)
        center_x, center_y = turret_hub_center(frame)
        shift_x = PIVOT[0] - center_x
        shift_y = PIVOT[1] - center_y
        shifted = frame.transform(
            FRAME,
            Image.Transform.AFFINE,
            (1.0, 0.0, -shift_x, 0.0, 1.0, -shift_y),
            resample=Image.Resampling.BICUBIC,
        )
        centered.alpha_composite(
            clean_alpha(shifted),
            (index * FRAME[0], 0),
        )
    return clean_alpha(centered)


def center_body_turret_sockets(atlas: Image.Image) -> Image.Image:
    centered = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas_frame(atlas, index)
        center_x, center_y = visual_body_socket_center(frame)
        shift_x = PIVOT[0] - center_x
        shift_y = PIVOT[1] - center_y
        shifted = frame.transform(
            FRAME,
            Image.Transform.AFFINE,
            (1.0, 0.0, -shift_x, 0.0, 1.0, -shift_y),
            resample=Image.Resampling.BICUBIC,
        )
        box = shifted.getchannel("A").getbbox()
        if box is None:
            raise AssertionError("empty centered tank-body frame")
        margin = 2
        left = PIVOT[0] - box[0]
        right = box[2] - PIVOT[0]
        top = PIVOT[1] - box[1]
        bottom = box[3] - PIVOT[1]
        scale = min(
            1.0,
            (PIVOT[0] - margin) / max(left, 1),
            (FRAME[0] - PIVOT[0] - margin) / max(right, 1),
            (PIVOT[1] - margin) / max(top, 1),
            (FRAME[1] - PIVOT[1] - margin) / max(bottom, 1),
        )
        if scale < 1.0:
            inverse = 1.0 / scale
            shifted = shifted.transform(
                FRAME,
                Image.Transform.AFFINE,
                (
                    inverse,
                    0.0,
                    PIVOT[0] * (1.0 - inverse),
                    0.0,
                    inverse,
                    PIVOT[1] * (1.0 - inverse),
                ),
                resample=Image.Resampling.BICUBIC,
            )
        for _ in range(3):
            final_center_x, final_center_y = visual_body_socket_center(
                shifted
            )
            correction_x = round(PIVOT[0] - final_center_x)
            correction_y = round(PIVOT[1] - final_center_y)
            if not correction_x and not correction_y:
                break
            shifted = shifted.transform(
                FRAME,
                Image.Transform.AFFINE,
                (
                    1.0,
                    0.0,
                    -correction_x,
                    0.0,
                    1.0,
                    -correction_y,
                ),
                resample=Image.Resampling.BICUBIC,
            )
        centered.alpha_composite(
            clean_alpha(shifted),
            (index * FRAME[0], 0),
        )
    return clean_alpha(centered)


def apply_engine_tint(
    image: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32).copy()
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    strength = (
        mask_rgba[:, :, 3] / 255.0
        * np.max(mask_rgba[:, :, :3], axis=2) / 255.0
    )
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        colored = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - strength)
            + colored * strength
        )
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def composed_frame(
    body: Image.Image,
    body_mask: Image.Image,
    top: Image.Image,
    top_mask: Image.Image,
    body_direction: int,
    top_direction: int,
    color: tuple[int, int, int],
) -> Image.Image:
    tinted_body = apply_engine_tint(body, body_mask, color)
    tinted_top = apply_engine_tint(top, top_mask, color)
    result = atlas_frame(tinted_body, body_direction)
    result.alpha_composite(atlas_frame(tinted_top, top_direction))
    return result


def draw_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    size: int,
    label: str,
) -> None:
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle(
        (x, y, x + size, y + size + 36),
        radius=7,
        fill=(22, 26, 31, 255),
        outline=(138, 105, 48, 255),
        width=2,
    )
    board.alpha_composite(
        sprite.resize((size, size), Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.text(
        (x + 8, y + size + 6),
        label,
        font=font(17, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    body: Image.Image,
    body_mask: Image.Image,
    top: Image.Image,
    top_mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1780, 1300), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Боевой танк — корпус и вращающаяся башня",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 70),
        "HD4: два независимых атласа 8×1, кадр 128×128",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    for index, direction in enumerate(DIRECTIONS):
        draw_card(
            board,
            composed_frame(
                body,
                body_mask,
                top,
                top_mask,
                index,
                index,
                HOUSE_COLORS["Ордос"],
            ),
            34 + index * 216,
            112,
            190,
            direction,
        )

    draw.text(
        (34, 355),
        "Независимый поворот башни — корпус направлен на север",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, direction in enumerate(DIRECTIONS):
        draw_card(
            board,
            composed_frame(
                body,
                body_mask,
                top,
                top_mask,
                2,
                index,
                HOUSE_COLORS["Атрейдесы"],
            ),
            34 + index * 216,
            405,
            190,
            direction,
        )

    draw.text(
        (34, 648),
        "Цветовые маски Домов",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for column, (name, color) in enumerate(HOUSE_COLORS.items()):
        draw_card(
            board,
            composed_frame(
                body,
                body_mask,
                top,
                top_mask,
                7,
                2,
                color,
            ),
            34 + column * 318,
            698,
            280,
            name,
        )
    draw_card(
        board,
        atlas_frame(body_mask, 2),
        988,
        698,
        280,
        "маска корпуса",
    )
    draw_card(
        board,
        atlas_frame(top_mask, 2),
        1306,
        698,
        280,
        "маска башни",
    )

    draw.text(
        (34, 1035),
        "Исходный контракт 32×32 → мастер HD4 128×128",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic_body = Image.open(CLASSIC_BODY).convert("RGBA")
    classic_top = Image.open(CLASSIC_TOP).convert("RGBA")
    classic = atlas_frame(
        classic_body.resize(ATLAS, Image.Resampling.NEAREST),
        2,
    )
    classic.alpha_composite(
        atlas_frame(
            classic_top.resize(ATLAS, Image.Resampling.NEAREST),
            2,
        )
    )
    draw_card(board, classic, 34, 1080, 180, "классика N")
    draw_card(
        board,
        composed_frame(
            body,
            body_mask,
            top,
            top_mask,
            2,
            2,
            HOUSE_COLORS["Ордос"],
        ),
        250,
        1080,
        180,
        "HD4 N",
    )
    draw.text(
        (480, 1100),
        "• порядок E, NE, N, NW, W, SW, S, SE\n"
        "• единый центр вращения 16×16 логических пикселей\n"
        "• корпус, башня, маски и тень разделены\n"
        "• передние и задние ракурсы не зеркальные",
        font=font(22),
        fill=(204, 208, 213, 255),
        spacing=14,
    )
    draw.text(
        (34, 1268),
        "Предварительный просмотр — в игру не установлено.",
        font=font(19),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(
    body: Image.Image,
    body_mask: Image.Image,
    top: Image.Image,
    top_mask: Image.Image,
) -> None:
    frames = []
    for direction in range(8):
        sprite = composed_frame(
            body,
            body_mask,
            top,
            top_mask,
            2,
            direction,
            HOUSE_COLORS["Ордос"],
        )
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            sprite.resize((512, 512), Image.Resampling.LANCZOS)
        )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=180,
        loop=0,
        disposal=2,
    )


def validate(
    body: Image.Image,
    body_mask: Image.Image,
    shadow: Image.Image,
    top: Image.Image,
    top_mask: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("body", body),
        ("body mask", body_mask),
        ("shadow", shadow),
        ("turret", top),
        ("turret mask", top_mask),
    ):
        if image.size != ATLAS:
            raise AssertionError(f"{name} atlas dimensions changed")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} atlas is empty")
    for name, image in (("body", body), ("turret", top)):
        frames = [atlas_frame(image, index) for index in range(8)]
        if len({frame.tobytes() for frame in frames}) != 8:
            raise AssertionError(f"{name} directions are not unique")
        for index, frame in enumerate(frames):
            box = frame.getchannel("A").getbbox()
            if (
                box is None
                or box[0] < 2
                or box[1] < 2
                or box[2] > 126
                or box[3] > 126
            ):
                raise AssertionError(
                    f"{name} frame {index} touches its boundary: {box}"
                )
        if name == "body":
            for index in range(4):
                opposite = frames[index + 4].transpose(
                    Image.Transpose.ROTATE_180
                )
                if frames[index].tobytes() == opposite.tobytes():
                    raise AssertionError(
                        "body opposite direction is a rotated raster: "
                        f"{DIRECTIONS[index]}"
                    )
    return {
        "resources": {
            "body": {"id": 159, "name": "UNIT_TANKBASE"},
            "shadow": {"id": 160, "name": "UNIT_TANKBASE_SHADOW"},
            "turret": {"id": 161, "name": "UNIT_TANKTOP"},
        },
        "direction_order": list(DIRECTIONS),
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "body_frames": 8,
        "turret_frames": 8,
        "body_mask_pixels": int(
            np.count_nonzero(
                np.asarray(body_mask.getchannel("A"), dtype=np.uint8) > 8
            )
        ),
        "turret_mask_pixels": int(
            np.count_nonzero(
                np.asarray(top_mask.getchannel("A"), dtype=np.uint8) > 8
            )
        ),
        "pivot_hd4": list(PIVOT),
        "pivot_logical": [16, 16],
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    body_cells = body_direction_frames(
        Image.open(BODY_SOURCE).convert("RGBA")
    )
    top_cells = grid_frames(Image.open(TOP_SOURCE).convert("RGBA"))
    body = assemble(
        body_cells,
        [body_pivot(cell) for cell in body_cells],
        normalize_each=True,
    )
    top = assemble(top_cells, [turret_pivot(cell) for cell in top_cells])
    body = normalize_atlas_to_classic(
        body,
        Image.open(CLASSIC_BODY).convert("RGBA"),
    )
    body = center_body_turret_sockets(body)
    top = normalize_atlas_to_classic(
        top,
        Image.open(CLASSIC_TOP).convert("RGBA"),
    )
    top = center_turret_hubs(top)
    neutral_body, body_mask = neutral_and_mask(body)
    neutral_top, top_mask = neutral_and_mask(top)
    shadow = build_shadow(neutral_body)
    validation = validate(
        neutral_body,
        body_mask,
        shadow,
        neutral_top,
        top_mask,
    )

    neutral_body.save(BODY_OUT, optimize=True)
    body_mask.save(BODY_MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    neutral_top.save(TOP_OUT, optimize=True)
    top_mask.save(TOP_MASK_OUT, optimize=True)
    neutral_body.resize((512, 64), Image.Resampling.LANCZOS).save(
        OUTPUT / "UNIT_TANKBASE_HD2_PREVIEW.png",
        optimize=True,
    )
    neutral_top.resize((512, 64), Image.Resampling.LANCZOS).save(
        OUTPUT / "UNIT_TANKTOP_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(
        neutral_body,
        body_mask,
        neutral_top,
        top_mask,
    ).save(REVIEW_OUT, optimize=True)
    build_animation(
        neutral_body,
        body_mask,
        neutral_top,
        top_mask,
    )
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "body_source": str(BODY_SOURCE),
        "turret_source": str(TOP_SOURCE),
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
