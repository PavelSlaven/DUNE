#include "cCreditsState.h"

#include "d2tmc.h"
#include "config.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "utils/Localization.hpp"
#include "include/Texture.hpp"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include <SDL2/SDL.h>
#include <algorithm>
#include <iostream>

cCreditsState::cCreditsState(cGame &theGame, GameContext* ctx) :
    cGameState(theGame, ctx),
    m_moveSpeed(0.15f),
    m_textDrawer(m_game.isHdGraphicsActive()
        ? ctx->getTextContext()->getMenuTextDrawer()
        : ctx->getTextContext()->getBeneTextDrawer())
{
    auto *gfxinter = ctx->getGraphicsContext()->gfxinter.get();
    if (m_game.isHdGraphicsActive()) {
        m_teamBmp = loadHdUiTexture(
            "credits_team.png",
            m_game.getGraphicsDensity(),
            "HD credits team photo"
        );
        m_titleBmp = loadHdUiTexture(
            "credits_title.png",
            m_game.getGraphicsDensity(),
            "HD credits title"
        );
        m_ownsTeamBmp = m_teamBmp != nullptr;
        m_ownsTitleBmp = m_titleBmp != nullptr;
    }
    if (!m_teamBmp) {
        m_teamBmp = gfxinter->getTexture(CREDITS_DUNE2_CORE_TEAM);
    }
    if (!m_titleBmp) {
        m_titleBmp = gfxinter->getTexture(D2TM_TITLE);
    }
    const int teamAtTheRight = m_game.m_screenW - (m_teamBmp->w * 1.1f);
    const int teamAlmostAtBottom = m_game.m_screenH - (m_teamBmp->h * 1.1f);
    m_teamCoordinates = cPoint(teamAtTheRight, teamAlmostAtBottom);

    int titleWidth = m_titleBmp->w;
    m_titleHeight = m_titleBmp->h;

    int centerOfScreen = m_game.m_screenW / 2;

    m_titleX = centerOfScreen - (titleWidth / 2);
    resetCrawler();

    const bool hdLayout = m_game.isHdGraphicsActive();
    const int backButtonWidth = hdLayout
        ? std::max(140, m_textDrawer->getTextLength(
            localization::text("BACK", "НАЗАД")) + 24)
        : m_textDrawer->getTextLength(
            localization::text(" BACK", " НАЗАД"));
    const int backButtonHeight = hdLayout
        ? std::max(36, m_textDrawer->getFontHeight() + 10)
        : 21;
    const int backButtonY = m_game.m_screenH - backButtonHeight;
    const int backButtonX = 0;
    cRectangle backButtonRect(backButtonX, backButtonY, backButtonWidth, backButtonHeight);
    backButton = GuiButtonBuilder()
            .withRect(backButtonRect)
            .withLabel(localization::text("BACK", "НАЗАД"))
            .withTextDrawer(m_textDrawer)
            .withTheme(hdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(hdLayout
                ? GuiRenderKind::REMASTER_BUTTON
                : GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .onClick([this]() {
                m_game.setNextStateToTransitionTo(GAME_MENU);
                m_game.initiateFadingOut();
            })
            .build();

    m_lines = std::vector<s_CreditLine>();
    prepareCrawlerLines();
}

void cCreditsState::prepareCrawlerLines()
{
    Color colorHeadlines = Color::green();

    int fontHeightWithALittlePadding = m_textDrawer->getFontHeight() + 4;
    int spacerAfterHeadline = fontHeightWithALittlePadding + m_textDrawer->getFontHeight();
    auto spacer = s_CreditLine {
        .name = "",
        .txt = "",
        .color = Color::black(),
        .height = 40
    };

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = std::format("Version {}", D2TM_VERSION),
        .color = Color::yellow(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "by Stefan Hendriks",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(spacer);
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "a remake of",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "Dune 2 - The Building of a Dynasty (by Westwood Studios)",
        .color = Color::red(),
        .height = spacerAfterHeadline
    });

    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "--- CONTRIBUTORS ---",
        .color = colorHeadlines,
        .height = spacerAfterHeadline,
    });
    m_lines.push_back(s_CreditLine {
        .name = "Paul",
        .txt = "Developer",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Arjen",
        .txt = "Developer & Sparring partner",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
        m_lines.push_back(s_CreditLine {
        .name = "Mira",
        .txt = "Developer",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Rozmy",
        .txt = "Graphics",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Nema Fakei",
        .txt = "Graphics",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Vidiware",
        .txt = "Graphics",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Timenn",
        .txt = "Graphics",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "MrFlibble",
        .txt = "Graphics",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Ripps",
        .txt = "Support at Discord, testing & Skirmish Maps",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Bruno",
        .txt = "For your lifelong support & valuable feedback",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });

    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "--- ACKNOWLEDGEMENTS ---",
        .color = colorHeadlines,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Westwood Studios",
        .txt = "for producing Dune 2",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Allegro",
        .txt = "by Shawn Hargreaves (et al)",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "AlFONT",
        .txt = "by Javier Gonzalez",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "Dune Legacy, Dune Dynasty and Dune The Golden Path",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });

    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "--- KO-FI SUPPORTERS ---",
        .color = colorHeadlines,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Fedaygin",
        .txt = "",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Morto",
        .txt = "",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "The General",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Bastian",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Florian",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Aleksandar",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Bruno",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Dan Greene",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Sergio Muad'Dib",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "saif3r",
        .txt = "",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "--- SPECIAL THANKS TO ---",
        .color = colorHeadlines,
        .height = spacerAfterHeadline
    });
    m_lines.push_back(s_CreditLine {
        .name = "Gobalopper",
        .txt = "for Dune2K, and hosting arrakis.dune2k.com",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Jpexs",
        .txt = "for help with the Dune 2 Seed Generator",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Rene",
        .txt = "for the D2TM Java Map Editor",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Mira",
        .txt = "for porting D2TM to SDL2",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Guillaume Lavoie",
        .txt = "",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Dennis Stansert",
        .txt = "",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Ash",
        .txt = "",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Ruurd Nijdam",
        .txt = "",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "rphl",
        .txt = "",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Non sono Mandrake",
        .txt = "for nudging me to work on D2TM again in C++",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });
    m_lines.push_back(s_CreditLine {
        .name = "Dune2k.com",
        .txt = "For all the good times at the arrakis forums",
        .color = Color::white(),
        .height = fontHeightWithALittlePadding
    });

    // spacer
    // and finally a thank you for the player
    m_lines.push_back(spacer);

    m_lines.push_back(s_CreditLine {
        .name = "",
        .txt = "Thank you for playing",
        .color = Color::white(),
        .height = spacerAfterHeadline
    });
}

void cCreditsState::resetCrawler()
{
    m_crawlerY = m_game.m_screenH + 1;
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
    renderDrawer->renderSprite(m_teamBmp, m_teamCoordinates.x, m_teamCoordinates.y);

    int halfScreen = m_game.m_screenW / 2;

    // draw crawler
    renderDrawer->renderSprite(m_titleBmp, m_titleX, m_crawlerY);
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

    // MOUSE
    m_game.getMouse()->draw();
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
    if (event.isType(eKeyEventType::PRESSED) && event.hasKey(SDL_SCANCODE_ESCAPE)) {
        m_game.setNextStateToTransitionTo(GAME_MENU);
        m_game.initiateFadingOut();
    }
}
