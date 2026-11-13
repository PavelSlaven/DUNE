#include "gamestates/ResolutionDialog.hpp"

#include "debug/UiAudit.hpp"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "game/cGameSettings.h"
#include "gui/GuiButton.h"
#include "gui/GuiTheme.hpp"
#include "utils/Localization.hpp"

#include <SDL3/SDL.h>

#include <utility>

ResolutionDialog::ResolutionDialog(
    SDLDrawer *sdlDrawer,
    cTextDrawer *textDrawer,
    cGameSettings *settings,
    std::function<void(std::size_t)> onChosen)
    : m_sdlDrawer(sdlDrawer)
    , m_textDrawer(textDrawer)
    , m_settings(settings)
    , m_onChosen(std::move(onChosen))
{
}

ResolutionDialog::~ResolutionDialog() = default;

void ResolutionDialog::open(
    const std::vector<std::string> &labels,
    std::size_t selectedIndex)
{
    m_labels = labels;
    m_selectedIndex = selectedIndex;
    rebuildLayout();
    m_open = true;
}

void ResolutionDialog::close()
{
    m_open = false;
}

bool ResolutionDialog::isOpen() const
{
    return m_open;
}

void ResolutionDialog::rebuildLayout()
{
    const int panelWidth = 420;
    const int innerMargin = 24;
    const int headingHeight = 40;
    const int buttonHeight = 40;
    const int rowStride = 48;
    const int panelHeight = 136 + static_cast<int>(m_labels.size()) * rowStride;
    const int panelX = (m_settings->getScreenW() - panelWidth) / 2;
    const int panelY = (m_settings->getScreenH() - panelHeight) / 2;
    const int contentWidth = panelWidth - innerMargin * 2;

    m_panelRect = cRectangle(panelX, panelY, panelWidth, panelHeight);
    m_titleRect = cRectangle(
        panelX + innerMargin,
        panelY + innerMargin,
        contentWidth,
        headingHeight
    );

    const int firstRowY = m_titleRect.getEndY() + 8;
    m_choiceRects.clear();
    m_choiceRects.reserve(m_labels.size());
    m_choiceButtons.clear();
    m_choiceButtons.reserve(m_labels.size());
    for (std::size_t index = 0; index < m_labels.size(); ++index) {
        const cRectangle rect(
            panelX + innerMargin,
            firstRowY + static_cast<int>(index) * rowStride,
            contentWidth,
            buttonHeight
        );
        m_choiceRects.push_back(rect);
        GuiTheme theme = GuiTheme::Remaster();
        if (index == m_selectedIndex) {
            theme.fillColor = Color{63, 52, 31, 255};
            theme.borderLight = Color{188, 137, 42, 255};
            theme.borderDark = Color{232, 184, 78, 255};
        }
        m_choiceButtons.push_back(GuiButtonBuilder()
            .withRect(rect)
            .withLabel(m_labels[index])
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(theme)
            .withKind(GuiRenderKind::REMASTER_BUTTON)
            .onClick([this, index]() {
                close();
                if (m_onChosen) {
                    m_onChosen(index);
                }
            })
            .build());
    }

    const int cancelY = firstRowY + static_cast<int>(m_labels.size()) * rowStride;
    m_cancelRect = cRectangle(
        panelX + innerMargin,
        cancelY,
        contentWidth,
        buttonHeight
    );
    m_cancelButton = GuiButtonBuilder()
        .withRect(m_cancelRect)
        .withLabel(localization::text("Cancel", "Отмена"))
        .withTextDrawer(m_textDrawer)
        .withRenderer(m_sdlDrawer)
        .withTheme(GuiTheme::Remaster())
        .withKind(GuiRenderKind::REMASTER_BUTTON)
        .onClick([this]() {
            close();
        })
        .build();
}

void ResolutionDialog::draw() const
{
    if (!m_open) {
        return;
    }
    if (uiaudit::isEnabled()) {
        uiaudit::dropClicksUnderModal();
        for (std::size_t index = 0; index < m_choiceRects.size(); ++index) {
            const cRectangle &choice = m_choiceRects[index];
            uiaudit::recordClick(
                ("resolution-choice:" + std::to_string(index)).c_str(),
                choice.getX(),
                choice.getY(),
                choice.getWidth(),
                choice.getHeight()
            );
        }
        uiaudit::recordClick(
            "resolution-cancel",
            m_cancelRect.getX(),
            m_cancelRect.getY(),
            m_cancelRect.getWidth(),
            m_cancelRect.getHeight()
        );
    }

    const Color overlay{0, 0, 0, 190};
    const Color panel{20, 25, 28, 255};
    const Color border{188, 137, 42, 255};
    m_sdlDrawer->renderRectFillColor(
        0,
        0,
        m_settings->getScreenW(),
        m_settings->getScreenH(),
        overlay
    );
    m_sdlDrawer->renderRectFillColor(m_panelRect, panel);
    m_sdlDrawer->renderRectColor(m_panelRect, border);
    m_textDrawer->drawTextCentered(
        localization::text("Screen resolution", "Разрешение экрана"),
        m_titleRect.getX(),
        m_titleRect.getWidth(),
        m_titleRect.getY() + (m_titleRect.getHeight() - m_textDrawer->getFontHeight()) / 2,
        border
    );
    for (const auto &button : m_choiceButtons) {
        button->draw();
    }
    m_cancelButton->draw();
}

void ResolutionDialog::onMouseEvent(const s_MouseEvent &event)
{
    if (!m_open) {
        return;
    }
    for (const auto &button : m_choiceButtons) {
        button->onNotifyMouseEvent(event);
    }
    m_cancelButton->onNotifyMouseEvent(event);
    if (!m_open || event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED) {
        return;
    }
    if (!m_panelRect.isPointWithin(event.coords.x, event.coords.y)) {
        close();
    }
}

void ResolutionDialog::onKeyboardEvent(const cKeyboardEvent &event)
{
    if (m_open && event.isType(eKeyEventType::PRESSED) && event.hasKey(SDL_SCANCODE_ESCAPE)) {
        close();
    }
}
