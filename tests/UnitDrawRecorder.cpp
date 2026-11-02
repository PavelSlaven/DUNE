#include "UnitDrawRecorder.hpp"

#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"

namespace {
void record(std::string method, const cRectangle &destination = {0, 0, 0, 0})
{
    UnitDrawCall call;
    call.method = std::move(method);
    call.destination = destination;
    call.x = destination.getX();
    call.y = destination.getY();
    call.width = destination.getWidth();
    call.height = destination.getHeight();
    unitDrawCalls().push_back(std::move(call));
}

void recordRect(std::string method, int x, int y, int width, int height, Color color)
{
    UnitDrawCall call;
    call.method = std::move(method);
    call.destination = {x, y, width, height};
    call.x = x;
    call.y = y;
    call.width = width;
    call.height = height;
    call.color = color;
    call.opacity = color.a;
    unitDrawCalls().push_back(std::move(call));
}
}

std::vector<UnitDrawCall> &unitDrawCalls()
{
    static std::vector<UnitDrawCall> calls;
    return calls;
}

void clearUnitDrawCalls()
{
    unitDrawCalls().clear();
}

SDLDrawer::SDLDrawer(SDL_Renderer *_renderer) : renderer(_renderer)
{
}

SDLDrawer::~SDLDrawer() = default;

void SDLDrawer::renderSprite(Texture *src, int x, int y, Uint8 opacity)
{
    UnitDrawCall call;
    call.method = "renderSprite";
    call.texture = src;
    call.x = x;
    call.y = y;
    call.opacity = opacity;
    unitDrawCalls().push_back(std::move(call));
}

void SDLDrawer::renderStrechSprite(
    Texture *src,
    cRectangle srcPos,
    cRectangle destPos,
    Uint8 opacity,
    SDL_BlendMode blendMode)
{
    UnitDrawCall call;
    call.method = "renderStrechSprite";
    call.texture = src;
    call.source = srcPos;
    call.destination = destPos;
    call.x = destPos.getX();
    call.y = destPos.getY();
    call.width = destPos.getWidth();
    call.height = destPos.getHeight();
    call.opacity = opacity;
    call.blendMode = blendMode;
    unitDrawCalls().push_back(std::move(call));
}

#if defined(D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER)
void SDLDrawer::renderStrechSpriteF(
    Texture *src,
    cRectangle srcPos,
    SDL_FRect destPos,
    Uint8 opacity,
    SDL_BlendMode blendMode)
{
    UnitDrawCall call;
    call.method = "renderStrechSpriteF";
    call.texture = src;
    call.source = srcPos;
    call.floatDestination = destPos;
    call.x = static_cast<int>(destPos.x);
    call.y = static_cast<int>(destPos.y);
    call.width = static_cast<int>(destPos.w);
    call.height = static_cast<int>(destPos.h);
    call.opacity = opacity;
    call.blendMode = blendMode;
    unitDrawCalls().push_back(std::move(call));
}
#endif

void SDLDrawer::renderStrechFullSprite(Texture *src, cRectangle destPos, Uint8 opacity)
{
    UnitDrawCall call;
    call.method = "renderStrechFullSprite";
    call.texture = src;
    call.destination = destPos;
    call.x = destPos.getX();
    call.y = destPos.getY();
    call.width = destPos.getWidth();
    call.height = destPos.getHeight();
    call.opacity = opacity;
    unitDrawCalls().push_back(std::move(call));
}

void SDLDrawer::renderFromSurface(SDL_Surface *, int x, int y, Uint8 opacity, int)
{
    UnitDrawCall call;
    call.method = "renderFromSurface";
    call.x = x;
    call.y = y;
    call.opacity = opacity;
    unitDrawCalls().push_back(std::move(call));
}

void SDLDrawer::renderTexture(SDL_Texture *, int x, int y, int width, int height, Uint8 opacity)
{
    UnitDrawCall call;
    call.method = "renderTexture";
    call.x = x;
    call.y = y;
    call.width = width;
    call.height = height;
    call.opacity = opacity;
    unitDrawCalls().push_back(std::move(call));
}

void SDLDrawer::renderRectFillColor(
    int x, int y, int width, int height, Uint8 red, Uint8 green, Uint8 blue, unsigned char opacity)
{
    recordRect("renderRectFillColor", x, y, width, height, Color{red, green, blue, opacity});
}

void SDLDrawer::renderRectFillColor(int x, int y, int width, int height, Color color)
{
    recordRect("renderRectFillColor", x, y, width, height, color);
}

void SDLDrawer::renderRectFillColor(const cRectangle &rect, Color color)
{
    recordRect("renderRectFillColor", rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight(), color);
}

void SDLDrawer::renderRectFillColor(const cRectangle &rect, Color color, Uint8 opacity)
{
    color.a = opacity;
    recordRect("renderRectFillColor", rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight(), color);
}

void SDLDrawer::renderRectColor(
    int x, int y, int width, int height, Uint8 red, Uint8 green, Uint8 blue, unsigned char opacity)
{
    recordRect("renderRectColor", x, y, width, height, Color{red, green, blue, opacity});
}

void SDLDrawer::renderRectColor(int x, int y, int width, int height, Color color)
{
    recordRect("renderRectColor", x, y, width, height, color);
}

void SDLDrawer::renderRectColor(const cRectangle &rect, Uint8 red, Uint8 green, Uint8 blue, unsigned char opacity)
{
    recordRect("renderRectColor", rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight(), Color{red, green, blue, opacity});
}

void SDLDrawer::renderRectColor(const cRectangle &rect, Color color, unsigned char opacity)
{
    color.a = opacity;
    recordRect("renderRectColor", rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight(), color);
}

void SDLDrawer::clearRectToTransparent(const cRectangle &rect)
{
    record("clearRectToTransparent", rect);
}

void SDLDrawer::resetClippingFor()
{
    record("resetClippingFor");
}

void SDLDrawer::setClippingFor(int left, int top, int right, int bottom)
{
    record("setClippingFor", {left, top, right - left, bottom - top});
}

void SDLDrawer::renderClearToColor(Color color)
{
    UnitDrawCall call;
    call.method = "renderClearToColor";
    call.color = color;
    unitDrawCalls().push_back(std::move(call));
}

void SDLDrawer::gui_DrawRect(const cRectangle &rectangle)
{
    record("gui_DrawRect", rectangle);
}

void SDLDrawer::gui_DrawRect(
    const cRectangle &rectangle, Color, Color, Color)
{
    record("gui_DrawRect", rectangle);
}

void SDLDrawer::gui_DrawRectBorder(const cRectangle &rectangle, Color, Color)
{
    record("gui_DrawRectBorder", rectangle);
}

void SDLDrawer::renderLine(int x1, int y1, int x2, int y2, Color color)
{
    UnitDrawCall call;
    call.method = "renderLine";
    call.x = x1;
    call.y = y1;
    call.width = x2;
    call.height = y2;
    call.color = color;
    unitDrawCalls().push_back(std::move(call));
}

void SDLDrawer::renderDot(int x, int y, Color color, int size)
{
    UnitDrawCall call;
    call.method = "renderDot";
    call.x = x;
    call.y = y;
    call.width = size;
    call.height = size;
    call.color = color;
    unitDrawCalls().push_back(std::move(call));
}

bool SDLDrawer::isSurface8BitPaletted(SDL_Surface *)
{
    record("isSurface8BitPaletted");
    return false;
}

void SDLDrawer::FillWithColor(SDL_Surface *, Color color)
{
    UnitDrawCall call;
    call.method = "FillWithColor";
    call.color = color;
    unitDrawCalls().push_back(std::move(call));
}

Color SDLDrawer::getPixel(SDL_Surface *, int, int)
{
    record("getPixel");
    return Color{};
}

void SDLDrawer::setPixel(SDL_Surface *, int x, int y, Color color)
{
    UnitDrawCall call;
    call.method = "setPixel";
    call.x = x;
    call.y = y;
    call.color = color;
    unitDrawCalls().push_back(std::move(call));
}

Texture *SDLDrawer::createRenderTargetTexture(int width, int height)
{
    UnitDrawCall call;
    call.method = "createRenderTargetTexture";
    call.width = width;
    call.height = height;
    unitDrawCalls().push_back(std::move(call));
    return nullptr;
}

void SDLDrawer::beginDrawingToTexture(Texture *targetTexture)
{
    UnitDrawCall call;
    call.method = "beginDrawingToTexture";
    call.texture = targetTexture;
    unitDrawCalls().push_back(std::move(call));
}

void SDLDrawer::endDrawingToTexture()
{
    record("endDrawingToTexture");
}
