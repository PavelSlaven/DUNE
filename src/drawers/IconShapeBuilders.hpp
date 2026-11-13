#pragma once

#include "drawers/CommandIcons.hpp"

#include <utility>
#include <vector>

namespace iconshape {
constexpr float gridSize = 64.0F;
constexpr float lineThickness = 5.0F;

inline IconShape stroke(std::vector<IconPoint> points, float thickness = lineThickness)
{
    return IconShape{IconShape::Kind::Stroke, std::move(points), 0.0F, 0.0F, 0.0F, thickness};
}

inline IconShape arc(IconPoint centre, float radius, float startAngle, float endAngle, float thickness = lineThickness)
{
    return IconShape{IconShape::Kind::Arc, {centre}, radius, startAngle, endAngle, thickness};
}

inline IconShape fill(std::vector<IconPoint> points)
{
    return IconShape{IconShape::Kind::Fill, std::move(points)};
}

inline IconShape dot(IconPoint centre, float radius)
{
    return IconShape{IconShape::Kind::Dot, {centre}, radius};
}
}
