#pragma once

enum class HdPresentationScene {
    Menu,
    Gameplay,
    Mentat,
    Legacy
};

template<typename Target>
struct HdPresentationRenderTargetSlot {
    Target *texture = nullptr;
    int width = 0;
    int height = 0;

    [[nodiscard]] constexpr bool needsResize(
        int requestedWidth,
        int requestedHeight) const
    {
        return width != requestedWidth || height != requestedHeight;
    }

    constexpr void setSize(int requestedWidth, int requestedHeight)
    {
        width = requestedWidth;
        height = requestedHeight;
    }
};

template<typename Target>
struct HdPresentationRenderTargets {
    HdPresentationRenderTargetSlot<Target> frame;
    HdPresentationRenderTargetSlot<Target> fade;

    [[nodiscard]] constexpr HdPresentationRenderTargetSlot<Target> &select(
        bool fadeTarget)
    {
        return fadeTarget ? fade : frame;
    }
};

[[nodiscard]] constexpr bool shouldUsePhysicalHdPresentation(
    bool hdGraphics,
    HdPresentationScene scene)
{
    return hdGraphics && scene != HdPresentationScene::Legacy;
}
