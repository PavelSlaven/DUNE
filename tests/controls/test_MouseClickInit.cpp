#include <catch2/catch_test_macros.hpp>
#include <filesystem>
#include <fstream>
#include <string>

namespace {
std::string trim(const std::string &line)
{
    const std::size_t first = line.find_first_not_of(" \t");
    if (first == std::string::npos) return "";
    const std::size_t last = line.find_last_not_of(" \t");
    return line.substr(first, last - first + 1);
}

bool hasLine(std::ifstream &file, const std::string &expected)
{
    std::string line;
    while (std::getline(file, line)) {
        if (trim(line) == expected) return true;
    }
    return false;
}

std::filesystem::path mouseHeaderPath()
{
    return std::filesystem::path(D2TM_SOURCE_DIR) / "src/controls/cMouse.h";
}
}

TEST_CASE("P10A left button is not clicked after creation", "[P10A]")
{
    std::ifstream file(mouseHeaderPath());
    REQUIRE(file.is_open());
    REQUIRE(hasLine(file, "bool m_leftButtonClicked = false;"));
}

TEST_CASE("P10A right button is not clicked after creation", "[P10A]")
{
    std::ifstream file(mouseHeaderPath());
    REQUIRE(file.is_open());
    REQUIRE(hasLine(file, "bool m_rightButtonClicked = false;"));
}
