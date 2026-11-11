# Сверка разведки P5G3R (Haiku)

Выборка: по 5 фактов из каждого файла, позиции 10, 30, 50, 70, 90 % по числу строк файла (headers.md — 4535, functions.md — 731, names.tsv — 219). Первый подходящий факт строго после позиции. В names.tsv факт — первая запись строки в столбце «объявления в PORT». Сравнение: текст отчёта и вывод команды, без пробелов в начале и конце строки.
Ревизии: acddd297b21ec200c7090dd2f1b73e014e2b74c0 (@acddd29), 9208dcf5a358f40afd95c99480e4e09f781ed566 (@9208dcf). Репозиторий команд: C:/Users/Slaven/Projects/DUNE-p2.

## Факт 1
- Отчёт: headers.md, строка 455 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `class GameContext {`
- Исходник: src/context/GameContext.hpp, строка 30
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/GameContext.hpp | sed -n '30p'`
- Вывод: `class GameContext {`
- Итог: совпало

## Факт 2
- Отчёт: headers.md, строка 1361 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `*/`
- Исходник: src/gameobjects/players/cPlayer.h, строка 445
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.h | sed -n '445p'`
- Вывод: `     */`
- Итог: совпало

## Факт 3
- Отчёт: headers.md, строка 2268 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `* @param iPlayer`
- Исходник: src/gameobjects/map/cMap.h, строка 382
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.h | sed -n '382p'`
- Вывод: `     * @param iPlayer`
- Итог: совпало

## Факт 4
- Отчёт: headers.md, строка 3175 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `return m_queuable;`
- Исходник: src/sidebar/cBuildingListItem.h, строка 157
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/cBuildingListItem.h | sed -n '157p'`
- Вывод: `        return m_queuable;`
- Итог: совпало

## Факт 5
- Отчёт: headers.md, строка 4082 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `int getTotalSpiceCapacityForPlayer(cPlayer *pPlayer);`
- Исходник: src/utils/cStructureUtils.h, строка 60
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/utils/cStructureUtils.h | sed -n '60p'`
- Вывод: `    int getTotalSpiceCapacityForPlayer(cPlayer *pPlayer);`
- Итог: совпало

## Факт 6
- Отчёт: functions.md, строка 74 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `m_sdlDrawer->renderRectFillColor(draw_x, draw_y, (w-1), height_y, static_cast<Uint8>(r),static_cast<Uint8>(g),32,255);`
- Исходник: src/drawers/cStructureDrawer.cpp, строка 506
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cStructureDrawer.cpp | sed -n '506p'`
- Вывод: `    m_sdlDrawer->renderRectFillColor(draw_x, draw_y, (w-1), height_y, static_cast<Uint8>(r),static_cast<Uint8>(g),32,255);`
- Итог: совпало

## Факт 7
- Отчёт: functions.md, строка 223 (`git grep -n`, путь в строке)
- Отчёт, текст: `void cSideBarDrawer::draw()`
- Исходник: src/drawers/cSideBarDrawer.cpp, строка 98
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cSideBarDrawer.cpp | sed -n '98p'`
- Вывод: `void cSideBarDrawer::draw()`
- Итог: совпало

## Факт 8
- Отчёт: functions.md, строка 373 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `2001 - 2022 (c) code by Stefan Hendriks`
- Исходник: src/cGame_logic.cpp, строка 9
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '9p'`
- Вывод: `  2001 - 2022 (c) code by Stefan Hendriks`
- Итог: совпало

## Факт 9
- Отчёт: functions.md, строка 513 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `int max = getUnitInfo().credit_capacity;`
- Исходник: src/gameobjects/units/cUnit.cpp, строка 578
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | sed -n '578p'`
- Вывод: `    int max = getUnitInfo().credit_capacity;`
- Итог: совпало

## Факт 10
- Отчёт: functions.md, строка 658 (`nl -ba`, путь из заголовка `###`)
- Отчёт, текст: `#include "data/gfxinter.h"`
- Исходник: src/managers/cDrawManager.cpp, строка 7
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '7p'`
- Вывод: `#include "data/gfxinter.h"`
- Итог: совпало

## Факт 11
- Отчёт: names.tsv, строка 22, первая запись
- Отчёт, текст: `bool canDeployUnitTypeAtCell(int iCell, int iUnitType);`
- Исходник: src/gameobjects/map/cMap.h, строка 69
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.h | sed -n '69p'`
- Вывод: `    bool canDeployUnitTypeAtCell(int iCell, int iUnitType);`
- Итог: совпало

## Факт 12
- Отчёт: names.tsv, строка 69, первая запись
- Отчёт, текст: `* Returns type of unit (ie QUAD, TANK, etc)`
- Исходник: src/gameobjects/units/cUnit.h, строка 436
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/units/cUnit.h | sed -n '436p'`
- Вывод: `     * Returns type of unit (ie QUAD, TANK, etc)`
- Итог: совпало

## Факт 13
- Отчёт: names.tsv, строка 110, первая запись
- Отчёт, текст: `float m_moveY;`
- Исходник: src/gameobjects/map/cMapCamera.h, строка 225
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMapCamera.h | sed -n '225p'`
- Вывод: `    float m_moveY;`
- Итог: совпало

## Факт 14
- Отчёт: names.tsv, строка 154, первая запись
- Отчёт, текст: `GAMESTATE_PLAYING,                      // #define GAME_PLAYING      2      // playing the actual game`
- Исходник: src/gamestates/cGameState.h, строка 38
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGameState.h | sed -n '38p'`
- Вывод: `    GAMESTATE_PLAYING,                      // #define GAME_PLAYING      2      // playing the actual game`
- Итог: совпало

## Факт 15
- Отчёт: names.tsv, строка 198, первая запись
- Отчёт, текст: `void setContextMouseState(eMouseState newState);`
- Исходник: src/gameobjects/players/cPlayer.h, строка 225
- Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.h | sed -n '225p'`
- Вывод: `    void setContextMouseState(eMouseState newState);`
- Итог: совпало

Итог: 15 из 15 совпало

## Пункт 4 — drawers.md (Haiku)

Выборка: 953 строки отчёта; позиции 10/30/50/70/90 % → строки отчёта 96, 286, 480, 669, 858 (первые строки вида `<номер>\t<текст>` с непустым текстом от позиции). Путь — из ближайшего заголовка `###` выше строки.

- Факт 1 — строка отчёта 96, `src/gamestates/cWinLoseState.h`, строка исходника 46.
  - Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.h | sed -n '46p'`
  - Вывод: `private:`
  - Строка отчёта: `private:`. Итог: совпало.
- Факт 2 — строка отчёта 286, `src/drawers/cUnitDrawer.cpp`, строка исходника 93.
  - Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.cpp | sed -n '93p'`
  - Вывод: `    }`
  - Строка отчёта: `    }` (без пробелов по краям: `}`). Итог: совпало.
- Факт 3 — строка отчёта 480, `src/gamestates/cWinLoseState.cpp`, строка исходника 127.
  - Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | sed -n '127p'`
  - Вывод: `eGameStateType cWinLoseState::getType()`
  - Строка отчёта: `eGameStateType cWinLoseState::getType()`. Итог: совпало.
- Факт 4 — строка отчёта 669, `src/managers/cDrawManager.cpp`, строка исходника 253.
  - Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | sed -n '253p'`
  - Вывод: `void cDrawManager::drawSidebar()`
  - Строка отчёта: `void cDrawManager::drawSidebar()`. Итог: совпало.
- Факт 5 — строка отчёта 858, `src/gamestates/cGamePlaying.cpp`, строка исходника 151.
  - Команда: `git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp | sed -n '151p'`
  - Вывод: `    for (cPlayer* pPlayer : m_objects->getPlayers()) {`
  - Строка отчёта: `    for (cPlayer* pPlayer : m_objects->getPlayers()) {`. Итог: совпало.

Итог пункта 4: 5 из 5 совпало
