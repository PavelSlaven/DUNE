#include "debug/UiAuditArguments.hpp"

#include <iostream>
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

int fail(const char *message)
{
    std::cerr << message << '\n';
    return 1;
}

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

int main()
{
    {
        Argv args({"d2tm"});
        uiaudit::consumeArguments(args.argc, args.argv());
        if (uiaudit::isEnabled() || uiaudit::options().list) {
            return fail("The mode must be off without its argument");
        }
        if (!remaining(args, {"d2tm"})) {
            return fail("No argument may be consumed from a plain launch");
        }
    }
    {
        Argv args({"d2tm", "-windowed", "-screenWidth", "1024", "-screenHeight", "768"});
        uiaudit::consumeArguments(args.argc, args.argv());
        if (uiaudit::isEnabled()) {
            return fail("Ordinary game arguments must not enable the mode");
        }
        if (!remaining(args, {"d2tm", "-windowed", "-screenWidth", "1024", "-screenHeight", "768"})) {
            return fail("Ordinary game arguments must stay untouched");
        }
    }
    {
        Argv args({"d2tm", "--ui-audit-out", "somewhere", "-windowed"});
        uiaudit::consumeArguments(args.argc, args.argv());
        if (uiaudit::isEnabled()) {
            return fail("The output directory alone must not enable the mode");
        }
    }
    {
        Argv args({"d2tm", "-windowed", "--ui-audit-scene", "main-menu",
                   "--ui-audit-out", "out dir", "-screenWidth", "1024"});
        uiaudit::consumeArguments(args.argc, args.argv());
        if (!uiaudit::isEnabled() || uiaudit::options().scene != "main-menu" ||
            uiaudit::options().outDir != "out dir" || uiaudit::options().list) {
            return fail("The scene and output arguments must enable the mode");
        }
        if (!remaining(args, {"d2tm", "-windowed", "-screenWidth", "1024"})) {
            return fail("Mode arguments must be removed and the others kept in order");
        }
    }
    {
        Argv args({"d2tm", "--ui-audit-list"});
        uiaudit::consumeArguments(args.argc, args.argv());
        if (!uiaudit::isEnabled() || !uiaudit::options().list) {
            return fail("The list argument must enable the mode");
        }
        if (!remaining(args, {"d2tm"})) {
            return fail("The list argument must be removed");
        }
    }
    {
        Argv args({"d2tm"});
        uiaudit::consumeArguments(args.argc, args.argv());
        if (uiaudit::isEnabled()) {
            return fail("A later plain launch must switch the mode off again");
        }
    }
    return 0;
}
