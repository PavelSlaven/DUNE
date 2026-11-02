# U13 — раскладка главной страницы окна настроек

Источник истины поведения для задания на приёмочные тесты (`codex-direct/U13/TESTS-options.md`) и для задания на реализацию. Issue #31.

## Почему

Автоматический масштаб отрисовки даёт холст высотой ровно 600 логических пикселей на любом выходе 4:3 и шире (`src/utils/RenderScale.cpp:17–24`; ручные масштабы доступны, только пока холст не ниже 600: `isManualRenderScaleAvailable`). Окно настроек в HD — `min(Hc − 32, 680)` = 568 в высоту (`src/gamestates/cOptionsState.cpp:764–766`). `OptionsMenuLayout::create` (`src/gamestates/OptionsMenuLayout.hpp`) ставит строку «Применить» на высоту `10 · (bh + 2)` от верха окна, а кнопки низа — снизу вверх по одной в ряд. При высоте кнопки HD `bh` = 42 кнопки низа ложатся на строки настроек: в игре «Сохранить игру», «Загрузить игру», «Выбор миссии» и «В главное меню» закрывают строки «Полноэкранный режим», «Язык», «Применить», «Дополнительные настройки»; в меню «В главное меню» задевает «Применить». В классической графике на холсте высотой 600 — то же. Журналы геометрии аудита U11 (`/srv/dune/worktrees/u11/.tmp/full/logs/*/*/*/*/options-*-main*.geometry.jsonl`): наложения есть только у главной страницы, у страниц «Дополнительных настроек» их нет.

Решение владельца: кнопки низа — в ряды по три; окно растёт в высоту, когда иначе не помещается, но не выше холста без 8 пикселей.

## Входы

`OptionsMenuLayout::create(int canvasWidth, int canvasHeight, int buttonHeight, bool hdLayout, bool playing)`:

- `Wc` = `canvasWidth`, `Hc` = `canvasHeight` — логический холст (`m_game.m_screenW`, `m_game.m_screenH`), всегда не меньше 800 × 600;
- `bh` = `buttonHeight` — высота кнопки (в игре: HD — `max(32, высота шрифта + 10)` = 42, классика — `высота шрифта + 4` = 20; на русском и английском одинаково, по журналам геометрии U11);
- `hd` = `hdLayout` — HD-графика;
- `playing` — окно открыто из игры (`m_prevState == GAME_PLAYING`): есть ряд «Сохранить игру», «Загрузить игру», «Выбор миссии».

## Величины

Все деления — целочисленные деления C++ над неотрицательными числами.

| Величина | HD | Классика |
|---|---|---|
| `m` (поле) | 8 | 4 |
| `g` (зазор между рядами кнопок низа) = `max(2, m / 2)` | 4 | 2 |
| `c` (зазор строк содержимого) | 2 | 5 |
| `contentX` | 24 | 5 |
| `applyWidth` | 170 | 115 |
| `advancedWidth` | 220 | 160 |
| `W` (ширина окна) | `min(Wc − 32, 680)` | `Wc / 2` |
| `oldH` (прежняя высота окна) | `min(Hc − 32, 680)` | `Hc / 2` |

- `applyY = 10 · (bh + c)`, `applyBottom = applyY + bh`.
- `n` = 2, если `playing`, иначе 1 — число рядов кнопок низа.
- `required = applyBottom + m + n · bh + (n − 1) · g + m`.
- `H = min(Hc − 8, max(oldH, required))` — высота окна.

## Результат

Новое поле `cRectangle window` — прямоугольник окна в координатах холста: `{(Wc − W) / 2, (Hc − H) / 2, W, H}`.

Остальные прямоугольники — в координатах окна: `cOptionsState` передаёт их в `GuiWindow::getRelativeRect` (`cOptionsState.cpp:801–808`).

- `apply = {contentX, applyY, applyWidth, bh}` — равно коду `main` (`OptionsMenuLayout.hpp:36–41`);
- `advanced = {contentX + applyWidth + m, applyY, advancedWidth, bh}` — равно коду `main` (`OptionsMenuLayout.hpp:42–47`);
- `status = {statusX, applyY, max(0, W − m − statusX), bh}`, `statusX = contentX + applyWidth + m + advancedWidth + m` — равно коду `main` (`OptionsMenuLayout.hpp:48–54`);
- столбцы кнопок низа: `colW = (W − 4 · m) / 3`; `x0 = m`; `x1 = 2 · m + colW`; `x2 = 3 · m + 2 · colW`; `lastW = W − m − x2`;
- нижний ряд, `bottomY = H − m − bh`: `quit = {x0, bottomY, colW, bh}`, `mainMenu = {x1, bottomY, colW, bh}`, `back = {x2, bottomY, lastW, bh}`;
- при `playing` верхний ряд, `upperY = bottomY − g − bh`: `save = {x0, upperY, colW, bh}`, `load = {x1, upperY, colW, bh}`, `missionSelect = {x2, upperY, lastW, bh}`;
- без `playing` поля `save`, `load`, `missionSelect` — прямоугольники по умолчанию (`cRectangle()`), равно коду `main` (`OptionsMenuLayout.hpp:76`).

Имена прежних полей не меняются. Прежняя сигнатура `create` с восемью параметрами удаляется.

## Строки содержимого

Строки настроек 1–9 главной страницы — в `cOptionsState::constructWindow`, их раскладка не меняется: строка `k` занимает по высоте `[k · (bh + c), k · (bh + c) + bh)` в координатах окна (`contentRowStride · k`, `cOptionsState.cpp:790` и строки 907–1403). Строка 10 — `apply`, `advanced`, `status`.

## Что меняется в `cOptionsState`

Только `cOptionsState::constructWindow` для главной страницы (`OptionsPage::Main`): прямоугольник `GuiWindow` берётся из `window`, ширина окна для прочих расчётов — `window.getWidth()`; строки 1–9 не меняются; надписи, темы и действия кнопок не меняются; прямоугольники кнопок берутся из полей раскладки. `constructAdvancedWindow` не меняется. Файлы `src/gamestates/cOptionsState.h` и `src/gui/GuiWindow.cpp` не меняются: их правит задача U11.

## Числа для сверки

| Случай | `W × H` | `window` | `bottomY` | `upperY` | `x0`, `x1`, `x2` | `colW`, `lastW` |
|---|---|---|---|---|---|---|
| HD, игра, холст 1067 × 600, `bh` 42 | 680 × 586 | {193, 7, 680, 586} | 536 | 490 | 8, 232, 456 | 216, 216 |
| HD, меню, холст 1067 × 600, `bh` 42 | 680 × 568 | {193, 16, 680, 568} | 518 | — | 8, 232, 456 | 216, 216 |
| HD, игра, холст 1920 × 1080, `bh` 42 | 680 × 680 | {620, 200, 680, 680} | 630 | 584 | 8, 232, 456 | 216, 216 |
| HD, игра, холст 801 × 600, `bh` 42 | 680 × 586 | {60, 7, 680, 586} | 536 | 490 | 8, 232, 456 | 216, 216 |
| Классика, игра, холст 800 × 600, `bh` 20 | 400 × 320 | {200, 140, 400, 320} | 296 | 274 | 4, 136, 268 | 128, 128 |
| Классика, игра, холст 1067 × 600, `bh` 20 | 533 × 320 | {267, 140, 533, 320} | 296 | 274 | 4, 180, 356 | 172, 173 |
| Классика, меню, холст 800 × 600, `bh` 20 | 400 × 300 | {200, 150, 400, 300} | 276 | — | 4, 136, 268 | 128, 128 |

`x0`, `x1`, `x2` — `x` у `quit`, `mainMenu`, `back` (и у `save`, `load`, `missionSelect` при `playing`). «—» в столбце `upperY`: верхнего ряда нет, поля `save`, `load`, `missionSelect` равны `cRectangle()`.

В HD-игре на холсте 1067 × 600: `applyBottom` = 482, `upperY` = 490 = `applyBottom + m`.

## Проверка в игре

Тест `create` не видит `cOptionsState::constructWindow`. После реализации ведущий проверяет игру по журналам геометрии аудита U11 на сборке с U13: сцены `options-menu-main`, `options-game-main-saves`, `options-game-main-nosaves`, все разрешения и масштабы аудита, русский и английский, HD и классика.

- Запись `GuiWindow` сцены равна `window` по формулам этого файла: холст — из строки `header`, `bh` — 42 в HD и 20 в классике, `playing` — у сцен `options-game-*`.
- Каждая запись `GuiButton` лежит внутри записи `GuiWindow`.
- Правило 9 (`click-zones-overlap`) аудита U11 — 0 флагов на этих сценах; правило 3 (`elements-overlap`) — 0 флагов в парах, где есть `GuiButton` или `GuiWindow`. Флаг, который есть и на той же сцене сборки `main` между элементами строк 1–10, к U13 не относится: ведущий заводит на него отдельный issue.
