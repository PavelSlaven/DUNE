#pragma once

#include "controls/cKeyboardEvent.h"
#include "controls/sMouseEvent.h"
#include "utils/cRectangle.h"

#include <cstddef>
#include <functional>
#include <memory>
#include <string>
#include <vector>

class GuiButton;
class SDLDrawer;
class cGameSettings;
class cTextDrawer;

class ResolutionDialog {
public:
    ResolutionDialog(
        SDLDrawer *sdlDrawer,
        cTextDrawer *textDrawer,
        cGameSettings *settings,
        std::function<void(std::size_t)> onChosen
    );
    ~ResolutionDialog();

    void open(const std::vector<std::string> &labels, std::size_t selectedIndex);
    void close();
    [[nodiscard]] bool isOpen() const;
    void draw() const;
    void onMouseEvent(const s_MouseEvent &event);
    void onKeyboardEvent(const cKeyboardEvent &event);

private:
    friend class UiAuditAccess;

    void rebuildLayout();

    SDLDrawer *m_sdlDrawer;
    cTextDrawer *m_textDrawer;
    cGameSettings *m_settings;
    std::function<void(std::size_t)> m_onChosen;
    std::vector<std::string> m_labels;
    std::vector<cRectangle> m_choiceRects;
    std::vector<std::unique_ptr<GuiButton>> m_choiceButtons;
    cRectangle m_panelRect;
    cRectangle m_titleRect;
    cRectangle m_cancelRect;
    std::unique_ptr<GuiButton> m_cancelButton;
    std::size_t m_selectedIndex = 0;
    bool m_open = false;
};
