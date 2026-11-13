# Задание P5G2 — сцены меню, кампании, ментатов и титров в режиме отладки интерфейса (шаг П5г, часть 2)

Исполнитель: корневая нить Codex `gpt-6-luna` `xhigh` и три помощника `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g2`, `HEAD` — `9f222a72f5a1c711788e0652b147e9d977972b82` (приёмочные тесты этой части поверх вершины ветки порта `91416fb0`). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5g2/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Добавить в режим отладки интерфейса порта 107 сцен экранов вне боя и записи режима из кода этих экранов по плану `PLAN-P5G2` ниже так, чтобы прошли замороженные приёмочные тесты этой части — скрипты `tests/ui_audit/ui_audit_part2_catalog.py` и `tests/ui_audit/ui_audit_part2_scenes.py` на установленной игре — и остались зелёными сборка (319 тестов) и четыре скрипта Python частей 1 и 4.

## Что уже решено

- Форк `9208dcf5a358f40afd95c99480e4e09f781ed566` (дальше — `FORK1`) написан на SDL2 и глобальных объектах игры (`game`, `players`, `drawManager`); порт — на SDL3, объектах `cGame`, `cGameSettings` и состояниях игры, которые создаёт `cCreatorState`. Сцены и записи переносятся из `FORK1` по плану и правилам переноса ниже, а не копируются.
- Часть 2 переносит сцены групп `region`, `choose-house`, `select-mission`, `tellhouse`, `mentat`, `skirmish-setup`, `options-menu`, `credits`, записи `click` экранов этих групп и записи `credit` титров. Сцены Дома Сардаукаров добавлены там же, где у трёх Домов форка: в порту есть кампания, ментат, карточка выбора Дома и тексты брифингов Сардаукаров.
- Не переносятся: сцены `options-menu-game`, `options-menu-controls`, `options-menu-diagnostics`, `options-menu-keybind` (в меню настроек порта нет страниц и назначения клавиш); `main-menu-saves`, `save-dialog-*` (шаг П8); `options-game-*`, `outcome-*`, `game-*`, `units-label-*`, `structure-label-*` (часть 3), а с ними функции `UiAuditAccess` `enterPlaying`, `missionOutcome`, `writeSaves`, `openMenuSaveDialog`, `saveDialog`, `optionsPage`, `optionsBinding`, `mentat`, `mapViewport`, `clearMouseClicks`, `stopCameraEdgeMove` и записи `area` и `label`.
- В порту ментат живёт в состоянии игры (`cMentatState::m_mentat`, `cTellHouseState::m_mentat`), а не в `cGame`. Поэтому сцена рассказа о Доме создаёт состояние `GAME_TELLHOUSE` заново вызовом `setState` (конструктор `cTellHouseState` сам готовит ментата для Дома `m_dataCampaign->housePlayer`), а не вызовом `cGame::prepareMentatToTellAboutHouse`: тот смотрит прогресс кампании и может пропустить рассказ.
- Файл `tools/ui-audit/exclusions.tsv` в этой части не меняется: его текст заморожен тестом части 4.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- приёмочные тесты этой части: `tests/ui_audit/ui_audit_part2_catalog.py`, `tests/ui_audit/ui_audit_part2_scenes.py`;
- файлы режима порта: `src/debug/UiAudit.hpp`, `src/debug/UiAuditCapture.cpp`, `src/debug/UiAuditScenes.hpp`, `src/debug/UiAuditScenes.cpp`, `src/debug/UiAuditAccess.cpp`;
- файлы порта: `src/game/cGame.h`; строки 913–940, 942–1228, 1239–1255 и 1489–1506 файла `src/game/cGame_logic.cpp`; `src/gamestates/cMentatState.h`, `src/gamestates/cTellHouseState.h`, `src/gamestates/cCreditsState.h`, `src/gamestates/cOptionsState.h`, `src/gamestates/cSetupSkirmishState.h`, `src/gamestates/cSelectYourNextConquestState.h`, `src/gameobjects/mentat/AbstractMentat.h`; строки 111–142 файла `src/gamestates/cChooseHouseState.cpp`; строки 441–469 файла `src/gamestates/cCreditsState.cpp`; строки 341–376 файла `src/gamestates/cSelectYourNextConquestState.cpp`; строки 273–314 файла `src/gameobjects/mentat/AbstractMentat.cpp`; строки 60–92, 436–534 и 1446–1530 файла `src/gamestates/cSetupSkirmishState.cpp`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>` для файлов форка: `src/debug/UiAudit.hpp`, `src/debug/UiAuditScenes.cpp`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '67,129p;202,301p'`, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | sed -n '33,43p;76,93p;200,211p;245,320p;354,357p;430,454p'`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь> | sed -n '<строки>'` для мест вызова режима в форке: `src/gamestates/cChooseHouseState.cpp` — `107,116p`; `src/gamestates/cCreditsState.cpp` — `403,407p`; `src/gamestates/cSelectYourNextConquestState.cpp` — `308,319p`; `src/gamestates/cSetupSkirmishState.cpp` — `452,497p`; `src/mentat/AbstractMentat.cpp` — `405,408p`.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт поведения

Этот раздел дословно взят из задания приёмочных тестов `TASK-G2T`.

Пункты 1–4 контракта части 1 действуют без изменений. Игра запускается так же, как в пункте 2 части 1: из каталога установки сборки порта (рабочий каталог процесса — этот каталог) с аргументами `-windowed -screenWidth 1024 -screenHeight 768` и аргументами режима; переменные среды `SDL_VIDEODRIVER=dummy`, `SDL_RENDER_DRIVER=software`, `SDL_AUDIODRIVER=dummy`, `XDG_DATA_HOME=<пустая временная папка>`; `LD_LIBRARY_PATH` задаёт вызывающий процесс. Три скрипта части 1 в `tests/ui_audit/` остаются зелёными.

5. **Каталог части 2.** В выводе `--ui-audit-list` у каждой сцены ровно ключи части 1. Среди сцен, у которых `group` — одна из `region`, `choose-house`, `select-mission`, `tellhouse`, `mentat`, `skirmish-setup`, `options-menu`, `credits`, нет двух с одним `id`, и эти сцены ровно совпадают по `id` и значениям всех ключей со 107 сценами таблицы ниже. У каждой из 107 сцен `game_screen` — `false`, `hud` — `false`, `hover` — `null`, `hd_only` — `false`, кроме `credits-4` и `credits-5`, у которых `hd_only` — `true`. `<дом>` — каждое из `atreides`, `harkonnen`, `ordos`, `sardaukar`; `<фаза>` — каждое из `speak`, `await`; `<Ментат>` — `AtreidesMentat`, `HarkonnenMentat`, `OrdosMentat`, `SardaukarMentat` для `<дом>` в том же порядке; `""` — пустая строка.

   | `id` | `group` | `state` | `screen` | `house` | `readiness` |
   |---|---|---|---|---|---|
   | `region-<дом>-intro-<n>`, n = 1, 2, 3 | `region` | `GAME_REGION` | `cSelectYourNextConquestState` | `<дом>` | `RegionIntroScene` |
   | `region-<дом>-conquer-<n>`, n = 3, 5, 7, 9 | `region` | `GAME_REGION` | `cSelectYourNextConquestState` | `<дом>` | `RegionConquerMessage` |
   | `region-<дом>-select-<n>`, n = 2, 3, 4, 5, 6, 7, 8, 9 | `region` | `GAME_REGION` | `cSelectYourNextConquestState` | `<дом>` | `RegionStateSelect` |
   | `choose-house` | `choose-house` | `GAME_SELECT_HOUSE` | `cChooseHouseState` | `""` | `StateSettled` |
   | `select-mission-<дом>` | `select-mission` | `GAME_MISSIONSELECT` | `cSelectMissionState` | `<дом>` | `StateSettled` |
   | `tellhouse-<дом>-<фаза>` | `tellhouse` | `GAME_TELLHOUSE` | `BeneMentat` | `<дом>` | `MentatFrozen` |
   | `mentat-briefing-<дом>-<фаза>` | `mentat` | `GAME_BRIEFING` | `<Ментат>` | `<дом>` | `MentatFrozen` |
   | `mentat-win-<дом>-<фаза>` | `mentat` | `GAME_WINBRIEF` | `<Ментат>` | `<дом>` | `MentatFrozen` |
   | `mentat-lose-<дом>-<фаза>` | `mentat` | `GAME_LOSEBRIEF` | `<Ментат>` | `<дом>` | `MentatFrozen` |
   | `skirmish-setup-random`, `skirmish-setup-ready-map` | `skirmish-setup` | `GAME_SETUPSKIRMISH` | `cSetupSkirmishState` | `""` | `FixedFrames(2, no readiness flag)` |
   | `options-menu-main`, `options-menu-applied` | `options-menu` | `GAME_OPTIONS` | `cOptionsState` | `""` | `FixedFrames(14, no readiness flag)` |
   | `credits-title`, `credits-1`, `credits-2`, `credits-3`, `credits-4`, `credits-5` | `credits` | `GAME_CREDITS` | `cCreditsState` | `""` | `CreditsScrollPosition` |

6. **Прогон сцены.** Для каждой из 107 сцен пункта 5 запуск с `--ui-audit-scene <id> --ui-audit-out <папка>` завершается с кодом выхода 0 не позже чем через 120 секунд; в `<папка>` есть файлы `<id>.png` и `<id>.geometry.jsonl`. PNG — 1024 × 768 точек, в нём есть блок `IDAT`, файл заканчивается блоком `IEND`, размер файла — не меньше 10 000 байт (снимок экрана, а не одноцветный кадр). Файл геометрии — текст UTF-8 из строк, разделённых символом `
` (после последней строки может стоять `
`); каждая строка — объект JSON без значений `NaN`, `Infinity` и `-Infinity`. Первая строка — заголовок: в нём значения ключей `k`, `scene`, `resolution`, `language`, `graphics`, `canvas`, `game_screen`, `render_scale`, `world_scale` равны `"header"`, `"<id>"`, `"1024x768"`, `"en"`, `"hd"`, `{"w": 800, "h": 600}`, `false`, `0`, `0`, а `version` — строка; другие ключи заголовка не проверяются. Каждая следующая строка — запись одного из четырёх видов ровно с такими ключами: `"k": "text"` — `k`, `s`, `x`, `y`, `w`, `h`, `box`; `"k": "gui"` — `k`, `t`, `x`, `y`, `w`, `h`; `"k": "click"` — `k`, `name`, `x`, `y`, `w`, `h`; `"k": "credit"` — `k`, `name`, `s`. У записей `text`, `gui` и `click` значения `x`, `y`, `w`, `h` — целые числа JSON. У каждой записи `click` прямоугольник лежит внутри холста: `w` > 0, `h` > 0, `x` ≥ 0, `y` ≥ 0, `x + w` ≤ 800, `y + h` ≤ 600. После всех запусков в папке `XDG_DATA_HOME` нет файла с именем `preferences.ini` ни на каком уровне вложенности.

7. **Записи сцен.** «Одна запись click `<имя>`» — ровно одна запись `"k": "click"` с этим `name`; «на весь холст» — `x` 0, `y` 0, `w` 800, `h` 600; «запись text `<строка>`» — запись `"k": "text"` с `s`, равным строке; прямоугольник A «внутри» прямоугольника B — `A.x` ≥ `B.x`, `A.y` ≥ `B.y`, `A.x + A.w` ≤ `B.x + B.w`, `A.y + A.h` ≤ `B.y + B.h`. `<вид>` — каждое из `briefing`, `win`, `lose`; `<Дом>` — `Atreides`, `Harkonnen`, `Ordos`, `Sardaukar` для `<дом>` в том же порядке.
   - `choose-house`: для каждой пары (`house-atreides`, `ATREIDES`), (`house-ordos`, `ORDOS`), (`house-harkonnen`, `HARKONNEN`), (`house-sardaukar`, `SARDAUKAR`), (`house-back`, `Back`) — одна запись click с этим именем и хотя бы одна запись text с этой строкой внутри прямоугольника этой записи click (порт рисует подписи карточек Домов и кнопки возврата внутри них, `src/gamestates/cChooseHouseState.cpp@91416fb:111-142` и функция `drawHdHouseCard`); запись text `CHOOSE YOUR HOUSE`.
   - Каждая сцена `select-mission-<дом>`: запись text `REPLAY MISSION`.
   - Каждая сцена `tellhouse-<дом>-speak` и `mentat-<вид>-<дом>-speak`: одна запись click `mentat-skip` на весь холст; нет записи text, у которой `s` начинается с `Do you wish to join house`.
   - Каждая сцена `tellhouse-<дом>-await`: нет записи click `mentat-skip`; есть запись text `Do you wish to join house <Дом> ?`.
   - Каждая сцена `mentat-<вид>-<дом>-await`: нет записи click `mentat-skip`.
   - `skirmish-setup-ready-map`: записи click `skirmish-house:<r>`, `skirmish-credits:<r>`, `skirmish-units:<r>`, `skirmish-team:<r>` для каждого r из 1, 2, 3, 4, записи click `skirmish-brain:3`, `skirmish-brain:4`, `skirmish-blooms`, `skirmish-worms`, `skirmish-tech-level`, `skirmish-detonate-blooms` и хотя бы одна запись click, у которой `name` начинается с `skirmish-map:`; нет записей click `skirmish-start-points`, `skirmish-brain:1`, `skirmish-brain:2`; запись text `Skirmish`.
   - `skirmish-setup-random`: записи click `skirmish-start-points`, `skirmish-house:1`, `skirmish-house:2`; нет записей click `skirmish-house:3`, `skirmish-brain:3`.
   - В обеих сценах схватки каждая запись click с `name` вида `skirmish-<столбец>:<r>`, где `<столбец>` — `brain`, `house`, `credits`, `units` или `team`, а r — номер строки игрока сцены (1–4 в `skirmish-setup-ready-map`, 1–2 в `skirmish-setup-random`), единственная со своим `name`, её `h` — 16, а `x` и `w` — по столбцу раскладки `SkirmishPlayerTableLayout` порта (`src/gamestates/cSetupSkirmishState.cpp@91416fb:64-84`): `brain` — 4 и 68, `house` — 72 и 94, `credits` — 166 и 89, `units` — 255 и 70, `team` — 325 и 75. Записи `skirmish-house:<r>` есть для каждой строки игрока сцены, по одной, и у записи строки r + 1 `y` ровно на 26 больше, чем у записи строки r.
   - `options-menu-main`: хотя бы одна запись `"k": "gui"`; нет записи text `Saved. Restart the game.`.
   - `options-menu-applied`: запись text `Saved. Restart the game.`.
   - Каждая сцена `region-<дом>-intro-<n>` и `region-<дом>-conquer-<n>`: нет записи click `campaign-region-map`.
   - Каждая сцена `region-<дом>-select-<n>`: одна запись click `campaign-region-map`.
   - Каждая из шести сцен `credits-*`: одна запись click `credits-speed-up` на весь холст; хотя бы одна запись `"k": "credit"`; у каждой записи text `y` ≥ 0 и `y + h` ≤ 600.

8. **Титры целиком.** Функция `check_credits.check_credits(<папка>)` из `tools/ui-audit/check_credits.py` порта, вызванная для папки с файлами геометрии шести сцен титров, возвращает число комбинаций 1 и пустой список проблем: каждая строка титров (запись `credit`) целиком видна хотя бы в одной сцене титров.

## Правила переноса

Строки форка, которые план велит перенести, меняются только по этим правилам:

1. `players[HUMAN].setHouse(<дом>)` → `UiAuditAccess::setHouse(game, <дом>)`; `drawManager->hasMessage()` → `UiAuditAccess::hasMessage(game)`; `game.m_screenH` → `currentGame.m_gameSettings->getScreenH()`; `std::strlen(mentat->sentence[<i>])` → `mentat->sentence[<i>].size()`; поле `startingPoints` → `iStartingPoints`; поле `m_displayStatusLabel` → `m_statusLabel`; `localization::text("<английский>", "<русский>")` → `"<английский>"`; имя параметра `game` в функциях `UiAuditAccess` → `currentGame`, как в функциях части 1 того же файла.
2. Прочие правила переноса части 1 действуют: `assert(` → `d2tm_assert(`; `logbook(...)` форка не переносится; подключения — пути порта от папки `src` (`"game/cGame.h"`, `"gamestates/cMentatState.h"`).
3. Вызов форка, у которого в порту нет пары по правилам 1–2 и плану, — подбери вызов порта с тем же действием в рамке правок и запиши строкой «Решено исполнителем» (файл:строка порта, вызов форка → вызов порта, основание — строка порта, где этот вызов уже делает то же действие). Нет вызова порта с тем же действием — блок `## Q-P5G2-NN` и стоп.

## PLAN-P5G2

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `src/debug/UiAudit.hpp` | В пространстве имён `uiaudit`: сразу после объявления `recordClick` — `void recordCanvasClick(const char *name);`; сразу после класса `BoxScope` — `void setVerticalClipText(bool enabled);` и `void recordCreditLine(const std::string &name, const std::string &text);` (строки 51, 66, 67 `src/debug/UiAudit.hpp` `FORK1`). В классе `UiAuditAccess` после `notFadingOut` — ровно двенадцать статических функций в этом порядке: `static void setHouse(cGame &game, int house);`, `static bool prepareMentatScene(cGame &game, int house, int kind);`, `static bool mentatFreeze(cGame &game, bool awaiting);`, `static bool prepareSkirmish(cGame &game, int variant);`, `static bool optionsStatus(cGame &game);`, `static bool creditsScroll(cGame &game, int frame);`, `static void recordCreditLines(cGame &game);`, `static void regionOpen(cGame &game, int mission, bool jump);`, `static int regionState(const cGame &game);`, `static int regionScene(const cGame &game);`, `static int regionSceneAlpha(const cGame &game);`, `static bool hasMessage(const cGame &game);`. Других объявлений не добавляй. | помощник A |
| 2 | `src/debug/UiAuditCapture.cpp` | (а) `enum class Kind { Text, Gui, Click, Credit };`. (б) В структуре `Entry` последним полем — `std::string name;`; каждый инициализатор `Entry` в файле перечисляет все шесть полей: у записей `Text`, `Gui`, `Click` последние два — `{}, {}`, как в строках 289, 303, 313 `FORK1` (иначе флаг `-Wextra` сборки CI с `-Werror` даёт ошибку о пропущенном поле). (в) Переменная `bool g_clipText = false;` сразу после `g_fadeAtBegin`. (г) В `writeGeometry` — ветка `case Kind::Credit:` строк 204–207 `FORK1`. (д) В `capture` перед строкой `const fs::path log = …` — строки 252–254 `FORK1` (`UiAuditAccess::recordCreditLines(currentGame)` для группы `credits`). (е) Сразу после закрывающей скобки анонимного пространства имён — функция `setVerticalClipText` строк 265–268 `FORK1`. (ж) Первые строки тела `recordText` — строки 286–288 `FORK1` (запись текста вне высоты холста при `g_clipText` пропускается). (з) Сразу после `recordClick` — `recordCanvasClick` строк 316–319 `FORK1`, затем `recordCreditLine`: `g_entries.push_back({Kind::Credit, text, {0, 0, 0, 0}, false, {}, name});`. (и) В `onSetupDone` сразу после строки `g_done = false;` — `g_clipText = false;`. Остальной код файла не меняется. | помощник A |
| 3 | `src/debug/UiAuditScenes.cpp` | (а) Подключения `#include "include/definitions.h"` и `#include "gamestates/cSelectYourNextConquestState.h"`. (б) В начале анонимного пространства имён — строки 16–32 `FORK1` (`g_step`, `g_wait`, `resetSteps`, `pause`). (в) Массив `kGroupScreens` — ровно восемь строк в этом порядке: `main-menu` (есть), затем строки 51–55, 59 и 61 `FORK1` (`region`, `choose-house`, `select-mission`, `tellhouse`, `options-menu`, `credits`, `skirmish-setup`). (г) После функции `scene` — `withScreen` и `hdOnly` (строки 78–89 `FORK1`). (д) Функции подготовки и готовности строк 97–109, 138–220, 284–304 и 327–360 `FORK1` (других функций подготовки форка в файле нет) с изменениями: в `prepareSelectMission` и `prepareRegion` вместо `players[HUMAN].setHouse(House);` — `UiAuditAccess::setHouse(game, House);`; тело `prepareTellHouse` — ровно `resetSteps(); UiAuditAccess::setHouse(game, House); UiAuditAccess::setState(game, GAME_TELLHOUSE); return true;`; в `readyOptionsMenu` строки 197–205 заменены строкой `if (Variant == 1) { UiAuditAccess::optionsStatus(game); }`, строк 212–214 нет, остальные шаги `switch` — как в форке; в `readyRegionConquer` — `UiAuditAccess::hasMessage(game)` вместо `drawManager->hasMessage()`; `prepareMainMenu` остаётся. (е) Вектор `g_catalog` — сцена `main-menu` (есть) и ровно 107 сцен таблицы пункта 5 контракта, в таком порядке: сцены `region` по Домам `atreides`, `harkonnen`, `ordos`, `sardaukar` (у каждого Дома intro 1–3, conquer 3, 5, 7, 9, select 2–9 — строки 364–408 `FORK1` и такие же 15 строк для `SARDAUKAR`); `choose-house` (строка 409); `select-mission` по тем же четырём Домам (строки 410–413 и строка для `SARDAUKAR`); `tellhouse` по четырём Домам, у каждого `speak`, затем `await` (строки 414–425 и две строки для `SARDAUKAR`); `mentat` по четырём Домам, у каждого `briefing`, `win`, `lose`, у каждого вида `speak`, затем `await` (строки 426–461 и шесть строк для `SARDAUKAR` с экраном `"SardaukarMentat"`); строки 462–464 (`skirmish-setup`); строки 469–472 (`options-menu-main`, `options-menu-applied`); строки 508–513 (`credits`). Каждая сцена строится тем же вызовом `scene`/`withScreen`/`hdOnly`, что её строка `FORK1`. | помощник A |
| 4 | `src/debug/UiAuditAccess.cpp` | Двенадцать функций шага 1. `setHouse`: `currentGame.m_gameObjectsContext->getPlayer(HUMAN)->setHouse(house); currentGame.m_dataCampaign->housePlayer = house;`. `prepareMentatScene`: `setHouse(currentGame, house)`; `m_dataCampaign->mission = CampaignProgress::FIRST_MISSION`; `m_dataCampaign->region = 1`; при `kind == 0` — `setNextStateToTransitionTo(GAME_BRIEFING)` и `transitionStateIfRequired()` объекта `currentGame` (тот же путь, что у игры в `cGame::prepareMentatToTellAboutHouse` и `cGame::transitionStateIfRequired`); иначе `currentGame.setState(kind == 1 ? GAME_WINBRIEF : GAME_LOSEBRIEF)`; возвращает `true`, если `m_currentState` — `cMentatState` (через `dynamic_cast`) и его `m_mentat` не пуст. `mentatFreeze`: ментат — `m_mentat.get()` текущего состояния, если оно `cMentatState` или `cTellHouseState` (через `dynamic_cast`), иначе возврат `false`; дальше — тело строк 78–94 `FORK1` по правилу переноса 1. `prepareSkirmish`: `currentGame.setState(GAME_SETUPSKIRMISH)`, затем строки 118–128 `FORK1` по правилу переноса 1 (в порту карты схватки загружены при запуске игры, `src/game/cGame_logic.cpp@91416fb:823`, поэтому строк 114–117 `FORK1` нет). `optionsStatus`: строки 204–210 `FORK1` по правилу переноса 1. `creditsScroll`, `recordCreditLines`, `regionOpen`, `regionState`, `regionScene`, `regionSceneAlpha`: строки 213–301 `FORK1` по правилу переноса 1; в `regionOpen` вместо `game.m_mission = mission;` — `currentGame.m_dataCampaign->mission = mission;`. `hasMessage`: `return currentGame.m_drawManager->hasMessage();`. Подключения — заголовки порта тех классов, к полям и функциям которых обращаются эти функции. | помощник A |
| 5 | `src/gamestates/cMentatState.h`, `src/gamestates/cTellHouseState.h`, `src/gamestates/cCreditsState.h`, `src/gamestates/cOptionsState.h`, `src/gamestates/cSetupSkirmishState.h`, `src/gamestates/cSelectYourNextConquestState.h`, `src/gameobjects/mentat/AbstractMentat.h` | Строка `    friend class UiAuditAccess;` первой строкой тела класса `cMentatState`, `cTellHouseState`, `cCreditsState`, `cOptionsState`, `cSetupSkirmishState`, `cSelectYourNextConquestState`, `AbstractMentat` (сразу после строки `class <Класс> … {`). | помощник B |
| 6 | `src/gamestates/cChooseHouseState.cpp` | Подключение `#include "debug/UiAudit.hpp"`. Первые строки тела `cChooseHouseState::draw` — ветка `if (uiaudit::isEnabled()) { … }` строк 111–116 `FORK1` с пятью вызовами `uiaudit::recordClick`: `house-atreides`, `house-ordos`, `house-harkonnen`, затем `house-sardaukar` с прямоугольником `houseSardaukar`, затем `house-back` с прямоугольником `backButtonRect` (в порту это значение `cRectangle`, доступ через `.`). | помощник B |
| 7 | `src/gamestates/cCreditsState.cpp` | Подключение `#include "debug/UiAudit.hpp"`. Первые строки тела `cCreditsState::draw` — строки 405–407 `FORK1` (`uiaudit::recordCanvasClick("credits-speed-up")`). | помощник B |
| 8 | `src/gamestates/cSelectYourNextConquestState.cpp` | Подключение `#include "debug/UiAudit.hpp"`. В `cSelectYourNextConquestState::draw` сразу после строки `m_mouse->setTile(MOUSE_NORMAL); // global state of mouse` — строки 316–319 `FORK1` (запись `campaign-region-map` по прямоугольнику `m_hdCampaignLayout.map` в состоянии `REGSTATE_SELECT_NEXT_CONQUEST`). | помощник B |
| 9 | `src/gameobjects/mentat/AbstractMentat.cpp` | Подключение `#include "debug/UiAudit.hpp"`. В `AbstractMentat::draw` первыми строками внутри ветки `if (state == SPEAKING) {` — строки 406–408 `FORK1` (`uiaudit::recordCanvasClick("mentat-skip")`). | помощник B |
| 10 | `src/gamestates/cSetupSkirmishState.cpp` | Подключение `#include "debug/UiAudit.hpp"`. (а) В `cSetupSkirmishState::draw` сразу после закрывающей скобки цикла `for (int p = 0; p < (AI_WORM - 1); p++) { … }` строк 497–510 и перед вызовом `drawPanel(cRectangle(-1, screen_y - topBarHeight, …` — ветка `if (uiaudit::isEnabled()) { … }` строк 452–497 `FORK1` без цикла записи карт (строки 479–496) с такими изменениями: лямбда `zone` принимает `const std::string &name` и передаёт `name.c_str()`; прямоугольники строк игрока — поля `player`, `house`, `credits`, `units`, `team` объекта `const SkirmishPlayerTableLayout rowLayout(playerList.getY() + 4 + (p * m_playerRowHeight));` вместо `cRectangle(4, y, 73, 16)`, `cRectangle(74, y, 76, 16)`, `cRectangle(174, y, 56, 16)`, `cRectangle(272, y, 21, 16)`, `cRectangle(340, y, 21, 16)` форка; `startingPoints` → `iStartingPoints`. (б) В `cSetupSkirmishState::drawMapList` сразу после строки `if (mapToRender->name.empty()) continue;` — `if (uiaudit::isEnabled() && mapToRender->validMap) { uiaudit::recordClick(("skirmish-map:" + std::to_string(mapIndexToRender)).c_str(), iDrawX, iDrawY, mapItemButtonWidth, mapItemButtonHeight); }`: запись карты — по месту, где порт рисует кнопку карты. | помощник B |
| 11 | — | Проверки раздела «Проверки» по порядку. | помощник D |

## Проверки

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`.

1. `sha256sum -c .tmp/p5g2t/tests.sha256` — четыре строки `OK`.
2. `df -m /srv` — в столбце `Available` не меньше 5000, иначе блок `## Q-P5G2-01` и стоп. Сборка: `DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5g2/build.log 2>&1; echo exit=$?` — `exit=0`; итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of 319`.
3. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -E 'src/debug/|cChooseHouseState|cCreditsState|cSelectYourNextConquestState|cSetupSkirmishState|AbstractMentat|cMentatState|cTellHouseState|cOptionsState'` — пустой вывод.
4. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`; файл `.tmp/out/xdg/D2TM/Dune II - The Maker/preferences.ini` есть: его пишет пробный запуск игры без режима отладки внутри скрипта сборки, и он по-прежнему сохраняет настройки (запуски скриптов Python идут с другой, временной папкой `XDG_DATA_HOME`).
5. Для каждого скрипта `<скрипт>` из `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_tools_run_combo.py`, `ui_audit_part2_catalog.py`, `ui_audit_part2_scenes.py`: `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p5g2/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`. После — `rm -r tests/ui_audit/__pycache__`, если такая папка появилась.
6. Сверки `grep` (в скобках — ожидаемый вывод):
   - `grep -rn -E 'localization|d2tmc\.h|renderDrawer|mapCamera|SDL2/|logbook|players\[|drawManager->' src/debug` (пусто);
   - `grep -rn -E 'GameKind|recordArea|recordLabel|setHover|remove_all|optionsPage|optionsBinding|writeSaves|enterPlaying|missionOutcome|prepareTellHouse\(game' src/debug` (пусто);
   - `grep -c 'friend class UiAuditAccess' src/gamestates/cMentatState.h src/gamestates/cTellHouseState.h src/gamestates/cCreditsState.h src/gamestates/cOptionsState.h src/gamestates/cSetupSkirmishState.h src/gamestates/cSelectYourNextConquestState.h src/gameobjects/mentat/AbstractMentat.h` (по 1 в каждом файле);
   - `grep -c 'uiaudit::record' src/gamestates/cChooseHouseState.cpp src/gamestates/cCreditsState.cpp src/gamestates/cSelectYourNextConquestState.cpp src/gameobjects/mentat/AbstractMentat.cpp src/gamestates/cSetupSkirmishState.cpp` (5, 1, 1, 1, 2);
   - `git diff --quiet -- tools/ui-audit/exclusions.tsv; echo exit=$?` (`exit=0`).
7. `git -c lfs.storage=$PWD/.tmp/p5g2/lfs status --short` — только файлы рамки правок и строки `__pycache__` вне `tests/`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P5G2-NN` с выводом и стоп. Тест не подгоняй и не меняй: файлы из `.tmp/p5g2t/tests.sha256` заморожены.

## Сдача

Последнее сообщение — блок `## DONE-P5G2 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p5g2/progress.md`): строка на каждый шаг плана;
- вывод каждой проверки 1–7 с кодами выхода (не больше 40 строк на проверку);
- `git diff --stat` и список для коммита: один пункт — все файлы рамки правок, сообщение на английском о сценах меню, кампании, ментатов и титров режима отладки интерфейса, последняя строка — `Behavior changes: …` со списком;
- раздел «Решено исполнителем» — каждая строка по правилу переноса 3;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g2 --size`; у `.tmp/p5g2` пометка `оставить — логи проверок нужны ревью`. Папки `.tmp/out`, `.tmp/deps`, `.tmp/p5g2t` созданы до этой задачи и в раздел не входят; копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → шаги 1–4 (помощник A) и шаги 5–10 (помощник B) одновременно → шаг 11 (помощник D) → сдача и стоп.
- **Параллельно:** помощники A и B правят разные файлы и не ждут друг друга. Помощник D начинает, когда A и B сдали свои шаги.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных. В бриф каждого дословно входят разделы «Что уже решено», «Контракт поведения», «Правила переноса», его строки таблицы `PLAN-P5G2` (помощнику D — раздел «Проверки»), абзац «Комментарии в коде» и запрет править файлы вне своих строк плана и `.tmp/p5g2/`. Корневая нить сама не правит код, не запускает сборку и проверки: механику — правки, сборку, проверки, выписку логов — делают только помощники; корневая нить читает раздел «Прочитать до работы», раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников, отвечает на вопросы помощников в рамке плана и сдаёт. Ошибку сборки в файле помощника A или B корневая нить отдаёт тому же помощнику.
- **Остановки:** только на `## DONE-P5G2` и на блоках `## Q-P5G2-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5G2-08` и стоп.
- **Рамка правок:** `src/debug/UiAudit.hpp`, `src/debug/UiAuditCapture.cpp`, `src/debug/UiAuditScenes.cpp`, `src/debug/UiAuditAccess.cpp`, семь заголовков шага 5, `src/gamestates/cChooseHouseState.cpp`, `src/gamestates/cCreditsState.cpp`, `src/gamestates/cSelectYourNextConquestState.cpp`, `src/gameobjects/mentat/AbstractMentat.cpp`, `src/gamestates/cSetupSkirmishState.cpp` и папка `.tmp/p5g2/`. Понадобился другой файл — блок `## Q-P5G2-NN` и стоп. Сборка пишет в `.tmp/out/` и `.tmp/deps/`, игра — в `.tmp/out/run/bin/` и временные папки скриптов; это не правка.

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
