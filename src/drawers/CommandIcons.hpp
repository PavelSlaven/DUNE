#pragma once

#include <SDL3/SDL.h>

#include <vector>

enum class CommandIcon {
    Move,
    Attack,
    Repair,
    Unload,
    Deploy,
    Rally,
    Release
};

struct IconPoint {
    float x;
    float y;
};

struct IconShape {
    enum class Kind {
        Stroke,
        Arc,
        Fill,
        Dot
    };

    Kind kind;
    // Stroke and Fill: the vertices. Arc and Dot: the centre only.
    std::vector<IconPoint> points;
    float radius = 0.0F;
    // Degrees; angle 0 points right and angles grow clockwise on screen.
    float startAngle = 0.0F;
    float endAngle = 0.0F;
    float thickness = 0.0F;
};

[[nodiscard]] const std::vector<IconShape> &commandIconShapes(CommandIcon icon);

[[nodiscard]] std::vector<SDL_Vertex> tessellateCommandIcon(CommandIcon icon, float sizePixels, SDL_FColor color);
