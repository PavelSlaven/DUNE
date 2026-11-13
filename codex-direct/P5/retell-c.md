## DONE-P5C-RETELL | Tue Nov 10 18:44:33 UTC 2026

**Цель:** перенести на боевой экран HD HUD форка по раскладке `HudLayout`, сохранив указанное поведение апстрима и добившись прохождения приёмочных проверок без изменения тестов.

Для выполнения P5C я сначала прочёл бы весь перечисленный материал: тест `test_HudLayout.cpp`, таблицы разведки, исходники порта и указанные файлы форка. Каждый файл и каждый вывод `git show` следовало бы читать отдельным вызовом; перед командами Git — добавить в `PATH` указанный Git LFS. Затем выполнил бы шаги 1–9, а после них — проверки шага 10. В конце сверил бы diff с планом, слиянием `drawList` и требованиями сохранить поведение апстрима, затем сдал бы результат без коммитов.

Шаги 1–4 выполняла бы дорожка A; 5, 6 и 8 — дорожка B; 7, 9 и слияние `drawList` — дорожка C. Эти три дорожки работают параллельно, не дожидаясь друг друга. Дорожка D проверяет результат после завершения A, B и C. В самом задании сказано о трёх субагентах, но названы четыре роли — A, B, C и D. Я бы понял это как трёх помощников всего: A, B и C работают параллельно, а после завершения их дорожек один освободившийся помощник выполняет проверки в роли D. Всего одновременно — не более трёх помощников.

### Шаги PLAN-P5C

1. **`src/sidebar/HudLayout.hpp` — новый файл.** Скопировать его дословно из указанной ревизии форка. В нём появятся `HudLayout::TopBarHeight`, поля размеров и прямоугольников раскладки, `create`, `visibleRows`, `totalRows`, `maxScrollRow`, `cardRect`, `tabRect` и `scrollbarThumb`. Файла `.cpp` нет, поэтому заголовок не добавляется ни в `src/CMakeLists.txt`, ни в `tests/CMakeLists.txt`. Остальные файлы на этом шаге не меняются.

2. **`src/sidebar/cSideBar.h`, `src/sidebar/cSideBar.cpp`.** В заголовке заменить две ширины боковой панели на изменяемые `inline static int` с начальными значениями 200 и `SidebarWidthWithoutCandyBar + VerticalCandyBarWidth`; объявить `configureLayout` после `TopBarHeight`. В `.cpp` подключить `HudLayout.hpp`, добавить указанное тело `configureLayout` в конце файла и после блока проверки `isMouseOnSidebarOrMinimap()` добавить передачу события в `getBuildingListDrawer()->onNotifyMouseEvent(event)`. Существующие действия `cSideBar` при кликах, в частности пауза и возобновление строительства, сохраняются.

3. **`src/game/cGame_logic.cpp`, `src/gamestates/cGamePlaying.cpp`.** После установки высоты экрана в `cGame::setupGame` вызвать `cSideBar::configureLayout` с шириной и высотой из настроек. В `cGamePlaying::onNotifyMouseEvent` пропускать через камеру все события, кроме прокрутки колеса над боковой панелью или мини-картой. Камера и её обработчик остаются прежними; колесо над боевым полем продолжает менять приближение.

4. **`src/managers/cDrawManager.h`, `src/managers/cDrawManager.cpp`.** Заменить тело `drawTopBarBackground` кодом форка с тёмной полосой на всю ширину, бронзовой линией и кнопкой `OPTIONS` в прямоугольнике `(7, 4, 126, 33)`. Клик открывает настройки через `setNextState(GAME_OPTIONS)`, текст рисуется через `drawTextCenteredInBox`. Удалить вызов и функцию `drawOptionBar`, её объявление, поле и создание `m_btnOptions`, а также `houseChanged` и связанное пересоздание кнопки в `setPlayerToDraw`. Слои боя остаются в прежнем порядке; музыкальные элементы, регулятор скорости и строка сообщений относятся к следующим шагам и здесь не переносятся.

5. **`src/drawers/cMiniMapDrawer.h`, `src/drawers/cMiniMapDrawer.cpp`.** Подключить `HudLayout.hpp` и получить `radarViewport` в конструкторе по размерам экрана из настроек. Для геометрии мини-карты использовать координаты и размеры этого прямоугольника вместо констант `cSideBar::WidthOfMinimap` и `HeightOfMinimap`. Удалить `drawStaticFrame`, его вызов и объявление, а также поле `m_iTrans` и его инициализацию. Состояния радара, звук включения, правый клик, дробный масштаб, рамка видимой области и скрытые туманом черви остаются.

6. **`src/drawers/CreditsDrawer.h`, `src/drawers/CreditsDrawer.cpp`.** Заменить только тело `CreditsDrawer::draw` кодом форка, заменив `currentCredits` на `m_currentCredits`. Добавить поле `m_gameTextDrawer`, получая игровой текстовый рисовальщик тем же способом, что и `cBuildingListDrawer`. Удалить `drawCurrentCredits`, `drawPreviousCredits` и их объявления. Анимация кредитов, `CreditsMath`, `thinkFast` и звук сохраняются; прочие функции и поля не меняются.

7. **`src/drawers/cBuildingListDrawer.h`, `src/drawers/cBuildingListDrawer.cpp`.** Перенести перечисленные функции форка: добавить UTF-8-помощники для обрезки названий; заменить `drawButtonHoverRectangle`, `drawButton`, `getDrawX`, `getDrawY`, `drawStructureSize`, проверки попадания в координаты и `onNotifyMouseEvent`; добавить `getCardWidth`, `getCardHeight`, `drawHdCard`, `getLayout`, прокрутку списка и `drawHdScrollbar`. Добавить и инициализировать `m_readyLabel("READY")`, перенести объявления функций без `UiAuditAccess` и подключить `HudLayout.hpp`. Сигнатуры порта, параметр `shouldDrawStructureSize` и параметры конструктора сохраняются; размеры структуры берутся из `InfoContext`. `drawList` собирается отдельно по четырём вставкам ниже. Лимиты построек и юнитов, `drawMaxBuilt` и подпись `"Paused"` сохраняются по указанным правилам слияния.

8. **`src/drawers/cSideBarDrawer.h`, `src/drawers/cSideBarDrawer.cpp`.** Заменить `draw` на вызов `drawHdSidebar` и добавить функции форка для отрисовки боковой панели, герба и имени Дома, радарной панели, шкал, показателей и списков построек. Для `SARDAUKAR` использовать `BMP_SELECT_HOUSE_SARDAUKAR` и подпись `"SARDAUKAR"`. Заменить создание candybar загрузкой трёх HD-гербов в `m_houseCrests` с владением, согласованным с `loadHdUiTexture` в порте. Удалить перечисленные candybar-функции и их объявления, связанные поля и вызовы пересоздания candybar в `setPlayer`. Вместе с candybar уходит прежняя отрисовка боковой панели; прочие классы панели не меняются.

9. **`src/sidebar/cBuildingList.h`, `src/sidebar/cBuildingList.cpp`, `src/sidebar/cBuildingListFactory.cpp`.** Перенести из форка методы `getButtonWidth`, `getButtonHeight`, `getItemCount`, изменить тело `isOverButton`, подключить `HudLayout.hpp` в factory и заменить тела `getButtonDrawY` и `getButtonDrawXStart`. В `initializeList` использовать новые размеры кнопок списка из форка. Другие файлы и фабрики не затрагиваются.

10. **Проверки.** Исходники на этом шаге не меняются. Дорожка D выполняет проверки 1–6 и передаёт коды выхода и требуемые строки логов корневой нити.

### Слияние `drawList`

Основа — `drawList` форка, с правилами переноса и сигнатурой порта, включая `const bool shouldDrawStructureSize`. Для прямоугольника картинки карточки используется `(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32)`.

1. Сразу после `heightOfIcon = getCardHeight()` добавить вычисления `structureLimitReached` и `unitLimitReached` из строк 182–183 порта.
2. В ветке незавершённого строительства после второго заполнения полосы прогресса добавить жёлтую надпись `"Paused"` для приостановленного элемента.
3. В ветке `item->isBuilding()` после обработки `shouldPlaceIt()` добавить вызов `drawMaxBuilt` с прямоугольником картинки карточки.
4. Перед указанной строкой форка добавить логику порта для определения `cannotBuildDueLimit`; условие сделать `if (!item->isAvailable() || isBuildingSameSubListItem || cannotBuildDueLimit)`. Существующее тело этой ветки обернуть в `if (!cannotBuildDueLimit)`, а для превышенного лимита вызвать `drawMaxBuilt`.

### Проверки 1–6 и ожидаемый успех

1. `sha256sum -c .tmp/p5ct/tests.sha256` — код 0 и две строки `OK`.

2. `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp | cmp - src/sidebar/HudLayout.hpp` — код 0.

3. Перед сборкой выполнить `df -m /srv`: если в столбце `Available` меньше 5000, остановиться с `## Q-P5C-01`. Иначе собрать из корня рабочей копии:

   ```bash
   DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5c/build.log 2>&1
   ```

   Успех: код 0; в `ctest.log` последней папки логов итог `100% tests passed, 0 tests failed out of 312`; все пять тестов `P5C ` имеют статус `Passed`; в `full.log` нет предупреждений из файлов рамки правок.

4. В `game-dummy.log` и `stdout-dummy.log` последней папки логов отсутствует `Imminent crash`.

5. Сверками `grep` проверить ожидаемые количества:

   - В добавлениях diff относительно `7eb119b007c05f063fe6dacf2e93ae31ac135b33` шаблон `^\+.*(localization::|uiaudit|UiAudit|renderDrawer|game\.m_screen|game\.getMouse|game\.isDebugMode|SDL2/)` — 0 строк.
   - В `src/drawers/cBuildingListDrawer.cpp`: `drawMaxBuilt(` — 3; `"Paused"` — 1; `isStructureLimitReached` — 1; `isUnitLimitReached` — 1; `drawHdCard(` — 2; `drawHdScrollbar(` — 2.
   - В `src/drawers/cSideBarDrawer.cpp`: `BMP_SELECT_HOUSE_SARDAUKAR` — 1; `hud_house_` — 3; `drawOrderButton` — 1; `drawHdSidebar` — 2.
   - Во всём `src/`: `drawStaticFrame`, `drawOptionBar`, `m_btnOptions`, `createCandyBar` — по 0.
   - В `src/game/cGame_logic.cpp` `cSideBar::configureLayout(` — 1; в `src/gamestates/cGamePlaying.cpp` `isWheelEvent` — 2.
   - В `src/drawers/CreditsDrawer.cpp` `CreditsMath` — не меньше 1.

   Расхождение ожидаемого числа строк или провал проверки 1–4 исправляется точной правкой в рамках дорожки и повторной проверкой. Третий подряд провал той же проверки означает `## Q-P5C-07` и остановку.

6. `git -c lfs.storage=$PWD/.tmp/p5c/lfs status --short` — вывод содержит только файлы рамки правок, новый `src/sidebar/HudLayout.hpp` и допустимые `__pycache__`.

### Область изменений и запреты

В исходниках можно менять только `src/sidebar/HudLayout.hpp`, `src/sidebar/cSideBar.h`, `src/sidebar/cSideBar.cpp`, `src/game/cGame_logic.cpp`, `src/gamestates/cGamePlaying.cpp`, `src/managers/cDrawManager.h`, `src/managers/cDrawManager.cpp`, `src/drawers/cMiniMapDrawer.h`, `src/drawers/cMiniMapDrawer.cpp`, `src/drawers/CreditsDrawer.h`, `src/drawers/CreditsDrawer.cpp`, `src/drawers/cBuildingListDrawer.h`, `src/drawers/cBuildingListDrawer.cpp`, `src/drawers/cSideBarDrawer.h`, `src/drawers/cSideBarDrawer.cpp`, `src/sidebar/cBuildingList.h`, `src/sidebar/cBuildingList.cpp`, `src/sidebar/cBuildingListFactory.cpp`. Для временных файлов и журналов задана папка `.tmp/p5c/`; сборка пишет в `.tmp/out/` и `.tmp/deps/`.

Запрещено менять тесты и файлы вне указанной рамки. В частности, в этом шаге не меняются `src/CMakeLists.txt`, `tests/CMakeLists.txt`, `src/map/cMapCamera.*`, `cMessageDrawer`, `cOrderDrawer`, `cStructureDrawer`, `cMouse`, `cGameControlsContext`, а также перечисленные в разделах «Не делать в этом шаге» код локализации, сохранений, музыки, скорости, панели приказов и UI-аудита. Коммитов не делать: их формирует ведущий по списку из сдачи.

### Остановки

Для исполнения P5C остановка требуется:

- при недостатке места перед сборкой — `## Q-P5C-01`;
- если вызывается функция форка без пары в порту, не названная в плане, или для продолжения нужна правка другого файла — подходящий блок `## Q-P5C-NN`;
- после третьего подряд провала одной и той же проверки из указанных для повторения случаев — `## Q-P5C-07`;
- если команда оболочки дважды подряд не завершилась с кодом выхода — `## Q-P5C-08`;
- при конфликте плана с кодом, нормой или данными — блок `Q` и стоп.

Для текущего пересказа правило запроса ограничивает работу только чтением вставленного текста и требует остановиться на `## DONE-P5C-RETELL`; никаких шагов P5C, остановок `Q` или правок я не выполнял.

### Двусмысленные места и выбранные прочтения

- В начале P5C сказано прочитать материалы до первого действия, а добавленные в конце правила требуют сначала вызвать `create_goal`, затем сразу читать материалы. Для гипотетического исполнения P5C я выбрал бы порядок из более конкретного добавленного правила: сначала `create_goal`, затем чтение. В этой задаче пересказа вызов запрещён, поэтому здесь я его не делал.
- Указаны «три субагента», но план называет роли A, B, C и D. Я выбрал прочтение о трёх помощниках всего: A–C работают параллельно, затем один из них после завершения своей дорожки выполняет проверки в роли D.
- Для нового `m_gameTextDrawer` не указано конкретное имя поля-источника. Я понимаю требование как получение игрового текстового рисовальщика тем же способом, которым `cBuildingListDrawer` получает свой.
- Правила переноса называют несколько возможных имён указателей настроек, мыши и `cDrawManager`. Я понимаю это как выбор уже используемого классом указателя соответствующего типа; фактический выбор следовало бы зафиксировать в сдаче с файлом и строкой.
- Текущий запрос запрещает открывать файлы и запускать команды, хотя P5C требует чтения исходников и проверок. Для этого хода выбрал прямое ограничение текущего задания: пересказал только предоставленный текст; файлы не открывал, команды проверки не запускал, изменения не вносил.