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
    static_cast<void>(outputWidth);
    static_cast<void>(outputHeight);
    return 4;
}

inline std::string hdDataFileSection(int density)
{
    static_cast<void>(density);
    return "HD4_DATAFILE";
}
