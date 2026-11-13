# Задание P13 — эталонные снимки старой и новой сборки, новые снимки галереи (шаг П13)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p13`, ветка `codex/p13`, `HEAD` — `0683500a829556942723703183692b29be39d539`, вершина ветки порта `port/up-d06f2fcd` после слияния П12 (PR #145). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p13/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p13/` (дальше — «папка задания»); файлы разведки — в `/srv/dune/tasks/p13/recon/`.

## Цель

Для каждой пары «сцена старой сборки — сцена новой сборки» из списка пар один вызов инструмента `tools/ui-audit/reference_shots.py` на весь список даёт два снимка в одинаковом разрешении (у пар без сцены старой сборки — `skirmish-hud`, `mentat-briefing-sardaukar` — один снимок новой и заглушка слева) и лист «старое | новое» рядом в одном PNG, а также таблицу `reference.tsv`; режим `--gallery` даёт пять снимков сцен порта под именами пяти файлов галереи README. Готово, когда новые тесты Python зелёные, сборка порта со всеми тестами CTest зелёная, инструмент на сервере без старой сборки прошёл все 31 «ячейку» (пара × разрешение) списка пар с кодами выхода 0 и нужными размерами PNG, а режим `--gallery` дал пять PNG 1920×1080. Код игры (`src/`, `tests/*.cpp`, `CMakeLists.txt`) шаг не меняет.

## Что уже решено

Ревизии. `B13` = `6bd02eb55d4cb3ad3a69be9384d1514d8fb517bd` — вершина порта со всеми шагами П1–П11, П8а и П10в (в ней нет файлов П12). `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566` — вершина форка и одновременно коммит тега `v0.8.0-ru-hd.10` (проверено: `git rev-parse 'v0.8.0-ru-hd.10^{commit}'` даёт `FORK1`). Значит старая сборка — выпуск `v0.8.0-ru-hd.10` — собрана из `FORK1`, и режим отладки интерфейса есть в ней целиком. Разведка (`recon/`) сделана по `010a6eb134661660a077279bb94a36f063b97d7a`; сверка с `B13`: файлы `src/debug/UiAuditArguments.cpp`, `src/debug/UiAuditCapture.cpp` и `src/utils/RenderScale.cpp` по существу те же (строки заголовка геометрии `UiAuditCapture.cpp@B13:175-180`); каталог сцен порта в `B13` — 192 сцены вместо 185: добавлены `game-factory-pad`, `game-radar-dish`, `game-refinery-harvester`, `options-game-game`, `options-game-controls`, `options-game-diagnostics`, `options-game-keybind` (`git show B13:src/debug/UiAuditScenes.cpp | grep -o 'scene("[^"]*"'`). Сцен `FORK1` — 157.

- **Режим отладки обеих сборок.** Аргументы одинаковы: `-windowed -screenWidth <W> -screenHeight <H> --ui-audit-scene <сцена> --ui-audit-out <папка>` (`recon/screen-size.tsv`, `recon/output.tsv`). `--ui-audit-list` печатает JSON `{"scenes":[{"id":...},...]}` и выходит с кодом 0 (`UiAuditCapture.cpp@B13:414-434`, `@FORK1:395-`). Прогон пишет `<сцена>.png` и `<сцена>.geometry.jsonl` в `--ui-audit-out`; первая строка JSONL — запись `"k":"header"` с ключами `scene`, `resolution`, `language`, `graphics`, `canvas` (`w`, `h`), `game_screen`, `render_scale`, `world_scale`. Код выхода 0 — успех, 1 — сцена не подготовлена, 2 — ошибка аргументов (`UiAuditCapture.cpp@B13:388-451`, `src/main.cpp@FORK1:132-134`).
- **Размер.** В режиме отладки окно и вывод рендера равны запрошенному размеру в обеих сборках (`src/game/cSDLSystem.cpp@B13:207-211`, `src/utils/cScreenInit.cpp@FORK1:127-128`), PNG имеет размер вывода. Холст при «Авто» (`RenderScale=0`) считает `calculateRenderCanvasSize` (`src/utils/RenderScale.cpp@B13:51-73`, в `FORK1` то же): масштаб = меньшее из `ширина/800`, `высота/600`; холст = размер вывода / масштаб, округление `lround`. Ожидаемые холсты: 800×600 → 800×600; 1920×1080 → 1067×600; 5120×1440 → 2133×600.
- **Язык.** Порт в режиме отладки берёт язык из `--ui-audit-language` (`en` по умолчанию, `src/main.cpp@B13:142-144`) и пишет в заголовок всегда `"language":"en"` (`UiAuditCapture.cpp@B13:176`, известная ошибка, issue #133). Форк аргумента языка не знает: язык берёт из `settings.ini` рядом с исполняемым файлом (`Language=ru` в выпуске, `resources/bin/settings.ini@FORK1:10`) и пишет настоящий язык в заголовок (`UiAuditCapture.cpp@FORK1:162`).
- **Масштабы.** Порт при каждом запуске читает ключи `RenderScale` и `WorldScale` из `preferences.ini` в папке данных пользователя (`src/main.cpp@B13:107-111`); форк — из `settings.ini` (`src/utils/common.cpp@FORK1:65-66`). Для сравнимых снимков оба значения должны быть 0 («Авто»); заголовок геометрии пишет их в `render_scale` и `world_scale`.
- **Рабочая папка.** Форк при любом запуске делает рабочей папкой папку исполняемого файла (`src/main.cpp@FORK1:34-50,85`); порт в режиме отладки рабочую папку не меняет (`src/main.cpp@B13:88-90`), она должна содержать ресурсы игры. Инструмент для обеих сборок запускает файл с `cwd` = папка этого файла.
- **Запись на диск.** Форк в сценах с сохранениями пишет `saves/` в свою папку (`UiAuditAccess::writeSaves`, `src/debug/UiAuditAccess.cpp@FORK1:138-147`). Эти сцены форка называются в константе `SAVE_WRITING_FORK_SCENES` (контракт, п. 2) и в списке пар не участвуют. Порт пишет сохранения сцен в `<--ui-audit-out>/saves` (`UiAuditCapture.cpp@B13:474-475`).
- **Пары сцен.** Источник — `recon/screens.tsv`, `recon/scenes.tsv`. Выбор — в таблице ниже; доводы — в столбце «довод».
- **Сборка и тесты порта** — как в `TASK-P10B.md`: `df -m /srv/library`; сборка `CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489`; для запуска собранных файлов `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib`. Папка запуска собранной игры — `.tmp/out/run/bin` (файл `d2tm`, ресурсы).
- **Сборка форка на сервере не делается** (SDL2 нет, пакеты ставить нельзя). Прогон на Windows — ведущий после сдачи; ты его не выполняешь.
- **Вид оценивает ведущий** (Р70). Ты снимки не смотришь и не оцениваешь: проверяешь только числа и коды.

### Таблица пар (список пар `tools/ui-audit/reference_pairs.tsv`, 27 пар, 31 ячейка)

| пара | сцена форка | сцена порта | разрешения | довод |
|---|---|---|---|---|
| `main-menu` | `main-menu` | `main-menu` | 1920×1080 | экран «главное меню»; сцена в обеих ревизиях (`screens.tsv`, строка 2) |
| `options-main` | `options-menu-main` | `options-menu-main` | 1920×1080 | экран «настройки», вход из меню; сцена в обеих ревизиях, подготовка `prepareOptionsMenu<0>` |
| `options-applied` | `options-menu-applied` | `options-menu-applied` | 1920×1080 | та же страница со строкой «Сохранено. Перезапустите игру.» (`UiAuditAccess::optionsStatus` только меняет подпись, на диск не пишет) |
| `options-page-game` | `options-menu-game` | `options-game-game` | 1920×1080 | страница «Игра»; у порта страницы есть только в сценах с входом из боя (`B13:UiAuditScenes.cpp` `readyOptionsPage<1>`), у форка — в сценах `options-menu-*`; сцены форка `options-game-*` пишут `saves/` и исключены. Вход различается — вопрос Q1 |
| `options-page-controls` | `options-menu-controls` | `options-game-controls` | 1920×1080 | страница «Управление»; то же |
| `options-page-diagnostics` | `options-menu-diagnostics` | `options-game-diagnostics` | 1920×1080 | страница «Диагностика»; то же |
| `options-page-keybind` | `options-menu-keybind` | `options-game-keybind` | 1920×1080 | страница «Управление» с захватом клавиши (`optionsBinding` в обеих ревизиях); то же |
| `skirmish-hud` | нет | `save-roundtrip` | 800×600, 1920×1080, 5120×1440 | экран «схватка с боковой панелью»: у форка сцены нет (`git grep -n startSkirmish FORK1 -- src/debug` — пусто, код 1); в порту единственная сцена схватки с боевым HUD (`UiAuditScenes.cpp@B13:374-378`: `startSkirmish`, площадки, круг сохранения) |
| `mission-hud` | `game-hud` | `game-hud` | 800×600, 1920×1080, 5120×1440 | экран «миссия кампании с боковой панелью»; Атрейдес, миссия 1, в обеих ревизиях (`prepareGame<ATREIDES, uiaudit::Hud>`) |
| `campaign-map-intro` | `region-atreides-intro-1` | `region-atreides-intro-1` | 1920×1080 | экран «карта кампании», начало кампании |
| `campaign-map-select` | `region-ordos-select-3` | `region-ordos-select-3` | 1920×1080 | экран «карта кампании», выбор области |
| `mentat-briefing-atreides` | `mentat-briefing-atreides-await` | `mentat-briefing-atreides-await` | 1920×1080 | экран «ментат», состояние «ждёт щелчка»: речь допечатана, кадр устойчив |
| `mentat-briefing-ordos` | `mentat-briefing-ordos-await` | `mentat-briefing-ordos-await` | 1920×1080 | то же для Ордосов |
| `mentat-briefing-harkonnen` | `mentat-briefing-harkonnen-await` | `mentat-briefing-harkonnen-await` | 1920×1080 | то же для Харконнен |
| `mentat-win-ordos` | `mentat-win-ordos-await` | `mentat-win-ordos-await` | 1920×1080 | ментат после победы |
| `tellhouse-ordos` | `tellhouse-ordos-await` | `tellhouse-ordos-await` | 1920×1080 | ментат выбранного Дома (`GAME_TELLHOUSE`) |
| `mentat-briefing-sardaukar` | нет | `mentat-briefing-sardaukar-await` | 1920×1080 | четвёртый Дом есть только в порту (`scenes.tsv`, `screens.tsv`, строка 7) |
| `credits-title` | `credits-title` | `credits-title` | 1920×1080 | экран «титры» |
| `credits-1` … `credits-5` | `credits-1` … `credits-5` | `credits-1` … `credits-5` | 1920×1080 | экран «титры»: по одной паре на положение прокрутки; пять пар — пять строк файла |
| `choose-house` | `choose-house` | `choose-house` | 1920×1080 | выбор Дома (`GAME_SELECT_HOUSE`); сцена в обеих ревизиях, `scenes.tsv`; у порта четыре карточки, у форка три |
| `select-mission-ordos` | `select-mission-ordos` | `select-mission-ordos` | 1920×1080 | выбор миссии (`GAME_MISSIONSELECT`, `prepareSelectMission<ORDOS>`); сцена в обеих ревизиях, `scenes.tsv` |
| `outcome-win` | `outcome-win` | `outcome-win` | 1920×1080 | экран победы (`GAME_WINNING`, `prepareOutcome<true>`); сцена в обеих ревизиях |
| `outcome-lose` | `outcome-lose` | `outcome-lose` | 1920×1080 | экран поражения (`GAME_LOSING`, `prepareOutcome<false>`); сцена в обеих ревизиях |

Итого 27 пар: 7 (главное меню и настройки) + 2 (бой) + 2 (карта кампании) + 6 (ментат) + 6 (титры) + 4 (выбор Дома, выбор миссии, победа, поражение); ячеек: 7 + 3 + 3 + 2 + 6 + 6 + 4 = 31 (`skirmish-hud` и `mission-hud` — по три, остальные — по одной). Ячеек старой сборки — 27 (у `skirmish-hud` три и у `mentat-briefing-sardaukar` одна ячейка без сцены форка).

### Таблица галереи (`tools/ui-audit/reference_gallery.tsv`, режим `--gallery`)

Источник — подписи и подписи-картинки галереи README (`README.md` ветки `codex/p12` коммит `4921ea629`, строки 7–28, и `README.md@FORK1`, строки 7–28; в `B13` галереи ещё нет, она приходит в PR #145, который вошёл в `HEAD` рабочей копии).

| файл `docs/screenshots/` | подпись README (alt / sub) | сцена порта | разрешение | довод |
|---|---|---|---|---|
| `main-menu.png` | «Remastered main menu» | `main-menu` | 1920×1080 | то же меню |
| `house-selection.png` | «House selection screen» / «Choose your House» | `choose-house` | 1920×1080 | сцена `GAME_SELECT_HOUSE` (`UiAuditScenes.cpp@B13:464`) |
| `ordos-briefing.png` | «Ordos campaign briefing» / «Remastered campaign briefing» | `mentat-briefing-ordos-await` | 1920×1080 | брифинг Ордосов, ждущий щелчка |
| `skirmish-gameplay.png` | «HD skirmish gameplay» / «HD gameplay and redesigned interface» | `save-roundtrip` | 1920×1080 | единственная сцена схватки с HUD; запасной вариант — `game-hud` — вопрос Q2 |
| `victory-screen.png` | «Victory screen» | `outcome-win` | 1920×1080 | экран победы (`GAME_WINNING`) |

Сами файлы `docs/screenshots/*.png` и подписи в `README.md` меняет ведущий после своего осмотра; в рамку правок исполнителя они не входят.

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом (пути без `/srv/` — от корня рабочей копии):

- `tools/ui-audit/run_combo.py` целиком;
- `tools/ui-audit/combos.py` целиком;
- `tools/ui-audit/build_sheets.py` строки 1–120;
- `tools/ui-audit/tests/test_run_all.py` строки 1–40;
- `tests/ui_audit/ui_audit_runtime_support.py` целиком;
- `src/debug/UiAuditArguments.cpp` целиком;
- `src/debug/UiAuditCapture.cpp` строки 160–300 и 380–490;
- `src/utils/RenderScale.cpp` целиком;
- `/srv/dune/tasks/p13/recon/screens.tsv`, `/srv/dune/tasks/p13/recon/screen-size.tsv`, `/srv/dune/tasks/p13/recon/output.tsv`;
- `README.md` строки 1–40;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | sed -n '155,185p;395,440p'`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '138,148p'`.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт

У шага нет тестов форка: в `FORK1` нет файла этого инструмента (`git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -i -E 'reference_shots|reference_pairs'` — пусто). Таблицы «проверка форка → случай Catch2» нет; тесты — Python `unittest`, раздел «Тесты».

Все новые файлы — в `tools/ui-audit/`. Python 3, стандартная библиотека и `PIL` (`/usr/bin/python3` его содержит; `build_sheets.py` использует его так же). Путь — только `pathlib`. Файл не зависит от других модулей `tools/ui-audit/`.

1. **Файлы.** Четыре новых: `tools/ui-audit/reference_shots.py`, `tools/ui-audit/reference_pairs.tsv`, `tools/ui-audit/reference_gallery.tsv`, `tools/ui-audit/tests/test_reference_shots.py`. Существующие файлы не меняются.

2. **Константы `reference_shots.py`.**
   ```python
   CELL_MAX_WIDTH = 1280
   HEADER_HEIGHT = 28
   GAP = 16
   BACKGROUND = (24, 24, 24)
   TEXT = (235, 235, 235)
   PLACEHOLDER = (40, 40, 40)
   SCENE_TIMEOUT_SECONDS = 120
   SCENE_ATTEMPTS = 2
   LIST_TIMEOUT_SECONDS = 60
   TABLE_HEADER = ("pair", "resolution", "old_scene", "new_scene", "old_exit", "new_exit", "old_png_size",
                   "new_png_size", "old_canvas", "new_canvas", "old_png", "new_png", "sheet", "problems")
   GALLERY_HEADER = ("file", "scene", "resolution", "exit", "png_size", "canvas", "problems")
   SAVE_WRITING_FORK_SCENES = frozenset({
       "main-menu-saves", "save-dialog-menu", "options-game-main-saves", "options-game-applied",
       "options-game-game", "options-game-controls", "options-game-diagnostics", "options-game-keybind",
       "save-dialog-load", "save-dialog-save-new", "save-dialog-overwrite", "save-dialog-load-error",
       "save-dialog-save-error",
   })
   ```
   В `SAVE_WRITING_FORK_SCENES` — ровно 13 сцен `FORK1`, подготовка которых (`prepareMenuWithSaves`, `prepareGameOptions<true>`) вызывает `UiAuditAccess::writeSaves` (`src/debug/UiAuditScenes.cpp@FORK1:222-231,248-259,481-506`; список — `recon/scenes.tsv`, столбец «функция подготовки»).

3. **Данные пар.** `reference_pairs.tsv` — UTF-8, строки с `\n`, разделитель — символ табуляции, первая строка — `pair`, `fork_scene`, `port_scene`, `resolutions`, `note` (через табуляцию), затем 27 строк таблицы пар в том же порядке, что в таблице выше (`credits-1` … `credits-5` — пять отдельных строк). Столбец `resolutions` — разрешения `ШxВ` через запятую без пробелов; `fork_scene` = `-`, если у форка сцены нет; `note` — `-`, кроме строк `options-page-*`, где `note` = `entry differs: menu / game`. Полный текст файла — в приложении А ниже.

4. **Данные галереи.** `reference_gallery.tsv` — тот же формат; первая строка — `file`, `port_scene`, `resolution`; пять строк таблицы галереи. Полный текст — в приложении А.

5. **Функции `reference_shots.py`.** Имена и сигнатуры — ровно такие (тесты вызывают их по именам):
   - `Pair` — `collections.namedtuple("Pair", "name fork_scene port_scene resolutions note")`; `fork_scene` — `None`, если в файле `-`; `resolutions` — список кортежей `(ширина, высота)`.
   - `GalleryRow` — `namedtuple("GalleryRow", "file port_scene resolution")`; `resolution` — кортеж `(ширина, высота)`.
   - `parse_pairs(path) -> list[Pair]`. Первая строка должна быть заголовком из п. 3; в каждой следующей непустой строке ровно 5 полей; имя пары не повторяется; каждое разрешение — `^\d+x\d+$`; `port_scene` не `-`; `fork_scene` не из `SAVE_WRITING_FORK_SCENES`. Любое нарушение — `ValueError`.
   - `parse_gallery(path) -> list[GalleryRow]` — заголовок из п. 4, 3 поля в строке, разрешение `^\d+x\d+$`, имя файла не повторяется; нарушение — `ValueError`.
   - `executable_name(os_name) -> str` — `"d2tm.exe"` для `"nt"`, иначе `"d2tm"`.
   - `scene_command(executable, side, scene, width, height, out_dir, language) -> list[str]` — `[str(executable), "-windowed", "-screenWidth", str(width), "-screenHeight", str(height), "--ui-audit-scene", scene, "--ui-audit-out", str(out_dir)]`; при `side == "new"` в конец добавляются `"--ui-audit-language", language`. `side` — `"old"` или `"new"`.
   - `game_environment(base, headless, xdg) -> dict` — копия `base`; при `headless` добавляются `SDL_VIDEODRIVER=dummy`, `SDL_RENDER_DRIVER=software`, `SDL_AUDIODRIVER=dummy`, `XDG_DATA_HOME=str(xdg)`.
   - `default_runner(command, cwd, env, timeout)` — `subprocess.run(command, cwd=cwd, env=env, check=False, capture_output=True, text=True, timeout=timeout)`.
   - `list_scenes(executable, runner, env) -> set[str]` — `runner([str(executable), "--ui-audit-list"], executable.parent, env, LIST_TIMEOUT_SECONDS)`; код выхода не 0 — `RuntimeError`; результат — множество `scene["id"]` из `json.loads(stdout)["scenes"]`.
   - `png_size(path) -> tuple[int, int]` — читает ширину и высоту из блока `IHDR` (байты 16–24); файл короче 24 байт или без подписи `\x89PNG\r\n\x1a\n` — `ValueError`.
   - `read_header(path) -> dict` — первая строка файла как JSON; не объект с `"k": "header"` — `ValueError`.
   - `cell_problems(side, exit_code, size, header, width, height, language) -> list[str]`; порядок: `f"exit={exit_code}"`, если `exit_code != 0`; `f"png-size={w}x{h}"`, если `size` не `None` и не `(width, height)`; если `header` не `None`: `f"render-scale={v}"` при `header["render_scale"] != 0`, `f"world-scale={v}"` при `header["world_scale"] != 0`, и только при `side == "old"` — `f"language={x}"` при `header["language"] != language`.
   - `compose_sheet(old_png, new_png, out_png, title)` — `old_png` может быть `None`. Размер ячейки по новому снимку: `f = min(1.0, CELL_MAX_WIDTH / new_w)`, `cw = round(new_w * f)`, `ch = round(new_h * f)`. Лист — RGB-изображение `2 * cw + GAP` на `HEADER_HEIGHT + ch`, фон `BACKGROUND`; старый снимок (приведённый к `cw × ch` фильтром `LANCZOS`) — в точке `(0, HEADER_HEIGHT)`, новый — в точке `(cw + GAP, HEADER_HEIGHT)`; при `old_png is None` на месте старого — прямоугольник `PLACEHOLDER` размера `cw × ch` и в его левом верхнем углу в точке `(8, HEADER_HEIGHT + 8)` текст `no old scene`. `title` рисуется в точке `(8, 8)` цветом `TEXT` шрифтом `ImageFont.load_default()`. Папка `out_png.parent` создаётся.
   - `capture_cell(runner, executable, side, scene, width, height, out_root, language, env) -> CellResult` — `CellResult = namedtuple("CellResult", "exit_code png size canvas header problems")`. Папка ячейки — `out_root / side / f"{width}x{height}"`, создаётся; прежние `<сцена>.png` и `<сцена>.geometry.jsonl` в ней удаляются до запуска. Запуск — `runner(scene_command(...), executable.parent, env, SCENE_TIMEOUT_SECONDS)`; при `subprocess.TimeoutExpired` — повтор до `SCENE_ATTEMPTS` попыток всего; все попытки с таймаутом — `exit_code = "timeout"`, `problems = ["timeout"]`, остальные поля `None`. После запуска папка `<папка ячейки>/saves` удаляется (`shutil.rmtree(..., ignore_errors=True)`). Нет PNG — `"no-png"`; нет файла геометрии — `"no-geometry"`; `read_header` бросил `ValueError` — `"bad-geometry"`; иначе `problems = cell_problems(...)`. `size` — результат `png_size`, `canvas` — `(header["canvas"]["w"], header["canvas"]["h"])`.
   - `run_reference(pairs, out, new_exe, old_exe, old_png_dir, language, runner, env) -> bool`. `old_exe` и `old_png_dir` — оба `None` в режиме «только новое». Порядок: `new_ids = list_scenes(new_exe, ...)`; `old_ids = list_scenes(old_exe, ...)`, если `old_exe` не `None`. Затем для каждой пары в порядке файла и каждого её разрешения в порядке записи — одна строка таблицы:
     - Старая ячейка. Нет сцены форка (`fork_scene is None`) или режим «только новое» — поля старой стороны `-`. `old_exe` задан: сцены нет в `old_ids` — проблема `old:no-scene` без запуска; иначе `capture_cell(..., "old", ...)`. `old_png_dir` задан: файл `old_png_dir / f"{w}x{h}" / f"{fork_scene}.png"`; нет файла — `old:no-png`, есть — `png_size` и проверка `png-size`; код выхода и холст — `-`.
     - Новая ячейка. Сцены нет в `new_ids` — проблема `new:no-scene` без запуска; иначе `capture_cell(..., "new", ...)`.
     - Лист: если новый PNG есть — `compose_sheet(старый PNG или None, новый PNG, out / "sheets" / f"{pair}_{w}x{h}.png", f"{pair} | {w}x{h} | old: {fork_scene or '-'} | new: {port_scene}")`; иначе столбец `sheet` — `-`.
     - Столбец `problems`: `ok`, если проблем нет, иначе проблемы через `;`, каждая с префиксом `old:` или `new:` (`old:exit=1`, `new:png-size=1920x1000`, `new:timeout`).
     - Размеры — `ШxВ`; отсутствующее значение — `-`; код выхода — число или `timeout`; пути — относительно `out` с `/` (`Path.as_posix()`), если файл лежит внутри `out`, иначе — `Path.as_posix()` пути как есть.
     Таблица `out / "reference.tsv"` — `TABLE_HEADER` и строки через табуляцию, UTF-8, `\n` в конце каждой строки. Возвращает `True`, если во всех строках `problems` равен `ok`.
   - `run_gallery(rows, out, new_exe, language, runner, env) -> bool` — для каждой строки `GalleryRow`: `capture_cell(runner, new_exe, "new", row.port_scene, w, h, out / "gallery-raw", language, env)` (сцена должна быть в каталоге, который `run_gallery` сама получает вызовом `list_scenes(new_exe, ...)` один раз до цикла по строкам, иначе проблема `no-scene`); при пустом списке проблем PNG копируется в `out / "gallery" / row.file`. Таблица `out / "gallery.tsv"` — `GALLERY_HEADER`, по строке на файл; `problems` — `ok` или проблемы через `;` без префиксов. Возвращает `True`, если везде `ok`.
   - `main(argv=None) -> int`. Аргументы: `--out` (обязателен), `--new-dir` (обязателен: папка новой сборки с файлом `executable_name(os.name)` и ресурсами), `--old-dir` (папка старой сборки), `--old-png-dir` (готовые снимки старой сборки: `<папка>/<ШxВ>/<сцена>.png`), `--no-old` (флаг), `--language` (`ru` или `en`, по умолчанию `ru`), `--pairs` (по умолчанию `reference_pairs.tsv` рядом с файлом инструмента), `--gallery-file` (по умолчанию `reference_gallery.tsv` рядом с файлом инструмента), `--gallery` (флаг), `--headless` (флаг), `--only` (имя пары; повторяемый; имя не из списка пар — `parser.error`). Без `--gallery` ровно одно из `--old-dir`, `--old-png-dir`, `--no-old` обязательно, иначе `parser.error` (код 2); с `--gallery` аргументы старой сборки не используются, и `--only` не используется. Нет исполняемого файла в `--new-dir` или `--old-dir` — `parser.error`. Среда — `game_environment(os.environ, args.headless, Path(args.out) / "xdg")`. Возвращает 0, если нужная из функций вернула `True`, иначе 1. Файл заканчивается блоком `if __name__ == "__main__": sys.exit(main())`.

6. **Чего инструмент не делает.** Не меняет и не читает `settings.ini`, `preferences.ini`, папку `saves/` старой сборки; не пишет ничего, кроме `--out` и файлов, которые сама игра пишет в свою рабочую папку (`nlog.txt`). Не сравнивает пиксели и не оценивает вид. Не удаляет ничего, кроме `saves` внутри папки ячейки и прежних файлов сцены этой ячейки.

7. **Нет других изменений.** Ни переформатирования соседних файлов, ни новых комментариев в коде и тестах, кроме разрешённых абзацем «Комментарии в коде» (по умолчанию — ни одного).

## Тесты

Тесты пишутся в шаге 1 плана. Файл `tools/ui-audit/tests/test_reference_shots.py`: `unittest`, импорт модуля как в `tools/ui-audit/tests/test_run_all.py` (`sys.path.insert(0, str(Path(__file__).resolve().parents[1]))`, `import reference_shots  # noqa: E402`), временные папки — `tempfile.TemporaryDirectory`. 25 методов `test_*` в пяти классах. В шаге 2 тесты краснеют до записи `reference_shots.py` и TSV: `ModuleNotFoundError: No module named 'reference_shots'`.

Подставной запуск `FakeRunner` (общий помощник файла тестов): вызываемый объект с аргументами `(command, cwd, env, timeout)`, хранит `calls` (список команд). Команду разбирает так: есть `--ui-audit-list` — возвращает `SimpleNamespace(returncode=0, stdout=json.dumps({"scenes": [{"id": i} for i in catalog]}), stderr="")`; иначе берёт `--ui-audit-scene`, `--ui-audit-out`, `-screenWidth`, `-screenHeight`, пишет в папку `--ui-audit-out` файл `<сцена>.png` — однотонный PNG `ширина × высота` (PIL) — и `<сцена>.geometry.jsonl` с одной строкой `{"k":"header","scene":<сцена>,"resolution":"WxH","language":"ru","graphics":"hd","canvas":{"w":W,"h":H},"game_screen":false,"render_scale":0,"world_scale":0}`, возвращает `SimpleNamespace(returncode=0, stdout="", stderr="")`. Параметры конструктора: `catalog` (список id сцен), `exit_codes` (словарь сцена → код выхода, по умолчанию 0; при коде не 0 файлы всё равно пишутся), `timeouts` (словарь сцена → сколько первых вызовов бросают `subprocess.TimeoutExpired(command, timeout)` до записи файлов), `saves` (булево: при `True` в папке `--ui-audit-out` создаётся `saves/x.d2s`), `render_scale` (значение в заголовке, по умолчанию 0), `language` (значение в заголовке, по умолчанию `"ru"`).

Класс `PairsFile` (реальные файлы `tools/ui-audit/reference_pairs.tsv`, `reference_gallery.tsv`, путь — от `Path(__file__).resolve().parents[1]`):

1. `test_pairs_file_has_27_unique_pairs` — `parse_pairs` даёт 27 пар; `len({p.name for p in pairs}) == 27`; у каждой `port_scene` не пуст.
2. `test_only_two_pairs_lack_a_fork_scene` — множество имён пар с `fork_scene is None` равно `{"skirmish-hud", "mentat-briefing-sardaukar"}`.
3. `test_battle_pairs_use_three_resolutions_and_the_rest_one` — у `skirmish-hud` и `mission-hud` `resolutions == [(800, 600), (1920, 1080), (5120, 1440)]`; у остальных 25 пар `resolutions == [(1920, 1080)]`; сумма длин списков разрешений равна 31.
4. `test_parse_rejects_bad_files` — пять случаев `subTest`, каждый: файл из заголовка `pair\tfork_scene\tport_scene\tresolutions\tnote` и строк, `parse_pairs` бросает `ValueError`: (а) две строки `x\ta\tb\t800x600\t-` (повтор имени); (б) `x\ta\tb\t800*600\t-`; (в) `x\ta\t-\t800x600\t-`; (г) `x\tsave-dialog-load\tb\t800x600\t-`; (д) `x\ta\tb\t800x600` (4 поля).
5. `test_save_writing_fork_scenes_are_pinned` — `SAVE_WRITING_FORK_SCENES == frozenset({...13 имён из п. 2 контракта...})` (литерал в тесте).
6. `test_gallery_file_lists_the_five_readme_files` — `parse_gallery` даёт список из 5 строк; множество `file` равно `{"main-menu.png", "house-selection.png", "ordos-briefing.png", "skirmish-gameplay.png", "victory-screen.png"}`; у каждой `resolution == (1920, 1080)`.

Класс `Command`:

7. `test_fork_command_has_no_language_argument` — `scene_command(Path("d"), "old", "main-menu", 1920, 1080, Path("o"), "ru") == ["d", "-windowed", "-screenWidth", "1920", "-screenHeight", "1080", "--ui-audit-scene", "main-menu", "--ui-audit-out", "o"]` (строки путей через `str(Path(...))`).
8. `test_port_command_ends_with_language_argument` — то же с `side="new"` и `language="en"` даёт тот же список плюс `["--ui-audit-language", "en"]` в конце.
9. `test_executable_name_by_platform` — `executable_name("nt") == "d2tm.exe"`, `executable_name("posix") == "d2tm"`.
10. `test_headless_environment` — `game_environment({"A": "1"}, True, Path("x"))` содержит `A=1`, `SDL_VIDEODRIVER=dummy`, `SDL_RENDER_DRIVER=software`, `SDL_AUDIODRIVER=dummy`, `XDG_DATA_HOME=str(Path("x"))`; `game_environment({"A": "1"}, False, Path("x")) == {"A": "1"}`.

Класс `Checks`:

11. `test_png_size_reads_the_header_and_rejects_other_files` — PNG 7×5 (PIL) даёт `(7, 5)`; файл из 30 байт `b"x"*30` и файл из 5 байт — `ValueError`.
12. `test_read_header_returns_the_first_record` — файл с двумя строками (`{"k":"header","a":1}` и `{"k":"text"}`) даёт `{"k": "header", "a": 1}`; файл, первая строка которого `{"k":"text"}`, — `ValueError`.
13. `test_cell_without_problems` — `cell_problems("new", 0, (1920, 1080), {"render_scale": 0, "world_scale": 0, "language": "en"}, 1920, 1080, "ru") == []` и `cell_problems("old", 0, (1920, 1080), {"render_scale": 0, "world_scale": 0, "language": "ru"}, 1920, 1080, "ru") == []`.
14. `test_cell_problems_are_named` — при остальных значениях из случая 13 (`side="old"`, язык `ru`): `exit_code=1` даёт `["exit=1"]`; `size=(1920, 1000)` — `["png-size=1920x1000"]`; `render_scale=125` — `["render-scale=125"]`; `world_scale=110` — `["world-scale=110"]`; язык заголовка `"en"` — `["language=en"]`; при `side="new"` и языке заголовка `"en"` — `[]`; `header=None` и `size=None` при `exit_code=0` — `[]`.

Класс `Sheet`:

15. `test_sheet_size_per_resolution` — для новых PNG 1920×1080, 800×600 и 5120×1440 (однотонные) листы имеют размеры соответственно `(2576, 748)`, `(1616, 628)`, `(2576, 388)` (`Image.open(...).size`).
16. `test_sheet_colours` — старый PNG 800×600 цвета `(200, 0, 0)`, новый `(0, 0, 200)`: пиксель листа `(10, 38)` равен `(200, 0, 0)`; пиксель `(1616 - 10, 38)` равен `(0, 0, 200)`; пиксель `(808, 100)` равен `BACKGROUND` (полоса зазора).
17. `test_sheet_without_old_picture_has_grey_cell` — `old_png=None`, новый 800×600 цвета `(0, 0, 200)`: пиксель `(400, 328)` равен `PLACEHOLDER`, пиксель `(1200, 328)` равен `(0, 0, 200)`.

Класс `RunReference` (`FakeRunner`, пути `tmp/old/d2tm`, `tmp/new/d2tm` как `Path`, выход — `tmp/out`):

18. `test_run_reference_writes_table_files_and_sheets` — пары `Pair("p1", "a", "b", [(800, 600)], "-")` и `Pair("p2", None, "c", [(800, 600)], "-")`, каталог `["a", "b", "c"]` у обеих сборок; `run_reference(..., old_exe=tmp/old/d2tm, old_png_dir=None, language="ru", ...)` возвращает `True`; команды сцен (без `--ui-audit-list`), по порядку — сцены `a`, `b`, `c`; существуют файлы `out/old/800x600/a.png`, `out/new/800x600/b.png`, `out/new/800x600/c.png`, `out/sheets/p1_800x600.png`, `out/sheets/p2_800x600.png`; первая строка `reference.tsv` равна `"\t".join(TABLE_HEADER)`; вторая — `p1\t800x600\ta\tb\t0\t0\t800x600\t800x600\t800x600\t800x600\told/800x600/a.png\tnew/800x600/b.png\tsheets/p1_800x600.png\tok`; третья — `p2\t800x600\t-\tc\t-\t0\t-\t800x600\t-\t800x600\t-\tnew/800x600/c.png\tsheets/p2_800x600.png\tok`; строк всего 3.
19. `test_a_failed_scene_is_named_in_problems_and_fails_the_run` — те же пары, `exit_codes={"b": 1}`: возвращается `False`; в строке `p1` столбец `problems` равен `new:exit=1`, столбец `new_exit` — `1`.
20. `test_timeout_is_retried_once` — пары `Pair("p1", None, "b", [(800, 600)], "-")` и `Pair("p2", None, "c", [(800, 600)], "-")`, `timeouts={"b": 1, "c": 2}`: сцена `b` запускалась 2 раза и строка `p1` кончается `ok`; сцена `c` запускалась 2 раза, в строке `p2` `new_exit` равен `timeout`, `problems` равен `new:timeout`, `sheet` равен `-`; возвращается `False`.
21. `test_old_png_directory_mode_does_not_run_the_old_build` — готовый `tmp/oldpng/800x600/a.png` (800×600); `run_reference(..., old_exe=None, old_png_dir=tmp/oldpng, ...)` с парой `p1`: команды сцен — только `b`; в строке `p1` `old_exit` равен `-`, `old_png_size` равен `800x600`, `problems` равен `ok`; при удалённом `a.png` строка имеет `problems` равный `old:no-png`.
22. `test_unknown_scene_is_not_run` — каталог новой сборки `["a"]` (сцены `b` нет), старой `["a"]`: пара `p1` (`a`, `b`) даёт `problems` равный `new:no-scene`, команды сцен — только `a`; `sheet` равен `-`; возвращается `False`.
23. `test_saves_folder_is_removed` — `FakeRunner(saves=True)`: после `run_reference` папки `out/new/800x600/saves` нет, `out/new/800x600/b.png` есть.

Класс `Gallery` и `MainOptions`:

24. `test_gallery_copies_the_five_pictures` — `run_gallery` с двумя строками `GalleryRow("one.png", "a", (800, 600))`, `GalleryRow("two.png", "b", (800, 600))`, каталог `["a", "b"]`: возвращает `True`; есть `out/gallery/one.png`, `out/gallery/two.png`; `out/gallery.tsv` — заголовок `"\t".join(GALLERY_HEADER)` и две строки `one.png\ta\t800x600\t0\t800x600\t800x600\tok`, `two.png\tb\t800x600\t0\t800x600\t800x600\tok`; при `exit_codes={"b": 1}` возвращает `False`, файла `out/gallery/two.png` нет, в строке `two.png` `problems` равен `exit=1`.
25. `test_main_option_errors` — `main(["--out", x, "--new-dir", y])` (нет аргумента старой сборки) и `main(["--out", x, "--new-dir", y, "--old-dir", z, "--no-old"])` (`--old-dir` вместе с `--no-old`) завершаются `SystemExit` с кодом 2 (`assertRaises(SystemExit)`, `.exception.code == 2`; папки `y`, `z` — существующие пустые временные).

Команды: красный и зелёный прогон — `cd tools/ui-audit/tests && python3 -B -m unittest test_reference_shots`; ожидаемая строка зелёного прогона — `Ran 25 tests`, последняя строка `OK`. Весь набор `tools/ui-audit/tests` — `cd tools/ui-audit && python3 -B -m unittest discover -s tests`.

`tests/CMakeLists.txt` и `TEST_SOURCES` не меняются: Python-тесты в CTest не входят.

## PLAN-P13

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tools/ui-audit/tests/test_reference_shots.py` | Раздел «Тесты» целиком. | помощник A |
| 2 | — | Красный прогон: `cd tools/ui-audit/tests && python3 -B -m unittest test_reference_shots > ../../../.tmp/p13/red.log 2>&1; echo exit=$?` — `exit` не 0, в логе есть `ModuleNotFoundError: No module named 'reference_shots'`. Запускается до записи шагов 3 и 4. | помощник A |
| 3 | `tools/ui-audit/reference_shots.py` | Пункты 2, 5–7 раздела «Контракт». | помощник B |
| 4 | `tools/ui-audit/reference_pairs.tsv`, `tools/ui-audit/reference_gallery.tsv` | Пункты 3 и 4 раздела «Контракт» и приложение А; файлы записываются побайтно из приложения (табуляции — настоящие). | помощник C |
| 5 | — | Проверки 1–7 раздела «Проверки» по порядку. | помощник A |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p13`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P13-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p13 && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p13/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает.
2. **Тесты Python.**
   - `cd tools/ui-audit/tests && python3 -B -m unittest test_reference_shots > ../../../.tmp/p13/py-new.log 2>&1; echo exit=$?` — `exit=0`, в логе строки `Ran 25 tests` и `OK`.
   - `cd tools/ui-audit && python3 -B -m unittest discover -s tests > ../../.tmp/p13/py-all.log 2>&1; echo exit=$?` — `exit=0`, последняя строка `OK`; число в строке `Ran N tests` записать в сдачу.
   - После — `rm -r tools/ui-audit/tests/__pycache__ tools/ui-audit/__pycache__` для тех из двух папок, что появились.
3. **Пары и каталоги сцен.** Помощник A пишет временный скрипт `.tmp/p13/check_pairs.py` (в репозиторий не входит; читает файлы данных через `reference_shots.parse_pairs` и `parse_gallery`) и запускает его: порт — `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=$PWD/.tmp/p13/xdg .tmp/out/run/bin/d2tm --ui-audit-list` (запуск из `.tmp/out/run/bin`) — множество id; форк — `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | grep -o 'scene("[^"]*"'` — множество id. Скрипт печатает `port_missing=<число>`, `fork_missing=<число>`, `gallery_missing=<число>` и `scenes_port=<число>` — ожидается `0`, `0`, `0` и `192`. Команда запуска скрипта: `python3 -B .tmp/p13/check_pairs.py > .tmp/p13/check-pairs.log 2>&1; echo exit=$?` — `exit=0`.
4. **Прогон инструмента на сервере (только новое).**
   - `mkdir -p .tmp/p13/tmp && TMPDIR=$PWD/.tmp/p13/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tools/ui-audit/reference_shots.py --out .tmp/p13/ref --new-dir .tmp/out/run/bin --no-old --headless --language ru > .tmp/p13/run-ref.log 2>&1; echo exit=$?` — `exit=0`. Команду не прерывай: ни Ctrl+C, ни kill, ни другой сигнал; она сама ограничена `timeout 1800`.
   - Помощник A пишет временный скрипт `.tmp/p13/check_ref.py` и запускает его (`python3 -B .tmp/p13/check_ref.py .tmp/p13/ref/reference.tsv > .tmp/p13/check-ref.log 2>&1; echo exit=$?`): в `reference.tsv` — заголовок и ровно 31 строку данных; у каждой строки `new_exit` равен `0`, `problems` равен `ok`, `new_png_size` равен разрешению из столбца `resolution`, `new_canvas` равен ожидаемому холсту (`800x600` → `800x600`, `1920x1080` → `1067x600`, `5120x1440` → `2133x600`); все 31 файл столбца `sheet` существуют; число строк с `old_scene` равным `-` равно 31; в `.tmp/p13/ref/new/` на каждую ячейку есть `.png` и `.geometry.jsonl`. Скрипт печатает `rows=31 ok=31 sheets=31 canvas_ok=31`; `exit=0`.
5. **Галерея.** `TMPDIR=$PWD/.tmp/p13/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tools/ui-audit/reference_shots.py --gallery --out .tmp/p13/gal --new-dir .tmp/out/run/bin --headless --language en > .tmp/p13/run-gal.log 2>&1; echo exit=$?` — `exit=0`; в `.tmp/p13/gal/gallery/` ровно пять файлов с именами из `reference_gallery.tsv`, у каждого размер PNG (по `reference_shots.png_size`, считает временный скрипт `.tmp/p13/check_gal.py`) равен 1920×1080; в `.tmp/p13/gal/gallery.tsv` заголовок и пять строк, у каждой `problems` равен `ok`; скрипт печатает `gallery_files=5 size_ok=5`.
6. **Справка и команда для Windows.** `python3 -B tools/ui-audit/reference_shots.py --help > .tmp/p13/help.log 2>&1; echo exit=$?` — `exit=0`, в логе есть строки `--old-dir`, `--old-png-dir`, `--no-old`, `--gallery`, `--headless`, `--language`, `--only`. Команда для Windows (ведущий выполняет её после сдачи; ты не выполняешь):
   ```
   python tools/ui-audit/reference_shots.py --out <OUT> --old-dir <OLD> --new-dir <NEW> --language ru --headless
   ```
   `<OLD>` — свежая распаковка выпуска `v0.8.0-ru-hd.10` (файл `d2tm.exe` и ресурсы; в `settings.ini` строки `Language=ru` и `RenderScale=0`, ключа `WorldScale` нет или он 0); `<NEW>` — папка запуска сборки порта с `d2tm.exe`; `<OUT>` — новая пустая папка. Перед запуском в `%APPDATA%\D2TM\Dune II - The Maker\preferences.ini` не должно быть ключей `RenderScale` и `WorldScale` (или они `0`). Эта команда и условия переписываются в сдачу дословно.
7. `git -c lfs.storage=$PWD/.tmp/p13/lfs status --short` — изменённых (` M`) путей нет; новые (`??`) — только `tools/ui-audit/reference_shots.py`, `tools/ui-audit/reference_pairs.tsv`, `tools/ui-audit/reference_gallery.tsv`, `tools/ui-audit/tests/test_reference_shots.py`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P13-NN` с выводом и стоп. Ожидания существующих тестов и скрипты в `tests/ui_audit/` не меняй. Проверку «ноль совпадений» (если нужна) прогони и на `B13`.

## Сдача

Последнее сообщение — блок `## DONE-P13 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p13/progress.md`): строка на каждый шаг плана;
- красный прогон шага 2: первые 30 строк `.tmp/p13/red.log`;
- вывод каждой проверки 1–7 с кодами выхода (не больше 40 строк на проверку); для проверок 4 и 5 — строки `rows=… ok=…`, `gallery_files=…` и первые 5 строк `reference.tsv` и `gallery.tsv`;
- команда и условия для Windows (проверка 6) дословно;
- `git diff --stat` и список для коммитов:
  1. тесты: `tools/ui-audit/tests/test_reference_shots.py`;
  2. код и данные: `tools/ui-audit/reference_shots.py`, `tools/ui-audit/reference_pairs.tsv`, `tools/ui-audit/reference_gallery.tsv`.

  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …` (для обоих — `Behavior changes: none, adds a developer tool`);
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p13 --size`; у `.tmp/p13` пометка `оставить — логи проверок и `ref`, `gal` нужны ведущему для просмотра`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаг 1 (помощник A), шаг 3 (помощник B) и шаг 4 (помощник C) — одновременно; помощники B и C не записывают файлы, пока помощник A не записал в журнал хода строку о конце шага 2.
  4. Шаг 2 (помощник A) — сразу после шага 1.
  5. Шаг 5 (помощник A) — после шагов 2, 3 и 4.
  6. Сдача и стоп.
- **Параллельно:** шаги 1, 3, 4 пишут разные файлы; общий у них только порядок записи (пункт 3 порядка). Собирает их вместе проверка 2.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных. Ожидаемое время: помощник A — 30 минут на шаги 1–2 и 60 минут на шаг 5 (сборка 20 минут, прогон инструмента до 30 минут); помощник B — 40 минут; помощник C — 10 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено» и «Контракт»; его шаги плана; помощнику A — ещё разделы «Тесты» и «Проверки»; помощникам B и C — ещё приложение А; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p13/`.
  - Корневая нить раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Правила команд.**
  - Каждая команда, запускающая собранные файлы (`d2tm`, `reference_shots.py`, `ctest`), получает `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib`.
  - Сверки «строка есть в файлах» — `git grep --untracked` или `grep -r`: исполнитель не коммитит, новые файлы не в индексе.
  - Команды `rm -f` и `rm -rf` песочница отклоняет: обнулить файл — `: > файл`, удалить папку — `rm -r`.
- **Остановки:** только на `## DONE-P13` и на блоках `## Q-P13-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P13-NN` и стоп. Прогон проверки 4 или 5, у которого размер PNG не равен запрошенному (например, `5120x1440` не получился в режиме `dummy`/`software`), — блок `## Q-P13-NN` с выводом и стоп: размер не подгоняется и проверка не ослабляется.
- **Рамка правок:** файлы шагов 1, 3 и 4 плана и папка `.tmp/p13/`. Понадобился другой файл — блок `## Q-P13-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` (`nlog.txt`) и в папки прогонов инструмента; это не правка.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

## Приложение А — тексты файлов данных

Разделитель полей — один символ табуляции; первая строка каждого файла — заголовок.

`tools/ui-audit/reference_pairs.tsv`:

```
pair	fork_scene	port_scene	resolutions	note
main-menu	main-menu	main-menu	1920x1080	-
options-main	options-menu-main	options-menu-main	1920x1080	-
options-applied	options-menu-applied	options-menu-applied	1920x1080	-
options-page-game	options-menu-game	options-game-game	1920x1080	entry differs: menu / game
options-page-controls	options-menu-controls	options-game-controls	1920x1080	entry differs: menu / game
options-page-diagnostics	options-menu-diagnostics	options-game-diagnostics	1920x1080	entry differs: menu / game
options-page-keybind	options-menu-keybind	options-game-keybind	1920x1080	entry differs: menu / game
skirmish-hud	-	save-roundtrip	800x600,1920x1080,5120x1440	-
mission-hud	game-hud	game-hud	800x600,1920x1080,5120x1440	-
campaign-map-intro	region-atreides-intro-1	region-atreides-intro-1	1920x1080	-
campaign-map-select	region-ordos-select-3	region-ordos-select-3	1920x1080	-
mentat-briefing-atreides	mentat-briefing-atreides-await	mentat-briefing-atreides-await	1920x1080	-
mentat-briefing-ordos	mentat-briefing-ordos-await	mentat-briefing-ordos-await	1920x1080	-
mentat-briefing-harkonnen	mentat-briefing-harkonnen-await	mentat-briefing-harkonnen-await	1920x1080	-
mentat-win-ordos	mentat-win-ordos-await	mentat-win-ordos-await	1920x1080	-
tellhouse-ordos	tellhouse-ordos-await	tellhouse-ordos-await	1920x1080	-
mentat-briefing-sardaukar	-	mentat-briefing-sardaukar-await	1920x1080	-
credits-title	credits-title	credits-title	1920x1080	-
credits-1	credits-1	credits-1	1920x1080	-
credits-2	credits-2	credits-2	1920x1080	-
credits-3	credits-3	credits-3	1920x1080	-
credits-4	credits-4	credits-4	1920x1080	-
credits-5	credits-5	credits-5	1920x1080	-
choose-house	choose-house	choose-house	1920x1080	-
select-mission-ordos	select-mission-ordos	select-mission-ordos	1920x1080	-
outcome-win	outcome-win	outcome-win	1920x1080	-
outcome-lose	outcome-lose	outcome-lose	1920x1080	-
```

`tools/ui-audit/reference_gallery.tsv`:

```
file	port_scene	resolution
main-menu.png	main-menu	1920x1080
house-selection.png	choose-house	1920x1080
ordos-briefing.png	mentat-briefing-ordos-await	1920x1080
skirmish-gameplay.png	save-roundtrip	1920x1080
victory-screen.png	outcome-win	1920x1080
```

<!-- team-process:executor-rules sha256=a9bda9c6318255670aecab75810e663ed3ef91095a214b541ff20d2adede49dd -->
## Обязательно: правила исполнителя

«Ведущий» в этих правилах — тот, кто ведёт твою задачу: он дал задание и принимает сдачу.

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Фоновые команды. Среда сама будит тебя, когда фоновая команда кончилась (сессия Claude: запуск с `run_in_background`), — долгий прогон запускай в фоне и делай тем временем то, что от него не зависит. Среда не будит (нить Codex) — фоновых команд нет: после остановки исполнителя никто его не разбудит; длинные прогоны — в переднем плане, с таймаутом до 30 минут. Ожидание циклом (`while …; sleep`) запрещено в обоих случаях.
- Git по договорённости с ведущим. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ведущий после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ведущего.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не останавливать и не менять (пользоваться ими как клиент можно), секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. В репозиторий и в корень рабочей копии ничего временного не клади. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. Удалять что-либо вне своей `tmp` — только по разделу «Уборка».
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- Субагенту, которого запускаешь, назначь ожидаемое время работы и запиши его в журнал хода. Время вышло, а итога нет — проверь, как он идёт: скриптом по его журналу или списком агентов среды, а не ожиданием. Стоит или ушёл в сторону — останови и перезапусти с более узкой задачей.
- **Чтение.** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по транскрипту: обрезанный вывод — не чтение.
- **Цель нити (исполнитель Codex).** Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; субагентам цель не ставить.
- **Строка хода (исполнитель Codex).** После чтения до работы и после каждого закрытого пункта задания или плана ведущего — отдельной строкой ответа: `ХОД: [x] <пункт>; [>] <пункт>; [ ] <пункт>`. В строке все пункты по порядку: `[x]` — сделан, `[>]` — в работе, `[ ]` — впереди. По этой строке панель ведущего и владельца показывает план и ход. Исполнитель в сессии Claude строку хода не пишет.
- **Сжатие контекста (исполнитель в сессии Claude).** На границе своих частей — часть закрыта, журнал хода обновлён — сам вызови `request_compact` и закончи ход. В `instructions`: задание, текущая часть и следующий шаг, id фоновых задач и сессий, пути, решения, открытые вопросы и строка «после сжатия перечитай раздел правил в задании». Посреди части не сжимай. После сжатия перечитай задание и журнал хода.

## Вопросы и остановки

Каждое препятствие сверяй в таком порядке:

1. Подходит под список «`Q` и стоп» — `Q` и стоп, даже если оно подходит и под список «Без вопроса».
2. Иначе подходит под список «Без вопроса» — решай сам и работай дальше.
3. Иначе: без ответа идущий подпункт выполнить нельзя — `Q` и стоп; можно — неблокирующий вопрос: запиши его в сдачу и работай дальше по списку, не простаивай.

`Q` в любом другом пункте этих правил — тоже «`Q` и стоп».

**`Q` и стоп.**
- ответ требует правки вне рамки правок, правки промптов, норм, governance, контрактов или замороженных тестов (файл, assert, смысл проверки);
- удаление данных, сеть или установка пакетов;
- смена цели, рамки или критерия готовности; новый механизм; решение по продукту;
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в сдаче;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса.** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи, журнала хода и того, что прямо называет задание, не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- **Общее, а не частное.** Код и поведение — универсальные и масштабируемые: одна логика и одни правила для всего продукта, в любом месте и с любыми сущностями и предметами, а не под конкретное место, персонажа или вещь; частное задают данные. Проблему чинить системно, в общем механизме, а не отдельным исключением для найденного случая.
- **Комментарии в коде.** Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий; исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи из списка — строго по порядку; независимые части одной задачи идут параллельно, как велит её раздел «Организация работы».
- Замечания ведущего выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения.
- Если исполнитель коммитит — незаконченное хранить в своей ветке WIP-коммитом, а не патчами во временной папке. Голый `git stash` не использовать: список stash общий для всех рабочих копий и сессий.
- Перенос и переформатирование кода — отдельным коммитом, изменение поведения — следующим. «Без изменения поведения» писать, только если это правда.
- Последняя строка сообщения коммита — `Behavior changes: …` со списком или `Behavior changes: none`. Называть и мелочи: запасной вариант, удалённое поле, удалённую настройку в тесте, изменённый предел.
- Заголовок не преувеличивает: «finish», «complete» — только если пункт закрыт целиком; остатки назвать в теле.

## Тесты

- Тест проходит путь пользователя через тот вход продукта, которым пользуется пользователь в сценарии: для интерфейса — события мыши и клавиатуры, для API — вызов API. Тестируемый код не подменять заглушками.
- Тест проверяет поведение, а не совпадение хэша или вывода с прошлой сборкой. Изображения сравнивать с эталоном с допуском из задания, а если в задании его нет — из действующего эталонного теста или конфигурации сравнения; ни один источник допуск не задаёт — `Q`.
- Асинхронный результат ждать по нему самому (нужное значение, запись, пиксель), а не по косвенному флагу.
- Нестабильный тест разбирать сразу, с логом и санитайзером, если он уже настроен в проекте. «Не воспроизвелось» проблему не закрывает: исполнитель перечисляет её в сдаче с логом, issue заводит ведущий.
- Тесты пишут только в свои временные папки; общее состояние (синглтоны, кэши) сбрасывать перед каждым тестом.
- Общие помощники тестов и константы — в одном месте, не копировать по файлам.
- В целевую ветку сливают только ветку с зелёным CI на её последнем коммите; кто сливает (обычно ведущий), тот после слияния проверяет CI целевой ветки и красной её не оставляет.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Сдача

Сдача — блок `## DONE-<id> | время | HEAD <sha>`, один на задачу; после возврата `REVIEW` — новая сдача. В ней:

- журнал хода без изменений (строка на подпункт: что сделано, коммит, тест) и строки вывода проверок — красный до правки, зелёный после; отдельной таблицы нет;
- числа только из логов, а не из памяти;
- свои вызовы и вызовы субагентов — числами скрипта по транскрипту: Claude — `tools/usage-daily.py <папка> --session <id>`, Codex — `tools/codex-watch.py`;
- раздел «не проверено» — обязателен; пустым без пояснения не бывает;
- раздел «Рабочие места» — по разделу «Уборка»;
- находки вне задачи — списком; issue заводит ведущий;
- `git status --short`;
- три пункта для владельца простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Отдельного отчёта владельцу не создавать.

## Уборка

- В сдаче — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер (`du -sh`), назначение и пометка: `удалить` или `оставить — <почему>`. Назначение — доказательство (на него ссылаются сдача, PR или журнал) или промежуточное; доказательства — только `оставить`.
- Удаляешь только после ответа ведущего `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Объекты сборки, ненужные для повторной проверки, — тоже только после `CLEAN-OK`.
- Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`.
- Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.

<!-- /team-process:executor-rules -->
