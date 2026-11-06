#include "cUnitFactory.h"

#include "d2tmc.h"
#include "definitions.h"
#include "gameobjects/units/cUnit.h"
#include "map/MapGeometry.hpp"
#include "map/cMap.h"
#include "player/cPlayer.h"
#include "utils/d2tm_math.h"

#include <algorithm>
#include <cmath>

cUnitFactory::cUnitFactory() = default;

void cUnitFactory::acceptReadyUnit(int unitType)
{
    if (factory_pad::offer(m_pad, unitType) == factory_pad::Offer::Appeared) {
        setAnimating(true);
    }
}

factory_pad::Point cUnitFactory::padOrigin()
{
    const factory_pad::Point center = factory_pad::padCenter(getWidth(), getHeight());
    return {pos_x() + center.x - TILESIZE_WIDTH_PIXELS / 2, pos_y() + center.y - TILESIZE_HEIGHT_PIXELS / 2};
}

int cUnitFactory::findExitCell(int unitType)
{
    const int x = global_map.getCellX(getCell());
    const int y = global_map.getCellY(getCell());
    return factory_pad::chooseExitCell(
               x, y, getWidth(), getHeight(),
    [](int cellX, int cellY) {
        return global_map.getGeometry().getCellWithMapBorders(cellX, cellY);
    },
    [unitType](int cell) {
        return !global_map.occupied(cell) && global_map.canDeployUnitTypeAtCell(cell, unitType);
    });
}

int cUnitFactory::padCell()
{
    return global_map.getGeometry().makeCell(global_map.getCellX(getCell()) + getWidth() - 1,
            global_map.getCellY(getCell()) + getHeight() - 1);
}

bool cUnitFactory::carryallStillCalled() const
{
    if (m_pad.carryallId < 0) {
        return false;
    }
    const cUnit &carryall = unit[m_pad.carryallId];
    return carryall.isValid() && carryall.iType == CARRYALL && carryall.iPlayer == iPlayer &&
           (carryall.m_transferType == eTransferType::PAD_PICKUP_STAY ||
            carryall.m_transferType == eTransferType::PAD_PICKUP_LEAVE);
}

void cUnitFactory::requestCarryall()
{
    const int cell = padCell();
    int carryallId = CARRYALL_NEAREST_FREE(getOwner(), cell);
    if (carryallId > -1) {
        unit[carryallId].carryall_order(-1, eTransferType::PAD_PICKUP_STAY, cell, -1);
    }
    else {
        carryallId = SPAWN_CARRYALL_AT_BORDER(getOwner(), cell);
    }
    if (carryallId > -1) {
        m_pad.carryallId = carryallId;
    }
}

void cUnitFactory::releaseCarryall()
{
    if (carryallStillCalled()) {
        cUnit &carryall = unit[m_pad.carryallId];
        carryall.setGoalCell(carryall.iCell);
        carryall.m_transferType = eTransferType::NONE;
    }
    m_pad.carryallId = -1;
}

int cUnitFactory::takeUnitForCarryall(int carryallId)
{
    if (m_pad.phase != factory_pad::Phase::Standing || m_pad.carryallId != carryallId) {
        return -1;
    }
    const int unitType = m_pad.unitType;
    if (factory_pad::finishPad(m_pad) > -1) {
        setAnimating(true);
    }
    return unitType;
}

void cUnitFactory::thinkPad()
{
    switch (m_pad.phase) {
        case factory_pad::Phase::Empty:
            return;
        case factory_pad::Phase::Standing: {
            if (m_pad.carryallId > -1 && !carryallStillCalled()) {
                m_pad.carryallId = -1;
            }
            const bool animationFinished = !isAnimating();
            const int exitCell = animationFinished ? findExitCell(m_pad.unitType) : -1;
            const factory_pad::StandingAction action = factory_pad::tickStanding(m_pad, animationFinished, exitCell > -1);
            if (action == factory_pad::StandingAction::StartRoll) {
                releaseCarryall();
                beginRoll(exitCell);
            }
            else if (action == factory_pad::StandingAction::RequestCarryall) {
                requestCarryall();
            }
            return;
        }
        case factory_pad::Phase::Rolling:
            advanceRoll();
            return;
    }
}

void cUnitFactory::beginRoll(int exitCell)
{
    const int unitId = UNIT_CREATE(exitCell, m_pad.unitType, getOwner(), true, false);
    if (unitId < 0) {
        return;
    }

    cUnit &rolling = unit[unitId];
    const factory_pad::Point from = padOrigin();
    const int toX = global_map.getAbsoluteXPositionFromCell(exitCell);
    const int toY = global_map.getAbsoluteYPositionFromCell(exitCell);
    const int facing = faceAngle(fDegrees(from.x, from.y, toX, toY));

    rolling.bRollingOffFactoryPad = true;
    rolling.posX = static_cast<float>(from.x);
    rolling.posY = static_cast<float>(from.y);
    rolling.iBodyFacing = facing;
    rolling.iBodyShouldFace = facing;
    rolling.iHeadFacing = facing;
    rolling.iHeadShouldFace = facing;
    factory_pad::startRoll(m_pad, unitId);
}

void cUnitFactory::advanceRoll()
{
    cUnit &rolling = unit[m_pad.rollUnitId];
    if (!rolling.isValid() || !rolling.bRollingOffFactoryPad) {
        finishRoll();
        return;
    }

    const factory_pad::Point from = padOrigin();
    const factory_pad::Point to{global_map.getAbsoluteXPositionFromCell(rolling.iCell),
                                global_map.getAbsoluteYPositionFromCell(rolling.iCell)};
    const int steps = factory_pad::rollSteps(from, to);
    const float cost = players[rolling.iPlayer].getDifficultySettings()->getMoveSpeed(
                           rolling.iType, global_map.getCellSlowDown(rolling.iCell));
    const factory_pad::RollTick result = factory_pad::tickRoll(m_pad, static_cast<int>(std::ceil(cost)), steps);
    if (result.advanced) {
        const factory_pad::Point now = factory_pad::rollPosition(from, to, m_pad.rollStep);
        rolling.posX = static_cast<float>(now.x);
        rolling.posY = static_cast<float>(now.y);
    }
    if (result.done) {
        finishRoll();
    }
}

void cUnitFactory::finishRoll()
{
    const int unitId = m_pad.rollUnitId;
    if (unitId > -1 && unit[unitId].isValid() && unit[unitId].bRollingOffFactoryPad) {
        cUnit &rolling = unit[unitId];
        rolling.bRollingOffFactoryPad = false;
        rolling.posX = static_cast<float>(global_map.getAbsoluteXPositionFromCell(rolling.iCell));
        rolling.posY = static_cast<float>(global_map.getAbsoluteYPositionFromCell(rolling.iCell));

        if (rolling.iPlayer > 0 && rolling.iPlayer < AI_WORM && !rolling.isAirbornUnit() &&
                rolling.iGoalCell == rolling.iCell) {
            const int freeCell = UNIT_FREE_AROUND_MOVE(unitId);
            if (freeCell > -1) {
                rolling.move_to(freeCell);
            }
        }
        if (getRallyPoint() > -1) {
            rolling.move_to(getRallyPoint(), -1, -1, INTENT_MOVE);
        }
    }

    const int nextType = factory_pad::finishPad(m_pad);
    if (nextType > -1) {
        setAnimating(true);
    }
}

void cUnitFactory::releasePad()
{
    releaseCarryall();
    if (m_pad.phase == factory_pad::Phase::Rolling && m_pad.rollUnitId > -1) {
        cUnit &rolling = unit[m_pad.rollUnitId];
        if (rolling.isValid() && rolling.bRollingOffFactoryPad) {
            rolling.bRollingOffFactoryPad = false;
            rolling.posX = static_cast<float>(global_map.getAbsoluteXPositionFromCell(rolling.iCell));
            rolling.posY = static_cast<float>(global_map.getAbsoluteYPositionFromCell(rolling.iCell));
        }
    }
    m_pad = factory_pad::PadState();
}

void cUnitFactory::restorePad(const factory_pad::PadState &pad)
{
    m_pad = pad;
}

void cUnitFactory::drawUnitOnPad()
{
    if (m_pad.phase != factory_pad::Phase::Standing || m_pad.unitType < 0) {
        return;
    }
    const factory_pad::Point origin = padOrigin();
    const cRectangle visual = cUnit::visualRectangleAt(m_pad.unitType, static_cast<float>(origin.x),
                              static_cast<float>(origin.y));
    cUnit::drawSprites(getOwner(), m_pad.unitType, FACE_DOWN, FACE_DOWN, 0, visual, true);
}
