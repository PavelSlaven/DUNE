# Задание P10A — панель приказов, клавиши приказов, режимы приказов мыши (шаг П10, часть а)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p10`, ветка `codex/p10`, `HEAD` — `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6` (вершина ветки порта `port/up-d06f2fcd`). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p10a/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p10a/` (дальше — «папка задания»).

## Цель

В бою под полем боя, у левого края, есть панель из семи кнопок приказов: «Переместить», «Атаковать», «Ремонт», «Разгрузить», «Развернуть», «Точка сбора», «Выпустить» (в английской игре — Move, Attack, Repair, Unload, Deploy, Rally, Release). Кнопка светлая, когда приказ доступен выбору игрока, и тёмная, когда недоступен; на светлой кнопке подписана клавиша приказа из настроек клавиш игры. Щелчок по светлой кнопке даёт приказ: движение, атаку, режим ремонта, разгрузку харвестера, развёртывание MCV, режим точки сбора, выпуск юнита из ремонтного центра. Щелчки и колесо мыши над панелью не доходят до карты. В режимах «принудительная атака», «точка сбора» и «ремонт» правая кнопка мыши отменяет режим, а принудительная атака не сбрасывается движением мыши. Флаги щелчков мыши после создания равны `false`. Уведомления в бою стоят над панелью, а не на ней. Готово, когда новые тесты Catch2, сборка со всеми тестами, скрипты режима отладки интерфейса и тесты скриптов `tools/ui-audit/tests` зелёные, а три новые сцены режима отладки показывают панель.

Не входит в этот шаг: страницы настроек, переназначение клавиш и опись клавиш режима отладки (`extract_keys.py`, `check_keys.py`, `keys.tsv` — шаг П10в), очередь Starport (часть П10б, задание `P10B`), предел юнитов апстрима (не меняется), музыкальный блок и сохранения (шаги П9 и П8).

## Что уже решено

Ревизия `B` = `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6` (дерево равно `a1e63b860482d7e7a82e502359965e2caefd6470`), ревизия форка `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`. Все факты о коде порта ниже — о файлах ревизии `B`; номера строк `FORK1` — той ревизии.

- **Источник вида и поведения** — форк (`FORK1`): `src/drawers/cCommandBarDrawer.h` (69 строк) и `.cpp` (363), `src/drawers/CommandBarLayout.hpp` (44), `src/drawers/CommandBarPolicy.hpp` (40), `src/controls/CommandModePolicy.hpp` (36). Класса `CommandBindings` форка в порту нет: клавиши приказов — действия `eKeyAction` таблицы `cKeyBindings` апстрима. Умолчания порта равны умолчаниям форка и не меняются.
- **Соответствие кнопок и действий порта.**

  | Кнопка | Действие `eKeyAction` | Где порт уже использует действие |
  |---|---|---|
  | Move | клавиши нет, подпись `LMB`/`ЛКМ` | — |
  | Attack | `ATTACK_MODE` | `cMouseUnitsSelectedState::onKeyDown` |
  | Repair | `REPAIR_UNIT` (в `settings.ini` — ключ `REPAIR`) | `cMouseNormalState::onKeyPressed`, `cMouseRepairState::onNotifyKeyboardEvent` |
  | Unload | `SEND_TO_REFINERY` | `cMouseUnitsSelectedState::onKeyPressed` |
  | Deploy | `DEPLOY_UNIT` | `cGamePlaying::onKeyPressedGamePlaying` (MCV → CONSTYARD) |
  | Rally | `ATTACK_MODE` у выбранной постройки | `cMouseNormalState::onKeyDown` (условие `canHaveRallyPoint()`) |
  | Release | `DEPLOY_UNIT` у выбранного ремонтного центра | `cGamePlaying::onKeyPressedGamePlaying` (событие `GAME_EVENT_DEPLOY_UNIT`) |

- **Подпись клавиши** берёт `cKeyBindings`: новый метод `getFirstKeyDisplayName(eKeyAction)` отдаёт имя первой назначенной клавиши действия для показа игроку (`Ctrl` для левого и правого Ctrl, `Shift`, `Alt`; иначе имя скан-кода SDL; пустая строка, если у действия нет клавиш). Текстовый рисовальщик клавиш — `ctx->getTextContext()->getSmallTextDrawer()`; нового шрифта нет (Р76).
- **Раскладка панели** — `CommandBarLayout` форка как есть, от `cGameSettings::getScreenW()`, `getScreenH()` и `cSideBar::SidebarWidth` (после `cSideBar::configureLayout` равна `HudLayout::create(...).sidebarWidth`, то есть ширине, на которую `HudLayout::battlefield` меньше экрана). Значения переработки интерфейса (Р72, Р73) не применяются.
- **События мыши.** В порту нет `cInteractionManager`: панель получает событие в `cGamePlaying::onNotifyMouseEvent` после контекста управления и до боковой панели; карта не получает событие, когда мышь над панелью. Клетка мыши над панелью — `cGameControlsContext::MOUSE_CELL_HOVER_COMMAND_BAR = -4` (порт хранит клетки `MOUSE_CELL_HOVER_*` в `cGameControlsContext.h`, а `MOUSECELL_*` в `definitions.h` закомментированы).
- **Тексты** — `localization::text(en, ru)`; русские тексты кнопок взяты из форка. Единственная новая строка — сообщение кнопки «Развернуть» при пределе построек (пункт 7.7).
- **Предел юнитов апстрима** (`cUnits::MAX_UNITS_CAPACITY` и всё, что от него зависит) не меняется; панель юнитов не создаёт.
- **Картинки** `resources/bin/data/hd4/command_bar.png` и `command_bar_disabled.png` кладёт в рабочую копию ведущий до запуска; ты их не меняешь. Картинки `resources/hd/master4/`, эталоны `resources/hd/source_references/command_bar_*_reference.png`, `tools/build_command_bar_asset.py` и `tools/check_command_bar_assets.py` в порт не переносятся: проверка `check_command_bar_assets.py` импортирует `make_disabled` из `build_command_bar_asset.py` (в порту нет его источников) и читает пары картинок из `resources/hd/master4/`.
- **Опись клавиш режима отладки** (`extract_keys.py`, `check_keys.py`, `keys.tsv`, их тесты) в этом шаге не переносится: её собирает шаг П10в после слияния П8 и П9, которые добавляют действия клавиш.
- **Уведомления в бою** — над панелью, как в форке (`FORK1:src/managers/cDrawManager.cpp`, `drawNotifications`: `y = m_commandBarDrawer.getTopY() - 18`); вне боя — на прежнем месте (пункт 12).
- **Параллельные шаги** меняют соседние места общих файлов: П8 — `cKeyBindings`, `settings.ini` (новые действия после `JUMP_TO_VIEWPORT_BOOKMARK_5`); П9 — `cDrawManager` (верхняя панель), `cKeyBindings` (действия после `MUSIC_VOLUME_UP`); П10б — `cOrderProcesser`, `cStarPort`, `cOrderDrawer`, `cBuildingListUpdater`. Эти места задание не трогает; вставки в общие списки — только после названных якорей.

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом:

- `src/controls/cKeyBindings.h` целиком; `src/controls/cKeyBindings.cpp` строки 24–70 и 227–359;
- `src/controls/cKeyboard.h` целиком; `src/controls/cKeyboardEvent.h` целиком;
- `src/controls/cGameControlsContext.h` целиком; `src/controls/cGameControlsContext.cpp` строки 1–135 и 219–300;
- `src/controls/mousestates/cMouseNormalState.cpp` целиком; `src/controls/mousestates/cMouseRepairState.cpp` целиком; `src/controls/mousestates/cMouseUnitsSelectedState.cpp` целиком; `src/controls/mousestates/cMouseNormalState.h` и `cMouseUnitsSelectedState.h` целиком;
- `src/controls/cMouse.h` целиком; `src/controls/cMouse.cpp` строки 1–70;
- `src/gamestates/cGamePlaying.cpp` строки 319–346 и 603–665;
- `src/managers/cDrawManager.cpp` строки 61–177 и 355–396; `src/managers/cDrawManager.h` целиком;
- `src/include/sGameServices.h` целиком; `src/game/cGame_logic.cpp` строки 1–60, 548–570 и 745–790;
- `src/debug/UiAudit.hpp` целиком; `src/debug/UiAuditAccess.cpp` строки 296–340 и 596–760; `src/debug/UiAuditScenes.cpp` строки 296–312 и 452–490;
- `tests/CMakeLists.txt` строки 1–80; `tests/controls/test_cKeyBindings.cpp` строки 1–80; `tests/ui_audit/ui_audit_part3b_catalog.py` целиком; `tests/ui_audit/ui_audit_part3b_scenes.py` целиком; `tests/ui_audit/data/latin-ru-allowed.tsv` целиком;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>` для каждого файла форка: `src/drawers/cCommandBarDrawer.h`, `src/drawers/cCommandBarDrawer.cpp`, `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp`, `src/controls/CommandModePolicy.hpp`, `tests/CommandBindingsTests.cpp`, `tests/CommandBarLayoutTests.cpp`, `tests/MouseClickInitTests.cpp`, `tests/InteractionRegressionTests.cpp`;
- вывод `git diff e17379a 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/controls/mousestates/cMouseNormalState.cpp src/controls/mousestates/cMouseRepairState.cpp src/controls/mousestates/cMouseUnitsSelectedState.cpp`.

Пути без `/srv/` — от корня рабочей копии. Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт поведения

Каждый пункт называет файл, место и точный новый текст. Правило «Подключение» из пункта 14 применяется ко всем новым строкам `#include`.

### 1. `cKeyBindings`: имя клавиши для показа

- `src/controls/cKeyBindings.h`: сразу после строки `    bool containsActionKey(const std::bitset<SDL_SCANCODE_COUNT> &keys, eKeyAction action) const;` добавляются строки (пустая строка перед комментарием):
  ```cpp

      /**
       * Name of the first key bound to the action, for showing it to the player: "Ctrl", "Shift" and "Alt" for
       * the left and right modifier keys, the SDL scancode name otherwise, empty when the action has no key.
       */
      std::string getFirstKeyDisplayName(eKeyAction action) const;
  ```
- `src/controls/cKeyBindings.cpp`: сразу после закрывающей скобки функции `cKeyBindings::containsActionKey` (перед `void cKeyBindings::bind(`) добавляются строки, пустая строка перед ними и после них:
  ```cpp
  std::string cKeyBindings::getFirstKeyDisplayName(eKeyAction action) const
  {
      auto it = m_bindings.find(action);
      if (it == m_bindings.end() || it->second.keys.empty()) return "";

      const SDL_Scancode first = it->second.keys.front();
      switch (first) {
          case SDL_SCANCODE_LCTRL:
          case SDL_SCANCODE_RCTRL:
              return "Ctrl";
          case SDL_SCANCODE_LSHIFT:
          case SDL_SCANCODE_RSHIFT:
              return "Shift";
          case SDL_SCANCODE_LALT:
          case SDL_SCANCODE_RALT:
              return "Alt";
          default:
              break;
      }
      const char *name = SDL_GetScancodeName(first);
      return name != nullptr ? name : "";
  }
  ```
- Таблица умолчаний, разбор `[KEYS]` и проверка совпадений `checkForClashes` не меняются.

### 2. Доступ рисовальщика к назначениям клавиш

- `src/controls/cKeyboard.h`: сразу после строки `    void loadKeyBindings(const cSection *section = nullptr);` добавляются строки: пустая строка и `    [[nodiscard]] const cKeyBindings *getKeyBindings() const { return m_keyBindings.get(); }`.
- `src/include/sGameServices.h`: после строки `class cMouse;` — строка `class cKeyboard;`; после строки `    cMouse *mouse = nullptr;` — строка `    cKeyboard *keyboard = nullptr;`.
- `src/game/cGame_logic.cpp`, `cGame::setupGame`: сразу после строки `    Logger::info(COMP_INIT, "Initializing Key Bindings", "Loaded from [KEYS] section");` — строка `    m_services->keyboard = m_keyboard.get();`.

### 3. Заголовки политик и раскладки (новые файлы)

Каждый файл — копия файла форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь> > <путь>`.

- `src/controls/CommandModePolicy.hpp`;
- `src/drawers/CommandBarLayout.hpp`;
- `src/drawers/CommandBarPolicy.hpp`.

Правок в этих файлах нет. Заголовки не добавляются в `src/CMakeLists.txt` и `TEST_SOURCES`: у них нет файлов `.cpp`.

### 4. Флаги щелчков мыши

`src/controls/cMouse.h`: строки `    bool m_leftButtonClicked;` и `    bool m_rightButtonClicked;` становятся `    bool m_leftButtonClicked = false;` и `    bool m_rightButtonClicked = false;`. Других правок нет.

### 5. `cGameControlsContext`: клетка мыши над панелью и команды

- `src/controls/cGameControlsContext.h`:
  - после строки `    static constexpr int MOUSE_CELL_HOVER_SIDEBAR = -3;` — строка `    static constexpr int MOUSE_CELL_HOVER_COMMAND_BAR = -4;`;
  - перед строкой `    bool isMouseOnSidebarOrMinimap() const {` — блок (пустая строка после него):
    ```cpp
        bool isMouseOnCommandBar() const {
            return m_mouseCell == MOUSE_CELL_HOVER_COMMAND_BAR;
        }
    ```
  - после строки `    void onFocusMouseStateEvent();` — пустая строка и строки:
    ```cpp
        void activateMoveCommand();
        void activateAttackCommand();
        void activateRallyPointCommand();
    ```
- `src/controls/cGameControlsContext.cpp`:
  - в функции `cGameControlsContext::updateMouseCell` сразу после закрывающей скобки блока `if (coords.y < cSideBar::TopBarHeight) { ... }` и перед блоком `if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {` добавляется блок и пустая строка после него:
    ```cpp
        if (m_drawManager->getCommandBarDrawer()->isMouseOver(coords)) {
            m_mouseCell = MOUSE_CELL_HOVER_COMMAND_BAR;
            m_mouseOnBattleField = false;
            return;
        }
    ```
  - после функции `cGameControlsContext::updateMouseCell` (перед `int cGameControlsContext::getMouseCellFromScreen(`) добавляются три функции из `FORK1:src/controls/cGameControlsContext.cpp` строки 75–95 (`activateMoveCommand`, `activateAttackCommand`, `activateRallyPointCommand`) по правилам переноса. Единственное отличие от форка: в `activateRallyPointCommand` условие `canSpawnUnits()` заменяется на `canHaveRallyPoint()` — так же, как условие точки сбора в `cMouseNormalState::onKeyDown` порта;
  - подключения: `drawers/cCommandBarDrawer.h`, `gameobjects/players/cPlayer.h`.
- Функций `isMouseOnInterface` и `refreshMouseHover` форка в порт не переносится: ни один шаг П10 их не вызывает.

### 6. Режимы мыши

- `src/controls/mousestates/cMouseNormalState.h`: после строки `    void onBlur() override;` — пустая строка и строка `    void setRallyPointCommandMode();`.
- `src/controls/mousestates/cMouseNormalState.cpp`:
  - подключение `controls/CommandModePolicy.hpp`;
  - `cMouseNormalState::onMouseRightButtonClicked` — первой в теле (перед `if (!m_mouse->isMapScrolling()) {`) добавляется блок; остальные строки функции не меняются:
    ```cpp
        if (rightClickCommandPolicy(
                m_state == SELECT_STATE_RALLY
                    ? ActiveCommandMode::Rally
                    : ActiveCommandMode::Normal
            ) == RightClickCommandPolicy::CancelCommand) {
            setState(SELECT_STATE_NORMAL);
            m_mouseTile = MOUSE_NORMAL;
            m_mouse->resetDragViewportInteraction();
            return;
        }
    ```
  - в конец файла добавляется функция:
    ```cpp
    void cMouseNormalState::setRallyPointCommandMode()
    {
        setState(SELECT_STATE_RALLY);
        m_mouseTile = MOUSE_RALLY;
        m_mouse->setTile(m_mouseTile);
    }
    ```
- `src/controls/mousestates/cMouseRepairState.cpp`: подключение `controls/CommandModePolicy.hpp`; условие `    if (!m_mouse->isMapScrolling()) {` в `cMouseRepairState::onMouseRightButtonClicked` становится:
  ```cpp
      if (!m_mouse->isMapScrolling() &&
          rightClickCommandPolicy(ActiveCommandMode::Repair) ==
              RightClickCommandPolicy::CancelCommand) {
  ```
- `src/controls/mousestates/cMouseUnitsSelectedState.h`: после строки `    void selectSameUnitsOnMap(int iType);` — строка `    void setCommandState(eMouseUnitsSelectedState newState);`.
- `src/controls/mousestates/cMouseUnitsSelectedState.cpp`:
  - подключение `controls/CommandModePolicy.hpp`;
  - `cMouseUnitsSelectedState::onMouseRightButtonClicked` — первым в теле (перед комментарием `// if we were dragging the viewport, keep the units and this state.`) добавляется блок:
    ```cpp
        if (rightClickCommandPolicy(
                m_state == SELECTED_STATE_FORCE_ATTACK
                    ? ActiveCommandMode::ForceAttack
                    : ActiveCommandMode::Normal
            ) == RightClickCommandPolicy::CancelCommand) {
            setState(SELECTED_STATE_MOVE);
            m_mouseTile = MOUSE_MOVE;
            m_mouse->resetDragViewportInteraction();
            return;
        }
    ```
  - `cMouseUnitsSelectedState::onMouseMovedTo`: строка `    else {` перед вызовом `evaluateMouseMoveState();` (вторая ветка после `if (m_state == SELECTED_STATE_ADD_TO_SELECTION) {`) становится:
    ```cpp
        else if (pointerMoveCommandPolicy(
                     m_state == SELECTED_STATE_FORCE_ATTACK
                         ? ActiveCommandMode::ForceAttack
                         : ActiveCommandMode::Normal
                 ) == PointerMoveCommandPolicy::Reevaluate) {
    ```
    тело ветки (`evaluateMouseMoveState();`) не меняется;
  - в конец файла добавляется функция:
    ```cpp
    void cMouseUnitsSelectedState::setCommandState(eMouseUnitsSelectedState newState)
    {
        setState(newState);
        switch (newState) {
            case SELECTED_STATE_ATTACK:
            case SELECTED_STATE_FORCE_ATTACK:
                m_mouseTile = MOUSE_ATTACK;
                break;
            case SELECTED_STATE_REPAIR:
                m_mouseTile = MOUSE_REPAIR;
                break;
            default:
                m_mouseTile = MOUSE_MOVE;
                break;
        }
        m_mouse->setTile(m_mouseTile);
    }
    ```
- Остальной код режимов (клавиши через `isAction`, левый щелчок, выбор постройки) не меняется.

### 7. Панель приказов `cCommandBarDrawer` (новые файлы)

`src/drawers/cCommandBarDrawer.h` — файл с ровно таким содержимым:

```cpp
#pragma once

#include "controls/eKeyAction.h"
#include "controls/sMouseEvent.h"
#include "utils/Color.hpp"
#include "utils/cPoint.h"
#include "utils/cRectangle.h"

#include <string>
#include <vector>

class cEventEmitter;
class cGameObjectContext;
class cGameSettings;
class cKeyboard;
class cPlayer;
class cTextDrawer;
class GameContext;
class SDLDrawer;
class Texture;
struct sGameServices;

class cCommandBarDrawer {
    friend class UiAuditAccess;
public:
    explicit cCommandBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services);
    ~cCommandBarDrawer();

    void draw();
    void onNotifyMouseEvent(const s_MouseEvent &event);
    void setPlayer(cPlayer *player);

    [[nodiscard]] bool isMouseOver(const cPoint &point) const;

private:
    enum class Command {
        Move,
        Attack,
        Repair,
        Unload,
        Deploy,
        Rally,
        Release
    };

    struct Button {
        Command command;
        cRectangle rect;
        std::string label;
        std::string hotkey;
        bool enabled;
        bool active;
    };

    void rebuildLayout();
    void drawButton(const Button &button) const;
    void drawIcon(Command command, const cRectangle &rect, Color color) const;
    void execute(Command command);
    void executeUnload();
    void executeDeploy();
    void executeRelease();

    [[nodiscard]] bool hasAttackCapableUnit() const;
    [[nodiscard]] bool hasUnloadableHarvester() const;
    [[nodiscard]] bool hasSelectedMcv() const;
    [[nodiscard]] std::string getKeyLabel(eKeyAction action) const;

    GameContext *m_ctx;
    cPlayer *m_player;
    SDLDrawer *m_sdlDrawer;
    cGameSettings *m_settings;
    cGameObjectContext *m_objects;
    cEventEmitter *m_eventEmitter;
    cKeyboard *m_keyboard;
    cTextDrawer *m_keyTextDrawer;
    Texture *m_commandBarTexture;
    Texture *m_disabledCommandBarTexture;
    cRectangle m_panelRect;
    std::vector<Button> m_buttons;
    int m_hoveredButton;
};
```

`src/drawers/cCommandBarDrawer.cpp` — `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp > src/drawers/cCommandBarDrawer.cpp`, затем правки 7.1–7.9 в таком порядке. Тела функций форка, которых правки не называют, переносятся по правилам переноса (раздел ниже) и по смыслу не меняются.

- **7.1. Подключения.** Блок строк `#include` форка (строки 1–19) заменяется блоком (в этом порядке):
  ```cpp
  #include "cCommandBarDrawer.h"

  #include "context/GameContext.hpp"
  #include "context/TextContext.hpp"
  #include "context/cGameObjectContext.h"
  #include "controls/cGameControlsContext.h"
  #include "controls/cKeyBindings.h"
  #include "controls/cKeyboard.h"
  #include "debug/UiAudit.hpp"
  #include "drawers/CommandBarLayout.hpp"
  #include "drawers/CommandBarPolicy.hpp"
  #include "drawers/SDLDrawer.hpp"
  #include "drawers/cTextDrawer.h"
  #include "game/cEventEmitter.h"
  #include "game/cGameSettings.h"
  #include "gameobjects/players/cPlayer.h"
  #include "gameobjects/structures/cAbstractStructure.h"
  #include "gameobjects/structures/cStructureFactory.h"
  #include "gameobjects/units/cUnit.h"
  #include "include/Texture.hpp"
  #include "include/cAssert.h"
  #include "include/definitions.h"
  #include "include/sGameEvent.h"
  #include "include/sGameServices.h"
  #include "sidebar/cSideBar.h"
  #include "utils/HdUiTextureLoader.hpp"
  #include "utils/Localization.hpp"

  #include <algorithm>
  #include <array>
  #include <cctype>
  ```
  Недостающий для компиляции заголовок порта добавляется в этот блок строкой в алфавитном порядке; каждая такая строка — запись «Решено исполнителем».
- **7.2. Анонимное пространство имён** (функции цветов `panelColor`, `panelBorder`, `brass`, `disabledText`, `blueFilter`) — без изменений.
- **7.3. Конструктор** заменяется:
  ```cpp
  cCommandBarDrawer::cCommandBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services) :
      m_ctx(ctx),
      m_player(player),
      m_sdlDrawer(ctx->getSDLDrawer()),
      m_settings(services->settings),
      m_objects(services->objects),
      m_eventEmitter(services->eventEmitter),
      m_keyboard(services->keyboard),
      m_keyTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
      m_commandBarTexture(nullptr),
      m_disabledCommandBarTexture(nullptr),
      m_panelRect(),
      m_buttons(),
      m_hoveredButton(-1)
  {
      d2tm_assert(m_player != nullptr);
      d2tm_assert(m_sdlDrawer != nullptr);
      d2tm_assert(m_settings != nullptr);
      d2tm_assert(m_objects != nullptr);
      d2tm_assert(m_eventEmitter != nullptr);
      d2tm_assert(m_keyboard != nullptr);
      d2tm_assert(m_keyTextDrawer != nullptr);

      m_commandBarTexture = loadHdUiTexture(
          m_sdlDrawer->getRenderer(),
          "command_bar.png",
          "HD command bar"
      );
      m_disabledCommandBarTexture = loadHdUiTexture(
          m_sdlDrawer->getRenderer(),
          "command_bar_disabled.png",
          "disabled HD command bar"
      );
      rebuildLayout();
  }
  ```
  Деструктор, `setPlayer`, `isMouseOver` — как в форке. Функция `getTopY` не переносится.
- **7.4. `rebuildLayout`.** Первая строка `const CommandBarLayout layout = ...` — `const CommandBarLayout layout = CommandBarLayout::create(m_settings->getScreenW(), m_settings->getScreenH(), cSideBar::SidebarWidth);`. Массив `actions` заменяется:
  ```cpp
      const std::array<Button, CommandBarLayout::ActionCount> actions{{
          {Command::Move, layout.actions[0], localization::text("Move", "Переместить"), localization::text("LMB", "ЛКМ"), isMoveCommandEnabled(!selectedUnits.empty()), false},
          {Command::Attack, layout.actions[1], localization::text("Attack", "Атаковать"), getKeyLabel(eKeyAction::ATTACK_MODE), isAttackCommandEnabled(hasAttackCapableUnit()), false},
          {Command::Repair, layout.actions[2], localization::text("Repair", "Ремонт"), getKeyLabel(eKeyAction::REPAIR_UNIT), isRepairCommandEnabled(), false},
          {Command::Unload, layout.actions[3], localization::text("Unload", "Разгрузить"), getKeyLabel(eKeyAction::SEND_TO_REFINERY), isUnloadCommandEnabled(hasUnloadableHarvester()), false},
          {Command::Deploy, layout.actions[4], localization::text("Deploy", "Развернуть"), getKeyLabel(eKeyAction::DEPLOY_UNIT), isDeployCommandEnabled(hasSelectedMcv()), false},
          {Command::Rally, layout.actions[5], localization::text("Rally", "Точка сбора"), getKeyLabel(eKeyAction::ATTACK_MODE), isRallyCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->canHaveRallyPoint()), false},
          {Command::Release, layout.actions[6], localization::text("Release", "Выпустить"), getKeyLabel(eKeyAction::DEPLOY_UNIT), isReleaseCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->getType() == REPAIR), false}
      }};
  ```
  Остальные строки функции — как в форке.
- **7.5. `draw`, `drawButton`, `drawIcon`, `onNotifyMouseEvent`, `execute`** — как в форке по правилам переноса. В `draw` строки `if (uiaudit::isEnabled()) { uiaudit::recordArea("command-bar", ...); UiAuditAccess::recordCommandBarClicks(*this); }` остаются.
- **7.6. `executeUnload`, `hasAttackCapableUnit`, `hasUnloadableHarvester`, `hasSelectedMcv`** — тела форка, в которых обращение к юниту `unit[id]` заменено на указатель `m_objects->getUnit(id)` (в лямбдах — с захватом `this`), точки `.` на юнитах — стрелками `->`.
- **7.7. `executeDeploy`** заменяется:
  ```cpp
  void cCommandBarDrawer::executeDeploy()
  {
      for (int id : m_player->getSelectedUnits()) {
          cUnit *selected = m_objects->getUnit(id);
          if (!selected->isValid() || selected->getType() != MCV || !selected->belongsTo(m_player)) continue;
          if (!m_player->canPlaceStructureAt(selected->getCell(), CONSTYARD, selected->iID).success) continue;
          // at the structure cap the Construction Yard can't be created; keep the MCV
          if (m_objects->getStructureFactory()->getFreeSlot() < 0) {
              m_eventEmitter->emit(s_GameEvent{
                  .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
                  .data = NotificationEvent{
                      .message = localization::text("Cannot deploy: maximum number of structures reached.",
                                                    "Нельзя развернуть: достигнут предел построек."),
                      .type = eNotificationType::BAD,
                  }
              });
              return;
          }
          const int cell = selected->getCell();
          selected->die(false, false);
          m_player->placeStructure(cell, CONSTYARD, 100);
          return;
      }
  }
  ```
- **7.8. `executeRelease`** заменяется:
  ```cpp
  void cCommandBarDrawer::executeRelease()
  {
      cAbstractStructure *selected = m_player->getSelectedStructure();
      if (!selected || selected->getType() != REPAIR) return;
      s_GameEvent event{
          .eventType = eGameEventType::GAME_EVENT_DEPLOY_UNIT,
          .data = CommonEvent{
              .entityType = eBuildType::UNKNOWN,
              .player = m_player
          }
      };
      selected->onNotifyGameEvent(event);
  }
  ```
- **7.9. `getKeyLabel`** — новая функция в конце файла:
  ```cpp
  std::string cCommandBarDrawer::getKeyLabel(eKeyAction action) const
  {
      const cKeyBindings *bindings = m_keyboard->getKeyBindings();
      std::string name = bindings != nullptr ? bindings->getFirstKeyDisplayName(action) : std::string();
      std::ranges::transform(name, name.begin(), [](unsigned char character) {
          return static_cast<char>(std::toupper(character));
      });
      return name;
  }
  ```
- Правка `src/CMakeLists.txt`: сразу после строки `    drawers/cOrderDrawer.cpp` — строка `    drawers/cCommandBarDrawer.cpp`.

### 8. `cDrawManager`: член панели и рисование

- `src/managers/cDrawManager.h`: после строки `class cBuildingListDrawer;` — строка `class cCommandBarDrawer;`; после блока функции `getOrderDrawer` (после его закрывающей `}` и пустой строки) — блок
  ```cpp
      cCommandBarDrawer *getCommandBarDrawer() {
          return m_commandBarDrawer.get();
      }

  ```
  после строки `    std::unique_ptr<cOrderDrawer> m_orderDrawer;` — строка `    std::unique_ptr<cCommandBarDrawer> m_commandBarDrawer;`.
- `src/managers/cDrawManager.cpp`:
  - подключение `drawers/cCommandBarDrawer.h`;
  - в `cDrawManager::reset` сразу после строки `    m_orderDrawer = std::make_unique<cOrderDrawer>(m_ctx, m_player, m_services);` — строка `    m_commandBarDrawer = std::make_unique<cCommandBarDrawer>(m_ctx, m_player, m_services);`;
  - в `cDrawManager::drawCombatState` перед парой строк `    m_sdlDrawer->resetClippingFor();` + пустая строка + `    if (m_gameSettings->isDrawUsages()) {` (последний `resetClippingFor` функции) вставляются строки `    m_commandBarDrawer->draw();` и пустая строка;
  - в `cDrawManager::setPlayerToDraw` сразу после строки `    m_sidebarDrawer->setPlayer(playerToDraw);` — строка `    m_commandBarDrawer->setPlayer(playerToDraw);`.
  - `cDrawManager::onNotifyMouseEvent` не меняется: панель получает событие из `cGamePlaying` (пункт 9).

### 9. `cGamePlaying`: события мыши

`src/gamestates/cGamePlaying.cpp`, подключение `drawers/cCommandBarDrawer.h`; в `cGamePlaying::onNotifyMouseEvent`:
- сразу после строки `    pContext->onNotifyMouseEvent(event); // must be first because other classes rely on this context` и пустой строки — строка `    m_drawManager->getCommandBarDrawer()->onNotifyMouseEvent(event);` и пустая строка;
- условие `    if (!isWheelEvent || !pContext->isMouseOnSidebarOrMinimap()) {` становится `    if ((!isWheelEvent || !pContext->isMouseOnSidebarOrMinimap()) && !pContext->isMouseOnCommandBar()) {`.
Порядок вызовов остаётся: контекст управления, панель приказов, боковая панель, камера, мини-карта, `cOrderDrawer`, `cItemBuilder`.

### 10. Режим отладки интерфейса: сцены, область и записи щелчков

- `src/debug/UiAudit.hpp`: после строки `class cSideBarDrawer;` — строка `class cCommandBarDrawer;`; в перечислении `GameKind` строка `    Rally` становится `    Rally,` и после неё добавляются строки `    DamagedUnit,`, `    Harvester,`, `    Mcv`; после строки `    static void recordSidebarClicks(cSideBarDrawer &drawer);` — строка `    static void recordCommandBarClicks(cCommandBarDrawer &drawer);`.
- `src/debug/UiAuditAccess.cpp`:
  - подключение `drawers/cCommandBarDrawer.h`;
  - функция `UiAuditAccess::recordCommandBarClicks` — из `FORK1:src/debug/UiAuditAccess.cpp` строки 401–410, вставляется перед функцией `void UiAuditAccess::missionOutcome(cGame &currentGame, bool victory)` и отделяется от неё пустой строкой;
  - в анонимном пространстве имён: `buildBase` получает параметр `float tankHp` — `bool buildBase(cGame &currentGame, cEventEmitter *events, bool withRadar, float tankHp, BaseResult &result)`, строка `result.tankId = spawnUnit(currentGame, events, TANK, 25, kStreetRow, 1.0f);` становится `result.tankId = spawnUnit(currentGame, events, TANK, 25, kStreetRow, tankHp);`; вызов в `prepareGameScreen` — `buildBase(currentGame, currentGame.m_eventEmitter.get(), withRadar, kind == GameKind::DamagedUnit ? 0.4f : 1.0f, base)`;
  - перед функцией `listForKind` добавляется функция и пустая строка после неё:
    ```cpp
    void selectOnly(cGame &currentGame, int unitId)
    {
        cPlayer *player = currentGame.m_gameObjectsContext->getPlayer(HUMAN);
        player->deselectAllUnits();
        player->selectUnits({unitId});
    }
    ```
  - в `prepareGameScreen` после блока `case GameKind::Rally:` (после его строки `return currentGame.m_gameObjectsContext->getStructures()[base.factoryId]->getRallyPoint() >= 0;`) добавляются блоки:
    ```cpp
            case GameKind::DamagedUnit:
                selectOnly(currentGame, base.tankId);
                return true;
            case GameKind::Harvester:
                selectOnly(currentGame, base.harvesterId);
                return true;
            case GameKind::Mcv:
                selectOnly(currentGame, base.mcvId);
                return true;
    ```
- `src/debug/UiAuditScenes.cpp`: сразу после строки сцены `"game-rally-point"` добавляются три строки:
  ```cpp
      onGameScreen(scene("game-command-damaged-unit", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::DamagedUnit>), false),
      onGameScreen(scene("game-command-harvester", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Harvester>), false),
      onGameScreen(scene("game-command-mcv", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Mcv>), false),
  ```
- Область `command-bar` и записи щелчков `command:<подпись>` пишет `cCommandBarDrawer::draw` (пункт 7.5); других мест записи нет.

### 11. Скрипты режима отладки интерфейса и данные переводов

Перечень сцен `game-*` проверяет `tests/ui_audit/ui_audit_part3b_catalog.py` (все `game-*` сцены, `EXPECTED_COUNT`), каждую — `ui_audit_part3b_scenes.py`; перевод — `ui_audit_translation.py` по `tests/ui_audit/data/latin-ru-allowed.tsv`. Три новые сцены и подписи клавиш `CTRL`, `R`, `D` требуют правки этих файлов; правка — расширение перечня, а не изменение прежних ожиданий.

- `tests/ui_audit/ui_audit_part3b_catalog.py`: кортеж `BASE_SCENES` — после элемента `"game-rally-point"` добавляются элементы `"game-command-damaged-unit", "game-command-harvester", "game-command-mcv"`; `EXPECTED_COUNT = 35` становится `EXPECTED_COUNT = 38`.
- `tests/ui_audit/ui_audit_part3b_scenes.py`:
  - после строки `BUILD_ITEM = "build-item:"` — строка `COMMAND_CLICK = "command:"` и строка `COMMAND_BUTTONS = 3`;
  - перед функцией `check_for` добавляется функция:
    ```python
    def check_command_bar(scene_id, header, body, bodies):
        panel, error = base.one_record(body, "area", "n", "command-bar")
        if error:
            return error
        commands = [record for record in base.records_of(body, "click") if record["name"].startswith(COMMAND_CLICK)]
        outside = [record for record in commands if not base.inside(record, panel)]
        return base.first_error(
            None if visible(panel) else f"the area record command-bar must have w > 0 and h > 0: {panel}",
            None if len(commands) == COMMAND_BUTTONS
            else f"expected {COMMAND_BUTTONS} click records {COMMAND_CLICK}<name>, got {commands}",
            f"command click records outside the panel {base.rect(panel)}: {outside}" if outside else None,
        )
    ```
  - в словарь `fixed` функции `check_for` после строки `"game-rally-point": check_rally_point,` добавляются строки `"game-command-damaged-unit": check_command_bar,`, `"game-command-harvester": check_command_bar,`, `"game-command-mcv": check_command_bar,`.
- `tests/ui_audit/data/latin-ru-allowed.tsv`: в конец файла добавляются три строки (поля через табуляцию): `CTRL`, `R`, `D`; причина у каждой — `подпись клавиши на кнопке панели приказов (src/drawers/cCommandBarDrawer.cpp)`.
- Ожидание числа записей `command:` в сценах: танк — Move, Attack, Repair; харвестер — Move, Repair, Unload; MCV — Move, Repair, Deploy. Если сцена даёт иное число или недоступна кнопка, которая по правилам панели должна быть доступна, — блок `## Q-P10A-NN` с записями сцены и стоп.

### 12. Уведомления над панелью

`src/game/cGame_logic.cpp`, `cGame::drawState`: строка `    m_notificationArea->draw(m_textDrawer, 14, m_gameSettings->getScreenH() - 64);` заменяется строками:
```cpp
    int notificationY = m_gameSettings->getScreenH() - 64;
    if (isState(GAME_PLAYING)) {
        notificationY = CommandBarLayout::create(m_gameSettings->getScreenW(), m_gameSettings->getScreenH(), cSideBar::SidebarWidth).panel.getY() - 18;
    }
    m_notificationArea->draw(m_textDrawer, 14, notificationY);
```
Подключения: `drawers/CommandBarLayout.hpp` и `sidebar/cSideBar.h` (каждое — если его в файле нет). `cNotificationArea` не меняется.

### 13. Картинки панели

Файлы `resources/bin/data/hd4/command_bar.png` и `resources/bin/data/hd4/command_bar_disabled.png` уже лежат в рабочей копии, их не меняй. Хэши (`sha256` объектов LFS): `2194d72c6de3bd01193701b708da3001485d7c0e23d69d8eb7563d88115d2acf` и `4a763c285568a6dd860f882c0a3f249d19e45a5690aef7c6fa5a0f61f3e44f23`. Проверка — в разделе «Проверки».

### 14. Правила переноса и подключения

Правила переноса применяются к каждой строке форка, которую пункты 5 и 7 переносят в порт.

1. `renderDrawer->` → `m_sdlDrawer->` (тот же метод, те же аргументы).
2. `game.m_screenW` → `m_settings->getScreenW()`, `game.m_screenH` → `m_settings->getScreenH()`.
3. `unit[<номер>]` → `m_objects->getUnit(<номер>)`; результат — указатель: ссылка `cUnit &x = unit[id]` становится `cUnit *x = m_objects->getUnit(id)`, константная ссылка — `const cUnit *x = ...`, обращения `x.` — `x->`. `structure[...]` → `m_objects->getStructures()[...]`.
4. `assert(` → `d2tm_assert(`.
5. Имя поля `mouseTile` → `m_mouseTile`.
6. Строки `game.getGraphicsDensity()`, `game.m_commandBindings` и подключения `<SDL2/...>`, `d2tmc.h`, `utils/Localization.hpp` второй раз не переносятся; `commandBindingDisplayName` не переносится.
7. Вызов функции форка, у которой нет пары в порту и которая не названа в контракте, — блок `## Q-P10A-NN` и стоп.

**Подключение.** Каждая новая строка `#include "…"` из пунктов 3–10 и 12 добавляется сразу после последней строки вида `#include "…"` в начале файла, если такой строки в файле ещё нет; несколько новых строк одного файла идут подряд в порядке пунктов. Для заголовка `.h` строки `#include` добавляются так же. Исключение: пункты 7.1 и 10 называют порядок сами.

### 15. Сохранить из апстрима

Это поведение порта остаётся после переноса:

1. Клавиши приказов обрабатывают `isAction`/`involvesActionKey` режимов мыши и `cGamePlaying` — они не меняются; кнопки панели дают те же приказы, что клавиши.
2. Правая кнопка без режима команды (ничего не выбрано, выбрана постройка, выбраны юниты в обычном режиме) действует как раньше; режим ремонта правая кнопка отменяет, как и раньше, — по пункту 6: снимает выбор, не мешая прокрутке карты правой кнопкой.
3. Фильтр колеса мыши над боковой панелью и мини-картой в `cGamePlaying::onNotifyMouseEvent` остаётся; к нему добавляется только условие панели приказов.
4. Предел построек при развёртывании MCV (проверка `getFreeSlot() < 0` в `cGamePlaying`) остаётся; кнопка «Развернуть» соблюдает тот же предел.
5. Проверка совпадений клавиш `checkForClashes` только пишет предупреждения и ничего не блокирует; не меняется.
6. Предел юнитов апстрима (`cUnits::MAX_UNITS_CAPACITY`, `isUnitLimitReached`, сообщения и блокировка списков) не меняется; панель не вызывает `unitCreate` и `addOrder`.
7. Вывод уведомлений (`cNotificationArea::draw`) и их место вне боя (`getScreenH() - 64`) не меняются; в бою меняется только высота строки отсчёта (пункт 12).

## Тесты

Новые тесты — Catch2; имя каждого случая начинается с `P10A `, тег `[P10A]`. Тесты форка шага — не Catch2 (`int main()`): каждый переносится в новый файл по таблицам ниже; число проверок (`REQUIRE`/`CHECK`) в новом файле не меньше числа проверок в файле форка; случаев по одному на проверку форка. Тесты пишутся в шаге 1 плана. В шаге 2 они краснеют: сборка падает, потому что нет заголовков `CommandModePolicy.hpp`, `CommandBarLayout.hpp`, `CommandBarPolicy.hpp` и метода `getFirstKeyDisplayName`.

**`tests/CMakeLists.txt`:**
- в `TEST_FILES` сразу после строки `    ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_cKeyBindings.cpp` — строки (в этом порядке):
  ```
      ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_CommandKeys.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_CommandPolicies.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_MouseClickInit.cpp
      ${CMAKE_CURRENT_SOURCE_DIR}/drawers/test_CommandBarLayout.cpp
  ```
- в `TEST_SOURCES` сразу после строки `    ${CMAKE_SOURCE_DIR}/src/controls/cKeyBindings.cpp` — строки для `test_MouseClickInit.cpp`: `    ${CMAKE_SOURCE_DIR}/src/controls/cMouse.cpp`, `    ${CMAKE_SOURCE_DIR}/src/context/GameContext.cpp`, `    ${CMAKE_SOURCE_DIR}/src/context/TextContext.cpp`. Если сборка `d2tm_tests` с этими тремя файлами не линкуется из-за неопределённых имён, к ним можно добавить не больше трёх файлов `.cpp` только из папок `src/controls`, `src/context`, `src/utils` (в том же месте, в алфавитном порядке); каждый добавленный файл — запись «Решено исполнителем» с именем неопределённого символа. Потребовался любой другой файл или больше трёх добавленных — блок `## Q-P10A-NN` и стоп.

**T1. `tests/controls/test_CommandKeys.cpp`** (из `CommandBindingsTests.cpp`, 7 проверок форка → 7 случаев). Подключает `controls/cKeyBindings.h`, `utils/cIniFile.h`; помощники — как в `tests/controls/test_cKeyBindings.cpp` (`pressed`, `defaults`); помощник `withKeys(const char *action, const char *value)` создаёт `cSection section("KEYS"); section.setValue(action, value);`, вызывает `defaults()`, затем `loadFromSection(section)` и возвращает `cKeyBindings`.

| № | Проверка форка | Случай Catch2 `P10A ...` | Ожидания |
|---|---|---|---|
| 1 | `commandBinding(attack) == LCTRL` | `P10A attack and rally default to the Ctrl keys` | `defaults().containsActionKey(pressed(SDL_SCANCODE_LCTRL), eKeyAction::ATTACK_MODE)` истинно; то же для `SDL_SCANCODE_RCTRL`; `REQUIRE_FALSE` для `SDL_SCANCODE_R` |
| 2 | `commandBindingDisplayName(attack) == "CTRL"` | `P10A first key name of a modifier pair` | `defaults().getFirstKeyDisplayName(eKeyAction::ATTACK_MODE) == "Ctrl"`; `defaults().getFirstKeyDisplayName(eKeyAction::ADD_TO_SELECTION) == "Shift"`; `withKeys("DEPLOY_UNIT", "Right Alt").getFirstKeyDisplayName(eKeyAction::DEPLOY_UNIT) == "Alt"` |
| 3 | `commandBindingDisplayName(SPACE, false)` | `P10A first key name is the SDL name for other keys` | `withKeys("SEND_TO_REFINERY", "Space").getFirstKeyDisplayName(eKeyAction::SEND_TO_REFINERY) == SDL_GetScancodeName(SDL_SCANCODE_SPACE)`; `defaults().getFirstKeyDisplayName(eKeyAction::REPAIR_UNIT) == "R"` |
| 4 | `setCommandBinding(repair, F)` | `P10A repair key can be rebound` | `withKeys("REPAIR", "F")`: `containsActionKey(pressed(SDL_SCANCODE_F), eKeyAction::REPAIR_UNIT)` истинно, `containsActionKey(pressed(SDL_SCANCODE_R), eKeyAction::REPAIR_UNIT)` ложно |
| 5 | `commandBindingFromIni(commandBindingToIni(repair))` | `P10A rebound key name is shown to the player` | `withKeys("REPAIR", "F").getFirstKeyDisplayName(eKeyAction::REPAIR_UNIT) == "F"` |
| 6 | `commandBindingFromIni("not-a-real-key", R) == R` | `P10A unknown key name keeps the default` | `withKeys("REPAIR", "not-a-real-key")`: `containsActionKey(pressed(SDL_SCANCODE_R), eKeyAction::REPAIR_UNIT)` истинно |
| 7 | `hasAssignedKey` правой клавиши | `P10A default command keys of the six orders` | `defaults()`: `containsActionKey(pressed(SDL_SCANCODE_D), eKeyAction::SEND_TO_REFINERY)`, `containsActionKey(pressed(SDL_SCANCODE_D), eKeyAction::DEPLOY_UNIT)`, `containsActionKey(pressed(SDL_SCANCODE_R), eKeyAction::REPAIR_UNIT)` истинны; `matches(pressed(SDL_SCANCODE_RCTRL), <combo с ctrlPressed = true>, eKeyAction::ATTACK_MODE)` истинно; пустое действие: `cKeyBindings{}.getFirstKeyDisplayName(eKeyAction::ATTACK_MODE).empty()` |

**T2. `tests/controls/test_CommandPolicies.cpp`** (из `InteractionRegressionTests.cpp`: 4 проверки политик режима мыши и 7 проверок доступности кнопок → 11 случаев). Подключает `controls/CommandModePolicy.hpp`, `drawers/CommandBarPolicy.hpp`.

| № | Проверка форка (сообщение) | Случай Catch2 | Ожидания |
|---|---|---|---|
| 1 | «force attack is reset by pointer movement» | `P10A force attack survives pointer movement` | `pointerMoveCommandPolicy(ActiveCommandMode::ForceAttack) == PointerMoveCommandPolicy::Preserve` и `pointerMoveCommandPolicy(ActiveCommandMode::Normal) == PointerMoveCommandPolicy::Reevaluate` |
| 2 | «right click does not cancel force attack» | `P10A right click cancels force attack` | `rightClickCommandPolicy(ActiveCommandMode::ForceAttack) == RightClickCommandPolicy::CancelCommand` и `rightClickCommandPolicy(ActiveCommandMode::Normal) == RightClickCommandPolicy::DefaultAction` |
| 3 | «right click does not cancel rally mode» | `P10A right click cancels rally mode` | `rightClickCommandPolicy(ActiveCommandMode::Rally) == RightClickCommandPolicy::CancelCommand` |
| 4 | «right click does not cancel repair mode» | `P10A right click cancels repair mode` | `rightClickCommandPolicy(ActiveCommandMode::Repair) == RightClickCommandPolicy::CancelCommand` |
| 5 | «repair command is disabled without a repairable selected unit» | `P10A repair command is always available` | `isRepairCommandEnabled()` истинно |
| 6 | «move command availability does not follow unit selection» | `P10A move command follows unit selection` | `!isMoveCommandEnabled(false)` и `isMoveCommandEnabled(true)` |
| 7 | «attack command availability does not follow attack-capable units» | `P10A attack command follows attack-capable units` | `!isAttackCommandEnabled(false)` и `isAttackCommandEnabled(true)` |
| 8 | «unload command availability does not follow harvester state» | `P10A unload command follows harvester state` | `!isUnloadCommandEnabled(false)` и `isUnloadCommandEnabled(true)` |
| 9 | «deploy command availability does not follow MCV selection» | `P10A deploy command follows MCV selection` | `!isDeployCommandEnabled(false)` и `isDeployCommandEnabled(true)` |
| 10 | «rally command availability does not require an owned producer» | `P10A rally command needs an owned producer` | `!isRallyCommandEnabled(false, true)`, `!isRallyCommandEnabled(true, false)`, `isRallyCommandEnabled(true, true)` |
| 11 | «release command availability does not require an owned repair facility» | `P10A release command needs an owned repair facility` | `!isReleaseCommandEnabled(false, true)`, `!isReleaseCommandEnabled(true, false)`, `isReleaseCommandEnabled(true, true)` |

Проверки форка `InteractionRegressionTests.cpp`, которые в T2 не переносятся: заголовок настроек (`AdvancedOptionsHeaderLayout`, шаг П10в), подпись кнопки заказа и три проверки очереди Starport (задание `P10B`, файл `tests/structures/test_StarportOrders.cpp`).

**T3. `tests/controls/test_MouseClickInit.cpp`** (из `MouseClickInitTests.cpp`, 2 проверки → 2 случая). Подключает `context/GameContext.hpp`, `controls/cMouse.h`, `drawers/SDLDrawer.hpp`, `<memory>`. Общий помощник: `GameContext context; context.setSDLDrawer(std::make_unique<SDLDrawer>(nullptr));` (порт требует рисовальщика SDL при создании `cMouse`; текстовый контекст не нужен).

| № | Проверка форка | Случай Catch2 | Ожидания |
|---|---|---|---|
| 1 | `mouse.isLeftButtonClicked()` после создания | `P10A left button is not clicked after creation` | `cMouse mouse(&context);` `REQUIRE_FALSE(mouse.isLeftButtonClicked())` |
| 2 | `mouse.isRightButtonClicked()` после создания | `P10A right button is not clicked after creation` | `REQUIRE_FALSE(mouse.isRightButtonClicked())` |

**T4. `tests/drawers/test_CommandBarLayout.cpp`** (из `CommandBarLayoutTests.cpp`, 8 проверок → 8 случаев). Подключает `drawers/CommandBarLayout.hpp`. Константы случаев 1–6: `screenWidth = 800`, `screenHeight = 600`, `sidebarWidth = 280`, `battlefieldWidth = 520`, `layout = CommandBarLayout::create(800, 600, 280)`.

| № | Проверка форка | Случай Catch2 | Ожидание |
|---|---|---|---|
| 1 | `panel.getWidth() >= battlefieldWidth` → 1 | `P10A command bar is narrower than the battlefield` | `layout.panel.getWidth() < 520` |
| 2 | `panel.getEndY() >= screenHeight` → 2 | `P10A command bar ends above the screen bottom` | `layout.panel.getEndY() < 600` |
| 3 | `panel.isPointWithin(260, 599)` → 3 | `P10A command bar leaves the bottom scroll strip free` | `REQUIRE_FALSE(layout.panel.isPointWithin(260, 599))` |
| 4 | кнопка с ненулевыми размерами → 4 | `P10A every button has a size` | для каждого из 7 `layout.actions`: ширина и высота больше 0 |
| 5 | левый верхний угол кнопки внутри панели → 5 | `P10A every button starts inside the panel` | для каждой кнопки `layout.panel.isPointWithin(button.getX(), button.getY())` |
| 6 | правый нижний угол кнопки внутри панели → 6 | `P10A every button ends inside the panel` | для каждой кнопки `layout.panel.isPointWithin(button.getEndX() - 1, button.getEndY() - 1)` |
| 7 | панель 1920×1080 → 7 | `P10A full size panel is 350 by 52` | `CommandBarLayout::create(1920, 1080, 280).panel.getWidth() == 350` и `.getHeight() == 52` |
| 8 | кнопки 1920×1080 → 8 | `P10A full size buttons are 50 by 52` | для каждой из 7 кнопок `CommandBarLayout::create(1920, 1080, 280)`: ширина 50, высота 52 |


## PLAN-P10A

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tests/controls/test_CommandKeys.cpp`, `tests/controls/test_CommandPolicies.cpp`, `tests/controls/test_MouseClickInit.cpp`, `tests/drawers/test_CommandBarLayout.cpp`, `tests/CMakeLists.txt` | Раздел «Тесты». | помощник A |
| 2 | — | Красный прогон: команда сборки проверки 1, у которой вместо `.tmp/p10a/build.log` стоит `.tmp/p10a/red-build.log`, — `exit` не `0`, в логе есть строки с `test_CommandKeys.cpp` и `getFirstKeyDisplayName`, с `test_CommandPolicies.cpp` и `CommandModePolicy.hpp`, с `test_CommandBarLayout.cpp` и `CommandBarLayout.hpp`. Запускается до того, как шаги 3 и 4 записали `src/controls/CommandModePolicy.hpp`, `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp` и правку `cKeyBindings`. | помощник A |
| 3 | `src/controls/CommandModePolicy.hpp`, `src/controls/cKeyBindings.h`, `src/controls/cKeyBindings.cpp`, `src/controls/cKeyboard.h`, `src/include/sGameServices.h`, `src/game/cGame_logic.cpp`, `src/controls/cMouse.h`, `src/controls/cGameControlsContext.h`, `src/controls/cGameControlsContext.cpp`, `src/controls/mousestates/cMouseNormalState.h`, `src/controls/mousestates/cMouseNormalState.cpp`, `src/controls/mousestates/cMouseRepairState.cpp`, `src/controls/mousestates/cMouseUnitsSelectedState.h`, `src/controls/mousestates/cMouseUnitsSelectedState.cpp` | Пункты 1–6 и 12 контракта. | помощник B |
| 4 | `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp`, `src/drawers/cCommandBarDrawer.h`, `src/drawers/cCommandBarDrawer.cpp`, `src/CMakeLists.txt`, `src/managers/cDrawManager.h`, `src/managers/cDrawManager.cpp`, `src/gamestates/cGamePlaying.cpp` | Пункты 3 (два заголовка), 7, 8, 9 контракта. | помощник C |
| 5 | `src/debug/UiAudit.hpp`, `src/debug/UiAuditAccess.cpp`, `src/debug/UiAuditScenes.cpp`, `tests/ui_audit/ui_audit_part3b_catalog.py`, `tests/ui_audit/ui_audit_part3b_scenes.py`, `tests/ui_audit/data/latin-ru-allowed.tsv` | Пункты 10 и 11 контракта. | помощник B (после шага 3) |
| 6 | — | Проверки раздела «Проверки» по порядку. | помощник A |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p10`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P10A-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p10a && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p10a/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345; в `ctest.log` ровно 28 строк `P10A ` со словом `Passed`.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает; в неё ничего не пиши.
2. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -F -f .tmp/p10a/changed-paths.txt` — пустой вывод. Файл `.tmp/p10a/changed-paths.txt` — пути файлов `.cpp`, `.hpp` и `.h` из шагов 1, 3, 4 и 5 плана, по одному на строку.
3. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`.
4. **Скрипты режима отладки интерфейса.**
   - Скрипты: `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_part3b_catalog.py`, `ui_audit_part3b_scenes.py`, `ui_audit_language.py`, `ui_audit_translation.py`.
   - Команда для каждого `<скрипт>`: `mkdir -p .tmp/p10a/tmp && TMPDIR=$PWD/.tmp/p10a/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p10a/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
   - Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал. Каждая команда сама ограничена `timeout 1800`; жди, пока она вернёт код выхода. `ui_audit_part3b_scenes.py` и `ui_audit_translation.py` идут по несколько минут — это норма.
   - После проверки — `rm -r tests/ui_audit/__pycache__`, если эта папка появилась.
5. **Python.** `python3 -B -m unittest discover -s tools/ui-audit/tests -p 'test_*.py' > .tmp/p10a/python-tests.log 2>&1; echo exit=$?` — `exit=0`, последняя строка `OK`, в выводе нет `FAILED` и `ERROR`; число `Ran <K> tests` — в сдачу. После — `find tools/ui-audit -name __pycache__ -prune -exec rm -r {} +`.
6. **Сверки `grep`** (в скобках — ожидаемое число строк):
   - `git diff 6ceb29d1604ad0a487436bb9f1a0c60a746deeb6 -- src | grep -E '^\+.*(renderDrawer|game\.m_screen|game\.getMouse|game\.isDebugMode|game\.m_commandBindings|SDL2/|d2tmc\.h)'` (0);
   - `grep -c 'REQUIRE\|CHECK' tests/controls/test_CommandKeys.cpp` — не меньше 7; `tests/controls/test_CommandPolicies.cpp` — не меньше 11; `tests/controls/test_MouseClickInit.cpp` — не меньше 2; `tests/drawers/test_CommandBarLayout.cpp` — не меньше 8;
   - `grep -c 'getCommandBarDrawer' src/controls/cGameControlsContext.cpp src/gamestates/cGamePlaying.cpp` (по 1 в каждом);
   - `grep -n 'recordCommandBarClicks' src/debug/UiAudit.hpp src/debug/UiAuditAccess.cpp src/drawers/cCommandBarDrawer.cpp` (3: объявление, определение, вызов);
   - `grep -c 'game-command-' src/debug/UiAuditScenes.cpp` (3).
7. **Картинки.** `printf '2194d72c6de3bd01193701b708da3001485d7c0e23d69d8eb7563d88115d2acf  resources/bin/data/hd4/command_bar.png\n4a763c285568a6dd860f882c0a3f249d19e45a5690aef7c6fa5a0f61f3e44f23  resources/bin/data/hd4/command_bar_disabled.png\n' | sha256sum -c -` — код 0, обе строки `OK`.
8. `git -c lfs.storage=$PWD/.tmp/p10a/lfs status --short` — изменённые (` M`) пути — только пути шагов 1, 3, 4 и 5 плана; два файла картинок панели (их кладёт ведущий) в счёт не идут; новые (`??`) — только: `src/controls/CommandModePolicy.hpp`, `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp`, `src/drawers/cCommandBarDrawer.h`, `src/drawers/cCommandBarDrawer.cpp`, `tests/controls/test_CommandKeys.cpp`, `tests/controls/test_CommandPolicies.cpp`, `tests/controls/test_MouseClickInit.cpp`, `tests/drawers/test_CommandBarLayout.cpp`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P10A-NN` с выводом и стоп. Ожидания существующих тестов и скрипты в `tests/ui_audit/` меняются только так, как назвал пункт 11; `tools/ui-audit/` не меняется.

## Сдача

Последнее сообщение — блок `## DONE-P10A | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p10a/progress.md`): строка на каждый шаг плана;
- красный прогон шага 2: строки `.tmp/p10a/red-build.log` с `error` (не больше 30);
- вывод каждой проверки 1–8 с кодами выхода (не больше 40 строк на проверку); строки `ctest.log` с `P10A ` и итоговая строка;
- таблица «проверка форка → случай Catch2» с числами `REQUIRE`/`CHECK` по четырём новым файлам из проверки 6;
- `git diff --stat` и список для коммитов:
  1. тесты: файлы шага 1;
  2. перенос и новые заголовки без смены поведения: `src/controls/CommandModePolicy.hpp`, `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp`;
  3. код панели, клавиш и режимов мыши: файлы шагов 3 и 4 (кроме двух заголовков коммита 2);
  4. режим отладки интерфейса: файлы шага 5;
  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …`;
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже (в том числе каждый добавленный `#include`, не названный в пункте 7.1, и каждый файл в `TEST_SOURCES`, добавленный сверх трёх);
- число `Ran <K> tests` из проверки 5;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p10a --size`; у `.tmp/p10a` пометка `оставить — логи проверок нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаг 1 (помощник A), шаг 3 (помощник B) и шаг 4 (помощник C) — одновременно; помощники B и C не создают `src/controls/CommandModePolicy.hpp`, `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp` и не правят `cKeyBindings`, пока помощник A не записал в журнал хода строку о конце шага 2.
  4. Шаг 2 (помощник A) — сразу после шага 1.
  5. Шаг 5 (помощник B) — после шага 3.
  6. Шаг 6 (помощник A) — после шагов 2, 4 и 5.
  7. Сдача и стоп.
- **Параллельно:** шаги 1, 3 и 4 правят разные файлы и идут одновременно; общего у них только порядок записи заголовков и правки `cKeyBindings` (пункт 3 порядка). Собирает их вместе проверка 1 шага 6.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных; одновременно — не больше трёх. Ожидаемое время: помощник A — 50 минут на шаги 1–2 и 60 минут на шаг 6; помощник B — 50 минут на шаг 3 и 40 минут на шаг 5; помощник C — 70 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено», «Контракт поведения» (пункты его шагов и пункт 14), «Сохранить из апстрима» (подраздел 15); его шаги плана; помощнику A — раздел «Тесты» и раздел «Проверки»; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p10a/`.
  - Корневая нить раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Остановки:** только на `## DONE-P10A` и на блоках `## Q-P10A-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P10A-NN` и стоп.
- **Рамка правок:** файлы шагов 1, 3, 4 и 5 плана и папка `.tmp/p10a/`. Понадобился другой файл — блок `## Q-P10A-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` и временные папки скриптов; это не правка.

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
