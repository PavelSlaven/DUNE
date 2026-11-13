#!/usr/bin/env python3
"""Restore/redraw the user-selected legacy UI and campaign-map resources.

The original HD comparison captures are used as geometry masks.  This keeps
the classic silhouettes and atlas dimensions while replacing the hard 4x4
pixel stair-steps with antialiased graphite/brass artwork.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "artifacts" / "hd_completion_comparison" / "old"
INTERFACE = ROOT / "artifacts" / "hd_completion" / "interface"
WORLD = ROOT / "artifacts" / "hd_completion" / "world"
REVIEW = ROOT / "artifacts" / "requested_ui_remaster"

GRID_IDS = {
    23: "GRID_0X0",
    24: "GRID_1X1",
    25: "GRID_2X2",
    26: "GRID_3X2",
    27: "GRID_3X3",
}

STATUS_IDS = {
    139: "ICON_POWER",
    140: "ICON_POWER_HIGH",
    141: "ICON_SOLARIS_LOW",
    142: "ICON_SOLARIS",
    143: "ICON_SOLARIS_FULL",
}


def old_path(pack: str, resource_id: int, name: str) -> Path:
    return OLD / f"{pack}_{resource_id:04d}_{name}.png"


def visible_mask(image: Image.Image, threshold: int = 10) -> Image.Image:
    rgba = image.convert("RGBA")
    rgb = rgba.convert("RGB")
    maximum = ImageChops.lighter(
        ImageChops.lighter(rgb.getchannel("R"), rgb.getchannel("G")),
        rgb.getchannel("B"),
    )
    mask = maximum.point(lambda value: 255 if value > threshold else 0)
    mask = ImageChops.multiply(mask, rgba.getchannel("A"))
    return mask.filter(ImageFilter.GaussianBlur(0.55))


def gradient_fill(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    result = Image.new("RGBA", size)
    pixels = result.load()
    height = max(1, size[1] - 1)
    for y in range(size[1]):
        t = y / height
        color = tuple(round(top[i] * (1.0 - t) + bottom[i] * t) for i in range(3)) + (255,)
        for x in range(size[0]):
            pixels[x, y] = color
    return result


def redraw_grid(source: Image.Image) -> Image.Image:
    mask = visible_mask(source, 8)
    result = Image.new("RGBA", source.size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", source.size, (0, 0, 0, 0))
    shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(1.2)).point(lambda value: value * 3 // 5))
    result.alpha_composite(Image.new("RGBA", source.size, (4, 6, 7, 0)))
    shadow_rgb = Image.new("RGBA", source.size, (2, 3, 4, 0))
    shadow_rgb.putalpha(shadow.getchannel("A"))
    result.alpha_composite(shadow_rgb, (1, 2))
    metal = gradient_fill(source.size, (232, 205, 130), (102, 83, 45))
    metal.putalpha(mask)
    result.alpha_composite(metal)
    edge = mask.filter(ImageFilter.FIND_EDGES).point(lambda value: min(170, value))
    highlight = Image.new("RGBA", source.size, (255, 234, 165, 0))
    highlight.putalpha(edge)
    result.alpha_composite(highlight)
    return result


def redraw_status(source: Image.Image, name: str) -> Image.Image:
    mask = visible_mask(source, 6)
    result = Image.new("RGBA", source.size, (0, 0, 0, 0))
    is_power = name.startswith("ICON_POWER")
    if name.endswith("HIGH") or name.endswith("FULL"):
        top, bottom, glow_color = (255, 116, 87), (179, 29, 31), (255, 48, 35)
    elif name.endswith("LOW") or name == "ICON_POWER":
        top, bottom, glow_color = (238, 244, 244), (125, 142, 147), (180, 218, 225)
    else:
        top, bottom, glow_color = (255, 218, 105), (175, 119, 34), (255, 186, 52)

    glow_mask = mask.filter(ImageFilter.GaussianBlur(3.0)).point(lambda value: value // 2)
    glow = Image.new("RGBA", source.size, (*glow_color, 0))
    glow.putalpha(glow_mask)
    result.alpha_composite(glow)

    dark_edge = mask.filter(ImageFilter.MaxFilter(5))
    outline = Image.new("RGBA", source.size, (10, 14, 17, 0))
    outline.putalpha(dark_edge)
    result.alpha_composite(outline)

    fill = gradient_fill(source.size, top, bottom)
    fill.putalpha(mask)
    result.alpha_composite(fill)
    if is_power:
        shine = Image.new("RGBA", source.size, (255, 255, 255, 0))
        shifted = ImageChops.offset(mask, -1, -1)
        shine.putalpha(ImageChops.subtract(shifted, mask).point(lambda value: min(150, value)))
        result.alpha_composite(shine)
    return result


def recolor_campaign_emblem(source: Image.Image) -> Image.Image:
    rgba = source.convert("RGBA")
    mask = visible_mask(rgba, 12)
    # Preserve the original emblem's relief, but move it into the shared
    # graphite/aged-brass campaign palette and remove the black matte.
    luminance = rgba.convert("L").filter(ImageFilter.SMOOTH_MORE)
    luminance = ImageEnhance.Contrast(luminance).enhance(1.18)
    color = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    pixels = color.load()
    values = luminance.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            value = values[x, y] / 255.0
            if value < 0.27:
                t = value / 0.27
                lo, hi = (18, 21, 23), (75, 54, 29)
            else:
                t = (value - 0.27) / 0.73
                lo, hi = (75, 54, 29), (239, 194, 93)
            pixels[x, y] = tuple(round(lo[i] * (1 - t) + hi[i] * t) for i in range(3)) + (255,)
    color.putalpha(mask)
    color = color.filter(ImageFilter.UnsharpMask(radius=1.1, percent=115, threshold=3))
    color.putalpha(mask)
    return color


def update_manifest(path: Path) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    records_key = "assets" if "assets" in manifest else "resources"
    base = path.parent
    for record in manifest[records_key]:
        asset = base / str(record["file"])
        if asset.is_file():
            record["sha256"] = hashlib.sha256(asset.read_bytes()).hexdigest()
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_review(paths: list[tuple[str, Path]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    cell_w, cell_h = 300, 220
    sheet = Image.new("RGBA", (cell_w * 3, cell_h * ((len(paths) + 2) // 3)), (13, 16, 18, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (name, path) in enumerate(paths):
        image = Image.open(path).convert("RGBA")
        image.thumbnail((260, 165), Image.Resampling.LANCZOS)
        x = (index % 3) * cell_w + (cell_w - image.width) // 2
        y = (index // 3) * cell_h + 14
        sheet.alpha_composite(image, (x, y))
        draw.text(((index % 3) * cell_w + 14, (index // 3) * cell_h + 187), name, fill=(230, 194, 113, 255))
    sheet.save(REVIEW / "contact_sheet.png", optimize=True)


def main() -> int:
    outputs: list[tuple[str, Path]] = []

    credits_source = old_path("sdl_inter", 21, "CREDITS_DUNE2_CORE_TEAM")
    credits_target = INTERFACE / "screens" / "0021_CREDITS_DUNE2_CORE_TEAM.png"
    shutil.copy2(credits_source, credits_target)
    outputs.append(("CREDITS_DUNE2_CORE_TEAM", credits_target))

    for resource_id, name in GRID_IDS.items():
        source = Image.open(old_path("sdl_inter", resource_id, name)).convert("RGBA")
        target = INTERFACE / "controls" / f"{resource_id:04d}_{name}.png"
        redraw_grid(source).save(target, optimize=True)
        outputs.append((name, target))

    for resource_id, name in STATUS_IDS.items():
        source = Image.open(old_path("sdl_inter", resource_id, name)).convert("RGBA")
        target = INTERFACE / "status" / f"{resource_id:04d}_{name}.png"
        redraw_status(source, name).save(target, optimize=True)
        outputs.append((name, target))

    for resource_id, name in ((1, "BMP_NCHAR"), (2, "BMP_NCORD")):
        source = Image.open(old_path("sdl_world", resource_id, name)).convert("RGBA")
        target = WORLD / f"{name}.png"
        recolor_campaign_emblem(source).save(target, optimize=True)
        outputs.append((name, target))

    update_manifest(INTERFACE / "manifest.json")
    update_manifest(WORLD / "manifest.json")
    build_review(outputs)
    report = {
        "restored": ["CREDITS_DUNE2_CORE_TEAM"],
        "redrawn": [name for name, _ in outputs if name != "CREDITS_DUNE2_CORE_TEAM"],
        "contact_sheet": str((REVIEW / "contact_sheet.png").relative_to(ROOT)).replace("\\", "/"),
    }
    (REVIEW / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(outputs)} requested resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
