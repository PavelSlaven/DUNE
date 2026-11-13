#!/usr/bin/env python3
"""Build faithful HD cursor masters from the original D2TM palette sprites.

The classic pixel masks remain authoritative for silhouette and hotspot geometry.
Only the material rendering inside those masks is upgraded.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
CLASSIC_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data.dat"
CURRENT_HD4_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data_hd4.dat"
OUT = ROOT / "artifacts" / "cursor_hd_redraw_v1"
HD4 = OUT / "hd4"
HD2 = OUT / "hd2"

CURSOR_IDS = tuple(range(79, 90))
EXPECTED_NAMES = (
    "MOUSE_ATTACK",
    "MOUSE_DOWN",
    "MOUSE_FORBIDDEN",
    "MOUSE_LEFT",
    "MOUSE_MOVE",
    "MOUSE_NORMAL",
    "MOUSE_PICK",
    "MOUSE_RALLY",
    "MOUSE_REPAIR",
    "MOUSE_RIGHT",
    "MOUSE_UP",
)

# Exact classic palette colours mapped to restrained remaster materials.
MATERIALS: dict[tuple[int, int, int], tuple[tuple[int, int, int], tuple[int, int, int]]] = {
    (255, 255, 255): ((255, 255, 255), (224, 226, 236)),
    (123, 125, 156): ((154, 157, 188), (101, 103, 135)),
    (65, 64, 65): ((79, 79, 90), (39, 39, 49)),
    (64, 64, 64): ((82, 82, 91), (38, 38, 47)),
    (49, 48, 82): ((65, 65, 105), (27, 26, 58)),
    (255, 0, 0): ((255, 54, 48), (205, 0, 12)),
    (131, 0, 0): ((151, 8, 13), (73, 0, 8)),
}


def safe_name(name: str) -> str:
    return name.lower().replace("mouse_", "")


def smooth_region_mask(source: Image.Image, colour: tuple[int, int, int], scale: int) -> Image.Image:
    rgba = np.asarray(source.convert("RGBA"))
    region = np.all(rgba[:, :, :3] == colour, axis=2) & (rgba[:, :, 3] > 0)
    logical = Image.fromarray(np.where(region, 255, 0).astype(np.uint8), "L")

    # Work at 4x the requested master size. A very small rounding pass removes
    # block stair-steps but retains the exact classic pixel topology.
    work_size = (source.width * scale * 4, source.height * scale * 4)
    work = logical.resize(work_size, Image.Resampling.NEAREST)
    work = work.filter(ImageFilter.GaussianBlur(radius=1.35))
    return work.resize((source.width * scale, source.height * scale), Image.Resampling.LANCZOS)


def gradient_layer(
    size: tuple[int, int],
    top_left: tuple[int, int, int],
    bottom_right: tuple[int, int, int],
) -> Image.Image:
    width, height = size
    yy, xx = np.mgrid[0:height, 0:width]
    denominator = max(1, width + height - 2)
    t = ((xx + yy) / denominator).astype(np.float32)
    start = np.asarray(top_left, dtype=np.float32)
    end = np.asarray(bottom_right, dtype=np.float32)
    rgb = start[None, None, :] * (1.0 - t[:, :, None]) + end[None, None, :] * t[:, :, None]
    alpha = np.full((height, width, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate((np.clip(rgb, 0, 255).astype(np.uint8), alpha), axis=2), "RGBA")


def add_inner_highlight(layer: Image.Image, mask: Image.Image, strength: int) -> None:
    eroded = mask.filter(ImageFilter.MinFilter(5))
    edge = ImageChops.subtract(mask, eroded)
    width, height = mask.size
    yy, xx = np.mgrid[0:height, 0:width]
    fade = np.clip(1.15 - (xx / max(1, width - 1) + yy / max(1, height - 1)), 0.0, 1.0)
    edge_array = np.asarray(edge, dtype=np.float32) * fade * (strength / 255.0)
    highlight = Image.new("RGBA", mask.size, (255, 255, 255, 0))
    highlight.putalpha(Image.fromarray(np.clip(edge_array, 0, 255).astype(np.uint8), "L"))
    layer.alpha_composite(highlight)


def remaster(source: Image.Image, scale: int = 4) -> Image.Image:
    source = source.convert("RGBA")
    target_size = (source.width * scale, source.height * scale)
    result = Image.new("RGBA", target_size, (0, 0, 0, 0))
    colours = Counter(
        (r, g, b)
        for r, g, b, a in source.getdata()
        if a > 0
    )

    for colour, _count in colours.most_common():
        if colour not in MATERIALS:
            raise ValueError(f"unsupported classic cursor colour {colour}")
        mask = smooth_region_mask(source, colour, scale)
        material = gradient_layer(target_size, *MATERIALS[colour])
        material.putalpha(mask)
        add_inner_highlight(material, mask, 72 if colour in {(255, 255, 255), (255, 0, 0)} else 38)
        result.alpha_composite(material)

    # Do not let antialiasing move a cursor past the classic occupied bounds.
    source_bbox = source.getchannel("A").getbbox()
    if source_bbox is None:
        raise ValueError("empty cursor")
    exact_bbox = tuple(value * scale for value in source_bbox)
    clipped = Image.new("RGBA", target_size, (0, 0, 0, 0))
    clipped.alpha_composite(result.crop(exact_bbox), (exact_bbox[0], exact_bbox[1]))
    return clipped


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (31, 35, 39, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(42, 47, 52, 255))
    return image


def place_preview(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    background = checker((x2 - x1, y2 - y1), 12)
    preview = image.copy()
    preview.thumbnail((x2 - x1 - 24, y2 - y1 - 24), Image.Resampling.LANCZOS)
    background.alpha_composite(preview, ((background.width - preview.width) // 2, (background.height - preview.height) // 2))
    canvas.alpha_composite(background, (x1, y1))


def build_comparison(records: list[dict[str, object]], classic: list, current: list) -> None:
    card_width, card_height = 1170, 250
    sheet = Image.new("RGBA", (card_width, card_height * len(records) + 70), (9, 12, 15, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((24, 22), "D2TM CURSORS: CLASSIC / CURRENT LANCZOS / FAITHFUL HD", fill=(224, 184, 91, 255), font=font)
    for row, record in enumerate(records):
        y = 70 + row * card_height
        draw.rectangle((12, y + 4, card_width - 12, y + card_height - 8), outline=(94, 76, 43, 255), width=1)
        draw.text((28, y + 20), f"#{record['id']}  {record['name']}", fill=(232, 226, 203, 255), font=font)
        draw.text((28, y + 46), "CLASSIC x8", fill=(160, 168, 175, 255), font=font)
        draw.text((394, y + 46), "CURRENT HD4", fill=(160, 168, 175, 255), font=font)
        draw.text((760, y + 46), "NEW HD4", fill=(224, 184, 91, 255), font=font)
        source = decode_image(classic[record["id"]].payload).convert("RGBA")
        old_hd = decode_image(current[record["id"]].payload).convert("RGBA")
        new_hd = Image.open(HD4 / record["file"]).convert("RGBA")
        place_preview(sheet, source.resize((source.width * 8, source.height * 8), Image.Resampling.NEAREST), (28, y + 68, 370, y + 228))
        place_preview(sheet, old_hd, (394, y + 68, 736, y + 228))
        place_preview(sheet, new_hd, (760, y + 68, 1102, y + 228))
    sheet.save(OUT / "comparison_classic_current_new.png", optimize=True)


def main() -> int:
    HD4.mkdir(parents=True, exist_ok=True)
    HD2.mkdir(parents=True, exist_ok=True)
    classic = read_pack(CLASSIC_PACK)
    current = read_pack(CURRENT_HD4_PACK)
    records: list[dict[str, object]] = []

    for offset, index in enumerate(CURSOR_IDS):
        entry = classic[index]
        expected_name = EXPECTED_NAMES[offset]
        if entry.name != expected_name or current[index].name != expected_name:
            raise ValueError(f"cursor contract mismatch at {index}")
        source = decode_image(entry.payload)
        current_image = decode_image(current[index].payload)
        if source is None or current_image is None:
            raise ValueError(f"cursor {expected_name} is not an image")
        master = remaster(source, 4)
        expected_size = (source.width * 4, source.height * 4)
        if master.size != expected_size:
            raise AssertionError(f"{expected_name}: wrong HD4 size")
        file_name = f"{index:04d}_{safe_name(expected_name)}.png"
        master.save(HD4 / file_name, optimize=True)
        master.resize((source.width * 2, source.height * 2), Image.Resampling.LANCZOS).save(HD2 / file_name, optimize=True)
        current_rgba = current_image.convert("RGBA")
        difference = ImageChops.difference(master, current_rgba)
        changed = sum(1 for pixel in difference.getdata() if pixel != (0, 0, 0, 0))
        classic_bbox = source.convert("RGBA").getchannel("A").getbbox()
        records.append(
            {
                "id": index,
                "name": expected_name,
                "file": file_name,
                "classic_size": list(source.size),
                "hd2_size": [source.width * 2, source.height * 2],
                "hd4_size": list(master.size),
                "classic_bbox": list(classic_bbox) if classic_bbox else None,
                "hd4_bbox": list(master.getchannel("A").getbbox() or ()),
                "changed_pixels_vs_current_lanczos": changed,
            }
        )

    build_comparison(records, classic, current)
    manifest = {
        "format": 1,
        "status": "review_only_not_installed",
        "source": str(CLASSIC_PACK),
        "rules": [
            "classic masks preserve silhouette and hotspot geometry",
            "palette family and cursor function are unchanged",
            "HD2 is derived deterministically from HD4",
            "pack IDs and logical sizes are unchanged",
        ],
        "resources": records,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"built": len(records), "output": str(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
