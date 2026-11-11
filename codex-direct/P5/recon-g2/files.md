# Пункт 1. Файлы дословно

### src/include/eGameState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/eGameState.h | nl -ba
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

### src/gamestates/cMainMenuState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMainMenuState.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file cMainMenuState.h
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
    20	#include "utils/cRectangle.h"
    21	#include "controls/sMouseEvent.h"
    22	
    23	#include <memory>
    24	
    25	class Texture;
    26	class cTextDrawer;
    27	class MissionFlow;
    28	class VideoFlow;
    29	class GameStateTransition;
    30	class cMouse;
    31	class GuiButton;
    32	class GuiWindow;
    33	class cGameSettings;
    34	
    35	class cMainMenuState : public cGameState {
    36	public:
    37	    explicit cMainMenuState(sGameServices* services);
    38	    ~cMainMenuState() override;
    39	
    40	    void thinkFast() override;
    41	    void draw() const override;
    42	
    43	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    44	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    45	
    46	    eGameStateType getType() override;
    47	
    48	private:
    49	    void buildHdMenu();
    50	    void drawHdBackground() const;
    51	
    52	    cGameSettings * m_settings = nullptr;
    53	    cTextDrawer* m_textDrawer = nullptr;
    54	    MissionFlow* m_missionFlow = nullptr;
    55	    VideoFlow* m_videoFlow = nullptr;
    56	    GameStateTransition* m_stateTransitions = nullptr;
    57	    cMouse* m_mouse = nullptr;
    58	
    59	    int logoX;
    60	    int logoY;
    61	
    62	    int mainMenuFrameX;
    63	    int mainMenuFrameY;
    64	    int mainMenuWidth;
    65	    int mainMenuHeight;
    66	    cRectangle m_logoRect;
    67	
    68	    std::unique_ptr<GuiWindow> gui_window;
    69	    std::unique_ptr<GuiButton> gui_btn_credits;
    70	
    71	    Texture *bmp_D2TM_Title;
    72	    Texture *m_hdMenuBackground = nullptr;
    73	    Texture *m_hdMenuLogo = nullptr;
    74	    std::unique_ptr<Texture> backGroundDebug;
    75	};
```

### src/gamestates/cChooseHouseState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cChooseHouseState.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file cChooseHouseState.h
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
    19	class cKeyboardEvent;
    20	struct s_MouseEvent;
    21	#include "utils/cRectangle.h"
    22	
    23	#include <string>
    24	
    25	struct SDL_Surface;
    26	class Texture;
    27	class GameContext;
    28	class GameStateTransition;
    29	class MentatFlow;
    30	class cMouse;
    31	class cTextDrawer;
    32	class cGameSettings;
    33	class Graphics;
    34	
    35	class cChooseHouseState : public cGameState {
    36	public:
    37	    explicit cChooseHouseState(sGameServices* services);
    38	    ~cChooseHouseState() override;
    39	
    40	    void thinkFast() override;
    41	    void draw() const override;
    42	
    43	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    44	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    45	
    46	    eGameStateType getType() override;
    47	
    48	private:
    49	    cGameSettings* m_settings = nullptr;
    50	    cTextDrawer* m_textDrawer = nullptr;
    51	    Graphics *m_gfxinter = nullptr;
    52	    GameStateTransition* m_stateTransitions = nullptr;
    53	    MentatFlow* m_mentatFlow = nullptr;
    54	    cMouse* m_mouse = nullptr;
    55	    cRectangle backButtonRect;
    56	
    57	    // TODO: abstract away the selectable houses
    58	    Texture *bmp_HouseAtreides;
    59	    Texture *bmp_HouseOrdos;
    60	    Texture *bmp_HouseHarkonnen;
    61	    Texture *bmp_HouseSardaukar;
    62	    Texture *m_hdBackground = nullptr;
    63	
    64	    // Click areas of house emblems
    65	    cRectangle houseAtreides;
    66	    cRectangle houseOrdos;
    67	    cRectangle houseHarkonnen;
    68	    cRectangle houseSardaukar;
    69	
    70	    // Functions
    71	    bool hoversOverBackButton;
    72	
    73	    void onMouseLeftButtonClicked(const s_MouseEvent &event) const;
    74	
    75	    void onMouseMoved(const s_MouseEvent &event);
    76	    void drawHdBackground() const;
    77	    void drawHdHouseCard(
    78	        const cRectangle &card,
    79	        Texture *emblem,
    80	        const std::string &name) const;
    81	};
```

### src/gamestates/cSelectMissionState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectMissionState.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file cSelectMissionState.h
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
    23	
    24	struct SDL_Surface;
    25	
    26	class GameContext;
    27	class cTextDrawer;
    28	class GuiWindow;
    29	class cGameSettings;
    30	class MissionFlow;
    31	class GameStateTransition;
    32	class cMouse;
    33	class Texture;
    34	
    35	class cSelectMissionState : public cGameState {
    36	public:
    37	    cSelectMissionState(sGameServices* services, int prevState);
    38	    ~cSelectMissionState() override;
    39	
    40	    void thinkFast() override;
    41	    void draw() const override;
    42	
    43	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    44	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    45	
    46	    eGameStateType getType() override;
    47	
    48	private:
    49	    cTextDrawer *m_textDrawer = nullptr;
    50	    cGameSettings* m_settings = nullptr;
    51	    MissionFlow* m_missionFlow = nullptr;
    52	    GameStateTransition* m_stateTransitions = nullptr;
    53	    cMouse* m_mouse = nullptr;
    54	    Texture* m_houseFlag = nullptr;
    55	    int m_flagX = 0;
    56	    int m_flagY = 0;
    57	    int m_flagWidth = 0;
    58	    int m_flagHeight = 0;
    59	    int m_headerX = 0;
    60	    int m_headerWidth = 0;
    61	    int m_headerY = 0;
    62	    Texture* m_hdBackground = nullptr;
    63	    std::unique_ptr<GuiWindow> gui_window;
    64	};
```

### src/gamestates/cSetupSkirmishState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file cSetupSkirmishState.h
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
    19	struct sGameServices;
    20	#include "controls/cKeyboardEvent.h"
    21	#include "definitions.h"
    22	#include "controls/sMouseEvent.h"
    23	#include "utils/cRectangle.h"
    24	#include "utils/Color.hpp"
    25	#include <memory>
    26	#include <functional>
    27	#include <vector>
    28	
    29	struct SDL_Surface;
    30	
    31	class cMouse;
    32	class cPreviewMaps;
    33	class cRandomMapGenerator;
    34	class Graphics;
    35	class SDLDrawer;
    36	class cTextDrawer;
    37	class cGameSettings;
    38	class ScenarioFlow;
    39	class cEventEmitter;
    40	class AudioContext;
    41	class GameStateTransition;
    42	class cScreenFader;
    43	class cMapCamera;
    44	class cGameConditionChecker;
    45	class GuiButton;
    46	
    47	struct s_DataCampaign;
    48	class cGameObjectContext;
    49	
    50	struct s_SkirmishPlayer {
    51	    bool bHuman;
    52	    bool bPlaying;
    53	    int startingUnits;
    54	    int iCredits;
    55	    int iHouse;
    56	    int team;
    57	};
    58	
    59	class cSetupSkirmishState : public cGameState {
    60	
    61	public:
    62	    explicit cSetupSkirmishState(sGameServices* services, cPreviewMaps* previewMaps, s_DataCampaign* dataCompaign);
    63	    ~cSetupSkirmishState() override;
    64	
    65	    void thinkFast() override;
    66	    void draw() const override;
    67	
    68	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    69	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    70	
    71	    eGameStateType getType() override;
    72	
    73	private:
    74	    cTextDrawer* m_textDrawer = nullptr;
    75	    cGameSettings* m_settings = nullptr;
    76	    ScenarioFlow* m_scenarioFlow = nullptr;
    77	    cEventEmitter* m_eventEmitter = nullptr;
    78	    AudioContext* m_audioContext = nullptr;
    79	    GameStateTransition* m_stateTransitions = nullptr;
    80	    cMapCamera* m_mapCamera = nullptr;
    81	    cGameConditionChecker* m_gameConditionChecker = nullptr;
    82	    cScreenFader* m_screenFader = nullptr;
    83	    cGameObjectContext* m_objects = nullptr;
    84	    sGameServices* m_services = nullptr;
    85	    s_DataCampaign* m_dataCampaign = nullptr;
    86	    cPreviewMaps* m_previewMaps = nullptr;
    87	    Graphics* m_gfxinter = nullptr;
    88	    cMouse *m_mouse = nullptr;
    89	
    90	    s_SkirmishPlayer skirmishPlayer[MAX_PLAYERS] = {};
    91	    
    92	    std::unique_ptr<cRandomMapGenerator> randomMapGenerator;
    93	
    94	    bool guiDrawFrame(int x, int y, int width, int height) const ;
    95	    bool guiDrawFramePressed(int x1, int y1, int width, int height) const;
    96	
    97	    std::function<void()> nextFunction;
    98	    std::function<void()> previousFunction;
    99	
   100	    int mapStartingIndexToDisplay;          // index of which maps are currently being displayed in the map list
   101	    int maxMapsInSelectArea = 0;            // maximum number of maps that can be displayed in the select area
   102	    int maxMapsInSelectAreaHorizontally;    // maximum number of maps that can be displayed in the select area, horizontally
   103	    int maxMapsInSelectAreaVertically;      // maximum number of maps that can be displayed in the select area, vertically
   104	    int iSkirmishMap;			            // what map is selected
   105	
   106	    int spawnWorms;
   107	    bool spawnBlooms;
   108	    bool detonateBlooms;
   109	    int iStartingPoints;
   110	    int techLevel;
   111	
   112	    // Colors
   113	    Color colorLightBackground;
   114	    Color colorDarkishBorder;
   115	    Color colorDarkerYellow;
   116	    Color colorDisabled;
   117	    Color colorOtherBorder;
   118	
   119	    // Some basic layout coordinates
   120	    int topBarHeight;
   121	    int previewMapHeight;
   122	    int previewMapWidth;
   123	    int widthOfRightColumn;
   124	    int mapItemButtonHeight;
   125	    int mapItemButtonWidth;
   126	    int m_playerRowHeight = 22;
   127	
   128	    // screen
   129	    int screen_x, screen_y;
   130	
   131	    // Rects
   132	    cRectangle topBar;
   133	    cRectangle playerTitleBar;
   134	    cRectangle topRightBox;
   135	    cRectangle playerList;
   136	    cRectangle mapList;
   137	    cRectangle mapListTitle;
   138	
   139	    cRectangle previewMapTitle; // the title above the sidebar of the preview map
   140	    cRectangle previewMap; // the sidebar where the map is within
   141	    cRectangle previewMapRect; // the actual 'map' image
   142	
   143	    cRectangle startPointsRect;
   144	    cRectangle wormsRect;
   145	    cRectangle bloomsRect;
   146	    cRectangle detonateBloomsRect;
   147	    cRectangle techLevelRect;
   148	    cRectangle selectArea;
   149	
   150	    std::unique_ptr<GuiButton> backButton;
   151	    std::unique_ptr<GuiButton> startButton;
   152	    std::unique_ptr<GuiButton> modifyButton;
   153	    std::unique_ptr<GuiButton> newMapButton;
   154	    std::unique_ptr<GuiButton> surpriseMeButton;
   155	    std::unique_ptr<GuiButton> nextMapButton;
   156	    std::unique_ptr<GuiButton> previousMapButton;
   157	
   158	    // Functions
   159	    void prepareSkirmishGameToPlayAndTransitionToCombatState(int iSkirmishMap);
   160	
   161	    // Returns the starting-unit types that are allowed at the given tech level.
   162	    std::vector<int> getEligibleStartingUnitTypes(int forTechLevel) const;
   163	
   164	    void surpriseMe();
   165	
   166	    void onMouseLeftButtonClicked(const s_MouseEvent &event);
   167	    void onMouseRightButtonClicked(const s_MouseEvent &event);    
   168	
   169	    void drawMapList(const cRectangle &mapList) const;
   170	
   171	    void drawWorms(const cRectangle &wormsRect) const;
   172	
   173	    void drawBlooms(const cRectangle &bloomsRect) const;
   174	
   175	    void drawDetonateBlooms(const cRectangle &detonateBloomsRect) const;
   176	
   177	    void drawPreviewMapAndMore(const cRectangle &previewMapRect) const;
   178	
   179	    void drawStartPoints(int iStartingPoints, const cRectangle &startPoints) const;
   180	
   181	    void drawPlayerBrain(const s_SkirmishPlayer &sSkirmishPlayer, const cRectangle &brainRect) const;
   182	
   183	    void drawHouse(const s_SkirmishPlayer &sSkirmishPlayer, const cRectangle &houseRec) const;
   184	
   185	    void drawCredits(const s_SkirmishPlayer &sSkirmishPlayer, const cRectangle &creditsRect) const;
   186	
   187	    Color getTextColorForRect(const s_SkirmishPlayer &sSkirmishPlayer, const cRectangle &rect) const;
   188	
   189	    void drawStartingUnits(const s_SkirmishPlayer &sSkirmishPlayer, const cRectangle &startingUnitsRect) const;
   190	
   191	    void drawTeams(const s_SkirmishPlayer &sSkirmishPlayer, const cRectangle &teamsRect) const;
   192	
   193	    void drawTechLevel(const cRectangle &techRect) const;
   194	
   195	    void onMouseMovedTo(const s_MouseEvent &event);
   196	
   197	    void generateRandomMap();
   198	
   199	
   200	    void onMouseLeftButtonClickedAtStartPoints();
   201	    void onMouseRightButtonClickedAtStartPoints();
   202	
   203	    void onMouseLeftButtonClickedAtWorms();
   204	    void onMouseRightButtonClickedAtWorms();
   205	
   206	    void onMouseLeftButtonClickedAtMapList(const cRectangle &selectMapRect);
   207	    void onMouseLeftButtonClickedAtSpawnBlooms();
   208	    void onMouseLeftButtonClickedAtDetonateBlooms();
   209	
   210	    void onMouseLeftButtonClickedAtPlayerList();
   211	    void onMouseRightButtonClickedAtPlayerList();
   212	
   213	    void onMouseLeftButtonClickedAtTechLevel();
   214	    void onMouseRightButtonClickedAtTechLevel();
   215	
   216	    void moveCursor(int deltaX, int deltaY);
   217	};
```

### src/gamestates/cOptionsState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file cOptionsState.h
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
    19	class cKeyboardEvent;
    20	struct s_MouseEvent;
    21	#include "include/Texture.hpp"
    22	
    23	#include <cstddef>
    24	#include <memory>
    25	#include <vector>
    26	
    27	struct SDL_Surface;
    28	
    29	class GameContext;
    30	class cTextDrawer;
    31	class GuiWindow;
    32	class GuiButton;
    33	class GuiLabel;
    34	class GameStateTransition;
    35	class cMouse;
    36	class cGameSettings;
    37	
    38	class cOptionsState : public cGameState {
    39	public:
    40	    explicit cOptionsState(sGameServices* services, int prevState);
    41	    ~cOptionsState() override;
    42	
    43	    void thinkFast() override;
    44	    void draw() const override;
    45	
    46	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    47	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    48	
    49	    eGameStateType getType() override;
    50	
    51	    void setPrevState(int prevState);
    52	    void refresh();
    53	
    54	private:
    55	    cTextDrawer* m_textDrawer = nullptr;
    56	    cGameSettings* m_settings = nullptr;
    57	    GameStateTransition* m_stateTransitions = nullptr;
    58	    cMouse* m_mouse = nullptr;
    59	
    60	    int m_prevState;
    61	
    62	    std::vector<int> m_renderScaleChoices;
    63	    std::vector<int> m_worldScaleChoices;
    64	    std::size_t m_selectedRenderScaleIndex = 0;
    65	    std::size_t m_selectedWorldScaleIndex = 0;
    66	    GuiLabel *m_renderScaleValueLabel = nullptr;
    67	    GuiLabel *m_worldScaleValueLabel = nullptr;
    68	    GuiLabel *m_statusLabel = nullptr;
    69	    GuiButton *m_applyButton = nullptr;
    70	
    71	    std::unique_ptr<GuiWindow> m_guiWindow;
    72	
    73	    void constructWindow(int prevState);
    74	    void selectRenderScale(int step);
    75	    void selectWorldScale(int step);
    76	    void updateScaleControls();
    77	    void applyScaleSettings();
    78	    Texture *const *m_backgroundTexture = nullptr;
    79	};
```

### src/gamestates/cCreditsState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file cCreditsState.h
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
    19	class cKeyboardEvent;
    20	#include "gui/GuiButton.h"
    21	struct s_MouseEvent;
    22	class cPoint;
    23	
    24	#include <string>
    25	#include <vector>
    26	#include <memory>
    27	
    28	class Texture;
    29	
    30	class cTextDrawer;
    31	class cGameSettings;
    32	class GameStateTransition;
    33	class cMouse;
    34	
    35	struct s_CreditLine {
    36	    std::string name;
    37	    std::string txt;
    38	    Color color;
    39	    int height;
    40	};
    41	
    42	class cCreditsState : public cGameState {
    43	
    44	public:
    45	    explicit cCreditsState(sGameServices* services);
    46	    ~cCreditsState() override;
    47	
    48	    void thinkFast() override;
    49	    void draw() const override;
    50	
    51	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    52	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    53	
    54	    eGameStateType getType() override;
    55	
    56	private:
    57	    cTextDrawer* m_textDrawer = nullptr;
    58	    cGameSettings* m_settings = nullptr;
    59	    GameStateTransition* m_stateTransitions = nullptr;
    60	    cMouse* m_mouse = nullptr;
    61	
    62	    int m_titleX;
    63	    float m_crawlerY;
    64	
    65	    float m_moveSpeed;
    66	    int m_titleHeight;
    67	
    68	    std::vector<s_CreditLine> m_lines;
    69	
    70	    cPoint m_teamCoordinates;
    71	    Texture *m_teamBmp = nullptr;
    72	    Texture *m_titleBmp = nullptr;
    73	    bool m_ownsTeamBmp = false;
    74	    bool m_ownsTitleBmp = false;
    75	    std::unique_ptr<GuiButton> backButton;
    76	
    77	    void resetCrawler();
    78	    void prepareCrawlerLines();
    79	};
    80
```

### src/gamestates/cSelectYourNextConquestState.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file cSelectYourNextConquestState.h
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
    18	#include "definitions.h"
    19	#include "cGameState.h"
    20	#include "gamestates/CampaignMapLayout.hpp"
    21	
    22	#include <array>
    23	#include <memory>
    24	#include <string>
    25	#include <SDL3/SDL.h>
    26	
    27	
    28	class GuiButton;
    29	struct SDL_Surface;
    30	class cMouse;
    31	class cIni;
    32	
    33	class Texture;
    34	class Graphics;
    35	class GameContext;
    36	class SDLDrawer;
    37	class ScenarioFlow;
    38	class AudioContext;
    39	class GameStateTransition;
    40	class MentatFlow;
    41	class MissionFlow;
    42	class cGameSettings;
    43	class cTextDrawer;
    44	class cGameObjectContext;
    45	class cDrawManager;
    46	
    47	struct s_DataCampaign;
    48	enum eRegionState {
    49	    REGSTATE_INIT,                   // Initialization
    50	    REGSTATE_INTRODUCTION,           // The very beginning, ie "3 houses have come to Dune" and ends with drawing the dune regions
    51	    REGSTATE_CONQUER_REGIONS,        // here we change state of regions, ie some regions get conquered / change sides
    52	    REGSTATE_SELECT_NEXT_CONQUEST,   // here the user may select the next area to attack
    53	    REGSTATE_FADEOUT                 // the player clicked on a region and we fade out
    54	};
    55	
    56	// these are the 3 iconic 'scenes' the campaign overview shows, and ends with "Select your next conquest
    57	enum eRegionSceneState {
    58	    SCENE_INIT,                         // load data first
    59	    SCENE_THREE_HOUSES_COME_FOR_DUNE,   // ...
    60	    SCENE_TO_TAKE_CONTROL_OF_THE_LAND,  // ...
    61	    SCENE_THAT_HAS_BECOME_DIVIDED,      // ...
    62	    SCENE_SELECT_YOUR_NEXT_CONQUEST     // this transitions to the next regionState "CONQUER_REGIONS"
    63	};
    64	
    65	class cRegion {
    66	public:
    67	    int iHouse;         // who (which house) owns this?
    68	    int oldHouse;       // avoid recreate Texture
    69	    int x, y;           // x and y position of the region
    70	    int iAlpha;         // Alpha (0 = not visible, > 0 goes up to 255)
    71	    int iTile;          // tile refering to gfxworld.dat
    72	    bool bSelectable;   // selectable for attacking (default = false)
    73	    SDL_Surface *bmp;        // the original bmp
    74	    Texture *bmpColor; // the bmp (created! and thus must be destroyed) on same bitdepth as bmp_screen
    75	};
    76	
    77	class cSelectYourNextConquestState : public cGameState {
    78	
    79	public:
    80	    explicit cSelectYourNextConquestState(sGameServices* services, cIni* ini, s_DataCampaign* dataCompaign);
    81	    ~cSelectYourNextConquestState() override;
    82	    static constexpr int MAX_REGIONS = 27;
    83	
    84	    
    85	    void thinkFast() override;
    86	    void draw() const override;
    87	
    88	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    89	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    90	
    91	    eGameStateType getType() override;
    92	
    93	    // !? need to figure out what this does exactly
    94	    void setRegionConquer(int iRegionIndex, int iRegion) {
    95	        iRegionConquer[iRegionIndex] = iRegion;
    96	    }
    97	
    98	    void setRegionHouse(int iRegionIndex, int iHouse) {
    99	        iRegionHouse[iRegionIndex] = iHouse;
   100	    }
   101	
   102	    void setRegionText(int iRegionIndex, const std::string &txt) {
   103	        cRegionText[iRegionIndex] = txt.substr(0, 254); // the old char buffer held at most 254 characters
   104	    }
   105	
   106	    void regionSetupLostMission();
   107	    void regionSetupNextMission(int iMission, int iHouse);
   108	    void installWorld();
   109	
   110	    void conquerRegions();
   111	
   112	    void calculateOffset();
   113	
   114	    void fastForwardUntilMission(int missionNr, int house);
   115	
   116	private:
   117	    cGameSettings* m_settings = nullptr;
   118	    ScenarioFlow* m_scenarioFlow = nullptr;
   119	    AudioContext* m_audioContext = nullptr;
   120	    GameStateTransition* m_stateTransitions = nullptr;
   121	    MentatFlow* m_mentatFlow = nullptr;
   122	    MissionFlow* m_missionFlow = nullptr;
   123	    cTextDrawer* m_textDrawer = nullptr;
   124	    cGameObjectContext* m_objects = nullptr;
   125	    s_DataCampaign* m_dataCampaign = nullptr;
   126	    Graphics* m_gfxworld = nullptr;
   127	    Graphics* m_gfxinter = nullptr;
   128	    cMouse* m_mouse = nullptr;
   129	    cDrawManager *m_drawManager = nullptr;
   130	    cIni* m_cIni = nullptr;
   131	    eRegionState state;
   132	
   133	    eRegionSceneState regionSceneState;
   134	    int iRegionSceneAlpha;          // scene alpha
   135	
   136	    int iRegionConquer[MAX_REGIONS];     // INDEX = REGION NR , > -1 means conquered..
   137	    int iRegionHouse[MAX_REGIONS];       // I guess... this is the house that the conquered region will become
   138	
   139	    std::array<std::string, MAX_REGIONS> cRegionText; // text for this
   140	
   141	    int offsetX;
   142	    int offsetY;
   143	
   144	    int selectNextConquestAlpha;
   145	
   146	    int regionMouseIsHoveringOver;
   147	
   148	    SDL_Surface *regionClickMapBmp;  // this is the bmp for determine player'choice.
   149	
   150	    bool isFinishedConqueringRegions = true;
   151	
   152	    bool fastForward = false;
   153	
   154	    std::unique_ptr<GuiButton> m_guiBtnToMissionSelect;
   155	
   156	    // Functions
   157	    void regionDraw(cRegion &regionPiece) const;
   158	
   159	    void drawStateSelectYourNextConquest() const;
   160	
   161	    void drawStateConquerRegions() const;
   162	
   163	    void drawStateIntroduction() const;
   164	
   165	    void drawHdBackground() const;
   166	    void drawHdChrome() const;
   167	    void drawHdMapBase(Uint8 opacity = 255) const;
   168	    void drawHdMapBorders(Uint8 opacity = 255) const;
   169	    void drawHdMessage() const;
   170	    Texture* createHdRegionTintTexture(int regionIndex, int house) const;
   171	    Texture* createHdRegionBordersTexture() const;
   172	
   173	    void transitionToNextRegionSceneState(eRegionSceneState newSceneState);
   174	
   175	    void drawRegion(cRegion &regionPiece) const;
   176	
   177	    void onMouseMove(const s_MouseEvent &event);
   178	
   179	    int regionOver(int mouseX, int mouseY);
   180	    void regionNew(int x, int y, int iAlpha, int iHouse, int iTile);
   181	
   182	    cRegion *getRegionMouseIsOver() const;
   183	
   184	    void loadScenarioAndTransitionToNextState(int iMission);
   185	
   186	    bool onMouseLeftButtonClicked(const s_MouseEvent &event);
   187	    mutable std::array<cRegion, MAX_REGIONS> world{};
   188	    CampaignMapLayout m_hdCampaignLayout;
   189	    Texture* m_hdBackground = nullptr;
   190	    Texture* m_hdCampaignMap = nullptr;
   191	    Texture* m_hdRegionBorders = nullptr;
   192	    Texture* m_hdHouseCrest = nullptr;
   193	};
```

### src/gameobjects/mentat/AbstractMentat.h@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.h | nl -ba
```

Вывод:

```text
     1	/**
     2	 * @file AbstractMentat.h
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
    18	#include "utils/cRectangle.h"
    19	#include "observers/cInputObserver.h"
    20	class Graphics;
    21	
    22	#include <array>
    23	#include <string>
    24	#include <memory>
    25	#include <SDL3_ttf/SDL_ttf.h>
    26	
    27	class GuiButton;
    28	struct SDL_Surface;
    29	class Texture;
    30	class GameContext;
    31	class MentatFlow;
    32	class GameStateTransition;
    33	class cGameSettings;
    34	class SDLDrawer;
    35	class cTextDrawer;
    36	
    37	enum eMentatState {
    38	    INIT,               // for loading data (Default state)
    39	    SPEAKING,           // the mentat is speaking about whatever
    40	    AWAITING_RESPONSE,  // the mentat is done speaking, the user needs to click something (yes/no, proceed/repeat, etc)
    41	    DESTROY,            // the mentat became 'invalid' (BeneGeserit-><house> transition)
    42	};
    43	
    44	class AbstractMentat : public cInputObserver {
    45	public:
    46	    AbstractMentat(GameContext* ctx, cGameSettings* settings, GameStateTransition* stateTransitions, MentatFlow* mentatFlow, bool canMissionSelect);
    47	    virtual ~AbstractMentat();
    48	
    49	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    50	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    51	
    52	    virtual void draw() = 0;
    53	    virtual void think() = 0;
    54	
    55	    void loadScene(const std::string &scene);
    56	
    57	    Texture *getBackgroundBitmap() const;
    58	
    59	    void initSentences();
    60	    void speak();
    61	    void setSentence(int i, const std::string &text);
    62	    void thinkMouth();
    63	    void thinkEyes();
    64	    void thinkMovie();
    65	    void setHouse(int value) {
    66	        house = value;
    67	    }
    68	    int getHouse() {
    69	        return house;
    70	    }
    71	    void resetSpeak();
    72	protected:
    73	    virtual void draw_mouth() = 0;
    74	
    75	    virtual void draw_eyes() = 0;
    76	
    77	    virtual void draw_other() = 0;
    78	
    79	    void draw_movie();
    80	
    81	    // Timed animation
    82	    int TIMER_Mouth;
    83	    int TIMER_Eyes;
    84	    int TIMER_Other;
    85	    int TIMER_Speaking;
    86	
    87	    // Movie playback (scene's from datafile)
    88	    int TIMER_movie;
    89	    int iMovieFrame;
    90	
    91	    int iBackgroundFrame;
    92	
    93	    // draw 2 sentences at once, so 0 1, 2 3, 4 5, 6 7, 8 9
    94	    std::array<std::string, 10> sentence;
    95	
    96	    int iMentatSentence;  // = sentence to draw and speak with (-1 = not ready)
    97	
    98	    int iMentatMouth;
    99	    int iMentatEyes;
   100	
   101	    std::shared_ptr<Graphics> gfxmovie;
   102	
   103	    eMentatState state;
   104	    cTextDrawer* m_textDrawer = nullptr;
   105	    SDLDrawer* m_sdlDrawer;
   106	
   107	    std::unique_ptr<cRectangle> leftButton;
   108	    std::unique_ptr<cRectangle> rightButton;
   109	
   110	    Texture *leftButtonBmp;
   111	    Texture *rightButtonBmp;
   112	
   113	    void buildLeftButton(Texture *bmp, int x, int y);
   114	    void buildRightButton(Texture *bmp, int x, int y);
   115	    std::unique_ptr<GuiButton> leftGuiButton;
   116	    std::unique_ptr<GuiButton> rightGuiButton;
   117	    int house;
   118	    int offsetX;
   119	    int offsetY;
   120	    int movieTopleftX;
   121	    int movieTopleftY;
   122	
   123	    std::unique_ptr<GuiButton> m_guiBtnToMissionSelect;
   124	    Graphics* gfxmentat;
   125	    GameStateTransition* m_stateTransitions = nullptr;
   126	    MentatFlow* m_mentatFlow = nullptr;
   127	};
```

### src/debug/UiAudit.hpp@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAudit.hpp | nl -ba
```

Вывод:

```text
     1	#pragma once
     2	
     3	#include "debug/UiAuditArguments.hpp"
     4	
     5	#include <string>
     6	
     7	class cGame;
     8	class cGameState;
     9	struct SDL_Renderer;
    10	
    11	namespace uiaudit {
    12	
    13	struct Rect {
    14	    int x;
    15	    int y;
    16	    int w;
    17	    int h;
    18	};
    19	
    20	void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box = nullptr);
    21	void recordGui(const char *type, int x, int y, int w, int h);
    22	void recordClick(const char *name, int x, int y, int w, int h);
    23	
    24	class BoxScope {
    25	public:
    26	    BoxScope(int x, int y, int w, int h);
    27	    ~BoxScope();
    28	    BoxScope(const BoxScope &) = delete;
    29	    BoxScope &operator=(const BoxScope &) = delete;
    30	};
    31	
    32	bool handleEarlyExit(int &exitCode);
    33	void onSetupDone(cGame &game);
    34	void beginFrame(cGame &game);
    35	void onFramePresented(cGame &game);
    36	bool failed();
    37	
    38	}
    39	
    40	class UiAuditAccess {
    41	public:
    42	    static int state(const cGame &game);
    43	    static const cGameState *currentState(const cGame &game);
    44	    static SDL_Renderer *renderer(cGame &game);
    45	    static int renderScale(const cGame &game);
    46	    static int worldScale(const cGame &game);
    47	    static void setState(cGame &game, int state);
    48	    static void freezeClock(cGame &game);
    49	    static void resumeClock(cGame &game);
    50	    static bool notFadingOut(const cGame &game);
    51	};
```

### src/debug/UiAuditScenes.hpp@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAuditScenes.hpp | nl -ba
```

Вывод:

```text
     1	#pragma once
     2	
     3	#include <string>
     4	#include <vector>
     5	
     6	class cGame;
     7	
     8	namespace uiaudit {
     9	
    10	struct Scene {
    11	    const char *id;
    12	    const char *group;
    13	    const char *state;
    14	    const char *screen;
    15	    const char *house;
    16	    bool hud;
    17	    bool gameScreen;
    18	    bool hdOnly;
    19	    bool hover;
    20	    int hoverX;
    21	    int hoverY;
    22	    const char *readiness;
    23	    int settleFrames;
    24	    bool (*prepare)(cGame &game);
    25	    bool (*ready)(cGame &game);
    26	};
    27	
    28	const std::vector<Scene> &catalog();
    29	const Scene *findScene(const std::string &id);
    30	
    31	}
```

### src/debug/UiAuditScenes.cpp@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAuditScenes.cpp | nl -ba
```

Вывод:

```text
     1	#include "debug/UiAuditScenes.hpp"
     2	
     3	#include "game/cGame.h"
     4	#include "debug/UiAudit.hpp"
     5	#include "include/eGameState.h"
     6	
     7	namespace uiaudit {
     8	
     9	namespace {
    10	
    11	struct GroupScreen {
    12	    const char *group;
    13	    const char *state;
    14	    const char *screen;
    15	};
    16	
    17	const GroupScreen kGroupScreens[] = {
    18	    {"main-menu", "GAME_MENU", "cMainMenuState"},
    19	};
    20	
    21	Scene scene(const char *id, const char *group, const char *house, const char *readiness,
    22	            bool (*prepare)(cGame &), bool (*ready)(cGame &) = nullptr, int settleFrames = 2)
    23	{
    24	    Scene result{id, group, "", "", house, false, false, false, false, 0, 0, readiness, settleFrames, prepare, ready};
    25	    for (const GroupScreen &entry : kGroupScreens) {
    26	        if (std::string(entry.group) == group) {
    27	            result.state = entry.state;
    28	            result.screen = entry.screen;
    29	        }
    30	    }
    31	    return result;
    32	}
    33	
    34	bool prepareMainMenu(cGame &game)
    35	{
    36	    UiAuditAccess::setState(game, GAME_MENU);
    37	    return true;
    38	}
    39	
    40	const std::vector<Scene> g_catalog = {
    41	    scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
    42	};
    43	
    44	}
    45	
    46	const std::vector<Scene> &catalog()
    47	{
    48	    return g_catalog;
    49	}
    50	
    51	const Scene *findScene(const std::string &id)
    52	{
    53	    for (const Scene &scene : g_catalog) {
    54	        if (scene.id == id) {
    55	            return &scene;
    56	        }
    57	    }
    58	    return nullptr;
    59	}
    60	
    61	}
```

### src/debug/UiAuditAccess.cpp@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAuditAccess.cpp | nl -ba
```

Вывод:

```text
     1	#include "debug/UiAudit.hpp"
     2	
     3	#include "game/cGame.h"
     4	#include "game/cGameSettings.h"
     5	#include "game/cScreenFader.h"
     6	#include "game/cTimeManager.h"
     7	#include "gamestates/cGameState.h"
     8	
     9	int UiAuditAccess::state(const cGame &currentGame)
    10	{
    11	    return currentGame.m_currentState == nullptr ? -1 : static_cast<int>(currentGame.m_currentState->getType());
    12	}
    13	
    14	const cGameState *UiAuditAccess::currentState(const cGame &currentGame)
    15	{
    16	    return currentGame.m_currentState;
    17	}
    18	
    19	SDL_Renderer *UiAuditAccess::renderer(cGame &currentGame)
    20	{
    21	    return currentGame.renderer;
    22	}
    23	
    24	int UiAuditAccess::renderScale(const cGame &currentGame)
    25	{
    26	    return currentGame.m_gameSettings->m_renderScalePercent;
    27	}
    28	
    29	int UiAuditAccess::worldScale(const cGame &currentGame)
    30	{
    31	    return currentGame.m_gameSettings->m_worldScalePercent;
    32	}
    33	
    34	void UiAuditAccess::setState(cGame &currentGame, int state)
    35	{
    36	    currentGame.setState(state);
    37	}
    38	
    39	void UiAuditAccess::freezeClock(cGame &currentGame)
    40	{
    41	    currentGame.m_timeManager->onWindowFocusLost();
    42	}
    43	
    44	void UiAuditAccess::resumeClock(cGame &currentGame)
    45	{
    46	    currentGame.m_timeManager->onWindowFocusGained();
    47	}
    48	
    49	// drawState restarts the fade-in every idle frame and the fade-in does not change the picture; only a fade-out does.
    50	bool UiAuditAccess::notFadingOut(const cGame &currentGame)
    51	{
    52	    return currentGame.m_cScreenFader->getAction() != eFadeAction::FadeOut;
    53	}
```

### git ls-tree src/gameobjects/mentat/@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git ls-tree --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 src/gameobjects/mentat/
```

Вывод:

```text
src/gameobjects/mentat/AbstractMentat.cpp
src/gameobjects/mentat/AbstractMentat.h
src/gameobjects/mentat/AtreidesMentat.cpp
src/gameobjects/mentat/AtreidesMentat.h
src/gameobjects/mentat/BeneMentat.cpp
src/gameobjects/mentat/BeneMentat.h
src/gameobjects/mentat/HarkonnenMentat.cpp
src/gameobjects/mentat/HarkonnenMentat.h
src/gameobjects/mentat/OrdosMentat.cpp
src/gameobjects/mentat/OrdosMentat.h
src/gameobjects/mentat/SardaukarMentat.cpp
src/gameobjects/mentat/SardaukarMentat.h
```

### git ls-tree src/gamestates/@acddd29

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git ls-tree --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 src/gamestates/
```

Вывод:

```text
src/gamestates/CampaignMapLayout.hpp
src/gamestates/OptionsMenuLayout.hpp
src/gamestates/cChooseHouseState.cpp
src/gamestates/cChooseHouseState.h
src/gamestates/cCreatorState.cpp
src/gamestates/cCreatorState.h
src/gamestates/cCreditsState.cpp
src/gamestates/cCreditsState.h
src/gamestates/cEditorState.cpp
src/gamestates/cEditorState.h
src/gamestates/cEditorState
src/gamestates/cGamePlaying.cpp
src/gamestates/cGamePlaying.h
src/gamestates/cGameState.cpp
src/gamestates/cGameState.h
src/gamestates/cMainMenuState.cpp
src/gamestates/cMainMenuState.h
src/gamestates/cMentatState.cpp
src/gamestates/cMentatState.h
src/gamestates/cNewMapEditorState.h
src/gamestates/cNewmapEditorState.cpp
src/gamestates/cOptionsState.cpp
src/gamestates/cOptionsState.h
src/gamestates/cScoringState.cpp
src/gamestates/cScoringState.h
src/gamestates/cSelectMissionState.cpp
src/gamestates/cSelectMissionState.h
src/gamestates/cSelectYourNextConquestState.cpp
src/gamestates/cSelectYourNextConquestState.h
src/gamestates/cSetupSkirmishState.cpp
src/gamestates/cSetupSkirmishState.h
src/gamestates/cTellHouseState.cpp
src/gamestates/cTellHouseState.h
src/gamestates/cVideoState.cpp
src/gamestates/cVideoState.h
src/gamestates/cWinLoseState.cpp
src/gamestates/cWinLoseState.h
```
