# Выборочная сверка RECON.md (P10R) с кодом

Источник: `C:\Users\Slaven\Projects\DUNE\codex-direct\P10\recon\RECON.md` (413 строк, прочитан целиком).
Репозиторий не менялся. Команды: `git -C C:/Users/Slaven/Projects/DUNE show <полный sha>:<путь> | nl -ba | sed -n '<диапазон>p'`. Скрипт, выполнивший команды: `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\p10r\spot.sh`.

Обозначения sha: FORK1 = 9208dcf5a358f40afd95c99480e4e09f781ed566; UP1 = d06f2fcd2a347182c3774fb96e9a85570405c489; PORT = 832c953a94a632d57872349013f7ed1a37434715.

| № | пункт отчёта | утверждение (кратко) | команда | вывод (до 2 строк) | совпало / не совпало |
|---|---|---|---|---|---|
| 1 | 1 | CommandBindingAction: Attack, Repair, Unload, Deploy, Rally, Release (`CommandBindings.hpp@9208dcf:11`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/CommandBindings.hpp \| sed -n '11,17p'` | `11 enum class CommandBindingAction {` / `12     Attack,` | совпало |
| 2 | 1 | Шесть ключей KeyAttack…KeyRelease читаются из ini (`common.cpp@9208dcf:110–127`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/common.cpp \| sed -n '110,127p'` | `110     if (section.hasValue("KeyAttack"))` / `113     if (section.hasValue("KeyRepair"))` | совпало |
| 3 | 2 | ActionCount равен 7 (`CommandBarLayout.hpp@9208dcf:8–12`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CommandBarLayout.hpp \| sed -n '8,12p'` | `9     static constexpr int ActionCount = 7;` / `12     std::array<cRectangle, ActionCount> actions{};` | совпало |
| 4 | 2 | isRepairCommandEnabled() безусловно возвращает true (`CommandBarPolicy.hpp@9208dcf:13–16`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CommandBarPolicy.hpp \| sed -n '13,16p'` | `13 [[nodiscard]] constexpr bool isRepairCommandEnabled()` / `15     return true;` | совпало |
| 5 | 3 | В состояние игры добавлен m_commandBindings (`src/cGame.h@9208dcf:85`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h \| sed -n '85p'` | `85     CommandBindings m_commandBindings;` | совпало |
| 6 | 3 | DrawManager подключает cCommandBarDrawer (`src/managers/cDrawManager.h@9208dcf:5`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.h \| sed -n '5p'` | `5 #include "drawers/cCommandBarDrawer.h"` | совпало |
| 7 | 4 | switchOptionsPage сбрасывает захват и сообщение (`cOptionsState.cpp@9208dcf:658–664`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp \| sed -n '658,664p'` | `660     m_bindingCapture.reset();` / `661     m_bindingMessage.clear();` | совпало |
| 8 | 4 | commandBindingKeysMatch: L/R Shift и L/R Alt конфликтуют, L/R Ctrl не объединяются (`CommandBindings.hpp@9208dcf:31–44`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/CommandBindings.hpp \| sed -n '31,44p'` | `38     if ((first == SDL_SCANCODE_LSHIFT ...` / `42     return (first == SDL_SCANCODE_LALT ...` (ветки для Ctrl нет) | совпало |
| 9 | 5 | Конструктор cOptionsState вызывает initializeDisplaySettings(), которая читает settings.ini (`cOptionsState.cpp@9208dcf:77–105`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp \| sed -n '77,105p'` | `83     initializeDisplaySettings();` / `104     const std::unique_ptr<GameSettings> settings = loadSettingsFromIni("settings.ini");` | совпало |
| 10 | 5 | Место в UP1 для «initializeDisplaySettings вызывается только при создании» (`cOptionsState.cpp@d06f2fc:39`) | `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cOptionsState.cpp \| sed -n '39p'`; дополнительно `git -C C:/Users/Slaven/Projects/DUNE grep -n initializeDisplaySettings d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/gamestates/cOptionsState.cpp` | `39 cOptionsState::cOptionsState(sGameServices* services, int prevState)` / grep: пустой вывод (имени нет в файле) | не совпало: строка 39 — только сигнатура конструктора UP1; вызова initializeDisplaySettings в этом файле UP1 нет |
| 11 | 6 | isStarportCatalogAvailable — constexpr-предикат, возвращающий аргумент (`StarportOrderQueue.hpp@9208dcf:76`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/StarportOrderQueue.hpp \| sed -n '76,78p'` | `76 constexpr bool isStarportCatalogAvailable(bool hasStarport) {` / `77     return hasStarport;` | совпало |
| 12 | 6 | Процессор передаёт очереди константу kMaxItemsToOrder = 8 из `cOrderProcesser.h@9208dcf:31` | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cOrderProcesser.h \| sed -n '31p'`; дополнительно `git -C C:/Users/Slaven/Projects/DUNE grep -n kMaxItemsToOrder 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src` | `31      * @return` / grep: `cOrderProcesser.h:10: static constexpr auto kMaxItemsToOrder = 8;`, `:66: StarportOrderQueue<kMaxItemsToOrder> orderedItems;` | не совпало: строка 31 — комментарий `@return`; значение 8 верное, но определение на строке 10, использование на строке 66 |
| 13 | 7 | MAX_UNITS_CAPACITY = 300 в PORT (`src/gameobjects/units/cUnits.h@832c953:70`) | `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/units/cUnits.h \| sed -n '70p'` | `70     static constexpr int MAX_UNITS_CAPACITY = 300;` | совпало |
| 14 | 8 | Регистрация CTest command_bindings (`CMakeLists.txt@9208dcf:184`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt \| sed -n '184p'` | `184     add_test(NAME command_bindings COMMAND command_bindings_tests)` | совпало |
| 15 | 8 | Регистрация mouse_click_init_tests через add_unit_frame_test (`tests/UnitRenderFixture.cmake@9208dcf:130`) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake \| sed -n '130p'` | `130 add_unit_frame_test(mouse_click_init_tests mouse_click_init MouseClickInitTests.cpp recorded)` | совпало |

## Проверка числа 1: участки diff в hooks.tsv

Файл `C:\Users\Slaven\Projects\DUNE\codex-direct\P10\recon\hooks.tsv`: всего 42 строки, из них 1 заголовок (`путь в FORK1 <TAB> путь@9208dcf:строка ...`). Строк данных (без заголовка, непустых) — 41.

Итог: совпало с числом 41 из отчёта (RECON.md, пункт 3).

## Проверка числа 2: «40 проверок» в тестах пункта 8

Команда из отчёта: скрипт `count_checks.py` (в отчёте текст скрипта приведён, сам файл удалён; воспроизведён по тексту отчёта в `...\scratchpad\p10r\count_checks.py`). Запущен локально с cwd = репозиторий, ревизия FORK1 = 9208dcf5a358f40afd95c99480e4e09f781ed566, интерпретатор `C:/Users/Slaven/AppData/Local/Programs/Python/Python313/python` (на servak — `/srv/dune/venv/bin/python`, в отчёте не повторялось).

Вывод:
```
tests/CommandBarLayoutTests.cpp: assert/check/fail macros=0; if-guards=8; require-calls=0; counted checks=8
tests/CommandBindingConflictTests.cpp: assert/check/fail macros=0; if-guards=7; require-calls=0; counted checks=7
tests/CommandBindingsTests.cpp: assert/check/fail macros=0; if-guards=7; require-calls=0; counted checks=7
tests/InteractionRegressionTests.cpp: assert/check/fail macros=0; if-guards=1; require-calls=16; counted checks=16
tests/MouseClickInitTests.cpp: assert/check/fail macros=0; if-guards=2; require-calls=0; counted checks=2
TOTAL=40
```
Совпадает с выводом в RECON.md, строки 395–399 (построчно), и с итогом «40» (строка 402). Сумма 8+7+7+16+2 = 40.

Итог: совпало.

Итог: 13 из 15 совпало.
