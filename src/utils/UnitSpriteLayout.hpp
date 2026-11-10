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
    float cameraZoom)
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
    return {
        static_cast<float>(visual.x) + static_cast<float>(visual.width - zoomedWidth) / 2.0F,
        static_cast<float>(visual.y) + static_cast<float>(visual.height - zoomedHeight) / 2.0F,
        static_cast<float>(zoomedWidth),
        static_cast<float>(zoomedHeight)
    };
}
