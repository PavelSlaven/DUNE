#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import combos


def plan_actions(out_root, flags, ordered_ids):
    needed = defaultdict(set)
    for combo, scene in combos.png_required(flags, ordered_ids):
        needed[combo].add(scene)
    missing, extra = [], []
    for identifier in ordered_ids:
        png_dir = Path(out_root) / "png" / identifier
        have = {path.stem for path in png_dir.glob("*.png")} if png_dir.is_dir() else set()
        missing += [(identifier, scene) for scene in sorted(needed[identifier] - have)]
        if identifier.count("/") != 2:
            extra += [(identifier, scene) for scene in sorted(have - needed[identifier])]
    return missing, extra


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Leave PNG only for the first flag with a given key per resolution; capture the ones still missing.")
    parser.add_argument("--exe", required=True)
    parser.add_argument("--resources", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--flags", required=True, help="flags JSON from check_geometry.py")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    out = Path(args.out)
    order = json.loads((out / "order.json").read_text(encoding="utf-8"))
    flags = json.loads(Path(args.flags).read_text(encoding="utf-8"))
    missing, extra = plan_actions(out, flags, order)
    print(f"extra PNG: {len(extra)}; missing PNG: {len(missing)}")
    if args.dry_run:
        return 0
    for identifier, scene in extra:
        (out / "png" / identifier / f"{scene}.png").unlink()
    by_combo = defaultdict(list)
    for identifier, scene in missing:
        by_combo[identifier].append(scene)
    code = 0
    for identifier, scenes in by_combo.items():
        command = [sys.executable, str(Path(__file__).resolve().parent / "run_combo.py"), "--exe", args.exe,
                   "--resources", args.resources, "--out", str(out), "--combo", identifier]
        for scene in scenes:
            command += ["--scene", scene]
        code = max(code, subprocess.run(command, check=False).returncode)
    return code


if __name__ == "__main__":
    sys.exit(main())
