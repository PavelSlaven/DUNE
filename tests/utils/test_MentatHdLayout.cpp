#include <catch2/catch_test_macros.hpp>

#include "gameobjects/mentat/MentatHdLayout.hpp"

bool insideFrame(int x, int y, int width, int height)
{
    return x >= 0 && y >= 0 && x + width <= MENTAT_HD_FRAME_WIDTH && y + height <= MENTAT_HD_FRAME_HEIGHT;
}

bool intersects(const MentatHdRect &a, const MentatHdRect &b)
{
    return a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height;
}

struct NamedMentatHdLayout {
    const char *name;
    const MentatHdLayout *layout;
};

constexpr std::array<NamedMentatHdLayout, 4> kMentatHdLayouts = {{
    {"Атрейдесы", &kAtreidesMentatHdLayout},
    {"Бене Гессерит", &kBeneMentatHdLayout},
    {"Харконнены", &kHarkonnenMentatHdLayout},
    {"Ордосы", &kOrdosMentatHdLayout}
}};

TEST_CASE("mentat HD layouts keep the fork values", "[P11]")
{
    CHECK(MENTAT_HD_FRAME_WIDTH == 640);
    CHECK(MENTAT_HD_FRAME_HEIGHT == 480);
    CHECK(MENTAT_EYES_WIDTH == 96);
    CHECK(MENTAT_EYES_HEIGHT == 32);
    CHECK(MENTAT_MOUTH_WIDTH == 112);
    CHECK(MENTAT_MOUTH_HEIGHT == 80);

    INFO("Атрейдесы");
    CHECK(kAtreidesMentatHdLayout.eyes.x == 96);
    CHECK(kAtreidesMentatHdLayout.eyes.y == 180);
    CHECK(kAtreidesMentatHdLayout.mouth.x == 100);
    CHECK(kAtreidesMentatHdLayout.mouth.y == 210);
    CHECK(kAtreidesMentatHdLayout.sceneFrame.x == 234);
    CHECK(kAtreidesMentatHdLayout.sceneFrame.y == 95);
    CHECK(kAtreidesMentatHdLayout.sceneFrame.width == 400);
    CHECK(kAtreidesMentatHdLayout.sceneFrame.height == 243);
    CHECK(kAtreidesMentatHdLayout.sceneOpening.x == 276);
    CHECK(kAtreidesMentatHdLayout.sceneOpening.y == 115);
    CHECK(kAtreidesMentatHdLayout.sceneOpening.width == 322);
    CHECK(kAtreidesMentatHdLayout.sceneOpening.height == 219);
    CHECK(kAtreidesMentatHdLayout.openingCornerHeight == 0);
    CHECK(kAtreidesMentatHdLayout.shoulderEdge.size() == 10);

    INFO("Бене Гессерит");
    CHECK(kBeneMentatHdLayout.eyes.x == 96);
    CHECK(kBeneMentatHdLayout.eyes.y == 180);
    CHECK(kBeneMentatHdLayout.mouth.x == 100);
    CHECK(kBeneMentatHdLayout.mouth.y == 210);
    CHECK(kBeneMentatHdLayout.sceneFrame.x == 211);
    CHECK(kBeneMentatHdLayout.sceneFrame.y == 93);
    CHECK(kBeneMentatHdLayout.sceneFrame.width == 400);
    CHECK(kBeneMentatHdLayout.sceneFrame.height == 243);
    CHECK(kBeneMentatHdLayout.sceneOpening.x == 215);
    CHECK(kBeneMentatHdLayout.sceneOpening.y == 104);
    CHECK(kBeneMentatHdLayout.sceneOpening.width == 398);
    CHECK(kBeneMentatHdLayout.sceneOpening.height == 215);
    CHECK(kBeneMentatHdLayout.openingCornerHeight == 14);
    CHECK(kBeneMentatHdLayout.shoulderEdge.size() == 0);

    INFO("Харконнены");
    CHECK(kHarkonnenMentatHdLayout.eyes.x == 96);
    CHECK(kHarkonnenMentatHdLayout.eyes.y == 180);
    CHECK(kHarkonnenMentatHdLayout.mouth.x == 100);
    CHECK(kHarkonnenMentatHdLayout.mouth.y == 210);
    CHECK(kHarkonnenMentatHdLayout.sceneFrame.x == 211);
    CHECK(kHarkonnenMentatHdLayout.sceneFrame.y == 93);
    CHECK(kHarkonnenMentatHdLayout.sceneFrame.width == 400);
    CHECK(kHarkonnenMentatHdLayout.sceneFrame.height == 243);
    CHECK(kHarkonnenMentatHdLayout.sceneOpening.x == 215);
    CHECK(kHarkonnenMentatHdLayout.sceneOpening.y == 104);
    CHECK(kHarkonnenMentatHdLayout.sceneOpening.width == 398);
    CHECK(kHarkonnenMentatHdLayout.sceneOpening.height == 215);
    CHECK(kHarkonnenMentatHdLayout.openingCornerHeight == 14);
    CHECK(kHarkonnenMentatHdLayout.shoulderEdge.size() == 0);

    INFO("Ордосы");
    CHECK(kOrdosMentatHdLayout.eyes.x == 48);
    CHECK(kOrdosMentatHdLayout.eyes.y == 174);
    CHECK(kOrdosMentatHdLayout.mouth.x == 52);
    CHECK(kOrdosMentatHdLayout.mouth.y == 207);
    CHECK(kOrdosMentatHdLayout.sceneFrame.x == 211);
    CHECK(kOrdosMentatHdLayout.sceneFrame.y == 93);
    CHECK(kOrdosMentatHdLayout.sceneFrame.width == 400);
    CHECK(kOrdosMentatHdLayout.sceneFrame.height == 243);
    CHECK(kOrdosMentatHdLayout.sceneOpening.x == 215);
    CHECK(kOrdosMentatHdLayout.sceneOpening.y == 104);
    CHECK(kOrdosMentatHdLayout.sceneOpening.width == 398);
    CHECK(kOrdosMentatHdLayout.sceneOpening.height == 215);
    CHECK(kOrdosMentatHdLayout.openingCornerHeight == 14);
    CHECK(kOrdosMentatHdLayout.shoulderEdge.size() == 11);

    INFO("Атрейдесы: ломаная плеча");
    CHECK(kAtreidesShoulderEdge[0].y == 270);
    CHECK(kAtreidesShoulderEdge[0].rightX == 273);
    CHECK(kAtreidesShoulderEdge[1].y == 290);
    CHECK(kAtreidesShoulderEdge[1].rightX == 273);
    CHECK(kAtreidesShoulderEdge[2].y == 294);
    CHECK(kAtreidesShoulderEdge[2].rightX == 275);
    CHECK(kAtreidesShoulderEdge[3].y == 296);
    CHECK(kAtreidesShoulderEdge[3].rightX == 285);
    CHECK(kAtreidesShoulderEdge[4].y == 300);
    CHECK(kAtreidesShoulderEdge[4].rightX == 289);
    CHECK(kAtreidesShoulderEdge[5].y == 306);
    CHECK(kAtreidesShoulderEdge[5].rightX == 293);
    CHECK(kAtreidesShoulderEdge[6].y == 314);
    CHECK(kAtreidesShoulderEdge[6].rightX == 297);
    CHECK(kAtreidesShoulderEdge[7].y == 320);
    CHECK(kAtreidesShoulderEdge[7].rightX == 303);
    CHECK(kAtreidesShoulderEdge[8].y == 326);
    CHECK(kAtreidesShoulderEdge[8].rightX == 308);
    CHECK(kAtreidesShoulderEdge[9].y == 334);
    CHECK(kAtreidesShoulderEdge[9].rightX == 314);

    INFO("Ордосы: ломаная плеча");
    CHECK(kOrdosShoulderEdge[0].y == 273);
    CHECK(kOrdosShoulderEdge[0].rightX == 213);
    CHECK(kOrdosShoulderEdge[1].y == 276);
    CHECK(kOrdosShoulderEdge[1].rightX == 218);
    CHECK(kOrdosShoulderEdge[2].y == 280);
    CHECK(kOrdosShoulderEdge[2].rightX == 225);
    CHECK(kOrdosShoulderEdge[3].y == 285);
    CHECK(kOrdosShoulderEdge[3].rightX == 232);
    CHECK(kOrdosShoulderEdge[4].y == 290);
    CHECK(kOrdosShoulderEdge[4].rightX == 239);
    CHECK(kOrdosShoulderEdge[5].y == 295);
    CHECK(kOrdosShoulderEdge[5].rightX == 243);
    CHECK(kOrdosShoulderEdge[6].y == 300);
    CHECK(kOrdosShoulderEdge[6].rightX == 247);
    CHECK(kOrdosShoulderEdge[7].y == 305);
    CHECK(kOrdosShoulderEdge[7].rightX == 250);
    CHECK(kOrdosShoulderEdge[8].y == 310);
    CHECK(kOrdosShoulderEdge[8].rightX == 254);
    CHECK(kOrdosShoulderEdge[9].y == 315);
    CHECK(kOrdosShoulderEdge[9].rightX == 257);
    CHECK(kOrdosShoulderEdge[10].y == 319);
    CHECK(kOrdosShoulderEdge[10].rightX == 261);
}

TEST_CASE("mentat HD layouts stay inside the 640x480 frame", "[P11]")
{
    for (const NamedMentatHdLayout &entry : kMentatHdLayouts) {
        INFO(entry.name);
        const MentatHdLayout &layout = *entry.layout;
        CHECK(insideFrame(layout.eyes.x, layout.eyes.y, MENTAT_EYES_WIDTH, MENTAT_EYES_HEIGHT));
        CHECK(insideFrame(layout.mouth.x, layout.mouth.y, MENTAT_MOUTH_WIDTH, MENTAT_MOUTH_HEIGHT));
        CHECK(insideFrame(layout.sceneFrame.x, layout.sceneFrame.y, layout.sceneFrame.width, layout.sceneFrame.height));
        CHECK(insideFrame(layout.sceneOpening.x, layout.sceneOpening.y, layout.sceneOpening.width, layout.sceneOpening.height));
    }
}

TEST_CASE("mentat HD scene opening does not cover eyes and mouth", "[P11]")
{
    for (const NamedMentatHdLayout &entry : kMentatHdLayouts) {
        INFO(entry.name);
        const MentatHdLayout &layout = *entry.layout;
        const MentatHdRect eyes = {layout.eyes.x, layout.eyes.y, MENTAT_EYES_WIDTH, MENTAT_EYES_HEIGHT};
        const MentatHdRect mouth = {layout.mouth.x, layout.mouth.y, MENTAT_MOUTH_WIDTH, MENTAT_MOUTH_HEIGHT};
        CHECK_FALSE(intersects(layout.sceneOpening, eyes));
        CHECK_FALSE(intersects(layout.sceneOpening, mouth));
    }
}

TEST_CASE("mentat HD shoulder edges are monotonic and inside the opening", "[P11]")
{
    const auto checkEdge = [](const auto &edge, const MentatHdLayout &layout) {
        for (std::size_t index = 1; index < edge.size(); ++index) {
            const MentatSceneEdgePoint previous = edge[index - 1];
            const MentatSceneEdgePoint next = edge[index];
            CHECK(next.y > previous.y);
            CHECK(next.rightX >= previous.rightX);
        }
        CHECK(edge.front().y >= layout.sceneOpening.y);
        CHECK(edge.back().y <= layout.sceneOpening.y + layout.sceneOpening.height);
    };

    INFO("Атрейдесы");
    checkEdge(kAtreidesShoulderEdge, kAtreidesMentatHdLayout);
    INFO("Ордосы");
    checkEdge(kOrdosShoulderEdge, kOrdosMentatHdLayout);
}

TEST_CASE("mentat HD scene opening rows follow the fork", "[P11]")
{
    const auto checkRow = [](const char *name, const MentatHdLayout &layout, int y, int expectedLeft, int expectedRight) {
        INFO(name);
        INFO("y=" << y);
        const MentatHdRowSpan span = sceneOpeningSpan(layout, y);
        CHECK(span.left == expectedLeft);
        CHECK(span.right == expectedRight);
    };

    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 114, 0, 0);
    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 115, 276, 598);
    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 200, 276, 598);
    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 290, 276, 598);
    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 296, 286, 598);
    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 300, 290, 598);
    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 333, 314, 598);
    checkRow("Атрейдесы", kAtreidesMentatHdLayout, 334, 0, 0);

    checkRow("Ордосы", kOrdosMentatHdLayout, 103, 0, 0);
    checkRow("Ордосы", kOrdosMentatHdLayout, 104, 229, 599);
    checkRow("Ордосы", kOrdosMentatHdLayout, 117, 216, 612);
    checkRow("Ордосы", kOrdosMentatHdLayout, 118, 215, 613);
    checkRow("Ордосы", kOrdosMentatHdLayout, 200, 215, 613);
    checkRow("Ордосы", kOrdosMentatHdLayout, 290, 240, 613);
    checkRow("Ордосы", kOrdosMentatHdLayout, 300, 248, 613);
    checkRow("Ордосы", kOrdosMentatHdLayout, 305, 251, 612);
    checkRow("Ордосы", kOrdosMentatHdLayout, 318, 261, 599);
    checkRow("Ордосы", kOrdosMentatHdLayout, 319, 0, 0);

    checkRow("Харконнены", kHarkonnenMentatHdLayout, 103, 0, 0);
    checkRow("Харконнены", kHarkonnenMentatHdLayout, 104, 229, 599);
    checkRow("Харконнены", kHarkonnenMentatHdLayout, 118, 215, 613);
    checkRow("Харконнены", kHarkonnenMentatHdLayout, 200, 215, 613);
    checkRow("Харконнены", kHarkonnenMentatHdLayout, 305, 216, 612);
    checkRow("Харконнены", kHarkonnenMentatHdLayout, 318, 229, 599);
    checkRow("Харконнены", kHarkonnenMentatHdLayout, 319, 0, 0);

    checkRow("Бене Гессерит", kBeneMentatHdLayout, 104, 229, 599);
    checkRow("Бене Гессерит", kBeneMentatHdLayout, 118, 215, 613);
    checkRow("Бене Гессерит", kBeneMentatHdLayout, 305, 216, 612);
    checkRow("Бене Гессерит", kBeneMentatHdLayout, 318, 229, 599);
}
