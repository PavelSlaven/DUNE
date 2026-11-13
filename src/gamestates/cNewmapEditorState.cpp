/**
 * @file cNewmapEditorState.cpp
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

#include "gamestates/cNewMapEditorState.h"
#include "game/GameStateTransition.hpp"
#include "game/ScenarioFlow.hpp"
#include "controls/cMouse.h"

#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "gui/GuiLabel.hpp"
#include "gui/GuiTextInput.h"
#include "gui/GuiCycleButton.h"
#include "gui/GuiCheckBox.hpp"
#include "gui/GuiTheme.hpp"
#include "gamestates/EditorTexts.hpp"
#include "gamestates/NewMapDialogLayout.hpp"
#include "drawers/SDLDrawer.hpp"
#include "context/GameContext.hpp"
#include "context/cGameObjectContext.h"
#include "drawers/cTextDrawer.h"
#include "gameobjects/map/cPreviewMaps.h"
#include "gameobjects/map/cRandomMapGenerator.h"
#include "gameobjects/map/SeedMapLoader.hpp"
#include "utils/ini.h"
#include "utils/Log.h"

#include "include/cAssert.h"
#include "context/TextContext.hpp"
#include "game/cGameSettings.h"
#include "gamestates/cGameState.h"
#include "include/sGameServices.h"
#include "include/eGameState.h"
#include "utils/Localization.hpp"
#include <charconv>
#include <chrono>
#include <optional>

static const int borderSize = 2;

cNewMapEditorState::cNewMapEditorState(sGameServices* services, cIni* ini)
    : cGameState(services),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_settings(services->settings),
    m_scenarioFlow(services->scenarioFlow),
    m_stateTransitions(services->stateTransitions),
    m_mouse(services->mouse),
    m_guiWindow(nullptr),
    m_objects(services->objects),
    m_previewMap(services->objects->getPreviewMaps()),
    m_cIni(ini)
{
    d2tm_assert(m_textDrawer != nullptr);
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_scenarioFlow != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    d2tm_assert(m_cIni != nullptr);
    constructWindow();
}

void cNewMapEditorState::constructWindow()
{
    const NewMapDialogLayout layout = NewMapDialogLayout::create(m_settings->getScreenW(), m_settings->getScreenH());
    m_titleRect = layout.title;

    const GuiTheme theme = GuiTheme::Remaster();
    GuiTheme panelTheme = theme;
    panelTheme.fillColor = Color{20, 25, 28, 255};
    panelTheme.borderLight = Color{188, 137, 42, 255};
    panelTheme.borderDark = Color{188, 137, 42, 255};
    m_guiWindow = std::make_unique<GuiWindow>(m_sdlDrawer, layout.panel, m_textDrawer);
    m_guiWindow->setTheme(panelTheme);

    const auto addLabel = [&](int row, EditorText text) {
        const cRectangle &cell = layout.labels[row];
        const int fontHeight = m_textDrawer->getFontHeight();
        auto label = GuiLabelBuilder()
            .withLabel(editorText(text))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .withTheme(theme)
            .withRect(cRectangle(cell.getX(), cell.getY() + (cell.getHeight() - fontHeight) / 2, cell.getWidth(), fontHeight))
            .build();
        m_guiWindow->addGuiObject(std::move(label));
    };
    const auto addInput = [&](int row) {
        auto input = std::make_unique<GuiTextInput>(m_sdlDrawer, layout.fields[row], m_textDrawer);
        input->setTheme(theme);
        GuiTextInput *result = input.get();
        m_guiWindow->addGuiObject(std::move(input));
        return result;
    };
    const auto addCycle = [&](int row) {
        const cRectangle &cell = layout.fields[row];
        auto cycle = GuiCycleButtonBuilder()
            .withRect(cRectangle(cell.getX(), cell.getY(), 80, cell.getHeight()))
            .withValues(m_sizesMap)
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(theme)
            .onChanged([this](int) {
                updateRandomCheckBox();
            })
            .build();
        GuiCycleButton *result = cycle.get();
        m_guiWindow->addGuiObject(std::move(cycle));
        return result;
    };

    addLabel(0, EditorText::NewMapName);
    m_inputName = addInput(0);
    addLabel(1, EditorText::NewMapAuthor);
    m_inputAuthor = addInput(1);
    addLabel(2, EditorText::NewMapDescription);
    m_inputDescription = addInput(2);
    addLabel(3, EditorText::NewMapWidth);
    m_cycleWidth = addCycle(3);
    addLabel(4, EditorText::NewMapHeight);
    m_cycleHeight = addCycle(4);

    addLabel(5, EditorText::NewMapRandom);
    const cRectangle &randomCell = layout.fields[5];
    auto checkRandom = GuiCheckBoxBuilder()
        .withRect(cRectangle(randomCell.getX(), randomCell.getY(), randomCell.getHeight(), randomCell.getHeight()))
        .withRenderer(m_sdlDrawer)
        .withTheme(theme)
        .onCheck([this]() {
            m_randomChecked = true;
        })
        .onUnCheck([this]() {
            m_randomChecked = false;
        })
        .build();
    checkRandom->setChecked(m_randomChecked); // GuiCheckBox starts checked
    m_checkRandom = checkRandom.get();
    m_guiWindow->addGuiObject(std::move(checkRandom));
    updateRandomCheckBox();

    addLabel(6, EditorText::NewMapSeed);
    m_inputSeed = addInput(6);

    auto returnButton = GuiButtonBuilder()
        .withRect(layout.returnButton)
        .withLabel(editorText(EditorText::NewMapReturn))
        .withTextDrawer(m_textDrawer)
        .withRenderer(m_sdlDrawer)
        .withTextAlign(GuiTextAlignHorizontal::CENTER)
        .withTheme(theme)
        .withKind(GuiRenderKind::REMASTER_BUTTON)
        .onClick([this]() {
            m_stateTransitions->setNextStateWithFade(eGameState::MENU);
        })
        .build();
    m_guiWindow->addGuiObject(std::move(returnButton));

    auto createButton = GuiButtonBuilder()
        .withRect(layout.createButton)
        .withLabel(editorText(EditorText::NewMapCreate))
        .withTextDrawer(m_textDrawer)
        .withRenderer(m_sdlDrawer)
        .withTheme(theme)
        .withKind(GuiRenderKind::REMASTER_BUTTON)
        .onClick([this](){
            this->constructEmptyMap();
            m_scenarioFlow->loadMapFromEditor(-1); // -1 means load the map from the editor, instead of loading a skirmish map
            m_stateTransitions->setNextStateWithFade(eGameState::EDITOR);
        })
        .build();
    m_guiWindow->addGuiObject(std::move(createButton));
}

cNewMapEditorState::~cNewMapEditorState()
{
    // Smart pointers handle cleanup
}

void cNewMapEditorState::thinkFast()
{

}

void cNewMapEditorState::draw() const
{
    m_sdlDrawer->renderRectFillColor(0, 0, m_settings->getScreenW(), m_settings->getScreenH(), Color{0, 0, 0, 190});
    m_guiWindow->draw();
    m_textDrawer->drawTextCentered(
        editorText(EditorText::NewMapTitle),
        m_titleRect.getX(),
        m_titleRect.getWidth(),
        m_titleRect.getY() + (m_titleRect.getHeight() - m_textDrawer->getFontHeight()) / 2,
        GuiTheme::Remaster().textColor
    );
    m_mouse->draw();
}

void cNewMapEditorState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    m_guiWindow->onNotifyMouseEvent(event);
}

eGameStateType cNewMapEditorState::getType()
{
    return GAMESTATE_NEW_MAP_EDITOR;
}

void cNewMapEditorState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    m_guiWindow->onNotifyKeyboardEvent(event);
}

bool cNewMapEditorState::isKeyboardCapturedByUi() const
{
    return m_guiWindow && m_guiWindow->hasFocusedInput();
}


// random maps need room: only allowed for sizes of minRandomMapSize or bigger
void cNewMapEditorState::updateRandomCheckBox()
{
    bool allowed = m_cycleWidth->getSelectedValue() >= minRandomMapSize &&
                   m_cycleHeight->getSelectedValue() >= minRandomMapSize;
    m_checkRandom->setEnabled(allowed);
    if (!allowed) {
        m_checkRandom->setChecked(false);
        m_randomChecked = false;
    }
}

void cNewMapEditorState::constructEmptyMap()
{
    // On récupère les valeurs localement pour être sûr
    std::string name = m_inputName->getText();
    if (name.empty()) {
        auto now = std::chrono::system_clock::now();
        name = std::format("New unnamed map {:%Y-%m-%d %H:%M:%S}", now);
    }
    std::string author = m_inputAuthor->getText();
    if (author.empty()) {
        author = "Unknown user";
    }
    std::string desc = m_inputDescription->getText();
    if (desc.empty()) {
        desc = "Made with D2TM: Internal Editor";
    }

    // a seed overrides the width and height settings
    const std::string &seedText = m_inputSeed->getText();
    if (!seedText.empty()) {
        int seed = 0;
        auto [ptr, ec] = std::from_chars(seedText.data(), seedText.data() + seedText.size(), seed);
        if (ec == std::errc() && ptr == seedText.data() + seedText.size()) {
            s_PreviewMap seedMap = SeedMapLoader::toPreviewMap(seed);
            seedMap.name = name;
            seedMap.author = author;
            seedMap.description = desc;
            m_previewMap->setEditorMap(std::move(seedMap));
            return;
        }
        Logger::warn(COMP_MAP, "cNewMapEditorState", "Seed [{}] is not a number, using width and height instead", seedText);
    }

    int width = m_cycleWidth->getSelectedValue()+borderSize;
    int height = m_cycleHeight->getSelectedValue()+borderSize;

    // a valid seed wins over Random, because it is the more specific request
    if (m_randomChecked) {
        s_PreviewMap randomMap;
        cRandomMapGenerator().generateRandomMap(width, height, 4, randomMap, m_objects);
        randomMap.validMap = true;
        randomMap.name = name;
        randomMap.author = author;
        randomMap.description = desc;
        m_previewMap->setEditorMap(std::move(randomMap));
        return;
    }
    m_previewMap->createEmptyMap(name, author, desc, width, height);
}