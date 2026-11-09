#include "data/gfxdata.h"
#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"
#include "utils/Graphics.hpp"
#include "utils/HouseColors.h"
#include "utils/cIniFile.h"
#include "utils/cRectangle.h"

#include <catch2/catch_test_macros.hpp>
#include <SDL3/SDL.h>

#include <array>
#include <filesystem>
#include <memory>
#include <string>
#include <utility>

namespace {

using Surface = std::unique_ptr<SDL_Surface, decltype(&SDL_DestroySurface)>;

class SoftwareRenderer {
public:
    SoftwareRenderer(int width, int height)
    {
        target = SDL_CreateSurface(width, height, SDL_PIXELFORMAT_RGBA32);
        REQUIRE(target != nullptr);
        renderer = SDL_CreateSoftwareRenderer(target);
        REQUIRE(renderer != nullptr);
    }

    ~SoftwareRenderer()
    {
        SDL_DestroyRenderer(renderer);
        SDL_DestroySurface(target);
        SDL_Quit();
    }

    SDL_Renderer *renderer = nullptr;

private:
    SDL_Surface *target = nullptr;
};

Surface createSurface(int width, int height, SDL_PixelFormat format = SDL_PIXELFORMAT_RGBA32)
{
    Surface surface(SDL_CreateSurface(width, height, format), SDL_DestroySurface);
    REQUIRE(surface != nullptr);
    return surface;
}

void fillSurface(SDL_Surface *surface, SDL_Color color, const SDL_Rect *rect = nullptr)
{
    REQUIRE(SDL_FillSurfaceRect(surface, rect,
                               SDL_MapSurfaceRGBA(surface, color.r, color.g, color.b, color.a)));
}

void clearRenderer(SDL_Renderer *renderer)
{
    REQUIRE(SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255));
    REQUIRE(SDL_RenderClear(renderer));
}

Surface readPixels(SDL_Renderer *renderer)
{
    Surface pixels(SDL_RenderReadPixels(renderer, nullptr), SDL_DestroySurface);
    REQUIRE(pixels != nullptr);
    return pixels;
}

void checkPixel(SDL_Surface *surface, int x, int y, SDL_Color expected)
{
    INFO("Pixel (" << x << ", " << y << ")");
    SDL_Color actual{};
    REQUIRE(SDL_ReadSurfacePixel(surface, x, y, &actual.r, &actual.g, &actual.b, &actual.a));
    CHECK(actual.r == expected.r);
    CHECK(actual.g == expected.g);
    CHECK(actual.b == expected.b);
    CHECK(actual.a == expected.a);
}

}

TEST_CASE("P3 Texture keeps physical size and density", "[P3]")
{
    Texture hd4(nullptr, 2560, 832, false, 4);
    CHECK(hd4.w == 640);
    CHECK(hd4.h == 208);
    CHECK(hd4.pixelW == 2560);
    CHECK(hd4.pixelH == 832);
    CHECK(hd4.density == 4);

    Texture classic(nullptr, 64, 48);
    CHECK(classic.w == 64);
    CHECK(classic.h == 48);
    CHECK(classic.pixelW == 64);
    CHECK(classic.pixelH == 48);
    CHECK(classic.density == 1);

    Texture zeroDensity(nullptr, 64, 48, false, 0);
    CHECK(zeroDensity.density == 1);
    CHECK(zeroDensity.w == 64);
}

TEST_CASE("P3 Graphics loads HD4 data pack with density 4", "[P3]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(8, 8);
    const std::filesystem::path sourceRoot = D2TM_SOURCE_DIR;
    Graphics gfx(canvas.renderer, (sourceRoot / "resources/bin/data/sdl_data_hd4.dat").string(), 4);
    CHECK(gfx.getDensity() == 4);

    Texture *t = gfx.getTexture(UNIT_QUAD);
    REQUIRE(t != nullptr);
    SDL_Surface *surface = gfx.getSurface(UNIT_QUAD);
    REQUIRE(surface != nullptr);
    CHECK(t->pixelW == surface->w);
    CHECK(t->pixelH == surface->h);
    CHECK(t->w == t->pixelW / 4);
    CHECK(t->h == t->pixelH / 4);
    CHECK(t->density == 4);
    SDL_ScaleMode scaleMode;
    REQUIRE(SDL_GetTextureScaleMode(t->tex.get(), &scaleMode));
    CHECK(scaleMode == SDL_SCALEMODE_LINEAR);
    CHECK(gfx.getTexture("UNIT_QUAD") == t);
    CHECK(gfx.getTexture(UNIT_QUAD) == t);

    Texture *harvester = gfx.getTexture("HM_UNIT_HARVESTER");
    REQUIRE(harvester != nullptr);
    CHECK(harvester->pixelW == 2560);
    CHECK(harvester->pixelH == 832);
    CHECK(harvester->w == 640);
    CHECK(harvester->h == 208);
    CHECK(harvester->density == 4);
}

TEST_CASE("P3 Graphics keeps the classic editor pack at density 1", "[P3]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(8, 8);
    const std::filesystem::path sourceRoot = D2TM_SOURCE_DIR;
    Graphics editor(canvas.renderer, (sourceRoot / "resources/bin/data/sdl_gfxeditor.dat").string());
    CHECK(editor.getDensity() == 1);
    Texture *t = editor.getTexture(0);
    REQUIRE(t != nullptr);
    SDL_Surface *surface = editor.getSurface(0);
    REQUIRE(surface != nullptr);
    CHECK(t->w == surface->w);
    CHECK(t->h == surface->h);
    CHECK(t->density == 1);
    SDL_ScaleMode scaleMode;
    REQUIRE(SDL_GetTextureScaleMode(t->tex.get(), &scaleMode));
    CHECK(scaleMode == SDL_SCALEMODE_NEAREST);
}

TEST_CASE("P3 renderStrechSprite scales the source rectangle by density", "[P3]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(8, 8);
    SDLDrawer drawer(canvas.renderer);
    auto surface = createSurface(8, 4);
    const SDL_Rect redHalf{0, 0, 4, 4};
    const SDL_Rect blueHalf{4, 0, 4, 4};
    fillSurface(surface.get(), {255, 0, 0, 255}, &redHalf);
    fillSurface(surface.get(), {0, 0, 255, 255}, &blueHalf);
    SDL_Texture *texture = SDL_CreateTextureFromSurface(canvas.renderer, surface.get());
    REQUIRE(texture != nullptr);
    Texture tex(texture, 8, 4, false, 4);
    REQUIRE(SDL_SetTextureScaleMode(tex.tex.get(), SDL_SCALEMODE_NEAREST));

    clearRenderer(canvas.renderer);
    drawer.renderStrechSprite(&tex, cRectangle{1, 0, 1, 1}, cRectangle{0, 0, 4, 4});
    auto stretchedPixels = readPixels(canvas.renderer);
    checkPixel(stretchedPixels.get(), 0, 0, {0, 0, 255, 255});
    checkPixel(stretchedPixels.get(), 3, 3, {0, 0, 255, 255});
    checkPixel(stretchedPixels.get(), 4, 4, {0, 0, 0, 255});

    clearRenderer(canvas.renderer);
    drawer.renderSprite(&tex, 0, 0);
    auto spritePixels = readPixels(canvas.renderer);
    checkPixel(spritePixels.get(), 0, 0, {255, 0, 0, 255});
    checkPixel(spritePixels.get(), 1, 0, {0, 0, 255, 255});
    checkPixel(spritePixels.get(), 2, 0, {0, 0, 0, 255});
    checkPixel(spritePixels.get(), 0, 1, {0, 0, 0, 255});
}

TEST_CASE("P3 renderFromSurface divides the destination by density", "[P3]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(16, 16);
    SDLDrawer drawer(canvas.renderer);
    auto surface = createSurface(8, 8);
    fillSurface(surface.get(), {0, 255, 0, 255});

    clearRenderer(canvas.renderer);
    drawer.renderFromSurface(surface.get(), 0, 0, 255, 4);
    auto hd4Pixels = readPixels(canvas.renderer);
    checkPixel(hd4Pixels.get(), 1, 1, {0, 255, 0, 255});
    checkPixel(hd4Pixels.get(), 2, 2, {0, 0, 0, 255});
    checkPixel(hd4Pixels.get(), 2, 0, {0, 0, 0, 255});

    clearRenderer(canvas.renderer);
    drawer.renderFromSurface(surface.get(), 0, 0);
    auto classicPixels = readPixels(canvas.renderer);
    checkPixel(classicPixels.get(), 7, 7, {0, 255, 0, 255});
    checkPixel(classicPixels.get(), 8, 8, {0, 0, 0, 255});
}

TEST_CASE("P3 palette recolor returns RGBA surfaces untinted with density", "[P3]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(8, 8);
    SDLDrawer drawer(canvas.renderer);
    auto surface = createSurface(8, 4);
    fillSurface(surface.get(), {40, 50, 60, 255});
    HouseColors colors{};
    colors.fill(HouseColor{10, 200, 30});

    Texture *t = drawer.createTextureFromIndexedSurfaceWithPalette(surface.get(), 0, colors, 4);
    REQUIRE(t != nullptr);
    CHECK(t->w == 2);
    CHECK(t->h == 1);
    CHECK(t->pixelW == 8);
    CHECK(t->pixelH == 4);
    CHECK(t->density == 4);
    clearRenderer(canvas.renderer);
    drawer.renderSprite(t, 0, 0);
    auto pixels = readPixels(canvas.renderer);
    checkPixel(pixels.get(), 0, 0, {40, 50, 60, 255});
    checkPixel(pixels.get(), 2, 0, {0, 0, 0, 255});
    checkPixel(pixels.get(), 0, 1, {0, 0, 0, 255});
    delete t;
}

TEST_CASE("P3 palette recolor still tints indexed surfaces", "[P3]")
{
    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(8, 8);
    SDLDrawer drawer(canvas.renderer);
    auto surface = createSurface(8, 4, SDL_PIXELFORMAT_INDEX8);
    SDL_Palette *palette = SDL_CreateSurfacePalette(surface.get());
    REQUIRE(palette != nullptr);
    REQUIRE(palette->ncolors == 256);
    std::array<SDL_Color, 256> paletteColors;
    paletteColors.fill(SDL_Color{0, 0, 0, 255});
    paletteColors[144] = {255, 255, 255, 255};
    REQUIRE(SDL_SetPaletteColors(palette, paletteColors.data(), 0, 256));
    REQUIRE(SDL_FillSurfaceRect(surface.get(), nullptr, 144));
    HouseColors colors{};
    colors[0] = {10, 200, 30};

    std::unique_ptr<Texture> classic(
        drawer.createTextureFromIndexedSurfaceWithPalette(surface.get(), 0, colors, 1));
    REQUIRE(classic != nullptr);
    CHECK(classic->w == 8);
    CHECK(classic->h == 4);
    CHECK(classic->density == 1);
    clearRenderer(canvas.renderer);
    drawer.renderSprite(classic.get(), 0, 0);
    auto pixels = readPixels(canvas.renderer);
    checkPixel(pixels.get(), 0, 0, {10, 200, 30, 255});

    std::unique_ptr<Texture> hd4(
        drawer.createTextureFromIndexedSurfaceWithPalette(surface.get(), 0, colors, 4));
    REQUIRE(hd4 != nullptr);
    CHECK(hd4->w == 2);
    CHECK(hd4->h == 1);
    CHECK(hd4->density == 4);
}

TEST_CASE("P3 settings point the game packs at HD4", "[P3]")
{
    const std::filesystem::path binRoot = std::filesystem::path(D2TM_SOURCE_DIR) / "resources/bin";
    cIniFile ini((binRoot / "settings.ini").string());
    REQUIRE(ini.isLoadSuccess());
    REQUIRE(ini.hasSection("DATAFILE"));
    const std::array<std::pair<std::string, std::string>, 6> expected{{
        {"GFXDATA", "sdl_data_hd4.dat"},
        {"GFXINTER", "sdl_inter_hd4.dat"},
        {"GFXWORLD", "sdl_world_hd4.dat"},
        {"GFXMENTAT", "sdl_mentat_hd4.dat"},
        {"GFXAUDIO", "sdl_audio.dat"},
        {"GFXEDITOR", "sdl_gfxeditor.dat"},
    }};
    for (const auto &[key, value] : expected) {
        INFO("DATAFILE key: " << key);
        CHECK(ini.getStringValue("DATAFILE", key) == value);
        CHECK(std::filesystem::is_regular_file(binRoot / "data" / value));
    }
}

TEST_CASE("P3 scenes load from the HD4 folder", "[P3]")
{
    CHECK(kHd4AssetDensity == 4);
    const std::filesystem::path binRoot = std::filesystem::path(D2TM_SOURCE_DIR) / "resources/bin";
    const std::array<std::string, 16> scenes{{
        "harvest", "ix", "sardukar", "palace", "repair", "hvyftry", "headqrts", "quad",
        "ltank", "win01", "win02", "lose01", "lose02", "platr", "plhar", "plord",
    }};
    for (const auto &scene : scenes) {
        INFO("Scene: " << scene);
        const std::string relativePath = hd4SceneFile(scene);
        CHECK(relativePath == "data/scenes/hd4/sdl_" + scene + ".dat");
        CHECK(std::filesystem::is_regular_file(binRoot / relativePath));
    }
}

TEST_CASE("P3 scaleToBitmap maps the campaign map onto the click bitmap", "[P3]")
{
    CHECK(scaleToBitmap(0, 608, 2432) == 0);
    CHECK(scaleToBitmap(100, 608, 2432) == 400);
    CHECK(scaleToBitmap(607, 608, 2432) == 2428);
    CHECK(scaleToBitmap(239, 240, 960) == 956);
    CHECK(scaleToBitmap(100, 608, 608) == 100);
}
