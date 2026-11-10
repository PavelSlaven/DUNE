# Задание P5BT — приёмочные тесты меню настроек (шаг П5б)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогоны сборки делает один субагент `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5b`, `HEAD` — `832c953a94a632d57872349013f7ed1a37434715` (вершина ветки порта после шага П6). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5bt/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Написать приёмочные тесты шага П5б по контракту API ниже, получить красный прогон по заявленной причине и заморозить тесты хэшем. Код игры не менять, кроме временных правок прогона B (шаг 2), которые убираются сразу после него.

## Что уже решено

Шаг П5б переносит на меню настроек порта раскладку окна форка `OptionsMenuLayout` и две строки форка: «Масштаб игры» (`RenderScale`) и «Размер объектов» (`WorldScale`). Выбор игрока по кнопке «Apply» записывается в файл `preferences.ini` и вступает в силу после перезапуска игры. Заголовок `src/gamestates/OptionsMenuLayout.hpp` переносится дословной копией ревизии форка `9208dcf5a358f40afd95c99480e4e09f781ed566`; приёмка раскладки — тест форка `tests/OptionsMenuLayoutTests.cpp` той же ревизии, перенесённый на Catch2.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- `tests/utils/test_Preferences.cpp` — образец тестов и помощник `freshDirectory`;
- `tests/utils/test_RenderScale.cpp`;
- `tests/CMakeLists.txt`;
- `src/game/Preferences.hpp`, `src/game/Preferences.cpp`;
- `src/utils/RenderScale.hpp`, `src/utils/RenderScale.cpp`, `src/utils/WorldScale.hpp`, `src/utils/InitialGameSettings.hpp`, `src/utils/cRectangle.h`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/OptionsMenuLayoutTests.cpp` — тест форка, который переносишь;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/OptionsMenuLayout.hpp` — заголовок форка.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт API

Этот раздел дословно входит и в задание исполнителя кода.

1. **Раскладка окна настроек (новый файл).** `src/gamestates/OptionsMenuLayout.hpp` — дословная копия одноимённого файла ревизии форка `9208dcf5a358f40afd95c99480e4e09f781ed566` (команда `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/OptionsMenuLayout.hpp`). В нём структура `OptionsMenuLayout`: поля `window`, `speedLabel`, `apply`, `advanced`, `status`, `save`, `load`, `missionSelect`, `mainMenu`, `quit`, `back` типа `cRectangle`, поля `contentTop` и `contentGap` типа `int`, статический метод `create(int canvasWidth, int canvasHeight, int buttonHeight, bool playing, int titleFontHeight = -1)`.
2. **Списки масштабов (новые файлы).** `src/utils/ScaleChoices.hpp`:
   ```cpp
   #pragma once

   #include <cstddef>
   #include <string>
   #include <vector>

   [[nodiscard]] std::vector<int> renderScaleChoices(int outputWidth, int outputHeight);
   [[nodiscard]] std::vector<int> worldScaleChoices();
   [[nodiscard]] std::size_t scaleChoiceIndex(const std::vector<int> &choices, int scalePercent);
   [[nodiscard]] std::string scaleChoiceText(int scalePercent, int automaticScalePercent);
   ```
   - `renderScaleChoices`: первый элемент — `AutomaticRenderScale` (0); за ним значения массива `ManualRenderScales` из `src/utils/RenderScale.hpp` в порядке массива — только те, для которых `isManualRenderScaleAvailable(outputWidth, outputHeight, <значение>)` возвращает `true`.
   - `worldScaleChoices`: первый элемент — `AutomaticWorldScale` (0); за ним все значения массива `ManualWorldScales` из `src/utils/WorldScale.hpp` в порядке массива. Результат — `{0, 100, 110, 125, 150}`.
   - `scaleChoiceIndex`: индекс первого элемента `choices`, равного `scalePercent`; если равного нет — 0.
   - `scaleChoiceText`: при `scalePercent` = 0 — `std::format("Auto ({}%)", automaticScalePercent)`; при любом другом `scalePercent` — `std::format("{}%", scalePercent)`.
   - Реализация — `src/utils/ScaleChoices.cpp`. В `src/CMakeLists.txt` строка `utils/ScaleChoices.cpp` стоит сразу после строки `utils/RenderScale.cpp`.
3. **Файл настроек игрока.** `src/game/Preferences.hpp` и `src/game/Preferences.cpp`, пространство имён `Preferences`:
   - константа `inline constexpr const char *FILE_NAME = "preferences.ini";` в `Preferences.hpp`;
   - функция `save` дополнительно записывает ключ `WorldScale` со значением `std::to_string(settings.worldScalePercent)`; строка записи стоит сразу после строки записи ключа `RenderScale`; остальное в `save` не меняется;
   - новая функция `bool saveScales(const std::filesystem::path &file, int renderScalePercent, int worldScalePercent, std::string &error);` Записывает в секцию `SETTINGS` файла `file` ключ `RenderScale` со значением `std::to_string(renderScalePercent)` и ключ `WorldScale` со значением `std::to_string(worldScalePercent)`. Если файл `file` существует, `cIniFile` его загружает и в нём есть секция `SETTINGS`, все остальные ключи секции `SETTINGS` сохраняют свои значения. Иначе после записи в секции `SETTINGS` только эти два ключа. Каталог файла создаётся; запись — через временный файл `<file>.tmp` и переименование, как в `save`. При ошибке — `false` и текст ошибки в `error`; иначе `true`;
   - новая функция `bool loadScales(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);` Если файла `file` нет, `cIniFile` его не загружает или в нём нет секции `SETTINGS` — `false`, текст ошибки в `error`, `settings` не меняется. Иначе: есть ключ `RenderScale` — `settings.renderScalePercent` получает его целое значение; есть ключ `WorldScale` — `settings.worldScalePercent` получает его целое значение; другие поля `settings` не меняются; результат `true`.

## Шаг 1. Тесты — корневая нить сама

Catch2 3, как остальные файлы `tests/`. У каждого нового `TEST_CASE` имя начинается с `P5B `, тег — `[P5B]`. Каждое условие ниже — отдельная проверка `CHECK`, кроме мест, где написано `REQUIRE`.

### Новый файл `tests/utils/test_OptionsMenu.cpp`

Первая строка — `#include <catch2/catch_test_macros.hpp>`; вторая — `#include "utils/ScaleChoices.hpp"`; затем строки 1–281 файла форка `tests/OptionsMenuLayoutTests.cpp@9208dcf5a358f40afd95c99480e4e09f781ed566` дословно (подключения, анонимное пространство имён со структурами `Case`, `Check`, `Field` и функциями `equal`, `rectangleEqual`, `compactSpacing`, `expectedContentTop`, `expectedRectangles`, `exact`, `table`, `inside`, `headerSpacing`, `intersects`, `overlap`). Функции `main` форка в файле нет: её проверки переходят в тесты 1–3. Тесты, по одному `TEST_CASE` на пункт:

1. **`P5B options menu layout matches the fork on the canvas matrix`.** Тело — строка 285 и строки 287–340 файла форка дословно (объявления `exactCheck`, `insideCheck`, `headerSpacingCheck`, `overlapCheck`, счётчик `cases`, лямбды `checkCanvas` и `checkOutput`, массивы `standardResolutions` и `otherOutputs`, все циклы матрицы). После них пять проверок: `cases` = 120978; `exactCheck.failures` = 0; `insideCheck.failures` = 0; `headerSpacingCheck.failures` = 0; `overlapCheck.failures` = 0. Число 120978 посчитано по циклам строк 291–340 и правилу `isManualRenderScaleAvailable` из `src/utils/RenderScale.cpp`: 4653 вызова `checkCanvas`, по 26 случаев в каждом.
2. **`P5B options menu layout keeps the fork table examples`.** `Check tableCheck{"table"};`, вызов `table(tableCheck);`, проверка `tableCheck.failures` = 0.
3. **`P5B options menu layout fits 44 pixel buttons on 600 lines`.** `Check headerSpacingCheck{"header-spacing"};`, затем строки 341–351 файла форка дословно, затем две проверки: `tallButtonCheck.failures` = 0; `headerSpacingCheck.failures` = 0.
4. **`P5B render scale choices follow the 800x600 minimum`.** Шесть проверок равенства с `std::vector<int>`:

   | вызов | ожидаемый результат |
   |---|---|
   | `renderScaleChoices(800, 600)` | `{0, 100}` |
   | `renderScaleChoices(640, 480)` | `{0, 100}` |
   | `renderScaleChoices(1280, 720)` | `{0, 100}` |
   | `renderScaleChoices(1366, 768)` | `{0, 100, 125}` |
   | `renderScaleChoices(1920, 1080)` | `{0, 100, 125, 150, 175}` |
   | `renderScaleChoices(2560, 1440)` | `{0, 100, 125, 150, 175, 200}` |

5. **`P5B world scale choices indexes and labels`.** Девять проверок: `worldScaleChoices()` = `std::vector<int>{0, 100, 110, 125, 150}`; `scaleChoiceIndex(std::vector<int>{0, 100, 125, 150, 175}, 175)` = 4; `scaleChoiceIndex(std::vector<int>{0, 100, 125, 150, 175}, 200)` = 0; `scaleChoiceIndex(std::vector<int>{0, 100, 125, 150, 175}, 0)` = 0; `scaleChoiceIndex(std::vector<int>{0, 100, 110, 125, 150}, 110)` = 2; `scaleChoiceText(0, 180)` = `"Auto (180%)"`; `scaleChoiceText(125, 180)` = `"125%"`; `scaleChoiceText(0, 110)` = `"Auto (110%)"`; `scaleChoiceText(150, 110)` = `"150%"`. Строки сравниваются как `std::string`.

### Дописать в конец файла `tests/utils/test_Preferences.cpp`

Существующие строки файла не меняются. Каталоги тестов — помощником `freshDirectory` этого файла; имя каталога у каждого теста своё, указано в пункте. Новые тесты:

6. **`P5B preferences save and load WorldScale`.** `std::string(Preferences::FILE_NAME)` = `"preferences.ini"`. Файл — `freshDirectory("d2tm_p5b_prefs_world") / "preferences.ini"`. `InitialGameSettings saved;` с `saved.renderScalePercent = 150;` и `saved.worldScalePercent = 125;`; `REQUIRE(Preferences::save(file, saved, error))`; `InitialGameSettings loaded;`, `REQUIRE(Preferences::load(file, loaded, error))`; `loaded.renderScalePercent` = 150; `loaded.worldScalePercent` = 125.
7. **`P5B preferences saveScales keeps the other keys`.** Файл — `freshDirectory("d2tm_p5b_prefs_keep") / "preferences.ini"`. `InitialGameSettings saved;` с `saved.playMusic = false;`, `saved.fogOfWarEnabled = true;`, `saved.renderScalePercent = 100;`, `saved.worldScalePercent = 100;`; `REQUIRE(Preferences::save(file, saved, error))`; `REQUIRE(Preferences::saveScales(file, 175, 110, error))`; `InitialGameSettings loaded;`, `REQUIRE(Preferences::load(file, loaded, error))`; `loaded.renderScalePercent` = 175; `loaded.worldScalePercent` = 110; `loaded.playMusic` = `false`; `loaded.fogOfWarEnabled` = `true`.
8. **`P5B preferences saveScales creates a missing file`.** Файл — `freshDirectory("d2tm_p5b_prefs_new") / "nested" / "preferences.ini"`; каталога `nested` до вызова нет. `REQUIRE(Preferences::saveScales(file, 150, 125, error))`; `std::filesystem::exists(file)` = `true`; `InitialGameSettings loaded;`, `REQUIRE(Preferences::load(file, loaded, error))`; `loaded.renderScalePercent` = 150; `loaded.worldScalePercent` = 125; `loaded.screenW` = 800; `loaded.playMusic` = `true`; `loaded.fogOfWarEnabled` = `false`.
9. **`P5B preferences loadScales reads only the scale keys`.** Файл — `freshDirectory("d2tm_p5b_prefs_scales") / "preferences.ini"`. `InitialGameSettings saved;` с `saved.screenW = 1280;`, `saved.playMusic = false;`, `saved.fogOfWarEnabled = true;`, `saved.renderScalePercent = 125;`, `saved.worldScalePercent = 150;`; `REQUIRE(Preferences::save(file, saved, error))`. `InitialGameSettings loaded;`, `REQUIRE(Preferences::loadScales(file, loaded, error))`; `loaded.renderScalePercent` = 125; `loaded.worldScalePercent` = 150; `loaded.screenW` = 800; `loaded.playMusic` = `true`; `loaded.fogOfWarEnabled` = `false`. Затем файл `freshDirectory("d2tm_p5b_prefs_missing") / "preferences.ini"` (его нет); `InitialGameSettings untouched;` с `untouched.renderScalePercent = 100;` и `untouched.worldScalePercent = 110;`; `std::string missingError;`; `Preferences::loadScales(<этот файл>, untouched, missingError)` = `false`; `missingError.empty()` = `false`; `untouched.renderScalePercent` = 100; `untouched.worldScalePercent` = 110.

Значения по умолчанию `InitialGameSettings`, на которые опираются тесты 8 и 9 (`src/utils/InitialGameSettings.hpp`): `screenW` = 800, `playMusic` = `true`, `fogOfWarEnabled` = `false`, `renderScalePercent` = 0, `worldScalePercent` = 0.

### Правки `tests/CMakeLists.txt`

В список `TEST_FILES` строка `${CMAKE_CURRENT_SOURCE_DIR}/utils/test_OptionsMenu.cpp` сразу после строки `${CMAKE_CURRENT_SOURCE_DIR}/utils/test_AdaptiveMenus.cpp`; в список `TEST_SOURCES` строка `${CMAKE_SOURCE_DIR}/src/utils/ScaleChoices.cpp` сразу после строки `${CMAKE_SOURCE_DIR}/src/utils/RenderScale.cpp`. Других правок в `tests/CMakeLists.txt` нет.

Другие файлы `tests/` и весь код вне `tests/` не меняются.

## Шаг 2. Красный прогон — субагент `gpt-6-luna` `xhigh`

Перед каждой сборкой `df -m /srv`: в столбце `Available` не меньше 5000, иначе блок `## Q-P5BT-01` и стоп. Команда сборки из корня рабочей копии (в `<лог>` — имя файла ниже):

```
DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5bt/<лог> 2>&1
```

Субагент сдаёт корневой нити код выхода каждого прогона, все строки лога прогона и `.tmp/out/logs/<последняя папка>/full.log`, содержащие `error:`, вывод `grep -A3 "CMake Error"` по тем же двум файлам и, если есть `ctest.log` последней папки логов, его строки с `Failed`, `failed` и итоговую строку `tests passed`.

- **Прогон A** — лог `build-red-a.log`, рабочая копия как после шага 1. Ожидается: код выхода не 0; сборка останавливается на настройке CMake; в выводе `grep -A3 "CMake Error"` ровно два блока `CMake Error` с местом `tests/CMakeLists.txt:<номер строки> (add_executable)`: первый содержит `Cannot find source file:` и путь, оканчивающийся на `src/utils/ScaleChoices.cpp`; второй содержит `No SOURCES given to target: d2tm_tests`; строк `error:` нет.
- **Прогон B** — лог `build-red-b.log`. Перед ним субагент делает временные правки:
  - файл `src/gamestates/OptionsMenuLayout.hpp` ровно такого вида:
    ```cpp
    #pragma once

    #include "utils/cRectangle.h"

    struct OptionsMenuLayout {
        cRectangle window;
        cRectangle speedLabel;
        cRectangle apply;
        cRectangle advanced;
        cRectangle status;
        cRectangle save;
        cRectangle load;
        cRectangle missionSelect;
        cRectangle mainMenu;
        cRectangle quit;
        cRectangle back;
        int contentTop = 0;
        int contentGap = 0;

        [[nodiscard]] static OptionsMenuLayout create(int, int, int, bool, int = -1)
        {
            return OptionsMenuLayout{};
        }
    };
    ```
  - файл `src/utils/ScaleChoices.hpp` ровно с текстом из пункта 2 контракта и заглушка `src/utils/ScaleChoices.cpp` ровно такого вида:
    ```cpp
    #include "utils/ScaleChoices.hpp"

    std::vector<int> renderScaleChoices(int, int)
    {
        return {};
    }

    std::vector<int> worldScaleChoices()
    {
        return {};
    }

    std::size_t scaleChoiceIndex(const std::vector<int> &, int)
    {
        return 0;
    }

    std::string scaleChoiceText(int, int)
    {
        return {};
    }
    ```
  - копии `cp src/game/Preferences.hpp .tmp/p5bt/Preferences.hpp.orig` и `cp src/game/Preferences.cpp .tmp/p5bt/Preferences.cpp.orig`; затем в `src/game/Preferences.hpp` сразу после строки `bool save(const std::filesystem::path &file, const InitialGameSettings &settings, std::string &error);` три строки:
    ```cpp
    inline constexpr const char *FILE_NAME = "preferences.ini";
    bool saveScales(const std::filesystem::path &file, int renderScalePercent, int worldScalePercent, std::string &error);
    bool loadScales(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);
    ```
    и в конец файла `src/game/Preferences.cpp` текст:
    ```cpp

    namespace Preferences {

    bool saveScales(const std::filesystem::path &, int, int, std::string &)
    {
        return false;
    }

    bool loadScales(const std::filesystem::path &, InitialGameSettings &, std::string &)
    {
        return false;
    }

    }
    ```

  `src/CMakeLists.txt` не меняется. Сразу после прогона B субагент убирает временные правки командами `rm src/gamestates/OptionsMenuLayout.hpp src/utils/ScaleChoices.hpp src/utils/ScaleChoices.cpp`, `cp .tmp/p5bt/Preferences.hpp.orig src/game/Preferences.hpp` и `cp .tmp/p5bt/Preferences.cpp.orig src/game/Preferences.cpp`; проверка уборки — `git show HEAD:src/game/Preferences.hpp | cmp - src/game/Preferences.hpp` и `git show HEAD:src/game/Preferences.cpp | cmp - src/game/Preferences.cpp`, каждая с кодом выхода 0, иначе блок `## Q-P5BT-05` и стоп. Ожидается: строк `error:` нет; код выхода не 0; в `ctest.log` провалены ровно девять тестов — все девять тестов `P5B ` из шага 1; остальные тесты — `Passed`.

Ошибка другого рода в файле теста (опечатка, неверный тип, неверный заголовок проекта) — корневая нить исправляет тест и повторяет прогон. Ошибки вне `tests/utils/test_OptionsMenu.cpp`, `tests/utils/test_Preferences.cpp` и `tests/CMakeLists.txt`, провал другого теста в прогоне B или любой из девяти тестов `P5B ` со статусом `Passed` или `Skipped` — блок `## Q-P5BT-02` с этими строками и стоп.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/utils/test_OptionsMenu.cpp tests/utils/test_Preferences.cpp tests/CMakeLists.txt > .tmp/p5bt/tests.sha256`. После этой команды файлы тестов не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p5bt/lfs status --short` выводит ровно три строки: ` M tests/CMakeLists.txt`, ` M tests/utils/test_Preferences.cpp` и `?? tests/utils/test_OptionsMenu.cpp`. Строки `__pycache__` в выводе допустимы; другие строки — блок `## Q-P5BT-03` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5BT | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- коды выхода прогонов A и B, их строки `error:`, вывод `grep -A3 "CMake Error"` и строки `ctest.log` из шага 2 (не больше 80 строк на прогон; если больше — первые 80 и их число);
- число проверок `CHECK` и `REQUIRE` в новых тестах — вывод `grep -cE '\b(CHECK|REQUIRE)\(' tests/utils/test_OptionsMenu.cpp` и вывод `git diff -U0 tests/utils/test_Preferences.cpp | grep -cE '^\+.*\b(CHECK|REQUIRE)(_FALSE)?\('`;
- содержимое `.tmp/p5bt/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — три файла шага 3, сообщение на английском о приёмочных тестах меню настроек: перенос теста раскладки форка, списки масштабов, запись `WorldScale` и двух масштабов в `preferences.ini`; последняя строка сообщения — `Behavior changes: none`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5bt --size`; у `.tmp/p5bt` пометка `оставить — хэши тестов нужны исполнителю`. Папки `.tmp/out` и `.tmp/deps` созданы до этой задачи и в раздел не входят. Ничего не удаляй, кроме временных правок прогона B.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → шаг 1 → шаг 2 (прогон A, затем прогон B) → шаг 3 → сдача и стоп.
- **Параллельно:** шаги зависят друг от друга, параллельных дорожек нет.
- **Помощники:** один субагент `gpt-6-luna` `xhigh`, без вложенных: шаг 2 — команды сборки, временные правки прогона B и их уборка, выписка строк ошибок. Бриф дословно содержит раздел «Шаг 2», абзац «Комментарии в коде» и запрет менять файлы, кроме временных правок прогона B и логов в `.tmp/p5bt/`. Шаги 1 и 3, разбор ошибок и сдачу делает корневая нить.
- **Остановки:** только на `## DONE-P5BT` и на блоках `## Q-P5BT-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5BT-04` и стоп.
- **Рамка правок:** `tests/utils/test_OptionsMenu.cpp`, `tests/utils/test_Preferences.cpp`, `tests/CMakeLists.txt`, временные правки прогона B и папка `.tmp/p5bt/`. Сборка пишет в `.tmp/out/` и `.tmp/deps/`; это не правка.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=2d86ef51aef14ab0cfe146d96e8768450f1161cc5c1f859bbf13ba4b7ae869e7 -->
## Обязательно: правила исполнителя

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Без фоновых команд: после остановки исполнителя никто его не разбудит. Длинные прогоны — в переднем плане, с таймаутом до 30 минут.
- Git по договорённости с ревьюером. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ревьюер после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ревьюера.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не трогать, секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Временные файлы — только в отведённой временной папке, в репозиторий и в корень рабочей копии ничего временного не класть. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Удалять что-либо вне своей временной папки — только по правилу «Уборка»; чужое, общее и постоянное — не удаляешь. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. В `DONE` — раздел «Рабочие места»: каждый созданный путь, его размер (`du -sh`) и что это — доказательство (на него ссылаются DONE, PR или журнал) или промежуточное. Объекты сборки, ненужные для повторной проверки, удаляешь только по правилу «Уборка»; до `CLEAN-OK` пути задачи не удаляешь.
- Уборка (владелец). В DONE — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер, назначение и пометка: `удалить` или `оставить — <почему>`; доказательства — только `оставить`. Удаляешь только после ответа ведущего-ревьюера `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; если в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`. Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- **Чтение (владелец).** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по журналу: обрезанный вывод — не чтение.
- Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; помощникам цель не ставить.

## Вопросы и остановки

Каждое препятствие сверяй в таком порядке:

1. Подходит под список «`Q` и стоп» — `Q` и стоп, даже если оно подходит и под список «Без вопроса».
2. Иначе подходит под список «Без вопроса» — решай сам и работай дальше.
3. Иначе: без ответа идущий подпункт выполнить нельзя — `Q` и стоп; можно — неблокирующий вопрос: запиши его в сдачу и работай дальше по списку, не простаивай.

`Q` в любом другом пункте этих правил — тоже «`Q` и стоп».

**`Q` и стоп.**
- ответ требует правки вне рамки правок, правки промптов, норм, governance, контрактов или замороженных тестов (файл, assert, смысл проверки);
- удаление данных, сеть или установка пакетов;
- смена цели, рамки или критерия готовности; новый механизм; решение по продукту;
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в DONE;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса (владелец).** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи и журнала хода не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий (владелец); исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи — строго по порядку списка.
- Замечания ревьюера выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения; DONE — один на задачу, после REVIEW — новый DONE.
- Если исполнитель коммитит — незаконченное хранить в своей ветке WIP-коммитом, а не патчами во временной папке. Голый `git stash` не использовать: список stash общий для всех рабочих копий и сессий.
- Перенос и переформатирование кода — отдельным коммитом, изменение поведения — следующим. «Без изменения поведения» писать, только если это правда.
- Последняя строка сообщения коммита — `Behavior changes: …` со списком или `Behavior changes: none`. Называть и мелочи: запасной вариант, удалённое поле, удалённую настройку в тесте, изменённый предел.
- Заголовок не преувеличивает: «finish», «complete» — только если пункт закрыт целиком; остатки назвать в теле.

## Тесты

- Тест проходит путь пользователя через тот вход продукта, которым пользуется пользователь в сценарии: для интерфейса — события мыши и клавиатуры, для API — вызов API. Тестируемый код не подменять заглушками.
- Тест проверяет поведение, а не совпадение хэша или вывода с прошлой сборкой. Изображения сравнивать с эталоном с допуском из задания, а если в задании его нет — из действующего эталонного теста или конфигурации сравнения; ни один источник допуск не задаёт — `Q`.
- Асинхронный результат ждать по нему самому (нужное значение, запись, пиксель), а не по косвенному флагу.
- Нестабильный тест разбирать сразу, с логом и санитайзером, если он уже настроен в проекте. «Не воспроизвелось» проблему не закрывает: исполнитель перечисляет её в сдаче с логом, issue заводит ведущий.
- Тесты пишут только в свои временные папки; общее состояние (синглтоны, кэши) сбрасывать перед каждым тестом.
- Общие помощники тестов и константы — в одном месте, не копировать по файлам.
- Сливать в целевую ветку только ветку с зелёным CI на её последнем коммите; после слияния проверить CI целевой ветки и красной её не оставлять.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Отчёт владельцу

- Три пункта на языке владельца — простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Эти три пункта — часть DONE; отдельного отчёта владельцу не создавать.

<!-- /team-process:executor-rules -->
