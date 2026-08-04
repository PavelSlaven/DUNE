#!/usr/bin/env python3
"""Assemble the approved artistic cursor redraws into reviewable HD2/HD4 assets."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
CLASSIC_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data.dat"
CURRENT_HD4_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data_hd4.dat"
OUT = ROOT / "artifacts" / "cursor_hd_redraw_v2"
ALPHA = OUT / "alpha"
HD4 = OUT / "hd4"
HD2 = OUT / "hd2"

CURSORS = (
    (79, "MOUSE_ATTACK", "0079_attack.png"),
    (80, "MOUSE_DOWN", "0080_down.png"),
    (81, "MOUSE_FORBIDDEN", "0081_forbidden.png"),
    (82, "MOUSE_LEFT", "0082_left.png"),
    (83, "MOUSE_MOVE", "0083_move.png"),
    (84, "MOUSE_NORMAL", "0084_normal.png"),
    (85, "MOUSE_PICK", "0085_pick.png"),
    (86, "MOUSE_RALLY", "0086_rally.png"),
    (87, "MOUSE_REPAIR", "0087_repair.png"),
    (88, "MOUSE_RIGHT", "0088_right.png"),
    (89, "MOUSE_UP", "0089_up.png"),
)

# HD4 placement preserves the classic canvas and cursor hotspot conventions.
# The normal pointer is intentionally a little broader than the old 14 px silhouette.
TARGET_BOXES = {
    "MOUSE_ATTACK": (8, 16, 128, 112),
    "MOUSE_DOWN": (1, 1, 71, 71),
    "MOUSE_FORBIDDEN": (8, 16, 128, 108),
    "MOUSE_LEFT": (1, 1, 63, 79),
    "MOUSE_MOVE": (8, 16, 128, 112),
    "MOUSE_NORMAL": (0, 0, 66, 108),
    "MOUSE_PICK": (4, 4, 140, 140),
    "MOUSE_RALLY": (8, 16, 128, 112),
    "MOUSE_REPAIR": (12, 6, 122, 128),
    "MOUSE_RIGHT": (1, 1, 63, 79),
    "MOUSE_UP": (1, 1, 71, 71),
}


def alpha_bbox(image: Image.Image, threshold: int = 12) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha > threshold)
    if len(xs) == 0:
        raise ValueError("generated cursor contains no visible pixels")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def premultiplied_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32) / 255.0
    alpha = rgba[:, :, 3:4]
    premultiplied = np.concatenate((rgba[:, :, :3] * alpha, alpha), axis=2)
    channels = []
    for channel in range(4):
        plane = Image.fromarray(premultiplied[:, :, channel], mode="F")
        channels.append(np.asarray(plane.resize(size, Image.Resampling.LANCZOS), dtype=np.float32))
    resized = np.stack(channels, axis=2)
    out_alpha = np.clip(resized[:, :, 3:4], 0.0, 1.0)
    rgb = np.divide(
        resized[:, :, :3],
        np.maximum(out_alpha, 1.0 / 255.0),
        out=np.zeros_like(resized[:, :, :3]),
        where=out_alpha > 0,
    )
    out = np.concatenate((np.clip(rgb, 0.0, 1.0), out_alpha), axis=2)
    return Image.fromarray(np.round(out * 255.0).astype(np.uint8), "RGBA")


def fit_cursor(name: str, source: Image.Image, canvas_size: tuple[int, int]) -> Image.Image:
    crop = source.convert("RGBA").crop(alpha_bbox(source))
    x1, y1, x2, y2 = TARGET_BOXES[name]
    target_w, target_h = x2 - x1, y2 - y1

    # Reticles and compact direction arrows intentionally follow the classic
    # projected footprint. Free silhouettes retain their authored proportions.
    stretch = name in {
        "MOUSE_ATTACK",
        "MOUSE_DOWN",
        "MOUSE_FORBIDDEN",
        "MOUSE_LEFT",
        "MOUSE_MOVE",
        "MOUSE_RALLY",
        "MOUSE_RIGHT",
        "MOUSE_UP",
    }
    if stretch:
        fitted = premultiplied_resize(crop, (target_w, target_h))
        px, py = x1, y1
    else:
        ratio = min(target_w / crop.width, target_h / crop.height)
        fitted_size = (max(1, round(crop.width * ratio)), max(1, round(crop.height * ratio)))
        fitted = premultiplied_resize(crop, fitted_size)
        if name == "MOUSE_NORMAL":
            px, py = x1, y1
        else:
            px = x1 + (target_w - fitted.width) // 2
            py = y1 + (target_h - fitted.height) // 2

    fitted = fitted.filter(ImageFilter.UnsharpMask(radius=0.65, percent=105, threshold=3))
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, (px, py))
    return canvas


def checker(size: tuple[int, int], cell: int = 10) -> Image.Image:
    result = Image.new("RGBA", size, (25, 29, 34, 255))
    draw = ImageDraw.Draw(result)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(37, 42, 48, 255))
    return result


def preview_cell(image: Image.Image, size: tuple[int, int], nearest: bool = False) -> Image.Image:
    cell = checker(size)
    limit = (size[0] - 22, size[1] - 22)
    sample = image.copy()
    sample.thumbnail(limit, Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)
    cell.alpha_composite(sample, ((cell.width - sample.width) // 2, (cell.height - sample.height) // 2))
    return cell


def font(size: int) -> ImageFont.ImageFont:
    candidates = (
        Path("C:/Windows/Fonts/arialbd.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def build_comparison(records: list[dict[str, object]], classic: list, current: list) -> None:
    width, row_h = 1220, 238
    sheet = Image.new("RGBA", (width, 82 + row_h * len(records)), (8, 11, 14, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 18), "D2TM — художественная перерисовка курсоров", font=font(24), fill=(229, 190, 91, 255))
    draw.text((410, 54), "ОРИГИНАЛ", font=font(15), fill=(162, 170, 180, 255))
    draw.text((675, 54), "ТЕКУЩИЙ HD", font=font(15), fill=(162, 170, 180, 255))
    draw.text((940, 54), "НОВАЯ РИСОВКА", font=font(15), fill=(229, 190, 91, 255))
    for row, record in enumerate(records):
        y = 82 + row * row_h
        draw.rectangle((14, y + 4, width - 14, y + row_h - 8), outline=(82, 68, 43, 255), width=1)
        draw.text((28, y + 28), f"#{record['id']}  {record['name']}", font=font(17), fill=(231, 226, 210, 255))
        original = decode_image(classic[record["id"]].payload).convert("RGBA")
        old_hd = decode_image(current[record["id"]].payload).convert("RGBA")
        new_hd = Image.open(HD4 / record["file"]).convert("RGBA")
        sheet.alpha_composite(preview_cell(original.resize((original.width * 8, original.height * 8), Image.Resampling.NEAREST), (240, 186), True), (380, y + 22))
        sheet.alpha_composite(preview_cell(old_hd, (240, 186)), (645, y + 22))
        sheet.alpha_composite(preview_cell(new_hd, (240, 186)), (910, y + 22))
    sheet.convert("RGB").save(OUT / "comparison_classic_current_artistic.jpg", quality=94, subsampling=0)


def main() -> int:
    HD4.mkdir(parents=True, exist_ok=True)
    HD2.mkdir(parents=True, exist_ok=True)
    classic = read_pack(CLASSIC_PACK)
    current = read_pack(CURRENT_HD4_PACK)
    records: list[dict[str, object]] = []

    for index, name, file_name in CURSORS:
        if classic[index].name != name or current[index].name != name:
            raise ValueError(f"cursor contract mismatch at {index}: {name}")
        source = decode_image(classic[index].payload).convert("RGBA")
        canvas_size = (source.width * 4, source.height * 4)
        art = Image.open(ALPHA / f"{name}.png").convert("RGBA")
        master = fit_cursor(name, art, canvas_size)
        master.save(HD4 / file_name, optimize=True)
        hd2 = premultiplied_resize(master, (source.width * 2, source.height * 2))
        hd2.save(HD2 / file_name, optimize=True)

        current_image = decode_image(current[index].payload).convert("RGBA")
        difference = ImageChops.difference(master, current_image)
        changed = sum(1 for pixel in difference.getdata() if pixel != (0, 0, 0, 0))
        records.append(
            {
                "id": index,
                "name": name,
                "file": file_name,
                "classic_size": list(source.size),
                "hd2_size": list(hd2.size),
                "hd4_size": list(master.size),
                "hd4_bbox": list(master.getchannel("A").getbbox() or ()),
                "changed_pixels_vs_current": changed,
            }
        )

    build_comparison(records, classic, current)
    manifest = {
        "format": 2,
        "status": "review_only_not_installed",
        "method": "image-guided artistic redraw plus deterministic alpha cleanup and packing",
        "rules": [
            "cursor function and palette family remain recognizable",
            "canvas dimensions and engine hotspot conventions are preserved",
            "HD2 is derived deterministically from HD4",
            "no game data pack has been modified",
        ],
        "resources": records,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"built": len(records), "comparison": str(OUT / "comparison_classic_current_artistic.jpg")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
