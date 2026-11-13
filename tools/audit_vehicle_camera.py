#!/usr/bin/env python3
"""Audit ground-vehicle HD4 atlases for flat top-down rotation artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
GAME_PACK = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data\sdl_data_hd4.dat")
CLASSIC_PACK = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data\sdl_data.dat")
OUT = ROOT / "artifacts" / "vehicle_camera_audit"
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ANGLES_FROM_W = (180, -135, -90, -45, 0, 45, 90, 135)


@dataclass(frozen=True)
class Vehicle:
    resource_id: int
    name: str
    frame: tuple[int, int]


VEHICLES = (
    Vehicle(132, "DEVASTATOR", (152, 192)),
    Vehicle(134, "DEVIATOR", (128, 128)),
    Vehicle(137, "HARVESTER", (320, 208)),
    Vehicle(139, "LAUNCHER", (128, 128)),
    Vehicle(141, "MCV", (192, 200)),
    Vehicle(145, "QUAD", (128, 128)),
    Vehicle(147, "RAIDER", (112, 104)),
    Vehicle(151, "SIEGE_BASE", (144, 152)),
    Vehicle(153, "SIEGE_TOP", (144, 152)),
    Vehicle(157, "SONIC_TANK", (128, 128)),
    Vehicle(159, "TANK_BASE", (128, 128)),
    Vehicle(161, "TANK_TOP", (128, 128)),
    Vehicle(162, "TRIKE", (112, 104)),
)


def frames(atlas: Image.Image, vehicle: Vehicle) -> list[Image.Image]:
    width, height = vehicle.frame
    if atlas.width != width * 8 or atlas.height < height:
        raise AssertionError(
            f"{vehicle.name}: atlas {atlas.size} does not match frame {vehicle.frame}"
        )
    return [atlas.crop((index * width, 0, (index + 1) * width, height)) for index in range(8)]


def alpha_iou(left: Image.Image, right: Image.Image) -> float:
    a = np.array(left.getchannel("A")) > 24
    b = np.array(right.getchannel("A")) > 24
    union = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / union) if union else 0.0


def appearance_similarity(left: Image.Image, right: Image.Image) -> float:
    a = np.array(left.convert("RGBA"), dtype=np.float32)
    b = np.array(right.convert("RGBA"), dtype=np.float32)
    mask = np.logical_or(a[:, :, 3] > 24, b[:, :, 3] > 24)
    if not mask.any():
        return 0.0
    difference = np.abs(a[:, :, :3] - b[:, :, :3]).mean(axis=2)
    return float(1.0 - np.clip(difference[mask].mean() / 255.0, 0.0, 1.0))


def flat_rotation_score(images: list[Image.Image]) -> tuple[float, float]:
    west = images[4]
    alpha_scores: list[float] = []
    appearance_scores: list[float] = []
    for image, angle in zip(images, ANGLES_FROM_W):
        rotated = west.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
        alpha_scores.append(alpha_iou(image, rotated))
        appearance_scores.append(appearance_similarity(image, rotated))
    return float(np.mean(alpha_scores)), float(np.mean(appearance_scores))


def contact_sheet(items: list[tuple[Vehicle, list[Image.Image], str]]) -> Image.Image:
    cell = 150
    label_width = 190
    row_height = cell + 24
    output = Image.new("RGB", (label_width + cell * 8, row_height * len(items)), (18, 20, 23))
    draw = ImageDraw.Draw(output)
    for row, (vehicle, images, verdict) in enumerate(items):
        y = row * row_height
        color = (225, 95, 80) if verdict == "FLAT_ROTATION" else (130, 210, 145)
        draw.text((8, y + 12), f"{vehicle.resource_id} {vehicle.name}", fill=(235, 225, 190))
        draw.text((8, y + 34), verdict, fill=color)
        for index, image in enumerate(images):
            backdrop = Image.new("RGBA", image.size, (43, 46, 51, 255))
            backdrop.alpha_composite(image)
            fitted = backdrop.convert("RGB")
            fitted.thumbnail((cell - 8, cell - 8), Image.Resampling.LANCZOS)
            x = label_width + index * cell
            output.paste(fitted, (x + (cell - fitted.width) // 2, y + (cell - fitted.height) // 2))
            draw.text((x + 6, y + cell + 4), DIRECTIONS[index], fill=(226, 204, 137))
    return output


def comparison_sheet(
    items: list[tuple[Vehicle, list[Image.Image], list[Image.Image]]],
) -> Image.Image:
    cell = 120
    label_width = 190
    row_height = cell + 22
    output = Image.new(
        "RGB",
        (label_width + cell * 8, row_height * len(items) * 2),
        (18, 20, 23),
    )
    draw = ImageDraw.Draw(output)
    for asset_row, (vehicle, classic, hd) in enumerate(items):
        for subrow, (label, images) in enumerate(
            (("CLASSIC", classic), ("HD4", hd))
        ):
            row = asset_row * 2 + subrow
            y = row * row_height
            draw.text((8, y + 10), f"{vehicle.resource_id} {vehicle.name}", fill=(235, 225, 190))
            draw.text((8, y + 32), label, fill=(130, 190, 225))
            for index, image in enumerate(images):
                backdrop = Image.new("RGBA", image.size, (43, 46, 51, 255))
                backdrop.alpha_composite(image)
                fitted = backdrop.convert("RGB")
                fitted.thumbnail((cell - 8, cell - 8), Image.Resampling.LANCZOS)
                x = label_width + index * cell
                output.paste(
                    fitted,
                    (x + (cell - fitted.width) // 2, y + (cell - fitted.height) // 2),
                )
                draw.text((x + 6, y + cell + 2), DIRECTIONS[index], fill=(226, 204, 137))
    return output


def main() -> int:
    entries = read_pack(GAME_PACK)
    classic_entries = read_pack(CLASSIC_PACK)
    results: list[dict[str, object]] = []
    sheet_items: list[tuple[Vehicle, list[Image.Image], str]] = []
    comparison_items: list[tuple[Vehicle, list[Image.Image], list[Image.Image]]] = []
    suspects: list[str] = []
    for vehicle in VEHICLES:
        image = decode_image(entries[vehicle.resource_id].payload)
        if image is None:
            raise AssertionError(f"cannot decode {vehicle.name}")
        directions = frames(image.convert("RGBA"), vehicle)
        classic_image = decode_image(classic_entries[vehicle.resource_id].payload)
        if classic_image is None:
            raise AssertionError(f"cannot decode classic {vehicle.name}")
        classic_vehicle = Vehicle(
            vehicle.resource_id,
            vehicle.name,
            (vehicle.frame[0] // 4, vehicle.frame[1] // 4),
        )
        classic_directions = frames(classic_image.convert("RGBA"), classic_vehicle)
        alpha_score, appearance_score = flat_rotation_score(directions)
        verdict = (
            "FLAT_ROTATION"
            if alpha_score >= 0.86 and appearance_score >= 0.84
            else "OBLIQUE_OR_DRAWN"
        )
        if verdict == "FLAT_ROTATION":
            suspects.append(vehicle.name)
        results.append(
            {
                "id": vehicle.resource_id,
                "name": vehicle.name,
                "frame": list(vehicle.frame),
                "alpha_rotation_score": round(alpha_score, 4),
                "appearance_rotation_score": round(appearance_score, 4),
                "verdict": verdict,
            }
        )
        sheet_items.append((vehicle, directions, verdict))
        comparison_items.append((vehicle, classic_directions, directions))

    OUT.mkdir(parents=True, exist_ok=True)
    contact_sheet(sheet_items).save(OUT / "vehicle_contact_sheet.png", optimize=True)
    comparison_sheet(comparison_items).save(
        OUT / "classic_hd_comparison.png",
        optimize=True,
    )
    report = {"suspects": suspects, "vehicles": results}
    (OUT / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 1 if suspects else 0


if __name__ == "__main__":
    raise SystemExit(main())
