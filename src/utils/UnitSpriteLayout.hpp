#pragma once

#include <cmath>

struct UnitSpriteFrame {
    int width;
    int height;
    bool usesHdFrame;
};

struct UnitSpriteRectangle {
    int x;
    int y;
    int width;
    int height;
};

struct UnitSpriteFloatRectangle {
    float x;
    float y;
    float width;
    float height;
};

inline UnitSpriteFrame resolveUnitSpriteFrame(
    int bmpWidth,
    int bmpHeight,
    int hdFrameWidth,
    int hdFrameHeight,
    int textureDensity)
{
    if (textureDensity > 1 && hdFrameWidth > 0 && hdFrameHeight > 0) {
        return {
            hdFrameWidth / textureDensity,
            hdFrameHeight / textureDensity,
            true
        };
    }

    return {bmpWidth, bmpHeight, false};
}

inline UnitSpriteRectangle unitSpriteSourceRectangle(
    UnitSpriteFrame frame,
    int facingIndex,
    int animationFrame)
{
    return {
        facingIndex * frame.width,
        animationFrame * frame.height,
        frame.width,
        frame.height
    };
}

inline UnitSpriteFloatRectangle unitSpriteDestinationRectangle(
    UnitSpriteFrame frame,
    UnitSpriteRectangle visual,
    float cameraZoom,
    float worldScale)
{
    if (!frame.usesHdFrame) {
        return {
            static_cast<float>(visual.x),
            static_cast<float>(visual.y),
            static_cast<float>(visual.width),
            static_cast<float>(visual.height)
        };
    }

    const int zoomedWidth = static_cast<int>(std::lround(frame.width * cameraZoom));
    const int zoomedHeight = static_cast<int>(std::lround(frame.height * cameraZoom));
    const int destinationWidth = static_cast<int>(std::lround(zoomedWidth * worldScale));
    const int destinationHeight = static_cast<int>(std::lround(zoomedHeight * worldScale));

    return {
        static_cast<float>(visual.x) + static_cast<float>(visual.width - destinationWidth) / 2.0F,
        static_cast<float>(visual.y) + static_cast<float>(visual.height - destinationHeight) / 2.0F,
        static_cast<float>(destinationWidth),
        static_cast<float>(destinationHeight)
    };
}
