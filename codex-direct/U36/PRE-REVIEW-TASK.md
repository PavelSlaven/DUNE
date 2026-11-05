# Задание U36-PR — предревью ветки U36 (раскатка угла Аванпоста на остальные здания)

## Цель

Независимо проверить два коммита ветки `codex/u36-building-rollout` поверх `ba8c17d0` (main):

- `18bccb69` — пак `resources/bin/data/sdl_data_hd4.dat` и 52 мастер-файла;
- `f9974e37` — тест `tools/building_angle/tests/test_rollout_pack.py`.

Выписать каждое расхождение с файлом, строкой и причиной. Задача только проверяет: код и данные ветки не меняются, коммитов нет. Свои скрипты и выводы — только в `.tmp/pre-review-u36/`. Вид картинок (красиво или нет) не оценивается: его принимает владелец в игре.

## Источник истины

- Задание и ответы ведущего: `/srv/dune/tasks/u36/task.md` (задание целиком), `task-01.md` … `task-06.md`. Сдачи исполнителя: `/srv/dune/tasks/u36/reply.txt`, `reply-01.txt` … `reply-06.txt`. Где ответ ведущего меняет задание, верен ответ с бо́льшим номером.
- Правила сборки записей: `task-03.md` (кадр 7 Космопорта, турели), `task-05.md` (все остальные записи, шаги 2–13), `task-06.md` (выбор варианта `b` Тяжёлого завода, установка, мастер-файлы, тест).
- Issue #81 и #82 — тексты в конце `/srv/dune/tasks/u36/task.md`, раздел «Тексты issue».
- Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/u36-building-rollout`, HEAD `f9974e37`. Промежуточные файлы исполнителя — `.tmp/` той же копии: `.tmp/u36-old/` (52 записи пака `ba8c17d0`), `.tmp/u36-fit/`, `.tmp/u36-stretch/`, `.tmp/u36-b1/`, `.tmp/u36-b2/`, `.tmp/u36-b2/work/`, `.tmp/u36-install/`, `.tmp/u36-pack/pack-before.dat`, `.tmp/u36-tools/`, `.tmp/u36-tests/head/`, `.tmp/u36-tests/after/`.
- Движок: `src/drawers/cStructureDrawer.cpp` (флаги и накладки), `src/utils/Graphics.cpp` строки 376–450 (окраска Дома по маске `HM_*`).
- Среда: `/srv/dune/venv/bin/python` (Pillow, numpy, scipy, `unittest`); Git LFS — `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`. Сети нет, пакеты не устанавливаются.

## Подготовка

Извлеки пак `ba8c17d0` в `.tmp/pre-review-u36/pack-before/sdl_data_hd4.dat` командой `git show ba8c17d0:resources/bin/data/sdl_data_hd4.dat | git lfs smudge > .tmp/pre-review-u36/pack-before/sdl_data_hd4.dat` (с Git LFS в `PATH`). Сравни его sha256 с sha256 файла `.tmp/u36-pack/pack-before.dat`; не равны — находка, дальше сравнивай с извлечённым тобой паком.

Дальше «запись HEAD» — запись пака рабочей копии после `tools.hd_assets.decode_image`, в RGBA; «равна» — попиксельно равна по RGBA.

## Что проверить

1. **Состав.** `git diff --stat ba8c17d0 f9974e37`: только `resources/bin/data/sdl_data_hd4.dat`, 52 мастер-файла из списка «### Коммиты» в `/srv/dune/tasks/u36/reply-06.txt` и `tools/building_angle/tests/test_rollout_pack.py`. Коммит `18bccb69` содержит только пак и мастер-файлы, `f9974e37` — только тест. Файл вне списка — находка.

2. **Пак.** Сравни паки `ba8c17d0` и HEAD через `tools.hd_assets.read_pack`:
   - одинаковое число записей и одинаковый порядок имён;
   - по содержимому отличаются ровно 52 записи с именами файлов `.tmp/u36-old/*.png`; остальные побайтно равны;
   - размеры 52 новых записей равны размерам старых;
   - каждая из 52 записей HEAD равна своему мастер-файлу на HEAD (мастер — `resources/hd/master4/sdl_data/[0-9][0-9][0-9][0-9]_<ЗАПИСЬ>.png`, а если такого нет — `resources/hd/master4_extra_packs/sdl_data/<ЗАПИСЬ>.png`).

3. **Происхождение.** Для каждой из 52 записей — строка таблицы: запись, источник, равна или число отличающихся пикселей. Неравенство — находка.
   - Готовые файлы: `BUILD_<B>` для B = `BARRACKS`, `CONSTYARD`, `IX`, `PALACE`, `SILO`, `WOR` — `.tmp/u36-fit/<B>_a.png`; `BUILD_LIGHTFACTORY` — `.tmp/u36-fit/LIGHTFACTORY_D2a.png`; `BUILD_HEAVYFACTORY` и `BUILD_HEAVYFACTORY_SHADOW` — `.tmp/u36-b2/work/BUILD_HEAVYFACTORY_b.png` и `BUILD_HEAVYFACTORY_b_SHADOW.png`; `BUILD_STARPORT`, `BUILD_TURRET`, `BUILD_TURRET_SHADOW`, `BUILD_RTURRET`, `BUILD_RTURRET_SHADOW` — `.tmp/u36-b1/`; `BUILD_HIGHTECH_FLAG`, `HM_BUILD_HIGHTECH_FLAG`, `BUILD_STARPORT_FLAG`, `HM_BUILD_STARPORT_FLAG` — `.tmp/u36-stretch/`.
   - Повтор скриптами ведущего в `.tmp/pre-review-u36/repro/`: `flags.py` (шаг 5 `task-05.md`, выходная папка — твоя), три команды `overlay_map.py` (шаги 6 и 7), `ht_fix0.py` и `ht_frames2.py` (шаг 11). Скрипты лежат в `.tmp/u36-tools/`; их sha256 сверь с таблицей шага 2 сдачи `reply-05.txt`. Выходы сравни с записями HEAD.
   - Тени: `angle.py shadow` на записях HEAD с плитами и числом кадров из таблицы шага 13 `task-05.md` (для `BUILD_HEAVYFACTORY` — 3x2, 11 кадров); результат сравни с записью `_SHADOW` HEAD.

4. **Анимации по правилам.** Напиши свои реализации по тексту правил, не открывая скрипты исполнителя до сравнения, и сравни результат с записями HEAD. Неравенство — находка; затем открой скрипт исполнителя и назови строку, где он расходится с правилом.
   - Машина Тяжёлого завода: шаг 8.3 `task-05.md`, режим `--edit` с E = `.tmp/u36-fit/HEAVYFACTORY_VEH_b.png`, основа B = `.tmp/u36-fit/HEAVYFACTORY_D2b.png` → запись `BUILD_HEAVYFACTORY`.
   - Завод переработки: шаг 9 `task-05.md`, N = `.tmp/u36-b2/work/REFINERY_a.png` → записи `BUILD_REFINERY` и `HM_BUILD_REFINERY`.
   - Ремонт: шаг 10 `task-05.md`, C = `.tmp/u36-b2/work/REPAIR_a.png`, Op = `.tmp/u36-fit/REPAIR_a_open.png` → запись `BUILD_REPAIR`.
   - Кадр 7 Космопорта: шаг 8 `task-03.md`, источник `.tmp/u36-stretch/BUILD_STARPORT.png` → запись `BUILD_STARPORT`.

5. **Окраска Дома и флаги.**
   - Для каждой пары `BUILD_<B>_FLAG` и `HM_BUILD_<B>_FLAG` (10 зданий) посчитай по 8 кадрам число пикселей, у которых альфа маски больше 0, а альфа флага равна 0, — в паке `ba8c17d0` и на HEAD. Рост числа — находка.
   - У `BUILD_PALACE_FLAG` посчитай по 8 кадрам число пикселей с R ≥ 2·G + 1 и R ≥ 2·B + 1 (красные огни), у которых альфа `HM_BUILD_PALACE_FLAG` больше 0, — в паке `ba8c17d0` и на HEAD. По `src/utils/Graphics.cpp` выпиши, перекрашивает ли окраска Дома такие пиксели. Справочно; рост числа и перекраска — находка с числом пикселей.
   - Для каждого флага, кроме `BUILD_STARPORT_FLAG`, — число различных кадров из 8 в паке `ba8c17d0` и на HEAD. Меньше, чем в `ba8c17d0`, — находка.

6. **Тесты.**
   - `tools/building_angle/tests/test_rollout_pack.py`: пять методов по шагу 5 `task-06.md`; каждое отличие — находка с номером строки.
   - Прогони `tools/building_angle/tests` (все файлы) с `D2TM_PACK_DIR=$PWD/resources/bin/data`. Ожидается: зелёный; пропущенные методы назови.
   - Прогони их же с `D2TM_PACK_DIR=$PWD/.tmp/pre-review-u36/pack-before`. Ожидается: падают пять методов `test_rollout_pack.py`, остальные методы дают тот же итог, что в первом прогоне.
   - Строки вывода — в отчёт.
   - Сравни списки падающих методов `.tmp/u36-tests/head/` и `.tmp/u36-tests/after/`. Метод, падающий только в `after`, — находка.

7. **Коммиты.**
   - Сообщения двух коммитов — английские.
   - Перед строкой `Co-Authored-By` стоит абзац, начинающийся с `Behavior changes:`.
   - Каждое утверждение сообщения, которое не подтверждается пунктами 2–5 или правилами ответов ведущего, — находка. Проверь утверждения `18bccb69`: «High-Tech and Starport keep their pictures and are stretched to the slab with one box for all frames», «in the last Starport frame the landing platform is scaled down to fit its pad», «Flag sheets and their house masks move with the new pictures», «the Refinery slot lights keep the old blinking pattern on the new slots», «Shadows are rebuilt by the existing rule».

## Организация работы

- Порядок: подготовка → пункты 1–7 → отчёт.
- Параллельно: после подготовки пункты 1–7 независимы друг от друга.
- Помощники: до 4 одновременно, `gpt-6-luna` `xhigh`, без вложенных: один — пункты 1, 2, 7; один — пункт 3; один — пункт 4; один — пункты 5, 6. Корневая нить сверяет выводы помощников, сама проверяет каждую находку и пишет отчёт.
- Остановки: только на итоговом отчёте.
- Рамка правок: только `.tmp/pre-review-u36/`. Ничего вне неё не меняй, не коммить.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

Помощникам этот абзац передаётся в бриф дословно.

## Отчёт

Заголовок: `## PRE-REVIEW-U36 | <время UTC из date -u> | HEAD <sha>`.

Затем по пунктам 1–7: «чисто» или список находок. У каждой находки — файл:строка, что не так, чем подтверждено (строка вывода). Справочные числа пунктов 3 и 5 — в своих пунктах.

В конце — «### Итог»: число находок; для каждой — блокирует ли она слияние (да/нет) и причина одной фразой.
