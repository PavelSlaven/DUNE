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
#include "gui/GuiTheme.hpp"
#include "gui/RemasterButtonFrame.hpp"
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
#include "utils/Localization.hpp"

#include <algorithm>
#include <array>
#include <cctype>

namespace {
Color panelColor() { return Color{13, 17, 19, 242}; }
Color panelBorder() { return Color{105, 80, 39, 255}; }
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
    m_iconTextures(),
    m_iconSides(),
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

    m_iconSides.fill(0);
    m_panelRect = CommandBarLayout::create(m_settings->getScreenW(), m_settings->getScreenH(), cSideBar::SidebarWidth).panel;
}

cCommandBarDrawer::~cCommandBarDrawer() = default;

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
    const cGameControlsContext *controls = m_player->getGameControlsContext();
    const CommandTargetingState targeting = controls != nullptr ? controls->commandTargetingState() : CommandTargetingState{};
    const std::array<Button, CommandBarLayout::ActionCount> actions{{
        {Command::Move, layout.actions[0], localization::text("Move", "Переместить"), localization::text("LMB", "ЛКМ"), isMoveCommandEnabled(!selectedUnits.empty()), isCommandButtonActive(Command::Move, targeting)},
        {Command::Attack, layout.actions[1], localization::text("Attack", "Атаковать"), getKeyLabel(eKeyAction::ATTACK_MODE), isAttackCommandEnabled(hasAttackCapableUnit()), isCommandButtonActive(Command::Attack, targeting)},
        {Command::Repair, layout.actions[2], localization::text("Repair", "Ремонт"), getKeyLabel(eKeyAction::REPAIR_UNIT), isRepairCommandEnabled(), isCommandButtonActive(Command::Repair, targeting)},
        {Command::Unload, layout.actions[3], localization::text("Unload", "Разгрузить"), getKeyLabel(eKeyAction::SEND_TO_REFINERY), isUnloadCommandEnabled(hasUnloadableHarvester()), isCommandButtonActive(Command::Unload, targeting)},
        {Command::Deploy, layout.actions[4], localization::text("Deploy", "Развернуть"), getKeyLabel(eKeyAction::DEPLOY_UNIT), isDeployCommandEnabled(hasSelectedMcv()), isCommandButtonActive(Command::Deploy, targeting)},
        {Command::Rally, layout.actions[5], localization::text("Rally", "Точка сбора"), std::string(), isRallyCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->canHaveRallyPoint()), isCommandButtonActive(Command::Rally, targeting)},
        {Command::Release, layout.actions[6], localization::text("Release", "Выпустить"), getKeyLabel(eKeyAction::DEPLOY_UNIT), isReleaseCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->getType() == REPAIR), isCommandButtonActive(Command::Release, targeting)}
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

    const GuiTheme theme = GuiTheme::Remaster();
    m_sdlDrawer->renderRectFillColor(m_panelRect, panelColor(), panelColor().a);
    m_sdlDrawer->renderRectColor(m_panelRect, panelBorder());

    for (int index = 0; index < static_cast<int>(m_buttons.size()); ++index) {
        drawButton(m_buttons[index], theme, index == m_hoveredButton);
    }

    if (m_hoveredButton >= 0 && m_hoveredButton < static_cast<int>(m_buttons.size())) {
        drawTooltip(m_buttons[m_hoveredButton], theme);
    }
}

void cCommandBarDrawer::drawButton(const Button &button, const GuiTheme &theme, bool hovered)
{
    GuiTheme look = theme;
    Color iconColor = theme.textColor;
    if (!button.enabled) {
        look.fillColor = theme.disabledFillColor;
        look.borderLight = theme.disabledBorderLight;
        look.borderDark = theme.disabledBorderDark;
        iconColor = theme.disabledTextColor;
    }
    else if (button.active) {
        look.fillColor = Color{63, 52, 31, 255};
        look.borderLight = Color{188, 137, 42, 255};
        look.borderDark = Color{232, 184, 78, 255};
        iconColor = theme.textColorHover;
    }
    else if (hovered) {
        iconColor = theme.textColorHover;
    }

    const cRectangle frame(
        button.rect.getX() + 2,
        button.rect.getY() + 2,
        button.rect.getWidth() - 4,
        button.rect.getHeight() - 4
    );
    drawRemasterButtonFrame(*m_sdlDrawer, frame, look, button.enabled && hovered, false);

    const int side = std::min(frame.getWidth(), frame.getHeight()) * 70 / 100;
    if (Texture *icon = iconTexture(button.command, side)) {
        SDL_SetTextureColorMod(icon->tex.get(), iconColor.r, iconColor.g, iconColor.b);
        m_sdlDrawer->renderTexture(
            icon->tex.get(),
            frame.getX() + (frame.getWidth() - side) / 2,
            frame.getY() + (frame.getHeight() - side) / 2,
            side,
            side,
            iconColor.a
        );
    }

    const std::string cornerKey = cornerKeyLabel(button.hotkey);
    if (button.enabled && !cornerKey.empty()) {
        m_keyTextDrawer->drawText(
            frame.getEndX() - 3 - m_keyTextDrawer->getTextLength(cornerKey),
            frame.getEndY() - 3 - m_keyTextDrawer->getFontHeight(),
            theme.textColor,
            cornerKey
        );
    }
}

void cCommandBarDrawer::drawTooltip(const Button &button, const GuiTheme &theme) const
{
    constexpr int padding = 6;
    constexpr int gap = 6;
    const std::string text = commandTooltip(button.label, button.hotkey);
    const int width = m_keyTextDrawer->getTextLength(text) + padding * 2;
    const int height = m_keyTextDrawer->getFontHeight() + padding * 2;
    const int centreX = button.rect.getX() + button.rect.getWidth() / 2;
    const cRectangle box(
        std::clamp(centreX - width / 2, 0, std::max(0, m_settings->getScreenW() - width)),
        std::max(0, m_panelRect.getY() - gap - height),
        width,
        height
    );
    m_sdlDrawer->renderRectFillColor(box, theme.fillColor);
    m_sdlDrawer->renderRectColor(box, theme.borderLight);
    m_keyTextDrawer->drawText(box.getX() + padding, box.getY() + padding, theme.textColor, text);
}

Texture *cCommandBarDrawer::iconTexture(Command command, int side)
{
    const std::size_t index = static_cast<std::size_t>(command);
    if (side <= 0) return nullptr;
    if (m_iconTextures[index] && m_iconSides[index] == side) return m_iconTextures[index].get();

    constexpr int supersampling = 4;
    const int pixels = side * supersampling;
    m_iconTextures[index].reset(m_sdlDrawer->createRenderTargetTexture(pixels, pixels));
    m_iconSides[index] = side;
    SDL_Texture *texture = m_iconTextures[index]->tex.get();
    SDL_SetTextureScaleMode(texture, SDL_SCALEMODE_LINEAR);
    SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND);

    const std::vector<SDL_Vertex> vertices = tessellateCommandIcon(command, static_cast<float>(pixels), SDL_FColor{1.0F, 1.0F, 1.0F, 1.0F});
    SDL_Renderer *renderer = m_sdlDrawer->getRenderer();
    m_sdlDrawer->beginDrawingToTexture(m_iconTextures[index].get());
    // Transparent white, so that the linear downscale does not darken the edge pixels.
    m_sdlDrawer->renderClearToColor(Color{255, 255, 255, 0});
    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
    SDL_RenderGeometry(renderer, nullptr, vertices.data(), static_cast<int>(vertices.size()), nullptr, 0);
    m_sdlDrawer->endDrawingToTexture();
    return m_iconTextures[index].get();
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
