#include <catch2/catch_test_macros.hpp>

#include "save/SaveFileCodec.hpp"
#include "save/SaveGameManager.hpp"
#include "utils/Localization.hpp"

namespace {
const std::string body = "META 0 1 0\nTEXT Проверка Ёжик\nEND\n";
}

TEST_CASE("P8 SaveFileCodec round trip keeps the body", "[P8]")
{
    const std::string encoded = save_file::encode(body, 1);
    const auto decoded = save_file::decode(encoded, 1, 1024);

    REQUIRE(decoded.succeeded());
    REQUIRE(decoded.body == body);
}

TEST_CASE("P8 SaveFileCodec rejects a wrong checksum", "[P8]")
{
    std::string encoded = save_file::encode(body, 1);
    encoded.back() = static_cast<char>(encoded.back() ^ 1);

    REQUIRE_FALSE(save_file::decode(encoded, 1, 1024).succeeded());
}

TEST_CASE("P8 SaveFileCodec rejects another version", "[P8]")
{
    const std::string encoded = save_file::encode(body, 1);

    REQUIRE_FALSE(save_file::decode(encoded, 2, 1024).succeeded());
}

TEST_CASE("P8 SaveFileCodec rejects a broken header", "[P8]")
{
    REQUIRE_FALSE(save_file::decode("D2TM_SAVE", 1, 1024).succeeded());
}

TEST_CASE("P8 SaveFileCodec rejects a file over the size limit", "[P8]")
{
    const std::string encoded = save_file::encode(body, 1);

    REQUIRE_FALSE(save_file::decode(encoded, 1, 4).succeeded());
}

TEST_CASE("P8 format version 3 rejects version 2 files", "[P8]")
{
    REQUIRE(SaveGameManager::FormatVersion == 3);

    const std::string encoded = save_file::encode(body, SaveGameManager::FormatVersion);
    REQUIRE(encoded.starts_with("D2TM_SAVE 3 "));
    REQUIRE(save_file::decode(encoded, 3, 1024).succeeded());

    const auto oldVersion = save_file::decode(
        save_file::encode(body, 2), SaveGameManager::FormatVersion, 1024);
    REQUIRE_FALSE(oldVersion.succeeded());
    REQUIRE(oldVersion.error == localization::text(
        "Unsupported save version", "Неподдерживаемая версия сохранения"));
}
