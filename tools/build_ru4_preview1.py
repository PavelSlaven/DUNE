#!/usr/bin/env python3
"""Build exact-size ru4-preview1 HD4 world masters from approved concept sheets."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageStat
from build_dune2000_buildings import build_all as build_dune2000_buildings
from build_dune2000_units import build_all as build_dune2000_units
from build_pixvoxel_infantry import build_all as build_pixvoxel_infantry


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "resources" / "hd" / "generated" / "ru4_preview1"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"


def classic(index: int) -> Path:
    return next(CLASSIC.glob(f"{index:04d}_*.png"))


def master(index: int) -> Path:
    source = classic(index)
    return MASTER / source.name


def green_to_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = []
    for r, g, b, _ in rgba.getdata():
        green_distance = g - max(r, b)
        alpha = 255 - max(0, min(255, green_distance * 3))
        if g > 100 and green_distance > 10:
            g = min(g, (r + b) // 2)
        pixels.append((r, g, b, alpha))
    rgba.putdata(pixels)
    alpha = rgba.getchannel("A").filter(ImageFilter.GaussianBlur(0.45))
    rgba.putalpha(alpha)
    return rgba


def black_to_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = []
    for r, g, b, _ in rgba.getdata():
        peak = max(r, g, b)
        alpha = max(0, min(255, int((peak - 2) * 1.35)))
        pixels.append((r, g, b, alpha))
    rgba.putdata(pixels)
    return rgba


def crop_subject(image: Image.Image, threshold: int = 96) -> Image.Image:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 1 if value > threshold else 0)
    column_minimum = max(2, round(image.height * 0.02))
    row_minimum = max(2, round(image.width * 0.02))
    columns = [
        x
        for x in range(image.width)
        if sum(mask.getpixel((x, y)) for y in range(image.height))
        >= column_minimum
    ]
    rows = [
        y
        for y in range(image.height)
        if sum(mask.getpixel((x, y)) for x in range(image.width))
        >= row_minimum
    ]
    box = (
        (min(columns), min(rows), max(columns) + 1, max(rows) + 1)
        if columns and rows
        else None
    )
    return image.crop(box) if box else image.copy()


def fit_subject(
    subject: Image.Image,
    size: tuple[int, int],
    fill: float = 0.88,
    bottom_margin: int = 4,
) -> Image.Image:
    subject = crop_subject(subject)
    max_width = max(1, int(size[0] * fill))
    max_height = max(1, int(size[1] * fill))
    scale = min(max_width / subject.width, max_height / subject.height)
    scaled = subject.resize(
        (
            max(1, int(subject.width * scale)),
            max(1, int(subject.height * scale)),
        ),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", size)
    x = (size[0] - scaled.width) // 2
    y = size[1] - bottom_margin - scaled.height
    canvas.alpha_composite(scaled, (x, max(0, y)))
    return canvas


def grid_subjects(
    source: Path,
    columns: int,
    rows: int,
    green: bool = True,
) -> list[Image.Image]:
    image = Image.open(source).convert("RGBA")
    cell_width = image.width / columns
    cell_height = image.height / rows
    result = []
    for row in range(rows):
        for column in range(columns):
            left = round(column * cell_width)
            top = round(row * cell_height)
            right = round((column + 1) * cell_width)
            bottom = round((row + 1) * cell_height)
            cell = image.crop((left, top, right, bottom))
            result.append(green_to_alpha(cell) if green else black_to_alpha(cell))
    return result


def save_atlas(
    frames: list[Image.Image],
    frame_size: tuple[int, int],
    columns: int,
    rows: int,
    path: Path,
) -> Image.Image:
    if len(frames) != columns * rows:
        raise ValueError(f"{path.name}: expected {columns * rows} frames")
    atlas = Image.new(
        "RGBA",
        (frame_size[0] * columns, frame_size[1] * rows),
    )
    for index, frame in enumerate(frames):
        atlas.alpha_composite(
            frame,
            (
                (index % columns) * frame_size[0],
                (index // columns) * frame_size[1],
            ),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(path)
    return atlas


TERRAIN_VARIANT_COUNT = 5
TERRAIN_PALETTES = {
    "sand": (162, 124, 73),
    "hill": (145, 101, 56),
    "rock": (91, 82, 70),
    "mountain": (87, 61, 42),
    "spice": (174, 91, 42),
    "spicehill": (139, 62, 29),
}
TERRAIN_NAMES = {
    118: "HILL",
    119: "MOUNTAIN",
    120: "ROCK",
    121: "SAND",
    123: "SPICE",
    124: "SPICEHILL",
}


def calm_periodic_material(kind: str, variant: int, size: int = 128) -> Image.Image:
    """Create a low-contrast tile whose variants have identical borders."""
    base_r, base_g, base_b = TERRAIN_PALETTES[kind]
    kind_phase = list(TERRAIN_PALETTES).index(kind) * 0.71
    pixels = []
    for y in range(size):
        normalized_y = y / (size - 1)
        edge_y = math.sin(math.pi * normalized_y) ** 2
        for x in range(size):
            normalized_x = x / (size - 1)
            edge_x = math.sin(math.pi * normalized_x) ** 2
            common = (
                math.sin(
                    math.tau * (normalized_x + normalized_y) + kind_phase
                )
                + 0.48
                * math.sin(
                    math.tau * (2 * normalized_x - normalized_y)
                    + kind_phase * 0.37
                )
                + 0.26
                * math.cos(
                    math.tau * (normalized_x + 2 * normalized_y)
                    - kind_phase * 0.53
                )
            )
            interior = 0.0
            if variant:
                phase = variant * 1.19 + kind_phase
                interior = edge_x * edge_y * (
                    math.sin(
                        math.tau
                        * (
                            (variant % 3 + 1) * normalized_x
                            + ((variant + 1) % 3 + 1) * normalized_y
                        )
                        + phase
                    )
                    + 0.55
                    * math.cos(
                        math.tau
                        * (
                            ((variant + 2) % 4 + 1) * normalized_x
                            - normalized_y
                        )
                        - phase * 0.61
                    )
                )
            common_strength = 5.0
            variant_strength = 9.0
            value = common * common_strength + interior * variant_strength
            red = max(0, min(255, round(base_r + value)))
            green = max(0, min(255, round(base_g + value * 0.82)))
            blue = max(0, min(255, round(base_b + value * 0.62)))
            pixels.append((red, green, blue))
    image = Image.new("RGB", (size, size))
    image.putdata(pixels)
    return image


def terrain_mask(index: int, frame: Image.Image) -> Image.Image:
    def score(pixel: tuple[int, int, int]) -> int:
        red, green, blue = pixel
        if index == 118:
            distance = abs(red - 182) + abs(green - 121) + abs(blue - 56)
            return max(0, min(255, (distance - 8) * 7))
        if index == 119:
            return max(0, min(255, (red - green - 4) * 11))
        if index == 120:
            return max(0, min(255, (132 - (red + green + blue) / 3) * 5))
        if index == 123:
            return max(0, min(255, (red - green - 45) * 7))
        if index == 124:
            distance = abs(red - 189) + abs(green - 96) + abs(blue - 32)
            return max(0, min(255, (distance - 8) * 6))
        raise ValueError(f"unsupported terrain resource {index}")

    mask = Image.new("L", frame.size)
    mask.putdata([round(score(pixel)) for pixel in frame.getdata()])
    return mask.resize((128, 128), Image.Resampling.BICUBIC).filter(
        ImageFilter.GaussianBlur(1.2)
    )


def terrain_atlas(
    index: int,
    base_kind: str,
    overlay_kind: str,
    variant: int,
) -> Image.Image:
    source = Image.open(classic(index)).convert("RGB")
    frame_count = source.width // 32
    base = calm_periodic_material(base_kind, variant)
    overlay = calm_periodic_material(overlay_kind, variant)
    frames = []
    for frame_index in range(frame_count):
        classic_frame = source.crop(
            (frame_index * 32, 0, (frame_index + 1) * 32, 32)
        )
        mask = terrain_mask(index, classic_frame)
        frame = Image.composite(overlay, base, mask)

        # Keep broad relief from the classic cell, without its pixel noise.
        if index in (118, 119, 124):
            relief = classic_frame.convert("L").resize(
                (128, 128), Image.Resampling.BICUBIC
            ).filter(ImageFilter.GaussianBlur(5.0))
            mean = ImageStat.Stat(relief).mean[0]
            relief = relief.point(
                lambda value: max(
                    224,
                    min(255, round(240 + (value - mean) * 0.12)),
                )
            )
            frame = ImageChops.multiply(
                frame,
                Image.merge("RGB", (relief, relief, relief)),
            )
        frames.append(frame.convert("RGBA"))
    atlas = Image.new("RGBA", (128 * frame_count, 128))
    for frame_index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (frame_index * 128, 0))
    return atlas


def terrain_variant_path(index: int, variant: int) -> Path:
    if variant == 0:
        return master(index)
    return EXTRA / f"TERRAIN_{TERRAIN_NAMES[index]}_VAR_{variant:02d}.png"


def build_terrain() -> None:
    EXTRA.mkdir(parents=True, exist_ok=True)
    terrain_recipes = {
        118: ("sand", "hill"),
        119: ("rock", "mountain"),
        120: ("sand", "rock"),
        123: ("sand", "spice"),
        124: ("spice", "spicehill"),
    }
    for variant in range(TERRAIN_VARIANT_COUNT):
        calm_periodic_material("sand", variant).convert("RGBA").save(
            terrain_variant_path(121, variant)
        )
        for index, (base_kind, overlay_kind) in terrain_recipes.items():
            terrain_atlas(index, base_kind, overlay_kind, variant).save(
                terrain_variant_path(index, variant)
            )


def house_mask(image: Image.Image, color: str = "blue") -> Image.Image:
    pixels = []
    for r, g, b, a in image.convert("RGBA").getdata():
        if color == "blue":
            selected = b > r * 1.08 and b > g * 1.04 and b > 55
        elif color == "red":
            selected = r > g * 1.18 and r > b * 1.10 and r > 55
        else:
            selected = g > r * 1.08 and g > b * 1.05 and g > 45
        strength = 255 if selected and a else 0
        pixels.append((255, 255, 255, strength))
    mask = Image.new("RGBA", image.size)
    mask.putdata(pixels)
    return mask.filter(ImageFilter.GaussianBlur(0.6))


def shadow_from_alpha(image: Image.Image) -> Image.Image:
    alpha = image.getchannel("A").filter(ImageFilter.GaussianBlur(4.0))
    alpha = alpha.point(lambda value: int(value * 0.42))
    shifted = ImageChops.offset(alpha, 10, 8)
    shadow = Image.new("RGBA", image.size, (7, 5, 3, 0))
    shadow.putalpha(shifted)
    return shadow


def build_harvester() -> None:
    subjects = grid_subjects(
        GENERATED / "harvester_sheet.png",
        4,
        2,
    )
    directions = [fit_subject(item, (320, 208), 0.86, 5) for item in subjects]
    frames = []
    for animation in range(4):
        for frame in directions:
            animated = frame.copy()
            if animation:
                strip = animated.crop((32, 160, 288, 204))
                strip = ImageEnhance.Brightness(strip).enhance(1.0 + animation * 0.035)
                animated.alpha_composite(strip, (32, 160))
            frames.append(animated)
    atlas = save_atlas(frames, (320, 208), 8, 4, master(137))
    shadow_from_alpha(atlas).save(master(138))
    house_mask(atlas).save(EXTRA / "HOUSEMASK_UNIT_HARVESTER.png")


def build_tank_variant(sheet: str, house: str, source_color: str) -> None:
    cells = grid_subjects(GENERATED / sheet, 4, 4)
    # A combat tank must nearly fill its logical 32x32 cell, matching the
    # proportions of the Dune 2000 sheets and the classic D2TM footprint.
    body = [fit_subject(item, (128, 128), 0.94, 12) for item in cells[:8]]
    top = [fit_subject(item, (128, 128), 0.82, 44) for item in cells[8:16]]
    body_atlas = save_atlas(
        body,
        (128, 128),
        8,
        1,
        EXTRA / f"HOUSEVARIANT_{house}_UNIT_TANKBASE.png",
    )
    save_atlas(
        top,
        (128, 128),
        8,
        1,
        EXTRA / f"HOUSEVARIANT_{house}_UNIT_TANKTOP.png",
    )
    if house == "ATREIDES":
        shadow_from_alpha(body_atlas).save(master(160))


def build_buildings() -> None:
    windtrap = fit_subject(
        green_to_alpha(Image.open(GENERATED / "windtrap.png")),
        (256, 256),
        0.94,
        3,
    )
    windtrap.save(master(40))
    shadow_from_alpha(windtrap).save(master(41))
    house_mask(windtrap).save(EXTRA / "HOUSEMASK_BUILD_WINDTRAP.png")

    refinery_frame = fit_subject(
        green_to_alpha(Image.open(GENERATED / "refinery.png")),
        (384, 256),
        0.95,
        3,
    )
    refinery_frames = []
    for frame_index in range(8):
        frame = refinery_frame.copy()
        if frame_index:
            glow = frame.crop((124, 20, 260, 100))
            glow = ImageEnhance.Brightness(glow).enhance(
                0.94 + (frame_index % 4) * 0.04
            )
            frame.alpha_composite(glow, (124, 20))
        refinery_frames.append(frame)
    refinery = save_atlas(
        refinery_frames,
        (384, 256),
        1,
        8,
        master(28),
    )
    shadow_from_alpha(refinery).save(master(29))
    house_mask(refinery).save(EXTRA / "HOUSEMASK_BUILD_REFINERY.png")


def rotate_asset(subject: Image.Image, angle: float, size: tuple[int, int]) -> Image.Image:
    rotated = subject.rotate(angle, Image.Resampling.BICUBIC, expand=True)
    return fit_subject(rotated, size, 0.82, 4)


def subject_angle(subject: Image.Image) -> float:
    alpha = subject.convert("RGBA").getchannel("A")
    points = [
        (x, y, alpha.getpixel((x, y)))
        for y in range(alpha.height)
        for x in range(alpha.width)
        if alpha.getpixel((x, y)) > 64
    ]
    total = sum(weight for _x, _y, weight in points)
    center_x = sum(x * weight for x, _y, weight in points) / total
    center_y = sum(y * weight for _x, y, weight in points) / total
    points.sort(
        key=lambda point: (
            (point[0] - center_x) ** 2 + (point[1] - center_y) ** 2
        ),
        reverse=True,
    )
    far = points[: max(1, len(points) // 8)]
    far_total = sum(weight for _x, _y, weight in far)
    far_x = sum(x * weight for x, _y, weight in far) / far_total
    far_y = sum(y * weight for _x, y, weight in far) / far_total
    return math.degrees(math.atan2(far_y - center_y, far_x - center_x))


def orient_asset(
    subject: Image.Image,
    target_angle: float,
    size: tuple[int, int],
) -> Image.Image:
    # Pillow rotates counter-clockwise, while image-space angles grow
    # clockwise because Y points down.
    rotation = subject_angle(subject) - target_angle
    return rotate_asset(subject, rotation, size)


def build_effects() -> None:
    explosions = grid_subjects(
        GENERATED / "explosion_sheet.png",
        5,
        1,
        green=False,
    )
    explosion_frames = [
        fit_subject(item, (128, 128), 0.86, 6) for item in explosions
    ]
    save_atlas(explosion_frames, (128, 128), 5, 1, master(68))

    effects = grid_subjects(
        GENERATED / "effects_sheet.png",
        3,
        1,
        green=False,
    )
    muzzle, rocket, smoke = [crop_subject(item) for item in effects]
    rocket_directions = [
        orient_asset(rocket, -90 + direction * 22.5, (192, 192))
        for direction in range(16)
    ]
    rocket_frames = []
    for animation in range(2):
        for frame in rocket_directions:
            rocket_frames.append(
                ImageEnhance.Brightness(frame).enhance(1.0 + animation * 0.08)
            )
    save_atlas(rocket_frames, (192, 192), 16, 2, master(50))

    classic_flash = Image.open(classic(105)).convert("RGB")
    compact_muzzle = fit_subject(muzzle, (48, 48), 0.86, 3)
    tank_shot_frames = []
    for direction in range(8):
        classic_frame = classic_flash.crop(
            (direction * 64, 0, (direction + 1) * 64, 64)
        )
        luminance = classic_frame.convert("L")
        weights = [
            (x, y, luminance.getpixel((x, y)))
            for y in range(64)
            for x in range(64)
            if luminance.getpixel((x, y)) > 32
        ]
        total = sum(weight for _x, _y, weight in weights)
        center_x = round(
            sum(x * weight for x, _y, weight in weights) / total * 4
        )
        center_y = round(
            sum(y * weight for _x, y, weight in weights) / total * 4
        )
        frame = Image.new("RGBA", (256, 256))
        frame.alpha_composite(
            compact_muzzle,
            (
                center_x - compact_muzzle.width // 2,
                center_y - compact_muzzle.height // 2,
            ),
        )
        tank_shot_frames.append(frame)
    save_atlas(tank_shot_frames, (256, 256), 8, 1, master(105))

    smoke_frames = []
    for scale in (0.78, 0.92):
        subject = smoke.resize(
            (
                max(1, int(smoke.width * scale)),
                max(1, int(smoke.height * scale)),
            ),
            Image.Resampling.LANCZOS,
        )
        smoke_frames.append(fit_subject(subject, (192, 192), 0.82, 6))
    save_atlas(smoke_frames, (192, 192), 2, 1, master(100))

    single_muzzle = fit_subject(muzzle, (84, 64), 0.92, 2)
    single_muzzle.save(master(112))


def main() -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    build_terrain()
    build_dune2000_units()
    build_dune2000_buildings()
    build_pixvoxel_infantry()
    build_effects()
    print(f"ru4-preview1 masters: {MASTER}")
    print(f"ru4-preview1 appended resources: {EXTRA}")


if __name__ == "__main__":
    main()
