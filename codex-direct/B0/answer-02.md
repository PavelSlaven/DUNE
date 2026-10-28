## REVIEW-b0 | 2026-10-28 | CHANGES

Проверялась вторая сдача в `/srv/dune/worktrees/b0` (пять файлов, не закоммичены). Механика верна: JSON детерминирован, все 199 ссылок `путь@коммит:строка` указывают на названный символ, судьба 390 путей совпадает с `git diff --name-status -M BASE..UP0`, числа плана разобраны, коллизии и индексы паков подтверждены, защита паков и мутации теста 4 работают. Сдачу продолжаешь в тех же пяти файлах.

Возврат — из-за отнесения файлов к функциям, во второй раз. Поэтому задание `TASK.md` меняет способ (причина — задание): в файле правил у каждой функции появляются маркеры кода, скрипт пишет `marker_hits` по строкам диффа, тест 6 требует, чтобы каждое совпадение маркера было объяснено, и сверяет известные случаи; тест 7 сверяет списки функций в карте с JSON. Раздел 1.2, раздел «Тест» и раздел «Организация работы» прочитай целиком: задание — источник истины, этот список — только что исправить в сданной работе.

Что исправить:

1. `tools/upstream/port_features.json:84`, `:207–208`, `:65` (и `paths[...].features` JSON, `PORT_MAP.md:135`, `:139`, `:305–306`) — файлы явно вписаны в функцию, кода которой в них нет:
   - `src/gameobjects/structures/cWindTrap.cpp` вписан в `hd-render`; единственное изменение форка — локализация (`#include "utils/Localization.hpp"`, `localization::format("{}; output {}%", "{}; выработка {}%", ...)`). Ожидается `localization`.
   - `src/gameobjects/structures/cHeavyFactory.cpp` и `src/gameobjects/structures/cLightFactory.cpp` вписаны в `localization`; локализации в диффе нет, изменения — HD-рендер (`renderStrechSprite(..., getVisualRectangle())`), у `cLightFactory.cpp` ещё `gfxdata->findTexture("BUILD_LIGHTFACTORY_PRODUCTION")` при `getDensity() > 1` (запись 240 пака `sdl_data_hd4.dat`). Ожидается `hd-render`, у `cLightFactory.cpp` также `hd4-assets`.
   - `src/include/definitions.h` вписан в `hd-render`; единственное изменение — `#define MOUSECELL_COMMAND_BAR -4`. Ожидается `command-bar`.

   Важность — В: исполнители шагов Б4 и Б7 этих файлов в своих списках не увидят.

2. Файлы, несущие несколько функций, отнесены не ко всем (пункт 2 `answer-01.md` закрыт не до конца). Дифф `git diff e17379ad 6662b2f4 -- <путь>`:
   - `src/gamestates/cMainMenuState.cpp` — `#include "save/SaveSlotsDialog.hpp"`, кнопка с `SaveGameManager::hasAnySave()`; нет `save-slots`.
   - `src/utils/GameSettings.hpp` — `CommandBindings commandBindings;`, `int renderScalePercent`; нет `command-bar` и `hd-render`.
   - `src/gamestates/cOptionsState.cpp` и `.h` — настройки `RenderScale` и `WorldScale` (`m_savedRenderScalePercent`, `ManualWorldScales`); нет `hd-render`.
   - `src/drawers/cMiniMapDrawer.cpp` — радар по `HudLayout::create(...)` и `hud.radarViewport`; нет `adaptive-layout`.
   - `src/drawers/cMessageDrawer.cpp` — размещение по `HudLayout` и `MusicControlsLayout`; нет `adaptive-layout` и `music-pools`.
   - `src/drawers/cMouseDrawer.cpp` — `localization::format("Sight: {}", "Обзор: {}", ...)`; нет `localization`.

   Ревьюер нашёл маркер чужой функции в 31 файле; выше — проверенные глазами. Ожидается: все 174 пути `src/`, `tests/`, `CMakeLists.txt` проходят через маркеры и тест 6 задания; каждое необъяснённое совпадение разобрано по диффу пути — функция добавлена или записана в `marker_exceptions` с причиной. Важность — С.

3. `docs/upstream/PORT_MAP.md:475` и `:736` — преемником удалённого `src/managers/cInteractionManager.cpp` назван `cGameControlsContext::onNotifyMouseEvent` (`src/controls/cGameControlsContext.cpp@a51b97f:210`). Эта функция была и в `BASE` (`@e17379ad:167`), и её вызывал сам `cInteractionManager` (`src/managers/cInteractionManager.cpp@e17379ad:85`), то есть это вызываемая функция, а не преемник. Блок рассылки событий мыши из `cInteractionManager::onNotifyMouseEvent` (`@e17379ad:81–97`) в `UP0` стоит в `cGamePlaying::onNotifyMouseEvent` — `src/gamestates/cGamePlaying.cpp@a51b97f:304`, с тем же комментарием «must be first because other classes rely on this context» (`:307`) и `m_mapCamera->onNotifyMouseEvent(event)` (`:310`). Ожидается: преемник — `cGamePlaying::onNotifyMouseEvent` в `:475` и в риске `:736`. Важность — В: перенос маршрутизации мыши для панели приказов (Б10) иначе уйдёт не в тот класс.

4. `tools/upstream/port_features.json:211` — шаблон `resources/bin/*/briefing*` в `localization` захватывает три музыкальных файла `resources/bin/music/briefing/{atreides,harkonnen,ordos}/*_MENTAT_*.wav` (знак `*` проходит через `/`). Ожидается: шаблон убрать. Важность — Н.

5. Узкие функции у путей из широких шаблонов (`hd4-assets` у них остаётся):
   - `tools/normalize_faction_masks.py`, `tools/check_unit_mask_uniformity.py`, `tools/verify_building_flag_colors.py`, `tools/verify_harvester_house_colors.py` — добавить `faction-tint-terrain`;
   - `tools/check_skirmish_and_mentat_ui.py` — добавить `localization`;
   - `resources/hd/master4/command_bar.png`, `resources/hd/master4/command_bar_disabled.png`, `resources/hd/source_references/command_bar_*.png` — добавить `command-bar`.

   Важность — Н.

6. `docs/upstream/PORT_MAP.md:738` — «Какой набор читает движок — не проверено». Код отвечает: `src/mentat/AbstractMentat.cpp@6662b2f:692` читает только `data/scenes/hd4/sdl_{}.dat`, путь `hd4/hd4` в `src/` не встречается. Ожидается: написать это со ссылкой; вложенный набор `scenes/hd4/hd4` кодом не читается. Важность — Н.

7. Списки функций в `PORT_MAP.md` построены разовым кодом в сессии, сверка `.tmp/audit_map.py` не сдана, теста «карта = JSON» нет. Ожидается: тест 7 задания; после правок 1, 2 и 5 карта перестраивается и тест 7 зелёный. Важность — Н, причина — задание.

Папки `.tmp/` и `__pycache__` прошлых кругов ведущий перенёс в архив; твои рабочие файлы и логи этого круга — в `.tmp/`. Тест 1 пишет временную папку в `ROOT/.tmp`; перевести на `tempfile.TemporaryDirectory()`.

Сдача — `DONE-b0` по правилам: журнал хода, красный прогон тестов 6 и 7, строки мутационного прогона, зелёный прогон полной командой задания, раздел «не проверено», `git status --short`.
