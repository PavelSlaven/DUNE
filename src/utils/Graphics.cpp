/**
 * @file Graphics.cpp
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

#include "Graphics.hpp"
#include "utils/cDataPack.hpp"
#include "utils/HouseMaskTint.hpp"
#include "include/Texture.hpp"
#include <iostream>
#include "include/cAssert.h"

Graphics::Graphics(SDL_Renderer *_renderer,const std::string &filePackName, int assetDensity)
    : renderer(_renderer), assetDensity(assetDensity)
{
    d2tm_assert(_renderer != nullptr);
    dataPack = std::make_unique<DataPack>(filePackName, nullptr);
}

Graphics::~Graphics()
{
    // Smart pointers handle automatic cleanup
}

SDL_Surface *Graphics::getSurface(int index) const
{
    return dataPack->getSurface(index);
}

SDL_Surface *Graphics::getSurface(const std::string &name) const
{
    return dataPack->getSurface(name);
}

Texture *Graphics::getTexture(int index)
{
    if (index < 0) {
        std::cerr << "Graphics: Invalid index " << index << std::endl;
        return nullptr;
    }
    auto it = texCache.find(index);
    if (it != texCache.end())
        return it->second.get();

    SDL_Surface *outSurface = dataPack->getSurface(index);
    if (!outSurface) {
        std::cerr << "Graphics: Failed to load image " << index << " : " <<SDL_GetError() << std::endl;
        return nullptr;
    }
    SDL_Texture *outTexture = SDL_CreateTextureFromSurface(renderer, outSurface);
    if (!outTexture) {
        std::cerr << "Graphics: Failed to convert texture " << index << " : " <<SDL_GetError() << std::endl;
        return nullptr;
    }
    SDL_SetTextureScaleMode(outTexture, getDensity() > 1 ? SDL_SCALEMODE_LINEAR : SDL_SCALEMODE_NEAREST);
    texCache.emplace(index, std::make_unique<Texture>(outTexture, outSurface->w, outSurface->h, false, getDensity()));
    return texCache[index].get();
}

Texture *Graphics::getTexture(const std::string &name)
{
    int index = dataPack->getIndexFromName(name);
    return this->getTexture(index);
}

Texture *Graphics::createHouseTexture(SDL_Surface *reference, const Color &houseColor)
{
    const int index = dataPack->getIndexFromSurface(reference);
    if (index < 0) {
        return nullptr;
    }

    const int maskIndex = dataPack->getIndexFromName("HM_" + dataPack->getNameFromIndex(index));
    if (maskIndex < 0) {
        return nullptr;
    }

    SDL_Surface *copy = SDL_ConvertSurface(reference, SDL_PIXELFORMAT_RGBA32);
    if (!copy) {
        return nullptr;
    }

    if (!applyHouseMaskTint(copy, dataPack->getSurface(maskIndex), houseColor)) {
        SDL_DestroySurface(copy);
        return nullptr;
    }

    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, copy);
    const int width = copy->w;
    const int height = copy->h;
    SDL_DestroySurface(copy);
    if (!texture) {
        return nullptr;
    }

    SDL_SetTextureScaleMode(texture, getDensity() > 1 ? SDL_SCALEMODE_LINEAR : SDL_SCALEMODE_NEAREST);
    return new Texture(texture, width, height, false, getDensity());
}

Texture *Graphics::getHouseTexture(const std::string &name, int houseId, const Color &houseColor)
{
    const int index = dataPack->getIndexFromName(name);
    if (index < 0) {
        return nullptr;
    }

    const auto key = std::make_pair(index, houseId);
    const auto cached = houseTexCache.find(key);
    if (cached != houseTexCache.end()) {
        return cached->second.get();
    }

    std::unique_ptr<Texture> texture(createHouseTexture(dataPack->getSurface(index), houseColor));
    if (texture) {
        Texture *result = texture.get();
        houseTexCache.emplace(key, std::move(texture));
        return result;
    }
    return getTexture(index);
}

int Graphics::getNumberOfFiles()
{
    return dataPack->getNumberOfFile();
}

std::vector<std::string> Graphics::getNames() const
{
    return dataPack->getNames();
}
