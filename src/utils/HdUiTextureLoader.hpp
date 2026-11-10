#pragma once

#include <string>

struct SDL_Renderer;
class Texture;

Texture *loadHdUiTexture(SDL_Renderer *renderer, const std::string &fileName, const std::string &logContext = "HD UI");
