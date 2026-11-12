#include <catch2/catch_test_macros.hpp>
#include <bitset>
#include <string>

#include "controls/cKeyBindings.h"
#include "utils/cIniFile.h"

namespace {
std::bitset<SDL_SCANCODE_COUNT> pressed(SDL_Scancode scancode)
{
    std::bitset<SDL_SCANCODE_COUNT> keys;
    keys.set(static_cast<std::size_t>(scancode));
    return keys;
}

cKeyBindings loadedFromSettingsIni()
{
    cKeyBindings bindings;
    bindings.loadDefaults();
    cIniFile ini(std::string(D2TM_SOURCE_DIR) + "/resources/bin/settings.ini");
    bindings.loadFromSection(ini.getSection("KEYS"));
    return bindings;
}
}

TEST_CASE("P9 music track keys are bound to square brackets by default", "[P9]")
{
    cKeyBindings bindings;
    bindings.loadDefaults();
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_LEFTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_PREVIOUS_TRACK));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_RIGHTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_NEXT_TRACK));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_LEFTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_NEXT_TRACK));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_RIGHTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_PREVIOUS_TRACK));
}

TEST_CASE("P9 music track keys load from the shipped settings.ini", "[P9]")
{
    cIniFile ini(std::string(D2TM_SOURCE_DIR) + "/resources/bin/settings.ini");
    const auto section = ini.getSection("KEYS");
    REQUIRE(section.hasValue("MUSIC_PREVIOUS_TRACK"));
    REQUIRE(section.getStringValue("MUSIC_PREVIOUS_TRACK") == "[");
    REQUIRE(section.hasValue("MUSIC_NEXT_TRACK"));
    REQUIRE(section.getStringValue("MUSIC_NEXT_TRACK") == "]");

    cKeyBindings bindings = loadedFromSettingsIni();
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_LEFTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_PREVIOUS_TRACK));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_RIGHTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_NEXT_TRACK));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_LEFTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_NEXT_TRACK));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_RIGHTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_PREVIOUS_TRACK));
}

TEST_CASE("P9 square bracket keys are not shared with another action", "[P9]")
{
    const cKeyBindings bindings = loadedFromSettingsIni();
    for (const SDL_Scancode scancode : {SDL_SCANCODE_LEFTBRACKET, SDL_SCANCODE_RIGHTBRACKET}) {
        int count = 0;
        for (int index = 0; index <= static_cast<int>(eKeyAction::DEBUG_SWITCH_PLAYER_3); ++index) {
            if (bindings.matches(pressed(scancode), s_KeysCombo{}, static_cast<eKeyAction>(index))) {
                ++count;
            }
        }
        REQUIRE(count == 1);
    }
}
