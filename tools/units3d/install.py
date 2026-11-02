"""Replace a unit's entries in an HD4 pack by name, keeping every other entry byte for byte.

  python tools/units3d/install.py --atlases <dir> --pack resources/bin/data/sdl_data_hd4.dat
"""

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from atlas_geometry import validate_atlas_size  # noqa: E402
from hd_assets import decode_image, read_pack, write_pack  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--atlases', required=True, type=Path)
    parser.add_argument('--pack', required=True, type=Path)
    args = parser.parse_args()

    manifest = json.loads((args.atlases / 'atlases.json').read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or not isinstance(manifest.get('entries'), dict):
        raise SystemExit('atlases.json must contain an entries object')
    manifest_entries = manifest['entries']
    entries = read_pack(args.pack)
    source_names = {entry.name for entry in entries}
    missing = set(manifest_entries) - source_names
    if missing:
        raise SystemExit(f'pack has no entries named {sorted(missing)}')

    payloads = {}
    for name, info in manifest_entries.items():
        if not isinstance(info, dict) or not isinstance(info.get('file'), str):
            raise SystemExit(f'{name}: manifest file must be a string')
        size = info.get('size')
        if (
            not isinstance(size, list)
            or len(size) != 2
            or any(type(value) is not int or value <= 0 for value in size)
        ):
            raise SystemExit(f'{name}: manifest size must contain two positive integers')
        payload = (args.atlases / info['file']).read_bytes()
        image = decode_image(payload)
        if image is None:
            raise SystemExit(f'{name}: atlas is not a decodable image')
        if list(image.size) != size:
            raise SystemExit(f'{name}: image size does not match manifest')
        source_entry = next(entry for entry in entries if entry.name == name)
        source_image = decode_image(source_entry.payload)
        if source_image is None:
            raise SystemExit(f'{name}: source pack entry is not a decodable image')
        try:
            validate_atlas_size(name, image.size, source_image.size)
        except ValueError as error:
            raise SystemExit(str(error)) from error
        payloads[name] = payload

    write_pack(args.pack, [replace(e, payload=payloads[e.name]) if e.name in payloads else e for e in entries])
    print(f'replaced {len(payloads)} entries in {args.pack}')


if __name__ == '__main__':
    main()
