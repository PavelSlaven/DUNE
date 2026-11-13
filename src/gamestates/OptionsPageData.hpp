#pragma once

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdlib>
#include <iterator>
#include <string_view>
#include <vector>

struct ResolutionOption {
    int width = 0;
    int height = 0;

    bool operator==(const ResolutionOption &) const = default;
};

[[nodiscard]] inline std::vector<ResolutionOption> resolutionChoices(
    ResolutionOption native, ResolutionOption saved)
{
    static constexpr std::array<ResolutionOption, 26> standard{{
        {3840, 2160}, {3200, 1800}, {2560, 1440}, {1920, 1080}, {1600, 900}, {1366, 768}, {1280, 720},
        {3840, 2400}, {2880, 1800}, {2560, 1600}, {1920, 1200}, {1680, 1050}, {1440, 900}, {1280, 800},
        {5120, 2160}, {3440, 1440}, {2560, 1080},
        {5120, 1440}, {3840, 1080},
        {2048, 1536}, {1600, 1200}, {1400, 1050}, {1280, 960}, {1024, 768}, {800, 600},
        {1280, 1024},
    }};
    std::vector<ResolutionOption> candidates;
    for (const ResolutionOption &option : standard) {
        const long long aspectDifference = std::abs(
            static_cast<long long>(option.width) * native.height -
            static_cast<long long>(native.width) * option.height);
        if (option.width <= native.width && option.height <= native.height &&
            option != native && option.width >= 800 && option.height >= 600 &&
            aspectDifference * 50 <= static_cast<long long>(native.width) * option.height) {
            candidates.push_back(option);
        }
    }
    std::ranges::sort(candidates, [](const ResolutionOption &left, const ResolutionOption &right) {
        const long long leftPixels = static_cast<long long>(left.width) * static_cast<long long>(left.height);
        const long long rightPixels = static_cast<long long>(right.width) * static_cast<long long>(right.height);
        if (leftPixels != rightPixels) {
            return leftPixels > rightPixels;
        }
        return left.width > right.width;
    });

    std::vector<ResolutionOption> result{native};
    for (std::size_t index = 0; index < candidates.size() && index < 5; ++index) {
        result.push_back(candidates[index]);
    }
    if (saved.width > 0 && saved.height > 0 &&
        std::find(result.begin(), result.end(), saved) == result.end()) {
        result.push_back(saved);
    }
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
