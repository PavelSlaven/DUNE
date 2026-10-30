from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from tools.hd_assets import decode_image, read_pack
from tools.units3d.redraw_common import InputError, ROOT


def _error(message):
    print(f'Ошибка установки пакета: {message}', file=sys.stderr)
    return 1


def run(unit, args) -> int:
    source = Path(unit.pack_path).resolve()
    output = Path(args.output).resolve()
    atlases = Path(args.atlases).resolve()
    if source == output or (output.exists() and os.path.samefile(source, output)):
        raise InputError('исходный пак и выходной файл совпадают')

    expected_names = [name for name in unit.atlases.values() if name]
    expected = set(expected_names)
    source_names = {entry.name for entry in unit.entries}
    missing = expected - source_names
    if missing:
        return _error(f'в исходном паке отсутствуют записи {sorted(missing)}')

    manifest_path = atlases / 'atlases.json'
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as error:
        raise InputError(f'{manifest_path}: {error}') from error
    if not isinstance(manifest, dict) or not isinstance(manifest.get('entries'), dict):
        raise InputError(f'{manifest_path}: entries должны быть объектом')
    entries = manifest['entries']
    sizes = {}
    for name, info in entries.items():
        if not isinstance(info, dict):
            raise InputError(f'{name}: запись манифеста должна быть объектом')
        if not isinstance(info.get('file'), str):
            raise InputError(f'{name}: file должен быть строкой')
        if not isinstance(info.get('sha256'), str):
            raise InputError(f'{name}: sha256 должен быть строкой')
        size = info.get('size')
        if (
            not isinstance(size, list)
            or len(size) != 2
            or any(type(value) is not int for value in size)
        ):
            raise InputError(f'{name}: size должен содержать две целые величины')
        sizes[name] = size

    if set(entries) != expected:
        return _error('набор записей манифеста не совпадает с атласами юнита')

    payloads = {}
    for name in expected_names:
        info = entries[name]
        payload = (atlases / info['file']).read_bytes()
        if hashlib.sha256(payload).hexdigest() != info['sha256']:
            return _error(f'{name}: SHA-256 файла не совпадает с манифестом')
        image = decode_image(payload)
        if image is None:
            return _error(f'{name}: файл не декодируется как изображение')
        source_image = unit.image(name)
        source_size = (source_image.shape[1], source_image.shape[0])
        if list(image.size) != sizes[name] or image.size != source_size:
            return _error(
                f'{name}: размер файла, манифеста и исходного атласа не совпадает'
            )
        payloads[name] = payload

    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output)
    try:
        result = subprocess.run(
            [
                sys.executable,
                'tools/units3d/install.py',
                '--atlases',
                str(atlases),
                '--pack',
                str(output),
            ],
            cwd=ROOT,
            timeout=1800,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return _error(str(error))
    if result.returncode != 0:
        return _error(f'установщик завершился с кодом {result.returncode}')

    before = unit.entries
    after = read_pack(output)
    before_signature = [
        (entry.index, entry.name, entry.extension) for entry in before
    ]
    after_signature = [
        (entry.index, entry.name, entry.extension) for entry in after
    ]
    if before_signature != after_signature:
        return _error('после установки изменился список записей пака')

    changed = [
        (old, new)
        for old, new in zip(before, after, strict=True)
        if old.payload != new.payload
    ]
    if any(new.name not in expected for _, new in changed):
        return _error('установщик изменил запись вне заданных атласов')
    for name, payload in payloads.items():
        if any(entry.payload != payload for entry in after if entry.name == name):
            return _error(f'{name}: payload в паке не совпадает с файлом атласа')

    changed_names = sorted({new.name for _, new in changed})
    unchanged_count = len(before) - len(changed)
    print(
        f'{len(before)} записей, {unchanged_count} без изменений, '
        f'заменены: {changed_names}'
    )
    return 0
