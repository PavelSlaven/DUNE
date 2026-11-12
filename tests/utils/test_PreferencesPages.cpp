#include <catch2/catch_test_macros.hpp>

#include "game/Preferences.hpp"
#include "utils/InitialGameSettings.hpp"
#include "utils/cIniFile.h"

#include <array>
#include <filesystem>
#include <string>
#include <string_view>
#include <vector>

namespace {
std::filesystem::path freshDirectory(const std::string &name)
{
    const auto directory = std::filesystem::temp_directory_path() / name;
    std::filesystem::remove_all(directory);
    std::filesystem::create_directories(directory);
    return directory;
}
}

TEST_CASE("P10C the chosen keys are the 21 keys of the options menu", "[P10C]")
{
    constexpr std::array<std::string_view, 21> expected{
        "RenderScale", "WorldScale", "Language", "ScreenWidth", "ScreenHeight", "FullScreen",
        "CameraEdgeMove", "CameraBorderOrKeyMoveSpeed", "CameraDragMoveSpeed", "pauseWhenLosingFocus",
        "AllowRepeatingReinforcements", "AllTurretsDownOnLowPower", "RocketTurretsDownOnLowPower",
        "Debug", "NoAI", "oneAi", "disableWormAi", "disableReinforcements", "noAiRest", "drawUnitDebug",
        "drawUsages",
    };

    CHECK(Preferences::CHOSEN_KEYS == expected);
}

TEST_CASE("P10C loadChosenOptions reads only the chosen keys", "[P10C]")
{
    const auto file = freshDirectory("d2tm_p10c_chosen_only") / "preferences.ini";
    InitialGameSettings saved;
    saved.screenW = 1280;
    saved.debugMode = true;
    saved.cameraDragMoveSpeed = 0.75f;
    saved.playMusic = false;
    saved.fogOfWarEnabled = true;
    std::string error;
    REQUIRE(Preferences::save(file, saved, error));

    InitialGameSettings loaded;
    REQUIRE(Preferences::loadChosenOptions(file, loaded, error));
    CHECK(loaded.screenW == 1280);
    CHECK(loaded.debugMode);
    CHECK(loaded.cameraDragMoveSpeed == 0.75f);
    CHECK(loaded.playMusic);
    CHECK_FALSE(loaded.fogOfWarEnabled);

    InitialGameSettings untouched;
    untouched.screenW = 1234;
    untouched.debugMode = true;
    std::string missingError;
    CHECK_FALSE(Preferences::loadChosenOptions(
        freshDirectory("d2tm_p10c_chosen_missing") / "preferences.ini", untouched, missingError));
    CHECK_FALSE(missingError.empty());
    CHECK(untouched.screenW == 1234);
    CHECK(untouched.debugMode);
}

TEST_CASE("P10C saved values keep the other keys and the key bindings", "[P10C]")
{
    const auto file = freshDirectory("d2tm_p10c_values_preserve") / "preferences.ini";
    std::string error;
    REQUIRE(Preferences::saveKeyBindings(file, {{"REPAIR", "Q"}}, error));
    REQUIRE(Preferences::saveValues(file, {{"Debug", "true"}, {"ScreenWidth", "1024"}}, error));

    InitialGameSettings loaded;
    REQUIRE(Preferences::load(file, loaded, error));
    CHECK(loaded.debugMode);
    CHECK(loaded.screenW == 1024);
    cSection keys;
    REQUIRE(Preferences::loadKeyBindings(file, keys, error));
    CHECK(keys.getStringValue("REPAIR") == "Q");

    REQUIRE(Preferences::saveScales(file, 150, 125, error));
    REQUIRE(Preferences::loadKeyBindings(file, keys, error));
    CHECK(keys.getStringValue("REPAIR") == "Q");
    REQUIRE(Preferences::load(file, loaded, error));
    CHECK(loaded.debugMode);
}

TEST_CASE("P10C a file with only key bindings has no chosen options", "[P10C]")
{
    const auto file = freshDirectory("d2tm_p10c_keys_only") / "preferences.ini";
    std::string error;
    REQUIRE(Preferences::saveKeyBindings(file, {{"REPAIR", "Q"}}, error));

    InitialGameSettings settings;
    CHECK_FALSE(Preferences::loadChosenOptions(file, settings, error));
    CHECK_FALSE(error.empty());
    cSection keys;
    CHECK(Preferences::loadKeyBindings(file, keys, error));
}

TEST_CASE("P10C the exit save keeps the chosen keys and the key bindings", "[P10C]")
{
    const auto file = freshDirectory("d2tm_p10c_exit_preserve") / "preferences.ini";
    std::string error;
    REQUIRE(Preferences::saveValues(file, {{"Debug", "true"}, {"RenderScale", "150"}}, error));
    REQUIRE(Preferences::saveKeyBindings(file, {{"REPAIR", "Q"}}, error));
    InitialGameSettings settings;
    settings.debugMode = false;
    settings.renderScalePercent = 100;
    settings.playMusic = false;
    settings.fogOfWarEnabled = true;
    settings.screenW = 1280;
    REQUIRE(Preferences::saveOnExit(file, settings, error));

    cIniFile ini;
    REQUIRE(ini.load(file.string()));
    const cSection values = ini.getSection("SETTINGS");
    CHECK(values.getStringValue("Debug") == "true");
    CHECK(values.getStringValue("RenderScale") == "150");
    CHECK_FALSE(values.hasValue("ScreenWidth"));
    CHECK(values.getStringValue("playMusic") == "false");
    CHECK(values.getStringValue("fogOfWarEnabled") == "true");
    CHECK(ini.getSection("KEYS").getStringValue("REPAIR") == "Q");
}

TEST_CASE("P10C the exit save of a missing file writes no chosen key", "[P10C]")
{
    const auto file = freshDirectory("d2tm_p10c_exit_new") / "preferences.ini";
    InitialGameSettings settings;
    settings.playMusic = false;
    std::string error;
    REQUIRE(Preferences::saveOnExit(file, settings, error));

    cIniFile ini;
    REQUIRE(ini.load(file.string()));
    const cSection values = ini.getSection("SETTINGS");
    CHECK(values.hasValue("playMusic"));
    CHECK_FALSE(values.hasValue("Debug"));
    CHECK_FALSE(values.hasValue("NoAI"));
    CHECK_FALSE(values.hasValue("RenderScale"));
    CHECK_FALSE(values.hasValue("ScreenWidth"));
}

TEST_CASE("P10C valuesOf renders the requested keys in order", "[P10C]")
{
    InitialGameSettings settings;
    settings.debugMode = true;
    constexpr std::array<std::string_view, 4> requested{"Debug", "FullScreen", "ScreenWidth", "Unknown"};
    const auto values = Preferences::valuesOf(settings, requested);

    REQUIRE(values.size() == 3);
    const std::pair<std::string, std::string> debug{"Debug", "true"};
    const std::pair<std::string, std::string> fullscreen{"FullScreen", "true"};
    const std::pair<std::string, std::string> screenWidth{"ScreenWidth", "800"};
    CHECK(values[0] == debug);
    CHECK(values[1] == fullscreen);
    CHECK(values[2] == screenWidth);
}
