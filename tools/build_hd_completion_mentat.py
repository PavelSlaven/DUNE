#!/usr/bin/env python3
"""Create isolated HD4 redraws for the remaining SDL mentat resources.

This never writes resources/bin, active .dat packs, or the current master set.
The seven masters are intended for visual review before any installation step.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from hd_assets import decode_image, read_pack, safe_name, scale_image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "resources" / "bin" / "data" / "sdl_mentat.dat"
OUT = ROOT / "artifacts" / "hd_completion" / "mentat"
SCALE = 4
TARGETS = {
    "BTN_NO", "BTN_YES", "BTN_PROCEED", "BTN_REPEAT", "MENTAT",
    "HEN_HARKONNEN", "MEN_WISH",
}

GRAPHITE = (22, 27, 31, 255)
BRASS = (161, 112, 42, 255)
GOLD = (226, 181, 86, 255)


def q(value: float) -> int:
    return round(value * SCALE)


def line(draw: ImageDraw.ImageDraw, xy, fill, width=1) -> None:
    draw.line([(q(x), q(y)) for x, y in xy], fill=fill, width=q(width))


def rect(draw: ImageDraw.ImageDraw, box, fill=None, outline=None, width=1) -> None:
    draw.rectangle(tuple(q(v) for v in box), fill=fill, outline=outline, width=q(width))


def brushed(size: tuple[int, int], seed: int, alpha: int = 255) -> Image.Image:
    """Graphite sheet with deterministic fine grain and top-left illumination."""
    w, h = q(size[0]), q(size[1])
    image = Image.new("RGBA", (w, h))
    px = image.load()
    for y in range(h):
        for x in range(w):
            grain = ((x * 17 + y * 29 + seed) ^ (x * 7 + y * 13)) & 15
            highlight = int(23 * (1 - x / max(1, w) - y / max(1, h)))
            v = max(0, min(255, 35 + grain - 7 + highlight))
            px[x, y] = (v, v + 4, v + 7, alpha)
    return image


def framed_panel(size: tuple[int, int], seed: int, inset=0) -> Image.Image:
    image = brushed(size, seed)
    draw = ImageDraw.Draw(image)
    w, h = size
    # Same nested bevel vocabulary as the accepted 640x480 mentat panels.
    rect(draw, (inset, inset, w - 1 - inset, h - 1 - inset), outline=(5, 7, 9, 255))
    line(draw, ((inset + 1, h - 2 - inset), (inset + 1, inset + 1), (w - 2 - inset, inset + 1)), (127, 139, 139, 255))
    line(draw, ((w - 2 - inset, inset + 2), (w - 2 - inset, h - 2 - inset), (inset + 2, h - 2 - inset)), (4, 5, 6, 255))
    rect(draw, (inset + 3, inset + 3, w - 4 - inset, h - 4 - inset), outline=BRASS)
    return image


def button(size: tuple[int, int], seed: int) -> Image.Image:
    image = framed_panel(size, seed, 1)
    draw = ImageDraw.Draw(image)
    w, h = size
    rect(draw, (7, 7, w - 8, h - 8), fill=(27, 34, 38, 255), outline=(85, 66, 35, 255))
    # Blank on purpose: labels are rendered by GuiButton in the HD mentat flow.
    line(draw, ((10, 9), (w - 10, 9)), (202, 156, 72, 180))
    line(draw, ((10, h - 10), (w - 10, h - 10)), (7, 10, 12, 255))
    for x in range(17, w - 14, 19):
        line(draw, ((x, 12), (x - 6, h - 13)), (54, 66, 68, 190))
    return image


def text_recess(size: tuple[int, int], seed: int) -> Image.Image:
    """Quiet text backing; all words are deliberately engine-owned."""
    image = framed_panel(size, seed, 0)
    draw = ImageDraw.Draw(image)
    w, h = size
    rect(draw, (3, 3, w - 4, h - 4), fill=(18, 23, 27, 255), outline=(87, 64, 31, 255))
    line(draw, ((6, 5), (w - 7, 5)), (211, 166, 75, 150))
    return image


def mentat_master(source: Image.Image) -> Image.Image:
    """Repaint the compact Bene panel without changing its logical geometry.

    The legacy portrait is retained only as a low-frequency reference layer;
    chrome, viewport, lighting and all high-frequency detail are redrawn.
    """
    size = source.size
    base = source.convert("RGBA").resize((q(size[0]), q(size[1])), Image.Resampling.LANCZOS)
    base = ImageEnhance.Color(base).enhance(0.72).filter(ImageFilter.GaussianBlur(q(0.55)))
    image = brushed(size, 0x36A9)
    # Preserve composition/face registration while making it distinct from any resample.
    portrait = base.crop((0, q(79), q(128), q(240))).filter(ImageFilter.UnsharpMask(q(1), 150, 3))
    image.alpha_composite(portrait, (0, q(79)))
    draw = ImageDraw.Draw(image)
    w, h = size
    # Architectural bands and viewport match the finished panels' thickness/light.
    for y in (6, 12, 64, 69, 225, 231):
        line(draw, ((0, y), (w, y)), (9, 12, 15, 255), 2)
        line(draw, ((0, y - 2), (w, y - 2)), (111, 83, 38, 180))
    for x in range(5, w, 16):
        rect(draw, (x, 14, x + 10, 61), fill=(29, 35, 40, 180), outline=(62, 73, 76, 150))
        rect(draw, (x, 173, x + 10, 223), fill=(27, 33, 38, 180), outline=(61, 72, 75, 150))
    # 168x80 classic viewport remains at the original coordinates and is transparent.
    vx, vy, vw, vh = 128, 81, 184, 84
    rect(draw, (vx - 5, vy - 5, vx + vw + 4, vy + vh + 4), fill=(7, 10, 12, 255), outline=(72, 56, 31, 255), width=2)
    rect(draw, (vx - 2, vy - 2, vx + vw + 1, vy + vh + 1), outline=GOLD)
    rect(draw, (vx, vy, vx + vw - 1, vy + vh - 1), fill=(22, 28, 31, 0), outline=(67, 81, 84, 255))
    # Clearly top-left lit rivets; no text is baked in.
    for x, y in ((9, 8), (311, 8), (9, 231), (311, 231), (122, 75), (317, 75)):
        draw.ellipse((q(x), q(y), q(x + 2), q(y + 2)), fill=(225, 184, 91, 255))
    return image


def sheet(items: list[tuple[str, Path]], destination: Path) -> None:
    cell = (400, 300)
    image = Image.new("RGBA", (cell[0] * 2, cell[1] * math.ceil(len(items) / 2)), (12, 15, 18, 255))
    draw = ImageDraw.Draw(image)
    for index, (name, path) in enumerate(items):
        art = Image.open(path).convert("RGBA")
        art.thumbnail((360, 235), Image.Resampling.LANCZOS)
        x = (index % 2) * cell[0] + (cell[0] - art.width) // 2
        y = (index // 2) * cell[1] + 35
        image.alpha_composite(art, (x, y))
        draw.text(((index % 2) * cell[0] + 16, (index // 2) * cell[1] + 12), name, fill=GOLD)
    image.save(destination)


def main() -> None:
    entries = [entry for entry in read_pack(PACK) if entry.name in TARGETS]
    if {entry.name for entry in entries} != TARGETS:
        raise SystemExit("missing expected SDL mentat resources")
    OUT.mkdir(parents=True, exist_ok=True)
    output_dir = OUT / "master4" / "sdl_mentat"
    output_dir.mkdir(parents=True, exist_ok=True)
    records, items = [], []
    for entry in entries:
        source = decode_image(entry.payload)
        if source is None:
            raise SystemExit(f"{entry.name} is not an image")
        if entry.name.startswith("BTN_"):
            master = button(source.size, entry.index)
        elif entry.name == "MENTAT":
            master = mentat_master(source)
        else:
            master = text_recess(source.size, entry.index)
        name = f"{entry.index:04d}_{safe_name(entry.name)}.png"
        destination = output_dir / name
        master.save(destination, optimize=True)
        nearest = scale_image(source, SCALE).convert("RGBA")
        lanczos = source.convert("RGBA").resize(master.size, Image.Resampling.LANCZOS)
        record = {
            "id": entry.index, "name": entry.name, "source_size": list(source.size),
            "hd_size": list(master.size), "file": destination.relative_to(OUT).as_posix(),
            "mode": master.mode, "alpha_nonempty": master.getchannel("A").getbbox() is not None,
            "differs_from_nearest": master.tobytes() != nearest.tobytes(),
            "differs_from_lanczos": master.tobytes() != lanczos.tobytes(),
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        }
        if not all(record[key] for key in ("alpha_nonempty", "differs_from_nearest", "differs_from_lanczos")):
            raise SystemExit(f"validation failed: {entry.name}")
        records.append(record)
        items.append((entry.name, destination))
    sheet(items, OUT / "contact_sheet.png")
    manifest = {
        "format": 1, "source_pack": str(PACK), "scale": SCALE, "asset_count": len(records),
        "description": "Isolated HD4 mentat redraws. Buttons and text strips are intentionally text-free because the HD UI renders their labels.",
        "assets": records,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} masters to {OUT}")


if __name__ == "__main__":
    main()
