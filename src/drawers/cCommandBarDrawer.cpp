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
Color textColor() { return Color{235, 226, 196, 255}; }
Color disabledText() { return Color{105, 105, 100, 255}; }
}

cCommandBarDrawer::cCommandBarDrawer(GameContext *ctx, cPlayer *player) :
    m_ctx(ctx),
    m_player(player),
    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
    m_commandBarTexture(nullptr),
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
    }
    rebuildLayout();
}

cCommandBarDrawer::~cCommandBarDrawer()
{
    delete m_commandBarTexture;
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
        {Command::Move, layout.actions[0], localization::text("Move", "Идти"), localization::text("LMB", "ЛКМ"), isMoveCommandEnabled(!selectedUnits.empty()), false},
        {Command::Attack, layout.actions[1], localization::text("Attack", "Атака"), commandBindingDisplayName(game.m_commandBindings.attack, localization::isEnglish()), isAttackCommandEnabled(hasAttackCapableUnit()), false},
        {Command::Repair, layout.actions[2], localization::text("Repair", "Ремонт"), commandBindingDisplayName(game.m_commandBindings.repair, localization::isEnglish()), isRepairCommandEnabled(), false},
        {Command::Unload, layout.actions[3], localization::text("Unload", "Разгрузка"), commandBindingDisplayName(game.m_commandBindings.unload, localization::isEnglish()), isUnloadCommandEnabled(hasUnloadableHarvester()), false},
        {Command::Deploy, layout.actions[4], localization::text("Deploy", "Развернуть"), commandBindingDisplayName(game.m_commandBindings.deploy, localization::isEnglish()), isDeployCommandEnabled(hasSelectedMcv()), false},
        {Command::Rally, layout.actions[5], localization::text("Rally", "Сбор"), commandBindingDisplayName(game.m_commandBindings.rally, localization::isEnglish()), isRallyCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->canSpawnUnits()), false},
        {Command::Release, layout.actions[6], localization::text("Release", "Выпустить"), commandBindingDisplayName(game.m_commandBindings.release, localization::isEnglish()), isReleaseCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->getType() == REPAIR), false}
    }};
    m_buttons.assign(actions.begin(), actions.end());
}

void cCommandBarDrawer::draw()
{
    if (!game.isHdGraphicsActive()) return;
    rebuildLayout();

    if (m_commandBarTexture) {
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
}

void cCommandBarDrawer::drawButton(const Button &button) const
{
    const int index = static_cast<int>(&button - m_buttons.data());
    const bool hovered = index == m_hoveredButton;
    const Color background = button.active ? Color{69, 54, 27, 255} :
                             hovered && button.enabled ? Color{39, 43, 42, 255} : Color{25, 30, 32, 255};
    const Color border = button.enabled ? (hovered || button.active ? brass() : panelBorder()) : Color{57, 59, 58, 255};
    const Color foreground = button.enabled ? textColor() : disabledText();

    if (m_commandBarTexture) {
        if (!button.enabled) {
            renderDrawer->renderRectFillColor(button.rect, Color{2, 3, 3, 118});
        }
        else if (hovered || button.active) {
            renderDrawer->renderRectFillColor(
                button.rect,
                Color{188, 139, 47, static_cast<Uint8>(button.active ? 72 : 35)}
            );
            renderDrawer->renderRectColor(button.rect, border);
        }
    }
    else {
        renderDrawer->renderRectFillColor(button.rect, background);
        renderDrawer->renderRectColor(button.rect, border);
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

    const cRectangle labelRect(
        button.rect.getX() + 4,
        button.rect.getY() + button.rect.getHeight() * 73 / 100,
        button.rect.getWidth() - 8,
        std::max(1, button.rect.getHeight() * 20 / 100)
    );
    const float widthScale = static_cast<float>(labelRect.getWidth()) /
        std::max(1, m_smallTextDrawer->getTextLength(button.label));
    float scale = std::clamp(widthScale, 0.66F, 0.92F);
    m_smallTextDrawer->drawTextScaledCenteredInBox(button.label, labelRect, scale, foreground);

    if (!button.hotkey.empty()) {
        const int badgePercent = button.hotkey.size() > 1 ? 42 : 24;
        const int badgeWidth = std::max(18, button.rect.getWidth() * badgePercent / 100);
        const int badgeHeight = std::max(11, button.rect.getHeight() * 18 / 100);
        const int badgeMargin = std::max(2, button.rect.getWidth() * 3 / 100);
        const cRectangle badge(
            button.rect.getEndX() - badgeWidth - badgeMargin,
            button.rect.getY() + std::max(2, button.rect.getHeight() * 8 / 100),
            badgeWidth,
            badgeHeight
        );
        renderDrawer->renderRectFillColor(badge, Color{7, 8, 8, 252});
        renderDrawer->renderRectColor(badge, Color{125, 89, 35, 255});
        const float keyScale = std::clamp(
            static_cast<float>(badge.getWidth() - 4) /
                std::max(1, m_smallTextDrawer->getTextLength(button.hotkey)),
            0.52F,
            0.72F
        );
        m_smallTextDrawer->drawTextScaledCenteredInBox(button.hotkey, badge, keyScale, foreground, false);
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
