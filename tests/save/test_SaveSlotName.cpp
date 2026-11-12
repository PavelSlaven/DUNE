#include <catch2/catch_test_macros.hpp>

#include "save/SaveSlotName.hpp"
#include "utils/Utf8.hpp"

#include <string>

TEST_CASE("P8 SaveSlotName accepts slots 1 to 10 only", "[P8]")
{
    REQUIRE(save_slot::isValidSlot(1));
    REQUIRE(save_slot::isValidSlot(10));
    REQUIRE_FALSE(save_slot::isValidSlot(0));
    REQUIRE_FALSE(save_slot::isValidSlot(11));
}

TEST_CASE("P8 SaveSlotName collapses spaces and keeps Cyrillic", "[P8]")
{
    REQUIRE(save_slot::sanitizeName("  Моя   игра Ё  ") == "Моя игра Ё");
}

TEST_CASE("P8 SaveSlotName removes control characters", "[P8]")
{
    REQUIRE(save_slot::sanitizeName("Тест\n\tимени") == "Тестимени");
}

TEST_CASE("P8 removeLastUtf8CodePoint removes whole UTF-8 letters", "[P8]")
{
    std::string value = "Ёж";
    removeLastUtf8CodePoint(value);
    REQUIRE(value == "Ё");
    removeLastUtf8CodePoint(value);
    REQUIRE(value.empty());
}

TEST_CASE("P8 SaveSlotName limit keeps whole UTF-8 letters", "[P8]")
{
    std::string input;
    for (int i = 0; i < 60; ++i) {
        input += "Я";
    }
    const std::string sanitized = save_slot::sanitizeName(input);

    REQUIRE(sanitized.size() == save_slot::MaximumNameBytes);
    REQUIRE(sanitized.substr(sanitized.size() - 2) == "Я");
}
