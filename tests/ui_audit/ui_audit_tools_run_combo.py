import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support

TIMEOUT_SECONDS = 300


def check(run_dir, tools_dir, root):
    user_xdg = root / "user-xdg"
    user_xdg.mkdir()
    out = root / "out"
    environment = dict(os.environ)
    environment["XDG_DATA_HOME"] = str(user_xdg)
    combinations = (
        ("1024x768/en/hd", 0, {"w": 800, "h": 600}),
        ("1024x768/en/hd/r100w0", 100, {"w": 1024, "h": 768}),
    )
    for identifier, render_scale, canvas in combinations:
        result = subprocess.run(
            [sys.executable, "-B", str(tools_dir / "run_combo.py"), "--run-dir", str(run_dir),
             "--out", str(out), "--combo", identifier, "--scene", "main-menu", "--min-free-gb", "0"],
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        if result.returncode != 0:
            return f"run_combo.py завершился с кодом {result.returncode}: {identifier}\n{result.stderr}"
        log = out / "logs" / identifier / "main-menu.geometry.jsonl"
        if not log.is_file():
            return f"Не создан файл геометрии: {log}"
        lines = log.read_text(encoding="utf-8").splitlines()
        if not lines:
            return f"Файл геометрии пуст: {log}"
        header = json.loads(lines[0])
        expected = {"render_scale": render_scale, "canvas": canvas}
        if render_scale == 0:
            expected.update(resolution="1024x768", language="en", world_scale=0)
        if not isinstance(header, dict) or any(header.get(key) != value for key, value in expected.items()):
            return f"Неверный заголовок геометрии для {identifier}: {header}"
        if render_scale == 0:
            png = out / "png" / identifier / "main-menu.png"
            if not png.is_file():
                return f"Не создан PNG: {png}"
            size = support.png_size(png)
            if size != (1024, 768):
                return f"Неверный размер PNG: {size}"
        work = out / "work" / identifier.replace("/", "_")
        if work.exists():
            return f"Не удалена рабочая папка комбинации: {work}"
        print(f"Проверена комбинация {identifier}", flush=True)
    if list(user_xdg.iterdir()):
        return f"Пользовательская папка XDG должна остаться пустой: {user_xdg}"
    return None


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--tools-dir", default=str(Path(__file__).resolve().parents[2] / "tools" / "ui-audit"))
    args = parser.parse_args(argv)
    try:
        with tempfile.TemporaryDirectory(prefix="ui-audit-tools-") as directory:
            error = check(Path(args.run_dir).resolve(), Path(args.tools_dir).resolve(), Path(directory))
            if error:
                print(error, file=sys.stderr)
                return 1
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"Проверка run_combo.py завершилась с ошибкой: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
