#!/usr/bin/env python3
"""Validate the complete Battle for Arrakis HD world replacement."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


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

BUILDING_IDS = (1, 3, 5, 8, 10, 12, 15, 26, 28, 30, 32, 34, 36, 38, 40, 42)
UNIT_IDS = (
    130,
    132,
    134,
    135,
    137,
    139,
    141,
    143,
    145,
    147,
    149,
    150,
    151,
    153,
    154,
    155,
    156,
    157,
    159,
    161,
    162,
    164,
    165,
    166,
)
INFANTRY_IDS = (149, 154, 155, 156, 164, 165, 166)
VARIANT_NAMES = {
    130: "UNIT_CARRYALL",
    132: "UNIT_DEVASTATOR",
    134: "UNIT_DEVIATOR",
    135: "UNIT_FRIGATE",
    137: "UNIT_HARVESTER",
    139: "UNIT_LAUNCHER",
    141: "UNIT_MCV",
    143: "UNIT_ORNITHOPTER",
    145: "UNIT_QUAD",
    147: "UNIT_RAIDER",
    149: "UNIT_SABOTEUR",
    151: "UNIT_SIEGEBASE",
    153: "UNIT_SIEGETOP",
    154: "UNIT_SINGLEFREMEN",
    155: "UNIT_SOLDIER",
    156: "UNIT_SOLDIERS",
    157: "UNIT_SONICTANK",
    159: "UNIT_TANKBASE",
    161: "UNIT_TANKTOP",
    162: "UNIT_TRIKE",
    164: "UNIT_TRIPLEFREMEN",
    165: "UNIT_TROOPER",
    166: "UNIT_TROOPERS",
}


def classic(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def master(resource_id: int) -> Path:
    return MASTER / classic(resource_id).name


def assert_source_manifest() -> None:
    manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["release"] == "v0.8.0-ru4-preview4"
    assert len(manifest["files"]) == 15
    for entry in manifest["files"]:
        path = SOURCE / entry["file"]
        assert path.is_file(), path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
        assert "duneiithebattleforarrakis/asset/" in entry["page_url"]


def assert_master_sizes() -> None:
    for resource_id in (*BUILDING_IDS, *UNIT_IDS):
        source_image = Image.open(classic(resource_id))
        hd = Image.open(master(resource_id)).convert("RGBA")
        assert hd.size == (
            source_image.width * 4,
            source_image.height * 4,
        ), (resource_id, source_image.size, hd.size)
        assert hd.getchannel("A").getbbox(), resource_id


def assert_directional_rows() -> None:
    for resource_id in (130, 132, 134, 135, 137, 139, 141, 143, 145, 147, 151, 157, 159, 162):
        classic_image = Image.open(classic(resource_id))
        hd = Image.open(master(resource_id)).convert("RGBA")
        frame_width = classic_image.width // 8 * 4
        frame_height = (
            32 * 4
            if resource_id in INFANTRY_IDS
            else hd.height
        )
        frames = [
            hd.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height))
            for index in range(8)
        ]
        distinct = 1
        for frame in frames[1:]:
            if ImageChops.difference(frames[0], frame).getbbox():
                distinct += 1
        assert distinct >= 6, (resource_id, distinct)


def assert_infantry_scale() -> None:
    for resource_id in INFANTRY_IDS:
        image = Image.open(master(resource_id)).convert("RGBA")
        frame = image.crop((0, 0, 128, 128))
        bounds = frame.getchannel("A").getbbox()
        assert bounds
        logical_height = (bounds[3] - bounds[1]) / 4
        maximum = 15 if resource_id in (156, 164, 166) else 9
        assert logical_height <= maximum, (resource_id, logical_height)

    for resource_id in (132, 137, 139, 145, 159):
        image = Image.open(master(resource_id)).convert("RGBA")
        classic_image = Image.open(classic(resource_id))
        frame_width = classic_image.width // 8 * 4
        frame_height = image.height // max(1, classic_image.height // (classic_image.height if resource_id not in (137,) else 52))
        frame = image.crop((0, 0, frame_width, min(image.height, max(128, frame_height))))
        bounds = frame.getchannel("A").getbbox()
        assert bounds
        assert (bounds[3] - bounds[1]) / 4 >= 20, resource_id


def assert_house_variants() -> None:
    for resource_id, name in VARIANT_NAMES.items():
        base = Image.open(master(resource_id))
        for code in ("A", "H", "O"):
            variant = EXTRA / f"HV_{code}_{name}.png"
            assert variant.is_file(), variant
            assert Image.open(variant).size == base.size, variant


def main() -> None:
    assert_source_manifest()
    assert_master_sizes()
    assert_directional_rows()
    assert_infantry_scale()
    assert_house_variants()
    print(
        "Battle for Arrakis world valid: 15 source sheets, "
        "16 structures, all D2TM unit families and 3 House palettes"
    )


if __name__ == "__main__":
    main()
