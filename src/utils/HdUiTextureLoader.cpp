#include "utils/HdUiTextureLoader.hpp"

#include "d2tmc.h"
#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"
#include "utils/cLog.h"

#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

#include <array>
#include <filesystem>
#include <format>

Texture *loadHdUiTexture(
    const std::string &fileName,
    int preferredDensity,
    const std::string &logContext)
{
    const std::array<int, 2> candidates{
        preferredDensity,
        preferredDensity == 4 ? 2 : 4
    };

    for (const int density : candidates) {
        const std::filesystem::path path =
            std::filesystem::path("data") /
            std::format("hd{}", density) /
            fileName;
        if (!std::filesystem::exists(path)) {
            continue;
        }

        SDL_Surface *surface = IMG_Load(path.string().c_str());
        if (!surface) {
            continue;
        }
        SDL_Texture *texture = SDL_CreateTextureFromSurface(
            renderDrawer->getRenderer(),
            surface
        );
        if (!texture) {
            SDL_FreeSurface(surface);
            continue;
        }

        SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND);
        SDL_SetTextureScaleMode(texture, SDL_ScaleModeLinear);
        Texture *result = new Texture(
            texture,
            surface->w,
            surface->h,
            false,
            density
        );
        SDL_FreeSurface(surface);
        return result;
    }

    cLogger::getInstance()->log(
        LOG_WARN,
        COMP_INIT,
        logContext,
        "Unable to load adaptive UI texture: " + fileName
    );
    return nullptr;
}
