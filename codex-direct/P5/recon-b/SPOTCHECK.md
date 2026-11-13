# Выборочная сверка RECON-P5BR

Источник: `C:\Users\Slaven\Projects\DUNE\codex-direct\P5\recon-b\RECON.md` (237 строк, прочитан целиком, обрезки не было).
Ревизии: F = `9208dcf5a358f40afd95c99480e4e09f781ed566`, P = `616280c8926ec642d86144a9fe2db105ceaf4061`. Репозиторий не менялся.
Команда каждой строки: `git -C C:/Users/Slaven/Projects/DUNE show <sha>:<путь> | sed -n '<диапазон>'`.

## Таблица

| № | пункт | утверждение (кратко) | команда | вывод (до 2 строк) | совпало/не совпало |
|---|---|---|---|---|---|
| 1 | 1 | `optionText` в `cOptionsState.cpp@F:31-36`: выбор english/russian по `settings.language == "en"` | `show F:src/gamestates/cOptionsState.cpp \| sed -n '31,36p'` | `std::string optionText(const GameSettings &settings,` / `return std::string(settings.language == "en" ? english : russian);` | совпало |
| 2 | 1 | `operator==` объявлен в `cOptionsState.h@F:47` | `show F:src/gamestates/cOptionsState.h \| sed -n '47p'` | `bool operator==(const ResolutionOption &) const = default;` | совпало |
| 3 | 2 | `OptionsMenuLayout.hpp@F:7-27`: 13 полей; `create` с параметрами canvasWidth, canvasHeight, buttonHeight, playing, titleFontHeight=-1 | `show F:src/gamestates/OptionsMenuLayout.hpp \| sed -n '7,27p'` | строки 8–18: 11 полей `cRectangle`; 19–20: `int contentTop`, `int contentGap` (итого 13); строки 22–27: `static OptionsMenuLayout create(`, параметры, `int titleFontHeight = -1)` | совпало |
| 4 | 2 | `AdvancedOptionsHeaderLayout.hpp@F:7-20`: поле `title`, четыре `tabs`; `create(windowWidth, margin, buttonHeight, fontHeight)` | `show F:src/gamestates/AdvancedOptionsHeaderLayout.hpp \| sed -n '7,20p'` | `cRectangle title;` / `std::array<cRectangle, 4> tabs;` / `create(` с `int windowWidth, int margin, int buttonHeight, int fontHeight` | совпало |
| 5 | 3 | `RenderScale.hpp@F:12-15`: Min 800×600, AutomaticRenderScale=0, ManualRenderScales={100,125,150,175,200} | `show F:src/utils/RenderScale.hpp \| sed -n '12,15p'` | `constexpr int MinimumRenderWidth = 800;` / `constexpr std::array<int, 5> ManualRenderScales{100, 125, 150, 175, 200};` | совпало |
| 6 | 3 | `WorldScale.hpp@F:5-6`: AutomaticWorldScale=0, ManualWorldScales={100,110,125,150} | `show F:src/utils/WorldScale.hpp \| sed -n '5,6p'` | `constexpr int AutomaticWorldScale = 0;` / `constexpr std::array<int, 4> ManualWorldScales{100, 110, 125, 150};` | совпало |
| 7 | 4 | `cOptionsState.cpp@F:734-740`: надпись «Saved. Restart the game.» / «Сохранено. Перезапустите игру.» | `show F:src/gamestates/cOptionsState.cpp \| sed -n '734,740p'` | `"Saved. Restart the game.",` / `"Сохранено. Перезапустите игру."` внутри `optionText(` | совпало |
| 8 | 4 | `Preferences.cpp@P:68-69`: WorldScale читается в `settings.worldScalePercent` | `show P:src/game/Preferences.cpp \| sed -n '68,69p'` | `if (section.hasValue("WorldScale")) {` / `settings.worldScalePercent = section.getInt("WorldScale");` | совпало |
| 9 | 5 | `cMainMenuState.cpp@P:166-168`: переход в GAME_OPTIONS из главного меню | `show P:src/gamestates/cMainMenuState.cpp \| sed -n '166,168p'` | `addButton("Options", true, [this]() {` / `m_stateTransitions->setNextState(GAME_OPTIONS);` (стр. 167) | совпало |
| 10 | 5 | `cGamePlaying.cpp@P:538-540`: переход в GAME_OPTIONS из боя | `show P:src/gamestates/cGamePlaying.cpp \| sed -n '538,540p'` | `if (event.isAction(eKeyAction::OPEN_MENU)) {` / `m_stateTransitions->setNextState(GAME_OPTIONS);` (стр. 539) | совпало |
| 11 | 6 | `constructAdvancedWindow` определена в `cOptionsState.cpp@F:278-518` | `show F:src/gamestates/cOptionsState.cpp \| sed -n '278p;518p'` | стр. 278: `void cOptionsState::constructAdvancedWindow(int /*prevState*/)` / стр. 518: `}` | совпало |
| 12 | 6 | `AdvancedOptionsHeaderLayout::create` вызывается из `cOptionsState.cpp@F:313` | `show F:src/gamestates/cOptionsState.cpp \| sed -n '313p'` | `AdvancedOptionsHeaderLayout::create(` | совпало |

Итог: 12 из 12 совпало.

## Проверки в OptionsMenuLayoutTests

Файл `tests/OptionsMenuLayoutTests.cpp@F`: 365 строк, 13 860 байт. Копия: `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\p5br\OptionsMenuLayoutTests.9208dcf.cpp`.

Счётчик макросов по шаблону из RECON (`assert`, `ASSERT_*`, `EXPECT_*`, `CHECK*`, `REQUIRE*`): вывод `0`. Отдельный поиск `\b(assert|ASSERT|EXPECT|CHECK|REQUIRE)`: совпадений нет.

Собственные проверки (статический подсчёт вызовов в тексте; вызовы групп из `checkCanvas` выполняются на каждом случае матрицы, в подсчёт это не входит):

| имя | вызовов | строки вызовов | определение |
|---|---|---|---|
| `check.fail(` | 6 | 49 (equal), 214, 227 (inside), 238 (headerSpacing), 263, 274 (overlap) | `Check::fail` строки 29–37 |
| `equal(` | 13 | внутри `rectangleEqual`, `exact`, `table` и др. | строки 47–52 |
| `rectangleEqual(` | 6 | `exact` 155, 164; `table` 202–204 и др. | строки 54–66 |
| `exact(` | 1 | 296 | строки 151–167 |
| `table(` | 1 | 352 | строки 169–207 |
| `inside(` | 2 | 297, 347 | строки 209–232 |
| `headerSpacing(` | 2 | 298, 348 | строки 234–242 |
| `overlap(` | 2 | 299, 349 | строки 252–280 |
| `.finish()` | 6 | 353–358 | строки 39–44 |
| `return 1` | 1 | 361 (`main`) | строки 283–365 |

Прочие функции: `compactSpacing` 68–78, `expectedContentTop` 80–87, `expectedRectangles` 108–149, `intersects` 244–250, `main` 283–365.

Что проверяет файл (по коду):
- `exact` (151–167): поля `OptionsMenuLayout` из `expectedRectangles` (10 прямоугольников, для playing — save/load/missionSelect), плюс `speedLabel`, `contentTop`, `contentGap`.
- `table` (169–207): четыре фиксированных входа (строки 183–186): окно, x/y/ширина кнопок quit, mainMenu, back, `save.y` для playing.
- `inside` (209–232): окно в пределах холста с вертикальным полем 4; кнопки внутри окна и с шириной больше 0.
- `headerSpacing` (234–242): `contentTop` не меньше `2 + (bh − 10) + 2`.
- `overlap` (252–280): попарные пересечения кнопок и пересечения каждой кнопки с девятью строками настроек.
- `main` (283–365): матрица — 35 стандартных разрешений и 4 других выхода, с ручными масштабами из `ManualRenderScales`, плюс диапазоны Wc×Hc, плюс bh 32–44; отдельный прогон `bh44` (341–351) вызывает `inside`, `headerSpacing`, `overlap` при bh 44.
- Провал: `Check::fail` увеличивает счётчик и пишет в stderr (вывод до 20 на группу, строка 32); при любом провале `main` возвращает 1; при успехе печатает «Проверено случаев матрицы А + Б» (строка 363).

Сверка диапазонов RECON с файлом (не входили в 12 фактов):
- `exact` RECON 151–168; функция 151–167 — не совпало (строка 168 пустая).
- `table` RECON 169–208; функция 169–207 — не совпало (строка 208 пустая).
- `inside` RECON 209–233; функция 209–232 — не совпало (строка 233 пустая).
- `header-spacing` RECON 234–250; функция 234–242, строки 244–250 — функция `intersects` — не совпало.
- `overlap` RECON 252–282; функция 252–280, строки 281–282 — закрытие namespace и пустая строка — не совпало.
- `bh44` RECON 341–349; цикл 341–351, вызовы 347–349 — не совпало (диапазон короче цикла).
- Заголовки `#include` в строках 4–9 совпали с RECON (`<algorithm>`, `<array>`, `<cstddef>`, `<iostream>`, `<string>`, `<string_view>`).

Выполнение теста не запускалось; проверялся только текст.
