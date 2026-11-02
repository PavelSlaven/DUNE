# Задание U9-I — реализация HD-кадра 176 × 176 Осадного танка

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце): план работы уже одобрен ведущим, ты не стоишь до ответа на план. Исполнитель: Codex `gpt-6.1-sol` `high`; помощники — субагенты `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u9f`, ветка `codex/u9-frame`, HEAD `cf757ad72f04515c8d91bf384cd0af11001574a6`. Коммитов не делай: ведущий коммитит по списку из сдачи.

## Цель

Правки движка, инструмента перерисовки, контракта и пака по одобренному плану `codex-direct/U9/PLAN-frame.md` с поправками `codex-direct/U9/PLAN-OK-frame.md`, после которых все приёмочные тесты ветки `codex/u9-frame` проходят, а замороженные файлы тестов не изменены: в графике HD Осадный танк рисуется из кадров 176 × 176 по центру своей логической рамки 36 × 36, а всё остальное рисуется как в коммите `bb2f1b37`.

## Источник истины

- Поведение — `codex-direct/U9/TASK-frame.md`, раздел «Поведение, которого надо добиться», пункты 1–6.
- Способ — `codex-direct/U9/PLAN-frame.md`, разделы 1–5 и коммиты 2–4 раздела 6. Поправки `codex-direct/U9/PLAN-OK-frame.md`, пункты 1–6, сильнее плана; там, где план и поправки расходятся, делай по поправке.
- Интерфейс для тестов — пункт 6 файла `codex-direct/U9/PLAN-OK-tests.md`: типы и функции `UnitSpriteFrame`, `UnitSpriteRectangle`, `UnitSpriteFloatRectangle`, `resolveUnitSpriteFrame`, `unitSpriteSourceRectangle`, `unitSpriteDestinationRectangle` из раздела 2 файла `codex-direct/U9/PLAN-tests.md` и метод `SDLDrawer::renderStrechSpriteF(Texture *, cRectangle, SDL_FRect, Uint8 = 255, SDL_BlendMode = SDL_BLENDMODE_BLEND)`. У типов без HD-кадра и у Осадного в классике `cUnit::draw` вызывает `renderStrechSprite` с теми же аргументами, что в `bb2f1b37`; `renderStrechSpriteF` — только у слоёв с HD-кадром. Определения функций `UnitSpriteLayout.hpp` — в заголовке или в новом `src/utils/UnitSpriteLayout.cpp`, выбери одно.
- Приёмочные тесты — 16 файлов ниже, они уже в ветке. Их суммы — файл `/srv/dune/tasks/u9-impl/frozen.sha256`.
- Перекраски для цвета Дома (поправка 2 `PLAN-OK-frame.md`): у кадра k — `units-gen/UNIT_SIEGEBASE/siegebase_recolour9_k<k>.png` и `units-gen/UNIT_SIEGETOP/siegetop_recolour9_k<k>.png`. Папка `units-gen` рабочей копии — ссылка на `/srv/dune/gen`; суммы файлов — `codex-direct/U9/gen/UNIT_SIEGEBASE.SHA256SUMS` и `codex-direct/U9/gen/UNIT_SIEGETOP.SHA256SUMS`, ведущий сверил их 2026-11-02.

## Замороженные файлы

```text
tests/UnitDrawRecorder.cpp
tests/UnitDrawRecorder.hpp
tests/UnitDrawRegressionTests.cpp
tests/UnitFrameBaseline.hpp
tests/UnitFrameFixture.cpp
tests/UnitFrameFixture.hpp
tests/UnitFrameInteractionsTests.cpp
tests/UnitHdFrameDrawTests.cpp
tests/UnitRenderFixture.cmake
tests/UnitRenderPixelsTests.cpp
tests/UnitSpriteLayoutTests.cpp
tests/UnitTextRecorder.cpp
tools/units3d/tests/test_siege_frame.py
tools/units3d/tests/test_install_geometry.py
tools/units3d/tests/test_siege_contract.py
tools/units3d/tests/test_unit_contract.py
```

Эти файлы, `tools/units3d/tests/ACCEPTANCE.sha256` и остальные файлы `tests/` и `tools/units3d/tests/` не меняются. Регистратор вызовов (`tests/UnitDrawRecorder.cpp`) определяет только те методы `SDLDrawer` и `cTextDrawer`, определения которых есть в этом файле. Если реализация вызывает вне `SDLDrawer.cpp` метод, которого регистратор не определяет, — блок `## Q-U9-I-NN` с именем метода и стоп.

## Что сделать

1. **Движок** — коммит 2 плана: поля `hd_frame_width`, `hd_frame_height` структуры `s_UnitInfo` (`src/include/structs.h`), размеры HD-кадра Осадного в `src/utils/cIniGameRessouces.cpp`, `src/utils/UnitSpriteLayout.hpp` (и `.cpp`, если выбрал его), `cUnit::draw` в `src/gameobjects/units/cUnit.cpp`, метод `renderStrechSpriteF` в `src/drawers/SDLDrawer.hpp` и `src/drawers/SDLDrawer.cpp`. `getVisualRectangle()`, полоса здоровья, рамка выделения, выбор щелчком и рамкой не меняются (пункт 2 поведения).
2. **Инструмент** — коммит 3 плана: `tools/units3d/redraw_common.py`, `redraw_build.py`, `redraw_shadow.py`, `redraw_sheets.py`, `redraw_pack.py`, `install.py`, новый `atlas_geometry.py`, `unit_contract.py`. Описание юнита задаёт поля `reference_frame`, `reference_anchor`, `frame`, `atlas_size`; без этих полей инструмент работает как в `bb2f1b37`. Новый размер атласа `pack` и `install.py` принимают только у пяти записей Осадного: `UNIT_SIEGEBASE`, `UNIT_SIEGEBASE_SHADOW`, `HM_UNIT_SIEGEBASE`, `UNIT_SIEGETOP`, `HM_UNIT_SIEGETOP`.
3. **Описания, атласы, пак и контракт** — коммит 4 плана, после пункта 2:
   - `tools/units3d/units/UNIT_SIEGEBASE/unit.json` и `tools/units3d/units/UNIT_SIEGETOP/unit.json`: `reference_frame` [144, 152], `reference_anchor` [72, 72], `frame` [176, 176], `atlas_size` [1408, 176]; `scale` 1.179349500917 у корпуса и 1.148390687555 у башни; `recolour` кадра k — файлы перекрасок из раздела «Источник истины»; `share_corridor` [0.10, 0.45] у корпуса и [0.15, 0.60] у башни; значения `"fit"` нет;
   - сборка корпуса и башни командой `build` в отдельных папках `.tmp/`, затем установка обеих групп в одну копию пака `resources/bin/data/sdl_data_hd4.dat`. Если `build` обрезает силуэт при этих числах `scale` — блок `## Q-U9-I-NN` с номерами кадров и стоп; поле `"fit"` не вводить;
   - проверка копии пака скриптом: у пяти записей Осадного атлас 1408 × 176, у каждой другой записи payload побайтно равен payload пака `bb2f1b37`;
   - контракт `docs/units/UNIT_CONTRACT.md` и `docs/units/unit_contract.json` — генератором `tools/units3d/unit_contract.py` из окончательной копии пака.

## Чем проверить

- **Суммы.** `sha256sum -c /srv/dune/tasks/u9-impl/frozen.sha256` из корня рабочей копии и `sha256sum -c tools/units3d/tests/ACCEPTANCE.sha256` — все строки `OK`. Вывод — в сдаче.
- **Сборка и CTest.** Сборка по рецепту `/srv/dune/deps/sdl2/README.txt` в `.tmp/` (копия исходников рабочей копии, как в задаче U9-T1: шаг `configure` пишет `src/include/config.h` в исходники); `ctest --output-on-failure` по всем тестам. Ожидается: проверка `D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER` — `Success`; все тесты CTest проходят, у теста `unit_render_pixels` все восемь строк проверок — `PASS`.
- **Python.** `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.tmp/unittest-tmp" D2TM_PACK_DIR="$PWD/resources/bin/data" /srv/dune/venv/bin/python -m unittest discover -s tools/units3d/tests -v`. Ожидается: `OK`, пропущенных (`skipped`) — 0.
- **Пак.** Строки вывода скрипта проверки копии пака из пункта 3.
- **Чистота.** `git diff --check cf757ad7` — пусто.

## Что не трогать

- Замороженные файлы и всё в `tests/` и `tools/units3d/tests/`.
- `CMakeLists.txt`, `.github/`, атласы и описания юнитов, кроме двух описаний Осадного и пяти записей Осадного в паке.
- Листы и просмотр картинок не делай: листы новых кадров собирает ведущий.

## Организация работы

- Порядок: `create_goal` → журнал хода `.tmp/progress.md` → пункты 1 и 2 → пункт 3 → сборка и CTest, Python, суммы → самоаудит одним кругом → сдача.
- Параллельно: пункт 1 (C++) и пункт 2 (Python) не зависят друг от друга — отдай их двум субагентам `gpt-6-luna` `xhigh` одновременно; сборку C++ и CTest запускай, пока идёт пункт 3.
- Помощники: субагенты `gpt-6-luna` `xhigh` — правки по ясному описанию, прогоны, выжимки логов. Выбор механизма, сверка с планом и поправками, итог — твои.
- Остановки — блок `## Q-U9-I-NN` в сдаче и стоп:
  - замороженный тест падает на реализации, которая выполняет план, поправки и поведение `TASK-frame.md`, — имя теста и строка вывода;
  - падает старый тест вне списка замороженных файлов — имя теста и строка вывода;
  - реализация вызывает метод, которого регистратор не определяет;
  - `build` обрезает силуэт;
  - свободно меньше 5 ГБ на `/` (`df -BG /` перед сборкой и перед установкой в пак);
  - команда оболочки дважды подряд не завершилась и за 30 минут не дописала ни строки в свой журнал. Команда, которую оболочка вернула без кода выхода, пока процесс работает, — не сбой; пустой вывод при коде выхода 0 — не повод для остановки.
- Журнал хода: строка в `.tmp/progress.md` после каждого пункта «Что сделать» и после каждого прогона; ведущий читает его каждые 30 минут.
- Рамка правок: файлы коммитов 2–4 раздела 6 `PLAN-frame.md` и `src/utils/UnitSpriteLayout.cpp`, если выбрал его; временное — в `.tmp/`.
- Комментарии в коде. Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

## Сдача

Блок `## DONE-U9-I | <время UTC из date -u> | HEAD <sha>` по разделу «Сдача» правил ниже. В нём: `## PLAN-U9-I` для записи (кто какой пункт делал); строки вывода сумм, проверки `D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER`, итога CTest и восьми строк `unit_render_pixels`, итога Python, проверки пака; пути собранных атласов в `.tmp/` для листов ведущего; список коммитов 2–4 по разделу 6 плана; раздел «Не проверено»; раздел «Рабочие места» — что лежит в `.tmp/` и сколько места занимает; `git status --short`.
