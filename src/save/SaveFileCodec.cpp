#include "save/SaveFileCodec.hpp"

#include "utils/Localization.hpp"

#include <cstdint>
#include <sstream>

namespace {
constexpr std::string_view SaveMagic = "D2TM_SAVE";

std::uint64_t checksum(std::string_view data)
{
    std::uint64_t result = 1469598103934665603ULL;
    for (const unsigned char byte : data) {
        result ^= byte;
        result *= 1099511628211ULL;
    }
    return result;
}
}

namespace save_file {

std::string encode(std::string_view body, int version)
{
    std::ostringstream output;
    output << SaveMagic << ' '
           << version << ' '
           << checksum(body) << '\n'
           << body;
    return output.str();
}

DecodeResult decode(
    std::string_view contents,
    int expectedVersion,
    std::size_t maximumBytes)
{
    if (contents.size() > maximumBytes) {
        return {"", localization::text("Save file is too large", "Файл сохранения слишком большой")};
    }
    const std::size_t headerEnd = contents.find('\n');
    if (headerEnd == std::string_view::npos) {
        return {"", localization::text("Save header is corrupted", "Повреждён заголовок сохранения")};
    }

    std::istringstream header{std::string(contents.substr(0, headerEnd))};
    std::string magic;
    int version = 0;
    std::uint64_t expectedChecksum = 0;
    if (!(header >> magic >> version >> expectedChecksum) ||
        magic != SaveMagic) {
        return {"", localization::text("Save header is corrupted", "Повреждён заголовок сохранения")};
    }
    std::string extraHeaderValue;
    if (header >> extraHeaderValue) {
        return {"", localization::text("Save header is corrupted", "Повреждён заголовок сохранения")};
    }
    if (version != expectedVersion) {
        return {"", localization::text("Unsupported save version", "Неподдерживаемая версия сохранения")};
    }

    const std::string_view body = contents.substr(headerEnd + 1);
    if (checksum(body) != expectedChecksum) {
        return {"", localization::text("Save checksum does not match", "Контрольная сумма сохранения не совпадает")};
    }
    return {std::string(body), ""};
}

}
