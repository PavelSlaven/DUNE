# Задание P8 — сохранения форка в порту (шаг П8)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p8`, ветка `codex/p8`, `HEAD` — `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6` (вершина ветки порта `port/up-d06f2fcd`). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p8/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p8/` (дальше — «папка задания»).

## Цель

В бою `F5` записывает быстрое сохранение в файл `saves/quicksave.d2s` рядом с игрой и показывает уведомление «Игра сохранена.» («Game saved.»), `F9` загружает его и показывает «Игра загружена.» («Game loaded.»); пятая закладка камеры переехала на `F6` (перейти) и `Alt+F6` (запомнить). В главном меню на месте неактивной кнопки «Загрузить» стоит кнопка «Сохранения» («Saved games»): она включена, когда есть хотя бы одно корректное сохранение, и открывает окно из 10 слотов для загрузки. В меню настроек, открытом из боя, работают кнопки «Сохранить игру» и «Загрузить игру». Сохранения версий `v0.8.0-ru-hd.3`–`hd.10` в списке слотов помечены «<повреждено>». Сохранение записывает всё состояние боя из таблицы пункта 4 контракта. Готово, когда новые тесты Catch2 `[P8]`, скрипт `tests/ui_audit/ui_audit_saves.py` (сцены сохранений и круг «быстрое сохранение → быстрая загрузка → быстрое сохранение» с одинаковыми файлами) и сборка со всеми тестами зелёные.

## Что уже решено

Ревизия `B` = `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6`; её дерево равно дереву `a1e63b860482d7e7a82e502359965e2caefd6470`. Ревизия форка `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`. Все номера строк порта ниже — файлов ревизии `B`; номера строк форка помечены `FORK1:`.

- **Решение владельца Р78** (`docs/decisions.md`, 2026-11-12): сохранения `hd.9` и `hd.10` несовместимы, как `hd.7` по Р5; новая версия формата, конвертера нет; файл старой версии в списке слотов помечен как повреждённый. Файлы — в папке `saves` рядом с игрой, рабочий каталог игры — каталог исполняемого файла. Быстрое сохранение — `F5`, быстрая загрузка — `F9`; пятая закладка камеры — `F6` и `Alt+F6`.
- **Версия формата — 3.** Форк пишет версию 2 (`FORK1:src/save/SaveGameManager.hpp:22`), релизы `hd.3`–`hd.8` — версию 1. Кодек отклоняет файл чужой версии (`FORK1:src/save/SaveFileCodec.cpp:60-62`), `slotInfo` форка тогда возвращает `valid = false` (`FORK1:src/save/SaveGameManager.cpp:1389-1391`), окно рисует строку `NN. <повреждено>` (`FORK1:src/save/SaveSlotsDialog.cpp:347-350`). Поэтому файлы версий 1 и 2 помечаются повреждёнными без отдельного кода.
- **Раздел FACTORYPADS** и всё о площадках заводов (`FactoryPad.hpp`, поля `bRollingOffFactoryPad`, `iRollingOffFactoryPadStructureId`, значения `PAD_PICKUP_*`, тест `FactoryPadSaveTests.cpp`) — шаг П8а. Версия 3 в этом шаге — без раздела FACTORYPADS; П8а добавит его в ту же версию 3 перед записью `END`.
- **Сохранений в порту нет:** в ревизии `B` нет папки `src/save/`, нет `SaveGameManager`, `SaveSlotsDialog`, `quicksave`, `D2TM_SAVE`.
- **Состояния порта получают `sGameServices*`, а не `cGame&`** (`src/gamestates/cGameState.h:63`, `src/include/sGameServices.h:42-66`). Доступ состояний к действиям `cGame` идёт через узкие классы с обратными вызовами — образец `src/game/MissionFlow.hpp` (весь файл), их создаёт конструктор `cGame` (`src/game/cGame_logic.cpp:225-292`). Сохранения подключаются так же: новый класс `SaveGameFlow` (пункт 7 контракта).
- **Члены `cGame`:** `m_mapCamera`, `m_drawManager`, `m_reinforcements`, `m_gameObjectsContext`, `m_infoContext`, `m_gameSettings` открыты (`src/game/cGame.h:104-117`); `m_state`, `m_nextState` (`:226-227`), `m_dataCampaign` (`:255`), `m_gameConditionChecker` (`:256`) закрыты. `friend class UiAuditAccess;` — строка 89.
- **Ход загрузки.** `cGame::missionInit` (`src/game/cGame_logic.cpp:434-464`) сбрасывает зум и закладки камеры, условия победы, карту `64×64`, юниты, частицы, снаряды, игроков и `m_drawManager->missionInit()`. `cGame::setupPlayers` (`:907-911`) пересоздаёт боковую панель, очередь построек, заказ космопорта и управление каждого игрока. `cGame::setState` (`:947-1233`): переход в `GAME_PLAYING` из `GAME_PLAYING` ничего не делает (`:949-952`); из `GAME_OPTIONS` — продолжение боя без сброса (`:1039-1048`); из других состояний — `m_drawManager->reset/missionInit/init`, `evaluateStillAliveForAI`, событие `GAME_EVENT_ABOUT_TO_BEGIN`, `startTimer` (`:1102-1120`, `:1183-1202`). `m_dataCampaign->housePlayer` ставится только на пути `:1184`. Музыка мирного времени в порту включается при выходе от ментата (`:1324`) и при старте схватки (`src/gamestates/cSetupSkirmishState.cpp:1075`), а не в `setState`.
- **Ввод текста в порту:** `cGameState::isKeyboardCapturedByUi()` (`src/gamestates/cGameState.h:75-77`); `cGame::syncTextInputState` (`src/game/cGame_logic.cpp:141-148`) включает `SDL_StartTextInput(window)` по этому признаку после каждого события мыши и клавиатуры (`:1447`, `:1474-1480`); пока признак истинен, глобальные клавиши `cGame::onKeyPressedGame` не срабатывают (`:1471-1477`). Текст приходит событием `PRESSED` без клавиш с `cKeyboardEvent::hasTextInput()` и `getTextInput()` (`src/controls/cKeyboard.cpp:73-75`, `:109-110`). Метода `onTextInput` в порту нет.
- **Уведомления в бою** — событие `GAME_EVENT_NOTIFICATION` через `m_eventEmitter->emit(...)` (образец — `src/gamestates/cGamePlaying.cpp:558-567`); `cGame::dispatchGameEvent` отдаёт его в `m_notificationArea` (`src/game/cGame_logic.cpp:1411-1414`). Типы — `NEUTRAL`, `PRIORITY`, `BAD`, `OTHER` (`src/include/eNotificationType.h`).
- **Клавиши:** `cKeyBindings::matches` отвергает привязку, если зажат модификатор, которого привязка не требует (`src/controls/cKeyBindings.cpp:278-309`). Поэтому `F5` без модификаторов не срабатывает на отладочное `Shift,Tab,F5` (`:125`), а `F9` — на `Shift,Tab,F9` (`:129`). Сейчас `F5` занято переходом к закладке 5 (`:56`, `resources/bin/settings.ini:122`), `Alt,F5` — записью закладки 5 (`:51`, `settings.ini:117`). `F6` без модификаторов и `Alt,F6` свободны.
- **Пути пользовательских файлов не зависят от рабочего каталога:** `PreferencesPath::directory()` берёт абсолютный путь `SDL_GetPrefPath("D2TM", "Dune II - The Maker")` (`src/game/PreferencesPath.cpp:28-40`); через него строятся `preferences.ini` (`src/main.cpp:83`, `:93`, `:137`) и `campaign-progress.ini` (`src/game/cGame_logic.cpp:769`). Смена рабочего каталога меняет только относительные пути: `nlog.txt` (`src/main.cpp:67`), `settings.ini` (`src/main.cpp:80`, `src/game/cGame_logic.cpp:717`), `intro.pak` (`src/gamestates/cMainMenuState.cpp:172`), данные `GameDir`, карты `skirmish/`, снимки экрана и новую папку `saves`.
- **Рабочий каталог в форке** ставит `useExecutableDirectoryAsWorkingDirectory()` (`FORK1:src/main.cpp:33-51`, вызов `:85`) через `SDL_GetBasePath()` SDL2. В SDL3 `SDL_GetBasePath()` возвращает `const char *`, строкой владеет SDL, `SDL_free` для неё не вызывают.
- **Режим отладки интерфейса разделяет параллельные запуски рабочим каталогом:** `tools/ui-audit/run_combo.py:33-49` собирает для каждого сочетания свою папку из символических ссылок на файлы папки запуска, кроме `nlog.txt` (`:15`), и запускает игру с этим рабочим каталогом (`:66`); `tools/ui-audit/run_all.py:129` гоняет сочетания параллельно; `tests/ui_audit/ui_audit_translation.py:79-84` гоняет сцены шестью потоками с общим рабочим каталогом папки запуска (`tests/ui_audit/ui_audit_runtime_support.py:31-39`). Поэтому в режиме отладки интерфейса рабочий каталог не меняется (пункт 10 контракта), а папка сохранений — своя у каждого запуска: `<--ui-audit-out>/saves` (пункт 14).
- **Окно слотов форка** рисует глобальным `renderDrawer`, берёт размеры из `m_game.m_screenW/H`, сам включает `SDL_StartTextInput()` (`FORK1:src/save/SaveSlotsDialog.cpp:75`, `:187`, `:190`) и получает текст через `onTextInput` (`:487-505`). В порту оно рисуется экземплярами `SDLDrawer` и `cTextDrawer`, кнопки — `GuiButton` с темой `GuiTheme::Remaster()` и видом `GuiRenderKind::REMASTER_BUTTON`, как кнопки главного меню (`src/gamestates/cMainMenuState.cpp:142-151`). `GuiButton::draw` сам пишет запись click `GuiButton:<подпись>` для включённой кнопки (`src/gui/GuiButton.cpp:47-53`); поэтому окно пишет свои записи click только для слотов и поля имени: вторая запись на тот же прямоугольник даёт пересечение зон по правилу 9 `tools/ui-audit/check_geometry.py:133-136`.
- **Обрезка имени** — по буквам UTF-8 функцией порта `removeLastUtf8CodePoint` (`src/utils/Utf8.hpp:17-28`); функция форка `save_slot::removeLastUtf8Character` (`FORK1:src/save/SaveSlotName.hpp:20-31`) в порт не переносится.
- **Главное меню:** кнопка `localization::text("Load", "Загрузить")` неактивна (`src/gamestates/cMainMenuState.cpp:163`); состояние `GAME_MENU` создаётся заново при каждом входе (`src/game/cGame_logic.cpp:993-996`, `:1155-1158`). **Меню настроек из боя:** неактивные «Save game» и «Load game» (`src/gamestates/cOptionsState.cpp:174-198`).
- **Режим отладки интерфейса порта:** 172 строки `scene("` в `src/debug/UiAuditScenes.cpp`; есть `options-game-main-nosaves` (`:428`), но нет сцен сохранений. Функции `uiaudit::dropClicksUnderModal` в порту нет; в форке она удаляет записи click, сделанные до окна (`FORK1:src/debug/UiAuditCapture.cpp:321-326`). `UiAuditAccess` — друг `cSetupSkirmishState` (`src/gamestates/cSetupSkirmishState.h:60`), старт схватки — закрытый метод `prepareSkirmishGameToPlayAndTransitionToCombatState` (`src/gamestates/cSetupSkirmishState.cpp:801-1116`).
- **Тексты** — `localization::text(en, ru)` и `localization::format(en, ru, ...)` из `src/utils/Localization.hpp`; русские тексты — из форка, кроме новых текстов, которые даны в этом задании дословно.
- **Данных LFS шаг не берёт.**
- **Параллельно идут** П9 (музыка: `src/game/cGame.h`, `src/game/cGame_logic.cpp`, `cKeyBindings` после `MUSIC_VOLUME_UP`), П10а (панель приказов: `cGamePlaying::onNotifyMouseEvent`, `cDrawManager`), П10б (`cOrderProcesser`, `cStarPort`), П11. Вставки этого шага в общие файлы — только на местах, названных в контракте.

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом:

- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>` для каждого файла форка: `src/save/SaveFileCodec.hpp`, `src/save/SaveFileCodec.cpp`, `src/save/SaveSlotName.hpp`, `src/save/SaveGameManager.hpp`, `src/save/SaveGameManager.cpp`, `src/save/SaveSlotsDialog.hpp`, `src/save/SaveSlotsDialog.cpp`, `tests/SaveFileCodecTests.cpp`, `tests/SaveSlotNameTests.cpp`;
- `src/game/cGame.h` целиком; `src/game/MissionFlow.hpp` целиком; `src/include/sGameServices.h` целиком;
- вывод `nl -ba src/game/cGame_logic.cpp | sed -n '120,300p;430,470p;940,1240p;1400,1530p'`;
- `src/gamestates/cGamePlaying.h` целиком; вывод `nl -ba src/gamestates/cGamePlaying.cpp | sed -n '77,130p;340,375p;550,645p'`;
- `src/gamestates/cMainMenuState.h` и `src/gamestates/cMainMenuState.cpp` целиком;
- `src/gamestates/cOptionsState.h` целиком; вывод `nl -ba src/gamestates/cOptionsState.cpp | sed -n '55,100p;170,200p;640,697p'`;
- вывод `nl -ba src/gameobjects/units/cUnit.h | sed -n '100,200p;295,315p;505,560p'`; `src/gameobjects/structures/cAbstractStructure.h` целиком; `src/gameobjects/map/cCell.h` целиком; вывод `nl -ba src/gameobjects/map/cMap.h | sed -n '50,60p;105,160p;455,515p'`; `src/gameobjects/map/FogMemory.hpp` целиком; вывод `nl -ba src/gameobjects/players/cPlayer.h | sed -n '94,110p;295,330p;535,575p;595,663p'`; `src/building/cItemBuilder.h` целиком; `src/sidebar/cBuildingListItem.h` целиком; `src/gameobjects/units/cReinforcements.h` целиком; `src/game/cGameConditionChecker.h` целиком;
- `src/debug/UiAudit.hpp` целиком; вывод `nl -ba src/debug/UiAuditScenes.cpp | sed -n '40,75p;280,312p;425,431p'`; вывод `nl -ba src/debug/UiAuditAccess.cpp | sed -n '150,175p;470,500p'`; вывод `nl -ba src/debug/UiAuditCapture.cpp | sed -n '325,345p;445,475p'`;
- `src/main.cpp` целиком; вывод `nl -ba src/controls/cKeyBindings.cpp | sed -n '20,60p;136,170p'`; вывод `nl -ba tests/CMakeLists.txt | sed -n '1,80p'`.

Пути без `/srv/` — от корня рабочей копии. Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт

### 1. Формат файла версии 3

Файл — `save_file::encode(тело, 3)`: строка `D2TM_SAVE 3 <контрольная сумма>`, перевод строки, тело. Тело — текст, каждая запись на своей строке, поля через один пробел, логические значения — `0` или `1`. Перед первой записью писатель выполняет `output << std::setprecision(std::numeric_limits<float>::max_digits10);`, чтобы числа `float` читались обратно без потерь. Записи идут строго в этом порядке:

| запись | поля по порядку | проверки при чтении (провал — `deserializeBody` возвращает `false` с текстом ошибки) |
|---|---|---|
| `INFO "<имя>"` | имя в `std::quoted` | первая запись — `INFO` или `META`, как `FORK1:src/save/SaveGameManager.cpp:373-388` |
| `META` | `skirmish region mission winFlags loseFlags cameraCell` | `skirmish` — 0 или 1 |
| `MAP` | `width height autoSpawnBlooms autoDetonateBlooms bloomTimer desiredWorms wormRespawnTimer` | `4 ≤ width, height ≤ 256`; логические — 0 или 1 |
| `PLAYERS 7`, затем 7 записей `PLAYER` | `index house team techLevel focusCell quota selectedStructure credits maxCredits powerUsage powerProduce alive autoSlab`, затем 50 чисел `primary`, 50 чисел `structures`, 50 чисел `upgrades`, 50 значений `appliedUpgrades` (0 или 1) | число записей = `MAX_PLAYERS`; `index` = номер записи; `0 ≤ house < HouseCount`; `credits`, `maxCredits` конечны |
| `CELLS N`, затем N записей `CELL` | `credits type tile smudgeTile smudgeType health passable passableFoot visibilityMask seenMask` | `N = width × height`; `TERRAIN_BLOOM ≤ type ≤ TERRAIN_WALL`; `−1 ≤ smudgeType < SmudgeType::COUNT` |
| `FOGMEMORY N`, затем N записей `FOG` | `cell hasTerrain terrainType terrainTile terrainSmudgeTile terrainSmudgeType hasStructure structureType structureOwner structureFrame structureOffsetX structureOffsetY hasUnit unitType unitOwner unitBodyIndex unitHeadIndex unitFrame` | `N ≤ width × height`; `0 ≤ cell < width × height`; `cell` строго растёт от записи к записи; `−1 ≤ terrainSmudgeType < SmudgeType::COUNT` |
| `STRUCTURES N`, затем N записей `STRUCTURE` | `oldId type player cell hitPoints rallyPoint frame buildPhase unitWithin unitEntering unitHeading concrete animate repair animateOnApproach smoke repairTimer flagTimer reduceSmokeTimer decayTimer prebuildTimer` | `N ≤ MAX_STRUCTURES`; проверки `FORK1:src/save/SaveGameManager.cpp:508-517` |
| `UNITS N`, затем N записей `UNIT` | `oldId type player cell hitPoints tempHitPoints posX posY experience groupMask nextCell goalCell`, затем 512 чисел `path`, затем `pathIndex pathFails calculatePath carryMe carryAll attackUnit attackStructure attackCell unitId structureId credits transferType bringTarget newUnitType lastDroppedOffCell bodyFacing headFacing bodyShouldFace headShouldFace frame selected action intent willBePickedUpBy pickedUp removeMe mission reinforcement unitsEaten harvestCellMemory stayAtGoalCell`, затем 12 чисел `timers` | `N ≤ UnitSlots`; `0 ≤ oldId < UnitSlots`, без повторов; `0 ≤ type < UnitTypeCount`; `0 ≤ player < MAX_PLAYERS`; `0 ≤ cell < width × height`; `posX`, `posY`, `experience` конечны; `0 ≤ groupMask < (1 << MAX_UNIT_GROUPS)` |
| `REINFORCEMENTS N`, затем N записей `REINFORCEMENT` | `delay unitType player cell repeat remove originalDelay` | `N ≤ 1024`; проверки `FORK1:src/save/SaveGameManager.cpp:587-592` с `UnitTypeCount` вместо `MAX_UNITTYPES` |
| `BUILD_QUEUE N`, затем N записей `BUILD` | `player slot timer listType buildType buildId subList progress buildFrame timesToBuild timesOrdered state placeIt deployIt waitingForUnitSlot progressFrameTimer flashingTimer timerCap` | `N ≤ MAX_PLAYERS × MAX_ITEMS`; `0 ≤ player < MAX_PLAYERS`; `0 ≤ slot < MAX_ITEMS`; `0 ≤ listType ≤ eListTypeAsInt(eListType::LIST_UPGRADES)`; `STRUCTURE ≤ buildType < UNKNOWN`; `AVAILABLE ≤ state ≤ UNAVAILABLE`; `progressFrameTimer` конечен |
| `END` | — | запись обязательна |

Отличия от версии 2 форка: в `PLAYER` добавлены `appliedUpgrades`; в `CELL` — `seenMask`; новая запись `FOGMEMORY`; в `UNIT` поле `group` заменено на `groupMask`, путь — 512 чисел, вместо `turnTimer` и 11 таймеров форка — `harvestCellMemory`, `stayAtGoalCell` и 12 таймеров; в `BUILD` нет `building`, добавлено `waitingForUnitSlot`; записи `FACTORYPADS` нет.

Тексты ошибок существующих записей — из `FORK1:src/save/SaveGameManager.cpp:367-692`. Новые тексты: список памяти тумана — `localization::text("Invalid fog memory list", "Некорректный список памяти тумана")`; повреждённая запись `FOG` — `localization::text("Fog memory is corrupted", "Повреждена память тумана")`; неверные значения `FOG` — `localization::text("Invalid fog memory data", "Некорректные данные памяти тумана")`.

### 2. Кодек и имена слотов (новые файлы)

- `src/save/SaveFileCodec.hpp` и `src/save/SaveFileCodec.cpp` — копии файлов форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveFileCodec.hpp > src/save/SaveFileCodec.hpp` и так же для `.cpp`. Других правок нет.
- `src/save/SaveSlotName.hpp` — копия файла форка той же командой, затем две правки: функция `removeLastUtf8Character` (строки 20–31 и пустая строка 32 файла форка) удаляется; после строки `#include "utils/Localization.hpp"` добавляется строка `#include "utils/Utf8.hpp"`. Других правок нет.

### 3. Снимок и тело (новые файлы)

`src/save/SaveSnapshot.hpp` — ровно:

```cpp
#pragma once

#include "include/definitions.h"

#include <array>
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace save_game_detail {

inline constexpr std::size_t MaximumSaveBytes = 16U * 1024U * 1024U;
inline constexpr int PathSize = 512;
inline constexpr int UnitSlots = 315;
inline constexpr int HouseCount = 12;
inline constexpr int UnitTypeCount = 50;
inline constexpr int UpgradeTypeCount = 50;
inline constexpr int UnitTimerCount = 12;
inline constexpr int DefaultTimerCap = 35;

struct PlayerState {
    int house = GENERALHOUSE;
    int team = -1;
    int techLevel = 0;
    int focusCell = 0;
    int quota = 0;
    int selectedStructure = -1;
    float credits = 0.0F;
    float maxCredits = 1000.0F;
    int powerUsage = 0;
    int powerProduce = 0;
    bool alive = true;
    bool autoSlab = false;
    std::array<int, MAX_STRUCTURETYPES> primary{};
    std::array<int, MAX_STRUCTURETYPES> structures{};
    std::array<int, MAX_STRUCTURETYPES> upgrades{};
    std::array<bool, UpgradeTypeCount> appliedUpgrades{};
};

struct CellState {
    int credits = 0;
    int type = 0;
    int tile = 0;
    int smudgeTile = 0;
    int smudgeType = -1;
    int health = 0;
    bool passable = true;
    bool passableFoot = true;
    std::uint32_t visibilityMask = 0;
    std::uint32_t seenMask = 0;
};

struct FogState {
    int cell = -1;
    bool hasTerrain = false;
    int terrainType = 0;
    int terrainTile = 0;
    int terrainSmudgeTile = -1;
    int terrainSmudgeType = -1;
    bool hasStructure = false;
    int structureType = 0;
    int structureOwner = 0;
    int structureFrame = 0;
    int structureOffsetX = 0;
    int structureOffsetY = 0;
    bool hasUnit = false;
    int unitType = 0;
    int unitOwner = 0;
    int unitBodyIndex = 0;
    int unitHeadIndex = 0;
    int unitFrame = 0;
};

struct StructureState {
    int oldId = -1;
    int type = -1;
    int player = -1;
    int cell = -1;
    int hitPoints = 0;
    int rallyPoint = -1;
    int frame = 0;
    int buildPhase = 0;
    int unitWithin = -1;
    int unitEntering = -1;
    int unitHeading = -1;
    float concrete = 0.0F;
    bool animate = false;
    bool repair = false;
    bool animateOnApproach = false;
    int smoke = 0;
    int repairTimer = 0;
    int flagTimer = 0;
    int reduceSmokeTimer = 0;
    int decayTimer = 0;
    int prebuildTimer = 0;
};

struct UnitState {
    int oldId = -1;
    int type = -1;
    int player = -1;
    int cell = -1;
    int hitPoints = 0;
    int tempHitPoints = 0;
    float posX = 0.0F;
    float posY = 0.0F;
    float experience = 0.0F;
    int groupMask = 0;
    int nextCell = -1;
    int goalCell = -1;
    std::array<int, PathSize> path{};
    int pathIndex = 0;
    int pathFails = 0;
    bool calculatePath = false;
    bool carryMe = false;
    int carryAll = -1;
    int attackUnit = -1;
    int attackStructure = -1;
    int attackCell = -1;
    int unitId = -1;
    int structureId = -1;
    int credits = 0;
    int transferType = 0;
    int bringTarget = -1;
    int newUnitType = -1;
    int lastDroppedOffCell = -1;
    int bodyFacing = 0;
    int headFacing = 0;
    int bodyShouldFace = 0;
    int headShouldFace = 0;
    int frame = 0;
    bool selected = false;
    int action = 0;
    int intent = 0;
    int willBePickedUpBy = -1;
    bool pickedUp = false;
    bool removeMe = false;
    int mission = -1;
    bool reinforcement = false;
    int unitsEaten = 0;
    int harvestCellMemory = -1;
    bool stayAtGoalCell = false;
    std::array<int, UnitTimerCount> timers{};
};

struct ReinforcementState {
    int delay = -1;
    int unitType = -1;
    int player = -1;
    int cell = -1;
    bool repeat = false;
    bool remove = false;
    int originalDelay = -1;
};

struct BuildQueueState {
    int player = -1;
    int slot = -1;
    int timer = 0;
    int listType = 0;
    int buildType = 0;
    int buildId = -1;
    int subList = 0;
    int progress = 0;
    int buildFrame = 0;
    int timesToBuild = 0;
    int timesOrdered = 0;
    int state = 0;
    bool placeIt = false;
    bool deployIt = false;
    bool waitingForUnitSlot = false;
    float progressFrameTimer = 0.0F;
    int flashingTimer = 0;
    int timerCap = DefaultTimerCap;
};

struct SaveSnapshot {
    std::string saveName;
    bool skirmish = false;
    int region = 1;
    int mission = 0;
    int winFlags = 0;
    int loseFlags = 0;
    int cameraCell = 0;
    int mapWidth = 64;
    int mapHeight = 64;
    bool autoSpawnBlooms = false;
    bool autoDetonateBlooms = false;
    int bloomTimer = 0;
    int desiredWorms = 0;
    int wormRespawnTimer = 0;
    std::array<PlayerState, MAX_PLAYERS> players{};
    std::vector<CellState> cells;
    std::vector<FogState> fog;
    std::vector<StructureState> structures;
    std::vector<UnitState> units;
    std::vector<ReinforcementState> reinforcements;
    std::vector<BuildQueueState> buildQueue;
};

}
```

`src/save/SaveBody.hpp` — ровно:

```cpp
#pragma once

#include "save/SaveSnapshot.hpp"

#include <string>
#include <string_view>

namespace save_game_detail {

[[nodiscard]] std::string serializeBody(const SaveSnapshot &save);

[[nodiscard]] bool deserializeBody(std::string_view body, SaveSnapshot &save, std::string &error);

}
```

`src/save/SaveBody.cpp`:
- подключает только `save/SaveBody.hpp`, `data/gfxdata.h`, `include/enums/BuildEnums.h`, `include/enums/ListEnums.h`, `include/enums/MapEnums.h`, `utils/Localization.hpp` и стандартные заголовки; не вызывает функций, определённых вне заголовков: файл входит в `d2tm_tests` без других исходников игры;
- вспомогательные функции `writeArray`, `readValue`, `readBool`, `readArray`, `expectTag` — строки 206–246 `FORK1:src/save/SaveGameManager.cpp` дословно, в пространстве имён `save_game_detail`;
- `serializeBody` — тело строк 248–365 форка, переписанное под таблицу пункта 1 (первой строкой после создания потока — `setprecision` из пункта 1; блок `FACTORYPADS` строк 357–362 не переносится; `FOGMEMORY` пишется сразу после `CELLS`);
- `deserializeBody` — тело строк 367–692 форка под таблицу пункта 1: `MAX_UNITS` → `UnitSlots`, `MAX_UNITTYPES` → `UnitTypeCount`, `MAX_HOUSES` → `HouseCount`, `SmudgeType::MAX` → `SmudgeType::COUNT`, `cSideBar::LIST_MAX` → граница `eListTypeAsInt(eListType::LIST_UPGRADES)` включительно; блок `FACTORYPADS` (строки 626–686) не переносится.

### 4. Таблица «член порта → раздел и поле файла»

Номера строк — объявления в ревизии `B`. «Не сохраняется» — с причиной; такой член SaveGameManager не трогает, кроме случаев, названных в пункте 5.

**`cGame` и связанные** (`src/game/`, `src/include/sDataCampaign.h`)

| член порта | раздел и поле | примечание |
|---|---|---|
| `cGameSettings::m_skirmish` (`cGameSettings.h:196`) | `META skirmish` | через `isSkirmish()` / `setSkirmish()` (`:120-125`) |
| `s_DataCampaign::region` (`sDataCampaign.h:22`) | `META region` | |
| `s_DataCampaign::mission` (`sDataCampaign.h:23`) | `META mission` | в схватке это уровень техники (`cSetupSkirmishState.cpp:806`) |
| `s_DataCampaign::housePlayer` (`sDataCampaign.h:21`) | не сохраняется: при загрузке = `house` записи `PLAYER 0` | путь `setState` из существующего состояния боя его не ставит |
| `cGameConditionChecker::m_winFlags`, `m_loseFlags` (`cGameConditionChecker.h:47`) | `META winFlags loseFlags` | запись — `setWinFlags`/`setLoseFlags` (`:29-30`) |
| `cMapCamera::m_viewportStartX/Y`, `m_viewportWidth/Height` (`cMapCamera.h:219-222`) | `META cameraCell` | клетка центра: `getViewportCenterX/Y()` (`:146-152`) делёные на `TILESIZE_WIDTH_PIXELS`/`TILESIZE_HEIGHT_PIXELS`, зажатые в карту, `makeCell` |
| `cMapCamera::m_zoomLevel`, `m_tileHeight`, `m_tileWidth` (`:241-245`) | не сохраняется: вид камеры; `missionInit` сбрасывает зум | |
| `cMapCamera::m_viewportBookmarks` (`:281`) | не сохраняется: закладки вида камеры; `missionInit` их сбрасывает (`cGame_logic.cpp:437`) | |
| `cMapCamera::m_moveX/Y`, скорости, `m_cameraEdgeMove`, `m_keyPressed*`, размеры окна, указатели (`:225-251`) | не сохраняется: ввод и настройки | |
| `cReinforcements::reinforcements` (`cReinforcements.h:65`) | `REINFORCEMENTS` | |
| `cMissionStatsCollector::m_playerStats` (`cMissionStatsCollector.h:37`), время боя `cTimeManager::getElapsedSeconds()` (`cTimeManager.h:53`) | не сохраняется: только экран итогов (`cScoringState.cpp:40`), на ход боя не влияет | |
| `cGamePlaying::m_TIMER_evaluatePlayerStatus` (`cGamePlaying.h:98`) | не сохраняется: таймер опроса в 5 тиков, значение 0–5 | |
| `cGamePlaying::m_trackedUnitIds` (`:112`), `m_lastGroupKeyPressed`, `m_lastGroupKeyPressedTick`, `m_lastDebugSwitchAction` (`:113-115`) | не сохраняется: слежение камеры и двойное нажатие клавиш; `m_trackedUnitIds` очищается после `F9` (пункт 9) | |
| `cNotificationArea` | не сохраняется: сообщения интерфейса | |
| прочие члены `cGame` и `cGameSettings` | не сохраняется: окно, контексты, фабрики, настройки игрока и запуска | |

**`cMap`** (`src/gameobjects/map/cMap.h`) **и `tCell`** (`cCell.h`)

| член порта | раздел и поле | примечание |
|---|---|---|
| `cMap::m_mapGeometry` (`cMap.h:497`) | `MAP width height` | `getGeometry()->getWidth()/getHeight()`; загрузка — `init(width, height)` |
| `m_bAutoSpawnSpiceBlooms`, `m_bAutoDetonateSpiceBlooms`, `m_iTIMER_blooms` (`:501-503`) | `MAP autoSpawnBlooms autoDetonateBlooms bloomTimer` | |
| `m_iDesiredAmountOfWorms`, `m_iTIMER_respawnSandworms` (`:509-510`) | `MAP desiredWorms wormRespawnTimer` | |
| `m_mBloomTimers` (`:504`) | не сохраняется: есть и в форке (`FORK1:src/map/cMap.h:555`), форк не сохранял | |
| `m_TIMER_scroll`, `m_iScrollSpeed` (`:513-514`) | не сохраняется: прокрутка камеры | |
| `m_cell` (`:481`) | `CELLS` | по полям `tCell` ниже |
| `m_wasSeen` (`:482`) | не сохраняется: буфер, перезаписывается из `iSeen` перед использованием (`cMap.cpp:388-393`) | |
| `m_fogMemory` (`:483`) | `FOGMEMORY` | по полям `FogMemory` ниже |
| указатели `m_ctx` … `m_gfxdata`, `m_pathFinder`, `m_reinforcements`, `m_terrainInfo` (`:484-507`) | не сохраняется: службы | |
| `tCell::credits, type, tile, smudgetile, health, passable, passableFoot` (`cCell.h:24-31`) | `CELL credits type tile smudgeTile health passable passableFoot` | |
| `tCell::smudgetype` (`:28`) | `CELL smudgeType` | `std::nullopt` ↔ `−1` |
| `tCell::iVisible[MAX_PLAYERS]` (`:33`) | `CELL visibilityMask` | бит `p` = `iVisible[p]` |
| `tCell::iSeen[MAX_PLAYERS]` (`:34`) | `CELL seenMask` | бит `p` = `iSeen[p]` |
| `tCell::id[4]` (`:38`) | не сохраняется: пересчитывается при загрузке по зданиям и юнитам | |
| `FogMemory::m_cells` (`FogMemory.hpp`) | `FOG hasTerrain terrainType terrainTile terrainSmudgeTile terrainSmudgeType` | чтение — `getTerrain(cell)`; загрузка — `update(cell, true, false, s_RememberedTerrain{...})` |
| `FogMemory::m_structures` | `FOG hasStructure structureType structureOwner structureFrame structureOffsetX structureOffsetY` | `getStructure(cell)`; `updateStructure(cell, true, false, ...)` |
| `FogMemory::m_units` | `FOG hasUnit unitType unitOwner unitBodyIndex unitHeadIndex unitFrame` | `getUnit(cell)`; `updateUnit(cell, true, false, ...)` |

Запись `FOG` пишется для каждой клетки, у которой есть хотя бы одна из трёх частей памяти, в порядке номеров клеток; поля отсутствующей части — значения по умолчанию `FogState`.

**`cPlayer`** (`src/gameobjects/players/cPlayer.h`)

| член порта | раздел и поле | примечание |
|---|---|---|
| `house` (`:616`) | `PLAYER house` | загрузка — `setHouse` |
| `iTeam` (`:620`) | `PLAYER team` | |
| `techLevel` (`:615`) | `PLAYER techLevel` | |
| `focusCell_` (`:651`) | `PLAYER focusCell` | |
| `spiceQuota` (`:658`) | `PLAYER quota` | |
| `selected_structure` (`:544`) | `PLAYER selectedStructure` | номер здания переводится при загрузке |
| `credits`, `maxCredits_` (`:648-649`) | `PLAYER credits maxCredits` | |
| `powerUsage_`, `powerProduce_` (`:645-646`) | `PLAYER powerUsage powerProduce` | `cPlayer::update` пересчитывает их из зданий (`cPlayer.cpp:899-905`) |
| `alive` (`:660`) | `PLAYER alive` | |
| `m_autoSlabStructures` (`:655`) | `PLAYER autoSlab` | |
| `iPrimaryBuilding`, `iStructures`, `iStructureUpgradeLevel` (`:640-642`) | `PLAYER primary structures upgrades` | `primary` переводится при загрузке |
| `m_appliedUpgrades[MAX_UPGRADETYPES]` (`:643`) | `PLAYER appliedUpgrades` | только в порту; читается `cBuildingListUpdater` при создании зданий (`cBuildingListUpdater.cpp:180-186`, `:434-440`, `:613`) — восстанавливается до размещения зданий |
| `id` (`:619`) | номер записи `PLAYER` | |
| `m_Human`, `difficultySettings` (`:601`, `:606`) | не сохраняется: создаются при инициализации игрока и выборе Дома | |
| `sidebar`, `itemBuilder`, `buildingListUpdater`, `orderProcesser`, `gameControlsContext` (`:608-613`) | не сохраняется: `setupPlayers` создаёт их заново; содержимое очереди `itemBuilder` — в `BUILD_QUEUE`; заказ космопорта форк не сохранял | |
| `brain_` (`:653`) | не сохраняется: форк не сохранял; `initPlayers` создаёт заново (`cPlayers.cpp:158-210`) | |
| `minimapColor`, `emblemBackgroundColor`, `bmp_structure`, `bmp_flag`, `bmp_flag_small`, `bmp_unit`, `bmp_unit_top` (`:617-618`, `:633-638`) | не сохраняется: рисование, создаётся по Дому | |
| службы `m_HousesInfo`, `m_settings` … `m_renderer` (`:612`, `:622-631`) | не сохраняется: службы | |

**`cAbstractStructure`** (`src/gameobjects/structures/cAbstractStructure.h`)

| член порта | раздел и поле | примечание |
|---|---|---|
| `id` (`:74`) | `STRUCTURE oldId` | при загрузке здание получает новый номер, ссылки переводятся |
| `getType()` (`:128`) | `STRUCTURE type` | |
| `iPlayer` (`:81`), `iCell` (`:47`) | `STRUCTURE player cell` | |
| `iHitPoints` (`:45`), `iRallyPoint` (`:49`), `iFrame` (`:79`), `iBuildFase` (`:83`) | `STRUCTURE hitPoints rallyPoint frame buildPhase` | |
| `iUnitIDWithinStructure`, `iUnitIDEnteringStructure`, `iUnitIDHeadingForStructure` (`:57-61`) | `STRUCTURE unitWithin unitEntering unitHeading` | |
| `fConcrete` (`:105`), `bAnimate` (`:51`), `bRepair` (`:86`), `shouldAnimateWhenUnitHeadsTowardsStructure` (`:73`), `m_smokeParticlesCreated` (`:109`) | `STRUCTURE concrete animate repair animateOnApproach smoke` | |
| `TIMER_repair`, `TIMER_flag`, `TIMER_reduceSmoke`, `TIMER_decay`, `TIMER_prebuild` (`:112-117`) | `STRUCTURE repairTimer flagTimer reduceSmokeTimer decayTimer prebuildTimer` | |
| `flags` (`:91`) | не сохраняется: рисование; флаги создаёт фабрика при размещении здания (`cStructureFactory.cpp:171-174`) | |
| `armor` (`:43`), `iWidth`, `iHeight` (`:76-77`), `frames` (`:88`), `posX`, `posY` (`:55`) | не сохраняется: из сведений о типе и клетки при размещении | |
| `dead` (`:53`) | не сохраняется: в снимок попадают только здания с `isValid()` | |
| службы (`:64-71`) | не сохраняется: службы | |
| члены подклассов зданий и `cOrderProcesser` | не сохраняется: есть и в форке, форк их не сохранял | |

**`cUnit`** (`src/gameobjects/units/cUnit.h`)

| член порта | раздел и поле | примечание |
|---|---|---|
| `iID` (`:157`) | `UNIT oldId` | юнит загружается в тот же слот |
| `iType` (`:158`), `iPlayer` (`:160`) | `UNIT type player` | |
| `position.iCell` (`:136`) | `UNIT cell` | чтение `getCell()`; загрузка `setCell()` |
| `position.posX`, `position.posY` (`:141`) | `UNIT posX posY` | чтение `getPosX/getPosY()`; загрузка `setPosX/setPosY()` после `setCell()` |
| `position.iCellX`, `position.iCellY` (`:137-138`) | не сохраняется: `updateCellXAndY()` при загрузке | |
| `iHitPoints` (`:534`), `iTempHitPoints` (`:525`), `fExperience` (`:155`) | `UNIT hitPoints tempHitPoints experience` | |
| `iGroups` (`:159`) | `UNIT groupMask` | бит `g` = `iGroups[g]`; в форке одно число `iGroup` |
| `movement.iNextCell`, `iGoalCell`, `iPath`, `iPathIndex`, `iPathFails`, `bCalculateNewPath` (`:108-114`) | `UNIT nextCell goalCell path pathIndex pathFails calculatePath` | `MAX_PATH_SIZE` = 512 (`:31`) |
| `movement.waypointCells` (`:111`) | не сохраняется: рисование точек пути (`cUnitDrawer.cpp:230`), пересчитывается с новым путём (`cPathFinder.cpp:556-583`) | |
| `bCarryMe`, `iCarryAll` (`:165-166`) | `UNIT carryMe carryAll` | |
| `combat.iAttackUnit`, `iAttackStructure`, `iAttackCell` (`:127-129`) | `UNIT attackUnit attackStructure attackCell` | `attackStructure` переводится |
| `iUnitID`, `iStructureID` (`:172-173`) | `UNIT unitId structureId` | `structureId` переводится |
| `iCredits` (`:176`) | `UNIT credits` | |
| `iHarvestCellMemory`, `m_stayAtGoalCell` (`:177-178`) | `UNIT harvestCellMemory stayAtGoalCell` | только в порту |
| `m_transferType` (`:184`), `iBringTarget`, `iNewUnitType`, `lastDroppedOffCell` (`:186-188`) | `UNIT transferType bringTarget newUnitType lastDroppedOffCell` | |
| `rendering.iBodyFacing`, `iHeadFacing`, `iBodyShouldFace`, `iHeadShouldFace` (`:118-121`) | `UNIT bodyFacing headFacing bodyShouldFace headShouldFace` | `Facing` ↔ `int` через `static_cast` |
| `rendering.iFrame` (`:122`) | `UNIT frame` | |
| `rendering.bHovered` (`:123`) | не сохраняется: наведение мыши; при загрузке `false` | |
| `m_bSelected` (`:547`) | `UNIT selected` | загрузка: `selected && player == HUMAN` |
| `m_action`, `intent` (`:522-523`) | `UNIT action intent` | |
| `willBePickedUpBy`, `bPickedUp`, `bRemoveMe`, `mission`, `isReinforcement`, `unitsEaten` (`:527-538`) | `UNIT willBePickedUpBy pickedUp removeMe mission reinforcement unitsEaten` | |
| `moveTimer`, `movewaitTimer`, `movedelayTimer`, `turnTimer`, `thinkwaitTimer`, `frameTimer`, `harvestTimer`, `guardTimer`, `boredTimer`, `attackTimer`, `wormTrailTimer`, `revealTimer` (`:301-312`) | `UNIT timers[0]` … `timers[11]` в этом порядке | `cTimer::get()` / `reset(int)`; `revealTimer` — только в порту |
| `TIMER_blink` форка | в порту члена нет | |
| `boundParticleId` (`:553`) | не сохраняется: частицы не сохраняются; при загрузке `−1` | |
| `dimensions` (`:559`) | не сохраняется: `recreateDimensions()` при загрузке | |
| службы (`:512-520`) | не сохраняется: службы | |

**Очередь построек**

| член порта | раздел и поле | примечание |
|---|---|---|
| `cItemBuilder::m_items[MAX_ITEMS]` (`cItemBuilder.h:75`) | `BUILD player slot listType buildType buildId subList` | пункт ищется в списке боковой панели по `buildType`, `buildId`, `subList` |
| `cItemBuilder::m_timers[MAX_ITEMS]` (`:83`) | `BUILD timer` | |
| `cItemBuilder::m_buildItemMultiplierEnabled` (`:84`) | не сохраняется: зажатая клавиша | |
| `cBuildingListItem::m_state` (`cBuildingListItem.h:299`) | `BUILD state` | число `eBuildingListItemState` порта, включая `PAUSED` = 2 (`include/enums/ListEnums.h:66-73`) |
| `m_progress`, `m_buildFrameToDraw`, `m_timesToBuild`, `m_timesOrdered` (`:300-303`) | `BUILD progress buildFrame timesToBuild timesOrdered` | |
| `m_placeIt`, `m_deployIt` (`:307`, `:309`) | `BUILD placeIt deployIt` | |
| `m_waitingForUnitSlot` (`:308`) | `BUILD waitingForUnitSlot` | только в порту |
| `m_TIMER_progressFrame`, `m_TIMER_flashing`, `m_timerCap` (`:314-316`) | `BUILD progressFrameTimer flashingTimer timerCap` | |
| `building` форка | в порту члена нет: признак выводится из `m_state` (`:95-97`) | |
| `m_icon`, `m_buildId`, `m_type`, `m_cost`, `m_slotId`, `m_creditsPerProgressTime`, `m_queuable`, `m_subList`, `m_myList`, службы (`:295-298`, `:304`, `:306`, `:310`, `:312`, `:318-320`) | не сохраняется: описание пункта каталога, создаётся с боковой панелью | |

**`cReinforcement`** (`cReinforcements.h:39-45`): `m_delayInSeconds, m_unitType, m_playerId, m_cell, m_repeat, m_removeMe, m_originalDelay` → `REINFORCEMENT delay unitType player cell repeat remove originalDelay`.

### 5. `SaveGameManager` (новые файлы)

`src/save/SaveGameManager.hpp` — копия файла форка (`git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.hpp > src/save/SaveGameManager.hpp`), затем две правки: строка `    static constexpr int FormatVersion = 2;` становится `    static constexpr int FormatVersion = 3;`; сразу после строки `    static constexpr int MaximumSlots = 10;` вставляются пустая строка и строки:

```cpp
    static void setSavesDirectory(const std::filesystem::path &directory);
    [[nodiscard]] static std::filesystem::path savesDirectory();
```

`src/save/SaveGameManager.cpp` — строки 696–1528 `FORK1:src/save/SaveGameManager.cpp` по правилам переноса, со следующими требованиями.

1. **Подключения.** Блок `#ifdef _WIN32` строк 1–4 форка ставится последним блоком подключений файла и получает строку `#define NOMINMAX` после `#define WIN32_LEAN_AND_MEAN`. Сразу после подключений — шесть строк проверок:
   ```cpp
   static_assert(save_game_detail::PathSize == MAX_PATH_SIZE);
   static_assert(save_game_detail::UnitSlots == cUnits::TOTAL_SLOTS);
   static_assert(save_game_detail::HouseCount == MAX_HOUSES);
   static_assert(save_game_detail::UnitTypeCount == MAX_UNITTYPES);
   static_assert(save_game_detail::UpgradeTypeCount == MAX_UPGRADETYPES);
   static_assert(save_game_detail::DefaultTimerCap == cBuildingListItem::DefaultTimerCap);
   ```
2. **Папка сохранений.** В безымянном пространстве имён — `std::filesystem::path g_savesDirectory = "saves";`. `setSavesDirectory` присваивает его, `savesDirectory` возвращает его. `slotPath` (форк `:1349-1359`) строит пути от `savesDirectory()`: слот 1 — `savesDirectory() / "quicksave.d2s"`, остальные — `savesDirectory() / std::format("save{:02}.d2s", slot)`.
3. **`captureSnapshot`** (форк `:698-917`) — по таблице пункта 4: каждое поле записи берётся из члена порта, названного в строке таблицы; здания — по слотам `0 … MAX_STRUCTURES − 1` с `getStructure(i) != nullptr && isValid()`; юниты — по слотам `0 … cUnits::TOTAL_SLOTS − 1` с `isValid()`; очередь — по `getItemBuilder()` каждого игрока, пропуская пустые слоты и пункты с `m_myList == nullptr`; блок `cUnitFactory` и площадок (`:797-801`) не переносится.
4. **`restoreSnapshot`** (форк `:975-1276`) — строго в этом порядке:
   1. `setSkirmish(save.skirmish)`; `m_dataCampaign->region`, `->mission` из `META`; `m_dataCampaign->housePlayer = save.players[HUMAN].house`.
   2. `setHouse(save.players[i].house)` каждому игроку.
   3. `game.missionInit()`; `game.setupPlayers()`.
   4. `map->init(save.mapWidth, save.mapHeight)`; восстановление клеток (функция `restoreCellState` форка `:919-940`, дополненная `iSeen` из `seenMask`); сброс всех слоёв клеток `cellResetIdFromLayer` (форк `:991-995`).
   5. Первый проход по игрокам: `setHouse`, `iTeam`, `techLevel`, `focusCell_`, `spiceQuota`, `selected_structure = -1`, `m_autoSlabStructures`, `iStructureUpgradeLevel`, `m_appliedUpgrades`.
   6. Здания — форк `:1016-1065`: `placeStructure(cell, type, процент)` с процентом от `game.m_infoContext->getStructureInfo(type).hp`; затем поля из таблицы.
   7. Юниты — форк `:1067-1142`: `init(oldId)`, затем поля из таблицы; позиция — `setCell(cell)`, `setPosX(posX)`, `setPosY(posY)`, `updateCellXAndY()`; `rendering.bHovered = false`; `boundParticleId = -1`; таймеры — `reset(timers[k])`; `recreateDimensions()`; слой клетки — как форк `:1132-1141`.
   8. Связи зданий с юнитами — форк `:1144-1154`.
   9. Повторное восстановление клеток и слоёв зданий и юнитов — форк `:1169-1190`.
   10. Второй проход по игрокам: `iStructures`, переведённые `iPrimaryBuilding` и `selected_structure`, затем `credits`, `maxCredits_`, `powerUsage_`, `powerProduce_`, `alive`.
   11. Память тумана — по записям `FOG` (таблица пункта 4).
   12. Подкрепления — форк `:1205-1218`; очередь построек — форк `:1220-1252` с полями порта (без `building`, с `m_waitingForUnitSlot`).
   13. Поля карты из `MAP` — форк `:1254-1258`; `setWinFlags(save.winFlags)`, `setLoseFlags(save.loseFlags)`. Строка форка `game.m_TIMER_evaluatePlayerStatus = 5;` не переносится.
   14. `game.m_gameObjectsContext->getParticles().reset()`; `init()` каждого снаряда из `getBullets()`.
   15. `game.m_drawManager->setPlayerToDraw(<игрок HUMAN>)`; `game.setPlayerToInteractFor(<игрок HUMAN>)`; `game.m_mapCamera->centerAndJumpViewPortToCell(<cameraCell, зажатая в карту>)`.
   16. Если `!game.isState(GAME_PLAYING)` — `game.playMusicByType(eMusicType::PEACE)`.
   17. `game.setNextStateToTransitionTo(GAME_PLAYING)`; `return true`.
5. **`writeAtomically`** (форк `:1278-1337`) — без изменений, кроме ветки не-Windows: строка `error = directoryError.message();` становится
   ```cpp
           error = localization::format(
               "Could not replace save file ({})",
               "Не удалось заменить сохранение ({})",
               directoryError.message()
           );
   ```
6. **Пути, слоты, сохранение и загрузка** (форк `:1338-1528`) — по правилам переноса; `deserializeBody`, `serializeBody`, `MaximumSaveBytes` берутся из `save/SaveBody.hpp` и `save/SaveSnapshot.hpp`; проверка состояния в `saveGame` (форк `:1451-1456`) использует `game.isState(...)` и `game.m_nextState`.

### 6. Доступ к закрытым членам

Строка `friend class SaveGameManager;` добавляется сразу после строки:
- `    friend class UiAuditAccess;` в `src/game/cGame.h` (строка 89);
- `class cGameConditionChecker {` в `src/game/cGameConditionChecker.h`;
- `class cItemBuilder : cInputObserver {` в `src/building/cItemBuilder.h`;
- `class cAbstractStructure : public cScenarioObserver {` в `src/gameobjects/structures/cAbstractStructure.h`;
- `class cReinforcement {` и `class cReinforcements {` в `src/gameobjects/units/cReinforcements.h` (две строки);
- `class cUnit {` в `src/gameobjects/units/cUnit.h`;
- `class cMap : public cScenarioObserver {` в `src/gameobjects/map/cMap.h`;
- `class cPlayer : public cScenarioObserver {` в `src/gameobjects/players/cPlayer.h`;
- `class cBuildingListItem {` в `src/sidebar/cBuildingListItem.h`.

Отступ строки — 4 пробела. Других правок в этих девяти файлах нет.

### 7. Связь состояний с сохранениями

- Новый файл `src/game/SaveGameFlow.hpp` — ровно:
  ```cpp
  #pragma once

  #include <functional>
  #include <string>
  #include <utility>

  class SaveGameFlow {
  public:
      using SaveCallback = std::function<bool(int slot, const std::string &name, std::string &errorMessage)>;
      using LoadCallback = std::function<bool(int slot, std::string &errorMessage)>;
      using QuickCallback = std::function<bool(std::string &errorMessage)>;

      SaveGameFlow(SaveCallback save, LoadCallback load, QuickCallback quickSave, QuickCallback quickLoad)
          : m_save(std::move(save)),
            m_load(std::move(load)),
            m_quickSave(std::move(quickSave)),
            m_quickLoad(std::move(quickLoad)) {
      }

      bool save(int slot, const std::string &name, std::string &errorMessage) const {
          return m_save(slot, name, errorMessage);
      }

      bool load(int slot, std::string &errorMessage) const {
          return m_load(slot, errorMessage);
      }

      bool quickSave(std::string &errorMessage) const {
          return m_quickSave(errorMessage);
      }

      bool quickLoad(std::string &errorMessage) const {
          return m_quickLoad(errorMessage);
      }

  private:
      SaveCallback m_save;
      LoadCallback m_load;
      QuickCallback m_quickSave;
      QuickCallback m_quickLoad;
  };
  ```
- `src/include/sGameServices.h`: после строки `class VideoFlow;` (строка 40) — строка `class SaveGameFlow;`; после строки `    VideoFlow *videoFlow = nullptr;` (строка 65) — строка `    SaveGameFlow *saveGameFlow = nullptr;`.
- `src/game/cGame.h`: после строки `class VideoFlow;` (строка 72) — строка `class SaveGameFlow;`; после строки `    std::unique_ptr<VideoFlow> m_videoFlow;` (строка 263) — строка `    std::unique_ptr<SaveGameFlow> m_saveGameFlow;`; строка друга — пункт 6.
- `src/game/cGame_logic.cpp`: после строки `#include "game/VideoFlow.hpp"` (строка 28) — строки `#include "game/SaveGameFlow.hpp"` и `#include "save/SaveGameManager.hpp"`; после строки `    m_services->videoFlow = m_videoFlow.get();` (строка 292) — ровно:
  ```cpp
      m_saveGameFlow = std::make_unique<SaveGameFlow>(
          [this](int slot, const std::string &name, std::string &errorMessage) {
              return SaveGameManager::saveGame(*this, slot, name, errorMessage);
          },
          [this](int slot, std::string &errorMessage) {
              return SaveGameManager::loadGame(*this, slot, errorMessage);
          },
          [this](std::string &errorMessage) {
              return SaveGameManager::saveQuickGame(*this, errorMessage);
          },
          [this](std::string &errorMessage) {
              return SaveGameManager::loadQuickGame(*this, errorMessage);
          });
      m_services->saveGameFlow = m_saveGameFlow.get();
  ```
  Других правок в `cGame.h` и `cGame_logic.cpp` нет.

### 8. Клавиши

- `src/controls/eKeyAction.h`: сразу после строки `    JUMP_TO_VIEWPORT_BOOKMARK_5,` (строка 46) — строки `    QUICK_SAVE,` и `    QUICK_LOAD,`.
- `src/controls/cKeyBindings.cpp`, `loadDefaults`: строка 51 становится `    bind(eKeyAction::SAVE_VIEWPORT_BOOKMARK_5, {SDL_SCANCODE_F6}, false, true, false);`; строка 56 — `    bind(eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5, {SDL_SCANCODE_F6});`; сразу после строки 56 — строки:
  ```cpp
      bind(eKeyAction::QUICK_SAVE,          {SDL_SCANCODE_F5});
      bind(eKeyAction::QUICK_LOAD,          {SDL_SCANCODE_F9});
  ```
- `src/controls/cKeyBindings.cpp`, `getActionTable`: сразу после строки `        {"JUMP_TO_VIEWPORT_BOOKMARK_5", eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5},` (строка 165) — строки:
  ```cpp
          {"QUICK_SAVE",                eKeyAction::QUICK_SAVE},
          {"QUICK_LOAD",                eKeyAction::QUICK_LOAD},
  ```
- `resources/bin/settings.ini`, раздел `[KEYS]`: строка 117 становится `SAVE_VIEWPORT_BOOKMARK_5=Alt,F6`; строка 122 — `JUMP_TO_VIEWPORT_BOOKMARK_5=F6`; сразу после строки 122 — строки `QUICK_SAVE=F5` и `QUICK_LOAD=F9`.

### 9. Быстрое сохранение и загрузка в бою

- `src/gamestates/cGamePlaying.h`: после строки `class MissionFlow;` (строка 33) — строка `class SaveGameFlow;`; после строки `    MissionFlow* m_missionFlow = nullptr;` (строка 83) — строка `    SaveGameFlow* m_saveGameFlow = nullptr;`.
- `src/gamestates/cGamePlaying.cpp`: после строки `#include "game/MissionFlow.hpp"` (строка 41) — строка `#include "game/SaveGameFlow.hpp"`; в конструкторе после строки `    d2tm_assert(m_missionFlow != nullptr);` (строка 94) — строки `    m_saveGameFlow = services->saveGameFlow;` и `    d2tm_assert(m_saveGameFlow != nullptr);`.
- `cGamePlaying::onKeyPressedGamePlaying`: сразу после закрывающей скобки блока `if (bookmarkNumber > 0) {` (строка 567) — пустая строка и ровно:
  ```cpp
      if (event.isAction(eKeyAction::QUICK_SAVE)) {
          std::string error;
          const bool saved = m_saveGameFlow->quickSave(error);
          m_eventEmitter->emit(s_GameEvent{
              .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
              .data = NotificationEvent{
                  .message = saved ? std::string(localization::text("Game saved.", "Игра сохранена.")) : error,
                  .type = saved ? eNotificationType::NEUTRAL : eNotificationType::BAD,
              }
          });
      }

      if (event.isAction(eKeyAction::QUICK_LOAD)) {
          std::string error;
          const bool loaded = m_saveGameFlow->quickLoad(error);
          if (loaded) {
              m_trackedUnitIds.clear();
          }
          m_eventEmitter->emit(s_GameEvent{
              .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
              .data = NotificationEvent{
                  .message = loaded ? std::string(localization::text("Game loaded.", "Игра загружена.")) : error,
                  .type = loaded ? eNotificationType::NEUTRAL : eNotificationType::BAD,
              }
          });
      }
  ```
  Других правок в `cGamePlaying.h` и `cGamePlaying.cpp` нет.

### 10. Рабочий каталог

`src/main.cpp`:
- после строки `#include <algorithm>` (строка 31) — строка `#include <filesystem>`; после строки `#include <SDL3/SDL_main.h>` (строка 36) — строка `#include <SDL3/SDL_filesystem.h>`;
- сразу после строки `#endif` (строка 54, конец блока `attachParentConsole`) — пустая строка и ровно:
  ```cpp
  namespace {
  void useExecutableDirectoryAsWorkingDirectory()
  {
      const char *basePath = SDL_GetBasePath();
      if (basePath == nullptr) {
          return;
      }

      try {
          const auto *utf8BasePath = reinterpret_cast<const char8_t *>(basePath);
          std::filesystem::current_path(std::filesystem::path(utf8BasePath));
      }
      catch (const std::filesystem::filesystem_error &error) {
          std::cerr << "Unable to use the game directory: " << error.what() << '\n';
      }
  }
  }
  ```
- в `main` сразу после закрывающей скобки блока `if (uiaudit::isEnabled() && uiaudit::handleEarlyExit(uiAuditExitCode)) {` (строка 65) — ровно:
  ```cpp
      // the UI audit harness separates its parallel runs by their working directory
      if (!uiaudit::isEnabled()) {
          useExecutableDirectoryAsWorkingDirectory();
      }
  ```

### 11. Окно слотов (новые файлы)

`src/save/SaveSlotsDialog.hpp` — ровно:

```cpp
#pragma once

#include "controls/cKeyboardEvent.h"
#include "controls/sMouseEvent.h"
#include "save/SaveGameManager.hpp"
#include "utils/cRectangle.h"

#include <functional>
#include <memory>
#include <string>
#include <vector>

class GuiButton;
class SDLDrawer;
class SaveGameFlow;
class cGameSettings;
class cTextDrawer;

class SaveSlotsDialog {
public:
    SaveSlotsDialog(
        const SaveGameFlow *saveGameFlow,
        SDLDrawer *sdlDrawer,
        cTextDrawer *textDrawer,
        cGameSettings *settings,
        std::function<void()> onLoaded,
        std::function<void()> onSlotsChanged = {}
    );
    ~SaveSlotsDialog();

    void open(bool allowSaving, bool preferSaving);
    void close();
    [[nodiscard]] bool isOpen() const;
    [[nodiscard]] bool isCapturingText() const;

    void draw() const;
    void onMouseEvent(const s_MouseEvent &event);
    void onKeyboardEvent(const cKeyboardEvent &event);

private:
    friend class UiAuditAccess;

    void rebuildLayout();
    void refreshSlots();
    void selectSlot(int slot);
    void saveSelected();
    void loadSelected();
    void setEditingName(bool editing);
    void appendText(const std::string &text);
    void updateLoadButton();
    [[nodiscard]] const SaveSlotInfo *selectedInfo() const;
    [[nodiscard]] std::string fittedText(
        const std::string &text,
        int maximumWidth
    ) const;

    const SaveGameFlow *m_saveGameFlow;
    SDLDrawer *m_sdlDrawer;
    cTextDrawer *m_textDrawer;
    cGameSettings *m_settings;
    std::function<void()> m_onLoaded;
    std::function<void()> m_onSlotsChanged;
    std::vector<SaveSlotInfo> m_slots;
    std::vector<cRectangle> m_slotRects;
    cRectangle m_panelRect;
    cRectangle m_nameRect;
    cRectangle m_saveRect;
    cRectangle m_loadRect;
    cRectangle m_closeRect;
    std::unique_ptr<GuiButton> m_saveButton;
    std::unique_ptr<GuiButton> m_loadButton;
    std::unique_ptr<GuiButton> m_closeButton;
    int m_selectedSlot = 1;
    bool m_open = false;
    bool m_allowSaving = false;
    bool m_preferSaving = false;
    bool m_editingName = false;
    bool m_replaceNameOnInput = false;
    std::string m_name;
    std::string m_status;
};
```

`src/save/SaveSlotsDialog.cpp` — функции `FORK1:src/save/SaveSlotsDialog.cpp` по правилам переноса, со следующими требованиями:
- конструктор — по строкам 16–26 форка с членами заголовка выше; деструктор, `isOpen`, `refreshSlots`, `selectedInfo` — строки форка дословно;
- `open` — строки 33–70 форка; `close` — строки 72–79 форка без строк `if (m_editingName) {`, `SDL_StopTextInput();`, `}`;
- `isCapturingText` — `return m_open && m_editingName;`;
- `rebuildLayout` — строки 86–143 форка, затем создание трёх кнопок:
  ```cpp
      m_saveButton = GuiButtonBuilder()
          .withRect(m_saveRect)
          .withLabel(localization::text("Save", "Сохранить"))
          .withTextDrawer(m_textDrawer)
          .withRenderer(m_sdlDrawer)
          .withTheme(m_allowSaving ? GuiTheme::Remaster() : GuiTheme::RemasterInactive())
          .withKind(GuiRenderKind::REMASTER_BUTTON)
          .withEnabled(m_allowSaving)
          .onClick([this]() {
              saveSelected();
          })
          .build();
      m_loadButton = GuiButtonBuilder()
          .withRect(m_loadRect)
          .withLabel(localization::text("Load", "Загрузить"))
          .withTextDrawer(m_textDrawer)
          .withRenderer(m_sdlDrawer)
          .withTheme(GuiTheme::RemasterInactive())
          .withKind(GuiRenderKind::REMASTER_BUTTON)
          .withEnabled(false)
          .onClick([this]() {
              loadSelected();
          })
          .build();
      m_closeButton = GuiButtonBuilder()
          .withRect(m_closeRect)
          .withLabel(localization::text("Close", "Закрыть"))
          .withTextDrawer(m_textDrawer)
          .withRenderer(m_sdlDrawer)
          .withTheme(GuiTheme::Remaster())
          .withKind(GuiRenderKind::REMASTER_BUTTON)
          .onClick([this]() {
              close();
          })
          .build();
  ```
- `selectSlot` — строки 151–163 форка и последней строкой `updateLoadButton();`;
- `updateLoadButton` — ровно:
  ```cpp
      const SaveSlotInfo *info = selectedInfo();
      const bool canLoad = info != nullptr && info->exists && info->valid;
      m_loadButton->setEnabled(canLoad);
      m_loadButton->setTheme(canLoad ? GuiTheme::Remaster() : GuiTheme::RemasterInactive());
  ```
- `setEditingName` — строки 177–192 форка без вызовов `SDL_StartTextInput()` и `SDL_StopTextInput()` и без ветки `else`, которая содержит только `SDL_StopTextInput();`;
- `saveSelected` — строки 194–220 форка: вызов `SaveGameManager::saveGame(m_game, m_selectedSlot, cleanName, error)` → `m_saveGameFlow->save(m_selectedSlot, cleanName, error)`; сразу после строки `refreshSlots();` — `updateLoadButton();`;
- `loadSelected` — строки 222–244 форка: `SaveGameManager::loadGame(m_game, m_selectedSlot, error)` → `m_saveGameFlow->load(m_selectedSlot, error)`; сразу после строки `refreshSlots();` ветки ошибки — `updateLoadButton();`;
- `fittedText` — строки 246–261 форка, `save_slot::removeLastUtf8Character` → `removeLastUtf8CodePoint`;
- `draw` — строки 263–409 форка: в блоке `if (uiaudit::isEnabled())` остаются `uiaudit::dropClicksUnderModal();`, цикл `recordClick` слотов `save-slot:N` и `recordClick` поля `save-name`; три строки `recordClick` для `save-save`, `save-load`, `save-close` не переносятся; лямбда `drawButton`, строка `const SaveSlotInfo *info = selectedInfo();` и три вызова `drawButton(...)` (строки 365–396) заменяются строками `m_saveButton->draw();`, `m_loadButton->draw();`, `m_closeButton->draw();`;
- `onMouseEvent` — ровно:
  ```cpp
      if (!m_open) {
          return;
      }
      m_saveButton->onNotifyMouseEvent(event);
      m_loadButton->onNotifyMouseEvent(event);
      m_closeButton->onNotifyMouseEvent(event);
      if (!m_open || event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED) {
          return;
      }
  ```
  затем строки 417–428 форка (выбор слота и поле имени); ветки кнопок Save, Load, Close форка (строки 429–439) не переносятся;
- `onKeyboardEvent` — строки 442–485 форка: первая проверка — `if (!m_open || !event.isType(eKeyEventType::PRESSED)) { return; }`; сразу после неё — `if (event.hasTextInput()) { appendText(event.getTextInput()); return; }`; `save_slot::removeLastUtf8Character` → `removeLastUtf8CodePoint`;
- `appendText` — строки 489–504 форка (тело `onTextInput`), параметр `const std::string &text`, `save_slot::removeLastUtf8Character` → `removeLastUtf8CodePoint`;
- подключения: `save/SaveSlotsDialog.hpp`, `debug/UiAudit.hpp`, `drawers/SDLDrawer.hpp`, `drawers/cTextDrawer.h`, `game/SaveGameFlow.hpp`, `game/cGameSettings.h`, `gui/GuiButton.h`, `gui/GuiTheme.hpp`, `save/SaveSlotName.hpp`, `utils/Localization.hpp`, `utils/Utf8.hpp`, `<SDL3/SDL.h>`, `<algorithm>`, `<format>`.

### 12. Главное меню

- `src/gamestates/cMainMenuState.h`: сразу после строки `class cMainMenuState : public cGameState {` (строка 35) — строка `    friend class UiAuditAccess;`; после строки `class cGameSettings;` (строка 33) — строка `class SaveSlotsDialog;`; после строки `    eGameStateType getType() override;` (строка 46) — пустая строка и строка `    bool isKeyboardCapturedByUi() const override;`; после строки `    std::unique_ptr<Texture> backGroundDebug;` (строка 74) — строка `    std::unique_ptr<SaveSlotsDialog> m_saveDialog;`.
- `src/gamestates/cMainMenuState.cpp`:
  - после строки `#include "game/VideoFlow.hpp"` (строка 33) — строки `#include "save/SaveGameManager.hpp"` и `#include "save/SaveSlotsDialog.hpp"`;
  - в конструкторе сразу после строки `    buildHdMenu();` (строка 69):
    ```cpp
        m_saveDialog = std::make_unique<SaveSlotsDialog>(
            services->saveGameFlow,
            m_sdlDrawer,
            m_textDrawer,
            m_settings,
            [this]() {
                m_stateTransitions->fadeOut();
            });
    ```
  - строка 163 `    addButton(localization::text("Load", "Загрузить"), false, nullptr);` заменяется строками:
    ```cpp
        addButton(localization::text("Saved games", "Сохранения"), SaveGameManager::hasAnySave(), [this]() {
            m_saveDialog->open(false, false);
        });
    ```
  - в `draw` сразу перед строкой `    // MOUSE` (строка 265) — строки `    if (m_saveDialog->isOpen()) {`, `        m_saveDialog->draw();`, `    }` и пустая строка;
  - первыми строками тела `onNotifyMouseEvent` — `if (m_saveDialog->isOpen()) { m_saveDialog->onMouseEvent(event); return; }` (четыре строки, отступ 4 пробела);
  - первыми строками тела `onNotifyKeyboardEvent` — `if (m_saveDialog->isOpen()) { m_saveDialog->onKeyboardEvent(event); return; }` (четыре строки);
  - в конце файла — определение `bool cMainMenuState::isKeyboardCapturedByUi() const { return m_saveDialog->isCapturingText(); }` (четыре строки).

### 13. Меню настроек

- `src/gamestates/cOptionsState.h`: после строки `class cGameSettings;` (строка 37) — строка `class SaveSlotsDialog;`; после строки `    void refresh();` (строка 54) — пустая строка и строка `    bool isKeyboardCapturedByUi() const override;`; после строки `    GuiButton *m_languageButton = nullptr;` (строка 73) — строка `    GuiButton *m_loadGameButton = nullptr;`; после строки `    std::unique_ptr<GuiWindow> m_guiWindow;` — строка `    std::unique_ptr<SaveSlotsDialog> m_saveDialog;`.
- `src/gamestates/cOptionsState.cpp`:
  - после строки `#include "utils/Localization.hpp"` (строка 46) — строки `#include "save/SaveGameManager.hpp"` и `#include "save/SaveSlotsDialog.hpp"`;
  - в конструкторе сразу перед строкой `    refresh();` (строка 78):
    ```cpp
        m_saveDialog = std::make_unique<SaveSlotsDialog>(
            services->saveGameFlow,
            m_sdlDrawer,
            m_textDrawer,
            m_settings,
            [this]() {
                m_stateTransitions->fadeOut();
            },
            [this]() {
                if (m_loadGameButton == nullptr) {
                    return;
                }
                m_loadGameButton->setEnabled(true);
                m_loadGameButton->setTheme(GuiTheme::Remaster());
            });
    ```
  - тело блока `if (m_prevState == GAME_PLAYING) {` (строки 175–197) заменяется ровно:
    ```cpp
            const bool hasSaves = SaveGameManager::hasAnySave();
            const cRectangle &saveRect = relativeRect(menuLayout.save);
            auto saveButton = GuiButtonBuilder()
                    .withRect(saveRect)
                    .withLabel(localization::text("Save game", "Сохранить игру"))
                    .withTextDrawer(m_textDrawer)
                    .withRenderer(m_sdlDrawer)
                    .withTheme(controlTheme)
                    .withKind(buttonKind)
                    .onClick([this]() {
                        m_saveDialog->open(true, true);
                    })
                    .build();
            m_guiWindow->addGuiObject(std::move(saveButton));

            const cRectangle &loadRect = relativeRect(menuLayout.load);
            auto loadButton = GuiButtonBuilder()
                    .withRect(loadRect)
                    .withLabel(localization::text("Load game", "Загрузить игру"))
                    .withTextDrawer(m_textDrawer)
                    .withRenderer(m_sdlDrawer)
                    .withTheme(hasSaves ? controlTheme : GuiTheme::RemasterInactive())
                    .withKind(buttonKind)
                    .withEnabled(hasSaves)
                    .onClick([this]() {
                        m_saveDialog->open(true, false);
                    })
                    .build();
            m_loadGameButton = loadButton.get();
            m_guiWindow->addGuiObject(std::move(loadButton));
    ```
  - в `draw` сразу после строки `    m_guiWindow->draw();` (строка 657) — строки `    if (m_saveDialog->isOpen()) {`, `        m_saveDialog->draw();`, `    }`;
  - первыми строками тела `onNotifyMouseEvent` — `if (m_saveDialog->isOpen()) { m_saveDialog->onMouseEvent(event); return; }` (четыре строки);
  - `onNotifyKeyboardEvent` (строка 673): параметр получает имя `event`, тело — `if (m_saveDialog->isOpen()) { m_saveDialog->onKeyboardEvent(event); }` (три строки);
  - в `refresh` первыми строками тела — `if (m_saveDialog) { m_saveDialog->close(); }` (три строки); после строки `    m_languageButton = nullptr;` (строка 694) — строка `    m_loadGameButton = nullptr;`;
  - в конце файла — определение `bool cOptionsState::isKeyboardCapturedByUi() const { return m_saveDialog->isCapturingText(); }` (четыре строки).

### 14. Режим отладки интерфейса

- `src/debug/UiAudit.hpp`: после строки `void recordCanvasClick(const char *name);` (строка 45) — строка `void dropClicksUnderModal();`; после строки `    static bool prepareGameScreen(cGame &game, int house, int kind);` (строка 102) — строки:
  ```cpp
      static void writeSaves(cGame &game);
      static bool openMenuSaveDialog(cGame &game);
      static bool saveDialog(cGame &game, int action);
      static bool startSkirmish(cGame &game);
      static bool saveRoundTrip(cGame &game);
  ```
- `src/debug/UiAuditCapture.cpp`: подключение `save/SaveGameManager.hpp`; сразу после функции `recordCanvasClick` (строки 336–339) — пустая строка и функция `dropClicksUnderModal` — строки 321–326 `FORK1:src/debug/UiAuditCapture.cpp` дословно; в `onSetupDone` сразу после строки `    UiAuditAccess::stopCameraEdgeMove(currentGame);` (строка 465) — ровно:
  ```cpp
      const std::filesystem::path savesDirectory = std::filesystem::path(options().outDir) / "saves";
      SaveGameManager::setSavesDirectory(savesDirectory);
      std::error_code savesError;
      std::filesystem::remove_all(savesDirectory, savesError);
  ```
- `src/debug/UiAuditAccess.cpp`: после строки `#include "utils/Localization.hpp"` (строка 50) — строки `#include "gamestates/cMainMenuState.h"`, `#include "save/SaveGameManager.hpp"`, `#include "save/SaveSlotsDialog.hpp"`; после строки `#include <cstdlib>` — строки `#include <filesystem>`, `#include <fstream>`. В конец файла — пять функций:
  - `writeSaves` — строки 138–147 `FORK1:src/debug/UiAuditAccess.cpp` с заменой `std::filesystem::create_directories("saves");` → `std::filesystem::create_directories(SaveGameManager::savesDirectory());`;
  - `openMenuSaveDialog` — строки 149–157 форка;
  - `saveDialog` — строки 159–179 форка;
  - в этих трёх функциях параметр называется `currentGame`, как в остальных функциях файла, и каждое `game` в теле становится `currentGame`;
  - `startSkirmish` — ровно:
    ```cpp
    bool UiAuditAccess::startSkirmish(cGame &currentGame)
    {
        if (!prepareSkirmish(currentGame, 1)) {
            return false;
        }
        auto *setup = dynamic_cast<cSetupSkirmishState *>(currentGame.m_currentState);
        setup->prepareSkirmishGameToPlayAndTransitionToCombatState(setup->iSkirmishMap);
        currentGame.transitionStateIfRequired();
        currentGame.m_gameObjectsContext->getMap()->setDesiredAmountOfWorms(0);
        for (int i = 0; i < cUnits::size(); i++) {
            cUnit *unit = currentGame.m_gameObjectsContext->getUnit(i);
            if (unit != nullptr && unit->isValid() && unit->iPlayer == AI_WORM) {
                unit->die(false, false);
            }
        }
        return currentGame.m_state == GAME_PLAYING;
    }
    ```
  - `saveRoundTrip` — ровно:
    ```cpp
    bool UiAuditAccess::saveRoundTrip(cGame &currentGame)
    {
        std::string error;
        if (!SaveGameManager::saveQuickGame(currentGame, error)) {
            return false;
        }
        std::error_code copyError;
        std::filesystem::copy_file(SaveGameManager::quickSavePath(),
                                   SaveGameManager::savesDirectory() / "roundtrip-first.d2s",
                                   std::filesystem::copy_options::overwrite_existing, copyError);
        if (copyError) {
            return false;
        }
        return SaveGameManager::loadQuickGame(currentGame, error) &&
               SaveGameManager::saveQuickGame(currentGame, error);
    }
    ```
- `src/debug/UiAuditScenes.cpp`:
  - после строки `    {"options-game", "GAME_OPTIONS", "cOptionsState"},` (строка 56) — строки `    {"save-dialog-menu", "GAME_MENU", "SaveSlotsDialog"},` и `    {"save-dialog", "GAME_OPTIONS", "SaveSlotsDialog"},`;
  - сразу после функции `prepareGameOptions` (строки 283–287) — пустая строка и функции: `prepareMenuWithSaves` и `readyMenuSaveDialog` — строки 222–246 `FORK1:src/debug/UiAuditScenes.cpp` дословно; `prepareGameOptionsWithSaves` — тело строк 249–259 форка для `WithSaves = true` без шаблона: `resetSteps(); if (!UiAuditAccess::enterPlaying(game, ATREIDES, 1)) { return false; } UiAuditAccess::writeSaves(game); return true;`; `readySaveDialog<int Action>` — строки 261–282 форка дословно; `prepareSaveRoundTrip` — `resetSteps(); return UiAuditAccess::startSkirmish(game) && UiAuditAccess::saveRoundTrip(game);`;
  - сразу после строки сцены `"main-menu"` (строка 311) — строка `    scene("main-menu-saves", "main-menu", "", "StateSettled", prepareMenuWithSaves),`;
  - сразу после строки сцены `"options-game-main-nosaves"` (строка 428) — ровно:
    ```cpp
        scene("save-dialog-menu", "save-dialog-menu", "", "FixedFrames(10, no readiness flag)", prepareMenuWithSaves,
              readyMenuSaveDialog),
        scene("options-game-main-saves", "options-game", "", "FixedFrames(14, no readiness flag)",
              prepareGameOptionsWithSaves, readyOptionsMenu<0>),
        scene("save-dialog-load", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptionsWithSaves,
              readySaveDialog<0>),
        scene("save-dialog-save-new", "save-dialog", "", "FixedFrames(14, no readiness flag)",
              prepareGameOptionsWithSaves, readySaveDialog<1>),
        scene("save-dialog-overwrite", "save-dialog", "", "FixedFrames(14, no readiness flag)",
              prepareGameOptionsWithSaves, readySaveDialog<2>),
        scene("save-dialog-load-error", "save-dialog", "", "FixedFrames(14, no readiness flag)",
              prepareGameOptionsWithSaves, readySaveDialog<3>),
        scene("save-dialog-save-error", "save-dialog", "", "FixedFrames(14, no readiness flag)",
              prepareGameOptionsWithSaves, readySaveDialog<4>),
        onGameScreen(scene("save-roundtrip", "game-playing", "", kFixedGameFrames, prepareSaveRoundTrip), false),
    ```
  После правки `grep -c 'scene("' src/debug/UiAuditScenes.cpp` даёт 181.

### 15. Скрипты `tools/ui-audit`

- `tools/ui-audit/check_screens.py`: после строки 9 (`CLASS_DIRECTORIES = ...`) — строка `CLASS_FILES = ("src/save/SaveSlotsDialog.hpp",)`; в `collect_code_names` строка `    return states + code_classes(sources)` заменяется строками 64–67 `FORK1:tools/ui-audit/check_screens.py` дословно.
- `tools/ui-audit/find_hit_tests.py`: строки 8–9 становятся
  ```python
  DIRECTORIES = ("src/gui", "src/drawers", "src/gamestates", "src/managers", "src/save", "src/sidebar",
                 "src/gameobjects/mentat", "src/controls", "src/debug")
  ```

### 16. Списки сборки

- `src/CMakeLists.txt`: сразу после строки `    game/PreferencesPath.cpp` (строка 46) — строки `    save/SaveBody.cpp`, `    save/SaveFileCodec.cpp`, `    save/SaveGameManager.cpp`, `    save/SaveSlotsDialog.cpp`.
- `tests/CMakeLists.txt`, `TEST_SOURCES`: сразу после строки `    ${CMAKE_SOURCE_DIR}/src/game/Preferences.cpp` — строки `    ${CMAKE_SOURCE_DIR}/src/save/SaveBody.cpp` и `    ${CMAKE_SOURCE_DIR}/src/save/SaveFileCodec.cpp`. Строки `TEST_FILES` — раздел «Тесты».

### 17. Ничего сверх контракта

Других изменений нет: ни переформатирования, ни новых комментариев, кроме строки комментария пункта 10, ни правок `cGame::setState`, ни новых действий клавиш, кроме `QUICK_SAVE` и `QUICK_LOAD`.

## Правила переноса

Правило применяется к каждой строке форка, которую контракт переносит в порт, если пункт контракта не говорит иначе.

1. `global_map` → `*game.m_gameObjectsContext->getMap()`; `global_map.getGeometry()` → `getMap()->getGeometry()`; `global_map.getMaxCells()` → `getMap()->getMaxCells()`.
2. `players[i]` → `*game.m_gameObjectsContext->getPlayer(i)`; `players[i].itemBuilder` → `getItemBuilder()`.
3. `structure[i]` → `game.m_gameObjectsContext->getStructure(i)`.
4. `unit[i]` → `*game.m_gameObjectsContext->getUnit(i)`; `MAX_UNITS` → `cUnits::TOTAL_SLOTS` в `SaveGameManager.cpp` и `UnitSlots` в `SaveBody.cpp`.
5. `mapCamera->` → `game.m_mapCamera->`; `drawManager->` → `game.m_drawManager->`; `renderDrawer->` → `m_sdlDrawer->`.
6. `game.m_skirmish` → `game.m_gameSettings->isSkirmish()` / `setSkirmish(...)`; `game.m_region` / `game.m_mission` → `game.m_dataCampaign->region` / `->mission`; `game.m_winFlags` / `m_loseFlags` → `game.m_gameConditionChecker->m_winFlags` / `m_loseFlags` при чтении и `setWinFlags` / `setLoseFlags` при записи.
7. `sStructureInfo[t]` → `game.m_infoContext->getStructureInfo(t)`.
8. Имена членов форка → имена членов порта по таблице пункта 4 (`iNextCell` → `movement.iNextCell`, `iAttackUnit` → `combat.iAttackUnit`, `iBodyFacing` → `rendering.iBodyFacing`, `bSelected` → `m_bSelected`, `TIMER_move` → `moveTimer.get()` / `reset(...)`, поля `cBuildingListItem` — с префиксом `m_`, `myList` → `m_myList`).
9. `cLogger::getInstance()->log(LOG_INFO, COMP_GAMERULES, "<заголовок>", path.string())` → `Logger::info(COMP_GAMERULES, "<заголовок>", "{}", path.string())`.
10. `m_game.m_screenW` / `m_screenH` → `m_settings->getScreenW()` / `getScreenH()`.
11. `assert(` → `d2tm_assert(`; подключения `<SDL2/...>` не переносятся, заголовки SDL3 — как в порту; `cGame.h` → `game/cGame.h`; `d2tmc.h` не подключается.
12. Строки с `factory_pad`, `FactoryPad`, `cUnitFactory`, `bRollingOffFactoryPad`, `iRollingOffFactoryPadStructureId`, `FACTORYPAD` не переносятся.
13. Вызов функции форка, у которой нет пары в порту и которая не названа в контракте или правилах, — блок `## Q-P8-NN` и стоп.

## Сохранить из апстрима

1. Закладки камеры 1–4 (`F1`–`F4`, `Alt+F1`–`Alt+F4`) и отладочные клавиши `Shift,Tab,F*` не меняются.
2. `preferences.ini` и `campaign-progress.ini` лежат в каталоге SDL (`PreferencesPath`); код путей не меняется.
3. Механизм ввода текста порта (`isKeyboardCapturedByUi`, `syncTextInputState`, `getTextInput`) не меняется; метода `onTextInput` нет.
4. `cGame::setState`, `cGame::missionInit`, `cGame::setupPlayers` не меняются.
5. Предел юнитов (`cUnits::TOTAL_SLOTS`), ожидание слота юнита (`m_waitingForUnitSlot`), пауза постройки (`PAUSED`) и память тумана работают после загрузки, потому что их состояние входит в файл.
6. Остальные кнопки главного меню и меню настроек не меняются.
7. Режим отладки интерфейса запускается с рабочим каталогом, который задал вызывающий скрипт.

### Не делать в этом шаге

- Раздел FACTORYPADS, `FactoryPad.hpp`, `cUnitFactory`, `FactoryPadSaveTests.cpp` — шаг П8а.
- Конвертер сохранений прошлых версий.
- Сохранение заказов космопорта, ИИ, статистики миссии, зума и закладок камеры.
- Музыкальный блок и `cGame` сверх пункта 7 — шаг П9; панель приказов — П10а; `cOrderProcesser` — П10б.
- Новый вид окна слотов: вид — как в форке.

## Тесты

Тесты пишутся в шаге 1 плана. В шаге 2 они собираются и краснеют до кода шагов 3–5.

- **T1 — `tests/save/test_SaveFileCodec.cpp`**, тег `[P8]`, имена случаев начинаются с `P8 `. Подключает `save/SaveFileCodec.hpp`, `save/SaveGameManager.hpp`, `utils/Localization.hpp`. Тело для случаев 1–5 — строка `"META 0 1 0\nTEXT Проверка Ёжик\nEND\n"`, `encoded = save_file::encode(тело, 1)`.
  1. «P8 SaveFileCodec round trip keeps the body»: `decode(encoded, 1, 1024)` — `succeeded()` и `body` равно телу.
  2. «P8 SaveFileCodec rejects a wrong checksum»: последний байт `encoded` с `^= 1` — `decode(..., 1, 1024)` не `succeeded()`.
  3. «P8 SaveFileCodec rejects another version»: `decode(encoded, 2, 1024)` не `succeeded()`.
  4. «P8 SaveFileCodec rejects a broken header»: `decode("D2TM_SAVE", 1, 1024)` не `succeeded()`.
  5. «P8 SaveFileCodec rejects a file over the size limit»: `decode(encoded, 1, 4)` не `succeeded()`.
  6. «P8 format version 3 rejects version 2 files»: `SaveGameManager::FormatVersion == 3`; `encode(тело, SaveGameManager::FormatVersion)` начинается с `"D2TM_SAVE 3 "` и декодируется с версией 3; `decode(encode(тело, 2), SaveGameManager::FormatVersion, 1024)` не `succeeded()`, а его `error` равен `localization::text("Unsupported save version", "Неподдерживаемая версия сохранения")`.
- **T2 — `tests/save/test_SaveSlotName.cpp`**, тег `[P8]`. Подключает `save/SaveSlotName.hpp`, `utils/Utf8.hpp`.
  1. «P8 SaveSlotName accepts slots 1 to 10 only»: `isValidSlot(1)`, `isValidSlot(10)` — `true`; `isValidSlot(0)`, `isValidSlot(11)` — `false`.
  2. «P8 SaveSlotName collapses spaces and keeps Cyrillic»: `sanitizeName("  Моя   игра Ё  ") == "Моя игра Ё"`.
  3. «P8 SaveSlotName removes control characters»: `sanitizeName("Тест\n\tимени") == "Тестимени"`.
  4. «P8 removeLastUtf8CodePoint removes whole UTF-8 letters»: строка `"Ёж"` после первого вызова — `"Ё"`, после второго — пустая.
  5. «P8 SaveSlotName limit keeps whole UTF-8 letters»: 60 букв `"Я"` подряд → `sanitizeName` даёт строку размера `MaximumNameBytes` (96), последние два байта — `"Я"`.
- **T3 — `tests/save/test_SaveBody.cpp`**, тег `[P8]`. Подключает `save/SaveBody.hpp`, `data/gfxdata.h`. Функция `sample()` в безымянном пространстве имён возвращает снимок:
  - `saveName = "Тест \"кавычки\" и \\ слэш"`, `skirmish = true`, `region = 3`, `mission = 5`, `winFlags = 6`, `loseFlags = 1`, `cameraCell = 9`, `mapWidth = 4`, `mapHeight = 4`, `autoSpawnBlooms = true`, `bloomTimer = 77`, `desiredWorms = 2`, `wormRespawnTimer = 1234`;
  - игрок `p` (0–6): `house = p % 5`, `team = p`, `techLevel = p + 1`, `focusCell = p`, `quota = 100 * p`, `selectedStructure = p == 0 ? 3 : -1`, `credits = 1234.567F + static_cast<float>(p)`, `maxCredits = 5000.25F`, `powerUsage = 10 * p`, `powerProduce = 20 * p`, `alive = p != 6`, `autoSlab = p % 2 == 1`, `primary[t] = t % 3 - 1`, `structures[t] = t % 4`, `upgrades[t] = t % 2`, `appliedUpgrades[u] = u % 3 == 0`;
  - 16 клеток, клетка `i`: `credits = 10 * i`, `type = i % 2 == 0 ? TERRAIN_SAND : TERRAIN_SPICE`, `tile = i`, `smudgeTile = i % 2 == 0 ? 3 : -1`, `smudgeType = i % 4 == 0 ? -1 : i % 3`, `health = 100`, `passable = i % 5 != 0`, `passableFoot = true`, `visibilityMask = i % 2 == 0 ? 1U : 3U`, `seenMask = i % 2 == 1 ? 1U : 0U`;
  - одна запись `fog`: `cell = 5`, `hasTerrain = true`, `terrainType = TERRAIN_SAND`, `terrainTile = 7`, `hasStructure = true`, `structureType = 2`, `structureOwner = 1`, `structureFrame = 3`, `structureOffsetX = 1`, остальные поля — по умолчанию;
  - два здания: `{oldId 0, type 1, player 0, cell 0, hitPoints 400, rallyPoint 5, frame 2, buildPhase 1, unitHeading 4, concrete 0.25F, animate true, animateOnApproach true, smoke 2, repairTimer 1, flagTimer 2, reduceSmokeTimer 3, decayTimer 4, prebuildTimer 5}` и `{oldId 3, type 5, player 1, cell 10, hitPoints 250}`, остальные поля — по умолчанию;
  - два юнита: `{oldId 0, type 3, player 0, cell 6, hitPoints 100, posX 33.25F, posY 64.5F, experience 0.1F, groupMask 21, nextCell 7, goalCell 9, path[k] = k % 16 - 1, pathIndex 2, pathFails 1, calculatePath true, attackStructure 3, structureId 0, credits 700, transferType 1, bodyFacing 2, headFacing 3, bodyShouldFace 4, headShouldFace 5, frame 1, selected true, action 1, mission 2, harvestCellMemory 11, stayAtGoalCell true, timers[k] = k + 1}` и `{oldId UnitSlots - 1, type 10, player 1, cell 15}`;
  - одно подкрепление `{delay 30, unitType 4, player 1, cell 12, repeat true, remove false, originalDelay 60}`;
  - одна запись очереди `{player 0, slot 2, timer 5, listType 3, buildType 1, buildId 4, subList 0, progress 50, buildFrame 7, timesToBuild 2, timesOrdered 0, state 2, waitingForUnitSlot true, progressFrameTimer 0.3F, flashingTimer 4, timerCap 35}`.

  Случаи (везде `body1 = serializeBody(sample())`):
  1. «P8 save body survives snapshot to body to snapshot to body»: `deserializeBody(body1, restored, error)` — `true`, `error` пуст, `serializeBody(restored) == body1`.
  2. «P8 save body keeps port state exactly»: после `deserializeBody(body1, restored, error)`: `restored.saveName == sample().saveName`; `restored.players[1].credits == sample().players[1].credits`; `restored.players[0].appliedUpgrades[3]` — `true`, `appliedUpgrades[1]` — `false`; `restored.cells[1].seenMask == 1U`; `restored.fog.size() == 1`, `restored.fog[0].structureFrame == 3`, `restored.fog[0].hasUnit` — `false`; `restored.units[0].posX == 33.25F`, `experience == 0.1F`, `groupMask == 21`, `timers[11] == 12`, `harvestCellMemory == 11`, `stayAtGoalCell` — `true`; `restored.units[1].oldId == UnitSlots - 1`; `restored.buildQueue[0].state == 2`, `waitingForUnitSlot` — `true`, `progressFrameTimer == 0.3F`.
  3. «P8 save body without END is rejected»: `body1` оканчивается на `"END\n"`; `body1` без последних четырёх символов — `deserializeBody` возвращает `false`, `error` не пуст.
  4. «P8 save body rejects values out of range»: три снимка `sample()` с одной правкой каждый — `buildQueue[0].state = 6`; `units[0].groupMask = 32`; `cells[0].type = 0` — у каждого `deserializeBody(serializeBody(снимок), ...)` возвращает `false`.
- **T4 — `tests/save/test_QuickSaveKeys.cpp`**, тег `[P8]`. Подключает `controls/cKeyBindings.h`, `utils/cIniFile.h`, `<bitset>`, `<string>`; вспомогательная `pressed(SDL_Scancode)` — как в `tests/controls/test_cKeyBindings.cpp:17-22`.
  1. «P8 quick save and quick load default keys»: у `cKeyBindings` после `loadDefaults()` — `matches(pressed(SDL_SCANCODE_F5), s_KeysCombo{}, eKeyAction::QUICK_SAVE)` и `matches(pressed(SDL_SCANCODE_F9), s_KeysCombo{}, eKeyAction::QUICK_LOAD)` — `true`.
  2. «P8 viewport bookmark 5 moved to F6»: `JUMP_TO_VIEWPORT_BOOKMARK_5` — `true` для `SDL_SCANCODE_F6` с `s_KeysCombo{}` и `false` для `SDL_SCANCODE_F5` с `s_KeysCombo{}`; `SAVE_VIEWPORT_BOOKMARK_5` — `true` для `SDL_SCANCODE_F6` с `altPressed = true` и `false` для `SDL_SCANCODE_F5` с `altPressed = true`.
  3. «P8 quick keys do not fire with the debug modifiers»: с `shiftPressed = true` и `tabPressed = true` — `QUICK_SAVE` на `SDL_SCANCODE_F5` и `QUICK_LOAD` на `SDL_SCANCODE_F9` — `false`; `DEBUG_REVEAL_MAP` на `SDL_SCANCODE_F5` и `DEBUG_SPAWN_WORM` на `SDL_SCANCODE_F9` — `true`.
  4. «P8 settings.ini binds F5, F9 and F6»: `cIniFile ini(std::string(D2TM_SOURCE_DIR) + "/resources/bin/settings.ini")`; `ini.hasSection("KEYS")` — `true`; у `cKeyBindings` после `loadDefaults()` и `loadFromSection(ini.getSection("KEYS"))` шесть вызовов `matches` из случаев 1 и 2 дают те же ответы.
- **T5 — новый скрипт `tests/ui_audit/ui_audit_saves.py`**, по образцу `tests/ui_audit/ui_audit_part3a_scenes.py` (аргумент `--run-dir`, `support.GameRun`, запуск `--ui-audit-scene <id> --ui-audit-out <game.out>`, разбор `<id>.geometry.jsonl`). Для каждой сцены: код выхода 0, есть PNG и журнал; `clicks` — множество полей `name` записей `"k": "click"`, `texts` — список полей `s` записей `"k": "text"`. `DIALOG = {"save-slot:1", …, "save-slot:10", "save-name"}`. Проверки:
  1. `main-menu`: `"Saved games"` в `texts`; `"GuiButton:Saved games"` нет в `clicks`.
  2. `main-menu-saves`: `"GuiButton:Saved games"` в `clicks`.
  3. `options-game-main-nosaves`: `"GuiButton:Save game"` в `clicks`; `"GuiButton:Load game"` нет.
  4. `options-game-main-saves`: `"GuiButton:Save game"` и `"GuiButton:Load game"` в `clicks`.
  5. `save-dialog-menu`: `DIALOG ⊆ clicks`; `"GuiButton:Load"`, `"GuiButton:Close"` в `clicks`; `"GuiButton:Save"` нет; `"SAVED GAMES"`, `"01. Save 1"`, `"03. <corrupted>"`, `"04. <empty>"` в `texts`.
  6. `save-dialog-load`: `DIALOG ⊆ clicks`; `"GuiButton:Save"`, `"GuiButton:Load"`, `"GuiButton:Close"` в `clicks`; `"01. Save 1"` в `texts`.
  7. `save-dialog-save-new`: `DIALOG ⊆ clicks`; `"GuiButton:Save"`, `"GuiButton:Close"` в `clicks`; `"GuiButton:Load"` нет; `"Save 4 |"` в `texts`.
  8. `save-dialog-overwrite`: `"GuiButton:Save"`, `"GuiButton:Load"`, `"GuiButton:Close"` в `clicks`; есть текст, начинающийся с `"A very long save name"`.
  9. `save-dialog-load-error`: `"GuiButton:Save"`, `"GuiButton:Close"` в `clicks`; `"GuiButton:Load"` нет; `"The selected slot has no valid save."` в `texts`.
  10. `save-dialog-save-error`: `"GuiButton:Save"`, `"GuiButton:Close"` в `clicks`; `"GuiButton:Load"` нет; есть текст, начинающийся с `"Could not replace save file"`.
  11. `save-roundtrip`: файлы `game.out / "saves" / "roundtrip-first.d2s"` и `game.out / "saves" / "quicksave.d2s"` есть, первый начинается с `b"D2TM_SAVE 3 "`, байты двух файлов равны.

  В конце — проверка `game.preferences_files()` пуст, как в `ui_audit_part3a_scenes.py:274-276`. Ошибки — в `stderr`, код выхода 1 при любой ошибке.
- **T6 — ожидания существующих тестов**, которые меняются, потому что сохранения появляются:
  - `tools/ui-audit/tests/test_port_changes.py`, строки 223–227: в словарь `sources` добавляется `"src/save/SaveSlotsDialog.hpp": "class SaveSlotsDialog {\n",`; строка 232 ждёт `["GAME_MENU", "GAME_REGION", "M", "cA", "SaveSlotsDialog"]` — `collect_code_names` читает класс окна из `CLASS_FILES`.
  - там же, строки 234–235: тест называется `test_e_class_files` и проверяет `self.assertEqual(check_screens.CLASS_FILES, ("src/save/SaveSlotsDialog.hpp",))` — в порту появляется `CLASS_FILES`.
  - там же, строки 238–241: ожидаемый кортеж — `("src/gui", "src/drawers", "src/gamestates", "src/managers", "src/save", "src/sidebar", "src/gameobjects/mentat", "src/controls", "src/debug")` — в `DIRECTORIES` появляется `src/save`.
  - там же, строка 252: ожидаемое множество — `{"src/gameobjects/mentat/x.cpp", "src/save/z.cpp"}` — `src/save` теперь сканируется.
  - `tests/ui_audit/ui_audit_part3a_catalog.py`, строка 36: `EXPECTED_COUNT = 25` (было 24: добавляется сцена `options-game-main-saves` группы `options-game`); строка 66: `for variant in ("main-saves", "main-nosaves", "applied"):`.
  - `tests/ui_audit/ui_audit_part3a_scenes.py`: в словарь `fixed` функции `check_for` сразу после строки `"options-game-main-nosaves": check_options_game_main,` — строка `"options-game-main-saves": check_options_game_main,` (скрипт гоняет все сцены своего каталога).
  - `tests/ui_audit/data/latin-ru-allowed.tsv`: в конец — две строки (разделитель — табуляция):
    ```text
    (02\.\ )?A\ very\ long\ save\ name.*	имя сохранения, которое записывает сцена режима отладки (src/debug/UiAuditAccess.cpp)
    05\.\ Before\ the\ final\ attack	имя сохранения, которое записывает сцена режима отладки (src/debug/UiAuditAccess.cpp)
    ```
    Причина: `ui_audit_translation.py` гоняет все сцены на русском, а имена `writeSaves` форка — английские.
  - Счётчики остальных каталогов не меняются: `ui_audit_part2_catalog.py` (107) не берёт группы `main-menu`, `options-game`, `save-dialog*`, `game-playing`; `ui_audit_part3b_catalog.py` (35) берёт только имена на `game-`; `ui_audit_part3c_catalog.py` (5) — группы `scoring`, `new-map-editor`, `editor`.
- **`tests/CMakeLists.txt`, `TEST_FILES`:** сразу после строки `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_Preferences.cpp` — строки `    ${CMAKE_CURRENT_SOURCE_DIR}/save/test_SaveFileCodec.cpp`, `    ${CMAKE_CURRENT_SOURCE_DIR}/save/test_SaveSlotName.cpp`, `    ${CMAKE_CURRENT_SOURCE_DIR}/save/test_SaveBody.cpp`, `    ${CMAKE_CURRENT_SOURCE_DIR}/save/test_QuickSaveKeys.cpp`.

### Тесты форка → случаи Catch2

| проверка форка | случай |
|---|---|
| `FORK1:tests/SaveFileCodecTests.cpp:35` (круговое декодирование) | T1.1 |
| `:42-47` (контрольная сумма) | T1.2 |
| `:48-53` (версия) | T1.3 |
| `:54-59` (заголовок) | T1.4 |
| `:60-65` (предел размера) | T1.5 |
| `FORK1:tests/SaveSlotNameTests.cpp:19-22` (слоты 1, 10, 0, 11) | T2.1 (4 проверки) |
| `:24-27` (пробелы, кириллица) | T2.2 |
| `:28-31` (управляющие символы) | T2.3 |
| `:33-43` (удаление последней буквы UTF-8, 2 проверки) | T2.4 — на функции порта `removeLastUtf8CodePoint`, которая заменяет `removeLastUtf8Character` |
| `:45-57` (предел 96 байт, 2 проверки) | T2.5 |

Проверок в T1 — 11 (в форке 5), в T2 — 10 (в форке 10).

## PLAN-P8

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tests/save/test_SaveFileCodec.cpp`, `tests/save/test_SaveSlotName.cpp`, `tests/save/test_SaveBody.cpp`, `tests/save/test_QuickSaveKeys.cpp`, `tests/CMakeLists.txt` (`TEST_FILES`), `tests/ui_audit/ui_audit_saves.py`, `tests/ui_audit/ui_audit_part3a_catalog.py`, `tests/ui_audit/ui_audit_part3a_scenes.py`, `tests/ui_audit/data/latin-ru-allowed.tsv`, `tools/ui-audit/tests/test_port_changes.py` | Раздел «Тесты». | помощник A |
| 2 | — | Красный прогон: команда сборки проверки 1, у которой вместо `.tmp/p8/build.log` стоит `.tmp/p8/red-build.log`, — `exit` не `0`; затем `make -k -C .tmp/out/build d2tm_tests > .tmp/p8/red-tests.log 2>&1; echo exit=$?` — `exit` не `0`, и в `red-tests.log` есть строки `error` с каждым из имён `test_SaveFileCodec.cpp`, `test_SaveSlotName.cpp`, `test_SaveBody.cpp`, `test_QuickSaveKeys.cpp`. Запускается до того, как шаги 3–5 создали файлы в `src/save/` и строки `QUICK_SAVE`, `QUICK_LOAD` в `eKeyAction.h`. | помощник A |
| 3 | `src/save/SaveFileCodec.hpp`, `src/save/SaveFileCodec.cpp`, `src/save/SaveSlotName.hpp`, `src/controls/eKeyAction.h`, `src/controls/cKeyBindings.cpp`, `resources/bin/settings.ini`, `src/main.cpp`, `src/CMakeLists.txt`, `tests/CMakeLists.txt` (`TEST_SOURCES`) | Пункты 2, 8, 10, 16 контракта. | помощник A |
| 4 | `src/save/SaveSnapshot.hpp`, `src/save/SaveBody.hpp`, `src/save/SaveBody.cpp`, `src/save/SaveGameManager.hpp`, `src/save/SaveGameManager.cpp`, `src/game/SaveGameFlow.hpp`, `src/include/sGameServices.h`, `src/game/cGame.h`, `src/game/cGame_logic.cpp`, `src/game/cGameConditionChecker.h`, `src/building/cItemBuilder.h`, `src/gameobjects/structures/cAbstractStructure.h`, `src/gameobjects/units/cReinforcements.h`, `src/gameobjects/units/cUnit.h`, `src/gameobjects/map/cMap.h`, `src/gameobjects/players/cPlayer.h`, `src/sidebar/cBuildingListItem.h`, `src/gamestates/cGamePlaying.h`, `src/gamestates/cGamePlaying.cpp` | Пункты 1, 3, 4, 5, 6, 7, 9 контракта. | помощник B |
| 5 | `src/save/SaveSlotsDialog.hpp`, `src/save/SaveSlotsDialog.cpp`, `src/gamestates/cMainMenuState.h`, `src/gamestates/cMainMenuState.cpp`, `src/gamestates/cOptionsState.h`, `src/gamestates/cOptionsState.cpp`, `src/debug/UiAudit.hpp`, `src/debug/UiAuditAccess.cpp`, `src/debug/UiAuditCapture.cpp`, `src/debug/UiAuditScenes.cpp`, `tools/ui-audit/check_screens.py`, `tools/ui-audit/find_hit_tests.py` | Пункты 11, 12, 13, 14, 15 контракта. | помощник C |
| 6 | — | Проверки раздела «Проверки» по порядку. | помощник A |
| 7 | — | Сверка `git diff` и новых файлов с контрактом и таблицей пункта 4 по каждой строке; разбор провалов проверок и поручение правки помощнику того шага, чей файл. | корневая нить |

Дорожка C не собирается без файлов дорожки B: она пишет код по точным текстам заголовков из пунктов 3, 5, 7 и 11 и не собирает ничего сама. Заглушек нет: единственная сборка кода — проверка 1 шага 6 после шагов 3, 4 и 5.

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p8`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P8-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p8 && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p8/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345.
   - `grep -E 'Test +#[0-9]+: P8 ' <ctest.log последней папки> | grep -c Passed` — `19`, и `grep -E 'Test +#[0-9]+: P8 ' <тот же файл> | grep -vc Passed` — `0`.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает; в неё ничего не пиши.
2. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -F -f .tmp/p8/changed-paths.txt` — пустой вывод. Файл `.tmp/p8/changed-paths.txt` — пути файлов `.cpp`, `.hpp` и `.h` из шагов 1, 3, 4 и 5 плана, по одному на строку.
3. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`.
4. **Рабочий каталог.** `: > .tmp/out/run/bin/nlog.txt && mkdir -p .tmp/p8/cwd && (cd .tmp/p8/cwd && SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy XDG_DATA_HOME=$PWD/../xdg LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 20 ../../out/run/bin/d2tm > ../cwd-run.log 2>&1; echo exit=$?)` — `exit=124`; затем `ls -A .tmp/p8/cwd | wc -l` — `0`; `grep -c -F 'Setting state from -1(=INITIALIZE) to 1(=MENU)' .tmp/out/run/bin/nlog.txt` — не меньше `1`.
5. **Скрипты режима отладки интерфейса.**
   - Скрипты: `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_part2_catalog.py`, `ui_audit_part3a_catalog.py`, `ui_audit_part3a_scenes.py`, `ui_audit_part3b_catalog.py`, `ui_audit_part3c_catalog.py`, `ui_audit_language.py`, `ui_audit_translation.py`, `ui_audit_tools_run_combo.py`, `ui_audit_saves.py`.
   - Команда для каждого `<скрипт>`: `mkdir -p .tmp/p8/tmp && TMPDIR=$PWD/.tmp/p8/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p8/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
   - Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал. Каждая команда сама ограничена `timeout 1800`; жди, пока она вернёт код выхода. `ui_audit_part3a_scenes.py`, `ui_audit_translation.py` и `ui_audit_saves.py` идут по несколько минут — это норма.
   - После проверки — `rm -r tests/ui_audit/__pycache__`, если эта папка появилась.
6. **Тесты скриптов.** `(cd tools/ui-audit/tests && python3 -B -m unittest test_port_changes test_check_screens test_find_hit_tests) > .tmp/p8/tools-tests.log 2>&1; echo exit=$?` — `exit=0`, последняя строка лога — `OK`.
7. **Сверки `grep`** (в скобках — ожидаемый вывод):
   - `git diff 6ceb29d1604ad0a487436bb9f1a0c60a746deeb6 -- src | grep -E '^\+' | grep -c -E 'SDL2/|renderDrawer|global_map|cLogger|onTextInput|SDL_StartTextInput|SDL_StopTextInput|factory_pad|FactoryPad|FACTORYPAD|removeLastUtf8Character'` (`0`);
   - `cat src/save/* src/game/SaveGameFlow.hpp | grep -c -E 'SDL2/|renderDrawer|global_map|cLogger|onTextInput|SDL_StartTextInput|SDL_StopTextInput|factory_pad|FactoryPad|FACTORYPAD|removeLastUtf8Character'` (`0`);
   - `grep -c 'FormatVersion = 3' src/save/SaveGameManager.hpp` (`1`);
   - `grep -c -E 'QUICK_SAVE|QUICK_LOAD' src/controls/cKeyBindings.cpp` (`4`); то же для `src/controls/eKeyAction.h` (`2`);
   - `grep -E '^(SAVE_VIEWPORT_BOOKMARK_5|JUMP_TO_VIEWPORT_BOOKMARK_5|QUICK_SAVE|QUICK_LOAD)=' resources/bin/settings.ini` (ровно четыре строки: `SAVE_VIEWPORT_BOOKMARK_5=Alt,F6`, `JUMP_TO_VIEWPORT_BOOKMARK_5=F6`, `QUICK_SAVE=F5`, `QUICK_LOAD=F9`);
   - `grep -c 'SDL_GetBasePath' src/main.cpp` (`1`);
   - `grep -c 'scene("' src/debug/UiAuditScenes.cpp` (`181`);
   - `grep -c 'friend class SaveGameManager;'` по каждому из девяти файлов пункта 6 (`1`, у `src/gameobjects/units/cReinforcements.h` — `2`).
8. `git -c lfs.storage=$PWD/.tmp/p8/lfs status --short` — изменённые (` M`) пути — только пути шагов 1, 3, 4 и 5 плана; новые (`??`) — только `src/save/`, `src/game/SaveGameFlow.hpp`, `tests/save/`, `tests/ui_audit/ui_audit_saves.py`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P8-NN` с выводом и стоп. Ожидания существующих тестов, кроме перечисленных в T6, не меняй.

## Сдача

Последнее сообщение — блок `## DONE-P8 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p8/progress.md`): строка на каждый шаг плана;
- красный прогон шага 2: строки `.tmp/p8/red-tests.log` с `error` (не больше 30);
- вывод каждой проверки 1–8 с кодами выхода (не больше 40 строк на проверку);
- `git diff --stat` и список для коммитов:
  1. тесты: файлы шага 1;
  2. код: файлы шагов 3, 4 и 5.

  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …`;
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p8 --size`; у `.tmp/p8` пометка `оставить — логи проверок нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаги 1 (помощник A), 4 (помощник B) и 5 (помощник C) начинаются одновременно. Помощники B и C не создают файлов в `src/save/`, пока помощник A не записал в журнал хода строку о конце шага 2; до этого они правят существующие файлы своих шагов. Помощник A не создаёт файлов в `src/save/` и строк `QUICK_SAVE`, `QUICK_LOAD` до конца шага 2.
  4. Шаг 2 (помощник A) — сразу после шага 1; шаг 3 (помощник A) — сразу после шага 2.
  5. Шаг 6 (помощник A) — после шагов 3, 4 и 5.
  6. Шаг 7 (корневая нить) — после шага 6.
  7. Сдача и стоп.
- **Параллельно:** шаги 1, 3, 4 и 5 правят разные файлы. Общие у них — тексты заголовков из пунктов 3, 5, 7 и 11 контракта: их пишут дословно, поэтому дорожки сходятся без согласования. Собирает их вместе проверка 1 шага 6.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных. Ожидаемое время: помощник A — 60 минут на шаги 1–2, 30 минут на шаг 3, 120 минут на шаг 6; помощник B — 180 минут; помощник C — 120 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено», «Контракт», «Правила переноса», «Сохранить из апстрима» с подразделом «Не делать в этом шаге»; его шаги плана; раздел «Тесты» и раздел «Проверки» — помощнику A; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p8/`.
  - Корневая нить раздаёт шаги, делает шаг 7, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Остановки:** только на `## DONE-P8` и на блоках `## Q-P8-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P8-NN` и стоп.
- **Рамка правок:** файлы шагов 1, 3, 4 и 5 плана и папка `.tmp/p8/`. Понадобился другой файл — блок `## Q-P8-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` и временные папки скриптов; это не правка.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=a9bda9c6318255670aecab75810e663ed3ef91095a214b541ff20d2adede49dd -->
## Обязательно: правила исполнителя

«Ведущий» в этих правилах — тот, кто ведёт твою задачу: он дал задание и принимает сдачу.

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Фоновые команды. Среда сама будит тебя, когда фоновая команда кончилась (сессия Claude: запуск с `run_in_background`), — долгий прогон запускай в фоне и делай тем временем то, что от него не зависит. Среда не будит (нить Codex) — фоновых команд нет: после остановки исполнителя никто его не разбудит; длинные прогоны — в переднем плане, с таймаутом до 30 минут. Ожидание циклом (`while …; sleep`) запрещено в обоих случаях.
- Git по договорённости с ведущим. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ведущий после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ведущего.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не останавливать и не менять (пользоваться ими как клиент можно), секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. В репозиторий и в корень рабочей копии ничего временного не клади. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. Удалять что-либо вне своей `tmp` — только по разделу «Уборка».
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- Субагенту, которого запускаешь, назначь ожидаемое время работы и запиши его в журнал хода. Время вышло, а итога нет — проверь, как он идёт: скриптом по его журналу или списком агентов среды, а не ожиданием. Стоит или ушёл в сторону — останови и перезапусти с более узкой задачей.
- **Чтение.** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по транскрипту: обрезанный вывод — не чтение.
- **Цель нити (исполнитель Codex).** Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; субагентам цель не ставить.
- **Строка хода (исполнитель Codex).** После чтения до работы и после каждого закрытого пункта задания или плана ведущего — отдельной строкой ответа: `ХОД: [x] <пункт>; [>] <пункт>; [ ] <пункт>`. В строке все пункты по порядку: `[x]` — сделан, `[>]` — в работе, `[ ]` — впереди. По этой строке панель ведущего и владельца показывает план и ход. Исполнитель в сессии Claude строку хода не пишет.
- **Сжатие контекста (исполнитель в сессии Claude).** На границе своих частей — часть закрыта, журнал хода обновлён — сам вызови `request_compact` и закончи ход. В `instructions`: задание, текущая часть и следующий шаг, id фоновых задач и сессий, пути, решения, открытые вопросы и строка «после сжатия перечитай раздел правил в задании». Посреди части не сжимай. После сжатия перечитай задание и журнал хода.

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
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в сдаче;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса.** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи, журнала хода и того, что прямо называет задание, не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- **Общее, а не частное.** Код и поведение — универсальные и масштабируемые: одна логика и одни правила для всего продукта, в любом месте и с любыми сущностями и предметами, а не под конкретное место, персонажа или вещь; частное задают данные. Проблему чинить системно, в общем механизме, а не отдельным исключением для найденного случая.
- **Комментарии в коде.** Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий; исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи из списка — строго по порядку; независимые части одной задачи идут параллельно, как велит её раздел «Организация работы».
- Замечания ведущего выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения.
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
- В целевую ветку сливают только ветку с зелёным CI на её последнем коммите; кто сливает (обычно ведущий), тот после слияния проверяет CI целевой ветки и красной её не оставляет.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Сдача

Сдача — блок `## DONE-<id> | время | HEAD <sha>`, один на задачу; после возврата `REVIEW` — новая сдача. В ней:

- журнал хода без изменений (строка на подпункт: что сделано, коммит, тест) и строки вывода проверок — красный до правки, зелёный после; отдельной таблицы нет;
- числа только из логов, а не из памяти;
- свои вызовы и вызовы субагентов — числами скрипта по транскрипту: Claude — `tools/usage-daily.py <папка> --session <id>`, Codex — `tools/codex-watch.py`;
- раздел «не проверено» — обязателен; пустым без пояснения не бывает;
- раздел «Рабочие места» — по разделу «Уборка»;
- находки вне задачи — списком; issue заводит ведущий;
- `git status --short`;
- три пункта для владельца простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Отдельного отчёта владельцу не создавать.

## Уборка

- В сдаче — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер (`du -sh`), назначение и пометка: `удалить` или `оставить — <почему>`. Назначение — доказательство (на него ссылаются сдача, PR или журнал) или промежуточное; доказательства — только `оставить`.
- Удаляешь только после ответа ведущего `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Объекты сборки, ненужные для повторной проверки, — тоже только после `CLEAN-OK`.
- Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`.
- Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.

<!-- /team-process:executor-rules -->
