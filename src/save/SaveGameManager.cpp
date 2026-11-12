#include "save/SaveGameManager.hpp"

#include "building/cItemBuilder.h"
#include "context/cGameObjectContext.h"
#include "context/cInfoContext.h"
#include "data/gfxaudio.h"
#include "data/gfxdata.h"
#include "game/cGame.h"
#include "game/cGameConditionChecker.h"
#include "game/cGameSettings.h"
#include "gameobjects/map/cMap.h"
#include "gameobjects/map/cMapCamera.h"
#include "gameobjects/particles/cParticle.h"
#include "gameobjects/particles/cParticles.h"
#include "gameobjects/players/cHousesInfo.h"
#include "gameobjects/players/cPlayer.h"
#include "gameobjects/projectiles/bullet.h"
#include "gameobjects/projectiles/cBullets.h"
#include "gameobjects/structures/cAbstractStructure.h"
#include "gameobjects/structures/cUnitFactory.h"
#include "gameobjects/units/cReinforcements.h"
#include "gameobjects/units/cUnit.h"
#include "gameobjects/units/cUnits.h"
#include "include/eGameState.h"
#include "include/sDataCampaign.h"
#include "managers/cDrawManager.h"
#include "save/SaveBody.hpp"
#include "save/SaveFileCodec.hpp"
#include "save/SaveSlotName.hpp"
#include "save/SaveSnapshot.hpp"
#include "sidebar/cBuildingList.h"
#include "sidebar/cBuildingListItem.h"
#include "sidebar/cSideBar.h"
#include "utils/Localization.hpp"
#include "utils/Log.h"

#include <algorithm>
#include <array>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <format>
#include <iterator>
#include <optional>
#include <string>
#include <string_view>
#include <system_error>
#include <utility>

#ifdef _WIN32
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#endif

static_assert(save_game_detail::PathSize == MAX_PATH_SIZE);
static_assert(save_game_detail::UnitSlots == cUnits::TOTAL_SLOTS);
static_assert(save_game_detail::HouseCount == MAX_HOUSES);
static_assert(save_game_detail::UnitTypeCount == MAX_UNITTYPES);
static_assert(save_game_detail::UpgradeTypeCount == MAX_UPGRADETYPES);
static_assert(save_game_detail::DefaultTimerCap == cBuildingListItem::DefaultTimerCap);

namespace {

std::filesystem::path g_savesDirectory = "saves";

void restoreCellState(cMap &map, const save_game_detail::SaveSnapshot &save)
{
    for (int index = 0; index < map.getMaxCells(); ++index) {
        tCell *target = map.getCell(index);
        const save_game_detail::CellState &source = save.cells[static_cast<std::size_t>(index)];
        target->credits = source.credits;
        target->type = source.type;
        target->tile = source.tile;
        target->smudgetile = source.smudgeTile;
        target->smudgetype = source.smudgeType >= 0
            ? std::optional<SmudgeType>(static_cast<SmudgeType>(source.smudgeType))
            : std::nullopt;
        target->health = source.health;
        target->passable = source.passable;
        target->passableFoot = source.passableFoot;
        for (int player = 0; player < MAX_PLAYERS; ++player) {
            target->iVisible[player] = (source.visibilityMask & (1U << player)) != 0;
            target->iSeen[player] = (source.seenMask & (1U << player)) != 0;
        }
    }
}

int translateStructureId(
    int oldId,
    const std::array<int, MAX_STRUCTURES> &mapping)
{
    if (oldId < 0 || oldId >= MAX_STRUCTURES) {
        return -1;
    }
    return mapping[oldId];
}

cBuildingListItem *findBuildItem(cGame &game, const save_game_detail::BuildQueueState &saved)
{
    if (saved.player < 0 || saved.player >= MAX_PLAYERS ||
        saved.listType < 0 || saved.listType > eListTypeAsInt(eListType::LIST_UPGRADES)) {
        return nullptr;
    }
    cPlayer *player = game.m_gameObjectsContext->getPlayer(saved.player);
    cSideBar *sidebar = player ? player->getSideBar() : nullptr;
    cBuildingList *list = sidebar ? sidebar->getList(saved.listType) : nullptr;
    if (!list) {
        return nullptr;
    }
    for (int index = 0; index < list->getItemCount(); ++index) {
        cBuildingListItem *item = list->getItem(index);
        if (item &&
            static_cast<int>(item->getBuildType()) == saved.buildType &&
            item->getBuildId() == saved.buildId &&
            item->getSubList() == saved.subList) {
            return item;
        }
    }
    return nullptr;
}

bool writeAtomically(
    const std::filesystem::path &destination,
    std::string_view contents,
    std::string &error)
{
    std::error_code directoryError;
    std::filesystem::create_directories(
        destination.parent_path(),
        directoryError
    );
    if (directoryError) {
        error = localization::text("Could not create the saves folder", "Не удалось создать папку saves");
        return false;
    }
    const std::filesystem::path temporary =
        destination.string() + ".tmp";
    {
        std::ofstream output(
            temporary,
            std::ios::binary | std::ios::trunc
        );
        if (!output) {
            error = localization::text("Could not create temporary save file", "Не удалось создать временный файл сохранения");
            return false;
        }
        output.write(
            contents.data(),
            static_cast<std::streamsize>(contents.size())
        );
        output.flush();
        if (!output) {
            error = localization::text("Error writing save file", "Ошибка записи сохранения");
            output.close();
            std::filesystem::remove(temporary, directoryError);
            return false;
        }
    }
#ifdef _WIN32
    if (!MoveFileExW(
            temporary.wstring().c_str(),
            destination.wstring().c_str(),
            MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)) {
        error = localization::format(
            "Could not replace save file (Windows error {})",
            "Не удалось заменить сохранение (ошибка Windows {})",
            GetLastError()
        );
        std::filesystem::remove(temporary, directoryError);
        return false;
    }
#else
    std::filesystem::rename(temporary, destination, directoryError);
    if (directoryError) {
        error = localization::format(
            "Could not replace save file ({})",
            "Не удалось заменить сохранение ({})",
            directoryError.message()
        );
        std::filesystem::remove(temporary, directoryError);
        return false;
    }
#endif
    return true;
}

}

save_game_detail::SaveSnapshot SaveGameManager::captureSnapshot(cGame &game)
{
    using namespace save_game_detail;

    SaveSnapshot save;
    cMap *map = game.m_gameObjectsContext->getMap();
    save.skirmish = game.m_gameSettings->isSkirmish();
    save.region = game.m_dataCampaign->region;
    save.mission = game.m_dataCampaign->mission;
    save.winFlags = game.m_gameConditionChecker->m_winFlags;
    save.loseFlags = game.m_gameConditionChecker->m_loseFlags;
    save.mapWidth = map->getGeometry()->getWidth();
    save.mapHeight = map->getGeometry()->getHeight();
    save.autoSpawnBlooms = map->m_bAutoSpawnSpiceBlooms;
    save.autoDetonateBlooms = map->m_bAutoDetonateSpiceBlooms;
    save.bloomTimer = map->m_iTIMER_blooms;
    save.desiredWorms = map->m_iDesiredAmountOfWorms;
    save.wormRespawnTimer = map->m_iTIMER_respawnSandworms;

    const int cameraX = game.m_mapCamera->getViewportCenterX();
    const int cameraY = game.m_mapCamera->getViewportCenterY();
    save.cameraCell = map->getGeometry()->makeCell(
        std::clamp(cameraX / TILESIZE_WIDTH_PIXELS, 0, save.mapWidth - 1),
        std::clamp(cameraY / TILESIZE_HEIGHT_PIXELS, 0, save.mapHeight - 1)
    );

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        const cPlayer &source = *game.m_gameObjectsContext->getPlayer(index);
        PlayerState &target = save.players[index];
        target.house = source.house;
        target.team = source.iTeam;
        target.techLevel = source.techLevel;
        target.focusCell = source.focusCell_;
        target.quota = source.spiceQuota;
        target.selectedStructure = source.selected_structure;
        target.credits = source.credits;
        target.maxCredits = source.maxCredits_;
        target.powerUsage = source.powerUsage_;
        target.powerProduce = source.powerProduce_;
        target.alive = source.alive;
        target.autoSlab = source.m_autoSlabStructures;
        std::copy_n(source.iPrimaryBuilding, MAX_STRUCTURETYPES, target.primary.begin());
        std::copy_n(source.iStructures, MAX_STRUCTURETYPES, target.structures.begin());
        std::copy_n(source.iStructureUpgradeLevel, MAX_STRUCTURETYPES, target.upgrades.begin());
        std::copy_n(source.m_appliedUpgrades, UpgradeTypeCount, target.appliedUpgrades.begin());
    }

    save.cells.reserve(static_cast<std::size_t>(map->getMaxCells()));
    for (int index = 0; index < map->getMaxCells(); ++index) {
        const tCell *source = map->getCell(index);
        CellState target;
        target.credits = source->credits;
        target.type = source->type;
        target.tile = source->tile;
        target.smudgeTile = source->smudgetile;
        target.smudgeType = source->smudgetype ? static_cast<int>(*source->smudgetype) : -1;
        target.health = source->health;
        target.passable = source->passable;
        target.passableFoot = source->passableFoot;
        for (int player = 0; player < MAX_PLAYERS; ++player) {
            if (source->iVisible[player]) {
                target.visibilityMask |= (1U << player);
            }
            if (source->iSeen[player]) {
                target.seenMask |= (1U << player);
            }
        }
        save.cells.push_back(target);
    }

    for (int index = 0; index < map->getMaxCells(); ++index) {
        const s_RememberedTerrain *terrain = map->m_fogMemory.getTerrain(index);
        const s_RememberedStructure *structure = map->m_fogMemory.getStructure(index);
        const s_RememberedUnit *unit = map->m_fogMemory.getUnit(index);
        if (terrain == nullptr && structure == nullptr && unit == nullptr) {
            continue;
        }
        FogState target;
        target.cell = index;
        if (terrain != nullptr) {
            target.hasTerrain = true;
            target.terrainType = terrain->type;
            target.terrainTile = terrain->tile;
            target.terrainSmudgeTile = terrain->smudgetile;
            target.terrainSmudgeType = terrain->smudgetype
                ? static_cast<int>(*terrain->smudgetype)
                : -1;
        }
        if (structure != nullptr) {
            target.hasStructure = true;
            target.structureType = structure->type;
            target.structureOwner = structure->ownerId;
            target.structureFrame = structure->frame;
            target.structureOffsetX = structure->offsetX;
            target.structureOffsetY = structure->offsetY;
        }
        if (unit != nullptr) {
            target.hasUnit = true;
            target.unitType = unit->type;
            target.unitOwner = unit->ownerId;
            target.unitBodyIndex = unit->bodyIndex;
            target.unitHeadIndex = unit->headIndex;
            target.unitFrame = unit->frame;
        }
        save.fog.push_back(target);
    }

    for (int index = 0; index < MAX_STRUCTURES; ++index) {
        cAbstractStructure *source = game.m_gameObjectsContext->getStructure(index);
        if (source == nullptr || !source->isValid()) {
            continue;
        }
        StructureState target;
        target.oldId = index;
        target.type = source->getType();
        target.player = source->iPlayer;
        target.cell = source->iCell;
        target.hitPoints = source->iHitPoints;
        target.rallyPoint = source->iRallyPoint;
        target.frame = source->iFrame;
        target.buildPhase = source->iBuildFase;
        target.unitWithin = source->iUnitIDWithinStructure;
        target.unitEntering = source->iUnitIDEnteringStructure;
        target.unitHeading = source->iUnitIDHeadingForStructure;
        target.concrete = source->fConcrete;
        target.animate = source->bAnimate;
        target.repair = source->bRepair;
        target.animateOnApproach = source->shouldAnimateWhenUnitHeadsTowardsStructure;
        target.smoke = source->m_smokeParticlesCreated;
        target.repairTimer = source->TIMER_repair;
        target.flagTimer = source->TIMER_flag;
        target.reduceSmokeTimer = source->TIMER_reduceSmoke;
        target.decayTimer = source->TIMER_decay;
        target.prebuildTimer = source->TIMER_prebuild;
        save.structures.push_back(target);

        if (const auto *factory = dynamic_cast<const cUnitFactory *>(source)) {
            if (!factory->isPadFree()) {
                save.factoryPads.push_back({index, factory->getPad()});
            }
        }
    }

    for (int index = 0; index < cUnits::TOTAL_SLOTS; ++index) {
        cUnit *source = game.m_gameObjectsContext->getUnit(index);
        if (source == nullptr || !source->isValid()) {
            continue;
        }
        UnitState target;
        target.oldId = index;
        target.type = source->iType;
        target.player = source->iPlayer;
        target.cell = source->getCell();
        target.hitPoints = source->iHitPoints;
        target.tempHitPoints = source->iTempHitPoints;
        target.posX = source->getPosX();
        target.posY = source->getPosY();
        target.experience = source->fExperience;
        for (int group = 0; group < MAX_UNIT_GROUPS; ++group) {
            if (source->iGroups[group]) {
                target.groupMask |= 1 << group;
            }
        }
        target.nextCell = source->movement.iNextCell;
        target.goalCell = source->movement.iGoalCell;
        std::copy_n(source->movement.iPath, PathSize, target.path.begin());
        target.pathIndex = source->movement.iPathIndex;
        target.pathFails = source->movement.iPathFails;
        target.calculatePath = source->movement.bCalculateNewPath;
        target.carryMe = source->bCarryMe;
        target.carryAll = source->iCarryAll;
        target.attackUnit = source->combat.iAttackUnit;
        target.attackStructure = source->combat.iAttackStructure;
        target.attackCell = source->combat.iAttackCell;
        target.unitId = source->iUnitID;
        target.structureId = source->iStructureID;
        target.credits = source->iCredits;
        target.transferType = static_cast<int>(source->m_transferType);
        target.bringTarget = source->iBringTarget;
        target.newUnitType = source->iNewUnitType;
        target.lastDroppedOffCell = source->lastDroppedOffCell;
        target.bodyFacing = static_cast<int>(source->rendering.iBodyFacing);
        target.headFacing = static_cast<int>(source->rendering.iHeadFacing);
        target.bodyShouldFace = static_cast<int>(source->rendering.iBodyShouldFace);
        target.headShouldFace = static_cast<int>(source->rendering.iHeadShouldFace);
        target.frame = source->rendering.iFrame;
        target.selected = source->m_bSelected;
        target.action = static_cast<int>(source->m_action);
        target.intent = static_cast<int>(source->intent);
        target.willBePickedUpBy = source->willBePickedUpBy;
        target.pickedUp = source->bPickedUp;
        target.removeMe = source->bRemoveMe;
        target.mission = source->mission;
        target.reinforcement = source->isReinforcement;
        target.unitsEaten = source->unitsEaten;
        target.harvestCellMemory = source->iHarvestCellMemory;
        target.stayAtGoalCell = source->m_stayAtGoalCell;
        target.timers = {
            source->moveTimer.get(),
            source->movewaitTimer.get(),
            source->movedelayTimer.get(),
            source->turnTimer.get(),
            source->thinkwaitTimer.get(),
            source->frameTimer.get(),
            source->harvestTimer.get(),
            source->guardTimer.get(),
            source->boredTimer.get(),
            source->attackTimer.get(),
            source->wormTrailTimer.get(),
            source->revealTimer.get()
        };
        save.units.push_back(target);
    }

    if (game.m_reinforcements) {
        for (const cReinforcement &source : game.m_reinforcements->reinforcements) {
            save.reinforcements.push_back({
                source.m_delayInSeconds,
                source.m_unitType,
                source.m_playerId,
                source.m_cell,
                source.m_repeat,
                source.m_removeMe,
                source.m_originalDelay
            });
        }
    }

    for (int playerIndex = 0; playerIndex < MAX_PLAYERS; ++playerIndex) {
        const cPlayer *player = game.m_gameObjectsContext->getPlayer(playerIndex);
        const cItemBuilder *builder = player ? player->getItemBuilder() : nullptr;
        if (builder == nullptr) {
            continue;
        }
        for (int slot = 0; slot < MAX_ITEMS; ++slot) {
            cBuildingListItem *item = builder->m_items[slot];
            if (item == nullptr || item->m_myList == nullptr) {
                continue;
            }
            BuildQueueState target;
            target.player = playerIndex;
            target.slot = slot;
            target.timer = builder->m_timers[slot];
            target.listType = eListTypeAsInt(item->getListType());
            target.buildType = static_cast<int>(item->m_type);
            target.buildId = item->m_buildId;
            target.subList = item->m_subList;
            target.progress = item->m_progress;
            target.buildFrame = item->m_buildFrameToDraw;
            target.timesToBuild = item->m_timesToBuild;
            target.timesOrdered = item->m_timesOrdered;
            target.state = static_cast<int>(item->m_state);
            target.placeIt = item->m_placeIt;
            target.deployIt = item->m_deployIt;
            target.waitingForUnitSlot = item->m_waitingForUnitSlot;
            target.progressFrameTimer = item->m_TIMER_progressFrame;
            target.flashingTimer = item->m_TIMER_flashing;
            target.timerCap = item->m_timerCap;
            save.buildQueue.push_back(target);
        }
    }
    return save;
}

bool SaveGameManager::restoreSnapshot(
    cGame &game,
    const save_game_detail::SaveSnapshot &save,
    std::string &error)
{
    game.m_gameSettings->setSkirmish(save.skirmish);
    game.m_dataCampaign->region = save.region;
    game.m_dataCampaign->mission = save.mission;
    game.m_dataCampaign->housePlayer = save.players[HUMAN].house;
    for (int index = 0; index < MAX_PLAYERS; ++index) {
        game.m_gameObjectsContext->getPlayer(index)->setHouse(save.players[index].house);
    }

    game.missionInit();
    game.setupPlayers();
    cMap *map = game.m_gameObjectsContext->getMap();
    map->init(save.mapWidth, save.mapHeight);
    restoreCellState(*map, save);
    for (int cell = 0; cell < map->getMaxCells(); ++cell) {
        for (int layer = 0; layer < MAPID_MAX; ++layer) {
            map->cellResetIdFromLayer(cell, layer);
        }
    }

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        cPlayer &target = *game.m_gameObjectsContext->getPlayer(index);
        const save_game_detail::PlayerState &source = save.players[index];
        target.setHouse(source.house);
        target.iTeam = source.team;
        target.techLevel = source.techLevel;
        target.focusCell_ = source.focusCell;
        target.spiceQuota = source.quota;
        target.selected_structure = -1;
        target.m_autoSlabStructures = source.autoSlab;
        std::copy(source.upgrades.begin(), source.upgrades.end(), target.iStructureUpgradeLevel);
        std::copy(source.appliedUpgrades.begin(), source.appliedUpgrades.end(), target.m_appliedUpgrades);
    }

    std::array<int, MAX_STRUCTURES> structureMapping{};
    structureMapping.fill(-1);
    for (const save_game_detail::StructureState &source : save.structures) {
        if (source.oldId < 0 || source.oldId >= MAX_STRUCTURES ||
            source.player < 0 || source.player >= MAX_PLAYERS ||
            source.cell < 0 || source.cell >= map->getMaxCells()) {
            error = localization::text("Invalid structure in save", "Некорректное здание в сохранении");
            return false;
        }
        const int maximumHp = std::max(1, game.m_infoContext->getStructureInfo(source.type).hp);
        const int hpPercent = std::clamp(source.hitPoints * 100 / maximumHp, 1, 100);
        cAbstractStructure *target = game.m_gameObjectsContext->getPlayer(source.player)->placeStructure(
            source.cell,
            source.type,
            hpPercent
        );
        if (target == nullptr) {
            error = localization::format(
                "Could not restore structure type {} at cell {}",
                "Не удалось восстановить здание типа {} в ячейке {}",
                source.type,
                source.cell
            );
            return false;
        }
        structureMapping[source.oldId] = target->getStructureId();
        target->setHitPoints(source.hitPoints);
        target->setRallyPoint(source.rallyPoint);
        target->setFrame(source.frame);
        target->setBuildingFase(source.buildPhase);
        target->fConcrete = source.concrete;
        target->setAnimating(source.animate);
        target->setRepairing(source.repair);
        target->shouldAnimateWhenUnitHeadsTowardsStructure = source.animateOnApproach;
        target->m_smokeParticlesCreated = source.smoke;
        target->TIMER_repair = source.repairTimer;
        target->TIMER_flag = source.flagTimer;
        target->TIMER_reduceSmoke = source.reduceSmokeTimer;
        target->TIMER_decay = source.decayTimer;
        target->TIMER_prebuild = source.prebuildTimer;
    }

    for (const save_game_detail::UnitState &source : save.units) {
        cUnit &target = *game.m_gameObjectsContext->getUnit(source.oldId);
        target.init(source.oldId);
        target.iType = source.type;
        target.iPlayer = source.player;
        target.setCell(source.cell);
        target.setPosX(source.posX);
        target.setPosY(source.posY);
        target.updateCellXAndY();
        target.iHitPoints = source.hitPoints;
        target.iTempHitPoints = source.tempHitPoints;
        target.fExperience = source.experience;
        for (int group = 0; group < MAX_UNIT_GROUPS; ++group) {
            target.iGroups[group] = (source.groupMask & (1 << group)) != 0;
        }
        target.movement.iNextCell = source.nextCell;
        target.movement.iGoalCell = source.goalCell;
        std::copy(source.path.begin(), source.path.end(), target.movement.iPath);
        target.movement.iPathIndex = source.pathIndex;
        target.movement.iPathFails = source.pathFails;
        target.movement.bCalculateNewPath = source.calculatePath;
        target.bCarryMe = source.carryMe;
        target.iCarryAll = source.carryAll;
        target.combat.iAttackUnit = source.attackUnit;
        target.combat.iAttackStructure = translateStructureId(source.attackStructure, structureMapping);
        target.combat.iAttackCell = source.attackCell;
        target.iUnitID = source.unitId;
        target.iStructureID = translateStructureId(source.structureId, structureMapping);
        target.iCredits = source.credits;
        target.m_transferType = static_cast<eTransferType>(source.transferType);
        target.iBringTarget = source.bringTarget;
        target.iNewUnitType = source.newUnitType;
        target.lastDroppedOffCell = source.lastDroppedOffCell;
        target.rendering.iBodyFacing = static_cast<Facing>(source.bodyFacing);
        target.rendering.iHeadFacing = static_cast<Facing>(source.headFacing);
        target.rendering.iBodyShouldFace = static_cast<Facing>(source.bodyShouldFace);
        target.rendering.iHeadShouldFace = static_cast<Facing>(source.headShouldFace);
        target.rendering.iFrame = source.frame;
        target.m_bSelected = source.selected && source.player == HUMAN;
        target.rendering.bHovered = false;
        target.m_action = static_cast<eActionType>(source.action);
        target.intent = static_cast<eUnitActionIntent>(source.intent);
        target.willBePickedUpBy = source.willBePickedUpBy;
        target.bPickedUp = source.pickedUp;
        target.bRemoveMe = source.removeMe;
        target.mission = source.mission;
        target.isReinforcement = source.reinforcement;
        target.unitsEaten = source.unitsEaten;
        target.iHarvestCellMemory = source.harvestCellMemory;
        target.m_stayAtGoalCell = source.stayAtGoalCell;
        target.boundParticleId = -1;
        target.moveTimer.reset(source.timers[0]);
        target.movewaitTimer.reset(source.timers[1]);
        target.movedelayTimer.reset(source.timers[2]);
        target.turnTimer.reset(source.timers[3]);
        target.thinkwaitTimer.reset(source.timers[4]);
        target.frameTimer.reset(source.timers[5]);
        target.harvestTimer.reset(source.timers[6]);
        target.guardTimer.reset(source.timers[7]);
        target.boredTimer.reset(source.timers[8]);
        target.attackTimer.reset(source.timers[9]);
        target.wormTrailTimer.reset(source.timers[10]);
        target.revealTimer.reset(source.timers[11]);
        target.recreateDimensions();

        if (!target.isHidden()) {
            int layer = MAPID_UNITS;
            if (target.isAirbornUnit()) {
                layer = MAPID_AIR;
            }
            else if (target.isSandworm()) {
                layer = MAPID_WORMS;
            }
            map->cellSetIdForLayer(source.cell, layer, source.oldId);
        }
    }

    for (const save_game_detail::StructureState &source : save.structures) {
        const int newId = structureMapping[source.oldId];
        cAbstractStructure *target = newId >= 0 ? game.m_gameObjectsContext->getStructure(newId) : nullptr;
        if (target == nullptr) {
            continue;
        }
        target->setUnitIdWithin(source.unitWithin);
        target->setUnitIdEntering(source.unitEntering);
        target->setUnitIdHeadingTowards(source.unitHeading);
    }

    for (const save_game_detail::FactoryPadSave &source : save.factoryPads) {
        const int newId = structureMapping[source.structureId];
        auto *factory = newId >= 0 ? dynamic_cast<cUnitFactory *>(game.m_gameObjectsContext->getStructure(newId)) : nullptr;
        if (factory == nullptr) {
            continue;
        }
        factory->restorePad(source.pad);
        if (source.pad.phase == factory_pad::Phase::Rolling) {
            cUnit *rolling = game.m_gameObjectsContext->getUnit(source.pad.rollUnitId);
            rolling->bRollingOffFactoryPad = true;
            rolling->iRollingOffFactoryPadStructureId = newId;
        }
    }

    restoreCellState(*map, save);
    for (const save_game_detail::StructureState &source : save.structures) {
        const int newId = structureMapping[source.oldId];
        cAbstractStructure *target = newId >= 0 ? game.m_gameObjectsContext->getStructure(newId) : nullptr;
        if (target == nullptr) {
            continue;
        }
        for (const int cell : target->getCellsOfStructure()) {
            map->cellSetIdForLayer(cell, MAPID_STRUCTURES, newId);
        }
    }
    for (const save_game_detail::UnitState &source : save.units) {
        cUnit &target = *game.m_gameObjectsContext->getUnit(source.oldId);
        if (target.isHidden()) {
            continue;
        }
        const int layer = target.isAirbornUnit()
            ? MAPID_AIR
            : (target.isSandworm() ? MAPID_WORMS : MAPID_UNITS);
        map->cellSetIdForLayer(source.cell, layer, source.oldId);
    }

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        cPlayer &target = *game.m_gameObjectsContext->getPlayer(index);
        const save_game_detail::PlayerState &source = save.players[index];
        std::copy(source.structures.begin(), source.structures.end(), target.iStructures);
        for (int type = 0; type < MAX_STRUCTURETYPES; ++type) {
            target.iPrimaryBuilding[type] = translateStructureId(source.primary[type], structureMapping);
        }
        target.selected_structure = translateStructureId(source.selectedStructure, structureMapping);
        target.credits = source.credits;
        target.maxCredits_ = source.maxCredits;
        target.powerUsage_ = source.powerUsage;
        target.powerProduce_ = source.powerProduce;
        target.alive = source.alive;
    }

    for (const save_game_detail::FogState &source : save.fog) {
        if (source.hasTerrain) {
            map->m_fogMemory.update(source.cell, true, false, s_RememberedTerrain{
                source.terrainType,
                source.terrainTile,
                source.terrainSmudgeTile,
                source.terrainSmudgeType >= 0
                    ? std::optional<SmudgeType>(static_cast<SmudgeType>(source.terrainSmudgeType))
                    : std::nullopt
            });
        }
        if (source.hasStructure) {
            map->m_fogMemory.updateStructure(source.cell, true, false, s_RememberedStructure{
                source.structureType,
                source.structureOwner,
                source.structureFrame,
                source.structureOffsetX,
                source.structureOffsetY
            });
        }
        if (source.hasUnit) {
            map->m_fogMemory.updateUnit(source.cell, true, false, s_RememberedUnit{
                source.unitType,
                source.unitOwner,
                source.unitBodyIndex,
                source.unitHeadIndex,
                source.unitFrame
            });
        }
    }

    if (game.m_reinforcements) {
        game.m_reinforcements->reinforcements.clear();
        for (const save_game_detail::ReinforcementState &source : save.reinforcements) {
            cReinforcement item;
            item.m_delayInSeconds = source.delay;
            item.m_unitType = source.unitType;
            item.m_playerId = source.player;
            item.m_cell = source.cell;
            item.m_repeat = source.repeat;
            item.m_removeMe = source.remove;
            item.m_originalDelay = source.originalDelay;
            game.m_reinforcements->reinforcements.push_back(item);
        }
    }

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        cItemBuilder *builder = game.m_gameObjectsContext->getPlayer(index)->getItemBuilder();
        if (builder == nullptr) {
            continue;
        }
        std::fill_n(builder->m_items, MAX_ITEMS, nullptr);
        std::fill_n(builder->m_timers, MAX_ITEMS, 0);
    }
    for (const save_game_detail::BuildQueueState &source : save.buildQueue) {
        if (source.player < 0 || source.player >= MAX_PLAYERS ||
            source.slot < 0 || source.slot >= MAX_ITEMS) {
            continue;
        }
        cPlayer *player = game.m_gameObjectsContext->getPlayer(source.player);
        cItemBuilder *builder = player ? player->getItemBuilder() : nullptr;
        cBuildingListItem *item = findBuildItem(game, source);
        if (builder == nullptr || item == nullptr) {
            continue;
        }
        item->m_progress = source.progress;
        item->m_buildFrameToDraw = source.buildFrame;
        item->m_timesToBuild = source.timesToBuild;
        item->m_timesOrdered = source.timesOrdered;
        item->m_state = static_cast<eBuildingListItemState>(source.state);
        item->m_placeIt = source.placeIt;
        item->m_deployIt = source.deployIt;
        item->m_waitingForUnitSlot = source.waitingForUnitSlot;
        item->m_TIMER_progressFrame = source.progressFrameTimer;
        item->m_TIMER_flashing = source.flashingTimer;
        item->m_timerCap = source.timerCap;
        builder->m_items[source.slot] = item;
        builder->m_timers[source.slot] = source.timer;
    }

    map->m_bAutoSpawnSpiceBlooms = save.autoSpawnBlooms;
    map->m_bAutoDetonateSpiceBlooms = save.autoDetonateBlooms;
    map->m_iTIMER_blooms = save.bloomTimer;
    map->m_iDesiredAmountOfWorms = save.desiredWorms;
    map->m_iTIMER_respawnSandworms = save.wormRespawnTimer;
    game.m_gameConditionChecker->setWinFlags(save.winFlags);
    game.m_gameConditionChecker->setLoseFlags(save.loseFlags);

    game.m_gameObjectsContext->getParticles().reset();
    for (cBullet &item : game.m_gameObjectsContext->getBullets()) {
        item.init();
    }
    cPlayer *humanPlayer = game.m_gameObjectsContext->getPlayer(HUMAN);
    game.m_drawManager->setPlayerToDraw(humanPlayer);
    game.setPlayerToInteractFor(humanPlayer);
    const int cameraCell = std::clamp(save.cameraCell, 0, map->getMaxCells() - 1);
    const auto *geometry = map->getGeometry();
    const int viewportX = geometry->getAbsoluteXPositionFromCell(cameraCell) +
        TILESIZE_WIDTH_PIXELS / 2 - game.m_mapCamera->getViewportWidth() / 2;
    const int viewportY = geometry->getAbsoluteYPositionFromCell(cameraCell) +
        TILESIZE_HEIGHT_PIXELS / 2 - game.m_mapCamera->getViewportHeight() / 2;
    game.m_mapCamera->setViewportPosition(viewportX, viewportY);
    if (!game.isState(GAME_PLAYING)) {
        game.playMusicByType(eMusicType::PEACE);
    }
    game.setNextStateToTransitionTo(GAME_PLAYING);
    return true;
}

void SaveGameManager::setSavesDirectory(const std::filesystem::path &directory)
{
    g_savesDirectory = directory;
}

std::filesystem::path SaveGameManager::savesDirectory()
{
    return g_savesDirectory;
}

std::filesystem::path SaveGameManager::quickSavePath()
{
    return slotPath(1);
}

bool SaveGameManager::hasQuickSave()
{
    std::error_code error;
    return std::filesystem::is_regular_file(quickSavePath(), error);
}

std::filesystem::path SaveGameManager::slotPath(int slot)
{
    if (!save_slot::isValidSlot(slot)) {
        return {};
    }
    if (slot == 1) {
        return savesDirectory() / "quicksave.d2s";
    }
    return savesDirectory() / std::format("save{:02}.d2s", slot);
}

SaveSlotInfo SaveGameManager::slotInfo(int slot)
{
    SaveSlotInfo info;
    info.slot = slot;
    if (!save_slot::isValidSlot(slot)) {
        return info;
    }

    const std::filesystem::path path = slotPath(slot);
    std::error_code fileError;
    info.exists = std::filesystem::is_regular_file(path, fileError);
    if (!info.exists || fileError) {
        return info;
    }

    std::ifstream input(path, std::ios::binary);
    if (!input) {
        return info;
    }
    const std::string contents{
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()
    };
    const save_file::DecodeResult decoded = save_file::decode(
        contents,
        FormatVersion,
        save_game_detail::MaximumSaveBytes
    );
    if (!decoded.succeeded()) {
        return info;
    }

    save_game_detail::SaveSnapshot save;
    std::string parseError;
    if (!save_game_detail::deserializeBody(decoded.body, save, parseError)) {
        return info;
    }
    info.valid = true;
    info.name = save_slot::sanitizeName(save.saveName);
    if (info.name.empty()) {
        info.name = slot == 1
            ? localization::text("Quick Save", "Быстрое сохранение")
            : save_slot::defaultName(slot);
    }
    return info;
}

std::vector<SaveSlotInfo> SaveGameManager::listSlots()
{
    std::vector<SaveSlotInfo> result;
    result.reserve(MaximumSlots);
    for (int slot = 1; slot <= MaximumSlots; ++slot) {
        result.push_back(slotInfo(slot));
    }
    return result;
}

bool SaveGameManager::hasAnySave()
{
    for (int slot = 1; slot <= MaximumSlots; ++slot) {
        const SaveSlotInfo info = slotInfo(slot);
        if (info.exists && info.valid) {
            return true;
        }
    }
    return false;
}

bool SaveGameManager::saveQuickGame(cGame &game, std::string &errorMessage)
{
    const SaveSlotInfo info = slotInfo(1);
    const std::string name = info.valid
        ? info.name
        : localization::text("Quick Save", "Быстрое сохранение");
    return saveGame(game, 1, name, errorMessage);
}

bool SaveGameManager::saveGame(
    cGame &game,
    int slot,
    const std::string &name,
    std::string &errorMessage)
{
    errorMessage.clear();
    if (!save_slot::isValidSlot(slot)) {
        errorMessage = localization::text("Invalid save slot number", "Некорректный номер слота");
        return false;
    }
    if (!game.isState(GAME_PLAYING) && !game.isState(GAME_OPTIONS) &&
        game.m_nextState != GAME_PLAYING) {
        errorMessage = localization::text("Saving is only available during a mission", "Сохранять можно только во время миссии");
        return false;
    }
    save_game_detail::SaveSnapshot save = captureSnapshot(game);
    save.saveName = save_slot::sanitizeName(name);
    if (save.saveName.empty()) {
        save.saveName = save_slot::defaultName(slot);
    }
    const std::string body = save_game_detail::serializeBody(save);
    const std::string contents = save_file::encode(body, FormatVersion);
    const std::filesystem::path path = slotPath(slot);
    if (!writeAtomically(path, contents, errorMessage)) {
        return false;
    }
    Logger::info(COMP_GAMERULES, "Save game", "{}", path.string());
    return true;
}

bool SaveGameManager::loadQuickGame(cGame &game, std::string &errorMessage)
{
    return loadGame(game, 1, errorMessage);
}

bool SaveGameManager::loadGame(cGame &game, int slot, std::string &errorMessage)
{
    errorMessage.clear();
    if (!save_slot::isValidSlot(slot)) {
        errorMessage = localization::text("Invalid save slot number", "Некорректный номер слота");
        return false;
    }
    const std::filesystem::path path = slotPath(slot);
    std::ifstream input(path, std::ios::binary);
    if (!input) {
        errorMessage = localization::text("Save file was not found", "Сохранение не найдено");
        return false;
    }
    std::string contents{
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()
    };
    save_file::DecodeResult decoded = save_file::decode(
        contents,
        FormatVersion,
        save_game_detail::MaximumSaveBytes
    );
    if (!decoded.succeeded()) {
        errorMessage = std::move(decoded.error);
        return false;
    }

    save_game_detail::SaveSnapshot save;
    if (!save_game_detail::deserializeBody(decoded.body, save, errorMessage)) {
        return false;
    }
    if (!restoreSnapshot(game, save, errorMessage)) {
        return false;
    }
    Logger::info(COMP_GAMERULES, "Load game", "{}", path.string());
    return true;
}
