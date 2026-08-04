#define SDL_MAIN_HANDLED

#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"

#include <SDL2/SDL.h>

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
    if (!viewportRestored || !scaleRestored || !clipRestored) {
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
    }

    drawer.endDrawingToTexture();
    delete minimap;
    delete frame;
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return viewportRestored && scaleRestored && clipRestored ? 0 : 1;
}
