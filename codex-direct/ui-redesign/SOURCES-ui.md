# SOURCES-ui — справочник «что | где» для переработки интерфейса DUNE

Дата сверки: 2026-11-11. Ревизии: `PORT` = `origin/port/up-d06f2fcd` (вершина `91416fb0c6aae877242d55e08559c32ec80de3e0`), `FORK` = `origin/main`; `docs/` — рабочая копия как есть. В «Где» для списков файлов указан путь файла целиком, без строки. «не сверено» — там, где сверка не удалась.

## 0. Ревизии и границы сверки

| Что | Где |
|---|---|
| PORT: `origin/port/up-d06f2fcd` | сначала отсутствовала в локальных ссылках (`git rev-parse --verify` пусто); после сообщения координатора загружена, резолвится в `91416fb0c`; все команды по PORT повторены с этим именем |
| FORK: `origin/main` | локальная ссылка есть |
| Рабочая копия (ветка `docs/p5`): `docs/upstream/PORT_PLAN.md` | файл изменён и не закоммичен (`git status`: M); текст взят из рабочей копии |

## 1. Решения владельца об интерфейсе и графике

`docs/decisions.md`: строки, где встречается одно из слов интерфейс, HUD, меню, боков, панел, кнопк, шрифт, HD, масштаб, экран, ментат, титр (без учёта регистра). Строк: 33. Проверка: набор строк, найденный скриптом, совпал с таблицей; номер Р в каждой строке совпал с текстом.

| Что | Где |
|---|---|
| — — заголовок раздела «Техника Sega-HD и обновление с апстримом» (2026-10-28) | docs/decisions.md:5 |
| Р5 — сохранения v0.8.0-ru-hd.7 после обновления объявлены несовместимыми; конвертер не пишется | docs/decisions.md:13 |
| Р12 — угол камеры юнитов θ = 63° (`elevation_deg` в `resources/hd/units3d/common/camera.json`), по листу сравнения 55–72° рядом со зданиями HD4 | docs/decisions.md:20 |
| Р15 — осадный по размеру как Девастатор: длина модели 8,2 м (131 px HD4 при 16 px/м) вместо 7,0 м | docs/decisions.md:23 |
| Р16 — HD-кадр Осадного 176×176 вместо 144×144; классический кадр 36×36 не меняется | docs/decisions.md:24 |
| Р18 — покраска 3D-юнитов при рендере — матовая краска Дома для всех юнитов; собственные цвет и блеск модели Tripo не берутся | docs/decisions.md:26 |
| Р19 — пилот 3D-рендера не принят владельцем («Новые юниты выглядят хуже старых»); проба пути Г | docs/decisions.md:27 |
| Р20 — цель — перерисовать имеющиеся HD4-спрайты юнитов под угол 63°; 3D-модели Tripo не используются | docs/decisions.md:28 |
| Р22 — все юниты одной задачей, автономно, на servak; план `docs/units/REDRAW_PLAN.md`, ветка интеграции `units63/main` | docs/decisions.md:30 |
| Р24 — масштаб юнитов — вариант D сверки размеров: коэффициент юнита — квадратный корень из коэффициента при реальных размерах, с ограничением | docs/decisions.md:32 |
| Р28 — Осадный крупнее Танка, цвет Дома на крупных плитах, аудит интерфейса (карточка `codex-direct/launch-card-10.md`) | docs/decisions.md:36 |
| Р30 — проверки интерфейса: весь интерфейс без наложений и конфликтов; скрипт находит наложения при каждом масштабе игры и размере объектов | docs/decisions.md:38 |
| Р32 — чинить всё, что нашла проверка поворота; размер по направлениям — по трём опорам (классика, старый HD-пак, проекция `block` под 63°) | docs/decisions.md:40 |
| Р33 — масштаб мира — приближение камеры (#38): 100, 110, 125, 150 % или авто; задаёт приближение в начале миссии и после сброса клавишей Z | docs/decisions.md:41 |
| Р34 — только HD-графика; режим «Классика», его выбор в окне настроек и откат на классику убираются | docs/decisions.md:42 |
| Р36 — удаляются `resources/bin/data/scenes/hd4/hd4/` и `resources/bin/CLASSIC_WORLD_TRIAL_RU.txt`; в истории git остаются | docs/decisions.md:47 |
| Р37 — звуковой танк перерисован по своему HD4-спрайту (Р20); Sega-референс не нужен; #4 и #6 закрыты | docs/decisions.md:48 |
| Р39 — источник истины четырёх юнитов — их записи в паке `resources/bin/data/sdl_data_hd4.dat` | docs/decisions.md:50 |
| Р41 — релиз `v0.8.0-ru-hd.8` — после слияния волны 2 карточки 14 одной тестовой сборкой и «да» владельца | docs/decisions.md:52 |
| Р43 — волна 2 (U26, U29, U31) принята владельцем; PR #76, #78, #77; затем релиз `v0.8.0-ru-hd.8` | docs/decisions.md:54 |
| Р46 — заборов и ворот у зданий нет: перила, ворота, двери и люки в передней стене убираются у всех зданий, кроме Казарм, WOR, Дворца и Ремонта | docs/decisions.md:75 |
| Р49 — площадка у Лёгкого (правая половина) и Тяжёлого (правая треть) заводов, как у Переработки | docs/decisions.md:78 |
| Р51 — аккуратный минимализм: заполнение по Р50 мелкими частями отклонено; бока Командного поста как у Казарм | docs/decisions.md:80 |
| Р53 — юнит выезжает с площадки завода; общей анимации сборки танка в отсеке Тяжёлого завода нет; U39 до релиза | docs/decisions.md:82 |
| Р55 — U39 принят владельцем 2026-11-06, PR #90 и #91 слиты; Командный пост (радар) перерисовывается в стиле зданий Р47 | docs/decisions.md:84 |
| Р56 — U40 принят, релиз `v0.8.0-ru-hd.9`; тарелка Командного поста — 32 кадра атласа `BUILD_RADAR` по 11,25° | docs/decisions.md:85 |
| Р57 — итог U38: проверка всех зданий нашла 6 расхождений (`codex-direct/U38/REPORT.md`), исправляются следующей задачей | docs/decisions.md:86 |
| Р62 — U45 принят, релиз `v0.8.0-ru-hd.10` с карточками U44 и правками зданий U41–U45 | docs/decisions.md:91 |
| Р65 — HD-версии четырёх новых картинок апстрима (выбор дома Сардаукаров `BMP_SELECT_HOUSE_SARDAUKAR`, фон ментата `MENTATS` и др.); исключение из Р63 | docs/decisions.md:94 |
| Р66 — «Масштаб игры» форка (100–200 % и «Авто» по высоте экрана) вместо фиксированного размера и `ScalingMode` апстрима | docs/decisions.md:95 |
| Р68 — цвет Сардаукаров в масках Дома — пурпур форка `255,0,255`, как `SARDAUKAR_MINIMAPCOLOR` форка (владелец 2026-11-10) | docs/decisions.md:97 |
| Р69 — масштабы из `preferences.ini` при каждом запуске: порт читает ini при запуске только с ключом `-prefs`; исключение из Р63 | docs/decisions.md:98 |
| Р71 — переработка всего визуального интерфейса — задача Fable (владелец, 2026-11-11: «надо переработать весь визуальный интерфейс»); исполнитель — сессия Claude Fable 5.2 `xhigh` | docs/decisions.md:100 |

## 2. Код интерфейса в PORT

`git ls-tree -r --name-only origin/port/up-d06f2fcd -- src/gui src/drawers src/gamestates src/sidebar src/gameobjects/mentat`: файлов 128. По папкам:

### src/drawers (32)

| Что | Где |
|---|---|
| CreditsDrawer.cpp | `src/drawers/CreditsDrawer.cpp`@PORT |
| CreditsDrawer.h | `src/drawers/CreditsDrawer.h`@PORT |
| CreditsMath.hpp | `src/drawers/CreditsMath.hpp`@PORT |
| SDLDrawer.cpp | `src/drawers/SDLDrawer.cpp`@PORT |
| SDLDrawer.hpp | `src/drawers/SDLDrawer.hpp`@PORT |
| TerrainVariation.hpp | `src/drawers/TerrainVariation.hpp`@PORT |
| cBuildingListDrawer.cpp | `src/drawers/cBuildingListDrawer.cpp`@PORT |
| cBuildingListDrawer.h | `src/drawers/cBuildingListDrawer.h`@PORT |
| cMapDrawer.cpp | `src/drawers/cMapDrawer.cpp`@PORT |
| cMapDrawer.h | `src/drawers/cMapDrawer.h`@PORT |
| cMessageDrawer.cpp | `src/drawers/cMessageDrawer.cpp`@PORT |
| cMessageDrawer.h | `src/drawers/cMessageDrawer.h`@PORT |
| cMiniMapDrawer.cpp | `src/drawers/cMiniMapDrawer.cpp`@PORT |
| cMiniMapDrawer.h | `src/drawers/cMiniMapDrawer.h`@PORT |
| cMouseDrawer.cpp | `src/drawers/cMouseDrawer.cpp`@PORT |
| cMouseDrawer.h | `src/drawers/cMouseDrawer.h`@PORT |
| cOrderDrawer.cpp | `src/drawers/cOrderDrawer.cpp`@PORT |
| cOrderDrawer.h | `src/drawers/cOrderDrawer.h`@PORT |
| cParticleDrawer.cpp | `src/drawers/cParticleDrawer.cpp`@PORT |
| cParticleDrawer.h | `src/drawers/cParticleDrawer.h`@PORT |
| cPlaceItDrawer.cpp | `src/drawers/cPlaceItDrawer.cpp`@PORT |
| cPlaceItDrawer.h | `src/drawers/cPlaceItDrawer.h`@PORT |
| cSideBarDrawer.cpp | `src/drawers/cSideBarDrawer.cpp`@PORT |
| cSideBarDrawer.h | `src/drawers/cSideBarDrawer.h`@PORT |
| cStructureDrawer.cpp | `src/drawers/cStructureDrawer.cpp`@PORT |
| cStructureDrawer.h | `src/drawers/cStructureDrawer.h`@PORT |
| cTextDrawer.cpp | `src/drawers/cTextDrawer.cpp`@PORT |
| cTextDrawer.h | `src/drawers/cTextDrawer.h`@PORT |
| cTextTextureCache.cpp | `src/drawers/cTextTextureCache.cpp`@PORT |
| cTextTextureCache.h | `src/drawers/cTextTextureCache.h`@PORT |
| cUnitDrawer.cpp | `src/drawers/cUnitDrawer.cpp`@PORT |
| cUnitDrawer.h | `src/drawers/cUnitDrawer.h`@PORT |

### src/gameobjects/mentat (12)

| Что | Где |
|---|---|
| AbstractMentat.cpp | `src/gameobjects/mentat/AbstractMentat.cpp`@PORT |
| AbstractMentat.h | `src/gameobjects/mentat/AbstractMentat.h`@PORT |
| AtreidesMentat.cpp | `src/gameobjects/mentat/AtreidesMentat.cpp`@PORT |
| AtreidesMentat.h | `src/gameobjects/mentat/AtreidesMentat.h`@PORT |
| BeneMentat.cpp | `src/gameobjects/mentat/BeneMentat.cpp`@PORT |
| BeneMentat.h | `src/gameobjects/mentat/BeneMentat.h`@PORT |
| HarkonnenMentat.cpp | `src/gameobjects/mentat/HarkonnenMentat.cpp`@PORT |
| HarkonnenMentat.h | `src/gameobjects/mentat/HarkonnenMentat.h`@PORT |
| OrdosMentat.cpp | `src/gameobjects/mentat/OrdosMentat.cpp`@PORT |
| OrdosMentat.h | `src/gameobjects/mentat/OrdosMentat.h`@PORT |
| SardaukarMentat.cpp | `src/gameobjects/mentat/SardaukarMentat.cpp`@PORT |
| SardaukarMentat.h | `src/gameobjects/mentat/SardaukarMentat.h`@PORT |

### src/gamestates (36)

| Что | Где |
|---|---|
| CampaignMapLayout.hpp | `src/gamestates/CampaignMapLayout.hpp`@PORT |
| OptionsMenuLayout.hpp | `src/gamestates/OptionsMenuLayout.hpp`@PORT |
| cChooseHouseState.cpp | `src/gamestates/cChooseHouseState.cpp`@PORT |
| cChooseHouseState.h | `src/gamestates/cChooseHouseState.h`@PORT |
| cCreatorState.cpp | `src/gamestates/cCreatorState.cpp`@PORT |
| cCreatorState.h | `src/gamestates/cCreatorState.h`@PORT |
| cCreditsState.cpp | `src/gamestates/cCreditsState.cpp`@PORT |
| cCreditsState.h | `src/gamestates/cCreditsState.h`@PORT |
| cEditorState.cpp | `src/gamestates/cEditorState.cpp`@PORT |
| cEditorState.h | `src/gamestates/cEditorState.h`@PORT |
| cGamePlaying.cpp | `src/gamestates/cGamePlaying.cpp`@PORT |
| cGamePlaying.h | `src/gamestates/cGamePlaying.h`@PORT |
| cGameState.cpp | `src/gamestates/cGameState.cpp`@PORT |
| cGameState.h | `src/gamestates/cGameState.h`@PORT |
| cMainMenuState.cpp | `src/gamestates/cMainMenuState.cpp`@PORT |
| cMainMenuState.h | `src/gamestates/cMainMenuState.h`@PORT |
| cMentatState.cpp | `src/gamestates/cMentatState.cpp`@PORT |
| cMentatState.h | `src/gamestates/cMentatState.h`@PORT |
| cNewMapEditorState.h | `src/gamestates/cNewMapEditorState.h`@PORT |
| cNewmapEditorState.cpp | `src/gamestates/cNewmapEditorState.cpp`@PORT |
| cOptionsState.cpp | `src/gamestates/cOptionsState.cpp`@PORT |
| cOptionsState.h | `src/gamestates/cOptionsState.h`@PORT |
| cScoringState.cpp | `src/gamestates/cScoringState.cpp`@PORT |
| cScoringState.h | `src/gamestates/cScoringState.h`@PORT |
| cSelectMissionState.cpp | `src/gamestates/cSelectMissionState.cpp`@PORT |
| cSelectMissionState.h | `src/gamestates/cSelectMissionState.h`@PORT |
| cSelectYourNextConquestState.cpp | `src/gamestates/cSelectYourNextConquestState.cpp`@PORT |
| cSelectYourNextConquestState.h | `src/gamestates/cSelectYourNextConquestState.h`@PORT |
| cSetupSkirmishState.cpp | `src/gamestates/cSetupSkirmishState.cpp`@PORT |
| cSetupSkirmishState.h | `src/gamestates/cSetupSkirmishState.h`@PORT |
| cTellHouseState.cpp | `src/gamestates/cTellHouseState.cpp`@PORT |
| cTellHouseState.h | `src/gamestates/cTellHouseState.h`@PORT |
| cVideoState.cpp | `src/gamestates/cVideoState.cpp`@PORT |
| cVideoState.h | `src/gamestates/cVideoState.h`@PORT |
| cWinLoseState.cpp | `src/gamestates/cWinLoseState.cpp`@PORT |
| cWinLoseState.h | `src/gamestates/cWinLoseState.h`@PORT |

### src/gamestates/cEditorState (4)

| Что | Где |
|---|---|
| cEditorCam.cpp | `src/gamestates/cEditorState/cEditorCam.cpp`@PORT |
| cEditorCam.h | `src/gamestates/cEditorState/cEditorCam.h`@PORT |
| cEditorUndoRedoHistory.cpp | `src/gamestates/cEditorState/cEditorUndoRedoHistory.cpp`@PORT |
| cEditorUndoRedoHistory.h | `src/gamestates/cEditorState/cEditorUndoRedoHistory.h`@PORT |

### src/gui (29)

| Что | Где |
|---|---|
| GuiBar.cpp | `src/gui/GuiBar.cpp`@PORT |
| GuiBar.h | `src/gui/GuiBar.h`@PORT |
| GuiButton.cpp | `src/gui/GuiButton.cpp`@PORT |
| GuiButton.h | `src/gui/GuiButton.h`@PORT |
| GuiButtonGroup.cpp | `src/gui/GuiButtonGroup.cpp`@PORT |
| GuiButtonGroup.h | `src/gui/GuiButtonGroup.h`@PORT |
| GuiCheckBox.cpp | `src/gui/GuiCheckBox.cpp`@PORT |
| GuiCheckBox.hpp | `src/gui/GuiCheckBox.hpp`@PORT |
| GuiConsole.cpp | `src/gui/GuiConsole.cpp`@PORT |
| GuiConsole.h | `src/gui/GuiConsole.h`@PORT |
| GuiCycleButton.cpp | `src/gui/GuiCycleButton.cpp`@PORT |
| GuiCycleButton.h | `src/gui/GuiCycleButton.h`@PORT |
| GuiLabel.cpp | `src/gui/GuiLabel.cpp`@PORT |
| GuiLabel.hpp | `src/gui/GuiLabel.hpp`@PORT |
| GuiObject.cpp | `src/gui/GuiObject.cpp`@PORT |
| GuiObject.h | `src/gui/GuiObject.h`@PORT |
| GuiSlider.cpp | `src/gui/GuiSlider.cpp`@PORT |
| GuiSlider.hpp | `src/gui/GuiSlider.hpp`@PORT |
| GuiStateButton.cpp | `src/gui/GuiStateButton.cpp`@PORT |
| GuiStateButton.h | `src/gui/GuiStateButton.h`@PORT |
| GuiTextInput.cpp | `src/gui/GuiTextInput.cpp`@PORT |
| GuiTextInput.h | `src/gui/GuiTextInput.h`@PORT |
| GuiTheme.hpp | `src/gui/GuiTheme.hpp`@PORT |
| GuiValueButton.cpp | `src/gui/GuiValueButton.cpp`@PORT |
| GuiValueButton.h | `src/gui/GuiValueButton.h`@PORT |
| GuiWindow.cpp | `src/gui/GuiWindow.cpp`@PORT |
| GuiWindow.h | `src/gui/GuiWindow.h`@PORT |
| cTextWriter.cpp | `src/gui/cTextWriter.cpp`@PORT |
| cTextWriter.h | `src/gui/cTextWriter.h`@PORT |

### src/gui/GuiConsole (2)

| Что | Где |
|---|---|
| GuiConsoleMessageParser.cpp | `src/gui/GuiConsole/GuiConsoleMessageParser.cpp`@PORT |
| GuiConsoleMessageParser.h | `src/gui/GuiConsole/GuiConsoleMessageParser.h`@PORT |

### src/sidebar (13)

| Что | Где |
|---|---|
| HudLayout.hpp | `src/sidebar/HudLayout.hpp`@PORT |
| cBuildingList.cpp | `src/sidebar/cBuildingList.cpp`@PORT |
| cBuildingList.h | `src/sidebar/cBuildingList.h`@PORT |
| cBuildingListFactory.cpp | `src/sidebar/cBuildingListFactory.cpp`@PORT |
| cBuildingListFactory.h | `src/sidebar/cBuildingListFactory.h`@PORT |
| cBuildingListItem.cpp | `src/sidebar/cBuildingListItem.cpp`@PORT |
| cBuildingListItem.h | `src/sidebar/cBuildingListItem.h`@PORT |
| cBuildingListUpdater.cpp | `src/sidebar/cBuildingListUpdater.cpp`@PORT |
| cBuildingListUpdater.h | `src/sidebar/cBuildingListUpdater.h`@PORT |
| cSideBar.cpp | `src/sidebar/cSideBar.cpp`@PORT |
| cSideBar.h | `src/sidebar/cSideBar.h`@PORT |
| cSideBarFactory.cpp | `src/sidebar/cSideBarFactory.cpp`@PORT |
| cSideBarFactory.h | `src/sidebar/cSideBarFactory.h`@PORT |

### Определения, загрузчик, шрифты (PORT)

| Что | Где |
|---|---|
| `struct HudLayout {` | `src/sidebar/HudLayout.hpp:13`@PORT |
| `struct OptionsMenuLayout {` | `src/gamestates/OptionsMenuLayout.hpp:7`@PORT |
| `struct GuiTheme {` | `src/gui/GuiTheme.hpp:20`@PORT |
| `enum GuiRenderKind {` | `src/gui/GuiObject.h:27`@PORT |
| `class cTextDrawer {` (класс, определение) | `src/drawers/cTextDrawer.h:28`@PORT |
| `Texture *loadHdUiTexture(...)` — определение | `src/utils/HdUiTextureLoader.cpp:11`@PORT |
| `loadHdUiTexture(...)` — объявление | `src/utils/HdUiTextureLoader.hpp:8`@PORT |
| предобъявления `class cTextDrawer;` — строк: 34 | `git grep -n 'class cTextDrawer;' origin/port/up-d06f2fcd -- src`@PORT (список ниже) |
| `class cTextDrawer;` | `src/context/ContextCreator.hpp:26`@PORT |
| `class cTextDrawer;` | `src/context/TextContext.hpp:19`@PORT |
| `class cTextDrawer;` | `src/drawers/CreditsDrawer.h:28`@PORT |
| `class cTextDrawer;` | `src/drawers/cBuildingListDrawer.h:18`@PORT |
| `class cTextDrawer;` | `src/drawers/cParticleDrawer.h:21`@PORT |
| `class cTextDrawer;` | `src/drawers/cStructureDrawer.h:21`@PORT |
| `class cTextDrawer;` | `src/drawers/cUnitDrawer.h:21`@PORT |
| `class cTextDrawer;` | `src/game/cGame.h:42`@PORT |
| `class cTextDrawer;` | `src/game/cNotificationArea.h:22`@PORT |
| `class cTextDrawer;` | `src/gameobjects/map/cMap.h:36`@PORT |
| `class cTextDrawer;` | `src/gameobjects/mentat/AbstractMentat.h:35`@PORT |
| `class cTextDrawer;` | `src/gameobjects/mentat/BeneMentat.h:20`@PORT |
| `class cTextDrawer;` | `src/gamestates/cChooseHouseState.h:31`@PORT |
| `class cTextDrawer;` | `src/gamestates/cCreditsState.h:30`@PORT |
| `class cTextDrawer;` | `src/gamestates/cEditorState.h:36`@PORT |
| `class cTextDrawer;` | `src/gamestates/cGamePlaying.h:29`@PORT |
| `class cTextDrawer;` | `src/gamestates/cGamePlaying.h:38`@PORT |
| `class cTextDrawer;` | `src/gamestates/cMainMenuState.h:26`@PORT |
| `class cTextDrawer;` | `src/gamestates/cNewMapEditorState.h:26`@PORT |
| `class cTextDrawer;` | `src/gamestates/cOptionsState.h:30`@PORT |
| `class cTextDrawer;` | `src/gamestates/cScoringState.h:11`@PORT |
| `class cTextDrawer;` | `src/gamestates/cSelectMissionState.h:27`@PORT |
| `class cTextDrawer;` | `src/gamestates/cSelectYourNextConquestState.h:43`@PORT |
| `class cTextDrawer;` | `src/gamestates/cSetupSkirmishState.h:36`@PORT |
| `class cTextDrawer;` | `src/gamestates/cWinLoseState.h:28`@PORT |
| `class cTextDrawer;` | `src/gui/GuiButton.h:26`@PORT |
| `class cTextDrawer;` | `src/gui/GuiConsole.h:22`@PORT |
| `class cTextDrawer;` | `src/gui/GuiCycleButton.h:25`@PORT |
| `class cTextDrawer;` | `src/gui/GuiLabel.hpp:26`@PORT |
| `class cTextDrawer;` | `src/gui/GuiObject.h:25`@PORT |
| `class cTextDrawer;` | `src/gui/GuiTextInput.h:23`@PORT |
| `class cTextDrawer;` | `src/gui/GuiValueButton.h:25`@PORT |
| `class cTextDrawer;` | `src/gui/GuiWindow.h:24`@PORT |
| `class cTextDrawer;` | `src/gui/cTextWriter.h:32`@PORT |
| строки с `loadHdUiTexture(` (вызовы, определение и объявление) — всего: 15 | см. строки ниже |
| шрифт: `game_font = TTF_OpenFont(settingsValidator->getFullName(eGameDirFileName::ARRAKEEN).c_str(),12);` | `src/context/ContextCreator.cpp:78`@PORT |
| шрифт: `bene_font = TTF_OpenFont(settingsValidator->getFullName(eGameDirFileName::BENEGESS).c_str(),12);` | `src/context/ContextCreator.cpp:86`@PORT |
| шрифт: `small_font = TTF_OpenFont(settingsValidator->getFullName(eGameDirFileName::SMALL).c_str(),12);` | `src/context/ContextCreator.cpp:94`@PORT |
| `.ttf` в комментарии (не загружается) | `src/utils/cFileValidator.cpp:28`@PORT |

Вызовы `loadHdUiTexture(`:

| Что | Где |
|---|---|
| m_houseCrests[0] = loadHdUiTexture( | `src/drawers/cSideBarDrawer.cpp:56`@PORT |
| m_houseCrests[1] = loadHdUiTexture( | `src/drawers/cSideBarDrawer.cpp:61`@PORT |
| m_houseCrests[2] = loadHdUiTexture( | `src/drawers/cSideBarDrawer.cpp:66`@PORT |
| m_hdBackground = loadHdUiTexture( | `src/gamestates/cChooseHouseState.cpp:61`@PORT |
| m_teamBmp = loadHdUiTexture( | `src/gamestates/cCreditsState.cpp:53`@PORT |
| m_titleBmp = loadHdUiTexture( | `src/gamestates/cCreditsState.cpp:57`@PORT |
| m_hdMenuBackground = loadHdUiTexture( | `src/gamestates/cMainMenuState.cpp:91`@PORT |
| m_hdMenuLogo = loadHdUiTexture( | `src/gamestates/cMainMenuState.cpp:96`@PORT |
| m_hdBackground = loadHdUiTexture( | `src/gamestates/cSelectMissionState.cpp:74`@PORT |
| m_hdBackground = loadHdUiTexture( | `src/gamestates/cSelectYourNextConquestState.cpp:123`@PORT |
| m_hdCampaignMap = loadHdUiTexture( | `src/gamestates/cSelectYourNextConquestState.cpp:128`@PORT |
| m_hdHouseCrest = loadHdUiTexture( | `src/gamestates/cSelectYourNextConquestState.cpp:149`@PORT |
| m_hdOutcomeTexture = loadHdUiTexture( | `src/gamestates/cWinLoseState.cpp:60`@PORT |
| Texture *loadHdUiTexture(SDL_Renderer *renderer, const std::string &fileName, const std::string &logContext) | `src/utils/HdUiTextureLoader.cpp:11`@PORT |
| Texture *loadHdUiTexture(SDL_Renderer *renderer, const std::string &fileName, const std::string &logContext = "HD UI"); | `src/utils/HdUiTextureLoader.hpp:8`@PORT |

## 3. FORK (origin/main): только отличия от PORT

Те же папки. Общих путей: 75. Только в PORT: 53. Только в FORK: 9. Файлы, которые есть в обеих ревизиях, в таблицы не входят.

### Есть только в PORT (53)

| Что | Где |
|---|---|
| CreditsMath.hpp | `src/drawers/CreditsMath.hpp`@PORT |
| cUnitDrawer.cpp | `src/drawers/cUnitDrawer.cpp`@PORT |
| cUnitDrawer.h | `src/drawers/cUnitDrawer.h`@PORT |
| AbstractMentat.cpp | `src/gameobjects/mentat/AbstractMentat.cpp`@PORT |
| AbstractMentat.h | `src/gameobjects/mentat/AbstractMentat.h`@PORT |
| AtreidesMentat.cpp | `src/gameobjects/mentat/AtreidesMentat.cpp`@PORT |
| AtreidesMentat.h | `src/gameobjects/mentat/AtreidesMentat.h`@PORT |
| BeneMentat.cpp | `src/gameobjects/mentat/BeneMentat.cpp`@PORT |
| BeneMentat.h | `src/gameobjects/mentat/BeneMentat.h`@PORT |
| HarkonnenMentat.cpp | `src/gameobjects/mentat/HarkonnenMentat.cpp`@PORT |
| HarkonnenMentat.h | `src/gameobjects/mentat/HarkonnenMentat.h`@PORT |
| OrdosMentat.cpp | `src/gameobjects/mentat/OrdosMentat.cpp`@PORT |
| OrdosMentat.h | `src/gameobjects/mentat/OrdosMentat.h`@PORT |
| SardaukarMentat.cpp | `src/gameobjects/mentat/SardaukarMentat.cpp`@PORT |
| SardaukarMentat.h | `src/gameobjects/mentat/SardaukarMentat.h`@PORT |
| cCreatorState.cpp | `src/gamestates/cCreatorState.cpp`@PORT |
| cCreatorState.h | `src/gamestates/cCreatorState.h`@PORT |
| cEditorState.cpp | `src/gamestates/cEditorState.cpp`@PORT |
| cEditorState.h | `src/gamestates/cEditorState.h`@PORT |
| cEditorCam.cpp | `src/gamestates/cEditorState/cEditorCam.cpp`@PORT |
| cEditorCam.h | `src/gamestates/cEditorState/cEditorCam.h`@PORT |
| cEditorUndoRedoHistory.cpp | `src/gamestates/cEditorState/cEditorUndoRedoHistory.cpp`@PORT |
| cEditorUndoRedoHistory.h | `src/gamestates/cEditorState/cEditorUndoRedoHistory.h`@PORT |
| cGamePlaying.cpp | `src/gamestates/cGamePlaying.cpp`@PORT |
| cGamePlaying.h | `src/gamestates/cGamePlaying.h`@PORT |
| cMentatState.cpp | `src/gamestates/cMentatState.cpp`@PORT |
| cMentatState.h | `src/gamestates/cMentatState.h`@PORT |
| cNewMapEditorState.h | `src/gamestates/cNewMapEditorState.h`@PORT |
| cNewmapEditorState.cpp | `src/gamestates/cNewmapEditorState.cpp`@PORT |
| cScoringState.cpp | `src/gamestates/cScoringState.cpp`@PORT |
| cScoringState.h | `src/gamestates/cScoringState.h`@PORT |
| cTellHouseState.cpp | `src/gamestates/cTellHouseState.cpp`@PORT |
| cTellHouseState.h | `src/gamestates/cTellHouseState.h`@PORT |
| cVideoState.cpp | `src/gamestates/cVideoState.cpp`@PORT |
| cVideoState.h | `src/gamestates/cVideoState.h`@PORT |
| cWinLoseState.cpp | `src/gamestates/cWinLoseState.cpp`@PORT |
| cWinLoseState.h | `src/gamestates/cWinLoseState.h`@PORT |
| GuiBar.cpp | `src/gui/GuiBar.cpp`@PORT |
| GuiBar.h | `src/gui/GuiBar.h`@PORT |
| GuiButtonGroup.cpp | `src/gui/GuiButtonGroup.cpp`@PORT |
| GuiButtonGroup.h | `src/gui/GuiButtonGroup.h`@PORT |
| GuiConsole.cpp | `src/gui/GuiConsole.cpp`@PORT |
| GuiConsole.h | `src/gui/GuiConsole.h`@PORT |
| GuiConsoleMessageParser.cpp | `src/gui/GuiConsole/GuiConsoleMessageParser.cpp`@PORT |
| GuiConsoleMessageParser.h | `src/gui/GuiConsole/GuiConsoleMessageParser.h`@PORT |
| GuiCycleButton.cpp | `src/gui/GuiCycleButton.cpp`@PORT |
| GuiCycleButton.h | `src/gui/GuiCycleButton.h`@PORT |
| GuiStateButton.cpp | `src/gui/GuiStateButton.cpp`@PORT |
| GuiStateButton.h | `src/gui/GuiStateButton.h`@PORT |
| GuiTextInput.cpp | `src/gui/GuiTextInput.cpp`@PORT |
| GuiTextInput.h | `src/gui/GuiTextInput.h`@PORT |
| GuiValueButton.cpp | `src/gui/GuiValueButton.cpp`@PORT |
| GuiValueButton.h | `src/gui/GuiValueButton.h`@PORT |

### Есть только в FORK (9)

| Что | Где |
|---|---|
| CommandBarLayout.hpp | `src/drawers/CommandBarLayout.hpp`@FORK |
| CommandBarPolicy.hpp | `src/drawers/CommandBarPolicy.hpp`@FORK |
| OrderButtonPolicy.hpp | `src/drawers/OrderButtonPolicy.hpp`@FORK |
| cCommandBarDrawer.cpp | `src/drawers/cCommandBarDrawer.cpp`@FORK |
| cCommandBarDrawer.h | `src/drawers/cCommandBarDrawer.h`@FORK |
| AdvancedOptionsHeaderLayout.hpp | `src/gamestates/AdvancedOptionsHeaderLayout.hpp`@FORK |
| MouseToolTip.cpp | `src/gui/MouseToolTip.cpp`@FORK |
| MouseToolTip.h | `src/gui/MouseToolTip.h`@FORK |
| MusicControlsLayout.hpp | `src/sidebar/MusicControlsLayout.hpp`@FORK |

## 4. HD-картинки интерфейса

`git ls-tree -r --name-only origin/port/up-d06f2fcd -- data/hd4`: **0 путей** (искал: `data/hd4`; в PORT такой папки нет, `git ls-tree --name-only origin/port/up-d06f2fcd -- data/` пуст). Ближайшая папка с HD4-картинками в PORT: `resources/bin/data/hd4/`, файлов: 12. Ниже — она, с фильтром по подстроке в имени файла (без учёта регистра): ui, button, panel, sidebar, menu, outcome, mentat, font, icon, cursor, command, card, frame, bar.

| Что | Где |
|---|---|
| campaign_map.png — не совпало | `resources/bin/data/hd4/campaign_map.png`@PORT |
| credits_team.png — не совпало | `resources/bin/data/hd4/credits_team.png`@PORT |
| credits_title.png — не совпало | `resources/bin/data/hd4/credits_title.png`@PORT |
| hud_house_atreides.png — не совпало | `resources/bin/data/hd4/hud_house_atreides.png`@PORT |
| hud_house_harkonnen.png — не совпало | `resources/bin/data/hd4/hud_house_harkonnen.png`@PORT |
| hud_house_ordos.png — не совпало | `resources/bin/data/hd4/hud_house_ordos.png`@PORT |
| main_menu_background.png (совп.: menu) | `resources/bin/data/hd4/main_menu_background.png`@PORT |
| main_menu_logo.png (совп.: menu) | `resources/bin/data/hd4/main_menu_logo.png`@PORT |
| outcome_defeat_en.png (совп.: outcome) | `resources/bin/data/hd4/outcome_defeat_en.png`@PORT |
| outcome_defeat_ru.png (совп.: outcome) | `resources/bin/data/hd4/outcome_defeat_ru.png`@PORT |
| outcome_victory_en.png (совп.: outcome) | `resources/bin/data/hd4/outcome_victory_en.png`@PORT |
| outcome_victory_ru.png (совп.: outcome) | `resources/bin/data/hd4/outcome_victory_ru.png`@PORT |

Вне этой папки в PORT найдено путей с `hd4`: 31 (паки `resources/bin/data/sdl_*_hd4.dat`, `resources/bin/data/scenes/hd4/…`, `docs/upstream/p2/hd4_alignment_*.tsv`, тесты `tests/utils/test_Hd4*.cpp`, `tests/data/hd4_packs_expected.tsv`, `tools/upstream/align_hd4_packs.py`); их имена картинок не перечисляют — в список не входят.

## 5. Проверки и тесты интерфейса (PORT)

### tools/ui-audit/*.py (12)

| Что | Где |
|---|---|
| build_sheets.py | `tools/ui-audit/build_sheets.py`@PORT |
| check_completeness.py | `tools/ui-audit/check_completeness.py`@PORT |
| check_credits.py | `tools/ui-audit/check_credits.py`@PORT |
| check_geometry.py | `tools/ui-audit/check_geometry.py`@PORT |
| check_options_geometry.py | `tools/ui-audit/check_options_geometry.py`@PORT |
| check_scenes.py | `tools/ui-audit/check_scenes.py`@PORT |
| check_screens.py | `tools/ui-audit/check_screens.py`@PORT |
| combos.py | `tools/ui-audit/combos.py`@PORT |
| finalize_png.py | `tools/ui-audit/finalize_png.py`@PORT |
| find_hit_tests.py | `tools/ui-audit/find_hit_tests.py`@PORT |
| run_all.py | `tools/ui-audit/run_all.py`@PORT |
| run_combo.py | `tools/ui-audit/run_combo.py`@PORT |

### tests/ui_audit/*.py (5)

| Что | Где |
|---|---|
| ui_audit_list_and_scales.py | `tests/ui_audit/ui_audit_list_and_scales.py`@PORT |
| ui_audit_main_menu_png.py | `tests/ui_audit/ui_audit_main_menu_png.py`@PORT |
| ui_audit_runtime_support.py | `tests/ui_audit/ui_audit_runtime_support.py`@PORT |
| ui_audit_tools_run_combo.py | `tests/ui_audit/ui_audit_tools_run_combo.py`@PORT |
| ui_audit_unknown_scene.py | `tests/ui_audit/ui_audit_unknown_scene.py`@PORT |

Вложенные `tools/ui-audit/tests/*.py` (14) — не входят в `tools/ui-audit/*.py`, перечислены отдельно:

| Что | Где |
|---|---|
| test_build_sheets.py | `tools/ui-audit/tests/test_build_sheets.py`@PORT |
| test_check_completeness.py | `tools/ui-audit/tests/test_check_completeness.py`@PORT |
| test_check_credits.py | `tools/ui-audit/tests/test_check_credits.py`@PORT |
| test_check_geometry.py | `tools/ui-audit/tests/test_check_geometry.py`@PORT |
| test_check_options_geometry.py | `tools/ui-audit/tests/test_check_options_geometry.py`@PORT |
| test_check_scenes.py | `tools/ui-audit/tests/test_check_scenes.py`@PORT |
| test_check_screens.py | `tools/ui-audit/tests/test_check_screens.py`@PORT |
| test_combos.py | `tools/ui-audit/tests/test_combos.py`@PORT |
| test_extra_rules.py | `tools/ui-audit/tests/test_extra_rules.py`@PORT |
| test_find_hit_tests.py | `tools/ui-audit/tests/test_find_hit_tests.py`@PORT |
| test_png_policy.py | `tools/ui-audit/tests/test_png_policy.py`@PORT |
| test_png_policy_outputs.py | `tools/ui-audit/tests/test_png_policy_outputs.py`@PORT |
| test_port_changes.py | `tools/ui-audit/tests/test_port_changes.py`@PORT |
| test_run_all.py | `tools/ui-audit/tests/test_run_all.py`@PORT |

`git ls-tree -r --name-only origin/port/up-d06f2fcd -- tests src | grep -i layout`: строк 6. Тест с `layout` в имени — один; остальные — заголовки в `src/`:

| Что | Где |
|---|---|
| CampaignMapLayout.hpp (заголовок, не тест) | `src/gamestates/CampaignMapLayout.hpp`@PORT |
| OptionsMenuLayout.hpp (заголовок, не тест) | `src/gamestates/OptionsMenuLayout.hpp`@PORT |
| HudLayout.hpp (заголовок, не тест) | `src/sidebar/HudLayout.hpp`@PORT |
| OutcomeScreenLayout.hpp (заголовок, не тест) | `src/utils/OutcomeScreenLayout.hpp`@PORT |
| UnitSpriteLayout.hpp (заголовок, не тест) | `src/utils/UnitSpriteLayout.hpp`@PORT |
| test_HudLayout.cpp (тест) | `tests/utils/test_HudLayout.cpp`@PORT |

## 6. Документы о прошлых работах по интерфейсу (рабочая копия)

`rg -l -i -e интерфейс -e HUD -e GuiTheme -e Remaster docs codex-direct`. Путей всего: 174. Показаны первые 60 по алфавиту; остальные 114 — не сверено (не выведено по ограничению 60).

| Путь — заголовок | Где |
|---|---|
| codex-direct/P1/TASK-A.md — Задание P1A — карта переноса на свежий апстрим | codex-direct/P1/TASK-A.md:1 |
| codex-direct/P1/retell.md — DONE-P1-RETELL \| 2026-11-09 07:54:25 UTC | codex-direct/P1/retell.md:1 |
| codex-direct/P10/RECON.md — Задание P10R — разведка панели приказов и клавиш перед шагом П10 | codex-direct/P10/RECON.md:1 |
| codex-direct/P10/recon/RECON.md — RECON-P10R | codex-direct/P10/recon/RECON.md:1 |
| codex-direct/P10/recon/controls-tab.tsv | строки-заголовка нет; не сверено |
| codex-direct/P11/RECON.md — Задание P11R — разведка ментатов HD, сцен, титров и вступительного ролика перед шагом П11 | codex-direct/P11/RECON.md:1 |
| codex-direct/P11/recon/credits.tsv | строки-заголовка нет; не сверено |
| codex-direct/P11/recon/spotcheck-executor.md — Выборочная сверка | codex-direct/P11/recon/spotcheck-executor.md:1 |
| codex-direct/P12/RECON.md — Задание P12R — разведка упаковки релиза, workflows и галереи перед шагом П12 | codex-direct/P12/RECON.md:1 |
| codex-direct/P12/recon/SPOTCHECK.md — Сверка разведки П12 (Haiku) | codex-direct/P12/recon/SPOTCHECK.md:1 |
| codex-direct/P12/recon/gallery.tsv | строки-заголовка нет; не сверено |
| codex-direct/P12/recon/spotcheck-executor.md — Сверка таблиц P12R | codex-direct/P12/recon/spotcheck-executor.md:1 |
| codex-direct/P3/RECON.md — Задание P3-R — разведка загрузки HD4 перед шагом П3 | codex-direct/P3/RECON.md:1 |
| codex-direct/P3/TASK.md — Задание P3 — загрузка HD4 с плотностью 4 на коде апстрима | codex-direct/P3/TASK.md:1 |
| codex-direct/P4/PREREVIEW-B.md — Задание P4B-PR — предревью сдачи П4б | codex-direct/P4/PREREVIEW-B.md:1 |
| codex-direct/P4/PREREVIEW.md — Задание P4-PR — предревью сдачи П4а | codex-direct/P4/PREREVIEW.md:1 |
| codex-direct/P4/RECON-B.md — Задание P4B-R — разведка «Масштаба игры» перед шагом П4б | codex-direct/P4/RECON-B.md:1 |
| codex-direct/P4/RECON.md — Задание P4-R — разведка HD-рендера и масштаба мира перед шагом П4 | codex-direct/P4/RECON.md:1 |
| codex-direct/P4/TASK-B.md — Задание P4B — «Масштаб игры» форка на коде апстрима (шаг П4б) | codex-direct/P4/TASK-B.md:1 |
| codex-direct/P4/TASK-BT.md — Задание P4BT — приёмочные тесты «Масштаба игры» (шаг П4б) | codex-direct/P4/TASK-BT.md:1 |
| codex-direct/P4/TASK-T.md — Задание P4T — приёмочные тесты HD-кадра, масштаба мира, HD-кадров юнитов и флага ветряка | codex-direct/P4/TASK-T.md:1 |
| codex-direct/P4/TASK.md — Задание P4 — HD-кадр, масштаб мира, HD-кадры юнитов и флаг ветряка на коде апстрима (шаг П4а) | codex-direct/P4/TASK.md:1 |
| codex-direct/P4/recon-b/RECON.md — Разведка P4B-R: масштаб игры | codex-direct/P4/recon-b/RECON.md:1 |
| codex-direct/P5/CARD-C.md — Карточка запуска — П5в, боевой HUD | codex-direct/P5/CARD-C.md:1 |
| codex-direct/P5/CARD-G.md — Карточка запуска — П5г, режим отладки интерфейса, часть 1 (ядро) | codex-direct/P5/CARD-G.md:1 |
| codex-direct/P5/CARD-G2.md — Карточка запуска — П5г, режим отладки интерфейса, часть 2 (экраны вне боя) | codex-direct/P5/CARD-G2.md:1 |
| codex-direct/P5/CARD-T.md — Карточка запуска — П5г, режим отладки интерфейса, часть 4 (инструменты Python) | codex-direct/P5/CARD-T.md:1 |
| codex-direct/P5/PLAN-A.md — PLAN-P5A — план ведущего для шага П5а | codex-direct/P5/PLAN-A.md:1 |
| codex-direct/P5/RECON-B.md — Задание P5BR — разведка меню настроек перед шагом П5б | codex-direct/P5/RECON-B.md:1 |
| codex-direct/P5/RECON-C.md — Задание P5CR — разведка боевого HUD перед шагом П5в | codex-direct/P5/RECON-C.md:1 |
| codex-direct/P5/RECON-C2.md — Задание P5CR2 — разведка: участки HUD форка и их места в порту | codex-direct/P5/RECON-C2.md:1 |
| codex-direct/P5/RECON-D.md — Задание P5DR — разведка режима отладки интерфейса перед шагом П5г | codex-direct/P5/RECON-D.md:1 |
| codex-direct/P5/RECON-G.md — Задание P5GR — разведка порта под режим отладки интерфейса (шаг П5г) | codex-direct/P5/RECON-G.md:1 |
| codex-direct/P5/RECON-G2.md — Задание P5G2R — разведка порта под сцены меню, карты кампании, ментатов и титров (шаг П5г, часть 2) | codex-direct/P5/RECON-G2.md:1 |
| codex-direct/P5/RECON-G3.md — Задание P5G3R — разведка порта под боевые сцены и метки юнитов и зданий (шаг П5г, часть 3) | codex-direct/P5/RECON-G3.md:1 |
| codex-direct/P5/RECON-G3V.md — Задание P5G3V — разведка экранов апстрима без сцен режима отладки интерфейса (шаг П5г, часть 3в) | codex-direct/P5/RECON-G3V.md:1 |
| codex-direct/P5/RECON-T.md — Задание P5TR — разведка инструментов Python режима отладки интерфейса (шаг П5г, часть 4) | codex-direct/P5/RECON-T.md:1 |
| codex-direct/P5/RECON.md — Задание P5-R — разведка адаптивных меню и отладки интерфейса перед шагом П5 | codex-direct/P5/RECON.md:1 |
| codex-direct/P5/TASK-A.md — Задание P5A — адаптивные меню форка вне боя и HD-картинки интерфейса (шаг П5а) | codex-direct/P5/TASK-A.md:1 |
| codex-direct/P5/TASK-AT.md — Задание P5AT — приёмочные тесты адаптивных меню (шаг П5а) | codex-direct/P5/TASK-AT.md:1 |
| codex-direct/P5/TASK-B.md — Задание P5B — меню настроек (шаг П5б) | codex-direct/P5/TASK-B.md:1 |
| codex-direct/P5/TASK-BT.md — Задание P5BT — приёмочные тесты меню настроек (шаг П5б) | codex-direct/P5/TASK-BT.md:1 |
| codex-direct/P5/TASK-C.md — Задание P5C — код боевого HUD (шаг П5в) | codex-direct/P5/TASK-C.md:1 |
| codex-direct/P5/TASK-CT.md — Задание P5CT — приёмочные тесты боевого HUD (шаг П5в) | codex-direct/P5/TASK-CT.md:1 |
| codex-direct/P5/TASK-G.md — Задание P5G — код ядра режима отладки интерфейса (шаг П5г, часть 1) | codex-direct/P5/TASK-G.md:1 |
| codex-direct/P5/TASK-G2.md — Задание P5G2 — сцены меню, кампании, ментатов и титров в режиме отладки интерфейса (шаг П5г, часть 2) | codex-direct/P5/TASK-G2.md:1 |
| codex-direct/P5/TASK-G2T.md — Задание P5G2T — приёмочные тесты сцен меню, кампании, ментатов и титров (шаг П5г, часть 2) | codex-direct/P5/TASK-G2T.md:1 |
| codex-direct/P5/TASK-GT.md — Задание P5GT — приёмочные тесты ядра режима отладки интерфейса (шаг П5г, часть 1) | codex-direct/P5/TASK-GT.md:1 |
| codex-direct/P5/TASK-T.md — Задание P5T — перенос инструментов Python режима отладки интерфейса (шаг П5г, часть 4) | codex-direct/P5/TASK-T.md:1 |
| codex-direct/P5/TASK-TT.md — Задание P5TT — приёмочные тесты инструментов Python режима отладки интерфейса (шаг П5г, часть 4) | codex-direct/P5/TASK-TT.md:1 |
| codex-direct/P5/answer-10.md — Ответ на Q-P5A-10 | codex-direct/P5/answer-10.md:1 |
| codex-direct/P5/answer-C-04.md — Приёмка P5C | codex-direct/P5/answer-C-04.md:1 |
| codex-direct/P5/answer-CT-01.md — Приёмка P5CT | codex-direct/P5/answer-CT-01.md:1 |
| codex-direct/P5/plan-a/executor-recon.md — PLAN-P5A | codex-direct/P5/plan-a/executor-recon.md:1 |
| codex-direct/P5/plan-a/gui-text.md | строки-заголовка нет; не сверено |
| codex-direct/P5/plan-a/screens-b.md — Главное меню | codex-direct/P5/plan-a/screens-b.md:3 |
| codex-direct/P5/recon-b/persistence.tsv | строки-заголовка нет; не сверено |
| codex-direct/P5/recon-b/port-options.tsv | строки-заголовка нет; не сверено |
| codex-direct/P5/recon-c/RECON.md — RECON-P5CR — разведка боевого HUD | codex-direct/P5/recon-c/RECON.md:1 |
| codex-direct/P5/recon-c/SPOTCHECK.md — Выборочная сверка RECON-P5CR (15 фактов и 2 числа) | codex-direct/P5/recon-c/SPOTCHECK.md:1 |

## 7. Шаги переноса, которые приносят интерфейс

`docs/upstream/PORT_PLAN.md` (рабочая копия): строки таблиц, где шаг — П7…П15 (включая П8а и «П13–П15, релиз»). Текст обрезан до 200 символов.

| Что | Где |
|---|---|
| \| П7 \| Б7 \| localization \| П5 \| — \| перевод кампании Сардаукаров \| | docs/upstream/PORT_PLAN.md:62 |
| \| П8 \| Б8 \| save-slots \| П7 \| П9, П10 \| совместимость старых сохранений (В5); `preferences.ini` апстрима и настройки форка \| | docs/upstream/PORT_PLAN.md:63 |
| \| П8а \| Б8а \| placement-rule, refinery-dock, factory-pads, radar-dish \| П8 \| П11 \| — \| | docs/upstream/PORT_PLAN.md:64 |
| \| П9 \| Б9 \| music-pools \| П7 \| П8, П10 \| папки музыки апстрима и музыкальные пулы форка \| | docs/upstream/PORT_PLAN.md:65 |
| \| П10 \| Б10 \| command-bar, controls-tab, interaction-refresh, starport-orders \| П7 \| П8, П9 \| предел юнитов апстрима, если спорит с панелью приказов \| | docs/upstream/PORT_PLAN.md:66 |
| \| П11 \| Б11 \| credits-art, ментаты и сцены (`hd4-assets`) \| П7 \| П8а \| вступительный ролик апстрима \| | docs/upstream/PORT_PLAN.md:67 |
| \| П12 \| Б12 \| release-packaging, author-gallery \| П8, П8а, П9, П10, П11 \| — \| workflow `claude-review`: установить приложение или удалить \| | docs/upstream/PORT_PLAN.md:68 |
| \| П13 \| Б13 \| эталонные снимки старой и новой сборки \| П12 \| — \| разбор отличий \| | docs/upstream/PORT_PLAN.md:69 |
| \| П14 \| Б14 \| process-docs; догоняющий merge, связывание истории, перемотка `main` \| П13 \| — \| приёмка новой сборки в игре до перемотки \| | docs/upstream/PORT_PLAN.md:70 |
| \| П15 \| Б15 \| документ и скрипт регулярного обновления с апстрима \| П14 \| — \| — \| | docs/upstream/PORT_PLAN.md:71 |
| \| П7 \| Перевод новой кампании Сардаукаров \| | docs/upstream/PORT_PLAN.md:128 |
| \| П8 \| Совместимость старых сохранений; `preferences.ini` апстрима и настройки форка \| | docs/upstream/PORT_PLAN.md:129 |
| \| П9 \| Папки музыки апстрима и музыкальные пулы форка \| | docs/upstream/PORT_PLAN.md:130 |
| \| П10 \| Предел юнитов — если спорит с панелью приказов \| | docs/upstream/PORT_PLAN.md:131 |
| \| П11 \| Вступительный ролик апстрима \| | docs/upstream/PORT_PLAN.md:132 |
| \| П12 \| Workflow `claude-review`: установить приложение Claude Code GitHub App и ключ или удалить workflow из форка (карточка 27) \| | docs/upstream/PORT_PLAN.md:133 |
| \| П14 \| Приёмка новой сборки в игре перед перемоткой `main` \| | docs/upstream/PORT_PLAN.md:134 |
| \| П7 \| p7r \| разведка сдана (`codex-direct/P7/recon/`, поправка `ERRATA.md`); строки порта в `src/gamestates/*` — после П5 \| | docs/upstream/PORT_PLAN.md:169 |
| \| П8 \| — \| разведка сдана (`codex-direct/P8/recon/`, выборочная сверка `SPOTCHECK.md` — 19 из 19); совместимость старых сохранений решена Р5 для hd.7, на шаге — вопрос о hd.10 \| | docs/upstream/PORT_PLAN.md:170 |
| \| П9 \| — \| разведка сдана (`codex-direct/P9/recon/`, сверка `SPOTCHECK.md` — 13 из 15, поправка `ERRATA.md`) \| | docs/upstream/PORT_PLAN.md:171 |
| \| П10 \| — \| разведка сдана (`codex-direct/P10/recon/`, сверка `SPOTCHECK.md` — 13 из 15, поправка `ERRATA.md`) \| | docs/upstream/PORT_PLAN.md:172 |
| \| П8а \| — \| первая часть разведки сдана (`codex-direct/P8A/recon-1/`, сверка `SPOTCHECK.md` — 13 из 15, поправка `ERRATA.md`); площадки заводов — второй частью после П8 \| | docs/upstream/PORT_PLAN.md:173 |
| \| П11 \| — \| разведка сдана (`codex-direct/P11/recon/`, сверка `SPOTCHECK.md` — 13 из 15, поправка `ERRATA.md`) \| | docs/upstream/PORT_PLAN.md:174 |
| \| П12 \| — \| разведка упаковки релиза, workflows и галереи сдана (`codex-direct/P12/recon/`, сверка `SPOTCHECK.md` — 15 из 15); workflows порта совпадают с `UP1`, каталога `packaging` в порту нет \| | docs/upstream/PORT_PLAN.md:175 |
| \| П13–П15, релиз \| — \| не начаты \| | docs/upstream/PORT_PLAN.md:176 |

## 8. Открытые issues об интерфейсе (PavelSlaven/DUNE)

`gh issue list --repo PavelSlaven/DUNE --state open --limit 100`: открытых 3. Фильтр по заголовку и меткам: интерфейс, UI (целое слово), HUD, меню, кнопк, панел, шрифт, экран, layout, sidebar (без учёта регистра).

| Что | Где |
|---|---|
| Совпадений нет (проверено открытых: #5 Апстрим перешёл на SDL3 и убрал cGame: функции форка переносятся по одной, #2 Коллизия индекса 167 в HD4-паке с апстримом, #1 Текущий план работ) | gh issue list, PavelSlaven/DUNE |

