/**
 * @file ContextCreator.cpp
 *
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 *
 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
 *
 * This is a non-commercial educational project.
 */

#include "context/ContextCreator.hpp"
#include "utils/Graphics.hpp"
#include "utils/Log.h"
#include "utils/cFileValidator.h"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "drawers/cTextDrawer.h"
#include "drawers/SDLDrawer.hpp"
#include "game/cGameSettings.h"

#include "include/cAssert.h"

#include <filesystem>

namespace {
constexpr float kGameFontSize = 16.0F;
constexpr float kBeneFontSize = 14.0F;
constexpr float kSmallFontSize = 12.0F;
}

ContextCreator::ContextCreator(SDL_Renderer *renderer, cFileValidator *settingsValidator)
{
    d2tm_assert(renderer!=nullptr);
    d2tm_assert(settingsValidator!=nullptr);
    //
    // loading all datapacks
    //
    gfxmentat = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXMENTAT), kHd4AssetDensity);
    if (gfxmentat == nullptr) {
        Logger::error(COMP_INIT, "Load data", "Could not hook/load datafile: {}", settingsValidator->getName(eGameDirFileName::GFXMENTAT));
    }
    else {
        Logger::info(COMP_INIT, "Load data", "Hooked datafile: {}", settingsValidator->getName(eGameDirFileName::GFXMENTAT));
    }

    gfxworld = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXWORLD), kHd4AssetDensity);
    if (gfxworld == nullptr) {
        Logger::error(COMP_INIT, "Load data", "Could not hook/load datafile: {}", settingsValidator->getName(eGameDirFileName::GFXWORLD));
    }
    else {
        Logger::info(COMP_INIT, "Load data", "Hooked datafile: {}", settingsValidator->getName(eGameDirFileName::GFXWORLD));
    }

    gfxinter = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXINTER), kHd4AssetDensity);
    if (gfxinter == nullptr) {
        Logger::error(COMP_INIT, "Load data", "Could not hook/load datafile: {}", settingsValidator->getName(eGameDirFileName::GFXINTER));
    }
    else {
        Logger::info(COMP_INIT, "Load data", "Hooked datafile: {}", settingsValidator->getName(eGameDirFileName::GFXINTER));
    }

    gfxdata = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXDATA), kHd4AssetDensity);
    if (gfxdata == nullptr) {
        Logger::error(COMP_INIT, "Load data", "Could not hook/load datafile: {}", settingsValidator->getName(eGameDirFileName::GFXDATA));
    }
    else {
        Logger::info(COMP_INIT, "Load data", "Hooked datafile: {}", settingsValidator->getName(eGameDirFileName::GFXDATA));
    }

    gfxeditor = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXEDITOR));
    if (gfxeditor == nullptr) {
        Logger::error(COMP_INIT, "Load data", "Could not hook/load datafile: {}", settingsValidator->getName(eGameDirFileName::GFXEDITOR));
    }
    else {
        Logger::info(COMP_INIT, "Load data", "Hooked datafile: {}", settingsValidator->getName(eGameDirFileName::GFXEDITOR));
    }

    //
    // loading all fonts
    //
    const auto fontDirectory = std::filesystem::path(
        settingsValidator->getFullName(eGameDirFileName::BENEGESS)).parent_path();
    const auto openFont = [settingsValidator](eGameDirFileName configuredFont, float size) {
        const auto fontPath = std::filesystem::path(settingsValidator->getFullName(configuredFont));
        TTF_Font *font = TTF_OpenFont(fontPath.string().c_str(), size);
        if (!font) {
            Logger::error(COMP_INIT, "Load data", "Could not hook/load font: {}", fontPath.filename().string());
        } else {
            Logger::info(COMP_INIT, "Load data", "Hooked font: {}", fontPath.filename().string());
        }
        return font;
    };
    game_font = openFont(eGameDirFileName::ARRAKEEN, kGameFontSize);
    bene_font = openFont(eGameDirFileName::BENEGESS, kBeneFontSize);
    small_font = openFont(eGameDirFileName::SMALL, kSmallFontSize);

    const auto fallbackFontPath = fontDirectory / "PTMono-Regular.ttf";
    const auto openFallbackFont = [&fallbackFontPath](TTF_Font *font, float size) {
        TTF_Font *fallback = TTF_OpenFont(fallbackFontPath.string().c_str(), size);
        if (!fallback) {
            Logger::warn(COMP_INIT, "Load data", "Could not hook/load fallback font: PTMono-Regular.ttf");
        } else {
            if (font && !TTF_AddFallbackFont(font, fallback)) {
                Logger::warn(COMP_INIT, "Load data", "Could not attach fallback font: PTMono-Regular.ttf: {}", SDL_GetError());
            }
            Logger::info(COMP_INIT, "Load data", "Hooked fallback font: PTMono-Regular.ttf");
        }
        return fallback;
    };
    game_fallback_font = openFallbackFont(game_font, kGameFontSize);
    bene_fallback_font = openFallbackFont(bene_font, kBeneFontSize);
    small_fallback_font = openFallbackFont(small_font, kSmallFontSize);
}

ContextCreator::~ContextCreator()
{
    TTF_CloseFont(game_font);
    TTF_CloseFont(bene_font);
    TTF_CloseFont(small_font);
    if (game_fallback_font) TTF_CloseFont(game_fallback_font);
    if (bene_fallback_font) TTF_CloseFont(bene_fallback_font);
    if (small_fallback_font) TTF_CloseFont(small_fallback_font);
}

std::unique_ptr<GraphicsContext> ContextCreator::createGraphicsContext()
{
    auto gtx = std::make_unique<GraphicsContext>();
    gtx->gfxmentat = gfxmentat;
    gtx->gfxworld = gfxworld;
    gtx->gfxinter = gfxinter;
    gtx->gfxdata = gfxdata;
    gtx->gfxeditor = gfxeditor;
    return gtx;
}

std::unique_ptr<TextContext> ContextCreator::createTextContext(cGameSettings *settings, SDLDrawer *renderer) {
    return std::make_unique<TextContext>(
        std::make_unique<cTextDrawer>(small_font, small_fallback_font, kSmallFontSize, settings, renderer),
        std::make_unique<cTextDrawer>(bene_font, bene_fallback_font, kBeneFontSize, settings, renderer),
        std::make_unique<cTextDrawer>(game_font, game_fallback_font, kGameFontSize, settings, renderer)
    );
}
