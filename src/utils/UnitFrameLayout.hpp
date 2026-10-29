#pragma once

#include <cmath>

struct UnitFrameRectangle {
    int x;
    int y;
    int width;
    int height;
};

struct UnitFrameLayout {
    UnitFrameRectangle src;
    UnitFrameRectangle dest;
};

inline UnitFrameLayout calculateUnitFrameLayout(
    int classicWidth,
    int classicHeight,
    int hdWidth,
    int hdHeight,
    int texturePixelWidth,
    int textureDensity,
    int column,
    int row,
    UnitFrameRectangle visual,
    float zoom,
    float visualScale)
{
    if (hdWidth > 0 && hdHeight > 0 && texturePixelWidth == 8 * hdWidth) {
        int fw = hdWidth / textureDensity;
        int fh = hdHeight / textureDensity;
        int originalWidth = static_cast<int>(std::lround(fw * zoom));
        int W = static_cast<int>(std::lround(originalWidth * visualScale));
        int originalHeight = static_cast<int>(std::lround(fh * zoom));
        int H = static_cast<int>(std::lround(originalHeight * visualScale));
        return {
            {column * fw, row * fh, fw, fh},
            {
                visual.x - (W - visual.width) / 2,
                visual.y - (H - visual.height) / 2,
                W,
                H
            }
        };
    }

    return {
        {column * classicWidth, row * classicHeight, classicWidth, classicHeight},
        visual
    };
}
