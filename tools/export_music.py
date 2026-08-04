#!/usr/bin/env python3
"""Extract D2TM music from an sdl_audio.dat DataPack with usage notes."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "resources" / "tools" / "datapack"))
from readerpack import ReaderPack  # noqa: E402


USAGE = {
    "MIDI_ATTACK": "Боевая тема: выбирается при обнаружении опасного противника; после окончания возвращается к мирной теме.",
    "MIDI_BUILDING": "Мирная игровая тема: случайно выбирается во время обычной игры и повторяется после окончания.",
    "MIDI_LOSE": "Поражение миссии: один из трёх вариантов.",
    "MIDI_MENTAT_ATR": "Брифинг/ментат Дома Атрейдесов.",
    "MIDI_MENTAT_HAR": "Брифинг/ментат Дома Харконненов.",
    "MIDI_MENTAT_ORD": "Брифинг/ментат Дома Ордосов.",
    "MIDI_MENU": "Главное меню и экран настройки схватки.",
    "MIDI_SCENARIO": "Карта кампании: выбор следующего владения.",
    "MIDI_WIN": "Победа в миссии: один из трёх вариантов.",
}


def usage_for(name: str) -> str:
    for prefix, usage in USAGE.items():
        if name.startswith(prefix):
            return usage
    return "Музыкальный ресурс; точка запуска не определена."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path, help="Path to sdl_audio.dat")
    parser.add_argument("output", type=Path, help="Folder for extracted .mid files")
    args = parser.parse_args()

    pack = ReaderPack(str(args.pack))
    if not args.pack.is_file() or not pack.fileInPack:
        raise SystemExit(f"Unable to read audio pack: {args.pack}")

    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)

    music = [(index, entry) for index, entry in enumerate(pack.fileInPack) if entry.extension.upper() in {"MID", "MIDI"}]
    rows = []
    for index, entry in music:
        filename = f"{index:02d}_{entry.fileId}.mid"
        (args.output / filename).write_bytes(pack.get_data(index))
        rows.append((index, filename, entry.fileId, entry.size, usage_for(entry.fileId)))

    lines = [
        "# Музыка D2TM",
        "",
        "Извлечено напрямую из `sdl_audio.dat`; MIDI-данные не перекодированы и не изменены.",
        "В игре каждая тема проигрывается один раз; для мирной темы следующий случайный трек запускается после завершения предыдущего.",
        "",
        "| ID | Файл | Ресурс | Когда играет |",
        "|---:|---|---|---|",
    ]
    for index, filename, resource, _size, usage in rows:
        lines.append(f"| {index} | `{filename}` | `{resource}` | {usage} |")
    lines.extend(["", f"Всего треков: {len(rows)}.", ""])
    (args.output / "README_RU.md").write_text("\n".join(lines), encoding="utf-8")

    manifest = ["id,file,resource,size_bytes,usage"]
    for index, filename, resource, size, usage in rows:
        manifest.append(f'{index},"{filename}","{resource}",{size},"{usage}"')
    (args.output / "music_manifest.csv").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    print(f"Extracted {len(rows)} tracks to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
