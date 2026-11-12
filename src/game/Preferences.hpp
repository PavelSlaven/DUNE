/**
 * @file Preferences.hpp
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


#pragma once

#include <filesystem>
#include <array>
#include <span>
#include <string_view>
#include <utility>
#include <vector>
#include <string>

class cSection;
struct InitialGameSettings;

// Saving and loading the player's options, in the same [SETTINGS] format as settings.ini.
namespace Preferences {

inline constexpr const char *FILE_NAME = "preferences.ini";

// Sets the settings for every key present in the section, keys that are absent keep their current value.
void readSettings(const cSection &section, InitialGameSettings &settings);

// Loads the preferences file over the settings. Returns false (settings untouched) when there is
// no usable file, and sets error.
bool load(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);

// Writes every value of the settings. On failure returns false and sets error.
bool save(const std::filesystem::path &file, const InitialGameSettings &settings, std::string &error);

// Saves only scale percentages, preserving other settings when the file is usable.
bool saveScales(const std::filesystem::path &file, int renderScalePercent, int worldScalePercent, std::string &error);

// Loads scale percentages without changing the other settings.
bool loadScales(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);

bool saveLanguage(const std::filesystem::path &file, const std::string &language, std::string &error);

bool loadLanguage(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);

// The values the options menu lets the player choose: read on every start, written only by the options menu.
inline constexpr std::array<std::string_view, 21> CHOSEN_KEYS = {
    "RenderScale", "WorldScale", "Language", "ScreenWidth", "ScreenHeight", "FullScreen",
    "CameraEdgeMove", "CameraBorderOrKeyMoveSpeed", "CameraDragMoveSpeed", "pauseWhenLosingFocus",
    "AllowRepeatingReinforcements", "AllTurretsDownOnLowPower", "RocketTurretsDownOnLowPower",
    "Debug", "NoAI", "oneAi", "disableWormAi", "disableReinforcements", "noAiRest", "drawUnitDebug", "drawUsages",
};

using KeyValues = std::vector<std::pair<std::string, std::string>>;

// Loads only the chosen keys over the settings; the other settings stay as they are.
bool loadChosenOptions(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);

// The text values of the given settings keys in the order of `keys`; a key that is not a settings key is skipped.
KeyValues valuesOf(const InitialGameSettings &settings, std::span<const std::string_view> keys);

// Writes the values to [SETTINGS] and keeps every other key and section of the file.
bool saveValues(const std::filesystem::path &file, const KeyValues &values, std::string &error);

// The save at the end of the game: writes every setting except the chosen keys and keeps the chosen keys and
// every other section of the file as they are.
bool saveOnExit(const std::filesystem::path &file, const InitialGameSettings &settings, std::string &error);

// The [KEYS] section of the file; false when the file has no such section.
bool loadKeyBindings(const std::filesystem::path &file, cSection &section, std::string &error);

// Writes the values to [KEYS] and keeps every other key and section of the file.
bool saveKeyBindings(const std::filesystem::path &file, const KeyValues &values, std::string &error);

}
