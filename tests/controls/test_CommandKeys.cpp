#include <catch2/catch_test_macros.hpp>
#include <bitset>

#include "controls/cKeyBindings.h"
#include "utils/cIniFile.h"

namespace {
using Keys = std::bitset<SDL_SCANCODE_COUNT>;

Keys pressed(SDL_Scancode sc)
{
    Keys keys;
    keys.set(static_cast<size_t>(sc));
    return keys;
}

cKeyBindings defaults()
{
    cKeyBindings bindings;
    bindings.loadDefaults();
    return bindings;
}

cKeyBindings withKeys(const char *action, const char *value)
{
    cSection section("KEYS");
    section.setValue(action, value);
    cKeyBindings bindings = defaults();
    bindings.loadFromSection(section);
    return bindings;
}
}

TEST_CASE("P10A attack and rally default to the Ctrl keys", "[P10A]")
{
    const cKeyBindings bindings = defaults();
    REQUIRE(bindings.containsActionKey(pressed(SDL_SCANCODE_LCTRL), eKeyAction::ATTACK_MODE));
    REQUIRE(bindings.containsActionKey(pressed(SDL_SCANCODE_RCTRL), eKeyAction::ATTACK_MODE));
    REQUIRE_FALSE(bindings.containsActionKey(pressed(SDL_SCANCODE_R), eKeyAction::ATTACK_MODE));
}

TEST_CASE("P10A first key name of a modifier pair", "[P10A]")
{
    REQUIRE(defaults().getFirstKeyDisplayName(eKeyAction::ATTACK_MODE) == "Ctrl");
    REQUIRE(defaults().getFirstKeyDisplayName(eKeyAction::ADD_TO_SELECTION) == "Shift");
    REQUIRE(withKeys("DEPLOY_UNIT", "Right Alt").getFirstKeyDisplayName(eKeyAction::DEPLOY_UNIT) == "Alt");
}

TEST_CASE("P10A first key name is the SDL name for other keys", "[P10A]")
{
    REQUIRE(withKeys("SEND_TO_REFINERY", "Space").getFirstKeyDisplayName(eKeyAction::SEND_TO_REFINERY) ==
            SDL_GetScancodeName(SDL_SCANCODE_SPACE));
    REQUIRE(defaults().getFirstKeyDisplayName(eKeyAction::REPAIR_UNIT) == "R");
}

TEST_CASE("P10A repair key can be rebound", "[P10A]")
{
    const cKeyBindings bindings = withKeys("REPAIR", "F");
    REQUIRE(bindings.containsActionKey(pressed(SDL_SCANCODE_F), eKeyAction::REPAIR_UNIT));
    REQUIRE_FALSE(bindings.containsActionKey(pressed(SDL_SCANCODE_R), eKeyAction::REPAIR_UNIT));
}

TEST_CASE("P10A rebound key name is shown to the player", "[P10A]")
{
    REQUIRE(withKeys("REPAIR", "F").getFirstKeyDisplayName(eKeyAction::REPAIR_UNIT) == "F");
}

TEST_CASE("P10A unknown key name keeps the default", "[P10A]")
{
    REQUIRE(withKeys("REPAIR", "not-a-real-key").containsActionKey(
        pressed(SDL_SCANCODE_R), eKeyAction::REPAIR_UNIT));
}

TEST_CASE("P10A default command keys of the six orders", "[P10A]")
{
    const cKeyBindings bindings = defaults();
    REQUIRE(bindings.containsActionKey(pressed(SDL_SCANCODE_D), eKeyAction::SEND_TO_REFINERY));
    REQUIRE(bindings.containsActionKey(pressed(SDL_SCANCODE_D), eKeyAction::DEPLOY_UNIT));
    REQUIRE(bindings.containsActionKey(pressed(SDL_SCANCODE_R), eKeyAction::REPAIR_UNIT));
    const s_KeysCombo ctrl{.ctrlPressed = true};
    REQUIRE(bindings.matches(pressed(SDL_SCANCODE_RCTRL), ctrl, eKeyAction::ATTACK_MODE));
    REQUIRE(cKeyBindings{}.getFirstKeyDisplayName(eKeyAction::ATTACK_MODE).empty());
}
