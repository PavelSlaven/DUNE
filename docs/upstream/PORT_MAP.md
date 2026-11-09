# Карта переноса функций RU/HD

BASE = e17379ad660fca46859b403a6c3d33ec8d831a40; FORK = 9208dcf5a358f40afd95c99480e4e09f781ed566; UP1 = d06f2fcd2a347182c3774fb96e9a85570405c489. Общий предок FORK и UP1 проверен командой git merge-base и равен BASE. Источники функций — README_AI и перечисленные в инвентаре коммиты FORK; полная связь путей с функциями хранится только в `tools/upstream/port_features.json` и `docs/upstream/port_inventory.json`.

Правила относят код по точным путям и glob из реестра. `marker_hits` фиксирует совпадения маркеров в добавленных и удалённых строках BASE..FORK1; каждое совпадение должно объясняться включённой функцией, её зависимостью либо мотивированным исключением. Тест карты сверяет пути, числа и совпадения с Git и инвентарём.

В судьбе пути «не менялся» означает отсутствие изменения BASE..UP1; файл, созданный только в FORK1, может отсутствовать в UP1. В записях Git rename отражён обеими границами одного перемещения. Класс функции показывает требуемый способ переноса её кода; данные и отдельные модули при этом могут переноситься иначе.

## Функции форка

| id | Название | Источник | Класс | Зависимости | Шаги | paths_count |
|---|---|---|---|---|---|---:|
| graphics-modes | Загрузка HD4 (классический режим удалён) | README_AI §1 | rewrite | нет | Б3 | 71 |
| hd4-assets | Единый комплект HD4: интерфейс, сцены, здания, юниты и эффекты | README_AI §1 | rewrite | graphics-modes | Б3, Б6, Б11 | 2884 |
| hd-render | Физический HD-рендер интерфейса и мира | README_AI §1 | rewrite | graphics-modes | Б4 | 88 |
| world-scale | Масштаб мира как стартовый зум камеры и HD-кадры юнитов | fork_commits | rewrite | hd-render | Б4 | 51 |
| retina-render-state | Восстановление состояния рендера на Retina | fork_commits | reapply | hd-render | Б4 | 4 |
| adaptive-layout | Адаптивные меню и HUD | README_AI §1 | rewrite | hd-render | Б5 | 62 |
| ui-audit | Режим отладки интерфейса | fork_commits | rewrite | adaptive-layout | Б5 | 65 |
| faction-tint-terrain | Маски цвета Дома и вариации поверхности | fork_commits | rewrite | hd-render, hd4-assets | Б6 | 20 |
| localization | Единая русская/английская сборка и переключение языка | README_AI §1 | rewrite | adaptive-layout | Б7 | 191 |
| save-slots | Десять именованных сохранений и F5/F9 | README_AI §1 | rewrite | adaptive-layout, localization | Б8 | 25 |
| music-pools | Музыкальные пулы, история и переключение треков | README_AI §1 | rewrite | adaptive-layout, localization | Б9 | 42 |
| command-bar | Бронзовая панель приказов и настраиваемые клавиши | README_AI §1 | rewrite | adaptive-layout, localization | Б10 | 38 |
| controls-tab | Вкладка управления в расширенных настройках | README_AI §1 | rewrite | command-bar | Б10 | 9 |
| interaction-refresh | Повторный вход в настройки, фиксация приказов и доступность ремонта | fork_commits | rewrite | command-bar, controls-tab | Б10 | 13 |
| starport-orders | Сохранение значения заказа Starport и закрытие потерянного каталога | fork_commits | rewrite | command-bar | Б10 | 7 |
| placement-rule | Единое правило размещения зданий | fork_commits | rewrite | hd-render | Б8а | 7 |
| refinery-dock | Стыковка Харвестера в центре площадки НПЗ | fork_commits | reapply | hd4-assets | Б8а | 8 |
| factory-pads | Площадки заводов: выезд юнитов, очередь, перевозчик, мигание, раздел сохранения FACTORYPADS | fork_commits | rewrite | hd4-assets, save-slots | Б8а | 24 |
| radar-dish | Тарелка Командного поста на 32 кадрах | fork_commits | rewrite | hd4-assets | Б8а | 10 |
| credits-art | Художественные изображения титров | README_AI §1 | rewrite | hd4-assets, localization | Б11 | 5 |
| release-packaging | Сборки и публикация Windows, Linux и macOS | fork_commits | reapply | save-slots, music-pools, interaction-refresh, credits-art | Б12 | 14 |
| author-gallery | Авторское приветствие, галерея и паспорт форка | fork_commits | reapply | release-packaging | Б12 | 7 |
| process-docs | Документы и инструменты процесса форка: задания, решения, карта переноса | fork_commits | reapply | нет | Б14 | 385 |

### graphics-modes — Загрузка HD4 (классический режим удалён)

Перенести загрузку HD4 и применение графических настроек.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/context/ContextCreator.cpp` — изменён
- `src/context/ContextCreator.hpp` — изменён
- `src/drawers/CreditsDrawer.cpp` — изменён
- `src/drawers/CreditsDrawer.h` — изменён
- `src/drawers/cBuildingListDrawer.cpp` — изменён
- `src/drawers/cBuildingListDrawer.h` — изменён
- `src/drawers/cCommandBarDrawer.cpp` — отсутствует
- `src/drawers/cMapDrawer.cpp` — изменён
- `src/drawers/cMessageDrawer.cpp` — изменён
- `src/drawers/cMiniMapDrawer.cpp` — изменён
- `src/drawers/cMiniMapDrawer.h` — изменён
- `src/drawers/cSideBarDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.h` — изменён
- `src/drawers/cStructureDrawer.cpp` — изменён
- `src/gameobjects/units/cUnit.cpp` — изменён
- `src/gamestates/OptionsMenuLayout.hpp` — отсутствует
- `src/gamestates/cChooseHouseState.cpp` — изменён
- `src/gamestates/cChooseHouseState.h` — изменён
- `src/gamestates/cCreditsState.cpp` — изменён
- `src/gamestates/cMainMenuState.cpp` — изменён
- `src/gamestates/cMainMenuState.h` — изменён
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `src/gamestates/cSelectMissionState.cpp` — изменён
- `src/gamestates/cSelectMissionState.h` — изменён
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён
- `src/gamestates/cSelectYourNextConquestState.h` — изменён
- `src/gamestates/cSetupSkirmishState.cpp` — изменён
- `src/gamestates/cSetupSkirmishState.h` — изменён
- `src/managers/cDrawManager.cpp` — изменён
- `src/managers/cDrawManager.h` — изменён
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`
- `src/mentat/AtreidesMentat.cpp` — удалён
- `src/mentat/BeneMentat.cpp` — удалён
- `src/mentat/HarkonnenMentat.cpp` — удалён
- `src/mentat/OrdosMentat.cpp` — удалён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/sidebar/HudLayout.hpp` — отсутствует
- `src/sidebar/MusicControlsLayout.hpp` — отсутствует
- `src/sidebar/cBuildingListFactory.cpp` — изменён
- `src/sidebar/cSideBar.cpp` — изменён
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`
- `src/utils/HdPresentation.hpp` — отсутствует
- `src/utils/HdUiTextureLoader.cpp` — отсутствует
- `src/utils/HdUiTextureLoader.hpp` — отсутствует
- `src/utils/WorldScale.cpp` — отсутствует
- `src/utils/WorldScale.hpp` — отсутствует
- `src/utils/cDataPack.cpp` — изменён
- `src/utils/cDataPack.hpp` — изменён
- `src/utils/cPack.cpp` — изменён
- `src/utils/cPack.h` — изменён
- `src/utils/common.cpp` — изменён
- `src/utils/common.h` — изменён
- `tests/HdPresentationTests.cpp` — отсутствует
- `tests/HudLayoutTests.cpp` — отсутствует
- `tests/MusicControlsLayoutTests.cpp` — отсутствует
- `tests/OptionsMenuLayoutTests.cpp` — отсутствует
- `tests/UnitDrawRegressionTests.cpp` — отсутствует
- `tests/UnitFrameFixture.cpp` — отсутствует
- `tests/UnitFrameInteractionsTests.cpp` — отсутствует
- `tests/WorldScaleTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: корень: 3; .github/workflows: 1; docs: 1; resources/bin: 1

### hd4-assets — Единый комплект HD4: интерфейс, сцены, здания, юниты и эффекты

Перенести комплект HD4 и инструменты его сборки, затем подключить ресурсы к загрузчику.

Пути кода и тестов; судьба в UP1:

- `src/drawers/cBuildingListDrawer.cpp` — изменён
- `src/drawers/cMapDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.h` — изменён
- `src/drawers/cStructureDrawer.cpp` — изменён
- `src/drawers/cStructureDrawer.h` — изменён
- `src/gameobjects/structures/cLightFactory.cpp` — изменён
- `src/gamestates/cChooseHouseState.cpp` — изменён
- `src/gamestates/cChooseHouseState.h` — изменён
- `src/gamestates/cCreditsState.cpp` — изменён
- `src/gamestates/cCreditsState.h` — изменён
- `src/gamestates/cMainMenuState.cpp` — изменён
- `src/gamestates/cMainMenuState.h` — изменён
- `src/gamestates/cSelectMissionState.cpp` — изменён
- `src/gamestates/cSelectMissionState.h` — изменён
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён
- `src/gamestates/cSelectYourNextConquestState.h` — изменён
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`
- `src/mentat/AtreidesMentat.cpp` — удалён
- `src/mentat/AtreidesMentat.h` — удалён
- `src/mentat/BeneMentat.cpp` — удалён
- `src/mentat/HarkonnenMentat.cpp` — удалён
- `src/mentat/OrdosMentat.cpp` — удалён
- `src/mentat/OrdosMentat.h` — удалён
- `src/utils/Graphics.cpp` — изменён
- `src/utils/Graphics.hpp` — изменён
- `src/utils/cDataPack.cpp` — изменён
- `src/utils/cDataPack.hpp` — изменён
- `src/utils/cIniGameRessouces.cpp` — удалён
- `src/utils/cPack.cpp` — изменён
- `src/utils/cPack.h` — изменён

Остальные пути по каталогу второго уровня: resources/bin: 49; resources/hd: 1723; tools: 209; tools/building_angle: 1; tools/ui-audit: 17; tools/units3d: 53; units-gen/UNIT_DEVIATOR: 24; units-gen/UNIT_HARVESTER: 104; units-gen/UNIT_LAUNCHER: 48; units-gen/UNIT_MCV: 24; units-gen/UNIT_QUAD: 24; units-gen/UNIT_SABOTEUR: 108; units-gen/UNIT_SIEGEBASE: 24; units-gen/UNIT_SIEGETOP: 24; units-gen/UNIT_SINGLEFREMEN: 108; units-gen/UNIT_SOLDIER: 108; units-gen/UNIT_SONICTANK: 24; units-gen/UNIT_TANKBASE: 24; units-gen/UNIT_TANKTOP: 24; units-gen/UNIT_TRIKE: 24; units-gen/UNIT_TROOPER: 108

### hd-render — Физический HD-рендер интерфейса и мира

Перенести физический HD-рендер интерфейса и мира в текущий цикл отрисовки.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/context/ContextCreator.cpp` — изменён
- `src/context/ContextCreator.hpp` — изменён
- `src/context/TextContext.cpp` — изменён
- `src/context/TextContext.hpp` — изменён
- `src/drawers/CreditsDrawer.cpp` — изменён
- `src/drawers/CreditsDrawer.h` — изменён
- `src/drawers/SDLDrawer.cpp` — изменён
- `src/drawers/SDLDrawer.hpp` — изменён
- `src/drawers/cBuildingListDrawer.cpp` — изменён
- `src/drawers/cBuildingListDrawer.h` — изменён
- `src/drawers/cCommandBarDrawer.cpp` — отсутствует
- `src/drawers/cMapDrawer.cpp` — изменён
- `src/drawers/cMessageDrawer.cpp` — изменён
- `src/drawers/cOrderDrawer.cpp` — изменён
- `src/drawers/cOrderDrawer.h` — изменён
- `src/drawers/cSideBarDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.h` — изменён
- `src/drawers/cStructureDrawer.cpp` — изменён
- `src/drawers/cStructureDrawer.h` — изменён
- `src/drawers/cTextDrawer.cpp` — изменён
- `src/drawers/cTextDrawer.h` — изменён
- `src/drawers/cTextTextureCache.cpp` — изменён
- `src/drawers/cTextTextureCache.h` — изменён
- `src/gameobjects/particles/cParticle.cpp` — изменён
- `src/gameobjects/particles/cParticle.h` — изменён
- `src/gameobjects/projectiles/bullet.cpp` — изменён
- `src/gameobjects/structures/cAbstractStructure.cpp` — изменён
- `src/gameobjects/structures/cAbstractStructure.h` — изменён
- `src/gameobjects/structures/cHeavyFactory.cpp` — изменён
- `src/gameobjects/structures/cLightFactory.cpp` — изменён
- `src/gameobjects/units/cUnit.cpp` — изменён
- `src/gameobjects/units/cUnit.h` — изменён
- `src/gamestates/cChooseHouseState.cpp` — изменён
- `src/gamestates/cChooseHouseState.h` — изменён
- `src/gamestates/cCreditsState.cpp` — изменён
- `src/gamestates/cMainMenuState.cpp` — изменён
- `src/gamestates/cMainMenuState.h` — изменён
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `src/gamestates/cSelectMissionState.cpp` — изменён
- `src/gamestates/cSelectMissionState.h` — изменён
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён
- `src/gamestates/cSelectYourNextConquestState.h` — изменён
- `src/gamestates/cSetupSkirmishState.cpp` — изменён
- `src/gamestates/cSetupSkirmishState.h` — изменён
- `src/gui/GuiButton.cpp` — изменён
- `src/gui/GuiButton.h` — изменён
- `src/gui/GuiCheckBox.cpp` — изменён
- `src/gui/GuiLabel.cpp` — изменён
- `src/gui/GuiLabel.hpp` — изменён
- `src/gui/GuiObject.h` — изменён
- `src/gui/GuiTheme.hpp` — изменён
- `src/include/Texture.hpp` — изменён
- `src/managers/cDrawManager.cpp` — изменён
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`
- `src/mentat/AtreidesMentat.cpp` — удалён
- `src/mentat/AtreidesMentat.h` — удалён
- `src/mentat/BeneMentat.cpp` — удалён
- `src/mentat/HarkonnenMentat.cpp` — удалён
- `src/mentat/OrdosMentat.cpp` — удалён
- `src/mentat/OrdosMentat.h` — удалён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`
- `src/utils/Graphics.cpp` — изменён
- `src/utils/Graphics.hpp` — изменён
- `src/utils/HdPresentation.hpp` — отсутствует
- `src/utils/OutcomeScreenLayout.hpp` — отсутствует
- `src/utils/RenderScale.cpp` — отсутствует
- `src/utils/RenderScale.hpp` — отсутствует
- `src/utils/TextAlignment.hpp` — отсутствует
- `src/utils/WorldObjectScale.hpp` — отсутствует
- `src/utils/WorldScale.cpp` — отсутствует
- `src/utils/WorldScale.hpp` — отсутствует
- `src/utils/cScreenInit.cpp` — удалён
- `src/utils/cScreenInit.h` — удалён
- `src/utils/common.cpp` — изменён
- `src/utils/common.h` — изменён
- `tests/HdPresentationTests.cpp` — отсутствует
- `tests/RenderScaleTests.cpp` — отсутствует
- `tests/RenderTargetStateTests.cpp` — отсутствует
- `tests/WorldObjectScaleTests.cpp` — отсутствует
- `tests/WorldScaleTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: resources/bin: 1

### world-scale — Масштаб мира как стартовый зум камеры и HD-кадры юнитов

Перенести стартовый зум камеры и масштаб HD-кадров юнитов. Коммиты FORK1: ae9c8644, cf757ad7, b460d25e, c8800549, e0a6fa1e, ad96bbbc, 3f130230, c0ec4a37.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/cGame_logic.cpp` — удалён
- `src/controls/cGameControlsContext.cpp` — изменён
- `src/controls/cGameControlsContext.h` — изменён
- `src/drawers/SDLDrawer.cpp` — изменён
- `src/drawers/SDLDrawer.hpp` — изменён
- `src/drawers/cMapDrawer.cpp` — изменён
- `src/drawers/cPlaceItDrawer.cpp` — изменён
- `src/gameobjects/particles/cParticle.cpp` — изменён
- `src/gameobjects/projectiles/bullet.cpp` — изменён
- `src/gameobjects/structures/cAbstractStructure.cpp` — изменён
- `src/gameobjects/units/cUnit.cpp` — изменён
- `src/include/structs.h` — изменён
- `src/map/cMapCamera.cpp` — перемещён в `src/gameobjects/map/cMapCamera.cpp`
- `src/map/cMapCamera.h` — перемещён в `src/gameobjects/map/cMapCamera.h`
- `src/utils/SoundDistance.hpp` — отсутствует
- `src/utils/UnitSpriteLayout.hpp` — отсутствует
- `src/utils/WorldObjectScale.hpp` — отсутствует
- `src/utils/cIniGameRessouces.cpp` — удалён
- `tests/BuildingRectangleTests.cpp` — отсутствует
- `tests/MouseCellRefreshTests.cpp` — отсутствует
- `tests/MouseCellScanTests.cpp` — отсутствует
- `tests/MouseHoverStateTests.cpp` — отсутствует
- `tests/PlacementFrameTests.cpp` — отсутствует
- `tests/SoundDistanceTests.cpp` — отсутствует
- `tests/TerrainTileGapTests.cpp` — отсутствует
- `tests/UnitDrawRecorder.cpp` — отсутствует
- `tests/UnitDrawRecorder.hpp` — отсутствует
- `tests/UnitDrawRegressionTests.cpp` — отсутствует
- `tests/UnitFrameBaseline.hpp` — отсутствует
- `tests/UnitFrameFixture.cpp` — отсутствует
- `tests/UnitFrameFixture.hpp` — отсутствует
- `tests/UnitFrameInteractionsTests.cpp` — отсутствует
- `tests/UnitHdFrameDrawTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует
- `tests/UnitRenderPixelsTests.cpp` — отсутствует
- `tests/UnitSpriteLayoutTests.cpp` — отсутствует
- `tests/UnitTextRecorder.cpp` — отсутствует
- `tests/WorldObjectScaleTests.cpp` — отсутствует
- `tests/ZoomStartTests.cpp` — отсутствует
- `tests/ZoomTestSupport.hpp` — отсутствует

Остальные пути по каталогу второго уровня: codex-direct/U15: 2; docs: 1; docs/units: 2; tools: 2; tools/units3d: 3

### retina-render-state — Восстановление состояния рендера на Retina

Перенести восстановление viewport, масштаба и clip для Retina в текущий SDL-рендерер.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/drawers/SDLDrawer.cpp` — изменён
- `src/drawers/SDLDrawer.hpp` — изменён
- `tests/RenderTargetStateTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: нет

### adaptive-layout — Адаптивные меню и HUD

Перенести геометрию адаптивных меню и HUD, подключив её к экранам.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/cGame_logic.cpp` — удалён
- `src/drawers/CommandBarLayout.hpp` — отсутствует
- `src/drawers/CreditsDrawer.cpp` — изменён
- `src/drawers/CreditsDrawer.h` — изменён
- `src/drawers/cBuildingListDrawer.cpp` — изменён
- `src/drawers/cBuildingListDrawer.h` — изменён
- `src/drawers/cCommandBarDrawer.cpp` — отсутствует
- `src/drawers/cMessageDrawer.cpp` — изменён
- `src/drawers/cMessageDrawer.h` — изменён
- `src/drawers/cMiniMapDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.h` — изменён
- `src/drawers/cTextDrawer.cpp` — изменён
- `src/drawers/cTextTextureCache.cpp` — изменён
- `src/drawers/cTextTextureCache.h` — изменён
- `src/gamestates/AdvancedOptionsHeaderLayout.hpp` — отсутствует
- `src/gamestates/CampaignMapLayout.hpp` — отсутствует
- `src/gamestates/OptionsMenuLayout.hpp` — отсутствует
- `src/gamestates/cChooseHouseState.cpp` — изменён
- `src/gamestates/cChooseHouseState.h` — изменён
- `src/gamestates/cCreditsState.cpp` — изменён
- `src/gamestates/cMainMenuState.cpp` — изменён
- `src/gamestates/cMainMenuState.h` — изменён
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `src/gamestates/cSelectMissionState.cpp` — изменён
- `src/gamestates/cSelectMissionState.h` — изменён
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён
- `src/gamestates/cSelectYourNextConquestState.h` — изменён
- `src/gamestates/cSetupSkirmishState.cpp` — изменён
- `src/gamestates/cSetupSkirmishState.h` — изменён
- `src/gui/GuiButton.cpp` — изменён
- `src/gui/GuiButton.h` — изменён
- `src/managers/cDrawManager.cpp` — изменён
- `src/managers/cDrawManager.h` — изменён
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`
- `src/mentat/AtreidesMentat.cpp` — удалён
- `src/mentat/AtreidesMentat.h` — удалён
- `src/mentat/BeneMentat.cpp` — удалён
- `src/mentat/HarkonnenMentat.cpp` — удалён
- `src/mentat/OrdosMentat.cpp` — удалён
- `src/mentat/OrdosMentat.h` — удалён
- `src/save/SaveSlotsDialog.cpp` — отсутствует
- `src/save/SaveSlotsDialog.hpp` — отсутствует
- `src/sidebar/HudLayout.hpp` — отсутствует
- `src/sidebar/MusicControlsLayout.hpp` — отсутствует
- `src/sidebar/cBuildingList.cpp` — изменён
- `src/sidebar/cBuildingList.h` — изменён
- `src/sidebar/cBuildingListFactory.cpp` — изменён
- `src/sidebar/cSideBar.cpp` — изменён
- `src/sidebar/cSideBar.h` — изменён
- `src/utils/OutcomeScreenLayout.hpp` — отсутствует
- `src/utils/TextAlignment.hpp` — отсутствует
- `tests/CampaignMapLayoutTests.cpp` — отсутствует
- `tests/CommandBarLayoutTests.cpp` — отсутствует
- `tests/HdPresentationTests.cpp` — отсутствует
- `tests/HudLayoutTests.cpp` — отсутствует
- `tests/InteractionRegressionTests.cpp` — отсутствует
- `tests/MusicControlsLayoutTests.cpp` — отсутствует
- `tests/OptionsMenuLayoutTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: нет

### ui-audit — Режим отладки интерфейса

Перенести режим отладки интерфейса, сбор снимков и вспомогательные инструменты. Коммиты FORK1: 87f6beeb, 5c77e8f9.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/audio/MusicController.h` — отсутствует
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/controls/cMouse.h` — изменён
- `src/debug/UiAudit.hpp` — отсутствует
- `src/debug/UiAuditAccess.cpp` — отсутствует
- `src/debug/UiAuditArguments.cpp` — отсутствует
- `src/debug/UiAuditArguments.hpp` — отсутствует
- `src/debug/UiAuditCapture.cpp` — отсутствует
- `src/debug/UiAuditScenes.cpp` — отсутствует
- `src/debug/UiAuditScenes.hpp` — отсутствует
- `src/drawers/cBuildingListDrawer.h` — изменён
- `src/drawers/cCommandBarDrawer.cpp` — отсутствует
- `src/drawers/cCommandBarDrawer.h` — отсутствует
- `src/drawers/cMiniMapDrawer.cpp` — изменён
- `src/drawers/cOrderDrawer.h` — изменён
- `src/drawers/cSideBarDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.h` — изменён
- `src/drawers/cStructureDrawer.cpp` — изменён
- `src/drawers/cTextDrawer.cpp` — изменён
- `src/gameobjects/units/cUnit.cpp` — изменён
- `src/gamestates/cChooseHouseState.cpp` — изменён
- `src/gamestates/cCreditsState.cpp` — изменён
- `src/gamestates/cCreditsState.h` — изменён
- `src/gamestates/cMainMenuState.h` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён
- `src/gamestates/cSelectYourNextConquestState.h` — изменён
- `src/gamestates/cSetupSkirmishState.cpp` — изменён
- `src/gamestates/cSetupSkirmishState.h` — изменён
- `src/gui/GuiButton.cpp` — изменён
- `src/gui/GuiCheckBox.cpp` — изменён
- `src/gui/GuiLabel.cpp` — изменён
- `src/gui/GuiObject.cpp` — изменён
- `src/gui/GuiObject.h` — изменён
- `src/gui/GuiSlider.cpp` — изменён
- `src/gui/GuiWindow.cpp` — изменён
- `src/main.cpp` — изменён
- `src/managers/cDrawManager.cpp` — изменён
- `src/map/cMapCamera.h` — перемещён в `src/gameobjects/map/cMapCamera.h`
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`
- `src/save/SaveSlotsDialog.cpp` — отсутствует
- `src/save/SaveSlotsDialog.hpp` — отсутствует
- `src/utils/cPlatformLayerInit.cpp` — удалён
- `src/utils/cScreenInit.cpp` — удалён
- `tests/UiAuditArgumentsTests.cpp` — отсутствует
- `tests/ui_audit_main_menu_png.py` — отсутствует
- `tests/ui_audit_runtime_support.py` — отсутствует
- `tests/ui_audit_unknown_scene.py` — отсутствует

Остальные пути по каталогу второго уровня: tools/ui-audit: 14

### faction-tint-terrain — Маски цвета Дома и вариации поверхности

Перенести фракционные цветовые маски, вариации поверхности и инструменты.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/drawers/TerrainVariation.hpp` — отсутствует
- `src/drawers/cMapDrawer.cpp` — изменён
- `src/drawers/cStructureDrawer.cpp` — изменён
- `src/drawers/cStructureDrawer.h` — изменён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`
- `src/utils/FactionTint.hpp` — отсутствует
- `src/utils/Graphics.cpp` — изменён
- `src/utils/Graphics.hpp` — изменён
- `src/utils/cDataPack.cpp` — изменён
- `src/utils/cDataPack.hpp` — изменён
- `src/utils/cPack.cpp` — изменён
- `src/utils/cPack.h` — изменён
- `tests/FactionTintTests.cpp` — отсутствует
- `tests/TerrainVariationTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: tools: 4

### localization — Единая русская/английская сборка и переключение языка

Перенести русскую и английскую сборки, переключение языка и локализованные ресурсы.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/context/ContextCreator.cpp` — изменён
- `src/context/ContextCreator.hpp` — изменён
- `src/context/TextContext.cpp` — изменён
- `src/context/TextContext.hpp` — изменён
- `src/controls/CommandBindings.hpp` — отсутствует
- `src/controls/mousestates/cMouseNormalState.cpp` — изменён
- `src/drawers/CreditsDrawer.cpp` — изменён
- `src/drawers/OrderButtonPolicy.hpp` — отсутствует
- `src/drawers/cBuildingListDrawer.cpp` — изменён
- `src/drawers/cCommandBarDrawer.cpp` — отсутствует
- `src/drawers/cMouseDrawer.cpp` — изменён
- `src/drawers/cOrderDrawer.cpp` — изменён
- `src/drawers/cOrderDrawer.h` — изменён
- `src/drawers/cSideBarDrawer.cpp` — изменён
- `src/drawers/cSideBarDrawer.h` — изменён
- `src/drawers/cTextDrawer.cpp` — изменён
- `src/drawers/cTextDrawer.h` — изменён
- `src/drawers/cTextTextureCache.cpp` — изменён
- `src/gameobjects/structures/cAbstractStructure.cpp` — изменён
- `src/gameobjects/structures/cOrderProcesser.cpp` — изменён
- `src/gameobjects/structures/cWindTrap.cpp` — изменён
- `src/gameobjects/units/cUnit.cpp` — изменён
- `src/gamestates/cChooseHouseState.cpp` — изменён
- `src/gamestates/cCreditsState.cpp` — изменён
- `src/gamestates/cMainMenuState.cpp` — изменён
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `src/gamestates/cSelectMissionState.cpp` — изменён
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён
- `src/gamestates/cSetupSkirmishState.cpp` — изменён
- `src/ini.cpp` — удалён
- `src/managers/cDrawManager.cpp` — изменён
- `src/map/cPreviewMaps.cpp` — удалён
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`
- `src/mentat/AtreidesMentat.cpp` — удалён
- `src/mentat/BeneMentat.cpp` — удалён
- `src/mentat/HarkonnenMentat.cpp` — удалён
- `src/mentat/OrdosMentat.cpp` — удалён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/save/SaveFileCodec.cpp` — отсутствует
- `src/save/SaveGameManager.cpp` — отсутствует
- `src/save/SaveSlotName.hpp` — отсутствует
- `src/save/SaveSlotsDialog.cpp` — отсутствует
- `src/sidebar/cBuildingListItem.cpp` — изменён
- `src/utils/FontSupport.hpp` — отсутствует
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`
- `src/utils/Localization.hpp` — отсутствует
- `src/utils/cIniGameRessouces.cpp` — удалён
- `src/utils/common.cpp` — изменён
- `tests/CommandBindingsTests.cpp` — отсутствует
- `tests/FontCoverageTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: resources/bin: 136; tools: 1

### save-slots — Десять именованных сохранений и F5/F9

Перенести именованные слоты сохранений, диалог выбора и команды F5/F9.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/building/cItemBuilder.h` — изменён
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/gameobjects/structures/cAbstractStructure.h` — изменён
- `src/gameobjects/units/cReinforcements.h` — изменён
- `src/gameobjects/units/cUnit.h` — изменён
- `src/gamestates/OptionsMenuLayout.hpp` — отсутствует
- `src/gamestates/cGameState.h` — изменён
- `src/gamestates/cMainMenuState.cpp` — изменён
- `src/gamestates/cMainMenuState.h` — изменён
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `src/map/cMap.h` — перемещён в `src/gameobjects/map/cMap.h`
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`
- `src/save/SaveFileCodec.cpp` — отсутствует
- `src/save/SaveFileCodec.hpp` — отсутствует
- `src/save/SaveGameManager.cpp` — отсутствует
- `src/save/SaveGameManager.hpp` — отсутствует
- `src/save/SaveSlotName.hpp` — отсутствует
- `src/save/SaveSlotsDialog.cpp` — отсутствует
- `src/save/SaveSlotsDialog.hpp` — отсутствует
- `src/sidebar/cBuildingListItem.h` — изменён
- `tests/SaveFileCodecTests.cpp` — отсутствует
- `tests/SaveSlotNameTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: нет

### music-pools — Музыкальные пулы, история и переключение треков

Перенести музыкальные пулы, историю воспроизведения и управление треками.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/audio/MusicController.cpp` — отсутствует
- `src/audio/MusicController.h` — отсутствует
- `src/audio/MusicPlaylist.cpp` — отсутствует
- `src/audio/MusicPlaylist.h` — отсутствует
- `src/audio/MusicTransitionPolicy.hpp` — отсутствует
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/drawers/cMessageDrawer.cpp` — изменён
- `src/managers/cDrawManager.cpp` — изменён
- `src/managers/cDrawManager.h` — изменён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`
- `src/sidebar/MusicControlsLayout.hpp` — отсутствует
- `src/utils/cSoundPlayer.cpp` — изменён
- `src/utils/cSoundPlayer.h` — изменён
- `tests/MusicControlsLayoutTests.cpp` — отсутствует
- `tests/MusicPlaylistTests.cpp` — отсутствует
- `tests/MusicTransitionPolicyTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: resources/bin: 22; tools: 1

### command-bar — Бронзовая панель приказов и настраиваемые клавиши

Перенести бронзовую панель приказов и настраиваемые привязки клавиш.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/context/TextContext.cpp` — изменён
- `src/context/TextContext.hpp` — изменён
- `src/controls/CommandBindings.hpp` — отсутствует
- `src/controls/CommandModePolicy.hpp` — отсутствует
- `src/controls/cGameControlsContext.cpp` — изменён
- `src/controls/cGameControlsContext.h` — изменён
- `src/controls/cKeyboardEvent.h` — изменён
- `src/controls/mousestates/cMouseNormalState.cpp` — изменён
- `src/controls/mousestates/cMouseNormalState.h` — изменён
- `src/controls/mousestates/cMouseRepairState.cpp` — изменён
- `src/controls/mousestates/cMouseUnitsSelectedState.cpp` — изменён
- `src/controls/mousestates/cMouseUnitsSelectedState.h` — изменён
- `src/drawers/CommandBarLayout.hpp` — отсутствует
- `src/drawers/CommandBarPolicy.hpp` — отсутствует
- `src/drawers/cCommandBarDrawer.cpp` — отсутствует
- `src/drawers/cCommandBarDrawer.h` — отсутствует
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `src/include/definitions.h` — изменён
- `src/managers/cDrawManager.cpp` — изменён
- `src/managers/cDrawManager.h` — изменён
- `src/managers/cInteractionManager.cpp` — удалён
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`
- `src/utils/common.cpp` — изменён
- `tests/CommandBarLayoutTests.cpp` — отсутствует
- `tests/CommandBindingsTests.cpp` — отсутствует
- `tests/InteractionRegressionTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: resources/bin: 2; resources/hd: 4; tools: 2

### controls-tab — Вкладка управления в расширенных настройках

Перенести вкладку управления и проверку конфликтов клавиш.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/controls/CommandBindings.hpp` — отсутствует
- `src/controls/cKeyboardEvent.h` — изменён
- `src/gamestates/AdvancedOptionsHeaderLayout.hpp` — отсутствует
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `tests/CommandBindingConflictTests.cpp` — отсутствует
- `tests/CommandBindingsTests.cpp` — отсутствует
- `tests/InteractionRegressionTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: нет

### interaction-refresh — Повторный вход в настройки, фиксация приказов и доступность ремонта

Перенести обновление настроек при повторном входе, фиксацию приказов и доступность ремонта.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/controls/CommandModePolicy.hpp` — отсутствует
- `src/controls/cMouse.h` — изменён
- `src/controls/mousestates/cMouseNormalState.cpp` — изменён
- `src/controls/mousestates/cMouseRepairState.cpp` — изменён
- `src/controls/mousestates/cMouseUnitsSelectedState.cpp` — изменён
- `src/drawers/CommandBarPolicy.hpp` — отсутствует
- `src/drawers/cCommandBarDrawer.cpp` — отсутствует
- `src/gamestates/cOptionsState.cpp` — изменён
- `src/gamestates/cOptionsState.h` — изменён
- `tests/InteractionRegressionTests.cpp` — отсутствует
- `tests/MouseClickInitTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует

Остальные пути по каталогу второго уровня: нет

### starport-orders — Сохранение значения заказа Starport и закрытие потерянного каталога

Перенести сохранение значения заказа Starport и закрытие потерянного каталога.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/gameobjects/structures/StarportOrderQueue.hpp` — отсутствует
- `src/gameobjects/structures/cOrderProcesser.cpp` — изменён
- `src/gameobjects/structures/cOrderProcesser.h` — изменён
- `src/gameobjects/structures/cStarPort.cpp` — изменён
- `src/sidebar/cBuildingListUpdater.cpp` — изменён
- `tests/InteractionRegressionTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: нет

### placement-rule — Единое правило размещения зданий

Перенести общее правило размещения зданий и подключить его к режиму установки, подсказке и проверке игрока. Коммиты FORK1: e7a1c04f, a8a7f49a, 9ea227d2.

Пути кода и тестов; судьба в UP1:

- `src/controls/mousestates/cMousePlaceState.cpp` — изменён
- `src/controls/mousestates/cMousePlaceState.h` — изменён
- `src/drawers/cPlaceItDrawer.cpp` — изменён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`
- `tests/PlacementRuleTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует

Остальные пути по каталогу второго уровня: нет

### refinery-dock — Стыковка Харвестера в центре площадки НПЗ

Перенести стыковку Харвестера в центре площадки НПЗ. Коммиты FORK1: c655ceb6, b6c58b8c.

Пути кода и тестов; судьба в UP1:

- `src/utils/WorldObjectScale.hpp` — отсутствует
- `tests/WorldObjectScaleTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: codex-direct/U23: 4; resources/bin: 1; tools/units3d: 1

### factory-pads — Площадки заводов: выезд юнитов, очередь, перевозчик, мигание, раздел сохранения FACTORYPADS

Перенести площадки заводов: выезд, очередь, перевозчик, мигание и раздел FACTORYPADS. Коммиты FORK1: 223f24c5, e39f6279, ac3c6b7d, e632b5e3, 90da98c4, 7bed86fc, 46b71484, 9e8a65e3, 00d15658, 5c2cda10, 29b3ca76, f2b5811e.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/building/cItemBuilder.cpp` — изменён
- `src/building/cItemBuilder.h` — изменён
- `src/drawers/cStructureDrawer.cpp` — изменён
- `src/gameobjects/structures/FactoryPad.hpp` — отсутствует
- `src/gameobjects/structures/cAbstractStructure.cpp` — изменён
- `src/gameobjects/structures/cAbstractStructure.h` — изменён
- `src/gameobjects/structures/cHeavyFactory.cpp` — изменён
- `src/gameobjects/structures/cHeavyFactory.h` — изменён
- `src/gameobjects/structures/cLightFactory.cpp` — изменён
- `src/gameobjects/structures/cLightFactory.h` — изменён
- `src/gameobjects/structures/cUnitFactory.cpp` — отсутствует
- `src/gameobjects/structures/cUnitFactory.h` — отсутствует
- `src/gameobjects/units/cUnit.cpp` — изменён
- `src/gameobjects/units/cUnit.h` — изменён
- `src/save/SaveGameManager.cpp` — отсутствует
- `src/save/SaveGameManager.hpp` — отсутствует
- `src/utils/cStructureUtils.cpp` — изменён
- `src/utils/cStructureUtils.h` — изменён
- `tests/FactoryPadEngineTests.cpp` — отсутствует
- `tests/FactoryPadSaveTests.cpp` — отсутствует
- `tests/FactoryPadTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует

Остальные пути по каталогу второго уровня: корень: 1

### radar-dish — Тарелка Командного поста на 32 кадрах

Перенести анимацию тарелки Командного поста на 32 кадрах и её ресурсы. Коммиты FORK1: 3d3ff49e, 849650d0.

Пути кода и тестов; судьба в UP1:

- `src/gameobjects/structures/cOutPost.cpp` — изменён
- `tests/OutpostFrameTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует

Остальные пути по каталогу второго уровня: корень: 1; resources/bin: 1; resources/hd: 2; tools/building_angle: 3

### credits-art — Художественные изображения титров

Перенести художественные изображения и разметку титров.

Пути кода и тестов; судьба в UP1:

- `src/gamestates/cCreditsState.cpp` — изменён
- `src/gamestates/cCreditsState.h` — изменён

Остальные пути по каталогу второго уровня: resources/bin: 2; tools: 1

### release-packaging — Сборки и публикация Windows, Linux и macOS

Перенести сборку и публикацию выпусков для Windows, Linux и macOS.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/main.cpp` — изменён

Остальные пути по каталогу второго уровня: корень: 2; .github/workflows: 2; packaging: 4; resources/bin: 4

### author-gallery — Авторское приветствие, галерея и паспорт форка

Перенести авторское приветствие, галерею снимков и паспорт FORK1.

Пути кода и тестов; судьба в UP1:

- нет.

Остальные пути по каталогу второго уровня: корень: 2; docs/screenshots: 5

### process-docs — Документы и инструменты процесса форка: задания, решения, карта переноса

Перенести документы и инструменты процесса форка.

Пути кода и тестов; судьба в UP1:

- нет.

Остальные пути по каталогу второго уровня: codex-direct: 23; codex-direct/A1: 1; codex-direct/B0: 1; codex-direct/G1: 12; codex-direct/G2: 20; codex-direct/G3: 70; codex-direct/U1: 12; codex-direct/U10: 1; codex-direct/U11: 11; codex-direct/U12: 14; codex-direct/U13: 4; codex-direct/U14: 2; codex-direct/U15: 4; codex-direct/U16: 2; codex-direct/U17: 1; codex-direct/U18: 1; codex-direct/U19: 1; codex-direct/U2: 2; codex-direct/U20: 1; codex-direct/U21: 2; codex-direct/U23: 4; codex-direct/U24: 8; codex-direct/U25: 5; codex-direct/U26: 6; codex-direct/U27: 5; codex-direct/U28: 3; codex-direct/U29: 4; codex-direct/U3: 13; codex-direct/U31: 4; codex-direct/U33: 6; codex-direct/U34: 11; codex-direct/U36: 25; codex-direct/U37: 4; codex-direct/U38: 1; codex-direct/U39: 2; codex-direct/U4: 12; codex-direct/U40: 1; codex-direct/U44: 1; codex-direct/U45: 1; codex-direct/U45R: 1; codex-direct/U5: 10; codex-direct/U6: 19; codex-direct/U7: 4; codex-direct/U8: 4; codex-direct/U9: 25; docs: 3; docs/screenshots: 5; docs/units: 5; docs/upstream: 5; tools/upstream: 3

## Реестр тестов форка

В FORK1 43 файла **tests/*.cpp**: 40 отдельных C++-тестов с собственным `main` и три файла поддержки. Для 40 тестов заданы отдельные CTest-имена; две runtime-проверки UI регистрируются опционально. Это реестр исходников и include, тесты не запускались. Столбец include показывает прямые project include: число перед стрелкой — строка include в исходном файле. Регистрации и строки относятся к FORK1.

| C++-файл / main | CTest и регистрация | Покрытие; прямые include |
|---|---|---|
| `tests/BuildingRectangleTests.cpp@9208dcf:75` | `building_visual_rectangle` (`tests/UnitRenderFixture.cmake:126`) | прямоугольники зданий; `1`→`tests/ZoomTestSupport.hpp`; `3`→`src/gameobjects/structures/cRefinery.h`; `4`→`src/gameobjects/structures/cWindTrap.h` |
| `tests/CampaignMapLayoutTests.cpp@9208dcf:6` | `campaign_map_layout_geometry` (`CMakeLists.txt:358`) | панели карты кампании; `1`→`src/gamestates/CampaignMapLayout.hpp` |
| `tests/CommandBarLayoutTests.cpp@9208dcf:3` | `command_bar_layout_geometry` (`CMakeLists.txt:249`) | геометрия панели приказов; `1`→`src/drawers/CommandBarLayout.hpp` |
| `tests/CommandBindingConflictTests.cpp@9208dcf:7` | `command_binding_conflicts` (`CMakeLists.txt:197`) | конфликты сочетаний клавиш; `2`→`src/controls/CommandBindings.hpp`; `3`→`src/controls/cKeyboardEvent.h` |
| `tests/CommandBindingsTests.cpp@9208dcf:7` | `command_bindings` (`CMakeLists.txt:184`) | назначения, SDL scancode и Ctrl; `2`→`src/controls/CommandBindings.hpp`; `3`→`src/controls/cKeyboardEvent.h` |
| `tests/FactionTintTests.cpp@9208dcf:5` | `faction_tint_uniformity` (`CMakeLists.txt:442`) | цветовой канал фракции; `1`→`src/utils/FactionTint.hpp` |
| `tests/FactoryPadEngineTests.cpp@9208dcf:1004` | `factory_pad_engine` (`tests/UnitRenderFixture.cmake:132`) | производство и выезд с factory pads; `1`→`tests/ZoomTestSupport.hpp`; `3`→`tests/UnitDrawRecorder.hpp`; `5`→`src/building/cItemBuilder.h`; `6`→`src/data/gfxdata.h`; `7`→`src/drawers/cStructureDrawer.h`; `8`→`src/gameobjects/structures/cBarracks.h`; `9`→`src/gameobjects/structures/cHeavyFactory.h`; `10`→`src/gameobjects/structures/cLightFactory.h`; `11`→`src/gameobjects/structures/cUnitFactory.h`; `12`→`src/gameobjects/units/cUnit.h`; `13`→`src/map/cMap.h`; `14`→`src/sidebar/cBuildingListItem.h` |
| `tests/FactoryPadSaveTests.cpp@9208dcf:219` | `factory_pad_save` (`tests/UnitRenderFixture.cmake:134`) | сохранение состояния factory pads; `1`→`src/save/SaveFileCodec.hpp`; `2`→`src/save/SaveGameManager.cpp` |
| `tests/FactoryPadTests.cpp@9208dcf:287` | `factory_pad_logic` (`CMakeLists.txt:318`) | очередь и выезд с factory pad; `1`→`src/gameobjects/structures/FactoryPad.hpp` |
| `tests/FontCoverageTests.cpp@9208dcf:9` | `russian_font_coverage` (`CMakeLists.txt:345`) | кириллические глифы настоящего шрифта; `2`→**SDL2/SDL_ttf.h**; `3`→`src/utils/FontSupport.hpp` |
| `tests/HdPresentationTests.cpp@9208dcf:21` | `hd_presentation_selection` (`CMakeLists.txt:329`) | HD-представления и геометрия outcome; `1`→`src/utils/HdPresentation.hpp`; `2`→`src/utils/OutcomeScreenLayout.hpp`; `3`→`src/utils/TextAlignment.hpp` |
| `tests/HudLayoutTests.cpp@9208dcf:47` | `hud_layout_geometry` (`CMakeLists.txt:222`) | геометрия HUD; `1`→`src/sidebar/HudLayout.hpp` |
| `tests/InteractionRegressionTests.cpp@9208dcf:28` | `interaction_regressions` (`CMakeLists.txt:262`) | заголовок настроек и фиксация/отмена приказа; `1`→`src/controls/CommandModePolicy.hpp`; `2`→`src/drawers/CommandBarPolicy.hpp`; `3`→`src/drawers/OrderButtonPolicy.hpp`; `4`→`src/gamestates/AdvancedOptionsHeaderLayout.hpp`; `5`→`src/gameobjects/structures/StarportOrderQueue.hpp` |
| `tests/MouseCellRefreshTests.cpp@9208dcf:167` | `mouse_cell_refresh` (`tests/UnitRenderFixture.cmake:129`) | обновление ячейки под курсором; `1`→`tests/ZoomTestSupport.hpp` |
| `tests/MouseCellScanTests.cpp@9208dcf:214` | `mouse_cell_scan` (`tests/UnitRenderFixture.cmake:128`) | сканирование ячеек под курсором; `1`→`tests/ZoomTestSupport.hpp` |
| `tests/MouseClickInitTests.cpp@9208dcf:11` | `mouse_click_init` (`tests/UnitRenderFixture.cmake:130`) | начальная обработка щелчка мыши; `1`→`src/utils/cSoundPlayer.h`; `2`→`src/utils/cTimeCounter.h`; `3`→`src/utils/cTimeManager.h`; `4`→`src/context/GameContext.hpp`; `5`→`src/context/TextContext.hpp`; `6`→`src/controls/cMouse.h`; `7`→`src/drawers/cTextDrawer.h` |
| `tests/MouseHoverStateTests.cpp@9208dcf:199` | `mouse_hover_state` (`CMakeLists.txt:483`) | переходы состояния наведения; `1`→`tests/ZoomTestSupport.hpp`; `3`→`src/controls/mousestates/cMouseNormalState.h`; `4`→`src/data/gfxdata.h` |
| `tests/MusicControlsLayoutTests.cpp@9208dcf:47` | `music_controls_layout_geometry` (`CMakeLists.txt:431`) | кнопки музыки в HUD; `1`→`src/sidebar/HudLayout.hpp`; `2`→`src/sidebar/MusicControlsLayout.hpp` |
| `tests/MusicPlaylistTests.cpp@9208dcf:22` | `music_playlist_shuffle_history` (`CMakeLists.txt:407`) | shuffle-bag и история треков; `1`→`src/audio/MusicPlaylist.h` |
| `tests/MusicTransitionPolicyTests.cpp@9208dcf:3` | `music_transition_policy` (`CMakeLists.txt:418`) | смена музыкальной категории; `1`→`src/audio/MusicTransitionPolicy.hpp` |
| `tests/OptionsMenuLayoutTests.cpp@9208dcf:283` | `options_menu_layout_geometry` (`CMakeLists.txt:236`) | геометрия меню настроек; `1`→`src/gamestates/OptionsMenuLayout.hpp`; `2`→`src/utils/RenderScale.hpp` |
| `tests/OutpostFrameTests.cpp@9208dcf:10` | `outpost_frame` (`tests/UnitRenderFixture.cmake:133`) | кадры аванпоста; `3`→`src/gameobjects/structures/cOutPost.h` |
| `tests/PlacementFrameTests.cpp@9208dcf:110` | `placement_frame` (`tests/UnitRenderFixture.cmake:127`) | геометрия предпросмотра здания; `1`→`tests/ZoomTestSupport.hpp`; `3`→`tests/UnitDrawRecorder.hpp`; `5`→`src/drawers/cPlaceItDrawer.h`; `6`→`src/gameobjects/structures/cRefinery.h`; `7`→`src/gameobjects/structures/cWindTrap.h`; `8`→`src/sidebar/cBuildingListItem.h` |
| `tests/PlacementRuleTests.cpp@9208dcf:321` | `placement_rule` (`tests/UnitRenderFixture.cmake:131`) | правила размещения зданий; `1`→`tests/ZoomTestSupport.hpp`; `3`→`tests/UnitDrawRecorder.hpp`; `5`→`src/controls/mousestates/cMousePlaceState.h`; `6`→`src/data/gfxdata.h`; `7`→`src/drawers/cPlaceItDrawer.h`; `8`→`src/building/cItemBuilder.h`; `9`→`src/gameobjects/structures/cWindTrap.h`; `10`→`src/player/cPlayer.h`; `11`→`src/sidebar/cBuildingList.h`; `12`→`src/sidebar/cBuildingListUpdater.h`; `13`→`src/sidebar/cSideBar.h` |
| `tests/RenderScaleTests.cpp@9208dcf:33` | `render_scale_calculations` (`CMakeLists.txt:209`) | логический canvas; `1`→`src/utils/RenderScale.hpp` |
| `tests/RenderTargetStateTests.cpp@9208dcf:28` | `render_target_state_restoration` (`CMakeLists.txt:372`) | состояние вложенных render targets; `3`→`src/drawers/SDLDrawer.hpp`; `4`→`src/include/Texture.hpp`; `6`→**SDL2/SDL.h** |
| `tests/SaveFileCodecTests.cpp@9208dcf:23` | `save_file_codec_roundtrip` (`CMakeLists.txt:384`) | кодек и неверные save-заголовки; `1`→`src/save/SaveFileCodec.hpp` |
| `tests/SaveSlotNameTests.cpp@9208dcf:16` | `save_slot_name_handling` (`CMakeLists.txt:395`) | слоты и UTF-8 имя; `1`→`src/save/SaveSlotName.hpp` |
| `tests/SoundDistanceTests.cpp@9208dcf:17` | `sound_distance_scale` (`CMakeLists.txt:296`) | затухание звука по расстоянию; `1`→`src/utils/SoundDistance.hpp` |
| `tests/TerrainTileGapTests.cpp@9208dcf:55` | `terrain_tile_gap` (`CMakeLists.txt:484`) | стыки кадров поверхности; `1`→`tests/ZoomTestSupport.hpp` |
| `tests/TerrainVariationTests.cpp@9208dcf:7` | `terrain_variation_selection` (`CMakeLists.txt:273`) | варианты поверхности и границы; `1`→`src/drawers/TerrainVariation.hpp` |
| `tests/UiAuditArgumentsTests.cpp@9208dcf:44` | `ui_audit_arguments` (`CMakeLists.txt:454`) | аргументы UI-аудита; `1`→`src/debug/UiAuditArguments.hpp` |
| `tests/UnitDrawRegressionTests.cpp@9208dcf:285` | `unit_draw_regression` (`tests/UnitRenderFixture.cmake:123`) | регрессии отрисовки юнитов; `1`→`tests/UnitDrawRecorder.hpp`; `2`→`tests/UnitFrameBaseline.hpp`; `3`→`tests/UnitFrameFixture.hpp`; `6`→`src/data/gfxdata.h`; `7`→`src/map/cMapCamera.h`; `8`→`src/player/cPlayer.h` |
| `tests/UnitFrameInteractionsTests.cpp@9208dcf:335` | `unit_frame_interactions` (`tests/UnitRenderFixture.cmake:122`) | покадровые взаимодействия; `1`→`tests/UnitDrawRecorder.hpp`; `2`→`tests/UnitFrameBaseline.hpp`; `3`→`tests/UnitFrameFixture.hpp`; `5`→`src/utils/cSoundPlayer.h`; `6`→`src/utils/cTimeCounter.h`; `7`→`src/utils/cTimeManager.h`; `8`→`src/context/GameContext.hpp`; `9`→`src/context/TextContext.hpp`; `10`→`src/controls/cGameControlsContext.h`; `11`→`src/controls/cMouse.h`; `12`→`src/data/gfxdata.h`; `14`→`src/drawers/cTextDrawer.h`; `15`→`src/map/cMapCamera.h`; `16`→`src/player/cPlayer.h` |
| `tests/UnitHdFrameDrawTests.cpp@9208dcf:197` | `unit_hd_frame_draw` (`tests/UnitRenderFixture.cmake:121`) | выбор HD-кадров юнитов; `1`→`tests/UnitDrawRecorder.hpp`; `2`→`tests/UnitFrameBaseline.hpp`; `3`→`tests/UnitFrameFixture.hpp`; `4`→`src/utils/UnitSpriteLayout.hpp`; `7`→`src/data/gfxdata.h`; `8`→`src/map/cMapCamera.h`; `9`→`src/player/cPlayer.h` |
| `tests/UnitRenderPixelsTests.cpp@9208dcf:241` | `unit_render_pixels` (`tests/UnitRenderFixture.cmake:124`) | пиксели рендера юнитов; `1`→`tests/UnitFrameFixture.hpp`; `4`→`src/map/cMapCamera.h`; `5`→`src/player/cPlayer.h` |
| `tests/UnitSpriteLayoutTests.cpp@9208dcf:101` | `unit_sprite_layout` (`tests/UnitRenderFixture.cmake:116`) | раскладка HD-спрайтов; `1`→`src/utils/UnitSpriteLayout.hpp`; `3`→`tests/UnitFrameBaseline.hpp` |
| `tests/WorldObjectScaleTests.cpp@9208dcf:17` | `world_object_scale_selection` (`CMakeLists.txt:307`) | масштаб объектов мира и НПЗ; `1`→`src/utils/WorldObjectScale.hpp` |
| `tests/WorldScaleTests.cpp@9208dcf:17` | `world_scale_selection` (`CMakeLists.txt:285`) | масштаб мира; `1`→`src/utils/WorldScale.hpp` |
| `tests/ZoomStartTests.cpp@9208dcf:83` | `zoom_start` (`tests/UnitRenderFixture.cmake:125`) | начальный масштаб карты; `1`→`tests/ZoomTestSupport.hpp` |
## Данные и паки

Двоичные паки определяются по .dat-путям каталога **resources/bin/data/** с `binary=true` или `lfs=true`; LFS-указатель может иметь текстовый numstat. В объединённом наборе 28 таких путей: FORK1 изменил 22 A + 2 M, UP1 — 1 A + 4 M. Единственный overlap — `resources/bin/data/sdl_inter.dat` (M/M). FORK1 изменил `resources/bin/data/sdl_world.dat`; UP1 изменил `resources/bin/data/sdl_data.dat`, `resources/bin/data/sdl_mentat.dat`, `resources/bin/data/sdl_audio.dat` и добавил `resources/bin/data/sdl_gfxeditor.dat`. Четыре HD4-пака добавлены FORK1.

В `id_collisions` JSON содержится 4 записи: `resources/bin/data/sdl_data_hd4.dat`, индекс 167 — `EXPLOSION_CARRYALL` в UP1 и запись форка `HM_BUILD_REFINERY`; `resources/bin/data/sdl_inter_hd4.dat`, индекс 144 — `BMP_SELECT_HOUSE_SARDAUKAR` в UP1, записи форка нет; `resources/bin/data/sdl_inter_hd4.dat`, индекс 145 — `ICON_POWER_LOW` в UP1, записи форка нет; `resources/bin/data/sdl_mentat_hd4.dat`, индекс 51 — `MENTATS` в UP1, записи форка нет. В FORK1 — 18 сцен .dat непосредственно в **resources/bin/data/scenes/hd4**, вложенного набора **scenes/hd4/hd4** нет.

SHA-256 HD4-паков FORK1, сверенные с LFS oid:

| Пак | SHA-256 |
|---|---|
| `resources/bin/data/sdl_data_hd4.dat` | 781d3f7cea009d357d8b1236c11f681f6bbe831e8245bcb3c81ee46e3646a0c1 |
| `resources/bin/data/sdl_inter_hd4.dat` | fe4a6044a9a80f90562debc1c4d0c183b8eff65f665ac667b2859e05d28ab739 |
| `resources/bin/data/sdl_mentat_hd4.dat` | 4455422c7e7b7e6e16532c66242859b43a2002068752c9da56a46e456fa284f6 |
| `resources/bin/data/sdl_world_hd4.dat` | 94cf42fef1a755cc36b3b70f34900b15f76f28a540a38b73f69483f41b311d68 |

## Аддитивное

Новые пути FORK1 со статусом A и `upstream=null` — кандидаты для переноса; каждый путь считается один раз. Новый путь сам по себе не гарантирует совместимость include, API или runtime-контракта.

| Каталог | Путей |
|---|---:|
| .github/workflows | 1 |
| README_AI.md | 1 |
| codex-direct | 364 |
| docs | 18 |
| packaging | 4 |
| resources/bin | 133 |
| resources/hd | 1723 |
| src/audio | 5 |
| src/controls | 2 |
| src/debug | 7 |
| src/drawers | 6 |
| src/gameobjects | 4 |
| src/gamestates | 3 |
| src/save | 7 |
| src/sidebar | 2 |
| src/utils | 15 |
| tests | 51 |
| tools | 305 |
| units-gen | 800 |
| **Итого** | **3451** |

## SDL2 в коде форка

Счётчик считает строки с токенами `SDL_`, `Mix_`, `MIX_`, `IMG_`, `TTF_` и путями **SDL2/<файл>** в изменённых/добавленных/перемещённых **src/**-файлах FORK1, если токен не встречался в **src/** UP1. Несколько токенов в строке дают одну строку, файлы с нулём строк исключены. JSON: 333 строки в 54 файлах. Это не обнаруживает сохранённые имена с изменёнными сигнатурами.

| Путь FORK1 | Строк |
|---|---:|
| `src/drawers/SDLDrawer.cpp` | 41 |
| `src/utils/cDataPack.cpp` | 37 |
| `src/utils/cSoundPlayer.cpp` | 32 |
| `src/cGame_logic.cpp` | 27 |
| `src/utils/cPack.cpp` | 24 |
| `src/player/cPlayer.cpp` | 19 |
| `src/utils/Graphics.cpp` | 17 |
| `src/debug/UiAuditCapture.cpp` | 12 |
| `src/utils/cScreenInit.cpp` | 11 |
| `src/drawers/cTextTextureCache.cpp` | 10 |

SDL2 прямо или транзитивно подключают 27 из 40 C++-тестов; прямой SDL2 include есть у `FontCoverageTests` и `RenderTargetStateTests`. Общие маршруты:

- Через `src/utils/cRectangle.h@9208dcf:4` → **SDL2/SDL_rect.h**: `CampaignMapLayout`, `CommandBarLayout`, `HdPresentation`, `HudLayout`, `InteractionRegression`, `MusicControlsLayout`, `OptionsMenuLayout`, `RenderTargetState`, `UnitSpriteLayout`.
- Через `tests/UnitFrameFixture.hpp@9208dcf:3` → `src/drawers/SDLDrawer.hpp@9208dcf:8` → **SDL2/SDL.h**: `BuildingRectangle`, `MouseCellRefresh`, `MouseCellScan`, `MouseHoverState`, `TerrainTileGap`, `UnitDrawRegression`, `UnitFrameInteractions`, `UnitHdFrameDraw`, `UnitRenderPixels`, `ZoomStart`.
- Через `tests/UnitDrawRecorder.hpp@9208dcf:6` → **SDL2/SDL.h**: `FactoryPadEngine`, `PlacementFrame`, `PlacementRule`, `UnitDrawRegression`, `UnitFrameInteractions`, `UnitHdFrameDraw` (последние три также входят в группу с `UnitFrameFixture`).
- `CommandBindingConflict` и `CommandBindings`: `src/controls/CommandBindings.hpp@9208dcf:3` → **SDL2/SDL.h**; `MouseClickInit`: `src/controls/cMouse.h@9208dcf:7` → **SDL2/SDL.h**.
- `FactoryPadSave`: `src/save/SaveGameManager.cpp@9208dcf:9` → `src/cGame.h@9208dcf:27` → **SDL2/SDL.h**.
- `FontCoverage`: прямой **SDL2/SDL_ttf.h** и `src/utils/FontSupport.hpp@9208dcf:3` → **SDL2/SDL_ttf.h**.
- У `RenderTargetState` дополнительно `src/drawers/SDLDrawer.hpp@9208dcf:4` → `src/utils/Color.hpp@9208dcf:3` → **SDL2/SDL_pixels.h**; прямое подключение `src/include/Texture.hpp@9208dcf:2` → **SDL2/SDL.h**.

## Риски переноса

- `src/cGame_logic.cpp` и `src/cGame.h` изменены FORK1, а UP1 удалил оба пути. Перенос этих файлов целиком вернёт прежнее владение состоянием вместо текущих `src/game/cGame_logic.cpp@d06f2fc:375` (**cGame::init**) и `src/game/cGame.h@d06f2fc:89` (**class cGame**).
- `src/save/SaveGameManager.cpp@9208dcf:9` подключает старый **cGame.h**, а `src/save/SaveGameManager.cpp@9208dcf:11` — **d2tmc.h**. Новый файл добавлен только форком, тогда как игровой API UP1 находится в `src/game/cGame.h@d06f2fc:89`; перенос сохранений требует адаптации к новому API.
- `src/drawers/SDLDrawer.cpp`, `src/utils/cDataPack.cpp`, `src/utils/cPack.cpp` и `src/utils/cSoundPlayer.cpp` изменены обеими сторонами и содержат SDL2-код. Инвентарь FORK1 насчитывает 333 строки SDL-токенов в 54 src-файлах, поэтому механическая замена имён не проверяет сигнатуры и контракты рендера, паков и аудио.
- `src/utils/GameSettings.hpp@9208dcf:6` в UP1 перемещён в `src/utils/InitialGameSettings.hpp@d06f2fc:21`; runtime-настройки представлены отдельно в `src/game/cGameSettings.h@d06f2fc:23`. При переносе нужно сохранить разные времена жизни начальных и runtime-настроек.
- `src/managers/cInteractionManager.cpp` изменён FORK1, но удалён UP1. Обработку событий следует встроить в `src/gamestates/cGamePlaying.cpp@d06f2fc:317` (**cGamePlaying::onNotifyMouseEvent**), сохранив порядок получателей.
- Среди двоичных/LFS-путей только `resources/bin/data/sdl_inter.dat` пересекается как M/M (`resources/bin/data/sdl_inter.dat@9208dcf:2`, `resources/bin/data/sdl_inter.dat@d06f2fc:2`). Индекс 167 в `resources/bin/data/sdl_data_hd4.dat` занят записью форка `HM_BUILD_REFINERY`, а UP1 объявляет там `EXPLOSION_CARRYALL` (`src/data/gfxdata.h@d06f2fc:191`); в `resources/bin/data/sdl_inter_hd4.dat` нет индексов 144 и 145 (`BMP_SELECT_HOUSE_SARDAUKAR` — `src/data/gfxinter.h@d06f2fc:168`, `ICON_POWER_LOW` — `src/data/gfxinter.h@d06f2fc:169`); в `resources/bin/data/sdl_mentat_hd4.dat` нет индекса 51 (`MENTATS` — `src/include/gfxmentat.h@d06f2fc:75`). Разбор и согласование относятся к Б2.
- Переименование `resources/bin/skirmish/4PL_SinéadPlains.ini` в `resources/bin/skirmish_en/4PL_Sin├йadPlains.ini@9208dcf:1` сохранено FORK1; разрешение имени файла целевыми платформами не проверено.
- `src/utils/FontSupport.hpp@9208dcf:3` и `tests/FontCoverageTests.cpp@9208dcf:2` зависят от SDL2_ttf. Проверка кириллицы на настоящем шрифте после миграции остаётся необходимой.
- `.github/workflows/release.yml@9208dcf:1` добавлен форком при пересекающемся `CMakeLists.txt`; команды выпуска и комплект зависимостей для UP1 не проверены.
- Маркерная карта содержит 554 назначения функций на кодовые пути; у 249 назначений на 152 путях нет совпадения маркера. В UP1 всё ещё встречаются `renderStrechSprite`, `buttonWidth`, `renderTargetStack`, `m_titleBmp` и `UNIT_RAIDER`, поэтому владельца каждого перенесённого пути нужно сверять по диффу.
- world-scale: UP1 переименовал `src/map/cMapCamera.cpp` в `src/gameobjects/map/cMapCamera.cpp`; преемник в UP1 — `src/gameobjects/map/cMapCamera.cpp@d06f2fc:89` (**cMapCamera::setZoomLevel**); выбор масштаба форка нужно согласовать с этим текущим владельцем.
- placement-rule: UP1 изменил `src/controls/mousestates/cMousePlaceState.cpp`; актуальная проверка размещения — `src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:98` (**cMousePlaceState::mayPlaceIt**).
- factory-pads: UP1 изменил `src/gameobjects/structures/cLightFactory.cpp`; логику площадки и выезда юнита нужно встроить в текущий вывод фабрики `src/gameobjects/structures/cLightFactory.cpp@d06f2fc:76` (**cLightFactory::draw**).
- radar-dish: UP1 изменил `src/gameobjects/structures/cOutPost.cpp`; вращение следует согласовать с текущей анимацией `src/gameobjects/structures/cOutPost.cpp@d06f2fc:51` (**cOutPost::think_animation**).
- refinery-dock: FORK1 вызывает `refineryHarvesterLayout` из `src/drawers/cStructureDrawer.cpp@9208dcf:880`; кодовые пути этой функции не изменены в BASE..UP1. UP1 рисует REFINERY через `src/drawers/cStructureDrawer.cpp@d06f2fc:316` (**cStructureDrawer::drawStructureForLayer**), который направляет его в `src/drawers/cStructureDrawer.cpp@d06f2fc:280` (**cStructureDrawer::drawStructureAnimationRefinery**). Путь потребителя не входит в запись refinery-dock.
## Сверка чисел плана

- До добавлений FORK1 изменил 204 пути M и сделал 1 rename: 205 операций. Полный FORK1 — 3451 A + 204 M + 1 R = 3656 операций и 3657 path-записей.
- UP1 удалил 222 пути и переместил 48; всего 270 D/R операций. Пересечение содержит 139 path-записей: 116 M, 15 D и 8 R. Это число затронутых путей, а не фактических merge-конфликтов.
- Кодовый объём **src/**, **tests/** и корневого `CMakeLists.txt`: FORK1 — 234 операции, +24 812 / −2 171 строка; UP1 — 499 операций, +44 323 / −19 619 строк. Rename считается один раз.
- Объединённый инвентарь содержит 4394 path-записи. UP1: 341 A + 217 M + 222 D + 48 R = 828 операций, 876 записей. FORK1: 3657 записей, 3656 операций.
- Первый родительский путь BASE..FORK1 содержит 183 коммита, BASE..UP1 — 2215. Файлы **tests/*.cpp**: 43 у FORK1 и 21 у UP1.
