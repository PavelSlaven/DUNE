# RECON-P6R

## Рабочие ревизии и метод

Ревизии для команд: `BASE=e17379ad660fca46859b403a6c3d33ec8d831a40`, `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566`, `UP1=d06f2fcd2a347182c3774fb96e9a85570405c489`, `PORT=0a33444e9032ef935dfe4cdde6bb622771484230`, `MAIN=62e1ff6585d8f1f047a3f983c63d990662e6afb6`. Перед командами Git использовался `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`. Рабочие ревизии читались только командами Git с явным SHA. Сборки, CTest и запуск игры не выполнялись.

## Чтение

До разведки прочитаны отдельными вызовами:

- `git show MAIN:docs/upstream/PORT_PLAN.md` — весь файл. Раздел 4 задаёт П6 после П4 и параллельно с П5; раздел 5 описывает П6 как перенос масок цвета Дома и вариаций поверхности и переданных HD-меток/флага ветряка; раздел 6 задаёт вопрос «цвет Сардаукаров».
- `git show MAIN:docs/upstream/PORT_MAP.md | sed -n '9,36p;442,466p'` — выведена строка функции `faction-tint-terrain`, перечень путей и количество `tools: 4`.
- `git show MAIN:docs/decisions.md | grep -E '^- \*\*Р(11|25|28|33|34|60|65)\.'` — команда напечатала шесть строк: Р25, Р28, Р33, Р34, Р60, Р65. Р11 не подошло под регулярное выражение, потому что заголовок в файле имеет вид `**Р11 (О3).`, а не `**Р11.`. Поэтому отдельной командой `git show MAIN:docs/decisions.md | rg -n 'Р[[:space:]0]*11|R11|решение 11'` прочитана строка 19: Р11 задаёт для юнитов цвет Дома по цвету краски модели; уточнение Р18 ограничивает окраску крупными броневыми плитами. Таким образом, прочитаны все семь перечисленных решений, но исходная команда задания вернула шесть.
- `git show MAIN:docs/PLAN_units_sega_upstream.md` сначала предупредил об усечённом выводе. Файл дочитан тремя командами `sed -n '1,100p'`, `sed -n '101,200p'`, `sed -n '201,320p'` от того же `git show`; последняя часть завершилась концом файла. План ссылается на §3.2 и §5.3 и на README форка как источник списка функций и тестов.
- `git show MAIN:codex-direct/launch-card-27.md` — весь файл, в том числе правила запуска шагов П2–П15 и ответы владельца о переносе функций.
- Дополнительно прочитаны связанные с источником функций разделы `git show FORK1:README_AI.md | sed -n '1,22p'` (§1) и `sed -n '117,168p'` (§5): §1 описывает состав RU/HD-функций и совместимость ID, §5 перечисляет тесты `faction_tint_tests` и `terrain_variation_tests`. Они не меняют объём этого задания, которое задаёт точные пути и фактические вопросы.

«Не хватило в задании»: в предпосылках плана указаны ссылки на §3.2/§5.3 и README форка, но сам текст этих источников в перечень обязательного чтения не включён; план и README прочитаны, чтобы сверить порядок переноса, роль тестов и происхождение списка функций. Единственное несоответствие чтения — фильтр Р11, описанное выше; Р11 прочитано отдельно до сдачи.

## 1. Код `faction-tint-terrain` в FORK1

Таблица `fork.tsv` содержит 41 строку данных: функции, структуры, константы, изменённые участки diff, входы/выходы и места вызова. Пути из карты проверялись отдельно командами `git diff BASE FORK1 -- <путь>`; в следующей таблице приведены существенные выводы diff. Это выборки из вывода, а не полные листинги.

| Путь | Команда | Существенный вывод diff |
|---|---|---|
| `CMakeLists.txt` | `git diff BASE FORK1 -- CMakeLists.txt` | Добавлены `include(CTest)`, цели двух тестовых программ и CTest `terrain_variation_selection`/`faction_tint_uniformity`; изменены Apple compiler flags. Подробные строки — `fork.tsv:2` и строки CMake в таблице тестов. |
| `src/drawers/TerrainVariation.hpp` | `git diff BASE FORK1 -- src/drawers/TerrainVariation.hpp` | Новый файл: `HD_TERRAIN_VARIANT_COUNT=5`, `supportsHdTerrainVariants`, `hdTerrainVariantIndex`, `hdTerrainVariantName`; соответствующие строки FORK1 — `:8,10,25,42`. |
| `src/drawers/cMapDrawer.cpp` | `git diff BASE FORK1 -- src/drawers/cMapDrawer.cpp` | Добавлен выбор детерминированной вариации по ячейке и типу; `drawShroud` и террейн используют выделение кадра/отрисовку полного кадра. Код — `@9208dcf:73,85,137-172`; вызовы новых variation-функций — `@9208dcf:152,154`. |
| `src/drawers/cStructureDrawer.cpp` | `git diff BASE FORK1 -- src/drawers/cStructureDrawer.cpp` | Добавлены 12 HD-флагов зданий, основание стройки и харвестер на площадке НПЗ; основной слой выбирает HD-флаг с fallback к `structure->drawFlags()`. Определения `@9208dcf:304,346,388,430,473,515,557,599,641,683,725,768,810,846`; вызовы — `@9208dcf:208,245,249-281,969`. |
| `src/drawers/cStructureDrawer.h` | `git diff BASE FORK1 -- src/drawers/cStructureDrawer.h` | Добавлены `Graphics *m_gfxdata` и объявления HD-флагов, основания и харвестера; `@9208dcf:31,37-50`. |
| `src/player/cPlayer.cpp` | `git diff BASE FORK1 -- src/player/cPlayer.cpp` | В `setHouse` HD-ресурсы направляются в `Graphics::getHouseTexture`, классические INDEX8-текстуры — в палитровую функцию; изменена конвертация RGBA. House-участок `@9208dcf:252-335`, конвертация начинается `:2418`. В том же файле есть несвязанные с tint изменения размещения зданий, уведомлений и локализации. |
| `src/player/cPlayer.h` | `git diff BASE FORK1 -- src/player/cPlayer.h` | Добавлены состояние HD-ссылок текстур, `s_PlaceResult`, проверка размещения и другие игровые поля; `@9208dcf:63,438,494,546,569-570`. |
| `src/utils/FactionTint.hpp` | `git diff BASE FORK1 -- src/utils/FactionTint.hpp` | Новый файл с эталонной яркостью `166.0F/255.0F` и `applyFactionTintChannel(target,pixelLuminance,averageLuminance)`, который нормализует яркость по маске и ограничивает канал 0–255; `@9208dcf:7-21`. |
| `src/utils/Graphics.cpp` | `git diff BASE FORK1 -- src/utils/Graphics.cpp` | Добавлены кадровый API, House-варианты `HV_`/`HOUSEVARIANT_`, поиск `HM_`/`HOUSEMASK_`, luminance-masking и кэши. Центральная функция `getHouseTexture` — `@9208dcf:226-470`; поиск именованных масок — `:295-308`, применение — `:369-448`. |
| `src/utils/Graphics.hpp` | `git diff BASE FORK1 -- src/utils/Graphics.hpp` | Добавлены `getHouseTexture`, кадровые методы, плотность и кэш `HouseTexCacheKey`; `@9208dcf:23,38-71,86`. |
| `src/utils/cDataPack.cpp` | `git diff BASE FORK1 -- src/utils/cDataPack.cpp` | Добавлены обратные индексы surface→index, index→name и `isValid`; `@9208dcf:42-68,127`. |
| `src/utils/cDataPack.hpp` | `git diff BASE FORK1 -- src/utils/cDataPack.hpp` | Объявлены `getIndexFromSurface`, `getNameFromIndex`, `isValid` и `surfaceIndex`; `@9208dcf:46-64`. |
| `src/utils/cPack.cpp` | `git diff BASE FORK1 -- src/utils/cPack.cpp` | Добавлены проверка целостности пакета/чтения и поиск имени по индексу; `@9208dcf:29-50,130-164`. |
| `src/utils/cPack.h` | `git diff BASE FORK1 -- src/utils/cPack.h` | Добавлены `getNameFromIndex`, `isValid` и флаг `valid`; `@9208dcf:34,42,55`. |
| `tests/FactionTintTests.cpp` | `git diff BASE FORK1 -- tests/FactionTintTests.cpp` | Новый `main()` проверяет равенство цели при разных яркостях, сохранение теней/бликов и нулевой канал; `@9208dcf:5-25`. |
| `tests/TerrainVariationTests.cpp` | `git diff BASE FORK1 -- tests/TerrainVariationTests.cpp` | Новый `main()` проверяет границы, имена, детерминизм и покрытие пяти значений на 4096 ячейках; `@9208dcf:7-32`. |

Для всех строк `fork.tsv` исходные команды были `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- <путь>`, а выводы — изменения и сигнатуры, приведённые выше и разложенные по строкам в таблице. Маска поверхности поддерживается для HILL, MOUNTAIN, ROCK, SAND, SPICE и SPICEHILL; варианты выбираются только для базовой плитки `tileIndex=0`, индексы — 0..4. `getHouseTexture` ищет сначала варианты House, затем маску выбранного ресурса и fallback-маску базового ресурса; House-цветом остаётся RGB `minimapColor`, а исходная яркость маски сохраняет объём/светотень.

## 2. Инструменты

Команда `git diff --name-status BASE FORK1 -- tools | wc -l` вывела `305`. Фильтр четырёх файлов из `tools/upstream/port_features.json@9208dcf:550-553` вывел:

```text
A tools/check_unit_mask_uniformity.py
A tools/normalize_faction_masks.py
A tools/verify_building_flag_colors.py
A tools/verify_harvester_house_colors.py
```

Широкий поиск `git grep -n -i -E 'tint|terrain|variation|house.?colou?r' FORK1 -- tools` дал 505 строк; полный вывод целевой маски по четырём скриптам содержал 15 совпадений: 4 в `normalize_faction_masks.py`, 7 в `verify_building_flag_colors.py`, 4 в `verify_harvester_house_colors.py`, 0 в `check_unit_mask_uniformity.py`. Вывод целевого поиска:

```text
normalize_faction_masks.py:26 HOUSE_COLORS
normalize_faction_masks.py:55 apply_tint
normalize_faction_masks.py:147-148 apply_tint / HOUSE_COLORS
verify_building_flag_colors.py:35 HOUSE_COLORS
verify_building_flag_colors.py:79 apply_engine_tint
verify_building_flag_colors.py:124,164 проверки пустой/отсутствующей маски
verify_building_flag_colors.py:127-129 цикл цветов и применение tint
verify_harvester_house_colors.py:2 описание, :37 tint, :75 вызов tint, :134 итог проверки
```

Все четыре инструмента запускаются человеком как CLI; совпадений вызова из CMake или другого скрипта не найдено. Содержание, входные файлы и побочные выходные файлы указаны в `tools.tsv`.

## 3. Апстрим в тех же путях

Для путей карты выполнялись `git diff BASE UP1 -- <путь>`; для `src/player/cPlayer.cpp/.h` дополнительно `git diff -M --find-renames=20% BASE UP1 -- <старый путь> <новый путь>`. Статусы по точным путям: изменены `CMakeLists.txt`, `src/drawers/cMapDrawer.cpp`, `src/drawers/cStructureDrawer.cpp/.h`, `src/utils/Graphics.cpp/.hpp`, `src/utils/cDataPack.cpp/.hpp`, `src/utils/cPack.cpp/.h`; `src/player/cPlayer.cpp/.h` перемещены в `src/gameobjects/players/cPlayer.cpp/.h` с совпадением 57% и 64%; `TerrainVariation.hpp`, `FactionTint.hpp` и два тестовых файла отсутствуют в UP1. Вывод `git diff -M` содержал `rename from src/player/cPlayer.cpp` / `rename to src/gameobjects/players/cPlayer.cpp` и соответствующие строки `.h`.

`git diff -U5 BASE UP1 -- src/drawers/cMapDrawer.cpp` показывает, что `drawTerrainCells(bool fogged)` при тумане берёт сохранённые `type/tile` (`src/drawers/cMapDrawer.cpp@d06f2fc:230-242`) и рисует обычный кадр `terrainTile*32` через `getTexture(terrainType)` (`:251-253`); именованных вариантов нет. Это пересекается с выбором `hdTerrainVariantIndex/Name` в `fork.tsv:8`.

`git diff -U1 BASE UP1 -- src/drawers/cStructureDrawer.cpp src/drawers/cStructureDrawer.h | rg '^diff |^@@|^\\+[^+]'` показал новый `drawRememberedStructures` (`src/drawers/cStructureDrawer.cpp@d06f2fc:82`, объявление `.h:41`), который рисует сохранённый bitmap структуры владельца при тумане. Другой общий hunk `drawStructureForLayer` связан со значком малой мощности, а не HD-флагами. Пересечение общего пути — `fork.tsv:10`; HD-флагов и HM-масок в UP1 нет.

`git diff -U3 BASE UP1 -- src/player/cPlayer.cpp src/gameobjects/players/cPlayer.cpp | rg -n -C 7 'getColors|setHouse|createPlayerTexture|createTextureFromIndexedSurface|palette|Palette|HouseColors|emblemBackground|SARDAUKAR'` показывает перенос игрока и палитровый путь: `cPlayer::getColors()` объявлен в `src/gameobjects/players/cPlayer.cpp@d06f2fc:157-160`; `setHouse` создаёт текстуры флагов/зданий/юнитов palette helper-ом (`:277,286,298,310,316`). Цвет Сардаукарского emblem в этом diff меняется на `{101,12,101}`. Таблица цветов хранится в `src/gameobjects/players/cHousesInfo.cpp@d06f2fc:36-75`, тип — `src/utils/HouseColors.h@d06f2fc:21,25`; `SDLDrawer.cpp@d06f2fc:344,387-398` кладёт семь HouseColors в palette slots 144–150. Это пересекает подготовку House-текстур `fork.tsv:18,19,31,32`, но пиксельной HM-маски в UP1 нет.

Для `Graphics`, `cDataPack`, `cPack` и CMake выполнялся `git diff -U1 BASE UP1 -- <пути> | rg '^diff |^@@|^\\+[^+]'`. Вывод показывает SDL3 texture/cache и I/O изменения, `SDL_RWops` → `SDL_IOStream`, `enable_testing()`/`add_subdirectory(tests)`; новых символов fork tint там нет. Поддерживающие пути и строки пересечения включены в `upstream.tsv`.

`git grep -n -E 'getHouseTexture|FactionTint|HM_BUILD|HOUSEMASK_|hdTerrainVariant|TerrainVariation' UP1 -- src` вывел пустой stdout. В UP1 вместо маскирования есть `HouseColors`: `cPlayer::getColors()` выдаёт палитру; `SDLDrawer::createTextureFromIndexedSurfaceWithPalette` заменяет индексы 144–150.

## 4. Состояние PORT и переданные из П4 метки

В `port.tsv` приведены все пути карты, существующие в PORT, relocated `src/gameobjects/players/cPlayer.*`, поддерживающие пути цвета и пять записей HD-масок из alignment TSV. В PORT отсутствуют `src/drawers/TerrainVariation.hpp`, `src/utils/FactionTint.hpp`, `tests/FactionTintTests.cpp`, `tests/TerrainVariationTests.cpp` и старые пути `src/player/cPlayer.*`.

`git ls-tree PORT -- <пути faction-tint-terrain с relocated cPlayer>` вывел 12 существующих файлов: `CMakeLists.txt`, `src/drawers/cMapDrawer.cpp`, `src/drawers/cStructureDrawer.cpp/.h`, `src/gameobjects/players/cPlayer.cpp/.h`, `src/utils/Graphics.cpp/.hpp`, `src/utils/cDataPack.cpp/.hpp`, `src/utils/cPack.cpp/.h`. `git grep -n -E 'getHouseTexture|FactionTint|HM_BUILD_(LIGHTFACTORY|SILO|CONSTYARD|BARRACKS|WINDTRAP)_FLAG|hdTerrainVariant(Index|Name)|TerrainVariation' PORT -- src` вывел пустой stdout. Отдельный поиск CTest-имён также пуст; `CMakeLists.txt@0a33444:95-96` подключает общие CTest/tests без целей П6.

В PORT поверхность использует обычный `terrainType`/`terrainTile`: fog может подменить их сохранённым значением (`src/drawers/cMapDrawer.cpp@0a33444:230-253`), а именованные HD-варианты не выбираются. `cPlayer::setHouse` получает HouseColors и использует indexed-palette helper для обычных флагов, зданий и юнитов (`src/gameobjects/players/cPlayer.cpp@0a33444:157,273-316`); семь HouseColors заменяют palette slots 144–150 только для INDEX8 surfaces (`src/drawers/SDLDrawer.cpp@0a33444:420-433`). Интерфейс получает HouseColors в `src/drawers/cOrderDrawer.cpp@0a33444:41` и `src/drawers/cSideBarDrawer.cpp@0a33444:106,108,110`. True-colour текстура создаётся напрямую без palette tint (`SDLDrawer.cpp@0a33444:366-378`).

Команды `git log --oneline FORK1..PORT -- <группа путей>` и `git grep` для символов форка проверяли, что из P2–P4 уже есть. Вывод `git log` по группам составил: cMapDrawer — 40 строк, cStructureDrawer.cpp/.h — 68, relocated cPlayer.cpp/.h — 156, Graphics.cpp/.hpp — 12, cDataPack/cPack — 12, CMakeLists — 19. Существенные строки вывода: `5d60e18f Fogged cells draw the remembered terrain instead of the live terrain`; `5e34da81 Tile floor+ceil rendering eliminates black line gaps`; `87efa64f Connect world scale and HD assets to gameplay rendering`; `883f37f0 Fogged structures are drawn from memory instead of live`; `81e8c8ae Using colors from Houses not Palettes`; `d35f4afc Add configured flag to s_UnitInfo and guard setHouse loop`; `0c289327 Move createTextureFromIndexedSurfaceWithPalette to texture_utility`; `f3b41e2f Add world scale, HD unit sprite, windtrap flag, and frame density helpers`; `a84d768d Update cDataPack to SDL3 I/O and surface APIs`; `3f995a60 Replace SDL_RWops with SDL_IOStream in cPack`; `468b6889 Introduce Catch2 unit testing framework with MapGeometry tests`. Для отсутствующих `TerrainVariation.hpp` и `FactionTint.hpp` лог пустой. Ни одного вызова `getHouseTexture`/HM mask из FORK1 в PORT не перенесено.

### Переданные HD-метки и флаг

В FORK1 HD-метки зданий обрабатываются в `src/drawers/cStructureDrawer.cpp@9208dcf:346-359` (казарма), `:515-528` (силос), `:683-696` (завод Light Factory), `:768-781` (строительная площадка), `:473-486` (ветряк). Dispatch идёт из `:249-281`; `Graphics::getHouseTexture` ищет `HM_`/`HOUSEMASK_` на `src/utils/Graphics.cpp@9208dcf:295-308` и применяет маску на `:369-448`. Целевой цвет задаёт `minimapColor` владельца из `cPlayer.cpp@9208dcf:270-283`. В частности, `HM_BUILD_WINDTRAP_FLAG` — запись HD4 pack с индексом 172, но `drawHdWindTrapFlag` загружает `BUILD_WINDTRAP_FLAG`; маска для этого имени динамически образуется как `HM_BUILD_WINDTRAP_FLAG`.

В PORT alignment таблица подтверждает, что записи `HM_BUILD_LIGHTFACTORY_FLAG` (индекс 220), `HM_BUILD_SILO_FLAG` (181), `HM_BUILD_CONSTYARD_FLAG` (178), `HM_BUILD_BARRACKS_FLAG` (183) и `HM_BUILD_WINDTRAP_FLAG` (172) остались в HD4 pack manifest (`docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv@0a33444:222,181,180,185,174`). Код PORT их не запрашивает. `drawHdWindTrapFlag` в `src/drawers/cStructureDrawer.cpp@0a33444:289-297` загружает сырой `BUILD_WINDTRAP_FLAG`, рисует его в `:297`, а dispatch вызывает его в `:337` и затем fallback `structure->drawFlags()` в `:338`; owner/HouseColors и HM-маска не передаются. Поэтому PORT пока не назначает цвет Дома ни этим четырём меткам, ни флагу ветряка.

## 5. Тесты

`CMakeLists.txt@9208dcf:264-273,433-442` создаёт `terrain_variation_tests`/`faction_tint_tests` и регистрирует CTest `terrain_variation_selection`/`faction_tint_uniformity`. Оба исходника используют обычный `main()`, а не `TEST_CASE`: `git grep -n 'TEST_CASE' FORK1 -- tests/FactionTintTests.cpp tests/TerrainVariationTests.cpp` завершился кодом 1 без совпадений.

Команды подсчёта и вывод:

```sh
/srv/dune/venv/bin/python -c 'import re,subprocess; rev="9208dcf5a358f40afd95c99480e4e09f781ed566"; p="tests/FactionTintTests.cpp"; s=subprocess.check_output(["git","show",f"{rev}:{p}"],text=True); print("if_groups=",len(re.findall(r"^\s*if\s*\(",s,re.M))); print("comparison_expressions=",sum(s.count(op) for op in (" != "," == "," >= "," <= "," > "," < "))); print("applyFactionTintChannel_calls=",s.count("applyFactionTintChannel(")); print("TEST_CASE_occurrences=",s.count("TEST_CASE"))'
```

```text
if_groups= 3
comparison_expressions= 4
applyFactionTintChannel_calls= 5
TEST_CASE_occurrences= 0
```

```sh
/srv/dune/venv/bin/python -c 'import re,subprocess; rev="9208dcf5a358f40afd95c99480e4e09f781ed566"; p="tests/TerrainVariationTests.cpp"; s=subprocess.check_output(["git","show",f"{rev}:{p}"],text=True); print("assert_sites=",len(re.findall(r"\bassert\s*\(",s))); print("TEST_CASE_occurrences=",s.count("TEST_CASE")); print("assert_evaluations_if_assert_active=6+2*4096+5=",6+2*4096+5)'
```

```text
assert_sites= 9
TEST_CASE_occurrences= 0
assert_evaluations_if_assert_active=6+2*4096+5= 8203
```

В tint-тесте четыре сравнения сгруппированы в три `if`, тест вызывает `applyFactionTintChannel` пять раз. Terrain-тест содержит девять assert-sites: шесть до циклов, две проверки на каждой из 4096 ячеек и пять проверок наличия всех вариантов. Это статический подсчёт, а не прогон теста. Поиск `ifstream`, `fopen`, `SDL_RW`, `cDataPack`, `dataPack`, `resources/bin/data`, `.dat`, `.png` в обоих тестах совпадений не дал (код 1); тесты не читают паки или LFS-файлы. Используемые символы, заголовки и присутствие в PORT перечислены в `tests.tsv`.

## 6. Данные и записи паков

`data.tsv` перечисляет 6 базовых поверхностей, 24 именованных варианта поверхности, 37 записей `HM_*` и 5 строк динамических семейств/пак-файла. Имена базовых поверхностей — `TERRAIN_HILL`, `TERRAIN_MOUNTAIN`, `TERRAIN_ROCK`, `TERRAIN_SAND`, `TERRAIN_SPICE`, `TERRAIN_SPICEHILL`; в PORT их ожидаемые записи находятся в `tests/data/hd4_packs_expected.tsv@0a33444:265-271`. Команда `git show PORT:tests/data/hd4_packs_expected.tsv | rg -n 'TERRAIN_HILL|HM_BUILD_BARRACKS_FLAG|HM_BUILD_WINDTRAP_FLAG'` вывела, среди прочего:

```text
265:sdl_data_hd4.dat	118	TERRAIN_HILL	PNG	2048	128	ffa1dbbceb02e2c44e2852843fd9650e08836f18ade1af72f8b1fc93ca8426af	fork
319:sdl_data_hd4.dat	172	HM_BUILD_WINDTRAP_FLAG	PNG	256	2048	abe38211c037c5adf15c016db4000fa810a58170603bd495a5aff91cb0ea0361	fork
330:sdl_data_hd4.dat	183	HM_BUILD_BARRACKS_FLAG	PNG	256	2048	d40122160ae689a724bda889cae9eefbc715393c52c17572d4927ce0e854c5fe	fork
```

Точные индексы и команды поиска каждого имени приведены в `data.tsv`. Имена масок создаются динамически в `src/utils/Graphics.cpp@9208dcf:295-308`: `HM_<selectedName>`, `HOUSEMASK_<selectedName>`, затем fallback для `baseName`; для House-варианта имена строятся на `:268-282`. `git grep -n -E 'HM_[A-Z0-9_]+' FORK1 -- src` не нашёл литеральных констант `HM_*` в коде. Файлы-источники в FORK1: 48 `HM_HV_*`, 39 `HOUSEMASK_*`, 117 `HV_*`, 69 `HOUSEVARIANT_*`; эти семейства динамических вариантов не найдены в ожидаемом индексе PORT.

Для 67 конкретных PNG из `data.tsv` выполнялся `git cat-file -p FORK1:<путь> | head -n 1`; путь и первая строка печатались для каждого объекта. Сводный вывод: `source_PNGs_checked=67`, `unique_first_lines=['version https://git-lfs.github.com/spec/v1']`, `non_LFS=0`. Для HD4-пака команда `git cat-file -p FORK1:resources/bin/data/sdl_data_hd4.dat | head -n 1` и та же команда для PORT вывели `version https://git-lfs.github.com/spec/v1`.

Первая попытка LFS-сверки передала шаблон `HM_HV_*.png` как буквальный путь; команда вернула `fatal: path ... does not exist`. Повторная проверка исключила шаблоны и прошла по 67 конкретным PNG: пропущенных файлов и файлов без LFS не обнаружено. Автопроверка ссылок в таблицах данных вывела `references_checked=185`, `errors=[]`.

## 7. Цвета Домов

`house-colors.tsv` содержит восемь домов по четырём ревизиям (32 строки): общий дом, Харконнены, Атрейдесы, Ордосы, Меркенарии, Сардаукары, Фремены и Коррино. В BASE/FORK1 `resources/game.ini` задаёт `SWAPCOLOR` (старт индекса палитры) и `MINIMAPCOLOR` RGB. Маска FORK1 получает целевой RGB из `minimapColor`: `src/player/cPlayer.cpp@9208dcf:270-283` передаёт House-цвет в `getHouseTexture`, а `src/utils/Graphics.cpp@9208dcf:429-447` применяет его по luminance-маске. Поэтому цвет маски для Сардаукаров FORK1 — `(255,0,255)` (`resources/game.ini@9208dcf:18-19`); код FORK1 Дом Сардаукаров с цветом содержит.

В UP1/PORT `resources/game.ini` задаёт `MINIMAPCOLOR` и палитру `TEAMCOLOR_0..6`; значения всех семи оттенков даны по каждому дому в таблице. `src/gameobjects/players/cHousesInfo.cpp@d06f2fc:36-75` содержит соответствующие семь RGB-ступеней; в UP1 цвет Сардаукаров — `(101,12,101)` (`resources/game.ini@d06f2fc:70-77`), PORT сохраняет те же значения (`@0a33444:70-77`). Команды `git diff BASE FORK1 -- resources/game.ini` и `git diff UP1 PORT -- resources/game.ini` вывели пустой diff.

## Выборочная сверка помощников корневой нитью

По дорожке 1 проверены три факта следующими командами и выводами:

```text
git show FORK1:src/drawers/TerrainVariation.hpp | nl -ba | sed -n '1,75p'
8  inline constexpr int HD_TERRAIN_VARIANT_COUNT = 5;
10 inline bool supportsHdTerrainVariants(int terrainType)
25 inline int hdTerrainVariantIndex(int cellId, int terrainType)
39 return static_cast<int>(value % HD_TERRAIN_VARIANT_COUNT);
42 inline const char *hdTerrainVariantName(
```

```text
git show FORK1:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '212,285p'
248 bool drewHdHouseMarker = false;
249 drewHdHouseMarker = drawHdRefineryFlag(structure);
251 drewHdHouseMarker = drawHdSiloFlag(structure);
254 drewHdHouseMarker = drawHdWindTrapFlag(structure);
257 drewHdHouseMarker = drawHdConstYardFlag(structure);
260 drewHdHouseMarker = drawHdBarracksFlag(structure);
283 if (!drewHdHouseMarker) { structure->drawFlags(); }
```

```text
git grep -n -i -E 'tint|terrain|variation|house.?colou?r' FORK1 -- tools/normalize_faction_masks.py tools/check_unit_mask_uniformity.py tools/verify_building_flag_colors.py tools/verify_harvester_house_colors.py
```

Вывод содержал 15 строк: `normalize_faction_masks.py` — 4; `verify_building_flag_colors.py` — 7; `verify_harvester_house_colors.py` — 4; `check_unit_mask_uniformity.py` — совпадений нет. Имена функций и строки совпадают с `tools.tsv`.

По дорожке 2 независимо проверены PORT-отрисовка поверхности, подготовка House-текстур и RGB-массив апстрима:

```text
git show PORT:src/drawers/cMapDrawer.cpp | nl -ba | sed -n '230,260p'
230             // fogged cells show what was last seen, not what happens there now
231             int terrainType = cell->type;
235             if (isFoggedCell) {
236                 if (const s_RememberedTerrain *remembered = m_map->getRememberedTerrain(iCell, iPl)) {
237                     terrainType = remembered->type;
238                     terrainTile = remembered->tile;
244             // Draw terrain
251                 const cRectangle src_pos = {terrainTile * 32, 0,32, 32};
253                 m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(terrainType), src_pos, dest_pos);
```

```text
git show PORT:src/gameobjects/players/cPlayer.cpp | nl -ba | sed -n '258,326p'
273 minimapColor = m_HousesInfo->getMinimapColor(house);
277 bmp_flag = createPlayerTextureFromIndexedSurfaceWithPalette(...);
286 bmp_structure[i].reset(createPlayerTextureFromIndexedSurfaceWithPalette(...));
310 bmp_unit[i].reset(createPlayerTextureFromIndexedSurfaceWithPalette(...));
316 bmp_unit_top[i].reset(createPlayerTextureFromIndexedSurfaceWithPalette(...));
```

```text
git show UP1:src/gameobjects/players/cHousesInfo.cpp | nl -ba | sed -n '36,74p'
38     m_houseInfo[GENERALHOUSE].minimap_color = Color(128,128,128);
39     m_houseInfo[GENERALHOUSE].colors = {{{194, 194, 218}, {157, 157, 186}, {125, 125, 153},
43     m_houseInfo[HARKONNEN].minimap_color = Color(255,0,0);
44     m_houseInfo[HARKONNEN].colors = {{{214, 0, 0}, {182, 0, 0}, {153, 0, 0},
48     m_houseInfo[ATREIDES].minimap_color = Color(0,0,255);
49     m_houseInfo[ATREIDES].colors = {{{80, 121, 214}, {52, 85, 182}, {40, 60, 153},
53     m_houseInfo[ORDOS].minimap_color = Color(0,255,0);
54     m_houseInfo[ORDOS].colors = {{{76, 214, 76}, {56, 182, 56}, {36, 153, 36},
63     m_houseInfo[SARDAUKAR].minimap_color = Color(255,0,255);
64     m_houseInfo[SARDAUKAR].colors = {{{242, 105, 242}, {206, 72, 206}, {170, 48, 170},
```

По дорожке 3 независимо проверены регистрация CTest, тестовые проверки, индекс HD-маски и LFS-указатели:

```text
git show FORK1:CMakeLists.txt | nl -ba | sed -n '260,276p;430,444p'
265 terrain_variation_tests
273 add_test(NAME terrain_variation_selection COMMAND terrain_variation_tests)
434 faction_tint_tests
442 add_test(NAME faction_tint_uniformity COMMAND faction_tint_tests)
```

```text
git show FORK1:tests/TerrainVariationTests.cpp | nl -ba | sed -n '7,32p'
    assert(hdTerrainVariantIndex(-1, TERRAIN_SAND) == 0);
    assert(hdTerrainVariantIndex(42, TERRAIN_WALL) == 0);
    assert(hdTerrainVariantName(TERRAIN_SAND, 0, 0) == nullptr);
    assert(hdTerrainVariantName(TERRAIN_SAND, 0, 5) == nullptr);
    assert(hdTerrainVariantName(TERRAIN_SAND, 1, 3) == nullptr);
    std::array<bool, HD_TERRAIN_VARIANT_COUNT> seen = {};
    for (int cell = 0; cell < 4096; ++cell) {
        const int first = hdTerrainVariantIndex(cell, TERRAIN_SAND);
        const int second = hdTerrainVariantIndex(cell, TERRAIN_SAND);
        assert(first == second);
        assert(first >= 0 && first < HD_TERRAIN_VARIANT_COUNT);
        seen[first] = true;
    }
    for (bool present : seen) {
        assert(present);
    }
```

```text
git show PORT:tests/data/hd4_packs_expected.tsv | rg -n 'HM_BUILD_WINDTRAP_FLAG'
319:sdl_data_hd4.dat 172 HM_BUILD_WINDTRAP_FLAG PNG 256 2048 ... fork

git cat-file -p FORK1:resources/bin/data/sdl_data_hd4.dat | head -n 1
version https://git-lfs.github.com/spec/v1

git cat-file -p FORK1:resources/hd/master4/sdl_data/0118_TERRAIN_HILL.png | head -n 1
version https://git-lfs.github.com/spec/v1

git show FORK1:resources/game.ini | nl -ba | sed -n '17,20p'
18 SARDAUKAR_SWAPCOLOR = 208
19 SARDAUKAR_MINIMAPCOLOR = 255,0,255
```

## Таблицы

### 1. Сводка функций и изменений FORK1 (`fork.tsv`)

```text
путь	символ или участок diff	путь@9208dcf:строка	входы	выходы	места вызова
CMakeLists.txt	CTest и регистрации тестов tint/terrain	CMakeLists.txt@9208dcf:7,265,273,434,442	BUILD_TESTING; исходники двух тестов	цели terrain_variation_tests/faction_tint_tests и CTest tests terrain_variation_selection/faction_tint_uniformity	CMakeLists.txt@9208dcf:265,273,434,442
src/drawers/TerrainVariation.hpp	HD_TERRAIN_VARIANT_COUNT	src/drawers/TerrainVariation.hpp@9208dcf:8	нет	константа 5: индекс 0 — базовая поверхность, 1–4 соответствуют именованным вариантам	src/drawers/TerrainVariation.hpp@9208dcf:39; src/drawers/TerrainVariation.hpp@9208dcf:51
src/drawers/TerrainVariation.hpp	supportsHdTerrainVariants	src/drawers/TerrainVariation.hpp@9208dcf:10	terrainType	возвращает true для HILL, MOUNTAIN, ROCK, SAND, SPICE, SPICEHILL; иначе false	src/drawers/TerrainVariation.hpp@9208dcf:27
src/drawers/TerrainVariation.hpp	hdTerrainVariantIndex	src/drawers/TerrainVariation.hpp@9208dcf:25	cellId и terrainType	детерминированный индекс 0–4 через 32-битное смешивание; для отрицательной ячейки или неподдерживаемого типа 0	src/drawers/cMapDrawer.cpp@9208dcf:152; tests/TerrainVariationTests.cpp@9208dcf:9,10,23,24
src/drawers/TerrainVariation.hpp	hdTerrainVariantName	src/drawers/TerrainVariation.hpp@9208dcf:42	terrainType, tileIndex, variant	имя TERRAIN_<тип>_VAR_01..04 либо nullptr; вариант применяется только к tileIndex=0 и variant=1..4	src/drawers/cMapDrawer.cpp@9208dcf:154; tests/TerrainVariationTests.cpp@9208dcf:11,12,13,16
src/drawers/cMapDrawer.cpp	drawShroud: выбор кадра атласа	src/drawers/cMapDrawer.cpp@9208dcf:73,85	SHROUD и src_pos	изолированная текстура кадра, затем отрисовка полного кадра	cMapDrawer::drawShroud, вызовы src/drawers/cMapDrawer.cpp@9208dcf:74,86
src/drawers/cMapDrawer.cpp	drawTerrain: размеры ячейки, базовая поверхность и вариация	src/drawers/cMapDrawer.cpp@9208dcf:95,137,149,168	ячейка карты, ее тип/кадр/iCell, источник и прямоугольник назначения	базовый кадр; при наличии именованной HD-текстуры выбирается вариант; полный кадр поверхности рисуется renderStrechFullSprite	src/drawers/cMapDrawer.cpp@9208dcf:150; src/drawers/cMapDrawer.cpp@9208dcf:152; src/drawers/cMapDrawer.cpp@9208dcf:154; src/drawers/cMapDrawer.cpp@9208dcf:161
src/drawers/cStructureDrawer.h	Graphics member и новые HD-функции отрисовки	src/drawers/cStructureDrawer.h@9208dcf:31,37,38,39,40,41,42,43,44,45,46,47,48,49,50	GameContext передаёт Graphics в конструктор	объявлены 12 bool drawHd*Flag(structure), void drawHdBuildingFoundation(structure), void drawHarvesterOnRefineryPad(structure); поле m_gfxdata	src/drawers/cStructureDrawer.cpp@9208dcf:27; методы вызываются строками из drawStructureForLayer/drawStructuresForLayer/drawStructureAnimationRefinery
src/drawers/cStructureDrawer.cpp	drawStructureForLayer: fallback и выбор HD-флага	src/drawers/cStructureDrawer.cpp@9208dcf:212,241,249,283	структура и слой	последовательная попытка специальных HD-флагов; если подходящий HD-флаг не нарисован, вызывается structure->drawFlags(); обычная анимация фабрики дополняется drawUnitOnPad(src/drawers/cStructureDrawer.cpp@9208dcf:245)	src/drawers/cStructureDrawer.cpp@9208dcf:249; src/drawers/cStructureDrawer.cpp@9208dcf:251; src/drawers/cStructureDrawer.cpp@9208dcf:254; src/drawers/cStructureDrawer.cpp@9208dcf:257; src/drawers/cStructureDrawer.cpp@9208dcf:260; src/drawers/cStructureDrawer.cpp@9208dcf:263; src/drawers/cStructureDrawer.cpp@9208dcf:266; src/drawers/cStructureDrawer.cpp@9208dcf:269; src/drawers/cStructureDrawer.cpp@9208dcf:272; src/drawers/cStructureDrawer.cpp@9208dcf:275; src/drawers/cStructureDrawer.cpp@9208dcf:278; src/drawers/cStructureDrawer.cpp@9208dcf:281; src/drawers/cStructureDrawer.cpp@9208dcf:283
src/drawers/cStructureDrawer.cpp	drawHdRadarFlag, drawHdBarracksFlag, drawHdWorFlag, drawHdRefineryFlag	src/drawers/cStructureDrawer.cpp@9208dcf:304,346,388,430	указатель cAbstractStructure; в каждом методе проверяется конкретный тип сооружения и загружается одноимённая BUILD_*_FLAG поверхность	возвращает true только при успешном получении House-текстуры и отрисовке 8-фазного флага; иначе false; цель — visual rectangle структуры	src/drawers/cStructureDrawer.cpp@9208dcf:317,359,401,443; src/drawers/cStructureDrawer.cpp@9208dcf:249,260,263,266
src/drawers/cStructureDrawer.cpp	drawHdWindTrapFlag, drawHdSiloFlag, drawHdStarportFlag, drawHdPalaceFlag	src/drawers/cStructureDrawer.cpp@9208dcf:473,515,557,599	указатель cAbstractStructure; соответствующий WINDTRAP/SILO/STARPORT/PALACE и BUILD_*_FLAG поверхность	возвращает true при получении House-текстуры и отрисовке, иначе false; анимация флага берёт фазу из SDL_GetTicks	src/drawers/cStructureDrawer.cpp@9208dcf:486,528,570,612; src/drawers/cStructureDrawer.cpp@9208dcf:249,251,269,272
src/drawers/cStructureDrawer.cpp	drawHdIxFlag, drawHdLightFactoryFlag, drawHdHighTechFlag, drawHdConstYardFlag	src/drawers/cStructureDrawer.cpp@9208dcf:641,683,725,768	указатель cAbstractStructure; соответствующий тип и BUILD_*_FLAG поверхность	возвращает true при получении House-текстуры и отрисовке, иначе false	src/drawers/cStructureDrawer.cpp@9208dcf:654,696,738,781; src/drawers/cStructureDrawer.cpp@9208dcf:249,275,278,281,257
src/drawers/cStructureDrawer.cpp	drawHdBuildingFoundation	src/drawers/cStructureDrawer.cpp@9208dcf:810	cAbstractStructure*; ищет BUILDING_FOUNDATION_HD по имени	ничего не возвращает; при наличии текстуры отрисовывает основание в отдельном проходе	src/drawers/cStructureDrawer.cpp@9208dcf:969
src/drawers/cStructureDrawer.cpp	drawHarvesterOnRefineryPad	src/drawers/cStructureDrawer.cpp@9208dcf:846	cAbstractStructure*; его текущий юнит внутри	ничего не возвращает; рисует харвестер на площадке НПЗ	src/drawers/cStructureDrawer.cpp@9208dcf:208
src/drawers/cStructureDrawer.cpp	прочие изменённые участки HD-отрисовки	src/drawers/cStructureDrawer.cpp@9208dcf:201,899,915	структура, тип/состояние ремонта, UI-иконки	рендер НПЗ дополняется харвестером; размеры иконок ремонта берутся в логических пикселях	src/drawers/cStructureDrawer.cpp@9208dcf:901,902,923,924
src/player/cPlayer.h	HD-ссылки и состояние/интерфейс с изменениями в общем пути	src/player/cPlayer.h@9208dcf:63,438,494,546,569,570	outOfBuildDistance; canPlaceBuildingListItemAt; SaveGameManager friend; m_hdTextureReferences; предупреждение о враге	новые поля структуры/игрока; новый метод возвращает s_PlaceResult	вызов src/player/cPlayer.cpp@9208dcf:1518
src/player/cPlayer.cpp	destroyAllegroBitmaps и setHouse: House-текстуры юнитов/сооружений	src/player/cPlayer.cpp@9208dcf:70,252	дом игрока, индекс палитры замены, minimapColor, SDL_Surface каждого флага/сооружения/юнита/верхней части	при HD density вызывает Graphics::getHouseTexture, иначе indexed-palette путь; хранит HD кэшевые указатели без их локального освобождения; обнуляет указатели при смене дома	src/player/cPlayer.cpp@9208dcf:274,278; createHouseTexture lambda: src/player/cPlayer.cpp@9208dcf:276,290,293,303,315,325,331
src/player/cPlayer.cpp	createTextureFromIndexedSurfaceWithPalette (изменённая функция)	src/player/cPlayer.cpp@9208dcf:2418	SDL_Surface* и индекс прозрачности	Texture*; HD RGBA получает прямую конвертацию; INDEX8 сохраняет замену палитры, копирует построчно с учётом pitch	createTextureFromRgba lambda: src/player/cPlayer.cpp@9208dcf:2423,2454,2539; основной вызовов много в существующем коде
src/player/cPlayer.cpp	canPlaceBuildingListItemAt (новая функция в том же пути, не относится к tint)	src/player/cPlayer.cpp@9208dcf:2012	iCell и тип сооружения	s_PlaceResult с границами, terrain, занятостью и build distance; success также зависит от отсутствия блокировок	src/player/cPlayer.cpp@9208dcf:1518
src/player/cPlayer.cpp	другие diff-hunks общего пути: init, имена Домов, placeItem, уведомления, discovery, потери юнитов	src/player/cPlayer.cpp@9208dcf:198,727,1507,1559,1874,2092,2130	разные существующие входы	инициализация кулдауна, локализованные тексты, проверка размещения человека, звуковое предупреждение с 30-секундным кулдауном, обновлённые сообщения	новое размещение вызывает src/player/cPlayer.cpp@9208dcf:1518; изменённые остальные методы вызываются прежними игровыми точками
src/utils/FactionTint.hpp	FactionTintReferenceLuminance	src/utils/FactionTint.hpp@9208dcf:7	нет	константа 166.0F/255.0F применяется как опорная средняя яркость маски	src/utils/FactionTint.hpp@9208dcf:14; src/utils/Graphics.cpp@9208dcf:404
src/utils/FactionTint.hpp	applyFactionTintChannel	src/utils/FactionTint.hpp@9208dcf:9	target uint8, pixelLuminance, averageLuminance	округлённый и ограниченный до 0..255 целевой канал с поправкой на среднюю яркость	src/utils/Graphics.cpp@9208dcf:431; tests/FactionTintTests.cpp@9208dcf:7,8,14,15,21
src/utils/Graphics.hpp	новый API Graphics и кэш ключей House-текстур	src/utils/Graphics.hpp@9208dcf:23,38,41,42,46,55,56,59,60,62,70,86	assetDensity; имя/индекс ресурса; cRectangle; SDL_Surface, houseId, палитра и цвет	новые методы: findTexture, getFrameTexture, findFrameTexture, getHouseTexture, isValid, getDensity, getLogicalWidth/Height; HouseTexCacheKey(baseIndex,houseId,density), хэш и кэши	реализации/вызовы в src/utils/Graphics.cpp; callers приведены в строках следующих строк таблицы
src/utils/Graphics.cpp	конструктор, деструктор и getTexture	src/utils/Graphics.cpp@9208dcf:9,19,45	SDL_Renderer, путь к паку, assetDensity; индексы ресурса	плотность минимум 1; уничтожаются три кэша текстур; getTexture создаёт текстуру и выбирает Linear для HD, Nearest для density=1	src/utils/cDataPack.cpp@9208dcf:16; существующие вызовы Graphics::getTexture
src/utils/Graphics.cpp	findTexture	src/utils/Graphics.cpp@9208dcf:86	имя ресурса	Texture* или nullptr без поиска индекса, если имя отсутствует	src/drawers/cStructureDrawer.cpp@9208dcf:814; src/gameobjects/structures/cLightFactory.cpp@9208dcf:72
src/utils/Graphics.cpp	getFrameTexture	src/utils/Graphics.cpp@9208dcf:92	индекс и прямоугольник логического кадра	Texture* изолированного кадра, учитывающий плотность и кэшированный по индексу/прямоугольнику	src/drawers/cMapDrawer.cpp@9208dcf:74,86,150; src/utils/Graphics.cpp@9208dcf:188
src/utils/Graphics.cpp	findFrameTexture	src/utils/Graphics.cpp@9208dcf:183	имя и прямоугольник логического кадра	Texture* либо nullptr, если ресурс не найден	src/drawers/cMapDrawer.cpp@9208dcf:161
src/utils/Graphics.cpp	houseVariantPrefix и houseVariantCode	src/utils/Graphics.cpp@9208dcf:192,202	houseId	строковое имя и короткий код только для houseId 1/2/3 (Харконнен/Атрейдес/Ордос); иначе пустая строка	src/utils/Graphics.cpp@9208dcf:268,269
src/utils/Graphics.cpp	readPixel	src/utils/Graphics.cpp@9208dcf:212	SDL_Surface* и координаты x,y	Uint32 пиксель, прочитанный с учётом BytesPerPixel	src/utils/Graphics.cpp@9208dcf:385,414
src/utils/Graphics.cpp	getHouseTexture	src/utils/Graphics.cpp@9208dcf:226	reference surface, houseId, paletteSwapStart, Color houseColor, transparentIndex	кэшированный Texture*; выбирает HV_<код>_<имя> или HOUSEVARIANT_<дом>_<имя>, ищет HM_*/HOUSEMASK_* для выбранной/базовой картинки; сохраняет alpha и применяет яркостную маску к RGB	вызовы: src/player/cPlayer.cpp@9208dcf:278; src/drawers/cStructureDrawer.cpp@9208dcf:317,359,401,443,486,528,570,612,654,696,738,781; tests/UnitFrameFixture.cpp@9208dcf:296,305
src/utils/Graphics.cpp	getHouseTexture local tint lambda	src/utils/Graphics.cpp@9208dcf:429	strength, luminance, averageMaskedLuminance; original и target channel	смешанный байтовый канал	src/utils/Graphics.cpp@9208dcf:445,446,447
src/utils/Graphics.cpp	isValid; getLogicalWidth; getLogicalHeight	src/utils/Graphics.cpp@9208dcf:477,482,488	нет для isValid; индекс для логических размеров	bool; ширина/высота поверхности, делённая на density, либо 0 при отсутствии	tests/UnitFrameFixture.cpp@9208dcf:155; src/drawers/CreditsDrawer.cpp@9208dcf:40; src/drawers/cStructureDrawer.cpp@9208dcf:901,902,923,924; src/managers/cDrawManager.cpp@9208dcf:164,165
src/utils/Graphics.hpp	getDensity и HouseTexCacheKeyHash::operator==/operator()	src/utils/Graphics.hpp@9208dcf:56,62,70,71	нет для density; ключ базы/Дома/плотности для equality/hash	плотность int; bool/hash size_t; std::unordered_map использует их при find/insert houseTexCache; getDensity вызывается в src/drawers/cMessageDrawer.cpp@9208dcf:121,236, src/gameobjects/structures/cLightFactory.cpp@9208dcf:70, src/player/cPlayer.cpp@9208dcf:274	src/utils/Graphics.hpp@9208dcf:86; src/utils/Graphics.cpp@9208dcf:244,468
src/utils/cDataPack.hpp	новые индексы поверхностей и validity	src/utils/cDataPack.hpp@9208dcf:46,47,59,64	SDL_Surface* для обратного индекса; нет для isValid	методы getIndexFromSurface/getNameFromIndex/isValid; side-map surface→index	src/utils/Graphics.cpp@9208dcf:237; src/utils/cDataPack.cpp@9208dcf:42,48,127
src/utils/cDataPack.cpp	getIndexFromSurface и getNameFromIndex	src/utils/cDataPack.cpp@9208dcf:42,48	SDL_Surface* / index	int (-1 если не найден) / имя ресурса	src/utils/Graphics.cpp@9208dcf:237,250,295
src/utils/cDataPack.cpp	getSurface: index-map cache; isValid	src/utils/cDataPack.cpp@9208dcf:53,62,67,127	index или validity-запрос	SDL_Surface* и обратный индекс; bool из ReaderPack	src/utils/cDataPack.cpp@9208dcf:62; src/utils/Graphics.cpp@9208dcf:479
src/utils/cPack.h	ReaderPack::getNameFromIndex/isValid и valid	src/utils/cPack.h@9208dcf:34,42,55	index / нет	std::string или bool; valid по умолчанию false; структура ReaderPack хранит статус	src/utils/cPack.cpp@9208dcf:164; src/utils/cPack.h@9208dcf:42; src/utils/cDataPack.cpp@9208dcf:129
src/utils/cPack.cpp	ReaderPack ctor, getData, readDataIntoMemory, getNameFromIndex	src/utils/cPack.cpp@9208dcf:29,130,151,164	путь к паку / индекс / содержимое ресурса	проверяет корректность заголовка/объёма/числа записей и чтения; запрещает выдавать ресурс невалидного пакета; имя индекса или пустую строку	src/utils/cDataPack.cpp@9208dcf:62; src/utils/cDataPack.cpp@9208dcf:50
tests/FactionTintTests.cpp	новый main и вызовы applyFactionTintChannel	tests/FactionTintTests.cpp@9208dcf:1	нет	проверки яркости/сохранения теней/нулевого канала; return-код процесса	CMakeLists.txt@9208dcf:442
tests/TerrainVariationTests.cpp	новый main и вызовы TerrainVariation API	tests/TerrainVariationTests.cpp@9208dcf:1	нет	проверки границ, допустимых типов, детерминизма, строк вариантов; return-код процесса	CMakeLists.txt@9208dcf:273
CMakeLists.txt	прочие изменения конфигурации Apple в общем файле	CMakeLists.txt@9208dcf:62,64,69,109	настройки компилятора/линковщика и архитектуры Apple	удалены прежние compiler path/stdlib flags, условие архитектуры заменено условием CMake CXX compiler Clang	CMakeLists.txt@9208dcf:62,64,69,109
``` 

### 2. Инструменты (`tools.tsv`)

```text
путь	что делает	какие файлы читает	какие файлы пишет	кто вызывает
tools/normalize_faction_masks.py	Нормализует HD4 маски HM_*: непрозрачное внутреннее ядро и сглаженный край; готовит обзор до/после трёх цветов. При --install обновляет мастера и два пака.	По умолчанию resources/bin/data/sdl_data_hd4.dat; GAME_ROOT/data/sdl_data_hd4.dat для сравнения/копии; при --install мастера resources/hd/master4_extra_packs/sdl_data/HM_*.png и HOUSEMASK_*.png; через hd_assets.py pack entries и PNG payloads.	Всегда artifacts/faction_masks_uniform_v1/FACTION_MASKS_REVIEW.png и result.json; при --install обновлённые master PNG, resources/bin/data/sdl_data_hd4.dat, C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data\sdl_data_hd4.dat, резервные копии и временный *.uniform-masks.tmp.	Человек запускает напрямую через argparse --install/без флага; точка входа tools/normalize_faction_masks.py@9208dcf:212,251; упоминаний вызова из CMake или другого скрипта не найдено.
tools/check_unit_mask_uniformity.py	Проверяет, что сердцевина каждой HM_* маски белая и полностью непрозрачная, а сглаживание есть только по краю; печатает PASS/FAIL.	Путь позиционного pack аргумента, по умолчанию resources/bin/data/sdl_data_hd4.dat; hd_assets.py читает пак и декодирует PNG.	Файлы не пишет; печатает результат проверки.	Человек запускает напрямую; точка входа tools/check_unit_mask_uniformity.py@9208dcf:27,69; упоминаний вызова из CMake или другого скрипта не найдено.
tools/verify_building_flag_colors.py	Сверяет маршрутизацию специальных флагов в исходниках и наличие/цвет House-масок для шести типов зданий; отдельно проверяет два общих палитровых флага.	src/utils/cIniGameRessouces.cpp и src/drawers/cStructureDrawer.cpp@9208dcf:47,49,51,54,60,61,69,71; packs sdl_data_hd2.dat и sdl_data_hd4.dat в указанном каталоге, по умолчанию artifacts/silo_integration_v1/data; изображения декодирует hd_assets.py/Pillow.	Файлы не пишет; печатает маршрутизацию и результаты.	Человек запускает напрямую; точка входа tools/verify_building_flag_colors.py@9208dcf:191,212; в CMake/другом скрипте вызова не найдено.
tools/verify_harvester_house_colors.py	Разрешает вариант HV_* и маску HM_*/HOUSEMASK_* для заданного ресурса и трёх игровых Домов; вычисляет доминирование зелёного для Ордосов, чтобы найти красный вариант.	Обязательный --data-dir, два pack-файла HD2/HD4 и изображения из их payloads через hd_assets.py.	Файлы не пишет; печатает измерения цвета или ошибки.	Человек запускает напрямую с --data-dir и optional --resource; точка входа tools/verify_harvester_house_colors.py@9208dcf:114,116,138; в CMake/другом скрипте вызова не найдено.
``` 

### 3. Изменения апстрима (`upstream.tsv`)

```text
путь в UP1	участок	путь@d06f2fc:строка	что изменено одной строкой	пересекается ли с участком форка из пункта 1
CMakeLists.txt	тестовая интеграция	CMakeLists.txt@d06f2fc:95	Включены общие CTest и каталог tests; совпадающих целей faction_tint_tests, terrain_variation_tests и одноимённых проверок нет.	fork.tsv:2 — только уровень подключения тестовой инфраструктуры
src/drawers/cMapDrawer.cpp	отрисовка поверхности	src/drawers/cMapDrawer.cpp@d06f2fc:180,253	drawTerrainCells отделяет живые и затуманенные клетки, берёт тип и кадр из сохранённого террейна при тумане и рисует прямоугольник cell tile обычной текстурой; выбора именованного варианта нет.	fork.tsv:8
src/drawers/cStructureDrawer.cpp	отрисовка структур и сохранённого состояния	src/drawers/cStructureDrawer.cpp@d06f2fc:82,430	Добавлен drawRememberedStructures, использующий bitmap структуры её владельца при затуманивании; HD-функций drawHd*Flag и обращения к HM-маскам в UP1 нет.	fork.tsv:10 — общий проход структур; HD-флагов и масок нет
src/drawers/cStructureDrawer.h	интерфейс структуры drawer	src/drawers/cStructureDrawer.h@d06f2fc:41	Добавлен drawRememberedStructures; в заголовке UP1 не объявлены drawHd*Flag и drawHdBuildingFoundation.	нет
src/gameobjects/players/cPlayer.cpp	создание House-текстур и цвета интерфейса	src/gameobjects/players/cPlayer.cpp@d06f2fc:157,277,286,310	getColors берёт HouseColors владельца; setHouse создаёт текстуры флагов, зданий и юнитов через createPlayerTextureFromIndexedSurfaceWithPalette вместо fork-вызова getHouseTexture.	fork.tsv:18,19
src/gameobjects/players/cPlayer.h	доступ к цветам игрока	src/gameobjects/players/cPlayer.h@d06f2fc:571	Объявлен const HouseColors& getColors() для общего построителя текстур.	fork.tsv:17,18
src/utils/Graphics.cpp	общий кэш текстур	src/utils/Graphics.cpp@d06f2fc:43,68	getTexture ищет данные по индексу/имени и создаёт SDL-текстуру; реализации getHouseTexture, FactionTint и поиска HM/HOUSEMASK в UP1 нет.	fork.tsv:25
src/utils/Graphics.hpp	API Graphics	src/utils/Graphics.hpp@d06f2fc:21	Graphics сохраняет общий кэш getTexture; API getHouseTexture и HouseTexCacheKey отсутствует.	fork.tsv:24 — кэш Graphics; tint API отсутствует
src/utils/cDataPack.cpp	чтение изображений из пака	src/utils/cDataPack.cpp@d06f2fc:58	getSurface загружает поверхность по индексу и кеширует её; обратных getIndexFromSurface/getNameFromIndex в API UP1 нет.	fork.tsv:35,36,37 — getSurface общий; обратные индексы отсутствуют
src/utils/cDataPack.hpp	API DataPack	src/utils/cDataPack.hpp@d06f2fc:62	Оставлен getIndexFromName для ресурса; методов getIndexFromSurface и getNameFromIndex в заголовке нет.	fork.tsv:35
src/utils/cPack.cpp	чтение и запись пака	src/utils/cPack.cpp@d06f2fc:139	ReaderPack::getData возвращает SDL_IOStream; чтение/запись переведены с SDL_RWops на SDL3 IO, без кода раскраски.	fork.tsv:39 — общий getData; в API UP1 нет fork getNameFromIndex
src/utils/cPack.h	интерфейс ReaderPack	src/utils/cPack.h@d06f2fc:49	ReaderPack предоставляет индекс по имени и SDL_IOStream содержимого; getNameFromIndex/isValid из fork API нет.	fork.tsv:38,39 — общий ReaderPack/getData
src/drawers/SDLDrawer.cpp	поддерживающий путь: палитра	src/drawers/SDLDrawer.cpp@d06f2fc:344,387	createTextureFromIndexedSurfaceWithPalette получает семь HouseColors и записывает их в палитру с индексов 144–150; это палитровая перекраска, без пиксельной маски.	fork.tsv:18,19,31,32 — тот же путь подготовки House-текстур, отдельная реализация
src/utils/texture_utils.cpp	поддерживающий путь: обёртка House-текстур	src/utils/texture_utils.cpp@d06f2fc:20,24	createPlayerTextureFromIndexedSurfaceWithPalette передаёт player->getColors() в SDLDrawer.	fork.tsv:18,19
src/gameobjects/players/cHousesInfo.cpp	поддерживающий путь: данные цветов Домов	src/gameobjects/players/cHousesInfo.cpp@d06f2fc:36,42,63	В cHousesInfo заданы массивы из семи RGB-ступеней на Дом, а minimapColor хранится отдельно и может задаваться настройками.	fork.tsv:18 — fork передаёт minimapColor как один целевой RGB
src/utils/HouseColors.h	поддерживающий путь: тип палитры	src/utils/HouseColors.h@d06f2fc:21,25	HouseColor содержит RGB-байты, HouseColors — std::array из семи записей.	fork.tsv:18,19 — количество HouseColors совпадает с семью позициями замены
``` 

### 4. Состояние PORT (`port.tsv`)

```text
путь в PORT	что	путь@0a33444:строка	как устроено одной-двумя строками	соответствие в FORK1
CMakeLists.txt	проверки tint/terrain	CMakeLists.txt@0a33444:95,96	Подключаются общие CTest и каталог tests; целей faction_tint_tests и terrain_variation_tests и проверок faction_tint_uniformity/terrain_variation_selection нет.	CMakeLists.txt@9208dcf:265,434
src/drawers/TerrainVariation.hpp	нет в PORT			
src/drawers/cMapDrawer.cpp	поверхность	src/drawers/cMapDrawer.cpp@0a33444:230,244,251,253	Туманная клетка берёт сохранённые type/tile; далее источник — tile*32 из обычного атласа terrainType, без выбора hdTerrainVariantName или варианта.	src/drawers/cMapDrawer.cpp@9208dcf:150,152,154,161
src/drawers/cStructureDrawer.cpp	HD-метки Дома и флаг ветряка	src/drawers/cStructureDrawer.cpp@0a33444:289,293,297,337,338	В слое здания рисуется только отдельная BUILD_WINDTRAP_FLAG без передачи владельца или HouseColors; для других зданий вызывается structure->drawFlags(). Четыре указанные HM_*_FLAG в коде не читаются и не рисуются.	src/drawers/cStructureDrawer.cpp@9208dcf:249,251,257,260,278,281; House-текстуры: src/utils/Graphics.cpp@9208dcf:296,298,369,429,445
src/drawers/cStructureDrawer.h	объявление HD-флага	src/drawers/cStructureDrawer.h@0a33444:74	Есть drawHdWindTrapFlag; методов HD-флагов для LIGHTFACTORY, SILO, CONSTYARD и BARRACKS нет.	src/drawers/cStructureDrawer.h@9208dcf:37,40,45,47,49
src/gameobjects/players/cPlayer.cpp	цвет Дома для юнитов, зданий и интерфейса	src/gameobjects/players/cPlayer.cpp@0a33444:157,258,273,277,286,298,310,316,322	getColors возвращает HouseColors из cHousesInfo; setHouse передаёт их в palette helper для indexed-текстур флагов, структур и юнитов. Те же HouseColors применяются к BTN_ORDER и candy bar; minimap/emblem используют отдельные цвета. Источники вызовов: src/drawers/cOrderDrawer.cpp@0a33444:41, src/drawers/cSideBarDrawer.cpp@0a33444:106,108,110; данные палитры: src/gameobjects/players/cHousesInfo.cpp@0a33444:38,43,48,53,58,63,68,73.	src/player/cPlayer.cpp@9208dcf:267,278,288; HD маски передаются через getHouseTexture at src/utils/Graphics.cpp@9208dcf:296,298
src/gameobjects/players/cPlayer.h	цветовая палитра игрока	src/gameobjects/players/cPlayer.h@0a33444:31,571	getColors выдаёт массив семи HouseColor для palette helper; тип объявлен как RGB-байты в src/utils/HouseColors.h@0a33444:21,25.	src/player/cPlayer.h@9208dcf:492 — старый indexed-palette helper
src/drawers/SDLDrawer.cpp	поддерживающий путь цвета Дома	src/drawers/SDLDrawer.cpp@0a33444:366,370,378,420,422,426,433	Для поверхности без 8-битной палитры helper сразу создаёт текстуру из исходной поверхности; для INDEX8 копирует палитру и записывает до семи HouseColors в слоты 144–150.	src/utils/Graphics.cpp@9208dcf:317,369,429,443 — HD-ветка применяет HouseColor по HM-маске
src/utils/texture_utils.cpp	обёртка palette helper	src/utils/texture_utils.cpp@0a33444:20,24,26	createPlayerTextureFromIndexedSurfaceWithPalette передаёт player->getColors() в SDLDrawer.	src/player/cPlayer.cpp@9208dcf:252,278
src/utils/FactionTint.hpp	нет в PORT			
src/utils/Graphics.cpp	загрузка текстур по имени и индексу	src/utils/Graphics.cpp@0a33444:54,59,69,71	getTexture получает поверхность из DataPack и вызывает SDL_CreateTextureFromSurface; метода getHouseTexture и вычисления HM-маски в файле нет.	src/utils/Graphics.cpp@9208dcf:226,237,296,369
src/utils/Graphics.hpp	публичный API Graphics	src/utils/Graphics.hpp@0a33444:34,43,45,52	Есть getTexture и общий кэш; getHouseTexture и HouseTexCacheKey отсутствуют.	src/utils/Graphics.hpp@9208dcf:46,62,86
src/utils/cDataPack.cpp	доступ к поверхностям по имени и индексу	src/utils/cDataPack.cpp@0a33444:47,53,58,64,67,72	DataPack кеширует загруженные поверхности по индексу и находит ресурс по имени; обратного поиска surface→index и index→name нет.	src/utils/cDataPack.cpp@9208dcf:42,48,53
src/utils/cDataPack.hpp	API DataPack	src/utils/cDataPack.hpp@0a33444:58,60,62	Объявлен getIndexFromName; getIndexFromSurface и getNameFromIndex отсутствуют.	src/utils/cDataPack.hpp@9208dcf:45,46,47
src/utils/cPack.cpp	чтение содержимого пака	src/utils/cPack.cpp@0a33444:127,139,160	ReaderPack ищет имя по индексу и выдаёт SDL_IOStream для содержимого записи.	src/utils/cPack.cpp@9208dcf:130,164
src/utils/cPack.h	API ReaderPack	src/utils/cPack.h@0a33444:49	В ReaderPack есть поиск индекса по имени и getData; getNameFromIndex/isValid отсутствуют.	src/utils/cPack.h@9208dcf:33,35,42
tests/FactionTintTests.cpp	нет в PORT			
tests/TerrainVariationTests.cpp	нет в PORT			
docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv	HD-метка LIGHTFACTORY	docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv@0a33444:222	В таблице паков запись HM_BUILD_LIGHTFACTORY_FLAG имеет индекс 220; исходная HD-запись присутствует в данных, но код PORT её не запрашивает.	docs/upstream/port_inventory.json@9208dcf:1651,24813; src/drawers/cStructureDrawer.cpp@9208dcf:683,696; src/utils/Graphics.cpp@9208dcf:296,298
docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv	HD-метка SILO	docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv@0a33444:181	В таблице паков запись HM_BUILD_SILO_FLAG имеет индекс 181; код PORT её не запрашивает.	docs/upstream/port_inventory.json@9208dcf:1656,24883; src/drawers/cStructureDrawer.cpp@9208dcf:515,528; src/utils/Graphics.cpp@9208dcf:296,298
docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv	HD-метка CONSTYARD	docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv@0a33444:180	В таблице паков запись HM_BUILD_CONSTYARD_FLAG имеет индекс 178; код PORT её не запрашивает.	docs/upstream/port_inventory.json@9208dcf:1648,24771; src/drawers/cStructureDrawer.cpp@9208dcf:768,781; src/utils/Graphics.cpp@9208dcf:296,298
docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv	HD-метка BARRACKS	docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv@0a33444:185	В таблице паков запись HM_BUILD_BARRACKS_FLAG имеет индекс 183; код PORT её не запрашивает.	docs/upstream/port_inventory.json@9208dcf:1647,24757; src/drawers/cStructureDrawer.cpp@9208dcf:346,359; src/utils/Graphics.cpp@9208dcf:296,298
docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv	HD-метка WINDTRAP_FLAG	docs/upstream/p2/hd4_alignment_sdl_data_hd4.tsv@0a33444:174	В таблице паков запись HM_BUILD_WINDTRAP_FLAG имеет индекс 172; drawHdWindTrapFlag запрашивает BUILD_WINDTRAP_FLAG, поэтому HM_BUILD_WINDTRAP_FLAG не используется и HouseColor к флагу не назначается.	docs/upstream/port_inventory.json@9208dcf:1658,24911; src/drawers/cStructureDrawer.cpp@9208dcf:473,486; src/utils/Graphics.cpp@9208dcf:296,298
``` 

### 5. Тесты (`tests.tsv`)

```text
файл	TEST_CASE и путь@9208dcf:строка	что проверяет	число проверок	используемые символы и заголовки	есть ли каждый в PORT	чтение паков или Git LFS
tests/FactionTintTests.cpp	TEST_CASE отсутствует; main() at tests/FactionTintTests.cpp@9208dcf:5; CTest faction_tint_uniformity: CMakeLists.txt@9208dcf:442	Сравнивает результат тонирования тёмной и светлой исходной яркости; проверяет сохранение контраста теней и бликов; проверяет, что целевой канал 0 остаётся невидимым.	4 сравнения в 3 if-группах (строки 9, 16, 21), 5 вызовов applyFactionTintChannel; команда подсчёта и вывод приведены в RECON.md	src/utils/FactionTint.hpp@9208dcf:1 — отсутствует в PORT; src/utils/FactionTint.hpp@9208dcf:9; вызовы tests/FactionTintTests.cpp@9208dcf:7-21 — отсутствует в PORT; <iostream> и std::cerr: tests/FactionTintTests.cpp@9208dcf:3,10 — стандартная библиотека, соответствующих файлов проекта в PORT нет.	Тестовый файл, заголовок и функция отсутствуют в PORT; Git grep по функции и заголовку в PORT не дал совпадений (exit 1).	Нет; git grep по ifstream, fopen, SDL_RW, cDataPack, dataPack, resources/bin/data, .dat и .png не дал совпадений (exit 1).
tests/TerrainVariationTests.cpp	TEST_CASE отсутствует; main() at tests/TerrainVariationTests.cpp@9208dcf:7; CTest terrain_variation_selection: CMakeLists.txt@9208dcf:273	Проверяет возврат варианта 0 для отрицательной ячейки и неподдерживаемого типа, nullptr для недопустимых координат варианта, имя песочного варианта 3, детерминизм и покрытие всех пяти вариантов на 4096 ячейках.	9 assert-сайтов; 8203 вычисления assert при включённых assert: 6 до циклов + 2×4096 + 5; команда подсчёта и вывод приведены в RECON.md	src/drawers/TerrainVariation.hpp@9208dcf:1 — отсутствует в PORT; src/drawers/TerrainVariation.hpp@9208dcf:8,25,42 — отсутствуют в PORT; src/data/gfxdata.h@9208dcf:127,131 — в PORT src/data/gfxdata.h@0a33444:145,149; <array>, <cassert>, <cstring>, std::array, assert, std::strcmp: tests/TerrainVariationTests.cpp@9208dcf:3-5,21,29-30 — стандартная библиотека, соответствующих файлов проекта в PORT нет.	Тестовый файл, src/drawers/TerrainVariation.hpp и HD_TERRAIN_VARIANT_COUNT/hdTerrainVariantIndex/hdTerrainVariantName отсутствуют в PORT; TERRAIN_SAND и TERRAIN_WALL имеются по указанным строкам.	Нет; git grep по ifstream, fopen, SDL_RW, cDataPack, dataPack, resources/bin/data, .dat и .png не дал совпадений (exit 1).
``` 

### 6. Данные (`data.tsv`)

```text
имя	путь@9208dcf:строка объявления	пак или файл	есть ли в PORT	команда установления
TERRAIN_HILL	src/data/gfxdata.h@9208dcf:124	resources/hd/master4/sdl_data/0118_TERRAIN_HILL.png; resources/bin/data/sdl_data_hd4.dat[118]	есть; tests/data/hd4_packs_expected.tsv@0a33444:265	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_HILL'
TERRAIN_MOUNTAIN	src/data/gfxdata.h@9208dcf:125	resources/hd/master4/sdl_data/0119_TERRAIN_MOUNTAIN.png; resources/bin/data/sdl_data_hd4.dat[119]	есть; tests/data/hd4_packs_expected.tsv@0a33444:266	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_MOUNTAIN'
TERRAIN_ROCK	src/data/gfxdata.h@9208dcf:126	resources/hd/master4/sdl_data/0120_TERRAIN_ROCK.png; resources/bin/data/sdl_data_hd4.dat[120]	есть; tests/data/hd4_packs_expected.tsv@0a33444:267	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_ROCK'
TERRAIN_SAND	src/data/gfxdata.h@9208dcf:127	resources/hd/master4/sdl_data/0121_TERRAIN_SAND.png; resources/bin/data/sdl_data_hd4.dat[121]	есть; tests/data/hd4_packs_expected.tsv@0a33444:268	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SAND'
TERRAIN_SPICE	src/data/gfxdata.h@9208dcf:129	resources/hd/master4/sdl_data/0123_TERRAIN_SPICE.png; resources/bin/data/sdl_data_hd4.dat[123]	есть; tests/data/hd4_packs_expected.tsv@0a33444:270	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICE'
TERRAIN_SPICEHILL	src/data/gfxdata.h@9208dcf:130	resources/hd/master4/sdl_data/0124_TERRAIN_SPICEHILL.png; resources/bin/data/sdl_data_hd4.dat[124]	есть; tests/data/hd4_packs_expected.tsv@0a33444:271	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICEHILL'
HM_UNIT_HARVESTER	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_HARVESTER.png; resources/bin/data/sdl_data_hd4.dat[168]	есть; tests/data/hd4_packs_expected.tsv@0a33444:315	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_HARVESTER'
HM_UNIT_SOLDIERS	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_SOLDIERS.png; resources/bin/data/sdl_data_hd4.dat[169]	есть; tests/data/hd4_packs_expected.tsv@0a33444:316	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_SOLDIERS'
HM_UNIT_SOLDIER	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_SOLDIER.png; resources/bin/data/sdl_data_hd4.dat[170]	есть; tests/data/hd4_packs_expected.tsv@0a33444:317	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_SOLDIER'
HM_BUILD_WINDTRAP_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_WINDTRAP_FLAG.png; resources/bin/data/sdl_data_hd4.dat[172]	есть; tests/data/hd4_packs_expected.tsv@0a33444:319	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_WINDTRAP_FLAG'
HM_BUILD_REFINERY_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_REFINERY_FLAG.png; resources/bin/data/sdl_data_hd4.dat[174]	есть; tests/data/hd4_packs_expected.tsv@0a33444:321	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_REFINERY_FLAG'
HM_UNIT_TANKBASE	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_TANKBASE.png; resources/bin/data/sdl_data_hd4.dat[175]	есть; tests/data/hd4_packs_expected.tsv@0a33444:322	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_TANKBASE'
HM_UNIT_TANKTOP	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_TANKTOP.png; resources/bin/data/sdl_data_hd4.dat[176]	есть; tests/data/hd4_packs_expected.tsv@0a33444:323	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_TANKTOP'
HM_BUILD_CONSTYARD_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_CONSTYARD_FLAG.png; resources/bin/data/sdl_data_hd4.dat[178]	есть; tests/data/hd4_packs_expected.tsv@0a33444:325	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_CONSTYARD_FLAG'
HM_UNIT_LAUNCHER	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_LAUNCHER.png; resources/bin/data/sdl_data_hd4.dat[179]	есть; tests/data/hd4_packs_expected.tsv@0a33444:326	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_LAUNCHER'
HM_BUILD_SILO_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_SILO_FLAG.png; resources/bin/data/sdl_data_hd4.dat[181]	есть; tests/data/hd4_packs_expected.tsv@0a33444:328	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_SILO_FLAG'
HM_BUILD_BARRACKS_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_BARRACKS_FLAG.png; resources/bin/data/sdl_data_hd4.dat[183]	есть; tests/data/hd4_packs_expected.tsv@0a33444:330	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_BARRACKS_FLAG'
HM_BUILD_RADAR_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_RADAR_FLAG.png; resources/bin/data/sdl_data_hd4.dat[185]	есть; tests/data/hd4_packs_expected.tsv@0a33444:332	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_RADAR_FLAG'
TERRAIN_HILL_VAR_01	src/drawers/TerrainVariation.hpp@9208dcf:56	resources/hd/master4_extra_packs/sdl_data/TERRAIN_HILL_VAR_01.png; resources/bin/data/sdl_data_hd4.dat[186]	есть; tests/data/hd4_packs_expected.tsv@0a33444:333	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_HILL_VAR_01'
TERRAIN_HILL_VAR_02	src/drawers/TerrainVariation.hpp@9208dcf:57	resources/hd/master4_extra_packs/sdl_data/TERRAIN_HILL_VAR_02.png; resources/bin/data/sdl_data_hd4.dat[187]	есть; tests/data/hd4_packs_expected.tsv@0a33444:334	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_HILL_VAR_02'
TERRAIN_HILL_VAR_03	src/drawers/TerrainVariation.hpp@9208dcf:58	resources/hd/master4_extra_packs/sdl_data/TERRAIN_HILL_VAR_03.png; resources/bin/data/sdl_data_hd4.dat[188]	есть; tests/data/hd4_packs_expected.tsv@0a33444:335	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_HILL_VAR_03'
TERRAIN_HILL_VAR_04	src/drawers/TerrainVariation.hpp@9208dcf:59	resources/hd/master4_extra_packs/sdl_data/TERRAIN_HILL_VAR_04.png; resources/bin/data/sdl_data_hd4.dat[189]	есть; tests/data/hd4_packs_expected.tsv@0a33444:336	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_HILL_VAR_04'
TERRAIN_MOUNTAIN_VAR_01	src/drawers/TerrainVariation.hpp@9208dcf:62	resources/hd/master4_extra_packs/sdl_data/TERRAIN_MOUNTAIN_VAR_01.png; resources/bin/data/sdl_data_hd4.dat[190]	есть; tests/data/hd4_packs_expected.tsv@0a33444:337	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_MOUNTAIN_VAR_01'
TERRAIN_MOUNTAIN_VAR_02	src/drawers/TerrainVariation.hpp@9208dcf:63	resources/hd/master4_extra_packs/sdl_data/TERRAIN_MOUNTAIN_VAR_02.png; resources/bin/data/sdl_data_hd4.dat[191]	есть; tests/data/hd4_packs_expected.tsv@0a33444:338	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_MOUNTAIN_VAR_02'
TERRAIN_MOUNTAIN_VAR_03	src/drawers/TerrainVariation.hpp@9208dcf:64	resources/hd/master4_extra_packs/sdl_data/TERRAIN_MOUNTAIN_VAR_03.png; resources/bin/data/sdl_data_hd4.dat[192]	есть; tests/data/hd4_packs_expected.tsv@0a33444:339	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_MOUNTAIN_VAR_03'
TERRAIN_MOUNTAIN_VAR_04	src/drawers/TerrainVariation.hpp@9208dcf:65	resources/hd/master4_extra_packs/sdl_data/TERRAIN_MOUNTAIN_VAR_04.png; resources/bin/data/sdl_data_hd4.dat[193]	есть; tests/data/hd4_packs_expected.tsv@0a33444:340	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_MOUNTAIN_VAR_04'
TERRAIN_ROCK_VAR_01	src/drawers/TerrainVariation.hpp@9208dcf:68	resources/hd/master4_extra_packs/sdl_data/TERRAIN_ROCK_VAR_01.png; resources/bin/data/sdl_data_hd4.dat[194]	есть; tests/data/hd4_packs_expected.tsv@0a33444:341	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_ROCK_VAR_01'
TERRAIN_ROCK_VAR_02	src/drawers/TerrainVariation.hpp@9208dcf:69	resources/hd/master4_extra_packs/sdl_data/TERRAIN_ROCK_VAR_02.png; resources/bin/data/sdl_data_hd4.dat[195]	есть; tests/data/hd4_packs_expected.tsv@0a33444:342	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_ROCK_VAR_02'
TERRAIN_ROCK_VAR_03	src/drawers/TerrainVariation.hpp@9208dcf:70	resources/hd/master4_extra_packs/sdl_data/TERRAIN_ROCK_VAR_03.png; resources/bin/data/sdl_data_hd4.dat[196]	есть; tests/data/hd4_packs_expected.tsv@0a33444:343	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_ROCK_VAR_03'
TERRAIN_ROCK_VAR_04	src/drawers/TerrainVariation.hpp@9208dcf:71	resources/hd/master4_extra_packs/sdl_data/TERRAIN_ROCK_VAR_04.png; resources/bin/data/sdl_data_hd4.dat[197]	есть; tests/data/hd4_packs_expected.tsv@0a33444:344	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_ROCK_VAR_04'
TERRAIN_SAND_VAR_01	src/drawers/TerrainVariation.hpp@9208dcf:74	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SAND_VAR_01.png; resources/bin/data/sdl_data_hd4.dat[198]	есть; tests/data/hd4_packs_expected.tsv@0a33444:345	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SAND_VAR_01'
TERRAIN_SAND_VAR_02	src/drawers/TerrainVariation.hpp@9208dcf:75	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SAND_VAR_02.png; resources/bin/data/sdl_data_hd4.dat[199]	есть; tests/data/hd4_packs_expected.tsv@0a33444:346	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SAND_VAR_02'
TERRAIN_SAND_VAR_03	src/drawers/TerrainVariation.hpp@9208dcf:76	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SAND_VAR_03.png; resources/bin/data/sdl_data_hd4.dat[200]	есть; tests/data/hd4_packs_expected.tsv@0a33444:347	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SAND_VAR_03'
TERRAIN_SAND_VAR_04	src/drawers/TerrainVariation.hpp@9208dcf:77	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SAND_VAR_04.png; resources/bin/data/sdl_data_hd4.dat[201]	есть; tests/data/hd4_packs_expected.tsv@0a33444:348	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SAND_VAR_04'
TERRAIN_SPICE_VAR_01	src/drawers/TerrainVariation.hpp@9208dcf:80	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICE_VAR_01.png; resources/bin/data/sdl_data_hd4.dat[202]	есть; tests/data/hd4_packs_expected.tsv@0a33444:349	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICE_VAR_01'
TERRAIN_SPICE_VAR_02	src/drawers/TerrainVariation.hpp@9208dcf:81	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICE_VAR_02.png; resources/bin/data/sdl_data_hd4.dat[203]	есть; tests/data/hd4_packs_expected.tsv@0a33444:350	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICE_VAR_02'
TERRAIN_SPICE_VAR_03	src/drawers/TerrainVariation.hpp@9208dcf:82	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICE_VAR_03.png; resources/bin/data/sdl_data_hd4.dat[204]	есть; tests/data/hd4_packs_expected.tsv@0a33444:351	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICE_VAR_03'
TERRAIN_SPICE_VAR_04	src/drawers/TerrainVariation.hpp@9208dcf:83	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICE_VAR_04.png; resources/bin/data/sdl_data_hd4.dat[205]	есть; tests/data/hd4_packs_expected.tsv@0a33444:352	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICE_VAR_04'
TERRAIN_SPICEHILL_VAR_01	src/drawers/TerrainVariation.hpp@9208dcf:86	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICEHILL_VAR_01.png; resources/bin/data/sdl_data_hd4.dat[206]	есть; tests/data/hd4_packs_expected.tsv@0a33444:353	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICEHILL_VAR_01'
TERRAIN_SPICEHILL_VAR_02	src/drawers/TerrainVariation.hpp@9208dcf:87	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICEHILL_VAR_02.png; resources/bin/data/sdl_data_hd4.dat[207]	есть; tests/data/hd4_packs_expected.tsv@0a33444:354	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICEHILL_VAR_02'
TERRAIN_SPICEHILL_VAR_03	src/drawers/TerrainVariation.hpp@9208dcf:88	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICEHILL_VAR_03.png; resources/bin/data/sdl_data_hd4.dat[208]	есть; tests/data/hd4_packs_expected.tsv@0a33444:355	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICEHILL_VAR_03'
TERRAIN_SPICEHILL_VAR_04	src/drawers/TerrainVariation.hpp@9208dcf:89	resources/hd/master4_extra_packs/sdl_data/TERRAIN_SPICEHILL_VAR_04.png; resources/bin/data/sdl_data_hd4.dat[209]	есть; tests/data/hd4_packs_expected.tsv@0a33444:356	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'TERRAIN_SPICEHILL_VAR_04'
HM_BUILD_STARPORT_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_STARPORT_FLAG.png; resources/bin/data/sdl_data_hd4.dat[211]	есть; tests/data/hd4_packs_expected.tsv@0a33444:358	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_STARPORT_FLAG'
HM_UNIT_DEVASTATOR	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_DEVASTATOR.png; resources/bin/data/sdl_data_hd4.dat[212]	есть; tests/data/hd4_packs_expected.tsv@0a33444:359	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_DEVASTATOR'
HM_UNIT_SIEGEBASE	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_SIEGEBASE.png; resources/bin/data/sdl_data_hd4.dat[213]	есть; tests/data/hd4_packs_expected.tsv@0a33444:360	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_SIEGEBASE'
HM_UNIT_SIEGETOP	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_SIEGETOP.png; resources/bin/data/sdl_data_hd4.dat[214]	есть; tests/data/hd4_packs_expected.tsv@0a33444:361	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_SIEGETOP'
HM_BUILD_PALACE_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_PALACE_FLAG.png; resources/bin/data/sdl_data_hd4.dat[216]	есть; tests/data/hd4_packs_expected.tsv@0a33444:363	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_PALACE_FLAG'
HM_BUILD_IX_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_IX_FLAG.png; resources/bin/data/sdl_data_hd4.dat[218]	есть; tests/data/hd4_packs_expected.tsv@0a33444:365	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_IX_FLAG'
HM_BUILD_LIGHTFACTORY_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_LIGHTFACTORY_FLAG.png; resources/bin/data/sdl_data_hd4.dat[220]	есть; tests/data/hd4_packs_expected.tsv@0a33444:367	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_LIGHTFACTORY_FLAG'
HM_UNIT_ORNITHOPTER	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_ORNITHOPTER.png; resources/bin/data/sdl_data_hd4.dat[221]	есть; tests/data/hd4_packs_expected.tsv@0a33444:368	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_ORNITHOPTER'
HM_BUILD_WOR_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_WOR_FLAG.png; resources/bin/data/sdl_data_hd4.dat[223]	есть; tests/data/hd4_packs_expected.tsv@0a33444:370	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_WOR_FLAG'
HM_UNIT_SABOTEUR	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_SABOTEUR.png; resources/bin/data/sdl_data_hd4.dat[224]	есть; tests/data/hd4_packs_expected.tsv@0a33444:371	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_SABOTEUR'
HM_BUILD_HIGHTECH_FLAG	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_HIGHTECH_FLAG.png; resources/bin/data/sdl_data_hd4.dat[226]	есть; tests/data/hd4_packs_expected.tsv@0a33444:373	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_HIGHTECH_FLAG'
HM_UNIT_TROOPER	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_TROOPER.png; resources/bin/data/sdl_data_hd4.dat[227]	есть; tests/data/hd4_packs_expected.tsv@0a33444:374	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_TROOPER'
HM_UNIT_TRIKE	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_TRIKE.png; resources/bin/data/sdl_data_hd4.dat[228]	есть; tests/data/hd4_packs_expected.tsv@0a33444:375	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_TRIKE'
HM_UNIT_MCV	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_MCV.png; resources/bin/data/sdl_data_hd4.dat[229]	есть; tests/data/hd4_packs_expected.tsv@0a33444:376	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_MCV'
HM_UNIT_CARRYALL	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_CARRYALL.png; resources/bin/data/sdl_data_hd4.dat[230]	есть; tests/data/hd4_packs_expected.tsv@0a33444:377	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_CARRYALL'
HM_UNIT_SINGLEFREMEN	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_SINGLEFREMEN.png; resources/bin/data/sdl_data_hd4.dat[231]	есть; tests/data/hd4_packs_expected.tsv@0a33444:378	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_SINGLEFREMEN'
HM_UNIT_TRIPLEFREMEN	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_TRIPLEFREMEN.png; resources/bin/data/sdl_data_hd4.dat[232]	есть; tests/data/hd4_packs_expected.tsv@0a33444:379	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_TRIPLEFREMEN'
HM_UNIT_TROOPERS	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_TROOPERS.png; resources/bin/data/sdl_data_hd4.dat[233]	есть; tests/data/hd4_packs_expected.tsv@0a33444:380	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_TROOPERS'
HM_UNIT_RAIDER	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_RAIDER.png; resources/bin/data/sdl_data_hd4.dat[234]	есть; tests/data/hd4_packs_expected.tsv@0a33444:381	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_RAIDER'
HM_UNIT_DEVIATOR	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_DEVIATOR.png; resources/bin/data/sdl_data_hd4.dat[235]	есть; tests/data/hd4_packs_expected.tsv@0a33444:382	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_DEVIATOR'
HM_UNIT_SONICTANK	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_SONICTANK.png; resources/bin/data/sdl_data_hd4.dat[236]	есть; tests/data/hd4_packs_expected.tsv@0a33444:383	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_SONICTANK'
HM_UNIT_QUAD	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_UNIT_QUAD.png; resources/bin/data/sdl_data_hd4.dat[237]	есть; tests/data/hd4_packs_expected.tsv@0a33444:384	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_UNIT_QUAD'
HM_BUILDING_FLAG_LARGE	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILDING_FLAG_LARGE.png; resources/bin/data/sdl_data_hd4.dat[238]	есть; tests/data/hd4_packs_expected.tsv@0a33444:385	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILDING_FLAG_LARGE'
HM_BUILDING_FLAG_SMALL	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILDING_FLAG_SMALL.png; resources/bin/data/sdl_data_hd4.dat[239]	есть; tests/data/hd4_packs_expected.tsv@0a33444:386	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILDING_FLAG_SMALL'
HM_BUILD_REFINERY	src/utils/Graphics.cpp@9208dcf:298 (шаблон HM_<selectedName>)	resources/hd/master4_extra_packs/sdl_data/HM_BUILD_REFINERY.png; resources/bin/data/sdl_data_hd4.dat[241]	есть; tests/data/hd4_packs_expected.tsv@0a33444:388	git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_BUILD_REFINERY'
HM_HV_<houseCode>_<baseName> (48 PNG исходников)	src/utils/Graphics.cpp@9208dcf:298,304	resources/hd/master4_extra_packs/sdl_data/HM_HV_*.png	в PORT ожидаемой таблицей записей не найдено	git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/hd/master4_extra_packs/sdl_data | rg '/HM_HV_' | wc -l → 48; git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HM_HV_' → нет совпадений
HOUSEMASK_<selectedName/baseName> (39 PNG исходников)	src/utils/Graphics.cpp@9208dcf:301,307	resources/hd/master4_extra_packs/sdl_data/HOUSEMASK_*.png	в PORT ожидаемой таблицей записей не найдено	git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/hd/master4_extra_packs/sdl_data | rg '/HOUSEMASK_' | wc -l → 39; git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HOUSEMASK_' → нет совпадений
HV_<houseCode>_<baseName> (117 PNG исходников)	src/utils/Graphics.cpp@9208dcf:272,278	resources/hd/master4_extra_packs/sdl_data/HV_*.png	в PORT ожидаемой таблицей записей не найдено	git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/hd/master4_extra_packs/sdl_data | rg '/HV_' | wc -l → 117; git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HV_|HOUSEVARIANT_' → нет совпадений
HOUSEVARIANT_<houseName>_<baseName> (69 PNG исходников)	src/utils/Graphics.cpp@9208dcf:275,282	resources/hd/master4_extra_packs/sdl_data/HOUSEVARIANT_*.png	в PORT ожидаемой таблицей записей не найдено	git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/hd/master4_extra_packs/sdl_data | rg '/HOUSEVARIANT_' | wc -l → 69; git show 0a33444e9032ef935dfe4cdde6bb622771484230:tests/data/hd4_packs_expected.tsv | rg 'HV_|HOUSEVARIANT_' → нет совпадений
resources/bin/data/sdl_data_hd4.dat	src/cGame_logic.cpp@9208dcf:124-125	Git LFS pack; lookup именовых записей ведётся через dataPack	есть; resources/bin/data/sdl_data_hd4.dat@0a33444 (в нём перечислены записи tests/data/hd4_packs_expected.tsv@0a33444:265-388)	git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/sdl_data_hd4.dat | head -n1 → version https://git-lfs.github.com/spec/v1
``` 

### 7. Цвета Домов (`house-colors.tsv`)

```text
Дом	ревизия	путь@ревизия:строка	способ задания	значение
Общий (GENERAL)	e17379a	resources/game.ini@e17379a:7-8	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=128; MINIMAPCOLOR=(128,128,128)
Харконнены	e17379a	resources/game.ini@e17379a:10-11	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=-1; MINIMAPCOLOR=(255,0,0)
Атрейдесы	e17379a	resources/game.ini@e17379a:12-13	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=160; MINIMAPCOLOR=(0,0,255)
Ордосы	e17379a	resources/game.ini@e17379a:14-15	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=176; MINIMAPCOLOR=(0,255,0)
Меркенарии	e17379a	resources/game.ini@e17379a:16-17	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=192; MINIMAPCOLOR=(214,121,16)
Сардаукары	e17379a	resources/game.ini@e17379a:18-19	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=208; MINIMAPCOLOR=(255,0,255)
Фремены	e17379a	resources/game.ini@e17379a:21-22	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=224; MINIMAPCOLOR=(194,125,60)
Коррино	e17379a	resources/game.ini@e17379a:23-24	Индекс начала замены палитры и RGB minimap; в FORK1 RGB передаётся маске как целевой цвет	SWAPCOLOR=136; MINIMAPCOLOR=(192,192,192)
Общий (GENERAL)	9208dcf	resources/game.ini@9208dcf:7-8	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=128; MINIMAPCOLOR=(128,128,128)
Харконнены	9208dcf	resources/game.ini@9208dcf:10-11	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=-1; MINIMAPCOLOR=(255,0,0)
Атрейдесы	9208dcf	resources/game.ini@9208dcf:12-13	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=160; MINIMAPCOLOR=(0,0,255)
Ордосы	9208dcf	resources/game.ini@9208dcf:14-15	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=176; MINIMAPCOLOR=(0,255,0)
Меркенарии	9208dcf	resources/game.ini@9208dcf:16-17	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=192; MINIMAPCOLOR=(214,121,16)
Сардаукары	9208dcf	resources/game.ini@9208dcf:18-19	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=208; MINIMAPCOLOR=(255,0,255)
Фремены	9208dcf	resources/game.ini@9208dcf:21-22	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=224; MINIMAPCOLOR=(194,125,60)
Коррино	9208dcf	resources/game.ini@9208dcf:23-24	Индекс начала замены палитры и RGB minimap; HD-маске передаётся RGB minimap	SWAPCOLOR=136; MINIMAPCOLOR=(192,192,192)
Общий (GENERAL)	d06f2fc	resources/game.ini@d06f2fc:20-27	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(128,128,128); TEAMCOLOR_0..6=[(194,194,218),(157,157,186),(125,125,153),(93,93,121),(64,64,89),(40,40,60),(20,20,40)]
Харконнены	d06f2fc	resources/game.ini@d06f2fc:30-37	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(255,0,0); TEAMCOLOR_0..6=[(214,0,0),(182,0,0),(153,0,0),(125,0,0),(89,0,0),(60,0,0),(32,0,0)]
Атрейдесы	d06f2fc	resources/game.ini@d06f2fc:40-47	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(0,0,255); TEAMCOLOR_0..6=[(80,121,214),(52,85,182),(40,60,153),(24,32,125),(8,12,89),(4,4,60),(0,0,32)]
Ордосы	d06f2fc	resources/game.ini@d06f2fc:50-57	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(0,255,0); TEAMCOLOR_0..6=[(76,214,76),(56,182,56),(36,153,36),(24,125,24),(12,89,12),(4,60,4),(0,32,0)]
Меркенарии	d06f2fc	resources/game.ini@d06f2fc:60-67	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(214,121,16); TEAMCOLOR_0..6=[(214,121,16),(182,97,8),(153,76,4),(121,60,4),(93,40,0),(60,24,0),(32,12,0)]
Сардаукары	d06f2fc	resources/game.ini@d06f2fc:70-77	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(101,12,101); TEAMCOLOR_0..6=[(242,105,242),(206,72,206),(170,48,170),(137,24,137),(101,12,101),(64,0,64),(32,0,32)]
Фремены	d06f2fc	resources/game.ini@d06f2fc:81-88	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(194,125,60); TEAMCOLOR_0..6=[(214,149,0),(182,125,0),(153,105,0),(125,80,0),(89,56,0),(60,36,0),(32,16,0)]
Коррино	d06f2fc	resources/game.ini@d06f2fc:91-98	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(192,192,192); TEAMCOLOR_0..6=[(226,182,149),(202,161,133),(178,141,117),(153,121,101),(129,101,85),(105,80,68),(80,60,52)]
Общий (GENERAL)	0a33444	resources/game.ini@0a33444:20-27	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(128,128,128); TEAMCOLOR_0..6=[(194,194,218),(157,157,186),(125,125,153),(93,93,121),(64,64,89),(40,40,60),(20,20,40)]
Харконнены	0a33444	resources/game.ini@0a33444:30-37	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(255,0,0); TEAMCOLOR_0..6=[(214,0,0),(182,0,0),(153,0,0),(125,0,0),(89,0,0),(60,0,0),(32,0,0)]
Атрейдесы	0a33444	resources/game.ini@0a33444:40-47	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(0,0,255); TEAMCOLOR_0..6=[(80,121,214),(52,85,182),(40,60,153),(24,32,125),(8,12,89),(4,4,60),(0,0,32)]
Ордосы	0a33444	resources/game.ini@0a33444:50-57	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(0,255,0); TEAMCOLOR_0..6=[(76,214,76),(56,182,56),(36,153,36),(24,125,24),(12,89,12),(4,60,4),(0,32,0)]
Меркенарии	0a33444	resources/game.ini@0a33444:60-67	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(214,121,16); TEAMCOLOR_0..6=[(214,121,16),(182,97,8),(153,76,4),(121,60,4),(93,40,0),(60,24,0),(32,12,0)]
Сардаукары	0a33444	resources/game.ini@0a33444:70-77	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(101,12,101); TEAMCOLOR_0..6=[(242,105,242),(206,72,206),(170,48,170),(137,24,137),(101,12,101),(64,0,64),(32,0,32)]
Фремены	0a33444	resources/game.ini@0a33444:81-88	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(194,125,60); TEAMCOLOR_0..6=[(214,149,0),(182,125,0),(153,105,0),(125,80,0),(89,56,0),(60,36,0),(32,16,0)]
Коррино	0a33444	resources/game.ini@0a33444:91-98	RGB minimap и таблица RGB для спрайтов TEAMCOLOR_0..6, от светлого к тёмному	MINIMAPCOLOR=(192,192,192); TEAMCOLOR_0..6=[(226,182,149),(202,161,133),(178,141,117),(153,121,101),(129,101,85),(105,80,68),(80,60,52)]
``` 

### Повторяемые проверки таблиц данных

Ссылки в `tests.tsv`, `data.tsv`, `house-colors.tsv` проверялись следующим inline-скриптом. Он выполнял `git show <ревизия>:<путь>` для каждой ссылки и сверял верхнюю границу номера строки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python - <<'PY'
import re
import subprocess
from pathlib import Path

revs = {
    "e17379a": "e17379ad660fca46859b403a6c3d33ec8d831a40",
    "9208dcf": "9208dcf5a358f40afd95c99480e4e09f781ed566",
    "d06f2fc": "d06f2fcd2a347182c3774fb96e9a85570405c489",
    "0a33444": "0a33444e9032ef935dfe4cdde6bb622771484230",
}
pattern = re.compile(
    r"([A-Za-z0-9_./-]+)@(e17379a|9208dcf|d06f2fc|0a33444):([0-9,-]+)"
)
errors = []
checked = 0

for filename in ("tests.tsv", "data.tsv", "house-colors.tsv"):
    text = (Path(".tmp/p6r") / filename).read_text()
    for path, short, linespec in pattern.findall(text):
        checked += 1
        proc = subprocess.run(
            ["git", "show", f"{revs[short]}:{path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode:
            errors.append((filename, path, short, linespec, "missing path"))
            continue
        total = len(proc.stdout.splitlines())
        for part in linespec.split(","):
            bounds = part.split("-")
            high = int(bounds[-1])
            if high > total:
                errors.append(
                    (filename, path, short, linespec, f"file has {total} lines")
                )

print("references_checked=", checked)
print("errors=", errors)
PY
```

Вывод: `references_checked= 185`, `errors= []`.

Первые строки конкретных PNG-файлов проверялись следующим inline-скриптом. Шаблоны с `*` пропускаются; каждый конкретный файл запрашивается отдельно через `git cat-file -p <FORK1>:<путь>`:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python - <<'PY'
import subprocess
from collections import Counter
from pathlib import Path

rev = "9208dcf5a358f40afd95c99480e4e09f781ed566"
rows = Path(".tmp/p6r/data.tsv").read_text().splitlines()[1:]
paths = []
for row in rows:
    cols = row.split("\t")
    if len(cols) < 5 or "resources/hd/" not in cols[2] or "*" in cols[2]:
        continue
    paths.append(cols[2].split(";", 1)[0])

first_lines = Counter()
missing = []
non_lfs = []
for path in paths:
    try:
        raw = subprocess.check_output(
            ["git", "cat-file", "-p", f"{rev}:{path}"]
        )
    except subprocess.CalledProcessError:
        missing.append(path)
        continue
    first = raw.splitlines()[0].decode("ascii", "replace") if raw else ""
    first_lines[first] += 1
    if first != "version https://git-lfs.github.com/spec/v1":
        non_lfs.append((path, first))

print("source_PNGs_checked=", len(paths))
print("first_line_counts=", dict(first_lines))
print("missing=", missing)
print("non_LFS=", non_lfs)
PY
```

Вывод:

```text
source_PNGs_checked= 67
first_line_counts= {'version https://git-lfs.github.com/spec/v1': 67}
missing= []
non_LFS= []
```

### Фактические команды `git log` для PORT

Для каждого пути с кодом из карты выполнен `git log --oneline FORK1..PORT -- <путь>`; строки группировались только там, где файлы совместно отражают один перенос. Счётчики stdout проверены через `wc -l`:

```text
git log --oneline FORK1..PORT -- src/drawers/cMapDrawer.cpp | wc -l
40
git log --oneline FORK1..PORT -- src/drawers/cStructureDrawer.cpp src/drawers/cStructureDrawer.h | wc -l
68
git log --oneline FORK1..PORT -- src/player/cPlayer.cpp src/gameobjects/players/cPlayer.cpp src/player/cPlayer.h src/gameobjects/players/cPlayer.h | wc -l
156
git log --oneline FORK1..PORT -- src/utils/Graphics.cpp src/utils/Graphics.hpp | wc -l
12
git log --oneline FORK1..PORT -- src/utils/cDataPack.cpp src/utils/cDataPack.hpp src/utils/cPack.cpp src/utils/cPack.h | wc -l
12
git log --oneline FORK1..PORT -- CMakeLists.txt | wc -l
19
git log --oneline FORK1..PORT -- src/drawers/TerrainVariation.hpp src/utils/FactionTint.hpp
```

Последняя команда вывела пустой stdout. Существенные строки, взятые из полных логов: `5d60e18f Fogged cells draw the remembered terrain instead of the live terrain`, `5e34da81 Tile floor+ceil rendering eliminates black line gaps`, `87efa64f Connect world scale and HD assets to gameplay rendering`, `883f37f0 Fogged structures are drawn from memory instead of live`, `81e8c8ae Using colors from Houses not Palettes`, `d35f4afc Add configured flag to s_UnitInfo and guard setHouse loop`, `0c289327 Move createTextureFromIndexedSurfaceWithPalette to texture_utility`, `f3b41e2f Add world scale, HD unit sprite, windtrap flag, and frame density helpers`, `a84d768d Update cDataPack to SDL3 I/O and surface APIs`, `3f995a60 Replace SDL_RWops with SDL_IOStream in cPack`, `468b6889 Introduce Catch2 unit testing framework with MapGeometry tests`. Поиск `git grep -n -E 'getHouseTexture|FactionTint|HM_BUILD_(LIGHTFACTORY|SILO|CONSTYARD|BARRACKS|WINDTRAP)_FLAG|hdTerrainVariant(Index|Name)|TerrainVariation' PORT -- src` также вывел пустой stdout.

## Проверка формата таблиц

После сборки отчёта проверено число колонок в каждой строке всех семи TSV. Команда использовала `/srv/dune/venv/bin/python` и напечатала:

```text
fork.tsv: columns=6, rows=41, bad_rows=[]
tools.tsv: columns=5, rows=4, bad_rows=[]
upstream.tsv: columns=5, rows=16, bad_rows=[]
port.tsv: columns=5, rows=23, bad_rows=[]
tests.tsv: columns=7, rows=2, bad_rows=[]
data.tsv: columns=5, rows=72, bad_rows=[]
house-colors.tsv: columns=5, rows=32, bad_rows=[]
```
