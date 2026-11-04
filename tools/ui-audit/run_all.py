#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import zip_longest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import combos
import run_combo

WORKERS = 16
MIN_FREE_GB = 5


def scales_for(executable, resolutions):
    scales = {}
    for resolution in resolutions:
        result = subprocess.run([str(executable), "--ui-audit-scales", resolution], env=run_combo.game_environment(),
                                check=True, capture_output=True, text=True, timeout=60)
        _, render, world = combos.parse_scales(result.stdout)
        scales[resolution] = {"render": [value for value in render if value], "world": [value for value in world if value]}
    return scales


def interleave(chains):
    result = []
    for row in zip_longest(*chains):
        result.extend(item for item in row if item is not None)
    return result


def plan(all_combos):
    old = [combo for combo in all_combos if combo["legacy"]]
    chains = {}
    for combo in all_combos:
        if not combo["legacy"]:
            chains.setdefault(combo["resolution"], []).append(combo)
    return old + interleave(list(chains.values()))


def audit_log_plan(ordered, scenes):
    return [
        {"combo": combos.combo_id(combo), "scene": scene["id"]}
        for combo in ordered
        for scene in combos.scenes_for(combo, scenes)
    ]


def done_marker(out_root, combo):
    return Path(out_root) / "done" / combos.combo_id(combo).replace("/", "_")


def combo_bytes(out_root, combo):
    identifier = combos.combo_id(combo)
    total = 0
    for kind in ("logs", "png"):
        directory = Path(out_root) / kind / identifier
        if directory.is_dir():
            total += sum(path.stat().st_size for path in directory.iterdir() if path.is_file())
    return total


def forecast_gb(finished_bytes, finished_scenes, remaining_scenes):
    if finished_scenes == 0:
        return 0.0
    return finished_bytes / finished_scenes * remaining_scenes / (1024 ** 3)


def run_one(args, combo, journal):
    identifier = combos.combo_id(combo)
    free = run_combo.free_gb(args.out)
    journal.write(f"{time.strftime('%F %T')} free {free:.1f} GB before {identifier}\n")
    journal.flush()
    if free < args.min_free_gb:
        return identifier, 3
    log_path = Path(args.out) / "run" / (identifier.replace("/", "_") + ".txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, str(Path(__file__).resolve().parent / "run_combo.py"), "--exe", args.exe,
               "--resources", args.resources, "--out", args.out, "--combo", identifier,
               "--min-free-gb", str(args.min_free_gb)]
    with open(log_path, "w", encoding="utf-8") as log:
        code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    if code == 0:
        marker = done_marker(args.out, combo)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("ok\n", encoding="utf-8")
    return identifier, code


def main(argv=None):
    parser = argparse.ArgumentParser(description="Capture all combinations, 16 at a time, skipping finished ones.")
    parser.add_argument("--exe", required=True)
    parser.add_argument("--resources", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--resolutions", default="1024x768,1280x720,1366x768,1600x900,1920x1080,2560x1440")
    parser.add_argument("--limit", type=int, help="run only this many unfinished combinations of the plan")
    parser.add_argument("--workers", type=int, default=WORKERS)
    parser.add_argument("--min-free-gb", type=float, default=MIN_FREE_GB)
    parser.add_argument("--only", action="append", help="run only this combination id (repeatable)")
    parser.add_argument("--list", action="store_true", help="print the plan and exit")
    args = parser.parse_args(argv)
    args.exe = str(Path(args.exe).resolve())
    args.resources = str(Path(args.resources).resolve())
    args.out = str(Path(args.out).resolve())
    Path(args.out).mkdir(parents=True, exist_ok=True)
    scales = scales_for(args.exe, args.resolutions.split(","))
    generated = combos.generate(scales)
    ordered = plan(generated)
    if args.list:
        for combo in ordered:
            print(combos.combo_id(combo))
        print(f"combinations: {len(ordered)}; new: {sum(1 for c in ordered if not c['legacy'])}")
        return 0
    (Path(args.out) / "order.json").write_text(json.dumps([combos.combo_id(c) for c in generated]), encoding="utf-8")
    scenes = json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]
    log_plan = audit_log_plan(ordered, scenes)
    (Path(args.out) / "audit-plan.json").write_text(
        json.dumps(log_plan, ensure_ascii=False, indent=1), encoding="utf-8")
    pending = [combo for combo in ordered if not done_marker(args.out, combo).exists()]
    if args.only:
        pending = [combo for combo in pending if combos.combo_id(combo) in args.only]
    if args.limit is not None:
        pending = pending[:args.limit]
    failed = []
    with open(Path(args.out) / "free-space.txt", "a", encoding="utf-8") as journal:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for identifier, code in pool.map(lambda combo: run_one(args, combo, journal), pending):
                print(f"{identifier} exit={code}", flush=True)
                if code != 0:
                    failed.append((identifier, code))
    finished = [combo for combo in ordered if done_marker(args.out, combo).exists()]
    finished_bytes = sum(combo_bytes(args.out, combo) for combo in finished)
    forecast = 0.0
    for legacy in (True, False):
        done = [combo for combo in finished if combo["legacy"] == legacy]
        rest = [combo for combo in ordered if combo["legacy"] == legacy and combo not in finished]
        forecast += forecast_gb(sum(combo_bytes(args.out, combo) for combo in done),
                                sum(len(combos.scenes_for(combo, scenes)) for combo in done),
                                sum(len(combos.scenes_for(combo, scenes)) for combo in rest))
    print(f"finished: {len(finished)}/{len(ordered)}; bytes: {finished_bytes}; "
          f"forecast of the rest: {forecast:.2f} GB; "
          f"free now: {run_combo.free_gb(args.out):.1f} GB")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
