#!/usr/bin/env python3
"""Build and pack the remastered campaign House-selection emblems."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME_DATA = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data")
ARTIFACT = ROOT / "artifacts" / "campaign_house_select_v2"
SOURCE_DIR = ARTIFACT / "generated"
OUTPUT_DATA = ARTIFACT / "data"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_inter"

HD4_SIZE = (360, 392)
HD2_SIZE = (180, 196)
HOUSE_RESOURCES = {
    11: ("Atreides", "BMP_SELECT_HOUSE_ATREIDES", "atreides.png"),
    12: ("Harkonnen", "BMP_SELECT_HOUSE_HARKONNEN", "harkonnen.png"),
    13: ("Ordos", "BMP_SELECT_HOUSE_ORDOS", "ordos.png"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_master(source_path: Path) -> Image.Image:
    with Image.open(source_path) as source:
        source = source.convert("RGB")
        square = source.resize((360, 360), Image.Resampling.LANCZOS)

    # The legacy contract is 90x98. Keep the new square medallion undistorted
    # and use its dark graphite corner colour for the vertical padding.
    corners = (
        square.getpixel((0, 0)),
        square.getpixel((359, 0)),
        square.getpixel((0, 359)),
        square.getpixel((359, 359)),
    )
    fill = tuple(sum(pixel[channel] for pixel in corners) // 4 for channel in range(3))
    canvas = Image.new("RGB", HD4_SIZE, fill)
    canvas.paste(square, (0, 16))
    return canvas.filter(ImageFilter.UnsharpMask(0.8, 72, 2)).convert("RGBA")


def replace_entry(entries: list[PackEntry], resource_id: int, image: Image.Image) -> None:
    old = entries[resource_id]
    expected_name = HOUSE_RESOURCES[resource_id][1]
    if old.name != expected_name:
        raise AssertionError(
            f"resource {resource_id} is {old.name}, expected {expected_name}"
        )
    entries[resource_id] = PackEntry(
        index=old.index,
        name=old.name,
        extension="PNG",
        payload=encode_png(image),
    )


def patch_pack(base: Path, output: Path, masters: dict[int, Image.Image], density: int) -> dict[str, object]:
    before = read_pack(base)
    after = list(before)
    expected_size = HD4_SIZE if density == 4 else HD2_SIZE
    for resource_id, master in masters.items():
        image = master if density == 4 else master.resize(HD2_SIZE, Image.Resampling.LANCZOS)
        replace_entry(after, resource_id, image)

    output.parent.mkdir(parents=True, exist_ok=True)
    write_pack(output, after)
    packed = read_pack(output)
    changed = [
        index
        for index, (old, new) in enumerate(zip(before, packed, strict=True))
        if (old.name, old.extension, old.payload) != (new.name, new.extension, new.payload)
    ]
    if changed != list(HOUSE_RESOURCES):
        raise AssertionError(f"unrelated resources changed: {changed}")
    for resource_id in HOUSE_RESOURCES:
        image = decode_image(packed[resource_id].payload)
        if image.size != expected_size:
            raise AssertionError(
                f"HD{density} resource {resource_id}: {image.size}, expected {expected_size}"
            )
    return {
        "file": str(output),
        "sha256": digest(output),
        "bytes": output.stat().st_size,
        "changed_ids": changed,
    }


def build_review(masters: dict[int, Image.Image]) -> None:
    board = Image.new("RGB", (1240, 490), (8, 12, 16))
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)
    for column, (resource_id, (label, _, _)) in enumerate(HOUSE_RESOURCES.items()):
        x = 40 + column * 400
        board.paste(masters[resource_id].convert("RGB"), (x, 38))
        text_width = draw.textbbox((0, 0), label, font=font)[2]
        draw.text(
            (x + (360 - text_width) // 2, 442),
            label,
            font=font,
            fill=(232, 213, 174),
        )
    board.save(ARTIFACT / "campaign_house_emblems_review.png", optimize=True)


def main() -> int:
    masters: dict[int, Image.Image] = {}
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    for resource_id, (_, resource_name, source_name) in HOUSE_RESOURCES.items():
        source_path = SOURCE_DIR / source_name
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        master = prepare_master(source_path)
        masters[resource_id] = master
        master.save(
            MASTER_DIR / f"{resource_id:04d}_{resource_name}.png",
            optimize=True,
        )

    builds = []
    for density in (2, 4):
        builds.append(
            patch_pack(
                GAME_DATA / f"sdl_inter_hd{density}.dat",
                OUTPUT_DATA / f"sdl_inter_hd{density}.dat",
                masters,
                density,
            )
        )

    # HD2 must remain the exact deterministic derivative of HD4.
    pack2 = read_pack(OUTPUT_DATA / "sdl_inter_hd2.dat")
    pack4 = read_pack(OUTPUT_DATA / "sdl_inter_hd4.dat")
    for resource_id in HOUSE_RESOURCES:
        image2 = decode_image(pack2[resource_id].payload).convert("RGBA")
        image4 = decode_image(pack4[resource_id].payload).convert("RGBA")
        expected = image4.resize(HD2_SIZE, Image.Resampling.LANCZOS)
        if ImageChops.difference(image2, expected).getbbox() is not None:
            raise AssertionError(f"HD2 resource {resource_id} is not derived from HD4")

    build_review(masters)
    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "resources": {
            str(resource_id): {
                "house": values[0],
                "name": values[1],
                "generated_source": str(SOURCE_DIR / values[2]),
            }
            for resource_id, values in HOUSE_RESOURCES.items()
        },
        "logical_size": [90, 98],
        "hd2_size": list(HD2_SIZE),
        "hd4_size": list(HD4_SIZE),
        "builds": builds,
    }
    (ARTIFACT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
