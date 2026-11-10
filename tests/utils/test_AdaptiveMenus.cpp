#include "gamestates/CampaignMapLayout.hpp"
#include "include/Texture.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "utils/OutcomeScreenLayout.hpp"
#include "utils/TextAlignment.hpp"

#include <catch2/catch_test_macros.hpp>

#include <array>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <string>

TEST_CASE("P5A campaign map layout fits each canvas", "[P5A]")
{
    constexpr std::array<std::array<int, 2>, 6> resolutions{{
        {{800, 600}},
        {{1067, 600}},
        {{1280, 720}},
        {{1920, 1080}},
        {{2133, 600}},
        {{3413, 960}}
    }};

    for (const auto &resolution : resolutions) {
        INFO("Холст: " << resolution[0] << 'x' << resolution[1]);
        const auto layout = CampaignMapLayout::create(
            resolution[0],
            resolution[1]
        );
        CHECK(layout.panel.getX() >= 0);
        CHECK(layout.panel.getY() >= 0);
        CHECK(layout.panel.getEndX() <= resolution[0]);
        CHECK(layout.panel.getEndY() <= resolution[1]);
        CHECK(layout.map.getWidth() >= 320);
        CHECK(layout.map.getHeight() >= 126);
        CHECK(layout.title.getEndY() <= layout.map.getY());
        CHECK(layout.map.getEndY() <= layout.message.getY());
        CHECK(layout.message.getEndY() <= layout.missionButton.getY());

        const auto wholeMap = layout.regionDestination(
            CampaignMapLayout::SourceMapX,
            CampaignMapLayout::SourceMapY,
            CampaignMapLayout::SourceMapWidth,
            CampaignMapLayout::SourceMapHeight
        );
        CHECK(wholeMap.getX() == layout.map.getX());
        CHECK(wholeMap.getY() == layout.map.getY());
        CHECK(wholeMap.getWidth() == layout.map.getWidth());
        CHECK(wholeMap.getHeight() == layout.map.getHeight());

        CHECK(layout.clickMapX(layout.map.getX(), 608) == 0);
        CHECK(layout.clickMapY(layout.map.getY(), 240) == 0);
        CHECK(layout.clickMapX(layout.map.getEndX(), 608) == 607);
        CHECK(layout.clickMapY(layout.map.getEndY(), 240) == 239);
    }
}

TEST_CASE("P5A outcome layout keeps the image and the prompt inside the canvas", "[P5A]")
{
    constexpr std::array<std::array<int, 2>, 6> screenSizes{{
        {800, 600},
        {1067, 600},
        {2048, 1152},
        {2133, 600},
        {3413, 960},
        {5120, 1440}
    }};
    for (const auto &[screenWidth, screenHeight] : screenSizes) {
        INFO("Холст: " << screenWidth << 'x' << screenHeight);
        const OutcomeScreenLayout outcome = calculateOutcomeScreenLayout(
            screenWidth,
            screenHeight,
            2752,
            1536
        );
        CHECK((outcome.image.getX() >= 0 &&
              outcome.image.getY() >= 0 &&
              outcome.image.getEndX() <= screenWidth &&
              outcome.image.getEndY() <= screenHeight));
        CHECK((outcome.prompt.getX() >= outcome.image.getX() &&
              outcome.prompt.getY() >= outcome.image.getY() &&
              outcome.prompt.getEndX() <= outcome.image.getEndX() &&
              outcome.prompt.getEndY() <= outcome.image.getEndY()));
        const int promptCenterX = outcome.prompt.getX() + outcome.prompt.getWidth() / 2;
        const int imageCenterX = outcome.image.getX() + outcome.image.getWidth() / 2;
        CHECK((std::abs(promptCenterX - imageCenterX) <= 1 &&
              outcome.prompt.getY() >=
              outcome.image.getY() + outcome.image.getHeight() * 3 / 4));
        constexpr int widePromptTextWidth = 2000;
        const OutcomeScreenLayout widePrompt = calculateOutcomeScreenLayout(
            screenWidth,
            screenHeight,
            2752,
            1536,
            widePromptTextWidth
        );
        CHECK(widePromptTextWidth * widePrompt.promptTextScale <=
              widePrompt.image.getWidth() - 24 + 0.5F);
        constexpr int outcomePromptFontHeight = 50;
        const int promptCenterY = outcome.prompt.getY() + outcome.prompt.getHeight() / 2;
        CHECK((promptCenterY - outcomePromptFontHeight / 2 >= outcome.image.getY() &&
               promptCenterY + outcomePromptFontHeight / 2 <= outcome.image.getEndY()));
    }
}

TEST_CASE("P5A optical text alignment centers visible glyphs", "[P5A]")
{
    const cRectangle textBox(100, 50, 300, 100);
    const TextInkBounds asymmetricInk{100, 40, 10, 3, 75, 25};
    const cPoint textOrigin = calculateOpticallyCenteredTextOrigin(
        textBox,
        200,
        80,
        asymmetricInk
    );
    const double visibleCenterX = textOrigin.x +
        (asymmetricInk.x + asymmetricInk.width / 2.0) * 200.0 /
        asymmetricInk.textureWidth;
    const double visibleCenterY = textOrigin.y +
        (asymmetricInk.y + asymmetricInk.height / 2.0) * 80.0 /
        asymmetricInk.textureHeight;
    CHECK(std::abs(visibleCenterX - (textBox.getX() + textBox.getWidth() / 2.0)) <= 0.5);
    CHECK(std::abs(visibleCenterY - (textBox.getY() + textBox.getHeight() / 2.0)) <= 0.5);
}

TEST_CASE("P5A HD UI loader reads a fork picture at density 4", "[P5A]")
{
    const auto logoPath = std::filesystem::path(D2TM_SOURCE_DIR) /
        "resources/bin/data/hd4/main_menu_logo.png";
    std::ifstream logoFile(logoPath, std::ios::binary);
    std::string firstLine;
    std::getline(logoFile, firstLine);
    if (!firstLine.empty() && firstLine.back() == '\r') {
        firstLine.pop_back();
    }
    if (firstLine == "version https://git-lfs.github.com/spec/v1") {
        SKIP("HD-картинка интерфейса является указателем Git LFS: " << logoPath.string());
    }

    struct Resources {
        std::filesystem::path previousDirectory = std::filesystem::current_path();
        SDL_Surface *target = nullptr;
        SDL_Renderer *renderer = nullptr;
        Texture *logo = nullptr;

        ~Resources()
        {
            delete logo;
            SDL_DestroyRenderer(renderer);
            SDL_DestroySurface(target);
            std::filesystem::current_path(previousDirectory);
        }
    } resources;

    SDL_Surface *target = SDL_CreateSurface(16, 16, SDL_PIXELFORMAT_RGBA8888);
    resources.target = target;
    REQUIRE(target != nullptr);
    SDL_Renderer *renderer = SDL_CreateSoftwareRenderer(target);
    resources.renderer = renderer;
    REQUIRE(renderer != nullptr);

    std::filesystem::current_path(std::filesystem::path(D2TM_SOURCE_DIR) / "resources/bin");
    Texture *logo = loadHdUiTexture(renderer, "main_menu_logo.png");
    resources.logo = logo;
    REQUIRE(logo != nullptr);
    CHECK(logo->density == 4);
    CHECK(logo->pixelW == logo->w * 4);
    CHECK(logo->pixelH == logo->h * 4);
    CHECK(logo->w > 0);
    CHECK(logo->h > 0);
    CHECK(loadHdUiTexture(renderer, "p5a_missing_picture.png") == nullptr);
    CHECK(loadHdUiTexture(nullptr, "main_menu_logo.png") == nullptr);
}
