# Задание P10C — страницы настроек «Игра», «Управление», «Диагностика», переназначение клавиш, строки «Разрешение» и «Полный экран», опись клавиш (шаг П10, часть в)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p10c`, ветка `codex/p10c`, `HEAD` — вершина ветки порта `port/up-d06f2fcd` после слияния П8 (дерево равно ревизии `B`; sha подставляет ведущий при запуске). Файлы Git LFS в этой рабочей копии — настоящие данные; шаг их не меняет и новых не берёт. Временные файлы — в `.tmp/p10c/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p10c/` (дальше — «папка задания»).

## Цель

Окно настроек имеет четыре страницы с вкладками: «Основные» (нынешняя страница), «Игра», «Управление», «Диагностика». Кнопка «More settings» («Ещё настройки») на «Основных» открывает «Игру». На «Основных» есть строки «Разрешение» и «Полный экран»; их выбор после «Apply» пишется в `preferences.ini` и действует после перезапуска игры. Семь настроек «Игры» и восемь настроек «Диагностики» после «Apply» пишутся в `preferences.ini`, читаются при каждом запуске и (кроме камеры и паузы при потере фокуса) действуют сразу. Страница «Управление» показывает все 86 действий таблицы клавиш игры (`cKeyBindings`), позволяет назначить действию новую клавишу с модификаторами (щелчок по кнопке, нажатие клавиши; `Escape` отменяет захват), не принимает клавишу, занятую другим действием, и после «Apply» применяет привязки сразу и пишет их в раздел `[KEYS]` файла `preferences.ini`; при запуске `[KEYS]` из `preferences.ini` накладывается поверх `[KEYS]` из `settings.ini`. Опись клавиш режима отладки (`extract_keys.py`, `check_keys.py`, `keys.tsv`) собрана заново по клавишам порта. Готово, когда новые тесты Catch2 и Python, сборка со всеми тестами и скрипты режима отладки интерфейса из раздела «Проверки» зелёные.

## Что уже решено

Ревизия `B` = `d95953ef9c46408d25a8782a2c38e4cfb30abbc6` (ветка порта со всеми шагами П8, П9, П10а, П10б, П11), ревизия форка `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`, апстрим `UP1` = `d06f2fcd2a347182c3774fb96e9a85570405c489`. Все факты о коде порта ниже — о файлах ревизии `B`; номера строк `FORK1` — той ревизии.

Решения владельца (Р80, 2026-11-12): настройки «Игры» и «Диагностики» сохраняются в `preferences.ini` в папке пользователя и читаются при каждом запуске, как масштабы и язык; «Управление» переназначает все действия таблицы клавиш игры, а не шесть приказов форка; изменения пишутся в раздел `[KEYS]` файла `preferences.ini` и при запуске накладываются поверх `[KEYS]` из `settings.ini`; на «Основных» появляются строки «Разрешение» и «Полный экран», выбор сохраняется и действует после перезапуска. Класс `CommandBindings` форка в порт не переносится: шесть команд форка — четыре действия порта (Attack и Rally — `ATTACK_MODE`, Repair — `REPAIR_UNIT`, Unload — `SEND_TO_REFINERY`, Deploy и Release — `DEPLOY_UNIT`). Новый вид окна настроек делает переработка интерфейса позже: здесь — виджеты и тема порта (`GuiButton`, `GuiTheme::Remaster()`).

Факты порта:

- Окно настроек — `src/gamestates/cOptionsState.cpp` (740 строк) и `.h`: одна страница; `thinkFast` пуст; `onNotifyKeyboardEvent` только передаёт события диалогу сохранений; кнопка «More settings» создана с `withEnabled(false)` и без обработчика; строк «Разрешение» и «Полный экран» нет. Состояние создаётся лениво (`cCreatorState`, `cOptionsState(m_services, текущее состояние)`), при повторном входе вызываются `setPrevState` или `refresh`. Диалог сохранений П8 (`SaveSlotsDialog`, кнопки «Save game», «Load game») уже в `B`.
- Раскладка `src/gamestates/OptionsMenuLayout.hpp`: строки содержимого 1–8, строка 9 — надпись режима читов, строка 10 — «Apply»; точные значения заморожены тестом `tests/utils/test_OptionsMenu.cpp`.
- Таблица клавиш: `src/controls/cKeyBindings.cpp`, `getActionTable()` — 86 пар (имя в `[KEYS]`, `eKeyAction`); имя действия `REPAIR_UNIT` в таблице — `REPAIR`. В `loadDefaults()` 98 привязок; 12 из них (`GROUP_ASSIGN_1..6`, `GROUP_ADDTOSEL_1..6`) в таблице нет и в окне настроек не показываются. Привязка — `s_KeyBinding {keys, requireCtrl, requireAlt, requireShift, requireTab}`. `loadFromSection(const cSection&)` заменяет привязку действия целиком и по концу вызывает `checkForClashes()` (только предупреждения в журнал). `parseBinding` читает значения `[KEYS]`: токены `alt`, `ctrl`, `shift`, `tab` без учёта регистра — модификаторы, остальные — имена скан-кодов SDL, через запятую; поэтому клавиша `Tab` и клавиша, чьё имя содержит запятую, в `[KEYS]` не записываются.
- События клавиатуры: `cKeyboard::updateState()` шлёт событие `PRESSED` по отпусканию клавиши (набор отпущенных клавиш и текущие модификаторы), `HOLD` — пока клавиша нажата; текстовые события имеют пустой набор клавиш и непустой `getTextInput()`. `cGame::onNotifyKeyboardEvent` после `m_currentState->onNotifyKeyboardEvent(event)` проверяет `m_currentState->isKeyboardCapturedByUi()`: при `true` глобальные действия игры (снимок экрана, `Alt+Enter` и другие) событие не получают.
- `cKeyboard::getKeyBindings()` — `const cKeyBindings*`; `loadKeyBindings` пересоздаёт объект `cKeyBindings`; `cKeyboardEvent` хранит указатель на тот же объект, поэтому присваивание `*getKeyBindings() = другой объект` обновляет привязки без пересоздания. `[KEYS]` читается в `cGame::setupGame` (`src/game/cGame_logic.cpp`, блок `if (settings->hasSection("KEYS"))`, перед строкой `m_services->keyboard = m_keyboard.get();`).
- `Preferences` (`src/game/Preferences.hpp/.cpp`): файл `preferences.ini`, раздел `[SETTINGS]`; `load` читает все ключи, `save` пишет все 28 ключей в новый файл (раздел `[KEYS]` стирается), `saveScales` и `saveLanguage` через `loadIni` требуют раздела `[SETTINGS]` (иначе пишут в новый файл). В `src/main.cpp`: масштабы и язык читаются при каждом запуске (`Preferences::loadScales`, `loadLanguage`), остальное — только с `-prefs`; аргументы командной строки идут после; при выходе `Preferences::save(*prefsFile, game.currentSettings(), ...)` пишет все ключи. Тесты `tests/utils/test_Preferences.cpp` заморожены (в том числе круговой обход `save` → `load`).
- `cGameSettings` (`src/game/cGameSettings.h`): геттеры диагностических флагов есть, сеттеров нет; `m_allowRepeatingReinforcements` без сеттера; `m_windowed` и `isWindowed()` есть, но поле нигде не заполняется; скорости и флаг края камеры, флаг паузы при потере фокуса и признак окна хранит `cGame` (`m_cameraEdgeMove`, `m_cameraDragMoveSpeed`, `m_cameraBorderOrKeyMoveSpeed`, `m_pauseWhenLosingFocus`, `m_windowed`), желаемый размер окна — `m_initialGameSettings->screenW/H`; `cGameSettings::m_screenW/H` после запуска — реальный размер холста. Камера и менеджер фокуса создаются при запуске по этим полям (`cGame_logic.cpp`: `std::make_unique<cMapCamera>(...)` и `m_focusManager->setEnabled(m_pauseWhenLosingFocus)`), поэтому эти значения действуют только после перезапуска.
- Размер окна при запуске: `cSDLSystem(m_gameSettings->m_screenW, m_gameSettings->m_screenH, title, m_windowed)` в `cGame::setupGame` берёт значения из `InitialGameSettings` (`screenW`, `screenH`, `windowed`), заполненных в `src/main.cpp` из `settings.ini`, `preferences.ini` и аргументов командной строки (`-screenWidth`, `-screenHeight`, `-fullscreen`, `-windowed`). `ScreenWidth × ScreenHeight` — желаемый размер окна; размер рабочего стола порт берёт через `SDL_GetDisplayBounds(SDL_GetPrimaryDisplay(), ...)` (`cSDLSystem::getWindowResolution`).
- Режим отладки интерфейса: `friend class UiAuditAccess` у `cOptionsState`; сцены `options-menu-*` (`tests/ui_audit/ui_audit_part2_catalog.py`, `EXPECTED_COUNT = 107`) и `options-game-main-saves`, `options-game-main-nosaves`, `options-game-applied` (`tests/ui_audit/ui_audit_part3a_catalog.py`, `EXPECTED_COUNT = 25`). Скрипты запуска игры дают каждому запуску свою `XDG_DATA_HOME`, поэтому `preferences.ini` пользователя сцены не затрагивает.
- Источник страниц и тестов форка (`FORK1`): `src/gamestates/AdvancedOptionsHeaderLayout.hpp` (33 строки), `src/gamestates/cOptionsState.cpp` (функции и строки, названные в контракте), `tests/CommandBindingConflictTests.cpp` (7 проверок), `tests/InteractionRegressionTests.cpp` (строки 31–36, одна проверка заголовка), `tools/ui-audit/extract_keys.py` (92 строки), `check_keys.py` (126), `tests/test_extract_keys.py` (8 случаев), `tests/test_check_keys.py` (23), `keys.tsv` (168 строк).

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом; пути без `/srv/` — от корня рабочей копии:

- `src/controls/cKeyBindings.h` целиком; `src/controls/cKeyBindings.cpp` целиком;
- `src/controls/cKeyboard.h` целиком; `src/controls/cKeyboard.cpp` строки 52–131; `src/controls/cKeyboardEvent.h` целиком; `src/controls/cKeyboardEvent.cpp` строки 1–80;
- `src/game/Preferences.hpp` целиком; `src/game/Preferences.cpp` целиком; `src/game/PreferencesPath.hpp` целиком; `src/utils/cIniFile.h` целиком;
- `src/game/cGameSettings.h` целиком; `src/game/cGame_logic.cpp` строки 150–220, 320–400, 770–810, 1595–1615; `src/main.cpp` строки 76–190;
- `src/gamestates/cOptionsState.h` и `src/gamestates/cOptionsState.cpp` целиком; `src/gamestates/OptionsMenuLayout.hpp` целиком; `src/gui/GuiWindow.h` целиком;
- `src/include/sGameServices.h` целиком; `src/controls/sMouseEvent.h` строки 1–40;
- `src/debug/UiAudit.hpp` строки 60–110; `src/debug/UiAuditAccess.cpp` строки 170–195; `src/debug/UiAuditScenes.cpp` строки 195–230, 280–330, 470–515;
- `tests/CMakeLists.txt` строки 1–60; `tests/utils/test_Preferences.cpp` целиком; `tests/controls/test_cKeyBindings.cpp` строки 1–60; `tests/utils/test_OptionsMenu.cpp` строки 1–60;
- `tests/ui_audit/ui_audit_part3a_catalog.py` целиком; `tests/ui_audit/ui_audit_part3a_scenes.py` целиком; `tests/ui_audit/data/latin-ru-allowed.tsv` целиком;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>` для: `src/gamestates/AdvancedOptionsHeaderLayout.hpp`, `src/gamestates/cOptionsState.h`, `tests/CommandBindingConflictTests.cpp`, `tools/ui-audit/extract_keys.py`, `tools/ui-audit/check_keys.py`, `tools/ui-audit/tests/test_extract_keys.py`, `tools/ui-audit/tests/test_check_keys.py`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp | sed -n '36,100p;270,560p;640,760p;1057,1130p;1260,1310p;1390,1402p;1435,1510p'`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/InteractionRegressionTests.cpp | sed -n '1,40p'`; вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/keys.tsv | head -40`.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт поведения

Правила переноса строк форка — в пункте 13. Новый код ниже — точный текст; где пункт называет функцию форка и её строки, тело переносится по правилам пункта 13.

### 1. `cKeyBindings`, `cKeyboard`, `cKeyboardEvent`

`src/controls/cKeyBindings.h`:

- после строки `#include <initializer_list>` — строка `#include <optional>`;
- строка `    static const std::vector<std::pair<std::string, eKeyAction>>& getActionTable();` удаляется из раздела `private:`;
- после строки `    std::string getFirstKeyDisplayName(eKeyAction action) const;` и пустой строки после неё в раздел `public:` добавляются строки:

```cpp
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

```

(Комментарии к этим объявлениям — единственные новые комментарии пункта 1; в `.cpp` комментариев нет.)

`src/controls/cKeyBindings.cpp`:

- в блоке подключений после строки `#include <tuple>` — пустая строка и анонимное пространство имён:

```cpp
namespace {

bool isSameKey(SDL_Scancode first, SDL_Scancode second)
{
    if (first == second) {
        return true;
    }
    const auto isShift = [](SDL_Scancode sc) { return sc == SDL_SCANCODE_LSHIFT || sc == SDL_SCANCODE_RSHIFT; };
    const auto isAlt = [](SDL_Scancode sc) { return sc == SDL_SCANCODE_LALT || sc == SDL_SCANCODE_RALT; };
    return (isShift(first) && isShift(second)) || (isAlt(first) && isAlt(second));
}

bool bindingsOverlap(const s_KeyBinding &first, const s_KeyBinding &second)
{
    if (first.requireCtrl != second.requireCtrl || first.requireAlt != second.requireAlt ||
        first.requireShift != second.requireShift || first.requireTab != second.requireTab) {
        return false;
    }
    for (SDL_Scancode firstKey : first.keys) {
        for (SDL_Scancode secondKey : second.keys) {
            if (isSameKey(firstKey, secondKey)) {
                return true;
            }
        }
    }
    return false;
}

std::string keyName(SDL_Scancode scancode)
{
    const char *name = SDL_GetScancodeName(scancode);
    return name != nullptr ? name : "";
}

}
```

- сразу после функции `cKeyBindings::getFirstKeyDisplayName` (перед функцией `cKeyBindings::bind`) добавляются определения:

```cpp
std::string cKeyBindings::getActionName(eKeyAction action)
{
    for (const auto &[name, candidate] : getActionTable()) {
        if (candidate == action) {
            return name;
        }
    }
    return "";
}

const s_KeyBinding *cKeyBindings::getBinding(eKeyAction action) const
{
    const auto it = m_bindings.find(action);
    return it == m_bindings.end() ? nullptr : &it->second;
}

void cKeyBindings::setBinding(eKeyAction action, const s_KeyBinding &binding)
{
    m_bindings[action] = binding;
}

std::vector<std::pair<eKeyAction, eKeyAction>> cKeyBindings::getDefaultSharedPairs()
{
    cKeyBindings defaults;
    defaults.loadDefaults();
    const auto &table = getActionTable();
    std::vector<std::pair<eKeyAction, eKeyAction>> pairs;
    for (std::size_t first = 0; first < table.size(); ++first) {
        for (std::size_t second = first + 1; second < table.size(); ++second) {
            const s_KeyBinding *firstBinding = defaults.getBinding(table[first].second);
            const s_KeyBinding *secondBinding = defaults.getBinding(table[second].second);
            if (firstBinding != nullptr && secondBinding != nullptr && bindingsOverlap(*firstBinding, *secondBinding)) {
                pairs.emplace_back(table[first].second, table[second].second);
            }
        }
    }
    return pairs;
}

std::optional<eKeyAction> cKeyBindings::findConflict(eKeyAction action, const s_KeyBinding &candidate) const
{
    static const std::vector<std::pair<eKeyAction, eKeyAction>> sharedPairs = getDefaultSharedPairs();
    const auto isSharedPair = [action](eKeyAction other) {
        return std::any_of(sharedPairs.begin(), sharedPairs.end(), [action, other](const auto &pair) {
            return (pair.first == action && pair.second == other) || (pair.first == other && pair.second == action);
        });
    };
    for (const auto &[name, other] : getActionTable()) {
        if (other == action || isSharedPair(other)) {
            continue;
        }
        const s_KeyBinding *binding = getBinding(other);
        if (binding != nullptr && bindingsOverlap(candidate, *binding)) {
            return other;
        }
    }
    return std::nullopt;
}

std::optional<eKeyAction> cKeyBindings::trySetBinding(eKeyAction action, const s_KeyBinding &binding)
{
    const std::optional<eKeyAction> conflict = findConflict(action, binding);
    if (!conflict) {
        setBinding(action, binding);
    }
    return conflict;
}

std::string cKeyBindings::toIniValue(eKeyAction action) const
{
    const s_KeyBinding *binding = getBinding(action);
    if (binding == nullptr) {
        return "";
    }
    std::string value;
    const auto append = [&value](const std::string &token) {
        if (!value.empty()) {
            value += ",";
        }
        value += token;
    };
    if (binding->requireCtrl) append("Ctrl");
    if (binding->requireAlt) append("Alt");
    if (binding->requireShift) append("Shift");
    if (binding->requireTab) append("Tab");
    for (SDL_Scancode scancode : binding->keys) {
        append(keyName(scancode));
    }
    return value;
}

std::string cKeyBindings::describeBinding(const s_KeyBinding &binding)
{
    std::string text;
    if (binding.requireCtrl) text += "Ctrl+";
    if (binding.requireAlt) text += "Alt+";
    if (binding.requireShift) text += "Shift+";
    if (binding.requireTab) text += "Tab+";
    const auto contains = [&binding](SDL_Scancode scancode) {
        return std::find(binding.keys.begin(), binding.keys.end(), scancode) != binding.keys.end();
    };
    std::string keys;
    const auto append = [&keys](const std::string &name) {
        if (!keys.empty()) {
            keys += " / ";
        }
        keys += name;
    };
    const auto appendGroup = [&](SDL_Scancode scancode, SDL_Scancode left, SDL_Scancode right, const char *name) {
        if ((scancode != left && scancode != right) || !contains(left) || !contains(right)) {
            return false;
        }
        if (scancode == left) {
            append(name);
        }
        return true;
    };
    for (SDL_Scancode scancode : binding.keys) {
        if (appendGroup(scancode, SDL_SCANCODE_LCTRL, SDL_SCANCODE_RCTRL, "Ctrl") ||
            appendGroup(scancode, SDL_SCANCODE_LSHIFT, SDL_SCANCODE_RSHIFT, "Shift") ||
            appendGroup(scancode, SDL_SCANCODE_LALT, SDL_SCANCODE_RALT, "Alt")) {
            continue;
        }
        append(keyName(scancode));
    }
    return text + keys;
}

std::string cKeyBindings::getBindingDisplayName(eKeyAction action) const
{
    const s_KeyBinding *binding = getBinding(action);
    return binding == nullptr ? "" : describeBinding(*binding);
}

s_KeyBinding cKeyBindings::makeCapturedBinding(SDL_Scancode key, const s_KeysCombo &combo)
{
    s_KeyBinding binding;
    binding.keys = {key};
    const bool keyIsCtrl = key == SDL_SCANCODE_LCTRL || key == SDL_SCANCODE_RCTRL;
    const bool keyIsAlt = key == SDL_SCANCODE_LALT || key == SDL_SCANCODE_RALT;
    const bool keyIsShift = key == SDL_SCANCODE_LSHIFT || key == SDL_SCANCODE_RSHIFT;
    binding.requireCtrl = combo.ctrlPressed && !keyIsCtrl;
    binding.requireAlt = combo.altPressed && !keyIsAlt;
    binding.requireShift = combo.shiftPressed && !keyIsShift;
    binding.requireTab = combo.tabPressed && key != SDL_SCANCODE_TAB;
    return binding;
}

bool cKeyBindings::canStoreKey(SDL_Scancode key)
{
    if (key <= SDL_SCANCODE_UNKNOWN || key >= SDL_SCANCODE_COUNT || key == SDL_SCANCODE_TAB) {
        return false;
    }
    const std::string name = keyName(key);
    return !name.empty() && name.find(',') == std::string::npos;
}
```

`src/controls/cKeyboard.h`: после строки `    [[nodiscard]] const cKeyBindings *getKeyBindings() const { return m_keyBindings.get(); }` — строка `    [[nodiscard]] cKeyBindings *getKeyBindings() { return m_keyBindings.get(); }`.

`src/controls/cKeyboardEvent.h`: в раздел `public:` после строки `    bool hasKeys(SDL_Scancode firstScanCode, SDL_Scancode secondScanCode) const;` и пустой строки после неё — строки:

```cpp
    // The lowest scancode of the event, SDL_SCANCODE_UNKNOWN when the event has no key (text input).
    SDL_Scancode getFirstKey() const;

    const s_KeysCombo &getCombo() const;

```

`src/controls/cKeyboardEvent.cpp`: после определения `cKeyboardEvent::isType` (перед `cKeyboardEvent::isAction`) — определения:

```cpp
SDL_Scancode cKeyboardEvent::getFirstKey() const
{
    for (int scancode = 0; scancode < SDL_SCANCODE_COUNT; ++scancode) {
        if (m_keys.test(static_cast<size_t>(scancode))) {
            return static_cast<SDL_Scancode>(scancode);
        }
    }
    return SDL_SCANCODE_UNKNOWN;
}

const s_KeysCombo &cKeyboardEvent::getCombo() const
{
    return m_combo;
}
```

### 2. `Preferences`

`src/game/Preferences.hpp`:

- после строки `#include <filesystem>` — строки `#include <array>`, `#include <span>`, `#include <string_view>`, `#include <utility>`, `#include <vector>` (подряд, строка `#include <string>` остаётся после них);
- перед строкой `}` (закрытие пространства имён, последняя строка файла) — строки:

```cpp
// The values the options menu lets the player choose: read on every start, written only by the options menu.
inline constexpr std::array<std::string_view, 21> CHOSEN_KEYS = {
    "RenderScale", "WorldScale", "Language", "ScreenWidth", "ScreenHeight", "FullScreen",
    "CameraEdgeMove", "CameraBorderOrKeyMoveSpeed", "CameraDragMoveSpeed", "pauseWhenLosingFocus",
    "AllowRepeatingReinforcements", "AllTurretsDownOnLowPower", "RocketTurretsDownOnLowPower",
    "Debug", "NoAI", "oneAi", "disableWormAi", "disableReinforcements", "noAiRest", "drawUnitDebug", "drawUsages",
};

using KeyValues = std::vector<std::pair<std::string, std::string>>;

// Loads only the chosen keys over the settings; the other settings stay as they are.
bool loadChosenOptions(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);

// The text values of the given settings keys in the order of `keys`; a key that is not a settings key is skipped.
KeyValues valuesOf(const InitialGameSettings &settings, std::span<const std::string_view> keys);

// Writes the values to [SETTINGS] and keeps every other key and section of the file.
bool saveValues(const std::filesystem::path &file, const KeyValues &values, std::string &error);

// The save at the end of the game: writes every setting except the chosen keys and keeps the chosen keys and
// every other section of the file as they are.
bool saveOnExit(const std::filesystem::path &file, const InitialGameSettings &settings, std::string &error);

// The [KEYS] section of the file; false when the file has no such section.
bool loadKeyBindings(const std::filesystem::path &file, cSection &section, std::string &error);

// Writes the values to [KEYS] and keeps every other key and section of the file.
bool saveKeyBindings(const std::filesystem::path &file, const KeyValues &values, std::string &error);

```

`src/game/Preferences.cpp`:

- в анонимном пространстве имён функция `loadIni` заменяется двумя функциями:

```cpp
bool loadAnyIni(const std::filesystem::path &file, cIniFile &ini, std::string &error)
{
    std::error_code filesystemError;
    if (!std::filesystem::exists(file, filesystemError)) {
        error = "No preferences file found at " + utf8FileName(file);
        return false;
    }

    if (!ini.load(utf8FileName(file))) {
        error = "Preferences file is unusable: " + utf8FileName(file);
        return false;
    }
    return true;
}

bool loadIni(const std::filesystem::path &file, cIniFile &ini, std::string &error)
{
    if (!loadAnyIni(file, ini, error)) {
        return false;
    }
    if (!ini.hasSection(SECTION)) {
        error = "Preferences file is unusable: " + utf8FileName(file);
        return false;
    }
    return true;
}
```

- после функции `writeIni` (внутри того же анонимного пространства) добавляются:

```cpp
constexpr const char *KEYS_SECTION = "KEYS";

KeyValues settingsValues(const InitialGameSettings &settings)
{
    return {
        {"ScreenWidth", std::to_string(settings.screenW)},
        {"ScreenHeight", std::to_string(settings.screenH)},
        {"CameraDragMoveSpeed", std::to_string(settings.cameraDragMoveSpeed)},
        {"CameraBorderOrKeyMoveSpeed", std::to_string(settings.cameraBorderOrKeyMoveSpeed)},
        {"FullScreen", toText(!settings.windowed)},
        {"CameraEdgeMove", toText(settings.cameraEdgeMove)},
        {"RenderScale", std::to_string(settings.renderScalePercent)},
        {"WorldScale", std::to_string(settings.worldScalePercent)},
        {"Language", settings.language},
        {"AllowRepeatingReinforcements", toText(settings.allowRepeatingReinforcements)},
        {"AllTurretsDownOnLowPower", toText(settings.turretsDownOnLowPower)},
        {"RocketTurretsDownOnLowPower", toText(settings.rocketTurretsDownOnLowPower)},
        {"ShowLowPowerIcon", toText(settings.showLowPowerIcon)},
        {"GameRules", settings.gameFilename},
        {"NoAI", toText(settings.disableAI)},
        {"Debug", toText(settings.debugMode)},
        {"playMusic", toText(settings.playMusic)},
        {"customMusic", toText(settings.customMusic)},
        {"playSound", toText(settings.playSound)},
        {"playCreditsSound", toText(settings.playCreditsSound)},
        {"drawUnitDebug", toText(settings.drawUnitDebug)},
        {"oneAi", toText(settings.oneAi)},
        {"disableWormAi", toText(settings.disableWormAi)},
        {"disableReinforcements", toText(settings.disableReinforcements)},
        {"noAiRest", toText(settings.noAiRest)},
        {"drawUsages", toText(settings.drawUsages)},
        {"pauseWhenLosingFocus", toText(settings.pauseWhenLosingFocus)},
        {"fogOfWarEnabled", toText(settings.fogOfWarEnabled)},
    };
}

bool saveInSection(const std::filesystem::path &file, const char *section, const KeyValues &values, std::string &error)
{
    cIniFile loaded;
    std::string loadError;
    cIniFile fresh;
    cIniFile &ini = loadAnyIni(file, loaded, loadError) ? loaded : fresh;
    for (const auto &[key, value] : values) {
        ini.setValue(section, key, value);
    }
    return writeIni(ini, file, error);
}
```

  В `settingsValues` ровно 28 пар: те же ключи и значения, в том же порядке, что пишет нынешний `save`.
- тело функции `save` становится:

```cpp
    cIniFile ini;
    for (const auto &[key, value] : settingsValues(settings)) {
        set(ini, key.c_str(), value);
    }

    return writeIni(ini, file, error);
```

- в `saveScales` и `saveLanguage` вызов `loadIni(file, loaded, loadError)` заменяется вызовом `loadAnyIni(file, loaded, loadError)`;
- в конец файла, перед строкой `}` пространства имён, добавляются определения:

```cpp
bool loadChosenOptions(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error)
{
    cIniFile ini;
    if (!loadIni(file, ini, error)) {
        return false;
    }

    InitialGameSettings loaded = settings;
    readSettings(ini.getSection(SECTION), loaded);
    settings.screenW = loaded.screenW;
    settings.screenH = loaded.screenH;
    settings.windowed = loaded.windowed;
    settings.cameraDragMoveSpeed = loaded.cameraDragMoveSpeed;
    settings.cameraBorderOrKeyMoveSpeed = loaded.cameraBorderOrKeyMoveSpeed;
    settings.cameraEdgeMove = loaded.cameraEdgeMove;
    settings.renderScalePercent = loaded.renderScalePercent;
    settings.worldScalePercent = loaded.worldScalePercent;
    settings.language = loaded.language;
    settings.allowRepeatingReinforcements = loaded.allowRepeatingReinforcements;
    settings.turretsDownOnLowPower = loaded.turretsDownOnLowPower;
    settings.rocketTurretsDownOnLowPower = loaded.rocketTurretsDownOnLowPower;
    settings.disableAI = loaded.disableAI;
    settings.debugMode = loaded.debugMode;
    settings.drawUnitDebug = loaded.drawUnitDebug;
    settings.oneAi = loaded.oneAi;
    settings.disableWormAi = loaded.disableWormAi;
    settings.disableReinforcements = loaded.disableReinforcements;
    settings.noAiRest = loaded.noAiRest;
    settings.drawUsages = loaded.drawUsages;
    settings.pauseWhenLosingFocus = loaded.pauseWhenLosingFocus;
    return true;
}

KeyValues valuesOf(const InitialGameSettings &settings, std::span<const std::string_view> keys)
{
    const KeyValues all = settingsValues(settings);
    KeyValues result;
    for (const std::string_view key : keys) {
        const auto found = std::find_if(all.begin(), all.end(), [key](const auto &entry) { return entry.first == key; });
        if (found != all.end()) {
            result.push_back(*found);
        }
    }
    return result;
}

bool saveValues(const std::filesystem::path &file, const KeyValues &values, std::string &error)
{
    return saveInSection(file, SECTION, values, error);
}

bool saveOnExit(const std::filesystem::path &file, const InitialGameSettings &settings, std::string &error)
{
    // The chosen keys are written only by the options menu: values changed by command-line options must not
    // become the player's choice, and a key the player never chose must not shadow settings.ini.
    KeyValues unchosen;
    for (const auto &entry : settingsValues(settings)) {
        if (std::find(CHOSEN_KEYS.begin(), CHOSEN_KEYS.end(), entry.first) == CHOSEN_KEYS.end()) {
            unchosen.push_back(entry);
        }
    }
    return saveInSection(file, SECTION, unchosen, error);
}

bool loadKeyBindings(const std::filesystem::path &file, cSection &section, std::string &error)
{
    cIniFile ini;
    if (!loadAnyIni(file, ini, error)) {
        return false;
    }
    if (!ini.hasSection(KEYS_SECTION)) {
        error = "No key bindings in " + utf8FileName(file);
        return false;
    }
    section = ini.getSection(KEYS_SECTION);
    return true;
}

bool saveKeyBindings(const std::filesystem::path &file, const KeyValues &values, std::string &error)
{
    return saveInSection(file, KEYS_SECTION, values, error);
}
```

- в блоке подключений после строки `#include "utils/InitialGameSettings.hpp"` — пустая строка не добавляется, добавляется строка `#include <algorithm>`.

`readSettings`, `load`, `loadScales`, `loadLanguage` не меняются.

### 3. `cGameSettings`, `cGame_logic.cpp`, `main.cpp`

`src/game/cGameSettings.h`:

- в разделе `public:` после метода `bool isWindowed() const { ... }` добавляются методы:

```cpp
    int getRequestedScreenW() const {
        return m_requestedScreenW;
    }
    int getRequestedScreenH() const {
        return m_requestedScreenH;
    }
    bool isCameraEdgeMove() const {
        return m_cameraEdgeMove;
    }
    float getCameraDragMoveSpeed() const {
        return m_cameraDragMoveSpeed;
    }
    float getCameraBorderOrKeyMoveSpeed() const {
        return m_cameraBorderOrKeyMoveSpeed;
    }
    bool isPauseWhenLosingFocus() const {
        return m_pauseWhenLosingFocus;
    }
    void setAllowRepeatingReinforcements(bool value) {
        m_allowRepeatingReinforcements = value;
    }
    void setDebugMode(bool value) {
        m_debugMode = value;
    }
    void setDisableAI(bool value) {
        m_disableAI = value;
    }
    void setOneAi(bool value) {
        m_oneAi = value;
    }
    void setDisableWormAi(bool value) {
        m_disableWormAi = value;
    }
    void setDisableReinforcements(bool value) {
        m_disableReinforcements = value;
    }
    void setNoAiRest(bool value) {
        m_noAiRest = value;
    }
    void setDrawUnitDebug(bool value) {
        m_drawUnitDebug = value;
    }
    void setDrawUsages(bool value) {
        m_drawUsages = value;
    }
```

- в разделе `private:` после строки `    int m_screenH;` добавляются строки:

```cpp
    // the window size and the camera and focus values the game was started with; they apply only after a restart
    int m_requestedScreenW = 0;
    int m_requestedScreenH = 0;
    bool m_cameraEdgeMove = true;
    float m_cameraDragMoveSpeed = 0.5f;
    float m_cameraBorderOrKeyMoveSpeed = 0.5f;
    bool m_pauseWhenLosingFocus = false;
```

- строка `    bool m_windowed;` (в блоке между строками `//-----------------------`) становится `    bool m_windowed = false;`.

`src/game/cGame_logic.cpp`:

- в `cGame::applySettings` после строки `    m_windowed = gs->windowed;` добавляются строки:

```cpp
    m_gameSettings->m_windowed = gs->windowed;
    m_gameSettings->m_requestedScreenW = gs->screenW;
    m_gameSettings->m_requestedScreenH = gs->screenH;
    m_gameSettings->m_cameraEdgeMove = gs->cameraEdgeMove;
    m_gameSettings->m_cameraDragMoveSpeed = gs->cameraDragMoveSpeed;
    m_gameSettings->m_cameraBorderOrKeyMoveSpeed = gs->cameraBorderOrKeyMoveSpeed;
    m_gameSettings->m_pauseWhenLosingFocus = gs->pauseWhenLosingFocus;
```

- в `cGame::setupGame` сразу после строки `    Logger::info(COMP_INIT, "Initializing Key Bindings", "Loaded from [KEYS] section");` добавляются строки:

```cpp
    if (const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME)) {
        cSection chosenKeys;
        std::string keysError;
        if (Preferences::loadKeyBindings(*prefsFile, chosenKeys, keysError)) {
            m_keyboard->getKeyBindings()->loadFromSection(chosenKeys);
        }
    }
```

  К этому месту `m_keyboard` создан и `loadKeyBindings()` вызван (`m_services->keyboard` присваивается следующей строкой). Подключение `game/Preferences.hpp` — по пункту 13, если его в файле нет (`PreferencesPath` в файле уже используется).
- в `cGame::onKeyPressedGame` в блоке `if (event.isAction(eKeyAction::TOGGLE_FULLSCREEN)) {` после закрывающей скобки вложенного `if (m_windowed) { ... } else { ... }` добавляется строка `        m_gameSettings->m_windowed = m_windowed;`.
- `cGame::currentSettings` не меняется.

`src/main.cpp`:

- блок

```cpp
    // the scales and the language chosen in the options menu apply on every start, the other preferences only with -prefs
    if (const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME)) {
        std::string scalesError;
        Preferences::loadScales(*prefsFile, *settings, scalesError);
        std::string languageError;
        Preferences::loadLanguage(*prefsFile, *settings, languageError);
    }
```

  заменяется блоком

```cpp
    // the values chosen in the options menu apply on every start, the other preferences only with -prefs
    if (const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME)) {
        std::string chosenError;
        Preferences::loadChosenOptions(*prefsFile, *settings, chosenError);
    }
```

- вызов `Preferences::save(*prefsFile, game.currentSettings(), prefsError)` в конце `main` заменяется вызовом `Preferences::saveOnExit(*prefsFile, game.currentSettings(), prefsError)`.

Порядок источников значений при запуске: `settings.ini` → выбор из меню (21 ключ `preferences.ini`) → весь `preferences.ini` при `-prefs` → аргументы командной строки. Следствие для игрока: `Alt+Enter` и аргументы командной строки больше не попадают в `preferences.ini` через ключи `FullScreen`, `ScreenWidth`, `ScreenHeight` и другие из `CHOSEN_KEYS`; эти ключи пишет только окно настроек.

### 4. Новые заголовки страниц настроек

`src/gamestates/AdvancedOptionsHeaderLayout.hpp` — копия файла форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/AdvancedOptionsHeaderLayout.hpp > src/gamestates/AdvancedOptionsHeaderLayout.hpp`. Не правится.

`src/gamestates/OptionsPageData.hpp` — новый файл:

```cpp
#pragma once

#include <algorithm>
#include <array>
#include <cstddef>
#include <iterator>
#include <string_view>
#include <vector>

struct ResolutionOption {
    int width = 0;
    int height = 0;

    bool operator==(const ResolutionOption &) const = default;
};

[[nodiscard]] inline std::vector<ResolutionOption> resolutionChoices(
    int desktopWidth, int desktopHeight, ResolutionOption saved)
{
    static constexpr std::array<ResolutionOption, 35> standard{{
        {800, 600}, {1024, 600}, {1024, 768}, {1152, 864}, {1280, 720}, {1280, 768}, {1280, 800}, {1280, 960},
        {1280, 1024}, {1360, 768}, {1366, 768}, {1440, 900}, {1600, 900}, {1600, 1024}, {1600, 1200},
        {1680, 1050}, {1920, 1080}, {1920, 1200}, {2048, 1080}, {2048, 1152}, {2048, 1536}, {2560, 1080},
        {2560, 1440}, {2560, 1600}, {2880, 1620}, {2880, 1800}, {3200, 1800}, {3440, 1440}, {3840, 1600},
        {3840, 2160}, {4096, 2160}, {5120, 1440}, {5120, 2160}, {5120, 2880}, {7680, 4320},
    }};
    std::vector<ResolutionOption> result;
    const auto add = [&result](ResolutionOption option) {
        if (std::find(result.begin(), result.end(), option) == result.end()) {
            result.push_back(option);
        }
    };
    for (const ResolutionOption &option : standard) {
        if (option.width <= desktopWidth && option.height <= desktopHeight) {
            add(option);
        }
    }
    add(saved);
    add({desktopWidth, desktopHeight});
    std::ranges::sort(result, [](const ResolutionOption &left, const ResolutionOption &right) {
        const long long leftPixels = static_cast<long long>(left.width) * static_cast<long long>(left.height);
        const long long rightPixels = static_cast<long long>(right.width) * static_cast<long long>(right.height);
        if (leftPixels != rightPixels) {
            return leftPixels < rightPixels;
        }
        if (left.width != right.width) {
            return left.width < right.width;
        }
        return left.height < right.height;
    });
    return result;
}

[[nodiscard]] inline std::size_t resolutionChoiceIndex(const std::vector<ResolutionOption> &choices, ResolutionOption selected)
{
    const auto found = std::find(choices.begin(), choices.end(), selected);
    return found == choices.end() ? 0 : static_cast<std::size_t>(std::distance(choices.begin(), found));
}

[[nodiscard]] constexpr int optionsVisibleRows(int listTop, int listBottom, int rowStride)
{
    return rowStride > 0 && listBottom > listTop ? std::max(1, (listBottom - listTop) / rowStride) : 1;
}

[[nodiscard]] constexpr int optionsMaxScrollRow(int totalRows, int visibleRows)
{
    return std::max(0, totalRows - visibleRows);
}

[[nodiscard]] constexpr int optionsClampScrollRow(int scrollRow, int totalRows, int visibleRows)
{
    return std::clamp(scrollRow, 0, optionsMaxScrollRow(totalRows, visibleRows));
}

inline constexpr std::array<std::string_view, 6> MAIN_PAGE_KEYS = {
    "RenderScale", "WorldScale", "Language", "ScreenWidth", "ScreenHeight", "FullScreen",
};

inline constexpr std::array<std::string_view, 7> GAMEPLAY_PAGE_KEYS = {
    "CameraEdgeMove", "CameraBorderOrKeyMoveSpeed", "CameraDragMoveSpeed", "pauseWhenLosingFocus",
    "AllowRepeatingReinforcements", "AllTurretsDownOnLowPower", "RocketTurretsDownOnLowPower",
};

inline constexpr std::array<std::string_view, 8> DIAGNOSTICS_PAGE_KEYS = {
    "Debug", "NoAI", "oneAi", "disableWormAi", "disableReinforcements", "noAiRest", "drawUnitDebug", "drawUsages",
};
```

`src/gamestates/OptionsKeyLabels.hpp` — новый файл: `#pragma once`, подключения `controls/eKeyAction.h`, `utils/Localization.hpp`, `<array>`, `<string>`, структура `struct KeyActionLabel { eKeyAction action; const char *english; const char *russian; };`, массив `inline constexpr std::array<KeyActionLabel, 86> KEY_ACTION_LABELS{{ ... }};` из строк ниже (порядок — порядок `getActionTable()`; пункт 9 даёт ту же таблицу для чтения) и функции:

```cpp
[[nodiscard]] inline const KeyActionLabel *findKeyActionLabel(eKeyAction action)
{
    for (const KeyActionLabel &label : KEY_ACTION_LABELS) {
        if (label.action == action) {
            return &label;
        }
    }
    return nullptr;
}

[[nodiscard]] inline std::string keyActionLabelText(eKeyAction action)
{
    const KeyActionLabel *label = findKeyActionLabel(action);
    return label == nullptr ? std::string() : std::string(localization::text(label->english, label->russian));
}
```

Строки массива:

```cpp
    {eKeyAction::SCREENSHOT, "Take screenshot", "Снимок экрана"},
    {eKeyAction::TOGGLE_MUSIC, "Toggle music", "Включить или выключить музыку"},
    {eKeyAction::MUSIC_VOLUME_DOWN, "Music volume down", "Музыка тише"},
    {eKeyAction::MUSIC_VOLUME_UP, "Music volume up", "Музыка громче"},
    {eKeyAction::MUSIC_PREVIOUS_TRACK, "Previous music track", "Предыдущий трек"},
    {eKeyAction::MUSIC_NEXT_TRACK, "Next music track", "Следующий трек"},
    {eKeyAction::GAME_SPEED_UP, "Game speed up", "Игра быстрее"},
    {eKeyAction::GAME_SPEED_DOWN, "Game speed down", "Игра медленнее"},
    {eKeyAction::TOGGLE_FULLSCREEN, "Toggle fullscreen", "Переключить полноэкранный режим"},
    {eKeyAction::TOGGLE_CHEAT, "Toggle cheat mode", "Переключить режим читов"},
    {eKeyAction::SCROLL_LEFT, "Scroll map left", "Прокрутка карты влево"},
    {eKeyAction::SCROLL_RIGHT, "Scroll map right", "Прокрутка карты вправо"},
    {eKeyAction::SCROLL_UP, "Scroll map up", "Прокрутка карты вверх"},
    {eKeyAction::SCROLL_DOWN, "Scroll map down", "Прокрутка карты вниз"},
    {eKeyAction::CENTER_ON_HOME, "Center on home", "К стартовой точке"},
    {eKeyAction::CENTER_ON_STRUCTURE, "Center on structure", "К выбранному зданию"},
    {eKeyAction::ZOOM_RESET, "Reset zoom", "Сбросить масштаб карты"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_1, "Save view bookmark 1", "Запомнить вид 1"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_2, "Save view bookmark 2", "Запомнить вид 2"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_3, "Save view bookmark 3", "Запомнить вид 3"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_4, "Save view bookmark 4", "Запомнить вид 4"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_5, "Save view bookmark 5", "Запомнить вид 5"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_1, "Go to view bookmark 1", "Перейти к виду 1"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_2, "Go to view bookmark 2", "Перейти к виду 2"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_3, "Go to view bookmark 3", "Перейти к виду 3"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_4, "Go to view bookmark 4", "Перейти к виду 4"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5, "Go to view bookmark 5", "Перейти к виду 5"},
    {eKeyAction::QUICK_SAVE, "Quick save", "Быстрое сохранение"},
    {eKeyAction::QUICK_LOAD, "Quick load", "Быстрая загрузка"},
    {eKeyAction::TOGGLE_FPS, "Show FPS", "Показать или скрыть FPS"},
    {eKeyAction::TOGGLE_TIME_DISPLAY, "Show game time", "Показать или скрыть время игры"},
    {eKeyAction::OPEN_MENU, "Open menu", "Открыть меню"},
    {eKeyAction::DEPLOY_UNIT, "Deploy / Release", "Развернуть / Выпустить"},
    {eKeyAction::SET_PRIMARY, "Set primary structure", "Сделать основным зданием"},
    {eKeyAction::ATTACK_MODE, "Attack / Rally", "Атаковать / Точка сбора"},
    {eKeyAction::ADD_TO_SELECTION, "Add to selection", "Добавить к выбору"},
    {eKeyAction::REPAIR_UNIT, "Repair", "Ремонт"},
    {eKeyAction::RETURN_TO_BASE, "Return to base", "Вернуться на базу"},
    {eKeyAction::SEND_TO_REFINERY, "Unload", "Разгрузить"},
    {eKeyAction::SELECT_SAME_TYPE_ON_MAP, "Select units of the same type on map", "Выбрать такие же юниты на карте"},
    {eKeyAction::SELECT_SAME_TYPE_ON_SCREEN, "Select units of the same type on screen", "Выбрать такие же юниты на экране"},
    {eKeyAction::SELECT_INFANTRY_ON_MAP, "Select infantry on map", "Выбрать пехоту на карте"},
    {eKeyAction::SELECT_INFANTRY_ON_SCREEN, "Select infantry on screen", "Выбрать пехоту на экране"},
    {eKeyAction::SELECT_WHEELS_ON_MAP, "Select wheeled units on map", "Выбрать колёсную технику на карте"},
    {eKeyAction::SELECT_WHEELS_ON_SCREEN, "Select wheeled units on screen", "Выбрать колёсную технику на экране"},
    {eKeyAction::SELECT_TANKS_ON_MAP, "Select tanks on map", "Выбрать танки на карте"},
    {eKeyAction::SELECT_TANKS_ON_SCREEN, "Select tanks on screen", "Выбрать танки на экране"},
    {eKeyAction::TRACK_UNIT, "Track selected units", "Следить за выбранными"},
    {eKeyAction::SELECT_LAUNCHERS_ON_MAP, "Select launchers on map", "Выбрать ракетные установки на карте"},
    {eKeyAction::SELECT_LAUNCHERS_ON_SCREEN, "Select launchers on screen", "Выбрать ракетные установки на экране"},
    {eKeyAction::SELECT_HARVESTERS_ON_MAP, "Select harvesters on map", "Выбрать харвестеры на карте"},
    {eKeyAction::SELECT_HARVESTERS_ON_SCREEN, "Select harvesters on screen", "Выбрать харвестеры на экране"},
    {eKeyAction::SELECT_ATTACKING_ON_MAP, "Select attacking units on map", "Выбрать атакующих на карте"},
    {eKeyAction::GROUP_1, "Select group 1", "Выбрать группу 1"},
    {eKeyAction::GROUP_2, "Select group 2", "Выбрать группу 2"},
    {eKeyAction::GROUP_3, "Select group 3", "Выбрать группу 3"},
    {eKeyAction::GROUP_4, "Select group 4", "Выбрать группу 4"},
    {eKeyAction::GROUP_5, "Select group 5", "Выбрать группу 5"},
    {eKeyAction::GROUP_6, "Select group 6", "Выбрать группу 6"},
    {eKeyAction::EDITOR_SAVE, "Editor: save map", "Редактор: сохранить карту"},
    {eKeyAction::EDITOR_ZOOM_IN, "Editor: zoom in", "Редактор: приблизить"},
    {eKeyAction::EDITOR_ZOOM_OUT, "Editor: zoom out", "Редактор: отдалить"},
    {eKeyAction::EDITOR_DISPLAY_GRID, "Editor: show grid", "Редактор: сетка"},
    {eKeyAction::EDITOR_DISPLAY_AXES, "Editor: show axes", "Редактор: оси"},
    {eKeyAction::EDITOR_UNDO, "Editor: undo", "Редактор: отменить"},
    {eKeyAction::EDITOR_REDO, "Editor: redo", "Редактор: повторить"},
    {eKeyAction::EDITOR_COPY, "Editor: copy", "Редактор: копировать"},
    {eKeyAction::EDITOR_PASTE, "Editor: paste", "Редактор: вставить"},
    {eKeyAction::EDITOR_CUT, "Editor: cut", "Редактор: вырезать"},
    {eKeyAction::MENU_BACK, "Menu: back", "Меню: назад"},
    {eKeyAction::MENU_CONFIRM, "Menu: confirm", "Меню: подтвердить"},
    {eKeyAction::MENU_CANCEL, "Menu: cancel", "Меню: отмена"},
    {eKeyAction::DEBUG_WIN, "Debug: win mission", "Отладка: победа в миссии"},
    {eKeyAction::DEBUG_LOSE, "Debug: lose mission", "Отладка: поражение в миссии"},
    {eKeyAction::DEBUG_GIVE_CREDITS, "Debug: give credits", "Отладка: выдать кредиты"},
    {eKeyAction::DEBUG_DESTROY_AT_CURSOR, "Debug: destroy at cursor", "Отладка: уничтожить под курсором"},
    {eKeyAction::DEBUG_REVEAL_MAP, "Debug: reveal map", "Отладка: открыть карту"},
    {eKeyAction::DEBUG_DAMAGE_AT_CURSOR, "Debug: damage at cursor", "Отладка: повредить под курсором"},
    {eKeyAction::DEBUG_KILL_CARRYALLS, "Debug: kill carryalls", "Отладка: уничтожить транспортники"},
    {eKeyAction::DEBUG_SPAWN_ORNITHOPTER, "Debug: spawn ornithopter", "Отладка: создать орнитоптер"},
    {eKeyAction::DEBUG_SPAWN_WORM, "Debug: spawn worm", "Отладка: создать червя"},
    {eKeyAction::DEBUG_CLEAR_SHROUD_AT_CURSOR, "Debug: clear shroud at cursor", "Отладка: снять туман под курсором"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_0, "Debug: switch to player 0", "Отладка: переключиться на игрока 0"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_1, "Debug: switch to player 1", "Отладка: переключиться на игрока 1"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_2, "Debug: switch to player 2", "Отладка: переключиться на игрока 2"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_3, "Debug: switch to player 3", "Отладка: переключиться на игрока 3"},
```

`src/gamestates/OptionsMenuLayout.hpp`: в функцию `create` добавляется последний параметр `int extraContentRows = 0` (после `int titleFontHeight = -1`); строка `const int preferredApplyY = (contentGap + buttonHeight) * 10;` становится `const int preferredApplyY = (contentGap + buttonHeight) * (10 + extraContentRows);`; строка `? contentTop + 9 * (buttonHeight + contentGap)` становится `? contentTop + (9 + extraContentRows) * (buttonHeight + contentGap)`. Других правок нет; результат при `extraContentRows = 0` равен прежнему (тест `test_OptionsMenu.cpp` не меняется).

### 5. `cOptionsState`: страницы, состояние, переключение

Где создаётся объект и что к этому моменту готово: `cCreatorState` создаёт `cOptionsState` при первом переходе в окно настроек (`GAME_OPTIONS`), то есть после `cGame::setupGame`: `m_services->keyboard` (с загруженными привязками), `m_services->settings` с заполненными в `applySettings` полями и звуковой контекст уже готовы. Конструктор читает только их.

`src/gamestates/cOptionsState.h`:

- после строки `#include "include/Texture.hpp"` — строки `#include "controls/cKeyBindings.h"`, `#include "gamestates/OptionsPageData.hpp"`, `#include "utils/InitialGameSettings.hpp"`; после строки `#include <memory>` — строка `#include <optional>`;
- после строки `class cGameSettings;` — строка `class cKeyboard;`;
- в раздел `public:` перед строкой `    explicit cOptionsState(sGameServices* services, int prevState);` — строки `    enum class OptionsPage { Main, Gameplay, Controls, Diagnostics };` и пустая строка;
- после строки `    cMouse* m_mouse = nullptr;` — строка `    cKeyboard* m_keyboard = nullptr;`;
- после строки `    GuiButton *m_loadGameButton = nullptr;` — строки:

```cpp
    GuiLabel *m_resolutionValueLabel = nullptr;
    OptionsPage m_optionsPage = OptionsPage::Main;
    std::optional<OptionsPage> m_pendingOptionsPage;
    bool m_refreshRequested = false;
    InitialGameSettings m_selected;
    cKeyBindings m_selectedBindings;
    std::optional<eKeyAction> m_bindingCapture;
    bool m_bindingCaptureFinished = false;
    std::string m_bindingMessage;
    int m_controlsScrollRow = 0;
    std::vector<ResolutionOption> m_resolutionChoices;
    std::size_t m_selectedResolutionIndex = 0;
    ResolutionOption m_savedResolution;
    bool m_selectedFullscreen = false;
    bool m_savedFullscreen = false;
```

- после строки `    void applyScaleSettings();` — строки:

```cpp
    void selectResolution(int step);
    void loadSelectedOptions();
    void switchOptionsPage(OptionsPage page);
    void requestOptionsPage(OptionsPage page);
    void constructAdvancedWindow(int prevState);
    void applyAdvancedPage();
```

`src/gamestates/cOptionsState.cpp`:

- подключения (правило пункта 13): `controls/cKeyboard.h`, `controls/cKeyboardEvent.h`, `controls/sMouseEvent.h`, `gamestates/OptionsKeyLabels.hpp`, `<SDL3/SDL.h>`, `<format>`;
- конструктор: в списке инициализации после строки `m_mouse(services->mouse),` — строка `m_keyboard(services->keyboard),`; после строки `d2tm_assert(m_mouse != nullptr);` — строки `d2tm_assert(m_keyboard != nullptr);` и `d2tm_assert(m_keyboard->getKeyBindings() != nullptr);`; перед строкой `refresh();` (в конструкторе, после создания `m_saveDialog`) — строка `loadSelectedOptions();`;
- `refresh()`: после строки `m_loadGameButton = nullptr;` — строка `m_resolutionValueLabel = nullptr;`;
- `isKeyboardCapturedByUi`: тело — `return m_bindingCapture.has_value() || m_saveDialog->isCapturingText();`;
- `setPrevState`: между строками `m_prevState = prevState;` и `refresh();` добавляются строки `m_optionsPage = OptionsPage::Main;`, `m_pendingOptionsPage.reset();`, `loadSelectedOptions();`;
- новые определения (текст точный):

```cpp
void cOptionsState::loadSelectedOptions()
{
    InitialGameSettings selected;
    selected.screenW = m_settings->getRequestedScreenW();
    selected.screenH = m_settings->getRequestedScreenH();
    selected.windowed = m_settings->isWindowed();
    selected.renderScalePercent = m_settings->getSavedRenderScalePercent();
    selected.worldScalePercent = m_settings->getSavedWorldScalePercent();
    selected.language = normalizeLanguage(m_settings->getSavedLanguage());
    selected.cameraEdgeMove = m_settings->isCameraEdgeMove();
    selected.cameraDragMoveSpeed = m_settings->getCameraDragMoveSpeed();
    selected.cameraBorderOrKeyMoveSpeed = m_settings->getCameraBorderOrKeyMoveSpeed();
    selected.pauseWhenLosingFocus = m_settings->isPauseWhenLosingFocus();
    selected.allowRepeatingReinforcements = m_settings->isAllowRepeatingReinforcements();
    selected.turretsDownOnLowPower = m_settings->isTurretsDownOnLowPower();
    selected.rocketTurretsDownOnLowPower = m_settings->isRocketTurretsDownOnLowPower();
    selected.debugMode = m_settings->isDebugMode();
    selected.disableAI = m_settings->isDisableAI();
    selected.oneAi = m_settings->isOneAi();
    selected.disableWormAi = m_settings->isDisableWormAi();
    selected.disableReinforcements = m_settings->isDisableReinforcements();
    selected.noAiRest = m_settings->isNoAiRest();
    selected.drawUnitDebug = m_settings->isDrawUnitDebug();
    selected.drawUsages = m_settings->isDrawUsages();
    if (const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME)) {
        std::string error;
        Preferences::loadChosenOptions(*prefsFile, selected, error);
    }
    m_selected = selected;
    m_selectedBindings = *m_keyboard->getKeyBindings();
    m_bindingCapture.reset();
    m_bindingCaptureFinished = false;
    m_bindingMessage.clear();
    m_controlsScrollRow = 0;

    int desktopWidth = m_settings->getScreenW();
    int desktopHeight = m_settings->getScreenH();
    SDL_Rect bounds{};
    if (SDL_GetDisplayBounds(SDL_GetPrimaryDisplay(), &bounds)) {
        desktopWidth = bounds.w;
        desktopHeight = bounds.h;
    }
    m_savedResolution = {selected.screenW, selected.screenH};
    m_resolutionChoices = resolutionChoices(desktopWidth, desktopHeight, m_savedResolution);
    m_selectedResolutionIndex = resolutionChoiceIndex(m_resolutionChoices, m_savedResolution);
    m_savedFullscreen = !selected.windowed;
    m_selectedFullscreen = m_savedFullscreen;
}

void cOptionsState::switchOptionsPage(OptionsPage page)
{
    m_bindingCapture.reset();
    m_bindingCaptureFinished = false;
    m_bindingMessage.clear();
    m_controlsScrollRow = 0;
    m_optionsPage = page;
    refresh();
}

void cOptionsState::requestOptionsPage(OptionsPage page)
{
    m_pendingOptionsPage = page;
}

void cOptionsState::thinkFast()
{
    if (m_pendingOptionsPage) {
        const OptionsPage page = *m_pendingOptionsPage;
        m_pendingOptionsPage.reset();
        switchOptionsPage(page);
        return;
    }
    if (m_bindingCaptureFinished) {
        m_bindingCaptureFinished = false;
        m_bindingCapture.reset();
        m_refreshRequested = false;
        refresh();
        return;
    }
    if (m_refreshRequested) {
        m_refreshRequested = false;
        refresh();
    }
}

void cOptionsState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (m_saveDialog->isOpen()) {
        m_saveDialog->onMouseEvent(event);
        return;
    }
    const bool isWheelEvent = event.eventType == eMouseEventType::MOUSE_SCROLLED_UP ||
                              event.eventType == eMouseEventType::MOUSE_SCROLLED_DOWN;
    if (isWheelEvent && m_optionsPage == OptionsPage::Controls && !m_bindingCapture) {
        m_controlsScrollRow += event.eventType == eMouseEventType::MOUSE_SCROLLED_UP ? -3 : 3;
        refresh();
        return;
    }
    m_guiWindow->onNotifyMouseEvent(event);
}

void cOptionsState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (m_saveDialog->isOpen()) {
        m_saveDialog->onKeyboardEvent(event);
        return;
    }
    if (m_optionsPage != OptionsPage::Controls || !m_bindingCapture || m_bindingCaptureFinished ||
        !event.isType(eKeyEventType::PRESSED) || event.hasTextInput()) {
        return;
    }
    const SDL_Scancode key = event.getFirstKey();
    if (key == SDL_SCANCODE_UNKNOWN) {
        return;
    }
    // The capture ends in thinkFast, so that the game's global key actions do not receive the key just chosen.
    m_bindingCaptureFinished = true;
    m_bindingMessage.clear();
    if (key == SDL_SCANCODE_ESCAPE) {
        return;
    }
    if (!cKeyBindings::canStoreKey(key)) {
        m_bindingMessage = localization::text("This key cannot be assigned.", "Эту клавишу нельзя назначить.");
        return;
    }
    const s_KeyBinding binding = cKeyBindings::makeCapturedBinding(key, event.getCombo());
    const std::optional<eKeyAction> conflict = m_selectedBindings.trySetBinding(*m_bindingCapture, binding);
    if (conflict) {
        m_bindingMessage = localization::format(
            "Key {} is already assigned to {}.",
            "Клавиша {} уже назначена команде «{}».",
            cKeyBindings::describeBinding(binding),
            keyActionLabelText(*conflict));
    }
}
```

  Прежние определения `thinkFast`, `onNotifyMouseEvent` и `onNotifyKeyboardEvent` заменяются этими; прежнее тело `onNotifyKeyboardEvent` (передача события диалогу сохранений) входит в новое.
- `constructWindow`: первой строкой тела (перед строкой `const int margin = 8;`) добавляются строки:

```cpp
    if (m_optionsPage != OptionsPage::Main) {
        constructAdvancedWindow(prevState);
        return;
    }
```

### 6. Страница «Основные»: «Разрешение», «Полный экран», «More settings», «Apply»

Правки `constructWindow` (страница «Основные»), `updateScaleControls`, `applyScaleSettings` в `src/gamestates/cOptionsState.cpp`:

1. Вызов `OptionsMenuLayout::create(` получает последним аргументом `2`: после аргумента `m_textDrawer->getFontHeight()` — `, 2` (на новой строке тем же отступом, что у соседних аргументов, с запятой после предыдущего аргумента).
2. Надпись режима читов: `contentRowY(9)` становится `contentRowY(11)`.
3. Сразу после строки `    m_guiWindow->addGuiObject(std::move(languageButton));` добавляются строки «Разрешение» (строка 9) и «Полный экран» (строка 10):

```cpp
    const cRectangle &resolutionRect = rect(contentX, contentRowY(9), displayLabelWidth, buttonHeight);
    auto resolutionLabel = GuiLabelBuilder()
            .withRect(resolutionRect)
            .withLabel(localization::text("Resolution", "Разрешение"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(std::move(resolutionLabel));

    const cRectangle &previousResolutionRect = rect(selectorX, contentRowY(9), arrowWidth, buttonHeight);
    auto previousResolutionButton = GuiButtonBuilder()
            .withRect(previousResolutionRect)
            .withLabel("◄")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectResolution(-1); })
            .build();
    m_guiWindow->addGuiObject(std::move(previousResolutionButton));

    const cRectangle &resolutionValueRect = rect(selectorX + arrowWidth + margin, contentRowY(9), scaleValueWidth, buttonHeight);
    auto resolutionValueLabel = GuiLabelBuilder()
            .withRect(resolutionValueRect)
            .withLabel("")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .build();
    m_resolutionValueLabel = resolutionValueLabel.get();
    m_guiWindow->addGuiObject(std::move(resolutionValueLabel));

    const cRectangle &nextResolutionRect = rect(selectorX + arrowWidth + margin + scaleValueWidth + margin, contentRowY(9), arrowWidth, buttonHeight);
    auto nextResolutionButton = GuiButtonBuilder()
            .withRect(nextResolutionRect)
            .withLabel("►")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectResolution(1); })
            .build();
    m_guiWindow->addGuiObject(std::move(nextResolutionButton));

    const cRectangle &fullscreenRect = rect(contentX, contentRowY(10), checkLabelWidth, buttonHeight);
    auto fullscreenLabel = GuiLabelBuilder()
            .withRect(fullscreenRect)
            .withLabel(localization::text("Fullscreen", "Полноэкранный режим"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .withTheme(controlTheme)
            .build();
    m_guiWindow->addGuiObject(std::move(fullscreenLabel));

    const cRectangle &fullscreenCheckRect = rect(checkX, contentRowY(10), buttonHeight, buttonHeight);
    auto fullscreenCheck = GuiCheckBoxBuilder()
            .withRect(fullscreenCheckRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .onCheck([this]() {
                m_selectedFullscreen = true;
                m_statusLabel->setText("");
                updateScaleControls();
            })
            .onUnCheck([this]() {
                m_selectedFullscreen = false;
                m_statusLabel->setText("");
                updateScaleControls();
            })
            .build();
    fullscreenCheck->setChecked(m_selectedFullscreen);
    m_guiWindow->addGuiObject(std::move(fullscreenCheck));
```

4. Кнопка «More settings»: строки `.withTheme(GuiTheme::RemasterInactive())`, `.withKind(buttonKind)`, `.withEnabled(false)` (перед `.build();` этой кнопки) заменяются строками `.withTheme(controlTheme)`, `.withKind(buttonKind)`, `.onClick([this]() { requestOptionsPage(OptionsPage::Gameplay); })`. Надпись кнопки остаётся `localization::text("More settings", "Ещё настройки")`.
5. Новое определение:

```cpp
void cOptionsState::selectResolution(int step)
{
    const int count = static_cast<int>(m_resolutionChoices.size());
    m_selectedResolutionIndex = static_cast<std::size_t>((static_cast<int>(m_selectedResolutionIndex) + step + count) % count);
    m_statusLabel->setText("");
    updateScaleControls();
}
```

6. В `updateScaleControls`: перед строкой `m_languageButton->setText(...)` добавляются строки:

```cpp
    const ResolutionOption &resolution = m_resolutionChoices[m_selectedResolutionIndex];
    m_resolutionValueLabel->setText(std::format("{}×{}", resolution.width, resolution.height));
```

   в условии `m_applyButton->setEnabled(...)` строка `m_selectedLanguage != savedLanguage` становится `m_selectedLanguage != savedLanguage ||`, и после неё добавляется строка `resolution != m_savedResolution || m_selectedFullscreen != m_savedFullscreen`.
7. Тело `applyScaleSettings` заменяется:

```cpp
    const int renderScale = m_renderScaleChoices[m_selectedRenderScaleIndex];
    const int worldScale = m_worldScaleChoices[m_selectedWorldScaleIndex];
    const ResolutionOption resolution = m_resolutionChoices[m_selectedResolutionIndex];
    m_selected.renderScalePercent = renderScale;
    m_selected.worldScalePercent = worldScale;
    m_selected.language = m_selectedLanguage;
    m_selected.screenW = resolution.width;
    m_selected.screenH = resolution.height;
    m_selected.windowed = !m_selectedFullscreen;
    std::string error = "Could not get the user data directory";
    const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME);
    const bool saved = prefsFile && Preferences::saveValues(*prefsFile, Preferences::valuesOf(m_selected, MAIN_PAGE_KEYS), error);
    if (saved) {
        m_settings->setSavedScalePercents(renderScale, worldScale);
        m_settings->setSavedLanguage(m_selectedLanguage);
        m_savedResolution = resolution;
        m_savedFullscreen = m_selectedFullscreen;
        m_statusLabel->setText(localization::text("Saved. Restart the game.", "Сохранено. Перезапустите игру."));
    } else {
        Logger::warn(COMP_GAMERULES, "Preferences", "Could not save preferences: {}", error);
        m_statusLabel->setText(localization::text("Could not save preferences.ini", "Не удалось сохранить preferences.ini"));
    }
    updateScaleControls();
```

   Функции `Preferences::saveScales` и `Preferences::saveLanguage` остаются в `Preferences`, но `cOptionsState` их больше не вызывает.

Строки 1–8 страницы «Основные», их положение, кнопки «Main menu», «Quit game», «Back», «Save game», «Load game», «Mission select» и диалог сохранений не меняются.

### 7. Страницы «Игра» и «Диагностика»

Новый файл `src/gamestates/cOptionsPages.cpp` содержит определения `cOptionsState::constructAdvancedWindow` и `cOptionsState::applyAdvancedPage` (пункты 7–8) и подключения: `gamestates/cOptionsState.h`, `config.h`, `gui/GuiButton.h`, `gui/GuiWindow.h`, `gui/GuiLabel.hpp`, `gui/GuiCheckBox.hpp`, `gui/GuiSlider.hpp`, `gui/GuiTheme.hpp`, `context/GameContext.hpp`, `context/TextContext.hpp`, `drawers/cTextDrawer.h`, `controls/cKeyboard.h`, `game/cGameSettings.h`, `game/Preferences.hpp`, `game/PreferencesPath.hpp`, `gamestates/AdvancedOptionsHeaderLayout.hpp`, `gamestates/OptionsKeyLabels.hpp`, `gamestates/OptionsPageData.hpp`, `include/cAssert.h`, `utils/Localization.hpp`, `utils/Log.h`, `<algorithm>`, `<cmath>`, `<string_view>`.

`cOptionsState::constructAdvancedWindow(int)` — перенос тела `cOptionsState::constructAdvancedWindow` форка (`FORK1:src/gamestates/cOptionsState.cpp`, строки 278–518) по правилам пункта 13 со следующими отличиями:

- Размеры: `windowWidth = std::min(m_settings->getScreenW() - 32, 760)`, `windowHeight = std::min(m_settings->getScreenH() - 32, 640)`, `margin = 8`, `buttonHeight = std::max(32, m_textDrawer->getFontHeight() + 10)`, `labelWidth = windowWidth - 200`, `checkX = windowWidth - 160`, `rowStride = buttonHeight + 4`, `footerY = windowHeight - buttonHeight - margin`; строка с номером `n` (счёт с 2) стоит на `y = n * rowStride`. Заголовок окна — `localization::text("Dune II - Settings", "Dune II — Настройки")`. Вкладки — по `AdvancedOptionsHeaderLayout::create(windowWidth, margin, buttonHeight, m_textDrawer->getFontHeight())`; подписи вкладок — в пункте 9; щелчок по вкладке — `requestOptionsPage(<страница>)`.
- `addToggle` и `addSpeed` работают с `m_selected` и указателями на члены `InitialGameSettings` (`bool InitialGameSettings::*`, `float InitialGameSettings::*`); ползунок скорости — значения 1–10, начальное значение `std::clamp(static_cast<int>(std::lround(value * 10.0f)), 1, 10)`, результат `static_cast<float>(value) / 10.0f`.
- Страница «Игра» (`m_optionsPage == OptionsPage::Gameplay`): строки по порядку, подписи — пункт 9:

  | № | Тип | Поле `InitialGameSettings` | Ключ |
  |---|---|---|---|
  | 1 | флажок | `cameraEdgeMove` | `CameraEdgeMove` |
  | 2 | ползунок | `cameraBorderOrKeyMoveSpeed` | `CameraBorderOrKeyMoveSpeed` |
  | 3 | ползунок | `cameraDragMoveSpeed` | `CameraDragMoveSpeed` |
  | 4 | флажок | `pauseWhenLosingFocus` | `pauseWhenLosingFocus` |
  | 5 | флажок | `allowRepeatingReinforcements` | `AllowRepeatingReinforcements` |
  | 6 | флажок | `turretsDownOnLowPower` | `AllTurretsDownOnLowPower` |
  | 7 | флажок | `rocketTurretsDownOnLowPower` | `RocketTurretsDownOnLowPower` |

  После них — надпись «Rules file: game.ini (change manually)» (как в форке, строки 405–413).
- Страница «Диагностика» (`m_optionsPage == OptionsPage::Diagnostics`): восемь флажков:

  | № | Поле `InitialGameSettings` | Ключ |
  |---|---|---|
  | 1 | `debugMode` | `Debug` |
  | 2 | `disableAI` | `NoAI` |
  | 3 | `oneAi` | `oneAi` |
  | 4 | `disableWormAi` | `disableWormAi` |
  | 5 | `disableReinforcements` | `disableReinforcements` |
  | 6 | `noAiRest` | `noAiRest` |
  | 7 | `drawUnitDebug` | `drawUnitDebug` |
  | 8 | `drawUsages` | `drawUsages` |

- Низ окна на всех трёх страницах: «Apply» (`16, footerY, 180, buttonHeight`) — `onClick` вызывает `applyAdvancedPage()`; надпись состояния (`16 + 180 + margin, footerY, windowWidth - 2 * (16 + 180 + margin), buttonHeight`, пустая, `TRANSPARENT_WITHOUT_BORDER`, выравнивание по левому краю; указатель на неё сохраняется в `m_statusLabel`); «Back» (`windowWidth - 180 - margin, footerY, 180, buttonHeight`) — `requestOptionsPage(OptionsPage::Main)`.

`cOptionsState::applyAdvancedPage()` — текст точный:

```cpp
void cOptionsState::applyAdvancedPage()
{
    std::string error = "Could not get the user data directory";
    const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME);
    bool saved = false;
    if (prefsFile) {
        switch (m_optionsPage) {
            case OptionsPage::Gameplay:
                saved = Preferences::saveValues(*prefsFile, Preferences::valuesOf(m_selected, GAMEPLAY_PAGE_KEYS), error);
                break;
            case OptionsPage::Diagnostics:
                saved = Preferences::saveValues(*prefsFile, Preferences::valuesOf(m_selected, DIAGNOSTICS_PAGE_KEYS), error);
                break;
            case OptionsPage::Controls: {
                Preferences::KeyValues values;
                for (const auto &[name, action] : cKeyBindings::getActionTable()) {
                    values.emplace_back(name, m_selectedBindings.toIniValue(action));
                }
                saved = Preferences::saveKeyBindings(*prefsFile, values, error);
                break;
            }
            case OptionsPage::Main:
                break;
        }
    }
    if (!saved) {
        Logger::warn(COMP_GAMERULES, "Preferences", "Could not save preferences: {}", error);
        m_statusLabel->setText(localization::text("Could not save preferences.ini", "Не удалось сохранить preferences.ini"));
        return;
    }
    switch (m_optionsPage) {
        case OptionsPage::Gameplay:
            m_settings->setAllowRepeatingReinforcements(m_selected.allowRepeatingReinforcements);
            m_settings->setTurretsDownOnLowPower(m_selected.turretsDownOnLowPower);
            m_settings->setRocketTurretsDownOnLowPower(m_selected.rocketTurretsDownOnLowPower);
            m_statusLabel->setText(localization::text("Saved. Restart the game.", "Сохранено. Перезапустите игру."));
            break;
        case OptionsPage::Diagnostics:
            m_settings->setDebugMode(m_selected.debugMode);
            m_settings->setDisableAI(m_selected.disableAI);
            m_settings->setOneAi(m_selected.oneAi);
            m_settings->setDisableWormAi(m_selected.disableWormAi);
            m_settings->setDisableReinforcements(m_selected.disableReinforcements);
            m_settings->setNoAiRest(m_selected.noAiRest);
            m_settings->setDrawUnitDebug(m_selected.drawUnitDebug);
            m_settings->setDrawUsages(m_selected.drawUsages);
            m_statusLabel->setText(localization::text("Saved.", "Сохранено."));
            break;
        case OptionsPage::Controls:
            *m_keyboard->getKeyBindings() = m_selectedBindings;
            m_statusLabel->setText(localization::text("Saved.", "Сохранено."));
            break;
        case OptionsPage::Main:
            break;
    }
}
```

Живые значения (применяются после «Apply» сразу): повтор подкреплений, башни, флаги «Диагностики», привязки клавиш. Значения камеры и паузы при потере фокуса действуют после перезапуска: страница «Игра» сообщает об этом строкой состояния «Saved. Restart the game.».

### 8. Страница «Управление»

Строки страницы «Управление» (`m_optionsPage == OptionsPage::Controls`) строятся в `constructAdvancedWindow` вместо строк пунктов 7; таблица — `cKeyBindings::getActionTable()` (86 действий, порядок таблицы), подписи действий — `keyActionLabelText(action)`:

```cpp
    const auto &table = cKeyBindings::getActionTable();
    const int totalRows = static_cast<int>(table.size());
    const int listTop = 2 * rowStride;
    const int listBottom = footerY - rowStride;
    const int visibleRows = optionsVisibleRows(listTop, listBottom, rowStride);
    m_controlsScrollRow = optionsClampScrollRow(m_controlsScrollRow, totalRows, visibleRows);
    const int bindingButtonWidth = 220;
    const int bindingButtonX = windowWidth - margin - bindingButtonWidth;
```

- Для каждого `offset` от 0 до `visibleRows - 1`, пока `m_controlsScrollRow + offset < totalRows`: действие `table[m_controlsScrollRow + offset].second`; подпись (`TRANSPARENT_WITHOUT_BORDER`, левый край) в `16, (2 + offset) * rowStride, bindingButtonX - 32, buttonHeight`; кнопка привязки в `bindingButtonX, (2 + offset) * rowStride, bindingButtonWidth, buttonHeight` (тема и вид как у «Apply»); надпись кнопки — `localization::text("Press key...", "Нажмите клавишу…")`, если `m_bindingCapture == action`, иначе `m_selectedBindings.getBindingDisplayName(action)`.
- Щелчок по кнопке: `m_bindingMessage.clear(); m_bindingCapture = action; m_bindingCaptureFinished = false; m_refreshRequested = true;` (окно перестраивает `thinkFast`; пересборка окна из обработчика его собственной кнопки не вызывается).
- Строка под списком: надпись (`TRANSPARENT_WITHOUT_BORDER`, левый край) в `16, (2 + visibleRows) * rowStride, windowWidth - 32, buttonHeight`; текст — `m_bindingMessage`, если он не пуст, иначе `localization::format("Actions {}-{} of {}", "Действия {}-{} из {}", m_controlsScrollRow + 1, m_controlsScrollRow + shownRows, totalRows)`, где `shownRows` — число построенных строк.
- Колесо мыши листает список (пункт 5, `onNotifyMouseEvent`): шаг три строки, границы — `optionsClampScrollRow`.
- Захват (пункт 5, `onNotifyKeyboardEvent`): первая клавиша события `PRESSED` вместе с модификаторами события даёт привязку `cKeyBindings::makeCapturedBinding`; `Escape` отменяет захват; клавиша, которую нельзя записать в `[KEYS]` (`canStoreKey`), даёт сообщение «This key cannot be assigned.»; занятая клавиша (`trySetBinding` вернул действие) даёт сообщение о конфликте, привязка не меняется; свободная клавиша заменяет привязку действия целиком одной клавишей с модификаторами. Захват заканчивается в `thinkFast`, пока он не закончен, `isKeyboardCapturedByUi()` равно `true`.
- Привязки хранит `m_selectedBindings` (копия действующих привязок на момент входа в окно); действующие привязки меняет только «Apply» (`applyAdvancedPage`). Правило конфликта и его исключения — пункт 1 (`findConflict`); в таблицу проверки входят действия таблицы (86), действия `GROUP_ASSIGN_*` и `GROUP_ADDTOSEL_*` не проверяются.
- «Apply» пишет в раздел `[KEYS]` файла `preferences.ini` все 86 действий таблицы (имя таблицы = ключ, значение — `toIniValue`), а не только изменённые.

### 9. Тексты

Все тексты — `localization::text(английский, русский)`; русские тексты форка перенесены как есть. Новые строки (нет в форке или иная форма):

| Место | English | Русский |
|---|---|---|
| вкладка 1 | Main | Основные |
| вкладка 2 | Gameplay | Игра |
| вкладка 3 | Controls | Управление |
| вкладка 4 | Diagnostics | Диагностика |
| заголовок страницы | Dune II - Settings | Dune II — Настройки |
| «Игра» 1 | Edge scrolling — move camera at screen edge | Прокрутка у края экрана |
| «Игра» 2 | Keyboard/edge camera speed | Скорость камеры с клавиатуры и у края |
| «Игра» 3 | Camera drag speed | Скорость перетаскивания камеры |
| «Игра» 4 | Pause when the window loses focus | Пауза при потере фокуса окна |
| «Игра» 5 | Repeat reinforcements | Повторять подкрепления |
| «Игра» 6 | All turrets stop on low power | Отключать все башни при нехватке энергии |
| «Игра» 7 | Rocket turrets stop on low power | Отключать ракетные башни при нехватке энергии |
| «Игра», надпись | Rules file: game.ini (change manually) | Файл правил: game.ini (меняется вручную) |
| «Диагностика» 1 | Debug mode | Режим отладки |
| «Диагностика» 2 | Disable all AI | Отключить ИИ |
| «Диагностика» 3 | Use one AI player | Оставить одного ИИ |
| «Диагностика» 4 | Disable worm AI | Отключить ИИ червя |
| «Диагностика» 5 | Disable reinforcements | Отключить подкрепления |
| «Диагностика» 6 | Disable remaining AI | Отключить остальных ИИ |
| «Диагностика» 7 | Show unit debug data | Показывать отладочные данные юнитов |
| «Диагностика» 8 | Show resource usage | Показывать расход ресурсов |
| «Основные» | Resolution | Разрешение |
| «Основные» | Fullscreen | Полноэкранный режим |
| «Управление», кнопка при захвате | Press key... | Нажмите клавишу… |
| «Управление», конфликт | Key {} is already assigned to {}. | Клавиша {} уже назначена команде «{}». |
| «Управление», нельзя назначить | This key cannot be assigned. | Эту клавишу нельзя назначить. |
| «Управление», диапазон | Actions {}-{} of {} | Действия {}-{} из {} |
| состояние после «Apply» | Saved. | Сохранено. |

Уже существующие в порту тексты, которые страницы используют без изменения: «Apply»/«Применить», «Back»/«Назад», «More settings»/«Ещё настройки», «Saved. Restart the game.»/«Сохранено. Перезапустите игру.», «Could not save preferences.ini»/«Не удалось сохранить preferences.ini».

Подписи действий страницы «Управление» (русские тексты новые; шесть команд форка покрыты четырьмя действиями: `ATTACK_MODE` — «Attack / Rally», `REPAIR_UNIT` — «Repair», `SEND_TO_REFINERY` — «Unload», `DEPLOY_UNIT` — «Deploy / Release»):

| № | Действие (`eKeyAction`) | English | Русский |
|---|---|---|---|
| 1 | `SCREENSHOT` | Take screenshot | Снимок экрана |
| 2 | `TOGGLE_MUSIC` | Toggle music | Включить или выключить музыку |
| 3 | `MUSIC_VOLUME_DOWN` | Music volume down | Музыка тише |
| 4 | `MUSIC_VOLUME_UP` | Music volume up | Музыка громче |
| 5 | `MUSIC_PREVIOUS_TRACK` | Previous music track | Предыдущий трек |
| 6 | `MUSIC_NEXT_TRACK` | Next music track | Следующий трек |
| 7 | `GAME_SPEED_UP` | Game speed up | Игра быстрее |
| 8 | `GAME_SPEED_DOWN` | Game speed down | Игра медленнее |
| 9 | `TOGGLE_FULLSCREEN` | Toggle fullscreen | Переключить полноэкранный режим |
| 10 | `TOGGLE_CHEAT` | Toggle cheat mode | Переключить режим читов |
| 11 | `SCROLL_LEFT` | Scroll map left | Прокрутка карты влево |
| 12 | `SCROLL_RIGHT` | Scroll map right | Прокрутка карты вправо |
| 13 | `SCROLL_UP` | Scroll map up | Прокрутка карты вверх |
| 14 | `SCROLL_DOWN` | Scroll map down | Прокрутка карты вниз |
| 15 | `CENTER_ON_HOME` | Center on home | К стартовой точке |
| 16 | `CENTER_ON_STRUCTURE` | Center on structure | К выбранному зданию |
| 17 | `ZOOM_RESET` | Reset zoom | Сбросить масштаб карты |
| 18 | `SAVE_VIEWPORT_BOOKMARK_1` | Save view bookmark 1 | Запомнить вид 1 |
| 19 | `SAVE_VIEWPORT_BOOKMARK_2` | Save view bookmark 2 | Запомнить вид 2 |
| 20 | `SAVE_VIEWPORT_BOOKMARK_3` | Save view bookmark 3 | Запомнить вид 3 |
| 21 | `SAVE_VIEWPORT_BOOKMARK_4` | Save view bookmark 4 | Запомнить вид 4 |
| 22 | `SAVE_VIEWPORT_BOOKMARK_5` | Save view bookmark 5 | Запомнить вид 5 |
| 23 | `JUMP_TO_VIEWPORT_BOOKMARK_1` | Go to view bookmark 1 | Перейти к виду 1 |
| 24 | `JUMP_TO_VIEWPORT_BOOKMARK_2` | Go to view bookmark 2 | Перейти к виду 2 |
| 25 | `JUMP_TO_VIEWPORT_BOOKMARK_3` | Go to view bookmark 3 | Перейти к виду 3 |
| 26 | `JUMP_TO_VIEWPORT_BOOKMARK_4` | Go to view bookmark 4 | Перейти к виду 4 |
| 27 | `JUMP_TO_VIEWPORT_BOOKMARK_5` | Go to view bookmark 5 | Перейти к виду 5 |
| 28 | `QUICK_SAVE` | Quick save | Быстрое сохранение |
| 29 | `QUICK_LOAD` | Quick load | Быстрая загрузка |
| 30 | `TOGGLE_FPS` | Show FPS | Показать или скрыть FPS |
| 31 | `TOGGLE_TIME_DISPLAY` | Show game time | Показать или скрыть время игры |
| 32 | `OPEN_MENU` | Open menu | Открыть меню |
| 33 | `DEPLOY_UNIT` | Deploy / Release | Развернуть / Выпустить |
| 34 | `SET_PRIMARY` | Set primary structure | Сделать основным зданием |
| 35 | `ATTACK_MODE` | Attack / Rally | Атаковать / Точка сбора |
| 36 | `ADD_TO_SELECTION` | Add to selection | Добавить к выбору |
| 37 | `REPAIR_UNIT` | Repair | Ремонт |
| 38 | `RETURN_TO_BASE` | Return to base | Вернуться на базу |
| 39 | `SEND_TO_REFINERY` | Unload | Разгрузить |
| 40 | `SELECT_SAME_TYPE_ON_MAP` | Select units of the same type on map | Выбрать такие же юниты на карте |
| 41 | `SELECT_SAME_TYPE_ON_SCREEN` | Select units of the same type on screen | Выбрать такие же юниты на экране |
| 42 | `SELECT_INFANTRY_ON_MAP` | Select infantry on map | Выбрать пехоту на карте |
| 43 | `SELECT_INFANTRY_ON_SCREEN` | Select infantry on screen | Выбрать пехоту на экране |
| 44 | `SELECT_WHEELS_ON_MAP` | Select wheeled units on map | Выбрать колёсную технику на карте |
| 45 | `SELECT_WHEELS_ON_SCREEN` | Select wheeled units on screen | Выбрать колёсную технику на экране |
| 46 | `SELECT_TANKS_ON_MAP` | Select tanks on map | Выбрать танки на карте |
| 47 | `SELECT_TANKS_ON_SCREEN` | Select tanks on screen | Выбрать танки на экране |
| 48 | `TRACK_UNIT` | Track selected units | Следить за выбранными |
| 49 | `SELECT_LAUNCHERS_ON_MAP` | Select launchers on map | Выбрать ракетные установки на карте |
| 50 | `SELECT_LAUNCHERS_ON_SCREEN` | Select launchers on screen | Выбрать ракетные установки на экране |
| 51 | `SELECT_HARVESTERS_ON_MAP` | Select harvesters on map | Выбрать харвестеры на карте |
| 52 | `SELECT_HARVESTERS_ON_SCREEN` | Select harvesters on screen | Выбрать харвестеры на экране |
| 53 | `SELECT_ATTACKING_ON_MAP` | Select attacking units on map | Выбрать атакующих на карте |
| 54 | `GROUP_1` | Select group 1 | Выбрать группу 1 |
| 55 | `GROUP_2` | Select group 2 | Выбрать группу 2 |
| 56 | `GROUP_3` | Select group 3 | Выбрать группу 3 |
| 57 | `GROUP_4` | Select group 4 | Выбрать группу 4 |
| 58 | `GROUP_5` | Select group 5 | Выбрать группу 5 |
| 59 | `GROUP_6` | Select group 6 | Выбрать группу 6 |
| 60 | `EDITOR_SAVE` | Editor: save map | Редактор: сохранить карту |
| 61 | `EDITOR_ZOOM_IN` | Editor: zoom in | Редактор: приблизить |
| 62 | `EDITOR_ZOOM_OUT` | Editor: zoom out | Редактор: отдалить |
| 63 | `EDITOR_DISPLAY_GRID` | Editor: show grid | Редактор: сетка |
| 64 | `EDITOR_DISPLAY_AXES` | Editor: show axes | Редактор: оси |
| 65 | `EDITOR_UNDO` | Editor: undo | Редактор: отменить |
| 66 | `EDITOR_REDO` | Editor: redo | Редактор: повторить |
| 67 | `EDITOR_COPY` | Editor: copy | Редактор: копировать |
| 68 | `EDITOR_PASTE` | Editor: paste | Редактор: вставить |
| 69 | `EDITOR_CUT` | Editor: cut | Редактор: вырезать |
| 70 | `MENU_BACK` | Menu: back | Меню: назад |
| 71 | `MENU_CONFIRM` | Menu: confirm | Меню: подтвердить |
| 72 | `MENU_CANCEL` | Menu: cancel | Меню: отмена |
| 73 | `DEBUG_WIN` | Debug: win mission | Отладка: победа в миссии |
| 74 | `DEBUG_LOSE` | Debug: lose mission | Отладка: поражение в миссии |
| 75 | `DEBUG_GIVE_CREDITS` | Debug: give credits | Отладка: выдать кредиты |
| 76 | `DEBUG_DESTROY_AT_CURSOR` | Debug: destroy at cursor | Отладка: уничтожить под курсором |
| 77 | `DEBUG_REVEAL_MAP` | Debug: reveal map | Отладка: открыть карту |
| 78 | `DEBUG_DAMAGE_AT_CURSOR` | Debug: damage at cursor | Отладка: повредить под курсором |
| 79 | `DEBUG_KILL_CARRYALLS` | Debug: kill carryalls | Отладка: уничтожить транспортники |
| 80 | `DEBUG_SPAWN_ORNITHOPTER` | Debug: spawn ornithopter | Отладка: создать орнитоптер |
| 81 | `DEBUG_SPAWN_WORM` | Debug: spawn worm | Отладка: создать червя |
| 82 | `DEBUG_CLEAR_SHROUD_AT_CURSOR` | Debug: clear shroud at cursor | Отладка: снять туман под курсором |
| 83 | `DEBUG_SWITCH_PLAYER_0` | Debug: switch to player 0 | Отладка: переключиться на игрока 0 |
| 84 | `DEBUG_SWITCH_PLAYER_1` | Debug: switch to player 1 | Отладка: переключиться на игрока 1 |
| 85 | `DEBUG_SWITCH_PLAYER_2` | Debug: switch to player 2 | Отладка: переключиться на игрока 2 |
| 86 | `DEBUG_SWITCH_PLAYER_3` | Debug: switch to player 3 | Отладка: переключиться на игрока 3 |

### 10. Режим отладки интерфейса: сцены страниц

Сцены (все в группе `options-game`, запуск из боя, как `options-game-main-nosaves`): `options-game-game` (страница «Игра»), `options-game-controls` («Управление»), `options-game-diagnostics` («Диагностика»), `options-game-keybind` («Управление» с захватом клавиши первого действия `SCREENSHOT`). Сцен `options-menu-*` для новых страниц нет.

- `src/debug/UiAudit.hpp`: после строки `    static bool optionsStatus(cGame &game);` — строки `    static bool optionsPage(cGame &game, int page);` и `    static bool optionsBinding(cGame &game);`.
- `src/debug/UiAuditAccess.cpp`: после функции `UiAuditAccess::optionsStatus` (перед `UiAuditAccess::creditsScroll`) — определения:

```cpp
bool UiAuditAccess::optionsPage(cGame &currentGame, int page)
{
    auto *options = dynamic_cast<cOptionsState *>(currentGame.m_currentState);
    if (options == nullptr) {
        return false;
    }
    options->switchOptionsPage(static_cast<cOptionsState::OptionsPage>(page));
    return true;
}

bool UiAuditAccess::optionsBinding(cGame &currentGame)
{
    auto *options = dynamic_cast<cOptionsState *>(currentGame.m_currentState);
    if (options == nullptr) {
        return false;
    }
    options->m_bindingCapture = eKeyAction::SCREENSHOT;
    options->refresh();
    return true;
}
```

- `src/debug/UiAuditScenes.cpp`: перед строкой `bool prepareCredits(cGame &game)` — функция и пустая строка после неё:

```cpp
template <int Variant>
bool readyOptionsPage(cGame &game)
{
    switch (g_step) {
        case 0:
            UiAuditAccess::setState(game, GAME_OPTIONS);
            g_step = 1;
            g_wait = 0;
            return false;
        case 1:
            if (!pause(4)) {
                return false;
            }
            UiAuditAccess::optionsPage(game, Variant == 4 ? 2 : Variant);
            if (Variant == 4) {
                UiAuditAccess::optionsBinding(game);
            }
            g_step = 2;
            return false;
        default:
            return pause(4);
    }
}
```

  Номер страницы: `Main` = 0, `Gameplay` = 1, `Controls` = 2, `Diagnostics` = 3; вариант 4 — «Управление» с захватом.
- `src/debug/UiAuditScenes.cpp`: сразу после строки сцены `"options-menu-applied"` добавляются строки:

```cpp
    scene("options-game-game", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsPage<1>),
    scene("options-game-controls", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsPage<2>),
    scene("options-game-diagnostics", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsPage<3>),
    scene("options-game-keybind", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsPage<4>),
```

- `tests/ui_audit/ui_audit_part3a_catalog.py`: кортеж `("main-saves", "main-nosaves", "applied")` в `expected_scenes` становится `("main-saves", "main-nosaves", "applied", "game", "controls", "diagnostics", "keybind")`; `EXPECTED_COUNT = 25` становится `EXPECTED_COUNT = 29`.
- `tests/ui_audit/ui_audit_part3a_scenes.py`: после строки `IN_GAME_OPTIONS_TEXTS = ("Mission select", "Save game", "Load game")` — строка `CONTROLS_RANGE = ("Actions 1-", " of 86")`; перед функцией `check_for` — функции:

```python
def check_options_page(*texts):
    def check(header, body):
        return first_error(
            forbid_kinds(body, ("area", "label")),
            None if records_of(body, "gui") else "no gui records",
            *(require_text(body, text) for text in texts),
            f"the status text {STATUS_TEXT!r} must not be shown before applying"
            if any(record["s"] == STATUS_TEXT for record in records_of(body, "text")) else None,
        )
    return check


def check_options_controls(header, body):
    prefix, suffix = CONTROLS_RANGE
    ranges = [record["s"] for record in records_of(body, "text")
              if record["s"].startswith(prefix) and record["s"].endswith(suffix)]
    return first_error(check_options_page("Take screenshot")(header, body),
                       None if ranges else f"no text record {prefix}<n>{suffix}")
```

  в словарь `fixed` функции `check_for` после строки `"options-game-applied": check_options_game_applied,` добавляются строки:

```python
        "options-game-game": check_options_page("Edge scrolling — move camera at screen edge",
                                                "Rules file: game.ini (change manually)"),
        "options-game-controls": check_options_controls,
        "options-game-diagnostics": check_options_page("Show resource usage"),
        "options-game-keybind": check_options_page("Take screenshot", "Press key..."),
```

- `tests/ui_audit/data/latin-ru-allowed.tsv`: скрипт `ui_audit_translation.py` запускает сцены на русском. Латинский текст сцен `options-game-controls` и `options-game-keybind` — названия клавиш SDL (`F11`, `Left Ctrl`, `Keypad +`, `Alt+Return` и другие, всё, что даёт `describeBinding` для видимых строк). Для каждого такого текста, который скрипт сообщил как недопустимый, в конец файла добавляется строка: регулярное выражение, полностью совпадающее с текстом (специальные символы экранируются, как в соседних строках), табуляция, причина `название клавиши SDL на кнопке привязки (src/gamestates/cOptionsPages.cpp)`. Любой другой латинский текст, о котором сообщил скрипт, — блок `## Q-P10C-NN` и стоп.
- Ожидание числа сцен: `--ui-audit-list` даёт на четыре сцены больше прежнего; других сцен шаг не добавляет и не убирает.
- Общие проверки сцен своей части: `check_options_game_main` (`IN_GAME_OPTIONS_TEXTS`: «Mission select», «Save game», «Load game») к новым сценам неприменима — на новых страницах этих кнопок нет, поэтому для новых сцен введены функции выше; запрет записей `area` и `label` (`forbid_kinds`) действует и для них. `tools/ui-audit/check_options_geometry.py` (`OPTIONS_SCENES`) не расширяется: правила 3 и 9 новые сцены не проверяют. Скрипт `ui_audit_part2_scenes.py` (`options-menu-main`, `options-menu-applied`) и `ui_audit_saves.py` (`options-game-main-*`) к странице «Основные» с двумя новыми строками применяются без правок.

### 11. Опись клавиш режима отладки

Перенос из форка (`FORK1`) с заменой под клавиши порта; `keys.tsv` собирается заново по коду после всех правок пунктов 1–10 (шаг 7 плана).

- `tools/ui-audit/extract_keys.py` — копия файла форка (`git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/extract_keys.py`) с двумя правками: строка `KEY_TOKEN = re.compile(r"SDLK_\w+|SDL_SCANCODE_\w+|m_commandBindings\.\w+|\bcommandBindings?\b")` становится `KEY_TOKEN = re.compile(r"SDLK_\w+|SDL_SCANCODE_\w+|eKeyAction::\w+")`; после строки `SOURCE_SUFFIXES = (".cpp", ".h", ".hpp", ".c", ".cc")` — строка `EXCLUDED_FILES = ("src/controls/cKeyBindings.cpp",)`, и в `extract_tree` перед строкой `rows += extract(...)` — условие: если `relative in EXCLUDED_FILES`, файл пропускается (`continue`). Причина исключения: таблица умолчаний и имён действий — определение клавиш, а не обработчик клавиши.
- `tools/ui-audit/check_keys.py` — копия файла форка с одной правкой: строка `BINDING_PREFIX = "m_commandBindings."` становится `BINDING_PREFIX = "eKeyAction::"`. Смысл: строка с ключом `eKeyAction::<ИМЯ>` — место, где код читает переназначаемое действие (в порту переназначаемы все действия таблицы); такие строки не участвуют в поиске конфликтов правила 10 между фиксированными клавишами, а дают список «переназначаемое действие × состояние». Проверка занятости клавиши при переназначении в порту — `cKeyBindings::findConflict`, поэтому проверка `check_keys.py` запускается с `--binding-check src/controls/cKeyBindings.cpp:findConflict`.
- `tools/ui-audit/tests/test_extract_keys.py`, `tools/ui-audit/tests/test_check_keys.py` — копии файлов форка плюс новые случаи (раздел «Тесты»).
- `tools/ui-audit/keys.tsv` — новая таблица; первая строка `file<TAB>function<TAB>key<TAB>mods<TAB>line<TAB>state<TAB>action<TAB>reason`. Правила:
  1. Строк данных столько же, сколько строк даёт `python3 tools/ui-audit/extract_keys.py --root . --out .tmp/p10c/keys-raw.tsv` (на `B` без правок шага — 218; после правок шага число считает скрипт). Каждой строке сырой выгрузки соответствует одна строка таблицы с теми же `file`, `function`, `key` и тем же порядком; `line` — номер строки в сырой выгрузке; свежесть проверяет `check_keys.py` (номера строк не сравниваются).
  2. `state` — одно или несколько состояний через ` | ` из перечня: `any state`, `main menu`, `choose house`, `select next conquest`, `credits`, `skirmish setup`, `mentat`, `editor`, `options: key capture`, `save/load dialog`, `game: nothing selected`, `game: structure selected`, `game: units selected`, `game: repair mode`, `game: debug mode`. Состояние выбирается по условиям, при которых код доходит до строки (какой обработчик состояния или режима мыши её вызывает); строка, действующая во всех состояниях боя, получает все пять состояний `game: …`. Состояния вне перечня не вводятся: нужное состояние вне перечня — блок `## Q-P10C-NN` и стоп.
  3. `action` — для ключа `eKeyAction::<ИМЯ>` это `<ИМЯ>` строчными буквами, `_` заменён на `-` (например, `quick-save`); для ключа `SDL_SCANCODE_*` и `SDLK_*` — короткое название действия латиницей строчными буквами через `-`, одинаковое для одного и того же действия во всех строках.
  4. `mods` — модификаторы, которые условие строки требует вместе с клавишей, заглавными буквами через `+` (`CTRL`, `SHIFT`, `ALT`); пусто, если условие модификаторов не требует. Для ключа `eKeyAction::<ИМЯ>` поле пустое.
  5. Строка, которая не является обработчиком клавиши (сравнение с «нет клавиши», размер таблицы, обработка модификатора, служебная запись), получает `state` = `-`, `action` = `-` и непустую `reason` по-русски одной фразой. У строки с `action` не `-` поле `reason` пустое, а `state` не `-`.
  6. Вызовы `cKeyBindings::`, `cKeyboard::`, `cKeyboardEvent::` в `src/controls/cKeyBindings.h`, `cKeyboard.*`, `cKeyboardEvent.*` — это передача событий, а не обработчики: их строки получают `-` и причину.
  7. Строка, добавленная этим шагом в `cOptionsState` (`SDL_SCANCODE_ESCAPE`, `SDL_SCANCODE_UNKNOWN` в `onNotifyKeyboardEvent`), получает состояние `options: key capture`; для `SDL_SCANCODE_ESCAPE` — действие `cancel-capture`.

### 12. Сохранить из апстрима

1. `cKeyBindings::loadFromSection`, `checkForClashes`, `matches`, `containsActionKey`, `getFirstKeyDisplayName` и `loadDefaults` не меняются; ни `resources/bin/settings.ini`, ни его раздел `[KEYS]` не меняются; `settings.ini` программа по-прежнему только читает.
2. `Preferences::load`, `save`, `saveScales`, `saveLanguage`, `loadScales`, `loadLanguage` сохраняют прежнее поведение; тесты `tests/utils/test_Preferences.cpp` проходят без правок. `-prefs` читает все ключи файла, аргументы командной строки идут после.
3. `OptionsMenuLayout::create` с прежними четырьмя или пятью аргументами даёт прежний результат; тест `tests/utils/test_OptionsMenu.cpp` проходит без правок.
4. Строки 1–8 страницы «Основные», их положение и поведение (музыка, звук, скорость игры, «FOW», масштабы, «Low power icon», язык), кнопки «Main menu», «Quit game», «Back», «Save game», «Load game», «Mission select» и диалог сохранений не меняются. «FOW» и «Low power icon» остаются на «Основных» и пишутся в `preferences.ini` при выходе из игры, как раньше.
5. Глобальные клавиши игры (снимок экрана, `Alt+Enter`, консоль и другие) работают, как раньше, везде, кроме момента захвата клавиши в окне настроек.
6. Камера, менеджер фокуса, строки `cGame::currentSettings` и `cGame::applySettings` (кроме добавленных строк) не меняются.

### 13. Правила переноса и подключения

Правила применяются к каждой строке форка, которую пункты 5–8 переносят в порт.

1. `optionText(m_selectedSettings, "<en>", "<ru>")` → `localization::text("<en>", "<ru>")`.
2. `m_game.m_screenW` → `m_settings->getScreenW()`, `m_game.m_screenH` → `m_settings->getScreenH()`.
3. `new GuiWindow(rect, m_textDrawer)` → `std::make_unique<GuiWindow>(m_sdlDrawer, rect, m_textDrawer)`.
4. Построители виджетов порта возвращают `std::unique_ptr`: каждый `GuiButtonBuilder`, `GuiLabelBuilder`, `GuiSliderBuilder`, `GuiCheckBoxBuilder` получает `.withRenderer(m_sdlDrawer)` (так же, как их строки в нынешнем `constructWindow` порта); результат кладётся в окно через `m_guiWindow->addGuiObject(std::move(объект))`; если указатель на объект нужен позже, он берётся до `std::move`.
5. `GameSettings::<поле>` → `InitialGameSettings::<то же поле>`; `m_selectedSettings` → `m_selected`; привязки форка `m_selectedSettings.commandBindings` не переносятся (их заменяет `m_selectedBindings`).
6. `cLogger::getInstance()->log(...)` → `Logger::warn(COMP_GAMERULES, "Preferences", "...{}", error)`.
7. Строки с `m_game.`, не названные выше, `uiaudit::` и `UiAuditAccess`, функции `saveSettingsToIni`, `loadSettingsFromIni`, `commandBinding*`, `trySetCommandBinding`, `bindingKeyName` не переносятся.
8. Вызов функции форка, у которой нет пары в порту и которая не названа в контракте, — блок `## Q-P10C-NN` и стоп.

**Подключение.** Каждая новая строка `#include "…"` из пунктов 1–10 добавляется сразу после последней строки вида `#include "…"` в начале файла, если такой строки в файле ещё нет; новая строка `#include <…>` — сразу после последней строки вида `#include <…>` блока подключений, а если таких строк нет — сразу после последней строки `#include "…"`; несколько новых строк одного файла идут подряд в порядке пунктов. Исключения: пункты, которые называют место строки сами (`Preferences.hpp`, `Preferences.cpp`, `cKeyBindings.h`, `cOptionsState.h`). В `cGame_logic.cpp` так добавляется `game/Preferences.hpp`, в `cOptionsState.cpp` — `<SDL3/SDL.h>`, `<format>`, `controls/cKeyboard.h`, `controls/cKeyboardEvent.h`, `controls/sMouseEvent.h`, `gamestates/OptionsKeyLabels.hpp`, в `src/CMakeLists.txt` — строка `    gamestates/cOptionsPages.cpp` сразу после строки `    gamestates/cOptionsState.cpp`.

## Тесты

Новые тесты Catch2: имя каждого случая начинается с `P10C `, тег `[P10C]`. Тесты форка шага — не Catch2 (`int main()`): каждая проверка переносится в новый случай (таблица ниже); число проверок (`REQUIRE`/`CHECK`) в новых файлах не меньше числа проверок в файлах форка (7 и 1). Тесты пишутся в шаге 1 плана. В шаге 2 они краснеют: сборка падает, потому что нет методов `cKeyBindings::trySetBinding` и других, функций `Preferences::saveOnExit` и других и заголовков `OptionsPageData.hpp`, `OptionsKeyLabels.hpp`, `AdvancedOptionsHeaderLayout.hpp`; Python-тесты падают на импорте: модулей `extract_keys` и `check_keys` ещё нет.

**`tests/CMakeLists.txt`:** в `TEST_FILES` сразу после строки `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_OptionsMenu.cpp` — строки (в этом порядке):

```
    ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_KeyRebinding.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_OptionPages.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_PreferencesPages.cpp
```

`TEST_SOURCES` не меняется (`cKeyBindings.cpp`, `Preferences.cpp`, `cIniFile.cpp`, `cRectangle.cpp` в нём уже есть; новые заголовки не требуют `.cpp`).

**T1 — `tests/controls/test_KeyRebinding.cpp`.** Подключает `controls/cKeyBindings.h`, `utils/cIniFile.h`, `game/Preferences.hpp`. Помощник `s_KeyBinding single(SDL_Scancode key, bool ctrl = false, bool alt = false, bool shift = false, bool tab = false)`. Таблица «проверка форка → случай» и остальные случаи; `defaults()` — объект `cKeyBindings` после `loadDefaults()`, каждый случай начинается с нового `defaults()`, если не сказано иное:

| № | Случай | Ожидание | Проверка форка |
|---|---|---|---|
| 1 | `P10C a taken key is refused and names its owner` | `setBinding(ATTACK_MODE, single(A))`, `setBinding(REPAIR_UNIT, single(B))`; `trySetBinding(ATTACK_MODE, single(B))` возвращает `REPAIR_UNIT` | 1 |
| 2 | `P10C a refused binding leaves both actions unchanged` | после случая 1: `getBinding(ATTACK_MODE)->keys == {A}`, `getBinding(REPAIR_UNIT)->keys == {B}` | 2, 3 |
| 3 | `P10C left and right Ctrl are different keys` | `setBinding(ATTACK_MODE, single(LCTRL))`; `trySetBinding(REPAIR_UNIT, single(RCTRL))` не даёт конфликта; `getBinding(REPAIR_UNIT)->keys == {RCTRL}` | 4, 5 |
| 4 | `P10C an event with the left Ctrl belongs to the left Ctrl binding only` | при `ATTACK_MODE = {LCTRL}`: `containsActionKey(набор{LCTRL}, ATTACK_MODE)` истинно, `containsActionKey(набор{RCTRL}, ATTACK_MODE)` ложно | 6, 7 |
| 5 | `P10C left and right Shift are the same key` | `defaults()`: `trySetBinding(REPAIR_UNIT, single(LSHIFT))` и `trySetBinding(REPAIR_UNIT, single(RSHIFT))` дают `ADD_TO_SELECTION` | новый |
| 6 | `P10C left and right Alt are the same key` | `setBinding(RETURN_TO_BASE, single(RALT))`; `trySetBinding(REPAIR_UNIT, single(LALT))` даёт `RETURN_TO_BASE` | новый |
| 7 | `P10C modifiers make a different key` | `defaults()`: `trySetBinding(REPAIR_UNIT, single(Z, true))` даёт `SELECT_SAME_TYPE_ON_MAP`; `trySetBinding(REPAIR_UNIT, single(Z))` даёт `ZOOM_RESET`; `trySetBinding(REPAIR_UNIT, single(Z, false, false, false, true))` не даёт конфликта | новый |
| 8 | `P10C the default shared pairs come from loadDefaults` | `getDefaultSharedPairs()` содержит ровно пять пар (в любом порядке и порядке внутри пары): `DEPLOY_UNIT`/`SEND_TO_REFINERY`, `MUSIC_VOLUME_UP`/`SET_PRIMARY`, `TOGGLE_FPS`/`RETURN_TO_BASE`, `OPEN_MENU`/`MENU_BACK`, `SELECT_SAME_TYPE_ON_MAP`/`EDITOR_UNDO` | новый |
| 9 | `P10C actions that share a default key do not conflict` | `defaults()`: `trySetBinding(DEPLOY_UNIT, single(D))`, `trySetBinding(SEND_TO_REFINERY, single(D))`, `trySetBinding(SET_PRIMARY, single(P))` не дают конфликта | новый |
| 10 | `P10C other actions still conflict on a shared key` | `defaults()`: `trySetBinding(DEPLOY_UNIT, single(P))` даёт `MUSIC_VOLUME_UP`; `getBinding(DEPLOY_UNIT)->keys == {D}` | новый |
| 11 | `P10C actions outside the table are not checked` | `defaults()`: `trySetBinding(REPAIR_UNIT, single(1, true))` не даёт конфликта (клавиша `1` — `SDL_SCANCODE_1`; `GROUP_ASSIGN_1` в таблице нет) | новый |
| 12 | `P10C every table action survives the [KEYS] round trip` | для каждой пары `getActionTable()`: значение `defaults().toIniValue(action)` записывается в `cIniFile` (раздел `KEYS`, ключ — имя из таблицы), новый пустой `cKeyBindings` читает `loadFromSection`; `getBinding(action)` не `nullptr`, `keys` и четыре флага модификаторов равны исходным; число проверенных действий равно 86 | новый |
| 13 | `P10C the file of the player overrides settings.ini` | временная папка; `Preferences::saveKeyBindings` пишет файл `settings.ini`-подобный (раздел `KEYS`: `REPAIR=Q`, `QUICK_SAVE=F8`) и файл предпочтений (`REPAIR=W`, `SCREENSHOT=F10`); `defaults()`, затем `loadFromSection` первого файла, затем `loadFromSection` второго (через `Preferences::loadKeyBindings`): `REPAIR_UNIT` — `{W}`, `SCREENSHOT` — `{F10}`, `QUICK_SAVE` — `{F8}`, `TOGGLE_MUSIC` — `{M, MUTE}` | новый |
| 14 | `P10C keys that cannot be written are refused` | `canStoreKey`: ложно для `SDL_SCANCODE_UNKNOWN`, `SDL_SCANCODE_TAB`, `SDL_SCANCODE_COMMA`; истинно для `SDL_SCANCODE_A`, `SDL_SCANCODE_LCTRL`, `SDL_SCANCODE_F11` | новый |
| 15 | `P10C a captured key takes the modifiers that were held` | `makeCapturedBinding(Z, {ctrl})`: `keys == {Z}`, `requireCtrl`; `makeCapturedBinding(LCTRL, {shift})`: `keys == {LCTRL}`, `requireShift`, `requireCtrl` ложно; `makeCapturedBinding(LCTRL, {ctrl})`: `requireCtrl` ложно; `makeCapturedBinding(F2, {shift, tab})`: `requireShift` и `requireTab`; `makeCapturedBinding(TAB, {tab})`: `requireTab` ложно | новый |
| 16 | `P10C bindings are described for the player` | `defaults()`: `getBindingDisplayName(ATTACK_MODE) == "Ctrl"`, `(ADD_TO_SELECTION) == "Shift"`, `(TOGGLE_FULLSCREEN) == "Alt+Return"`, `(SELECT_SAME_TYPE_ON_MAP) == "Ctrl+Z"`, `(DEBUG_WIN) == "Shift+Tab+F2"`, `(REPAIR_UNIT) == "R"`; `describeBinding(single(LCTRL)) == "Left Ctrl"`; пустой `cKeyBindings`: `getBindingDisplayName(REPAIR_UNIT)` пуст | новый |
| 17 | `P10C the action table has names for the options page` | `getActionTable().size() == 86`; `getActionName(REPAIR_UNIT) == "REPAIR"`; `getActionName(SCREENSHOT) == "SCREENSHOT"`; `getActionName(GROUP_ASSIGN_1)` пуст | новый |

**T2 — `tests/utils/test_OptionPages.cpp`** (подключает `gamestates/AdvancedOptionsHeaderLayout.hpp`, `gamestates/OptionsMenuLayout.hpp`, `gamestates/OptionsPageData.hpp`, `gamestates/OptionsKeyLabels.hpp`, `game/Preferences.hpp`, `controls/cKeyBindings.h`):

| № | Случай | Ожидание | Проверка форка |
|---|---|---|---|
| 1 | `P10C the settings title does not overlap a tab` | `AdvancedOptionsHeaderLayout::create(760, 8, 34, 24)`: для каждой из четырёх вкладок прямоугольники заголовка и вкладки не пересекаются (пересечение — как функция `overlaps` в `FORK1:tests/InteractionRegressionTests.cpp`, строки 22–28) | `InteractionRegression` (1 проверка) |
| 2 | `P10C the settings header has the exact geometry` | `create(760, 8, 34, 24)`: заголовок `(0, 2, 760, 24)`; вкладки `(8, 34, 180, 34)`, `(196, 34, 180, 34)`, `(384, 34, 180, 34)`, `(572, 34, 180, 34)` | новый |
| 3 | `P10C the list scroll helpers` | `optionsVisibleRows(76, 560, 38) == 12`; `optionsVisibleRows(100, 100, 38) == 1`; `optionsVisibleRows(0, 1000, 0) == 1`; `optionsMaxScrollRow(86, 12) == 74`; `optionsMaxScrollRow(10, 12) == 0`; `optionsClampScrollRow(100, 86, 12) == 74`; `optionsClampScrollRow(-5, 86, 12) == 0`; `optionsClampScrollRow(30, 86, 12) == 30` | новый |
| 4 | `P10C resolution choices follow the desktop` | `resolutionChoices(1920, 1080, {1280, 720})` — ровно 16 элементов в порядке: 800×600, 1024×600, 1024×768, 1280×720, 1280×768, 1152×864, 1280×800, 1360×768, 1366×768, 1280×960, 1440×900, 1280×1024, 1600×900, 1600×1024, 1680×1050, 1920×1080; `resolutionChoices(1366, 700, {1000, 700})` — ровно `{800,600}`, `{1024,600}`, `{1000,700}`, `{1366,700}` | новый |
| 5 | `P10C the saved resolution is selected` | `resolutionChoiceIndex(resolutionChoices(1920, 1080, {1280, 720}), {1280, 720}) == 3`; для `{123, 45}` результат `0` | новый |
| 6 | `P10C every table action has a label` | `KEY_ACTION_LABELS.size() == 86`; для каждой пары `getActionTable()` на том же индексе `KEY_ACTION_LABELS[i].action` равно действию; `english` и `russian` не пусты; все `english` различны; все `russian` различны; `findKeyActionLabel(GROUP_ASSIGN_1) == nullptr` | новый |
| 7 | `P10C the page keys are the chosen keys` | размеры `MAIN_PAGE_KEYS`, `GAMEPLAY_PAGE_KEYS`, `DIAGNOSTICS_PAGE_KEYS` — 6, 7, 8; их объединение — ровно `Preferences::CHOSEN_KEYS` (21 различный ключ) | новый |
| 8 | `P10C the options menu layout keeps its rows without extra rows` | `OptionsMenuLayout::create(1920, 1080, 42, true)` равна `create(1920, 1080, 42, true, -1, 0)` по полям `window`, `apply`, `save`, `quit`; `apply.getY() == 440` | новый |
| 9 | `P10C two extra content rows move the action rows down` | `create(1920, 1080, 42, false, -1, 2)`: `apply == (24, 528, 170, 42)`, `window == (620, 200, 680, 680)`, `quit.getY() == 630`, `contentTop == 44`; `create(1920, 1080, 42, true, -1, 2)`: `apply.getY() == 528`, `save.getY() == 584` | новый |

**T3 — `tests/utils/test_PreferencesPages.cpp`** (подключает `game/Preferences.hpp`, `utils/cIniFile.h`, `utils/InitialGameSettings.hpp`; каждая проверка работает во временной папке, как `tests/utils/test_Preferences.cpp`):

| № | Случай | Ожидание |
|---|---|---|
| 1 | `P10C the chosen keys are the 21 keys of the options menu` | `CHOSEN_KEYS` равен списку: `RenderScale`, `WorldScale`, `Language`, `ScreenWidth`, `ScreenHeight`, `FullScreen`, `CameraEdgeMove`, `CameraBorderOrKeyMoveSpeed`, `CameraDragMoveSpeed`, `pauseWhenLosingFocus`, `AllowRepeatingReinforcements`, `AllTurretsDownOnLowPower`, `RocketTurretsDownOnLowPower`, `Debug`, `NoAI`, `oneAi`, `disableWormAi`, `disableReinforcements`, `noAiRest`, `drawUnitDebug`, `drawUsages` |
| 2 | `P10C loadChosenOptions reads only the chosen keys` | `Preferences::save` пишет настройки (`screenW = 1280`, `debugMode = true`, `cameraDragMoveSpeed = 0.75f`, `playMusic = false`, `fogOfWarEnabled = true`); `loadChosenOptions` в настройки по умолчанию даёт `screenW == 1280`, `debugMode`, `cameraDragMoveSpeed == 0.75f`, а `playMusic` остаётся `true`, `fogOfWarEnabled` — `false`; на отсутствующем файле возвращает `false`, `error` не пуст, настройки не тронуты |
| 3 | `P10C saved values keep the other keys and the key bindings` | `saveKeyBindings(F, {{"REPAIR", "Q"}})` создаёт файл; затем `saveValues(F, {{"Debug", "true"}, {"ScreenWidth", "1024"}})`; `Preferences::load` даёт `debugMode` и `screenW == 1024`; `loadKeyBindings` даёт раздел с `REPAIR == "Q"`; после `saveScales(F, 150, 125, error)` `REPAIR` остаётся `"Q"`, `debugMode` остаётся `true` |
| 4 | `P10C a file with only key bindings has no chosen options` | файл только с `[KEYS]` (создан `saveKeyBindings`): `loadChosenOptions` возвращает `false`, `error` не пуст; `loadKeyBindings` возвращает `true` |
| 5 | `P10C the exit save keeps the chosen keys and the key bindings` | файл из `saveValues({{"Debug", "true"}, {"RenderScale", "150"}})` и `saveKeyBindings({{"REPAIR", "Q"}})`; `saveOnExit` с настройками `debugMode = false`, `renderScalePercent = 100`, `playMusic = false`, `fogOfWarEnabled = true`, `screenW = 1280`; в файле: `Debug == "true"`, `RenderScale == "150"`, `ScreenWidth` отсутствует, `playMusic == "false"`, `fogOfWarEnabled == "true"`, раздел `KEYS` содержит `REPAIR == "Q"` |
| 6 | `P10C the exit save of a missing file writes no chosen key` | `saveOnExit` в отсутствующий файл создаёт его; `playMusic` есть; `Debug`, `NoAI`, `RenderScale`, `ScreenWidth` отсутствуют |
| 7 | `P10C valuesOf renders the requested keys in order` | настройки по умолчанию с `debugMode = true`; `valuesOf(settings, {"Debug", "FullScreen", "ScreenWidth", "Unknown"})` — ровно три пары: `("Debug", "true")`, `("FullScreen", "true")`, `("ScreenWidth", "800")` |

**Python, `unittest`:**

- `tools/ui-audit/tests/test_extract_keys.py` — 10 случаев: 8 случаев форка без изменений и два новых. В начало файла после строки `import sys` добавляется строка `import tempfile`. В класс `ExtractKeys` добавляются методы:

```python
    def test_action_token_is_a_row(self):
        text = "void A::f(const cKeyboardEvent &event) {\n    if (event.isAction(eKeyAction::QUICK_SAVE)) {}\n}\n"
        rows = extract_keys.extract(text, "a.cpp")
        self.assertEqual([(r["function"], r["key"], r["line"]) for r in rows], [("A::f", "eKeyAction::QUICK_SAVE", 2)])

    def test_the_defaults_table_file_gives_no_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "src" / "controls"
            source.mkdir(parents=True)
            (source / "cKeyBindings.cpp").write_text(
                "void f() { bind(eKeyAction::SCREENSHOT, {SDL_SCANCODE_F11}); }\n", encoding="utf-8")
            (source / "other.cpp").write_text("void g() { return SDLK_A; }\n", encoding="utf-8")
            rows = extract_keys.extract_tree(directory)
        self.assertEqual([row["file"] for row in rows], ["src/controls/other.cpp"])
```

- `tools/ui-audit/tests/test_check_keys.py` — 24 случая: 23 случая форка без изменений и один новый; в класс `KeyRebinding` добавляется метод:

```python
    def test_action_rows_are_rebindable_commands_with_their_states(self):
        rows = [
            row("game: units selected", "eKeyAction::REPAIR_UNIT", "repair-unit"),
            row("game: repair mode", "eKeyAction::REPAIR_UNIT", "repair-unit"),
            row("game: units selected", "SDL_SCANCODE_TAB", "debug-keys"),
        ]
        self.assertEqual(check_keys.rebindable_from_rows(rows), [
            {"command": "REPAIR_UNIT", "states": ["game: units selected", "game: repair mode"]},
        ])
```

Новые случаи Catch2: 17 + 9 + 7 = 33 (число `P10C ` в `ctest.log` после сборки — 33). Python: 34 случая в двух файлах.

## PLAN-P10C

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tests/controls/test_KeyRebinding.cpp`, `tests/utils/test_OptionPages.cpp`, `tests/utils/test_PreferencesPages.cpp`, `tests/CMakeLists.txt`, `tools/ui-audit/tests/test_extract_keys.py`, `tools/ui-audit/tests/test_check_keys.py` | Раздел «Тесты». Python-тесты — копии файлов форка плюс новые методы; пока нет `extract_keys.py` и `check_keys.py`, они не запускаются как зелёные. | помощник A |
| 2 | — | Красный прогон: команда сборки проверки 1, у которой вместо `.tmp/p10c/build.log` стоит `.tmp/p10c/red-build.log`, — код выхода не `0`, в логе есть строки с `test_KeyRebinding.cpp`, `test_OptionPages.cpp` или `test_PreferencesPages.cpp` и с `trySetBinding`, `saveOnExit` или `OptionsPageData.hpp`. Красный Python: `cd tools/ui-audit/tests && python3 -B -m unittest test_extract_keys test_check_keys` — падает на импорте (нет модулей `extract_keys`, `check_keys`). Запускается до того, как шаги 3–6 и 8 записали код. | помощник A |
| 3 | `src/controls/cKeyBindings.h`, `src/controls/cKeyBindings.cpp`, `src/controls/cKeyboard.h`, `src/controls/cKeyboardEvent.h`, `src/controls/cKeyboardEvent.cpp`, `src/game/Preferences.hpp`, `src/game/Preferences.cpp` | Пункты 1 и 2 контракта. | помощник B |
| 4 | `src/game/cGameSettings.h`, `src/game/cGame_logic.cpp`, `src/main.cpp` | Пункт 3 контракта. | помощник B |
| 5 | `src/gamestates/AdvancedOptionsHeaderLayout.hpp`, `src/gamestates/OptionsPageData.hpp`, `src/gamestates/OptionsKeyLabels.hpp`, `src/gamestates/OptionsMenuLayout.hpp`, `src/gamestates/cOptionsState.h`, `src/gamestates/cOptionsState.cpp`, `src/gamestates/cOptionsPages.cpp`, `src/CMakeLists.txt` | Пункты 4–9 и 13 контракта. Заголовки `AdvancedOptionsHeaderLayout.hpp`, `OptionsPageData.hpp`, `OptionsKeyLabels.hpp` не создаются, пока помощник A не записал в журнал хода строку о конце шага 2. | помощник C |
| 6 | `src/debug/UiAudit.hpp`, `src/debug/UiAuditAccess.cpp`, `src/debug/UiAuditScenes.cpp`, `tests/ui_audit/ui_audit_part3a_catalog.py`, `tests/ui_audit/ui_audit_part3a_scenes.py`, `tests/ui_audit/data/latin-ru-allowed.tsv` | Пункт 10 контракта (строки `latin-ru-allowed.tsv` добавляются после первого запуска `ui_audit_translation.py` в шаге 8). | помощник C |
| 7 | `tools/ui-audit/extract_keys.py`, `tools/ui-audit/check_keys.py`, `tools/ui-audit/keys.tsv` | Пункт 11 контракта; `keys.tsv` собирается после шагов 3–6. | помощник A |
| 8 | — | Проверки раздела «Проверки» по порядку. Правки по их итогам делают помощники своих шагов. | помощник A |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p10c`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P10C-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p10c && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p10c/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345; в `ctest.log` 33 строки со случаями `P10C ` со статусом `Passed`; существующие тесты `tests/utils/test_Preferences.cpp` и `tests/utils/test_OptionsMenu.cpp` проходят.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает.
2. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -F -f .tmp/p10c/changed-paths.txt` — пустой вывод. Файл `.tmp/p10c/changed-paths.txt` — пути файлов `.cpp`, `.hpp` и `.h` из шагов 1, 3, 4, 5, 6 плана, по одному на строку.
3. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`.
4. **Python-тесты и опись клавиш.**
   - `python3 -B -m unittest discover -s tools/ui-audit/tests -p 'test_*.py' > .tmp/p10c/py-all.log 2>&1; echo exit=$?` — `exit=0`, в `py-all.log` последняя строка `OK`.
   - `cd tools/ui-audit/tests && python3 -B -m unittest test_extract_keys test_check_keys 2>&1 | tail -3` — строки `Ran 34 tests` и `OK`.
   - `python3 -B tools/ui-audit/extract_keys.py --root . --out .tmp/p10c/keys-raw.tsv` — код 0, строка `keys-raw rows: <K>`.
   - `python3 -B tools/ui-audit/check_keys.py --keys tools/ui-audit/keys.tsv --raw .tmp/p10c/keys-raw.tsv --binding-check src/controls/cKeyBindings.cpp:findConflict` — код 0, в выводе строка `keys: freshness OK; rule 10 flags: <F>`; число `<F>` записать в сдачу вместе с выводом строк правила 10.
   - `git grep --untracked -n 'findConflict' -- src/controls/cKeyBindings.cpp` — не пуст.
   - Разбор `keys.tsv`: файл `.tmp/p10c/check_keys_tsv.py` с текстом ниже (создаёт помощник A, в рамку правок и коммит он не входит), затем `python3 -B .tmp/p10c/check_keys_tsv.py <K>` — код 0 и строка `annotation problems: 0`:

```python
import csv
import sys

HEADER = ["file", "function", "key", "mods", "line", "state", "action", "reason"]
STATES = {
    "any state", "main menu", "choose house", "select next conquest", "credits", "skirmish setup", "mentat",
    "editor", "options: key capture", "save/load dialog", "game: nothing selected", "game: structure selected",
    "game: units selected", "game: repair mode", "game: debug mode",
}
with open("tools/ui-audit/keys.tsv", encoding="utf-8", newline="") as handle:
    rows = list(csv.reader(handle, delimiter="\t", quoting=csv.QUOTE_NONE))
problems = []
if rows[0] != HEADER:
    problems.append(f"header differs: {rows[0]}")
data = rows[1:]
if len(data) != int(sys.argv[1]):
    problems.append(f"expected {sys.argv[1]} data rows, got {len(data)}")
for number, row in enumerate(data, 2):
    if len(row) != 8:
        problems.append(f"line {number}: {len(row)} columns")
        continue
    file, function, key, mods, line, state, action, reason = row
    if action != "-":
        states = [item.strip() for item in state.split(" | ")]
        if state == "-" or any(item not in STATES for item in states):
            problems.append(f"line {number}: bad state {state!r}")
        if reason:
            problems.append(f"line {number}: a handler row has a reason")
        if key.startswith("eKeyAction::") and action != key[len("eKeyAction::"):].lower().replace("_", "-"):
            problems.append(f"line {number}: action {action!r} does not match {key}")
    else:
        if state != "-":
            problems.append(f"line {number}: a row without an action has a state")
        if not reason:
            problems.append(f"line {number}: a row without an action has no reason")
for problem in problems[:50]:
    print(problem)
print(f"annotation problems: {len(problems)}")
sys.exit(1 if problems else 0)
```
5. **Скрипты режима отладки интерфейса.**
   - Скрипты: `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_part2_catalog.py`, `ui_audit_part2_scenes.py`, `ui_audit_part3a_catalog.py`, `ui_audit_part3a_scenes.py`, `ui_audit_saves.py`, `ui_audit_language.py`, `ui_audit_translation.py`.
   - Команда для каждого `<скрипт>`: `mkdir -p .tmp/p10c/tmp && TMPDIR=$PWD/.tmp/p10c/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p10c/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
   - Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал. Каждая команда сама ограничена `timeout 1800`; жди, пока она вернёт код выхода. `ui_audit_part2_scenes.py`, `ui_audit_part3a_scenes.py` и `ui_audit_translation.py` идут по несколько минут — это норма.
   - `ui_audit_translation.py` может сначала вернуть ошибки латинского текста сцен `options-game-controls` и `options-game-keybind`: правило — пункт 10 (строки `latin-ru-allowed.tsv`), затем скрипт запускается заново до `exit=0`.
   - После проверки — `rm -r tests/ui_audit/__pycache__ tools/ui-audit/__pycache__ tools/ui-audit/tests/__pycache__`, если эти папки появились.
6. **Сверки `git grep --untracked` (в скобках — ожидаемое число строк вывода `-c` по файлу):**
   - в `src/main.cpp`: `Preferences::loadChosenOptions` (1), `Preferences::saveOnExit` (1), `Preferences::loadScales` (0), `Preferences::loadLanguage` (0), `Preferences::save(` (0);
   - в `src/game/cGame_logic.cpp`: `Preferences::loadKeyBindings` (1), `m_gameSettings->m_windowed = m_windowed;` (1);
   - в `src/gamestates/cOptionsState.cpp` и `src/gamestates/cOptionsPages.cpp`: `saveScales` (0), `saveLanguage` (0), `commandBindings` (0);
   - во всём `src/`: `m_commandBindings` (0), `uiaudit::` в `src/gamestates/` (0); `localization::text(` в `src/gamestates/cOptionsPages.cpp` — не меньше 20;
   - в `src/gamestates/cOptionsPages.cpp`: `GAMEPLAY_PAGE_KEYS` (1), `DIAGNOSTICS_PAGE_KEYS` (1), `trySetBinding` (0); в `src/gamestates/cOptionsState.cpp`: `trySetBinding` (1), `MAIN_PAGE_KEYS` (1).
7. `git -c lfs.storage=$PWD/.tmp/p10c/lfs status --short` — изменённые (` M`) пути — только пути шагов 1, 3–7 плана (кроме новых файлов); новые (`??`) — только `src/gamestates/AdvancedOptionsHeaderLayout.hpp`, `src/gamestates/OptionsPageData.hpp`, `src/gamestates/OptionsKeyLabels.hpp`, `src/gamestates/cOptionsPages.cpp`, `tests/controls/test_KeyRebinding.cpp`, `tests/utils/test_OptionPages.cpp`, `tests/utils/test_PreferencesPages.cpp`, `tools/ui-audit/extract_keys.py`, `tools/ui-audit/check_keys.py`, `tools/ui-audit/keys.tsv`, `tools/ui-audit/tests/test_extract_keys.py`, `tools/ui-audit/tests/test_check_keys.py`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P10C-NN` с выводом и стоп. Ожидания существующих тестов (`tests/utils/test_Preferences.cpp`, `tests/utils/test_OptionsMenu.cpp`, `tests/controls/test_cKeyBindings.cpp` и других) и скрипты в `tests/ui_audit/` меняются только так, как назвал пункт 10; `tools/ui-audit/tests/` — только файлы шага 1.

## Сдача

Последнее сообщение — блок `## DONE-P10C | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p10c/progress.md`): строка на каждый шаг плана;
- красный прогон шага 2: строки `.tmp/p10c/red-build.log` с `error` (не больше 30) и вывод красных Python-тестов;
- вывод каждой проверки 1–7 с кодами выхода (не больше 40 строк на проверку); число `<K>` и число `<F>` проверки 4; строки `ctest.log` с `P10C `;
- `git diff --stat` и список для коммитов:
  1. тесты: файлы шага 1;
  2. код ключей и предпочтений: файлы шагов 3 и 4;
  3. страницы настроек: файлы шага 5;
  4. режим отладки интерфейса: файлы шага 6;
  5. опись клавиш: файлы шага 7.

  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …` (названо: `preferences.ini` читается при каждом запуске по 21 ключу; выход из игры больше не пишет эти 21 ключ; `Alt+Enter` и аргументы командной строки не меняют эти ключи; `[KEYS]` из `preferences.ini` накладывается на `settings.ini`; `Preferences::saveScales` и `saveLanguage` сохраняют остальные разделы файла; новые сеттеры `cGameSettings`);
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p10c --size`; у `.tmp/p10c` пометка `оставить — логи проверок нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаг 1 (помощник A), шаги 3 и 4 (помощник B), шаги 5 и 6 (помощник C) — одновременно; помощники B и C не создают новые заголовки и не пишут код, который их вызывает, пока помощник A не записал в журнал хода строку о конце шага 2 (B и C до этого читают файлы и готовят правки без записи в рамку правок).
  4. Шаг 2 (помощник A) — сразу после шага 1.
  5. Шаг 7 (помощник A) — после шагов 3–6.
  6. Шаг 8 (помощник A) — после шага 7.
  7. Сдача и стоп.
- **Параллельно:** шаги 1, 3–4 и 5–6 правят разные файлы; общие у них только имена функций и заголовков из контракта. Собирает их вместе проверка 1 шага 8. Файлы с наибольшим риском конфликта с параллельным шагом П8а — `tests/CMakeLists.txt`, `src/CMakeLists.txt`, `src/debug/UiAuditScenes.cpp`, `src/game/cGame_logic.cpp`: правки в них только после названных якорей.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных. Ожидаемое время: помощник A — 60 минут на шаги 1–2, 60 минут на шаг 7 и 60 минут на шаг 8; помощник B — 60 минут; помощник C — 120 минут на шаги 5–6.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено» и «Контракт поведения»; его шаги плана; раздел «Тесты» и раздел «Проверки» — помощнику A; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p10c/`.
  - Корневая нить раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Данные LFS:** шаг не берёт картинок и звука из форка.
- **Остановки:** только на `## DONE-P10C` и на блоках `## Q-P10C-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P10C-NN` и стоп.
- **Рамка правок:** файлы шагов 1, 3, 4, 5, 6, 7 плана и папка `.tmp/p10c/`. Понадобился другой файл — блок `## Q-P10C-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` и временные папки скриптов; это не правка.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=a9bda9c6318255670aecab75810e663ed3ef91095a214b541ff20d2adede49dd -->
## Обязательно: правила исполнителя

«Ведущий» в этих правилах — тот, кто ведёт твою задачу: он дал задание и принимает сдачу.

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Фоновые команды. Среда сама будит тебя, когда фоновая команда кончилась (сессия Claude: запуск с `run_in_background`), — долгий прогон запускай в фоне и делай тем временем то, что от него не зависит. Среда не будит (нить Codex) — фоновых команд нет: после остановки исполнителя никто его не разбудит; длинные прогоны — в переднем плане, с таймаутом до 30 минут. Ожидание циклом (`while …; sleep`) запрещено в обоих случаях.
- Git по договорённости с ведущим. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ведущий после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ведущего.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не останавливать и не менять (пользоваться ими как клиент можно), секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. В репозиторий и в корень рабочей копии ничего временного не клади. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. Удалять что-либо вне своей `tmp` — только по разделу «Уборка».
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- Субагенту, которого запускаешь, назначь ожидаемое время работы и запиши его в журнал хода. Время вышло, а итога нет — проверь, как он идёт: скриптом по его журналу или списком агентов среды, а не ожиданием. Стоит или ушёл в сторону — останови и перезапусти с более узкой задачей.
- **Чтение.** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по транскрипту: обрезанный вывод — не чтение.
- **Цель нити (исполнитель Codex).** Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; субагентам цель не ставить.
- **Строка хода (исполнитель Codex).** После чтения до работы и после каждого закрытого пункта задания или плана ведущего — отдельной строкой ответа: `ХОД: [x] <пункт>; [>] <пункт>; [ ] <пункт>`. В строке все пункты по порядку: `[x]` — сделан, `[>]` — в работе, `[ ]` — впереди. По этой строке панель ведущего и владельца показывает план и ход. Исполнитель в сессии Claude строку хода не пишет.
- **Сжатие контекста (исполнитель в сессии Claude).** На границе своих частей — часть закрыта, журнал хода обновлён — сам вызови `request_compact` и закончи ход. В `instructions`: задание, текущая часть и следующий шаг, id фоновых задач и сессий, пути, решения, открытые вопросы и строка «после сжатия перечитай раздел правил в задании». Посреди части не сжимай. После сжатия перечитай задание и журнал хода.

## Вопросы и остановки

Каждое препятствие сверяй в таком порядке:

1. Подходит под список «`Q` и стоп» — `Q` и стоп, даже если оно подходит и под список «Без вопроса».
2. Иначе подходит под список «Без вопроса» — решай сам и работай дальше.
3. Иначе: без ответа идущий подпункт выполнить нельзя — `Q` и стоп; можно — неблокирующий вопрос: запиши его в сдачу и работай дальше по списку, не простаивай.

`Q` в любом другом пункте этих правил — тоже «`Q` и стоп».

**`Q` и стоп.**
- ответ требует правки вне рамки правок, правки промптов, норм, governance, контрактов или замороженных тестов (файл, assert, смысл проверки);
- удаление данных, сеть или установка пакетов;
- смена цели, рамки или критерия готовности; новый механизм; решение по продукту;
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в сдаче;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса.** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи, журнала хода и того, что прямо называет задание, не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- **Общее, а не частное.** Код и поведение — универсальные и масштабируемые: одна логика и одни правила для всего продукта, в любом месте и с любыми сущностями и предметами, а не под конкретное место, персонажа или вещь; частное задают данные. Проблему чинить системно, в общем механизме, а не отдельным исключением для найденного случая.
- **Комментарии в коде.** Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий; исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи из списка — строго по порядку; независимые части одной задачи идут параллельно, как велит её раздел «Организация работы».
- Замечания ведущего выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения.
- Если исполнитель коммитит — незаконченное хранить в своей ветке WIP-коммитом, а не патчами во временной папке. Голый `git stash` не использовать: список stash общий для всех рабочих копий и сессий.
- Перенос и переформатирование кода — отдельным коммитом, изменение поведения — следующим. «Без изменения поведения» писать, только если это правда.
- Последняя строка сообщения коммита — `Behavior changes: …` со списком или `Behavior changes: none`. Называть и мелочи: запасной вариант, удалённое поле, удалённую настройку в тесте, изменённый предел.
- Заголовок не преувеличивает: «finish», «complete» — только если пункт закрыт целиком; остатки назвать в теле.

## Тесты

- Тест проходит путь пользователя через тот вход продукта, которым пользуется пользователь в сценарии: для интерфейса — события мыши и клавиатуры, для API — вызов API. Тестируемый код не подменять заглушками.
- Тест проверяет поведение, а не совпадение хэша или вывода с прошлой сборкой. Изображения сравнивать с эталоном с допуском из задания, а если в задании его нет — из действующего эталонного теста или конфигурации сравнения; ни один источник допуск не задаёт — `Q`.
- Асинхронный результат ждать по нему самому (нужное значение, запись, пиксель), а не по косвенному флагу.
- Нестабильный тест разбирать сразу, с логом и санитайзером, если он уже настроен в проекте. «Не воспроизвелось» проблему не закрывает: исполнитель перечисляет её в сдаче с логом, issue заводит ведущий.
- Тесты пишут только в свои временные папки; общее состояние (синглтоны, кэши) сбрасывать перед каждым тестом.
- Общие помощники тестов и константы — в одном месте, не копировать по файлам.
- В целевую ветку сливают только ветку с зелёным CI на её последнем коммите; кто сливает (обычно ведущий), тот после слияния проверяет CI целевой ветки и красной её не оставляет.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Сдача

Сдача — блок `## DONE-<id> | время | HEAD <sha>`, один на задачу; после возврата `REVIEW` — новая сдача. В ней:

- журнал хода без изменений (строка на подпункт: что сделано, коммит, тест) и строки вывода проверок — красный до правки, зелёный после; отдельной таблицы нет;
- числа только из логов, а не из памяти;
- свои вызовы и вызовы субагентов — числами скрипта по транскрипту: Claude — `tools/usage-daily.py <папка> --session <id>`, Codex — `tools/codex-watch.py`;
- раздел «не проверено» — обязателен; пустым без пояснения не бывает;
- раздел «Рабочие места» — по разделу «Уборка»;
- находки вне задачи — списком; issue заводит ведущий;
- `git status --short`;
- три пункта для владельца простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Отдельного отчёта владельцу не создавать.

## Уборка

- В сдаче — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер (`du -sh`), назначение и пометка: `удалить` или `оставить — <почему>`. Назначение — доказательство (на него ссылаются сдача, PR или журнал) или промежуточное; доказательства — только `оставить`.
- Удаляешь только после ответа ведущего `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Объекты сборки, ненужные для повторной проверки, — тоже только после `CLEAN-OK`.
- Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`.
- Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.

<!-- /team-process:executor-rules -->
