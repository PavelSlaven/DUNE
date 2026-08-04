#pragma once

#include <algorithm>
#include <cstddef>
#include <string>
#include <string_view>

#include "utils/Localization.hpp"

namespace save_slot {

constexpr int MaximumSlots = 10;
constexpr std::size_t MaximumNameBytes = 96;

[[nodiscard]] inline bool isValidSlot(int slot)
{
    return slot >= 1 && slot <= MaximumSlots;
}

inline void removeLastUtf8Character(std::string &value)
{
    if (value.empty()) {
        return;
    }
    std::size_t start = value.size() - 1;
    while (start > 0 &&
           (static_cast<unsigned char>(value[start]) & 0xC0U) == 0x80U) {
        --start;
    }
    value.resize(start);
}

[[nodiscard]] inline std::string sanitizeName(std::string_view input)
{
    std::string result;
    result.reserve(std::min(input.size(), MaximumNameBytes));
    bool pendingSpace = false;
    for (std::size_t index = 0; index < input.size();) {
        const unsigned char character =
            static_cast<unsigned char>(input[index]);
        if (character < 0x20U || character == 0x7FU) {
            ++index;
            continue;
        }
        if (character == ' ') {
            pendingSpace = !result.empty();
            ++index;
            continue;
        }
        std::size_t characterBytes = 1;
        if ((character & 0xE0U) == 0xC0U) {
            characterBytes = 2;
        }
        else if ((character & 0xF0U) == 0xE0U) {
            characterBytes = 3;
        }
        else if ((character & 0xF8U) == 0xF0U) {
            characterBytes = 4;
        }
        if (index + characterBytes > input.size()) {
            break;
        }
        bool validCharacter = characterBytes == 1;
        if (characterBytes > 1) {
            validCharacter = true;
            for (std::size_t byte = 1; byte < characterBytes; ++byte) {
                if ((static_cast<unsigned char>(input[index + byte]) &
                     0xC0U) != 0x80U) {
                    validCharacter = false;
                    break;
                }
            }
        }
        if (!validCharacter) {
            ++index;
            continue;
        }
        if (pendingSpace) {
            if (result.size() + 1 > MaximumNameBytes) {
                break;
            }
            result.push_back(' ');
            pendingSpace = false;
        }
        if (result.size() + characterBytes > MaximumNameBytes) {
            break;
        }
        result.append(input.substr(index, characterBytes));
        index += characterBytes;
    }
    return result;
}

[[nodiscard]] inline std::string defaultName(int slot)
{
    return std::string(localization::text("Save ", "Сохранение ")) +
           std::to_string(slot);
}

}
