#include "utils/RenderScale.hpp"
#include "game/Preferences.hpp"
#include "utils/InitialGameSettings.hpp"
#include "utils/cIniFile.h"

#include <catch2/catch_test_macros.hpp>

#include <array>
#include <filesystem>
#include <fstream>

TEST_CASE("P4B render scale constants", "[P4B]")
{
    CHECK(MinimumRenderWidth == 800);
    CHECK(MinimumRenderHeight == 600);
    CHECK(AutomaticRenderScale == 0);
    CHECK((ManualRenderScales == std::array<int, 5>{100, 125, 150, 175, 200}));
}

TEST_CASE("P4B render canvas follows the output size and the scale", "[P4B]")
{
    CHECK((calculateRenderCanvasSize(800, 600, 0) == RenderCanvasSize{800, 600}));
    CHECK((calculateRenderCanvasSize(1024, 768, 0) == RenderCanvasSize{800, 600}));
    CHECK((calculateRenderCanvasSize(1280, 720, 0) == RenderCanvasSize{1067, 600}));
    CHECK((calculateRenderCanvasSize(1920, 1080, 0) == RenderCanvasSize{1067, 600}));
    CHECK((calculateRenderCanvasSize(1920, 1080, 100) == RenderCanvasSize{1920, 1080}));
    CHECK((calculateRenderCanvasSize(1920, 1080, 175) == RenderCanvasSize{1097, 617}));
    CHECK((calculateRenderCanvasSize(2560, 1440, 0) == RenderCanvasSize{1067, 600}));
    CHECK((calculateRenderCanvasSize(5120, 1440, 0) == RenderCanvasSize{2133, 600}));
    CHECK((calculateRenderCanvasSize(1366, 768, 125) == RenderCanvasSize{1093, 614}));
    CHECK((calculateRenderCanvasSize(1366, 768, 150) == RenderCanvasSize{1067, 600}));
    CHECK((calculateRenderCanvasSize(3840, 2160, 200) == RenderCanvasSize{1920, 1080}));
    CHECK((calculateRenderCanvasSize(799, 500, 0) == RenderCanvasSize{800, 600}));
    CHECK((calculateRenderCanvasSize(1920, 1080, 120) == RenderCanvasSize{1067, 600}));
}

TEST_CASE("P4B automatic percent and manual choices", "[P4B]")
{
    CHECK(calculateAutomaticRenderScalePercent(1920, 1080) == 180);
    CHECK(calculateAutomaticRenderScalePercent(1024, 768) == 128);
    CHECK(calculateAutomaticRenderScalePercent(800, 600) == 100);
    CHECK(calculateAutomaticRenderScalePercent(640, 480) == 100);
    CHECK(calculateAutomaticRenderScalePercent(3840, 2160) == 360);

    CHECK(isManualRenderScaleAvailable(1920, 1080, 175));
    CHECK_FALSE(isManualRenderScaleAvailable(1920, 1080, 200));
    CHECK_FALSE(isManualRenderScaleAvailable(1920, 1080, 120));
    CHECK_FALSE(isManualRenderScaleAvailable(1920, 1080, 0));
    CHECK(isManualRenderScaleAvailable(800, 600, 100));
    CHECK(isManualRenderScaleAvailable(3840, 2160, 200));
    CHECK_FALSE(isManualRenderScaleAvailable(1366, 768, 150));
}

TEST_CASE("P4B settings read the render scale key", "[P4B]")
{
    const auto setPath = std::filesystem::temp_directory_path() / "p4b_render_scale_set.ini";
    const auto unsetPath = std::filesystem::temp_directory_path() / "p4b_render_scale_unset.ini";
    {
        std::ofstream file(setPath);
        REQUIRE(file.is_open());
        file << "[SETTINGS]\nRenderScale=150\n";
        REQUIRE(file.good());
    }
    {
        std::ofstream file(unsetPath);
        REQUIRE(file.is_open());
        file << "[SETTINGS]\nScreenWidth=1024\n";
        REQUIRE(file.good());
    }

    cIniFile setIni(setPath.string());
    REQUIRE(setIni.isLoadSuccess());
    REQUIRE(setIni.hasSection("SETTINGS"));
    InitialGameSettings setSettings;
    Preferences::readSettings(setIni.getSection("SETTINGS"), setSettings);
    CHECK(setSettings.renderScalePercent == 150);

    cIniFile unsetIni(unsetPath.string());
    REQUIRE(unsetIni.isLoadSuccess());
    REQUIRE(unsetIni.hasSection("SETTINGS"));
    InitialGameSettings unsetSettings;
    Preferences::readSettings(unsetIni.getSection("SETTINGS"), unsetSettings);
    CHECK(unsetSettings.renderScalePercent == 0);

    const auto settingsPath = std::filesystem::path(D2TM_SOURCE_DIR) / "resources/bin/settings.ini";
    cIniFile shippedIni(settingsPath.string());
    REQUIRE(shippedIni.isLoadSuccess());
    REQUIRE(shippedIni.hasSection("SETTINGS"));
    const auto section = shippedIni.getSection("SETTINGS");
    InitialGameSettings shippedSettings;
    Preferences::readSettings(section, shippedSettings);
    CHECK(shippedSettings.renderScalePercent == 0);
    CHECK(section.hasValue("RenderScale"));
    CHECK_FALSE(section.hasValue("ScalingMode"));
    REQUIRE(shippedIni.hasSection("KEYS"));
    const auto keys = shippedIni.getSection("KEYS");
    CHECK(keys.hasValue("TOGGLE_FULLSCREEN"));
    CHECK_FALSE(keys.hasValue("TOGGLE_SCALING_MODE"));

    CHECK(std::filesystem::remove(setPath));
    CHECK(std::filesystem::remove(unsetPath));
}
