#!/usr/bin/env python3
"""Audit the post-House-selection Mentat screen and its HD artwork."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from hd_assets import decode_image, read_pack  # noqa: E402


MENTAT_IDS = (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 39)
EYE_IDS = range(10, 15)
MOUTH_IDS = range(15, 20)
ACTIVE_EYE_IDS = (12, 14)
SCENES = ("platr", "plhar", "plord")
MAX_RESOURCE_BLOCK_SIMILARITY = 0.985
MAX_SCENE_BLOCK_SIMILARITY = 0.98


def block_similarity(image: Image.Image, density: int = 4) -> float:
    rgb = image.convert("RGB")
    logical = rgb.resize(
        (rgb.width // density, rgb.height // density),
        Image.Resampling.NEAREST,
    )
    nearest = logical.resize(rgb.size, Image.Resampling.NEAREST)
    difference = np.asarray(
        ImageChops.difference(nearest, rgb), dtype=np.float32
    )
    return 1.0 - float(difference.mean() / 255.0)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        Path(r"C:\Windows\Fonts\seguisb.ttf"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def contact_sheet(mentat_path: Path, scenes_root: Path, output: Path) -> None:
    canvas = Image.new("RGB", (1600, 1280), (9, 12, 17))
    draw = ImageDraw.Draw(canvas)
    draw.text((32, 22), "Mentat HD audit", font=font(34), fill=(239, 218, 166))

    mentat = read_pack(mentat_path)
    background = decode_image(mentat[39].payload).convert("RGB")
    canvas.paste(ImageOps.fit(background, (720, 540), Image.Resampling.LANCZOS), (32, 80))
    draw.text((32, 630), "MENTATM HD4", font=font(24), fill=(225, 225, 225))

    x0, y0 = 790, 80
    for row, scene in enumerate(SCENES):
        pack = read_pack(scenes_root / f"sdl_{scene}.dat")
        for column, index in enumerate((0, 8, 16, 24, 32)):
            image = decode_image(pack[index].payload).convert("RGB")
            thumb = ImageOps.fit(image, (150, 92), Image.Resampling.LANCZOS)
            canvas.paste(thumb, (x0 + column * 156, y0 + row * 142))
        draw.text(
            (x0, y0 + row * 142 + 98),
            scene,
            font=font(20),
            fill=(225, 225, 225),
        )

    background_rgba = background.convert("RGBA")
    face_crop = (280, 620, 900, 1240)
    for row, resource_ids in enumerate((EYE_IDS, MOUTH_IDS)):
        for column, resource_id in enumerate(resource_ids):
            frame = background_rgba.copy()
            overlay = decode_image(mentat[resource_id].payload).convert("RGBA")
            position = (96 * 4, 180 * 4) if resource_id in EYE_IDS else (100 * 4, 210 * 4)
            frame.alpha_composite(overlay, position)
            thumb = ImageOps.fit(frame.crop(face_crop), (220, 220), Image.Resampling.LANCZOS)
            canvas.paste(thumb.convert("RGB"), (32 + column * 228, 760 + row * 236))
        draw.text(
            (1190, 845 + row * 236),
            "eyes" if row == 0 else "mouth",
            font=font(22),
            fill=(225, 225, 225),
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game",
        type=Path,
        default=Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "artifacts" / "mentat_hd_v1" / "audit.json",
    )
    parser.add_argument("--mentat-pack", type=Path)
    parser.add_argument("--scenes-root", type=Path)
    args = parser.parse_args()
    mentat_path = args.mentat_pack or args.game / "data" / "sdl_mentat_hd4.dat"
    scenes_root = args.scenes_root or args.game / "data" / "scenes" / "hd4"

    failures: list[str] = []
    source = (ROOT / "src" / "mentat" / "AbstractMentat.cpp").read_text(
        encoding="utf-8"
    )
    bene_source = (ROOT / "src" / "mentat" / "BeneMentat.cpp").read_text(
        encoding="utf-8"
    )
    if "cRectangle dest = {offsetX, offsetY,640, 480};" in source:
        failures.append("Mentat canvas is hard-coded to 640x480")
    if "m_textDrawer = ctx->getTextContext()->getBeneTextDrawer();" in source:
        failures.append("HD Mentat still uses the 12 px text drawer")

    context_source = (ROOT / "src" / "context" / "ContextCreator.cpp").read_text(
        encoding="utf-8"
    )
    drawer_source = (ROOT / "src" / "drawers" / "cTextDrawer.cpp").read_text(
        encoding="utf-8"
    )
    font_path = ROOT / "resources" / "bin" / "data" / "RussoOne-Regular.ttf"
    if not font_path.exists():
        failures.append("Dedicated remastered Mentat font is missing")
    if "RussoOne-Regular.ttf" not in context_source:
        failures.append("Dedicated remastered Mentat font is not loaded")
    if "getMentatHdTextDrawer()" not in source:
        failures.append("HD Mentat does not use its dedicated text drawer")
    if "drawTextScaledCenteredInBox" not in source or "drawTextScaledCenteredInBox" not in drawer_source:
        failures.append("HD Mentat text is not centered by actual TTF metrics")
    for expected_rect in (
        "baseRect(336, 405, 112, 49)",
        "baseRect(492, 405, 112, 49)",
    ):
        if expected_rect not in bene_source:
            failures.append(
                f"HD response button does not match its background recess: {expected_rect}"
            )

    mentat_pack = read_pack(mentat_path)
    resources: dict[str, float] = {}
    for resource_id in MENTAT_IDS:
        entry = mentat_pack[resource_id]
        image = decode_image(entry.payload)
        similarity = block_similarity(image)
        resources[entry.name] = round(similarity, 5)
        if similarity > MAX_RESOURCE_BLOCK_SIMILARITY:
            failures.append(
                f"{entry.name} is a low-detail logical upscale ({similarity:.4f})"
            )
        if resource_id in (*EYE_IDS, *MOUTH_IDS):
            expected_size = (384, 128) if resource_id in EYE_IDS else (448, 320)
            if image.size != expected_size:
                failures.append(
                    f"{entry.name} has unstable dimensions {image.size}, expected {expected_size}"
                )
            alpha = np.asarray(image.convert("RGBA").getchannel("A"), dtype=np.uint8)
            border_alpha = max(
                int(alpha[0, :].max()),
                int(alpha[-1, :].max()),
                int(alpha[:, 0].max()),
                int(alpha[:, -1].max()),
            )
            if border_alpha != 0:
                failures.append(
                    f"{entry.name} has an opaque crop border (alpha {border_alpha})"
                )
            if resource_id in ACTIVE_EYE_IDS:
                # The eyelid core must replace the open eye, not alpha-blend
                # over it.  A translucent core makes the iris shine through
                # during a blink.
                eye_cores = (
                    alpha[45:92, 58:116],
                    alpha[43:92, 164:236],
                )
                core_opacity = min(
                    float(np.percentile(core, 10)) for core in eye_cores
                )
                if core_opacity < 245:
                    failures.append(
                        f"{entry.name} leaves the iris visible through the eyelid "
                        f"(eye-core alpha p10 {core_opacity:.0f})"
                    )

    scenes: dict[str, float] = {}
    for scene in SCENES:
        pack = read_pack(scenes_root / f"sdl_{scene}.dat")
        similarities = [block_similarity(decode_image(entry.payload)) for entry in pack]
        average = sum(similarities) / len(similarities)
        scenes[scene] = round(average, 5)
        if average > MAX_SCENE_BLOCK_SIMILARITY:
            failures.append(
                f"{scene} animation is a low-detail logical upscale ({average:.4f})"
            )

    report = {
        "mentat_font": {
            "name": "Russo One",
            "path": str(font_path),
            "present": font_path.exists(),
        },
        "mentat_resources": resources,
        "scene_average_block_similarity": scenes,
        "failures": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    contact_sheet(mentat_path, scenes_root, args.output.with_name("current_contact_sheet.png"))

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: Mentat screen is adaptive and contains true HD detail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
