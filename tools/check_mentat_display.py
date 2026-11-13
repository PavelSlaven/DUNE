#!/usr/bin/env python3
"""Fast regression check for the remastered post-House Mentat screen."""

from __future__ import annotations

import re
import sys
import math
from pathlib import Path

from PIL import Image, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SAFE_TEXT_WIDTH = 640 - 2 * 18


def check_ordos_shoulder(failures: list[str]) -> int:
    source = (ROOT / "src" / "mentat" / "OrdosMentat.cpp").read_text(
        encoding="utf-8"
    )
    match = re.search(
        r"shoulderEdge\s*=\s*\{\{(?P<points>.*?)\}\};",
        source,
        flags=re.DOTALL,
    )
    if not match:
        failures.append("Ordos shoulder has no explicit curved movie-mask contour")
        return 0

    points = [
        (int(y), int(x))
        for y, x in re.findall(r"\{\s*(\d+)\s*,\s*(\d+)\s*\}", match["points"])
    ]
    if len(points) < 2:
        failures.append("Ordos shoulder contour needs at least two points")
        return 0
    if any(y2 <= y1 or x2 < x1 for (y1, x1), (y2, x2) in zip(points, points[1:])):
        failures.append("Ordos shoulder contour must progress down and to the right")
        return 0

    y_span = points[-1][0] - points[0][0]
    x_span = points[-1][1] - points[0][1]
    if y_span < 35 or x_span < 35:
        failures.append(
            f"Ordos shoulder contour is too short: {x_span}px across {y_span} rows"
        )

    interpolated_x: list[int] = []
    for (y1, x1), (y2, x2) in zip(points, points[1:]):
        for y in range(y1, y2):
            progress = (y - y1) / (y2 - y1)
            interpolated_x.append(math.floor(x1 + (x2 - x1) * progress + 0.5))

    longest_vertical_run = 0
    current_run = 0
    previous_x: int | None = None
    for x in interpolated_x:
        current_run = current_run + 1 if x == previous_x else 1
        longest_vertical_run = max(longest_vertical_run, current_run)
        previous_x = x
    if longest_vertical_run > 6:
        failures.append(
            "Ordos shoulder has a long vertical cut: "
            f"{longest_vertical_run} rows (expected at most 6)"
        )

    portrait_path = ROOT / "resources" / "hd" / "master4" / "sdl_mentat" / "0040_MENTAT_ORDOS.png"
    with Image.open(portrait_path) as portrait:
        if portrait.size != (2560, 1920):
            failures.append(
                f"Ordos HD portrait has unexpected dimensions: {portrait.size}"
            )
        shoulder_core = portrait.convert("RGB").crop((700, 1650, 1100, 1900))
        pixels = shoulder_core.load()
        green_dominant = sum(
            1
            for y in range(shoulder_core.height)
            for x in range(shoulder_core.width)
            if pixels[x, y][1] >= pixels[x, y][0] + 1
            and pixels[x, y][1] >= pixels[x, y][2] + 1
        )
        green_ratio = green_dominant / (shoulder_core.width * shoulder_core.height)
        if green_ratio < 0.70:
            failures.append(
                "Ordos lower shoulder exposes the blue/black UI panel: "
                f"only {green_ratio:.1%} of its core is green fabric"
            )
    return longest_vertical_run


def check_mission_select_panels(failures: list[str]) -> None:
    mentat_source = (ROOT / "src" / "mentat" / "AbstractMentat.cpp").read_text(
        encoding="utf-8"
    )
    if "drawHdMissionSelectFrame" in mentat_source:
        failures.append("Mission select still draws a floating runtime outline")

    assets = ROOT / "resources" / "hd" / "master4" / "sdl_mentat"
    panels = {
        "Atreides": (assets / "0037_MENTAT_ATREIDES.png", 2148),
        "Harkonnen": (assets / "0038_MENTAT_HARKONNEN.png", 2192),
        "Ordos": (assets / "0040_MENTAT_ORDOS.png", 2192),
    }
    for house, (path, center_x) in panels.items():
        with Image.open(path) as source:
            panel = source.convert("L")
        y = 1438
        left = center_x
        while left > 0 and panel.getpixel((left, y)) < 30:
            left -= 1
        right = center_x
        while right < panel.width - 1 and panel.getpixel((right, y)) < 30:
            right += 1
        inset_width = right - left - 1
        if not 400 <= inset_width <= 560:
            failures.append(
                f"{house} baked Missions panel has an invalid dark inset: "
                f"{inset_width}px (expected 400..560px)"
            )


def main() -> int:
    failures: list[str] = []
    ordos_vertical_run = check_ordos_shoulder(failures)
    check_mission_select_panels(failures)
    game_source = (ROOT / "src" / "cGame_logic.cpp").read_text(encoding="utf-8")
    presentation_body = game_source.split("bool cGame::useHdPresentation() const", 1)[1]
    presentation_body = presentation_body.split("Texture *cGame::ensureHdPresentationRenderTarget", 1)[0]
    if "GAME_TELLHOUSE" not in presentation_body:
        failures.append("GAME_TELLHOUSE bypasses the physical HD presentation target")

    font_path = ROOT / "resources" / "bin" / "data" / "RussoOne-Regular.ttf"
    font = ImageFont.truetype(str(font_path), 20)
    longest_text = ""
    longest_width = 0.0
    for briefing in (ROOT / "resources" / "bin" / "campaign" / "briefings").glob("mentat*.ini"):
        source = briefing.read_text(encoding="utf-8-sig")
        for value in re.findall(r'^Text="(.*)"$', source, flags=re.MULTILINE):
            width = font.getlength(value)
            if width > longest_width:
                longest_text = value
                longest_width = width
    if longest_width > SAFE_TEXT_WIDTH:
        mentat_source = (ROOT / "src" / "mentat" / "AbstractMentat.cpp").read_text(
            encoding="utf-8"
        )
        if "wrapMentatText" not in mentat_source:
            failures.append(
                "Mentat speech has no width-aware wrapping: "
                f"{longest_width:.0f}px > {SAFE_TEXT_WIDTH}px ({longest_text})"
            )

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        "PASS: Mentat uses physical HD presentation and width-aware text layout; "
        f"Ordos shoulder vertical run is {ordos_vertical_run} rows; "
        "Missions panels are baked into all House backgrounds"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
