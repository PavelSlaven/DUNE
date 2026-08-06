#pragma once

#include <SDL2/SDL_ttf.h>

#include <cstdint>
#include <string_view>

[[nodiscard]] inline bool ttfFontSupportsText(TTF_Font *font, std::string_view text)
{
    if (!font) return false;

    const auto *current = reinterpret_cast<const unsigned char *>(text.data());
    const auto *end = current + text.size();
    while (current < end) {
        std::uint32_t codepoint = 0;
        std::size_t remaining = static_cast<std::size_t>(end - current);
        std::size_t length = 0;

        if (*current < 0x80) {
            codepoint = *current;
            length = 1;
        }
        else if ((*current & 0xE0) == 0xC0 && remaining >= 2) {
            codepoint = *current & 0x1F;
            length = 2;
        }
        else if ((*current & 0xF0) == 0xE0 && remaining >= 3) {
            codepoint = *current & 0x0F;
            length = 3;
        }
        else if ((*current & 0xF8) == 0xF0 && remaining >= 4) {
            codepoint = *current & 0x07;
            length = 4;
        }
        else {
            return false;
        }

        for (std::size_t i = 1; i < length; ++i) {
            if ((current[i] & 0xC0) != 0x80) return false;
            codepoint = (codepoint << 6) | (current[i] & 0x3F);
        }
        current += length;

        if (codepoint == ' ' || codepoint == '\t' ||
            codepoint == '\n' || codepoint == '\r') {
            continue;
        }
        if (TTF_GlyphIsProvided32(font, static_cast<Uint32>(codepoint)) == 0) {
            return false;
        }
    }
    return true;
}
