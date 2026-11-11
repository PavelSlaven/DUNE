# Задание P5G3BC — сцены базы в бою в режиме отладки интерфейса (шаг П5г, часть 3б)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и три помощника `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g3b`, `HEAD` — `14308945` (приёмочные тесты этой части поверх `af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf`, части 3а шага П5г). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5g3bc/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Добавить в режим отладки интерфейса порта 35 сцен части 3б и пять новых записей режима по плану `PLAN-P5G3BC` ниже так, чтобы прошли замороженные приёмочные тесты этой части — скрипты `tests/ui_audit/ui_audit_part3b_catalog.py` и `tests/ui_audit/ui_audit_part3b_scenes.py` на установленной игре — и остались зелёными сборка (319 тестов), восемь скриптов Python частей 1, 2, 3а и 4 и весь набор `tools/ui-audit/tests`.

## Что уже решено

- Форк `9208dcf5a358f40afd95c99480e4e09f781ed566` (дальше — `FORK1`) написан на SDL2 и глобальных объектах игры (`global_map`, `mapCamera`, `players`, `unit`, `structure`, `drawManager`); порт — на SDL3 и объектах `cGame` (`m_gameObjectsContext`, `m_mapCamera`, `m_infoContext`, `m_drawManager`, `m_mouse`, `m_notificationArea`). Код форка переносится по плану и правилам переноса ниже, а не копируется.
- Часть 3б переносит из форка: перечисление `GameKind`, функцию `UiAuditAccess::prepareGameScreen` с её вспомогательными функциями (база со всеми зданиями, уровень технологий 9), функции сцен `withHud` и `prepareGame` и сцены `game-*`. Сцены — 29 сцен форка (`src/debug/UiAuditScenes.cpp@9208dcf:536,541-568`) и шесть новых сцен `game-sardaukar-list-<вид>` по образцу сцен `game-ordos-list-<вид>`.
- Не переносятся: сцены `game-music` и `game-command-*` (музыка — шаг П9, панель команд — шаг П10; в порту нет `MusicController` и `cCommandBarDrawer`), значения `Music`, `DamagedUnit`, `Harvester`, `Mcv` перечисления `GameKind`, функция `selectOnly`, функция `recordCommandBarClicks` и запись click `order-button`, функция `dropClicksUnderModal`.
- Своих записей для смысла этих сцен у форка нет. Код части 3б добавляет в порт пять новых записей, которых ждут тесты: метки `structure-selected` и `rally-point` (в `cDrawManager::drawRallyPoint`, `src/managers/cDrawManager.cpp@af6a2e1:223-252`), метку `place-cell` (в цикле клеток `cPlaceItDrawer::drawStatusOfStructureAtCell`, `src/drawers/cPlaceItDrawer.cpp@af6a2e1:139-183`; тип метки — цвет клетки: `Color::PlaceGood` → `GOOD`, `Color::PlaceNeutral` → `NEUTRAL`, `Color::PlaceBad` → `BAD`), метку `card-hover` (в ветке наведения на карточку `cBuildingListDrawer::drawList`, `src/drawers/cBuildingListDrawer.cpp@af6a2e1:553-568`) и область `selection-box` (в `cGamePlaying::drawCombatMouse`, `src/gamestates/cGamePlaying.cpp@af6a2e1:460-462`). Координаты рамки выделения у порта — закрытые поля `m_mouseCoX1`, `m_mouseCoY1`, `m_mouseCoX2`, `m_mouseCoY2` класса `cMouse` (`src/controls/cMouse.h@af6a2e1:138-141`), поэтому `cMouse` получает строку `friend class UiAuditAccess;`.
- Бой сцен — область 22 у всех четырёх Домов, как у форка: файлы `resources/bin/campaign/maps/scena022.ini`, `scenh022.ini`, `sceno022.ini`, `scens022.ini` есть в порту. Ведущий проверил: у игрока в этих файлах нет зданий; на клетках столбцов 20–40 и строк 22–33 нет зданий других игроков (ближайшие — четыре ракетные башни Ордоса на клетках столбцов 32–33 и строк 20–21 в `scenh022.ini` и `scens022.ini`); файлы `scena022.ini`, `scenh022.ini`, `sceno022.ini` порта совпадают с файлами `FORK1`. Сцены Сардаукаров идут на `scens022.ini`; у Сардаукаров список дворца не пуст (`SPECIAL_DEATHHAND`, `src/sidebar/cBuildingListUpdater.cpp@af6a2e1:476-478`).
- Порт ведёт себя в местах сцен так же, как форк: `cMiniMapDrawer::think` переводит мини-карту из `NOTAVAILABLE` в работу при радаре у игрока (`src/drawers/cMiniMapDrawer.cpp@af6a2e1:151-205`); энергия ветряной электростанции пропорциональна её здоровью (`src/gameobjects/structures/cWindTrap.cpp@af6a2e1:59-63`), поэтому `setHitPoints(1)` у всех ветряных электростанций оставляет игрока без энергии; клетки установки здания рисуются, только если место рядом со зданием игрока (`bWithinBuildDistance`, `src/drawers/cPlaceItDrawer.cpp@af6a2e1:99-136`); `cUnits::unitCreate` сам снимает выделение с нового юнита (`src/gameobjects/units/cUnits.cpp@af6a2e1:204`).

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- приёмочные тесты этой части: `tests/ui_audit/ui_audit_part3b_catalog.py`, `tests/ui_audit/ui_audit_part3b_scenes.py`;
- файлы режима порта: `src/debug/UiAudit.hpp`, `src/debug/UiAuditScenes.cpp`, `src/debug/UiAuditAccess.cpp`;
- файлы порта: `src/game/cGame.h`; `src/controls/cMouse.h`; строки 223–252 файла `src/managers/cDrawManager.cpp`; строки 70–185 файла `src/drawers/cPlaceItDrawer.cpp`; строки 458–475 файла `src/gamestates/cGamePlaying.cpp`; строки 238–280 и 553–568 файла `src/drawers/cBuildingListDrawer.cpp`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp | nl -ba | sed -n '16,38p'`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | nl -ba | sed -n '91,95p;313,318p;536,568p'`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '641,934p'`.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт поведения

Этот раздел дословно взят из задания приёмочных тестов `TASK-G3BT`.

Пункты 1–12 контрактов частей 1, 2 и 3а действуют без изменений; скрипты частей 1, 2, 3а и 4 в `tests/ui_audit/` остаются зелёными. Игра запускается так же, как в пункте 2 части 1.

13. **Каталог части 3б.** В выводе `--ui-audit-list` у каждой сцены ровно ключи части 1. Среди сцен, у которых `id` начинается с `game-`, нет двух с одним `id`, и эти сцены ровно совпадают по `id` и значениям всех ключей с 35 сценами ниже. У каждой из 35 сцен `group` — `game-playing`, `state` — `GAME_PLAYING`, `screen` — `cGamePlaying`, `game_screen` — `true`, `readiness` — `FixedFrames(5, no readiness flag)`; `hud` — `true` только у `game-hud`; `hd_only` — `true` только у `game-list-scroll-end`; `hover` — `{"x": 0, "y": 0}` у `game-place-allowed`, `game-place-forbidden`, `game-group-select` и `game-item-hover` и `null` у остальных; `house` — `harkonnen` у сцен `game-harkonnen-list-<вид>`, `ordos` у `game-ordos-list-<вид>`, `sardaukar` у `game-sardaukar-list-<вид>` и `atreides` у остальных. Сцены: `game-list-<вид>`, `game-harkonnen-list-<вид>`, `game-ordos-list-<вид>`, `game-sardaukar-list-<вид>` (`<вид>` — каждое из `build`, `infantry`, `vehicles`, `starport`, `palace`, `upgrades`), `game-hud`, `game-structure-selected`, `game-radar-none`, `game-radar-nopower`, `game-place-allowed`, `game-place-forbidden`, `game-group-select`, `game-messages`, `game-item-hover`, `game-list-scroll-end`, `game-rally-point`. Покрытие экранов — как в пункте 10: итоговый список содержит только восемь строк экранов части 3в.

14. **Прогон сцены части 3б.** Для каждой из 35 сцен пункта 13 — всё, что пункт 11 требует от сцен части 3а с `game_screen` `true`: код выхода 0 не позже чем через 120 секунд, файлы `<id>.png` и `<id>.geometry.jsonl`, PNG и заголовок как там, ключ `map_viewport` со значением `{"x": 0, "y": 42, "w": 520, "h": 558}`, записи пяти видов с теми же ключами и ограничениями, нет файла `preferences.ini` в папке `XDG_DATA_HOME`.

15. **Записи сцен части 3б.** «Одна запись», «внутри» и «прямоугольник (x, y, w, h)» — как в пункте 12; у записи `label` её имя — значение `kind`. Прямоугольники A и B «пересекаются», если `A.x < B.x + B.w`, `B.x < A.x + A.w`, `A.y < B.y + B.h` и `B.y < A.y + A.h`. «Номер» записи click `list-button:<n>` или `build-item:<n>` — число `<n>`, записанное десятичными цифрами без знака и без ведущих нулей (как `std::to_string` пишет неотрицательное целое).
    - Каждая сцена части 3б:
      - одна запись area `top-panel` с прямоугольником (0, 0, 800, 42); одна запись area `sidebar` с прямоугольником (520, 42, 280, 558); одна запись area `build-list` внутри прямоугольника `sidebar`; одна запись click `top-options` с прямоугольником (7, 4, 126, 33); нет записи click `order-button`;
      - каждая запись click, у которой `name` начинается с `list-button:` или `build-item:` либо равно `build-scrollbar`, лежит внутри прямоугольника `sidebar`; есть хотя бы одна запись click, у которой `name` начинается с `list-button:` или `build-item:`;
      - у каждой записи label `kind` — одно из `structure-health`, `structure-selected`, `rally-point`, `place-cell`, `card-hover` (меток юнитов нет: юниты базы не выделены);
      - запись area `selection-box` есть только у `game-group-select`; записи label `place-cell` — только у `game-place-allowed` и `game-place-forbidden`; `card-hover` — только у `game-item-hover`; `structure-selected` — только у `game-structure-selected` и `game-rally-point`; `rally-point` — только у `game-rally-point`.
    - Радар. У каждой сцены, кроме `game-radar-none`, одна запись area `minimap` внутри прямоугольника `sidebar` и одна запись click `minimap` с тем же прямоугольником (у игрока есть радар; в `game-radar-nopower` ему не хватает энергии, и порт всё равно рисует мини-карту, `src/drawers/cMiniMapDrawer.cpp@dc6e5ff:116-130`). У `game-radar-none` нет записей area и click `minimap`.
    - Списки. У сцены `game-list-<вид>`, `game-harkonnen-list-<вид>`, `game-ordos-list-<вид>`, `game-sardaukar-list-<вид>` выбран список с номером `<n>`: `build` — 1, `infantry` — 2, `vehicles` — 3, `starport` — 4, `palace` — 5, `upgrades` — 6 (номера списков порта, `src/include/enums/ListEnums.h@af6a2e1:44-63`). У такой сцены нет записи click `list-button:<n>` (кнопку выбранного списка режим не записывает, `src/debug/UiAuditAccess.cpp@af6a2e1:297-309`); есть хотя бы одна запись click `list-button:<m>`; номер каждой записи click `list-button:<m>` — целое от 1 до 6; есть хотя бы одна запись click `build-item:<i>`.
    - `game-structure-selected`: одна запись label `structure-selected`; её `type` — `STRUCTURE`, `w` > 0, `h` > 0.
    - `game-rally-point`: одна запись label `structure-selected` с тем же требованием и одна запись label `rally-point`, у которой `type` — `STRUCTURE`, `w` > 0, `h` > 0, `obj` равно `obj` записи `structure-selected`, `owner` равен `owner` записи `structure-selected` (тот же прямоугольник здания), а прямоугольник `rally-point` не пересекается с этим `owner` (точка сбора стоит на клетке в стороне от здания).
    - `game-place-allowed`: ровно четыре записи label `place-cell` (ветряная электростанция — 2 × 2 клетки), у всех одно значение `obj`, у каждой `w` > 0 и `h` > 0, `type` каждой — `GOOD` или `NEUTRAL`.
    - `game-place-forbidden`: ровно четыре записи label `place-cell`, у всех одно значение `obj`, у каждой `w` > 0 и `h` > 0, `type` каждой — `GOOD`, `NEUTRAL` или `BAD`, и хотя бы у одной — `BAD`.
    - `game-group-select`: одна запись area `selection-box` внутри прямоугольника (0, 42, 520, 558) — области карты.
    - `game-messages`: записи text, у которых `s` равно `Construction complete: the Windtrap is ready to be placed`, `Neutral notification`, `Priority notification: Harvester is full` и `Bad news: a structure is under attack` — по одной на каждую из четырёх строк.
    - `game-item-hover`: одна запись label `card-hover`; её `obj` — 2, `type` — `ITEM`; точка (x + w // 2, y + h // 2) её прямоугольника лежит в прямоугольнике единственной записи click `build-item:2` (`X ≤ x < X + W`, `Y ≤ y < Y + H`).
    - `game-list-scroll-end`: одна запись click `build-scrollbar`; есть хотя бы одна запись click `build-item:<i>`; нет записи click `build-item:0`; наибольший номер записей click `build-item:<i>` этой сцены больше наибольшего номера записей click `build-item:<i>` сцены `game-list-build`.

## Правила переноса

Строки форка, которые план велит перенести, меняются только по этим правилам:

1. В функциях `UiAuditAccess` и вспомогательных функциях `src/debug/UiAuditAccess.cpp` имя параметра `game` → `currentGame`, как в функциях частей 1–3а того же файла. Каждая перенесённая вспомогательная функция строк 643–776 `FORK1`, кроме `listForKind` (она не обращается к игре; лишний параметр дал бы предупреждение `-Wunused-parameter`, а сборка CI идёт с `-Werror`), получает первым параметром `cGame &currentGame`, и каждый вызов этих функций и функций `cellAt`, `revealAround` части 3а передаёт `currentGame` первым аргументом.
2. Замены имён форка:
   - `global_map.isValidCell(<c>)` → `currentGame.m_gameObjectsContext->getMap()->getGeometry()->isValidCell(<c>)`; другие `global_map.<функция>(` → `currentGame.m_gameObjectsContext->getMap()-><функция>(`;
   - `mapCamera->` → `currentGame.m_mapCamera->`; `drawManager->` → `currentGame.m_drawManager->`;
   - `players[HUMAN].addNotification(<текст>, <тип>)` → `currentGame.m_notificationArea->addNotification(<текст>, <тип>)`; другие `players[HUMAN].` → `player->`, где `player` — локальная переменная `cPlayer *player = currentGame.m_gameObjectsContext->getPlayer(HUMAN);` (место её объявления — в плане, шаг 3);
   - `structure[<i>]` → `currentGame.m_gameObjectsContext->getStructures()[<i>]`; `unit[<i>].` → `currentGame.m_gameObjectsContext->getUnit(<i>)->`;
   - `cStructureFactory::getInstance()->createStructure(` → `currentGame.m_gameObjectsContext->getStructureFactory()->createStructure(`;
   - `UNIT_CREATE(<клетка>, <тип>, HUMAN, true, false, <доля>)` → `cUnits::unitCreate(currentGame.m_gameObjectsContext.get(), currentGame.m_infoContext.get(), currentGame.m_eventEmitter.get(), <клетка>, <тип>, HUMAN, true, false, <доля>)`;
   - `structureUtils.getWidthOfStructureTypeInCells(<t>)` → `currentGame.m_infoContext->getStructureInfo(<t>).bmp_width / TILESIZE_WIDTH_PIXELS`; `structureUtils.getHeightOfStructureTypeInCells(<t>)` → `currentGame.m_infoContext->getStructureInfo(<t>).bmp_height / TILESIZE_HEIGHT_PIXELS` (та же формула, что у `cStructureUtils`, `src/utils/cStructureUtils.cpp@af6a2e1:52-64`; макросы — `src/gameobjects/map/cMap.h@af6a2e1:28-29`);
   - `game.getMouse()` → `currentGame.m_mouse.get()`; поля `mouse_co_x1`, `mouse_co_y1`, `mouse_co_x2`, `mouse_co_y2` → `m_mouseCoX1`, `m_mouseCoY1`, `m_mouseCoX2`, `m_mouseCoY2`.
3. Прочие правила переноса частей 1–3а действуют: `assert(` → `d2tm_assert(`; `logbook(...)` форка не переносится; `localization::text("<английский>", "<русский>")` → `"<английский>"`; подключения — пути порта от папки `src`.
4. Вызов форка, у которого в порту нет пары по правилам 1–3 и плану, — подбери вызов порта с тем же действием в рамке правок и запиши строкой «Решено исполнителем» (файл:строка порта, вызов форка → вызов порта, основание — строка порта, где этот вызов уже делает то же действие). Нет вызова порта с тем же действием — блок `## Q-P5G3BC-NN` и стоп.

## PLAN-P5G3BC

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `src/debug/UiAudit.hpp` | (а) В пространстве имён `uiaudit` сразу перед строкой `struct Rect {` — перечисление `GameKind` строк 16–38 `FORK1` без четырёх строк `Music,`, `DamagedUnit,`, `Harvester,`, `Mcv,` (остаются 17 значений от `Hud` до `Rally` в порядке форка), за ним пустая строка. (б) В классе `UiAuditAccess` сразу после строки `static bool placeStructure(cGame &game, int edge);` — строка `static bool prepareGameScreen(cGame &game, int house, int kind);`. Других правок в файле нет. | помощник A |
| 2 | `src/debug/UiAuditScenes.cpp` | (а) Сразу после функции `hdOnly` — функция `withHud` строк 91–95 `FORK1` без изменений. (б) Сразу после шаблонной функции `prepareStructureLabel` — шаблонная функция `prepareGame` строк 313–318 `FORK1` без изменений. (в) В конец `g_catalog`, после сцены `units-label-saboteur`, — 35 строк в этом порядке: строка 536 `FORK1`; строки 541–568 `FORK1`; затем шесть строк — копии строк 563–568 `FORK1`, в которых `game-ordos-list-` заменено на `game-sardaukar-list-`, `"ordos"` — на `"sardaukar"`, `ORDOS` — на `SARDAUKAR`. Строки 537–540 `FORK1` не переносятся. Других правок в файле нет. | помощник A |
| 3 | `src/debug/UiAuditAccess.cpp` | (а) Сразу после строки `#include "sidebar/cSideBar.h"` — десять строк подключений в этом порядке: `"controls/cMouse.h"`, `"controls/mousestates/eMouseStates.h"`, `"data/gfxdata.h"`, `"drawers/cMiniMapDrawer.h"`, `"game/cNotificationArea.h"`, `"gameobjects/structures/cAbstractStructure.h"`, `"gameobjects/structures/cStructures.h"`, `"include/eNotificationType.h"`, `"sidebar/cBuildingListItem.h"`, `"sidebar/cBuildingListUpdater.h"` (каждая в форме `#include "<путь>"`). (б) В конце файла — анонимное пространство имён с функциями и константами строк 643–776 `FORK1` по правилам переноса 1–3, с такими отличиями: в `spawnUnit` нет строк 698–700; `buildBase` имеет параметры `cGame &currentGame, bool withRadar, BaseResult &result`, первая строка её тела — `cPlayer *player = currentGame.m_gameObjectsContext->getPlayer(HUMAN);`, строка 735 `FORK1` заменена на `result.tankId = spawnUnit(currentGame, TANK, 25, kStreetRow, 1.0f);`; функция `selectOnly` (строки 756–763) не переносится. (в) После этого пространства имён — функция `bool UiAuditAccess::prepareGameScreen(cGame &currentGame, int house, int kind)` строк 780–934 `FORK1` по правилам переноса 1–3, с такими отличиями: сразу после блока `if (!enterPlaying(currentGame, house, 22)) { return false; }` — строка `cPlayer *player = currentGame.m_gameObjectsContext->getPlayer(HUMAN);`; строка 788 `FORK1` заменена на `if (!buildBase(currentGame, withRadar, base)) {`; ветви `case GameKind::Music:` (строки 827–842) и `case GameKind::DamagedUnit:`, `case GameKind::Harvester:`, `case GameKind::Mcv:` (строки 843–851) не переносятся. Других правок в файле нет. | помощник A |
| 4 | `src/controls/cMouse.h` | Строка `    friend class UiAuditAccess;` сразу после строки `class cMouse {`. | помощник B |
| 5 | `src/managers/cDrawManager.cpp` | В функции `cDrawManager::drawRallyPoint` (подключение `debug/UiAudit.hpp` в файле уже есть). (а) Сразу после строки `if (!theStructure) return;` — блок: `const uiaudit::Rect auditStructure{theStructure->iDrawX(), theStructure->iDrawY(), static_cast<int>(m_mapCamera->factorZoomLevel(theStructure->getWidthInPixels())), static_cast<int>(m_mapCamera->factorZoomLevel(theStructure->getHeightInPixels()))};` и `if (uiaudit::isEnabled()) { uiaudit::recordLabel("structure-selected", m_player->selected_structure, "STRUCTURE", auditStructure.x, auditStructure.y, auditStructure.w, auditStructure.h, auditStructure); }` (прямоугольник здания — тот же, что у `cStructureUtils::isMouseOverStructure`, `src/utils/cStructureUtils.cpp@af6a2e1:282-293`). (б) Сразу после строки `cRectangle dest = {drawX, drawY, rallyPointWidthScaled, rallyPointHeightScaled};` — `if (uiaudit::isEnabled()) { uiaudit::recordLabel("rally-point", m_player->selected_structure, "STRUCTURE", dest.getX(), dest.getY(), dest.getWidth(), dest.getHeight(), auditStructure); }`. Других правок в файле нет. | помощник B |
| 6 | `src/drawers/cPlaceItDrawer.cpp` | Подключение `#include "debug/UiAudit.hpp"` сразу после строки `#include "cPlaceItDrawer.h"`. В функции `drawStatusOfStructureAtCell`, внутри цикла `for (int iY=0; iY < cellHeight; iY++) {`: (а) сразу после первой строки тела этого цикла `itemToPlaceColor = Color::PlaceNeutral;` — `const char *auditType = "NEUTRAL";`; (б) сразу после каждой из трёх строк `itemToPlaceColor = Color::PlaceBad;` этого цикла — `auditType = "BAD";`; сразу после строки `itemToPlaceColor = Color::PlaceGood;` — `auditType = "GOOD";`; (в) сразу перед строкой `m_sdlDrawer->renderRectFillColor(iDrawX+posX, iDrawY+posY, desiredWidth, desiredHeight,itemToPlaceColor);` — `if (uiaudit::isEnabled()) { uiaudit::recordLabel("place-cell", structureId, auditType, static_cast<int>(iDrawX + posX), static_cast<int>(iDrawY + posY), static_cast<int>(desiredWidth), static_cast<int>(desiredHeight), uiaudit::Rect{iDrawX, iDrawY, static_cast<int>(cellWidth * desiredWidth), static_cast<int>(cellHeight * desiredHeight)}); }`. Строку `itemToPlaceColor = Color::PlaceNeutral;` вне цикла (в ветке `if (!bWithinBuildDistance) {`) не трогай. Других правок в файле нет. | помощник B |
| 7 | `src/gamestates/cGamePlaying.cpp` | Подключение `#include "debug/UiAudit.hpp"` сразу после строки `#include "gamestates/cGamePlaying.h"`. В функции `cGamePlaying::drawCombatMouse` первой строкой тела ветки `if (m_mouse->isBoxSelecting()) {` — `if (uiaudit::isEnabled()) { const cRectangle box = m_mouse->getBoxSelectRectangle(); uiaudit::recordArea("selection-box", box.getX(), box.getY(), box.getWidth(), box.getHeight()); }`. Других правок в файле нет. | помощник B |
| 8 | `src/drawers/cBuildingListDrawer.cpp` | Подключение `#include "debug/UiAudit.hpp"` сразу после строки `#include "cBuildingListDrawer.h"`. В функции `cBuildingListDrawer::drawList(cBuildingList *list, const bool shouldDrawStructureSize)` первой строкой тела ветки `if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {` — `if (uiaudit::isEnabled()) { uiaudit::recordLabel("card-hover", i, "ITEM", iDrawX, iDrawY, iDrawXEnd - iDrawX, iDrawYEnd - iDrawY, uiaudit::Rect{card.getX(), card.getY(), card.getWidth(), card.getHeight()}); }` (`i` — номер карточки в цикле этой функции, `card` — её прямоугольник, `src/drawers/cBuildingListDrawer.cpp@af6a2e1:264-278`). Других правок в файле нет. | помощник B |
| 9 | — | Проверки раздела «Проверки» по порядку. | помощник D |

## Проверки

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`.

1. `sha256sum -c .tmp/p5g3bt/tests.sha256` — восемь строк `OK`.
2. `df -m /srv` — в столбце `Available` не меньше 5000, иначе блок `## Q-P5G3BC-01` и стоп. Сборка: `DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5g3bc/build.log 2>&1; echo exit=$?` — `exit=0`; итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of 319`.
3. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -E 'src/debug/|cMouse|cDrawManager|cPlaceItDrawer|cGamePlaying|cBuildingListDrawer'` — пустой вывод.
4. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`; файл `.tmp/out/xdg/D2TM/Dune II - The Maker/preferences.ini` есть.
5. Для каждого скрипта `<скрипт>` из `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_tools_run_combo.py`, `ui_audit_part2_catalog.py`, `ui_audit_part2_scenes.py`, `ui_audit_part3a_catalog.py`, `ui_audit_part3a_scenes.py`, `ui_audit_part3b_catalog.py`, `ui_audit_part3b_scenes.py`: `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p5g3bc/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
6. `mkdir -p .tmp/p5g3bc/tmp && (cd tools/ui-audit && TMPDIR=$PWD/../../.tmp/p5g3bc/tmp python3 -B -m unittest discover -s tests) > .tmp/p5g3bc/run-j.log 2>&1; echo exit=$?` — `exit=0`, последняя строка `.tmp/p5g3bc/run-j.log` — `OK`. После проверок 5 и 6 — `rm -r tests/ui_audit/__pycache__ tools/ui-audit/tests/__pycache__` для тех из двух папок, что появились.
7. Сверки `grep` (в скобках — ожидаемый вывод):
   - `grep -rn -E 'localization|d2tmc\.h|renderDrawer|SDL2/|logbook|global_map|UNIT_CREATE|players\[|unit\[|structure\[|getInstance\(\)|structureUtils|getMouse\(\)|mouse_co_' src/debug` (пусто);
   - `grep -rn -E 'DamagedUnit|Mcv|MusicController|selectOnly|game-music|game-command|recordCommandBarClicks|dropClicksUnderModal|order-button|writeSaves|clearMouseClicks|remove_all' src/debug` (пусто);
   - `grep -c -E '^ +(Hud|Structure|ListBuild|ListInfantry|ListVehicles|ListStarport|ListPalace|ListUpgrades|RadarNone|RadarNoPower|PlaceAllowed|PlaceForbidden|GroupSelect|Messages|ItemHover|ScrollEnd|Rally),?$' src/debug/UiAudit.hpp` (17);
   - `grep -c 'scene("game-' src/debug/UiAuditScenes.cpp` (35);
   - `grep -c 'friend class UiAuditAccess' src/controls/cMouse.h` (1);
   - `grep -o -h -E '"(structure-selected|rally-point|place-cell|card-hover|selection-box)"' src/managers/cDrawManager.cpp src/drawers/cPlaceItDrawer.cpp src/gamestates/cGamePlaying.cpp src/drawers/cBuildingListDrawer.cpp | sort | uniq -c` (по 1 у `"card-hover"`, `"place-cell"`, `"rally-point"`, `"selection-box"`, `"structure-selected"`).
8. `git -c lfs.storage=$PWD/.tmp/p5g3bc/lfs status --short` — только файлы рамки правок.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P5G3BC-NN` с выводом и стоп. Тест не подгоняй и не меняй: файлы из `.tmp/p5g3bt/tests.sha256` заморожены. Подготовка сцены вернула `false` (скрипт сообщает об ошибке сцены, а журнал игры — о неудаче подготовки) — тоже блок `## Q-P5G3BC-NN` с именем сцены и строками журнала, без правок вне плана.

## Сдача

Последнее сообщение — блок `## DONE-P5G3BC | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p5g3bc/progress.md`): строка на каждый шаг плана;
- вывод каждой проверки 1–8 с кодами выхода (не больше 40 строк на проверку);
- `git diff --stat` и список для коммита: один пункт — все файлы рамки правок, сообщение на английском о сценах базы в бою режима отладки интерфейса и новых записях `structure-selected`, `rally-point`, `place-cell`, `card-hover`, `selection-box`, последняя строка — `Behavior changes: …` со списком;
- раздел «Решено исполнителем» — каждая строка по правилу переноса 4;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3bc --size`; у `.tmp/p5g3bc` пометка `оставить — логи проверок нужны ревью`. Папки `.tmp/out`, `.tmp/deps`, `.tmp/p5g3bt` созданы до этой задачи и в раздел не входят; копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → шаги 1–3 (помощник A) и шаги 4–8 (помощник B) одновременно → шаг 9 (помощник D) → сдача и стоп.
- **Параллельно:** помощники A и B правят разные файлы и не ждут друг друга. Помощник D начинает, когда A и B сдали свои шаги.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных; одновременно работают не больше двух. В бриф каждого дословно входят разделы «Что уже решено», «Контракт поведения», «Правила переноса», его строки таблицы `PLAN-P5G3BC` (помощнику D — раздел «Проверки»), абзац «Комментарии в коде» и запрет править файлы вне своих строк плана и `.tmp/p5g3bc/`. Корневая нить сама не правит код, не запускает сборку и проверки: механику — правки, сборку, проверки, выписку логов — делают только помощники; корневая нить читает раздел «Прочитать до работы», раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников, отвечает на вопросы помощников в рамке плана и сдаёт. Ошибку сборки в файле помощника A или B корневая нить отдаёт тому же помощнику.
- **Остановки:** только на `## DONE-P5G3BC` и на блоках `## Q-P5G3BC-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5G3BC-08` и стоп.
- **Рамка правок:** `src/debug/UiAudit.hpp`, `src/debug/UiAuditScenes.cpp`, `src/debug/UiAuditAccess.cpp`, `src/controls/cMouse.h`, `src/managers/cDrawManager.cpp`, `src/drawers/cPlaceItDrawer.cpp`, `src/gamestates/cGamePlaying.cpp`, `src/drawers/cBuildingListDrawer.cpp` и папка `.tmp/p5g3bc/`. Понадобился другой файл — блок `## Q-P5G3BC-NN` и стоп. Сборка пишет в `.tmp/out/` и `.tmp/deps/`, игра — в `.tmp/out/run/bin/` и временные папки скриптов; это не правка.

Не отступай от плана, не переусложняй.

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
