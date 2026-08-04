#!/usr/bin/env python3
"""Normalize selected HD vehicle silhouettes to their classic logical size."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

from build_dune2000_units import resize_premultiplied
from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
CLASSIC_PACK = GAME / "data" / "sdl_data.dat"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
OUTPUT = ROOT / "artifacts" / "unit_size_normalization_v1"
STAGE = OUTPUT / "data"
BACKUP = OUTPUT / "backup"


@dataclass(frozen=True)
class Vehicle:
    resource_id: int
    name: str
    shadow_id: int | None
    columns: int
    rows: int
    logical_frame: tuple[int, int]


VEHICLES = (
    Vehicle(134, "UNIT_DEVIATOR", None, 8, 1, (32, 32)),
    Vehicle(143, "UNIT_ORNITHOPTER", 144, 8, 4, (48, 48)),
    Vehicle(145, "UNIT_QUAD", 146, 8, 1, (32, 32)),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frames(image: Image.Image, vehicle: Vehicle, density: int):
    frame_width = vehicle.logical_frame[0] * density
    frame_height = vehicle.logical_frame[1] * density
    expected = (frame_width * vehicle.columns, frame_height * vehicle.rows)
    if image.size != expected:
        raise AssertionError(f"{vehicle.name}: expected {expected}, got {image.size}")
    for row in range(vehicle.rows):
        for column in range(vehicle.columns):
            box = (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
            yield box, image.crop(box)


def major_extent(frame: Image.Image, density: int) -> float:
    bounds = frame.getchannel("A").getbbox()
    if bounds is None:
        raise AssertionError("transparent vehicle frame")
    return max(bounds[2] - bounds[0], bounds[3] - bounds[1]) / density


def apparent_scale(classic: Image.Image, hd4: Image.Image, vehicle: Vehicle) -> float:
    classic_frames = list(frames(classic, vehicle, 1))
    hd_frames = list(frames(hd4, vehicle, 4))
    ratios = [
        major_extent(hd_frame, 4) / major_extent(classic_frame, 1)
        for (_, classic_frame), (_, hd_frame) in zip(
            classic_frames, hd_frames, strict=True
        )
    ]
    return float(np.median(ratios))


def scale_frame(frame: Image.Image, factor: float) -> Image.Image:
    new_size = (
        max(1, round(frame.width * factor)),
        max(1, round(frame.height * factor)),
    )
    resized = resize_premultiplied(frame.convert("RGBA"), new_size)
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    x = (frame.width - resized.width) // 2
    y = (frame.height - resized.height) // 2
    if x >= 0 and y >= 0:
        result.alpha_composite(resized, (x, y))
        return result
    crop_left = max(0, -x)
    crop_top = max(0, -y)
    crop = resized.crop(
        (
            crop_left,
            crop_top,
            crop_left + frame.width,
            crop_top + frame.height,
        )
    )
    result.alpha_composite(crop)
    return result


def scale_atlas(image: Image.Image, vehicle: Vehicle, factor: float) -> Image.Image:
    result = Image.new("RGBA", image.size, (0, 0, 0, 0))
    for box, frame in frames(image.convert("RGBA"), vehicle, 4):
        result.alpha_composite(scale_frame(frame, factor), (box[0], box[1]))
    return result


def source_path(vehicle: Vehicle) -> Path:
    return MASTER / f"{vehicle.resource_id:04d}_{vehicle.name}.png"


def mask_paths(vehicle: Vehicle) -> tuple[Path, Path]:
    return (
        EXTRA / f"HM_{vehicle.name}.png",
        EXTRA / f"HOUSEMASK_{vehicle.name}.png",
    )


def patch_pack(
    source: Path,
    target: Path,
    replacements: dict[int, Image.Image],
    named_replacements: dict[str, Image.Image],
) -> dict[str, object]:
    before = read_pack(source)
    after = list(before)
    changed: set[int] = set()
    for resource_id, image in replacements.items():
        entry = before[resource_id]
        after[resource_id] = PackEntry(
            resource_id, entry.name, "PNG", encode_png(image)
        )
        changed.add(resource_id)
    for name, image in named_replacements.items():
        matches = [entry.index for entry in after if entry.name == name]
        if len(matches) != 1:
            raise AssertionError(f"expected one installed resource named {name}")
        resource_id = matches[0]
        after[resource_id] = PackEntry(
            resource_id, name, "PNG", encode_png(image)
        )
        changed.add(resource_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    write_pack(target, after)
    packed = read_pack(target)
    for entry in before:
        if entry.index in changed:
            continue
        current = packed[entry.index]
        if (
            entry.name != current.name
            or entry.extension != current.extension
            or entry.payload != current.payload
        ):
            raise AssertionError(f"unrelated resource changed: {entry.index}:{entry.name}")
    return {
        "path": str(target),
        "changed_ids": sorted(changed),
        "sha256": sha256(target),
    }


def install(staged: Path, live: Path) -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    backup = BACKUP / live.name
    if not backup.exists():
        shutil.copy2(live, backup)
    temporary = live.with_name(live.name + ".unit-size.tmp")
    try:
        shutil.copy2(staged, temporary)
        os.replace(temporary, live)
    finally:
        temporary.unlink(missing_ok=True)
    if sha256(live) != sha256(staged):
        raise AssertionError(f"installed pack differs from staged {live.name}")


def main() -> int:
    classic_entries = read_pack(CLASSIC_PACK)
    resources4: dict[int, Image.Image] = {}
    masks4: dict[str, Image.Image] = {}
    report: list[dict[str, object]] = []
    OUTPUT.mkdir(parents=True, exist_ok=True)

    for vehicle in VEHICLES:
        classic = decode_image(classic_entries[vehicle.resource_id].payload)
        if classic is None:
            raise AssertionError(f"cannot decode classic {vehicle.name}")
        original = Image.open(source_path(vehicle)).convert("RGBA")
        before_scale = apparent_scale(classic.convert("RGBA"), original, vehicle)
        factor = 1.0 / before_scale
        normalized = scale_atlas(original, vehicle, factor)
        after_scale = apparent_scale(classic.convert("RGBA"), normalized, vehicle)
        if abs(after_scale - 1.0) > 0.03:
            raise AssertionError(
                f"{vehicle.name}: normalized scale is {after_scale:.3f}"
            )
        resources4[vehicle.resource_id] = normalized
        if vehicle.shadow_id is not None:
            shadow_name = classic_entries[vehicle.shadow_id].name
            shadow_path = MASTER / f"{vehicle.shadow_id:04d}_{shadow_name}.png"
            resources4[vehicle.shadow_id] = scale_atlas(
                Image.open(shadow_path).convert("RGBA"), vehicle, factor
            )
        primary_mask, alias_mask = mask_paths(vehicle)
        mask = scale_atlas(Image.open(primary_mask).convert("RGBA"), vehicle, factor)
        masks4[f"HM_{vehicle.name}"] = mask
        normalized.save(OUTPUT / f"{vehicle.name}_HD4_NORMALIZED.png", optimize=True)
        report.append(
            {
                "id": vehicle.resource_id,
                "name": vehicle.name,
                "before": round(before_scale, 4),
                "factor": round(factor, 4),
                "after": round(after_scale, 4),
            }
        )

    # Keep accepted masters and their legacy aliases in sync.
    for vehicle in VEHICLES:
        resources4[vehicle.resource_id].save(source_path(vehicle), optimize=True)
        if vehicle.shadow_id is not None:
            shadow_name = classic_entries[vehicle.shadow_id].name
            resources4[vehicle.shadow_id].save(
                MASTER / f"{vehicle.shadow_id:04d}_{shadow_name}.png", optimize=True
            )
        for path in mask_paths(vehicle):
            masks4[f"HM_{vehicle.name}"].save(path, optimize=True)

    resources2 = {
        resource_id: image.resize(
            (image.width // 2, image.height // 2), Image.Resampling.LANCZOS
        )
        for resource_id, image in resources4.items()
    }
    masks2 = {
        name: image.resize(
            (image.width // 2, image.height // 2), Image.Resampling.LANCZOS
        )
        for name, image in masks4.items()
    }
    live2 = GAME / "data" / "sdl_data_hd2.dat"
    live4 = GAME / "data" / "sdl_data_hd4.dat"
    staged2 = STAGE / live2.name
    staged4 = STAGE / live4.name
    build2 = patch_pack(live2, staged2, resources2, masks2)
    build4 = patch_pack(live4, staged4, resources4, masks4)

    packed2 = read_pack(staged2)
    packed4 = read_pack(staged4)
    names = set(masks4)
    ids = set(resources4)
    ids.update(entry.index for entry in packed4 if entry.name in names)
    for resource_id in ids:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode staged resource {resource_id}")
        expected = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(image2.convert("RGBA"), expected).getbbox():
            raise AssertionError(f"HD2 resource {resource_id} is not an HD4 derivative")

    install(staged2, live2)
    install(staged4, live4)
    manifest = {
        "status": "installed",
        "excluded_ids": [130, 137],
        "vehicles": report,
        "packs": [build2, build4],
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
