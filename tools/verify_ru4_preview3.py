#!/usr/bin/env python3
"""Validate preview3 infantry, buildings, restored terrain and menu path."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
SOURCE = ROOT / "resources" / "hd" / "source_references" / "preview3"
FRAME_SIZE = 128

INFANTRY = {
    155: ("UNIT_SOLDIER", False),
    156: ("UNIT_SOLDIERS", True),
    165: ("UNIT_TROOPER", False),
    166: ("UNIT_TROOPERS", True),
}
MASKED_VEHICLES = {
    "UNIT_CARRYALL": 130,
    "UNIT_DEVASTATOR": 132,
    "UNIT_DEVIATOR": 134,
    "UNIT_HARVESTER": 137,
    "UNIT_LAUNCHER": 139,
    "UNIT_MCV": 141,
    "UNIT_ORNITHOPTER": 143,
    "UNIT_QUAD": 145,
    "UNIT_RAIDER": 147,
    "UNIT_SIEGEBASE": 151,
    "UNIT_SIEGETOP": 153,
    "UNIT_SONICTANK": 157,
    "UNIT_TRIKE": 162,
}
BUILDINGS = {
    1: ("BUILD_BARRACKS", (64, 64), 1),
    3: ("BUILD_CONSTYARD", (64, 64), 1),
    5: ("BUILD_HEAVYFACTORY", (96, 64), 11),
    8: ("BUILD_HIGHTECH", (96, 64), 7),
    10: ("BUILD_IX", (64, 64), 1),
    12: ("BUILD_LIGHTFACTORY", (64, 64), 1),
    15: ("BUILD_PALACE", (96, 96), 1),
    26: ("BUILD_RADAR", (64, 64), 8),
    28: ("BUILD_REFINERY", (96, 64), 8),
    30: ("BUILD_REPAIR", (96, 64), 8),
    32: ("BUILD_RTURRET", (32, 32), 8),
    34: ("BUILD_SILO", (64, 64), 1),
    36: ("BUILD_STARPORT", (96, 96), 8),
    38: ("BUILD_TURRET", (32, 32), 8),
    40: ("BUILD_WINDTRAP", (64, 64), 1),
    42: ("BUILD_WOR", (64, 64), 1),
}
SHADOW_IDS = (2, 4, 7, 9, 11, 14, 16, 27, 29, 31, 33, 35, 37, 39, 41, 43)
TERRAIN_IDS = tuple(range(117, 126))
TERRAIN_VARIANTS = {
    118: "TERRAIN_HILL",
    119: "TERRAIN_MOUNTAIN",
    120: "TERRAIN_ROCK",
    121: "TERRAIN_SAND",
    123: "TERRAIN_SPICE",
    124: "TERRAIN_SPICEHILL",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resource(folder: Path, resource_id: int) -> Path:
    return next(folder.glob(f"{resource_id:04d}_*.png"))


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.convert("RGBA").getchannel("A").getbbox()
    if bounds is None:
        raise AssertionError("transparent frame")
    return bounds


def verify_sources() -> None:
    source_manifest = json.loads(
        (SOURCE / "manifest.json").read_text(encoding="utf-8")
    )
    expected = {
        "commando_enemy_soldiers_281892.png": (
            (761, 387),
            "fbf0fb089333fe46ba3a879545a67e75"
            "aa8a6fd9f5284086c69443961bbee0cf",
        ),
        "battle_for_arrakis_buildings_239094.png": (
            (512, 352),
            "3f73042e24d2211011e44da22aa6da1c0"
            "24b8ba29203208fbf03a70184dad7ba",
        ),
    }
    recorded_names = {entry["file"] for entry in source_manifest["sources"]}
    if recorded_names != set(expected):
        raise AssertionError("preview3 source manifest changed")
    for name, (size, digest) in expected.items():
        path = SOURCE / name
        if Image.open(path).size != size:
            raise AssertionError(f"{name}: unexpected dimensions")
        if sha256(path) != digest:
            raise AssertionError(f"{name}: checksum changed")


def verify_infantry() -> None:
    manifest = json.loads(
        (SOURCE / "commando_infantry_manifest.json").read_text(encoding="utf-8")
    )
    if manifest["direction_order"] != ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]:
        raise AssertionError("infantry direction order changed")

    opaque_areas: dict[int, int] = {}
    for resource_id, (name, is_group) in INFANTRY.items():
        atlas = Image.open(resource(MASTER, resource_id)).convert("RGBA")
        mask = Image.open(EXTRA / f"HOUSEMASK_{name}.png").convert("RGBA")
        if atlas.size != (1024, 512) or mask.size != atlas.size:
            raise AssertionError(f"{name}: expected an 8x4 atlas of 128px frames")
        if mask.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name}: empty House mask")
        body_pixels = sum(
            value > 24 for value in atlas.getchannel("A").get_flattened_data()
        )
        mask_alpha = mask.getchannel("A")
        masked_pixels = sum(
            value > 12 for value in mask_alpha.get_flattened_data()
        )
        if masked_pixels / max(1, body_pixels) > 0.18:
            raise AssertionError(f"{name}: House colour covers too much of the body")
        if mask_alpha.getextrema()[1] > 128:
            raise AssertionError(f"{name}: House colour is too saturated")

        area = 0
        first_row: list[Image.Image] = []
        for animation in range(4):
            for direction in range(8):
                frame = atlas.crop(
                    (
                        direction * FRAME_SIZE,
                        animation * FRAME_SIZE,
                        (direction + 1) * FRAME_SIZE,
                        (animation + 1) * FRAME_SIZE,
                    )
                )
                bounds = alpha_bounds(frame)
                height = bounds[3] - bounds[1]
                if is_group:
                    if not 48 <= height <= 70:
                        raise AssertionError(f"{name}: group height {height}")
                elif not 26 <= height <= 42:
                    raise AssertionError(f"{name}: single height {height}")
                area += sum(value > 24 for value in frame.getchannel("A").get_flattened_data())
                if animation == 0:
                    first_row.append(frame)

        for direction, frame in enumerate(first_row):
            opposite = first_row[(8 - direction) % 8].transpose(
                Image.Transpose.FLIP_LEFT_RIGHT
            )
            if ImageChops.difference(frame, opposite).getbbox() is None:
                raise AssertionError(
                    f"{name}: direction {direction} is a mirrored duplicate"
                )
        opaque_areas[resource_id] = area

    for single, squad in ((155, 156), (165, 166)):
        ratio = opaque_areas[squad] / opaque_areas[single]
        if not 2.0 <= ratio <= 3.4:
            raise AssertionError(f"infantry squad/single area ratio {ratio:.2f}")


def verify_vehicle_house_masks() -> None:
    for name, resource_id in MASKED_VEHICLES.items():
        unit = Image.open(resource(MASTER, resource_id)).convert("RGBA")
        mask = Image.open(EXTRA / f"HOUSEMASK_{name}.png").convert("RGBA")
        if unit.size != mask.size:
            raise AssertionError(f"{name}: House mask size changed")
        opaque = sum(
            value > 24 for value in unit.getchannel("A").get_flattened_data()
        )
        mask_alpha = mask.getchannel("A")
        coloured = sum(
            value > 48 for value in mask_alpha.get_flattened_data()
        )
        if coloured / max(1, opaque) > 0.16:
            raise AssertionError(f"{name}: House colour panel is too broad")
        if mask_alpha.getextrema()[1] > 110:
            raise AssertionError(f"{name}: House colour is too saturated")


def verify_buildings() -> None:
    generated_manifest = json.loads(
        (
            ROOT
            / "resources"
            / "hd"
            / "generated"
            / "preview3"
            / "buildings"
            / "manifest.json"
        ).read_text(encoding="utf-8")
    )
    if len(generated_manifest["buildings"]) != len(BUILDINGS):
        raise AssertionError("not all 16 Sega/ImageGen buildings were produced")

    for resource_id, (name, frame_size, frame_count) in BUILDINGS.items():
        classic = Image.open(resource(CLASSIC, resource_id))
        master = Image.open(resource(MASTER, resource_id)).convert("RGBA")
        expected_size = (classic.width * 4, classic.height * 4)
        if master.size != expected_size:
            raise AssertionError(f"{name}: {master.size}, expected {expected_size}")

        frame_height = frame_size[1] * 4
        if master.size != (frame_size[0] * 4, frame_height * frame_count):
            raise AssertionError(f"{name}: frame count or frame size changed")
        for frame_index in range(frame_count):
            frame = master.crop(
                (0, frame_index * frame_height, master.width, (frame_index + 1) * frame_height)
            )
            bounds = alpha_bounds(frame)
            if bounds[3] != frame_height - 8:
                raise AssertionError(f"{name}: bottom anchor changed in frame {frame_index}")

        transparent_mask = Image.open(EXTRA / f"HOUSEMASK_{name}.png").convert("RGBA")
        if transparent_mask.size != master.size or transparent_mask.getchannel("A").getbbox():
            raise AssertionError(f"{name}: neutral building has a coloured body mask")
        for house in ("A", "H", "O"):
            variant = Image.open(EXTRA / f"HV_{house}_{name}.png").convert("RGBA")
            if ImageChops.difference(master, variant).getbbox():
                raise AssertionError(f"{name}: House {house} body is not neutral")

    for resource_id in SHADOW_IDS:
        shadow = Image.open(resource(MASTER, resource_id)).convert("RGBA")
        if shadow.getchannel("A").getbbox() is None:
            raise AssertionError(f"building shadow ID {resource_id} is empty")
    for resource_id in range(1, 46):
        image = Image.open(resource(MASTER, resource_id))
        classic = Image.open(resource(CLASSIC, resource_id))
        if image.size != (classic.width * 4, classic.height * 4):
            raise AssertionError(f"building auxiliary ID {resource_id}: size changed")


def verify_terrain() -> None:
    for resource_id in TERRAIN_IDS:
        master = Image.open(resource(MASTER, resource_id)).convert("RGBA")
        classic = Image.open(resource(CLASSIC, resource_id))
        if master.size != (classic.width * 4, classic.height * 4):
            raise AssertionError(f"terrain ID {resource_id}: wrong HD4 size")

    for resource_id in (120, 121, 123):
        master = Image.open(resource(MASTER, resource_id)).convert("RGB")
        frame = master.crop((0, 0, FRAME_SIZE, FRAME_SIZE))
        low_detail = frame.resize((32, 32), Image.Resampling.LANCZOS).resize(
            frame.size, Image.Resampling.LANCZOS
        )
        detail_rms = sum(
            ImageStat.Stat(ImageChops.difference(frame, low_detail)).rms
        ) / 3.0
        # The calmer preview3 material deliberately avoids the noisy surface
        # that shimmered at high resolution, while still carrying sub-tile
        # detail unavailable in a 32 px roundtrip.
        if detail_rms < 3.25:
            raise AssertionError(
                f"terrain ID {resource_id}: HD4 lacks real surface detail "
                f"({detail_rms:.2f})"
            )
        pixels = frame.load()
        horizontal = sum(
            sum(abs(pixels[0, y][c] - pixels[frame.width - 1, y][c]) for c in range(3))
            for y in range(frame.height)
        ) / (frame.height * 3)
        vertical = sum(
            sum(abs(pixels[x, 0][c] - pixels[x, frame.height - 1][c]) for c in range(3))
            for x in range(frame.width)
        ) / (frame.width * 3)
        if max(horizontal, vertical) > 2.0:
            raise AssertionError(
                f"terrain ID {resource_id}: tile edges do not match "
                f"({horizontal:.2f}/{vertical:.2f})"
            )

    for resource_id in (113, 114):
        path = resource(MASTER, resource_id)
        if not path.is_file():
            raise AssertionError(f"shroud ID {resource_id}: no HD4 master")

    guard = 8
    for resource_id, name in TERRAIN_VARIANTS.items():
        base = Image.open(resource(MASTER, resource_id)).convert("RGBA")
        for variant_path in sorted(EXTRA.glob(f"{name}_VAR_*.png")):
            variant = Image.open(variant_path).convert("RGBA")
            if variant.size != base.size:
                raise AssertionError(f"{variant_path.name}: size changed")
            edge_mask = Image.new("L", base.size, 255)
            edge_mask.paste(
                0,
                (guard, guard, base.width - guard, base.height - guard),
            )
            if (
                ImageChops.difference(
                    base.convert("RGB"),
                    variant.convert("RGB"),
                ).getbbox()
                is None
            ):
                raise AssertionError(f"{variant_path.name}: variant is identical")
            edge_difference = ImageChops.difference(base, variant)
            if edge_difference.getbbox() and edge_difference.getchannel("A").getbbox():
                raise AssertionError(f"{variant_path.name}: alpha edge changed")
            rgb_difference = ImageChops.difference(
                base.convert("RGB"), variant.convert("RGB")
            )
            if ImageChops.multiply(rgb_difference, edge_mask.convert("RGB")).getbbox():
                raise AssertionError(f"{variant_path.name}: protected edge changed")


def verify_house_beacons() -> None:
    for house in ("ATREIDES", "HARKONNEN", "ORDOS"):
        path = EXTRA / f"HOUSE_BEACON_{house}.png"
        if not path.is_file():
            raise AssertionError(f"missing HD House beacon: {house}")
        image = Image.open(path).convert("RGBA")
        if image.size != (18 * 8 * 4, 18 * 4):
            raise AssertionError(f"{path.name}: wrong 8-frame HD4 atlas size")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{path.name}: transparent beacon atlas")

    drawer = (ROOT / "src" / "drawers" / "cStructureDrawer.cpp").read_text(
        encoding="utf-8"
    )
    if "drawHdHouseFlag" in drawer or "drawHdHouseBeacon" not in drawer:
        raise AssertionError("HD building flags were not replaced by beacons")


def verify_presentation_path() -> None:
    game_header = (ROOT / "src" / "cGame.h").read_text(encoding="utf-8")
    game_logic = (ROOT / "src" / "cGame_logic.cpp").read_text(encoding="utf-8")
    for marker in (
        "m_hdPresentationRenderer",
        "m_hdPresentationScreenTexture",
        "m_hdPresentationFadeCaptureActive",
    ):
        if marker not in game_header:
            raise AssertionError(f"missing HD presentation state: {marker}")
    for marker in (
        "SDL_GetRendererOutputSize",
        "SDL_RenderSetLogicalSize",
        "useHdPresentation",
        "shouldUsePhysicalHdPresentation",
        "m_state == GAME_PLAYING",
        "captureCurrentFrameForFade",
    ):
        if marker not in game_logic:
            raise AssertionError(f"missing physical HD presentation path: {marker}")


def main() -> int:
    verify_sources()
    verify_infantry()
    verify_vehicle_house_masks()
    verify_buildings()
    verify_terrain()
    verify_house_beacons()
    verify_presentation_path()
    print(
        "ru4-preview3 assets valid: Commando infantry, neutral Sega buildings, "
        "true-detail seamless terrain, House beacons and physical-resolution "
        "HD menu/gameplay path"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
