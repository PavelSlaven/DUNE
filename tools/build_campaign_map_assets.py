from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "style_reference" / "campaign_map_v1.png"
OUTPUTS = {
    4: (ROOT / "resources" / "bin" / "data" / "hd4" / "campaign_map.png", (2432, 960)),
    2: (ROOT / "resources" / "bin" / "data" / "hd2" / "campaign_map.png", (1216, 480)),
}


def crop_to_aspect(image: Image.Image, target_aspect: float) -> Image.Image:
    source_aspect = image.width / image.height
    if source_aspect > target_aspect:
        width = round(image.height * target_aspect)
        left = (image.width - width) // 2
        return image.crop((left, 0, left + width, image.height))
    height = round(image.width / target_aspect)
    top = (image.height - height) // 2
    return image.crop((0, top, image.width, top + height))


def main() -> None:
    with Image.open(SOURCE) as source:
        cropped = crop_to_aspect(source.convert("RGB"), 608 / 240)
        master_path, master_size = OUTPUTS[4]
        master_path.parent.mkdir(parents=True, exist_ok=True)
        master = cropped.resize(master_size, Image.Resampling.LANCZOS)
        master.save(master_path, optimize=True)

        hd2_path, hd2_size = OUTPUTS[2]
        hd2_path.parent.mkdir(parents=True, exist_ok=True)
        master.resize(hd2_size, Image.Resampling.LANCZOS).save(
            hd2_path,
            optimize=True,
        )


if __name__ == "__main__":
    main()
