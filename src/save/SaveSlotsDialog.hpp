#pragma once

#include "controls/cKeyboardEvent.h"
#include "save/SaveGameManager.hpp"
#include "sMouseEvent.h"
#include "utils/cRectangle.h"

#include <functional>
#include <string>
#include <string_view>
#include <vector>

class cGame;
class cTextDrawer;

class SaveSlotsDialog {
public:
    SaveSlotsDialog(
        cGame &game,
        cTextDrawer *textDrawer,
        std::function<void()> onLoaded,
        std::function<void()> onSlotsChanged = {}
    );
    ~SaveSlotsDialog();

    void open(bool allowSaving, bool preferSaving);
    void close();
    [[nodiscard]] bool isOpen() const;

    void draw() const;
    void onMouseEvent(const s_MouseEvent &event);
    void onKeyboardEvent(const cKeyboardEvent &event);
    void onTextInput(std::string_view text);

private:
    void rebuildLayout();
    void refreshSlots();
    void selectSlot(int slot);
    void saveSelected();
    void loadSelected();
    void setEditingName(bool editing);
    [[nodiscard]] const SaveSlotInfo *selectedInfo() const;
    [[nodiscard]] std::string fittedText(
        const std::string &text,
        int maximumWidth
    ) const;

    cGame &m_game;
    cTextDrawer *m_textDrawer;
    std::function<void()> m_onLoaded;
    std::function<void()> m_onSlotsChanged;
    std::vector<SaveSlotInfo> m_slots;
    std::vector<cRectangle> m_slotRects;
    cRectangle m_panelRect;
    cRectangle m_nameRect;
    cRectangle m_saveRect;
    cRectangle m_loadRect;
    cRectangle m_closeRect;
    int m_selectedSlot = 1;
    bool m_open = false;
    bool m_allowSaving = false;
    bool m_preferSaving = false;
    bool m_editingName = false;
    bool m_replaceNameOnInput = false;
    std::string m_name;
    std::string m_status;
};
