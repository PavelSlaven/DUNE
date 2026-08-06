#include "cCommandBarDrawer.h"

#include "drawers/CommandBarLayout.hpp"
#include "drawers/CommandBarPolicy.hpp"
#include "context/GameContext.hpp"
#include "context/TextContext.hpp"
#include "controls/cGameControlsContext.h"
#include "d2tmc.h"
#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"
#include "gameobjects/structures/cAbstractStructure.h"
#include "gameobjects/units/cUnit.h"
#include "player/cPlayer.h"
#include "sidebar/cSideBar.h"
#include "utils/Localization.hpp"
#include "utils/HdUiTextureLoader.hpp"

#include <algorithm>

namespace {
Color panelColor() { return Color{13, 17, 19, 242}; }
Color panelBorder() { return Color{105, 80, 39, 255}; }
Color brass() { return Color{188, 139, 47, 255}; }
Color disabledText() { return Color{105, 105, 100, 255}; }
Color blueFilter() { return Color{5, 24, 48, 38}; }
}

cCommandBarDrawer::cCommandBarDrawer(GameContext *ctx, cPlayer *player) :
    m_ctx(ctx),
    m_player(player),
    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
    m_keyTextDrawer(ctx->getTextContext()->getCommandKeyTextDrawer()),
    m_commandBarTexture(nullptr),
    m_disabledCommandBarTexture(nullptr),
    m_panelRect(),
    m_buttons(),
    m_hoveredButton(-1)
{
    if (game.isHdGraphicsActive()) {
        m_commandBarTexture = loadHdUiTexture(
            "command_bar.png",
            game.getGraphicsDensity(),
            "HD command bar"
        );
        m_disabledCommandBarTexture = loadHdUiTexture(
            "command_bar_disabled.png",
            game.getGraphicsDensity(),
            "disabled HD command bar"
        );
    }
    rebuildLayout();
}

cCommandBarDrawer::~cCommandBarDrawer()
{
    delete m_commandBarTexture;
    delete m_disabledCommandBarTexture;
}

void cCommandBarDrawer::setPlayer(cPlayer *player)
{
    m_player = player;
}

int cCommandBarDrawer::getTopY() const
{
    return m_panelRect.getY();
}

bool cCommandBarDrawer::isMouseOver(const cPoint &point) const
{
    return game.isHdGraphicsActive() && m_panelRect.isPointWithin(point.x, point.y);
}

void cCommandBarDrawer::rebuildLayout()
{
    const CommandBarLayout layout = CommandBarLayout::create(game.m_screenW, game.m_screenH, cSideBar::SidebarWidth);
    m_panelRect = layout.panel;
    m_buttons.clear();

    if (!game.isHdGraphicsActive() || layout.panel.getWidth() <= 0) return;

    const auto selectedUnits = m_player->getSelectedUnits();
    cAbstractStructure *selectedStructure = m_player->getSelectedStructure();
    const bool ownsSelectedStructure = selectedStructure && selectedStructure->belongsTo(m_player);
    const std::array<Button, CommandBarLayout::ActionCount> actions{{
        {Command::Move, layout.actions[0], localization::text("Move", "Переместить"), localization::text("LMB", "ЛКМ"), isMoveCommandEnabled(!selectedUnits.empty()), false},
        {Command::Attack, layout.actions[1], localization::text("Attack", "Атаковать"), commandBindingDisplayName(game.m_commandBindings.attack, localization::isEnglish()), isAttackCommandEnabled(hasAttackCapableUnit()), false},
        {Command::Repair, layout.actions[2], localization::text("Repair", "Ремонт"), commandBindingDisplayName(game.m_commandBindings.repair, localization::isEnglish()), isRepairCommandEnabled(), false},
        {Command::Unload, layout.actions[3], localization::text("Unload", "Разгрузить"), commandBindingDisplayName(game.m_commandBindings.unload, localization::isEnglish()), isUnloadCommandEnabled(hasUnloadableHarvester()), false},
        {Command::Deploy, layout.actions[4], localization::text("Deploy", "Развернуть"), commandBindingDisplayName(game.m_commandBindings.deploy, localization::isEnglish()), isDeployCommandEnabled(hasSelectedMcv()), false},
        {Command::Rally, layout.actions[5], localization::text("Rally", "Точка сбора"), commandBindingDisplayName(game.m_commandBindings.rally, localization::isEnglish()), isRallyCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->canSpawnUnits()), false},
        {Command::Release, layout.actions[6], localization::text("Release", "Выпустить"), commandBindingDisplayName(game.m_commandBindings.release, localization::isEnglish()), isReleaseCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->getType() == REPAIR), false}
    }};
    m_buttons.assign(actions.begin(), actions.end());
}

void cCommandBarDrawer::draw()
{
    if (!game.isHdGraphicsActive()) return;
    rebuildLayout();

    if (m_disabledCommandBarTexture) {
        renderDrawer->renderStrechFullSprite(m_disabledCommandBarTexture, m_panelRect);
    }
    else if (m_commandBarTexture) {
        renderDrawer->renderStrechFullSprite(m_commandBarTexture, m_panelRect);
    }
    else {
        renderDrawer->renderRectFillColor(m_panelRect, panelColor());
        renderDrawer->renderLine(m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getEndX(), m_panelRect.getY(), brass());
        renderDrawer->renderRectColor(m_panelRect, panelBorder());
    }

    for (const Button &button : m_buttons) {
        drawButton(button);
    }

    // A restrained cool overlay keeps the bright supplied artwork readable
    // against the battlefield without baking another set of source images.
    renderDrawer->renderRectFillColor(m_panelRect, blueFilter());
}

void cCommandBarDrawer::drawButton(const Button &button) const
{
    const int index = static_cast<int>(&button - m_buttons.data());

    if (m_commandBarTexture) {
        if (button.enabled && m_disabledCommandBarTexture) {
            const int sourceWidth = m_commandBarTexture->w / CommandBarLayout::ActionCount;
            const cRectangle sourceRect(
                index * sourceWidth,
                0,
                index == CommandBarLayout::ActionCount - 1
                    ? m_commandBarTexture->w - index * sourceWidth
                    : sourceWidth,
                m_commandBarTexture->h
            );
            renderDrawer->renderStrechSprite(m_commandBarTexture, sourceRect, button.rect);
        }
        else if (!button.enabled && !m_disabledCommandBarTexture) {
            renderDrawer->renderRectFillColor(button.rect, Color{2, 3, 3, 118});
        }
    }
    else {
        renderDrawer->renderRectFillColor(
            button.rect,
            button.active ? Color{69, 54, 27, 255} : Color{25, 30, 32, 255}
        );
        renderDrawer->renderRectColor(
            button.rect,
            button.enabled ? panelBorder() : Color{57, 59, 58, 255}
        );
    }

    if (!m_commandBarTexture) {
        const cRectangle iconRect(
            button.rect.getX() + 4,
            button.rect.getY() + 5,
            button.rect.getWidth() - 8,
            button.rect.getHeight() * 52 / 100
        );
        drawIcon(button.command, iconRect, button.enabled ? Color{210, 170, 82, 255} : disabledText());
    }

    if (button.enabled && !button.hotkey.empty()) {
        const int keyWidth = std::max(9, button.rect.getWidth() * 30 / 100);
        const int keyHeight = std::max(9, button.rect.getHeight() * 30 / 100);
        const bool circleAtBottomLeft = index % 2 == 0;
        const cRectangle keyRect(
            button.rect.getX() + button.rect.getWidth() * (circleAtBottomLeft ? 6 : 65) / 100,
            button.rect.getY() + button.rect.getHeight() * (circleAtBottomLeft ? 67 : 4) / 100,
            keyWidth,
            keyHeight
        );
        const float widthScale = static_cast<float>(keyRect.getWidth() - 4) /
            std::max(1, m_keyTextDrawer->getTextLength(button.hotkey));
        const float heightScale = static_cast<float>(keyRect.getHeight() - 4) /
            std::max(1, m_keyTextDrawer->getFontHeight());
        const float maximumKeyScale = button.hotkey.size() == 1 ? 1.45F : 1.15F;
        const float keyScale = std::clamp(
            std::min(widthScale, heightScale),
            0.50F,
            maximumKeyScale
        );
        m_keyTextDrawer->drawTextScaledCenteredInBox(
            button.hotkey,
            keyRect,
            keyScale,
            Color{83, 50, 19, 255},
            false
        );
    }
}

void cCommandBarDrawer::drawIcon(Command command, const cRectangle &rect, Color color) const
{
    const int cx = rect.getX() + rect.getWidth() / 2;
    const int cy = rect.getY() + rect.getHeight() / 2;
    const int left = cx - 8;
    const int right = cx + 8;
    const int top = cy - 7;
    const int bottom = cy + 7;

    switch (command) {
        case Command::Move:
            renderDrawer->renderLine(left, cy, right, cy, color);
            renderDrawer->renderLine(right, cy, right - 5, cy - 5, color);
            renderDrawer->renderLine(right, cy, right - 5, cy + 5, color);
            renderDrawer->renderLine(cx, top, cx, bottom, color);
            break;
        case Command::Attack:
            renderDrawer->renderRectColor(cx - 6, cy - 6, 12, 12, color);
            renderDrawer->renderLine(left, cy, cx - 3, cy, color);
            renderDrawer->renderLine(cx + 3, cy, right, cy, color);
            renderDrawer->renderLine(cx, top, cx, cy - 3, color);
            renderDrawer->renderLine(cx, cy + 3, cx, bottom, color);
            break;
        case Command::Repair:
            renderDrawer->renderRectFillColor(cx - 2, top, 4, 14, color);
            renderDrawer->renderRectFillColor(left + 1, cy - 2, 14, 4, color);
            break;
        case Command::Unload:
            renderDrawer->renderLine(cx, top, cx, bottom - 2, color);
            renderDrawer->renderLine(cx, bottom - 2, cx - 5, bottom - 7, color);
            renderDrawer->renderLine(cx, bottom - 2, cx + 5, bottom - 7, color);
            renderDrawer->renderDot(left + 2, top + 2, color, 2);
            renderDrawer->renderDot(right - 2, top + 2, color, 2);
            break;
        case Command::Deploy:
            renderDrawer->renderLine(left, top, cx, bottom, color);
            renderDrawer->renderLine(right, top, cx, bottom, color);
            renderDrawer->renderLine(left + 5, top, cx, bottom - 5, color);
            renderDrawer->renderLine(right - 5, top, cx, bottom - 5, color);
            break;
        case Command::Rally:
            renderDrawer->renderLine(left + 3, top, left + 3, bottom, color);
            renderDrawer->renderLine(left + 3, top, right, top + 4, color);
            renderDrawer->renderLine(right, top + 4, left + 3, cy + 1, color);
            break;
        case Command::Release:
            renderDrawer->renderRectColor(left, top, 16, 14, color);
            renderDrawer->renderLine(cx, top + 3, cx, bottom + 1, color);
            renderDrawer->renderLine(cx, bottom + 1, cx - 4, bottom - 3, color);
            renderDrawer->renderLine(cx, bottom + 1, cx + 4, bottom - 3, color);
            break;
    }
}

void cCommandBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (!game.isHdGraphicsActive()) return;
    rebuildLayout();

    if (event.eventType == MOUSE_MOVED_TO) {
        m_hoveredButton = -1;
        for (int i = 0; i < static_cast<int>(m_buttons.size()); ++i) {
            if (m_buttons[i].rect.isPointWithin(event.coords.x, event.coords.y)) {
                m_hoveredButton = i;
                break;
            }
        }
    }
    else if (event.eventType == MOUSE_LEFT_BUTTON_CLICKED) {
        for (const Button &button : m_buttons) {
            if (button.enabled && button.rect.isPointWithin(event.coords.x, event.coords.y)) {
                execute(button.command);
                break;
            }
        }
    }
}

void cCommandBarDrawer::execute(Command command)
{
    cGameControlsContext *context = m_player->getGameControlsContext();
    switch (command) {
        case Command::Move:
            context->activateMoveCommand();
            break;
        case Command::Attack:
            context->activateAttackCommand();
            break;
        case Command::Repair:
            context->setMouseState(MOUSESTATE_REPAIR);
            break;
        case Command::Unload:
            executeUnload();
            break;
        case Command::Deploy:
            executeDeploy();
            break;
        case Command::Rally:
            context->activateRallyPointCommand();
            break;
        case Command::Release:
            executeRelease();
            break;
        default:
            break;
    }
}

void cCommandBarDrawer::executeUnload()
{
    for (int id : m_player->getSelectedUnits()) {
        cUnit &selected = unit[id];
        if (selected.isHarvester() && selected.canUnload()) {
            selected.findBestStructureCandidateAndHeadTowardsItOrWait(REFINERY, true, INTENT_UNLOAD_SPICE);
        }
    }
}

void cCommandBarDrawer::executeDeploy()
{
    const auto selectedUnits = m_player->getSelectedUnits();
    for (int id : selectedUnits) {
        cUnit &selected = unit[id];
        if (!selected.isValid() || selected.getType() != MCV || !selected.belongsTo(m_player)) continue;
        if (!m_player->canPlaceStructureAt(selected.getCell(), CONSTYARD, selected.iID).success) continue;
        const int cell = selected.getCell();
        selected.die(false, false);
        m_player->placeStructure(cell, CONSTYARD, 100);
        break;
    }
}

void cCommandBarDrawer::executeRelease()
{
    cAbstractStructure *selected = m_player->getSelectedStructure();
    if (!selected || selected->getType() != REPAIR) return;
    s_GameEvent event{
        .eventType = eGameEventType::GAME_EVENT_DEPLOY_UNIT,
        .entityType = eBuildType::UNKNOWN,
        .entityID = -1,
        .player = m_player
    };
    selected->onNotifyGameEvent(event);
}

bool cCommandBarDrawer::hasAttackCapableUnit() const
{
    return std::ranges::any_of(m_player->getSelectedUnits(), [](int id) {
        const cUnit &selected = unit[id];
        const s_UnitInfo &info = selected.getUnitInfo();
        return !selected.isHarvester() && (info.canAttackUnits || info.canAttackAirUnits || info.canEnterAndDamageStructure);
    });
}

bool cCommandBarDrawer::hasUnloadableHarvester() const
{
    return std::ranges::any_of(m_player->getSelectedUnits(), [](int id) {
        return unit[id].isHarvester() && unit[id].canUnload();
    });
}

bool cCommandBarDrawer::hasSelectedMcv() const
{
    return std::ranges::any_of(m_player->getSelectedUnits(), [](int id) {
        return unit[id].isValid() && unit[id].getType() == MCV;
    });
}
