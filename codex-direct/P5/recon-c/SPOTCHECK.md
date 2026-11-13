# Выборочная сверка RECON-P5CR (15 фактов и 2 числа)

Источник: C:\Users\Slaven\Projects\DUNE\codex-direct\P5\recon-c\RECON.md
Команда для каждого факта: `git -C C:/Users/Slaven/Projects/DUNE show <REV>:<путь> | sed -n '<диапазон>p'`
Ревизии: FORK1 = 9208dcf5a358f40afd95c99480e4e09f781ed566; UP1 = d06f2fcd2a347182c3774fb96e9a85570405c489; PORT = 832c953a94a632d57872349013f7ed1a37434715; BASE = e17379ad660fca46859b403a6c3d33ec8d831a40.
Репозиторий не менялся: использованы только `git show`, `git grep`, `git diff`, `sed`, `grep`.

## Таблица фактов

| № | пункт | утверждение (кратко) | команда | вывод (до 2 строк) | совпало / не совпало |
|---|---|---|---|---|---|
| 1 | 1 | HudLayout.hpp:13–14: struct HudLayout на 13, TopBarHeight = 42 на 14 | REV=FORK1, путь src/sidebar/HudLayout.hpp, sed -n '13,14p' | `struct HudLayout {` / `static constexpr int TopBarHeight = 42;` | совпало |
| 2 | 1 | HudLayout.hpp:38–53 (create): sidebarWidth 280 при ширине < 960, иначе 360 | REV=FORK1, путь src/sidebar/HudLayout.hpp, sed -n '38,53p' (начало create); плюс git grep -n по строке с 960 | sed: `static HudLayout create(` / `int logicalWidth,`; grep: строка 46 `layout.sidebarWidth = logicalWidth < 960 ? 280 : 360;` | совпало |
| 3 | 1 | HudLayout.hpp:177–184 (tabRect): ширина таба = tabs.getWidth()/tabCount, последний таб получает остаток до EndX | REV=FORK1, путь src/sidebar/HudLayout.hpp, sed -n '177,184p' | `const int width = tabs.getWidth() / tabCount;` / `tabIndex == tabCount - 1 ? tabs.getEndX() - x : width;` | совпало |
| 4 | 2 | cSideBarDrawer.cpp:32, 37, 42: имена hud_house_atreides / harkonnen / ordos .png | REV=FORK1, путь src/drawers/cSideBarDrawer.cpp, sed -n '32p;37p;42p' | `"hud_house_atreides.png",` (32); `"hud_house_harkonnen.png",` (37); `"hud_house_ordos.png",` (42) | совпало |
| 5 | 2 | cSelectYourNextConquestState.cpp:99, 101, 104 — присвоения crestFile; загрузка crestFile на 107 | REV=FORK1, путь src/gamestates/cSelectYourNextConquestState.cpp, sed -n '99p;101p;104p;107p' | 99: `std::string crestFile = "hud_house_atreides.png";`; 101: `crestFile = "hud_house_harkonnen.png";`; 104: `crestFile = "hud_house_ordos.png";`; 107: `crestFile,` (аргумент вызова loadHdUiTexture, который начинается на 106) | совпало (уточнение: вызов занимает 106–108) |
| 6 | 2 | CreditsDrawer::draw на BASE:180 и PORT:209 | REV=BASE, путь src/drawers/CreditsDrawer.cpp, sed -n '180p'; REV=PORT, тот же путь, sed -n '209p' | BASE:180 `void CreditsDrawer::draw()`; PORT:209 `void CreditsDrawer::draw()` | совпало |
| 7 | 3 | cSideBarDrawer.cpp@PORT:84: прямоугольник (W−224, 0, 224, H) | REV=PORT, путь src/drawers/cSideBarDrawer.cpp, sed -n '84p' | `renderRectFillColor((getScreenW() - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, getScreenH(), ...)`. Константы: SidebarWidthWithoutCandyBar = 200, VerticalCandyBarWidth = 24, SidebarWidth = 200 + 24 = 224 (src/sidebar/cSideBar.h:102–104) | совпало |
| 8 | 3 | cMiniMapDrawer.cpp@PORT:67–89: масштаб min(200/mapW, 208/mapH); область (W−200, 42, 200, 208) | REV=PORT, путь src/drawers/cMiniMapDrawer.cpp, sed -n '67,89p' | 67: `float reportX = cSideBar::WidthOfMinimap*1.f / getMapWidthInPixels();`; 68: `float reportY = cSideBar::HeightOfMinimap*1.f / getMapHeightInPixels();`; 69: `m_factorZoom = std::min(reportX, reportY);`. Область: topLeftX = getScreenW() − WidthOfMinimap, topLeftY = TopBarHeight, RectFullMinimap(…, WidthOfMinimap, HeightOfMinimap). Константы: WidthOfMinimap = 200, HeightOfMinimap = 208, TopBarHeight = 42 (cSideBar.h:105–107) | совпало |
| 9 | 3 | cSideBarDrawer.cpp@PORT:393–398: x = W−224+8, y = 90, w = 7, h = 132 | REV=PORT, путь src/drawers/cSideBarDrawer.cpp, sed -n '393,398p' | 395: `int barTotalHeight = (cSideBar::HeightOfMinimap - 76);` (= 132); 396: `int barX = (getScreenW() - cSideBar::SidebarWidth) + (VerticalCandyBarWidth / 3);` (= W−224+8); 397: `int barY = cSideBar::TopBarHeight + 48;` (= 90); 398: `int barWidth = (VerticalCandyBarWidth / 3) - 1;` (= 7) | совпало |
| 10 | 4 | cMiniMapDrawer.cpp@UP1:293: hunk @@ -242,13 +293,16 @@; pixelSize = std::max(m_factorZoom, 0.001f); floor для начала; ceil и max(1, …) для размеров | REV=UP1, путь src/drawers/cMiniMapDrawer.cpp, sed -n '293,300p'; плюс git diff BASE UP1 -- путь \| grep -n '^@@' | sed: `iWidth--;` / `iHeight--;` (строка 293 — начало hunk; pixelSize на 296, floor на 301–302, max(1, ceil) на 304–305). grep: `@@ -242,13 +293,16 @@ void cMiniMapDrawer::drawViewPortRectangle()` | совпало (по hunk, см. примечание A) |
| 11 | 4 | cSideBarDrawer.cpp@UP1:274: добавлена ветка Sardaukar | REV=UP1, путь src/drawers/cSideBarDrawer.cpp, sed -n '274p'; плюс git diff BASE UP1 -- путь \| grep -n '^@@' и тело hunk | sed: `srcY = 11;` (контекст ветки ORDOS). grep hunk: `@@ -236,6 +274,12 @@ void cSideBarDrawer::drawMinimap()`; добавлено: `if (m_player->isHouse(SARDAUKAR)) {` (строка 277), `bitmapId = BMP_SELECT_HOUSE_SARDAUKAR;` (278) | совпало (по hunk, см. примечание A) |
| 12 | 4 | cDrawManager.cpp@UP1:170: удаляется вызов drawNotifications; меняется порядок боевых слоёв | REV=UP1, путь src/managers/cDrawManager.cpp, sed -n '170p'; плюс git diff BASE UP1 -- путь \| grep -n '^@@' и git grep -n drawNotifications UP1 | sed: `    // THE MESSAGE` (контекст). hunk: `@@ -88,100 +170,95 @@ void cDrawManager::drawCombatState()`; в hunk: `-    drawNotifications();` (BASE:91). git grep в UP1 — пусто | совпало по удалению вызова (по hunk, см. примечание A); порядок слоёв не проверялся |
| 13 | 5 | CMakeLists.txt@FORK1:222: add_test(NAME hud_layout_geometry COMMAND hud_layout_tests) | REV=FORK1, путь CMakeLists.txt, sed -n '222p' | `    add_test(NAME hud_layout_geometry COMMAND hud_layout_tests)` | совпало |
| 14 | 5 | CMakeLists.txt@FORK1:329: add_test(NAME hd_presentation_selection COMMAND hd_presentation_tests) | REV=FORK1, путь CMakeLists.txt, sed -n '329p' | `    add_test(NAME hd_presentation_selection COMMAND hd_presentation_tests)` | совпало |
| 15 | 5 | CMakeLists.txt:213 — tests/HudLayoutTests.cpp; :322 — tests/HdPresentationTests.cpp | REV=FORK1, путь CMakeLists.txt, sed -n '213p;322p' | 213: `        tests/HudLayoutTests.cpp`; 322: `        tests/HdPresentationTests.cpp` | совпало |

Примечание A. Для фактов 10, 11, 12 номер строки в отчёте — начало hunk (заголовок `@@ ... +N,... @@` совпадает). Сама строка N в UP1 — контекст (293 — `iWidth--;`; 274 — `srcY = 11;`; 170 — `// THE MESSAGE`), а описанное изменение находится внутри hunk. Точное совпадение строки N с описанным изменением: нет для 10, 11, 12.

Примечание B. Факт 5: строка 107 — аргумент `crestFile,` вызова, который начинается на 106. Номер 107 относится к загрузке, но сама загрузка занимает 106–108.

## Проверка числа «101 hunk» (пункт 4)

- Строк данных в `codex-direct/P5/recon-c/upstream-hud.tsv` без заголовка: 101 (файл 102 строки, первая — заголовок `путь	путь@d06f2fc:строка	что меняет участок	место в PORT`). Совпадение с утверждением: да.
- `git diff e17379a… d06f2fc… -- <8 путей> | grep -c '^@@ '` = 101.
- `... | sed -n '/^diff --git /p;/^@@ /p' | wc -l` = 109 (8 заголовков файлов + 101 hunk), как в RECON.
- Итог: совпало.

## Проверка числа «13 мест вызова assert» (пункт 5)

- `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HudLayoutTests.cpp | grep -c 'assert('` = 13.
- Контроль регулярным выражением `\bassert[[:space:]]*\(`: 13.
- Строки совпадений (grep -n): 10, 11, 12, 13, 14, 15, 16, 20, 21, 22, 26, 29, 43.
- Итог: совпало.

Итог: 15 из 15 совпало (факты 10, 11, 12 совпали по hunk, см. примечание A; факт 5 — с уточнением, примечание B). Числа 101 и 13 — совпало.
