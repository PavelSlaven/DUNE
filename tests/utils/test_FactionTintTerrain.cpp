#include "drawers/TerrainVariation.hpp"
#include "include/Texture.hpp"
#include "include/definitions.h"
#include "utils/FactionTint.hpp"
#include "utils/Graphics.hpp"
#include "utils/HdHouseFlag.hpp"
#include "utils/HouseMaskTint.hpp"

#include <catch2/catch_test_macros.hpp>
#include <SDL3/SDL.h>

#include <array>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <memory>
#include <string>

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

void writePixel(SDL_Surface *surface, int x, SDL_Color color)
{
    auto *row = static_cast<Uint32 *>(surface->pixels);
    row[x] = SDL_MapSurfaceRGBA(surface, color.r, color.g, color.b, color.a);
}

SDL_Color readPixel(SDL_Surface *surface, int x, int y = 0)
{
    SDL_Color color{};
    SDL_ReadSurfacePixel(surface, x, y, &color.r, &color.g, &color.b, &color.a);
    return color;
}

void checkPixel(SDL_Surface *surface, int x, SDL_Color expected)
{
    INFO("Pixel x = " << x);
    const auto actual = readPixel(surface, x);
    CHECK(actual.r == expected.r);
    CHECK(actual.g == expected.g);
    CHECK(actual.b == expected.b);
    CHECK(actual.a == expected.a);
}

constexpr std::array<SDL_Color, 9> targetPixels{{
    {200, 200, 200, 255},
    {110, 110, 110, 128},
    {40, 40, 40, 0},
    {80, 90, 100, 255},
    {120, 120, 120, 255},
    {90, 90, 90, 255},
    {60, 70, 80, 255},
    {180, 180, 180, 255},
    {160, 160, 160, 255},
}};

}

TEST_CASE("P6 faction tint keeps one tone for dark and light assets", "[P6]")
{
    CHECK(applyFactionTintChannel(255, 0.40F, 0.40F) == 166);
    CHECK(applyFactionTintChannel(255, 1.20F, 1.20F) == 166);
    CHECK(applyFactionTintChannel(255, 0.40F, 0.65F) < applyFactionTintChannel(255, 0.90F, 0.65F));
    CHECK(applyFactionTintChannel(0, 1.0F, 1.0F) == 0);
}

TEST_CASE("P6 terrain variation picks deterministic variants", "[P6]")
{
    CHECK(hdTerrainVariantIndex(-1, TERRAIN_SAND) == 0);
    CHECK(hdTerrainVariantIndex(42, TERRAIN_WALL) == 0);
    CHECK(hdTerrainVariantName(TERRAIN_SAND, 0, 0) == nullptr);
    CHECK(hdTerrainVariantName(TERRAIN_SAND, 0, 5) == nullptr);
    CHECK(hdTerrainVariantName(TERRAIN_SAND, 1, 3) == nullptr);
    CHECK(
        std::strcmp(
            hdTerrainVariantName(TERRAIN_SAND, 0, 3),
            "TERRAIN_SAND_VAR_03"
        ) == 0
    );

    std::array<bool, HD_TERRAIN_VARIANT_COUNT> seen = {};
    for (int cell = 0; cell < 4096; ++cell) {
        const int first = hdTerrainVariantIndex(cell, TERRAIN_SAND);
        const int second = hdTerrainVariantIndex(cell, TERRAIN_SAND);
        CHECK(first == second);
        CHECK((first >= 0 && first < HD_TERRAIN_VARIANT_COUNT));
        seen[first] = true;
    }
    for (bool present : seen) {
        CHECK(present);
    }
}

TEST_CASE("P6 house mask target keeps fork purple for Sardaukar", "[P6]")
{
    const auto sardaukar = houseMaskTargetColor(SARDAUKAR, Color{101, 12, 101, 255});
    CHECK(sardaukar.r == 255);
    CHECK(sardaukar.g == 0);
    CHECK(sardaukar.b == 255);
    CHECK(sardaukar.a == 255);

    const std::array<int, 4> houses{{HARKONNEN, ATREIDES, ORDOS, FREMEN}};
    const std::array<Color, 4> colors{{
        {255, 0, 0, 255}, {0, 0, 255, 255}, {0, 255, 0, 255}, {194, 125, 60, 200},
    }};
    for (std::size_t i = 0; i < houses.size(); ++i) {
        INFO("House = " << houses[i]);
        const auto actual = houseMaskTargetColor(houses[i], colors[i]);
        CHECK(actual.r == colors[i].r);
        CHECK(actual.g == colors[i].g);
        CHECK(actual.b == colors[i].b);
        CHECK(actual.a == colors[i].a);
    }
}

TEST_CASE("P6 house mask tint colors only masked pixels", "[P6]")
{
    auto target = createSurface(9, 1);
    auto mask = createSurface(9, 1);
    const std::array<SDL_Color, 9> maskPixels{{
        {255, 255, 255, 255}, {255, 255, 255, 255}, {255, 255, 255, 255},
        {0, 0, 0, 0}, {128, 128, 128, 255}, {0, 0, 255, 255},
        {255, 255, 255, 0}, {253, 0, 0, 255}, {250, 250, 250, 255},
    }};
    const std::array<SDL_Color, 9> expected{{
        {229, 29, 115, 255}, {126, 16, 63, 128}, {40, 40, 40, 0},
        {80, 90, 100, 255}, {128, 68, 94, 255}, {103, 13, 52, 255},
        {60, 70, 80, 255}, {205, 27, 103, 255}, {182, 25, 93, 255},
    }};
    for (int x = 0; x < 9; ++x) {
        writePixel(target.get(), x, targetPixels[x]);
        writePixel(mask.get(), x, maskPixels[x]);
    }
    const Color houseColor{255, 32, 128, 255};
    CHECK(applyHouseMaskTint(target.get(), mask.get(), houseColor));
    for (int x = 0; x < 9; ++x) {
        checkPixel(target.get(), x, expected[x]);
    }

    auto partialTarget = createSurface(1, 1);
    auto partialMask = createSurface(1, 1);
    writePixel(partialTarget.get(), 0, {100, 100, 100, 255});
    writePixel(partialMask.get(), 0, {128, 128, 128, 255});
    CHECK(applyHouseMaskTint(partialTarget.get(), partialMask.get(), houseColor));
    checkPixel(partialTarget.get(), 0, {149, 62, 100, 255});
}

TEST_CASE("P6 house mask tint rejects unusable surfaces", "[P6]")
{
    auto target = createSurface(5, 1);
    auto narrowMask = createSurface(2, 1);
    auto tallMask = createSurface(5, 2);
    auto mask = createSurface(5, 1);
    for (int x = 0; x < 5; ++x) {
        writePixel(target.get(), x, targetPixels[x]);
    }
    for (SDL_Surface *surface : {narrowMask.get(), tallMask.get(), mask.get()}) {
        SDL_FillSurfaceRect(surface, nullptr, SDL_MapSurfaceRGBA(surface, 255, 255, 255, 255));
    }
    const Color houseColor{255, 32, 128, 255};
    CHECK(applyHouseMaskTint(target.get(), narrowMask.get(), houseColor) == false);
    CHECK(applyHouseMaskTint(target.get(), tallMask.get(), houseColor) == false);
    CHECK(applyHouseMaskTint(nullptr, mask.get(), houseColor) == false);
    CHECK(applyHouseMaskTint(target.get(), nullptr, houseColor) == false);
    for (int x = 0; x < 5; ++x) {
        checkPixel(target.get(), x, targetPixels[x]);
    }

    auto argbTarget = createSurface(5, 1, SDL_PIXELFORMAT_ARGB8888);
    for (int x = 0; x < 5; ++x) {
        writePixel(argbTarget.get(), x, targetPixels[x]);
    }
    CHECK(applyHouseMaskTint(argbTarget.get(), mask.get(), houseColor) == false);
    for (int x = 0; x < 5; ++x) {
        checkPixel(argbTarget.get(), x, targetPixels[x]);
    }
}

TEST_CASE("P6 HD house flags cover twelve buildings", "[P6]")
{
    const std::array<HdHouseFlag, 12> expected{{
        {RADAR, "BUILD_RADAR_FLAG", 64, 64},
        {BARRACKS, "BUILD_BARRACKS_FLAG", 64, 64},
        {WOR, "BUILD_WOR_FLAG", 64, 64},
        {REFINERY, "BUILD_REFINERY_FLAG", 96, 64},
        {WINDTRAP, "BUILD_WINDTRAP_FLAG", 64, 64},
        {SILO, "BUILD_SILO_FLAG", 64, 64},
        {STARPORT, "BUILD_STARPORT_FLAG", 96, 96},
        {PALACE, "BUILD_PALACE_FLAG", 96, 96},
        {IX, "BUILD_IX_FLAG", 64, 64},
        {LIGHTFACTORY, "BUILD_LIGHTFACTORY_FLAG", 64, 64},
        {HIGHTECH, "BUILD_HIGHTECH_FLAG", 96, 64},
        {CONSTYARD, "BUILD_CONSTYARD_FLAG", 64, 64},
    }};
    for (const auto &entry : expected) {
        INFO("Structure = " << entry.structureType);
        const auto *actual = findHdHouseFlag(entry.structureType);
        REQUIRE(actual != nullptr);
        CHECK(actual->structureType == entry.structureType);
        CHECK(std::string(actual->textureName) == entry.textureName);
        CHECK(actual->frameWidth == entry.frameWidth);
        CHECK(actual->frameHeight == entry.frameHeight);
    }
    for (int t = -1; t <= 30; ++t) {
        bool listed = false;
        for (const auto &entry : expected) {
            if (entry.structureType == t) {
                listed = true;
                break;
            }
        }
        if (!listed) {
            INFO("Structure = " << t);
            CHECK(findHdHouseFlag(t) == nullptr);
        }
    }
}

TEST_CASE("P6 Graphics creates house textures from HD4 masks", "[P6]")
{
    const std::filesystem::path packPath =
        std::filesystem::path(D2TM_SOURCE_DIR) / "resources/bin/data/sdl_data_hd4.dat";
    std::ifstream packFile(packPath, std::ios::binary);
    REQUIRE(packFile.is_open());
    std::string firstLine;
    std::getline(packFile, firstLine);
    if (!firstLine.empty() && firstLine.back() == '\r') {
        firstLine.pop_back();
    }
    if (firstLine == "version https://git-lfs.github.com/spec/v1") {
        SKIP("HD4 pack is a Git LFS pointer: sdl_data_hd4.dat");
    }

    SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy");
    REQUIRE(SDL_Init(SDL_INIT_VIDEO));
    SoftwareRenderer canvas(1024, 128);
    Graphics gfx(canvas.renderer, packPath.string(), 4);
    SDL_Surface *quad = gfx.getSurface("UNIT_QUAD");
    REQUIRE(quad != nullptr);
    REQUIRE(quad->w == 1024);
    REQUIRE(quad->h == 128);
    Surface original(SDL_ConvertSurface(quad, SDL_PIXELFORMAT_RGBA32), SDL_DestroySurface);
    REQUIRE(original != nullptr);
    const std::array<Color, 2> colors{{{255, 0, 255, 255}, {0, 255, 0, 255}}};
    for (const Color &color : colors) {
        INFO("House color = " << int(color.r) << ", " << int(color.g) << ", " << int(color.b));
        std::unique_ptr<Texture> tinted(gfx.createHouseTexture(quad, color));
        REQUIRE(tinted != nullptr);
        CHECK(tinted->pixelW == 1024);
        CHECK(tinted->pixelH == 128);
        CHECK(tinted->density == 4);
        SDL_ScaleMode scaleMode{};
        SDL_GetTextureScaleMode(tinted->tex.get(), &scaleMode);
        CHECK(scaleMode == SDL_SCALEMODE_LINEAR);

        Surface expected(SDL_ConvertSurface(quad, SDL_PIXELFORMAT_RGBA32), SDL_DestroySurface);
        REQUIRE(expected != nullptr);
        REQUIRE(applyHouseMaskTint(expected.get(), gfx.getSurface("HM_UNIT_QUAD"), color));
        SDL_SetTextureBlendMode(tinted->tex.get(), SDL_BLENDMODE_NONE);
        SDL_SetRenderDrawColor(canvas.renderer, 0, 0, 0, 0);
        SDL_RenderClear(canvas.renderer);
        SDL_RenderTexture(canvas.renderer, tinted->tex.get(), nullptr, nullptr);
        Surface shot(SDL_RenderReadPixels(canvas.renderer, nullptr), SDL_DestroySurface);
        REQUIRE(shot != nullptr);

        int opaquePixels = 0;
        int mismatchedPixels = 0;
        int changedPixels = 0;
        for (int y = 0; y < expected->h; ++y) {
            for (int x = 0; x < expected->w; ++x) {
                const auto wanted = readPixel(expected.get(), x, y);
                if (wanted.a != 255) {
                    continue;
                }
                ++opaquePixels;
                const auto actual = readPixel(shot.get(), x, y);
                const auto source = readPixel(original.get(), x, y);
                if (actual.r != wanted.r || actual.g != wanted.g || actual.b != wanted.b) {
                    ++mismatchedPixels;
                }
                if (source.r != wanted.r || source.g != wanted.g || source.b != wanted.b) {
                    ++changedPixels;
                }
            }
        }
        REQUIRE(opaquePixels > 0);
        CHECK(mismatchedPixels == 0);
        CHECK(changedPixels > 0);
    }

    SDL_Surface *sand = gfx.getSurface("TERRAIN_SAND");
    REQUIRE(sand != nullptr);
    CHECK(gfx.createHouseTexture(sand, Color{255, 0, 255, 255}) == nullptr);
    Texture *flag = gfx.getHouseTexture("BUILD_WINDTRAP_FLAG", SARDAUKAR, Color{255, 0, 255, 255});
    REQUIRE(flag != nullptr);
    CHECK(gfx.getHouseTexture("BUILD_WINDTRAP_FLAG", SARDAUKAR, Color{255, 0, 255, 255}) == flag);
    CHECK(gfx.getHouseTexture("BUILD_WINDTRAP_FLAG", SARDAUKAR, Color{0, 255, 0, 255}) == flag);
    CHECK(gfx.getHouseTexture("BUILD_WINDTRAP_FLAG", ATREIDES, Color{0, 0, 255, 255}) != flag);
    CHECK(flag != gfx.getTexture("BUILD_WINDTRAP_FLAG"));
    CHECK(gfx.getHouseTexture("TERRAIN_SAND", SARDAUKAR, Color{255, 0, 255, 255}) == gfx.getTexture("TERRAIN_SAND"));
    CHECK(gfx.getHouseTexture("P6_NO_SUCH_ENTRY", SARDAUKAR, Color{255, 0, 255, 255}) == nullptr);
}
