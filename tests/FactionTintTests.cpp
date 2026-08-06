#include "utils/FactionTint.hpp"

#include <iostream>

int main()
{
    const auto darkAsset = applyFactionTintChannel(255, 0.40F, 0.40F);
    const auto lightAsset = applyFactionTintChannel(255, 1.20F, 1.20F);
    if (darkAsset != 166 || lightAsset != 166) {
        std::cerr << "different source textures produce different faction tones\n";
        return 1;
    }

    const auto shadow = applyFactionTintChannel(255, 0.40F, 0.65F);
    const auto highlight = applyFactionTintChannel(255, 0.90F, 0.65F);
    if (shadow >= highlight) {
        std::cerr << "faction tint no longer preserves texture shading\n";
        return 1;
    }

    if (applyFactionTintChannel(0, 1.0F, 1.0F) != 0) {
        std::cerr << "inactive house-color channel became visible\n";
        return 1;
    }
    return 0;
}
