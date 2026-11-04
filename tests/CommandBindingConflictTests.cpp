#define SDL_MAIN_HANDLED
#include "controls/CommandBindings.hpp"
#include "controls/cKeyboardEvent.h"

#include <set>

int main()
{
    CommandBindings bindings;
    setCommandBinding(bindings, CommandBindingAction::Attack, SDL_SCANCODE_A);
    setCommandBinding(bindings, CommandBindingAction::Repair, SDL_SCANCODE_B);

    const auto conflict = trySetCommandBinding(
        bindings,
        CommandBindingAction::Attack,
        SDL_SCANCODE_B
    );
    if (conflict != CommandBindingAction::Repair) return 1;
    if (commandBinding(bindings, CommandBindingAction::Attack) != SDL_SCANCODE_A) return 2;
    if (commandBinding(bindings, CommandBindingAction::Repair) != SDL_SCANCODE_B) return 3;

    setCommandBinding(bindings, CommandBindingAction::Attack, SDL_SCANCODE_LCTRL);
    if (trySetCommandBinding(
            bindings,
            CommandBindingAction::Repair,
            SDL_SCANCODE_RCTRL)) {
        return 4;
    }
    if (commandBinding(bindings, CommandBindingAction::Repair) != SDL_SCANCODE_RCTRL) return 5;

    std::set<SDL_Scancode> leftControl{SDL_SCANCODE_LCTRL};
    const cKeyboardEvent leftControlEvent(eKeyEventType::HOLD, leftControl);
    if (!leftControlEvent.hasAssignedKey(SDL_SCANCODE_LCTRL)) return 6;
    if (leftControlEvent.hasAssignedKey(SDL_SCANCODE_RCTRL)) return 7;

    return 0;
}
