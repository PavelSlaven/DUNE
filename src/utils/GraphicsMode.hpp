#pragma once

#include <algorithm>
#include <cctype>
#include <string>
#include <string_view>

enum class GraphicsMode {
    Classic,
    Hd
};

inline std::string graphicsModeToString(GraphicsMode mode)
{
    return mode == GraphicsMode::Hd ? "HD" : "Classic";
}

inline GraphicsMode graphicsModeFromString(std::string value)
{
    std::ranges::transform(value, value.begin(), [](unsigned char character) {
        return static_cast<char>(std::tolower(character));
    });
    return value == "classic" ? GraphicsMode::Classic : GraphicsMode::Hd;
}

inline int selectHdAssetDensity(int outputWidth, int outputHeight)
{
    return outputWidth >= 3840 || outputHeight >= 2160 ? 4 : 2;
}

inline std::string hdDataFileSection(int density)
{
    return density >= 4 ? "HD4_DATAFILE" : "HD2_DATAFILE";
}
