#include <catch2/catch_test_macros.hpp>

#include "controls/cKeyBindings.h"
#include "game/Preferences.hpp"
#include "utils/cIniFile.h"

#include <algorithm>
#include <bitset>
#include <filesystem>
#include <set>
#include <string>
#include <utility>
#include <vector>

namespace {
s_KeyBinding single(SDL_Scancode key, bool ctrl = false, bool alt = false, bool shift = false, bool tab = false)
{
    s_KeyBinding binding;
    binding.keys = {key};
    binding.requireCtrl = ctrl;
    binding.requireAlt = alt;
    binding.requireShift = shift;
    binding.requireTab = tab;
    return binding;
}

cKeyBindings defaults()
{
    cKeyBindings bindings;
    bindings.loadDefaults();
    return bindings;
}

std::filesystem::path freshDirectory(const std::string &name)
{
    const auto directory = std::filesystem::temp_directory_path() / name;
    std::filesystem::remove_all(directory);
    std::filesystem::create_directories(directory);
    return directory;
}

std::set<std::pair<eKeyAction, eKeyAction>> normalizedPairs(
    const std::vector<std::pair<eKeyAction, eKeyAction>> &pairs)
{
    std::set<std::pair<eKeyAction, eKeyAction>> result;
    for (const auto &[first, second] : pairs) {
        result.emplace(std::min(first, second), std::max(first, second));
    }
    return result;
}
}

TEST_CASE("P10C a taken key is refused and names its owner", "[P10C]")
{
    auto bindings = defaults();
    bindings.setBinding(eKeyAction::ATTACK_MODE, single(SDL_SCANCODE_A));
    bindings.setBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_B));

    const auto conflict = bindings.trySetBinding(eKeyAction::ATTACK_MODE, single(SDL_SCANCODE_B));

    REQUIRE(conflict.has_value());
    CHECK(*conflict == eKeyAction::REPAIR_UNIT);
}

TEST_CASE("P10C a refused binding leaves both actions unchanged", "[P10C]")
{
    auto bindings = defaults();
    bindings.setBinding(eKeyAction::ATTACK_MODE, single(SDL_SCANCODE_A));
    bindings.setBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_B));
    REQUIRE(bindings.trySetBinding(eKeyAction::ATTACK_MODE, single(SDL_SCANCODE_B)).has_value());

    const auto *attack = bindings.getBinding(eKeyAction::ATTACK_MODE);
    const auto *repair = bindings.getBinding(eKeyAction::REPAIR_UNIT);
    REQUIRE(attack != nullptr);
    REQUIRE(repair != nullptr);
    CHECK(attack->keys == std::vector<SDL_Scancode>{SDL_SCANCODE_A});
    CHECK(repair->keys == std::vector<SDL_Scancode>{SDL_SCANCODE_B});
}

TEST_CASE("P10C left and right Ctrl are different keys", "[P10C]")
{
    auto bindings = defaults();
    bindings.setBinding(eKeyAction::ATTACK_MODE, single(SDL_SCANCODE_LCTRL));

    const auto conflict = bindings.trySetBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_RCTRL));

    CHECK_FALSE(conflict.has_value());
    REQUIRE(bindings.getBinding(eKeyAction::REPAIR_UNIT) != nullptr);
    CHECK(bindings.getBinding(eKeyAction::REPAIR_UNIT)->keys == std::vector<SDL_Scancode>{SDL_SCANCODE_RCTRL});
}

TEST_CASE("P10C an event with the left Ctrl belongs to the left Ctrl binding only", "[P10C]")
{
    auto bindings = defaults();
    bindings.setBinding(eKeyAction::ATTACK_MODE, single(SDL_SCANCODE_LCTRL));
    std::bitset<SDL_SCANCODE_COUNT> leftCtrl;
    std::bitset<SDL_SCANCODE_COUNT> rightCtrl;
    leftCtrl.set(SDL_SCANCODE_LCTRL);
    rightCtrl.set(SDL_SCANCODE_RCTRL);

    CHECK(bindings.containsActionKey(leftCtrl, eKeyAction::ATTACK_MODE));
    CHECK_FALSE(bindings.containsActionKey(rightCtrl, eKeyAction::ATTACK_MODE));
}

TEST_CASE("P10C left and right Shift are the same key", "[P10C]")
{
    auto leftBindings = defaults();
    auto rightBindings = defaults();

    const auto leftConflict = leftBindings.trySetBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_LSHIFT));
    const auto rightConflict = rightBindings.trySetBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_RSHIFT));

    REQUIRE(leftConflict.has_value());
    REQUIRE(rightConflict.has_value());
    CHECK(*leftConflict == eKeyAction::ADD_TO_SELECTION);
    CHECK(*rightConflict == eKeyAction::ADD_TO_SELECTION);
}

TEST_CASE("P10C left and right Alt are the same key", "[P10C]")
{
    auto bindings = defaults();
    bindings.setBinding(eKeyAction::RETURN_TO_BASE, single(SDL_SCANCODE_RALT));

    const auto conflict = bindings.trySetBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_LALT));

    REQUIRE(conflict.has_value());
    CHECK(*conflict == eKeyAction::RETURN_TO_BASE);
}

TEST_CASE("P10C modifiers make a different key", "[P10C]")
{
    auto ctrlBindings = defaults();
    auto plainBindings = defaults();
    auto tabBindings = defaults();

    const auto ctrlConflict = ctrlBindings.trySetBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_Z, true));
    const auto plainConflict = plainBindings.trySetBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_Z));
    const auto tabConflict = tabBindings.trySetBinding(
        eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_Z, false, false, false, true));

    REQUIRE(ctrlConflict.has_value());
    REQUIRE(plainConflict.has_value());
    CHECK(*ctrlConflict == eKeyAction::SELECT_SAME_TYPE_ON_MAP);
    CHECK(*plainConflict == eKeyAction::ZOOM_RESET);
    CHECK_FALSE(tabConflict.has_value());
}

TEST_CASE("P10C the default shared pairs come from loadDefaults", "[P10C]")
{
    const auto sharedPairs = cKeyBindings::getDefaultSharedPairs();
    CHECK(sharedPairs.size() == 5);
    const auto actual = normalizedPairs(sharedPairs);
    const std::set<std::pair<eKeyAction, eKeyAction>> expected{
        {std::min(eKeyAction::DEPLOY_UNIT, eKeyAction::SEND_TO_REFINERY),
         std::max(eKeyAction::DEPLOY_UNIT, eKeyAction::SEND_TO_REFINERY)},
        {std::min(eKeyAction::MUSIC_VOLUME_UP, eKeyAction::SET_PRIMARY),
         std::max(eKeyAction::MUSIC_VOLUME_UP, eKeyAction::SET_PRIMARY)},
        {std::min(eKeyAction::TOGGLE_FPS, eKeyAction::RETURN_TO_BASE),
         std::max(eKeyAction::TOGGLE_FPS, eKeyAction::RETURN_TO_BASE)},
        {std::min(eKeyAction::OPEN_MENU, eKeyAction::MENU_BACK),
         std::max(eKeyAction::OPEN_MENU, eKeyAction::MENU_BACK)},
        {std::min(eKeyAction::SELECT_SAME_TYPE_ON_MAP, eKeyAction::EDITOR_UNDO),
         std::max(eKeyAction::SELECT_SAME_TYPE_ON_MAP, eKeyAction::EDITOR_UNDO)},
    };

    CHECK(actual == expected);
}

TEST_CASE("P10C actions that share a default key do not conflict", "[P10C]")
{
    auto bindings = defaults();

    CHECK_FALSE(bindings.trySetBinding(eKeyAction::DEPLOY_UNIT, single(SDL_SCANCODE_D)).has_value());
    CHECK_FALSE(bindings.trySetBinding(eKeyAction::SEND_TO_REFINERY, single(SDL_SCANCODE_D)).has_value());
    CHECK_FALSE(bindings.trySetBinding(eKeyAction::SET_PRIMARY, single(SDL_SCANCODE_P)).has_value());
}

TEST_CASE("P10C other actions still conflict on a shared key", "[P10C]")
{
    auto bindings = defaults();

    const auto conflict = bindings.trySetBinding(eKeyAction::DEPLOY_UNIT, single(SDL_SCANCODE_P));

    REQUIRE(conflict.has_value());
    CHECK(*conflict == eKeyAction::MUSIC_VOLUME_UP);
    REQUIRE(bindings.getBinding(eKeyAction::DEPLOY_UNIT) != nullptr);
    CHECK(bindings.getBinding(eKeyAction::DEPLOY_UNIT)->keys == std::vector<SDL_Scancode>{SDL_SCANCODE_D});
}

TEST_CASE("P10C actions outside the table are not checked", "[P10C]")
{
    auto bindings = defaults();

    const auto conflict = bindings.trySetBinding(eKeyAction::REPAIR_UNIT, single(SDL_SCANCODE_1, true));

    CHECK_FALSE(conflict.has_value());
}

TEST_CASE("P10C every table action survives the [KEYS] round trip", "[P10C]")
{
    auto original = defaults();
    cIniFile ini;
    for (const auto &[name, action] : cKeyBindings::getActionTable()) {
        ini.setValue("KEYS", name, original.toIniValue(action));
    }
    auto loaded = cKeyBindings{};
    loaded.loadFromSection(ini.getSection("KEYS"));

    std::size_t checked = 0;
    for (const auto &[name, action] : cKeyBindings::getActionTable()) {
        static_cast<void>(name);
        const auto *before = original.getBinding(action);
        const auto *after = loaded.getBinding(action);
        REQUIRE(before != nullptr);
        REQUIRE(after != nullptr);
        CHECK(after->keys == before->keys);
        CHECK(after->requireCtrl == before->requireCtrl);
        CHECK(after->requireAlt == before->requireAlt);
        CHECK(after->requireShift == before->requireShift);
        CHECK(after->requireTab == before->requireTab);
        ++checked;
    }
    CHECK(checked == 86);
}

TEST_CASE("P10C the file of the player overrides settings.ini", "[P10C]")
{
    const auto directory = freshDirectory("d2tm_p10c_key_override");
    const auto settingsFile = directory / "settings.ini";
    const auto preferencesFile = directory / "preferences.ini";
    std::string error;
    REQUIRE(Preferences::saveKeyBindings(settingsFile, {{"REPAIR", "Q"}, {"QUICK_SAVE", "F8"}}, error));
    REQUIRE(Preferences::saveKeyBindings(preferencesFile, {{"REPAIR", "W"}, {"SCREENSHOT", "F10"}}, error));
    cIniFile settingsIni;
    REQUIRE(settingsIni.load(settingsFile.string()));
    cSection chosenKeys;
    REQUIRE(Preferences::loadKeyBindings(preferencesFile, chosenKeys, error));
    auto bindings = defaults();
    bindings.loadFromSection(settingsIni.getSection("KEYS"));
    bindings.loadFromSection(chosenKeys);

    REQUIRE(bindings.getBinding(eKeyAction::REPAIR_UNIT) != nullptr);
    CHECK(bindings.getBinding(eKeyAction::REPAIR_UNIT)->keys == std::vector<SDL_Scancode>{SDL_SCANCODE_W});
    REQUIRE(bindings.getBinding(eKeyAction::SCREENSHOT) != nullptr);
    CHECK(bindings.getBinding(eKeyAction::SCREENSHOT)->keys == std::vector<SDL_Scancode>{SDL_SCANCODE_F10});
    REQUIRE(bindings.getBinding(eKeyAction::QUICK_SAVE) != nullptr);
    CHECK(bindings.getBinding(eKeyAction::QUICK_SAVE)->keys == std::vector<SDL_Scancode>{SDL_SCANCODE_F8});
    REQUIRE(bindings.getBinding(eKeyAction::TOGGLE_MUSIC) != nullptr);
    CHECK(bindings.getBinding(eKeyAction::TOGGLE_MUSIC)->keys ==
          std::vector<SDL_Scancode>{SDL_SCANCODE_M, SDL_SCANCODE_MUTE});
}

TEST_CASE("P10C keys that cannot be written are refused", "[P10C]")
{
    CHECK_FALSE(cKeyBindings::canStoreKey(SDL_SCANCODE_UNKNOWN));
    CHECK_FALSE(cKeyBindings::canStoreKey(SDL_SCANCODE_TAB));
    CHECK_FALSE(cKeyBindings::canStoreKey(SDL_SCANCODE_COMMA));
    CHECK(cKeyBindings::canStoreKey(SDL_SCANCODE_A));
    CHECK(cKeyBindings::canStoreKey(SDL_SCANCODE_LCTRL));
    CHECK(cKeyBindings::canStoreKey(SDL_SCANCODE_F11));
}

TEST_CASE("P10C a captured key takes the modifiers that were held", "[P10C]")
{
    s_KeysCombo ctrlCombo{};
    ctrlCombo.ctrlPressed = true;
    s_KeysCombo shiftCombo{};
    shiftCombo.shiftPressed = true;
    s_KeysCombo shiftTabCombo{};
    shiftTabCombo.shiftPressed = true;
    shiftTabCombo.tabPressed = true;
    s_KeysCombo tabCombo{};
    tabCombo.tabPressed = true;

    const auto ctrlZ = cKeyBindings::makeCapturedBinding(SDL_SCANCODE_Z, ctrlCombo);
    const auto leftCtrlWithShift = cKeyBindings::makeCapturedBinding(SDL_SCANCODE_LCTRL, shiftCombo);
    const auto leftCtrl = cKeyBindings::makeCapturedBinding(SDL_SCANCODE_LCTRL, ctrlCombo);
    const auto shiftedF2 = cKeyBindings::makeCapturedBinding(SDL_SCANCODE_F2, shiftTabCombo);
    const auto tab = cKeyBindings::makeCapturedBinding(SDL_SCANCODE_TAB, tabCombo);

    CHECK(ctrlZ.keys == std::vector<SDL_Scancode>{SDL_SCANCODE_Z});
    CHECK(ctrlZ.requireCtrl);
    CHECK(leftCtrlWithShift.keys == std::vector<SDL_Scancode>{SDL_SCANCODE_LCTRL});
    CHECK(leftCtrlWithShift.requireShift);
    CHECK_FALSE(leftCtrlWithShift.requireCtrl);
    CHECK_FALSE(leftCtrl.requireCtrl);
    CHECK(shiftedF2.requireShift);
    CHECK(shiftedF2.requireTab);
    CHECK_FALSE(tab.requireTab);
}

TEST_CASE("P10C bindings are described for the player", "[P10C]")
{
    auto bindings = defaults();

    CHECK(bindings.getBindingDisplayName(eKeyAction::ATTACK_MODE) == "Ctrl");
    CHECK(bindings.getBindingDisplayName(eKeyAction::ADD_TO_SELECTION) == "Shift");
    CHECK(bindings.getBindingDisplayName(eKeyAction::TOGGLE_FULLSCREEN) == "Alt+Return");
    CHECK(bindings.getBindingDisplayName(eKeyAction::SELECT_SAME_TYPE_ON_MAP) == "Ctrl+Z");
    CHECK(bindings.getBindingDisplayName(eKeyAction::DEBUG_WIN) == "Shift+Tab+F2");
    CHECK(bindings.getBindingDisplayName(eKeyAction::REPAIR_UNIT) == "R");
    CHECK(cKeyBindings::describeBinding(single(SDL_SCANCODE_LCTRL)) == "Left Ctrl");
    CHECK(cKeyBindings{}.getBindingDisplayName(eKeyAction::REPAIR_UNIT).empty());
}

TEST_CASE("P10C the action table has names for the options page", "[P10C]")
{
    CHECK(cKeyBindings::getActionTable().size() == 86);
    CHECK(cKeyBindings::getActionName(eKeyAction::REPAIR_UNIT) == "REPAIR");
    CHECK(cKeyBindings::getActionName(eKeyAction::SCREENSHOT) == "SCREENSHOT");
    CHECK(cKeyBindings::getActionName(eKeyAction::GROUP_ASSIGN_1).empty());
}
