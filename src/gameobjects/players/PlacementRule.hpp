#pragma once

#include "include/definitions.h"

namespace placement_rule {

struct CellFacts {
    bool withinBoundaries = true;
    bool validTerrain = true;
    bool structurePresent = false;
    bool livingUnitPresent = false;
};

struct CellVerdict {
    bool outOfBounds = false;
    bool badTerrain = false;
    bool structureBlocks = false;
    bool unitBlocks = false;

    [[nodiscard]] bool allowed() const
    {
        return !outOfBounds && !badTerrain && !structureBlocks && !unitBlocks;
    }
};

inline CellVerdict judgeCell(int structureType, const CellFacts &facts)
{
    CellVerdict verdict;
    if (!facts.withinBoundaries) {
        verdict.outOfBounds = true;
        return verdict;
    }
    if (structureType == SLAB4) {
        return verdict;
    }
    verdict.badTerrain = !facts.validTerrain;
    verdict.structureBlocks = facts.structurePresent;
    verdict.unitBlocks = facts.livingUnitPresent;
    return verdict;
}

struct AnchorFacts {
    bool ownStructure = false;
    bool otherStructure = false;
    bool wallOrSlab = false;
};

inline bool isBuildAnchor(const AnchorFacts &facts)
{
    if (facts.ownStructure) {
        return true;
    }
    if (facts.otherStructure) {
        return false;
    }
    return facts.wallOrSlab;
}

}
