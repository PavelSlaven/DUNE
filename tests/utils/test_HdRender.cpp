#include "utils/WorldScale.hpp"
#include "utils/UnitSpriteLayout.hpp"
#include "utils/WindTrapFlag.hpp"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "drawers/cTextTextureCache.h"
#include "game/Preferences.hpp"
#include "game/cGameSettings.h"
#include "include/Texture.hpp"
#include "utils/Graphics.hpp"
#include "utils/InitialGameSettings.hpp"
#include "utils/cIniFile.h"
#include "utils/cRectangle.h"
#include "utils/Color.hpp"

#include <catch2/catch_approx.hpp>
#include <catch2/catch_test_macros.hpp>
#include <SDL3/SDL.h>
#include <SDL3_ttf/SDL_ttf.h>

#include <array>
#include <filesystem>
#include <fstream>
#include <memory>

namespace {

class SoftwareRenderer {
public:
    SoftwareRenderer(int width, int height)
    {
        output = SDL_CreateSurface(width, height, SDL_PIXELFORMAT_RGBA32);
        REQUIRE(output != nullptr);
        renderer = SDL_CreateSoftwareRenderer(output);
        REQUIRE(renderer != nullptr);
    }

    ~SoftwareRenderer()
    {
        SDL_DestroyRenderer(renderer);
        SDL_DestroySurface(output);
        SDL_Quit();
    }

    SDL_Surface *output = nullptr;
    SDL_Renderer *renderer = nullptr;
};

SDL_Color readPixel(const SoftwareRenderer &canvas, int x, int y)
{
    REQUIRE(SDL_FlushRenderer(canvas.renderer));
    SDL_Color color{};
    REQUIRE(SDL_ReadSurfacePixel(canvas.output, x, y, &color.r, &color.g, &color.b, &color.a));
    return color;
}

void checkColor(SDL_Color actual, SDL_Color expected)
{
    CHECK(actual.r == expected.r);
    CHECK(actual.g == expected.g);
    CHECK(actual.b == expected.b);
    CHECK(actual.a == expected.a);
}

void checkFrame(UnitSpriteFrame actual, UnitSpriteFrame expected)
{
    CHECK(actual.width == expected.width);
    CHECK(actual.height == expected.height);
    CHECK(actual.usesHdFrame == expected.usesHdFrame);
}

void checkRectangle(UnitSpriteRectangle actual, UnitSpriteRectangle expected)
{
    CHECK(actual.x == expected.x);
    CHECK(actual.y == expected.y);
    CHECK(actual.width == expected.width);
    CHECK(actual.height == expected.height);
}

void checkRectangle(UnitSpriteFloatRectangle actual, UnitSpriteFloatRectangle expected)
{
    CHECK(actual.x == expected.x);
    CHECK(actual.y == expected.y);
    CHECK(actual.width == expected.width);
    CHECK(actual.height == expected.height);
}

void checkLogicalPresentation(SDL_Renderer *renderer, int expectedWidth, int expectedHeight,
                              SDL_RendererLogicalPresentation expectedMode)
{
    int width = 0;
    int height = 0;
    SDL_RendererLogicalPresentation mode;
    REQUIRE(SDL_GetRenderLogicalPresentation(renderer, &width, &height, &mode));
    CHECK(width == expectedWidth);
    CHECK(height == expectedHeight);
    CHECK(mode == expectedMode);
}

struct TtfSession {
    ~TtfSession()
    {
        TTF_Quit();
    }
};

}

TEST_CASE("P4 automatic world scale follows the output height", "[P4]")
{
    const std::array<std::array<int, 2>, 8> cases{{
        {600, 100}, {768, 100}, {769, 110}, {1080, 110},
        {1081, 125}, {1600, 125}, {1601, 150}, {2160, 150},
    }};
    for (const auto &[height, expected] : cases) {
        INFO("Output height: " << height);
        CHECK(calculateAutomaticWorldScalePercent(height) == expected);
    }
}

TEST_CASE("P4 world scale choice resolves to a supported percent", "[P4]")
{
    for (int percent : {0, 100, 110, 125, 150}) {
        INFO("Supported percent: " << percent);
        CHECK(isWorldScaleSupported(percent));
    }
    for (int percent : {120, 200, -1}) {
        INFO("Unsupported percent: " << percent);
        CHECK_FALSE(isWorldScaleSupported(percent));
    }
    CHECK(resolveWorldScalePercent(0, 1080) == 110);
    CHECK(resolveWorldScalePercent(125, 768) == 125);
    CHECK(resolveWorldScalePercent(120, 1440) == 125);
    CHECK(resolveWorldScalePercent(-5, 600) == 100);
}

TEST_CASE("P4 world scale zoom is the resolved percent over 100", "[P4]")
{
    CHECK(worldScaleZoom(0, 768) == Catch::Approx(1.0f).epsilon(1e-6));
    CHECK(worldScaleZoom(0, 1080) == Catch::Approx(1.1f).epsilon(1e-6));
    CHECK(worldScaleZoom(150, 768) == Catch::Approx(1.5f).epsilon(1e-6));
    CHECK(worldScaleZoom(0, 2160) == Catch::Approx(1.5f).epsilon(1e-6));
    CHECK(worldScaleZoom(120, 768) == Catch::Approx(1.0f).epsilon(1e-6));
}

TEST_CASE("P4 settings read the world scale key", "[P4]")
{
    const auto setPath = std::filesystem::temp_directory_path() / "p4_world_scale_set.ini";
    const auto unsetPath = std::filesystem::temp_directory_path() / "p4_world_scale_unset.ini";
    {
        std::ofstream file(setPath);
        REQUIRE(file.is_open());
        file << "[SETTINGS]\nWorldScale=125\n";
        REQUIRE(file.good());
    }
    {
        std::ofstream file(unsetPath);
        REQUIRE(file.is_open());
        file << "[SETTINGS]\nScreenWidth=1024\n";
        REQUIRE(file.good());
    }

    cIniFile setIni(setPath.string());
    REQUIRE(setIni.isLoadSuccess());
    REQUIRE(setIni.hasSection("SETTINGS"));
    InitialGameSettings setSettings;
    Preferences::readSettings(setIni.getSection("SETTINGS"), setSettings);
    CHECK(setSettings.worldScalePercent == 125);

    cIniFile unsetIni(unsetPath.string());
    REQUIRE(unsetIni.isLoadSuccess());
    REQUIRE(unsetIni.hasSection("SETTINGS"));
    InitialGameSettings unsetSettings;
    Preferences::readSettings(unsetIni.getSection("SETTINGS"), unsetSettings);
    CHECK(unsetSettings.worldScalePercent == 0);

    const auto settingsPath = std::filesystem::path(D2TM_SOURCE_DIR) / "resources/bin/settings.ini";
    cIniFile shippedIni(settingsPath.string());
    REQUIRE(shippedIni.isLoadSuccess());
    REQUIRE(shippedIni.hasSection("SETTINGS"));
    InitialGameSettings shippedSettings;
    Preferences::readSettings(shippedIni.getSection("SETTINGS"), shippedSettings);
    CHECK(shippedSettings.worldScalePercent == 0);

    CHECK(std::filesystem::remove(setPath));
    CHECK(std::filesystem::remove(unsetPath));
}

TEST_CASE("P4 HD unit frames use the HD frame size", "[P4]")
{
    checkFrame(resolveUnitSpriteFrame(36, 36, 176, 176, 4), {44, 44, true});
    checkFrame(resolveUnitSpriteFrame(36, 36, 176, 176, 1), {36, 36, false});
    checkFrame(resolveUnitSpriteFrame(36, 36, 0, 0, 4), {36, 36, false});

    checkRectangle(unitSpriteSourceRectangle({44, 44, true}, 3, 0), {132, 0, 44, 44});
    checkRectangle(unitSpriteSourceRectangle({36, 36, false}, 5, 1), {180, 36, 36, 36});

    checkRectangle(unitSpriteDestinationRectangle({44, 44, true}, {100, 200, 36, 36}, 1.0f),
                   {96.0f, 196.0f, 44.0f, 44.0f});
    checkRectangle(unitSpriteDestinationRectangle({44, 44, true}, {100, 200, 54, 54}, 1.5f),
                   {94.0f, 194.0f, 66.0f, 66.0f});
    checkRectangle(unitSpriteDestinationRectangle({36, 36, false}, {100, 200, 54, 54}, 1.5f),
                   {100.0f, 200.0f, 54.0f, 54.0f});
}

TEST_CASE("P4 windtrap flag frame changes every 125 ms", "[P4]")
{
    CHECK(kWindTrapFlagFrames == 8);
    CHECK(kWindTrapFlagFrameSize == 64);
    CHECK(windTrapFlagFrame(0) == 0);
    CHECK(windTrapFlagFrame(124) == 0);
    CHECK(windTrapFlagFrame(125) == 1);
    CHECK(windTrapFlagFrame(999) == 7);
    CHECK(windTrapFlagFrame(1000) == 0);
    CHECK(windTrapFlagFrame(1125) == 1);
}

TEST_CASE("P4 frame density rounds the presentation scale up", "[P4]")
{
    CHECK(calculateFrameDensity(1024, 768, 1024, 768) == 1);
    CHECK(calculateFrameDensity(2048, 1536, 1024, 768) == 2);
    CHECK(calculateFrameDensity(1440, 1080, 1024, 768) == 2);
    CHECK(calculateFrameDensity(1023.9f, 767.9f, 1024, 768) == 1);
    CHECK(calculateFrameDensity(2050, 1538, 1024, 768) == 2);
    CHECK(calculateFrameDensity(5120, 1440, 1024, 768) == 2);
    CHECK(calculateFrameDensity(8192, 6144, 1024, 768) == 4);
    CHECK(calculateFrameDensity(100, 100, 0, 768) == 1);
}

TEST_CASE("P4 render target with density keeps logical size and physical pixels", "[P4]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(32, 32);
    SDLDrawer drawer(canvas.renderer);

    Texture *t = drawer.createRenderTargetTexture(8, 4, 2);
    REQUIRE(t != nullptr);
    CHECK(t->w == 8);
    CHECK(t->h == 4);
    CHECK(t->pixelW == 16);
    CHECK(t->pixelH == 8);
    CHECK(t->density == 2);
    CHECK(t->isRenderTarget);
    float width = 0;
    float height = 0;
    REQUIRE(SDL_GetTextureSize(t->tex.get(), &width, &height));
    CHECK(width == 16);
    CHECK(height == 8);
    SDL_ScaleMode scaleMode;
    REQUIRE(SDL_GetTextureScaleMode(t->tex.get(), &scaleMode));
    CHECK(scaleMode == SDL_SCALEMODE_LINEAR);
    CHECK(SDL_GetRenderTarget(canvas.renderer) == nullptr);

    drawer.beginDrawingToTexture(t);
    checkLogicalPresentation(canvas.renderer, 8, 4, SDL_LOGICAL_PRESENTATION_STRETCH);
    drawer.endDrawingToTexture();

    Texture *u = drawer.createRenderTargetTexture(8, 4);
    REQUIRE(u != nullptr);
    CHECK(u->pixelW == 8);
    CHECK(u->density == 1);
    REQUIRE(SDL_GetTextureScaleMode(u->tex.get(), &scaleMode));
    CHECK(scaleMode == SDL_SCALEMODE_NEAREST);
    drawer.beginDrawingToTexture(u);
    int logicalWidth = 0;
    int logicalHeight = 0;
    SDL_RendererLogicalPresentation mode;
    REQUIRE(SDL_GetRenderLogicalPresentation(canvas.renderer, &logicalWidth, &logicalHeight, &mode));
    CHECK(mode == SDL_LOGICAL_PRESENTATION_DISABLED);
    drawer.endDrawingToTexture();

    CHECK(drawer.getFrameDensity() == 1);
    drawer.setFrameDensity(3);
    CHECK(drawer.getFrameDensity() == 3);
    drawer.setFrameDensity(0);
    CHECK(drawer.getFrameDensity() == 1);
    delete u;
    delete t;
}

TEST_CASE("P4 HD frame target keeps detail finer than a logical pixel", "[P4]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(16, 16);
    SDLDrawer drawer(canvas.renderer);
    REQUIRE(SDL_SetRenderLogicalPresentation(canvas.renderer, 8, 8, SDL_LOGICAL_PRESENTATION_INTEGER_SCALE));

    std::unique_ptr<SDL_Surface, decltype(&SDL_DestroySurface)> surface(
        SDL_CreateSurface(4, 4, SDL_PIXELFORMAT_RGBA32), SDL_DestroySurface);
    REQUIRE(surface != nullptr);
    const SDL_Rect redHalf{0, 0, 2, 4};
    const SDL_Rect blueHalf{2, 0, 2, 4};
    REQUIRE(SDL_FillSurfaceRect(surface.get(), &redHalf,
                               SDL_MapSurfaceRGBA(surface.get(), 255, 0, 0, 255)));
    REQUIRE(SDL_FillSurfaceRect(surface.get(), &blueHalf,
                               SDL_MapSurfaceRGBA(surface.get(), 0, 0, 255, 255)));
    SDL_Texture *texture = SDL_CreateTextureFromSurface(canvas.renderer, surface.get());
    REQUIRE(texture != nullptr);
    Texture src(texture, 4, 4, false, 4);
    REQUIRE(SDL_SetTextureScaleMode(src.tex.get(), SDL_SCALEMODE_NEAREST));

    Texture *frame = drawer.createRenderTargetTexture(8, 8, 2);
    REQUIRE(frame != nullptr);
    drawer.beginDrawingToTexture(frame);
    drawer.renderClearToColor();
    drawer.renderStrechSprite(&src, cRectangle{0, 0, 1, 1}, cRectangle{0, 0, 1, 1});
    drawer.endDrawingToTexture();
    drawer.renderClearToColor();
    drawer.renderSprite(frame, 0, 0);
    checkColor(readPixel(canvas, 0, 0), {255, 0, 0, 255});
    checkColor(readPixel(canvas, 1, 0), {0, 0, 255, 255});
    checkColor(readPixel(canvas, 2, 0), {0, 0, 0, 255});
    delete frame;

    frame = drawer.createRenderTargetTexture(8, 8);
    REQUIRE(frame != nullptr);
    drawer.beginDrawingToTexture(frame);
    drawer.renderClearToColor();
    drawer.renderStrechSprite(&src, cRectangle{0, 0, 1, 1}, cRectangle{0, 0, 1, 1});
    drawer.endDrawingToTexture();
    drawer.renderClearToColor();
    drawer.renderSprite(frame, 0, 0);
    checkColor(readPixel(canvas, 0, 0), readPixel(canvas, 1, 0));
    delete frame;
}

TEST_CASE("P4 nested render target keeps the frame target state", "[P4]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(16, 16);
    SDLDrawer drawer(canvas.renderer);
    REQUIRE(SDL_SetRenderLogicalPresentation(canvas.renderer, 8, 8, SDL_LOGICAL_PRESENTATION_INTEGER_SCALE));

    Texture *frame = drawer.createRenderTargetTexture(8, 8, 2);
    REQUIRE(frame != nullptr);
    Texture *inner = drawer.createRenderTargetTexture(4, 4);
    REQUIRE(inner != nullptr);
    drawer.beginDrawingToTexture(frame);
    drawer.renderClearToColor();
    drawer.beginDrawingToTexture(inner);
    drawer.renderClearToColor(Color{0, 0, 255, 255});
    drawer.endDrawingToTexture();
    CHECK(SDL_GetRenderTarget(canvas.renderer) == frame->tex.get());
    checkLogicalPresentation(canvas.renderer, 8, 8, SDL_LOGICAL_PRESENTATION_STRETCH);
    CHECK_FALSE(SDL_RenderClipEnabled(canvas.renderer));

    drawer.renderRectFillColor(0, 0, 1, 1, Color{0, 255, 0, 255});
    drawer.endDrawingToTexture();
    drawer.renderClearToColor();
    drawer.renderSprite(frame, 0, 0);
    checkColor(readPixel(canvas, 0, 0), {0, 255, 0, 255});
    checkColor(readPixel(canvas, 1, 1), {0, 255, 0, 255});
    checkColor(readPixel(canvas, 2, 2), {0, 0, 0, 255});
    delete inner;
    delete frame;
}

TEST_CASE("Text drawer measures in canvas points at every frame density", "[text]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    REQUIRE(TTF_Init());
    SoftwareRenderer canvas(64, 64);
    TtfSession ttfSession;

    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> font(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTSansNarrow-Regular.ttf", 14), TTF_CloseFont);
    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> fallback(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTMono-Regular.ttf", 14), TTF_CloseFont);
    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> reference14(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTSansNarrow-Regular.ttf", 14), TTF_CloseFont);
    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> referenceFallback14(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTMono-Regular.ttf", 14), TTF_CloseFont);
    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> reference28(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTSansNarrow-Regular.ttf", 28), TTF_CloseFont);
    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> referenceFallback28(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTMono-Regular.ttf", 28), TTF_CloseFont);
    REQUIRE(font != nullptr);
    REQUIRE(fallback != nullptr);
    REQUIRE(reference14 != nullptr);
    REQUIRE(referenceFallback14 != nullptr);
    REQUIRE(reference28 != nullptr);
    REQUIRE(referenceFallback28 != nullptr);
    REQUIRE(TTF_AddFallbackFont(font.get(), fallback.get()));
    REQUIRE(TTF_AddFallbackFont(reference14.get(), referenceFallback14.get()));
    REQUIRE(TTF_AddFallbackFont(reference28.get(), referenceFallback28.get()));

    int w14 = 0;
    int h14 = 0;
    int w28 = 0;
    int h28 = 0;
    REQUIRE(TTF_GetStringSize(reference14.get(), "Настройки ◄", 0, &w14, &h14));
    REQUIRE(TTF_GetStringSize(reference28.get(), "Настройки ◄", 0, &w28, &h28));

    {
        SDLDrawer drawer(canvas.renderer);
        cGameSettings settings;
        cTextDrawer text(font.get(), fallback.get(), 14.0F, &settings, &drawer);

        CHECK(text.getTextLength("Настройки ◄") == w14);
        CHECK(text.getFontHeight() == TTF_GetFontHeight(reference14.get()));

        drawer.setFrameDensity(2);
        CHECK(text.getTextLength("Настройки ◄") == (w28 + 1) / 2);
        CHECK(text.getFontHeight() == (TTF_GetFontHeight(reference28.get()) + 1) / 2);
        CHECK(TTF_GetFontSize(font.get()) == 28.0F);
        CHECK(TTF_GetFontSize(fallback.get()) == 28.0F);

        drawer.setFrameDensity(1);
        CHECK(text.getTextLength("Настройки ◄") == w14);
        CHECK(TTF_GetFontSize(font.get()) == 14.0F);
        CHECK(TTF_GetFontSize(fallback.get()) == 14.0F);
    }
}

TEST_CASE("Text is drawn anti-aliased", "[text]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    REQUIRE(TTF_Init());
    SoftwareRenderer canvas(160, 40);
    TtfSession ttfSession;

    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> font(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTSansNarrow-Regular.ttf", 14), TTF_CloseFont);
    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> fallback(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTMono-Regular.ttf", 14), TTF_CloseFont);
    REQUIRE(font != nullptr);
    REQUIRE(fallback != nullptr);
    REQUIRE(TTF_AddFallbackFont(font.get(), fallback.get()));

    {
        SDLDrawer drawer(canvas.renderer);
        cGameSettings settings;
        cTextDrawer text(font.get(), fallback.get(), 14.0F, &settings, &drawer);

        REQUIRE(SDL_SetRenderDrawColor(canvas.renderer, 0, 0, 0, 255));
        REQUIRE(SDL_RenderClear(canvas.renderer));
        text.drawText(4, 4, Color::White, "Ремонт", false);

        int full = 0;
        int partial = 0;
        for (int y = 0; y < 40; ++y) {
            for (int x = 0; x < 160; ++x) {
                const SDL_Color pixel = readPixel(canvas, x, y);
                if (pixel.r == 255) {
                    ++full;
                } else if (pixel.r > 0 && pixel.r < 255) {
                    ++partial;
                }
            }
        }
        CHECK(full > 0);
        CHECK(partial > 0);
    }
}

TEST_CASE("Text cache keeps pixel size and canvas size apart", "[text]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    REQUIRE(TTF_Init());
    SoftwareRenderer canvas(64, 64);
    TtfSession ttfSession;

    std::unique_ptr<TTF_Font, decltype(&TTF_CloseFont)> font(
        TTF_OpenFont(D2TM_SOURCE_DIR "/resources/bin/data/PTSansNarrow-Regular.ttf", 28), TTF_CloseFont);
    REQUIRE(font != nullptr);

    {
        SDLDrawer drawer(canvas.renderer);
        [[maybe_unused]] cGameSettings settings;
        cTextTextureCache cache(font.get(), &drawer);
        cache.setDensity(2);
        textCacheEntry *entry = cache.findOrCreate(Color::White, "Repair");
        REQUIRE(entry != nullptr);

        float textureWidth = 0.0F;
        float textureHeight = 0.0F;
        REQUIRE(SDL_GetTextureSize(entry->texture, &textureWidth, &textureHeight));
        CHECK(textureWidth == entry->pixelWidth);
        CHECK(textureHeight == entry->pixelHeight);
        CHECK(entry->width == (entry->pixelWidth + 1) / 2);
        CHECK(entry->height == (entry->pixelHeight + 1) / 2);

        SDL_ScaleMode textureScaleMode;
        SDL_ScaleMode shadowScaleMode;
        REQUIRE(SDL_GetTextureScaleMode(entry->texture, &textureScaleMode));
        REQUIRE(SDL_GetTextureScaleMode(entry->shadowsTexture, &shadowScaleMode));
        CHECK(textureScaleMode == SDL_SCALEMODE_LINEAR);
        CHECK(shadowScaleMode == SDL_SCALEMODE_LINEAR);
    }
}
