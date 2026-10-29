#include "utils/UnitFrameLayout.hpp"

#include <array>
#include <iostream>

namespace {
struct FrameInput {
    int classicWidth;
    int classicHeight;
    int hdWidth;
    int hdHeight;
    int texturePixelWidth;
    int textureDensity;
    int column;
    int row;
    UnitFrameRectangle visual;
    float zoom;
    float visualScale;
};

struct Presentation {
    float zoom;
    float visualScale;
    UnitFrameRectangle visual;
    UnitFrameRectangle expectedDest;
};

bool equal(UnitFrameRectangle actual, UnitFrameRectangle expected)
{
    return actual.x == expected.x && actual.y == expected.y &&
           actual.width == expected.width && actual.height == expected.height;
}

std::ostream &operator<<(std::ostream &stream, UnitFrameRectangle rectangle)
{
    return stream << '{' << rectangle.x << ',' << rectangle.y << ','
                  << rectangle.width << ',' << rectangle.height << '}';
}

int checks = 0;
int failures = 0;

void check(int caseNumber, const FrameInput &input, UnitFrameLayout expected)
{
    ++checks;
    const UnitFrameLayout actual = calculateUnitFrameLayout(
        input.classicWidth, input.classicHeight, input.hdWidth, input.hdHeight,
        input.texturePixelWidth, input.textureDensity, input.column, input.row,
        input.visual, input.zoom, input.visualScale
    );
    if (equal(actual.src, expected.src) && equal(actual.dest, expected.dest)) {
        return;
    }
    ++failures;
    std::cerr << "FAIL U" << caseNumber
              << " input classic=" << input.classicWidth << 'x' << input.classicHeight
              << " hd=" << input.hdWidth << 'x' << input.hdHeight
              << " pixelW=" << input.texturePixelWidth
              << " density=" << input.textureDensity
              << " column=" << input.column << " row=" << input.row
              << " visual=" << input.visual << " zoom=" << input.zoom
              << " visualScale=" << input.visualScale
              << " got src=" << actual.src << " dest=" << actual.dest
              << " expected src=" << expected.src << " dest=" << expected.dest
              << '\n';
}

void checkLegacy(
    int caseNumber, int classicWidth, int classicHeight, int hdWidth, int hdHeight,
    int texturePixelWidth, int textureDensity, int column, int row,
    UnitFrameRectangle expectedSrc)
{
    const std::array<Presentation, 2> presentations{{
        {1.0F, 1.0F, {100, 200, classicWidth, classicHeight},
         {100, 200, classicWidth, classicHeight}},
        {1.3F, 1.25F, {94, 194, 59, 59}, {94, 194, 59, 59}}
    }};
    for (const auto &presentation : presentations) {
        check(caseNumber, {
            classicWidth, classicHeight, hdWidth, hdHeight,
            texturePixelWidth, textureDensity, column, row,
            presentation.visual, presentation.zoom, presentation.visualScale
        }, {expectedSrc, presentation.expectedDest});
    }
}
}

int main()
{
    for (int column = 0; column < 8; ++column) {
        check(1, {36, 36, 176, 176, 1408, 4, column, 0,
                  {100, 200, 36, 36}, 1.0F, 1.0F},
              {{44 * column, 0, 44, 44}, {96, 196, 44, 44}});
    }

    constexpr std::array<Presentation, 32> grid{{
        {0.25F, 1.0F, {100, 200, 9, 9}, {99, 199, 11, 11}},
        {0.25F, 1.1F, {100, 200, 10, 10}, {99, 199, 12, 12}},
        {0.25F, 1.25F, {100, 200, 11, 11}, {99, 199, 14, 14}},
        {0.25F, 1.5F, {100, 200, 14, 14}, {99, 199, 17, 17}},
        {0.5F, 1.0F, {100, 200, 18, 18}, {98, 198, 22, 22}},
        {0.5F, 1.1F, {100, 200, 20, 20}, {98, 198, 24, 24}},
        {0.5F, 1.25F, {100, 200, 23, 23}, {98, 198, 28, 28}},
        {0.5F, 1.5F, {100, 200, 27, 27}, {97, 197, 33, 33}},
        {1.0F, 1.0F, {100, 200, 36, 36}, {96, 196, 44, 44}},
        {1.0F, 1.1F, {100, 200, 40, 40}, {96, 196, 48, 48}},
        {1.0F, 1.25F, {100, 200, 45, 45}, {95, 195, 55, 55}},
        {1.0F, 1.5F, {100, 200, 54, 54}, {94, 194, 66, 66}},
        {1.5F, 1.0F, {100, 200, 54, 54}, {94, 194, 66, 66}},
        {1.5F, 1.1F, {100, 200, 59, 59}, {93, 193, 73, 73}},
        {1.5F, 1.25F, {100, 200, 68, 68}, {93, 193, 83, 83}},
        {1.5F, 1.5F, {100, 200, 81, 81}, {91, 191, 99, 99}},
        {2.0F, 1.0F, {100, 200, 72, 72}, {92, 192, 88, 88}},
        {2.0F, 1.1F, {100, 200, 79, 79}, {91, 191, 97, 97}},
        {2.0F, 1.25F, {100, 200, 90, 90}, {90, 190, 110, 110}},
        {2.0F, 1.5F, {100, 200, 108, 108}, {88, 188, 132, 132}},
        {4.0F, 1.0F, {100, 200, 144, 144}, {84, 184, 176, 176}},
        {4.0F, 1.1F, {100, 200, 158, 158}, {82, 182, 194, 194}},
        {4.0F, 1.25F, {100, 200, 180, 180}, {80, 180, 220, 220}},
        {4.0F, 1.5F, {100, 200, 216, 216}, {76, 176, 264, 264}},
        {0.3F, 1.0F, {100, 200, 11, 11}, {99, 199, 13, 13}},
        {0.3F, 1.1F, {100, 200, 12, 12}, {99, 199, 14, 14}},
        {0.3F, 1.25F, {100, 200, 14, 14}, {99, 199, 16, 16}},
        {0.3F, 1.5F, {100, 200, 17, 17}, {99, 199, 20, 20}},
        {1.3F, 1.0F, {100, 200, 47, 47}, {95, 195, 57, 57}},
        {1.3F, 1.1F, {100, 200, 52, 52}, {95, 195, 63, 63}},
        {1.3F, 1.25F, {100, 200, 59, 59}, {94, 194, 71, 71}},
        {1.3F, 1.5F, {100, 200, 71, 71}, {93, 193, 86, 86}}
    }};
    for (const auto &presentation : grid) {
        check(2, {36, 36, 176, 176, 1408, 4, 3, 0,
                  presentation.visual, presentation.zoom, presentation.visualScale},
              {{132, 0, 44, 44}, presentation.expectedDest});
    }

    for (int column = 0; column < 8; ++column) {
        checkLegacy(3, 36, 36, 176, 176, 288, 1, column, 0,
                    {36 * column, 0, 36, 36});
        checkLegacy(4, 36, 36, 176, 176, 1152, 4, column, 0,
                    {36 * column, 0, 36, 36});
        checkLegacy(5, 36, 36, 176, 176, 1412, 4, column, 0,
                    {36 * column, 0, 36, 36});
        checkLegacy(6, 36, 36, 176, 0, 1408, 4, column, 0,
                    {36 * column, 0, 36, 36});
        checkLegacy(6, 36, 36, 0, 176, 1408, 4, column, 0,
                    {36 * column, 0, 36, 36});
        checkLegacy(7, 38, 46, 0, 0, 1216, 4, column, 0,
                    {38 * column, 0, 38, 46});
        checkLegacy(8, 48, 48, 0, 0, 1536, 4, column, 1,
                    {48 * column, 48, 48, 48});
        for (int row = 0; row < 4; ++row) {
            checkLegacy(9, 80, 52, 0, 0, 640, 1, column, row,
                        {80 * column, 52 * row, 80, 52});
            checkLegacy(9, 80, 52, 0, 0, 2560, 4, column, row,
                        {80 * column, 52 * row, 80, 52});
        }
        for (int row = 0; row < 2; ++row) {
            check(10, {38, 46, 160, 192, 1280, 4, column, row,
                       {100, 200, 38, 46}, 1.0F, 1.0F},
                  {{40 * column, 48 * row, 40, 48}, {99, 199, 40, 48}});
            check(10, {38, 46, 160, 192, 1280, 4, column, row,
                       {100, 200, 61, 75}, 1.3F, 1.25F},
                  {{40 * column, 48 * row, 40, 48}, {98, 199, 65, 78}});
        }
    }

    std::cout << "UnitFrameLayout checks=" << checks << " failures=" << failures << '\n';
    return failures == 0 ? 0 : 1;
}
