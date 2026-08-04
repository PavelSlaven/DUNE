#include "save/SaveSlotsDialog.hpp"

#include "cGame.h"
#include "d2tmc.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "save/SaveSlotName.hpp"
#include "utils/Localization.hpp"

#include <SDL2/SDL.h>

#include <algorithm>
#include <format>

SaveSlotsDialog::SaveSlotsDialog(
    cGame &game,
    cTextDrawer *textDrawer,
    std::function<void()> onLoaded,
    std::function<void()> onSlotsChanged)
    : m_game(game)
    , m_textDrawer(textDrawer)
    , m_onLoaded(std::move(onLoaded))
    , m_onSlotsChanged(std::move(onSlotsChanged))
{
}

SaveSlotsDialog::~SaveSlotsDialog()
{
    close();
}

void SaveSlotsDialog::open(bool allowSaving, bool preferSaving)
{
    m_allowSaving = allowSaving;
    m_preferSaving = allowSaving && preferSaving;
    m_status.clear();
    refreshSlots();
    rebuildLayout();

    int initialSlot = 1;
    if (m_preferSaving) {
        const auto empty = std::find_if(
            m_slots.begin(),
            m_slots.end(),
            [](const SaveSlotInfo &info) {
                return !info.exists;
            }
        );
        if (empty != m_slots.end()) {
            initialSlot = empty->slot;
        }
    }
    else {
        const auto existing = std::find_if(
            m_slots.begin(),
            m_slots.end(),
            [](const SaveSlotInfo &info) {
                return info.exists && info.valid;
            }
        );
        if (existing != m_slots.end()) {
            initialSlot = existing->slot;
        }
    }

    m_open = true;
    selectSlot(initialSlot);
    setEditingName(m_preferSaving);
}

void SaveSlotsDialog::close()
{
    if (m_editingName) {
        SDL_StopTextInput();
    }
    m_editingName = false;
    m_open = false;
}

bool SaveSlotsDialog::isOpen() const
{
    return m_open;
}

void SaveSlotsDialog::rebuildLayout()
{
    const int panelWidth = std::min(m_game.m_screenW - 24, 760);
    const int panelHeight = std::min(m_game.m_screenH - 24, 560);
    const int panelX = (m_game.m_screenW - panelWidth) / 2;
    const int panelY = (m_game.m_screenH - panelHeight) / 2;
    m_panelRect = cRectangle(panelX, panelY, panelWidth, panelHeight);

    const int margin = 14;
    m_nameRect = cRectangle(
        panelX + margin,
        panelY + 48,
        panelWidth - margin * 2,
        34
    );

    const int buttonY = panelY + panelHeight - 48;
    const int buttonGap = 8;
    const int buttonWidth =
        (panelWidth - margin * 2 - buttonGap * 2) / 3;
    m_saveRect = cRectangle(
        panelX + margin,
        buttonY,
        buttonWidth,
        34
    );
    m_loadRect = cRectangle(
        panelX + margin + buttonWidth + buttonGap,
        buttonY,
        buttonWidth,
        34
    );
    m_closeRect = cRectangle(
        panelX + margin + (buttonWidth + buttonGap) * 2,
        buttonY,
        buttonWidth,
        34
    );

    const int slotsY = panelY + 92;
    const int statusY = buttonY - 27;
    const int rowGap = 3;
    const int rowHeight = std::max(
        22,
        (statusY - 8 - slotsY -
         rowGap * (save_slot::MaximumSlots - 1)) /
        save_slot::MaximumSlots
    );
    m_slotRects.clear();
    m_slotRects.reserve(save_slot::MaximumSlots);
    for (int index = 0; index < save_slot::MaximumSlots; ++index) {
        m_slotRects.emplace_back(
            panelX + margin,
            slotsY + index * (rowHeight + rowGap),
            panelWidth - margin * 2,
            rowHeight
        );
    }
}

void SaveSlotsDialog::refreshSlots()
{
    m_slots = SaveGameManager::listSlots();
}

void SaveSlotsDialog::selectSlot(int slot)
{
    if (!save_slot::isValidSlot(slot)) {
        return;
    }
    m_selectedSlot = slot;
    const SaveSlotInfo *info = selectedInfo();
    m_name = info && info->valid
        ? info->name
        : save_slot::defaultName(slot);
    m_replaceNameOnInput = true;
    m_status.clear();
}

const SaveSlotInfo *SaveSlotsDialog::selectedInfo() const
{
    const auto found = std::find_if(
        m_slots.begin(),
        m_slots.end(),
        [this](const SaveSlotInfo &info) {
            return info.slot == m_selectedSlot;
        }
    );
    return found == m_slots.end() ? nullptr : &*found;
}

void SaveSlotsDialog::setEditingName(bool editing)
{
    editing = editing && m_allowSaving;
    if (editing == m_editingName) {
        return;
    }
    m_editingName = editing;
    if (m_editingName) {
        m_preferSaving = true;
        m_replaceNameOnInput = true;
        SDL_StartTextInput();
    }
    else {
        SDL_StopTextInput();
    }
}

void SaveSlotsDialog::saveSelected()
{
    if (!m_allowSaving) {
        return;
    }
    std::string cleanName = save_slot::sanitizeName(m_name);
    if (cleanName.empty()) {
        cleanName = save_slot::defaultName(m_selectedSlot);
    }
    std::string error;
    if (!SaveGameManager::saveGame(
            m_game,
            m_selectedSlot,
            cleanName,
            error)) {
        m_status = std::move(error);
        return;
    }
    refreshSlots();
    m_name = cleanName;
    m_replaceNameOnInput = true;
    m_status = localization::format(
        "Slot {} saved.", "Слот {} сохранён.", m_selectedSlot);
    if (m_onSlotsChanged) {
        m_onSlotsChanged();
    }
}

void SaveSlotsDialog::loadSelected()
{
    const SaveSlotInfo *info = selectedInfo();
    if (!info || !info->exists || !info->valid) {
        m_status = localization::text(
            "The selected slot has no valid save.",
            "В выбранном слоте нет корректного сохранения.");
        return;
    }
    std::string error;
    if (!SaveGameManager::loadGame(
            m_game,
            m_selectedSlot,
            error)) {
        m_status = std::move(error);
        refreshSlots();
        return;
    }
    close();
    if (m_onLoaded) {
        m_onLoaded();
    }
}

std::string SaveSlotsDialog::fittedText(
    const std::string &text,
    int maximumWidth) const
{
    if (m_textDrawer->getTextLength(text) <= maximumWidth) {
        return text;
    }
    std::string result = text;
    const std::string ellipsis = "...";
    while (!result.empty() &&
           m_textDrawer->getTextLength(result + ellipsis) >
               maximumWidth) {
        save_slot::removeLastUtf8Character(result);
    }
    return result + ellipsis;
}

void SaveSlotsDialog::draw() const
{
    if (!m_open) {
        return;
    }

    const Color overlay{0, 0, 0, 190};
    const Color panel{20, 25, 28, 255};
    const Color row{27, 33, 36, 255};
    const Color selected{63, 52, 31, 255};
    const Color border{188, 137, 42, 255};
    const Color text{232, 225, 202, 255};
    const Color inactive{114, 112, 104, 255};
    const Color error{235, 126, 96, 255};

    renderDrawer->renderRectFillColor(
        0,
        0,
        m_game.m_screenW,
        m_game.m_screenH,
        overlay
    );
    renderDrawer->renderRectFillColor(m_panelRect, panel);
    renderDrawer->renderRectColor(m_panelRect, border);

    m_textDrawer->drawTextCentered(
        localization::text("SAVED GAMES", "СОХРАНЕНИЯ"),
        m_panelRect.getX(),
        m_panelRect.getWidth(),
        m_panelRect.getY() + 12,
        border
    );

    renderDrawer->renderRectFillColor(m_nameRect, row);
    renderDrawer->renderRectColor(
        m_nameRect,
        m_editingName ? Color{232, 184, 78, 255} : border
    );
    std::string inputText = m_name;
    if (m_editingName) {
        inputText += " |";
    }
    inputText = fittedText(inputText, m_nameRect.getWidth() - 20);
    m_textDrawer->drawText(
        m_nameRect.getX() + 10,
        m_nameRect.getY() +
            (m_nameRect.getHeight() - m_textDrawer->getFontHeight()) / 2,
        text,
        inputText
    );

    for (std::size_t index = 0;
         index < m_slotRects.size() && index < m_slots.size();
         ++index) {
        const SaveSlotInfo &info = m_slots[index];
        const cRectangle &rect = m_slotRects[index];
        const bool isSelected = info.slot == m_selectedSlot;
        renderDrawer->renderRectFillColor(
            rect,
            isSelected ? selected : row
        );
        renderDrawer->renderRectColor(
            rect,
            isSelected ? Color{232, 184, 78, 255} : border
        );

        std::string label;
        Color labelColor = text;
        if (!info.exists) {
            label = localization::format(
                "{:02}. <empty>", "{:02}. <пусто>", info.slot);
            labelColor = inactive;
        }
        else if (!info.valid) {
            label = localization::format(
                "{:02}. <corrupted>", "{:02}. <повреждено>", info.slot);
            labelColor = error;
        }
        else {
            label = std::format("{:02}. {}", info.slot, info.name);
        }
        label = fittedText(label, rect.getWidth() - 18);
        m_textDrawer->drawText(
            rect.getX() + 9,
            rect.getY() +
                (rect.getHeight() - m_textDrawer->getFontHeight()) / 2,
            labelColor,
            label
        );
    }

    const auto drawButton = [
        this,
        border,
        text,
        inactive
    ](
        const cRectangle &rect,
        const std::string &label,
        bool enabled)
    {
        renderDrawer->renderRectFillColor(
            rect,
            enabled
                ? Color{35, 42, 45, 255}
                : Color{24, 28, 30, 255}
        );
        renderDrawer->renderRectColor(rect, enabled ? border : inactive);
        m_textDrawer->drawTextCenteredInBox(
            label,
            rect,
            enabled ? text : inactive
        );
    };

    const SaveSlotInfo *info = selectedInfo();
    drawButton(m_saveRect, localization::text("Save", "Сохранить"), m_allowSaving);
    drawButton(
        m_loadRect,
        localization::text("Load", "Загрузить"),
        info && info->exists && info->valid
    );
    drawButton(m_closeRect, localization::text("Close", "Закрыть"), true);

    if (!m_status.empty()) {
        m_textDrawer->drawTextCentered(
            fittedText(m_status, m_panelRect.getWidth() - 28),
            m_panelRect.getX(),
            m_panelRect.getWidth(),
            m_saveRect.getY() - 25,
            m_status.find(localization::text("saved", "сохранён")) != std::string::npos
                ? Color{148, 213, 146, 255}
                : error
        );
    }
}

void SaveSlotsDialog::onMouseEvent(const s_MouseEvent &event)
{
    if (!m_open ||
        event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED) {
        return;
    }
    for (std::size_t index = 0; index < m_slotRects.size(); ++index) {
        if (m_slotRects[index].isPointWithin(
                event.coords.x,
                event.coords.y)) {
            selectSlot(static_cast<int>(index) + 1);
            return;
        }
    }
    if (m_nameRect.isPointWithin(event.coords.x, event.coords.y)) {
        setEditingName(true);
        return;
    }
    if (m_saveRect.isPointWithin(event.coords.x, event.coords.y)) {
        saveSelected();
        return;
    }
    if (m_loadRect.isPointWithin(event.coords.x, event.coords.y)) {
        loadSelected();
        return;
    }
    if (m_closeRect.isPointWithin(event.coords.x, event.coords.y)) {
        close();
    }
}

void SaveSlotsDialog::onKeyboardEvent(const cKeyboardEvent &event)
{
    if (!m_open || event.eventType != eKeyEventType::PRESSED) {
        return;
    }
    if (event.hasKey(SDL_SCANCODE_ESCAPE)) {
        close();
        return;
    }
    if (event.hasKey(SDL_SCANCODE_UP)) {
        selectSlot(
            m_selectedSlot == 1
                ? save_slot::MaximumSlots
                : m_selectedSlot - 1
        );
        return;
    }
    if (event.hasKey(SDL_SCANCODE_DOWN)) {
        selectSlot(
            m_selectedSlot == save_slot::MaximumSlots
                ? 1
                : m_selectedSlot + 1
        );
        return;
    }
    if (event.hasKey(SDL_SCANCODE_BACKSPACE) && m_editingName) {
        if (m_replaceNameOnInput) {
            m_name.clear();
            m_replaceNameOnInput = false;
        }
        else {
            save_slot::removeLastUtf8Character(m_name);
        }
        return;
    }
    if (event.hasEitherKey(SDL_SCANCODE_RETURN, SDL_SCANCODE_KP_ENTER)) {
        if (m_preferSaving && m_allowSaving) {
            saveSelected();
        }
        else {
            loadSelected();
        }
    }
}

void SaveSlotsDialog::onTextInput(std::string_view text)
{
    if (!m_open || !m_editingName || text.empty()) {
        return;
    }
    if (m_replaceNameOnInput) {
        m_name.clear();
        m_replaceNameOnInput = false;
    }
    for (char character : text) {
        const unsigned char byte = static_cast<unsigned char>(character);
        if (byte >= 0x20U && byte != 0x7FU) {
            m_name.push_back(character);
        }
    }
    while (m_name.size() > save_slot::MaximumNameBytes) {
        save_slot::removeLastUtf8Character(m_name);
    }
}
