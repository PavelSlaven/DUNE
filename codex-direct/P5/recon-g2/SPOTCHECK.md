# Сверка разведки P5G2R (Haiku)

Ревизия: `acddd297b21ec200c7090dd2f1b73e014e2b74c0` (`@acddd29`). Репозиторий сверки: `C:/Users/Slaven/Projects/DUNE-p2`. Команды только чтения (`git show | sed -n`).

Правило выборки: в каждом отчёте строки — это строки вида `<номер>\t<текст>` (nl -ba, путь из ближайшего `###`) и `<ревизия>:<путь>:<номер>:<текст>` (git grep). Пустой текст строки не считается фактом. Позиция — номер строки отчёта; берётся первая подходящая строка с номером не меньше порога (процент от числа строк отчёта).

Отчёты (всего строк / подходящих строк / пороги):
- `files.md`: 1429 строк, подходящих 948, пороги [(10, 142.9), (35, 500.1), (60, 857.4), (85, 1214.7)]
- `functions.md`: 1992 строк, подходящих 1492, пороги [(10, 199.2), (35, 697.2), (60, 1195.2), (85, 1693.2)]
- `names.md`: 575 строк, подходящих 232, пороги [(10, 57.5), (35, 201.2), (60, 345.0), (85, 488.8)]
- `houses.md`: 393 строк, подходящих 86, пороги [(20, 78.6), (50, 196.5), (80, 314.4)]

## Факт 1. files.md, строка отчёта 144 (порог 10 %, позиция 142.9)

- Файл отчёта: `files.md`, строка 144 (вид строки: nl)
- Путь и строка исходника: `src/gamestates/cMainMenuState.h:46`
- Текст строки отчёта:
```
eGameStateType getType() override;
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMainMenuState.h | sed -n '46p'
```
- Вывод:
```
    eGameStateType getType() override;
```
- Итог: совпало

## Факт 2. files.md, строка отчёта 501 (порог 35 %, позиция 500.1)

- Файл отчёта: `files.md`, строка 501 (вид строки: nl)
- Путь и строка исходника: `src/gamestates/cSetupSkirmishState.h:144`
- Текст строки отчёта:
```
cRectangle wormsRect;
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.h | sed -n '144p'
```
- Вывод:
```
    cRectangle wormsRect;
```
- Итог: совпало

## Факт 3. files.md, строка отчёта 858 (порог 60 %, позиция 857.4)

- Файл отчёта: `files.md`, строка 858 (вид строки: nl)
- Путь и строка исходника: `src/gamestates/cSelectYourNextConquestState.h:86`
- Текст строки отчёта:
```
void draw() const override;
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.h | sed -n '86p'
```
- Вывод:
```
    void draw() const override;
```
- Итог: совпало

## Факт 4. files.md, строка отчёта 1227 (порог 85 %, позиция 1214.7)

- Файл отчёта: `files.md`, строка 1227 (вид строки: nl)
- Путь и строка исходника: `src/debug/UiAuditScenes.cpp:1`
- Текст строки отчёта:
```
#include "debug/UiAuditScenes.hpp"
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAuditScenes.cpp | sed -n '1p'
```
- Вывод:
```
#include "debug/UiAuditScenes.hpp"
```
- Итог: совпало

## Факт 5. functions.md, строка отчёта 200 (порог 10 %, позиция 199.2)

- Файл отчёта: `functions.md`, строка 200 (вид строки: nl)
- Путь и строка исходника: `src/game/cGame_logic.cpp:1106`
- Текст строки отчёта:
```
m_drawManager->init();
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '1106p'
```
- Вывод:
```
                    m_drawManager->init();
```
- Итог: совпало

## Факт 6. functions.md, строка отчёта 698 (порог 35 %, позиция 697.2)

- Файл отчёта: `functions.md`, строка 698 (вид строки: nl)
- Путь и строка исходника: `src/gamestates/cSetupSkirmishState.cpp:285`
- Текст строки отчёта:
```
startPointsRect = cRectangle(startPointsX, startPointsY, startPointHitBoxWidth, startPointHitBoxHeight);
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp | sed -n '285p'
```
- Вывод:
```
    startPointsRect = cRectangle(startPointsX, startPointsY, startPointHitBoxWidth, startPointHitBoxHeight);
```
- Итог: совпало

## Факт 7. functions.md, строка отчёта 1196 (порог 60 %, позиция 1195.2)

- Файл отчёта: `functions.md`, строка 1196 (вид строки: nl)
- Путь и строка исходника: `src/gamestates/cSelectYourNextConquestState.cpp:154`
- Текст строки отчёта:
```
}
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | sed -n '154p'
```
- Вывод:
```
    }
```
- Итог: совпало

## Факт 8. functions.md, строка отчёта 1694 (порог 85 %, позиция 1693.2)

- Файл отчёта: `functions.md`, строка 1694 (вид строки: nl)
- Путь и строка исходника: `src/game/cGameConditionChecker.cpp:103`
- Текст строки отчёта:
```
*/
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp | sed -n '103p'
```
- Вывод:
```
             */
```
- Итог: совпало

## Факт 9. names.md, строка отчёта 58 (порог 10 %, позиция 57.5)

- Файл отчёта: `names.md`, строка 58 (вид строки: git grep)
- Путь и строка исходника: `src/game/cGame_logic.cpp:988`
- Текст строки отчёта:
```
bool deleteOldState = (newState != GAME_REGION &&
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '988p'
```
- Вывод:
```
        bool deleteOldState = (newState != GAME_REGION &&
```
- Итог: совпало

## Факт 10. names.md, строка отчёта 223 (порог 35 %, позиция 201.2)

- Файл отчёта: `names.md`, строка 223 (вид строки: git grep)
- Путь и строка исходника: `src/game/cGame.h:130`
- Текст строки отчёта:
```
// void loadSkirmishMaps() const;
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h | sed -n '130p'
```
- Вывод:
```
    // void loadSkirmishMaps() const;
```
- Итог: совпало

## Факт 11. names.md, строка отчёта 354 (порог 60 %, позиция 345.0)

- Файл отчёта: `names.md`, строка 354 (вид строки: git grep)
- Путь и строка исходника: `src/gamestates/cCreditsState.cpp:45`
- Текст строки отчёта:
```
m_moveSpeed(0.15f)
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp | sed -n '45p'
```
- Вывод:
```
    m_moveSpeed(0.15f)
```
- Итог: совпало

## Факт 12. names.md, строка отчёта 530 (порог 85 %, позиция 488.8)

- Файл отчёта: `names.md`, строка 530 (вид строки: git grep)
- Путь и строка исходника: `src/game/cGame.h:89`
- Текст строки отчёта:
```
friend class UiAuditAccess;
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h | sed -n '89p'
```
- Вывод:
```
    friend class UiAuditAccess;
```
- Итог: совпало

## Факт 13. houses.md, строка отчёта 79 (порог 20 %, позиция 78.6)

- Файл отчёта: `houses.md`, строка 79 (вид строки: git grep)
- Путь и строка исходника: `src/gameobjects/players/cPlayerDifficultySettings.cpp:95`
- Текст строки отчёта:
```
case SARDAUKAR:
```
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayerDifficultySettings.cpp | sed -n '95p'
```
- Вывод:
```
        case SARDAUKAR:
```
- Итог: совпало

## Факт 14. houses.md, порог 50 %

Не найдено: искал строку вида `<путь>:<номер>:<текст>` или `<номер>\t<текст>` с номером строки отчёта не меньше 196.5; в отчёте такой нет.

Итог: не найдено, факт не выбран

## Факт 15. houses.md, порог 80 %

Не найдено: искал строку вида `<путь>:<номер>:<текст>` или `<номер>\t<текст>` с номером строки отчёта не меньше 314.4; в отчёте такой нет.

Итог: не найдено, факт не выбран

Итог: 13 из 15 совпало

Не выбрано фактов (подходящих строк нет): 2; проверено: 13, из них совпало: 13.

## Пункт 5 — states.md (Haiku)

Правило выбора: порог = ceil(1739 × p), берётся первая строка отчёта `<номер>\t<текст>` с непустым текстом на позиции не меньше порога.

## Факт 1. states.md, строка отчёта 174 (порог 10 %, порог 174)

- Путь и строка исходника: `src/gamestates/cCreatorState.h:19` (заголовок отчёта, строка 149)
- Текст строки отчёта: `#include "gamestates/cGameState.h"`
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.h | sed -n '19p'
```
- Вывод:
```
#include "gamestates/cGameState.h"
```
- Итог: совпало

## Факт 2. states.md, строка отчёта 523 (порог 30 %, порог 522, взята следующая подходящая строка)

- Путь и строка исходника: `src/gameobjects/mentat/AbstractMentat.cpp:204` (заголовок отчёта, строка 313)
- Текст строки отчёта: `        // its the same` (без пробелов по краям: `// its the same`)
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp | sed -n '204p'
```
- Вывод:
```
        // its the same
```
- Итог: совпало

## Факт 3. states.md, строка отчёта 873 (порог 50 %, порог 870, взята следующая подходящая строка)

- Путь и строка исходника: `src/game/CampaignProgress.hpp:1` (заголовок отчёта, строка 866)
- Текст строки отчёта: `/**`
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.hpp | sed -n '1p'
```
- Вывод:
```
/**
```
- Итог: совпало

## Факт 4. states.md, строка отчёта 1218 (порог 70 %, порог 1218)

- Путь и строка исходника: `src/gamestates/cMentatState.cpp:126` (заголовок отчёта, строка 1160)
- Текст строки отчёта: `m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, humanPlayer, m_dataCampaign);` (с отступом 16 пробелов)
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | sed -n '126p'
```
- Вывод:
```
                m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, humanPlayer, m_dataCampaign);
```
- Итог: совпало

## Факт 5. states.md, строка отчёта 1576 (порог 90 %, порог 1566, взята следующая подходящая строка)

- Путь и строка исходника: `src/gamestates/cSelectYourNextConquestState.cpp:923` (заголовок отчёта, строка 1569)
- Текст строки отчёта: `void cSelectYourNextConquestState::installWorld()`
- Команда:
```
git -C C:/Users/Slaven/Projects/DUNE-p2 show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | sed -n '923p'
```
- Вывод:
```
void cSelectYourNextConquestState::installWorld()
```
- Итог: совпало

Итог пункта 5: 5 из 5 совпало
