## RECON-P13R | Thu Nov 12 17:14:45 UTC 2026

Перед командами Git устанавливался `PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`. Во всех таблицах четвёртая колонка содержит полученную строку кода или значение; для строк кода её вывод получен `git show <полная ревизия>:<путь> | nl -ba | sed -n '<номер>p'`. Сборок, CTest, запуска игры, скриптов режима отладки и сети не было.

### 1. Каталоги сцен

Команды разбора аргумента:

```text
git grep -n -e '--ui-audit-scene' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:29:        else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {

git grep -n -e '--ui-audit-scene' 010a6eb134661660a077279bb94a36f063b97d7a -- src
010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditArguments.cpp:29:        else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {
```

В обеих ревизиях строку разбирает `src/debug/UiAuditArguments.cpp@9208dcf:29` / `src/debug/UiAuditArguments.cpp@010a6eb:29`. Идентификатор по каталогу ищет `findScene`: `src/debug/UiAuditScenes.cpp@9208dcf:578`, `src/debug/UiAuditScenes.cpp@010a6eb:583`. Каталоги сцен находятся в `src/debug/UiAuditScenes.cpp`; регистрации, функции подготовки и состояния из тел этих функций перечислены по каждой сцене в `scenes.tsv`.

Подсчёт строк регистрации:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | rg -c 'scene\("'
157

git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | rg -c 'scene\("'
185
```

`scenes.tsv` содержит 157 строк FORK1 и 185 строк PORT. Идентификатор, строка регистрации, подготовка, открываемое состояние и строка состояния указаны в её столбцах.

### 2. Экраны шага П13

`screens.tsv` перечисляет идентификаторы каждой сцены для каждого экрана и ревизии, а также строки регистрации и подготовки. Числа сцен FORK1 / PORT: главное меню — 3 / 3; настройки — 18 / 10; схватка с боковой панелью — 0 / 1; миссия кампании с боковой панелью — 53 / 59; карта кампании — 45 / 60; ментат — 24 / 32; титры — 6 / 6.

Для схватки `git grep -n -e 'startSkirmish' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug` дал пустой вывод и код завершения 1. В PORT сцену `save-roundtrip` регистрирует `src/debug/UiAuditScenes.cpp@010a6eb:511`; подготовка выбирает схватку в `src/debug/UiAuditScenes.cpp@010a6eb:353` и `src/debug/UiAuditAccess.cpp@010a6eb:968,975,984`. Доказательства для миссий кампании и остальных экранов указаны в `screens.tsv`.

### 3. Размер окна и холста

Команда поиска аргументов размера в FORK1:

```text
git grep -n -e '-screenWidth' -e '-screenHeight' -e '-windowed' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:9:    {"-windowed",               Options::WINDOWED},
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:19:    {"-screenWidth",            Options::SCREENX},
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:20:    {"-screenHeight",           Options::SCREENY},
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:113:    std::cout << "Usage: d2tm[.exe] [-windowed] [-screenWidth <width>] ...\n\n";
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:116:    std::cout << "-windowed              - Run game in window instead of fullscreen\n";
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:117:    std::cout << "-screenWidth <value>   - Width of screen / window (minimum 800)\n";
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:118:    std::cout << "-screenHeight <value>  - Height of screen / window (minimum 600)\n";
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp:147:    std::cout << "d2tm.exe -windowed -screenWidth 1024 -screenHeight 768\n";
```

Та же команда в PORT:

```text
git grep -n -e '-screenWidth' -e '-screenHeight' -e '-windowed' 010a6eb134661660a077279bb94a36f063b97d7a -- src
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:23:    {"-windowed",               Options::WINDOWED},
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:34:    {"-screenWidth",            Options::SCREENX},
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:35:    {"-screenHeight",           Options::SCREENY},
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:141:    std::cout << "Usage: d2tm[.exe] [-windowed] [-screenWidth <width>] ...\n\n";
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:144:    std::cout << "-windowed              - Run game in window instead of fullscreen\n";
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:146:    std::cout << "-screenWidth <value>   - Width of screen / window (minimum 800)\n";
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:147:    std::cout << "-screenHeight <value>  - Height of screen / window (minimum 600)\n";
010a6eb134661660a077279bb94a36f063b97d7a:src/utils/cHandleArgument.cpp:178:    std::cout << "d2tm.exe -windowed -screenWidth 1024 -screenHeight 768\n";
```

FORK1 записывает `-windowed` в `settings->windowed` (`src/utils/cHandleArgument.cpp@9208dcf:53`), а ширину и высоту — в `settings->screenW/H` (`src/utils/cHandleArgument.cpp@9208dcf:86,94`); значения по умолчанию — 800×600 (`src/utils/GameSettings.hpp@9208dcf:7-8`). PORT записывает `-windowed` в `settings->windowed` (`src/utils/cHandleArgument.cpp@010a6eb:72`), а размеры — в `InitialGameSettings::screenW/H` (`src/utils/cHandleArgument.cpp@010a6eb:108,116`, поля `src/utils/InitialGameSettings.hpp@010a6eb:20-21`); в таблице также есть дополнительный параметр `-fullscreen` (`src/utils/cHandleArgument.cpp@010a6eb:24`). В FORK1 `--ui-audit-scales` задаёт список масштабов режима аудита (`src/debug/UiAuditArguments.cpp@9208dcf:26-27`); эта опция не задаёт размер окна снимка (`src/debug/UiAuditCapture.cpp@9208dcf:371`).

Поиск SDL-вызовов рабочего размера:

```text
git grep -n -e 'SDL_CreateWindow' -e 'SDL_SetWindowSize' -e 'SDL_SetVideoMode' -e 'SDL_GetDesktopDisplayMode' -e 'SDL_GetCurrentDisplayMode' -e 'SDL_GetWindowSize' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp:140:    if (SDL_GetCurrentDisplayMode(0, &desktopMode) == 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cDataPack.cpp:177:    SDL_Window * window = SDL_CreateWindow("SDL2", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 640, 480, 0);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp:37:    SDL_SetWindowSize(window, windowedSize.width, windowedSize.height);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp:52:    if (SDL_GetCurrentDisplayMode(0, &mode) == 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp:161:    window = SDL_CreateWindow(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp:196:    SDL_SetWindowSize(window, windowedSize.width, windowedSize.height);

git grep -n -e 'SDL_CreateWindow' -e 'SDL_SetWindowSize' -e 'SDL_SetVideoMode' -e 'SDL_GetDesktopDisplayMode' -e 'SDL_GetCurrentDisplayMode' -e 'SDL_GetWindowSize' 010a6eb134661660a077279bb94a36f063b97d7a -- src
010a6eb134661660a077279bb94a36f063b97d7a:src/game/cSDLSystem.cpp:107:    SDL_SetWindowSize(window, renderResolution.width, renderResolution.height);
010a6eb134661660a077279bb94a36f063b97d7a:src/game/cSDLSystem.cpp:115:    // SDL_GetCurrentDisplayMode returns PHYSICAL pixels, but SDL_CreateWindow
010a6eb134661660a077279bb94a36f063b97d7a:src/game/cSDLSystem.cpp:306:    window = SDL_CreateWindow(title.c_str(), renderResolution.width, renderResolution.height, 0);
010a6eb134661660a077279bb94a36f063b97d7a:src/game/cSDLSystem.cpp:338:    SDL_SetWindowSize(window, renderResolution.width, renderResolution.height);
```

В этом поиске нет совпадений `SDL_GetDesktopDisplayMode`; в PORT также нет вызовов `SDL_GetCurrentDisplayMode`, вместо них используются `SDL_GetDisplayBounds` и `SDL_GetDisplayUsableBounds`.

В FORK1 `cScreenInit` получает размер окна из `windowedSize` (`src/utils/cScreenInit.cpp@9208dcf:161,165-166`). Минимум холста задан как 800×600 (`src/utils/RenderScale.hpp@9208dcf:12-13`); начальный размер рабочего стола берётся через `SDL_GetCurrentDisplayMode` (`src/utils/cScreenInit.cpp@9208dcf:51-55`), затем обычный оконный путь использует доступную область, `std::min` и `std::max` (`src/utils/cScreenInit.cpp@9208dcf:127-145`). Ветка ui-audit возвращает размер вывода до этого desktop-fit ограничения (`src/utils/cScreenInit.cpp@9208dcf:125-127`). Холст вычисляется `calculateRenderCanvasSize` из размера вывода и `RenderScale` (`src/utils/cScreenInit.cpp@9208dcf:90-95`; `src/utils/RenderScale.cpp@9208dcf:9,14,23,64-70`) и задаётся как logical size (`src/utils/cScreenInit.cpp@9208dcf:198`).

В PORT размеры проходят через `cGameSettings` в `cSDLSystem` (`src/game/cGame_logic.cpp@010a6eb:322,328,786`). Система получает границы дисплея и usable bounds (`src/game/cSDLSystem.cpp@010a6eb:122-135`), ограничивает оконный размер аспектом и `std::min` (`src/game/cSDLSystem.cpp@010a6eb:214-229`); ui-audit устанавливает запрошенные размеры после минимального ограничения и выходит до desktop-fit (`src/game/cSDLSystem.cpp@010a6eb:199-238`). Окно создаётся с `renderResolution.width/height` (`src/game/cSDLSystem.cpp@010a6eb:306`), фактический размер renderer output синхронизируется при старте (`src/game/cSDLSystem.cpp@010a6eb:173-197`). `applyRenderScale` берёт SDL renderer output и считает холст (`src/game/cSDLSystem.cpp@010a6eb:65-82`), вызывается в `src/game/cGame_logic.cpp@010a6eb:790`; размеры холста записываются обратно в `m_screenW/H` (`src/game/cGame_logic.cpp@010a6eb:805-806`). Все точные строки ограничений, сравнений и преобразований, включая `std::min`, `std::max`, desktop mode и SDL bounds, приведены в `screen-size.tsv`.

### 4. Вывод прогона сцены

В обеих ревизиях аргумент разбирается в `src/debug/UiAuditArguments.cpp:32`, значение сохраняется в `s_options.outDir` на строке 33. Вывод команды для FORK1:

```text
git grep -n -e '--ui-audit-out' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:32:        else if (std::strcmp(argv[i], "--ui-audit-out") == 0 && i + 1 < argc) {
```

Вывод команды для PORT:

```text
git grep -n -e '--ui-audit-out' 010a6eb134661660a077279bb94a36f063b97d7a -- src
010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditArguments.cpp:32:        else if (std::strcmp(argv[i], "--ui-audit-out") == 0 && i + 1 < argc) {
```

Снимок кадра — `<scene-id>.png`, геометрия — `<scene-id>.geometry.jsonl`; пути строятся в `src/debug/UiAuditCapture.cpp@9208dcf:247,255` и `src/debug/UiAuditCapture.cpp@010a6eb:268,276`. PNG записывает `writePng` (`src/debug/UiAuditCapture.cpp@9208dcf:213,227`; `src/debug/UiAuditCapture.cpp@010a6eb:232,249`) через `IMG_SavePNG`. Первая запись geometry-файла — JSONL header с разрешением, языком, graphics, размером canvas, флагом game_screen и масштабами: `src/debug/UiAuditCapture.cpp@9208dcf:161-165` и `src/debug/UiAuditCapture.cpp@010a6eb:175-180`. Последующие записи геометрии — JSONL, например запись текста с ключами `k,s,x,y,w,h,box`: `src/debug/UiAuditCapture.cpp@9208dcf:177`, `src/debug/UiAuditCapture.cpp@010a6eb:196`. В PORT `--ui-audit-frames` добавляет в header `frames` и `frame_ms` (`src/debug/UiAuditCapture.cpp@010a6eb:188-190`).

Сопутствующие файлы сохранений также перечислены в `output.tsv`: FORK1 подготавливает слоты в `saves/` относительно текущей папки, отдельно от `--ui-audit-out` (`src/debug/UiAuditAccess.cpp@9208dcf:141-146`), с именами `quicksave.d2s` и `saveNN.d2s` (`src/save/SaveGameManager.cpp@9208dcf:1355-1358`). PORT направляет фикстуры в `outDir/saves` (`src/debug/UiAuditCapture.cpp@010a6eb:474-475`), с теми же именами слотов (`src/save/SaveGameManager.cpp@010a6eb:792,794`), а сцена roundtrip пишет `roundtrip-first.d2s` (`src/debug/UiAuditAccess.cpp@010a6eb:994-995`).

### 5. Сборка форка

`git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 -- .github/workflows` вывела `build_manual.yml`, `build_master.yml`, `build_pr.yml`, `release-notes.yml`, `release.yml`. Команда `git grep -n -E 'runs-on:.*(ubuntu|windows)' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- .github/workflows` показала задания Linux/Windows в первых трёх build-workflow и сборочные задания Windows/Linux в `release.yml`. В `release.yml` задания `prepare-release`, `common-assets`, `publish-release` не собирают приложение; `release-notes.yml` собирает заметки и Wiki. Строки установки зависимостей, вызовов CMake и сборки в каждом задании приведены в `fork-build.tsv` с путями, номерами строк и фактическим выводом.

Корневой `CMakeLists.txt` FORK1: поиск выполнялся командой `git grep -n -e cmake_minimum_required -e project -e find_package -e add_subdirectory -e option 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt`. Она вывела `cmake_minimum_required(VERSION 3.21)` — `CMakeLists.txt@9208dcf:1`; `project(d2tm)` — `:5`; `find_package` для PkgConfig и SDL2/SDL2_ttf/SDL2_image/SDL2_mixer — `:39,87-90`; `add_subdirectory(src)` — `:95`; `option(D2TM_UI_AUDIT_RUNTIME_TESTS ...)` — `:456`. Дословные строки находятся в `fork-build.tsv`.

`tools/upstream/build_upstream_linux.sh` принимает `<SHA базы апстрима> [--pristine]`; SHA должен состоять из 40 шестнадцатеричных знаков (`tools/upstream/build_upstream_linux.sh@010a6eb:21-22,276-284`). Значение записывается в `upstream_base` (`:280`); далее скрипт выводит его вместе с HEAD через `git rev-parse`, проверяет предка командой `git merge-base --is-ancestor`, а при `--pristine` проверяет `git diff --quiet` (`tools/upstream/build_upstream_linux.sh@010a6eb:182-187`).

Пакеты сверялись командами `git grep -n -e '\.dat"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src`, `git ls-tree -r -l 9208dcf5a358f40afd95c99480e4e09f781ed566 -- <пути пакетов>` и `git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>`. По выводу `git grep` активными стартовыми пакетами являются `sdl_audio.dat`, `sdl_data_hd4.dat`, `sdl_inter_hd4.dat`, `sdl_world_hd4.dat`, `sdl_mentat_hd4.dat`; шаблон динамической загрузки — `data/scenes/hd4/sdl_{}.dat`. Размеры Git-блобов и метки приведены для каждого пути в `fork-build.tsv`: `sdl_audio.dat` — 1 315 544 байта, обычный blob с бинарным началом `D2TMl\0MIDI_ATTACK01\0`; четыре стартовых HD4-пака — по 132–133 байта. Их содержимое и все 18 файлов HD4-сцен начинаются со строки `version https://git-lfs.github.com/spec/v1`, то есть являются LFS-указателями; сценовые файлы имеют размер 132–134 байта. Пять совпадений `gfx*.dat` в `src/utils/cFileValidator.cpp@9208dcf:14-18` — закомментированные старые имена, не открываемые пакеты. Таблица связывает каждое имя, исходный код открытия/шаблон, путь в дереве, размер и вывод проверки blob.

### Чтение

Полностью прочитан файл из списка «Прочитать до работы»: `/srv/dune/tasks/load-check/PORT_PLAN.md`. В нём приведены ссылки на `docs/PLAN_units_sega_upstream.md` (§3.2 и §5.3), `docs/upstream/PORT_MAP.md` и `codex-direct/launch-card-27.md`; эти документы описывают источник шагов, карту функций и организацию запуска. Для статической разведки здесь требуемые ревизии, команды, экраны и ограничения уже заданы в задании и разделе П13 плана, поэтому дополнительное правило или контракт из этих ссылок для выполненных действий не требовался.

### Выводы строк по пунктам 1–2

Для всех 431 уникальных ссылок на строки из столбцов регистрации и состояния `scenes.tsv` и доказательств `screens.tsv` ниже приведены отдельная команда и её фактический вывод. Повторные ссылки сведены в одну запись, а в связи перечислены все относящиеся к строке сцены или экраны. Числа после запятой в ссылках обработаны как отдельные номера строк и отдельные команды. Перед командами Git установлен PATH `/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

#### `src/debug/UiAuditAccess.cpp@9208dcf:97`

Связь: `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '97p'
bool UiAuditAccess::prepareMentatScene(cGame &game, int house, int kind)
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:102`

Связь: `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '102p'
        game.setNextStateToTransitionTo(GAME_BRIEFING);
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:106`

Связь: `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '106p'
        game.setState(kind == 1 ? GAME_WINBRIEF : GAME_LOSEBRIEF);
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:112`

Связь: `screens.tsv`, экран: схватка с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '112p'
bool UiAuditAccess::prepareSkirmish(cGame &game, int variant)
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:274`

Связь: `screens.tsv`, экран: карта кампании.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '274p'
void UiAuditAccess::regionOpen(cGame &game, int mission, bool jump)
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:282`

Связь: `screens.tsv`, экран: карта кампании.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '282p'
    game.setState(GAME_REGION);
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:536`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '536p'
bool UiAuditAccess::enterPlaying(cGame &game, int house, int region)
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:542`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '542p'
    game.setNextStateToTransitionTo(GAME_PLAYING);
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:780`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '780p'
bool UiAuditAccess::prepareGameScreen(cGame &game, int house, int kind)
```

#### `src/debug/UiAuditAccess.cpp@9208dcf:783`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '783p'
    if (!enterPlaying(game, house, 22)) {
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:50`

Связь: `scenes.tsv`, состояние `GAME_MENU` для: FORK1/main-menu, FORK1/main-menu-saves; `screens.tsv`, экран: главное меню.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '50p'
    {"main-menu", "GAME_MENU", "cMainMenuState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:51`

Связь: `scenes.tsv`, состояние `GAME_REGION` для: FORK1/region-atreides-conquer-3, FORK1/region-atreides-conquer-5, FORK1/region-atreides-conquer-7, FORK1/region-atreides-conquer-9, FORK1/region-atreides-intro-1, FORK1/region-atreides-intro-2, FORK1/region-atreides-intro-3, FORK1/region-atreides-select-2, FORK1/region-atreides-select-3, FORK1/region-atreides-select-4, FORK1/region-atreides-select-5, FORK1/region-atreides-select-6, FORK1/region-atreides-select-7, FORK1/region-atreides-select-8, FORK1/region-atreides-select-9, FORK1/region-harkonnen-conquer-3, FORK1/region-harkonnen-conquer-5, FORK1/region-harkonnen-conquer-7, FORK1/region-harkonnen-conquer-9, FORK1/region-harkonnen-intro-1, FORK1/region-harkonnen-intro-2, FORK1/region-harkonnen-intro-3, FORK1/region-harkonnen-select-2, FORK1/region-harkonnen-select-3, FORK1/region-harkonnen-select-4, FORK1/region-harkonnen-select-5, FORK1/region-harkonnen-select-6, FORK1/region-harkonnen-select-7, FORK1/region-harkonnen-select-8, FORK1/region-harkonnen-select-9, FORK1/region-ordos-conquer-3, FORK1/region-ordos-conquer-5, FORK1/region-ordos-conquer-7, FORK1/region-ordos-conquer-9, FORK1/region-ordos-intro-1, FORK1/region-ordos-intro-2, FORK1/region-ordos-intro-3, FORK1/region-ordos-select-2, FORK1/region-ordos-select-3, FORK1/region-ordos-select-4, FORK1/region-ordos-select-5, FORK1/region-ordos-select-6, FORK1/region-ordos-select-7, FORK1/region-ordos-select-8, FORK1/region-ordos-select-9; `screens.tsv`, экран: карта кампании.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '51p'
    {"region", "GAME_REGION", "cSelectYourNextConquestState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:52`

Связь: `scenes.tsv`, состояние `GAME_SELECT_HOUSE` для: FORK1/choose-house.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '52p'
    {"choose-house", "GAME_SELECT_HOUSE", "cChooseHouseState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:53`

Связь: `scenes.tsv`, состояние `GAME_MISSIONSELECT` для: FORK1/select-mission-atreides, FORK1/select-mission-harkonnen, FORK1/select-mission-ordos.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '53p'
    {"select-mission", "GAME_MISSIONSELECT", "cSelectMissionState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:54`

Связь: `scenes.tsv`, состояние `GAME_TELLHOUSE` для: FORK1/tellhouse-atreides-await, FORK1/tellhouse-atreides-speak, FORK1/tellhouse-harkonnen-await, FORK1/tellhouse-harkonnen-speak, FORK1/tellhouse-ordos-await, FORK1/tellhouse-ordos-speak; `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '54p'
    {"tellhouse", "GAME_TELLHOUSE", "BeneMentat"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:55`

Связь: `scenes.tsv`, состояние `GAME_OPTIONS` для: FORK1/options-menu-applied, FORK1/options-menu-controls, FORK1/options-menu-diagnostics, FORK1/options-menu-game, FORK1/options-menu-keybind, FORK1/options-menu-main; `screens.tsv`, экран: меню настроек.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '55p'
    {"options-menu", "GAME_OPTIONS", "cOptionsState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:56`

Связь: `scenes.tsv`, состояние `GAME_OPTIONS` для: FORK1/options-game-applied, FORK1/options-game-controls, FORK1/options-game-diagnostics, FORK1/options-game-game, FORK1/options-game-keybind, FORK1/options-game-main-nosaves, FORK1/options-game-main-saves.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '56p'
    {"options-game", "GAME_OPTIONS", "cOptionsState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:57`

Связь: `scenes.tsv`, состояние `GAME_MENU` для: FORK1/save-dialog-menu.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '57p'
    {"save-dialog-menu", "GAME_MENU", "SaveSlotsDialog"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:58`

Связь: `scenes.tsv`, состояние `GAME_OPTIONS` для: FORK1/save-dialog-load, FORK1/save-dialog-load-error, FORK1/save-dialog-overwrite, FORK1/save-dialog-save-error, FORK1/save-dialog-save-new.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '58p'
    {"save-dialog", "GAME_OPTIONS", "SaveSlotsDialog"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:59`

Связь: `scenes.tsv`, состояние `GAME_CREDITS` для: FORK1/credits-1, FORK1/credits-2, FORK1/credits-3, FORK1/credits-4, FORK1/credits-5, FORK1/credits-title; `screens.tsv`, экран: титры.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '59p'
    {"credits", "GAME_CREDITS", "cCreditsState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:60`

Связь: `scenes.tsv`, состояние `GAME_PLAYING` для: FORK1/game-command-damaged-unit, FORK1/game-command-harvester, FORK1/game-command-mcv, FORK1/game-group-select, FORK1/game-harkonnen-list-build, FORK1/game-harkonnen-list-infantry, FORK1/game-harkonnen-list-palace, FORK1/game-harkonnen-list-starport, FORK1/game-harkonnen-list-upgrades, FORK1/game-harkonnen-list-vehicles, FORK1/game-hud, FORK1/game-item-hover, FORK1/game-list-build, FORK1/game-list-infantry, FORK1/game-list-palace, FORK1/game-list-scroll-end, FORK1/game-list-starport, FORK1/game-list-upgrades, FORK1/game-list-vehicles, FORK1/game-messages, FORK1/game-music, FORK1/game-ordos-list-build, FORK1/game-ordos-list-infantry, FORK1/game-ordos-list-palace, FORK1/game-ordos-list-starport, FORK1/game-ordos-list-upgrades, FORK1/game-ordos-list-vehicles, FORK1/game-place-allowed, FORK1/game-place-forbidden, FORK1/game-radar-none, FORK1/game-radar-nopower, FORK1/game-rally-point, FORK1/game-structure-selected, FORK1/structure-label-right, FORK1/structure-label-top, FORK1/units-label-devastator, FORK1/units-label-deviator, FORK1/units-label-harvester, FORK1/units-label-infantry, FORK1/units-label-launcher, FORK1/units-label-mcv, FORK1/units-label-quad, FORK1/units-label-raider, FORK1/units-label-saboteur, FORK1/units-label-siegetank, FORK1/units-label-soldier, FORK1/units-label-sonictank, FORK1/units-label-tank, FORK1/units-label-trike, FORK1/units-label-trooper, FORK1/units-label-troopers, FORK1/units-label-unit-fremen-one, FORK1/units-label-unit-fremen-three; `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '60p'
    {"game-playing", "GAME_PLAYING", "cDrawManager"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:61`

Связь: `scenes.tsv`, состояние `GAME_SETUPSKIRMISH` для: FORK1/skirmish-setup-random, FORK1/skirmish-setup-ready-map.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '61p'
    {"skirmish-setup", "GAME_SETUPSKIRMISH", "cSetupSkirmishState"},
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:101`

Связь: `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '101p'
    return UiAuditAccess::prepareMentatScene(game, House, Kind);
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:134`

Связь: `screens.tsv`, экран: главное меню.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '134p'
    UiAuditAccess::setState(game, GAME_MENU);
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:189`

Связь: `screens.tsv`, экран: меню настроек.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '189p'
            UiAuditAccess::setState(game, GAME_OPTIONS);
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:284`

Связь: `screens.tsv`, экран: титры.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '284p'
bool prepareCredits(cGame &game)
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:287`

Связь: `screens.tsv`, экран: титры.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '287p'
    UiAuditAccess::setState(game, GAME_CREDITS);
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:306`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '306p'
template <int Type>
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:317`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '317p'
    return UiAuditAccess::prepareGameScreen(game, House, Kind);
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:327`

Связь: `screens.tsv`, экран: карта кампании.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '327p'
template <int House, int Mission, bool Jump>
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:363`

Связь: `scenes.tsv`, регистрация: FORK1/main-menu.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '363p'
    scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:364`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-intro-1.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '364p'
    scene("region-atreides-intro-1", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<1>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:365`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-intro-2.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '365p'
    scene("region-atreides-intro-2", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<2>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:366`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-intro-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '366p'
    scene("region-atreides-intro-3", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<3>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:367`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-conquer-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '367p'
    scene("region-atreides-conquer-3", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 3, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:368`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-conquer-5.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '368p'
    scene("region-atreides-conquer-5", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 5, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:369`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-conquer-7.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '369p'
    scene("region-atreides-conquer-7", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 7, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:370`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-conquer-9.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '370p'
    scene("region-atreides-conquer-9", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 9, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:371`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-2.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '371p'
    scene("region-atreides-select-2", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 2, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:372`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '372p'
    scene("region-atreides-select-3", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 3, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:373`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-4.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '373p'
    scene("region-atreides-select-4", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 4, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:374`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-5.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '374p'
    scene("region-atreides-select-5", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 5, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:375`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-6.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '375p'
    scene("region-atreides-select-6", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 6, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:376`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-7.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '376p'
    scene("region-atreides-select-7", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 7, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:377`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-8.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '377p'
    scene("region-atreides-select-8", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 8, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:378`

Связь: `scenes.tsv`, регистрация: FORK1/region-atreides-select-9.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '378p'
    scene("region-atreides-select-9", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 9, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:379`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-intro-1.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '379p'
    scene("region-harkonnen-intro-1", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<1>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:380`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-intro-2.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '380p'
    scene("region-harkonnen-intro-2", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<2>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:381`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-intro-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '381p'
    scene("region-harkonnen-intro-3", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<3>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:382`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-conquer-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '382p'
    scene("region-harkonnen-conquer-3", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 3, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:383`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-conquer-5.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '383p'
    scene("region-harkonnen-conquer-5", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 5, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:384`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-conquer-7.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '384p'
    scene("region-harkonnen-conquer-7", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 7, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:385`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-conquer-9.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '385p'
    scene("region-harkonnen-conquer-9", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 9, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:386`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-2.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '386p'
    scene("region-harkonnen-select-2", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 2, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:387`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '387p'
    scene("region-harkonnen-select-3", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 3, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:388`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-4.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '388p'
    scene("region-harkonnen-select-4", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 4, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:389`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-5.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '389p'
    scene("region-harkonnen-select-5", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 5, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:390`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-6.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '390p'
    scene("region-harkonnen-select-6", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 6, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:391`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-7.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '391p'
    scene("region-harkonnen-select-7", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 7, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:392`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-8.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '392p'
    scene("region-harkonnen-select-8", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 8, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:393`

Связь: `scenes.tsv`, регистрация: FORK1/region-harkonnen-select-9.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '393p'
    scene("region-harkonnen-select-9", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 9, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:394`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-intro-1.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '394p'
    scene("region-ordos-intro-1", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<1>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:395`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-intro-2.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '395p'
    scene("region-ordos-intro-2", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<2>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:396`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-intro-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '396p'
    scene("region-ordos-intro-3", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<3>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:397`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-conquer-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '397p'
    scene("region-ordos-conquer-3", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 3, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:398`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-conquer-5.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '398p'
    scene("region-ordos-conquer-5", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 5, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:399`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-conquer-7.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '399p'
    scene("region-ordos-conquer-7", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 7, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:400`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-conquer-9.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '400p'
    scene("region-ordos-conquer-9", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 9, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:401`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-2.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '401p'
    scene("region-ordos-select-2", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 2, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:402`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '402p'
    scene("region-ordos-select-3", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 3, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:403`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-4.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '403p'
    scene("region-ordos-select-4", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 4, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:404`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-5.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '404p'
    scene("region-ordos-select-5", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 5, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:405`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-6.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '405p'
    scene("region-ordos-select-6", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 6, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:406`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-7.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '406p'
    scene("region-ordos-select-7", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 7, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:407`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-8.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '407p'
    scene("region-ordos-select-8", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 8, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:408`

Связь: `scenes.tsv`, регистрация: FORK1/region-ordos-select-9.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '408p'
    scene("region-ordos-select-9", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 9, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:409`

Связь: `scenes.tsv`, регистрация: FORK1/choose-house.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '409p'
    scene("choose-house", "choose-house", "", "StateSettled", prepareChooseHouse),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:410`

Связь: `scenes.tsv`, регистрация: FORK1/select-mission-atreides.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '410p'
    scene("select-mission-atreides", "select-mission", "atreides", "StateSettled", prepareSelectMission<ATREIDES>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:411`

Связь: `scenes.tsv`, регистрация: FORK1/select-mission-harkonnen.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '411p'
    scene("select-mission-harkonnen", "select-mission", "harkonnen", "StateSettled",
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:413`

Связь: `scenes.tsv`, регистрация: FORK1/select-mission-ordos.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '413p'
    scene("select-mission-ordos", "select-mission", "ordos", "StateSettled", prepareSelectMission<ORDOS>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:414`

Связь: `scenes.tsv`, регистрация: FORK1/tellhouse-atreides-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '414p'
    scene("tellhouse-atreides-speak", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, false>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:416`

Связь: `scenes.tsv`, регистрация: FORK1/tellhouse-atreides-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '416p'
    scene("tellhouse-atreides-await", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:418`

Связь: `scenes.tsv`, регистрация: FORK1/tellhouse-harkonnen-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '418p'
    scene("tellhouse-harkonnen-speak", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, false>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:420`

Связь: `scenes.tsv`, регистрация: FORK1/tellhouse-harkonnen-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '420p'
    scene("tellhouse-harkonnen-await", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:422`

Связь: `scenes.tsv`, регистрация: FORK1/tellhouse-ordos-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '422p'
    scene("tellhouse-ordos-speak", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, false>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:424`

Связь: `scenes.tsv`, регистрация: FORK1/tellhouse-ordos-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '424p'
    scene("tellhouse-ordos-await", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:426`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-briefing-atreides-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '426p'
    withScreen(scene("mentat-briefing-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:427`

Связь: `scenes.tsv`, состояние `GAME_BRIEFING` для: FORK1/mentat-briefing-atreides-speak; `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '427p'
                     readyMentatFrozen<false>), "GAME_BRIEFING", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:428`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-briefing-atreides-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '428p'
    withScreen(scene("mentat-briefing-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:429`

Связь: `scenes.tsv`, состояние `GAME_BRIEFING` для: FORK1/mentat-briefing-atreides-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '429p'
                     readyMentatFrozen<true>), "GAME_BRIEFING", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:430`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-win-atreides-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '430p'
    withScreen(scene("mentat-win-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:431`

Связь: `scenes.tsv`, состояние `GAME_WINBRIEF` для: FORK1/mentat-win-atreides-speak; `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '431p'
                     readyMentatFrozen<false>), "GAME_WINBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:432`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-win-atreides-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '432p'
    withScreen(scene("mentat-win-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:433`

Связь: `scenes.tsv`, состояние `GAME_WINBRIEF` для: FORK1/mentat-win-atreides-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '433p'
                     readyMentatFrozen<true>), "GAME_WINBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:434`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-lose-atreides-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '434p'
    withScreen(scene("mentat-lose-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:435`

Связь: `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: FORK1/mentat-lose-atreides-speak; `screens.tsv`, экран: ментат.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '435p'
                     readyMentatFrozen<false>), "GAME_LOSEBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:436`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-lose-atreides-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '436p'
    withScreen(scene("mentat-lose-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:437`

Связь: `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: FORK1/mentat-lose-atreides-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '437p'
                     readyMentatFrozen<true>), "GAME_LOSEBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:438`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-briefing-harkonnen-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '438p'
    withScreen(scene("mentat-briefing-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:439`

Связь: `scenes.tsv`, состояние `GAME_BRIEFING` для: FORK1/mentat-briefing-harkonnen-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '439p'
                     readyMentatFrozen<false>), "GAME_BRIEFING", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:440`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-briefing-harkonnen-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '440p'
    withScreen(scene("mentat-briefing-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:441`

Связь: `scenes.tsv`, состояние `GAME_BRIEFING` для: FORK1/mentat-briefing-harkonnen-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '441p'
                     readyMentatFrozen<true>), "GAME_BRIEFING", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:442`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-win-harkonnen-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '442p'
    withScreen(scene("mentat-win-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:443`

Связь: `scenes.tsv`, состояние `GAME_WINBRIEF` для: FORK1/mentat-win-harkonnen-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '443p'
                     readyMentatFrozen<false>), "GAME_WINBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:444`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-win-harkonnen-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '444p'
    withScreen(scene("mentat-win-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:445`

Связь: `scenes.tsv`, состояние `GAME_WINBRIEF` для: FORK1/mentat-win-harkonnen-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '445p'
                     readyMentatFrozen<true>), "GAME_WINBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:446`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-lose-harkonnen-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '446p'
    withScreen(scene("mentat-lose-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:447`

Связь: `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: FORK1/mentat-lose-harkonnen-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '447p'
                     readyMentatFrozen<false>), "GAME_LOSEBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:448`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-lose-harkonnen-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '448p'
    withScreen(scene("mentat-lose-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:449`

Связь: `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: FORK1/mentat-lose-harkonnen-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '449p'
                     readyMentatFrozen<true>), "GAME_LOSEBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:450`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-briefing-ordos-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '450p'
    withScreen(scene("mentat-briefing-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:451`

Связь: `scenes.tsv`, состояние `GAME_BRIEFING` для: FORK1/mentat-briefing-ordos-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '451p'
                     readyMentatFrozen<false>), "GAME_BRIEFING", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:452`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-briefing-ordos-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '452p'
    withScreen(scene("mentat-briefing-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:453`

Связь: `scenes.tsv`, состояние `GAME_BRIEFING` для: FORK1/mentat-briefing-ordos-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '453p'
                     readyMentatFrozen<true>), "GAME_BRIEFING", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:454`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-win-ordos-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '454p'
    withScreen(scene("mentat-win-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:455`

Связь: `scenes.tsv`, состояние `GAME_WINBRIEF` для: FORK1/mentat-win-ordos-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '455p'
                     readyMentatFrozen<false>), "GAME_WINBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:456`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-win-ordos-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '456p'
    withScreen(scene("mentat-win-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:457`

Связь: `scenes.tsv`, состояние `GAME_WINBRIEF` для: FORK1/mentat-win-ordos-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '457p'
                     readyMentatFrozen<true>), "GAME_WINBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:458`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-lose-ordos-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '458p'
    withScreen(scene("mentat-lose-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:459`

Связь: `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: FORK1/mentat-lose-ordos-speak.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '459p'
                     readyMentatFrozen<false>), "GAME_LOSEBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:460`

Связь: `scenes.tsv`, регистрация: FORK1/mentat-lose-ordos-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '460p'
    withScreen(scene("mentat-lose-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:461`

Связь: `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: FORK1/mentat-lose-ordos-await.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '461p'
                     readyMentatFrozen<true>), "GAME_LOSEBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:462`

Связь: `scenes.tsv`, регистрация: FORK1/skirmish-setup-random; `screens.tsv`, экран: схватка с боковой панелью.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '462p'
    scene("skirmish-setup-random", "skirmish-setup", "", "FixedFrames(2, no readiness flag)", prepareSkirmishSetup<0>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:463`

Связь: `scenes.tsv`, регистрация: FORK1/skirmish-setup-ready-map.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '463p'
    scene("skirmish-setup-ready-map", "skirmish-setup", "", "FixedFrames(2, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:465`

Связь: `scenes.tsv`, регистрация: FORK1/outcome-win.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '465p'
    withScreen(scene("outcome-win", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:466`

Связь: `scenes.tsv`, состояние `GAME_WINNING` для: FORK1/outcome-win.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '466p'
                     readyOutcome<true>), "GAME_WINNING", "cGame::drawOutcomeScreen"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:467`

Связь: `scenes.tsv`, регистрация: FORK1/outcome-lose.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '467p'
    withScreen(scene("outcome-lose", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<false>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:468`

Связь: `scenes.tsv`, состояние `GAME_LOSING` для: FORK1/outcome-lose.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '468p'
                     readyOutcome<false>), "GAME_LOSING", "cGame::drawOutcomeScreen"),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:469`

Связь: `scenes.tsv`, регистрация: FORK1/options-menu-main.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '469p'
    scene("options-menu-main", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:471`

Связь: `scenes.tsv`, регистрация: FORK1/options-menu-applied.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '471p'
    scene("options-menu-applied", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:473`

Связь: `scenes.tsv`, регистрация: FORK1/options-menu-game.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '473p'
    scene("options-menu-game", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<2>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:475`

Связь: `scenes.tsv`, регистрация: FORK1/options-menu-controls.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '475p'
    scene("options-menu-controls", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<3>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:477`

Связь: `scenes.tsv`, регистрация: FORK1/options-menu-diagnostics.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '477p'
    scene("options-menu-diagnostics", "options-menu", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:479`

Связь: `scenes.tsv`, регистрация: FORK1/options-menu-keybind.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '479p'
    scene("options-menu-keybind", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<5>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:481`

Связь: `scenes.tsv`, регистрация: FORK1/main-menu-saves.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '481p'
    scene("main-menu-saves", "main-menu", "", "StateSettled", prepareMenuWithSaves),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:482`

Связь: `scenes.tsv`, регистрация: FORK1/save-dialog-menu.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '482p'
    scene("save-dialog-menu", "save-dialog-menu", "", "FixedFrames(10, no readiness flag)", prepareMenuWithSaves,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:484`

Связь: `scenes.tsv`, регистрация: FORK1/options-game-main-saves.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '484p'
    scene("options-game-main-saves", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:486`

Связь: `scenes.tsv`, регистрация: FORK1/options-game-main-nosaves.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '486p'
    scene("options-game-main-nosaves", "options-game", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:488`

Связь: `scenes.tsv`, регистрация: FORK1/options-game-applied.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '488p'
    scene("options-game-applied", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:490`

Связь: `scenes.tsv`, регистрация: FORK1/options-game-game.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '490p'
    scene("options-game-game", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:492`

Связь: `scenes.tsv`, регистрация: FORK1/options-game-controls.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '492p'
    scene("options-game-controls", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:494`

Связь: `scenes.tsv`, регистрация: FORK1/options-game-diagnostics.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '494p'
    scene("options-game-diagnostics", "options-game", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:496`

Связь: `scenes.tsv`, регистрация: FORK1/options-game-keybind.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '496p'
    scene("options-game-keybind", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:498`

Связь: `scenes.tsv`, регистрация: FORK1/save-dialog-load.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '498p'
    scene("save-dialog-load", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:500`

Связь: `scenes.tsv`, регистрация: FORK1/save-dialog-save-new.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '500p'
    scene("save-dialog-save-new", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:502`

Связь: `scenes.tsv`, регистрация: FORK1/save-dialog-overwrite.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '502p'
    scene("save-dialog-overwrite", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:504`

Связь: `scenes.tsv`, регистрация: FORK1/save-dialog-load-error.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '504p'
    scene("save-dialog-load-error", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:506`

Связь: `scenes.tsv`, регистрация: FORK1/save-dialog-save-error.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '506p'
    scene("save-dialog-save-error", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:508`

Связь: `scenes.tsv`, регистрация: FORK1/credits-title.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '508p'
    scene("credits-title", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<0>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:509`

Связь: `scenes.tsv`, регистрация: FORK1/credits-1.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '509p'
    scene("credits-1", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<1>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:510`

Связь: `scenes.tsv`, регистрация: FORK1/credits-2.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '510p'
    scene("credits-2", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<2>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:511`

Связь: `scenes.tsv`, регистрация: FORK1/credits-3.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '511p'
    scene("credits-3", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<3>),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:512`

Связь: `scenes.tsv`, регистрация: FORK1/credits-4.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '512p'
    hdOnly(scene("credits-4", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<4>)),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:513`

Связь: `scenes.tsv`, регистрация: FORK1/credits-5.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '513p'
    hdOnly(scene("credits-5", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<5>)),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:514`

Связь: `scenes.tsv`, регистрация: FORK1/structure-label-top.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '514p'
    onGameScreen(scene("structure-label-top", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<0>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:516`

Связь: `scenes.tsv`, регистрация: FORK1/structure-label-right.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '516p'
    onGameScreen(scene("structure-label-right", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<1>,
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:518`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-trike.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '518p'
    onGameScreen(scene("units-label-trike", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TRIKE>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:519`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-raider.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '519p'
    onGameScreen(scene("units-label-raider", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<RAIDER>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:520`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-quad.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '520p'
    onGameScreen(scene("units-label-quad", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<QUAD>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:521`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-tank.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '521p'
    onGameScreen(scene("units-label-tank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TANK>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:522`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-siegetank.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '522p'
    onGameScreen(scene("units-label-siegetank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SIEGETANK>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:523`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-launcher.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '523p'
    onGameScreen(scene("units-label-launcher", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<LAUNCHER>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:524`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-deviator.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '524p'
    onGameScreen(scene("units-label-deviator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVIATOR>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:525`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-sonictank.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '525p'
    onGameScreen(scene("units-label-sonictank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SONICTANK>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:526`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-devastator.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '526p'
    onGameScreen(scene("units-label-devastator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVASTATOR>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:527`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-harvester.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '527p'
    onGameScreen(scene("units-label-harvester", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<HARVESTER>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:528`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-mcv.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '528p'
    onGameScreen(scene("units-label-mcv", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<MCV>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:529`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-soldier.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '529p'
    onGameScreen(scene("units-label-soldier", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SOLDIER>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:530`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-infantry.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '530p'
    onGameScreen(scene("units-label-infantry", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<INFANTRY>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:531`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-trooper.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '531p'
    onGameScreen(scene("units-label-trooper", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPER>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:532`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-troopers.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '532p'
    onGameScreen(scene("units-label-troopers", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPERS>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:533`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-unit-fremen-one.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '533p'
    onGameScreen(scene("units-label-unit-fremen-one", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_ONE>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:534`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-unit-fremen-three.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '534p'
    onGameScreen(scene("units-label-unit-fremen-three", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_THREE>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:535`

Связь: `scenes.tsv`, регистрация: FORK1/units-label-saboteur.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '535p'
    onGameScreen(scene("units-label-saboteur", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SABOTEUR>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:536`

Связь: `scenes.tsv`, регистрация: FORK1/game-hud.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '536p'
    withHud(onGameScreen(scene("game-hud", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Hud>), false)),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:537`

Связь: `scenes.tsv`, регистрация: FORK1/game-music.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '537p'
    onGameScreen(scene("game-music", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Music>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:538`

Связь: `scenes.tsv`, регистрация: FORK1/game-command-damaged-unit.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '538p'
    onGameScreen(scene("game-command-damaged-unit", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::DamagedUnit>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:539`

Связь: `scenes.tsv`, регистрация: FORK1/game-command-harvester.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '539p'
    onGameScreen(scene("game-command-harvester", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Harvester>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:540`

Связь: `scenes.tsv`, регистрация: FORK1/game-command-mcv.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '540p'
    onGameScreen(scene("game-command-mcv", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Mcv>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:541`

Связь: `scenes.tsv`, регистрация: FORK1/game-structure-selected.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '541p'
    onGameScreen(scene("game-structure-selected", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Structure>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:542`

Связь: `scenes.tsv`, регистрация: FORK1/game-list-build.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '542p'
    onGameScreen(scene("game-list-build", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListBuild>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:543`

Связь: `scenes.tsv`, регистрация: FORK1/game-list-infantry.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '543p'
    onGameScreen(scene("game-list-infantry", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListInfantry>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:544`

Связь: `scenes.tsv`, регистрация: FORK1/game-list-vehicles.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '544p'
    onGameScreen(scene("game-list-vehicles", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListVehicles>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:545`

Связь: `scenes.tsv`, регистрация: FORK1/game-list-starport.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '545p'
    onGameScreen(scene("game-list-starport", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListStarport>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:546`

Связь: `scenes.tsv`, регистрация: FORK1/game-list-palace.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '546p'
    onGameScreen(scene("game-list-palace", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListPalace>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:547`

Связь: `scenes.tsv`, регистрация: FORK1/game-list-upgrades.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '547p'
    onGameScreen(scene("game-list-upgrades", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListUpgrades>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:548`

Связь: `scenes.tsv`, регистрация: FORK1/game-radar-none.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '548p'
    onGameScreen(scene("game-radar-none", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RadarNone>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:549`

Связь: `scenes.tsv`, регистрация: FORK1/game-radar-nopower.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '549p'
    onGameScreen(scene("game-radar-nopower", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RadarNoPower>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:550`

Связь: `scenes.tsv`, регистрация: FORK1/game-place-allowed.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '550p'
    onGameScreen(scene("game-place-allowed", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::PlaceAllowed>), true),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:551`

Связь: `scenes.tsv`, регистрация: FORK1/game-place-forbidden.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '551p'
    onGameScreen(scene("game-place-forbidden", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::PlaceForbidden>), true),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:552`

Связь: `scenes.tsv`, регистрация: FORK1/game-group-select.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '552p'
    onGameScreen(scene("game-group-select", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::GroupSelect>), true),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:553`

Связь: `scenes.tsv`, регистрация: FORK1/game-messages.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '553p'
    onGameScreen(scene("game-messages", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Messages>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:554`

Связь: `scenes.tsv`, регистрация: FORK1/game-item-hover.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '554p'
    onGameScreen(scene("game-item-hover", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ItemHover>), true),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:555`

Связь: `scenes.tsv`, регистрация: FORK1/game-list-scroll-end.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '555p'
    hdOnly(onGameScreen(scene("game-list-scroll-end", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ScrollEnd>), false)),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:556`

Связь: `scenes.tsv`, регистрация: FORK1/game-rally-point.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '556p'
    onGameScreen(scene("game-rally-point", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Rally>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:557`

Связь: `scenes.tsv`, регистрация: FORK1/game-harkonnen-list-build.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '557p'
    onGameScreen(scene("game-harkonnen-list-build", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListBuild>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:558`

Связь: `scenes.tsv`, регистрация: FORK1/game-harkonnen-list-infantry.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '558p'
    onGameScreen(scene("game-harkonnen-list-infantry", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListInfantry>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:559`

Связь: `scenes.tsv`, регистрация: FORK1/game-harkonnen-list-vehicles.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '559p'
    onGameScreen(scene("game-harkonnen-list-vehicles", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListVehicles>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:560`

Связь: `scenes.tsv`, регистрация: FORK1/game-harkonnen-list-starport.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '560p'
    onGameScreen(scene("game-harkonnen-list-starport", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListStarport>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:561`

Связь: `scenes.tsv`, регистрация: FORK1/game-harkonnen-list-palace.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '561p'
    onGameScreen(scene("game-harkonnen-list-palace", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListPalace>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:562`

Связь: `scenes.tsv`, регистрация: FORK1/game-harkonnen-list-upgrades.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '562p'
    onGameScreen(scene("game-harkonnen-list-upgrades", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListUpgrades>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:563`

Связь: `scenes.tsv`, регистрация: FORK1/game-ordos-list-build.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '563p'
    onGameScreen(scene("game-ordos-list-build", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListBuild>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:564`

Связь: `scenes.tsv`, регистрация: FORK1/game-ordos-list-infantry.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '564p'
    onGameScreen(scene("game-ordos-list-infantry", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListInfantry>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:565`

Связь: `scenes.tsv`, регистрация: FORK1/game-ordos-list-vehicles.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '565p'
    onGameScreen(scene("game-ordos-list-vehicles", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListVehicles>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:566`

Связь: `scenes.tsv`, регистрация: FORK1/game-ordos-list-starport.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '566p'
    onGameScreen(scene("game-ordos-list-starport", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListStarport>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:567`

Связь: `scenes.tsv`, регистрация: FORK1/game-ordos-list-palace.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '567p'
    onGameScreen(scene("game-ordos-list-palace", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListPalace>), false),
```

#### `src/debug/UiAuditScenes.cpp@9208dcf:568`

Связь: `scenes.tsv`, регистрация: FORK1/game-ordos-list-upgrades.

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '568p'
    onGameScreen(scene("game-ordos-list-upgrades", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListUpgrades>), false),
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:118`

Связь: `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '118p'
bool UiAuditAccess::prepareMentatScene(cGame &currentGame, int house, int kind)
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:124`

Связь: `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '124p'
        currentGame.setNextStateToTransitionTo(GAME_BRIEFING);
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:128`

Связь: `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '128p'
        currentGame.setState(kind == 1 ? GAME_WINBRIEF : GAME_LOSEBRIEF);
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:252`

Связь: `screens.tsv`, экран: карта кампании.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '252p'
void UiAuditAccess::regionOpen(cGame &currentGame, int mission, bool jump)
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:260`

Связь: `screens.tsv`, экран: карта кампании.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '260p'
    currentGame.setState(GAME_REGION);
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:497`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '497p'
bool UiAuditAccess::enterPlaying(cGame &currentGame, int house, int region)
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:504`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '504p'
    currentGame.setNextStateToTransitionTo(GAME_PLAYING);
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:773`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '773p'
bool UiAuditAccess::prepareGameScreen(cGame &currentGame, int house, int kind)
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:776`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '776p'
    if (!enterPlaying(currentGame, house, 22)) {
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:968`

Связь: `screens.tsv`, экран: схватка с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '968p'
bool UiAuditAccess::startSkirmish(cGame &currentGame)
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:975`

Связь: `screens.tsv`, экран: схватка с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '975p'
    setup->prepareSkirmishGameToPlayAndTransitionToCombatState(setup->iSkirmishMap);
```

#### `src/debug/UiAuditAccess.cpp@010a6eb:984`

Связь: `screens.tsv`, экран: схватка с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditAccess.cpp | sed -n '984p'
    return currentGame.m_state == GAME_PLAYING;
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:47`

Связь: `scenes.tsv`, состояние `GAME_MENU` для: PORT/main-menu, PORT/main-menu-saves; `screens.tsv`, экран: главное меню.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '47p'
    {"main-menu", "GAME_MENU", "cMainMenuState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:48`

Связь: `scenes.tsv`, состояние `GAME_REGION` для: PORT/region-atreides-conquer-3, PORT/region-atreides-conquer-5, PORT/region-atreides-conquer-7, PORT/region-atreides-conquer-9, PORT/region-atreides-intro-1, PORT/region-atreides-intro-2, PORT/region-atreides-intro-3, PORT/region-atreides-select-2, PORT/region-atreides-select-3, PORT/region-atreides-select-4, PORT/region-atreides-select-5, PORT/region-atreides-select-6, PORT/region-atreides-select-7, PORT/region-atreides-select-8, PORT/region-atreides-select-9, PORT/region-harkonnen-conquer-3, PORT/region-harkonnen-conquer-5, PORT/region-harkonnen-conquer-7, PORT/region-harkonnen-conquer-9, PORT/region-harkonnen-intro-1, PORT/region-harkonnen-intro-2, PORT/region-harkonnen-intro-3, PORT/region-harkonnen-select-2, PORT/region-harkonnen-select-3, PORT/region-harkonnen-select-4, PORT/region-harkonnen-select-5, PORT/region-harkonnen-select-6, PORT/region-harkonnen-select-7, PORT/region-harkonnen-select-8, PORT/region-harkonnen-select-9, PORT/region-ordos-conquer-3, PORT/region-ordos-conquer-5, PORT/region-ordos-conquer-7, PORT/region-ordos-conquer-9, PORT/region-ordos-intro-1, PORT/region-ordos-intro-2, PORT/region-ordos-intro-3, PORT/region-ordos-select-2, PORT/region-ordos-select-3, PORT/region-ordos-select-4, PORT/region-ordos-select-5, PORT/region-ordos-select-6, PORT/region-ordos-select-7, PORT/region-ordos-select-8, PORT/region-ordos-select-9, PORT/region-sardaukar-conquer-3, PORT/region-sardaukar-conquer-5, PORT/region-sardaukar-conquer-7, PORT/region-sardaukar-conquer-9, PORT/region-sardaukar-intro-1, PORT/region-sardaukar-intro-2, PORT/region-sardaukar-intro-3, PORT/region-sardaukar-select-2, PORT/region-sardaukar-select-3, PORT/region-sardaukar-select-4, PORT/region-sardaukar-select-5, PORT/region-sardaukar-select-6, PORT/region-sardaukar-select-7, PORT/region-sardaukar-select-8, PORT/region-sardaukar-select-9; `screens.tsv`, экран: карта кампании.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '48p'
    {"region", "GAME_REGION", "cSelectYourNextConquestState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:49`

Связь: `scenes.tsv`, состояние `GAME_SELECT_HOUSE` для: PORT/choose-house.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '49p'
    {"choose-house", "GAME_SELECT_HOUSE", "cChooseHouseState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:50`

Связь: `scenes.tsv`, состояние `GAME_MISSIONSELECT` для: PORT/select-mission-atreides, PORT/select-mission-harkonnen, PORT/select-mission-ordos, PORT/select-mission-sardaukar.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '50p'
    {"select-mission", "GAME_MISSIONSELECT", "cSelectMissionState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:51`

Связь: `scenes.tsv`, состояние `GAME_TELLHOUSE` для: PORT/tellhouse-atreides-await, PORT/tellhouse-atreides-speak, PORT/tellhouse-harkonnen-await, PORT/tellhouse-harkonnen-speak, PORT/tellhouse-ordos-await, PORT/tellhouse-ordos-speak, PORT/tellhouse-sardaukar-await, PORT/tellhouse-sardaukar-speak; `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '51p'
    {"tellhouse", "GAME_TELLHOUSE", "BeneMentat"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:52`

Связь: `scenes.tsv`, состояние `GAME_OPTIONS` для: PORT/options-menu-applied, PORT/options-menu-main; `screens.tsv`, экран: меню настроек.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '52p'
    {"options-menu", "GAME_OPTIONS", "cOptionsState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:53`

Связь: `scenes.tsv`, состояние `GAME_CREDITS` для: PORT/credits-1, PORT/credits-2, PORT/credits-3, PORT/credits-4, PORT/credits-5, PORT/credits-title; `screens.tsv`, экран: титры.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '53p'
    {"credits", "GAME_CREDITS", "cCreditsState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:54`

Связь: `scenes.tsv`, состояние `GAME_SETUPSKIRMISH` для: PORT/skirmish-setup-random, PORT/skirmish-setup-ready-map.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '54p'
    {"skirmish-setup", "GAME_SETUPSKIRMISH", "cSetupSkirmishState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:55`

Связь: `scenes.tsv`, состояние `GAME_PLAYING` для: PORT/game-command-damaged-unit, PORT/game-command-harvester, PORT/game-command-mcv, PORT/game-group-select, PORT/game-harkonnen-list-build, PORT/game-harkonnen-list-infantry, PORT/game-harkonnen-list-palace, PORT/game-harkonnen-list-starport, PORT/game-harkonnen-list-upgrades, PORT/game-harkonnen-list-vehicles, PORT/game-hud, PORT/game-item-hover, PORT/game-list-build, PORT/game-list-infantry, PORT/game-list-palace, PORT/game-list-scroll-end, PORT/game-list-starport, PORT/game-list-upgrades, PORT/game-list-vehicles, PORT/game-messages, PORT/game-music, PORT/game-ordos-list-build, PORT/game-ordos-list-infantry, PORT/game-ordos-list-palace, PORT/game-ordos-list-starport, PORT/game-ordos-list-upgrades, PORT/game-ordos-list-vehicles, PORT/game-place-allowed, PORT/game-place-forbidden, PORT/game-radar-none, PORT/game-radar-nopower, PORT/game-rally-point, PORT/game-sardaukar-list-build, PORT/game-sardaukar-list-infantry, PORT/game-sardaukar-list-palace, PORT/game-sardaukar-list-starport, PORT/game-sardaukar-list-upgrades, PORT/game-sardaukar-list-vehicles, PORT/game-structure-selected, PORT/save-roundtrip, PORT/structure-label-right, PORT/structure-label-top, PORT/units-label-devastator, PORT/units-label-deviator, PORT/units-label-harvester, PORT/units-label-infantry, PORT/units-label-launcher, PORT/units-label-mcv, PORT/units-label-quad, PORT/units-label-raider, PORT/units-label-saboteur, PORT/units-label-siegetank, PORT/units-label-soldier, PORT/units-label-sonictank, PORT/units-label-tank, PORT/units-label-trike, PORT/units-label-trooper, PORT/units-label-troopers, PORT/units-label-unit-fremen-one, PORT/units-label-unit-fremen-three; `screens.tsv`, экран: миссия кампании с боковой панелью, схватка с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '55p'
    {"game-playing", "GAME_PLAYING", "cGamePlaying"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:56`

Связь: `scenes.tsv`, состояние `GAME_OPTIONS` для: PORT/options-game-applied, PORT/options-game-main-nosaves, PORT/options-game-main-saves.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '56p'
    {"options-game", "GAME_OPTIONS", "cOptionsState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:57`

Связь: `scenes.tsv`, состояние `GAME_MENU` для: PORT/save-dialog-menu.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '57p'
    {"save-dialog-menu", "GAME_MENU", "SaveSlotsDialog"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:58`

Связь: `scenes.tsv`, состояние `GAME_OPTIONS` для: PORT/save-dialog-load, PORT/save-dialog-load-error, PORT/save-dialog-overwrite, PORT/save-dialog-save-error, PORT/save-dialog-save-new.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '58p'
    {"save-dialog", "GAME_OPTIONS", "SaveSlotsDialog"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:59`

Связь: `scenes.tsv`, состояние `GAME_SCORING` для: PORT/scoring.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '59p'
    {"scoring", "GAME_SCORING", "cScoringState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:60`

Связь: `scenes.tsv`, состояние `GAME_NEW_MAP_EDITOR` для: PORT/editor-new-map.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '60p'
    {"new-map-editor", "GAME_NEW_MAP_EDITOR", "cNewMapEditorState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:61`

Связь: `scenes.tsv`, состояние `GAME_EDITOR` для: PORT/editor-start-cells, PORT/editor-symmetry, PORT/editor-topology.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '61p'
    {"editor", "GAME_EDITOR", "cEditorState"},
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:100`

Связь: `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '100p'
    return UiAuditAccess::prepareMentatScene(game, House, Kind);
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:158`

Связь: `screens.tsv`, экран: главное меню.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '158p'
    UiAuditAccess::setState(game, GAME_MENU);
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:212`

Связь: `screens.tsv`, экран: меню настроек.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '212p'
            UiAuditAccess::setState(game, GAME_OPTIONS);
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:228`

Связь: `screens.tsv`, экран: титры.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '228p'
bool prepareCredits(cGame &game)
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:231`

Связь: `screens.tsv`, экран: титры.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '231p'
    UiAuditAccess::setState(game, GAME_CREDITS);
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:250`

Связь: `screens.tsv`, экран: карта кампании.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '250p'
template <int House, int Mission, bool Jump>
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:255`

Связь: `screens.tsv`, экран: карта кампании.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '255p'
    UiAuditAccess::regionOpen(game, Mission, Jump);
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:353`

Связь: `screens.tsv`, экран: схватка с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '353p'
    return UiAuditAccess::startSkirmish(game) && UiAuditAccess::saveRoundTrip(game);
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:357`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '357p'
bool prepareUnitLabels(cGame &game)
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:374`

Связь: `screens.tsv`, экран: миссия кампании с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '374p'
    return UiAuditAccess::prepareGameScreen(game, House, Kind);
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:378`

Связь: `scenes.tsv`, регистрация: PORT/main-menu.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '378p'
    scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:379`

Связь: `scenes.tsv`, регистрация: PORT/main-menu-saves.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '379p'
    scene("main-menu-saves", "main-menu", "", "StateSettled", prepareMenuWithSaves),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:380`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-intro-1.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '380p'
    scene("region-atreides-intro-1", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:381`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-intro-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '381p'
    scene("region-atreides-intro-2", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<2>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:382`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-intro-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '382p'
    scene("region-atreides-intro-3", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<3>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:383`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-conquer-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '383p'
    scene("region-atreides-conquer-3", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 3, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:384`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-conquer-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '384p'
    scene("region-atreides-conquer-5", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 5, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:385`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-conquer-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '385p'
    scene("region-atreides-conquer-7", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 7, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:386`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-conquer-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '386p'
    scene("region-atreides-conquer-9", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 9, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:387`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '387p'
    scene("region-atreides-select-2", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 2, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:388`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '388p'
    scene("region-atreides-select-3", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 3, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:389`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-4.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '389p'
    scene("region-atreides-select-4", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 4, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:390`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '390p'
    scene("region-atreides-select-5", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 5, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:391`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-6.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '391p'
    scene("region-atreides-select-6", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 6, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:392`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '392p'
    scene("region-atreides-select-7", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 7, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:393`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-8.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '393p'
    scene("region-atreides-select-8", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 8, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:394`

Связь: `scenes.tsv`, регистрация: PORT/region-atreides-select-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '394p'
    scene("region-atreides-select-9", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 9, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:395`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-intro-1.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '395p'
    scene("region-harkonnen-intro-1", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:396`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-intro-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '396p'
    scene("region-harkonnen-intro-2", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<2>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:397`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-intro-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '397p'
    scene("region-harkonnen-intro-3", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<3>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:398`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-conquer-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '398p'
    scene("region-harkonnen-conquer-3", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 3, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:399`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-conquer-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '399p'
    scene("region-harkonnen-conquer-5", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 5, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:400`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-conquer-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '400p'
    scene("region-harkonnen-conquer-7", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 7, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:401`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-conquer-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '401p'
    scene("region-harkonnen-conquer-9", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 9, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:402`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '402p'
    scene("region-harkonnen-select-2", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 2, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:403`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '403p'
    scene("region-harkonnen-select-3", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 3, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:404`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-4.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '404p'
    scene("region-harkonnen-select-4", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 4, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:405`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '405p'
    scene("region-harkonnen-select-5", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 5, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:406`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-6.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '406p'
    scene("region-harkonnen-select-6", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 6, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:407`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '407p'
    scene("region-harkonnen-select-7", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 7, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:408`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-8.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '408p'
    scene("region-harkonnen-select-8", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 8, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:409`

Связь: `scenes.tsv`, регистрация: PORT/region-harkonnen-select-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '409p'
    scene("region-harkonnen-select-9", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 9, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:410`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-intro-1.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '410p'
    scene("region-ordos-intro-1", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:411`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-intro-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '411p'
    scene("region-ordos-intro-2", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<2>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:412`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-intro-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '412p'
    scene("region-ordos-intro-3", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<3>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:413`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-conquer-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '413p'
    scene("region-ordos-conquer-3", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 3, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:414`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-conquer-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '414p'
    scene("region-ordos-conquer-5", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 5, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:415`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-conquer-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '415p'
    scene("region-ordos-conquer-7", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 7, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:416`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-conquer-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '416p'
    scene("region-ordos-conquer-9", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 9, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:417`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '417p'
    scene("region-ordos-select-2", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 2, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:418`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '418p'
    scene("region-ordos-select-3", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 3, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:419`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-4.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '419p'
    scene("region-ordos-select-4", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 4, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:420`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '420p'
    scene("region-ordos-select-5", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 5, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:421`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-6.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '421p'
    scene("region-ordos-select-6", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 6, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:422`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '422p'
    scene("region-ordos-select-7", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 7, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:423`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-8.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '423p'
    scene("region-ordos-select-8", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 8, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:424`

Связь: `scenes.tsv`, регистрация: PORT/region-ordos-select-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '424p'
    scene("region-ordos-select-9", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 9, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:425`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-intro-1.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '425p'
    scene("region-sardaukar-intro-1", "region", "sardaukar", "RegionIntroScene", prepareRegion<SARDAUKAR, 1, false>, readyRegionIntro<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:426`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-intro-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '426p'
    scene("region-sardaukar-intro-2", "region", "sardaukar", "RegionIntroScene", prepareRegion<SARDAUKAR, 1, false>, readyRegionIntro<2>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:427`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-intro-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '427p'
    scene("region-sardaukar-intro-3", "region", "sardaukar", "RegionIntroScene", prepareRegion<SARDAUKAR, 1, false>, readyRegionIntro<3>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:428`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-conquer-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '428p'
    scene("region-sardaukar-conquer-3", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 3, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:429`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-conquer-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '429p'
    scene("region-sardaukar-conquer-5", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 5, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:430`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-conquer-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '430p'
    scene("region-sardaukar-conquer-7", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 7, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:431`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-conquer-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '431p'
    scene("region-sardaukar-conquer-9", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 9, true>, readyRegionConquer, 1),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:432`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '432p'
    scene("region-sardaukar-select-2", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 2, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:433`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '433p'
    scene("region-sardaukar-select-3", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 3, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:434`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-4.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '434p'
    scene("region-sardaukar-select-4", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 4, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:435`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '435p'
    scene("region-sardaukar-select-5", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 5, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:436`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-6.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '436p'
    scene("region-sardaukar-select-6", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 6, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:437`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-7.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '437p'
    scene("region-sardaukar-select-7", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 7, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:438`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-8.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '438p'
    scene("region-sardaukar-select-8", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 8, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:439`

Связь: `scenes.tsv`, регистрация: PORT/region-sardaukar-select-9.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '439p'
    scene("region-sardaukar-select-9", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 9, true>, readyRegionSelect),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:440`

Связь: `scenes.tsv`, регистрация: PORT/choose-house.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '440p'
    scene("choose-house", "choose-house", "", "StateSettled", prepareChooseHouse),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:441`

Связь: `scenes.tsv`, регистрация: PORT/select-mission-atreides.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '441p'
    scene("select-mission-atreides", "select-mission", "atreides", "StateSettled", prepareSelectMission<ATREIDES>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:442`

Связь: `scenes.tsv`, регистрация: PORT/select-mission-harkonnen.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '442p'
    scene("select-mission-harkonnen", "select-mission", "harkonnen", "StateSettled", prepareSelectMission<HARKONNEN>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:443`

Связь: `scenes.tsv`, регистрация: PORT/select-mission-ordos.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '443p'
    scene("select-mission-ordos", "select-mission", "ordos", "StateSettled", prepareSelectMission<ORDOS>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:444`

Связь: `scenes.tsv`, регистрация: PORT/select-mission-sardaukar.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '444p'
    scene("select-mission-sardaukar", "select-mission", "sardaukar", "StateSettled", prepareSelectMission<SARDAUKAR>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:445`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-atreides-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '445p'
    scene("tellhouse-atreides-speak", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, false>, readyMentatFrozen<false>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:446`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-atreides-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '446p'
    scene("tellhouse-atreides-await", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, true>, readyMentatFrozen<true>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:447`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-harkonnen-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '447p'
    scene("tellhouse-harkonnen-speak", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, false>, readyMentatFrozen<false>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:448`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-harkonnen-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '448p'
    scene("tellhouse-harkonnen-await", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, true>, readyMentatFrozen<true>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:449`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-ordos-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '449p'
    scene("tellhouse-ordos-speak", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, false>, readyMentatFrozen<false>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:450`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-ordos-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '450p'
    scene("tellhouse-ordos-await", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, true>, readyMentatFrozen<true>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:451`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-sardaukar-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '451p'
    scene("tellhouse-sardaukar-speak", "tellhouse", "sardaukar", "MentatFrozen", prepareTellHouse<SARDAUKAR, false>, readyMentatFrozen<false>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:452`

Связь: `scenes.tsv`, регистрация: PORT/tellhouse-sardaukar-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '452p'
    scene("tellhouse-sardaukar-await", "tellhouse", "sardaukar", "MentatFrozen", prepareTellHouse<SARDAUKAR, true>, readyMentatFrozen<true>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:453`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-atreides-speak; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-atreides-speak; `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '453p'
    withScreen(scene("mentat-briefing-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:454`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-atreides-await; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-atreides-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '454p'
    withScreen(scene("mentat-briefing-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:455`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-atreides-speak; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-atreides-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '455p'
    withScreen(scene("mentat-win-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:456`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-atreides-await; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-atreides-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '456p'
    withScreen(scene("mentat-win-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:457`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-atreides-speak; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-atreides-speak; `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '457p'
    withScreen(scene("mentat-lose-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:458`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-atreides-await; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-atreides-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '458p'
    withScreen(scene("mentat-lose-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "AtreidesMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:459`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-harkonnen-speak; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-harkonnen-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '459p'
    withScreen(scene("mentat-briefing-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:460`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-harkonnen-await; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-harkonnen-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '460p'
    withScreen(scene("mentat-briefing-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:461`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-harkonnen-speak; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-harkonnen-speak; `screens.tsv`, экран: ментат.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '461p'
    withScreen(scene("mentat-win-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:462`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-harkonnen-await; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-harkonnen-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '462p'
    withScreen(scene("mentat-win-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:463`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-harkonnen-speak; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-harkonnen-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '463p'
    withScreen(scene("mentat-lose-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:464`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-harkonnen-await; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-harkonnen-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '464p'
    withScreen(scene("mentat-lose-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "HarkonnenMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:465`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-ordos-speak; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-ordos-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '465p'
    withScreen(scene("mentat-briefing-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:466`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-ordos-await; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-ordos-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '466p'
    withScreen(scene("mentat-briefing-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:467`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-ordos-speak; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-ordos-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '467p'
    withScreen(scene("mentat-win-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:468`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-ordos-await; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-ordos-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '468p'
    withScreen(scene("mentat-win-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:469`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-ordos-speak; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-ordos-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '469p'
    withScreen(scene("mentat-lose-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:470`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-ordos-await; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-ordos-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '470p'
    withScreen(scene("mentat-lose-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "OrdosMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:471`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-sardaukar-speak; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-sardaukar-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '471p'
    withScreen(scene("mentat-briefing-sardaukar-speak", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "SardaukarMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:472`

Связь: `scenes.tsv`, регистрация: PORT/mentat-briefing-sardaukar-await; `scenes.tsv`, состояние `GAME_BRIEFING` для: PORT/mentat-briefing-sardaukar-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '472p'
    withScreen(scene("mentat-briefing-sardaukar-await", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "SardaukarMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:473`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-sardaukar-speak; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-sardaukar-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '473p'
    withScreen(scene("mentat-win-sardaukar-speak", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "SardaukarMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:474`

Связь: `scenes.tsv`, регистрация: PORT/mentat-win-sardaukar-await; `scenes.tsv`, состояние `GAME_WINBRIEF` для: PORT/mentat-win-sardaukar-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '474p'
    withScreen(scene("mentat-win-sardaukar-await", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "SardaukarMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:475`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-sardaukar-speak; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-sardaukar-speak.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '475p'
    withScreen(scene("mentat-lose-sardaukar-speak", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "SardaukarMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:476`

Связь: `scenes.tsv`, регистрация: PORT/mentat-lose-sardaukar-await; `scenes.tsv`, состояние `GAME_LOSEBRIEF` для: PORT/mentat-lose-sardaukar-await.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '476p'
    withScreen(scene("mentat-lose-sardaukar-await", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "SardaukarMentat"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:477`

Связь: `scenes.tsv`, регистрация: PORT/skirmish-setup-random.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '477p'
    scene("skirmish-setup-random", "skirmish-setup", "", "FixedFrames(2, no readiness flag)", prepareSkirmishSetup<0>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:478`

Связь: `scenes.tsv`, регистрация: PORT/skirmish-setup-ready-map.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '478p'
    scene("skirmish-setup-ready-map", "skirmish-setup", "", "FixedFrames(2, no readiness flag)", prepareSkirmishSetup<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:479`

Связь: `scenes.tsv`, регистрация: PORT/options-menu-main.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '479p'
    scene("options-menu-main", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<0>, readyOptionsMenu<0>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:480`

Связь: `scenes.tsv`, регистрация: PORT/options-menu-applied.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '480p'
    scene("options-menu-applied", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<1>, readyOptionsMenu<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:481`

Связь: `scenes.tsv`, регистрация: PORT/credits-title.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '481p'
    scene("credits-title", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<0>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:482`

Связь: `scenes.tsv`, регистрация: PORT/credits-1.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '482p'
    scene("credits-1", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:483`

Связь: `scenes.tsv`, регистрация: PORT/credits-2.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '483p'
    scene("credits-2", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<2>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:484`

Связь: `scenes.tsv`, регистрация: PORT/credits-3.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '484p'
    scene("credits-3", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<3>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:485`

Связь: `scenes.tsv`, регистрация: PORT/credits-4.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '485p'
    hdOnly(scene("credits-4", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<4>)),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:486`

Связь: `scenes.tsv`, регистрация: PORT/credits-5.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '486p'
    hdOnly(scene("credits-5", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<5>)),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:487`

Связь: `scenes.tsv`, регистрация: PORT/outcome-win.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '487p'
    withScreen(scene("outcome-win", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<true>,
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:488`

Связь: `scenes.tsv`, состояние `GAME_WINNING` для: PORT/outcome-win.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '488p'
                     readyOutcome<true>), "GAME_WINNING", "cWinLoseState"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:489`

Связь: `scenes.tsv`, регистрация: PORT/outcome-lose.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '489p'
    withScreen(scene("outcome-lose", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<false>,
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:490`

Связь: `scenes.tsv`, состояние `GAME_LOSING` для: PORT/outcome-lose.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '490p'
                     readyOutcome<false>), "GAME_LOSING", "cWinLoseState"),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:491`

Связь: `scenes.tsv`, регистрация: PORT/scoring.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '491p'
    scene("scoring", "scoring", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<true>, readyScoring),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:492`

Связь: `scenes.tsv`, регистрация: PORT/editor-new-map.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '492p'
    scene("editor-new-map", "new-map-editor", "", "StateSettled", prepareNewMapEditor),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:493`

Связь: `scenes.tsv`, регистрация: PORT/editor-topology.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '493p'
    scene("editor-topology", "editor", "", "StateSettled", prepareEditor<0>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:494`

Связь: `scenes.tsv`, регистрация: PORT/editor-start-cells.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '494p'
    scene("editor-start-cells", "editor", "", "StateSettled", prepareEditor<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:495`

Связь: `scenes.tsv`, регистрация: PORT/editor-symmetry.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '495p'
    scene("editor-symmetry", "editor", "", "StateSettled", prepareEditor<2>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:496`

Связь: `scenes.tsv`, регистрация: PORT/options-game-main-nosaves.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '496p'
    scene("options-game-main-nosaves", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsMenu<0>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:497`

Связь: `scenes.tsv`, регистрация: PORT/save-dialog-menu.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '497p'
    scene("save-dialog-menu", "save-dialog-menu", "", "FixedFrames(10, no readiness flag)", prepareMenuWithSaves,
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:499`

Связь: `scenes.tsv`, регистрация: PORT/options-game-main-saves.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '499p'
    scene("options-game-main-saves", "options-game", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:501`

Связь: `scenes.tsv`, регистрация: PORT/save-dialog-load.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '501p'
    scene("save-dialog-load", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptionsWithSaves,
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:503`

Связь: `scenes.tsv`, регистрация: PORT/save-dialog-save-new.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '503p'
    scene("save-dialog-save-new", "save-dialog", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:505`

Связь: `scenes.tsv`, регистрация: PORT/save-dialog-overwrite.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '505p'
    scene("save-dialog-overwrite", "save-dialog", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:507`

Связь: `scenes.tsv`, регистрация: PORT/save-dialog-load-error.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '507p'
    scene("save-dialog-load-error", "save-dialog", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:509`

Связь: `scenes.tsv`, регистрация: PORT/save-dialog-save-error.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '509p'
    scene("save-dialog-save-error", "save-dialog", "", "FixedFrames(14, no readiness flag)",
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:511`

Связь: `scenes.tsv`, регистрация: PORT/save-roundtrip; `screens.tsv`, экран: схватка с боковой панелью.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '511p'
    onGameScreen(scene("save-roundtrip", "game-playing", "", kFixedGameFrames, prepareSaveRoundTrip), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:512`

Связь: `scenes.tsv`, регистрация: PORT/options-game-applied.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '512p'
    scene("options-game-applied", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsMenu<1>),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:513`

Связь: `scenes.tsv`, регистрация: PORT/structure-label-top.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '513p'
    onGameScreen(scene("structure-label-top", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<0>,
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:515`

Связь: `scenes.tsv`, регистрация: PORT/structure-label-right.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '515p'
    onGameScreen(scene("structure-label-right", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<1>,
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:517`

Связь: `scenes.tsv`, регистрация: PORT/units-label-trike.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '517p'
    onGameScreen(scene("units-label-trike", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TRIKE>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:518`

Связь: `scenes.tsv`, регистрация: PORT/units-label-raider.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '518p'
    onGameScreen(scene("units-label-raider", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<RAIDER>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:519`

Связь: `scenes.tsv`, регистрация: PORT/units-label-quad.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '519p'
    onGameScreen(scene("units-label-quad", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<QUAD>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:520`

Связь: `scenes.tsv`, регистрация: PORT/units-label-tank.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '520p'
    onGameScreen(scene("units-label-tank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TANK>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:521`

Связь: `scenes.tsv`, регистрация: PORT/units-label-siegetank.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '521p'
    onGameScreen(scene("units-label-siegetank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SIEGETANK>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:522`

Связь: `scenes.tsv`, регистрация: PORT/units-label-launcher.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '522p'
    onGameScreen(scene("units-label-launcher", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<LAUNCHER>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:523`

Связь: `scenes.tsv`, регистрация: PORT/units-label-deviator.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '523p'
    onGameScreen(scene("units-label-deviator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVIATOR>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:524`

Связь: `scenes.tsv`, регистрация: PORT/units-label-sonictank.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '524p'
    onGameScreen(scene("units-label-sonictank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SONICTANK>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:525`

Связь: `scenes.tsv`, регистрация: PORT/units-label-devastator.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '525p'
    onGameScreen(scene("units-label-devastator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVASTATOR>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:526`

Связь: `scenes.tsv`, регистрация: PORT/units-label-harvester.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '526p'
    onGameScreen(scene("units-label-harvester", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<HARVESTER>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:527`

Связь: `scenes.tsv`, регистрация: PORT/units-label-mcv.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '527p'
    onGameScreen(scene("units-label-mcv", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<MCV>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:528`

Связь: `scenes.tsv`, регистрация: PORT/units-label-soldier.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '528p'
    onGameScreen(scene("units-label-soldier", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SOLDIER>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:529`

Связь: `scenes.tsv`, регистрация: PORT/units-label-infantry.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '529p'
    onGameScreen(scene("units-label-infantry", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<INFANTRY>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:530`

Связь: `scenes.tsv`, регистрация: PORT/units-label-trooper.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '530p'
    onGameScreen(scene("units-label-trooper", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPER>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:531`

Связь: `scenes.tsv`, регистрация: PORT/units-label-troopers.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '531p'
    onGameScreen(scene("units-label-troopers", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPERS>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:532`

Связь: `scenes.tsv`, регистрация: PORT/units-label-unit-fremen-one.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '532p'
    onGameScreen(scene("units-label-unit-fremen-one", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_ONE>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:533`

Связь: `scenes.tsv`, регистрация: PORT/units-label-unit-fremen-three.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '533p'
    onGameScreen(scene("units-label-unit-fremen-three", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_THREE>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:534`

Связь: `scenes.tsv`, регистрация: PORT/units-label-saboteur.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '534p'
    onGameScreen(scene("units-label-saboteur", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SABOTEUR>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:535`

Связь: `scenes.tsv`, регистрация: PORT/game-hud.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '535p'
    withHud(onGameScreen(scene("game-hud", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Hud>), false)),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:536`

Связь: `scenes.tsv`, регистрация: PORT/game-music.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '536p'
    onGameScreen(scene("game-music", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Music>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:537`

Связь: `scenes.tsv`, регистрация: PORT/game-structure-selected.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '537p'
    onGameScreen(scene("game-structure-selected", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Structure>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:538`

Связь: `scenes.tsv`, регистрация: PORT/game-list-build.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '538p'
    onGameScreen(scene("game-list-build", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListBuild>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:539`

Связь: `scenes.tsv`, регистрация: PORT/game-list-infantry.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '539p'
    onGameScreen(scene("game-list-infantry", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListInfantry>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:540`

Связь: `scenes.tsv`, регистрация: PORT/game-list-vehicles.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '540p'
    onGameScreen(scene("game-list-vehicles", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListVehicles>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:541`

Связь: `scenes.tsv`, регистрация: PORT/game-list-starport.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '541p'
    onGameScreen(scene("game-list-starport", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListStarport>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:542`

Связь: `scenes.tsv`, регистрация: PORT/game-list-palace.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '542p'
    onGameScreen(scene("game-list-palace", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListPalace>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:543`

Связь: `scenes.tsv`, регистрация: PORT/game-list-upgrades.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '543p'
    onGameScreen(scene("game-list-upgrades", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListUpgrades>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:544`

Связь: `scenes.tsv`, регистрация: PORT/game-radar-none.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '544p'
    onGameScreen(scene("game-radar-none", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RadarNone>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:545`

Связь: `scenes.tsv`, регистрация: PORT/game-radar-nopower.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '545p'
    onGameScreen(scene("game-radar-nopower", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RadarNoPower>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:546`

Связь: `scenes.tsv`, регистрация: PORT/game-place-allowed.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '546p'
    onGameScreen(scene("game-place-allowed", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::PlaceAllowed>), true),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:547`

Связь: `scenes.tsv`, регистрация: PORT/game-place-forbidden.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '547p'
    onGameScreen(scene("game-place-forbidden", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::PlaceForbidden>), true),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:548`

Связь: `scenes.tsv`, регистрация: PORT/game-group-select.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '548p'
    onGameScreen(scene("game-group-select", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::GroupSelect>), true),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:549`

Связь: `scenes.tsv`, регистрация: PORT/game-messages.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '549p'
    onGameScreen(scene("game-messages", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Messages>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:550`

Связь: `scenes.tsv`, регистрация: PORT/game-item-hover.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '550p'
    onGameScreen(scene("game-item-hover", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ItemHover>), true),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:551`

Связь: `scenes.tsv`, регистрация: PORT/game-list-scroll-end.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '551p'
    hdOnly(onGameScreen(scene("game-list-scroll-end", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ScrollEnd>), false)),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:552`

Связь: `scenes.tsv`, регистрация: PORT/game-rally-point.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '552p'
    onGameScreen(scene("game-rally-point", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Rally>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:553`

Связь: `scenes.tsv`, регистрация: PORT/game-command-damaged-unit.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '553p'
    onGameScreen(scene("game-command-damaged-unit", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::DamagedUnit>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:554`

Связь: `scenes.tsv`, регистрация: PORT/game-command-harvester.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '554p'
    onGameScreen(scene("game-command-harvester", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Harvester>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:555`

Связь: `scenes.tsv`, регистрация: PORT/game-command-mcv.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '555p'
    onGameScreen(scene("game-command-mcv", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Mcv>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:556`

Связь: `scenes.tsv`, регистрация: PORT/game-harkonnen-list-build.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '556p'
    onGameScreen(scene("game-harkonnen-list-build", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListBuild>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:557`

Связь: `scenes.tsv`, регистрация: PORT/game-harkonnen-list-infantry.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '557p'
    onGameScreen(scene("game-harkonnen-list-infantry", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListInfantry>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:558`

Связь: `scenes.tsv`, регистрация: PORT/game-harkonnen-list-vehicles.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '558p'
    onGameScreen(scene("game-harkonnen-list-vehicles", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListVehicles>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:559`

Связь: `scenes.tsv`, регистрация: PORT/game-harkonnen-list-starport.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '559p'
    onGameScreen(scene("game-harkonnen-list-starport", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListStarport>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:560`

Связь: `scenes.tsv`, регистрация: PORT/game-harkonnen-list-palace.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '560p'
    onGameScreen(scene("game-harkonnen-list-palace", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListPalace>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:561`

Связь: `scenes.tsv`, регистрация: PORT/game-harkonnen-list-upgrades.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '561p'
    onGameScreen(scene("game-harkonnen-list-upgrades", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListUpgrades>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:562`

Связь: `scenes.tsv`, регистрация: PORT/game-ordos-list-build.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '562p'
    onGameScreen(scene("game-ordos-list-build", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListBuild>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:563`

Связь: `scenes.tsv`, регистрация: PORT/game-ordos-list-infantry.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '563p'
    onGameScreen(scene("game-ordos-list-infantry", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListInfantry>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:564`

Связь: `scenes.tsv`, регистрация: PORT/game-ordos-list-vehicles.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '564p'
    onGameScreen(scene("game-ordos-list-vehicles", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListVehicles>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:565`

Связь: `scenes.tsv`, регистрация: PORT/game-ordos-list-starport.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '565p'
    onGameScreen(scene("game-ordos-list-starport", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListStarport>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:566`

Связь: `scenes.tsv`, регистрация: PORT/game-ordos-list-palace.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '566p'
    onGameScreen(scene("game-ordos-list-palace", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListPalace>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:567`

Связь: `scenes.tsv`, регистрация: PORT/game-ordos-list-upgrades.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '567p'
    onGameScreen(scene("game-ordos-list-upgrades", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListUpgrades>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:568`

Связь: `scenes.tsv`, регистрация: PORT/game-sardaukar-list-build.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '568p'
    onGameScreen(scene("game-sardaukar-list-build", "game-playing", "sardaukar", kFixedGameFrames, prepareGame<SARDAUKAR, uiaudit::ListBuild>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:569`

Связь: `scenes.tsv`, регистрация: PORT/game-sardaukar-list-infantry.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '569p'
    onGameScreen(scene("game-sardaukar-list-infantry", "game-playing", "sardaukar", kFixedGameFrames, prepareGame<SARDAUKAR, uiaudit::ListInfantry>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:570`

Связь: `scenes.tsv`, регистрация: PORT/game-sardaukar-list-vehicles.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '570p'
    onGameScreen(scene("game-sardaukar-list-vehicles", "game-playing", "sardaukar", kFixedGameFrames, prepareGame<SARDAUKAR, uiaudit::ListVehicles>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:571`

Связь: `scenes.tsv`, регистрация: PORT/game-sardaukar-list-starport.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '571p'
    onGameScreen(scene("game-sardaukar-list-starport", "game-playing", "sardaukar", kFixedGameFrames, prepareGame<SARDAUKAR, uiaudit::ListStarport>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:572`

Связь: `scenes.tsv`, регистрация: PORT/game-sardaukar-list-palace.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '572p'
    onGameScreen(scene("game-sardaukar-list-palace", "game-playing", "sardaukar", kFixedGameFrames, prepareGame<SARDAUKAR, uiaudit::ListPalace>), false),
```

#### `src/debug/UiAuditScenes.cpp@010a6eb:573`

Связь: `scenes.tsv`, регистрация: PORT/game-sardaukar-list-upgrades.

```text
git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '573p'
    onGameScreen(scene("game-sardaukar-list-upgrades", "game-playing", "sardaukar", kFixedGameFrames, prepareGame<SARDAUKAR, uiaudit::ListUpgrades>), false),
```

### Не проверено

Сборка, CTest, игра и скрипты режима отладки не запускались; файлы снимков в игре не создавались и визуально не оценивались. Сеть не использовалась. Из таблиц пунктов 1–4 помощник 3 сверил восемь строк: все восемь совпали с выводом `git show`; остальные строки отдельно этой выборочной сверкой не проверялись.
