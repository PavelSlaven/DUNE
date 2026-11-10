# Сверка разведки П5г (Haiku)

Ревизии: FORK1 = 9208dcf5a358f40afd95c99480e4e09f781ed566, PORT = 7eb119b007c05f063fe6dacf2e93ae31ac135b33.
Команды выполнены из `C:\Users\Slaven\Projects\DUNE`, файлы таблиц не изменялись.

## Факт 1

- Таблица: api.tsv, строка 2 (№ 2)
- Утверждение: `src/debug/UiAudit.hpp:7` — предварительное объявление `class cGame;`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp | sed -n '7p'`
- Вывод:
```
class cGame;
```
- Итог: совпало

## Факт 2

- Таблица: api.tsv, строка 40 (№ 40)
- Утверждение: `src/debug/UiAudit.hpp:86` — `static bool mapViewport(const cGame &game, int &x, int &y, int &w, int &h);`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp | sed -n '86p'`
- Вывод:
```
    static bool mapViewport(const cGame &game, int &x, int &y, int &w, int &h);
```
- Итог: совпало

## Факт 3

- Таблица: api.tsv, строка 77 (№ 77)
- Утверждение: `src/debug/UiAuditScenes.hpp:29` — `const Scene *findScene(const std::string &id);`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.hpp | sed -n '29p'`
- Вывод:
```
const Scene *findScene(const std::string &id);
```
- Итог: совпало

## Факт 4

- Таблица: hooks.tsv, строка 5
- Утверждение: `src/cGame_logic.cpp:771` — в `cGame::run` вызов `uiaudit::isEnabled`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '771p'`
- Вывод:
```
        if (uiaudit::isEnabled()) {
```
- Итог: совпало

## Факт 5

- Таблица: hooks.tsv, строка 62
- Утверждение: `src/gamestates/cChooseHouseState.cpp:114` — `uiaudit::recordClick` с литералом `"house-harkonnen"`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp | sed -n '114p'`
- Вывод:
```
        uiaudit::recordClick("house-harkonnen", houseHarkonnen.getX(), houseHarkonnen.getY(), houseHarkonnen.getWidth(), houseHarkonnen.getHeight());
```
- Итог: совпало

## Факт 6

- Таблица: hooks.tsv, строка 123
- Утверждение: `src/utils/cScreenInit.cpp:127` — вызов `uiaudit::isEnabled`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp | sed -n '127p'`
- Вывод:
```
    if (uiaudit::isEnabled()) {
```
- Итог: совпало
- Примечание: имя `cScreenInit::getWindowedSize` в одной строке 127 не видно; проверен вызов.

## Факт 7

- Таблица: scenes.tsv, строка 2 (сцена main-menu)
- Утверждение: `src/debug/UiAuditScenes.cpp:363` — определение сцены `main-menu` (id из первой колонки)
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '363p'`
- Вывод:
```
    scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
```
- Итог: совпало
- Примечание: литерала `GAME_MENU` в строке 363 нет; таблица относит код действий к строке 132.

## Факт 8

- Таблица: scenes.tsv, строка 80 (сцена options-menu-main)
- Утверждение: `src/debug/UiAuditScenes.cpp:469` — определение сцены `options-menu-main` (id из первой колонки)
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '469p'`
- Вывод:
```
    scene("options-menu-main", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<0>,
```
- Итог: совпало
- Примечание: литералов `GAME_MENU` и `GAME_OPTIONS` в строке 469 нет.

## Факт 9

- Таблица: scenes.tsv, строка 158 (сцена game-ordos-list-upgrades)
- Утверждение: `src/debug/UiAuditScenes.cpp:568` — определение сцены `game-ordos-list-upgrades` (id из первой колонки)
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '568p'`
- Вывод:
```
    onGameScreen(scene("game-ordos-list-upgrades", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListUpgrades>), false),
```
- Итог: совпало
- Примечание: в строке литерал `uiaudit::ListUpgrades`, а не `LIST_UPGRADES`.

Критерий для факта 7–9 принят как id сцены из первой колонки. Если критерий — литералы из третьей колонки (`GAME_MENU`, `GAME_OPTIONS`, `LIST_UPGRADES`), то факты 7–9 не совпадают. Выбор критерия — вопрос владельцу.

## Факт 10

- Таблица: entry.tsv, строка 2 (FORK1, аргумент `--ui-audit-list`)
- Утверждение: `src/debug/UiAuditArguments.cpp:23` — распознавание `--ui-audit-list`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp | sed -n '23p'`
- Вывод:
```
        if (std::strcmp(argv[i], "--ui-audit-list") == 0) {
```
- Итог: совпало

## Факт 11

- Таблица: entry.tsv, строка 16 (FORK1, файл геометрии JSONL, объект label)
- Утверждение: `src/debug/UiAuditCapture.cpp:196` — запись объекта `label`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | sed -n '196p'`
- Вывод:
```
                file << "{\"k\":\"label\",\"kind\":\"" << escapeJson(entry.label) << "\",\"obj\":" << entry.obj
```
- Итог: совпало
- Примечание: в строке видны ключи k, kind, obj; ключи type, x, y, w, h, owner на следующих строках и не проверялись.

## Факт 12

- Таблица: entry.tsv, строка 30 (PORT, место вызова разбора аргументов в main)
- Утверждение: `src/main.cpp:94` — вызов `handleArg.handleArguments(argc, argv, settings.get())`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/main.cpp | sed -n '94p'`
- Вывод:
```
        int parseResult = handleArg.handleArguments(argc, argv, settings.get());
```
- Итог: совпало

## Факт 13

- Таблица: tools.tsv, строка 2 (`tests/UiAuditArgumentsTests.cpp`, строк 103)
- Утверждение: число строк файла 103
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UiAuditArgumentsTests.cpp | wc -l`
- Вывод:
```
103
```
- Итог: совпало

## Факт 14

- Таблица: tools.tsv, строка 19 (`tools/ui-audit/keys.tsv`, строк 169)
- Утверждение: число строк файла 169
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/keys.tsv | wc -l`
- Вывод:
```
169
```
- Итог: совпало

## Факт 15

- Таблица: tools.tsv, строка 36 (`tools/ui-audit/tests/test_run_all.py`, строк 70)
- Утверждение: число строк файла 70
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/tests/test_run_all.py | wc -l`
- Вывод:
```
70
```
- Итог: совпало

Итог: совпало 15 из 15
