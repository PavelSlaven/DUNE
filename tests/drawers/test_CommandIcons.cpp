#include <catch2/catch_test_macros.hpp>

#include "controls/CommandModePolicy.hpp"
#include "drawers/CommandBarPolicy.hpp"
#include "drawers/CommandIcons.hpp"

#include <algorithm>
#include <array>
#include <cmath>

namespace {
constexpr std::array<CommandIcon, 7> allIcons{
    CommandIcon::Move, CommandIcon::Attack, CommandIcon::Repair, CommandIcon::Unload,
    CommandIcon::Deploy, CommandIcon::Rally, CommandIcon::Release
};

constexpr float margin = 6.0F;
constexpr float gridSize = 64.0F;
constexpr float pi = 3.14159265358979F;

struct Bounds {
    float minX = 1000.0F;
    float minY = 1000.0F;
    float maxX = -1000.0F;
    float maxY = -1000.0F;

    void add(float x, float y, float reach)
    {
        minX = std::min(minX, x - reach);
        minY = std::min(minY, y - reach);
        maxX = std::max(maxX, x + reach);
        maxY = std::max(maxY, y + reach);
    }
};

Bounds boundsOf(const std::vector<IconShape> &shapes)
{
    Bounds bounds;
    for (const IconShape &shape : shapes) {
        switch (shape.kind) {
            case IconShape::Kind::Stroke:
                for (const IconPoint &point : shape.points) {
                    bounds.add(point.x, point.y, shape.thickness / 2.0F);
                }
                break;
            case IconShape::Kind::Fill:
                for (const IconPoint &point : shape.points) {
                    bounds.add(point.x, point.y, 0.0F);
                }
                break;
            case IconShape::Kind::Dot:
                bounds.add(shape.points.front().x, shape.points.front().y, shape.radius);
                break;
            case IconShape::Kind::Arc:
                for (int step = 0; step <= 90; ++step) {
                    const float angle = (shape.startAngle + (shape.endAngle - shape.startAngle) * static_cast<float>(step) / 90.0F) * pi / 180.0F;
                    bounds.add(
                        shape.points.front().x + shape.radius * std::cos(angle),
                        shape.points.front().y + shape.radius * std::sin(angle),
                        shape.thickness / 2.0F
                    );
                }
                break;
        }
    }
    return bounds;
}
}

TEST_CASE("P17 every command icon has shapes inside the grid margin", "[P17]")
{
    for (const CommandIcon icon : allIcons) {
        const std::vector<IconShape> &shapes = commandIconShapes(icon);
        REQUIRE_FALSE(shapes.empty());
        const Bounds bounds = boundsOf(shapes);
        REQUIRE(bounds.minX >= margin);
        REQUIRE(bounds.minY >= margin);
        REQUIRE(bounds.maxX <= gridSize - margin);
        REQUIRE(bounds.maxY <= gridSize - margin);
    }
}

TEST_CASE("P17 tessellated icons are triangles inside the square in the given color", "[P17]")
{
    constexpr float size = 48.0F;
    const SDL_FColor color{0.25F, 0.5F, 0.75F, 1.0F};
    for (const CommandIcon icon : allIcons) {
        const std::vector<SDL_Vertex> vertices = tessellateCommandIcon(icon, size, color);
        REQUIRE_FALSE(vertices.empty());
        REQUIRE(vertices.size() % 3 == 0);
        for (const SDL_Vertex &vertex : vertices) {
            REQUIRE(vertex.position.x >= 0.0F);
            REQUIRE(vertex.position.x <= size);
            REQUIRE(vertex.position.y >= 0.0F);
            REQUIRE(vertex.position.y <= size);
            REQUIRE(vertex.color.r == color.r);
            REQUIRE(vertex.color.g == color.g);
            REQUIRE(vertex.color.b == color.b);
            REQUIRE(vertex.color.a == color.a);
        }
    }
}

TEST_CASE("P17 corner key label is only a single character", "[P17]")
{
    REQUIRE(cornerKeyLabel("R") == "R");
    REQUIRE(cornerKeyLabel("CTRL").empty());
    REQUIRE(cornerKeyLabel("ЛКМ").empty());
    REQUIRE(cornerKeyLabel("").empty());
}

TEST_CASE("P17 command tooltip names the key only when there is one", "[P17]")
{
    REQUIRE(commandTooltip("Ремонт", "R") == "Ремонт (R)");
    REQUIRE(commandTooltip("Точка сбора", "") == "Точка сбора");
}

TEST_CASE("P17 repair button is active only in repair mode", "[P17]")
{
    CommandTargetingState state;
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Repair, state));
    state.repair = true;
    REQUIRE(isCommandButtonActive(CommandIcon::Repair, state));
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Attack, state));
}

TEST_CASE("P17 attack button is active while a target is being picked", "[P17]")
{
    CommandTargetingState state;
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Attack, state));
    state.attack = true;
    REQUIRE(isCommandButtonActive(CommandIcon::Attack, state));
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Repair, state));
}

TEST_CASE("P17 move and rally buttons follow their own picking mode", "[P17]")
{
    CommandTargetingState state;
    state.move = true;
    REQUIRE(isCommandButtonActive(CommandIcon::Move, state));
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Rally, state));
    state = CommandTargetingState{};
    state.rally = true;
    REQUIRE(isCommandButtonActive(CommandIcon::Rally, state));
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Move, state));
}

TEST_CASE("P17 deploy, unload and release have no mode", "[P17]")
{
    const CommandTargetingState everything{true, true, true, true};
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Deploy, everything));
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Unload, everything));
    REQUIRE_FALSE(isCommandButtonActive(CommandIcon::Release, everything));
}
