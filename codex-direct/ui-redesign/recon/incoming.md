# Карта фактов: части интерфейса форка, которые придут шагами П8–П11

## Источники и соглашения

- Разделы 1–5, 8, 9: код форка из `origin/main` (`git show origin/main:<путь>`). Номера строк совпадают со строками FORK1 `9208dcf`: по UI-файлам разница между `9208dcf` и `origin/main` нулевая (`git diff --stat 9208dcf origin/main -- src` даёт одну строку: `src/utils/d2tm_math.cpp`, вне UI).
- Разделы 6–7: документы разведки `L/codex-direct/P8..P11/recon/` (RECON.md, ERRATA.md, TSV). Ревизии в них: BASE `e17379a`, FORK1 `9208dcf` (предок `origin/main`), UP1 `d06f2fc`, MAIN `62e1ff6`. PORT: П8 — `0a33444`, П9 — `616280c`, П10 и П11 — `832c953` (предок `HEAD` рабочей копии `91416fb0c`; в `origin/main` не входит).
- Координаты — логические пиксели (`game.m_screenW`, `game.m_screenH`). Формулы записаны как в коде. Примеры «1280×800» — расчёт по формулам кода, запуска не было.
- Все проверки — чтение (`git show`, `git grep`, `git ls-tree`, `git cat-file`), без изменения состояния.

---

## 1. Панель приказов (`cCommandBarDrawer`)

### Где и когда видна
- Рисуется безусловно в `cDrawManager::drawCombatState`: `src/managers/cDrawManager.cpp:93` (`m_commandBarDrawer.draw()`), после уведомлений (`:91`). Условия скрытия в функции нет (чтение `cDrawManager.cpp:48-100`). Если ширина панели ≤ 0, кнопки не строятся (`src/drawers/cCommandBarDrawer.cpp:80`).
- Клик: `cInteractionManager.cpp:87`, `cDrawManager.cpp:459` → `onNotifyMouseEvent`. Блок курсора по панели: `src/controls/cGameControlsContext.cpp:54` (`isMouseOver`).

### Геометрия (`src/drawers/CommandBarLayout.hpp`, 44 строки)
- Константы: `ActionCount = 7` (`:9`); идеал 350×52 (`:16-17`); `bottomScrollClearance = 8` (`:18`); `outerMargin = 8` (`:19`).
- `battlefieldW = max(0, W − sidebarW)` (`:21`); `availableW = max(0, battlefieldW − 16)` (`:22`); `panelW = min(350, availableW)` (`:23`).
- `panelH = max(1, (panelW·52 + 175) / 350)` (`:24-27`) — пропорционально ширине.
- `panelX = min(8, max(0, battlefieldW − panelW))` (`:28`); `panelY = max(0, H − 8 − panelH)` (`:29`) — низ экрана, левый край.
- Ячейки: границы `0,400,800,1200,1600,2000,2400,2800` (`:34-36`), `x0 = panelX + panelW·ref/2800` (`:38-39`) — семь равных ячеек по 1/7 ширины.
- `sidebarW` = `cSideBar::SidebarWidth` (`cCommandBarDrawer.cpp:76`). Значение по умолчанию 224 (`src/sidebar/cSideBar.h:84`). В HD-режиме `configureLayout`: 280 при `logicalWidth < 960`, иначе 360 (`src/sidebar/cSideBar.cpp:411-421`, строка `:419`).
- Пример (расчёт): 1280×800 → sidebarW 360, battlefieldW 920, панель 350×52 в точке (8, 740); ячейка 50 px по ширине; ячейки начинаются с x = 8, 58, 108, 158, 208, 258, 308.

### Кнопки (`src/drawers/cCommandBarDrawer.cpp:85-93`, `CommandBarPolicy.hpp`)

| Ячейка | Command | Подпись (`localization::text`) | Клавиша (отображаемая) | Условие доступности | Значок без текстуры | Действие |
|---|---|---|---|---|---|---|
| 0 | Move | Move / Переместить | `LMB` (строка, не клавиша) | есть выбранные юниты (`CommandBarPolicy.hpp:3`) | стрелка (`cCommandBarDrawer.cpp:208`) | `activateMoveCommand` (`:279-281`) |
| 1 | Attack | Attack / Атаковать | `commandBindingDisplayName(attack)` = `CTRL` | выбран не-харвестер, атакующий юниты/воздух/здания (`:342-349`; `Policy:8`) | прицел (`:214-220`) | `activateAttackCommand` (`:282-284`) |
| 2 | Repair | Repair / Ремонт | `R` | всегда (`Policy:13-16`) | крест (`:221-224`) | `setMouseState(MOUSESTATE_REPAIR)` (`:285-287`) |
| 3 | Unload | Unload / Разгрузить | `D` | выбран харвестер с `canUnload()` (`:351-356`) | стрелка вниз (`:225-231`) | `executeUnload`: харвестеры к НПЗ (`:305-313`) |
| 4 | Deploy | Deploy / Развернуть | `D` | выбран MCV (`:358-363`) | силуэт здания (`:232-237`) | `executeDeploy`: CONSTYARD, если можно разместить (`:315-327`) |
| 5 | Rally | Rally / Точка сбора | `CTRL` | своя выбранная структура с `canSpawnUnits()` (`Policy:28-33`) | флаг (`:238-242`) | `activateRallyPointCommand` (`:294-296`) |
| 6 | Release | Release / Выпустить | `D` | своя выбранная структура типа REPAIR (`Policy:35-40`) | бокс со стрелкой вверх (`:243-248`) | `GAME_EVENT_DEPLOY_UNIT` (`:329-340`) |

- Поле `active` во всех ячейках `false` (`:86-92`). Поле `label` в `draw` не читается (в `cCommandBarDrawer.cpp` нет обращения к `button.label`), поэтому подписи на экране не выводятся. Подсказок при наведении нет: `m_hoveredButton` (`cCommandBarDrawer.h:68`) пишется в `onNotifyMouseEvent` (`:257-262`), но в `draw`/`drawButton` (`:97-196`) не используется.
- Клавиши по умолчанию — `src/controls/CommandBindings.hpp:21-26`: attack `LCTRL`, repair `R`, unload `D`, deploy `D`, rally `LCTRL`, release `D`. Подписи `commandBindingDisplayName` (`:115-143`): `CTRL`, `SHIFT`, `ALT`, `ENTER`, `SPACE`/`ПРОБЕЛ`; остальное — имя SDL-скан-кода в верхнем регистре.

### Состояния ячейки (`cCommandBarDrawer.cpp:126-196`)
- Есть `command_bar.png` и загружен `command_bar_disabled.png`: enabled → ячейка i из `command_bar.png`; ширина источника `w/7`, последняя ячейка — остаток (`:130-142`); disabled → ячейка не рисуется, виден фон `command_bar_disabled.png` (`:105-107`).
- Есть `command_bar.png`, нет disabled-текстуры: disabled → заливка `Color{2,3,3,118}` поверх ячейки (`:143-145`).
- Нет текстур: заливка `active ? {69,54,27,255} : {25,30,32,255}`; рамка `enabled ? {105,80,39} : {57,59,58}` (`:147-156`); значок цвета `enabled ? {210,170,82} : {105,105,100}` (`:165`).
- Фон панели без текстур: `{13,17,19,242}`, линия сверху `{188,139,47}`, рамка `{105,80,39}` (`:112-114`).
- В конце `draw` — общий фильтр по всей панели `Color{5,24,48,38}` (`:121-123`).
- Значок (без текстуры): область `x+4, y+5, w−8, h·52/100` (`:158-164`); полуширина 8, полувысота 7 от центра (`drawIcon :198-205`).

### Горячие клавиши на ячейке (`:168-195`)
- Прямоугольник клавиши: `w = max(9, cellW·30/100)`, `h = max(9, cellH·30/100)` (`:169-170`).
- Позиция: чётный индекс (Move, Repair, Deploy, Release) — x = 6%, y = 67%; нечётный (Attack, Unload, Rally) — x = 65%, y = 4% (`:171-177`).
- Текст цвета `Color{83,50,19}`; масштаб: `clamp(min(wScale, hScale), 0.50, 1.45 для одного символа / 1.15 иначе)` (`:178-187`). Рисуется только у enabled-кнопки с непустой клавишей (`:168`).
- Шрифт: `TextContext::getCommandKeyTextDrawer()` (`cCommandBarDrawer.cpp:33`; `src/context/TextContext.cpp:32`).

### Текстуры
- `loadHdUiTexture("command_bar.png" | "command_bar_disabled.png")` (`cCommandBarDrawer.cpp:40-49`). Путь: `data/hd4/<имя>` относительно рабочего каталога; плотность зашита как 4 (`src/utils/HdUiTextureLoader.cpp:14-22`, константа `:20`).
- Файлы и размеры — раздел 9: оба файла 2800×414 px; 7 ячеек по 400 px.

### Подсказки и уведомления над панелью
- Всплывающих подсказок у панели нет (см. «Подписи» выше).
- Уведомления: `cDrawManager::drawNotifications` (`src/managers/cDrawManager.cpp:435-444`): `x = 4`, `y = top панели − 18`, шаг −15 px, цвет из `notification.getColor()`.

### Кнопка ORDER / ЗАКАЗ (рядом по смыслу, другой класс)
- `src/drawers/cOrderDrawer.cpp`: кнопка `BTN_ORDER` из gfxinter (индексный спрайт, не HD PNG), точка: `x = (W − sidebarWidthWithoutCandyBar/2) − w/2`, `y = (H − 25) − h/2` (`:25-32`); подпись `ORDER`/`ЗАКАЗ`, масштаб 0.92 (`:57-66`); в серой/нажатой фазе — затемнение `renderRectColor(...,0,0,0,128)` (`:49-52`).
- `OrderButtonPolicy.hpp:3-6` (`shouldDrawOrderLabelShadow() = false`) используется только здесь (`cOrderDrawer.cpp:65`). Вызов: `cSideBarDrawer.cpp:402`.

---

## 2. Панель музыки

### Где и кто рисует
- Верхняя полоса боя (TopBar, высота 42: `src/sidebar/HudLayout.hpp:14`). Вызов: `cDrawManager::drawCombatState` → `drawTopBarMusicControls()` (`cDrawManager.cpp:89`).
- `drawTopBarMusicControls` (`cDrawManager.cpp:288-294`): `left = 143` (константа `:291`), `right = layout.battlefield.endX − 8` (`:292`), `HudLayout.battlefield = (0, 42, W − sidebarWidth, H − 42)` (`HudLayout.hpp:58-63`).
- `drawMusicControls(left, right)` (`cDrawManager.cpp:296-422`) — рисует панель, кнопки, подпись, ползунок.
- Сообщение справа от панели: `cMessageDrawer::draw` (`src/drawers/cMessageDrawer.cpp:39-75`) вычисляет тот же layout (`:51-55`), затем `messageX = music.visible ? music.panel.endX + 8 : left` (`:56-58`), прямоугольник `y = 4`, `h = 33`, заливка `{20,24,26}` (`:59-71`). `reserved = textLength(message) + 16` (`cMessageDrawer.cpp:48-50`; `cDrawManager.cpp:298-301`).

### Раскладка (`src/sidebar/MusicControlsLayout.hpp`, 65 строк)
- `create(left, right, reservedMessageWidth)` (`:18-59`): `available = right − left`; при `reserved > 0`: `controlsWidth = available − reserved − 8` (`:26-28`); если `controlsWidth < 200` — не видна (`:29-31`).
- `width = min(controlsWidth, 520)` (`:33`); `buttonSize = 33` (`:34`); `y = 4` (`:35`); `gap = 5` (`:36`); `sectionGap = 8` (`:37`).
- `contentWidth = width − 8`; `musicWidth = contentWidth/2`; `speedWidth = contentWidth − musicWidth` (`:38-40`).
- `labelX = left + 38`; `labelWidth = max(0, musicWidth − 76)` (`:41-42`).
- `speedX = left + musicWidth + 8`; `speedLabelWidth = min(76, speedWidth/2)`; `speedSliderX = speedX + speedLabelWidth + 5`; `speedSliderWidth = max(0, speedWidth − speedLabelWidth − 5)` (`:43-46`).
- Прямоугольники (`:50-57`): `panel (left,4,width,33)`, `musicPanel (left,4,musicWidth,33)`, `previous (left,4,33,33)`, `label (labelX,4,labelWidth,33)`, `next (left + musicWidth − 33, 4, 33, 33)`, `speedPanel (speedX,4,speedWidth,33)`, `speedLabel (speedX,4,speedLabelWidth,33)`, `speedSlider (speedSliderX,4,speedSliderWidth,33)`.
- `showsLabel()` = `label.width ≥ 80` (`:61-64`).
- Пример 1280×800 без сообщения (расчёт): `left 143`, `right 912`, `width 520`; музыка 143–399, скорость 407–663; prev 143–176; подпись 181–361; next 366–399; speedLabel 407–483; ползунок 488–663 (ширина 175).

### Цвета и кнопки (`cDrawManager.cpp:316-326`)
- Панель `{35,32,25,255}`; рамка `{188,139,47,255}`; тёмная рамка `{71,50,24,255}`; текст `{232,222,188,255}`.
- Кнопки prev/next — заливка панели + рамка; символы `"<"` и `">"` через `m_textDrawer`, по центру (`:321-326`).
- Клик (`:412-421`): при `mouse->isLeftButtonClicked()` над prev → `game.playPreviousGameplayTrack()`, над next → `game.playNextGameplayTrack()`.
- Подпись трека: `game.getCurrentMusicTrackName()`; обрезка по `label.width − 10` с `"..."` через `m_smallTextDrawer` (`:328-350`); рисуется заливкой панели и рамкой (`:354-356`), текст по центру `drawTextCenteredInBox`. Подпись только при `showsLabel()`.
- Подпись ползунка: `localization::text("SPEED", "СКОРОСТЬ")` в `speedLabel`, малый шрифт (`:359-365`); заливка и рамка `gui_DrawRectBorder` (`:359-360`, `:367-368`, `:409-410`).

### Ползунок скорости (`:370-410`)
- Диапазон `MinSliderValue = 2`, `MaxSliderValue = 10`; ширина ручки `12` (`:370-372`).
- `globalSpeed = clamp(timeManager.getGlobalSpeed(), 2, 10)`; `sliderValue = 12 − globalSpeed` (`:373-374`).
- Начало перетаскивания: нажатие или клик в зоне ползунка (`:377-388`). Во время перетаскивания: `value = 2 + pos·8 / max(1, w)`, `requestedGlobalSpeed = 12 − value`; при отличии вызывается `setGlobalSpeed` (`:389-402`).
- Ручка: `knobTravel = max(0, w − 12)`; `knobX = x + (value − 2)·knobTravel / 8` (`:404-408`); заливка `borderDark`, рамка `border/borderDark` (`:409-410`).

### Клавиатурные действия трека (не в панели)
- `cGame_logic.cpp:2105-2110`: `SDL_SCANCODE_LEFTBRACKET` → предыдущий, `SDL_SCANCODE_RIGHTBRACKET` → следующий (код, не настройка).
- `cGame_logic.cpp:2092`: `M` или `MUTE` — переключение музыки. `:2113`: `O` / `VOLUMEDOWN`. `:2117`: `P` / `VOLUMEUP`.
- В `origin/main` `resources/bin/settings.ini` секции `[KEYS]` нет (секции: `[SETTINGS]` строка 1, `[DATAFILE]` 69, `[HD4_DATAFILE]` 72, `[FONT]` 79); ключей `TOGGLE_MUSIC` / `MUSIC_VOLUME_*` нет; есть только закомментированный `#playMusic = false` (строка 61).

### Не найдено / не проверено
- Поиск `MusicControlsLayout` в `origin/main -- src` дал: `cMessageDrawer.cpp:7,51`, `cDrawManager.cpp:15,302`, `MusicControlsLayout.hpp`. Других рисовальщиков нет.

---

## 3. Подсказка у курсора

### Что лежит в файлах форка
- `src/gui/MouseToolTip.h:12-22` — класс `cMouseToolTip`: публичные конструктор и деструктор, закрытое поле `cPlayer *player`. Методов рисования нет.
- `src/gui/MouseToolTip.cpp:12-20` — конструктор (`assert`, сохранение игрока), деструктор пустой.
- `src/drawers/cMouseDrawer.h:36` — член `cMouseToolTip m_mouseToolTip`; обращений к нему, кроме инициализации (`cMouseDrawer.cpp:17`), нет (`git grep`).

### Фактически нарисованная подсказка — `cMouseDrawer`
- Вызов: `cDrawManager::drawCombatMouse` (`src/managers/cDrawManager.cpp:216-225`): `if (context->shouldDrawToolTip()) m_mouseDrawer->drawToolTip();`.
- Флаг: `cGameControlsContext::shouldDrawToolTip()` (`src/controls/cGameControlsContext.h:68-70`) возвращает `m_drawToolTip`; инициализация `false` (`cGameControlsContext.cpp:13`).
- Единственное место, где флаг мог бы стать `true`, — `determineToolTip()` (`cGameControlsContext.cpp:102-110`); тело полностью закомментировано (`:104-109`). Присваивания `m_drawToolTip` в коде остались только в комментариях (`:106`, `:108`). Поэтому подсказка сейчас не показывается.
- Ширина (`cMouseDrawer.cpp:53-62`): 250, если `context->isMouseOverStructure()`, иначе 0 (тогда не рисуется).
- Высота (`:64-96`): 78 для WINDTRAP, REFINERY, SILO, TURRET, RTURRET; иначе 50.
- Позиция (`:29-51`): `x = mouseX + 32`, `y = mouseY + 32`; при выходе за `m_screenW`/`m_screenH` сдвиг назад на величину выхода.
- Фон (`:135-169`): цвет — `getMinimapColor()` владельца структуры (или игрока, если структуры нет); каждый канал − 64 (не ниже 0); альфа 128; прямоугольник `(x, y, w, h)`. Тень: чёрный, альфа 128, полоса `(x+4, y+h, w−4, 4)` и полоса `(x+w, y+4, 4, h)` (`:164-168`).
- Текст: `cTextWriter(textDrawer, 12)` (`cMouseDrawer.cpp:21`), `moveTo(x+2, y+2)` (`:113`), шаг строки 12 px (`src/gui/cTextWriter.cpp:36-39`). Шрифт — малый текстовый drawer (`cDrawManager.cpp:41`).
- Строки общей части (`:184-199`): название структуры жёлтым `{255,255,0}`, при primary — `"<name> (PRIMARY)"`; `"Health: {}/{}"` / `"Прочность: {}/{}"`; `"Armor: {}"` / `"Броня: {}"`; `"Foundation: {}%"` / `"Фундамент: {}%"`.
- Ветка ветряка (`:202-221`): владелец HUMAN — `"Usage: {}/{} (normal|low)"` / `"Расход: {}/{} (норма|мало)"` и `"Power output: {}/{}"` / `"Выработка энергии: {}/{}"`; чужой — варианты `unknown`/`неизвестно`.
- Ветка турели (`:171-182`): `"Sight: {}"` / `"Обзор: {}"`, `"Range: {}"` / `"Дальность: {}"`; чужая — `unknown`/`неизвестно`.
- Ветка SILO/REFINERY (`:223-…`): вызов есть (`:126-128`), строки не разбирались полностью.

### Курсор
- Курсор рисует `game.getMouse()->draw()` (`cMouseDrawer.cpp:24-27`, `cDrawManager.cpp:227-230`).

---

## 4. Меню настроек форка (`cOptionsState`)

### Структура
- Класс: `src/gamestates/cOptionsState.h:24`. Страницы — `enum class OptionsPage { Main, Gameplay, Controls, Diagnostics }` (`cOptionsState.h:50-55`). Текущая: `m_optionsPage` (`:75`).
- Главная страница строится в `constructWindow` (`cOptionsState.cpp:760-1385`). Остальные три — в `constructAdvancedWindow` (`:278-518`), вызов при `page != Main` (`:762-765`).
- Переход: `requestOptionsPage` ставит `m_pendingOptionsPage` (`:666-669`), `thinkFast` переключает (`:1393-1402`), `switchOptionsPage` сбрасывает захват клавиши и сообщение, затем `refresh()` (`:658-664`).

### Вкладки (`src/gamestates/AdvancedOptionsHeaderLayout.hpp`, 33 строки)
- `tabWidth = (W − margin·5) / 4` (`:17`); `tabY = fontH + margin + 2` (`:18`); вкладка i: `x = margin·(i+1) + tabWidth·i`, `h = buttonHeight` (`:24-29`); заголовок `(0, 2, W, fontH)` (`:20`).
- Подписи (`cOptionsState.cpp:321-331`): `Main / Основные`, `Gameplay / Игра`, `Controls / Управление`, `Diagnostics / Диагностика`.
- Окно advanced: `w = min(W − 32, 760)`, `h = min(H − 32, 640)`, центр (`:280-283`); `margin = 8`; `buttonHeight = max(32, fontH + 10)` (`:285`); `labelWidth = 560`, `checkX = 600` (`:286-287`); заголовок `"Dune II - Settings"` / `"Dune II — Настройки"` (`:296-298`).
- Строки: `y = row·(buttonHeight + 4)`, `row` начинается с 2 (`:333`, `:337`); подпись `x = 16`, ширина 560 (`:343`); чекбокс `x = 600`, квадрат `buttonHeight` (`:348`); ползунок `x = 370`, ширина 230 (`:369`), диапазон 1..10 (`:371-372`).

### Страница Gameplay (`:383-414`)
1. Чекбокс `cameraEdgeMove`: "Edge scrolling — move camera at screen edge" / "Прокрутка у края экрана".
2. Ползунок 1..10 `cameraBorderOrKeyMoveSpeed` (значение = round(x·10), сохранение x/10): "Keyboard/edge camera speed" / "Скорость камеры с клавиатуры и у края".
3. Ползунок `cameraDragMoveSpeed`: "Camera drag speed" / "Скорость перетаскивания камеры".
4. Чекбокс `pauseWhenLosingFocus`: "Pause when the window loses focus" / "Пауза при потере фокуса окна".
5. Чекбокс `allowRepeatingReinforcements`: "Repeat reinforcements" / "Повторять подкрепления".
6. Чекбокс `turretsDownOnLowPower`: "All turrets stop on low power" / "Отключать все башни при нехватке энергии".
7. Чекбокс `rocketTurretsDownOnLowPower`: "Rocket turrets stop on low power" / "Отключать ракетные башни при нехватке энергии".
8. Только подпись (без управления): "Rules file: game.ini (change manually)" / "Файл правил: game.ini (меняется вручную)" (`:405-413`).

### Страница Controls (`:415-479`)
- Строки: Move (`:460`), Attack (`:461`), Repair (`:462`), Unload (`:463`), Deploy (`:464`), Rally (`:465`), Release (`:466`).
- Подпись строки — слева, `w = bindingButtonX − 32`; кнопка значения: `w = 190`, `x = W_panel − 8 − 190` (`:416-417`), `h = buttonHeight`.
- Значение: у Move — `"LMB"`, кнопка выключена (`std::nullopt`, `:434-449`). У остальных — `bindingKeyName(...)`; в режиме захвата — `"Press key..."` / `"Нажмите клавишу…"` (`:436-441`).
- Клик → `m_bindingMessage.clear()`, `m_bindingCapture = action`, `refresh()` (`:451-455`).
- Сообщение под строками: `y = row·(buttonHeight + 4)`, ширина `W_panel − 32` (`:467-478`).
- Клавиатура при захвате (`:1439-1475`): только `PRESSED`; `ESCAPE` и `UNKNOWN` отменяют; конфликт → `"Key <K> is already assigned to <action>."` / `"Клавиша <K> уже назначена команде «<action>»."` (`:1457-1463`); захват сбрасывается и вызывается `refresh()` (`:1472-1473`).

### Страница Diagnostics (`:480-489`)
- 8 чекбоксов: "Debug mode" / "Режим отладки" (`debugMode`); "Disable all AI" / "Отключить ИИ" (`disableAI`); "Use one AI player" / "Оставить одного ИИ" (`oneAi`); "Disable worm AI" / "Отключить ИИ червя" (`disableWormAi`); "Disable reinforcements" / "Отключить подкрепления" (`disableReinforcements`); "Disable remaining AI" / "Отключить остальных ИИ" (`noAiRest`); "Show unit debug data" / "Показывать отладочные данные юнитов" (`drawUnitDebug`); "Show resource usage" / "Показывать расход ресурсов" (`drawUsages`).

### Нижняя панель advanced-страниц (`:491-517`)
- `Apply` / `Применить`: `x = 16`, `w = 180`, `y = mainMenuHeight − buttonHeight − 8`; сохраняет `settings.ini` через `saveSettingsToIni` (`:500`), при успехе — `m_game.m_commandBindings` (`:504`).
- `Back` / `Назад`: `x = mainMenuWidth − 180 − 8`, `w = 180` → страница Main (`:513-515`).

### Главная страница (`constructWindow`, `:760-1385`)
- Геометрия: `OptionsMenuLayout::create(W, H, buttonHeight, playing = (m_prevState == GAME_PLAYING), fontH)` (`:768-774`).
- Окно (`src/gamestates/OptionsMenuLayout.hpp:22-64`): `w = min(W − 32, 680)`, `h = min(H − 32, 680)` (`:35-36`), в компактном режиме выше; центр. Константы: `margin = 8` (`:29`), `contentGap = 2` (`:31`), `contentX = 24` (`:32`), `applyWidth = 170` (`:33`), `advancedWidth = 220` (`:34`).
- Строки контента: `contentTop + (row−1)·(buttonHeight + 2)`, `contentTop = buttonHeight + 2` (обычный режим; `:39`, `:48-50`).
- Заголовок: `"Dune II - The Maker - version " + D2TM_VERSION` (`:802`).
- Кнопки (`:806-889`):
  - `Main menu` / `В главное меню` → `GAME_MENU` + затемнение (`:806-816`), низ-середина.
  - `Quit game` / `Выйти из игры` → `m_playing = false` + затемнение (`:820-830`), низ-левая.
  - `Back` / `Назад` → предыдущее состояние (`:835-844`), низ-правая.
  - Только при `m_prevState == GAME_PLAYING` (`:847`): `Load game` / `Загрузить игру` (`:850-865`; выключена и серая, если `!SaveGameManager::hasAnySave()`; открывает диалог `open(true, false)`); `Save game` / `Сохранить игру` (`:867-877`; `open(true, true)`); `Mission select` / `Выбор миссии` (`:880-889`; `GAME_MISSIONSELECT`). Их позиция — верхний ряд (`OptionsMenuLayout.hpp:120-139`).
- Звук и музыка (`:891-1023`):
  - Строка 1: подпись `Music` / `Музыка` (`x = 24`, `w = 110`, `:897-903`); чекбокс `x = 138` → `setMusicEnabled` (`:906-923`); подпись `Volume` / `Громкость` (`x = 218`, `w = 110`, `:925-938`); ползунок `x = 350`, `w = 250`, 0..10 → `setMusicVolume` (`:940-956`).
  - Строка 2: `Sound` / `Звуки` и чекбокс → `setSoundEnabled` (`:958-990`); `Volume` / `Громкость` и ползунок 0..10 → `setSoundVolume` (`:992-1023`).
- Скорость игры (`:1025-1055`): подпись `Game speed` / `Скорость игры` (`speedLabel`: `x = 16`, `w = 122`); ползунок `x = 138`, `w = 220`, диапазон 2..10; значение `2 − globalSpeed + 10`; обратное преобразование `globalSpeed = 10 − v + 2` (`:1042-1052`).
- Строка «Разрешение» / `Resolution` / `Разрешение` (`:1057-1124`): подпись `x = 24`, `w = 160`; кнопка `<` `x = 198`, `w = 46`; значение `x = 252`, `w = 180`; кнопка `>` `x = 440`, `w = 46`.
- Строка «Масштаб игры» / `Game scale` / `Масштаб игры` (`:1126-1190`): значение `w = 200`; `>` при `x = 460`.
- Строка «Размер объектов» / `Object size` / `Размер объектов` (`:1192-1262`): такая же раскладка, значение `w = 200`.
- Полноэкранный режим / `Fullscreen` / `Полноэкранный режим` (`:1264-1308`): подпись `w = 220`, чекбокс `x = 252`.
- Язык / `Language` / `Язык` (`:1310-1346`): `<` и `>` вызывают `toggleLanguage` (`:644-656`); подпись значения `English` или `Русский` (`:655`).
- Нижний ряд: `Apply` / `Применить` (`:1349-1360`, активна при изменении, `updateDisplaySettingsDirtyState` `:671-688`); статус (`:1362-1371`): `"Saved. Restart the game."` / `"Сохранено. Перезапустите игру."` и `"Could not save settings.ini"` / `"Не удалось сохранить settings.ini"` (`:734-754`); `More settings` / `Дополнительные настройки` → страница Gameplay (`:1373-1382`).
- Фон: `m_backgroundTexture` и заливка `Color{4,6,7,150}` (`:1404-1416`).
- Диалог сохранения рисуется поверх (`:1418-1420`) и перехватывает мышь и клавиатуру, пока открыт (`:1425-1445`, `:1477-1481`).

### Файлы
- `src/gamestates/cOptionsState.cpp` (1510 строк), `cOptionsState.h` (109), `OptionsMenuLayout.hpp` (144), `AdvancedOptionsHeaderLayout.hpp` (33). Тест: `tests/OptionsMenuLayoutTests.cpp` (есть в `origin/main`).

---

## 5. Окна сохранения и загрузки (`SaveSlotsDialog`)

### Файлы форка
- `src/save/SaveSlotsDialog.hpp` (69 строк), `.cpp` (505), `src/save/SaveSlotName.hpp` (100), `src/save/SaveGameManager.hpp` (struct `SaveSlotInfo` `:13-18`), `.cpp`, `src/save/SaveFileCodec.{hpp,cpp}`. Тесты: `tests/SaveFileCodecTests.cpp`, `tests/SaveSlotNameTests.cpp`, `tests/FactoryPadSaveTests.cpp`.
- Константы: `save_slot::MaximumSlots = 10` (`SaveSlotName.hpp:12`), `MaximumNameBytes = 96` (`:13`); `SaveGameManager::FormatVersion = 2` (`SaveGameManager.hpp:22`).

### Где открывается
- Главное меню: кнопка `Saved games` / `Сохранения`, включена при `SaveGameManager::hasAnySave()` → `m_saveDialog->open(false, false)` (только загрузка) (`src/gamestates/cMainMenuState.cpp:164-165`).
- Меню настроек в игре: `Load game` (`open(true, false)`) и `Save game` (`open(true, true)`) — см. раздел 4 (`cOptionsState.cpp:850-877`).
- Клавиши F5 (быстрое сохранение) и F9 (быстрая загрузка): `cGame_logic.cpp` по P8 §4 строки 2042–2059 (FORK1 `9208dcf`).

### Геометрия (`SaveSlotsDialog.cpp:86-144`)
- Панель: `w = min(W − 24, 760)`, `h = min(H − 24, 560)`, центр (`:88-92`).
- Затемнение всего экрана `Color{0,0,0,190}` (`draw :280-295`).
- Заголовок `"SAVED GAMES"` / `"СОХРАНЕНИЯ"`, по центру, `y = panelY + 12`, цвет рамки (`:299-304`).
- Поле имени: `(panelX + 14, panelY + 48, panelW − 28, 34)` (`:95-100`); фон `{27,33,36,255}`; рамка `{232,184,78}` при редактировании, иначе `{188,137,42}` (`:307-311`); текст + `" |"` при редактировании, обрезка по `w − 20` (`:312-323`).
- Строки слотов (10 штук): `x = panelX + 14`, `w = panelW − 28`; `y0 = panelY + 92`; шаг `rowH + 3`; `rowH = max(22, (statusY − 8 − slotsY − 3·9) / 10)`, `statusY = buttonY − 27` (`:125-143`). Фон: обычный `{27,33,36}`, выбранный `{63,52,31}`; рамка `{188,137,42}` / выбранная `{232,184,78}` (`:331-338`).
- Текст строки (`:340-362`): пусто — `"NN. <empty>"` / `"NN. <пусто>"`, цвет `{114,112,104}`; повреждено — `"NN. <corrupted>"` / `"NN. <повреждено>"`, цвет `{235,126,96}`; иначе `"NN. <name>"`, цвет `{232,225,202}`. Текст: `x = rect.x + 9`, обрезка по `w − 18`.
- Кнопки внизу: `y = panelY + panelH − 48`, `h = 34`, ширина `(panelW − 28 − 16) / 3`; `Save` / `Сохранить` at `panelX + 14`, `Load` / `Загрузить` правее на `w + 8`, `Close` / `Закрыть` — ещё на `2·(w + 8)` (`:102-123`, `:390-396`). Заливка включённой `{35,42,45}`, выключенной `{24,28,30}`; рамка включённой `{188,137,42}`, выключенной `{114,112,104}`.
- Включение: Save — `m_allowSaving`; Load — выбранный слот существует и валиден (`:390-395`).
- Статус: `y = saveRect.y − 25`, по центру; зелёный `{148,213,146}`, если текст содержит «сохранён»/«saved», иначе `{235,126,96}` (`:398-408`).

### Тексты
- `"Slot {} saved."` / `"Слот {} сохранён."` (`:215-216`).
- `"The selected slot has no valid save."` / `"В выбранном слоте нет корректного сохранения."` (`:226-228`).
- Ошибки сохранения и загрузки — строка `error` из `SaveGameManager` (`:209`, `:236`).
- Имя по умолчанию: `"Save N"` / `"Сохранение N"` (`SaveSlotName.hpp:94-98`).

### Поведение
- Открытие (`:33-70`): при `preferSaving` выбирается первый пустой слот; иначе первый существующий валидный; если ничего нет — слот 1. При `preferSaving` включается редактирование имени (`:69`, `:177-192`: `SDL_StartTextInput`).
- Клавиатура (`:442-485`): ESC — закрыть; UP/DOWN — переход по слотам с зацикливанием 1..10; BACKSPACE при редактировании — удалить последний UTF-8 символ, при первом вводе — очистить; ENTER или KP_ENTER — сохранить (если `preferSaving && allowSaving`), иначе загрузить.
- Текстовый ввод (`:487-505`): байты `≥ 0x20` и `≠ 0x7F`; обрезка до 96 байт.
- Мышь (`:411-440`): клик по строке — выбор слота; по полю — редактирование; `Save`, `Load`, `Close`.
- Очистка имени (`SaveSlotName.hpp:33-92`): убирает управляющие символы, схлопывает пробелы, обрезает края, не добавляет неполные UTF-8 последовательности; лимит 96 байт.
- Сохранение (`:194-220`): `SaveGameManager::saveGame(m_game, slot, name, error)`; после успеха — `refreshSlots`, статус, `m_onSlotsChanged`.
- Загрузка (`:222-244`): `loadGame`; при успехе — `close()` и `m_onLoaded()`.
- Хранение (по P8 §1, FORK1): каталог `saves/` относительно каталога исполняемого файла; слот 1 — `saves/quicksave.d2s`, остальные — `saves/saveNN.d2s`; заголовок `D2TM_SAVE <version> <checksum>`; лимит файла 16 MiB (`SaveGameManager.cpp:43`, `:1349-1359` по P8).

---

## 6. Ментаты HD и титры форка (П11, по документам разведки)

### Ментаты
- FORK1 (`src/mentat/AbstractMentat.cpp`, `AtreidesMentat.cpp`, `BeneMentat.cpp`, `HarkonnenMentat.cpp`, `OrdosMentat.cpp`; P11 `fork-mentat.tsv`):
  - Логический экран ментата 640×480 (P11 `port-mentat.tsv`, строка про `MENTAT_SCREEN_W/H`; в UP1 константа `d06f2fc:34`).
  - Глаза и рот (`fork-mentat.tsv`): Atreides — глаза `ATR_EYES01+iMentatEyes` в `(96,180)`, рот `ATR_MOUTH01+iMentatMouth` в `(100,210)`; Bene — `BEN_*` в тех же точках; Harkonnen — `HAR_*` в тех же точках; Ordos — глаза `ORD_EYES01+…` в `(48,174)`, рот `ORD_MOUTH01+…` в `(52,207)`.
  - Фон по индексу `iBackgroundFrame` из gfxmentat (`AbstractMentat.cpp:516-520`); фон дома: `MENTATA` (Atreides), `MENTATM` (Bene), `MENTATH` (Harkonnen), `MENTATO` (Ordos) — числовые ID.
  - Заголовок HD: `drawHdTextHeader` — полоса из текстуры `MENTATA` (`:469-477`).
  - Подписи кнопок: `harmonizeHdButtonTextScale` — общий масштаб по всем кнопкам (`:479-514`).
  - Фон + «окно сцены»: `getHdForegroundLayer` (кэш копии фона как render target, `:538-557`); `clearHdMovieOpening` (`:559-579`), `clearHdForegroundLayerRegion` переводит прямоугольники из 640×480 в пиксели фона (`:581-605`); формы окна: Atreides `AtreidesMentat.cpp:73-118`, Ordos `OrdosMentat.cpp:57-117`.
  - Сцены: `AbstractMentat::loadScene` (`:645-675`), путь `data/scenes/hd4/sdl_{}.dat` (`:650`). Вызовы: `win01`, `win02`, `lose01`, `lose02` (`cGame_logic.cpp:1535-1547`), `platr`, `plhar`, `plord` (`:1582-1590`); `ini.cpp:690` — `pMentat->loadScene(scene)` с именем сцены из данных (не константа).
  - Файлы сцен в `origin/main`: `resources/bin/data/scenes/hd4/` — 18 файлов (`sdl_harvest`, `sdl_headqrts`, `sdl_hitcftry`, `sdl_hvyftry`, `sdl_ix`, `sdl_liteftry`, `sdl_lose01`, `sdl_lose02`, `sdl_ltank`, `sdl_palace`, `sdl_platr`, `sdl_plhar`, `sdl_plord`, `sdl_quad`, `sdl_repair`, `sdl_sardukar`, `sdl_win01`, `sdl_win02`).
  - Счётчики записей в паке (P11, `tests/data/hd4_packs_expected.tsv@832c953`): `win01`, `win02`, `lose01`, `lose02` — по 1; `platr`, `plhar`, `plord` — по 33.
- PORT (`832c953`, P11 `port-mentat.tsv`): `src/gameobjects/mentat/*.cpp`, 24 функции; `AbstractMentat::loadScene` `:346-364` использует `hd4SceneFile(scene)` и `kHd4AssetDensity = 4` (`src/gameobjects/mentat/AbstractMentat.cpp@832c953:346-364`); `draw_movie` `:322-331` (кадр `iMovieFrame`); Sardaukar: `draw_eyes` пустая (`SardaukarMentat.cpp@832c953:71-74`). Вызовы сцен: `cMentatState.cpp@832c953:111-131`, `cTellHouseState.cpp@832c953:73-81`.
- Тест форка `HdPresentationTests` (4 проверки: Menu, Gameplay, Mentat, Legacy) и `src/utils/HdPresentation.hpp` в PORT отсутствуют (P11 §5).
- Кадры сцены: `AbstractMentat::think*` — глаза, рот, фильм по 21 тику (P11 §2, `AbstractMentat.cpp@832c953:168-182`).

### Титры (`src/gamestates/cCreditsState.cpp/.h`, `origin/main`)
- Картинки: `credits_team.png` (948×624) и `credits_title.png` (1280×800) через `loadHdUiTexture` (`cCreditsState.cpp:24-33`). Резерв, если файла нет: записи пака `gfxinter` `CREDITS_DUNE2_CORE_TEAM` и `D2TM_TITLE` (`:36-41`).
- Раскладка (`:42-52`):
  - Командное фото: `x = W − team.w·1.1`, `y = H − team.h·1.1` (правый нижний угол; приведение к int).
  - Заголовок: `x = W/2 − title.w/2`, `y = m_crawlerY` (движется).
  - Текст прокрутки: начало `y = crawlerY + title.h`; строка с одним полем — центр; строка с двумя полями: `txt` с `x = halfScreen + 4`, `name` с `x = halfScreen − (nameW + 4)` (`:415-429`); шаг `line.height`.
  - Скорость `m_moveSpeed = 0.15f` (`:20`).
- Кнопка `BACK` / `НАЗАД` (`:54-70`): `x = 0`, `y = H − h`, `w = max(140, textLen + 24)`, `h = max(36, fontH + 10)`; тема `GuiTheme::Remaster()`; переход в `GAME_MENU` + затемнение.
- Порядок отрисовки (`draw :403-436`): командное фото → заголовок и прокрутка → кнопка Back → курсор.
- Не проверено: как `renderSprite` применяет плотность 4 к текстурам из `loadHdUiTexture` (масштаб на экране не проверен).
- P11 `credits.tsv` (2 256 строк, файл 1.2 MB): пять коммитов апстрима по `cCreditsState.cpp` (`d7b927d4`, `ea6bfc4a`, `5c77e8f9`, `ecfd4990`, `f1b8ea26`); 69 путей вне `src/` отсутствуют в FORK1 (P11 §3).
- В PORT класс тот же: ctor `cCreditsState.cpp@832c953:39-100`, draw `:441-469`; те же два HD-файла (P11 §3).

### Вступительный ролик (апстрим, P11 §4)
- Файл `src/VideoFlow.hpp` из задания не существует в UP1; фактический `src/game/VideoFlow.hpp@d06f2fc` (класс `:26`, `PlayCallback` `:28`, конструктор `:30`, `play` `:34`).
- Кнопка `Introduction` в главном меню: `cMainMenuState.cpp@d06f2fc:295,297` (`getType`), путь `intro.pak` и проверка `std::filesystem::exists` `:210-211`, клик `:214-221`.
- `cVideoState` (`cVideoState.cpp@d06f2fc`): кадр на `thinkNormal`, по окончании или клику/клавише → меню с затемнением (`:56-112`).
- Файл `intro.pak` в деревьях UP1 и PORT отсутствует (`git ls-tree` пуст) и в `origin/main` не найден (поиск по всему дереву).

---

## 7. Что каждый шаг П8, П9, П10, П11 приносит в интерфейс

### П8 — сохранения (по P8 RECON)
- Экраны и элементы: кнопка «Сохранения» в главном меню (`cMainMenuState.cpp:164-165`); кнопки «Загрузить игру» / «Сохранить игру» в меню настроек в игре (`cOptionsState.cpp:850-877`); диалог `SaveSlotsDialog` (10 слотов, поле имени, Save/Load/Close, статусы); клавиши F5/F9 (`cGame_logic.cpp:2042, 2057`).
- В UP1 (`d06f2fc`) и PORT: кнопок сохранения/загрузки в меню настроек нет (P8 §4); главное меню UP1 имеет кнопку `Load` (`cMainMenuState.cpp@d06f2fc:151-163`, P8 §5).
- Файлы порта (отсутствуют в UP1 по карте переноса, P8 §8): `src/save/SaveFileCodec.{cpp,hpp}`, `SaveGameManager.{cpp,hpp}`, `SaveSlotName.hpp`, `SaveSlotsDialog.{cpp,hpp}`; тесты `tests/SaveFileCodecTests.cpp`, `tests/SaveSlotNameTests.cpp`.
- Риск из карты (P8 §5/§8): `SaveGameManager.cpp@9208dcf:9` подключает старый `cGame.h`; API `cGame` в UP1 — `src/game/cGame.h@d06f2fc:89`.
- Формат: `FormatVersion = 2` (P8 §8); сохранения `v0.8.0-ru-hd.7` объявлены несовместимыми (Р5, `docs/decisions.md` по P8 §Чтение).
- Настройки (P8 §5–6): `preferences.ini` (новое в UP1, `src/game/Preferences.cpp`, `PreferencesPath.cpp`, `src/main.cpp:54`); в PORT вместо `ScalingMode` (UP1) — `RenderScale`; `WorldScale` читается, не пишется (`preferences.tsv`).
- Места кода, которые П8 описывает (P8 §4–6): `src/main.cpp` (каталог exe через `SDL_GetBasePath`, `:34-49,85`; загрузка settings.ini `:92`), `src/utils/common.cpp` (чтение/запись settings.ini), `src/gamestates/cOptionsState.cpp` (вызовы `:104,500,728`), `cMainMenuState.cpp` (`:164-165`), `src/cGame_logic.cpp` (F5/F9 `:2042-2059`). Правки форка вне `src/save/` по P8 §3 затрагивают `cUnit.h` и `cPlayer.h` (не UI).

### П9 — музыка на SDL3_mixer (по P9 RECON, PORT `616280c`)
- Экраны и элементы: панель музыки в верхней полосе боя (`MusicControlsLayout`, `cDrawManager::drawMusicControls`); сообщение справа от панели (`cMessageDrawer`); клавиши `[`, `]`, `M`, `O`, `P` (`cGame_logic.cpp:2092-2117`).
- Файлы форка: `src/audio/MusicController.{h,cpp}`, `src/audio/MusicPlaylist.{h,cpp}`, `src/audio/MusicTransitionPolicy.hpp`, `src/sidebar/MusicControlsLayout.hpp`, `src/cGame_logic.cpp` (категории `:96-116`, выбор `:1116-1153`, переходы `:2229-2267`), `src/drawers/cMessageDrawer.cpp`, `src/managers/cDrawManager.{h,cpp}`, `src/utils/cSoundPlayer.{h,cpp}`, `src/player/cPlayer.{h,cpp}`, `CMakeLists.txt`, тесты музыки.
- Апстрим (UP1, P9 §4): `src/context/MusicJukeBox.cpp`, `AudioContext.cpp`; создание папок `audio/win`, `audio/lose`, `audio/attack`, `audio/peace`, `audio/menu`, `audio/conquest`, `audio/briefing/{atreides,harkonnen,ordos,sardaukar}` при старте (`6f41fdc3`).
- Ресурсы: в PORT `616280c` и в дереве `resources/bin` нет ни одного музыкального файла (P9 §4, пустой вывод `git ls-tree`).
- Настройки (P9 §6): `playMusic`, `playSound`, `customMusic`, `playCreditsSound` — в PORT `settings.ini` и `preferences.ini`; `customMusic` в FORK1 не найден.
- Меню настроек (раздел 4): `Music`, `Volume`, `Sound`, `Volume` — уже в форке (`cOptionsState.cpp:897-1023`).

### П10 — приказы и управление (по P10 RECON, PORT `832c953`)
- Экраны и элементы: панель приказов (7 кнопок, раздел 1); вкладка `Controls` меню настроек (раздел 4); режимы приказов (ForceAttack, Rally, Repair; правый клик отменяет); очередь Starport (`ORDER`); сообщения лимита юнитов.
- Файлы изображений, которых нет в PORT (P10 §2): `resources/bin/data/hd4/command_bar.png`, `resources/hd/master4/command_bar.png`, `resources/hd/master4/command_bar_disabled.png`, `resources/hd/source_references/command_bar_bronze_reference.png`, `resources/hd/source_references/command_bar_color_reference.png`; `resources/bin/settings.ini` есть в PORT, но отличается.
- Конфиг (P10 §2): в FORK1 `Language=ru` и `KeyAttack…KeyRelease`; в PORT — секция `[KEYS]` с другими правилами (diff `9208dcf..832c953`, P10 §2).
- Файлы кода форка: `src/controls/CommandBindings.hpp`, `CommandModePolicy.hpp`, `src/drawers/cCommandBarDrawer.{h,cpp}`, `CommandBarLayout.hpp`, `CommandBarPolicy.hpp`, `OrderButtonPolicy.hpp`, `src/gamestates/cOptionsState.{h,cpp}`, `src/utils/common.cpp`, `src/controls/cGameControlsContext.cpp`, `src/controls/mousestates/cMouseUnitsSelectedState.cpp`, `cMouseNormalState.cpp`, `src/cGame_logic.cpp:2078, 2157`.
- Starport (P10 §6): `src/gameobjects/structures/StarportOrderQueue.hpp` (новый в форке, в PORT отсутствует); `cOrderProcesser.{h,cpp}`, `cStarPort.cpp`, `src/sidebar/cBuildingListUpdater.cpp` (в PORT указательная версия).
- Предел юнитов (апстрим, P10 §7): уже есть в UP1 и PORT. Сообщение `"Unable to create more."` (`src/building/cItemBuilder.cpp:202-209`, `src/sidebar/cSideBar.cpp:111`); отметка `Max built` (`src/drawers/cBuildingListDrawer.cpp:381-391`, PORT `:382-392`); меняется строка вызова в `cPlayer.cpp` (`@d06f2fc:1395`, `@832c953:1402`). Константа `cUnits::MAX_UNITS_CAPACITY = 300` (`cUnits.h:70`); `MaxUnits` в `.ini` карт — в `src` чтения не найдено (P10 §7).

### П11 — ментаты HD, титры, вступительный ролик (по P11 RECON, PORT `832c953`)
- Экраны и элементы: ментат (4 дома, фон, рот, глаза, кнопки, фильм), титры (два HD-изображения, прокрутка, кнопка Back), вступительный ролик (кнопка «Introduction» в главном меню, `cVideoState`).
- Файлы форка: `src/mentat/*` (`AbstractMentat`, `AtreidesMentat`, `BeneMentat`, `HarkonnenMentat`, `OrdosMentat`); PORT: `src/gameobjects/mentat/*`; `src/gamestates/cCreditsState.{cpp,h}`; `src/cGame_logic.cpp` (вызовы `loadScene`).
- Апстрим: `src/game/VideoFlow.hpp`, `src/gamestates/cVideoState.{cpp,h}`, `src/gamestates/cMainMenuState.cpp` (кнопка Introduction), `src/game/cGame.h`, `src/game/cGame_logic.cpp`, `src/eGameState.{h,cpp}` (состояние `VIDEO`), `src/include/sGameServices.h`, `src/gamestates/cCreatorState.*`, `cSelectYourNextConquestState.*` (21 исходный файл по P11 §4).
- Ресурсы: `intro.pak` отсутствует в UP1 и PORT (P11 §4); титры — `resources/bin/data/hd4/credits_team.png`, `credits_title.png` (раздел 9).
- Тесты: `tests/HdPresentationTests.cpp` (4 проверки) — только FORK1 (P11 §5).

---

## 8. Русский язык и шрифты форка

### Языки
- Отдельных языковых файлов нет: `git ls-tree -r --name-only origin/main | grep -i -E "lang|locale|strings"` дал только файлы шрифтов (см. ниже), строк перевода в файлах нет.
- Строки в коде: 281 вызов `localization::text(en, ru)` и `localization::format(en_fmt, ru_fmt, …)` в 34 файлах `src` (`git grep -c`).
- Механизм (`src/utils/Localization.hpp:9-46`): глобальный `bool english`; `setLanguage(lang)`: `english = (lang == "en" || "EN")` (`:13-16`); `text()` выбирает строку (`:18-23`); `campaignRoot()` → `"campaign_en"` или `"campaign"` (`:30-33`).
- Выбор языка при старте: `src/cGame_logic.cpp:187` — `localization::setLanguage(gs->language)`.
- Ключ: `resources/bin/settings.ini:10` — `Language=ru`. Если значение не `en` и не `ru`, меню приводит его к `ru` (`src/gamestates/cOptionsState.cpp:106-108`); `m_savedLanguage` по умолчанию `"ru"` (`cOptionsState.h:74`).
- Переключатель: строка Language на главной странице меню настроек (раздел 4, `:1310-1346`, `toggleLanguage :644-656`); применяется через кнопку Apply с перезапуском (`:734-754`).
- Кампания по языку: каталоги `resources/bin/campaign/` (ru) и `resources/bin/campaign_en/` (en) (`git ls-tree`).

### Шрифты в `resources/bin/data/` (`git ls-tree -r -l origin/main`)

| Файл | Размер в дереве | Фактически | Ссылки в коде |
|---|---:|---|---|
| PTMono-Regular.ttf | 185 912 | файл | `settings.ini [FONT]` ARRAKEEN и SMALL; `tests/FontCoverageTests.cpp:21` (fallback) |
| PTSansNarrow-Regular.ttf | 131 | LFS-указатель, объект 396 212 Б | `settings.ini [FONT]` BENEGESS |
| RussoOne-Regular.ttf | 130 | LFS-указатель, объект 39 124 Б | `ContextCreator.cpp:84` (mentat HD) |
| Sangyo-Regular.otf | 133 248 | файл | `ContextCreator.cpp:83`; `tests/FontCoverageTests.cpp:18` |
| RunttiSP-Bold.otf | 166 328 | файл | ссылок в `src`, `tests`, `tools` не найдено |
| arrak.ttf | 56 600 | файл | ссылок не найдено |
| arrakeen.fon | 7 776 | файл | в `origin/main` не назначен (настройки PTMono); упоминание только в комментариях `cFileValidator.cpp:11` |
| benegess.fon | 5 936 | файл | не назначен; комментарий `cFileValidator.cpp:12` |
| benegess.ttf | 15 932 | файл | ссылок не найдено |
| small.ttf | 19 492 | файл | не назначен; комментарий `cFileValidator.cpp:13` |

- `settings.ini` (origin/main): `[FONT]` строки 79–82: `ARRAKEEN=PTMono-Regular.ttf`, `BENEGESS=PTSansNarrow-Regular.ttf`, `SMALL=PTMono-Regular.ttf`. Значения читаются в `cGame_logic.cpp:1043-1045`.

### Выбор шрифтов (`src/context/ContextCreator.cpp`)
- Русский: `useRussianFont = !localization::isEnglish() && существует Sangyo-Regular.otf` (`:82-86`).
- `openLocalizedFont(fallback, pointSize, role, fallbackFont)` (`:88-131`): основной = Sangyo (если русский), иначе настроенный; если Sangyo не открылся — настроенный (`:101-114`); если Sangyo открылся — запасной `fallbackFont` = настроенный (`:115-119`).
- Размеры (умножаются на `density`): игровой `game_font` (ARRAKEEN) 12 (`:133-135`); `bene_font` (BENEGESS) 12 (`:143-145`); `small_font` (SMALL) 12 (`:153-155`); `menu_font` (BENEGESS) 24 (`:163-165`); `mentat_hd_font` (`russoFontPath` = RussoOne) 20 (`:187-189`); при его отсутствии — BENEGESS 20 × density (`:198-201`).
- Запасной шрифт для знаков (`cTextDrawer::shouldUseFallback`, `src/drawers/cTextDrawer.cpp:32-47`): если задан fallback и основной шрифт не содержит глифы строки, а fallback содержит — строка рисуется fallback. Результат кэшируется по тексту (`:36-41`). Проверка глифов: `src/utils/FontSupport.hpp:8-54` (`TTF_GlyphIsProvided32`; пробел, tab, CR, LF пропускаются).
- Итог по коду: для русского интерфейса запасной шрифт — настроенный из `[FONT]` (PTMono / PTSansNarrow). Для английского основной = настроенный, запасного нет.
- Для mentat: запасной = RussoOne, если Sangyo открылся (`openLocalizedFont` с `fallback = russoFontPath`).
- Тест: `tests/FontCoverageTests.cpp:16-58` проверяет Sangyo на русских строках и PTMono как fallback.

### Лицензии
- Sangyo: `resources/bin/data/licenses/Sangyo-LICENSE.txt` (4 301 Б), `Sangyo-COPYRIGHT.txt` (38 Б).
- PT-шрифты (PTMono, PTSansNarrow): `resources/bin/OFL_PT_FONTS.txt` (4 586 Б).
- RussoOne: `resources/bin/data/OFL_RUSSO_ONE.txt` (4 389 Б).
- RunttiSP: `resources/bin/data/licenses/RunttiSP-ReadMe.pdf` (587 680 Б) — только readme, не читался.
- Лицензий для `arrak.ttf`, `arrakeen.fon`, `benegess.fon`, `benegess.ttf`, `small.ttf` в `origin/main` не найдено (поиск `licen|OFL|font|copying|notice` по дереву).
- `resources/bin/README_RU.txt` (19 939 Б) не проверялся на упоминания шрифтов.

---

## 9. Картинки интерфейса форка (`resources/bin/data/hd4`)

- `git ls-tree -r -l origin/main -- data/hd4 resources/bin/data/hd4`: путь `data/hd4` в дереве отсутствует; записей 14, все в `resources/bin/data/hd4/`.
- Все 14 — LFS-указатели (blob 130–132 байта: `version https://git-lfs.github.com/spec/v1`). Реальные файлы — в LFS-кэше `C:/Users/Slaven/Projects/DUNE/.git/lfs/objects/<oid[0:2]>/<oid[2:4]>/<oid>`, все 14 найдены. Размеры и PNG-заголовки прочитаны из кэша (`IHDR`).
- Загрузка в игре — `data/hd4/<имя>` относительно рабочего каталога (раздел 1, `HdUiTextureLoader.cpp:22`).

| Файл | blob, байт | Реальный размер, байт | PNG, px | Цвет | Использование |
|---|---:|---:|---|---|---|
| campaign_map.png | 132 | 4 541 123 | 2432×960 | RGB (тип 2) | `cSelectYourNextConquestState.cpp:94` |
| command_bar.png | 132 | 1 219 692 | 2800×414 | RGBA (6) | `cCommandBarDrawer.cpp:41` |
| command_bar_disabled.png | 131 | 952 143 | 2800×414 | RGBA | `cCommandBarDrawer.cpp:46` |
| credits_team.png | 131 | 292 900 | 948×624 | RGBA | `cCreditsState.cpp:25` |
| credits_title.png | 131 | 113 285 | 1280×800 | RGBA | `cCreditsState.cpp:30` |
| hud_house_atreides.png | 131 | 237 299 | 384×384 | RGBA | `cSideBarDrawer.cpp:32`; `cSelectYourNextConquestState.cpp:99` |
| hud_house_harkonnen.png | 131 | 258 354 | 384×384 | RGBA | `cSideBarDrawer.cpp:37`; `cSelectYourNextConquestState.cpp:101` |
| hud_house_ordos.png | 131 | 265 207 | 384×384 | RGBA | `cSideBarDrawer.cpp:42`; `cSelectYourNextConquestState.cpp:104` |
| main_menu_background.png | 132 | 5 094 199 | 5120×1440 | RGB (2) | `cChooseHouseState.cpp:31`; `cMainMenuState.cpp:48`; `cSelectMissionState.cpp:21`; `cSelectYourNextConquestState.cpp:89` |
| main_menu_logo.png | 131 | 254 231 | 1792×320 | RGBA | `cMainMenuState.cpp:53` |
| outcome_defeat_en.png | 132 | 6 403 321 | 2752×1536 | RGBA | `cGame_logic.cpp:2546` (список исходов) |
| outcome_defeat_ru.png | 132 | 6 446 955 | 2752×1536 | RGBA | `cGame_logic.cpp:2547` |
| outcome_victory_en.png | 132 | 7 431 127 | 2752×1536 | RGBA | `cGame_logic.cpp:2542` |
| outcome_victory_ru.png | 132 | 7 459 732 | 2752×1536 | RGBA | `cGame_logic.cpp:2543` |

- Раскладка `command_bar.png`: 7 ячеек по 400 px (2800/7), высота 414 (`cCommandBarDrawer.cpp:132-139`).
- Для сравнения: в `resources/hd/` в `origin/main` 1723 файла (не разбирались); в P10 §2 перечислены ещё четыре `command_bar`-файла из `resources/hd/master4` и `source_references`.

---

## Не найдено и не проверено (сводно)
- Реальный запуск и скриншоты не делались. Все размеры экрана — расчёт по формулам кода.
- Масштабирование HD-текстур на экране (плотность 4) не проверялось.
- Сборки, тесты и `ctest` не запускались.
- Раздел 7 опирается на документы разведки L (P8–P11); их факты не перепроверялись в `origin/main`, кроме прямо процитированных мест.
