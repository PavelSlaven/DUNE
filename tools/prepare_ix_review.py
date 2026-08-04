#!/usr/bin/env python3
"""Build an approval-ready HD House of IX with an animated House flag."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "ix_review_v1"
SOURCE = OUTPUT / "generated" / "ix_alpha.png"
USER_REFERENCE = OUTPUT / "user_reference.png"
CLASSIC = OUTPUT / "0010_BUILD_IX_CLASSIC.png"

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
ANIMATION_FRAMES = 8
FLAG_SIZE = (46, 28)

BUILDING_OUT = OUTPUT / "BUILD_IX_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_IX_SHADOW_HD4_PREVIEW.png"
OVERLAY_OUT = OUTPUT / "BUILD_IX_FLAG_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_BUILD_IX_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_IX_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_IX_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def clean_magenta_edge(image: Image.Image) -> Image.Image:
    pixels = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    edge = (
        (pixels[:, :, 0] > 145)
        & (pixels[:, :, 2] > 145)
        & (pixels[:, :, 1] < 115)
        & (pixels[:, :, 3] < 240)
    )
    pixels[edge] = 0
    return Image.fromarray(pixels, "RGBA")


def fit_building(source: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    source = clean_magenta_edge(source)
    alpha = np.asarray(source.getchannel("A")) > 0
    labels, count = ndimage.label(
        alpha,
        structure=np.ones((3, 3), dtype=np.uint8),
    )
    components: list[tuple[int, int, tuple[int, int, int, int]]] = []
    for label_id in range(1, count + 1):
        ys, xs = np.nonzero(labels == label_id)
        if len(xs) < 100:
            continue
        components.append(
            (
                len(xs),
                label_id,
                (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1),
            )
        )
    components.sort(reverse=True)
    if len(components) < 2:
        raise AssertionError("IX building and flag pole were not separated")

    _, building_id, building_box = components[0]
    _, pole_id, pole_box = components[1]
    building_mask = Image.fromarray(
        np.where(labels == building_id, 255, 0).astype(np.uint8),
        "L",
    )
    pole_mask = Image.fromarray(
        np.where(labels == pole_id, 255, 0).astype(np.uint8),
        "L",
    )

    building = source.copy()
    building.putalpha(building_mask)
    building = building.crop(building_box)
    scale = min(250 / building.width, 250 / building.height)
    building_size = (
        round(building.width * scale),
        round(building.height * scale),
    )
    building = building.resize(building_size, Image.Resampling.LANCZOS)
    building_position = (
        (FRAME[0] - building.width) // 2,
        FRAME[1] - building.height - 3,
    )

    pole = source.copy()
    pole.putalpha(pole_mask)
    pole = pole.crop(pole_box)
    pole_size = (
        max(1, round(pole.width * scale)),
        max(1, round(pole.height * scale)),
    )
    pole = pole.resize(pole_size, Image.Resampling.LANCZOS)
    pole_position = (
        round(
            building_position[0]
            + (pole_box[0] - building_box[0]) * scale
        ),
        round(
            building_position[1]
            + (pole_box[1] - building_box[1]) * scale
        ),
    )
    pole_position = (
        min(FRAME[0] - pole.width - 2, pole_position[0]),
        min(FRAME[1] - pole.height - 2, pole_position[1]),
    )

    result = Image.new("RGBA", FRAME)
    result.alpha_composite(building, building_position)
    result.alpha_composite(pole, pole_position)
    flag_attach = (
        pole_position[0] + round(pole.width * 0.32),
        pole_position[1] + round(pole.height * 0.09),
    )
    return result, flag_attach


def extract_flag(reference: Image.Image) -> Image.Image:
    rgba = np.asarray(reference.convert("RGBA"), dtype=np.float32)
    red, green, blue = (rgba[:, :, index] for index in range(3))
    selection = (
        (green > 70)
        & (green > red * 1.16)
        & (green > blue * 1.10)
    )
    labels, count = ndimage.label(
        selection,
        structure=np.ones((3, 3), dtype=np.uint8),
    )
    candidates = []
    for label_id in range(1, count + 1):
        component = labels == label_id
        ys, xs = np.nonzero(component)
        if len(xs) < 300:
            continue
        if xs.mean() > reference.width * 0.65:
            candidates.append((len(xs), component))
    if not candidates:
        raise AssertionError("unable to locate IX flag fabric")
    component = max(candidates, key=lambda item: item[0])[1]
    fabric = ndimage.binary_closing(component, iterations=2)
    fabric = ndimage.binary_dilation(fabric, iterations=2)
    alpha = np.where(fabric, 255, 0).astype(np.uint8)
    extracted = reference.convert("RGBA").copy()
    extracted.putalpha(Image.fromarray(alpha, "L"))
    box = Image.fromarray(alpha, "L").getbbox()
    if box is None:
        raise AssertionError("IX flag extraction is empty")
    return extracted.crop(box).resize(FLAG_SIZE, Image.Resampling.LANCZOS)


def wave_flag(flag: Image.Image, phase: int) -> Image.Image:
    source = np.asarray(flag.convert("RGBA"), dtype=np.float32)
    height, width = source.shape[:2]
    output = np.zeros_like(source)
    phase_angle = phase * 2.0 * math.pi / ANIMATION_FRAMES
    for x in range(width):
        distance = (width - 1 - x) / max(1, width - 1)
        shift = (
            3.0
            * distance
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


def build_flag_atlases(
    flag: Image.Image,
    attach: tuple[int, int],
) -> tuple[Image.Image, Image.Image]:
    atlas_size = (FRAME[0], FRAME[1] * ANIMATION_FRAMES)
    atlas = Image.new("RGBA", atlas_size)
    mask = Image.new("RGBA", atlas_size, (255, 255, 255, 0))
    for phase in range(ANIMATION_FRAMES):
        waved = wave_flag(flag, phase)
        position = (
            attach[0] - waved.width + 3,
            attach[1] - round(waved.height * 0.34),
        )
        frame = Image.new("RGBA", FRAME)
        frame.alpha_composite(waved, position)
        mask_frame = Image.new("RGBA", FRAME, (255, 255, 255, 0))
        mask_piece = Image.new("RGBA", waved.size, (255, 255, 255, 0))
        mask_piece.putalpha(
            waved.getchannel("A").point(lambda value: round(value * 0.86))
        )
        mask_frame.alpha_composite(mask_piece, position)
        atlas.alpha_composite(frame, (0, phase * FRAME[1]))
        mask.alpha_composite(mask_frame, (0, phase * FRAME[1]))
    return atlas, mask


def frame_from(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (
            0,
            phase * FRAME[1],
            FRAME[0],
            (phase + 1) * FRAME[1],
        )
    )


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
        apply_tint(frame_from(overlay, phase), frame_from(mask, phase), color)
    )
    return result


def build_shadow(building: Image.Image) -> Image.Image:
    alpha = building.getchannel("A").filter(ImageFilter.GaussianBlur(2.0))
    alpha = alpha.point(lambda value: round(value * 0.18))
    silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(silhouette, (4, 4))
    return result


def card(
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
        (x + 7, y + size + 5),
        label,
        font=font(16, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1780, 1190), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Центр ИКС — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "Корпус 64×64; восемь фаз флага, стойка в штатной позиции",
        font=font(19),
        fill=(187, 193, 201, 255),
    )
    for phase in range(ANIMATION_FRAMES):
        card(
            board,
            composed(building, overlay, mask, phase, HOUSE_COLORS["Ордос"]),
            34 + phase * 216,
            108,
            190,
            f"фаза {phase}",
        )

    draw.text(
        (34, 355),
        "Цвет Домов применяется только к ткани флага",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for column, (name, color) in enumerate(HOUSE_COLORS.items()):
        card(
            board,
            composed(building, overlay, mask, 1 + column * 2, color),
            34 + column * 330,
            400,
            300,
            name,
        )
    card(board, building, 1024, 400, 300, "корпус без ткани")
    card(board, frame_from(mask, 2), 1354, 400, 300, "маска флага")

    draw.text(
        (34, 780),
        "Размер и исходный контракт",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    card(board, classic, 34, 825, 260, "классика 64×64")
    card(
        board,
        composed(building, overlay, mask, 2, HOUSE_COLORS["Ордос"]),
        330,
        825,
        260,
        "HD4 256×256",
    )
    notes = (
        "• площадь здания 2×2 клетки\n"
        "• один неподвижный кадр корпуса\n"
        "• три купола и четыре угловых модуля\n"
        "• нижняя граница и ориентация сохранены\n"
        "• флаг имеет 8 уникальных фаз\n"
        "• отдельная детерминированная тень"
    )
    draw.multiline_text(
        (640, 835),
        notes,
        font=font(22),
        fill=(201, 205, 212, 255),
        spacing=13,
    )
    draw.text(
        (34, 1150),
        "Предварительный просмотр — в игру не установлено.",
        font=font(18),
        fill=(183, 188, 196, 255),
    )
    return board


def validate(
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    if building.size != FRAME:
        raise AssertionError("invalid IX HD4 building size")
    if overlay.size != (FRAME[0], FRAME[1] * ANIMATION_FRAMES):
        raise AssertionError("invalid IX flag atlas size")
    if mask.size != overlay.size:
        raise AssertionError("IX flag mask size differs")
    box = building.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("IX building is transparent")
    hashes = {
        frame_from(overlay, phase).tobytes()
        for phase in range(ANIMATION_FRAMES)
    }
    if len(hashes) != ANIMATION_FRAMES:
        raise AssertionError("IX flag phases are not unique")
    if mask.getchannel("A").getbbox() is None:
        raise AssertionError("IX flag mask is empty")
    return {
        "resources": {
            "building": {"id": 10, "name": "BUILD_IX"},
            "shadow": {"id": 11, "name": "BUILD_IX_SHADOW"},
            "overlay": "BUILD_IX_FLAG",
            "overlay_mask": "HM_BUILD_IX_FLAG",
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd4_frame": list(FRAME),
        "footprint": [2, 2],
        "base_frames": 1,
        "overlay_frames": ANIMATION_FRAMES,
        "building_box_hd4": list(box),
        "flag_mask_pixels": int(
            np.count_nonzero(np.asarray(mask.getchannel("A")))
        ),
    }


def main() -> int:
    for path in (SOURCE, USER_REFERENCE, CLASSIC):
        if not path.is_file():
            raise FileNotFoundError(path)
    source = Image.open(SOURCE).convert("RGBA")
    reference = Image.open(USER_REFERENCE).convert("RGBA")
    building, attach = fit_building(source)
    flag = extract_flag(reference)
    overlay, mask = build_flag_atlases(flag, attach)
    shadow = build_shadow(building)

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    overlay.save(OVERLAY_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    building.resize((128, 128), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_IX_HD2_PREVIEW.png",
        optimize=True,
    )
    overlay.resize((128, 1024), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_IX_FLAG_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(building, overlay, mask).save(REVIEW_OUT, optimize=True)

    animation = [
        composed(building, overlay, mask, phase, HOUSE_COLORS["Ордос"])
        .resize((640, 640), Image.Resampling.LANCZOS)
        .convert("P", palette=Image.Palette.ADAPTIVE)
        for phase in range(ANIMATION_FRAMES)
    ]
    animation[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=animation[1:],
        duration=125,
        loop=0,
        disposal=2,
    )
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(USER_REFERENCE),
        "generated_base": str(SOURCE),
        "classic_contract": str(CLASSIC),
        "generation_mode": (
            "ImageGen base plus deterministic House flag animation"
        ),
        "validation": validate(building, overlay, mask),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
