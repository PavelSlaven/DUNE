#include "cScreenInit.h"

#include "cLog.h"
#include "RenderScale.hpp"

#include <SDL2/SDL.h>
#include <format>

#include <algorithm>
#include <cmath>

void cScreenInit::setFullScreenMode()
{
    SDL_SetWindowFullscreen(window, SDL_WINDOW_FULLSCREEN_DESKTOP);
    SDL_RenderSetLogicalSize(renderer, renderResolution.width, renderResolution.height);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
    cLogger::getInstance()->log(LOG_INFO, COMP_SDL2, "desktop", "Fullscreen desktop");
    // Affiche la taille réelle du rendu
    int renderW, renderH;
    SDL_GetRendererOutputSize(renderer, &renderW, &renderH);
    cLogger::getInstance()->log(LOG_INFO, COMP_SDL2, "desktop", std::format("Renderer output size : {}x{}",renderW,renderH));
    // Affiche le DPI
    float ddpi, hdpi, vdpi;
    if (SDL_GetDisplayDPI(0, &ddpi, &hdpi, &vdpi) == 0) {
        cLogger::getInstance()->log(LOG_INFO, COMP_SDL2, "DPI", std::format("DPI : {}, (H: {},V: {})",ddpi,hdpi,vdpi));
    } else {
        cLogger::getInstance()->log(LOG_ERROR, COMP_SDL2, "DPI", SDL_GetError());
    }
}

void cScreenInit::setWindowMode()
{
    const DisplayResolution windowedSize = getWindowedSize();
    SDL_SetWindowFullscreen(window, 0);
    SDL_SetWindowSize(window, windowedSize.width, windowedSize.height);
    SDL_SetWindowPosition(window, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED);
    SDL_RenderSetLogicalSize(renderer, renderResolution.width, renderResolution.height);
    cLogger::getInstance()->log(
        LOG_INFO,
        COMP_SDL2,
        "desktop",
        std::format("Windowed desktop : {}x{}", windowedSize.width, windowedSize.height)
    );
}

void cScreenInit::getWindowResolution()
{
    SDL_DisplayMode mode{};
    windowResolution = {800, 600};
    if (SDL_GetCurrentDisplayMode(0, &mode) == 0) {
        cLogger::getInstance()->log(LOG_INFO, COMP_SDL2, "desktop", std::format("Resolution screen : {}x{}",mode.w,mode.h));
        windowResolution.width = mode.w;
        windowResolution.height = mode.h;
    }
}

void cScreenInit::adaptResolution(
    int desiredWidth,
    int desiredHeight,
    int renderScalePercent)
{
    auto logger = cLogger::getInstance();
    outputResolution = {
        std::max(desiredWidth, MinimumRenderWidth),
        std::max(desiredHeight, MinimumRenderHeight)
    };

    int selectedScale = renderScalePercent;
    if (selectedScale != AutomaticRenderScale &&
        !isManualRenderScaleAvailable(
            outputResolution.width,
            outputResolution.height,
            selectedScale)) {
        logger->log(
            LOG_WARN,
            COMP_SDL2,
            "Render scale",
            std::format(
                "{}% is unavailable for {}x{}; using Auto",
                selectedScale,
                outputResolution.width,
                outputResolution.height
            )
        );
        selectedScale = AutomaticRenderScale;
    }

    const RenderCanvasSize canvas = calculateRenderCanvasSize(
        outputResolution.width,
        outputResolution.height,
        selectedScale
    );
    renderResolution = {canvas.width, canvas.height};

    logger->log(
        LOG_INFO,
        COMP_SDL2,
        "Resolution",
        std::format("Desired output : {}x{}", desiredWidth, desiredHeight)
    );
    logger->log(
        LOG_INFO,
        COMP_SDL2,
        "Render scale",
        selectedScale == AutomaticRenderScale
            ? std::format(
                "Auto ({}%)",
                calculateAutomaticRenderScalePercent(
                    outputResolution.width,
                    outputResolution.height
                )
            )
            : std::format("{}%", selectedScale)
    );
    logger->log(
        LOG_INFO,
        COMP_SDL2,
        "Resolution",
        std::format("Adopted logical canvas : {}x{}", renderResolution.width, renderResolution.height)
    );
}

DisplayResolution cScreenInit::getWindowedSize() const
{
    SDL_Rect usableBounds{};
    int availableWidth = windowResolution.width;
    int availableHeight = windowResolution.height;
    if (SDL_GetDisplayUsableBounds(0, &usableBounds) == 0) {
        availableWidth = usableBounds.w;
        availableHeight = usableBounds.h;
    }

    const double fitScale = std::min({
        1.0,
        static_cast<double>(availableWidth) / outputResolution.width,
        static_cast<double>(availableHeight) / outputResolution.height
    });
    return {
        std::max(1, static_cast<int>(std::lround(outputResolution.width * fitScale))),
        std::max(1, static_cast<int>(std::lround(outputResolution.height * fitScale)))
    };
}

cScreenInit::cScreenInit(
    int desiredWidth,
    int desiredHeight,
    int renderScalePercent,
    const std::string &title)
{
    this->getWindowResolution();
    this->adaptResolution(desiredWidth, desiredHeight, renderScalePercent);
    const DisplayResolution windowedSize = getWindowedSize();

    auto logger = cLogger::getInstance();

    window = SDL_CreateWindow(
        title.c_str(),
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        windowedSize.width,
        windowedSize.height,
        SDL_WINDOW_ALLOW_HIGHDPI
    );
    if (window == nullptr) {
        const auto msg = std::format("Failed initialized screen with resolution {}x{}", renderResolution.width, renderResolution.height);
        logger->log(LOG_ERROR, COMP_SDL2, "Screen init", msg, OUTC_FAILED);
        SDL_Quit();
        return;
    }
    else {
        const auto msg = std::format("Successfully initialized screen with resolution {}x{}.", renderResolution.width, renderResolution.height);
        //std::cout << msg << std::endl;
        logger->log(LOG_INFO, COMP_SDL2, "Screen init", msg, OUTC_SUCCESS);
    }

    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "0");
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (renderer == nullptr) {
        const auto msg = std::format("Failed initialized renderer with resolution {}x{}", renderResolution.width, renderResolution.height);
        logger->log(LOG_ERROR, COMP_SDL2, "Renderer init", msg, OUTC_FAILED);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return;
    }
    else {
        const auto msg = std::format("Successfully initialized renderer");
        logger->log(LOG_INFO, COMP_SDL2, "Renderer init", msg, OUTC_SUCCESS);
    }

    SDL_SetWindowFullscreen(window, 0);
    SDL_SetWindowSize(window, windowedSize.width, windowedSize.height);
    SDL_SetWindowPosition(window, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED);
    SDL_RenderSetLogicalSize(renderer, renderResolution.width, renderResolution.height);
}
