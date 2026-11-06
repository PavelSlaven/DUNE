#pragma once

#include "cAbstractStructure.h"
#include "FactoryPad.hpp"

class cUnitFactory : public cAbstractStructure {
public:
    cUnitFactory();

    bool isPadFree() const {
        return m_pad.phase == factory_pad::Phase::Empty;
    }

    bool hasUnitStandingOnPad() const {
        return m_pad.phase == factory_pad::Phase::Standing;
    }

    int getUnitTypeOnPad() const {
        return m_pad.unitType;
    }

    void acceptReadyUnit(int unitType);

    void drawUnitOnPad();

    void releasePad() override;

    int takeUnitForCarryall(int carryallId);

    const factory_pad::PadState &getPad() const {
        return m_pad;
    }
    void restorePad(const factory_pad::PadState &pad);

protected:
    void thinkPad();
    void thinkFlicker();

private:
    factory_pad::Point padOrigin();
    int findExitCell(int unitType);
    int padCell();
    bool carryallStillCalled() const;
    void requestCarryall();
    void releaseCarryall();
    void beginRoll(int exitCell);
    void advanceRoll();
    void finishRoll();

    bool isFlickeringFactory();

    factory_pad::PadState m_pad;
    int m_flickerTimer = 0;
};
