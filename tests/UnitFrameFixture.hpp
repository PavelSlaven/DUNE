#pragma once

#include "drawers/SDLDrawer.hpp"
#include "gameobjects/units/cUnit.h"
#include "include/Texture.hpp"
#include "utils/Graphics.hpp"

#include <memory>
#include <string>

class UnitFrameFixture {
public:
    explicit UnitFrameFixture(int density = 4, int worldScalePercent = 100);
    ~UnitFrameFixture();

    UnitFrameFixture(const UnitFrameFixture &) = delete;
    UnitFrameFixture &operator=(const UnitFrameFixture &) = delete;

    void setCamera(float zoom, float viewportX = 0.0F, float viewportY = 0.0F);
    void setDisplaySettings(int density, int worldScalePercent);
    void setUnit(
        int index,
        int type,
        int posX = 256,
        int posY = 256,
        int bodyFacing = 0,
        int headFacing = 0,
        int animationFrame = 0);
    void setUnitTextures(int type, Texture *shadow = nullptr);
    void setTurretTexture(int type, Texture *texture);
    void setUnitFlags(int index, bool selected, bool carryMe);

    SDL_Renderer *renderer() const { return renderer_; }
    SDL_Window *window() const { return window_; }
    Texture *bodyTexture(int type) const;
    Texture *turretTexture(int type) const;
    Texture *shadowTexture(int type) const;
    SDL_Surface *siegeSurface() const;
    Texture *siegeHouseTexture() const;
    const std::string &packPath() const { return packPath_; }

private:
    void createSyntheticPack();
    void initializeGameData();

    int density_;
    int worldScalePercent_;
    SDL_Window *window_ = nullptr;
    SDL_Renderer *renderer_ = nullptr;
    std::string packPath_;
    bool ownsVideoSubsystem_ = false;
    bool ownsImageSubsystem_ = false;
};
