# Карта переноса функций RU/HD

BASE = e17379ad660fca46859b403a6c3d33ec8d831a40; FORK = 6662b2f4857c679425ea2166092a21f4bde7d6e7; UP0 = a51b97f15d0eee2d323a1737f140eb2cbd60973c. Общий предок FORK и UP0 проверен командой git merge-base и равен BASE. Источники: README_AI §1 в FORK, все 13 заголовков fork_commits и соседний port_inventory.json. Правила отнесения хранятся в tools/upstream/port_features.json; полная связь путей с функциями хранится только в JSON.

Для кода правила используют явные пути, выбранные по диффу BASE..FORK. marker_hits хранит совпадения маркеров с добавленными и удалёнными строками. Проверка требует объяснить каждое совпадение собственной функцией, транзитивной зависимостью или мотивированным исключением; совпадение API само по себе не определяет принадлежность файла. Тест карты отдельно сверяет все списки и числа с JSON.

«Не менялся» означает отсутствие изменения BASE..UP0; новый файл форка при этом может отсутствовать в UP0. Класс функции определяется наиболее сложной интеграцией её кода, поэтому внутри rewrite остаются данные и чистые модули для копирования. У rename JSON сохраняет обе границы пути; это две записи одной операции, а не два файла FORK.

## Функции форка

Порядок таблицы — рекомендуемый порядок переноса. Б2 предшествует интерпретации индексов; шаги Б3–Б12 следуют плану. Зависимости описывают порядок переноса функций, а не полный граф #include. Тестовые зависимости просмотрены транзитивно; общий include сам по себе не доказывает проверку функции.

| id | Название | Источник | Класс | Зависимости | Шаги | paths_count |
|---|---|---|---|---|---|---:|
| graphics-modes | Режимы Classic/HD и загрузка HD4 | README_AI §1 | rewrite | нет | Б3 | 22 |
| hd4-assets | Единый комплект HD4: интерфейс, сцены, здания, юниты и эффекты | README_AI §1 | rewrite | graphics-modes | Б3, Б6, Б11 | 2032 |
| hd-render | Физический HD-рендер интерфейса и мира | README_AI §1 | rewrite | graphics-modes | Б4 | 88 |
| retina-render-state | Восстановление состояния рендера на Retina | fork_commits | reapply | hd-render | Б4 | 4 |
| adaptive-layout | Адаптивные меню и HUD | README_AI §1 | rewrite | hd-render | Б5 | 62 |
| faction-tint-terrain | Маски цвета Дома и вариации поверхности | fork_commits | rewrite | hd-render, hd4-assets | Б6 | 20 |
| localization | Единая русская/английская сборка и переключение языка | README_AI §1 | rewrite | adaptive-layout | Б7 | 191 |
| save-slots | Десять именованных сохранений и F5/F9 | README_AI §1 | rewrite | adaptive-layout, localization | Б8 | 25 |
| music-pools | Музыкальные пулы, история и переключение треков | README_AI §1 | rewrite | adaptive-layout, localization | Б9 | 42 |
| command-bar | Бронзовая панель приказов и настраиваемые клавиши | README_AI §1 | rewrite | adaptive-layout, localization | Б10 | 38 |
| controls-tab | Вкладка управления в расширенных настройках | README_AI §1 | rewrite | command-bar | Б10 | 5 |
| interaction-refresh | Повторный вход в настройки, фиксация приказов и доступность ремонта | fork_commits | rewrite | command-bar, controls-tab | Б10 | 10 |
| starport-orders | Сохранение значения заказа Starport и закрытие потерянного каталога | fork_commits | rewrite | command-bar | Б10 | 7 |
| credits-art | Художественные изображения титров | README_AI §1 | rewrite | hd4-assets, localization | Б11 | 5 |
| release-packaging | Сборки и публикация Windows, Linux и macOS | fork_commits | reapply | save-slots, music-pools, interaction-refresh, credits-art | Б12 | 13 |
| author-gallery | Авторское приветствие, галерея и паспорт форка | fork_commits | reapply | release-packaging | Б12 | 7 |

Десять пользовательских возможностей перечислены в `README_AI.md@6662b2f:11` (**единая русская/английская**) и следующих пунктах §1. Дополнения fork_commits: f1b8ea26 — маски, поверхность и Starport; 863fc08d — Retina; 45f81e3a и 05048ffb — настройки и приказы; 2d7c6883, 46da206b, 26bb1e90, b8eff0c5, ecfd4990, 53adba17 — выпуск; 9aa0eae6 и 6662b2f4 — приветствие и галерея; d8bfe207 уточняет локализацию. Пути каждого коммита опубликованы в fork_commits.

### graphics-modes — Режимы Classic/HD и загрузка HD4

Переписать загрузку и применение настроек на владельцев UP0; чистый выбор режима сохранить. Сначала согласовать индексы на Б2, затем подключать HD4.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90` (**class cGame**).
- `src/cGame_logic.cpp` — удалён; код: `src/game/cGame_logic.cpp@a51b97f:289` (**cGame::applySettings**); `src/game/GameStateTransition.hpp@a51b97f:21` (**class GameStateTransition**); `src/game/MentatFlow.hpp@a51b97f:25` (**class MentatFlow**); `src/game/MissionFlow.hpp@a51b97f:25` (**class MissionFlow**); `src/game/ScenarioFlow.hpp@a51b97f:27` (**class ScenarioFlow**).
- `src/context/ContextCreator.cpp` — изменён.
- `src/context/ContextCreator.hpp` — изменён.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`.
- `src/utils/GraphicsMode.hpp` — не менялся.
- `src/utils/HdUiTextureLoader.cpp` — не менялся.
- `src/utils/HdUiTextureLoader.hpp` — не менялся.
- `src/utils/WorldScale.cpp` — не менялся.
- `src/utils/WorldScale.hpp` — не менялся.
- `src/utils/cDataPack.cpp` — изменён.
- `src/utils/cDataPack.hpp` — изменён.
- `src/utils/cPack.cpp` — изменён.
- `src/utils/cPack.h` — изменён.
- `src/utils/common.cpp` — изменён.
- `src/utils/common.h` — изменён.
- `tests/GraphicsModeTests.cpp` — не менялся.
- `tests/WorldScaleTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: resources/bin: 1.

Тесты форка: `tests/GraphicsModeTests.cpp`, `tests/WorldScaleTests.cpp` (выбор HD4). `tests/CommandBindingsTests.cpp` транзитивно включает common.h, но режимы графики не проверяет. Подключения и контракты — в реестре ниже.

Обратная зависимость от hd-render: загрузчик передаёт плотность в конструктор Texture — `src/utils/HdUiTextureLoader.cpp@6662b2f:34` (**new Texture**), — а параметр плотности добавлен вместе с hd-render (шаг Б4): `src/include/Texture.hpp@6662b2f:21` (**assetDensity**). Б3 переносить вместе с этим конструктором или после него.

### hd4-assets — Единый комплект HD4: интерфейс, сцены, здания, юниты и эффекты

Мастера и инструменты скопировать как исходные данные. Класс rewrite относится к интеграции: ментаты перемещены, часть прежних классов удалена. Сценарии загрузки, отдельные спрайты рейдера и дополнительные индексы согласовать на Б2; HD4 включать на Б3, маски на Б6, сцены на Б11.

Пути кода и тестов; судьба в апстриме:

- `src/drawers/cBuildingListDrawer.cpp` — изменён.
- `src/drawers/cMapDrawer.cpp` — изменён.
- `src/drawers/cSideBarDrawer.cpp` — изменён.
- `src/drawers/cSideBarDrawer.h` — изменён.
- `src/drawers/cStructureDrawer.cpp` — изменён.
- `src/drawers/cStructureDrawer.h` — изменён.
- `src/gameobjects/structures/cLightFactory.cpp` — изменён.
- `src/gamestates/cChooseHouseState.cpp` — изменён.
- `src/gamestates/cChooseHouseState.h` — изменён.
- `src/gamestates/cCreditsState.cpp` — изменён.
- `src/gamestates/cCreditsState.h` — изменён.
- `src/gamestates/cMainMenuState.cpp` — изменён.
- `src/gamestates/cMainMenuState.h` — изменён.
- `src/gamestates/cSelectMissionState.cpp` — изменён.
- `src/gamestates/cSelectMissionState.h` — изменён.
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён.
- `src/gamestates/cSelectYourNextConquestState.h` — изменён.
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`.
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`.
- `src/mentat/AtreidesMentat.cpp` — удалён; код: `src/gameobjects/mentat/AtreidesMentat.cpp@a51b97f:27` (**AtreidesMentat::AtreidesMentat**).
- `src/mentat/AtreidesMentat.h` — удалён; код: `src/gameobjects/mentat/AtreidesMentat.h@a51b97f:20` (**class AtreidesMentat**).
- `src/mentat/BeneMentat.cpp` — удалён; код: `src/gameobjects/mentat/BeneMentat.cpp@a51b97f:35` (**BeneMentat::BeneMentat**).
- `src/mentat/HarkonnenMentat.cpp` — удалён; код: `src/gameobjects/mentat/HarkonnenMentat.cpp@a51b97f:28` (**HarkonnenMentat::HarkonnenMentat**).
- `src/mentat/OrdosMentat.cpp` — удалён; код: `src/gameobjects/mentat/OrdosMentat.cpp@a51b97f:27` (**OrdosMentat::OrdosMentat**).
- `src/mentat/OrdosMentat.h` — удалён; код: `src/gameobjects/mentat/OrdosMentat.h@a51b97f:20` (**class OrdosMentat**).
- `src/utils/Graphics.cpp` — изменён.
- `src/utils/Graphics.hpp` — изменён.
- `src/utils/cDataPack.cpp` — изменён.
- `src/utils/cDataPack.hpp` — изменён.
- `src/utils/cPack.cpp` — изменён.
- `src/utils/cPack.h` — изменён.
- `src/utils/cIniGameRessouces.cpp` — удалён; код: `src/context/cInfoContextCreator.cpp@a51b97f:109` (**cInfoContextCreator::initUnits**); `src/context/cInfoContextCreator.cpp@a51b97f:1378` (**cInfoContextCreator::initStructures**).

Остальные пути по каталогу второго уровня: resources/bin: 68; resources/hd: 1723; tools: 209.

Тесты форка: нет подходящих tests/*.cpp по графу включений. Подключения и контракты — в реестре ниже.

### hd-render — Физический HD-рендер интерфейса и мира

Переписать владение окном, настройками и состояниями; заново применить физический рендер и масштабирование к SDL3. Чистые расчёты масштаба сохранить вместе с тестами.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90` (**class cGame**).
- `src/cGame_logic.cpp` — удалён; код: `src/game/cGame_logic.cpp@a51b97f:289` (**cGame::applySettings**); `src/game/GameStateTransition.hpp@a51b97f:21` (**class GameStateTransition**); `src/game/MentatFlow.hpp@a51b97f:25` (**class MentatFlow**); `src/game/MissionFlow.hpp@a51b97f:25` (**class MissionFlow**); `src/game/ScenarioFlow.hpp@a51b97f:27` (**class ScenarioFlow**).
- `src/context/ContextCreator.cpp` — изменён.
- `src/context/ContextCreator.hpp` — изменён.
- `src/context/TextContext.cpp` — изменён.
- `src/context/TextContext.hpp` — изменён.
- `src/drawers/CreditsDrawer.cpp` — изменён.
- `src/drawers/CreditsDrawer.h` — изменён.
- `src/drawers/SDLDrawer.cpp` — изменён.
- `src/drawers/SDLDrawer.hpp` — изменён.
- `src/drawers/cBuildingListDrawer.cpp` — изменён.
- `src/drawers/cBuildingListDrawer.h` — изменён.
- `src/drawers/cCommandBarDrawer.cpp` — не менялся.
- `src/drawers/cMapDrawer.cpp` — изменён.
- `src/drawers/cMessageDrawer.cpp` — изменён.
- `src/drawers/cOrderDrawer.cpp` — изменён.
- `src/drawers/cOrderDrawer.h` — изменён.
- `src/drawers/cSideBarDrawer.cpp` — изменён.
- `src/drawers/cSideBarDrawer.h` — изменён.
- `src/drawers/cStructureDrawer.cpp` — изменён.
- `src/drawers/cStructureDrawer.h` — изменён.
- `src/drawers/cTextDrawer.cpp` — изменён.
- `src/drawers/cTextDrawer.h` — изменён.
- `src/drawers/cTextTextureCache.cpp` — изменён.
- `src/drawers/cTextTextureCache.h` — изменён.
- `src/gameobjects/particles/cParticle.cpp` — изменён.
- `src/gameobjects/particles/cParticle.h` — изменён.
- `src/gameobjects/projectiles/bullet.cpp` — изменён.
- `src/gameobjects/structures/cAbstractStructure.cpp` — изменён.
- `src/gameobjects/structures/cAbstractStructure.h` — изменён.
- `src/gameobjects/structures/cHeavyFactory.cpp` — изменён.
- `src/gameobjects/structures/cLightFactory.cpp` — изменён.
- `src/gameobjects/units/cUnit.cpp` — изменён.
- `src/gameobjects/units/cUnit.h` — изменён.
- `src/gamestates/cChooseHouseState.cpp` — изменён.
- `src/gamestates/cChooseHouseState.h` — изменён.
- `src/gamestates/cCreditsState.cpp` — изменён.
- `src/gamestates/cMainMenuState.cpp` — изменён.
- `src/gamestates/cMainMenuState.h` — изменён.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `src/gamestates/cSelectMissionState.cpp` — изменён.
- `src/gamestates/cSelectMissionState.h` — изменён.
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён.
- `src/gamestates/cSelectYourNextConquestState.h` — изменён.
- `src/gamestates/cSetupSkirmishState.cpp` — изменён.
- `src/gamestates/cSetupSkirmishState.h` — изменён.
- `src/gui/GuiButton.cpp` — изменён.
- `src/gui/GuiButton.h` — изменён.
- `src/gui/GuiCheckBox.cpp` — изменён.
- `src/gui/GuiLabel.cpp` — изменён.
- `src/gui/GuiLabel.hpp` — изменён.
- `src/gui/GuiObject.h` — изменён.
- `src/gui/GuiTheme.hpp` — изменён.
- `src/include/Texture.hpp` — изменён.
- `src/managers/cDrawManager.cpp` — изменён.
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`.
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`.
- `src/mentat/AtreidesMentat.cpp` — удалён; код: `src/gameobjects/mentat/AtreidesMentat.cpp@a51b97f:27` (**AtreidesMentat::AtreidesMentat**).
- `src/mentat/AtreidesMentat.h` — удалён; код: `src/gameobjects/mentat/AtreidesMentat.h@a51b97f:20` (**class AtreidesMentat**).
- `src/mentat/BeneMentat.cpp` — удалён; код: `src/gameobjects/mentat/BeneMentat.cpp@a51b97f:35` (**BeneMentat::BeneMentat**).
- `src/mentat/HarkonnenMentat.cpp` — удалён; код: `src/gameobjects/mentat/HarkonnenMentat.cpp@a51b97f:28` (**HarkonnenMentat::HarkonnenMentat**).
- `src/mentat/OrdosMentat.cpp` — удалён; код: `src/gameobjects/mentat/OrdosMentat.cpp@a51b97f:27` (**OrdosMentat::OrdosMentat**).
- `src/mentat/OrdosMentat.h` — удалён; код: `src/gameobjects/mentat/OrdosMentat.h@a51b97f:20` (**class OrdosMentat**).
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`.
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`.
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`.
- `src/utils/Graphics.cpp` — изменён.
- `src/utils/Graphics.hpp` — изменён.
- `src/utils/HdPresentation.hpp` — не менялся.
- `src/utils/OutcomeScreenLayout.hpp` — не менялся.
- `src/utils/RenderScale.cpp` — не менялся.
- `src/utils/RenderScale.hpp` — не менялся.
- `src/utils/TextAlignment.hpp` — не менялся.
- `src/utils/WorldObjectScale.hpp` — не менялся.
- `src/utils/WorldScale.cpp` — не менялся.
- `src/utils/WorldScale.hpp` — не менялся.
- `src/utils/cScreenInit.cpp` — удалён; код: `src/game/cSDLSystem.cpp@a51b97f:249` (**cSDLSystem::cSDLSystem**).
- `src/utils/cScreenInit.h` — удалён; код: `src/game/cSDLSystem.h@a51b97f:28` (**class cSDLSystem**).
- `src/utils/common.cpp` — изменён.
- `src/utils/common.h` — изменён.
- `tests/HdPresentationTests.cpp` — не менялся.
- `tests/RenderScaleTests.cpp` — не менялся.
- `tests/RenderTargetStateTests.cpp` — не менялся.
- `tests/WorldObjectScaleTests.cpp` — не менялся.
- `tests/WorldScaleTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: resources/bin: 1.

Тесты форка: `tests/HdPresentationTests.cpp`, `tests/RenderScaleTests.cpp`, `tests/RenderTargetStateTests.cpp`, `tests/WorldObjectScaleTests.cpp`, `tests/WorldScaleTests.cpp`. Подключения и контракты — в реестре ниже.

### retina-render-state — Восстановление состояния рендера на Retina

Применить восстановление viewport, scale и clip к SDL3 после базового HD-рендера. Проверить вложенные render targets профильным тестом.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/drawers/SDLDrawer.cpp` — изменён.
- `src/drawers/SDLDrawer.hpp` — изменён.
- `tests/RenderTargetStateTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: нет.

Тесты форка: `tests/RenderTargetStateTests.cpp`. Подключения и контракты — в реестре ниже.

### adaptive-layout — Адаптивные меню и HUD

Сохранить геометрические политики; адаптировать прямоугольники к SDL3, затем переписать привязку к состояниям и настройкам UP0. Проверить тесты геометрии до интеграции экранов.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/cGame_logic.cpp` — удалён; код: `src/game/cGame_logic.cpp@a51b97f:289` (**cGame::applySettings**); `src/game/GameStateTransition.hpp@a51b97f:21` (**class GameStateTransition**); `src/game/MentatFlow.hpp@a51b97f:25` (**class MentatFlow**); `src/game/MissionFlow.hpp@a51b97f:25` (**class MissionFlow**); `src/game/ScenarioFlow.hpp@a51b97f:27` (**class ScenarioFlow**).
- `src/drawers/CommandBarLayout.hpp` — не менялся.
- `src/drawers/CreditsDrawer.cpp` — изменён.
- `src/drawers/CreditsDrawer.h` — изменён.
- `src/drawers/cBuildingListDrawer.cpp` — изменён.
- `src/drawers/cBuildingListDrawer.h` — изменён.
- `src/drawers/cCommandBarDrawer.cpp` — не менялся.
- `src/drawers/cMessageDrawer.cpp` — изменён.
- `src/drawers/cMessageDrawer.h` — изменён.
- `src/drawers/cMiniMapDrawer.cpp` — изменён.
- `src/drawers/cSideBarDrawer.cpp` — изменён.
- `src/drawers/cSideBarDrawer.h` — изменён.
- `src/drawers/cTextDrawer.cpp` — изменён.
- `src/drawers/cTextTextureCache.cpp` — изменён.
- `src/drawers/cTextTextureCache.h` — изменён.
- `src/gamestates/AdvancedOptionsHeaderLayout.hpp` — не менялся.
- `src/gamestates/CampaignMapLayout.hpp` — не менялся.
- `src/gamestates/OptionsMenuLayout.hpp` — не менялся.
- `src/gamestates/cChooseHouseState.cpp` — изменён.
- `src/gamestates/cChooseHouseState.h` — изменён.
- `src/gamestates/cCreditsState.cpp` — изменён.
- `src/gamestates/cMainMenuState.cpp` — изменён.
- `src/gamestates/cMainMenuState.h` — изменён.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `src/gamestates/cSelectMissionState.cpp` — изменён.
- `src/gamestates/cSelectMissionState.h` — изменён.
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён.
- `src/gamestates/cSelectYourNextConquestState.h` — изменён.
- `src/gamestates/cSetupSkirmishState.cpp` — изменён.
- `src/gamestates/cSetupSkirmishState.h` — изменён.
- `src/gui/GuiButton.cpp` — изменён.
- `src/gui/GuiButton.h` — изменён.
- `src/managers/cDrawManager.cpp` — изменён.
- `src/managers/cDrawManager.h` — изменён.
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`.
- `src/mentat/AbstractMentat.h` — перемещён в `src/gameobjects/mentat/AbstractMentat.h`.
- `src/mentat/AtreidesMentat.cpp` — удалён; код: `src/gameobjects/mentat/AtreidesMentat.cpp@a51b97f:27` (**AtreidesMentat::AtreidesMentat**).
- `src/mentat/AtreidesMentat.h` — удалён; код: `src/gameobjects/mentat/AtreidesMentat.h@a51b97f:20` (**class AtreidesMentat**).
- `src/mentat/BeneMentat.cpp` — удалён; код: `src/gameobjects/mentat/BeneMentat.cpp@a51b97f:35` (**BeneMentat::BeneMentat**).
- `src/mentat/HarkonnenMentat.cpp` — удалён; код: `src/gameobjects/mentat/HarkonnenMentat.cpp@a51b97f:28` (**HarkonnenMentat::HarkonnenMentat**).
- `src/mentat/OrdosMentat.cpp` — удалён; код: `src/gameobjects/mentat/OrdosMentat.cpp@a51b97f:27` (**OrdosMentat::OrdosMentat**).
- `src/mentat/OrdosMentat.h` — удалён; код: `src/gameobjects/mentat/OrdosMentat.h@a51b97f:20` (**class OrdosMentat**).
- `src/save/SaveSlotsDialog.cpp` — не менялся.
- `src/save/SaveSlotsDialog.hpp` — не менялся.
- `src/sidebar/HudLayout.hpp` — не менялся.
- `src/sidebar/MusicControlsLayout.hpp` — не менялся.
- `src/sidebar/cBuildingList.cpp` — изменён.
- `src/sidebar/cBuildingList.h` — изменён.
- `src/sidebar/cBuildingListFactory.cpp` — изменён.
- `src/sidebar/cSideBar.cpp` — изменён.
- `src/sidebar/cSideBar.h` — изменён.
- `src/utils/OutcomeScreenLayout.hpp` — не менялся.
- `src/utils/TextAlignment.hpp` — не менялся.
- `tests/CampaignMapLayoutTests.cpp` — не менялся.
- `tests/CommandBarLayoutTests.cpp` — не менялся.
- `tests/HdPresentationTests.cpp` — не менялся.
- `tests/HudLayoutTests.cpp` — не менялся.
- `tests/InteractionRegressionTests.cpp` — не менялся.
- `tests/MusicControlsLayoutTests.cpp` — не менялся.
- `tests/OptionsMenuLayoutTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: нет.

Тесты форка: `tests/CampaignMapLayoutTests.cpp`, `tests/CommandBarLayoutTests.cpp`, `tests/HdPresentationTests.cpp`, `tests/HudLayoutTests.cpp`, `tests/InteractionRegressionTests.cpp`, `tests/MusicControlsLayoutTests.cpp`, `tests/OptionsMenuLayoutTests.cpp`. Подключения и контракты — в реестре ниже.

### faction-tint-terrain — Маски цвета Дома и вариации поверхности

Переписать интеграцию масок с контекстами игроков и объектов; расчёт цвета и варианты поверхности применить заново после сверки ID. Носитель выбора масок по имени — `src/utils/Graphics.cpp@6662b2f:292` (**"HM_"**); `src/utils/cDataPack.cpp@6662b2f:42` (**DataPack::getIndexFromSurface**) и `src/utils/cDataPack.cpp@6662b2f:48` (**DataPack::getNameFromIndex**) связывают поверхность с именем записи для выбора маски. DataPack включён также в загрузку режимов и HD4-ассеты.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/drawers/TerrainVariation.hpp` — не менялся.
- `src/drawers/cMapDrawer.cpp` — изменён.
- `src/drawers/cStructureDrawer.cpp` — изменён.
- `src/drawers/cStructureDrawer.h` — изменён.
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`.
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`.
- `src/utils/FactionTint.hpp` — не менялся.
- `src/utils/Graphics.cpp` — изменён.
- `src/utils/Graphics.hpp` — изменён.
- `src/utils/cDataPack.cpp` — изменён.
- `src/utils/cDataPack.hpp` — изменён.
- `src/utils/cPack.cpp` — изменён.
- `src/utils/cPack.h` — изменён.
- `tests/FactionTintTests.cpp` — не менялся.
- `tests/TerrainVariationTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: tools: 4.

Тесты форка: `tests/FactionTintTests.cpp`, `tests/TerrainVariationTests.cpp`. Подключения и контракты — в реестре ниже.

### localization — Единая русская/английская сборка и переключение языка

Переписать интеграцию локализации с новым разбором кампаний и владельцами настроек; перенести языковые ресурсы, шрифт и функции выбора текста. Новую кампанию Сардаукаров переводить отдельной проверяемой правкой на Б7.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90` (**class cGame**).
- `src/cGame_logic.cpp` — удалён; код: `src/game/cGame_logic.cpp@a51b97f:289` (**cGame::applySettings**); `src/game/GameStateTransition.hpp@a51b97f:21` (**class GameStateTransition**); `src/game/MentatFlow.hpp@a51b97f:25` (**class MentatFlow**); `src/game/MissionFlow.hpp@a51b97f:25` (**class MissionFlow**); `src/game/ScenarioFlow.hpp@a51b97f:27` (**class ScenarioFlow**).
- `src/context/ContextCreator.cpp` — изменён.
- `src/context/ContextCreator.hpp` — изменён.
- `src/context/TextContext.cpp` — изменён.
- `src/context/TextContext.hpp` — изменён.
- `src/controls/CommandBindings.hpp` — не менялся.
- `src/controls/mousestates/cMouseNormalState.cpp` — изменён.
- `src/drawers/CreditsDrawer.cpp` — изменён.
- `src/drawers/OrderButtonPolicy.hpp` — не менялся.
- `src/drawers/cBuildingListDrawer.cpp` — изменён.
- `src/drawers/cCommandBarDrawer.cpp` — не менялся.
- `src/drawers/cMouseDrawer.cpp` — изменён.
- `src/drawers/cOrderDrawer.cpp` — изменён.
- `src/drawers/cOrderDrawer.h` — изменён.
- `src/drawers/cSideBarDrawer.cpp` — изменён.
- `src/drawers/cSideBarDrawer.h` — изменён.
- `src/drawers/cTextDrawer.cpp` — изменён.
- `src/drawers/cTextDrawer.h` — изменён.
- `src/drawers/cTextTextureCache.cpp` — изменён.
- `src/gameobjects/structures/cAbstractStructure.cpp` — изменён.
- `src/gameobjects/structures/cOrderProcesser.cpp` — изменён.
- `src/gameobjects/structures/cWindTrap.cpp` — изменён.
- `src/gameobjects/units/cUnit.cpp` — изменён.
- `src/gamestates/cChooseHouseState.cpp` — изменён.
- `src/gamestates/cCreditsState.cpp` — изменён.
- `src/gamestates/cMainMenuState.cpp` — изменён.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `src/gamestates/cSelectMissionState.cpp` — изменён.
- `src/gamestates/cSelectYourNextConquestState.cpp` — изменён.
- `src/gamestates/cSetupSkirmishState.cpp` — изменён.
- `src/ini.cpp` — удалён; код: `src/utils/ini.cpp@a51b97f:80` (**cIni::loadRegionfile**).
- `src/managers/cDrawManager.cpp` — изменён.
- `src/map/cPreviewMaps.cpp` — удалён; код: `src/gameobjects/map/cPreviewMaps.cpp@a51b97f:37` (**cPreviewMaps::cPreviewMaps**).
- `src/mentat/AbstractMentat.cpp` — перемещён в `src/gameobjects/mentat/AbstractMentat.cpp`.
- `src/mentat/AtreidesMentat.cpp` — удалён; код: `src/gameobjects/mentat/AtreidesMentat.cpp@a51b97f:27` (**AtreidesMentat::AtreidesMentat**).
- `src/mentat/BeneMentat.cpp` — удалён; код: `src/gameobjects/mentat/BeneMentat.cpp@a51b97f:35` (**BeneMentat::BeneMentat**).
- `src/mentat/HarkonnenMentat.cpp` — удалён; код: `src/gameobjects/mentat/HarkonnenMentat.cpp@a51b97f:28` (**HarkonnenMentat::HarkonnenMentat**).
- `src/mentat/OrdosMentat.cpp` — удалён; код: `src/gameobjects/mentat/OrdosMentat.cpp@a51b97f:27` (**OrdosMentat::OrdosMentat**).
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`.
- `src/save/SaveFileCodec.cpp` — не менялся.
- `src/save/SaveGameManager.cpp` — не менялся.
- `src/save/SaveSlotName.hpp` — не менялся.
- `src/save/SaveSlotsDialog.cpp` — не менялся.
- `src/sidebar/cBuildingListItem.cpp` — изменён.
- `src/utils/FontSupport.hpp` — не менялся.
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`.
- `src/utils/Localization.hpp` — не менялся.
- `src/utils/cIniGameRessouces.cpp` — удалён; код: `src/context/cInfoContextCreator.cpp@a51b97f:109` (**cInfoContextCreator::initUnits**); `src/context/cInfoContextCreator.cpp@a51b97f:1378` (**cInfoContextCreator::initStructures**).
- `src/utils/common.cpp` — изменён.
- `tests/CommandBindingsTests.cpp` — не менялся.
- `tests/FontCoverageTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: resources/bin: 136; tools: 1.

Тесты форка: `tests/FontCoverageTests.cpp`, `tests/SaveSlotNameTests.cpp`, `tests/CommandBindingsTests.cpp` (русское имя клавиши). Подключения и контракты — в реестре ниже.


### save-slots — Десять именованных сохранений и F5/F9

Сохранить кодек и правила имён; переписать захват и восстановление объектов UP0. Зависимости старого менеджера видны в `src/save/SaveGameManager.cpp@6662b2f:9` (**"cGame.h"**) и `src/save/SaveGameManager.cpp@6662b2f:11` (**"d2tmc.h"**). Тесты кодека не проверяют восстановление миссии.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/building/cItemBuilder.h` — изменён.
- `src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90` (**class cGame**).
- `src/cGame_logic.cpp` — удалён; код: `src/game/cGame_logic.cpp@a51b97f:289` (**cGame::applySettings**); `src/game/GameStateTransition.hpp@a51b97f:21` (**class GameStateTransition**); `src/game/MentatFlow.hpp@a51b97f:25` (**class MentatFlow**); `src/game/MissionFlow.hpp@a51b97f:25` (**class MissionFlow**); `src/game/ScenarioFlow.hpp@a51b97f:27` (**class ScenarioFlow**).
- `src/gameobjects/structures/cAbstractStructure.h` — изменён.
- `src/gameobjects/units/cReinforcements.h` — изменён.
- `src/gameobjects/units/cUnit.h` — изменён.
- `src/gamestates/OptionsMenuLayout.hpp` — не менялся.
- `src/gamestates/cGameState.h` — изменён.
- `src/gamestates/cMainMenuState.cpp` — изменён.
- `src/gamestates/cMainMenuState.h` — изменён.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `src/map/cMap.h` — перемещён в `src/gameobjects/map/cMap.h`.
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`.
- `src/save/SaveFileCodec.cpp` — не менялся.
- `src/save/SaveFileCodec.hpp` — не менялся.
- `src/save/SaveGameManager.cpp` — не менялся.
- `src/save/SaveGameManager.hpp` — не менялся.
- `src/save/SaveSlotName.hpp` — не менялся.
- `src/save/SaveSlotsDialog.cpp` — не менялся.
- `src/save/SaveSlotsDialog.hpp` — не менялся.
- `src/sidebar/cBuildingListItem.h` — изменён.
- `tests/SaveFileCodecTests.cpp` — не менялся.
- `tests/SaveSlotNameTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: нет.

Тесты форка: `tests/OptionsMenuLayoutTests.cpp`, `tests/SaveFileCodecTests.cpp`, `tests/SaveSlotNameTests.cpp`. Подключения и контракты — в реестре ниже.

### music-pools — Музыкальные пулы, история и переключение треков

Сохранить независимый плейлист и политику перехода. Переписать backend и маршрутизацию категорий под UP0; граница старого менеджера — `src/audio/MusicController.h@6662b2f:10` (**class cSoundPlayer**). Внешние WAV перенести как данные без перезаписи пользовательской музыки.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/audio/MusicController.cpp` — не менялся.
- `src/audio/MusicController.h` — не менялся.
- `src/audio/MusicPlaylist.cpp` — не менялся.
- `src/audio/MusicPlaylist.h` — не менялся.
- `src/audio/MusicTransitionPolicy.hpp` — не менялся.
- `src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90` (**class cGame**).
- `src/cGame_logic.cpp` — удалён; код: `src/game/cGame_logic.cpp@a51b97f:289` (**cGame::applySettings**); `src/game/GameStateTransition.hpp@a51b97f:21` (**class GameStateTransition**); `src/game/MentatFlow.hpp@a51b97f:25` (**class MentatFlow**); `src/game/MissionFlow.hpp@a51b97f:25` (**class MissionFlow**); `src/game/ScenarioFlow.hpp@a51b97f:27` (**class ScenarioFlow**).
- `src/drawers/cMessageDrawer.cpp` — изменён.
- `src/managers/cDrawManager.cpp` — изменён.
- `src/managers/cDrawManager.h` — изменён.
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`.
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`.
- `src/sidebar/MusicControlsLayout.hpp` — не менялся.
- `src/utils/cSoundPlayer.cpp` — изменён.
- `src/utils/cSoundPlayer.h` — изменён.
- `tests/MusicControlsLayoutTests.cpp` — не менялся.
- `tests/MusicPlaylistTests.cpp` — не менялся.
- `tests/MusicTransitionPolicyTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: resources/bin: 22; tools: 1.

Тесты форка: `tests/MusicControlsLayoutTests.cpp`, `tests/MusicPlaylistTests.cpp`, `tests/MusicTransitionPolicyTests.cpp`. Подключения и контракты — в реестре ниже.

### command-bar — Бронзовая панель приказов и настраиваемые клавиши

Сохранить чистые политики и графику панели, применить рисование заново; переписать интеграцию ввода с преемниками InteractionManager. Подписи и клавиши формировать из фактических назначений.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90` (**class cGame**).
- `src/cGame_logic.cpp` — удалён; код: `src/game/cGame_logic.cpp@a51b97f:289` (**cGame::applySettings**); `src/game/GameStateTransition.hpp@a51b97f:21` (**class GameStateTransition**); `src/game/MentatFlow.hpp@a51b97f:25` (**class MentatFlow**); `src/game/MissionFlow.hpp@a51b97f:25` (**class MissionFlow**); `src/game/ScenarioFlow.hpp@a51b97f:27` (**class ScenarioFlow**).
- `src/context/TextContext.cpp` — изменён.
- `src/context/TextContext.hpp` — изменён.
- `src/controls/CommandBindings.hpp` — не менялся.
- `src/controls/CommandModePolicy.hpp` — не менялся.
- `src/controls/cGameControlsContext.cpp` — изменён.
- `src/controls/cGameControlsContext.h` — изменён.
- `src/controls/cKeyboardEvent.h` — изменён.
- `src/controls/mousestates/cMouseNormalState.cpp` — изменён.
- `src/controls/mousestates/cMouseNormalState.h` — изменён.
- `src/controls/mousestates/cMouseRepairState.cpp` — изменён.
- `src/controls/mousestates/cMouseUnitsSelectedState.cpp` — изменён.
- `src/controls/mousestates/cMouseUnitsSelectedState.h` — изменён.
- `src/drawers/CommandBarLayout.hpp` — не менялся.
- `src/drawers/CommandBarPolicy.hpp` — не менялся.
- `src/drawers/cCommandBarDrawer.cpp` — не менялся.
- `src/drawers/cCommandBarDrawer.h` — не менялся.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `src/include/definitions.h` — изменён.
- `src/managers/cDrawManager.cpp` — изменён.
- `src/managers/cDrawManager.h` — изменён.
- `src/managers/cInteractionManager.cpp` — удалён; код: `src/gamestates/cGamePlaying.cpp@a51b97f:304` (**cGamePlaying::onNotifyMouseEvent**).
- `src/utils/GameSettings.hpp` — перемещён в `src/utils/InitialGameSettings.hpp`.
- `src/utils/common.cpp` — изменён.
- `tests/CommandBarLayoutTests.cpp` — не менялся.
- `tests/CommandBindingsTests.cpp` — не менялся.
- `tests/InteractionRegressionTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: resources/bin: 2; resources/hd: 4; tools: 2.

Тесты форка: `tests/CommandBarLayoutTests.cpp`, `tests/CommandBindingsTests.cpp`, `tests/InteractionRegressionTests.cpp`. Подключения и контракты — в реестре ниже.

### controls-tab — Вкладка управления в расширенных настройках

Переписать интеграцию вкладки с новым владельцем настроек; раскладку применить заново к изменённому экрану после переноса назначений клавиш. Тесты политик не доказывают сохранение настроек при полном повторном входе.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/gamestates/AdvancedOptionsHeaderLayout.hpp` — не менялся.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `tests/InteractionRegressionTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: нет.

Тесты форка: `tests/InteractionRegressionTests.cpp`. Подключения и контракты — в реестре ниже.

### interaction-refresh — Повторный вход в настройки, фиксация приказов и доступность ремонта

Переписать привязку к новому циклу состояний, сохранив правила фиксации приказа, отмены и доступности ремонта. Полный цикл повторного входа в настройки тестами политик не проверен.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/controls/CommandModePolicy.hpp` — не менялся.
- `src/controls/mousestates/cMouseNormalState.cpp` — изменён.
- `src/controls/mousestates/cMouseRepairState.cpp` — изменён.
- `src/controls/mousestates/cMouseUnitsSelectedState.cpp` — изменён.
- `src/drawers/CommandBarPolicy.hpp` — не менялся.
- `src/drawers/cCommandBarDrawer.cpp` — не менялся.
- `src/gamestates/cOptionsState.cpp` — изменён.
- `src/gamestates/cOptionsState.h` — изменён.
- `tests/InteractionRegressionTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: нет.

Тесты форка: `tests/InteractionRegressionTests.cpp`. Подключения и контракты — в реестре ниже.

### starport-orders — Сохранение значения заказа Starport и закрытие потерянного каталога

Скопировать чистую очередь и переписать интеграцию с владельцами игроков и объектов; проверить сохранение build ID после изменения каталога и закрытие заказа при потере Starport.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/gameobjects/structures/StarportOrderQueue.hpp` — не менялся.
- `src/gameobjects/structures/cOrderProcesser.cpp` — изменён.
- `src/gameobjects/structures/cOrderProcesser.h` — изменён.
- `src/gameobjects/structures/cStarPort.cpp` — изменён.
- `src/sidebar/cBuildingListUpdater.cpp` — изменён.
- `tests/InteractionRegressionTests.cpp` — не менялся.

Остальные пути по каталогу второго уровня: нет.

Тесты форка: `tests/InteractionRegressionTests.cpp`. Подключения и контракты — в реестре ниже.

### credits-art — Художественные изображения титров

Изображения скопировать, отрисовку и переходы экрана переписать с новым владельцем настроек после HD-рендера и локализации. Профильного теста изображений нет; визуальная приёмка относится к Б13.

Пути кода и тестов; судьба в апстриме:

- `src/gamestates/cCreditsState.cpp` — изменён.
- `src/gamestates/cCreditsState.h` — изменён.

Остальные пути по каталогу второго уровня: resources/bin: 2; tools: 1.

Тесты форка: нет подходящих tests/*.cpp по графу включений. Подключения и контракты — в реестре ниже.

### release-packaging — Сборки и публикация Windows, Linux и macOS

Применить workflow, CMake и правила LFS заново к зависимостям UP0. Тексты установки сохранить как исходный материал и обновить сведения о SDL3; проверка платформ относится к Б12.

Пути кода и тестов; судьба в апстриме:

- `CMakeLists.txt` — изменён.
- `src/main.cpp` — изменён.

Остальные пути по каталогу второго уровня: .github/workflows: 1; packaging: 4; resources/bin: 4; корень: 2.

Тесты форка: нет подходящих tests/*.cpp по графу включений. Подключения и контракты — в реестре ниже.

### author-gallery — Авторское приветствие, галерея и паспорт форка

Скопировать снимки и паспорт как исторические материалы, применить приветствие заново в README апстрима. Тексты паспорта о SDL2 и прежних владельцах состояния обновить после переноса; снимки форка не подтверждают поведение UP0.

Пути кода и тестов; судьба в апстриме:

Остальные пути по каталогу второго уровня: docs/screenshots: 5; корень: 2.

Тесты форка: нет подходящих tests/*.cpp по графу включений. Подключения и контракты — в реестре ниже.

## Реестр тестов форка

Каждый файл использует собственный main, а не именованные TEST_CASE. Ниже приведены имена CTest, прямые проектные include и оставшиеся транзитивные зависимости из FORK. Реестр описывает проверки в исходниках; C++-тесты на Б0 не запускались.

- `tests/CampaignMapLayoutTests.cpp@6662b2f:6` (**main**); CTest: campaign_map_layout_geometry — `CMakeLists.txt@6662b2f:333` (**campaign_map_layout_geometry**). Панели карты кампании помещаются в экран. Прямые include: `tests/CampaignMapLayoutTests.cpp@6662b2f:1` (**gamestates/CampaignMapLayout.hpp**) → `src/gamestates/CampaignMapLayout.hpp`. Косвенные: `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/CommandBarLayoutTests.cpp@6662b2f:3` (**main**); CTest: command_bar_layout_geometry — `CMakeLists.txt@6662b2f:246` (**command_bar_layout_geometry**). Геометрия кнопок панели приказов при разных размерах. Прямые include: `tests/CommandBarLayoutTests.cpp@6662b2f:1` (**drawers/CommandBarLayout.hpp**) → `src/drawers/CommandBarLayout.hpp`. Косвенные: `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/CommandBindingsTests.cpp@6662b2f:7` (**main**); CTest: command_bindings — `CMakeLists.txt@6662b2f:184` (**command_bindings**). Назначения клавиш, разбор SDL scancode и эквивалентность левого и правого Ctrl. Прямые include: `tests/CommandBindingsTests.cpp@6662b2f:2` (**controls/CommandBindings.hpp**) → `src/controls/CommandBindings.hpp`, `tests/CommandBindingsTests.cpp@6662b2f:3` (**controls/cKeyboardEvent.h**) → `src/controls/cKeyboardEvent.h`. Косвенные: `src/include/enums.h`, `src/utils/cPoint.h`, `src/utils/common.h`.
- `tests/FactionTintTests.cpp@6662b2f:5` (**main**); CTest: faction_tint_uniformity — `CMakeLists.txt@6662b2f:417` (**faction_tint_uniformity**). Расчёт цветового канала фракции и сохранение оттенков текстуры; загрузка масок не проверяется. Прямые include: `tests/FactionTintTests.cpp@6662b2f:1` (**utils/FactionTint.hpp**) → `src/utils/FactionTint.hpp`. Косвенные: нет.
- `tests/FontCoverageTests.cpp@6662b2f:9` (**main**); CTest: russian_font_coverage — `CMakeLists.txt@6662b2f:320` (**russian_font_coverage**). Наличие кириллических глифов в настоящем шрифте. Прямые include: `tests/FontCoverageTests.cpp@6662b2f:3` (**utils/FontSupport.hpp**) → `src/utils/FontSupport.hpp`. Косвенные: нет.
- `tests/GraphicsModeTests.cpp@6662b2f:5` (**main**); CTest: graphics_mode_selection — `CMakeLists.txt@6662b2f:207` (**graphics_mode_selection**). Разбор режима Classic/HD, запасной режим и выбор секции HD4. Прямые include: `tests/GraphicsModeTests.cpp@6662b2f:1` (**utils/GraphicsMode.hpp**) → `src/utils/GraphicsMode.hpp`. Косвенные: нет.
- `tests/HdPresentationTests.cpp@6662b2f:20` (**main**); CTest: hd_presentation_selection — `CMakeLists.txt@6662b2f:304` (**hd_presentation_selection**). Выбор физического представления, отдельные frame/fade targets, геометрия outcome и оптическое центрирование текста. Прямые include: `tests/HdPresentationTests.cpp@6662b2f:1` (**utils/HdPresentation.hpp**) → `src/utils/HdPresentation.hpp`, `tests/HdPresentationTests.cpp@6662b2f:2` (**utils/OutcomeScreenLayout.hpp**) → `src/utils/OutcomeScreenLayout.hpp`, `tests/HdPresentationTests.cpp@6662b2f:3` (**utils/TextAlignment.hpp**) → `src/utils/TextAlignment.hpp`. Косвенные: `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/HudLayoutTests.cpp@6662b2f:47` (**main**); CTest: hud_layout_geometry — `CMakeLists.txt@6662b2f:220` (**hud_layout_geometry**). Геометрия HUD и отсутствие пересечений. Прямые include: `tests/HudLayoutTests.cpp@6662b2f:1` (**sidebar/HudLayout.hpp**) → `src/sidebar/HudLayout.hpp`. Косвенные: `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/InteractionRegressionTests.cpp@6662b2f:28` (**main**); CTest: interaction_regressions — `CMakeLists.txt@6662b2f:259` (**interaction_regressions**). Заголовок настроек, фиксация приказа, отмена, доступность команд и значение заказа Starport. Прямые include: `tests/InteractionRegressionTests.cpp@6662b2f:1` (**controls/CommandModePolicy.hpp**) → `src/controls/CommandModePolicy.hpp`, `tests/InteractionRegressionTests.cpp@6662b2f:2` (**drawers/CommandBarPolicy.hpp**) → `src/drawers/CommandBarPolicy.hpp`, `tests/InteractionRegressionTests.cpp@6662b2f:3` (**drawers/OrderButtonPolicy.hpp**) → `src/drawers/OrderButtonPolicy.hpp`, `tests/InteractionRegressionTests.cpp@6662b2f:4` (**gamestates/AdvancedOptionsHeaderLayout.hpp**) → `src/gamestates/AdvancedOptionsHeaderLayout.hpp`, `tests/InteractionRegressionTests.cpp@6662b2f:5` (**gameobjects/structures/StarportOrderQueue.hpp**) → `src/gameobjects/structures/StarportOrderQueue.hpp`. Косвенные: `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/MusicControlsLayoutTests.cpp@6662b2f:48` (**main**); CTest: music_controls_layout_geometry — `CMakeLists.txt@6662b2f:406` (**music_controls_layout_geometry**). Размещение музыкальных кнопок в HUD. Прямые include: `tests/MusicControlsLayoutTests.cpp@6662b2f:1` (**sidebar/HudLayout.hpp**) → `src/sidebar/HudLayout.hpp`, `tests/MusicControlsLayoutTests.cpp@6662b2f:2` (**sidebar/MusicControlsLayout.hpp**) → `src/sidebar/MusicControlsLayout.hpp`. Косвенные: `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/MusicPlaylistTests.cpp@6662b2f:22` (**main**); CTest: music_playlist_shuffle_history — `CMakeLists.txt@6662b2f:382` (**music_playlist_shuffle_history**). Shuffle-bag, история назад/вперёд и обнаружение внешних файлов. Прямые include: `tests/MusicPlaylistTests.cpp@6662b2f:1` (**audio/MusicPlaylist.h**) → `src/audio/MusicPlaylist.h`. Косвенные: нет.
- `tests/MusicTransitionPolicyTests.cpp@6662b2f:3` (**main**); CTest: music_transition_policy — `CMakeLists.txt@6662b2f:393` (**music_transition_policy**). Повторный вход в категорию и смена категории. Прямые include: `tests/MusicTransitionPolicyTests.cpp@6662b2f:1` (**audio/MusicTransitionPolicy.hpp**) → `src/audio/MusicTransitionPolicy.hpp`. Косвенные: нет.
- `tests/OptionsMenuLayoutTests.cpp@6662b2f:38` (**main**); CTest: options_menu_layout_geometry — `CMakeLists.txt@6662b2f:233` (**options_menu_layout_geometry**). Геометрия меню настроек и действий сохранения/загрузки. Прямые include: `tests/OptionsMenuLayoutTests.cpp@6662b2f:1` (**gamestates/OptionsMenuLayout.hpp**) → `src/gamestates/OptionsMenuLayout.hpp`. Косвенные: `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/RenderScaleTests.cpp@6662b2f:33` (**main**); CTest: render_scale_calculations — `CMakeLists.txt@6662b2f:196` (**render_scale_calculations**). Автоматический и ручной размер логического canvas. Прямые include: `tests/RenderScaleTests.cpp@6662b2f:1` (**utils/RenderScale.hpp**) → `src/utils/RenderScale.hpp`. Косвенные: нет.
- `tests/RenderTargetStateTests.cpp@6662b2f:28` (**main**); CTest: render_target_state_restoration — `CMakeLists.txt@6662b2f:347` (**render_target_state_restoration**). Вложенные render targets, viewport, scale, clip, прозрачность и alpha. Прямые include: `tests/RenderTargetStateTests.cpp@6662b2f:3` (**drawers/SDLDrawer.hpp**) → `src/drawers/SDLDrawer.hpp`, `tests/RenderTargetStateTests.cpp@6662b2f:4` (**include/Texture.hpp**) → `src/include/Texture.hpp`. Косвенные: `src/utils/Color.hpp`, `src/utils/cPoint.h`, `src/utils/cRectangle.h`.
- `tests/SaveFileCodecTests.cpp@6662b2f:23` (**main**); CTest: save_file_codec_roundtrip — `CMakeLists.txt@6662b2f:359` (**save_file_codec_roundtrip**). Round-trip и отклонение неверных checksum, версии, заголовка и размера. Прямые include: `tests/SaveFileCodecTests.cpp@6662b2f:1` (**save/SaveFileCodec.hpp**) → `src/save/SaveFileCodec.hpp`. Косвенные: нет.
- `tests/SaveSlotNameTests.cpp@6662b2f:16` (**main**); CTest: save_slot_name_handling — `CMakeLists.txt@6662b2f:370` (**save_slot_name_handling**). Слоты 1–10, очистка имени и корректное усечение UTF-8. Прямые include: `tests/SaveSlotNameTests.cpp@6662b2f:1` (**save/SaveSlotName.hpp**) → `src/save/SaveSlotName.hpp`. Косвенные: `src/utils/Localization.hpp`.
- `tests/TerrainVariationTests.cpp@6662b2f:7` (**main**); CTest: terrain_variation_selection — `CMakeLists.txt@6662b2f:270` (**terrain_variation_selection**). Детерминированный выбор варианта поверхности и проверка границ. Прямые include: `tests/TerrainVariationTests.cpp@6662b2f:1` (**drawers/TerrainVariation.hpp**) → `src/drawers/TerrainVariation.hpp`. Косвенные: `src/data/gfxdata.h`.
- `tests/WorldObjectScaleTests.cpp@6662b2f:28` (**main**); CTest: world_object_scale_selection — `CMakeLists.txt@6662b2f:293` (**world_object_scale_selection**). Масштаб объектов и геометрия харвестера на НПЗ. Прямые include: `tests/WorldObjectScaleTests.cpp@6662b2f:1` (**utils/WorldObjectScale.hpp**) → `src/utils/WorldObjectScale.hpp`. Косвенные: нет.
- `tests/WorldScaleTests.cpp@6662b2f:17` (**main**); CTest: world_scale_selection — `CMakeLists.txt@6662b2f:282` (**world_scale_selection**). Автоматический и ручной масштаб мира; HD4 при разных canvas. Прямые include: `tests/WorldScaleTests.cpp@6662b2f:1` (**utils/WorldScale.hpp**) → `src/utils/WorldScale.hpp`. Косвенные: нет.

## Данные и паки

Изменения двоичных паков определяются по путям .dat, где binary или lfs равен true: указатель LFS сам по себе может иметь текстовый numstat. В пересечении сторон только `resources/bin/data/sdl_inter.dat` (M/M). Все двоичные пересечения JSON:

- `resources/bin/data/sdl_inter.dat` — M/M.

Классический `resources/bin/data/sdl_world.dat` менял только форк; `resources/bin/data/sdl_data.dat`, `resources/bin/data/sdl_mentat.dat`, `resources/bin/data/sdl_audio.dat` — только апстрим. `resources/bin/data/sdl_gfxeditor.dat` добавлен апстримом. Для общего sdl_inter требуется сверка записей на Б2. Флаги binary и lfs в JSON отражают разные свойства: numstat Git и фильтр FORK.

Перед read_pack из `tools/hd_assets.py` сверены SHA-256 четырёх HD4-паков с oid их LFS-указателей в FORK. Полученные хеши:

| Пак FORK | SHA-256 |
|---|---|
| `resources/bin/data/sdl_data_hd4.dat` | e2a87ce8cf9143f9d11ee0a54dcf10b7a57d109b49e713dadf4133c12d882045 |
| `resources/bin/data/sdl_inter_hd4.dat` | 8ecf69b14ee2becec0978d81d9fd911e557dc56445fae324560e9fe83fff021e |
| `resources/bin/data/sdl_mentat_hd4.dat` | 4455422c7e7b7e6e16532c66242859b43a2002068752c9da56a46e456fa284f6 |
| `resources/bin/data/sdl_world_hd4.dat` | 94cf42fef1a755cc36b3b70f34900b15f76f28a540a38b73f69483f41b311d68 |

Все записи id_collisions из JSON; define_pair отсутствуют, поскольку форк не добавлял числовых define в этих заголовках. Отсутствие define_pair не исключает конфликта содержимого пака.

| kind | Заголовок UP0 / define | Значение | Пак FORK | fork_entry |
|---|---|---:|---|---|
| pack_index_missing | `src/data/gfxinter.h@a51b97f:165` (**BMP_SELECT_HOUSE_SARDAUKAR**) | 144 | `resources/bin/data/sdl_inter_hd4.dat` | null |
| pack_index_missing | `src/data/gfxmentat.h@a51b97f:72` (**MENTATS**) | 51 | `resources/bin/data/sdl_mentat_hd4.dat` | null |
| pack_index_taken | `src/data/gfxdata.h@a51b97f:188` (**EXPLOSION_CARRYALL**) | 167 | `resources/bin/data/sdl_data_hd4.dat` | HM_BUILD_REFINERY |

Коллизия индекса 167 — подтверждённый факт: в `resources/bin/data/sdl_data_hd4.dat` запись HM_BUILD_REFINERY занимает индекс, который апстрим отдал EXPLOSION_CARRYALL. См. [PavelSlaven/DUNE#2](https://github.com/PavelSlaven/DUNE/issues/2) и шаг Б2 плана. На Б2 нужно согласовать таблицы и содержимое паков до переноса масок. Содержание issue по сети на Б0 не запрашивалось; факт установлен чтением локального пака и закреплённого заголовка.

Правило сканирования не отличает индекс от другой числовой константы. Среди найденных трёх записей случая «не индекс» нет: EXPLOSION_CARRYALL используется в `src/context/cInfoContextCreator.cpp@a51b97f:800` (**EXPLOSION_CARRYALL**); BMP_SELECT_HOUSE_SARDAUKAR передаётся в getTexture в `src/gamestates/cChooseHouseState.cpp@a51b97f:63` (**BMP_SELECT_HOUSE_SARDAUKAR**). MENTATS присваивается iBackgroundFrame в `src/gameobjects/mentat/SardaukarMentat.cpp@a51b97f:32` (**iBackgroundFrame = MENTATS**), который передаётся в getTexture в `src/gameobjects/mentat/AbstractMentat.cpp@a51b97f:316` (**getTexture(iBackgroundFrame)**).

## Аддитивное

Новые пути FORK со статусом A и upstream=null — кандидаты для копирования исходников и данных; таблица считает каждый путь один раз. Сначала переносится содержимое, затем проверяется интеграция по классу функции. Наличие нового пути не доказывает совместимость его include, API или runtime-контракта.

| Каталог | Новые пути для копирования |
|---|---:|
| .github/workflows | 1 |
| README_AI.md | 1 |
| docs/screenshots | 5 |
| packaging | 4 |
| resources/bin | 152 |
| resources/hd | 1723 |
| src/audio | 5 |
| src/controls | 2 |
| src/drawers | 6 |
| src/gameobjects | 1 |
| src/gamestates | 3 |
| src/save | 7 |
| src/sidebar | 2 |
| src/utils | 14 |
| tests | 20 |
| tools | 210 |

`README_AI.md`, HD-мастера, инструменты и снимки переносятся как исходные материалы. Тесты сохраняются все; SDL2-зависимые подключения адаптируются по списку ниже. Регистрацию целей из `CMakeLists.txt` применяют заново. Тексты packaging обновляют под новые зависимости. Совместимость инструментов с будущими паками не проверена.

## SDL2 в коде форка

Счётчик собирает токены с префиксами SDL_, Mix_, MIX_, IMG_, TTF_ и пути SDL2/<файл> из #include. Подтверждёнными считаются все токены, встретившиеся хотя бы в одном файле src/ в UP0. В каждом добавленном, изменённом или перемещённом форком src-файле считаются строки FORK с токеном вне подтверждённого множества; несколько токенов в строке дают одну строку. Файлы с нулём строк исключены. Шаблоны замен из diff не используются.

По JSON: 305 строк в 49 файлах. Наибольшие значения:

| Путь FORK | lines |
|---|---:|
| `src/drawers/SDLDrawer.cpp` | 39 |
| `src/utils/cDataPack.cpp` | 37 |
| `src/utils/cSoundPlayer.cpp` | 32 |
| `src/cGame_logic.cpp` | 27 |
| `src/utils/cPack.cpp` | 23 |
| `src/player/cPlayer.cpp` | 20 |
| `src/utils/Graphics.cpp` | 17 |
| `src/utils/cScreenInit.cpp` | 11 |
| `src/drawers/cTextTextureCache.cpp` | 10 |
| `src/gamestates/cSelectYourNextConquestState.cpp` | 10 |

Подсчёт не видит функции, у которых в SDL3 сохранилось имя, но изменилась сигнатура.

SDL2 прямо или транзитивно подключают 10 из 20 тестов. Семь тестов без собственного прямого SDL2 include приходят к `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**); RenderTargetStateTests дополнительно имеет прямое подключение и тоже достигает cRectangle. Ниже полные цепочки подключений для каждого из десяти тестов:

- `tests/CampaignMapLayoutTests.cpp`:
  - `tests/CampaignMapLayoutTests.cpp@6662b2f:1` (**gamestates/CampaignMapLayout.hpp**) → `src/gamestates/CampaignMapLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
- `tests/CommandBarLayoutTests.cpp`:
  - `tests/CommandBarLayoutTests.cpp@6662b2f:1` (**drawers/CommandBarLayout.hpp**) → `src/drawers/CommandBarLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
- `tests/CommandBindingsTests.cpp`:
  - `tests/CommandBindingsTests.cpp@6662b2f:2` (**controls/CommandBindings.hpp**) → `src/controls/CommandBindings.hpp@6662b2f:3` (**SDL2/SDL.h**).
  - `tests/CommandBindingsTests.cpp@6662b2f:3` (**controls/cKeyboardEvent.h**) → `src/controls/cKeyboardEvent.h@6662b2f:9` (**utils/common.h**) → `src/utils/common.h@6662b2f:19` (**SDL2/SDL.h**).
- `tests/FontCoverageTests.cpp`:
  - `tests/FontCoverageTests.cpp@6662b2f:2` (**SDL2/SDL_ttf.h**).
  - `tests/FontCoverageTests.cpp@6662b2f:3` (**utils/FontSupport.hpp**) → `src/utils/FontSupport.hpp@6662b2f:3` (**SDL2/SDL_ttf.h**).
- `tests/HdPresentationTests.cpp`:
  - `tests/HdPresentationTests.cpp@6662b2f:2` (**utils/OutcomeScreenLayout.hpp**) → `src/utils/OutcomeScreenLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
  - `tests/HdPresentationTests.cpp@6662b2f:3` (**utils/TextAlignment.hpp**) → `src/utils/TextAlignment.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
- `tests/HudLayoutTests.cpp`:
  - `tests/HudLayoutTests.cpp@6662b2f:1` (**sidebar/HudLayout.hpp**) → `src/sidebar/HudLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
- `tests/InteractionRegressionTests.cpp`:
  - `tests/InteractionRegressionTests.cpp@6662b2f:4` (**gamestates/AdvancedOptionsHeaderLayout.hpp**) → `src/gamestates/AdvancedOptionsHeaderLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
- `tests/MusicControlsLayoutTests.cpp`:
  - `tests/MusicControlsLayoutTests.cpp@6662b2f:1` (**sidebar/HudLayout.hpp**) → `src/sidebar/HudLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
  - `tests/MusicControlsLayoutTests.cpp@6662b2f:2` (**sidebar/MusicControlsLayout.hpp**) → `src/sidebar/MusicControlsLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
- `tests/OptionsMenuLayoutTests.cpp`:
  - `tests/OptionsMenuLayoutTests.cpp@6662b2f:1` (**gamestates/OptionsMenuLayout.hpp**) → `src/gamestates/OptionsMenuLayout.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
- `tests/RenderTargetStateTests.cpp`:
  - `tests/RenderTargetStateTests.cpp@6662b2f:3` (**drawers/SDLDrawer.hpp**) → `src/drawers/SDLDrawer.hpp@6662b2f:3` (**utils/cRectangle.h**) → `src/utils/cRectangle.h@6662b2f:4` (**SDL2/SDL_rect.h**).
  - `tests/RenderTargetStateTests.cpp@6662b2f:3` (**drawers/SDLDrawer.hpp**) → `src/drawers/SDLDrawer.hpp@6662b2f:4` (**utils/Color.hpp**) → `src/utils/Color.hpp@6662b2f:3` (**SDL2/SDL_pixels.h**).
  - `tests/RenderTargetStateTests.cpp@6662b2f:3` (**drawers/SDLDrawer.hpp**) → `src/drawers/SDLDrawer.hpp@6662b2f:8` (**SDL2/SDL.h**).
  - `tests/RenderTargetStateTests.cpp@6662b2f:4` (**include/Texture.hpp**) → `src/include/Texture.hpp@6662b2f:2` (**SDL2/SDL.h**).
  - `tests/RenderTargetStateTests.cpp@6662b2f:6` (**SDL2/SDL.h**).

## Риски переноса

- `src/cGame_logic.cpp` и `src/cGame.h` удалены по JSON. Перенос целого старого файла вернёт прежнее владение состоянием. Преемники перечислены у функций; распределение RU/HD-кода между ними требует реализации и тестов следующих шагов.
- `src/save/SaveGameManager.cpp` — новый путь без пересечения с апстримом, но его include указывают на прежние cGame и d2tmc. Поэтому отсутствие overlap не разрешает копировать интеграцию сохранений; ссылки на подключения приведены в save-slots.
- `src/drawers/SDLDrawer.cpp`, `src/utils/cDataPack.cpp`, `src/utils/cPack.cpp`, `src/utils/cSoundPlayer.cpp`: JSON показывает одновременно изменения сторон и неподтверждённые SDL-токены. Копирование прежней реализации затронет новые API рендера, ввода-вывода и аудио; механическая замена имён не проверена.
- `src/utils/GameSettings.hpp` перемещён в `src/utils/InitialGameSettings.hpp`; runtime-настройки представлены отдельно: `src/game/cGameSettings.h@a51b97f:20` (**class cGameSettings**). Параметры HD, языка, музыки и клавиш нужно распределить по времени жизни, а не переносить только старую структуру.
- `src/managers/cInteractionManager.cpp` удалён; входные события находятся в `src/gamestates/cGamePlaying.cpp@a51b97f:304` (**cGamePlaying::onNotifyMouseEvent**). Рассылку событий панели приказов нужно встроить в cGamePlaying, сохранив порядок контекста, камеры и остальных получателей.
- `resources/bin/data/sdl_inter.dat` — пересечение M/M; выбор одного целого пака потеряет изменения другой стороны. `resources/bin/data/sdl_data_hd4.dat` несёт подтверждённую коллизию 167; `resources/bin/data/sdl_inter_hd4.dat` и `resources/bin/data/sdl_mentat_hd4.dat` не содержат индексов новых картинок Сардаукаров. Разбор и согласование относятся к Б2.
- Два набора сцен FORK: resources/bin/data/scenes/hd4 содержит 18 DAT непосредственно в каталоге, а resources/bin/data/scenes/hd4/hd4 — ещё 18 DAT. У всех 18 одноимённых пар разные oid LFS. Пример: `resources/bin/data/scenes/hd4/sdl_ix.dat@6662b2f:2` (**sha256:22ae115b4f82698918be5854746883ee1c37d34e5bb51d8c10a46e86fc6da6a6**) и `resources/bin/data/scenes/hd4/hd4/sdl_ix.dat@6662b2f:2` (**sha256:c13e88db4ac518f9e7ab31f416dcdaa1b199af01beb2b5bd7125501a960476d0**). Загрузчик `src/mentat/AbstractMentat.cpp@6662b2f:692` (**data/scenes/hd4/sdl_{}.dat**) проверяет только прямой набор scenes/hd4. Вложенный набор scenes/hd4/hd4 кодом src/ в FORK не читается: путь hd4/hd4 в исходниках отсутствует. Выбор сохраняемого набора при упаковке относится к Б11.
- `resources/bin/skirmish_en/4PL_Sin├йadPlains.ini`: JSON фиксирует rename из `resources/bin/skirmish/4PL_SinéadPlains.ini`. Написание имени изменилось вместе с языковым каталогом; разрешение имени на целевых платформах не проверено.
- `src/utils/FontSupport.hpp` и `tests/FontCoverageTests.cpp` зависят от SDL2_ttf через подключения в реестре. Проверка кириллицы с настоящим шрифтом после миграции относится к Б7.
- `.github/workflows/release.yml` — новый путь форка, однако `CMakeLists.txt` пересекается с апстримом. Старые команды выпуска и комплект зависимостей нельзя считать проверенными для UP0; платформенные сборки относятся к Б12.
- Отнесение путей к функциям проверено маркерами в одну сторону: тест 6 ловит недостающих владельцев, но не лишних. Около 85 отнесений у 46 путей кода не подтверждены ни одним маркером, а маркеры renderStrechSprite, buttonWidth, renderTargetStack, TTF_SizeUTF8, m_titleBmp, UNIT_RAIDER и CMAKE_CXX_COMPILER_ID встречаются и в коде апстрима. Исполнитель шага переноса сверяет список путей своей функции с диффом BASE..FORK этих путей.

## Сверка чисел плана

В шаге Б0 и §3.2 перечислены исходные оценки объёма. Следующие строки уточняют каждое несовпадение объёма или смысла статуса по JSON:

- «184 изменённых форком файла» в шаге Б0: 184 = 183 M + 1 операция R среди прежних путей; JSON хранит R дважды, на исходном и целевом пути. Полный объём с добавлениями: 2156 A + 183 M + 1 R = 2340 операций, или 2341 запись путей. Охват функций проверяется для всех 2341 записей, а не только для прежних файлов.
- «20 удалённых файлов» в §3.2: среди overlap апстрим имеет 14 D + 6 исходных R = 20 путей с переносом интеграции; буквально удалённых по Git — 14, остальные 6 перемещены.
- «Не меньше 118 конфликтных файлов» в §3.2: 118 = 98 M + 14 D + 6 исходных R апстрима среди путей overlap. JSON подтверждает пересечение изменений, но не число фактических конфликтов merge; merge на Б0 не выполнялся.

Число 20 «удалённых или перенесённых» из шага Б0 совпадает с 14 D + 6 R. Для проверки границ подсчёта кодовый объём из §1.2 также воспроизводится: src/ + tests/ + корневой CMakeLists.txt дают для форка 114 M + 60 A = 174 операции, +15 654 / −1 262 строки; для апстрима 197 M + 176 A + 48 D + 49 R = 470 операций, +40 438 / −18 467 строк. В суммах строки каждого rename учитываются один раз. Эти 174 и 470 не описывают все ресурсы и инструменты дерева.

Итоговый объединённый раздел paths содержит 3076 записей. Полный FORK: 2156 A + 183 M + 2 границы R; полный UP0: 312 A + 219 M + 214 D + 108 границ R (54 операции). Коммиты BASE..FORK: 13. Тестовые файлы tests/*.cpp: 20 у форка и 15 в UP0. Источник статусов и соответствия функциям — JSON, источник состава и назначения тестов — реестр подключений выше.
