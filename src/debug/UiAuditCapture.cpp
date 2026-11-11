#include "debug/UiAudit.hpp"

#include "debug/UiAuditScenes.hpp"

#include "game/cGame.h"
#include "game/cGameSettings.h"

#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>

#include <cstdio>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

#include "include/config.h"
#include "utils/RenderScale.hpp"
#include "utils/WorldScale.hpp"

namespace uiaudit {

namespace {

constexpr int kReadinessTimeoutFrames = 900;
constexpr int kOffscreenCursor = -300;

enum class Kind { Text, Gui, Click };

struct Entry {
    Kind kind;
    std::string label;
    Rect rect;
    bool hasBox;
    Rect box;
};

std::vector<Entry> g_entries;
std::vector<Rect> g_boxes;
const Scene *g_scene = nullptr;
bool g_failed = false;
bool g_done = false;
int g_frame = 0;
int g_settled = 0;
int g_stateAtBegin = -1;
const cGameState *g_currentStateAtBegin = nullptr;
bool g_fadeAtBegin = false;
int g_canvasW = 0;
int g_canvasH = 0;
SDL_Renderer *g_renderer = nullptr;

std::string escapeJson(const std::string &text)
{
    std::string out;
    out.reserve(text.size() + 2);
    for (const unsigned char c : text) {
        switch (c) {
            case '"': out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default:
                if (c < 0x20) {
                    char buffer[8];
                    std::snprintf(buffer, sizeof(buffer), "\\u%04x", c);
                    out += buffer;
                }
                else {
                    out += static_cast<char>(c);
                }
        }
    }
    return out;
}

std::string rectJson(const Rect &rect)
{
    return "\"x\":" + std::to_string(rect.x) + ",\"y\":" + std::to_string(rect.y) +
           ",\"w\":" + std::to_string(rect.w) + ",\"h\":" + std::to_string(rect.h);
}

void fail(const std::string &message)
{
    std::cerr << "ui-audit: " << message << '\n';
    g_failed = true;
}

void moveCursor(int x, int y)
{
    SDL_Event event{};
    event.type = SDL_EVENT_MOUSE_MOTION;
    event.motion.x = static_cast<float>(x);
    event.motion.y = static_cast<float>(y);
    SDL_PushEvent(&event);
}

bool writeGeometry(cGame &currentGame, const std::filesystem::path &path, int outputW, int outputH)
{
    std::ofstream file(path, std::ios::binary);
    if (!file) {
        return false;
    }
    file << "{\"k\":\"header\",\"scene\":\"" << escapeJson(g_scene->id) << "\",\"resolution\":\"" << outputW << 'x'
         << outputH << "\",\"language\":\"en\",\"graphics\":\"hd\",\"canvas\":{\"w\":"
         << currentGame.m_gameSettings->getScreenW() << ",\"h\":" << currentGame.m_gameSettings->getScreenH()
         << "},\"game_screen\":" << (g_scene->gameScreen ? "true" : "false")
         << ",\"render_scale\":" << UiAuditAccess::renderScale(currentGame)
         << ",\"world_scale\":" << UiAuditAccess::worldScale(currentGame)
         << ",\"version\":\"" << escapeJson(D2TM_VERSION) << "\"}\n";
    for (const Entry &entry : g_entries) {
        switch (entry.kind) {
            case Kind::Text:
                file << "{\"k\":\"text\",\"s\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
                     << ",\"box\":";
                if (entry.hasBox) {
                    file << '{' << rectJson(entry.box) << '}';
                }
                else {
                    file << "null";
                }
                file << "}\n";
                break;
            case Kind::Gui:
                file << "{\"k\":\"gui\",\"t\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
                     << "}\n";
                break;
            case Kind::Click:
                file << "{\"k\":\"click\",\"name\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
                     << "}\n";
                break;
        }
    }
    return static_cast<bool>(file);
}

bool writePng(SDL_Renderer *renderer, const std::filesystem::path &path, int &outputW, int &outputH)
{
    if (!SDL_GetRenderOutputSize(renderer, &outputW, &outputH)) {
        return false;
    }
    int logicalW = 0;
    int logicalH = 0;
    SDL_RendererLogicalPresentation logicalPresentation = SDL_LOGICAL_PRESENTATION_DISABLED;
    if (!SDL_GetRenderLogicalPresentation(renderer, &logicalW, &logicalH, &logicalPresentation)) {
        return false;
    }
    if (!SDL_SetRenderLogicalPresentation(renderer, 0, 0, SDL_LOGICAL_PRESENTATION_DISABLED)) {
        return false;
    }
    SDL_Surface *surface = SDL_RenderReadPixels(renderer, nullptr);
    bool saved = false;
    if (surface != nullptr) {
        saved = IMG_SavePNG(surface, path.string().c_str());
        SDL_DestroySurface(surface);
    }
    const bool restored = SDL_SetRenderLogicalPresentation(renderer, logicalW, logicalH, logicalPresentation);
    return saved && restored;
}

void capture(cGame &currentGame)
{
    namespace fs = std::filesystem;
    const fs::path outDir(options().outDir);
    std::error_code error;
    fs::create_directories(outDir, error);
    if (error) {
        fail("cannot create " + outDir.string());
        return;
    }
    int outputW = 0;
    int outputH = 0;
    const fs::path png = outDir / (std::string(g_scene->id) + ".png");
    if (!writePng(UiAuditAccess::renderer(currentGame), png, outputW, outputH)) {
        fail("cannot write " + png.string() + ": " + SDL_GetError());
        return;
    }
    const fs::path log = outDir / (std::string(g_scene->id) + ".geometry.jsonl");
    if (!writeGeometry(currentGame, log, outputW, outputH)) {
        fail("cannot write " + log.string());
        return;
    }
    g_done = true;
}

}

void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box)
{
    Entry entry{Kind::Text, text, {x, y, w, h}, false, {}};
    if (box != nullptr) {
        entry.hasBox = true;
        entry.box = *box;
    }
    else if (!g_boxes.empty()) {
        entry.hasBox = true;
        entry.box = g_boxes.back();
    }
    g_entries.push_back(std::move(entry));
}

void recordGui(const char *type, int x, int y, int w, int h)
{
    g_entries.push_back({Kind::Gui, type, {x, y, w, h}, false, {}});
}

void recordClick(const char *name, int x, int y, int w, int h)
{
    g_entries.push_back({Kind::Click, name, {x, y, w, h}, false, {}});
}

BoxScope::BoxScope(int x, int y, int w, int h)
{
    g_boxes.push_back({x, y, w, h});
}

BoxScope::~BoxScope()
{
    g_boxes.pop_back();
}

bool handleEarlyExit(int &exitCode)
{
    if (!options().scales.empty()) {
        int width = 0;
        int height = 0;
        if (std::sscanf(options().scales.c_str(), "%dx%d", &width, &height) != 2) {
            std::cerr << "ui-audit: bad resolution " << options().scales << '\n';
            exitCode = 2;
            return true;
        }
        std::string json = "{\"resolution\":\"" + std::to_string(width) + "x" + std::to_string(height) +
                           "\",\"render\":[0";
        for (const int scale : ManualRenderScales) {
            if (isManualRenderScaleAvailable(width, height, scale)) {
                json += "," + std::to_string(scale);
            }
        }
        json += "],\"world\":[0";
        for (const int scale : ManualWorldScales) {
            json += "," + std::to_string(scale);
        }
        json += "]}";
        std::cout << json << '\n';
        exitCode = 0;
        return true;
    }
    if (options().list) {
        std::string json = "{\"scenes\":[";
        bool first = true;
        for (const Scene &scene : catalog()) {
            if (!first) {
                json += ',';
            }
            first = false;
            json += "{\"id\":\"" + escapeJson(scene.id) + "\",\"group\":\"" + escapeJson(scene.group) +
                    "\",\"state\":\"" + escapeJson(scene.state) + "\",\"screen\":\"" + escapeJson(scene.screen) +
                    "\",\"game_screen\":" + (scene.gameScreen ? "true" : "false") + ",\"house\":\"" + escapeJson(scene.house) + "\",\"hud\":" + (scene.hud ? "true" : "false") +
                    ",\"hd_only\":" + (scene.hdOnly ? "true" : "false") + ",\"hover\":";
            json += scene.hover ? "{\"x\":" + std::to_string(scene.hoverX) + ",\"y\":" + std::to_string(scene.hoverY) + "}"
                                : std::string("null");
            json += ",\"readiness\":\"" + escapeJson(scene.readiness) + "\"}";
        }
        json += "]}";
        std::cout << json << '\n';
        exitCode = 0;
        return true;
    }
    if (findScene(options().scene) == nullptr) {
        std::cerr << "ui-audit: unknown scene " << options().scene << '\n';
        exitCode = 2;
        return true;
    }
    return false;
}

void onSetupDone(cGame &currentGame)
{
    g_scene = findScene(options().scene);
    g_entries.clear();
    g_frame = 0;
    g_settled = 0;
    g_done = false;
    currentGame.m_gameSettings->setPlayMusic(false);
    UiAuditAccess::freezeClock(currentGame);
    const bool prepared = g_scene != nullptr && g_scene->prepare(currentGame);
    UiAuditAccess::resumeClock(currentGame);
    if (!prepared) {
        fail("cannot prepare scene " + options().scene);
        currentGame.m_gameSettings->setPlaying(false);
    }
}

void beginFrame(cGame &currentGame)
{
    g_entries.clear();
    g_boxes.clear();
    ++g_frame;
    g_canvasW = currentGame.m_gameSettings->getScreenW();
    g_canvasH = currentGame.m_gameSettings->getScreenH();
    g_renderer = UiAuditAccess::renderer(currentGame);
    g_stateAtBegin = UiAuditAccess::state(currentGame);
    g_currentStateAtBegin = UiAuditAccess::currentState(currentGame);
    g_fadeAtBegin = UiAuditAccess::notFadingOut(currentGame);
    moveCursor(kOffscreenCursor, kOffscreenCursor);
}

void onFramePresented(cGame &currentGame)
{
    if (g_scene == nullptr || g_done || g_failed) {
        currentGame.m_gameSettings->setPlaying(false);
        return;
    }
    const bool stable = g_stateAtBegin == UiAuditAccess::state(currentGame) &&
                        g_currentStateAtBegin == UiAuditAccess::currentState(currentGame) &&
                        g_fadeAtBegin && UiAuditAccess::notFadingOut(currentGame);
    g_settled = stable ? g_settled + 1 : 0;
    if (g_settled >= g_scene->settleFrames && (g_scene->ready == nullptr || g_scene->ready(currentGame))) {
        capture(currentGame);
        currentGame.m_gameSettings->setPlaying(false);
        return;
    }
    if (g_frame > kReadinessTimeoutFrames) {
        fail(std::string("scene ") + g_scene->id + " was not ready after " +
             std::to_string(kReadinessTimeoutFrames) + " frames");
        currentGame.m_gameSettings->setPlaying(false);
    }
}

bool failed()
{
    return g_failed;
}

}
