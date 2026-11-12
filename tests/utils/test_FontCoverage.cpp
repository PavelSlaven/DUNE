#define SDL_MAIN_HANDLED
#include <SDL3_ttf/SDL_ttf.h>

#include "utils/FontSupport.hpp"

#include <catch2/catch_test_macros.hpp>

#include <filesystem>
#include <memory>
#include <stdexcept>
#include <string>

namespace {

struct TtfQuitGuard {
    ~TtfQuitGuard()
    {
        TTF_Quit();
    }
};

struct FontCloser {
    void operator()(TTF_Font *font) const
    {
        if (font) {
            TTF_CloseFont(font);
        }
    }
};

using FontPtr = std::unique_ptr<TTF_Font, FontCloser>;

}

TEST_CASE("Russian text glyphs are covered by the UI fonts or the symbol fallback", "[font]")
{
    if (!TTF_Init()) {
        throw std::runtime_error("TTF_Init failed");
    }
    TtfQuitGuard ttfQuitGuard;

    const auto fontDirectory = std::filesystem::path(D2TM_SOURCE_DIR) / "resources/bin/data";
    FontPtr russo(TTF_OpenFont((fontDirectory / "RussoOne-Regular.ttf").string().c_str(), 20));
    FontPtr narrow(TTF_OpenFont((fontDirectory / "PTSansNarrow-Regular.ttf").string().c_str(), 20));
    FontPtr fallback(TTF_OpenFont((fontDirectory / "PTMono-Regular.ttf").string().c_str(), 20));
    if (!russo || !narrow || !fallback) {
        throw std::runtime_error("Could not open required fonts");
    }

    const std::u32string russianRequired =
        U"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        U"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        U"0123456789.,!?—–-[]()<>/:;«»";
    const std::u32string serviceSymbols = U"%+=№₽";
    TTF_Font *fonts[] = {russo.get(), narrow.get()};
    for (TTF_Font *font : fonts) {
        for (const char32_t codepoint : russianRequired) {
            CHECK(TTF_FontHasGlyph(font, static_cast<Uint32>(codepoint)));
        }
        for (const char32_t codepoint : serviceSymbols) {
            CHECK((TTF_FontHasGlyph(font, static_cast<Uint32>(codepoint)) ||
                   TTF_FontHasGlyph(fallback.get(), static_cast<Uint32>(codepoint))));
        }
        CHECK(ttfFontSupportsText(font, "Повторить Миссии Далее"));
        CHECK((ttfFontSupportsText(font, "150%") ||
               ttfFontSupportsText(fallback.get(), "150%")));
    }
    CHECK(TTF_FontHasGlyph(fallback.get(), static_cast<Uint32>(U'<')));
    CHECK(TTF_FontHasGlyph(fallback.get(), static_cast<Uint32>(U'>')));
    CHECK(TTF_FontHasGlyph(fallback.get(), static_cast<Uint32>(U'…')));
}

TEST_CASE("Scale arrows are provided only by the symbol fallback font", "[font]")
{
    if (!TTF_Init()) {
        throw std::runtime_error("TTF_Init failed");
    }
    TtfQuitGuard ttfQuitGuard;

    FontPtr fallback(TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTMono-Regular.ttf", 12));
    FontPtr arrakeen(TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/arrakeen.fon", 12));
    FontPtr benegess(TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/benegess.fon", 12));
    FontPtr small(TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/small.ttf", 12));
    FontPtr russo(TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/RussoOne-Regular.ttf", 12));
    FontPtr narrow(TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTSansNarrow-Regular.ttf", 12));
    if (!fallback || !arrakeen || !benegess || !small || !russo || !narrow) {
        throw std::runtime_error("Could not open required fonts");
    }

    CHECK(TTF_FontHasGlyph(fallback.get(), 0x25C4));
    CHECK(TTF_FontHasGlyph(fallback.get(), 0x25BA));
    CHECK_FALSE(TTF_FontHasGlyph(arrakeen.get(), 0x25C4));
    CHECK_FALSE(TTF_FontHasGlyph(arrakeen.get(), 0x25BA));
    CHECK_FALSE(TTF_FontHasGlyph(benegess.get(), 0x25C4));
    CHECK_FALSE(TTF_FontHasGlyph(benegess.get(), 0x25BA));
    CHECK_FALSE(TTF_FontHasGlyph(small.get(), 0x25C4));
    CHECK_FALSE(TTF_FontHasGlyph(small.get(), 0x25BA));
    CHECK_FALSE(TTF_FontHasGlyph(russo.get(), 0x25C4));
    CHECK_FALSE(TTF_FontHasGlyph(russo.get(), 0x25BA));
    CHECK_FALSE(TTF_FontHasGlyph(narrow.get(), 0x25C4));
    CHECK_FALSE(TTF_FontHasGlyph(narrow.get(), 0x25BA));
}
