# Карта фактов: интерфейс экрана боя (DUNE)

Рабочая копия W = `C:/Users/Slaven/Projects/DUNE/.claude/worktrees/ui-redesign-360d77`. Все пути ниже относительны W. Формат `путь:строка`; значения и формулы даны как в коде. Если сказано «вычислено вручную», значение посчитано по формуле без запуска игры. Рисование юнитов, зданий, местности, снарядов и меток на поле боя не описано; упоминаются только элементы, которые относятся к панели (курсор, подсказка, предпросмотр размещения).

---

## 1. Порядок рисования экрана боя

Цепочка вызовов за кадр (рисование):

1. `src/game/cGame_logic.cpp:546` `cGame::drawState()` → `src/game/cGame_logic.cpp:563` `m_currentState->draw()`.
2. `src/gamestates/cGamePlaying.cpp:300` `cGamePlaying::draw()`:
   - `:302` `m_drawManager->drawCombatState()` (см. ниже, слои 1-9);
   - `:303` `drawTrackingOverlays()` (подсветка поля боя, `:270-298`; относится к полю);
   - `:305` `drawTextFps()` при `shouldDrawFps()` (`:304`);
   - `:308` `drawCombatMouse()` (`:458-475`): рамка выделения, линия перетаскивания карты, `m_mouse->draw()` (`:469`), отладочный текст `MouseCell` в `(0, TopBarHeight+1)` (`:473`) при debug;
   - `:311` `drawTextTime()` при `shouldDrawTime()` (`:310`);
   - `:314` `m_drawManager->drawCombatMouse()` (`src/managers/cDrawManager.cpp:283-291`): `drawMouse()` → `cMouseDrawer::draw()` → `m_mouse->draw()` (`src/drawers/cMouseDrawer.cpp:50`); затем `cMouseDrawer::drawToolTip()`, если `m_drawToolTip && isMouseOnBattleField()` (`cDrawManager.cpp:288-289`).
3. `src/game/cGame_logic.cpp:564` `m_notificationArea->draw(m_textDrawer, 14, screenH - 64)`.
4. `src/game/cGame_logic.cpp:565` `m_guiConsole->draw()`.

Внутри `cDrawManager::drawCombatState()` (`src/managers/cDrawManager.cpp:119-175`), по порядку:

| # | Строка | Что | Клип |
|---|---|---|---|
| a | `:122` | карта: terrain, структуры, юниты, снаряды, туман, shroud, rally (`:123-153`) | `(0, 42, windowW, screenH)` |
| b | `:155` | сброс клипа | - |
| c | `:158` → `:253-259` `drawSidebar()`: `cSideBarDrawer::draw()` (фон панели, герб, радар, полосы, вкладки, карточки, кнопка космопорта), затем `cMiniMapDrawer::draw()` | `x >= screenW - SidebarWidth` |
| d | `:160-162` `drawStructurePlacing()` (предпросмотр размещения, `cPlaceItDrawer`, поле) | `(0, 42, windowW, windowH+42)` |
| e | `:164` `drawTopBarBackground()` (`:298-342`) | - |
| f | `:165` `drawCredits()` → `CreditsDrawer::draw()` | - |
| g | `:168` `drawMessage()` → `cMessageDrawer::draw()` | - |
| h | `:172-174` `drawDebugInfoUsages()` при `isDrawUsages()` (отладка, текст с y=74, шаг 14: `:208-213`) | - |

Следствия порядка, вычисленные из кода: топбар (e) рисуется после боковой панели (c) и закрывает её верхние 42 px; кредиты (f) и строка сообщений (g) рисуются поверх топбара; миникарта (в c, после сайдбара) перекрывает герб-заглушку и рамку радара (см. раздел 3).

---

## 2. Верхняя панель

Геометрия: высота `TopBarHeight = 42` (`src/sidebar/cSideBar.h:105`, `src/sidebar/HudLayout.hpp:14`). Прямоугольник `layout.topBar = (0, 0, W, 42)` (`HudLayout.hpp:57`).

Элементы, которые рисуются в полосе 0..41 (`src/managers/cDrawManager.cpp:298-342`):

- Фон: `renderRectFillColor(0, 0, W, 42)` цвет `(17, 21, 23)` (`:300, :303-309`).
- Нижняя линия: `renderLine(0, 40, W, 40)` цвет `(151, 113, 43)` (`:301, :310-316`; `40 = TopBarHeight - 2`).
- Кнопка «OPTIONS»: прямоугольник `(7, 4, 126, 33)` (`:318`); заливка `(27, 31, 33)` (`:324`); рамка `(151, 113, 43)` 1 px (`:326-332`); текст `"OPTIONS"` через `m_textDrawer->drawTextCenteredInBox(...)`, цвет `(232, 222, 188)` (`:333`). Клик: `m_mouse->isLeftButtonClicked() && isOverRectangle(...)` → `m_stateTransitions->setNextState(GAME_OPTIONS)` (`:334-341`). Обработка клика находится в функции отрисовки, а не во входном обработчике.
- Кредиты: блок находится в колонке боковой панели, а не в центре топбара (см. ниже).
- FPS (`src/gamestates/cGamePlaying.cpp:477-480`): `drawText(180, 8, Color::Black, "FPS/REST: {fps}/{waitingTime}", no shadow)`; только при `shouldDrawFps()` (`:304`).
- Время (`cGamePlaying.cpp:482-488`): `drawText(screenW - SidebarWidth - 75, 43, White, currentTime)` и `drawText(..., 58, White, currentTimer)`; только при `shouldDrawTime()` (`:310`).

Кредиты (`src/drawers/CreditsDrawer.cpp:215-295`, `draw()`):

- Прямоугольник `layout.credits = (sidebarX + 8, 4, sidebarW - 16, 34)` (`src/sidebar/HudLayout.hpp:70-75`).
- Заливка `(15, 19, 21)` (`CreditsDrawer.cpp:222`, рисование `:227`); рамка `(155, 116, 43)` (`:223`, `:234`).
- Монетка: заливка `(205, 133, 35)` в `(x+7, y+10, 12, 14)` (`:246`, `:241-246`); рамка `(255, 215, 103)` (`:253`, `:248-253`).
- Надпись `"CREDITS"` в `(x+26, y+10)`, цвет `(208, 196, 157)` (`:224`, `:255-261`), шрифт `m_gameTextDrawer` (ARRAKEEN).
- Сумма: `std::max(0, m_currentCredits)`, правый край `endX - textWidth - 9`, `y+10`, цвет `(255, 210, 82)` (`:225`, `:265-272`), шрифт ARRAKEEN.
- Показывается `m_currentCredits` (ролл), а не `m_player->getCredits()`. Обновление в `CreditsDrawer::thinkFast()` (`:111-160`): если цифры догнали цель или `m_initial`, то `m_currentCredits = CreditsMath::nextDisplayedCredits(prev, player credits)` (`:125`); правила `src/drawers/CreditsMath.hpp:47-51`: разница > 200 → шаг `diff/8`; > 20 → `diff/4`; иначе сразу цель.
- Звук: `SOUND_CREDITUP` / `SOUND_CREDITDOWN` (`CreditsDrawer.cpp:129, 132`); не более 7 за цикл (`:198`).
- Анимация поразрядной прокрутки (`thinkAboutIndividualCreditOffsets`, `:162-210`; `m_offset_credit[i] += 1.0F * m_rollSpeed` на `:207`, порог `> 18.0F` на `:195`) вычисляется, но `draw()` значения `m_offset_*` не читает.
- Поля `m_drawX`, `m_drawY` (`CreditsDrawer.cpp:80-81`, `CreditsDrawer.h:89`) заполняются от `CREDITS_BAR` и нигде не читаются.

Шрифты верхней панели:

- OPTIONS, кредиты, строка сообщений, уведомления: `getGameTextDrawer()` = ARRAKEEN (`src/context/TextContext.cpp:46`; `cDrawManager.cpp:63`; `CreditsDrawer.cpp` ctor; `cMessageDrawer.cpp:39`; `cGame_logic.cpp:800`).
- FPS и время: `m_textDrawer` cGamePlaying = `getBeneTextDrawer()` = BENEGESS (`src/gamestates/cGamePlaying.cpp:115`).
- Все шрифты открываются TTF размером 12 (`src/context/ContextCreator.cpp:78, 86, 94`). Имена файлов шрифтов в этих файлах не заданы (берутся из `settingsValidator->getFullName`); enum `ARRAKEEN/BENEGESS/SMALL` в `src/utils/cFileValidator.h:23-25`.

Картинки в топбаре: не найдено. Все элементы топбара нарисованы примитивами (`renderRectFillColor`, `renderRectColor`, `renderLine`, текст).

Курсор над полосой: `src/controls/cGameControlsContext.cpp:87-92` `y < TopBarHeight` → `MOUSE_CELL_HOVER_TOPBAR`, без клетки поля.

---

## 3. Боковая панель

Ширина (`src/sidebar/HudLayout.hpp:46-47`): `sidebarWidth = W < 960 ? 280 : 360`; колонок карточек `columns = W < 960 ? 2 : 3`. Левый край `sidebarX = W - sidebarWidth` (`:50`). Прямоугольник `layout.sidebar = (sidebarX, 0, sidebarWidth, H)` (`:64-69`).

Статические значения до `configureLayout`: `SidebarWidth = 224`, `SidebarWidthWithoutCandyBar = 200` (`src/sidebar/cSideBar.h:102-104`). `configureLayout` (`src/sidebar/cSideBar.cpp:462-467`) ставит `SidebarWidth = HudLayout.sidebarWidth` и `SidebarWidthWithoutCandyBar = SidebarWidth - 8`. Вызов: `src/game/cGame_logic.cpp:783`, до создания `cDrawManager` (`:876`).

### 3.1 Фон и разделители (`src/drawers/cSideBarDrawer.cpp:109-140`, `drawHdSidebar`)

- Фон `(12, 15, 17)` на весь `layout.sidebar` (`:115-121`).
- Полоса `(32, 36, 38)` шириной 5 px, от `y = 42` до `H` (`:122-128`).
- Линия `(166, 124, 44)` по `x = sidebarX + 5`, от `y = 42` до `H` (`:129-135`).

### 3.2 Шапка с гербом (`cSideBarDrawer.cpp:202-236`)

- Прямоугольник `houseHeader = (radarPanel.x + 5, radarPanel.y + 4, radarPanel.w - 10, 28)` (`HudLayout.hpp:82-87`).
- Заливка `(25, 29, 30)` (`cSideBarDrawer.cpp:207`).
- Акцентная полоса 2 px в `y = endY - 2` цветом `m_player->getSelectFadingColor()` (`:210-215`).
- Герб: размер 24 (`:218`), позиция `(x + 3, y + 2)` (`:222-226`), `renderStrechFullSprite` (`:220`).
- Имя дома: `drawText(x + 24 + 10, y + 7, (235, 225, 191), getHouseDisplayName(), no shadow)` (`:230-236`), малый шрифт SMALL (`m_smallTextDrawer`, `:50`).
- Текст по домам (`cSideBarDrawer.cpp:159-174`): `"HOUSE ATREIDES"`, `"HOUSE HARKONNEN"`, `"HOUSE ORDOS"`, `"SARDAUKAR"`, иначе `"UNKNOWN HOUSE"`.

Картинки гербов (`getHouseCrest`, `cSideBarDrawer.cpp:142-157`):

- ATREIDES → `m_houseCrests[0]` (`hud_house_atreides.png`);
- HARKONNEN → `m_houseCrests[1]` (`hud_house_harkonnen.png`);
- ORDOS → `m_houseCrests[2]` (`hud_house_ordos.png`);
- SARDAUKAR → `m_gfxinter->getTexture(BMP_SELECT_HOUSE_SARDAUKAR)` (`src/data/gfxinter.h:168`, индекс 144), не HD-файл;
- иначе `nullptr` (герб не рисуется).

Как грузятся PNG (`cSideBarDrawer.cpp:56-70`, конструктор): `loadHdUiTexture(renderer, "hud_house_*.png", ...)`. Путь `std::filesystem::path("data") / "hd4" / fileName` (`src/utils/HdUiTextureLoader.cpp:13`), относительно рабочей папки (`bin/`). Если файла нет или он не загрузился, пишется `Logger::warn` и возвращается `nullptr` (`HdUiTextureLoader.cpp:29`). Масштаб текстуры `kHd4AssetDensity` (`:21`). Освобождаются в деструкторе (`cSideBarDrawer.cpp:73-79`). Размер герба в шапке фиксирован 24 px и не зависит от `HudLayout`.

### 3.3 Радарная панель (`cSideBarDrawer.cpp:176-271`, `drawHdRadarPanel`)

- Прямоугольник `radarPanel = (sidebarX + 8, 42, panelW, 208)` (`HudLayout.hpp:76-81`), `panelW = sidebarWidth - 16`.
- Заливка `(16, 20, 22)` (`cSideBarDrawer.cpp:182, 188-194`), рамка `(151, 113, 43)` (`:184, 195-201`).
- Viewport миникарты: `radarViewport = (radarPanel.x + 5, radarPanel.y + 34, radarPanel.w - 10, 138)` (`HudLayout.hpp:88-93`). Заливка `(7, 10, 11)` (`cSideBarDrawer.cpp:183, 238-244`), рамка `(62, 68, 67)` (`:250-251`).
- Герб-заглушка, если `!m_player->hasRadarAndEnoughPower() && crest != nullptr` (`:253-270`): размер `min(96, viewport.h - 18)` (`:254-257`), по центру viewport (`:258-268`), альфа 210 (`:268`).

Важно: миникарта рисуется после панели (`cDrawManager.cpp:256-257`) и её заливка чёрным на весь viewport (`cMiniMapDrawer.cpp:120`) закрывает и герб, и рамку, если статус миникарты не `NOTAVAILABLE`. Вычислено из порядка вызовов; отдельно не проверялось на экране.

### 3.4 Мини-карта (`src/drawers/cMiniMapDrawer.cpp`, `cMiniMapDrawer.h:48-54`)

Статусы `eMinimapStatus`: `NOTAVAILABLE`, `POWERUP`, `RENDERMAP`, `POWERDOWN`, `LOWPOWER` (`cMiniMapDrawer.h:48-54`).

Переходы (`think()`, `cMiniMapDrawer.cpp:144-201`; вызывается из `cGamePlaying::thinkNormal()` через `cDrawManager::think()`, `cGamePlaying.cpp:236`, то есть примерно раз в 100 мс по `CLAUDE.md`):

- Нет радара: `!hasAtleastOneStructure(RADAR)` → `NOTAVAILABLE` (`:146-156`). Если радар есть и статус был `NOTAVAILABLE`, он переходит в `POWERDOWN` (`:146-152`).
- Есть радар и энергия (`hasRadarAndEnoughPower = getAmountOfStructuresForType(RADAR) > 0 && bEnoughPower()`, `:160`): из `POWERUP`/`RENDERMAP` при нехватке энергии → `POWERDOWN` с голосом `SOUND_VOICE_04_ATR` (`:163-170`); из `POWERDOWN`/`LOWPOWER` при достатке → `POWERUP` с `SOUND_RADAR` и `SOUND_VOICE_03_ATR` (`:173-181`).
- Счётчик `m_iStaticFrame`: в `POWERDOWN` растёт до `STAT21`, затем `LOWPOWER` (`:185-191`); в `POWERUP` падает до `STAT01`, затем `RENDERMAP` (`:193-199`).

`draw()` (`cMiniMapDrawer.cpp:110-134`):

- `NOTAVAILABLE` → выход, ничего не рисуется (`:116-118`); виден только фон и герб-заглушка (раздел 3.3).
- `POWERUP`, `RENDERMAP`, `POWERDOWN` → `drawTerrain()` + `drawUnitsAndStructures(false)` (`:122-125`).
- `LOWPOWER` → `cleanDrawTerrain()` (чистит текстуру в чёрный, `:479-483`) + `drawUnitsAndStructures(true)`: только свои структуры и юниты (`:127-130`).
- Заливка `Color::Black` на `m_RectFullMinimap` (= radarViewport) в начале (`:120`); текстура `m_mipMapTex` растягивается в `m_RectMinimap` (`:131`); `drawViewPortRectangle()` (`:133`, `:263-298`) рисует белый `(255, 255, 255)` прямоугольник камеры (`:297`).

Состояния по запросу:

- **Обычное**: `RENDERMAP` (карта + все игроки).
- **Нет радара**: `NOTAVAILABLE` (пустой viewport, герб-заглушка).
- **Нет энергии**: `POWERDOWN` (карта ещё рисуется, счётчик до `STAT21`), затем `LOWPOWER` (чёрный фон, только свои объекты). Текста нет.
- **Помехи (статика)**: не найдено. `STAT01..STAT21` (`src/data/gfxinter.h:142-162`, индексы 118..138) используются только как счётчик `m_iStaticFrame` (`cMiniMapDrawer.cpp:59, 98, 139, 186-195`). Ни один вызов рисования не читает их.

Геометрия миникарты (`cMiniMapDrawer.cpp:67-87`, конструктор):

- `minimapArea = radarViewport`.
- `m_factorZoom = min(vpW / mapWidthPx, vpH / mapHeightPx)` (`:69-71`).
- `m_drawX = vpX + (vpW/2 - zoom * mapW/2)`, `m_drawY = vpY + (vpH/2 - zoom * mapH/2)` (`:74-82`).
- `m_RectMinimap = (m_drawX, m_drawY, zoom * mapW, zoom * mapH)` (`:87`).
- Размеры карты — из `m_mapGeometry->getWidth()/getHeight()` (`:402-408`).

Цвета (`getRGBColorForTerrainType`, `cMiniMapDrawer.cpp:373-400`):

- `TERRAIN_ROCK (80, 80, 60)`, `TERRAIN_SPICE (186, 93, 32)`, `TERRAIN_SPICEHILL (180, 90, 25)`, `TERRAIN_HILL (188, 115, 50)`, `TERRAIN_MOUNTAIN (48, 48, 36)`, `TERRAIN_SAND (194, 125, 60)`, `TERRAIN_WALL (192, 192, 192)`, `TERRAIN_SLAB (80, 80, 80)`, `TERRAIN_BLOOM (214, 145, 100)`, `-1` и default → `(255, 0, 255)`.
- Клетка видна по `m_map->isVisible(cell, playerId)` (`:247-248`), иначе чёрная; граница карты (`isWithinBoundaries`) чёрная (`:253-255`).
- Объекты (`drawUnitsAndStructures`, `:305-371`): цвет владельца `getMinimapColor()` (`:329, 340, 351`); червь — `getSelectFadingColor()` (`:360`); при `playerOnly` чужие пропускаются (`:326-327, 337-338, 348-349, 356-357`); скрытое туманом пропускается (`:335, 346, 359`); чёрные пиксели не рисуются (`:364-366`).

Мышь на миникарте:

- `m_isMouseOver = m_RectMinimap.isPointWithin(x, y)` (`cMiniMapDrawer.cpp:412`) — наведение только на карту, а клик проверяется по `m_RectFullMinimap` (`:429, 455, 469`).
- Курсор (`:416-426`): `MOUSE_MOVE`, если выбраны юниты, иначе `MOUSE_NORMAL`; только при `m_isMouseOver && status != NOTAVAILABLE`.
- Левый клик (`:428-451`): при выбранных юнитах → `units->move_to(cell)`, частица `D2TM_PARTICLE_MOVE` (`:440`), звук пехоты `SOUND_MOVINGOUT + rnd(2)`, техники `SOUND_ACKNOWLEDGED + rnd(3)` (`:443-448`).
- Левое нажатие (`:453-465`): без выбранных юнитов → `centerAndJumpViewPortToCell(cell)`.
- Правое нажатие (`:467-477`): всегда `centerAndJumpViewPortToCell(cell)`.

### 3.5 Полоса энергии и пряности (`cSideBarDrawer.cpp:343-368` и `273-341`)

Размещение (`HudLayout.hpp:95-110`):

- `meterY = radarPanel.y + 176` (`:96`); `meterWidth = (radarPanel.w - 10 - 5) / 2` (`:97-98`); `powerMeter = (radarPanel.x + 5, meterY, meterWidth, 27)` (`:99-104`); `spiceMeter = (powerMeter.endX + 5, meterY, meterWidth, 27)` (`:105-110`).

Энергия (`cSideBarDrawer.cpp:349-358`):

- `produced = max(0, getPowerProduced())`, `used = max(0, getPowerUsage())`.
- Подпись: `width < 140 ? "PWR" : "POWER"` (`:353`).
- Текст: `"{used}/{produced}"` (`drawHdMeter`, `:314`).
- Заполнение: `ratio = clamp(used / max(1, produced), 0, 1)` (`:281-286`); ширина полосы `int(barWidth * ratio)` (`:334-340`).
- Цвет заливки `(72, 202, 103)` (`:356`). При `!bEnoughPower()` → `getErrorFadingColor()` (`:289-291`, `:357`), это `Color::Red` (`cPlayer.cpp:755-758`).
- `bEnoughPower()` (`cPlayer.cpp:360-373`): не скирмиш и не человек → `hasAtleastOneStructure(WINDTRAP) || hasAtleastOneStructure(CONSTYARD)`; иначе `powerProduce_ >= powerUsage_`.
- `powerUsage_`, `powerProduce_`: `cPlayer::update()` (`cPlayer.cpp:898-903`) из `m_structureUtils->getTotalPowerUsageForPlayer / getTotalPowerOutForPlayer`.

Спайс (`cSideBarDrawer.cpp:359-367`):

- `value = max(0, getCredits())`, `maximum = max(1, (int)getMaxCredits())` (`:363-364`).
- Подпись: `width < 140 ? "SPC" : "SPICE"` (`:362`).
- Текст `"{credits}/{maxCredits}"`.
- Заливка `(218, 139, 47)` (`:365`). Предупреждение `!bEnoughSpiceCapacityToStoreCredits()` (`:366`) → `getErrorFadingColor()` (Red). Правило (`cPlayer.cpp:350-357`): `(maxCredits_ - 0) > credits`; значит предупреждение при `credits >= maxCredits_`.
- `maxCredits_` по умолчанию 1000 (`cPlayer.cpp:246`; `cPlayer.h:649`), обновляется из `getTotalSpiceCapacityForPlayer` (`cPlayer.cpp:903`).

Общая отрисовка `drawHdMeter` (`cSideBarDrawer.cpp:273-341`):

- Заливка `(10, 13, 15)` (`:293-299`), рамка `(104, 82, 43)` 1 px (`:287, 300-306`).
- Подпись: `drawText(x+4, y+2, (225, 218, 190), label, no shadow)` (`:307-313`), SMALL.
- Сумма: правый край `endX - textWidth - 4`, `y + 2` (`:314-322`).
- Фон полосы `(31, 35, 36)` в `(x+4, endY-7, w-8, 4)` (`:324-333`).

### 3.6 Прочее в панели

Тактических подсказок и иконок вне вкладок и карточек в боковой панели не найдено.

---

## 4. Вкладки списков построек

Количество: 6 видимых вкладок. `enum eListType`: `LIST_NONE` (0), `LIST_CONSTYARD` (1), `LIST_FOOT_UNITS` (2), `LIST_UNITS` (3), `LIST_STARPORT` (4), `LIST_PALACE` (5), `LIST_UPGRADES` (6) (`src/include/enums/ListEnums.h:4-10`). `cSideBar::LIST_MAX = 7` (`src/sidebar/cSideBar.h:100`). Рисуются id 1..6 (`src/drawers/cSideBarDrawer.cpp:394-401`).

Геометрия:

- `layout.tabs = (sidebarX + 8, 42 + 220 = 262, panelW, 34)` (`HudLayout.hpp:111-116`).
- Заливка фона вкладок `(13, 16, 18)` (`cSideBarDrawer.cpp:386-392`).
- Кнопка каждого списка (`src/sidebar/cBuildingListFactory.cpp:24-113`): ширина `tabs.w / 6` (`:55`), высота `tabs.h` (`:56`), `y = tabs.y` (`:24-30, 49`), `x = tabs.x + index * width`. Индекс: CONSTYARD 0, FOOT_UNITS 1, UNITS 2, STARPORT 3, PALACE 4, UPGRADES 5 (`:60-113`).
- Вычислено вручную для 1920×1080: вкладки на `(1568, 262, 344, 34)`, ширина каждой 57 px, `x = 1568, 1625, 1682, 1739, 1796, 1853`.
- `HudLayout::tabRect()` (`HudLayout.hpp:177-184`) в рисовании и хит-тесте не используется: единственные ссылки — сам `HudLayout.hpp` и `tests/utils/test_HudLayout.cpp:191-202`. Последняя вкладка у `tabRect` растягивается до конца, у кнопки списка — нет.

Иконки (индексы gfxinter, `src/data/gfxinter.h`):

- CONSTYARD → `LIST_BTN_CONSTYARD` = 72 (`:96`);
- FOOT_UNITS → `LIST_BTN_INFANTRY` = 74 (`:98`);
- UNITS → `LIST_BTN_FACTORY` = 73 (`:97`);
- STARPORT → `LIST_BTN_STARPORT` = 76 (`:100`);
- PALACE → `LIST_BTN_PALACE` = 75 (`:99`);
- UPGRADES → `LIST_BTN_UPGRADE` = 77 (`:101`).
- Нажатая и ненажатая иконка одна и та же (`cBuildingListFactory.cpp:63-113`).

Состояния (`cBuildingListDrawer::drawButton`, `src/drawers/cBuildingListDrawer.cpp:144-222`):

- Панель `(18, 22, 25)` (`:164, 167`).
- Иконка масштабируется с сохранением пропорций в `(w - 8, h - 6)` и центрируется (`:170-183`). Альфа 255 если доступна, 96 если нет (`:184-188`).
- Недоступна (`!list->isAvailable()`): поверх иконки заливка `(20, 22, 23)` с непрозрачностью 138 (`:189-195`).
- Рамка 1 px: `(93, 78, 49)` обычная, `(217, 164, 54)` нажатая (`:165-166, 196-202`).
- Нажатая: полоса 2 px в `(x+2, y+h-3, w-4, 2)` цветом `(217, 164, 54)` (`:203-210`); `list->stopFlashing()` (`:211`).
- Мигание: внутренняя рамка 1 px в `list->getFlashingColor()` (`:213-221`).
- Цвет мигания `cBuildingList::getFlashingColor() = m_screenFader->getColorFadeSelected(255, 209, 64)` (`src/sidebar/cBuildingList.cpp:470-473`).
- Таймер мигания: `startFlashing()` ставит 2500 (`cBuildingList.cpp:509-512`). Декремент в `cBuildingList::think()` (`:477-479`), вызывается из `cSideBar::thinkProgressAnimation()` только для доступных списков (`src/sidebar/cSideBar.cpp:169-179`), а тот — из `cPlayer::thinkFast()` (`src/gameobjects/players/cPlayer.cpp:961-965`).
- Запуск мигания: новый элемент в списке (`cBuildingList.cpp:193`); список стал доступным (`cSideBar.cpp:414-417`); элемент готов к размещению (`:404-407`); спец-оружие готово к выбору цели (`:409-412`).
- Доступность: `cBuildingList::isAvailable() = m_maxItems > 0` (`cBuildingList.h:110-112`).
- Наведение (вкладка доступна и не выбрана): две рамки `selectFadingColor` (`cSideBarDrawer.cpp:422-431` → `cBuildingListDrawer.cpp:128-142`).
- Выбранная вкладка: `drawButton(list, selectedListId == listId)` (`cSideBarDrawer.cpp:397-399`).

Клики по вкладкам (`src/sidebar/cSideBar.cpp:199-229`):

- Проверка по `list->isOverButton()` (`cBuildingList.cpp:272-282`), то есть `cRectangle::isWithin` с включительной правой и нижней границей.
- Недоступные списки не кликаются (`cSideBar.cpp:207-208`).
- Клик: `setSelectedListId`, звук `SOUND_BUTTON` (`:213-214`).
- Если выбранный список опустел (`!isAvailable`), выбор сбрасывается в `LIST_NONE` (`:226-229`).
- Выбор по умолчанию: `findFirstActiveListAndSelectIt()` (`cSideBar.cpp:433-444`) при событии `GAME_EVENT_ABOUT_TO_BEGIN` (`:395-397`) и при уходе выбранного списка в недоступное (`:419-425`).

---

## 5. Карточка постройки и каталог

### 5.1 Геометрия каталога (`src/sidebar/HudLayout.hpp`)

- `cardGap = 6` (`:48`).
- `catalogY = 302` (`:53`); `catalogBottom = H - (reserveStarportOrderArea ? 54 : 6)` (`:54-55`).
- `catalog = (sidebarX + 8, 302, panelW, max(0, catalogBottom - 302))` (`:117-122`).
- `scrollbar = (catalog.endX - 10, catalog.y, 10, catalog.h)` (`:123-128`).
- `cards = (catalog.x, catalog.y, catalog.w - 15, catalog.h)` (`:129-134`).
- `cardWidth = (cards.w - (columns - 1) * cardGap) / columns` (`:136-138`).
- `imageHeight = max(1, (cardWidth - 4) * 3 / 4)` (`:139-140`); `cardHeight = imageHeight + 32` (`:141`).
- `cardRect(i, scrollRow) = (cards.x + col * (cardW + gap), cards.y + (i / cols - scrollRow) * (cardH + gap), cardW, cardH)` (`:163-175`).
- `visibleRows() = max(1, (cards.h + gap) / (cardH + gap))` (`:145-151`); `totalRows(n) = ceil(n / cols)` (`:153-156`); `maxScrollRow(n) = max(0, totalRows - visibleRows)` (`:158-161`).
- Вычислено вручную, 1920×1080, не starport: catalog `(1568, 302, 344, 772)`; cards `(1568, 302, 329, 772)`; `cardWidth = (329 - 12) / 3 = 105`; `imageHeight = 75`; `cardHeight = 107`; scrollbar `(1902, 302, 10, 772)`.
- Вычислено вручную, 800×600, не starport: catalog `(528, 302, 264, 292)`; cards `(528, 302, 249, 292)`; `cardWidth = 121`; `imageHeight = 87`; `cardHeight = 119`; `visibleRows = 2`.
- Вычислено вручную, 1920×1080, starport: `catalogBottom = 1026`, catalog `h = 724`.

Клип и отрисовка (`cBuildingListDrawer.cpp:238-592`, `drawList`):

- `setClippingFor(cards)` (`:257-262`), сброс `resetClippingFor()` (`:590`).
- Карточки, полностью вне `cards` по Y, пропускаются (`:270-274`); частично видимые рисуются и обрезаются клипом.
- Выбор функции: `drawList(list, listId == CONSTYARD)` (`cBuildingListDrawer.cpp:108-121`). Только для CONSTYARD показывается размер постройки (`drawStructureSize`).

### 5.2 Оформление карточки (`drawHdCard`, `cBuildingListDrawer.cpp:689-826`)

- Высота подписи `labelHeight = 32` (`:693`); `imageHeight = cardH - 32` (`:694`).
- Цвета: панель `(18, 22, 25)` (`:695, 701`); рамка `(142, 111, 51)` (`:696`); внутренняя рамка `(56, 61, 62)` (`:697`); подпись `(232, 225, 196)` (`:698`); цена `(255, 205, 73)` (`:699`).
- Картинка: `renderStrechSprite(icon, (0,0,icon.w,icon.h), (x+3, y+3, w-6, imageH-5))` (`:702-707`). Иконка — `item->getIconId()`.
- Панель подписи: заливка `(x+1, y+imageH, w-2, 31)` цветом панели (`:708-714`).
- Внешняя рамка 1 px (`:715`); внутренняя рамка 1 px с отступом 1 (`:716-722`).
- Разделительная линия `(x+2, y+imageH) → (x+w-3, y+imageH)`, цвет рамки (`:723-729`).

Имя (`:731-801`):

- Источник: `item->getNameString()` (`src/sidebar/cBuildingListItem.cpp:448-468`): для постройки `name` структуры, юнит `name`, апгрейд/спец `description`.
- Сокращения (`compactCardName`, `cBuildingListDrawer.cpp:76-84`): `"Spice Refinery"` → `"Refinery"`, `"Light Infantry"` → `"Infantry"`; `"Hi-Tech"`, `"MCV"`, `"Troopers"` без изменений; остальные как есть.
- Если ширина строки ≤ `w - 6` (`textWidth = cardW - 6`, `:732-733`): одна строка, центрирована в `(x+3, y+imageH, w-6, 32)`, цвет `(232, 225, 196)`, SMALL (`:733-742`).
- Иначе перенос по словам (`:744-766`): первая строка набирается, пока `secondLine` пуст и кандидат помещается; все последующие слова уходят во вторую строку без повторной проверки первой. Обе строки обрезаются `fitWithEllipsis` с `"…"` (`:768-773`).
- Строки рисуются `drawTextCentered(..., x+3, width w-6, y)`: первая `y = y+imageH+2` (`:785`), вторая `y + fontHeight` (`:797`).

Цена (`:803-825`): если `buildCost > 0`: текст `"${cost}"`, цвет `(255, 205, 73)`, SMALL, в `(x+6, y+4)` (`:804-806, 824`). Плашка `(x+3, y+3, textW+4, 17)` заливка `(8, 10, 12)` с непрозрачностью 220 (`:807-816`), рамка `(126, 94, 35)` (`:817-823`).

Размер постройки (`drawStructureSize`, `:617-640`, только для CONSTYARD): плашка `(x + w - 22, y + 3, 19, 19)` заливка `(8, 10, 12)` непрозрачность 220 (`:635-637`). Спрайт фона `GRID_0X0` (`src/data/gfxinter.h:47`), затем клетка: `GRID_1X1` (по умолчанию, `:621`), `GRID_2X2` (`:623-625`), `GRID_3X2` (`:627-629`), `GRID_3X3` (`:631-633`). Размер берётся из `bmp_width / 32` и `bmp_height / 32`.

### 5.3 Состояния карточки

Строительство (`item->isBuilding()` = BUILDING или PAUSED; `cBuildingListItem.h:95-97`) (`cBuildingListDrawer.cpp:287-356`):

- Пока `!isDoneBuilding() || frame < 31` (`:289`): полоса прогресса `(x+2, y+h-36, w-4, 4)` (`:295-305`). Фон `(15, 18, 20)` непрозрачность 230 (`:296-305`). Заполнение `clamp((w-4) * frame / 31, 0, w-4)` цветом `selectFadingColor` (`:290-294, 306-312`).
- Кадр прогресса: `calculateBuildProgressFrameBasedOnBuildProgress() = min(31, healthBar(31, progress, totalBuildTime))` (`cBuildingListItem.cpp:268-279`); `healthBar(max_w, i, w) = (i / w) * max_w` (`src/utils/common.cpp:97-108`).
- Шаг кадра: `resetProgressFrameTimer()` ставит `buildTimeInTicks / 31` (`cBuildingListItem.cpp:291-302`), где `buildTimeInTicks = timerCap * buildTime` (`:304-312`). `timerCap` — `DefaultTimerCap = 35`, `DebugTimerCap = 2` при чите (`cBuildingListItem.h:54-55`; `.cpp:72`). Таймер уменьшается в `cBuildingList::think()` (`cBuildingList.cpp:489-499`), которое вызывается из `cPlayer::thinkFast()` (5 мс, `cPlayer.cpp:961-965`).
- Пауза: надпись `"Paused"` цветом `Color::Yellow` (`(255, 207, 41)`, `src/utils/Color.hpp:56`) в `(x+2, y+2, w-4, h-32)` (`:313-322`); только пока полоса видна.
- Готово (`isDoneBuilding() && frame >= 31`, `:324-346`):
  - `shouldPlaceIt()` → `"READY"` (`m_readyLabel`, `:94`), в `(x+2, y+2, w-4, h-32)`, масштаб 1.0 (`:329-334`); цвет `(225, 48, 42)`, если состояние мыши `MOUSESTATE_PLACE`, иначе `Color::White` (`:326-328`);
  - `shouldDeployIt()` → то же для `MOUSESTATE_DEPLOY` (`:336-345`).
- Лимит юнитов при строительстве: `unitLimitReached && isTypeUnit()` → `drawMaxBuilt` (`:348-355`).

Не строится (`:357-460`):

- Лимит построек: `structureLimitReached = list CONSTYARD && structureFactory.isStructureLimitReached()` (`:249-251`); на карточку влияет, если `!cStructureFactory::isModifyingTerrain(buildId)` (`:367-369`).
- Лимит юнитов: `unitLimitReached = (FOOT_UNITS или UNITS) && isUnitLimitReached()` (`:252-255`); влияет на `isTypeUnit()` (`:370-371`).
- Затемнение, если `!isAvailable() || isBuildingSameSubListItem || cannotBuildDueLimit` (`:375`):
  - без лимита: заливка `(0, 0, 0)` непрозрачность 128 в `(x, y, w, h-32)` (`:377-386`);
    - `isPendingUpgrading()`: рамка и диагонали `errorFadingColor` (`Red`) по всей карточке, текст `"Upgrade"` цвета `(255, 0, 0)` по центру карточки (`:387-418`);
    - `isPendingBuilding()`: то же, текст `"OCCUPIED"` `(255, 0, 0)` (`:419-450`).
  - по лимиту: `drawMaxBuilt(x+2, y+2, w-4, h-32)` (`:452-459`).
- `isBuildingSameSubListItem`: в этом подсписке уже строится другой элемент (`:358-365`); даёт только затемнение.
- Starport (`:462-500`): `cannotPayIt = !hasEnoughCreditsFor(cost)` (`:279`); `orderIsAwaitingFrigate = isOrderPlaced() || isFrigateSent()` (`:463-465`). Тогда заливка `(0, 0, 0)` непрозрачность 128 в `h-32`, рамка и диагонали `Red`, текста нет (`:466-499`).

`drawMaxBuilt` (`:596-607`): спрайт `PROGRESSNA` (`src/data/gfxinter.h:139`, индекс 115) непрозрачность 64 в `(x, y)` (`:598`); рамка `Red` (`:599-600`), диагонали (`:601-602`); текст `"Max"` (верхняя половина) и `"built"` (нижняя) цвета `Color::Red` (`:604-606`), SMALL.

Счётчик очереди (`:520-545`):

- `amountToShow = getTimesToBuild()`, `showAmount = isQueuable() && amount > 0` (`:520-521`). Для starport `amountToShow = getTimesOrdered()`, показывается всегда (`:522-526`).
- Плашка `(textX - 3, textY - 1, w - (textX - x) - 1, 16)`, заливка `(8, 10, 12)` непрозрачность 220 (`:534-543`).
- `textX = x + w - 20` (`+6`, если `amount < 10`); `textY = y + h - 51` (`:529-531`). Текст через `m_gameTextDrawer` (ARRAKEEN) (`:544`).

Выделение и наведение:

- Последняя нажатая карточка: рамка 1 и 2 px `selectFadingColor` (`:502-517`), по `list->getLastClickedId() == i`.
- Наведение (`isOverItemCoordinates_Boolean`, `:553-568, 642-651`): x в `[drawX, drawX + cardW]`, y в `[drawY, drawY + cardH)`; рамка `selectFadingColor` 1 и 2 px.
- Иначе, если `item->isFlashing()` (таймер 500 в `cBuildingListItem.cpp:54`, уменьшается только для выбранного списка, `cBuildingList.cpp:485-487`), рамка цветом списка `getFlashingColor()` (`cBuildingListDrawer.cpp:570-586`).

Отладка: `m_renderListIds` (держатся TAB+D) → номер подсписка в `(x+41, y+40)` (`:547-551`, `:988-1000`), только при `isDebugMode()`.

### 5.4 Клики и колесо по карточкам

Левая кнопка (`src/sidebar/cSideBar.cpp:199-273`, не starport):

- `shouldPlaceIt()` → `setContextMouseState(MOUSESTATE_PLACE)` (`:248-249`);
- `shouldDeployIt()` → `MOUSESTATE_DEPLOY` (`:251-252`);
- `isPaused()` → `startBuilding()` (`:254-256`);
- иначе `startBuildingItemIfOk(item)` (`:257-258`).
- Сообщение строки с информацией о карточке: `drawMessageBarWithItemInfo(item)` (`:244`).

`startBuildingItemIfOk(item)` (`cSideBar.cpp:95-138`):

- Структура, лимит построек: `setMessage("Unable to create more.")`, `return false` (`:106-110`); юнит вне starport, лимит юнитов: то же (`:112-115`).
- `isAvailable()`: если `isQueuable()` → `addItemToList`; иначе только если первый в своём типе списка (`:117-131`). `setLastClickedId(slot)` (`:134`).

Левая кнопка (starport, `cSideBar.cpp:261-271`): если `acceptsOrders()` и `hasEnoughCreditsFor(cost)`: `increaseTimesOrdered()`, `addOrder(item)`, `substractCredits(cost)`.

Правая кнопка (не starport, `cSideBar.cpp:286-294`): если `!isPaused() && isBuilding()` → `pauseBuilding()`; иначе `cancelBuildingListItem(item)` (`:308-342`):

- `timesToBuild--`; при нуле: если строится — возврат `getRefundAmount()` (`cBuildingListItem.cpp:151-158`: `progress * creditsPerProgressTime` при `progress >= 1`, иначе 0); `onBuildItemCancelled`; `cancelBuilding()` (AVAILABLE, сброс прогресса); событие `GAME_EVENT_LIST_ITEM_CANCELLED` (`:326-335`); `itemBuilder->removeItemFromList(item)` (`:338-339`).

Правая кнопка (starport, `cSideBar.cpp:295-305`): если `!isOrderPlaced()` и `timesOrdered > 0` → `decreaseTimesOrdered()`, `removeOrder(item)`.

Наведение (`cSideBar.cpp:181-197`): при выбранном списке и курсоре над карточкой → `setMessage(item->getInfo())` (`:190-196`); `setKeepMessage(mouseOverSidebar)` (`:183-184`).

Текст `getInfo()` (`cBuildingListItem.cpp:397-431`): `seconds = getTotalBuildTimeInMs() / 1000` (`= timerCap * buildTime * 5 / 1000`), минус прогресс, если строится. Форматы:

- структура: `"${cost} | {name} | {power_give - power_drain} Power | {s} Secs"`;
- юнит с ценой > 0: `"${cost} | {name} | {s} Secs"`; при цене 0: `"{name} | {s} Secs"`;
- апгрейд: `"UPGRADE: ${cost} | {description} | {s} Secs"`;
- спец: `"${cost} | {description} | {s} Secs"`;
- иначе: `"ERROR: UNKNOWN BUILD TYPE"`.

Колесо и полоса прокрутки (`cBuildingListDrawer.cpp:928-972`, `onNotifyMouseEvent`):

- Маршрут: `cGamePlaying.cpp:322` → `cSideBar::onNotifyMouseEvent` (`cSideBar.cpp:344-356`): если курсор не на панели или миникарте, обрабатывается только `MOVED_TO`; иначе событие передаётся в `cBuildingListDrawer::onNotifyMouseEvent` (`cSideBar.cpp:356`). Колесо над `layout.catalog` → `scrollSelectedList(∓1)` (`cBuildingListDrawer.cpp:945-955`). `cGamePlaying.cpp:323-325` не даёт колесу уходить в камеру карты.
- Левая кнопка по полосе прокрутки: выше ползунка → `scrollSelectedList(-visibleRows)`, ниже → `+visibleRows` (`:957-971`).
- Клампинг `scrollRow` в `[0, maxScrollRow]` (`cBuildingListDrawer.cpp:844-874`).

Полоса прокрутки (`drawHdScrollbar`, `cBuildingListDrawer.cpp:890-926`):

- Фон `(10, 13, 15)` непрозрачность 245 (`:894, 897-903`); рамка `(83, 69, 43)` 1 px (`:895, 904-910`).
- Если `maxScrollRow <= 0`, ползунка нет (`:912-914`).
- Ползунок `(181, 135, 44)`, рисуется со смещением 2 px со всех сторон (`:896, 919-925`).
- Формулы `HudLayout::scrollbarThumb` (`HudLayout.hpp:186-209`): `thumbH = max(22, scrollbar.h * visibleRows / totalRows)`; `travel = scrollbar.h - thumbH`; `thumbY = scrollbar.y + travel * clamp(scrollRow, 0, maxScroll) / maxScroll`.

---

## 6. Кнопка заказа космопорта (`src/drawers/cOrderDrawer.cpp`)

Где: рисуется только когда выбранный список — STARPORT (`src/drawers/cSideBarDrawer.cpp:433-436`).

Размер и положение (`cOrderDrawer.cpp:32-50`, конструктор):

- Спрайт `BTN_ORDER` (`src/data/gfxinter.h:43`, индекс 19), масштаб `getDensity()` (`:41`).
- `halfOfSidebar = SidebarWidthWithoutCandyBar / 2` (`:43`).
- `halfOfHeightLeftForButton = 50 / 2` (`:44`, комментарий: высота строки иконок, убранная для starport).
- `m_buttonRect = ((screenW - halfOfSidebar) - halfOfButton, (screenH - 25) - halfOfButtonHeight, w, h)` (`:46-48`).
- Координаты фиксируются в конструкторе.

Состояния:

- Спрайт всегда (`:62`).
- `canOrder = orderProcesser->canPlaceOrder()` (`:64`); `canPlaceOrder() = hasOrderedAnything() && !isOrderPlaced()` (`src/gameobjects/structures/cOrderProcesser.h:56-59`).
- Не `canOrder`: заливка `Color::Black` с непрозрачностью 128 по всей кнопке (`:65-68`).
- Наведение при `canOrder`: рамка 2 px цветом `getHouseFadingColor()` (`:69-71, 74-83`).
- Цвет дома (`cPlayer.cpp:731-746`): ATREIDES → Blue, HARKONNEN → Red, ORDOS → Green, SARDAUKAR → Purple, иначе White.
- Текста на кнопке нет (надпись — часть картинки `BTN_ORDER`).

Наведение и клик:

- `onMouseAt`: `m_buttonRect.isPointWithin(coords)` (`cOrderDrawer.cpp:85-88`).
- `onMouseClickedLeft`: при наведении и `canPlaceOrder()` → `placeOrder()` (`:90-99`).
- Вызовы: `src/sidebar/cSideBar.cpp:235-237` (клик по панели, если выбран starport) и `src/gamestates/cGamePlaying.cpp:329` (`onNotify` для всех мышиных событий, включая движение).

---

## 7. Сообщения и уведомления

### 7.1 Строка сообщений (`src/drawers/cMessageDrawer.cpp`)

Положение (боевой режим, `initCombatPosition`, `:143-157`):

- `x = 164` (`widthOfOptionsButton = 160 + 4`, `:149-150, 154`), `y = 1` (`:156`).
- Ширина `W - (SidebarWidth + 164)` (`:151`), высота `30 * density` (`:180`).
- Режим «следующий завоеватель» (`initRegionPosition`, `:128-141`): ширина 480 (`:134`), позиция `(offsetX + 73, offsetY + 358)` (`:139-140`).

Фон (`createMessageBarBmp`, `:173-195`): `MESSAGE_LEFT` (`src/data/gfxinter.h:102`, индекс 78) в 0; `MESSAGE_MIDDLE` (79) повторяется каждые `55 * density` с первого смещения `11 * density` (`:185-190`); `MESSAGE_RIGHT` (80) у правого края со смещением `11 * density` (`:191-194`).

Отрисовка (`draw()`, `:58-69`):

- В боевом режиме полоса рисуется всегда с альфой 255 (`:60-62`).
- Если `m_alpha > -1`: полоса с альфой `m_alpha` (`:64-65`), текст `drawText(x + 13, y + 6, Color{0, 0, 0, alpha}, msg, no shadow)` (`:67`), шрифт ARRAKEEN.

Таймеры (`thinkFast`, `:71-101`; вызов `cDrawManager::thinkFast` ← `cGame::thinkFast`, `cGame_logic.cpp:1385`; по `CLAUDE.md` `thinkFast()` каждые ~5 мс):

- Появление: `m_TIMER_message++`, альфа `+= 3`, потолок 255 (`:73-86`).
- Если `m_TIMER_message > m_timeMessageIsVisible` и `!m_keepMessage` → затухание (`:76-79`). `m_timeMessageIsVisible = 450` в бою (`:147`), `650` в режиме региона (`:132`).
- Затухание: альфа `-= 6`, минимум −1 (`:91-94`); при `alpha < 1` текст очищается (`:97-99`).
- `setMessage` сбрасывает таймер и переводит в `FADE_IN` (`:165-171`); `keepMessage` ставится `cSideBar::onMouseAt` при курсоре над панелью (`cSideBar.cpp:183-184`) и держит текст.

Источники сообщений (`setMessage`): `cSideBar.cpp:92` (информация о карточке), `:108`, `:113` (`"Unable to create more."`); `src/building/cItemBuilder.cpp:206` (то же); `src/controls/mousestates/cMousePlaceState.cpp:88` (то же); `cMouseNormalState.cpp:97` (`"{n} units selected"`), `:101, :124` (статус юнита), `:143` (статус структуры); `src/gameobjects/structures/cOrderProcesser.cpp:160, 165, 172` (`"Frigate is arriving..."` и `msg`).

Цвета: текст чёрный на светлой полосе; других цветов нет.

### 7.2 Область уведомлений (`src/game/cNotificationArea.cpp`, `src/gameobjects/players/cPlayerNotification.cpp`)

- Вызов: `cGame_logic.cpp:564` `draw(m_textDrawer, 14, screenH - 64)`. `m_textDrawer` = `getGameTextDrawer()` (ARRAKEEN, `cGame_logic.cpp:800`).
- Строки: первая (самая новая) — внизу, на `y = H - 64`; каждая следующая выше на 20 px (`cNotificationArea.cpp:66-68`). Порядок: сортировка по таймеру по убыванию (`:35-41`), самое новое имеет наибольший таймер, то есть index 0.
- Подложка (`:64-65`): `renderRectFillColor((x-5, y-5-height+20, 505, 5+height), {0,0,0,128}, opacity 64)`, где `height = 20 * count`. Цвет из `Color` берётся только для RGB, альфа 128 игнорируется (перегрузка `SDLDrawer.cpp:123-127`).
- Время жизни: `m_TIMER = (1000/5) * 7 = 1400` (`cPlayerNotification.cpp:40`), декремент в `thinkFast()` (`cNotificationArea.cpp:43-57`), вызов `cGame_logic.cpp:1380`; видимость `m_TIMER > 0` (`src/gameobjects/players/cPlayerNotification.h:31-33`), невидимые удаляются в `cNotificationArea::thinkFast` (`cNotificationArea.cpp:49-56`).
- Цвета (`cPlayerNotification.cpp:54-72`): `NEUTRAL` → `Color::White`; `PRIORITY` → `Color::Yellow` (`(255, 207, 41)`); `BAD` → `Color::Red`; `OTHER` → `Color::Green`.
- Источники: `cGame_logic.cpp:1409` (событие с сообщением и типом); `:1518` `"Screenshot saved."` (NEUTRAL); `:1535` `"Music toggle successfully"` (NEUTRAL); `:1540` `"Music volume down"`; `:1545` `"Music volume up"`; `:1551` `"Game speed up"`; `:1557` `"Game speed down"` (все NEUTRAL); `:1574` `message` (OTHER). Клавиши: `SCREENSHOT` (`:1529`), `TOGGLE_MUSIC` (`:1533`), `MUSIC_VOLUME_DOWN` (`:1538`), `MUSIC_VOLUME_UP` (`:1543`), `GAME_SPEED_UP` (`:1548`), `GAME_SPEED_DOWN` (`:1554`), `TOGGLE_CHEAT` (`:1570`).
- Очистка при начале миссии: `cGame_logic.cpp:391`.

---

## 8. Подсказки при наведении

Подсказка по структуре (`src/drawers/cMouseDrawer.cpp`), единственная найденная:

- Показывается, только пока держат клавишу `T` (`src/managers/cDrawManager.cpp:397-399` HOLD ставит `m_drawToolTip = true`; `:414-416` PRESSED снимает). Вызов: `cDrawManager.cpp:287-289`, условие `m_drawToolTip && isMouseOnBattleField()`.
- Есть структура под курсором: `isMouseOverStructure()` (`cMouseDrawer.cpp:81`). Ширина 250 (`:82`), иначе 0 (нет подсказки).
- Высота: 78 для WINDTRAP, REFINERY, SILO, TURRET, RTURRET; иначе 50 (`:95-115`).
- Позиция: `x = mouseX + 32`, `y = mouseY + 32` (`:55, 67`), с сдвигом назад, если выходит за экран (`:57-61, 69-73`). Координаты мыши из `MOUSE_MOVED_TO` (`:282-286`).
- Фон (`:159-193`): цвет владельца структуры `getMinimapColor()`, каждый канал −64 (не ниже 0), альфа 128 (`:169-185`); тень чёрная, альфа 128, 4 px справа и снизу (`:186-192`).
- Текст: `cTextWriter(smallTextDrawer, 12)` (`:45`, `src/gui/cTextWriter.cpp:53-54`, шаг строки 12 px); старт `moveTo(x+2, y+2)` (`:137`).
- Строки (`:208-224`): имя (с `" (PRIMARY)"` если основная), цвет `(255, 255, 0)`; `"Hitpoints : {hp}/{maxHP}"`; `"Armor : {armor}"`; `"Protected : {100 - percentageNotPaved}%%"`. Строка `%%` передаётся в `std::format`, который не превращает её в `%`, поэтому на экране будут два знака `%`.
- Ветка ветряка (`:226-245`): при владельце HUMAN `"Total usage : {use}/{out} (OK|LOW)"` (OK при `use <= out`) и `"Windtrap outage : {powerOut}/{maxPowerOut}"`; иначе `"Unknown"`.
- Ветка силоса и рафинери (`:247-280`): при HUMAN `"Total usage : {spice}/{maxSpice} (OK|NOK)"` (OK при `spice <= maxSpice`, `maxSpice = getMaxCredits()`) и `"Silo capacity : {cap}/1000"` (литерал 1000, `:275`); иначе `"Spice usage : Unknown"`.
- Ветка турели (`:195-206`): при владельце `"Sight : {n}"`, `"Range : {n}"`; иначе `"Unknown"`.

Подсказки по карточкам и кнопкам: только подсветка (раздел 4, 5, 6) и строка сообщений (раздел 7). Отдельных всплывающих подсказок на панели не найдено.

---

## 9. Курсоры (`src/controls/cMouse.cpp`, `src/drawers/cMouseDrawer.cpp`)

Константы картинок (`src/data/gfxdata.h:103-113`, BMP):

- `MOUSE_ATTACK` 79, `MOUSE_DOWN` 80, `MOUSE_FORBIDDEN` 81, `MOUSE_LEFT` 82, `MOUSE_MOVE` 83, `MOUSE_NORMAL` 84, `MOUSE_PICK` 85, `MOUSE_RALLY` 86, `MOUSE_REPAIR` 87, `MOUSE_RIGHT` 88, `MOUSE_UP` 89.

Отрисовка (`cMouse::draw()`, `cMouse.cpp:355-394`):

- Позиция = координаты курсора минус смещение (`cMouse.cpp:357-381`):
  - `MOUSE_DOWN`: `y − 16`;
  - `MOUSE_RIGHT`: `x − 16`;
  - `MOUSE_MOVE`, `MOUSE_RALLY`, `MOUSE_ATTACK`, `MOUSE_REPAIR`, `MOUSE_FORBIDDEN`, `MOUSE_PICK`: `x − 16`, `y − 16`;
  - `MOUSE_NORMAL`, `MOUSE_LEFT`, `MOUSE_UP`: без смещения (пустая ветка `else`).
- Спрайт `gfxdata->getTexture(m_mouseTile)` через `renderSprite` (`:393`). Размер — размер текстуры, в коде не задан.
- По умолчанию `MOUSE_NORMAL` (`cMouse.cpp:64`). Смена `setTile()` (`:427-435`) с логом.

Когда какой курсор (внешние точки установки):

- `MOUSE_MOVE` и `MOUSE_NORMAL`: миникарта (`src/drawers/cMiniMapDrawer.cpp:416-426`); `cGameControlsContext.cpp:229` (`NORMAL`, вне поля боя).
- `MOUSE_LEFT`, `MOUSE_RIGHT`, `MOUSE_UP`, `MOUSE_DOWN`: прокрутка края карты (`src/gameobjects/map/cMapCamera.cpp:295-313, 392-410`).
- `MOUSE_ATTACK`, `MOUSE_PICK`, `MOUSE_MOVE`, `MOUSE_RALLY`, `MOUSE_REPAIR`: состояния мыши (`src/controls/mousestates/`), например `cMouseNormalState.cpp:190-246`, `cMouseUnitsSelectedState.cpp:274-459`, `cMouseDeployState.cpp:109` (`MOUSE_ATTACK`), `cMouseRepairState.cpp:100-105`.
- `cMousePlaceState.cpp:228` → `MOUSE_NORMAL`.
- `cSelectYourNextConquestState.cpp:715, 1023` → `MOUSE_ATTACK` (не бой).

Что ещё рисуется у курсора:

- Рамка выделения: `cGamePlaying.cpp:458-462` `renderRectColor(getBoxSelectRectangle(), getColorFadeSelectedLimited(White, 0.5))`.
- Линия перетаскивания карты: `cGamePlaying.cpp:464-468` `renderLine(start, end, то же цвет)`.
- Подсказка рядом с курсором: раздел 8.
- Предпросмотр размещения постройки (`src/drawers/cPlaceItDrawer.cpp:56-68`): спрайт с альфой 96 (`:220`) и клетки `PlaceNeutral (242, 174, 36, 64)`, `PlaceGood (64, 255, 64, 64)`, `PlaceBad (160, 0, 0, 64)` (`src/utils/Color.hpp:58-60`). Рисуется на поле боя; условия в `:70-185`. Вызов `cDrawManager.cpp:264-274`.

Пульсация выделения (`src/game/cScreenFader.cpp:74-87`): `fadeSelect += 1/256` до `> 0.99`, затем `-= 1/256` до `< 0.3125`. Цвет `getColorFadeSelected(r,g,b) = (r,g,b) * fadeSelect` (`:107-124`). Шаг вызывается из `cGame::thinkFast_fading` (`cGame_logic.cpp:1230-1233`, `:1378`).

---

## 10. Клавиши и мышь интерфейса боя

Мышь на панели (`src/sidebar/cSideBar.cpp:344-372`):

- Полоса и миникарта: курсор в зоне панели или миникарты — `pContext->isMouseOnSidebarOrMinimap()` (`src/controls/cGameControlsContext.h:99-101`).
- `MOUSE_MOVED_TO` → `onMouseAt` (подсказка-сообщение, `:181-197`).
- `MOUSE_LEFT_BUTTON_CLICKED` и `DOUBLE_CLICKED` → `onMouseClickedLeft` (`:199-273`).
- `MOUSE_RIGHT_BUTTON_CLICKED` → `onMouseClickedRight` (`:275-306`).
- Колесо над каталогом → прокрутка (раздел 5.4).

Миникарта (раздел 3.4): левая кнопка (клик и нажатие), правая кнопка (нажатие).

Топбар: клик левой кнопкой по «OPTIONS» (`cDrawManager.cpp:334-341`).

Кнопка космопорта (раздел 6): наведение и левый клик.

Клавиатура (`cDrawManager::onNotifyKeyboardEvent`, `:371-385`, вызывается из `cGamePlaying.cpp:359`):

- `cSideBarDrawer::onNotifyKeyboardEvent` → `cBuildingListDrawer::onNotifyKeyboardEvent` (`cSideBarDrawer.cpp:93-96`, `cBuildingListDrawer.cpp:974-1000`):
  - HOLD `TAB` + `D` → `m_renderListIds = true` (`:988-993`, отладка номеров подсписков);
  - PRESSED `TAB` или `D` → `false` (`:995-1000`).
- `cDrawManager::onKeyDown` (`:387-400`): при debug: TAB+D → `setDrawWithoutShroudTiles(true)` (`:389-391`), `G` → `setDrawGrid(true)` (`:393-395`); всегда `T` → `m_drawToolTip = true` (`:397-399`).
- `cDrawManager::onKeyPressed` (`:402-417`): при debug — отпускание TAB/D и G; `T` → `m_drawToolTip = false` (`:414-416`).
- `cGamePlaying::onKeyDownGamePlaying` (`src/gamestates/cGamePlaying.cpp:498-520`): при debug `TAB` → `onKeyDownDebugMode` (`:508-509`).

Клавиш, которые меняют видимость HUD (показ FPS и времени, `TOGGLE_FPS`, `TOGGLE_TIME_DISPLAY`), в коде есть: `src/controls/eKeyAction.h:48-49`. Какая клавиша за ними закреплена, в этом проходе не проверялось (`settings.ini` и `keys.md` не читались).

---

## 11. Вызовы `uiaudit::` в перечисленных файлах

В перечисленных файлах (`src/sidebar/`, `src/drawers/cSideBarDrawer.*`, `cBuildingListDrawer.*`, `cMiniMapDrawer.*`, `cMessageDrawer.*`, `cOrderDrawer.*`, `cMouseDrawer.*`, `cPlaceItDrawer.*`, `src/managers/cDrawManager.*`, `src/game/cNotificationArea.*`, `src/gamestates/cGamePlaying.*` (и `src/drawers/CreditsDrawer.*`, `tests/utils/test_HudLayout.cpp`)) вызовов `uiaudit::` не найдено (0 совпадений при поиске).

Рядом с HUD, вне списка: `src/drawers/cTextDrawer.cpp`:

- `:51` `uiaudit::isEnabled()`, `:52` `uiaudit::recordText(msg, x, y, w, h)`;
- `:97-98` `std::optional<uiaudit::BoxScope>` + `isEnabled()`;
- `:129-131` `uiaudit::Rect box{...}` и `recordText(..., &box)`;
- `:158-160` то же;
- `:182-183` `BoxScope` + `isEnabled()`.

Вне HUD, для справки: `src/game/cGame_logic.cpp:576-638` (`beginFrame`, `onFramePresented`).

---

## 12. Числовые константы раскладки вне `HudLayout.hpp`

Формат: `путь:строка` — значение — к чему относится. Вычисляемые позиции `HudLayout` не дублируются.

**Топбар и клипы**
- `src/managers/cDrawManager.cpp:122` — клип карты, верх `TopBarHeight` (42) — поле боя.
- `:160` — клип размещения, `(0, 42, windowW, windowH + 42)` — размещение.
- `:255` — клип панели, `x = screenW − SidebarWidth`.
- `:300-316` — топбар заливка `(17, 21, 23)`, линия `y = 40` `(151, 113, 43)`.
- `:318` — OPTIONS `(7, 4, 126, 33)`; `:324` `(27, 31, 33)`; `:333` текст `(232, 222, 188)`.
- `:208-209` — отладочный текст usages `y = 74`, шаг 14.
- `src/gamestates/cGamePlaying.cpp:479` — FPS `(180, 8)`, `Color::Black`.
- `:485`, `:487` — время `x = screenW − SidebarWidth − 75`, `y = 43` и `58`, `Color::White`.
- `:473` — отладка `MouseCell` `y = 43`.
- `:282` — подпись поля `y = TopBarHeight + 10` (поле).
- `:115` — шрифт cGamePlaying = BENE.

**Кредиты (`src/drawers/CreditsDrawer.cpp`)**
- `:80-81` — `m_drawX`, `m_drawY` (не используются).
- `:222-225` — панель `(15, 19, 21)`, рамка `(155, 116, 43)`, подпись `(208, 196, 157)`, сумма `(255, 210, 82)`.
- `:241-246` — монетка `+7, +10`, `12 × 14`, `(205, 133, 35)`.
- `:248-253` — рамка монетки `(255, 215, 103)`.
- `:256` — текст `CREDITS` `x + 26`; `:269` — сумма `endX − textW − 9`; `y + 10`.
- `:139` — `m_TIMER_money > 20`; `:141` — `−= 0.005`; `:153-154` — `< 3.0`, `+= 0.005`.
- `:195` — порог `> 18.0F`; `:198` — `m_soundsMade < 7`; `:199` — дистанция звука `32`.
- `src/drawers/CreditsMath.hpp:49-50` — `200 / 8` и `20 / 4`.

**Панель (`src/drawers/cSideBarDrawer.cpp`)**
- `:49` — `m_sidebarColor` (инициализация; в отрисовке не используется).
- `:115-121` — фон `(12, 15, 17)`.
- `:122-128` — полоса `5 px`, `(32, 36, 38)`.
- `:129-135` — линия `(166, 124, 44)`, `x + 5`.
- `:182-186` — панель `(16, 20, 22)`, внутри `(7, 10, 11)`, бронза `(151, 113, 43)`, текст `(235, 225, 191)`.
- `:207` — шапка `(25, 29, 30)`.
- `:210-215` — акцент `2 px`, `endY − 2`.
- `:218` — герб `24`; `:222-226` — `+3, +2`.
- `:231-232` — имя `+34`, `+7`.
- `:250` — рамка viewport `(62, 68, 67)`.
- `:254-257` — герб в viewport `min(96, h − 18)`.
- `:268` — альфа герба 210.
- `:281-286` — диапазон шкалы `[0, 1]`.
- `:287-288` — рамка шкалы `(104, 82, 43)`, текст `(225, 218, 190)`.
- `:298` — фон шкалы `(10, 13, 15)`.
- `:307-322` — подпись `+4, +2`, сумма `endX − w − 4`.
- `:324-333` — полоса `x + 4`, `endY − 7`, ширина `w − 8`, высота 4; фон `(31, 35, 36)`.
- `:353`, `:362` — порог ширины 140 (`PWR`/`SPC`).
- `:356` — зелёный `(72, 202, 103)`; `:365` — оранжевый `(218, 139, 47)`.
- `:386-391` — фон вкладок `(13, 16, 18)`.
- `:403-416` — каталог `(12, 15, 17)`, рамка `(93, 75, 40)`.

**Карточки (`src/drawers/cBuildingListDrawer.cpp`)**
- `:138-141` — подсветка наведения 2 px.
- `:164-166` — панель `(18, 22, 25)`, рамка `(93, 78, 49)`, активный `(217, 164, 54)`.
- `:170-171` — иконка кнопки `w − 8`, `h − 6`.
- `:187` — альфа 255 / 96.
- `:193` — затемнение `(20, 22, 23)`, непрозрачность 138.
- `:203-210` — нижняя полоса нажатой кнопки: `x + 2`, `y + h − 3`, `w − 4`, 2 px.
- `:289` — кадров прогресса 31; `:295` — `y + h − 36`.
- `:297-305` — полоса: `x + 2`, `w − 4`, 4 px, фон `(15, 18, 20)`, непрозрачность 230.
- `:313-321` — `"Paused"` `Color::Yellow`, `(x+2, y+2, w−4, h−32)`.
- `:326-346` — `"READY"`, красный `(225, 48, 42)`.
- `:376-386` — затемнение `(0, 0, 0)`, непрозрачность 128, высота `h − 32`.
- `:411, :416, :442, :448` — «Upgrade», «OCCUPIED» `(255, 0, 0)`.
- `:453-458` — `drawMaxBuilt(x+2, y+2, w−4, h−32)`.
- `:520-531` — счётчик: `y + h − 51`; `x + w − 20` (+6 при `< 10`).
- `:535-543` — плашка счётчика `(-3, -1, ..., 16)`, `(8, 10, 12)`, непрозрачность 220.
- `:548-549` — отладочный номер `(x+41, y+40)`.
- `:596-606` — `PROGRESSNA` непрозрачность 64, `halfHeight = h / 2`.
- `:635-637` — плашка размера `(x + w − 22, y + 3, 19, 19)`, `(8, 10, 12)`, непрозрачность 220.
- `:693` — подпись `32`; `:695-699` — цвета карточки.
- `:703-706` — иконка `(x+3, y+3, w−6, imageH−5)`.
- `:708-714` — панель подписи `(x+1, y+imageH, w−2, 31)`.
- `:716-722` — внутренняя рамка, отступ 1.
- `:723-729` — линия `x + 2 … x + w − 3`.
- `:732` — ширина текста `w − 6`; `:785` — `y + imageH + 2`; `:797` — шаг `fontHeight`.
- `:804-823` — цена: текст `(x+6, y+4)` `(255, 205, 73)`; плашка `(x+3, y+3, textW+4, 17)` `(8, 10, 12)` 220, рамка `(126, 94, 35)`.
- `:894-896` — полоса прокрутки: `(10, 13, 15)` 245, рамка `(83, 69, 43)`, ползунок `(181, 135, 44)`.
- `:919-925` — отступ ползунка 2 px.
- `:949-971` — колесо ±1; клик по полосе ±`visibleRows`.

**Вкладки и список (`src/sidebar/`)**
- `src/sidebar/cBuildingListFactory.cpp:55-56` — ширина вкладки `tabs.w / 6`, высота `tabs.h`.
- `src/sidebar/cBuildingList.cpp:470-473` — мигание `(255, 209, 64)`.
- `:511` — таймер мигания списка 2500.
- `src/sidebar/cBuildingListItem.cpp:54` — таймер мигания элемента 500.
- `src/sidebar/cBuildingListItem.h:54-55` — `DefaultTimerCap = 35`, `DebugTimerCap = 2`.
- `src/sidebar/cBuildingListItem.cpp:272` — `healthBar(31, ...)`; `:297` — `ticks / 31`; `:326`, `:336` — `× 5` мс.
- `src/sidebar/cSideBar.cpp:466` — `SidebarWidth − 8`.
- `src/sidebar/cSideBar.h:102-105` — стартовые значения 24, 200, 224, 42 (до `configureLayout`).
- `src/sidebar/cSideBar.h:107-117` — `HeightOfMinimap 208`, `WidthOfMinimap 200`, `PowerBarMarginHeight 32`, `HorizontalCandyBarHeight 12`, `HeightOfListButton 34`: в проекте вне `cSideBar.*` не используются (grep).

**Миникарта (`src/drawers/cMiniMapDrawer.cpp`)**
- `:69-71`, `:74-87` — масштаб и центрирование.
- `:120` — чёрная заливка.
- `:186`, `:194` — границы счётчика `STAT21`, `STAT01`.
- `:266-267` — размеры рамки камеры `/ TILESIZE − 1`.
- `:271` — минимальный масштаб `0.001`.
- `:297` — рамка камеры `(255, 255, 255)`.
- `:378-398` — цвета местности.

**Сообщения и уведомления**
- `src/drawers/cMessageDrawer.cpp:49` — `10` (перезаписывается в `init`).
- `:61`, `:67` — альфа полосы 255; текст `+13, +6`.
- `:82`, `:84`, `:91`, `:97` — `+3`, потолок `254 → 255`, `−6`, порог `< 1`.
- `:132`, `:147` — время 650 (регион), 450 (бой).
- `:134` — ширина региона 480; `:139-140` — `+73, +358`.
- `:149-150` — `160 + 4`; `:154` — `x = 164`; `:156` — `y = 1`.
- `:180` — высота `30 * density`; `:185` — шаг `55 * density`; `:185, :191-192` — смещение `11 * density`.
- `src/game/cNotificationArea.cpp:64-65` — высота `20 × n`; подложка `x − 5`, `y − 5 − h + 20`, ширина `500 + 5`, высота `5 + h`; непрозрачность 64.
- `:68` — шаг строки 20.
- `src/gameobjects/players/cPlayerNotification.cpp:40` — `TIMER = (1000 / 5) × 7 = 1400`.
- `src/game/cGame_logic.cpp:564` — `x = 14`, `y = H − 64`.

**Кнопка космопорта (`src/drawers/cOrderDrawer.cpp`)**
- `:43` — `SidebarWidthWithoutCandyBar / 2`; `:44` — `50 / 2 = 25`; `:46-48` — позиция.
- `:66` — затемнение непрозрачностью 128.
- `:81-82` — рамка 2 px.

**Подсказка (`src/drawers/cMouseDrawer.cpp`)**
- `:45` — шаг строки 12.
- `:55`, `:67` — `+32`.
- `:82` — ширина 250.
- `:95-115` — высоты 78 / 50.
- `:181-183` — `−64` по каналам.
- `:185`, `:187` — альфа 128.
- `:191-192` — тень 4 px.
- `:275` — `1000` (ёмкость силоса, литерал).

**Курсор и состояние (`src/controls/cMouse.cpp`, `src/game/cScreenFader.cpp`, `src/gameobjects/players/cPlayer.cpp`)**
- `cMouse.cpp:355-394` — смещения курсора `16`.
- `cScreenFader.cpp:43` — `m_fadeSelect = 1.0`; `:74` — шаг `1/256`; `:78` — порог `0.99`; `:87` — порог `0.3125`.
- `cPlayer.cpp:246` — `maxCredits_ = 1000`; `:350-357` — правило спайса; `:360-373` — правило энергии; `:731-746` — цвета домов; `:755-758` — `Red`; `:773-775` — пульсация `(255, 255, 255)`; `:898-903` — пересчёт энергии и ёмкости; `:961-965` — `sidebar->think()` каждые 5 мс.
- `src/controls/cGameControlsContext.cpp:89, 95, 101` — границы зон мыши (`TopBarHeight`, миникарта, `SidebarWidth`).
- `src/utils/common.cpp:97-108` — `healthBar`.
- `src/utils/HdUiTextureLoader.cpp:13` — путь `data/hd4`; `:21` — `kHd4AssetDensity`.
- `src/game/cGame_logic.cpp:783` — `configureLayout`; `:800` — шрифт текста; `:876-877` — создание `cDrawManager`; `:1380`, `:1385` — `thinkFast` уведомлений и сообщений.
- `src/building/cItemBuilder.cpp:189` — `increaseProgress(1)` (вне списка, влияет на прогресс карточки).

---

## Неопределённости и что не найдено

- Помехи миникарты (статика): не найдено (раздел 3.4).
- Анимация включения/выключения миникарты в кадре: видна только смена содержимого (`POWERUP`/`POWERDOWN` рисуют местность без статики); визуально не проверялось.
- Перекрытие герба и рамки миникарты (раздел 3.3): вычислено из порядка вызовов, на экране не проверялось.
- `HudLayout::tabRect` в рисовании не используется (раздел 4); значения вкладок в `tabRect` и на экране различаются для последней вкладки.
- Имена файлов шрифтов (ARRAKEEN, BENEGESS, SMALL) и размеры текстур (иконки, курсоры, `hud_house_*.png`, `BTN_ORDER`) в коде не заданы; найдены только индексы и вызовы.
- Наличие `data/hd4/hud_house_*.png` в ресурсах не проверялось (файлы не открывались).
- Клавиши `TOGGLE_FPS` и `TOGGLE_TIME_DISPLAY` и их назначение в `settings.ini` не проверялись.
- Частота вызова `cGame::thinkFast` (~5 мс) взята из `CLAUDE.md` (раздел про цикл игры), в код не проверялась; таймеры в тиках пересчитаны по этой частоте.
- `cGamePlaying::drawTrackingOverlays` и отладочные строки поля (раздел 1, пункт 2) отнесены к полю, детально не разбирались.
- `cBuildingListUpdater.*` (логика состава списков, `onBuildItemStarted`, `onStructureCreated` и др.) и `cItemBuilder` не разбирались по содержанию; в них рисования и цветов не найдено (grep по `Color|render|draw|setMessage|Sound|Notification` в `cBuildingListUpdater.*` — 0 совпадений).
- Тесты `tests/utils/test_HudLayout.cpp` (`:60-220`): покрывают раскладку для 800×600, 1067×600, 1280×720, 1920×1080 и перебор размеров 800..3840 × 600..2160 (4747001 случаев), скроллбар (955624 случая), вкладки (`tabRect`, `:187-203`), зарезервированную зону starport (3122 случая). Тесты не запускались.
- Не проверялось: поведение `renderRectFillColor` в SDL при непрозрачности, отличной от 255, и размеры курсора на экране.
