#pragma once

#include <SDL2/SDL.h>
#include <string>
#include <memory>
#include <unordered_map>

#include "include/Texture.hpp"
#include "utils/Color.hpp"
#include "utils/cRectangle.h"

class DataPack;

/*
 * This class provides the Images of its internal container.
 * It only returns the Surfaces of the container.
 * It returns the Textures of the container. It manages its creation and destruction via a cache to avoid rebuilding the texture.
 */
class Graphics {
public:
    explicit Graphics(
        SDL_Renderer *_renderer,
        const std::string &filePackName,
        int assetDensity = 1
    );
    ~Graphics();
    // return a surface from his index
    SDL_Surface *getSurface(int index) const;
    // return a surface from his name
    SDL_Surface *getSurface(const std::string &name) const;
    // return a texture from his index
    Texture *getTexture(int index);
    // return a texture from his name
    Texture *getTexture(const std::string &name);
    // return a named texture, or nullptr without logging when it is absent
    Texture *findTexture(const std::string &name);
    // Return an isolated atlas frame so linear filtering cannot sample a
    // neighbouring frame.
    Texture *getFrameTexture(int index, const cRectangle &logicalFrame);
    Texture *findFrameTexture(
        const std::string &name,
        const cRectangle &logicalFrame
    );
    Texture *getHouseTexture(
        SDL_Surface *reference,
        int houseId,
        int paletteSwapStart,
        Color houseColor,
        int transparentIndex
    );
    // return number of file in Pack
    int getNumberOfFiles();
    [[nodiscard]] bool isValid() const;
    [[nodiscard]] int getDensity() const {
        return density;
    }
    [[nodiscard]] int getLogicalWidth(int index) const;
    [[nodiscard]] int getLogicalHeight(int index) const;
private:
    SDL_Renderer *renderer;
    int density;
    std::unique_ptr<DataPack> dataPack;
    std::unordered_map<int, Texture *> texCache;
    std::unordered_map<std::string, Texture *> frameTexCache;
    std::unordered_map<std::string, Texture *> houseTexCache;
    std::unordered_map<std::string, bool> loggedFallbacks;
};
