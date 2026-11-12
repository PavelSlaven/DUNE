/**
 * @file cCreditsState.cpp
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

#include "cCreditsState.h"
#include "game/cGameSettings.h"

#include "controls/eKeyAction.h"
#include "config.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "include/Texture.hpp"
#include "drawers/cTextDrawer.h"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include "game/GameStateTransition.hpp"
#include "controls/cMouse.h"
#include "utils/HdUiTextureLoader.hpp"

#include "include/cAssert.h"
#include "context/TextContext.hpp"
#include "include/sGameServices.h"
#include "include/eGameState.h"
#include "debug/UiAudit.hpp"
#include "utils/Localization.hpp"

#include <algorithm>

cCreditsState::cCreditsState(sGameServices* services) :
    cGameState(services),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_settings(services->settings),
    m_stateTransitions(services->stateTransitions),
    m_mouse(services->mouse),
    m_moveSpeed(0.15f)
{
    d2tm_assert(m_textDrawer != nullptr);
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    auto *gfxinter = m_ctx->getGraphicsContext()->gfxinter.get();
    d2tm_assert(gfxinter != nullptr);

    m_teamBmp = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "credits_team.png",
        "HD credits team photo");
    m_titleBmp = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "credits_title.png",
        "HD credits title");
    m_ownsTeamBmp = m_teamBmp != nullptr;
    m_ownsTitleBmp = m_titleBmp != nullptr;
    if (!m_teamBmp) {
        m_teamBmp = gfxinter->getTexture(CREDITS_DUNE2_CORE_TEAM);
    }
    if (!m_titleBmp) {
        m_titleBmp = gfxinter->getTexture(D2TM_TITLE);
    }
    const int teamAtTheRight = m_settings->getScreenW() - (m_teamBmp->w * 1.1f);
    const int teamAlmostAtBottom = m_settings->getScreenH() - (m_teamBmp->h * 1.1f);
    m_teamCoordinates = cPoint(teamAtTheRight, teamAlmostAtBottom);

    int titleWidth = m_titleBmp->w;
    m_titleHeight = m_titleBmp->h;

    int centerOfScreen = m_settings->getScreenW() / 2;

    m_titleX = centerOfScreen - (titleWidth / 2);
    resetCrawler();

    const int backButtonWidth = std::max(140, m_textDrawer->getTextLength(localization::text("Back", "Назад")) + 24);
    const int backButtonHeight = std::max(36, m_textDrawer->getFontHeight() + 10);
    const int backButtonY = m_settings->getScreenH() - backButtonHeight;
    const int backButtonX = 0;
    cRectangle backButtonRect(backButtonX, backButtonY, backButtonWidth, backButtonHeight);
    backButton = GuiButtonBuilder()
            .withRect(backButtonRect)
            .withLabel(localization::text("Back", "Назад"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(GuiTheme::Remaster())
            .withKind(GuiRenderKind::REMASTER_BUTTON)
            .onClick([this]() {
                m_stateTransitions->setNextStateWithFade(GAME_MENU);
            })
            .build();

    m_lines = std::vector<s_CreditLine>();
    prepareCrawlerLines();
}

void cCreditsState::prepareCrawlerLines()
{
    Color colorHeadlines = Color::Green;

    int fontHeightWithALittlePadding = m_textDrawer->getFontHeight() + 4;
    int spacerAfterHeadline = fontHeightWithALittlePadding + m_textDrawer->getFontHeight();
    auto spacer = s_CreditLine {
        .name = "",
        .txt = "",
        .color = Color::Black,
        .height = 40
    };

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::format("Version {}", "Версия {}", D2TM_VERSION),
        .color = Color::Yellow,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("by Stefan Hendriks", "автор — Stefan Hendriks"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(spacer);
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("a remake of", "ремейк игры"),
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "Dune 2 - The Building of a Dynasty (by Westwood Studios)",
        .color = Color::Red,
        .height = spacerAfterHeadline
    });

    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("--- CONTRIBUTORS ---", "--- УЧАСТНИКИ ---"),
        .color = colorHeadlines,
        .height = spacerAfterHeadline,
    });
    m_lines.push_back(s_CreditLine {
        .name = "Paul",
        .txt = localization::text("Developer", "Разработчик"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Arjen",
        .txt = localization::text("Developer & Sparring partner", "Разработчик и спарринг-партнёр"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
        m_lines.push_back(s_CreditLine {
        .name = "Mira",
        .txt = localization::text("Developer", "Разработчик"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Matt Van Horn",
        .txt = localization::text("Bugfixes", "Исправление ошибок"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Rozmy",
        .txt = localization::text("Graphics", "Графика"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Nema Fakei",
        .txt = localization::text("Graphics", "Графика"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Vidiware",
        .txt = localization::text("Graphics", "Графика"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Timenn",
        .txt = localization::text("Graphics", "Графика"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "MrFlibble",
        .txt = localization::text("Graphics", "Графика"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Ravenborn",
        .txt = localization::text("Internal Editor UI graphics and miscellaneous assets", "Графика редактора и другие ресурсы"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Ripps",
        .txt = localization::text("Support at Discord, testing & Skirmish Maps", "Поддержка в Discord, тестирование и карты схваток"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Bruno",
        .txt = localization::text("For your lifelong support & valuable feedback", "За многолетнюю поддержку и ценные отзывы"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });

    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("--- ACKNOWLEDGEMENTS ---", "--- БЛАГОДАРНОСТИ ---"),
        .color = colorHeadlines,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Westwood Studios",
        .txt = localization::text("for producing Dune 2", "за создание Dune 2"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "SDL3",
        .txt = localization::text("by Sam Lantinga and contributors", "Sam Lantinga и соавторы"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("with SDL_image, SDL_ttf and SDL_mixer", "с SDL_image, SDL_ttf и SDL_mixer"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("Dune Legacy, Dune Dynasty and Dune The Golden Path", "Dune Legacy, Dune Dynasty и Dune The Golden Path"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });

    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("--- KO-FI SUPPORTERS ---", "--- ПОДДЕРЖКА НА KO-FI ---"),
        .color = colorHeadlines,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Fedaygin",
        .txt = "",
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Morto",
        .txt = "",
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "The General",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Bastian",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Florian",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Aleksandar",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Bruno",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Dan Greene",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Sergio Muad'Dib",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "saif3r",
        .txt = "",
        .color = Color::White,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("--- SPECIAL THANKS TO ---", "--- ОСОБАЯ БЛАГОДАРНОСТЬ ---"),
        .color = colorHeadlines,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Gobalopper",
        .txt = localization::text("for Dune2K, and hosting arrakis.dune2k.com", "за Dune2K и сайт arrakis.dune2k.com"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Jpexs",
        .txt = localization::text("for help with the Dune 2 Seed Generator", "за помощь с генератором карт Dune 2"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Rene",
        .txt = localization::text("for the D2TM Java Map Editor", "за редактор карт D2TM на Java"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Mira",
        .txt = localization::text("for porting D2TM to SDL2", "за перенос D2TM на SDL2"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Guillaume Lavoie",
        .txt = "",
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Dennis Stansert",
        .txt = "",
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Ash",
        .txt = "",
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Ruurd Nijdam",
        .txt = "",
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "rphl",
        .txt = "",
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Non sono Mandrake",
        .txt = localization::text("for nudging me to work on D2TM again in C++", "за то, что вернул меня к D2TM на C++"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Dune2k.com",
        .txt = localization::text("For all the good times at the arrakis forums", "За хорошие времена на форумах arrakis"),
        .color = Color::White,
        .height = fontHeightWithALittlePadding
    });

    // spacer
    // and finally a thank you for the player
    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = localization::text("Thank you for playing", "Спасибо за игру"),
        .color = Color::White,
        .height = spacerAfterHeadline
    });
}

void cCreditsState::resetCrawler()
{
    m_crawlerY = m_settings->getScreenH() + 1;
}

cCreditsState::~cCreditsState()
{
    if (m_ownsTeamBmp) {
        delete m_teamBmp;
    }
    if (m_ownsTitleBmp) {
        delete m_titleBmp;
    }
    m_teamBmp = nullptr;
    m_titleBmp = nullptr;
}

void cCreditsState::thinkFast()
{
    m_crawlerY -= m_moveSpeed;

    int textCrawlY = m_crawlerY + m_titleHeight;
    for (auto &line : m_lines) {
        textCrawlY += line.height;
    }

    if (textCrawlY < 0) {
        resetCrawler();
    }
}

void cCreditsState::draw() const
{
    if (uiaudit::isEnabled()) {
        uiaudit::recordCanvasClick("credits-speed-up");
    }

    m_sdlDrawer->renderSprite(m_teamBmp, m_teamCoordinates.x, m_teamCoordinates.y);

    int halfScreen = m_settings->getScreenW() / 2;

    // draw crawler
    m_sdlDrawer->renderSprite(m_titleBmp, m_titleX, m_crawlerY);
    int textCrawlY = m_crawlerY + m_titleHeight;
    for (auto &line : m_lines) {
        if (line.name.empty()) {
            m_textDrawer->drawTextCentered(line.txt.c_str(), textCrawlY, line.color);
        }
        else if (line.txt.empty()) {
            m_textDrawer->drawTextCentered(line.name.c_str(), textCrawlY, line.color);
        }
        else {
            int spaceBetween = 4;
            // both name and line given, then we render them differently.
            m_textDrawer->drawText(halfScreen+spaceBetween, textCrawlY, line.txt.c_str());
            int widthOfName = m_textDrawer->getTextLength(line.name.c_str());
            m_textDrawer->drawText(halfScreen - (widthOfName + spaceBetween), textCrawlY, line.name.c_str());
        }
        textCrawlY += line.height;
    }

    backButton->draw();
    m_mouse->draw();
}

void cCreditsState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    backButton->onNotifyMouseEvent(event);

    if (event.eventType == eMouseEventType::MOUSE_LEFT_BUTTON_PRESSED) {
        m_moveSpeed = 1.0f; // speed up
    }
    else if (event.eventType == eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED) {
        m_moveSpeed = 0.15f; // restore
    }
}

eGameStateType cCreditsState::getType()
{
    return GAMESTATE_CREDITS;
}

void cCreditsState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (event.isType(eKeyEventType::PRESSED) && event.isAction(eKeyAction::MENU_BACK)) {
        m_stateTransitions->setNextStateWithFade(GAME_MENU);
    }
}
