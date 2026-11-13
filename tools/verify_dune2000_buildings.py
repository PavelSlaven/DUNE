#!/usr/bin/env python3
"""Verify the direct Dune 2000 building imports before packing."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_dune2000_buildings import (
    BUILDINGS,
    EXTRA,
    HOUSES,
    HOUSE_CODES,
    MASTER,
    SOURCE,
)


ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
DIRECT_IDS = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16,
    26, 27, 28, 29, 30, 32, 34, 35, 36, 37, 38, 40, 41, 42, 43,
)


def classic(index: int) -> Path:
    return next(CLASSIC.glob(f"{index:04d}_*.png"))


def master(index: int) -> Path:
    return MASTER / classic(index).name


def has_keyed_magenta(image: Image.Image) -> bool:
    return any(
        r >= 245 and b >= 245 and g <= 16 and a
        for r, g, b, a in image.convert("RGBA").getdata()
    )


def average_saturation(image: Image.Image) -> float:
    opaque = [
        max(red, green, blue) - min(red, green, blue)
        for red, green, blue, alpha in image.convert("RGBA").getdata()
        if alpha > 64
    ]
    return sum(opaque) / len(opaque) if opaque else 0.0


def verify_sources(errors: list[str]) -> None:
    manifest = json.loads((SOURCE / "manifest.json").read_text("utf-8"))
    records = {
        entry["file"]: entry
        for entry in manifest["sources"]
        if entry["file"].startswith("dune2000_")
    }
    for spec in BUILDINGS:
        filename = f"dune2000_{spec.source_name}.png"
        path = SOURCE / filename
        record = records.get(filename)
        if not record:
            errors.append(f"source missing from manifest: {filename}")
            continue
        if not path.is_file():
            errors.append(f"source file missing: {filename}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != record["sha256"]:
            errors.append(f"source hash mismatch: {filename}")


def verify_direct_masters(errors: list[str]) -> None:
    for index in DIRECT_IDS:
        expected_image = Image.open(classic(index))
        path = master(index)
        if not path.is_file():
            errors.append(f"missing direct master for ID {index}")
            continue
        image = Image.open(path).convert("RGBA")
        expected = (expected_image.width * 4, expected_image.height * 4)
        if image.size != expected:
            errors.append(f"ID {index}: {image.size}, expected {expected}")
        if has_keyed_magenta(image):
            errors.append(f"ID {index}: keyed magenta remains")
        if index in (1, 3, 5, 8, 10, 12, 15, 26, 28, 30, 32, 34, 36, 38, 40, 42):
            saturation = average_saturation(image)
            if saturation > 38.0:
                errors.append(
                    f"ID {index}: building is not neutral enough "
                    f"(average saturation {saturation:.1f})"
                )

    for index in (6, 13):
        image = Image.open(master(index)).convert("RGBA")
        if image.getchannel("A").getbbox():
            errors.append(f"ID {index}: obsolete factory flash is not empty")


def verify_variants(errors: list[str]) -> None:
    for spec in BUILDINGS:
        expected = (
            spec.frame_size[0] * 4,
            spec.frame_size[1] * spec.frame_count * 4,
        )
        for house in HOUSES:
            variant_name = (
                f"HV_{HOUSE_CODES[house]}_{spec.resource_name}.png"
            )
            path = EXTRA / variant_name
            mask = EXTRA / f"HM_{variant_name}"
            if not path.is_file():
                errors.append(f"missing building variant: {variant_name}")
                continue
            image = Image.open(path).convert("RGBA")
            if image.size != expected:
                errors.append(
                    f"{variant_name}: {image.size}, expected {expected}"
                )
            if has_keyed_magenta(image):
                errors.append(f"{variant_name}: keyed magenta remains")
            saturation = average_saturation(image)
            if saturation > 38.0:
                errors.append(
                    f"{variant_name}: variant is not neutral enough "
                    f"(average saturation {saturation:.1f})"
                )
            frame_height = spec.frame_size[1] * 4
            for row in range(spec.frame_count):
                frame = image.crop(
                    (
                        0,
                        row * frame_height,
                        expected[0],
                        (row + 1) * frame_height,
                    )
                )
                if not frame.getchannel("A").getbbox():
                    errors.append(
                        f"{variant_name}: empty gameplay frame {row}"
                    )
            if not mask.is_file():
                errors.append(f"missing House mask: {mask.name}")
            elif Image.open(mask).size != expected:
                errors.append(f"{mask.name}: unexpected size")


def main() -> int:
    errors: list[str] = []
    verify_sources(errors)
    verify_direct_masters(errors)
    verify_variants(errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(
        "Dune 2000 building masters valid: "
        "11 sheets, 3 House variants, unchanged D2TM footprints"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
