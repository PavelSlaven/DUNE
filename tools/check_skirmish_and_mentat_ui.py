#!/usr/bin/env python3
"""Fast regression checks for the localized skirmish and Mentat layouts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIRMISH_SOURCE = ROOT / "src" / "gamestates" / "cSetupSkirmishState.cpp"
MENTAT_SOURCE = ROOT / "src" / "mentat" / "AbstractMentat.cpp"
MAPS = ROOT / "resources" / "bin" / "skirmish"
MAX_MAP_TITLE_CHARACTERS = 13


def check_skirmish(failures: list[str]) -> None:
    source = SKIRMISH_SOURCE.read_text(encoding="utf-8")
    for abbreviation in ("Кр.", "Ком."):
        if abbreviation in source:
            failures.append(f"Skirmish header still contains {abbreviation!r}")
    for label in ("Игрок", "Дом", "Кредиты", "Войска", "Команда"):
        if f'"{label}"' not in source:
            failures.append(f"Skirmish header is missing {label!r}")
    if "SkirmishPlayerTableLayout" not in source:
        failures.append("Skirmish rows and headers do not share one column layout")

    for path in sorted(MAPS.glob("*.ini")):
        text = path.read_text(encoding="utf-8-sig")
        match = re.search(r'^Title="(.*)"$', text, flags=re.MULTILINE)
        if not match:
            failures.append(f"{path.name}: no Title entry")
            continue
        title = match.group(1)
        if len(title) > MAX_MAP_TITLE_CHARACTERS:
            failures.append(
                f"{path.name}: {title!r} has {len(title)} characters, "
                f"maximum is {MAX_MAP_TITLE_CHARACTERS}"
            )


def check_mentat_header(failures: list[str]) -> None:
    source = MENTAT_SOURCE.read_text(encoding="utf-8")
    expected_rect = "baseRect(20, 6, 600, 78)"
    if expected_rect not in source:
        failures.append(f"Mentat text area is not the expanded {expected_rect}")
    if "drawHdTextHeader();" not in source:
        failures.append("Mentat draw path does not install the shared HD text header")
    if "gfxmentat->getTexture(MENTATA)" not in source:
        failures.append("Mentat HD text header does not reuse the Atreides frame")
    if "HD_MENTAT_TEXT_HEADER_HEIGHT = 90" not in source:
        failures.append("Mentat shared HD text header has an unexpected height")


def main() -> int:
    failures: list[str] = []
    check_skirmish(failures)
    check_mentat_header(failures)
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        "PASS: skirmish columns use full labels, every map title is at most "
        "13 characters, and all Mentat headers share the expanded frame"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
