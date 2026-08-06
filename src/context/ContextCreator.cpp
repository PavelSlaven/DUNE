#include "context/ContextCreator.hpp"
#include "utils/Graphics.hpp"
#include "utils/cLog.h"
#include "utils/cFileValidator.h"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "drawers/cTextDrawer.h"
#include "utils/Localization.hpp"

#include <algorithm>
#include <filesystem>

ContextCreator::ContextCreator(
    SDL_Renderer *renderer,
    cFileValidator *settingsValidator,
    int assetDensity)
    : density(std::max(1, assetDensity))
{
    // 
    // loading all datapacks
    //
    gfxmentat = std::make_shared<Graphics>(
        renderer,
        settingsValidator->getFullName(eGameDirFileName::GFXMENTAT),
        density
    );
    if (gfxmentat == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load datafile:" + settingsValidator->getName(eGameDirFileName::GFXMENTAT), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", "Hooked datafile: " + settingsValidator->getName(eGameDirFileName::GFXMENTAT), OUTC_SUCCESS);
    }

    gfxworld = std::make_shared<Graphics>(
        renderer,
        settingsValidator->getFullName(eGameDirFileName::GFXWORLD),
        density
    );
    if (gfxworld == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load datafile:" + settingsValidator->getName(eGameDirFileName::GFXWORLD), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", "Hooked datafile: " + settingsValidator->getName(eGameDirFileName::GFXWORLD), OUTC_SUCCESS);
    }

    gfxinter = std::make_shared<Graphics>(
        renderer,
        settingsValidator->getFullName(eGameDirFileName::GFXINTER),
        density
    );
    if (gfxinter == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load datafile:" + settingsValidator->getName(eGameDirFileName::GFXINTER), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", "Hooked datafile: " + settingsValidator->getName(eGameDirFileName::GFXINTER), OUTC_SUCCESS);
    }

    gfxdata = std::make_shared<Graphics>(
        renderer,
        settingsValidator->getFullName(eGameDirFileName::GFXDATA),
        density
    );
    if (gfxdata == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load datafile:" + settingsValidator->getName(eGameDirFileName::GFXDATA), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", "Hooked datafile: " + settingsValidator->getName(eGameDirFileName::GFXDATA), OUTC_SUCCESS);
    }

    //
    // loading all fonts
    //
    const auto gameFontFallback = std::filesystem::path(
        settingsValidator->getFullName(eGameDirFileName::ARRAKEEN)
    );
    const auto beneFontFallback = std::filesystem::path(
        settingsValidator->getFullName(eGameDirFileName::BENEGESS)
    );
    const auto smallFontFallback = std::filesystem::path(
        settingsValidator->getFullName(eGameDirFileName::SMALL)
    );
    const auto fontDirectory = beneFontFallback.parent_path();
    const auto russianFontPath = fontDirectory / "Sangyo-Regular.otf";
    const auto russoFontPath = fontDirectory / "RussoOne-Regular.ttf";
    const bool useRussianFont = !localization::isEnglish() &&
        std::filesystem::is_regular_file(russianFontPath);

    const auto openLocalizedFont = [this, useRussianFont, &russianFontPath](
        const std::filesystem::path &fallback,
        int pointSize,
        const char *role,
        TTF_Font *&fallbackFont) {
        fallbackFont = nullptr;
        const std::filesystem::path primary = useRussianFont
            ? russianFontPath
            : fallback;
        TTF_Font *font = TTF_OpenFont(
            primary.string().c_str(),
            pointSize * density
        );
        if (!font && primary != fallback) {
            cLogger::getInstance()->log(
                LOG_WARN,
                COMP_INIT,
                "Load data",
                std::string("Could not load Sangyo for ") + role +
                    "; using the configured fallback",
                OUTC_FAILED
            );
            font = TTF_OpenFont(
                fallback.string().c_str(),
                pointSize * density
            );
        }
        else if (font && primary != fallback) {
            fallbackFont = TTF_OpenFont(
                fallback.string().c_str(),
                pointSize * density
            );
            if (!fallbackFont) {
                cLogger::getInstance()->log(
                    LOG_WARN,
                    COMP_INIT,
                    "Load data",
                    std::string("Could not load the symbol fallback for ") + role,
                    OUTC_FAILED
                );
            }
        }
        return font;
    };

    game_font = openLocalizedFont(
        gameFontFallback, 12, "game text", game_fallback_font
    );
    if (game_font == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load font:" + settingsValidator->getName(eGameDirFileName::ARRAKEEN), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", useRussianFont ? "Hooked game font: Sangyo-Regular.otf" : "Hooked font: " + settingsValidator->getName(eGameDirFileName::ARRAKEEN), OUTC_SUCCESS);
    }  

    bene_font = openLocalizedFont(
        beneFontFallback, 12, "dialog text", bene_fallback_font
    );
    if (bene_font == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load font:" + settingsValidator->getName(eGameDirFileName::BENEGESS), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", useRussianFont ? "Hooked dialog font: Sangyo-Regular.otf" : "Hooked font: " + settingsValidator->getName(eGameDirFileName::BENEGESS), OUTC_SUCCESS);
    }  

    small_font = openLocalizedFont(
        smallFontFallback, 12, "small UI text", small_fallback_font
    );
    if (small_font == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load font:" + settingsValidator->getName(eGameDirFileName::SMALL), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", useRussianFont ? "Hooked small UI font: Sangyo-Regular.otf" : "Hooked font: " + settingsValidator->getName(eGameDirFileName::SMALL), OUTC_SUCCESS);
    }

    menu_font = openLocalizedFont(
        beneFontFallback, 24, "menu text", menu_fallback_font
    );
    if (menu_font == nullptr) {
        cLogger::getInstance()->log(
            LOG_ERROR,
            COMP_INIT,
            "Load data",
            "Could not load configured HD menu font",
            OUTC_FAILED
        );
    }
    else {
        cLogger::getInstance()->log(
            LOG_INFO,
            COMP_INIT,
            "Load data",
            useRussianFont
                ? "Hooked HD menu font: Sangyo-Regular.otf"
                : "Hooked HD menu font: " + settingsValidator->getName(eGameDirFileName::BENEGESS),
            OUTC_SUCCESS
        );
    }

    mentat_hd_font = openLocalizedFont(
        russoFontPath, 20, "Mentat text", mentat_hd_fallback_font
    );
    if (mentat_hd_font == nullptr) {
        cLogger::getInstance()->log(
            LOG_WARN,
            COMP_INIT,
            "Load data",
            "Could not load remastered Mentat font; using configured Bene Gesserit font",
            OUTC_FAILED
        );
        mentat_hd_font = TTF_OpenFont(
            settingsValidator->getFullName(eGameDirFileName::BENEGESS).c_str(),
            20 * density
        );
    }
    else {
        cLogger::getInstance()->log(
            LOG_INFO,
            COMP_INIT,
            "Load data",
            useRussianFont
                ? "Hooked remastered Mentat font: Sangyo-Regular.otf"
                : "Hooked remastered Mentat font: RussoOne-Regular.ttf",
            OUTC_SUCCESS
        );
    }
}

ContextCreator::~ContextCreator()
{
    TTF_CloseFont(game_font);
    TTF_CloseFont(bene_font);
    TTF_CloseFont(small_font);
    TTF_CloseFont(menu_font);
    TTF_CloseFont(mentat_hd_font);
    if (game_fallback_font) TTF_CloseFont(game_fallback_font);
    if (bene_fallback_font) TTF_CloseFont(bene_fallback_font);
    if (small_fallback_font) TTF_CloseFont(small_fallback_font);
    if (menu_fallback_font) TTF_CloseFont(menu_fallback_font);
    if (mentat_hd_fallback_font) TTF_CloseFont(mentat_hd_fallback_font);
}

std::unique_ptr<GraphicsContext> ContextCreator::createGraphicsContext()
{
    auto gtx = std::make_unique<GraphicsContext>();
    gtx->gfxmentat = gfxmentat;
    gtx->gfxworld = gfxworld;
    gtx->gfxinter = gfxinter;
    gtx->gfxdata = gfxdata;
    return gtx;
}

std::unique_ptr<TextContext> ContextCreator::createTextContext() {
    return std::make_unique<TextContext>(
        std::make_unique<cTextDrawer>(small_font, density, small_fallback_font),
        std::make_unique<cTextDrawer>(
            small_fallback_font ? small_fallback_font : small_font,
            density
        ),
        std::make_unique<cTextDrawer>(bene_font, density, bene_fallback_font),
        std::make_unique<cTextDrawer>(game_font, density, game_fallback_font),
        std::make_unique<cTextDrawer>(menu_font, density, menu_fallback_font),
        std::make_unique<cTextDrawer>(mentat_hd_font, density, mentat_hd_fallback_font)
    );
}
