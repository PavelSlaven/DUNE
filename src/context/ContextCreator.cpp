#include "context/ContextCreator.hpp"
#include "utils/Graphics.hpp"
#include "utils/cLog.h"
#include "utils/cFileValidator.h"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "drawers/cTextDrawer.h"

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
    game_font = TTF_OpenFont(
        settingsValidator->getFullName(eGameDirFileName::ARRAKEEN).c_str(),
        12 * density
    );
    if (game_font == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load font:" + settingsValidator->getName(eGameDirFileName::ARRAKEEN), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", "Hooked font: " + settingsValidator->getName(eGameDirFileName::ARRAKEEN), OUTC_SUCCESS);
    }  

    bene_font = TTF_OpenFont(
        settingsValidator->getFullName(eGameDirFileName::BENEGESS).c_str(),
        12 * density
    );
    if (bene_font == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load font:" + settingsValidator->getName(eGameDirFileName::BENEGESS), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", "Hooked font: " + settingsValidator->getName(eGameDirFileName::BENEGESS), OUTC_SUCCESS);
    }  

    small_font = TTF_OpenFont(
        settingsValidator->getFullName(eGameDirFileName::SMALL).c_str(),
        12 * density
    );
    if (small_font == nullptr) {
        cLogger::getInstance()->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load font:" + settingsValidator->getName(eGameDirFileName::SMALL), OUTC_FAILED);
    }
    else {
        cLogger::getInstance()->log(LOG_INFO, COMP_INIT, "Load data", "Hooked font: " + settingsValidator->getName(eGameDirFileName::SMALL), OUTC_SUCCESS);
    }

    const auto fontDirectory = std::filesystem::path(
        settingsValidator->getFullName(eGameDirFileName::BENEGESS)
    ).parent_path();
    const auto russoFontPath = fontDirectory / "RussoOne-Regular.ttf";

    menu_font = TTF_OpenFont(
        settingsValidator->getFullName(eGameDirFileName::BENEGESS).c_str(),
        18 * density
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
            "Hooked HD menu font: " + settingsValidator->getName(eGameDirFileName::BENEGESS),
            OUTC_SUCCESS
        );
    }

    const auto mentatFontPath = russoFontPath;
    mentat_hd_font = TTF_OpenFont(mentatFontPath.string().c_str(), 20 * density);
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
            "Hooked remastered Mentat font: RussoOne-Regular.ttf",
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
        std::make_unique<cTextDrawer>(small_font, density),
        std::make_unique<cTextDrawer>(bene_font, density),
        std::make_unique<cTextDrawer>(game_font, density),
        std::make_unique<cTextDrawer>(menu_font, density),
        std::make_unique<cTextDrawer>(mentat_hd_font, density)
    );
}
