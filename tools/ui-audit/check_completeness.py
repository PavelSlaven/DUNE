import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import combos

RESOLUTIONS = ("1024x768", "1280x720", "1366x768", "1600x900", "1920x1080", "2560x1440")
LANGUAGES = ("ru", "en")
GRAPHICS = ("hd", "classic")


def all_combos():
    return [f"{r}/{l}/{g}" for r in RESOLUTIONS for l in LANGUAGES for g in GRAPHICS]


def check(root, scenes, flagged, combo_ids):
    return check_combinations(root, scenes, flagged, [combos.legacy_combo(c) for c in combo_ids])


def check_combinations(root, scenes, flagged, combo_list, required=None):
    root = Path(root)
    problems = []
    for combo in combo_list:
        identifier = combos.combo_id(combo)
        combo_scenes = combos.scenes_for(combo, scenes)
        expected_png = {
            f"png/{identifier}/{scene['id']}.png"
            for scene in combo_scenes
            if (combos.keep_png(combo, scene, flagged) if combo["legacy"] or required is None
                else (identifier, scene["id"]) in required)
        }
        for relative in sorted(expected_png):
            if not (root / relative).is_file():
                problems.append(("missing-png", relative))
        png_dir = root / "png" / identifier
        if png_dir.is_dir():
            for path in sorted(png_dir.glob("*.png")):
                relative = path.relative_to(root).as_posix()
                if relative not in expected_png:
                    problems.append(("extra-png", relative))
        for scene in combo_scenes:
            relative = f"logs/{identifier}/{scene['id']}.geometry.jsonl"
            if not (root / relative).is_file():
                problems.append(("missing-log", relative))
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check that every expected PNG and log exists.")
    parser.add_argument("root")
    parser.add_argument("--catalog", required=True, help="JSON printed by the game with --ui-audit-list")
    parser.add_argument("--flags", help="JSON of flags written by check_geometry.py")
    parser.add_argument("--order", help="order.json written by run_all.py: every combination in capture order")
    args = parser.parse_args(argv)
    scenes = json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]
    flags = json.loads(Path(args.flags).read_text(encoding="utf-8")) if args.flags else []
    flagged = {(flag["combo"], flag["scene"]) for flag in flags}
    if args.order:
        order = json.loads(Path(args.order).read_text(encoding="utf-8"))
        problems = check_combinations(Path(args.root), scenes, flagged, [combos.parse_id(i) for i in order],
                                      combos.png_required(flags, order))
    else:
        problems = check(Path(args.root), scenes, flagged, all_combos())
    for kind, relative in problems:
        print(f"{kind}: {relative}")
    print(f"completeness: {'OK' if not problems else 'FAIL'}; problems: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
