#!/usr/bin/env python3
"""Build the second approval-ready HD4 combat-tank preview."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

import prepare_tank_review as tank


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "tank_review_v2"
BODY_SOURCE = OUTPUT / "tankbase_alpha.png"
TOP_SOURCE = OUTPUT / "tanktop_alpha.png"

BODY_OUT = OUTPUT / "UNIT_TANKBASE_HD4_PREVIEW.png"
BODY_MASK_OUT = OUTPUT / "HM_UNIT_TANKBASE_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "UNIT_TANKBASE_SHADOW_HD4_PREVIEW.png"
TOP_OUT = OUTPUT / "UNIT_TANKTOP_HD4_PREVIEW.png"
TOP_MASK_OUT = OUTPUT / "HM_UNIT_TANKTOP_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_TANK_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_TANK_TURRET_ROTATION_PREVIEW.gif"
BODY_ALIGNMENT_OUT = OUTPUT / "UNIT_TANKBASE_ALIGNMENT_REFERENCE.png"

# ImageGen follows the six-view arrangement of the supplied reference.
# Reorder it into D2TM's fixed E, NE, N, NW, W, SW, S, SE contract.
SOURCE_TO_D2TM = (0, 5, 6, 7, 4, 1, 2, 3)


def reordered_grid(path: Path) -> list[Image.Image]:
    cells = tank.grid_frames(Image.open(path).convert("RGBA"))
    return [cells[index] for index in SOURCE_TO_D2TM]


def shift_atlas_frame(
    atlas: Image.Image,
    index: int,
    offset_x: int,
    offset_y: int,
) -> Image.Image:
    shifted = Image.new("RGBA", tank.ATLAS)
    for frame_index in range(8):
        frame = tank.atlas_frame(atlas, frame_index)
        x = frame_index * tank.FRAME[0]
        y = 0
        if frame_index == index:
            x += offset_x
            y += offset_y
        shifted.alpha_composite(frame, (x, y))
    return tank.clean_alpha(shifted)


def main() -> int:
    for path in (BODY_SOURCE, TOP_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    body_cells = reordered_grid(BODY_SOURCE)
    top_cells = reordered_grid(TOP_SOURCE)

    body = tank.assemble(
        body_cells,
        [tank.body_pivot(cell) for cell in body_cells],
        normalize_each=True,
    )
    top = tank.assemble(
        top_cells,
        [tank.turret_pivot(cell) for cell in top_cells],
    )

    classic_body = Image.open(tank.CLASSIC_BODY).convert("RGBA")
    classic_top = Image.open(tank.CLASSIC_TOP).convert("RGBA")
    body = tank.normalize_atlas_to_classic(body, classic_body)
    body = tank.center_body_turret_sockets(body)
    # Neutralizing the generated SW armour changes the visual socket
    # detector's center by four HD pixels. Compensate in the body layer only;
    # the turret remains fixed at the shared (64, 64) pivot.
    body = shift_atlas_frame(body, 5, 4, 0)
    top = tank.normalize_atlas_to_classic(top, classic_top)
    top = tank.center_turret_hubs(top)

    body.save(BODY_ALIGNMENT_OUT, optimize=True)
    neutral_body, body_mask = tank.neutral_and_mask(body)
    neutral_top, top_mask = tank.neutral_and_mask(top)
    shadow = tank.build_shadow(neutral_body)
    validation = tank.validate(
        neutral_body,
        body_mask,
        shadow,
        neutral_top,
        top_mask,
    )

    neutral_body.save(BODY_OUT, optimize=True)
    body_mask.save(BODY_MASK_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    neutral_top.save(TOP_OUT, optimize=True)
    top_mask.save(TOP_MASK_OUT, optimize=True)
    neutral_body.resize((512, 64), Image.Resampling.LANCZOS).save(
        OUTPUT / "UNIT_TANKBASE_HD2_PREVIEW.png",
        optimize=True,
    )
    neutral_top.resize((512, 64), Image.Resampling.LANCZOS).save(
        OUTPUT / "UNIT_TANKTOP_HD2_PREVIEW.png",
        optimize=True,
    )

    tank.ANIMATION_OUT = ANIMATION_OUT
    tank.build_review(
        neutral_body,
        body_mask,
        neutral_top,
        top_mask,
    ).save(REVIEW_OUT, optimize=True)
    tank.build_animation(
        neutral_body,
        body_mask,
        neutral_top,
        top_mask,
    )

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.jpg"),
        "source_grid_order": [
            "E",
            "SW",
            "S",
            "SE",
            "W",
            "NE",
            "N",
            "NW",
        ],
        "direction_order": list(tank.DIRECTIONS),
        "body_source": str(BODY_SOURCE),
        "turret_source": str(TOP_SOURCE),
        "body_alignment_reference": str(BODY_ALIGNMENT_OUT),
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
