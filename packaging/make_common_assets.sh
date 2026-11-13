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
for png in campaign_map credits_team credits_title \
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
