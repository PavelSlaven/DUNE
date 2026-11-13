/**
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 */

#include <catch2/catch_test_macros.hpp>
#include <filesystem>
#include <string>
#include "game/Preferences.hpp"
#include "utils/cIniFile.h"
#include "utils/InitialGameSettings.hpp"

namespace {
std::filesystem::path freshDirectory(const char *name)
{
    const auto dir = std::filesystem::temp_directory_path() / name;
    std::filesystem::remove_all(dir);
    return dir;
}
}

TEST_CASE("Preferences - saved settings load back identical", "[preferences]")
{
    const auto file = freshDirectory("d2tm_prefs_roundtrip") / "preferences.ini";

    InitialGameSettings saved;
    saved.screenW = 1280;
    saved.screenH = 720;
    saved.cameraDragMoveSpeed = 0.75f;
    saved.cameraBorderOrKeyMoveSpeed = 0.25f;
    saved.cameraEdgeMove = false;
    saved.windowed = true;
    saved.renderScalePercent = 150;
    saved.allowRepeatingReinforcements = true;
    saved.turretsDownOnLowPower = true;
    saved.rocketTurretsDownOnLowPower = true;
    saved.showLowPowerIcon = true;
    saved.playMusic = false;
    saved.playSound = false;
    saved.debugMode = true;
    saved.drawUnitDebug = true;
    saved.disableAI = true;
    saved.oneAi = true;
    saved.disableWormAi = true;
    saved.disableReinforcements = true;
    saved.noAiRest = true;
    saved.drawUsages = true;
    saved.fogOfWarEnabled = true;
    saved.pauseWhenLosingFocus = true;
    saved.gameFilename = "custom.ini";

    std::string error;
    REQUIRE(Preferences::save(file, saved, error));

    InitialGameSettings loaded;
    REQUIRE(Preferences::load(file, loaded, error));
    REQUIRE(loaded.screenW == 1280);
    REQUIRE(loaded.screenH == 720);
    REQUIRE(loaded.cameraDragMoveSpeed == 0.75f);
    REQUIRE(loaded.cameraBorderOrKeyMoveSpeed == 0.25f);
    REQUIRE_FALSE(loaded.cameraEdgeMove);
    REQUIRE(loaded.windowed);
    REQUIRE(loaded.renderScalePercent == 150);
    REQUIRE(loaded.allowRepeatingReinforcements);
    REQUIRE(loaded.turretsDownOnLowPower);
    REQUIRE(loaded.rocketTurretsDownOnLowPower);
    REQUIRE(loaded.showLowPowerIcon);
    REQUIRE_FALSE(loaded.playMusic);
    REQUIRE_FALSE(loaded.playSound);
    REQUIRE(loaded.debugMode);
    REQUIRE(loaded.drawUnitDebug);
    REQUIRE(loaded.disableAI);
    REQUIRE(loaded.oneAi);
    REQUIRE(loaded.disableWormAi);
    REQUIRE(loaded.disableReinforcements);
    REQUIRE(loaded.noAiRest);
    REQUIRE(loaded.drawUsages);
    REQUIRE(loaded.fogOfWarEnabled);
    REQUIRE(loaded.pauseWhenLosingFocus);
    REQUIRE(loaded.gameFilename == "custom.ini");
}

TEST_CASE("Preferences - loading a missing file leaves the settings untouched", "[preferences]")
{
    InitialGameSettings settings;
    settings.fogOfWarEnabled = true;
    std::string error;
    REQUIRE_FALSE(Preferences::load(freshDirectory("d2tm_prefs_missing") / "preferences.ini", settings, error));
    REQUIRE_FALSE(error.empty());
    REQUIRE(settings.fogOfWarEnabled);
}

TEST_CASE("Preferences - the low power icon is off unless the preferences enable it", "[preferences]")
{
    REQUIRE_FALSE(InitialGameSettings{}.showLowPowerIcon);

    const auto file = freshDirectory("d2tm_prefs_lowpoweroff") / "preferences.ini";
    InitialGameSettings saved;
    std::string error;
    REQUIRE(Preferences::save(file, saved, error));

    InitialGameSettings loaded;
    loaded.showLowPowerIcon = true;
    REQUIRE(Preferences::load(file, loaded, error));
    REQUIRE_FALSE(loaded.showLowPowerIcon);
}

TEST_CASE("P5B preferences save and load WorldScale", "[P5B]")
{
    CHECK(std::string(Preferences::FILE_NAME) == "preferences.ini");
    const auto file = freshDirectory("d2tm_p5b_prefs_world") / "preferences.ini";
    InitialGameSettings saved;
    saved.renderScalePercent = 150;
    saved.worldScalePercent = 125;
    std::string error;
    REQUIRE(Preferences::save(file, saved, error));

    InitialGameSettings loaded;
    REQUIRE(Preferences::load(file, loaded, error));
    CHECK(loaded.renderScalePercent == 150);
    CHECK(loaded.worldScalePercent == 125);
}

TEST_CASE("P5B preferences saveScales keeps the other keys", "[P5B]")
{
    const auto file = freshDirectory("d2tm_p5b_prefs_keep") / "preferences.ini";
    InitialGameSettings saved;
    saved.playMusic = false;
    saved.fogOfWarEnabled = true;
    saved.renderScalePercent = 100;
    saved.worldScalePercent = 100;
    std::string error;
    REQUIRE(Preferences::save(file, saved, error));
    REQUIRE(Preferences::saveScales(file, 175, 110, error));

    InitialGameSettings loaded;
    REQUIRE(Preferences::load(file, loaded, error));
    CHECK(loaded.renderScalePercent == 175);
    CHECK(loaded.worldScalePercent == 110);
    CHECK(loaded.playMusic == false);
    CHECK(loaded.fogOfWarEnabled == true);
}

TEST_CASE("P5B preferences saveScales creates a missing file", "[P5B]")
{
    const auto file = freshDirectory("d2tm_p5b_prefs_new") / "nested" / "preferences.ini";
    std::string error;
    REQUIRE(Preferences::saveScales(file, 150, 125, error));
    CHECK(std::filesystem::exists(file) == true);

    InitialGameSettings loaded;
    REQUIRE(Preferences::load(file, loaded, error));
    CHECK(loaded.renderScalePercent == 150);
    CHECK(loaded.worldScalePercent == 125);
    CHECK(loaded.screenW == 0);
    CHECK(loaded.playMusic == true);
    CHECK(loaded.fogOfWarEnabled == false);
}

TEST_CASE("P5B preferences loadScales reads only the scale keys", "[P5B]")
{
    const auto file = freshDirectory("d2tm_p5b_prefs_scales") / "preferences.ini";
    InitialGameSettings saved;
    saved.screenW = 1280;
    saved.playMusic = false;
    saved.fogOfWarEnabled = true;
    saved.renderScalePercent = 125;
    saved.worldScalePercent = 150;
    std::string error;
    REQUIRE(Preferences::save(file, saved, error));

    InitialGameSettings loaded;
    REQUIRE(Preferences::loadScales(file, loaded, error));
    CHECK(loaded.renderScalePercent == 125);
    CHECK(loaded.worldScalePercent == 150);
    CHECK(loaded.screenW == 0);
    CHECK(loaded.playMusic == true);
    CHECK(loaded.fogOfWarEnabled == false);

    const auto missingFile = freshDirectory("d2tm_p5b_prefs_missing") / "preferences.ini";
    InitialGameSettings untouched;
    untouched.renderScalePercent = 100;
    untouched.worldScalePercent = 110;
    std::string missingError;
    CHECK(Preferences::loadScales(missingFile, untouched, missingError) == false);
    CHECK(missingError.empty() == false);
    CHECK(untouched.renderScalePercent == 100);
    CHECK(untouched.worldScalePercent == 110);
}

TEST_CASE("Preferences default language is Russian", "[preferences]")
{
    CHECK(InitialGameSettings{}.language == "ru");
}

TEST_CASE("Preferences readSettings reads Language", "[preferences]")
{
    cSection section("SETTINGS");
    section.setValue("Language", "en");
    InitialGameSettings settings;

    Preferences::readSettings(section, settings);

    CHECK(settings.language == "en");
}

TEST_CASE("Preferences save writes Language", "[preferences]")
{
    const auto file = freshDirectory("d2tm_prefs_language_save") / "preferences.ini";
    InitialGameSettings settings;
    settings.language = "en";
    std::string error;
    REQUIRE(Preferences::save(file, settings, error));

    cIniFile ini;
    REQUIRE(ini.load(file.string()));
    CHECK(ini.getSection("SETTINGS").getStringValue("Language") == "en");
}

TEST_CASE("Preferences loadLanguage reads only Language", "[preferences]")
{
    const auto file = freshDirectory("d2tm_prefs_language_load") / "preferences.ini";
    InitialGameSettings saved;
    saved.language = "en";
    saved.renderScalePercent = 150;
    std::string error;
    REQUIRE(Preferences::save(file, saved, error));

    InitialGameSettings loaded;
    loaded.language = "ru";
    loaded.renderScalePercent = 125;
    REQUIRE(Preferences::loadLanguage(file, loaded, error));
    CHECK(loaded.language == "en");
    CHECK(loaded.renderScalePercent == 125);
}

TEST_CASE("Preferences loadLanguage leaves settings unchanged for a missing file", "[preferences]")
{
    InitialGameSettings settings;
    settings.language = "ru";
    settings.renderScalePercent = 125;
    std::string error;

    CHECK_FALSE(Preferences::loadLanguage(
        freshDirectory("d2tm_prefs_language_missing") / "preferences.ini", settings, error));
    CHECK_FALSE(error.empty());
    CHECK(settings.language == "ru");
    CHECK(settings.renderScalePercent == 125);
}

TEST_CASE("Preferences saveLanguage preserves other keys", "[preferences]")
{
    const auto file = freshDirectory("d2tm_prefs_language_preserve") / "preferences.ini";
    InitialGameSettings saved;
    saved.renderScalePercent = 150;
    std::string error;
    REQUIRE(Preferences::save(file, saved, error));
    REQUIRE(Preferences::saveLanguage(file, "en", error));

    cIniFile ini;
    REQUIRE(ini.load(file.string()));
    const auto section = ini.getSection("SETTINGS");
    CHECK(section.getInt("RenderScale") == 150);
    CHECK(section.getStringValue("Language") == "en");
}

TEST_CASE("Preferences saveLanguage creates a missing file", "[preferences]")
{
    const auto file = freshDirectory("d2tm_prefs_language_new") / "nested" / "preferences.ini";
    std::string error;

    REQUIRE(Preferences::saveLanguage(file, "en", error));
    CHECK(std::filesystem::exists(file));

    cIniFile ini;
    REQUIRE(ini.load(file.string()));
    CHECK(ini.getSection("SETTINGS").getStringValue("Language") == "en");
}
