#pragma once

enum class ActiveCommandMode {
    Normal,
    ForceAttack,
    Rally,
    Repair
};

enum class PointerMoveCommandPolicy {
    Reevaluate,
    Preserve
};

enum class RightClickCommandPolicy {
    DefaultAction,
    CancelCommand
};

[[nodiscard]] constexpr PointerMoveCommandPolicy pointerMoveCommandPolicy(
    ActiveCommandMode mode
) {
    return mode == ActiveCommandMode::ForceAttack
        ? PointerMoveCommandPolicy::Preserve
        : PointerMoveCommandPolicy::Reevaluate;
}

[[nodiscard]] constexpr RightClickCommandPolicy rightClickCommandPolicy(
    ActiveCommandMode mode
) {
    return mode == ActiveCommandMode::ForceAttack ||
           mode == ActiveCommandMode::Rally ||
           mode == ActiveCommandMode::Repair
        ? RightClickCommandPolicy::CancelCommand
        : RightClickCommandPolicy::DefaultAction;
}
