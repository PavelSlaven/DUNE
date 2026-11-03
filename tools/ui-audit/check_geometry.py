import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

RULE_NAMES = {
    1: "outside-canvas",
    2: "text-across-element",
    3: "elements-overlap",
    4: "text-on-text",
    5: "text-larger-than-box",
    6: "differs-between-resolutions",
    7: "label-over-panel",
    8: "labels-of-one-object-overlap",
    9: "click-zones-overlap",
    10: "key-conflict",
}


def rect_of(record):
    return {"x": record["x"], "y": record["y"], "w": record["w"], "h": record["h"]}


def intersects(a, b):
    return (min(a["x"] + a["w"], b["x"] + b["w"]) > max(a["x"], b["x"])
            and min(a["y"] + a["h"], b["y"] + b["h"]) > max(a["y"], b["y"]))


def contains(outer, inner):
    return (outer["x"] <= inner["x"] and outer["y"] <= inner["y"]
            and inner["x"] + inner["w"] <= outer["x"] + outer["w"]
            and inner["y"] + inner["h"] <= outer["y"] + outer["h"])


def has_area(rect):
    return rect["w"] > 0 and rect["h"] > 0


def combo_of(header):
    base = f"{header['resolution']}/{header['language']}/{header['graphics']}"
    render, world = header.get("render_scale", 0), header.get("world_scale", 0)
    if render or world:
        return f"{base}/r{render}w{world}"
    return base


def name_of(record):
    return record.get({"text": "s", "gui": "t", "area": "n", "click": "name", "label": "kind"}[record["k"]], "")


def make_flag(header, rule, a=None, b=None, texts=(), names=()):
    return {
        "rule": rule,
        "scene": header["scene"],
        "combo": combo_of(header),
        "a": a,
        "b": b,
        "texts": list(texts),
        "names": [name_of(record) for record in names],
    }


def check_records(header, records):
    canvas = {"x": 0, "y": 0, "w": header["canvas"]["w"], "h": header["canvas"]["h"]}
    texts = [r for r in records if r["k"] == "text"]
    elements = [r for r in records if r["k"] in ("gui", "area")]
    flags = []

    for record in records:
        if record["k"] in ("text", "gui", "area") and not contains(canvas, rect_of(record)):
            label = record.get("s", record.get("t", record.get("n", "")))
            flags.append(make_flag(header, 1, rect_of(record), None,
                                   [label] if record["k"] == "text" else [], [record]))

    for text in texts:
        text_rect = rect_of(text)
        for element in elements:
            element_rect = rect_of(element)
            if (has_area(element_rect) and intersects(text_rect, element_rect)
                    and not contains(element_rect, text_rect)):
                flags.append(make_flag(header, 2, text_rect, element_rect, [text["s"]], [text, element]))

    for index, first in enumerate(elements):
        first_rect = rect_of(first)
        for second in elements[index + 1:]:
            second_rect = rect_of(second)
            if (intersects(first_rect, second_rect)
                    and not contains(first_rect, second_rect)
                    and not contains(second_rect, first_rect)):
                flags.append(make_flag(header, 3, first_rect, second_rect, (), [first, second]))

    for index, first in enumerate(texts):
        first_rect = rect_of(first)
        for second in texts[index + 1:]:
            second_rect = rect_of(second)
            if intersects(first_rect, second_rect):
                flags.append(make_flag(header, 4, first_rect, second_rect, [first["s"], second["s"]], [first, second]))

    for text in texts:
        box = text.get("box")
        if box is not None and (text["w"] > box["w"] or text["h"] > box["h"]):
            flags.append(make_flag(header, 5, rect_of(text), dict(box), [text["s"]], [text]))

    return flags


def check_extra_records(header, records):
    flags = []
    panels = []
    labels = []
    zones = []
    for record in records:
        kind = record["k"]
        if kind == "area":
            panels.append(record)
        elif kind == "label":
            rect = rect_of(record)
            for panel in panels:
                if has_area(rect) and intersects(rect, rect_of(panel)):
                    flags.append(make_flag(header, 7, rect, rect_of(panel), [record["kind"], panel["n"]], [record, panel]))
            labels.append(record)
        elif kind == "click":
            zones.append(record)
    for index, first in enumerate(labels):
        for second in labels[index + 1:]:
            if (first["obj"] == second["obj"] and first["type"] == second["type"]
                    and intersects(rect_of(first), rect_of(second))):
                flag = make_flag(header, 8, rect_of(first), rect_of(second), [first["kind"], second["kind"]], [first, second])
                flag["obj"] = first["obj"]
                flag["type"] = first["type"]
                flags.append(flag)
    for index, first in enumerate(zones):
        for second in zones[index + 1:]:
            if intersects(rect_of(first), rect_of(second)):
                flags.append(make_flag(header, 9, rect_of(first), rect_of(second), [first["name"], second["name"]], [first, second]))
    return flags


def summarize_rule8(logs):
    totals = defaultdict(set)
    crossing = defaultdict(set)
    for header, records in logs:
        combo = combo_of(header)
        labels = [r for r in records if r["k"] == "label"]
        for record in labels:
            totals[record["type"]].add((combo, header["scene"], record["obj"]))
        for index, first in enumerate(labels):
            for second in labels[index + 1:]:
                if (first["obj"] == second["obj"] and first["type"] == second["type"]
                        and intersects(rect_of(first), rect_of(second))):
                    pair = tuple(sorted((first["kind"], second["kind"])))
                    crossing[(first["type"], pair)].add((combo, header["scene"], first["obj"]))
    return [
        {"type": type_, "kinds": list(pair), "objects_intersecting": len(objects),
         "objects_total": len(totals[type_])}
        for (type_, pair), objects in sorted(crossing.items())
    ]


def load_log(path):
    lines = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines or lines[0].get("k") != "header":
        raise ValueError(f"{path}: the first record is not a header")
    return lines[0], lines[1:]


def check_log(path):
    header, records = load_log(path)
    return check_records(header, records) + check_extra_records(header, records)


def content_key(header, records):
    kinds = ("text", "gui") if header.get("game_screen") else ("text", "gui", "area")
    return sorted(json.dumps(r, sort_keys=True) for r in records if r["k"] in kinds)


def compare_resolutions(logs):
    groups = defaultdict(list)
    for header, records in logs:
        key = (header["scene"], header["canvas"]["w"], header["canvas"]["h"],
               header["language"], header["graphics"])
        groups[key].append((header, content_key(header, records)))
    flags = []
    for members in groups.values():
        members.sort(key=lambda member: member[0]["resolution"])
        base_header, base_content = members[0]
        for header, content in members[1:]:
            if content != base_content:
                flag = make_flag(header, 6)
                flag["other"] = combo_of(base_header)
                flags.append(flag)
    return flags


def format_flag(flag):
    parts = [f"{flag['scene']}", f"{flag['combo']}", f"rule {flag['rule']} ({RULE_NAMES[flag['rule']]})"]
    for key in ("a", "b"):
        rect = flag.get(key)
        if rect:
            parts.append(f"{key}={rect['x']},{rect['y']} {rect['w']}x{rect['h']}")
    if flag.get("other"):
        parts.append(f"differs from {flag['other']}")
    if flag.get("type"):
        parts.append(f"object={flag['type']}#{flag['obj']}")
    if flag.get("texts"):
        parts.append("texts=" + " | ".join(t.replace("\n", " ") for t in flag["texts"]))
    return "; ".join(parts)


def check_tree(logs_root):
    loaded = []
    flags = []
    for path in sorted(Path(logs_root).rglob("*.geometry.jsonl")):
        header, records = load_log(path)
        loaded.append((header, records))
        for flag in check_records(header, records) + check_extra_records(header, records):
            flag["log"] = path.as_posix()
            flags.append(flag)
    flags.extend(compare_resolutions(loaded))
    return len(loaded), flags


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check UI geometry logs against rules 1-9.")
    parser.add_argument("logs_root")
    parser.add_argument("--json", dest="json_out")
    parser.add_argument("--txt", dest="txt_out")
    parser.add_argument("--summary8", dest="summary8_out")
    args = parser.parse_args(argv)
    count, flags = check_tree(args.logs_root)
    lines = [format_flag(flag) for flag in flags]
    if args.txt_out:
        Path(args.txt_out).write_text("".join(line + "\n" for line in lines), encoding="utf-8")
    else:
        for line in lines:
            print(line)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(flags, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.summary8_out:
        summary_logs = [load_log(path) for path in sorted(Path(args.logs_root).rglob("*.geometry.jsonl"))]
        Path(args.summary8_out).write_text(
            json.dumps(summarize_rule8(summary_logs), ensure_ascii=False, indent=1), encoding="utf-8")
    per_rule = {rule: sum(1 for flag in flags if flag["rule"] == rule) for rule in RULE_NAMES if rule != 10}
    summary = ", ".join(f"rule {rule}: {number}" for rule, number in per_rule.items())
    print(f"logs: {count}; flags: {len(flags)}; {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
