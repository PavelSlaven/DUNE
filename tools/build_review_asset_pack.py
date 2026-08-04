#!/usr/bin/env python3
"""Build a review/editing pack for every D2TM building and unit atlas."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
SOURCE = ROOT / "resources" / "hd" / "source_references" / "battle_for_arrakis_complete"
ARTIFACTS = ROOT / "artifacts"
PACK_NAME = "D2TM_BattleForArrakis_AssetPack_v1"
PACK = ARTIFACTS / PACK_NAME
USER_BUILDING_SHEET = Path(
    r"C:\Users\Slaven\Downloads\15ae2e81-d40d-4a8e-b228-a989ee8dcd0f.png"
)
DIRECTIONS = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]


@dataclass(frozen=True)
class AssetSpec:
    resource_id: int
    symbol: str
    name_ru: str
    frame_size: tuple[int, int]
    columns: int
    rows: int
    source_file: str
    notes_ru: str = ""
    row_labels: tuple[str, ...] = ()

    @property
    def atlas_size(self) -> tuple[int, int]:
        return self.frame_size[0] * self.columns, self.frame_size[1] * self.rows

    @property
    def hd4_size(self) -> tuple[int, int]:
        width, height = self.atlas_size
        return width * 4, height * 4


BUILDINGS = [
    AssetSpec(1, "BUILD_BARRACKS", "Казармы", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(3, "BUILD_CONSTYARD", "Строительный двор", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(
        5,
        "BUILD_HEAVYFACTORY",
        "Тяжёлый завод",
        (96, 64),
        1,
        11,
        "239094_buildings.png",
        "11 вертикальных кадров производственной анимации.",
    ),
    AssetSpec(
        8,
        "BUILD_HIGHTECH",
        "Высокотехнологичный завод",
        (96, 64),
        1,
        7,
        "239094_buildings.png",
        "7 вертикальных кадров анимации.",
    ),
    AssetSpec(10, "BUILD_IX", "Центр Икс", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(12, "BUILD_LIGHTFACTORY", "Лёгкий завод", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(15, "BUILD_PALACE", "Дворец", (96, 96), 1, 1, "239094_buildings.png"),
    AssetSpec(
        26,
        "BUILD_RADAR",
        "Радар",
        (64, 64),
        1,
        8,
        "239094_buildings.png",
        "8 вертикальных кадров анимации.",
    ),
    AssetSpec(
        28,
        "BUILD_REFINERY",
        "Перерабатывающий завод",
        (96, 64),
        1,
        8,
        "239094_buildings.png",
        "8 вертикальных кадров. Площадка харвестера должна оставаться читаемой во всех кадрах.",
    ),
    AssetSpec(
        30,
        "BUILD_REPAIR",
        "Ремонтный завод",
        (96, 64),
        1,
        8,
        "239094_buildings.png",
        "8 вертикальных кадров.",
    ),
    AssetSpec(
        32,
        "BUILD_RTURRET",
        "Ракетная башня",
        (32, 32),
        1,
        8,
        "239094_buildings.png",
        "Направления хранятся вертикально: E, NE, N, NW, W, SW, S, SE.",
        tuple(DIRECTIONS),
    ),
    AssetSpec(34, "BUILD_SILO", "Хранилище пряности", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(
        36,
        "BUILD_STARPORT",
        "Космопорт",
        (96, 96),
        1,
        8,
        "239094_buildings.png",
        "8 вертикальных кадров. Использовать сохранённую справа на исходном листе цепочку анимации.",
    ),
    AssetSpec(
        38,
        "BUILD_TURRET",
        "Орудийная башня",
        (32, 32),
        1,
        8,
        "239094_buildings.png",
        "Направления хранятся вертикально: E, NE, N, NW, W, SW, S, SE.",
        tuple(DIRECTIONS),
    ),
    AssetSpec(40, "BUILD_WINDTRAP", "Ветряная ловушка", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(42, "BUILD_WOR", "Казармы ВОР", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(109, "PLACE_SLAB1", "Бетонная плита", (32, 32), 1, 1, "239094_buildings.png"),
    AssetSpec(110, "PLACE_SLAB4", "Бетонные плиты 2×2", (64, 64), 1, 1, "239094_buildings.png"),
    AssetSpec(
        111,
        "PLACE_WALL",
        "Бетонная стена",
        (32, 32),
        1,
        1,
        "239094_buildings.png",
        "Сохранить стыкуемость с соседними сегментами и исходную занимаемую клетку.",
    ),
]


UNITS = [
    AssetSpec(130, "UNIT_CARRYALL", "Транспортник", (48, 48), 8, 2, "141660_carryall.png", row_labels=("ANIM_0", "ANIM_1")),
    AssetSpec(132, "UNIT_DEVASTATOR", "Девастатор", (38, 48), 8, 1, "550032_devastator.png"),
    AssetSpec(134, "UNIT_DEVIATOR", "Девиатор", (32, 32), 8, 1, "550380_missile_tank_deviator.png"),
    AssetSpec(135, "UNIT_FRIGATE", "Фрегат космопорта", (64, 64), 8, 1, "550136_starport_ship.png"),
    AssetSpec(
        137,
        "UNIT_HARVESTER",
        "Харвестер",
        (80, 52),
        8,
        4,
        "141659_harvester.png",
        "Строки должны сохранять один корпус и отличаться только рабочей анимацией.",
        ("MOVE_0", "MOVE_1", "MOVE_2", "MOVE_3"),
    ),
    AssetSpec(139, "UNIT_LAUNCHER", "Ракетная установка", (32, 32), 8, 1, "550380_missile_tank_deviator.png"),
    AssetSpec(141, "UNIT_MCV", "Мобильный стройкомплекс", (48, 50), 8, 1, "550068_mcv.png"),
    AssetSpec(
        143,
        "UNIT_ORNITHOPTER",
        "Орнитоптер",
        (48, 48),
        8,
        4,
        "550028_ornithopter.png",
        row_labels=("WING_0", "WING_1", "WING_2", "WING_3"),
    ),
    AssetSpec(145, "UNIT_QUAD", "Квад", (32, 32), 8, 1, "169130_quad.png"),
    AssetSpec(147, "UNIT_RAIDER", "Рейдерский трайк", (28, 26), 8, 1, "169129_trike_raider.png"),
    AssetSpec(149, "UNIT_SABOTEUR", "Диверсант", (32, 32), 8, 4, "169099_soldier_infantry.png", row_labels=("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")),
    AssetSpec(
        150,
        "UNIT_SANDWORM",
        "Песчаный червь",
        (48, 48),
        1,
        5,
        "550031_sandworm.png",
        "Пять вертикальных кадров.",
        ("FRAME_0", "FRAME_1", "FRAME_2", "FRAME_3", "FRAME_4"),
    ),
    AssetSpec(151, "UNIT_SIEGEBASE", "Осадный танк — корпус", (36, 38), 8, 1, "550030_siege_tank.png"),
    AssetSpec(153, "UNIT_SIEGETOP", "Осадный танк — башня", (36, 38), 8, 1, "550030_siege_tank.png"),
    AssetSpec(154, "UNIT_SINGLEFREMEN", "Фримен", (32, 32), 8, 4, "169099_soldier_infantry.png", row_labels=("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")),
    AssetSpec(155, "UNIT_SOLDIER", "Солдат", (32, 32), 8, 4, "169099_soldier_infantry.png", row_labels=("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")),
    AssetSpec(156, "UNIT_SOLDIERS", "Отряд солдат", (32, 32), 8, 4, "169099_soldier_infantry.png", row_labels=("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")),
    AssetSpec(
        157,
        "UNIT_SONICTANK",
        "Звуковой танк",
        (32, 32),
        8,
        1,
        "550030_siege_tank.png",
        "В Sega-каталоге нет отдельного листа звукового танка; силуэт требуется согласовать отдельно.",
    ),
    AssetSpec(159, "UNIT_TANKBASE", "Боевой танк — корпус", (32, 32), 8, 1, "550029_combat_tank.png"),
    AssetSpec(161, "UNIT_TANKTOP", "Боевой танк — башня", (32, 32), 8, 1, "550029_combat_tank.png"),
    AssetSpec(162, "UNIT_TRIKE", "Трайк", (28, 26), 8, 1, "169129_trike_raider.png"),
    AssetSpec(164, "UNIT_TRIPLEFREMEN", "Отряд фрименов", (32, 32), 8, 4, "169099_soldier_infantry.png", row_labels=("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")),
    AssetSpec(165, "UNIT_TROOPER", "Гранатомётчик", (32, 32), 8, 4, "169128_trooper_troopers.png", row_labels=("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")),
    AssetSpec(166, "UNIT_TROOPERS", "Отряд гранатомётчиков", (32, 32), 8, 4, "169128_trooper_troopers.png", row_labels=("MOVE_0", "MOVE_1", "MOVE_2", "ATTACK")),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classic_path(resource_id: int) -> Path:
    matches = list(CLASSIC.glob(f"{resource_id:04d}_*.png"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one classic resource for ID {resource_id}, got {matches}")
    return matches[0]


def font(size: int) -> ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def checkerboard(size: tuple[int, int], step: int = 32) -> Image.Image:
    image = Image.new("RGBA", size, (34, 38, 42, 255))
    draw = ImageDraw.Draw(image)
    for top in range(0, size[1], step):
        for left in range(0, size[0], step):
            if (left // step + top // step) % 2:
                draw.rectangle(
                    (left, top, min(size[0] - 1, left + step - 1), min(size[1] - 1, top + step - 1)),
                    fill=(50, 55, 60, 255),
                )
    return image


def make_guide(spec: AssetSpec, destination: Path) -> None:
    image = checkerboard(spec.hd4_size)
    draw = ImageDraw.Draw(image)
    frame_width = spec.frame_size[0] * 4
    frame_height = spec.frame_size[1] * 4
    label_font = font(
        10 if frame_width < 96 else max(12, min(34, spec.frame_size[1] * 2))
    )
    for row in range(spec.rows):
        for column in range(spec.columns):
            left = column * frame_width
            top = row * frame_height
            right = left + frame_width - 1
            bottom = top + frame_height - 1
            draw.rectangle((left, top, right, bottom), outline=(255, 64, 190, 255), width=3)
            if spec.columns == 8:
                column_label = DIRECTIONS[column]
            else:
                column_label = f"C{column:02d}"
            if spec.row_labels:
                row_label = spec.row_labels[row]
            elif spec.rows > 1:
                row_label = f"FRAME_{row:02d}"
            else:
                row_label = ""
            label = row_label if spec.columns == 1 and row_label else f"{column_label} {row_label}".strip()
            padding_x = 2 if frame_width < 96 else 8
            draw.text((left + padding_x, top + 4), label, font=label_font, fill=(255, 232, 120, 255))
            safe = max(2, min(4 * 4, (frame_width - 4) // 2, (frame_height - 4) // 2))
            draw.rectangle(
                (left + safe, top + safe, right - safe, bottom - safe),
                outline=(86, 210, 255, 170),
                width=2,
            )
    image.save(destination)


def make_classic_preview(source_path: Path, destination: Path) -> None:
    image = Image.open(source_path).convert("RGBA")
    image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST).save(destination)


def source_url(filename: str, source_manifest: dict) -> str:
    for entry in source_manifest["files"]:
        if entry["file"] == filename:
            return entry["page_url"]
    raise KeyError(filename)


def write_asset_folder(
    parent: Path,
    spec: AssetSpec,
    source_manifest: dict,
    building_sheet: Path,
) -> dict:
    folder = parent / f"{spec.resource_id:04d}_{spec.symbol}"
    folder.mkdir(parents=True)
    source_file = building_sheet if spec.source_file == "239094_buildings.png" else SOURCE / spec.source_file
    shutil.copy2(source_file, folder / "01_SOURCE_ORIGINAL.png")
    classic_file = classic_path(spec.resource_id)
    shutil.copy2(classic_file, folder / "02_CURRENT_D2TM_CLASSIC.png")
    make_classic_preview(classic_file, folder / "03_CURRENT_D2TM_CLASSIC_4X.png")
    Image.new("RGBA", spec.hd4_size, (0, 0, 0, 0)).save(folder / "EDIT_ME_HD4.png")
    Image.new("RGBA", spec.hd4_size, (0, 0, 0, 0)).save(folder / "HOUSE_MASK_HD4.png")
    make_guide(spec, folder / "GUIDE_HD4.png")

    actual_size = Image.open(classic_file).size
    if actual_size != spec.atlas_size:
        raise AssertionError(
            f"{spec.symbol}: contract {spec.atlas_size} != classic {actual_size}"
        )

    contract = {
        **asdict(spec),
        "atlas_size": list(spec.atlas_size),
        "hd4_size": list(spec.hd4_size),
        "density": 4,
        "direction_order": DIRECTIONS if spec.columns == 8 else None,
        "anchor": "bottom-center; do not change atlas or frame dimensions",
        "source_url": source_url(spec.source_file, source_manifest),
        "return_files": ["EDIT_ME_HD4.png", "HOUSE_MASK_HD4.png"],
        "rules_ru": [
            "Сохранить прозрачный RGBA-фон.",
            "Не изменять размер холста, число кадров и их порядок.",
            "Не добавлять текст, подписи или водяные знаки внутрь спрайта.",
            "Цветовую маску делать небольшой и распределять по осмысленным деталям корпуса.",
        ],
    }
    (folder / "CONTRACT.json").write_text(
        json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "resource_id": spec.resource_id,
        "symbol": spec.symbol,
        "name_ru": spec.name_ru,
        "folder": folder.name,
        "source": spec.source_file,
        "classic_sha256": sha256(classic_file),
        "edit_size": list(spec.hd4_size),
    }


def make_labelled_grid(building_sheet: Path, destination: Path) -> None:
    original = Image.open(building_sheet).convert("RGBA")
    scale = 4
    image = original.resize((original.width * scale, original.height * scale), Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(image)
    grid_font = font(23)
    cell = 32 * scale
    for row in range(original.height // 32):
        for column in range(original.width // 32):
            left = column * cell
            top = row * cell
            draw.rectangle((left, top, left + cell - 1, top + cell - 1), outline=(255, 0, 220, 255), width=2)
            label = f"R{row:02d} C{column:02d}"
            bounds = draw.textbbox((0, 0), label, font=grid_font)
            width = bounds[2] - bounds[0]
            draw.rectangle((left + 2, top + 2, left + width + 10, top + 31), fill=(0, 0, 0, 205))
            draw.text((left + 6, top + 3), label, font=grid_font, fill=(255, 242, 90, 255))
    image.save(destination)


def build_module_catalog(building_sheet: Path) -> dict:
    target = PACK / "03_BUILDING_MODULES"
    tiles = target / "tiles_32x32"
    target.mkdir(parents=True)
    tiles.mkdir()
    shutil.copy2(building_sheet, target / "BUILDINGS_ORIGINAL.png")
    make_labelled_grid(building_sheet, target / "BUILDINGS_GRID_LABELLED_4X.png")

    original = Image.open(building_sheet).convert("RGBA")
    modules = []
    for row in range(original.height // 32):
        for column in range(original.width // 32):
            filename = f"R{row:02d}_C{column:02d}.png"
            crop = original.crop((column * 32, row * 32, column * 32 + 32, row * 32 + 32))
            crop.save(tiles / filename)
            modules.append(
                {
                    "file": filename,
                    "row": row,
                    "column": column,
                    "source_rect": [column * 32, row * 32, 32, 32],
                }
            )

    # Preserve the animation-rich right band and the siren frames independently.
    animation = target / "animation_candidates"
    animation.mkdir()
    for frame in range(4):
        original.crop((416, frame * 64, 512, frame * 64 + 64)).save(
            animation / f"RIGHT_STACK_3x2_FRAME_{frame:02d}.png"
        )
    original.crop((416, 256, 512, 320)).save(animation / "SIREN_SOURCE_REGION.png")
    original.crop((0, 288, 416, 352)).save(animation / "TURRETS_AND_DETAILS_SOURCE_REGION.png")

    index = {
        "sheet_size": list(original.size),
        "cell_size": [32, 32],
        "columns": original.width // 32,
        "rows": original.height // 32,
        "module_count": len(modules),
        "modules": modules,
        "notes_ru": [
            "Правый вертикальный блок сохранён как четыре 96×64 кадра-кандидата анимации космопорта/базы харвестера.",
            "Сирена и нижняя полоса турелей сохранены отдельно без изменения пикселей.",
            "Окончательное соответствие модулей зданиям выбирается после визуального просмотра пользователем.",
        ],
    }
    (target / "MODULE_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return index


def build_siren_pack(building_sheet: Path) -> dict:
    target = PACK / "04_SUPPORT" / "SIREN_HOUSE_MARKER"
    target.mkdir(parents=True)
    original = Image.open(building_sheet).convert("RGBA")
    original.crop((416, 256, 512, 320)).save(target / "01_SIREN_SOURCE_REGION.png")

    specs = [
        ("LARGE", (16, 8), (16, 96)),
        ("SMALL", (11, 6), (11, 72)),
    ]
    entries = []
    for name, frame_size, atlas_size in specs:
        hd4_size = (atlas_size[0] * 4, atlas_size[1] * 4)
        Image.new("RGBA", hd4_size, (0, 0, 0, 0)).save(target / f"EDIT_ME_SIREN_{name}_HD4.png")
        guide_spec = AssetSpec(
            44 if name == "LARGE" else 45,
            f"SIREN_{name}",
            f"Сирена {name.lower()}",
            frame_size,
            1,
            12,
            "239094_buildings.png",
            "12 вертикальных кадров вращения; корпус нейтральный, светящаяся линза окрашивается в цвет Дома.",
            tuple(f"ROT_{index:02d}" for index in range(12)),
        )
        make_guide(guide_spec, target / f"GUIDE_SIREN_{name}_HD4.png")
        entries.append(
            {
                "replacement_resource_id": guide_spec.resource_id,
                "name": name,
                "logical_frame_size": list(frame_size),
                "frames": 12,
                "hd4_size": list(hd4_size),
            }
        )
    (target / "CONTRACT.json").write_text(
        json.dumps(
            {
                "purpose_ru": "Замена флагов зданий вращающейся сиреной цвета Дома.",
                "source_rect": [416, 256, 96, 64],
                "entries": entries,
                "rules_ru": [
                    "Ракурс сверху под тем же углом, что и у зданий.",
                    "Основание нейтральное; цвет Дома только на линзе/свечении.",
                    "Первый и двенадцатый кадры должны давать бесшовный цикл.",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {"folder": str(target.relative_to(PACK)), "entries": entries}


def write_readme() -> None:
    (PACK / "README_RU.txt").write_text(
        """D2TM — комплект ассетов для просмотра и ручной детализации

Цель
====
В комплекте есть отдельная папка для каждого игрового здания и каждого
графического ресурса юнитов. Игра и установленные HD-пакеты этим комплектом
не изменяются.

Что находится в папке объекта
==============================
01_SOURCE_ORIGINAL.png       — исходный лист Battle for Arrakis.
02_CURRENT_D2TM_CLASSIC.png  — текущий классический атлас D2TM.
03_CURRENT_D2TM_CLASSIC_4X.png — тот же атлас, увеличенный только для просмотра.
EDIT_ME_HD4.png              — прозрачный целевой холст точного размера.
HOUSE_MASK_HD4.png           — отдельная маска небольших цветовых деталей Дома.
GUIDE_HD4.png                — схема кадров; её возвращать не нужно.
CONTRACT.json                — точные размеры, порядок кадров и примечания.

Правила редактирования
======================
1. Рисуйте в EDIT_ME_HD4.png и не меняйте его размер.
2. Формат — PNG RGBA с прозрачным фоном.
3. Восемь направлений юнитов слева направо:
   E, NE, N, NW, W, SW, S, SE.
4. Корпус и башня танка находятся в отдельных папках и должны смотреть
   в одно и то же направление. Не объединяйте их.
5. Пехота должна быть заметно меньше техники: высота одного бойца внутри
   кадра 32×32 не должна визуально конкурировать с танком.
6. Здания привязаны к нижней границе кадра. Выступающие детали не должны
   выходить за холст.
7. HOUSE_MASK_HD4.png: прозрачный фон; белым/серым обозначаются только
   небольшие панели, полосы и линзы для окраски Дома. Не закрашивайте весь корпус.
8. Не добавляйте текст, псевдобуквы и водяные знаки.

Модульный лист зданий
=====================
В 03_BUILDING_MODULES лежит исходный лист целиком, увеличенная координатная
сетка и 176 неизменённых модулей 32×32. Правый блок с кадрами анимации
космопорта/базы харвестера, область сирены и нижняя полоса турелей также
сохранены отдельными файлами.

Сирена
======
В 04_SUPPORT/SIREN_HOUSE_MARKER находятся два 12-кадровых HD4-шаблона,
точно соответствующие существующим большим и малым флагам D2TM. Основание
сирены должно быть нейтральным, а линза — окрашиваться в цвет Дома.

Что вернуть
===========
Верните изменённые EDIT_ME_HD4.png и HOUSE_MASK_HD4.png с сохранением
структуры папок. Для сирены верните оба EDIT_ME_SIREN_*_HD4.png.
""",
        encoding="utf-8",
    )

    lines = ["КОНТРОЛЬНЫЙ СПИСОК ВОЗВРАТА", ""]
    lines.append("Здания:")
    lines.extend(f"[ ] {spec.resource_id:04d} {spec.name_ru} ({spec.symbol})" for spec in BUILDINGS)
    lines.extend(["", "Юниты:"])
    lines.extend(f"[ ] {spec.resource_id:04d} {spec.name_ru} ({spec.symbol})" for spec in UNITS)
    lines.extend(["", "Поддержка:", "[ ] Сирена LARGE — 12 кадров", "[ ] Сирена SMALL — 12 кадров", ""])
    (PACK / "RETURN_CHECKLIST_RU.txt").write_text("\n".join(lines), encoding="utf-8")


def write_sources(source_manifest: dict, building_sheet: Path, pixel_equal: bool) -> None:
    target = PACK / "00_ORIGINAL_SHEETS"
    target.mkdir(parents=True)
    for entry in source_manifest["files"]:
        path = building_sheet if entry["file"] == "239094_buildings.png" else SOURCE / entry["file"]
        shutil.copy2(path, target / entry["file"])
    lines = [
        "Dune II: The Battle for Arrakis — исходные страницы The Spriters Resource",
        "",
    ]
    lines.extend(f"{entry['file']}: {entry['page_url']}" for entry in source_manifest["files"])
    lines.extend(
        [
            "",
            "Пользовательский лист зданий:",
            str(USER_BUILDING_SHEET),
            f"Пиксельно совпадает с загруженным asset/239094: {'да' if pixel_equal else 'нет'}",
            "",
            "Использование: локальная некоммерческая модификация; исходные права принадлежат их владельцам.",
        ]
    )
    (target / "SOURCE_URLS_RU.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify(pack_manifest: dict) -> dict:
    errors: list[str] = []
    for category in ("buildings", "units"):
        for entry in pack_manifest[category]:
            folder = PACK / ("01_BUILDINGS" if category == "buildings" else "02_UNITS") / entry["folder"]
            for filename in (
                "01_SOURCE_ORIGINAL.png",
                "02_CURRENT_D2TM_CLASSIC.png",
                "03_CURRENT_D2TM_CLASSIC_4X.png",
                "EDIT_ME_HD4.png",
                "HOUSE_MASK_HD4.png",
                "GUIDE_HD4.png",
                "CONTRACT.json",
            ):
                if not (folder / filename).exists():
                    errors.append(f"missing {folder / filename}")
            for filename in ("EDIT_ME_HD4.png", "HOUSE_MASK_HD4.png", "GUIDE_HD4.png"):
                if Image.open(folder / filename).size != tuple(entry["edit_size"]):
                    errors.append(f"wrong size: {folder / filename}")

    tile_files = list((PACK / "03_BUILDING_MODULES" / "tiles_32x32").glob("*.png"))
    if len(tile_files) != 176:
        errors.append(f"expected 176 building modules, got {len(tile_files)}")
    for tile in tile_files:
        if Image.open(tile).size != (32, 32):
            errors.append(f"wrong tile size: {tile}")

    if errors:
        raise AssertionError("\n".join(errors))
    return {
        "status": "OK",
        "building_folders": len(pack_manifest["buildings"]),
        "unit_folders": len(pack_manifest["units"]),
        "building_modules": len(tile_files),
    }


def zip_pack() -> Path:
    archive = ARTIFACTS / f"{PACK_NAME}.zip"
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in sorted(PACK.rglob("*")):
            if path.is_file():
                handle.write(path, Path(PACK_NAME) / path.relative_to(PACK))
    return archive


def main() -> None:
    if not USER_BUILDING_SHEET.exists():
        raise FileNotFoundError(USER_BUILDING_SHEET)
    downloaded_sheet = SOURCE / "239094_buildings.png"
    user_image = Image.open(USER_BUILDING_SHEET).convert("RGBA")
    downloaded_image = Image.open(downloaded_sheet).convert("RGBA")
    pixel_equal = (
        user_image.size == downloaded_image.size
        and ImageChops.difference(user_image, downloaded_image).getbbox() is None
    )
    if not pixel_equal:
        raise AssertionError("User building sheet differs from downloaded asset/239094")

    if PACK.exists():
        raise FileExistsError(f"Refusing to overwrite existing pack: {PACK}")
    PACK.mkdir(parents=True)
    source_manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    write_sources(source_manifest, USER_BUILDING_SHEET, pixel_equal)

    buildings_root = PACK / "01_BUILDINGS"
    units_root = PACK / "02_UNITS"
    buildings_root.mkdir()
    units_root.mkdir()
    manifest = {
        "format": 1,
        "pack": PACK_NAME,
        "density": 4,
        "direction_order": DIRECTIONS,
        "user_building_sheet": str(USER_BUILDING_SHEET),
        "user_building_sheet_sha256": sha256(USER_BUILDING_SHEET),
        "downloaded_building_sheet_sha256": sha256(downloaded_sheet),
        "building_sheet_pixel_equal": pixel_equal,
        "buildings": [
            write_asset_folder(buildings_root, spec, source_manifest, USER_BUILDING_SHEET)
            for spec in BUILDINGS
        ],
        "units": [
            write_asset_folder(units_root, spec, source_manifest, USER_BUILDING_SHEET)
            for spec in UNITS
        ],
    }
    manifest["building_modules"] = build_module_catalog(USER_BUILDING_SHEET)
    manifest["siren"] = build_siren_pack(USER_BUILDING_SHEET)
    write_readme()
    manifest["verification"] = verify(manifest)
    (PACK / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    archive = zip_pack()
    print(json.dumps({"pack": str(PACK), "zip": str(archive), **manifest["verification"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
