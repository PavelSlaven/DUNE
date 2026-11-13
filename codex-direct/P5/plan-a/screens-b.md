Сейчас только чтение и таблица; файлы вне `.tmp/p5a/plan/` не меняй, сборку не запускай

## Главное меню

Каждая строка ниже соответствует одному hunk полного вывода `git diff BASE FORK1 -- src/gamestates/cMainMenuState.cpp` или его заголовка. Портовые действия, ввод, переходы и английские названия остаются из кода порта.

| Файл форка и диапазон строк | Что делает блок | Решение и место в порту |
|---|---|---|
| `cMainMenuState.cpp`, 1–313 | Вместо фиксированной рамки строит адаптивную панель и кнопки; загружает HD фон и логотип, выбирает логотип, рисует их; задаёт тему кнопок. В том же блоке форк добавляет Multiplayer, Saved games, локализованные строки и диалог сохранений. | Переносится в П5а в `cMainMenuState::cMainMenuState`, новый `buildHdMenu()` и `draw()`/новый `drawHdBackground()`; портовые действия и их подписи остаются. Multiplayer не добавляется, поскольку его нет в портовой логике; Saved games относится к П8, переводы — к П7. `getMenuTextDrawer()` из форка в порту отсутствует; используется существующий портовый рисовальщик. Фон при отсутствии текстуры остаётся отсутствующим, для логотипа сохраняется fallback на портовый `BMP_D2TM`. Общие формулы адаптивной панели и кнопок переносятся без изменения. Производная от сохранённых восьми портовых кнопок величина `buttonCount` равна 8 вместо 7 у форка, чтобы расчёт панели охватывал все восемь действий. |
| `cMainMenuState.cpp`, 317–350 | Меняет обработку клавиатуры и добавляет ввод текста для диалога сохранений. | Не переносится: ввод и игровая логика остаются портовыми; ввод текста для SaveSlotsDialog относится к П8. Место в порту — существующая `cMainMenuState::onNotifyKeyboardEvent()`. |
| `cMainMenuState.h`, 7–18 | Добавляет типы и указатель SaveSlotsDialog. | Не переносится, П8: в порту `cMainMenuState.h` не добавляется член SaveSlotsDialog или типы только для него. |
| `cMainMenuState.h`, 24–39 | Добавляет `onTextInput`, функции сборки меню и фона, а также доступ UiAudit. | `buildHdMenu()` и `drawHdBackground()` переносятся в П5а в `cMainMenuState`; `onTextInput` относится к П8, `UiAuditAccess` — к П5г. |
| `cMainMenuState.h`, 43–57 | Добавляет мета-рисовальщик, прямоугольник логотипа и указатели HD-фона/логотипа; также указатель SaveSlotsDialog. | `m_logoRect`, `m_hdMenuBackground` и `m_hdMenuLogo` переносятся в П5а в `cMainMenuState`; `m_metaTextDrawer`/`getMenuTextDrawer()` не переносятся, поскольку такого метода в порту нет; указатель SaveSlotsDialog не переносится, П8. |

**Прямоугольники восьми действий портового меню.** Для всех строк используется прямоугольник форка `cRectangle(buttonX, buttonY + row * (buttonHeight + buttonGap), buttonWidth, buttonHeight)`, где `buttonX = panelX + panelPadding` и `buttonY = panelY + panelPadding`. Порядок кнопок и подписи остаются портовыми; производное значение `buttonCount = 8` включает Map Editor и Introduction.

| Действие порта | Строка | Прямоугольник при 800×600 | Прямоугольник при 2133×600 |
|---|---:|---|---|
| Campaign | 0 | `cRectangle(260, 148, 280, 40)` | `cRectangle(886, 148, 360, 40)` |
| Skirmish | 1 | `cRectangle(260, 194, 280, 40)` | `cRectangle(886, 194, 360, 40)` |
| Load | 2 | `cRectangle(260, 240, 280, 40)` | `cRectangle(886, 240, 360, 40)` |
| Map Editor | 3 | `cRectangle(260, 286, 280, 40)` | `cRectangle(886, 286, 360, 40)` |
| Options | 4 | `cRectangle(260, 332, 280, 40)` | `cRectangle(886, 332, 360, 40)` |
| Hall of Fame | 5 | `cRectangle(260, 378, 280, 40)` | `cRectangle(886, 378, 360, 40)` |
| Introduction | 6 | `cRectangle(260, 424, 280, 40)` | `cRectangle(886, 424, 360, 40)` |
| Exit | 7 | `cRectangle(260, 470, 280, 40)` | `cRectangle(886, 470, 360, 40)` |

| Портовый элемент без аналога у форка | Прямоугольник и место в порту |
|---|---|
| Map Editor | Строка 3 общей формулы действия выше; обработчик остаётся в `cMainMenuState::cMainMenuState()`. |
| Introduction | Строка 6 общей формулы действия выше; сохраняются портовая проверка `intro.pak` и обработчик в `cMainMenuState::cMainMenuState()`. |
| Load | Строка 2 общей формулы действия выше; кнопка и её портовый обработчик остаются, а Saved games из форка относится к отдельной функции П8. |
| Дата сборки | Остаётся в `cMainMenuState::draw()`; `drawTextBottomRight(D2TM_BUILD_DATETIME, 20)` задаёт `cRectangle(getScreenW() - getTextLength(D2TM_BUILD_DATETIME) - 20, getScreenH() - getFontHeight() - 40, getTextLength(D2TM_BUILD_DATETIME), getFontHeight())`. |
| Отладочная сетка `DEBUG` | Остаётся в `cMainMenuState::draw()` под `isDebugMode()`; `cRectangle(0, 0, getScreenW(), getScreenH())`. |

Статус fork-only элементов: Multiplayer не добавляется, поскольку его нет в портовой логике; Saved games не переносится, П8. Портовые `Load` и `Options` сохраняют исходные подписи и действия.

## Выбор Дома

Каждая строка соответствует одному hunk полного вывода `git diff BASE FORK1 -- src/gamestates/cChooseHouseState.cpp` или его заголовка. Портовый порядок карточек и обработчики выбора дома сохраняются.

| Файл форка и диапазон строк | Что делает блок | Решение и место в порту |
|---|---|---|
| `cChooseHouseState.cpp`, 1–7 | Добавляет загрузчик HD-текстуры, локализацию и импорт аудита. | Загрузчик — П5а в `cChooseHouseState::cChooseHouseState()` и `draw()`; локализация — П7; `UiAudit` — П5г. Английские строки порта остаются. |
| `cChooseHouseState.cpp`, 10–89 | Удаляет старые отдельные спрайты Dune/заголовка, загружает HD-фон и рассчитывает карточки и кнопку Back. Форк рассчитывает три карточки и выбирает новый текстовый рисовальщик. | Переносится в П5а в `cChooseHouseState::cChooseHouseState()`: фон, прямоугольники карточек и Back. Для карточек применяется заданная в задании формула четырёх домов, с порядком портовых полей Атрейдесы, Ордосы, Харконнены, Сардаукары; прямоугольники приведены ниже. Портовый asset Сардаукаров сохраняется в четвёртой карточке. `getMenuTextDrawer()` в порту отсутствует, остаётся портовый рисовальщик; источник игрового выбора и обработчики порта остаются. |
| `cChooseHouseState.cpp`, 91–99 | Освобождает загруженный HD-фон, оставляя заимствованные гербы не принадлежащими состоянию. | Переносится в П5а в `cChooseHouseState::~cChooseHouseState()`; в порту состояние удаляет HD-фон, гербы из `gfxinter` не удаляет. |
| `cChooseHouseState.cpp`, 108–299 | Рисует HD-фон, заголовок, карточки и кнопку Back; добавляет hover-подсветку карточек и блоки ui-audit. | Рисование HD-фона и карточек переносится в П5а в `cChooseHouseState::draw()` и новые `drawHdBackground()`/`drawHdHouseCard()`. В качестве подписей остаются английские строки порта; переводы — П7. `ui-audit` не переносится, П5г. Hover-код для карточек не переносится: обработка событий остаётся портовой; портовая подсветка Back сохраняется. |
| `cChooseHouseState.cpp`, 343–358 | Добавляет отслеживание наведённой карточки в `onMouseMoved()`. | Не переносится: событие мыши и ввод остаются портовыми. Порт уже обрабатывает щелчки по четырём карточкам и подсветку Back в `cChooseHouseState::onMouseMoved()`. |
| `cChooseHouseState.h`, 30–58 | Заменяет поля старых картинок на HD-фон, добавляет hover-поле и функции рисования карточек/фона. | HD-фон и методы рисования переносятся в П5а в `cChooseHouseState`; `m_hoveredHouse` не добавляется, поскольку hover-обработка карточек не переносится. Портовые поля гербов четырёх домов остаются. |

| Портовый элемент без аналога у форка | Прямоугольник и место в порту |
|---|---|
| Карточка Сардаукаров | Портовый четвёртый дом остаётся в `cChooseHouseState::draw()` и обработчике выбора; прямоугольники `cRectangle(595, 100, 171, 360)` при 800×600 и `cRectangle(1534, 100, 420, 360)` при 2133×600, согласно строке «Сардаукары» таблицы прямоугольников ниже. |

### Прямоугольники карточек

Расчёт использует ровно заданные формулы: `gap = clamp(W / 48, 16, 32)`, `horizontalMargin = clamp(W / 24, 28, 72)`, `availableCardWidth = (W - horizontalMargin * 2 - gap * 3) / 4`, `cardWidth = clamp(availableCardWidth, 160, 420)`, `cardsWidth = cardWidth * 4 + gap * 3`; `cardsY`, `backY`, высота карточки и формула `firstX` — как в `FORK1`.

| Холст | Значения раскладки | Атрейдесы | Ордосы | Харконнены | Сардаукары |
|---|---|---|---|---|---|
| 800×600 | `gap=16`, `horizontalMargin=33`, `availableCardWidth=171`, `cardWidth=171`, `cardsWidth=732`, `firstX=34`, `cardsY=100`, `cardHeight=360` | `cRectangle(34, 100, 171, 360)` | `cRectangle(221, 100, 171, 360)` | `cRectangle(408, 100, 171, 360)` | `cRectangle(595, 100, 171, 360)` |
| 2133×600 | `gap=32`, `horizontalMargin=72`, `availableCardWidth=473`, `cardWidth=420`, `cardsWidth=1776`, `firstX=178`, `cardsY=100`, `cardHeight=360` | `cRectangle(178, 100, 420, 360)` | `cRectangle(630, 100, 420, 360)` | `cRectangle(1082, 100, 420, 360)` | `cRectangle(1534, 100, 420, 360)` |

## Выбор миссии

Каждая строка соответствует одному hunk полного вывода `git diff BASE FORK1 -- src/gamestates/cSelectMissionState.cpp` или его заголовка. Логику кампании, разблокировки миссий, переходы и обработчики порта сохраняем; применяем только геометрию, HD-фон и оформление общих кнопок.

| Файл форка и диапазон строк | Что делает блок | Решение и место в порту |
|---|---|---|
| `cSelectMissionState.cpp`, 5–49 | Загружает HD-фон, задаёт размеры и центр панели, высоты/ширины кнопок и тему Remaster; меняет текстовый контекст на новый `getMenuTextDrawer()`. | Переносится в П5а в `cSelectMissionState::cSelectMissionState()` и `draw()`: фон и геометрия окна. Настройки экрана читаются через `m_settings->getScreenW()/getScreenH()`. Тема применяется к кнопкам порта. `getMenuTextDrawer()` в порту отсутствует, поэтому остаётся портовый текстовый рисовальщик; английские подписи остаются, локализация — П7. |
| `cSelectMissionState.cpp`, 52–67 | Меняет отступ и оформление кнопок в цикле миссий; меняет подписи на локализуемые. | В П5а переносится только оформление `GuiTheme::Remaster()`/`REMASTER_BUTTON` к существующим кнопкам порта в `cSelectMissionState::cSelectMissionState()`. Генерация миссий, текст и переходы сохраняются из порта; локализация относится к П7. |
| `cSelectMissionState.cpp`, 78–87 | Меняет подпись и тему кнопки Back. | В П5а переносится оформление Remaster на портовую кнопку Back в конструкторе; английская подпись `Back` и портовый обработчик остаются. Положение порта ограничивается окном нового размера: `gui_window->getRelativeRect(mainMenuWidth - 70, mainMenuHeight - 30, 55, 22)`. Перевод — П7. |
| `cSelectMissionState.cpp`, 92–98 | Удаляет загруженный HD-фон при уничтожении состояния. | Переносится в П5а в `cSelectMissionState::~cSelectMissionState()`. |
| `cSelectMissionState.cpp`, 102–151 | Рисует очистку, HD-фон с сохранением пропорций и затемнение панели перед содержимым окна. | Переносится в П5а в начало `cSelectMissionState::draw()`; при `nullptr` фон не рисуется, остальной экран продолжает работу. |
| `cSelectMissionState.h`, 9–15 | Добавляет forward declaration `class Texture;` перед объявлением состояния. | Не дублируется: в порту уже есть `class Texture;` в `src/gamestates/cSelectMissionState.h:33`; декларации достаточно для указателя HD-фона из следующего hunk. |
| `cSelectMissionState.h`, 28–32 | Добавляет поле `Texture *m_hdBackground` с начальным значением `nullptr`. | Переносится в П5а в приватные поля `cSelectMissionState` рядом с `m_houseFlag`; текстура принадлежит состоянию и удаляется в `cSelectMissionState::~cSelectMissionState()`. |
| Портовый элемент без аналога у форка: заголовок кампании | Остаётся в title bar окна `cRectangle(mainMenuFrameX, mainMenuFrameY, mainMenuWidth, mainMenuHeight)`; текст и обработка принадлежат порту. |
| Портовый элемент без аналога у форка: герб выбранного Дома | Остаётся в `cSelectMissionState::draw()` в `cRectangle(m_flagX, m_flagY, m_flagWidth, m_flagHeight)`; исходное позиционирование портового герба остаётся в левой половине окна. |
| Портовый элемент без аналога у форка: Continue | Остаётся в `cSelectMissionState::cSelectMissionState()` в `cRectangle(mainMenuFrameX + 25, mainMenuFrameY + 340, 270, buttonHeight)`; переход кампании остаётся портовым. |
| Портовый элемент без аналога у форка: заголовок Replay Mission | Остаётся в `cSelectMissionState::draw()` в `cRectangle(rightButtonX, mainMenuFrameY + 42, 270, getFontHeight())`, где `rightButtonX = mainMenuFrameX + mainMenuWidth - 25 - 270`. |
| Портовый элемент без аналога у форка: список доступных для повтора миссий | Кнопка миссии `i` остаётся в `cSelectMissionState::cSelectMissionState()` в `cRectangle(rightButtonX, mainMenuFrameY + 62 + (i - 1) * 38, 270, 34)`, где `rightButtonX = mainMenuFrameX + mainMenuWidth - 25 - 270`; список определяется данными кампании порта. |

## Титры

Каждая строка соответствует одному hunk полного вывода `git diff BASE FORK1 -- src/gamestates/cCreditsState.cpp` или его заголовка. Список прокручиваемых портовых титров, скорость и обработчики остаются портовыми.

| Файл форка и диапазон строк | Что делает блок | Решение и место в порту |
|---|---|---|
| `cCreditsState.cpp`, 1–47 | Загружает HD изображения команды и титульной надписи с fallback на картинки HD4, задаёт позицию изображения команды; меняет рисовальщик и добавляет локализацию/аудит. | Загрузчик, fallback и расчёт позиции переносятся в П5а в `cCreditsState::cCreditsState()`. `getMenuTextDrawer()` из форка в порту отсутствует, остаётся портовый рисовальщик; английские подписи остаются портовыми, локализация — П7; `UiAudit` — П5г. Загруженные HD-текстуры принадлежат состоянию, fallback-картинки `gfxinter` заимствуются. |
| `cCreditsState.cpp`, 51–68 | Рассчитывает прямоугольник Back и применяет тему Remaster; текст кнопки локализуется. | В П5а переносится прямоугольник и тема в `cCreditsState::cCreditsState()`, с английской подписью `Back` и портовым обработчиком; прямоугольник — `cRectangle(0, getScreenH() - max(36, getFontHeight() + 10), max(140, getTextLength("Back") + 24), max(36, getFontHeight() + 10))`. Локализация — П7. |
| `cCreditsState.cpp`, 376–388 | Удаляет только HD-картинки, загруженные самим состоянием. | Переносится в П5а в `cCreditsState::~cCreditsState()`; заимствованные `gfxinter` картинки не удаляются. |
| `cCreditsState.cpp`, 402–411 | Заменяет изображение Dune на картинку команды; в тот же блок форк добавляет ui-audit запись. | Рисование HD-картинки команды переносится в П5а в `cCreditsState::draw()`; запись `ui-audit` не переносится, П5г. Рисование титульной картинки и прокрутка текста остаются. |
| `cCreditsState.h`, 23–29 | Добавляет доступ UiAuditAccess в публичную часть состояния. | Не переносится, П5г. |
| `cCreditsState.h`, 46–56 | Заменяет координаты/указатель Dune полями изображения команды и флагами владения HD-текстурами. | Переносится в П5а в `cCreditsState.h`; портовый список строк прокрутки не меняется. |
