/*

  Dune II - The Maker

  Author : Stefan Hendriks
  Contact: stefan@fundynamic.com
  Website: http://dune2themaker.fundynamic.com

  2001 - 2022 (c) code by Stefan Hendriks

  */

#include "AbstractMentat.h"
#include "d2tmc.h"
#include "data/gfxmentat.h"
#include "definitions.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/RNG.hpp"
#include "context/GameContext.hpp"
#include "gui/GuiButton.h"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"

#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <format>
#include <array>
#include <algorithm>
#include <cmath>
#include <filesystem>
#include <limits>
#include <sstream>
#include <vector>

namespace {
constexpr float HD_MENTAT_TEXT_SCALE = 0.85F;
constexpr float HD_MENTAT_TEXT_MIN_SCALE = 1.20F;
constexpr float HD_MENTAT_TEXT_MAX_SCALE = 1.55F;
constexpr int HD_MENTAT_TEXT_HEADER_HEIGHT = 90;
constexpr int HD_STANDARD_MOVIE_X = 211;
constexpr int HD_STANDARD_MOVIE_Y = 93;
constexpr int HD_STANDARD_MOVIE_WIDTH = 400;
constexpr int HD_STANDARD_MOVIE_HEIGHT = 243;
constexpr int HD_MISSION_SELECT_FRAME_Y = 345;
constexpr int HD_MISSION_SELECT_FRAME_WIDTH = 114;
constexpr int HD_MISSION_SELECT_FRAME_HEIGHT = 29;
constexpr int HD_MISSION_SELECT_BUTTON_Y = HD_MISSION_SELECT_FRAME_Y + 3;
constexpr int HD_MISSION_SELECT_BUTTON_WIDTH = HD_MISSION_SELECT_FRAME_WIDTH - 8;
constexpr int HD_MISSION_SELECT_BUTTON_HEIGHT = HD_MISSION_SELECT_FRAME_HEIGHT - 5;

int utf8CharacterCount(const char *text)
{
    int count = 0;
    for (const auto *byte = reinterpret_cast<const unsigned char *>(text); *byte != '\0'; ++byte) {
        if ((*byte & 0xC0) != 0x80) {
            ++count;
        }
    }
    return count;
}

struct MentatTextLayout {
    std::array<std::string, 2> lines;
    int lineCount = 0;
    float scale = 1.0F;
};

MentatTextLayout wrapMentatText(
    cTextDrawer *drawer,
    const std::string &first,
    const std::string &second,
    int availableWidth,
    float fixedScale)
{
    MentatTextLayout result;
    std::string combined = first;
    if (!second.empty()) {
        if (!combined.empty()) combined += ' ';
        combined += second;
    }
    if (combined.empty()) return result;

    std::istringstream stream(combined);
    std::vector<std::string> words;
    for (std::string word; stream >> word;) words.push_back(std::move(word));
    if (words.empty()) return result;

    auto joinWords = [&words](std::size_t begin, std::size_t end) {
        std::string line;
        for (std::size_t index = begin; index < end; ++index) {
            if (!line.empty()) line += ' ';
            line += words[index];
        }
        return line;
    };

    result.lines[0] = combined;
    result.lineCount = 1;
    int widestLine = drawer->getTextLength(combined);
    if (words.size() > 1 && widestLine * fixedScale > availableWidth) {
        int bestWidth = std::numeric_limits<int>::max();
        for (std::size_t split = 1; split < words.size(); ++split) {
            const std::string left = joinWords(0, split);
            const std::string right = joinWords(split, words.size());
            const int width = std::max(
                drawer->getTextLength(left),
                drawer->getTextLength(right)
            );
            if (width < bestWidth) {
                bestWidth = width;
                result.lines[0] = left;
                result.lines[1] = right;
            }
        }
        result.lineCount = 2;
        widestLine = bestWidth;
    }

    // A single scale is deliberately used for every briefing phrase.  The
    // previous per-phrase fitting made the captions visibly grow and shrink.
    result.scale = fixedScale;
    return result;
}
}

AbstractMentat::AbstractMentat(
    GameContext* ctx,
    bool canMissionSelect,
    bool adaptiveHdLayout,
    int hdMissionSelectCenterX,
    float hdMissionTextOffsetY)
{
    gfxmentat = ctx->getGraphicsContext()->gfxmentat.get();
    m_adaptiveHdLayout = adaptiveHdLayout && game.isHdGraphicsActive();
    m_hdMissionSelectCenterX = hdMissionSelectCenterX;
    m_textDrawer = m_adaptiveHdLayout
        ? ctx->getTextContext()->getMentatHdTextDrawer()
        : ctx->getTextContext()->getBeneTextDrawer();
    iMentatSentence = -1;

    TIMER_Speaking = -1;
    TIMER_Mouth = 0;
    TIMER_Eyes = 0;
    TIMER_Other = 0;
    TIMER_movie = 0;

    iMentatMouth = 3;
    iMentatEyes = 3;
    iMovieFrame = -1;

    iBackgroundFrame = -1;

    house = GENERALHOUSE;

    gfxmovie = nullptr;
    leftButton = nullptr;
    rightButton = nullptr;
    // the mentat does not *own* the bitmaps
    leftButtonBmp = nullptr;
    rightButtonBmp = nullptr;
    leftGuiButton = nullptr;
    rightGuiButton = nullptr;

    m_guiBtnToMissionSelect = nullptr;

    state = INIT;

    if (m_adaptiveHdLayout) {
        const float widthScale = static_cast<float>(game.m_screenW) * 0.90F / 640.0F;
        const float heightScale = static_cast<float>(game.m_screenH) * 0.90F / 480.0F;
        m_uiScale = std::clamp(std::min(widthScale, heightScale), 1.0F, 2.25F);
    }
    m_panelWidth = static_cast<int>(std::lround(640.0F * m_uiScale));
    m_panelHeight = static_cast<int>(std::lround(480.0F * m_uiScale));
    offsetX = (game.m_screenW - m_panelWidth) / 2;
    offsetY = (game.m_screenH - m_panelHeight) / 2;
    const int movieBaseX = m_adaptiveHdLayout ? HD_STANDARD_MOVIE_X : 256;
    const int movieBaseY = m_adaptiveHdLayout ? HD_STANDARD_MOVIE_Y : 120;
    if (m_adaptiveHdLayout) {
        // Keep the source scene at its full 23:14 presentation size.  It is
        // covered outside the glass opening by the foreground pass, which
        // keeps the opaque remastered frame above the unscaled scene.
        m_movieWidth = HD_STANDARD_MOVIE_WIDTH;
        m_movieHeight = HD_STANDARD_MOVIE_HEIGHT;
    }
    movieTopleftX = baseX(movieBaseX);
    movieTopleftY = baseY(movieBaseY);

    if (canMissionSelect) {
        const std::string label = m_adaptiveHdLayout
            ? localization::text("Missions", "Миссии")
            : localization::text("Mission select", "Выбор миссии");
        cRectangle toMissionSelectRect;
        if (m_adaptiveHdLayout) {
            // Center campaign navigation above the right response button.
            const int frameX = m_hdMissionSelectCenterX - HD_MISSION_SELECT_FRAME_WIDTH / 2;
            toMissionSelectRect = baseRect(
                frameX + 4,
                HD_MISSION_SELECT_BUTTON_Y,
                HD_MISSION_SELECT_BUTTON_WIDTH,
                HD_MISSION_SELECT_BUTTON_HEIGHT
            );
        }
        else {
            const int length = m_textDrawer->getTextLength(label);
            toMissionSelectRect = cRectangle(
                game.m_screenW - length,
                game.m_screenH - m_textDrawer->getFontHeight(),
                length,
                m_textDrawer->getFontHeight()
            );
        }

        m_guiBtnToMissionSelect = GuiButtonBuilder()
            .withRect(toMissionSelectRect)
            .withLabel(label)
            .withTextDrawer(m_textDrawer)
            .withTextScale(m_adaptiveHdLayout ? HD_BUTTON_TEXT_SCALE : 1.0F)
            .withTextOffsetY(m_adaptiveHdLayout
                ? static_cast<int>(std::lround(hdMissionTextOffsetY * m_uiScale))
                : 0)
            .withTheme(m_adaptiveHdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(m_adaptiveHdLayout
                ? GuiRenderKind::TRANSPARENT_WITHOUT_BORDER
                : GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .onClick([] {
                game.setNextStateToTransitionTo(GAME_MISSIONSELECT);
            })
            .build();
    }
    memset(sentence, 0, sizeof(sentence));
    logbook("cAbstractMentat::cAbstractMentat()");
}

AbstractMentat::~AbstractMentat()
{
    delete leftButton;
    delete rightButton;
    leftButtonBmp = nullptr;
    rightButtonBmp = nullptr;
    delete m_guiBtnToMissionSelect;
    delete m_hdForegroundLayer;

    logbook("cAbstractMentat::~cAbstractMentat()");
}

void AbstractMentat::think()
{
    if (state == INIT) {
        // no thinking for init state
        return;
    }

    if (state == SPEAKING) {
        if (TIMER_Speaking > 0) {
            TIMER_Speaking--;
        }
        else if (TIMER_Speaking == 0) {
            // calculate speaking stuff
            iMentatSentence += 2; // makes 0, 2, etc.

            // done talking
            if (iMentatSentence > 8) {
                state = AWAITING_RESPONSE;
                return;
            }

            // lentgh calculation of time
            int iLength = utf8CharacterCount(sentence[iMentatSentence]);
            iLength += utf8CharacterCount(sentence[iMentatSentence + 1]);

            // nothing to say, await response
            if (iLength < 2) {
                state = AWAITING_RESPONSE;
                return;
            }

            TIMER_Speaking = iLength * 12;
        }

        thinkMouth();
    }
    else {
        iMentatMouth = 0; // keep lips sealed
    }

    // eyes blink always
    thinkEyes();

    // regardless, think about movie animation
    thinkMovie();
}

void AbstractMentat::thinkMovie()
{
    if (gfxmovie != nullptr) {
        TIMER_movie++;

        if (TIMER_movie > 20) {
            iMovieFrame++;

            if (iMovieFrame == gfxmovie->getNumberOfFiles()) {
                iMovieFrame = 0;
            }
            TIMER_movie = 0;
        }
    }
}

void AbstractMentat::thinkEyes()
{
    if (TIMER_Eyes > 0) {
        TIMER_Eyes--;
    }
    else {
        int i = RNG::rnd(100);

        int iWas = iMentatEyes;

        if (i < 30) {
            iMentatEyes = 3;
        }
        else if (i < 60) {
            iMentatEyes = 0;
        }
        else {
            iMentatEyes = 4;
        }

        // its the same
        if (iMentatEyes == iWas) {
            iMentatEyes = RNG::rnd(4);
        }

        if (iMentatEyes != 4) {
            TIMER_Eyes = 90 + RNG::rnd(160);
        }
        else {
            TIMER_Eyes = 30;
        }
    }
}

void AbstractMentat::thinkMouth()  // MOUTH
{
    if (TIMER_Mouth > 0) {
        TIMER_Mouth--;
    }
    else {
        // still speaking
        if (TIMER_Speaking > 0) {

            int iOld = iMentatMouth;

            if (iMentatMouth == 0) { // mouth is shut
                // when mouth is shut, we wait a bit.
                if (RNG::rnd(100) < 45) {
                    iMentatMouth += (1 + RNG::rnd(4));
                }
                else {
                    TIMER_Mouth = 25; // wait
                }
            }
            else {
                iMentatMouth += (1 + RNG::rnd(4));
            }

            // correct any frame
            if (iMentatMouth > 4) {
                iMentatMouth -= 5;
            }

            // Test if we did not set the timer, when not, we changed stuff, and we
            // have to make sure we do not reshow the same animation.. which looks
            // odd!
            if (TIMER_Mouth <= 0) {
                // did not change mouth, force it
                if (iMentatMouth == iOld) {
                    iMentatMouth++;
                }

                // correct if needed:
                if (iMentatMouth > 4) {
                    iMentatMouth -= 5;
                }
            }
        }
        else {
            iMentatMouth = 0; // when there is no sentence, do not animate mouth
        }

        if (TIMER_Mouth <= 0) {
            TIMER_Mouth = 13 + RNG::rnd(15);
        }
    } // Animating mouth

}

void AbstractMentat::draw()
{
    renderDrawer->renderClearToColor(Color{7,7,15,255});
    renderDrawer->renderRectColor(offsetX-1, offsetY-1, m_panelWidth+1, m_panelHeight+1, Color{64, 64,89,255});
    renderDrawer->renderRectColor(offsetX-2, offsetY-2, m_panelWidth+2, m_panelHeight+2, Color{40,40,60,255});
    renderDrawer->renderRectColor(offsetX-3, offsetY-3, m_panelWidth+3, m_panelHeight+3, Color{0,0,0,255});

    Texture *background = getBackgroundBitmap();
    const cRectangle panelDestination = {offsetX, offsetY, m_panelWidth, m_panelHeight};
    const bool hasMovie = gfxmovie != nullptr && iMovieFrame >= 0;

    if (m_adaptiveHdLayout && hasMovie) {
        // HD composition, back to front: an oversized scene, one continuous
        // foreground texture with an alpha opening, then mentat animations and
        // text below.  The scene never draws over the frame or portrait.
        draw_movie();
        renderDrawer->renderStrechFullSprite(
            getHdForegroundLayer(background),
            panelDestination
        );
    }
    else {
        // Classic backgrounds already contain transparent openings.  HD Bene
        // Gesserit screens have no separate movie and stay fully opaque.
        if (!m_adaptiveHdLayout) draw_movie();
        renderDrawer->renderStrechFullSprite(background, panelDestination);
    }

    drawHdTextHeader();

    draw_eyes();
    draw_mouth();
    draw_other();

    if (state == SPEAKING) {
        // draw text that is being spoken
        if (iMentatSentence >= 0) {
            if (m_adaptiveHdLayout) {
                const cRectangle textBox = baseRect(20, 6, 600, 78);
                const int gap = static_cast<int>(std::lround(2.0F * m_uiScale));
                const float textScale = std::clamp(
                    HD_MENTAT_TEXT_SCALE * m_uiScale,
                    HD_MENTAT_TEXT_MIN_SCALE,
                    HD_MENTAT_TEXT_MAX_SCALE
                );
                const auto layout = wrapMentatText(
                    m_textDrawer,
                    sentence[iMentatSentence],
                    sentence[iMentatSentence + 1],
                    textBox.getWidth(),
                    textScale
                );
                const int lineHeight = static_cast<int>(
                    std::lround(m_textDrawer->getFontHeight() * layout.scale)
                );
                const int blockHeight = lineHeight * layout.lineCount +
                    std::max(0, layout.lineCount - 1) * gap;
                const int blockTop = textBox.getY() +
                    std::max(0, (textBox.getHeight() - blockHeight) / 2);
                renderDrawer->setClippingFor(
                    textBox.getX(),
                    textBox.getY(),
                    textBox.getX() + textBox.getWidth(),
                    textBox.getY() + textBox.getHeight()
                );
                for (int line = 0; line < layout.lineCount; ++line) {
                    m_textDrawer->drawTextScaledCenteredInBox(
                        layout.lines[line],
                        cRectangle(
                            textBox.getX(),
                            blockTop + line * (lineHeight + gap),
                            textBox.getWidth(),
                            lineHeight
                        ),
                        layout.scale,
                        Color{255, 226, 165,255}
                    );
                }
                renderDrawer->resetClippingFor();
            }
            else {
                m_textDrawer->drawText(baseX(18), baseY(17) + 1,Color{0, 0, 0,255},sentence[iMentatSentence]);
                m_textDrawer->drawText(baseX(17), baseY(17),Color{255, 229, 174,255},sentence[iMentatSentence]);
                const int secondLineY = baseY(17) + m_textDrawer->getFontHeight() + 5;
                m_textDrawer->drawText(baseX(18), secondLineY + 1,Color{0, 0, 0,255},sentence[iMentatSentence+1]);
                m_textDrawer->drawText(baseX(17), secondLineY,Color{255, 229, 174,255},sentence[iMentatSentence+1]);
            }
        }
    }

    if (state == AWAITING_RESPONSE) {
        if (leftGuiButton) {
            leftGuiButton->draw();
        }
        if (rightGuiButton){
            rightGuiButton->draw();
        }
    }

    if (m_guiBtnToMissionSelect) {
        m_guiBtnToMissionSelect->draw();
    }
}

void AbstractMentat::drawHdTextHeader() const
{
    if (!m_adaptiveHdLayout) return;

    Texture *atreidesHeader = gfxmentat->getTexture(MENTATA);
    renderDrawer->renderStrechSprite(
        atreidesHeader,
        cRectangle(0, 0, 640, HD_MENTAT_TEXT_HEADER_HEIGHT),
        baseRect(0, 0, 640, HD_MENTAT_TEXT_HEADER_HEIGHT)
    );
}

void AbstractMentat::harmonizeHdButtonTextScale()
{
    if (!m_adaptiveHdLayout || !leftGuiButton || !rightGuiButton) return;

    float sharedScale = HD_BUTTON_TEXT_SCALE;
    const int fontHeight = std::max(1, m_textDrawer->getFontHeight());
    const auto include = [this, fontHeight, &sharedScale](
        const cRectangle &rect,
        const std::string &label) {
        const float widthScale = static_cast<float>(std::max(1, rect.getWidth() - 16)) /
            std::max(1, m_textDrawer->getTextLength(label));
        const float heightScale = static_cast<float>(std::max(1, rect.getHeight() - 8)) /
            fontHeight;
        sharedScale = std::min({sharedScale, widthScale, heightScale});
    };

    include(*leftButton, localization::text("Repeat", "Повторить"));
    include(*rightButton, localization::text("Next", "Далее"));
    if (m_guiBtnToMissionSelect) {
        const int frameX = m_hdMissionSelectCenterX - HD_MISSION_SELECT_FRAME_WIDTH / 2;
        include(
            baseRect(
                frameX + 4,
                HD_MISSION_SELECT_BUTTON_Y,
                HD_MISSION_SELECT_BUTTON_WIDTH,
                HD_MISSION_SELECT_BUTTON_HEIGHT
            ),
            localization::text("Missions", "Миссии")
        );
    }

    sharedScale = std::max(0.65F, sharedScale);
    leftGuiButton->setTextScale(sharedScale);
    rightGuiButton->setTextScale(sharedScale);
    if (m_guiBtnToMissionSelect) m_guiBtnToMissionSelect->setTextScale(sharedScale);
}

Texture *AbstractMentat::getBackgroundBitmap() const
{
    if (iBackgroundFrame < 0) return nullptr;
    return gfxmentat->getTexture(iBackgroundFrame);
}

void AbstractMentat::draw_movie()
{
    if (gfxmovie == nullptr) return;
    if (iMovieFrame < 0) return;

    // drawing only, circulating is done in think function
    Texture *tmp = gfxmovie->getTexture(iMovieFrame);
    cRectangle dest = {
        movieTopleftX,
        movieTopleftY,
        static_cast<int>(std::lround((m_adaptiveHdLayout ? m_movieWidth : tmp->w) * m_uiScale)),
        static_cast<int>(std::lround((m_adaptiveHdLayout ? m_movieHeight : tmp->h) * m_uiScale))
    };
    renderDrawer->renderStrechFullSprite(tmp, dest);
}

Texture *AbstractMentat::getHdForegroundLayer(Texture *background)
{
    if (!background) return nullptr;
    if (m_hdForegroundLayer) return m_hdForegroundLayer;

    m_hdForegroundLayer = renderDrawer->createRenderTargetTexture(
        background->pixelW,
        background->pixelH
    );
    renderDrawer->beginDrawingToTexture(m_hdForegroundLayer);
    renderDrawer->renderClearToColor(Color{0, 0, 0, 0});
    renderDrawer->renderStrechFullSprite(
        background,
        cRectangle(0, 0, background->pixelW, background->pixelH)
    );
    clearHdMovieOpening(background);
    renderDrawer->endDrawingToTexture();
    SDL_SetTextureBlendMode(m_hdForegroundLayer->tex, SDL_BLENDMODE_BLEND);
    return m_hdForegroundLayer;
}

void AbstractMentat::clearHdMovieOpening(Texture *background)
{
    constexpr int cornerHeight = 14;
    const int bottom = m_movieClipY + m_movieClipHeight;
    for (int y = m_movieClipY; y < bottom; ++y) {
        int inset = 0;
        if (y < m_movieClipY + cornerHeight) {
            inset = m_movieClipY + cornerHeight - y;
        }
        else if (y >= bottom - cornerHeight) {
            inset = y - (bottom - cornerHeight) + 1;
        }
        clearHdForegroundLayerRegion(
            background,
            m_movieClipX + inset,
            y,
            m_movieClipWidth - inset * 2,
            1
        );
    }
}

void AbstractMentat::clearHdForegroundLayerRegion(
    Texture *background,
    int x,
    int y,
    int width,
    int height) const
{
    if (!background || width <= 0 || height <= 0) return;

    const int left = static_cast<int>(std::lround(
        static_cast<double>(x) * background->pixelW / 640.0
    ));
    const int top = static_cast<int>(std::lround(
        static_cast<double>(y) * background->pixelH / 480.0
    ));
    const int right = static_cast<int>(std::lround(
        static_cast<double>(x + width) * background->pixelW / 640.0
    ));
    const int bottom = static_cast<int>(std::lround(
        static_cast<double>(y + height) * background->pixelH / 480.0
    ));
    renderDrawer->clearRectToTransparent(
        cRectangle(left, top, right - left, bottom - top)
    );
}

int AbstractMentat::baseX(int value) const
{
    return offsetX + static_cast<int>(std::lround(value * m_uiScale));
}

int AbstractMentat::baseY(int value) const
{
    return offsetY + static_cast<int>(std::lround(value * m_uiScale));
}

cRectangle AbstractMentat::baseRect(int x, int y, int width, int height) const
{
    return cRectangle(
        baseX(x),
        baseY(y),
        static_cast<int>(std::lround(width * m_uiScale)),
        static_cast<int>(std::lround(height * m_uiScale))
    );
}

void AbstractMentat::drawMentatTexture(Texture *texture, int x, int y)
{
    if (texture == nullptr) return;
    const cRectangle destination = baseRect(x, y, texture->w, texture->h);
    renderDrawer->renderStrechFullSprite(texture, destination);
}

void AbstractMentat::initSentences()
{
    memset(sentence, 0, sizeof(sentence));
}

void AbstractMentat::setSentence(int i, const char *text)
{
    snprintf(sentence[i], sizeof(sentence[i]), "%s", text);
    logbook(std::format("Sentence[{}]={}", i, text));
}

void AbstractMentat::loadScene(const std::string &scene)
{
    gfxmovie = nullptr;

    std::string filename = std::format(
        "data/scenes/sdl_{}.dat",
        scene
    );
    int sceneDensity = 1;
    if (game.isHdGraphicsActive()) {
        const std::string candidate = std::format(
            "data/scenes/hd4/sdl_{}.dat",
            scene
        );
        if (std::filesystem::exists(candidate)) {
            filename = candidate;
            sceneDensity = 4;
        }
    }

    gfxmovie = std::make_shared<Graphics>(
        renderDrawer->getRenderer(),
        filename,
        sceneDensity
    );

    TIMER_movie = 0;
    iMovieFrame=0;

    if (gfxmovie != nullptr) {
        logbook(std::format(
            "Successful loaded scene [{}] ({}x)",
            filename,
            sceneDensity
        ));
        return;
    }

    gfxmovie=nullptr;
    logbook(std::format("Failed to load scene [{}]", filename));
}

void AbstractMentat::speak()
{
    TIMER_Speaking = 0;
    TIMER_Mouth = 0;
    iMentatSentence = -2; // ugh
    state = SPEAKING;
}

void AbstractMentat::buildLeftButton(Texture *bmp, int x, int y)
{
    delete leftButton;
    leftButton = new cRectangle(baseRect(x, y, bmp->w, bmp->h));
    leftButtonBmp = bmp;
}

void AbstractMentat::buildRightButton(Texture *bmp, int x, int y)
{
    delete rightButton;
    rightButton = new cRectangle(baseRect(x, y, bmp->w, bmp->h));
    rightButtonBmp = bmp;
}

void AbstractMentat::resetSpeak()
{
    speak();
}

void AbstractMentat::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (state == SPEAKING) {
        if (event.eventType==MOUSE_LEFT_BUTTON_CLICKED) {
            if (TIMER_Speaking > 0) {
                TIMER_Speaking = 1;
            }
        }
    }

    if (state == AWAITING_RESPONSE) {
        if (m_guiBtnToMissionSelect) {
            m_guiBtnToMissionSelect->onNotifyMouseEvent(event);
        }
        if (leftGuiButton) {
            leftGuiButton->onNotifyMouseEvent(event);
        }
        if (rightGuiButton) {
            rightGuiButton->onNotifyMouseEvent(event);
        }
    }
}

void AbstractMentat::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (m_guiBtnToMissionSelect) {
        m_guiBtnToMissionSelect->onNotifyKeyboardEvent(event);
    }
}
