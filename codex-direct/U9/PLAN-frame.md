## PLAN-U9-frame | 2026-11-01 20:55:02 UTC

План опирается на [Р15–Р17](/srv/dune/worktrees/u9f/docs/decisions.md:23), [Р28](/srv/dune/worktrees/u9f/docs/decisions.md:36), поведение из задания и разрешение ведущего обновить старые ожидания тестов. Эталон неизменяемого поведения — `bb2f1b37`. Код, атласы и отслеживаемые документы не изменены; чтение и пробы сохранены в `.tmp/`.

### 1. Движок

**Разделить логическую рамку юнита и размер HD-кадра.** Сейчас логические размеры находятся в [s_UnitInfo](/srv/dune/worktrees/u9f/src/include/structs.h:21); для Осадного задано 36 × 36 в [cIniGameRessouces.cpp](/srv/dune/worktrees/u9f/src/utils/cIniGameRessouces.cpp:183). [cUnit::draw](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:758) использует эти размеры одновременно для шага кадров, исходного прямоугольника и назначения.

Предлагаю добавить в `s_UnitInfo` поля `hd_frame_width/height`, выраженные в физических пикселях атласа:

- Нулевые значения сохраняют прежний расчёт через `bmp_width/height`.
- Только у Осадного значения равны 176 × 176.
- `bmp_width/height`, `getBmpWidth/Height()` и [getVisualRectangle()](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:532) остаются прежними.

Общий расчёт вынести в новый `src/utils/UnitSpriteLayout.hpp`, без зависимости от SDL. Признак применения новых размеров — наличие HD-размеров и HD-плотность конкретной текстуры; проверки типа `if (SIEGETANK)` в механизме рисования не будет.

В HD плотность равна четырём: загрузка задаёт её в [cGame_logic.cpp](/srv/dune/worktrees/u9f/src/cGame_logic.cpp:1056), [Texture](/srv/dune/worktrees/u9f/src/include/Texture.hpp:16) хранит физические и логические размеры, а [SDLDrawer](/srv/dune/worktrees/u9f/src/drawers/SDLDrawer.cpp:72) умножает исходный прямоугольник на плотность. Поэтому для нового кадра:

- Исходный прямоугольник в единицах API рисования — 44 × 44.
- Столбец тела и тени начинается с `bodyFacingIndex × 44`, башни — с `headFacingIndex × 44`.
- Строка начинается с `iFrame × 44`.
- После умножения на плотность читается ровно 176 × 176 физических пикселей.

Размер назначения рассчитывать от 44 через существующий порядок округлений камеры и масштаба мира. Центр назначения брать из прежнего `visual`, рассчитанного от 36. При единичных масштабах картинка занимает 44 × 44 логических пикселя, а рамка — 36 × 36; плотность изображения остаётся прежней.

**Развилка центрирования.** Целочисленное назначение при нечётной разности размеров смещает центр на половину пикселя. Рекомендую отдельный overload `SDLDrawer` с дробным назначением для общего механизма HD-размера:

```text
x = visual.x + (visual.width  - spriteWidth)  / 2.0
y = visual.y + (visual.height - spriteHeight) / 2.0
```

Он использует `SDL_RenderCopyF`; прежний `SDL_Rect`-путь сохраняется для классики и юнитов без переопределения. Альтернатива — оставить целочисленное округление, но тогда буквальное совпадение центров выполняется не при каждой комбинации масштабов. Рекомендация — дробное назначение; доступность API проверяется сборкой SDL2 в CI.

Корпус, тень и башня используют один расчёт назначения и соответствующие направления. Маски Дома накладываются на целый атлас при подготовке текстур в [Graphics::getHouseTexture](/srv/dune/worktrees/u9f/src/utils/Graphics.cpp:226); [проверка совпадения размеров маски и изображения](/srv/dune/worktrees/u9f/src/utils/Graphics.cpp:376) уже подходит. Обе маски должны обновиться вместе с изображениями.

Остальные зависимости сохраняются:

| Путь | Решение |
|---|---|
| Здоровье, спайс, группа, опыт | Оставить расчёты от `visual`: [cUnit.cpp:574](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:574), [621](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:621), [651](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:651), [712](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:712). |
| `FOCUS`, значок ожидания carryall, отладочные линии | Сохранить прежние координаты в конце [draw()](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:839). |
| Путь отладки | Сохранить расчёт по клеткам в [draw_path()](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:727). |
| Щелчок | Сохранить поиск по ячейке карты: [cGameControlsContext.cpp:142](/srv/dune/worktrees/u9f/src/controls/cGameControlsContext.cpp:142). |
| Выбор рамкой | Сохранить попадание центра юнита в рамку: [cPlayer.cpp:454](/srv/dune/worktrees/u9f/src/player/cPlayer.cpp:454). |
| Отсечение по viewport | Сохранить `dimensions = getVisualRectangle()`: [cUnit.cpp:3098](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:3098). |
| Carryall | Перевозимый юнит скрывается; собственное рисование carryall и смещение его тени остаются прежними: [cUnit.cpp:758](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:758), [798](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:798). |
| Иконки и ремонтное превью | Используют отдельный `icon`, а не кадры тела: [cBuildingListDrawer.cpp:141](/srv/dune/worktrees/u9f/src/drawers/cBuildingListDrawer.cpp:141), [cStructureDrawer.cpp:912](/srv/dune/worktrees/u9f/src/drawers/cStructureDrawer.cpp:912). |
| Превью харвестера на НПЗ | Отдельный потребитель кадра харвестера; не менять: [cStructureDrawer.cpp:859](/srv/dune/worktrees/u9f/src/drawers/cStructureDrawer.cpp:859). |
| Смерть | Осадный создаёт отдельные частицы: [cUnit.cpp:262](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:262). Их атласы не меняются. |
| Мини-карта | Рисует обозначения по клеткам и цветам игроков: [cMiniMapDrawer.cpp:294](/srv/dune/worktrees/u9f/src/drawers/cMiniMapDrawer.cpp:294). |

Таким образом, пункты 2–4 обеспечиваются сохранением логической геометрии, прежнего пути классики и прежнего пути каждого юнита без HD-переопределения. Новые размеры затрагивают только картинку Осадного.

### 2. Инструмент перерисовки и пак

Сейчас [Unit.old_frame()](/srv/dune/worktrees/u9f/tools/units3d/redraw_common.py:97) режет старый атлас по `frame`, [place()](/srv/dune/worktrees/u9f/tools/units3d/redraw_common.py:340) использует размер выходного кадра также для масштаба холста, а [build](/srv/dune/worktrees/u9f/tools/units3d/redraw_build.py:117) выделяет атласы по размеру старого изображения. Одной замены `frame` недостаточно.

В двух описаниях Осадного предлагаю задать:

```json
"reference_frame": [144, 152],
"reference_anchor": [72, 72],
"frame": [176, 176],
"atlas_size": [1408, 176]
```

Файлы: [UNIT_SIEGEBASE/unit.json](/srv/dune/worktrees/u9f/tools/units3d/units/UNIT_SIEGEBASE/unit.json:7) и [UNIT_SIEGETOP/unit.json](/srv/dune/worktrees/u9f/tools/units3d/units/UNIT_SIEGETOP/unit.json:7).

Для описаний без новых полей сохранить прежние значения: старый кадр равен `frame`, выходной атлас равен старому атласу. Дополнительные поля проверяются в [load_unit()](/srv/dune/worktrees/u9f/tools/units3d/redraw_common.py:103).

Расчёт сборки:

1. Старые кадры, их рамки и доли старых масок читать по `reference_frame`, то есть 144 × 152.
2. Медиану считать по прежней формуле [redraw_build.py:49](/srv/dune/worktrees/u9f/tools/units3d/redraw_build.py:49), с `M = 152`. Расчёт соответствует [шагу 2 U1](/srv/dune/worktrees/u9f/codex-direct/U1/TASK.md:113).
3. Размер уменьшенного холста в `place` оставить `round(M × scale)`. Передать исходный `M` отдельно от выходного кадра. Замена `M` на 176 внесла бы дополнительное увеличение, отсутствующее в выбранном коэффициенте.
4. Старую рамку для размещения перевести на `(16, 16)`: старый игровой центр `(72, 72)` переходит в `(88, 88)`. Сдвиг `(16, 12)` ошибочно использовал бы центр полного старого кадра высотой 152; движок читал только 144 строки.
5. После центрирования сохранить сдвиг внутрь и проверку всей ненулевой альфы после окончательного размещения — [шаг 3 U1](/srv/dune/worktrees/u9f/codex-direct/U1/TASK.md:114). Корпус, перекраска и маска получают одинаковый сдвиг.
6. Для Осадного выделять выходные массивы 1408 × 176. Остальным оставить существующее выделение, включая прежние прозрачные остаточные полосы.
7. В [redraw_shadow.py:10](/srv/dune/worktrees/u9f/tools/units3d/redraw_shadow.py:10) анализировать старую тень по `reference_frame`. Подготовка направляющих и `score` получают прежний исходный `M` через `Unit.maximum`.
8. В [redraw_sheets.py:190](/srv/dune/worktrees/u9f/tools/units3d/redraw_sheets.py:190) старую картинку переносить на общий холст с сохранением игрового центра. Нельзя растягивать старые 144 × 152 непосредственно до новых размеров ячейки: нынешний вызов [на строке 194](/srv/dune/worktrees/u9f/tools/units3d/redraw_sheets.py:194) исказил бы сравнение.

`redraw.py` остаётся входной командой; его [диспетчеризация](/srv/dune/worktrees/u9f/tools/units3d/redraw.py:49) уже передаёт описание общим модулям. Исходный закреплённый пак инструмента не менять: [redraw_common.py:17](/srv/dune/worktrees/u9f/tools/units3d/redraw_common.py:17).

**Правило размера «как у Девастатора».** Рекомендую единый коэффициент по медиане отношений ширин непрозрачных рамок тела в одинаковых направлениях:

```text
F = median(Wdevastator[k] / Wsiegebase[k])
```

Измерение по `alpha > 127`, без тени и башни, дало:

| Кадры k0…k7 | Ширины HD, px |
|---|---|
| Девастатор | 135, 131, 95, 136, 125, 134, 91, 129 |
| Корпус Осадного | 99, 108, 87, 113, 96, 111, 85, 108 |

`F = 1.205373515108`. Текущий пак и сохранённые кадры пробы дали одинаковые значения. Источник чисел — [.tmp/u9-siege-bbox-comparison.txt](/srv/dune/worktrees/u9f/.tmp/u9-siege-bbox-comparison.txt).

Применить один `F` к существующим масштабам обеих деталей:

- Корпус: `0.978410 × F = 1.179349500917`.
- Башня: `0.952726 × F = 1.148390687555`.

Коэффициент D дополнительно не применять: Р28 заменяет его для Осадного. Общий коэффициент сохраняет нынешнее соотношение размеров корпуса и башни. Правило задаёт сходство по медиане направлений; равенство ширин в каждом направлении не требуется.

Оценка увеличенных рамок — 136.21 × 125.36 для корпуса и 108.48 × 98.84 для башни. Это оценка, а не доказательство отсутствия обрезки полупрозрачных краёв. Новый `build` должен закончиться `all frames pass`; автоматически уменьшать выбранный размер через `"fit"` не предлагаю.

**Установка.** В [redraw_pack.py:73](/srv/dune/worktrees/u9f/tools/units3d/redraw_pack.py:73) сейчас требуется равенство новому PNG и старому атласу. В [install.py:23](/srv/dune/worktrees/u9f/tools/units3d/install.py:23) собственной проверки размеров сейчас нет.

Вынести общее правило размеров в новый `tools/units3d/atlas_geometry.py` и применять перед записью в обоих путях:

- Только пять имён из задания допускают переход 1152 × 152 → 1408 × 176.
- Повторная установка 1408 × 176 поверх 1408 × 176 поддерживается.
- Для остальных имён размер PNG обязан совпадать с исходной записью.
- Сохранить сверки манифеста, SHA-256, списка записей и неизменности чужих payload: [redraw_pack.py:59](/srv/dune/worktrees/u9f/tools/units3d/redraw_pack.py:59), [100](/srv/dune/worktrees/u9f/tools/units3d/redraw_pack.py:100).

### 3. Контракт и проверки атласов

Источник размеров — метаданные движка; фактические размеры атласов берутся из целевого пака.

В `unit_contract.py` изменить:

- [Регулярное выражение назначений, строка 29](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:29): читать новые HD-поля.
- [parse_unit_records, строка 254](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:254): сохранить логические и HD-размеры вместе с настоящими ссылками на источник.
- [build_entries, строка 1041](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:1041): `frame_classic` оставить прежним; `frame_hd4` брать из переопределения либо прежнего произведения на плотность.
- [parse_draw_geometry, строка 734](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:734), [source_rectangle, строка 901](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:901), [draw_destination, строка 922](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:922): описать обе ветви рисования и отдельную логическую рамку. Ссылки должны вести на исполняемый код, без добавления строк ради парсера.

Перегенерировать:

- [UNIT_CONTRACT.md](/srv/dune/worktrees/u9f/docs/units/UNIT_CONTRACT.md:28): строки пяти записей сейчас находятся на 28–30 и 51–52.
- [unit_contract.json](/srv/dune/worktrees/u9f/docs/units/unit_contract.json:5126): записи `UNIT_SIEGEBASE`, `UNIT_SIEGEBASE_SHADOW`, `UNIT_SIEGETOP`, `HM_UNIT_SIEGEBASE`, `HM_UNIT_SIEGETOP`, производный список исключений и правила рисования.

У пяти записей результат: `frame_classic=[36,36]`, `frame_hd4=[176,176]`, `hd4_size=[1408,176]`, сетка 8 × 1, остаток `[0,0]`. У остальных записей размеры остаются прежними; номера строк ссылок могут измениться вслед за кодом.

[check_unit.py:385](/srv/dune/worktrees/u9f/tools/units3d/check_unit.py:385) уже берёт геометрию из профиля, сверяет её с контрактом и PNG. [Проверка пака](/srv/dune/worktrees/u9f/tools/units3d/check_unit.py:456) уже требует неизменности записей вне выбранного набора. Производственную логику `check_unit.py` менять не требуется: новый размер проходит для Осадного через обновлённый контракт, а попытка присвоить его другому юниту расходится с контрактом другого юнита. Добавляются соответствующие приёмочные случаи.

### 4. Тесты и старые ожидания

Поиск выполнен по всем найденным тестам в `tests/`, `tools/units3d/tests/`, `tools/upstream/tests/`:

```sh
rg -n '144|152|1152' tests tools/units3d/tests tools/upstream/tests
rg -n 'frame_hd4|frame_classic|density|\* *4|4 *\*|× *4|4x' tests tools/units3d/tests tools/upstream/tests
rg -ni 'siege|siegetank' tests tools/units3d/tests tools/upstream/tests
```

Полная выжимка — [.tmp/u9-old-test-expectations.md](/srv/dune/worktrees/u9f/.tmp/u9-old-test-expectations.md).

**Ожидания, которые меняет отдельный исполнитель приёмочных тестов:**

| Проверка | Новое ожидание |
|---|---|
| [test_unit_contract.py:206](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:206) | Для пяти явно перечисленных имён HD-кадр 176 × 176 при классическом 36 × 36. Для всех остальных остаётся `frame_classic × 4`. |
| [test_unit_contract.py:271](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:271) | Фиксированное ожидание `UNIT_SIEGEBASE`: атлас `[1408,176]`, кадр `[176,176]`, остаток `[0,0]`, столбцов 8. Распространить положительную проверку новой геометрии на все пять записей. |

Других жёстких ожиданий старой геометрии Осадного не найдено. Связанные динамические проверки сохранить:

- [Сетка, строки 238–247](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:238): для пяти записей получится 8 × 1 без остатка.
- [Набор исключений, строки 249–267](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:249): индексы 151–153 остаются исключениями из равенства размеров атласа `classic × 4`; индексы 213–214 выходят из списка, поскольку классической картинки маски нет, а остаток исчезает.
- [Совпадение масок, строки 329–340](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:329): маски и окрашиваемые атласы равны 1408 × 176.
- [Генерация документов, строка 845](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:845): документы воспроизводятся из нового кода и целевого пака.
- [Инвентарь и размеры, строки 876–907](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:876): пять PNG имеют новый размер; классический пак остаётся прежним.

Не менять ожидания Девастатора [на строках 278–280](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:278), Carryall [на строках 289–312](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract.py:289), синтетические размеры `test_check_unit.py` и синтетических тестов `redraw`. Совпадения `1440`, размеров render target, каналов цвета и десятичных коэффициентов к кадру Осадного не относятся. Старых проверок универсальной формулы `source_rectangle`, `draw_destination` или `draw_order` не найдено.

**Новые проверки CTest:**

- `unit_sprite_layout`: исходные прямоугольники всех направлений и строк; 176 физических пикселей при плотности четыре; отдельное направление башни; точный центр назначения; неизменный результат при отсутствии HD-размеров и в классике.
- `unit_frame_interactions`: настоящий юнит сохраняет `getVisualRectangle`, полосы, `FOCUS`, группу, опыт, путь отладки, выбор щелчком и рамкой. Графический выступ не расширяет выбор.
- `unit_render_pixels`: реальный путь `cUnit::draw`, окраска Дома и SDL-рисование. Контрольные метки на границах кадров обнаруживают старый шаг, обрезку, перепутанное направление и неправильный размер маски.

Предлагаемые файлы — `tests/UnitSpriteLayoutTests.cpp`, `tests/UnitRenderPixelsTests.cpp` и `tests/UnitRenderFixture.cmake`. Приёмочный исполнитель регистрирует тесты в `CMakeLists.txt`.

Для попиксельного сравнения использовать один и тот же fixture на исходниках `bb2f1b37` и на новой версии, одинаковые паки и один программный SDL-рендерер. Сравнивать прочитанные RGBA-буферы без допуска:

- Осадный в классике и остальные юниты в обеих графиках.
- Используемые строки анимации, направления тела и независимые направления башни.
- Цвета Домов, поддерживаемые масштабы мира, зумы с целыми и дробными результатами, позиции с разной чётностью координат.
- НПЗ с харвестером, carryall, иконки и частицы смерти — отдельные неизменяемые случаи.

Эталонные результаты получать в `.tmp/` из закреплённого коммита, а не из формул нового helper. Сравнение выполнять внутри каждой платформы; равенство разных SDL-бэкендов между платформами не требуется. Помимо пиксельной матрицы, сохранённый старый путь должен передавать прежние `src/dest` без изменения округлений.

**Новые Python-проверки** в `test_siege_frame.py` и `test_install_geometry.py`:

- Старые crop, bbox и медиана используют 144 × 152 и `M=152`.
- Новый выход — пять атласов 1408 × 176; перенос якоря `(16,16)`; корпус и маска совмещены; обрезка проверяется после окончательного сдвига.
- Описание без новых полей воспроизводит прежние атласы остальных юнитов попиксельно.
- `pack` и прямой `install.py` принимают новый размер только для пяти имён, отклоняют неверный размер другого юнита до записи, поддерживают повторную установку.
- Чужие payload, порядок, имена и расширения записей не меняются.
- `check_unit` принимает согласованную геометрию Осадного и отклоняет ту же подмену для другого юнита.

Команды последующей задачи:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.tmp/unittest-tmp" \
D2TM_PACK_DIR="$PWD/resources/bin/data" \
/srv/dune/venv/bin/python -m unittest discover -s tools/units3d/tests -v

SDL_VIDEODRIVER=dummy ctest --test-dir .tmp/build-u9 \
  --output-on-failure
```

Проверки контракта запускаются с **целевым паком**, не со старым `/srv/dune/inputs/packs`.

Если после правок упадёт любая другая старая проверка, исполнитель оформляет `Q-U9-frame-NN` с именем теста и строкой вывода. Её ожидание не меняется автоматически.

### 5. Сборка и прогон на servak

Корневой [CMakeLists.txt:87](/srv/dune/worktrees/u9f/CMakeLists.txt:87) безусловно требует SDL2; SDL3 из `/srv/dune/deps/prefix` его не заменяет. Кроме того, [CONFIGURE_FILE](/srv/dune/worktrees/u9f/CMakeLists.txt:31) пишет `src/include/config.h`, поэтому корневую конфигурацию в режиме только плана не запускал.

Без SDL2 доступны:

- Python-сборка атласов, упаковка копии пака, генерация контракта и Python-тесты.
- Новый независимый расчёт геометрии и его C++-тест через временный CMake harness.
- Существующие расчётные тесты без SDL-зависимостей.

Сохранённый прогон [.tmp/u9f-ctest.log](/srv/dune/worktrees/u9f/.tmp/u9f-ctest.log) содержит:

```text
100% tests passed, 0 tests failed out of 4
```

Это `render_scale_calculations`, `world_scale_selection`, `world_object_scale_selection`, `hd_presentation_selection`. Последний собран с временным минимальным определением `SDL_Rect`; результат не доказывает работоспособность SDL-рендера.

Полный движок, подготовка текстур Домов, интеграционные проверки выбора и RGBA-сравнение требуют настоящих SDL2, SDL2_image, SDL2_ttf и SDL2_mixer. На servak они выполняются только после отдельного разрешения владельца на получение зависимостей. В этой задаче ничего не устанавливать и не скачивать.

Рекомендую добавить запуск CTest в четыре задания [build_pr.yml](/srv/dune/worktrees/u9f/.github/workflows/build_pr.yml:1): Windows, Ubuntu, macOS ARM и macOS Intel. Сейчас эти задания собирают программу, но не запускают CTest. Для проверки настоящих атласов нужен LFS checkout. Базовый образец сборки и тестирования уже есть в [release.yml](/srv/dune/worktrees/u9f/.github/workflows/release.yml:258). Python-проверки можно выполнить на servak; SDL-проверки должны быть зелёными в CI до слияния.

### 6. Порядок, исполнители и коммиты

Чтение движка, инструмента и контракта выполнено тремя субагентами `gpt-6-luna` `xhigh`. Поиск старых ожиданий и измерение сохранённых кадров выполнены отдельным субагентом с той же моделью. Повторной сборки после ответа ведущего не было. При реализации механические правки и прогоны передаются Luna; выбор механизма, сверка поведения и итог остаются у основного исполнителя.

**Один PR** должен включать движок, инструмент, разрешённые изменения приёмочных тестов, новый пак и перегенерированный контракт. Не сливать новый пак раньше поддержки кадра движком или отдельно от масок и башни.

Предлагаемый список коммитов для ведущего; тестовые файлы и изменения старых ожиданий готовит отдельный исполнитель:

**1.**
```text
test: define independent HD unit frame behavior

Behavior changes: none
```

```text
tests/UnitSpriteLayoutTests.cpp
tests/UnitRenderPixelsTests.cpp
tests/UnitRenderFixture.cmake
tools/units3d/tests/test_siege_frame.py
tools/units3d/tests/test_install_geometry.py
tools/units3d/tests/test_unit_contract.py
CMakeLists.txt
.github/workflows/build_pr.yml
```

Зафиксировать красные результаты новых требований до производственных правок. Независимый эталон — `bb2f1b37`.

**2.**
```text
feat: draw HD unit frames independently of logical bounds

Behavior changes: HD Siege Tank uses its own frame size and remains centered; logical bounds remain unchanged
```

```text
src/include/structs.h
src/utils/cIniGameRessouces.cpp
src/utils/UnitSpriteLayout.hpp
src/gameobjects/units/cUnit.cpp
src/drawers/SDLDrawer.hpp
src/drawers/SDLDrawer.cpp
```

**3.**
```text
feat: support resized Siege atlases in unit tools

Behavior changes: unit tools support separate reference and output frames; only the five Siege entries may change atlas size
```

```text
tools/units3d/redraw_common.py
tools/units3d/redraw_build.py
tools/units3d/redraw_shadow.py
tools/units3d/redraw_sheets.py
tools/units3d/redraw_pack.py
tools/units3d/install.py
tools/units3d/atlas_geometry.py
tools/units3d/unit_contract.py
```

**4.**
```text
assets: update Siege frames and generated unit contract

Behavior changes: HD Siege Tank artwork uses 176 by 176 frames and the approved Devastator-relative scale
```

```text
tools/units3d/units/UNIT_SIEGEBASE/unit.json
tools/units3d/units/UNIT_SIEGETOP/unit.json
resources/bin/data/sdl_data_hd4.dat
docs/units/UNIT_CONTRACT.md
docs/units/unit_contract.json
```

Сначала собрать корпус и башню в отдельных каталогах `.tmp/`, затем установить обе группы в одну копию пака, проверить все пять записей и неизменность остальных payload. Контракт генерировать из окончательной копии пака. После Python-проверок и SDL-проверок CI ведущий получает весь PR для приёмки. Коммиты здесь не создаются.

### 7. Чего план не закроет

- Новую модель, новую камеру и доказательство физической длины модели в метрах. Для имеющихся перерисовок предложено измеримое правило сходства с Девастатором.
- Новую раскладку цвета Дома по Р28. Маски получают новый размер и сохраняют совмещение; художественное изменение доли окраски — отдельная работа.
- Изменение частиц смерти, иконок, мини-карты и поведения carryall.
- Расширение выбора или отсечения по графическому выступу. Прежний viewport-прямоугольник сохраняется; картинка, выступающая за него, не расширяет условие видимости.
- Полную 3D-приёмку с provenance: в рабочей копии отсутствует каталог `resources/hd/units3d`; геометрические проверки `check_unit` проверяются на согласованных тестовых данных.
- Установку SDL2, публикацию, открытие PR и слияние.

Уточнение к формулировке про «область щелчка 36 × 36»: фактически код выбирает ячейку карты, а рамочное выделение проверяет центр. План сохраняет эти алгоритмы и логические размеры 36 × 36, не вводя новый hitbox.

### Не проверено

- Новый код и атласы 176 × 176 ещё не созданы.
- Предложенные масштабы не проходили новый `build`; оценки bbox не исключают обрезку полупрозрачных краёв.
- Полный Python-прогон был остановлен до завершения и после ответа ведущего не возобновлялся.
- SDL2-сборка, попиксельное сравнение и CI четырёх платформ не выполнялись.
- Коммит `5d52bf53` отсутствует среди доступных локальных объектов; дополнение к заданию принято из сообщения ведущего.

### git status --short

Вывод пуст.

**Остановка до `PLAN-OK-U9-frame`.**