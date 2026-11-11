import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

UNKNOWN_SCENE = "no-such-scene__nothing"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    with support.GameRun(args.run_dir) as game:
        result = game.run(["--ui-audit-scene", UNKNOWN_SCENE, "--ui-audit-out", str(game.out)])
        if result.returncode != 2:
            print(f"An unknown scene must exit with 2, got {result.returncode}\n{result.stderr}", file=sys.stderr)
            return 1
        if f"ui-audit: unknown scene {UNKNOWN_SCENE}" not in result.stderr:
            print(f"The unknown scene is not named on stderr:\n{result.stderr}", file=sys.stderr)
            return 1
        leftovers = sorted(path.name for path in game.out.rglob("*") if path.is_file())
        if leftovers:
            print(f"An unknown scene must not create files: {leftovers}", file=sys.stderr)
            return 1
        preferences = game.preferences_files()
        if preferences:
            print(f"An audit run must not write preferences: {preferences}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
