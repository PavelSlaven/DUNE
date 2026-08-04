#pragma once

#include <string>
#include <set>
#include <format>

#include "utils/cPoint.h"
#include "enums.h"
#include "utils/common.h"

enum class eKeyEventType {
    NONE,
    /**
     * key is being pressed down (hold)
     */
    HOLD,
    /**
     * key is held, then released. Makes a key "pressed".
     */
    PRESSED,
};

class cKeyboardEvent {

public:
    cKeyboardEvent(eKeyEventType eventType, std::set<SDL_Scancode> &keys);

    eKeyEventType eventType = eKeyEventType::NONE;

    inline const std::string toString() const {
        std::string str= std::format("cKeyboardEvent [type={}], keys: ", toStringKeyboardEventType(eventType));
        str.append("[");
        for (auto aKey : keys) {
            str.append(SDL_GetScancodeName(aKey));
        }
        str.append("]");

        return str;
    }

    bool hasKey(SDL_Scancode scanCode) const {
        return keys.find(scanCode) != keys.end();
    }

    /**
     * Returns true when both scancodes are present in this event
     * @param firstScanCode
     * @param secondScanCode
     * @return
     */
    bool hasKeys(SDL_Scancode firstScanCode, SDL_Scancode secondScanCode) const {
        return hasKey(firstScanCode) && hasKey(secondScanCode);
    }

    /**
     * Returns true when one of both scancodes are present in this event
     * @param firstScanCode
     * @param secondScanCode
     * @return
     */
    bool hasEitherKey(SDL_Scancode firstScanCode, SDL_Scancode secondScanCode) const {
        return hasKey(firstScanCode) || hasKey(secondScanCode);
    }

    bool hasAssignedKey(SDL_Scancode scanCode) const {
        switch (scanCode) {
            case SDL_SCANCODE_LCTRL:
            case SDL_SCANCODE_RCTRL:
                return hasEitherKey(SDL_SCANCODE_LCTRL, SDL_SCANCODE_RCTRL);
            case SDL_SCANCODE_LSHIFT:
            case SDL_SCANCODE_RSHIFT:
                return hasEitherKey(SDL_SCANCODE_LSHIFT, SDL_SCANCODE_RSHIFT);
            case SDL_SCANCODE_LALT:
            case SDL_SCANCODE_RALT:
                return hasEitherKey(SDL_SCANCODE_LALT, SDL_SCANCODE_RALT);
            default:
                return hasKey(scanCode);
        }
    }

    bool isType(eKeyEventType type) const {
        return eventType == type;
    }

    /**
     * If a numerical key is pressed, return that value.
     * @return
     */
    int getGroupNumber() const;

    [[nodiscard]] SDL_Scancode firstKey() const {
        return keys.empty() ? SDL_SCANCODE_UNKNOWN : *keys.begin();
    }

private:
    inline const char *toStringKeyboardEventType(const eKeyEventType &type) const {
        switch (type) {
            case eKeyEventType::NONE:
                return "NONE";
            case eKeyEventType::HOLD:
                return "HOLD";
            case eKeyEventType::PRESSED:
                return "PRESSED";
            default:
                assert(false);
                break;
        }
        return "";
    }

    std::set<SDL_Scancode> keys;
};
