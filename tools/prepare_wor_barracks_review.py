#!/usr/bin/env python3
"""Build an approval-ready HD4 WOR Barracks with an animated House flag."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "wor_barracks_review_v1"
SOURCE = OUTPUT / "wor_barracks_alpha.png"
FLAG_SOURCE = ROOT / "artifacts" / "barracks_review_v1" / "twin_flags_alpha.png"
CLASSIC = OUTPUT / "0042_BUILD_WOR_CLASSIC.png"

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
FLAG_FRAMES = 8
FLAG_SIZE = (76, 98)
FLAG_POSITION = (12, 151)

BUILDING_OUT = OUTPUT / "BUILD_WOR_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_WOR_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_WOR_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_WOR_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_WOR_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_WOR_ANIMATION_PREVIEW.gif"
MANIFEST_OUT = OUTPUT / "manifest.json"

HOUSE_COLORS = (
    ("Атрейдесы", (54, 112, 245)),
    ("Харконнены", (230, 42, 38)),
    ("Ордос", (41, 211, 82)),
    ("Фремены", (225, 178, 63)),
    ("Сардаукары", (126, 75, 194)),
    ("Наёмники", (43, 190, 196)),
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def fit_building(source: Image.Image) -> Image.Image:
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated WOR Barracks are transparent")
    subject = source.crop(box)
    max_size = (244, 242)
    scale = min(max_size[0] / subject.width, max_size[1] / subject.height)
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", FRAME)
    frame.alpha_composite(
        subject,
        (
            (FRAME[0] - subject.width) // 2,
            FRAME[1] - subject.height - 6,
        ),
    )
    return frame


def extract_single_flag(source: Image.Image) -> tuple[Image.Image, Image.Image]:
    rgba = np.asarray(source.convert("RGBA"), dtype=np.uint8)
    labels, count = ndimage.label(rgba[:, :, 3] > 8)
    components = []
    for label_id in range(1, count + 1):
        ys, xs = np.nonzero(labels == label_id)
        if len(xs) > 100:
            components.append((len(xs), label_id, xs, ys))
    if len(components) < 2:
        raise AssertionError("the approved source does not contain two flags")

    # Use the larger left-hand assembly.  Its cloth waves away from the pole
    # and remains readable over the dark front-left roof of BUILD_WOR.
    components.sort(reverse=True)
    _, label_id, xs, ys = components[0]
    margin = 4
    box = (
        max(0, int(xs.min()) - margin),
        max(0, int(ys.min()) - margin),
        min(source.width, int(xs.max()) + margin + 1),
        min(source.height, int(ys.max()) + margin + 1),
    )
    component_mask = labels[box[1]:box[3], box[0]:box[2]] == label_id
    crop = rgba[box[1]:box[3], box[0]:box[2]].copy()
    crop[~component_mask] = 0

    red, green, blue, alpha = (crop[:, :, index] for index in range(4))
    fabric_selection = (
        (alpha > 6)
        & (green > 48)
        & (green.astype(np.float32) > red * 1.18)
        & (green.astype(np.float32) > blue * 1.12)
    )
    fabric_selection = ndimage.binary_dilation(
        fabric_selection,
        iterations=2,
    )
    fabric_rgba = crop.copy()
    fabric_rgba[:, :, 3] = np.where(
        fabric_selection,
        crop[:, :, 3],
        0,
    )
    pole_rgba = crop.copy()
    pole_rgba[fabric_selection] = 0

    pole = Image.fromarray(pole_rgba, "RGBA").resize(
        FLAG_SIZE,
        Image.Resampling.LANCZOS,
    )
    fabric = Image.fromarray(fabric_rgba, "RGBA").resize(
        FLAG_SIZE,
        Image.Resampling.LANCZOS,
    )
    if pole.getchannel("A").getbbox() is None:
        raise AssertionError("flag pole extraction failed")
    if fabric.getchannel("A").getbbox() is None:
        raise AssertionError("flag fabric extraction failed")
    return pole, fabric


def wave_fabric(fabric: Image.Image, phase: int) -> Image.Image:
    source = np.asarray(fabric.convert("RGBA"), dtype=np.float32)
    height, width = source.shape[:2]
    output = np.zeros_like(source)
    phase_angle = phase * 2.0 * math.pi / FLAG_FRAMES
    for x in range(width):
        distance_from_pole = (width - 1 - x) / max(1, width - 1)
        shift = (
            2.4
            * distance_from_pole
            * math.sin(
                phase_angle
                + x / max(1, width - 1) * math.pi * 1.75
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
    pole: Image.Image,
    fabric: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    atlas_size = (FRAME[0], FRAME[1] * FLAG_FRAMES)
    atlas = Image.new("RGBA", atlas_size)
    mask_atlas = Image.new("RGBA", atlas_size)
    for phase in range(FLAG_FRAMES):
        waved = wave_fabric(fabric, phase)
        frame = Image.new("RGBA", FRAME)
        frame.alpha_composite(pole, FLAG_POSITION)
        frame.alpha_composite(waved, FLAG_POSITION)
        atlas.alpha_composite(frame, (0, phase * FRAME[1]))

        mask_piece = Image.new("RGBA", waved.size, (255, 255, 255, 0))
        mask_piece.putalpha(waved.getchannel("A"))
        mask_frame = Image.new("RGBA", FRAME)
        mask_frame.alpha_composite(mask_piece, FLAG_POSITION)
        mask_atlas.alpha_composite(mask_frame, (0, phase * FRAME[1]))
    return atlas, mask_atlas


def build_shadow(building: Image.Image) -> Image.Image:
    alpha = building.getchannel("A").filter(ImageFilter.GaussianBlur(1.7))
    alpha = alpha.point(lambda value: round(value * 0.18))
    silhouette = Image.new("RGBA", FRAME, (6, 5, 4, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(silhouette)
    return result


def flag_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (0, phase * FRAME[1], FRAME[0], (phase + 1) * FRAME[1])
    )


def apply_house_color(
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
        rgba[:, :, 0] * 0.299
        + rgba[:, :, 1] * 0.587
        + rgba[:, :, 2] * 0.114
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
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = building.copy()
    result.alpha_composite(
        apply_house_color(
            flag_frame(flag_atlas, phase),
            flag_frame(mask_atlas, phase),
            color,
        )
    )
    return result


def checkerboard(size: tuple[int, int], cell: int = 18) -> Image.Image:
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    colors = ((33, 36, 42, 255), (45, 49, 57, 255))
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            draw.rectangle(
                (x, y, x + cell - 1, y + cell - 1),
                fill=colors[((x // cell) + (y // cell)) & 1],
            )
    return image


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
        radius=8,
        fill=(20, 24, 29, 245),
        outline=(146, 105, 46, 255),
        width=2,
    )
    background = checkerboard((size, size), 18)
    board.alpha_composite(background, (x, y))
    board.alpha_composite(
        sprite.resize((size, size), Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.text(
        (x + 8, y + size + 6),
        label,
        font=font(17, True),
        fill=(234, 217, 180, 255),
    )


def build_review(
    building: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1760, 1250), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "КАЗАРМЫ ВОР · HD4 · ФЛАГ ДОМА",
        font=font(34, True),
        fill=(237, 218, 177, 255),
    )
    draw.text(
        (34, 70),
        "BUILD_WOR: корпус 64×64, площадь 2×2, один флаг, 8 фаз",
        font=font(19),
        fill=(190, 197, 206, 255),
    )

    for phase in range(FLAG_FRAMES):
        draw_card(
            board,
            composed(
                building,
                flag_atlas,
                mask_atlas,
                phase,
                HOUSE_COLORS[2][1],
            ),
            34 + phase * 214,
            108,
            188,
            f"фаза {phase}",
        )

    draw.text(
        (34, 350),
        "Цвета фракций · корпус остаётся нейтральным",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, (name, color) in enumerate(HOUSE_COLORS):
        draw_card(
            board,
            composed(
                building,
                flag_atlas,
                mask_atlas,
                (index + 1) % FLAG_FRAMES,
                color,
            ),
            34 + index * 284,
            395,
            258,
            name,
        )

    draw.text(
        (34, 715),
        "Сверка с классическим атласом",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    draw_card(board, classic, 34, 760, 360, "классика 64×64")
    draw_card(
        board,
        composed(
            building,
            flag_atlas,
            mask_atlas,
            0,
            HOUSE_COLORS[1][1],
        ),
        430,
        760,
        360,
        "HD4 256×256",
    )
    draw_card(
        board,
        flag_frame(mask_atlas, 0),
        826,
        760,
        360,
        "маска ткани",
    )
    draw.text(
        (1240, 800),
        "• ID корпуса 42\n"
        "• ID тени 43\n"
        "• нижняя привязка сохранена\n"
        "• флаг не меняет габариты здания\n"
        "• 8 уникальных фаз ткани\n"
        "• шесть цветов фракций\n"
        "• отдельная мягкая тень",
        font=font(22),
        fill=(207, 211, 218, 255),
        spacing=16,
    )
    draw.text(
        (34, 1210),
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
            HOUSE_COLORS[1][1],
        )
        shown = checkerboard((512, 512), 32)
        shown.alpha_composite(
            sprite.resize((512, 512), Image.Resampling.LANCZOS)
        )
        frames.append(
            shown.convert("P", palette=Image.Palette.ADAPTIVE)
        )
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
        raise AssertionError("WOR building dimensions changed")
    expected_atlas = (FRAME[0], FRAME[1] * FLAG_FRAMES)
    if flag_atlas.size != expected_atlas or mask_atlas.size != expected_atlas:
        raise AssertionError("WOR flag dimensions changed")

    building_box = building.getchannel("A").getbbox()
    shadow_box = shadow.getchannel("A").getbbox()
    for name, box in (("building", building_box), ("shadow", shadow_box)):
        if (
            box is None
            or box[0] < 1
            or box[1] < 1
            or box[2] > FRAME[0] - 1
            or box[3] > FRAME[1] - 1
        ):
            raise AssertionError(f"{name} touches boundary: {box}")

    flag_hashes = set()
    flag_boxes = []
    for phase in range(FLAG_FRAMES):
        item = flag_frame(flag_atlas, phase)
        box = item.getchannel("A").getbbox()
        if (
            box is None
            or box[0] < 1
            or box[1] < 1
            or box[2] > FRAME[0] - 1
            or box[3] > FRAME[1] - 1
        ):
            raise AssertionError(
                f"flag phase {phase} touches boundary: {box}"
            )
        flag_hashes.add(item.tobytes())
        flag_boxes.append(list(box))
    if len(flag_hashes) != FLAG_FRAMES:
        raise AssertionError("WOR flag phases are not unique")

    mask_alpha = np.asarray(mask_atlas.getchannel("A"), dtype=np.float64)
    flag_alpha = np.asarray(flag_atlas.getchannel("A"), dtype=np.float64)
    coverage = float(mask_alpha.sum() / max(flag_alpha.sum(), 1.0))
    if not 0.12 <= coverage <= 0.70:
        raise AssertionError(f"invalid flag mask coverage: {coverage:.4f}")

    return {
        "resources": {
            "building": {"id": 42, "name": "BUILD_WOR"},
            "shadow": {"id": 43, "name": "BUILD_WOR_SHADOW"},
            "flag": "BUILD_WOR_FLAG",
            "flag_mask": "HM_BUILD_WOR_FLAG",
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd2_frame": [128, 128],
        "hd4_frame": list(FRAME),
        "footprint": [2, 2],
        "building_frames": 1,
        "flag_frames": FLAG_FRAMES,
        "building_box_hd4": list(building_box),
        "shadow_box_hd4": list(shadow_box),
        "flag_boxes_hd4": flag_boxes,
        "flag_position_hd4": list(FLAG_POSITION),
        "flag_mask_coverage": round(coverage, 5),
        "installed": False,
    }


def main() -> int:
    for path in (SOURCE, FLAG_SOURCE, CLASSIC):
        if not path.is_file():
            raise FileNotFoundError(path)

    building = fit_building(Image.open(SOURCE).convert("RGBA"))
    pole, fabric = extract_single_flag(
        Image.open(FLAG_SOURCE).convert("RGBA")
    )
    flag_atlas, mask_atlas = build_flag_atlases(pole, fabric)
    shadow = build_shadow(building)
    validation = validate(building, shadow, flag_atlas, mask_atlas)

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    flag_atlas.save(FLAG_OUT, optimize=True)
    mask_atlas.save(FLAG_MASK_OUT, optimize=True)
    build_review(building, flag_atlas, mask_atlas).save(
        REVIEW_OUT,
        optimize=True,
    )
    build_animation(building, flag_atlas, mask_atlas)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "generation_mode": (
            "built-in imagegen plus deterministic 8-frame House flag"
        ),
        "validation": validation,
    }
    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
