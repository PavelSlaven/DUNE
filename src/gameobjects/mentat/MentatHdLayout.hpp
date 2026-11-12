#pragma once

#include <algorithm>
#include <array>
#include <cmath>
#include <cstddef>
#include <span>

struct MentatHdPoint {
    int x;
    int y;
};

struct MentatHdRect {
    int x;
    int y;
    int width;
    int height;
};

struct MentatSceneEdgePoint {
    int y;
    int rightX;
};

struct MentatHdRowSpan {
    int left;
    int right;
};

struct MentatHdLayout {
    MentatHdPoint eyes;
    MentatHdPoint mouth;
    MentatHdRect sceneFrame;
    MentatHdRect sceneOpening;
    int openingCornerHeight;
    std::span<const MentatSceneEdgePoint> shoulderEdge;
};

inline constexpr int MENTAT_HD_FRAME_WIDTH = 640;
inline constexpr int MENTAT_HD_FRAME_HEIGHT = 480;
inline constexpr int MENTAT_EYES_WIDTH = 96;
inline constexpr int MENTAT_EYES_HEIGHT = 32;
inline constexpr int MENTAT_MOUTH_WIDTH = 112;
inline constexpr int MENTAT_MOUTH_HEIGHT = 80;

inline constexpr std::array<MentatSceneEdgePoint, 10> kAtreidesShoulderEdge = {{
    {270, 273}, {290, 273}, {294, 275}, {296, 285}, {300, 289},
    {306, 293}, {314, 297}, {320, 303}, {326, 308}, {334, 314}
}};

inline constexpr std::array<MentatSceneEdgePoint, 11> kOrdosShoulderEdge = {{
    {273, 213}, {276, 218}, {280, 225}, {285, 232}, {290, 239}, {295, 243},
    {300, 247}, {305, 250}, {310, 254}, {315, 257}, {319, 261}
}};

inline constexpr MentatHdLayout kAtreidesMentatHdLayout = {
    {96, 180}, {100, 210}, {234, 95, 400, 243}, {276, 115, 322, 219}, 0, kAtreidesShoulderEdge
};

inline constexpr MentatHdLayout kBeneMentatHdLayout = {
    {96, 180}, {100, 210}, {211, 93, 400, 243}, {215, 104, 398, 215}, 14, {}
};

inline constexpr MentatHdLayout kHarkonnenMentatHdLayout = {
    {96, 180}, {100, 210}, {211, 93, 400, 243}, {215, 104, 398, 215}, 14, {}
};

inline constexpr MentatHdLayout kOrdosMentatHdLayout = {
    {48, 174}, {52, 207}, {211, 93, 400, 243}, {215, 104, 398, 215}, 14, kOrdosShoulderEdge
};

inline MentatHdRowSpan sceneOpeningSpan(const MentatHdLayout &layout, int y)
{
    const MentatHdRect &opening = layout.sceneOpening;
    const int bottom = opening.y + opening.height;
    if (y < opening.y || y >= bottom) {
        return {0, 0};
    }

    int inset = 0;
    if (y < opening.y + layout.openingCornerHeight) {
        inset = opening.y + layout.openingCornerHeight - y;
    }
    else if (y >= bottom - layout.openingCornerHeight) {
        inset = y - (bottom - layout.openingCornerHeight) + 1;
    }

    int left = opening.x + inset;
    const int right = opening.x + opening.width - inset;
    for (std::size_t segment = 0; segment + 1 < layout.shoulderEdge.size(); ++segment) {
        const MentatSceneEdgePoint from = layout.shoulderEdge[segment];
        const MentatSceneEdgePoint to = layout.shoulderEdge[segment + 1];
        if (y < from.y || y >= to.y) {
            continue;
        }
        const double progress = static_cast<double>(y - from.y) / (to.y - from.y);
        const int portraitRight = static_cast<int>(std::lround(from.rightX + (to.rightX - from.rightX) * progress));
        left = std::max(left, portraitRight + 1);
        break;
    }
    return {left, right};
}
