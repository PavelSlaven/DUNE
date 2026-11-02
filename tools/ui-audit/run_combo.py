#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_geometry
import combos

RUNTIME_LINKS = ("campaign", "campaign_en", "data", "skirmish", "skirmish_en")
FULL_RESOLUTIONS = ("1024x768", "1920x1080")
SCENE_TIMEOUT_SECONDS = 90
SCENE_ATTEMPTS = 2
MIN_FREE_GB = 5
EXIT_LOW_DISK = 3


def free_gb(path):
    return shutil.disk_usage(path).free / (1024 ** 3)


def apply_settings(text, values):
    for key, value in values.items():
        pattern = re.compile(rf"^{key}\s*=.*$", re.MULTILINE)
        line = f"{key}={value}"
        if pattern.search(text):
            text = pattern.sub(line, text, count=1)
        else:
            text = text.replace("[SETTINGS]", f"[SETTINGS]\n{line}", 1)
    return text


def split_resolution(combo):
    width, height = combo["resolution"].split("x")
    return int(width), int(height)


def make_runtime(executable, resources, directory, combo):
    width, height = split_resolution(combo)
    runtime = Path(directory)
    if runtime.exists():
        shutil.rmtree(runtime)
    runtime.mkdir(parents=True)
    shutil.copy2(executable, runtime / "d2tm")
    bin_dir = Path(resources) / "bin"
    for name in RUNTIME_LINKS:
        os.symlink(bin_dir / name, runtime / name)
    shutil.copy2(Path(resources) / "game.ini", runtime / "game.ini")
    settings = apply_settings((bin_dir / "settings.ini").read_text(encoding="utf-8"), {
        "ScreenWidth": width,
        "ScreenHeight": height,
        "FullScreen": "false",
        "RenderScale": combo["render"],
        "WorldScale": combo["world"],
        "GraphicsMode": "HD" if combo["graphics"] == "hd" else "Classic",
        "Language": combo["language"],
    })
    (runtime / "settings.ini").write_text(settings, encoding="utf-8")
    return runtime


def game_environment():
    environment = dict(os.environ)
    environment.update(SDL_VIDEODRIVER="dummy", SDL_RENDER_DRIVER="software", SDL_AUDIODRIVER="dummy")
    return environment


def run_scene(runtime, combo, scene_id, out_dir):
    width, height = split_resolution(combo)
    command = [
        str(runtime / "d2tm"), "-windowed", "-screenWidth", str(width), "-screenHeight", str(height),
        "--ui-audit-scene", scene_id, "--ui-audit-out", str(out_dir),
    ]
    return subprocess.run(command, cwd=runtime, env=game_environment(), check=False,
                          capture_output=True, text=True, timeout=SCENE_TIMEOUT_SECONDS)


def list_scenes(executable):
    result = subprocess.run([str(executable), "--ui-audit-list"], env=game_environment(), check=True,
                            capture_output=True, text=True, timeout=60)
    return json.loads(result.stdout)["scenes"]


def load_order(out_root):
    path = Path(out_root) / "order.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []


def has_new_flag(out_root, order, combo, scene_id, log_path):
    flags = check_geometry.check_log(log_path)
    identifier = combos.combo_id(combo)
    if not flags or combo["legacy"] or identifier not in order:
        return bool(flags)
    seen = set()
    for earlier in combos.earlier_ids(order, identifier):
        earlier_log = Path(out_root) / "logs" / earlier / f"{scene_id}.geometry.jsonl"
        if earlier_log.is_file():
            seen.update(combos.flag_key(flag) for flag in check_geometry.check_log(earlier_log))
    return any(combos.flag_key(flag) not in seen for flag in flags)


def run_combo(executable, resources, combo, out_root, scenes, only=None, work_root=None):
    identifier = combos.combo_id(combo)
    out_root = Path(out_root)
    order = load_order(out_root)
    png_dir = out_root / "png" / identifier
    log_dir = out_root / "logs" / identifier
    png_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    work = Path(work_root or out_root / "work") / identifier.replace("/", "_")
    runtime = make_runtime(executable, resources, work / "runtime", combo)
    failures = []
    for scene in combos.scenes_for(combo, scenes):
        if only is not None and scene["id"] not in only:
            continue
        scene_out = work / "out"
        if scene_out.exists():
            shutil.rmtree(scene_out)
        scene_out.mkdir(parents=True)
        started = time.time()
        ok = False
        message = ""
        for _ in range(SCENE_ATTEMPTS):
            try:
                result = run_scene(runtime, combo, scene["id"], scene_out)
                ok = result.returncode == 0
                message = result.stderr.strip()[-300:]
                break
            except subprocess.TimeoutExpired:
                message = "timeout"
        png = scene_out / f"{scene['id']}.png"
        log = scene_out / f"{scene['id']}.geometry.jsonl"
        if not ok or not png.is_file() or not log.is_file():
            failures.append((scene["id"], message))
            continue
        shutil.move(log, log_dir / log.name)
        flagged = {(identifier, scene["id"])} if has_new_flag(out_root, order, combo, scene["id"], log_dir / log.name) else set()
        if only is not None or combos.keep_png(combo, scene, flagged):
            shutil.move(png, png_dir / png.name)
        elif (png_dir / png.name).exists():
            (png_dir / png.name).unlink()
        print(f"{identifier} {scene['id']} {time.time() - started:.1f}s", flush=True)
    shutil.rmtree(work, ignore_errors=True)
    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(description="Capture all scenes for one resolution/language/graphics combination.")
    parser.add_argument("--exe", required=True)
    parser.add_argument("--resources", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--combo", required=True, help="WxH/lang/gfx or WxH/lang/gfx/r<R>w<W>, for example 1024x768/ru/hd")
    parser.add_argument("--scene", action="append", help="limit to these scene ids")
    parser.add_argument("--flags", help="flags JSON: capture only the flagged scenes of this combination, with PNG")
    parser.add_argument("--min-free-gb", type=float, default=MIN_FREE_GB)
    args = parser.parse_args(argv)
    args.exe = str(Path(args.exe).resolve())
    args.resources = str(Path(args.resources).resolve())
    args.out = str(Path(args.out).resolve())
    Path(args.out).mkdir(parents=True, exist_ok=True)
    free = free_gb(args.out)
    if free < args.min_free_gb:
        print(f"low disk space: {free:.1f} GB free, need {args.min_free_gb} GB", file=sys.stderr)
        return EXIT_LOW_DISK
    scenes = list_scenes(args.exe)
    combo = combos.parse_id(args.combo)
    only = set(args.scene) if args.scene else None
    if args.flags:
        flagged = {f["scene"] for f in json.loads(Path(args.flags).read_text(encoding="utf-8"))
                   if f["combo"] == args.combo}
        only = flagged if only is None else only & flagged
    failures = run_combo(args.exe, args.resources, combo, args.out, scenes, only)
    for scene_id, message in failures:
        print(f"FAILED {args.combo} {scene_id}: {message}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
