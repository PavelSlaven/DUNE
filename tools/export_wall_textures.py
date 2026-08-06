#!/usr/bin/env python3
"""Export the concrete-wall visuals used by the D2TM runtime packs.

This utility is deliberately read-only with respect to game packs and source
assets.  It creates an editing/reference package under ``artifacts``.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from hd_assets import decode_image, read_pack, sha256


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "wall_textures"
DATA = ROOT / "resources" / "bin" / "data"

ASSETS = (
    ("sdl_data", 111, "PLACE_WALL", "Предпросмотр при размещении стены"),
    ("sdl_data", 125, "TERRAIN_WALL", "Игровой атлас сегментов стены"),
    ("sdl_inter", 48, "ICON_STR_WALL", "Значок стены в панели строительства"),
)


def load_asset(pack_stem: str, density: str, index: int):
    suffix = "_hd4" if density == "hd4" else ""
    pack = DATA / f"{pack_stem}{suffix}.dat"
    entry = read_pack(pack)[index]
    image = decode_image(entry.payload)
    if image is None:
        raise ValueError(f"{pack.name}:{index} is not an image")
    return pack, entry, image.convert("RGBA")


def save_png(image: Image.Image, path: Path) -> None:
    image.save(path, "PNG", optimize=True)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(DATA / "PTMono-Regular.ttf"), size)


def label(draw: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    draw.text((x + 2, y + 2), text, font=font(18), fill=(0, 0, 0, 230))
    draw.text((x, y), text, font=font(18), fill=(247, 229, 180, 255))


def make_wall_atlas_sheet(hd4: Image.Image, classic: Image.Image) -> None:
    cell = hd4.height
    width = 4 * (cell + 24)
    height = 4 * (cell + 60) + 140
    sheet = Image.new("RGBA", (width, height), (14, 18, 22, 255))
    draw = ImageDraw.Draw(sheet)
    label(draw, 20, 18, "TERRAIN_WALL — HD4, 16 ячеек 32×32 (в игре используются 0–11)")
    for index in range(16):
        x = 12 + (index % 4) * (cell + 24)
        y = 58 + (index // 4) * (cell + 60)
        tile = hd4.crop((index * cell, 0, (index + 1) * cell, cell))
        sheet.alpha_composite(tile, (x, y))
        label(draw, x, y + cell + 8, f"{index:02d}")

    classic_y = height - 78
    label(draw, 20, classic_y, "Классический атлас: 512×32, те же 16 ячеек по 32×32")
    preview = classic.resize((512, 32), Image.Resampling.NEAREST)
    sheet.alpha_composite(preview, (20 + 360, classic_y))
    save_png(sheet, OUT / "wall_atlas_hd4_contact_sheet.png")


def main() -> int:
    if OUT.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing export directory: {OUT}"
        )
    OUT.mkdir(parents=True)

    records = []
    loaded: dict[tuple[str, str], Image.Image] = {}
    for pack_stem, index, expected_name, purpose in ASSETS:
        for density in ("hd4", "classic"):
            pack, entry, image = load_asset(pack_stem, density, index)
            if entry.name != expected_name:
                raise ValueError(
                    f"Expected {expected_name} at {pack.name}:{index}, got {entry.name}"
                )
            filename = f"{density}_{index:04d}_{entry.name}.png"
            save_png(image, OUT / filename)
            loaded[(density, entry.name)] = image
            records.append(
                {
                    "id": index,
                    "name": entry.name,
                    "purpose_ru": purpose,
                    "density": density,
                    "source_pack": str(pack.resolve()),
                    "source_entry_index": entry.index,
                    "source_entry_extension": entry.extension,
                    "source_payload_sha256": sha256(entry.payload),
                    "size_px": [image.width, image.height],
                    "export": filename,
                }
            )

    atlas_hd4 = loaded[("hd4", "TERRAIN_WALL")]
    atlas_classic = loaded[("classic", "TERRAIN_WALL")]
    if atlas_hd4.size != (2048, 128) or atlas_classic.size != (512, 32):
        raise ValueError("Unexpected concrete-wall atlas dimensions")
    make_wall_atlas_sheet(atlas_hd4, atlas_classic)

    manifest = {
        "format": 1,
        "created": date.today().isoformat(),
        "description_ru": "Полный набор визуальных ресурсов бетонной стены D2TM.",
        "runtime_note_ru": (
            "PLACE_WALL — предпросмотр размещения; TERRAIN_WALL — видимые "
            "на карте сегменты; ICON_STR_WALL — иконка строительства."
        ),
        "terrain_wall": {
            "cell_size_logical_px": [32, 32],
            "atlas_cells": 16,
            "used_cell_indices": list(range(12)),
            "unused_cell_indices": list(range(12, 16)),
        },
        "assets": records,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "README.md").write_text(
        "# Текстуры бетонной стены\n\n"
        "Это экспорт без изменений игровых паков.\n\n"
        "- `hd4_0125_TERRAIN_WALL.png` — основной игровой атлас стены. "
        "Он содержит 16 горизонтальных сегментов; движок использует сегменты 0–11.\n"
        "- `hd4_0111_PLACE_WALL.png` — изображение, показываемое при размещении.\n"
        "- `hd4_0048_ICON_STR_WALL.png` — иконка стены в строительной панели.\n"
        "- Файлы с префиксом `classic_` — исходные 1× версии для сравнения.\n"
        "- `wall_atlas_hd4_contact_sheet.png` — контактный лист всех сегментов.\n\n"
        "Точные источники, ID и размеры записаны в `manifest.json`.\n",
        encoding="utf-8",
    )
    print(f"Wall textures exported to: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
