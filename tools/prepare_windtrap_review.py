#!/usr/bin/env python3
"""Build an approval-ready HD wind trap and animated House flag."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "windtrap_review_v1"
SOURCE = OUTPUT / "windtrap_alpha.png"
USER_REFERENCE = OUTPUT / "user_reference.png"
CLASSIC = OUTPUT / "0040_BUILD_WINDTRAP_CLASSIC.png"

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
FLAG_FRAMES = 8
FLAG_ATTACH = (212, 130)
FLAG_SIZE = (42, 27)

BUILDING_OUT = OUTPUT / "BUILD_WINDTRAP_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_WINDTRAP_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_WINDTRAP_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_WINDTRAP_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def fit_building(source: Image.Image) -> Image.Image:
    alpha_box = source.getchannel("A").getbbox()
    if alpha_box is None:
        raise AssertionError("generated wind trap is transparent")
    subject = source.crop(alpha_box)
    max_size = (248, 244)
    scale = min(max_size[0] / subject.width, max_size[1] / subject.height)
    size = (round(subject.width * scale), round(subject.height * scale))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    pixels = np.asarray(subject, dtype=np.uint8).copy()
    weak_chroma = (
        (pixels[:, :, 3] < 8)
        & (pixels[:, :, 0] > 220)
        & (pixels[:, :, 2] > 220)
        & (pixels[:, :, 1] < 80)
    )
    pixels[weak_chroma] = 0
    subject = Image.fromarray(pixels, "RGBA")
    frame = Image.new("RGBA", FRAME)
    frame.alpha_composite(
        subject,
        (
            (FRAME[0] - subject.width) // 2,
            FRAME[1] - subject.height - 4,
        ),
    )
    return frame


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
    components = []
    for label_id in range(1, count + 1):
        component = labels == label_id
        ys, xs = np.nonzero(component)
        if not len(xs):
            continue
        # The reference flag occupies the lower-right service quadrant.
        if xs.mean() > reference.width * 0.55 and ys.mean() > reference.height * 0.40:
            components.append((len(xs), component))
    if not components:
        raise AssertionError("unable to locate green flag fabric")
    component = max(components, key=lambda item: item[0])[1]
    fabric = ndimage.binary_dilation(component, iterations=3)
    alpha = np.where(fabric, 255, 0).astype(np.uint8)
    extracted = reference.convert("RGBA").copy()
    extracted.putalpha(Image.fromarray(alpha, "L"))
    box = Image.fromarray(alpha, "L").getbbox()
    if box is None:
        raise AssertionError("flag extraction is empty")
    return extracted.crop(box).resize(FLAG_SIZE, Image.Resampling.LANCZOS)


def wave_flag(flag: Image.Image, phase: int) -> Image.Image:
    source = np.asarray(flag.convert("RGBA"), dtype=np.float32)
    height, width = source.shape[:2]
    output = np.zeros_like(source)
    phase_angle = phase * 2.0 * math.pi / FLAG_FRAMES
    for x in range(width):
        distance_from_pole = (width - 1 - x) / max(1, width - 1)
        shift = (
            2.2
            * distance_from_pole
            * math.sin(phase_angle + x / max(1, width - 1) * math.pi * 1.7)
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
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8), "RGBA")


def build_flag_atlases(flag: Image.Image) -> tuple[Image.Image, Image.Image]:
    atlas = Image.new("RGBA", (FRAME[0], FRAME[1] * FLAG_FRAMES))
    mask = Image.new("RGBA", atlas.size, (255, 255, 255, 0))
    for phase in range(FLAG_FRAMES):
        waved = wave_flag(flag, phase)
        position = (
            FLAG_ATTACH[0] - waved.width + 2,
            FLAG_ATTACH[1] - waved.height // 2,
        )
        frame = Image.new("RGBA", FRAME)
        frame.alpha_composite(waved, position)
        atlas.alpha_composite(frame, (0, phase * FRAME[1]))
        mask_frame = Image.new("RGBA", FRAME, (255, 255, 255, 0))
        strength = waved.getchannel("A").point(
            lambda value: round(value * 0.82)
        )
        mask_piece = Image.new("RGBA", waved.size, (255, 255, 255, 0))
        mask_piece.putalpha(strength)
        mask_frame.alpha_composite(mask_piece, position)
        mask.alpha_composite(mask_frame, (0, phase * FRAME[1]))
    return atlas, mask


def build_shadow(building: Image.Image) -> Image.Image:
    alpha = building.getchannel("A").filter(ImageFilter.GaussianBlur(2.2))
    alpha = alpha.point(lambda value: round(value * 0.18))
    silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(silhouette, (6, 6))
    return result


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


def flag_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (0, phase * FRAME[1], FRAME[0], (phase + 1) * FRAME[1])
    )


def composed(
    building: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = building.copy()
    tinted = apply_engine_tint(
        flag_frame(flag_atlas, phase),
        flag_frame(mask_atlas, phase),
        color,
    )
    result.alpha_composite(tinted)
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
        (x, y, x + size, y + size + 38),
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
        (x + 8, y + size + 7),
        label,
        font=font(17, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    building: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1780, 1320), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Ветряная ловушка — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "Корпус 64×64; восемь фаз флага вынесены в отдельный слой",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    for phase in range(FLAG_FRAMES):
        draw_card(
            board,
            composed(
                building,
                flag_atlas,
                mask_atlas,
                phase,
                HOUSE_COLORS["Ордос"],
            ),
            34 + phase * 216,
            110,
            190,
            f"фаза {phase}",
        )

    draw.text(
        (34, 360),
        "Цвет Дома — меняется только ткань флага",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    draw_card(
        board,
        composed(
            building,
            flag_atlas,
            mask_atlas,
            2,
            HOUSE_COLORS["Харконнены"],
        ),
        34,
        405,
        300,
        "Харконнены",
    )
    draw_card(
        board,
        composed(
            building,
            flag_atlas,
            mask_atlas,
            4,
            HOUSE_COLORS["Атрейдесы"],
        ),
        370,
        405,
        300,
        "Атрейдесы",
    )
    draw_card(
        board,
        composed(
            building,
            flag_atlas,
            mask_atlas,
            6,
            HOUSE_COLORS["Ордос"],
        ),
        706,
        405,
        300,
        "Ордос",
    )
    draw_card(board, building, 1042, 405, 300, "база без ткани")
    draw_card(
        board,
        flag_frame(mask_atlas, 0),
        1378,
        405,
        300,
        "маска флага",
    )

    draw.text(
        (34, 790),
        "Оригинальный контракт и проверка границ",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    if CLASSIC.is_file():
        classic = Image.open(CLASSIC).convert("RGBA")
        draw_card(board, classic, 34, 835, 360, "оригинал 64×64")
    draw_card(
        board,
        composed(
            building,
            flag_atlas,
            mask_atlas,
            0,
            HOUSE_COLORS["Ордос"],
        ),
        430,
        835,
        360,
        "HD4 256×256",
    )
    draw.text(
        (850, 875),
        "• три воздухозаборника\n"
        "• исходная компоновка 2×2\n"
        "• нижняя граница неизменна\n"
        "• отдельная детерминированная тень\n"
        "• ткань не запечена в корпус",
        font=font(23),
        fill=(204, 208, 213, 255),
        spacing=16,
    )
    draw.text(
        (34, 1260),
        "Предварительный просмотр — в игру не установлено.",
        font=font(20),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(
    building: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> None:
    frames = []
    for phase in range(FLAG_FRAMES):
        sprite = composed(
            building,
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
        duration=125,
        loop=0,
        disposal=2,
    )


def validate(
    building: Image.Image,
    shadow: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> dict[str, object]:
    if building.size != FRAME or shadow.size != FRAME:
        raise AssertionError("building or shadow dimensions changed")
    if flag_atlas.size != (FRAME[0], FRAME[1] * FLAG_FRAMES):
        raise AssertionError("flag atlas dimensions changed")
    if mask_atlas.size != flag_atlas.size:
        raise AssertionError("flag mask dimensions changed")
    for name, image in (
        ("building", building),
        ("shadow", shadow),
        ("flag", flag_atlas),
        ("flag mask", mask_atlas),
    ):
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is empty")
    box = building.getchannel("A").getbbox()
    if box is None or box[0] < 2 or box[1] < 2 or box[2] > 254 or box[3] > 254:
        raise AssertionError(f"building touches frame edge: {box}")
    flag_shapes = {
        flag_frame(flag_atlas, phase).getchannel("A").tobytes()
        for phase in range(FLAG_FRAMES)
    }
    if len(flag_shapes) != FLAG_FRAMES:
        raise AssertionError("flag phases are not unique")
    mask_pixels = int(
        np.count_nonzero(np.asarray(mask_atlas.getchannel("A")) > 8)
    )
    return {
        "resource": "BUILD_WINDTRAP",
        "resource_id": 40,
        "shadow_id": 41,
        "logical_frame": list(LOGICAL_FRAME),
        "hd4_frame": list(FRAME),
        "base_frames": 1,
        "flag_frames": FLAG_FRAMES,
        "flag_resource": "BUILD_WINDTRAP_FLAG",
        "flag_mask": "HM_BUILD_WINDTRAP_FLAG",
        "building_alpha_bbox_hd4": list(box),
        "flag_mask_pixels": mask_pixels,
        "unique_flag_phases": len(flag_shapes),
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    building = fit_building(Image.open(SOURCE).convert("RGBA"))
    flag = extract_flag(Image.open(USER_REFERENCE).convert("RGBA"))
    flag_atlas, mask_atlas = build_flag_atlases(flag)
    shadow = build_shadow(building)
    validation = validate(building, shadow, flag_atlas, mask_atlas)

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    flag_atlas.save(FLAG_OUT, optimize=True)
    mask_atlas.save(FLAG_MASK_OUT, optimize=True)
    building.resize((128, 128), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_WINDTRAP_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(building, flag_atlas, mask_atlas).save(
        REVIEW_OUT,
        optimize=True,
    )
    build_animation(building, flag_atlas, mask_atlas)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(USER_REFERENCE),
        "generated_base": str(SOURCE),
        "classic_contract": str(CLASSIC),
        "animation_contract": (
            "base remains one 64x64 frame; eight House-colored flag phases "
            "are an appended overlay"
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
