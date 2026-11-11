import argparse
import json
import statistics
import sys
from pathlib import Path

from PIL import Image


def lum(rgb):
    total = 0.0
    for c, k in zip(rgb[:3], (0.2126, 0.7152, 0.0722)):
        v = c / 255
        total += k * (v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return total


def contrast(img, scale, rec):
    iw, ih = img.size
    x0 = round(rec["x"] * scale)
    y0 = round(rec["y"] * scale)
    x1 = round((rec["x"] + rec["w"]) * scale)
    y1 = round((rec["y"] + rec["h"]) * scale)
    ring = max(1, round(2 * scale))
    ox0, oy0 = max(0, x0 - ring), max(0, y0 - ring)
    ox1, oy1 = min(iw, x1 + ring), min(ih, y1 + ring)
    ix0, iy0, ix1, iy1 = max(0, x0), max(0, y0), min(iw, x1), min(ih, y1)
    if ix1 <= ix0 or iy1 <= iy0:
        return None
    px = img.load()
    ringl = []
    for y in range(oy0, oy1):
        for x in range(ox0, ox1):
            if not (ix0 <= x < ix1 and iy0 <= y < iy1):
                ringl.append(lum(px[x, y]))
    inner = [lum(px[x, y]) for y in range(iy0, iy1) for x in range(ix0, ix1)]
    if not ringl or not inner:
        return None
    bg = statistics.median(ringl)
    inner.sort(key=lambda v: abs(v - bg), reverse=True)
    n = max(1, round(len(inner) * 0.15))
    fg = sum(inner[:n]) / n
    return (max(fg, bg) + 0.05) / (min(fg, bg) + 0.05)


def read_log(path):
    recs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            recs.append(json.loads(line))
    return recs


def measure_scene(scene, recs, img):
    canvas_w = 800
    for r in recs:
        if r.get("k") == "header":
            canvas_w = r["canvas"]["w"]
            break
    scale = img.size[0] / canvas_w
    rows = []
    for r in recs:
        k = r.get("k")
        if k == "text" and r.get("s") and r["w"] >= 2 and r["h"] >= 2:
            c = contrast(img, scale, r)
            rows.append((scene, "text", r["s"], r["x"], r["y"], r["w"], r["h"], r["h"], c))
        elif k == "click":
            rows.append((scene, "click", r["name"], r["x"], r["y"], r["w"], r["h"], min(r["w"], r["h"]), None))
    return rows


def summary(rows, nscenes):
    out = [f"scenes: {nscenes}"]
    texts = sorted((r for r in rows if r[1] == "text"), key=lambda r: r[7])
    clicks = sorted((r for r in rows if r[1] == "click"), key=lambda r: r[7])
    out.append(f"text records: {len(texts)}")
    if texts:
        out.append(f"min text height: {texts[0][7]}")
        out.append("5 smallest text:")
        out += [f"  {r[0]}\t{r[2]!r}\t{r[7]}" for r in texts[:5]]
    out.append(f"click records: {len(clicks)}")
    if clicks:
        out.append(f"min click side: {clicks[0][7]}")
        out.append("5 smallest click:")
        out += [f"  {r[0]}\t{r[2]}\t{r[5]}x{r[6]}" for r in clicks[:5]]
    cs = sorted((r for r in texts if r[8] is not None), key=lambda r: r[8])
    if cs:
        vals = [r[8] for r in cs]
        p5 = vals[min(len(vals) - 1, int(0.05 * len(vals)))]
        out.append(f"contrast records: {len(vals)}")
        out.append(f"contrast min: {vals[0]:.2f}  p5: {p5:.2f}  median: {statistics.median(vals):.2f}")
        out.append(f"contrast < 4.5: {sum(v < 4.5 for v in vals)}  < 3.0: {sum(v < 3.0 for v in vals)}")
        out.append("10 lowest contrast:")
        out += [f"  {r[0]}\t{r[2]!r}\t{r[8]:.2f}" for r in cs[:10]]
    return "\n".join(out)


def selftest():
    img = Image.new("RGB", (200, 100), (0, 0, 0))
    for y in range(40, 60):
        for x in range(50, 150):
            img.putpixel((x, y), (255, 255, 255))
    recs = [{"k": "header", "canvas": {"w": 200, "h": 100}},
            {"k": "text", "s": "X", "x": 50, "y": 40, "w": 100, "h": 20}]
    rows = measure_scene("t", recs, img)
    assert len(rows) == 1 and rows[0][7] == 20
    assert rows[0][8] > 20, rows[0][8]
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs")
    ap.add_argument("--png")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    logs, pngs = Path(a.logs), Path(a.png)
    rows = []
    n = 0
    for lp in sorted(logs.glob("*.geometry.jsonl")):
        scene = lp.name[: -len(".geometry.jsonl")]
        pp = pngs / f"{scene}.png"
        if not pp.exists():
            print(f"no png for {scene}", file=sys.stderr)
            continue
        with Image.open(pp) as im:
            rows += measure_scene(scene, read_log(lp), im.convert("RGB"))
        n += 1
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        f.write("scene\tkind\tname\tx\ty\tw\th\tsize\tcontrast\n")
        for r in rows:
            f.write("\t".join("" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v)) for v in r) + "\n")
    print(summary(rows, n))


if __name__ == "__main__":
    main()
