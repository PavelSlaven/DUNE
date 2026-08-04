#include "audio/MusicTransitionPolicy.hpp"

int main()
{
    const bool valid =
        !shouldAdvanceRepeatedMusicCategory(true, true) &&
        !shouldAdvanceRepeatedMusicCategory(true, false) &&
        shouldAdvanceRepeatedMusicCategory(false, false);
    return valid ? 0 : 1;
}
