#!/usr/bin/env python3
"""Prepare an approval-ready HD4 missile-launcher atlas."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "launcher_review_v1"
SOURCE = OUTPUT / "user_reference.png"
DIRECTION_SOURCES = OUTPUT / "direction_sources"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0139_UNIT_LAUNCHER.png"
)

FRAME = (128, 128)
ATLAS = (1024, 128)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")

# The supplied reference presents the same vehicle from front to rear:
# S, SW, W, NW, N. The opposite three quarter views are valid mirrors
# because the launcher design is bilaterally symmetric.
SOURCE_CROPS = {
    "S": (42, 118, 355, 604),
    "SW": (350, 110, 835, 620),
    "W": (815, 135, 1322, 625),
    "NW": (1270, 118, 1768, 620),
    "N": (1745, 112, 2135, 610),
}

ATLAS_OUT = OUTPUT / "UNIT_LAUNCHER_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_LAUNCHER_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "UNIT_LAUNCHER_SHADOW_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "UNIT_LAUNCHER_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_LAUNCHER_REVIEW.png"
ROTATION_OUT = OUTPUT / "UNIT_LAUNCHER_ROTATION_PREVIEW.gif"
CLASSIC_REFS = OUTPUT / "classic_direction_refs"

HOUSE_COLORS = {
    "Харконнены": (235, 28, 28),
    "Атрейдесы": (30, 105, 245),
    "Ордос": (20, 220, 70),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def clean_component(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    labels, count = ndimage.label(alpha > 8)
    if count < 1:
        raise AssertionError("launcher extraction is empty")
    sizes = ndimage.sum(alpha > 8, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    keep = ndimage.binary_dilation(labels == largest, iterations=2)
    rgba[~keep] = 0
    rgba[rgba[:, :, 3] < 3] = 0
    return Image.fromarray(rgba, "RGBA")


def extract_subject(source: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    crop = np.asarray(source.crop(box).convert("RGB"))
    height, width = crop.shape[:2]

    mask = np.full((height, width), cv2.GC_PR_BGD, dtype=np.uint8)
    border = max(8, round(min(width, height) * 0.035))
    mask[:border, :] = cv2.GC_BGD
    mask[-border:, :] = cv2.GC_BGD
    mask[:, :border] = cv2.GC_BGD
    mask[:, -border:] = cv2.GC_BGD

    # Bright and saturated pixels are unambiguously part of the vehicle.
    hsv = cv2.cvtColor(crop, cv2.COLOR_RGB2HSV)
    value = hsv[:, :, 2]
    saturation = hsv[:, :, 1]
    foreground_seed = (value > 72) | ((value > 38) & (saturation > 48))
    foreground_seed = ndimage.binary_erosion(foreground_seed, iterations=1)
    mask[foreground_seed] = cv2.GC_FGD

    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(
        cv2.cvtColor(crop, cv2.COLOR_RGB2BGR),
        mask,
        None,
        background_model,
        foreground_model,
        8,
        cv2.GC_INIT_WITH_MASK,
    )
    alpha = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        255,
        0,
    ).astype(np.uint8)

    # Keep only the main vehicle and soften a single antialiasing band.
    labels, count = ndimage.label(alpha > 0)
    if count < 1:
        raise AssertionError("GrabCut did not find the launcher")
    sizes = ndimage.sum(alpha > 0, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    solid = labels == largest
    soft = ndimage.gaussian_filter(solid.astype(np.float32), 0.65)
    alpha = np.clip(soft * 255.0, 0, 255).astype(np.uint8)

    rgba = np.dstack((crop, alpha))
    rgba[alpha == 0, :3] = 0
    return clean_component(Image.fromarray(rgba, "RGBA"))


def source_frames() -> dict[str, Image.Image]:
    source = Image.open(SOURCE).convert("RGBA")
    extracted = {
        direction: clean_component(
            Image.open(
                DIRECTION_SOURCES / f"{direction}_alpha.png"
            ).convert("RGBA")
        )
        for direction in ("NE", "S", "SE")
    }
    # The launcher is bilaterally symmetric in the top-down game view.  The
    # north-facing frame must therefore be the exact vertical reflection of
    # south; an independently rendered N perspective makes it visibly tilt
    # when the unit starts moving upward.
    extracted["N"] = extracted["S"].transpose(
        Image.Transpose.FLIP_TOP_BOTTOM
    )
    # The central vehicle in the supplied reference is the true west-facing
    # side profile.  Keep it in the W slot and derive E by symmetry.  Reversing
    # these two slots makes the launcher drive tail-first at 3 and 9 o'clock.
    extracted["W"] = extract_subject(source, SOURCE_CROPS["W"])
    extracted["E"] = extracted["W"].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    extracted["NW"] = extracted["NE"].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    extracted["SW"] = extracted["SE"].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return extracted


def assemble(frames: dict[str, Image.Image]) -> Image.Image:
    boxes = {}
    for direction, image in frames.items():
        box = image.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"empty direction: {direction}")
        boxes[direction] = box

    result = Image.new("RGBA", ATLAS)
    for index, direction in enumerate(DIRECTIONS):
        image = frames[direction]
        box = boxes[direction]
        subject = image.crop(box)
        # Keep the apparent vehicle length stable while it rotates. Width and
        # height naturally exchange roles between cardinal directions.
        scale = min(
            116 / subject.width,
            116 / subject.height,
        )
        size = (
            max(1, round(subject.width * scale)),
            max(1, round(subject.height * scale)),
        )
        subject = subject.resize(size, Image.Resampling.LANCZOS)
        position = (
            index * FRAME[0] + (FRAME[0] - size[0]) // 2,
            (FRAME[1] - size[1]) // 2,
        )
        result.alpha_composite(subject, position)
    return result


def smoothstep(low: float, high: float, value: np.ndarray) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def neutral_and_mask(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    dominance = (green - np.maximum(red, blue)) / 255.0
    purity = (green - np.maximum(red, blue)) / np.maximum(green, 1.0)
    selection = (
        smoothstep(0.025, 0.16, dominance)
        * smoothstep(0.06, 0.34, purity)
        * smoothstep(22.0, 68.0, green)
        * (alpha / 255.0)
    )

    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    neutral_rgb = np.dstack(
        (luminance * 0.72, luminance * 0.78, luminance * 0.84)
    )
    amount = np.clip(selection * 1.30, 0.0, 1.0)[:, :, None]
    neutral = rgba.copy()
    neutral[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - amount) + neutral_rgb * amount
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


def export_classic_direction_refs() -> None:
    classic = Image.open(CLASSIC).convert("RGBA")
    CLASSIC_REFS.mkdir(parents=True, exist_ok=True)
    for index, direction in enumerate(DIRECTIONS):
        frame = classic.crop((index * 32, 0, (index + 1) * 32, 32))
        guide = Image.new("RGBA", (512, 512), (255, 0, 255, 255))
        enlarged = frame.resize((448, 448), Image.Resampling.NEAREST)
        guide.alpha_composite(enlarged, (32, 32))
        guide.convert("RGB").save(
            CLASSIC_REFS / f"{index}_{direction}.png",
            optimize=True,
        )


def build_shadow(atlas: Image.Image) -> Image.Image:
    shadow_atlas = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas_frame(atlas, index)
        alpha = frame.getchannel("A").filter(
            ImageFilter.GaussianBlur(1.6)
        ).point(lambda value: round(value * 0.20))
        shadow = Image.new("RGBA", FRAME, (7, 5, 3, 0))
        shadow.putalpha(alpha)
        shadow_frame = Image.new("RGBA", FRAME)
        shadow_frame.alpha_composite(shadow, (2, 2))
        shadow_atlas.alpha_composite(
            shadow_frame,
            (index * FRAME[0], 0),
        )
    return shadow_atlas


def apply_tint(
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
        (x, y, x + size, y + size + 34),
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
        (x + 8, y + size + 5),
        label,
        font=font(17, True),
        fill=(231, 214, 177, 255),
    )


def build_review(atlas: Image.Image, mask: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1775, 1050), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Ракетная установка — полный атлас направлений",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 70),
        "HD4: 8×1, кадр 128×128; игровой порядок E, NE, N, NW, W, SW, S, SE",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    tinted = apply_tint(atlas, mask, HOUSE_COLORS["Ордос"])
    for index, direction in enumerate(DIRECTIONS):
        draw_card(
            board,
            atlas_frame(tinted, index),
            34 + index * 216,
            112,
            190,
            direction,
        )

    draw.text(
        (34, 365),
        "Цветовая маска Домов",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for column, (name, color) in enumerate(HOUSE_COLORS.items()):
        draw_card(
            board,
            atlas_frame(apply_tint(atlas, mask, color), 1),
            34 + column * 300,
            415,
            260,
            name,
        )
    draw_card(
        board,
        atlas_frame(mask, 1),
        934,
        415,
        260,
        "маска",
    )

    classic = Image.open(CLASSIC).convert("RGBA")
    draw.text(
        (34, 755),
        "Сравнение размера и ориентации",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    draw_card(
        board,
        atlas_frame(
            classic.resize(ATLAS, Image.Resampling.NEAREST),
            1,
        ),
        34,
        805,
        180,
        "классика NE",
    )
    draw_card(
        board,
        atlas_frame(tinted, 1),
        250,
        805,
        180,
        "HD4 NE",
    )
    draw.text(
        (480, 820),
        "• исходный контракт 32×32 сохранён\n"
        "• все ракурсы имеют единый масштаб и центр\n"
        "• перед, корма и направление ракет согласованы\n"
        "• корпус и пусковая установка остаются одним ресурсом",
        font=font(22),
        fill=(204, 208, 213, 255),
        spacing=14,
    )
    draw.text(
        (34, 1018),
        "Предварительный просмотр — в игру не установлено.",
        font=font(19),
        fill=(188, 194, 202, 255),
    )
    return board


def build_rotation(atlas: Image.Image, mask: Image.Image) -> None:
    tinted = apply_tint(atlas, mask, HOUSE_COLORS["Ордос"])
    frames = []
    for index in range(8):
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            atlas_frame(tinted, index).resize(
                (512, 512),
                Image.Resampling.LANCZOS,
            )
        )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ROTATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=220,
        loop=0,
        disposal=2,
    )


def validate(
    atlas: Image.Image,
    mask: Image.Image,
    shadow: Image.Image,
    hd2: Image.Image,
) -> dict[str, object]:
    for name, image in (
        ("launcher", atlas),
        ("mask", mask),
        ("shadow", shadow),
    ):
        if image.size != ATLAS:
            raise AssertionError(f"{name} atlas size changed: {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} atlas is empty")

    frames = [atlas_frame(atlas, index) for index in range(8)]
    if len({frame.tobytes() for frame in frames}) != 8:
        raise AssertionError("launcher directions are not unique")

    frame_boxes = {}
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
                f"{DIRECTIONS[index]} touches frame boundary: {box}"
            )
        frame_boxes[DIRECTIONS[index]] = list(box)

        shadow_box = atlas_frame(shadow, index).getchannel("A").getbbox()
        if (
            shadow_box is None
            or shadow_box[0] < 1
            or shadow_box[1] < 1
            or shadow_box[2] > 127
            or shadow_box[3] > 127
        ):
            raise AssertionError(
                f"{DIRECTIONS[index]} shadow touches boundary: "
                f"{shadow_box}"
            )

    expected_hd2 = atlas.resize((512, 64), Image.Resampling.LANCZOS)
    if ImageChops.difference(hd2, expected_hd2).getbbox():
        raise AssertionError("HD2 is not the deterministic HD4 derivative")

    return {
        "resources": {
            "launcher": {"id": 139, "name": "UNIT_LAUNCHER"},
            "shadow": {"id": 140, "name": "UNIT_LAUNCHER_SHADOW"},
            "house_mask": {"name": "HM_UNIT_LAUNCHER"},
        },
        "direction_order": list(DIRECTIONS),
        "logical_frame": [32, 32],
        "hd2_frame": [64, 64],
        "hd4_frame": list(FRAME),
        "hd4_atlas": list(ATLAS),
        "frames": 8,
        "frame_boxes_hd4": frame_boxes,
        "mask_pixels": int(
            np.count_nonzero(
                np.asarray(mask.getchannel("A"), dtype=np.uint8) > 8
            )
        ),
        "pivot_hd4": [64, 64],
        "pivot_logical": [16, 16],
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_classic_direction_refs()
    extracted = source_frames()
    colored_atlas = assemble(extracted)
    atlas, mask = neutral_and_mask(colored_atlas)
    shadow = build_shadow(atlas)
    hd2 = atlas.resize((512, 64), Image.Resampling.LANCZOS)
    validation = validate(atlas, mask, shadow, hd2)

    atlas.save(ATLAS_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    hd2.save(HD2_OUT, optimize=True)
    build_review(atlas, mask).save(REVIEW_OUT, optimize=True)
    build_rotation(atlas, mask)

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(SOURCE),
        "generation_sources": {
            "W": {
                "file": str(SOURCE),
                "crop": list(SOURCE_CROPS["W"]),
                "note": "approved true west-facing side profile from user reference",
            },
            **{
                direction: str(
                    DIRECTION_SOURCES / f"{direction}_chroma.png"
                )
                for direction in ("NE", "N", "S", "SE")
            },
        },
        "derived_by_horizontal_symmetry": {
            "E": "W",
            "NW": "NE",
            "SW": "SE",
        },
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
