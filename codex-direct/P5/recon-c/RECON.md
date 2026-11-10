# RECON-P5CR — разведка боевого HUD
Дата: 2026-11-10 17:29:48 UTC

Рабочая копия: /srv/dune/worktrees/u13g. Исследуемые ревизии: BASE e17379ad660fca46859b403a6c3d33ec8d831a40, FORK1 9208dcf5a358f40afd95c99480e4e09f781ed566, UP1 d06f2fcd2a347182c3774fb96e9a85570405c489, PORT 832c953a94a632d57872349013f7ed1a37434715.

## 1. Раскладка HudLayout в FORK1

Команда:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp | nl -ba

Вывод по структуре: HudLayout начинается на строке 13; TopBarHeight = 42 — строка 14; семь целочисленных полей — строки 16–22; тринадцать полей cRectangle — строки 24–36. Функции и диапазоны: create — 38–143; visibleRows — 145–151; totalRows — 153–156; maxScrollRow — 158–161; cardRect — 163–175; tabRect — 177–184; scrollbarThumb — 186–209. Всего одна структура, 20 полей, одна константа и семь функций.

Для каждого поля и функции искались совпадения в FORK1; для методов использовалась команда вида:

    git grep -n 'HudLayout::create' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src

Её вывод для create: CreditsDrawer.cpp:188; cBuildingListDrawer.cpp:728; cMessageDrawer.cpp:42; cMiniMapDrawer.cpp:35; cSideBarDrawer.cpp:77, 141, 308, 342; cDrawManager.cpp:290; cBuildingListFactory.cpp:24, 32, 49. Аналогичный поиск visibleRows вывел строки HudLayout.hpp:145, 160, 197 и cBuildingListDrawer.cpp:859, 862; totalRows — HudLayout.hpp:153, 160, 194; maxScrollRow — cBuildingListDrawer.cpp:747, 763, 803 и HudLayout.hpp:158, 190, 201, 202; cardRect — UiAuditAccess.cpp:380, 921, cBuildingListDrawer.cpp:242, 529 и HudLayout.hpp:163; scrollbarThumb — cBuildingListDrawer.cpp:806, 854 и HudLayout.hpp:186. Для tabRect вывод содержит только определение HudLayout.hpp:177, вызовов в src нет. Места использования полей и формулы всех функций приведены по строкам в таблице hud-layout.tsv.

Таблица: [hud-layout.tsv](/srv/dune/worktrees/u13g/.tmp/p5cr/hud-layout.tsv), 29 строк данных и 5 столбцов. Она содержит структуру, каждое поле, константу, функции, входы, выходы/формулы и все места использования с путём и строкой.

## 2. Потребители раскладки в FORK1

Команда поиска функций-потребителей:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n -E '::(drawHdSidebar|drawHdRadarPanel|drawHdCapacities|drawHdBuildingLists|getDrawX|getDrawY|drawList|isOverItemCoordinates|getCardWidth|getCardHeight|getLayout|getScrollRow|setScrollRow|drawHdScrollbar|onNotifyMouseEvent|draw|drawTopBarMusicControls|getButtonDrawY|getButtonDrawXStart|initializeList|recordSidebarClicks|prepareGameScreen|cMiniMapDrawer|cSideBarDrawer|cSelectYourNextConquestState)\(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cSideBarDrawer.cpp src/drawers/cBuildingListDrawer.cpp src/drawers/CreditsDrawer.cpp src/drawers/cMiniMapDrawer.cpp src/drawers/cMessageDrawer.cpp src/managers/cDrawManager.cpp src/sidebar/cBuildingListFactory.cpp src/debug/UiAuditAccess.cpp src/gamestates/cSelectYourNextConquestState.cpp

Вывод содержит 24 функции: HD-методы боковой панели и списка построек; методы отрисовки, прокрутки и hit-test списка построек; CreditsDrawer::draw, cMiniMapDrawer constructor, cMessageDrawer::draw, cDrawManager::drawTopBarMusicControls; три метода cBuildingListFactory; две функции UiAuditAccess. Все диапазоны, область HUD, совпадение имени в BASE и путь/функция PORT находятся в таблице fork-consumers.tsv. Проверка git grep для BASE и PORT подтвердила совпадения и отсутствующие функции из этой таблицы. Например, поиск drawHdSidebar в BASE вывода не дал; CreditsDrawer::draw находится в BASE на CreditsDrawer.cpp:180 и в PORT на CreditsDrawer.cpp:209.

Отдельный поиск мест с именами гербов:

    git grep -n 'hud_house' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src

Вывод:

    src/drawers/cSideBarDrawer.cpp:32: "hud_house_atreides.png"
    src/drawers/cSideBarDrawer.cpp:37: "hud_house_harkonnen.png"
    src/drawers/cSideBarDrawer.cpp:42: "hud_house_ordos.png"
    src/gamestates/cSelectYourNextConquestState.cpp:99: crestFile = "hud_house_atreides.png"
    src/gamestates/cSelectYourNextConquestState.cpp:101: crestFile = "hud_house_harkonnen.png"
    src/gamestates/cSelectYourNextConquestState.cpp:104: crestFile = "hud_house_ordos.png"

В cSideBarDrawer картинки загружает конструктор на строке 21; в cSelectYourNextConquestState имена выбираются в конструкторе на строках 99, 101 и 104, а выбранный crestFile загружается на строке 107. Все строки привязаны к FORK1 в таблице.

Путь src/debug/UiAuditAccess.cpp есть в FORK1, но отсутствует в PORT. Остальные исследованные потребители имеют одноимённый файл в PORT; поимённые результаты сверки даны в fork-consumers.tsv.

Таблица: [fork-consumers.tsv](/srv/dune/worktrees/u13g/.tmp/p5cr/fork-consumers.tsv), 24 функции, 6 столбцов.

## 3. Геометрия HUD в PORT

Команда проверки заданных путей:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cSideBarDrawer.cpp src/drawers/cMiniMapDrawer.cpp src/drawers/cBuildingListDrawer.cpp src/drawers/cMessageDrawer.cpp src/drawers/CreditsDrawer.cpp src/managers/cDrawManager.cpp src/sidebar/cSideBar.cpp src/sidebar/cBuildingList.cpp

Вывод содержит все восемь путей. Такой же поиск в BASE тоже вывел все восемь файлов. Поэтому поиск файлов по классу при отсутствии заданного пути не потребовался.

Геометрические функции, формулы, все чтения размеров экрана и места создания соответствующих объектов перечислены в port-hud.tsv. Основные формулы из строк таблицы:

- Боковая панель: прямоугольник (W−224, 0, 224, H), cSideBarDrawer::draw, src/drawers/cSideBarDrawer.cpp@832c953:81-91, вычисление на :84.
- Список построек: сетка начинается в (W−198, 302), шаг колонок 66 и строк 50; cBuildingListDrawer::drawList и расчёты getDrawX/getDrawY, src/drawers/cBuildingListDrawer.cpp@832c953:152-160, 165-196, 366-375.
- Мини-карта: область (W−200, 42, 200, 208), масштаб min(200/mapW, 208/mapH), конструктор cMiniMapDrawer, src/drawers/cMiniMapDrawer.cpp@832c953:67-89.
- Строка сообщений боя: начало (164, 1), ширина W−(224+164), высота 30, cMessageDrawer::initCombatPosition, src/drawers/cMessageDrawer.cpp@832c953:143-157.
- Полоса кредитной ёмкости: x=W−224+8, y=90, w=7, h=132, cSideBarDrawer::drawCreditsUsage, src/drawers/cSideBarDrawer.cpp@832c953:393-398.
- Герб Дома: исходник 68×50, у Ordos высота 49; увеличивается вдвое и центрируется в области мини-карты, cSideBarDrawer::drawMinimap, src/drawers/cSideBarDrawer.cpp@832c953:265-299.
- Счётчик кредитов: центрируется в правой панели по ширине текстуры, CreditsDrawer constructor, src/drawers/CreditsDrawer.cpp@832c953:72-75.

Команда поиска чтений экранных размеров:

    git grep -n -E 'getScreen[WH]|m_screen[WH]|[[:alnum:]_](Width|Height)\(' 832c953a94a632d57872349013f7ed1a37434715 -- <восемь заданных путей>

Вывод, сгруппированный по функциям, записан в port-hud.tsv. Среди совпадений: cSideBarDrawer — строки 50, 84, 115, 143, 148-149, 168, 172, 185-186, 191, 196-197, 238, 244, 262, 305, 340-341, 396; cMiniMapDrawer — 74, 266-267, 291-292, 333-334, 428, 432; cBuildingListDrawer — 154; cMessageDrawer — 151; CreditsDrawer — 74; cDrawManager — 123, 163, 258, 304, 336-339; cSideBar — 182. В cBuildingList.cpp совпадений нет. Строки с шириной/высотой карты и viewport также помечены отдельно в TSV.

Команда поиска мест создания:

    git grep -n -E 'make_unique<cDrawManager>|new cSideBar\(|new cBuildingList\(|m_sidebarDrawer =|m_creditsDrawer =|m_miniMapDrawer =|m_messageDrawer =|m_buildingListDrawer\(' 832c953a94a632d57872349013f7ed1a37434715 -- src/game/cGame_logic.cpp src/sidebar/cSideBarFactory.cpp src/sidebar/cBuildingListFactory.cpp src/managers/cDrawManager.cpp src/drawers/cSideBarDrawer.cpp

Вывод: cDrawManager создаётся в src/game/cGame_logic.cpp:866; drawer-объекты — в src/managers/cDrawManager.cpp:92-98; cBuildingListDrawer — как под-объект в src/drawers/cSideBarDrawer.cpp:42; cSideBar создаётся в src/sidebar/cSideBarFactory.cpp:35; cBuildingList — в src/sidebar/cBuildingListFactory.cpp:116.

Таблица: [port-hud.tsv](/srv/dune/worktrees/u13g/.tmp/p5cr/port-hud.tsv), 34 функции, 6 столбцов.

## 4. Изменения HUD между BASE и UP1

Команда наличия файлов в BASE:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git ls-tree -r --name-only e17379ad660fca46859b403a6c3d33ec8d831a40 -- src/drawers/cSideBarDrawer.cpp src/drawers/cMiniMapDrawer.cpp src/drawers/cBuildingListDrawer.cpp src/drawers/cMessageDrawer.cpp src/drawers/CreditsDrawer.cpp src/managers/cDrawManager.cpp src/sidebar/cSideBar.cpp src/sidebar/cBuildingList.cpp

Вывод: в BASE есть все восемь путей. Для каждого файла выполнено сравнение:

    git diff e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- <путь>

Контрольный вывод команды:

    git diff e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/drawers/cSideBarDrawer.cpp src/drawers/cMiniMapDrawer.cpp src/drawers/cBuildingListDrawer.cpp src/drawers/cMessageDrawer.cpp src/drawers/CreditsDrawer.cpp src/managers/cDrawManager.cpp src/sidebar/cSideBar.cpp src/sidebar/cBuildingList.cpp | sed -n '/^diff --git /p;/^@@ /p' | wc -l
    109

Число 109 включает 8 заголовков файлов и 101 diff-hunk. Отдельная строка на каждый hunk, начало в UP1, краткое изменение и соответствующее место в PORT приведены в upstream-hud.tsv.

Примеры вывода diff:

- src/drawers/cMiniMapDrawer.cpp@d06f2fc:293: расчёт viewport-рамки использует float scale, floor/ceil и минимальный размер 1 px. Выборочная команда:

      export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
      git diff --unified=3 e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/drawers/cMiniMapDrawer.cpp | sed -n '/^@@.*293/,+18p'

  вывела hunk @@ -242,13 +293,16 @@ и строки: int pixelSize = factorZoom заменён на const float pixelSize = std::max(m_factorZoom, 0.001f); начало координат использует std::floor, ширина и высота — std::ceil и std::max(1, ...).
- src/drawers/cSideBarDrawer.cpp@d06f2fc:274: добавлена ветка Sardaukar.
- src/sidebar/cSideBar.cpp@d06f2fc:245, 273: добавлены возобновление и пауза строящегося элемента.
- src/drawers/cBuildingListDrawer.cpp@d06f2fc:178, 233, 260, 375: лимиты построек и юнитов, а также наложение Max built.
- src/managers/cDrawManager.cpp@d06f2fc:170: меняется порядок боевых слоёв и удаляется вызов drawNotifications.

Таблица: [upstream-hud.tsv](/srv/dune/worktrees/u13g/.tmp/p5cr/upstream-hud.tsv), 101 hunk, 4 столбца.

## 5. Тесты

Команда поиска регистрации и имён тестов:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n -E 'HudLayoutTests|HdPresentationTests' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt tests

Вывод включает CMakeLists.txt:213 для HudLayoutTests.cpp и :322 для HdPresentationTests.cpp. Вызовы регистрации CTest из вывода CMakeLists.txt:

- add_test(NAME hud_layout_geometry COMMAND hud_layout_tests) — CMakeLists.txt@9208dcf:222.
- add_test(NAME hd_presentation_selection COMMAND hd_presentation_tests) — CMakeLists.txt@9208dcf:329.

Подсчёт по исходнику tests/HudLayoutTests.cpp:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HudLayoutTests.cpp | /srv/dune/venv/bin/python -c 'import re,sys; s=sys.stdin.read(); sites=len(re.findall(r"\bassert\s*\(",s)); body=s.split("int main()",1)[1]; cols=[int(x) for x in re.findall(r"verifyHdLayout\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*(\d+)\s*\)",body)]; loops=len(re.findall(r"for\s*\(\s*int\s+i\s*=\s*0\s*;\s*i\s*<\s*expectedColumns",s)); loop_asserts=3; total=len(cols)*sites-loop_asserts*len(cols)+loop_asserts*sum(cols); print(f"assert_call_sites={sites}; verifyHdLayout_invocations={len(cols)}; inner_loop_iterations={sum(cols)}; runtime_assert_evaluations={total}; other_check_call_sites=0")'
    assert_call_sites=13; verifyHdLayout_invocations=4; inner_loop_iterations=11; runtime_assert_evaluations=73; other_check_call_sites=0

Файл содержит 13 статических assert-вызовов, 4 вызова verifyHdLayout, 11 итераций внутренних циклов, что даёт 73 вычисления assert по коду теста; иных call-site проверок нет. Смысл каждой проверки на строке FORK1, используемые символы и заголовки и их наличие в PORT приведены построчно в tests.tsv.

Для HdPresentationTests выполнен поиск терминов HudLayout, SideBar, Sidebar, MiniMap, Minimap, hud_house и CreditsDrawer. Команда:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | /srv/dune/venv/bin/python -c 'import re,sys; s=sys.stdin.read(); terms=re.compile(r"HudLayout|SideBar|Sidebar|MiniMap|Minimap|hud_house|CreditsDrawer"); print("matching_test_lines=" + ",".join(str(i) for i,line in enumerate(s.splitlines(),1) if terms.search(line)) + "; qualifying_check_sites=0")'
    matching_test_lines=; qualifying_check_sites=0

Вывод не содержит совпадений; подходящих проверок нет.

Для проверки строк вызванных тестом функций и связанных заголовков выполнено:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n -E 'HudLayout|SideBar|Sidebar|MiniMap|Minimap|hud_house|CreditsDrawer' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- tests/HdPresentationTests.cpp src/utils/HdPresentation.hpp src/utils/OutcomeScreenLayout.hpp src/utils/TextAlignment.hpp src/utils/cRectangle.h src/utils/cRectangle.cpp

Вывод пуст.

PORT-сверка: git ls-tree вывел src/utils/cRectangle.h, src/utils/OutcomeScreenLayout.hpp и src/utils/TextAlignment.hpp; tests/HudLayoutTests.cpp, tests/HdPresentationTests.cpp, src/sidebar/HudLayout.hpp и src/utils/HdPresentation.hpp отсутствуют. Поиск HudLayout и verifyHdLayout в PORT вывода не дал. Символы и заголовки по каждой проверке сопоставлены с PORT в tests.tsv.

Таблица: [tests.tsv](/srv/dune/worktrees/u13g/.tmp/p5cr/tests.tsv), 14 строк данных, 4 столбца.

## Чтение

Прочитан целиком файл /srv/dune/tasks/load-check/PORT_PLAN.md. Отдельными командами прочитаны указанный участок docs/upstream/PORT_MAP.md на ревизии 62e1ff6585d8f1f047a3f983c63d990662e6afb6 и три строки Р30, Р33, Р66 из docs/decisions.md той же ревизии.

Команды чтения:

    cat /srv/dune/tasks/load-check/PORT_PLAN.md
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '311,381p'
    git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р(30|33|66)\.'

Вывод карты переноса перечисляет адаптивные экраны, в том числе HUD-файлы форка, которых нет в UP1. Вывод решений содержит три полные строки Р30, Р33 и Р66. Дополнительных правил, норм или контрактов, необходимых для этой разведки и отсутствующих в указанном списке, не обнаружено: разведка опиралась на факты источников и запреты самого задания; сборки и проверки из будущих шагов не выполнялись. PORT_PLAN ссылается на план шагов, проверок и launch-card-27, но эти материалы не требовались для чтения исходников или выполнения перечисленных здесь фактических проверок.

## Выборочная сверка корневой нитью

Для пункта 1 повторно выведены строки FORK1:
    
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp | nl -ba | sed -n '13,21p'
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp | nl -ba | sed -n '38,53p'
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp | nl -ba | sed -n '177,184p'

Вывод подтвердил struct HudLayout на :13 и TopBarHeight=42 на :14; create принимает logicalWidth, logicalHeight, reserveStarportOrderArea и выбирает sidebarWidth 280 при ширине меньше 960, иначе 360; tabRect делит ширину tabs на tabCount и последней вкладке отдаёт остаток.

Для пункта 2 повторно выполнены команды:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n 'drawHdSidebar' e17379ad660fca46859b403a6c3d33ec8d831a40 -- src/drawers/cSideBarDrawer.cpp
    git grep -n 'CreditsDrawer::draw' e17379ad660fca46859b403a6c3d33ec8d831a40 -- src/drawers/CreditsDrawer.cpp
    git grep -n 'CreditsDrawer::draw' 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/CreditsDrawer.cpp
    git grep -n 'hud_house' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src

Вывод первой команды пуст. Следующие команды вывели CreditsDrawer::draw на BASE:180 и PORT:209; также одноимённые drawCurrentCredits и drawPreviousCredits на BASE:220, 255 и PORT:222, 255. Поиск hud_house вывел шесть строк, перечисленных в пункте 2.

Для пункта 3 повторно выполнены команды:

    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show 832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp | nl -ba | sed -n '48,90p'
    git show 832c953a94a632d57872349013f7ed1a37434715:src/drawers/CreditsDrawer.cpp | nl -ba | sed -n '209,226p'
    git show 832c953a94a632d57872349013f7ed1a37434715:src/managers/cDrawManager.cpp | nl -ba | sed -n '88,99p'

Вывод первого фрагмента показал вычисление масштаба через отношение ширины и высоты мини-карты к размерам карты, координаты и два прямоугольника мини-карты, затем создание render target. Второй содержит CreditsDrawer::draw на :209. Третий содержит создание m_miniMapDrawer в cDrawManager::reset на :96.

Для пункта 4 повторён diff BASE..UP1 по src/drawers/cMiniMapDrawer.cpp. Вывод на hunk @@ -242,13 +293,16 @@ подтвердил изменение viewport-рамки: float pixelSize=max(m_factorZoom,0.001f), floor для начала координат и ceil/max(1,...) для размеров.

Схемы и число столбцов пяти таблиц проверены командой:

    /srv/dune/venv/bin/python -c 'from pathlib import Path; expected={"hud-layout.tsv":5,"fork-consumers.tsv":6,"port-hud.tsv":6,"upstream-hud.tsv":4,"tests.tsv":4}; [print(f"{name}: rows={len(rows)-1} columns={n} bad_rows={sum(len(row.split(chr(9)))!=n for row in rows)}") for name,n in expected.items() for rows in [Path(".tmp/p5cr",name).read_text().splitlines()]]'

Итоговый вывод: hud-layout.tsv rows=29 columns=5 bad_rows=0; fork-consumers.tsv rows=24 columns=6 bad_rows=0; port-hud.tsv rows=34 columns=6 bad_rows=0; upstream-hud.tsv rows=101 columns=4 bad_rows=0; tests.tsv rows=14 columns=4 bad_rows=0. Предыдущий запуск того же скрипта ожидал ошибочное число столбцов 5 у tests.tsv и вывел bad_rows=15; ожидание было исправлено на 4, повторный запуск дал bad_rows=0.

## Файлы .tmp/p5cr/

- RECON.md
- progress.md
- hud-layout.tsv
- fork-consumers.tsv
- port-hud.tsv
- upstream-hud.tsv
- tests.tsv

## Не проверено

Сборки, CTest и запуск игры не выполнялись по запрету задания. Поведение HUD в запущенной игре и фактические пиксельные размеры не проверялись; выводы относятся к исходному коду указанных ревизий.
