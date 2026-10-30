"""Rebuild unit sprites from the accepted G3 redraw pipeline."""

import argparse
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.units3d.redraw_common import REPO_PACK, InputError, load_unit


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest='command', required=True)
    modules = {'inputs': 'inputs', 'recolour-inputs': 'recolour', 'score': 'score',
               'shadow-rule': 'shadow', 'build': 'build', 'pack': 'pack',
               'contact': 'sheets', 'sheet': 'sheets'}
    for name, module in modules.items():
        command = commands.add_parser(name)
        command.add_argument('unit', type=Path)
        command.set_defaults(module=module)
        if name == 'pack':
            command.add_argument('atlases', type=Path)
            command.add_argument('output', type=Path)
            command.add_argument('--source', type=Path, default=REPO_PACK)
        else:
            command.add_argument('--pack', type=Path)
            if name in ('inputs', 'recolour-inputs', 'build'):
                command.add_argument('output', type=Path)
            elif name == 'score':
                command.add_argument('--out', type=Path)
            elif name == 'contact':
                command.add_argument('inputs', type=Path)
                command.add_argument('output', type=Path)
            elif name == 'sheet':
                command.add_argument('atlases', type=Path)
                command.add_argument('output', type=Path)
                command.add_argument('--row', type=int, default=0)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == 'build' and args.output.exists():
            if not args.output.is_dir() or any(args.output.iterdir()):
                raise InputError(f'{args.output}: output must be absent or empty')
        unit = load_unit(args.unit, args.command, args.source if args.command == 'pack' else args.pack)
        module = importlib.import_module(f'tools.units3d.redraw_{args.module}')
        return module.run(unit, args)
    except (InputError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
