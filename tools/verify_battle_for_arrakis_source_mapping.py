#!/usr/bin/env python3
"""Regression checks for Sega sheet direction-cell mapping."""

from __future__ import annotations

from PIL import ImageChops

from build_battle_for_arrakis_world import (
    crop_cell,
    extract_large_row,
    source,
)


def assert_same(actual, expected, label: str) -> None:
    if actual.size != expected.size or ImageChops.difference(actual, expected).getbbox():
        raise AssertionError(label)


def main() -> None:
    # The tank/siege sheets reserve cell 0 for the IDLE label and store the
    # eight direction sprites in cells 1..8. Source direction 2 is East and
    # therefore becomes D2TM atlas column 0.
    for filename in ("550029_combat_tank.png", "550030_siege_tank.png"):
        sheet = source(filename)
        actual_body_east = extract_large_row(
            filename,
            "ATREIDES",
            88,
            576,
        )[0]
        expected_body_east = crop_cell(sheet, 40 + 2 * 32, 88)
        assert_same(
            actual_body_east,
            expected_body_east,
            f"{filename}: East body is shifted by the IDLE label cell",
        )

        actual_turret_east = extract_large_row(
            filename,
            "ATREIDES",
            56,
            576,
        )[0]
        expected_turret_east = crop_cell(sheet, 40 + 2 * 32, 56)
        assert_same(
            actual_turret_east,
            expected_turret_east,
            f"{filename}: East turret is shifted by the IDLE label cell",
        )

    # Sheets without IDLE/FIRE groups begin directly at x=8.
    mcv = source("550068_mcv.png")
    assert_same(
        extract_large_row("550068_mcv.png", "ATREIDES", 56)[0],
        crop_cell(mcv, 8 + 2 * 32, 56),
        "MCV: simple eight-direction row mapping changed",
    )
    print("Battle for Arrakis direction-cell mapping: OK")


if __name__ == "__main__":
    main()
