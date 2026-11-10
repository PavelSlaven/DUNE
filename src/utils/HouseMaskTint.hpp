#pragma once

#include "utils/Color.hpp"

struct SDL_Surface;

[[nodiscard]] Color houseMaskTargetColor(int houseId, const Color &minimapColor);
bool applyHouseMaskTint(SDL_Surface *target, SDL_Surface *mask, const Color &houseColor);
