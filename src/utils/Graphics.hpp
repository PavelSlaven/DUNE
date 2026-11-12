/**
 * @file Graphics.hpp
 *
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 *
 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
 *
 * This is a non-commercial educational project.
 */

#pragma once

#include <SDL3/SDL.h>
#include <algorithm>
#include <cmath>
#include "utils/Color.hpp"
#include <string>
#include <memory>
#include <map>
#include <unordered_map>
#include <utility>
#include <vector>

class Texture;

class DataPack;

/*
 * This class provides the Images of its internal container.
 * It only returns the Surfaces of the container.
 * It returns the Textures of the container. It manages its creation and destruction via a cache to avoid rebuilding the texture.
 */
class Graphics {
public:
    explicit Graphics(SDL_Renderer *_renderer, const std::string &filePackName, int assetDensity = 1);
    ~Graphics();
    // return a surface from his index
    SDL_Surface *getSurface(int index) const;
    // return a surface from his name
    SDL_Surface *getSurface(const std::string &name) const;
    // return a texture from his index
    Texture *getTexture(int index);
    // return a texture from his name
    Texture *getTexture(const std::string &name);
    Texture *createHouseTexture(SDL_Surface *reference, const Color &houseColor);
    Texture *getHouseTexture(const std::string &name, int houseId, const Color &houseColor);
    // return number of file in Pack
    int getNumberOfFiles();
    int getDensity() const {
        return std::max(1, assetDensity);
    }
    // name of every file in the pack, in index order
    std::vector<std::string> getNames() const;
private:
    SDL_Renderer *renderer;
    int assetDensity;
    std::unique_ptr<DataPack> dataPack;
    std::unordered_map<int, std::unique_ptr<Texture>> texCache;
    std::map<std::pair<int, int>, std::unique_ptr<Texture>> houseTexCache;
};

inline constexpr int kHd4AssetDensity = 4;

inline std::string hd4SceneFile(const std::string &scene)
{
    return "data/scenes/hd4/sdl_" + scene + ".dat";
}

inline int scaleToBitmap(int logical, int logicalExtent, int bitmapExtent)
{
    return static_cast<int>(std::round(logical * static_cast<double>(bitmapExtent) / logicalExtent));
}

inline int calculateFrameDensity(float presentationWidth, float presentationHeight, int logicalWidth, int logicalHeight)
{
    if (logicalWidth <= 0 || logicalHeight <= 0) {
        return 1;
    }

    const float scale = std::min(presentationWidth / logicalWidth, presentationHeight / logicalHeight);
    return std::clamp(static_cast<int>(std::ceil(scale - 0.01f)), 1, kHd4AssetDensity);
}
