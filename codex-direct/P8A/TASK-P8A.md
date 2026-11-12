# Задание P8A — игровые правки зданий: правило размещения, док очистительного завода, площадки заводов, тарелка радара (шаг П8а)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p8a`, ветка `codex/p8a`, `HEAD` — вершина ветки порта `port/up-d06f2fcd` после слияния шага П8 — `010a6eb134661660a077279bb94a36f063b97d7a` (слияние PR #142; дерево равно ревизии `B`, см. «Что уже решено»). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p8a/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p8a/` (дальше — «папка задания»).

## Цель

Игрок ставит здание по одному правилу размещения: подсветка клеток, щелчок и размещение отвечают одинаково, а отказ показывает причину. Харвестер, зашедший на Завод переработки, стоит в центре площадки завода. Готовый юнит Лёгкого и Тяжёлого заводов появляется на площадке завода, сам съезжает на свободную клетку, а если выезды заняты три секунды — его забирает Карриер; пока юнит строится, завод мерцает. Командный пост крутит тарелку по 32 кадрам. Площадки заводов сохраняются и загружаются в разделе `FACTORYPADS` формата версии 3. Готово, когда новые тесты Catch2, сборка со всеми тестами и скрипты режима отладки интерфейса зелёные, а снимки трёх новых сцен лежат в сдаче для оценки вида ведущим.

## Что уже решено

Ревизии:

- `B` = `d95953ef9c46408d25a8782a2c38e4cfb30abbc6` — вершина ветки `codex/p8`: ветка порта со всеми шагами П9, П10а, П10б, П11 и сам П8. Все факты о коде порта ниже — о файлах ревизии `B` (команда `git show d95953ef9:<путь>`). После слияния П8 дерево `HEAD` равно дереву `B`: проверь `git diff d95953ef9 HEAD --stat` — вывод пустой, иначе блок `## Q-P8A-NN` и стоп.
- `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566` — вершина форка, источник переносимых функций. Читай командами `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>` и `git diff e17379a 9208dcf5a -- <путь>`.
- `UP1` = `d06f2fcd2a347182c3774fb96e9a85570405c489` — апстрим; `BASE` = `e17379a` — общий предок форка и апстрима.

Решения владельца, на которые опирается задание (текст — `docs/decisions.md` ведущего):

- Р33, Р34: масштаб мира — приближение камеры; графика только HD; харвестер на площадке завода рисуется в масштабе, которым юнит рисуется на карте.
- Р49, Р53, Р54: у Лёгкого и Тяжёлого заводов правая часть — площадка, как у Завода переработки; пока юнит строится, площадка пуста, а огни в щелях мерцают кадрами 0–6 с тем же шагом, что у Завода переработки; в момент готовности юнит появляется в центре площадки, сам съезжает на свободную клетку, а если все выезды заняты — его забирает Карриер.
- Р55, Р56: тарелка Командного поста — 32 кадра атласа `BUILD_RADAR` (256 × 8192), 55 вызовов `thinkFast` на кадр. Атлас уже лежит в паке порта: `tests/data/hd4_packs_expected.tsv`, строка `sdl_data_hd4.dat 26 BUILD_RADAR PNG 256 8192`. Данные не меняются.
- Р63: новинки апстрима берутся как есть; где они спорят с функцией форка, решает владелец. Три таких места — пункты 1.5–1.7 раздела «Контракт поведения».
- Р81: владелец решил эти три места так, как они записаны в пунктах 1.5–1.7: юнит запрещает бетон 1×1, как в апстриме; плита или стена под чужим зданием не опора, как в апстриме; причины отказа форка уведомлениями (функция `notifyPlacementFailure` контракта), основание одним цветом, при пределе построек — строка апстрима.
- Р70: вид оценивает только ведущий; ты даёшь снимки сцен.
- Р78 и решение шага П8: формат сохранения — версия 3; раздел `FACTORYPADS` добавляется в версию 3 перед записью `END`, номер версии не меняется, старые файлы версии 3 без этого раздела не читаются (это допустимо: релизов между шагами нет).

Четыре функции карты и их коммиты форка (`FORK1`):

- `placement-rule`: `e7a1c04f`, `a8a7f49a`, `9ea227d2`;
- `refinery-dock`: `c655ceb6`, `b6c58b8c`;
- `factory-pads`: `223f24c5`, `e39f6279`, `ac3c6b7d`, `e632b5e3`, `90da98c4`, `7bed86fc`, `46b71484`, `9e8a65e3`, `00d15658`, `5c2cda10`, `29b3ca76`, `f2b5811e`;
- `radar-dish`: `3d3ff49e`, `849650d0`.

Факты порта, которые определяют форму задания (ревизия `d95953ef9`):

1. Тесты Catch2 порта собираются из `tests/CMakeLists.txt` и линкуют только перечисленные там `TEST_SOURCES`; классы игры (`cPlayer`, `cUnit`, `cLightFactory`, `cMap`) в тесты не линкуются. Поэтому каждая переносимая логика, которую проверяют тесты, лежит в заголовке без зависимостей от игры (образец — `src/gameobjects/structures/StarportOrderQueue.hpp`), а классы игры вызывают этот заголовок.
2. В порту нет глобальных `global_map`, `unit[]`, `structure[]`, `players[]`, `structureUtils`, `game`, `renderDrawer`, `mapCamera`: вместо них — указатели `m_objects` (`cGameObjectContext*`), `m_info`/`m_infos` (`cInfoContext*`), `m_mapCamera`, `m_renderer` (`SDLDrawer*`), `m_eventEmitter`, `m_map`. Полная таблица замен — в разделе «Правила переноса».
3. Поля юнита порта сгруппированы: `rendering.iBodyFacing` (тип `Facing`), `movement.iGoalCell`, `position` (закрытое поле; ячейка — `getCell()`, пиксельные координаты — закрытые `setPosX(float)` и `setPosY(float)`, доступные дружественному классу).
4. Юнит создаёт `cUnits::unitCreate(m_objects, m_info, m_eventEmitter, <клетка>, <тип>, <игрок>, <bOnStart>, <isReinforcement>, <доля hp>, <canUseCarryAllReserve>)`; при отсутствии свободного слота (предел апстрима — 300 обычных юнитов и резерв для Карриеров) он возвращает `-1`. Предел проверяет `m_objects->getUnits()->isUnitLimitReached()`; `cItemBuilder` порта не завершает постройку юнита, пока предел достигнут (`src/building/cItemBuilder.cpp`, строки 202–212).
5. Юнит рисует `cUnitDrawer::draw()` (`src/drawers/cUnitDrawer.cpp`, строки 241–356); функций `cUnit::drawSprites` и `cUnit::visualRectangleAt` форка в порту нет.
6. Игроку сообщения показывают событием `GAME_EVENT_NOTIFICATION` с `NotificationEvent{.message, .type}` через `cEventEmitter::emit` (образец — `src/drawers/cCommandBarDrawer.cpp`, строки 342–351); метода `addNotification` у `cPlayer` в порту нет.
7. Подсветка размещения и щелчок в порту проверяют размещение раздельно: `cPlaceItDrawer::drawStatusOfStructureAtCell` (`src/drawers/cPlaceItDrawer.cpp`, строки 71–192) и `cMousePlaceState::mayPlaceIt` (`src/controls/mousestates/cMousePlaceState.cpp`, строки 99–204), а `cPlayer::placeItem` (`src/gameobjects/players/cPlayer.cpp`, строки 1601–1644) проверяет третьим способом — `canPlaceStructureAt`.
8. Структура сохранения порта — чистые `src/save/SaveSnapshot.hpp`, `src/save/SaveBody.cpp` (тестируются) и `src/save/SaveGameManager.cpp` (сборка снимка из игры и восстановление; не тестируется Catch2).

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитай частями до конца. Пути без `/srv/` — от корня рабочей копии. Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

Файлы порта (целиком):

- `src/controls/mousestates/cMousePlaceState.cpp`, `src/controls/mousestates/cMousePlaceState.h`;
- `src/drawers/cPlaceItDrawer.cpp`, `src/drawers/cPlaceItDrawer.h`;
- `src/gameobjects/players/cPlayer.h` и в `src/gameobjects/players/cPlayer.cpp` строки 1560–1660 и 1930–2170;
- `src/gameobjects/structures/cAbstractStructure.h`, `src/gameobjects/structures/cLightFactory.cpp`, `src/gameobjects/structures/cLightFactory.h`, `src/gameobjects/structures/cHeavyFactory.cpp`, `src/gameobjects/structures/cHeavyFactory.h`, `src/gameobjects/structures/cOutPost.cpp`;
- `src/building/cItemBuilder.h` и в `src/building/cItemBuilder.cpp` строки 180–340 и 430–490;
- `src/utils/cStructureUtils.h` и в `src/utils/cStructureUtils.cpp` строки 60–170;
- `src/gameobjects/units/cUnit.h`; в `src/gameobjects/units/cUnit.cpp` строки 95–160, 999–1012, 1380–1560, 1740–1810, 3488–3510, 3990–4070; `src/gameobjects/units/cReinforcements.cpp` строки 178–235;
- `src/drawers/cUnitDrawer.h`, `src/drawers/cUnitDrawer.cpp`; `src/utils/UnitSpriteLayout.hpp`;
- `src/drawers/cStructureDrawer.h` и в `src/drawers/cStructureDrawer.cpp` строки 170–380;
- `src/save/SaveSnapshot.hpp`, `src/save/SaveBody.cpp`, `src/save/SaveBody.hpp`; в `src/save/SaveGameManager.cpp` строки 193–330 и 451–720; `tests/save/test_SaveBody.cpp`;
- `src/debug/UiAudit.hpp`; в `src/debug/UiAuditAccess.cpp` строки 455–480, 600–870, 968–1005; в `src/debug/UiAuditScenes.cpp` строки 345–356 и 535–560;
- `tests/ui_audit/ui_audit_part3b_catalog.py`, `tests/ui_audit/ui_audit_part3b_scenes.py`, `tests/ui_audit/ui_audit_part3a_catalog.py`, `tests/ui_audit/ui_audit_saves.py`;
- `src/CMakeLists.txt` строки 95–125; `tests/CMakeLists.txt` строки 1–60;
- `tests/structures/test_StarportOrders.cpp` — образец формы тестов.

Файлы форка (вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>`):

- `src/controls/mousestates/cMousePlaceState.cpp`;
- `src/drawers/cPlaceItDrawer.cpp`;
- `src/player/cPlayer.cpp` — строки 1501–1557 и 1992–2090; `src/player/cPlayer.h` — строки 50–70;
- `src/utils/WorldObjectScale.hpp`;
- `src/drawers/cStructureDrawer.cpp` — строки 195–260 и 846–897;
- `src/gameobjects/structures/FactoryPad.hpp`;
- `src/gameobjects/structures/cUnitFactory.h`, `src/gameobjects/structures/cUnitFactory.cpp`;
- `src/gameobjects/structures/cLightFactory.cpp`, `src/gameobjects/structures/cHeavyFactory.cpp`, `src/gameobjects/structures/cHeavyFactory.h`, `src/gameobjects/structures/cAbstractStructure.cpp` — строки 165–185 и 705–720;
- `src/building/cItemBuilder.cpp` — строки 398–420 и 780–795;
- `src/utils/cStructureUtils.cpp` — строки 135–175;
- `src/gameobjects/units/cUnit.cpp` — строки 90–110, 1236–1245, 1705–1720, 1945–2070, 3685–3695, 4895–4950; `src/gameobjects/units/cUnit.h` — строки 22–40, 110–120, 160–170, 450–460, 540–550;
- `src/gameobjects/structures/cOutPost.cpp`;
- `src/save/SaveGameManager.cpp` — вывод `git diff e17379a 9208dcf5a -- src/save/SaveGameManager.cpp` по фрагментам с `FACTORYPAD`, `factoryPads`, `restorePad` (три участка: разбор, снимок, восстановление);
- тесты: `tests/PlacementRuleTests.cpp`, `tests/WorldObjectScaleTests.cpp`, `tests/OutpostFrameTests.cpp`, `tests/FactoryPadTests.cpp`, `tests/FactoryPadEngineTests.cpp`, `tests/FactoryPadSaveTests.cpp`, `tests/UnitRenderFixture.cmake`.

## Правила переноса

Правило применяется к каждой строке форка, которую контракт переносит в порт, если пункт контракта не говорит иначе. «Тело функции X форка переносится» значит: строки тела копируются в функцию порта и к каждой применяются правила 1–12; имена и порядок строк остаются, пока правило не требует замены.

1. Карта и геометрия. `global_map.<метод>` → `m_objects->getMap()-><метод>` для методов карты: `occupied`, `canDeployUnitTypeAtCell`, `getCellType`, `getCellIdStructuresLayer`, `getCellIdUnitLayer`, `getCellSlowDown`, `isValidTerrainForStructureAtCell`. Методы геометрии: `getCellX`, `getCellY`, `makeCell`, `isWithinBoundaries`, `getCellWithMapBorders`, `getCellWithMapDimensions`, `getAbsoluteXPositionFromCell`, `getAbsoluteYPositionFromCell`, `getWidth`, `getHeight`, `distance`, `isValidCell` — `global_map.<метод>` и `global_map.getGeometry().<метод>` → `m_objects->getMapGeometry()-><метод>`. В классе `cUnit` вместо `m_objects->getMap()` пиши поле `m_map`.
2. Массивы. `unit[<id>]` → `*m_objects->getUnit(<id>)` (в коде порта это указатель `cUnit *`: `.` → `->`); `structure[<id>]` → `m_objects->getStructure(<id>)`; `players[<id>]` → `*m_objects->getPlayer(<id>)`. Цикл `for (i = 0; i < MAX_UNITS; ...)` → `for (i = 0; i < m_objects->getUnitsSize(); ...)`.
3. Службы. `structureUtils.<метод>` → `m_structureUtils-><метод>` в классах структур (поле добавляет пункт 3.4); в `cItemBuilder` — `m_services->structureUtils-><метод>`. `renderDrawer->` → `m_renderer->` в классах структур и `m_sdlDrawer->` в `cStructureDrawer`; `mapCamera->` → `m_mapCamera->`.
4. Поля юнита. `posX`, `posY` (запись) → `setPosX(<float>)`, `setPosY(<float>)`; `iCell` → `getCell()`; `iGoalCell` → `movement.iGoalCell`; `iBodyFacing`, `iHeadFacing`, `iBodyShouldFace`, `iHeadShouldFace` → `rendering.<то же имя>` с типом `Facing`: значение `faceAngle(fDegrees(...))` → `facingFromInt(faceAngle(fDegrees(...)))`. Поля `iPlayer`, `iType`, `iBringTarget`, `iNewUnitType`, `m_transferType`, `bRollingOffFactoryPad`, `iRollingOffFactoryPadStructureId` пишутся с тем же именем.
5. Создание юнита. `UNIT_CREATE(<клетка>, <тип>, <игрок>, true, false)` → `cUnits::unitCreate(m_objects, m_info, m_eventEmitter, <клетка>, <тип>, <игрок>, true, false)`. `UNIT_FREE_AROUND_MOVE(<id>)` → `cUnit::freeAroundMove(<id>, m_objects)`. `iFindCloseBorderCell(<клетка>)` → `iFindCloseBorderCell(<клетка>, m_objects)`. `CARRYALL_NEAREST_FREE(<игрок>, <клетка>)` → `cUnit::carryallNearestFree(<игрок>, <клетка>, m_objects)`; `SPAWN_CARRYALL_AT_BORDER(<игрок>, <клетка>)` → `cUnit::spawnCarryallAtBorder(<игрок>, <клетка>, m_objects, m_info, m_eventEmitter)` (обе функции — пункт 3.7).
6. Таймеры и частицы. `TIMER_movedelay = <N>` → `movedelayTimer.reset(<N>)`; `cParticle::create(<x>, <y>, <тип>, -1, -1)` → `cParticle::create(<x>, <y>, <тип>, -1, -1, m_objects, m_infos)` в `cUnit` (в структурах — `m_info`).
7. Сложность хода. `players[<игрок>].getDifficultySettings()->getMoveSpeed(<тип>, global_map.getCellSlowDown(<клетка>))` → `m_objects->getPlayer(<игрок>)->getDifficultySettings()->getMoveSpeed(<тип>, m_objects->getMap()->getCellSlowDown(<клетка>))`.
8. `assert(` → `d2tm_assert(` (подключение `include/cAssert.h`).
9. Рисование юнита. `cUnit::visualRectangleAt(...)` и `cUnit::drawSprites(...)` форка заменяют `cUnitDrawer::visualRectangleAt` и `cUnitDrawer::drawSprites` порта (пункт 3.8).
10. Тексты `localization::text("<английский>", "<русский>")` остаются как есть: в порту есть русская локализация.
11. Подключения `<SDL2/...>`, `d2tmc.h`, `map/...`, `player/...` не переносятся; нужные заголовки берутся такими, какие подключает соседний код порта (путь `gameobjects/...`, `context/...`).
12. Комментарии форка в переносимых телах не копируются (абзац «Комментарии в коде»).
13. Вызов функции форка, у которой нет пары в порту и которая не названа в контракте, — блок `## Q-P8A-NN` и стоп.

## Сохранить из апстрима

Это поведение порта остаётся после переноса.

1. `cMousePlaceState::onMouseLeftButtonClicked` проверяет `isStructureLimitReached()` до звука и показывает строку `"Unable to create more."` / `"Больше построить нельзя."` через `m_context->getDrawManager()->setMessage` — пункт 1.8 сохраняет эту ветку.
2. `cPlayer::placeItem`: ветка `isStructureLimitReached() && !isModifyingTerrain` возвращает `nullptr` до создания, готовый элемент остаётся в режиме «поставить»; вызовы `itemToPlace->cancelBuilding()` вместо `setIsBuilding(false)`/`resetProgress()` не меняются.
3. Предел юнитов: `cItemBuilder` (строки 202–212) не завершает постройку юнита при достигнутом пределе; `cUnits::unitCreate` возвращает `-1` без свободного слота; `cStarPort::think_deploy` оставляет заказ. Эти места не меняются.
4. ИИ ставит здания через `cPlayer::placeItem` → `canPlaceStructureAt`; вызовы `canPlaceStructureAt` в `cPlayerBrainSkirmish.cpp`, `cCommandBarDrawer.cpp`, `cGamePlaying.cpp`, `cSetupSkirmishState.cpp` и `placeStructure` не меняются.
5. Запись `uiaudit::recordLabel("place-cell", ...)` в `cPlaceItDrawer` остаётся на каждую клетку основания (скрипт `tests/ui_audit/ui_audit_part3b_scenes.py` ждёт 4 записи).
6. Память тумана войны: `s_RememberedStructure.frame` и `SaveBody` поле `structureFrame` хранят кадр как `int`; кадры тарелки 0–31 в них помещаются, формат не меняется.
7. Флаг Командного поста `drawHdHouseFlag(...)` в `cStructureDrawer::drawStructureForLayer` не меняется.
8. Порядок вызовов в `cStructureDrawer::drawStructureForLayer` не меняется: новая строка пункта 3.11 стоит внутри существующей ветки.

## Контракт поведения

### 1. Правило размещения (функция `placement-rule`)

Одно правило `cPlayer::canPlaceBuildingListItemAt` решает подсветку, щелчок и размещение человека; ИИ остаётся на `canPlaceStructureAt` (как в порту и как в форке, коммит `a8a7f49a`).

**1.1 Новый файл** `src/gameobjects/players/PlacementRule.hpp` — ровно этот текст:

```cpp
#pragma once

#include "include/definitions.h"

namespace placement_rule {

struct CellFacts {
    bool withinBoundaries = true;
    bool validTerrain = true;
    bool structurePresent = false;
    bool livingUnitPresent = false;
};

struct CellVerdict {
    bool outOfBounds = false;
    bool badTerrain = false;
    bool structureBlocks = false;
    bool unitBlocks = false;

    [[nodiscard]] bool allowed() const
    {
        return !outOfBounds && !badTerrain && !structureBlocks && !unitBlocks;
    }
};

inline CellVerdict judgeCell(int structureType, const CellFacts &facts)
{
    CellVerdict verdict;
    if (!facts.withinBoundaries) {
        verdict.outOfBounds = true;
        return verdict;
    }
    if (structureType == SLAB4) {
        return verdict;
    }
    verdict.badTerrain = !facts.validTerrain;
    verdict.structureBlocks = facts.structurePresent;
    verdict.unitBlocks = facts.livingUnitPresent;
    return verdict;
}

struct AnchorFacts {
    bool ownStructure = false;
    bool otherStructure = false;
    bool wallOrSlab = false;
};

inline bool isBuildAnchor(const AnchorFacts &facts)
{
    if (facts.ownStructure) {
        return true;
    }
    if (facts.otherStructure) {
        return false;
    }
    return facts.wallOrSlab;
}

}
```

**1.2 `src/gameobjects/players/cPlayer.h`.** В `struct s_PlaceResult` сразу после строки `bool outOfBounds = false; // (one of the cells) is out of bounds` и пустой строки после неё — строки `bool outOfBuildDistance = false; // no own structure, wall or slab next to the footprint` и пустая строка. После строки `s_PlaceResult canPlaceConcreteAt(int iCell);` — строка `s_PlaceResult canPlaceBuildingListItemAt(int iCell, int iStructureType);`.

**1.3 `src/gameobjects/players/cPlayer.cpp`, новая функция.** Подключение `#include "gameobjects/players/PlacementRule.hpp"` — сразу после последней строки вида `#include "…"` в начале файла. Определение — сразу после закрывающей скобки `cPlayer::canPlaceConcreteAt` и пустой строки, ровно этот текст:

```cpp
s_PlaceResult cPlayer::canPlaceBuildingListItemAt(int iCell, int iStructureType)
{
    s_PlaceResult result;
    MapGeometry *geometry = m_objects->getMapGeometry();
    cMap *map = m_objects->getMap();

    if (iStructureType < 0 || iStructureType >= MAX_STRUCTURETYPES || !geometry->isValidCell(iCell)) {
        result.outOfBounds = true;
        return result;
    }

    const s_StructureInfo &info = m_infos->getStructureInfo(iStructureType);
    const int width = info.bmp_width / TILESIZE_WIDTH_PIXELS;
    const int height = info.bmp_height / TILESIZE_HEIGHT_PIXELS;
    if (width < 1 || height < 1) {
        result.outOfBounds = true;
        return result;
    }

    const int startX = geometry->getCellX(iCell);
    const int startY = geometry->getCellY(iCell);

    for (int offsetX = 0; offsetX < width; offsetX++) {
        for (int offsetY = 0; offsetY < height; offsetY++) {
            placement_rule::CellFacts facts;
            facts.withinBoundaries = geometry->isWithinBoundaries(startX + offsetX, startY + offsetY);
            int structureId = -1;
            int unitId = -1;
            if (facts.withinBoundaries) {
                const int cell = geometry->makeCell(startX + offsetX, startY + offsetY);
                facts.validTerrain = map->isValidTerrainForStructureAtCell(cell);
                structureId = map->getCellIdStructuresLayer(cell);
                unitId = map->getCellIdUnitLayer(cell);
                facts.structurePresent = structureId > -1;
                facts.livingUnitPresent = unitId > -1 && !m_objects->getUnit(unitId)->isDead();
            }

            const placement_rule::CellVerdict verdict = placement_rule::judgeCell(iStructureType, facts);
            result.outOfBounds = result.outOfBounds || verdict.outOfBounds;
            result.badTerrain = result.badTerrain || verdict.badTerrain;
            if (verdict.structureBlocks) {
                result.structureIds.insert(structureId);
            }
            if (verdict.unitBlocks) {
                result.unitIds.insert(unitId);
            }
        }
    }

    bool withinBuildDistance = false;
    const int firstX = std::max(0, startX - 1);
    const int firstY = std::max(0, startY - 1);
    const int endX = std::min(geometry->getWidth(), startX + width + 1);
    const int endY = std::min(geometry->getHeight(), startY + height + 1);

    for (int x = firstX; x < endX && !withinBuildDistance; x++) {
        for (int y = firstY; y < endY; y++) {
            const int cell = geometry->getCellWithMapDimensions(x, y);
            if (cell < 0) {
                continue;
            }

            placement_rule::AnchorFacts anchor;
            const int structureId = map->getCellIdStructuresLayer(cell);
            if (structureId > -1) {
                cAbstractStructure *other = m_objects->getStructure(structureId);
                anchor.ownStructure = other != nullptr && other->getOwner() == getId();
                anchor.otherStructure = !anchor.ownStructure;
            }
            const int terrain = map->getCellType(cell);
            anchor.wallOrSlab = terrain == TERRAIN_WALL || terrain == TERRAIN_SLAB;
            if (placement_rule::isBuildAnchor(anchor)) {
                withinBuildDistance = true;
                break;
            }
        }
    }

    result.outOfBuildDistance = !withinBuildDistance;
    result.success = !result.outOfBounds && !result.badTerrain && result.unitIds.empty() &&
                     result.structureIds.empty() && !result.outOfBuildDistance;
    result.onlyMyUnitsBlock = false;
    return result;
}
```

Если `TERRAIN_WALL`, `TERRAIN_SLAB` или `MapGeometry` не видны в `cPlayer.cpp`, подключи заголовок, который их объявляет (`git grep -n 'TERRAIN_SLAB' -- src/include src/data` и `src/gameobjects/map/MapGeometry.hpp`); других правок нет.

**1.4 `cPlayer::placeItem`.** В теле функции:

- строки
  ```cpp
      bool canPlace = canPlaceStructureAt(destinationCell, iStructureTypeId).success;
      if (!canPlace) {
          return nullptr;
      }
  ```
  заменяются строками
  ```cpp
      const bool isHumanPlayer = isHuman();
      const bool canPlace = isHumanPlayer
                            ? canPlaceBuildingListItemAt(destinationCell, iStructureTypeId).success
                            : canPlaceStructureAt(destinationCell, iStructureTypeId).success;
      if (!canPlace) {
          return nullptr;
      }
  ```
- сразу после оператора `cAbstractStructure *pStructure = pStructureFactory->createStructure(...);` (четыре строки аргументов) и пустой строки — строки
  ```cpp
      if (isHumanPlayer && pStructure == nullptr && !cStructureFactory::isModifyingTerrain(iStructureTypeId)) {
          return nullptr;
      }

  ```
- остальные строки функции (ветка предела, слабы, `buildingListUpdater->onBuildItemCompleted`, `cancelBuilding`) не меняются.

**1.5 Спорное место с апстримом: юниты.** В `cMousePlaceState::mayPlaceIt` апстрима юнит блокирует любое здание, включая `SLAB1`, кроме `SLAB4`, и мёртвый юнит не блокирует; форк разрешал `SLAB1` над юнитом. Текст 1.1 и 1.3 написан по апстриму: `judgeCell` блокирует юнитом всё, кроме `SLAB4`; `livingUnitPresent` ложен для мёртвого юнита. Не меняй это без ответа ведущего (`QUESTIONS-P8A.md`, вопрос 1).

**1.6 Спорное место с апстримом: якорь стройки.** Апстрим не засчитывает плиту под зданием другого игрока как якорь стройки; форк засчитывал. Текст 1.1 и 1.3 (`isBuildAnchor`) написан по апстриму. Не меняй без ответа ведущего (вопрос 2).

**1.7 Спорное место с апстримом: строка о пределе зданий.** Строку апстрима `"Unable to create more."` ветка 1.8 сохраняет; строка форка «Cannot place another structure: the structure limit has been reached.» не переносится. Не меняй без ответа ведущего (вопрос 3).

**1.8 `src/controls/mousestates/cMousePlaceState.h` и `.cpp`.**

- `.h`: после строки `class cBuildingListItem;` — строка `struct s_PlaceResult;`. Объявление `bool mayPlaceIt(cBuildingListItem *itemToPlace, int mouseCell);` заменяется строками
  ```cpp
      bool mayPlaceIt(cBuildingListItem *itemToPlace, int mouseCell, s_PlaceResult *result = nullptr);

      void notifyPlacementFailure(const s_PlaceResult &result);
  ```
- `.cpp`: подключения `#include "game/cEventEmitter.h"` и `#include "include/sGameEvent.h"` — сразу после последней строки вида `#include "…"` в начале файла. Функции `onMouseLeftButtonClicked` и `mayPlaceIt` заменяются целиком на этот текст (строки `// this assumes the m_context has been updated beforehand...`, `int mouseCell = ...`, `if (mouseCell < 0)` и `itemToPlace` в начале `onMouseLeftButtonClicked` совпадают с текущими), а сразу после `mayPlaceIt` добавляется `notifyPlacementFailure`:

```cpp
void cMousePlaceState::onMouseLeftButtonClicked()
{
    // this assumes the m_context has been updated beforehand...
    int mouseCell = m_context->getMouseCell();

    if (mouseCell < 0) {
        return;
    }

    cBuildingListItem *itemToPlace = m_player->getSideBar()->getList(eListType::LIST_CONSTYARD)->getItemToPlace();
    if (itemToPlace == nullptr) {
        return;
    }

    s_PlaceResult result;
    if (!mayPlaceIt(itemToPlace, mouseCell, &result)) {
        notifyPlacementFailure(result);
        return;
    }

    const int structureType = itemToPlace->getBuildId();
    if (m_context->getObjects()->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(structureType)) {
        m_context->getDrawManager()->setMessage(localization::text("Unable to create more.", "Больше построить нельзя."));
        return;
    }

    cAbstractStructure *placed = m_player->placeItem(mouseCell, itemToPlace);
    if (placed == nullptr && !cStructureFactory::isModifyingTerrain(structureType)) {
        notifyPlacementFailure(m_player->canPlaceBuildingListItemAt(mouseCell, structureType));
        return;
    }

    m_context->getAudioContext()->playSound(SOUND_PLACE);
    m_context->toPreviousState();
}

bool cMousePlaceState::mayPlaceIt(cBuildingListItem *itemToPlace, int mouseCell, s_PlaceResult *result)
{
    if (itemToPlace == nullptr || mouseCell < 0) {
        return false;
    }

    d2tm_assert(itemToPlace->getBuildId() > -1);
    const s_PlaceResult placement = m_player->canPlaceBuildingListItemAt(mouseCell, itemToPlace->getBuildId());
    if (result != nullptr) {
        *result = placement;
    }
    return placement.success;
}

void cMousePlaceState::notifyPlacementFailure(const s_PlaceResult &result)
{
    const char *message = localization::text(
        "Cannot build here.",
        "Здесь нельзя строить.");
    if (result.success) {
        message = localization::text(
            "Unable to create more.",
            "Больше построить нельзя.");
    }
    else if (result.outOfBounds) {
        message = localization::text(
            "Cannot build here: the structure would be outside the map.",
            "Здесь нельзя строить: постройка выходит за пределы карты.");
    }
    else if (result.badTerrain) {
        message = localization::text(
            "Cannot build here: this terrain does not support structures.",
            "Здесь нельзя строить: неподходящий рельеф.");
    }
    else if (!result.unitIds.empty()) {
        message = localization::text(
            "Cannot build here: a unit occupies the site.",
            "Здесь нельзя строить: клетку занимает юнит.");
    }
    else if (!result.structureIds.empty()) {
        message = localization::text(
            "Cannot build here: a structure occupies the site.",
            "Здесь нельзя строить: клетку занимает постройка.");
    }
    else if (result.outOfBuildDistance) {
        message = localization::text(
            "Cannot build here: the site is too far from your base.",
            "Здесь нельзя строить: место слишком далеко от вашей базы.");
    }
    m_context->getEventEmitter()->emit(s_GameEvent{
        .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
        .data = NotificationEvent{
            .message = message,
            .type = eNotificationType::BAD,
        }
    });
}
```

Остальные функции файла, включая `#define SCANWIDTH`, которого после замены в файле нет, не меняются.

**1.9 `src/drawers/cPlaceItDrawer.cpp`.** Определение `cPlaceItDrawer::drawStatusOfStructureAtCell` (строки 71–192) заменяется целиком этим текстом; остальные функции и подключения файла не меняются:

```cpp
void cPlaceItDrawer::drawStatusOfStructureAtCell(cBuildingListItem *itemToPlace, int mouseCell)
{
    d2tm_assert(itemToPlace);
    if (mouseCell < 0) return;

    const int structureId = itemToPlace->getBuildId();
    d2tm_assert(structureId > -1);

    const s_PlaceResult placement = m_player->canPlaceBuildingListItemAt(mouseCell, structureId);
    const int cellWidth = m_structureUtils->getWidthOfStructureTypeInCells(structureId);
    const int cellHeight = m_structureUtils->getHeightOfStructureTypeInCells(structureId);

    const int iCellX = m_objects->getMapGeometry()->getCellX(mouseCell);
    const int iCellY = m_objects->getMapGeometry()->getCellY(mouseCell);

    const int iDrawX = m_objects->getMap()->mouse_draw_x(mouseCell);
    const int iDrawY = m_objects->getMap()->mouse_draw_y(mouseCell);

    for (int iX = 0; iX < cellWidth; iX++) {
        for (int iY = 0; iY < cellHeight; iY++) {
            const int cellX = iCellX + iX;
            const int cellY = iCellY + iY;
            if (!m_objects->getMapGeometry()->isWithinBoundaries(cellX, cellY)) {
                continue;
            }

            const int cell = m_objects->getMapGeometry()->makeCell(cellX, cellY);
            Color itemToPlaceColor = Color::PlaceBad;
            const char *auditType = "BAD";
            if (placement.success) {
                if (m_objects->getMap()->getCellType(cell) == TERRAIN_SLAB) {
                    itemToPlaceColor = Color::PlaceGood;
                    auditType = "GOOD";
                }
                else {
                    itemToPlaceColor = Color::PlaceNeutral;
                    auditType = "NEUTRAL";
                }
            }

            const float desiredWidth = m_mapCamera->getZoomedTileWidth();
            const float desiredHeight = m_mapCamera->getZoomedTileHeight();
            const float posX = iX * desiredWidth;
            const float posY = iY * desiredHeight;
            if (uiaudit::isEnabled()) { uiaudit::recordLabel("place-cell", structureId, auditType, static_cast<int>(iDrawX + posX), static_cast<int>(iDrawY + posY), static_cast<int>(desiredWidth), static_cast<int>(desiredHeight), uiaudit::Rect{iDrawX, iDrawY, static_cast<int>(cellWidth * desiredWidth), static_cast<int>(cellHeight * desiredHeight)}); }
            m_sdlDrawer->renderRectFillColor(iDrawX + posX, iDrawY + posY, desiredWidth, desiredHeight, itemToPlaceColor);
        }
    }
}
```

**1.10 Что не меняется:** `cPlaceItDrawer::drawStructureIdAtMousePos`, `cPlayer::canPlaceStructureAt` обеих перегрузок, `cPlayer::canPlaceConcreteAt`, `cPlayer::placeStructure`, все вызовы `canPlaceStructureAt` вне `placeItem`.

### 2. Док харвестера на Заводе переработки (функция `refinery-dock`)

Харвестер, находящийся внутри Завода переработки, рисуется поверх здания в центре площадки: раскладка — `refineryHarvesterLayout` форка (коммиты `c655ceb6`, `b6c58b8c`; итоговые смещения `32.375F` и `0.625F`).

**2.1 Новый файл** `src/utils/WorldObjectScale.hpp` — дословная копия файла форка, включая его комментарий: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp > src/utils/WorldObjectScale.hpp`. Файл не правится.

**2.2 `src/drawers/cStructureDrawer.h`.** После строки `void drawStructureAnimationRefinery(cAbstractStructure *structure);` — строка `void drawHarvesterOnRefineryPad(cAbstractStructure *structure) const;`.

**2.3 `src/drawers/cStructureDrawer.cpp`.** Подключения `#include "utils/WorldObjectScale.hpp"`, `#include "include/Facing.h"`, `#include <cmath>` — сразу после последней строки вида `#include "…"` в начале файла, если таких строк в файле ещё нет. В `drawStructureAnimationRefinery` после строки `drawStructureAnimation(structure);` — строки

```cpp
    if (structure->hasUnitWithin()) {
        drawHarvesterOnRefineryPad(structure);
    }
```

и сразу после закрывающей скобки `drawStructureAnimationRefinery` и пустой строки — новая функция, ровно этот текст (это тело `drawHarvesterOnRefineryPad` из `FORK1:src/drawers/cStructureDrawer.cpp`, строки 846–897, по правилам переноса; прямоугольник здания считается на месте, потому что `getVisualRectangle` форка в порт не переносится):

```cpp
void cStructureDrawer::drawHarvesterOnRefineryPad(cAbstractStructure *structure) const
{
    if (!structure || !structure->hasUnitWithin()) {
        return;
    }
    const int unitId = structure->getUnitIdWithin();
    if (unitId < 0 || unitId >= m_objects->getUnitsSize()) {
        return;
    }
    cUnit *harvester = m_objects->getUnit(unitId);
    if (!harvester->isValid() || harvester->iType != HARVESTER) {
        return;
    }

    Texture *bitmap = m_objects->getPlayer(structure->getOwner())->getUnitBitmap(HARVESTER);
    if (!bitmap) {
        return;
    }
    const int frameWidth = harvester->getBmpWidth();
    const int frameHeight = harvester->getBmpHeight();
    const int bodyFrame = convertAngleToDrawIndex(facingToInt(Facing::DOWN));
    const cRectangle source = {
        bodyFrame * frameWidth,
        0,
        frameWidth,
        frameHeight,
    };

    const WorldObjectLayout harvesterVisual = refineryHarvesterLayout(
        structure->iDrawX(),
        structure->iDrawY(),
        static_cast<int>(std::lround(m_mapCamera->factorZoomLevel(structure->getWidthInPixels()))),
        static_cast<int>(std::lround(m_mapCamera->factorZoomLevel(structure->getHeightInPixels())))
    );
    const cRectangle destination = {
        harvesterVisual.x,
        harvesterVisual.y,
        harvesterVisual.width,
        harvesterVisual.height,
    };
    m_sdlDrawer->renderStrechSprite(bitmap, source, destination);
}
```

Если `convertAngleToDrawIndex` не виден в файле, подключи заголовок, который его объявляет (`src/utils/d2tm_math.h`). Других правок в `cStructureDrawer.cpp` по этому пункту нет; строка пункта 3.11 — отдельно.

### 3. Площадки заводов (функция `factory-pads`)

Готовый юнит Лёгкого и Тяжёлого заводов (`cItemBuilder::deployUnit`) не создаётся рядом с заводом, а встаёт на площадку выбранного завода; когда анимация выпуска закончена и есть свободная клетка выезда, юнит создаётся на этой клетке и съезжает с площадки по прямой; если все клетки выезда заняты 600 вызовов подряд, ближайший свободный Карриер владельца (или новый с границы карты) прилетает, забирает юнит с площадки и ставит его у точки сбора или на ближайшей свободной клетке. Пока владелец строит юнит для завода, завод, который получит юнит, мерцает кадрами 0–6 (41 вызов на кадр). Готовые юниты, не поместившиеся на площадку, ждут в очереди площадки без предела. Юнит на площадке создаётся только когда есть свободный слот юнитов: предел апстрима не меняется (проверка `isUnitLimitReached`).

**3.1 `src/gameobjects/structures/FactoryPad.hpp` (новый файл).** Дословная копия файла форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/FactoryPad.hpp > src/gameobjects/structures/FactoryPad.hpp`. Затем в конец файла, сразу перед последней строкой `}` (закрытие `namespace factory_pad`) и одной пустой строкой перед вставкой, добавляются ровно эти строки:

```cpp
inline constexpr int FlickerFrames = 7;
inline constexpr int FlickerTicksPerFrame = 41;

inline Point padOrigin(int structurePixelX, int structurePixelY, int widthInCells, int heightInCells, int tileWidth,
                       int tileHeight)
{
    const Point center = padCenter(widthInCells, heightInCells);
    return {structurePixelX + center.x - tileWidth / 2, structurePixelY + center.y - tileHeight / 2};
}

inline void advanceFlicker(int &frame, int &timer, bool active)
{
    if (!active) {
        frame = 0;
        timer = 0;
        return;
    }
    if (frame < 0) {
        frame = 0;
    }
    ++timer;
    if (timer >= FlickerTicksPerFrame) {
        timer = 0;
        ++frame;
        if (frame >= FlickerFrames) {
            frame = 0;
        }
    }
}

```

Других правок в файле нет.

**3.2 `src/gameobjects/structures/cUnitFactory.h` (новый файл).** Дословная копия файла форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cUnitFactory.h > src/gameobjects/structures/cUnitFactory.h`. Файл не правится.

**3.3 `src/gameobjects/structures/cUnitFactory.cpp` (новый файл).** Тело каждой функции берётся из `FORK1:src/gameobjects/structures/cUnitFactory.cpp` по правилам переноса, кроме функций ниже, которые заданы точным текстом. Подключения файла (порядок — как здесь):

```cpp
#include "cUnitFactory.h"

#include "building/cItemBuilder.h"
#include "context/cGameObjectContext.h"
#include "context/cInfoContext.h"
#include "drawers/cUnitDrawer.h"
#include "gameobjects/map/MapGeometry.hpp"
#include "gameobjects/map/cMap.h"
#include "gameobjects/map/cMapCamera.h"
#include "gameobjects/players/cPlayer.h"
#include "gameobjects/players/cPlayerDifficultySettings.h"
#include "gameobjects/units/cUnit.h"
#include "gameobjects/units/cUnits.h"
#include "include/definitions.h"
#include "utils/cStructureUtils.h"
#include "utils/common.h"
#include "utils/d2tm_math.h"

#include <algorithm>
#include <cmath>
```

Функции и их источники (`FORK1`, строки файла `cUnitFactory.cpp`):

- `cUnitFactory::cUnitFactory() = default;`, `acceptReadyUnit` (18–23), `takeUnitForCarryall` (94–104), `restorePad` (258–261) — перенос без изменений;
- `padOrigin` — ровно:
  ```cpp
  factory_pad::Point cUnitFactory::padOrigin()
  {
      return factory_pad::padOrigin(pos_x(), pos_y(), getWidth(), getHeight(), TILESIZE_WIDTH_PIXELS, TILESIZE_HEIGHT_PIXELS);
  }
  ```
- `findExitCell` (31–43), `padCell` (45–49), `carryallStillCalled` (51–61), `requestCarryall` (63–76), `releaseCarryall` (78–92), `finishRoll` (213–240), `releasePad` (242–256), `drawUnitOnPad` (263–272) — по правилам переноса; в `drawUnitOnPad` вызовы `cUnit::visualRectangleAt(m_pad.unitType, <x>, <y>)` и `cUnit::drawSprites(getOwner(), m_pad.unitType, FACE_DOWN, FACE_DOWN, 0, visual, true)` заменяются на
  ```cpp
      const s_UnitInfo &info = m_info->getUnitInfo(m_pad.unitType);
      const cRectangle visual = cUnitDrawer::visualRectangleAt(m_mapCamera, info, static_cast<float>(origin.x), static_cast<float>(origin.y));
      cUnitDrawer::drawSprites(m_renderer, m_mapCamera, getPlayer(), m_pad.unitType, info, Facing::DOWN, Facing::DOWN, 0, visual, true);
  ```
- `isFlickeringFactory` — ровно:
  ```cpp
  bool cUnitFactory::isFlickeringFactory()
  {
      cItemBuilder *builder = getPlayer()->getItemBuilder();
      if (!builder || !builder->isBuildingUnitForStructureType(getType())) {
          return false;
      }
      return m_structureUtils->findFactoryForFinishedUnit(getPlayer(), getType()) == getStructureId();
  }
  ```
- `thinkFlicker` — ровно:
  ```cpp
  void cUnitFactory::thinkFlicker()
  {
      factory_pad::advanceFlicker(iFrame, m_flickerTimer, isFlickeringFactory());
  }
  ```
- `thinkPad` (134–161) — по правилам переноса, строки не меняются;
- `beginRoll` — тело `FORK1` (163–185) по правилам переноса с одним добавлением: первой строкой тела, перед созданием юнита:
  ```cpp
      if (m_objects->getUnits()->isUnitLimitReached()) {
          return;
      }
  ```
  (при достигнутом пределе юнит остаётся стоять на площадке и попытка повторяется на следующем вызове, как ожидание готового юнита в `cItemBuilder`);
- `advanceRoll` (187–211) — по правилам переноса; вычисление `cost` — по правилу 7.

**3.4 `cAbstractStructure`.** `src/gameobjects/structures/cAbstractStructure.h`: после строки `class SDLDrawer;` — строка `class cStructureUtils;`; после строки `SDLDrawer *m_renderer = nullptr;` — строка `cStructureUtils *m_structureUtils = nullptr;`; после строки `void die(int originId = -1, eBuildType originType = eBuildType::UNKNOWN, int killingDamage = 0); // die` — пустая строка и строка `virtual void releasePad() {}`. `src/gameobjects/structures/cAbstractStructure.cpp`: в `serviceInit` после строки `m_renderer = services->ctx->getSDLDrawer();` — строка `m_structureUtils = services->structureUtils;`; в `die` первой строкой тела (перед `// selected structure`) — `releasePad();` и пустая строка; в `getsCapturedBy` первой строкой тела — `releasePad();` и пустая строка.

**3.5 `cLightFactory`.** `.h`: строка `#include "cAbstractStructure.h"` → `#include "cUnitFactory.h"`; строка `class cLightFactory : public cAbstractStructure {` → `class cLightFactory : public cUnitFactory {`. `.cpp`: строка `cLightFactory::cLightFactory() : cAbstractStructure()` → `cLightFactory::cLightFactory() : cUnitFactory()`; в `think_animation` после строки `think_animation_unitDeploy();` — строка `thinkPad();`.

**3.6 `cHeavyFactory`** (коммиты `ac3c6b7d`, `46b71484`: анимация выпуска кончается, как у Лёгкого завода, кадр не сбрасывается). `.h`: те же две замены, что в 3.5 (`cHeavyFactory`); из класса удаляется поле `int TIMER_animation;` вместе с пустой строкой перед ним. `.cpp`:

- `cHeavyFactory::cHeavyFactory() : cAbstractStructure()` → `cHeavyFactory::cHeavyFactory() : cUnitFactory()`; из конструктора удаляется строка `TIMER_animation = 0;`;
- в `think_animation_unitDeploy` удаляется блок

  ```cpp
      if (iFrame < 10) {
          TIMER_animation++;
          if (TIMER_animation > 35) {
              TIMER_animation = 0;
              iFrame++;
          }
      }

  ```

  и блок
  ```cpp
      else {
          TIMER_flag = 0;
          drawFlash = false;
      }

      if (iFrame > 9) {
          setAnimating(false);
      }
  ```
  заменяется блоком
  ```cpp
      else {
          setAnimating(false);
      }
  ```
- в `think_animation` после строки `think_animation_unitDeploy();` — строка `thinkPad();`;
- в `startAnimating` из ветки `else` удаляется строка `iFrame = 0;`.

**3.7 `cUnit` (`src/gameobjects/units/cUnit.h`, `cUnit.cpp`).**

- `.h`: после строки `class cPathFinder;` — строка `class cUnitFactory;`. В `enum class eTransferType` после строки `DIE, …` — строки `PAD_PICKUP_STAY,` и `PAD_PICKUP_LEAVE,` (без комментариев). После строки `friend class SaveGameManager;` — строка `friend class cUnitFactory;`. После строки `bool bCarryMe; …` — строки `bool bRollingOffFactoryPad;` и `int iRollingOffFactoryPadStructureId;`. После строки `static int carryallTransfer(int iuID, int iGoal, cGameObjectContext* objects);` — строки
  ```cpp
      static int carryallNearestFree(int iPlayer, int iCell, cGameObjectContext *objects);
      static int spawnCarryallAtBorder(int iPlayer, int iCell, cGameObjectContext *objects, cInfoContext *infos, cEventEmitter *eventEmitter);
  ```
  После строки `void forgetAboutUnitToPickUp();` — строка `void pickUpUnitFromFactoryPad();`.
- `.cpp`: подключение `#include "gameobjects/structures/cUnitFactory.h"` — сразу после последней строки вида `#include "…"` в начале файла, если его нет. В `cUnit::init` после строки `bCarryMe = false; …` — строки `bRollingOffFactoryPad = false;` и `iRollingOffFactoryPadStructureId = -1;`. В `cUnit::think` после строки `revealTimer.decrementUntil();` и пустой строки — строки
  ```cpp
      if (bRollingOffFactoryPad) {
          return;
      }

  ```
  В `cUnit::thinkFast` после строки `thinkFast_position();` и пустой строки — тот же блок `if (bRollingOffFactoryPad) { return; }` и пустая строка. В `cUnit::thinkFast_move_airUnit` непосредственно перед строкой `// transfer is to create a new unit` (строка 1469 ревизии `B`) — строки

  ```cpp
          if (m_transferType == eTransferType::PAD_PICKUP_STAY ||
                  m_transferType == eTransferType::PAD_PICKUP_LEAVE) {
              pickUpUnitFromFactoryPad();
              return;
          }

  ```
  В `cUnit::carryall_order` непосредственно перед строкой `else if (transferType == eTransferType::PICKUP && iuID > -1) {` — ветка
  ```cpp
      else if (transferType == eTransferType::PAD_PICKUP_STAY || transferType == eTransferType::PAD_PICKUP_LEAVE) {
          m_transferType = transferType;
          setGoalCell(iBring);
          iBringTarget = movement.iGoalCell;
          iUnitID = -1;
          iNewUnitType = -1;
          bPickedUp = false;
      }
  ```
  Новые функции — после определения `cUnit::forgetAboutUnitToPickUp` (`pickUpUnitFromFactoryPad`) и после определения `cUnit::carryallTransfer` (две статические).

  `cUnit::pickUpUnitFromFactoryPad` — тело `FORK1:src/gameobjects/units/cUnit.cpp`, строки 1956–1999, по правилам переноса; перед строкой `int unitType = -1;` вставляются строки

  ```cpp
      if (factory && factory->getOwner() == iPlayer && factory->hasUnitStandingOnPad() &&
              m_objects->getUnits()->isUnitLimitReached()) {
          return;
      }

  ```
  (при достигнутом пределе Карриер остаётся над площадкой и повторяет попытку на следующем вызове).

  `cUnit::carryallNearestFree` — ровно:
  ```cpp
  int cUnit::carryallNearestFree(int iPlayer, int iCell, cGameObjectContext *objects)
  {
      int nearestId = -1;
      double nearestDistance = 0;
      for (int i = 0; i < objects->getUnitsSize(); i++) {
          cUnit *candidate = objects->getUnit(i);
          if (!candidate->isValid()) continue;
          if (candidate->iPlayer != iPlayer) continue;
          if (candidate->iType != CARRYALL) continue;
          if (candidate->m_transferType != eTransferType::NONE) continue;
          if (candidate->isHidden()) continue;

          const double distance = objects->getMapGeometry()->distance(candidate->getCell(), iCell);
          if (nearestId < 0 || distance < nearestDistance) {
              nearestId = i;
              nearestDistance = distance;
          }
      }
      return nearestId;
  }
  ```
  `cUnit::spawnCarryallAtBorder` — ровно:
  ```cpp
  int cUnit::spawnCarryallAtBorder(int iPlayer, int iCell, cGameObjectContext *objects, cInfoContext *infos, cEventEmitter *eventEmitter)
  {
      const int startCell = iFindCloseBorderCell(iCell, objects);
      if (startCell < 0) {
          return -1;
      }

      const int carryallId = cUnits::unitCreate(objects, infos, eventEmitter, startCell, CARRYALL, iPlayer, true, false, 1.0f, true);
      if (carryallId < 0) {
          return -1;
      }

      MapGeometry *geometry = objects->getMapGeometry();
      const Facing facing = facingFromInt(faceAngle(fDegrees(geometry->getCellX(startCell), geometry->getCellY(startCell),
                                                             geometry->getCellX(iCell), geometry->getCellY(iCell))));
      cUnit *carryall = objects->getUnit(carryallId);
      carryall->rendering.iBodyShouldFace = facing;
      carryall->rendering.iBodyFacing = facing;
      carryall->rendering.iHeadShouldFace = facing;
      carryall->rendering.iHeadFacing = facing;
      carryall->carryall_order(-1, eTransferType::PAD_PICKUP_LEAVE, iCell, -1);
      return carryallId;
  }
  ```
  (последний аргумент `true` у `unitCreate` — резерв слотов для Карриеров, как в `REINFORCE`).

**3.8 `cUnitDrawer` (`src/drawers/cUnitDrawer.h`, `cUnitDrawer.cpp`).** Рисование спрайтов юнита выделяется в статические функции (в форке это `cUnit::drawSprites` и `cUnit::visualRectangleAt`, коммит `e632b5e3`); поведение `cUnitDrawer::draw()` не меняется.

- `.h`: подключения `#include "include/Facing.h"`, `#include "utils/cRectangle.h"`, `#include "gameobjects/units/cUnitInfos.h"` и объявления `class cMapCamera;`, `class cPlayer;` (после `class cTextDrawer;`); в `public` после `void draw();` — строки
  ```cpp
      static cRectangle visualRectangleAt(cMapCamera *mapCamera, const s_UnitInfo &info, float x, float y);
      static void drawSprites(SDLDrawer *renderer, cMapCamera *mapCamera, cPlayer *owner, int unitType, const s_UnitInfo &info,
                              Facing bodyFacing, Facing headFacing, int frameIndex, const cRectangle &visual, bool drawTop);
  ```
- `.cpp`: `visualRectangleAt` — ровно:
  ```cpp
  cRectangle cUnitDrawer::visualRectangleAt(cMapCamera *mapCamera, const s_UnitInfo &info, float x, float y)
  {
      const int offsetX = (TILESIZE_WIDTH_PIXELS - info.bmp_width) / 2;
      const int offsetY = (TILESIZE_HEIGHT_PIXELS - info.bmp_height) / 2;
      return {
          mapCamera->getWindowXPositionWithOffset(static_cast<int>(x), offsetX),
          mapCamera->getWindowYPositionWithOffset(static_cast<int>(y), offsetY),
          static_cast<int>(std::lround(mapCamera->factorZoomLevel(info.bmp_width))),
          static_cast<int>(std::lround(mapCamera->factorZoomLevel(info.bmp_height)))
      };
  }
  ```
  `drawSprites` — перенос строк 257–330 текущего `cUnitDrawer::draw` (от `s_UnitInfo &unitType = m_unit.getUnitInfo();` до закрывающей скобки блока `// Draw TOP`) в новую функцию без изменения порядка и значений, со сменой имён: `unitType` (структура) → `info`; `m_unit.iType` → `unitType` (параметр); `m_renderer` → `renderer`; `m_unit.getMapCamera()` → `mapCamera`; `m_unit.getPlayer()` → `owner` (строка `cPlayer *cPlayer = m_unit.getPlayer();` не переносится, `cPlayer->` → `owner->`); `m_unit.rendering.iFrame` → `frameIndex`; `facingToInt(m_unit.rendering.iHeadFacing)` → `facingToInt(headFacing)`; `facingToInt(m_unit.rendering.iBodyFacing)` → `facingToInt(bodyFacing)`; условие `m_unit.getHitPoints() > -1` → `drawTop`; вычисление `visual` (`UnitSpriteRectangle visual{ux, uy, roundedScaledWidth, roundedScaledHeight}`) заменяется строкой `const UnitSpriteRectangle visualRectangle{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()};` и дальше передаётся в `unitSpriteDestinationRectangle` под этим именем; вызов `m_unit.log(std::format("unit of iType [{}] did not have a bitmap!?", m_unit.iType))` в статической функции заменяется на `Logger::warn(COMP_UNITS, "cUnitDrawer", "unit of type {} did not have a bitmap", unitType)`. В `cUnitDrawer::draw` блок строк 257–330 заменяется строками (после них идёт блок `// when we want to be picked up..` без изменений):
  ```cpp
      const cRectangle visual = {
          ux,
          uy,
          static_cast<int>(std::lround(m_unit.getMapCamera()->factorZoomLevel(m_unit.getBmpWidth()))),
          static_cast<int>(std::lround(m_unit.getMapCamera()->factorZoomLevel(m_unit.getBmpHeight())))
      };
      drawSprites(m_renderer, m_unit.getMapCamera(), m_unit.getPlayer(), m_unit.iType, m_unit.getUnitInfo(),
                  m_unit.rendering.iBodyFacing, m_unit.rendering.iHeadFacing, m_unit.rendering.iFrame, visual,
                  m_unit.getHitPoints() > -1);
  ```
  Подключения `utils/Log.h` и других заголовков, нужных `Logger::warn`, добавь сразу после последней строки вида `#include "…"`, если их нет.

**3.9 `cStructureUtils` (`src/utils/cStructureUtils.h`, `cStructureUtils.cpp`).** `.h`: после строки `int findStructureToDeployUnit(cPlayer *pPlayer, int structureType);` и пустой строки — строка `int findFactoryForFinishedUnit(cPlayer *pPlayer, int structureType);`. `.cpp`: подключения `#include "gameobjects/structures/FactoryPad.hpp"`, `#include "gameobjects/structures/cUnitFactory.h"`, `#include <vector>` — сразу после последней строки вида `#include "…"`; определение — сразу после закрывающей скобки `cStructureUtils::findStructureToDeployUnit` и пустой строки, ровно:

```cpp
int cStructureUtils::findFactoryForFinishedUnit(cPlayer *pPlayer, int structureType)
{
    d2tm_assert(pPlayer);
    const int playerId = pPlayer->getId();
    int primaryId = pPlayer->getPrimaryStructureForStructureType(structureType);
    if (primaryId > -1) {
        cAbstractStructure *primary = m_objects->getStructures()[primaryId];
        if (!primary || !primary->isValid() || primary->getType() != structureType || !primary->belongsTo(playerId)) {
            primaryId = -1;
        }
    }

    std::vector<factory_pad::FactoryCandidate> candidates;
    for (int i = 0; i < MAX_STRUCTURES; i++) {
        cAbstractStructure *theStructure = m_objects->getStructures()[i];
        if (!theStructure || !theStructure->isValid() || !theStructure->belongsTo(playerId) ||
                theStructure->getType() != structureType) {
            continue;
        }
        auto *factory = dynamic_cast<cUnitFactory *>(theStructure);
        if (!factory) {
            continue;
        }
        candidates.push_back({i, factory->isPadFree()});
    }

    const int chosen = factory_pad::chooseFactory(candidates, primaryId);
    if (chosen > -1 && primaryId < 0) {
        pPlayer->setPrimaryBuildingForStructureType(structureType, chosen);
    }
    return chosen;
}

```

**3.10 `cItemBuilder` (`src/building/cItemBuilder.h`, `cItemBuilder.cpp`).** `.h`: после строки `bool isAnotherBuildingListItemInTheSameListBeingBuilt(cBuildingListItem *item);` и пустой строки — строка `bool isBuildingUnitForStructureType(int structureType);` и пустая строка. `.cpp`: подключение `#include "gameobjects/structures/cUnitFactory.h"` — сразу после последней строки вида `#include "…"`; в `cItemBuilder::deployUnit` сразу после строки `d2tm_assert(structureTypeByItem > -1);` и пустой строки — блок

```cpp
    if (structureTypeByItem == LIGHTFACTORY || structureTypeByItem == HEAVYFACTORY) {
        const int factoryId = m_services->structureUtils->findFactoryForFinishedUnit(m_player, structureTypeByItem);
        if (factoryId > -1) {
            static_cast<cUnitFactory *>(m_services->objects->getStructures()[factoryId])->acceptReadyUnit(buildId);
        }
        return;
    }

```

и сразу после закрывающей скобки `cItemBuilder::getItem` и пустой строки — определение

```cpp
bool cItemBuilder::isBuildingUnitForStructureType(int structureType)
{
    for (int i = 0; i < MAX_ITEMS; i++) {
        cBuildingListItem *item = m_items[i];
        if (item == nullptr || !item->isBuilding() || item->getBuildType() != UNIT) {
            continue;
        }
        if (m_services->structureUtils->getStructureTypeByUnitBuildId(item->getBuildId()) == structureType) {
            return true;
        }
    }
    return false;
}

```

**3.11 `cStructureDrawer::drawStructureForLayer`.** Подключение `#include "gameobjects/structures/cUnitFactory.h"` — сразу после последней строки вида `#include "…"`. В ветке `else { drawStructureAnimation(structure); }` (последняя ветка цепочки `if (TURRET || RTURRET) … else if (REFINERY) … else`) после строки `drawStructureAnimation(structure);` — строки

```cpp
                if (auto *factory = dynamic_cast<cUnitFactory *>(structure)) {
                    factory->drawUnitOnPad();
                }
```

**3.12 Сохранение: `src/save/SaveSnapshot.hpp` и `src/save/SaveBody.cpp`.**

- `SaveSnapshot.hpp`: подключение `#include "gameobjects/structures/FactoryPad.hpp"` — сразу после строки `#include "include/definitions.h"`. Перед `struct SaveSnapshot {` — структура

  ```cpp
  struct FactoryPadSave {
      int structureId = -1;
      factory_pad::PadState pad;
  };

  ```

  В `struct SaveSnapshot` после строки `std::vector<BuildQueueState> buildQueue;` — строка `std::vector<FactoryPadSave> factoryPads;`.
- `SaveBody.cpp`, `serializeBody`: сразу перед строкой `output << "END\n";` — строки

  ```cpp
      output << "FACTORYPADS " << save.factoryPads.size() << '\n';
      for (const FactoryPadSave &item : save.factoryPads) {
          output << "FACTORYPAD " << item.structureId << ' ';
          factory_pad::write(output, item.pad);
          output << '\n';
      }
  ```
- `SaveBody.cpp`, `deserializeBody`: сразу перед строкой `if (!expectTag(input, "END")) {` — блок (разбор и проверки из `FORK1:src/save/SaveGameManager.cpp`, коммиты `9e8a65e3` и `f2b5811e`, с константами порта):

  ```cpp
      if (!expectTag(input, "FACTORYPADS") || !readValue(input, count) || count > MAX_STRUCTURES) {
          error = localization::text("Invalid factory pad list", "Некорректный список площадок заводов");
          return false;
      }
      std::array<bool, MAX_STRUCTURES> padStructureSeen{};
      save.factoryPads.resize(count);
      for (FactoryPadSave &item : save.factoryPads) {
          if (!expectTag(input, "FACTORYPAD") ||
              !readValue(input, item.structureId) ||
              !factory_pad::read(input, item.pad, UnitSlots)) {
              error = localization::text("Factory pad data is corrupted", "Повреждены данные площадок заводов");
              return false;
          }
          bool isFactory = false;
          int factoryOwner = -1;
          for (const StructureState &structureItem : save.structures) {
              if (structureItem.oldId == item.structureId) {
                  isFactory = structureItem.type == LIGHTFACTORY || structureItem.type == HEAVYFACTORY;
                  if (isFactory) {
                      factoryOwner = structureItem.player;
                  }
              }
          }
          bool referencesAreValid = item.structureId >= 0 && item.structureId < MAX_STRUCTURES &&
                                    isFactory && !padStructureSeen[item.structureId] &&
                                    item.pad.phase != factory_pad::Phase::Empty &&
                                    item.pad.unitType >= 0 && item.pad.unitType < UnitTypeCount &&
                                    item.pad.carryallId >= -1 && item.pad.carryallId < UnitSlots;
          if (referencesAreValid && item.pad.carryallId >= 0) {
              referencesAreValid = usedUnitIds[item.pad.carryallId];
              for (const UnitState &unitItem : save.units) {
                  if (unitItem.oldId == item.pad.carryallId) {
                      referencesAreValid = referencesAreValid && unitItem.type == CARRYALL &&
                                           unitItem.player == factoryOwner;
                      break;
                  }
              }
          }
          for (const int waitingType : item.pad.waiting) {
              referencesAreValid = referencesAreValid && waitingType >= 0 && waitingType < UnitTypeCount;
          }
          if (referencesAreValid && item.pad.phase == factory_pad::Phase::Rolling) {
              referencesAreValid = item.pad.rollUnitId >= 0 && item.pad.rollUnitId < UnitSlots && usedUnitIds[item.pad.rollUnitId];
              bool foundMatchingRoller = false;
              for (const UnitState &unitItem : save.units) {
                  if (unitItem.oldId == item.pad.rollUnitId) {
                      foundMatchingRoller = unitItem.type == item.pad.unitType && unitItem.player == factoryOwner;
                      break;
                  }
              }
              referencesAreValid = referencesAreValid && foundMatchingRoller;
          }
          if (!referencesAreValid) {
              error = localization::text("Invalid factory pad data", "Некорректные данные площадки завода");
              return false;
          }
          padStructureSeen[item.structureId] = true;
      }
  ```

  Версия формата `SaveGameManager::FormatVersion` остаётся `3`.

**3.13 `src/save/SaveGameManager.cpp`.** Подключение `#include "gameobjects/structures/cUnitFactory.h"` — сразу после строки `#include "gameobjects/structures/cAbstractStructure.h"`. В `captureSnapshot`, в цикле по структурам, сразу после строки `save.structures.push_back(target);` — строки

```cpp

        if (const auto *factory = dynamic_cast<const cUnitFactory *>(source)) {
            if (!factory->isPadFree()) {
                save.factoryPads.push_back({index, factory->getPad()});
            }
        }
```

В `restoreSnapshot` сразу после закрывающей скобки цикла, который вызывает `target->setUnitIdHeadingTowards(source.unitHeading);` (строка 616 ревизии `B`), и перед строкой `restoreCellState(*map, save);` — блок

```cpp
    for (const save_game_detail::FactoryPadSave &source : save.factoryPads) {
        const int newId = structureMapping[source.structureId];
        auto *factory = newId >= 0 ? dynamic_cast<cUnitFactory *>(game.m_gameObjectsContext->getStructure(newId)) : nullptr;
        if (factory == nullptr) {
            continue;
        }
        factory->restorePad(source.pad);
        if (source.pad.phase == factory_pad::Phase::Rolling) {
            cUnit *rolling = game.m_gameObjectsContext->getUnit(source.pad.rollUnitId);
            rolling->bRollingOffFactoryPad = true;
            rolling->iRollingOffFactoryPadStructureId = newId;
        }
    }

```

Поля юнита `bRollingOffFactoryPad` и `iRollingOffFactoryPadStructureId` в записи `UNIT` не пишутся: они восстанавливаются из записи `FACTORYPAD` (так сделано в форке).

### 4. Тарелка радара (функция `radar-dish`)

Тарелка Командного поста перебирает 32 кадра атласа `BUILD_RADAR` по 55 вызовов `thinkFast` на кадр (коммиты `3d3ff49e`, `849650d0`).

**4.1 Новый файл** `src/gameobjects/structures/OutpostDish.hpp` — ровно этот текст:

```cpp
#pragma once

namespace outpost_dish {

inline constexpr int FrameCount = 32;
inline constexpr int CallsPerFrame = 55;

inline void advance(int &frame, int &timer)
{
    ++timer;
    if (timer >= CallsPerFrame) {
        ++frame;
        if (frame >= FrameCount) {
            frame = 0;
        }
        timer = 0;
    }
}

}
```

**4.2 `src/gameobjects/structures/cOutPost.cpp`.** Подключение `#include "gameobjects/structures/OutpostDish.hpp"` — сразу после строки `#include "definitions.h"`. В `cOutPost::thinkFast` строки от `TIMER_flag++;` до закрывающей скобки блока `if (TIMER_flag > 54) { … }` (включая комментарий `// switch between 0 and 7.`) заменяются одной строкой `outpost_dish::advance(iFrame, TIMER_flag);`; два комментария над `TIMER_flag++;` и вызов `cAbstractStructure::thinkFast();` остаются.

### 5. Сцены режима отладки интерфейса и скрипты

Три новые игровые сцены дают снимки вида для ведущего (Р70); круговая проверка сохранения получает площадки.

**5.1 `src/debug/UiAudit.hpp`.** В `enum GameKind` строка `Mcv` → строки `Mcv,`, `RadarDish,`, `RefineryHarvester,`, `FactoryPad` (по одной на строку, с отступом как у соседних). В класс `UiAuditAccess` после строки `static bool saveRoundTrip(cGame &game);` — строка `static bool addFactoryPads(cGame &game);`.

**5.2 `src/debug/UiAuditScenes.cpp`.** Сразу после строки сцены `"game-place-forbidden"` — три строки (образец формы — строка `game-radar-nopower`):

```cpp
    onGameScreen(scene("game-radar-dish", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RadarDish>), false),
    onGameScreen(scene("game-refinery-harvester", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RefineryHarvester>), false),
    onGameScreen(scene("game-factory-pad", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::FactoryPad>), false),
```

В `prepareSaveRoundTrip` строка `return UiAuditAccess::startSkirmish(game) && UiAuditAccess::saveRoundTrip(game);` → `return UiAuditAccess::startSkirmish(game) && UiAuditAccess::addFactoryPads(game) && UiAuditAccess::saveRoundTrip(game);`.

**5.3 `src/debug/UiAuditAccess.cpp`.** Подключения `#include "gameobjects/structures/OutpostDish.hpp"` и `#include "gameobjects/structures/cUnitFactory.h"` — сразу после последней строки вида `#include "…"` в начале файла. В `prepareGameScreen` непосредственно перед `case GameKind::GroupSelect: {` — три ветки:

```cpp
        case GameKind::RadarDish: {
            for (int i = 0; i < MAX_STRUCTURES; i++) {
                cAbstractStructure *s = currentGame.m_gameObjectsContext->getStructures()[i];
                if (s != nullptr && s->isValid() && s->getOwner() == HUMAN && s->getType() == RADAR) {
                    s->setFrame(outpost_dish::FrameCount - 1);
                    s->TIMER_flag = -1000000;
                    return true;
                }
            }
            return false;
        }
        case GameKind::RefineryHarvester: {
            for (int i = 0; i < MAX_STRUCTURES; i++) {
                cAbstractStructure *s = currentGame.m_gameObjectsContext->getStructures()[i];
                if (s != nullptr && s->isValid() && s->getOwner() == HUMAN && s->getType() == REFINERY) {
                    s->enterStructure(base.harvesterId);
                    return s->hasUnitWithin();
                }
            }
            return false;
        }
        case GameKind::FactoryPad: {
            int filled = 0;
            for (int i = 0; i < MAX_STRUCTURES; i++) {
                cAbstractStructure *s = currentGame.m_gameObjectsContext->getStructures()[i];
                if (s == nullptr || !s->isValid() || s->getOwner() != HUMAN) {
                    continue;
                }
                auto *factory = dynamic_cast<cUnitFactory *>(s);
                if (factory == nullptr) {
                    continue;
                }
                factory->acceptReadyUnit(s->getType() == LIGHTFACTORY ? QUAD : TANK);
                filled++;
            }
            return filled == 2;
        }
```

Сцена `game-factory-pad` ждёт ровно два завода игрока (Лёгкий и Тяжёлый из `kBaseSpots`); `filled == 2` — условие успеха сцены.

**5.4 `UiAuditAccess::addFactoryPads`** — определение сразу после определения `UiAuditAccess::saveRoundTrip` в `src/debug/UiAuditAccess.cpp`. Правило функции (код пишет исполнитель по правилу, текст не задан дословно, потому что клетки зависят от карты схватки):

1. Для типов `LIGHTFACTORY` (основание 2×2) и `HEAVYFACTORY` (основание 3×2) ищется место: перебор `column` и `row` от 3 до (ширина карты − 6) и (высота карты − 6) по строкам, первая позиция, где для каждой клетки основания и для каждой клетки кольца шириной 1 вокруг основания верно: клетка допустима (`isValidCell`), нет строения в слое строений, нет юнита в слое юнитов, а для клеток основания ещё `isValidTerrainForStructureAtCell` истинно. Не нашлось — функция возвращает `false`.
2. На найденном месте создаётся здание игрока `HUMAN`: `getStructureFactory()->createStructure(<клетка>, <тип>, HUMAN, 100)`, у результата `setBuildingFase(10)`; `nullptr` — `false`. Лёгкий завод создаётся первым (так второй поиск видит его основание занятым).
3. Лёгкий завод: три вызова `acceptReadyUnit(TRIKE)`, `acceptReadyUnit(QUAD)`, `acceptReadyUnit(TRIKE)` на приведённом к `cUnitFactory` указателе (стоит Трайк, ждут Квад и Трайк).
4. Тяжёлый завод: клетка выезда — клетка колонки `x + 2` (последняя колонка основания) в строке `y + 2` (под основанием), где `x`, `y` — клетка верхнего левого угла завода; на ней создаётся юнит `TANK` игрока `HUMAN` через `cUnits::unitCreate(objects, infoContext, eventEmitter, <клетка>, TANK, HUMAN, true, false)`; `-1` — `false`. У юнита `bRollingOffFactoryPad = true`, `iRollingOffFactoryPadStructureId` — номер завода. Затем `restorePad` завода получает состояние `factory_pad::PadState` с `phase = Rolling`, `unitType = TANK`, `rollUnitId` — номер танка, `rollStep = 12`, `rollTick = 2`, `waiting = {HARVESTER}`.
5. Возвращается `true`.

**5.5 `tests/ui_audit/ui_audit_part3b_catalog.py`.** В кортеже `BASE_SCENES` после строки, начинающейся с элемента `"game-place-forbidden",` (вторая строка кортежа; она же содержит `"game-group-select"`), вставляется новая строка с тем же отступом: `"game-radar-dish", "game-refinery-harvester", "game-factory-pad",`; `EXPECTED_COUNT = 39` → `EXPECTED_COUNT = 42`. Запись сцены `game_scene(...)` для новых id не меняется: `hover` — `None`, `hud` — ложь, `hd_only` — ложь, готовность — `GAME_READINESS`; это совпадает с кодом из 5.2 (`false` в конце, `kFixedGameFrames`).

**5.6 `tests/ui_audit/ui_audit_part3b_scenes.py`.** В словаре `fixed` функции `check_for` после строки `"game-place-forbidden": check_place({"GOOD", "NEUTRAL", "BAD"}, True),` — строки

```python
        "game-radar-dish": check_nothing_more,
        "game-refinery-harvester": check_nothing_more,
        "game-factory-pad": check_nothing_more,
```

Правила общей проверки `check_common` и каталога, которые новые сцены обязаны выполнять и выполняют без расширения: область `top-panel` и `sidebar` в точных прямоугольниках, область `build-list` внутри боковой панели, клик `top-options` в точном прямоугольнике, нет клика `order-button`, метки только видов из `LABEL_KINDS` (новые сцены меток не пишут), записи мини-карты `minimap` (область и клик) присутствуют, потому что сцены строят базу с Командным постом и питанием. Правило, которое новые сцены нарушили бы без правок 5.5 и 5.6: каталог части 3б требует каждый идентификатор `game-…` в `BASE_SCENES` и совпадения числа с `EXPECTED_COUNT`, а `check_for` бросает `ValueError` для идентификатора без проверки. Число игровых сцен каталога: до правок `39`, после — `42`; общее число сцен `--ui-audit-list` пересчитай до и после (`+3`) и запиши в журнал хода.

**5.7 `tests/ui_audit/ui_audit_saves.py`.** В ветке `scene_id == "save-roundtrip"` после проверки `first_bytes.startswith(b"D2TM_SAVE 3 ")` — строки

```python
                if b"\nFACTORYPADS 2\n" not in first_bytes:
                    errors.append("save-roundtrip: first save has no FACTORYPADS section with two pads")
                if first_bytes.count(b"\nFACTORYPAD ") != 2:
                    errors.append("save-roundtrip: first save does not hold two FACTORYPAD records")
```

Проверка `first_bytes != second_bytes` остаётся.

### 6. Подключение файлов к сборке

- `src/CMakeLists.txt`: сразу после строки `    gameobjects/structures/cStructureFactory.cpp` — строка `    gameobjects/structures/cUnitFactory.cpp`.
- `tests/CMakeLists.txt`: в `TEST_FILES` сразу после строки `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_HdRender.cpp` — шесть строк:
  ```
      ${CMAKE_CURRENT_SOURCE_DIR}/players/test_PlacementRule.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/structures/test_FactoryPad.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/structures/test_FactoryPadEngine.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/structures/test_OutpostDish.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/save/test_FactoryPadSave.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_WorldObjectScale.cpp
  ```
  `TEST_SOURCES` не меняется: все шесть файлов используют только заголовки и уже перечисленные `SaveBody.cpp`, `SaveFileCodec.cpp`.

### 7. Ничего сверх контракта

Других изменений нет: ни переформатирования, ни новых комментариев, ни переноса строк сверх нужного для правки. `src/gameobjects/structures/cOrderProcesser.*`, `cStarPort.cpp`, `cBuildingListUpdater.cpp`, файлы настроек и клавиш (`cOptionsState`, `cKeyBindings`, `Preferences`, `main.cpp`) не трогаются: их правит параллельный шаг П10в.

## Тесты

Тесты пишутся в шаге 1 плана; формат — Catch2 (`#include <catch2/catch_test_macros.hpp>`, образец — `tests/structures/test_StarportOrders.cpp`). Имя каждого `TEST_CASE` начинается с `P8A ` и уникально; у каждого случая тег `[P8A]` и тег файла из списка ниже. Тесты не линкуют классы игры: только заголовки `PlacementRule.hpp`, `FactoryPad.hpp`, `OutpostDish.hpp`, `WorldObjectScale.hpp`, `SaveBody.hpp`, `SaveFileCodec.hpp`, `SaveGameManager.hpp`. В шаге 2 тесты собираются и краснеют до правок шагов 3 и 4: заголовков нет.

Тесты форка — не Catch2 (`int main()`); каждый перенесён так: функция проверки форка → один `TEST_CASE` с тем же смыслом, `check(<условие>, <сообщение>)` и `require(...)` форка → `INFO(<сообщение>); CHECK(<условие>);` (в цикле — `REQUIRE`, если после провала продолжать нельзя). Число проверок («assertions» Catch2) в каждом файле не меньше порога из таблицы; пороги — число проверок форка в тексте файла, увеличенное там, где случай выполняется в цикле.

| файл | тег файла | случаев | не меньше проверок | источник |
|---|---|---|---|---|
| `tests/players/test_PlacementRule.cpp` | `[P8A-placement]` | 5 | 41 | `PlacementRuleTests.cpp` (16 проверок) |
| `tests/structures/test_FactoryPad.cpp` | `[P8A-pad]` | 12 | 47 | `FactoryPadTests.cpp` (47 проверок) |
| `tests/structures/test_FactoryPadEngine.cpp` | `[P8A-padengine]` | 8 | 23 | `FactoryPadEngineTests.cpp` (часть из 87 проверок, таблица ниже) |
| `tests/structures/test_OutpostDish.cpp` | `[P8A-dish]` | 1 | 34 | `OutpostFrameTests.cpp` (5 проверок, одна в цикле на 32 интервала) |
| `tests/save/test_FactoryPadSave.cpp` | `[P8A-padsave]` | 4 | 23 | `FactoryPadSaveTests.cpp` (23 проверки) |
| `tests/utils/test_WorldObjectScale.cpp` | `[P8A-scale]` | 1 | 16 | `WorldObjectScaleTests.cpp` (16 проверок) |
| `tests/save/test_SaveBody.cpp` (дописывается) | `[P8A-save]` | 1 | 4 | решение шага: сохранение площадок |

Всего новых случаев — 32. Существующие случаи `tests/save/test_SaveBody.cpp` и остальных файлов не меняются; новый случай дописывается в конец `test_SaveBody.cpp`.

### T1. `tests/players/test_PlacementRule.cpp` — подключает `gameobjects/players/PlacementRule.hpp`

Грани клетки задаются полями `placement_rule::CellFacts`; типы — `WINDTRAP`, `SLAB1`, `SLAB4` (`include/definitions.h`). Случаи:

1. `P8A placement rule terrain decides ordinary buildings and SLAB1` — `WINDTRAP` на `validTerrain = false` (песок, гора, пряность) — `allowed()` ложь (3 проверки); на `validTerrain = true` (скала, плита) — истина (2 проверки); `SLAB1` на `validTerrain = false` — ложь; `SLAB4` на `validTerrain = false` — истина.
2. `P8A placement rule matrix of 21 combinations` — для каждого из пяти рельефов (песок `false`, скала `true`, плита `true`, гора `false`, пряность `false` по `validTerrain`) и каждого из типов `WINDTRAP`, `SLAB1`, `SLAB4` ожидается `allowed()`: песок {ложь, ложь, истина}, скала {истина, истина, истина}, плита {истина, истина, истина}, гора {ложь, ложь, истина}, пряность {ложь, ложь, истина}; затем на скале (`validTerrain = true`) для занятой клетки строением (`structurePresent = true`) — {ложь, ложь, истина}, для клетки с живым юнитом (`livingUnitPresent = true`) — {ложь, ложь, истина}. Всего 21 проверка.
3. `P8A placement rule structures and units block ordinary buildings but not SLAB4` — `judgeCell(WINDTRAP, {structurePresent = true})`: `structureBlocks` истина, `allowed()` ложь; то же для `SLAB4`: `allowed()` истина; `judgeCell(WINDTRAP, {livingUnitPresent = true})`: `unitBlocks` истина; `judgeCell(SLAB1, {livingUnitPresent = true})`: `unitBlocks` истина (поведение апстрима, пункт 1.5; ответ ведущего может изменить только эту проверку).
4. `P8A placement rule out of bounds` — `withinBoundaries = false`: `outOfBounds` истина и `allowed()` ложь для `WINDTRAP`, `SLAB1` и `SLAB4` (3 проверки); при `withinBoundaries = false` и `structurePresent = true` для `WINDTRAP` поле `structureBlocks` ложно (1 проверка).
5. `P8A placement rule build anchor` — `isBuildAnchor`: своё строение — истина; чужое строение при `wallOrSlab = true` — ложь (плита под чужим зданием не якорь, пункт 1.6); стена или плита без строения — истина; ничего — ложь; своё строение вместе с `wallOrSlab = true` — истина.

### T2. `tests/structures/test_FactoryPad.cpp` — подключает `gameobjects/structures/FactoryPad.hpp`

Двенадцать случаев — по одному на каждую функцию `FORK1:tests/FactoryPadTests.cpp` (строки 31–284), с теми же данными и ожиданиями: `padCenterIsOnTheRightColumn`, `exitCellsFollowTheDocumentedOrder`, `exitSelectionSkipsOutsideAndOccupiedCells`, `rollMovesInAStraightLineWithoutJumps`, `padIsBusyUntilTheRollEnds`, `queueKeepsEveryReadyUnit`, `factoryChoiceFollowsThePrimaryRule`, `blockedExitCallsACarryallAfterThreeSeconds`, `aFreeExitStartsTheRollAndResetsTheCounter`, `rollAdvancesByTheMovementSpeed`, `stateSurvivesWritingAndReading`, `damagedStateIsRejected`. Имя случая — `P8A pad <имя функции форка словами>`; вспомогательная функция `describe` форка переносится в анонимное пространство имён файла.

### T3. `tests/save/test_FactoryPadSave.cpp` — подключает `save/SaveBody.hpp`, `save/SaveFileCodec.hpp`, `save/SaveGameManager.hpp`, `data/gfxdata.h`

Четыре случая — по одному на каждую функцию `FORK1:tests/FactoryPadSaveTests.cpp` (строки 99–216): `padsSurviveWritingAndReading`, `saveWithoutPadsIsReadable`, `damagedPadsAreRejected`, `truncatedAndOldBodiesAreRejected`; вспомогательные функции форка (`factoryState`, `unitState`, `baseSnapshot`, `standingPad`, `rollingPad`, `samePad`, `parses`) переносятся в анонимное пространство имён. Замены: `SaveSnapshot`, `StructureState`, `UnitState`, `serializeBody`, `deserializeBody` — из `namespace save_game_detail` порта; `MAX_UNITTYPES` → `save_game_detail::UnitTypeCount`; `MAX_UNITS` → `save_game_detail::UnitSlots`; `save_file::decode(…, SaveGameManager::FormatVersion, 16 * 1024 * 1024)` → `save_file::decode(…, SaveGameManager::FormatVersion, save_game_detail::MaximumSaveBytes)`. Если заготовка `baseSnapshot()` не проходит разбор порта, заполнение игроков и ячеек копируется из `sample()` в `tests/save/test_SaveBody.cpp`; ожидания случаев не меняются.

Случай `saveWithoutPadsIsReadable` — как в форке: снимок без площадок записывается `serializeBody` (тело содержит `FACTORYPADS 0`) и читается `deserializeBody` с пустым `factoryPads`. Файлы версии 3, записанные сборкой шага П8 без раздела `FACTORYPADS`, не читаются: релизов между шагами не было.

### T4. `tests/utils/test_WorldObjectScale.cpp` — подключает `utils/WorldObjectScale.hpp`

Один случай `P8A world object scale refinery harvester layout`; 16 проверок значений — по четыре на раскладку:

| вызов `refineryHarvesterLayout(x, y, ширина, высота)` | `x` | `y` | `width` | `height` |
|---|---|---|---|---|
| `(0, 0, 96, 64)` | 32 | 1 | 80 | 52 |
| `(10, 20, 106, 70)` | 46 | 21 | 88 | 57 |
| `(0, 0, 120, 80)` | 40 | 1 | 100 | 65 |
| `(0, 0, 144, 96)` | 49 | 1 | 120 | 78 |

### T5. `tests/structures/test_OutpostDish.cpp` — подключает `gameobjects/structures/OutpostDish.hpp`

Один случай `P8A outpost dish 32 frames with 55 calls per frame`: `int frame = 0; int timer = 0;` и до 4000 вызовов `outpost_dish::advance(frame, timer)`; при каждой смене `frame` значение записывается в список, а число вызовов с прошлой смены — в список интервалов (для второй и следующих смен); вызовы прекращаются, когда в списке 33 кадра. Проверки: список кадров равен `1, 2, …, 31, 0, 1` (одна проверка); список интервалов содержит 32 значения (одна проверка); каждый интервал равен 55 (проверка на каждый интервал, 32 проверки).

### T6. `tests/structures/test_FactoryPadEngine.cpp` — подключает `gameobjects/structures/FactoryPad.hpp`

Восемь случаев на чистой логике. Размер клетки — 32 × 32.

1. `P8A pad engine unit center sits on the pad center` — `factory_pad::padOrigin(480, 320, 2, 2, 32, 32)` равен `{512, 335}`, `padOrigin(480, 320, 3, 2, 32, 32)` равен `{542, 334}` (по две проверки `x` и `y`; всего 4).
2. `P8A pad engine exit cell is the first free cell and moves on when blocked` — `chooseExitCell(20, 20, 2, 2, resolve, isFree)` с `resolve(x, y) = y * 64 + x` и свободными клетками возвращает первую клетку `exitCandidates(20, 20, 2, 2)`; когда первая занята, возвращает вторую (2 проверки).
3. `P8A pad engine roll starts at the pad center and takes more than 20 ticks` — `from = padOrigin(480, 320, 2, 2, 32, 32)`, `to = {21 * 32, 22 * 32}`: `rollPosition(from, to, 0)` равно `from`; `rollSteps(from, to) * 4 > 20` (2 проверки).
4. `P8A pad engine roll duration follows the movement speed` — для тех же `from` и `to` цикл `tickRoll(pad, 4, steps)` до `done`: число `advanced` равно `rollSteps(from, to)`, число вызовов лежит в пределах от `steps * 4 - 4` до `steps * 4 + 4` включительно (2 проверки).
5. `P8A pad engine roll position never jumps` — для шагов `1…steps` соседние `rollPosition` отличаются не больше чем на 1 по каждой оси и не уменьшаются (2 проверки в цикле).
6. `P8A pad engine flicker steps through frames 0 to 6 once per 41 calls` — `int frame = 0; int timer = 0;`, 656 вызовов `advanceFlicker(frame, timer, true)`: после вызова номер `tick` (от 1) `frame == (tick / 41) % 7` (одна проверка в цикле); затем `advanceFlicker(frame, timer, false)` — `frame == 0` и `timer == 0` (2 проверки).
7. `P8A pad engine flicker goes only to the chosen factory and only for the building type` — два завода с номерами 3 и 5, основной 5, обе площадки свободны: `chooseFactory({{3, true}, {5, true}}, 5) == 5`; за 82 вызова `advanceFlicker` с `active = (chosen == id)` кадр завода 3 остаётся 0, кадр завода 5 равен 2 (2 проверки); при `active = false` для обоих (юнит другого типа) оба кадра после 82 вызовов равны 0 (2 проверки).
8. `P8A pad engine flicker follows the free pad and goes on under a standing unit` — завод 5 основной; `offer(pad5, 7)` занимает его площадку, `chooseFactory({{3, true}, {5, false}}, 5) == 3`; за 82 вызова кадр завода 5 (`active = false`) равен 0, кадр завода 3 равен 2 (3 проверки); для завода, активного независимо от площадки, после 123 вызовов кадр равен 3 (1 проверка).

### T7. Дописываемый случай в `tests/save/test_SaveBody.cpp`

В конец файла добавляется случай `P8A save body keeps factory pads` с тегами `[P8A][P8A-save]`: `auto save = sample();`, у `save.structures[1]` тип меняется на `LIGHTFACTORY` (его `oldId` равен 3, игрок 1); в `save.factoryPads` добавляется `save_game_detail::FactoryPadSave` с `structureId = 3`, `pad.phase = factory_pad::Phase::Standing`, `pad.unitType = 4`, `pad.waiting = {5, 6}`. Проверки: `deserializeBody(serializeBody(save), restored, error)` истинно; `restored.factoryPads.size() == 1`; `restored.factoryPads[0].pad.waiting == std::vector<int>({5, 6})`; `serializeBody(restored) == serializeBody(save)`.

### Таблица «проверка форка → случай»

| проверка форка | число проверок форка | случай Catch2 |
|---|---|---|
| `PlacementRuleTests.cpp`: `checkTerrainRule` | 2 | T1 случай 1 |
| `checkSlab4OverStructure` | 1 | T1 случай 3 |
| `checkSlab1OverUnit` | 1 | T1 случаи 2 и 3 (ожидание меняется по пункту 1.5) |
| `checkPlacementDecisionMatrix` (21 сочетание) | 5 на сочетание через `assertSharedDecision` | T1 случай 2: решение правила; согласие подсветки, щелчка и размещения — проверка 5 (строки поиска) и сцены `game-place-allowed`, `game-place-forbidden` |
| `checkAiPlacementWithoutBuilderConnection` | 4 | T1 случай 5 (нет якоря — отказ); ветка ИИ — проверка 5 (строка поиска в `placeItem`) |
| `WorldObjectScaleTests.cpp` | 16 | T4 |
| `OutpostFrameTests.cpp` | 5 | T5 |
| `FactoryPadTests.cpp`, 12 функций | 47 | T2, 12 случаев |
| `FactoryPadSaveTests.cpp`, 4 функции | 23 | T3, 4 случая; поля юнита `bRollingOffFactoryPad` — раздел `FACTORYPADS` и круговая проверка `ui_audit_saves.py` |
| `FactoryPadEngineTests.cpp`: `checkPadAppearance` | 9 | T6 случай 1 (2 проверки центра); 7 проверок рисования — сцена `game-factory-pad` |
| `itemTwoRoll` | 8 | T6 случаи 2 и 3 (выбор клетки, начало, длина пути); 5 проверок живого мира — нет Catch2 |
| `itemTwoRollDetails` | 12 | T6 случаи 4 и 5 (4 проверки); 8 проверок живого мира — нет Catch2 |
| `itemTwoAi`, `itemTwoStaleRollerAlias` | 3 + 3 | нет Catch2 (нужен живой мир) |
| `itemThree`, `itemThreeBarracksUnchanged`, `itemThreeNoReinforcement` | 4 + 2 + 1 | выбор завода и очередь — T2 (`factoryChoiceFollowsThePrimaryRule`, `padIsBusyUntilTheRollEnds`); остальное нет Catch2 |
| `itemFourOwnCarryall` (2 вызова), `itemFourNewCarryall`, `itemFourReleased`, `itemFourReleasedCarryallDestinations`, `itemFourForeignCarryall` | 9 + 5 + 4 + 6 + 3 | таймер трёх секунд — T2 (`blockedExitCallsACarryallAfterThreeSeconds`); полёт Карриера нет Catch2 |
| `itemFive` | 4 | нет Catch2 (анимация выпуска двух заводов) |
| `itemSevenSingleFactory`, `itemSevenWrongType`, `itemSevenChosenFactory`, `itemSevenUnderStandingUnit` | 3 + 2 + 5 + 2 | T6 случаи 6, 7, 8 |
| `itemSevenDrawsTheFrame` | 2 | нет Catch2; кадр мигания рисуется общим путём `drawWithShadow`, строки не меняются |

Из 87 проверок `FactoryPadEngineTests.cpp` 21 заменены случаями T6, остальные 66 требуют живого мира (мир, юниты, Карриеры, рисование) и в Catch2 порта невыполнимы без линковки классов игры; вместо них — сцены и снимки (пункт 5 контракта), круговая проверка сохранения и вопрос ведущему (`QUESTIONS-P8A.md`, вопрос 4).

## PLAN-P8A

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tests/players/test_PlacementRule.cpp`, `tests/structures/test_FactoryPad.cpp`, `tests/structures/test_FactoryPadEngine.cpp`, `tests/structures/test_OutpostDish.cpp`, `tests/save/test_FactoryPadSave.cpp`, `tests/utils/test_WorldObjectScale.cpp`, `tests/save/test_SaveBody.cpp`, `tests/CMakeLists.txt` | Раздел «Тесты» и пункт 6 контракта (`tests/CMakeLists.txt`). | помощник A |
| 2 | — | Красный прогон: команда сборки проверки 1, у которой вместо `.tmp/p8a/build.log` стоит `.tmp/p8a/red-build.log`, — `exit` не `0`, в логе есть строка с `error` и с одним из имён `PlacementRule.hpp`, `FactoryPad.hpp`, `OutpostDish.hpp`, `WorldObjectScale.hpp`. Запускается до того, как шаги 3 и 4 записали эти четыре файла. | помощник A |
| 3 | `src/gameobjects/players/PlacementRule.hpp`, `src/gameobjects/players/cPlayer.h`, `src/gameobjects/players/cPlayer.cpp`, `src/controls/mousestates/cMousePlaceState.h`, `src/controls/mousestates/cMousePlaceState.cpp`, `src/drawers/cPlaceItDrawer.cpp`, `src/utils/WorldObjectScale.hpp`, `src/gameobjects/structures/OutpostDish.hpp`, `src/gameobjects/structures/cOutPost.cpp`, `src/drawers/cStructureDrawer.h`, `src/drawers/cStructureDrawer.cpp` | Пункты 1, 2, 3.11 и 4 контракта. | помощник B |
| 4 | `src/gameobjects/structures/FactoryPad.hpp`, `src/gameobjects/structures/cUnitFactory.h`, `src/gameobjects/structures/cUnitFactory.cpp`, `src/gameobjects/structures/cAbstractStructure.h`, `src/gameobjects/structures/cAbstractStructure.cpp`, `src/gameobjects/structures/cLightFactory.h`, `src/gameobjects/structures/cLightFactory.cpp`, `src/gameobjects/structures/cHeavyFactory.h`, `src/gameobjects/structures/cHeavyFactory.cpp`, `src/gameobjects/units/cUnit.h`, `src/gameobjects/units/cUnit.cpp`, `src/drawers/cUnitDrawer.h`, `src/drawers/cUnitDrawer.cpp`, `src/utils/cStructureUtils.h`, `src/utils/cStructureUtils.cpp`, `src/building/cItemBuilder.h`, `src/building/cItemBuilder.cpp`, `src/save/SaveSnapshot.hpp`, `src/save/SaveBody.cpp`, `src/save/SaveGameManager.cpp`, `src/CMakeLists.txt` | Пункты 3.1–3.10, 3.12, 3.13 контракта и строка `src/CMakeLists.txt` пункта 6. | помощник C |
| 5 | `src/debug/UiAudit.hpp`, `src/debug/UiAuditScenes.cpp`, `src/debug/UiAuditAccess.cpp`, `tests/ui_audit/ui_audit_part3b_catalog.py`, `tests/ui_audit/ui_audit_part3b_scenes.py`, `tests/ui_audit/ui_audit_saves.py` | Пункт 5 контракта. | помощник D |
| 6 | — | Проверки раздела «Проверки» по порядку; снимки сцен. | помощник A |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p8a`. Каждая команда, которая запускает собранные файлы, получает `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib`. Сверки «строка есть в файлах» — `git grep --untracked` или `grep -r`: исполнитель не коммитит, новые файлы не в индексе. Команды `rm -f` и `rm -rf` песочница отклоняет: удалить папку — `rm -r`, обнулить файл — `: > файл`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P8A-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p8a && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p8a/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345; строк `P8A ` со статусом `Passed` в этом `ctest.log` — ровно 32.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает.
2. **Число проверок Catch2 по тегам.** Двоичный файл тестов: `TESTS=$(find .tmp/out -name d2tm_tests -type f | head -1)`. Для каждой пары `<тег> <случаев> <порог>` из списка — `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib $TESTS "<тег>"`: вывод содержит `All tests passed (<A> assertions in <случаев> test cases)` с `<A>` не меньше порога. Пары: `[P8A-placement] 5 41`, `[P8A-pad] 12 47`, `[P8A-padengine] 8 23`, `[P8A-dish] 1 34`, `[P8A-padsave] 4 23`, `[P8A-scale] 1 16`, `[P8A-save] 1 4`.
3. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -F -f .tmp/p8a/changed-paths.txt` — пустой вывод. Файл `.tmp/p8a/changed-paths.txt` — пути файлов `.cpp`, `.hpp` и `.h` из шагов 1, 3, 4 и 5 плана, по одному на строку.
4. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`.
5. **Сверки состава.**
   - `git grep -n --untracked 'canPlaceBuildingListItemAt' -- src | wc -l` — 6 (объявление, определение, `placeItem`, две строки `cMousePlaceState.cpp`, одна строка `cPlaceItDrawer.cpp`).
   - Число строк `canPlaceStructureAt` в `src/gameobjects/players/cPlayer.cpp` равно числу в `git show d95953ef9:src/gameobjects/players/cPlayer.cpp | grep -c canPlaceStructureAt` (ветка ИИ в `placeItem` остаётся).
   - `git grep -n --untracked 'SCANWIDTH' -- src | wc -l` — 0.
   - `git grep -n --untracked -E 'global_map|renderDrawer|SDL2/|d2tmc.h' -- src/gameobjects/structures/cUnitFactory.cpp src/gameobjects/structures/FactoryPad.hpp src/utils/WorldObjectScale.hpp | wc -l` — 0.
   - `cmp <(git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp) src/utils/WorldObjectScale.hpp` и `cmp <(git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cUnitFactory.h) src/gameobjects/structures/cUnitFactory.h` — код 0.
   - `diff <(git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/FactoryPad.hpp) src/gameobjects/structures/FactoryPad.hpp | grep -c '^<'` — 0 (в файле только добавленные строки).
   - `grep -c 'FACTORYPADS' src/save/SaveBody.cpp` — 2; `grep -n 'FormatVersion = ' src/save/SaveGameManager.hpp` — `FormatVersion = 3`.
   - `grep -P '^sdl_data_hd4.dat\t26\tBUILD_RADAR\tPNG\t256\t8192\t' tests/data/hd4_packs_expected.tsv | wc -l` — 1 (данные тарелки уже в паке).
   - `git grep -n --untracked 'outpost_dish::advance' -- src | wc -l` — 1.
6. **Скрипты режима отладки интерфейса.**
   - Скрипты: `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_part2_catalog.py`, `ui_audit_part3a_catalog.py`, `ui_audit_part3b_catalog.py`, `ui_audit_part3b_scenes.py`, `ui_audit_part3c_catalog.py`, `ui_audit_part3c_scenes.py`, `ui_audit_saves.py`, `ui_audit_language.py`, `ui_audit_translation.py`.
   - Команда для каждого `<скрипт>`: `mkdir -p .tmp/p8a/tmp && TMPDIR=$PWD/.tmp/p8a/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p8a/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
   - Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал. Каждая команда сама ограничена `timeout 1800`; жди, пока она вернёт код выхода. `ui_audit_part3b_scenes.py` и `ui_audit_translation.py` идут по несколько минут — это норма.
   - После проверки — `rm -r tests/ui_audit/__pycache__`, если эта папка появилась.
7. **Снимки сцен для ведущего.** Для каждой сцены `game-radar-dish`, `game-refinery-harvester`, `game-factory-pad`: `mkdir -p .tmp/p8a/snap .tmp/p8a/xdg && (cd .tmp/out/run/bin && SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=$OLDPWD/.tmp/p8a/xdg LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 600 ./d2tm -windowed -screenWidth 1024 -screenHeight 768 --ui-audit-scene <сцена> --ui-audit-out $OLDPWD/.tmp/p8a/snap > $OLDPWD/.tmp/p8a/snap-<сцена>.log 2>&1; echo exit=$?)` — `exit=0`; файл `.tmp/p8a/snap/<сцена>.png` существует; `sha256sum .tmp/p8a/snap/*.png` — три строки. Оценку вида исполнитель не даёт.
8. `git -c lfs.storage=$PWD/.tmp/p8a/lfs status --short` — изменённые (` M`) пути — только пути шагов 1, 3, 4 и 5 плана; новые (`??`) — только `src/gameobjects/players/PlacementRule.hpp`, `src/utils/WorldObjectScale.hpp`, `src/gameobjects/structures/OutpostDish.hpp`, `src/gameobjects/structures/FactoryPad.hpp`, `src/gameobjects/structures/cUnitFactory.h`, `src/gameobjects/structures/cUnitFactory.cpp`, `tests/players/`, `tests/structures/test_FactoryPad.cpp`, `tests/structures/test_FactoryPadEngine.cpp`, `tests/structures/test_OutpostDish.cpp`, `tests/save/test_FactoryPadSave.cpp`, `tests/utils/test_WorldObjectScale.cpp`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P8A-NN` с выводом и стоп. Ожидания существующих тестов и существующие проверки в `tests/ui_audit/` (кроме правок, названных в пункте 5 контракта) не меняй.

## Сдача

Последнее сообщение — блок `## DONE-P8A | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p8a/progress.md`): строка на каждый шаг плана; число сцен `--ui-audit-list` до и после (из шага 5);
- красный прогон шага 2: строки `.tmp/p8a/red-build.log` с `error` (не больше 30);
- вывод каждой проверки 1–8 с кодами выхода (не больше 40 строк на проверку); строки `P8A ` из `ctest.log`; для проверки 2 — семь строк `All tests passed (…)`;
- пути трёх снимков `.tmp/p8a/snap/*.png` и их `sha256`;
- `git diff --stat` и список для коммитов:
  1. тесты: файлы шага 1;
  2. placement-rule: `src/gameobjects/players/PlacementRule.hpp`, `cPlayer.h`, `cPlayer.cpp`, `src/controls/mousestates/cMousePlaceState.h`, `cMousePlaceState.cpp`, `src/drawers/cPlaceItDrawer.cpp`;
  3. refinery-dock и radar-dish: `src/utils/WorldObjectScale.hpp`, `src/gameobjects/structures/OutpostDish.hpp`, `cOutPost.cpp`, `src/drawers/cStructureDrawer.h`, `cStructureDrawer.cpp` (файл несёт и строку пункта 3.11: в сообщении коммита это названо);
  4. factory-pads: файлы шага 4;
  5. сцены режима отладки и скрипты: файлы шага 5.

  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …`;
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже; обязательно названы: клетки, выбранные `addFactoryPads`; подключения, добавленные сверх названных в контракте;
- раздел «Находки вне задачи» — список;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p8a --size`; у `.tmp/p8a` пометка `оставить — логи проверок и снимки нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаг 1 (помощник A), шаг 3 (помощник B) и шаг 4 (помощник C) — одновременно; помощники B и C не создают файлы `PlacementRule.hpp`, `WorldObjectScale.hpp`, `OutpostDish.hpp`, `FactoryPad.hpp`, пока помощник A не записал в журнал хода строку о конце шага 2.
  4. Шаг 2 (помощник A) — сразу после шага 1.
  5. Шаг 5 (помощник D) — после шагов 3 и 4 (он вызывает `cUnitFactory`).
  6. Шаг 6 (помощник A) — после шагов 2–5.
  7. Сдача и стоп.
- **Параллельно:** шаги 1, 3 и 4 правят разные файлы и идут одновременно; общих файлов у них нет (`cStructureDrawer.cpp` целиком у шага 3, строка пункта 3.11 стоит в нём же). Собирает их вместе проверка 1 шага 6.
- **Помощники:** четыре, `gpt-6-luna` `xhigh`, без вложенных; одновременно — не больше трёх (A, B, C, затем D). Ожидаемое время: помощник A — 90 минут на шаги 1–2 и 90 минут на шаг 6, помощник B — 60 минут, помощник C — 120 минут, помощник D — 60 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено», «Правила переноса», «Сохранить из апстрима» и «Контракт поведения» (помощнику A — только пункты 1–6 «Контракта поведения»: тесты проверяют их; помощнику D — пункты 3 и 5); его шаги плана; помощнику A — раздел «Тесты» и раздел «Проверки»; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p8a/`.
  - Корневая нить раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Остановки:** только на `## DONE-P8A` и на блоках `## Q-P8A-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P8A-NN` и стоп.
- **Рамка правок:** файлы шагов 1, 3, 4 и 5 плана и папка `.tmp/p8a/`. Понадобился другой файл — блок `## Q-P8A-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` и временные папки скриптов; это не правка.
- **Данные LFS:** файлы Git LFS (пак `resources/bin/data/sdl_data_hd4.dat` и прочие) не меняются; задание их не берёт из форка.

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
