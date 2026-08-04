#!/usr/bin/env python3
"""Validate card IDs, Russian terminology, dimensions and label wrapping."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageFont


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    root = parse_args().repo.resolve()
    catalog = json.loads(
        (root / "resources/hd/CARD_NAMES_RU.json").read_text(encoding="utf-8")
    )
    cards = catalog["cards"]
    expected_ids = list(range(29, 72))
    actual_ids = [card["id"] for card in cards]
    if actual_ids != expected_ids:
        raise ValueError(f"card IDs changed: {actual_ids}")

    header = (root / "src/data/gfxinter.h").read_text(encoding="utf-8")
    defines = {
        symbol: int(entry_id)
        for symbol, entry_id in re.findall(
            r"(?m)^#define\s+(ICON_(?:SPECIAL|STR|UNIT)_[A-Z0-9_]+)"
            r"\s+(\d+)",
            header,
        )
    }
    for card in cards:
        if defines.get(card["symbol"]) != card["id"]:
            raise ValueError(
                f"{card['symbol']} maps to {defines.get(card['symbol'])}, "
                f"expected {card['id']}"
            )

    status = json.loads(
        (root / "resources/hd/card_master_status.json").read_text(
            encoding="utf-8"
        )
    )
    if len(status["approved_ai_masters"]) != 43:
        raise ValueError("not all 43 cards are approved artistic masters")
    if status["clean_fallback_masters"]:
        raise ValueError("fallback card masters remain")

    master_dir = root / "resources/hd/master4/sdl_inter"
    for card in cards:
        matches = sorted(master_dir.glob(f"{card['id']:04d}_*.png"))
        if len(matches) != 1:
            raise ValueError(f"ID {card['id']} has {len(matches)} masters")
        with Image.open(matches[0]) as image:
            if image.size != (256, 192):
                raise ValueError(f"{matches[0]} has size {image.size}")

    font = ImageFont.truetype(
        str(root / "resources/bin/data/PTSansNarrow-Regular.ttf"),
        12,
    )
    narrow_text_width = 99
    for card in cards:
        words = card["name"].split()
        lines = [""]
        for word in words:
            candidate = f"{lines[-1]} {word}".strip()
            if font.getlength(candidate) <= narrow_text_width:
                lines[-1] = candidate
            elif len(lines) == 1:
                lines.append(word)
            else:
                lines[-1] = candidate
        if len(lines) > 2 or any(
            font.getlength(line) > narrow_text_width for line in lines
        ):
            raise ValueError(
                f"card {card['id']} label does not fit two lines: {lines}"
            )

    source = (root / "src/utils/cIniGameRessouces.cpp").read_text(
        encoding="utf-8"
    )
    required = [
        "Мобильный стройкомплекс",
        "Гранатомётчик",
        "Отряд гранатомётчиков",
        "Бетонные плиты 2×2",
        "Высокотехнологичный завод",
        "Казармы ВОР",
        "Центр Икс",
    ]
    forbidden = [
        "Мобильная база",
        "Штурмовики",
        "4 бетонные плиты",
        '"Хай-тек"',
        '"ВОР"',
        '"Дом Икс"',
        "Ракетница",
    ]
    for term in required:
        if term not in source:
            raise ValueError(f"required terminology missing: {term}")
    for term in forbidden:
        if term in source:
            raise ValueError(f"obsolete terminology remains: {term}")

    print("HD_CARD_CATALOG_OK")
    print("- IDs 29-71 match gfxinter.h")
    print("- 43 artistic masters at 256x192; no fallbacks")
    print("- all Russian labels fit two lines at the narrow HD layout")
    print("- obsolete unit/building names are absent")


if __name__ == "__main__":
    main()
