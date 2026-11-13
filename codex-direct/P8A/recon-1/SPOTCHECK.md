# Сверка разведки П8а-1 (Haiku)

Источник фактов: `RECON.md` и таблицы `placement.tsv`, `port-placement.tsv`, `refinery.tsv`, `radar.tsv`, `tests.tsv` в этой папке. Все команды выполнены в `C:/Users/Slaven/Projects/DUNE` через `git -C`. Ревизии подставлены полными: FORK1 = `9208dcf5a358f40afd95c99480e4e09f781ed566`, PORT = `832c953a94a632d57872349013f7ed1a37434715`, UP1 = `d06f2fcd2a347182c3774fb96e9a85570405c489`, `c655ceb6` = `c655ceb600abc910beef8c926f48839c5d1d2534` (полный хэш из `RECON.md`, строка 499).

## Размещение (placement.tsv)

### 1. placement.tsv, строка 3
- Утверждение: `cPlayer.cpp@9208dcf:1516` — для AI остаётся прежняя `canPlaceStructureAt`, для человека используется общий validator.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/player/cPlayer.cpp | sed -n '1516p'`
- Вывод:
```
    const bool isHumanPlayer = isHuman();
```
- Итог: не совпало. Таблица называет в строке 1516 вызов `canPlaceStructureAt` и общий validator; в выводе есть только `isHuman()`, ни `canPlaceStructureAt`, ни `canPlaceBuildingListItemAt` в строке нет. Для справки: в выводе `git grep 'canPlaceBuildingListItemAt'` из `RECON.md`, строка 1998, та же ревизия, вызов стоит в `src/player/cPlayer.cpp:1518`.

### 2. placement.tsv, строка 6
- Утверждение: `cPlayer::canPlaceBuildingListItemAt` определён в `cPlayer.cpp@9208dcf:2012` как единая проверка.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/player/cPlayer.cpp | sed -n '2012p'`
- Вывод:
```
s_PlaceResult cPlayer::canPlaceBuildingListItemAt(int iCell, int iStructureType)
```
- Итог: совпало.

### 3. placement.tsv, строка 10
- Утверждение: `cMousePlaceState.cpp@9208dcf:64` — текст о достигнутом лимите построек.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMousePlaceState.cpp | sed -n '64p'`
- Вывод:
```
                "Cannot place another structure: the structure limit has been reached.",
```
- Итог: совпало (строка содержит английский вариант сообщения о лимите; русский вариант в таблице на этой же строке не назван).

## Порт размещения (port-placement.tsv)

### 4. port-placement.tsv, строка 3
- Утверждение: `cMousePlaceState.cpp@832c953:101-103` — отклоняет отрицательную клетку.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp | sed -n '101,103p'`
- Вывод:
```
    if (mouseCell < 0) {
        return false;
    }
```
- Итог: совпало.

### 5. port-placement.tsv, строка 16
- Утверждение: `cPlayer.cpp@832c953:2012-2016` — любое существующее строение считается blocker-ом.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp | sed -n '2012,2016p'`
- Вывод:
```
            // another structure found on this location, "blocked"
            int structureId = m_objects->getMap()->getCellIdStructuresLayer(cll);
            if (structureId > -1) {
                result.structureIds.insert(structureId);
            }
```
- Итог: совпало.

### 6. port-placement.tsv, строка 47
- Утверждение: `cPlaceItDrawer.cpp@d06f2fc:128` — расчёт предпросмотра; `drawStructureIdAtMousePos` получает `mouseCell`.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/drawers/cPlaceItDrawer.cpp | sed -n '128p'`
- Вывод:
```
        }
```
- Итог: не совпало. Таблица называет в строке 128 вызов `drawStructureIdAtMousePos` с `mouseCell`; в выводе только закрывающая скобка блока, ни имени функции, ни `mouseCell` в строке нет.

## Стыковка у НПЗ (refinery.tsv)

### 7. refinery.tsv, строка 2
- Утверждение: `WorldObjectScale.hpp@c655ceb6:26-27` — смещения сдвинуты на 26.75 и 17.375.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show c655ceb600abc910beef8c926f48839c5d1d2534:src/utils/WorldObjectScale.hpp | sed -n '26,27p'`
- Вывод:
```
    constexpr float logicalOffsetX = 26.75F;
    constexpr float logicalOffsetY = 17.375F;
```
- Итог: совпало.

### 8. refinery.tsv, строка 14
- Утверждение: `cStructureDrawer.cpp@9208dcf:880-885` — передаётся визуальный прямоугольник НПЗ в `refineryHarvesterLayout`.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp | sed -n '880,885p'`
- Вывод:
```
    const WorldObjectLayout harvesterVisual = refineryHarvesterLayout(
        refineryVisual.getX(),
        refineryVisual.getY(),
        refineryVisual.getWidth(),
        refineryVisual.getHeight()
    );
```
- Итог: совпало.

### 9. refinery.tsv, строка 23
- Утверждение: `cAbstractStructure.cpp@832c953:809-843` — `unitLeavesStructure` выбирает свободную клетку вокруг здания и передаёт её в `setCell`.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cAbstractStructure.cpp | sed -n '809,843p'`
- Вывод (первые 12 из 35 строк; совпадения в строках 809–815):
```
void cAbstractStructure::unitLeavesStructure()
{
    cUnit *unitToLeave = m_objects->getUnit(iUnitIDWithinStructure);
    int iNewCell = getNonOccupiedCellAroundStructure();

    if (iNewCell > -1) {
        unitToLeave->setCell(iNewCell);
    }
    else {
        Logger::warn(COMP_STRUCTURES, "cAbstractStructure", "Could not find space for this unit");
        // TODO: Pick up by carry-all!?
    }

    // done & restore unit
```
- Итог: совпало.

## Радар (radar.tsv)

### 10. radar.tsv, строка 2
- Утверждение: `cOutPost.cpp@9208dcf:15-32` — при `TIMER_flag > 54` увеличивает `iFrame`, циклически выбирает 0…31.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cOutPost.cpp | sed -n '15,32p'`
- Вывод (полный вывод 18 строк; показаны строки 16–27, где лежат оба совпадения — строка 24 и строка 27):
```
{
    // last but not least, think like our abstraction
    cAbstractStructure::thinkFast();

    // this is not really flag animation anymore, but just base animation (ie, turning around of
    // dish on outpost)
    TIMER_flag++;

    if (TIMER_flag > 54) {
        iFrame++;

        if (iFrame > 31) {
```
- Итог: совпало.

### 11. radar.tsv, строка 8
- Утверждение: `cInfoContextCreator.cpp@832c953:1546` — загружает изображение тарелки из записи пака через `getSurface`.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp | sed -n '1546p'`
- Вывод:
```
    structureInfos[RADAR].bmp = m_gfxdata->getSurface(BUILD_RADAR);
```
- Итог: совпало.

### 12. radar.tsv, строка 15
- Утверждение: `OutpostFrameTests.cpp@9208dcf:56` — проверяет по 55 вызовов `thinkFast` в каждом интервале.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/OutpostFrameTests.cpp | sed -n '56p'`
- Вывод:
```
        if (callsBetweenChanges[interval] != 55) {
```
- Итог: совпало.

## Тесты (tests.tsv)

### 13. tests.tsv, строка 3
- Утверждение: `PlacementRuleTests.cpp@9208dcf:91` — общая функция игрока возвращает ожидаемый результат.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/PlacementRuleTests.cpp | sed -n '91p'`
- Вывод:
```
    requirePlacement(placement.success == expected, label + ": shared placement rule returned the wrong result");
```
- Итог: совпало. Строка проверяет, что результат общего правила размещения (`placement.success`) равен ожидаемому; имени функции `canPlaceBuildingListItemAt` в самой строке нет, оно в таблице не названо.

### 14. tests.tsv, строка 22
- Утверждение: `WorldObjectScaleTests.cpp@9208dcf:22` — 100%: x ожидается 32.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp | sed -n '22p'`
- Вывод:
```
    passed &= expectEqual("100% x", scale100.x, 32);
```
- Итог: совпало.

### 15. tests.tsv, строка 39
- Утверждение: `OutpostFrameTests.cpp@9208dcf:51` — число интервалов между сменами кадра равно 32.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/OutpostFrameTests.cpp | sed -n '51p'`
- Вывод:
```
    if (callsBetweenChanges.size() != 32) {
```
- Итог: совпало.

Итог: совпало 13 из 15
