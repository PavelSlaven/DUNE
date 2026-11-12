# Вопросы ведущему к заданию P14A

Задание — `codex-direct/P14/TASK-P14A.md`. Вопросов четыре; ни один не блокирует запуск при рекомендованном варианте, но каждый меняет то, что исполнитель вправе править, поэтому ответ нужен до запуска. Игроку виден результат ни одного из них: все четыре касаются тестовых данных и инструментов.

## Как проверен черновик (ПК ведущего, вне репозитория)

Я разрешил 27 файлов по таблицам К2 и К3 в копии дерева `22d47aa4…` (папка в scratchpad, репозиторий не менялся) и проверил результат тем, что есть на этом ПК (MSYS2 `g++` 16.2, `-std=c++23`, SDL3 из `C:\msys64\mingw64`, Catch2 3):

- Все 196 файлов `src/**/*.cpp` проходят `g++ -fsyntax-only` (на `B14` — 195; лишний — `GameStateMachine.cpp`). Без правок К3.1, К3.2, К3.5 и К3.6 не компилируются 28 файлов: 26 из-за `UiAudit.hpp` и `UiAuditAccess.cpp`, плюс `cOptionsPages.cpp` и `cWinLoseState.cpp`.
- 196 файлов `D2TM_SOURCES` из `src/CMakeLists.txt` компилируются и линкуются в `d2tm.exe`; на диске и в `D2TM_SOURCES` одни и те же 196 файлов.
- 109 источников `tests/CMakeLists.txt` компилируются и линкуются в `d2tm_tests`; `--list-tests` — `563 test cases` (на `B14`, собранном так же, — 471; разница 92). Запуск без ресурсов игры: 542 случая проходят, 21 падает — те же 21 случай и те же 36 проверок, что на `B14` (нет файлов ресурсов и `D2TM_SOURCE_DIR`), новых падений нет.
- `-Wall -Wextra -Wpedantic` на 24 изменённых `.cpp` (19 из таблицы К2 и 5 из К3) — предупреждений нет (как на `B14`).
- Python: 233 теста `tools/ui-audit/tests` на `B14` и после правки; два падения (`test_b3_runtime_links_and_preferences`, `test_b4_game_environment`) есть и на `B14` на этом ПК (нужна среда Linux); после правки К3.7 шесть падений `test_g_exclusions_exist_in_port_code` уходят; три новых теста зелёные, на дереве слияния они красные (`failures=1, errors=2`). `test_classic_pack_entries` после К3.9 — `OK` (107 строк `sdl_audio.dat`).
- `check_tests.py`: `problems=0`; `check_hunks.py`: `files=27 hunks=38 mismatches=0`; опись клавиш `extract_keys.py` + `check_keys.py`: `freshness OK`, 178 отметок, как на `B14`.

Не проверено: компилятор clang и флаги `-Werror` macOS; сборка и CTest на Linux (servak); запуск игры, сцены режима отладки, снимки; данные LFS (на ПК их нет). Эти проверки — в разделе «Проверки» задания.

## Q-P14A-Q1. Менять ли данные существующего теста `classic_packs_expected.tsv`

**Что не решено.** Апстрим изменил пак `resources/bin/data/sdl_audio.dat`, а Python-тест порта сравнивает его запись за записью с файлом данных; без обновления файла данных тест падает.

**Факты.**

- `git diff --stat d06f2fcd d7869e710 -- resources/bin/data/sdl_audio.dat`: 1 359 423 → 1 356 190 байт; в `UP2` 107 записей против 108 (`MIDI_LOSE1..3` → `MIDI_LOSE01..03`, `SOUND_TANKDIE` → `SOUND_TANKDIE1`, запись `SOUND_TANK` удалена, индексы после 72 сдвинуты; коммиты 8a3468304 и 4ba66a16b). Порт файл не менял.
- `0683500a:tools/upstream/tests/test_port_packs_data.py:122` (`test_classic_pack_entries`) читает `resources/bin/data/sdl_audio.dat` и сравнивает 108 строк `tests/data/classic_packs_expected.tsv` (строки 2–109 файла в `0683500a`).
- Правило исполнителя запрещает менять ожидания существующих тестов без `Q`.

**Варианты.**

1. Регенерировать строки `sdl_audio.dat` скриптом из пака `UP2` (задание К3.9, приложение А): остальные 436 строк файла не меняются, тест остаётся строгим. Рекомендация.
2. Оставить файл как есть и вывести `sdl_audio.dat` из сравнения теста — ослабляет тест и требует правки самого теста.

**Что следует.** При варианте 1 утверждение вашего «да» на задание — это разрешение на правку данных теста; задание уже называет файл и скрипт.

## Q-P14A-Q2. Правило «каждое имя `TEST_CASE` из `B14` и из `UP2` есть в дереве» невыполнимо для одного случая

**Что не решено.** Брифом шага названа проверка «каждое имя `TEST_CASE` из `B14` и из `UP2` есть в дереве». Одного имени из `UP2` в дереве не будет никогда.

**Факты.**

- Случай `cHandleArgument - scaling mode flags` есть в `d06f2fcd:tests/utils/test_cHandleArgument.cpp:178` и, значит, в `UP2` (апстрим файл не менял: `git diff --stat d06f2fcd d7869e710 -- tests/utils/test_cHandleArgument.cpp` пуст).
- Порт заменил его случаем `cHandleArgument - removed scaling mode flags are unknown options` (`0683500a:tests/utils/test_cHandleArgument.cpp:178`, коммит 867948487 «Add acceptance tests for game scale and replace scaling mode checks», шаг П4б: `ScalingMode`, Alt+L и `-integerscale` удалены решением Р66).
- Число проверок в файле одно и то же: 63 в `UP1`, `B14` и `UP2`.

**Варианты.**

1. Скрипт `check_tests.py` требует от `UP2` только случаи, которых не было в `UP1` (92 новых), а от `B14` — все 474; пропавшее по решению П4б не возвращается. Рекомендация; так написано в задании.
2. Вернуть случай `cHandleArgument - scaling mode flags` — противоречит П4б (аргументы `-integerscale` и другие больше не распознаются как параметры масштаба).

## Q-P14A-Q3. Правка скрипта сборки `tools/upstream/build_upstream_linux.sh` (строка MENU)

**Что не решено.** Без правки скрипт не может завершиться кодом 0 на дереве после слияния; правка — в чужом, но портовом инструменте.

**Факты.**

- `0683500a:tools/upstream/build_upstream_linux.sh:13`: `menu_text='Setting state from -1(=INITIALIZE) to 1(=MENU)'`; строка 253 ищет её в логе игры и при отсутствии вызывает `question` (выход 1).
- `d7869e710:src/game/GameStateMachine.cpp:51-52` пишет `Setting state from INITIALIZE to MENU` (`gameStateToString`, `d7869e710:src/include/eGameState.cpp`); старой строки в `UP2` нет (`git grep -n 'Setting state from {}(={})' d7869e710 -- src` — пусто).
- Строка 261 того же скрипта печатает источник `src/game/cGame_logic.cpp:945–946`; после слияния верный источник — `src/game/GameStateMachine.cpp:51–52`.
- Аргумент скрипта (`d06f2fcd…`) менять нельзя: строка 183 требует, чтобы он был предком `HEAD`, а `d7869e710…` предком станет только после вашего коммита слияния.

**Варианты.**

1. Править строки 13 и 261 в рамке задания (К3.8). Рекомендация.
2. Не править; тогда проверка 1 всегда падает на `question`, а исполнитель остановится на `Q`.

**Замечание вне репозитория.** Если ваши скрипты надзора или приёмки ищут в логах игры строку `Setting state from -1(=INITIALIZE) to 1(=MENU)`, после слияния они тоже должны искать `Setting state from INITIALIZE to MENU` (поиск по `~/.claude`, `/srv/dune/tools` и папкам заданий я не делал: на этом ПК их нет).

## Q-P14A-Q4. Как инструмент `check_screens.py` получает имена состояний после удаления констант `GAME_*`

**Что не решено.** Скрипт `tools/ui-audit/check_screens.py` берёт имена состояний из целочисленных констант `GAME_*` файла `src/include/eGameState.h`; апстрим удалил эти константы (коммит 94b54034c), остался `enum class eGameState`.

**Факты.**

- `0683500a:tools/ui-audit/check_screens.py:7` (`STATE_DEFINE`), `:59` (`collect_code_names`); каталог сцен (`0683500a:src/debug/UiAuditScenes.cpp`, таблица `kGroupScreens`, строки 47–61) и `tools/ui-audit/exclusions.tsv` называют состояния `GAME_MENU`, `GAME_INTRO` и т. д.; `tests/ui_audit/ui_audit_list_and_scales.py:15-16` проверяет вывод `--ui-audit-list` с `"state": "GAME_MENU"`.
- Без правки `collect_code_names` возвращает ноль имён `GAME_*`: тест `test_g_exclusions_exist_in_port_code` (`tools/ui-audit/tests/test_port_changes.py`) падает шестью подтестами, скрипты `ui_audit_part3a_catalog.py` и `ui_audit_part3c_catalog.py` — ошибками «exclusion … is not a name in the code».

**Варианты.**

1. Оставить имена `GAME_*` в каталоге и `exclusions.tsv`, а `check_screens.py` научить выводить их из перечисления (`GAME_<ИМЯ>`, `COUNT` → `GAME_MAX_STATES`): 3 вставки и 3 новых теста (задание К3.7, К4); существующие тесты, `exclusions.tsv` и вывод `--ui-audit-list` не меняются. Рекомендация.
2. Переименовать состояния в каталоге, `exclusions.tsv` и пяти скриптах `tests/ui_audit/*catalog.py` на `eGameState::<ИМЯ>`: меняет вывод `--ui-audit-list` (поле `state` каждой из 192 сцен) и скрипты `tests/ui_audit/`, которые задание менять запрещает; шире шага и рискованнее.

## Замечания к заданию (не вопросы)

- В задании одна подстановка за вами: `HEAD` рабочей копии (вершина порта после слияния П13). Проверка 0 ожидает, что П13 добавил в порт ровно четыре файла из брифа шага; если слияние П13 принесёт другие файлы, поправьте этот список. Номера строк задания верны, пока П13 не меняет `src/`, `tests/` и три файла `tools/`, правимых здесь (`check_screens.py`, `build_upstream_linux.sh`, `tests/data/classic_packs_expected.tsv`).
- Блок правил исполнителя не вставлен; `check-literal.py --task` на черновике даёт единственный флаг «нет блока правил».
- Дорожки помощников: A — звук (10 файлов), B — состояния игры (18 файлов), C — паки, инструменты, тесты и проверки; наибольшие риски разрешения: `src/context/AudioContext.cpp` (конструктор, К2.2), `src/game/cGame_logic.cpp` и `src/game/cGame.h` (состояния и колбэки), `src/gamestates/cMainMenuState.cpp` и `cOptionsState.cpp` (участки по 70–190 строк). Параллельных шагов нет.

## Ответы ведущего (2026-11-13)

- Q1 — вариант 1: строки `sdl_audio.dat` в `tests/data/classic_packs_expected.tsv` регенерируются скриптом из пака `UP2` (К3.9); остальные строки файла не меняются.
- Q2 — вариант 1: от `UP2` требуются только случаи, которых не было в `UP1`; от `B14` — все.
- Q3 — вариант 1: строки 13 и 261 `tools/upstream/build_upstream_linux.sh` правятся в рамке задания (К3.8).
- Q4 — вариант 1: имена `GAME_*` остаются в каталоге и `exclusions.tsv`, `check_screens.py` выводит их из перечисления (К3.7, К4).
- Подстановка `HEAD` — `6967cc72fe80be6a800829d2e2268aca293e66c7`; П13 добавил ровно четыре файла из брифа.
