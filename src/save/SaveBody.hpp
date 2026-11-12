#pragma once

#include "save/SaveSnapshot.hpp"

#include <string>
#include <string_view>

namespace save_game_detail {

[[nodiscard]] std::string serializeBody(const SaveSnapshot &save);

[[nodiscard]] bool deserializeBody(std::string_view body, SaveSnapshot &save, std::string &error);

}
