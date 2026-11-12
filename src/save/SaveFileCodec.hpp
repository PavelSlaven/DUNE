#pragma once

#include <cstddef>
#include <string>
#include <string_view>

namespace save_file {

struct DecodeResult {
    std::string body;
    std::string error;

    [[nodiscard]] bool succeeded() const {
        return error.empty();
    }
};

[[nodiscard]] std::string encode(std::string_view body, int version);

[[nodiscard]] DecodeResult decode(
    std::string_view contents,
    int expectedVersion,
    std::size_t maximumBytes
);

}
