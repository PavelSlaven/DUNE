#pragma once

#include <algorithm>
#include <cstdlib>
#include <istream>
#include <ostream>
#include <vector>

namespace factory_pad {

inline constexpr int BlockedTicksBeforeCarryall = 600;
inline constexpr int CarryallRetryTicks = 200;
inline constexpr int MaxQueued = 256;

struct Point {
    int x;
    int y;
};

struct CellCoord {
    int x;
    int y;
};

enum class Phase { Empty, Standing, Rolling };
enum class Offer { Appeared, Queued };
enum class StandingAction { None, StartRoll, RequestCarryall };

struct RollTick {
    bool advanced;
    bool done;
};

struct FactoryCandidate {
    int id;
    bool padFree;
};

struct PadState {
    Phase phase = Phase::Empty;
    int unitType = -1;
    int rollUnitId = -1;
    int rollStep = 0;
    int rollTick = 0;
    int blockedTicks = 0;
    int carryallId = -1;
    int carryallRetry = 0;
    std::vector<int> waiting;
};

inline Point padCenter(int width, int height)
{
    return {(width - 1) * 32 + 16, height * 16};
}

inline std::vector<CellCoord> exitCandidates(int x, int y, int width, int height)
{
    const int padColumn = x + width - 1;
    const int below = y + height;
    std::vector<CellCoord> cells{{padColumn, below}, {padColumn + 1, below}, {padColumn - 1, below}};
    for (int row = below - 1; row >= y - 1; --row) {
        cells.push_back({padColumn + 1, row});
    }
    cells.push_back({padColumn, y - 1});
    cells.push_back({padColumn - 1, y - 1});
    return cells;
}

template<class Resolve, class IsFree>
int chooseExitCell(int x, int y, int width, int height, Resolve resolve, IsFree isFree)
{
    for (const CellCoord &candidate : exitCandidates(x, y, width, height)) {
        const int cell = resolve(candidate.x, candidate.y);
        if (cell >= 0 && isFree(cell)) {
            return cell;
        }
    }
    return -1;
}

inline int rollSteps(Point from, Point to)
{
    return std::max(std::abs(to.x - from.x), std::abs(to.y - from.y));
}

namespace detail {
inline int roundedShare(int distance, int step, int steps)
{
    const int numerator = 2 * distance * step + steps;
    const int denominator = 2 * steps;
    int quotient = numerator / denominator;
    if (numerator % denominator < 0) {
        --quotient;
    }
    return quotient;
}
}

inline Point rollPosition(Point from, Point to, int step)
{
    const int steps = rollSteps(from, to);
    if (steps == 0) {
        return from;
    }
    step = std::clamp(step, 0, steps);
    return {from.x + detail::roundedShare(to.x - from.x, step, steps),
            from.y + detail::roundedShare(to.y - from.y, step, steps)};
}

inline void clearStanding(PadState &pad)
{
    pad.rollUnitId = -1;
    pad.rollStep = 0;
    pad.rollTick = 0;
    pad.blockedTicks = 0;
    pad.carryallId = -1;
    pad.carryallRetry = 0;
}

inline Offer offer(PadState &pad, int unitType)
{
    if (pad.phase == Phase::Empty) {
        clearStanding(pad);
        pad.phase = Phase::Standing;
        pad.unitType = unitType;
        return Offer::Appeared;
    }
    if (static_cast<int>(pad.waiting.size()) < MaxQueued) {
        pad.waiting.push_back(unitType);
    }
    return Offer::Queued;
}

inline int finishPad(PadState &pad)
{
    clearStanding(pad);
    if (pad.waiting.empty()) {
        pad.phase = Phase::Empty;
        pad.unitType = -1;
        return -1;
    }
    const int next = pad.waiting.front();
    pad.waiting.erase(pad.waiting.begin());
    pad.phase = Phase::Standing;
    pad.unitType = next;
    return next;
}

inline StandingAction tickStanding(PadState &pad, bool animationFinished, bool exitFree)
{
    if (pad.carryallRetry > 0) {
        --pad.carryallRetry;
    }
    if (!animationFinished) {
        return StandingAction::None;
    }
    if (exitFree) {
        pad.blockedTicks = 0;
        return StandingAction::StartRoll;
    }
    ++pad.blockedTicks;
    if (pad.blockedTicks >= BlockedTicksBeforeCarryall && pad.carryallId < 0 && pad.carryallRetry == 0) {
        pad.carryallRetry = CarryallRetryTicks;
        return StandingAction::RequestCarryall;
    }
    return StandingAction::None;
}

inline void startRoll(PadState &pad, int unitId)
{
    pad.phase = Phase::Rolling;
    pad.rollUnitId = unitId;
    pad.rollStep = 0;
    pad.rollTick = 0;
    pad.blockedTicks = 0;
    pad.carryallId = -1;
    pad.carryallRetry = 0;
}

inline RollTick tickRoll(PadState &pad, int ticksPerPixel, int steps)
{
    if (pad.rollStep >= steps) {
        return {false, true};
    }
    ++pad.rollTick;
    if (pad.rollTick < std::max(1, ticksPerPixel)) {
        return {false, false};
    }
    pad.rollTick = 0;
    ++pad.rollStep;
    return {true, pad.rollStep >= steps};
}

inline int chooseFactory(const std::vector<FactoryCandidate> &factories, int primaryId)
{
    bool primaryListed = false;
    for (const FactoryCandidate &factory : factories) {
        if (factory.id == primaryId) {
            if (factory.padFree) {
                return primaryId;
            }
            primaryListed = true;
        }
    }
    for (const FactoryCandidate &factory : factories) {
        if (factory.padFree) {
            return factory.id;
        }
    }
    if (primaryListed) {
        return primaryId;
    }
    return factories.empty() ? -1 : factories.front().id;
}

inline void write(std::ostream &out, const PadState &pad)
{
    out << static_cast<int>(pad.phase) << ' ' << pad.unitType << ' ' << pad.rollUnitId << ' ' << pad.rollStep << ' '
        << pad.rollTick << ' ' << pad.blockedTicks << ' ' << pad.carryallId << ' ' << pad.carryallRetry << ' '
        << pad.waiting.size();
    for (const int type : pad.waiting) {
        out << ' ' << type;
    }
}

inline bool read(std::istream &in, PadState &pad)
{
    int phase = 0;
    PadState parsed;
    std::size_t waitingCount = 0;
    if (!(in >> phase >> parsed.unitType >> parsed.rollUnitId >> parsed.rollStep >> parsed.rollTick >>
          parsed.blockedTicks >> parsed.carryallId >> parsed.carryallRetry >> waitingCount)) {
        return false;
    }
    if (phase < 0 || phase > 2 || waitingCount > static_cast<std::size_t>(MaxQueued)) {
        return false;
    }
    parsed.phase = static_cast<Phase>(phase);
    for (std::size_t index = 0; index < waitingCount; ++index) {
        int type = 0;
        if (!(in >> type) || type < 0) {
            return false;
        }
        parsed.waiting.push_back(type);
    }
    if (parsed.rollStep < 0 || parsed.rollTick < 0 || parsed.blockedTicks < 0 || parsed.carryallRetry < 0 ||
            parsed.carryallId < -1) {
        return false;
    }
    if (parsed.phase == Phase::Empty && (parsed.unitType != -1 || !parsed.waiting.empty())) {
        return false;
    }
    if (parsed.phase != Phase::Empty && parsed.unitType < 0) {
        return false;
    }
    if (parsed.phase == Phase::Rolling && parsed.rollUnitId < 0) {
        return false;
    }
    pad = parsed;
    return true;
}

}
