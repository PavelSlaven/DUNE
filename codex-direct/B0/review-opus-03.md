CHANGES

# Приёмка третьего круга B0 — Claude Opus 5.5, 2026-10-28

Проверялась сдача в `/srv/dune/worktrees/b0` (ветка `codex/b0`). Пять сданных файлов совпадают по sha256 с копиями `files3/`. Анализ диффов делался по локальному клону (`BASE`, `FORK`); всё, что касается `UP0`, проверено на сервере. Временные скрипты: на сервере `/tmp/b0-review3/refs.py` и `mut.py`, на ПК `…\scratchpad\codex\b0\r3\`. В рабочей копии ничего не менялось: `git status` до проверки и после неё одинаков.

Механика третьего круга в порядке. Тесты 6 и 7 написаны по заданию, мутации краснеют, все 206 ссылок `путь@коммит:строка (**символ**)` указывают на названный символ, судьба 379 путей в списках функций совпадает с JSON, пункты 3 и 6 `answer-02.md` закрыты по коду.

Возврат вызван тремя ошибками отнесения уровня С. Каждая нарушает раздел 1.2 задания: путь должен получать функцию по коду своего диффа, а маркер должен быть идентификатором, который форк добавил ради этой функции. Тест 6 их не ловит, потому что проверяет только недостающих владельцев (см. Н4). Все три правки небольшие и механические.

## Находки

**С1.** `docs/upstream/port_inventory.json` → `paths["src/cGame.h"].features`; `tools/upstream/port_features.json:573` (include функции `localization`); `docs/upstream/PORT_MAP.md:322–385` (раздел `localization`).
- Что не так: в третьем круге у `src/cGame.h` сняли `localization`, хотя в диффе `BASE..FORK` есть её код. Это пара текстур экрана исхода для двух языков: `src/cGame.h@6662b2f:353–356` (`m_hdVictoryRu`, `m_hdVictoryEn`, `m_hdDefeatRu`, `m_hdDefeatEn`). Нужную текстуру выбирает `localization::isEnglish()` в `src/cGame_logic.cpp@6662b2f:2590–2593`. Без локализации этих членов не было бы.
- Что ожидается: вернуть `localization` пути `src/cGame.h` (через include и маркер, например `\bm_hd(?:Victory|Defeat)(?:Ru|En)\b`). В раздел `localization` карты добавить строку «`src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90`», как в разделе `command-bar` (`PORT_MAP.md:459`).
- Важность: С. Исполнитель шага Б7 не увидит этот файл в своём списке. Файл в апстриме удалён, поэтому без строки в карте члены легко потерять.
- Причина: исполнитель.

**С2.** `tools/upstream/port_features.json:732` (маркер `m_playMusic`), `:733` (маркер `"playMusic"`), `:713` и `:726` (include `music-pools`); JSON `paths["src/gamestates/cMainMenuState.cpp"].features` и `paths["src/utils/common.cpp"].features`; `PORT_MAP.md:437`, `:445`.
- Что не так: оба маркера — идентификаторы апстрима, а не форка:
  - `m_playMusic` есть в `BASE`: `src/cGame.h@e17379ad:87`, `src/gamestates/cMainMenuState.cpp@e17379ad:244`;
  - `"playMusic"` — ключ INI, который читается уже в `BASE`: `src/utils/common.cpp@e17379ad:68`.

  В итоге появились два ложных владельца `music-pools`:
  - `src/gamestates/cMainMenuState.cpp` получил функцию в третьем круге только из-за переставленного кода апстрима: выключателя музыки по M/MUTE (`@6662b2f:513–514` = `@e17379ad:244–245`);
  - у `src/utils/common.cpp` единственное основание — строка `{"playMusic", boolToIni(settings.playMusic)}` (`@6662b2f:377`) в общем `saveSettingsToIni`. Эта функция сохраняет все настройки подряд: playSound, Debug и остальные.

  Кода пулов, истории и переключения треков ни в одном из двух диффов нет.
- Что ожидается: убрать `m_playMusic` и `"playMusic"` из маркеров `music-pools` (`m_lastEnemyWarningMs` и остальные оставить). Снять `music-pools` с обоих путей и убрать их из раздела карты.
- Важность: С. Исполнитель Б9 получит два файла без своего кода. Кроме того, маркер апстрима отметит любую изменённую строку рядом со старым флагом.
- Причина: исполнитель.

**С3.** `tools/upstream/port_features.json:792` (`OrderButtonPolicy` в маркере 0 функции `command-bar`), `:794` (`shouldDrawOrderLabelShadow` в маркере 2), `:766`, `:769–770` (include); JSON `paths["src/drawers/OrderButtonPolicy.hpp" | "src/drawers/cOrderDrawer.cpp" | "src/drawers/cOrderDrawer.h"].features`; `PORT_MAP.md:477`, `:480–481`.
- Что не так: `shouldDrawOrderLabelShadow()` управляет тенью надписи «ЗАКАЗ» на кнопке Starport в `cOrderDrawer::drawOrderButton`: `src/drawers/cOrderDrawer.cpp@6662b2f:57–65`, рядом `orderProcesser->isOrderPlaced()`. Код появился в коммите `ecfd4990` вместе с `StarportOrderQueue` и проверяется в блоке Starport: `tests/InteractionRegressionTests.cpp@6662b2f:91`, «starport order label shadow looks like a duplicate label». Бронзовая панель приказов (`cCommandBarDrawer`) эту политику не использует: «заказ» здесь — покупка в Starport, а не «приказ» юнитам. Маркер отнёс этот код к `command-bar`. Из-за него `cOrderDrawer.cpp` и `.h` получили `command-bar` в этом круге, а маркеры `starport-orders` этот код пропускают.
- Что ожидается: убрать `OrderButtonPolicy` и `shouldDrawOrderLabelShadow` из маркеров `command-bar`. `OrderButtonPolicy.hpp` отнести к функции, которой принадлежит кнопка заказа Starport: к `starport-orders` или к функциям, которые рисуют надпись (`hd-render`, `localization`). Выбрать по коду `ecfd4990` — решает sol. Снять `command-bar` с `OrderButtonPolicy.hpp` и `cOrderDrawer.*` и поправить раздел карты.
- Важность: С. Шаг один (Б10), поэтому перенос не уйдёт далеко, но факт карты неверен.
- Причина: исполнитель.

**Н1.** Маркеры, совпадающие с кодом апстрима, кроме уже названных в С2. Ложных владельцев они сейчас не дают: у каждого такого пути есть и признак форка. Но любую изменённую строку апстрима рядом с таким идентификатором они отметят как код функции.
- `port_features.json:412` (`hd-render`: `renderStrechSprite`, `renderStrechFullSprite` — в `BASE` в 12 и 9 файлах);
- `:518` (`adaptive-layout`: `buttonWidth`, `buttonHeight` — локальные переменные в 4 меню `BASE`);
- `:436` (`retina-render-state`: `renderTargetStack` — член `src/drawers/SDLDrawer.hpp` в `BASE`);
- `:640` (`TTF_SizeUTF8`);
- `:897` (`m_titleBmp`);
- `:301` (`UNIT_RAIDER` — `#define` апстрима);
- `:928` (`CMAKE_CXX_COMPILER_ID`, `HOMEBREW_PREFIX`).

Мелочи:
- `:558`: `HM_` записан без `\b` (совпадений нет).
- `TTF_RenderUTF8_Blended` стоит и в `hd-render` (`:413`), и в `localization` (`:640`), поэтому функции не различает.

Проверенные отдельно маркеры приемлемы:
- `\b(?:language|…)\b` (`:639`) даёт 6 путей, и все с настоящей локализацией. Одно совпадение — строка лога в `cPreviewMaps.cpp`, одно — комментарий в `GameSettings.hpp`.
- `\bfindTexture\b` встречается только в форке и даёт 4 пути, все — именованные выборки HD4.

Причина: исполнитель.

**Н2.** Узкие маркеры.
- `retina-render-state` не видит само исправление коммита `863fc08d`: `src/drawers/SDLDrawer.cpp@6662b2f:502` (`if (state.logicalWidth == 0 || state.logicalHeight == 0)`). Его совпадения идут от переделки `renderTargetStack`.
- `interaction-refresh`: файл `src/gamestates/AdvancedOptionsHeaderLayout.hpp` целиком добавлен коммитом `45f81e3a` («Fix reentrant settings refresh and command latching»), но отнесён к `adaptive-layout` и `controls-tab`. Маркер не содержит `requestOptionsPage`, `ActiveCommandMode`, `PointerMoveCommandPolicy` и `RightClickCommandPolicy` с заглавной буквы, а также `interaction_regression_tests` из `CMakeLists.txt`. Остальные файлы коммитов `45f81e3a` и `05048ffb` маркер находит. Шаг тот же (Б10).
- `credits-art`: пропусков нет. Весь код функции — в `cCreditsState.cpp` и `.h`, оба пойманы; `src/data/` форк не менял.
- `starport-orders`: пропущен только `OrderButtonPolicy` (см. С3).
- В целом у 46 путей кода около 85 отнесений не подтверждены ни одним маркером (`hd-render` 25, `hd4-assets` 21, `adaptive-layout` 9 и т. д.). Тест 6 их не проверяет. Пример лишнего владельца из этого круга: `src/player/cPlayer.h` получил `hd-render`, хотя в диффе только `friend class SaveGameManager`, `m_hdTextureReferences` и поля предупреждения о враге (`@6662b2f:491`, `:543`, `:566–567`). Кода `hd-render` там нет.

Причина: исполнитель.

**Н3.** `src/utils/HdUiTextureLoader.cpp` после снятия `hd-render` остался только в `graphics-modes` (шаг Б3). При этом он вызывает конструктор `Texture` с плотностью (`@6662b2f:20`, `:33–34`), а этот конструктор — код `hd-render` (`src/include/Texture.hpp@6662b2f:21`, шаг Б4). У `graphics-modes` `depends_on` пуст, поэтому обратная зависимость Б3 → Б4 нигде не видна. Нужно записать её в карте или в `depends_on`. Причина: исполнитель.

**Н4.** Тест 6 по устройству ловит только недостающих владельцев. Лишние владельцы и отнесения без подтверждения маркером он не проверяет, поэтому С1–С3 и прошли. Причина: задание.

**Н5.** В рабочей копии лежит `tools/upstream/tests/__pycache__/test_port_inventory.cpython-313.pyc` (создан в 22:08:33, во время работы исполнителя). Тесты запускали без `PYTHONDONTWRITEBYTECODE`. Файл скрыт правилом `.gitignore:34`, в `git status` его нет. Причина: исполнитель.

Замечание ведущему (не находка): в `check3.out` выведены только первые 60 изменившихся путей, поэтому в брифе «около 40». На деле снятые функции есть у 79 путей кода, это 132 пары. Ещё `check3.py` берёт ключ переименования `source`, а в JSON он называется `source_path`. На результат это не влияет: переименованных путей кода у форка нет.

## Ответы по пунктам

### 1. Снятые владельцы

Проверены все 79 путей `src/`, `tests/` и `CMakeLists.txt` со снятыми функциями (132 пары) по `git diff -U0 e17379ad 6662b2f4 -- <путь>`, а не выборка. Неверна одна пара: `src/cGame.h` — `localization` (С1). Остальные снятия верны, спорные помечены.

Четыре пути вне кода тоже проверены, снятия верны:
- три WAV брифинга потеряли `localization`, теперь у них `music-pools` (пункт 4 `answer-02`);
- `tools/export_music.py` потерял `hd4-assets`: это выгрузка музыки из `sdl_audio.dat`, теперь у него `music-pools`.

В столбце «строка диффа» — характерная добавленная строка `FORK`. Она показывает, чей код в диффе на самом деле.

| путь | снятая функция | вердикт | строка диффа |
|---|---|---|---|
| `src/cGame.h` | localization | **неверно** (С1) | `src/cGame.h@6662b2f:353` `Texture *m_hdVictoryRu = nullptr;` (и :354–356 En/Ru) |
| `src/cGame.h` | adaptive-layout | верно (спорно) | `src/cGame.h@6662b2f:402` `void drawOutcomeScreen(bool victory);` — раскладка в cGame_logic.cpp |
| `src/controls/CommandBindings.hpp` | controls-tab | верно | `src/controls/CommandBindings.hpp@6662b2f:18` `struct CommandBindings {` |
| `src/controls/cGameControlsContext.cpp` | interaction-refresh, music-pools, save-slots | верно: только панель приказов | `src/controls/cGameControlsContext.cpp@6662b2f:55` `m_mouseCell = MOUSECELL_COMMAND_BAR;` |
| `src/controls/cGameControlsContext.h` | interaction-refresh, music-pools, save-slots | верно: только панель приказов | `src/controls/cGameControlsContext.h@6662b2f:91` `void activateMoveCommand();` |
| `src/controls/mousestates/cMouseNormalState.h` | interaction-refresh | верно: коммиты 45f81e3a и 05048ffb этот файл не трогали | `src/controls/mousestates/cMouseNormalState.h@6662b2f:48` `void setRallyPointCommandMode();` |
| `src/controls/mousestates/cMouseUnitsSelectedState.h` | interaction-refresh | верно: коммиты 45f81e3a и 05048ffb этот файл не трогали | `src/controls/mousestates/cMouseUnitsSelectedState.h@6662b2f:49` `void setCommandState(eMouseUnitsSelectedState newState);` |
| `src/drawers/CommandBarLayout.hpp` | hd-render | верно | `src/drawers/CommandBarLayout.hpp@6662b2f:8` `struct CommandBarLayout {` |
| `src/drawers/CommandBarPolicy.hpp` | hd-render | верно | `src/drawers/CommandBarPolicy.hpp@6662b2f:13` `isRepairCommandEnabled()` |
| `src/drawers/CreditsDrawer.cpp` | hd4-assets | верно | `src/drawers/CreditsDrawer.cpp@6662b2f:194` `const cRectangle &rect = layout.credits;` |
| `src/drawers/CreditsDrawer.h` | hd4-assets, localization | верно | `src/drawers/CreditsDrawer.h@6662b2f:34` `cTextDrawer *m_gameTextDrawer;` |
| `src/drawers/OrderButtonPolicy.hpp` | hd-render, interaction-refresh | верно; но оставшийся владелец command-bar тоже неверен — находка С3 | `src/drawers/OrderButtonPolicy.hpp@6662b2f:3` `constexpr bool shouldDrawOrderLabelShadow()` |
| `src/drawers/TerrainVariation.hpp` | hd-render | верно | `src/drawers/TerrainVariation.hpp@6662b2f:25` `inline int hdTerrainVariantIndex(int cellId, int terrainType)` |
| `src/drawers/cCommandBarDrawer.h` | hd-render, localization | верно | `src/drawers/cCommandBarDrawer.h@6662b2f:15` `class cCommandBarDrawer {` |
| `src/drawers/cMessageDrawer.cpp` | localization | верно | `src/drawers/cMessageDrawer.cpp@6662b2f:48` `const MusicControlsLayout music = MusicControlsLayout::create(` |
| `src/drawers/cMessageDrawer.h` | hd-render, localization | верно | `src/drawers/cMessageDrawer.h@6662b2f:42` `std::string getMessage() const {` |
| `src/drawers/cMiniMapDrawer.cpp` | hd-render | верно | `src/drawers/cMiniMapDrawer.cpp@6662b2f:41` `? hud.radarViewport` |
| `src/drawers/cMouseDrawer.cpp` | hd-render | верно | `src/drawers/cMouseDrawer.cpp@6662b2f:175` `localization::format("Sight: {}"` |
| `src/drawers/cTextTextureCache.h` | localization | верно | `src/drawers/cTextTextureCache.h@6662b2f:34` `TextInkBounds inkBounds;` |
| `src/gameobjects/particles/cParticle.cpp` | hd4-assets | верно: SDL_BLENDMODE_ADD по старому флагу usesAdditiveBlending — рендер, не HD4 | `src/gameobjects/particles/cParticle.cpp@6662b2f:123` `const float worldScale = game.getWorldScaleFactor();` |
| `src/gameobjects/particles/cParticle.h` | hd4-assets | верно | `src/gameobjects/particles/cParticle.h@6662b2f:106` `cRectangle getVisualRectangle();` |
| `src/gameobjects/projectiles/bullet.cpp` | hd4-assets | верно | `src/gameobjects/projectiles/bullet.cpp@6662b2f:96` `originalSize * game.getWorldScaleFactor()` |
| `src/gameobjects/structures/cAbstractStructure.cpp` | command-bar, faction-tint-terrain, save-slots | верно | `src/gameobjects/structures/cAbstractStructure.cpp@6662b2f:914` `cRectangle cAbstractStructure::getVisualRectangle()` |
| `src/gameobjects/structures/cAbstractStructure.h` | command-bar, faction-tint-terrain | верно | `src/gameobjects/structures/cAbstractStructure.h@6662b2f:26` `friend class SaveGameManager;` |
| `src/gameobjects/structures/cHeavyFactory.cpp` | localization | верно | `src/gameobjects/structures/cHeavyFactory.cpp@6662b2f:93` `getVisualRectangle()` |
| `src/gameobjects/structures/cLightFactory.cpp` | localization | верно | `src/gameobjects/structures/cLightFactory.cpp@6662b2f:71` `gfxdata->findTexture("BUILD_LIGHTFACTORY_PRODUCTION");` |
| `src/gameobjects/structures/cOrderProcesser.cpp` | save-slots | верно | `src/gameobjects/structures/cOrderProcesser.cpp@6662b2f:39` `return orderedItems.takeNext();` |
| `src/gameobjects/structures/cOrderProcesser.h` | save-slots | верно | `src/gameobjects/structures/cOrderProcesser.h@6662b2f:66` `StarportOrderQueue<kMaxItemsToOrder> orderedItems;` |
| `src/gameobjects/structures/cWindTrap.cpp` | hd-render | верно | `src/gameobjects/structures/cWindTrap.cpp@6662b2f:105` `localization::format("{}; output {}%"` |
| `src/gameobjects/units/cUnit.cpp` | command-bar, save-slots | верно | `src/gameobjects/units/cUnit.cpp@6662b2f:532` `cRectangle cUnit::getVisualRectangle()` |
| `src/gameobjects/units/cUnit.h` | command-bar | верно | `src/gameobjects/units/cUnit.h@6662b2f:449` `friend class SaveGameManager;` |
| `src/gamestates/AdvancedOptionsHeaderLayout.hpp` | localization | верно | `src/gamestates/AdvancedOptionsHeaderLayout.hpp@6662b2f:7` `struct AdvancedOptionsHeaderLayout {` |
| `src/gamestates/CampaignMapLayout.hpp` | localization | верно | `src/gamestates/CampaignMapLayout.hpp@6662b2f:8` `struct CampaignMapLayout {` |
| `src/gamestates/OptionsMenuLayout.hpp` | localization | верно | `src/gamestates/OptionsMenuLayout.hpp@6662b2f:7` `struct OptionsMenuLayout {` |
| `src/gamestates/cChooseHouseState.h` | localization | верно | `src/gamestates/cChooseHouseState.h@6662b2f:59` `void drawHdBackground() const;` |
| `src/gamestates/cCreditsState.h` | adaptive-layout, localization | верно | `src/gamestates/cCreditsState.h@6662b2f:49` `Texture *m_teamBmp = nullptr;` |
| `src/gamestates/cGameState.h` | adaptive-layout, localization | верно | `src/gamestates/cGameState.h@6662b2f:47` `virtual void onTextInput(std::string_view) {}` |
| `src/gamestates/cMainMenuState.h` | localization | верно | `src/gamestates/cMainMenuState.h@6662b2f:56` `std::unique_ptr<SaveSlotsDialog> m_saveDialog;` |
| `src/gamestates/cOptionsState.cpp` | music-pools | верно: только синхронизация старого флага playMusic и перекладка старых контролов громкости | `src/gamestates/cOptionsState.cpp@6662b2f:468` `m_selectedSettings.playMusic = m_ctx->getSoundPlayer()->getMusicEnabled();` |
| `src/gamestates/cOptionsState.h` | music-pools | верно | `src/gamestates/cOptionsState.h@6662b2f:79` `std::optional<CommandBindingAction> m_bindingCapture;` |
| `src/gamestates/cSelectMissionState.h` | localization | верно | `src/gamestates/cSelectMissionState.h@6662b2f:31` `Texture *m_hdBackground = nullptr;` |
| `src/gamestates/cSelectYourNextConquestState.h` | localization | верно | `src/gamestates/cSelectYourNextConquestState.h@6662b2f:147` `CampaignMapLayout m_hdCampaignLayout;` |
| `src/gamestates/cSetupSkirmishState.h` | localization | верно | `src/gamestates/cSetupSkirmishState.h@6662b2f:81` `int m_playerRowHeight = 22;` |
| `src/gui/GuiButton.cpp` | localization | верно | `src/gui/GuiButton.cpp@6662b2f:60` `case REMASTER_BUTTON: {` |
| `src/gui/GuiButton.h` | localization | верно | `src/gui/GuiButton.h@6662b2f:17` `float textScale = 1.0F;` |
| `src/gui/GuiCheckBox.cpp` | adaptive-layout, localization | верно (adaptive-layout — спорно: стиль HD-кнопок) | `src/gui/GuiCheckBox.cpp@6662b2f:33` `case REMASTER_BUTTON:` |
| `src/gui/GuiLabel.cpp` | adaptive-layout, localization | верно | `src/gui/GuiLabel.cpp@6662b2f:53` `void GuiLabel::setText(const std::string &value)` |
| `src/gui/GuiLabel.hpp` | adaptive-layout, localization | верно | `src/gui/GuiLabel.hpp@6662b2f:33` `void setText(const std::string &value);` |
| `src/gui/GuiObject.h` | adaptive-layout, localization | верно (adaptive-layout — спорно: стиль HD-кнопок) | `src/gui/GuiObject.h@6662b2f:13` `REMASTER_BUTTON = 5` |
| `src/gui/GuiTheme.hpp` | adaptive-layout, localization | верно (adaptive-layout — спорно: тема HD-кнопок) | `src/gui/GuiTheme.hpp@6662b2f:44` `static GuiTheme Remaster() {` |
| `src/include/definitions.h` | hd-render | верно | `src/include/definitions.h@6662b2f:7` `#define MOUSECELL_COMMAND_BAR -4` |
| `src/main.cpp` | graphics-modes, hd-render, localization | верно | `src/main.cpp@6662b2f:33` `void useExecutableDirectoryAsWorkingDirectory()` |
| `src/managers/cDrawManager.h` | hd-render, localization | верно | `src/managers/cDrawManager.h@6662b2f:106` `void drawMusicControls(int left, int right, bool hd);` |
| `src/map/cMap.h` | hd-render | верно | `src/map/cMap.h@6662b2f:542` `friend class SaveGameManager;` |
| `src/map/cPreviewMaps.cpp` | hd-render | верно | `src/map/cPreviewMaps.cpp@6662b2f:207` `localization::isEnglish() ? "skirmish_en" : "skirmish"` |
| `src/mentat/AbstractMentat.h` | localization | верно | `src/mentat/AbstractMentat.h@6662b2f:147` `bool m_adaptiveHdLayout = false;` |
| `src/mentat/AtreidesMentat.h` | localization | верно | `src/mentat/AtreidesMentat.h@6662b2f:15` `void clearHdMovieOpening(Texture *background) override;` |
| `src/mentat/OrdosMentat.h` | localization | верно | `src/mentat/OrdosMentat.h@6662b2f:14` `void clearHdMovieOpening(Texture *background) override;` |
| `src/player/cPlayer.cpp` | command-bar, save-slots | верно | `src/player/cPlayer.cpp@6662b2f:278` `? gfxdata->getHouseTexture(` |
| `src/player/cPlayer.h` | command-bar | верно | `src/player/cPlayer.h@6662b2f:543` `bool m_hdTextureReferences = false;` |
| `src/sidebar/cBuildingList.cpp` | command-bar, localization, save-slots, starport-orders | верно | `src/sidebar/cBuildingList.cpp@6662b2f:256` `return cRectangle::isWithin(` |
| `src/sidebar/cBuildingList.h` | command-bar, localization, save-slots, starport-orders | верно | `src/sidebar/cBuildingList.h@6662b2f:82` `int getButtonWidth() const {` |
| `src/sidebar/cBuildingListFactory.cpp` | command-bar, localization, save-slots, starport-orders | верно | `src/sidebar/cBuildingListFactory.cpp@6662b2f:67` `widthOfButtonIncludingMargin = layout.tabs.getWidth() / 6;` |
| `src/sidebar/cBuildingListItem.cpp` | adaptive-layout, command-bar, save-slots, starport-orders | верно | `src/sidebar/cBuildingListItem.cpp@6662b2f:387` `msg = localization::format("${} \| {} \| power {} \| {} s"` |
| `src/sidebar/cBuildingListItem.h` | adaptive-layout, command-bar, localization, starport-orders | верно | `src/sidebar/cBuildingListItem.h@6662b2f:256` `friend class SaveGameManager;` |
| `src/sidebar/cBuildingListUpdater.cpp` | adaptive-layout, command-bar, localization, save-slots | верно | `src/sidebar/cBuildingListUpdater.cpp@6662b2f:439` `isStarportCatalogAvailable(` |
| `src/sidebar/cSideBar.cpp` | command-bar, hd-render, localization | верно | `src/sidebar/cSideBar.cpp@6662b2f:413` `void cSideBar::configureLayout(bool hdMode, int logicalWidth)` |
| `src/sidebar/cSideBar.h` | command-bar, hd-render, localization | верно | `src/sidebar/cSideBar.h@6662b2f:98` `static void configureLayout(bool hdMode, int logicalWidth);` |
| `src/utils/GameSettings.hpp` | music-pools | верно | `src/utils/GameSettings.hpp@6662b2f:34` `CommandBindings commandBindings;` |
| `src/utils/HdUiTextureLoader.cpp` | hd-render | верно (вызов API hd-render — зависимость; см. Н3) | `src/utils/HdUiTextureLoader.cpp@6662b2f:14` `Texture *loadHdUiTexture(` |
| `src/utils/HdUiTextureLoader.hpp` | hd-render | верно | `src/utils/HdUiTextureLoader.hpp@6662b2f:7` `Texture *loadHdUiTexture(` |
| `src/utils/cDataPack.cpp` | hd-render | верно | `src/utils/cDataPack.cpp@6662b2f:42` `int DataPack::getIndexFromSurface(SDL_Surface *surface) const` |
| `src/utils/cDataPack.hpp` | hd-render | верно | `src/utils/cDataPack.hpp@6662b2f:46` `int getIndexFromSurface(SDL_Surface *surface) const;` |
| `src/utils/cIniGameRessouces.cpp` | graphics-modes | верно | `src/utils/cIniGameRessouces.cpp@6662b2f:294` `sUnitInfo[RAIDER].bmp = gfxdata->getSurface(UNIT_RAIDER);` |
| `src/utils/cPack.cpp` | hd-render | верно | `src/utils/cPack.cpp@6662b2f:47` `valid = fileInPack.size() == static_cast<std::size_t>(fileInPak);` |
| `src/utils/cPack.h` | hd-render | верно | `src/utils/cPack.h@6662b2f:35` `std::string getNameFromIndex(int index) const;` |
| `src/utils/common.cpp` | adaptive-layout, controls-tab, save-slots | верно | `src/utils/common.cpp@6662b2f:356` `bool saveSettingsToIni(` |
| `src/utils/common.h` | adaptive-layout, command-bar, controls-tab, localization, music-pools, save-slots | верно | `src/utils/common.h@6662b2f:71` `bool saveSettingsToIni(` |
| `tests/CommandBindingsTests.cpp` | controls-tab | верно | `tests/CommandBindingsTests.cpp@6662b2f:14` `setCommandBinding(bindings, CommandBindingAction::Repair, SDL_SCANCODE_F);` |
| `tests/OptionsMenuLayoutTests.cpp` | controls-tab | верно | `tests/OptionsMenuLayoutTests.cpp@6662b2f:15` `bool verifyNoOverlap(const OptionsMenuLayout &layout, bool playing)` |

### 2. Качество маркеров

Слишком общие маркеры, которые ловят чужой код: `m_playMusic` и `"playMusic"` дают ложных владельцев (С2); `OrderButtonPolicy` и `shouldDrawOrderLabelShadow` относят код Starport к панели приказов (С3); остальные маркеры с идентификаторами апстрима перечислены в Н1.

Из примеров брифа:
- `\b(?:language|…)\b` и `\bfindTexture\b` чужой код сейчас не ловят;
- в `HM_|maskIndex|…` совпадает только `maskIndex` в `src/utils/Graphics.cpp`, а `HM_` записан без границы слова.

Узкие маркеры:
- `interaction-refresh`: пропущены `AdvancedOptionsHeaderLayout.hpp` (весь файл из коммита `45f81e3a`) и регистрация теста в CMake (Н2);
- `credits-art`: пропусков нет;
- `starport-orders`: пропущен `OrderButtonPolicy` (С3);
- `retina-render-state` не видит строку самого исправления (Н2).

Кроме того, около 85 отнесений не подтверждены ни одним маркером (Н2, Н4).

### 3. Пункты 1–7 `answer-02.md`

- **1.** Закрыт: все 11 известных случаев записаны в `test_port_inventory.py:35–50` и выполнены.
- **2.** Закрыт по механике: у 174 путей ноль необъяснённых совпадений, `marker_hits` совпадает с независимым пересчётом. По существу же два маркера создали ложных владельцев (С2, С3), а одно снятие неверно (С1).
- **3.** Закрыт. В `PORT_MAP.md:487` и `:726` преемник — `cGamePlaying::onNotifyMouseEvent` (`src/gamestates/cGamePlaying.cpp@a51b97f:304`). На сервере проверено:
  - `:304` — сама функция;
  - `:307` — `pContext->onNotifyMouseEvent(event); // must be first…`;
  - `:310` — `m_mapCamera->onNotifyMouseEvent(event)`.

  Это тот же блок, что `src/managers/cInteractionManager.cpp@e17379ad:85–90`. Упоминания `cGameControlsContext::onNotifyMouseEvent` в карте нет.
- **4.** Закрыт: три WAV брифинга теперь только в `music-pools`.
- **5.** Закрыт: у четырёх инструментов масок есть `faction-tint-terrain`, у `check_skirmish_and_mentat_ui.py` — `localization`, у `command_bar.png`, `command_bar_disabled.png` и двух `source_references/command_bar_*.png` — `command-bar`. `hd4-assets` у всех сохранён.
- **6.** Закрыт: `PORT_MAP.md:728` ссылается на `src/mentat/AbstractMentat.cpp@6662b2f:692`, а этот код читает только `data/scenes/hd4/sdl_{}.dat`. `git grep 'hd4/hd4' 6662b2f4 -- src` ничего не находит.
- **7.** Закрыт: тест 7 есть и зелёный, мои мутации краснеют (пункт 4). Тест 1 пишет во временную папку через `tempfile.TemporaryDirectory()` (`test_port_inventory.py:508`).

Дополнительно, скриптом:
- 206 ссылок `путь@коммит:строка (**символ**)` — все верны;
- 379 строк судьбы в списках функций совпадают со статусом `upstream` в JSON;
- все 41 удалённых пути называют код преемника `@a51b97f`.

### 4. Тесты 6 и 7

Проверки сделаны функциями модуля, как требует задание: `marker_coverage_errors(data, rules, map_text)` и `port_map_errors(data, rules, map_text)`. Известные случаи теста 6 записаны в самом тесте (`EXPECTED_PATH_FEATURES`), а не читаются из правил.

Мои мутации, `/tmp/b0-review3/mut.py`, модуль импортирован из рабочей копии с `PYTHONDONTWRITEBYTECODE=1`.

Тест 7:

| мутация | результат |
|---|---|
| исходная карта | 0 ошибок |
| убрана строка пути | 1 ошибка: «`hd-render` … missing=[`src/drawers/cCommandBarDrawer.cpp`]» |
| изменено число каталога (`resources/bin: 1` → `2`) | 1 ошибка |
| добавлен лишний путь | 1 ошибка: «extra=[`src/main.cpp`]» |
| удалён заголовок функции | 5 ошибок |
| заголовок функции продублирован | 1 ошибка |
| испорчена строка чисел | 1 ошибка |
| изменён только текст судьбы | 0 ошибок — задание этого и не требует; судьбы я сверил скриптом |

Тест 6:

| мутация | результат |
|---|---|
| исходные данные | 0 ошибок |
| у `cMessageDrawer.cpp` снят `music-pools` | 1 ошибка «not explained» |
| добавлен маркер, который ничего не находит | 1 ошибка |
| испорчен `marker_hits` у `src/main.cpp` | 1 ошибка |
| исключение без совпадения | 1 ошибка |
| у `cMainMenuState.cpp` снят `save-slots` | проверка известных случаев срабатывает |

Ограничение теста 6 — в Н4.

### 5. Рамка

`git status --short --untracked-files=all` показывает ровно пять путей: `docs/upstream/PORT_MAP.md`, `docs/upstream/port_inventory.json`, `tools/upstream/port_features.json`, `tools/upstream/port_inventory.py`, `tools/upstream/tests/test_port_inventory.py`. Скрытые правилами `.tmp/` и `tools/upstream/tests/__pycache__/` — см. Н5. Мутационный скрипт лежит в `.tmp/mutate_map.py`, в репозиторий не входит. Размер карты — 75 768 байт.
