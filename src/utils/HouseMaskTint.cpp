#include "utils/HouseMaskTint.hpp"

#include "utils/FactionTint.hpp"
#include "include/definitions.h"

#include <SDL3/SDL.h>

#include <algorithm>

[[nodiscard]] Color houseMaskTargetColor(int houseId, const Color &minimapColor)
{
    if (houseId == SARDAUKAR) {
        return Color{255, 0, 255, 255};
    }
    return minimapColor;
}

bool applyHouseMaskTint(SDL_Surface *target, SDL_Surface *mask, const Color &houseColor)
{
    if (target == nullptr || mask == nullptr || target->format != SDL_PIXELFORMAT_RGBA32 ||
        target->w != mask->w || target->h != mask->h) {
        return false;
    }

    SDL_Surface *maskCopy = SDL_ConvertSurface(mask, SDL_PIXELFORMAT_RGBA32);
    if (maskCopy == nullptr) {
        return false;
    }
    if (!SDL_LockSurface(target)) {
        SDL_DestroySurface(maskCopy);
        return false;
    }
    if (!SDL_LockSurface(maskCopy)) {
        SDL_UnlockSurface(target);
        SDL_DestroySurface(maskCopy);
        return false;
    }

    float maskedLuminanceSum = 0.0F;
    int maskedLuminancePixels = 0;
    for (int y = 0; y < target->h; ++y) {
        auto *targetRow = static_cast<Uint8 *>(target->pixels) + y * target->pitch;
        auto *maskRow = static_cast<Uint8 *>(maskCopy->pixels) + y * maskCopy->pitch;
        for (int x = 0; x < target->w; ++x) {
            const Uint8 *targetPixel = targetRow + x * 4;
            const Uint8 *maskPixel = maskRow + x * 4;
            const Uint8 r = targetPixel[0];
            const Uint8 g = targetPixel[1];
            const Uint8 b = targetPixel[2];
            const Uint8 a = targetPixel[3];
            const Uint8 mr = maskPixel[0];
            const Uint8 mg = maskPixel[1];
            const Uint8 mb = maskPixel[2];
            const Uint8 ma = maskPixel[3];
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
    for (int y = 0; y < target->h; ++y) {
        auto *targetRow = static_cast<Uint8 *>(target->pixels) + y * target->pitch;
        auto *maskRow = static_cast<Uint8 *>(maskCopy->pixels) + y * maskCopy->pitch;
        for (int x = 0; x < target->w; ++x) {
            Uint8 *targetPixel = targetRow + x * 4;
            const Uint8 *maskPixel = maskRow + x * 4;
            const Uint8 r = targetPixel[0];
            const Uint8 g = targetPixel[1];
            const Uint8 b = targetPixel[2];
            const Uint8 a = targetPixel[3];
            const Uint8 mr = maskPixel[0];
            const Uint8 mg = maskPixel[1];
            const Uint8 mb = maskPixel[2];
            const Uint8 ma = maskPixel[3];
            const float strength =
                (static_cast<float>(ma) / 255.0F) *
                (static_cast<float>(std::max({mr, mg, mb})) / 255.0F);
            if (strength <= 0.0F || a == 0) {
                continue;
            }
            const float luminance =
                (0.299F * r + 0.587F * g + 0.114F * b) / 128.0F;
            const auto tint = [strength, luminance, averageMaskedLuminance](Uint8 original, Uint8 targetChannel) {
                const float colored = applyFactionTintChannel(
                    targetChannel,
                    luminance,
                    averageMaskedLuminance
                );
                return static_cast<Uint8>(std::clamp(
                    original * (1.0F - strength) + colored * strength,
                    0.0F,
                    255.0F
                ));
            };
            targetPixel[0] = tint(r, houseColor.r);
            targetPixel[1] = tint(g, houseColor.g);
            targetPixel[2] = tint(b, houseColor.b);
        }
    }

    SDL_UnlockSurface(maskCopy);
    SDL_UnlockSurface(target);
    SDL_DestroySurface(maskCopy);
    return true;
}
