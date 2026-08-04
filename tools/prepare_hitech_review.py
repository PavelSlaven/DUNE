#!/usr/bin/env python3
"""Build an approval-ready HD high-tech factory and animated House flag."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from prepare_soldiers_review import apply_engine_tint


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "hitech_review_v1"
SOURCE = OUTPUT / "hitech_wide_alpha.png"
FLAG_REFERENCE = (
    ROOT
    / "artifacts"
    / "windtrap_review_v1"
    / "BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)
FLAG_MASK_REFERENCE = (
    ROOT
    / "artifacts"
    / "windtrap_review_v1"
    / "HM_BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)

FRAME = (384, 256)
LOGICAL_FRAME = (96, 64)
BUILDING_FRAMES = 7
FLAG_FRAMES = 8
DYNAMIC_BAY = (114, 60, 288, 248)
LED_CENTERS = (
    (310, 21),
    (355, 78),
    (310, 137),
    (264, 78),
)
LED_RADIUS = 14
FLAG_POSITION = (94, 96)

BUILDING_OUT = OUTPUT / "BUILD_HIGHTECH_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_HIGHTECH_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_HIGHTECH_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_HIGHTECH_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_HIGHTECH_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_HIGHTECH_ANIMATION_PREVIEW.gif"
MANIFEST_OUT = OUTPUT / "manifest.json"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
    "Император": (210, 0, 120),
    "Наёмники": (218, 170, 132),
    "Фримены": (0, 205, 220),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def projection_intervals(image: Image.Image) -> list[tuple[int, int]]:
    alpha = np.asarray(image.getchannel("A"))
    active = np.count_nonzero(alpha > 12, axis=0) > 0
    intervals: list[tuple[int, int]] = []
    start: int | None = None
    for x, value in enumerate(active):
        if value and start is None:
            start = x
        if start is not None and (not value or x == len(active) - 1):
            end = x if not value else x + 1
            if end - start > 20:
                intervals.append((start, end))
            start = None
    if len(intervals) != BUILDING_FRAMES:
        raise AssertionError(
            f"expected {BUILDING_FRAMES} factories, found {len(intervals)}"
        )
    return intervals


def source_frames(source: Image.Image) -> list[Image.Image]:
    frames: list[Image.Image] = []
    for left, right in projection_intervals(source):
        part = source.crop((left, 0, right, source.height))
        box = part.getchannel("A").getbbox()
        if box is None:
            raise AssertionError("empty factory state")
        frames.append(part.crop(box))
    return frames


def normalized_building_frames(source: Image.Image) -> list[Image.Image]:
    parts = source_frames(source)
    canonical_width = max(part.width for part in parts)
    canonical_height = max(part.height for part in parts)
    common_scale = min(
        376 / canonical_width,
        248 / canonical_height,
    )
    canonical_size = (
        round(canonical_width * common_scale),
        round(canonical_height * common_scale),
    )
    anchor = (
        (FRAME[0] - canonical_size[0]) // 2,
        FRAME[1] - canonical_size[1] - 4,
    )
    frames: list[Image.Image] = []
    for part in parts:
        # Image generation changed the outer footprint by up to seven percent
        # between door states. The factory itself is static, so every state must
        # use one canonical footprint; only the internal bay animation may move.
        fitted = part.resize(
            canonical_size,
            Image.Resampling.LANCZOS,
        )
        frame = Image.new("RGBA", FRAME)
        frame.alpha_composite(fitted, anchor)
        frames.append(frame)
    return frames


def bay_mask() -> Image.Image:
    mask = Image.new("L", FRAME)
    ImageDraw.Draw(mask).ellipse(DYNAMIC_BAY, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(2.0))


def animate_pad_leds(frame: Image.Image, phase: int) -> None:
    pixels = np.asarray(frame.convert("RGBA")).copy()
    for index, (center_x, center_y) in enumerate(LED_CENTERS):
        left = center_x - LED_RADIUS
        top = center_y - LED_RADIUS
        right = center_x + LED_RADIUS + 1
        bottom = center_y + LED_RADIUS + 1
        patch = pixels[top:bottom, left:right]
        red = patch[:, :, 0].astype(np.int16)
        green = patch[:, :, 1].astype(np.int16)
        blue = patch[:, :, 2].astype(np.int16)
        alpha = patch[:, :, 3]
        emitter = (
            (red > 105)
            & (red > green * 1.25)
            & (red > blue * 1.15)
            & (alpha > 48)
        )
        active = index == phase % len(LED_CENTERS)
        if active:
            patch[emitter, 0] = 255
            patch[emitter, 1] = 82
            patch[emitter, 2] = 26
        else:
            patch[emitter, 0] = 82
            patch[emitter, 1] = 28
            patch[emitter, 2] = 18

    frame.paste(Image.fromarray(pixels, "RGBA"))


def build_building_atlas(source: Image.Image) -> Image.Image:
    generated = normalized_building_frames(source)
    fixed_body = generated[0]
    dynamic_mask = bay_mask()
    atlas = Image.new(
        "RGBA",
        (FRAME[0], FRAME[1] * BUILDING_FRAMES),
    )
    for index, generated_frame in enumerate(generated):
        # The generator redrew every supposedly static component in each state.
        # Keep one immutable body and take only the moving bay from later states.
        frame = fixed_body.copy()
        frame.paste(generated_frame, (0, 0), dynamic_mask)
        draw_pole(frame)
        animate_pad_leds(frame, index)
        atlas.alpha_composite(frame, (0, index * FRAME[1]))
    return atlas


def build_shadow_atlas(building: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", building.size)
    for index in range(BUILDING_FRAMES):
        box = (
            0,
            index * FRAME[1],
            FRAME[0],
            (index + 1) * FRAME[1],
        )
        alpha = (
            building.crop(box)
            .getchannel("A")
            .filter(ImageFilter.GaussianBlur(2.0))
            .point(lambda value: round(value * 0.18))
        )
        shadow = Image.new("RGBA", FRAME, (7, 5, 3, 0))
        shadow.putalpha(alpha)
        shifted = Image.new("RGBA", FRAME)
        shifted.alpha_composite(shadow, (5, 5))
        atlas.alpha_composite(shifted, (0, index * FRAME[1]))
    return atlas


def draw_pole(frame: Image.Image) -> None:
    draw = ImageDraw.Draw(frame)
    pole_x = 88
    # Contact shadow and collar embed the mast in the existing roof boss.
    draw.ellipse(
        (79, 144, 103, 159),
        fill=(28, 31, 33, 255),
    )
    draw.ellipse(
        (82, 140, 100, 157),
        fill=(48, 54, 59, 255),
        outline=(151, 160, 168, 255),
        width=2,
    )
    draw.ellipse(
        (86, 144, 96, 153),
        fill=(21, 25, 29, 255),
        outline=(100, 109, 117, 255),
        width=1,
    )
    draw.rounded_rectangle(
        (pole_x, 90, pole_x + 8, 149),
        radius=3,
        fill=(23, 27, 31, 255),
        outline=(126, 135, 144, 255),
        width=1,
    )
    draw.line(
        (pole_x + 3, 94, pole_x + 3, 145),
        fill=(76, 84, 91, 255),
        width=2,
    )
    draw.ellipse(
        (pole_x - 2, 84, pole_x + 10, 96),
        fill=(137, 145, 153, 255),
        outline=(32, 36, 41, 255),
        width=2,
    )


def build_flag_atlases() -> tuple[Image.Image, Image.Image]:
    source = Image.open(FLAG_REFERENCE).convert("RGBA")
    source_mask = Image.open(FLAG_MASK_REFERENCE).convert("RGBA")
    source_frame_height = source.height // FLAG_FRAMES
    atlas = Image.new(
        "RGBA",
        (FRAME[0], FRAME[1] * FLAG_FRAMES),
    )
    mask = Image.new("RGBA", atlas.size, (255, 255, 255, 0))
    for phase in range(FLAG_FRAMES):
        source_frame = source.crop(
            (
                0,
                phase * source_frame_height,
                source.width,
                (phase + 1) * source_frame_height,
            )
        )
        source_mask_frame = source_mask.crop(
            (
                0,
                phase * source_frame_height,
                source_mask.width,
                (phase + 1) * source_frame_height,
            )
        )
        box = source_frame.getchannel("A").getbbox()
        mask_box = source_mask_frame.getchannel("A").getbbox()
        if box is None or mask_box is None:
            raise AssertionError(f"approved flag phase {phase} is empty")
        position = FLAG_POSITION
        atlas.alpha_composite(
            source_frame.crop(box),
            (position[0], position[1] + phase * FRAME[1]),
        )
        mask.alpha_composite(
            source_mask_frame.crop(mask_box),
            (position[0], position[1] + phase * FRAME[1]),
        )
    return atlas, mask


def atlas_frame(
    atlas: Image.Image,
    index: int,
    frame_count: int,
) -> Image.Image:
    height = atlas.height // frame_count
    return atlas.crop((0, index * height, atlas.width, (index + 1) * height))


def downscale_atlas_framewise(
    atlas: Image.Image,
    frame_count: int,
) -> Image.Image:
    result = Image.new("RGBA", (192, 128 * frame_count))
    for index in range(frame_count):
        frame = atlas_frame(atlas, index, frame_count)
        result.alpha_composite(
            frame.resize((192, 128), Image.Resampling.LANCZOS),
            (0, index * 128),
        )
    return result


def composed(
    building: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
    building_frame: int,
    flag_phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = atlas_frame(
        building,
        building_frame,
        BUILDING_FRAMES,
    )
    tinted = apply_engine_tint(
        atlas_frame(flag, flag_phase, FLAG_FRAMES),
        atlas_frame(mask, flag_phase, FLAG_FRAMES),
        color,
    )
    result.alpha_composite(tinted)
    return result


def checker_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    label: str,
    size: tuple[int, int] = (288, 192),
) -> None:
    draw = ImageDraw.Draw(board)
    width, height = size
    for yy in range(0, height, 24):
        for xx in range(0, width, 24):
            color = (
                (47, 50, 50, 255)
                if (xx // 24 + yy // 24) % 2 == 0
                else (35, 38, 39, 255)
            )
            draw.rectangle(
                (x + xx, y + yy, x + xx + 23, y + yy + 23),
                fill=color,
            )
    board.alpha_composite(
        sprite.resize(size, Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.rectangle(
        (x, y, x + width - 1, y + height - 1),
        outline=(154, 114, 42, 255),
        width=2,
    )
    draw.text(
        (x + 7, y + height + 6),
        label,
        font=font(17, True),
        fill=(229, 219, 198, 255),
    )


def build_review(
    building: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1920, 1260), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (30, 22),
        "Высокотехнологичный завод — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (30, 66),
        "7 кадров ангара и бегущих огней 96×64; флаг — 8 фаз и маска Дома",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    for index in range(BUILDING_FRAMES):
        row = index // 4
        column = index % 4
        checker_card(
            board,
            composed(
                building,
                flag,
                mask,
                index,
                index % FLAG_FRAMES,
                HOUSE_COLORS["Ордос"],
            ),
            30 + column * 460,
            110 + row * 270,
            f"кадр здания {index + 1}",
            (432, 288),
        )

    draw.text(
        (30, 700),
        "Восемь фаз развевающегося флага",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for phase in range(FLAG_FRAMES):
        checker_card(
            board,
            composed(
                building,
                flag,
                mask,
                0,
                phase,
                HOUSE_COLORS["Атрейдесы"],
            ),
            30 + phase * 232,
            744,
            f"фаза {phase + 1}",
            (216, 144),
        )

    draw.text(
        (30, 940),
        "Шесть цветов фракций",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, (name, color) in enumerate(HOUSE_COLORS.items()):
        checker_card(
            board,
            composed(building, flag, mask, 0, 2, color),
            30 + index * 308,
            982,
            name,
            (288, 192),
        )
    return board


def build_animation(
    building: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> None:
    # Matches cHighTech::think_animation_unitDeploy in v0.8.0:
    # idle 0, open through 5, hold, then close back to 0.
    timeline = [0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0]
    durations = [1200, 155, 155, 155, 155, 155, 605, 155, 155, 155, 155, 1400]
    frames: list[Image.Image] = []
    for preview_phase, building_frame in enumerate(timeline):
        sprite = composed(
            building,
            flag,
            mask,
            building_frame,
            preview_phase % FLAG_FRAMES,
            HOUSE_COLORS["Ордос"],
        )
        canvas = Image.new("RGBA", (768, 512), (18, 21, 24, 255))
        canvas.alpha_composite(
            sprite.resize((720, 480), Image.Resampling.LANCZOS),
            (24, 16),
        )
        frames.append(
            canvas.convert("P", palette=Image.Palette.ADAPTIVE),
        )
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def validate(
    building: Image.Image,
    shadow: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    expected = {
        "building": (FRAME[0], FRAME[1] * BUILDING_FRAMES),
        "shadow": (FRAME[0], FRAME[1] * BUILDING_FRAMES),
        "flag": (FRAME[0], FRAME[1] * FLAG_FRAMES),
        "mask": (FRAME[0], FRAME[1] * FLAG_FRAMES),
    }
    images = {
        "building": building,
        "shadow": shadow,
        "flag": flag,
        "mask": mask,
    }
    failures: list[str] = []
    bounds: dict[str, list[list[int]]] = {}
    for name, image in images.items():
        if image.size != expected[name]:
            failures.append(f"{name} size {image.size} != {expected[name]}")
        count = BUILDING_FRAMES if name in ("building", "shadow") else FLAG_FRAMES
        records: list[list[int]] = []
        for index in range(count):
            box = atlas_frame(image, index, count).getchannel("A").getbbox()
            if box is None:
                failures.append(f"{name} frame {index} is empty")
                continue
            records.append(list(box))
            if box[0] < 0 or box[1] < 0 or box[2] > FRAME[0] or box[3] > FRAME[1]:
                failures.append(f"{name} frame {index} overflows")
        bounds[name] = records

    building_bounds = bounds.get("building", [])
    alignment: dict[str, object] = {}
    if len(building_bounds) == BUILDING_FRAMES:
        edge_values = {
            "left": [box[0] for box in building_bounds],
            "top": [box[1] for box in building_bounds],
            "right": [box[2] for box in building_bounds],
            "bottom": [box[3] for box in building_bounds],
            "width": [box[2] - box[0] for box in building_bounds],
            "height": [box[3] - box[1] for box in building_bounds],
        }
        drift = {
            name: max(values) - min(values)
            for name, values in edge_values.items()
        }
        alignment = {
            "edges": edge_values,
            "drift": drift,
            "maximum_allowed_drift": 1,
        }
        for name, value in drift.items():
            if value > 1:
                failures.append(
                    f"building {name} drifts by {value}px; maximum is 1px"
                )

    return {
        "format": 1,
        "status": "approval_preview" if not failures else "failed",
        "resource_id": 8,
        "resource": "BUILD_HIGHTECH",
        "shadow_id": 9,
        "shadow": "BUILD_HIGHTECH_SHADOW",
        "building_frames": BUILDING_FRAMES,
        "flag_frames": FLAG_FRAMES,
        "logical_frame": list(LOGICAL_FRAME),
        "hd2_frame": [192, 128],
        "hd4_frame": list(FRAME),
        "flag": "BUILD_HIGHTECH_FLAG",
        "mask": "HM_BUILD_HIGHTECH_FLAG",
        "house_colors": list(HOUSE_COLORS),
        "anchor": "fixed bottom-center footprint for all seven frames",
        "animation": {
            "static_body": "identical in all seven frames",
            "moving_region": "central bay only",
            "pad_leds": "clockwise sequence over four emitters",
            "runtime_trigger": "air unit production completed",
            "runtime_frames": [0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0],
            "idle_frame": 0,
            "unused_by_v0.8.0": [6],
            "preview_note": "looped demonstration with long idle pauses",
            "flag_motion": "exact approved eight-phase building flag animation",
            "flag_mount": "roof boss near HD4 coordinate (92, 150)",
        },
        "bounds": bounds,
        "building_alignment": alignment,
        "failures": failures,
        "installed": False,
    }


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    building = build_building_atlas(source)
    shadow = build_shadow_atlas(building)
    flag, mask = build_flag_atlases()
    manifest = validate(building, shadow, flag, mask)
    if manifest["failures"]:
        raise AssertionError("\n".join(manifest["failures"]))

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    flag.save(FLAG_OUT, optimize=True)
    mask.save(FLAG_MASK_OUT, optimize=True)
    downscale_atlas_framewise(building, BUILDING_FRAMES).save(
        OUTPUT / "BUILD_HIGHTECH_HD2_PREVIEW.png",
        optimize=True,
    )
    downscale_atlas_framewise(shadow, BUILDING_FRAMES).save(
        OUTPUT / "BUILD_HIGHTECH_SHADOW_HD2_PREVIEW.png",
        optimize=True,
    )
    downscale_atlas_framewise(flag, FLAG_FRAMES).save(
        OUTPUT / "BUILD_HIGHTECH_FLAG_HD2_PREVIEW.png",
        optimize=True,
    )
    downscale_atlas_framewise(mask, FLAG_FRAMES).save(
        OUTPUT / "HM_BUILD_HIGHTECH_FLAG_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(building, flag, mask).save(REVIEW_OUT, optimize=True)
    build_animation(building, flag, mask)
    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
