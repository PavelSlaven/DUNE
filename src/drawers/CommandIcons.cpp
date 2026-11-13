#include "CommandIcons.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <utility>

namespace {
constexpr float gridSize = 64.0F;
constexpr float lineThickness = 5.0F;
constexpr int segmentsPerCircle = 32;
constexpr float pi = 3.14159265358979F;

IconShape stroke(std::vector<IconPoint> points, float thickness = lineThickness)
{
    return IconShape{IconShape::Kind::Stroke, std::move(points), 0.0F, 0.0F, 0.0F, thickness};
}

IconShape arc(IconPoint centre, float radius, float startAngle, float endAngle)
{
    return IconShape{IconShape::Kind::Arc, {centre}, radius, startAngle, endAngle, lineThickness};
}

IconShape fill(std::vector<IconPoint> points)
{
    return IconShape{IconShape::Kind::Fill, std::move(points)};
}

IconShape dot(IconPoint centre, float radius)
{
    return IconShape{IconShape::Kind::Dot, {centre}, radius};
}

std::vector<IconShape> buildShapes(CommandIcon icon)
{
    switch (icon) {
        case CommandIcon::Move:
            return {
                stroke({{10, 32}, {52, 32}}),
                stroke({{36, 14}, {54, 32}, {36, 50}})
            };
        case CommandIcon::Attack:
            return {
                arc({32, 32}, 20, 0, 360),
                stroke({{32, 14}, {32, 24}}),
                stroke({{32, 40}, {32, 50}}),
                stroke({{14, 32}, {24, 32}}),
                stroke({{40, 32}, {50, 32}}),
                dot({32, 32}, 3)
            };
        case CommandIcon::Repair:
            return {
                stroke({{12, 52}, {37, 27}}, 7.0F),
                arc({44, 20}, 10, 350, 640)
            };
        case CommandIcon::Unload:
            return {
                fill({{32, 8}, {25.5F, 19}, {38.5F, 19}}),
                dot({32, 22}, 7),
                stroke({{32, 33}, {32, 46}}),
                stroke({{25, 40}, {32, 47}, {39, 40}}),
                stroke({{14, 48}, {14, 54}, {50, 54}, {50, 48}})
            };
        case CommandIcon::Deploy:
            return {
                stroke({{26, 26}, {38, 26}, {38, 38}, {26, 38}, {26, 26}}),
                stroke({{32, 20}, {32, 10}}),
                stroke({{27, 15}, {32, 10}, {37, 15}}),
                stroke({{32, 44}, {32, 54}}),
                stroke({{27, 49}, {32, 54}, {37, 49}}),
                stroke({{20, 32}, {10, 32}}),
                stroke({{15, 27}, {10, 32}, {15, 37}}),
                stroke({{44, 32}, {54, 32}}),
                stroke({{49, 27}, {54, 32}, {49, 37}})
            };
        case CommandIcon::Rally:
            return {
                stroke({{18, 10}, {18, 54}}),
                fill({{20, 10}, {52, 22}, {20, 34}}),
                stroke({{10, 54}, {26, 54}})
            };
        case CommandIcon::Release:
            return {
                stroke({{30, 14}, {14, 14}, {14, 50}, {30, 50}}),
                stroke({{24, 32}, {52, 32}}),
                stroke({{42, 22}, {52, 32}, {42, 42}})
            };
    }
    return {};
}

class Tessellator {
public:
    Tessellator(float scale, SDL_FColor color) : m_scale(scale), m_color(color) {}

    std::vector<SDL_Vertex> take() { return std::move(m_vertices); }

    void add(const IconShape &shape)
    {
        switch (shape.kind) {
            case IconShape::Kind::Stroke:
                addStroke(shape);
                break;
            case IconShape::Kind::Arc:
                addArc(shape);
                break;
            case IconShape::Kind::Fill:
                addFill(shape.points);
                break;
            case IconShape::Kind::Dot:
                addDisc(shape.points.front(), shape.radius);
                break;
        }
    }

private:
    void vertex(float x, float y)
    {
        SDL_Vertex v{};
        v.position = SDL_FPoint{x * m_scale, y * m_scale};
        v.color = m_color;
        m_vertices.push_back(v);
    }

    void triangle(IconPoint a, IconPoint b, IconPoint c)
    {
        vertex(a.x, a.y);
        vertex(b.x, b.y);
        vertex(c.x, c.y);
    }

    void quad(IconPoint a, IconPoint b, IconPoint c, IconPoint d)
    {
        triangle(a, b, c);
        triangle(a, c, d);
    }

    void addDisc(IconPoint centre, float radius)
    {
        for (int i = 0; i < segmentsPerCircle; ++i) {
            const float from = 2.0F * pi * static_cast<float>(i) / segmentsPerCircle;
            const float to = 2.0F * pi * static_cast<float>(i + 1) / segmentsPerCircle;
            triangle(
                centre,
                {centre.x + radius * std::cos(from), centre.y + radius * std::sin(from)},
                {centre.x + radius * std::cos(to), centre.y + radius * std::sin(to)}
            );
        }
    }

    void addFill(const std::vector<IconPoint> &points)
    {
        for (std::size_t i = 1; i + 1 < points.size(); ++i) {
            triangle(points[0], points[i], points[i + 1]);
        }
    }

    void addStroke(const IconShape &shape)
    {
        const float half = shape.thickness / 2.0F;
        for (std::size_t i = 0; i + 1 < shape.points.size(); ++i) {
            const IconPoint a = shape.points[i];
            const IconPoint b = shape.points[i + 1];
            const float length = std::hypot(b.x - a.x, b.y - a.y);
            if (length <= 0.0F) continue;
            const float nx = -(b.y - a.y) / length * half;
            const float ny = (b.x - a.x) / length * half;
            quad({a.x + nx, a.y + ny}, {b.x + nx, b.y + ny}, {b.x - nx, b.y - ny}, {a.x - nx, a.y - ny});
        }
        for (const IconPoint &point : shape.points) {
            addDisc(point, half);
        }
    }

    void addArc(const IconShape &shape)
    {
        const IconPoint centre = shape.points.front();
        const float half = shape.thickness / 2.0F;
        const float sweep = shape.endAngle - shape.startAngle;
        const int segments = std::max(1, static_cast<int>(std::ceil(segmentsPerCircle * std::fabs(sweep) / 360.0F)));
        const float inner = shape.radius - half;
        const float outer = shape.radius + half;
        for (int i = 0; i < segments; ++i) {
            const float from = (shape.startAngle + sweep * static_cast<float>(i) / segments) * pi / 180.0F;
            const float to = (shape.startAngle + sweep * static_cast<float>(i + 1) / segments) * pi / 180.0F;
            quad(
                {centre.x + inner * std::cos(from), centre.y + inner * std::sin(from)},
                {centre.x + outer * std::cos(from), centre.y + outer * std::sin(from)},
                {centre.x + outer * std::cos(to), centre.y + outer * std::sin(to)},
                {centre.x + inner * std::cos(to), centre.y + inner * std::sin(to)}
            );
        }
        if (std::fabs(sweep) < 360.0F) {
            for (const float angle : {shape.startAngle, shape.endAngle}) {
                const float radians = angle * pi / 180.0F;
                addDisc({centre.x + shape.radius * std::cos(radians), centre.y + shape.radius * std::sin(radians)}, half);
            }
        }
    }

    float m_scale;
    SDL_FColor m_color;
    std::vector<SDL_Vertex> m_vertices;
};
}

const std::vector<IconShape> &commandIconShapes(CommandIcon icon)
{
    static const std::array<std::vector<IconShape>, 7> all{
        buildShapes(CommandIcon::Move),
        buildShapes(CommandIcon::Attack),
        buildShapes(CommandIcon::Repair),
        buildShapes(CommandIcon::Unload),
        buildShapes(CommandIcon::Deploy),
        buildShapes(CommandIcon::Rally),
        buildShapes(CommandIcon::Release)
    };
    return all[static_cast<std::size_t>(icon)];
}

std::vector<SDL_Vertex> tessellateCommandIcon(CommandIcon icon, float sizePixels, SDL_FColor color)
{
    Tessellator tessellator(sizePixels / gridSize, color);
    for (const IconShape &shape : commandIconShapes(icon)) {
        tessellator.add(shape);
    }
    return tessellator.take();
}
