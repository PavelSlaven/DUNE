#include "gamestates/CampaignMapLayout.hpp"

#include <array>
#include <cassert>

int main()
{
    constexpr std::array<std::array<int, 2>, 4> resolutions{{
        {{800, 600}},
        {{1067, 600}},
        {{1920, 1080}},
        {{3413, 960}}
    }};

    for (const auto &resolution : resolutions) {
        const auto layout = CampaignMapLayout::create(
            resolution[0],
            resolution[1]
        );
        assert(layout.panel.getX() >= 0);
        assert(layout.panel.getY() >= 0);
        assert(layout.panel.getEndX() <= resolution[0]);
        assert(layout.panel.getEndY() <= resolution[1]);
        assert(layout.map.getWidth() >= 320);
        assert(layout.map.getHeight() >= 126);
        assert(layout.title.getEndY() <= layout.map.getY());
        assert(layout.map.getEndY() <= layout.message.getY());
        assert(layout.message.getEndY() <= layout.missionButton.getY());

        const auto wholeMap = layout.regionDestination(
            CampaignMapLayout::SourceMapX,
            CampaignMapLayout::SourceMapY,
            CampaignMapLayout::SourceMapWidth,
            CampaignMapLayout::SourceMapHeight
        );
        assert(wholeMap.getX() == layout.map.getX());
        assert(wholeMap.getY() == layout.map.getY());
        assert(wholeMap.getWidth() == layout.map.getWidth());
        assert(wholeMap.getHeight() == layout.map.getHeight());

        assert(layout.clickMapX(layout.map.getX(), 608) == 0);
        assert(layout.clickMapY(layout.map.getY(), 240) == 0);
        assert(layout.clickMapX(layout.map.getEndX(), 608) == 607);
        assert(layout.clickMapY(layout.map.getEndY(), 240) == 239);
    }
}
