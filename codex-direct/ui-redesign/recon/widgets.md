# Карта фактов: общий слой UI (виджеты, тема, текст, шрифты, примитивы)

Рабочая копия: W = `C:/Users/Slaven/Projects/DUNE/.claude/worktrees/ui-redesign-360d77`. Пути ниже относительны к W; номера строк — по файлам на момент чтения. Только чтение: git не запускался, файлы кода не менялись.

Цвета записаны как R,G,B,A. Значения по умолчанию `Color(r=0,g=0,b=0,a=255)` (src/utils/Color.hpp:24-25). Именованные: `Color::White` 255,255,255,255; `Color::Black` 0,0,0,255; `Color::Yellow` 255,207,41,255 (src/utils/Color.hpp:54-56).

---

## 1. Шрифты и текст

### 1.1 Файлы шрифтов

- Имена в настройках: `resources/bin/settings.ini:89` `[FONT]`; `:90` `ARRAKEEN=arrakeen.fon`; `:91` `BENEGESS=benegess.fon`; `:92` `SMALL=small.ttf`.
- Чтение: `src/game/cGame_logic.cpp:727-729` (`settings->getStringValue("FONT", ...)` в `m_transfertMap`), передача `src/game/cGame_logic.cpp:737` → `cFileValidator::addResources` (`src/utils/cFileValidator.cpp:36-38`).
- Полный путь: `cFileValidator::getFullName` = `m_path + "/" + имя` (`src/utils/cFileValidator.cpp:76-79`).
- Инициализация SDL_ttf: `src/game/cSDLSystem.cpp:288` `TTF_Init()`.
- Открытие: `src/context/ContextCreator.cpp:78` (ARRAKEEN → `game_font`), `:86` (BENEGESS → `bene_font`), `:94` (SMALL → `small_font`). Размер у всех трёх: `12` (второй аргумент `TTF_OpenFont`, пункты). Ошибка только логируется (`Logger::error`, строки 79-81, 87-89, 95-97), игра не останавливается.
- Закрытие: `src/context/ContextCreator.cpp:103-108`.
- Переменные-члены: `game_font`, `bene_font`, `small_font` (ContextCreator.cpp:78, 86, 94; тип в заголовке ContextCreator.hpp — не открывал).
- Привязка к drawer-ам: `src/context/ContextCreator.cpp:121-127` `createTextContext`: small → `small_font`, bene → `bene_font`, game → `game_font`. Геттеры: `src/context/TextContext.hpp:33-35` (`getSmallTextDrawer`, `getBeneTextDrawer`, `getGameTextDrawer`).
- Файлы, где вызываются геттеры (список файлов, не строк):
  - Small: cDrawManager.cpp, cBuildingListDrawer.cpp, cSideBarDrawer.cpp, cScoringState.cpp (src/managers, src/drawers, src/gamestates).
  - Bene: cChooseHouseState, cCreditsState, cGamePlaying, cEditorState, cScoringState, cOptionsState, cWinLoseState, cMap.cpp, cNewmapEditorState, cSetupSkirmishState, cMainMenuState, cSelectYourNextConquestState, cSelectMissionState (src/gamestates), cStructureDrawer.cpp, AbstractMentat.cpp (src/gameobjects/...).
  - Game: cDrawManager.cpp, cBuildingListDrawer.cpp, cMessageDrawer.cpp, CreditsDrawer.cpp, cGame_logic.cpp.
- Курсор мыши: `src/drawers/cMouseDrawer.cpp:45` `std::make_unique<cTextWriter>(textDrawer, 12)`.
- Не найдено: кроме `.fon`/`.ttf` файлов в настройках иных шрифтов не найдено (rg `TTF_OpenFont` — только ContextCreator.cpp:78,86,94). Сами файлы в репозитории не искал.

### 1.2 Открытые методы cTextDrawer (src/drawers/cTextDrawer.h)

Конструктор: `cTextDrawer(TTF_Font*, cGameSettings*, SDLDrawer*)` (h:31; cpp:29-38: создаёт собственный `cTextTextureCache`). Деструктор h:32.

- h:35 `drawText(int x, int y, const std::string& msg, bool applyShadow=true) const` — белым.
- h:37 `drawText(cPoint& coords, Color color, const std::string& msg, bool applyShadow=true) const` — ссылка на `cPoint` неконстантная.
- h:39 `drawText(int x, int y, Color color, const std::string& msg, bool applyShadow=true) const` — основной (cpp:45-58).
- h:41 `drawTextCentered(const std::string& msg, int y) const` — белым, по центру экрана.
- h:43 `drawTextCentered(const std::string& msg, int y, Color color) const` — по центру экрана (cpp:75-83).
- h:45 `drawTextCentered(const std::string& msg, int x, int width, int y, Color color) const` — центр в полосе (x,width) (cpp:174-187).
- h:52 `drawTextCenteredInBox(const std::string& msg, int x, int y, int boxWidth, int boxHeight, Color color) const` (cpp:85-102).
- h:54 `drawTextCenteredInBox(const std::string& msg, const cRectangle& rect, Color color) const` (cpp:104-107).
- h:56 `drawTextCenteredInBox(const std::string& msg, const cRectangle& rect, Color color, int offsetX, int offsetY) const` (cpp:109-112).
- h:57 `drawTextScaledCenteredInBox(const std::string& msg, const cRectangle& rect, float scale, Color color, bool applyShadow=true) const` (cpp:114-137).
- h:58 `drawTextScaledOpticallyCenteredInBox(const std::string& msg, const cRectangle& rect, float scale, Color color, bool applyShadow=true) const` (cpp:139-172).
- h:60 `drawTextBottomRight(const std::string& msg, int margin=0) const` — белым (cpp:189-192).
- h:62 `drawTextBottomLeft(const std::string& msg, int margin=0) const` — белым (cpp:194-197).
- h:64 `drawTextBottomRight(Color color, const std::string& msg, int margin=0) const` (cpp:199-208).
- h:66 `drawTextBottomLeft(Color color, const std::string& msg, int margin=0) const` (cpp:215-222).
- h:68 `int getTextLength(const std::string& msg) const` — ширина в пикселях (cpp:224-229).
- h:70 `int getFontHeight() const` (cpp:210-213).
- h:72 `void resetCache() const` (cpp:241-244).
- h:74 `cRectangle getRect(int x, int y, const std::string& msg) const` (cpp:231-234).
- h:76 `cRectangle getAsRectangle(int x, int y, const std::string& msg) const` — тот же результат, что getRect (cpp:236-239).

Публичных членов-данных нет. Приватные: `m_font` (h:81), `m_textCache` `unique_ptr<cTextTextureCache>` (h:82), `m_settings` (h:83), `m_renderer` (h:84).

### 1.3 Масштаб, тень, выравнивание, перенос, высота строки

- Масштаб: только в `drawTextScaled*`. `scale = max(0.5F, scale)` (cpp:122, 147). Ширина/высота = `static_cast<int>(size * scale + 0.5F)` (cpp:125-126, 150-151). Обычный `drawText` масштаба не имеет.
  - Дополнительные ограничения у вызывающего: `GuiButton::setTextScale` — `max(0.65F, scale)` (src/gui/GuiButton.cpp:181); в `GuiButton::drawText` — `fittedScale = clamp(min(m_textScale, widthScale, heightScale), 0.65F, m_textScale)` (GuiButton.cpp:205-209).
- Тень: при `applyShadow` рисуется текстура тени (чёрный Solid-текст из кэша) со смещением:
  - `drawText` +1,+1 (cpp:54-56);
  - `drawTextScaledCenteredInBox` +2,+2 (cpp:133-135);
  - `drawTextScaledOpticallyCenteredInBox` +2,+2 (cpp:162-170).
  - Цвет тени зашит: `Color::Black` (src/drawers/cTextTextureCache.cpp:99). `theme.textColorShadow` текст не использует.
  - По умолчанию `applyShadow = true` во всех перегрузках (h:35-58); `drawTextCentered*` и `drawTextBottom*` тень рисуют всегда (через drawText).
- Выравнивание (x_text, y_text):
  - `drawTextCentered(msg,y[,color])`: x = `screenW/2 - w/2` (cpp:80-81). `w` = `TTF_GetStringSize`.
  - `drawTextCenteredInBox(x,y,boxW,boxH)`: x_text = `x + (boxW/2 - w/2)`; y_text = `y + (boxH/2 - h/2)` (cpp:94-96); `w,h` = `TTF_GetStringSize` (cpp:89).
  - `drawTextCentered(x,width,y)`: x_text = `x + (width/2 - w/2)`, y без изменений (cpp:179-181).
  - `drawTextScaledCenteredInBox`: x = `rect.x + (rect.w - width)/2`, y = `rect.y + (rect.h - height)/2` (целочисленное деление; cpp:127-128).
  - `drawTextScaledOpticallyCenteredInBox`: origin из `calculateOpticallyCenteredTextOrigin` (src/utils/TextAlignment.hpp:17-37): центр ink-bbox совпадает с центром rect. `inkCenterX = (ink.x + ink.width/2.0) * drawWidth / textureWidth`; `origin.x = lround(rect.x + rect.w/2.0 - inkCenterX)`; по Y аналогично. Ink-bbox = bbox пикселей с alpha != 0 (cTextTextureCache.cpp:25-69).
  - `drawTextBottomRight`: x = `screenW - w - margin`, y = `screenH - fontHeight - 20 - margin` (cpp:205-206).
  - `drawTextBottomLeft`: x = `margin`, y = `screenH - h - 20 - margin`, h из `TTF_GetStringSize` (cpp:219-221).
  - Левое выравнивание (`LEFT`) — просто `drawText(x, y, ...)`; отдельного метода нет.
- Перенос строк: не найдено. Искал: `rg -i wrap src/drawers src/gui` (пусто); в `src/` вызовов `TTF_RenderText_Wrapped`/`TTF_SetFontWrap` нет. Единственный TTF-рендер — `TTF_RenderText_Solid` (cTextTextureCache.cpp:99,108).
- Многострочный текст — только через несколько `drawText` с шагом по y (см. cTextWriter, 1.5).
- Высота строки: `getFontHeight()` = `TTF_GetFontHeight(m_font)` (cTextDrawer.cpp:210-213) — метрика шрифта, не замер строки. Высота конкретной строки — второй выход `TTF_GetStringSize` (`h`), который cTextDrawer использует в `drawTextCenteredInBox` (cpp:89-96) и `drawTextBottomLeft` (cpp:219).
- Ширина строки: `getTextLength` = `TTF_GetStringSize` `w` (cpp:224-229). `getRect`/`getAsRectangle` = `(x, y, getTextLength, getFontHeight)` (cpp:231-239).
- cTextWriter (src/gui/cTextWriter.cpp:33-54): `moveTo(x,y)` задаёт позицию; каждый `write` вызывает `drawText(drawX, drawY, ...)` и `drawY += fontSize` (аргумент конструктора, `cTextWriter(cTextDrawer*, int fontSize)` h:38). Не класс-виджет; единственный пользователь — `cMouseDrawer` (cMouseDrawer.cpp:45, fontSize 12).
- Усечение текста: в виджетах (GuiTextInput, см. раздел 3), а не в cTextDrawer.

### 1.4 Кэш текста

- Владение: `cTextDrawer::m_textCache` (cTextDrawer.h:82, создаётся cpp:31). Каждый из трёх cTextDrawer имеет свой кэш.
- Ключ: `textKey{std::string msg; Color color}` (src/drawers/cTextTextureCache.h:28-31). Хеш: `hash(msg) ^ hash(uint32((r<<24)|(g<<16)|(b<<8)|a))` (h:33-37). Равенство: msg и все 4 компонента цвета (h:39-44).
- Хранилище: `mutable std::unordered_map<textKey, std::unique_ptr<textCacheEntry>, ...>` (h:68).
- Запись `textCacheEntry` (h:46-53): `SDL_Texture* texture` (цвет), `SDL_Texture* shadowsTexture` (чёрный), `int width, height` (размер поверхности цвета), `TextInkBounds inkBounds`, `int lifeCounter`.
- Создание (cpp:92-122): (1) `TTF_RenderText_Solid(m_font, msg, 0, Black)` → `shadowsTexture` (cpp:99, 104), `SetTextureScaleMode NEAREST` (cpp:105); (2) `TTF_RenderText_Solid(m_font, msg, 0, color)` → `texture` (cpp:108, 113), NEAREST (cpp:114); `width/height` из этой поверхности (cpp:115-116); `inkBounds = findInkBounds(surface)` (cpp:117); `lifeCounter = 10` (cpp:118).
  - Если вторая поверхность не создана, возвращается `nullptr` (cpp:109-112), а уже созданная `shadowsTexture` не уничтожается (cpp:104 создана, cpp:111 выход без SDL_DestroyTexture).
- `findInkBounds` (cpp:25-69): конвертация в RGBA32 (cpp:35), перебор alpha != 0; возвращает `TextInkBounds{textureWidth, textureHeight, x, y, width, height}` (struct в src/utils/TextAlignment.hpp:8-15; дефолты 1,1,0,0,1,1). Если пусто — bbox = вся поверхность.
- Поиск: `findOrCreate(Color, msg)` (cpp:124-137): находит или создаёт; при неудаче `nullptr`.
- Учёт использования: `lifeCounter += 1` при каждом `drawText` (cTextDrawer.cpp:50), `drawTextScaledCenteredInBox` (cpp:124), `drawTextScaledOpticallyCenteredInBox` (cpp:149).
- Очистка: `cTextTextureCache::resetCache()` (cpp:139-153): записи с `lifeCounter == 0` удаляются (обе текстуры уничтожаются), у остальных `lifeCounter = 0`.
- Цепочка вызова: `cTimeManager::handleTimerCache` (src/game/cTimeManager.cpp:178-183) вызывает `m_game->thinkCache()`; `cGame::thinkCache` (cGame_logic.cpp:1619-1622) → `ctx->resetCache()` → `GameContext::resetCache` (GameContext.cpp:84-88) → `TextContext::resetCache` (TextContext.cpp:32-36) → `resetCache` трёх drawer-ов.
- Период: `m_timerMinute.tickDuration = 60000` (cTimeManager.cpp:294); счётчик `count` растёт в cpp:217-219.
- Деструктор кэша уничтожает все текстуры (cTextTextureCache.cpp:79-90).
- Нулевая проверка: `drawText` проверяет `cacheEntry` (cTextDrawer.cpp:49). `drawTextScaledCenteredInBox` (cpp:123-124) и `drawTextScaledOpticallyCenteredInBox` (cpp:148-149) разыменовывают `cacheEntry` без проверки на `nullptr`.
- Сбросов по размеру/по шрифту нет; кэш привязан к `TTF_Font*` и `SDLDrawer*`, переданным в конструктор `cTextTextureCache` (h:58).

---

## 2. Тема GuiTheme

Структура: `src/gui/GuiTheme.hpp:20-38`. Поля (12 шт.):

| Поле | строка |
|---|---|
| fillColor | :22 |
| borderLight | :23 |
| borderDark | :24 |
| background | :25 |
| textColor | :28 |
| textDarkColor | :29 |
| textColorHover | :30 |
| textColorShadow | :31 |
| disabledTextColor | :34 |
| disabledFillColor | :35 |
| disabledBorderLight | :36 |
| disabledBorderDark | :37 |

Значения (R,G,B,A):

| Поле | Remaster() (:41-52) | RemasterInactive() (:58-69) | dark() (:79-90) | inactive() (:95-106) | light() (:111-122) |
|---|---|---|---|---|---|
| fillColor | 24,29,33,238 | 20,24,27,220 | 84,84,120,255 | 84,84,120,255 | 176,176,196,255 |
| borderLight | 190,145,58,255 | 91,84,66,255 | 40,40,40,255 | 40,40,40,255 | 252,252,252,255 |
| borderDark | 71,50,24,255 | 46,42,34,255 | 176,176,196,255 | 176,176,196,255 | 84,84,120,255 |
| background | 32,32,32,255 | 32,32,32,255 | 32,32,32,255 | 32,32,32,255 | 32,32,32,255 |
| textColor | 236,229,202,255 | 132,132,124,255 | White | 192,192,192,255 | White |
| textDarkColor | 225,177,21,255 | 225,177,21,255 | 225,177,21,255 | 128,128,128,255 | 225,177,21,255 |
| textColorHover | 255,202,83,255 | 154,146,124,255 | 255,0,0,255 | Black | 255,0,0,255 |
| textColorShadow | 4,6,7,220 | 4,6,7,220 | Black | 128,128,128,255 | Black |
| disabledTextColor | 132,132,124,255 | 132,132,124,255 | 128,128,128,255 | 128,128,128,255 | 128,128,128,255 |
| disabledFillColor | 20,24,27,220 | 20,24,27,220 | 64,64,100,255 | 64,64,100,255 | 146,146,166,255 |
| disabledBorderLight | 91,84,66,255 | 91,84,66,255 | 40,40,40,255 | 40,40,40,255 | 84,84,120,255 |
| disabledBorderDark | 46,42,34,255 | 46,42,34,255 | 20,20,20,255 | 176,176,196,255 | 128,128,128,255 |

- Строки билдера: `dark()` — `GuiTheme.hpp:78-92`; `inactive()` — `:94-108`; `light()` — `:110-124`; `withTextColor(c)` — `:126-129` (меняет только textColor); `build()` — `:131-146`; поля билдера — `:148-160`.
- Использование фабрик в `src/`: `GuiTheme::Remaster()` и `RemasterInactive()` — в gamestates и gameobjects (см. раздел 4, cMainMenuState.cpp:133,146,186; cSetupSkirmishState.cpp:263-393, 520-522; cSelectMissionState.cpp:86,116,139,160; cOptionsState.cpp:82,170,182,532; cCreditsState.cpp:91; cSelectYourNextConquestState.cpp:170). `cGuiThemeBuilder().light()` — в cNewmapEditorState, cEditorState, AbstractMentat.cpp:92, cOptionsState.cpp:212 (с `withTextColor(Color::Yellow)`), и как дефолт параметров виджетов.
- `dark()` и `inactive()` в `src/` не вызываются (rg `\.dark\(\)|\.inactive\(\)` — пусто).
- Дефолтная тема виджетов: `GuiButton.h:188`, `GuiCheckBox.hpp:31`, `GuiSlider.hpp:30`, `GuiLabel.hpp:34`, `GuiStateButton.h:30`, `GuiTextInput.h:94`, `GuiCycleButton.h:110`, `GuiValueButton.h:147` — `cGuiThemeBuilder().light().build()`. В `GuiConsole.cpp:45` тема `light()` задана явно.
- `GuiObject::m_theme` (`GuiObject.h:92`) без инициализатора; `GuiTheme` без member-инициализаторов, значит поля — `Color()` = 0,0,0,255 (Color.hpp:24-25). Так выглядит тема `GuiWindow` в `GuiConsole` (см. 3.12).

### Кто читает каждое поле

- **fillColor**
  - GuiObject.cpp:68 `drawRectFillBorder` (через `renderRectFillColor(rect, color)` — перегрузка с `opacity`, альфа Color **не** используется; см. 5). Вызывают: GuiWindow.cpp:43, GuiBar.cpp:45, GuiCycleButton.cpp:71.
  - GuiButton.cpp:61, 68 — OPAQUE_WITHOUT/WITH_BORDER: перегрузка `(x,y,w,h,Color)`, альфа **используется** (238 у Remaster).
  - GuiButton.cpp:101-130 — REMASTER_BUTTON: fill с модификацией, вызов `renderRectFillColor(m_rect, fillColor)` (cpp:130), альфа **не** используется.
  - GuiCheckBox.cpp:50, 58 (int-перегрузка, альфа используется); GuiLabel.cpp:47, 55 (int-перегрузка, альфа используется).
  - GuiSlider.cpp:85 (трек, rect-перегрузка, альфа не используется); GuiValueButton.cpp:95 (rect-перегрузка).
- **disabledFillColor**: GuiButton.cpp:61, 68 (`isDisabled ? disabledFillColor : fillColor`, только OPAQUE_*). Другие виджеты не читают.
- **borderLight / borderDark**
  - GuiObject.cpp:61-63 `drawRectBorder` (`renderRectColor(rect, borderRect)` + 2 `renderLine`), вызывается из GuiObject.cpp:69 и напрямую: GuiCheckBox.cpp:62, 106 (`drawBox`); GuiLabel.cpp:56, 60; GuiSlider.cpp:86.
  - SDLDrawer `gui_DrawRectBorder` (SDLDrawer.cpp:180-198): GuiButton.cpp:70, 74, 83, 87 (OPAQUE/TRANSPARENT с рамкой; при нажатии светлая/тёмная меняются местами); GuiValueButton.cpp:97, 99; GuiSlider.cpp:97 (knob).
  - GuiButton REMASTER: `outerBorder = borderDark`, `innerBorder = borderLight` (GuiButton.cpp:102-103), при нажатии `std::swap` (cpp:120); строка-подсветка при `enabled&&focus` иначе `borderLight` (cpp:146).
  - GuiSlider knob: fill `borderDark` (GuiSlider.cpp:96, rect-перегрузка), border (light,dark) (cpp:97).
- **disabledBorderLight / disabledBorderDark**: GuiButton.cpp:76, 89 — только для OPAQUE_WITH_BORDER и TRANSPARENT_WITH_BORDER, когда не нажата и disabled.
- **background**: GuiTextInput.cpp:54 — единственный читатель (fill всей области поля).
- **textColor**: GuiButton.cpp:193 (обычный текст, если не hover и не disabled); GuiLabel.cpp:99 (всегда); GuiCycleButton.cpp:75; GuiValueButton.cpp:103 (через `focus ? hover : textColor`); GuiTextInput.cpp:60; GuiCheckBox.cpp:93, 100 (две линии «галочки»).
- **textDarkColor**: не найдено. Поле объявлено (GuiTheme.hpp:29) и заполняется в 5 местах (:46, :63, :84, :100, :116), но в `src/` не читается (rg по всему `src`).
- **textColorHover**: GuiButton.cpp:145 (REMASTER-подсветка, `enabled && focus`), :193 (текст при hover/focus); GuiValueButton.cpp:103 (текст при focus); GuiTextInput.cpp:57 (рамка фокуса).
- **textColorShadow**: GuiButton.cpp:128 (REMASTER: тень-прямоугольник со смещением +3,+3; вызов `renderRectFillColor(x+3,y+3,w,h,Color)` — int-перегрузка, альфа используется); GuiCheckBox.cpp:78, 85 (тень «галочки», diagonal lines). Тень текста — не этот цвет (см. 1.3).
- **disabledTextColor**: GuiButton.cpp:195 (`drawText`); GuiValueButton.cpp:105.

---

## 3. Виджеты

### 3.0 Общая база и интерфейсы

- `src/gui/GuiObject.h`:
  - `enum GuiRenderKind` :27-35 (значения — см. 3.0.1).
  - `enum GuiTextAlignHorizontal { LEFT, CENTER }` :37-40.
  - `class GuiTextual` :42-50 (`setTextDrawer`, `setTextAlignHorizontal` (по умолчанию пусто), `setText`).
  - `class GuiClickable` :52-59 (`setEnabled`, `isEnabled`, `set{Left,Right}MouseButtonClickedAction`).
  - `class GuiStatefulVisual` :61-73: `enum class VisualState { Normal, Hover, Pressed, Disabled }`, `setVisualState`, `visualState`.
  - `class GuiObject : cInputObserver` :77-98: `draw()` pure; `hasKeyboardFocus()` по умолчанию false (:81-83); `setTheme`, `setPosition` (`m_rect.move`), `setSize` (`m_rect.resize`) (GuiObject.cpp:30-52); защищённые `m_rect`, `m_theme`, `m_sdlDrawer`, `drawRectBorder`, `drawRectFillBorder`, `auditRecord`, `auditClick`.
- `GuiObject::drawRectBorder` (GuiObject.cpp:54-64): `renderRectColor(m_rect, borderRect)` (outline, альфа не используется) + две линии: `renderLine(x+w, y, x+w, y+h, dark)` и `renderLine(x, y+h, x+w, y+h, dark)` — правая и нижняя линии лежат на пиксель за пределами прямоугольника. Отличается от `SDLDrawer::gui_DrawRectBorder`, который рисует правую/нижнюю линии на `x+w-1`/`y+h-1` (SDLDrawer.cpp:180-198).
- `GuiObject::drawRectFillBorder(theme)` (GuiObject.cpp:66-70): fill `theme.fillColor` (rect-перегрузка, альфа не используется) + `drawRectBorder(borderLight, borderDark)`.

#### 3.0.1 GuiRenderKind (значения и смысл в коде)

| Значение | Смысл (как написано) | Виджеты, которые понимают |
|---|---|---|
| 0 OPAQUE_WITH_BORDER | fill + рамка (+текст) | GuiButton, GuiCheckBox, GuiLabel |
| 1 OPAQUE_WITHOUT_BORDER | только fill (+текст) | GuiButton, GuiCheckBox, GuiLabel |
| 2 TRANSPARENT_WITH_BORDER | только рамка (+текст) | GuiButton, GuiCheckBox, GuiLabel |
| 3 TRANSPARENT_WITHOUT_BORDER | ничего, только текст/галочка | GuiButton, GuiCheckBox, GuiLabel |
| 4 WITH_TEXTURE | `renderSprite(m_tex, x, y)` — нативный размер | GuiButton (GuiButton.cpp:94-96), GuiLabel (GuiLabel.cpp:63-65); GuiCheckBox — `d2tm_assert(false)` (GuiCheckBox.cpp:65-68) |
| 5 WITH_STRETCHED_TEXTURE | `renderStrechFullSprite(m_tex, m_rect, 255)` | GuiButton (cpp:97-99), GuiLabel (cpp:66-68); GuiCheckBox — assert |
| 6 REMASTER_BUTTON | собственная отрисовка «кнопки» с тенью | GuiButton — полностью (cpp:100-150); GuiCheckBox и GuiLabel трактуют как OPAQUE_WITH_BORDER (GuiCheckBox.cpp:56-57; GuiLabel.cpp:53-54) |

- Дефолтный kind: у GuiButton конструктор ставит OPAQUE_WITHOUT_BORDER (GuiButton.cpp:31), но билдер по умолчанию OPAQUE_WITH_BORDER (GuiButton.h:187), и `build()` всегда вызывает `setRenderKind(m_kind)` (GuiButton.h:165). У GuiCheckBox конструктор — OPAQUE_WITHOUT_BORDER (GuiCheckBox.cpp:25), params — OPAQUE_WITH_BORDER (GuiCheckBox.hpp:30). У GuiLabel конструктор — OPAQUE_WITHOUT_BORDER (GuiLabel.cpp:26), params — OPAQUE_WITH_BORDER (GuiLabel.hpp:33).
- Виджеты без GuiRenderKind: GuiSlider, GuiCycleButton, GuiValueButton, GuiStateButton, GuiTextInput, GuiBar, GuiWindow, GuiConsole.
- `nextRenderKind()` (циклы 0→1→2→3→0) есть в GuiButton.cpp:236-250, GuiCheckBox.cpp:117-131, GuiLabel.cpp:111-125; вызовов вне `src/gui` не найдено.

### 3.1 GuiButton (src/gui/GuiButton.h:29-92; GuiButton.cpp)

- Базы: GuiObject, GuiClickable, GuiTextual, GuiStatefulVisual.
- Поля: `m_textDrawer` (h:66; по умолчанию nullptr, cpp:29); `m_buttonText`; `m_renderKind`; `m_textAlignHorizontal`; `m_tex`; `m_focus` (= курсор над прямоугольником); `m_pressed`; `m_enabled`; `m_textScale` (h:79, default 1.0); `m_textOffsetY` (h:80, default 0); `m_visualState` (Normal).
- Флаги в `draw()` (cpp:55-56): `isDisabled = !m_enabled || vs==Disabled`; `isPressed = m_pressed || vs==Pressed`. В `drawText()` (cpp:192): `isHovered = m_focus || vs==Hover`.
- Состояния (draw, cpp:47-152):
  - OPAQUE_WITHOUT_BORDER (cpp:60-63): fill = `isDisabled ? disabledFillColor : fillColor` (int-перегрузка, альфа используется); текст.
  - TRANSPARENT_WITHOUT_BORDER (cpp:64-66): только текст.
  - OPAQUE_WITH_BORDER (cpp:67-80): fill как выше; если `isPressed` → `gui_DrawRectBorder(rect, borderDark, borderLight)` (cpp:70); иначе если не disabled → `(borderLight, borderDark)` (cpp:74); иначе `(disabledBorderLight, disabledBorderDark)` (cpp:76); текст.
  - TRANSPARENT_WITH_BORDER (cpp:81-93): та же логика рамки без fill.
  - WITH_TEXTURE / WITH_STRETCHED_TEXTURE: см. 3.0.1.
  - REMASTER_BUTTON (cpp:100-150):
    - `fillColor = fillColor`; если `enabled && focus` — каждый канал RGB `+18`, max 255 (cpp:105-112);
    - если `m_pressed` — каждый канал RGB `*3/4` (целочисленно), внешняя и внутренняя рамка меняются местами (cpp:113-121);
    - тень: rect (x+3, y+3, w, h) цветом `textColorShadow` (cpp:123-129; int-перегрузка, альфа 220 в Remaster используется);
    - fill rect (cpp:130; rect-перегрузка, альфа не используется);
    - внешняя рамка `renderRectColor(rect, outerBorder)` (cpp:131);
    - внутренняя рамка `renderRectColor(x+1, y+1, w-2, h-2, innerBorder)` (cpp:132-138);
    - линия-подсветка `renderLine(x+4, y+3, x+w-5, y+3, color)`, color = `textColorHover` если `enabled && focus`, иначе `borderLight` (cpp:139-147);
    - текст (cpp:148).
    - REMASTER не читает disabled-поля: disabled выглядит как обычная кнопка, кроме отсутствия hover-подсветки.
- Текст (`drawText`, cpp:189-234):
  - Цвет (cpp:191-196): `isHovered ? textColorHover : textColor`; если `isDisabled` → `disabledTextColor`.
  - `CENTER` (cpp:198-224): `widthScale = max(1, w-16) / max(1, textLength)`; `heightScale = max(1, h-8) / max(1, fontHeight)`; `fitted = clamp(min(textScale, widthScale, heightScale), 0.65, textScale)`; сдвиг `pressedOffset = m_pressed ? 1 : 0`; прямоугольник текста = `(x+p, y+p+textOffsetY, w, h)`; вызов `drawTextScaledOpticallyCenteredInBox(text, textRect, fitted, color)` (тень +2,+2).
  - `LEFT` (cpp:225-232): `drawText(x+1, y+1)` при `m_pressed`, иначе `drawText(x, y)` (тень +1,+1).
  - Выравнивание по умолчанию CENTER: cpp:32, h:189.
  - `setTextScale` — min 0.65 (cpp:181); `setTextOffsetY` (cpp:184-187); `toggleTextAlignHorizontal` (cpp:252-260).
- Прямоугольник нажатия: `m_rect`. Проверка `cRectangle::isPointWithin` включает правый и нижний край (`<= x+width`, `<= y+height`; src/utils/cRectangle.cpp:40-44).
- События (`onNotifyMouseEvent` cpp:262-280):
  - MOVED_TO → `onMouseMovedTo` (cpp:282-294): `m_focus = inside`; visual: `Disabled` если !enabled, `Pressed` если m_pressed, `Hover` если focus, иначе `Normal`.
  - LEFT_PRESSED → `onMouseLeftButtonPressed` (cpp:313-319): если enabled: `m_pressed = m_focus`; visual Pressed / Hover / Normal.
  - LEFT_CLICKED → `onMouseLeftButtonClicked` (cpp:321-332): если вне прямоугольника или disabled — выход; если `m_focus` и есть action → action; затем `m_pressed = false`, visual Hover/Normal.
  - RIGHT_CLICKED → `onMouseRightButtonClicked` (cpp:296-303): если `m_focus && enabled` и есть right-action → вызов.
  - RIGHT_PRESSED: в `switch` (cpp:264-279) обработки нет; `onMouseRightButtonPressed` (cpp:305-311) определён (h:88), но не вызывается.
- Клавиатура: `onNotifyKeyboardEvent` пустой (cpp:391-393).
- Звук: вызовов звука в `src/gui` нет (rg `Sound|sound|Audio|audio|sfx` по `src/gui` — пусто). Звук при нажатии, если есть, задаётся внешним callback-ом.
- `setEnabled(false)`: `m_enabled=false`, visual Disabled, `m_pressed=false` (cpp:344-355). `setVisualState`: Disabled → `m_enabled=false`, `m_pressed=false`, `m_focus=false`; Pressed → `m_pressed=true`, `m_focus=true`; Hover → `m_pressed=false`, `m_focus=true`; Normal → оба false (cpp:362-384).
- Не найдено: проверки `m_textDrawer != nullptr` перед разыменованием в `drawText()` (cpp:201-232).

### 3.2 GuiCheckBox (src/gui/GuiCheckBox.hpp:37-85; GuiCheckBox.cpp)

- Поля: `m_renderKind`, `m_onCheckAction`, `m_onUnCheckAction`, `m_focus`, `m_pressed`, `m_enabled`, `m_checked` (по умолчанию `true`, cpp:31), `m_visualState`.
- Безтекстовый. Галочка — «X» из четырёх линий (renderChecked, cpp:72-102):
  - две линии `textColorShadow`: (x+2, y+3)→(x+w-3, y+h-2) и (x+2, y+h-2)→(x+w-3, y+3);
  - две линии `textColor`: (x+2, y+2)→(x+w-3, y+h-3) и (x+2, y+h-3)→(x+w-3, y+2).
- `draw()` (cpp:40-70):
  - OPAQUE_WITHOUT_BORDER: fill `fillColor` (int-перегрузка, альфа используется) + `drawBox()`;
  - TRANSPARENT_WITHOUT_BORDER: `drawBox()`;
  - REMASTER_BUTTON и OPAQUE_WITH_BORDER: fill + `drawBox()`;
  - TRANSPARENT_WITH_BORDER: `drawRectBorder(light, dark)` + `drawBox()`;
  - WITH_TEXTURE / WITH_STRETCHED_TEXTURE: `d2tm_assert(false)`.
- `drawBox()` (cpp:104-110) **всегда** вызывает `drawRectBorder(borderLight, borderDark)` — то есть рамка рисуется и при OPAQUE_WITHOUT_BORDER/TRANSPARENT_WITHOUT_BORDER. При TRANSPARENT_WITH_BORDER рамка рисуется дважды (cpp:62 и cpp:106). Затем при `m_checked` — `renderChecked()`.
- Состояния: `draw()` не читает `m_enabled`, `m_focus`, `m_pressed`, `m_visualState` — внешний вид не меняется ни при hover, ни при нажатии, ни при disabled. `setVisualState` / `visualState` (cpp:255-282) только меняют поля (Disabled → `m_enabled=false`, `m_pressed=false`, `m_focus=false`; Pressed → `m_pressed=true`, `m_focus=false`; Hover → `m_focus=true`, `m_pressed=false`; Normal → оба false).
- Прямоугольник нажатия: `m_rect` (cpp:164).
- События (cpp:133-160):
  - MOVED_TO → `onMouseMovedTo` (cpp:162-174).
  - LEFT_PRESSED → `onMouseLeftButtonPressed` (cpp:184-190): если enabled && focus → `m_pressed=true`, visual Pressed.
  - RIGHT_PRESSED → `onMouseRightButtonPressed` (cpp:176-182): то же.
  - LEFT_CLICKED → `onMouseLeftButtonClicked` (cpp:192-216): требует `m_focus && m_enabled`; если `m_checked` → `m_checked=false`, вызов `onUnCheck`; иначе `m_checked=true`, вызов `onCheck`; затем left-action (если задан); `m_pressed=false`; visual Hover/Normal.
  - RIGHT_CLICKED (cpp:142-150): если focus — right-action (если enabled); `m_pressed=false`; visual Hover/Normal.
- Клавиатура: пусто (cpp:290-291). Звук: нет.
- Методы: `setChecked(bool)` (cpp:284-287) — без callback; `setCheckAction` / `setUnCheckAction` (cpp:218-226).

### 3.3 GuiSlider (src/gui/GuiSlider.hpp:34-71; GuiSlider.cpp)

- Поля: `m_minValue`, `m_maxValue`, `m_value` (clamp при создании, cpp:28), `m_dragging`, `m_leftButtonHeld` (false), `m_enabled` (true), `m_visualState`, `m_onValueChanged`, left/right actions.
- Конструктор по умолчанию: min 0, max 100, initial 0 (hpp:36).
- Геометрия: ширина ручки `GUI_KNOB_WIDTH = 12` (cpp:22). Трек = весь `m_rect`. Ручка: `knobX = x + int(t * (w - 12))`, `t = (value - min) / (max - min)` (cpp:89-92); прямоугольник ручки `(knobX, y, 12, h)` (cpp:95).
- `draw()` (cpp:75-82): `recordGui("GuiSlider")` + `recordClick("GuiSlider")` (только при `uiaudit::isEnabled()`); затем `drawTrack()` и `drawKnob()`.
- `drawTrack()` (cpp:84-87): `renderRectFillColor(m_rect, fillColor)` (rect-перегрузка, альфа не используется) + `drawRectBorder(borderLight, borderDark)`.
- `drawKnob()` (cpp:89-98): `renderRectFillColor(knobRect, borderDark)` + `gui_DrawRectBorder(knobRect, borderLight, borderDark)`.
- Состояния: `draw()` не читает `m_enabled` и `m_visualState` — внешний вид не меняется. `setEnabled(false)` → `m_dragging=false`, `m_leftButtonHeld=false`, visual Disabled (cpp:34-44). `setVisualState(Disabled)` → `m_enabled=false`, `m_dragging=false` (cpp:61-68).
- Мышь (`onNotifyMouseEvent`, cpp:118-165; если `!m_enabled` — выход):
  - LEFT_PRESSED: если `m_leftButtonHeld` — выход (PRESSED приходит каждый кадр); иначе `m_leftButtonHeld=true`; если внутри `m_rect` → `m_dragging=true`, visual Pressed, `updateValueFromMouse(x)`.
  - LEFT_CLICKED: если внутри и есть action → action; `m_dragging=false`, `m_leftButtonHeld=false`, visual Normal.
  - LEFT_DOUBLE_CLICKED: сброс `m_dragging`, `m_leftButtonHeld`, visual Normal (без action).
  - RIGHT_CLICKED: если внутри и есть right-action → вызов; `m_dragging=false`; visual Normal.
  - MOVED_TO: если `m_dragging` → `updateValueFromMouse(x)`.
- `updateValueFromMouse(mouseX)` (cpp:167-176): `pos = mouseX - x`; `norm = clamp(pos / w, 0, 1)` (делитель — **w**, не `w-12`); `value = int(min + norm * (max - min))` (усечение); вызов `setValue` (cpp:100-108; callback только при изменении значения).
  - Расхождение: отрисовка ручки использует `(w - 12)` (cpp:92), пересчёт мышью использует `w` (cpp:169).
- Клавиатура: пусто (cpp:179-180). Звук: нет.

### 3.4 GuiLabel (src/gui/GuiLabel.hpp:40-79; GuiLabel.cpp)

- Поля: `m_textDrawer` (nullptr по умолчанию, cpp:24), `m_buttonText`, `m_renderKind`, `m_textAlignHorizontal` (CENTER), `m_tex`, `m_focus`, `m_enabled` (true).
- `draw()` (cpp:38-70): если `!m_enabled` — ничего не рисуется (cpp:40-41); затем `recordGui("GuiLabel")` (при uiaudit); по kind:
  - OPAQUE_WITHOUT_BORDER: fill `fillColor` (int-перегрузка, альфа используется) + текст;
  - TRANSPARENT_WITHOUT_BORDER: текст;
  - REMASTER_BUTTON / OPAQUE_WITH_BORDER: fill + `drawRectBorder(light, dark)` + текст;
  - TRANSPARENT_WITH_BORDER: `drawRectBorder` + текст;
  - WITH_TEXTURE / WITH_STRETCHED_TEXTURE: спрайт, без текста.
- Текст (`drawText`, cpp:97-109): цвет **всегда** `textColor` (cpp:99), без hover/disabled.
  - CENTER: `drawTextCenteredInBox(text, m_rect, textColor)` (cpp:103) — по TTF-размеру; тень +1,+1.
  - LEFT: `drawText(x, y, textColor, text)` (cpp:106).
  - `m_textDrawer` не проверяется (cpp:97-109).
- `m_focus` выставляется в `onMouseMovedTo` (cpp:148-151), но в `draw()` не используется.
- Мышь: только MOVED_TO (cpp:137-146). Клавиатура: пусто (cpp:158-159). `setEnabled(bool)` (cpp:153-156) не наследуется от GuiClickable — метод без `override`. Звук: нет.

### 3.5 GuiWindow (src/gui/GuiWindow.h:26-52; GuiWindow.cpp)

- Наследует `protected GuiObject`. Не имеет состояний и кликов.
- `draw()` (cpp:37-51): `recordGui("GuiWindow")` (при uiaudit); `drawRectFillBorder(m_theme)` (fill rect-перегрузкой, альфа не используется; рамка light/dark); затем все дочерние `draw()` по порядку вставки (cpp:44-46); затем заголовок, если `title` не пуст: `drawTextCentered(title, x, width, y+2, Color::Yellow)` (cpp:50). Цвет заголовка жёстко `Color::Yellow` (255,207,41,255), не из темы.
- `setTitle` (h:42-44); `setTheme` (h:45-47) меняет тему **только окна** (не дочерних).
- Мышь (cpp:59-64): всем дочерним без проверки попадания. Клавиатура (cpp:71-78): только `PRESSED`, всем дочерним.
- `hasFocusedInput()` (cpp:80-89): true, если хотя бы один дочерний `hasKeyboardFocus()` (true только у GuiTextInput с `m_focused`).
- `getRelativeRect(x,y,w,h)` = `(x + rect.x, y + rect.y, w, h)` (cpp:66-69).
- Конструктор требует `textDrawer != nullptr` (cpp:28-29).
- Звук: нет.

### 3.6 GuiBar (src/gui/GuiBar.h:30-58; GuiBar.cpp)

- `enum class GuiBarPlacement : char { HORIZONTAL=0, VERTICAL=1 }` (h:25-28).
- Конструктор: `GuiBar(drawer, rect, placement, int iconSize=40)` (h:32); в cpp параметр назван `heightBarSize`.
- Отступ: `halfMarginBetweenButtons = (rect.h - iconSize) / 2` для HORIZONTAL, `(rect.w - iconSize)/2` для VERTICAL (cpp:25-29; целочисленное деление).
- `addAutoGuiObject(obj)` (cpp:57-71):
  - HORIZONTAL: `x = placementPosition`, `y = halfMargin` (без `rect.x/rect.y`); `placementPosition += iconSize + 2*halfMargin` (cpp:60-63);
  - VERTICAL: `x = rect.x + halfMargin`, `y = rect.y + placementPosition`; `placementPosition += iconSize + 2*halfMargin` (cpp:64-67).
  - Затем `obj->setPosition(x, y)` (cpp:69). Так что координаты HORIZONTAL — относительные, VERTICAL — абсолютные.
- `addGuiObject(obj)` (cpp:52-55) — без позиционирования; `beginPlacement(int)` (h:49-51) сбрасывает `placementPosition`.
- `draw()` (cpp:40-50): `drawRectFillBorder(m_theme)` и затем дочерние `draw()`. Состояний нет.
- Мышь (cpp:73-80): дочерним только если `coords.isWithinRectangle(&m_rect)`. Клавиатура (cpp:87-92): всем дочерним.
- `getRelativeRect` (cpp:82-85) — как у GuiWindow. `setTheme` (h:45-47).
- Звук: нет.

### 3.7 GuiButtonGroup (src/gui/GuiButtonGroup.h:20-30; GuiButtonGroup.cpp)

- Не виджет: вектор `GuiStateButton*` и `m_currentlySelected` (h:28-29).
- `add(btn)` (cpp:42-45).
- `updateStates(clicked)` (cpp:19-31): если `clicked == nullptr` или уже выбран → выход; у прежнего `setPressed(false)`; у нового `setPressed(true)`; `m_currentlySelected = clicked`.
- `updateState(index)` (cpp:33-40): проверка границ, затем `updateStates(members[index])`.
- `isCurrentlySelected(btn)` (cpp:47-50).
- Отрисовки и событий нет. Файл `GuiButtonGroup.h` **не содержит** `#pragma once` (проверено `rg`).

### 3.8 GuiStateButton (src/gui/GuiStateButton.h:37-67; GuiStateButton.cpp)

- Спрайтовая кнопка: одна текстура `m_tex` (setTexture, cpp:40-43), три ячейки внутри неё (`rectState`, cpp:24-26), размер 32×32 в координатах текстуры:
  - UNCLICKED `(0,0,32,32)` (cpp:24);
  - DISABLED `(32,0,32,32)` (cpp:25);
  - CLICKED `(64,0,32,32)` (cpp:26).
  - Начальное состояние UNCLICKED (cpp:23).
- `draw()` (cpp:66-69): `renderStrechSprite(m_tex, текущая_ячейка, m_rect)` — растягивание в `m_rect`. Тема не читается; текста и рамки нет.
- Смена состояния `changeState` (cpp:45-64).
- Мышь (cpp:71-91): проверка `coords.isWithinRectangle(&m_rect)`.
  - LEFT_CLICKED с группой: если уже выбран и есть action → action и выход; иначе `group->updateStates(this)` (внутри `setPressed(true)` → action при переходе в CLICKED).
  - LEFT_CLICKED без группы: `setPressed(true)`.
  - RIGHT_CLICKED: right-action (состояние не меняется).
- `setPressed(true)` (cpp:93-109): если enabled и состояние не CLICKED → CLICKED и вызов left-action. `setPressed(false)` → UNCLICKED (cpp:106-108).
- `setEnabled` (cpp:111-122): false → DISABLED ячейка, visual Disabled; true → UNCLICKED, visual Normal.
- `setVisualState` (cpp:129-149): Disabled → `m_enabled=false`, DISABLED; Pressed → CLICKED (только если enabled, без action); Hover/Normal → UNCLICKED (если enabled).
- Клавиатура (cpp:156-166): только `PRESSED` и только при группе: `getGroupNumber() = n > 0` → `group->updateState(n-1)`.
- `setGroup(g)` (cpp:34-38): `m_group = g; g->add(this)`.
- Hover-состояния нет. Звук: нет.
- Файл `GuiStateButton.h` **не содержит** `#pragma once` (проверено `rg`).

### 3.9 GuiCycleButton (src/gui/GuiCycleButton.h:27-59; GuiCycleButton.cpp)

- Список `std::vector<int> m_values`, индекс `m_currentIndex` (0 по умолчанию, cpp:21).
- Текст: если `m_textDrawer != nullptr` и список не пуст — `label = m_displayText` или `to_string(value)` (cpp:74); `drawText(x+5, y+3, textColor, label)` (cpp:75; тень по умолчанию). Выравнивания нет (фикс. смещение).
- `draw()` (cpp:69-77): `drawRectFillBorder(m_theme)` (fill rect-перегрузкой, альфа не используется; рамка light/dark), затем текст.
- Состояний нет. `m_enabled` влияет только на клики (cpp:48).
- Клики (cpp:46-63): если disabled или точка вне `m_rect.isPointWithin(x, y)` — выход. LEFT_CLICKED → `nextValue()` (индекс +1 по модулю, `m_displayText = to_string`, вызов `m_onChanged(value)` если задан, cpp:80-86) и затем left-action. RIGHT_CLICKED → `previousValue()` (аналогично, cpp:88-94) и right-action.
- Клавиатура: пусто (cpp:66-67). Звук: нет.
- `setText(text)` (h:42) задаёт `m_displayText` до первого клика.
- Прямоугольник нажатия: `m_rect`.

### 3.10 GuiValueButton (src/gui/GuiValueButton.h:28-71; GuiValueButton.cpp)

- Поля: `m_value`, `m_stepValue` (`max(1, step)`, cpp:27), `m_minValue = min(min,max)`, `m_maxValue = max(min,max)` (cpp:28-29); `m_label`; `m_texture`; `m_focus`; `m_pressed`; `m_enabled`; `m_visualState`.
- `draw()` (cpp:93-124):
  - `renderRectFillColor(m_rect, fillColor)` (rect-перегрузка, альфа не используется);
  - рамка: если `m_visualState == Pressed` → `gui_DrawRectBorder(rect, borderDark, borderLight)`, иначе `(borderLight, borderDark)` (cpp:95-100);
  - если `m_textDrawer != nullptr`: цвет = `m_focus ? textColorHover : textColor`, `!m_enabled` → `disabledTextColor` (cpp:102-106);
    - если есть `m_label` или `m_texture`: верхняя половина `topHeight = h/2`, нижняя `h - topHeight`; верх — текстура `renderStrechFullSprite(m_texture, topRect)` (альфа 255) либо `drawTextCenteredInBox(m_label, topRect, color)`; низ — `drawTextCenteredInBox(to_string(value), bottomRect, color)` (cpp:107-120);
    - иначе — `drawTextCenteredInBox(to_string(value), rect, color)` (cpp:122).
- Мышь (cpp:35-87; при `!m_enabled` — выход):
  - MOVED_TO: `m_focus = inside`; если не focus → `m_pressed=false`; visual Disabled/Pressed/Hover/Normal (cpp:42-56);
  - LEFT_PRESSED / RIGHT_PRESSED: `m_pressed = inside`; если pressed → visual Pressed (cpp:57-63);
  - LEFT_CLICKED: если внутри → `increaseValue()` (value + step, clamp) и left-action; `m_pressed=false`; visual Hover/Normal (cpp:64-73);
  - RIGHT_CLICKED: если внутри → `decreaseValue()` и right-action; то же сброс (cpp:74-83).
- `updateValue(v)` (cpp:222-233): clamp, при изменении вызывает `m_onChanged`.
- Клавиатура: пусто (cpp:89-91). Звук: нет.
- Используется только в cEditorState (см. раздел 4).

### 3.11 GuiTextInput (src/gui/GuiTextInput.h:26-50; GuiTextInput.cpp)

- Константы (cpp:24-27): `kHorizontalPadding = 4`, `kSecurityPadding = 5`, `kCursorBlinkHalfPeriodMs = 500`.
- Поля: `m_text`, `m_writer` (cTextDrawer, обязателен — assert cpp:48-49), `m_focused` (false), `m_onEnter`.
- `draw()` (cpp:52-61):
  - fill `m_theme.background` (rect-перегрузка, альфа не используется); рамок нет;
  - если `m_focused`: контур `(x-3, y-3, w+6, h+6)` цветом `textColorHover` через `renderRectColor(rect, color)` (cpp:55-58);
  - текст: `drawText(x+4, y+4, textColor, getFittedDisplayText())` (cpp:60; тень +1,+1). Y фиксирован (+4), не центрируется.
- `getFittedDisplayText()` (cpp:113-129): `display = text`; если `m_focused && курсор видим` → добавляется `'|'` (курсор видим, если `(SDL_GetTicks()/500) % 2 == 0`, cpp:29-31, 116-118); затем пока ширина > максимума — удаляется **первый** символ (прокрутка влево, cpp:124-126).
- Максимальная ширина: `max(0, w - 2*4 - 5)` = `w - 13` (cpp:95).
- Ввод (`onNotifyKeyboardEvent`, cpp:63-78; только если `m_focused`):
  - `hasTextInput()` → `canAppendText(input)` (cpp:98-111): кандидат = `text + input` (+ `'|'` если focused) должен влезать в максимум, иначе не добавляется;
  - `isBackspace()` → удаление последнего UTF-8 кодпоинта (cpp:33-42, 74);
  - `isEnter()` → `m_onEnter(m_text)` (текст не очищается, cpp:75-76).
- `setText(text)` (cpp:80-91): задаёт текст и обрезает **с конца**, пока ширина > максимума (без многоточия).
- `hasKeyboardFocus()` = `m_focused` (h:33).
- Мышь (cpp:131-139): только `MOUSE_LEFT_BUTTON_CLICKED`; `m_focused = inside`.
- Визуальных состояний (hover/pressed/disabled) нет. Звук: нет.

### 3.12 GuiConsole (src/gui/GuiConsole.h:30-54; GuiConsole.cpp) — не GuiObject

- Состав: `m_window` (GuiWindow), `m_input` (GuiTextInput, указатель внутри окна), `m_messageParser` (GuiConsoleMessageParser), `m_visible` (false).
- Геометрия (cpp:32-36): `width = max(260, min(520, screenW - 16))`; `inputHeight = fontHeight + 4`; `height = inputHeight + 8`; `x = 8`; `y = screenH - height - 10`.
- Окно: `GuiWindow(sdlDrawer, rect(x,y,width,height), textDrawer)` (cpp:38). **`setTheme` для окна не вызывается** (cpp:38-52), значит тема окна — `GuiTheme` по умолчанию (все Color = 0,0,0,255).
- Поле ввода: `GuiTextInputBuilder` с rect `window.getRelativeRect(8, 6, width-16, inputHeight)` (cpp:42), тема `light()` (cpp:45), `onEnter → submit` (cpp:46-48). Затем `addGuiObject` (cpp:52).
- `toggle()` (cpp:57-63): инвертирует `m_visible`, выставляет фокус полю ввода. `isKeyboardCaptured()` (cpp:70-73) = `visible && window.hasFocusedInput()`.
- `draw()` (cpp:75-82): только если видно. Клавиатура и мышь (cpp:84-100): пропускаются, если не видно.
- `submit(text)` (cpp:102-111): `parser.submit(text)`, затем `input.setText("")`.
- Вызовы из `cGame`: `cGame_logic.cpp:565` (`draw`), `:133` (`isKeyboardCaptured`), `:1433-1434` (мышь при видимости), `:1448` (`toggle`, при `isConsoleToggleKey(event)`), `:1453-1459` (клавиатура).
- Парсер (`src/gui/GuiConsole/GuiConsoleMessageParser.cpp`):
  - `normalize` = trim + lower (cpp:59-62, 26-50);
  - `submit` (cpp:64-89): пустая строка → выход; `verifyOddWordCommand` (нечётное число слов, cpp:104-119) иначе уведомление `"Malformed command: {text}"` BAD (cpp:72);
  - `parseCommand` (cpp:92-102): первое слово → `m_command`, далее пары `key value` → `m_arguments`;
  - `"help"` → уведомление `"Help mode."` NEUTRAL (cpp:83-86); иначе `"> {normalized}"` NEUTRAL (cpp:88).
  - Уведомления: `cNotificationArea::addNotification` (cpp:72, 84, 88).

---

## 4. Кто создаёт виджеты (по всему src/)

Все вхождения — `GuiXBuilder()` или `make_unique<GuiX>` вне `src/gui/`.

- **GuiButton** (через `GuiButtonBuilder`):
  - src/gamestates/cSelectMissionState.cpp:111, 130, 155;
  - src/gamestates/cMainMenuState.cpp:141, 181;
  - src/gamestates/cOptionsState.cpp:121, 135, 150, 165, 177, 191, 390, 414, 438, 462, 501, 527;
  - src/gamestates/cNewmapEditorState.cpp:249, 266;
  - src/gamestates/cEditorState.cpp:151;
  - src/gamestates/cSetupSkirmishState.cpp:258, 268, 321, 341, 358, 374, 388;
  - src/gamestates/cSelectYourNextConquestState.cpp:164;
  - src/gamestates/cCreditsState.cpp:86;
  - src/gameobjects/mentat/AbstractMentat.cpp:87 (`gui_btn_toMissionSelect`);
  - src/gameobjects/mentat/AtreidesMentat.cpp:36, 45; BeneMentat.cpp:43, 52; HarkonnenMentat.cpp:35, 44; OrdosMentat.cpp:34, 43; SardaukarMentat.cpp:35, 44 (left/right кнопки).
  - Хранение: `std::unique_ptr<GuiButton>` в cCreditsState.h:75, cSetupSkirmishState.h:150-156, cSelectYourNextConquestState.h:154, AbstractMentat.h:115-123.
- **GuiCheckBox** (`GuiCheckBoxBuilder`): src/gamestates/cOptionsState.cpp:231, 282, 363, 486; src/gamestates/cNewmapEditorState.cpp:210.
- **GuiSlider** (`GuiSliderBuilder`): src/gamestates/cOptionsState.cpp:257, 308, 335.
- **GuiLabel** (`GuiLabelBuilder`):
  - src/gamestates/cOptionsState.cpp:207, 220, 246, 271, 297, 322, 351, 378, 402, 426, 450, 474, 514;
  - src/gamestates/cNewmapEditorState.cpp:93, 112, 131, 150, 175, 200, 228.
- **GuiWindow** (`make_unique<GuiWindow>`): src/gamestates/cSelectMissionState.cpp:85; cMainMenuState.cpp:129 (хранится `gui_window`, cMainMenuState.h:68); cOptionsState.cpp:113 (`m_guiWindow`, cOptionsState.h:71); cNewmapEditorState.cpp:81 (`m_guiWindow`, cNewMapEditorState.h:60); src/gui/GuiConsole.cpp:38.
- **GuiTextInput** (`make_unique<GuiTextInput>` / builder): src/gamestates/cNewmapEditorState.cpp:103, 122, 141, 238; src/gui/GuiConsole.cpp:41-49 (через builder).
- **GuiCycleButton** (`GuiCycleButtonBuilder`): src/gamestates/cNewmapEditorState.cpp:160, 185.
- **GuiValueButton** (`GuiValueButtonBuilder`): src/gamestates/cEditorState.cpp:236.
- **GuiStateButton** (`GuiStateButtonBuilder`): src/gamestates/cEditorState.cpp:115, 127, 138, 169, 180, 191, 202, 214, 225, 257, 269, 280, 291, 302, 318, 330, 342, 354, 366, 377, 388, 399.
- **GuiBar** (`make_unique<GuiBar>`): src/gamestates/cEditorState.cpp:85-88 (`m_selectBar`, `m_topologyBar`, `m_startCellBar`, `m_symmetricBar`; cEditorState.h:99-103).
- **GuiButtonGroup** (`make_unique<GuiButtonGroup>`): src/gamestates/cEditorState.cpp:113, 167, 255, 316 (cEditorState.h:105-108).
- **GuiConsole** (`make_unique<GuiConsole>`): src/game/cGame_logic.cpp:814; хранится `cGame.h:219` (`m_guiConsole`).
- **GuiConsoleMessageParser**: создаётся в GuiConsole.cpp:39.
- **cTextWriter**: src/drawers/cMouseDrawer.cpp:45 (`make_unique<cTextWriter>(textDrawer, 12)`), хранится cMouseDrawer.h:59.
- **GuiTheme**: см. раздел 2 (места использования `Remaster`/`RemasterInactive`/`light()`).

---

## 5. Примитивы рисования: SDLDrawer

Заголовок `src/drawers/SDLDrawer.hpp`; реализация `src/drawers/SDLDrawer.cpp`. Альфа-модуляции текстур — `SDL_SetTextureAlphaMod` (SDLDrawer.cpp:43, 55, 74, 83, 97). Оттенка (`SDL_SetTextureColorMod`) в `src/` **не найдено** (rg `ColorMod` — пусто). Градиенты **не найдены** (rg `Gradient|gradient` — только комментарий src/gameobjects/units/cPathFinder.cpp:503).

- h:33 `renderSprite(Texture* src, int x, int y, Uint8 opacity=255)` — нативный размер текстуры, альфа = opacity, BLEND (cpp:37-47).
- h:34 `renderStrechSprite(Texture* src, cRectangle src_pos, cRectangle dest_pos, Uint8 opacity=255)` — под-прямоугольник источника, умножается на `src->density` (cpp:79-91).
- h:35 `renderStrechFullSprite(Texture* src, cRectangle dest_pos, Uint8 opacity=255)` — вся текстура в dest (cpp:93-100).
- h:36 `renderFromSurface(SDL_Surface* src, int x, int y, Uint8 opacity=255, int density=1)` — color-key магента (255,0,255), создаёт временную текстуру на каждый вызов, уничтожает её (cpp:61-77); scale LINEAR при density>1, иначе NEAREST.
- h:37 `renderTexture(SDL_Texture* tex, int x, int y, int w, int h, Uint8 opacity=255)` — растяжение до w×h, альфа (cpp:49-59).
- h:39 `renderRectFillColor(int x, int y, int w, int h, Uint8 r, Uint8 g, Uint8 b, unsigned char opacity=255)` — `SDL_RenderFillRect` (cpp:102-108).
- h:40 `renderRectFillColor(int x, int y, int w, int h, Color color)` — альфа = `color.a` (cpp:110-113).
- h:41 `renderRectFillColor(const cRectangle& rect, Color color, Uint8 opacity=255)` — альфа = параметр `opacity`, **`color.a` игнорируется** (cpp:123-127).
- h:42 `renderRectColor(int x, int y, int w, int h, Uint8 r, Uint8 g, Uint8 b, unsigned char opacity=255)` — контур `SDL_RenderRect` (cpp:115-119).
- h:43 `renderRectColor(int x, int y, int w, int h, Color color)` — альфа = `color.a` (cpp:134-137).
- h:44 `renderRectColor(const cRectangle& rect, Uint8 r, Uint8 g, Uint8 b, unsigned char opacity=255)` (cpp:129-132).
- h:45 `renderRectColor(const cRectangle& rect, Color color, unsigned char opacity=255)` — **`color.a` игнорируется** (cpp:139-143).
- h:47 `resetClippingFor()` — `SDL_SetRenderClipRect(nullptr)` (cpp:145-148).
- h:48 `setClippingFor(int topLeftX, int topLeftY, int bottomRightX, int bottomRightY)` — принимает правый нижний угол, переводит в ширину/высоту (cpp:150-154).
- h:50 `setPixel(SDL_Surface* bmp, int x, int y, Color color)` (cpp:288).
- h:51 `renderClearToColor(Color color = {0,0,0,255})` — `SDL_RenderClear` (cpp:200-204).
- h:53 `gui_DrawRect(const cRectangle&, Color fill, Color borderLight, Color borderDark)` — fill + контур light + тёмные правая/нижняя линии на `x+w-1`/`y+h-1` (cpp:156-178).
- h:54 `gui_DrawRectBorder(const cRectangle&, Color borderLight, Color borderDark)` — контур light, тёмные правая/нижняя линии (cpp:180-198). Альфа цветов передаётся через `renderChangeColor`.
- h:56 `renderLine(int x1, int y1, int x2, int y2, Color color)` — `renderChangeColor` (SDL draw color с альфой) + `SDL_RenderLine` (cpp:206-210).
- h:57 `renderDot(int x, int y, Color color, int size)` — size==1: точка; иначе квадрат size×size точек (cpp:212-228).
- h:59 `isSurface8BitPaletted(SDL_Surface*)` (cpp:230).
- h:61 `FillWithColor(SDL_Surface*, Color)` (cpp:273).
- h:63-65 `getRenderer()` — inline, возвращает `SDL_Renderer*`.
- h:67 `createRenderTargetTexture(int w, int h, int density=1)` — `SDL_TEXTUREACCESS_TARGET`, RGBA8888, размер `w*d × h*d`, при ошибке `throw` (cpp:309-328).
- h:68 `setFrameDensity(int)` / h:69 `getFrameDensity() const` (cpp:330-338).
- h:70 `beginDrawingToTexture(Texture*)` — push текущей цели в стек, `SDL_SetRenderTarget` (cpp:342-353); `throw` при ошибке.
- h:71 `endDrawingToTexture()` — pop и восстановление цели (cpp:354-364); `throw` при пустом стеке.
- h:72 `createTextureFromIndexedSurfaceWithPalette(SDL_Surface*, int paletteIndexForTransparency, const HouseColors&, int assetDensity=1)` — тело (cpp:366) не разбирал.
- Приватные: `set_pixel` (h:74), `renderChangeColor(Color)` (h:79; cpp:303-306 — `SDL_SetRenderDrawColor` с альфой).
- Режимы масштабирования текстур: NEAREST, LINEAR при density>1 (cpp:72, 320, 377, 459).
- Blend: в большинстве примитивов ставится `SDL_BLENDMODE_BLEND` (cpp:41-42, 101-108, 116-118).
- Отсечение: `setClippingFor` / `resetClippingFor` — вызовы вне `src/gui` не разбирались (не найдено в просмотренных файлах).

### 5.1 HdUiTextureLoader (src/utils/HdUiTextureLoader.cpp:11-31; .hpp:8)

- `loadHdUiTexture(renderer, fileName, logContext="HD UI")`: путь `"data" / "hd4" / fileName` (cpp:13); `IMG_Load` → `SDL_CreateTextureFromSurface`; `SDL_SetTextureBlendMode(BLEND)` (cpp:19); `SDL_SetTextureScaleMode(LINEAR)` (cpp:20); `new Texture(tex, w, h, false, kHd4AssetDensity)` (cpp:21); `kHd4AssetDensity = 4` (src/utils/Graphics.hpp:64). При ошибке — `Logger::warn` и `nullptr` (cpp:29-30).
- Вызовы (файл → имя файла):
  - src/gamestates/cCreditsState.cpp:53-59 — `credits_team.png`, `credits_title.png`;
  - src/gamestates/cChooseHouseState.cpp:61-63 — `main_menu_background.png`;
  - src/gamestates/cMainMenuState.cpp:91-98 — `main_menu_background.png`, `main_menu_logo.png`;
  - src/gamestates/cSelectMissionState.cpp:74-76 — `main_menu_background.png`;
  - src/gamestates/cSelectYourNextConquestState.cpp:123-130 — `main_menu_background.png`, `campaign_map.png`; :149 — `houseCrestFile` (имя не захвачено);
  - src/drawers/cSideBarDrawer.cpp:56-68 — `hud_house_atreides.png`, `hud_house_harkonnen.png`, `hud_house_ordos.png`;
  - src/gamestates/cWinLoseState.cpp:60 — `outcomeFile` (имя не захвачено).

---

## 6. Вызовы uiaudit:: и аудит-записи

Файлы из задания. `uiaudit::` в них — только в перечисленных строках. Реализация записей: `src/debug/UiAuditCapture.cpp:190-222` (`recordText` берёт явный box или верхний из стека `g_boxes`; `recordGui`/`recordClick` — записи с типом Gui/Click; `BoxScope` — push/pop бокса в стек). Флаг: `src/debug/UiAuditArguments.hpp:19-22` (`isEnabled()` = `g_enabled`). Заголовок: `src/debug/UiAudit.hpp:11-31`.

- src/drawers/cTextDrawer.cpp:17 — include `debug/UiAudit.hpp`.
- src/drawers/cTextDrawer.cpp:51-53 — `drawText(color)`: `recordText(msg, x, y, cacheEntry->width, cacheEntry->height)` (Text; box — верхний из стека, если есть).
- src/drawers/cTextDrawer.cpp:97-101 — `drawTextCenteredInBox(x,y,boxW,boxH)`: `BoxScope(x, y, boxW, boxH)` (push на время вызова drawText).
- src/drawers/cTextDrawer.cpp:129-132 — `drawTextScaledCenteredInBox`: `recordText(msg, x, y, width, height, &box)` с box = rect.
- src/drawers/cTextDrawer.cpp:158-161 — `drawTextScaledOpticallyCenteredInBox`: `recordText(msg, origin.x, origin.y, width, height, &box)`.
- src/drawers/cTextDrawer.cpp:182-185 — `drawTextCentered(x,width,y,color)`: `BoxScope(x, y, width, getFontHeight())`.
- src/gui/GuiObject.cpp:35-43 — `auditRecord(type)` → `recordGui(type, rect)`; `auditClick(name)` → `recordClick(name, rect)` (объявлены GuiObject.h:96-97).
- src/gui/GuiWindow.cpp:39-41 — `auditRecord("GuiWindow")` при `isEnabled()`.
- src/gui/GuiLabel.cpp:42-44 — `auditRecord("GuiLabel")` при `isEnabled()`, после early return при `!m_enabled` (cpp:40-41).
- src/gui/GuiSlider.cpp:76-79 — `auditRecord("GuiSlider")` и `auditClick("GuiSlider")` при `isEnabled()`, без проверки enabled.
- src/gui/GuiButton.cpp:49-54 — `auditRecord("GuiButton")`; если `m_enabled` и есть любой click-action → `auditClick("GuiButton:" + m_buttonText)`.
- src/gui/GuiCheckBox.cpp:42-47 — `auditRecord("GuiCheckBox")`; если `m_enabled` → `auditClick("GuiCheckBox")`.
- Не найдено `uiaudit::`/`auditRecord`/`auditClick` в: GuiValueButton, GuiCycleButton, GuiStateButton, GuiTextInput, GuiBar, GuiButtonGroup, GuiConsole, GuiConsoleMessageParser, cTextWriter, cTextTextureCache, ContextCreator, TextContext, HdUiTextureLoader, SDLDrawer (rg по `src/gui`, `src/drawers`, `src/context`, `src/utils`).
- Вне перечисленных файлов (справочно): `src/main.cpp`, `src/game/cSDLSystem.cpp`, `src/game/cGame_logic.cpp` тоже содержат `uiaudit::`; их не разбирал.

---

## 7. Не найдено, неопределённости, расхождения (только факты)

- Не найдено: звук в виджетах; перенос строк; градиенты; оттенок текстуры (ColorMod); вызовы `dark()`/`inactive()`; чтение `textDarkColor`; `#pragma once` в `GuiButtonGroup.h` и `GuiStateButton.h`; проверка `m_textDrawer` в `GuiButton::drawText`, `GuiLabel::drawText`.
- Не разбирал: тело `createTextureFromIndexedSurfaceWithPalette` (SDLDrawer.cpp:366); тело `UiAuditCapture` сверх перечисленного; тип `ContextCreator.hpp` (поля шрифтов); файлы шрифтов в `data/` (их наличие и формат `.fon` не проверял); точные имена файлов в cWinLoseState.cpp:60 и cSelectYourNextConquestState.cpp:149; вызов `GuiStateButton` в cEditorState не разбирал поштучно.
- Тень текста: `drawText*` рисует тень `Color::Black` (cTextTextureCache.cpp:99), поле `textColorShadow` используется только в GuiButton (REMASTER) и GuiCheckBox.
- Путь утечки: при неудаче второй `TTF_RenderText_Solid` в `createCacheEntry` первая текстура тени не уничтожается (cTextTextureCache.cpp:104-111).
- Null-разыменование: `drawTextScaled*` не проверяют `findOrCreate` на nullptr (cTextDrawer.cpp:123-124, 148-149).
- Альфа в примитивах: перегрузки `renderRectFillColor(rect, Color)` (SDLDrawer.cpp:123) и `renderRectColor(rect, Color)` (SDLDrawer.cpp:139) игнорируют `Color.a`; перегрузки `(x,y,w,h,Color)` (SDLDrawer.cpp:110, 134) используют. В результате `fillColor` с alpha 238 (Remaster) у GuiButton OPAQUE_* применяется с альфой, у GuiButton REMASTER/GuiWindow/GuiBar/GuiCycleButton/GuiValueButton/GuiSlider — без неё.
- GuiCheckBox: `drawBox()` всегда рисует рамку, поэтому kind OPAQUE_WITHOUT_BORDER и TRANSPARENT_WITHOUT_BORDER тоже рисуют рамку (GuiCheckBox.cpp:104-110); при TRANSPARENT_WITH_BORDER рамка рисуется дважды (cpp:61-63).
- GuiConsole: тема окна не задана, окно рисуется цветами `Color()` = чёрные (GuiConsole.cpp:38; GuiTheme.hpp:22-37; Color.hpp:24-25).
- GuiSlider: делитель при расчёте значения мышью `w`, при отрисовке ручки `w-12` (GuiSlider.cpp:169 и :92).
- GuiBar: `addAutoGuiObject` для HORIZONTAL позиционирует без `rect.x/rect.y` (GuiBar.cpp:61-62), для VERTICAL — с ними (cpp:65-66).
- GuiButton: `onMouseRightButtonPressed` определён (GuiButton.cpp:305-311), но в `onNotifyMouseEvent` не вызывается (cpp:262-280).
- Регистр имён: в `src/gamestates` встречаются `cNewMapEditorState.h` (cNewMapEditorState.h:30, :60) и `cNewmapEditorState.cpp` (cNewmapEditorState.cpp:21-81) — различается регистр букв; не проверял, один ли это файл.
- `cTextDrawer::drawTextBottomLeft` использует высоту строки `h`, `drawTextBottomRight` — `getFontHeight()` (cTextDrawer.cpp:206 и :220); разные метрики.

---

## Расход

Примерно 250 тыс. токенов по счётчику total_tokens (15 000 000 → 14 745 707). Точнее не оценить: часть — чтение больших файлов целиком.
