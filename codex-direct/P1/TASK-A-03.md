# Задание P1A-03 — правки по предревью карты переноса

## Цель

Предревью sol нашло пять расхождений в коммите `33cb68f0`. Одно из них вызвано генератором. `UP1` объявляет индексы картинок как `constexpr int NAME = N;`, а `gfxmentat.h` и `gfxworld.h` перенёс в `src/include/`. Генератор понимает только `#define` в `src/data/`, поэтому `id_collisions` в `UP1` пуст, хотя настоящие конфликты индексов паков есть.

После этого задания:
- генератор находит эти конфликты;
- тест на это добавлен;
- карта и две причины исключений исправлены;
- все тесты проходят.

Рабочая копия — `/srv/dune/worktrees/u34`, ветка `codex/p1a`, HEAD `33cb68f0c88eb6b09ef86557f5eeade551e694fa`. `BASE`, `FORK1`, `UP1` — как в задании P1A.

## Шаги

1. **Вход.** `git rev-parse HEAD` равен `33cb68f0c88eb6b09ef86557f5eeade551e694fa`, `git status --short` без строк `.tmp/` пуст. Иначе — блок `Q-P1A-07` и стоп.
2. **Красный тест.** Добавь в `tools/upstream/tests/test_port_inventory.py` метод `test_pack_indices_are_read_from_constexpr_and_moved_headers`. Тест не читает Git и паки. Он вызывает функции модуля генератора `parse_defines`, `new_defines` и `pack_index_findings` на таких данных:
   - исходники базы: `{"src/data/gfxmentat.h": ["#define MENTAT_A 0"], "src/data/gfxdata.h": ["#define DATA_A 0"]}`;
   - исходники апстрима: `{"src/include/gfxmentat.h": ["constexpr int MENTAT_A = 0;", "constexpr int MENTAT_B = 1;"], "src/data/gfxdata.h": ["constexpr int DATA_A = 0;", "constexpr int DATA_B = 1;"]}`;
   - записи паков: `{"sdl_mentat_hd4.dat": {0: "MENTAT_A"}, "sdl_data_hd4.dat": {0: "DATA_A", 1: "HM_OTHER"}}`;
   - вызов: `pack_index_findings(new_defines(parse_defines(<база>), parse_defines(<апстрим>)), <записи паков>)`;
   - ожидаемый результат — ровно этот список:
     ```python
     [
         {"kind": "pack_index_taken", "header": "src/data/gfxdata.h", "pack": "sdl_data_hd4.dat", "define": "DATA_B", "value": 1, "fork_entry": "HM_OTHER"},
         {"kind": "pack_index_missing", "header": "src/include/gfxmentat.h", "pack": "sdl_mentat_hd4.dat", "define": "MENTAT_B", "value": 1, "fork_entry": None},
     ]
     ```
   
   Запусти только этот тест. Он должен упасть, потому что генератор возвращает пустой список. Лог — `.tmp/p1a/test-03-red.log`. Тест проходит до правки генератора или падает по другой причине — блок `Q-P1A-07` с выводом и стоп.
3. **Генератор** `tools/upstream/port_inventory.py`. Изменяются только функции `parse_defines`, `new_defines`, `id_collisions`, `pack_index_findings` и словарь `PACKS`, и только так:
   - `parse_defines` читает файлы, путь которых соответствует `src/(data|include)/gfx[^/]+\.h`. Кроме строк `#define NAME <число>` она распознаёт строки `constexpr int NAME = <число>;`; перед `constexpr` могут стоять `inline` и `static`. Число разбирается по тем же правилам, что сейчас для `#define`. Поле `path` записи — путь файла в его ревизии.
   - Заголовок определяется именем файла. `new_defines` и `id_collisions` сравнивают имена по имени файла заголовка, а не по полному пути: имя, которое в базе есть в `src/data/gfxmentat.h`, не считается новым в `src/include/gfxmentat.h` апстрима.
   - Ключи `PACKS` — имена файлов: `gfxdata.h`, `gfxinter.h`, `gfxmentat.h`, `gfxworld.h`, с теми же паками, что сейчас. `pack_index_findings` ищет пак по имени файла из `path`. Поле `header` находки — `path` записи.
   - Если в одной ревизии два прочитанных заголовка имеют одинаковое имя файла, генератор завершается с ошибкой, в которой названы оба пути.
   
   Затем запусти тест шага 2. Ожидается `OK`. Лог — `.tmp/p1a/test-03-green.log`.
4. **Вывод генератора.** Выполни шаг 4 задания P1A. В `id_collisions` нового `docs/upstream/port_inventory.json` ожидаются ровно четыре записи:

   | kind | header | pack | define | value | fork_entry |
   |---|---|---|---|---:|---|
   | pack_index_taken | `src/data/gfxdata.h` | `sdl_data_hd4.dat` | `EXPLOSION_CARRYALL` | 167 | `HM_BUILD_REFINERY` |
   | pack_index_missing | `src/data/gfxinter.h` | `sdl_inter_hd4.dat` | `BMP_SELECT_HOUSE_SARDAUKAR` | 144 | `null` |
   | pack_index_missing | `src/data/gfxinter.h` | `sdl_inter_hd4.dat` | `ICON_POWER_LOW` | 145 | `null` |
   | pack_index_missing | `src/include/gfxmentat.h` | `sdl_mentat_hd4.dat` | `MENTATS` | 51 | `null` |

   Другой состав — блок `Q-P1A-07` с содержимым `id_collisions` и стоп.
5. **Причины двух исключений** в `tools/upstream/port_features.json`. Замени `reason` ровно у этих двух исключений на текст ниже:
   - запись `command-bar`, путь `src/debug/UiAuditAccess.cpp`: `UiAuditAccess sets CommandBindingAction to start key capture in an audited options scene and records command-bar button geometry through recordCommandBarClicks; it does not implement the command bar.`
   - запись `faction-tint-terrain`, путь `tests/UnitFrameFixture.cpp`: `UnitFrameFixture adds HM_UNIT_* house masks to a test pack and calls getHouseTexture only to build house-coloured unit textures for render tests; it does not implement house tinting.`
6. **`docs/upstream/PORT_MAP.md`.** Три правки, остальной текст не меняется.
   - **Раздел «Данные и паки».** Первое предложение начинается словами «Двоичные паки определяются по .dat-путям каталога `resources/bin/data/` с». Предложение «JSON содержит пустой `id_collisions`.» заменяется предложением, которое называет число записей `id_collisions` и перечисляет каждую: пак, индекс, имя в `UP1` и запись форка или «записи нет».
   - **Раздел «Риски переноса», строка, которая начинается словами «Среди двоичных/LFS-путей».** Предложение «Записей `id_collisions` в JSON нет; общий пак нужно сверить по содержимому.» заменяется двумя предложениями. Первое: индекс 167 `sdl_data_hd4.dat` занят записью форка `HM_BUILD_REFINERY`, а `UP1` объявляет там `EXPLOSION_CARRYALL`; в `sdl_inter_hd4.dat` нет индексов 144 и 145 (`BMP_SELECT_HOUSE_SARDAUKAR`, `ICON_POWER_LOW`), в `sdl_mentat_hd4.dat` нет индекса 51 (`MENTATS`). У каждого имени — ссылка `путь@d06f2fc:строка` на его объявление в `UP1`. Второе: «Разбор и согласование относятся к Б2.»
   - **Раздел «Риски переноса», строка `world-scale`.** Она начинается так: «world-scale: UP1 переименовал `src/map/cMapCamera.cpp` в `src/gameobjects/map/cMapCamera.cpp`;». Дальше остаётся нынешний текст о преемнике `src/gameobjects/map/cMapCamera.cpp@d06f2fc:89` (**cMapCamera::setZoomLevel**).
   
   Размер файла — не больше 80000 байт, иначе блок `Q-P1A-04` и стоп.
7. **Проверки.**
   - `D2TM_PACK_DIR=$PWD/resources/bin/data /srv/dune/venv/bin/python -m unittest discover -s tools/upstream/tests -v`, лог `.tmp/p1a/tests-03.log`. Ожидается 8 тестов и `OK` без пропусков.
   - Повторный запуск генератора с `--out .tmp/p1a/inventory-03.json` и `cmp` с `docs/upstream/port_inventory.json`: код 0.
   - `git status --short` без строк `.tmp/` содержит ровно пять файлов: `tools/upstream/port_inventory.py`, `tools/upstream/tests/test_port_inventory.py`, `tools/upstream/port_features.json`, `docs/upstream/port_inventory.json`, `docs/upstream/PORT_MAP.md`. Другой файл или отсутствие одного из пяти — находка в сдаче.
   - Падение теста — блок `Q-P1A-05` со строками вывода и стоп.

## Сдача

Блок `## DONE-P1A-03 | <время UTC из date -u> | HEAD <sha>`. В нём:
- строки входа шага 1;
- строка падения теста из `.tmp/p1a/test-03-red.log` и итог `.tmp/p1a/test-03-green.log`;
- `git diff tools/upstream/port_inventory.py tools/upstream/tests/test_port_inventory.py` полностью;
- `id_collisions` из нового JSON;
- `git diff docs/upstream/PORT_MAP.md tools/upstream/port_features.json` полностью;
- размер `PORT_MAP.md` в байтах;
- итог тестов из `.tmp/p1a/tests-03.log` и вывод `cmp`;
- `### Коммиты` — одно английское сообщение `Read constexpr pack indices and moved headers in the port inventory` и список файлов. В сообщении ровно один абзац `Behavior changes:`, он стоит перед завершающей строкой `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Это исключение из правила раздела «Git» о последней строке; повторять абзац запрещено;
- `### Не проверено`;
- `### git status --short`.

## Организация работы

- **Режим:** «Ведёт sol».
- **Порядок:** шаг 1 → шаг 2 → шаг 3 → шаг 4 → шаги 5 и 6 → шаг 7 → `## DONE-P1A-03` и стоп.
- **Параллельно:** шаги 5 и 6 не зависят друг от друга; остальные шаги опираются на предыдущий.
- **Помощники:** не больше одного, `gpt-6-luna` `xhigh`, без вложенных: найти номера строк объявлений для ссылок шага 6. Корневая нить делает остальное и сама сверяет номера строк. В бриф помощника дословно входят абзац «Комментарии в коде» ниже и запрет писать вне `.tmp/p1a/`.
- **Остановки:** только на `## DONE-P1A-03` и на блоках `Q-P1A-NN`.
- **Рамка правок:** пять файлов задания P1A и `.tmp/p1a/`. Коммитов не делай.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.
