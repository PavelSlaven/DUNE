ACCEPT

# Приёмка третьего круга Codex A1, проверяющий — Claude Opus

Объект проверки: `/srv/dune/worktrees/a1`, ветка `codex/a1`, HEAD `39a88806`, четыре неотслеживаемых файла. Их sha256 совпадают с копией `files3`:
- `tools/units3d/unit_contract.py` — `e0648fbf…`, 1788 строк;
- `tools/units3d/tests/test_unit_contract.py` — `60c50409…`, 929 строк;
- `docs/units/unit_contract.json` — `2cdbdc94…`;
- `docs/units/UNIT_CONTRACT.md` — `12bd395b…`.

Я сам читал код, JSON, MD и исходники движка. Отчёту исполнителя не доверял. То, что ведущий уже проверил скриптом `check3.py`, не повторял.

## Итог

Все девять пунктов `answer-02.md` закрыты по существу. Цепочка «где рисуется кадр» верна: каждое звено подтверждено строкой кода, утверждений сверх кода нет. Условие HD-пути и ссылка тени на исполняемую строку `cPlayer.cpp:587` на месте. Ветка «неразобранное место отрисовки» действительно падает. `SourceIndex.ref` отсеивает и `//`, и `/* … */`. Все 7 проверок задания есть, проверки 2–7 вынесены в функции `(contract, markdown)`. Все пять мутаций задания и ещё 10 моих краснеют. Рамка: ровно четыре пути.

Нашёл пять замечаний, все уровня Н. Ни одно не касается полей, которые читает A2b: `name`, `role`, `unit_types`, `frame_hd4`, `hd4_size`, `columns`, `column_meaning`, `house_mask`, `light.median_angle_degrees`.

## Находки

Важность: **В** — мешает A2b или неверный факт; **С** — исправить до слияния; **Н** — косметика, не блокирует приёмку.

1. **Н** — `tools/units3d/unit_contract.py:190–205` (`source_call_refs`), `:614–674` (`parse_draw_sites`). Причина — исполнитель.
   - **Что не так.** Место отрисовки молча теряется в двух случаях:
     - вызов `getUnit*Bitmap(` перенесён на следующую строку: регулярное выражение работает по одной строке;
     - вызов без `.` или `->` перед именем, например `return getUnitBitmap(TANK);` внутри метода `cPlayer`.
   - **Проверка.** На копии дерева такие вызовы дают exit 0, а вывод побайтно равен базовому (пробы D и F).
   - **Похожая слабость.** `parse_unit_records` (`:257`, `source.lines`) и `parse_structure_specs` (`:1254`, `source.text`) разбирают сырой текст. Закомментированное присваивание `sUnitInfo[...]` стало бы значением.
   - **Асимметрия в тесте.** `_strip_cpp_comments` в тесте применяется и к `.py`/`.json`, а скрипт снимает комментарии только у `.cpp`/`.h`/`.hpp`.
   - **Сейчас вреда нет.** В `src/` все четыре вызова однострочные и через `.` (`cUnit.cpp:784/810/827`, `cStructureDrawer.cpp:859`), закомментированных присваиваний полей `bmp|top|shadow|bmp_width|bmp_height` нет.
   - **Ожидается.** Разбор вызова, перенесённого на следующую строку, и неквалифицированного вызова — либо ошибка генерации; разбор присваиваний по тексту без комментариев.

2. **Н** — `docs/units/unit_contract.json` → `draw_rules.hd_house_masks.value` (генератор `unit_contract.py:955–976`). Причина — исполнитель.
   - **Что не так.** Два утверждения повторены под разными ключами, а задание (раздел 2) требует «каждое — один раз»:
     - порядок поиска маски есть в `mask_lookup_order` и ещё раз в последнем предложении `mask_name_selection` («HM_<selectedName>/HOUSEMASK_<selectedName> ищется первым; HM_<baseName>/… только если selectedIndex != baseIndex»);
     - формула яркости `(0.299*r + 0.587*g + 0.114*b) / 128` есть в `average_luminance_pixels` и в `pixel_luminance`.
   - **Ожидается.** Оставить каждое утверждение под одним ключом.

3. **Н** — `draw_rules.hd_house_masks.value.mask_name_selection`. Причина — исполнитель.
   - **Что не так.** Текст «Иначе selectedName берётся из доступного HV_<code>_<base>, затем HOUSEVARIANT_<house>_<base>…» неточен для нейтральных HD-зданий `BUILD_*` со встроенными деталями (13 имён allowlist). По `Graphics.cpp:270–276` варианты ищутся только при `!neutralHdStructure`. У этих зданий маска ищется, но `selectedName` всегда равен `baseName`.
   - **Сейчас вреда нет.** В `sdl_data_hd4.dat` нет ни одной записи `HV_*` или `HOUSEVARIANT_*`. Юнитов это не касается: у них `neutralHdStructure` ложно.
   - **Ожидается.** Выбор варианта зависит только от `neutralHdStructure`, поиск маски — от `!neutral || embedded`.

4. **Н** — `draw_rules` (генератор `unit_contract.py:766–794`, `:922–948`). Причина — исполнитель.
   - **Что не так.** Все утверждения цепочки верны, но несколько связующих звеньев не названы и не сопровождены ссылкой:
     - `visualScale = unitWorldScaleFactor(...)` (`cUnit.cpp:540`): `visual_rectangle` говорит о `visualScale`, а `unit_world_scale_factor` — о `unitWorldScaleFactor`, но прямо они не связаны;
     - переход `draw_x()` → `draw_x(getBmpWidth())` (`cUnit.cpp:507`, `:522`) и то, что `getBmpWidth()` = `sUnitInfo[iType].bmp_width` (`cUnit.cpp:597–599`);
     - «размер берётся из visual.getWidth()» — ссылка ведёт на `:795` (`roundedScaledWidth,`), а не на присваивание `:786`;
     - `hd4_density` ссылается на `srcRect.w/h` (`SDLDrawer.cpp:87–88`), но не на `srcRect.x/y` (`:85–86`).
   - **Ожидается.** Добавить эти звенья и ссылки.

5. **Н** — рабочая копия, игнорируемые файлы. Причина — исполнитель.
   - **Что не так.** Остались `tools/__pycache__/hd_assets.cpython-313.pyc` (21:48) и `tools/units3d/__pycache__/unit_contract.cpython-313.pyc` (22:04). Их оставили прогоны исполнителя без `PYTHONDONTWRITEBYTECODE`: тест `unit_contract` не импортирует. В `git status` их нет (они в ignore), на коммит не влияют. Второй файл попал и в копию `files3`.
   - **Ожидается.** Удалить их при уборке перед коммитом.

## Ответы по пунктам брифа

### 1. Пункты 1–9 `answer-02.md` закрыты по существу

- **П. 1, `sega_reference`.**
  - `parse_sega_asset_specs` (`:451–519`) разбирает `UNITS` через `ast`: позиционные аргументы — по порядку `AnnAssign` класса `AssetSpec`, именованные — по имени.
  - Лист не из manifest или повтор `symbol` — ошибка с именем.
  - `body`/`top` — по `symbol` (`:1143–1146`), `shadow` — от единственного `body` с тем же `unit_types` (`:1210–1226`), ноль или больше одного — ошибка с именем. Маски — от `painted_entry` (`:1243`).
  - Разбора подстрок и `sega_reference_note` нет. Значения сверил ведущий.
- **П. 2, ссылка тени.** `function_ref` внутри `Texture *cPlayer::getUnitShadowBitmap(int index)` даёт `cPlayer.cpp:587` (`if (sUnitInfo[index].shadow) {`), это исполняемая строка. Комментарий `:566` пропущен.
- **П. 3, тесты.** Проверки 2, 4–7 — функции модуля, мутации краснеют (п. 5 ниже).
- **П. 4, пустые присваивания и неразобранные места.**
  - Пустых присваиваний и повторного расчёта нет. У масок `facing_source = None` и `sites = []` — только начальные значения, позже наследуются от `painted_entry` (`:1241–1242`).
  - Неразобранное место отрисовки — `ValueError` с `путь:строка` (`:651–652`, `:663–664`, `:672–674`), подтверждено пробой.
  - Значения `column` и `row` у мест в `cUnit::draw` — текст `"convertAngleToDrawIndex(iBodyFacing|iHeadFacing)"` и `"iFrame"`. Они записаны литералами, но совпадают с `cUnit.cpp:775–780`.
- **П. 5, `yaw` и пехота.**
  - `yaw_step = 360 // facing_count`, где `facing_count` разобран из умолчания `maxFacings = 8` объявления `convertAngleToDrawIndex` (`:344–352`, `:408–411`); `column * 45` нет.
  - Пехота — `parse_infantry_assignments` по тексту без комментариев: SOLDIER, INFANTRY, TROOPER, TROOPERS, UNIT_FREMEN_ONE, UNIT_FREMEN_THREE, SABOTEUR — все 7 присваиваний `cIniGameRessouces.cpp:365–512`.
- **П. 6, цепочка.** Полная, см. п. 2 ниже. В MD первая ссылка у `draw_x` — `cUnit.cpp:515`, у `draw_y` — `cUnit.cpp:528`.
- **П. 7, медиана.** Круговая медиана (`:1534–1543`), выбросы считаются от неё (`:1545–1548`), оба определения записаны в `light.measurement`.
- **П. 8, временные файлы.** Тест пишет только в `tempfile.TemporaryDirectory()` (`test:846`), в `ROOT/.tmp` ничего не пишет.
- **П. 9, маски.**
  - `texture_path`: условие `m_hdTextureReferences = gfxdata->getDensity() > 1` (`cPlayer.cpp:274`), иначе `createTextureFromIndexedSurfaceWithPalette` (`:285`), со ссылками.
  - Отдельного ключа `BUILD_*_SHADOW` больше нет. Остаточные повторы — находка 2.

### 2. Цепочка «где рисуется кадр»

Все звенья сверены с кодом, каждое ссылается на свою строку:

| Звено | Строки | Что в коде |
|---|---|---|
| `draw_x` | `cUnit.cpp:515`, `:517`, `cMapCamera.h:82` | `bmpOffset = (TILESIZE_WIDTH_PIXELS - bmpWidth) / 2`; `getWindowXPositionWithOffset(pos_x(), bmpOffset)` = `round(factorZoomLevel((x - m_viewportStartX) + offset))` |
| `draw_y` | `:528`, `:529`, `cMapCamera.h:93` | то же, плюс `m_heightOfTopBar` |
| `visual_rectangle`, `visual_rectangle_y` | `:535/538`, `:546/549`, `:552/553` | `lround`, масштаб `visualScale`, сдвиг на `(visual − original) / 2` |
| `unit_world_scale_factor` | `:541`, `WorldObjectScale.hpp:29` | возвращает `worldScaleFactor` без изменений |
| `world_scale_configuration` | `cGame.h:295–297` | при HD — `m_effectiveWorldScalePercent / 100`, иначе `1.0F` |
| `draw_destination` | `:785`, `:792`, `:795` | `visual = getVisualRectangle()`, `dest = {visualX, visualY, w, h}` |
| `draw_order` | `:806`, `:819`, `:839` | порядок: тень → корпус → башня |
| смещение тени `CARRYALL` | `:801` | `visualY + 24` |

Фраза «с целочисленным округлением центр остаётся у `draw_x() + originalWidth / 2`» верна с точностью до 0,5 px от целочисленного деления. Утверждений, которых код не говорит, нет; неназванные связки — находка 4.

### 3. `draw_rules.hd_house_masks`

- Условие HD-пути верно. `cPlayer.cpp:274` присваивает флаг, `:277–285` выбирает между `getHouseTexture` и палитровым путём.
- Ссылка тени ведёт на исполняемую строку `:587` внутри `getUnitShadowBitmap`.
- Формулы силы окраски, пропуска пикселя, пропуска всей маски по размеру и порядок поиска совпадают с `Graphics.cpp:243–301` и `:378–454`.
- Повторы — находка 2, неточность про нейтральные здания — находка 3.

### 4. Код

- `yaw` берётся из разобранного `max_facings`, пехота — из присваиваний `.infantry = true`.
- **Ветка ошибки падает** (пробы на копии дерева в `/tmp/a1-review3/`):
  - B: `players[0].getUnitBitmap(TANK)` в `cStructureDrawer.cpp` → `ValueError: …cStructureDrawer.cpp:1038: unparsed getUnitBitmap draw site for 'TANK'`, exit 1;
  - C: `players[0].getUnitTopBitmap(iType)` вне `cUnit::draw` → `ValueError: …cUnit.cpp:4795: unknown getUnitTopBitmap argument 'iType'`, exit 1;
  - G: аргумент `unit[id].getType()` → `ValueError … unknown …`, exit 1;
  - E: закомментированный вызов игнорируется, exit 0 — верно.
  - Пробелы D и F — находка 1.
- **`SourceIndex.ref`**:
  - `ref("src/player/cPlayer.cpp", "if (sUnitInfo[index].shadow)")` возвращает `:587`;
  - якорь из строки `// Path creation definitions` (`cUnit.cpp:38`) — `ValueError`;
  - якорь из блока `/** … */` (`cPlayer.cpp:559`) — `ValueError`.

### 5. Тесты

- **8 тестов.** Генерация с побайтным сравнением, инвентарь паков и шесть функций `check_*(contract, markdown)`: 2 — сетка и `size_exceptions`, 3 — маски, 4 — ссылки, 5 — направления, 6 — Sega, 7 — MD и свет.
- **Состав 14 тестов второго круга** (по `baseline.log`) слит в эти функции без потери покрытия задания.
- **Известные случаи на месте:**
  - `UNIT_SIEGEBASE` и `UNIT_DEVASTATOR`: `hd4_size`, `frame_hd4`, `remainder_px`, `columns` (`test:270–287`);
  - Sega: все 12 случаев задания плюс 10 согласованных с `UNITS` (`test:642–670`).
- **Мутационный скрипт исполнителя.** Импортирует `check_*` из модуля теста и вызывает их на `deepcopy` JSON. Его копия в `/tmp/a1-review3/exec_mutations.py` (изменён только `ROOT`) дала 6 строк `PASS: … rejected -> AssertionError`, exit 0.
- **Мой набор** `/tmp/a1-review3/my_mutations.py`. Сначала все 6 функций зелёные на файлах сдачи. Затем каждая мутация краснеет с нужным сообщением:
  - мутации задания:
    - все `direction` = null → «every directional column needs a direction and yaw»;
    - `UNIT_LAUNCHER.sega_reference` = null → «sega_reference must not be null»;
    - ссылка на `cPlayer.cpp:566` (`//`) → «identifier is absent from executable source»;
    - пустой MD → «Markdown contract is empty»;
    - `UNIT_SIEGEBASE.frame_hd4` = `[144, 152]` → «frame_hd4 must be four times frame_classic»;
  - дополнительно:
    - ссылка внутрь `/* */`;
    - `yaw` +45;
    - перевёрнутый `draw_rules.direction_columns`;
    - чужой лист у `UNIT_SIEGEBASE`;
    - `UNIT_SIEGEBASE` удалён из `size_exceptions`;
    - строка MD удалена;
    - строка MD повторена;
    - правило `draw_y` удалено из MD;
    - медиана +1°;
    - перевёрнутый флаг `outlier`.
  - Итог: 15/15 RED.
- **Красные прогоны.**
  - В `red.log` на артефактах второго круга упали тесты 4, 3, 7, 6. Тесты 2 и 5 там зелёные: эти поля во втором круге были верны.
  - В `red_seeded.log` все 8 упали на мутированных артефактах.
  - По `progress.md` исполнитель мутировал файлы сдачи на месте и восстановил их. Побайтное равенство подтверждает тест 1 и моя генерация в A.
- **Корень репозитория.** Тест в него не пишет: только `TemporaryDirectory`, JSON и MD лишь читаются. После всех моих прогонов `git status --short --ignored --untracked-files=all` не изменился.

### 6. Рамка

`git status --short --untracked-files=all` показывает ровно четыре пути `??`: оба файла `docs/units/` и оба файла `tools/units3d/`. `git diff --stat` пуст. Игнорируемые файлы: `.tmp/*` (логи исполнителя) и два `__pycache__` (находка 5).

## Выводы команд

```
git rev-parse HEAD → 39a88806f4a4260b5b303a781448189e672f59f3; branch codex/a1
git status --short --untracked-files=all → ?? docs/units/UNIT_CONTRACT.md, ?? docs/units/unit_contract.json,
  ?? tools/units3d/tests/test_unit_contract.py, ?? tools/units3d/unit_contract.py
sha256 сервер = files3 (все четыре)
grep getUnit*Bitmap src/ → вызовы: cUnit.cpp:784, 810, 827; cStructureDrawer.cpp:859 (остальное — объявления/определения)
probe A (копия дерева без правок) → exit 0, JSON и MD побайтно равны сданным
probe B → ValueError: src/drawers/cStructureDrawer.cpp:1038: unparsed getUnitBitmap draw site for 'TANK'
probe C → ValueError: src/gameobjects/units/cUnit.cpp:4795: unknown getUnitTopBitmap argument 'iType'
probe D (перенос строки) / F (без '.') → exit 0, вывод = базовый
probe_index.py → ref shadow cPlayer.cpp:587; комментарные якоря → ValueError; max_facings 8, yaw 0…315
exec_mutations.py → 6 × PASS … rejected -> AssertionError
my_mutations.py → baseline 6/6 pass; 15/15 RED; exit 0
HD4 pack: записей HV_* / HOUSEVARIANT_* — 0
status до/после моих прогонов (включая ignored) — без изменений
```

Временные файлы — `/tmp/a1-review3/`: скрипты `exec_mutations.py`, `my_mutations.py`, `probe_index.py`, логи `log_A…G.txt`, `status_before.txt` и `status_after.txt`. Копии дерева удалены.
