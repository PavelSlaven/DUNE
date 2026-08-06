#define SDL_MAIN_HANDLED

#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"

#include <SDL2/SDL.h>

#include <array>
#include <iostream>

namespace {
bool sameRect(const SDL_Rect &left, const SDL_Rect &right)
{
    return left.x == right.x &&
           left.y == right.y &&
           left.w == right.w &&
           left.h == right.h;
}

bool sameScale(float leftX, float leftY, float rightX, float rightY)
{
    constexpr float epsilon = 0.0001F;
    return SDL_fabsf(leftX - rightX) < epsilon &&
           SDL_fabsf(leftY - rightY) < epsilon;
}
}

int main()
{
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, "software");
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cerr << "SDL_Init: " << SDL_GetError() << '\n';
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow(
        "render target state test",
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        640,
        480,
        SDL_WINDOW_HIDDEN
    );
    SDL_Renderer *renderer = window
        ? SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE)
        : nullptr;
    if (!renderer) {
        std::cerr << "SDL renderer: " << SDL_GetError() << '\n';
        if (window) {
            SDL_DestroyWindow(window);
        }
        SDL_Quit();
        return 1;
    }

    SDLDrawer drawer(renderer);
    Texture *frame = drawer.createRenderTargetTexture(5120, 1440);
    Texture *minimap = drawer.createRenderTargetTexture(64, 64);
    Texture *alphaTarget = drawer.createRenderTargetTexture(8, 8);

    drawer.beginDrawingToTexture(frame);
    SDL_RenderSetLogicalSize(renderer, 3413, 960);
    const SDL_Rect expectedClip{3053, 42, 360, 918};
    SDL_RenderSetClipRect(renderer, &expectedClip);
    SDL_Rect expectedViewport{};
    SDL_RenderGetViewport(renderer, &expectedViewport);
    float expectedScaleX = 0.0F;
    float expectedScaleY = 0.0F;
    SDL_RenderGetScale(renderer, &expectedScaleX, &expectedScaleY);

    drawer.beginDrawingToTexture(minimap);
    drawer.renderClearToColor(Color{255, 0, 0, 255});
    drawer.clearRectToTransparent(cRectangle(16, 16, 32, 32));

    std::array<Uint32, 64 * 64> pixels{};
    const bool readbackSucceeded = SDL_RenderReadPixels(
        renderer,
        nullptr,
        SDL_PIXELFORMAT_RGBA8888,
        pixels.data(),
        64 * static_cast<int>(sizeof(Uint32))
    ) == 0;
    SDL_PixelFormat *pixelFormat = SDL_AllocFormat(SDL_PIXELFORMAT_RGBA8888);
    Uint8 outerR = 0;
    Uint8 outerG = 0;
    Uint8 outerB = 0;
    Uint8 outerA = 0;
    Uint8 openingR = 0;
    Uint8 openingG = 0;
    Uint8 openingB = 0;
    Uint8 openingA = 0;
    if (readbackSucceeded && pixelFormat) {
        SDL_GetRGBA(pixels[0], pixelFormat, &outerR, &outerG, &outerB, &outerA);
        SDL_GetRGBA(pixels[32 * 64 + 32], pixelFormat, &openingR, &openingG, &openingB, &openingA);
    }
    SDL_FreeFormat(pixelFormat);
    const bool transparentOpening =
        readbackSucceeded &&
        outerR == 255 && outerG == 0 && outerB == 0 && outerA == 255 &&
        openingA == 0;
    drawer.endDrawingToTexture();

    drawer.beginDrawingToTexture(alphaTarget);
    drawer.renderClearToColor(Color{255, 255, 255, 255});
    drawer.renderRectFillColor(cRectangle(0, 0, 8, 8), Color{5, 24, 48, 38});

    Uint32 alphaPixel = 0;
    const SDL_Rect alphaReadRect{4, 4, 1, 1};
    const bool alphaReadbackSucceeded = SDL_RenderReadPixels(
        renderer,
        &alphaReadRect,
        SDL_PIXELFORMAT_RGBA8888,
        &alphaPixel,
        static_cast<int>(sizeof(Uint32))
    ) == 0;
    SDL_PixelFormat *alphaPixelFormat = SDL_AllocFormat(SDL_PIXELFORMAT_RGBA8888);
    Uint8 filteredR = 0;
    Uint8 filteredG = 0;
    Uint8 filteredB = 0;
    Uint8 filteredA = 0;
    if (alphaReadbackSucceeded && alphaPixelFormat) {
        SDL_GetRGBA(alphaPixel, alphaPixelFormat, &filteredR, &filteredG, &filteredB, &filteredA);
    }
    SDL_FreeFormat(alphaPixelFormat);
    const bool colorAlphaApplied =
        alphaReadbackSucceeded &&
        filteredR > 5 && filteredG > 24 && filteredB > 48 && filteredA == 255;
    drawer.endDrawingToTexture();

    SDL_Rect restoredViewport{};
    SDL_RenderGetViewport(renderer, &restoredViewport);
    float restoredScaleX = 0.0F;
    float restoredScaleY = 0.0F;
    SDL_RenderGetScale(renderer, &restoredScaleX, &restoredScaleY);
    SDL_Rect restoredClip{};
    SDL_RenderGetClipRect(renderer, &restoredClip);

    const bool viewportRestored = sameRect(expectedViewport, restoredViewport);
    const bool scaleRestored = sameScale(
        expectedScaleX,
        expectedScaleY,
        restoredScaleX,
        restoredScaleY
    );
    const bool clipRestored =
        SDL_RenderIsClipEnabled(renderer) == SDL_TRUE &&
        sameRect(expectedClip, restoredClip);
    if (!viewportRestored || !scaleRestored || !clipRestored || !transparentOpening || !colorAlphaApplied) {
        std::cerr
            << "nested render target corrupted gameplay presentation state\n"
            << "viewport expected "
            << expectedViewport.x << ',' << expectedViewport.y << ' '
            << expectedViewport.w << 'x' << expectedViewport.h
            << ", got "
            << restoredViewport.x << ',' << restoredViewport.y << ' '
            << restoredViewport.w << 'x' << restoredViewport.h << '\n'
            << "scale expected " << expectedScaleX << 'x' << expectedScaleY
            << ", got " << restoredScaleX << 'x' << restoredScaleY << '\n'
            << "clip expected "
            << expectedClip.x << ',' << expectedClip.y << ' '
            << expectedClip.w << 'x' << expectedClip.h
            << ", got "
            << restoredClip.x << ',' << restoredClip.y << ' '
            << restoredClip.w << 'x' << restoredClip.h << '\n';
        if (!transparentOpening) {
            std::cerr
                << "transparent render-target opening failed: outer rgba "
                << static_cast<int>(outerR) << ','
                << static_cast<int>(outerG) << ','
                << static_cast<int>(outerB) << ','
                << static_cast<int>(outerA)
                << ", opening alpha " << static_cast<int>(openingA) << '\n';
        }
        if (!colorAlphaApplied) {
            std::cerr
                << "rectangle Color alpha was ignored: rgba "
                << static_cast<int>(filteredR) << ','
                << static_cast<int>(filteredG) << ','
                << static_cast<int>(filteredB) << ','
                << static_cast<int>(filteredA) << '\n';
        }
    }

    drawer.endDrawingToTexture();
    delete alphaTarget;
    delete minimap;
    delete frame;
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return viewportRestored && scaleRestored && clipRestored && transparentOpening && colorAlphaApplied ? 0 : 1;
}
