# Задание P17 — панель приказов: вид кнопок настроек и значки, нарисованные кодом

Исполнитель: субагент Claude Sonnet. Первым действием вызови навык `team-process-claude` (ты — исполнитель Claude: прочитай ядро и `executor-rules.md`). Отвечай по-русски, код и коммиты — по-английски. Рабочая копия: `C:\Users\Slaven\Projects\DUNE-p2` (Git Bash), ветка `p17/command-bar` от `6d7aa74443d751a4bf7d2aa7db6413b991b264f1` (вершина ветки порта `port/up-d06f2fcd`). Временные файлы — `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\p17\` (удалять только её содержимое). Коммитишь сам, локально; push, PR и слияние делает ведущий.

## Цель

Семь кнопок панели приказов внизу слева игрового экрана (`cCommandBarDrawer`) выглядят как кнопки экрана настроек и несут значки, нарисованные кодом, по смыслу действия; включённый режим и наведение видны; при наведении — подсказка. Решение владельца Р86 (`C:\Users\Slaven\Projects\DUNE\docs\decisions.md`, последняя запись), карточка `C:\Users\Slaven\Projects\DUNE\codex-direct\P17\CARD-P17.md`. Доказательство — тесты `[P17]`, полный CTest на Windows, снимки сцен.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом Read:

- `C:\Users\Slaven\Projects\DUNE\codex-direct\P1\windows.md` — сборка и запуск на Windows;
- `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\orders\RECON-orders.md` — разведка панели;
- `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\orders\cursors.png` — знаки курсоров на карте (образец формы прицела и разводного ключа);
- в рабочей копии: `src/drawers/cCommandBarDrawer.h`, `src/drawers/cCommandBarDrawer.cpp`, `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp`, `src/drawers/SDLDrawer.hpp`, `src/drawers/SDLDrawer.cpp`, `src/gui/GuiTheme.hpp`, `src/gui/GuiButton.cpp`, `src/gamestates/ResolutionDialog.cpp`, `tests/drawers/test_CommandBarLayout.cpp`, `tests/controls/test_CommandPolicies.cpp`, `tests/ui_audit/ui_audit_part3b_scenes.py`, `packaging/make_common_assets.sh`.

## Подготовка

`git -C C:/Users/Slaven/Projects/DUNE-p2 status --short` — пусто, иначе стоп. `git -C C:/Users/Slaven/Projects/DUNE-p2 fetch -q origin +refs/heads/port/up-d06f2fcd:refs/remotes/origin/port/up-d06f2fcd`, затем `git -C C:/Users/Slaven/Projects/DUNE-p2 switch -q -c p17/command-bar 6d7aa74443d751a4bf7d2aa7db6413b991b264f1`; `git rev-parse HEAD` — этот SHA, иначе стоп. Журнал хода — `scratchpad\p17\progress.md`, строка на закрытый шаг.

## Контракт

1. **Значки — данные, а не картинки.** Новые файлы `src/drawers/CommandIcons.hpp` и `src/drawers/CommandIcons.cpp` (добавить в список исходников `src/CMakeLists.txt` рядом с `drawers/cCommandBarDrawer.cpp`):
   - `enum class CommandIcon { Move, Attack, Repair, Unload, Deploy, Rally, Release };`
   - фигуры в сетке 64×64 (0..64 по обеим осям): ломаная с толщиной и круглыми концами (`Stroke`), дуга окружности с толщиной (`Arc`: центр, радиус, начальный и конечный угол, толщина), закрашенный выпуклый многоугольник (`Fill`), закрашенный круг (`Dot`);
   - `[[nodiscard]] const std::vector<IconShape> &commandIconShapes(CommandIcon icon);`
   - `[[nodiscard]] std::vector<SDL_Vertex> tessellateCommandIcon(CommandIcon icon, float sizePixels, SDL_FColor color);` — треугольники (число вершин кратно 3) в квадрате `[0, sizePixels]`; дуги и круги — не меньше 24 отрезков на полный круг; круглые концы ломаных — закрашенный круг диаметром толщины.
   - Значки (линии толщиной 5 из 64, кроме оговорённого): **Move** — стрелка вправо: древко и наконечник-шеврон; **Attack** — прицел по образцу курсора атаки: окружность и четыре риски внутрь, точка в центре; **Repair** — разводной ключ по образцу курсора ремонта: диагональная рукоять толщиной 7 из левого нижнего угла в правый верхний и раскрытый зев на конце (дуга с разрывом); **Unload** — капля пряности сверху и стрелка вниз в лоток; **Deploy** — квадрат фундамента в центре и четыре стрелки наружу от его сторон; **Rally** — вертикальное древко, треугольный флажок вправо от его верхней части, короткое основание; **Release** — проём ворот (дуга-арка со стойками) слева и стрелка из него вправо. Отступ всех фигур от краёв сетки — не меньше 6.
2. **Рисование значка.** В `cCommandBarDrawer`: для каждого значка один раз на размер кнопки строится белая текстура-цель размером 4× стороны значка (`SDL_CreateTexture` с `SDL_TEXTUREACCESS_TARGET`, прозрачная очистка, `SDL_RenderGeometry` вершин `tessellateCommandIcon(icon, 4 * side, white)`), режим масштаба `SDL_SCALEMODE_LINEAR`, смешение `SDL_BLENDMODE_BLEND`; выводится в кнопку размером `side` по центру, цвет состояния — `SDL_SetTextureColorMod`/`SDL_SetTextureAlphaMod`. `side` — 70 % меньшей стороны кнопки, округление вниз. Кэш пересобирается при смене `side`. Текущую цель отрисовки сохранить до переключения и вернуть после; если в коде уже есть способ рисовать в текстуру (`git grep -n "SDL_SetRenderTarget" -- src`) — делать тем же способом. Если при включённой логической раскладке (`SDL_SetRenderLogicalPresentation`) переключение цели ломает раскладку кадра — `Q` и стоп.
3. **Вид кнопки.** Фон и рамку каждой кнопки рисовать тем же кодом, каким `GuiButton` рисует вид `GuiRenderKind::REMASTER_BUTTON`; если этот код недоступен снаружи `GuiButton`, вынести его в свободную функцию в `src/gui/` и вызывать из обоих мест (поведение `GuiButton` не меняется). Прямоугольник кнопки — прямоугольник раскладки `CommandBarLayout`, сжатый на 2 px с каждой стороны. Фон панели под кнопками — `renderRectFillColor` цветом `panelColor` этого файла и рамка `panelBorder`. Состояния (тема `GuiTheme::Remaster()`):
   - выключена — цвета `disabled*` темы, значок `disabledTextColor`;
   - включена — `fillColor`/`borderLight`/`borderDark`, значок `textColor`;
   - под курсором (поле `m_hoveredButton`) и включена — значок `textColorHover`;
   - режим кнопки включён — заливка `{63, 52, 31, 255}`, рамка `{188, 137, 42, 255}`/`{232, 184, 78, 255}` (как выбранная строка в `ResolutionDialog.cpp`), значок `textColorHover`. Режим включён: Атаковать — когда идёт выбор цели атаки, начатый `activateAttackCommand`; Ремонт — когда состояние мыши `MOUSESTATE_REPAIR`; Точка сбора — когда идёт выбор точки, начатый `activateRallyPointCommand`; Переместить — когда идёт выбор точки, начатый `activateMoveCommand`; у остальных режима нет. Проверка — чистой функцией `[[nodiscard]] bool isCommandButtonActive(<команда>, <состояние, которое вы читаете из cGameControlsContext>)` в `CommandBarPolicy.hpp`.
4. **Клавиша и подсказка.** Чистые функции в `CommandBarPolicy.hpp`: `cornerKeyLabel(const std::string &keyLabel)` — сама подпись, если в ней ровно один символ Юникода, иначе пустая строка; `commandTooltip(const std::string &caption, const std::string &keyLabel)` — `"<caption> (<keyLabel>)"`, а при пустой `keyLabel` — `caption`. У «Точки сбора» подписи клавиши нет (сейчас ей ошибочно дана подпись атаки CTRL). Буква `cornerKeyLabel` — в правом нижнем углу кнопки малым шрифтом, которым сейчас выводятся подписи клавиш на панели, цвет `textColor`, только у включённых кнопок; овалов нет. Подсказка — над панелью при наведении на кнопку: прямоугольник `fillColor` с рамкой `borderLight`, текст `textColor`, отступы 6 px, низ подсказки на 6 px выше верха панели, по центру кнопки по горизонтали, сдвиг внутрь экрана, если выходит за край. Если в коде уже есть общий способ подсказок (`git grep -n -i "tooltip" -- src`) — использовать его.
5. **Картинки удалить:** `resources/bin/data/hd4/command_bar.png`, `resources/bin/data/hd4/command_bar_disabled.png` (`git rm`), их загрузку в `cCommandBarDrawer.cpp`, строки в `packaging/make_common_assets.sh`, прежний запасной `drawIcon` и `blueFilter`. Других упоминаний (`git grep -n "command_bar" -- . ':!*.md'`) не остаётся; если они есть в тестах или инструментах — поправить их там же и перечислить в сдаче.
6. **Сцена режима отладки интерфейса** `game-command-repair-mode` по образцу сцен `game-command-*` (`src/debug/UiAuditScenes.cpp`): выбран повреждённый юнит, включён режим ремонта, курсор над кнопкой Ремонт (видны золотая заливка и подсказка). Если сцены перечислены ещё в файлах тестов или инструментов (`git grep -n "game-command-mcv" -- tests tools`) — добавить туда так же.
7. Захват в лямбду констант с константным инициализатором запрещён (CI на macOS собирает clang с `-Werror`, `-Wunused-lambda-capture`). Предупреждений `warning:` в сборке не добавлять.

## Тесты (`tests/drawers/test_CommandIcons.cpp`, добавить в `tests/CMakeLists.txt` там же, где `test_CommandBarLayout.cpp`) — сначала красные

`TEST_CASE(..., "[P17]")`:
- у каждого из 7 значков `commandIconShapes` не пуст; все точки фигур с учётом половины толщины лежат в `[6, 58]`;
- `tessellateCommandIcon(icon, 48.0f, color)` для каждого значка: число вершин > 0 и кратно 3, все координаты в `[0, 48]`, цвет вершин — переданный;
- `cornerKeyLabel("R") == "R"`, `cornerKeyLabel("CTRL") == ""`, `cornerKeyLabel("ЛКМ") == ""`, `cornerKeyLabel("") == ""`;
- `commandTooltip("Ремонт", "R") == "Ремонт (R)"`, `commandTooltip("Точка сбора", "") == "Точка сбора"`;
- `isCommandButtonActive`: Ремонт активен в режиме ремонта и не активен вне его; Атаковать активен в режиме выбора цели атаки; Развернуть не активен ни в одном режиме.

Ожидания существующих тестов не меняются; падает существующий тест — `Q` и стоп.

## План

| Шаг | Что | Кто |
|---|---|---|
| 0 | Навык, чтение, подготовка, журнал | ты |
| 1 | Тесты `[P17]`; красная сборка тестов — лог `scratchpad\p17\red.log` | ты |
| 2 | Контракт 1 и 4 (данные, чистые функции); тесты `[P17]` зелёные | ты |
| 3 | Контракт 2, 3, 5 (рисование, вид, удаление картинок) | ты |
| 4 | Контракт 6 (сцена) | ты |
| 5 | Проверки и коммиты | ты |

## Проверки

1. Сборка и полный CTest на Windows по `windows.md` (каталог `C:\Users\Slaven\Projects\DUNE-p2\build`, `CCACHE_DISABLE=1`): код 0, `100% tests passed`, число тестов = 568 + число новых случаев `[P17]`; ни одной строки `warning:` в логе сборки, которой нет в `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\res\ship\build.log`. Логи — `scratchpad\p17\build.log`, `scratchpad\p17\ctest.log`.
2. Снимки сцен `game-command-damaged-unit`, `game-command-harvester`, `game-command-mcv`, `game-command-repair-mode` в 1920×1080 (`d2tm.exe -windowed -screenWidth 1920 -screenHeight 1080 --ui-audit-scene <id> --ui-audit-out <папка>`; запуск из PowerShell, из каталога запуска по `windows.md`, PATH без MSYS2; `preferences.ini` из `%APPDATA%\D2TM\Dune II - The Maker\` до снимков скопировать в `scratchpad\p17\preferences.ini.bak` и после вернуть побайтно, sha256 равны). PNG сложить в `scratchpad\p17\shots\<id>.png`. Плюс лист `scratchpad\p17\shots\icons.png`: панель, вырезанная из снимка `game-command-damaged-unit` по прямоугольнику области `command-bar` из файла `.geometry.jsonl` этого снимка и увеличенная в 4 раза методом ближайшего соседа (скрипт Python с Pillow: `C:\Users\Slaven\AppData\Local\Programs\Python\Python313\python.exe`). Вид не оценивай: его смотрит ведущий.
3. `git grep -n "command_bar" -- . ':!*.md'` — пусто или только перечисленное в сдаче.
4. Коммиты (по правилам исполнителя): тесты — отдельным коммитом; код — следующим; последняя строка каждого — `Behavior changes: ...`; подпись `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. `git status --short` — пусто.

## Сдача

Блок `## DONE-P17 | <время> | HEAD <sha>` файлом `scratchpad\p17\DONE-P17.md` (в ответе — путь и до 10 строк): журнал хода, красный прогон (первые 20 строк), каждая проверка — команда, код выхода, главные строки, SHA коммитов, `git diff --stat` от `6d7aa744`, пути PNG, «Решено исполнителем», «Не проверено», «Рабочие места».

## Организация работы

- **Порядок:** шаги 0 → 1 → 2 → 3 → 4 → 5.
- **Параллельно:** нет.
- Помощники: 0. Ожидаемое время — 2 часа.
- **Остановки:** `## Q-P17-NN` с выводом — файлом `scratchpad\p17\Q-P17-NN.md`, в ответе путь, и стоп.
- **Рамка правок:** файлы контракта, `src/CMakeLists.txt`, `tests/CMakeLists.txt`, `tests/drawers/test_CommandIcons.cpp`, найденные по пунктам 5 и 6 контракта файлы тестов и инструментов, `scratchpad\p17\`.
- Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
