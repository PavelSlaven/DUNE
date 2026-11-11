# Разведка: шрифты и строки интерфейса (DUNE, порт и форк)

Дата: 2026-11-11. Режим: только чтение игры и репозитория; git-команд, меняющих состояние, не было. Рабочие файлы: `W/.cache/ui-redesign/` (скрипты, шрифты, `strings.tsv`, `strings.json`, `fonts/specimen.png`). Каталог `scripts/` общий с другими сессиями: файлы `build_report.py` и `dump_pack.py` там не мои, я их не трогал.

Обозначения: `W` = `C:/Users/Slaven/Projects/DUNE/.claude/worktrees/ui-redesign-360d77`; `origin/main` = форк (русская версия). Длина строки = число кодовых точек (`len` в Python).

## Команды (ключевые)

- `python --version; python -c "import PIL"` → Python 3.13.3, Pillow 12.2.0.
- `git ls-tree -r -l origin/main | grep -i -E "\.(ttf|otf|fon)$"` → в форке 10 шрифтовых файлов; в порте 5 (`arrak.ttf`, `arrakeen.fon`, `benegess.fon`, `benegess.ttf`, `small.ttf`). Хэши `git hash-object` порт = форк для всех пяти.
- `git show origin/main:resources/bin/data/{PTSansNarrow-Regular.ttf,RussoOne-Regular.ttf}` → LFS-указатели (131 и 130 байт), не доставались.
- `git show origin/main:<PTMono-Regular.ttf|RunttiSP-Bold.otf|Sangyo-Regular.otf> > W/.cache/ui-redesign/fonts/…` → размеры 185912, 166328, 133248 байт (совпадают с размерами блобов).
- `python -I -X utf8 .cache/ui-redesign/scripts/font_probe.py .cache/ui-redesign/fonts <тег> <ttf…>` → `probe_port.json`, `probe_fork.json`. Скрипт читает `name`, `cmap` (форматы 0/4/6/12), `maxp`, `head`, `hhea`, `OS/2` собственным кодом на `struct`; метрики — `ImageFont.getmetrics()` и `getlength()`.
- `python -I -X utf8 .cache/ui-redesign/scripts/specimen.py . .cache/ui-redesign/fonts/specimen.png` → 1100×2052 px, 6 шрифтов, 16 и 32 px.
- `python -I -X utf8 .cache/ui-redesign/scripts/fon_probe.py resources/bin/data/arrakeen.fon` → см. раздел «Ограничения».
- `git grep -n -i -e fallback -e TTF_AddFallbackFont -e "\.ttf" origin/main -- src`; чтение `src/context/ContextCreator.cpp` (строки 60–200), `src/utils/Localization.hpp`, `src/utils/FontSupport.hpp`, `src/drawers/cTextDrawer.cpp` (34–44).
- `python -I -X utf8 .cache/ui-redesign/scripts/extract_strings.py . origin/main .cache/ui-redesign/strings.tsv .cache/ui-redesign/strings.json` → разбор 291 вызова `localization::text/format` в 34 файлах, 248 уникальных ключей, 0 нераспарсенных вызовов.
- `python -I -X utf8 .cache/ui-redesign/scripts/stats.py .cache/ui-redesign/strings.json` → статистика без отладочных строк.
- Сверка англ. строк форка с портом (Python, подстроки в `W/src`, `W/resources`): 232 ключа длиной ≥ 4 вне отладки, 126 найдено дословно (подстрочное совпадение, не точное).

## Часть А. Шрифты порта

### А.1 Метаданные

| Файл | Семейство (name 1 / 4) | Авторское право (name 0) | Лицензия (name 13) | Глифов (maxp) | Кодовых точек в cmap | upem | Подтаблицы cmap |
|---|---|---|---|---|---|---|---|
| arrak.ttf | Algerian (полное имя Algerian; в nl/es локалях — Arrakeen) | URW Software, Copyright 1993 by URW | нет | 204 | 236 | 2048 | (3,1) |
| benegess.ttf | Bene Gesserit / Bene Gesserit | Virgin/Westwood Studios; extracted Nema Fakei | нет | 228 | 220 | 1000 | (0,3), (3,1) |
| small.ttf | 04b03 / 04b03 | 1999-2003 / yuji oshimoto / 04@dsg4.com / www.04.jp.org | нет | 99 | 97 | 1000 | (0,0), (3,1) |

Файлов лицензий в порте (`W/resources/bin`, `W/resources/bin/data`) нет. В форке для этих трёх шрифтов лицензии тоже нет: в `resources/bin/THIRD_PARTY_ASSETS_RU.txt` (строка 40) упомянуты Westwood Studios и Virgin Interactive без условий лицензии.

Диапазоны Юникода (полный список — в `W/.cache/ui-redesign/fonts/probe_port.json`, поле `ranges`): arrak — 35 диапазонов, benegess — 18, small — 3. Все три покрывают ASCII-буквы и цифры и не покрывают кириллицу.

### А.2 Покрытие знаков (cmap)

| Шрифт | Группа | Есть из N | Каких нет |
|---|---|---|---|
| arrak.ttf | Латиница A–Z | 26/26 | — |
| arrak.ttf | Латиница a–z | 26/26 | — |
| arrak.ttf | Цифры 0–9 | 10/10 | — |
| arrak.ttf | Кириллица А–Я | 0/32 | все |
| arrak.ttf | Кириллица а–я | 0/32 | все |
| arrak.ttf | Ё ё | 0/2 | все |
| arrak.ttf | Пунктуация | 26/27 | № |
| arrak.ttf | Типографика | 8/8 | — |
| arrak.ttf | Стрелки/значки | 2/12 | ← → ↑ ↓ ▲ ▼ ◄ ► ✓ · (есть × •) |
| benegess.ttf | Латиница A–Z | 26/26 | — |
| benegess.ttf | Латиница a–z | 26/26 | — |
| benegess.ttf | Цифры 0–9 | 10/10 | — |
| benegess.ttf | Кириллица А–Я | 0/32 | все |
| benegess.ttf | Кириллица а–я | 0/32 | все |
| benegess.ttf | Ё ё | 0/2 | все |
| benegess.ttf | Пунктуация | 26/27 | № |
| benegess.ttf | Типографика | 8/8 | — |
| benegess.ttf | Стрелки/значки | 3/12 | ← → ↑ ↓ ▲ ▼ ◄ ► ✓ (есть · × •) |
| small.ttf | Латиница A–Z | 26/26 | — |
| small.ttf | Латиница a–z | 26/26 | — |
| small.ttf | Цифры 0–9 | 10/10 | — |
| small.ttf | Кириллица А–Я | 0/32 | все |
| small.ttf | Кириллица а–я | 0/32 | все |
| small.ttf | Ё ё | 0/2 | все |
| small.ttf | Пунктуация | 26/27 | № |
| small.ttf | Типографика | 0/8 | « » — – … ’ “ ” |
| small.ttf | Стрелки/значки | 0/12 | все |

### А.3 Метрики Pillow (px = размер em, ascent/descent из `getmetrics()`, ширины из `getlength()`)

Ширины «Постройки» у шрифтов порта — это ширина глифа-заглушки (.notdef), потому что кириллицы в них нет. Число не говорит о реальной ширине текста.

| Шрифт | px | ascent | descent | строка | Structures | Mission accomplished | 1234567890 | Постройки |
|---|---|---|---|---|---|---|---|---|
| arrak | 12 | 11 | 4 | 15 | 71.5 | 132.7 | 71.9 | 27.0 (заглушка) |
| arrak | 16 | 15 | 5 | 20 | 95.3 | 176.9 | 95.9 | 36.0 (заглушка) |
| arrak | 20 | 18 | 6 | 24 | 119.1 | 221.1 | 119.7 | 45.0 (заглушка) |
| arrak | 24 | 22 | 7 | 29 | 143.0 | 265.4 | 143.8 | 54.0 (заглушка) |
| arrak | 32 | 29 | 9 | 38 | 190.6 | 353.8 | 191.6 | 72.0 (заглушка) |
| benegess | 12 | 10 | 3 | 13 | 69.2 | 144.0 | 72.8 | 39.4 (заглушка) |
| benegess | 16 | 13 | 4 | 17 | 92.3 | 192.0 | 97.2 | 52.5 (заглушка) |
| benegess | 20 | 16 | 4 | 20 | 115.4 | 240.0 | 121.5 | 65.5 (заглушка) |
| benegess | 24 | 20 | 5 | 25 | 138.4 | 288.0 | 145.8 | 78.6 (заглушка) |
| benegess | 32 | 26 | 7 | 33 | 184.6 | 384.0 | 194.4 | 104.8 (заглушка) |
| small | 12 | 9 | 3 | 12 | 67.5 | 130.5 | 72.0 | 54.0 (заглушка) |
| small | 16 | 12 | 4 | 16 | 90.0 | 174.0 | 96.0 | 72.0 (заглушка) |
| small | 20 | 15 | 5 | 20 | 112.5 | 217.5 | 120.0 | 90.0 (заглушка) |
| small | 24 | 18 | 6 | 24 | 135.0 | 261.0 | 144.0 | 108.0 (заглушка) |
| small | 32 | 24 | 8 | 32 | 180.0 | 348.0 | 192.0 | 144.0 (заглушка) |

### А.4 Образцы

`W/.cache/ui-redesign/fonts/specimen.png` (1100×2052, светлый текст на тёмном фоне, 16 и 32 px, подпись с именем файла). Строки: A–Z, a–z с цифрами, А–Я, а–я. Квадраты в образце — отсутствующие глифы: у трёх шрифтов порта кириллица везде квадраты.

## Часть Б. Шрифты форка

### Б.0 Что есть в форке и чего нет в порте

| Файл в форке | Размер, байт | В порте | Статус |
|---|---|---|---|
| PTMono-Regular.ttf | 185912 | нет | доставлен в `fonts/` |
| RunttiSP-Bold.otf | 166328 | нет | доставлен в `fonts/` |
| Sangyo-Regular.otf | 133248 | нет | доставлен в `fonts/` |
| PTSansNarrow-Regular.ttf | 131 | нет | LFS-указатель (`size 396212`) — не доставлен |
| RussoOne-Regular.ttf | 130 | нет | LFS-указатель (`size 39124`) — не доставлен |
| arrak.ttf, arrakeen.fon, benegess.fon, benegess.ttf, small.ttf | те же | да | хэши совпадают |

### Б.1–Б.3 Метаданные, покрытие, метрики

| Шрифт | Семейство / авторство / лицензия | Глифов | Кодовых точек | Латиница | Цифры | Кириллица (А–Я, а–я, Ёё) | Пунктуация | Типографика | Значки |
|---|---|---|---|---|---|---|---|---|---|
| PTMono-Regular.ttf | PT Mono, ParaType Ltd. 2010; OFL 1.1 | 808 | 805 (подтаблицы (0,3), (3,1)) | 26/26, 26/26 | 10/10 | 32/32, 32/32, 2/2 | 27/27 | 8/8 | 11/12 (нет ✓) |
| RunttiSP-Bold.otf | Runtti SP Bold; OFL 1.1 (в name 13) | 387 | 386 ((3,1)) | 26/26, 26/26 | 10/10 | 32/32, 32/32, 2/2 | 22/27 (нет + = % № $) | 8/8 | 2/12 (нет ← → ↑ ↓ ▲ ▼ ◄ ► ✓ ×; есть • ·) |
| Sangyo-Regular.otf | Sangyo, © 2024 GGBotNet; OFL 1.1 | 818 | 820 ((0,3), (0,4), (3,1), (3,10)) | 26/26, 26/26 | 10/10 | 32/32, 32/32, 2/2 | 27/27 | 8/8 | 3/12 (нет ← → ↑ ↓ ▲ ▼ ◄ ► ✓; есть × • ·) |

Метрики Pillow (ascent / descent / строка; ширины — реальные, кириллица есть):

| Шрифт | 12 px | 16 px | 20 px | 24 px | 32 px | Постройки 16 px | Structures 16 px | Mission accomplished 16 px | 1234567890 16 px |
|---|---|---|---|---|---|---|---|---|---|
| PTMono | 11/3/14 | 15/4/19 | 18/5/23 | 22/6/28 | 29/8/37 | 86.3 | 95.9 | 191.9 | 95.9 |
| RunttiSP-Bold | 10/3/13 | 13/4/17 | 16/5/21 | 19/6/25 | 25/8/33 | 79.7 | 67.5 | 144.6 | 77.4 |
| Sangyo | 11/2/13 | 15/2/17 | 18/2/20 | 22/3/25 | 29/4/33 | 57.7 | 64.1 | 126.5 | 64.1 |

Полные строки метрик по всем размерам и ширины «Постройки» на 12–32 px — в `W/.cache/ui-redesign/fonts/probe_fork.json`.

Метрики `hhea` и `OS/2` у форка: PTMono asc 885 / desc −235 (upem 1000); RunttiSP asc 766 / desc −240 (win 949/230); Sangyo asc 900 / desc −100.

### Б.4 Запасной шрифт и подключение (форк)

- Настройки: `resources/bin/settings.ini` форка, секция `[FONT]` (строки 79–82): `ARRAKEEN=PTMono-Regular.ttf`, `BENEGESS=PTSansNarrow-Regular.ttf`, `SMALL=PTMono-Regular.ttf`. Порт (`W/resources/bin/settings.ini`, строки 89–92) использует `arrakeen.fon`, `benegess.fon`, `small.ttf`. В порте ключа `Language` нет, в форке `Language=ru` (строка 10).
- `src/context/ContextCreator.cpp` (origin/main), строки 73–84: путь основного русского шрифта `fontDirectory / "Sangyo-Regular.otf"`, шрифт Mentat — `RussoOne-Regular.ttf`. Строки 85–131: `useRussianFont = !isEnglish() && файл Sangyo существует`. Лямбда `openLocalizedFont` берёт Sangyo как основной и настроенный шрифт как «запасной» (`game_fallback_font`, `bene_fallback_font`, `small_fallback_font`, `menu_fallback_font`, `mentat_hd_fallback_font`). Это не `TTF_AddFallbackFont`: в форке такого вызова нет (поиск по `origin/main -- src` пустой).
- Выбор запасного шрифта по строке: `src/drawers/cTextDrawer.cpp` (origin/main), строки 36–41: `useFallback = !ttfFontSupportsText(m_font, msg) && ttfFontSupportsText(m_fallbackFont, msg)`, результат кешируется по строке.
- `src/utils/FontSupport.hpp` (origin/main): проверка по кодовым точкам UTF-8 через `TTF_GlyphIsProvided32` из `<SDL2/SDL_ttf.h>`. Форк собран на SDL2; порт на SDL3. Аналог в SDL3_ttf в этой разведке не проверялся.
- Уязвимость (выведено из кода и настроек, не запускалось): при английской локали основной и запасной шрифты — `PTSansNarrow-Regular.ttf` (LFS-указатель) и `PTMono-Regular.ttf`. Без `git lfs pull` открытие `BENEGESS` упадёт; Mentat-шрифт `RussoOne` тоже LFS.

### Б.5 Лицензии форка

- `resources/bin/OFL_PT_FONTS.txt` (4586 байт): PT Sans Narrow и PT Mono, ParaType, SIL OFL 1.1.
- `resources/bin/data/OFL_RUSSO_ONE.txt` (4389 байт): Russo One, Jovanny Lemonad, SIL OFL 1.1.
- `resources/bin/data/licenses/Sangyo-LICENSE.txt` (4301 байт) и `Sangyo-COPYRIGHT.txt` (38 байт): Sangyo, © 2024 GGBotNet, SIL OFL 1.1.
- `resources/bin/data/licenses/RunttiSP-ReadMe.pdf` (587680 байт): PDF-1.3; текст не читался, в name-таблице указана OFL 1.1.
- `resources/bin/THIRD_PARTY_ASSETS_RU.txt`: общий перечень сторонних ресурсов.

## Часть В. Строки интерфейса

### В.5 Формат

Строки форка лежат в коде, таблиц и `.po`-файлов нет. Механизм — `src/utils/Localization.hpp` (origin/main): глобальный `bool english`, `setLanguage(language)` (вызывается в `src/cGame_logic.cpp:187` из настройки `Language`). Функции: `localization::text("en", "ru")` и `localization::format("en {}", "ru {}", args…)`, выбор по флагу. Также `isEnglish()` используется в 13 местах (например `cCommandBarDrawer.cpp:87–92`, `ini.cpp:422`, `map/cPreviewMaps.cpp:207` — выбор папки `skirmish_en`), `campaignRoot()` возвращает `campaign_en` или `campaign`.

Вызовов `localization::text/format`: 291 в 34 файлах `src/` (распределение по файлам: `cIniGameRessouces.cpp` 56, `SaveGameManager.cpp` 39, `cSetupSkirmishState.cpp` 25, `cPlayer.cpp` 17, `cMouseDrawer.cpp` 16, `cMousePlaceState.cpp` 7, `cBuildingListDrawer.cpp` 8 и т. д.). Вне кода: `resources/hd/CARD_NAMES_RU.json` (русские названия карточек с ключами `ICON_STR_*`/`ICON_UNIT_*`), он используется только `tools/verify_hd_card_catalog.py`. Изображения исхода: `resources/bin/data/hd4/outcome_{victory,defeat}_{en,ru}.png` (выбор в `src/gamestates/cWinLoseState.cpp`) — текст исхода растровый, в TSV его нет.

### В.6 TSV

`W/.cache/ui-redesign/strings.tsv`: 248 строк данных (+ заголовок). Столбцы: ключ (= английская строка), английский текст, русский текст, длина en, длина ru, категория, число вызовов, конфликт ru, место `файл:строка`. Категории по пути файла: названия построек и юнитов 46 (`IniGameRessouces`), сохранение 48, боковая панель 33, сообщения 30, схватка 27, настройки 27, меню 23, ментат 8, отладка 6 (`src/debug/`). Категория «исход» пуста (текст — картинки).

Строк без `src/debug/`: 242. Конфликты (одна английская строка — разные русские): `CREDITS` (КРЕДИТЫ), `Troopers` (Отряд ракетчиков / Ракетчики в compactCardName), `Atreides` (Атрейдес), `Harkonnen` (Харконнен).

### В.7 Статистика (без отладки, n = 242)

- Отношение ru/en: среднее 1.201, медиана 1.091, максимум 5.333 (`WOR` → `Военная академия`, аббревиатура), минимум 0.529.
- Длина en: среднее 15.5, медиана 13, максимум 69. Длина ru: среднее 17.2, медиана 14, максимум 62.
- 20 самых длинных русских строк (ru / en, место):

| # | ru | en | место |
|---|---|---|---|
| 1 | 62 | 69 | cMousePlaceState.cpp:63 |
| 2 | 57 | 58 | cMousePlaceState.cpp:68 |
| 3 | 57 | 54 | cMousePlaceState.cpp:88 |
| 4 | 50 | 46 | SaveGameManager.cpp:1041 |
| 5 | 50 | 46 | SaveGameManager.cpp:1320 |
| 6 | 48 | 49 | cMousePlaceState.cpp:83 |
| 7 | 48 | 46 | cPlayer.cpp:2140 |
| 8 | 45 | 36 | SaveSlotsDialog.cpp:226 |
| 9 | 44 | 36 | SaveGameManager.cpp:1300 |
| 10 | 43 | 44 | cMousePlaceState.cpp:78 |
| 11 | 42 | 60 | cMousePlaceState.cpp:73 |
| 12 | 41 | 33 | cPlayer.cpp:2119 |
| 13 | 41 | 28 | SaveFileCodec.cpp:65 |
| 14 | 41 | 32 | SaveGameManager.cpp:622 |
| 15 | 38 | 24 | SaveGameManager.cpp:409 |
| 16 | 38 | 41 | SaveGameManager.cpp:1454 |
| 17 | 36 | 24 | SaveGameManager.cpp:629 |
| 18 | 36 | 38 | cIniGameRessouces.cpp:1126 |
| 19 | 35 | 35 | SaveGameManager.cpp:514 |
| 20 | 35 | 24 | SaveGameManager.cpp:682 |

В двадцатке самые длинные строки — сообщения (ошибки сохранения, подсказки размещения), не подписи кнопок.

### В.8 Названия построек и юнитов

Источник: `src/utils/cIniGameRessouces.cpp` (названия и подсказки) и `src/drawers/cBuildingListDrawer.cpp:54–57` (короткие имена в карточках). Приблизительная выборка: 34 названия из `IniGameRessouces` без подсказок «Build …».

- Самое длинное en-название: `Spice Storage Silo` (18).
- Самое длинное ru-название: `Переработчик пряности` (21, `cBuildingListDrawer.cpp:54` — полное имя `Spice Refinery`; короткая карточка — `Переработчик`, 12); `Бетонная площадка 2×2` (21, `cIniGameRessouces.cpp:1263`, en `4 Concrete Slabs`). Из `IniGameRessouces`: `Хранилище пряности` (18) и `Ракетная установка` (18).
- Расхождение: `CARD_NAMES_RU.json` называет здание `Перерабатывающий завод` (22) и ветроловушку `Ветряная ловушка` (16), в коде — `Переработчик пряности` и `Ветроловушка` (12). JSON используется только инструментом.

## Часть В.8 порта: где заданы строки

Порт английский, кириллицы в `W/src` нет (поиск по всем 443 файлам `.cpp/.h/.hpp`: 0 файлов). Строки литералами в коде, таблиц и `localization` нет.

Примеры `путь:строка`:
1. `src/gamestates/cMainMenuState.cpp:166` — `addButton("Options", …)`
2. `src/gamestates/cOptionsState.cpp:167` — `.withLabel("Save game")`
3. `src/context/cInfoContextCreator.cpp:255` — `unitInfos[HARVESTER].name = "Harvester";`
4. `src/context/cInfoContextCreator.cpp:1634` — `structureInfos[REFINERY].name = "Spice Refinery";`
5. `src/context/cInfoContextCreator.cpp:1283` — `…description = "Build Ornithopter at Hi-Tech";`
6. `src/gameobjects/players/cPlayer.cpp:2269` — `.message = "No harvesters and refineries left!";` (в форке: `or`)
7. `src/gamestates/cScoringState.cpp:109` — `drawTextCentered("Click to continue", …)`
8. `src/gameobjects/mentat/AbstractMentat.cpp:89` — `.withLabel("Mission select")`
9. `src/gamestates/cWinLoseState.cpp:58–59` — выбор `outcome_defeat_en.png` / `outcome_victory_en.png`
10. `src/context/ContextCreator.cpp:78` — `TTF_OpenFont(…ARRAKEEN…, 12)`; имя файла задано в `W/resources/bin/settings.ini:90`.

## Ограничения и неопределённости

1. FON-шрифты не измерены. Pillow открывает `arrakeen.fon` только на 16 px, `benegess.fon` только на 13 px. Все символы `arrakeen.fon` при 16 px рисуются одинаковым блоком 5×10 (проверено рендером `Ж`, `A`, `b`, `1`), поэтому ширины и покрытие по нему недостоверны. Разбор FNT-таблиц вне задачи.
2. Покрытие — по `cmap` подтаблицам (0,x), (3,x). Глифы, доступные только через нестандартные подтаблицы, не учтены.
3. Метрики — Pillow (FreeType), SDL_ttf может округлять иначе. Размеры — в пикселях em.
4. Сверка «есть в порте» — подстрочная (126 из 232), не точная: короткие ключи совпадают случайно (например, `Refinery` в `CMakeLists.txt`).
5. Строки: учтены только `localization::text/format`. Английские литералы без локализации в форке (например, `addNotification("…")`) не разбирались. Строки с выбором через `isEnglish()` (13 мест) разобраны вручную частично.
6. Категории и «названия» — эвристики по пути файла и по префиксу `Build `.
7. Конфликты (4 строки) не разрешены: какой вариант нужен, решает владелец.
8. Не проверено: отрисовка шрифтов в игре, поведение при отсутствии LFS, аналог `TTF_GlyphIsProvided32` в SDL3_ttf.

## Расход

Оценка: около 200 тыс. токенов (по ходу работы, оценка без точного счётчика). Субагентов не запускалось.
