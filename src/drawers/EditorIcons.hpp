#pragma once

#include "drawers/CommandIcons.hpp"

#include <SDL3/SDL.h>

#include <array>
#include <memory>
#include <vector>

class SDLDrawer;
class Texture;

enum class EditorIcon {
    Terrain,
    StartFlag,
    Symmetry,
    Save,
    CopyRight,
    CopyLeft,
    CopyUp,
    CopyDown,
    CopyBottomLeft,
    CopyBottomRight,
    CopyTopLeft,
    CopyTopRight,
    StartDisc,
    Start1,
    Start2,
    Start3,
    Start4,
    Start5,
    Count
};

[[nodiscard]] const std::vector<IconShape> &editorIconShapes(EditorIcon icon);

[[nodiscard]] std::vector<SDL_Vertex> tessellateEditorIcon(EditorIcon icon, float sizePixels, SDL_FColor color);

class EditorIconTextures {
public:
    EditorIconTextures();
    ~EditorIconTextures();

    Texture *get(SDLDrawer &drawer, EditorIcon icon, int side);

private:
    static constexpr std::size_t kCount = static_cast<std::size_t>(EditorIcon::Count);
    std::array<std::unique_ptr<Texture>, kCount> m_textures;
    std::array<int, kCount> m_sides{};
};
