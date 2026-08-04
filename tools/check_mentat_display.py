#!/usr/bin/env python3
"""Fast regression check for the remastered post-House Mentat screen."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import ImageFont


ROOT = Path(__file__).resolve().parents[1]
SAFE_TEXT_WIDTH = 640 - 2 * 18


def main() -> int:
    failures: list[str] = []
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
    print("PASS: Mentat uses physical HD presentation and width-aware text layout")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
