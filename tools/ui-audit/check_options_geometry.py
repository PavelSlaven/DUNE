#!/usr/bin/env python3
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_geometry

OPTIONS_SCENES = (
    "options-menu-main",
    "options-game-main-saves",
    "options-game-main-nosaves",
)


def is_gui(record, type_):
    return record.get("k") == "gui" and record.get("t") == type_


def is_button(record):
    return is_gui(record, "GuiButton")


def is_window(record):
    return is_gui(record, "GuiWindow")


def check_rule3(header, records):
    elements = [record for record in records if record.get("k") in ("gui", "area")]
    flags = []
    for index, first in enumerate(elements):
        first_rect = check_geometry.rect_of(first)
        for second in elements[index + 1:]:
            second_rect = check_geometry.rect_of(second)
            if not check_geometry.intersects(first_rect, second_rect):
                continue
            button_pair = is_button(first) or is_button(second)
            window_button_pair = ((is_window(first) and is_button(second))
                                  or (is_button(first) and is_window(second)))
            if window_button_pair:
                window = first if is_window(first) else second
                button = second if is_button(second) else first
                if check_geometry.contains(check_geometry.rect_of(window), check_geometry.rect_of(button)):
                    continue
            if button_pair or (not check_geometry.contains(first_rect, second_rect)
                               and not check_geometry.contains(second_rect, first_rect)):
                flags.append(check_geometry.make_flag(header, 3, first_rect, second_rect, (), [first, second]))
    return flags


def check_log(path):
    header, records = check_geometry.load_log(path)
    if header.get("scene") not in OPTIONS_SCENES:
        return []
    flags = check_rule3(header, records)
    flags.extend(flag for flag in check_geometry.check_extra_records(header, records)
                 if flag["rule"] == 9)
    return flags


def planned_pairs(plan_path=None, combos_path=None):
    if combos_path:
        combos = [line.strip() for line in Path(combos_path).read_text(encoding="utf-8").splitlines()
                  if line.strip()]
        return Counter((combo, scene) for combo in combos for scene in OPTIONS_SCENES)
    entries = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError(f"{plan_path}: audit plan must be a list of combo/scene entries")
    pairs = []
    for entry in entries:
        if not isinstance(entry, dict) or "combo" not in entry or "scene" not in entry:
            raise ValueError(f"{plan_path}: each audit plan entry must have combo and scene")
        if entry["scene"] in OPTIONS_SCENES:
            pairs.append((entry["combo"], entry["scene"]))
    return Counter(pairs)


def check_tree(logs_root, expected):
    actual = Counter()
    flags = []
    for path in sorted(Path(logs_root).rglob("*.geometry.jsonl")):
        header, _ = check_geometry.load_log(path)
        scene = header.get("scene")
        if scene not in OPTIONS_SCENES:
            continue
        actual[(check_geometry.combo_of(header), scene)] += 1
        for flag in check_log(path):
            flag["log"] = path.as_posix()
            flags.append(flag)
    missing = expected - actual
    extra = actual - expected
    return actual, flags, missing, extra


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check options-window logs with audit rules 3 and 9.")
    parser.add_argument("logs_root")
    plan = parser.add_mutually_exclusive_group(required=True)
    plan.add_argument("--plan", help="audit-plan.json emitted by run_all.py")
    plan.add_argument("--combos", help="one planned audit combo id per line")
    args = parser.parse_args(argv)

    expected = planned_pairs(args.plan, args.combos)
    actual, flags, missing, extra = check_tree(args.logs_root, expected)
    for flag in flags:
        print(check_geometry.format_flag(flag))
    actual_count, expected_count = sum(actual.values()), sum(expected.values())
    print(f"logs: {actual_count}; planned: {expected_count}; flags: {len(flags)}; "
          f"rule 3: {sum(flag['rule'] == 3 for flag in flags)}; "
          f"rule 9: {sum(flag['rule'] == 9 for flag in flags)}")
    if missing or extra:
        print(f"plan mismatch: missing={sorted(missing.elements())}; extra={sorted(extra.elements())}",
              file=sys.stderr)
    return 1 if missing or extra or flags else 0


if __name__ == "__main__":
    sys.exit(main())
