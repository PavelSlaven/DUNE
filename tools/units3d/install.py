"""Replace a unit's entries in an HD4 pack by name, keeping every other entry byte for byte.

  python tools/units3d/install.py --atlases <dir> --pack resources/bin/data/sdl_data_hd4.dat
"""

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hd_assets import read_pack, write_pack  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--atlases', required=True, type=Path)
    parser.add_argument('--pack', required=True, type=Path)
    args = parser.parse_args()

    manifest = json.loads((args.atlases / 'atlases.json').read_text(encoding='utf-8'))
    payloads = {name: (args.atlases / info['file']).read_bytes() for name, info in manifest['entries'].items()}
    entries = read_pack(args.pack)
    missing = set(payloads) - {e.name for e in entries}
    if missing:
        raise SystemExit(f'pack has no entries named {sorted(missing)}')
    write_pack(args.pack, [replace(e, payload=payloads[e.name]) if e.name in payloads else e for e in entries])
    print(f'replaced {len(payloads)} entries in {args.pack}')


if __name__ == '__main__':
    main()
