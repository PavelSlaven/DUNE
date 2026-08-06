#include "Graphics.hpp"
#include "FactionTint.hpp"
#include "utils/cDataPack.hpp"
#include <algorithm>
#include <cstring>
#include <format>
#include <iostream>

Graphics::Graphics(
    SDL_Renderer *_renderer,
    const std::string &filePackName,
    int assetDensity)
    : renderer(_renderer),
    density(std::max(1, assetDensity))
{
    dataPack = std::make_unique<DataPack>(filePackName);
}

Graphics::~Graphics()
{
    for (auto& [_, texObj] : texCache) {
        delete texObj;
    }
    texCache.clear();
    for (auto& [_, texObj] : houseTexCache) {
        delete texObj;
    }
    houseTexCache.clear();
    for (auto& [_, texObj] : frameTexCache) {
        delete texObj;
    }
    frameTexCache.clear();
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
        return it->second;

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
    SDL_SetTextureScaleMode(
        outTexture,
        density > 1 ? SDL_ScaleModeLinear : SDL_ScaleModeNearest
    );
    Texture *Tex = new Texture(
        outTexture,
        outSurface->w,
        outSurface->h,
        false,
        density
    );
    texCache[index] = Tex;
    return Tex;
}

Texture *Graphics::getTexture(const std::string &name)
{
    int index = dataPack->getIndexFromName(name);
    return this->getTexture(index);
}

Texture *Graphics::findTexture(const std::string &name)
{
    const int index = dataPack->getIndexFromName(name);
    return index >= 0 ? getTexture(index) : nullptr;
}

Texture *Graphics::getFrameTexture(
    int index,
    const cRectangle &logicalFrame)
{
    if (index < 0) {
        return nullptr;
    }
    const std::string cacheKey = std::format(
        "{}:{}:{}:{}:{}",
        index,
        logicalFrame.getX(),
        logicalFrame.getY(),
        logicalFrame.getWidth(),
        logicalFrame.getHeight()
    );
    if (const auto cached = frameTexCache.find(cacheKey);
        cached != frameTexCache.end()) {
        return cached->second;
    }

    SDL_Surface *source = dataPack->getSurface(index);
    if (!source) {
        return nullptr;
    }
    const SDL_Rect sourceRect = {
        logicalFrame.getX() * density,
        logicalFrame.getY() * density,
        logicalFrame.getWidth() * density,
        logicalFrame.getHeight() * density,
    };
    if (sourceRect.x < 0 || sourceRect.y < 0 ||
        sourceRect.x + sourceRect.w > source->w ||
        sourceRect.y + sourceRect.h > source->h) {
        std::cerr << "Graphics: Invalid atlas frame " << cacheKey << '\n';
        return nullptr;
    }

    SDL_Surface *converted =
        SDL_ConvertSurfaceFormat(source, SDL_PIXELFORMAT_RGBA32, 0);
    SDL_Surface *cropped = SDL_CreateRGBSurfaceWithFormat(
        0,
        sourceRect.w,
        sourceRect.h,
        32,
        SDL_PIXELFORMAT_RGBA32
    );
    if (!converted || !cropped) {
        SDL_FreeSurface(converted);
        SDL_FreeSurface(cropped);
        return nullptr;
    }
    SDL_LockSurface(converted);
    SDL_LockSurface(cropped);
    for (int y = 0; y < sourceRect.h; ++y) {
        const auto *sourceRow =
            static_cast<const Uint8 *>(converted->pixels) +
            (sourceRect.y + y) * converted->pitch +
            sourceRect.x * converted->format->BytesPerPixel;
        auto *targetRow =
            static_cast<Uint8 *>(cropped->pixels) + y * cropped->pitch;
        std::memcpy(
            targetRow,
            sourceRow,
            sourceRect.w * converted->format->BytesPerPixel
        );
    }
    SDL_UnlockSurface(cropped);
    SDL_UnlockSurface(converted);
    SDL_FreeSurface(converted);

    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, cropped);
    if (!texture) {
        SDL_FreeSurface(cropped);
        return nullptr;
    }
    SDL_SetTextureScaleMode(
        texture,
        density > 1 ? SDL_ScaleModeLinear : SDL_ScaleModeNearest
    );
    auto *result = new Texture(
        texture,
        cropped->w,
        cropped->h,
        false,
        density
    );
    SDL_FreeSurface(cropped);
    frameTexCache[cacheKey] = result;
    return result;
}

Texture *Graphics::findFrameTexture(
    const std::string &name,
    const cRectangle &logicalFrame)
{
    const int index = dataPack->getIndexFromName(name);
    return index >= 0 ? getFrameTexture(index, logicalFrame) : nullptr;
}

namespace {
std::string houseVariantPrefix(int houseId)
{
    switch (houseId) {
        case 2: return "ATREIDES";
        case 1: return "HARKONNEN";
        case 3: return "ORDOS";
        default: return {};
    }
}

std::string houseVariantCode(int houseId)
{
    switch (houseId) {
        case 2: return "A";
        case 1: return "H";
        case 3: return "O";
        default: return {};
    }
}

Uint32 readPixel(const SDL_Surface *surface, int x, int y)
{
    const auto *row =
        static_cast<const Uint8 *>(surface->pixels) + y * surface->pitch;
    Uint32 pixel = 0;
    std::memcpy(
        &pixel,
        row + x * surface->format->BytesPerPixel,
        surface->format->BytesPerPixel
    );
    return pixel;
}
}

Texture *Graphics::getHouseTexture(
    SDL_Surface *reference,
    int houseId,
    int paletteSwapStart,
    Color houseColor,
    int transparentIndex)
{
    if (!reference) {
        return nullptr;
    }

    const int baseIndex = dataPack->getIndexFromSurface(reference);
    if (baseIndex < 0) {
        std::cerr << "HD world: surface does not belong to active data pack"
                  << std::endl;
        return nullptr;
    }

    const std::string baseName = dataPack->getNameFromIndex(baseIndex);
    const bool neutralHdStructure =
        density > 1 && baseName.starts_with("BUILD_");
    const bool hasEmbeddedHouseDetails =
        density > 1 &&
        (baseName == "BUILD_REFINERY" ||
         baseName == "BUILD_BARRACKS_FLAG" ||
         baseName == "BUILD_WOR_FLAG" ||
         baseName == "BUILD_RADAR_FLAG" ||
         baseName == "BUILD_PALACE_FLAG" ||
         baseName == "BUILD_IX_FLAG" ||
         baseName == "BUILD_LIGHTFACTORY_FLAG" ||
         baseName == "BUILD_HIGHTECH_FLAG" ||
         baseName == "BUILD_REFINERY_FLAG" ||
         baseName == "BUILD_SILO_FLAG" ||
         baseName == "BUILD_STARPORT_FLAG" ||
         baseName == "BUILD_WINDTRAP_FLAG" ||
         baseName == "BUILD_CONSTYARD_FLAG");
    const std::string houseName = houseVariantPrefix(houseId);
    const std::string houseCode = houseVariantCode(houseId);
    const std::string compactVariantName = houseCode.empty()
        ? std::string()
        : "HV_" + houseCode + "_" + baseName;
    const std::string legacyVariantName = houseName.empty()
        ? std::string()
        : "HOUSEVARIANT_" + houseName + "_" + baseName;
    int selectedIndex = neutralHdStructure || compactVariantName.empty()
        ? -1
        : dataPack->getIndexFromName(compactVariantName);
    if (!neutralHdStructure &&
        selectedIndex < 0 &&
        !legacyVariantName.empty()) {
        selectedIndex = dataPack->getIndexFromName(legacyVariantName);
    }
    if (selectedIndex < 0) {
        selectedIndex = baseIndex;
        if (!neutralHdStructure &&
            !legacyVariantName.empty() &&
            !loggedFallbacks[legacyVariantName]) {
            std::clog << "HD world fallback: " << legacyVariantName
                      << " -> " << baseName << std::endl;
            loggedFallbacks[legacyVariantName] = true;
        }
    }

    const std::string selectedName = dataPack->getNameFromIndex(selectedIndex);
    int maskIndex = -1;
    if (!neutralHdStructure || hasEmbeddedHouseDetails) {
        maskIndex = dataPack->getIndexFromName("HM_" + selectedName);
        if (maskIndex < 0) {
            maskIndex =
                dataPack->getIndexFromName("HOUSEMASK_" + selectedName);
        }
        if (maskIndex < 0 && selectedIndex != baseIndex) {
            maskIndex = dataPack->getIndexFromName("HM_" + baseName);
            if (maskIndex < 0) {
                maskIndex =
                    dataPack->getIndexFromName("HOUSEMASK_" + baseName);
            }
        }
    }

    const std::string cacheKey = std::format(
        "{}:{}:{}:{}:{}",
        baseIndex,
        selectedIndex,
        maskIndex,
        houseId,
        density
    );
    const auto cached = houseTexCache.find(cacheKey);
    if (cached != houseTexCache.end()) {
        return cached->second;
    }

    SDL_Surface *selected = dataPack->getSurface(selectedIndex);
    if (!selected) {
        return nullptr;
    }

    SDL_Surface *prepared = nullptr;
    if (selected->format->palette) {
        SDL_Surface *indexed = SDL_CreateRGBSurfaceWithFormat(
            0,
            selected->w,
            selected->h,
            8,
            SDL_PIXELFORMAT_INDEX8
        );
        if (!indexed) {
            return nullptr;
        }
        SDL_LockSurface(selected);
        SDL_LockSurface(indexed);
        for (int y = 0; y < selected->h; ++y) {
            std::memcpy(
                static_cast<Uint8 *>(indexed->pixels) + y * indexed->pitch,
                static_cast<const Uint8 *>(selected->pixels) + y * selected->pitch,
                std::min(indexed->pitch, selected->pitch)
            );
        }
        SDL_UnlockSurface(indexed);
        SDL_UnlockSurface(selected);
        SDL_SetPaletteColors(
            indexed->format->palette,
            selected->format->palette->colors,
            0,
            selected->format->palette->ncolors
        );
        if (paletteSwapStart >= 0 &&
            paletteSwapStart + 7 <= indexed->format->palette->ncolors &&
            indexed->format->palette->ncolors >= 151) {
            SDL_Color replacement[7];
            for (int i = 0; i < 7; ++i) {
                replacement[i] =
                    indexed->format->palette->colors[paletteSwapStart + i];
            }
            SDL_SetPaletteColors(indexed->format->palette, replacement, 144, 7);
        }
        SDL_SetColorKey(indexed, SDL_TRUE, transparentIndex);
        prepared =
            SDL_ConvertSurfaceFormat(indexed, SDL_PIXELFORMAT_RGBA32, 0);
        SDL_FreeSurface(indexed);
    }
    else {
        prepared =
            SDL_ConvertSurfaceFormat(selected, SDL_PIXELFORMAT_RGBA32, 0);
    }
    if (!prepared) {
        return nullptr;
    }

    SDL_Surface *mask =
        maskIndex >= 0 ? dataPack->getSurface(maskIndex) : nullptr;
    if (mask && mask->w == prepared->w && mask->h == prepared->h) {
        SDL_LockSurface(prepared);
        SDL_LockSurface(mask);
        float maskedLuminanceSum = 0.0F;
        int maskedLuminancePixels = 0;
        for (int y = 0; y < prepared->h; ++y) {
            auto *row = reinterpret_cast<Uint32 *>(
                static_cast<Uint8 *>(prepared->pixels) + y * prepared->pitch
            );
            for (int x = 0; x < prepared->w; ++x) {
                Uint8 r, g, b, a;
                SDL_GetRGBA(row[x], prepared->format, &r, &g, &b, &a);
                Uint8 mr, mg, mb, ma;
                SDL_GetRGBA(
                    readPixel(mask, x, y),
                    mask->format,
                    &mr,
                    &mg,
                    &mb,
                    &ma
                );
                const float strength =
                    (static_cast<float>(ma) / 255.0F) *
                    (static_cast<float>(std::max({mr, mg, mb})) / 255.0F);
                if (strength >= 0.99F && a != 0) {
                    maskedLuminanceSum +=
                        (0.299F * r + 0.587F * g + 0.114F * b) / 128.0F;
                    ++maskedLuminancePixels;
                }
            }
        }
        const float averageMaskedLuminance = maskedLuminancePixels > 0
            ? maskedLuminanceSum / maskedLuminancePixels
            : FactionTintReferenceLuminance;
        for (int y = 0; y < prepared->h; ++y) {
            auto *row = reinterpret_cast<Uint32 *>(
                static_cast<Uint8 *>(prepared->pixels) + y * prepared->pitch
            );
            for (int x = 0; x < prepared->w; ++x) {
                Uint8 r, g, b, a;
                SDL_GetRGBA(row[x], prepared->format, &r, &g, &b, &a);
                Uint8 mr, mg, mb, ma;
                SDL_GetRGBA(
                    readPixel(mask, x, y),
                    mask->format,
                    &mr,
                    &mg,
                    &mb,
                    &ma
                );
                const float strength =
                    (static_cast<float>(ma) / 255.0F) *
                    (static_cast<float>(std::max({mr, mg, mb})) / 255.0F);
                if (strength <= 0.0F || a == 0) {
                    continue;
                }
                const float luminance =
                    (0.299F * r + 0.587F * g + 0.114F * b) / 128.0F;
                const auto tint =
                    [strength, luminance, averageMaskedLuminance](Uint8 original, Uint8 target) {
                        const float colored = applyFactionTintChannel(
                            target,
                            luminance,
                            averageMaskedLuminance
                        );
                        return static_cast<Uint8>(std::clamp(
                            original * (1.0F - strength) +
                                colored * strength,
                            0.0F,
                            255.0F
                        ));
                    };
                row[x] = SDL_MapRGBA(
                    prepared->format,
                    tint(r, houseColor.r),
                    tint(g, houseColor.g),
                    tint(b, houseColor.b),
                    a
                );
            }
        }
        SDL_UnlockSurface(mask);
        SDL_UnlockSurface(prepared);
    }

    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, prepared);
    if (!texture) {
        SDL_FreeSurface(prepared);
        return nullptr;
    }
    SDL_SetTextureScaleMode(
        texture,
        density > 1 ? SDL_ScaleModeLinear : SDL_ScaleModeNearest
    );
    auto *result =
        new Texture(texture, prepared->w, prepared->h, false, density);
    SDL_FreeSurface(prepared);
    houseTexCache[cacheKey] = result;
    return result;
}

int Graphics::getNumberOfFiles()
{
    return dataPack->getNumberOfFile();
}

bool Graphics::isValid() const
{
    return dataPack && dataPack->isValid();
}

int Graphics::getLogicalWidth(int index) const
{
    SDL_Surface *surface = getSurface(index);
    return surface ? surface->w / density : 0;
}

int Graphics::getLogicalHeight(int index) const
{
    SDL_Surface *surface = getSurface(index);
    return surface ? surface->h / density : 0;
}
