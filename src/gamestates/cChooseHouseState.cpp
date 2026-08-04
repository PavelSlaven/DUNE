#include "gamestates/cChooseHouseState.h"

#include "d2tmc.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/cSoundPlayer.h"
#include "utils/Graphics.hpp"
#include <SDL2/SDL.h>
#include "include/Texture.hpp"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include <algorithm>

#include "data/gfxaudio.h"
#include "utils/HdUiTextureLoader.hpp"
#include "utils/Localization.hpp"

cChooseHouseState::cChooseHouseState(cGame &theGame, GameContext* ctx) :
    cGameState(theGame, ctx),
    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
{
    m_hdLayout = m_game.isHdGraphicsActive();
    m_textDrawer = m_hdLayout
        ? ctx->getTextContext()->getMenuTextDrawer()
        : ctx->getTextContext()->getBeneTextDrawer();

    bmp_Dune = m_gfxinter->getTexture(BMP_GAME_DUNE);

    int duneAtTheRight = m_game.m_screenW - bmp_Dune->w;
    int duneAlmostAtBottom = m_game.m_screenH - (bmp_Dune->h * 0.90);
    coords_Dune = cPoint(duneAtTheRight, duneAlmostAtBottom);

    bmp_SelectYourHouseTitle = m_gfxinter->getTexture(BMP_SELECT_YOUR_HOUSE);

    selectYourHouseXCentered = (m_game.m_screenW / 2) - bmp_SelectYourHouseTitle->w / 2;
    coords_SelectYourHouseTitle = cPoint(selectYourHouseXCentered, 0);

    bmp_HouseAtreides = m_gfxinter->getTexture(BMP_SELECT_HOUSE_ATREIDES);
    bmp_HouseOrdos = m_gfxinter->getTexture(BMP_SELECT_HOUSE_ORDOS);
    bmp_HouseHarkonnen = m_gfxinter->getTexture(BMP_SELECT_HOUSE_HARKONNEN);

    if (m_hdLayout) {
        m_hdBackground = loadHdUiTexture(
            "main_menu_background.png",
            m_game.getGraphicsDensity(),
            "HD house selection"
        );

        const int gap = std::clamp(m_game.m_screenW / 48, 16, 32);
        const int horizontalMargin = std::clamp(
            m_game.m_screenW / 24,
            28,
            72
        );
        const int availableCardWidth = (
            m_game.m_screenW - horizontalMargin * 2 - gap * 2
        ) / 3;
        const int cardWidth = std::clamp(
            availableCardWidth,
            220,
            420
        );
        const int cardsY = std::clamp(m_game.m_screenH / 6, 96, 150);
        const int backWidth = 240;
        const int backHeight = 46;
        const int backY = m_game.m_screenH - backHeight - 18;
        const int availableCardHeight = backY - cardsY - 26;
        const int preferredCardHeight = std::clamp(
            m_game.m_screenH * 3 / 5,
            320,
            520
        );
        const int cardHeight = std::max(
            280,
            std::min(preferredCardHeight, availableCardHeight)
        );
        const int cardsWidth = cardWidth * 3 + gap * 2;
        const int firstX = (m_game.m_screenW - cardsWidth) / 2;

        houseAtreides = cRectangle(firstX, cardsY, cardWidth, cardHeight);
        houseOrdos = cRectangle(
            firstX + cardWidth + gap,
            cardsY,
            cardWidth,
            cardHeight
        );
        houseHarkonnen = cRectangle(
            firstX + (cardWidth + gap) * 2,
            cardsY,
            cardWidth,
            cardHeight
        );

        backButtonRect = new cRectangle(
            (m_game.m_screenW - backWidth) / 2,
            backY,
            backWidth,
            backHeight
        );
    }
    else {
        backButtonRect = m_textDrawer->getAsRectangle(
            0,
            m_game.m_screenH - m_textDrawer->getFontHeight(),
            localization::text(" BACK", " НАЗАД")
        );
        int selectYourHouseY = m_game.m_screenH * 0.25f;
        int columnWidth = m_game.m_screenW / 7;
        int offset = (columnWidth / 2) - (bmp_HouseAtreides->w / 2);

        houseAtreides = cRectangle((columnWidth * 1) + offset, selectYourHouseY, 90, 98);
        houseOrdos = cRectangle((columnWidth * 3) + offset, selectYourHouseY, 90, 98);
        houseHarkonnen = cRectangle((columnWidth * 5) + offset, selectYourHouseY, 90, 98);
    }

    hoversOverBackButton = false;
}

cChooseHouseState::~cChooseHouseState()
{
    delete backButtonRect;
    delete m_hdBackground;

    // not owner of these
    bmp_Dune = nullptr;
    bmp_SelectYourHouseTitle = nullptr;
    bmp_HouseAtreides = nullptr;
    bmp_HouseOrdos = nullptr;
    bmp_HouseHarkonnen = nullptr;
}

void cChooseHouseState::thinkFast()
{

}

void cChooseHouseState::draw() const
{
    cMouse *mouse = m_game.getMouse();

    if (m_hdLayout) {
        drawHdBackground();

        const std::string title = localization::text(
            "CHOOSE YOUR HOUSE", "ВЫБЕРИТЕ СВОЙ ДОМ");
        const int titleWidth = m_textDrawer->getTextLength(title);
        m_textDrawer->drawText(
            (m_game.m_screenW - titleWidth) / 2,
            48,
            Color{231, 190, 91, 255},
            title
        );

        drawHdHouseCard(
            houseAtreides,
            bmp_HouseAtreides,
            localization::text("ATREIDES", "АТРЕЙДЕС"),
            m_hoveredHouse == ATREIDES
        );
        drawHdHouseCard(
            houseOrdos,
            bmp_HouseOrdos,
            localization::text("ORDOS", "ОРДОС"),
            m_hoveredHouse == ORDOS
        );
        drawHdHouseCard(
            houseHarkonnen,
            bmp_HouseHarkonnen,
            localization::text("HARKONNEN", "ХАРКОННЕН"),
            m_hoveredHouse == HARKONNEN
        );

        const Color backFill = hoversOverBackButton
            ? Color{43, 49, 53, 245}
            : Color{25, 31, 35, 245};
        renderDrawer->renderRectFillColor(*backButtonRect, backFill);
        renderDrawer->renderRectColor(
            *backButtonRect,
            Color{195, 142, 43, 255}
        );
        const std::string backLabel = localization::text("BACK", "НАЗАД");
        const int backLabelWidth = m_textDrawer->getTextLength(backLabel);
        m_textDrawer->drawText(
            backButtonRect->getX() +
                (backButtonRect->getWidth() - backLabelWidth) / 2,
            backButtonRect->getY() +
                (backButtonRect->getHeight() -
                 m_textDrawer->getFontHeight()) / 2,
            hoversOverBackButton
                ? Color{255, 224, 139, 255}
                : Color{238, 229, 204, 255},
            backLabel
        );

        mouse->draw();
        return;
    }

    // Render the planet Dune a bit downward
    renderDrawer->renderSprite(bmp_Dune, coords_Dune.x, coords_Dune.y);

    // HOUSES
    renderDrawer->renderSprite(bmp_SelectYourHouseTitle, coords_SelectYourHouseTitle.x, coords_SelectYourHouseTitle.y);

    renderDrawer->renderSprite(bmp_HouseAtreides, houseAtreides.getX(), houseAtreides.getY());
    renderDrawer->renderSprite(bmp_HouseOrdos, houseOrdos.getX(), houseOrdos.getY());
    renderDrawer->renderSprite(bmp_HouseHarkonnen, houseHarkonnen.getX(),houseOrdos.getY());

    // BACK (bottom right
    // TODO: Use actual cGuiButton
    Color color = hoversOverBackButton ? Color{255, 0, 0,255} : Color{255, 255, 255,255};
    m_textDrawer->drawText(
        backButtonRect->getTopLeft(), color,
        localization::text(" BACK", " НАЗАД"));

    // MOUSE
    mouse->draw();
}

void cChooseHouseState::drawHdBackground() const
{
    renderDrawer->renderClearToColor(Color{10, 12, 13, 255});
    if (!m_hdBackground) {
        return;
    }

    const float sourceAspect =
        static_cast<float>(m_hdBackground->w) /
        std::max(1, m_hdBackground->h);
    const float screenAspect =
        static_cast<float>(m_game.m_screenW) /
        std::max(1, m_game.m_screenH);
    cRectangle destination;
    if (sourceAspect > screenAspect) {
        const int width = static_cast<int>(
            m_game.m_screenH * sourceAspect
        );
        destination = cRectangle(
            (m_game.m_screenW - width) / 2,
            0,
            width,
            m_game.m_screenH
        );
    }
    else {
        const int height = static_cast<int>(
            m_game.m_screenW / sourceAspect
        );
        destination = cRectangle(
            0,
            (m_game.m_screenH - height) / 2,
            m_game.m_screenW,
            height
        );
    }
    renderDrawer->renderStrechFullSprite(m_hdBackground, destination);
    renderDrawer->renderRectFillColor(
        0,
        0,
        m_game.m_screenW,
        m_game.m_screenH,
        Color{3, 6, 8, 142}
    );
}

void cChooseHouseState::drawHdHouseCard(
    const cRectangle &card,
    Texture *emblem,
    const std::string &name,
    bool hovered) const
{
    const Color fill = hovered
        ? Color{43, 49, 53, 248}
        : Color{21, 27, 31, 244};
    const Color border = hovered
        ? Color{235, 185, 77, 255}
        : Color{173, 125, 39, 255};

    renderDrawer->renderRectFillColor(
        card.getX() + 5,
        card.getY() + 6,
        card.getWidth(),
        card.getHeight(),
        Color{0, 0, 0, 150}
    );
    renderDrawer->renderRectFillColor(card, fill);
    renderDrawer->renderRectColor(card, border);
    renderDrawer->renderRectColor(
        card.getX() + 4,
        card.getY() + 4,
        card.getWidth() - 8,
        card.getHeight() - 8,
        Color{102, 78, 35, 255}
    );

    const int imageMaxWidth = card.getWidth() - 24;
    const int imageMaxHeight = card.getHeight() - 72;
    const float sourceAspect = static_cast<float>(emblem->w) /
        std::max(1, emblem->h);
    int imageWidth = imageMaxWidth;
    int imageHeight = std::max(
        1,
        static_cast<int>(imageWidth / sourceAspect)
    );
    if (imageHeight > imageMaxHeight) {
        imageHeight = imageMaxHeight;
        imageWidth = std::max(
            1,
            static_cast<int>(imageHeight * sourceAspect)
        );
    }
    const cRectangle source(
        0,
        0,
        emblem->w,
        emblem->h
    );
    const cRectangle destination(
        card.getX() + (card.getWidth() - imageWidth) / 2,
        card.getY() + 12,
        imageWidth,
        imageHeight
    );
    renderDrawer->renderStrechSprite(
        emblem,
        source,
        destination,
        hovered ? 255 : 232
    );

    const int nameWidth = m_textDrawer->getTextLength(name);
    m_textDrawer->drawText(
        card.getX() + (card.getWidth() - nameWidth) / 2,
        card.getY() + card.getHeight() -
            m_textDrawer->getFontHeight() - 22,
        hovered
            ? Color{255, 224, 139, 255}
            : Color{238, 229, 204, 255},
        name
    );
}

eGameStateType cChooseHouseState::getType()
{
    return GAMESTATE_SELECT_YOUR_NEXT_CONQUEST;
}

void cChooseHouseState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    switch (event.eventType) {
        case MOUSE_LEFT_BUTTON_CLICKED:
            onMouseLeftButtonClicked(event);
            break;
        case MOUSE_MOVED_TO:
            onMouseMoved(event);
            break;
        default:
            break;
    }
}

void cChooseHouseState::onMouseLeftButtonClicked(const s_MouseEvent &event) const
{

    if (event.coords.isWithinRectangle(&houseAtreides)) {
        m_game.prepareMentatToTellAboutHouse(ATREIDES);
        m_game.playSound(SOUND_ATREIDES);
        m_game.setNextStateToTransitionTo(GAME_TELLHOUSE);
        m_game.initiateFadingOut();
    }
    else if (event.coords.isWithinRectangle(&houseOrdos)) {
        m_game.prepareMentatToTellAboutHouse(ORDOS);
        m_game.playSound(SOUND_ORDOS);
        m_game.setNextStateToTransitionTo(GAME_TELLHOUSE);
        m_game.initiateFadingOut();
    }
    else if (event.coords.isWithinRectangle(&houseHarkonnen)) {
        m_game.prepareMentatToTellAboutHouse(HARKONNEN);
        m_game.playSound(SOUND_HARKONNEN);
        m_game.setNextStateToTransitionTo(GAME_TELLHOUSE);
        m_game.initiateFadingOut();
    }
    else if (event.coords.isWithinRectangle(backButtonRect)) {
        m_game.setNextStateToTransitionTo(GAME_MENU);
        m_game.initiateFadingOut();
    }
}

void cChooseHouseState::onMouseMoved(const s_MouseEvent &event)
{
    hoversOverBackButton = event.coords.isWithinRectangle(backButtonRect);
    m_hoveredHouse = -1;
    if (event.coords.isWithinRectangle(&houseAtreides)) {
        m_hoveredHouse = ATREIDES;
    }
    else if (event.coords.isWithinRectangle(&houseOrdos)) {
        m_hoveredHouse = ORDOS;
    }
    else if (event.coords.isWithinRectangle(&houseHarkonnen)) {
        m_hoveredHouse = HARKONNEN;
    }
}

void cChooseHouseState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (event.isType(eKeyEventType::PRESSED)) {
        if (event.hasKey(SDL_SCANCODE_ESCAPE)) {
            m_game.setNextStateToTransitionTo(GAME_MENU);
            m_game.initiateFadingOut();
        }
    }
}
