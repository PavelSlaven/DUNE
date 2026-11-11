#include "UiAuditArguments.hpp"

#include <cstring>

namespace uiaudit {

bool g_enabled = false;

namespace {
Options s_options;
}

const Options &options()
{
    return s_options;
}

void consumeArguments(int &argc, char **argv)
{
    s_options = Options{};
    int kept = 1;
    for (int i = 1; i < argc; i++) {
        if (std::strcmp(argv[i], "--ui-audit-list") == 0) {
            s_options.list = true;
        }
        else if (std::strcmp(argv[i], "--ui-audit-scales") == 0 && i + 1 < argc) {
            s_options.scales = argv[++i];
        }
        else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {
            s_options.scene = argv[++i];
        }
        else if (std::strcmp(argv[i], "--ui-audit-out") == 0 && i + 1 < argc) {
            s_options.outDir = argv[++i];
        }
        else if (std::strcmp(argv[i], "--ui-audit-frames") == 0 && i + 1 < argc) {
            s_options.frames = argv[++i];
        }
        else {
            argv[kept++] = argv[i];
        }
    }
    for (int i = kept; i < argc; i++) {
        argv[i] = nullptr;
    }
    argc = kept;
    g_enabled = s_options.list || !s_options.scales.empty() || (!s_options.scene.empty() && !s_options.outDir.empty());
}

}
