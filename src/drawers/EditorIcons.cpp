#include "drawers/EditorIcons.hpp"

#include "drawers/IconShapeBuilders.hpp"
#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"

#include <cmath>
#include <utility>

namespace {
using iconshape::arc;
using iconshape::dot;
using iconshape::fill;
using iconshape::stroke;

constexpr float squareThickness = 4.0F;
constexpr float axisThickness = 3.0F;
constexpr float arrowThickness = 4.5F;
constexpr float digitThickness = 4.5F;

IconShape square()
{
    return stroke({{12, 12}, {52, 12}, {52, 52}, {12, 52}, {12, 12}}, squareThickness);
}

IconShape axis(IconPoint from, IconPoint to)
{
    return stroke({from, to}, axisThickness);
}

std::vector<IconShape> copyIcon(IconPoint axisFrom, IconPoint axisTo, float directionX, float directionY)
{
    constexpr float pi = 3.14159265358979F;
    constexpr float halfLength = 15.0F;
    constexpr float headLength = 10.0F;
    constexpr float headAngle = 40.0F * pi / 180.0F;
    const float length = std::hypot(directionX, directionY);
    const float ux = directionX / length;
    const float uy = directionY / length;
    const IconPoint tail{32.0F - ux * halfLength, 32.0F - uy * halfLength};
    const IconPoint tip{32.0F + ux * halfLength, 32.0F + uy * halfLength};
    const float backX = -ux;
    const float backY = -uy;
    const float cosA = std::cos(headAngle);
    const float sinA = std::sin(headAngle);
    const IconPoint wingA{tip.x + headLength * (backX * cosA - backY * sinA), tip.y + headLength * (backX * sinA + backY * cosA)};
    const IconPoint wingB{tip.x + headLength * (backX * cosA + backY * sinA), tip.y + headLength * (-backX * sinA + backY * cosA)};
    return {
        square(),
        axis(axisFrom, axisTo),
        stroke({tail, tip}, arrowThickness),
        stroke({wingA, tip, wingB}, arrowThickness)
    };
}

std::vector<IconShape> startDigit(int digit)
{
    std::vector<IconShape> shapes{arc({32, 32}, 23, 0, 360, squareThickness)};
    switch (digit) {
        case 1:
            shapes.push_back(stroke({{26, 26}, {33, 20}, {33, 44}}, digitThickness));
            break;
        case 2:
            shapes.push_back(stroke({{25, 26}, {28, 21}, {36, 21}, {39, 26}, {39, 31}, {25, 44}, {40, 44}}, digitThickness));
            break;
        case 3:
            shapes.push_back(stroke({{25, 21}, {39, 21}, {31, 31}}, digitThickness));
            shapes.push_back(stroke({{31, 31}, {37, 32}, {40, 36}, {40, 40}, {36, 44}, {29, 44}, {25, 40}}, digitThickness));
            break;
        case 4:
            shapes.push_back(stroke({{35, 44}, {35, 20}, {24, 37}, {41, 37}}, digitThickness));
            break;
        default:
            shapes.push_back(stroke({{39, 21}, {27, 21}, {26, 31}, {32, 30}, {38, 33}, {40, 38}, {37, 43}, {31, 44}, {25, 41}}, digitThickness));
            break;
    }
    return shapes;
}

std::vector<IconShape> buildShapes(EditorIcon icon)
{
    switch (icon) {
        case EditorIcon::Terrain:
            return {fill({{8, 50}, {24, 24}, {32, 34}, {42, 14}, {56, 50}})};
        case EditorIcon::StartFlag:
            return {
                stroke({{16, 10}, {16, 54}}),
                stroke({{10, 54}, {26, 54}}),
                stroke({{16, 12}, {52, 12}, {52, 36}, {16, 36}, {16, 12}}, squareThickness),
                stroke({{29, 22}, {34, 17}, {34, 31}}, 3.5F),
                stroke({{29, 31}, {39, 31}}, 3.5F)
            };
        case EditorIcon::Symmetry:
            return {
                square(),
                fill({{16, 16}, {30, 16}, {30, 48}, {16, 48}}),
                axis({32, 8}, {32, 20}),
                axis({32, 26}, {32, 38}),
                axis({32, 44}, {32, 56})
            };
        case EditorIcon::Save:
            return {
                stroke({{14, 12}, {42, 12}, {52, 22}, {52, 52}, {14, 52}, {14, 12}}, squareThickness),
                fill({{22, 14}, {42, 14}, {42, 28}, {22, 28}}),
                stroke({{22, 52}, {22, 40}, {44, 40}, {44, 52}}, squareThickness)
            };
        case EditorIcon::CopyRight:
            return copyIcon({32, 8}, {32, 56}, 1.0F, 0.0F);
        case EditorIcon::CopyLeft:
            return copyIcon({32, 8}, {32, 56}, -1.0F, 0.0F);
        case EditorIcon::CopyUp:
            return copyIcon({8, 32}, {56, 32}, 0.0F, -1.0F);
        case EditorIcon::CopyDown:
            return copyIcon({8, 32}, {56, 32}, 0.0F, 1.0F);
        case EditorIcon::CopyBottomLeft:
            return copyIcon({9, 9}, {55, 55}, -1.0F, 1.0F);
        case EditorIcon::CopyTopRight:
            return copyIcon({9, 9}, {55, 55}, 1.0F, -1.0F);
        case EditorIcon::CopyTopLeft:
            return copyIcon({9, 55}, {55, 9}, -1.0F, -1.0F);
        case EditorIcon::CopyBottomRight:
            return copyIcon({9, 55}, {55, 9}, 1.0F, 1.0F);
        case EditorIcon::StartDisc:
            return {dot({32, 32}, 25)};
        case EditorIcon::Start1:
            return startDigit(1);
        case EditorIcon::Start2:
            return startDigit(2);
        case EditorIcon::Start3:
            return startDigit(3);
        case EditorIcon::Start4:
            return startDigit(4);
        case EditorIcon::Start5:
            return startDigit(5);
        case EditorIcon::Count:
            break;
    }
    return {};
}
}

const std::vector<IconShape> &editorIconShapes(EditorIcon icon)
{
    static const std::array<std::vector<IconShape>, static_cast<std::size_t>(EditorIcon::Count)> all = [] {
        std::array<std::vector<IconShape>, static_cast<std::size_t>(EditorIcon::Count)> shapes;
        for (std::size_t index = 0; index < shapes.size(); ++index) {
            shapes[index] = buildShapes(static_cast<EditorIcon>(index));
        }
        return shapes;
    }();
    return all[static_cast<std::size_t>(icon)];
}

std::vector<SDL_Vertex> tessellateEditorIcon(EditorIcon icon, float sizePixels, SDL_FColor color)
{
    return tessellateIconShapes(editorIconShapes(icon), sizePixels, color);
}

EditorIconTextures::EditorIconTextures() = default;

EditorIconTextures::~EditorIconTextures() = default;

Texture *EditorIconTextures::get(SDLDrawer &drawer, EditorIcon icon, int side)
{
    const std::size_t index = static_cast<std::size_t>(icon);
    if (side <= 0) return nullptr;
    if (m_textures[index] && m_sides[index] == side) return m_textures[index].get();

    constexpr int supersampling = 4;
    const int pixels = side * supersampling;
    m_textures[index].reset(drawer.createRenderTargetTexture(pixels, pixels));
    m_sides[index] = side;
    SDL_Texture *texture = m_textures[index]->tex.get();
    SDL_SetTextureScaleMode(texture, SDL_SCALEMODE_LINEAR);
    SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND);

    const std::vector<SDL_Vertex> vertices = tessellateEditorIcon(icon, static_cast<float>(pixels), SDL_FColor{1.0F, 1.0F, 1.0F, 1.0F});
    drawer.beginDrawingToTexture(m_textures[index].get());
    // Transparent white, so that the linear downscale does not darken the edge pixels.
    drawer.renderClearToColor(Color{255, 255, 255, 0});
    SDL_SetRenderDrawBlendMode(drawer.getRenderer(), SDL_BLENDMODE_BLEND);
    SDL_RenderGeometry(drawer.getRenderer(), nullptr, vertices.data(), static_cast<int>(vertices.size()), nullptr, 0);
    drawer.endDrawingToTexture();
    return m_textures[index].get();
}
