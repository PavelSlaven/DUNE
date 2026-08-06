#include "utils/HdUiTextureLoader.hpp"

#include "d2tmc.h"
#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"
#include "utils/cLog.h"

#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

#include <filesystem>
#include <format>

Texture *loadHdUiTexture(
    const std::string &fileName,
    int preferredDensity,
    const std::string &logContext)
{
    static_cast<void>(preferredDensity);
    constexpr int density = 4;
    const std::filesystem::path path =
        std::filesystem::path("data") / "hd4" / fileName;
    if (std::filesystem::exists(path)) {

        SDL_Surface *surface = IMG_Load(path.string().c_str());
        if (surface) {
            SDL_Texture *texture = SDL_CreateTextureFromSurface(
                renderDrawer->getRenderer(),
                surface
            );
            if (texture) {
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
            SDL_FreeSurface(surface);
        }
    }

    cLogger::getInstance()->log(
        LOG_WARN,
        COMP_INIT,
        logContext,
        "Unable to load adaptive UI texture: " + fileName
    );
    return nullptr;
}
