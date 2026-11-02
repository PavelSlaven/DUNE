#!/usr/bin/env python3
import argparse
import html
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import combos

PER_SHEET = 6
COLUMNS = 3
CELL_WIDTH = 640
CELL_IMAGE_MAX_HEIGHT = 480
CAPTION_LINES = 3
LINE_HEIGHT = 18
GAP = 8
FONT_PATHS = ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf")
COLOR_A = (230, 30, 30)
COLOR_B = (30, 90, 240)
BACKGROUND = (24, 24, 24)
TEXT = (235, 235, 235)


def load_font(size=13):
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def chunks(items, size=PER_SHEET):
    return [items[start:start + size] for start in range(0, len(items), size)]


def scale_text(combo):
    def one(value):
        return str(value) if value else "auto"

    return f"render {one(combo['render'])} / world {one(combo['world'])}"


def caption_lines(meta, combo, extra=""):
    first = meta["id"] if not extra else f"{meta['id']}  {extra}"
    second = f"screen {meta.get('screen', '')}  state {meta.get('state', '')}  house {meta.get('house') or '-'}"
    third = f"{combo['resolution']}  {combo['language']}  {combo['graphics']}  {scale_text(combo)}"
    return [first, second, third]


def combo_of_path(png_root, path):
    parts = Path(os.path.relpath(path, png_root)).parts
    return combos.parse_id("/".join(parts[:-1])), Path(parts[-1]).stem


def find_pngs(png_root):
    return sorted(Path(png_root).rglob("*.png"))


def scaled_rect(rect, factor):
    left, top = rect["x"] * factor, rect["y"] * factor
    return [left, top, max(left, (rect["x"] + rect["w"]) * factor - 1), max(top, (rect["y"] + rect["h"]) * factor - 1)]


def render_cell(png_path, lines, rects, font):
    image = Image.open(png_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    for rect, color in rects:
        draw.rectangle(scaled_rect(rect, 1.0), outline=color, width=max(2, image.width // 400))
    ratio = min(CELL_WIDTH / image.width, CELL_IMAGE_MAX_HEIGHT / image.height)
    image = image.resize((max(1, round(image.width * ratio)), max(1, round(image.height * ratio))), Image.LANCZOS)
    cell = Image.new("RGB", (CELL_WIDTH, CELL_IMAGE_MAX_HEIGHT + LINE_HEIGHT * CAPTION_LINES), BACKGROUND)
    cell.paste(image, (0, 0))
    text_draw = ImageDraw.Draw(cell)
    for index, line in enumerate(lines[:CAPTION_LINES]):
        text_draw.text((4, CELL_IMAGE_MAX_HEIGHT + index * LINE_HEIGHT + 1), line, fill=TEXT, font=font)
    return cell


def make_sheet(cells, path):
    rows = (PER_SHEET + COLUMNS - 1) // COLUMNS
    cell_height = CELL_IMAGE_MAX_HEIGHT + LINE_HEIGHT * CAPTION_LINES
    sheet = Image.new("RGB", (COLUMNS * CELL_WIDTH + (COLUMNS + 1) * GAP, rows * cell_height + (rows + 1) * GAP), BACKGROUND)
    for index, cell in enumerate(cells):
        column, row = index % COLUMNS, index // COLUMNS
        sheet.paste(cell, (GAP + column * (CELL_WIDTH + GAP), GAP + row * (cell_height + GAP)))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, "JPEG", quality=85)


def build_catalog_sheets(png_root, meta, combo_id, out_dir):
    font = load_font()
    directory = Path(png_root) / combo_id
    by_scene = {path.stem: path for path in directory.glob("*.png")}
    ordered = [scene for scene in meta if scene in by_scene]
    combo = combos.parse_id(combo_id)
    written = []
    for number, group in enumerate(chunks(ordered), 1):
        cells = [render_cell(by_scene[scene], caption_lines(meta[scene], combo), [], font) for scene in group]
        path = Path(out_dir) / combo_id.replace("/", "_") / f"{number:03d}.jpg"
        make_sheet(cells, path)
        written.append(path)
    return written


def canvas_factor(png_path, logs_root, combo_id, scene):
    log = Path(logs_root) / combo_id / f"{scene}.geometry.jsonl"
    if not log.exists():
        return 1.0
    header = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
    return Image.open(png_path).width / header["canvas"]["w"]


def flag_rects(flag, factor):
    rects = []
    for key, color in (("a", COLOR_A), ("b", COLOR_B)):
        rect = flag.get(key)
        if rect:
            rects.append(({"x": rect["x"] * factor, "y": rect["y"] * factor,
                           "w": rect["w"] * factor, "h": rect["h"] * factor}, color))
    return rects


def flag_text(flag):
    texts = " | ".join(text.replace("\n", " ") for text in flag.get("texts", []))
    return f"rule {flag['rule']}  {texts}".strip()


def unique_flags(flags):
    seen, result = set(), []
    for flag in flags:
        key = (flag["rule"], flag["scene"], flag["combo"], json.dumps(flag.get("a")), json.dumps(flag.get("b")))
        if key not in seen:
            seen.add(key)
            result.append(flag)
    return sorted(result, key=lambda f: (f["rule"], f["combo"], f["scene"]))


def display_flags(png_root, flags, ordered_ids):
    if not ordered_ids:
        return flags
    first = combos.first_combo_by_key(flags, ordered_ids)
    source = {}
    for flag in flags:
        source.setdefault((flag["combo"], combos.flag_key(flag)), flag)
    result = []
    for flag in flags:
        if (Path(png_root) / flag["combo"] / f"{flag['scene']}.png").exists():
            result.append(flag)
            continue
        origin = first[(combos.resolution_of(flag["combo"]), combos.flag_key(flag))]
        result.append(source[(origin, combos.flag_key(flag))])
    return result


def build_flag_sheets(png_root, logs_root, meta, flags, out_dir, ordered_ids=None):
    font = load_font()
    written, missing = [], []
    by_rule = {}
    for flag in unique_flags(display_flags(png_root, flags, ordered_ids)):
        by_rule.setdefault(flag["rule"], []).append(flag)
    for rule, group in sorted(by_rule.items()):
        items = []
        for flag in group:
            png = Path(png_root) / flag["combo"] / f"{flag['scene']}.png"
            if not png.exists():
                missing.append((flag["scene"], flag["combo"], flag["rule"]))
                continue
            items.append((flag, png))
        for number, part in enumerate(chunks(items), 1):
            cells = []
            for flag, png in part:
                combo = combos.parse_id(flag["combo"])
                scene_meta = meta.get(flag["scene"], {"id": flag["scene"]})
                factor = canvas_factor(png, logs_root, flag["combo"], flag["scene"])
                lines = caption_lines(scene_meta, combo, flag_text(flag))
                cells.append(render_cell(png, lines, flag_rects(flag, factor), font))
            path = Path(out_dir) / f"rule{rule}-{number:03d}.jpg"
            make_sheet(cells, path)
            written.append(path)
    return written, missing


INDEX_STYLE = """body{font:14px sans-serif;margin:16px;background:#181818;color:#eee}
a{color:#8ab4ff}input,select{margin:0 8px 8px 0}table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #333;padding:2px 8px;text-align:left}
tr.hidden{display:none}"""

INDEX_SCRIPT = """const rows=[...document.querySelectorAll('tbody tr')];
const filters=[...document.querySelectorAll('[data-col]')];
function apply(){let shown=0;for(const row of rows){let ok=true;
for(const f of filters){const v=f.value.toLowerCase();
if(v&&!row.children[+f.dataset.col].textContent.toLowerCase().includes(v)){ok=false;break;}}
row.classList.toggle('hidden',!ok);if(ok)shown++;}
document.getElementById('count').textContent=shown+' / '+rows.length;}
filters.forEach(f=>f.addEventListener('input',apply));apply();"""

COLUMN_NAMES = ("scene", "screen", "state", "house", "resolution", "language", "graphics", "render", "world", "flags")


def build_index(png_root, meta, flags, sheets, index_path):
    flag_count = {}
    for flag in unique_flags(flags):
        key = (flag["combo"], flag["scene"])
        flag_count[key] = flag_count.get(key, 0) + 1
    base = Path(index_path).parent
    rows = []
    for png in find_pngs(png_root):
        combo, scene = combo_of_path(png_root, png)
        scene_meta = meta.get(scene, {"id": scene})
        cells = [scene, scene_meta.get("screen", ""), scene_meta.get("state", ""), scene_meta.get("house") or "",
                 combo["resolution"], combo["language"], combo["graphics"],
                 str(combo["render"] or "auto"), str(combo["world"] or "auto"),
                 str(flag_count.get((combos.combo_id(combo), scene), 0))]
        link = html.escape(os.path.relpath(png, base).replace(os.sep, "/"))
        rows.append(f'<tr><td><a href="{link}">{html.escape(cells[0])}</a></td>'
                    + "".join(f"<td>{html.escape(cell)}</td>" for cell in cells[1:]) + "</tr>")
    inputs = "".join(f'<input data-col="{index}" placeholder="{name}" size="12">'
                     for index, name in enumerate(COLUMN_NAMES))
    sheet_links = "".join(f'<a href="{html.escape(os.path.relpath(path, base).replace(os.sep, "/"))}">'
                          f'{html.escape(Path(path).parent.name + "/" + Path(path).name)}</a> ' for path in sheets)
    page = (f"<!doctype html><html><head><meta charset='utf-8'><title>UI audit index</title>"
            f"<style>{INDEX_STYLE}</style></head><body><h1>UI audit index</h1>"
            f"<p id='count'></p><div>{inputs}</div><details><summary>Sheets ({len(sheets)})</summary>"
            f"<p>{sheet_links}</p></details><table><thead><tr>"
            + "".join(f"<th>{name}</th>" for name in COLUMN_NAMES)
            + f"</tr></thead><tbody>{''.join(rows)}</tbody></table><script>{INDEX_SCRIPT}</script></body></html>")
    Path(index_path).write_text(page, encoding="utf-8")
    return len(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build contact sheets, flag sheets and the HTML index.")
    parser.add_argument("--png-root", required=True)
    parser.add_argument("--logs-root", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--flags", help="flags JSON from check_geometry.py")
    parser.add_argument("--full", action="append", default=[], help="combination id with a full catalog sheet set")
    parser.add_argument("--order", help="order.json written by run_all.py")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    meta = {scene["id"]: scene for scene in json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]}
    flags = json.loads(Path(args.flags).read_text(encoding="utf-8")) if args.flags else []
    out = Path(args.out)
    sheets = []
    for combo_id in args.full:
        sheets.extend(build_catalog_sheets(args.png_root, meta, combo_id, out / "sheets"))
    order = json.loads(Path(args.order).read_text(encoding="utf-8")) if args.order else None
    flag_sheets, missing = build_flag_sheets(args.png_root, args.logs_root, meta, flags, out / "flag-sheets", order)
    count = build_index(args.png_root, meta, flags, sheets + flag_sheets, out / "index.html")
    print(f"sheets: {len(sheets)}; flag sheets: {len(flag_sheets)}; flagged without PNG: {len(missing)}; "
          f"index rows: {count}")
    for scene, combo, rule in missing:
        print(f"no PNG: {scene}; {combo}; rule {rule}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
