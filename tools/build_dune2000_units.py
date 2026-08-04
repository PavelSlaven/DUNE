#!/usr/bin/env python3
"""Import the complete Dune 2000 vehicle set into D2TM HD4 atlases.

The source sheets remain the artwork. Processing is limited to background
removal, direction selection, frame placement, house-colour masks and
deterministic shadows. HD2 is produced later from these HD4 masters.
"""

from __future__ import annotations

import math
from collections import deque
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "source_references" / "ru4"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)


def classic(index: int) -> Path:
    return next(CLASSIC.glob(f"{index:04d}_*.png"))


def master(index: int) -> Path:
    return MASTER / classic(index).name


def source(name: str) -> Image.Image:
    return Image.open(SOURCE / f"dune2000_{name}.png").convert("RGB")


def bands(values: list[bool]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(values + [False]):
        if value and start is None:
            start = index
        elif not value and start is not None:
            result.append((start, index))
            start = None
    return result


def non_black_row_bands(image: Image.Image) -> list[tuple[int, int]]:
    pixels = image.load()
    return bands(
        [
            any(pixels[x, y] != BLACK for x in range(image.width))
            for y in range(image.height)
        ]
    )


def non_black_column_bands(
    image: Image.Image,
    top: int,
    bottom: int,
) -> list[tuple[int, int]]:
    pixels = image.load()
    return bands(
        [
            any(pixels[x, y] != BLACK for y in range(top, bottom))
            for x in range(image.width)
        ]
    )


def clear_border_black(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    queue: deque[tuple[int, int]] = deque()
    visited: set[tuple[int, int]] = set()

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        r, g, b, a = pixels[x, y]
        if a == 0 or (r, g, b) != BLACK:
            continue
        pixels[x, y] = (0, 0, 0, 0)
        for nx, ny in (
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ):
            if 0 <= nx < width and 0 <= ny < height:
                queue.append((nx, ny))
    return rgba


def clean_cell(cell: Image.Image, black_key: bool = False) -> Image.Image:
    rgba = cell.convert("RGBA")
    cleaned = []
    for r, g, b, _a in rgba.getdata():
        magenta = r >= 248 and b >= 248 and g <= 8
        transparent_black = black_key and (r, g, b) == BLACK
        alpha = 0 if magenta or transparent_black else 255
        cleaned.append((r, g, b, alpha))
    rgba.putdata(cleaned)
    if not black_key:
        rgba = clear_border_black(rgba)
    box = rgba.getchannel("A").getbbox()
    return rgba.crop(box) if box else Image.new("RGBA", (1, 1))


def extract_rows(
    image: Image.Image,
    row_indices: list[int],
    black_key: bool = False,
) -> list[Image.Image]:
    row_ranges = non_black_row_bands(image)
    result: list[Image.Image] = []
    for row_index in row_indices:
        top, bottom = row_ranges[row_index]
        for left, right in non_black_column_bands(image, top, bottom):
            result.append(
                clean_cell(
                    image.crop((left, top, right, bottom)),
                    black_key,
                )
            )
    return result


def first_32_directions(name: str) -> list[Image.Image]:
    image = source(name)
    rows = non_black_row_bands(image)
    frames = extract_rows(image, list(range(4)))
    if len(rows) < 4 or len(frames) != 32:
        raise ValueError(f"{name}: expected 32 body directions")
    return frames


def eight_directions(frames: list[Image.Image]) -> list[Image.Image]:
    count = len(frames)
    if count < 8:
        raise ValueError(f"direction set has only {count} frames")
    # The Dune 2000 sheets turn clockwise from north. D2TM's draw index
    # traverses the atlas in the opposite direction and starts at east:
    # E, NE, N, NW, W, SW, S, SE.
    indices = [
        int(math.floor(count / 4 - index * count / 8 + 0.5)) % count
        for index in range(8)
    ]
    return [frames[index] for index in indices]


def opaque_median(image: Image.Image) -> tuple[int, int]:
    alpha = image.getchannel("A")
    xs: list[int] = []
    ys: list[int] = []
    for y in range(image.height):
        for x in range(image.width):
            if alpha.getpixel((x, y)) > 32:
                xs.append(x)
                ys.append(y)
    if not xs:
        return image.width // 2, image.height // 2
    xs.sort()
    ys.sort()
    return xs[len(xs) // 2], ys[len(ys) // 2]


def place_subject(
    subject: Image.Image,
    frame_size: tuple[int, int],
    content_size: tuple[int, int] | None = None,
) -> Image.Image:
    subject = subject.convert("RGBA")
    max_width, max_height = content_size or (
        frame_size[0] - 2,
        frame_size[1] - 2,
    )
    scale = min(
        1.0,
        max_width / subject.width,
        max_height / subject.height,
    )
    if scale < 1.0:
        subject = subject.resize(
            (
                max(1, round(subject.width * scale)),
                max(1, round(subject.height * scale)),
            ),
            Image.Resampling.LANCZOS,
        )
    # Lanczos can retain fully keyed magenta RGB in almost-transparent edge
    # pixels. Drop that invisible colour fringe before the 4x nearest upscale.
    sanitized = []
    for r, g, b, a in subject.getdata():
        keyed_fringe = r >= 248 and b >= 248 and g <= 8 and a <= 32
        sanitized.append((0, 0, 0, 0) if keyed_fringe else (r, g, b, a))
    subject.putdata(sanitized)

    anchor_x, anchor_y = opaque_median(subject)
    target_x = frame_size[0] // 2
    target_y = frame_size[1] // 2
    x = target_x - anchor_x
    y = target_y - anchor_y
    x = min(max(x, 0), frame_size[0] - subject.width)
    y = min(max(y, 0), frame_size[1] - subject.height)

    frame = Image.new("RGBA", frame_size)
    frame.alpha_composite(subject, (x, y))
    return frame


def resize_premultiplied(
    image: Image.Image,
    size: tuple[int, int],
    resample: Image.Resampling = Image.Resampling.LANCZOS,
) -> Image.Image:
    """Resize RGBA without dark or keyed-colour fringes around the alpha edge."""
    rgba = image.convert("RGBA")
    premultiplied = Image.new("RGBA", rgba.size)
    pixels = []
    for r, g, b, a in rgba.getdata():
        pixels.append(
            (
                round(r * a / 255),
                round(g * a / 255),
                round(b * a / 255),
                a,
            )
        )
    premultiplied.putdata(pixels)
    resized = premultiplied.resize(size, resample)
    restored = []
    for r, g, b, a in resized.getdata():
        if a <= 1:
            restored.append((0, 0, 0, 0))
        else:
            restored.append(
                (
                    min(255, round(r * 255 / a)),
                    min(255, round(g * 255 / a)),
                    min(255, round(b * 255 / a)),
                    a,
                )
            )
    resized.putdata(restored)
    return resized


def remaster_subject(
    subject: Image.Image,
    target_size: tuple[int, int],
) -> Image.Image:
    """Create a density-first HD sprite while preserving pose and silhouette.

    The source sheets are small, so a plain Lanczos resize only produces a
    smooth low-resolution sprite. An edge-aware material pass restores panel
    boundaries, local contrast and small highlights at HD4 without changing
    the direction or outline of a frame.
    """
    resized = resize_premultiplied(subject, target_size)
    alpha = resized.getchannel("A")
    rgba = np.asarray(resized.convert("RGBA"), dtype=np.uint8)
    rgb = rgba[..., :3]
    bilateral = cv2.bilateralFilter(rgb, 7, 22, 3)
    broad = cv2.GaussianBlur(bilateral, (0, 0), 1.15)
    detailed = cv2.addWeighted(
        bilateral.astype(np.float32),
        1.58,
        broad.astype(np.float32),
        -0.58,
        0.0,
    )

    luminance = cv2.cvtColor(
        np.clip(detailed, 0, 255).astype(np.uint8),
        cv2.COLOR_RGB2GRAY,
    )
    gx = cv2.Sobel(luminance, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(luminance, cv2.CV_32F, 0, 1, ksize=3)
    bevel = np.clip((-gx - gy) * 0.075, -7.0, 7.0)[..., None]
    detailed = np.clip(detailed + bevel, 0, 255).astype(np.uint8)
    detailed[rgba[..., 3] == 0] = 0

    restored = Image.fromarray(
        np.dstack((detailed, rgba[..., 3])),
        "RGBA",
    ).filter(
        ImageFilter.UnsharpMask(radius=0.65, percent=115, threshold=2)
    )
    restored.putalpha(alpha)
    sanitized = []
    for r, g, b, a in restored.getdata():
        keyed_fringe = r >= 245 and b >= 245 and g <= 16 and a <= 96
        sanitized.append(
            (0, 0, 0, 0) if a == 0 or keyed_fringe else (r, g, b, a)
        )
    restored.putdata(sanitized)
    return restored


def place_subject_hd4(
    subject: Image.Image,
    frame_size: tuple[int, int],
    content_size: tuple[int, int] | None = None,
) -> Image.Image:
    """Place source art directly on a 4x frame without a logical-size roundtrip."""
    subject = subject.convert("RGBA")
    max_width, max_height = content_size or (
        frame_size[0] - 2,
        frame_size[1] - 2,
    )
    logical_scale = min(
        1.0,
        max_width / subject.width,
        max_height / subject.height,
    )
    target_size = (
        max(1, round(subject.width * logical_scale * 4)),
        max(1, round(subject.height * logical_scale * 4)),
    )
    subject = remaster_subject(subject, target_size)
    frame_size_hd4 = (frame_size[0] * 4, frame_size[1] * 4)
    anchor_x, anchor_y = opaque_median(subject)
    x = frame_size_hd4[0] // 2 - anchor_x
    y = frame_size_hd4[1] // 2 - anchor_y
    x = min(max(x, 0), frame_size_hd4[0] - subject.width)
    y = min(max(y, 0), frame_size_hd4[1] - subject.height)
    frame = Image.new("RGBA", frame_size_hd4)
    frame.alpha_composite(subject, (x, y))
    return frame


def build_hd4_atlas(
    rows: list[list[Image.Image]],
    frame_size: tuple[int, int],
    content_size: tuple[int, int] | None = None,
) -> Image.Image:
    if not rows or any(len(row) != 8 for row in rows):
        raise ValueError("D2TM directional rows must contain eight frames")
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    atlas = Image.new(
        "RGBA",
        (frame_width * 8, frame_height * len(rows)),
    )
    for row_index, row in enumerate(rows):
        for column, subject in enumerate(row):
            frame = place_subject_hd4(subject, frame_size, content_size)
            atlas.alpha_composite(
                frame,
                (column * frame_width, row_index * frame_height),
            )
    return atlas


def save_master4(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def build_logical_atlas(
    rows: list[list[Image.Image]],
    frame_size: tuple[int, int],
    content_size: tuple[int, int] | None = None,
) -> Image.Image:
    if not rows or any(len(row) != 8 for row in rows):
        raise ValueError("D2TM directional rows must contain eight frames")
    atlas = Image.new(
        "RGBA",
        (frame_size[0] * 8, frame_size[1] * len(rows)),
    )
    for row_index, row in enumerate(rows):
        for column, subject in enumerate(row):
            frame = place_subject(subject, frame_size, content_size)
            atlas.alpha_composite(
                frame,
                (column * frame_size[0], row_index * frame_size[1]),
            )
    return atlas


def save_hd4(image: Image.Image, path: Path) -> None:
    save_master4(
        remaster_subject(
            image,
            (image.width * 4, image.height * 4),
        ),
        path,
    )


def is_house_coloured_pixel(
    red: int,
    green: int,
    blue: int,
    alpha: int,
) -> bool:
    maximum = max(red, green, blue)
    minimum = min(red, green, blue)
    saturation = maximum - minimum
    blue_or_cyan = (
        saturation >= 28
        and blue >= 60
        and blue >= red * 1.08
        and green >= red * 0.82
    )
    purple = (
        saturation >= 34
        and red >= 55
        and blue >= 55
        and green * 1.18 < max(red, blue)
    )
    return bool(alpha and (blue_or_cyan or purple))


def neutralize_house_colours(image: Image.Image) -> Image.Image:
    pixels = []
    for red, green, blue, alpha in image.convert("RGBA").getdata():
        if is_house_coloured_pixel(red, green, blue, alpha):
            luminance = 0.299 * red + 0.587 * green + 0.114 * blue
            value = max(34, min(186, round(28 + luminance * 0.76)))
            pixels.append(
                (
                    round(value * 0.92),
                    round(value * 0.96),
                    value,
                    alpha,
                )
            )
        else:
            pixels.append((red, green, blue, alpha))
    result = Image.new("RGBA", image.size)
    result.putdata(pixels)
    return result


def house_mask(
    image: Image.Image,
    frame_size: tuple[int, int],
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    output = np.zeros(rgba.shape[:2], dtype=np.uint8)
    for top in range(0, image.height, frame_height):
        for left in range(0, image.width, frame_width):
            frame = rgba[
                top : top + frame_height,
                left : left + frame_width,
            ]
            red = frame[..., 0].astype(np.float32)
            green = frame[..., 1].astype(np.float32)
            blue = frame[..., 2].astype(np.float32)
            alpha = frame[..., 3]
            maximum = np.maximum(np.maximum(red, green), blue)
            minimum = np.minimum(np.minimum(red, green), blue)
            saturation = maximum - minimum
            candidate = (
                (alpha > 0)
                & (
                    (
                        (saturation >= 28)
                        & (blue >= 60)
                        & (blue >= red * 1.08)
                        & (green >= red * 0.82)
                    )
                    | (
                        (saturation >= 34)
                        & (red >= 55)
                        & (blue >= 55)
                        & (green * 1.18 < np.maximum(red, blue))
                    )
                )
            )
            opaque_count = int(np.count_nonzero(alpha > 24))
            maximum_coloured = max(1, round(opaque_count * 0.14))
            candidate_count = int(np.count_nonzero(candidate))
            if candidate_count > maximum_coloured:
                score = saturation + maximum * 0.12
                score = cv2.GaussianBlur(score, (0, 0), 1.3)
                threshold = np.partition(
                    score[candidate],
                    candidate_count - maximum_coloured,
                )[candidate_count - maximum_coloured]
                candidate &= score >= threshold
            selected = np.where(candidate, 96, 0).astype(np.uint8)
            selected = cv2.GaussianBlur(selected, (0, 0), 0.65)
            output[
                top : top + frame_height,
                left : left + frame_width,
            ] = np.minimum(selected, 96)

    pixels = [
        (255, 255, 255, int(strength))
        for strength in output.flat
    ]
    mask = Image.new("RGBA", image.size)
    mask.putdata(pixels)
    return mask


def save_house_mask(
    image: Image.Image,
    resource_name: str,
    frame_size: tuple[int, int],
) -> None:
    save_master4(
        house_mask(image, frame_size),
        EXTRA / f"HOUSEMASK_{resource_name}.png",
    )


def logical_shadow(
    image: Image.Image,
    source_frame: tuple[int, int],
    target_frame: tuple[int, int],
    rows: int,
    opacity: float,
    offset: tuple[int, int],
) -> Image.Image:
    density = 4
    source_frame_hd = (
        source_frame[0] * density,
        source_frame[1] * density,
    )
    target_frame_hd = (
        target_frame[0] * density,
        target_frame[1] * density,
    )
    result = Image.new(
        "RGBA",
        (target_frame_hd[0] * 8, target_frame_hd[1] * rows),
    )
    for row in range(rows):
        for column in range(8):
            source_box = (
                column * source_frame_hd[0],
                row * source_frame_hd[1],
                (column + 1) * source_frame_hd[0],
                (row + 1) * source_frame_hd[1],
            )
            alpha = image.crop(source_box).getchannel("A")
            alpha = alpha.filter(ImageFilter.GaussianBlur(1.8))
            alpha = alpha.point(lambda value: round(value * opacity))
            silhouette = Image.new("RGBA", source_frame_hd, (7, 5, 3, 0))
            silhouette.putalpha(alpha)
            x = (
                column * target_frame_hd[0]
                + (target_frame_hd[0] - source_frame_hd[0]) // 2
                + offset[0] * density
            )
            y = (
                row * target_frame_hd[1]
                + (target_frame_hd[1] - source_frame_hd[1]) // 2
                + offset[1] * density
            )
            result.alpha_composite(silhouette, (x, y))
    return result


def save_vehicle(
    resource_id: int,
    shadow_id: int | None,
    rows: list[list[Image.Image]],
    frame_size: tuple[int, int],
    resource_name: str,
    content_size: tuple[int, int] | None = None,
    shadow_frame: tuple[int, int] | None = None,
    air_shadow: bool = False,
) -> Image.Image:
    coloured_hd4 = build_hd4_atlas(rows, frame_size, content_size)
    hd4 = neutralize_house_colours(coloured_hd4)
    save_master4(hd4, master(resource_id))
    save_house_mask(coloured_hd4, resource_name, frame_size)
    if shadow_id is not None:
        target = shadow_frame or frame_size
        shadow = logical_shadow(
            hd4,
            frame_size,
            target,
            len(rows),
            0.30 if air_shadow else 0.18,
            (5, 5) if air_shadow else (2, 2),
        )
        save_master4(shadow, master(shadow_id))
    return hd4


def build_standard_vehicles() -> None:
    carryall = eight_directions(first_32_directions("carryall"))
    save_vehicle(
        130,
        131,
        [carryall, carryall],
        (48, 48),
        "UNIT_CARRYALL",
        shadow_frame=(50, 56),
        air_shadow=True,
    )

    devastator = eight_directions(first_32_directions("devastator"))
    save_vehicle(
        132,
        133,
        [devastator],
        (38, 48),
        "UNIT_DEVASTATOR",
        content_size=(36, 44),
    )

    deviator = eight_directions(first_32_directions("deviator"))
    save_vehicle(
        134,
        None,
        [deviator],
        (32, 32),
        "UNIT_DEVIATOR",
    )

    harvester = eight_directions(first_32_directions("harvester"))
    save_vehicle(
        137,
        138,
        [harvester, harvester, harvester, harvester],
        (80, 52),
        "UNIT_HARVESTER",
    )

    launcher = eight_directions(first_32_directions("missile_tank"))
    save_vehicle(
        139,
        140,
        [launcher],
        (32, 32),
        "UNIT_LAUNCHER",
    )

    mcv = eight_directions(first_32_directions("mcv"))
    save_vehicle(
        141,
        142,
        [mcv],
        (48, 50),
        "UNIT_MCV",
    )

    quad = eight_directions(first_32_directions("quad"))
    save_vehicle(145, 146, [quad], (32, 32), "UNIT_QUAD")

    raider = eight_directions(first_32_directions("raider_trike"))
    save_vehicle(147, 148, [raider], (28, 26), "UNIT_RAIDER")

    sonic_frames = extract_rows(source("sonic_tank"), [0, 1, 2])
    if len(sonic_frames) != 30:
        raise ValueError("sonic_tank: expected 30 directions")
    sonic = eight_directions(sonic_frames)
    save_vehicle(157, 158, [sonic], (32, 32), "UNIT_SONICTANK")

    trike = eight_directions(first_32_directions("trike"))
    save_vehicle(162, 163, [trike], (28, 26), "UNIT_TRIKE")


def build_ornithopter() -> None:
    image = source("ornithopter")
    animations = []
    for first_row in (0, 2, 4):
        frames = extract_rows(image, [first_row, first_row + 1])
        if len(frames) != 32:
            raise ValueError(
                f"ornithopter rows {first_row}-{first_row + 1}: "
                f"expected 32 directions, got {len(frames)}"
            )
        animations.append(eight_directions(frames))
    save_vehicle(
        143,
        144,
        [animations[0], animations[1], animations[2], animations[1]],
        (48, 48),
        "UNIT_ORNITHOPTER",
        air_shadow=True,
    )


def build_combat_tanks() -> None:
    variants: dict[str, tuple[Image.Image, Image.Image]] = {}
    for house, filename in (
        ("ATREIDES", "tank_atreides"),
        ("HARKONNEN", "tank_harkonnen"),
        ("ORDOS", "tank_ordos"),
    ):
        image = source(filename)
        body_frames = extract_rows(image, [0, 1, 2, 3])
        top_frames = extract_rows(image, [4, 5, 6])
        if len(body_frames) != 32 or len(top_frames) != 32:
            raise ValueError(
                f"{filename}: expected 32 body and 32 turret directions"
            )
        body = build_hd4_atlas(
            [eight_directions(body_frames)],
            (32, 32),
        )
        top = build_hd4_atlas(
            [eight_directions(top_frames)],
            (32, 32),
        )
        variants[house] = (body, top)
        save_master4(
            body,
            EXTRA / f"HOUSEVARIANT_{house}_UNIT_TANKBASE.png",
        )
        save_master4(
            top,
            EXTRA / f"HOUSEVARIANT_{house}_UNIT_TANKTOP.png",
        )

    default_body, default_top = variants["ATREIDES"]
    save_master4(default_body, master(159))
    save_master4(default_top, master(161))
    shadow = logical_shadow(
        default_body,
        (32, 32),
        (32, 32),
        1,
        0.18,
        (2, 2),
    )
    save_master4(shadow, master(160))


def build_siege_tank() -> None:
    image = source("siege_tank")
    body_frames = extract_rows(image, [0, 1, 2, 3])
    top_frames = extract_rows(image, [4, 5, 6, 7])
    if len(body_frames) != 32 or len(top_frames) != 32:
        raise ValueError("siege_tank: expected 32 body and 32 turret directions")
    body = save_vehicle(
        151,
        152,
        [eight_directions(body_frames)],
        (36, 38),
        "UNIT_SIEGEBASE",
        content_size=(34, 34),
    )
    coloured_top = build_hd4_atlas(
        [eight_directions(top_frames)],
        (36, 38),
        (34, 34),
    )
    top = neutralize_house_colours(coloured_top)
    save_master4(top, master(153))
    save_house_mask(coloured_top, "UNIT_SIEGETOP", (36, 38))


def build_sandworm() -> None:
    frames = extract_rows(source("sandworm"), [0], black_key=True)
    if len(frames) != 16:
        raise ValueError(f"sandworm: expected 16 frames, got {len(frames)}")
    indices = (0, 4, 7, 10, 14)
    hd4 = Image.new("RGBA", (48 * 4, 48 * len(indices) * 4))
    for row, index in enumerate(indices):
        frame = place_subject_hd4(frames[index], (48, 48))
        hd4.alpha_composite(frame, (0, row * 48 * 4))
    save_master4(hd4, master(150))


def build_all() -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    build_standard_vehicles()
    build_ornithopter()
    build_combat_tanks()
    build_siege_tank()
    build_sandworm()
    print("Dune 2000 units imported: 14 D2TM unit types, 3 tank variants")
    print("Classic fallback retained: UNIT_FRIGATE (no Dune 2000 sheet)")


def main() -> None:
    build_all()


if __name__ == "__main__":
    main()
