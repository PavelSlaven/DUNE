#define SDL_MAIN_HANDLED
#include "controls/CommandBindings.hpp"
#include "controls/cKeyboardEvent.h"

#include <set>

int main()
{
    CommandBindings bindings;
    if (commandBinding(bindings, CommandBindingAction::Attack) != SDL_SCANCODE_LCTRL) return 1;
    if (commandBindingDisplayName(bindings.attack, true) != "CTRL") return 2;
    if (commandBindingDisplayName(SDL_SCANCODE_SPACE, false) != "ПРОБЕЛ") return 3;

    setCommandBinding(bindings, CommandBindingAction::Repair, SDL_SCANCODE_F);
    if (bindings.repair != SDL_SCANCODE_F) return 4;
    if (commandBindingFromIni(commandBindingToIni(bindings.repair), SDL_SCANCODE_R) !=
        SDL_SCANCODE_F) return 5;
    if (commandBindingFromIni("not-a-real-key", SDL_SCANCODE_R) != SDL_SCANCODE_R) return 6;
    std::set<SDL_Scancode> rightControl{SDL_SCANCODE_RCTRL};
    const cKeyboardEvent modifierEvent(eKeyEventType::HOLD, rightControl);
    if (!modifierEvent.hasAssignedKey(SDL_SCANCODE_LCTRL)) return 7;
    return 0;
}
