#pragma once

#include <string>
#include <string_view>

inline int utf8CodePointCount(std::string_view text)
{
    int count = 0;
    for (char byte : text) {
        if ((static_cast<unsigned char>(byte) & 0xC0U) != 0x80U) {
            ++count;
        }
    }
    return count;
}

inline void removeLastUtf8CodePoint(std::string &text)
{
    if (text.empty()) {
        return;
    }
    std::size_t position = text.size() - 1;
    while (position > 0 &&
           (static_cast<unsigned char>(text[position]) & 0xC0U) == 0x80U) {
        --position;
    }
    text.erase(position);
}
