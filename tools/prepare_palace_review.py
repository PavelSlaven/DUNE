#!/usr/bin/env python3
"""Build an approval-ready HD palace with animated LEDs and House flag."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "palace_review_v1"
SOURCE = OUTPUT / "generated" / "palace_alpha.png"
USER_REFERENCE = OUTPUT / "user_reference.png"
CLASSIC = OUTPUT / "0015_BUILD_PALACE_CLASSIC.png"

FRAME = (384, 384)
LOGICAL_FRAME = (96, 96)
ANIMATION_FRAMES = 8
FLAG_SIZE = (76, 46)

BUILDING_OUT = OUTPUT / "BUILD_PALACE_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_PALACE_SHADOW_HD4_PREVIEW.png"
OVERLAY_OUT = OUTPUT / "BUILD_PALACE_FLAG_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_BUILD_PALACE_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_PALACE_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_PALACE_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}

# Source coordinates of the five small-dome beacon tips and the attachment
# point on the central flag pole in the accepted ImageGen master.
SOURCE_LED_POINTS = (
    (287, 142),
    (712, 84),
    (958, 145),
    (326, 606),
    (823, 553),
)
SOURCE_FLAG_ATTACH = (486, 212)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def fit_building(
    source: Image.Image,
) -> tuple[Image.Image, list[tuple[int, int]], tuple[int, int]]:
    source = source.convert("RGBA")
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated palace is transparent")
    subject = source.crop(box)
    scale = min(376 / subject.width, 372 / subject.height)
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)

    pixels = np.asarray(subject, dtype=np.uint8).copy()
    magenta_edge = (
        (pixels[:, :, 0] > 150)
        & (pixels[:, :, 2] > 150)
        & (pixels[:, :, 1] < 105)
        & (pixels[:, :, 3] < 230)
    )
    pixels[magenta_edge] = 0
    subject = Image.fromarray(pixels, "RGBA")

    position = (
        (FRAME[0] - subject.width) // 2,
        FRAME[1] - subject.height - 6,
    )
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(subject, position)

    def mapped(point: tuple[int, int]) -> tuple[int, int]:
        return (
            round(position[0] + (point[0] - box[0]) * scale),
            round(position[1] + (point[1] - box[1]) * scale),
        )

    return (
        result,
        [mapped(point) for point in SOURCE_LED_POINTS],
        mapped(SOURCE_FLAG_ATTACH),
    )


def extract_flag(reference: Image.Image) -> Image.Image:
    rgba = np.asarray(reference.convert("RGBA"), dtype=np.float32)
    red, green, blue = (rgba[:, :, index] for index in range(3))
    selection = (
        (green > 70)
        & (green > red * 1.18)
        & (green > blue * 1.14)
    )
    labels, count = ndimage.label(
        selection,
        structure=np.ones((3, 3), dtype=np.uint8),
    )
    candidates = []
    for label_id in range(1, count + 1):
        component = labels == label_id
        ys, xs = np.nonzero(component)
        if len(xs) < 100:
            continue
        if (
            xs.mean() < reference.width * 0.55
            and ys.mean() < reference.height * 0.40
        ):
            candidates.append((len(xs), component))
    if not candidates:
        raise AssertionError("unable to locate palace flag fabric")
    component = max(candidates, key=lambda item: item[0])[1]
    fabric = ndimage.binary_dilation(component, iterations=3)
    alpha = np.where(fabric, 255, 0).astype(np.uint8)
    extracted = reference.convert("RGBA").copy()
    extracted.putalpha(Image.fromarray(alpha, "L"))
    box = Image.fromarray(alpha, "L").getbbox()
    if box is None:
        raise AssertionError("palace flag extraction is empty")
    return extracted.crop(box).resize(FLAG_SIZE, Image.Resampling.LANCZOS)


def wave_flag(flag: Image.Image, phase: int) -> Image.Image:
    source = np.asarray(flag.convert("RGBA"), dtype=np.float32)
    height, width = source.shape[:2]
    output = np.zeros_like(source)
    phase_angle = phase * 2.0 * math.pi / ANIMATION_FRAMES
    for x in range(width):
        distance_from_pole = (width - 1 - x) / max(1, width - 1)
        shift = (
            3.3
            * distance_from_pole
            * math.sin(
                phase_angle
                + x / max(1, width - 1) * math.pi * 1.7
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


def draw_led(
    frame: Image.Image,
    position: tuple[int, int],
    intensity: float,
) -> None:
    if intensity <= 0.0:
        return
    glow = Image.new("RGBA", FRAME)
    glow_draw = ImageDraw.Draw(glow)
    x, y = position
    glow_draw.ellipse(
        (x - 8, y - 8, x + 8, y + 8),
        fill=(255, 18, 4, round(115 * intensity)),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(5.0))
    frame.alpha_composite(glow)
    draw = ImageDraw.Draw(frame)
    draw.ellipse(
        (x - 3, y - 3, x + 3, y + 3),
        fill=(255, 30, 12, round(235 * intensity)),
    )
    draw.ellipse(
        (x - 1, y - 2, x + 1, y),
        fill=(255, 238, 206, round(255 * intensity)),
    )


def build_overlay_atlases(
    flag: Image.Image,
    flag_attach: tuple[int, int],
    led_points: list[tuple[int, int]],
) -> tuple[Image.Image, Image.Image]:
    atlas_size = (FRAME[0], FRAME[1] * ANIMATION_FRAMES)
    atlas = Image.new("RGBA", atlas_size)
    mask = Image.new("RGBA", atlas_size, (255, 255, 255, 0))
    led_phases = (
        (0.15, 0.00),
        (0.60, 0.00),
        (1.00, 0.15),
        (0.35, 0.65),
        (0.00, 1.00),
        (0.00, 0.45),
        (0.45, 0.20),
        (1.00, 1.00),
    )
    for phase in range(ANIMATION_FRAMES):
        waved = wave_flag(flag, phase)
        flag_position = (
            flag_attach[0] - waved.width + 3,
            flag_attach[1] - waved.height // 2,
        )
        overlay_frame = Image.new("RGBA", FRAME)
        overlay_frame.alpha_composite(waved, flag_position)

        mask_frame = Image.new("RGBA", FRAME, (255, 255, 255, 0))
        mask_piece = Image.new("RGBA", waved.size, (255, 255, 255, 0))
        mask_piece.putalpha(
            waved.getchannel("A").point(lambda value: round(value * 0.84))
        )
        mask_frame.alpha_composite(mask_piece, flag_position)

        rear_intensity, front_intensity = led_phases[phase]
        for position in led_points[:3]:
            draw_led(overlay_frame, position, rear_intensity)
        for position in led_points[3:]:
            draw_led(overlay_frame, position, front_intensity)

        atlas.alpha_composite(overlay_frame, (0, phase * FRAME[1]))
        mask.alpha_composite(mask_frame, (0, phase * FRAME[1]))
    return atlas, mask


def overlay_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (
            0,
            phase * FRAME[1],
            FRAME[0],
            (phase + 1) * FRAME[1],
        )
    )


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
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = building.copy()
    result.alpha_composite(
        apply_engine_tint(
            overlay_frame(overlay, phase),
            overlay_frame(mask, phase),
            color,
        )
    )
    return result


def build_shadow(building: Image.Image) -> Image.Image:
    alpha = building.getchannel("A").filter(ImageFilter.GaussianBlur(2.4))
    alpha = alpha.point(lambda value: round(value * 0.18))
    silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(silhouette, (5, 5))
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
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1780, 1370), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Дворец — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "Корпус 96×96; восемь фаз флага и пяти сигнальных диодов",
        font=font(19),
        fill=(187, 193, 201, 255),
    )
    for phase in range(ANIMATION_FRAMES):
        draw_card(
            board,
            composed(
                building,
                overlay,
                mask,
                phase,
                HOUSE_COLORS["Ордос"],
            ),
            34 + phase * 216,
            108,
            190,
            f"фаза {phase}",
        )

    draw.text(
        (34, 355),
        "Цвет Домов — только ткань флага; диоды остаются красными",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for column, (name, color) in enumerate(HOUSE_COLORS.items()):
        draw_card(
            board,
            composed(building, overlay, mask, 2 + column * 2, color),
            34 + column * 330,
            400,
            300,
            name,
        )
    draw_card(board, building, 1024, 400, 300, "корпус без анимации")
    draw_card(
        board,
        overlay_frame(mask, 0),
        1354,
        400,
        300,
        "маска флага",
    )

    draw.text(
        (34, 790),
        "Размер и исходный контракт",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    draw_card(
        board,
        Image.open(CLASSIC).convert("RGBA"),
        34,
        835,
        360,
        "классика 96×96",
    )
    draw_card(
        board,
        composed(
            building,
            overlay,
            mask,
            7,
            HOUSE_COLORS["Ордос"],
        ),
        430,
        835,
        360,
        "HD4 384×384",
    )
    draw.text(
        (840, 880),
        "• площадь здания 3×3 клетки\n"
        "• один неподвижный кадр корпуса\n"
        "• нижняя граница и вход сохранены\n"
        "• пять маяков мигают двумя группами\n"
        "• флаг имеет 8 уникальных фаз\n"
        "• отдельная детерминированная тень",
        font=font(23),
        fill=(204, 208, 213, 255),
        spacing=16,
    )
    draw.text(
        (34, 1322),
        "Предварительный просмотр — в игру не установлено.",
        font=font(20),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> None:
    frames = []
    for phase in range(ANIMATION_FRAMES):
        sprite = composed(
            building,
            overlay,
            mask,
            phase,
            HOUSE_COLORS["Ордос"],
        )
        shown = Image.new("RGBA", (640, 640), (16, 20, 26, 255))
        shown.alpha_composite(
            sprite.resize((640, 640), Image.Resampling.LANCZOS)
        )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=125,
        loop=0,
        disposal=2,
    )


def validate(
    building: Image.Image,
    shadow: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
    led_points: list[tuple[int, int]],
    flag_attach: tuple[int, int],
) -> dict[str, object]:
    if building.size != FRAME or shadow.size != FRAME:
        raise AssertionError("palace or shadow dimensions changed")
    expected_atlas = (FRAME[0], FRAME[1] * ANIMATION_FRAMES)
    if overlay.size != expected_atlas or mask.size != expected_atlas:
        raise AssertionError("palace overlay dimensions changed")
    box = building.getchannel("A").getbbox()
    if (
        box is None
        or box[0] < 3
        or box[1] < 3
        or box[2] > 381
        or box[3] > 381
    ):
        raise AssertionError(f"palace touches frame boundary: {box}")
    phases = [
        overlay_frame(overlay, phase) for phase in range(ANIMATION_FRAMES)
    ]
    masks = [
        overlay_frame(mask, phase) for phase in range(ANIMATION_FRAMES)
    ]
    if len({phase.tobytes() for phase in phases}) != ANIMATION_FRAMES:
        raise AssertionError("palace animation phases are not unique")
    if len({phase.tobytes() for phase in masks}) != ANIMATION_FRAMES:
        raise AssertionError("palace flag phases are not unique")
    if len(led_points) != 5:
        raise AssertionError("palace must have five roof LEDs")
    return {
        "resources": {
            "building": {"id": 15, "name": "BUILD_PALACE"},
            "shadow": {"id": 16, "name": "BUILD_PALACE_SHADOW"},
            "overlay": "BUILD_PALACE_FLAG",
            "overlay_mask": "HM_BUILD_PALACE_FLAG",
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd4_frame": list(FRAME),
        "footprint": [3, 3],
        "base_frames": 1,
        "overlay_frames": ANIMATION_FRAMES,
        "building_box_hd4": list(box),
        "led_points_hd4": [list(point) for point in led_points],
        "flag_attach_hd4": list(flag_attach),
        "flag_mask_pixels": int(
            np.count_nonzero(np.asarray(mask.getchannel("A")) > 8)
        ),
    }


def main() -> None:
    for path in (SOURCE, USER_REFERENCE, CLASSIC):
        if not path.is_file():
            raise FileNotFoundError(path)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    building, led_points, flag_attach = fit_building(Image.open(SOURCE))
    flag = extract_flag(Image.open(USER_REFERENCE))
    overlay, mask = build_overlay_atlases(
        flag,
        flag_attach,
        led_points,
    )
    shadow = build_shadow(building)
    validation = validate(
        building,
        shadow,
        overlay,
        mask,
        led_points,
        flag_attach,
    )

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    overlay.save(OVERLAY_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    building.resize((192, 192), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_PALACE_HD2_PREVIEW.png",
        optimize=True,
    )
    overlay.resize((192, 1536), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_PALACE_FLAG_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(building, overlay, mask).save(REVIEW_OUT, optimize=True)
    build_animation(building, overlay, mask)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(USER_REFERENCE),
        "generated_base": str(SOURCE),
        "classic_contract": str(CLASSIC),
        "generation_mode": (
            "ImageGen base plus deterministic flag and LED animation"
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
