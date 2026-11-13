# Разведка P5-R

Рабочая копия: /srv/dune/worktrees/u34. Для чтения использованы только явные ревизии BASE=e17379ad660fca46859b403a6c3d33ec8d831a40, FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566, UP1=d06f2fcd2a347182c3774fb96e9a85570405c489, PORT=0a33444e9032ef935dfe4cdde6bb622771484230 и MAIN=284961e88b21079c548ed638ad4e4735920d6729. Рабочие файлы и ветка не менялись. Сборки, CTest и запуск игры не выполнялись.
Перед каждым вызовом Git в shell выполнялся export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH. Команды в таблицах даны в форме, запускавшейся после такого экспорта.

## Чтение

Полностью прочитан план переноса:
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 284961e88b21079c548ed638ad4e4735920d6729:docs/upstream/PORT_PLAN.md
- Результат: полный вывод без усечения. Релевантные строки: П5 после П4 и с функциями adaptive-layout/ui-audit — docs/upstream/PORT_PLAN.md@284961e88b21079c548ed638ad4e4735920d6729:60; перенос HD4 PNG, RenderScale/WorldScale, HD bar images и WorldScale persistence по разным шагам — строки 89–90 и 96; приёмка П5 — строка 90.

Полностью прочитано задание П4б. Первый вывод был усечён; файл перечитан частями, отдельными командами:
- git show 284961e88b21079c548ed638ad4e4735920d6729:codex-direct/P4/TASK-B.md | sed -n '1,120p'
- git show 284961e88b21079c548ed638ad4e4735920d6729:codex-direct/P4/TASK-B.md | sed -n '121,254p'
- Результат: строки 1–254 прочитаны полностью. Холст считается один раз при запуске — codex-direct/P4/TASK-B.md@284961e88b21079c548ed638ad4e4735920d6729:13; WorldScale не зависит от RenderScale и считается от высоты вывода — строка 16; меню настроек, адаптивные раскладки и отдельные HD4 UI картинки отданы П5, WorldScale persistence — П8 — строки 116–119.

Карта и решения прочитаны требуемыми командами:
- git show 284961e88b21079c548ed638ad4e4735920d6729:docs/upstream/PORT_MAP.md | sed -n '311,440p' — полный вывод секций adaptive-layout и ui-audit. В общей таблице функций adaptive-layout — PORT_MAP.md@284961e88b21079c548ed638ad4e4735920d6729:18, ui-audit зависит от adaptive-layout — строка 19; save-slots, music-pools, command-bar, controls-tab и interaction-refresh — строки 22–26.
- git show 284961e88b21079c548ed638ad4e4735920d6729:docs/decisions.md | grep -E '^- \*\*Р(28|30|33|34|63|66)\.' — вывод дал ровно шесть строк: решения Р28, Р30, Р33, Р34, Р63 и Р66 на docs/decisions.md@284961e88b21079c548ed638ad4e4735920d6729:36, 38, 41, 42, 92 и 95.
- Дополнительно прочитаны нужные строки таблицы зависимостей П4б: git show 284961e88b21079c548ed638ad4e4735920d6729:codex-direct/P4/recon-b/screen-size-uses.tsv с выборкой по нужным путям; опорные записи приведены в пункте 8.
- Не хватает в задании: дополнительных норм или контрактов, необходимых для этой read-only разведки, не обнаружено. Сборочные правила и связанные с ними ссылки плана к разведке не применялись.

## 1. Раскладки FORK1

Полная таблица — .tmp/p5r/layouts.tsv. В ней 33 строки с символами восьми файлов, входами/выходами, местами вызовов, привязкой к функциям карты, командами чтения и их выводом. Структуры, функции и именованные API-константы указаны отдельно; локальные промежуточные const значения описаны внутри строки функции, которая их вычисляет.

Команда чтения каждого файла и точные фрагменты вывода даны в полях «команда источника» и «вывод источника». Места вызовов собраны отдельными git grep командами с явной ревизией и результатами в последних двух полях. Ключевые разделения: HudLayout, OptionsMenuLayout, CampaignMapLayout, OutcomeScreenLayout и TextAlignment относятся к adaptive-layout; CommandBarLayout вызывается cCommandBarDrawer и относится к command-bar/П10; MusicControlsLayout вызывается message/credit drawers и относится к music-pools/П9; AdvancedOptionsHeaderLayout используется страницей дополнительных настроек и также связан с controls-tab/П10. Командная панель и музыкальные controls перечислены в карте и в adaptive-layout как затронутые пути, но их отдельные функции принадлежат П10 и П9 соответственно.

## 2. Экраны FORK1 и PORT

Полная матрица — .tmp/p5r/screens.tsv: 15 строк для запрошенных экранов и подэкранов, с классом состояния, исходной раскладкой/HD картинками, классом PORT, формулами координат и наблюдениями для всех пяти холстов. Каждая строка содержит команду чтения PORT кода и опорный вывод.

Основные результаты из таблицы:
- PORT центрирует неизменные области 640×480 карты кампании и выбора миссии; свободное поле увеличивается с холстом.
- Главное меню сохраняет нативный размер графики и фиксированную высоту панели кнопок, центрируя блок по ширине холста.
- Главное окно настроек PORT занимает прямоугольник с полями 30% высоты; строки внутри привязаны к левому краю окна, поэтому широкий холст оставляет пустое внутреннее пространство. У FORK1 есть дополнительная страница настроек, у PORT её нет.
- Меню выбора Дома распределяет четыре фиксированных прямоугольника по ширине, а ментат масштабирует фиксированную картинку до ограниченного коэффициента и центрирует.
- В схватке PORT использует width=heightOfRightColumn+2, где heightOfRightColumn=H−185, хотя X preview начинается в W−302. Поэтому прямоугольник выходит за правый край на 115, 235 или 475 пикселей при заданных высотах 600, 720 и 960; снизу он выходит на 55 пикселей при каждой высоте. Расчёт для каждого холста приведён в таблице.
- В боевом HUD боковая панель имеет ширину 224 и прижата справа; список построек и мини-карта используют фиксированные native размеры, строка сообщений растёт по ширине поля боя, верхняя полоса кредитов центрируется в 200-пиксельной внутренней части панели.

## 3. HD-картинки интерфейса

Полный список 14 PNG — .tmp/p5r/hd-ui.tsv. Каждая строка содержит FORK1 путь, LFS проверку и точный вывод (указатель/размер), загрузчик, место рисования, классическую замену или fallback, а также проверку наличия файла/загрузчика/рисования в PORT.

Команда export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/data/hd4 | grep '\.png$' | wc -l вывела 14. Пример проверки campaign_map.png:
- Команда: git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/campaign_map.png | head -4
- Вывод: version https://git-lfs.github.com/spec/v1; oid sha256:b150c09b58ca4a8debfee7eb0c262153722283d89b648e62927a61ecd71019c7; size 4541123. Git blob указателя имеет 132 байта.
- В PORT папки resources/bin/data/hd4 нет; поиск известных 14 имен и loadHdUiTexture по src не дал строк. Файлы, прямой PNG loader и места их рисования отсутствуют.

PORT грузит игровые HD4 datafiles через ContextCreator.cpp@0a33444:35,43,51,59 как Graphics с kHd4AssetDensity; Graphics.hpp@0a33444:58–63 задаёт плотность 4 и путь HD4 сцен. AbstractMentat.cpp@0a33444:346–364 открывает HD4 scene .dat файл. Команда export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'campaign_map\.png|command_bar\.png|command_bar_disabled\.png|credits_team\.png|credits_title\.png|hud_house_atreides\.png|hud_house_harkonnen\.png|hud_house_ordos\.png|main_menu_background\.png|main_menu_logo\.png|outcome_defeat_en\.png|outcome_defeat_ru\.png|outcome_victory_en\.png|outcome_victory_ru\.png|loadHdUiTexture' 0a33444e9032ef935dfe4cdde6bb622771484230 -- src вывела пустой результат.

Р34 говорит, что игра использует HD4 паки и классический режим/откат удалён, но не запрещает отдельный PNG, если он также содержит максимальную графику. Р63 требует сохранить работы форка и брать новые возможности апстрима, если они не спорят с функцией форка — docs/decisions.md@284961e88b21079c548ed638ad4e4735920d6729:42, 92. Карта П4 прямо передаёт отдельные PNG из data/hd4 и loadHdUiTexture шагам П5/П10 — PORT_PLAN.md@284961e88b21079c548ed638ad4e4735920d6729:89–90, 96.

## 4. «Масштаб игры» и «Размер объектов»

FORK1:
- Команда export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'Масштаб игры|Размер объектов|selectedRenderScaleText|selectedWorldScaleText|saveDisplaySettings|Saved\. Restart' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/gamestates/cOptionsState.cpp вывела строки 576, 626, 696, 699, 707, 737, 1135, 1166, 1201, 1237 и 1357.
- Основная настройка: cOptionsState.cpp@9208dcf:1134–1190 — label «Масштаб игры», кнопка уменьшения, value label, кнопка увеличения. Дополнительная страница есть: constructAdvancedWindow в cOptionsState.cpp@9208dcf:278–295. «Размер объектов» и такие же контролы — cOptionsState.cpp@9208dcf:1200–1262.
- RenderScale: Auto=0 или 100/125/150/175/200% — RenderScale.hpp@9208dcf:12–15. WorldScale: Auto=0 или 100/110/125/150% — WorldScale.hpp@9208dcf:5–6. Auto WorldScale зависит от высоты: WorldScale.cpp@9208dcf:13–24. Отображаемый текст собирают selectedRenderScaleText и selectedWorldScaleText — cOptionsState.cpp@9208dcf:576–597, 626–642.
- Кнопка Apply вызывает saveDisplaySettings — cOptionsState.cpp@9208dcf:1349–1360. Настройки записываются в settings.ini с ключами RenderScale и WorldScale — cOptionsState.cpp@9208dcf:715–728 и common.cpp@9208dcf:332–360. После сохранения выводится «Сохранено. Перезапустите игру.» — cOptionsState.cpp@9208dcf:734–740. Значит выбор применяется после перезапуска: создаются экран cScreenInit и контекст, повторно читаются screen W/H, перенастраиваются sidebar и ресурсы — cGame_logic.cpp@9208dcf:1075–1095; начальный зум камеры определяется WorldScale — cMapCamera.cpp@9208dcf:37–64.

PORT:
- Меню — один экран cOptionsState; constructWindow и текущая сборка GUI — cOptionsState.cpp@0a33444:39–71, 374–378. Контролы относятся к музыке, звуку, скорости игры, fog of war и low power — строки 158–327. Строк «Масштаб игры» и «Размер объектов» и отдельной страницы нет. GUI добавляет объекты в m_guiWindow через addGuiObject.
- Preferences читает RenderScale и WorldScale — Preferences.cpp@0a33444:65–69. Записывает только RenderScale — Preferences.cpp@0a33444:163; команды git grep по ключам в Preferences показывают для WorldScale только чтение, без вызова set для сохранения.
- PREFERENCES_FILE задаёт preferences.ini, чтение и сохранение подключены в main.cpp@0a33444:54, 79, 82, 113, 115. Запись WorldScale в preferences.ini ещё не реализована; план переносит её в П8 — PORT_PLAN.md@284961e88b21079c548ed638ad4e4735920d6729:89, 93.
- cGame::setupGame вызывает applyRenderScale один раз — cGame_logic.cpp@0a33444:752–756, затем заполняет размеры холста и outputH — строки 771–774. applyRenderScale меняет SDL logical presentation — cSDLSystem.cpp@0a33444:59–80. Изменение RenderScale через live GUI потребовало бы повторного построения всех связанных размеров и render targets.
- Камера берёт WorldScale при создании и при resetZoom — cMapCamera.cpp@0a33444:44–54, 71–74. Настройка записывается в game settings при запуске — cGame_logic.cpp@0a33444:300–340. В PORT нет UI, который меняет WorldScale на лету.

## 5. Режим ui-audit

Полная таблица исходников, мест вызова/доступа, инструментов и тестов — .tmp/p5r/ui-audit.tsv. В таблице по каждому файлу есть назначение, что требует от игры и соответствие в PORT.

Ключевые точки:
- Аргументы и ранние выходы — UiAuditArguments.hpp/.cpp@9208dcf и main.cpp@9208dcf:86–89, 111–135. Каталог сцен — UiAuditScenes.hpp/.cpp@9208dcf. Снимок PNG физического разрешения и JSONL geometry output с header и records — UiAuditCapture.cpp@9208dcf:155–261, 369–498.
- UiAuditAccess даёт friend-шлюз к приватному состоянию игры и готовит реальные опции, сохранения, campaign, HUD, marks и hitboxes — UiAudit.hpp@9208dcf:78–115 и UiAuditAccess.cpp@9208dcf:42–72, 97–213, 261–350, 536–632, 780–937.
- Ветви интеграции вызываются main.cpp, игровым циклом cGame_logic.cpp, platform/screen initialization, а friend-доступ открыт в audio/controller, game, mouse и camera headers; вся судьба файлов и перемещённые классы отражены в таблице. В PORT имя ui-audit не найдено по src/tools/tests.
- tools/ui-audit содержит генерацию комбинаций/сцен, запуск/сбор результатов, PNG и JSONL геометрии, проверки геометрии, клавиш, screen catalog и completeness, плюс unit tests. Каждая строка таблицы описывает вход игры и ожидаемые файлы.
- Р30: combos.py получает набор доступных render/world scales. RenderScale прогоняется для каталога сцен; WorldScale — только для игровых экранов. run_all.py запускает шесть стандартных разрешений: 1024×768, 1280×720, 1366×768, 1600×900, 1920×1080, 2560×1440. check_geometry.py проверяет правила 1–9 на overlays, обрезку текста, labels на панелях, пересечение click zones и геометрию; сюда входят метки юнитов/зданий. check_keys.py проверяет rule 10 — две клавиши на одно действие в состоянии. check_screens.py сверяет кодовые экраны с каталогом либо явным исключением; check_completeness.py требует полный набор ожидаемых PNG и geometry logs. Источники: combos.py@9208dcf:14–26, 58–61; run_all.py@9208dcf:19–27, 94–120; check_geometry.py@9208dcf:7–18, 64–137; check_keys.py@9208dcf:38–118; check_screens.py@9208dcf:39–82; check_completeness.py@9208dcf:22–69.
- PORT не содержит ни каталога сцен, ни точек сбора text/gui/area/label/click/credit geometry, ни тестов аудита. В коде форка и в таблице отражены доступы friend/accessor и вызовы, отсутствующие в PORT.

## 6. Тесты FORK1

Полная таблица всех 11 файлов — .tmp/p5r/tests.tsv. Включены CTest target и строки его регистрации, команда/результат статического подсчёта проверочных sites, описание каждого тестового entry point, нужные символы/заголовки и наличие в PORT, функция карты.

Подсчёт статический: C++ main-driven файлы считают места assert/require/expectEqual, а Python runtime smoke files — условные guard sites; runtime helper имеет ноль самостоятельных test-функций. Таблица не выдаёт статические sites за количество реально выполненных проверок. Дополнительные заметки об этом были перенесены из хвоста TSV в этот раздел, чтобы каждый ряд tests.tsv оставался шестиколоночной строкой.

Два runtime CTest входят в CMake только при D2TM_UI_AUDIT_RUNTIME_TESTS=ON; опция default OFF — CMakeLists.txt@9208dcf:456–475. Команду CTest не запускали.

## 7. Изменения UP1 относительно BASE

Полная таблица по каждому из 124 файлов PORT в нужных каталогах — .tmp/p5r/upstream.tsv: команда git log --oneline BASE..UP1 -- <path> | wc -l и число для каждого файла; git log --format='%h %s' --shortstat с отсортированными крупнейшими изменениями и до пяти коммитов; статус BASE→UP1.

Корневые проверки объёма:
- export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree -r --name-only 0a33444e9032ef935dfe4cdde6bb622771484230 src/gamestates src/gui src/sidebar src/drawers src/gameobjects/mentat | wc -l → 124.
- export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git diff --name-status e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/gamestates src/gui src/sidebar src/drawers | wc -l → 114.
- Тот же git diff с awk '$1 == "A" {n++} END {print n+0}' вывел 41 добавленный путь.
- Новые state/screen классы включают cCreatorState, cEditorState, cGamePlaying, cMentatState, cNewMapEditorState, cScoringState, cTellHouseState, cVideoState, cWinLoseState; новые GUI-классы включают GuiBar, GuiButtonGroup, GuiConsole, GuiConsoleMessageParser, GuiCycleButton, GuiStateButton, GuiTextInput, GuiValueButton. Полный вывод статусов находится в upstream.tsv.
- Крупные изменения ранжированы по сумме insertions+deletions. Это механический размер diff, а не оценка архитектурной важности.

### Независимая выборочная сверка корневой нитью

Три факта дорожки 1:
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '57,70p'
- Вывод: строка 59 margin = screenH * 0.3; строки 60–63 x/y = margin, width/height = W/H − 2*margin; строки 65–67 задают button height/width.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/gamestates/cSetupSkirmishState.cpp | nl -ba | sed -n '201,207p'
- Вывод: 203 heightOfRightColumn = screen_y − (playerListBarHeight + previewMapFrameHeight); 204 previewMap = cRectangle(previewMapX, previewMapY, heightOfRightColumn + 2, heightOfRightColumn); 207 selectArea width = screen_x − heightOfRightColumn − 2.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '140,144p'
- Вывод: строка 142 offsetX = (screenW − 640)/2; строка 143 offsetY = (screenH − 480)/2.

Три факта дорожки 2:
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/campaign_map.png | head -4
- Вывод: version https://git-lfs.github.com/spec/v1; oid sha256:b150c09b58ca4a8debfee7eb0c262153722283d89b648e62927a61ecd71019c7; size 4541123.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git log --oneline e17379ad660fca46859b403a6c3d33ec8d831a40..d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/drawers/CreditsDrawer.cpp | wc -l
- Вывод: 25.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'RenderScale|WorldScale' 0a33444e9032ef935dfe4cdde6bb622771484230 -- src/game/Preferences.cpp
- Вывод: строки 65–66 читают RenderScale; строки 68–69 читают WorldScale; строка 163 сохраняет RenderScale. Совпадения set(WorldScale) нет.

Три факта дорожки 3:
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HudLayoutTests.cpp | grep -Ec 'assert[[:space:]]*\('
- Вывод: 13.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt | nl -ba | sed -n '456,475p'
- Вывод: строка 456 задаёт D2TM_UI_AUDIT_RUNTIME_TESTS default OFF; внутри условия регистрируются ui_audit_unknown_scene (459–466) и ui_audit_main_menu_png (467–474).
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -i -E 'uiaudit|ui-audit' 0a33444e9032ef935dfe4cdde6bb622771484230 -- src tools tests
- Вывод: пустой; код возврата 1.

Сверка объёмов:
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree -r --name-only 0a33444e9032ef935dfe4cdde6bb622771484230 src/gamestates src/gui src/sidebar src/drawers src/gameobjects/mentat | wc -l. Вывод: 124.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/data/hd4 | grep '\.png$' | wc -l. Вывод: 14.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git diff --name-status e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/gamestates src/gui src/sidebar src/drawers | awk '$1 == "A" {n++} END {print n+0}'. Вывод: 41.

## 8. Развилки и рекомендации

### Деление П5

Вариант 1 — перенести адаптивные раскладки, настройки, HD UI и аудит одним заданием. Риск: геометрия, новое подключение экранов, настройки и тестовый инструмент с доступом к приватному runtime попадают в один большой набор изменений.

Вариант 2 — две части внутри П5: сначала адаптивные layout функции, подключение экранов, UI PNG, две настройки и layout/presentation tests; затем ui-audit hooks, сцены, geometry/capture API, tools и audit tests. Порядок совпадает с зависимостью ui-audit → adaptive-layout в PORT_MAP.md@284961e88b21079c548ed638ad4e4735920d6729:18–19. Во второй части аудит уже может снимать и проверять мигрированные экраны. Рекомендация — два этапа внутри П5; оставить оба в одном шаге карты.

В layout части: HudLayoutTests, OptionsMenuLayoutTests, CampaignMapLayoutTests и относящиеся к адаптивной геометрии случаи HdPresentationTests. В audit части: UiAuditArgumentsTests и три Python файла ui_audit_*.py; фактический запуск остаётся по настройке CTest runtime. CommandBarLayoutTests, MusicControlsLayoutTests и InteractionRegressionTests относятся к последующим функциям, описанным ниже.

### Раскладки и тесты по шагам

- П5/adaptive-layout: HudLayout, OptionsMenuLayout, CampaignMapLayout, OutcomeScreenLayout, TextAlignment; основной экран OptionsMenu. AdvancedOptionsHeaderLayout — геометрия страницы настроек, но Controls tab и ввод клавиш относятся к controls-tab/П10. Сохранение/загрузка как действия меню остаются интерфейсом П5, а сами save-slot диалоги/логика — П8.
- П8/save-slots: SaveSlotsDialog и persistence WorldScale в preferences.ini. В списке восьми layout headers отдельного SaveSlotsLayout нет. Layout окна настроек не переносит сам диалог сохранений.
- П9/music-pools: MusicControlsLayout и MusicControlsLayoutTests.
- П10/command-bar, controls-tab, interaction-refresh, starport-orders: CommandBarLayout, CommandBarLayoutTests и InteractionRegressionTests. В adaptive-layout файлах есть CommandBarLayout.hpp и AdvancedOptionsHeaderLayout.hpp, но место вызова/функция карты относит соответствующую работу к П10.
- HdPresentationTests содержит смешанные проверки физического HD presentation (П3/П4), outcome geometry/text alignment (П5), поэтому включать весь файл в П5 без разбиения case-level требований нельзя. HD command-bar images из этой функции карты идут отдельно в П10 — PORT_PLAN.md@284961e88b21079c548ed638ad4e4735920d6729:96.
- Факты о функциях и CTest targets находятся в PORT_MAP.md@284961e88b21079c548ed638ad4e4735920d6729:18–26 и PORT_PLAN.md@284961e88b21079c548ed638ad4e4735920d6729:90, 93–96; тестовые case summaries — в tests.tsv.


### Перенос экранов, переписанных апстримом

Вариант 1 — переносить код экранов форка поверх переписанного апстримного состояния. Риск: вернуть старые архитектурные/API зависимости, отсутствующие в UP1, и затронуть новые апстримные экраны/GUI.

Вариант 2 — оставить состояния и компоненты UP1, перенести функции расчёта геометрии по правилам форка и подключить их к новым вызовам апстрима. Риск: понадобится адаптация каждого caller и сохранение поведения координат/ввода. Рекомендация — второй вариант: карта помечает большинство этих путей как rewrite, а список добавленных screen/GUI классов зафиксирован в upstream.tsv. Это сохраняет кодовые контракты UP1 и переносит именно геометрию.

### Отдельные PNG или HD4 pack

Вариант 1 — оставлять UI PNG в data/hd4 с прямым loadHdUiTexture. Риск: отдельная ветка загрузки помимо HD4 datafiles. Она переносит существующие картинки/назначение напрямую и не создаёт классический fallback.

Вариант 2 — включить те же изображения в HD4 pack. Это ближе к формулировке Р34 о постоянной загрузке HD4 паков, но потребует назначить записи pack/имена и изменить загрузчик/места чтения. Р34 не говорит, что все HD картинки обязаны находиться только внутри pack; Р63 требует сохранить работу форка. Рекомендация — следовать явно переданному П4 пути loadHdUiTexture и отдельным PNG в П5, если ведущий не обнаружит отдельного упаковочного контракта: картинки HD, classic fallback отсутствует, а изменение pack schema не требуется. Р34/Р63 и передача П4 подтверждены docs/decisions.md@284961e:42,92 и docs/upstream/PORT_PLAN.md@284961e:89–90.

### Изменение RenderScale после запуска

Вариант 1 — выбор сохраняется, холст применяется после перезапуска. Пользователь ждёт до нового старта, зато сохраняется контракт П4б: размер холста рассчитывается один раз при создании окна и renderer. Рекомендация — этот вариант.

Вариант 2 — применить немедленно. Помимо SDL logical presentation пришлось бы пересоздать screen-sized targets actualRenderer/screenTexture, размеры m_gameSettings и mapViewport, console/viewports, cached HUD textures, sidebar/minimap hitboxes и позиции drawer/state GUI. Эти consumer группы присутствуют в codex-direct/P4/recon-b/screen-size-uses.tsv@284961e88b21079c548ed638ad4e4735920d6729:31–49, 76–90 и 198–201. Внутренние ссылки таблицы указывают на создание frame targets и viewport в cGame_logic.cpp@ce0cacf:650–661, 821; cached geometry sidebar/minimap в cSideBarDrawer.cpp@ce0cacf:50, 84, 115 и cMiniMapDrawer.cpp@ce0cacf:74–86; GUI окна в cOptionsState.cpp@ce0cacf:59–70. В таблице есть и другие creator-time consumers. Изменить только SDL canvas недостаточно: оставшиеся объекты будут использовать старые координаты.
- Источник контракта: codex-direct/P4/TASK-B.md@284961e:13, 117; applyRenderScale и начальное применение — cGame_logic.cpp@0a33444:752–756 и cSDLSystem.cpp@0a33444:59–80.
- Решено исполнителем: RenderScale → применение после перезапуска; было — холст и зависимые объекты создаются из размера старта, стало бы — только SDL canvas изменён при открытых старых объектах; основание: контракт П4б и зависимости codex-direct/P4/recon-b/screen-size-uses.tsv@284961e88b21079c548ed638ad4e4735920d6729:31–49, 76–90, 198–201.

Точечный вывод таблицы использования размеров:
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 284961e88b21079c548ed638ad4e4735920d6729:codex-direct/P4/recon-b/screen-size-uses.tsv | nl -ba | grep -E 'cGame_logic.cpp@ce0cacf:(650|651|659|661|753|771|772|821)|cSideBarDrawer.cpp@ce0cacf:(50|84|115|143|238|305)|cMiniMapDrawer.cpp@ce0cacf:(74|75|82|85|86)|cOptionsState.cpp@ce0cacf:(59|62|63|70)'
Вывод команды screen-size-uses.tsv:
31	src/drawers/cSideBarDrawer.cpp@ce0cacf:50	getScreenH()	m_candiBarRenderer = m_sdlDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, m_services->settings->getScreenH()-40, m_sdlDrawer->getFrameDensity());	при создании объекта
34	src/drawers/cSideBarDrawer.cpp@ce0cacf:115	getScreenH()	m_candiBarRenderer = m_sdlDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, m_services->settings->getScreenH()-40, m_sdlDrawer->getFrameDensity());	при событии: смена дома игрока или плотности кадра
17	src/drawers/cMiniMapDrawer.cpp@ce0cacf:74	getScreenW()	int topLeftX = settings->getScreenW() - cSideBar::WidthOfMinimap;	при создании объекта
20	src/drawers/cMiniMapDrawer.cpp@ce0cacf:85	cMiniMapDrawer::m_RectMinimap [cRectangle]	сохраняет hit-test прямоугольник миникарты в логических координатах	при создании объекта
76	src/game/cGame_logic.cpp@ce0cacf:650	m_screenH	actualRenderer = m_sdlDrawer->createRenderTargetTexture(m_gameSettings->m_screenW, m_gameSettings->m_screenH, density);	при событии: запуск или изменение плотности кадра
78	src/game/cGame_logic.cpp@ce0cacf:651	m_screenH	screenTexture = m_sdlDrawer->createRenderTargetTexture(m_gameSettings->m_screenW, m_gameSettings->m_screenH, density);	при событии: запуск или изменение плотности кадра
89	src/game/cGame_logic.cpp@ce0cacf:821	getScreenH()	m_mapViewport = std::make_unique<cRectangle>(0, cSideBar::TopBarHeight, m_gameSettings->getScreenW() - cSideBar::SidebarWidth, m_gameSettings->getScreenH() - cSideBar::TopBarHeight);	при создании объекта: установка размеров консоли и viewport после SDL
198	src/gamestates/cOptionsState.cpp@ce0cacf:59	getScreenH()	int margin = m_settings->getScreenH() * 0.3;	при событии: создание или перестроение окна опций

Команды и выводы по веткам рекомендаций:
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'adaptive-layout|ui-audit|command-bar|music-pools|save-slots|interaction-refresh' 284961e88b21079c548ed638ad4e4735920d6729 -- docs/upstream/PORT_MAP.md. Вывод строк 18–26: adaptive-layout — Б5; ui-audit — Б5 после adaptive-layout; save-slots — Б8; music-pools — Б9; command-bar и interaction-refresh — Б10.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'П4|П5|Масштаб игры|HD-картинки интерфейса|перенесено в другие шаги' 284961e88b21079c548ed638ad4e4735920d6729 -- docs/upstream/PORT_PLAN.md. Вывод: строка 89 отдаёт настройки/PNG П5, command bar П10 и WorldScale persistence П8; строка 90 перечисляет тесты П5 и его PNG/settings; строка 96 назначает командные HD картинки П10.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'Р30|Р33|Р34|Р63|Р66' 284961e88b21079c548ed638ad4e4735920d6729 -- docs/decisions.md. Вывод: decisions.md:38 требует отсутствие overlaps/conflicts во всём интерфейсе по scales/sizes, labels, click intersections, key conflicts и полноту screen catalog; :41 определяет WorldScale как camera zoom на старте и после Z; :42 фиксирует HD4 packs и отсутствие classic mode/fallback; :92 требует сохранять наработки форка и брать новую функциональность апстрима; :95 фиксирует переменный холст RenderScale для адаптивного П5.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'RenderScale|WorldScale|Масштаб игры|Размер объектов|Game scale|Object size' 0a33444e9032ef935dfe4cdde6bb622771484230 -- src/gamestates/cOptionsState.cpp src/gui. Вывод пустой, код возврата 1.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/game/cGame_logic.cpp | nl -ba | sed -n '752,774p'. Вывод: 752 создаёт cSDLSystem; 756 один раз вызывает applyRenderScale; 771–774 затем записывает canvas width/height и OutputHeight и выводит world-scale zoom.
- Команда: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '44,54p;71,74p'. Вывод: строка 45 инициализирует zoom из getWorldScaleFactor; 71–74 resetZoom повторно берёт getWorldScaleFactor и ставит zoom.

### Изменение WorldScale во время игры

Вариант 1 — немедленно вызвать обновление зума камеры. Текущий cMapCamera имеет resetZoom(), который повторно берёт getWorldScaleFactor; но это изменит текущий zoom и может сбросить ручную позицию/величину зума игрока.

Вариант 2 — сохранить выбранное WorldScale и применить при новом запуске. Рекомендация — после перезапуска: П4б фиксирует WorldScale от высоты вывода на запуск и оставляет его неизменным до конца игры, а Р33 задаёт его как стартовый zoom и значение после Z. В PORT настройки читаются при запуске и камера использует их при создании/reset; UI live setter отсутствует. Запись WorldScale в preferences.ini относится к П8. Вариант «сразу через zoom камеры» потребовал бы согласовать сброс текущего zoom и точку его применения. Источники: решения Р33 и Р66 — docs/decisions.md@284961e:41,95; cMapCamera.cpp@0a33444:44–54,71–74; docs/upstream/PORT_PLAN.md@284961e:89,93.
- Решено исполнителем: WorldScale → выбор вступает в силу при перезапуске и сохраняется в П8; было — камера использует стартовый scale и не имеет настроечного live control, стало бы — вызов resetZoom сбрасывал бы zoom во время текущей сессии; основание: Р33, контракт П4б и назначение записи preferences шагу П8.

### Перенос ui-audit

Вариант 1 — перенести полностью внутри П5. Один критерий Р30 покроет все перенесённые экраны; риск — крупный переход частных доступов и тестовых инструментов одновременно с геометрией.

Вариант 2 — перенести в двух частях П5 после adaptive-layout: сначала каталог/аргументы/доступ к объектам и lifecycle/сбор PNG+JSONL; затем подключить все code hooks, tools и tests для Р30 к портовым состояниям. Риск — промежуточная часть сама не завершает аудит. Рекомендация — разделить П5 на эти два этапа, но считать ui-audit обязательной второй частью приёмки П5. Полный вариант следует Р30; отдельный независимый шаг после П5 отложил бы проверку геометрии дольше.
- Минимум для Р30 в PORT: каталог должен покрывать каждое игровое состояние или иметь явное исключение; команда должна перечислять доступные RenderScale/WorldScale; capture должен собирать текст, UI rects, labels, click areas и credits с их владельцем и сохранять PNG/JSONL; scripts должны проверить геометрические правила 1–9, десятое правило key conflicts, полноту scenes и ожидаемых outputs. Р30 — docs/decisions.md@284961e:38. В FORK1 эти точки находятся в файлах, перечисленных в ui-audit.tsv; в PORT соответствия нет.
- Ограничение фактической проверки: runtime scripts, CTest, сборка и игра не запускались; описание сообщает контракт/входы, но не доказывает, что аудит успешно проходит на FORK1.

### Другие развилки и найденные ограничения

- CTest runtime UI audit по умолчанию отключён, поэтому наличие runtime test scripts не означает их запуска стандартной конфигурацией; явное включение требуется для приёмки этих сценариев. CMakeLists.txt@9208dcf:456–475.
- Скirmish preview в PORT выходит за холст на всех заданных высотах: правый overflow 115/235/475 px и нижний overflow 55 px. Это точное поведение исходной формулы, не предположение по скриншоту. Если ведущий решит исправить его в П5, ожидаемое расположение должно быть записано в задании и покрыто приёмочным тестом.
- Размеры PNG и нативных классических текстур, кроме зафиксированных в pointer metadata, не измерялись. В screens.tsv выводы сделаны по формулам и размерам, которые явно заданы кодом.

