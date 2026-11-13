#include <catch2/catch_test_macros.hpp>

#include "drawers/EditorIcons.hpp"
#include "gamestates/EditorTexts.hpp"
#include "gamestates/NewMapDialogLayout.hpp"
#include "utils/Localization.hpp"

#include <array>
#include <cstring>
#include <utility>
#include <vector>

namespace {
constexpr std::array<std::pair<int, int>, 6> screens{{
    {800, 600}, {1024, 768}, {1920, 1080}, {2560, 1440}, {3840, 2160}, {5120, 1440}
}};

bool disjoint(const cRectangle &a, const cRectangle &b)
{
    return a.getEndX() <= b.getX() || b.getEndX() <= a.getX() || a.getEndY() <= b.getY() || b.getEndY() <= a.getY();
}

bool inside(const cRectangle &inner, const cRectangle &outer)
{
    return inner.getX() >= outer.getX() && inner.getY() >= outer.getY() && inner.getEndX() <= outer.getEndX() &&
           inner.getEndY() <= outer.getEndY();
}

std::vector<cRectangle> contentOf(const NewMapDialogLayout &layout)
{
    std::vector<cRectangle> result{layout.title, layout.returnButton, layout.createButton};
    for (int row = 0; row < NewMapDialogLayout::RowCount; ++row) {
        result.push_back(layout.labels[row]);
        result.push_back(layout.fields[row]);
    }
    return result;
}
}

TEST_CASE("P18 new map dialog panel is on the screen and centred", "[P18]")
{
    for (const auto &[width, height] : screens) {
        const NewMapDialogLayout layout = NewMapDialogLayout::create(width, height);
        REQUIRE(layout.panel.getX() >= 0);
        REQUIRE(layout.panel.getY() >= 0);
        REQUIRE(layout.panel.getEndX() <= width);
        REQUIRE(layout.panel.getEndY() <= height);
        REQUIRE(layout.panel.getX() + layout.panel.getEndX() == width);
        REQUIRE(layout.panel.getY() + layout.panel.getEndY() == height);
    }
}

TEST_CASE("P18 new map dialog content stays inside the panel", "[P18]")
{
    for (const auto &[width, height] : screens) {
        const NewMapDialogLayout layout = NewMapDialogLayout::create(width, height);
        for (const cRectangle &rect : contentOf(layout)) {
            REQUIRE(rect.getWidth() > 0);
            REQUIRE(rect.getHeight() > 0);
            REQUIRE(inside(rect, layout.panel));
        }
    }
}

TEST_CASE("P18 new map dialog content never overlaps", "[P18]")
{
    for (const auto &[width, height] : screens) {
        const std::vector<cRectangle> content = contentOf(NewMapDialogLayout::create(width, height));
        for (std::size_t first = 0; first < content.size(); ++first) {
            for (std::size_t second = first + 1; second < content.size(); ++second) {
                REQUIRE(disjoint(content[first], content[second]));
            }
        }
    }
}

TEST_CASE("P18 new map dialog rows run top to bottom above the buttons", "[P18]")
{
    const NewMapDialogLayout layout = NewMapDialogLayout::create(800, 600);
    REQUIRE(layout.title.getEndY() <= layout.labels[0].getY());
    for (int row = 1; row < NewMapDialogLayout::RowCount; ++row) {
        REQUIRE(layout.labels[row - 1].getEndY() <= layout.labels[row].getY());
    }
    REQUIRE(layout.labels[NewMapDialogLayout::RowCount - 1].getEndY() <= layout.returnButton.getY());
    REQUIRE(layout.returnButton.getEndX() <= layout.createButton.getX());
}

TEST_CASE("P18 every editor icon has triangles inside the cell", "[P18]")
{
    constexpr float size = 64.0F;
    constexpr float margin = 6.0F;
    const SDL_FColor color{0.25F, 0.5F, 0.75F, 1.0F};
    for (int index = 0; index < static_cast<int>(EditorIcon::Count); ++index) {
        const std::vector<SDL_Vertex> vertices = tessellateEditorIcon(static_cast<EditorIcon>(index), size, color);
        REQUIRE_FALSE(vertices.empty());
        REQUIRE(vertices.size() % 3 == 0);
        for (const SDL_Vertex &vertex : vertices) {
            REQUIRE(vertex.position.x >= margin);
            REQUIRE(vertex.position.x <= size - margin);
            REQUIRE(vertex.position.y >= margin);
            REQUIRE(vertex.position.y <= size - margin);
            REQUIRE(vertex.color.r == color.r);
            REQUIRE(vertex.color.a == color.a);
        }
    }
}

TEST_CASE("P18 editor icons scale with the requested size", "[P18]")
{
    const SDL_FColor color{1.0F, 1.0F, 1.0F, 1.0F};
    for (int index = 0; index < static_cast<int>(EditorIcon::Count); ++index) {
        const std::vector<SDL_Vertex> vertices = tessellateEditorIcon(static_cast<EditorIcon>(index), 256.0F, color);
        REQUIRE_FALSE(vertices.empty());
        for (const SDL_Vertex &vertex : vertices) {
            REQUIRE(vertex.position.x >= 0.0F);
            REQUIRE(vertex.position.x <= 256.0F);
            REQUIRE(vertex.position.y >= 0.0F);
            REQUIRE(vertex.position.y <= 256.0F);
        }
    }
}

TEST_CASE("P18 every editor text exists in both languages", "[P18]")
{
    for (const char *language : {"en", "ru"}) {
        localization::setLanguage(language);
        for (int index = 0; index < static_cast<int>(EditorText::Count); ++index) {
            REQUIRE(std::strlen(editorText(static_cast<EditorText>(index))) > 0);
        }
    }
    localization::setLanguage("ru");
}

TEST_CASE("P18 editor texts differ between English and Russian", "[P18]")
{
    for (int index = 0; index < static_cast<int>(EditorText::Count); ++index) {
        localization::setLanguage("en");
        const std::string english = editorText(static_cast<EditorText>(index));
        localization::setLanguage("ru");
        const std::string russian = editorText(static_cast<EditorText>(index));
        REQUIRE(english != russian);
    }
}
