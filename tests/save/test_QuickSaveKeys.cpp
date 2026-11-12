#include <catch2/catch_test_macros.hpp>

#include "controls/cKeyBindings.h"
#include "utils/cIniFile.h"

#include <bitset>
#include <string>

namespace {
std::bitset<SDL_SCANCODE_COUNT> pressed(SDL_Scancode scancode)
{
    std::bitset<SDL_SCANCODE_COUNT> keys;
    keys.set(static_cast<std::size_t>(scancode));
    return keys;
}
}

TEST_CASE("P8 quick save and quick load default keys", "[P8]")
{
    cKeyBindings bindings;
    bindings.loadDefaults();

    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F5), s_KeysCombo{}, eKeyAction::QUICK_SAVE));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F9), s_KeysCombo{}, eKeyAction::QUICK_LOAD));
}

TEST_CASE("P8 viewport bookmark 5 moved to F6", "[P8]")
{
    cKeyBindings bindings;
    bindings.loadDefaults();
    s_KeysCombo alt;
    alt.altPressed = true;

    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F6), s_KeysCombo{}, eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_F5), s_KeysCombo{}, eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F6), alt, eKeyAction::SAVE_VIEWPORT_BOOKMARK_5));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_F5), alt, eKeyAction::SAVE_VIEWPORT_BOOKMARK_5));
}

TEST_CASE("P8 quick keys do not fire with the debug modifiers", "[P8]")
{
    cKeyBindings bindings;
    bindings.loadDefaults();
    s_KeysCombo debugModifiers;
    debugModifiers.shiftPressed = true;
    debugModifiers.tabPressed = true;

    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_F5), debugModifiers, eKeyAction::QUICK_SAVE));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_F9), debugModifiers, eKeyAction::QUICK_LOAD));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F5), debugModifiers, eKeyAction::DEBUG_REVEAL_MAP));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F9), debugModifiers, eKeyAction::DEBUG_SPAWN_WORM));
}

TEST_CASE("P8 settings.ini binds F5, F9 and F6", "[P8]")
{
    cIniFile ini(std::string(D2TM_SOURCE_DIR) + "/resources/bin/settings.ini");
    REQUIRE(ini.hasSection("KEYS"));

    cKeyBindings bindings;
    bindings.loadDefaults();
    bindings.loadFromSection(ini.getSection("KEYS"));
    s_KeysCombo alt;
    alt.altPressed = true;

    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F5), s_KeysCombo{}, eKeyAction::QUICK_SAVE));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F9), s_KeysCombo{}, eKeyAction::QUICK_LOAD));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F6), s_KeysCombo{}, eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_F5), s_KeysCombo{}, eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5));
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_F6), alt, eKeyAction::SAVE_VIEWPORT_BOOKMARK_5));
    REQUIRE_FALSE(bindings.matches(pressed(SDL_SCANCODE_F5), alt, eKeyAction::SAVE_VIEWPORT_BOOKMARK_5));
}
