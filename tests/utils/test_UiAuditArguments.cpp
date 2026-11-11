#include <catch2/catch_test_macros.hpp>

#include "debug/UiAuditArguments.hpp"

#include <string>
#include <vector>

namespace {
struct Argv {
    explicit Argv(std::vector<std::string> values) : storage(std::move(values))
    {
        for (auto &value : storage) {
            pointers.push_back(value.data());
        }
        pointers.push_back(nullptr);
        argc = static_cast<int>(storage.size());
    }

    std::vector<std::string> storage;
    std::vector<char *> pointers;
    int argc = 0;
    char **argv() { return pointers.data(); }
};

bool remaining(Argv &args, const std::vector<std::string> &expected)
{
    if (args.argc != static_cast<int>(expected.size())) {
        return false;
    }
    for (int i = 0; i < args.argc; i++) {
        if (expected[i] != args.argv()[i]) {
            return false;
        }
    }
    return true;
}
}

TEST_CASE("P5G ui audit stays off on a plain launch", "[P5G]")
{
    Argv args({"d2tm"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
    CHECK_FALSE(uiaudit::options().list);
    CHECK(remaining(args, {"d2tm"}));
}

TEST_CASE("P5G ui audit keeps ordinary game arguments", "[P5G]")
{
    Argv args({"d2tm", "-windowed", "-screenWidth", "1024", "-screenHeight", "768"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
    CHECK(remaining(args, {"d2tm", "-windowed", "-screenWidth", "1024", "-screenHeight", "768"}));
}

TEST_CASE("P5G ui audit needs a scene besides the output directory", "[P5G]")
{
    Argv args({"d2tm", "--ui-audit-out", "somewhere", "-windowed"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
    CHECK(uiaudit::options().outDir == "somewhere");
    CHECK(remaining(args, {"d2tm", "-windowed"}));
}

TEST_CASE("P5G ui audit scene and output enable the mode and are removed", "[P5G]")
{
    Argv args({"d2tm", "-windowed", "--ui-audit-scene", "main-menu", "--ui-audit-out", "out dir", "-screenWidth", "1024"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK(uiaudit::isEnabled());
    CHECK(uiaudit::options().scene == "main-menu");
    CHECK(uiaudit::options().outDir == "out dir");
    CHECK_FALSE(uiaudit::options().list);
    CHECK(remaining(args, {"d2tm", "-windowed", "-screenWidth", "1024"}));
}

TEST_CASE("P5G ui audit list enables the mode and is removed", "[P5G]")
{
    Argv args({"d2tm", "--ui-audit-list"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK(uiaudit::isEnabled());
    CHECK(uiaudit::options().list);
    CHECK(remaining(args, {"d2tm"}));
}

TEST_CASE("P5G ui audit scales enable the mode and are removed", "[P5G]")
{
    Argv args({"d2tm", "--ui-audit-scales", "1024x768", "-windowed"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK(uiaudit::isEnabled());
    CHECK(uiaudit::options().scales == "1024x768");
    CHECK_FALSE(uiaudit::options().list);
    CHECK(remaining(args, {"d2tm", "-windowed"}));
}

TEST_CASE("P5G ui audit is switched off again by a later plain launch", "[P5G]")
{
    Argv enabling({"d2tm", "--ui-audit-list"});
    uiaudit::consumeArguments(enabling.argc, enabling.argv());
    REQUIRE(uiaudit::isEnabled());
    Argv args({"d2tm"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
}
