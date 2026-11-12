#pragma once

#include "controls/cKeyboardEvent.h"
#include "controls/sMouseEvent.h"
#include "save/SaveGameManager.hpp"
#include "utils/cRectangle.h"

#include <functional>
#include <memory>
#include <string>
#include <vector>

class GuiButton;
class SDLDrawer;
class SaveGameFlow;
class cGameSettings;
class cTextDrawer;

class SaveSlotsDialog {
public:
    SaveSlotsDialog(
        const SaveGameFlow *saveGameFlow,
        SDLDrawer *sdlDrawer,
        cTextDrawer *textDrawer,
        cGameSettings *settings,
        std::function<void()> onLoaded,
        std::function<void()> onSlotsChanged = {}
    );
    ~SaveSlotsDialog();

    void open(bool allowSaving, bool preferSaving);
    void close();
    [[nodiscard]] bool isOpen() const;
    [[nodiscard]] bool isCapturingText() const;

    void draw() const;
    void onMouseEvent(const s_MouseEvent &event);
    void onKeyboardEvent(const cKeyboardEvent &event);

private:
    friend class UiAuditAccess;

    void rebuildLayout();
    void refreshSlots();
    void selectSlot(int slot);
    void saveSelected();
    void loadSelected();
    void setEditingName(bool editing);
    void appendText(const std::string &text);
    void updateLoadButton();
    [[nodiscard]] const SaveSlotInfo *selectedInfo() const;
    [[nodiscard]] std::string fittedText(
        const std::string &text,
        int maximumWidth
    ) const;

    const SaveGameFlow *m_saveGameFlow;
    SDLDrawer *m_sdlDrawer;
    cTextDrawer *m_textDrawer;
    cGameSettings *m_settings;
    std::function<void()> m_onLoaded;
    std::function<void()> m_onSlotsChanged;
    std::vector<SaveSlotInfo> m_slots;
    std::vector<cRectangle> m_slotRects;
    cRectangle m_panelRect;
    cRectangle m_nameRect;
    cRectangle m_saveRect;
    cRectangle m_loadRect;
    cRectangle m_closeRect;
    std::unique_ptr<GuiButton> m_saveButton;
    std::unique_ptr<GuiButton> m_loadButton;
    std::unique_ptr<GuiButton> m_closeButton;
    int m_selectedSlot = 1;
    bool m_open = false;
    bool m_allowSaving = false;
    bool m_preferSaving = false;
    bool m_editingName = false;
    bool m_replaceNameOnInput = false;
    std::string m_name;
    std::string m_status;
};
