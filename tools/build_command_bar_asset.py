from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "source_references" / "command_bar_bronze_reference.png"
MASTER = ROOT / "resources" / "hd" / "master4" / "command_bar.png"
HD4 = ROOT / "resources" / "bin" / "data" / "hd4" / "command_bar.png"
HD2 = ROOT / "resources" / "bin" / "data" / "hd2" / "command_bar.png"

EXPECTED_SOURCE_SIZE = (2804, 561)
MASTER_SIZE = (2800, 344)


def fill_from_nearby_dark_rows(
    image: Image.Image,
    target: tuple[int, int, int, int],
    sample_x_ranges: tuple[tuple[int, int], ...],
) -> None:
    pixels = image.load()
    x0, y0, x1, y1 = target
    for y in range(y0, y1):
        samples = []
        for sample_x0, sample_x1 in sample_x_ranges:
            for x in range(max(0, sample_x0), min(image.width, sample_x1)):
                color = pixels[x, y]
                if sum(color[:3]) < 135:
                    samples.append(color)
        if not samples:
            samples = [(10, 11, 10, 255)]
        samples.sort(key=lambda color: sum(color[:3]))
        color = samples[len(samples) // 2]
        for x in range(x0, x1):
            pixels[x, y] = color


def clean_label(image: Image.Image, slot_x: int) -> None:
    fill_from_nearby_dark_rows(
        image,
        (slot_x + 35, 370, slot_x + 365, 430),
        ((slot_x + 28, slot_x + 35), (slot_x + 365, slot_x + 372)),
    )


def clean_hotkey(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    width = x1 - x0
    fill_from_nearby_dark_rows(
        image,
        box,
        ((max(0, x0 - width), max(0, x0 - 8)), (min(image.width, x1 + 8), min(image.width, x1 + width))),
    )


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != EXPECTED_SOURCE_SIZE:
        raise ValueError(f"Unexpected command bar reference size: {source.size}")

    for slot_x in range(0, 2800, 400):
        clean_label(source, slot_x)

    for box in (
        (312, 140, 442, 214),
        (713, 140, 854, 214),
        (1155, 140, 1234, 214),
        (1553, 140, 1630, 214),
        (1951, 140, 2031, 214),
        (2242, 140, 2401, 214),
        (2715, 140, 2800, 214),
    ):
        clean_hotkey(source, box)

    master = source.crop((2, 115, 2802, 459)).resize(MASTER_SIZE, Image.Resampling.LANCZOS)
    for path in (MASTER, HD4):
        path.parent.mkdir(parents=True, exist_ok=True)
        master.save(path, optimize=True)

    HD2.parent.mkdir(parents=True, exist_ok=True)
    master.resize((1400, 172), Image.Resampling.LANCZOS).save(HD2, optimize=True)


if __name__ == "__main__":
    main()
