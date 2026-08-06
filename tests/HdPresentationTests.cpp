#include "utils/HdPresentation.hpp"
#include "utils/OutcomeScreenLayout.hpp"
#include "utils/TextAlignment.hpp"

#include <array>
#include <iostream>

namespace {
bool expectEqual(const char *label, bool actual, bool expected)
{
    if (actual == expected) {
        return true;
    }
    std::cerr << label << ": got " << actual << ", expected " << expected
              << '\n';
    return false;
}
}

int main()
{
    bool passed = true;
    passed &= expectEqual(
        "HD menu uses physical presentation",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Menu),
        true
    );
    passed &= expectEqual(
        "HD gameplay uses physical presentation",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Gameplay),
        true
    );
    passed &= expectEqual(
        "HD post-House Mentat uses physical presentation",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Mentat),
        true
    );
    passed &= expectEqual(
        "Classic gameplay keeps logical presentation",
        shouldUsePhysicalHdPresentation(false, HdPresentationScene::Gameplay),
        false
    );
    passed &= expectEqual(
        "Unconverted legacy screens keep their current path",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Legacy),
        false
    );

    int frameTexture = 1;
    int fadeTexture = 2;
    HdPresentationRenderTargets<int> targets;
    targets.frame.texture = &frameTexture;
    targets.frame.setSize(2475, 1392);

    auto &fadeTarget = targets.select(true);
    fadeTarget.texture = &fadeTexture;
    fadeTarget.setSize(2048, 1152);

    passed &= expectEqual(
        "Resizing the fade target preserves the captured frame texture",
        targets.frame.texture == &frameTexture,
        true
    );
    passed &= expectEqual(
        "Frame and fade targets retain independent sizes",
        targets.frame.needsResize(2048, 1152) &&
            !targets.fade.needsResize(2048, 1152),
        true
    );

    constexpr std::array<std::array<int, 2>, 3> screenSizes{{
        {800, 600},
        {2048, 1152},
        {5120, 1440}
    }};
    for (const auto &[screenWidth, screenHeight] : screenSizes) {
        const OutcomeScreenLayout outcome = calculateOutcomeScreenLayout(
            screenWidth,
            screenHeight,
            2752,
            1536
        );
        passed &= expectEqual(
            "Outcome image fits inside the screen",
            outcome.image.getX() >= 0 &&
                outcome.image.getY() >= 0 &&
                outcome.image.getEndX() <= screenWidth &&
                outcome.image.getEndY() <= screenHeight,
            true
        );
        passed &= expectEqual(
            "Outcome prompt stays inside the image",
            outcome.prompt.getX() >= outcome.image.getX() &&
                outcome.prompt.getY() >= outcome.image.getY() &&
                outcome.prompt.getEndX() <= outcome.image.getEndX() &&
                outcome.prompt.getEndY() <= outcome.image.getEndY(),
            true
        );
        passed &= expectEqual(
            "Outcome prompt occupies the lower-right area",
            outcome.prompt.getX() >=
                outcome.image.getX() + outcome.image.getWidth() / 3 &&
                outcome.prompt.getY() >=
                outcome.image.getY() + outcome.image.getHeight() * 3 / 4,
            true
        );
        constexpr int outcomePromptFontHeight = 50;
        const int promptCenterY = outcome.prompt.getY() + outcome.prompt.getHeight() / 2;
        passed &= expectEqual(
            "50 px outcome prompt stays vertically inside the image",
            promptCenterY - outcomePromptFontHeight / 2 >= outcome.image.getY() &&
                promptCenterY + outcomePromptFontHeight / 2 <= outcome.image.getEndY(),
            true
        );
    }

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
    passed &= expectEqual(
        "Optical text alignment centers visible glyphs horizontally",
        std::abs(visibleCenterX - (textBox.getX() + textBox.getWidth() / 2.0)) <= 0.5,
        true
    );
    passed &= expectEqual(
        "Optical text alignment centers visible glyphs vertically",
        std::abs(visibleCenterY - (textBox.getY() + textBox.getHeight() / 2.0)) <= 0.5,
        true
    );
    return passed ? 0 : 1;
}
