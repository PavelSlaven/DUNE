#!/usr/bin/env python3
"""Build the eight-frame HD4 refinery preview and House-color mask."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "refinery_review_v1"
SOURCE = ARTIFACT / "refinery_master_alpha.png"
SOURCE_NO_FLAG = ARTIFACT / "refinery_base_no_flag_alpha.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0028_BUILD_REFINERY.png"
)
HARVESTER = (
    ROOT
    / "artifacts"
    / "harvester_faction_preview_v1"
    / "variants"
    / "UNIT_HARVESTER_ORDOS_HD4_PREVIEW.png"
)

FRAME = (384, 256)
LOGICAL_FRAME = (96, 64)
ATLAS = (384, 2048)
FRAME_COUNT = 8
HARVESTER_DESTINATION = (120, 60)
HARVESTER_SIZE = (320, 208)
HARVESTER_DIRECTION_COLUMN = 6
FLAG_ROI = (100, 30, 170, 90)
PLATFORM_ROI = (185, 78, 380, 242)

BUILDING_OUT = ARTIFACT / "BUILD_REFINERY_HD4_PREVIEW.png"
MASK_OUT = ARTIFACT / "HOUSEMASK_BUILD_REFINERY_HD4_PREVIEW.png"
FLAG_OUT = ARTIFACT / "BUILD_REFINERY_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = ARTIFACT / "HOUSEMASK_BUILD_REFINERY_FLAG_HD4_PREVIEW.png"
HD2_OUT = ARTIFACT / "BUILD_REFINERY_HD2_PREVIEW.png"
REVIEW_OUT = ARTIFACT / "BUILD_REFINERY_REVIEW.png"
ANIMATION_OUT = ARTIFACT / "BUILD_REFINERY_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def smoothstep(low: float, high: float, value: np.ndarray) -> np.ndarray:
    normalized = np.clip((value - low) / (high - low), 0.0, 1.0)
    return normalized * normalized * (3.0 - 2.0 * normalized)


def green_selection(image: Image.Image) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    dominance = (green - np.maximum(red, blue)) / 255.0
    purity = (green - np.maximum(red, blue)) / np.maximum(green, 1.0)
    return (
        smoothstep(0.035, 0.20, dominance)
        * smoothstep(0.10, 0.45, purity)
        * smoothstep(25.0, 75.0, green)
        * (alpha / 255.0)
    )


def crop_selection(
    selection: np.ndarray,
    box: tuple[int, int, int, int],
) -> np.ndarray:
    result = np.zeros_like(selection)
    left, top, right, bottom = box
    result[top:bottom, left:right] = selection[top:bottom, left:right]
    return result


def extend_platform_to_frame_edge(image: Image.Image) -> Image.Image:
    """Give the full-size harvester enough deck beneath its lower body."""
    result = image.copy()
    left, top, right, source_bottom = 180, 184, FRAME[0], 238
    platform_bottom = result.crop((left, top, right, source_bottom))
    platform_bottom = platform_bottom.resize(
        (right - left, FRAME[1] - top),
        Image.Resampling.LANCZOS,
    )
    result.paste(
        Image.new("RGBA", (right - left, FRAME[1] - top)),
        (left, top),
    )
    result.alpha_composite(platform_bottom, (left, top))
    return result


def largest_component(selection: np.ndarray, minimum: int) -> np.ndarray:
    labels, count = ndimage.label(
        selection > 0.10,
        structure=np.ones((3, 3), dtype=np.uint8),
    )
    best = np.zeros_like(selection, dtype=bool)
    best_size = 0
    for label_id in range(1, count + 1):
        component = labels == label_id
        size = int(np.count_nonzero(component))
        if size >= minimum and size > best_size:
            best = component
            best_size = size
    if best_size == 0:
        raise AssertionError("unable to locate required green component")
    expanded = ndimage.binary_dilation(best, iterations=2)
    return np.where(expanded, np.maximum(selection, 0.70), 0.0)


def main_platform_components(
    selection: np.ndarray,
) -> list[tuple[np.ndarray, tuple[float, float]]]:
    selection = crop_selection(selection, PLATFORM_ROI)
    labels, count = ndimage.label(
        selection > 0.12,
        structure=np.ones((3, 3), dtype=np.uint8),
    )
    components: list[tuple[np.ndarray, tuple[float, float]]] = []
    for label_id in range(1, count + 1):
        component = labels == label_id
        if np.count_nonzero(component) < 180:
            continue
        ys, xs = np.nonzero(component)
        softened = Image.fromarray(
            np.where(component, 255, 0).astype(np.uint8),
            "L",
        ).filter(ImageFilter.GaussianBlur(0.65))
        components.append(
            (
                np.asarray(softened, dtype=np.float32) / 255.0,
                (float(xs.mean()), float(ys.mean())),
            )
        )
    if len(components) != 7:
        raise AssertionError(
            f"expected seven main diode groups, got {len(components)}"
        )
    return components


def order_components(
    components: list[tuple[np.ndarray, tuple[float, float]]],
) -> list[np.ndarray]:
    # Clockwise chase: top, upper-right, lower-right, bottom,
    # lower-left, upper-left, center.
    center_x, center_y = 268.0, 156.0

    def chase_key(item: tuple[np.ndarray, tuple[float, float]]) -> int:
        _, (x, y) = item
        if abs(x - center_x) < 18 and abs(y - center_y) < 24:
            return 6
        if y < 120:
            return 0
        if x > center_x + 25 and y < center_y:
            return 1
        if x > center_x + 25 and y >= center_y:
            return 2
        if y > 194:
            return 3
        if x < center_x - 25 and y >= center_y:
            return 4
        return 5

    ordered = sorted(components, key=chase_key)
    if [chase_key(item) for item in ordered] != list(range(7)):
        raise AssertionError("diode groups do not match the expected layout")
    return [item[0] for item in ordered]


def neutralize(
    image: Image.Image,
    selection: np.ndarray,
    cool: bool,
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    rgb = rgba[:, :, :3]
    luminance = (
        0.299 * rgb[:, :, 0]
        + 0.587 * rgb[:, :, 1]
        + 0.114 * rgb[:, :, 2]
    )
    if cool:
        target = np.dstack(
            (
                luminance * 0.74,
                luminance * 0.80,
                luminance * 0.88,
            )
        )
    else:
        target = np.dstack(
            (
                luminance * 0.98,
                luminance,
                luminance * 1.03,
            )
        )
    amount = np.clip(selection * 1.25, 0.0, 1.0)[:, :, None]
    rgba[:, :, :3] = rgb * (1.0 - amount) + target * amount
    rgba[rgba[:, :, 3] == 0] = 0
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def make_white_mask(selection: np.ndarray) -> Image.Image:
    alpha = np.clip(selection * 255.0, 0, 255).astype(np.uint8)
    rgba = np.full((*alpha.shape, 4), 255, dtype=np.uint8)
    rgba[:, :, 3] = alpha
    rgba[alpha == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def warp_flag(
    layer: Image.Image,
    phase: int,
) -> Image.Image:
    rgba = np.asarray(layer.convert("RGBA"), dtype=np.uint8)
    output = np.zeros_like(rgba)
    left, top, right, bottom = FLAG_ROI
    width = right - left
    phase_angle = phase * 2.0 * np.pi / FRAME_COUNT
    for x in range(left, right):
        normalized = (x - left) / max(1, width - 1)
        anchor_weight = 1.0 - normalized
        raw = np.sin(normalized * np.pi * 2.25 + phase_angle)
        anchored = raw - np.sin(np.pi * 2.25 + phase_angle)
        offset = int(round(3.5 * anchor_weight * anchored))
        source_top = max(top, top - offset)
        source_bottom = min(bottom, bottom - offset)
        target_top = source_top + offset
        target_bottom = source_bottom + offset
        if source_bottom > source_top:
            output[target_top:target_bottom, x] = rgba[
                source_top:source_bottom,
                x,
            ]
    return Image.fromarray(output, "RGBA")


def set_component_brightness(
    image: Image.Image,
    component: np.ndarray,
    factor: float,
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    strength = component[:, :, None]
    adjusted = np.clip(rgba[:, :, :3] * factor, 0.0, 255.0)
    rgba[:, :, :3] = (
        rgba[:, :, :3] * (1.0 - strength) + adjusted * strength
    )
    rgba[rgba[:, :, 3] == 0] = 0
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def frame_states(frame_index: int) -> list[float]:
    if frame_index == 7:
        return [0.65, 0.65, 0.65, 0.85, 0.65, 0.65, 1.0]
    states = [0.10] * 7
    states[frame_index] = 1.0
    states[(frame_index - 1) % 7] = 0.38
    if frame_index in (2, 5):
        states[6] = max(states[6], 0.62)
    return states


def build_frames() -> tuple[Image.Image, Image.Image, Image.Image, Image.Image]:
    source = Image.open(SOURCE).convert("RGBA").resize(
        FRAME,
        Image.Resampling.LANCZOS,
    )
    clean = Image.open(SOURCE_NO_FLAG).convert("RGBA").resize(
        FRAME,
        Image.Resampling.LANCZOS,
    )
    source = extend_platform_to_frame_edge(source)
    clean = extend_platform_to_frame_edge(clean)
    source_green = green_selection(source)
    clean_green = green_selection(clean)

    flag_selection = largest_component(
        crop_selection(source_green, FLAG_ROI),
        minimum=100,
    )
    platform_selection = crop_selection(clean_green, PLATFORM_ROI)
    platform_components = order_components(
        main_platform_components(clean_green)
    )

    neutral_base = neutralize(clean, platform_selection, cool=True)
    flag_pixels = np.asarray(source, dtype=np.uint8).copy()
    flag_pixels[:, :, 3] = np.clip(
        flag_pixels[:, :, 3].astype(np.float32) * flag_selection,
        0,
        255,
    ).astype(np.uint8)
    flag_pixels[flag_pixels[:, :, 3] == 0, :3] = 0
    neutral_flag = neutralize(
        Image.fromarray(flag_pixels, "RGBA"),
        flag_selection,
        cool=False,
    )
    raw_flag_mask = make_white_mask(flag_selection)

    building_atlas = Image.new("RGBA", ATLAS)
    mask_atlas = Image.new("RGBA", ATLAS)
    flag_atlas = Image.new("RGBA", ATLAS)
    flag_mask_atlas = Image.new("RGBA", ATLAS)

    for frame_index in range(FRAME_COUNT):
        states = frame_states(frame_index)
        frame = neutral_base.copy()
        diode_mask = np.zeros((FRAME[1], FRAME[0]), dtype=np.float32)
        for component, state in zip(platform_components, states, strict=True):
            frame = set_component_brightness(
                frame,
                component,
                0.58 + state * 0.82,
            )
            diode_mask = np.maximum(diode_mask, component * state)
            if state > 0.35:
                glow = Image.fromarray(
                    np.clip(component * 255.0, 0, 255).astype(np.uint8),
                    "L",
                ).filter(ImageFilter.GaussianBlur(3.0))
                diode_mask = np.maximum(
                    diode_mask,
                    np.asarray(glow, dtype=np.float32)
                    / 255.0
                    * state
                    * 0.28,
                )

        flag = warp_flag(neutral_flag, frame_index)
        flag_mask = warp_flag(raw_flag_mask, frame_index)

        combined_mask = make_white_mask(diode_mask)
        y = frame_index * FRAME[1]
        building_atlas.alpha_composite(frame, (0, y))
        mask_atlas.alpha_composite(combined_mask, (0, y))
        flag_atlas.alpha_composite(flag, (0, y))
        flag_mask_atlas.alpha_composite(flag_mask, (0, y))

    return building_atlas, mask_atlas, flag_atlas, flag_mask_atlas


def apply_engine_tint(
    neutral: Image.Image,
    mask: Image.Image,
    target: tuple[int, int, int],
) -> Image.Image:
    base = np.asarray(neutral.convert("RGBA"), dtype=np.float32)
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    strength = (
        mask_rgba[:, :, 3] / 255.0
        * np.max(mask_rgba[:, :, :3], axis=2)
        / 255.0
    )
    luminance = (
        0.299 * base[:, :, 0]
        + 0.587 * base[:, :, 1]
        + 0.114 * base[:, :, 2]
    ) / 128.0
    colored = np.empty_like(base[:, :, :3])
    for channel, target_value in enumerate(target):
        colored[:, :, channel] = np.minimum(
            255.0,
            target_value * luminance,
        )
    output = base.copy()
    output[:, :, :3] = (
        base[:, :, :3] * (1.0 - strength[:, :, None])
        + colored * strength[:, :, None]
    )
    output[base[:, :, 3] == 0] = 0
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8), "RGBA")


def atlas_frame(atlas: Image.Image, index: int) -> Image.Image:
    top = index * FRAME[1]
    return atlas.crop((0, top, FRAME[0], top + FRAME[1]))


def compose_house_atlas(
    building: Image.Image,
    mask: Image.Image,
    flag: Image.Image,
    flag_mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    tinted_building = apply_engine_tint(building, mask, color)
    tinted_flag = apply_engine_tint(flag, flag_mask, color)
    result = tinted_building.copy()
    for index in range(FRAME_COUNT):
        frame = atlas_frame(result, index)
        frame.alpha_composite(atlas_frame(tinted_flag, index))
        result.paste(frame, (0, index * FRAME[1]))
    return result


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def draw_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    label: str,
    size: tuple[int, int] = (288, 192),
) -> None:
    draw = ImageDraw.Draw(board)
    width, height = size
    draw.rounded_rectangle(
        (x - 7, y - 7, x + width + 7, y + height + 35),
        radius=8,
        fill=(23, 27, 32, 255),
        outline=(139, 108, 52, 255),
        width=2,
    )
    board.alpha_composite(
        sprite.resize(size, Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.text(
        (x + 8, y + height + 5),
        label,
        font=font(17, True),
        fill=(232, 216, 181, 255),
    )


def build_review(
    building: Image.Image,
    mask: Image.Image,
    flag: Image.Image,
    flag_mask: Image.Image,
) -> Image.Image:
    green = compose_house_atlas(
        building,
        mask,
        flag,
        flag_mask,
        HOUSE_COLORS["Ордос"],
    )
    red = compose_house_atlas(
        building,
        mask,
        flag,
        flag_mask,
        HOUSE_COLORS["Харконнены"],
    )
    blue = compose_house_atlas(
        building,
        mask,
        flag,
        flag_mask,
        HOUSE_COLORS["Атрейдесы"],
    )
    board = Image.new("RGBA", (1800, 1430), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (36, 24),
        "Перерабатывающий завод — HD4, 8 кадров",
        font=font(34, True),
        fill=(235, 218, 180, 255),
    )
    draw.text(
        (36, 70),
        "Площадка с диодами принимает харвестер; флаг и свет окрашиваются маской",
        font=font(19),
        fill=(188, 194, 202, 255),
    )

    for index in range(8):
        column = index % 4
        row = index // 4
        draw_card(
            board,
            atlas_frame(green, index),
            40 + column * 430,
            125 + row * 295,
            f"кадр {index}: "
            + ("разгрузка" if index == 7 else "бегущий сигнал"),
            (360, 240),
        )

    occupied = atlas_frame(green, 7)
    if HARVESTER.is_file():
        harvester_atlas = Image.open(HARVESTER).convert("RGBA")
        # N heading, first movement row. This uses the exact rectangle from
        # drawHarvesterOnRefineryPad().
        source_left = HARVESTER_DIRECTION_COLUMN * HARVESTER_SIZE[0]
        harvester = harvester_atlas.crop(
            (
                source_left,
                0,
                source_left + HARVESTER_SIZE[0],
                HARVESTER_SIZE[1],
            )
        )
        occupied.alpha_composite(harvester, HARVESTER_DESTINATION)

    draw.text(
        (36, 725),
        "Проверка площадки реальным спрайтом харвестера",
        font=font(25, True),
        fill=(226, 190, 100, 255),
    )
    draw_card(
        board,
        occupied,
        40,
        775,
        "кадр 7: машина поверх площадки, не внутри картинки",
        (576, 384),
    )
    draw_card(
        board,
        atlas_frame(mask, 3),
        670,
        775,
        "маска: белое = цвет фракции",
        (432, 288),
    )
    draw_card(
        board,
        atlas_frame(red, 2),
        1150,
        775,
        "Харконнены",
        (288, 192),
    )
    draw_card(
        board,
        atlas_frame(blue, 5),
        1470,
        775,
        "Атрейдесы",
        (288, 192),
    )
    draw.text(
        (36, 1195),
        "Восемь фаз флага",
        font=font(23, True),
        fill=(226, 190, 100, 255),
    )
    for index in range(FRAME_COUNT):
        flag_frame = atlas_frame(green, index).crop((96, 24, 176, 96))
        x = 40 + index * 215
        y = 1240
        draw.rounded_rectangle(
            (x - 4, y - 4, x + 164, y + 148),
            radius=6,
            fill=(23, 27, 32, 255),
            outline=(92, 79, 51, 255),
            width=1,
        )
        board.alpha_composite(
            flag_frame.resize((160, 144), Image.Resampling.LANCZOS),
            (x, y),
        )
        draw.text(
            (x + 68, y + 116),
            str(index),
            font=font(16, True),
            fill=(232, 216, 181, 255),
        )
    draw.text(
        (36, 1400),
        "Предварительный просмотр — в игру не установлено.",
        font=font(18),
        fill=(176, 181, 187, 255),
    )
    return board


def build_animation(
    building: Image.Image,
    mask: Image.Image,
    flag: Image.Image,
    flag_mask: Image.Image,
) -> None:
    green = compose_house_atlas(
        building,
        mask,
        flag,
        flag_mask,
        HOUSE_COLORS["Ордос"],
    )
    frames: list[Image.Image] = []
    harvester_atlas = (
        Image.open(HARVESTER).convert("RGBA")
        if HARVESTER.is_file()
        else None
    )
    for index in range(FRAME_COUNT):
        sprite = atlas_frame(green, index)
        if index == 7 and harvester_atlas is not None:
            source_left = (
                HARVESTER_DIRECTION_COLUMN * HARVESTER_SIZE[0]
            )
            harvester = harvester_atlas.crop(
                (
                    source_left,
                    0,
                    source_left + HARVESTER_SIZE[0],
                    HARVESTER_SIZE[1],
                )
            )
            sprite.alpha_composite(harvester, HARVESTER_DESTINATION)
        shown = Image.new("RGBA", (768, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            sprite.resize((768, 512), Image.Resampling.LANCZOS)
        )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=[170, 170, 170, 170, 170, 170, 170, 650],
        loop=0,
        disposal=2,
    )


def validate(
    building: Image.Image,
    mask: Image.Image,
    flag: Image.Image,
    flag_mask: Image.Image,
) -> dict[str, object]:
    if building.size != ATLAS or mask.size != ATLAS:
        raise AssertionError("refinery atlas dimensions changed")
    if flag.size != ATLAS or flag_mask.size != ATLAS:
        raise AssertionError("flag atlas dimensions changed")
    if building.getchannel("A").getbbox() is None:
        raise AssertionError("refinery atlas is transparent")
    if mask.getchannel("A").getbbox() is None:
        raise AssertionError("House mask is empty")

    base_frames = [atlas_frame(building, index) for index in range(8)]
    mask_frames = [atlas_frame(mask, index) for index in range(8)]
    if len({frame.getchannel("A").tobytes() for frame in flag_mask_frames(flag_mask)}) < 4:
        raise AssertionError("flag animation has fewer than four distinct poses")
    if len({frame.tobytes() for frame in mask_frames}) != 8:
        raise AssertionError("diode/flag mask does not contain eight phases")

    frame7 = base_frames[7]
    harvester_atlas = Image.open(HARVESTER).convert("RGBA")
    source_left = HARVESTER_DIRECTION_COLUMN * HARVESTER_SIZE[0]
    harvester = harvester_atlas.crop(
        (
            source_left,
            0,
            source_left + HARVESTER_SIZE[0],
            HARVESTER_SIZE[1],
        )
    )
    harvester_layer = Image.new("RGBA", FRAME)
    harvester_layer.alpha_composite(harvester, HARVESTER_DESTINATION)
    vehicle_pixels = (
        np.asarray(harvester_layer.getchannel("A"), dtype=np.uint8) > 16
    )
    building_pixels = (
        np.asarray(frame7.getchannel("A"), dtype=np.uint8) > 128
    )
    dock_coverage = float(
        np.count_nonzero(vehicle_pixels & building_pixels)
    ) / max(1, np.count_nonzero(vehicle_pixels))
    if dock_coverage < 0.92:
        raise AssertionError(
            f"harvester dock coverage is only {dock_coverage:.1%}"
        )

    mask_alpha = np.asarray(mask.getchannel("A"), dtype=np.uint8)
    mask_coverage = float(np.count_nonzero(mask_alpha > 8)) / mask_alpha.size
    if not 0.01 < mask_coverage < 0.22:
        raise AssertionError(
            f"unexpected House-mask coverage: {mask_coverage:.1%}"
        )
    return {
        "frame_count": FRAME_COUNT,
        "logical_frame": list(LOGICAL_FRAME),
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "harvester_destination_logical": [30, 15, 80, 52],
        "harvester_destination_hd4": [
            *HARVESTER_DESTINATION,
            *HARVESTER_SIZE,
        ],
        "harvester_direction": "S",
        "harvester_scale_percent": 100,
        "dock_opaque_coverage_percent": round(dock_coverage * 100.0, 2),
        "house_mask_coverage_percent": round(mask_coverage * 100.0, 2),
        "distinct_flag_poses": len(
            {
                frame.getchannel("A").tobytes()
                for frame in flag_mask_frames(flag_mask)
            }
        ),
    }


def flag_mask_frames(atlas: Image.Image) -> list[Image.Image]:
    return [atlas_frame(atlas, index) for index in range(FRAME_COUNT)]


def main() -> None:
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    building, mask, flag, flag_mask = build_frames()
    validation = validate(building, mask, flag, flag_mask)
    building.save(BUILDING_OUT)
    mask.save(MASK_OUT)
    flag.save(FLAG_OUT)
    flag_mask.save(FLAG_MASK_OUT)
    building.resize((192, 1024), Image.Resampling.LANCZOS).save(HD2_OUT)
    build_review(building, mask, flag, flag_mask).save(REVIEW_OUT)
    build_animation(building, mask, flag, flag_mask)

    manifest = {
        "resource": "BUILD_REFINERY",
        "resource_id": 28,
        "shadow_id": 29,
        "status": "preview_not_integrated",
        "source_reference": str(SOURCE),
        "classic_contract": str(CLASSIC),
        "frame_meaning": {
            "0-6": "harvester approach; chasing diode signal",
            "7": "harvester unloading on the diode platform",
        },
        "animation": {
            "diodes": "seven-state chase plus unloading state",
            "flag": "eight wind-wave poses; intended as independent overlay",
        },
        "house_mask": "animated platform diodes only",
        "flag_mask": "flag fabric only; independent overlay",
        "validation": validation,
    }
    (ARTIFACT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
