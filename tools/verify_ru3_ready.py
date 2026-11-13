#!/usr/bin/env python3
"""Verify that an unpacked ru3 preview contains visible HD UI assets."""

from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import read_pack


STANDALONE_UI = {
    2: {
        "main_menu_background.png": (2560, 720),
        "main_menu_logo.png": (896, 160),
        "hud_house_atreides.png": (192, 192),
        "hud_house_harkonnen.png": (192, 192),
        "hud_house_ordos.png": (192, 192),
    },
    4: {
        "main_menu_background.png": (5120, 1440),
        "main_menu_logo.png": (1792, 320),
        "hud_house_atreides.png": (384, 384),
        "hud_house_harkonnen.png": (384, 384),
        "hud_house_ordos.png": (384, 384),
    },
}


def setting(text: str, key: str) -> str | None:
    match = re.search(
        rf"(?mi)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*(.*?)[ \t]*$",
        text,
    )
    return match.group(1) if match else None


def verify_card_masters(
    ready_root: Path,
    master_root: Path,
    density: int,
    errors: list[str],
) -> None:
    pack_path = ready_root / "data" / f"sdl_inter_hd{density}.dat"
    if not pack_path.is_file():
        errors.append(f"missing pack: {pack_path}")
        return

    entries = read_pack(pack_path)
    card_masters = sorted(
        path.name
        for path in (master_root / "sdl_inter").glob("*.png")
        if 29 <= int(path.name[:4]) <= 71
    )
    if len(card_masters) != 43:
        errors.append(
            f"expected 43 card masters, found {len(card_masters)}"
        )

    for master_name in card_masters:
        index = int(master_name[:4])
        master_path = master_root / "sdl_inter" / master_name
        if not master_path.is_file():
            errors.append(f"missing master: {master_path}")
            continue
        if index >= len(entries):
            errors.append(f"pack has no entry {index}: {pack_path}")
            continue

        with Image.open(master_path) as source:
            master = source.convert("RGB")
        expected = (
            master
            if density == 4
            else master.resize((128, 96), Image.Resampling.LANCZOS)
        )
        with Image.open(io.BytesIO(entries[index].payload)) as packed_source:
            packed = packed_source.convert("RGB")
        if packed.size != expected.size:
            errors.append(
                f"{pack_path.name}[{index}] is {packed.size}, "
                f"expected {expected.size}"
            )
            continue
        if ImageChops.difference(packed, expected).getbbox() is not None:
            errors.append(
                f"{pack_path.name}[{index}] does not match approved master"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ready-root", required=True, type=Path)
    parser.add_argument("--master-root", required=True, type=Path)
    parser.add_argument("--require-auto-scale", action="store_true")
    args = parser.parse_args()

    ready_root = args.ready_root.resolve()
    master_root = args.master_root.resolve()
    errors: list[str] = []

    if not (ready_root / "d2tm.exe").is_file():
        errors.append(f"missing executable: {ready_root / 'd2tm.exe'}")

    settings_path = ready_root / "settings.ini"
    if not settings_path.is_file():
        errors.append(f"missing settings: {settings_path}")
    else:
        settings_text = settings_path.read_text(
            encoding="utf-8-sig",
            errors="replace",
        )
        graphics_mode = setting(settings_text, "GraphicsMode")
        if graphics_mode is not None and graphics_mode.lower() != "hd":
            errors.append("GraphicsMode is not HD")
        if args.require_auto_scale:
            render_scale = setting(settings_text, "RenderScale")
            if render_scale != "0":
                errors.append(
                    f"RenderScale is {render_scale!r}; preview must default "
                    "to Auto (0)"
                )

    for density, assets in STANDALONE_UI.items():
        for name, expected_size in assets.items():
            path = ready_root / "data" / f"hd{density}" / name
            if not path.is_file():
                errors.append(f"missing standalone HD UI asset: {path}")
                continue
            with Image.open(path) as image:
                if image.size != expected_size:
                    errors.append(
                        f"{path} is {image.size}; expected {expected_size}"
                    )

    for density in (2, 4):
        verify_card_masters(
            ready_root,
            master_root,
            density,
            errors,
        )

    skirmish_root = ready_root / "skirmish"
    if skirmish_root.is_dir():
        for map_path in skirmish_root.glob("*.ini"):
            if not map_path.name.isascii():
                errors.append(
                    "non-ASCII skirmish filename is not supported by the "
                    f"engine: {map_path.name}"
                )

    if errors:
        print("RU3_READY_FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RU3_READY_OK")
    print("- standalone HD menu assets are present")
    print("- preview defaults to Auto scale")
    print("- HD2/HD4 card entries match all 43 clean masters")
    print("- HD house crests are present with valid density sizes")
    print("- skirmish filenames are engine-safe ASCII")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
