#include "UnitFrameFixture.hpp"

#include "context/GameContext.hpp"
#include "data/gfxdata.h"
#include "d2tmc.h"
#include "gameobjects/particles/cParticle.h"
#include "gameobjects/projectiles/bullet.h"
#include "gamestates/cSelectYourNextConquestState.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"
#include "utils/cIniGameRessouces.h"
#include "utils/cPack.h"
#include "utils/cStructureUtils.h"

#include <SDL2/SDL_image.h>
#include <algorithm>
#include <array>
#include <filesystem>
#include <format>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

cGame game;
cStructureUtils structureUtils;
cMap global_map;
cAbstractStructure *structure[MAX_STRUCTURES]{};
cUnit unit[MAX_UNITS];
cPlayer players[MAX_PLAYERS];
cParticle particle[MAX_PARTICLES];
cBullet bullet[MAX_BULLETS];
cRegion world[MAX_REGIONS];
cDrawManager *drawManager = nullptr;
SDLDrawer *renderDrawer = nullptr;
cMapCamera *mapCamera = nullptr;
s_StructureInfo sStructureInfo[MAX_STRUCTURETYPES];
s_UnitInfo sUnitInfo[MAX_UNITTYPES];
s_UpgradeInfo sUpgradeInfo[MAX_UPGRADETYPES];
s_SpecialInfo sSpecialInfo[MAX_SPECIALTYPES];
s_BulletInfo sBulletInfo[MAX_BULLET_TYPES];
s_ParticleInfo sParticleInfo[MAX_PARTICLE_TYPES];
std::shared_ptr<Graphics> gfxdata;

namespace {
constexpr int kAtlasWidth = 1408;
constexpr int kAtlasHeight = 176;
constexpr int kPlaceholderCount = 256;

SDL_Surface *makeSurface(int width, int height, Uint8 red, Uint8 green, Uint8 blue, Uint8 alpha)
{
    SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(
        0, width, height, 32, SDL_PIXELFORMAT_RGBA32
    );
    if (!surface) {
        throw std::runtime_error(std::format("SDL_CreateRGBSurfaceWithFormat: {}", SDL_GetError()));
    }
    const Uint32 color = SDL_MapRGBA(surface->format, red, green, blue, alpha);
    if (SDL_FillRect(surface, nullptr, color) != 0) {
        SDL_FreeSurface(surface);
        throw std::runtime_error(std::format("SDL_FillRect: {}", SDL_GetError()));
    }
    return surface;
}

void savePng(SDL_Surface *surface, const std::filesystem::path &path)
{
    if (IMG_SavePNG(surface, path.string().c_str()) != 0) {
        const std::string error = IMG_GetError();
        SDL_FreeSurface(surface);
        throw std::runtime_error(std::format("IMG_SavePNG: {}", error));
    }
    SDL_FreeSurface(surface);
}

void saveAtlas(const std::filesystem::path &path, bool mask)
{
    SDL_Surface *surface = makeSurface(
        kAtlasWidth,
        kAtlasHeight,
        0,
        0,
        0,
        mask ? 0 : 255
    );
    if (!mask) {
        for (int column = 0; column < 8; ++column) {
            SDL_Rect frame{column * 176, 0, 176, 176};
            const Uint32 color = column == 0
                ? SDL_MapRGBA(surface->format, 255, 255, 255, 255)
                : SDL_MapRGBA(surface->format, 20, 230, 40, 255);
            SDL_FillRect(surface, &frame, color);
        }
        const Uint32 top = SDL_MapRGBA(surface->format, 255, 0, 0, 255);
        const Uint32 bottom = SDL_MapRGBA(surface->format, 0, 0, 255, 255);
        const Uint32 left = SDL_MapRGBA(surface->format, 255, 255, 0, 255);
        const Uint32 right = SDL_MapRGBA(surface->format, 0, 255, 255, 255);
        SDL_Rect topEdge{0, 0, 176, 12};
        SDL_Rect bottomEdge{0, 164, 176, 12};
        SDL_Rect leftEdge{0, 0, 12, 176};
        SDL_Rect rightEdge{164, 0, 12, 176};
        SDL_FillRect(surface, &topEdge, top);
        SDL_FillRect(surface, &bottomEdge, bottom);
        SDL_FillRect(surface, &leftEdge, left);
        SDL_FillRect(surface, &rightEdge, right);
    }
    else {
        const SDL_Rect markerRect{24, 24, 16, 16};
        const Uint32 marker = SDL_MapRGBA(surface->format, 255, 255, 255, 255);
        SDL_FillRect(surface, &markerRect, marker);
    }
    savePng(surface, path);
}

void addFileOrThrow(WriterPack &pack, const std::filesystem::path &file, const std::string &name)
{
    if (!pack.addFile(file.string(), name)) {
        throw std::runtime_error(std::format("WriterPack rejected {}", name));
    }
}
}

UnitFrameFixture::UnitFrameFixture(int density, int worldScalePercent)
    : density_(density), worldScalePercent_(worldScalePercent)
{
    if (SDL_WasInit(SDL_INIT_VIDEO) == 0) {
        if (SDL_Init(SDL_INIT_VIDEO) != 0) {
            throw std::runtime_error(std::format("SDL_Init(SDL_INIT_VIDEO): {}", SDL_GetError()));
        }
        ownsVideoSubsystem_ = true;
    }
    if ((IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG) == 0) {
        throw std::runtime_error(std::format("IMG_Init(IMG_INIT_PNG): {}", IMG_GetError()));
    }
    ownsImageSubsystem_ = true;

    window_ = SDL_CreateWindow(
        "U9-T1 frame fixture",
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        800,
        600,
        SDL_WINDOW_HIDDEN
    );
    if (!window_) {
        throw std::runtime_error(std::format("SDL_CreateWindow: {}", SDL_GetError()));
    }
    renderer_ = SDL_CreateRenderer(window_, -1, SDL_RENDERER_SOFTWARE);
    if (!renderer_) {
        throw std::runtime_error(std::format("SDL_CreateRenderer: {}", SDL_GetError()));
    }

    createSyntheticPack();
    gfxdata = std::make_shared<Graphics>(renderer_, packPath_, density_);
    if (!gfxdata->isValid()) {
        throw std::runtime_error("The synthetic unit frame pack did not load");
    }

    game.m_screenW = 800;
    game.m_screenH = 600;
    game.m_graphicsDensity = density_;
    game.m_effectiveWorldScalePercent = worldScalePercent_;
    game.m_drawUnitDebug = false;
    game.m_mapViewport = nullptr;

    IniGameRessources::install_units();

    players[HUMAN].id = HUMAN;
    players[HUMAN].house = ATREIDES;
    players[HUMAN].m_Human = true;
    global_map.init(64, 64);
    mapCamera = new cMapCamera(&global_map, 0.0F, 0.0F, false);
    mapCamera->m_viewportStartX = 0.0F;
    mapCamera->m_viewportStartY = 0.0F;
    mapCamera->m_heightOfTopBar = 40;
    mapCamera->m_zoomLevel = 1.0F;

    renderDrawer = new SDLDrawer(renderer_);
    initializeGameData();
}

UnitFrameFixture::~UnitFrameFixture()
{
    if (players[HUMAN].gameControlsContext) {
        delete players[HUMAN].gameControlsContext;
        players[HUMAN].gameControlsContext = nullptr;
    }
    std::fill(std::begin(players[HUMAN].bmp_unit), std::end(players[HUMAN].bmp_unit), nullptr);
    std::fill(std::begin(players[HUMAN].bmp_unit_top), std::end(players[HUMAN].bmp_unit_top), nullptr);
    delete renderDrawer;
    renderDrawer = nullptr;
    delete mapCamera;
    mapCamera = nullptr;
    gfxdata.reset();
    if (renderer_) {
        SDL_DestroyRenderer(renderer_);
        renderer_ = nullptr;
    }
    if (window_) {
        SDL_DestroyWindow(window_);
        window_ = nullptr;
    }
    std::error_code error;
    if (!packPath_.empty()) {
        std::filesystem::remove(packPath_, error);
    }
    if (ownsImageSubsystem_) {
        IMG_Quit();
    }
    if (ownsVideoSubsystem_) {
        SDL_QuitSubSystem(SDL_INIT_VIDEO);
    }
}

void UnitFrameFixture::createSyntheticPack()
{
    const std::filesystem::path root = D2TM_UNIT_FRAME_FIXTURE_ROOT;
    std::filesystem::create_directories(root);
    const std::string suffix = std::to_string(SDL_GetTicks());
    const auto placeholderPath = root / ("placeholder-" + suffix + ".png");
    const auto atlasPath = root / ("siege-atlas-" + suffix + ".png");
    const auto shadowPath = root / ("siege-shadow-" + suffix + ".png");
    const auto topPath = root / ("siege-top-" + suffix + ".png");
    const auto tankPath = root / ("tank-hd-" + suffix + ".png");
    const auto tankShadowPath = root / ("tank-hd-shadow-" + suffix + ".png");
    const auto harvesterPath = root / ("harvester-hd-" + suffix + ".png");
    const auto harvesterShadowPath = root / ("harvester-hd-shadow-" + suffix + ".png");
    const auto bodyMaskPath = root / ("siege-mask-" + suffix + ".png");
    const auto topMaskPath = root / ("siege-top-mask-" + suffix + ".png");
    const auto packPath = root / ("unit-frame-" + suffix + ".dat");

    savePng(makeSurface(8, 8, 100, 120, 140, 255), placeholderPath);
    saveAtlas(atlasPath, false);
    saveAtlas(shadowPath, true);
    saveAtlas(topPath, false);
    savePng(makeSurface(8 * 160, 160, 100, 120, 140, 255), tankPath);
    savePng(makeSurface(8 * 160, 160, 0, 0, 0, 0), tankShadowPath);
    savePng(makeSurface(8 * 352, 5 * 224, 100, 120, 140, 255), harvesterPath);
    savePng(makeSurface(8 * 352, 5 * 224, 0, 0, 0, 0), harvesterShadowPath);
    saveAtlas(bodyMaskPath, true);
    saveAtlas(topMaskPath, true);

    WriterPack pack(packPath.string());
    for (int index = 0; index < kPlaceholderCount; ++index) {
        const std::string name = index == UNIT_SIEGEBASE
            ? "UNIT_SIEGEBASE"
            : index == UNIT_SIEGEBASE_SHADOW
                ? "UNIT_SIEGEBASE_SHADOW"
                : index == UNIT_SIEGETOP
                    ? "UNIT_SIEGETOP"
                    : std::format("FIXTURE_{}", index);
        const auto &file = index == UNIT_SIEGEBASE
            ? atlasPath
            : index == UNIT_SIEGEBASE_SHADOW
                ? shadowPath
                : index == UNIT_SIEGETOP
                    ? topPath
                    : index == UNIT_TANKBASE
                        ? tankPath
                        : index == UNIT_TANKBASE_SHADOW
                            ? tankShadowPath
                            : index == UNIT_TANKTOP
                                ? tankPath
                                : index == UNIT_HARVESTER
                                    ? harvesterPath
                                    : index == UNIT_HARVESTER_SHADOW
                                        ? harvesterShadowPath
                    : placeholderPath;
        addFileOrThrow(pack, file, name);
    }
    addFileOrThrow(pack, bodyMaskPath, "HM_UNIT_SIEGEBASE");
    addFileOrThrow(pack, topMaskPath, "HM_UNIT_SIEGETOP");
    std::ostringstream writerOutput;
    std::streambuf *originalOutput = std::cout.rdbuf(writerOutput.rdbuf());
    const bool packWritten = pack.writePackFilesOnDisk();
    std::cout.rdbuf(originalOutput);
    if (!packWritten) {
        throw std::runtime_error("WriterPack failed to write the synthetic data pack");
    }
    packPath_ = packPath.string();

    std::error_code error;
    for (const auto &file : {placeholderPath, atlasPath, shadowPath, topPath, tankPath,
                             tankShadowPath, harvesterPath, harvesterShadowPath,
                             bodyMaskPath, topMaskPath}) {
        std::filesystem::remove(file, error);
    }
}

void UnitFrameFixture::initializeGameData()
{
    const Color houseColor{240, 24, 32, 255};
    std::ostringstream fallbackOutput;
    std::streambuf *originalLog = std::clog.rdbuf(fallbackOutput.rdbuf());
    for (int type = 0; type < MAX_UNITTYPES; ++type) {
        if (sUnitInfo[type].bmp) {
            players[HUMAN].bmp_unit[type] = gfxdata->getHouseTexture(
                sUnitInfo[type].bmp,
                ATREIDES,
                -1,
                houseColor,
                TransparentColorIndex
            );
        }
        if (sUnitInfo[type].top) {
            players[HUMAN].bmp_unit_top[type] = gfxdata->getHouseTexture(
                sUnitInfo[type].top,
                ATREIDES,
                -1,
                houseColor,
                TransparentColorIndex
            );
        }
    }
    std::clog.rdbuf(originalLog);
}

void UnitFrameFixture::setCamera(float zoom, float viewportX, float viewportY)
{
    mapCamera->m_zoomLevel = zoom;
    mapCamera->m_viewportStartX = viewportX;
    mapCamera->m_viewportStartY = viewportY;
}

void UnitFrameFixture::setDisplaySettings(int density, int worldScalePercent)
{
    const int normalizedDensity = std::max(1, density);
    game.m_graphicsDensity = normalizedDensity;
    game.m_effectiveWorldScalePercent = worldScalePercent;
    gfxdata->density = normalizedDensity;
    const auto updateTextureDensity = [normalizedDensity](auto &cache) {
        for (auto &[_, texture] : cache) {
            if (!texture) continue;
            texture->density = normalizedDensity;
            texture->w = texture->pixelW / normalizedDensity;
            texture->h = texture->pixelH / normalizedDensity;
        }
    };
    updateTextureDensity(gfxdata->texCache);
    updateTextureDensity(gfxdata->houseTexCache);
    updateTextureDensity(gfxdata->frameTexCache);
}

void UnitFrameFixture::setUnit(
    int index,
    int type,
    int posX,
    int posY,
    int bodyFacing,
    int headFacing,
    int animationFrame)
{
    unit[index].init(index);
    unit[index].iType = type;
    unit[index].iPlayer = HUMAN;
    unit[index].iCellX = posX / 32;
    unit[index].iCellY = posY / 32;
    unit[index].iCell = unit[index].iCellY * 64 + unit[index].iCellX;
    unit[index].posX = static_cast<float>(posX);
    unit[index].posY = static_cast<float>(posY);
    unit[index].iHitPoints = std::max(1, sUnitInfo[type].hp / 2);
    unit[index].iTempHitPoints = -1;
    unit[index].iBodyFacing = bodyFacing;
    unit[index].iHeadFacing = headFacing;
    unit[index].iFrame = animationFrame;
    global_map.cellSetIdForLayer(unit[index].iCell, MAPID_UNITS, index);
    global_map.setVisibleFor(unit[index].iCell, HUMAN);
}

void UnitFrameFixture::setUnitTextures(int type, Texture *shadow)
{
    sUnitInfo[type].shadow = shadow;
}

void UnitFrameFixture::setTurretTexture(int type, Texture *texture)
{
    players[HUMAN].bmp_unit_top[type] = texture;
}

void UnitFrameFixture::setUnitFlags(int index, bool selected, bool carryMe)
{
    unit[index].bSelected = selected;
    unit[index].bCarryMe = carryMe;
}

Texture *UnitFrameFixture::bodyTexture(int type) const
{
    return players[HUMAN].bmp_unit[type];
}

Texture *UnitFrameFixture::turretTexture(int type) const
{
    return players[HUMAN].bmp_unit_top[type];
}

Texture *UnitFrameFixture::shadowTexture(int type) const
{
    return sUnitInfo[type].shadow;
}

SDL_Surface *UnitFrameFixture::siegeSurface() const
{
    return sUnitInfo[SIEGETANK].bmp;
}

Texture *UnitFrameFixture::siegeHouseTexture() const
{
    return players[HUMAN].bmp_unit[SIEGETANK];
}
