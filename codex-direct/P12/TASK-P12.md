# Задание P12 — упаковка релиза, workflows, авторское приветствие и галерея (шаг П12)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p12`, ветка `codex/p12`, `HEAD` — `0d186e8b1894d37091b31c362cecffa95ffadb4e` (вершина ветки порта `port/up-d06f2fcd` после слияния П8а; шаг П10в сливается в ветку порта параллельно, его файлов этот шаг не трогает). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p12/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p12/` (дальше — «папка задания»).

## Цель

Выпуск порта собирается и публикуется так же, как выпуск форка: по тегу `v*` workflow `release.yml` собирает Windows, Linux и macOS на SDL3, пакует общий архив данных `common-assets` и три платформенных архива и публикует выпуск. Общий архив содержит всё, что порт открывает при запуске, и не содержит классических паков. Файла `.github/workflows/claude-code-review.yml` нет. Авторское приветствие и галерея снимков форка стоят в начале `README.md`. Готово, когда скрипт проверки `check_p12.py` печатает `CHECKS 17 OK`, сухой прогон упаковки на собранной Linux-сборке даёт ожидаемый список файлов, Linux-архив запускает игру через `d2tm.sh` со своими библиотеками SDL3, а сборка со всеми тестами зелёная. Код игры, `CMakeLists.txt` и `src/main.cpp` шаг не меняет.

## Что уже решено

Ревизия `B` = `0d186e8b1894d37091b31c362cecffa95ffadb4e`; рабочая копия шага — `B` плюс файлы П10в, которые файлов упаковки, `.github`, `README*` и `docs/screenshots` не трогают. Ревизия форка `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`. Все факты о порте ниже — о файлах `B`.

- **Объём** — две функции карты (`release-packaging`, `author-gallery`) и удаление `.github/workflows/claude-code-review.yml` (Р82: владелец, 2026-11-12, «Удалить файл в П12»; секрет `CLAUDE_CODE_OAUTH_TOKEN` не заводится).
- **Workflows порта.** В `B` четыре файла: `build_manual.yml`, `build_master.yml`, `build_pr.yml`, `claude-code-review.yml`; все четыре совпадают с апстримом `d06f2fcd` (`git diff --stat d06f2fcd2a347182c3774fb96e9a85570405c489 0d186e8b1894d37091b31c362cecffa95ffadb4e -- .github` — пусто). После удаления четвёртого остаются три; шаг их не меняет. Строки, без которых workflow выпуска форка не встанет на сборку порта, лежат в новом `release.yml` (пункт 3 контракта), а не в этих трёх.
- **Сборка порта** (из `build_pr.yml@B`): Windows — MSYS2 MINGW64, пакеты `mingw-w64-x86_64-toolchain mingw-w64-x86_64-gcc mingw-w64-x86_64-sdl3 mingw-w64-x86_64-sdl3-mixer mingw-w64-x86_64-sdl3-image mingw-w64-x86_64-sdl3-ttf mingw64/mingw-w64-x86_64-cmake mingw-w64-x86_64-catch`, действие `al-cheb/configure-pagefile-action@v1.5` (16GB, `C:`), генератор `MinGW Makefiles`, `cmake --build . -j2`, `ctest --output-on-failure`; Linux — `egor-tensin/setup-gcc@v1` (версия 14, `x64`), затем `./install_dependencies_ubuntu.sh` (SDL3 собирается из исходников: `install_dependencies_ubuntu.sh@B:5`), `cmake`, `make -j4`, `ctest`; macOS — `./install_dependencies_macosx.sh` (`brew install --quiet cmake ninja pkg-config sdl3 sdl3_ttf sdl3_image sdl3_mixer catch2`, `install_dependencies_macosx.sh@B:14`), раннеры `macos-15` (arm64) и `macos-15-intel` (Intel), `cmake`, `make -j4`, `ctest`. Во всех `actions/checkout@v6`, CI без LFS.
- **Workflow выпуска форка** — `FORK1:.github/workflows/release.yml` (341 строка): задания `prepare-release`, `common-assets`, `windows`, `linux`, `macos` (матрица `arm64` и `x64`), `publish-release`; триггеры — push тегов `v*` и `workflow_dispatch` с обязательным `inputs.tag`; имя и номер выпуска берутся из тега (`RELEASE_TAG`); выпуск создаётся черновиком, архивы грузятся `gh release upload --clobber`, публикуется `gh release edit --draft=false --latest` после всех заданий. Эта логика переносится без изменений.
- **Что порт открывает при запуске** (всё относительно каталога игры; рабочий каталог — каталог исполняемого файла, `src/main.cpp:61-68`, Р78):
  - `settings.ini` — `src/game/cGame_logic.cpp:739`, `src/main.cpp:105`; `game.ini` — `src/utils/InitialGameSettings.hpp:47` (в пакете копия `resources/game.ini.org`);
  - проверка файлов настроек `cGame_logic.cpp:749-763` (папка `GameDir=data`): шрифты `PTSansNarrow-Regular.ttf`, `RussoOne-Regular.ttf` и пакеты `sdl_data_hd4.dat`, `sdl_inter_hd4.dat`, `sdl_world_hd4.dat`, `sdl_mentat_hd4.dat`, `sdl_audio.dat`, `sdl_gfxeditor.dat` (значения — `resources/bin/settings.ini`, секции `[DATAFILE]` и `[FONT]`); пакет без любого из них — игра не запускается (`cGame_logic.cpp:766-767`);
  - запасной шрифт `data/PTMono-Regular.ttf` — `src/context/ContextCreator.cpp:102`;
  - сцены ментатов `data/scenes/hd4/sdl_<имя>.dat` — `src/utils/Graphics.hpp:66-69`; в `resources/bin/data/scenes/hd4/` 18 файлов: `harvest headqrts hitcftry hvyftry ix liteftry lose01 lose02 ltank palace platr plhar plord quad repair sardukar win01 win02`;
  - 14 картинок `data/hd4/*.png` — `src/utils/HdUiTextureLoader.cpp:13`: `campaign_map command_bar command_bar_disabled credits_team credits_title hud_house_atreides hud_house_harkonnen hud_house_ordos main_menu_background main_menu_logo outcome_defeat_en outcome_defeat_ru outcome_victory_en outcome_victory_ru`;
  - музыка — папки `music/gameplay`, `music/menu`, `music/conquest`, `music/briefing/atreides`, `music/briefing/harkonnen`, `music/briefing/ordos`, `music/victory`, `music/defeat` (`src/context/AudioContext.cpp:61-70`); всего 22 файла `.wav` (Р79);
  - кампании: `campaign` для английского и `campaign_ru` для русского (`src/utils/IniParsing.cpp:646-649`), в каждой `<дом>/mission1.ini … mission8.ini` для `atreides`, `harkonnen`, `ordos`, `sardaukar` (`src/utils/ini.cpp:83`) и `briefings/mentata.ini`, `mentath.ini`, `mentato.ini`, `mentats.ini` (`ini.cpp:358`); карты — `campaign/maps/scen*.ini` (`src/utils/cIniUtils.cpp:246`);
  - стычка — папка `skirmish` (`src/gameobjects/map/cPreviewMaps.cpp:303`);
  - сохранения — папка `saves` рядом с игрой, игра создаёт её сама (`src/save/SaveGameManager.cpp:69,133`; Р78); в пакет она не входит;
  - классические паки `sdl_data.dat`, `sdl_inter.dat`, `sdl_world.dat`, `sdl_mentat.dat`, классические сцены `data/scenes/sdl_*.dat`, `new.dat`, `windtrap.dat` порт не открывает: `git grep -n '\.dat"' B -- src` даёт одну строку кода, `Graphics.hpp:68`, остальные — закомментированные строки `cFileValidator.cpp:29-33` (Р34).
- **Состав пакета** — как у `common-assets` форка: копия `resources/bin/` без `d2tm.exe` и без классических файлов, плюс `game.ini` из `resources/game.ini.org`. Папки `music`, `campaign_ru`, файл `sdl_gfxeditor.dat` и файлы шрифтов лежат в `resources/bin/` в `B` и попадают в пакет самой копией. Сценарий `create_release.sh` форка (`FORK1:create_release.sh`) `sdl_gfxeditor.dat`, `music` и `campaign_ru` не копировал; шаг этот сценарий не использует и не меняет.
- **Приветствие и галерея** — переносятся как есть: начало `FORK1:README.md` (строки 1–37) и 5 PNG из `docs/screenshots` (в `B` их нет). Абзац о шрифтах заменён (пункт 11 контракта): шрифт Sangyo из `FORK1:README.md:38-40` порт не использует.
- **Файлы, которые шаг не меняет:** `CMakeLists.txt` и `src/main.cpp` (в разности `BASE`—`FORK1` у них нет правок упаковки: у `CMakeLists.txt` одна строка `find_package(Python3 REQUIRED COMPONENTS Interpreter)` — это тесты режима отладки, не упаковка; у `src/main.cpp` совпадений нет), `create_release.sh`, `create_release.bat`, `.gitattributes` (в `.gitattributes@B` нет правила на `docs/screenshots/*.png`, снимки — обычные блобы), `build_manual.yml`, `build_master.yml`, `build_pr.yml`, любой `.cpp`, `.hpp`, `.h` и тест, `README_AI.md`, `resources/bin/README_RU.txt`, `resources/bin/data/licenses/` (их в `B` нет и они не переносятся; `THIRD_PARTY_ASSETS_RU.txt` переносится, пункт 13).
- **Ответы ведущего** (2026-11-12; полный текст — в конце `QUESTIONS-P12.md`): Q-P12-01 — Linux-архив несёт свои библиотеки SDL3 в папке `lib/` и скрипт запуска `d2tm.sh`, `patchelf` не используется (пункты 3, E5a, и 7); Q-P12-02 (Р83) — снимки и галерея как есть, новые снимки и правка `README.md` — на шаге П13 (пункт 12); Q-P12-03 — абзац о шрифтах по пункту 11, `README_AI.md` не переносится; Q-P12-04 (Р83) — `THIRD_PARTY_ASSETS_RU.txt` переносится с правками (пункт 13), `README_RU.txt` не переносится; Q-P12-05 — `create_release.sh` и `.bat` не меняются; Q-P12-06 — текст `RELEASE_NOTES.md` по пункту 8; Q-P12-07 — DLL Windows как у форка (пункт 3, шаг `Package Windows binary and DLLs`).

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом:

- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:.github/workflows/release.yml | cat -n`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/RELEASE_NOTES.md`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/LINUX_README.txt`, затем `MACOS_README.txt` и `WINDOWS_README.txt` той же папки (три вызова);
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:README.md | sed -n '1,45p'`;
- `.github/workflows/build_pr.yml` целиком;
- `install_dependencies_ubuntu.sh` и `install_dependencies_macosx.sh` целиком (два вызова);
- `resources/bin/settings.ini` строки 1–100;
- `src/context/AudioContext.cpp` строки 55–75;
- вывод `git ls-files resources/bin | grep -v -E '^resources/bin/(campaign|campaign_ru|skirmish|music)/' | head -80`.

Пути без `/srv/` — от корня рабочей копии. Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт

В блоках кода внутри пунктов списка первые пять пробелов каждой строки — отступ списка Markdown; в файлы они не переносятся. Остальные пробелы переносятся.

1. **Удаление workflow.** Файл `.github/workflows/claude-code-review.yml` удаляется командой `rm .github/workflows/claude-code-review.yml` (без `-f`). После удаления `git grep --untracked -n -i -E 'claude-code-review|CLAUDE_CODE_OAUTH|claude-review' -- .github README.md packaging create_release.sh create_release.bat CMakeLists.txt` — ноль строк (на `B` в этих путях три строки, все в удаляемом файле).
2. **Три workflow апстрима** (`build_manual.yml`, `build_master.yml`, `build_pr.yml`) не меняются: `git diff --stat -- .github/workflows/build_manual.yml .github/workflows/build_master.yml .github/workflows/build_pr.yml` — пустой вывод.
3. **`.github/workflows/release.yml` (новый файл).** Копия файла форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:.github/workflows/release.yml > .github/workflows/release.yml`. Затем правки E6, E5, E5a, E4, E3, E2, E1, E0 и замена версии действия. Номера строк — номера строк копии до правок; применяй правки снизу вверх в порядке, в котором они перечислены (E6 первой, E0 последней), тогда номера не сдвигаются.
   - **E6, macOS, строки 293–298** (от `          cmake -S . -B build -G Ninja \` до `          ctest --test-dir build --output-on-failure`) заменяются тремя строками (отступ — 10 пробелов):
     ```
          cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
          cmake --build build --parallel 4
          ctest --test-dir build --output-on-failure
     ```
   - **E5, macOS, строка 286** `          brew install cmake ninja pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer` заменяется строкой `          ./install_dependencies_macosx.sh`.
   - **E4, Linux, строки 236–241** (от `          cmake -S . -B build -G Ninja \` до `          SDL_VIDEODRIVER=dummy ctest --test-dir build --output-on-failure`) заменяются тремя строками (отступ — 10 пробелов):
     ```
               cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
               cmake --build build --parallel 4
               ctest --test-dir build --output-on-failure
     ```
   - **E5a, Linux, строки 249–250** (`          cp build/d2tm package/` и `          chmod +x package/d2tm`) заменяются восемью строками (отступ — 10 пробелов, у строки `cp -a` — 12):
     ```
               cp build/d2tm package/
               cp packaging/d2tm.sh package/
               chmod 755 package/d2tm package/d2tm.sh
               mkdir package/lib
               ldd build/d2tm | awk '$2 == "=>" && $3 ~ /^\/usr\/local\/lib\/libSDL3/ { print $3 }' | sort -u | while read -r lib; do
                 cp -a "${lib%%.so*}".so* package/lib/
               done
               test -n "$(ls package/lib)"
     ```
     Строка 251 `cp packaging/LINUX_README.txt package/INSTALL.txt` и строки 252–253 (`tar`, `test -s`) остаются.
   - **E3, Linux.** Строки 226–229 (от `          sudo apt-get update` до `            libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev`) заменяются двумя строками (отступ — 10 пробелов):
     ```
               chmod +x install_dependencies_ubuntu.sh
               ./install_dependencies_ubuntu.sh
     ```
     Затем сразу перед строкой 217 (`      - uses: actions/checkout@v4`, первый шаг задания `linux`) вставляется шаг и одна пустая строка после него (отступ `- name` — 6 пробелов):
     ```
           - name: Set up GCC
             uses: egor-tensin/setup-gcc@v1
             with:
               version: 14
               platform: x64

     ```
   - **E2, Windows, строки 179–180** (`          cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release` и `          cmake --build build --parallel 3`) заменяются двумя строками (отступ — 10 пробелов):
     ```
               cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
               cmake --build build -j2
     ```
     Строка 181 `          ctest --test-dir build --output-on-failure` остаётся.
   - **E1, Windows.** Строки 159–167 (от `          install: >-` до `            mingw-w64-x86_64-SDL2_mixer`) заменяются блоком (отступ `install:` — 10 пробелов, значений — 12):
     ```
               install: >-
                 git zip
                 mingw-w64-x86_64-toolchain
                 mingw-w64-x86_64-gcc
                 mingw-w64-x86_64-sdl3
                 mingw-w64-x86_64-sdl3-mixer
                 mingw-w64-x86_64-sdl3-image
                 mingw-w64-x86_64-sdl3-ttf
                 mingw64/mingw-w64-x86_64-cmake
                 mingw-w64-x86_64-catch
     ```
     Затем сразу перед строкой 169 (`      - uses: actions/checkout@v4`, шаг после `Install MSYS2 toolchain`) вставляется шаг и одна пустая строка после него (отступ `- name` — 6 пробелов):
     ```
           - name: Configure pagefile
             uses: al-cheb/configure-pagefile-action@v1.5
             with:
               minimum-size: 16GB
               maximum-size: 16GB
               disk-root: "C:"

     ```
   - **E0, общий архив, строки 105–130** (от `          mkdir -p package` до `          test -f package/data/sdl_mentat_hd4.dat` включительно) заменяются одной строкой `          bash packaging/make_common_assets.sh package`. Строки 104 (`archive=...`) и 131–135 (распаковка в `zip` и `test -s`) остаются.
   - **Версия действия.** Пять строк `      - uses: actions/checkout@v4` (строки 31, 79, 169, 217, 277 копии до правок) становятся `      - uses: actions/checkout@v6` (версия из `build_pr.yml@B`).
   - Остальные строки файла не меняются: триггеры, `permissions`, `concurrency`, `env`, задания `prepare-release` и `publish-release`, шаги `Fetch packaged LFS files`, `Verify LFS checkout`, `Upload ...`, шаги `Package Windows binary and DLLs`, `Package Linux binary`, `Package macOS binary`, комментарий в строке 85. Шаг `Package Windows binary and DLLs` копирует `resources/dll/*.dll` и DLL из `ldd`, как у форка (Q-P12-07).
4. **`packaging/make_common_assets.sh` (новый файл).** Содержимое — точно:
   ```bash
   #!/bin/bash
   set -euo pipefail

   if [[ $# -ne 1 ]]; then
       echo "Usage: $0 <new package directory>" >&2
       exit 2
   fi
   package=$1
   if [[ -e "$package" ]]; then
       echo "Package directory already exists: $package" >&2
       exit 1
   fi

   fail() {
       echo "$1" >&2
       exit 1
   }

   mkdir -p "$package"
   cp -a resources/bin/. "$package/"
   rm -f "$package/d2tm.exe"
   cp resources/game.ini.org "$package/game.ini"

   classic_files=(
       data/sdl_data.dat data/sdl_inter.dat data/sdl_world.dat data/sdl_mentat.dat
       data/scenes/new.dat data/scenes/windtrap.dat
   )
   for classic in "${classic_files[@]}"; do
       rm -f "$package/$classic"
   done
   rm -f "$package"/data/scenes/sdl_*.dat

   for classic in "${classic_files[@]}"; do
       [[ ! -e "$package/$classic" ]] || fail "Classic file is in the package: $classic"
   done
   if compgen -G "$package/data/scenes/sdl_*.dat" > /dev/null; then
       fail "Classic scenes are in the package"
   fi
   [[ ! -e "$package/saves" ]] || fail "The saves directory is in the package"

   required=(
       settings.ini game.ini windowed.bat campaign/info.txt
       OFL_PT_FONTS.txt data/OFL_RUSSO_ONE.txt
       data/sdl_audio.dat data/sdl_data_hd4.dat data/sdl_inter_hd4.dat
       data/sdl_world_hd4.dat data/sdl_mentat_hd4.dat data/sdl_gfxeditor.dat
       data/PTSansNarrow-Regular.ttf data/RussoOne-Regular.ttf data/PTMono-Regular.ttf
   )
   for png in campaign_map command_bar command_bar_disabled credits_team credits_title \
       hud_house_atreides hud_house_harkonnen hud_house_ordos main_menu_background main_menu_logo \
       outcome_defeat_en outcome_defeat_ru outcome_victory_en outcome_victory_ru
   do
       required+=("data/hd4/$png.png")
   done
   for scene in harvest headqrts hitcftry hvyftry ix liteftry lose01 lose02 ltank palace \
       platr plhar plord quad repair sardukar win01 win02
   do
       required+=("data/scenes/hd4/sdl_$scene.dat")
   done
   for text_dir in campaign campaign_ru; do
       for mentat in mentata mentath mentato mentats; do
           required+=("$text_dir/briefings/$mentat.ini")
       done
       for house in atreides harkonnen ordos sardaukar; do
           for mission in 1 2 3 4 5 6 7 8; do
               required+=("$text_dir/$house/mission$mission.ini")
           done
       done
   done
   for item in "${required[@]}"; do
       [[ -f "$package/$item" ]] || fail "Missing from the package: $item"
   done

   for music_dir in gameplay menu conquest briefing/atreides briefing/harkonnen briefing/ordos victory defeat; do
       compgen -G "$package/music/$music_dir/*.wav" > /dev/null || fail "No music in music/$music_dir"
   done
   wav_count=$(find "$package/music" -type f -name '*.wav' | wc -l)
   [[ "$wav_count" -eq 22 ]] || fail "Expected 22 music tracks, found $wav_count"
   compgen -G "$package/skirmish/*.ini" > /dev/null || fail "No skirmish maps"
   compgen -G "$package/campaign/maps/scen*.ini" > /dev/null || fail "No campaign maps"
   ```
   Других строк и комментариев в файле нет.
5. **`packaging/WINDOWS_README.txt` (новый файл).** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/WINDOWS_README.txt | sed 's/SDL2/SDL3/g' > packaging/WINDOWS_README.txt`. Единственное отличие от файла форка — строка 8: `The required MinGW and SDL3 DLLs are included in this platform archive.`
6. **`packaging/MACOS_README.txt` (новый файл).** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/MACOS_README.txt | sed -e 's/SDL2/SDL3/g' -e 's/sdl2/sdl3/g' > packaging/MACOS_README.txt`. Отличия от файла форка — две строки: строка 7 `2. Install the SDL3 runtime dependencies:` и строка 9 `   brew install sdl3 sdl3_image sdl3_ttf sdl3_mixer`.
7. **Linux-архив: `packaging/d2tm.sh` и `packaging/LINUX_README.txt` (новые файлы; ответ на Q-P12-01).**
   - `packaging/d2tm.sh` — точно эти три строки (последняя строка заканчивается переводом строки), права файла `755` (`chmod 755 packaging/d2tm.sh`):
     ```
     #!/bin/sh
     HERE="$(cd "$(dirname "$0")" && pwd)"
     LD_LIBRARY_PATH="$HERE/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" exec "$HERE/d2tm" "$@"
     ```
   - `packaging/LINUX_README.txt` — копия файла форка (`git show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/LINUX_README.txt`), у которой строки 7–18 (от `1. Install the SDL2 runtime dependencies. On Debian/Ubuntu:` до `   ./d2tm`) заменены строками блока (блок — окончательный текст замены):
     ```
     1. Download the matching common-assets ZIP from the same GitHub Release.
     2. Extract this archive and common-assets into the same empty directory.
     3. Ensure the launcher and the binary are executable and start the game:

        chmod +x d2tm d2tm.sh
        ./d2tm.sh

     The SDL3 libraries are included in the lib directory of this archive.
     d2tm.sh makes the game use them, so start the game through d2tm.sh.
     ```
     Строки 1–6 и 19–20 файла форка (пустая строка и `Back up settings.ini, music and saves before replacing an older installation.`) не меняются.
   - Linux-архив после шага `Package Linux binary` (правка E5a): `d2tm`, `d2tm.sh`, `INSTALL.txt`, папка `lib/` с файлами `libSDL3*.so*`, `libSDL3_image*.so*`, `libSDL3_ttf*.so*`, `libSDL3_mixer*.so*` со всеми символическими ссылками.
8. **`packaging/RELEASE_NOTES.md` (новый файл).** Содержимое — точно (выбор по умолчанию, Q-P12-06):
   ```markdown
   # DUNE RU/HD cross-platform release

   This release contains the Dune II — The Maker RU/HD remaster for Windows,
   Linux and macOS, built on SDL3.

   ## Installation

   1. Download `DUNE-<version>-common-assets.zip`.
   2. Download exactly one platform archive:
      - `windows-x64.zip` for 64-bit Windows;
      - `linux-x64.tar.gz` for 64-bit Linux;
      - `macos-arm64.tar.gz` for Apple Silicon;
      - `macos-x64.tar.gz` for Intel Macs.
   3. Extract both archives into the same empty directory.
   4. Read `INSTALL.txt` from the platform archive and start `d2tm`/`d2tm.exe`.

   The common archive includes the bilingual campaigns, HD4 graphics, fonts and
   the 22 music tracks in the `music` folder. Existing `settings.ini`, `music`
   and `saves` directories should be backed up before updating an older
   installation. The game creates the `saves` folder next to itself. Saved games
   from releases that predate this SDL3 build are not compatible: the game
   lists them as damaged slots.

   Windows binaries are portable and include their runtime DLLs. Linux targets
   Ubuntu 24.04 or compatible distributions and includes the SDL3 libraries it
   needs, started through `d2tm.sh`. macOS targets macOS 15+, requires SDL3 from
   Homebrew, and is currently unsigned and not notarized.

   Source builds require Git LFS.
   ```
   Раздела `Highlights` в файле нет: его пишет ведущий на шаге «Релиз», вместе с номером выпуска.
9. **`resources/bin/windowed.bat`.** Файл заменяется копией файла форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/windowed.bat > resources/bin/windowed.bat` (три строки: `@echo off`, `cd /d "%~dp0"`, `"%~dp0d2tm.exe" -windowed`).
10. **`.gitignore`.** В конец файла добавляется строка `resources/bin/d2tm.exe` (если последняя строка файла без перевода строки — сначала перевод строки). Других правок нет.
11. **`README.md`.** Новый файл = (а) строки 1–37 файла форка, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:README.md | sed -n '1,37p'` (заголовок `# Dune II — The Maker RU/HD Remaster`, приветствие, раздел `## Screenshots` с пятью ссылками на `docs/screenshots/*.png`, раздел `## Downloads`, пустая строка), затем (б) абзац о шрифтах (строка 38), пустая строка (39), (в) строка `---` (40) и пустая строка (41), затем (г) весь прежний `README.md` (`git show HEAD:README.md`) без единого изменения. Абзац (б) — точно, одной строкой Markdown (выбор по умолчанию, Q-P12-03):
    ```
    The interface text uses **PT Sans Narrow** and **Russo One**, with **PT Mono** as the fallback font. All three are distributed under the SIL Open Font License 1.1; their copyright and license notices are in [`resources/bin/OFL_PT_FONTS.txt`](resources/bin/OFL_PT_FONTS.txt) and [`resources/bin/data/OFL_RUSSO_ONE.txt`](resources/bin/data/OFL_RUSSO_ONE.txt).
    ```
    Строки 38–50 файла форка (абзац о Sangyo, заголовок апстрима и ссылка на `README_AI.md`) в новый файл не входят. Перед записью проверь `grep -c -E 'PT Sans Narrow|PT Mono' resources/bin/OFL_PT_FONTS.txt` и `grep -c 'Russo' resources/bin/data/OFL_RUSSO_ONE.txt` — оба больше `0`.
12. **Снимки.** `docs/screenshots/house-selection.png`, `main-menu.png`, `ordos-briefing.png`, `skirmish-gameplay.png`, `victory-screen.png` уже лежат в рабочей копии (положил ведущий из `FORK1`), их не меняй (Р83: снимки и галерея как есть, новые снимки и правка `README.md` — на шаге П13). Проверка `sha256sum`:
    ```
    aa7203f71b9ba68f00a1e7c346f300ceaf38e4703d59d5bf7d9926afd5669c3f  docs/screenshots/house-selection.png
    fcdf727a425894bfeb54c1d7c88304135a8948d0cf5fdffd91445ac70ea491b8  docs/screenshots/main-menu.png
    20683ebfb5aa9bc18204ea354ff7a02f3cf94c0864814504c5cbbb334820be76  docs/screenshots/ordos-briefing.png
    7f36a31524aae867d956d963c955fd8ce473d6d5e3bc0234a329d114d9ff3ea8  docs/screenshots/skirmish-gameplay.png
    e28fb565718718058cfe2fabb2ea10413158820ae76e4c500da818544e52ef7e  docs/screenshots/victory-screen.png
    ```
    Расхождение — блок `## Q-P12-NN` и стоп. Это обычные блобы Git, не LFS.
13. **`resources/bin/THIRD_PARTY_ASSETS_RU.txt` (новый файл; ответ на Q-P12-04, Р83).** Файл форка с тремя заменами строк и добавленным концом. Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/THIRD_PARTY_ASSETS_RU.txt | sed -e '1s/.*/D2TM, русская HD-сборка — ИСТОЧНИКИ ВИЗУАЛЬНЫХ РЕФЕРЕНСОВ/' -e '4s/.*/Эта сборка — некоммерческая любительская./' -e '43s/.*/Материалы этой сборки не предназначены для продажи,/' > resources/bin/THIRD_PARTY_ASSETS_RU.txt`, затем к файлу дописываются пустая строка и три строки (каждая заканчивается переводом строки):
    ```
    
    PT Sans Narrow и PT Mono
    Шрифты текста интерфейса. Авторы: ParaType.
    Лицензия: SIL Open Font License 1.1 (OFL_PT_FONTS.txt).
    ```
    Строки файла форка, кроме 1, 4 и 43, не меняются (в том числе строка 2 из знаков `=` и абзац `Russo One` в конце). Пакет берёт файл копией `resources/bin`. `resources/bin/README_RU.txt` не переносится.
14. **Ничего сверх контракта.** Других изменений нет: ни правки других workflow, ни `create_release.*`, ни переформатирования, ни новых комментариев в файлах, кроме комментария в строке 85 `release.yml`, который приходит из файла форка.

## Тесты

Новых тестов Catch2 нет: у форка нет тестов упаковки (`git grep -n -i -E 'release|packag' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- tests` даёт только слово `release` в комментариях `tests/FactoryPadEngineTests.cpp` про анимацию завода), число тестов CTest не меняется и остаётся больше 345. `tests/CMakeLists.txt` не меняется. Взамен — одноразовый скрипт проверки `.tmp/p12/check_p12.py` (в репозиторий не коммитится): он берёт факты из файлов рабочей копии, а не из текста контракта. Каждая проверка печатает `C<номер> OK` или `C<номер> FAIL: <причина>` и продолжает; в конце печатает `CHECKS <число OK> OK` и выходит с кодом `0` только если все 17 — OK. Перед запуском `.tmp/p12/dry` удаляется средствами Python (`shutil.rmtree`), не командой `rm`; после записи `.tmp/p12/package-files.txt` папка `.tmp/p12/dry` удаляется так же.

- **C1.** В `.github/workflows/` ровно файлы `build_manual.yml`, `build_master.yml`, `build_pr.yml`, `release.yml`.
- **C2.** `git diff --stat` по трём workflow апстрима (пункт 2) — пустой.
- **C3.** `release.yml` разбирается как YAML (`import yaml`, интерпретатор `/usr/bin/python3`; PyYAML читает ключ `on` как булево `True`, поэтому секция триггеров — `doc.get("on", doc.get(True))`); `on.push.tags == ["v*"]`; `on.workflow_dispatch.inputs.tag.required` истинно; ключи `jobs` — ровно `prepare-release`, `common-assets`, `windows`, `linux`, `macos`, `publish-release`; `publish-release.needs` содержит остальные пять; `jobs.macos.strategy.matrix.include` — ровно `{runner: macos-15, arch: arm64}` и `{runner: macos-15-intel, arch: x64}`; `jobs.linux.runs-on == "ubuntu-24.04"`; `jobs.windows.runs-on == "windows-latest"`. Если модуль `yaml` не импортируется и `actionlint` нет — блок `## Q-P12-NN` и стоп.
- **C4.** Каждое значение `uses:` в `release.yml` встречается среди значений `uses:` файлов `build_pr.yml` и `build_master.yml` рабочей копии.
- **C5.** Значение `install` шага `msys2/setup-msys2@v2` в `release.yml` содержит слова `git`, `zip`, `mingw-w64-x86_64-toolchain`, `mingw-w64-x86_64-gcc`, `mingw-w64-x86_64-sdl3`, `mingw-w64-x86_64-sdl3-mixer`, `mingw-w64-x86_64-sdl3-image`, `mingw-w64-x86_64-sdl3-ttf`, `mingw64/mingw-w64-x86_64-cmake`, `mingw-w64-x86_64-catch`; задание `linux` содержит шаг `./install_dependencies_ubuntu.sh` и `egor-tensin/setup-gcc@v1`; задание `macos` содержит шаг `./install_dependencies_macosx.sh`.
- **C6.** `git grep --untracked -n -i 'sdl2' -- .github/workflows/release.yml packaging README.md` — ноль строк (на `B` в этих путях — ноль).
- **C7.** Имена архивов `DUNE-${RELEASE_TAG}-common-assets.zip`, `DUNE-${RELEASE_TAG}-windows-x64.zip`, `DUNE-${RELEASE_TAG}-linux-x64.tar.gz`, `DUNE-${RELEASE_TAG}-macos-${{ matrix.arch }}.tar.gz` (в шаге Windows для `pwsh` — `DUNE-$env:RELEASE_TAG-windows-x64.zip`) встречаются и в шаге упаковки, и в шаге загрузки своего задания; шаг `Package Windows binary and DLLs` содержит `cp resources/dll/*.dll package/` и `cp packaging/WINDOWS_README.txt package/INSTALL.txt`.
- **C8.** Сухой прогон упаковки платформ. Linux: в `.tmp/p12/dry/linux/` создаются `build/d2tm` (копия `.tmp/out/build/d2tm`) и копия папки `packaging`; `run` шага `Package Linux binary` (из разобранного YAML), в котором подстрока `\/usr\/local\/lib\/libSDL3` заменена на `\/srv\/library\/dune\/deps\/prefix\/lib\/libSDL3`, выполняется командой `bash` в этой папке с `RELEASE_TAG=vdry` и `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib`; в `tar -tzvf DUNE-vdry-linux-x64.tar.gz` есть записи `./`, `./d2tm`, `./d2tm.sh`, `./INSTALL.txt`, `./lib/` и записи `./lib/<имя>`, где каждое имя начинается с `libSDL3`; для каждого из `libSDL3.so`, `libSDL3_image.so`, `libSDL3_ttf.so`, `libSDL3_mixer.so` в `lib/` есть и обычный файл с `.so.` в имени, и символическая ссылка (в первом столбце `tar -tv` — `l`); `d2tm` и `d2tm.sh` — с правами `-rwxr-xr-x`; `INSTALL.txt` в архиве равен `packaging/LINUX_README.txt`, `d2tm.sh` в архиве равен `packaging/d2tm.sh`. macOS: `.tmp/p12/dry/macos/`, `run` шага `Package macOS binary`, в котором строка `${{ matrix.arch }}` заменена на `arm64`, даёт `DUNE-vdry-macos-arm64.tar.gz` с записями `./`, `./d2tm`, `./INSTALL.txt` и `INSTALL.txt` = `packaging/MACOS_README.txt`.
- **C9.** Сухой прогон общего архива: `bash packaging/make_common_assets.sh .tmp/p12/dry/common/package` из корня рабочей копии — код `0`; список файлов пакета (`find ... -type f`, отсортированный, с размерами) пишется в `.tmp/p12/package-files.txt`; число строк списка печатается.
- **C10.** Состав пакета по фактам рабочей копии (независимо от массивов `make_common_assets.sh`): множество файлов пакета равно множеству файлов `resources/bin/` минус `d2tm.exe`, минус `data/sdl_data.dat`, `data/sdl_inter.dat`, `data/sdl_world.dat`, `data/sdl_mentat.dat`, `data/scenes/new.dat`, `data/scenes/windtrap.dat`, минус `data/scenes/sdl_*.dat` (только прямо в `data/scenes`), плюс `game.ini`; в пакете нет путей, начинающихся с `saves/`; число файлов `.wav` в `music/` равно 22.
- **C11.** Всё, что порт открывает, есть в пакете: (а) значения `[DATAFILE]` и `[FONT]` из `settings.ini` пакета — существующие файлы в `data/` пакета, плюс `data/PTMono-Regular.ttf`; (б) каждое имя из `git grep --untracked -h -o -E '"[a-z_0-9]+\.png"' -- src` (без кавычек) — существующий файл в `data/hd4/` пакета; (в) для каждого из `atreides harkonnen ordos sardaukar` и каждого `N` от 1 до 8 существуют `campaign/<дом>/mission<N>.ini` и `campaign_ru/<дом>/mission<N>.ini`; (г) все 18 файлов `data/scenes/hd4/sdl_<имя>.dat` из раздела «Что уже решено» существуют; (д) число файлов `skirmish/*.ini` и `campaign/maps/*` в пакете равно числу файлов в `resources/bin/skirmish` и `resources/bin/campaign/maps`.
- **C12.** `README.md`: первые 37 строк равны `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:README.md | sed -n '1,37p'`; строка 38 — абзац (б) из пункта 11 дословно; строки 39–41 — пустая, `---`, пустая; остаток файла равен `git show HEAD:README.md`; каждый путь `docs/screenshots/<имя>.png` из `README.md` — существующий файл, и в `README.md` ровно 5 таких ссылок; `sha256sum` пяти снимков равны значениям пункта 12; в `README.md` нет слов `Sangyo` и `README_AI`.
- **C13.** `resources/bin/windowed.bat` побайтно равен `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/windowed.bat`; последняя строка `.gitignore` — `resources/bin/d2tm.exe`, остальные строки равны `git show HEAD:.gitignore`.
- **C14.** `packaging/`: ровно файлы `LINUX_README.txt`, `MACOS_README.txt`, `RELEASE_NOTES.md`, `WINDOWS_README.txt`, `d2tm.sh`, `make_common_assets.sh`; `WINDOWS_README.txt` и `MACOS_README.txt` отличаются от файлов форка только строками, названными в пунктах 5 и 6 (разница `diff`: в `WINDOWS_README.txt` одна изменённая строка, в `MACOS_README.txt` две); `LINUX_README.txt` отличается от файла форка заменой строк 7–18 из пункта 7; `RELEASE_NOTES.md` равен тексту пункта 8; `make_common_assets.sh` равен тексту пункта 4; `d2tm.sh` равен трём строкам пункта 7, права файла (`os.stat`) — `0o755`.
- **C15.** Библиотеки Linux-архива. Архив из C8 распаковывается в `.tmp/p12/dry/linux/pkg`; выполняется `env -u LD_LIBRARY_PATH sh -c 'LD_LIBRARY_PATH=<абсолютный путь pkg>/lib ldd <абсолютный путь pkg>/d2tm'`; каждая строка вывода со словом `libSDL3` указывает на путь внутри `<pkg>/lib/`, строк со словами `not found` нет, и среди строк есть все четыре имени `libSDL3.so`, `libSDL3_image.so`, `libSDL3_ttf.so`, `libSDL3_mixer.so`.
- **C16.** Запуск из пакета. Содержимое `.tmp/p12/dry/linux/pkg` копируется поверх `.tmp/p12/dry/common/package` из C9 (игрок распаковывает оба архива в одну папку); в этой папке выполняется `env -u LD_LIBRARY_PATH SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=<абсолютный путь .tmp/p12/dry/xdg> timeout 120 ./d2tm.sh --ui-audit-scene main-menu --ui-audit-out <абсолютный путь .tmp/p12/dry/audit>`; код выхода `0`, и в `.tmp/p12/dry/audit` есть файл `main-menu.png` (поиск `find` по папке, размер больше 0). Команда и код выхода печатаются.
- **C17.** `resources/bin/THIRD_PARTY_ASSETS_RU.txt` равен тексту, который скрипт строит из `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/THIRD_PARTY_ASSETS_RU.txt`: строки 1, 4 и 43 заменены текстами пункта 13, в конец добавлены пустая строка и три строки пункта 13; в файле нет слов `local` и `локальной`; `resources/bin/README_RU.txt` не существует.

Порядок выполнения проверок в скрипте: C1–C7, C9, C8, C10–C17 (C15 и C16 нужны результаты C8 и C9); печать — по мере выполнения. Если C9 или C8 не выполнены, C16 печатает `FAIL`.

## PLAN-P12

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `.tmp/p12/check_p12.py` | Написать скрипт проверки по разделу «Тесты». Красный прогон: команда проверки 2 раздела «Проверки» до шагов 2–4 — `exit` не `0`, в выводе строки `C3 FAIL`, `C9 FAIL`, `C14 FAIL` (файлов `release.yml` и `make_common_assets.sh` ещё нет). Сохранить вывод в `.tmp/p12/red-check.log`. Сборку проверки 1 для красного прогона не запускать: пока нет `.tmp/out/build/d2tm`, `C8` печатает `FAIL`, это допустимо. | помощник A |
| 2 | `.github/workflows/release.yml`, `.github/workflows/claude-code-review.yml` | Пункты 1 и 3 контракта. | помощник A |
| 3 | `packaging/make_common_assets.sh`, `packaging/d2tm.sh`, `resources/bin/THIRD_PARTY_ASSETS_RU.txt`, `packaging/WINDOWS_README.txt`, `packaging/MACOS_README.txt`, `packaging/LINUX_README.txt`, `packaging/RELEASE_NOTES.md`, `resources/bin/windowed.bat`, `.gitignore` | Пункты 4–10 и 13 контракта. | помощник B |
| 4 | `README.md` | Пункты 11–12 контракта. | помощник C |
| 5 | — | Проверки раздела «Проверки» по порядку. | помощник A |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p12`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 8000 (сухой прогон копирует `resources/bin/`), иначе блок `## Q-P12-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p12 && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p12/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает; в неё ничего не пиши.
2. **Скрипт проверки.** `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib python3 -B .tmp/p12/check_p12.py > .tmp/p12/check.log 2>&1; echo exit=$?` — `exit=0`, в логе последняя строка `CHECKS 17 OK` и по одной строке `C1 OK` … `C17 OK`. Команда запускается после проверки 1 (нужен `.tmp/out/build/d2tm`). В этот же лог пишутся команды и коды выхода проверок C15 (`ldd` из пакета) и C16 (запуск сцены `main-menu` через `d2tm.sh`); для DONE из лога берутся строки этих двух проверок целиком.
3. **actionlint.** `command -v actionlint && actionlint .github/workflows/release.yml; echo exit=$?` — либо `exit=0` после пути `actionlint`, либо только строка `exit=1` (значит, `actionlint` на сервере нет; тогда проверку заменяет C3).
4. **Код не тронут.** `git -c lfs.storage=$PWD/.tmp/p12/lfs diff --stat -- src tests CMakeLists.txt tools create_release.sh create_release.bat .gitattributes .github/workflows/build_manual.yml .github/workflows/build_master.yml .github/workflows/build_pr.yml` — пустой вывод.
5. **Список файлов пакета.** `wc -l .tmp/p12/package-files.txt` и `grep -v -E ' (campaign/maps/|skirmish/)' .tmp/p12/package-files.txt | head -120` — для DONE.
6. `git -c lfs.storage=$PWD/.tmp/p12/lfs status --short` — изменённые (` M`): `.gitignore`, `README.md`, `resources/bin/windowed.bat`; удалённый (` D`): `.github/workflows/claude-code-review.yml`; новые (`??`): `.github/workflows/release.yml`, `packaging/`, `resources/bin/THIRD_PARTY_ASSETS_RU.txt`, `docs/screenshots/` (пять снимков, положил ведущий). Больше ничего. Появилась папка `tests/ui_audit/__pycache__` или другая лишняя — `rm -r` её.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P12-NN` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P12 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p12/progress.md`): строка на каждый шаг плана;
- красный прогон шага 1: вывод `.tmp/p12/red-check.log` (не больше 40 строк);
- вывод каждой проверки 1–6 с кодами выхода (не больше 40 строк на проверку; у проверки 5 — вывод двух команд, не больше 130 строк);
- `git diff --stat` и список для коммитов:
  1. workflows: `.github/workflows/release.yml`, удаление `.github/workflows/claude-code-review.yml`;
  2. упаковка: `packaging/*`, `resources/bin/THIRD_PARTY_ASSETS_RU.txt`, `resources/bin/windowed.bat`, `.gitignore`;
  3. приветствие и галерея: `README.md`, `docs/screenshots/*.png`.

  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …`;
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p12 --size`; у `.tmp/p12` пометка `оставить — логи проверок нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаг 1 (помощник A); после красного прогона — шаги 2 (помощник A), 3 (помощник B) и 4 (помощник C) одновременно.
  4. Шаг 5 (помощник A) — после шагов 2–4.
  5. Сдача и стоп.
- **Параллельно:** шаги 2, 3 и 4 правят разные файлы. Общий порядок один: помощники B и C не создают файлов, пока помощник A не записал в журнал хода строку о конце красного прогона шага 1.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных. Ожидаемое время: помощник A — 40 минут на шаги 1–2 и 80 минут на шаг 5 (сборка, сухой прогон), помощник B — 30 минут, помощник C — 20 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено» и «Контракт»; его шаги плана; помощнику A — раздел «Тесты» и раздел «Проверки»; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p12/`.
  - Корневая нить раздаёт шаги, разбирает ошибки проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Остановки:** только на `## DONE-P12` и на блоках `## Q-P12-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P12-NN` и стоп.
- **Рамка правок:** файлы шагов 1–4 плана и папка `.tmp/p12/`. Понадобился другой файл — блок `## Q-P12-NN` и стоп. Сборка пишет в `.tmp/out/`; это не правка.
- **Команды удаления:** `rm -f` и `rm -rf` песочница отклоняет; обнулить файл — `: > файл`, удалить файл — `rm файл`, папку — `rm -r папка`.
- **Сеть** исполнитель не использует: запуск workflow выпуска на GitHub делает ведущий после PR.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

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
