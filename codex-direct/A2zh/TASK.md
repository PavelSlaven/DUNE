# Задание A2zh — HD-кадр Осадного 176×176 в движке и контракте

Режим: **«План у ревьюера»** (см. «Режим задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high`; механика — субагентам `gpt-6-luna` `xhigh`.
Ветка: `codex/a2zh` от `units3d/pilot`. Рабочая копия: `/srv/dune/worktrees/a2zh`.

## Цель

Владелец решил (`docs/decisions.md`, Р15–Р17):
- длина модели Осадного — 8,2 м, масштаб HD4 для всех юнитов — 16 px/м;
- HD-кадр Осадного — 176 × 176 пикселей атласа HD4 вместо 144 × 144; классический кадр 36 × 36 не меняется;
- правка движка делается сейчас, в этой ветке;
- по кадру 176 × 176 меняется только картинка корпуса, тени и башни. Полоса здоровья, полоса спайса, номер группы, звёзды опыта, рамка выделения `FOCUS` и `dimensions` по-прежнему строятся по прямоугольнику `getVisualRectangle()` (36 × 36 при масштабе 1). Наведение и выбор юнита по-прежнему идут по клетке карты и от кадра не зависят.

Ведущий уже перерендерил Осадного: в `resources/hd/units3d/siegebase/unit.json` стоят `frame_hd4` [176, 176] и `atlas_hd4` [1408, 176]. Пять атласов Осадного размером 1408 × 176 установлены в копию пака `/srv/dune/out/a2zh/packs/sdl_data_hd4.dat` (SHA-256 `adacfce94b6832627a01085a0cadd2e43496633c412944041ac15347af9799a2`). Рядом лежит классический `sdl_data.dat` (`07103d82e3975bc821ac52fa0f571f4a4276d34b9c57939abbf497c3f3ac0f80`). В той же копии пака стоят и атласы Девастатора пилота; их размеры прежние.

Сейчас движок вырезает HD-кадр юнита только как классический кадр × 4, поэтому атлас с кадром 176 читается неверно. Нужно, чтобы:
1. движок рисовал корпус, тень и башню Осадного кадром 176 × 176. Центр картинки совпадает с центром прямоугольника `getVisualRectangle()` с точностью до половины экранного пикселя: так работает целочисленное правило пункта 2 (при ширинах разной чётности точнее целыми координатами нельзя);
2. контракт `docs/units/unit_contract.json` описывал этот кадр.

## Что в коде сейчас

- `cUnit::draw()` (`src/gameobjects/units/cUnit.cpp:758–865`):
  - прямоугольник вырезки — `{start_x, start_y, bmp_width, bmp_height}`, где `start_x = bmp_body * bmp_width` (у башни — `bmp_head * bmp_width`), `start_y = bmp_height * iFrame`;
  - прямоугольник отрисовки — `getVisualRectangle()`; у тени керриола (`iType == CARRYALL`) он сдвинут на `+24` по `y`;
  - тень рисуется с прозрачностью `ShadowTrans`; башня — только при `top && iHitPoints > -1`; порядок — тень, корпус, башня; значок `SYMB_PICKMEUP` и рамка `FOCUS` берут `visualX`, `visualY` и `visual`.
- `SDLDrawer::renderStrechSprite` (`src/drawers/SDLDrawer.cpp:72–89`) умножает прямоугольник вырезки на `Texture::density`. У HD4-текстур `density` = 4, у классических — 1.
- `Texture` (`src/include/Texture.hpp`): `pixelW` — ширина текстуры в пикселях атласа, `w` — ширина в классических единицах (`pixelW / density`), `density` — плотность.
- `cUnit::getVisualRectangle()` (`cUnit.cpp:532–557`): `originalWidth = lround(factorZoomLevel(bmp_width))`, `visualWidth = lround(originalWidth * visualScale)`, `x = draw_x() - (visualWidth - originalWidth) / 2`; высота — так же. `factorZoomLevel(int value)` возвращает `float`: `value * m_zoomLevel` (`src/map/cMapCamera.h:149`); сам масштаб отдаёт `cMapCamera::getZoomLevel()` (`cMapCamera.h:173`). `visualScale` — результат `unitWorldScaleFactor` (`src/utils/WorldObjectScale.hpp`), вызов — `cUnit.cpp:540–544`.
- `dimensions` (`thinkFast_position`, `cUnit.cpp:3101`) = `getVisualRectangle()`. Он нужен только для отсечения по окну (`cUnit::isWithinViewport`, `cUnit.cpp:3444`; вызовы в `src/map/cMap.cpp`) и отладочной рамки.
- Размеры кадра юнита — `sUnitInfo[...]` в `src/utils/cIniGameRessouces.cpp`. Обнуление всех типов — цикл, который начинается в строке 31; он пишет через псевдоним `unitInfo.` (строки `unitInfo.bmp_width = 0;` и `unitInfo.bmp_height = 0;`). У Осадного `bmp_width = 18 * 2` (строка 183), `bmp_startpixel = 1` (строка 184), `bmp_height = 18 * 2` (строка 185). Структура — `s_UnitInfo` в `src/include/structs.h:16`, поля `bmp_width` и `bmp_height` — строки 21–22.
- `tools/units3d/unit_contract.py`:
  - читает присваивания `sUnitInfo[<тип>].<поле> = <значение>;` регулярным выражением (строка 29, поля `bmp|top|shadow|bmp_width|bmp_height`); присваивания через `unitInfo.` оно не видит;
  - задаёт `frame_hd4 = [bmp_width * density, bmp_height * density]` (строка 1050), а `hd4_size` берёт из пака `--pack-dir`;
  - ссылается на текстовые строки `cUnit::draw()`: в `draw_rules` (`parse_draw_geometry`, строки 734–980) и в записях атласов. Строка `int start_y = bmp_height * iFrame;` входит в `row_meaning.sources` и `sources` 35 записей `entries` и 8 записей `size_exceptions` (`unit_row_usage`, строка 610). Ветку `if (iType == CARRYALL)` и число после `visualY +` читает `parse_carryall_offset` (строка 700);
  - `size_exceptions` сейчас — 9 записей; у пяти записей Осадного причина — «HD4-размер не делится на целое число кадров».
- `tools/units3d/tests/test_unit_contract.py`:
  - строка 206 требует `frame_hd4 == frame_classic × 4` у каждой записи;
  - строки 271–276 закрепляют `UNIT_SIEGEBASE`: `hd4_size` [1152, 152], `frame_hd4` [144, 144], `remainder_px` [0, 8], `columns` 8;
  - генератор тест запускает отдельным процессом; модуль `unit_contract` сейчас не импортирует.
- Тесты движка (`tests/*.cpp`) — отдельные программы с `main()` без библиотеки тестов, регистрация — в блоке `if(BUILD_TESTING)` файла `CMakeLists.txt` (образец — `hd_presentation_tests`, строки 295–304). Конфигурация CMake требует SDL2. На servak SDL2 нет, поэтому новый тест должен компилироваться без SDL (пункт 2).

## Что сделать

### 1. Поле HD-кадра юнита

- В `s_UnitInfo` (`src/include/structs.h`), сразу после поля `bmp_height`, — два поля `int`: `hd_bmp_width` и `hd_bmp_height`. Значение — размер HD-кадра в пикселях атласа HD4. Значение 0 означает, что поле не задано.
- В цикле обнуления `cIniGameRessouces.cpp`, сразу после строки `unitInfo.bmp_height = 0;`, — строки `unitInfo.hd_bmp_width = 0;` и `unitInfo.hd_bmp_height = 0;`.
- У Осадного, сразу после строки `sUnitInfo[SIEGETANK].bmp_height = 18 * 2;`, — две строки подряд: `sUnitInfo[SIEGETANK].hd_bmp_width = 176;` и `sUnitInfo[SIEGETANK].hd_bmp_height = 176;`. Значение — целое число без выражения.
- Другим типам юнитов поля не задаются.

### 2. Чистая функция кадра — `src/utils/UnitFrameLayout.hpp`

Новый заголовок подключает только стандартную библиотеку C++: ни SDL, ни `cRectangle`. Прямоугольник — своя структура из четырёх `int`: `x`, `y`, `width`, `height`. Имена функции и структуры — твои, назови их в PLAN. Тест и мутации подключают заголовок строкой `#include "utils/UnitFrameLayout.hpp"`.

Входы функции:

| Вход | Смысл |
|---|---|
| `classicWidth`, `classicHeight` | `bmp_width`, `bmp_height` юнита |
| `hdWidth`, `hdHeight` | `hd_bmp_width`, `hd_bmp_height` юнита |
| `texturePixelWidth` | `Texture::pixelW` той текстуры, которую рисует этот вызов |
| `textureDensity` | `Texture::density` той же текстуры |
| `column`, `row` | столбец кадра (`bmp_body` или `bmp_head`) и строка (`iFrame`) |
| `visual` | прямоугольник `getVisualRectangle()` |
| `zoom` | `float`, масштаб карты (`cMapCamera::getZoomLevel()`) |
| `visualScale` | `float`, то же значение, которое `getVisualRectangle()` получает от `unitWorldScaleFactor` |

Выходы — прямоугольник вырезки `src` в единицах текстуры до умножения на плотность (то есть то, что сейчас передаётся в `renderStrechSprite`) и прямоугольник отрисовки `dest`.

**Правило.** HD-кадр действует тогда и только тогда, когда одновременно выполнено:
- `hdWidth > 0`;
- `hdHeight > 0`;
- `texturePixelWidth == 8 * hdWidth`.

Классический атлас Осадного шире 288 пикселей не бывает, поэтому при классической графике HD-кадр не действует по последнему условию.

- **HD-кадр не действует:**
  - `src = {column * classicWidth, row * classicHeight, classicWidth, classicHeight}`;
  - `dest = visual`.

  Это нынешнее поведение без изменений.
- **HD-кадр действует:**
  - `fw = hdWidth / textureDensity`, `fh = hdHeight / textureDensity` (целое деление);
  - `src = {column * fw, row * fh, fw, fh}`;
  - `W = lround(lround(fw * zoom) * visualScale)`, `H = lround(lround(fh * zoom) * visualScale)`. Арифметика — как в `getVisualRectangle`: `fw * zoom` — произведение `int` на `float`, результат `float`; `std::lround`; результат приводится к `int` через `static_cast<int>`; второе произведение — `int` на `float`, `std::lround`, `static_cast<int>`;
  - `dest = {visual.x - (W - visual.width) / 2, visual.y - (H - visual.height) / 2, W, H}` с целым делением C++.

### 3. `cUnit::draw()`

- Строка `const cRectangle visual = getVisualRectangle();` остаётся.
- `zoom` — `mapCamera->getZoomLevel()`.
- `visualScale` — в `draw()` тот же вызов с теми же аргументами, что в `getVisualRectangle()`: `unitWorldScaleFactor(game.getWorldScaleFactor(), gfxdata && gfxdata->getDensity() > 1, iType == TANK || iType == SIEGETANK)`. Сам `getVisualRectangle()` не меняется.
- Тень, корпус и башня берут `src` и `dest` из функции пункта 2. Каждый вызов получает `pixelW` и `density` своей текстуры: `shadow`, `bitmap`, `top` (поле `pixelW`, не `w`). Столбец: у тени и корпуса — `bmp_body`, у башни — `bmp_head`. Строка — `iFrame`.
- Тень керриола: в ветке `if (iType == CARRYALL)` к `dest.y`, полученному от функции, прибавляется число `24`, записанное литералом (нынешний код — `cUnit.cpp:798–805`).
- Не меняются: ранние выходы `isHidden()` и `isSandworm()`; условия `if (shadow)`, `if (bitmap)` с записью в лог, `if (top && iHitPoints > -1)`; `ShadowTrans` у тени; порядок тень → корпус → башня; `SYMB_PICKMEUP` по `visualX`, `visualY - 7`; рамка `FOCUS` по `visual`.

Не меняются:
- `getVisualRectangle()`, `draw_x()`, `draw_y()`, `getBmpWidth()`, `getBmpHeight()`, `isWithinViewport()`, `thinkFast_position()`;
- полоса здоровья, полоса спайса, номер группы, звёзды, рамка `FOCUS`, `dimensions`;
- харвестер на очистительном заводе (`cStructureDrawer::drawHarvesterOnRefineryPad`, `src/drawers/cStructureDrawer.cpp:843`);
- все остальные функции движка.

Отсечение по окну остаётся по `dimensions`. Поэтому у края окна Осадный начинает рисоваться, когда в окно входит прямоугольник `getVisualRectangle()`. Полоса картинки шириной `(W − visual.width) / 2` (4 пикселя при масштабе 1) до этого не видна. Так же сейчас ведёт себя тень керриола со сдвигом `+24`. Задача это не меняет.

### 4. Тест движка — `tests/UnitFrameLayoutTests.cpp`

Программа в стиле `tests/HdPresentationTests.cpp`: `main()` возвращает 0, если все проверки прошли, иначе 1. На каждую проваленную проверку печатает строку `FAIL <номер случая> <вход> <получено> <ожидалось>`. Регистрация в `CMakeLists.txt` по образцу `hd_presentation_tests`: цель `unit_frame_layout_tests`, `add_test(NAME unit_frame_layout COMMAND unit_frame_layout_tests)`.

Ожидаемые значения — числа, записанные в тесте. Тест не вызывает функцию пункта 2 для получения ожидаемого значения. В цикле по `column` или `row` ожидаемое смещение пишется как литерал ширины или высоты кадра, умноженный на `column` или `row` (например, `44 * column`). Значения `W`, `H`, `dest.x`, `dest.y` — только литералы из таблиц ниже.

Числа таблицы У2 и случая У10 вычисли независимым скриптом Python `.tmp/u2_check.py`: `numpy.float32` для обоих произведений, округление половины от нуля, деление смещения с усечением к нулю. Запуск — `/srv/dune/venv/bin/python .tmp/u2_check.py > .tmp/u2_check.log` (`numpy` в этом окружении есть). Если скрипт даёт для ячейки другое число — `Q` с выводом скрипта, тест не подгонять.

Наборы параметров для случаев, где HD-кадр не действует:
- **Н1:** `zoom` 1, `visualScale` 1, `visual` = {100, 200, `classicWidth`, `classicHeight`};
- **Н2:** `zoom` 1,3, `visualScale` 1,25, `visual` = {94, 194, 59, 59}.

Случаи (в каждом сравниваются `src` и `dest` целиком; `row` = 0, если не сказано иначе):

| № | Юнит и вход | Ожидается |
|---|---|---|
| У1 | Осадный: `classic` 36 × 36, `hd` 176 × 176, `density` 4, `pixelW` 1408, `visual` {100, 200, 36, 36}, `zoom` 1, `visualScale` 1; `column` 0–7 | `src` {44 · column, 0, 44, 44}; `dest` {96, 196, 44, 44} |
| У2 | Осадный, как У1, `column` 3; сетка `zoom` × `visualScale`, `visual` = {100, 200, w, w}, где `w` — ширина из таблицы ниже | `src` {132, 0, 44, 44}; `dest` = {x, x + 100, W, W} по таблице ниже |
| У3 | Осадный, классическая графика: `classic` 36 × 36, `hd` 176 × 176, `density` 1, `pixelW` 288; `column` 0–7; Н1 и Н2 | `src` {36 · column, 0, 36, 36}; `dest` = `visual` |
| У4 | Осадный, старый HD-атлас: как У3, но `density` 4, `pixelW` 1152; Н1 и Н2 | как У3 |
| У5 | Осадный, атлас не по правилу: как У4, но `pixelW` 1412; Н1 и Н2 | как У3 |
| У6 | Осадный, задана одна сторона: как У4, но `pixelW` 1408 и `hd` 176 × 0, затем `hd` 0 × 176; Н1 и Н2 | как У3 |
| У7 | Девастатор: `classic` 38 × 46, `hd` 0 × 0, `density` 4, `pixelW` 1216, `column` 0–7; Н1 и Н2 | `src` {38 · column, 0, 38, 46}; `dest` = `visual` |
| У8 | Тень керриола: `classic` 48 × 48, `hd` 0 × 0, `density` 4, `pixelW` 1536, `column` 0–7, `row` 1; Н1 и Н2 | `src` {48 · column, 48, 48, 48}; `dest` = `visual` (без `+24`: сдвиг делает `draw()`) |
| У9 | Харвестер: `classic` 80 × 52, `hd` 0 × 0, две пары (`density` 1, `pixelW` 640) и (`density` 4, `pixelW` 2560), `column` 0–7, `row` 0–3; Н1 и Н2 | `src` {80 · column, 52 · row, 80, 52}; `dest` = `visual` |
| У10 | Прямоугольный HD-кадр (синтетический вход): `classic` 38 × 46, `hd` 160 × 192, `density` 4, `pixelW` 1280, `column` 0–7, `row` 0 и 1 | `src` {40 · column, 48 · row, 40, 48}; при `zoom` 1, `visualScale` 1, `visual` {100, 200, 38, 46} — `dest` {99, 199, 40, 48}; при `zoom` 1,3, `visualScale` 1,25, `visual` {100, 200, 61, 75} — `dest` {98, 199, 65, 78} |

Таблица У2: в ячейке — `w → W, x`. Здесь `w` — ширина `visual` (`lround(lround(36 · zoom) · visualScale)`), `W` — ширина `dest`, `x` — `dest.x`; высота равна ширине, `dest.y = x + 100`.

| `zoom` \ `visualScale` | 1,0 | 1,1 | 1,25 | 1,5 |
|---|---|---|---|---|
| 0,25 | 9 → 11, 99 | 10 → 12, 99 | 11 → 14, 99 | 14 → 17, 99 |
| 0,5 | 18 → 22, 98 | 20 → 24, 98 | 23 → 28, 98 | 27 → 33, 97 |
| 1,0 | 36 → 44, 96 | 40 → 48, 96 | 45 → 55, 95 | 54 → 66, 94 |
| 1,5 | 54 → 66, 94 | 59 → 73, 93 | 68 → 83, 93 | 81 → 99, 91 |
| 2,0 | 72 → 88, 92 | 79 → 97, 91 | 90 → 110, 90 | 108 → 132, 88 |
| 4,0 | 144 → 176, 84 | 158 → 194, 82 | 180 → 220, 80 | 216 → 264, 76 |
| 0,3 | 11 → 13, 99 | 12 → 14, 99 | 14 → 16, 99 | 17 → 20, 99 |
| 1,3 | 47 → 57, 95 | 52 → 63, 95 | 59 → 71, 94 | 71 → 86, 93 |

Компиляция и запуск на servak (без SDL):
```
g++ -std=c++20 -Wall -Wextra -Werror -Isrc tests/UnitFrameLayoutTests.cpp -o .tmp/unit_frame_layout_tests && .tmp/unit_frame_layout_tests
```

### 5. Контракт — `tools/units3d/unit_contract.py`

**Поля.** Регулярное выражение строки 29 читает и поля `hd_bmp_width`, `hd_bmp_height`.

**Состояние HD-кадра типа юнита:**
- «не задан» — у типа нет присваиваний `hd_bmp_*` или оба равны 0;
- «задан» — оба поля присвоены и оба больше 0;
- любое другое сочетание (присвоено одно поле; одно больше 0, другое 0) — `ValueError` с именем типа.

**`frame_hd4` записи атласа** — отдельная функция; имя и подпись назови в PLAN. Входы: имя атласа, записи типов юнитов, отображённых на атлас, в формате `parse_unit_records` (`record["type"]`, `record["sizes"]`), `density`, `hd4_size` (может быть `None`). Результат:
- все типы «не задан» — `[bmp_width * density, bmp_height * density]` (нынешнее правило строки 1050);
- все типы «задан» с одной и той же парой `[W, H]`, и `hd4_size` равен `None` или `hd4_size[0] == 8 * W` — `[W, H]`;
- иначе — `ValueError` с именем атласа: смесь «задан» и «не задан»; разные пары; `hd4_size[0] != 8 * W`.

Неоднозначные классические размеры по-прежнему дают нынешний `ValueError` (строки 1046–1047). `frame_classic` не меняется.

**Ссылки на поля.** В `sources` пяти записей Осадного (`UNIT_SIEGEBASE`, `UNIT_SIEGEBASE_SHADOW`, `UNIT_SIEGETOP`, `HM_UNIT_SIEGEBASE`, `HM_UNIT_SIEGETOP`) добавляются две ссылки — на строки `sUnitInfo[SIEGETANK].hd_bmp_width` и `sUnitInfo[SIEGETANK].hd_bmp_height` в `cIniGameRessouces.cpp`, в том же формате, что нынешние ссылки на `bmp_width` и `bmp_height`. Строки обнуления в контракт не попадают.

**Ссылки на `cUnit::draw()`.** Генератор читает новый текст `draw()`:
- `draw_rules.source_rectangle` и `draw_rules.draw_destination`: `value` описывает правило пункта 2 — условие и обе ветви. `sources` ссылаются на строки функции в `src/utils/UnitFrameLayout.hpp` и на три её вызова в `draw()`;
- `draw_rules.carryall_shadow_offset`: число 24 читается из строки ветки `if (iType == CARRYALL)` в новом `draw()`;
- остальные правила `draw_rules`, которые ссылаются на строки `draw()`, получают ссылки на новые строки с тем же смыслом;
- в `row_meaning.sources` и `sources` записей `entries` и `size_exceptions` ссылка с `identifier` `int start_y = bmp_height * iFrame;` заменяется ссылкой на строку `draw()`, где `iFrame` передаётся функции пункта 2 как `row`. Новый `identifier` — фрагмент этой строки, содержащий `iFrame`, один и тот же во всех записях. Текст `row_meaning.value` не меняется.

Все ссылки `sources` указывают на существующие строки, которые содержат свой `identifier`: это проверяет тест `test_all_source_references_resolve_to_executable_lines`.

**Пересоздание** `docs/units/unit_contract.json` и `docs/units/UNIT_CONTRACT.md`:
```
/srv/dune/venv/bin/python tools/units3d/unit_contract.py --pack-dir /srv/dune/out/a2zh/packs
```

**Ожидаемый дифф `unit_contract.json` против `ecffa2f5`:**
- (а) пять записей Осадного в `entries`: `frame_hd4` [176, 176], `hd4_size` [1408, 176], `remainder_px` [0, 0], две новые ссылки на поля `hd_bmp_*`; `columns` 8 и `rows` 1 остаются;
- (б) `size_exceptions`: `UNIT_SIEGEBASE`, `UNIT_SIEGEBASE_SHADOW`, `UNIT_SIEGETOP` остаются с одной причиной «HD4-размер не равен classic-размеру, умноженному на 4.», с новыми `hd4_size`, `frame_hd4`, `remainder_px` и с прежним `expected_hd4_size` [1152, 152]; `HM_UNIT_SIEGEBASE` и `HM_UNIT_SIEGETOP` из `size_exceptions` уходят;
- (в) `draw_rules` и `draw_sites`;
- (г) номера строк в ссылках на изменённые файлы `cUnit.cpp`, `cIniGameRessouces.cpp`, `structs.h` (ссылок на `structs.h` сейчас нет — 0 строк);
- (д) замена ссылки `int start_y = bmp_height * iFrame;` по правилу выше во всех записях `entries` и `size_exceptions`.

Любое другое изменение — `Q` до сдачи.

### 6. Тесты контракта — `tools/units3d/tests/test_unit_contract.py`

Здесь разрешено менять именно эти ожидания, потому что они записывают старое правило кадра:
- строка 206: пять записей Осадного из проверки `frame_hd4 == frame_classic × 4` исключаются, у всех остальных записей проверка остаётся;
- строки 271–276: `UNIT_SIEGEBASE` — `hd4_size` [1408, 176], `frame_hd4` [176, 176], `remainder_px` [0, 0], `columns` 8.

Добавить тесты:
- у пяти записей Осадного `frame_classic` = [36, 36] и `frame_hd4` = [176, 176] (литералы);
- функция `frame_hd4` пункта 5 на синтетических записях — отдельный класс тестов без `skipUnless`; модуль импортируется из `tools/units3d` (`sys.path` и `import unit_contract`). Случаи (`density` 4, классический кадр 36 × 36 у всех типов):

| № | Записи типов на атласе | `hd4_size` | Ожидается |
|---|---|---|---|
| Т1 | два типа, оба «не задан» | [1152, 152] | [144, 144] |
| Т2 | два типа, оба 176 × 176 | [1408, 176] | [176, 176] |
| Т3 | тип A 176 × 176, тип B «не задан» | [1408, 176] | `ValueError`, в тексте — имя атласа |
| Т4 | тип A 176 × 176, тип B 176 × 180 | [1408, 176] | `ValueError`, в тексте — имя атласа |
| Т5 | один тип: `hd_bmp_width` 176, `hd_bmp_height` 0 | [1408, 176] | `ValueError` |
| Т6 | два типа, оба 176 × 176 | [1152, 152] | `ValueError`, в тексте — имя атласа |

Другие ожидания `test_unit_contract.py` не менять. Если тест падает из-за другого ожидания — `Q`.

### 7. Приёмочные тесты — первыми и под хэшем

До кода движка и генератора ты (sol) пишешь:
- `tests/UnitFrameLayoutTests.cpp` и его регистрацию в `CMakeLists.txt`;
- правки и новые тесты пункта 6;
- скрипт `.tmp/u2_check.py` и его вывод `.tmp/u2_check.log`;
- заглушку `.tmp/red-stub/utils/UnitFrameLayout.hpp` с теми же именами и подписью, что в PLAN, и с нынешним поведением: HD-кадр не действует никогда.

Затем красный прогон, лог `.tmp/red.log`:
- тест движка с заглушкой: `g++ -std=c++20 -Wall -Wextra -Werror -I.tmp/red-stub -Isrc tests/UnitFrameLayoutTests.cpp -o .tmp/red-engine && .tmp/red-engine`. Ожидается: код выхода 1; строки `FAIL` есть у У1, У2 и У10; у У3–У9 строк `FAIL` нет;
- тесты Python на нынешнем коде, команда из «Чем проверить» п. 2. Ожидается красный у теста со строками 206 и 271–276, у нового теста пяти записей Осадного, у Т1–Т6 (функции ещё нет), у `test_generated_files_match_committed_files` и у `test_inventory_and_sizes_match_packs` в пяти подслучаях Осадного (в нынешнем JSON `hd4_size` [1152, 152], в паке — [1408, 176]). Все остальные тесты зелёные. Ведущий проверил это на нетронутой ветке: 127 тестов, 6 падений — `test_generated_files_match_committed_files` и пять подслучаев `test_inventory_and_sizes_match_packs`; прогон идёт около 18 минут.

Если красный прогон отличается от ожидаемого — `Q` с логом.

Хэши — в новый файл `codex-direct/A2zh/ACCEPTANCE.sha256`, две строки в формате вывода `sha256sum` (`<hex>  <путь от корня репозитория>`): `tests/UnitFrameLayoutTests.cpp` и `tools/units3d/tests/test_unit_contract.py`.

После этого оба файла не меняются. Если тест неверен — `Q`. Код пишут субагенты luna под твоим надзором.

## Доказательство красным

Мутации — в копиях заголовка `.tmp/mut/<имя>/utils/UnitFrameLayout.hpp`, сам код не трогать. Мутация пишется на C++ в копии; типы — как в функции (`int` и `float`). Одна программа `.tmp/mut/run.sh` создаёт все копии, компилирует тест с `-I.tmp/mut/<имя> -Isrc` и запускает его; лог — `.tmp/mut/mutations.log`. Каждый случай правого столбца даёт строку `FAIL` на своей мутации и проходит на настоящем коде.

| Имя | Мутация функции пункта 2 | Краснеет (не меньше) |
|---|---|---|
| MU1 | `dest.x = visual.x`, `dest.y = visual.y` (без центрирования) | У1, У2 |
| MU2 | `W = static_cast<int>(std::lround(fw * zoom * visualScale))`, `H` — так же (одно округление) | ячейки У2 (0,3; 1,1), (0,3; 1,25) и (1,3; 1,25) |
| MU3 | условие без `texturePixelWidth == 8 * hdWidth` | У4, У5 |
| MU4 | при действующем HD-кадре `src` остаётся классическим | У1, У10 |
| MU5 | условие `(hdWidth > 0 \|\| hdHeight > 0) && texturePixelWidth == 8 * hdWidth` | У6 со входом `hd` 176 × 0 |
| MU6 | `fh = hdWidth / textureDensity` | У10 |

## Проверка подключения в `draw()`

`cUnit.cpp` на servak не компилируется, поэтому подключение функции тестом не проверяется. В DONE для каждого пункта — строка нового `cUnit.cpp` (файл:строка):
1. тень и корпус передают столбец `bmp_body`, башня — `bmp_head`; строка у всех — `iFrame`;
2. каждый вызов передаёт `pixelW` и `density` своей текстуры (`shadow`, `bitmap`, `top`);
3. `zoom` — `mapCamera->getZoomLevel()`; `visualScale` — вызов `unitWorldScaleFactor` с аргументами пункта 3;
4. `+24` керриола прибавляется к `dest.y` только в ветке тени; `ShadowTrans` у тени сохранён;
5. `SYMB_PICKMEUP` и `FOCUS` по-прежнему берут `visualX`, `visualY`, `visual`;
6. ранние выходы, проверки указателей, условие башни `iHitPoints > -1` и порядок тень → корпус → башня не изменились.

Ведущий сверяет эти пункты по диффу и проверяет сборкой и запуском игры.

## Чем проверить

1. Тест движка — команда из пункта 4, лог `.tmp/engine-test.log`, код выхода 0.
2. Тесты Python с новым паком, без пропусков:
   ```
   D2TM_PACK_DIR=/srv/dune/out/a2zh/packs PYTHONDONTWRITEBYTECODE=1 /srv/dune/venv/bin/python -m unittest discover -s tools/units3d/tests -v
   ```
   Лог — `.tmp/green.log`. Все тесты зелёные, `skipped` нет.
3. `sha256sum -c tools/units3d/tests/ACCEPTANCE.sha256` — обе строки `OK`: `check_unit.py` и его тесты не меняются.
4. `sha256sum -c codex-direct/A2zh/ACCEPTANCE.sha256` — обе строки `OK`.
5. `git status --short` — только файлы рамки правок. Папка `.tmp/` исключена через `.git/info/exclude` и в выводе не появляется.

`cUnit.cpp` и `cIniGameRessouces.cpp` на servak не компилируются: нужен SDL2. Полную сборку и `ctest` делает ведущий на своей машине. В DONE это пункт «Не проверено».

## Не трогать

- `tools/units3d/check_unit.py`, `tools/units3d/tests/test_check_unit.py`, `tools/units3d/tests/ACCEPTANCE.sha256`;
- `tools/units3d/render_unit.py`, `tools/units3d/build_atlases.py`, `tools/units3d/install.py`, `tools/hd_assets.py`;
- `resources/`, пакеты в `/srv/dune/inputs/` и `/srv/dune/out/a2zh/packs/`;
- `src/` и `tests/` вне файлов рамки правок.

## Чего задача не делает

- Не меняет HD-кадры других юнитов и классическую графику.
- Не меняет полосу здоровья, рамку выделения, наведение и выбор юнита, отсечение по окну.
- Не меняет свет и тень.
- Не собирает игру и не запускает её: это делает ведущий.
- Не обновляет пак в репозитории.

## Режим задания

«План у ревьюера»: до любых правок, включая тесты, пришли `## PLAN-A2zh` и жди `PLAN-OK-A2zh`. В PLAN:
- имена и подписи функции и структуры пункта 2 и функции `frame_hd4` пункта 5;
- цепочка от атласа в паке до `Texture::pixelW` и `Texture::density` для текстур `getUnitBitmap`, `getUnitTopBitmap` и `getUnitShadowBitmap` Осадного: каждое звено — ссылкой файл:строка. Если `pixelW` хотя бы одной из них не равен ширине атласа HD4 в пикселях — `Q`;
- каждое требование своими словами;
- источник истины;
- что изменишь;
- чем проверишь;
- развилки с рекомендацией;
- объём;
- чего решение не закроет.

Смена цели, границ правок, критерия готовности или источника истины — `PLAN-A2zh-delta`.

## Организация работы

- **Параллельно:** в шаге 3 — помощники A и B одновременно; в шаге 4 — помощники B и C одновременно.
- **Порядок и исполнители:**
1. Ты: PLAN, затем стоп до `PLAN-OK-A2zh`.
2. Ты: приёмочные тесты и всё из пункта 7, красный прогон, хэши.
3. Одновременно два помощника:
   - помощник A — код движка (пункты 1–3);
   - помощник B — генератор без ссылок на `draw()`: поля, состояния, функция `frame_hd4`, ссылки на поля Осадного (пункт 5 до раздела «Ссылки на `cUnit::draw()`»).
4. Когда A закончил, одновременно:
   - помощник B в той же сессии — ссылки на `cUnit::draw()` (раздел пункта 5);
   - помощник C — `.tmp/mut/run.sh` и прогон мутаций MU1–MU6.
5. Ты: пересоздание контракта, сверка диффа с (а)–(д), тест движка и тесты Python зелёные, проверка результата мутаций, пункты подключения в `draw()`.
6. Ты: полный прогон «Чем проверить», `DONE-A2zh`.

Помощники — `gpt-6-luna` `xhigh`. Твоё — приёмочные тесты, сверка диффа контракта, проверка подключения и итоговая сверка.

**Остановки** (`Q` и стоп):
- дифф контракта выходит за пункты (а)–(д);
- тест падает из-за ожидания, которое задание не разрешает менять;
- красный прогон отличается от ожидаемого;
- случай правого столбца остался зелёным на своей мутации;
- число таблицы У2 или случая У10 расходится с твоим независимым скриптом.

**Рамка правок:** только
- `src/include/structs.h`, `src/utils/cIniGameRessouces.cpp`, `src/gameobjects/units/cUnit.cpp`, `src/utils/UnitFrameLayout.hpp`;
- `tests/UnitFrameLayoutTests.cpp`, `CMakeLists.txt`;
- `tools/units3d/unit_contract.py`, `tools/units3d/tests/test_unit_contract.py`;
- `docs/units/unit_contract.json`, `docs/units/UNIT_CONTRACT.md`, `codex-direct/A2zh/ACCEPTANCE.sha256`;
- `.tmp/`.

Правка вне рамки — `Q` до правки.

**Журнал:** `.tmp/progress.md`, строка после каждого закрытого шага порядка; только то, что подтверждено логом.

## Сдача

Последнее сообщение — `## DONE-A2zh | время | ветка codex/a2zh`. Состав:
- журнал хода;
- красный прогон до правки (путь к логу, строки итога и строки `FAIL`);
- зелёные прогоны пунктов 1–4 «Чем проверить» (пути к логам, строки итога);
- путь к `.tmp/u2_check.log`;
- мутации MU1–MU6: путь к логу и список покрасневших случаев;
- дифф контракта по пунктам (а)–(д) с числом изменённых строк в каждом;
- шесть пунктов «Проверка подключения в `draw()`» со ссылками файл:строка;
- раздел «Не проверено» (обязателен);
- `git status --short`.
