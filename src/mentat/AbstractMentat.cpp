/*

  Dune II - The Maker

  Author : Stefan Hendriks
  Contact: stefan@fundynamic.com
  Website: http://dune2themaker.fundynamic.com

  2001 - 2022 (c) code by Stefan Hendriks

  */

#include "AbstractMentat.h"
#include "d2tmc.h"
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
constexpr float HD_MENTAT_BUTTON_TEXT_SCALE = 0.85F;

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

AbstractMentat::AbstractMentat(GameContext* ctx, bool canMissionSelect, bool adaptiveHdLayout)
{
    gfxmentat = ctx->getGraphicsContext()->gfxmentat.get();
    m_adaptiveHdLayout = adaptiveHdLayout && game.isHdGraphicsActive();
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
    const int movieBaseX = m_adaptiveHdLayout ? 205 : 256;
    const int movieBaseY = m_adaptiveHdLayout ? 96 : 120;
    if (m_adaptiveHdLayout) {
        // Preserve the source scene's 23:14 aspect ratio.  The old 385x210
        // destination stretched every campaign animation horizontally.
        m_movieWidth = 400;
        m_movieHeight = 243;
    }
    movieTopleftX = baseX(movieBaseX);
    movieTopleftY = baseY(movieBaseY);

    if (canMissionSelect) {
        const std::string label = m_adaptiveHdLayout
            ? localization::text("Missions", "Миссии")
            : localization::text("Mission select", "Выбор миссии");
        cRectangle toMissionSelectRect;
        if (m_adaptiveHdLayout) {
            // Keep campaign navigation inside the remastered 640x480 panel.
            // The previous absolute screen-space placement was calculated
            // before the panel scale and offset and ended up clipped at the
            // physical bottom-right corner on wide displays.
            toMissionSelectRect = baseRect(514, 451, 110, 24);
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
            .withTextScale(m_adaptiveHdLayout ? HD_MENTAT_BUTTON_TEXT_SCALE : 1.0F)
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

    // Classic mentat backgrounds use transparent cut-outs, so the movie stays
    // behind them.  The remastered Bene Gesserit background is deliberately
    // opaque and its viewport is composited afterwards at native HD quality.
    if (!m_adaptiveHdLayout) draw_movie();

    Texture *tmp = getBackgroundBitmap();
    cRectangle dest = {offsetX, offsetY, m_panelWidth, m_panelHeight};
    renderDrawer->renderStrechFullSprite(tmp, dest);

    if (m_adaptiveHdLayout) draw_movie();

    draw_eyes();
    draw_mouth();
    draw_other();

    if (state == SPEAKING) {
        // draw text that is being spoken
        if (iMentatSentence >= 0) {
            if (m_adaptiveHdLayout) {
                const cRectangle textBox = baseRect(24, 10, 592, 61);
                const int gap = static_cast<int>(std::lround(2.0F * m_uiScale));
                const auto layout = wrapMentatText(
                    m_textDrawer,
                    sentence[iMentatSentence],
                    sentence[iMentatSentence + 1],
                    textBox.getWidth(),
                    HD_MENTAT_TEXT_SCALE
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
        if (m_adaptiveHdLayout) drawHdMissionSelectFrame();
        m_guiBtnToMissionSelect->draw();
    }
}

void AbstractMentat::drawHdMissionSelectFrame() const
{
    // The two response-button frames are part of the remastered background.
    // Mission selection has no painted recess in the source artwork, so build
    // a compact matching inset from layered steel and aged-brass strokes.
    const cRectangle outer = baseRect(510, 448, 118, 29);
    const cRectangle middle(
        outer.getX() + std::max(1, static_cast<int>(std::lround(2.0F * m_uiScale))),
        outer.getY() + std::max(1, static_cast<int>(std::lround(2.0F * m_uiScale))),
        outer.getWidth() - std::max(2, static_cast<int>(std::lround(4.0F * m_uiScale))),
        outer.getHeight() - std::max(2, static_cast<int>(std::lround(4.0F * m_uiScale)))
    );
    const cRectangle inner(
        middle.getX() + std::max(1, static_cast<int>(std::lround(2.0F * m_uiScale))),
        middle.getY() + std::max(1, static_cast<int>(std::lround(2.0F * m_uiScale))),
        middle.getWidth() - std::max(2, static_cast<int>(std::lround(4.0F * m_uiScale))),
        middle.getHeight() - std::max(2, static_cast<int>(std::lround(4.0F * m_uiScale)))
    );

    renderDrawer->renderRectFillColor(
        outer.getX() + std::max(1, static_cast<int>(std::lround(2.0F * m_uiScale))),
        outer.getY() + std::max(1, static_cast<int>(std::lround(2.0F * m_uiScale))),
        outer.getWidth(),
        outer.getHeight(),
        Color{0, 0, 0, 190}
    );
    renderDrawer->renderRectFillColor(outer, Color{8, 12, 18, 255});
    renderDrawer->renderRectColor(outer, Color{74, 56, 29, 255});
    renderDrawer->renderRectFillColor(middle, Color{27, 29, 30, 255});
    renderDrawer->renderRectColor(middle, Color{163, 116, 38, 255});
    renderDrawer->renderRectFillColor(inner, Color{18, 24, 29, 255});
    renderDrawer->renderRectColor(inner, Color{45, 38, 27, 255});
    renderDrawer->renderLine(
        inner.getX() + std::max(1, static_cast<int>(std::lround(3.0F * m_uiScale))),
        inner.getY() + 1,
        inner.getX() + inner.getWidth() - std::max(2, static_cast<int>(std::lround(3.0F * m_uiScale))),
        inner.getY() + 1,
        Color{113, 82, 36, 255}
    );
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
        const int preferredDensity = game.getGraphicsDensity();
        const std::array<int, 2> densities{
            preferredDensity,
            preferredDensity == 4 ? 2 : 4
        };
        for (const int density : densities) {
            const std::string candidate = std::format(
                "data/scenes/hd{}/sdl_{}.dat",
                density,
                scene
            );
            if (std::filesystem::exists(candidate)) {
                filename = candidate;
                sceneDensity = density;
                break;
            }
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
