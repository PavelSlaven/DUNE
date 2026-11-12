#include "gameobjects/mentat/MentatTextLayout.hpp"

#include <algorithm>
#include <sstream>
#include <vector>

std::array<std::string, 2> layoutMentatPage(const std::string &first, const std::string &second, int availableWidth,
                                            const std::function<int(const std::string &)> &textWidth)
{
    if (textWidth(first) <= availableWidth && textWidth(second) <= availableWidth) {
        return {first, second};
    }

    std::istringstream input(first + " " + second);
    std::vector<std::string> words;
    std::string word;
    while (input >> word) {
        words.push_back(word);
    }

    if (words.size() < 2) {
        return {words.empty() ? std::string{} : words.front(), ""};
    }

    std::array<std::string, 2> best;
    int bestWidth = 0;
    for (std::size_t k = 1; k < words.size(); ++k) {
        std::string left;
        std::string right;
        for (std::size_t i = 0; i < words.size(); ++i) {
            std::string &line = i < k ? left : right;
            if (!line.empty()) {
                line += ' ';
            }
            line += words[i];
        }

        const int width = std::max(textWidth(left), textWidth(right));
        if (k == 1 || width < bestWidth) {
            best = {left, right};
            bestWidth = width;
        }
    }

    return best;
}
