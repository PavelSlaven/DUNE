#!/usr/bin/env python3
"""Build an approval-ready HD4 siege-tank preview."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

import prepare_tank_review as tank


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "siege_tank_review_v1"
GENERATED = OUTPUT / "generated"
BODY_RAW = GENERATED / "siege_body_raw.png"
TOP_RAW = GENERATED / "siege_turret_raw.png"
BODY_NE_RAW = GENERATED / "siege_body_NE_raw.png"
TOP_NE_RAW = GENERATED / "siege_turret_NE_raw.png"
BODY_ALPHA = GENERATED / "siege_body_alpha.png"
TOP_ALPHA = GENERATED / "siege_turret_alpha.png"
BODY_NE_ALPHA = GENERATED / "siege_body_NE_alpha.png"
TOP_NE_ALPHA = GENERATED / "siege_turret_NE_alpha.png"
TOP_DIRECTION_RAW = {
    "E": GENERATED / "siege_turret_E_raw.png",
    "NE": TOP_NE_RAW,
    "N": GENERATED / "siege_turret_N_raw.png",
    "NW": GENERATED / "siege_turret_NW_raw.png",
    "W": GENERATED / "siege_turret_W_raw.png",
    "SW": GENERATED / "siege_turret_SW_raw.png",
    "S": GENERATED / "siege_turret_S_raw.png",
    "SE": GENERATED / "siege_turret_SE_raw.png",
}

CLASSIC_BODY = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0151_UNIT_SIEGEBASE.png"
)
CLASSIC_TOP = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0153_UNIT_SIEGETOP.png"
)

LOGICAL_FRAME = (36, 38)
HD4_FRAME = (144, 152)
HD4_ATLAS = (1152, 152)
PIVOT = (72, 76)
# The E/W cannon muzzles are the limiting frames.  Values above 0.90 enter
# the two-pixel linear-filter guard band, so the final enlargement happens
# through the shared runtime destination rectangle instead.
TOP_EXTENT_SCALE = 0.90
# ImageGen's actual camera directions, determined from the gun muzzles:
# cell 7=E, 6=N, 5=NW, 4=W, 0=SW, 2=S, 3=SE.
# NE is rendered separately because the first grid duplicated SE.
SOURCE_WITH_NE_TO_D2TM = (7, None, 6, 5, 4, 0, 2, 3)

BODY4 = OUTPUT / "UNIT_SIEGEBASE_HD4_PREVIEW.png"
BODY2 = OUTPUT / "UNIT_SIEGEBASE_HD2_PREVIEW.png"
BODY_MASK = OUTPUT / "HM_UNIT_SIEGEBASE_HD4_PREVIEW.png"
SHADOW4 = OUTPUT / "UNIT_SIEGEBASE_SHADOW_HD4_PREVIEW.png"
TOP4 = OUTPUT / "UNIT_SIEGETOP_HD4_PREVIEW.png"
TOP2 = OUTPUT / "UNIT_SIEGETOP_HD2_PREVIEW.png"
TOP_MASK = OUTPUT / "HM_UNIT_SIEGETOP_HD4_PREVIEW.png"
REVIEW = OUTPUT / "UNIT_SIEGETANK_REVIEW.png"
ANIMATION = OUTPUT / "UNIT_SIEGETANK_TURRET_ROTATION.gif"


def remove_connected_chroma(
    image: Image.Image,
    columns: int = 4,
    rows: int = 2,
) -> Image.Image:
    """Remove only green-key pixels connected to a cell border."""
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    cell_width = image.width // columns
    cell_height = image.height // rows
    result = np.zeros_like(rgba)
    for row in range(rows):
        for column in range(columns):
            x0 = column * cell_width
            y0 = row * cell_height
            cell = rgba[y0:y0 + cell_height, x0:x0 + cell_width].copy()
            rgb = cell[:, :, :3].astype(np.int16)
            green_key = (
                (rgb[:, :, 1] > 175)
                & (rgb[:, :, 1] > rgb[:, :, 0] * 1.55)
                & (rgb[:, :, 1] > rgb[:, :, 2] * 1.55)
            )
            labels, count = ndimage.label(green_key)
            border_labels = np.unique(
                np.concatenate(
                    (
                        labels[0],
                        labels[-1],
                        labels[:, 0],
                        labels[:, -1],
                    )
                )
            )
            background = np.isin(labels, border_labels[border_labels > 0])
            background = ndimage.binary_dilation(background, iterations=1)
            cell[background] = 0

            alpha = cell[:, :, 3]
            edge = (alpha > 0) & ndimage.binary_dilation(background, iterations=2)
            green_excess = np.maximum(
                0,
                cell[:, :, 1].astype(np.int16)
                - np.maximum(cell[:, :, 0], cell[:, :, 2]).astype(np.int16),
            )
            spill = edge & (green_excess > 45)
            neutral_green = (
                cell[:, :, 0].astype(np.int16)
                + cell[:, :, 2].astype(np.int16)
            ) // 2
            cell[:, :, 1][spill] = np.clip(
                neutral_green[spill] + 20,
                0,
                255,
            ).astype(np.uint8)
            result[y0:y0 + cell_height, x0:x0 + cell_width] = cell
    return Image.fromarray(result, "RGBA")


def configure_shared_builder() -> None:
    tank.FRAME = HD4_FRAME
    tank.ATLAS = HD4_ATLAS
    tank.PIVOT = PIVOT
    tank.CLASSIC_BODY = CLASSIC_BODY
    tank.CLASSIC_TOP = CLASSIC_TOP
    tank.CLASSIC_EXTENT_SCALE = 0.96
    tank.BODY_OUT = BODY4
    tank.BODY_MASK_OUT = BODY_MASK
    tank.SHADOW_OUT = SHADOW4
    tank.TOP_OUT = TOP4
    tank.TOP_MASK_OUT = TOP_MASK
    tank.REVIEW_OUT = REVIEW
    tank.ANIMATION_OUT = ANIMATION

    def classic_frame(atlas: Image.Image, index: int) -> Image.Image:
        return atlas.crop(
            (
                index * LOGICAL_FRAME[0],
                0,
                (index + 1) * LOGICAL_FRAME[0],
                LOGICAL_FRAME[1],
            )
        )

    tank.classic_atlas_frame = classic_frame


def reordered_frames(
    image: Image.Image,
    north_east: Image.Image,
) -> list[Image.Image]:
    cells = tank.grid_frames(image)
    ne_subject = tank.single_subject(north_east)
    return [
        ne_subject if index is None else cells[index]
        for index in SOURCE_WITH_NE_TO_D2TM
    ]


def full_resolution_turret_frames() -> list[Image.Image]:
    frames = []
    for direction in tank.DIRECTIONS:
        source = TOP_DIRECTION_RAW[direction]
        alpha = remove_connected_chroma(
            Image.open(source),
            columns=1,
            rows=1,
        )
        alpha.save(
            GENERATED / f"siege_turret_{direction}_alpha.png",
            optimize=True,
        )
        frames.append(tank.single_subject(alpha))
    return frames


def frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop(
        (
            index * HD4_FRAME[0],
            0,
            (index + 1) * HD4_FRAME[0],
            HD4_FRAME[1],
        )
    )


def normalize_turret_once(
    atlas: Image.Image,
    classic: Image.Image,
) -> Image.Image:
    """Match classic extents with one resampling pass per direction."""
    normalized = Image.new("RGBA", HD4_ATLAS)
    for index in range(8):
        item = frame(atlas, index)
        current_forward, current_lateral = tank.oriented_extents(
            item,
            index,
        )
        classic_item = tank.classic_atlas_frame(classic, index)
        target_forward, target_lateral = tank.oriented_extents(
            classic_item,
            index,
        )
        target_forward *= 4.0 * TOP_EXTENT_SCALE
        target_lateral *= 4.0 * TOP_EXTENT_SCALE
        item = tank.transform_frame_axes(
            item,
            index,
            target_forward / current_forward,
            target_lateral / current_lateral,
        )
        normalized.alpha_composite(item, (index * HD4_FRAME[0], 0))
    return tank.clean_alpha(normalized)


def center_turret_without_resampling(atlas: Image.Image) -> Image.Image:
    """Translate turret hubs to the pivot without another blur pass."""
    centered = Image.new("RGBA", HD4_ATLAS)
    for index in range(8):
        item = frame(atlas, index)
        center_x, center_y = tank.turret_hub_center(item)
        offset_x = round(PIVOT[0] - center_x)
        offset_y = round(PIVOT[1] - center_y)
        centered.alpha_composite(
            item,
            (index * HD4_FRAME[0] + offset_x, offset_y),
        )
    return tank.clean_alpha(centered)


def restore_microcontrast(atlas: Image.Image) -> Image.Image:
    """Restore detail lost by the unavoidable HD-master downsampling."""
    alpha = atlas.getchannel("A")
    rgb = atlas.convert("RGB").filter(
        ImageFilter.UnsharpMask(radius=0.55, percent=85, threshold=2)
    )
    rgb.putalpha(alpha)
    return tank.clean_alpha(rgb)


def compose(
    body: Image.Image,
    body_mask: Image.Image,
    top: Image.Image,
    top_mask: Image.Image,
    body_direction: int,
    top_direction: int,
    color: tuple[int, int, int],
) -> Image.Image:
    tinted_body = tank.apply_engine_tint(body, body_mask, color)
    tinted_top = tank.apply_engine_tint(top, top_mask, color)
    result = frame(tinted_body, body_direction)
    result.alpha_composite(frame(tinted_top, top_direction))
    return result


def draw_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    size: int,
    label: str,
) -> None:
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle(
        (x, y, x + size, y + size + 34),
        radius=7,
        fill=(21, 25, 30, 255),
        outline=(139, 106, 48, 255),
        width=2,
    )
    shown = Image.new("RGBA", (size, size))
    scale = min(size / sprite.width, size / sprite.height)
    resized = sprite.resize(
        (round(sprite.width * scale), round(sprite.height * scale)),
        Image.Resampling.LANCZOS,
    )
    shown.alpha_composite(
        resized,
        ((size - resized.width) // 2, (size - resized.height) // 2),
    )
    board.alpha_composite(shown, (x, y))
    draw.text(
        (x + 8, y + size + 5),
        label,
        font=tank.font(17, True),
        fill=(232, 216, 180, 255),
    )


def build_review(
    body: Image.Image,
    body_mask: Image.Image,
    top: Image.Image,
    top_mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1780, 1260), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Осадный танк — корпус и двухствольная башня",
        font=tank.font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 70),
        "HD4: два независимых атласа 8×1; кадр 144×152",
        font=tank.font(19),
        fill=(188, 194, 202, 255),
    )
    for index, direction in enumerate(tank.DIRECTIONS):
        draw_card(
            board,
            compose(
                body,
                body_mask,
                top,
                top_mask,
                index,
                index,
                tank.HOUSE_COLORS["Ордос"],
            ),
            34 + index * 216,
            108,
            190,
            direction,
        )

    draw.text(
        (34, 350),
        "Независимое вращение башни — корпус направлен на север",
        font=tank.font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, direction in enumerate(tank.DIRECTIONS):
        draw_card(
            board,
            compose(
                body,
                body_mask,
                top,
                top_mask,
                2,
                index,
                tank.HOUSE_COLORS["Атрейдесы"],
            ),
            34 + index * 216,
            400,
            190,
            direction,
        )

    draw.text(
        (34, 642),
        "Цветовые маски Домов",
        font=tank.font(25, True),
        fill=(225, 188, 98, 255),
    )
    for column, (name, color) in enumerate(tank.HOUSE_COLORS.items()):
        draw_card(
            board,
            compose(body, body_mask, top, top_mask, 7, 2, color),
            34 + column * 318,
            692,
            280,
            name,
        )
    draw_card(board, frame(body_mask, 2), 988, 692, 280, "маска корпуса")
    draw_card(board, frame(top_mask, 2), 1306, 692, 280, "маска башни")

    draw.text(
        (34, 1071),
        "Контракт: 36×38 → HD4 144×152; порядок E, NE, N, NW, W, SW, S, SE",
        font=tank.font(24, True),
        fill=(225, 188, 98, 255),
    )
    classic_body = Image.open(CLASSIC_BODY).convert("RGBA")
    classic_top = Image.open(CLASSIC_TOP).convert("RGBA")
    classic = tank.classic_atlas_frame(classic_body, 2)
    classic.alpha_composite(tank.classic_atlas_frame(classic_top, 2))
    draw_card(board, classic, 34, 1112, 110, "классика N")
    draw_card(
        board,
        compose(
            body,
            body_mask,
            top,
            top_mask,
            2,
            2,
            tank.HOUSE_COLORS["Ордос"],
        ),
        180,
        1112,
        110,
        "HD4 N",
    )
    draw.text(
        (330, 1124),
        "• центр башни совпадает с посадочным кольцом корпуса\n"
        "• корпус и башня имеют 8 уникальных направлений\n"
        "• два ствола остаются параллельными и одинаковой длины\n"
        "• предпросмотр: в игру ещё не установлено",
        font=tank.font(21),
        fill=(204, 208, 214, 255),
        spacing=10,
    )
    return board


def validate(
    body: Image.Image,
    body_mask: Image.Image,
    top: Image.Image,
    top_mask: Image.Image,
) -> dict[str, object]:
    details: dict[str, object] = {}
    for name, image in (
        ("body", body),
        ("body_mask", body_mask),
        ("turret", top),
        ("turret_mask", top_mask),
    ):
        if image.size != HD4_ATLAS:
            raise AssertionError(f"{name}: неверный размер {image.size}")
        cells = [frame(image, index) for index in range(8)]
        if name in {"body", "turret"}:
            if len({cell.tobytes() for cell in cells}) != 8:
                raise AssertionError(f"{name}: направления не уникальны")
            for index, cell in enumerate(cells):
                box = cell.getchannel("A").getbbox()
                if box is None:
                    raise AssertionError(f"{name}: пустой кадр {index}")
                if box[0] < 2 or box[1] < 2 or box[2] > 142 or box[3] > 150:
                    raise AssertionError(f"{name}: кадр касается края {index}: {box}")
        details[name] = {
            "size": list(image.size),
            "non_empty_pixels": int(
                np.count_nonzero(np.asarray(image.getchannel("A")) > 8)
            ),
        }

    body_centers = []
    turret_centers = []
    for index in range(8):
        body_center = tank.visual_body_socket_center(frame(body, index))
        turret_center = tank.turret_hub_center(frame(top, index))
        body_centers.append([round(value, 2) for value in body_center])
        turret_centers.append([round(value, 2) for value in turret_center])
        if np.hypot(body_center[0] - PIVOT[0], body_center[1] - PIVOT[1]) > 2.0:
            raise AssertionError(f"корпус {index}: смещено посадочное кольцо")
        if np.hypot(turret_center[0] - PIVOT[0], turret_center[1] - PIVOT[1]) > 2.0:
            raise AssertionError(f"башня {index}: смещён центр вращения")
    details["body_socket_centers"] = body_centers
    details["turret_hub_centers"] = turret_centers
    return details


def main() -> int:
    configure_shared_builder()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    body_alpha = remove_connected_chroma(Image.open(BODY_RAW))
    top_alpha = remove_connected_chroma(Image.open(TOP_RAW))
    body_ne_alpha = remove_connected_chroma(
        Image.open(BODY_NE_RAW),
        columns=1,
        rows=1,
    )
    top_ne_alpha = remove_connected_chroma(
        Image.open(TOP_NE_RAW),
        columns=1,
        rows=1,
    )
    body_alpha.save(BODY_ALPHA, optimize=True)
    top_alpha.save(TOP_ALPHA, optimize=True)
    body_ne_alpha.save(BODY_NE_ALPHA, optimize=True)
    top_ne_alpha.save(TOP_NE_ALPHA, optimize=True)

    body_cells = reordered_frames(body_alpha, body_ne_alpha)
    top_cells = full_resolution_turret_frames()
    body = tank.assemble(
        body_cells,
        [tank.body_pivot(cell) for cell in body_cells],
        normalize_each=True,
    )
    top = tank.assemble(
        top_cells,
        [tank.turret_pivot(cell) for cell in top_cells],
    )
    body = tank.normalize_atlas_to_classic(
        body,
        Image.open(CLASSIC_BODY).convert("RGBA"),
    )
    body = tank.center_body_turret_sockets(body)
    top = normalize_turret_once(
        top,
        Image.open(CLASSIC_TOP).convert("RGBA"),
    )
    top = center_turret_without_resampling(top)
    top = restore_microcontrast(top)
    neutral_body, body_mask = tank.neutral_and_mask(body)
    neutral_top, top_mask = tank.neutral_and_mask(top)
    shadow = tank.build_shadow(neutral_body)
    validation = validate(
        neutral_body,
        body_mask,
        neutral_top,
        top_mask,
    )

    neutral_body.save(BODY4, optimize=True)
    body_mask.save(BODY_MASK, optimize=True)
    shadow.save(SHADOW4, optimize=True)
    neutral_top.save(TOP4, optimize=True)
    top_mask.save(TOP_MASK, optimize=True)
    neutral_body.resize((576, 76), Image.Resampling.LANCZOS).save(
        BODY2,
        optimize=True,
    )
    neutral_top.resize((576, 76), Image.Resampling.LANCZOS).save(
        TOP2,
        optimize=True,
    )
    build_review(
        neutral_body,
        body_mask,
        neutral_top,
        top_mask,
    ).save(REVIEW, optimize=True)
    tank.build_animation(
        neutral_body,
        body_mask,
        neutral_top,
        top_mask,
    )

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "resources": {
            "body": {"id": 151, "name": "UNIT_SIEGEBASE"},
            "shadow": {"id": 152, "name": "UNIT_SIEGEBASE_SHADOW"},
            "turret": {"id": 153, "name": "UNIT_SIEGETOP"},
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd4_frame": list(HD4_FRAME),
        "direction_order": list(tank.DIRECTIONS),
        "source_grid_actual_order": [
            "SW",
            "SE duplicate",
            "S",
            "SE",
            "W",
            "NW",
            "N",
            "E",
        ],
        "north_east_rendered_separately": True,
        "full_resolution_turret_directions": list(tank.DIRECTIONS),
        "pivot_hd4": list(PIVOT),
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
