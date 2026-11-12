#pragma once

#include <algorithm>
#include <array>
#include <cstddef>
#include <iterator>
#include <string_view>
#include <vector>

struct ResolutionOption {
    int width = 0;
    int height = 0;

    bool operator==(const ResolutionOption &) const = default;
};

[[nodiscard]] inline std::vector<ResolutionOption> resolutionChoices(
    int desktopWidth, int desktopHeight, ResolutionOption saved)
{
    static constexpr std::array<ResolutionOption, 35> standard{{
        {800, 600}, {1024, 600}, {1024, 768}, {1152, 864}, {1280, 720}, {1280, 768}, {1280, 800}, {1280, 960},
        {1280, 1024}, {1360, 768}, {1366, 768}, {1440, 900}, {1600, 900}, {1600, 1024}, {1600, 1200},
        {1680, 1050}, {1920, 1080}, {1920, 1200}, {2048, 1080}, {2048, 1152}, {2048, 1536}, {2560, 1080},
        {2560, 1440}, {2560, 1600}, {2880, 1620}, {2880, 1800}, {3200, 1800}, {3440, 1440}, {3840, 1600},
        {3840, 2160}, {4096, 2160}, {5120, 1440}, {5120, 2160}, {5120, 2880}, {7680, 4320},
    }};
    std::vector<ResolutionOption> result;
    const auto add = [&result](ResolutionOption option) {
        if (std::find(result.begin(), result.end(), option) == result.end()) {
            result.push_back(option);
        }
    };
    for (const ResolutionOption &option : standard) {
        if (option.width <= desktopWidth && option.height <= desktopHeight) {
            add(option);
        }
    }
    add(saved);
    add({desktopWidth, desktopHeight});
    std::ranges::sort(result, [](const ResolutionOption &left, const ResolutionOption &right) {
        const long long leftPixels = static_cast<long long>(left.width) * static_cast<long long>(left.height);
        const long long rightPixels = static_cast<long long>(right.width) * static_cast<long long>(right.height);
        if (leftPixels != rightPixels) {
            return leftPixels < rightPixels;
        }
        if (left.width != right.width) {
            return left.width < right.width;
        }
        return left.height < right.height;
    });
    return result;
}

[[nodiscard]] inline std::size_t resolutionChoiceIndex(const std::vector<ResolutionOption> &choices, ResolutionOption selected)
{
    const auto found = std::find(choices.begin(), choices.end(), selected);
    return found == choices.end() ? 0 : static_cast<std::size_t>(std::distance(choices.begin(), found));
}

[[nodiscard]] constexpr int optionsVisibleRows(int listTop, int listBottom, int rowStride)
{
    return rowStride > 0 && listBottom > listTop ? std::max(1, (listBottom - listTop) / rowStride) : 1;
}

[[nodiscard]] constexpr int optionsMaxScrollRow(int totalRows, int visibleRows)
{
    return std::max(0, totalRows - visibleRows);
}

[[nodiscard]] constexpr int optionsClampScrollRow(int scrollRow, int totalRows, int visibleRows)
{
    return std::clamp(scrollRow, 0, optionsMaxScrollRow(totalRows, visibleRows));
}

inline constexpr std::array<std::string_view, 6> MAIN_PAGE_KEYS = {
    "RenderScale", "WorldScale", "Language", "ScreenWidth", "ScreenHeight", "FullScreen",
};

inline constexpr std::array<std::string_view, 7> GAMEPLAY_PAGE_KEYS = {
    "CameraEdgeMove", "CameraBorderOrKeyMoveSpeed", "CameraDragMoveSpeed", "pauseWhenLosingFocus",
    "AllowRepeatingReinforcements", "AllTurretsDownOnLowPower", "RocketTurretsDownOnLowPower",
};

inline constexpr std::array<std::string_view, 8> DIAGNOSTICS_PAGE_KEYS = {
    "Debug", "NoAI", "oneAi", "disableWormAi", "disableReinforcements", "noAiRest", "drawUnitDebug", "drawUsages",
};
