#!/usr/bin/env python3
"""Build an exact old/current visual catalogue for the 169-resource HD pass."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hd_assets import decode_image, read_pack, safe_name  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BACKUP = Path(
    r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru.backup-before-style-pass-20260802-172412\data"
)
DEFAULT_CURRENT = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data")
DEFAULT_REPORT = ROOT / "artifacts" / "hd_completion" / "integrated" / "integration_report.json"
DEFAULT_STAGE = ROOT / "artifacts" / "hd_completion" / "integrated" / "data"
DEFAULT_OUTPUT = ROOT / "artifacts" / "hd_completion_comparison"

RETURNED_NAMES = {
    "MOUSE_ATTACK", "MOUSE_DOWN", "MOUSE_FORBIDDEN", "MOUSE_LEFT",
    "MOUSE_MOVE", "MOUSE_NORMAL", "MOUSE_PICK", "MOUSE_RALLY",
    "MOUSE_REPAIR", "MOUSE_RIGHT", "MOUSE_UP", "SHROUD", "SHROUD_SHADOW",
}

PACK_TITLES = {
    "sdl_data": "Эффекты и игровые служебные изображения",
    "sdl_inter": "Интерфейс",
    "sdl_world": "Карта кампании",
    "sdl_mentat": "Экраны ментата",
}


def rgba_digest(image: Image.Image) -> str:
    rgba = image.convert("RGBA")
    digest = hashlib.sha256()
    digest.update(f"{rgba.width}x{rgba.height}".encode("ascii"))
    digest.update(rgba.tobytes())
    return digest.hexdigest()


def image_metrics(image: Image.Image) -> dict[str, object]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    extrema = alpha.getextrema()
    bbox = alpha.getbbox()
    grayscale = rgba.convert("RGB").convert("L")
    variance = float(ImageStat.Stat(grayscale).var[0])
    opaque = sum(1 for value in alpha.getdata() if value > 8)
    total = rgba.width * rgba.height
    border_values = []
    if rgba.width and rgba.height:
        border_values.extend(alpha.crop((0, 0, rgba.width, 1)).getdata())
        border_values.extend(alpha.crop((0, rgba.height - 1, rgba.width, rgba.height)).getdata())
        border_values.extend(alpha.crop((0, 0, 1, rgba.height)).getdata())
        border_values.extend(alpha.crop((rgba.width - 1, 0, rgba.width, rgba.height)).getdata())
    border_ratio = (
        sum(1 for value in border_values if value > 8) / len(border_values)
        if border_values else 0.0
    )
    bbox_ratio = 0.0
    if bbox:
        bbox_ratio = ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) / total
    return {
        "size": [rgba.width, rgba.height],
        "alpha_min": extrema[0],
        "alpha_max": extrema[1],
        "opaque_ratio": opaque / total if total else 0.0,
        "border_ratio": border_ratio,
        "bbox_ratio": bbox_ratio,
        "luma_variance": variance,
    }


def audit_notes(old: Image.Image, new: Image.Image) -> list[str]:
    notes: list[str] = []
    old_m = image_metrics(old)
    new_m = image_metrics(new)
    if old.size != new.size:
        notes.append(f"размер изменён: {old.width}×{old.height} → {new.width}×{new.height}")
    if float(new_m["opaque_ratio"]) < 0.0005:
        notes.append("почти пустое изображение")
    if float(new_m["luma_variance"]) < 2.0:
        notes.append("почти нет деталей/контраста")
    if int(new_m["alpha_min"]) < 255:
        old_edge = float(old_m["border_ratio"])
        new_edge = float(new_m["border_ratio"])
        if new_edge > 0.25 and new_edge > old_edge + 0.15:
            notes.append("новая альфа заметно касается границ атласа")
        old_bbox = float(old_m["bbox_ratio"])
        new_bbox = float(new_m["bbox_ratio"])
        if old_bbox > 0.01 and (new_bbox / old_bbox > 1.45 or new_bbox / old_bbox < 0.65):
            notes.append("сильно изменился занимаемый силуэтом объём")
    return notes


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGB", size, (24, 28, 32))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            color = (39, 44, 49) if ((x // cell) + (y // cell)) % 2 else (27, 31, 35)
            draw.rectangle((x, y, min(x + cell, size[0]), min(y + cell, size[1])), fill=color)
    return image


def fit_preview(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    rgba.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = checker(size)
    x = (size[0] - rgba.width) // 2
    y = (size[1] - rgba.height) // 2
    canvas.paste(rgba, (x, y), rgba)
    return canvas


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def build_contact_pages(records: list[dict[str, object]], output: Path) -> list[str]:
    page_dir = output / "pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    title_font = load_font(ROOT / "resources" / "bin" / "data" / "RussoOne-Regular.ttf", 25)
    label_font = load_font(ROOT / "resources" / "bin" / "data" / "PTSansNarrow-Regular.ttf", 18)
    small_font = load_font(ROOT / "resources" / "bin" / "data" / "PTSansNarrow-Regular.ttf", 15)
    page_files: list[str] = []
    per_page = 8
    for page_index in range(math.ceil(len(records) / per_page)):
        chunk = records[page_index * per_page:(page_index + 1) * per_page]
        page = Image.new("RGB", (1440, 104 + len(chunk) * 230), (11, 14, 17))
        draw = ImageDraw.Draw(page)
        heading = f"СТАРОЕ → ТЕКУЩЕЕ   |   страница {page_index + 1}/{math.ceil(len(records) / per_page)}"
        draw.text((28, 23), heading, font=title_font, fill=(228, 188, 91))
        draw.text((28, 61), "Слева — бэкап до пакетной фазы; справа — фактический ресурс игры сейчас", font=small_font, fill=(176, 184, 191))
        for row, record in enumerate(chunk):
            y = 104 + row * 230
            draw.rectangle((18, y + 4, 1422, y + 220), outline=(88, 72, 41), width=1)
            old_image = Image.open(output / str(record["old_file"])).convert("RGBA")
            new_image = Image.open(output / str(record["new_file"])).convert("RGBA")
            page.paste(fit_preview(old_image, (540, 168)), (218, y + 42))
            page.paste(fit_preview(new_image, (540, 168)), (840, y + 42))
            draw.text((32, y + 18), f"{record['pack']}  #{record['id']:03d}", font=small_font, fill=(228, 188, 91))
            draw.text((32, y + 48), str(record["name"]), font=label_font, fill=(238, 239, 233))
            draw.text((32, y + 82), str(record["category"]), font=small_font, fill=(164, 174, 181))
            draw.text((32, y + 112), str(record["status_label"]), font=small_font, fill=tuple(record["status_color"]))
            draw.text((218, y + 16), "СТАРОЕ", font=label_font, fill=(186, 194, 199))
            draw.text((840, y + 16), "ТЕКУЩЕЕ", font=label_font, fill=(238, 209, 129))
            note = "; ".join(record["notes"]) if record["notes"] else "автоматических технических замечаний нет"
            draw.text((32, y + 178), note[:160], font=small_font, fill=(197, 159, 111) if record["notes"] else (126, 154, 132))
        filename = f"comparison_{page_index + 1:02d}.png"
        page.save(page_dir / filename, optimize=True)
        page_files.append(f"pages/{filename}")
    return page_files


def build_html(records: list[dict[str, object]], page_files: list[str], output: Path) -> None:
    counts: dict[str, int] = {}
    for record in records:
        counts[str(record["status"])] = counts.get(str(record["status"]), 0) + 1
    cards = []
    for record in records:
        notes = "<br>".join(html.escape(str(note)) for note in record["notes"]) or "Автоматических технических замечаний нет"
        key = f"{record['pack']}:{record['id']}"
        cards.append(f"""
<article class="card" data-pack="{html.escape(str(record['pack']))}" data-status="{html.escape(str(record['status']))}" data-search="{html.escape((str(record['pack'])+' '+str(record['id'])+' '+str(record['name'])).lower())}">
  <header><span class="id">{html.escape(str(record['pack']))} #{int(record['id']):03d}</span><strong>{html.escape(str(record['name']))}</strong><span class="badge {html.escape(str(record['status']))}">{html.escape(str(record['status_label']))}</span></header>
  <div class="compare">
    <figure><a href="{html.escape(str(record['old_file']))}" target="_blank"><img src="{html.escape(str(record['old_file']))}" loading="lazy"></a><figcaption>СТАРОЕ · {record['old_size'][0]}×{record['old_size'][1]}</figcaption></figure>
    <figure><a href="{html.escape(str(record['new_file']))}" target="_blank"><img src="{html.escape(str(record['new_file']))}" loading="lazy"></a><figcaption>ТЕКУЩЕЕ · {record['new_size'][0]}×{record['new_size'][1]}</figcaption></figure>
  </div>
  <p class="notes">{notes}</p>
  <div class="decision" data-key="{html.escape(key)}"><button data-value="accept">Принять</button><button data-value="redo">Переделать</button><button data-value="restore">Вернуть старое</button><input placeholder="Комментарий"></div>
</article>""")
    page_links = " ".join(f'<a href="{html.escape(path)}" target="_blank">{index + 1}</a>' for index, path in enumerate(page_files))
    summary = f"Пакетная версия: {counts.get('batch', 0)} · Доработано позже: {counts.get('later', 0)} · Возвращено: {counts.get('restored', 0)} · Отмечено для визуальной проверки: {counts.get('review', 0)}"
    document = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>D2TM — сравнение 169 ресурсов</title>
<style>
@font-face{{font-family:PTN;src:url('../../resources/bin/data/PTSansNarrow-Regular.ttf')}}
@font-face{{font-family:Russo;src:url('../../resources/bin/data/RussoOne-Regular.ttf')}}
:root{{color-scheme:dark;--bg:#0b0e11;--panel:#151a1e;--line:#765f32;--gold:#e1b84e;--text:#e7e5dc}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:18px PTN,Arial,sans-serif}}
.toolbar{{position:sticky;top:0;z-index:5;background:#0d1115f2;border-bottom:1px solid var(--line);padding:16px 24px}}
h1{{font:28px Russo;margin:0 0 8px;color:var(--gold)}} .summary{{color:#bbc2c7}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}} input,select,button{{font:16px PTN;background:#171d21;color:var(--text);border:1px solid #80672f;padding:8px 12px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(620px,1fr));gap:16px;padding:20px}}
.card{{background:var(--panel);border:1px solid #3f3525;padding:12px;min-width:0}} .card header{{display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
.id{{color:#d8ad4d}} .badge{{margin-left:auto;padding:3px 8px;border:1px solid currentColor}} .badge.restored{{color:#a9b2b8}} .badge.later{{color:#6ec8ed}} .badge.batch{{color:#87c987}} .badge.review{{color:#ed9f68}}
.compare{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}} figure{{margin:0;background:repeating-conic-gradient(#252b30 0 25%,#1a1f23 0 50%) 50%/24px 24px;min-width:0}} figure img{{display:block;width:100%;height:280px;object-fit:contain}} figcaption{{background:#0e1215;padding:6px;text-align:center;color:#c7b274}}
.notes{{min-height:28px;color:#c3c8cb}} .decision{{display:grid;grid-template-columns:auto auto auto 1fr;gap:6px}} .decision button.active{{background:#7b5f20;color:#fff}} .decision input{{min-width:80px}}
.pages{{margin-top:8px}} .pages a{{color:#e6bd55;margin-right:8px}} .hidden{{display:none!important}}
@media(max-width:750px){{.grid{{grid-template-columns:1fr;padding:8px}}.compare{{grid-template-columns:1fr}}.decision{{grid-template-columns:1fr 1fr}}}}
</style></head><body>
<div class="toolbar"><h1>D2TM · СТАРОЕ → ТЕКУЩЕЕ</h1><div class="summary">169 ресурсов большой пакетной фазы. {html.escape(summary)}</div>
<div class="filters"><input id="search" placeholder="ID или имя"><select id="pack"><option value="">Все пакеты</option><option>sdl_data</option><option>sdl_inter</option><option>sdl_world</option><option>sdl_mentat</option></select><select id="status"><option value="">Все статусы</option><option value="batch">Пакетная версия</option><option value="later">Доработано позже</option><option value="restored">Возвращено</option><option value="review">Проверить визуально</option></select><button id="export">Экспорт решений JSON</button></div>
<div class="pages">Контактные листы PNG: {page_links}</div></div>
<main class="grid">{''.join(cards)}</main>
<script>
const state=JSON.parse(localStorage.getItem('d2tm-hd-review')||'{{}}');
document.querySelectorAll('.decision').forEach(d=>{{const k=d.dataset.key,v=state[k]||{{}};d.querySelector('input').value=v.note||'';d.querySelectorAll('button').forEach(b=>{{if(b.dataset.value===v.decision)b.classList.add('active');b.onclick=()=>{{d.querySelectorAll('button').forEach(x=>x.classList.remove('active'));b.classList.add('active');state[k]={{decision:b.dataset.value,note:d.querySelector('input').value}};localStorage.setItem('d2tm-hd-review',JSON.stringify(state));}}}});d.querySelector('input').onchange=e=>{{state[k]={{...(state[k]||{{}}),note:e.target.value}};localStorage.setItem('d2tm-hd-review',JSON.stringify(state));}}}});
function filter(){{const q=document.querySelector('#search').value.toLowerCase(),p=document.querySelector('#pack').value,s=document.querySelector('#status').value;document.querySelectorAll('.card').forEach(c=>c.classList.toggle('hidden',!!((q&&!c.dataset.search.includes(q))||(p&&c.dataset.pack!==p)||(s&&c.dataset.status!==s))))}}
document.querySelectorAll('#search,#pack,#status').forEach(x=>x.addEventListener('input',filter));
document.querySelector('#export').onclick=()=>{{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(state,null,2)],{{type:'application/json'}}));a.download='d2tm_hd_review.json';a.click();URL.revokeObjectURL(a.href)}};
</script></body></html>"""
    (output / "index.html").write_text(document, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", type=Path, default=DEFAULT_BACKUP)
    parser.add_argument("--current", type=Path, default=DEFAULT_CURRENT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--stage", type=Path, default=DEFAULT_STAGE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    if int(report.get("changed_total", -1)) != 169:
        raise ValueError("The integration report does not describe the expected 169 resources")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "old").mkdir(exist_ok=True)
    (args.output / "new").mkdir(exist_ok=True)

    records: list[dict[str, object]] = []
    for pack_report in report["packs"]:
        pack_name = str(pack_report["pack"])
        density4 = next(item for item in pack_report["densities"] if int(item["density"]) == 4)
        old_entries = read_pack(args.backup / f"{pack_name}_hd4.dat")
        new_entries = read_pack(args.current / f"{pack_name}_hd4.dat")
        stage_entries = read_pack(args.stage / f"{pack_name}_hd4.dat")
        for changed in density4["changed"]:
            target_id = int(changed["id"])
            old_entry = old_entries[target_id]
            new_entry = new_entries[target_id]
            stage_entry = stage_entries[target_id]
            expected_name = str(changed["name"])
            if old_entry.name != expected_name or new_entry.name != expected_name:
                raise ValueError(f"Entry identity mismatch: {pack_name}[{target_id}] {expected_name}")
            old_image = decode_image(old_entry.payload)
            new_image = decode_image(new_entry.payload)
            stage_image = decode_image(stage_entry.payload)
            if old_image is None or new_image is None or stage_image is None:
                raise ValueError(f"Cannot decode {pack_name}[{target_id}] {expected_name}")
            stem = f"{pack_name}_{target_id:04d}_{safe_name(expected_name)}.png"
            old_path = args.output / "old" / stem
            new_path = args.output / "new" / stem
            old_image.save(old_path, optimize=True)
            new_image.save(new_path, optimize=True)
            old_digest = rgba_digest(old_image)
            new_digest = rgba_digest(new_image)
            stage_digest = rgba_digest(stage_image)
            notes = audit_notes(old_image, new_image)
            if new_digest == old_digest:
                status = "restored"
                status_label = "ВОЗВРАЩЕНО К СТАРОМУ"
                status_color = [176, 184, 191]
            elif notes:
                status = "review"
                status_label = "ПРОВЕРИТЬ ВИЗУАЛЬНО"
                status_color = [237, 159, 104]
            elif new_digest != stage_digest:
                status = "later"
                status_label = "ДОРАБОТАНО ПОЗЖЕ"
                status_color = [110, 200, 237]
            else:
                status = "batch"
                status_label = "ПАКЕТНАЯ ВЕРСИЯ"
                status_color = [135, 201, 135]
            if expected_name in RETURNED_NAMES and status != "restored":
                notes.append("ресурс предполагалось вернуть к старой версии, но пиксели отличаются")
                status = "review"
                status_label = "ПРОВЕРИТЬ ВОЗВРАТ"
                status_color = [237, 159, 104]
            records.append({
                "pack": pack_name,
                "category": PACK_TITLES.get(pack_name, pack_name),
                "id": target_id,
                "name": expected_name,
                "old_file": old_path.relative_to(args.output).as_posix(),
                "new_file": new_path.relative_to(args.output).as_posix(),
                "old_size": list(old_image.size),
                "new_size": list(new_image.size),
                "status": status,
                "status_label": status_label,
                "status_color": status_color,
                "notes": notes,
                "old_digest": old_digest,
                "new_digest": new_digest,
                "stage_digest": stage_digest,
            })

    records.sort(key=lambda item: (str(item["pack"]), int(item["id"])))
    if len(records) != 169:
        raise AssertionError(f"Expected 169 records, got {len(records)}")
    page_files = build_contact_pages(records, args.output)
    build_html(records, page_files, args.output)
    (args.output / "report.json").write_text(json.dumps({"format": 1, "count": len(records), "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.output / "report.csv").open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(["pack", "id", "name", "status", "notes", "old_file", "new_file"])
        for record in records:
            writer.writerow([record["pack"], record["id"], record["name"], record["status"], " | ".join(record["notes"]), record["old_file"], record["new_file"]])
    counts: dict[str, int] = {}
    for record in records:
        counts[str(record["status"])] = counts.get(str(record["status"]), 0) + 1
    print(json.dumps({"count": len(records), "pages": len(page_files), "statuses": counts, "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
