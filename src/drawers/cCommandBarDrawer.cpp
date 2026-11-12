#include "cCommandBarDrawer.h"

#include "context/GameContext.hpp"
#include "context/TextContext.hpp"
#include "context/cGameObjectContext.h"
#include "controls/cGameControlsContext.h"
#include "controls/cKeyBindings.h"
#include "controls/cKeyboard.h"
#include "debug/UiAudit.hpp"
#include "drawers/CommandBarLayout.hpp"
#include "drawers/CommandBarPolicy.hpp"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "game/cEventEmitter.h"
#include "game/cGameSettings.h"
#include "gameobjects/players/cPlayer.h"
#include "gameobjects/structures/cAbstractStructure.h"
#include "gameobjects/structures/cStructureFactory.h"
#include "gameobjects/units/cUnit.h"
#include "include/Texture.hpp"
#include "include/cAssert.h"
#include "include/definitions.h"
#include "include/sGameEvent.h"
#include "include/sGameServices.h"
#include "sidebar/cSideBar.h"
#include "utils/HdUiTextureLoader.hpp"
#include "utils/Localization.hpp"

#include <algorithm>
#include <array>
#include <cctype>

namespace {
Color panelColor() { return Color{13, 17, 19, 242}; }
Color panelBorder() { return Color{105, 80, 39, 255}; }
Color brass() { return Color{188, 139, 47, 255}; }
Color disabledText() { return Color{105, 105, 100, 255}; }
Color blueFilter() { return Color{5, 24, 48, 38}; }
}

cCommandBarDrawer::cCommandBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services) :
    m_ctx(ctx),
    m_player(player),
    m_sdlDrawer(ctx->getSDLDrawer()),
    m_settings(services->settings),
    m_objects(services->objects),
    m_eventEmitter(services->eventEmitter),
    m_keyboard(services->keyboard),
    m_keyTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
    m_commandBarTexture(nullptr),
    m_disabledCommandBarTexture(nullptr),
    m_panelRect(),
    m_buttons(),
    m_hoveredButton(-1)
{
    d2tm_assert(m_player != nullptr);
    d2tm_assert(m_sdlDrawer != nullptr);
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_objects != nullptr);
    d2tm_assert(m_eventEmitter != nullptr);
    d2tm_assert(m_keyboard != nullptr);
    d2tm_assert(m_keyTextDrawer != nullptr);

    m_commandBarTexture = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "command_bar.png",
        "HD command bar"
    );
    m_disabledCommandBarTexture = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "command_bar_disabled.png",
        "disabled HD command bar"
    );
    m_panelRect = CommandBarLayout::create(m_settings->getScreenW(), m_settings->getScreenH(), cSideBar::SidebarWidth).panel;
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

bool cCommandBarDrawer::isMouseOver(const cPoint &point) const
{
    return m_panelRect.isPointWithin(point.x, point.y);
}

void cCommandBarDrawer::rebuildLayout()
{
    const CommandBarLayout layout = CommandBarLayout::create(m_settings->getScreenW(), m_settings->getScreenH(), cSideBar::SidebarWidth);
    m_panelRect = layout.panel;
    m_buttons.clear();

    if (layout.panel.getWidth() <= 0) return;

    const auto selectedUnits = m_player->getSelectedUnits();
    cAbstractStructure *selectedStructure = m_player->getSelectedStructure();
    const bool ownsSelectedStructure = selectedStructure && selectedStructure->belongsTo(m_player);
    const std::array<Button, CommandBarLayout::ActionCount> actions{{
        {Command::Move, layout.actions[0], localization::text("Move", "Переместить"), localization::text("LMB", "ЛКМ"), isMoveCommandEnabled(!selectedUnits.empty()), false},
        {Command::Attack, layout.actions[1], localization::text("Attack", "Атаковать"), getKeyLabel(eKeyAction::ATTACK_MODE), isAttackCommandEnabled(hasAttackCapableUnit()), false},
        {Command::Repair, layout.actions[2], localization::text("Repair", "Ремонт"), getKeyLabel(eKeyAction::REPAIR_UNIT), isRepairCommandEnabled(), false},
        {Command::Unload, layout.actions[3], localization::text("Unload", "Разгрузить"), getKeyLabel(eKeyAction::SEND_TO_REFINERY), isUnloadCommandEnabled(hasUnloadableHarvester()), false},
        {Command::Deploy, layout.actions[4], localization::text("Deploy", "Развернуть"), getKeyLabel(eKeyAction::DEPLOY_UNIT), isDeployCommandEnabled(hasSelectedMcv()), false},
        {Command::Rally, layout.actions[5], localization::text("Rally", "Точка сбора"), getKeyLabel(eKeyAction::ATTACK_MODE), isRallyCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->canHaveRallyPoint()), false},
        {Command::Release, layout.actions[6], localization::text("Release", "Выпустить"), getKeyLabel(eKeyAction::DEPLOY_UNIT), isReleaseCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->getType() == REPAIR), false}
    }};
    m_buttons.assign(actions.begin(), actions.end());
}

void cCommandBarDrawer::draw()
{
    rebuildLayout();
    if (uiaudit::isEnabled()) {
        uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight());
        UiAuditAccess::recordCommandBarClicks(*this);
    }

    if (m_disabledCommandBarTexture) {
        m_sdlDrawer->renderStrechFullSprite(m_disabledCommandBarTexture, m_panelRect);
    }
    else if (m_commandBarTexture) {
        m_sdlDrawer->renderStrechFullSprite(m_commandBarTexture, m_panelRect);
    }
    else {
        m_sdlDrawer->renderRectFillColor(m_panelRect, panelColor(), 242);
        m_sdlDrawer->renderLine(m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getEndX(), m_panelRect.getY(), brass());
        m_sdlDrawer->renderRectColor(m_panelRect, panelBorder());
    }

    for (const Button &button : m_buttons) {
        drawButton(button);
    }

    // A restrained cool overlay keeps the bright supplied artwork readable
    // against the battlefield without baking another set of source images.
    m_sdlDrawer->renderRectFillColor(m_panelRect, blueFilter(), 38);
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
            m_sdlDrawer->renderStrechSprite(m_commandBarTexture, sourceRect, button.rect);
        }
        else if (!button.enabled && !m_disabledCommandBarTexture) {
            m_sdlDrawer->renderRectFillColor(button.rect, Color{2, 3, 3, 118}, 118);
        }
    }
    else {
        m_sdlDrawer->renderRectFillColor(
            button.rect,
            button.active ? Color{69, 54, 27, 255} : Color{25, 30, 32, 255}
        );
        m_sdlDrawer->renderRectColor(
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
            m_sdlDrawer->renderLine(left, cy, right, cy, color);
            m_sdlDrawer->renderLine(right, cy, right - 5, cy - 5, color);
            m_sdlDrawer->renderLine(right, cy, right - 5, cy + 5, color);
            m_sdlDrawer->renderLine(cx, top, cx, bottom, color);
            break;
        case Command::Attack:
            m_sdlDrawer->renderRectColor(cx - 6, cy - 6, 12, 12, color);
            m_sdlDrawer->renderLine(left, cy, cx - 3, cy, color);
            m_sdlDrawer->renderLine(cx + 3, cy, right, cy, color);
            m_sdlDrawer->renderLine(cx, top, cx, cy - 3, color);
            m_sdlDrawer->renderLine(cx, cy + 3, cx, bottom, color);
            break;
        case Command::Repair:
            m_sdlDrawer->renderRectFillColor(cx - 2, top, 4, 14, color);
            m_sdlDrawer->renderRectFillColor(left + 1, cy - 2, 14, 4, color);
            break;
        case Command::Unload:
            m_sdlDrawer->renderLine(cx, top, cx, bottom - 2, color);
            m_sdlDrawer->renderLine(cx, bottom - 2, cx - 5, bottom - 7, color);
            m_sdlDrawer->renderLine(cx, bottom - 2, cx + 5, bottom - 7, color);
            m_sdlDrawer->renderDot(left + 2, top + 2, color, 2);
            m_sdlDrawer->renderDot(right - 2, top + 2, color, 2);
            break;
        case Command::Deploy:
            m_sdlDrawer->renderLine(left, top, cx, bottom, color);
            m_sdlDrawer->renderLine(right, top, cx, bottom, color);
            m_sdlDrawer->renderLine(left + 5, top, cx, bottom - 5, color);
            m_sdlDrawer->renderLine(right - 5, top, cx, bottom - 5, color);
            break;
        case Command::Rally:
            m_sdlDrawer->renderLine(left + 3, top, left + 3, bottom, color);
            m_sdlDrawer->renderLine(left + 3, top, right, top + 4, color);
            m_sdlDrawer->renderLine(right, top + 4, left + 3, cy + 1, color);
            break;
        case Command::Release:
            m_sdlDrawer->renderRectColor(left, top, 16, 14, color);
            m_sdlDrawer->renderLine(cx, top + 3, cx, bottom + 1, color);
            m_sdlDrawer->renderLine(cx, bottom + 1, cx - 4, bottom - 3, color);
            m_sdlDrawer->renderLine(cx, bottom + 1, cx + 4, bottom - 3, color);
            break;
    }
}

void cCommandBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
{
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
        cUnit *selected = m_objects->getUnit(id);
        if (selected->isHarvester() && selected->canUnload()) {
            selected->findBestStructureCandidateAndHeadTowardsItOrWait(REFINERY, true, INTENT_UNLOAD_SPICE);
        }
    }
}

void cCommandBarDrawer::executeDeploy()
{
    for (int id : m_player->getSelectedUnits()) {
        cUnit *selected = m_objects->getUnit(id);
        if (!selected->isValid() || selected->getType() != MCV || !selected->belongsTo(m_player)) continue;
        if (!m_player->canPlaceStructureAt(selected->getCell(), CONSTYARD, selected->iID).success) continue;
        // at the structure cap the Construction Yard can't be created; keep the MCV
        if (m_objects->getStructureFactory()->getFreeSlot() < 0) {
            m_eventEmitter->emit(s_GameEvent{
                .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
                .data = NotificationEvent{
                    .message = localization::text("Cannot deploy: maximum number of structures reached.",
                                                  "Нельзя развернуть: достигнут предел построек."),
                    .type = eNotificationType::BAD,
                }
            });
            return;
        }
        const int cell = selected->getCell();
        selected->die(false, false);
        m_player->placeStructure(cell, CONSTYARD, 100);
        return;
    }
}

void cCommandBarDrawer::executeRelease()
{
    cAbstractStructure *selected = m_player->getSelectedStructure();
    if (!selected || selected->getType() != REPAIR) return;
    s_GameEvent event{
        .eventType = eGameEventType::GAME_EVENT_DEPLOY_UNIT,
        .data = CommonEvent{
            .entityType = eBuildType::UNKNOWN,
            .player = m_player
        }
    };
    selected->onNotifyGameEvent(event);
}

bool cCommandBarDrawer::hasAttackCapableUnit() const
{
    return std::ranges::any_of(m_player->getSelectedUnits(), [this](int id) {
        const cUnit *selected = m_objects->getUnit(id);
        const s_UnitInfo &info = selected->getUnitInfo();
        return !selected->isHarvester() && (info.canAttackUnits || info.canAttackAirUnits || info.canEnterAndDamageStructure);
    });
}

bool cCommandBarDrawer::hasUnloadableHarvester() const
{
    return std::ranges::any_of(m_player->getSelectedUnits(), [this](int id) {
        cUnit *selected = m_objects->getUnit(id);
        return selected->isHarvester() && selected->canUnload();
    });
}

bool cCommandBarDrawer::hasSelectedMcv() const
{
    return std::ranges::any_of(m_player->getSelectedUnits(), [this](int id) {
        cUnit *selected = m_objects->getUnit(id);
        return selected->isValid() && selected->getType() == MCV;
    });
}

std::string cCommandBarDrawer::getKeyLabel(eKeyAction action) const
{
    const cKeyBindings *bindings = m_keyboard->getKeyBindings();
    std::string name = bindings != nullptr ? bindings->getFirstKeyDisplayName(action) : std::string();
    std::ranges::transform(name, name.begin(), [](unsigned char character) {
        return static_cast<char>(std::toupper(character));
    });
    return name;
}
