# Ассеты интерфейса hd4: опись

Сделано скриптами: `.cache/ui-redesign/scripts/dump_pack.py` (чтение пака и PNG) и `build_report.py` (этот файл).
Игровые файлы не менялись. `git status --short` до и после pull: `?? codex-direct/` (индекс не трогали).

## 1. Шаг 1: LFS

Команда: `git lfs ls-files -s | grep -E "_hd4\.dat|data/hd4/"`
```
b150c09b58 * resources/bin/data/hd4/campaign_map.png (4.5 MB)
48cf78fec2 * resources/bin/data/hd4/credits_team.png (293 KB)
4c96017a3f * resources/bin/data/hd4/credits_title.png (113 KB)
2e0bed616d * resources/bin/data/hd4/hud_house_atreides.png (237 KB)
33269ed1a0 * resources/bin/data/hd4/hud_house_harkonnen.png (258 KB)
973f2e4495 * resources/bin/data/hd4/hud_house_ordos.png (265 KB)
962d8f7760 * resources/bin/data/hd4/main_menu_background.png (5.1 MB)
23e7a4ce3c * resources/bin/data/hd4/main_menu_logo.png (254 KB)
7db3df50f9 * resources/bin/data/hd4/outcome_defeat_en.png (6.4 MB)
5a1e52d4d4 * resources/bin/data/hd4/outcome_defeat_ru.png (6.4 MB)
930bab6a5c * resources/bin/data/hd4/outcome_victory_en.png (7.4 MB)
269b0d7718 * resources/bin/data/hd4/outcome_victory_ru.png (7.5 MB)
e260cd4091 * resources/bin/data/sdl_data_hd4.dat (38 MB)
6c52d5ab2e * resources/bin/data/sdl_inter_hd4.dat (7.6 MB)
21872030cc * resources/bin/data/sdl_mentat_hd4.dat (33 MB)
94cf42fef1 * resources/bin/data/sdl_world_hd4.dat (12 MB)
```

Перед pull маркер в строках был ` - ` (файл только указателем), после pull ` * ` (содержимое скачано).
Сумма 16 файлов по диску: 129221243 байт (129.2 MB), порог 4 ГБ, поэтому стянуты все 16.
Команда: `git lfs pull --include="resources/bin/data/hd4/*.png,resources/bin/data/sdl_inter_hd4.dat,resources/bin/data/sdl_mentat_hd4.dat,resources/bin/data/sdl_data_hd4.dat,resources/bin/data/sdl_world_hd4.dat"` — exit 0.

## 2. Шаг 2: 12 файлов hd4 (`resources/bin/data/hd4/*.png`)

Скопированы в `.cache/ui-redesign/assets/hd4/`.

| файл | ширина × высота | режим | размер, байт |
|---|---|---|---|
| campaign_map.png | 2432 × 960 | RGB | 4541123 |
| credits_team.png | 948 × 624 | RGBA | 292900 |
| credits_title.png | 1280 × 800 | RGBA | 113285 |
| hud_house_atreides.png | 384 × 384 | RGBA | 237299 |
| hud_house_harkonnen.png | 384 × 384 | RGBA | 258354 |
| hud_house_ordos.png | 384 × 384 | RGBA | 265207 |
| main_menu_background.png | 5120 × 1440 | RGB | 5094199 |
| main_menu_logo.png | 1792 × 320 | RGBA | 254231 |
| outcome_defeat_en.png | 2752 × 1536 | RGBA | 6403321 |
| outcome_defeat_ru.png | 2752 × 1536 | RGBA | 6446955 |
| outcome_victory_en.png | 2752 × 1536 | RGBA | 7431127 |
| outcome_victory_ru.png | 2752 × 1536 | RGBA | 7459732 |

## 3. Формат пака и имена

`tools/hd_assets.py` (импортирует только stdlib и Pillow). Пак: заголовок `D2TM` + uint16 число записей; каталог из записей `<40s name, 4s ext, uint32 offset, uint32 size>`; данные сразу за каталогом. Имя записи лежит в каталоге пака, поэтому номер→имя берётся из пака.
Готовой команды извлечения для hd4 нет: `inventory` берёт только `sdl_data.dat, sdl_inter.dat, sdl_world.dat, sdl_mentat.dat` (`MAIN_PACKS`, функция `discover_packs`), имена hd4 туда не входят. Поэтому `dump_pack.py` использует из модуля `read_pack`, `decode_image`, `encode_png`, `safe_name` (запуск `python -B`, без `__pycache__` в репозитории).

Сверка `src/data/gfxinter.h` с номерами пака `sdl_inter_hd4`: совпало 146 из 146 констант `constexpr int NAME = N`.
Сверка `src/data/gfxdata.h` с номерами пака `sdl_data_hd4`: совпало 168 из 168 констант `constexpr int NAME = N`.
`src/data/gfxmentat.h` и `src/data/gfxworld.h` в репозитории отсутствуют (в `src/data/` только gfxaudio.h, gfxdata.h, gfxinter.h), сверка для ментатов и мира не выполнена.

## 4. Паки: счётчики

| пак | записей | картинок | не картинок | PNG сохранено | записей интерфейса по правилу |
|---|---|---|---|---|---|
| sdl_inter_hd4 | 146 | 146 | 0 | 146 | 146 |
| sdl_mentat_hd4 | 52 | 52 | 0 | 52 | 52 |
| sdl_data_hd4 | 242 | 242 | 0 | 36 | 36 |
| sdl_world_hd4 | 36 | 36 | 0 | 36 | 36 |

Правило для `sdl_data_hd4` и `sdl_world_hd4`: исключены имена, начинающиеся с `UNIT_`, `BUILD_`, `HM_`, `TERRAIN`, `EXPLOSION`, `BULLET`, `PARTICLE`, `OBJECT_`, `TRACK` (регистр важен). Исключено в `sdl_data_hd4`: 206, в `sdl_world_hd4`: 0.
Для `sdl_inter_hd4` и `sdl_mentat_hd4` сохранены все записи.

## 5. sdl_inter_hd4: записи интерфейса (146)

### значки построек (ICON_STR_*): 19

| номер | имя | ширина × высота |
|---|---|---|
| 32 | ICON_STR_1SLAB | 256 × 192 |
| 33 | ICON_STR_4SLAB | 256 × 192 |
| 34 | ICON_STR_BARRACKS | 256 × 192 |
| 35 | ICON_STR_CONSTYARD | 256 × 192 |
| 36 | ICON_STR_HEAVYFACTORY | 256 × 192 |
| 37 | ICON_STR_HIGHTECH | 256 × 192 |
| 38 | ICON_STR_IX | 256 × 192 |
| 39 | ICON_STR_LIGHTFACTORY | 256 × 192 |
| 40 | ICON_STR_PALACE | 256 × 192 |
| 41 | ICON_STR_RADAR | 256 × 192 |
| 42 | ICON_STR_REFINERY | 256 × 192 |
| 43 | ICON_STR_REPAIR | 256 × 192 |
| 44 | ICON_STR_RTURRET | 256 × 192 |
| 45 | ICON_STR_SILO | 256 × 192 |
| 46 | ICON_STR_STARPORT | 256 × 192 |
| 47 | ICON_STR_TURRET | 256 × 192 |
| 48 | ICON_STR_WALL | 256 × 192 |
| 49 | ICON_STR_WINDTRAP | 256 × 192 |
| 50 | ICON_STR_WOR | 256 × 192 |

### значки юнитов (ICON_UNIT_*): 21

| номер | имя | ширина × высота |
|---|---|---|
| 51 | ICON_UNIT_CARRYALL | 256 × 192 |
| 52 | ICON_UNIT_DEVASTATOR | 256 × 192 |
| 53 | ICON_UNIT_DEVIATOR | 256 × 192 |
| 54 | ICON_UNIT_FREMEN | 256 × 192 |
| 55 | ICON_UNIT_HARVESTER | 256 × 192 |
| 56 | ICON_UNIT_INFANTRY | 256 × 192 |
| 57 | ICON_UNIT_LAUNCHER | 256 × 192 |
| 58 | ICON_UNIT_MCV | 256 × 192 |
| 59 | ICON_UNIT_ORNITHOPTER | 256 × 192 |
| 60 | ICON_UNIT_QUAD | 256 × 192 |
| 61 | ICON_UNIT_RAIDER | 256 × 192 |
| 62 | ICON_UNIT_SABOTEUR | 256 × 192 |
| 63 | ICON_UNIT_SANDWORM | 256 × 192 |
| 64 | ICON_UNIT_SARDAUKAR | 256 × 192 |
| 65 | ICON_UNIT_SIEGETANK | 256 × 192 |
| 66 | ICON_UNIT_SOLDIER | 256 × 192 |
| 67 | ICON_UNIT_SONICTANK | 256 × 192 |
| 68 | ICON_UNIT_TANK | 256 × 192 |
| 69 | ICON_UNIT_TRIKE | 256 × 192 |
| 70 | ICON_UNIT_TROOPER | 256 × 192 |
| 71 | ICON_UNIT_TROOPERS | 256 × 192 |

### прочие значки (ICON_*, ICON_SPECIAL/POWER/SOLARIS): 9

| номер | имя | ширина × высота |
|---|---|---|
| 29 | ICON_SPECIAL_FREMEN | 256 × 192 |
| 30 | ICON_SPECIAL_MISSILE | 256 × 192 |
| 31 | ICON_SPECIAL_SABOTEUR | 256 × 192 |
| 139 | ICON_POWER | 64 × 64 |
| 140 | ICON_POWER_HIGH | 64 × 64 |
| 141 | ICON_SOLARIS_LOW | 64 × 64 |
| 142 | ICON_SOLARIS | 64 × 64 |
| 143 | ICON_SOLARIS_FULL | 64 × 64 |
| 145 | ICON_POWER_LOW | 64 × 64 |

### кнопки списка производства (LIST_BTN_*): 6

| номер | имя | ширина × высота |
|---|---|---|
| 72 | LIST_BTN_CONSTYARD | 132 × 108 |
| 73 | LIST_BTN_FACTORY | 132 × 108 |
| 74 | LIST_BTN_INFANTRY | 132 × 108 |
| 75 | LIST_BTN_PALACE | 132 × 108 |
| 76 | LIST_BTN_STARPORT | 132 × 108 |
| 77 | LIST_BTN_UPGRADE | 132 × 108 |

### кнопки (BTN_*): 2

| номер | имя | ширина × высота |
|---|---|---|
| 18 | BTN_OPTIONS | 640 × 128 |
| 19 | BTN_ORDER | 640 × 128 |

### сетки размещения построек (GRID_*): 5

| номер | имя | ширина × высота |
|---|---|---|
| 23 | GRID_0X0 | 76 × 76 |
| 24 | GRID_1X1 | 76 × 76 |
| 25 | GRID_2X2 | 76 × 76 |
| 26 | GRID_3X2 | 76 × 76 |
| 27 | GRID_3X3 | 76 × 76 |

### кадры прогресса (PROGRESS*): 34

| номер | имя | ширина × высота |
|---|---|---|
| 82 | PROGRESS001 | 240 × 144 |
| 83 | PROGRESS002 | 240 × 144 |
| 84 | PROGRESS003 | 240 × 144 |
| 85 | PROGRESS004 | 240 × 144 |
| 86 | PROGRESS005 | 240 × 144 |
| 87 | PROGRESS006 | 240 × 144 |
| 88 | PROGRESS007 | 240 × 144 |
| 89 | PROGRESS008 | 240 × 144 |
| 90 | PROGRESS009 | 240 × 144 |
| 91 | PROGRESS010 | 240 × 144 |
| 92 | PROGRESS011 | 240 × 144 |
| 93 | PROGRESS012 | 240 × 144 |
| 94 | PROGRESS013 | 240 × 144 |
| 95 | PROGRESS014 | 240 × 144 |
| 96 | PROGRESS015 | 240 × 144 |
| 97 | PROGRESS016 | 240 × 144 |
| 98 | PROGRESS017 | 240 × 144 |
| 99 | PROGRESS018 | 240 × 144 |
| 100 | PROGRESS019 | 240 × 144 |
| 101 | PROGRESS020 | 240 × 144 |
| 102 | PROGRESS021 | 240 × 144 |
| 103 | PROGRESS022 | 240 × 144 |
| 104 | PROGRESS023 | 240 × 144 |
| 105 | PROGRESS024 | 240 × 144 |
| 106 | PROGRESS025 | 240 × 144 |
| 107 | PROGRESS026 | 240 × 144 |
| 108 | PROGRESS027 | 240 × 144 |
| 109 | PROGRESS028 | 240 × 144 |
| 110 | PROGRESS029 | 240 × 144 |
| 111 | PROGRESS030 | 240 × 144 |
| 112 | PROGRESS031 | 240 × 144 |
| 113 | PROGRESS032 | 240 × 144 |
| 114 | PROGRESSFIX | 240 × 148 |
| 115 | PROGRESSNA | 256 × 192 |

### READY*: 2

| номер | имя | ширина × высота |
|---|---|---|
| 116 | READY01 | 232 × 40 |
| 117 | READY02 | 232 × 40 |

### STAT* (512×512): 21

| номер | имя | ширина × высота |
|---|---|---|
| 118 | STAT01 | 512 × 512 |
| 119 | STAT02 | 512 × 512 |
| 120 | STAT03 | 512 × 512 |
| 121 | STAT04 | 512 × 512 |
| 122 | STAT05 | 512 × 512 |
| 123 | STAT06 | 512 × 512 |
| 124 | STAT07 | 512 × 512 |
| 125 | STAT08 | 512 × 512 |
| 126 | STAT09 | 512 × 512 |
| 127 | STAT10 | 512 × 512 |
| 128 | STAT11 | 512 × 512 |
| 129 | STAT12 | 512 × 512 |
| 130 | STAT13 | 512 × 512 |
| 131 | STAT14 | 512 × 512 |
| 132 | STAT15 | 512 × 512 |
| 133 | STAT16 | 512 × 512 |
| 134 | STAT17 | 512 × 512 |
| 135 | STAT18 | 512 × 512 |
| 136 | STAT19 | 512 × 512 |
| 137 | STAT20 | 512 × 512 |
| 138 | STAT21 | 512 × 512 |

### рамки сообщений (MESSAGE_*): 3

| номер | имя | ширина × высота |
|---|---|---|
| 78 | MESSAGE_LEFT | 44 × 120 |
| 79 | MESSAGE_MIDDLE | 220 × 120 |
| 80 | MESSAGE_RIGHT | 44 × 120 |

### панели сайдбара и полосы (CANDYBAR, BMP_GERALD_*): 8

| номер | имя | ширина × высота |
|---|---|---|
| 3 | BMP_GERALD_CANDYBAR_BALL | 96 × 104 |
| 4 | BMP_GERALD_CANDYBAR_BOTTOM | 96 × 40 |
| 5 | BMP_GERALD_CANDYBAR_PIECE | 96 × 96 |
| 6 | BMP_GERALD_CANDYBAR_TOP | 96 × 48 |
| 7 | BMP_GERALD_ICONLIST_BACKGROUND | 256 × 336 |
| 8 | BMP_GERALD_SIDEBAR_PIECE | 800 × 12 |
| 9 | BMP_GERALD_TOP_BAR | 3196 × 28 |
| 28 | HORIZONTAL_CANDYBAR | 800 × 48 |

### выбор дома (BMP_SELECT_*): 5

| номер | имя | ширина × высота |
|---|---|---|
| 11 | BMP_SELECT_HOUSE_ATREIDES | 360 × 392 |
| 12 | BMP_SELECT_HOUSE_HARKONNEN | 360 × 392 |
| 13 | BMP_SELECT_HOUSE_ORDOS | 360 × 392 |
| 14 | BMP_SELECT_YOUR_HOUSE | 540 × 84 |
| 144 | BMP_SELECT_HOUSE_SARDAUKAR | 360 × 392 |

### растровые экраны и фоны (BMP_*): 7

| номер | имя | ширина × высота |
|---|---|---|
| 0 | BMP_D2TM | 2432 × 664 |
| 1 | BMP_GAME_DUNE | 2560 × 1600 |
| 2 | BMP_GENERATING | 1280 × 480 |
| 10 | BMP_LOSING | 1280 × 480 |
| 15 | BMP_TOPBAR_BACKGROUND | 472 × 120 |
| 16 | BMP_UNKNOWNMAP | 512 × 512 |
| 17 | BMP_WINNING | 1280 × 480 |

### CREDITS_*: 2

| номер | имя | ширина × высота |
|---|---|---|
| 20 | CREDITS_BAR | 512 × 128 |
| 21 | CREDITS_DUNE2_CORE_TEAM | 948 × 624 |

### палитры (PAL*): 1

| номер | имя | ширина × высота |
|---|---|---|
| 81 | PAL_INTER | 128 × 32 |

### прочее: 1

| номер | имя | ширина × высота |
|---|---|---|
| 22 | D2TM_TITLE | 1280 × 800 |

## 5. sdl_mentat_hd4: записи интерфейса (52)

### кнопки (BTN_*): 4

| номер | имя | ширина × высота |
|---|---|---|
| 20 | BTN_NO | 616 × 184 |
| 21 | BTN_PROCEED | 616 × 184 |
| 22 | BTN_REPEAT | 616 × 184 |
| 23 | BTN_YES | 616 × 184 |

### части ментатов по домам (ATR/BEN/HAR/ORD_*: глаза, рот): 40

| номер | имя | ширина × высота |
|---|---|---|
| 0 | ATR_EYES01 | 384 × 128 |
| 1 | ATR_EYES02 | 384 × 128 |
| 2 | ATR_EYES03 | 384 × 128 |
| 3 | ATR_EYES04 | 384 × 128 |
| 4 | ATR_EYES05 | 384 × 128 |
| 5 | ATR_MOUTH01 | 448 × 320 |
| 6 | ATR_MOUTH02 | 448 × 320 |
| 7 | ATR_MOUTH03 | 448 × 320 |
| 8 | ATR_MOUTH04 | 448 × 320 |
| 9 | ATR_MOUTH05 | 448 × 320 |
| 10 | BEN_EYES01 | 384 × 128 |
| 11 | BEN_EYES02 | 384 × 128 |
| 12 | BEN_EYES03 | 384 × 128 |
| 13 | BEN_EYES04 | 384 × 128 |
| 14 | BEN_EYES05 | 384 × 128 |
| 15 | BEN_MOUTH01 | 448 × 320 |
| 16 | BEN_MOUTH02 | 448 × 320 |
| 17 | BEN_MOUTH03 | 448 × 320 |
| 18 | BEN_MOUTH04 | 448 × 320 |
| 19 | BEN_MOUTH05 | 448 × 320 |
| 24 | HAR_EYES01 | 384 × 128 |
| 25 | HAR_EYES02 | 384 × 128 |
| 26 | HAR_EYES03 | 384 × 128 |
| 27 | HAR_EYES04 | 384 × 128 |
| 28 | HAR_EYES05 | 384 × 128 |
| 29 | HAR_MOUTH01 | 448 × 320 |
| 30 | HAR_MOUTH02 | 448 × 320 |
| 31 | HAR_MOUTH03 | 448 × 320 |
| 32 | HAR_MOUTH04 | 448 × 320 |
| 33 | HAR_MOUTH05 | 448 × 320 |
| 41 | ORD_EYES01 | 384 × 128 |
| 42 | ORD_EYES02 | 384 × 128 |
| 43 | ORD_EYES03 | 384 × 128 |
| 44 | ORD_EYES04 | 384 × 128 |
| 45 | ORD_EYES05 | 384 × 128 |
| 46 | ORD_MOUTH01 | 448 × 320 |
| 47 | ORD_MOUTH02 | 448 × 320 |
| 48 | ORD_MOUTH03 | 448 × 320 |
| 49 | ORD_MOUTH04 | 448 × 320 |
| 50 | ORD_MOUTH05 | 448 × 320 |

### ментат: текст и фоны (MENTAT*, MEN_*, HEN_*): 8

| номер | имя | ширина × высота |
|---|---|---|
| 34 | HEN_HARKONNEN | 732 × 108 |
| 35 | MEN_WISH | 1680 × 168 |
| 36 | MENTAT | 1280 × 960 |
| 37 | MENTATA | 2560 × 1920 |
| 38 | MENTATH | 2560 × 1920 |
| 39 | MENTATM | 2560 × 1920 |
| 40 | MENTATO | 2560 × 1920 |
| 51 | MENTATS | 2560 × 1920 |

## 5. sdl_data_hd4: записи интерфейса (36)

### курсоры (MOUSE_*): 11

| номер | имя | ширина × высота |
|---|---|---|
| 79 | MOUSE_ATTACK | 128 × 128 |
| 80 | MOUSE_DOWN | 72 × 72 |
| 81 | MOUSE_FORBIDDEN | 128 × 128 |
| 82 | MOUSE_LEFT | 64 × 80 |
| 83 | MOUSE_MOVE | 128 × 128 |
| 84 | MOUSE_NORMAL | 128 × 128 |
| 85 | MOUSE_PICK | 144 × 144 |
| 86 | MOUSE_RALLY | 128 × 128 |
| 87 | MOUSE_REPAIR | 128 × 128 |
| 88 | MOUSE_RIGHT | 64 × 80 |
| 89 | MOUSE_UP | 72 × 72 |

### CREDITS_*: 11

| номер | имя | ширина × высота |
|---|---|---|
| 53 | CREDITS_0 | 64 × 64 |
| 54 | CREDITS_1 | 64 × 64 |
| 55 | CREDITS_2 | 64 × 64 |
| 56 | CREDITS_3 | 64 × 64 |
| 57 | CREDITS_4 | 64 × 64 |
| 58 | CREDITS_5 | 64 × 64 |
| 59 | CREDITS_6 | 64 × 64 |
| 60 | CREDITS_7 | 64 × 64 |
| 61 | CREDITS_8 | 64 × 64 |
| 62 | CREDITS_9 | 64 × 64 |
| 63 | CREDITS_NONE | 64 × 64 |

### метки, туман, флаги (SHROUD, SMUDGE, FOCUS, PLACE_*, BUILDING_FLAG_*, ...): 13

| номер | имя | ширина × высота |
|---|---|---|
| 0 | ATTACK_INDICATOR | 1280 × 128 |
| 44 | BUILDING_FLAG_LARGE | 64 × 384 |
| 45 | BUILDING_FLAG_SMALL | 44 × 288 |
| 78 | FOCUS | 128 × 128 |
| 90 | MOVE_INDICATOR | 1280 × 128 |
| 109 | PLACE_SLAB1 | 128 × 128 |
| 110 | PLACE_SLAB4 | 256 × 256 |
| 111 | PLACE_WALL | 128 × 128 |
| 112 | SHOOT_TANK | 84 × 64 |
| 113 | SHROUD | 2048 × 128 |
| 114 | SHROUD_SHADOW | 2048 × 128 |
| 115 | SMUDGE | 1280 × 512 |
| 116 | SYMB_PICKMEUP | 40 × 40 |

### палитры (PAL*): 1

| номер | имя | ширина × высота |
|---|---|---|
| 108 | PALETTE_D2TM | 128 × 32 |

## 5. sdl_world_hd4: записи интерфейса (36)

### карта кампании и мира (PIECE_DUNE_*, WORLD_*, CONQUEST, BMP_N*): 35

| номер | имя | ширина × высота |
|---|---|---|
| 0 | BMP_NCATR | 256 × 256 |
| 1 | BMP_NCHAR | 256 × 256 |
| 2 | BMP_NCORD | 256 × 256 |
| 3 | BMP_NEXTCONQ | 2560 × 1920 |
| 4 | CONQUEST | 128 × 128 |
| 6 | PIECE_DUNE_001 | 512 × 208 |
| 7 | PIECE_DUNE_002 | 448 × 368 |
| 8 | PIECE_DUNE_003 | 512 × 368 |
| 9 | PIECE_DUNE_004 | 704 × 288 |
| 10 | PIECE_DUNE_005 | 448 × 384 |
| 11 | PIECE_DUNE_006 | 512 × 184 |
| 12 | PIECE_DUNE_007 | 512 × 480 |
| 13 | PIECE_DUNE_008 | 576 × 288 |
| 14 | PIECE_DUNE_009 | 384 × 320 |
| 15 | PIECE_DUNE_010 | 448 × 264 |
| 16 | PIECE_DUNE_011 | 320 × 400 |
| 17 | PIECE_DUNE_012 | 320 × 280 |
| 18 | PIECE_DUNE_013 | 320 × 368 |
| 19 | PIECE_DUNE_014 | 640 × 384 |
| 20 | PIECE_DUNE_015 | 576 × 400 |
| 21 | PIECE_DUNE_016 | 448 × 432 |
| 22 | PIECE_DUNE_017 | 384 × 240 |
| 23 | PIECE_DUNE_018 | 368 × 320 |
| 24 | PIECE_DUNE_019 | 192 × 456 |
| 25 | PIECE_DUNE_020 | 320 × 304 |
| 26 | PIECE_DUNE_021 | 448 × 232 |
| 27 | PIECE_DUNE_022 | 448 × 272 |
| 28 | PIECE_DUNE_023 | 448 × 224 |
| 29 | PIECE_DUNE_024 | 448 × 240 |
| 30 | PIECE_DUNE_025 | 512 × 240 |
| 31 | PIECE_DUNE_026 | 384 × 176 |
| 32 | PIECE_DUNE_027 | 440 × 344 |
| 33 | WORLD_DUNE | 2432 × 960 |
| 34 | WORLD_DUNE_CLICK | 2432 × 960 |
| 35 | WORLD_DUNE_REGIONS | 2432 × 960 |

### палитры (PAL*): 1

| номер | имя | ширина × высота |
|---|---|---|
| 5 | PALETTE_WORLD | 128 × 32 |

## 6. Сумма

PNG в `assets/`: 270 (по паки) + 12 (hd4) = 282. Папка `.cache/ui-redesign/assets/`: 286 файлов, 91439131 байт (91.4 MB), включая TSV.

## 7. Что не удалось и неопределённости

- Все записи всех четырёх паков декодированы как картинки; записей данных без картинки нет (0 в каждом TSV).
- Категории в разделе 5 даны по префиксу имени, а не по изображению. Смысл каждой записи визуально не проверен.
- Правило исключения по префиксу отбрасывает записи, которые могут быть интерфейсом: `BUILD_*` (включая `BUILD_*_FLAG`, `BUILD_LIGHTFACTORY_PRODUCTION`, `BUILD_PRE_*`), `HM_*`, `TERRAIN*`, `EXPLOSION_CARRYALL`. Их нет в PNG.
- Спорные по правилу, но сохранены: `BUILDING_FLAG_*`, `PLACE_*`, `SHOOT_TANK`, `SMUDGE`, `SHROUD`, `FOCUS`, `CREDITS_*`, `PALETTE_*`. Назначение не проверено.
- `STAT01..21` (512×512) и `PROGRESS*` в `sdl_inter_hd4` назначения не знаю, в раздел помещены только по префиксу.
- Сверка индексов с gfx-заголовками выполнена только для `sdl_inter_hd4` и `sdl_data_hd4`; для ментатов и карты заголовков в репозитории нет.
- Для ментатных пакетов и `sdl_world_hd4` PNG не открывались глазами, проверены только размеры и режимы.

