#!/usr/bin/env bash
set -euo pipefail

script_path=$(readlink -f -- "${BASH_SOURCE[0]}")
repo_root=$(cd -- "$(dirname -- "$script_path")/../.." && pwd -P)
export DUNE_DEPS_DIR=${DUNE_DEPS_DIR:-/srv/dune/deps}
export DUNE_OUT_DIR=${DUNE_OUT_DIR:-/srv/dune/out/b1}
mkdir -p "$DUNE_DEPS_DIR" "$DUNE_OUT_DIR/logs" "$DUNE_OUT_DIR/tmp"
export DUNE_DEPS_DIR=$(cd -- "$DUNE_DEPS_DIR" && pwd -P)
export DUNE_OUT_DIR=$(cd -- "$DUNE_OUT_DIR" && pwd -P)
export TMPDIR="$DUNE_OUT_DIR/tmp"
prefix="$DUNE_DEPS_DIR/prefix"
menu_text='Setting state from -1(=INITIALIZE) to 1(=MENU)'

question() {
    printf '\nОШИБКА: %s\n' "$*" >&2
    exit 1
}

run() {
    printf 'Команда:'
    printf ' %q' "$@"
    printf '\n'
    timeout 1800 "$@"
}

check_disk() {
    local deps_kib out_kib
    deps_kib=$(du -sk "$DUNE_DEPS_DIR" | cut -f1)
    out_kib=$(du -sk "$DUNE_OUT_DIR" | cut -f1)
    du -sh "$DUNE_DEPS_DIR" "$DUNE_OUT_DIR"
    if (( deps_kib + out_kib > 6 * 1024 * 1024 )); then
        question 'Зависимости и выходной каталог превысили 6 ГБ.'
    fi
}

dependency_options() {
    local name=$1
    dep_url="https://github.com/libsdl-org/$name.git"
    dep_args=("-DCMAKE_BUILD_TYPE=Release" "-DCMAKE_INSTALL_PREFIX=$prefix")
    case "$name" in
        SDL)
            dep_tag=release-3.4.10
            dep_sha=8e37db5e797b6167f3a00d697d816a684bd259c7
            dep_args+=(
                -DSDL_INSTALL=ON -DSDL_SHARED=ON -DSDL_STATIC=OFF
                -DSDL_TEST_LIBRARY=OFF -DSDL_TESTS=OFF -DSDL_EXAMPLES=OFF
                -DSDL_AUDIO=ON -DSDL_VIDEO=ON -DSDL_RENDER=ON
                -DSDL_DUMMYAUDIO=ON -DSDL_DUMMYVIDEO=ON -DSDL_OFFSCREEN=ON
                -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF -DSDL_JACK=OFF
                -DSDL_PIPEWIRE=OFF -DSDL_SNDIO=OFF -DSDL_X11=OFF
                -DSDL_WAYLAND=OFF -DSDL_KMSDRM=OFF -DSDL_OPENGL=OFF
                -DSDL_OPENGLES=OFF -DSDL_VULKAN=OFF -DSDL_UNIX_CONSOLE_BUILD=ON
            )
            ;;
        SDL_image)
            dep_tag=release-3.4.4
            dep_sha=bec9134a26c7d0f31b36d6083c25296e04cabff5
            dep_args+=("-DCMAKE_PREFIX_PATH=$prefix"
                -DBUILD_SHARED_LIBS=ON -DSDLIMAGE_INSTALL=ON
                -DSDLIMAGE_SAMPLES=OFF -DSDLIMAGE_TESTS=OFF
                -DSDLIMAGE_VENDORED=OFF -DSDLIMAGE_PNG=ON
                -DSDLIMAGE_PNG_LIBPNG=OFF -DSDLIMAGE_BACKEND_STB=ON
                -DSDLIMAGE_AVIF=OFF -DSDLIMAGE_JXL=OFF
                -DSDLIMAGE_TIF=OFF -DSDLIMAGE_WEBP=OFF
            )
            ;;
        SDL_ttf)
            dep_tag=release-3.2.2
            dep_sha=a1ce3670aec736ecbf0936c43f2f0cc53aa61e5b
            dep_args+=("-DCMAKE_PREFIX_PATH=$prefix"
                -DBUILD_SHARED_LIBS=ON -DSDLTTF_INSTALL=ON
                -DSDLTTF_SAMPLES=OFF -DSDLTTF_VENDORED=ON
                -DSDLTTF_HARFBUZZ=OFF -DSDLTTF_PLUTOSVG=OFF
            )
            ;;
        SDL_mixer)
            dep_tag=release-3.2.4
            dep_sha=72a81869b45e249e8e67102db4e98dd2441f05a1
            dep_args+=("-DCMAKE_PREFIX_PATH=$prefix"
                -DBUILD_SHARED_LIBS=ON -DSDLMIXER_INSTALL=ON
                -DSDLMIXER_SAMPLES=OFF -DSDLMIXER_EXAMPLES=OFF
                -DSDLMIXER_TESTS=OFF -DSDLMIXER_VENDORED=OFF
                -DSDLMIXER_WAVE=ON -DSDLMIXER_MIDI=ON
                -DSDLMIXER_MIDI_TIMIDITY=ON -DSDLMIXER_MIDI_FLUIDSYNTH=OFF
                -DSDLMIXER_FLAC_LIBFLAC=OFF -DSDLMIXER_GME=OFF
                -DSDLMIXER_MOD=OFF -DSDLMIXER_MP3_MPG123=OFF
                -DSDLMIXER_OPUS=OFF -DSDLMIXER_VORBIS_VORBISFILE=OFF
                -DSDLMIXER_WAVPACK=OFF
            )
            ;;
        Catch2)
            dep_url=https://github.com/catchorg/Catch2.git
            dep_tag=v3.4.0
            dep_sha=6e79e682b726f524310d55dec8ddac4e9c52fb5f
            dep_args+=(
                -DCATCH_DEVELOPMENT_BUILD=OFF -DCATCH_BUILD_TESTING=OFF
                -DCATCH_INSTALL_DOCS=OFF -DCATCH_INSTALL_EXTRAS=ON
            )
            ;;
        *) question "Неизвестная зависимость: $name" ;;
    esac
}

build_dependency() {
    local name=$1 source_dir build_dir actual_sha manifest stamp submodule_url
    dependency_options "$name"
    source_dir="$DUNE_DEPS_DIR/src/$name"
    build_dir="$DUNE_DEPS_DIR/build/$name"
    stamp="$DUNE_DEPS_DIR/installed/$name"
    if [[ ! -d "$source_dir" ]]; then
        run git clone --depth 1 --branch "$dep_tag" "$dep_url" "$source_dir"
    else
        printf 'Исходники уже получены: %s\n' "$source_dir"
    fi
    actual_sha=$(git -C "$source_dir" rev-parse HEAD)
    [[ "$actual_sha" == "$dep_sha" ]] || question "Не совпадает SHA $name."
    printf 'Зависимость: %s; тег: %s; SHA: %s\n' "$name" "$dep_tag" "$actual_sha"
    printf 'Опции CMake:'
    printf ' %q' "${dep_args[@]}"
    printf '\n'
    if [[ "$name" == SDL_ttf ]]; then
        submodule_url=$(git -C "$source_dir" config -f .gitmodules --get submodule.external/freetype.url)
        [[ "$submodule_url" == https://github.com/libsdl-org/freetype.git ]] ||
            question "URL подмодуля FreeType не разрешён: $submodule_url"
        if [[ ! -f "$source_dir/external/freetype/.git" ]]; then
            run git -C "$source_dir" submodule update --init --depth 1 -- external/freetype
        fi
        actual_sha=$(git -C "$source_dir/external/freetype" rev-parse HEAD)
        [[ "$actual_sha" == 9973564cfa63763a3e4ac67c09147899539b1e07 ]] ||
            question 'Не совпадает SHA подмодуля FreeType.'
        printf 'Подмодуль: %s; URL: %s; SHA: %s\n' "$source_dir/external/freetype" "$submodule_url" "$actual_sha"
    fi
    manifest=$(printf '%s\n' "$dep_sha" "${dep_args[@]}")
    if [[ -f "$stamp" && "$(cat "$stamp")" == "$manifest" ]]; then
        printf 'SKIP_DEPENDENCY %s: установка с теми же SHA и опциями уже завершена.\n' "$name"
        return
    fi
    run cmake -S "$source_dir" -B "$build_dir" "${dep_args[@]}"
    run cmake --build "$build_dir" -j16
    run cmake --install "$build_dir"
    printf '%s\n' "$manifest" > "$stamp"
}

run_game() {
    local driver=$1
    printf 'Рабочий каталог: %s\n' "$DUNE_OUT_DIR/run/bin"
    printf 'Команда: SDL_VIDEODRIVER=%s SDL_AUDIODRIVER=dummy XDG_DATA_HOME=%q timeout 20 %q\n' \
        "$driver" "$DUNE_OUT_DIR/xdg" "$DUNE_OUT_DIR/build/d2tm"
    if (cd "$DUNE_OUT_DIR/run/bin" &&
        SDL_VIDEODRIVER="$driver" SDL_AUDIODRIVER=dummy \
        XDG_DATA_HOME="$DUNE_OUT_DIR/xdg" timeout 20 "$DUNE_OUT_DIR/build/d2tm") \
        > "$log_dir/stdout-$driver.log" 2>&1; then
        game_status=0
    else
        game_status=$?
    fi
    game_log="$log_dir/game-$driver.log"
    if [[ -f "$DUNE_OUT_DIR/run/bin/nlog.txt" ]]; then
        cp -p "$DUNE_OUT_DIR/run/bin/nlog.txt" "$game_log"
    else
        : > "$game_log"
    fi
    cat "$log_dir/stdout-$driver.log"
    printf 'Драйвер %s: код выхода timeout %s\n' "$driver" "$game_status"
}

main() {
    printf 'Полный лог: %s/full.log\n' "$log_dir"
    up0=a51b97f15d0eee2d323a1737f140eb2cbd60973c
    printf 'База UP0: %s; HEAD: %s\n' "$up0" "$(git -C "$repo_root" rev-parse HEAD)"
    git -C "$repo_root" merge-base --is-ancestor "$up0" HEAD ||
        question 'UP0 не является предком HEAD.'
    git -C "$repo_root" diff --quiet "$up0" -- . ':(exclude)tools/upstream' ||
        question 'Отслеживаемые файлы вне tools/upstream отличаются от UP0.'
    df -h /
    check_disk
    mkdir -p "$DUNE_DEPS_DIR/src" "$DUNE_DEPS_DIR/build" "$DUNE_DEPS_DIR/installed" "$prefix"
    printf '%s\0' SDL Catch2 |
        xargs -0 -n1 -P2 bash "$script_path" --dependency "$log_dir"
    check_disk
    printf '%s\0' SDL_image SDL_ttf SDL_mixer |
        xargs -0 -n1 -P3 bash "$script_path" --dependency "$log_dir"
    check_disk

    library_dir="$prefix/lib"
    if [[ ! -f "$library_dir/libSDL3.so" ]]; then
        library_dir=$(find "$prefix" -name libSDL3.so -printf '%h\n' -quit)
    fi
    [[ -n "$library_dir" && -f "$library_dir/libSDL3.so" ]] || question 'Не найден установленный libSDL3.so.'
    export CPATH="$prefix/include"
    export LIBRARY_PATH="$library_dir"
    export LD_LIBRARY_PATH="$library_dir"
    printf 'Обход UP0: CMakeLists.txt:88 использует голые имена SDL; CI устанавливает зависимости в стандартные пути /usr/local и вызывает ldconfig.\n'
    printf 'CPATH=%s\nLIBRARY_PATH=%s\nLD_LIBRARY_PATH=%s\n' "$CPATH" "$LIBRARY_PATH" "$LD_LIBRARY_PATH"

    up0_cache="$DUNE_OUT_DIR/build/CMakeCache.txt"
    if [[ -f "$up0_cache" &&
        "$(sed -n 's/^CMAKE_HOME_DIRECTORY:[^=]*=//p' "$up0_cache")" == "$repo_root" &&
        "$(sed -n 's/^CMAKE_BUILD_TYPE:[^=]*=//p' "$up0_cache")" == RelWithDebInfo &&
        "$(sed -n 's/^CMAKE_PREFIX_PATH:[^=]*=//p' "$up0_cache")" == "$prefix" ]]; then
        printf 'Конфигурация UP0 с теми же исходниками и префиксом уже готова.\n'
    else
        run cmake -S "$repo_root" -B "$DUNE_OUT_DIR/build" \
            -DCMAKE_BUILD_TYPE=RelWithDebInfo "-DCMAKE_PREFIX_PATH=$prefix"
    fi
    run make -C "$DUNE_OUT_DIR/build" -j16
    check_disk
    if (cd "$DUNE_OUT_DIR/build" && timeout 1800 ctest --output-on-failure) 2>&1 | tee "$log_dir/ctest.log"; then
        test_summary=$(grep -E '^[0-9]+% tests passed, [0-9]+ tests failed out of [0-9]+' "$log_dir/ctest.log")
        test_count=$(awk '/% tests passed, .* tests failed out of / {print $NF}' "$log_dir/ctest.log")
        [[ "$test_count" =~ ^[1-9][0-9]*$ ]] || question 'В выводе ctest нет ненулевого числа тестов.'
    else
        question "ctest завершился ошибкой; лог $log_dir/ctest.log"
    fi

    if [[ -d "$DUNE_OUT_DIR/run" ]]; then
        mv "$DUNE_OUT_DIR/run" "$log_dir/previous-run"
    fi
    mkdir -p "$DUNE_OUT_DIR/run/bin" "$DUNE_OUT_DIR/xdg"
    cp -a "$repo_root/resources/bin/campaign" "$repo_root/resources/bin/data" \
        "$repo_root/resources/bin/skirmish" "$DUNE_OUT_DIR/run/bin/"
    mkdir -p "$DUNE_OUT_DIR/run/bin/data/bmp" \
        "$DUNE_OUT_DIR/run/bin/save/atreides" "$DUNE_OUT_DIR/run/bin/save/harkonnen" \
        "$DUNE_OUT_DIR/run/bin/save/ordos" "$DUNE_OUT_DIR/run/bin/save/skirmish"
    cp "$repo_root/resources/bin/settings.ini" "$DUNE_OUT_DIR/run/bin/"
    cp "$repo_root/resources/game.ini.org" "$DUNE_OUT_DIR/run/bin/game.ini"
    cp "$repo_root/resources/doc/versionhistory.txt" "$repo_root/resources/doc/controls.txt" "$DUNE_OUT_DIR/run/bin/"
    cp -p "$DUNE_OUT_DIR/build/d2tm" "$DUNE_OUT_DIR/run/bin/"
    run_game dummy
    selected_driver=dummy
    if [[ "$game_status" != 124 ]]; then
        if grep -Eiq 'No available video device|dummy.*(not available|not supported)|Couldn.t find matching render driver|Failed initialized (screen|renderer)' \
            "$log_dir/stdout-dummy.log" "$game_log"; then
            printf 'Ошибка видеодрайвера dummy сохранена; проверяю offscreen.\n'
            run_game offscreen
            selected_driver=offscreen
        else
            question "Запуск с dummy завершился кодом $game_status вместо 124."
        fi
    fi
    [[ "$game_status" == 124 ]] || question "Запуск завершился кодом $game_status вместо 124."
    menu_line=$(grep -F -m1 "$menu_text" "$game_log") || question "В $game_log нет строки перехода в MENU."
    printf '\nИтог\n'
    for name in SDL SDL_image SDL_ttf SDL_mixer Catch2; do
        dependency_options "$name"
        printf '%s %s %s\n' "$name" "$dep_tag" "$(git -C "$DUNE_DEPS_DIR/src/$name" rev-parse HEAD)"
    done
    printf 'Тесты ctest: %s; %s\n' "$test_count" "$test_summary"
    printf 'Запуск: SDL_VIDEODRIVER=%s; код timeout=%s\n' "$selected_driver" "$game_status"
    printf 'Строка MENU: %s\nИсточник: src/game/cGame_logic.cpp:903–904, вызов :785\n' "$menu_line"
    printf 'Лог игры: %s\nКаталог библиотек: %s\n' "$game_log" "$library_dir"
    printf 'Причина переменных окружения: голые имена в CMakeLists.txt:88; в CI апстрима используются стандартные пути /usr/local и ldconfig.\n'
    check_disk
    df -h /
    printf 'Полный лог: %s/full.log\n' "$log_dir"
}

if [[ ${1:-} == --dependency ]]; then
    log_dir=$2
    name=$3
    build_dependency "$name" 2>&1 | tee "$log_dir/$name.log"
    exit
fi

log_dir="$DUNE_OUT_DIR/logs/$(date -u +%Y%m%dT%H%M%S)-$$"
mkdir -p "$log_dir"
main 2>&1 | tee "$log_dir/full.log"
