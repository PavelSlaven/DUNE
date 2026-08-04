#pragma once

[[nodiscard]] constexpr bool shouldAdvanceRepeatedMusicCategory(
    bool repeatedCategory,
    bool /*playingState*/)
{
    return !repeatedCategory;
}
