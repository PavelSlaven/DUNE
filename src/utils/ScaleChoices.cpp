#include "utils/ScaleChoices.hpp"

#include "utils/RenderScale.hpp"
#include "utils/WorldScale.hpp"
#include "utils/Localization.hpp"

#include <algorithm>
#include <format>
#include <iterator>

std::vector<int> renderScaleChoices(int outputWidth, int outputHeight)
{
    std::vector<int> choices{AutomaticRenderScale};
    for (const int scalePercent : ManualRenderScales) {
        if (isManualRenderScaleAvailable(outputWidth, outputHeight, scalePercent)) {
            choices.push_back(scalePercent);
        }
    }
    return choices;
}

std::vector<int> worldScaleChoices()
{
    std::vector<int> choices{AutomaticWorldScale};
    choices.insert(choices.end(), ManualWorldScales.begin(), ManualWorldScales.end());
    return choices;
}

std::size_t scaleChoiceIndex(const std::vector<int> &choices, int scalePercent)
{
    const auto choice = std::find(choices.begin(), choices.end(), scalePercent);
    return choice == choices.end()
        ? 0
        : static_cast<std::size_t>(std::distance(choices.begin(), choice));
}

std::string scaleChoiceText(int scalePercent, int automaticScalePercent)
{
    return scalePercent == AutomaticRenderScale
        ? localization::format("Auto ({}%)", "Авто ({}%)", automaticScalePercent)
        : std::format("{}%", scalePercent);
}
