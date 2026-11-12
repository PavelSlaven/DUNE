#include "cUnitFactory.h"

#include "building/cItemBuilder.h"
#include "context/cGameObjectContext.h"
#include "context/cInfoContext.h"
#include "drawers/cUnitDrawer.h"
#include "gameobjects/map/MapGeometry.hpp"
#include "gameobjects/map/cMap.h"
#include "gameobjects/map/cMapCamera.h"
#include "gameobjects/players/cPlayer.h"
#include "gameobjects/players/cPlayerDifficultySettings.h"
#include "gameobjects/units/cUnit.h"
#include "gameobjects/units/cUnits.h"
#include "include/definitions.h"
#include "utils/cStructureUtils.h"
#include "utils/common.h"
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
    return factory_pad::padOrigin(pos_x(), pos_y(), getWidth(), getHeight(), TILESIZE_WIDTH_PIXELS, TILESIZE_HEIGHT_PIXELS);
}

int cUnitFactory::findExitCell(int unitType)
{
    const int x = m_objects->getMapGeometry()->getCellX(getCell());
    const int y = m_objects->getMapGeometry()->getCellY(getCell());
    return factory_pad::chooseExitCell(
        x, y, getWidth(), getHeight(),
        [this](int cellX, int cellY) {
            return m_objects->getMapGeometry()->getCellWithMapBorders(cellX, cellY);
        },
        [this, unitType](int cell) {
            return !m_objects->getMap()->occupied(cell) &&
                   m_objects->getMap()->canDeployUnitTypeAtCell(cell, unitType);
        });
}

int cUnitFactory::padCell()
{
    return m_objects->getMapGeometry()->makeCell(m_objects->getMapGeometry()->getCellX(getCell()) + getWidth() - 1,
                                                 m_objects->getMapGeometry()->getCellY(getCell()) + getHeight() - 1);
}

bool cUnitFactory::carryallStillCalled()
{
    if (m_pad.carryallId < 0) {
        return false;
    }
    const cUnit *carryall = m_objects->getUnit(m_pad.carryallId);
    return carryall->isValid() && carryall->iType == CARRYALL && carryall->iPlayer == iPlayer &&
           carryall->iBringTarget == padCell() &&
           (carryall->m_transferType == eTransferType::PAD_PICKUP_STAY ||
            carryall->m_transferType == eTransferType::PAD_PICKUP_LEAVE);
}

void cUnitFactory::requestCarryall()
{
    const int cell = padCell();
    int carryallId = cUnit::carryallNearestFree(getOwner(), cell, m_objects);
    if (carryallId > -1) {
        m_objects->getUnit(carryallId)->carryall_order(-1, eTransferType::PAD_PICKUP_STAY, cell, -1);
    }
    else {
        carryallId = cUnit::spawnCarryallAtBorder(getOwner(), cell, m_objects, m_info, m_eventEmitter);
    }
    if (carryallId > -1) {
        m_pad.carryallId = carryallId;
    }
}

void cUnitFactory::releaseCarryall()
{
    if (carryallStillCalled()) {
        cUnit *carryall = m_objects->getUnit(m_pad.carryallId);
        if (carryall->m_transferType == eTransferType::PAD_PICKUP_LEAVE) {
            carryall->m_transferType = eTransferType::DIE;
            carryall->setGoalCell(iFindCloseBorderCell(carryall->getCell(), m_objects));
        }
        else {
            carryall->setGoalCell(carryall->getCell());
            carryall->m_transferType = eTransferType::NONE;
        }
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

bool cUnitFactory::isFlickeringFactory()
{
    cItemBuilder *builder = getPlayer()->getItemBuilder();
    if (!builder || !builder->isBuildingUnitForStructureType(getType())) {
        return false;
    }
    return m_structureUtils->findFactoryForFinishedUnit(getPlayer(), getType()) == getStructureId();
}

void cUnitFactory::thinkFlicker()
{
    factory_pad::advanceFlicker(iFrame, m_flickerTimer, isFlickeringFactory());
}

void cUnitFactory::thinkPad()
{
    thinkFlicker();

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
    if (m_objects->getUnits()->isUnitLimitReached()) {
        return;
    }

    const int unitId = cUnits::unitCreate(m_objects, m_info, m_eventEmitter, exitCell, m_pad.unitType, getOwner(), true, false);
    if (unitId < 0) {
        return;
    }

    cUnit *rolling = m_objects->getUnit(unitId);
    const factory_pad::Point from = padOrigin();
    const int toX = m_objects->getMapGeometry()->getAbsoluteXPositionFromCell(exitCell);
    const int toY = m_objects->getMapGeometry()->getAbsoluteYPositionFromCell(exitCell);
    const Facing facing = facingFromInt(faceAngle(fDegrees(from.x, from.y, toX, toY)));

    rolling->bRollingOffFactoryPad = true;
    rolling->iRollingOffFactoryPadStructureId = getStructureId();
    rolling->setPosX(static_cast<float>(from.x));
    rolling->setPosY(static_cast<float>(from.y));
    rolling->rendering.iBodyFacing = facing;
    rolling->rendering.iBodyShouldFace = facing;
    rolling->rendering.iHeadFacing = facing;
    rolling->rendering.iHeadShouldFace = facing;
    factory_pad::startRoll(m_pad, unitId);
}

void cUnitFactory::advanceRoll()
{
    cUnit *rolling = m_objects->getUnit(m_pad.rollUnitId);
    if (!rolling->isValid() || !rolling->bRollingOffFactoryPad ||
            rolling->iRollingOffFactoryPadStructureId != getStructureId()) {
        finishRoll();
        return;
    }

    const factory_pad::Point from = padOrigin();
    const factory_pad::Point to{m_objects->getMapGeometry()->getAbsoluteXPositionFromCell(rolling->getCell()),
                                m_objects->getMapGeometry()->getAbsoluteYPositionFromCell(rolling->getCell())};
    const int steps = factory_pad::rollSteps(from, to);
    const float cost = m_objects->getPlayer(rolling->iPlayer)->getDifficultySettings()->getMoveSpeed(
        rolling->iType, m_objects->getMap()->getCellSlowDown(rolling->getCell()));
    const factory_pad::RollTick result = factory_pad::tickRoll(m_pad, static_cast<int>(std::ceil(cost)), steps);
    if (result.advanced) {
        const factory_pad::Point now = factory_pad::rollPosition(from, to, m_pad.rollStep);
        rolling->setPosX(static_cast<float>(now.x));
        rolling->setPosY(static_cast<float>(now.y));
    }
    if (result.done) {
        finishRoll();
    }
}

void cUnitFactory::finishRoll()
{
    const int unitId = m_pad.rollUnitId;
    if (unitId > -1 && m_objects->getUnit(unitId)->isValid() &&
            m_objects->getUnit(unitId)->bRollingOffFactoryPad &&
            m_objects->getUnit(unitId)->iRollingOffFactoryPadStructureId == getStructureId()) {
        cUnit *rolling = m_objects->getUnit(unitId);
        rolling->bRollingOffFactoryPad = false;
        rolling->iRollingOffFactoryPadStructureId = -1;
        rolling->setPosX(static_cast<float>(m_objects->getMapGeometry()->getAbsoluteXPositionFromCell(rolling->getCell())));
        rolling->setPosY(static_cast<float>(m_objects->getMapGeometry()->getAbsoluteYPositionFromCell(rolling->getCell())));

        if (rolling->iPlayer > 0 && rolling->iPlayer < AI_WORM && !rolling->isAirbornUnit() &&
                rolling->movement.iGoalCell == rolling->getCell()) {
            const int freeCell = cUnit::freeAroundMove(unitId, m_objects);
            if (freeCell > -1) {
                rolling->move_to(freeCell);
            }
        }
        if (getRallyPoint() > -1) {
            rolling->move_to(getRallyPoint(), -1, -1, INTENT_MOVE);
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
        cUnit *rolling = m_objects->getUnit(m_pad.rollUnitId);
        if (rolling->isValid() && rolling->bRollingOffFactoryPad &&
                rolling->iRollingOffFactoryPadStructureId == getStructureId()) {
            rolling->bRollingOffFactoryPad = false;
            rolling->iRollingOffFactoryPadStructureId = -1;
            rolling->setPosX(static_cast<float>(m_objects->getMapGeometry()->getAbsoluteXPositionFromCell(rolling->getCell())));
            rolling->setPosY(static_cast<float>(m_objects->getMapGeometry()->getAbsoluteYPositionFromCell(rolling->getCell())));
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
    const s_UnitInfo &info = m_info->getUnitInfo(m_pad.unitType);
    const cRectangle visual = cUnitDrawer::visualRectangleAt(m_mapCamera, info, static_cast<float>(origin.x), static_cast<float>(origin.y));
    cUnitDrawer::drawSprites(m_renderer, m_mapCamera, getPlayer(), m_pad.unitType, info, Facing::DOWN, Facing::DOWN, 0, visual, true);
}
