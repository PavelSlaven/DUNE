#include "utils/HdUiTextureLoader.hpp"

#include "include/Texture.hpp"
#include "utils/Graphics.hpp"
#include "utils/Log.h"

#include <SDL3_image/SDL_image.h>

#include <filesystem>

Texture *loadHdUiTexture(SDL_Renderer *renderer, const std::string &fileName, const std::string &logContext)
{
    const std::filesystem::path path = std::filesystem::path("data") / "hd4" / fileName;
    if (renderer != nullptr && std::filesystem::exists(path)) {
        SDL_Surface *surface = IMG_Load(path.string().c_str());
        if (surface != nullptr) {
            SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, surface);
            if (texture != nullptr) {
                SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND);
                SDL_SetTextureScaleMode(texture, SDL_SCALEMODE_LINEAR);
                Texture *result = new Texture(texture, surface->w, surface->h, false, kHd4AssetDensity);
                SDL_DestroySurface(surface);
                return result;
            }
            SDL_DestroySurface(surface);
        }
    }

    Logger::warn(COMP_INIT, logContext, "Unable to load adaptive UI texture: {}", fileName);
    return nullptr;
}
