#pragma once

#include <SDL2/SDL.h>

#include <algorithm>
#include <array>
#include <cctype>
#include <optional>
#include <string>

enum class CommandBindingAction {
    Attack,
    Repair,
    Unload,
    Deploy,
    Rally,
    Release
};

struct CommandBindings {
    SDL_Scancode attack = SDL_SCANCODE_LCTRL;
    SDL_Scancode repair = SDL_SCANCODE_R;
    SDL_Scancode unload = SDL_SCANCODE_D;
    SDL_Scancode deploy = SDL_SCANCODE_D;
    SDL_Scancode rally = SDL_SCANCODE_LCTRL;
    SDL_Scancode release = SDL_SCANCODE_D;

    bool operator==(const CommandBindings &) const = default;
};

[[nodiscard]] inline bool commandBindingKeysMatch(
    SDL_Scancode first,
    SDL_Scancode second)
{
    if (first == second) {
        return true;
    }
    if ((first == SDL_SCANCODE_LSHIFT || first == SDL_SCANCODE_RSHIFT) &&
        (second == SDL_SCANCODE_LSHIFT || second == SDL_SCANCODE_RSHIFT)) {
        return true;
    }
    return (first == SDL_SCANCODE_LALT || first == SDL_SCANCODE_RALT) &&
        (second == SDL_SCANCODE_LALT || second == SDL_SCANCODE_RALT);
}

[[nodiscard]] inline SDL_Scancode commandBinding(
    const CommandBindings &bindings,
    CommandBindingAction action)
{
    switch (action) {
        case CommandBindingAction::Attack: return bindings.attack;
        case CommandBindingAction::Repair: return bindings.repair;
        case CommandBindingAction::Unload: return bindings.unload;
        case CommandBindingAction::Deploy: return bindings.deploy;
        case CommandBindingAction::Rally: return bindings.rally;
        case CommandBindingAction::Release: return bindings.release;
    }
    return SDL_SCANCODE_UNKNOWN;
}

inline void setCommandBinding(
    CommandBindings &bindings,
    CommandBindingAction action,
    SDL_Scancode scancode)
{
    switch (action) {
        case CommandBindingAction::Attack: bindings.attack = scancode; break;
        case CommandBindingAction::Repair: bindings.repair = scancode; break;
        case CommandBindingAction::Unload: bindings.unload = scancode; break;
        case CommandBindingAction::Deploy: bindings.deploy = scancode; break;
        case CommandBindingAction::Rally: bindings.rally = scancode; break;
        case CommandBindingAction::Release: bindings.release = scancode; break;
    }
}

[[nodiscard]] inline std::optional<CommandBindingAction> trySetCommandBinding(
    CommandBindings &bindings,
    CommandBindingAction action,
    SDL_Scancode scancode)
{
    constexpr std::array actions{
        CommandBindingAction::Attack,
        CommandBindingAction::Repair,
        CommandBindingAction::Unload,
        CommandBindingAction::Deploy,
        CommandBindingAction::Rally,
        CommandBindingAction::Release
    };
    const auto conflict = std::find_if(actions.begin(), actions.end(), [&](const auto candidate) {
        return candidate != action &&
            commandBindingKeysMatch(commandBinding(bindings, candidate), scancode);
    });
    if (conflict != actions.end()) {
        return *conflict;
    }

    setCommandBinding(bindings, action, scancode);
    return std::nullopt;
}

[[nodiscard]] inline SDL_Scancode commandBindingFromIni(
    const std::string &value,
    SDL_Scancode fallback)
{
    const SDL_Scancode parsed = SDL_GetScancodeFromName(value.c_str());
    return parsed == SDL_SCANCODE_UNKNOWN ? fallback : parsed;
}

[[nodiscard]] inline std::string commandBindingToIni(SDL_Scancode scancode)
{
    const char *name = SDL_GetScancodeName(scancode);
    return name && *name ? name : SDL_GetScancodeName(SDL_SCANCODE_UNKNOWN);
}

[[nodiscard]] inline std::string commandBindingDisplayName(
    SDL_Scancode scancode,
    bool english)
{
    switch (scancode) {
        case SDL_SCANCODE_LCTRL:
        case SDL_SCANCODE_RCTRL:
            return "CTRL";
        case SDL_SCANCODE_LSHIFT:
        case SDL_SCANCODE_RSHIFT:
            return "SHIFT";
        case SDL_SCANCODE_LALT:
        case SDL_SCANCODE_RALT:
            return "ALT";
        case SDL_SCANCODE_RETURN:
        case SDL_SCANCODE_KP_ENTER:
            return "ENTER";
        case SDL_SCANCODE_SPACE:
            return english ? "SPACE" : "ПРОБЕЛ";
        default:
            break;
    }

    std::string name = commandBindingToIni(scancode);
    std::ranges::transform(name, name.begin(), [](unsigned char character) {
        return static_cast<char>(std::toupper(character));
    });
    return name;
}
