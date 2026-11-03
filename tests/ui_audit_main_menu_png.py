import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE = "main-menu"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", required=True)
    parser.add_argument("--resources", required=True)
    args = parser.parse_args()

    with support.GameRun(args.exe, args.resources) as game:
        result = game.run(["--ui-audit-scene", SCENE, "--ui-audit-out", str(game.out)])
        if result.returncode != 0:
            print(f"Game exited with {result.returncode}\n{result.stdout}\n{result.stderr}",
                  file=sys.stderr)
            return 1

        png = game.out / f"{SCENE}.png"
        log = game.out / f"{SCENE}.geometry.jsonl"
        if not png.is_file() or not log.is_file():
            print(f"Missing output: png={png.is_file()} log={log.is_file()}", file=sys.stderr)
            return 1

        try:
            size = support.png_size(png)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1
        if size != (1024, 768):
            print(f"Unexpected PNG size: {size[0]}x{size[1]}", file=sys.stderr)
            return 1

        records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
        kinds = [record.get("k") for record in records]
        if not records or kinds[0] != "header":
            print("The log must start with a header record", file=sys.stderr)
            return 1
        header = records[0]
        if header.get("scene") != SCENE or header.get("resolution") != "1024x768":
            print(f"Unexpected header: {header}", file=sys.stderr)
            return 1
        if header.get("canvas") != {"w": 800, "h": 600}:
            print(f"Unexpected canvas: {header.get('canvas')}", file=sys.stderr)
            return 1
        if kinds.count("text") < 1:
            print("The log has no text record", file=sys.stderr)
            return 1
        if kinds.count("gui") < 1:
            print("The log has no GuiObject record", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
