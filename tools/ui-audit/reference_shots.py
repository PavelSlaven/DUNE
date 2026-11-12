#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CELL_MAX_WIDTH = 1280
HEADER_HEIGHT = 28
GAP = 16
BACKGROUND = (24, 24, 24)
TEXT = (235, 235, 235)
PLACEHOLDER = (40, 40, 40)
SCENE_TIMEOUT_SECONDS = 120
SCENE_ATTEMPTS = 2
LIST_TIMEOUT_SECONDS = 60
TABLE_HEADER = (
    "pair", "resolution", "old_scene", "new_scene", "old_exit", "new_exit",
    "old_png_size", "new_png_size", "old_canvas", "new_canvas", "old_png",
    "new_png", "sheet", "problems",
)
GALLERY_HEADER = ("file", "scene", "resolution", "exit", "png_size", "canvas", "problems")
SAVE_WRITING_FORK_SCENES = frozenset(
    {
        "main-menu-saves", "save-dialog-menu", "options-game-main-saves", "options-game-applied",
        "options-game-game", "options-game-controls", "options-game-diagnostics", "options-game-keybind",
        "save-dialog-load", "save-dialog-save-new", "save-dialog-overwrite", "save-dialog-load-error",
        "save-dialog-save-error",
    }
)

Pair = namedtuple("Pair", "name fork_scene port_scene resolutions note")
GalleryRow = namedtuple("GalleryRow", "file port_scene resolution")
CellResult = namedtuple("CellResult", "exit_code png size canvas header problems")

PAIR_HEADER = ("pair", "fork_scene", "port_scene", "resolutions", "note")
PAIR_RESOLUTION = re.compile(r"\d+x\d+\Z")
GALLERY_FILE_HEADER = ("file", "port_scene", "resolution")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def parse_pairs(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if not lines or tuple(lines[0].split("\t")) != PAIR_HEADER:
        raise ValueError("invalid pair table header")
    pairs = []
    names = set()
    for line in lines[1:]:
        if not line:
            continue
        fields = line.split("\t")
        if len(fields) != 5:
            raise ValueError("invalid pair table row")
        name, fork_scene, port_scene, resolutions, note = fields
        if name in names:
            raise ValueError(f"duplicate pair: {name}")
        if port_scene == "-":
            raise ValueError(f"missing port scene: {name}")
        if fork_scene != "-" and fork_scene in SAVE_WRITING_FORK_SCENES:
            raise ValueError(f"fork scene writes saves: {fork_scene}")
        parsed_resolutions = []
        for value in resolutions.split(","):
            if PAIR_RESOLUTION.fullmatch(value) is None:
                raise ValueError(f"invalid resolution: {value}")
            width, height = value.split("x")
            parsed_resolutions.append((int(width), int(height)))
        names.add(name)
        pairs.append(
            Pair(name, None if fork_scene == "-" else fork_scene, port_scene, parsed_resolutions, note)
        )
    return pairs


def parse_gallery(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if not lines or tuple(lines[0].split("\t")) != GALLERY_FILE_HEADER:
        raise ValueError("invalid gallery table header")
    rows = []
    files = set()
    for line in lines[1:]:
        if not line:
            continue
        fields = line.split("\t")
        if len(fields) != 3:
            raise ValueError("invalid gallery table row")
        file, port_scene, resolution = fields
        if file in files:
            raise ValueError(f"duplicate gallery file: {file}")
        if PAIR_RESOLUTION.fullmatch(resolution) is None:
            raise ValueError(f"invalid resolution: {resolution}")
        width, height = resolution.split("x")
        files.add(file)
        rows.append(GalleryRow(file, port_scene, (int(width), int(height))))
    return rows


def executable_name(os_name):
    return "d2tm.exe" if os_name == "nt" else "d2tm"


def scene_command(executable, side, scene, width, height, out_dir, language):
    command = [
        str(executable),
        "-windowed",
        "-screenWidth",
        str(width),
        "-screenHeight",
        str(height),
        "--ui-audit-scene",
        scene,
        "--ui-audit-out",
        str(out_dir),
    ]
    if side == "new":
        command.extend(("--ui-audit-language", language))
    return command


def game_environment(base, headless, xdg):
    environment = dict(base)
    if headless:
        environment.update(
            SDL_VIDEODRIVER="dummy",
            SDL_RENDER_DRIVER="software",
            SDL_AUDIODRIVER="dummy",
            XDG_DATA_HOME=str(xdg),
        )
    return environment


def default_runner(command, cwd, env, timeout):
    return subprocess.run(
        command, cwd=cwd, env=env, check=False, capture_output=True, text=True, timeout=timeout
    )


def list_scenes(executable, runner, env):
    executable = Path(executable)
    result = runner(
        [str(executable), "--ui-audit-list"], executable.parent, env, LIST_TIMEOUT_SECONDS
    )
    if result.returncode != 0:
        raise RuntimeError(f"scene listing failed with exit={result.returncode}")
    return {scene["id"] for scene in json.loads(result.stdout)["scenes"]}


def png_size(path):
    with Path(path).open("rb") as image_file:
        data = image_file.read(24)
    if len(data) < 24 or data[:8] != PNG_SIGNATURE or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def read_header(path):
    with Path(path).open(encoding="utf-8") as geometry_file:
        line = geometry_file.readline()
    if not line:
        raise ValueError(f"empty geometry file: {path}")
    header = json.loads(line)
    if not isinstance(header, dict) or header.get("k") != "header":
        raise ValueError(f"invalid geometry header: {path}")
    return header


def cell_problems(side, exit_code, size, header, width, height, language):
    problems = []
    if exit_code != 0:
        problems.append(f"exit={exit_code}")
    if size is not None and size != (width, height):
        problems.append(f"png-size={size[0]}x{size[1]}")
    if header is not None:
        if header["render_scale"] != 0:
            problems.append(f"render-scale={header['render_scale']}")
        if header["world_scale"] != 0:
            problems.append(f"world-scale={header['world_scale']}")
        if side == "old" and header["language"] != language:
            problems.append(f"language={header['language']}")
    return problems


def compose_sheet(old_png, new_png, out_png, title):
    with Image.open(new_png) as new_image:
        new_width, new_height = new_image.size
        factor = min(1.0, CELL_MAX_WIDTH / new_width)
        cell_width = round(new_width * factor)
        cell_height = round(new_height * factor)
        new_cell = new_image.convert("RGB").resize((cell_width, cell_height), Image.LANCZOS)

    sheet = Image.new("RGB", (2 * cell_width + GAP, HEADER_HEIGHT + cell_height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    if old_png is None:
        draw.rectangle(
            (0, HEADER_HEIGHT, cell_width - 1, HEADER_HEIGHT + cell_height - 1), fill=PLACEHOLDER
        )
        draw.text((8, HEADER_HEIGHT + 8), "no old scene", fill=TEXT, font=ImageFont.load_default())
    else:
        with Image.open(old_png) as old_image:
            old_cell = old_image.convert("RGB").resize(
                (cell_width, cell_height), Image.LANCZOS
            )
        sheet.paste(old_cell, (0, HEADER_HEIGHT))
    sheet.paste(new_cell, (cell_width + GAP, HEADER_HEIGHT))
    draw.text((8, 8), title, fill=TEXT, font=ImageFont.load_default())
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_png, "PNG")


def capture_cell(runner, executable, side, scene, width, height, out_root, language, env):
    executable = Path(executable)
    out_cell = Path(out_root) / side / f"{width}x{height}"
    out_cell.mkdir(parents=True, exist_ok=True)
    png = out_cell / f"{scene}.png"
    geometry = out_cell / f"{scene}.geometry.jsonl"
    command = scene_command(executable, side, scene, width, height, out_cell, language)
    result = None
    for _ in range(SCENE_ATTEMPTS):
        for path in (png, geometry):
            if path.exists():
                path.unlink()
        try:
            result = runner(command, executable.parent, env, SCENE_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            shutil.rmtree(out_cell / "saves", ignore_errors=True)
            continue
        shutil.rmtree(out_cell / "saves", ignore_errors=True)
        break
    if result is None:
        return CellResult("timeout", None, None, None, None, ["timeout"])
    if not png.is_file():
        return CellResult(result.returncode, None, None, None, None, ["no-png"])
    size = png_size(png)
    if not geometry.is_file():
        return CellResult(result.returncode, png, size, None, None, ["no-geometry"])
    try:
        header = read_header(geometry)
    except ValueError:
        return CellResult(result.returncode, png, size, None, None, ["bad-geometry"])
    canvas = (header["canvas"]["w"], header["canvas"]["h"])
    problems = cell_problems(side, result.returncode, size, header, width, height, language)
    return CellResult(result.returncode, png, size, canvas, header, problems)


def _size_text(size):
    return "-" if size is None else f"{size[0]}x{size[1]}"


def _exit_text(exit_code):
    return "-" if exit_code is None else str(exit_code)


def _path_text(path, out):
    if path is None:
        return "-"
    path = Path(path)
    try:
        return path.relative_to(out).as_posix()
    except ValueError:
        return path.as_posix()


def _write_table(path, header, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(header)]
    lines.extend("\t".join(str(value) for value in row) for row in rows)
    with path.open("w", encoding="utf-8", newline="\n") as table_file:
        table_file.write("\n".join(lines) + "\n")


def run_reference(pairs, out, new_exe, old_exe, old_png_dir, language, runner, env):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    new_exe = Path(new_exe)
    new_ids = list_scenes(new_exe, runner, env)
    old_ids = list_scenes(old_exe, runner, env) if old_exe is not None else None
    rows = []
    all_ok = True
    for pair in pairs:
        for width, height in pair.resolutions:
            resolution = f"{width}x{height}"
            has_old = old_exe is not None or old_png_dir is not None
            old_scene = pair.fork_scene if has_old and pair.fork_scene is not None else None
            old_result = None
            old_png = None
            old_size = None
            old_canvas = None
            old_exit = None
            old_problems = []
            if old_scene is not None:
                if old_exe is not None:
                    if old_scene not in old_ids:
                        old_problems.append("no-scene")
                    else:
                        old_result = capture_cell(
                            runner, old_exe, "old", old_scene, width, height, out,
                            language, env,
                        )
                        old_exit = old_result.exit_code
                        old_png = old_result.png
                        old_size = old_result.size
                        old_canvas = old_result.canvas
                        old_problems.extend(old_result.problems)
                else:
                    old_path = Path(old_png_dir) / resolution / f"{old_scene}.png"
                    if not old_path.is_file():
                        old_problems.append("no-png")
                    else:
                        old_png = old_path
                        old_size = png_size(old_path)
                        if old_size != (width, height):
                            old_problems.append(f"png-size={old_size[0]}x{old_size[1]}")

            if pair.port_scene not in new_ids:
                new_result = None
                new_problems = ["no-scene"]
            else:
                new_result = capture_cell(
                    runner, new_exe, "new", pair.port_scene, width, height, out,
                    language, env,
                )
                new_problems = list(new_result.problems)

            new_png = new_result.png if new_result is not None else None
            sheet_path = None
            if new_png is not None:
                sheet_path = out / "sheets" / f"{pair.name}_{resolution}.png"
                compose_sheet(
                    old_png,
                    new_png,
                    sheet_path,
                    f"{pair.name} | {width}x{height} | old: {pair.fork_scene or '-'} | new: {pair.port_scene}",
                )

            problems = [f"old:{problem}" for problem in old_problems]
            problems.extend(f"new:{problem}" for problem in new_problems)
            if problems:
                all_ok = False
            rows.append(
                (
                    pair.name,
                    resolution,
                    old_scene or "-",
                    pair.port_scene,
                    _exit_text(old_exit if old_result is not None else None),
                    _exit_text(new_result.exit_code if new_result is not None else None),
                    _size_text(old_size),
                    _size_text(new_result.size if new_result is not None else None),
                    _size_text(old_canvas),
                    _size_text(new_result.canvas if new_result is not None else None),
                    _path_text(old_png, out),
                    _path_text(new_png, out),
                    _path_text(sheet_path, out),
                    ";".join(problems) if problems else "ok",
                )
            )
    _write_table(out / "reference.tsv", TABLE_HEADER, rows)
    return all_ok


def run_gallery(rows, out, new_exe, language, runner, env):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    new_exe = Path(new_exe)
    new_ids = list_scenes(new_exe, runner, env)
    table_rows = []
    all_ok = True
    for row in rows:
        width, height = row.resolution
        resolution = f"{width}x{height}"
        if row.port_scene not in new_ids:
            result = None
            problems = ["no-scene"]
        else:
            result = capture_cell(
                runner, new_exe, "new", row.port_scene, width, height,
                out / "gallery-raw", language, env,
            )
            problems = list(result.problems)
        if result is not None and not problems and result.png is not None:
            destination = out / "gallery" / row.file
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(result.png, destination)
        if problems:
            all_ok = False
        table_rows.append(
            (
                row.file,
                row.port_scene,
                resolution,
                _exit_text(result.exit_code if result is not None else None),
                _size_text(result.size if result is not None else None),
                _size_text(result.canvas if result is not None else None),
                ";".join(problems) if problems else "ok",
            )
        )
    _write_table(out / "gallery.tsv", GALLERY_HEADER, table_rows)
    return all_ok


def main(argv=None):
    parser = argparse.ArgumentParser(description="Capture reference screenshots for UI audit scenes.")
    parser.add_argument("--out", required=True)
    parser.add_argument("--new-dir", required=True)
    parser.add_argument("--old-dir")
    parser.add_argument("--old-png-dir")
    parser.add_argument("--no-old", action="store_true")
    parser.add_argument("--language", choices=("ru", "en"), default="ru")
    parser.add_argument(
        "--pairs", default=str(Path(__file__).resolve().with_name("reference_pairs.tsv"))
    )
    parser.add_argument(
        "--gallery-file", default=str(Path(__file__).resolve().with_name("reference_gallery.tsv"))
    )
    parser.add_argument("--gallery", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--only", action="append")
    args = parser.parse_args(argv)

    if not args.gallery:
        old_modes = sum((args.old_dir is not None, args.old_png_dir is not None, args.no_old))
        if old_modes != 1:
            parser.error("choose exactly one of --old-dir, --old-png-dir, or --no-old")

    out = Path(args.out).resolve()
    new_dir = Path(args.new_dir).resolve()
    new_exe = new_dir / executable_name(os.name)
    if not new_exe.is_file():
        parser.error(f"executable not found: {new_exe}")

    env = game_environment(os.environ, args.headless, out / "xdg")
    if args.gallery:
        rows = parse_gallery(Path(args.gallery_file).resolve())
        ok = run_gallery(rows, out, new_exe, args.language, default_runner, env)
        return 0 if ok else 1

    old_exe = None
    old_png_dir = None
    if args.old_dir is not None:
        old_dir = Path(args.old_dir).resolve()
        old_exe = old_dir / executable_name(os.name)
        if not old_exe.is_file():
            parser.error(f"executable not found: {old_exe}")
    elif args.old_png_dir is not None:
        old_png_dir = Path(args.old_png_dir).resolve()

    pairs = parse_pairs(Path(args.pairs).resolve())
    if args.only:
        pair_names = {pair.name for pair in pairs}
        unknown = [name for name in args.only if name not in pair_names]
        if unknown:
            parser.error(f"unknown pair: {unknown[0]}")
        selected = set(args.only)
        pairs = [pair for pair in pairs if pair.name in selected]
    ok = run_reference(
        pairs, out, new_exe, old_exe, old_png_dir, args.language, default_runner, env
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
