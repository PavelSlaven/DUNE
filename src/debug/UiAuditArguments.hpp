#pragma once

#include <string>

namespace uiaudit {

struct Options {
    bool list = false;
    std::string scales;
    std::string scene;
    std::string outDir;
    std::string frames;
    std::string language;
};

extern bool g_enabled;

void consumeArguments(int &argc, char **argv);
const Options &options();

inline bool isEnabled()
{
    return g_enabled;
}

}
