#define SDL_MAIN_HANDLED
#include <SDL2/SDL_ttf.h>
#include "utils/FontSupport.hpp"

#include <filesystem>
#include <iostream>
#include <string>

int main()
{
    if (TTF_Init() != 0) {
        std::cerr << "TTF_Init failed: " << TTF_GetError() << '\n';
        return 1;
    }

    const std::filesystem::path fontPath =
        std::filesystem::path(D2TM_SOURCE_DIR) /
        "resources/bin/data/Sangyo-Regular.otf";
    const std::filesystem::path fallbackPath =
        std::filesystem::path(D2TM_SOURCE_DIR) /
        "resources/bin/data/PTMono-Regular.ttf";
    TTF_Font *font = TTF_OpenFont(fontPath.string().c_str(), 20);
    TTF_Font *fallback = TTF_OpenFont(fallbackPath.string().c_str(), 20);
    if (!font || !fallback) {
        std::cerr << "Could not open Sangyo: " << TTF_GetError() << '\n';
        if (font) TTF_CloseFont(font);
        if (fallback) TTF_CloseFont(fallback);
        TTF_Quit();
        return 1;
    }

    const std::u32string russianRequired =
        U"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        U"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        U"0123456789.,!?—–-[]()<>/:;«»";
    bool passed = true;
    for (const char32_t codepoint : russianRequired) {
        if (TTF_GlyphIsProvided32(font, static_cast<Uint32>(codepoint)) != 0) {
            continue;
        }
        std::cerr << "Sangyo is missing U+" << std::hex
                  << static_cast<Uint32>(codepoint) << '\n';
        passed = false;
    }

    const std::u32string serviceSymbols = U"%+=№₽";
    for (const char32_t codepoint : serviceSymbols) {
        if (TTF_GlyphIsProvided32(font, static_cast<Uint32>(codepoint)) != 0 ||
            TTF_GlyphIsProvided32(fallback, static_cast<Uint32>(codepoint)) != 0) {
            continue;
        }
        std::cerr << "Neither font provides U+" << std::hex
                  << static_cast<Uint32>(codepoint) << '\n';
        passed = false;
    }

    if (!ttfFontSupportsText(font, "Повторить Миссии Далее")) {
        std::cerr << "Sangyo cannot render a representative Russian label\n";
        passed = false;
    }
    if (!ttfFontSupportsText(font, "150%") &&
        !ttfFontSupportsText(fallback, "150%")) {
        std::cerr << "The missing-glyph fallback contract is broken\n";
        passed = false;
    }

    TTF_CloseFont(font);
    TTF_CloseFont(fallback);
    TTF_Quit();
    return passed ? 0 : 1;
}
