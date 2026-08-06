#include "cMainMenuState.h"

#include "config.h"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "d2tmc.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "save/SaveGameManager.hpp"
#include "save/SaveSlotsDialog.hpp"
#include "utils/Graphics.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "utils/Localization.hpp"
#include "utils/cLog.h"
#include "utils/cSoundPlayer.h"

#include <SDL2/SDL.h>

#include <algorithm>
#include <functional>
#include <string>

cMainMenuState::cMainMenuState(cGame &theGame, GameContext* ctx) :
    cGameState(theGame, ctx)
{
    m_hdLayout = m_game.isHdGraphicsActive();
    m_metaTextDrawer = m_hdLayout
        ? ctx->getTextContext()->getMenuTextDrawer()
        : ctx->getTextContext()->getBeneTextDrawer();
    m_textDrawer = m_hdLayout
        ? ctx->getTextContext()->getMenuTextDrawer()
        : m_metaTextDrawer;

    auto *gfxinter = ctx->getGraphicsContext()->gfxinter.get();
    bmp_D2TM_Title = gfxinter->getTexture(BMP_D2TM);

    if (m_hdLayout) {
        buildHdMenu();
    }
    else {
        buildClassicMenu();
    }

    m_saveDialog = std::make_unique<SaveSlotsDialog>(
        m_game,
        m_textDrawer,
        [this]() {
            m_game.initiateFadingOut();
        }
    );

    if (m_game.isDebugMode()) {
        backGroundDebug = renderDrawer->createRenderTargetTexture(
            m_game.m_screenW,
            m_game.m_screenH
        );
        renderDrawer->beginDrawingToTexture(backGroundDebug);
        for (int x = 0; x < m_game.m_screenW; x += 60) {
            for (int y = 0; y < m_game.m_screenH; y += 20) {
                m_metaTextDrawer->drawText(
                    x,
                    y,
                    Color{48, 48, 48, 255},
                    "DEBUG"
                );
            }
        }
        renderDrawer->endDrawingToTexture();
    }
}

void cMainMenuState::buildHdMenu()
{
    const int density = m_game.getGraphicsDensity();
    m_hdMenuBackground = loadHdUiTexture(
        "main_menu_background.png",
        density,
        "HD menu"
    );
    m_hdMenuLogo = loadHdUiTexture(
        "main_menu_logo.png",
        density,
        "HD menu"
    );

    const int buttonCount = 7;
    const int buttonWidth = std::clamp(
        m_game.m_screenW / 4,
        280,
        360
    );
    const int buttonHeight = std::clamp(
        m_game.m_screenH / 15,
        40,
        48
    );
    const int buttonGap = std::clamp(
        m_game.m_screenH / 90,
        6,
        10
    );
    const int panelPadding = 16;
    const int panelWidth = buttonWidth + panelPadding * 2;
    const int panelHeight =
        buttonCount * buttonHeight +
        (buttonCount - 1) * buttonGap +
        panelPadding * 2;
    const int panelX = (m_game.m_screenW - panelWidth) / 2;
    const int panelY = std::clamp(
        (m_game.m_screenH - panelHeight) / 2 + 28,
        132,
        std::max(132, m_game.m_screenH - panelHeight - 46)
    );

    mainMenuFrameX = panelX;
    mainMenuFrameY = panelY;
    mainMenuWidth = panelWidth;
    mainMenuHeight = panelHeight;

    const int sourceLogoWidth = m_hdMenuLogo
        ? m_hdMenuLogo->w
        : bmp_D2TM_Title->w;
    const int sourceLogoHeight = m_hdMenuLogo
        ? m_hdMenuLogo->h
        : bmp_D2TM_Title->h;
    const int logoWidth = std::clamp(
        m_game.m_screenW * 2 / 5,
        310,
        430
    );
    const int logoHeight = std::max(
        1,
        logoWidth * sourceLogoHeight / std::max(1, sourceLogoWidth)
    );
    logoX = (m_game.m_screenW - logoWidth) / 2;
    logoY = std::max(24, panelY - logoHeight - 24);
    m_logoRect = cRectangle(logoX, logoY, logoWidth, logoHeight);

    gui_window = new GuiWindow(
        cRectangle(panelX, panelY, panelWidth, panelHeight),
        m_textDrawer
    );
    gui_window->setTheme(GuiTheme::Remaster());

    const int buttonX = panelX + panelPadding;
    int buttonY = panelY + panelPadding;
    const auto addButton = [
        this,
        buttonX,
        buttonWidth,
        buttonHeight,
        buttonGap,
        &buttonY
    ](
        const std::string &label,
        bool enabled,
        std::function<void()> onClick)
    {
        GuiButton *button = GuiButtonBuilder()
            .withRect(cRectangle(
                buttonX,
                buttonY,
                buttonWidth,
                buttonHeight
            ))
            .withLabel(label)
            .withTextDrawer(m_textDrawer)
            .withTheme(
                enabled
                    ? GuiTheme::Remaster()
                    : GuiTheme::RemasterInactive()
            )
            .withKind(GuiRenderKind::REMASTER_BUTTON)
            .withEnabled(enabled)
            .onClick(std::move(onClick))
            .build();
        gui_window->addGuiObject(button);
        buttonY += buttonHeight + buttonGap;
    };

    addButton(localization::text("Campaign", "Кампания"), true, [this]() {
        m_game.setNextStateToTransitionTo(GAME_SELECT_HOUSE);
        m_game.initiateFadingOut();
    });
    addButton(localization::text("Skirmish", "Схватка"), true, [this]() {
        m_game.loadSkirmishMaps();
        m_game.initSkirmish();
        m_game.setNextStateToTransitionTo(GAME_SETUPSKIRMISH);
        m_game.initiateFadingOut();
    });
    addButton(localization::text("Multiplayer", "Сетевая игра"), false, nullptr);
    addButton(localization::text("Saved games", "Сохранения"), SaveGameManager::hasAnySave(), [this]() {
        m_saveDialog->open(false, false);
    });
    addButton(localization::text("Settings", "Настройки"), true, [this]() {
        m_game.setNextStateToTransitionTo(GAME_OPTIONS);
    });
    addButton(localization::text("Hall of Fame", "Зал славы"), false, nullptr);
    addButton(localization::text("Exit", "Выход"), true, [this]() {
        m_game.m_playing = false;
        m_game.initiateFadingOut();
    });

    const int creditsWidth = 132;
    const int creditsHeight = 34;
    gui_btn_credits = GuiButtonBuilder()
        .withRect(cRectangle(
            m_game.m_screenW - creditsWidth - 18,
            16,
            creditsWidth,
            creditsHeight
        ))
        .withLabel(localization::text("CREDITS", "АВТОРЫ"))
        .withTextDrawer(m_metaTextDrawer)
        .withTheme(GuiTheme::Remaster())
        .withKind(GuiRenderKind::REMASTER_BUTTON)
        .onClick([this]() {
            m_game.setNextStateToTransitionTo(GAME_CREDITS);
            m_game.initiateFadingOut();
        })
        .build();

    sdl2power = cRectangle(
        18,
        m_game.m_screenH - m_metaTextDrawer->getFontHeight() - 22,
        0,
        0
    );
}

void cMainMenuState::buildClassicMenu()
{
    const int logoWidth = bmp_D2TM_Title->w;
    const int logoHeight = bmp_D2TM_Title->h;
    const int centerOfScreen = m_game.m_screenW / 2;

    logoX = centerOfScreen - logoWidth / 2;
    logoY = logoHeight / 10;
    mainMenuWidth = 130;
    mainMenuHeight = 143;
    mainMenuFrameX = centerOfScreen - mainMenuWidth / 2;
    mainMenuFrameY = 319;
    logoY = static_cast<int>(
        mainMenuFrameY - logoHeight * 1.2f
    );
    m_logoRect = cRectangle(
        logoX,
        logoY,
        logoWidth,
        logoHeight
    );
    sdl2power = cRectangle(
        centerOfScreen + logoWidth / 4,
        logoY + logoHeight + 75,
        0,
        0
    );

    const int buttonHeight = m_textDrawer->getFontHeight() + 4;
    const int creditsWidth = m_textDrawer->getTextLength(
        localization::text("CREDITS", "АВТОРЫ")
    ) / 2;
    gui_btn_credits = GuiButtonBuilder()
        .withRect(cRectangle(
            centerOfScreen - creditsWidth,
            0,
            creditsWidth,
            buttonHeight
        ))
        .withLabel(localization::text("CREDITS", "АВТОРЫ"))
        .withTextDrawer(m_textDrawer)
        .withTheme(GuiTheme::Light())
        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
        .onClick([this]() {
            m_game.setNextStateToTransitionTo(GAME_CREDITS);
            m_game.initiateFadingOut();
        })
        .build();

    gui_window = new GuiWindow(
        cRectangle(
            mainMenuFrameX,
            mainMenuFrameY,
            mainMenuWidth,
            mainMenuHeight
        ),
        m_textDrawer
    );
    gui_window->setTheme(GuiTheme::Light());

    const int buttonX = mainMenuFrameX + 2;
    const int buttonWidth = mainMenuWidth - 8;
    const std::array<std::pair<const char *, int>, 7> rows{{
        {localization::text("Campaign", "Кампания"), 323},
        {localization::text("Skirmish", "Схватка"), 344},
        {localization::text("Multiplayer", "Сетевая игра"), 364},
        {localization::text("Saved games", "Сохранения"), 384},
        {localization::text("Settings", "Настройки"), 404},
        {localization::text("Hall of Fame", "Зал славы"), 424},
        {localization::text("Exit", "Выход"), 444}
    }};

    for (std::size_t index = 0; index < rows.size(); ++index) {
        const bool enabled =
            index == 0 ||
            index == 1 ||
            (index == 3 && SaveGameManager::hasAnySave()) ||
            index == 4 ||
            index == 6;
        std::function<void()> onClick;
        if (index == 0) {
            onClick = [this]() {
                m_game.setNextStateToTransitionTo(GAME_SELECT_HOUSE);
                m_game.initiateFadingOut();
            };
        }
        else if (index == 1) {
            onClick = [this]() {
                m_game.loadSkirmishMaps();
                m_game.initSkirmish();
                m_game.setNextStateToTransitionTo(GAME_SETUPSKIRMISH);
                m_game.initiateFadingOut();
            };
        }
        else if (index == 3) {
            onClick = [this]() {
                m_saveDialog->open(false, false);
            };
        }
        else if (index == 4) {
            onClick = [this]() {
                m_game.setNextStateToTransitionTo(GAME_OPTIONS);
            };
        }
        else if (index == 6) {
            onClick = [this]() {
                m_game.m_playing = false;
                m_game.initiateFadingOut();
            };
        }

        GuiButton *button = GuiButtonBuilder()
            .withRect(cRectangle(
                buttonX,
                rows[index].second,
                buttonWidth,
                buttonHeight
            ))
            .withLabel(rows[index].first)
            .withTextDrawer(m_textDrawer)
            .withTheme(
                enabled
                    ? GuiTheme::Light()
                    : GuiTheme::Inactive()
            )
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withEnabled(enabled)
            .onClick(std::move(onClick))
            .build();
        gui_window->addGuiObject(button);
    }
}

cMainMenuState::~cMainMenuState()
{
    delete gui_window;
    delete gui_btn_credits;
    delete m_hdMenuBackground;
    delete m_hdMenuLogo;
    if (m_game.isDebugMode()) {
        delete backGroundDebug;
    }
}

void cMainMenuState::thinkFast()
{
}

void cMainMenuState::drawHdBackground() const
{
    renderDrawer->renderClearToColor(Color{10, 12, 14, 255});
    if (!m_hdMenuBackground) {
        return;
    }

    renderDrawer->renderStrechFullSprite(
        m_hdMenuBackground,
        cRectangle(
            0,
            0,
            m_game.m_screenW,
            m_game.m_screenH
        ),
        90
    );

    const float backgroundAspect =
        static_cast<float>(m_hdMenuBackground->w) /
        std::max(1, m_hdMenuBackground->h);
    const float screenAspect =
        static_cast<float>(m_game.m_screenW) /
        std::max(1, m_game.m_screenH);

    int drawWidth = m_game.m_screenW;
    int drawHeight = m_game.m_screenH;
    if (screenAspect > 2.2f) {
        drawHeight = m_game.m_screenH;
        drawWidth = static_cast<int>(drawHeight * backgroundAspect);
    }
    else if (screenAspect > backgroundAspect) {
        drawWidth = m_game.m_screenW;
        drawHeight = static_cast<int>(drawWidth / backgroundAspect);
    }
    else {
        drawHeight = m_game.m_screenH;
        drawWidth = static_cast<int>(drawHeight * backgroundAspect);
    }

    renderDrawer->renderStrechFullSprite(
        m_hdMenuBackground,
        cRectangle(
            (m_game.m_screenW - drawWidth) / 2,
            (m_game.m_screenH - drawHeight) / 2,
            drawWidth,
            drawHeight
        )
    );
}

void cMainMenuState::draw() const
{
    if (m_hdLayout) {
        drawHdBackground();
    }
    else if (m_game.isDebugMode()) {
        renderDrawer->renderSprite(backGroundDebug, 0, 0);
    }

    Texture *logo = m_hdMenuLogo
        ? m_hdMenuLogo
        : bmp_D2TM_Title;
    if (m_hdLayout) {
        renderDrawer->renderStrechFullSprite(logo, m_logoRect);
    }
    else {
        renderDrawer->renderSprite(logo, logoX, logoY);
    }

    gui_window->draw();
    gui_btn_credits->draw();

    m_metaTextDrawer->drawTextBottomRight(
        Color{220, 213, 188, 230},
        D2TM_VERSION,
        18
    );
    m_metaTextDrawer->drawText(
        sdl2power.getX(),
        sdl2power.getY(),
        Color{218, 177, 75, 220},
        localization::text("Powered by SDL2", "На базе SDL2")
    );

    if (m_game.isDebugMode()) {
        const auto mouse = m_game.getMouse();
        m_metaTextDrawer->drawText(
            0,
            0,
            std::format("{}, {}", mouse->getX(), mouse->getY()).c_str()
        );
    }

    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->draw();
    }
    m_game.getMouse()->draw();
}

void cMainMenuState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->onMouseEvent(event);
        return;
    }
    gui_window->onNotifyMouseEvent(event);
    gui_btn_credits->onNotifyMouseEvent(event);
}

eGameStateType cMainMenuState::getType()
{
    return GAMESTATE_MAIN_MENU;
}

void cMainMenuState::onNotifyKeyboardEvent(
    const cKeyboardEvent &event)
{
    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->onKeyboardEvent(event);
        return;
    }
    if (event.eventType != eKeyEventType::PRESSED) {
        return;
    }
    if (event.hasKey(SDL_SCANCODE_ESCAPE)) {
        m_game.m_playing = false;
    }
    if (
        event.hasKey(SDL_SCANCODE_M) ||
        event.hasKey(SDL_SCANCODE_MUTE)
    ) {
        auto soundPlayer = m_ctx->getSoundPlayer();
        game.m_playMusic = !game.m_playMusic;
        if (!game.m_playMusic) {
            soundPlayer->stopMusic();
        }
    }
}

void cMainMenuState::onTextInput(std::string_view text)
{
    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->onTextInput(text);
    }
}
