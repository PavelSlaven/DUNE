#include <catch2/catch_test_macros.hpp>

#include "utils/Utf8.hpp"

TEST_CASE("UTF-8 helpers count and remove code points", "[utf8]")
{
    CHECK(utf8CodePointCount("Атрейдес") == 8);
    CHECK(utf8CodePointCount("abc") == 3);
    CHECK(utf8CodePointCount("") == 0);

    std::string russian = "Дюна";
    removeLastUtf8CodePoint(russian);
    CHECK(russian == "Дюн");

    std::string latin = "ab";
    removeLastUtf8CodePoint(latin);
    CHECK(latin == "a");

    std::string empty;
    removeLastUtf8CodePoint(empty);
    CHECK(empty.empty());
}
