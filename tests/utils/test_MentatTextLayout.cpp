#include <catch2/catch_test_macros.hpp>

#include "gameobjects/mentat/MentatTextLayout.hpp"
#include "utils/Utf8.hpp"

TEST_CASE("mentat page layout keeps two short lines", "[mentat]")
{
    const auto width = [](const std::string &text) { return 10 * utf8CodePointCount(text); };
    CHECK(layoutMentatPage("abc", "de", 100, width) == std::array<std::string, 2>{"abc", "de"});
}

TEST_CASE("mentat page layout balances words and keeps the earliest tie", "[mentat]")
{
    const auto width = [](const std::string &text) { return 10 * utf8CodePointCount(text); };
    CHECK(layoutMentatPage("aaaa bbbb cccc", "", 100, width) == std::array<std::string, 2>{"aaaa", "bbbb cccc"});
    CHECK(layoutMentatPage("один два три четыре", "пять", 100, width) == std::array<std::string, 2>{"один два три", "четыре пять"});
}

TEST_CASE("mentat page layout leaves an indivisible word on the first line", "[mentat]")
{
    const auto width = [](const std::string &text) { return 10 * utf8CodePointCount(text); };
    CHECK(layoutMentatPage("word", "", 3, width) == std::array<std::string, 2>{"word", ""});
}
