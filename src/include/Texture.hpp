#pragma once
#include <SDL2/SDL.h>
#include <algorithm>

class Texture {

public:
    SDL_Texture *tex;
    int w=0;
    int h=0;
    int pixelW=0;
    int pixelH=0;
    int density=1;
    bool isRenderTarget=false;

    explicit Texture(
        SDL_Texture *texture,
        int width,
        int height,
        bool isTarget = false,
        int assetDensity = 1)
        : tex(texture),
        w(width / std::max(1, assetDensity)),
        h(height / std::max(1, assetDensity)),
        pixelW(width),
        pixelH(height),
        density(std::max(1, assetDensity)),
        isRenderTarget(isTarget) {}

    Texture() = delete;

    ~Texture() {
        if (tex) {
            SDL_DestroyTexture(tex);
            tex = nullptr;
        }
    }
};
