#pragma once

#include "include/definitions.h"
#include "utils/cRectangle.h"

#include <array>
#include <cmath>
#include <initializer_list>
#include <vector>

struct UnitFrameBaseline {
    int type;
    const char *name;
    int width;
    int height;
    int animationFrames;
    bool hasShadow;
    bool hasBody;
    bool hasTurret;
};

inline constexpr std::array<UnitFrameBaseline, 22> UnitFrameBaselines{{
    {CARRYALL, "CARRYALL", 48, 48, 2, true, true, false},
    {ORNITHOPTER, "ORNITHOPTER", 48, 48, 4, true, true, false},
    {DEVASTATOR, "DEVASTATOR", 38, 46, 1, true, true, false},
    {HARVESTER, "HARVESTER", 80, 52, 4, true, true, false},
    {TANK, "TANK", 32, 32, 0, true, true, true},
    {SIEGETANK, "SIEGETANK", 36, 36, 0, true, true, true},
    {MCV, "MCV", 48, 50, 1, true, true, false},
    {DEVIATOR, "DEVIATOR", 32, 32, 1, false, true, false},
    {LAUNCHER, "LAUNCHER", 32, 32, 1, true, true, false},
    {QUAD, "QUAD", 32, 32, 1, true, true, false},
    {TRIKE, "TRIKE", 28, 26, 1, true, true, false},
    {RAIDER, "RAIDER", 28, 26, 1, true, true, false},
    {FRIGATE, "FRIGATE", 64, 64, 2, true, true, false},
    {SONICTANK, "SONICTANK", 32, 32, 1, true, true, false},
    {SOLDIER, "SOLDIER", 32, 32, 3, false, true, false},
    {INFANTRY, "INFANTRY", 32, 32, 3, false, true, false},
    {TROOPER, "TROOPER", 32, 32, 3, false, true, false},
    {TROOPERS, "TROOPERS", 32, 32, 3, false, true, false},
    {UNIT_FREMEN_ONE, "UNIT_FREMEN_ONE", 32, 32, 3, false, true, false},
    {UNIT_FREMEN_THREE, "UNIT_FREMEN_THREE", 32, 32, 3, false, true, false},
    {SABOTEUR, "SABOTEUR", 32, 32, 3, false, true, false},
    {SANDWORM, "SANDWORM", 48, 48, 0, false, true, false},
}};

inline constexpr std::array<float, 4> UnitFrameZoomLevels{0.8F, 1.0F, 1.3F, 2.0F};
inline constexpr std::array<float, 4> UnitFrameWorldScales{1.0F, 1.1F, 1.25F, 1.5F};
inline constexpr int UnitFrameShadowOpacity = 160;

inline std::vector<int> unitFrameAnimationRows(int animationFrames)
{
    std::vector<int> rows{0};
    if (animationFrames > 0) {
        rows.push_back(1);
        if (animationFrames != 1) {
            rows.push_back(animationFrames);
        }
    }
    return rows;
}

inline int unitFrameFacingIndex(int facingAngle)
{
    return (2 - facingAngle + 8) % 8;
}

inline cRectangle unitFrameExpectedVisual(
    int posX,
    int posY,
    int viewportStartX,
    int viewportStartY,
    int topBarHeight,
    int logicalWidth,
    int logicalHeight,
    float zoom,
    float worldScale)
{
    const int drawX = static_cast<int>(std::round(
        zoom * (posX - viewportStartX + (32 - logicalWidth) / 2)
    ));
    const int drawY = static_cast<int>(std::round(
        zoom * (posY - viewportStartY + (32 - logicalHeight) / 2) + topBarHeight
    ));
    const int originalWidth = static_cast<int>(std::lround(zoom * logicalWidth));
    const int originalHeight = static_cast<int>(std::lround(zoom * logicalHeight));
    const int visualWidth = static_cast<int>(std::lround(originalWidth * worldScale));
    const int visualHeight = static_cast<int>(std::lround(originalHeight * worldScale));
    return {
        drawX - (visualWidth - originalWidth) / 2,
        drawY - (visualHeight - originalHeight) / 2,
        visualWidth,
        visualHeight
    };
}

inline std::array<int, 4> unitFrameExpectedSource(
    int logicalWidth,
    int logicalHeight,
    int facing,
    int animationFrame)
{
    return {facing * logicalWidth, animationFrame * logicalHeight,
            logicalWidth, logicalHeight};
}

inline float unitFrameExpectedDestinationSize(
    int logicalSize,
    float zoom,
    float worldScale)
{
    return static_cast<float>(std::lround(
        std::lround(logicalSize * zoom) * worldScale
    ));
}
