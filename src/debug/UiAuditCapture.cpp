#include "debug/UiAudit.hpp"

#include "debug/UiAuditScenes.hpp"

#include "game/cGame.h"
#include "game/cGameSettings.h"

#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>

#include <algorithm>
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

enum class Kind { Text, Gui, Click, Credit, Area, Label };

struct Entry {
    Kind kind;
    std::string label;
    Rect rect;
    bool hasBox;
    Rect box;
    std::string name;
    int obj;
};

std::vector<Entry> g_entries;
std::vector<Rect> g_boxes;
const Scene *g_scene = nullptr;
int g_hoverX = 0;
int g_hoverY = 0;
bool g_failed = false;
bool g_done = false;
int g_frame = 0;
int g_settled = 0;
int g_stateAtBegin = -1;
const cGameState *g_currentStateAtBegin = nullptr;
bool g_fadeAtBegin = false;
bool g_clipText = false;
int g_canvasW = 0;
int g_canvasH = 0;
SDL_Renderer *g_renderer = nullptr;
bool g_collecting = false;
bool g_collected = false;
Rect g_union{0, 0, 0, 0};

Rect clipped(const Rect &rect)
{
    if (g_renderer == nullptr || !SDL_RenderClipEnabled(g_renderer)) {
        return rect;
    }
    SDL_Rect clip{};
    SDL_GetRenderClipRect(g_renderer, &clip);
    const int left = std::max(rect.x, clip.x);
    const int top = std::max(rect.y, clip.y);
    const int right = std::min(rect.x + rect.w, clip.x + clip.w);
    const int bottom = std::min(rect.y + rect.h, clip.y + clip.h);
    return {left, top, std::max(0, right - left), std::max(0, bottom - top)};
}

const char *unitTypeName(int unitType)
{
    switch (unitType) {
        case 0: return "SOLDIER";
        case 1: return "TROOPER";
        case 2: return "INFANTRY";
        case 3: return "TROOPERS";
        case 4: return "TRIKE";
        case 5: return "RAIDER";
        case 6: return "QUAD";
        case 7: return "TANK";
        case 8: return "LAUNCHER";
        case 9: return "SIEGETANK";
        case 10: return "DEVASTATOR";
        case 11: return "DEVIATOR";
        case 12: return "SONICTANK";
        case 13: return "HARVESTER";
        case 14: return "MCV";
        case 15: return "CARRYALL";
        case 16: return "ORNITHOPTER";
        case 17: return "SANDWORM";
        case 19: return "SABOTEUR";
        case 20: return "UNIT_FREMEN_ONE";
        case 21: return "UNIT_FREMEN_THREE";
        case 29: return "FRIGATE";
        default: return "UNIT";
    }
}

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

void moveCursor(float x, float y)
{
    SDL_Event event{};
    event.type = SDL_EVENT_MOUSE_MOTION;
    event.motion.x = x;
    event.motion.y = y;
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
         << ",\"world_scale\":" << UiAuditAccess::worldScale(currentGame);
    int viewX = 0;
    int viewY = 0;
    int viewW = 0;
    int viewH = 0;
    if (g_scene->gameScreen && UiAuditAccess::mapViewport(currentGame, viewX, viewY, viewW, viewH)) {
        file << ",\"map_viewport\":{" << rectJson({viewX, viewY, viewW, viewH}) << '}';
    }
    file << ",\"version\":\"" << escapeJson(D2TM_VERSION) << "\"}\n";
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
            case Kind::Area:
                file << "{\"k\":\"area\",\"n\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
                     << "}\n";
                break;
            case Kind::Label:
                file << "{\"k\":\"label\",\"kind\":\"" << escapeJson(entry.label) << "\",\"obj\":" << entry.obj
                     << ",\"type\":\"" << escapeJson(entry.name) << "\"," << rectJson(entry.rect)
                     << ",\"owner\":{" << rectJson(entry.box) << "}}\n";
                break;
            case Kind::Click:
                file << "{\"k\":\"click\",\"name\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
                     << "}\n";
                break;
            case Kind::Credit:
                file << "{\"k\":\"credit\",\"name\":\"" << escapeJson(entry.name) << "\",\"s\":\""
                     << escapeJson(entry.label) << "\"}\n";
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
    if (std::string(g_scene->group) == "credits") {
        UiAuditAccess::recordCreditLines(currentGame);
    }
    const fs::path log = outDir / (std::string(g_scene->id) + ".geometry.jsonl");
    if (!writeGeometry(currentGame, log, outputW, outputH)) {
        fail("cannot write " + log.string());
        return;
    }
    g_done = true;
}

}

void setVerticalClipText(bool enabled)
{
    g_clipText = enabled;
}

void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box)
{
    if (g_collecting) {
        if (!g_collected) {
            g_union = {x, y, w, h};
            g_collected = true;
        }
        else {
            const int left = std::min(g_union.x, x);
            const int top = std::min(g_union.y, y);
            const int right = std::max(g_union.x + g_union.w, x + w);
            const int bottom = std::max(g_union.y + g_union.h, y + h);
            g_union = {left, top, right - left, bottom - top};
        }
        return;
    }
    if (g_clipText && (y < 0 || y + h > g_canvasH)) {
        return;
    }
    Entry entry{Kind::Text, text, {x, y, w, h}, false, {}, {}, 0};
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
    g_entries.push_back({Kind::Gui, type, {x, y, w, h}, false, {}, {}, 0});
}

void recordArea(const char *name, int x, int y, int w, int h)
{
    g_entries.push_back({Kind::Area, name, {x, y, w, h}, false, {}, {}, 0});
}

void recordClick(const char *name, int x, int y, int w, int h)
{
    g_entries.push_back({Kind::Click, name, {x, y, w, h}, false, {}, {}, 0});
}

void recordCanvasClick(const char *name)
{
    recordClick(name, 0, 0, g_canvasW, g_canvasH);
}

void recordLabel(const char *kind, int obj, const char *type, int x, int y, int w, int h, const Rect &owner)
{
    g_entries.push_back({Kind::Label, kind, clipped({x, y, w, h}), true, owner, type, obj});
}

void recordUnitLabel(const char *kind, int obj, int unitType, int x, int y, int w, int h, const Rect &owner)
{
    recordLabel(kind, obj, unitTypeName(unitType), x, y, w, h, owner);
}

void beginLabelText()
{
    g_collecting = true;
    g_collected = false;
}

void endLabelText(const char *kind, int obj, int unitType, const Rect &owner)
{
    g_collecting = false;
    if (g_collected) {
        recordUnitLabel(kind, obj, unitType, g_union.x, g_union.y, g_union.w, g_union.h, owner);
    }
}

void recordCreditLine(const std::string &name, const std::string &text)
{
    g_entries.push_back({Kind::Credit, text, {0, 0, 0, 0}, false, {}, name, 0});
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

void setHover(int x, int y)
{
    g_hoverX = x;
    g_hoverY = y;
}

void onSetupDone(cGame &currentGame)
{
    g_scene = findScene(options().scene);
    g_hoverX = g_scene != nullptr ? g_scene->hoverX : 0;
    g_hoverY = g_scene != nullptr ? g_scene->hoverY : 0;
    g_entries.clear();
    g_frame = 0;
    g_settled = 0;
    g_done = false;
    g_clipText = false;
    currentGame.m_gameSettings->setPlayMusic(false);
    UiAuditAccess::stopCameraEdgeMove(currentGame);
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
    g_collecting = false;
    g_stateAtBegin = UiAuditAccess::state(currentGame);
    g_currentStateAtBegin = UiAuditAccess::currentState(currentGame);
    g_fadeAtBegin = UiAuditAccess::notFadingOut(currentGame);
    if (g_scene != nullptr && g_scene->hover) {
        float windowX = 0.0f;
        float windowY = 0.0f;
        SDL_RenderCoordinatesToWindow(g_renderer, static_cast<float>(g_hoverX), static_cast<float>(g_hoverY), &windowX,
                                      &windowY);
        moveCursor(windowX, windowY);
    }
    else {
        moveCursor(static_cast<float>(kOffscreenCursor), static_cast<float>(kOffscreenCursor));
    }
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
