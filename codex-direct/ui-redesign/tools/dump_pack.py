#!/usr/bin/env python3
"""Read one D2TM pack: write a TSV inventory and export image entries as PNG.

Reads the pack and the parser of tools/hd_assets.py (read_pack, decode_image,
encode_png, safe_name). Writes only under --out-dir. Never touches the game data.
Run with python -B so the tool module does not leave __pycache__ in the repo.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def load_tool(path: Path):
    spec = importlib.util.spec_from_file_location("hd_assets", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True, type=Path)
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument(
        "--exclude-prefix",
        action="append",
        default=[],
        help="skip PNG export for names starting with this prefix (case-sensitive)",
    )
    parser.add_argument("--no-png", action="store_true")
    args = parser.parse_args()

    tool = load_tool(args.tool)
    entries = tool.read_pack(args.pack)
    stem = args.pack.stem
    png_dir = args.out_dir / stem
    rows = ["номер\tимя\tширина\tвысота\tтип записи"]
    image_count = 0
    saved = 0
    skipped_prefix = 0
    skipped_names: list[str] = []
    saved_bytes = 0

    for entry in entries:
        image = tool.decode_image(entry.payload)
        if image is None:
            kind = f"данные ext={entry.extension or '-'} size={len(entry.payload)}"
            rows.append(f"{entry.index}\t{entry.name}\t\t\t{kind}")
            continue
        image_count += 1
        rows.append(
            f"{entry.index}\t{entry.name}\t{image.width}\t{image.height}\t"
            f"картинка {image.mode}"
        )
        if args.no_png:
            continue
        if any(entry.name.startswith(p) for p in args.exclude_prefix):
            skipped_prefix += 1
            skipped_names.append(entry.name)
            continue
        png_dir.mkdir(parents=True, exist_ok=True)
        out = png_dir / f"{entry.index:04d}_{tool.safe_name(entry.name)}.png"
        data = tool.encode_png(image)
        out.write_bytes(data)
        saved += 1
        saved_bytes += len(data)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    tsv = args.out_dir / f"{stem}.tsv"
    tsv.write_text("\n".join(rows) + "\n", encoding="utf-8")

    print(f"pack={args.pack.name} entries={len(entries)} images={image_count}")
    print(f"tsv={tsv}")
    if not args.no_png:
        print(f"png_saved={saved} png_bytes={saved_bytes} png_dir={png_dir}")
        print(f"png_skipped_by_prefix={skipped_prefix}")
        if skipped_names:
            print("skipped_names=" + ",".join(skipped_names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
