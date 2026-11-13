### src/gamestates/cScoringState.h@91416fb

Команда:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.h | nl -ba
```

Вывод:
```text
     1	#pragma once
     2	
     3	#include "cGameState.h"
     4	#include "game/MissionStats.h"
     5	
     6	class cKeyboardEvent;
     7	struct s_MouseEvent;
     8	class cGameSettings;
     9	class MissionFlow;
    10	class GameStateTransition;
    11	class cTextDrawer;
    12	class cMouse;
    13	class cScreenFader;
    14	
    15	class cScoringState : public cGameState {
    16	
    17	public:
    18	    explicit cScoringState(sGameServices* services);
    19	    ~cScoringState() override;
    20	
    21	    void thinkFast() override;
    22	    void draw() const override;
    23	
    24	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    25	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    26	
    27	    eGameStateType getType() override;
    28	
    29	private:
    30	    void continueToWinBrief() const;
    31	
    32	    cGameSettings* m_settings = nullptr;
    33	    MissionFlow* m_missionFlow = nullptr;
    34	    GameStateTransition* m_stateTransitions = nullptr;
    35	    cTextDrawer* m_textDrawer = nullptr;
    36	    cTextDrawer* m_smallTextDrawer = nullptr;
    37	    cMouse* m_mouse = nullptr;
    38	    cScreenFader* m_screenFader = nullptr;
    39	    MissionStats m_stats;
    40	};
```

### src/gamestates/cVideoState.h@91416fb

Команда:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cVideoState.h
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
    18	#include "cGameState.h"
    19	#include <memory>
    20	#include <string>
    21	
    22	class cGameSettings;
    23	class GameStateTransition;
    24	class cMouse;
    25	class Graphics;
    26	class Texture;
    27	
    28	class cVideoState : public cGameState {
    29	public:
    30	    cVideoState(sGameServices* services, const std::string &filename);
    31	    ~cVideoState() override;
    32	
    33	    void thinkFast() override;
    34	    void thinkNormal() override;
    35	    void draw() const override;
    36	
    37	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    38	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    39	
    40	    eGameStateType getType() override;
    41	
    42	private:
    43	    cGameSettings* m_settings = nullptr;
    44	    GameStateTransition* m_stateTransitions = nullptr;
    45	    cMouse* m_mouse = nullptr;
    46	    std::unique_ptr<Graphics> m_gfxMovie;
    47	    int m_movieFrame = 0;
    48	    int m_offsetX = 0;
    49	    int m_offsetY = 0;
    50	    Texture* m_currentFrame = nullptr;
    51	};
    52
```

### src/gamestates/cEditorState.h@91416fb

Команда:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cEditorState.h
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
    18	#include "cGameState.h"
    19	#include "utils/cMatrix.h"
    20	#include "controls/cKeyboardEvent.h"
    21	#include "controls/sMouseEvent.h"
    22	#include "utils/cRectangle.h"
    23	
    24	#include <memory>
    25	#include <array>
    26	#include <string>
    27	#include <vector>
    28	
    29	class Texture;
    30	class Graphics;
    31	
    32	struct s_PreviewMap;
    33	class cPreviewMaps;
    34	class GuiBar;
    35	class GuiButtonGroup;
    36	class cTextDrawer;
    37	class cMouse;
    38	class cEditorUndoRedoHistory;
    39	class cEditorCam;
    40	class cEventEmitter;
    41	class GameStateTransition;
    42	class cGameSettings;
    43	
    44	class cEditorState : public cGameState {
    45	public:
    46	    explicit cEditorState(sGameServices* services);
    47	    ~cEditorState() override;
    48	
    49	    void thinkFast() override;
    50	    void draw() const override;
    51	    // load mapIndex from cPreviewMaps, if -1 is given, load the currently edited map (m_editedMap)
    52	    void loadMap(int mapIndex);
    53	    void setCursorSize(int value);
    54	
    55	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    56	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    57	
    58	    eGameStateType getType() override;
    59	private:
    60	    Graphics *m_gfxdata = nullptr;
    61	    Graphics *m_gfxeditor = nullptr;
    62	    cGameSettings *m_settings = nullptr;
    63	    cEventEmitter* m_eventEmitter = nullptr;
    64	    GameStateTransition* m_stateTransitions = nullptr;
    65	    cMouse* m_mouse = nullptr;
    66	    cTextDrawer *m_textDrawer = nullptr;
    67	    cPreviewMaps* m_previewMaps = nullptr;
    68	    std::string m_mapName, m_mapAuthor, m_mapDescription;
    69	    enum class Direction : char { top, bottom, left, right, topLeft, topRight, bottomLeft, bottomRight };
    70	    void populateTopologyBar();
    71	    void populateStartCellBar();
    72	    void populateSelectBar();
    73	    void populateSymmetricBar();
    74	    void setCurrentBar(GuiBar* bar);
    75	    void modifySymmetricArea(Direction dir);
    76	
    77	    void drawMap() const;
    78	    void drawHoveredCellHighlight() const;
    79	    void drawSelectionRectangle() const;
    80	    void drawPastePreviewGhost() const;
    81	    void drawStartCells() const;
    82	    void drawGrid() const;
    83	    void drawAxes() const;
    84	    int getActiveCursorSize() const;
    85	    int getNormalizedCursorSize() const;
    86	    void getBrushTileBounds(int centerTileX, int centerTileY, int &brushStartTileX, int &brushStartTileY, int &brushEndTileX, int &brushEndTileY) const;
    87	    void modifyTile(int posX, int posY, int tileID);
    88	    void modifyStartCell(int posX, int posY, int startCellID);
    89	    void normalizeModifications();
    90	    bool tryGetTileFromMouseCoords(const cPoint &coords, int &tileX, int &tileY) const;
    91	    bool tryGetEditableTileFromMouseCoords(const cPoint &coords, int &tileX, int &tileY) const;
    92	    bool isEditableTile(int tileX, int tileY) const;
    93	    void updateSelectionFromTiles(int startTileX, int startTileY, int endTileX, int endTileY);
    94	    void copySelectionToClipboard();
    95	    void cutSelectionToClipboard();
    96	    void pasteClipboardAtMouseCursor();
    97	
    98	    bool saveMap(bool backup = false) const;
    99	    std::unique_ptr<GuiBar> m_selectBar;
   100	    std::unique_ptr<GuiBar> m_topologyBar;
   101	    std::unique_ptr<GuiBar> m_startCellBar;
   102	    std::unique_ptr<GuiBar> m_symmetricBar;
   103	    GuiBar* m_currentBar = nullptr;
   104	    std::unique_ptr<Matrix<int>> m_mapData;
   105	    std::unique_ptr<GuiButtonGroup> m_selectGroup;
   106	    std::unique_ptr<GuiButtonGroup> m_topologyGroup;
   107	    std::unique_ptr<GuiButtonGroup> m_startCellGroup;
   108	    std::unique_ptr<GuiButtonGroup> m_symmetricGroup;
   109	
   110	    std::unique_ptr<cEditorUndoRedoHistory> m_undoRedo;
   111	    std::unique_ptr<cEditorCam> m_editorCam;
   112	
   113	    cRectangle mapSizeArea;
   114	
   115	    // map modification 
   116	    int idTerrainToMapModif = -1;
   117	    int idStartCellPlayer = -1;
   118	    int m_cursorSize = 1;
   119	    int m_topologyCursorSize = 1;
   120	    bool m_displayGrid = false;
   121	    bool m_displayAxes = false;
   122	    bool m_hasChanged = false;
   123	    bool m_displayPastPreview = false;
   124	
   125	    bool m_hasSelection = false;
   126	    bool m_isDraggingSelection = false;
   127	    int m_selectionStartTileX = 1;
   128	    int m_selectionStartTileY = 1;
   129	    int m_selectionEndTileX = 1;
   130	    int m_selectionEndTileY = 1;
   131	    int m_selectionAnchorTileX = 1;
   132	    int m_selectionAnchorTileY = 1;
   133	
   134	    std::vector<std::vector<int>> m_clipboardTiles;
   135	
   136	    // startCell positions 
   137	    std::array<cPoint,5> startCells;
   138	};
```

### src/gamestates/cNewMapEditorState.h@91416fb

Команда:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewMapEditorState.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cNewMapEditorState.h
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
    18	#include "cGameState.h"
    19	#include "controls/cKeyboardEvent.h"
    20	#include "controls/sMouseEvent.h"
    21	
    22	#include <memory>
    23	#include <vector>
    24	
    25	
    26	class cTextDrawer;
    27	class ScenarioFlow;
    28	class GameStateTransition;
    29	class cMouse;
    30	class GuiWindow;
    31	class GuiCycleButton;
    32	class GuiCheckBox;
    33	class GuiTextInput;
    34	class cPreviewMaps;
    35	class cGameObjectContext;
    36	class cIni;
    37	class cGameSettings;
    38	
    39	
    40	class cNewMapEditorState : public cGameState {
    41	public:
    42	    cNewMapEditorState(sGameServices* services, cIni* ini);
    43	    ~cNewMapEditorState() override;
    44	
    45	    void thinkFast() override;
    46	    void draw() const override;
    47	
    48	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    49	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    50	    bool isKeyboardCapturedByUi() const override;
    51	
    52	    eGameStateType getType() override;
    53	
    54	private:
    55	    cTextDrawer* m_textDrawer = nullptr;
    56	    cGameSettings* m_settings = nullptr;
    57	    ScenarioFlow* m_scenarioFlow = nullptr;
    58	    GameStateTransition* m_stateTransitions = nullptr;
    59	    cMouse* m_mouse = nullptr;
    60	    std::unique_ptr<GuiWindow> m_guiWindow;
    61	    cGameObjectContext* m_objects = nullptr;
    62	    cPreviewMaps* m_previewMap = nullptr;
    63	    cIni* m_cIni = nullptr;
    64	    void constructWindow();
    65	    GuiTextInput* m_inputName = nullptr;
    66	    GuiTextInput* m_inputAuthor = nullptr;
    67	    GuiTextInput* m_inputDescription = nullptr;
    68	    GuiTextInput* m_inputSeed = nullptr;
    69	    GuiCheckBox* m_checkRandom = nullptr;
    70	    bool m_randomChecked = false;
    71	    GuiCycleButton* m_cycleWidth = nullptr;
    72	    GuiCycleButton* m_cycleHeight = nullptr;
    73	
    74	    void constructEmptyMap();
    75	    void updateRandomCheckBox();
    76	
    77	    static constexpr int minRandomMapSize = 64;
    78	    std::vector<int> m_sizesMap = {16, 24, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192};
    79	};
```

### src/include/eGameState.h@91416fb

Команда:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file eGameState.h
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
    18	enum class eGameState : char {
    19	    INITIALIZE = 0,        // initialize game
    20	    OVER,                  // game over
    21	    MENU,                  // in a menu
    22	    PLAYING,               // playing the actual game
    23	    BRIEFING,              // doing some briefing
    24	    EDITOR,                // running the editor
    25	    NEW_MAP_EDITOR,        // prepare new map editor parameters
    26	    OPTIONS,               // options menu
    27	    REGION,                // select a region / select your next conquest
    28	    SELECT_HOUSE,          // pick a house
    29	    INTRO,               
    30	    TELLHOUSE,             // tell about the house
    31	    WINNING,               // when winning, do some cool animation
    32	    SCORING,               // crude mission scoring screen, shown after winning
    33	    WINBRIEF,              // mentat chatter when won the mission
    34	    LOSEBRIEF,             // briefing when losing
    35	    LOSING,                // when losing, do something cool
    36	    SKIRMISH,              // playing a skirmish mission!
    37	    SETUPSKIRMISH,         // set up a skirmish game
    38	    CREDITS,               // credits
    39	    MISSIONSELECT,         // mission select
    40	    VIDEO,                 // playing a video
    41	    COUNT            
    42	};
    43	
    44	const char *gameStateToString(eGameState state);
    45	
    46	// Game states (state machine)
    47	inline constexpr int GAME_INITIALIZE = -1;      // initialize game
    48	inline constexpr int GAME_OVER = 0;      // game over
    49	inline constexpr int GAME_MENU = 1;      // in a menu
    50	inline constexpr int GAME_PLAYING = 2;      // playing the actual game
    51	inline constexpr int GAME_BRIEFING = 3;      // doing some briefing
    52	inline constexpr int GAME_EDITOR = 4;      // running the editor
    53	inline constexpr int GAME_OPTIONS = 5;		 // options menu
    54	inline constexpr int GAME_REGION = 6;		 // select a region / select your next conquest
    55	inline constexpr int GAME_SELECT_HOUSE = 8;		 // pick a house
    56	inline constexpr int GAME_INTRO = 9;
    57	inline constexpr int GAME_TELLHOUSE = 10;		 // tell about the house
    58	inline constexpr int GAME_WINNING = 11;      // when winning, do some cool animation
    59	inline constexpr int GAME_WINBRIEF = 12;      // mentat chatter when won the mission
    60	inline constexpr int GAME_LOSEBRIEF = 13;      // briefing when losing
    61	inline constexpr int GAME_LOSING = 14;      // when losing, do something cool
    62	inline constexpr int GAME_SKIRMISH = 15;      // playing a skirmish mission!
    63	inline constexpr int GAME_SETUPSKIRMISH = 16;    // set up a skirmish game
    64	inline constexpr int GAME_CREDITS = 17;    // credits
    65	inline constexpr int GAME_MISSIONSELECT = 18;    // mission select
    66	inline constexpr int GAME_NEW_MAP_EDITOR = 19;    // new map editor
    67	inline constexpr int GAME_SCORING = 20;      // crude mission scoring screen, shown after winning
    68	inline constexpr int GAME_VIDEO = 21;           // playing a video
    69	inline constexpr int GAME_MAX_STATES = 22;
    70	
    71	[[deprecated]] // We should start using eGameState enum, get rid of int state
    72	const char *stateToString(const int &state);
```
