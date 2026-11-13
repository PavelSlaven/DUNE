#!/usr/bin/env python3
"""Replace D2TM HD world objects with Battle for Arrakis sprite artwork.

The source sheets define every silhouette, direction and House palette.
Processing is deterministic: crop service backgrounds, map directions, build
true HD4 atlases, generate shadows, and derive compact structure variants.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from build_dune2000_units import logical_shadow, remaster_subject, save_master4


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "resources"
    / "hd"
    / "source_references"
    / "battle_for_arrakis_complete"
)
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
PREVIEW = ROOT / "resources" / "hd" / "previews" / "ru4"

HOUSE_BLOCK = {"ATREIDES": 0, "ORDOS": 1, "HARKONNEN": 2}
HOUSE_SMALL_ROW = {"ATREIDES": 0, "HARKONNEN": 1, "ORDOS": 2}
HOUSE_COLOUR = {
    "ATREIDES": (46, 118, 198),
    "HARKONNEN": (184, 56, 40),
    "ORDOS": (48, 157, 75),
}
HOUSE_CODE = {"ATREIDES": "A", "HARKONNEN": "H", "ORDOS": "O"}
# Source: N, NE, E, SE, S, SW, W, NW. D2TM: E, NE, N, NW, W, SW, S, SE.
D2TM_FROM_CLOCKWISE = (2, 1, 0, 7, 6, 5, 4, 3)


def source(name: str) -> Image.Image:
    return Image.open(SOURCE / name).convert("RGBA")


def classic(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def master(resource_id: int) -> Path:
    return MASTER / classic(resource_id).name


def border_colours(image: Image.Image) -> set[tuple[int, int, int]]:
    rgb = image.convert("RGB")
    border = []
    border.extend(rgb.crop((0, 0, rgb.width, 1)).getdata())
    border.extend(rgb.crop((0, rgb.height - 1, rgb.width, rgb.height)).getdata())
    border.extend(rgb.crop((0, 0, 1, rgb.height)).getdata())
    border.extend(rgb.crop((rgb.width - 1, 0, rgb.width, rgb.height)).getdata())
    counts = Counter(border)
    selected: set[tuple[int, int, int]] = set()
    covered = 0
    target = max(1, round(len(border) * 0.72))
    for colour, count in counts.most_common(10):
        if count < 3 and selected:
            break
        selected.add(colour)
        covered += count
        if covered >= target:
            break
    return selected


def clean_cell(image: Image.Image, aggressive: bool = True) -> Image.Image:
    rgba = image.convert("RGBA")
    keys = border_colours(rgba)
    if aggressive:
        counts = Counter(rgba.convert("RGB").getdata())
        service_threshold = max(3, round(rgba.width * rgba.height * 0.15))
        keys.update(
            colour
            for colour, count in counts.items()
            if count >= service_threshold
        )
    pixels = []
    for red, green, blue, alpha in rgba.getdata():
        pixels.append(
            (0, 0, 0, 0)
            if alpha == 0 or (red, green, blue) in keys
            else (red, green, blue, alpha)
        )
    rgba.putdata(pixels)
    bounds = rgba.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("empty source frame after background removal")
    return rgba.crop(bounds)


def crop_cell(
    image: Image.Image,
    left: int,
    top: int,
    width: int = 32,
    height: int = 32,
) -> Image.Image:
    return clean_cell(image.crop((left, top, left + width, top + height)))


def map_directions(frames: list[Image.Image]) -> list[Image.Image]:
    if len(frames) != 8:
        raise ValueError(f"expected 8 directions, got {len(frames)}")
    return [frames[index] for index in D2TM_FROM_CLOCKWISE]


def derive_eight(north: Image.Image, north_east: Image.Image, east: Image.Image) -> list[Image.Image]:
    south_east = ImageOps.flip(north_east)
    south = ImageOps.flip(north)
    south_west = ImageOps.mirror(south_east)
    west = ImageOps.mirror(east)
    north_west = ImageOps.mirror(north_east)
    return [east, north_east, north, north_west, west, south_west, south, south_east]


def extract_large_row(
    filename: str,
    house: str,
    top: int,
    block_width: int = 256,
) -> list[Image.Image]:
    image = source(filename)
    # The large combat/siege sheets reserve the first 32-pixel cell in
    # every House block for the IDLE/FIRE label. The simple 256-wide
    # sheets start their direction cells immediately after the 8px gutter.
    left = (40 if block_width == 576 else 8) + HOUSE_BLOCK[house] * block_width
    frames = [crop_cell(image, left + column * 32, top) for column in range(8)]
    return map_directions(frames)


def fit_subject(
    subject: Image.Image,
    content_size: tuple[int, int],
) -> Image.Image:
    scale = min(
        content_size[0] / max(1, subject.width),
        content_size[1] / max(1, subject.height),
    )
    size = (
        max(1, round(subject.width * scale * 4)),
        max(1, round(subject.height * scale * 4)),
    )
    return remaster_subject(subject, size)


def place_frame(
    subject: Image.Image,
    frame_size: tuple[int, int],
    content_size: tuple[int, int],
    bottom_anchor: bool = False,
) -> Image.Image:
    result = Image.new("RGBA", (frame_size[0] * 4, frame_size[1] * 4))
    fitted = fit_subject(subject, content_size)
    left = (result.width - fitted.width) // 2
    if bottom_anchor:
        top = result.height - fitted.height - 8
    else:
        top = (result.height - fitted.height) // 2
    result.alpha_composite(fitted, (left, max(0, top)))
    return result


def build_atlas(
    rows: list[list[Image.Image]],
    frame_size: tuple[int, int],
    content_size: tuple[int, int],
    bottom_anchor: bool = False,
) -> Image.Image:
    if not rows or any(len(row) != 8 for row in rows):
        raise ValueError("directional atlas rows must have eight frames")
    atlas = Image.new(
        "RGBA",
        (frame_size[0] * 4 * 8, frame_size[1] * 4 * len(rows)),
    )
    for row, frames in enumerate(rows):
        for column, subject in enumerate(frames):
            atlas.alpha_composite(
                place_frame(subject, frame_size, content_size, bottom_anchor),
                (column * frame_size[0] * 4, row * frame_size[1] * 4),
            )
    return atlas


def transparent_mask(name: str, size: tuple[int, int]) -> None:
    save_master4(
        Image.new("RGBA", size),
        EXTRA / f"HOUSEMASK_{name}.png",
    )


def save_unit(
    resource_id: int,
    shadow_id: int | None,
    resource_name: str,
    variants: dict[str, list[list[Image.Image]]],
    frame_size: tuple[int, int],
    content_size: tuple[int, int],
    shadow_frame: tuple[int, int] | None = None,
    air_shadow: bool = False,
) -> Image.Image:
    atlases = {
        house: build_atlas(rows, frame_size, content_size)
        for house, rows in variants.items()
    }
    base = atlases.get("ATREIDES") or next(iter(atlases.values()))
    save_master4(base, master(resource_id))
    transparent_mask(resource_name, base.size)
    for house, atlas in atlases.items():
        save_master4(
            atlas,
            EXTRA / f"HV_{HOUSE_CODE[house]}_{resource_name}.png",
        )
    if shadow_id is not None:
        target = shadow_frame or frame_size
        rows = base.height // (frame_size[1] * 4)
        shadow = logical_shadow(
            base,
            frame_size,
            target,
            rows,
            0.30 if air_shadow else 0.18,
            (5, 5) if air_shadow else (2, 2),
        )
        save_master4(shadow, master(shadow_id))
    return base


def recolour_warm(image: Image.Image, house: str) -> Image.Image:
    target = HOUSE_COLOUR[house]
    output = []
    for red, green, blue, alpha in image.convert("RGBA").getdata():
        warm = alpha and red > 60 and red > blue * 1.18 and green < red * 0.92
        if warm:
            luminance = max(0.22, min(1.0, (red + green + blue) / 510))
            output.append(
                (
                    round(target[0] * luminance),
                    round(target[1] * luminance),
                    round(target[2] * luminance),
                    alpha,
                )
            )
        else:
            output.append((red, green, blue, alpha))
    result = Image.new("RGBA", image.size)
    result.putdata(output)
    return result


def build_large_units() -> list[tuple[str, Image.Image, tuple[int, int]]]:
    previews: list[tuple[str, Image.Image, tuple[int, int]]] = []
    specs = (
        (132, 133, "UNIT_DEVASTATOR", "550032_devastator.png", (38, 48), (34, 38)),
        (139, 140, "UNIT_LAUNCHER", "550380_missile_tank_deviator.png", (32, 32), (29, 27)),
        (141, 142, "UNIT_MCV", "550068_mcv.png", (48, 50), (38, 36)),
    )
    for resource_id, shadow_id, name, filename, frame_size, content_size in specs:
        variants = {
            house: [extract_large_row(filename, house, 56)]
            for house in HOUSE_BLOCK
        }
        atlas = save_unit(
            resource_id,
            shadow_id,
            name,
            variants,
            frame_size,
            content_size,
        )
        previews.append((name, atlas, frame_size))

    deviator = {
        house: [extract_large_row("550380_missile_tank_deviator.png", house, 56)]
        for house in HOUSE_BLOCK
    }
    atlas = save_unit(134, None, "UNIT_DEVIATOR", deviator, (32, 32), (29, 27))
    previews.append(("UNIT_DEVIATOR", atlas, (32, 32)))

    ornithopter = {
        house: [
            extract_large_row("550028_ornithopter.png", house, top)
            for top in (56, 88, 120, 88)
        ]
        for house in HOUSE_BLOCK
    }
    atlas = save_unit(
        143,
        144,
        "UNIT_ORNITHOPTER",
        ornithopter,
        (48, 48),
        (42, 40),
        air_shadow=True,
    )
    previews.append(("UNIT_ORNITHOPTER", atlas, (48, 48)))

    for prefix, base_id, shadow_id, top_id, filename in (
        ("UNIT_TANK", 159, 160, 161, "550029_combat_tank.png"),
        ("UNIT_SIEGE", 151, 152, 153, "550030_siege_tank.png"),
    ):
        frame_size = (32, 32) if prefix == "UNIT_TANK" else (36, 38)
        content_size = (30, 29) if prefix == "UNIT_TANK" else (33, 34)
        body_variants = {
            house: [extract_large_row(filename, house, 88, 576)]
            for house in HOUSE_BLOCK
        }
        top_variants = {
            house: [extract_large_row(filename, house, 56, 576)]
            for house in HOUSE_BLOCK
        }
        body_name = f"{prefix}BASE"
        top_name = f"{prefix}TOP"
        body = save_unit(
            base_id,
            shadow_id,
            body_name,
            body_variants,
            frame_size,
            content_size,
        )
        top = save_unit(
            top_id,
            None,
            top_name,
            top_variants,
            frame_size,
            content_size,
        )
        previews.extend(((body_name, body, frame_size), (top_name, top, frame_size)))

    # D2TM has a Sonic Tank but the Sega catalog has no separate sheet.
    # Use the complete Siege Tank model so no non-Sega artwork remains.
    sonic_variants = {}
    for house in HOUSE_BLOCK:
        body = extract_large_row("550030_siege_tank.png", house, 88, 576)
        top = extract_large_row("550030_siege_tank.png", house, 56, 576)
        combined = []
        for body_frame, top_frame in zip(body, top):
            canvas = Image.new("RGBA", (48, 48))
            for subject in (body_frame, top_frame):
                canvas.alpha_composite(
                    subject,
                    (
                        (48 - subject.width) // 2,
                        (48 - subject.height) // 2,
                    ),
                )
            bounds = canvas.getchannel("A").getbbox()
            combined.append(canvas.crop(bounds) if bounds else canvas)
        sonic_variants[house] = [combined]
    sonic = save_unit(
        157,
        158,
        "UNIT_SONICTANK",
        sonic_variants,
        (32, 32),
        (30, 29),
    )
    previews.append(("UNIT_SONICTANK", sonic, (32, 32)))
    return previews


def small_three_direction_variants(
    filename: str,
    row_height: int,
    x_positions: tuple[int, int, int],
    phase_offset: int = 0,
) -> dict[str, list[Image.Image]]:
    image = source(filename)
    result = {}
    for house, row in HOUSE_SMALL_ROW.items():
        top = row * row_height
        frames = [
            crop_cell(image, left + phase_offset, top, 32, 32)
            for left in x_positions
        ]
        result[house] = derive_eight(frames[0], frames[1], frames[2])
    return result


def build_small_vehicles() -> list[tuple[str, Image.Image, tuple[int, int]]]:
    previews: list[tuple[str, Image.Image, tuple[int, int]]] = []
    carryall_phases = []
    for positions in ((0, 33, 66), (101, 134, 167)):
        carryall_phases.append(
            small_three_direction_variants(
                "141660_carryall.png",
                35,
                positions,
            )
        )
    carryall = {
        house: [phase[house] for phase in carryall_phases]
        for house in HOUSE_SMALL_ROW
    }
    atlas = save_unit(
        130,
        131,
        "UNIT_CARRYALL",
        carryall,
        (48, 48),
        (42, 38),
        shadow_frame=(50, 56),
        air_shadow=True,
    )
    previews.append(("UNIT_CARRYALL", atlas, (48, 48)))

    harvester_dirs = small_three_direction_variants(
        "141659_harvester.png",
        32,
        (0, 32, 63),
    )
    harvester = {house: [frames] * 4 for house, frames in harvester_dirs.items()}
    atlas = save_unit(
        137,
        138,
        "UNIT_HARVESTER",
        harvester,
        (80, 52),
        (48, 40),
    )
    previews.append(("UNIT_HARVESTER", atlas, (80, 52)))

    circles = (
        ("169130_quad.png", 84, 145, 146, "UNIT_QUAD", (32, 32), (28, 26)),
        ("169129_trike_raider.png", 112, 147, 148, "UNIT_RAIDER", (28, 26), (25, 23)),
        ("169129_trike_raider.png", 112, 162, 163, "UNIT_TRIKE", (28, 26), (25, 23)),
    )
    for filename, top, resource_id, shadow_id, name, frame_size, content_size in circles:
        image = source(filename)
        y_mid = top + 40
        y_bottom = top + 80
        cells = {
            "N": crop_cell(image, 48, top, 16, 16),
            "NE": crop_cell(image, 68, top, 16, 16),
            "E": crop_cell(image, 88, y_mid, 16, 16),
            "SE": crop_cell(image, 68, y_bottom, 16, 16),
            "S": crop_cell(image, 48, y_bottom, 16, 16),
            "SW": crop_cell(image, 28, y_bottom, 16, 16),
            "W": crop_cell(image, 8, y_mid, 16, 16),
            "NW": crop_cell(image, 28, top, 16, 16),
        }
        ordered = [cells[key] for key in ("E", "NE", "N", "NW", "W", "SW", "S", "SE")]
        variants = {
            house: [[recolour_warm(frame, house) for frame in ordered]]
            for house in HOUSE_COLOUR
        }
        atlas = save_unit(
            resource_id,
            shadow_id,
            name,
            variants,
            frame_size,
            content_size,
        )
        previews.append((name, atlas, frame_size))
    return previews


def build_frigate_and_worm() -> list[tuple[str, Image.Image, tuple[int, int]]]:
    ship = source("550136_starport_ship.png")
    ship_frames = [
        crop_cell(ship, 8 + index * 40, 64, 40, 40)
        for index in range(8)
    ]
    ship_frames = map_directions(ship_frames)
    ship_variants = {house: [ship_frames] for house in HOUSE_COLOUR}
    frigate = save_unit(
        135,
        136,
        "UNIT_FRIGATE",
        ship_variants,
        (64, 64),
        (58, 56),
        air_shadow=True,
    )

    worm_source = source("550031_sandworm.png")
    frames = [
        crop_cell(worm_source, 168 + index * 40, 24, 40, 40)
        for index in range(5)
    ]
    worm = Image.new("RGBA", (48 * 4, 48 * 4 * 5))
    for row, frame in enumerate(frames):
        worm.alpha_composite(
            place_frame(frame, (48, 48), (40, 40)),
            (0, row * 48 * 4),
        )
    save_master4(worm, master(150))
    return [
        ("UNIT_FRIGATE", frigate, (64, 64)),
        ("UNIT_SANDWORM", worm, (48, 48)),
    ]


def infantry_directions(filename: str, group: bool) -> list[Image.Image]:
    image = source(filename)
    if group:
        points = {
            "N": (28, 92),
            "NE": (48, 92),
            "E": (48, 112),
            "SE": (48, 132),
            "S": (28, 132),
            "SW": (8, 132),
            "W": (8, 112),
            "NW": (8, 92),
        }
        width = height = 16
    else:
        points = {
            "N": (20, 16),
            "NE": (32, 16),
            "E": (32, 28),
            "SE": (32, 40),
            "S": (20, 40),
            "SW": (8, 40),
            "W": (8, 28),
            "NW": (8, 16),
        }
        width = height = 8
    return [
        crop_cell(image, *points[key], width, height)
        for key in ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
    ]


def build_infantry() -> list[tuple[str, Image.Image, tuple[int, int]]]:
    specs = (
        (149, "UNIT_SABOTEUR", "169099_soldier_infantry.png", False, (8, 8)),
        (154, "UNIT_SINGLEFREMEN", "169099_soldier_infantry.png", False, (8, 8)),
        (155, "UNIT_SOLDIER", "169099_soldier_infantry.png", False, (8, 8)),
        (156, "UNIT_SOLDIERS", "169099_soldier_infantry.png", True, (14, 14)),
        (164, "UNIT_TRIPLEFREMEN", "169099_soldier_infantry.png", True, (14, 14)),
        (165, "UNIT_TROOPER", "169128_trooper_troopers.png", False, (8, 8)),
        (166, "UNIT_TROOPERS", "169128_trooper_troopers.png", True, (14, 14)),
    )
    previews = []
    for resource_id, name, filename, group, content_size in specs:
        frames = infantry_directions(filename, group)
        variants = {
            house: [[recolour_warm(frame, house) for frame in frames] for _ in range(4)]
            for house in HOUSE_COLOUR
        }
        atlas = save_unit(
            resource_id,
            None,
            name,
            variants,
            (32, 32),
            content_size,
        )
        previews.append((name, atlas, (32, 32)))
    return previews


@dataclass(frozen=True)
class BuildingSpec:
    resource_id: int
    shadow_id: int
    name: str
    frame_size: tuple[int, int]
    frames: int
    source_cells: tuple[int, int, int, int]
    directional: bool = False


BUILDINGS = (
    BuildingSpec(1, 2, "BUILD_BARRACKS", (64, 64), 1, (3, 6, 6, 9)),
    BuildingSpec(3, 4, "BUILD_CONSTYARD", (64, 64), 1, (0, 6, 3, 9)),
    BuildingSpec(5, 7, "BUILD_HEAVYFACTORY", (96, 64), 11, (13, 2, 16, 4)),
    BuildingSpec(8, 9, "BUILD_HIGHTECH", (96, 64), 7, (9, 1, 12, 3)),
    BuildingSpec(10, 11, "BUILD_IX", (64, 64), 1, (7, 3, 10, 5)),
    BuildingSpec(12, 14, "BUILD_LIGHTFACTORY", (64, 64), 1, (13, 4, 16, 6)),
    BuildingSpec(15, 16, "BUILD_PALACE", (96, 96), 1, (3, 3, 7, 5)),
    BuildingSpec(26, 27, "BUILD_RADAR", (64, 64), 8, (0, 1, 3, 3)),
    BuildingSpec(28, 29, "BUILD_REFINERY", (96, 64), 8, (13, 0, 16, 2)),
    BuildingSpec(30, 31, "BUILD_REPAIR", (96, 64), 8, (0, 3, 3, 5)),
    BuildingSpec(32, 33, "BUILD_RTURRET", (32, 32), 8, (4, 10, 5, 11), True),
    BuildingSpec(34, 35, "BUILD_SILO", (64, 64), 1, (3, 1, 6, 3)),
    BuildingSpec(36, 37, "BUILD_STARPORT", (96, 96), 8, (13, 6, 16, 8)),
    BuildingSpec(38, 39, "BUILD_TURRET", (32, 32), 8, (0, 10, 1, 11), True),
    BuildingSpec(40, 41, "BUILD_WINDTRAP", (64, 64), 1, (6, 1, 9, 3)),
    BuildingSpec(42, 43, "BUILD_WOR", (64, 64), 1, (6, 6, 9, 9)),
)


def building_subject(spec: BuildingSpec) -> Image.Image:
    image = source("239094_buildings.png")
    left, top, right, bottom = spec.source_cells
    return clean_cell(
        image.crop((left * 32, top * 32, right * 32, bottom * 32)),
        aggressive=False,
    )


def rotate_directions(subject: Image.Image) -> list[Image.Image]:
    # Source turret points north. Generate the exact eight D2TM headings.
    angles = (-90, -45, 0, 45, 90, 135, 180, -135)
    return [
        subject.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        for angle in angles
    ]


def build_buildings() -> list[tuple[str, Image.Image, tuple[int, int]]]:
    previews = []
    for spec in BUILDINGS:
        subject = building_subject(spec)
        directions = rotate_directions(subject) if spec.directional else [subject] * 8
        rows = [directions] * spec.frames
        content_ratio = 0.76 if spec.directional else 0.84
        content_size = (
            max(10, round(spec.frame_size[0] * content_ratio)),
            max(10, round(spec.frame_size[1] * content_ratio)),
        )
        atlas = build_atlas(
            rows,
            spec.frame_size,
            content_size,
            bottom_anchor=True,
        )
        # Structure animation/direction frames are stored vertically by D2TM.
        frame_width = spec.frame_size[0] * 4
        frame_height = spec.frame_size[1] * 4
        compact = Image.new(
            "RGBA",
            (frame_width, frame_height * spec.frames),
        )
        for row in range(spec.frames):
            column = row if spec.directional else 0
            compact.alpha_composite(
                atlas.crop(
                    (
                        column * frame_width,
                        row * frame_height,
                        (column + 1) * frame_width,
                        (row + 1) * frame_height,
                    )
                ),
                (0, row * frame_height),
            )
        atlas = compact
        save_master4(atlas, master(spec.resource_id))
        transparent_mask(spec.name, atlas.size)
        for code in ("A", "H", "O"):
            save_master4(atlas, EXTRA / f"HV_{code}_{spec.name}.png")
            save_master4(
                Image.new("RGBA", atlas.size),
                EXTRA / f"HM_HV_{code}_{spec.name}.png",
            )
        shadow = Image.new("RGBA", atlas.size)
        for row in range(spec.frames):
            frame = atlas.crop(
                (0, row * frame_height, frame_width, (row + 1) * frame_height)
            )
            alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(1.8))
            alpha = alpha.point(lambda value: round(value * 0.16))
            silhouette = Image.new("RGBA", frame.size, (7, 5, 3, 0))
            silhouette.putalpha(alpha)
            frame_shadow = Image.new("RGBA", frame.size)
            frame_shadow.alpha_composite(silhouette, (8, 8))
            shadow.alpha_composite(frame_shadow, (0, row * frame_height))
        save_master4(shadow, master(spec.shadow_id))
        previews.append((spec.name, atlas, spec.frame_size))
    return previews


def first_frame(
    atlas: Image.Image,
    frame_size: tuple[int, int],
) -> Image.Image:
    return atlas.crop((0, 0, frame_size[0] * 4, frame_size[1] * 4))


def build_preview(items: list[tuple[str, Image.Image, tuple[int, int]]]) -> None:
    cell_width = 224
    cell_height = 184
    columns = 5
    rows = (len(items) + columns - 1) // columns
    canvas = Image.new(
        "RGBA",
        (cell_width * columns, cell_height * rows),
        (25, 28, 31, 255),
    )
    font = ImageFont.truetype(
        ROOT / "resources" / "bin" / "data" / "PTSansNarrow-Regular.ttf",
        18,
    )
    drawer = ImageDraw.Draw(canvas)
    for index, (name, atlas, frame_size) in enumerate(items):
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        frame = first_frame(atlas, frame_size)
        frame.thumbnail((cell_width - 20, cell_height - 36), Image.Resampling.LANCZOS)
        canvas.alpha_composite(
            frame,
            (
                x + (cell_width - frame.width) // 2,
                y + 26 + (cell_height - 32 - frame.height) // 2,
            ),
        )
        drawer.text((x + 6, y + 4), name, font=font, fill=(238, 211, 153, 255))
    PREVIEW.mkdir(parents=True, exist_ok=True)
    canvas.save(PREVIEW / "battle_for_arrakis_complete_world.png")


def write_manifest() -> None:
    urls = {
        "141660_carryall.png": 141660,
        "550029_combat_tank.png": 550029,
        "550032_devastator.png": 550032,
        "141659_harvester.png": 141659,
        "550068_mcv.png": 550068,
        "550380_missile_tank_deviator.png": 550380,
        "550028_ornithopter.png": 550028,
        "169130_quad.png": 169130,
        "550031_sandworm.png": 550031,
        "550030_siege_tank.png": 550030,
        "169099_soldier_infantry.png": 169099,
        "550136_starport_ship.png": 550136,
        "169129_trike_raider.png": 169129,
        "169128_trooper_troopers.png": 169128,
        "239094_buildings.png": 239094,
    }
    entries = []
    for filename, asset_id in urls.items():
        path = SOURCE / filename
        entries.append(
            {
                "file": filename,
                "asset_id": asset_id,
                "page_url": (
                    "https://www.spriters-resource.com/sega_genesis/"
                    f"duneiithebattleforarrakis/asset/{asset_id}/"
                ),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "size": Image.open(path).size,
            }
        )
    manifest = {
        "release": "v0.8.0-ru4-preview4",
        "source_game": "Dune II: The Battle for Arrakis (Sega Genesis)",
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "files": entries,
        "notes": [
            "All D2TM HD world objects now use Battle for Arrakis silhouettes.",
            "Sonic Tank reuses the Sega Siege Tank because the catalog has no separate Sonic Tank sheet.",
            "Buildings are assembled directly from the 32x32 modular Sega building sheet.",
            "HD2 is derived later from these HD4 masters.",
        ],
    }
    (SOURCE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_all() -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    items = []
    items.extend(build_large_units())
    items.extend(build_small_vehicles())
    items.extend(build_frigate_and_worm())
    items.extend(build_infantry())
    items.extend(build_buildings())
    build_preview(items)
    write_manifest()
    print(
        "Battle for Arrakis world: 20 D2TM unit resources, "
        "7 infantry resources and 16 structures"
    )


if __name__ == "__main__":
    build_all()
