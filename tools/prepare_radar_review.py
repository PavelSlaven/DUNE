#!/usr/bin/env python3
"""Build approval-ready HD radar frames and animated House flags."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "radar_review_v1"
BODY_SOURCE = OUTPUT / "radar_body_alpha.png"
ROTOR_SOURCE = OUTPUT / "radar_rotor_alpha.png"
FLAG_SOURCE = OUTPUT / "radar_flag_alpha.png"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0026_BUILD_RADAR.png"
)

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
FRAME_COUNT = 8
BODY_SOURCE_PIVOT = (817, 300)
ROTOR_SOURCE_PIVOT = (665, 551)
ROTOR_SQUARE_SIDE = 840
ROTOR_TARGET_SIDE = 76

BUILDING_OUT = OUTPUT / "BUILD_RADAR_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_RADAR_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_RADAR_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_RADAR_FLAG_HD4_PREVIEW.png"
BUILDING_HD2_OUT = OUTPUT / "BUILD_RADAR_HD2_PREVIEW.png"
SHADOW_HD2_OUT = OUTPUT / "BUILD_RADAR_SHADOW_HD2_PREVIEW.png"
FLAG_HD2_OUT = OUTPUT / "BUILD_RADAR_FLAG_HD2_PREVIEW.png"
FLAG_MASK_HD2_OUT = OUTPUT / "HM_BUILD_RADAR_FLAG_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_RADAR_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_RADAR_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def crop_alpha(source: Image.Image) -> tuple[Image.Image, tuple[int, ...]]:
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated source is fully transparent")
    return source.crop(box), box


def fit_body(source: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    subject, box = crop_alpha(source)
    max_size = (232, 236)
    scale = min(max_size[0] / subject.width, max_size[1] / subject.height)
    size = (
        round(subject.width * scale),
        round(subject.height * scale),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    position = (
        (FRAME[0] - subject.width) // 2,
        FRAME[1] - subject.height - 8,
    )
    frame = Image.new("RGBA", FRAME)
    frame.alpha_composite(subject, position)
    pivot = (
        round(position[0] + (BODY_SOURCE_PIVOT[0] - box[0]) * scale),
        round(position[1] + (BODY_SOURCE_PIVOT[1] - box[1]) * scale),
    )
    return frame, pivot


def centered_rotor(source: Image.Image) -> Image.Image:
    half = ROTOR_SQUARE_SIDE // 2
    pivot_x, pivot_y = ROTOR_SOURCE_PIVOT
    box = (
        pivot_x - half,
        pivot_y - half,
        pivot_x + half,
        pivot_y + half,
    )
    square = source.crop(box)
    if square.size != (ROTOR_SQUARE_SIDE, ROTOR_SQUARE_SIDE):
        raise AssertionError("radar rotor crop lost its square geometry")
    return square.resize(
        (ROTOR_TARGET_SIDE, ROTOR_TARGET_SIDE),
        Image.Resampling.LANCZOS,
    )


def radar_frame(
    body: Image.Image,
    rotor: Image.Image,
    pivot: tuple[int, int],
    phase: int,
) -> Image.Image:
    # The classic order is S, SW, W, NW, N, NE, E, SE.
    # The generated master points SE, so frame zero needs one clockwise step.
    angle = -45 * (phase + 1)
    rotated = rotor.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=False,
    )
    frame = body.copy()
    frame.alpha_composite(
        rotated,
        (
            pivot[0] - rotated.width // 2,
            pivot[1] - rotated.height // 2,
        ),
    )
    return frame


def split_flag(source: Image.Image) -> tuple[Image.Image, Image.Image]:
    subject, _ = crop_alpha(source)
    rgba = np.asarray(subject, dtype=np.uint8).copy()
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    fabric_mask = (
        (alpha > 6)
        & (green > 55)
        & (green.astype(np.float32) > red * 1.20)
        & (green.astype(np.float32) > blue * 1.15)
    )
    labels, count = ndimage.label(fabric_mask)
    if count < 1:
        raise AssertionError("unable to isolate radar flag fabric")
    sizes = ndimage.sum(fabric_mask, labels, range(1, count + 1))
    fabric_mask = labels == (int(np.argmax(sizes)) + 1)
    fabric_mask = ndimage.binary_dilation(fabric_mask, iterations=2)
    fabric_rgba = rgba.copy()
    fabric_rgba[:, :, 3] = np.where(fabric_mask, alpha, 0)
    pole_rgba = rgba.copy()
    pole_rgba[fabric_mask] = 0
    return (
        Image.fromarray(pole_rgba, "RGBA"),
        Image.fromarray(fabric_rgba, "RGBA"),
    )


def wave_component(component: Image.Image, phase: int) -> Image.Image:
    source = np.asarray(component.convert("RGBA"), dtype=np.float32)
    height, width = source.shape[:2]
    output = np.zeros_like(source)
    phase_angle = phase * 2.0 * math.pi / FRAME_COUNT
    for x in range(width):
        distance_from_pole = (width - 1 - x) / max(1, width - 1)
        shift = (
            1.7
            * distance_from_pole
            * math.sin(
                phase_angle + x / max(1, width - 1) * math.pi * 1.65
            )
        )
        for y in range(height):
            source_y = y - shift
            lower = math.floor(source_y)
            upper = lower + 1
            fraction = source_y - lower
            if 0 <= lower < height:
                output[y, x] += source[lower, x] * (1.0 - fraction)
            if 0 <= upper < height:
                output[y, x] += source[upper, x] * fraction
    return Image.fromarray(
        np.clip(output, 0, 255).astype(np.uint8),
        "RGBA",
    )


def flag_variant(
    pole: Image.Image,
    fabric: Image.Image,
    size: tuple[int, int],
    phase: int,
) -> tuple[Image.Image, Image.Image]:
    pole_scaled = pole.resize(size, Image.Resampling.LANCZOS)
    fabric_scaled = fabric.resize(size, Image.Resampling.LANCZOS)
    waved = wave_component(fabric_scaled, phase)
    visible = Image.new("RGBA", size)
    visible.alpha_composite(pole_scaled)
    visible.alpha_composite(waved)
    mask = Image.new("RGBA", size, (255, 255, 255, 0))
    mask.putalpha(waved.getchannel("A"))
    return visible, mask


def build_flag_atlases(
    pole: Image.Image,
    fabric: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    atlas = Image.new("RGBA", (FRAME[0], FRAME[1] * FRAME_COUNT))
    mask_atlas = Image.new("RGBA", atlas.size)
    for phase in range(FRAME_COUNT):
        frame = Image.new("RGBA", FRAME)
        mask_frame = Image.new("RGBA", FRAME)
        small, small_mask = flag_variant(
            pole,
            fabric,
            (44, 62),
            (phase + 2) % FRAME_COUNT,
        )
        large, large_mask = flag_variant(
            pole,
            fabric,
            (64, 84),
            phase,
        )
        # Original corrected top-left coordinates are both (2, y):
        # large (2, 38), small (2, 46) in the 64x64 frame.
        frame.alpha_composite(small, (8, 181))
        mask_frame.alpha_composite(small_mask, (8, 181))
        frame.alpha_composite(large, (8, 148))
        mask_frame.alpha_composite(large_mask, (8, 148))
        atlas.alpha_composite(frame, (0, phase * FRAME[1]))
        mask_atlas.alpha_composite(
            mask_frame,
            (0, phase * FRAME[1]),
        )
    return atlas, mask_atlas


def frame_from_atlas(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (0, phase * FRAME[1], FRAME[0], (phase + 1) * FRAME[1])
    )


def build_shadow_atlas(building_atlas: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", building_atlas.size)
    for phase in range(FRAME_COUNT):
        frame = frame_from_atlas(building_atlas, phase)
        alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(1.4))
        alpha = alpha.point(lambda value: round(value * 0.17))
        silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
        silhouette.putalpha(alpha)
        shadow = Image.new("RGBA", FRAME)
        shadow.alpha_composite(silhouette, (2, 2))
        atlas.alpha_composite(shadow, (0, phase * FRAME[1]))
    return atlas


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
    return Image.fromarray(
        np.clip(rgba, 0, 255).astype(np.uint8),
        "RGBA",
    )


def composed(
    building_atlas: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    frame = frame_from_atlas(building_atlas, phase)
    flag = frame_from_atlas(flag_atlas, phase)
    mask = frame_from_atlas(mask_atlas, phase)
    frame.alpha_composite(apply_engine_tint(flag, mask, color))
    return frame


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
        font=font(16, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    building_atlas: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1760, 1320), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Радар — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "ID 26; 8 кадров 64×64; порядок S → SW → W → NW → N → NE → E → SE",
        font=font(18),
        fill=(187, 193, 201, 255),
    )
    for phase in range(FRAME_COUNT):
        draw_card(
            board,
            composed(
                building_atlas,
                flag_atlas,
                mask_atlas,
                phase,
                HOUSE_COLORS["Ордос"],
            ),
            34 + phase * 214,
            108,
            188,
            f"кадр {phase}",
        )

    draw.text(
        (34, 350),
        "Цвет Домов и отдельные слои",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, (name, color) in enumerate(HOUSE_COLORS.items()):
        draw_card(
            board,
            composed(
                building_atlas,
                flag_atlas,
                mask_atlas,
                1 + index * 2,
                color,
            ),
            34 + index * 330,
            395,
            300,
            name,
        )
    draw_card(
        board,
        frame_from_atlas(building_atlas, 0),
        1024,
        395,
        300,
        "корпус + ротор",
    )
    draw_card(
        board,
        frame_from_atlas(mask_atlas, 0),
        1354,
        395,
        300,
        "маска тканей",
    )

    draw.text(
        (34, 785),
        "Сверка с классическим атласом",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    for phase in range(FRAME_COUNT):
        draw_card(
            board,
            classic.crop((0, phase * 64, 64, (phase + 1) * 64)),
            34 + phase * 156,
            830,
            132,
            f"старый {phase}",
        )
    draw.text(
        (34, 1035),
        "• площадь здания 2×2 клетки\n"
        "• один неизменный корпус во всех восьми кадрах\n"
        "• единый ротор вращается вокруг фиксированного центра\n"
        "• длина и масштаб ротора одинаковы во всех направлениях\n"
        "• сохранены большой и малый флаг из исходной конфигурации\n"
        "• цветовая маска затрагивает только ткани",
        font=font(22),
        fill=(204, 208, 213, 255),
        spacing=13,
    )
    draw.text(
        (34, 1270),
        "Предварительный просмотр — в игру не установлено.",
        font=font(20),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(
    building_atlas: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> None:
    frames = []
    for phase in range(FRAME_COUNT):
        sprite = composed(
            building_atlas,
            flag_atlas,
            mask_atlas,
            phase,
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
        duration=140,
        loop=0,
        disposal=2,
    )


def validate(
    building_atlas: Image.Image,
    shadow_atlas: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
    pivot: tuple[int, int],
) -> dict[str, object]:
    expected_size = (FRAME[0], FRAME[1] * FRAME_COUNT)
    for name, atlas in (
        ("building", building_atlas),
        ("shadow", shadow_atlas),
        ("flag", flag_atlas),
        ("flag mask", mask_atlas),
    ):
        if atlas.size != expected_size:
            raise AssertionError(f"{name} atlas dimensions changed")

    building_frames = [
        frame_from_atlas(building_atlas, phase)
        for phase in range(FRAME_COUNT)
    ]
    if len({frame.tobytes() for frame in building_frames}) != FRAME_COUNT:
        raise AssertionError("radar animation phases are not unique")
    flag_frames = [
        frame_from_atlas(flag_atlas, phase)
        for phase in range(FRAME_COUNT)
    ]
    if len({frame.tobytes() for frame in flag_frames}) != FRAME_COUNT:
        raise AssertionError("flag animation phases are not unique")

    boxes = {}
    for name, frames in (
        ("building", building_frames),
        ("flag", flag_frames),
    ):
        frame_boxes = []
        for phase, frame in enumerate(frames):
            box = frame.getchannel("A").getbbox()
            if (
                box is None
                or box[0] < 1
                or box[1] < 1
                or box[2] > 255
                or box[3] > 255
            ):
                raise AssertionError(
                    f"{name} phase {phase} touches boundary: {box}"
                )
            frame_boxes.append(list(box))
        boxes[name] = frame_boxes

    return {
        "resources": {
            "building": {"id": 26, "name": "BUILD_RADAR"},
            "shadow": {"id": 27, "name": "BUILD_RADAR_SHADOW"},
            "flag": "BUILD_RADAR_FLAG",
            "flag_mask": "HM_BUILD_RADAR_FLAG",
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd2_frame": [128, 128],
        "hd4_frame": list(FRAME),
        "footprint": [2, 2],
        "building_frames": FRAME_COUNT,
        "flag_frames": FRAME_COUNT,
        "direction_order": ["S", "SW", "W", "NW", "N", "NE", "E", "SE"],
        "original_flag_points": [[17, 38], [12, 46]],
        "radar_pivot_hd4": list(pivot),
        "boxes_hd4": boxes,
    }


def main() -> None:
    for path in (BODY_SOURCE, ROTOR_SOURCE, FLAG_SOURCE, CLASSIC):
        if not path.is_file():
            raise FileNotFoundError(path)

    body, pivot = fit_body(Image.open(BODY_SOURCE).convert("RGBA"))
    rotor = centered_rotor(Image.open(ROTOR_SOURCE).convert("RGBA"))
    building_atlas = Image.new(
        "RGBA",
        (FRAME[0], FRAME[1] * FRAME_COUNT),
    )
    for phase in range(FRAME_COUNT):
        building_atlas.alpha_composite(
            radar_frame(body, rotor, pivot, phase),
            (0, phase * FRAME[1]),
        )

    pole, fabric = split_flag(Image.open(FLAG_SOURCE).convert("RGBA"))
    flag_atlas, mask_atlas = build_flag_atlases(pole, fabric)
    shadow_atlas = build_shadow_atlas(building_atlas)
    validation = validate(
        building_atlas,
        shadow_atlas,
        flag_atlas,
        mask_atlas,
        pivot,
    )

    building_atlas.save(BUILDING_OUT, optimize=True)
    shadow_atlas.save(SHADOW_OUT, optimize=True)
    flag_atlas.save(FLAG_OUT, optimize=True)
    mask_atlas.save(FLAG_MASK_OUT, optimize=True)
    building_atlas.resize((128, 1024), Image.Resampling.LANCZOS).save(
        BUILDING_HD2_OUT,
        optimize=True,
    )
    shadow_atlas.resize((128, 1024), Image.Resampling.LANCZOS).save(
        SHADOW_HD2_OUT,
        optimize=True,
    )
    flag_atlas.resize((128, 1024), Image.Resampling.LANCZOS).save(
        FLAG_HD2_OUT,
        optimize=True,
    )
    mask_atlas.resize((128, 1024), Image.Resampling.LANCZOS).save(
        FLAG_MASK_HD2_OUT,
        optimize=True,
    )
    build_review(building_atlas, flag_atlas, mask_atlas).save(
        REVIEW_OUT,
        optimize=True,
    )
    build_animation(building_atlas, flag_atlas, mask_atlas)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "generation_mode": (
            "built-in imagegen plus deterministic rotor/flag animation"
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
