"""Copy the repository pack, put the three new Devastator atlases into the copy, and prove nothing else changed.
usage: python -X utf8 pack.py <atlas dir> <pack copy>   (run from the repo root)"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path('tools').resolve()))
from hd_assets import read_pack  # noqa: E402

ATLAS, COPY = Path(sys.argv[1]), Path(sys.argv[2])
SRC = Path('resources/bin/data/sdl_data_hd4.dat')
COPY.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, COPY)
subprocess.run([sys.executable, 'tools/units3d/install.py', '--atlases', str(ATLAS), '--pack', str(COPY)], check=True)
manifest = json.loads((ATLAS / 'atlases.json').read_text(encoding='utf-8'))['entries']
before, after = read_pack(SRC), read_pack(COPY)
assert [(e.index, e.name, e.extension) for e in before] == [(e.index, e.name, e.extension) for e in after], 'entry list changed'
changed = [b.name for b, a in zip(before, after) if b.payload != a.payload]
assert sorted(changed) == sorted(manifest), f'changed entries {changed}'
for a in after:
    if a.name in manifest:
        assert a.payload == (ATLAS / manifest[a.name]['file']).read_bytes(), a.name
print(f'{len(before)} entries, {len(before) - len(changed)} byte-identical, replaced: {sorted(changed)}')
