#!/usr/bin/env python3
"""Regrade the accepted Light Factory without changing its geometry."""

from __future__ import annotations

import argparse
import colorsys
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "artifacts" / "lightfactory_palette_fix"
SOURCE = WORK / "source" / "0012_BUILD_LIGHTFACTORY.png"
OUTPUT = WORK / "masters" / "0012_BUILD_LIGHTFACTORY.png"
REVIEW = ROOT / "artifacts" / "lightfactory_review_v2" / "BUILD_LIGHTFACTORY_HD4_PREVIEW.png"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0012_BUILD_LIGHTFACTORY.png"


def clamp(value: float) -> int:
    return max(0, min(255, round(value)))


def regrade_pixel(pixel: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    r, g, b, a = pixel
    if a == 0 or max(r, g, b) <= 4:
        return pixel

    hue, saturation, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    # Preserve the accepted indicator colours and warning light.
    cyan = b >= r + 18 and g >= r + 15 and (g + b) >= 130
    red = r >= 80 and r >= g * 1.45 and r >= b * 1.30
    if cyan or red:
        return r, g, b, a

    # Existing brass pipes and ochre mechanisms already match the common style.
    warm_metal = (
        hue < 0.18
        and saturation > 0.12
        and r - b >= 12
        and g - b >= 4
        and r >= g * 0.92
    )
    if warm_metal:
        target = min(255.0, luminance * 1.05 + 2.0)
        scale = target / max(1.0, luminance)
        return clamp(r * scale), clamp(g * scale), clamp(b * scale), a

    # Neutral steel/graphite body. Keep local shading and 12% of the source
    # chroma so fine material variation survives while the olive cast does not.
    target = max(0.0, min(255.0, luminance * 1.10 + 7.0))
    scale = target / max(1.0, luminance)
    source_r = r * scale
    source_g = g * scale
    source_b = b * scale
    neutral_r = target * 1.01
    neutral_g = target * 0.995
    neutral_b = target * 1.02
    source_mix = 0.12
    return (
        clamp(neutral_r * (1 - source_mix) + source_r * source_mix),
        clamp(neutral_g * (1 - source_mix) + source_g * source_mix),
        clamp(neutral_b * (1 - source_mix) + source_b * source_mix),
        a,
    )


def regrade(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    result = Image.new("RGBA", rgba.size)
    result.putdata([regrade_pixel(pixel) for pixel in rgba.getdata()])
    return result


def metrics(image: Image.Image) -> dict[str, object]:
    pixels = [
        pixel[:3]
        for pixel in image.convert("RGBA").getdata()
        if pixel[3] > 32 and max(pixel[:3]) > 8
    ]
    means = [sum(pixel[channel] for pixel in pixels) / len(pixels) for channel in range(3)]
    luminance = sum(
        0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in pixels
    ) / len(pixels)
    return {
        "visible_pixels": len(pixels),
        "mean_rgb": [round(value, 3) for value in means],
        "mean_luminance": round(luminance, 3),
        "green_bias": round(means[1] - (means[0] + means[2]) / 2, 3),
    }


def make_comparison(before: Image.Image, after: Image.Image, path: Path) -> None:
    scale = 2
    tile_size = (before.width * scale, before.height * scale)
    canvas = Image.new("RGB", (tile_size[0] * 2, tile_size[1] + 48), (14, 17, 20))
    canvas.paste(before.resize(tile_size, Image.Resampling.NEAREST), (0, 48), before.resize(tile_size, Image.Resampling.NEAREST))
    canvas.paste(after.resize(tile_size, Image.Resampling.NEAREST), (tile_size[0], 48), after.resize(tile_size, Image.Resampling.NEAREST))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((12, 16), "BEFORE: olive cast", fill=(230, 230, 230), font=font)
    draw.text((tile_size[0] + 12, 16), "AFTER: neutral graphite / steel", fill=(230, 230, 230), font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(path, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="update the approved review image and canonical HD4 master",
    )
    args = parser.parse_args()

    before = Image.open(SOURCE).convert("RGBA")
    after = regrade(before)
    if before.size != (256, 256):
        raise AssertionError(f"unexpected Light Factory size: {before.size}")
    if list(before.getchannel("A").getdata()) != list(after.getchannel("A").getdata()):
        raise AssertionError("alpha silhouette changed")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    after.save(OUTPUT, optimize=True)
    make_comparison(before, after, WORK / "comparison_palette_fix.png")

    report = {
        "source": str(SOURCE),
        "output": str(OUTPUT),
        "before": metrics(before),
        "after": metrics(after),
        "alpha_exact": True,
        "geometry_changed": False,
        "applied": args.apply,
    }
    if abs(float(report["after"]["green_bias"])) >= abs(float(report["before"]["green_bias"])):
        raise AssertionError("olive cast was not reduced")

    if args.apply:
        for destination in (REVIEW, MASTER):
            destination.parent.mkdir(parents=True, exist_ok=True)
            after.save(destination, optimize=True)

    (WORK / "palette_fix_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
