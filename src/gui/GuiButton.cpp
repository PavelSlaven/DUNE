/**
 * @file GuiButton.cpp
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

#include "GuiButton.h"

#include "debug/UiAudit.hpp"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "game/cGameSettings.h"
#include "include/cAssert.h"
#include "controls/sMouseEvent.h"

#include <algorithm>
#include <cmath>

GuiButton::GuiButton(SDLDrawer* drawer, const cRectangle &rect, const std::string &btnText)
    : GuiObject(drawer, rect)
    , m_textDrawer(nullptr)
    , m_buttonText(btnText)
    , m_renderKind(GuiRenderKind::OPAQUE_WITHOUT_BORDER)
    , m_textAlignHorizontal(GuiTextAlignHorizontal::CENTER)
    , m_onLeftMouseButtonClickedAction(nullptr)
    , m_onRightMouseButtonClickedAction(nullptr)
    , m_tex(nullptr)
    , m_focus(false)
    , m_pressed(false)
    , m_enabled(true)   // by default always enabled
{
    d2tm_assert(drawer != nullptr);
}

GuiButton::~GuiButton()
{
}

void GuiButton::draw() const
{
    if (uiaudit::isEnabled()) {
        auditRecord("GuiButton");
        if (m_enabled && (m_onLeftMouseButtonClickedAction || m_onRightMouseButtonClickedAction)) {
            auditClick("GuiButton:" + m_buttonText);
        }
    }
    const bool isDisabled = !m_enabled || m_visualState == VisualState::Disabled;
    const bool isPressed = m_pressed || m_visualState == VisualState::Pressed;
    //const bool isHovered = m_focus || m_visualState == VisualState::Hover;

    switch (m_renderKind) {
        case OPAQUE_WITHOUT_BORDER:
            m_sdlDrawer->renderRectFillColor(m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight(), isDisabled ? m_theme.disabledFillColor : m_theme.fillColor);
            drawText();
            break;
        case TRANSPARENT_WITHOUT_BORDER:
            drawText();
            break;
        case OPAQUE_WITH_BORDER:
            m_sdlDrawer->renderRectFillColor(m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight(), isDisabled ? m_theme.disabledFillColor : m_theme.fillColor);
            if (isPressed) {
                m_sdlDrawer->gui_DrawRectBorder(m_rect, m_theme.borderDark, m_theme.borderLight);
            }
            else {
                if (!isDisabled) {
                    m_sdlDrawer->gui_DrawRectBorder(m_rect, m_theme.borderLight, m_theme.borderDark);
                } else {
                    m_sdlDrawer->gui_DrawRectBorder(m_rect, m_theme.disabledBorderLight, m_theme.disabledBorderDark);
                }
            }
            drawText();
            break;
        case TRANSPARENT_WITH_BORDER:
            if (isPressed) {
                m_sdlDrawer->gui_DrawRectBorder(m_rect, m_theme.borderDark, m_theme.borderLight);
            }
            else {
                if (!isDisabled) {
                    m_sdlDrawer->gui_DrawRectBorder(m_rect, m_theme.borderLight, m_theme.borderDark);
                } else {
                    m_sdlDrawer->gui_DrawRectBorder(m_rect, m_theme.disabledBorderLight, m_theme.disabledBorderDark);
                }
            }
            drawText();
            break;
        case WITH_TEXTURE:
            m_sdlDrawer->renderSprite(m_tex, m_rect.getX(),m_rect.getY());
            break;
        case WITH_STRETCHED_TEXTURE:
            m_sdlDrawer->renderStrechFullSprite(m_tex, m_rect, 255);
            break;
        case REMASTER_BUTTON: {
            Color fillColor = m_theme.fillColor;
            Color outerBorder = m_theme.borderDark;
            Color innerBorder = m_theme.borderLight;

            if (m_enabled && m_focus) {
                fillColor = Color{
                    static_cast<Uint8>(std::min(255, fillColor.r + 18)),
                    static_cast<Uint8>(std::min(255, fillColor.g + 18)),
                    static_cast<Uint8>(std::min(255, fillColor.b + 18)),
                    fillColor.a
                };
            }
            if (m_pressed) {
                fillColor = Color{
                    static_cast<Uint8>(fillColor.r * 3 / 4),
                    static_cast<Uint8>(fillColor.g * 3 / 4),
                    static_cast<Uint8>(fillColor.b * 3 / 4),
                    fillColor.a
                };
                std::swap(outerBorder, innerBorder);
            }

            m_sdlDrawer->renderRectFillColor(
                m_rect.getX() + 3,
                m_rect.getY() + 3,
                m_rect.getWidth(),
                m_rect.getHeight(),
                m_theme.textColorShadow
            );
            m_sdlDrawer->renderRectFillColor(m_rect, fillColor);
            m_sdlDrawer->renderRectColor(m_rect, outerBorder);
            m_sdlDrawer->renderRectColor(
                m_rect.getX() + 1,
                m_rect.getY() + 1,
                m_rect.getWidth() - 2,
                m_rect.getHeight() - 2,
                innerBorder
            );
            m_sdlDrawer->renderLine(
                m_rect.getX() + 4,
                m_rect.getY() + 3,
                m_rect.getX() + m_rect.getWidth() - 5,
                m_rect.getY() + 3,
                m_enabled && m_focus
                    ? m_theme.textColorHover
                    : m_theme.borderLight
            );
            drawText();
            break;
        }
    }
}

void GuiButton::setTextAlignHorizontal(GuiTextAlignHorizontal value)
{
    m_textAlignHorizontal = value;
}

void GuiButton::setText(const std::string& text)
{
    m_buttonText = text;
}

void GuiButton::setRenderKind(GuiRenderKind value)
{
    m_renderKind = value;
}

void GuiButton::setTextDrawer(cTextDrawer *cTextDrawer)
{
    m_textDrawer = cTextDrawer;
}

void GuiButton::setTexture(Texture *tex)
{
    m_tex = tex;
}

void GuiButton::setTextScale(float scale)
{
    m_textScale = std::max(0.65F, scale);
}

void GuiButton::setTextOffsetY(int offset)
{
    m_textOffsetY = offset;
}

void GuiButton::drawText() const
{
    const bool isDisabled = !m_enabled || m_visualState == VisualState::Disabled;
    const bool isHovered = m_focus || m_visualState == VisualState::Hover;
    Color textColor = isHovered ? m_theme.textColorHover : m_theme.textColor;
    if (isDisabled) {
        textColor = m_theme.disabledTextColor;
    }

    switch (m_textAlignHorizontal) {
        case GuiTextAlignHorizontal::CENTER:
            {
                const float widthScale = static_cast<float>(std::max(1, m_rect.getWidth() - 16)) /
                    std::max(1, m_textDrawer->getTextLength(m_buttonText));
                const float heightScale = static_cast<float>(std::max(1, m_rect.getHeight() - 8)) /
                    std::max(1, m_textDrawer->getFontHeight());
                const float fittedScale = std::clamp(
                    std::min({m_textScale, widthScale, heightScale}),
                    0.65F,
                    m_textScale
                );
                const int pressedOffset = m_pressed ? 1 : 0;
                const cRectangle textRect(
                    m_rect.getX() + pressedOffset,
                    m_rect.getY() + pressedOffset + m_textOffsetY,
                    m_rect.getWidth(),
                    m_rect.getHeight()
                );
                m_textDrawer->drawTextScaledOpticallyCenteredInBox(
                    m_buttonText,
                    textRect,
                    fittedScale,
                    textColor
                );
            }
            break;
        case GuiTextAlignHorizontal::LEFT:
            if (m_pressed) {
                m_textDrawer->drawText(m_rect.getX() + 1, m_rect.getY() + 1, textColor, m_buttonText.c_str());
            }
            else {
                m_textDrawer->drawText(m_rect.getX(), m_rect.getY(), textColor, m_buttonText.c_str());
            }
            break;
    }
}

void GuiButton::nextRenderKind()
{
    if (m_renderKind == GuiRenderKind::OPAQUE_WITH_BORDER) {
        m_renderKind = GuiRenderKind::OPAQUE_WITHOUT_BORDER;
    }
    else if (m_renderKind == GuiRenderKind::OPAQUE_WITHOUT_BORDER) {
        m_renderKind = GuiRenderKind::TRANSPARENT_WITH_BORDER;
    }
    else if (m_renderKind == GuiRenderKind::TRANSPARENT_WITH_BORDER) {
        m_renderKind = GuiRenderKind::TRANSPARENT_WITHOUT_BORDER;
    }
    else if (m_renderKind == GuiRenderKind::TRANSPARENT_WITHOUT_BORDER) {
        m_renderKind = GuiRenderKind::OPAQUE_WITH_BORDER;
    }
}

void GuiButton::toggleTextAlignHorizontal()
{
    if (m_textAlignHorizontal == GuiTextAlignHorizontal::CENTER) {
        m_textAlignHorizontal = GuiTextAlignHorizontal::LEFT;
    }
    else {
        m_textAlignHorizontal = GuiTextAlignHorizontal::CENTER;
    }
}

void GuiButton::onNotifyMouseEvent(const s_MouseEvent &event)
{
    switch (event.eventType) {
        case MOUSE_MOVED_TO:
            onMouseMovedTo(event);
            break;
        case MOUSE_RIGHT_BUTTON_CLICKED:
            onMouseRightButtonClicked(event);
            break;
        case MOUSE_LEFT_BUTTON_CLICKED:
            onMouseLeftButtonClicked(event);
            break;
        case MOUSE_LEFT_BUTTON_PRESSED:
            onMouseLeftButtonPressed(event);
            break;
        default:
            break;
    }
}

void GuiButton::onMouseMovedTo(const s_MouseEvent &event)
{
    m_focus = m_rect.isPointWithin(event.coords);
    if (!m_enabled) {
        m_visualState = VisualState::Disabled;
    } else if (m_pressed) {
        m_visualState = VisualState::Pressed;
    } else if (m_focus) {
        m_visualState = VisualState::Hover;
    } else {
        m_visualState = VisualState::Normal;
    }
}

void GuiButton::onMouseRightButtonClicked(const s_MouseEvent &)
{
    if (m_focus) {
        if (m_enabled && m_onRightMouseButtonClickedAction) {
            m_onRightMouseButtonClickedAction();
        }
    }
}

void GuiButton::onMouseRightButtonPressed(const s_MouseEvent &)
{
    if (m_enabled) {
        m_pressed = m_focus;
        m_visualState = m_pressed ? VisualState::Pressed : (m_focus ? VisualState::Hover : VisualState::Normal);
    }
}

void GuiButton::onMouseLeftButtonPressed(const s_MouseEvent &)
{
    if (m_enabled) {
        m_pressed = m_focus;
        m_visualState = m_pressed ? VisualState::Pressed : (m_focus ? VisualState::Hover : VisualState::Normal);
    }
}

void GuiButton::onMouseLeftButtonClicked(const s_MouseEvent &event) {
    if (!m_rect.isPointWithin(event.coords) || !m_enabled) {
        return;
    }

    if (m_focus && m_onLeftMouseButtonClickedAction) {
        m_onLeftMouseButtonClickedAction();
    }

    m_pressed = false;
    m_visualState = m_focus ? VisualState::Hover : VisualState::Normal;
}

void GuiButton::setOnLeftMouseButtonClickedAction(std::function<void()> action)
{
    m_onLeftMouseButtonClickedAction = std::move(action);
}

void GuiButton::setOnRightMouseButtonClickedAction(std::function<void()> action)
{
    m_onRightMouseButtonClickedAction = std::move(action);
}

void GuiButton::setEnabled(bool value)
{
    m_enabled = value;
    if (!m_enabled) {
        m_visualState = VisualState::Disabled;
        m_pressed = false;
    } else if (m_focus) {
        m_visualState = VisualState::Hover;
    } else {
        m_visualState = VisualState::Normal;
    }
}

bool GuiButton::isEnabled() const
{
    return m_enabled;
}

void GuiButton::setVisualState(VisualState state)
{
    m_visualState = state;
    switch (state) {
        case VisualState::Disabled:
            m_enabled = false;
            m_pressed = false;
            m_focus = false;
            break;
        case VisualState::Pressed:
            m_pressed = true;
            m_focus = true;
            break;
        case VisualState::Hover:
            m_pressed = false;
            m_focus = true;
            break;
        case VisualState::Normal:
            m_pressed = false;
            m_focus = false;
            break;
    }
}

GuiButton::VisualState GuiButton::visualState() const
{
    return m_visualState;
}

void GuiButton::onNotifyKeyboardEvent(const cKeyboardEvent &)
{
}
