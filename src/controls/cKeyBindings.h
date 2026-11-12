/**
 * @file cKeyBindings.h
 *
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 *
 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
 *
 * This is a non-commercial educational project.
 */

#pragma once

#include <bitset>
#include <map>
#include <vector>
#include <string>
#include <initializer_list>
#include <optional>
#include <SDL3/SDL.h>

#include "controls/eKeyAction.h"
#include "controls/eKeyboardEnum.h"
#include "utils/cIniFile.h"

struct s_KeyBinding {
    std::vector<SDL_Scancode> keys;
    bool requireCtrl  = false;
    bool requireAlt   = false;
    bool requireShift = false;
    bool requireTab   = false;
};

class cKeyBindings {
public:
    void loadDefaults();
    void loadFromSection(const cSection &section);

    /**
     * Returns true when the given key set and modifier combo match the binding for the given action.
     * Called internally by cKeyboardEvent::isAction().
     */
    bool matches(const std::bitset<SDL_SCANCODE_COUNT> &keys, const s_KeysCombo &combo, eKeyAction action) const;

    /**
     * Returns true when the given key set contains one of the keys bound to the given action,
     * ignoring modifiers. Called internally by cKeyboardEvent::involvesActionKey().
     */
    bool containsActionKey(const std::bitset<SDL_SCANCODE_COUNT> &keys, eKeyAction action) const;

    /**
     * Name of the first key bound to the action, for showing it to the player: "Ctrl", "Shift" and "Alt" for
     * the left and right modifier keys, the SDL scancode name otherwise, empty when the action has no key.
     */
    std::string getFirstKeyDisplayName(eKeyAction action) const;

    static const std::vector<std::pair<std::string, eKeyAction>>& getActionTable();

    // Name of the action in [KEYS], empty for an action that is not in the table.
    static std::string getActionName(eKeyAction action);

    // nullptr when the action has no binding.
    const s_KeyBinding *getBinding(eKeyAction action) const;

    void setBinding(eKeyAction action, const s_KeyBinding &binding);

    // The first table action (other than `action`) whose binding is the same key with the same modifiers as the
    // candidate. Left and right Shift are the same key, left and right Alt are the same key, left and right Ctrl
    // are different keys. A pair of actions that share a key in loadDefaults() is never a conflict.
    std::optional<eKeyAction> findConflict(eKeyAction action, const s_KeyBinding &candidate) const;

    // Sets the binding when findConflict() finds nothing; otherwise changes nothing and returns the conflicting action.
    std::optional<eKeyAction> trySetBinding(eKeyAction action, const s_KeyBinding &binding);

    // The pairs of table actions that share a key with the same modifiers in loadDefaults().
    static std::vector<std::pair<eKeyAction, eKeyAction>> getDefaultSharedPairs();

    // The value of the action in [KEYS] format, for example "Ctrl,Z"; empty when the action has no binding.
    std::string toIniValue(eKeyAction action) const;

    // The binding for showing it to the player, for example "Ctrl+Z", "Shift+Tab+F2", "Left Ctrl", "Ctrl".
    static std::string describeBinding(const s_KeyBinding &binding);
    std::string getBindingDisplayName(eKeyAction action) const;

    // The binding made of a captured key and the modifiers held while it was pressed; a modifier that is the
    // captured key itself is not added as a required modifier.
    static s_KeyBinding makeCapturedBinding(SDL_Scancode key, const s_KeysCombo &combo);

    // False for an unknown key, for Tab and for a key whose name contains a comma: they cannot be written to [KEYS].
    static bool canStoreKey(SDL_Scancode key);

private:
    std::map<eKeyAction, s_KeyBinding> m_bindings;

    void bind(eKeyAction action, std::initializer_list<SDL_Scancode> keys,
              bool requireCtrl = false, bool requireAlt = false, bool requireShift = false,
              bool requireTab = false);

    static s_KeyBinding parseBinding(const std::string &value);
    void checkForClashes() const;
};
