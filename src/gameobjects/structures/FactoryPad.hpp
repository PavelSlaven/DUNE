#pragma once

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

inline Point padCenter(int, int)
{
    return {0, 0};
}

inline std::vector<CellCoord> exitCandidates(int, int, int, int)
{
    return {};
}

template<class Resolve, class IsFree>
int chooseExitCell(int, int, int, int, Resolve, IsFree)
{
    return -1;
}

inline int rollSteps(Point, Point)
{
    return 0;
}

inline Point rollPosition(Point from, Point, int)
{
    return from;
}

inline Offer offer(PadState &, int)
{
    return Offer::Queued;
}

inline int finishPad(PadState &)
{
    return -1;
}

inline StandingAction tickStanding(PadState &, bool, bool)
{
    return StandingAction::None;
}

inline void startRoll(PadState &, int)
{
}

inline RollTick tickRoll(PadState &, int, int)
{
    return {false, false};
}

inline int chooseFactory(const std::vector<FactoryCandidate> &, int)
{
    return -1;
}

inline void write(std::ostream &, const PadState &)
{
}

inline bool read(std::istream &, PadState &)
{
    return false;
}

}
