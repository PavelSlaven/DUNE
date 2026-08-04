#!/usr/bin/env python3
"""Create isolated HD4 campaign-world masters without touching game packs.

The legacy images are used only as geometry contracts.  Their alpha masks and
the region outlines are copied at exact 4x coordinates, while the visible
materials are redrawn from the approved campaign-map master.
"""

from __future__ import annotations

import hashlib
import json
import random
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "hd_completion" / "world"
CLASSIC_PACK = ROOT / "resources" / "bin" / "data" / "sdl_world.dat"
BACKGROUND = ROOT / "resources" / "bin" / "data" / "hd4" / "campaign_map.png"
DENSITY = 4

# IDs intentionally exclude PALETTE_WORLD and WORLD_DUNE_CLICK.
TARGET_IDS = (0, 1, 2, 3, 4, *range(6, 34), 35)
PIECE_ORIGINS = {
    6: (16, 73), 7: (126, 73), 8: (210, 73), 9: (306, 73), 10: (438, 73), 11: (510, 73),
    12: (16, 91), 13: (158, 149), 14: (282, 135), 15: (362, 105), 16: (456, 117), 17: (544, 105),
    18: (16, 155), 19: (58, 165), 20: (190, 213), 21: (312, 163), 22: (388, 163), 23: (502, 167), 24: (576, 167),
    25: (16, 237), 26: (62, 255), 27: (134, 245), 28: (282, 257), 29: (360, 253), 30: (406, 213), 31: (448, 269), 32: (514, 227),
}
HOUSE = ((146, 106, 48), (48, 100, 126), (104, 75, 114))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha4(source: Image.Image) -> Image.Image:
    return source.convert("RGBA").getchannel("A").resize(
        (source.width * DENSITY, source.height * DENSITY), Image.Resampling.NEAREST
    )


def mask_edges(mask: Image.Image, width: int = 3) -> Image.Image:
    # Interior boundary: stable, clean contour, exactly registered to the mask.
    eroded = mask.filter(ImageFilter.MinFilter(width * 2 + 1))
    return ImageChops.subtract(mask, eroded)


def desert_texture(size: tuple[int, int], seed: int, tint: tuple[int, int, int] = (1, 1, 1)) -> Image.Image:
    """Deterministic dune material lit from the upper-left."""
    rng = random.Random(seed)
    base = Image.new("RGB", size, (157, 96, 43))
    detail = Image.effect_noise(size, 36).filter(ImageFilter.GaussianBlur(1.2))
    detail = ImageOps.colorize(detail, (75, 48, 28), (218, 161, 77))
    base = Image.blend(base, detail, 0.42)
    draw = ImageDraw.Draw(base, "RGBA")
    w, h = size
    step = max(14, min(w, h) // 12)
    for y in range(-step, h + step, step):
        phase = rng.randrange(-step, step)
        points = []
        for x in range(-step, w + step, step // 2):
            crest = y + int(0.16 * step * ((x + phase) // max(1, step) % 3 - 1))
            points.append((x, crest))
        draw.line(points, fill=(239, 195, 112, 54), width=max(1, step // 9))
        draw.line([(x, yy + max(1, step // 5)) for x, yy in points], fill=(58, 39, 25, 35), width=max(1, step // 10))
    # upper-left sun sheen, deliberately restrained
    glow = Image.linear_gradient("L").resize(size).rotate(90, expand=False)
    glow = ImageOps.invert(glow).point(lambda v: int(v * 0.18))
    base = Image.composite(Image.new("RGB", size, (232, 185, 99)), base, glow)
    return Image.merge("RGB", tuple(channel.point(lambda v, t=t: min(255, v * t)) for channel, t in zip(base.split(), tint))).convert("RGBA")


def make_piece(source: Image.Image, world: Image.Image, resource_id: int) -> Image.Image:
    origin = PIECE_ORIGINS[resource_id]
    target_size = (source.width * DENSITY, source.height * DENSITY)
    left, top = origin[0] * DENSITY, origin[1] * DENSITY
    material = world.crop((left, top, left + target_size[0], top + target_size[1])).convert("RGBA")
    alpha = alpha4(source)
    result = Image.new("RGBA", target_size, (0, 0, 0, 0))
    result.paste(material, mask=alpha)
    edge = mask_edges(alpha, 2)
    result.alpha_composite(Image.merge("RGBA", (Image.new("L", target_size, 41), Image.new("L", target_size, 29), Image.new("L", target_size, 18), edge)))
    result.putalpha(alpha)
    return result


def panel(size: tuple[int, int], seed: int) -> Image.Image:
    texture = desert_texture(size, seed, (0.73, 0.67, 0.55))
    draw = ImageDraw.Draw(texture, "RGBA")
    w, h = size
    margin = max(8, min(w, h) // 18)
    draw.rectangle((margin, margin, w - margin - 1, h - margin - 1), outline=(235, 191, 96, 255), width=max(2, margin // 4))
    draw.rectangle((margin + 5, margin + 5, w - margin - 6, h - margin - 6), outline=(59, 47, 34, 220), width=max(1, margin // 7))
    return texture


def make_icon(source: Image.Image, resource_id: int) -> Image.Image:
    size = (source.width * DENSITY, source.height * DENSITY)
    silhouette = alpha4(source)
    art = panel(size, resource_id + 300)
    # Preserve the original silhouette and give it a graphite/aged-brass rim.
    edge = mask_edges(silhouette, 2)
    art.alpha_composite(Image.merge("RGBA", (Image.new("L", size, 39), Image.new("L", size, 34), Image.new("L", size, 28), edge)))
    art.putalpha(silhouette)
    return art


def make_regions(source: Image.Image, world: Image.Image) -> Image.Image:
    alpha = alpha4(source)
    size = alpha.size
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    # preserve each original colour field as the region identity, but paint it
    # with transparent House-toned mineral washes over the new Arrakis map.
    legacy = source.convert("RGBA")
    colors = list(legacy.get_flattened_data())
    opaque_colours = sorted({pixel[:3] for pixel in colors if pixel[3] > 0 and sum(pixel[:3]) > 35})
    for number, color in enumerate(opaque_colours):
        mask = Image.new("L", legacy.size)
        mask.putdata([255 if px[:3] == color and px[3] else 0 for px in colors])
        large = mask.resize(size, Image.Resampling.NEAREST)
        tint = HOUSE[number % len(HOUSE)]
        wash = Image.new("RGBA", size, (*tint, 106))
        result.alpha_composite(Image.composite(wash, Image.new("RGBA", size), large))
    # Region seams remain exactly where the classic map defines them.
    dark = Image.new("L", legacy.size)
    dark.putdata([255 if px[3] and sum(px[:3]) < 60 else 0 for px in colors])
    seams = dark.resize(size, Image.Resampling.NEAREST)
    result.alpha_composite(Image.merge("RGBA", (Image.new("L", size, 24), Image.new("L", size, 20), Image.new("L", size, 16), seams)))
    result.putalpha(alpha)
    return result


def make_next_conquest(source: Image.Image) -> Image.Image:
    size = (source.width * DENSITY, source.height * DENSITY)
    result = panel(size, 701)
    # The legacy alpha/text mask anchors labels and controls in the original layout.
    legacy = source.convert("RGBA").resize(size, Image.Resampling.NEAREST)
    bright = legacy.convert("L").point(lambda v: 255 if v > 185 else 0)
    gold = Image.new("RGBA", size, (234, 188, 86, 190))
    result.alpha_composite(Image.composite(gold, Image.new("RGBA", size), bright))
    result.putalpha(alpha4(source))
    return result


def render(source: Image.Image, world: Image.Image, resource_id: int) -> tuple[Image.Image, str]:
    if resource_id == 33:
        return world.copy(), "approved_campaign_background"
    if resource_id == 35:
        return make_regions(source, world), "legacy_region_alpha_and_seams_with_house_mineral_washes"
    if resource_id in PIECE_ORIGINS:
        return make_piece(source, world, resource_id), "legacy_piece_alpha_mask_with_world_material_crop"
    if resource_id == 3:
        return make_next_conquest(source), "redrawn_graphite_and_aged_brass_panel_with_legacy_layout_mask"
    if resource_id in (0, 1, 2, 4):
        return make_icon(source, resource_id), "redrawn_graphite_and_aged_brass_emblem_with_legacy_silhouette"
    raise AssertionError(resource_id)


def verify(records: list[dict[str, object]], sources: dict[int, Image.Image]) -> dict[str, object]:
    for record in records:
        rid = int(record["id"])
        output = Image.open(OUT / record["file"]).convert("RGBA")
        expected = (sources[rid].width * DENSITY, sources[rid].height * DENSITY)
        if output.size != expected:
            raise AssertionError(f"{record['name']}: {output.size}, expected {expected}")
        if ImageChops.difference(output.getchannel("A"), alpha4(sources[rid])).getbbox() is not None:
            raise AssertionError(f"{record['name']}: alpha geometry changed")
    regions = Image.open(OUT / "WORLD_DUNE_REGIONS.png").convert("RGBA")
    legacy = sources[35].convert("RGBA")
    seam_source = Image.new("L", legacy.size)
    seam_source.putdata([255 if px[3] and sum(px[:3]) < 60 else 0 for px in legacy.get_flattened_data()])
    seam = seam_source.resize(regions.size, Image.Resampling.NEAREST)
    seam_pixels = seam.load()
    result_pixels = regions.load()
    for y in range(regions.height):
        for x in range(regions.width):
            if seam_pixels[x, y] and not all(value <= 30 for value in result_pixels[x, y][:3]):
                raise AssertionError("WORLD_DUNE_REGIONS: seam geometry changed")
    return {"passed": True, "checked_resources": len(records), "alpha_geometry": "exact_nearest_4x",
            "region_seams": "exact_nearest_4x"}


def contact_sheet(records: list[dict[str, object]]) -> None:
    cell_w, cell_h = 260, 170
    board = Image.new("RGB", (cell_w * 5, cell_h * 7), (16, 18, 18))
    draw = ImageDraw.Draw(board)
    for pos, record in enumerate(records):
        image = Image.open(OUT / record["file"]).convert("RGBA")
        image.thumbnail((238, 132), Image.Resampling.LANCZOS)
        x, y = (pos % 5) * cell_w + 11, (pos // 5) * cell_h + 8
        board.paste(image, (x, y), image)
        draw.text((x, y + 138), record["name"], fill=(225, 203, 152))
    board.save(OUT / "contact_sheet.png", optimize=True)


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    entries = read_pack(CLASSIC_PACK)
    sources = {rid: decode_image(entries[rid].payload) for rid in TARGET_IDS}
    if any(image is None for image in sources.values()):
        raise RuntimeError("a requested world resource is not a PNG image")
    world = Image.open(BACKGROUND).convert("RGBA")
    if world.size != (2432, 960):
        raise AssertionError(f"campaign map size is {world.size}, expected (2432, 960)")
    records: list[dict[str, object]] = []
    for rid in TARGET_IDS:
        source = sources[rid]
        assert source is not None
        output, method = render(source, world, rid)
        filename = f"{entries[rid].name}.png"
        output.save(OUT / filename, optimize=True)
        records.append({"id": rid, "name": entries[rid].name, "file": filename,
                        "source_size": list(source.size), "target_size": list(output.size), "method": method,
                        "sha256": digest(OUT / filename)})
    checks = verify(records, sources)  # type: ignore[arg-type]
    contact_sheet(records)
    manifest = {"format": 1, "density": 4, "status": "masters_only_not_installed", "resources": records,
                "checks": checks, "excluded": ["PALETTE_WORLD", "WORLD_DUNE_CLICK"]}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUT), "resources": len(records), "checks": checks}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
