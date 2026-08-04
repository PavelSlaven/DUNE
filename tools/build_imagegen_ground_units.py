#!/usr/bin/env python3
"""Build direction-locked HD4 ground units from accepted ImageGen masters."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageFilter

from build_dune2000_units import (
    house_mask,
    neutralize_house_colours,
    resize_premultiplied,
)


ROOT = Path(__file__).resolve().parents[1]
GENERATED = (
    ROOT / "resources" / "hd" / "generated" / "preview4" / "units"
)
ALPHA = GENERATED / "alpha"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
PREVIEW = ROOT / "resources" / "hd" / "previews" / "ru4"

DIRECTION_ANGLES = (-90, -45, 0, 45, 90, 135, 180, -135)


@dataclass(frozen=True)
class UnitSpec:
    source_name: str
    resource_id: int
    shadow_id: int
    resource_name: str
    frame_size: tuple[int, int]
    rows: int
    content_scale: float = 0.88


UNITS = (
    UnitSpec(
        "harvester-v2",
        137,
        138,
        "UNIT_HARVESTER",
        (80, 52),
        4,
        0.92,
    ),
    UnitSpec(
        "launcher-v2",
        139,
        140,
        "UNIT_LAUNCHER",
        (32, 32),
        1,
        0.92,
    ),
    UnitSpec(
        "mcv-v2",
        141,
        142,
        "UNIT_MCV",
        (48, 50),
        1,
        0.90,
    ),
    UnitSpec(
        "quad-v2",
        145,
        146,
        "UNIT_QUAD",
        (32, 32),
        1,
        0.88,
    ),
    UnitSpec(
        "raider-v2",
        147,
        148,
        "UNIT_RAIDER",
        (28, 26),
        1,
        0.87,
    ),
    UnitSpec(
        "trike-v2",
        162,
        163,
        "UNIT_TRIKE",
        (28, 26),
        1,
        0.87,
    ),
)


def resource(folder: Path, resource_id: int) -> Path:
    return next(folder.glob(f"{resource_id:04d}_*.png"))


def crop_subject(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bounds = rgba.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("empty ImageGen unit")
    return rgba.crop(bounds)


def rotate_with_pivot(
    image: Image.Image,
    angle: float,
    pivot: tuple[float, float] | None = None,
) -> tuple[Image.Image, tuple[float, float]]:
    subject = image.convert("RGBA")
    if pivot is None:
        pivot = (subject.width / 2.0, subject.height / 2.0)
    radius = math.ceil(
        max(
            pivot[0],
            subject.width - pivot[0],
            pivot[1],
            subject.height - pivot[1],
        )
        * math.sqrt(2.0)
    )
    side = radius * 2 + 4
    center = side / 2.0
    canvas = Image.new("RGBA", (side, side))
    canvas.alpha_composite(
        subject,
        (
            round(center - pivot[0]),
            round(center - pivot[1]),
        ),
    )
    rotated = canvas.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=False,
    )
    bounds = rotated.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("rotated ImageGen unit became empty")
    return (
        rotated.crop(bounds),
        (center - bounds[0], center - bounds[1]),
    )


def fit_frame(
    subject: Image.Image,
    pivot: tuple[float, float],
    frame_size: tuple[int, int],
    content_scale: float,
) -> Image.Image:
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    maximum_width = (frame_width - 8) * content_scale
    maximum_height = (frame_height - 8) * content_scale
    scale = min(
        maximum_width / subject.width,
        maximum_height / subject.height,
    )
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = resize_premultiplied(subject, size)
    scaled_pivot = (pivot[0] * scale, pivot[1] * scale)
    frame = Image.new("RGBA", (frame_width, frame_height))
    frame.alpha_composite(
        subject,
        (
            round(frame_width / 2 - scaled_pivot[0]),
            round(frame_height / 2 - scaled_pivot[1]),
        ),
    )
    return frame


def build_direction_row(
    source: Image.Image,
    frame_size: tuple[int, int],
    content_scale: float,
    pivot: tuple[float, float] | None = None,
) -> Image.Image:
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    row = Image.new("RGBA", (frame_width * 8, frame_height))
    for index, angle in enumerate(DIRECTION_ANGLES):
        rotated, rotated_pivot = rotate_with_pivot(
            source,
            angle,
            pivot,
        )
        frame = fit_frame(
            rotated,
            rotated_pivot,
            frame_size,
            content_scale,
        )
        row.alpha_composite(frame, (index * frame_width, 0))
    return row


def repeat_rows(row: Image.Image, row_count: int) -> Image.Image:
    result = Image.new("RGBA", (row.width, row.height * row_count))
    for row_index in range(row_count):
        result.alpha_composite(row, (0, row_index * row.height))
    return result


def build_shadow(
    atlas: Image.Image,
    frame_size: tuple[int, int],
    rows: int,
) -> Image.Image:
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    result = Image.new("RGBA", atlas.size)
    for row in range(rows):
        for column in range(8):
            frame = atlas.crop(
                (
                    column * frame_width,
                    row * frame_height,
                    (column + 1) * frame_width,
                    (row + 1) * frame_height,
                )
            )
            alpha = frame.getchannel("A").filter(
                ImageFilter.GaussianBlur(1.6)
            ).point(lambda value: round(value * 0.20))
            shadow = Image.new(
                "RGBA",
                (frame_width, frame_height),
                (6, 5, 4, 0),
            )
            shadow.putalpha(alpha)
            result.alpha_composite(
                shadow,
                (column * frame_width + 5, row * frame_height + 5),
            )
    return result


def save_unit(spec: UnitSpec) -> Image.Image:
    source = crop_subject(Image.open(ALPHA / f"{spec.source_name}.png"))
    # The accepted harvester master has its intake at the bottom despite the
    # north-facing prompt. Normalize it once before the shared direction pass.
    if spec.resource_name == "UNIT_HARVESTER":
        source = source.rotate(
            180,
            resample=Image.Resampling.BICUBIC,
            expand=True,
        )
        source = crop_subject(source)
    row = build_direction_row(
        source,
        spec.frame_size,
        spec.content_scale,
    )
    coloured = repeat_rows(row, spec.rows)
    neutral = neutralize_house_colours(coloured)
    neutral.save(resource(MASTER, spec.resource_id), optimize=True)
    build_shadow(neutral, spec.frame_size, spec.rows).save(
        resource(MASTER, spec.shadow_id),
        optimize=True,
    )
    house_mask(coloured, spec.frame_size).save(
        EXTRA / f"HOUSEMASK_{spec.resource_name}.png",
        optimize=True,
    )
    return neutral


def save_tank() -> tuple[Image.Image, Image.Image]:
    frame_size = (32, 32)
    base_source = crop_subject(Image.open(ALPHA / "tankbase-v2.png"))
    base_row = build_direction_row(base_source, frame_size, 0.91)

    top_source = crop_subject(Image.open(ALPHA / "tanktop-v2.png"))
    # The generated turret pivot is below the visual centre because the long
    # barrel points north.
    top_pivot = (
        top_source.width / 2.0,
        top_source.height * 0.76,
    )
    top_row = build_direction_row(
        top_source,
        frame_size,
        0.88,
        top_pivot,
    )

    neutral_base = neutralize_house_colours(base_row)
    neutral_top = neutralize_house_colours(top_row)
    neutral_base.save(resource(MASTER, 159), optimize=True)
    neutral_top.save(resource(MASTER, 161), optimize=True)
    build_shadow(neutral_base, frame_size, 1).save(
        resource(MASTER, 160),
        optimize=True,
    )
    house_mask(base_row, frame_size).save(
        EXTRA / "HOUSEMASK_UNIT_TANKBASE.png",
        optimize=True,
    )
    house_mask(top_row, frame_size).save(
        EXTRA / "HOUSEMASK_UNIT_TANKTOP.png",
        optimize=True,
    )
    for house in ("ATREIDES", "HARKONNEN", "ORDOS"):
        neutral_base.save(
            EXTRA / f"HOUSEVARIANT_{house}_UNIT_TANKBASE.png",
            optimize=True,
        )
        neutral_top.save(
            EXTRA / f"HOUSEVARIANT_{house}_UNIT_TANKTOP.png",
            optimize=True,
        )
    return neutral_base, neutral_top


def build_preview(images: list[tuple[str, Image.Image, tuple[int, int]]]) -> None:
    cell = 180
    preview = Image.new(
        "RGBA",
        (cell * 4, cell * 2),
        (19, 22, 24, 255),
    )
    for index, (_name, atlas, frame_size) in enumerate(images):
        frame = atlas.crop(
            (0, 0, frame_size[0] * 4, frame_size[1] * 4)
        )
        bounds = frame.getchannel("A").getbbox()
        if bounds:
            frame = frame.crop(bounds)
        frame.thumbnail((150, 150), Image.Resampling.LANCZOS)
        x = index % 4 * cell + (cell - frame.width) // 2
        y = index // 4 * cell + (cell - frame.height) // 2
        preview.alpha_composite(frame, (x, y))
    PREVIEW.mkdir(parents=True, exist_ok=True)
    preview.save(PREVIEW / "imagegen_ground_units.png", optimize=True)


def main() -> None:
    images: list[tuple[str, Image.Image, tuple[int, int]]] = []
    for spec in UNITS:
        atlas = save_unit(spec)
        images.append((spec.resource_name, atlas, spec.frame_size))
    tank_base, tank_top = save_tank()
    images.append(("UNIT_TANKBASE", tank_base, (32, 32)))
    images.append(("UNIT_TANKTOP", tank_top, (32, 32)))
    build_preview(images)
    manifest = {
        "release": "v0.8.0-ru4-preview3",
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "sources": [spec.source_name for spec in UNITS]
        + ["tankbase-v2", "tanktop-v2"],
        "policy": (
            "one north-facing density-first master per object; deterministic "
            "pivot-locked 45 degree rotations"
        ),
    }
    (GENERATED / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("ImageGen ground units: 6 vehicles and layered combat tank")


if __name__ == "__main__":
    main()
