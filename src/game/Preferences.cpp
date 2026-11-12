/**
 * @file Preferences.cpp
 *
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 *
 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
 *
 * This is a non-commercial educational project.
 */


#include "game/Preferences.hpp"

#include "utils/cIniFile.h"
#include "utils/InitialGameSettings.hpp"
#include <algorithm>

namespace Preferences {

namespace {
constexpr const char *SECTION = "SETTINGS";

// cIniFile expects UTF-8 file names, path::string() would give the ANSI code page on Windows
std::string utf8FileName(const std::filesystem::path &path)
{
    const std::u8string name = path.u8string();
    return std::string(name.begin(), name.end());
}

std::string toText(bool value)
{
    return value ? "true" : "false";
}

void set(cIniFile &ini, const char *key, const std::string &value)
{
    ini.setValue(SECTION, key, value);
}

bool loadAnyIni(const std::filesystem::path &file, cIniFile &ini, std::string &error)
{
    std::error_code filesystemError;
    if (!std::filesystem::exists(file, filesystemError)) {
        error = "No preferences file found at " + utf8FileName(file);
        return false;
    }

    if (!ini.load(utf8FileName(file))) {
        error = "Preferences file is unusable: " + utf8FileName(file);
        return false;
    }
    return true;
}

bool loadIni(const std::filesystem::path &file, cIniFile &ini, std::string &error)
{
    if (!loadAnyIni(file, ini, error)) {
        return false;
    }
    if (!ini.hasSection(SECTION)) {
        error = "Preferences file is unusable: " + utf8FileName(file);
        return false;
    }
    return true;
}

bool writeIni(const cIniFile &ini, const std::filesystem::path &file, std::string &error)
{
    std::error_code filesystemError;
    std::filesystem::create_directories(file.parent_path(), filesystemError);
    if (filesystemError) {
        error = "Could not create preferences directory: " + filesystemError.message();
        return false;
    }

    // write to a temporary file first, so a crash while writing cannot leave a half written file
    std::filesystem::path tempPath = file;
    tempPath += ".tmp";
    if (!ini.save(utf8FileName(tempPath))) {
        error = "Could not write preferences file";
        return false;
    }
    std::filesystem::rename(tempPath, file, filesystemError);
    if (filesystemError) {
        error = "Could not replace preferences file: " + filesystemError.message();
        return false;
    }
    return true;
}

constexpr const char *KEYS_SECTION = "KEYS";

KeyValues settingsValues(const InitialGameSettings &settings)
{
    return {
        {"ScreenWidth", std::to_string(settings.screenW)},
        {"ScreenHeight", std::to_string(settings.screenH)},
        {"CameraDragMoveSpeed", std::to_string(settings.cameraDragMoveSpeed)},
        {"CameraBorderOrKeyMoveSpeed", std::to_string(settings.cameraBorderOrKeyMoveSpeed)},
        {"FullScreen", toText(!settings.windowed)},
        {"CameraEdgeMove", toText(settings.cameraEdgeMove)},
        {"RenderScale", std::to_string(settings.renderScalePercent)},
        {"WorldScale", std::to_string(settings.worldScalePercent)},
        {"Language", settings.language},
        {"AllowRepeatingReinforcements", toText(settings.allowRepeatingReinforcements)},
        {"AllTurretsDownOnLowPower", toText(settings.turretsDownOnLowPower)},
        {"RocketTurretsDownOnLowPower", toText(settings.rocketTurretsDownOnLowPower)},
        {"ShowLowPowerIcon", toText(settings.showLowPowerIcon)},
        {"GameRules", settings.gameFilename},
        {"NoAI", toText(settings.disableAI)},
        {"Debug", toText(settings.debugMode)},
        {"playMusic", toText(settings.playMusic)},
        {"customMusic", toText(settings.customMusic)},
        {"playSound", toText(settings.playSound)},
        {"playCreditsSound", toText(settings.playCreditsSound)},
        {"drawUnitDebug", toText(settings.drawUnitDebug)},
        {"oneAi", toText(settings.oneAi)},
        {"disableWormAi", toText(settings.disableWormAi)},
        {"disableReinforcements", toText(settings.disableReinforcements)},
        {"noAiRest", toText(settings.noAiRest)},
        {"drawUsages", toText(settings.drawUsages)},
        {"pauseWhenLosingFocus", toText(settings.pauseWhenLosingFocus)},
        {"fogOfWarEnabled", toText(settings.fogOfWarEnabled)},
    };
}

bool saveInSection(const std::filesystem::path &file, const char *section, const KeyValues &values, std::string &error)
{
    cIniFile loaded;
    std::string loadError;
    cIniFile fresh;
    cIniFile &ini = loadAnyIni(file, loaded, loadError) ? loaded : fresh;
    for (const auto &[key, value] : values) {
        ini.setValue(section, key, value);
    }
    return writeIni(ini, file, error);
}
}

void readSettings(const cSection &section, InitialGameSettings &settings)
{
    if (section.hasValue("ScreenWidth")) {
        settings.screenW = section.getInt("ScreenWidth");
    }
    if (section.hasValue("ScreenHeight")) {
        settings.screenH = section.getInt("ScreenHeight");
    }
    if (section.hasValue("CameraDragMoveSpeed")) {
        settings.cameraDragMoveSpeed = section.getDouble("CameraDragMoveSpeed");
    }
    if (section.hasValue("CameraBorderOrKeyMoveSpeed")) {
        settings.cameraBorderOrKeyMoveSpeed = section.getDouble("CameraBorderOrKeyMoveSpeed");
    }
    if (section.hasValue("FullScreen")) {
        settings.windowed = !section.getBoolean("FullScreen");
    }
    if (section.hasValue("CameraEdgeMove")) {
        settings.cameraEdgeMove = section.getBoolean("CameraEdgeMove");
    }
    if (section.hasValue("RenderScale")) {
        settings.renderScalePercent = section.getInt("RenderScale");
    }
    if (section.hasValue("WorldScale")) {
        settings.worldScalePercent = section.getInt("WorldScale");
    }
    if (section.hasValue("Language")) {
        settings.language = section.getStringValue("Language");
    }
    if (section.hasValue("AllowRepeatingReinforcements")) {
        settings.allowRepeatingReinforcements = section.getBoolean("AllowRepeatingReinforcements");
    }
    if (section.hasValue("AllTurretsDownOnLowPower")) {
        settings.turretsDownOnLowPower = section.getBoolean("AllTurretsDownOnLowPower");
    }
    if (section.hasValue("ShowLowPowerIcon")) {
        settings.showLowPowerIcon = section.getBoolean("ShowLowPowerIcon");
    }
    if (section.hasValue("RocketTurretsDownOnLowPower")) {
        settings.rocketTurretsDownOnLowPower = section.getBoolean("RocketTurretsDownOnLowPower");
    }
    if (section.hasValue("GameRules")) {
        settings.gameFilename = section.getStringValue("GameRules");
    }
    if (section.hasValue("NoAI")) {
        settings.disableAI = section.getBoolean("NoAI");
    }
    if (section.hasValue("Debug")) {
        settings.debugMode = section.getBoolean("Debug");
    }
    if (section.hasValue("playMusic")) {
        settings.playMusic = section.getBoolean("playMusic");
    }
    if (section.hasValue("customMusic")) {
        settings.customMusic = section.getBoolean("customMusic");
    }
    if (section.hasValue("playSound")) {
        settings.playSound = section.getBoolean("playSound");
    }
    if (section.hasValue("playCreditsSound")) {
        settings.playCreditsSound = section.getBoolean("playCreditsSound");
    }
    if (section.hasValue("drawUnitDebug")) {
        settings.drawUnitDebug = section.getBoolean("drawUnitDebug");
    }
    if (section.hasValue("oneAi")) {
        settings.oneAi = section.getBoolean("oneAi");
    }
    if (section.hasValue("disableWormAi")) {
        settings.disableWormAi = section.getBoolean("disableWormAi");
    }
    if (section.hasValue("disableReinforcements")) {
        settings.disableReinforcements = section.getBoolean("disableReinforcements");
    }
    if (section.hasValue("noAiRest")) {
        settings.noAiRest = section.getBoolean("noAiRest");
    }
    if (section.hasValue("drawUsages")) {
        settings.drawUsages = section.getBoolean("drawUsages");
    }
    if (section.hasValue("pauseWhenLosingFocus")) {
        settings.pauseWhenLosingFocus = section.getBoolean("pauseWhenLosingFocus");
    }
    if (section.hasValue("fogOfWarEnabled")) {
        settings.fogOfWarEnabled = section.getBoolean("fogOfWarEnabled");
    }
}

bool load(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error)
{
    cIniFile ini;
    if (!loadIni(file, ini, error)) {
        return false;
    }
    readSettings(ini.getSection(SECTION), settings);
    return true;
}

bool save(const std::filesystem::path &file, const InitialGameSettings &settings, std::string &error)
{
    cIniFile ini;
    for (const auto &[key, value] : settingsValues(settings)) {
        set(ini, key.c_str(), value);
    }

    return writeIni(ini, file, error);
}

bool saveScales(
    const std::filesystem::path &file,
    int renderScalePercent,
    int worldScalePercent,
    std::string &error)
{
    cIniFile loaded;
    std::string loadError;
    cIniFile fresh;
    cIniFile &ini = loadAnyIni(file, loaded, loadError) ? loaded : fresh;
    set(ini, "RenderScale", std::to_string(renderScalePercent));
    set(ini, "WorldScale", std::to_string(worldScalePercent));
    return writeIni(ini, file, error);
}

bool loadScales(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error)
{
    cIniFile ini;
    if (!loadIni(file, ini, error)) {
        return false;
    }

    const cSection section = ini.getSection(SECTION);
    if (section.hasValue("RenderScale")) {
        settings.renderScalePercent = section.getInt("RenderScale");
    }
    if (section.hasValue("WorldScale")) {
        settings.worldScalePercent = section.getInt("WorldScale");
    }
    return true;
}

bool saveLanguage(const std::filesystem::path &file, const std::string &language, std::string &error)
{
    cIniFile loaded;
    std::string loadError;
    cIniFile fresh;
    cIniFile &ini = loadAnyIni(file, loaded, loadError) ? loaded : fresh;
    set(ini, "Language", language);
    return writeIni(ini, file, error);
}

bool loadLanguage(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error)
{
    cIniFile ini;
    if (!loadIni(file, ini, error)) {
        return false;
    }

    const cSection section = ini.getSection(SECTION);
    if (section.hasValue("Language")) {
        settings.language = section.getStringValue("Language");
    }
    return true;
}

bool loadChosenOptions(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error)
{
    cIniFile ini;
    if (!loadIni(file, ini, error)) {
        return false;
    }

    InitialGameSettings loaded = settings;
    readSettings(ini.getSection(SECTION), loaded);
    settings.screenW = loaded.screenW;
    settings.screenH = loaded.screenH;
    settings.windowed = loaded.windowed;
    settings.cameraDragMoveSpeed = loaded.cameraDragMoveSpeed;
    settings.cameraBorderOrKeyMoveSpeed = loaded.cameraBorderOrKeyMoveSpeed;
    settings.cameraEdgeMove = loaded.cameraEdgeMove;
    settings.renderScalePercent = loaded.renderScalePercent;
    settings.worldScalePercent = loaded.worldScalePercent;
    settings.language = loaded.language;
    settings.allowRepeatingReinforcements = loaded.allowRepeatingReinforcements;
    settings.turretsDownOnLowPower = loaded.turretsDownOnLowPower;
    settings.rocketTurretsDownOnLowPower = loaded.rocketTurretsDownOnLowPower;
    settings.disableAI = loaded.disableAI;
    settings.debugMode = loaded.debugMode;
    settings.drawUnitDebug = loaded.drawUnitDebug;
    settings.oneAi = loaded.oneAi;
    settings.disableWormAi = loaded.disableWormAi;
    settings.disableReinforcements = loaded.disableReinforcements;
    settings.noAiRest = loaded.noAiRest;
    settings.drawUsages = loaded.drawUsages;
    settings.pauseWhenLosingFocus = loaded.pauseWhenLosingFocus;
    return true;
}

KeyValues valuesOf(const InitialGameSettings &settings, std::span<const std::string_view> keys)
{
    const KeyValues all = settingsValues(settings);
    KeyValues result;
    for (const std::string_view key : keys) {
        const auto found = std::find_if(all.begin(), all.end(), [key](const auto &entry) { return entry.first == key; });
        if (found != all.end()) {
            result.push_back(*found);
        }
    }
    return result;
}

bool saveValues(const std::filesystem::path &file, const KeyValues &values, std::string &error)
{
    return saveInSection(file, SECTION, values, error);
}

bool saveOnExit(const std::filesystem::path &file, const InitialGameSettings &settings, std::string &error)
{
    // The chosen keys are written only by the options menu: values changed by command-line options must not
    // become the player's choice, and a key the player never chose must not shadow settings.ini.
    KeyValues unchosen;
    for (const auto &entry : settingsValues(settings)) {
        if (std::find(CHOSEN_KEYS.begin(), CHOSEN_KEYS.end(), entry.first) == CHOSEN_KEYS.end()) {
            unchosen.push_back(entry);
        }
    }
    return saveInSection(file, SECTION, unchosen, error);
}

bool loadKeyBindings(const std::filesystem::path &file, cSection &section, std::string &error)
{
    cIniFile ini;
    if (!loadAnyIni(file, ini, error)) {
        return false;
    }
    if (!ini.hasSection(KEYS_SECTION)) {
        error = "No key bindings in " + utf8FileName(file);
        return false;
    }
    section = ini.getSection(KEYS_SECTION);
    return true;
}

bool saveKeyBindings(const std::filesystem::path &file, const KeyValues &values, std::string &error)
{
    return saveInSection(file, KEYS_SECTION, values, error);
}

}
