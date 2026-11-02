#pragma once

#include "utils/Color.hpp"
#include "utils/cRectangle.h"

#include <SDL2/SDL.h>
#include <string>
#include <vector>

class Texture;

struct UnitDrawCall {
    std::string method;
    Texture *texture = nullptr;
    cRectangle source{0, 0, 0, 0};
    cRectangle destination{0, 0, 0, 0};
    SDL_FRect floatDestination{0.0F, 0.0F, 0.0F, 0.0F};
    Color color{0, 0, 0, 0};
    int x = 0;
    int y = 0;
    int width = 0;
    int height = 0;
    Uint8 opacity = 255;
    SDL_BlendMode blendMode = SDL_BLENDMODE_BLEND;
};

struct UnitRecordedText {
    int x;
    int y;
    Color color;
    std::string text;
    bool shadow;
};

std::vector<UnitDrawCall> &unitDrawCalls();
void clearUnitDrawCalls();
std::vector<UnitRecordedText> &unitRecordedText();
void clearUnitRecordedText();
