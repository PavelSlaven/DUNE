# Карта фактов: экраны меню DUNE (рабочая копия ui-redesign-360d77)

Только чтение. Пути относительно `W = C:/Users/Slaven/Projects/DUNE/.claude/worktrees/ui-redesign-360d77`, строки — по текущему файлу. Значения и формулы — как в коде.

## 0. Общее для всех экранов

- Холст: `m_settings->getScreenW()` / `getScreenH()` (W, H ниже). Семантику отличия от `getOutputW/H` не проверял.
- Шрифт всех шести экранов: `m_textDrawer = m_ctx->getTextContext()->getBeneTextDrawer()` (`cMainMenuState.cpp:54`, `cOptionsState.cpp:51`, `cChooseHouseState.cpp:43`, `cSelectYourNextConquestState.cpp:86`, `cSelectMissionState.cpp:47`, `cSetupSkirmishState.cpp:95`). Bene-шрифт: `resources/bin/settings.ini:91` `BENEGESS=benegess.fon`, открывается `TTF_OpenFont(..., 12)` (`src/context/ContextCreator.cpp:86`). В таблицах шрифт = «bene».
- Тема кнопок/окон по умолчанию: `GuiTheme::Remaster()` (`src/gui/GuiTheme.hpp:39-54`): fillColor `{24,29,33,238}`, borderLight `{190,145,58,255}`, borderDark `{71,50,24,255}`, textColor `{236,229,202,255}`, textColorHover `{255,202,83,255}`, textColorShadow `{4,6,7,220}`, disabledTextColor `{132,132,124,255}`. Неактивная: `GuiTheme::RemasterInactive()` (`GuiTheme.hpp:56-70`): fillColor `{20,24,27,220}`, borderLight `{91,84,66,255}`, borderDark `{46,42,34,255}`.
- Кнопка `GuiRenderKind::REMASTER_BUTTON` (`src/gui/GuiButton.cpp:100-125`): тень смещением (+3,+3) цветом textColorShadow; заливка fillColor; внешняя рамка borderDark, внутренняя (inset 1) borderLight; линия у верха (x+4..w-5, y+3) цветом textColorHover при focus, иначе borderLight. Focus: заливка +18 по каждому каналу; pressed: заливка *3/4 и рамки меняются местами. Текст (`GuiButton.cpp:189-`): цвет textColorHover при focus/hover, иначе textColor, disabled — disabledTextColor; для CENTER масштаб текста = min(textScale, (w-16)/textLen, (h-8)/fontH), но не ниже 0.65.
- Окно `GuiWindow` (`src/gui/GuiWindow.cpp:37-51`): `drawRectFillBorder(m_theme)` (строка 43); заголовок, если не пуст: `drawTextCentered(title, x, w, y+2, Color::Yellow)` (строка 50). `drawRectFillBorder` = заливка fillColor + `drawRectBorder(borderLight, borderDark)` (`src/gui/GuiObject.cpp:54-70`).
- Цвета-константы: `Color::Yellow = {255,207,41,255}`, `Color::Red = {255,0,0}`, `Color::White = {255,255,255,255}` (`src/utils/Color.hpp:51-56`).
- Загрузка HD-текстур: `loadHdUiTexture(renderer, name, ctx)` читает `data/hd4/<name>` относительно текущей папки (`src/utils/HdUiTextureLoader.cpp:11-30`), плотность `kHd4AssetDensity = 4` (`src/utils/Graphics.hpp:64`). Текстура создаётся с `Texture(..., kHd4AssetDensity)`.
- Пакеты графики: `resources/bin/settings.ini:81-87` `GFXINTER=sdl_inter_hd4.dat`, `GFXWORLD=sdl_world_hd4.dat`, `GFXMENTAT=sdl_mentat_hd4.dat`, `GFXDATA=sdl_data_hd4.dat`; `ContextCreator.cpp:35-67` открывает их с density 4. Загрузка картинок из пакета: `src/utils/cPack.cpp` (заголовок `D2TM`, uint16 число файлов, запись 52 байта: имя 40, расширение 4, offset uint32, size uint32; данные после `6 + 52*N`).
- Курсор: во всех экранах `m_mouse->draw()` в конце `draw()`.

### 0.1 Размеры исходных картинок (проверено скриптом, см. раздел 9)

| Ресурс | Откуда | Исходный размер (px) | Формат содержимого |
|---|---|---|---|
| `main_menu_background.png` | `resources/bin/data/hd4/` → `data/hd4/` | 5120 × 1440 | PNG |
| `main_menu_logo.png` | `resources/bin/data/hd4/` | 1792 × 320 | PNG |
| `campaign_map.png` | `resources/bin/data/hd4/` | 2432 × 960 | PNG |
| `hud_house_atreides.png` | `resources/bin/data/hd4/` | 384 × 384 | PNG |
| `hud_house_harkonnen.png` | `resources/bin/data/hd4/` | 384 × 384 | PNG |
| `hud_house_ordos.png` | `resources/bin/data/hd4/` | 384 × 384 | PNG |
| gfxinter idx 0 `BMP_D2TM` | `sdl_inter_hd4.dat` | 2432 × 664 | PNG (имя «BMP», содержимое PNG) |
| gfxinter idx 11 `BMP_SELECT_HOUSE_ATREIDES` | `sdl_inter_hd4.dat` | 360 × 392 | PNG |
| gfxinter idx 12 `BMP_SELECT_HOUSE_HARKONNEN` | `sdl_inter_hd4.dat` | 360 × 392 | PNG |
| gfxinter idx 13 `BMP_SELECT_HOUSE_ORDOS` | `sdl_inter_hd4.dat` | 360 × 392 | PNG |
| gfxinter idx 144 `BMP_SELECT_HOUSE_SARDAUKAR` | `sdl_inter_hd4.dat` | 360 × 392 | PNG |
| gfxinter idx 16 `BMP_UNKNOWNMAP` | `sdl_inter_hd4.dat` | 512 × 512 | PNG |
Индексы: `src/data/gfxinter.h:24,35-37,40,168`.

---

## 1. Главное меню — `cMainMenuState` (`src/gamestates/cMainMenuState.cpp`, `.h`)

### 1а. Порядок рисования (`draw()`, `cMainMenuState.cpp:236-267`)
1. `drawHdBackground()` (стр. 238): `renderClearToColor {10,12,14,255}`; если фон есть — `renderStrechFullSprite(main_menu_background, rect(0,0,W,H), 90)` (стр. 201-204, третий аргумент — непрозрачность 90; сигнатура `SDLDrawer.hpp:35`, по умолчанию 255); затем вписывание в экран (стр. 206-229): `backgroundAspect = bg.w/bg.h`, `screenAspect = W/H`; если `screenAspect > 2.2` → drawH = H, drawW = H*bgAspect; иначе если `screenAspect > backgroundAspect` → drawW = W, drawH = W/bgAspect; иначе drawH = H, drawW = H*bgAspect; рисуется по центру `((W-dW)/2, (H-dH)/2)`.
2. Отладочный фон (только debug).
3. Логотип (стр. 244-246): `renderStrechFullSprite(m_hdMenuLogo ? m_hdMenuLogo : bmp_D2TM_Title, m_logoRect)`. Если HD-лого нет — gfxinter idx 0 (2432×664).
4. `gui_window->draw()` (стр. 248): панель-окно с заливкой и рамкой Remaster, затем 8 кнопок.
5. `gui_btn_credits->draw()` (стр. 249).
6. Версия: `drawTextBottomRight(Color{220,213,188,230}, D2TM_VERSION, 18)` (стр. 251-254).
7. Дата сборки: `drawText(18, H - fontHeight - 22, D2TM_BUILD_DATETIME)` (стр. 255-258), цвет по умолчанию.
8. Debug: координаты мыши (стр. 260-262).
9. `m_mouse->draw()` (стр. 265).

### 1б. Элементы

Геометрия (значения клампов в `buildHdMenu`, стр. 102-127):
- `buttonCount = 8` (стр. 102); `buttonWidth = clamp(W/4, 280, 360)` (стр. 103); `buttonHeight = clamp(H/15, 40, 48)` (стр. 104); `buttonGap = clamp(H/90, 6, 10)` (стр. 105); `panelPadding = 16` (стр. 106).
- Окно: `panelWidth = buttonWidth + 32`; `panelHeight = 8*buttonHeight + 7*buttonGap + 32` (стр. 107-109); `panelX = (W - panelWidth)/2` (стр. 110); `panelY = clamp((H - panelHeight)/2 + 28, 132, max(132, H - panelHeight - 46))` (стр. 111-114).
- Кнопки: `x = panelX + 16`, `y0 = panelY + 16`, шаг `buttonHeight + buttonGap` (стр. 135-136, 137-153). Ширина `buttonWidth`, высота `buttonHeight`.
- Лого: `logoWidth = clamp(W*2/5, 310, 430)` (стр. 123); `logoHeight = max(1, logoWidth * srcH / srcW)`, src = HD-лого или gfxinter 0 (стр. 121-124); `logoX = (W - logoWidth)/2`; `logoY = max(24, panelY - logoHeight - 24)` (стр. 125-126).

| Элемент | Вид | Текст | Геометрия | Шрифт | Цвета | путь:строка |
|---|---|---|---|---|---|---|
| Логотип | ручной вывод картинки | — | `m_logoRect` = (logoX, logoY, logoWidth, logoHeight) | — | — | `cMainMenuState.cpp:121-127, 244-246` |
| Окно-панель | `GuiWindow`, тема Remaster, без заголовка | — | (panelX, panelY, panelWidth, panelHeight) | — | fill `{24,29,33,238}`, рамки `{190,145,58}`/`{71,50,24}` | `cMainMenuState.cpp:129-133` |
| Campaign | `GuiButton` REMASTER_BUTTON, enabled | `Campaign` | (x, y0 + 0*step, bw, bh) | bene | Remaster | `cMainMenuState.cpp:155-157` |
| Skirmish | `GuiButton` REMASTER_BUTTON, enabled | `Skirmish` | строка 2 | bene | Remaster | `cMainMenuState.cpp:158-161` |
| Load | `GuiButton`, **disabled** (`nullptr` onClick) | `Load` | строка 3 | bene | тема RemasterInactive (тема выбирается по `enabled`, `cMainMenuState.cpp:146`) | `cMainMenuState.cpp:162` |
| Map Editor | `GuiButton`, enabled | `Map Editor` | строка 4 | bene | Remaster | `cMainMenuState.cpp:163-165` |
| Options | `GuiButton`, enabled | `Options` | строка 5 | bene | Remaster | `cMainMenuState.cpp:166-168` |
| Hall of Fame | `GuiButton`, **disabled** | `Hall of Fame` | строка 6 | bene | RemasterInactive | `cMainMenuState.cpp:169` |
| Introduction | `GuiButton`, enabled только если `std::filesystem::exists("intro.pak")` (путь относительно CWD) | `Introduction` | строка 7 | bene | Remaster если файл есть, иначе RemasterInactive | `cMainMenuState.cpp:171-175` |
| Exit | `GuiButton`, enabled | `Exit` | строка 8 | bene | Remaster | `cMainMenuState.cpp:176-179` |
| CREDITS | `GuiButton` REMASTER_BUTTON (вне окна, отдельный) | `CREDITS` | (W - 132 - 18, 16, 132, 34) | bene | Remaster | `cMainMenuState.cpp:181-191` |
| Версия | текст | `D2TM_VERSION` (макрос из `config.h.in:7`) | drawTextBottomRight, margin 18 | bene | `{220,213,188,230}` | `cMainMenuState.cpp:251-254` |
| Дата сборки | текст | `D2TM_BUILD_DATETIME` | (18, H - fontH - 22) | bene | по умолчанию текста | `cMainMenuState.cpp:255-258` |

Строка i (i от 0) = `y0 + i*(buttonHeight + buttonGap)`; порядок строк 0..7 — как в таблице выше.
Пример расчёта при W=1920, H=1080 (по формулам): buttonWidth=360, buttonHeight=48, buttonGap=10, panelW=392, panelH=486, panelX=764, panelY=325; logoW=430, logoH=430*320/1792=76, logoX=745, logoY=225; CREDITS=(1770,16,132,34).

### 1в. Зоны нажатия вне виджетов
Нет. Мышь обрабатывают только `gui_window->onNotifyMouseEvent` и `gui_btn_credits->onNotifyMouseEvent` (`cMainMenuState.cpp:269-273`).

### 1г. Клавиши (`onNotifyKeyboardEvent`, `cMainMenuState.cpp:280-295`, только `PRESSED`)
- `eKeyAction::MENU_BACK` (`settings.ini:143` `Escape`) → `m_settings->setPlaying(false)` (стр. 283-285). Это завершает игровой цикл, переход не выполняется.
- `eKeyAction::TOGGLE_MUSIC` (`settings.ini:99` `M`) или `SDL_SCANCODE_MUTE` → переключает `setPlayMusic`; при выключении `stopMusic()` (стр. 287-293).

### 1д. Переходы
| Кнопка | Действие | путь:строка |
|---|---|---|
| Campaign | `setNextStateWithFade(GAME_SELECT_HOUSE)` | `cMainMenuState.cpp:155-157` |
| Skirmish | `m_missionFlow->init()`; `setNextStateWithFade(GAME_SETUPSKIRMISH)` | `:158-161` |
| Map Editor | `setNextStateWithFade(GAME_NEW_MAP_EDITOR)` | `:163-165` |
| Options | `setNextState(GAME_OPTIONS)` (без затухания) | `:166-168` |
| Introduction | `m_videoFlow->play("intro.pak")` | `:173-175` |
| Exit | `setPlaying(false)`; `fadeOut()` | `:176-179` |
| CREDITS | `setNextStateWithFade(GAME_CREDITS)` | `:188-190` |
| Escape | `setPlaying(false)` | `:283-285` |

### 1е. Пороги раскладки (клампы)
- `buttonWidth`: нижняя граница 280 действует при `W/4 < 280`, верхняя 360 при `W/4 > 360` (`:103`).
- `buttonHeight`: 40 при `H/15 < 40`, 48 при `H/15 > 48` (`:104`).
- `buttonGap`: 6 при `H/90 < 6`, 10 при `H/90 > 10` (`:105`).
- `panelY`: нижняя 132; верхняя `max(132, H - panelHeight - 46)` (`:111-114`).
- `logoWidth`: 310 при `W*2/5 < 310`, 430 при `> 430` (`:123`); `logoY` минимум 24 (`:126`).
- Других ветвлений по размеру нет (проверены `buildHdMenu`, `draw`, `drawHdBackground`).

### 1ж. Вызовы `uiaudit::`
- В `cMainMenuState.*` вызовов нет.
- Виджеты, которые рисует меню: `GuiWindow.cpp:39-41` `auditRecord("GuiWindow")`; `GuiButton.cpp:49-52` `auditRecord("GuiButton")` и `auditClick("GuiButton:" + text)`; `GuiObject.cpp:37` `uiaudit::recordGui(...)`, `:42` `uiaudit::recordClick(name, ...)`.
- Сценарий аудита: `src/debug/UiAuditScenes.cpp:18` `{"main-menu", "GAME_MENU", "cMainMenuState"}`, сцена `:41`.

---

## 2. Меню настроек — `cOptionsState` (`cOptionsState.cpp`, `.h`) + `OptionsMenuLayout.hpp`

### 2а. Порядок рисования (`draw()`, `cOptionsState.cpp:596-605`)
1. Фон: если `m_backgroundTexture && *m_backgroundTexture` → `renderSprite(*m_backgroundTexture, 0, 0)` (стр. 598-600). Это `services->screenTexture` (снимок экрана), задаётся в конструкторе (стр. 68). После `setPrevState`/`refresh()` фон сбрасывается в `nullptr` (стр. 639). Значит, фон есть только у экземпляра, созданного до первого `refresh`. Очистки цвета нет.
2. `m_guiWindow->draw()` (стр. 601): окно (заливка Remaster), заголовок, все виджеты в порядке добавления.
3. `m_mouse->draw()` (стр. 604).

Картинок нет. Экран полностью виджетный.

### 2б. Элементы

Геометрия окна (`OptionsMenuLayout::create(W, H, bh, playing, fontH)`, `OptionsMenuLayout.hpp:22-143`):
- `bh = buttonHeight = max(32, fontH + 10)` (`cOptionsState.cpp:74`). `fontH = m_textDrawer->getFontHeight()` (значение не измерял).
- `margin = 8`, `actionGap = max(2, 4) = 4`, `contentGap = 2`, `contentX = 24`, `applyWidth = 170`, `advancedWidth = 220` (`:29-34`).
- `windowWidth = min(W - 32, 680)` (`:35`); `oldHeight = min(H - 32, 680)` (`:36`); `actionRows = playing ? 2 : 1` (`:37`); `availableHeight = H - 8` (`:38`).
- `preferredContentTop = bh + 2` (`:39`); `preferredApplyY = (2 + bh) * 10` (`:43`); `preferredHeight = preferredApplyY + bh + 8 + actionRows*bh + (actionRows-1)*actionGap + 8` (`:44-45`).
- `compact = preferredHeight > availableHeight` (`:46`); `minimumContentTop = 2 + fontH + 2` (`:47`).
- `contentTop = compact ? max(28, minimumContentTop) : bh + 2` (`:48-50`); `compactActionGap = compact ? 2 : 4` (`:51`); `applyGap = compact ? 2 : 8` (`:52`); `bottomMargin = compact ? 4 : 8` (`:53`).
- `applyY = compact ? contentTop + 9*(bh+2) : preferredApplyY` (`:54-56`); `requiredHeight = applyY + bh + applyGap + actionRows*bh + (actionRows-1)*compactActionGap + bottomMargin` (`:57-58`).
- `windowHeight = min(H - 8, max(oldHeight, requiredHeight))` (`:59`); окно центрируется `((W-ww)/2, (H-wh)/2, ww, wh)` (`:61-67`).
- Строки контента: `contentRowY(row) = contentTop + (row-1)*(bh+2)` (`cOptionsState.cpp:97-100`).
- Нижний ряд: `columnWidth = (ww - 32)/3` (`OptionsMenuLayout.hpp:95`); `x0 = 8`, `x1 = 16 + colW`, `x2 = 24 + 2*colW`, `lastWidth = ww - 8 - x2` (`:96-99`); `bottomY = wh - bottomMargin - bh` (`:100`). `mainMenu=(x1,bottomY,colW)`, `quit=(x0,bottomY,colW)`, `back=(x2,bottomY,lastWidth)` (`:101-118`). При `playing`: `upperY = bottomY - compactActionGap - bh` (`:121`); `save=(x0,upperY,colW)`, `load=(x1,upperY,colW)`, `missionSelect=(x2,upperY,lastWidth)` (`:122-139`).
- `speedLabel = (16, contentTop + 2*(bh+2), 122, bh)` (`:70-75`); `apply = (24, applyY, 170, bh)` (`:76-81`); `advanced = (24+170+8=202, applyY, 220, bh)` (`:82-87`); `status = (advanced.x+advanced.w+8, applyY, max(0, ww - 8 - statusX), bh)` (`:88-94`).

Координаты внутри окна (из `cOptionsState.cpp:71-111`, `rect()`/`relativeRect()` — относительные к окну): X-константы: contentX 24, audioLabelWidth 110, audioCheckX 138, volumeLabelX 218, volumeLabelWidth 110, audioSliderX 350, audioSliderWidth 250, checkLabelWidth 220, checkX 252, displayLabelWidth 160, arrowWidth 46, selectorX 198, scaleValueWidth 200.

| Элемент | Вид | Текст | Геометрия (x, row, w, h) | Цвета / примечание | путь:строка |
|---|---|---|---|---|---|
| Заголовок окна | заголовок GuiWindow | `"Dune II - The Maker - version " + D2TM_VERSION` | y окна + 2, центр, Yellow | Yellow | `cOptionsState.cpp:118`, `GuiWindow.cpp:50` |
| Main menu | GuiButton, enabled | `Main menu` | menuLayout.mainMenu | Remaster | `:121-132` |
| Quit game | GuiButton, enabled | `Quit game` | menuLayout.quit | Remaster | `:134-147` |
| Back | GuiButton, enabled | `Back` | menuLayout.back | Remaster | `:149-161` |
| Save game | GuiButton, **disabled** (только при playing) | `Save game` | menuLayout.save | RemasterInactive | `:163-174` |
| Load game | GuiButton, **disabled** (только при playing) | `Load game` | menuLayout.load | RemasterInactive | `:176-187` |
| Mission select | GuiButton, enabled (только при playing и не skirmish) | `Mission select` | menuLayout.missionSelect | Remaster | `:189-203` |
| Cheat mode enabled | GuiLabel (только если `isCheatMode()`) | `Cheat mode enabled` | (24, row 9, 220, bh) | Yellow текст, `GuiTextAlignHorizontal::LEFT` | `:205-217` |
| Music | GuiLabel | `Music` | (24, row 1, 110, bh) | Remaster, прозрачный | `:219-228` |
| Music (чекбокс) | GuiCheckBox | — | (138, row 1, bh, bh) | onCheck → `setMusicEnabled(true)`; setChecked(getMusicEnabled) | `:230-243` |
| Volume (музыка) | GuiLabel | `Volume` | (218, row 1, 110, bh) | | `:245-254` |
| Volume (музыка, слайдер) | GuiSlider | — | (350, row 1, 250, bh); min 0, max 10, init `getMusicVolume()` | onValueChanged → `setMusicVolume(v)` | `:256-268` |
| Sound | GuiLabel | `Sound` | (24, row 2, 110, bh) | | `:270-279` |
| Sound (чекбокс) | GuiCheckBox | — | (138, row 2, bh, bh) | `setSoundEnabled` | `:281-294` |
| Volume (звук) | GuiLabel | `Volume` | (218, row 2, 110, bh) | | `:296-305` |
| Volume (звук, слайдер) | GuiSlider | — | (350, row 2, 250, bh); 0..10, init `getSoundVolume()` | `setSoundVolume` | `:307-319` |
| Game speed | GuiLabel | `Game speed` | speedLabel = (16, row 3, 122, bh) | | `:321-330` |
| Game speed (слайдер) | GuiSlider | — | (138, row 3, 220, bh); min 2, max 10, init `2 - getGlobalSpeed() + 10` | onValueChanged: `globalSpeed = 10 - v + 2` → `setGlobalSpeed` | `:332-348` |
| FOW | GuiLabel | `FOW` | (24, row 4, 220, bh), LEFT | | `:350-360` |
| FOW (чекбокс) | GuiCheckBox | — | (252, row 4, bh, bh) | `setFogOfWarEnabled` | `:362-375` |
| Game scale | GuiLabel | `Game scale` | (24, row 5, 160, bh), LEFT | | `:377-387` |
| Game scale `<` | GuiButton | `<` | (198, row 5, 46, bh) | onClick `selectRenderScale(-1)` | `:389-399` |
| Game scale значение | GuiLabel OPAQUE_WITH_BORDER | текст из `scaleChoiceText` | (198+46+8=252, row 5, 200, bh) | | `:401-411` |
| Game scale `>` | GuiButton | `>` | (198+46+8+200+8=460, row 5, 46, bh) | `selectRenderScale(+1)` | `:413-423` |
| Object size | GuiLabel | `Object size` | (24, row 6, 160, bh), LEFT | | `:425-435` |
| Object size `<` | GuiButton | `<` | (198, row 6, 46, bh) | `selectWorldScale(-1)` | `:437-447` |
| Object size значение | GuiLabel OPAQUE_WITH_BORDER | текст из `scaleChoiceText` | (252, row 6, 200, bh) | | `:449-459` |
| Object size `>` | GuiButton | `>` | (460, row 6, 46, bh) | `selectWorldScale(+1)` | `:461-471` |
| Low power icon | GuiLabel | `Low power icon` | (24, row 7, 220, bh), LEFT | | `:473-483` |
| Low power icon (чекбокс) | GuiCheckBox | — | (252, row 7, bh, bh) | `setShowLowPowerIcon` | `:485-498` |
| Apply | GuiButton | `Apply` | menuLayout.apply (enabled, см. ниже) | Remaster | `:500-511` |
| Статус | GuiLabel TRANSPARENT | `""`, затем `Saved. Restart the game.` или `Could not save preferences.ini` | menuLayout.status, LEFT | | `:513-524, 579, 582` |
| More settings | GuiButton, **disabled** | `More settings` | menuLayout.advanced | RemasterInactive | `:526-536` |

Значения и допустимые варианты:
- Music / Sound: чекбокс, вкл/выкл. Громкость: слайдер целых 0..10.
- Game speed: слайдер 2..10; значение в UI = `2 - globalSpeed + 10` (больше = медленнее по подписи, конвертация при `onValueChanged` обратная).
- FOW, Low power icon: чекбоксы.
- Game scale (`renderScaleChoices(outputW, outputH)`, `src/utils/ScaleChoices.cpp:4-14`): список = `[0 (Auto)]` + из `{100,125,150,175,200}` только доступные: `isManualRenderScaleAvailable` (`src/utils/RenderScale.cpp`): `max(outputW,800)*100 >= 800*p` и `max(outputH,600)*100 >= 600*p`. Auto-процент = `lround(min(Wn/800, Hn/600)*100)`. Текст: `Auto (N%)` или `N%` (`ScaleChoices.cpp:43-48` — `scaleChoiceText`).
- Object size (`worldScaleChoices()`, `src/utils/WorldScale.hpp`): `[0 (Auto)]` + `{100,110,125,150}`. Auto по `outputH`: `<=768 → 100`, `<=1080 → 110`, `<=1600 → 125`, иначе `150`.
- Кнопки `<`/`>`: циклический выбор `(index + step + count) % count` (`cOptionsState.cpp:541-555`); при каждом выборе статус очищается.
- Apply активна (`setEnabled`) только если выбранный render-процент или world-процент отличается от сохранённого (`updateScaleControls`, стр. 557-569). `applyScaleSettings` (стр. 571-585) сохраняет в `preferences.ini` через `Preferences::saveScales`; при успехе статус `Saved. Restart the game.`, иначе `Could not save preferences.ini`.

Страницы/вкладки: нет. Один экран с строками 1..9 и нижним рядом.

Кнопки внизу: `Main menu` (GAME_MENU, fade), `Quit game` (`setPlaying(false)` + fadeOut), `Back` (`setNextState(prevState)`, без fade). При playing дополнительно `Save game`/`Load game` (оба disabled) и `Mission select`.

### 2в. Зоны нажатия вне виджетов
Нет. `onNotifyMouseEvent` только `m_guiWindow->onNotifyMouseEvent(event)` (`cOptionsState.cpp:607-610`).

### 2г. Клавиши
Нет. `onNotifyKeyboardEvent` пустой (`cOptionsState.cpp:617-619`). Клавиши MENU_BACK/Escape не обрабатываются.

### 2д. Переходы
| Кнопка | Действие | путь:строка |
|---|---|---|
| Main menu | `setNextStateWithFade(GAME_MENU)` | `cOptionsState.cpp:128-130` |
| Quit game | `setPlaying(false)`; `fadeOut()` | `:142-146` |
| Back | `setNextState(prevState)` (prevState = состояние, из которого открыли) | `:157-159` |
| Mission select (только при playing, не skirmish) | `setNextState(GAME_MISSIONSELECT)` | `:198-200` |
prevState задаётся при создании: `cCreatorState.cpp:158` `cOptionsState(m_services, m_stateTransitions->getCurrentState())`; при переходе из игры `cGame_logic.cpp:1080-1086` вызывает `setPrevState(m_state)`, кроме случая `m_state == GAME_MISSIONSELECT` (тогда только `refresh()`). Переход в options из игры: `cGamePlaying.cpp:542`, из редактора: `cEditorState.cpp:513`, из меню: `cMainMenuState.cpp:166-168`, из кампании: `cSelectYourNextConquestState.cpp:1044`.

### 2е. Пороги раскладки
- `windowWidth = min(W-32, 680)`; `oldHeight = min(H-32, 680)`.
- `compact` при `preferredHeight > H - 8` (`OptionsMenuLayout.hpp:46`). При `bh = 32` (fontH <= 22): порог H < 428 (не playing), H < 464 (playing). Для другого bh порог меняется по той же формуле.
- В `compact`: `contentTop = max(28, 2+fontH+2)`; `applyY = contentTop + 9*(bh+2)`; `compactActionGap = 2`; `applyGap = 2`; `bottomMargin = 4` (`:47-56`).
- `buttonHeight = max(32, fontH+10)` (`cOptionsState.cpp:74`).
- Ширина колонок нижнего ряда: `(ww - 32)/3`.

### 2ж. Вызовы `uiaudit::`
- В `cOptionsState.*` и `OptionsMenuLayout.hpp` вызовов нет.
- Через виджеты: GuiLabel `GuiLabel.cpp:42-44`; GuiCheckBox `GuiCheckBox.cpp:42-45` (`auditClick("GuiCheckBox")`); GuiSlider `GuiSlider.cpp:76-79` (`auditRecord`, `auditClick("GuiSlider")`); GuiButton `GuiButton.cpp:49-52` (`auditClick("GuiButton:" + text)`); GuiWindow `GuiWindow.cpp:39-41`.
- Сценария аудита для options нет (в `UiAuditScenes.cpp` только `main-menu`, см. 1ж).

### 2з. Разница «из боя» / «из главного меню»
- `playing = (m_prevState == GAME_PLAYING)` (`cOptionsState.cpp:79`). Другие состояния-источники (редактор `cEditorState.cpp:513`, кампания `cSelectYourNextConquestState.cpp:1044`, главное меню) дают `playing=false`.
- playing=true: 2 ряда внизу (`layout.save/load/missionSelect` строка upperY), кнопки `Save game`, `Load game` (disabled), `Mission select` (если не skirmish, `:189`). Окно выше на одну строку действий.
- playing=false: только `Main menu`, `Quit game`, `Back` в нижнем ряду; `Apply`, `More settings` в обоих режимах.
- Фон-снимок `screenTexture` виден только при первом построении из игры; после `setPrevState` фон не рисуется (`:639`).

---

## 3. Выбор Дома — `cChooseHouseState` (`cChooseHouseState.cpp`, `.h`)

### 3а. Порядок рисования (`draw()`, `cChooseHouseState.cpp:111-142`)
1. `drawHdBackground()` (стр. 113): `renderClearToColor {10,12,13,255}`; фон `main_menu_background.png` (`hd4`, 5120×1440) вписывается (стр. 151-170): если `srcAspect > screenAspect` → высота H, ширина `H*srcAspect`, по центру по X; иначе ширина W, высота `W/srcAspect`, по центру по Y. Вывод `renderStrechFullSprite` (стр. 171). Затем заливка на весь экран `{3,6,8,142}` (стр. 172-177).
2. Заголовок `"CHOOSE YOUR HOUSE"` (стр. 115-121): центр по X, y=48, цвет `{231,190,91,255}`.
3. Четыре карточки `drawHdHouseCard` (стр. 123-126): ATREIDES, ORDOS, HARKONNEN, SARDAUKAR.
4. Кнопка Back: заливка `{43,49,53,245}` при hover, иначе `{25,31,35,245}`; рамка `renderRectColor {195,142,43,255}`; текст `Back` (стр. 128-139).
5. `m_mouse->draw()` (стр. 141).

Карточка (`drawHdHouseCard`, стр. 180-224):
- тень: прямоугольник `(x+5, y+6, w, h)` цветом `{0,0,0,150}` (стр. 185-190);
- заливка `{21,27,31,244}` (стр. 191); рамка `{173,125,39,255}` (стр. 192); внутренняя рамка `(x+4, y+4, w-8, h-8)` `{102,78,35,255}` (стр. 193-198);
- эмблема: `imageMaxWidth = w - 24`, `imageMaxHeight = h - 72` (стр. 200-201); `imageWidth = imageMaxWidth`, `imageHeight = imageWidth / srcAspect`; если `imageHeight > maxH` → `imageHeight = maxH`, `imageWidth = imageHeight*srcAspect` (стр. 202-209); положение `(x + (w - imgW)/2, y + 12, imgW, imgH)` (стр. 211-215); `renderStrechSprite(emblem, src, dst, 232)` (стр. 216);
- подпись: центр по X, `y = card.y + card.h - fontH - 22`, цвет `{238,229,204,255}` (стр. 218-223).

### 3б. Элементы

Геометрия (ctor, `cChooseHouseState.cpp:66-92`):
- `gap = clamp(W/48, 16, 32)`; `horizontalMargin = clamp(W/24, 28, 72)`; `availableCardWidth = (W - 2*hM - 3*gap)/4`; `cardWidth = clamp(availableCardWidth, 160, 420)` (стр. 66-70).
- `cardsWidth = 4*cardWidth + 3*gap`; `firstX = (W - cardsWidth)/2` (стр. 71-72).
- `cardsY = clamp(H/6, 96, 150)` (стр. 73).
- `backHeight = 46`; `backY = H - 46 - 18` (стр. 74-75); `availableCardHeight = backY - cardsY - 26` (стр. 76).
- `preferredCardHeight = clamp(H*3/5, 320, 520)`; `cardHeight = max(280, min(preferredCardHeight, availableCardHeight))` (стр. 77-80).
- Карточки: `houseAtreides = (firstX, cardsY, cw, ch)`, далее `+ (cw+gap)` для Ordos, Harkonnen, Sardaukar (стр. 82-85).
- Back: `backWidth = 240`, `backButtonRect = ((W-240)/2, backY, 240, 46)` (стр. 87-92).

| Элемент | Вид | Текст | Геометрия | Шрифт | Цвета | путь:строка |
|---|---|---|---|---|---|---|
| Фон | картинка main_menu_background.png | — | см. 3а.1 | — | clear `{10,12,13}`, оверлей `{3,6,8,142}` | `cChooseHouseState.cpp:61-64, 144-177` |
| Заголовок | ручной текст | `CHOOSE YOUR HOUSE` | y=48, центр X | bene | `{231,190,91,255}` | `:115-121` |
| Карточка ATREIDES | ручное рисование + картинка | `ATREIDES` (подпись) | houseAtreides | bene | `{21,27,31,244}`, рамки `{173,125,39}`/`{102,78,35}`, текст `{238,229,204}` | `:82, 123, 180-224` |
| Карточка ORDOS | то же | `ORDOS` | houseOrdos | bene | то же | `:83, 124` |
| Карточка HARKONNEN | то же | `HARKONNEN` | houseHarkonnen | bene | то же | `:84, 125` |
| Карточка SARDAUKAR | то же | `SARDAUKAR` | houseSardaukar | bene | то же | `:85, 126` |
| Картинка домов | `renderStrechSprite` gfxinter `BMP_SELECT_HOUSE_*` | — | см. 3а.2 (360×392) | — | альфа 232 | `:56-59, 216` |
| Back | ручной прямоугольник + текст (не GuiButton) | `Back` | (x=(W-240)/2, y=backY, 240, 46) | bene | fill `{25,31,35,245}` / hover `{43,49,53,245}`; рамка `{195,142,43,255}`; текст `{238,229,204}` / hover `{255,224,139}` | `:88-92, 128-139` |

Примечание: `cChooseHouseState::getType()` возвращает `GAMESTATE_SELECT_YOUR_NEXT_CONQUEST` (`cChooseHouseState.cpp:226-229`), а не отдельный тип этого экрана. Факт, без оценки.

### 3в. Зоны нажатия вне виджетов (`onMouseLeftButtonClicked`, стр. 245-263)
- `houseAtreides`, `houseOrdos`, `houseHarkonnen`, `houseSardaukar` (прямоугольники карточек целиком) → `m_mentatFlow->prepareToTellAboutHouse(ATREIDES | ORDOS | HARKONNEN | SARDAUKAR)`.
- `backButtonRect` → `setNextStateWithFade(GAME_MENU)`.
- Наведение (`MOUSE_MOVED_TO`, стр. 265-268): только `hoversOverBackButton` по `backButtonRect`.

### 3г. Клавиши (`cChooseHouseState.cpp:270-277`, PRESSED)
- `MENU_BACK` (Escape) → `setNextStateWithFade(GAME_MENU)`.

### 3д. Переходы
| Действие | Куда | путь:строка |
|---|---|---|
| Клик по карточке дома | `prepareToTellAboutHouse(house)` → лямбда MentatFlow (`cGame_logic.cpp:224-233`) → `cGame::prepareMentatToTellAboutHouse` (`cGame_logic.cpp:1257-1285`): `cTellHouseState::prepareMentat(house)`, `setNextStateToTransitionTo(GAME_TELLHOUSE)`, `initiateFadingOut()` (стр. 1283-1284) | `cChooseHouseState.cpp:249-258` |
| Back / Escape | `GAME_MENU` с затуханием | `cChooseHouseState.cpp:261, 274` |

### 3е. Пороги раскладки
- `gap`: 16 при `W/48 < 16`, 32 при `W/48 > 32` (`:66`).
- `horizontalMargin`: 28 при `W/24 < 28`, 72 при `W/24 > 72` (`:67`).
- `cardWidth`: 160 при `availableCardWidth < 160`, 420 при `> 420` (`:70`).
- `cardsY`: 96 при `H/6 < 96`, 150 при `H/6 > 150` (`:73`).
- `preferredCardHeight`: 320 при `H*3/5 < 320`, 520 при `> 520` (`:78`); `cardHeight` не меньше 280 (`:79`).
- Ветвлений по размеру в `drawHdBackground` нет (сравнение аспектов — см. 3а.1).

### 3ж. Вызовы `uiaudit::`
- В `cChooseHouseState.*` вызовов нет. Виджетов тут нет, только ручной рендер.

---

## 4. Карта кампании — `cSelectYourNextConquestState` (`cSelectYourNextConquestState.cpp`, `.h`) + `CampaignMapLayout.hpp`

### 4а. Порядок рисования (`draw()`, `cSelectYourNextConquestState.cpp:341-376`)
1. `m_mouse->setTile(MOUSE_NORMAL)` (стр. 343).
2. `drawHdBackground()` (стр. 344, 378-418): clear `{7,9,11,255}`; `main_menu_background.png`; вписывание: `srcAspect > screenAspect` → `width = ceil(H*srcAspect)` по центру X; иначе `height = ceil(W/srcAspect)` по центру Y (стр. 389-408); затем заливка `{3,5,7,178}` на весь экран (стр. 411-417).
3. `drawHdChrome()` (стр. 345, 420-468): панель `panel` заливка `{14,18,21,246}` (стр. 422-425); рамка `panel` `{82,58,27,255}` (стр. 426-429); внутренняя рамка inset 3 `{190,145,58,255}` (стр. 430-436); заголовок-плашка `title`: заливка `{20,25,29,245}`, рамка `{112,82,36,255}` (стр. 438-445); текст `SELECT YOUR NEXT REGION` `drawTextCenteredInBox`, цвет `{239,194,88,255}` (стр. 446-450); герб дома игрока: квадрат `crestSize = max(28, title.h - 12)`, позиция `(title.x + 8, title.y + (title.h - crestSize)/2)` (стр. 452-467).
4. Clip на `map` (стр. 347-352), затем по состоянию (стр. 353-364):
   - INTRODUCTION → `drawStateIntroduction()` (стр. 675-689): в сцене THREE_HOUSES — `drawHdMapBase(alpha)`; в TO_TAKE_CONTROL / THAT_HAS_BECOME_DIVIDED — база + границы с альфой; в SELECT_YOUR_NEXT — база + границы;
   - CONQUER_REGIONS или FADEOUT → `drawStateConquerRegions()` (стр. 691-705): база, границы, все 27 регионов (`regionDraw`), сообщение `Select your next region.`, если `isFinishedConqueringRegions && !hasMessage()` (стр. 702-704);
   - SELECT_NEXT_CONQUEST → `drawStateSelectYourNextConquest()` (стр. 707-727): база, границы, hover-регион альфа 256 и курсор `MOUSE_ATTACK` (стр. 712-716), регионы, сообщение.
5. `resetClippingFor()` (стр. 366); рамка карты `renderRectColor(map, {190,145,58,255})` (стр. 367-370).
6. `drawHdMessage()` (стр. 371, 654-673): заливка `message` `{18,23,27,248}`, рамка `{112,82,36,255}`; текст `drawTextScaledCenteredInBox(msg, message, 1.0F, {232,225,199,255})`.
7. `m_guiBtnToMissionSelect->draw()` (стр. 373).
8. `m_drawManager->drawMouse()` (стр. 375).

Карта: `campaign_map.png` (hd4, 2432×960) растягивается в `map` с `opacity` (стр. 470-485); fallback — `gfxworld` `WORLD_DUNE` (стр. 480-484). Границы регионов: собственная текстура из `WORLD_DUNE_CLICK` (`createHdRegionBordersTexture`, стр. 577-652): цвет `{20,18,17}`, альфа 210 на границе, 0 иначе. Окраска регионов `createHdRegionTintTexture` (стр. 498-575): ATREIDES `{45,92,192}`, HARKONNEN `{194,48,42}`, ORDOS `{52,156,67}`, прочее `{126,118,102}`, RGBA 255 внутри региона, 0 снаружи. Альфа региона при `drawRegion` (стр. 865-881): максимум 132 если `bSelectable`, иначе 104; `alpha = clamp(iAlpha*max/255, 0, max)`.

Портреты-гербы: `hud_house_*.png`, 384×384, по `m_objects->getPlayer(0)->getHouse()` (стр. 134-154): ATREIDES → `hud_house_atreides.png`, HARKONNEN → `hud_house_harkonnen.png`, ORDOS → `hud_house_ordos.png`, SARDAUKAR → без герба.

### 4б. Элементы

Геометрия (`CampaignMapLayout::create(W, H)`, `src/gamestates/CampaignMapLayout.hpp:20-84`):
- `margin = clamp(W/48, 14, 40)`; `titleHeight = clamp(H/14, 44, 64)`; `messageHeight = clamp(H/12, 46, 64)`; `buttonHeight = clamp(H/15, 42, 54)`; `gap = clamp(H/80, 8, 14)`; `panelPadding = clamp(W/100, 14, 24)` (стр. 24-29).
- `availableMapHeight = max(180, H - 2*margin - titleH - msgH - btnH - 4*gap - 2*pad)` (стр. 31-35); `availableMapWidth = max(320, W - 2*margin - 2*pad)` (стр. 36-39).
- `aspect = 608/240` (`SourceMapWidth/SourceMapHeight`, стр. 9-12, 40-41); `mapWidth = max(320, min(availableMapWidth, round(availableMapHeight*aspect)))` (стр. 42-48); `mapHeight = max(126, round(mapWidth/aspect))` (стр. 49-52).
- `panelWidth = mapWidth + 2*pad`; `panelHeight = 2*pad + titleH + mapH + msgH + btnH + 4*gap` (стр. 54-56); `panelX = (W - panelWidth)/2`; `panelY = max(margin, (H - panelHeight)/2)` (стр. 57-58).
- Внутренние блоки: `contentX = panelX + pad`, `contentY = panelY + pad`; `title = (contentX, contentY, mapW, titleH)`; `map = (contentX, title.y + titleH + gap, mapW, mapH)`; `message = (contentX, map.y + mapH + gap, mapW, msgH)`; далее `contentY = message.y + msgH + gap` (стр. 59-74).
- `buttonWidth = clamp(mapW/4, 190, 300)`; `missionButton = (contentX + mapW - buttonWidth, contentY, buttonWidth, btnH)` (стр. 76-82).
- Регионы: `regionDestination(sx,sy,sw,sh)` (стр. 86-104): масштаб `mapW/608`, `mapH/240`; координаты `map.x + (sx-16)*scaleX`, `map.y + (sy-73)*scaleY`.
- Клик: `clickMapX(screenX, cw)` = `clamp(int((screenX - map.x)/map.w * cw), 0, cw-1)`, аналогично Y (стр. 106-126).

| Элемент | Вид | Текст | Геометрия | Шрифт | Цвета | путь:строка |
|---|---|---|---|---|---|---|
| Панель | ручное рисование | — | `panel` | — | fill `{14,18,21,246}`, рамка `{82,58,27}`, внутр. `{190,145,58}` (inset 3) | `cSelectYourNextConquestState.cpp:420-436` |
| Заголовок | ручной текст в плашке | `SELECT YOUR NEXT REGION` | `title` (`contentX`, `contentY`, `mapW`, `titleH`) | bene | плашка `{20,25,29,245}`, рамка `{112,82,36}`, текст `{239,194,88}` | `:438-450` |
| Герб дома | картинка | — | (title.x+8, title.y + (titleH - s)/2, s, s), s = max(28, titleH-12) | — | — | `:452-467` |
| Карта | картинка `campaign_map.png` | — | `map` | — | рамка `{190,145,58}` | `:470-485, 367-370` |
| Границы регионов | текстура (из WORLD_DUNE_CLICK) | — | `map` | — | `{20,18,17}` a=210 | `:487-496, 577-652` |
| Регионы (27 шт.) | текстура-тинт | — | `map` | — | см. 4а | `:498-575, 843-881` |
| Сообщение | ручной текст в плашке | runtime, см. ниже | `message` | bene, масштаб 1.0 | fill `{18,23,27,248}`, рамка `{112,82,36}`, текст `{232,225,199}` | `:654-673` |
| Mission select | GuiButton REMASTER_BUTTON | `Mission select` | `missionButton` | bene | Remaster | `:163-173` |

Тексты сообщений (runtime):
- `3 Houses have come to Dune.` (стр. 226); `To take control of the land.` (231); `That has become divided.` (237); `Select your next region.` (703, 725, флаг `true`); hover: `region {N}`, где N = `c-1` из пиксела клик-карты (895).

Клик-карта: `WORLD_DUNE_CLICK` (`regionClickMapBmp`, стр. 200): индекс региона = значение пиксела − 1 (стр. 893-896).

Регионы: 27 штук. Позиции (source-координаты 608×240, стр. 942-974): `PIECE_DUNE_001`=(16,73), `_002`=(126,73), `_003`=(210,73), `_004`=(306,73), `_005`=(438,73), `_006`=(510,73), `_007`=(16,91), `_008`=(158,149), `_009`=(282,135), `_010`=(362,105), `_011`=(456,117), `_012`=(544,105), `_013`=(16,155), `_014`=(58,165), `_015`=(190,213), `_016`=(312,163), `_017`=(388,163), `_018`=(502,167), `_019`=(576,167), `_020`=(16,237), `_021`=(62,255), `_022`=(134,245), `_023`=(282,257), `_024`=(360,253), `_025`=(406,213), `_026`=(448,269), `_027`=(514,227). Вызов `installWorld()` из `cGame::jumpToSelectYourNextConquestMission` (`cGame_logic.cpp:929`) и из `cGame::setState` при переходе в `GAME_REGION` (`:1122-1126`). Свойства региона (`iHouse`, `bSelectable`, `iAlpha`, конквест) задаёт файл `campaign/<house>/mission<N>.ini` через `cIni::loadRegionfile` (`src/utils/ini.cpp:81-107`; вызов `cSelectYourNextConquestState.cpp:830`).

### 4в. Зоны нажатия вне виджетов
- Карта `map` (прямоугольник): `regionOver(x,y)` (`cSelectYourNextConquestState.cpp:884-897`) — пиксель клик-карты → регион. Только в состоянии SELECT_NEXT_CONQUEST (`onMouseMove` стр. 1013-1025, `onMouseLeftButtonClicked` стр. 1027-1038).
- Клик по выбираемому (`bSelectable`) региону → `loadScenarioAndTransitionToNextState(mission)` (`:1034`).
- Вне карты (`isPointWithin` false) → region = -1 (стр. 888).

### 4г. Клавиши (`cSelectYourNextConquestState.cpp:1040-1047`, PRESSED)
- `MENU_BACK` (Escape) → `setNextState(GAME_OPTIONS)` (без затухания, стр. 1043-1045).

### 4д. Переходы
| Действие | Куда | путь:строка |
|---|---|---|
| Mission select (кнопка) | `setNextState(GAME_MISSIONSELECT)` | `cSelectYourNextConquestState.cpp:172` |
| Клик по выбираемому региону | `m_missionFlow->init()`; `setNextState(GAME_BRIEFING)`; `m_dataCampaign->region = iNewReg`; `mission++`; `prepareForPlayer()`; `loadScenario()`; музыка BRIEFING; `state = REGSTATE_FADEOUT`; `fadeOut()` | `:729-784` (переход: `:770, 783`) |
| Escape | `GAME_OPTIONS` (без затухания) | `:1043-1045` |

Номер региона `iNewReg`: таблица миссий (стр. 743-752): миссия 0→1, 1→2, 2→5, 3→8, 4→11, 5→14, 6→17, 7→20, 8→22; `+` индекс среди `bSelectable` до выбранного (стр. 755-767).

Переход на эту карту из других экранов: `cSelectMissionState.cpp:122-124, 142-143` (`GAME_REGION`), `cGame_logic.cpp:1349, 1360` (после выигрыша/проигрыша миссии).

### 4е. Пороги раскладки (клампы в `CampaignMapLayout.hpp`)
- `margin`: 14 при `W/48 < 14`, 40 при `> 40` (стр. 24).
- `titleHeight`: 44 при `H/14 < 44`, 64 при `> 64` (стр. 25).
- `messageHeight`: 46 при `H/12 < 46`, 64 при `> 64` (стр. 26).
- `buttonHeight`: 42 при `H/15 < 42`, 54 при `> 54` (стр. 27).
- `gap`: 8 при `H/80 < 8`, 14 при `> 14` (стр. 28).
- `panelPadding`: 14 при `W/100 < 14`, 24 при `> 24` (стр. 29).
- `availableMapHeight` не меньше 180; `availableMapWidth` не меньше 320; `mapWidth` не меньше 320; `mapHeight` не меньше 126 (стр. 31-52).
- `buttonWidth`: 190 при `mapW/4 < 190`, 300 при `> 300` (стр. 76).
- Герб: `crestSize` не меньше 28 (стр. 453-454).
- Ветвления по размеру экрана в `drawHdBackground` и `drawHdChrome` нет.

### 4ж. Вызовы `uiaudit::`
- В `cSelectYourNextConquestState.*` и `CampaignMapLayout.hpp` вызовов нет.
- Через виджет: GuiButton `GuiButton.cpp:49-52` (`Mission select`).

---

## 5. Выбор миссии — `cSelectMissionState` (`cSelectMissionState.cpp`, `.h`)

### 5а. Порядок рисования (`draw()`, `cSelectMissionState.cpp:179-224`)
1. `renderClearToColor {10,12,14,255}` (стр. 181).
2. Если фон есть (стр. 182-210): `main_menu_background.png` вписывается так же, как в выборе дома: `srcAspect > screenAspect` → высота H, ширина `H*srcAspect`, по центру X; иначе ширина W, высота `W/srcAspect`, по центру Y (стр. 183-202); вывод `renderStrechFullSprite` (стр. 203); затем заливка `{3,6,8,150}` на весь экран (стр. 204-209).
3. `gui_window->draw()` (стр. 212): заливка Remaster, заголовок `"<имя дома> Campaign"` (y окна + 2, Yellow), кнопки.
4. Флаг дома: `renderTexture(m_houseFlag->tex, m_flagX, m_flagY, m_flagWidth, m_flagHeight)` (стр. 213-214). Не растягивается по окну, размер уже вычислен.
5. Заголовок `REPLAY MISSION` `drawTextCentered(..., m_headerX, m_headerWidth, m_headerY, Color::Yellow)` (стр. 215-220).
6. `m_mouse->draw()` (стр. 223).

Флаг: `m_houseFlag` — gfxinter `BMP_SELECT_HOUSE_ATREIDES/HARKONNEN/ORDOS/SARDAUKAR` (360×392) по дому человека (стр. 56-68); для других домов — `humanPlayer->getFlagBitmap()` (стр. 67; размер не проверял). Масштаб: `flagScale = min(270/w, 220/h)` (стр. 90-94).

### 5б. Элементы

Геометрия окна:
- `mainMenuWidth = clamp(W - 64, 440, 600)` (стр. 79); `mainMenuHeight = min(H - 64, 500)` (стр. 80); `frameX = (W - mainW)/2`, `frameY = (H - mainH)/2` (стр. 81-82).
- Флаг: `flagX = frameX + (320 - flagW)/2`, `flagY = frameY + 65 + (230 - flagH)/2` (стр. 97-98).
- `buttonHeight = max(30, fontH + 12)` (стр. 100); `buttonWidth = 270` (стр. 101); `leftButtonX = frameX + 25` (стр. 102); `rightButtonX = frameX + mainW - 25 - 270` (стр. 103).
- Заголовок-надпись `REPLAY MISSION`: `headerX = rightButtonX`, `headerWidth = 270`, `headerY = frameY + 42` (стр. 104-106).
- Миссии: `missionButtonY = frameY + 62`, высота 34, шаг 38 (стр. 107-109).
- Back: `backButtonHeight = max(36, fontH + 10)` (стр. 149); прямоугольник `gui_window->getRelativeRect(8, mainH - (bh+8), mainW - 16 - 8, bh)` (стр. 150-154).

| Элемент | Вид | Текст | Геометрия | Шрифт | Цвета | путь:строка |
|---|---|---|---|---|---|---|
| Окно | `GuiWindow`, Remaster | заголовок `<имя дома> Campaign` (`humanPlayer->getHouseName()`) | (frameX, frameY, mainW, mainH) | bene, заголовок Yellow | Remaster | `cSelectMissionState.cpp:84-88` |
| Флаг дома | картинка (renderTexture) | — | (flagX, flagY, flagW, flagH) | — | — | `:90-98, 213-214` |
| Заголовок миссий | ручной текст | `REPLAY MISSION` | (rightX, frameY+42, 270) центр | bene | Yellow `{255,207,41}` | `:104-106, 215-220` |
| CONTINUE | GuiButton REMASTER_BUTTON, **всегда enabled** (при `campaignCompleted` клик ничего не делает) | `CONTINUE` | (leftX = frameX+25, frameY+340, 270, bh) | bene | Remaster | `:111-127` |
| MISSION i (i = 1..highestUnlocked) | GuiButton REMASTER_BUTTON | `MISSION {i}` | (rightX, frameY + 62 + (i-1)*38, 270, 34) | bene | Remaster | `:129-147` |
| Back | GuiButton REMASTER_BUTTON | `Back` | (frameX+8, frameY+mainH-(bh_back+8), mainW-24, bh_back) | bene | Remaster | `:149-166` |

`highestUnlocked = campaignProgress->highestUnlockedMission(house)`, если `CampaignProgress::supportsHouse(house)`, иначе `LAST_MISSION = 9` (стр. 69-71). `campaignCompleted = nextMission(house) == COMPLETED` (стр. 72-73). Константы: `FIRST_MISSION = 1`, `LAST_MISSION = 9`, `COMPLETED = 10` (`src/game/CampaignProgress.hpp:31-33`).

### 5в. Зоны нажатия вне виджетов
Нет. `onNotifyMouseEvent` → только `gui_window->onNotifyMouseEvent(event)` (`cSelectMissionState.cpp:226-229`). Флаг не кликабелен.

### 5г. Клавиши
Нет. `onNotifyKeyboardEvent` пустой (`cSelectMissionState.cpp:236-238`).

### 5д. Переходы
| Кнопка | Действие | путь:строка |
|---|---|---|
| CONTINUE | если не `campaignCompleted`: `jumpToSelectYourNextConquest(highestUnlocked)`; `setNextStateWithFade(highest == 1 ? GAME_BRIEFING : GAME_REGION)` | `:118-125` |
| MISSION i | `jumpToSelectYourNextConquest(i)`; `setNextStateWithFade(i == 1 ? GAME_BRIEFING : GAME_REGION)` | `:141-144` |
| Back | `setNextState(prevState)` (без затухания); prevState — состояние при создании (`cCreatorState.cpp:162-163`) | `:162-164` |

`jumpToSelectYourNextConquest(mission)` → `cGame::jumpToSelectYourNextConquestMission` (`cGame_logic.cpp:913-`): для миссии 1 только задаёт `mission = 1`, `region = 1`; для остальных создаёт/берёт `cSelectYourNextConquestState` и вызывает `installWorld()` (`:913-930`).

### 5е. Пороги раскладки
- `mainMenuWidth`: 440 при `W - 64 < 440`, 600 при `W - 64 > 600` (`:79`).
- `mainMenuHeight = min(H-64, 500)` — верхняя граница 500 при `H - 64 > 500`, т.е. `H > 564` (`:80`).
- `buttonHeight` (Continue и миссии): не меньше 30 (`:100`); Back: не меньше 36 (`:149`).
- Ширина кнопок фиксирована 270 и `rightButtonX` зависит от `mainW`.
- Флаг: не больше 270×220 (`:90-91`).

### 5ж. Вызовы `uiaudit::`
- В `cSelectMissionState.*` вызовов нет. Через виджеты: GuiButton (`GuiButton.cpp:49-52`), GuiWindow (`GuiWindow.cpp:39-41`).

---

## 6. Настройка схватки — `cSetupSkirmishState` (`cSetupSkirmishState.cpp`, `.h`)

### 6а. Порядок рисования (`draw()`, `cSetupSkirmishState.cpp:436-534`)
1. `renderClearToColor {10,13,15,255}` (стр. 438). Картинок (фон-текстуры) нет.
2. Верхняя панель `topBar` = (-1,-1, W+4, 28): заливка `{25,31,35,255}`, рамка `colorDarkishBorder` (стр. 445). Текст `Skirmish` `drawTextCentered(msg, y=(28 - fontH)/2, {231,190,91})` (стр. 446-450).
3. Заголовок игроков `playerTitleBar` (стр. 451): заливка `colorLightBackground {21,27,31}`, рамка `colorDarkishBorder {173,125,39}`.
4. `topRightBox` (стр. 452): заливка `{25,31,35}`, рамка darkish.
5. `playerList` (стр. 453): заливка `colorLightBackground`, рамка darkish.
6. `mapListTitle` (стр. 454) + `Maps` (стр. 455-461, y+4, цвет `{231,190,91}`).
7. `previewMapTitle` (стр. 462) + `Preview` (стр. 463-469).
8. `previewMap` (стр. 470) — панель предпросмотра; `selectArea` (стр. 471) — панель списка карт.
9. Предпросмотр и инфо (`drawPreviewMapAndMore`, стр. 473, 641-697).
10. Строки настроек: `drawStartPoints` (474), `drawWorms` (475), `drawBlooms` (476), `drawDetonateBlooms` (477), `drawTechLevel` (478).
11. Список карт `drawMapList(selectArea)` (стр. 479, 1446-1531).
12. Заголовки колонок игроков `Player`, `House`, `Credits`, `Units`, `Team` (стр. 481-495).
13. Строки игроков (стр. 497-510): для `p < AI_WORM - 1 (= 5)`, `y = playerList.y + 4 + p*26`; при `p < iStartingPoints` — `drawPlayerBrain`, `drawHouse`, `drawCredits`, `drawStartingUnits`, `drawTeams`.
14. Нижняя панель `(-1, H-28, W+2, 30)`: заливка `{25,31,35}`, рамка darkish (стр. 512-516).
15. `startButton` и `modifyButton`: enabled/theme по `iSkirmishMap > -1` (стр. 518-523).
16. Кнопки: `backButton`, `startButton`, `modifyButton`, `newMapButton`, `surpriseMeButton`, `nextMapButton`, `previousMapButton` (стр. 524-530).
17. `m_mouse->draw()` (стр. 533).

Предпросмотр (`drawPreviewMapAndMore`, стр. 641-697):
- `iSkirmishMap > 0`: если `selectedMap->name` не пуст и есть `terrain` — картинка `previewTex` в `previewMapRect` с сохранением пропорции: при `w > h` — `dst = (x, y, pw, pw*h/w)`; иначе `(x, y, ph*w/h, ph)` (стр. 647-663).
- `iSkirmishMap == 0` (случайная): `dst = (x, y, pw, pw)`; при наведении мыши на `previewMapRect` — `previewTex`, иначе `BMP_UNKNOWNMAP` (gfxinter 16, 512×512) (стр. 664-672).
- Инфо-блок (только при `iSkirmishMap > -1`), `infoY = previewMapRect.y + h + 8`, `infoRowH = fontH + 2` (стр. 673-674):
  - `Name: {name}` цвет `Yellow`, `(previewRect.x + 4, infoY)` (стр. 675-677);
  - размер (`getMapSize`) справа: `(W - textLen - 4, infoY)`, цвет `colorDarkerYellow {255,224,139}` (стр. 676, 678-683);
  - `Author: {author}` белым, `(x+4, infoY + rowH)` (стр. 684-689);
  - `description` белым, `(x+4, infoY + 2*rowH)` (стр. 690-695).

### 6б. Элементы

Геометрия (`cSetupSkirmishState` ctor, `cSetupSkirmishState.cpp:93-402`). Константы: `topBarHeight = 28`, `previewMapHeight = 129`, `previewMapWidth = 129`, `widthOfRightColumn = 300`, `mapItemButtonHeight = 150`, `mapItemButtonWidth = 145`, `m_playerRowHeight = 26` (стр. 161-168). Ширина правой колонки `widthOfSidebar = 300 + 2 = 302` (стр. 181).

| Прямоугольник | Формула (x, y, w, h) | путь:строка |
|---|---|---|
| `topBar` | (-1, -1, W+4, 28) | `:175-178` |
| `playerTitleBar` | (0, 27, W-302, 28) | `:181-186` |
| `topRightBox` | (W-302, 27, 302, 28+129+28=185) | `:189-193` |
| `playerList` | (0, 55, W-302, 28+129=157) | `:196-200` |
| `mapListTitle` | (0, 212, W-302, 28) | `:205-210` |
| `previousMaps` (кнопка Previous) | (4, 212, 60, 28) | `:211` |
| `nextMaps` (кнопка Next) | (W-302-48 = W-350, 212, 50, 28) | `:212` |
| `previewMapTitle` | (W-302, 212, 302, 28) | `:215-219` |
| `previewMap` (панель) | (W-302, 240, 300, H-28-240) | `:224-227` |
| `previewMapRect` | (W-302 + (300-s)/2, 258, s, s), s = min(250, H-268-92=H-360) | `:228-234` |
| `selectArea` | (0, 240, W-302, H-268) | `:236` |
| `startPointsRect` | (W-300, 34, 260, fontH+4) | `:281-285` |
| `wormsRect` | (W-300, 66, 260, fontH+4) | `:287-292` |
| `bloomsRect` | (W-300, 98, 260, fontH+4) | `:295-299` |
| `detonateBloomsRect` | (W-300, 130, 260, fontH+4) | `:301-305` |
| `techLevelRect` | (W-300, 162, 260, fontH+4) | `:307-311` |
| `backButton` | (0, H-28, 150, 28) | `:317-320` |
| `startButton` | (W-150, H-28, 150, 28) | `:337-340` |
| `surpriseMeButton` | (startX - 15 - w, H-26, w, 24), w = textLen("Surprise me") + 8 | `:355-357` |
| `newMapButton` | (centerX, H-26, w, 24), w = textLen("New Map") + 8; centerX = W/2 - groupW/2 | `:369-374` |
| `modifyButton` | (centerX + newW + 15, H-26, w, 24), w = textLen("Modify") + 8 | `:386-387` |

Макс. карт в области: `maxMapsInSelectAreaHorizontally = selectArea.w / (145+10)`, `maxMapsInSelectAreaVertically = selectArea.h / (150+15)`, `maxMapsInSelectArea = H*V` (стр. 240-242).

Плитка карты (`drawMapList`, стр. 1446-1531): старт `(x0 + 5, y0 + 5)`; шаг по X 145+15, по Y 150+15; перенос строки при `x + 145 > selectArea.endX` (стр. 1524-1529). Внутри: текст имени `(x+4, y+4)` с обрезкой `...` по ширине `145-8` (стр. 1492-1503); картинка `(x+4, y + fontH + 7, 145-8, 150 - fontH - 11)` (стр. 1514-1520).

Игроки. Строка p: `y = playerList.y + 4 + p*26`; высота ячеек 16. Колонки отрисовки (`SkirmishPlayerTableLayout(y, height=16)`, стр. 64-85): `player (4, w68)`, `house (72, w94)`, `credits (166, w89)`, `units (255, w70)`, `team (325, w75)`; заголовки в `playerTitleBar.y + 3`.

| Строка / элемент | Вид | Текст (формат) | Значения и переход | Цвета | путь:строка |
|---|---|---|---|---|---|
| Игрок p (brain) | текст + клик | `Human` (human), `CPU` (остальные) | клик ЛКМ по (4, y, 73, 16) для p>1: переключает `bPlaying` | Human — White; CPU — White если playing, иначе colorDisabled `{92,96,98}`; hover — цвет screenFader(255,0,0) / (128,128,128) | `:603-624, 1196-1218` |
| House | текст + клик | `Random` (iHouse=0), иначе `Atreides`/`Harkonnen`/`Ordos`/`Sardaukar` | ЛКМ по (74, y, 76, 16): iHouse++ (если >4 → 0); ПКМ: iHouse-- (если <0 → 4) | getTextColorForRect | `:589-601, 1229-1234, 1134-1143` |
| Credits | текст + клик | `{iCredits}` (число), стартово 2500 | ЛКМ по (174, y, 56, 16): +500; если >10000 → 1000. ПКМ: -500; если <1000 → 10000 | getTextColorForRect | `:562-572, 1241-1246, 1146-1156` |
| Units | текст + клик | `{startingUnits}`, стартово 3 | ЛКМ по (272, y, 21, 16): ++; если >10 → 0. ПКМ: --; если <0 → 10 | getTextColorForRect | `:548-560, 1253-1257, 1159-1168` |
| Team | текст + клик | `{team}`, стартово i+1 | ЛКМ по (340, y, 21, 16): ++; если >iStartingPoints → 1. ПКМ: --; если <1 → iStartingPoints | getTextColorForRect | `:536-546, 1265-1269, 1171-1180` |

Правила строк игроков (`cSetupSkirmishState.cpp:1124-1273`):
- Строки рисуются и кликаются только для `p < iStartingPoints`; ПКМ-правка пропускает неактивные (`if (!bPlaying) continue`, стр. 1131). Брейн-переключатель ЛКМ доступен для p>1 (стр. 1210); `p=0` — человек, `p=1` — всегда играет.
- Начальные значения (ctor, стр. 120-135): `bHuman = (i==0)`, `bPlaying = (i <= 1)`, `startingUnits = 3`, `iCredits = 2500`, `iHouse = 0`, `team = i+1`.

Остальные строки настроек:

| Элемент | Вид | Текст (формат) | Клик / значения | Цвета | путь:строка |
|---|---|---|---|---|---|
| Startpoints | текст + клик (только `iSkirmishMap == 0`) | `Startpoints: {iStartingPoints}` | ЛКМ: +1, если >4 → 2, затем `generateRandomMap()`; ПКМ: -1, если <2 → 4, затем `generateRandomMap()` | White; Red при hover и iSkirmishMap==0; для других карт colorDisabled | `:626-639, 1301-1314, 1533-1546` |
| Worms | текст + клик | `Worms? : {spawnWorms}` | ЛКМ: +1, если >4 → 0; ПКМ: -1, если <0 → 4. Начально 2 | White / Red при hover | `:718-723, 1291-1299, 1548-1556` |
| Spice blooms | текст + клик | `Spice blooms : YES|NO` | ЛКМ: переключает `spawnBlooms`. Начально YES | White / Red при hover | `:711-716, 1284-1289` |
| Auto-detonate | текст + клик (только при spawnBlooms) | `Auto-detonate : YES|NO`; при выкл. blooms — `Auto-detonate : -` (colorDisabled) | ЛКМ (только при spawnBlooms): переключает `detonateBlooms`. Начально YES | White / Red при hover | `:699-709, 1275-1282` |
| TechLevel | текст + клик | `TechLevel : {techLevel}` | ЛКМ: ++, если >9 → 2; ПКМ: --, если <2 → 9. Начально 9 | White / Red при hover | `:725-730, 1570-1578, 1559-1568` |

Список карт (`drawMapList`, стр. 1446-1531, `onMouseLeftButtonClickedAtMapList`, стр. 1316-1371):
- Индекс 0 — `Random map` (`cPreviewMaps.cpp:419`) — случайная карта, генерируется (`generateRandomMap`).
- Остальные — `resources/bin/skirmish/*.ini`: 37 файлов, загрузка `cPreviewMaps.cpp:299-305` (`directory_iterator("skirmish")`, `.ini`). Названия берутся из `Title`. Примеры: `Ancient Delta`, `Bottle Neck`, `Broken Mountains`, `Cliffs of Rene`, `David's Pass`, `Division`, `Drifting Plains`, `Duality`, `Duran'Cut`, `Edge to Edge`, `Kig-Yar`, `Kynes Valley Loop`, `M'Rel Canyon`, `Marland Cove`, `Martha's Rock`, `Mayberry Rise`, `Ogelle Basin`, `Rabban`, `Silverstone Channel`, `Sanctuarys`, `Twin Fists`, `Two Stacks`, `Focal Point`, `Gankyil`, `Guillermo Gorge`, `Middle Man`, `Uvavu Basin`, `Felis Cathedra`, `Golek Crossing`, `Huelsbeck Ring`, `Isis Fields`, `Bad Neighbours`, `Sietch Stefan`, `Sinéad Plains`, `The Warm Place`, `Worms Hole` (полный список — `resources/bin/skirmish/*.ini`, строка 2 каждого файла).
- Клик по плитке (ЛКМ, `validMap` и hover): `iSkirmishMap = idx`; при idx=0 → `generateRandomMap()`; иначе `iStartingPoints = count(iStartCell > -1)` и `bPlaying = false` для `p >= iStartingPoints` (стр. 1341-1359).
- Постраничность: `nextFunction` — `start += maxMapsInSelectArea`, если `start + max <= getMapCount()` (стр. 244-250); `previousFunction` — `start -= max`, если `start > 0` (стр. 251-256).
- Текст плитки: `Red` при hover, `White` иначе; выбранная — `Yellow` (или `colorDarkerYellow` при hover) и рамка 2 px `Color::Yellow` вокруг (стр. 1480-1485); невалидная — `colorDisabled` (стр. 1488-1490).
- Размер карты в инфо: `getMapSize`: `(width-2)*(height-2)`: `<=1024` → `SMALL`; `<=4096` → `MEDIUM`; `<=8192` → `LARGE`; иначе `HUGE` (`cPreviewMaps.cpp:442-457`).

Кнопки (GuiButton, REMASTER_BUTTON, тема Remaster; disabled-тема у Start/Modify при пустом выборе):

| Кнопка | Текст | Действие | путь:строка |
|---|---|---|---|
| Back | `Back` | `setNextStateWithFade(GAME_MENU)` | `:317-331` |
| Start | `Start` | если `isValidMap(iSkirmishMap)` → `prepareSkirmishGameToPlayAndTransitionToCombatState(iSkirmishMap)` | `:337-353` |
| Surprise me | `Surprise me` | `surpriseMe()` | `:355-366` |
| New Map | `New Map` | `setNextStateWithFade(GAME_NEW_MAP_EDITOR)` | `:369-384` |
| Modify | `Modify` | если `iSkirmishMap > -1`: `m_scenarioFlow->loadMapFromEditor(iSkirmishMap)`; `fadeOut()` (следующее состояние не задаётся в этом месте) | `:386-401` |
| Next | `Next` | `nextFunction` (листинг карт) | `:258-266` |
| Previous | `Previous` | `previousFunction` | `:268-276` |

Старт игры: `prepareSkirmishGameToPlayAndTransitionToCombatState` (стр. 769-1084): `m_dataCampaign->mission = techLevel` (стр. 774); `setupPlayers()` (776); `setSkirmish(true)` (779); карта пересоздаётся; в конце `drawManager->missionInit()` и `setNextStateWithFade(GAME_PLAYING)` (стр. 1081-1083).

`surpriseMe()` (стр. 1373-1413): случайная валидная карта; для 0: `iStartingPoints = 2 + rnd(3)`; для остальных `iStartingPoints = 2 + rnd(maxPlayers - 1)`; у игроков `bPlaying = p < iStartingPoints`, `iHouse = 0`, `iCredits = 1000 + rnd(19)*500`; человек играет; затем старт.

`generateRandomMap()` (стр. 1415-1444): 128×128; `spawnWorms = (128*128 > 64*64) ? 4 : 2` → всегда 4 (стр. 1432); `author = "D2TM"` (стр. 1435).

Цвета (ctor, стр. 155-159): `colorDarkishBorder {173,125,39,255}`, `colorDarkerYellow {255,224,139,255}`, `colorDisabled {92,96,98,255}`, `colorLightBackground {21,27,31,255}`, `colorOtherBorder {102,78,35,255}`. Заголовки колонок и подписи `{231,190,91,255}`.

Цвет выбора цвета игрока: в `cSetupSkirmishState` не найдено. Колонки: Player, House, Credits, Units, Team.

### 6в. Зоны нажатия вне виджетов
Все клики по прямоугольникам через `isPointWithin` / `mouse_within_rect`:
- строки игроков (brain, house, credits, units, team) — см. 6б;
- `startPointsRect`, `wormsRect`, `bloomsRect`, `detonateBloomsRect`, `techLevelRect`;
- `selectArea` (список карт) — плитки по формуле 6б;
- ПКМ: те же зоны (startPoints, worms, player list, tech level). Blooms/detonate — только ЛКМ.
- `mouse_within_rect` (стр. 87-91): x в `[x, x+w)`, y в `[y, y+h]`.
- Пиксельные зоны (`isPointWithin`) и GuiButton-обработка — обе ветви работают на одном событии.
- `MOUSE_MOVED_TO` — пустой обработчик (стр. 1580-1582).

Несовпадение геометрии (факт): колонки текста рисуются по `SkirmishPlayerTableLayout` (house x=72..166, credits x=166..255, units x=255..325, team x=325..400), а зоны клика — по константам 74/76 (house), 174/56 (credits), 272/21 (units), 340/21 (team). Зоны не совпадают с отрисованными колонками (стр. 1134-1173, 1237-1263 против 64-85, 481-510).

### 6г. Клавиши (`onNotifyKeyboardEvent`, `cSetupSkirmishState.cpp:1611-1635`, PRESSED)
- `MENU_BACK` (Escape) → `setNextStateWithFade(GAME_MENU)` (стр. 1614-1616).
- `SCROLL_LEFT` (Left) → `moveCursor(-1, 0)`; `SCROLL_RIGHT` (Right) → `moveCursor(1, 0)`; `SCROLL_UP` (Up) → `moveCursor(0, -1)`; `SCROLL_DOWN` (Down) → `moveCursor(0, 1)` (стр. 1617-1628). Ключи: `settings.ini:106-109`.
- `MENU_CONFIRM` (Return) → если `isValidMap(iSkirmishMap)` → `prepareSkirmishGameToPlayAndTransitionToCombatState` (стр. 1629-1633). Ключ: `settings.ini:144`.
- `moveCursor(dx, dy)` (стр. 1584-1609): если `iSkirmishMap == -1` → `iSkirmishMap = mapStartingIndexToDisplay`; иначе `newIndex = idx + dx + dy*maxMapsInSelectAreaHorizontally`, `clamp(newIndex, 0, getMapCount())`; `mapStartingIndexToDisplay = (idx / maxMapsInSelectArea) * maxMapsInSelectArea`; для idx 0 и невалидной карты выход; иначе `iStartingPoints` = число стартовых ячеек, `bPlaying = false` для лишних.

### 6д. Переходы
| Действие | Куда | путь:строка |
|---|---|---|
| Back / Escape | `GAME_MENU` с затуханием | `:329, 1615` |
| Start / Enter | `GAME_PLAYING` с затуханием (через `prepareSkirmish...`) | `:349-351, 1083, 1630-1632` |
| Surprise me | `GAME_PLAYING` (через `prepareSkirmish...`) | `:365, 412` |
| New Map | `GAME_NEW_MAP_EDITOR` с затуханием | `:382` |
| Modify | `loadMapFromEditor(iSkirmishMap)`; `fadeOut()` (состояние задаёт `ScenarioFlow`, не проверял) | `:396-399` |

### 6е. Пороги раскладки
- `previewSize = min(250, H-360)` (`:228`): 250 при `H-360 >= 250`, т.е. `H >= 610`.
- Ширина колонки: `widthOfSidebar = 302`, `widthOfRightColumn = 300`, `startPointHitBoxWidth = 260` — константы, не клампы.
- Число карт в области: `W-302` делится на 155, `H-268` делится на 165 (стр. 240-242).
- `btnHeight = topBarHeight - 4 = 24` (стр. 315).
- Ветвлений по размеру экрана нет; все прямоугольники заданы относительно W и H.

### 6ж. Вызовы `uiaudit::`
- В `cSetupSkirmishState.*` вызовов нет.
- Через виджеты: GuiButton (`GuiButton.cpp:49-52`) — кнопки Back, Start, Modify, New Map, Surprise me, Next, Previous.

---

## 7. Сводка по `uiaudit::` (вызовы, которые касаются экранов через общие классы)

| Место | Строка | Запись |
|---|---|---|
| `src/gui/GuiButton.cpp` | 49-52 | `isEnabled()`, `auditRecord("GuiButton")`, `auditClick("GuiButton:" + text)` |
| `src/gui/GuiCheckBox.cpp` | 42-45 | `auditRecord("GuiCheckBox")`, `auditClick("GuiCheckBox")` |
| `src/gui/GuiLabel.cpp` | 42-44 | `auditRecord("GuiLabel")` |
| `src/gui/GuiSlider.cpp` | 76-79 | `auditRecord("GuiSlider")`, `auditClick("GuiSlider")` |
| `src/gui/GuiWindow.cpp` | 39-41 | `auditRecord("GuiWindow")` |
| `src/gui/GuiObject.cpp` | 37 | `uiaudit::recordGui(type, x, y, w, h)` |
| `src/gui/GuiObject.cpp` | 42 | `uiaudit::recordClick(name, x, y, w, h)` |
| `src/drawers/cTextDrawer.cpp` | 51-52 | `recordText(msg, x, y, w, h)` |
| `src/drawers/cTextDrawer.cpp` | 97-98, 182-183 | `std::optional<uiaudit::BoxScope>` |
| `src/drawers/cTextDrawer.cpp` | 129-131, 158-160 | `recordText(msg, x, y, w, h, &box)` |
Глобальные (не экранные): `src/main.cpp:60-62, 123-124, 128, 150`, `src/game/cGame_logic.cpp:576, 615, 627-628, 637-638`, `src/game/cSDLSystem.cpp:206`. Сценарии: `src/debug/UiAuditScenes.cpp:18, 34-41` — только `main-menu`.

Файлы экранов (шесть) не содержат ни одного вызова `uiaudit::` (поиск `uiaudit` по `src/`, см. раздел 9).

---

## 8. Неопределённости и непроверенное

- Семантика `getScreenW/H` (логический холст) vs `getOutputW/H` (окно) — не проверял, какой холст используется при `Texture`-масштабе.
- `fontH` (`getFontHeight()`) — значение в пикселях не измерял, поэтому все формулы с fontH даны как символы.
- `drawTextBottomRight(color, msg, margin)` — семантика третьего аргумента `18` не проверял (`cTextDrawer.h:64`).
- `renderStrechFullSprite(tex, rect, opacity)`: по умолчанию `opacity = 255` (`SDLDrawer.hpp:35`); влияние `Texture`-density на масштаб при отрисовке не проверял.
- Внутренняя геометрия `GuiSlider`, `GuiCheckBox`, `GuiLabel` (стрелки, полоса, галочка) не разбирал — вне шести экранов.
- `GuiButton` — какое событие мыши вызывает `onClick` (нажатие/отпускание) не разбирал.
- `timeManager->getGlobalSpeed()` (значение по умолчанию для Game speed) — не проверял.
- Цвет при hover в `getTextColorForRect` берётся из `m_screenFader->getColorFadeSelected(...)` — функция не читал, значение может меняться во времени.
- `D2TM_VERSION` / `D2TM_BUILD_DATETIME` — генерируются из `config.h.in` (CMake); конкретные значения не найдены в этом проходе.
- `main_menu_background.png` в экранах 1, 3, 4, 5 — один и тот же файл (`resources/bin/data/hd4/`). Совпадение файлов в `bin/` (генерируемая копия) не проверял.
- Размеры gfxinter-спрайтов взяты из `resources/bin/data/sdl_inter_hd4.dat` (упакован). Копию в `bin/data/` не сравнивал.
- Для `cSelectMissionState`: размер флага для не-военных домов (`getFlagBitmap()`) не проверял.
- Для `cSelectYourNextConquestState`: содержимое `WORLD_DUNE_CLICK` (значения пикселей → регионы 1..27) не проверял. Значения `iHouse`, `bSelectable`, `iAlpha` для каждой миссии — из `campaign/*/mission*.ini`, не читал.
- Для `cSetupSkirmishState`: `cRandomMapGenerator::generateRandomMap` и `cPreviewMaps::createEmptyMap` не читал; название случайной карты задано `cPreviewMaps.cpp:419` (`Random map`), но перезапись имени в генераторе не проверял.
- Для `cSetupSkirmishState`: поведение `setupPlayers()`, `loadMapFromEditor()`, `getMapSize` для размеров больше 8192 клеток не проверял.
- Расхождение геометрии клика и отрисовки колонок игроков в `cSetupSkirmishState` (см. 6в) — зафиксировано как факт кода; причина и намерение не проверял.
- Несоответствие `cChooseHouseState::getType()` возвращаемому типу экрана (см. 3б) — факт кода; назначение не проверял.
- Все разделы Options (раздел 2) — проверено по `cOptionsState.cpp`; разбор `Preferences::saveScales` и `PreferencesPath::file` не читал.

---

## 9. Выполненные команды и результаты

Все команды только чтение. Git не запускался. Пакеты не ставились. Субагентов не запускал.

1. `Glob src/gamestates/*` — список файлов `cMainMenuState.*`, `cOptionsState.*`, `OptionsMenuLayout.hpp`, `cChooseHouseState.*`, `cSelectYourNextConquestState.*`, `CampaignMapLayout.hpp`, `cSelectMissionState.*`, `cSetupSkirmishState.*` найдены.
2. `wc -l` по шести экранам: `cMainMenuState.cpp` 295, `.h` 75; `cOptionsState.cpp` 640, `.h` 79; `OptionsMenuLayout.hpp` 144; `cChooseHouseState.cpp` 277, `.h` 81; `cSelectYourNextConquestState.cpp` 1070, `.h` 193; `CampaignMapLayout.hpp` 127; `cSelectMissionState.cpp` 238, `.h` 64; `cSetupSkirmishState.cpp` 1636, `.h` 217.
3. `Grep "uiaudit::|uiaudit" src/` — 0 совпадений в файлах `src/gamestates/*`; совпадения в `src/gui/*`, `src/drawers/cTextDrawer.cpp`, `src/main.cpp`, `src/game/cGame_logic.cpp`, `src/game/cSDLSystem.cpp`, `src/debug/UiAudit*`.
4. `Grep` по `cOptionsState(|cSelectMissionState(|...|prepareToTellAboutHouse|loadHdUiTexture(|getBeneTextDrawer|Remaster()|FIRST_MISSION|LAST_MISSION|COMPLETED|jumpToSelectYourNextConquest|GAME_REGION` — вывод учтён в разделах 1-6, в т.ч. `CampaignProgress.hpp:31-33`, `GuiTheme.hpp:39,56`, `cCreatorState.cpp:98-170`.
5. `Grep installWorld|loadRegionfile|setNextState(|setNextStateWithFade(|fadeOut(` — вызовы переходов учтены.
6. `sed`/`cat` `src/utils/HdUiTextureLoader.cpp`, `src/gui/GuiTheme.hpp`, `cCreatorState.cpp:145-170`, `ContextCreator.cpp:35-125`, `settings.ini:81-92`, `ini.cpp:78-107`, `cGame_logic.cpp:220-260, 913-932, 940-970, 1078-1092, 1119-1130, 1272-1290, 1340-1362` — выводы учтены.
7. `ls resources/bin/data/hd4/` — 12 файлов, включая `main_menu_background.png`, `main_menu_logo.png`, `campaign_map.png`, `hud_house_*.png`.
8. `ls resources/bin/skirmish/*.ini | wc -l` — 37.
9. Скрипт `dims.py` (вне репозитория, `C:\Users\Slaven\AppData\Local\Temp\claude\a0c06789fe226c20\97deb261-de69-4897-9696-03fe6181af4a\scratchpad\dims.py`), запуск `Python313\python.exe -I`, только чтение:
   - `sdl_inter_hd4.dat`: idx 0 `BMP_D2TM` 2432×664; idx 11 `BMP_SELECT_HOUSE_ATREIDES` 360×392; idx 12 `BMP_SELECT_HOUSE_HARKONNEN` 360×392; idx 13 `BMP_SELECT_HOUSE_ORDOS` 360×392; idx 144 `BMP_SELECT_HOUSE_SARDAUKAR` 360×392; idx 16 `BMP_UNKNOWNMAP` 512×512; всего 146 записей.
   - hd4 PNG: `main_menu_background.png` 5120×1440; `main_menu_logo.png` 1792×320; `campaign_map.png` 2432×960; `hud_house_atreides/harkonnen/ordos.png` 384×384.
   - Первый запуск дал ошибку из-за неверного шага записи (48 вместо 52 байт) и исправлен; второй запуск успешный, код выхода 0.
10. Ошибка: `python3` в PATH — заглушка Store, выход 49; использован полный путь к `Python313\python.exe`.
11. `Grep` `src/gameobjects/map/cPreviewMaps.cpp` — `getMapSize`, `skirmish/` сканирование (строки 299-305), random map name (419).
12. `sed -n` по `src/utils/cPack.cpp` — формат `D2TM`, размеры полей (`cPack.cpp:25-35, 103-126, 168-173`).

## 10. Расход токенов

По счётчику total_tokens: старт 15 000 000, последнее значение 14 691 865, расход ≈308 000 (включая чтение файлов, скрипт, правки и запись этого файла).
