/**
 * @file cEditorState.cpp
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

#include "gamestates/cEditorState.h"
#include "debug/UiAudit.hpp"
#include "gamestates/cEditorState/cEditorCam.h"
#include "gamestates/cEditorState/cEditorUndoRedoHistory.h"
#include "controls/eKeyAction.h"
#include "gui/GuiBar.h"
#include "gui/GuiStateButton.h"
#include "gui/GuiButton.h"
#include "gui/GuiButtonGroup.h"
#include "gui/GuiValueButton.h"
#include "data/gfxdata.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "utils/Graphics.hpp"
#include "context/GameContext.hpp"
#include "context/cGameObjectContext.h"
#include "game/cEventEmitter.h"
#include "game/GameStateTransition.hpp"
#include "controls/cMouse.h"
#include "gameobjects/map/cPreviewMaps.h"
#include "controls/cKeyBindings.h"
#include "include/Texture.hpp"
#include "controls/cKeyboard.h"
#include "drawers/CommandBarPolicy.hpp"
#include "gui/RemasterButtonFrame.hpp"
#include "include/sGameEvent.h"

#include "include/cAssert.h"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "game/cGameSettings.h"
#include "gamestates/cGameState.h"
#include "include/sGameServices.h"
#include "include/eGameState.h"
#include "utils/Localization.hpp"
#include <algorithm>
#include <cctype>
#include <memory>

const int heightBarSize = 48;
const int heightButtonSize = 40;
const int maxPenSize = 11; // must be odd to have a center
const Color editorGridColor = Color{128, 128, 128, 180};
const Color editorCenterLineColor = Color{32, 176, 32, 220};
const Color editorHoveredCellFillColor = Color{255, 230, 64, 96};
const Color editorHoveredCellBorderColor = Color{255, 230, 64, 220};
const Color editorSelectionFillColor = Color{255, 255, 255, 40};
const Color editorSelectionBorderColor = Color{255, 255, 255, 255};
const Color editorPasteGhostFillColor = Color{64, 208, 255, 60};
const Color editorPasteGhostBorderColor = Color{64, 208, 255, 220};
const Color editorPanelColor = Color{20, 25, 28, 255};
const Color editorPanelBorderColor = Color{188, 137, 42, 255};

namespace {
GuiTheme editorPanelTheme()
{
    GuiTheme theme = GuiTheme::Remaster();
    theme.fillColor = editorPanelColor;
    theme.borderLight = editorPanelBorderColor;
    theme.borderDark = editorPanelBorderColor;
    return theme;
}
}


cEditorState::cEditorState(sGameServices* services) 
    : cGameState(services),
    m_gfxdata(m_ctx->getGraphicsContext()->gfxdata.get()),
    m_settings(services->settings),
    m_eventEmitter(services->eventEmitter),
    m_keyboard(services->keyboard),
    m_stateTransitions(services->stateTransitions),
    m_mouse(services->mouse),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_previewMaps(services->objects->getPreviewMaps())
{
    d2tm_assert(m_gfxdata != nullptr);
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_eventEmitter != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    d2tm_assert(m_mouse != nullptr);
    d2tm_assert(m_textDrawer != nullptr);

    m_undoRedo = std::make_unique<cEditorUndoRedoHistory>();

    const cRectangle &selectRect = cRectangle(0, 0, m_settings->getScreenW(), heightBarSize);
    const cRectangle &modifRect = cRectangle(m_settings->getScreenW()-heightBarSize, heightBarSize, heightBarSize, m_settings->getScreenH()-heightBarSize);
    mapSizeArea = cRectangle(0,heightBarSize,m_settings->getScreenW()-heightBarSize,m_settings->getScreenH()-heightBarSize);
    m_editorCam = std::make_unique<cEditorCam>(mapSizeArea);
    m_selectBar = std::make_unique<GuiBar>(m_sdlDrawer, selectRect,GuiBarPlacement::HORIZONTAL,heightButtonSize);
    m_topologyBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    m_startCellBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    m_symmetricBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);

    m_selectBar->setTheme(editorPanelTheme());
    m_selectBar->beginPlacement(heightBarSize);
    m_topologyBar->setTheme(editorPanelTheme());
    m_topologyBar->beginPlacement(heightBarSize);
    m_startCellBar->setTheme(editorPanelTheme());
    m_startCellBar->beginPlacement(heightBarSize);
    m_symmetricBar->setTheme(editorPanelTheme());
    m_symmetricBar->beginPlacement(heightBarSize);

    populateSelectBar();
    populateTopologyBar();
    populateStartCellBar();
    populateSymmetricBar();
    setCurrentBar(m_topologyBar.get());
    startCells.fill({-1, -1});
}

cEditorState::~cEditorState()
{
}

std::string cEditorState::keyLabel(eKeyAction action) const
{
    const cKeyBindings *bindings = m_keyboard != nullptr ? m_keyboard->getKeyBindings() : nullptr;
    std::string name = bindings != nullptr ? bindings->getFirstKeyDisplayName(action) : std::string();
    std::ranges::transform(name, name.begin(), [](unsigned char character) {
        return static_cast<char>(std::toupper(character));
    });
    return name;
}

std::string cEditorState::groupKeyLabel(int number) const
{
    constexpr std::array<eKeyAction, 6> groupKeys{eKeyAction::GROUP_1, eKeyAction::GROUP_2, eKeyAction::GROUP_3,
                                                  eKeyAction::GROUP_4, eKeyAction::GROUP_5, eKeyAction::GROUP_6};
    return number >= 1 && number <= static_cast<int>(groupKeys.size()) ? keyLabel(groupKeys[number - 1]) : std::string();
}

void cEditorState::drawToolButton(const cRectangle &rect, bool selected, bool enabled, EditorText name,
                                  const std::string &key, const ToolContent &content) const
{
    const GuiTheme theme = enabled ? GuiTheme::Remaster() : GuiTheme::RemasterInactive();
    const bool hovered = enabled && m_mouse->getMouseCoords().isWithinRectangle(&rect);
    GuiTheme look = theme;
    Color contentColor = theme.textColor;
    if (selected) {
        look.fillColor = Color{63, 52, 31, 255};
        look.borderLight = Color{188, 137, 42, 255};
        look.borderDark = Color{232, 184, 78, 255};
    }
    if (enabled && (selected || hovered)) {
        contentColor = theme.textColorHover;
    }

    const cRectangle frame(rect.getX() + 2, rect.getY() + 2, rect.getWidth() - 4, rect.getHeight() - 4);
    drawRemasterButtonFrame(*m_sdlDrawer, frame, look, hovered, false);
    content(frame, contentColor);

    if (hovered) {
        m_tooltipText = commandTooltip(editorText(name), key);
        m_tooltipAnchor = rect;
    }
}

void cEditorState::drawIcon(const cRectangle &frame, EditorIcon icon, Color color) const
{
    const int side = std::min(frame.getWidth(), frame.getHeight()) * 85 / 100;
    if (Texture *texture = m_icons.get(*m_sdlDrawer, icon, side)) {
        SDL_SetTextureColorMod(texture->tex.get(), color.r, color.g, color.b);
        m_sdlDrawer->renderTexture(texture->tex.get(), frame.getX() + (frame.getWidth() - side) / 2,
                                   frame.getY() + (frame.getHeight() - side) / 2, side, side, color.a);
    }
}

void cEditorState::drawTooltip() const
{
    if (m_tooltipText.empty()) {
        return;
    }
    constexpr int padding = 6;
    constexpr int gap = 6;
    const GuiTheme theme = GuiTheme::Remaster();
    const int width = m_textDrawer->getTextLength(m_tooltipText) + padding * 2;
    const int height = m_textDrawer->getFontHeight() + padding * 2;
    const int screenW = m_settings->getScreenW();
    const int screenH = m_settings->getScreenH();
    int x = 0;
    int y = 0;
    if (m_tooltipAnchor.getY() < heightBarSize) {
        x = m_tooltipAnchor.getX() + m_tooltipAnchor.getWidth() / 2 - width / 2;
        y = m_tooltipAnchor.getEndY() + gap;
    } else {
        x = m_tooltipAnchor.getX() - gap - width;
        y = m_tooltipAnchor.getY() + m_tooltipAnchor.getHeight() / 2 - height / 2;
    }
    const cRectangle box(std::clamp(x, 0, std::max(0, screenW - width)), std::clamp(y, 0, std::max(0, screenH - height)), width, height);
    m_sdlDrawer->renderRectFillColor(box, theme.fillColor);
    m_sdlDrawer->renderRectColor(box, theme.borderLight);
    m_textDrawer->drawText(box.getX() + padding, box.getY() + padding, theme.textColor, m_tooltipText);
}

void cEditorState::addToolButton(GuiBar &bar, GuiButtonGroup &group, bool initiallySelected, EditorText name,
                                 const std::string &key, ToolContent content, std::function<void()> onClick)
{
    auto button = GuiStateButtonBuilder()
            .withRect(cRectangle(0, 0, heightButtonSize, heightButtonSize))
            .withRenderer(m_sdlDrawer)
            .onClick(std::move(onClick))
            .build();
    button->setCustomDraw([this, name, key, content = std::move(content)](const cRectangle &rect, bool selected, bool enabled) {
        drawToolButton(rect, selected, enabled, name, key, content);
    });
    button->setGroup(&group);
    if (initiallySelected) {
        group.updateStates(button.get());
    }
    bar.addAutoGuiObject(std::move(button));
}

void cEditorState::populateSelectBar()
{
    m_selectGroup = std::make_unique<GuiButtonGroup>();
    const auto iconContent = [this](EditorIcon icon) {
        return [this, icon](const cRectangle &frame, Color color) { drawIcon(frame, icon, color); };
    };
    addToolButton(*m_selectBar, *m_selectGroup, true, EditorText::ModeTerrain, "", iconContent(EditorIcon::Terrain),
                  [this]() { setCurrentBar(m_topologyBar.get()); });
    addToolButton(*m_selectBar, *m_selectGroup, false, EditorText::ModeStartPoints, "", iconContent(EditorIcon::StartFlag),
                  [this]() { setCurrentBar(m_startCellBar.get()); });
    addToolButton(*m_selectBar, *m_selectGroup, false, EditorText::ModeSymmetry, "", iconContent(EditorIcon::Symmetry),
                  [this]() { setCurrentBar(m_symmetricBar.get()); });

    const auto rectGui = cRectangle(m_settings->getScreenW()-heightButtonSize*3, (heightBarSize-heightButtonSize)/2, heightButtonSize, heightButtonSize);
    auto guiIcon = GuiButtonBuilder()
            .withRect(rectGui)
            .withRenderer(m_sdlDrawer)
            .onClick([this]() {
                if (saveMap()) {
                    m_hasChanged = false;
                }
            })
            .build();
    guiIcon->setCustomDraw([this](const cRectangle &rect, bool selected, bool enabled) {
        drawToolButton(rect, selected, enabled, EditorText::Save, keyLabel(eKeyAction::EDITOR_SAVE),
                       [this](const cRectangle &frame, Color color) { drawIcon(frame, EditorIcon::Save, color); });
    });
    m_selectBar->addGuiObject(std::move(guiIcon));
}

void cEditorState::populateTopologyBar()
{
    m_topologyGroup = std::make_unique<GuiButtonGroup>();
    struct Terrain {
        int tile;
        EditorText name;
    };
    const std::array<Terrain, 6> terrains{{
        {TERRAIN_HILL, EditorText::TerrainHill},
        {TERRAIN_MOUNTAIN, EditorText::TerrainMountain},
        {TERRAIN_ROCK, EditorText::TerrainRock},
        {TERRAIN_SAND, EditorText::TerrainSand},
        {TERRAIN_SPICE, EditorText::TerrainSpice},
        {TERRAIN_SPICEHILL, EditorText::TerrainSpiceHill},
    }};
    for (int index = 0; index < static_cast<int>(terrains.size()); ++index) {
        const int tile = terrains[index].tile;
        addToolButton(*m_topologyBar, *m_topologyGroup, tile == TERRAIN_SAND, terrains[index].name, groupKeyLabel(index + 1),
                      [this, tile](const cRectangle &frame, Color) {
                          const cRectangle inner(frame.getX() + 4, frame.getY() + 4, frame.getWidth() - 8, frame.getHeight() - 8);
                          m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(tile), cRectangle{0, 0, 32, 32}, inner);
                      },
                      [this, tile]() { idTerrainToMapModif = tile; });
    }

    auto cursorSizeButton = GuiValueButtonBuilder()
            .withRect(cRectangle(0, 0, heightButtonSize, heightButtonSize))
            .withRenderer(m_sdlDrawer)
            .withInitialValue(m_topologyCursorSize)
            .withStepValue(2)
            .withMinValue(1)
            .withMaxValue(maxPenSize)
            .onChanged([this](int value) {
                setCursorSize(value);
            })
            .build();
    cursorSizeButton->setCustomDraw([this](const cRectangle &rect, bool selected, bool enabled) {
        drawToolButton(rect, selected, enabled, EditorText::BrushSize, "",
                       [this](const cRectangle &frame, Color color) {
                           m_textDrawer->drawTextCenteredInBox(std::to_string(m_topologyCursorSize), frame, color);
                       });
    });
    m_topologyBar->addAutoGuiObject(std::move(cursorSizeButton));
}

void cEditorState::populateStartCellBar()
{
    m_startCellGroup = std::make_unique<GuiButtonGroup>();
    constexpr std::array<EditorText, 5> names{EditorText::StartPoint1, EditorText::StartPoint2, EditorText::StartPoint3,
                                              EditorText::StartPoint4, EditorText::StartPoint5};
    for (int index = 0; index < static_cast<int>(names.size()); ++index) {
        const EditorIcon icon = static_cast<EditorIcon>(static_cast<int>(EditorIcon::Start1) + index);
        addToolButton(*m_startCellBar, *m_startCellGroup, index == 0, names[index], groupKeyLabel(index + 1),
                      [this, icon](const cRectangle &frame, Color color) { drawIcon(frame, icon, color); },
                      [this, index]() { idStartCellPlayer = index; });
    }
}

void cEditorState::populateSymmetricBar()
{
    m_symmetricGroup = std::make_unique<GuiButtonGroup>();
    struct Mirror {
        EditorIcon icon;
        EditorText name;
        Direction direction;
    };
    const std::array<Mirror, 8> mirrors{{
        {EditorIcon::CopyRight, EditorText::MirrorRight, Direction::right},
        {EditorIcon::CopyLeft, EditorText::MirrorLeft, Direction::left},
        {EditorIcon::CopyUp, EditorText::MirrorUp, Direction::top},
        {EditorIcon::CopyDown, EditorText::MirrorDown, Direction::bottom},
        {EditorIcon::CopyBottomLeft, EditorText::MirrorBottomLeft, Direction::bottomLeft},
        {EditorIcon::CopyBottomRight, EditorText::MirrorBottomRight, Direction::bottomRight},
        {EditorIcon::CopyTopLeft, EditorText::MirrorTopLeft, Direction::topLeft},
        {EditorIcon::CopyTopRight, EditorText::MirrorTopRight, Direction::topRight},
    }};
    for (int index = 0; index < static_cast<int>(mirrors.size()); ++index) {
        const Mirror mirror = mirrors[index];
        addToolButton(*m_symmetricBar, *m_symmetricGroup, false, mirror.name, groupKeyLabel(index + 1),
                      [this, icon = mirror.icon](const cRectangle &frame, Color color) { drawIcon(frame, icon, color); },
                      [this, direction = mirror.direction]() { modifySymmetricArea(direction); });
    }
}

void cEditorState::thinkFast()
{
}

void cEditorState::draw() const
{
    if (uiaudit::isEnabled()) {
        uiaudit::recordArea("editor-map", mapSizeArea.getX(), mapSizeArea.getY(), mapSizeArea.getWidth(),
                            mapSizeArea.getHeight());
    }
    m_tooltipText.clear();
    drawMap();
    drawHoveredCellHighlight();
    drawSelectionRectangle();
    if (m_displayPastPreview)
        drawPastePreviewGhost();
    if (m_displayGrid)
        drawGrid();
    if (m_displayAxes)
        drawAxes();
    if (m_currentBar == m_startCellBar.get())
        drawStartCells();
    m_selectBar->draw();
    m_currentBar->draw();
    drawTooltip();
    m_mouse->draw();
}

void cEditorState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (m_mapData == nullptr) {
        return;
    }

    if (event.eventType == MOUSE_RIGHT_BUTTON_CLICKED) {
        if (m_hasSelection) {
            const int selectionWidth = m_selectionEndTileX - m_selectionStartTileX + 1;
            const int selectionHeight = m_selectionEndTileY - m_selectionStartTileY + 1;
            if (selectionWidth * selectionHeight < 2) {
                m_hasSelection = false;
            }
        }
        m_isDraggingSelection = false;
    }

    if (event.coords.isWithinRectangle(&mapSizeArea)) {
        // Zoom centered on the cursor
        int mouseX = event.coords.x;
        int mouseY = event.coords.y - mapSizeArea.getY(); // offset barre
        if (event.eventType == MOUSE_SCROLLED_DOWN) {
            m_editorCam->zoomAtMapPosition(mouseX, mouseY, cEditorCam::ZoomDirection::zoomOut, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        } else if (event.eventType == MOUSE_SCROLLED_UP) {
            m_editorCam->zoomAtMapPosition(mouseX, mouseY, cEditorCam::ZoomDirection::zoomIn, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        } else if (event.eventType == MOUSE_RIGHT_BUTTON_PRESSED) {
            int tileX = 0;
            int tileY = 0;
            if (tryGetTileFromMouseCoords(event.coords, tileX, tileY) && isEditableTile(tileX, tileY)) {
                if (!m_isDraggingSelection) {
                    m_selectionAnchorTileX = tileX;
                    m_selectionAnchorTileY = tileY;
                    m_isDraggingSelection = true;
                    m_hasSelection = true;
                }
                updateSelectionFromTiles(m_selectionAnchorTileX, m_selectionAnchorTileY, tileX, tileY);
            }
        } else if (event.eventType == MOUSE_MOVED_TO && m_isDraggingSelection) {
            int tileX = 0;
            int tileY = 0;
            if (tryGetTileFromMouseCoords(event.coords, tileX, tileY)) {
                updateSelectionFromTiles(m_selectionAnchorTileX, m_selectionAnchorTileY, tileX, tileY);
            }
        } else if (event.eventType == MOUSE_LEFT_BUTTON_PRESSED && m_currentBar == m_topologyBar.get()) {
            modifyTile(mouseX, mouseY, idTerrainToMapModif);
        }else if (event.eventType == MOUSE_LEFT_BUTTON_PRESSED && m_currentBar == m_startCellBar.get()) {
            modifyStartCell(mouseX, mouseY, idStartCellPlayer);
        }        
        else {
            return;
        }
	// to test : updateVisibleTiles();
    } else {
        m_selectBar->onNotifyMouseEvent(event);
        m_currentBar->onNotifyMouseEvent(event);
    }
}

eGameStateType cEditorState::getType()
{
    return GAMESTATE_EDITOR;
}

void cEditorState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (m_mapData == nullptr) {
        if (event.isType(eKeyEventType::PRESSED) && event.isAction(eKeyAction::MENU_BACK)) {
            m_stateTransitions->setNextStateWithFade(eGameState::MENU);
        }
        return;
    }
    if (event.isType(eKeyEventType::PRESSED)) {
        if (event.isAction(eKeyAction::MENU_BACK)) {
            if (m_hasChanged) {
                // saveMap() notifies the user when it fails, still leave the editor
                saveMap(true);
                m_hasChanged = false;
            }
            m_stateTransitions->setNextState(eGameState::OPTIONS);
        }
        if (event.isAction(eKeyAction::EDITOR_SAVE)) {
            //std::cout << "Save" << std::endl;
            if (saveMap()) {
                m_hasChanged = false;
            }
        }
        if (event.isAction(eKeyAction::EDITOR_ZOOM_IN)) {
            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomIn, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        }
        if (event.isAction(eKeyAction::EDITOR_ZOOM_OUT)) {
            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomOut, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        }
        // to test : updateVisibleTiles();
        //m_selectBar->onNotifyKeyboardEvent(event);
        m_currentBar->onNotifyKeyboardEvent(event);

        if (event.isAction(eKeyAction::EDITOR_DISPLAY_GRID)) {
            // toggle grid display
            //std::cout << "Toggle grid display" << std::endl;
            m_displayGrid = !m_displayGrid;

        }
        if (event.isAction(eKeyAction::EDITOR_DISPLAY_AXES)) {
            // toggle axes display
            //std::cout << "Toggle axes display" << std::endl;
            m_displayAxes = !m_displayAxes;
        }
        if (event.isAction(eKeyAction::EDITOR_UNDO)) {
            if (m_undoRedo->applyUndo(*m_mapData, startCells)) {
                m_hasChanged = true;
            }
        }
        if (event.isAction(eKeyAction::EDITOR_REDO)) {
            if (m_undoRedo->applyRedo(*m_mapData, startCells)) {
                m_hasChanged = true;
            }
        }
        if (event.isAction(eKeyAction::EDITOR_COPY)) {
            //std::cout << "Action : Copy selection to clipboard" << std::endl;
            copySelectionToClipboard();
        }
        if (event.isAction(eKeyAction::EDITOR_PASTE)) {
            //std::cout << "Action : Paste selection to clipboard" << std::endl;
            pasteClipboardAtMouseCursor();
        }
        if (event.isAction(eKeyAction::EDITOR_CUT)) {
            cutSelectionToClipboard();
        }

        if (!event.isCtrlPressed()) {
            m_displayPastPreview = false;
        }
    }

    if (event.isType(eKeyEventType::HOLD)) {
        if (event.isAction(eKeyAction::SCROLL_LEFT)) {
            m_editorCam->scrollByTiles(-1, 0, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        }
        if (event.isAction(eKeyAction::SCROLL_RIGHT)) {
            m_editorCam->scrollByTiles(1, 0, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        }
        if (event.isAction(eKeyAction::SCROLL_UP)) {
            m_editorCam->scrollByTiles(0, -1, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        }
        if (event.isAction(eKeyAction::SCROLL_DOWN)) {
            m_editorCam->scrollByTiles(0, 1, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
        }
        if (event.isShiftPressed() && event.isAction(eKeyAction::SCROLL_UP)) {
            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomIn, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
            return;
        }
        if (event.isShiftPressed() && event.isAction(eKeyAction::SCROLL_DOWN)) {
            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomOut, *m_mapData);
            m_editorCam->updateVisibleTiles(*m_mapData);
            return;
        }
        if (event.isCtrlPressed()) {
            m_displayPastPreview = true;
        }
        //to test : updateVisibleTiles();
    }
}

void cEditorState::loadMap(int mapIndex)
{
    s_PreviewMap* map = m_previewMaps->getMap(mapIndex);
    //std::cout << "open |"<< map->name << "|" << std::endl;
    m_mapData = std::make_unique<Matrix<int>>(map->terrainType, map->height, map->width);
    m_mapAuthor = map->author;
    m_mapDescription = map->description;
    m_mapName = map->name;
    startCells.fill({-1, -1});
    for (int i=0; i<MAX_SKIRMISHMAP_PLAYERS; i++) {
        if (map->iStartCell[i] !=-1) {
            //std::cout << "startCell " << map->iStartCell[i] << std::endl;
            int w = map->iStartCell[i] % map->width;
            int h = map->iStartCell[i] / map->width;
            startCells[i] = cPoint(w,h);
        }
    }
    m_editorCam->reset();
    m_editorCam->updateVisibleTiles(*m_mapData);
    normalizeModifications();
    m_displayGrid = false;
    m_displayAxes = false;
    m_displayPastPreview = false;
    m_hasChanged = false;
    m_hasSelection = false;
    m_isDraggingSelection = false;
    m_undoRedo->clear();
}

void cEditorState::setCursorSize(int value)
{
    int normalizedValue = std::max(1, value);
    if (normalizedValue % 2 == 0) {
        normalizedValue += 1;
    }

    normalizedValue = std::min(normalizedValue, maxPenSize);
    if (normalizedValue % 2 == 0) {
        normalizedValue -= 1;
    }

    m_topologyCursorSize = normalizedValue;
    m_cursorSize = getActiveCursorSize();
}

void cEditorState::setCurrentBar(GuiBar* bar)
{
    m_currentBar = bar;
    m_cursorSize = getActiveCursorSize();
}

int cEditorState::getActiveCursorSize() const
{
    if (m_currentBar == m_topologyBar.get()) {
        return m_topologyCursorSize;
    }

    return 1;
}

void cEditorState::normalizeModifications()
{
    for (size_t j = 0; j < m_mapData->getRows(); j++) {
        (*m_mapData)[j][0] = -1;
        (*m_mapData)[j][m_mapData->getCols()-1] = -1;
    }
    for (size_t i = 0; i < m_mapData->getCols(); i++) {
        (*m_mapData)[0][i] = -1;
        (*m_mapData)[m_mapData->getRows()-1][i] = -1;
    }
}

void cEditorState::drawMap() const
{
    if (m_mapData == nullptr) {
        return;
    }

    const int cameraX = m_editorCam->getCameraX();
    const int cameraY = m_editorCam->getCameraY();
    const int tileLenSize = m_editorCam->getTileSize();
    const int startX = m_editorCam->getStartX();
    const int startY = m_editorCam->getStartY();
    const size_t endX = m_editorCam->getEndX();
    const size_t endY = m_editorCam->getEndY();
    
    int tileID;
    int tile_world_x, tile_world_y;
    int tile_screen_x, tile_screen_y;

    cRectangle destRect;
    cRectangle srcRect{0,0,32,32}; // we take the first full textured sprite
    for (size_t j = static_cast<size_t>(startY); j < endY; j++) {
        for (size_t i = static_cast<size_t>(startX); i < endX; i++) {
            // Ideal position in pixels if the map started at (0,0)
            tile_world_x = i * tileLenSize;
            tile_world_y = j * tileLenSize;
            // Rendering position on the screen (including camera offset)
            tile_screen_x = tile_world_x - cameraX;
            tile_screen_y = tile_world_y - cameraY;
            
            destRect= cRectangle(tile_screen_x, heightBarSize+tile_screen_y,tileLenSize,tileLenSize);
           
            tileID = (*m_mapData)[j][i];
            switch (tileID)
            {
            case TERRAIN_SPICE:
                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_SPICE), srcRect, destRect);
                break;
            case TERRAIN_SAND:
                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_SAND), srcRect, destRect);
                break;
            case TERRAIN_MOUNTAIN:
                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_MOUNTAIN), srcRect, destRect);
                break;
            case TERRAIN_ROCK:
                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_ROCK), srcRect, destRect);
                break;
            case TERRAIN_SPICEHILL:
                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_SPICEHILL), srcRect, destRect);
                break;  
            case TERRAIN_HILL:
                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_HILL), srcRect, destRect);
                break;            
            default:
                break;
            }
        }
    }
}

void cEditorState::drawHoveredCellHighlight() const
{
    if (m_mapData == nullptr) {
        return;
    }

    cMouse *mouse = m_mouse;
    if (mouse == nullptr) {
        return;
    }

    const cPoint mouseCoords = mouse->getMouseCoords();
    if (!mouseCoords.isWithinRectangle(&mapSizeArea)) {
        return;
    }

    const int mouseMapX = mouseCoords.x;
    const int mouseMapY = mouseCoords.y - mapSizeArea.getY();
    const int cameraX = m_editorCam->getCameraX();
    const int cameraY = m_editorCam->getCameraY();
    const int tileLenSize = m_editorCam->getTileSize();

    const int tileX = (cameraX + mouseMapX) / tileLenSize;
    const int tileY = (cameraY + mouseMapY) / tileLenSize;

    if (tileX < 0 || tileY < 0 || tileX >= static_cast<int>(m_mapData->getCols()) || tileY >= static_cast<int>(m_mapData->getRows())) {
        return;
    }

    int highlightStartTileX = 0;
    int highlightStartTileY = 0;
    int highlightEndTileX = 0;
    int highlightEndTileY = 0;
    getBrushTileBounds(tileX, tileY, highlightStartTileX, highlightStartTileY, highlightEndTileX, highlightEndTileY);

    if (highlightStartTileX > highlightEndTileX || highlightStartTileY > highlightEndTileY) {
        return;
    }

    const int cellScreenX = highlightStartTileX * tileLenSize - cameraX;
    const int cellScreenY = heightBarSize + highlightStartTileY * tileLenSize - cameraY;
    const int highlightWidth = (highlightEndTileX - highlightStartTileX + 1) * tileLenSize;
    const int highlightHeight = (highlightEndTileY - highlightStartTileY + 1) * tileLenSize;

    cRectangle cellRect(cellScreenX, cellScreenY, highlightWidth, highlightHeight);
    m_sdlDrawer->renderRectFillColor(cellRect, editorHoveredCellFillColor, editorHoveredCellFillColor.a);
    m_sdlDrawer->renderRectColor(cellRect, editorHoveredCellBorderColor, editorHoveredCellBorderColor.a);
}

void cEditorState::drawSelectionRectangle() const
{
    if (m_mapData == nullptr || !m_hasSelection) {
        return;
    }
    const int cameraX = m_editorCam->getCameraX();
    const int cameraY = m_editorCam->getCameraY();
    const int tileLenSize = m_editorCam->getTileSize();

    const int cellScreenX = m_selectionStartTileX * tileLenSize - cameraX;
    const int cellScreenY = heightBarSize + m_selectionStartTileY * tileLenSize - cameraY;
    const int highlightWidth = (m_selectionEndTileX - m_selectionStartTileX + 1) * tileLenSize;
    const int highlightHeight = (m_selectionEndTileY - m_selectionStartTileY + 1) * tileLenSize;

    cRectangle selectionRect(cellScreenX, cellScreenY, highlightWidth, highlightHeight);
    m_sdlDrawer->renderRectFillColor(selectionRect, editorSelectionFillColor, editorSelectionFillColor.a);
    m_sdlDrawer->renderRectColor(selectionRect, editorSelectionBorderColor, editorSelectionBorderColor.a);
}

void cEditorState::drawPastePreviewGhost() const
{
    if (m_mapData == nullptr || m_clipboardTiles.empty() || m_clipboardTiles.front().empty()) {
        return;
    }

    cMouse *mouse = m_mouse;
    int anchorTileX = 0;
    int anchorTileY = 0;
    if (!tryGetEditableTileFromMouseCoords(mouse->getMouseCoords(), anchorTileX, anchorTileY)) {
        return;
    }

    const int widthInTiles = static_cast<int>(m_clipboardTiles.front().size());
    const int heightInTiles = static_cast<int>(m_clipboardTiles.size());
    if (widthInTiles <= 0 || heightInTiles <= 0) {
        return;
    }

    const int cameraX = m_editorCam->getCameraX();
    const int cameraY = m_editorCam->getCameraY();
    const int tileLenSize = m_editorCam->getTileSize();

    const int cellScreenX = anchorTileX * tileLenSize - cameraX;
    const int cellScreenY = heightBarSize + anchorTileY * tileLenSize - cameraY;
    const int ghostWidth = widthInTiles * tileLenSize;
    const int ghostHeight = heightInTiles * tileLenSize;

    cRectangle ghostRect(cellScreenX, cellScreenY, ghostWidth, ghostHeight);
    m_sdlDrawer->renderRectFillColor(ghostRect, editorPasteGhostFillColor, editorPasteGhostFillColor.a);
    m_sdlDrawer->renderRectColor(ghostRect, editorPasteGhostBorderColor, editorPasteGhostBorderColor.a);
}

bool cEditorState::tryGetTileFromMouseCoords(const cPoint &coords, int &tileX, int &tileY) const
{
    if (!coords.isWithinRectangle(&mapSizeArea)) {
        return false;
    }

    tileX = m_editorCam->screenToTileX(coords.x);
    tileY = m_editorCam->screenToTileY(coords.y - mapSizeArea.getY());
    if (tileX < 0 || tileY < 0 || tileX >= static_cast<int>(m_mapData->getCols()) || tileY >= static_cast<int>(m_mapData->getRows())) {
        return false;
    }

    return true;
}

bool cEditorState::tryGetEditableTileFromMouseCoords(const cPoint &coords, int &tileX, int &tileY) const
{
    if (m_mapData == nullptr || !tryGetTileFromMouseCoords(coords, tileX, tileY)) {
        return false;
    }

    const int minX = 1;
    const int minY = 1;
    const int maxX = static_cast<int>(m_mapData->getCols()) - 2;
    const int maxY = static_cast<int>(m_mapData->getRows()) - 2;
    if (maxX < minX || maxY < minY) {
        return false;
    }

    tileX = std::clamp(tileX, minX, maxX);
    tileY = std::clamp(tileY, minY, maxY);
    return true;
}

bool cEditorState::isEditableTile(int tileX, int tileY) const
{
    if (m_mapData == nullptr) {
        return false;
    }

    return tileX >= 1 && tileY >= 1 && tileX < static_cast<int>(m_mapData->getCols()) - 1 && tileY < static_cast<int>(m_mapData->getRows()) - 1;
}

void cEditorState::updateSelectionFromTiles(int startTileX, int startTileY, int endTileX, int endTileY)
{
    if (m_mapData == nullptr) {
        return;
    }

    const int minX = 1;
    const int minY = 1;
    const int maxX = static_cast<int>(m_mapData->getCols()) - 2;
    const int maxY = static_cast<int>(m_mapData->getRows()) - 2;

    startTileX = std::clamp(startTileX, minX, maxX);
    startTileY = std::clamp(startTileY, minY, maxY);
    endTileX = std::clamp(endTileX, minX, maxX);
    endTileY = std::clamp(endTileY, minY, maxY);

    m_selectionStartTileX = std::min(startTileX, endTileX);
    m_selectionStartTileY = std::min(startTileY, endTileY);
    m_selectionEndTileX = std::max(startTileX, endTileX);
    m_selectionEndTileY = std::max(startTileY, endTileY);
    m_hasSelection = true;
}

void cEditorState::cutSelectionToClipboard()
{
    if (m_mapData == nullptr || !m_hasSelection) {
        return;
    }
    copySelectionToClipboard();
    const int width = m_selectionEndTileX - m_selectionStartTileX + 1;
    const int height = m_selectionEndTileY - m_selectionStartTileY + 1;
    if (width <= 0 || height <= 0 || (width * height) < 2) {
        return;
    }
    m_undoRedo->beginRecordGroup();
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            auto oldTileID = (*m_mapData)[m_selectionStartTileY + y][m_selectionStartTileX + x];
            m_undoRedo->recordTileChange(m_selectionStartTileX + x, m_selectionStartTileY + y, oldTileID, TERRAIN_SAND);
            (*m_mapData)[m_selectionStartTileY + y][m_selectionStartTileX + x] = TERRAIN_SAND;
        }
    }
    m_hasChanged = true;
}

void cEditorState::copySelectionToClipboard()
{
    if (m_mapData == nullptr || !m_hasSelection) {
        return;
    }
    const int width = m_selectionEndTileX - m_selectionStartTileX + 1;
    const int height = m_selectionEndTileY - m_selectionStartTileY + 1;
    if (width <= 0 || height <= 0 || (width * height) < 2) {
        return;
    }

    m_clipboardTiles.assign(height, std::vector<int>(width, TERRAIN_SAND));
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            m_clipboardTiles[y][x] = (*m_mapData)[m_selectionStartTileY + y][m_selectionStartTileX + x];
        }
    }
    m_hasSelection = false;
}

void cEditorState::pasteClipboardAtMouseCursor()
{
    if (m_mapData == nullptr || m_clipboardTiles.empty() || m_clipboardTiles.front().empty()) {
        return;
    }

    cMouse *mouse = m_mouse;
    int anchorTileX = 0;
    int anchorTileY = 0;
    if (!tryGetEditableTileFromMouseCoords(mouse->getMouseCoords(), anchorTileX, anchorTileY)) {
        return;
    }

    bool hasRecordedGroup = false;
    const int height = static_cast<int>(m_clipboardTiles.size());
    const int width = static_cast<int>(m_clipboardTiles.front().size());
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            const int destTileX = anchorTileX + x;
            const int destTileY = anchorTileY + y;
            if (!isEditableTile(destTileX, destTileY)) {
                continue;
            }

            const int newTileID = m_clipboardTiles[y][x];
            const int oldTileID = (*m_mapData)[destTileY][destTileX];
            if (oldTileID == newTileID) {
                continue;
            }

            if (!hasRecordedGroup) {
                m_undoRedo->beginRecordGroup();
                hasRecordedGroup = true;
            }

            m_undoRedo->recordTileChange(destTileX, destTileY, oldTileID, newTileID);
            (*m_mapData)[destTileY][destTileX] = newTileID;
        }
    }

    if (hasRecordedGroup) {
        m_hasChanged = true;
    }
}

int cEditorState::getNormalizedCursorSize() const
{
    int cursorSize = std::max(1, getActiveCursorSize());
    if (cursorSize % 2 == 0) {
        cursorSize += 1;
    }

    return cursorSize;
}

void cEditorState::getBrushTileBounds(int centerTileX, int centerTileY, int &brushStartTileX, int &brushStartTileY, int &brushEndTileX, int &brushEndTileY) const
{
    const int cursorRadius = getNormalizedCursorSize() / 2;

    brushStartTileX = std::max(1, centerTileX - cursorRadius);
    brushStartTileY = std::max(1, centerTileY - cursorRadius);
    brushEndTileX = std::min(static_cast<int>(m_mapData->getCols()) - 2, centerTileX + cursorRadius);
    brushEndTileY = std::min(static_cast<int>(m_mapData->getRows()) - 2, centerTileY + cursorRadius);
}

void cEditorState::drawGrid() const
{
    if (m_mapData == nullptr) {
        return;
    }

    const int cameraX = m_editorCam->getCameraX();
    const int cameraY = m_editorCam->getCameraY();
    const int tileLenSize = m_editorCam->getTileSize();
    const int startX = m_editorCam->getStartX();
    const int startY = m_editorCam->getStartY();
    const size_t endX = m_editorCam->getEndX();
    const size_t endY = m_editorCam->getEndY();

    const int viewportTop = heightBarSize;
    const int viewportBottom = heightBarSize + mapSizeArea.getHeight() - 1;
    const int viewportLeft = 0;
    const int viewportRight = mapSizeArea.getWidth() - 1;

    const int mapLeftOnScreen = -cameraX;
    const int mapRightOnScreen = static_cast<int>(m_mapData->getCols() * tileLenSize) - cameraX;
    const int mapTopOnScreen = heightBarSize - cameraY;
    const int mapBottomOnScreen = heightBarSize + static_cast<int>(m_mapData->getRows() * tileLenSize) - cameraY;

    const int gridLeft = std::max(viewportLeft, mapLeftOnScreen);
    const int gridRight = std::min(viewportRight, mapRightOnScreen);
    const int gridTop = std::max(viewportTop, mapTopOnScreen);
    const int gridBottom = std::min(viewportBottom, mapBottomOnScreen);

    if (gridLeft > gridRight || gridTop > gridBottom) {
        return;
    }

    for (int i = startX; i <= static_cast<int>(endX); i++) {
        int lineX = (i * tileLenSize) - cameraX;
        if (lineX < gridLeft || lineX > gridRight) {
            continue;
        }
        m_sdlDrawer->renderLine(lineX, gridTop, lineX, gridBottom, editorGridColor);
    }

    for (int j = startY; j <= static_cast<int>(endY); j++) {
        int lineY = heightBarSize + (j * tileLenSize) - cameraY;
        if (lineY < gridTop || lineY > gridBottom) {
            continue;
        }
        m_sdlDrawer->renderLine(gridLeft, lineY, gridRight, lineY, editorGridColor);
    }
}

void cEditorState::drawAxes() const
{
    if (m_mapData == nullptr) {
        return;
    }

    const int cameraX = m_editorCam->getCameraX();
    const int cameraY = m_editorCam->getCameraY();
    const int tileLenSize = m_editorCam->getTileSize();

    const int viewportTop = heightBarSize;
    const int viewportBottom = heightBarSize + mapSizeArea.getHeight() - 1;
    const int viewportLeft = 0;
    
    const int mapLeftOnScreen = -cameraX;
    const int mapRightOnScreen = static_cast<int>(m_mapData->getCols() * tileLenSize) - cameraX;
    const int mapTopOnScreen = heightBarSize - cameraY;
    const int mapBottomOnScreen = heightBarSize + static_cast<int>(m_mapData->getRows() * tileLenSize) - cameraY;

    const int viewportRight = mapSizeArea.getWidth() - 1;
    const int gridLeft = std::max(viewportLeft, mapLeftOnScreen);
    const int gridRight = std::min(viewportRight, mapRightOnScreen);
    const int gridTop = std::max(viewportTop, mapTopOnScreen);
    const int gridBottom = std::min(viewportBottom, mapBottomOnScreen);

    if (gridLeft > gridRight || gridTop > gridBottom) {
        return;
    }

    const int middleX = (static_cast<int>(m_mapData->getCols()) * tileLenSize) / 2 - cameraX;
    if (middleX >= gridLeft && middleX <= gridRight) {
        m_sdlDrawer->renderLine(middleX, gridTop, middleX, gridBottom, editorCenterLineColor);
    }

    const int middleY = heightBarSize + (static_cast<int>(m_mapData->getRows()) * tileLenSize) / 2 - cameraY;
    if (middleY >= gridTop && middleY <= gridBottom) {
        m_sdlDrawer->renderLine(gridLeft, middleY, gridRight, middleY, editorCenterLineColor);
    }
}

void cEditorState::modifyTile(int posX, int posY, int tileID)
{
    if (tileID == -1) {
        return;
    }

    const int tileX = m_editorCam->screenToTileX(posX);
    const int tileY = m_editorCam->screenToTileY(posY);
    if (m_mapData == nullptr || tileX < 1 || tileY < 1 || tileX >= static_cast<int>(m_mapData->getCols()) - 1 || tileY >= static_cast<int>(m_mapData->getRows()) - 1) {
        return;
    }

    int brushStartTileX = 0;
    int brushStartTileY = 0;
    int brushEndTileX = 0;
    int brushEndTileY = 0;
    getBrushTileBounds(tileX, tileY, brushStartTileX, brushStartTileY, brushEndTileX, brushEndTileY);

    bool hasRecordedGroup = false;
    for (int brushTileY = brushStartTileY; brushTileY <= brushEndTileY; brushTileY++) {
        for (int brushTileX = brushStartTileX; brushTileX <= brushEndTileX; brushTileX++) {
            int oldTileID = (*m_mapData)[brushTileY][brushTileX];
            if (oldTileID == tileID) {
                continue;
            }

            if (!hasRecordedGroup) {
                m_undoRedo->beginRecordGroup();
                hasRecordedGroup = true;
            }

            m_undoRedo->recordTileChange(brushTileX, brushTileY, oldTileID, tileID);
            (*m_mapData)[brushTileY][brushTileX] = tileID;
            m_hasChanged = true;
        }
    }
}

void cEditorState::modifyStartCell(int posX, int posY, int startCellID)
{
    if (startCellID == -1) {
        return;
    }
    const int tileX = m_editorCam->screenToTileX(posX);
    const int tileY = m_editorCam->screenToTileY(posY);
    if (m_mapData && tileX >= 1 && tileY >= 1 && tileX < static_cast<int>(m_mapData->getCols())-1 && tileY < static_cast<int>(m_mapData->getRows())-1) {
        cPoint oldPos = startCells[startCellID];
        cPoint newPos = {tileX, tileY};
        if (oldPos.x == newPos.x && oldPos.y == newPos.y) return;
        m_undoRedo->beginRecordGroup();
        m_undoRedo->recordStartCellChange(startCellID, oldPos, newPos);
        startCells[startCellID] = newPos;
        m_hasChanged = true;
    }
}

void cEditorState::modifySymmetricArea(Direction dir)
{
    //std::cout << "modifySymmetricArea " << static_cast<int>(dir) << std::endl;
    switch (dir) {
        case Direction::bottom:
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < (m_mapData->getRows())/2; j++) {
                for (size_t i = 1; i < m_mapData->getCols(); i++) {
                    size_t mirrorJ = (m_mapData->getRows()-1)-j;
                    int oldVal = (*m_mapData)[mirrorJ][i];
                    int newVal = (*m_mapData)[j][i];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(i, mirrorJ, oldVal, newVal);
                        (*m_mapData)[mirrorJ][i] = newVal;
                    }
                }
            }
            break;
        case Direction::top:
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < (m_mapData->getRows())/2; j++) {
                for (size_t i = 1; i < m_mapData->getCols(); i++) {
                    size_t mirrorJ = (m_mapData->getRows()-1)-j;
                    int oldVal = (*m_mapData)[j][i];
                    int newVal = (*m_mapData)[mirrorJ][i];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(i, j, oldVal, newVal);
                        (*m_mapData)[j][i] = newVal;
                    }
                }
            }
            break;
        case Direction::right:
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < m_mapData->getRows(); j++) {
                for (size_t i = 1; i < (m_mapData->getCols())/2; i++) {
                    size_t mirrorI = (m_mapData->getCols()-1)-i;
                    int oldVal = (*m_mapData)[j][mirrorI];
                    int newVal = (*m_mapData)[j][i];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(mirrorI, j, oldVal, newVal);
                        (*m_mapData)[j][mirrorI] = newVal;
                    }
                }
            }
            break;
        case Direction::left:
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < m_mapData->getRows(); j++) {
                for (size_t i = 1; i < (m_mapData->getCols())/2; i++) {
                    size_t mirrorI = (m_mapData->getCols()-1)-i;
                    int oldVal = (*m_mapData)[j][i];
                    int newVal = (*m_mapData)[j][mirrorI];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(i, j, oldVal, newVal);
                        (*m_mapData)[j][i] = newVal;
                    }
                }
            }
            break;
        case Direction::topLeft:
            if (m_mapData->getCols() != m_mapData->getRows()) {
                const s_GameEvent newEvent {
                    .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
                    .data = NotificationEvent {
                        .message = editorText(EditorText::SquareRequired),
                        .type = eNotificationType::PRIORITY,
                    }
                };                
                m_eventEmitter->emit(newEvent);
                break;
            }
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < m_mapData->getRows()-1; j++) {
                for (size_t i = 1; i < m_mapData->getCols()-1; i++) {
                    if ((i + j) >= (m_mapData->getCols()-1)) {
                        continue;
                    }

                    size_t mirrorJ = (m_mapData->getRows()-1)-i;
                    size_t mirrorI = (m_mapData->getCols()-1)-j;
                    int oldVal = (*m_mapData)[j][i];
                    int newVal = (*m_mapData)[mirrorJ][mirrorI];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(i, j, oldVal, newVal);
                        (*m_mapData)[j][i] = newVal;
                    }
                }
            }
            break;

        case Direction::topRight:
            if (m_mapData->getCols() != m_mapData->getRows()) {
                const s_GameEvent newEvent {
                    .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
                    .data = NotificationEvent {
                        .message = editorText(EditorText::SquareRequired),
                        .type = eNotificationType::PRIORITY,
                    }
                };                
                m_eventEmitter->emit(newEvent);
                break;
            }
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < m_mapData->getRows()-1; j++) {
                for (size_t i = 1; i < m_mapData->getCols()-1; i++) {
                    if (i <= j) {
                        continue;
                    }

                    int oldVal = (*m_mapData)[j][i];
                    int newVal = (*m_mapData)[i][j];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(i, j, oldVal, newVal);
                        (*m_mapData)[j][i] = newVal;
                    }
                }
            }
            break;

        case Direction::bottomLeft:
            if (m_mapData->getCols() != m_mapData->getRows()) {
                const s_GameEvent newEvent {
                    .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
                    .data = NotificationEvent {
                        .message = editorText(EditorText::SquareRequired),
                        .type = eNotificationType::PRIORITY,
                    }
                };                
                m_eventEmitter->emit(newEvent);
                break;
            }
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < m_mapData->getRows()-1; j++) {
                for (size_t i = 1; i < m_mapData->getCols()-1; i++) {
                    if (j <= i) {
                        continue;
                    }

                    int oldVal = (*m_mapData)[j][i];
                    int newVal = (*m_mapData)[i][j];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(i, j, oldVal, newVal);
                        (*m_mapData)[j][i] = newVal;
                    }
                }
            }
            break;

        case Direction::bottomRight:
            if (m_mapData->getCols() != m_mapData->getRows()) {
                const s_GameEvent newEvent {
                    .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
                    .data = NotificationEvent {
                        .message = editorText(EditorText::SquareRequired),
                        .type = eNotificationType::PRIORITY,
                    }
                };                
                m_eventEmitter->emit(newEvent);
                break;
            }
            m_undoRedo->beginRecordGroup();
            for (size_t j = 1; j < m_mapData->getRows()-1; j++) {
                for (size_t i = 1; i < m_mapData->getCols()-1; i++) {
                    if ((i + j) <= (m_mapData->getCols()-1)) {
                        continue;
                    }

                    size_t mirrorJ = (m_mapData->getRows()-1)-i;
                    size_t mirrorI = (m_mapData->getCols()-1)-j;
                    int oldVal = (*m_mapData)[j][i];
                    int newVal = (*m_mapData)[mirrorJ][mirrorI];
                    if (oldVal != newVal) {
                        m_undoRedo->recordTileChange(i, j, oldVal, newVal);
                        (*m_mapData)[j][i] = newVal;
                    }
                }
            }
            break;
    }
    m_hasChanged = true;
}

void cEditorState::drawStartCells() const
{
    const int cameraX = m_editorCam->getCameraX();
    const int cameraY = m_editorCam->getCameraY();
    const int tileLenSize = m_editorCam->getTileSize();
    const GuiTheme theme = GuiTheme::Remaster();
    int x,y;
    for(size_t i=0; i<startCells.size(); i++) {
        if (startCells[i].x != -1 && startCells[i].y != -1) {
            x = startCells[i].x * tileLenSize - cameraX;
            y = heightBarSize + startCells[i].y * tileLenSize - cameraY;
            // Display if onscreen
            if (x + tileLenSize > 0 && x < m_settings->getScreenW() &&y + tileLenSize > heightBarSize && y < m_settings->getScreenH()) {
                const EditorIcon digit = static_cast<EditorIcon>(static_cast<int>(EditorIcon::Start1) + static_cast<int>(i));
                Texture *disc = m_icons.get(*m_sdlDrawer, EditorIcon::StartDisc, tileLenSize);
                Texture *ring = m_icons.get(*m_sdlDrawer, digit, tileLenSize);
                if (disc != nullptr && ring != nullptr) {
                    SDL_SetTextureColorMod(disc->tex.get(), editorPanelColor.r, editorPanelColor.g, editorPanelColor.b);
                    m_sdlDrawer->renderTexture(disc->tex.get(), x, y, tileLenSize, tileLenSize, 220);
                    SDL_SetTextureColorMod(ring->tex.get(), theme.textColorHover.r, theme.textColorHover.g, theme.textColorHover.b);
                    m_sdlDrawer->renderTexture(ring->tex.get(), x, y, tileLenSize, tileLenSize);
                }
            }
        }
    }
}

bool cEditorState::saveMap(bool backup) const
{
    s_PreviewMap map;
    map.width = static_cast<int>(m_mapData->getCols());
    map.height = static_cast<int>(m_mapData->getRows());
    map.name = m_mapName;
    map.author = m_mapAuthor;
    map.description = m_mapDescription;
    map.iStartCell.fill(-1);
    map.terrainType.reserve(static_cast<size_t>(map.width * map.height));
    for (int y = 0; y < map.height; y++) {
        for (int x = 0; x < map.width; x++) {
            map.terrainType.push_back((*m_mapData)[y][x]);
        }
    }
    for (size_t i = 0; i < startCells.size(); i++) {
        if (startCells[i].x != -1 && startCells[i].y != -1) {
            map.iStartCell[i] = startCells[i].y * map.width + startCells[i].x;
        }
    }
    if (!m_previewMaps->saveSkirmishMap(map, backup)) {
        const s_GameEvent errorEvent {
            .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
            .data = NotificationEvent {
                .message = editorText(EditorText::SaveFailed),
                .type = eNotificationType::PRIORITY,
            }
        };
        m_eventEmitter->emit(errorEvent);
        return false;
    }

    const s_GameEvent newEvent {
        .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
        .data = NotificationEvent {
            .message = editorText(EditorText::SaveDone),
            .type = eNotificationType::NEUTRAL,
        }
    };                
    m_eventEmitter->emit(newEvent);
    return true;
}
