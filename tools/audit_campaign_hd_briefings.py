#!/usr/bin/env python3
"""Audit campaign HD packs and render deterministic layout previews."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "campaign_hd_v1"
DATA = ARTIFACT / "data"
SCENES = (
    "harvest", "headqrts", "hitcftry", "hvyftry", "ix", "liteftry",
    "lose01", "lose02", "ltank", "palace", "platr", "plhar", "plord",
    "quad", "repair", "sardukar", "win01", "win02",
)
MENTATS = {
    "atreides": {
        "background": 37, "eyes": 2, "mouth": 8,
        "eye_origin": (96, 180), "mouth_origin": (100, 210),
        "movie": (265, 114, 337, 205),
        "buttons": ((342, 393, 124, 52), (482, 393, 110, 52)),
    },
    "harkonnen": {
        "background": 38, "eyes": 26, "mouth": 32,
        "eye_origin": (96, 180), "mouth_origin": (100, 210),
        "buttons": ((313, 397, 148, 59), (479, 397, 139, 59)),
    },
    "ordos": {
        "background": 40, "eyes": 43, "mouth": 49,
        "eye_origin": (48, 174), "mouth_origin": (52, 207),
        "buttons": ((313, 397, 148, 59), (479, 397, 139, 59)),
    },
}


def image(entry) -> Image.Image:
    return decode_image(entry.payload).convert("RGBA")


def assert_equal_image(actual: Image.Image, expected: Image.Image, label: str) -> None:
    if actual.size != expected.size or ImageChops.difference(actual, expected).getbbox() is not None:
        raise AssertionError(f"{label}: HD2 is not the deterministic HD4 downsample")


def assert_atreides_mentat_identity(background: Image.Image) -> dict[str, float]:
    """Reject the dark-haired portrait accidentally used instead of blond Cyril."""
    logical = background.convert("RGB").resize((640, 480), Image.Resampling.LANCZOS)
    portrait_hair = logical.crop((35, 130, 210, 345))
    pixels = list(portrait_hair.get_flattened_data())
    blond_ratio = sum(
        1 for red, green, blue in pixels
        if red > 85 and red > green * 1.08 and green > blue * 1.25
    ) / len(pixels)
    dark_ratio = sum(1 for red, green, blue in pixels if max(red, green, blue) < 45) / len(pixels)
    if blond_ratio < 0.15 or dark_ratio > 0.75:
        raise AssertionError(
            "atreides: MENTATA does not contain Cyril's blond portrait "
            f"(blond={blond_ratio:.3f}, dark={dark_ratio:.3f})"
        )
    return {"blond_ratio": blond_ratio, "dark_ratio": dark_ratio}


def mouth_dark_row(image: Image.Image) -> int:
    """Locate the dark lip/aperture line in the fixed Atreides mouth crop."""
    gray = image.convert("RGB").crop((120, 40, 280, 160)).convert("L")
    rows = [
        sum(gray.crop((0, y, gray.width, y + 1)).get_flattened_data())
        for y in range(gray.height)
    ]
    return 40 + min(range(len(rows)), key=rows.__getitem__)


def assert_atreides_mouth_registration(
    background: Image.Image,
    mouth: Image.Image,
) -> dict[str, int]:
    """Catch a speaking mouth that jumps away from the resting lip line."""
    origin_x, origin_y = (value * 4 for value in MENTATS["atreides"]["mouth_origin"])
    base = background.crop(
        (origin_x, origin_y, origin_x + mouth.width, origin_y + mouth.height)
    ).convert("RGBA")
    speaking = base.copy()
    speaking.alpha_composite(mouth)
    resting_row = mouth_dark_row(base)
    speaking_row = mouth_dark_row(speaking)
    delta = speaking_row - resting_row
    if abs(delta) > 3:
        raise AssertionError(
            "atreides: speaking mouth is vertically displaced from the resting mouth "
            f"by {delta} HD4 pixels"
        )
    return {
        "mouth_resting_row": resting_row,
        "mouth_speaking_row": speaking_row,
        "mouth_registration_delta": delta,
    }


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = ROOT / "resources" / "bin" / "data" / "RussoOne-Regular.ttf"
    return ImageFont.truetype(path, size) if path.exists() else ImageFont.load_default()


def render_scene_contact_sheet() -> Path:
    thumb = (368, 224)
    sheet = Image.new("RGB", (thumb[0] * 3, (thumb[1] + 28) * 6), (7, 7, 15))
    draw = ImageDraw.Draw(sheet)
    label_font = font(16)
    for index, name in enumerate(SCENES):
        entries = read_pack(DATA / "scenes" / "hd4" / f"sdl_{name}.dat")
        frame = image(entries[len(entries) // 2]).convert("RGB")
        frame.thumbnail(thumb, Image.Resampling.LANCZOS)
        x = (index % 3) * thumb[0]
        y = (index // 3) * (thumb[1] + 28)
        sheet.paste(ImageOps.fit(frame, thumb, Image.Resampling.LANCZOS), (x, y))
        draw.text((x + 8, y + thumb[1] + 4), name, font=label_font, fill=(255, 226, 165))
    output = ARTIFACT / "campaign_scene_contact_sheet.png"
    sheet.save(output, optimize=True)
    return output


def render_mentat_previews() -> list[Path]:
    pack = read_pack(DATA / "sdl_mentat_hd4.dat")
    scene = image(read_pack(DATA / "scenes" / "hd4" / "sdl_platr.dat")[16])
    outputs: list[Path] = []
    labels = ("Повторить", "Далее")
    button_font = font(52)
    text_font = font(44)
    for name, ids in MENTATS.items():
        canvas = image(pack[ids["background"]])
        movie_rect = ids.get("movie", (205, 96, 400, 243))
        movie = scene.resize((movie_rect[2] * 4, movie_rect[3] * 4), Image.Resampling.LANCZOS)
        canvas.alpha_composite(movie, (movie_rect[0] * 4, movie_rect[1] * 4))
        canvas.alpha_composite(image(pack[ids["eyes"]]), tuple(value * 4 for value in ids["eye_origin"]))
        canvas.alpha_composite(image(pack[ids["mouth"]]), tuple(value * 4 for value in ids["mouth_origin"]))
        draw = ImageDraw.Draw(canvas, "RGBA")
        sample = "Разведданные подтверждены. Начинайте операцию."
        box = draw.textbbox((0, 0), sample, font=text_font)
        draw.text(((canvas.width - (box[2] - box[0])) // 2, 72), sample, font=text_font, fill=(255, 226, 165, 255))
        for rect, label in zip(ids["buttons"], labels, strict=True):
            x, y, width, height = (value * 4 for value in rect)
            draw.rounded_rectangle(
                (x, y, x + width, y + height),
                radius=8,
                fill=(23, 29, 33, 246),
                outline=(179, 132, 43, 255),
                width=4,
            )
            text_box = draw.textbbox((0, 0), label, font=button_font)
            text_width = text_box[2] - text_box[0]
            text_height = text_box[3] - text_box[1]
            draw.text(
                (x + (width - text_width) // 2, y + (height - text_height) // 2 - text_box[1]),
                label,
                font=button_font,
                fill=(244, 235, 204, 255),
            )
        output = ARTIFACT / f"preview_mentat_{name}.png"
        canvas.resize((1280, 960), Image.Resampling.LANCZOS).save(output, optimize=True)
        outputs.append(output)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, required=True)
    args = parser.parse_args()

    checks: list[dict[str, object]] = []
    for name in SCENES:
        classic = read_pack(args.game / "data" / "scenes" / f"sdl_{name}.dat")
        hd2 = read_pack(DATA / "scenes" / "hd2" / f"sdl_{name}.dat")
        hd4 = read_pack(DATA / "scenes" / "hd4" / f"sdl_{name}.dat")
        if not (len(classic) == len(hd2) == len(hd4)):
            raise AssertionError(f"{name}: frame count changed")
        for index, (entry2, entry4) in enumerate(zip(hd2, hd4, strict=True)):
            frame2 = image(entry2)
            frame4 = image(entry4)
            if frame4.size != (1472, 896) or frame2.size != (736, 448):
                raise AssertionError(f"{name}[{index}]: unexpected frame size")
            assert_equal_image(
                frame2,
                frame4.resize(frame2.size, Image.Resampling.LANCZOS),
                f"{name}[{index}]",
            )
        checks.append({"scene": name, "frames": len(hd4), "status": "PASS"})

    mentat2 = read_pack(DATA / "sdl_mentat_hd2.dat")
    mentat4 = read_pack(DATA / "sdl_mentat_hd4.dat")
    for name, ids in MENTATS.items():
        background4 = image(mentat4[ids["background"]])
        if background4.size != (2560, 1920):
            raise AssertionError(f"{name}: background is not HD4")
        identity_metrics = assert_atreides_mentat_identity(background4) if name == "atreides" else {}
        for resource_id in (ids["background"], ids["eyes"], ids["mouth"]):
            frame2 = image(mentat2[resource_id])
            frame4 = image(mentat4[resource_id])
            assert_equal_image(
                frame2,
                frame4.resize(frame2.size, Image.Resampling.LANCZOS),
                f"{name} resource {resource_id}",
            )
        eye = image(mentat4[ids["eyes"]])
        opaque_pixels = sum(1 for alpha in eye.getchannel("A").get_flattened_data() if alpha >= 245)
        if opaque_pixels < eye.width * eye.height // 30:
            raise AssertionError(f"{name}: closed-eye overlay is too transparent")
        if name == "atreides":
            alpha_bbox = eye.getchannel("A").getbbox()
            if alpha_bbox is None or alpha_bbox[3] > 100:
                raise AssertionError(
                    f"atreides: eye animation mask leaks into cheeks: {alpha_bbox}"
                )
            mouth_metrics = assert_atreides_mouth_registration(
                background4,
                image(mentat4[ids["mouth"]]),
            )
        else:
            mouth_metrics = {}
        checks.append({
            "mentat": name,
            "closed_eye_opaque_pixels": opaque_pixels,
            **identity_metrics,
            **mouth_metrics,
            "status": "PASS",
        })

    contact = render_scene_contact_sheet()
    previews = render_mentat_previews()
    report = {
        "status": "PASS",
        "checks": checks,
        "contact_sheet": str(contact),
        "previews": [str(path) for path in previews],
    }
    report_path = ARTIFACT / "campaign_hd_audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(SCENES)} scene packs, {len(MENTATS)} mentats; report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
