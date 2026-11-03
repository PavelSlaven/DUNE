#include "UnitFrameFixture.hpp"

#include "d2tmc.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <format>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
struct PixelBounds {
    int left = 0;
    int top = 0;
    int right = -1;
    int bottom = -1;
    int count = 0;
};

struct Pixel {
    Uint8 r;
    Uint8 g;
    Uint8 b;
    Uint8 a;
};

void require(bool condition, const std::string &message)
{
    if (!condition) throw std::runtime_error(message);
}

PixelBounds alphaBounds(const std::vector<Uint32> &pixels, int width, int height, SDL_PixelFormat *format)
{
    PixelBounds bounds;
    bounds.left = width;
    bounds.top = height;
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            Uint8 red, green, blue, alpha;
            SDL_GetRGBA(pixels[static_cast<std::size_t>(y * width + x)], format,
                        &red, &green, &blue, &alpha);
            if (alpha < 128) continue;
            bounds.left = std::min(bounds.left, x);
            bounds.top = std::min(bounds.top, y);
            bounds.right = std::max(bounds.right, x);
            bounds.bottom = std::max(bounds.bottom, y);
            ++bounds.count;
        }
    }
    if (bounds.count == 0) {
        bounds.left = 0;
        bounds.top = 0;
    }
    return bounds;
}

Pixel pixelAt(const std::vector<Uint32> &pixels, int width, int x, int y, SDL_PixelFormat *format)
{
    Uint8 red, green, blue, alpha;
    SDL_GetRGBA(pixels[static_cast<std::size_t>(y * width + x)], format,
                &red, &green, &blue, &alpha);
    return {red, green, blue, alpha};
}

std::string boundsText(const PixelBounds &bounds)
{
    return std::format("({},{}..{},{}; pixels={})", bounds.left, bounds.top,
                       bounds.right, bounds.bottom, bounds.count);
}

PixelBounds renderSiegeAtScale(
    UnitFrameFixture &fixture,
    int worldScalePercent,
    float zoom,
    std::vector<std::string> &failures)
{
    constexpr int posX = 256;
    constexpr int posY = 256;
    const std::string label = std::format("ws={}% z={}", worldScalePercent, zoom);
    fixture.setDisplaySettings(4, worldScalePercent);
    fixture.setCamera(zoom);
    fixture.setUnit(0, SIEGETANK, posX, posY, 2, 2, 0);
    fixture.setUnitFlags(0, false, false);
    sUnitInfo[SIEGETANK].shadow = nullptr;
    fixture.setTurretTexture(SIEGETANK, nullptr);
    require(fixture.siegeSurface() != nullptr, "Synthetic Siege atlas surface is missing");
    require(fixture.siegeHouseTexture() != nullptr,
            "Graphics::getHouseTexture failed to prepare the synthetic Siege body and mask");

    const int outputWidth = 800;
    const int outputHeight = 600;
    SDL_Texture *target = SDL_CreateTexture(
        fixture.renderer(), SDL_PIXELFORMAT_RGBA32, SDL_TEXTUREACCESS_TARGET,
        outputWidth, outputHeight
    );
    require(target != nullptr, std::format("SDL_CreateTexture target: {}", SDL_GetError()));
    SDL_SetTextureBlendMode(target, SDL_BLENDMODE_NONE);
    require(SDL_SetRenderTarget(fixture.renderer(), target) == 0,
            std::format("SDL_SetRenderTarget: {}", SDL_GetError()));
    SDL_SetRenderDrawBlendMode(fixture.renderer(), SDL_BLENDMODE_NONE);
    SDL_SetRenderDrawColor(fixture.renderer(), 0, 0, 0, 0);
    require(SDL_RenderClear(fixture.renderer()) == 0,
            std::format("SDL_RenderClear: {}", SDL_GetError()));
    unit[0].draw();

    std::vector<Uint32> pixels(static_cast<std::size_t>(outputWidth * outputHeight));
    require(SDL_RenderReadPixels(
                fixture.renderer(), nullptr, SDL_PIXELFORMAT_RGBA32,
                pixels.data(), outputWidth * static_cast<int>(sizeof(Uint32))) == 0,
            std::format("SDL_RenderReadPixels: {}", SDL_GetError()));
    SDL_SetRenderTarget(fixture.renderer(), nullptr);
    SDL_DestroyTexture(target);

    std::unique_ptr<SDL_PixelFormat, decltype(&SDL_FreeFormat)> format(
        SDL_AllocFormat(SDL_PIXELFORMAT_RGBA32), SDL_FreeFormat
    );
    require(format != nullptr, std::format("SDL_AllocFormat: {}", SDL_GetError()));
    const PixelBounds actual = alphaBounds(pixels, outputWidth, outputHeight, format.get());
    const int drawX = static_cast<int>(std::round(zoom * (posX + (32 - 36) / 2)));
    const int drawY = static_cast<int>(std::round(zoom * (posY + (32 - 36) / 2) + 40));
    const int originalWidth = static_cast<int>(std::lround(zoom * 36));
    const int expectedSize = static_cast<int>(std::lround(44 * zoom));
    const int expectedX = static_cast<int>(std::lround(drawX + (originalWidth - expectedSize) / 2.0F));
    const int expectedY = static_cast<int>(std::lround(drawY + (originalWidth - expectedSize) / 2.0F));
    const int expectedRight = expectedX + expectedSize - 1;
    const int expectedBottom = expectedY + expectedSize - 1;
    const bool bboxMatches = actual.count > 0 && std::abs(actual.left - expectedX) <= 1 &&
        std::abs(actual.top - expectedY) <= 1 &&
        std::abs(actual.right - expectedRight) <= 1 &&
        std::abs(actual.bottom - expectedBottom) <= 1;
    if (!bboxMatches) {
        failures.push_back(std::format(
            "{}: alpha bbox {} expected ({},{}..{},{}), expected draw dest size {}",
            label, boundsText(actual), expectedX, expectedY, expectedRight, expectedBottom, expectedSize
        ));
    }

    const Pixel topEdge = pixelAt(pixels, outputWidth, expectedX + expectedSize / 2,
                                  expectedY + 2, format.get());
    const Pixel bottomEdge = pixelAt(pixels, outputWidth, expectedX + expectedSize / 2,
                                     expectedBottom - 2, format.get());
    const Pixel leftEdge = pixelAt(pixels, outputWidth, expectedX + 2,
                                   expectedY + expectedSize / 2, format.get());
    const Pixel rightEdge = pixelAt(pixels, outputWidth, expectedRight - 2,
                                    expectedY + expectedSize / 2, format.get());
    const bool boundaryMarkersMatch = !(topEdge.a < 128 || topEdge.r < 180 || topEdge.g > 80 || topEdge.b > 80 ||
        bottomEdge.a < 128 || bottomEdge.b < 180 || bottomEdge.r > 80 || bottomEdge.g > 80 ||
        leftEdge.a < 128 || leftEdge.r < 180 || leftEdge.g < 180 || leftEdge.b > 80 ||
        rightEdge.a < 128 || rightEdge.g < 180 || rightEdge.b < 180 || rightEdge.r > 80);
    std::cout << std::format("{}: own-frame boundary markers: {}\n", label, boundaryMarkersMatch ? "PASS" : "FAIL");
    if (!boundaryMarkersMatch) {
        failures.push_back(std::format(
            "{}: own-frame boundary markers are absent or crossed (top={},{},{},{} bottom={},{},{},{} left={},{},{},{} right={},{},{},{})",
            label,
            topEdge.r, topEdge.g, topEdge.b, topEdge.a,
            bottomEdge.r, bottomEdge.g, bottomEdge.b, bottomEdge.a,
            leftEdge.r, leftEdge.g, leftEdge.b, leftEdge.a,
            rightEdge.r, rightEdge.g, rightEdge.b, rightEdge.a
        ));
    }

    bool neighborColorInsideDestination = false;
    for (int y = std::max(0, expectedY); y <= std::min(outputHeight - 1, expectedBottom); ++y) {
        for (int x = std::max(0, expectedX); x <= std::min(outputWidth - 1, expectedRight); ++x) {
            const Pixel sample = pixelAt(pixels, outputWidth, x, y, format.get());
            if (sample.a >= 128 && sample.g > 180 && sample.g > sample.r * 1.5F &&
                sample.g > sample.b * 1.5F) {
                neighborColorInsideDestination = true;
            }
        }
    }
    std::cout << std::format("{}: neighboring frame marker: {}\n", label, neighborColorInsideDestination ? "FAIL" : "PASS");
    if (neighborColorInsideDestination) {
        failures.push_back(std::format("{}: neighboring frame's green marker entered the destination", label));
    }

    const int outsideX = std::min(outputWidth - 1, expectedRight + 2);
    const Pixel outside = pixelAt(pixels, outputWidth, outsideX, expectedY + expectedSize / 2, format.get());
    std::cout << std::format("{}: leakage beyond destination: {}\n", label, outside.a >= 128 ? "FAIL" : "PASS");
    if (outside.a >= 128) {
        failures.push_back(std::format("{}: a neighboring atlas marker leaked beyond the destination", label));
    }

    const int markerX = expectedX + static_cast<int>(std::lround(32.0F / 4.0F * zoom));
    const int markerY = expectedY + static_cast<int>(std::lround(32.0F / 4.0F * zoom));
    const Pixel houseMarker = pixelAt(pixels, outputWidth, markerX, markerY, format.get());
    const bool houseColorMatches = houseMarker.a >= 128 && houseMarker.r > houseMarker.g && houseMarker.r > houseMarker.b;
    std::cout << std::format("{}: House color marker: {}\n", label, houseColorMatches ? "PASS" : "FAIL");
    if (!houseColorMatches) {
        failures.push_back(std::format(
            "{}: masked marker is not tinted with the House color (rgba={},{},{},{})",
            label, houseMarker.r, houseMarker.g, houseMarker.b, houseMarker.a
        ));
    }
    return actual;
}

bool sameBounds(const PixelBounds &first, const PixelBounds &second)
{
    return first.left == second.left && first.top == second.top &&
        first.right == second.right && first.bottom == second.bottom &&
        first.count == second.count;
}

void runPixelChecks()
{
    UnitFrameFixture fixture(4, 100);
    std::vector<std::string> failures;
    const PixelBounds atHundred = renderSiegeAtScale(fixture, 100, 1.0F, failures);
    const PixelBounds scaledWorldSameZoom = renderSiegeAtScale(fixture, 125, 1.0F, failures);
    if (!sameBounds(atHundred, scaledWorldSameZoom)) {
        failures.push_back(std::format(
            "world scale 125% at zoom 1.0 changed the drawn bounds: {} vs {} at 100%",
            boundsText(scaledWorldSameZoom), boundsText(atHundred)
        ));
    }
    const PixelBounds zoomedHundred = renderSiegeAtScale(fixture, 100, 1.25F, failures);
    const PixelBounds zoomedScaled = renderSiegeAtScale(fixture, 125, 1.25F, failures);
    if (!sameBounds(zoomedHundred, zoomedScaled)) {
        failures.push_back(std::format(
            "world scale 125% at zoom 1.25 changed the drawn bounds: {} vs {} at 100%",
            boundsText(zoomedScaled), boundsText(zoomedHundred)
        ));
    }
    if (!failures.empty()) {
        std::string message = "synthetic SDL draw/readback failed semantically:";
        for (const std::string &failure : failures) {
            message += "\n  " + failure;
        }
        throw std::runtime_error(message);
    }
}
}

int main()
{
    try {
        runPixelChecks();
        std::cout << "unit_render_pixels: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "unit_render_pixels: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
