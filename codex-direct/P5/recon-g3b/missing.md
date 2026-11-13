# P5G3B, пункт 2: имена форка без объявления в порту

Для команд Git перед запуском был установлен путь к Git LFS:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
```

### MusicController

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'MusicController'
    17	#include "audio/MusicController.h"
   828	            MusicController *music = game.m_musicController.get();
```

Команда и вывод:

```text
$ git grep -n -w 'MusicController' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### MusicCategory

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'MusicCategory'
   836	            auto &state = music->m_categories[static_cast<std::size_t>(MusicCategory::Gameplay)];
   839	            music->m_activeCategory = MusicCategory::Gameplay;
```

Команда и вывод:

```text
$ git grep -n -w 'MusicCategory' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### MusicTrack

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'MusicTrack'
   832	            MusicTrack track;
```

Команда и вывод:

```text
$ git grep -n -w 'MusicTrack' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### setTracks

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'setTracks'
   837	            state.playlist.setTracks({track});
```

Команда и вывод:

```text
$ git grep -n -w 'setTracks' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### m_musicController

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'm_musicController'
   828	            MusicController *music = game.m_musicController.get();
```

Команда и вывод:

```text
$ git grep -n -w 'm_musicController' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### currentDisplayName

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'currentDisplayName'
   841	            return !music->currentDisplayName().empty();
```

Команда и вывод:

```text
$ git grep -n -w 'currentDisplayName' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### cCommandBarDrawer

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'cCommandBarDrawer'
     9	#include "drawers/cCommandBarDrawer.h"
   401	void UiAuditAccess::recordCommandBarClicks(cCommandBarDrawer &drawer)
```

Команда и вывод:

```text
$ git grep -n -w 'cCommandBarDrawer' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### m_buttons

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'm_buttons'
   403	    for (const auto &button : drawer.m_buttons) {
```

Команда и вывод:

```text
$ git grep -n -w 'm_buttons' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### mouse_co_x1

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'mouse_co_x1'
   885	            mouse->mouse_co_x1 = mapCamera->getWindowXPositionFromCell(cell1);
```

Команда и вывод:

```text
$ git grep -n -w 'mouse_co_x1' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### mouse_co_y1

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'mouse_co_y1'
   886	            mouse->mouse_co_y1 = mapCamera->getWindowYPositionFromCell(cell1);
```

Команда и вывод:

```text
$ git grep -n -w 'mouse_co_y1' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### getMouse

Команда и вывод:

```text
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | grep -w 'getMouse'
   884	            cMouse *mouse = game.getMouse();
```

Команда и вывод:

```text
$ git grep -n -w 'getMouse' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | head -20

```

### cMouse.h

Команда и вывод:

```text
$ git ls-tree -r --name-only dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | grep -E '/cMouse.h$'
src/controls/cMouse.h
```

Команда и вывод:

```text
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.h | nl -ba
     1	/**
     2	 * @file cMouse.h
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#pragma once
    17	
    18	#include "utils/cPoint.h"
    19	
    20	#include <SDL3/SDL.h>
    21	#include <string>
    22	
    23	class cRectangle;
    24	class GameContext;
    25	class SDLDrawer;
    26	class cInputObserver;
    27	class cGameSettings;
    28	
    29	class cMouse {
    30	
    31	public:
    32	    cMouse(GameContext *ctx);
    33	
    34	    ~cMouse();
    35	
    36	    void handleEvent(const SDL_Event &event);
    37	
    38	    void updateState(); // updates state from SDL, calls appropriate on* methods on gameControlContext class
    39	
    40	    void setMouseObserver(cInputObserver *mouseObserver);
    41	
    42	    void init();
    43	
    44	    void setSettings(cGameSettings *settings) { m_settings = settings; }
    45	
    46	    // these functions return true when the mouse button is being hold down
    47	    bool isLeftButtonPressed() {
    48	        return m_leftButtonPressed;
    49	    }
    50	
    51	    bool isRightButtonPressed() {
    52	        return m_rightButtonPressed;
    53	    }
    54	
    55	    // these functions return true when the mouse button was pressed in the previous
    56	    // frame, but released in the current (which is counted as a 'click')
    57	    bool isLeftButtonClicked() {
    58	        return m_leftButtonClicked;
    59	    }
    60	
    61	    bool isRightButtonClicked() {
    62	        return m_rightButtonClicked;
    63	    }
    64	
    65	    int getX() {
    66	        return m_coords.x;
    67	    }
    68	
    69	    int getY() {
    70	        return m_coords.y;
    71	    }
    72	
    73	    void setCursorPosition(SDL_Window *_windows, int x, int y);
    74	
    75	    bool isOverRectangle(int x, int y, int width, int height);
    76	
    77	    bool isOverRectangle(cRectangle *rectangle);
    78	
    79	    bool isMapScrolling();
    80	
    81	    bool isBoxSelecting();
    82	
    83	    void setTile(int value);
    84	
    85	    void resetDragViewportInteraction();
    86	
    87	    void dragViewportInteraction();
    88	
    89	    void boxSelectLogic(int mouseCell);
    90	
    91	    cRectangle getBoxSelectRectangle();
    92	
    93	    void resetBoxSelect();
    94	
    95	    bool isTile(int value);
    96	
    97	    void draw();
    98	
    99	    bool isNormalRightClick();
   100	
   101	    int getMouseDragDeltaX();
   102	
   103	    int getMouseDragDeltaY();
   104	
   105	    cPoint getMouseCoords();
   106	
   107	    cPoint getDragLineStartPoint();
   108	
   109	    cPoint getDragLineEndPoint();
   110	
   111	private:
   112	    cInputObserver *m_mouseObserver = nullptr;
   113	    GameContext* m_ctx = nullptr;
   114	    SDLDrawer* m_sdlDrawer = nullptr;
   115	    cGameSettings* m_settings = nullptr;
   116	
   117	    bool m_leftButtonPressed;
   118	    bool m_rightButtonPressed;
   119	
   120	    bool m_leftButtonReleased;
   121	    bool m_rightButtonReleased;
   122	
   123	    bool m_leftButtonClicked;
   124	    bool m_rightButtonClicked;
   125	    bool m_leftButtonDoubleClicked;
   126	
   127	    bool m_leftButtonClickedInPreviousFrame;
   128	    bool m_rightButtonClickedInPreviousFrame;
   129	
   130	    bool m_mouseScrolledUp;
   131	    bool m_mouseScrolledDown;
   132	    bool m_didMouseMove;
   133	
   134	    cPoint m_coords;
   135	    cPoint m_coordsOnClick;
   136	
   137	    // Mouse information - for select box and dragging, etc
   138	    int m_mouseCoX1;        // coordinates
   139	    int m_mouseCoY1;        // of
   140	    int m_mouseCoX2;        // the
   141	    int m_mouseCoY2;        // select box
   142	
   143	    int m_mouseMvX1;        // coordinates
   144	    int m_mouseMvY1;        // of
   145	    int m_mouseMvX2;        // the
   146	    int m_mouseMvY2;        // dragging viewport
   147	
   148	    int m_mouseTile;       // mouse picture in gfxdata
   149	
   150	    std::string mouseTileName(int tile);
   151	
   152	};
```

### cCommandBarDrawer.h

Команда и вывод:

```text
$ git ls-tree -r --name-only dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | grep -E '/cCommandBarDrawer.h$'

```

Файл: нет файла.

```text
нет файла
```

### MusicController.h

Команда и вывод:

```text
$ git ls-tree -r --name-only dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | grep -E '/MusicController.h$'

```

Файл: нет файла.

```text
нет файла
```

### MusicJukeBox.hpp

Команда и вывод:

```text
$ git ls-tree -r --name-only dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | grep -E '/MusicJukeBox.hpp$'
src/context/MusicJukeBox.hpp
```

Команда и вывод:

```text
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/context/MusicJukeBox.hpp | nl -ba
     1	/**
     2	 * @file MusicJukeBox.hpp
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#pragma once
    17	
    18	#include "context/MusicChoice.hpp"
    19	#include "definitions.h"
    20	
    21	#include <filesystem>
    22	#include <optional>
    23	
    24	// Decides what music to play; it does not play anything itself.
    25	// Every music type has its own directory below the root: win, lose, attack, peace, menu and conquest.
    26	// BRIEFING has one per house: briefing/atreides, briefing/harkonnen, briefing/ordos and briefing/sardaukar.
    27	// A file is only picked when custom music is enabled and the directory holds audio files.
    28	class MusicJukeBox {
    29	public:
    30	    explicit MusicJukeBox(std::filesystem::path root = "audio");
    31	
    32	    // Creates the empty directories players can put their music in; failure to do so is harmless.
    33	    void createRepertoryDirectories() const;
    34	
    35	    void setCustomMusicEnabled(bool enabled);
    36	
    37	    [[nodiscard]] MusicChoice choose(eMusicType type, int archiveTrack, int house) const;
    38	
    39	private:
    40	    std::filesystem::path m_root;
    41	    bool m_customMusicEnabled = false;
    42	};
```

### music

Команда и вывод:

```text
$ git grep -n -i -E 'music' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src/managers src/drawers src/sidebar src/gamestates/cGamePlaying.cpp | head -60

```

### command

Команда и вывод:

```text
$ git grep -n -i -E 'command' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src/managers src/drawers src/sidebar src/gamestates/cGamePlaying.cpp | head -60

```

## Краткая сводка

Число строк вывода команд для каждого имени (сначала команда по FORK1, затем поиск по PORT):

| Имя | FORK1 | PORT |
|---|---:|---:|
| MusicController | 2 | 0 |
| MusicCategory | 2 | 0 |
| MusicTrack | 1 | 0 |
| setTracks | 1 | 0 |
| m_musicController | 1 | 0 |
| currentDisplayName | 1 | 0 |
| cCommandBarDrawer | 2 | 0 |
| m_buttons | 1 | 0 |
| mouse_co_x1 | 1 | 0 |
| mouse_co_y1 | 1 | 0 |
| getMouse | 1 | 0 |

Файлы по имени и число строк полного вывода команды git show с nl -ba:

| Имя файла | Путь в PORT | Строк |
|---|---|---:|
| cMouse.h | src/controls/cMouse.h | 152 |
| cCommandBarDrawer.h | нет файла | — |
| MusicController.h | нет файла | — |
| MusicJukeBox.hpp | src/context/MusicJukeBox.hpp | 42 |

Дополнительные поиски: music — 0 строк; command — 0 строк.
