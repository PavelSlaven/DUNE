from collections import deque
from pathlib import Path

from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "source_references" / "command_bar_color_reference.png"

MASTER_DIR = ROOT / "resources" / "hd" / "master4"
HD4_DIR = ROOT / "resources" / "bin" / "data" / "hd4"

EXPECTED_SOURCE_SIZE = (2172, 1294)
MASTER_SIZE = (2800, 414)
CELL_SIZE = (400, 414)

# The supplied sheet contains a bright row and a disabled reference row.
BRIGHT_CROP = (2, 205, 2169, 526)
BRIGHT_CELL_BOUNDARIES = (0, 339, 651, 949, 1244, 1552, 1851, 2167)


def remove_connected_white_background(image: Image.Image) -> Image.Image:
    """Remove only the near-white background connected to the crop boundary."""
    result = image.convert("RGBA")
    pixels = result.load()
    width, height = result.size
    background = bytearray(width * height)
    pending: deque[tuple[int, int]] = deque()

    def is_background(x: int, y: int) -> bool:
        red, green, blue, _ = pixels[x, y]
        return min(red, green, blue) >= 220 and max(red, green, blue) - min(red, green, blue) <= 28

    def enqueue(x: int, y: int) -> None:
        offset = y * width + x
        if not background[offset] and is_background(x, y):
            background[offset] = 1
            pending.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while pending:
        x, y = pending.popleft()
        if x > 0:
            enqueue(x - 1, y)
        if x + 1 < width:
            enqueue(x + 1, y)
        if y > 0:
            enqueue(x, y - 1)
        if y + 1 < height:
            enqueue(x, y + 1)

    for y in range(height):
        for x in range(width):
            if background[y * width + x]:
                red, green, blue, _ = pixels[x, y]
                pixels[x, y] = (red, green, blue, 0)
    return result


def prepare_row(
    source: Image.Image,
    crop: tuple[int, int, int, int],
    boundaries: tuple[int, ...],
) -> Image.Image:
    row = remove_connected_white_background(source.crop(crop))
    normalized = Image.new("RGBA", MASTER_SIZE, (0, 0, 0, 0))
    for index, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
        cell = row.crop((left, 0, right, row.height)).resize(
            CELL_SIZE,
            Image.Resampling.LANCZOS,
        )
        normalized.alpha_composite(cell, (index * CELL_SIZE[0], 0))
    return normalized


def save_asset(image: Image.Image, filename: str) -> None:
    for directory, size in (
        (MASTER_DIR, MASTER_SIZE),
        (HD4_DIR, MASTER_SIZE),
    ):
        directory.mkdir(parents=True, exist_ok=True)
        output = image if image.size == size else image.resize(size, Image.Resampling.LANCZOS)
        output.save(directory / filename, optimize=True)


def make_disabled(bright: Image.Image) -> Image.Image:
    disabled = ImageEnhance.Color(bright).enhance(0.72)
    disabled = ImageEnhance.Brightness(disabled).enhance(0.58)
    disabled.putalpha(bright.getchannel("A"))
    return disabled


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != EXPECTED_SOURCE_SIZE:
        raise ValueError(f"Unexpected command bar reference size: {source.size}")

    bright = prepare_row(source, BRIGHT_CROP, BRIGHT_CELL_BOUNDARIES)
    disabled = make_disabled(bright)

    save_asset(bright, "command_bar.png")
    save_asset(disabled, "command_bar_disabled.png")


if __name__ == "__main__":
    main()
