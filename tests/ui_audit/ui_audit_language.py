import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE = "options-menu-main"
HEADER = {
    "k": "header",
    "scene": SCENE,
    "resolution": "1024x768",
    "language": "en",
    "graphics": "hd",
    "canvas": {"w": 800, "h": 600},
    "game_screen": False,
    "render_scale": 0,
    "world_scale": 0,
}


def reject_constant(name):
    raise ValueError(f"{name} is not a JSON number")


def read_scene(game, language=None):
    arguments = ["--ui-audit-scene", SCENE, "--ui-audit-out", str(game.out)]
    if language is not None:
        arguments.extend(["--ui-audit-language", language])
    try:
        result = game.run(arguments)
    except subprocess.TimeoutExpired:
        return None, None, f"{SCENE} did not exit within {support.TIMEOUT_SECONDS} seconds"
    if result.returncode != 0:
        return result, None, f"{SCENE} exited with {result.returncode}\n{result.stdout}\n{result.stderr}"

    geometry = game.out / f"{SCENE}.geometry.jsonl"
    if not geometry.is_file():
        return result, None, f"{SCENE} geometry log is missing"
    try:
        lines = geometry.read_text(encoding="utf-8").splitlines()
        records = [json.loads(line, parse_constant=reject_constant) for line in lines]
    except (OSError, ValueError) as error:
        return result, None, f"{SCENE} geometry log could not be read: {error}"
    if not records or not all(isinstance(record, dict) for record in records):
        return result, None, f"{SCENE} geometry log must contain JSON objects"

    header = records[0]
    expected = dict(HEADER)
    if not support.same_json({key: header.get(key) for key in expected}, expected) or \
            not isinstance(header.get("version"), str):
        return result, None, f"{SCENE} has an unexpected geometry header: {header}"
    return result, records[1:], None


def check_text(records, required, forbidden=()):
    texts = [record.get("s") for record in records if record.get("k") == "text"]
    missing = sorted(set(required) - set(texts))
    if missing:
        return f"{SCENE} is missing text records {missing}"
    present = sorted(set(forbidden) & set(texts))
    if present:
        return f"{SCENE} has unexpected text records {present}"
    return None


def check_font_log(game, result, require_fallback):
    process_output = result.stdout + result.stderr
    log_path = game.run_dir / "nlog.txt"
    try:
        game_log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.is_file() else ""
    except OSError as log_error:
        return f"The game log could not be read: {log_error}"
    output = process_output + game_log
    if "Sangyo" in output:
        return "The game output or log unexpectedly mentions Sangyo"
    if require_fallback and "Hooked fallback font: PTMono-Regular.ttf" not in output:
        return "The Russian run did not report Hooked fallback font: PTMono-Regular.ttf"
    return None


def check_default_language(game):
    result, records, error = read_scene(game)
    if error:
        return error
    error = check_text(records, ("Language", "English"), ("Язык",))
    if error:
        return error
    return check_font_log(game, result, False)


def check_russian_language(game):
    result, records, error = read_scene(game, "ru")
    if error:
        return error
    error = check_text(records, ("Язык", "Русский"))
    if error:
        return error

    png = game.out / f"{SCENE}.png"
    if not png.is_file() or png.stat().st_size == 0:
        return f"{SCENE} PNG is missing or empty"
    try:
        size = support.png_size(png)
    except ValueError as png_error:
        return str(png_error)
    if size != (1024, 768):
        return f"{SCENE} PNG has unexpected dimensions {size[0]}x{size[1]}"

    return check_font_log(game, result, True)


def check_bad_language(game):
    result, _, error = read_scene(game, "de")
    if result is None:
        return error
    if result.returncode != 2:
        return f"An unsupported language must exit with 2, got {result.returncode}\n{result.stderr}"
    if "ui-audit: bad language de" not in result.stderr:
        return f"The unsupported language was not named on stderr:\n{result.stderr}"
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    with support.GameRun(args.run_dir) as game:
        for check in (check_default_language, check_russian_language, check_bad_language):
            error = check(game)
            if error:
                print(error, file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
