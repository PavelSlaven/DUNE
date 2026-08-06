from pathlib import Path

from PIL import Image, ImageChops

from build_command_bar_asset import make_disabled


ROOT = Path(__file__).resolve().parents[1]
ASSET_PAIRS = (
    (
        ROOT / "resources" / "hd" / "master4" / "command_bar.png",
        ROOT / "resources" / "hd" / "master4" / "command_bar_disabled.png",
        (2800, 414),
    ),
    (
        ROOT / "resources" / "bin" / "data" / "hd4" / "command_bar.png",
        ROOT / "resources" / "bin" / "data" / "hd4" / "command_bar_disabled.png",
        (2800, 414),
    ),
)


def main() -> None:
    for bright_path, disabled_path, expected_size in ASSET_PAIRS:
        bright = Image.open(bright_path).convert("RGBA")
        disabled = Image.open(disabled_path).convert("RGBA")
        if bright.size != expected_size or disabled.size != expected_size:
            raise AssertionError(f"Unexpected command bar size: {bright_path}")
        if bright.width % 7 != 0:
            raise AssertionError(f"Command bar does not have seven equal cells: {bright_path}")
        alpha_difference = ImageChops.difference(
            bright.getchannel("A"),
            disabled.getchannel("A"),
        )
        if alpha_difference.getbbox() is not None:
            raise AssertionError(f"Command bar contours do not match: {bright_path}")
        expected_disabled = make_disabled(bright)
        if ImageChops.difference(expected_disabled, disabled).getbbox() is not None:
            raise AssertionError(
                f"Disabled command bar is not an exact darkened copy: {bright_path}"
            )

    print("Command bar assets: matching contours and seven equal cells")


if __name__ == "__main__":
    main()
