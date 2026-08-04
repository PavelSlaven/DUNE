#pragma once

class GameContext;
class Graphics;

#include "gameobjects/structures/cAbstractStructure.h"
#include "utils/cStructureUtils.h"
#include "utils/Color.hpp"

class cStructureDrawer {
public:
    explicit cStructureDrawer(GameContext *ctx);
    ~cStructureDrawer() = default;
    void drawStructuresFirstLayer();
    void drawStructuresSecondLayer();
    void drawStructuresHealthBars();

protected:
    void drawStructureHealthBar(int iStructure);
    void drawStructuresForLayer(int layer);
    void drawRectangleOfStructure(cAbstractStructure *theStructure, Color color);
    void drawStructurePrebuildAnimation(cAbstractStructure *structure);
    void drawStructureAnimation(cAbstractStructure *structure);
    void drawStructureAnimationRefinery(cAbstractStructure *structure);
    void drawStructureAnimationTurret(cAbstractStructure *structure);
    void drawStructureForLayer(cAbstractStructure *structure, int layer);

    int determinePreBuildAnimationIndex(cAbstractStructure *structure);

private:
    Graphics *m_gfxdata;
    Graphics *m_gfxinter;
    cStructureUtils structureUtils;

    void renderIconOfUnitBeingRepaired(cAbstractStructure *structure) const;
    void renderIconThatStructureIsBeingRepaired(cAbstractStructure *structure) const;
    void drawHdBuildingFoundation(cAbstractStructure *structure) const;
    bool drawHdBarracksFlag(cAbstractStructure *structure) const;
    bool drawHdWorFlag(cAbstractStructure *structure) const;
    bool drawHdRadarFlag(cAbstractStructure *structure) const;
    bool drawHdConstYardFlag(cAbstractStructure *structure) const;
    bool drawHdRefineryFlag(cAbstractStructure *structure) const;
    bool drawHdPalaceFlag(cAbstractStructure *structure) const;
    bool drawHdIxFlag(cAbstractStructure *structure) const;
    bool drawHdLightFactoryFlag(cAbstractStructure *structure) const;
    bool drawHdHighTechFlag(cAbstractStructure *structure) const;
    bool drawHdSiloFlag(cAbstractStructure *structure) const;
    bool drawHdStarportFlag(cAbstractStructure *structure) const;
    bool drawHdWindTrapFlag(cAbstractStructure *structure) const;
    void drawHarvesterOnRefineryPad(cAbstractStructure *structure) const;
};
