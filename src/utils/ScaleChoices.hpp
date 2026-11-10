#pragma once

#include <cstddef>
#include <string>
#include <vector>

[[nodiscard]] std::vector<int> renderScaleChoices(int outputWidth, int outputHeight);
[[nodiscard]] std::vector<int> worldScaleChoices();
[[nodiscard]] std::size_t scaleChoiceIndex(const std::vector<int> &choices, int scalePercent);
[[nodiscard]] std::string scaleChoiceText(int scalePercent, int automaticScalePercent);
