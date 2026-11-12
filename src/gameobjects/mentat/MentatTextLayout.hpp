#pragma once

#include <array>
#include <functional>
#include <string>

// the 640 pixel mentat screen less the 17 pixel text inset on each side
inline constexpr int MENTAT_TEXT_WIDTH = 606;

std::array<std::string, 2> layoutMentatPage(const std::string &first, const std::string &second, int availableWidth,
                                            const std::function<int(const std::string &)> &textWidth);
