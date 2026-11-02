#include "utils/UnitSpriteLayout.hpp"

#include "UnitFrameBaseline.hpp"

#include <cmath>
#include <format>
#include <iostream>
#include <stdexcept>

namespace {
void require(bool condition, const std::string &message)
{
    if (!condition) {
        throw std::runtime_error(message);
    }
}

void requireNear(float actual, float expected, const std::string &label)
{
    require(std::abs(actual - expected) < 0.0001F,
            std::format("{}: expected {}, got {}", label, expected, actual));
}

void testSiegeSourcesAndDensity()
{
    const UnitSpriteFrame frame = resolveUnitSpriteFrame(36, 36, 176, 176, 4);
    require(frame.width == 44 && frame.height == 44 && frame.usesHdFrame,
            "The Siege HD frame must resolve to 44 by 44 logical pixels");

    for (int body = 0; body < 8; ++body) {
        const UnitSpriteRectangle bodySource = unitSpriteSourceRectangle(frame, body, 0);
        require(bodySource.x == body * 44 && bodySource.y == 0 &&
                    bodySource.width == 44 && bodySource.height == 44,
                std::format("Body direction {} has the wrong source rectangle", body));
        for (int turret = 0; turret < 8; ++turret) {
            const UnitSpriteRectangle turretSource = unitSpriteSourceRectangle(frame, turret, 0);
            require(turretSource.x == turret * 44 && turretSource.y == 0 &&
                        turretSource.width == 44 && turretSource.height == 44,
                    std::format("Independent turret direction {} has the wrong source rectangle", turret));
        }
    }

    const UnitSpriteFrame classic = resolveUnitSpriteFrame(36, 36, 176, 176, 1);
    require(classic.width == 36 && classic.height == 36 && !classic.usesHdFrame,
            "Classic rendering must retain the logical frame");
    const UnitSpriteFrame unconfigured = resolveUnitSpriteFrame(36, 36, 0, 0, 4);
    require(unconfigured.width == 36 && unconfigured.height == 36 && !unconfigured.usesHdFrame,
            "A type without an HD frame must retain the logical frame");
}

template <typename Frame, typename Visual>
auto destinationRectangle(Frame frame, Visual visual, float zoom, float worldScale)
{
    if constexpr (requires { unitSpriteDestinationRectangle(frame, visual, zoom, worldScale); }) {
        return unitSpriteDestinationRectangle(frame, visual, zoom, worldScale);
    }
    else {
        return unitSpriteDestinationRectangle(frame, visual, zoom);
    }
}

void testDestinationsAcrossZoom()
{
    const UnitSpriteFrame frame = resolveUnitSpriteFrame(36, 36, 176, 176, 4);
    constexpr int posX = 256;
    constexpr int posY = 288;
    constexpr int viewportX = 64;
    constexpr int viewportY = 80;
    constexpr int topBarHeight = 40;
    for (const float zoom : UnitFrameZoomLevels) {
        const cRectangle visual = unitFrameExpectedVisual(
            posX, posY, viewportX, viewportY, topBarHeight,
            36, 36, zoom
        );
        const UnitSpriteFloatRectangle destination = destinationRectangle(
            frame,
            UnitSpriteRectangle{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()},
            zoom,
            1.0F
        );
        const float width = unitFrameExpectedDestinationSize(44, zoom);
        const float height = unitFrameExpectedDestinationSize(44, zoom);
        requireNear(destination.x, visual.getX() + (visual.getWidth() - width) / 2.0F,
                    "HD destination x");
        requireNear(destination.y, visual.getY() + (visual.getHeight() - height) / 2.0F,
                    "HD destination y");
        requireNear(destination.width, width, "HD destination width");
        requireNear(destination.height, height, "HD destination height");
    }

    const UnitSpriteFrame legacy = resolveUnitSpriteFrame(32, 32, 0, 0, 4);
    const UnitSpriteRectangle visual{17, 29, 41, 43};
    const UnitSpriteFloatRectangle unchanged = destinationRectangle(legacy, visual, 1.3F, 1.5F);
    requireNear(unchanged.x, 17.0F, "Legacy destination x");
    requireNear(unchanged.y, 29.0F, "Legacy destination y");
    requireNear(unchanged.width, 41.0F, "Legacy destination width");
    requireNear(unchanged.height, 43.0F, "Legacy destination height");
}
}

int main()
{
    try {
        testSiegeSourcesAndDensity();
        testDestinationsAcrossZoom();
        std::cout << "unit_sprite_layout: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "unit_sprite_layout: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
