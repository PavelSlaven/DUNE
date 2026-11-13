#!/usr/bin/env python3
"""Build an approval-ready 11-frame HD heavy-factory animation.

The two ImageGen masters intentionally contain the same factory in idle and
completed states.  Intermediate frames are composed deterministically so that
the stationary building cannot jitter between animation phases.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


FRAME_COUNT = 11
HD4_SIZE = (384, 256)
HD2_SIZE = (192, 128)


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def extract_vehicle_mask(idle: Image.Image, complete: Image.Image) -> Image.Image:
    """Isolate the assembled vehicle from the generated completed frame."""
    if idle.size != complete.size:
        raise ValueError(f"master sizes differ: {idle.size} and {complete.size}")
    width, height = idle.size

    # A hand-traced silhouette is deliberate here.  ImageGen makes tiny
    # material changes to the empty floor between the two masters, so a plain
    # RGB-difference mask would incorrectly replace a rectangular floor patch
    # together with the vehicle.
    points_normalized = (
        (0.739, 0.346),
        (0.767, 0.346),
        (0.775, 0.378),
        (0.779, 0.414),
        (0.775, 0.447),
        (0.783, 0.468),
        (0.780, 0.516),
        (0.772, 0.544),
        (0.768, 0.575),
        (0.760, 0.592),
        (0.739, 0.592),
        (0.731, 0.575),
        (0.727, 0.545),
        (0.719, 0.521),
        (0.717, 0.471),
        (0.724, 0.444),
        (0.722, 0.407),
        (0.731, 0.376),
    )
    points = [(round(x * width), round(y * height)) for x, y in points_normalized]
    mask = Image.new("L", idle.size, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(1.4))


def smooth_reveal(mask: Image.Image, phase: int) -> Image.Image:
    """Reveal the chassis from bottom to top across phases 1..10."""
    if phase <= 0:
        return Image.new("L", mask.size, 0)
    if phase >= 10:
        return mask.copy()

    alpha = np.asarray(mask, dtype=np.float32) / 255.0
    ys, _ = np.nonzero(alpha > 0.08)
    if len(ys) == 0:
        return Image.new("L", mask.size, 0)
    top, bottom = int(ys.min()), int(ys.max())
    progress = phase / 10.0
    edge = bottom - progress * (bottom - top + 1)
    yy = np.arange(mask.height, dtype=np.float32)[:, None]
    ramp = np.clip((yy - edge + 12.0) / 24.0, 0.0, 1.0)
    revealed = np.clip(alpha * ramp, 0.0, 1.0)
    return Image.fromarray(np.uint8(revealed * 255.0), mode="L")


def add_production_effects(
    frame: Image.Image,
    vehicle_mask: Image.Image,
    phase: int,
) -> Image.Image:
    if phase <= 0 or phase >= 10:
        return frame

    mask_np = np.asarray(vehicle_mask)
    ys, xs = np.nonzero(mask_np > 64)
    if len(xs) == 0:
        return frame

    progress = phase / 10.0
    top, bottom = int(ys.min()), int(ys.max())
    left, right = int(xs.min()), int(xs.max())
    edge_y = round(bottom - progress * (bottom - top))

    glow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    soft = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    soft_draw = ImageDraw.Draw(soft)

    # Alternating weld heads follow the assembly front without changing the
    # factory silhouette.  At HD4 they remain visible but not oversized.
    weld_xs = (
        round(left + (right - left) * 0.25),
        round(left + (right - left) * 0.75),
    )
    for index, x in enumerate(weld_xs):
        if (phase + index) % 2 == 0:
            soft_draw.ellipse(
                (x - 18, edge_y - 18, x + 18, edge_y + 18),
                fill=(255, 132, 22, 90),
            )
            draw.ellipse(
                (x - 4, edge_y - 4, x + 4, edge_y + 4),
                fill=(255, 245, 185, 245),
            )

    soft = soft.filter(ImageFilter.GaussianBlur(10))
    frame = Image.alpha_composite(frame, soft)
    return Image.alpha_composite(frame, glow)


def make_source_frames(
    idle: Image.Image,
    complete: Image.Image,
    vehicle_mask: Image.Image,
) -> list[Image.Image]:
    if idle.size != complete.size:
        raise ValueError(f"master sizes differ: {idle.size} and {complete.size}")

    frames: list[Image.Image] = []
    for phase in range(FRAME_COUNT):
        frame = idle.copy()
        reveal = smooth_reveal(vehicle_mask, phase)
        frame.paste(complete, (0, 0), reveal)
        frame = add_production_effects(frame, vehicle_mask, phase)
        frames.append(frame)
    return frames


def fit_frame(source: Image.Image, bounds: tuple[int, int, int, int]) -> Image.Image:
    left, top, right, bottom = bounds
    subject = source.crop(bounds)
    max_width, max_height = 368, 244
    scale = min(max_width / subject.width, max_height / subject.height)
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", HD4_SIZE, (0, 0, 0, 0))
    x = (HD4_SIZE[0] - size[0]) // 2
    y = HD4_SIZE[1] - size[1] - 6
    frame.alpha_composite(subject, (x, y))
    return frame


def common_bounds(frames: list[Image.Image]) -> tuple[int, int, int, int]:
    union = Image.new("L", frames[0].size, 0)
    for frame in frames:
        union = Image.fromarray(
            np.maximum(np.asarray(union), np.asarray(frame.getchannel("A"))),
            mode="L",
        )
    bbox = union.getbbox()
    if bbox is None:
        raise RuntimeError("empty heavy-factory masters")
    return bbox


def stack_vertical(frames: list[Image.Image], frame_size: tuple[int, int]) -> Image.Image:
    atlas = Image.new(
        "RGBA",
        (frame_size[0], frame_size[1] * len(frames)),
        (0, 0, 0, 0),
    )
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (0, index * frame_size[1]))
    return atlas


def make_shadow(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A")
    blurred = alpha.filter(ImageFilter.GaussianBlur(3.0))
    shadow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    silhouette = Image.new("RGBA", frame.size, (8, 7, 6, 105))
    shifted = Image.new("L", frame.size, 0)
    shifted.paste(blurred, (4, 5))
    silhouette.putalpha(shifted.point(lambda value: value * 82 // 255))
    shadow.alpha_composite(silhouette)
    return shadow


def make_flash(frame: Image.Image) -> Image.Image:
    """Production flash overlay drawn by cHeavyFactory during deployment."""
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    glow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    sharp_draw = ImageDraw.Draw(result)

    # Red reactor/status window on the left factory block.
    center = (159, 151)
    glow_draw.ellipse(
        (center[0] - 25, center[1] - 19, center[0] + 25, center[1] + 19),
        fill=(255, 38, 18, 125),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    result = Image.alpha_composite(result, glow)
    sharp_draw = ImageDraw.Draw(result)
    sharp_draw.ellipse(
        (center[0] - 5, center[1] - 4, center[0] + 5, center[1] + 4),
        fill=(255, 190, 80, 215),
    )
    return result


def make_contact_sheet(frames: list[Image.Image]) -> Image.Image:
    columns, rows = 4, 3
    sheet = Image.new(
        "RGBA",
        (HD4_SIZE[0] * columns, HD4_SIZE[1] * rows),
        (19, 21, 23, 255),
    )
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        x = (index % columns) * HD4_SIZE[0]
        y = (index // columns) * HD4_SIZE[1]
        sheet.alpha_composite(frame, (x, y))
        draw.rounded_rectangle(
            (x + 7, y + 7, x + 38, y + 32),
            radius=5,
            fill=(0, 0, 0, 190),
        )
        draw.text((x + 17, y + 11), str(index), fill=(255, 216, 83, 255))
    return sheet


def save_gif(frames: list[Image.Image], path: Path) -> None:
    backdrop = Image.new("RGB", HD4_SIZE, (54, 50, 42))
    gif_frames = []
    for frame in frames:
        composite = backdrop.copy()
        composite.paste(frame.convert("RGB"), (0, 0), frame.getchannel("A"))
        gif_frames.append(composite)
    gif_frames[0].save(
        path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=110,
        loop=0,
        disposal=2,
    )


def validate(frames: list[Image.Image], animation_bounds: tuple[int, int, int, int]) -> dict:
    if len(frames) != FRAME_COUNT:
        raise AssertionError(f"expected {FRAME_COUNT} frames, got {len(frames)}")
    if any(frame.size != HD4_SIZE for frame in frames):
        raise AssertionError("one or more HD4 frames have an invalid size")

    x0, y0, x1, y1 = animation_bounds
    static_mask = np.ones((HD4_SIZE[1], HD4_SIZE[0]), dtype=bool)
    static_mask[y0:y1, x0:x1] = False
    baseline = np.asarray(frames[0], dtype=np.int16)
    maximum_static_delta = 0
    for frame in frames[1:]:
        delta = np.max(np.abs(np.asarray(frame, dtype=np.int16) - baseline), axis=2)
        maximum_static_delta = max(
            maximum_static_delta,
            int(delta[static_mask].max(initial=0)),
        )
    if maximum_static_delta != 0:
        raise AssertionError(
            f"stationary factory pixels changed outside animation bounds: "
            f"{maximum_static_delta}"
        )

    return {
        "frame_count": len(frames),
        "logical_frame": [96, 64],
        "hd4_frame": list(HD4_SIZE),
        "hd4_atlas": [HD4_SIZE[0], HD4_SIZE[1] * FRAME_COUNT],
        "hd2_frame": list(HD2_SIZE),
        "hd2_atlas": [HD2_SIZE[0], HD2_SIZE[1] * FRAME_COUNT],
        "stationary_max_delta": maximum_static_delta,
        "animation_bounds_hd4": list(animation_bounds),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idle", type=Path, required=True)
    parser.add_argument("--complete", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    idle = load_rgba(args.idle)
    complete = load_rgba(args.complete)
    vehicle_mask = extract_vehicle_mask(idle, complete)
    source_frames = make_source_frames(idle, complete, vehicle_mask)
    bounds = common_bounds(source_frames)
    frames4 = [fit_frame(frame, bounds) for frame in source_frames]
    frames2 = [
        frame.resize(HD2_SIZE, Image.Resampling.LANCZOS) for frame in frames4
    ]

    # Only this rectangle may change across production frames.  It includes
    # the cradle, the two weld heads, and their short-lived glow.
    animation_bounds = (252, 73, 329, 190)
    report = validate(frames4, animation_bounds)

    atlas4 = stack_vertical(frames4, HD4_SIZE)
    atlas2 = stack_vertical(frames2, HD2_SIZE)
    shadows4 = [make_shadow(frame) for frame in frames4]
    shadows2 = [
        frame.resize(HD2_SIZE, Image.Resampling.LANCZOS) for frame in shadows4
    ]

    atlas4.save(args.out / "BUILD_HEAVYFACTORY_HD4_PREVIEW.png")
    atlas2.save(args.out / "BUILD_HEAVYFACTORY_HD2_PREVIEW.png")
    stack_vertical(shadows4, HD4_SIZE).save(
        args.out / "BUILD_HEAVYFACTORY_SHADOW_HD4_PREVIEW.png"
    )
    stack_vertical(shadows2, HD2_SIZE).save(
        args.out / "BUILD_HEAVYFACTORY_SHADOW_HD2_PREVIEW.png"
    )
    make_flash(frames4[0]).save(
        args.out / "BUILD_HEAVYFACTORY_FLASH_HD4_PREVIEW.png"
    )
    make_flash(frames4[0]).resize(HD2_SIZE, Image.Resampling.LANCZOS).save(
        args.out / "BUILD_HEAVYFACTORY_FLASH_HD2_PREVIEW.png"
    )
    make_contact_sheet(frames4).save(args.out / "heavyfactory_11frames_review.png")
    save_gif(frames4, args.out / "heavyfactory_production_animation.gif")
    vehicle_mask.save(args.out / "debug_vehicle_mask.png")
    (args.out / "validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
