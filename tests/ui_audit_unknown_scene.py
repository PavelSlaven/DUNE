import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

UNKNOWN_SCENE = "no-such-scene__nothing"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", required=True)
    parser.add_argument("--resources", required=True)
    args = parser.parse_args()

    with support.GameRun(args.exe, args.resources) as game:
        listing = game.run(["--ui-audit-list"])
        if listing.returncode != 0:
            print(f"--ui-audit-list exited with {listing.returncode}\n{listing.stderr}",
                  file=sys.stderr)
            return 1
        try:
            catalog = support.read_catalog(listing.stdout)
        except (ValueError, KeyError, TypeError) as error:
            print(f"--ui-audit-list did not print a catalog: {error}", file=sys.stderr)
            return 1
        if UNKNOWN_SCENE in catalog or "main-menu" not in catalog:
            print("Catalog does not match the test premise", file=sys.stderr)
            return 1

        result = game.run(["--ui-audit-scene", UNKNOWN_SCENE, "--ui-audit-out", str(game.out)])
        if result.returncode == 0:
            print("Unknown scene must give a non-zero exit code", file=sys.stderr)
            return 1
        if UNKNOWN_SCENE not in result.stderr + result.stdout:
            print("Unknown scene name is not reported", file=sys.stderr)
            return 1
        leftovers = sorted(path.name for path in game.out.rglob("*") if path.is_file())
        if leftovers:
            print(f"Unknown scene must not create files: {leftovers}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
