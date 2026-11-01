#!/usr/bin/env python3
"""Найти старые placements отрядов и собрать по ним новые одиночные атласы."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import correlate


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "tools/hd_assets.py").is_file())
sys.path.insert(0, str(ROOT / "tools"))
from hd_assets import decode_image, read_pack


CELL = 128
ATLAS_WIDTH = 1024
ATLAS_HEIGHT = 512
COLS = ATLAS_WIDTH // CELL
ROWS = ATLAS_HEIGHT // CELL
SQUADS = {
    "UNIT_SOLDIERS": "UNIT_SOLDIER",
    "UNIT_TROOPERS": "UNIT_TROOPER",
    "UNIT_TRIPLEFREMEN": "UNIT_TROOPER",
}
SINGLES = {
    "UNIT_SOLDIERS": "UNIT_SOLDIER",
    "UNIT_TROOPERS": "UNIT_TROOPER",
    "UNIT_TRIPLEFREMEN": "UNIT_SINGLEFREMEN",
}
ANCHOR = 64
SAND = (198, 174, 132, 255)
FONT_PATH = ROOT / "resources/bin/data/PTSansNarrow-Regular.ttf"


class SearchFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class Template:
    frame: int
    mask: np.ndarray
    bbox: tuple[int, int, int, int]
    total: int


def note(message: str, log_path: Path | None = None) -> None:
    print(message, flush=True)
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as stream:
            stream.write(message + "\n")


def parse_scale(path: Path) -> dict[str, float]:
    text = path.read_text(encoding="utf-8")
    # В таблице поля разделены буквальной последовательностью «\\t».
    text = text.replace("\\t", "\t")
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    scales: dict[str, float] = {}
    for row in reader:
        if not row.get("record") or not row.get("factor"):
            continue
        scales[row["record"]] = float(row["factor"])
    return scales


def old_atlases(pack_path: Path) -> dict[str, Image.Image]:
    wanted = set(SQUADS) | set(SQUADS.values()) | {"UNIT_SINGLEFREMEN"}
    found: dict[str, Image.Image] = {}
    for entry in read_pack(pack_path):
        if entry.name not in wanted:
            continue
        decoded = decode_image(entry.payload)
        if decoded is None:
            raise ValueError(f"пакетный элемент {entry.name} не является изображением")
        image = decoded.convert("RGBA")
        if image.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
            raise ValueError(f"старый атлас {entry.name}: ожидался 1024x512, получен {image.size}")
        found[entry.name] = image
    missing = wanted - set(found)
    if missing:
        raise ValueError("в старом пакете нет атласов: " + ", ".join(sorted(missing)))
    return found


def cell_alpha(image: Image.Image, k: int, r: int) -> np.ndarray:
    alpha = image.getchannel("A").crop(
        (k * CELL, r * CELL, (k + 1) * CELL, (r + 1) * CELL)
    )
    return np.asarray(alpha, dtype=np.uint8) > 0


def make_template(image: Image.Image, k: int, r: int) -> Template | None:
    mask = cell_alpha(image, k, r)
    rows, cols = np.nonzero(mask)
    if rows.size == 0:
        return None
    left = int(cols.min())
    top = int(rows.min())
    right = int(cols.max()) + 1
    bottom = int(rows.max()) + 1
    cropped = np.ascontiguousarray(mask[top:bottom, left:right])
    return Template(r, cropped, (left, top, right, bottom), int(cropped.sum()))


def correlate_counts(remaining: np.ndarray, template: np.ndarray) -> np.ndarray:
    # int64 нужен, потому что узкие целые переполняются на крупных пересечениях.
    # FFT-результат scipy округляет до целых счётчиков.
    counts = correlate(
        remaining.astype(np.int64, copy=False),
        template.astype(np.int64, copy=False),
        mode="full",
        method="fft",
    )
    if not np.issubdtype(counts.dtype, np.integer):
        raise TypeError(f"ожидались целые счётчики корреляции, получен {counts.dtype}")
    return counts


def best_location(
    remaining: np.ndarray,
    templates: list[Template],
) -> tuple[Template, int, int, int, int]:
    best: tuple[Template, int, int, int, int] | None = None
    for template in templates:
        counts = correlate_counts(remaining, template.mask)
        max_count = int(counts.max()) if counts.size else 0
        candidate_indexes = np.argwhere(counts == max_count)
        iy, ix = (int(value) for value in candidate_indexes[0])
        dy = iy - (template.mask.shape[0] - 1)
        dx = ix - (template.mask.shape[1] - 1)
        if best is None:
            best = (template, dx, dy, max_count, template.total)
            continue
        current_template, _, _, current_count, current_total = best
        lhs = max_count * current_total
        rhs = current_count * template.total
        if lhs > rhs or (lhs == rhs and max_count > current_count):
            best = (template, dx, dy, max_count, template.total)
    if best is None:
        raise SearchFailure("для кадра не нашёлся ни один непустой образец")
    return best


def remove_covered(remaining: np.ndarray, template: np.ndarray, dx: int, dy: int) -> None:
    h, w = template.shape
    dst_left = max(0, dx)
    dst_top = max(0, dy)
    dst_right = min(CELL, dx + w)
    dst_bottom = min(CELL, dy + h)
    if dst_left >= dst_right or dst_top >= dst_bottom:
        return
    src_left = dst_left - dx
    src_top = dst_top - dy
    src_right = src_left + (dst_right - dst_left)
    src_bottom = src_top + (dst_bottom - dst_top)
    overlap = template[src_top:src_bottom, src_left:src_right]
    remaining[dst_top:dst_bottom, dst_left:dst_right] &= ~overlap


def save_placements(folder: Path, payload: dict[str, Any]) -> None:
    path = folder / "placements.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = payload.get("placements", [])
    columns = (
        "k", "r", "piece", "sample_atlas", "r_prime", "dx", "dy",
        "bbox_left", "bbox_top", "bbox_right", "bbox_bottom", "center_x", "center_y",
        "matched_pixels", "sample_alpha_pixels", "fraction",
    )
    with (folder / "placements.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(columns)
        for row in rows:
            bbox = row["old_bbox_cell"]
            center = row["center_old_frame"]
            writer.writerow(
                (
                    row["k"], row["r"], row["piece"], row["sample_atlas"], row["r_prime"],
                    row["dx"], row["dy"], bbox["left"], bbox["top"], bbox["right"], bbox["bottom"],
                    center["x"], center["y"], row["matched_pixels"], row["sample_alpha_pixels"],
                    f'{row["fraction"]:.8f}',
                )
            )
    below = [row for row in rows if row["matched_pixels"] / row["sample_alpha_pixels"] < 0.9]
    with (folder / "below-0.9.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(columns)
        for row in below:
            bbox = row["old_bbox_cell"]
            center = row["center_old_frame"]
            writer.writerow(
                (
                    row["k"], row["r"], row["piece"], row["sample_atlas"], row["r_prime"],
                    row["dx"], row["dy"], bbox["left"], bbox["top"], bbox["right"], bbox["bottom"],
                    center["x"], center["y"], row["matched_pixels"], row["sample_alpha_pixels"],
                    f'{row["fraction"]:.8f}',
                )
            )


def search(args: argparse.Namespace) -> int:
    pack_path = Path(args.pack)
    out_root = Path(args.out_root)
    scales = parse_scale(Path(args.scale))
    atlases = old_atlases(pack_path)
    low_rows: list[dict[str, Any]] = []

    for squad, sample_name in SQUADS.items():
        folder = out_root / "squads" / squad
        folder.mkdir(parents=True, exist_ok=True)
        log_path = folder / "search.log"
        log_path.write_text("", encoding="utf-8")
        scale = scales.get(squad)
        if scale is None:
            raise ValueError(f"в таблице масштаба нет строки {squad}")
        target_image = atlases[squad]
        sample_image = atlases[sample_name]
        templates_by_col: dict[int, list[Template]] = {}
        for k in range(COLS):
            templates = [
                item
                for r_prime in range(ROWS)
                if (item := make_template(sample_image, k, r_prime)) is not None
            ]
            templates_by_col[k] = templates

        note(f"[{squad}] поиск начат; D={scale:.15g}; источник={sample_name}", log_path)
        payload: dict[str, Any] = {
            "format": 1,
            "squad": squad,
            "old_sample_atlas": sample_name,
            "source_pack": str(pack_path),
            "atlas_size": [ATLAS_WIDTH, ATLAS_HEIGHT],
            "cell_size": CELL,
            "columns": COLS,
            "rows": ROWS,
            "scale_D": scale,
            "coordinates": "dx,dy — сдвиг полного кадра образца; центр фактического bbox фигуры задан в координатах целевой клетки.",
            "placements": [],
            "complete": False,
        }
        placements: list[dict[str, Any]] = payload["placements"]
        for r in range(ROWS):
            for k in range(COLS):
                remaining = cell_alpha(target_image, k, r)
                templates = templates_by_col[k]
                found = 0
                for piece in range(1, 4):
                    if not templates:
                        failure = f"{squad} k={k} r={r}: найдено {found} фигур из 3; образцы пусты"
                        payload["failure"] = failure
                        save_placements(folder, payload)
                        note(f"ОСТАНОВКА: {failure}", log_path)
                        raise SearchFailure(failure)
                    chosen, found_left, found_top, matched, total = best_location(remaining, templates)
                    fraction = matched / total
                    if matched == 0 or fraction < 0.5:
                        failure = (
                            f"{squad} k={k} r={r}: найдено {found} фигур из 3; "
                            f"лучшая доля {matched}/{total}={fraction:.8f} ниже 0.5"
                        )
                        payload["failure"] = failure
                        save_placements(folder, payload)
                        note(f"ОСТАНОВКА: {failure}", log_path)
                        raise SearchFailure(failure)

                    left, top, right, bottom = chosen.bbox
                    dx = found_left - left
                    dy = found_top - top
                    old_bbox = {
                        "left": dx + left,
                        "top": dy + top,
                        "right": dx + right,
                        "bottom": dy + bottom,
                    }
                    center_x = (old_bbox["left"] + old_bbox["right"]) / 2
                    center_y = (old_bbox["top"] + old_bbox["bottom"]) / 2
                    entry: dict[str, Any] = {
                        "k": k,
                        "r": r,
                        "piece": piece,
                        "sample_atlas": sample_name,
                        "r_prime": chosen.frame,
                        "dx": dx,
                        "dy": dy,
                        "old_bbox_cell": old_bbox,
                        "center_old_frame": {"x": center_x, "y": center_y},
                        "matched_pixels": matched,
                        "sample_alpha_pixels": total,
                        "fraction": fraction,
                        "fraction_exact": {"numerator": matched, "denominator": total},
                    }
                    placements.append(entry)
                    if fraction < 0.9:
                        low_rows.append({"squad": squad, **entry})
                    note(
                        f"{squad} k={k} r={r} piece={piece}: r′={chosen.frame} "
                        f"dx={dx} dy={dy} count={matched}/{total} fraction={fraction:.8f}",
                        log_path,
                    )
                    remove_covered(remaining, chosen.mask, found_left, found_top)
                    found += 1
                if found != 3:
                    failure = f"{squad} k={k} r={r}: найдено {found} фигур из 3"
                    payload["failure"] = failure
                    save_placements(folder, payload)
                    note(f"ОСТАНОВКА: {failure}", log_path)
                    raise SearchFailure(failure)
                save_placements(folder, payload)
        payload["complete"] = True
        save_placements(folder, payload)
        note(f"[{squad}] размещено {len(placements)} фигур", log_path)

    summary = out_root / "squads" / "below-0.9.tsv"
    summary.parent.mkdir(parents=True, exist_ok=True)
    columns = (
        "squad", "k", "r", "piece", "sample_atlas", "r_prime", "dx", "dy",
        "center_x", "center_y", "matched_pixels", "sample_alpha_pixels", "fraction",
    )
    with summary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(columns)
        for row in low_rows:
            center = row["center_old_frame"]
            writer.writerow(
                (
                    row["squad"], row["k"], row["r"], row["piece"], row["sample_atlas"], row["r_prime"],
                    row["dx"], row["dy"], center["x"], center["y"], row["matched_pixels"],
                    row["sample_alpha_pixels"], f'{row["fraction"]:.8f}',
                )
            )
    print(f"Список долей ниже 0.9: {summary}")
    return 0


def round_nearest(value: float) -> int:
    if value >= 0:
        return math.floor(value + 0.5)
    return math.ceil(value - 0.5)


def open_atlas(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    if image.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
        raise ValueError(f"ожидался атлас 1024x512, получен {image.size}: {path}")
    return image


def source_bbox(image: Image.Image, k: int, r: int) -> tuple[int, int, int, int] | None:
    alpha = image.getchannel("A").crop((k * CELL, r * CELL, (k + 1) * CELL, (r + 1) * CELL))
    return alpha.getbbox()


def compose(args: argparse.Namespace) -> int:
    squad = args.squad
    out_root = Path(args.out_root)
    folder = out_root / "squads" / squad
    folder.mkdir(parents=True, exist_ok=True)
    log_path = folder / f"compose-{Path(args.source).stem}.log"
    log_path.write_text("", encoding="utf-8")
    source_path = Path(args.source)
    body_path = Path(args.body) if args.body else source_path
    if args.mask and not args.body:
        raise ValueError("режим --mask требует путь к телу через --body")
    placements_path = Path(args.placements) if args.placements else folder / "placements.json"
    placements_doc = json.loads(placements_path.read_text(encoding="utf-8"))
    if placements_doc.get("squad") != squad or not placements_doc.get("complete"):
        raise ValueError(f"размещения неполны или относятся к другому отряду: {placements_path}")
    rows = placements_doc.get("placements", [])
    by_cell: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for item in rows:
        by_cell.setdefault((int(item["r"]), int(item["k"])), []).append(item)
    if len(by_cell) != ROWS * COLS or any(len(items) != 3 for items in by_cell.values()):
        raise ValueError(f"в placements.json должны быть три фигуры в каждом из 32 кадров: {placements_path}")

    source = open_atlas(source_path)
    body = open_atlas(body_path)
    result = Image.new("RGBA", (ATLAS_WIDTH, ATLAS_HEIGHT), (0, 0, 0, 0))
    cell_reports: list[dict[str, Any]] = []
    failures: list[str] = []
    for r in range(ROWS):
        for k in range(COLS):
            pieces: list[tuple[float, int, int, dict[str, Any], int, int, tuple[int, int, int, int] | None, tuple[int, int, int, int] | None]] = []
            for item in by_cell[(r, k)]:
                source_r = int(item["r_prime"])
                support_bbox = source_bbox(body, k, source_r)
                actual_bbox = source_bbox(source, k, source_r)
                if support_bbox is None:
                    if actual_bbox is not None:
                        raise ValueError(
                            f"body пуст, но source непуст в {squad} k={k} r′={source_r}; "
                            "для смещения нужен body"
                        )
                    shift_x = shift_y = 0
                    bottom = 0.0
                else:
                    cx = (support_bbox[0] + support_bbox[2]) / 2
                    cy = (support_bbox[1] + support_bbox[3]) / 2
                    old_center = item["center_old_frame"]
                    target_x = ANCHOR + float(placements_doc["scale_D"]) * (float(old_center["x"]) - ANCHOR)
                    target_y = ANCHOR + float(placements_doc["scale_D"]) * (float(old_center["y"]) - ANCHOR)
                    shift_x = round_nearest(target_x - cx)
                    shift_y = round_nearest(target_y - cy)
                    bottom = support_bbox[3] + shift_y
                if actual_bbox is not None:
                    moved = (
                        actual_bbox[0] + shift_x,
                        actual_bbox[1] + shift_y,
                        actual_bbox[2] + shift_x,
                        actual_bbox[3] + shift_y,
                    )
                    if moved[0] < 0 or moved[1] < 0 or moved[2] > CELL or moved[3] > CELL:
                        failure = (
                            f"alpha вне клетки: {squad} k={k} r={r} piece={item['piece']} "
                            f"r′={source_r} bbox={moved}"
                        )
                        failures.append(failure)
                        note(f"ОШИБКА: {failure}", log_path)
                        continue
                pieces.append((bottom, int(item["piece"]), source_r, item, shift_x, shift_y, support_bbox, actual_bbox))

            visible_layers = 0
            ordered_pieces = sorted(pieces, key=lambda p: (p[0], p[1]))
            if args.mask:
                mask_alpha = np.zeros((CELL, CELL), dtype=np.float64)
                for _, _, source_r, _, shift_x, shift_y, _, actual_bbox in ordered_pieces:
                    bounds = (k * CELL, source_r * CELL, (k + 1) * CELL, (source_r + 1) * CELL)
                    body_cell = body.crop(bounds)
                    source_cell = source.crop(bounds)
                    shifted_body = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
                    shifted_mask = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
                    shifted_body.alpha_composite(body_cell, (shift_x, shift_y))
                    shifted_mask.alpha_composite(source_cell, (shift_x, shift_y))
                    body_alpha = np.asarray(shifted_body.getchannel("A"), dtype=np.float64)
                    layer_mask_alpha = np.asarray(shifted_mask.getchannel("A"), dtype=np.float64)
                    mask_alpha *= 1.0 - body_alpha / 255.0
                    mask_alpha += layer_mask_alpha
                    if actual_bbox is not None:
                        visible_layers += 1
                if np.any(mask_alpha < 0.0) or np.any(mask_alpha > 255.0):
                    raise ValueError(f"составная альфа маски вышла за диапазон 0..255: {squad} k={k} r={r}")
                pixels = np.full((CELL, CELL, 4), 255, dtype=np.uint8)
                pixels[..., 3] = np.floor(mask_alpha + 0.5).astype(np.uint8)
                cell = Image.fromarray(pixels, mode="RGBA")
            else:
                cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
                for _, _, source_r, _, shift_x, shift_y, _, actual_bbox in ordered_pieces:
                    source_cell = source.crop(
                        (k * CELL, source_r * CELL, (k + 1) * CELL, (source_r + 1) * CELL)
                    )
                    layer = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
                    layer.alpha_composite(source_cell, (shift_x, shift_y))
                    cell = Image.alpha_composite(cell, layer)
                    if actual_bbox is not None:
                        visible_layers += 1
            result.paste(cell, (k * CELL, r * CELL))
            cell_reports.append(
                {"k": k, "r": r, "placement_count": len(by_cell[(r, k)]), "visible_layers": visible_layers}
            )

    if failures:
        raise ValueError("\n".join(failures))
    default_stem = f"HM_{squad}" if args.mask else f"{source_path.stem}_{squad}"
    output_path = Path(args.output) if args.output else folder / f"{default_stem}.png"
    sheet_path = Path(args.sheet) if args.sheet else folder / f"{default_stem}-sheet.png"
    report_path = Path(args.report) if args.report else folder / f"{default_stem}-checks.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path)
    atlas_sheet = Image.new("RGBA", result.size, SAND)
    atlas_sheet.alpha_composite(result)
    atlas_sheet = atlas_sheet.resize((result.width * 2, result.height * 2), Image.Resampling.NEAREST)
    left_margin = 76
    top_margin = 56
    sheet = Image.new("RGBA", (atlas_sheet.width + left_margin, atlas_sheet.height + top_margin), SAND)
    sheet.alpha_composite(atlas_sheet, (left_margin, top_margin))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(str(FONT_PATH), 20) if FONT_PATH.is_file() else ImageFont.load_default()
        sheet_font = str(FONT_PATH) if FONT_PATH.is_file() else "Pillow default"
    except OSError:
        font = ImageFont.load_default()
        sheet_font = "Pillow default"
    draw.text((10, 12), f"{squad}  ·  4 строки × 8 кадров", font=font, fill=(45, 39, 31, 255))
    for k in range(COLS):
        px = left_margin + k * CELL * 2 + 8
        draw.text((px, top_margin - 24), f"k{k}", font=font, fill=(45, 39, 31, 255))
    for r in range(ROWS):
        py = top_margin + r * CELL * 2 + 8
        draw.text((12, py), f"r{r}", font=font, fill=(45, 39, 31, 255))
    for x in range(COLS + 1):
        px = left_margin + x * CELL * 2
        draw.line((px, top_margin, px, sheet.height - 1), fill=(82, 71, 54, 180), width=1)
    for y in range(ROWS + 1):
        py = top_margin + y * CELL * 2
        draw.line((left_margin, py, sheet.width - 1, py), fill=(82, 71, 54, 180), width=1)
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path)
    report = {
        "squad": squad,
        "source": str(source_path),
        "body_geometry": str(body_path),
        "output": str(output_path),
        "sheet": str(sheet_path),
        "sheet_font": sheet_font,
        "atlas_size": list(result.size),
        "cell_size": CELL,
        "all_alpha_inside_cells": True,
        "three_placements_per_frame": all(row["placement_count"] == 3 for row in cell_reports),
        "cells": cell_reports,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    note(f"Атлас: {output_path}", log_path)
    note(f"Лист 4x8: {sheet_path}", log_path)
    note(f"Проверки: {report_path}", log_path)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_search = subparsers.add_parser("search", help="найти старые места фигур в трёх отрядах")
    parser_search.add_argument("--pack", default=str(ROOT / "tools/units3d/data/sdl_data_hd4_source.dat"))
    parser_search.add_argument("--scale", default=str(ROOT / "codex-direct/U7/scale-D.tsv"))
    parser_search.add_argument("--out-root", default=str(ROOT / ".tmp/out-u8"))
    parser_search.set_defaults(func=search)

    parser_compose = subparsers.add_parser("compose", help="собрать новый атлас из placements.json")
    parser_compose.add_argument("--squad", choices=sorted(SQUADS), required=True)
    parser_compose.add_argument("--source", required=True, help="новый atlas, который будет наложен")
    parser_compose.add_argument("--body", help="атлас геометрической опоры; по умолчанию равен --source")
    parser_compose.add_argument("--mask", action="store_true", help="собрать маску с учётом перекрытия тел")
    parser_compose.add_argument("--placements", help="путь к placements.json")
    parser_compose.add_argument("--out-root", default=str(ROOT / ".tmp/out-u8"))
    parser_compose.add_argument("--output", help="путь результирующего атласа")
    parser_compose.add_argument("--sheet", help="путь листа на песчаном фоне")
    parser_compose.add_argument("--report", help="путь JSON-проверки")
    parser_compose.set_defaults(func=compose)

    args = parser.parse_args()
    try:
        return args.func(args)
    except SearchFailure as error:
        print(f"ОСТАНОВКА ПО УСЛОВИЮ ПОИСКА: {error}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
