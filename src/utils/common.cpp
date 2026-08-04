/*

  Dune II - The Maker

  Author : Stefan Hendriks
  Contact: stefan@fundynamic.com
  Website: http://dune2themaker.fundynamic.com

  2001 - 2022 (c) code by Stefan Hendriks

  */

#include "common.h"

#include "data/gfxdata.h"
#include "data/gfxinter.h"
#include "d2tmc.h"
#include "gameobjects/projectiles/bullet.h"
#include "map/cMapCamera.h"
#include "sidebar/cSideBar.h"
#include "utils/cLog.h"
#include "utils/cSoundPlayer.h"
#include "utils/cIniFile.h"
#include "utils/Graphics.hpp"
#include "utils/GameSettings.hpp"

#include <cmath>
#include <filesystem>
#include <format>
#include <fstream>
#include <iterator>
#include <sstream>
#include <system_error>
#include <vector>

#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#define Unknown WindowsUnknown
#include <windows.h>
#undef Unknown
#endif

#include "data/gfxaudio.h"

std::unique_ptr<GameSettings> loadSettingsFromIni(const std::string& filename)
{
    std::shared_ptr<cIniFile> file = std::make_shared<cIniFile>(filename, true);
    std::unique_ptr<GameSettings> gameSettings = std::make_unique<GameSettings>();

    if (!file->hasSection("SETTINGS")) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_GAMERULES, filename, "Expected to find [SETTINGS] in file.ini file");
        return gameSettings;
    }

    const cSection &section = file->getSection("SETTINGS");

    if (section.hasValue("ScreenWidth"))
        gameSettings->screenW = section.getInt("ScreenWidth");
    if (section.hasValue("ScreenHeight"))
        gameSettings->screenH = section.getInt("ScreenHeight");
    if (section.hasValue("RenderScale"))
        gameSettings->renderScalePercent = section.getInt("RenderScale");
    if (section.hasValue("WorldScale"))
        gameSettings->worldScalePercent = section.getInt("WorldScale");
    if (section.hasValue("GraphicsMode"))
        gameSettings->graphicsMode = graphicsModeFromString(
            section.getStringValue("GraphicsMode")
        );
    if (section.hasValue("CameraDragMoveSpeed"))
        gameSettings->cameraDragMoveSpeed = section.getDouble("CameraDragMoveSpeed");
    if (section.hasValue("CameraBorderOrKeyMoveSpeed"))
        gameSettings->cameraBorderOrKeyMoveSpeed = section.getDouble("CameraBorderOrKeyMoveSpeed");
    if (section.hasValue("CameraEdgeMove"))
        gameSettings->cameraEdgeMove = section.getBoolean("CameraEdgeMove");
    if (section.hasValue("FullScreen"))
        gameSettings->windowed = !section.getBoolean("FullScreen");
    if (section.hasValue("AllowRepeatingReinforcements"))
        gameSettings->allowRepeatingReinforcements = section.getBoolean("AllowRepeatingReinforcements");
    if (section.hasValue("AllTurretsDownOnLowPower"))
        gameSettings->turretsDownOnLowPower = section.getBoolean("AllTurretsDownOnLowPower");
    if (section.hasValue("RocketTurretsDownOnLowPower"))
        gameSettings->rocketTurretsDownOnLowPower = section.getBoolean("RocketTurretsDownOnLowPower");
    if (section.hasValue("GameRules"))
        gameSettings->gameFilename = section.getStringValue("GameRules");
    if (section.hasValue("NoAI"))
        gameSettings->disableAI = section.getBoolean("NoAI");
    if (section.hasValue("Debug"))
        gameSettings->debugMode = section.getBoolean("Debug");

    if (section.hasValue("playMusic"))
        gameSettings->playMusic = section.getBoolean("playMusic");
    if (section.hasValue("playSound"))
        gameSettings->playSound = section.getBoolean("playSound");

    if (section.hasValue("drawUnitDebug"))
        gameSettings->drawUnitDebug = section.getBoolean("drawUnitDebug");
    if (section.hasValue("oneAi"))
        gameSettings->oneAi = section.getBoolean("oneAi");
    if (section.hasValue("disableWormAi"))
        gameSettings->disableWormAi = section.getBoolean("disableWormAi");

    if (section.hasValue("disableReinforcements"))
        gameSettings->disableReinforcements = section.getBoolean("disableReinforcements");
    if (section.hasValue("noAiRest"))
        gameSettings->noAiRest = section.getBoolean("noAiRest");
    if (section.hasValue("drawUsages"))
        gameSettings->drawUsages = section.getBoolean("drawUsages");
    if (section.hasValue("pauseWhenLosingFocus"))
        gameSettings->pauseWhenLosingFocus = section.getBoolean("pauseWhenLosingFocus");
    if (section.hasValue("Language"))
        gameSettings->language = section.getStringValue("Language");
    if (section.hasValue("KeyAttack"))
        gameSettings->commandBindings.attack = commandBindingFromIni(
            section.getStringValue("KeyAttack"), gameSettings->commandBindings.attack);
    if (section.hasValue("KeyRepair"))
        gameSettings->commandBindings.repair = commandBindingFromIni(
            section.getStringValue("KeyRepair"), gameSettings->commandBindings.repair);
    if (section.hasValue("KeyUnload"))
        gameSettings->commandBindings.unload = commandBindingFromIni(
            section.getStringValue("KeyUnload"), gameSettings->commandBindings.unload);
    if (section.hasValue("KeyDeploy"))
        gameSettings->commandBindings.deploy = commandBindingFromIni(
            section.getStringValue("KeyDeploy"), gameSettings->commandBindings.deploy);
    if (section.hasValue("KeyRally"))
        gameSettings->commandBindings.rally = commandBindingFromIni(
            section.getStringValue("KeyRally"), gameSettings->commandBindings.rally);
    if (section.hasValue("KeyRelease"))
        gameSettings->commandBindings.release = commandBindingFromIni(
            section.getStringValue("KeyRelease"), gameSettings->commandBindings.release);

    return gameSettings;
}

namespace {
std::string trimIniLine(std::string value)
{
    const auto first = value.find_first_not_of(" \t");
    if (first == std::string::npos) {
        return "";
    }
    const auto last = value.find_last_not_of(" \t");
    return value.substr(first, last - first + 1);
}

bool isIniSection(const std::string &line)
{
    const std::string trimmed = trimIniLine(line);
    return trimmed.size() >= 2 && trimmed.front() == '[' && trimmed.back() == ']';
}

bool isIniKey(const std::string &line, const std::string &key)
{
    const std::string trimmed = trimIniLine(line);
    if (trimmed.empty() || trimmed.front() == '#' || trimmed.front() == ';') {
        return false;
    }

    const auto equals = trimmed.find('=');
    if (equals == std::string::npos) {
        return false;
    }
    return trimIniLine(trimmed.substr(0, equals)) == key;
}

std::string replaceIniValue(const std::string &line, const std::string &value)
{
    const std::size_t equals = line.find('=');
    if (equals == std::string::npos) {
        return line;
    }

    std::size_t valueStart = equals + 1;
    while (valueStart < line.size() && (line[valueStart] == ' ' || line[valueStart] == '\t')) {
        ++valueStart;
    }

    std::size_t suffixStart = line.find_first_of("#;", valueStart);
    if (suffixStart == std::string::npos) {
        suffixStart = line.size();
    }
    while (suffixStart > valueStart &&
           (line[suffixStart - 1] == ' ' || line[suffixStart - 1] == '\t')) {
        --suffixStart;
    }

    return line.substr(0, valueStart) + value + line.substr(suffixStart);
}
}

namespace {
bool saveIniReplacements(
    const std::string &filename,
    const std::vector<std::pair<std::string, std::string>> &replacements,
    std::string &errorMessage)
{
    errorMessage.clear();
    std::ifstream input(filename, std::ios::binary);
    if (!input) {
        errorMessage = "Unable to open settings file";
        return false;
    }

    std::string contents{
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()
    };
    input.close();

    std::string byteOrderMark;
    if (contents.starts_with("\xEF\xBB\xBF")) {
        byteOrderMark = contents.substr(0, 3);
        contents.erase(0, 3);
    }

    const std::string newline = contents.find("\r\n") != std::string::npos ? "\r\n" : "\n";
    const bool hadFinalNewline = !contents.empty() && contents.back() == '\n';
    std::vector<std::string> lines;
    std::istringstream lineReader(contents);
    std::string line;
    while (std::getline(lineReader, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        lines.push_back(line);
    }

    std::size_t settingsStart = lines.size();
    std::size_t settingsEnd = lines.size();
    for (std::size_t index = 0; index < lines.size(); ++index) {
        const std::string trimmed = trimIniLine(lines[index]);
        if (trimmed == "[SETTINGS]") {
            settingsStart = index;
            settingsEnd = lines.size();
            for (std::size_t next = index + 1; next < lines.size(); ++next) {
                if (isIniSection(lines[next])) {
                    settingsEnd = next;
                    break;
                }
            }
            break;
        }
    }

    if (settingsStart == lines.size()) {
        errorMessage = "Missing [SETTINGS] section";
        return false;
    }

    std::vector<bool> replaced(replacements.size(), false);

    for (std::size_t index = settingsStart + 1; index < settingsEnd; ++index) {
        for (std::size_t replacement = 0; replacement < replacements.size(); ++replacement) {
            if (isIniKey(lines[index], replacements[replacement].first)) {
                lines[index] = replaceIniValue(lines[index], replacements[replacement].second);
                replaced[replacement] = true;
                break;
            }
        }
    }

    std::size_t insertionPoint = settingsEnd;
    for (std::size_t replacement = 0; replacement < replacements.size(); ++replacement) {
        if (!replaced[replacement]) {
            lines.insert(
                lines.begin() + static_cast<std::ptrdiff_t>(insertionPoint),
                replacements[replacement].first + "=" + replacements[replacement].second
            );
            ++insertionPoint;
        }
    }

    std::ostringstream output;
    output << byteOrderMark;
    for (std::size_t index = 0; index < lines.size(); ++index) {
        output << lines[index];
        if (index + 1 < lines.size() || hadFinalNewline) {
            output << newline;
        }
    }

    const std::filesystem::path destination(filename);
    const std::filesystem::path temporary = destination.string() + ".tmp";
    {
        std::ofstream temporaryOutput(temporary, std::ios::binary | std::ios::trunc);
        if (!temporaryOutput) {
            errorMessage = "Unable to create temporary settings file";
            return false;
        }
        const std::string serialized = output.str();
        temporaryOutput.write(serialized.data(), static_cast<std::streamsize>(serialized.size()));
        temporaryOutput.flush();
        if (!temporaryOutput) {
            errorMessage = "Unable to write temporary settings file";
            temporaryOutput.close();
            std::error_code cleanupError;
            std::filesystem::remove(temporary, cleanupError);
            return false;
        }
    }

#ifdef _WIN32
    if (!MoveFileExW(
            temporary.wstring().c_str(),
            destination.wstring().c_str(),
            MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)) {
        errorMessage = std::format(
            "Could not replace settings file (Windows error {})",
            GetLastError()
        );
        std::error_code cleanupError;
        std::filesystem::remove(temporary, cleanupError);
        return false;
    }
#else
    std::error_code replaceError;
    std::filesystem::rename(temporary, destination, replaceError);
    if (replaceError) {
        errorMessage = replaceError.message();
        std::error_code cleanupError;
        std::filesystem::remove(temporary, cleanupError);
        return false;
    }
#endif

    return true;
}

std::string boolToIni(bool value)
{
    return value ? "true" : "false";
}
}

bool saveDisplaySettingsToIni(
    const std::string &filename,
    int screenWidth,
    int screenHeight,
    bool fullscreen,
    int renderScalePercent,
    int worldScalePercent,
    GraphicsMode graphicsMode,
    std::string &errorMessage)
{
    return saveIniReplacements(filename, {
        {"ScreenWidth", std::format("{}", screenWidth)},
        {"ScreenHeight", std::format("{}", screenHeight)},
        {"FullScreen", boolToIni(fullscreen)},
        {"RenderScale", std::format("{}", renderScalePercent)},
        {"WorldScale", std::format("{}", worldScalePercent)},
        {"GraphicsMode", graphicsModeToString(graphicsMode)}
    }, errorMessage);
}

bool saveSettingsToIni(
    const std::string &filename,
    const GameSettings &settings,
    std::string &errorMessage)
{
    return saveIniReplacements(filename, {
        {"ScreenWidth", std::format("{}", settings.screenW)},
        {"ScreenHeight", std::format("{}", settings.screenH)},
        {"FullScreen", boolToIni(!settings.windowed)},
        {"RenderScale", std::format("{}", settings.renderScalePercent)},
        {"WorldScale", std::format("{}", settings.worldScalePercent)},
        {"GraphicsMode", graphicsModeToString(settings.graphicsMode)},
        {"CameraDragMoveSpeed", std::format("{}", settings.cameraDragMoveSpeed)},
        {"CameraBorderOrKeyMoveSpeed", std::format("{}", settings.cameraBorderOrKeyMoveSpeed)},
        {"CameraEdgeMove", boolToIni(settings.cameraEdgeMove)},
        {"AllowRepeatingReinforcements", boolToIni(settings.allowRepeatingReinforcements)},
        {"AllTurretsDownOnLowPower", boolToIni(settings.turretsDownOnLowPower)},
        {"RocketTurretsDownOnLowPower", boolToIni(settings.rocketTurretsDownOnLowPower)},
        {"GameRules", settings.gameFilename},
        {"NoAI", boolToIni(settings.disableAI)},
        {"Debug", boolToIni(settings.debugMode)},
        {"playMusic", boolToIni(settings.playMusic)},
        {"playSound", boolToIni(settings.playSound)},
        {"drawUnitDebug", boolToIni(settings.drawUnitDebug)},
        {"oneAi", boolToIni(settings.oneAi)},
        {"disableWormAi", boolToIni(settings.disableWormAi)},
        {"disableReinforcements", boolToIni(settings.disableReinforcements)},
        {"noAiRest", boolToIni(settings.noAiRest)},
        {"drawUsages", boolToIni(settings.drawUsages)},
        {"pauseWhenLosingFocus", boolToIni(settings.pauseWhenLosingFocus)},
        {"Language", settings.language},
        {"KeyAttack", commandBindingToIni(settings.commandBindings.attack)},
        {"KeyRepair", commandBindingToIni(settings.commandBindings.repair)},
        {"KeyUnload", commandBindingToIni(settings.commandBindings.unload)},
        {"KeyDeploy", commandBindingToIni(settings.commandBindings.deploy)},
        {"KeyRally", commandBindingToIni(settings.commandBindings.rally)},
        {"KeyRelease", commandBindingToIni(settings.commandBindings.release)}
    }, errorMessage);
}


/**
 * Default printing in logs. Only will be done if game.isDebugMode() is true.
 * @param txt
 */
void logbook(const std::string &txt)
{
    if (game.isDebugMode()) {
        cLogger *logger = cLogger::getInstance();
        logger->log(LOG_WARN, COMP_NONE, "(logbook)", txt);
    }
}

int slowThinkMsToTicks(int desiredMs)
{
    if (desiredMs < 100) {
        return 1; // fastest thinking is 1 tick (100 ms)
    }
    // "slow" thinking, is 1 tick == 100ms
    return desiredMs / 100;
}

int fastThinkTicksToMs(int ticks)
{
    // "fast" thinking, is 1 tick == 5ms
    return ticks * 5;
}

int fastThinkMsToTicks(int desiredMs)
{
    if (desiredMs < 5) {
        return 1; // fastest thinking is 1 tick (5 ms)
    }
    // "fast" thinking, is 1 tick == 5ms
    return desiredMs / 5;
}

/******************************
 Calculation for SPICE/POWER bars, returns amount of pixels
 ******************************/
// MAX_W = pixels maxed
// I = How much we have (CURRENT STATE)
// W = MAX it can have
float healthBar(float max_w, int i, int w)
{
    float flHP   = i;
    float flMAX  = w;

    if (flHP > flMAX) {
        return max_w;
    }

    // amount of pixels (max_w = 100%)
    auto health = flHP / flMAX;

    return (health * max_w);
}

// return a border cell, close to iCll
int iFindCloseBorderCell(int iCll)
{
    return global_map.findCloseMapBorderCellRelativelyToDestinationCel(iCll);
}


int distanceBetweenCellAndCenterOfScreen(int iCell)
{
    if (global_map.isValidCell(iCell)) {
        int centerX = mapCamera->getViewportCenterX();
        int centerY = mapCamera->getViewportCenterY();

        int cellX = global_map.getAbsoluteXPositionFromCell(iCell);
        int cellY = global_map.getAbsoluteYPositionFromCell(iCell);

        return ABS_length(centerX, centerY, cellX, cellY);
    }
    // return as if very close?
    return 1;
}

/**
 * Creates a bullet, of type, starting at *fromCell* and moving towards *targetCell*. The 'unitWhichShoots' or
 * 'structureWhichShoots' is the owner of the bullet.
 * @param type
 * @param fromCell
 * @param targetCell
 * @param unitWhichShoots
 * @param structureWhichShoots
 * @return
 */
int createBullet(int type, int fromCell, int targetCell, int unitWhichShoots, int structureWhichShoots)
{
    int new_id = -1;

    for (int i = 0; i < MAX_BULLETS; i++)
        if (bullet[i].bAlive == false) {
            new_id = i;
            break;
        }

    if (new_id < 0)
        return -1;  // failed

    if (type < 0)
        return -1; // failed


    cBullet &newBullet = bullet[new_id];
    newBullet.init();

    newBullet.iType = type;
    newBullet.posX = global_map.getAbsoluteXPositionFromCellCentered(fromCell);
    newBullet.posY = global_map.getAbsoluteYPositionFromCellCentered(fromCell);
    newBullet.iOwnerStructure = structureWhichShoots;
    newBullet.iOwnerUnit = unitWhichShoots;

    newBullet.targetX = global_map.getAbsoluteXPositionFromCellCentered(targetCell);
    newBullet.targetY = global_map.getAbsoluteYPositionFromCellCentered(targetCell);

    // if we start firing from a mountain, flag it so the bullet won't be blocked by mountains along
    // the way
    newBullet.bStartedFromMountain = global_map.getCell(fromCell)->type == TERRAIN_MOUNTAIN;

    int structureIdAtTargetCell = global_map.getCellIdStructuresLayer(targetCell);
    if (structureIdAtTargetCell > -1) {
        cAbstractStructure *pStructure = structure[structureIdAtTargetCell];
        if (pStructure && pStructure->isValid()) {
            newBullet.targetX = pStructure->getRandomPosX();
            newBullet.targetY = pStructure->getRandomPosY();
        }
    }

    newBullet.bAlive = true;
    newBullet.iFrame = 0;

    newBullet.iPlayer = -1;

    if (unitWhichShoots > -1 ) {
        cUnit &cUnit = unit[unitWhichShoots];
        newBullet.iPlayer = cUnit.iPlayer;
        // if an airborn unit shoots (ie Ornithopter), reveal on map for everyone
        if (cUnit.isAirbornUnit()) {
            global_map.clearShroudForAllPlayers(fromCell, 2);
        }
    }

    if (structureWhichShoots > -1) {
        cAbstractStructure *pStructure = structure[structureWhichShoots];
        newBullet.iPlayer = pStructure->getOwner();

        int unitIdAtTargetCell = global_map.getCellIdUnitLayer(targetCell);
        if (unitIdAtTargetCell > -1) {
            cUnit &unitTarget = unit[unitIdAtTargetCell];
            // reveal for player which is being attacked
            global_map.clearShroud(fromCell, 2, unitTarget.iPlayer);
        }

        unitIdAtTargetCell = global_map.getCellIdAirUnitLayer(targetCell);
        if (unitIdAtTargetCell > -1) {
            cUnit &unitTarget = unit[unitIdAtTargetCell];
            // reveal for player which is being attacked
            global_map.clearShroud(fromCell, 2, unitTarget.iPlayer);
        }
    }

    if (newBullet.iPlayer < 0) {
        logbook("New bullet produced without any player!?");
    }

    // play sound (when we have one)
    s_BulletInfo &sBullet = sBulletInfo[type];
    if (sBullet.sound > -1) {
        game.playSoundWithDistance(sBullet.sound, distanceBetweenCellAndCenterOfScreen(fromCell));
    }

    return new_id;
}

const char *toStringBuildTypeSpecificType(const eBuildType &buildType, const int &specificTypeId)
{
    switch (buildType) {
        case eBuildType::SPECIAL:
            return sSpecialInfo[specificTypeId].description;
        case eBuildType::UNIT:
            return sUnitInfo[specificTypeId].name;
        case eBuildType::STRUCTURE:
            return sStructureInfo[specificTypeId].name;
        case eBuildType::BULLET:
            return sBulletInfo[specificTypeId].description;
        case eBuildType::UPGRADE:
            return sUpgradeInfo[specificTypeId].description;
        case eBuildType::UNKNOWN:
            return "Unknown";
        default:
            assert(false && "Undefined buildType?");
            break;
    }
    return "";
}
