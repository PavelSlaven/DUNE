#pragma once

enum class HdPresentationScene {
    Menu,
    Gameplay,
    Mentat,
    Legacy
};

[[nodiscard]] constexpr bool shouldUsePhysicalHdPresentation(
    bool hdGraphics,
    HdPresentationScene scene)
{
    return hdGraphics && scene != HdPresentationScene::Legacy;
}
