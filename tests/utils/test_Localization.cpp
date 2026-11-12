#include <catch2/catch_test_macros.hpp>
#include <string_view>
#include "utils/Localization.hpp"

TEST_CASE("Localization selects English for en", "[localization]")
{
    localization::setLanguage("en");
    CHECK(localization::isEnglish());
    CHECK(std::string_view(localization::text("A", "Б")) == "A");
    localization::setLanguage("ru");
}

TEST_CASE("Localization selects English for EN", "[localization]")
{
    localization::setLanguage("EN");
    CHECK(localization::isEnglish());
    CHECK(std::string_view(localization::text("A", "Б")) == "A");
    localization::setLanguage("ru");
}

TEST_CASE("Localization selects Russian for ru", "[localization]")
{
    localization::setLanguage("ru");
    CHECK_FALSE(localization::isEnglish());
    CHECK(std::string_view(localization::text("A", "Б")) == "Б");
    localization::setLanguage("ru");
}

TEST_CASE("Localization selects Russian for other languages", "[localization]")
{
    localization::setLanguage("de");
    CHECK_FALSE(localization::isEnglish());
    CHECK(std::string_view(localization::text("A", "Б")) == "Б");
    localization::setLanguage("ru");
}

TEST_CASE("Localization formats English text", "[localization]")
{
    localization::setLanguage("en");
    CHECK(localization::format("{} units", "{} юнитов", 3) == "3 units");
    localization::setLanguage("ru");
}

TEST_CASE("Localization formats Russian text", "[localization]")
{
    localization::setLanguage("ru");
    CHECK(localization::format("{} units", "{} юнитов", 3) == "3 юнитов");
    localization::setLanguage("ru");
}
