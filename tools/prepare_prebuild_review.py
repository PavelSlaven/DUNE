from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "prebuild_review_v1"
KIT_PATH = OUT / "construction_kit_alpha.png"
CLASSIC_CONTACT = ROOT / "artifacts" / "prebuild_classic_contact.png"

HD4_SIZES = {
    "BUILD_PRE_1X1": (128, 128),
    "BUILD_PRE_2X2": (256, 256),
    "BUILD_PRE_3X2": (384, 256),
    "BUILD_PRE_3X3": (384, 384),
}

RESOURCE_IDS = {
    "BUILD_PRE_1X1": (17, 18),
    "BUILD_PRE_2X2": (19, 20),
    "BUILD_PRE_3X2": (21, 22),
    "BUILD_PRE_3X3": (23, 24),
}

# Bboxes are taken from the four isolated components generated for this kit.
COMPONENT_BBOXES = {
    "vertical_truss": (265, 92, 370, 511),
    "horizontal_truss": (685, 274, 1056, 420),
    "single_crate": (198, 794, 426, 1074),
    "crate_cluster": (616, 722, 1129, 1147),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def alpha_trim(image: Image.Image) -> Image.Image:
    alpha_bbox = image.getchannel("A").getbbox()
    if alpha_bbox is None:
        raise ValueError("Component has no visible pixels")
    return image.crop(alpha_bbox)


def resize_width(image: Image.Image, width: int) -> Image.Image:
    height = max(1, round(image.height * width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def resize_height(image: Image.Image, height: int) -> Image.Image:
    width = max(1, round(image.width * height / image.height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def crop_height(image: Image.Image, height: int, from_bottom: bool = False) -> Image.Image:
    if height >= image.height:
        return image.copy()
    y = image.height - height if from_bottom else 0
    return image.crop((0, y, image.width, y + height))


def paste(canvas: Image.Image, image: Image.Image, x: int, y: int) -> None:
    canvas.alpha_composite(image, (x, y))


def build_components() -> dict[str, Image.Image]:
    kit = Image.open(KIT_PATH).convert("RGBA")
    return {
        name: alpha_trim(kit.crop(bbox))
        for name, bbox in COMPONENT_BBOXES.items()
    }


def compose_1x1(c: dict[str, Image.Image]) -> Image.Image:
    out = Image.new("RGBA", HD4_SIZES["BUILD_PRE_1X1"], (0, 0, 0, 0))
    horizontal = resize_width(c["horizontal_truss"], 74)
    crate = resize_width(c["single_crate"], 52)
    paste(out, horizontal, 13, 25)
    paste(out, crate, 61, 48)
    return out


def compose_2x2(c: dict[str, Image.Image]) -> Image.Image:
    out = Image.new("RGBA", HD4_SIZES["BUILD_PRE_2X2"], (0, 0, 0, 0))
    vertical = resize_height(c["vertical_truss"], 91)
    short_vertical = crop_height(resize_height(c["vertical_truss"], 91), 69, True)
    horizontal = resize_width(c["horizontal_truss"], 95)
    cluster = resize_width(c["crate_cluster"], 116)
    paste(out, vertical, 29, 32)
    paste(out, short_vertical, 67, 94)
    paste(out, horizontal, 118, 43)
    paste(out, cluster, 104, 126)
    return out


def compose_3x2(c: dict[str, Image.Image]) -> Image.Image:
    out = Image.new("RGBA", HD4_SIZES["BUILD_PRE_3X2"], (0, 0, 0, 0))
    vertical = resize_height(c["vertical_truss"], 94)
    short_vertical = crop_height(vertical, 72, True)
    horizontal = resize_width(c["horizontal_truss"], 96)
    short_horizontal = horizontal.crop((13, 0, 86, horizontal.height))
    cluster = resize_width(c["crate_cluster"], 118)
    crate = resize_width(c["single_crate"], 53)

    paste(out, vertical, 25, 39)
    paste(out, short_vertical, 83, 125)
    paste(out, horizontal, 116, 30)
    paste(out, short_horizontal, 245, 105)
    paste(out, cluster, 165, 127)
    paste(out, crate, 313, 166)
    return out


def compose_3x3(c: dict[str, Image.Image]) -> Image.Image:
    out = Image.new("RGBA", HD4_SIZES["BUILD_PRE_3X3"], (0, 0, 0, 0))
    vertical = resize_height(c["vertical_truss"], 96)
    short_vertical = crop_height(vertical, 70, True)
    horizontal = resize_width(c["horizontal_truss"], 98)
    short_horizontal = horizontal.crop((12, 0, 84, horizontal.height))
    cluster = resize_width(c["crate_cluster"], 120)
    crate = resize_width(c["single_crate"], 53)
    crate_small = resize_width(c["single_crate"], 47)

    paste(out, vertical, 27, 40)
    paste(out, short_vertical, 76, 179)
    paste(out, horizontal, 112, 35)
    paste(out, short_horizontal, 226, 116)
    paste(out, vertical, 339, 253)
    paste(out, short_vertical, 124, 275)
    paste(out, cluster, 183, 218)
    paste(out, crate, 303, 63)
    paste(out, crate_small, 43, 270)
    return out


def make_shadow(asset: Image.Image) -> Image.Image:
    alpha = asset.getchannel("A")
    blurred = alpha.filter(ImageFilter.GaussianBlur(4))
    shadow_alpha = blurred.point(lambda value: round(value * 0.42))
    shifted_alpha = Image.new("L", asset.size, 0)
    shifted_alpha.paste(
        shadow_alpha.crop((0, 0, asset.width - 4, asset.height - 5)),
        (4, 5),
    )
    edge = ImageDraw.Draw(shifted_alpha)
    edge.rectangle((0, 0, asset.width - 1, 1), fill=0)
    edge.rectangle((0, asset.height - 2, asset.width - 1, asset.height - 1), fill=0)
    edge.rectangle((0, 0, 1, asset.height - 1), fill=0)
    edge.rectangle((asset.width - 2, 0, asset.width - 1, asset.height - 1), fill=0)
    shadow = Image.new("RGBA", asset.size, (7, 8, 10, 0))
    shadow.putalpha(shifted_alpha)
    return shadow


def make_metal_background(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (92, 94, 75))
    draw = ImageDraw.Draw(image)
    tile = 64
    for y in range(0, height, tile):
        for x in range(0, width, tile):
            color = (96, 98, 79) if ((x // tile) + (y // tile)) % 2 == 0 else (88, 90, 72)
            draw.rectangle((x, y, min(width - 1, x + tile), min(height - 1, y + tile)), fill=color)
            draw.line((x, y, min(width - 1, x + tile), y), fill=(130, 130, 104), width=2)
            draw.line((x, y, x, min(height - 1, y + tile)), fill=(130, 130, 104), width=2)
            draw.line(
                (x, min(height - 1, y + tile - 1), min(width - 1, x + tile), min(height - 1, y + tile - 1)),
                fill=(55, 57, 47),
                width=2,
            )
            draw.line(
                (min(width - 1, x + tile - 1), y, min(width - 1, x + tile - 1), min(height - 1, y + tile)),
                fill=(55, 57, 47),
                width=2,
            )
    return image.convert("RGBA")


def fit(image: Image.Image, max_size: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    return copy


def panel(
    sheet: Image.Image,
    asset: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    subtitle: str,
) -> None:
    x1, y1, x2, y2 = box
    draw = ImageDraw.Draw(sheet)
    draw.rounded_rectangle(box, radius=16, fill=(24, 27, 29), outline=(177, 134, 48), width=2)
    draw.text((x1 + 18, y1 + 14), title, font=font(24, True), fill=(237, 225, 197))
    draw.text((x1 + 18, y1 + 46), subtitle, font=font(16), fill=(174, 180, 177))
    viewport = (x1 + 18, y1 + 76, x2 - 18, y2 - 18)
    vw = viewport[2] - viewport[0]
    vh = viewport[3] - viewport[1]
    background = make_metal_background((vw, vh))
    scaled = fit(asset, (vw - 24, vh - 24))
    background.alpha_composite(
        scaled,
        ((vw - scaled.width) // 2, (vh - scaled.height) // 2),
    )
    sheet.alpha_composite(background, (viewport[0], viewport[1]))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_asset(name: str, hd4: Image.Image, hd2: Image.Image) -> dict[str, object]:
    expected = HD4_SIZES[name]
    if hd4.size != expected:
        raise ValueError(f"{name}: expected {expected}, got {hd4.size}")
    if hd2.size != (expected[0] // 2, expected[1] // 2):
        raise ValueError(f"{name}: invalid HD2 size {hd2.size}")
    bbox = hd4.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"{name}: empty image")
    if bbox[0] <= 1 or bbox[1] <= 1 or bbox[2] >= expected[0] - 1 or bbox[3] >= expected[1] - 1:
        raise ValueError(f"{name}: visible pixels touch the frame boundary: {bbox}")
    magenta_pixels = 0
    pixels = hd4.load()
    for y in range(hd4.height):
        for x in range(hd4.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha > 16 and red > 180 and blue > 180 and green < 80:
                magenta_pixels += 1
    if magenta_pixels:
        raise ValueError(f"{name}: {magenta_pixels} visible chroma-key pixels remain")
    recreated = hd4.resize(hd2.size, Image.Resampling.LANCZOS)
    if recreated.tobytes() != hd2.tobytes():
        raise ValueError(f"{name}: HD2 is not an exact Lanczos derivative")
    return {
        "hd4_size": list(hd4.size),
        "hd2_size": list(hd2.size),
        "visible_bbox_hd4": list(bbox),
    }


def build_review(assets: dict[str, Image.Image]) -> Path:
    sheet = Image.new("RGBA", (1600, 1240), (12, 14, 16, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((54, 34), "СТРОЙПЛОЩАДКИ — HD4, ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР", font=font(34, True), fill=(241, 224, 183))
    draw.text(
        (54, 80),
        "Композиции собраны по реальным размерам атласа. Фон прозрачен и в игровые ресурсы не входит.",
        font=font(20),
        fill=(180, 187, 185),
    )

    boxes = {
        "BUILD_PRE_1X1": (48, 132, 420, 500),
        "BUILD_PRE_2X2": (438, 132, 810, 500),
        "BUILD_PRE_3X2": (828, 132, 1552, 500),
        "BUILD_PRE_3X3": (48, 524, 772, 1148),
    }
    titles = {
        "BUILD_PRE_1X1": "1×1 — ID 17",
        "BUILD_PRE_2X2": "2×2 — ID 19",
        "BUILD_PRE_3X2": "3×2 — ID 21",
        "BUILD_PRE_3X3": "3×3 — ID 23",
    }
    for name, box in boxes.items():
        panel(sheet, assets[name], box, titles[name], f"HD4 {assets[name].width}×{assets[name].height}")

    kit_box = (796, 524, 1552, 1148)
    draw.rounded_rectangle(kit_box, radius=16, fill=(24, 27, 29), outline=(177, 134, 48), width=2)
    draw.text((818, 542), "ЕДИНЫЙ НАБОР ДЕТАЛЕЙ", font=font(24, True), fill=(237, 225, 197))
    draw.text(
        (818, 576),
        "Крупные площадки дорисованы компоновкой деталей,\nа не растягиванием малого спрайта.",
        font=font(17),
        fill=(174, 180, 177),
        spacing=5,
    )
    kit = Image.open(OUT / "construction_kit_alpha.png").convert("RGBA")
    kit_scaled = fit(kit, (700, 420))
    kit_background = make_metal_background((700, 420))
    kit_background.alpha_composite(
        kit_scaled,
        ((700 - kit_scaled.width) // 2, (420 - kit_scaled.height) // 2),
    )
    sheet.alpha_composite(kit_background, (824, 650))
    draw.text(
        (818, 1090),
        "Тени подготовлены отдельно. BUILD_PRE_CONST (ID 25) не меняется: движок его не использует.",
        font=font(15),
        fill=(164, 170, 168),
    )
    draw.text(
        (54, 1182),
        "СТАТУС: В ИГРУ НЕ УСТАНОВЛЕНО",
        font=font(22, True),
        fill=(231, 100, 79),
    )
    output = OUT / "BUILD_PREBUILD_REVIEW.png"
    sheet.convert("RGB").save(output, quality=94)
    return output


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    components = build_components()
    assets = {
        "BUILD_PRE_1X1": compose_1x1(components),
        "BUILD_PRE_2X2": compose_2x2(components),
        "BUILD_PRE_3X2": compose_3x2(components),
        "BUILD_PRE_3X3": compose_3x3(components),
    }

    validation: dict[str, object] = {}
    files: dict[str, dict[str, str]] = {}
    for name, hd4 in assets.items():
        hd2 = hd4.resize((hd4.width // 2, hd4.height // 2), Image.Resampling.LANCZOS)
        shadow_hd4 = make_shadow(hd4)
        shadow_hd2 = shadow_hd4.resize((hd4.width // 2, hd4.height // 2), Image.Resampling.LANCZOS)

        paths = {
            "hd4": OUT / f"{name}_HD4_PREVIEW.png",
            "hd2": OUT / f"{name}_HD2_PREVIEW.png",
            "shadow_hd4": OUT / f"{name}_SHADOW_HD4_PREVIEW.png",
            "shadow_hd2": OUT / f"{name}_SHADOW_HD2_PREVIEW.png",
        }
        hd4.save(paths["hd4"])
        hd2.save(paths["hd2"])
        shadow_hd4.save(paths["shadow_hd4"])
        shadow_hd2.save(paths["shadow_hd2"])
        validation[name] = validate_asset(name, hd4, hd2)
        files[name] = {key: str(path.relative_to(ROOT)) for key, path in paths.items()}

    review = build_review(assets)
    manifest = {
        "status": "preview_not_integrated",
        "source_kit": str(KIT_PATH.relative_to(ROOT)),
        "source_kit_sha256": sha256(KIT_PATH),
        "classic_reference": str(CLASSIC_CONTACT.relative_to(ROOT)),
        "density": {
            "HD4": "master",
            "HD2": "deterministic Lanczos downscale from HD4",
        },
        "resources": {
            name: {
                "resource_id": RESOURCE_IDS[name][0],
                "shadow_resource_id": RESOURCE_IDS[name][1],
                "files": files[name],
                **validation[name],
            }
            for name in assets
        },
        "unused_resource": {
            "name": "BUILD_PRE_CONST",
            "resource_id": 25,
            "action": "left_unchanged",
            "reason": "not referenced by current prebuild rendering path",
        },
        "review": str(review.relative_to(ROOT)),
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(review)


if __name__ == "__main__":
    main()
