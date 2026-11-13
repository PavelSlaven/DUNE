#!/usr/bin/env python3
"""Verify all building-flag paths for the three playable Houses."""

from __future__ import annotations

import re
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK_DIR = ROOT / "artifacts" / "silo_integration_v1" / "data"
SPECIAL_FLAGS = (
    "BUILD_BARRACKS_FLAG",
    "BUILD_RADAR_FLAG",
    "BUILD_WINDTRAP_FLAG",
    "BUILD_REFINERY_FLAG",
    "BUILD_CONSTYARD_FLAG",
    "BUILD_SILO_FLAG",
)
SPECIAL_STRUCTURES = {
    "BARRACKS",
    "RADAR",
    "WINDTRAP",
    "REFINERY",
    "CONSTYARD",
    "SILO",
}
HOUSE_COLORS = {
    "HARKONNEN": (255, 0, 0),
    "ATREIDES": (0, 90, 255),
    "ORDOS": (0, 255, 0),
}
PALETTE_STARTS = {
    "HARKONNEN": 144,
    "ATREIDES": 160,
    "ORDOS": 176,
}


def verify_source_routing() -> tuple[list[str], list[str]]:
    config = (
        ROOT / "src" / "utils" / "cIniGameRessouces.cpp"
    ).read_text(encoding="utf-8")
    drawer = (
        ROOT / "src" / "drawers" / "cStructureDrawer.cpp"
    ).read_text(encoding="utf-8")
    flagged = set(
        re.findall(
            r"sStructureInfo\[(\w+)\]\.flags\.push_back",
            config,
        )
    )
    for structure in SPECIAL_STRUCTURES:
        function_name = {
            "BARRACKS": "drawHdBarracksFlag",
            "RADAR": "drawHdRadarFlag",
            "WINDTRAP": "drawHdWindTrapFlag",
            "REFINERY": "drawHdRefineryFlag",
            "CONSTYARD": "drawHdConstYardFlag",
            "SILO": "drawHdSiloFlag",
        }[structure]
        if function_name not in drawer:
            raise AssertionError(f"missing HD route for {structure}")
    if "structure->drawFlags();" not in drawer:
        raise AssertionError("generic building-flag fallback is absent")
    generic = flagged - SPECIAL_STRUCTURES
    if not generic:
        raise AssertionError("no structures use the generic flag path")
    return sorted(flagged), sorted(generic)


def apply_engine_tint(
    base: np.ndarray,
    mask: np.ndarray,
    color: tuple[int, int, int],
) -> np.ndarray:
    result = base.astype(np.float32).copy()
    strength = (
        mask[:, :, 3] / 255.0
        * np.max(mask[:, :, :3], axis=2) / 255.0
    )
    luminance = (
        0.299 * result[:, :, 0]
        + 0.587 * result[:, :, 1]
        + 0.114 * result[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        colored = np.minimum(255.0, target * luminance)
        result[:, :, channel] = (
            result[:, :, channel] * (1.0 - strength)
            + colored * strength
        )
    return result


def verify_special_flags(entries) -> dict[str, dict[str, list[float]]]:
    by_name = {entry.name: entry for entry in entries}
    result = {}
    for name in SPECIAL_FLAGS:
        mask_name = "HM_" + name
        if name not in by_name or mask_name not in by_name:
            raise AssertionError(f"missing {name} or {mask_name}")
        base_image = decode_image(by_name[name].payload)
        mask_image = decode_image(by_name[mask_name].payload)
        if base_image is None or mask_image is None:
            raise AssertionError(f"unable to decode {name}")
        if base_image.size != mask_image.size:
            raise AssertionError(f"{name}: mask size mismatch")
        base = np.asarray(base_image.convert("RGBA"), dtype=np.float32)
        mask = np.asarray(mask_image.convert("RGBA"), dtype=np.float32)
        strength = (
            mask[:, :, 3] / 255.0
            * np.max(mask[:, :, :3], axis=2) / 255.0
        )
        selection = (strength > 0.1) & (base[:, :, 3] > 0)
        if int(selection.sum()) < 32:
            raise AssertionError(f"{name}: empty House-color mask")

        means = {}
        for house, color in HOUSE_COLORS.items():
            tinted = apply_engine_tint(base, mask, color)
            mean = tinted[selection, :3].mean(axis=0)
            dominant = {
                "HARKONNEN": 0,
                "ATREIDES": 2,
                "ORDOS": 1,
            }[house]
            if mean[dominant] <= max(
                mean[index] for index in range(3) if index != dominant
            ):
                raise AssertionError(
                    f"{name}: {house} color is not dominant: {mean}"
                )
            means[house] = [round(float(value), 2) for value in mean]
        if len({tuple(value) for value in means.values()}) != 3:
            raise AssertionError(f"{name}: House variants are identical")
        result[name] = means
    return result


def verify_generic_flags(entries) -> dict[str, object]:
    by_name = {entry.name: entry for entry in entries}
    result = {}
    for name in ("BUILDING_FLAG_LARGE", "BUILDING_FLAG_SMALL"):
        entry = by_name.get(name)
        if entry is None:
            raise AssertionError(f"missing generic resource {name}")
        image = Image.open(BytesIO(entry.payload))
        if image.mode != "P" or image.getpalette() is None:
            raise AssertionError(f"{name}: indexed palette was lost")
        pixels = np.asarray(image)
        used_swap_indices = sorted(
            set(int(value) for value in np.unique(pixels))
            & set(range(144, 151))
        )
        if not used_swap_indices:
            raise AssertionError(f"{name}: no House-color pixels")
        palette = np.asarray(image.getpalette(), dtype=np.float32).reshape(
            -1,
            3,
        )
        means = {}
        for house, start in PALETTE_STARTS.items():
            mean = palette[start:start + 7].mean(axis=0)
            dominant = {
                "HARKONNEN": 0,
                "ATREIDES": 2,
                "ORDOS": 1,
            }[house]
            if mean[dominant] <= max(
                mean[index] for index in range(3) if index != dominant
            ):
                raise AssertionError(
                    f"{name}: invalid {house} palette ramp: {mean}"
                )
            means[house] = [round(float(value), 2) for value in mean]
        result[name] = {
            "swap_indices": used_swap_indices,
            "palette_means": means,
        }
    return result


def main() -> int:
    pack_dir = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else DEFAULT_PACK_DIR
    )
    flagged, generic = verify_source_routing()
    print("Flagged structures:", ", ".join(flagged))
    print("Generic flag path:", ", ".join(generic))
    for density in (2, 4):
        entries = read_pack(pack_dir / f"sdl_data_hd{density}.dat")
        special = verify_special_flags(entries)
        generic_flags = verify_generic_flags(entries)
        print(
            f"HD{density}: {len(special)} masked HD flags, "
            f"{len(generic_flags)} generic flag atlases: OK"
        )
    print("Harkonnen/Atreides/Ordos flag colors: OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
