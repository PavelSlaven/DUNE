# P5G2R — пункт 5. Состояния ментата и кампании

### src/gamestates/cMentatState.h@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.h | nl -ba
```

```text
     1	/**
     2	 * @file cMentatState.h
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
    19	#include "gameobjects/mentat/AbstractMentat.h"
    20	#include <memory>
    21	#include "iniSections.h"
    22	
    23	struct s_DataCampaign;
    24	class cReinforcements;
    25	class ScenarioFlow;
    26	class GameStateTransition;
    27	class MentatFlow;
    28	class MissionFlow;
    29	class cGameSettings;
    30	class cIni;
    31	class cMouse;
    32	class cGameObjectContext;
    33	
    34	enum class MentatMode {
    35	    Briefing,
    36	    WinBrief,
    37	    LoseBrief
    38	};
    39	
    40	class cMentatState : public cGameState {
    41	public:
    42	    cMentatState(sGameServices* services, MentatMode mode, cIni* cini, s_DataCampaign* dataCampaign);
    43	    ~cMentatState() override;
    44	
    45	    void thinkFast() override;
    46	    void draw() const override;
    47	
    48	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    49	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    50	
    51	    eGameStateType getType() override;
    52	    void loadScenario(cReinforcements *reinforcements);
    53	    void loadBriefing(int iScenarioFind, eScenarioIniSection iSectionFind);
    54	    void prepareMentat(int house);
    55	private:
    56	    std::unique_ptr<AbstractMentat> m_mentat;
    57	
    58	    s_DataCampaign* m_dataCampaign = nullptr;
    59	    cGameSettings* m_settings = nullptr;
    60	    ScenarioFlow* m_scenarioFlow = nullptr;
    61	    GameStateTransition* m_stateTransitions = nullptr;
    62	    MentatFlow* m_mentatFlow = nullptr;
    63	    MissionFlow* m_missionFlow = nullptr;
    64	    cMouse* m_mouse = nullptr;
    65	    cGameObjectContext* m_objects = nullptr;
    66	    cReinforcements* m_reinforcements = nullptr;
    67	    cIni* m_cIni = nullptr;
    68	    MentatMode m_mode;
    69	    int m_house;
    70	    bool m_allowMissionSelect;
    71	};
```

### src/gamestates/cTellHouseState.h@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.h | nl -ba
```

```text
     1	/**
     2	 * @file cTellHouseState.h
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
    19	#include "gameobjects/mentat/AbstractMentat.h"
    20	
    21	#include <memory>
    22	
    23	struct s_DataCampaign;
    24	class cMouse;
    25	class cIni;
    26	class AudioContext;
    27	class cGameSettings;
    28	class cPlayer;
    29	class GameStateTransition;
    30	class MissionFlow;
    31	
    32	class cTellHouseState : public cGameState {
    33	public:
    34	    cTellHouseState(sGameServices* services, cIni *ini, s_DataCampaign* dataCampaign);
    35	    ~cTellHouseState() override;
    36	
    37	    void thinkFast() override;
    38	    void draw() const override;
    39	
    40	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    41	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    42	
    43	    eGameStateType getType() override;
    44	    void prepareMentat(int house);
    45	
    46	private:
    47	    std::unique_ptr<AbstractMentat> m_mentat;
    48	    int m_house = -1;
    49	    s_DataCampaign* m_dataCampaign = nullptr;
    50	    cMouse* m_mouse = nullptr;
    51	    cIni* m_cIni = nullptr;
    52	    AudioContext* m_audioContext = nullptr;
    53	    cGameSettings* m_settings = nullptr;
    54	    GameStateTransition* m_stateTransitions = nullptr;
    55	    MissionFlow* m_missionFlow = nullptr;
    56	    cPlayer* m_humanPlayer = nullptr;
    57	};
```

### src/gamestates/cCreatorState.h@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.h | nl -ba
```

```text
     1	/**
     2	 * @file cCreatorState.h
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
    18	#include "include/eGameState.h"
    19	#include "gamestates/cGameState.h"
    20	#include "utils/cEnumArray.h"
    21	#include "include/sDataCampaign.h"
    22	
    23	#include <memory>
    24	#include <optional>
    25	#include <string>
    26	
    27	class GameContext;
    28	class GameStateTransition;
    29	class cIni;
    30	
    31	class cCreatorState {
    32	public:
    33	    explicit cCreatorState(sGameServices *services, cIni *ini, s_DataCampaign *dataCampaign);
    34	
    35	    ~cCreatorState();
    36	
    37	    cGameState *getState(eGameState gameState);
    38	
    39	    cGameState *getOrCreateState(eGameState gameState, bool forceRecreate = false);
    40	
    41	    [[nodiscard]] bool hasState(eGameState gameState) const;
    42	
    43	    // the video state needs to know what to play, so it has no createStateFromScratch case
    44	    void createVideoState(const std::string &filename);
    45	
    46	    void destroyState(eGameState gameState);
    47	
    48	    void destroyAllStates();
    49	
    50	private:
    51	    EnumArray<std::optional<std::unique_ptr<cGameState> >, eGameState> m_states;
    52	    sGameServices *m_services = nullptr;
    53	    s_DataCampaign *m_dataCampaign = nullptr;
    54	    GameStateTransition *m_stateTransitions = nullptr;
    55	    cIni *m_cIni = nullptr;
    56	
    57	    void createStateFromScratch(eGameState gameState);
    58	};
```

### src/gamestates/cGameState.h@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGameState.h | nl -ba
```

```text
     1	/**
     2	 * @file cGameState.h
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
    18	class cKeyboardEvent;
    19	#include "observers/cInputObserver.h"
    20	struct s_MouseEvent;
    21	struct s_GameEvent;
    22	struct sGameServices;
    23	
    24	class GameContext;
    25	class SDLDrawer;
    26	class cLog;
    27	
    28	enum eGameStateType {
    29	    GAMESTATE_CHOOSE_HOUSE,                 // #define GAME_SELECT_HOUSE  8		// pick a house
    30	    GAMESTATE_CREDITS,                      // #define GAME_CREDITS       17    // credits
    31	    GAMESTATE_EDITOR,                       // #define GAME_EDITOR      4      // running the editor
    32	    GAMESTATE_NEW_MAP_EDITOR,               // #define GAME_NEW_MAP_EDITOR 19    // new map editor
    33	    GAMESTATE_MAIN_MENU,                    // #define GAME_MENU          1     // in a menu    
    34	    GAMESTATE_MENTAT,                       // #define GAME_WINNING     11      // when winning, do some cool animation
    35	                                            // #define GAME_LOSEBRIEF   13      // briefing when losing
    36	                                            // #define GAME_BRIEFING     3      // doing some briefing
    37	    GAMESTATE_OPTIONS,                      // #define GAME_OPTIONS	      5     // options menu
    38	    GAMESTATE_PLAYING,                      // #define GAME_PLAYING      2      // playing the actual game
    39	    GAMESTATE_SCORING,                      // #define GAME_SCORING     20      // crude mission scoring screen, shown after winning
    40	    GAMESTATE_SELECT_MISSION,               // #define GAME_MISSIONSELECT 18    // mission select
    41	    GAMESTATE_SELECT_YOUR_NEXT_CONQUEST,    // #define GAME_REGION		  6	    // select a region / select your next conquest
    42	    GAMESTATE_SETUP_SKIRMISH,               // #define GAME_SETUPSKIRMISH 16    // set up a skirmish game
    43	    GAMESTATE_TELLHOUSE,                    // #define GAME_TELLHOUSE	10		// tell about the house
    44	    GAMESTATE_WINLOSE,                      // #define GAME_LOSING      14      // when losing, do something cool
    45	                                            // #define GAME_WINBRIEF    12      // mentat chatter when won the mission
    46	    GAMESTATE_VIDEO                         // playing a video
    47	};
    48	
    49	const char *gameStateTypeToString(eGameStateType state);
    50	// #define GAME_INITIALIZE  -1      // initialize game
    51	// #define GAME_OVER         0      // game over
    52	
    53	
    54	
    55	// #define GAME_INTRO	     9
    56	
    57	// #define GAME_SKIRMISH    15      // playing a skirmish mission!
    58	
    59	
    60	class cGameState : cInputObserver {
    61	
    62	public:
    63	    explicit cGameState(sGameServices* services);
    64	    virtual ~cGameState() = default;
    65	
    66	    virtual void thinkFast() = 0;
    67	    virtual void thinkNormal();
    68	    virtual void thinkSlow();
    69	    virtual void draw() const = 0;
    70	
    71	    virtual void onNotifyMouseEvent(const s_MouseEvent &event) override = 0;
    72	    virtual void onNotifyKeyboardEvent(const cKeyboardEvent &event) override = 0;
    73	    virtual void onNotifyGameEvent(const s_GameEvent &) {
    74	    }
    75	    virtual bool isKeyboardCapturedByUi() const {
    76	        return false;
    77	    }
    78	    // Do note: not every game state is a scenario observer!
    79	
    80	    virtual eGameStateType getType() = 0;
    81	    virtual void update();
    82	
    83	protected:
    84	    GameContext* m_ctx=nullptr;
    85	    SDLDrawer* m_sdlDrawer=nullptr;
    86	private:
    87	
    88	};
```

### src/gameobjects/mentat/AbstractMentat.cpp@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp | nl -ba
```

```text
     1	/**
     2	 * @file AbstractMentat.cpp
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
    16	#include "AbstractMentat.h"
    17	#include "definitions.h"
    18	#include "include/eGameState.h"
    19	#include "drawers/SDLDrawer.hpp"
    20	#include "utils/RNG.hpp"
    21	#include "context/GameContext.hpp"
    22	#include "game/GameStateTransition.hpp"
    23	#include "game/MentatFlow.hpp"
    24	#include "game/cGameSettings.h"
    25	#include "gui/GuiButton.h"
    26	#include "utils/Graphics.hpp"
    27	// #include "utils/common.h"
    28	#include "utils/Log.h"
    29	#include "drawers/cTextDrawer.h"
    30	
    31	#include <SDL3/SDL.h>
    32	#include <SDL3_ttf/SDL_ttf.h>
    33	#include <format>
    34	#include "include/cAssert.h"
    35	#include "context/GraphicsContext.hpp"
    36	#include "context/TextContext.hpp"
    37	#include "include/Texture.hpp"
    38	#include "utils/cRectangle.h"
    39	
    40	// The mentat screen artwork was designed for 640x480. On higher resolutions it
    41	// is centered, so the offset is half the extra pixels on each axis.
    42	static constexpr int MENTAT_SCREEN_W = 640;
    43	static constexpr int MENTAT_SCREEN_H = 480;
    44	
    45	AbstractMentat::AbstractMentat(GameContext* ctx, cGameSettings* settings, GameStateTransition* stateTransitions, MentatFlow* mentatFlow, bool canMissionSelect)
    46	{
    47	    d2tm_assert(ctx != nullptr);
    48	    d2tm_assert(settings != nullptr);
    49	    m_stateTransitions = stateTransitions;
    50	    d2tm_assert(m_stateTransitions != nullptr);
    51	    m_mentatFlow = mentatFlow;
    52	    gfxmentat = ctx->getGraphicsContext()->gfxmentat.get();
    53	    m_textDrawer = ctx->getTextContext()->getBeneTextDrawer();
    54	    m_sdlDrawer = ctx->getSDLDrawer();
    55	    iMentatSentence = -1;
    56	
    57	    TIMER_Speaking = -1;
    58	    TIMER_Mouth = 0;
    59	    TIMER_Eyes = 0;
    60	    TIMER_Other = 0;
    61	    TIMER_movie = 0;
    62	
    63	    iMentatMouth = 3;
    64	    iMentatEyes = 3;
    65	    iMovieFrame = -1;
    66	
    67	    iBackgroundFrame = -1;
    68	
    69	    house = GENERALHOUSE;
    70	
    71	    gfxmovie = nullptr;
    72	    leftButton = nullptr;
    73	    rightButton = nullptr;
    74	    // the mentat does not *own* the bitmaps
    75	    leftButtonBmp = nullptr;
    76	    rightButtonBmp = nullptr;
    77	    leftGuiButton = nullptr;
    78	    rightGuiButton = nullptr;
    79	
    80	    if (canMissionSelect) {
    81	
    82	        int length = m_textDrawer->getTextLength("Mission select");
    83	        const cRectangle &toMissionSelectRect = m_textDrawer->getAsRectangle(settings->getScreenW() - length,
    84	                                                settings->getScreenH() - m_textDrawer->getFontHeight(),
    85	                                                "Mission select");
    86	
    87	        auto gui_btn_toMissionSelect = GuiButtonBuilder()
    88	            .withRect(toMissionSelectRect)
    89	            .withLabel("Mission select")
    90	            .withTextDrawer(m_textDrawer)
    91	            .withRenderer(m_sdlDrawer)
    92	            .withTheme(cGuiThemeBuilder().light().build())
    93	            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
    94	            .onClick([this] {
    95	                m_stateTransitions->setNextState(GAME_MISSIONSELECT);
    96	            })
    97	            .build();
    98	        m_guiBtnToMissionSelect = std::move(gui_btn_toMissionSelect);
    99	    }
   100	    else {
   101	        m_guiBtnToMissionSelect = nullptr;
   102	    }
   103	
   104	    state = INIT;
   105	
   106	    offsetX = (settings->getScreenW() - MENTAT_SCREEN_W) / 2;
   107	    offsetY = (settings->getScreenH() - MENTAT_SCREEN_H) / 2;
   108	    movieTopleftX = offsetX + 256;
   109	    movieTopleftY = offsetY + 120;
   110	    Logger::info(COMP_GAME, "AbstractMentat::AbstractMentat", "Initialized AbstractMentat with mission select button: {}", canMissionSelect);
   111	}
   112	
   113	AbstractMentat::~AbstractMentat()
   114	{
   115	    leftButtonBmp = nullptr;
   116	    rightButtonBmp = nullptr;
   117	    // m_guiBtnToMissionSelect will be a unique_ptr, auto-cleaned
   118	    Logger::info(COMP_GAME, "AbstractMentat::~AbstractMentat", "Destroying AbstractMentat");
   119	}
   120	
   121	void AbstractMentat::think()
   122	{
   123	    if (state == INIT) {
   124	        // no thinking for init state
   125	        return;
   126	    }
   127	
   128	    if (state == SPEAKING) {
   129	        if (TIMER_Speaking > 0) {
   130	            TIMER_Speaking--;
   131	        }
   132	        else if (TIMER_Speaking == 0) {
   133	            // calculate speaking stuff
   134	            iMentatSentence += 2; // makes 0, 2, etc.
   135	
   136	            // done talking
   137	            if (iMentatSentence > 8) {
   138	                state = AWAITING_RESPONSE;
   139	                return;
   140	            }
   141	
   142	            // lentgh calculation of time
   143	            int iLength = static_cast<int>(sentence[iMentatSentence].size());
   144	            iLength += static_cast<int>(sentence[iMentatSentence + 1].size());
   145	
   146	            // nothing to say, await response
   147	            if (iLength < 2) {
   148	                state = AWAITING_RESPONSE;
   149	                return;
   150	            }
   151	
   152	            TIMER_Speaking = iLength * 12;
   153	        }
   154	
   155	        thinkMouth();
   156	    }
   157	    else {
   158	        iMentatMouth = 0; // keep lips sealed
   159	    }
   160	
   161	    // eyes blink always
   162	    thinkEyes();
   163	
   164	    // regardless, think about movie animation
   165	    thinkMovie();
   166	}
   167	
   168	void AbstractMentat::thinkMovie()
   169	{
   170	    if (gfxmovie != nullptr) {
   171	        TIMER_movie++;
   172	
   173	        if (TIMER_movie > 20) {
   174	            iMovieFrame++;
   175	
   176	            if (iMovieFrame == gfxmovie->getNumberOfFiles()) {
   177	                iMovieFrame = 0;
   178	            }
   179	            TIMER_movie = 0;
   180	        }
   181	    }
   182	}
   183	
   184	void AbstractMentat::thinkEyes()
   185	{
   186	    if (TIMER_Eyes > 0) {
   187	        TIMER_Eyes--;
   188	    }
   189	    else {
   190	        int i = RNG::rnd(100);
   191	
   192	        int iWas = iMentatEyes;
   193	
   194	        if (i < 30) {
   195	            iMentatEyes = 3;
   196	        }
   197	        else if (i < 60) {
   198	            iMentatEyes = 0;
   199	        }
   200	        else {
   201	            iMentatEyes = 4;
   202	        }
   203	
   204	        // its the same
   205	        if (iMentatEyes == iWas) {
   206	            iMentatEyes = RNG::rnd(4);
   207	        }
   208	
   209	        if (iMentatEyes != 4) {
   210	            TIMER_Eyes = 90 + RNG::rnd(160);
   211	        }
   212	        else {
   213	            TIMER_Eyes = 30;
   214	        }
   215	    }
   216	}
   217	
   218	void AbstractMentat::thinkMouth()  // MOUTH
   219	{
   220	    if (TIMER_Mouth > 0) {
   221	        TIMER_Mouth--;
   222	    }
   223	    else {
   224	        // still speaking
   225	        if (TIMER_Speaking > 0) {
   226	
   227	            int iOld = iMentatMouth;
   228	
   229	            if (iMentatMouth == 0) { // mouth is shut
   230	                // when mouth is shut, we wait a bit.
   231	                if (RNG::rnd(100) < 45) {
   232	                    iMentatMouth += (1 + RNG::rnd(4));
   233	                }
   234	                else {
   235	                    TIMER_Mouth = 25; // wait
   236	                }
   237	            }
   238	            else {
   239	                iMentatMouth += (1 + RNG::rnd(4));
   240	            }
   241	
   242	            // correct any frame
   243	            if (iMentatMouth > 4) {
   244	                iMentatMouth -= 5;
   245	            }
   246	
   247	            // Test if we did not set the timer, when not, we changed stuff, and we
   248	            // have to make sure we do not reshow the same animation.. which looks
   249	            // odd!
   250	            if (TIMER_Mouth <= 0) {
   251	                // did not change mouth, force it
   252	                if (iMentatMouth == iOld) {
   253	                    iMentatMouth++;
   254	                }
   255	
   256	                // correct if needed:
   257	                if (iMentatMouth > 4) {
   258	                    iMentatMouth -= 5;
   259	                }
   260	            }
   261	        }
   262	        else {
   263	            iMentatMouth = 0; // when there is no sentence, do not animate mouth
   264	        }
   265	
   266	        if (TIMER_Mouth <= 0) {
   267	            TIMER_Mouth = 13 + RNG::rnd(15);
   268	        }
   269	    } // Animating mouth
   270	
   271	}
   272	
   273	void AbstractMentat::draw()
   274	{
   275	    m_sdlDrawer->renderClearToColor(Color{7,7,15,255});
   276	    m_sdlDrawer->renderRectColor(offsetX-1, offsetY-1, 641, 481, Color{64, 64,89,255});
   277	    m_sdlDrawer->renderRectColor(offsetX-2, offsetY-2, 642, 482, Color{40,40,60,255});
   278	    m_sdlDrawer->renderRectColor(offsetX-3, offsetY-3, 643, 483, Color{0,0,0,255});
   279	
   280	    // movie
   281	    draw_movie();
   282	
   283	    Texture *tmp = getBackgroundBitmap();
   284	    cRectangle dest = {offsetX, offsetY, MENTAT_SCREEN_W, MENTAT_SCREEN_H};
   285	    m_sdlDrawer->renderStrechFullSprite(tmp, dest);
   286	
   287	    draw_eyes();
   288	    draw_mouth();
   289	    draw_other();
   290	
   291	    if (state == SPEAKING) {
   292	        // draw text that is being spoken
   293	        if (iMentatSentence >= 0) {
   294	            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{0, 0, 0,255},sentence[iMentatSentence]);
   295	            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{255, 255, 255,255},sentence[iMentatSentence]);
   296	
   297	            m_textDrawer->drawText(offsetX + 17, offsetY + 37,Color{0, 0, 0,255},sentence[iMentatSentence+1]);
   298	            m_textDrawer->drawText(offsetX + 17, offsetY + 36,Color{255, 255, 255,255},sentence[iMentatSentence+1]);
   299	        }
   300	    }
   301	
   302	    if (state == AWAITING_RESPONSE) {
   303	        if (leftGuiButton) {
   304	            leftGuiButton->draw();
   305	        }
   306	        if (rightGuiButton){
   307	            rightGuiButton->draw();
   308	        }
   309	    }
   310	
   311	    if (m_guiBtnToMissionSelect) {
   312	        m_guiBtnToMissionSelect->draw();
   313	    }
   314	}
   315	
   316	Texture *AbstractMentat::getBackgroundBitmap() const
   317	{
   318	    if (iBackgroundFrame < 0) return nullptr;
   319	    return gfxmentat->getTexture(iBackgroundFrame);
   320	}
   321	
   322	void AbstractMentat::draw_movie()
   323	{
   324	    if (gfxmovie == nullptr) return;
   325	    if (iMovieFrame < 0) return;
   326	
   327	    // drawing only, circulating is done in think function
   328	    Texture *tmp = gfxmovie->getTexture(iMovieFrame);
   329	    cRectangle dest = {movieTopleftX, movieTopleftY,tmp->w, tmp->h};
   330	    m_sdlDrawer->renderStrechFullSprite(tmp, dest);
   331	}
   332	
   333	void AbstractMentat::initSentences()
   334	{
   335	    for (auto &line : sentence) {
   336	        line.clear();
   337	    }
   338	}
   339	
   340	void AbstractMentat::setSentence(int i, const std::string &text)
   341	{
   342	    sentence[i] = text.substr(0, 254); // the old char buffer held at most 254 characters
   343	    Logger::info(COMP_GAME, "AbstractMentat::setSentence", "Sentence[{}]={}", i, text);
   344	}
   345	
   346	void AbstractMentat::loadScene(const std::string &scene)
   347	{
   348	    gfxmovie = nullptr;
   349	
   350	    const std::string filename = hd4SceneFile(scene);
   351	
   352	    gfxmovie = std::make_shared<Graphics>(m_sdlDrawer->getRenderer(),filename, kHd4AssetDensity);
   353	
   354	    TIMER_movie = 0;
   355	    iMovieFrame=0;
   356	
   357	    if (gfxmovie != nullptr) {
   358	        Logger::info(COMP_GAME, "AbstractMentat", "Successful loaded scene [{}]", filename);
   359	        return;
   360	    }
   361	
   362	    gfxmovie=nullptr;
   363	    Logger::error(COMP_GAME, "AbstractMentat", "Failed to load scene [{}]", filename);
   364	}
   365	
   366	void AbstractMentat::speak()
   367	{
   368	    TIMER_Speaking = 0;
   369	    TIMER_Mouth = 0;
   370	    iMentatSentence = -2; // ugh
   371	    state = SPEAKING;
   372	}
   373	
   374	void AbstractMentat::buildLeftButton(Texture *bmp, int x, int y)
   375	{
   376	    leftButton = std::make_unique<cRectangle>(offsetX + x, offsetY + y, bmp->w, bmp->h);
   377	    leftButtonBmp = bmp;
   378	}
   379	
   380	void AbstractMentat::buildRightButton(Texture *bmp, int x, int y)
   381	{
   382	    rightButton = std::make_unique<cRectangle>(offsetX + x, offsetY + y, bmp->w, bmp->h);
   383	    rightButtonBmp = bmp;
   384	}
   385	
   386	void AbstractMentat::resetSpeak()
   387	{
   388	    speak();
   389	}
   390	
   391	void AbstractMentat::onNotifyMouseEvent(const s_MouseEvent &event)
   392	{
   393	    // Always keep button hover state current so focus is correct when buttons re-appear
   394	    if (event.eventType == MOUSE_MOVED_TO) {
   395	        if (m_guiBtnToMissionSelect) {
   396	            m_guiBtnToMissionSelect->onNotifyMouseEvent(event);
   397	        }
   398	        if (leftGuiButton) {
   399	            leftGuiButton->onNotifyMouseEvent(event);
   400	        }
   401	        if (rightGuiButton) {
   402	            rightGuiButton->onNotifyMouseEvent(event);
   403	        }
   404	        return;
   405	    }
   406	
   407	    if (state == SPEAKING) {
   408	        if (m_guiBtnToMissionSelect) {
   409	            m_guiBtnToMissionSelect->onNotifyMouseEvent(event);
   410	        }
   411	        if (event.eventType == MOUSE_LEFT_BUTTON_CLICKED) {
   412	            if (TIMER_Speaking > 0) {
   413	                TIMER_Speaking = 1;
   414	            }
   415	        }
   416	    }
   417	
   418	    if (state == AWAITING_RESPONSE) {
   419	        if (m_guiBtnToMissionSelect) {
   420	            m_guiBtnToMissionSelect->onNotifyMouseEvent(event);
   421	        }
   422	        if (leftGuiButton) {
   423	            leftGuiButton->onNotifyMouseEvent(event);
   424	        }
   425	        if (rightGuiButton) {
   426	            rightGuiButton->onNotifyMouseEvent(event);
   427	        }
   428	    }
   429	}
   430	
   431	void AbstractMentat::onNotifyKeyboardEvent(const cKeyboardEvent &event)
   432	{
   433	    if (m_guiBtnToMissionSelect) {
   434	        m_guiBtnToMissionSelect->onNotifyKeyboardEvent(event);
   435	    }
   436	}
```

### src/include/sDataCampaign.h@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/sDataCampaign.h | nl -ba
```

```text
     1	/**
     2	 * @file sDataCampaign.h
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
    18	static constexpr int LAST_CAMPAIGN_MISSION = 9;
    19	
    20	struct s_DataCampaign {
    21	    int housePlayer;
    22	    int region;                   // what region is selected?
    23	    int mission;		            // what mission are we playing?
    24	};
```

### src/include/sGameServices.h@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/sGameServices.h | nl -ba
```

```text
     1	/**
     2	 * @file sGameServices.h
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
    18	class GameContext;
    19	class cGameObjectContext;
    20	class cInfoContext;
    21	class cGameSettings;
    22	class cLog;
    23	class cMapCamera;
    24	class cStructureUtils;
    25	class cEventEmitter;
    26	class cDrawManager;
    27	class cRectangle;
    28	class cReinforcements;
    29	class cMouse;
    30	class cMissionStatsCollector;
    31	class cGameConditionChecker;
    32	class cScreenShake;
    33	class cScreenFader;
    34	class CampaignProgress;
    35	class Texture;
    36	class GameStateTransition;
    37	class MentatFlow;
    38	class MissionFlow;
    39	class ScenarioFlow;
    40	class VideoFlow;
    41	
    42	struct sGameServices
    43	{
    44	    GameContext *ctx = nullptr;
    45	    cGameObjectContext *objects = nullptr;
    46	    cInfoContext *info = nullptr;
    47	    cGameSettings *settings = nullptr;
    48	    cMapCamera *mapCamera = nullptr;
    49	    cStructureUtils *structureUtils = nullptr;
    50	    cEventEmitter *eventEmitter = nullptr;
    51	    cDrawManager *drawManager = nullptr;
    52	    cRectangle *mapViewport = nullptr;
    53	    cReinforcements *reinforcements = nullptr;
    54	    cMouse *mouse = nullptr;
    55	    cMissionStatsCollector *missionStatsCollector = nullptr;
    56	    cGameConditionChecker *gameConditionChecker = nullptr;
    57	    cScreenShake *screenShake = nullptr;
    58	    cScreenFader *screenFader = nullptr;
    59	    CampaignProgress *campaignProgress = nullptr;
    60	    Texture *screenTexture = nullptr; // set in cGame::run(), before any state transition
    61	    GameStateTransition *stateTransitions = nullptr;
    62	    MentatFlow *mentatFlow = nullptr;
    63	    MissionFlow *missionFlow = nullptr;
    64	    ScenarioFlow *scenarioFlow = nullptr;
    65	    VideoFlow *videoFlow = nullptr;
    66	};
```

### src/game/CampaignProgress.hpp@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.hpp | nl -ba
```

```text
     1	/**
     2	 * @file CampaignProgress.hpp
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
    18	#include <array>
    19	#include <cstddef>
    20	#include <filesystem>
    21	#include <string>
    22	
    23	enum class CampaignProgressLoadResult {
    24	    NotFound,
    25	    Loaded,
    26	    Invalid
    27	};
    28	
    29	class CampaignProgress {
    30	public:
    31	    static constexpr int FIRST_MISSION = 1;
    32	    static constexpr int LAST_MISSION = 9;
    33	    static constexpr int COMPLETED = LAST_MISSION + 1;
    34	
    35	    explicit CampaignProgress(std::filesystem::path filePath);
    36	
    37	    CampaignProgressLoadResult load(std::string& error);
    38	    bool save(std::string& error) const;
    39	
    40	    int nextMission(int house) const;
    41	    int highestUnlockedMission(int house) const;
    42	    static bool supportsHouse(int house);
    43	    bool markStarted(int house);
    44	    bool recordMissionVictory(int house, int mission);
    45	
    46	private:
    47	    static std::size_t houseIndex(int house);
    48	
    49	    std::filesystem::path m_filePath;
    50	    std::array<int, 4> m_nextMission{};
    51	};
```

### src/game/MentatFlow.hpp@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/MentatFlow.hpp | nl -ba
```

```text
     1	/**
     2	 * @file MentatFlow.hpp
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
    18	#include <functional>
    19	#include <utility>
    20	
    21	/**
    22	 * Narrow entry point to the mentat related flow of the game (preparing the mentat, leaving it).
    23	 * Holds callbacks so it does not depend on cGame.
    24	 */
    25	class MentatFlow {
    26	public:
    27	    using HouseCallback = std::function<void(int)>;
    28	    using Callback = std::function<void()>;
    29	
    30	    MentatFlow(HouseCallback prepareToTellAboutHouse, Callback prepareForPlayer, Callback leave)
    31	        : m_prepareToTellAboutHouse(std::move(prepareToTellAboutHouse)),
    32	          m_prepareForPlayer(std::move(prepareForPlayer)),
    33	          m_leave(std::move(leave)) {
    34	    }
    35	
    36	    void prepareToTellAboutHouse(int house) const {
    37	        m_prepareToTellAboutHouse(house);
    38	    }
    39	
    40	    void prepareForPlayer() const {
    41	        m_prepareForPlayer();
    42	    }
    43	
    44	    void leave() const {
    45	        m_leave();
    46	    }
    47	
    48	private:
    49	    HouseCallback m_prepareToTellAboutHouse;
    50	    Callback m_prepareForPlayer;
    51	    Callback m_leave;
    52	};
```

### src/game/MissionFlow.hpp@acddd29

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/MissionFlow.hpp | nl -ba
```

```text
     1	/**
     2	 * @file MissionFlow.hpp
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
    18	#include <functional>
    19	#include <utility>
    20	
    21	/**
    22	 * Narrow entry point to the mission related flow of the game (initializing, winning, losing, jumping to a mission).
    23	 * Holds callbacks so it does not depend on cGame.
    24	 */
    25	class MissionFlow {
    26	public:
    27	    using Callback = std::function<void()>;
    28	    using IntCallback = std::function<void(int)>;
    29	
    30	    MissionFlow(Callback init, Callback setWon, Callback setLost, Callback checkWinOrFail,
    31	                IntCallback jumpToSelectYourNextConquest, IntCallback goingToWinLoseBrief)
    32	        : m_init(std::move(init)),
    33	          m_setWon(std::move(setWon)),
    34	          m_setLost(std::move(setLost)),
    35	          m_checkWinOrFail(std::move(checkWinOrFail)),
    36	          m_jumpToSelectYourNextConquest(std::move(jumpToSelectYourNextConquest)),
    37	          m_goingToWinLoseBrief(std::move(goingToWinLoseBrief)) {
    38	    }
    39	
    40	    void init() const {
    41	        m_init();
    42	    }
    43	
    44	    void setWon() const {
    45	        m_setWon();
    46	    }
    47	
    48	    void setLost() const {
    49	        m_setLost();
    50	    }
    51	
    52	    void checkWinOrFail() const {
    53	        m_checkWinOrFail();
    54	    }
    55	
    56	    void jumpToSelectYourNextConquest(int mission) const {
    57	        m_jumpToSelectYourNextConquest(mission);
    58	    }
    59	
    60	    void goingToWinLoseBrief(int winOrLoseBrief) const {
    61	        m_goingToWinLoseBrief(winOrLoseBrief);
    62	    }
    63	
    64	private:
    65	    Callback m_init;
    66	    Callback m_setWon;
    67	    Callback m_setLost;
    68	    Callback m_checkWinOrFail;
    69	    IntCallback m_jumpToSelectYourNextConquest;
    70	    IntCallback m_goingToWinLoseBrief;
    71	};
```

### Определения `cMentatState` и `cTellHouseState`

```sh
git grep -n -E '^(.*[ *&])?(cMentatState|cTellHouseState)::[A-Za-z_~]+\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:38:cMentatState::cMentatState(sGameServices* services, MentatMode mode, cIni* cini, s_DataCampaign* dataCampaign)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:67:cMentatState::~cMentatState()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:70:eGameStateType cMentatState::getType()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:75:void cMentatState::prepareMentat(int house)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:139:void cMentatState::thinkFast()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:144:void cMentatState::draw() const
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:151:void cMentatState::onNotifyMouseEvent(const s_MouseEvent &event)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:156:void cMentatState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:161:void cMentatState::loadScenario(cReinforcements *reinforcements)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:166:void cMentatState::loadBriefing(int iScenarioFind, eScenarioIniSection iSectionFind)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:34:cTellHouseState::cTellHouseState(sGameServices* services, cIni *ini, s_DataCampaign* dataCampaign)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:56:cTellHouseState::~cTellHouseState()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:59:eGameStateType cTellHouseState::getType()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:64:void cTellHouseState::prepareMentat(int house)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:93:void cTellHouseState::thinkFast()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:98:void cTellHouseState::draw() const
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:105:void cTellHouseState::onNotifyMouseEvent(const s_MouseEvent &event)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:110:void cTellHouseState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
```

### cMentatState::cMentatState — src/gamestates/cMentatState.cpp@acddd29:38-65

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '38,65p'
```

```text
    38	cMentatState::cMentatState(sGameServices* services, MentatMode mode, cIni* cini, s_DataCampaign* dataCampaign)
    39	    : cGameState(services),
    40	      m_dataCampaign(dataCampaign),
    41	      m_settings(services->settings),
    42	      m_scenarioFlow(services->scenarioFlow),
    43	      m_stateTransitions(services->stateTransitions),
    44	      m_mentatFlow(services->mentatFlow),
    45	      m_missionFlow(services->missionFlow),
    46	      m_mouse(services->mouse),
    47	      m_objects(services->objects),
    48	      m_reinforcements(services->reinforcements),
    49	      m_cIni(cini),
    50	      m_mode(mode),
    51	      m_house(dataCampaign->housePlayer),
    52	      m_allowMissionSelect(false)
    53	{
    54	    d2tm_assert(services != nullptr);
    55	    d2tm_assert(m_dataCampaign != nullptr);
    56	    d2tm_assert(m_settings != nullptr);
    57	    d2tm_assert(m_scenarioFlow != nullptr);
    58	    d2tm_assert(m_stateTransitions != nullptr);
    59	    d2tm_assert(m_mentatFlow != nullptr);
    60	    d2tm_assert(m_missionFlow != nullptr);
    61	    d2tm_assert(m_objects != nullptr);
    62	    d2tm_assert(m_reinforcements != nullptr);
    63	    d2tm_assert(m_cIni != nullptr);
    64	    prepareMentat(m_house);
    65	}
```

### cMentatState::~cMentatState — src/gamestates/cMentatState.cpp@acddd29:67-73

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '67,73p'
```

```text
    67	cMentatState::~cMentatState()
    68	{}
    69	
    70	eGameStateType cMentatState::getType()
    71	{
    72	    return eGameStateType::GAMESTATE_MENTAT;
    73	}
```

### cMentatState::getType — src/gamestates/cMentatState.cpp@acddd29:70-73

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '70,73p'
```

```text
    70	eGameStateType cMentatState::getType()
    71	{
    72	    return eGameStateType::GAMESTATE_MENTAT;
    73	}
```

### cMentatState::prepareMentat — src/gamestates/cMentatState.cpp@acddd29:75-137

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '75,137p'
```

```text
    75	void cMentatState::prepareMentat(int house)
    76	{
    77	    // this state is cached, so decide per use (not at construction) whether a skirmish game is active
    78	    m_allowMissionSelect = !m_settings->isSkirmish();
    79	    auto* humanPlayer = m_objects->getPlayer(HUMAN);
    80	    house = (m_house > GENERALHOUSE) ? m_house : humanPlayer->getHouse();
    81	    switch (m_mode) {
    82	        case MentatMode::Briefing:
    83	            if (house == ATREIDES)
    84	                m_mentat = std::make_unique<AtreidesMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
    85	            else if (house == HARKONNEN)
    86	                m_mentat = std::make_unique<HarkonnenMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
    87	            else if (house == ORDOS)
    88	                m_mentat = std::make_unique<OrdosMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
    89	            else if (house == SARDAUKAR)
    90	                m_mentat = std::make_unique<SardaukarMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
    91	            else 
    92	                m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, humanPlayer, m_dataCampaign);
    93	            m_missionFlow->init();
    94	            m_scenarioFlow->setupPlayers();
    95	            m_cIni->loadScenario(m_mentat.get(), m_reinforcements,m_dataCampaign);
    96	            m_cIni->loadBriefing(house, m_dataCampaign->region, eScenarioIniSection::BRIEFING, m_mentat.get());
    97	            break;
    98	        case MentatMode::WinBrief:
    99	            if (house == ATREIDES)
   100	                m_mentat = std::make_unique<AtreidesMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   101	            else if (house == HARKONNEN)
   102	                m_mentat = std::make_unique<HarkonnenMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   103	            else if (house == ORDOS) 
   104	                m_mentat = std::make_unique<OrdosMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   105	            else if (house == SARDAUKAR)
   106	                m_mentat = std::make_unique<SardaukarMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   107	            else 
   108	                m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, humanPlayer, m_dataCampaign);
   109	            
   110	            if (RNG::rnd(100) < 50)
   111	                m_mentat->loadScene("win01");
   112	            else
   113	                m_mentat->loadScene("win02");
   114	            m_cIni->loadBriefing(house, m_dataCampaign->region, eScenarioIniSection::WIN, m_mentat.get());
   115	            break;
   116	        case MentatMode::LoseBrief:
   117	            if (house == ATREIDES) 
   118	                m_mentat = std::make_unique<AtreidesMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   119	            else if (house == HARKONNEN)
   120	                m_mentat = std::make_unique<HarkonnenMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   121	            else if (house == ORDOS)
   122	                m_mentat = std::make_unique<OrdosMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   123	            else if (house == SARDAUKAR)
   124	                m_mentat = std::make_unique<SardaukarMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
   125	            else 
   126	                m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, humanPlayer, m_dataCampaign);
   127	            
   128	            if (RNG::rnd(100) < 50)
   129	                m_mentat->loadScene("lose01");
   130	            else
   131	                m_mentat->loadScene("lose02");
   132	            
   133	            m_cIni->loadBriefing(house, m_dataCampaign->region, eScenarioIniSection::LOSE, m_mentat.get());
   134	            break;
   135	    }
   136	    m_mentat->speak();
   137	}
```

### cMentatState::thinkFast — src/gamestates/cMentatState.cpp@acddd29:139-142

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '139,142p'
```

```text
   139	void cMentatState::thinkFast()
   140	{
   141	    if (m_mentat) m_mentat->think();
   142	}
```

### cMentatState::draw — src/gamestates/cMentatState.cpp@acddd29:144-149

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '144,149p'
```

```text
   144	void cMentatState::draw() const
   145	{
   146	    m_mouse->setTile(MOUSE_NORMAL);
   147	    if (m_mentat) m_mentat->draw();
   148	    m_mouse->draw();
   149	}
```

### cMentatState::onNotifyMouseEvent — src/gamestates/cMentatState.cpp@acddd29:151-154

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '151,154p'
```

```text
   151	void cMentatState::onNotifyMouseEvent(const s_MouseEvent &event)
   152	{
   153	    if (m_mentat) m_mentat->onNotifyMouseEvent(event);
   154	}
```

### cMentatState::onNotifyKeyboardEvent — src/gamestates/cMentatState.cpp@acddd29:156-159

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '156,159p'
```

```text
   156	void cMentatState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
   157	{
   158	    if (m_mentat) m_mentat->onNotifyKeyboardEvent(event);
   159	}
```

### cMentatState::loadScenario — src/gamestates/cMentatState.cpp@acddd29:161-164

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '161,164p'
```

```text
   161	void cMentatState::loadScenario(cReinforcements *reinforcements)
   162	{
   163	    m_cIni->loadScenario(m_mentat.get(), reinforcements, m_dataCampaign);
   164	}
```

### cMentatState::loadBriefing — src/gamestates/cMentatState.cpp@acddd29:166-169

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | nl -ba | sed -n '166,169p'
```

```text
   166	void cMentatState::loadBriefing(int iScenarioFind, eScenarioIniSection iSectionFind)
   167	{
   168	    m_cIni->loadBriefing(m_dataCampaign->housePlayer, iScenarioFind, iSectionFind, m_mentat.get());
   169	}
```

### cTellHouseState::cTellHouseState — src/gamestates/cTellHouseState.cpp@acddd29:34-54

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '34,54p'
```

```text
    34	cTellHouseState::cTellHouseState(sGameServices* services, cIni *ini, s_DataCampaign* dataCampaign)
    35	    : cGameState(services),
    36	    m_house(dataCampaign->housePlayer),
    37	    m_dataCampaign(dataCampaign),
    38	    m_cIni(ini)
    39	{
    40	    d2tm_assert(services != nullptr);
    41	    d2tm_assert(m_cIni != nullptr);
    42	    d2tm_assert(dataCampaign != nullptr);
    43	    m_mouse = services->mouse;
    44	    d2tm_assert(m_mouse != nullptr);
    45	    m_audioContext = services->ctx->getAudioContext();
    46	    m_settings = services->settings;
    47	    m_stateTransitions = services->stateTransitions;
    48	    d2tm_assert(m_stateTransitions != nullptr);
    49	    m_missionFlow = services->missionFlow;
    50	    d2tm_assert(m_missionFlow != nullptr);
    51	    d2tm_assert(m_settings != nullptr);
    52	    m_humanPlayer = services->objects->getPlayer(HUMAN);
    53	    prepareMentat(m_house);
    54	}
```

### cTellHouseState::~cTellHouseState — src/gamestates/cTellHouseState.cpp@acddd29:56-62

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '56,62p'
```

```text
    56	cTellHouseState::~cTellHouseState()
    57	{}
    58	
    59	eGameStateType cTellHouseState::getType()
    60	{
    61	     return eGameStateType::GAMESTATE_TELLHOUSE; 
    62	}
```

### cTellHouseState::getType — src/gamestates/cTellHouseState.cpp@acddd29:59-62

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '59,62p'
```

```text
    59	eGameStateType cTellHouseState::getType()
    60	{
    61	     return eGameStateType::GAMESTATE_TELLHOUSE; 
    62	}
```

### cTellHouseState::prepareMentat — src/gamestates/cTellHouseState.cpp@acddd29:64-91

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '64,91p'
```

```text
    64	void cTellHouseState::prepareMentat(int house)
    65	{
    66	    m_house = house;
    67	    m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, m_humanPlayer, m_dataCampaign);
    68	    m_mentat->setHouse(house);
    69	
    70	    if (house == ATREIDES) {
    71	        m_audioContext->playSound(SOUND_ATREIDES);
    72	        m_cIni->loadBriefing(ATREIDES, 0, eScenarioIniSection::DESCRIPTION, m_mentat.get());
    73	        m_mentat->loadScene("platr");
    74	    } else if (house == HARKONNEN) {
    75	        m_audioContext->playSound(SOUND_HARKONNEN);
    76	        m_cIni->loadBriefing(HARKONNEN, 0, eScenarioIniSection::DESCRIPTION, m_mentat.get());
    77	        m_mentat->loadScene("plhar");
    78	    } else if (house == ORDOS) {
    79	        m_audioContext->playSound(SOUND_ORDOS);
    80	        m_cIni->loadBriefing(ORDOS, 0, eScenarioIniSection::DESCRIPTION, m_mentat.get());
    81	        m_mentat->loadScene("plord");
    82	    } else if (house == SARDAUKAR) {
    83	        //m_audioContext->playSound(SOUND_SARDAUKAR);
    84	        m_cIni->loadBriefing(SARDAUKAR, 0, eScenarioIniSection::DESCRIPTION, m_mentat.get());
    85	        //m_mentat->loadScene("plsar");
    86	    } else {
    87	        Logger::warn(COMP_GAMERULES, "cTellHouseState::prepareMentat", "called with an invalid house value: {}", house);
    88	        m_mentat->setSentence(0, "Looks like you choose an unknown house");
    89	    }
    90	    m_mentat->speak();
    91	}
```

### cTellHouseState::thinkFast — src/gamestates/cTellHouseState.cpp@acddd29:93-96

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '93,96p'
```

```text
    93	void cTellHouseState::thinkFast()
    94	{
    95	    if (m_mentat) m_mentat->think();
    96	}
```

### cTellHouseState::draw — src/gamestates/cTellHouseState.cpp@acddd29:98-103

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '98,103p'
```

```text
    98	void cTellHouseState::draw() const
    99	{
   100	    m_mouse->setTile(MOUSE_NORMAL);
   101	    if (m_mentat) m_mentat->draw();
   102	    m_mouse->draw();
   103	}
```

### cTellHouseState::onNotifyMouseEvent — src/gamestates/cTellHouseState.cpp@acddd29:105-108

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '105,108p'
```

```text
   105	void cTellHouseState::onNotifyMouseEvent(const s_MouseEvent &event)
   106	{
   107	    if (m_mentat) m_mentat->onNotifyMouseEvent(event);
   108	}
```

### cTellHouseState::onNotifyKeyboardEvent — src/gamestates/cTellHouseState.cpp@acddd29:110-113

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp | nl -ba | sed -n '110,113p'
```

```text
   110	void cTellHouseState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
   111	{
   112	    if (m_mentat) m_mentat->onNotifyKeyboardEvent(event);
   113	}
```

### Определение `cCreatorState::getOrCreateState`

```sh
git grep -n -E '^(.*[ *&])?cCreatorState::getOrCreateState\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.cpp:66:cGameState *cCreatorState::getOrCreateState(eGameState gameState, bool forceRecreate) {
```

### cCreatorState::getOrCreateState — src/gamestates/cCreatorState.cpp@acddd29:66-75

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '66,75p'
```

```text
    66	cGameState *cCreatorState::getOrCreateState(eGameState gameState, bool forceRecreate) {
    67	
    68	    if (!hasState(gameState)) {
    69	        createStateFromScratch(gameState);
    70	    } else if (forceRecreate) {
    71	        createStateFromScratch(gameState);
    72	    }
    73	
    74	    return m_states[gameState].value().get();
    75	}
```

### Определение `cCreatorState::getState`

```sh
git grep -n -E '^(.*[ *&])?cCreatorState::getState\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.cpp:62:cGameState *cCreatorState::getState(eGameState gameState) {
```

### cCreatorState::getState — src/gamestates/cCreatorState.cpp@acddd29:62-64

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '62,64p'
```

```text
    62	cGameState *cCreatorState::getState(eGameState gameState) {
    63	    return getOrCreateState(gameState, false);
    64	}
```

### Определение `cCreatorState::hasState`

```sh
git grep -n -E '^(.*[ *&])?cCreatorState::hasState\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.cpp:77:bool cCreatorState::hasState(eGameState gameState) const {
```

### cCreatorState::hasState — src/gamestates/cCreatorState.cpp@acddd29:77-79

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '77,79p'
```

```text
    77	bool cCreatorState::hasState(eGameState gameState) const {
    78	    return m_states[gameState].has_value();
    79	}
```

### Определение `cSelectYourNextConquestState::calculateOffset`

```sh
git grep -n -E '^(.*[ *&])?cSelectYourNextConquestState::calculateOffset\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:176:void cSelectYourNextConquestState::calculateOffset()
```

### cSelectYourNextConquestState::calculateOffset — src/gamestates/cSelectYourNextConquestState.cpp@acddd29:176-180

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '176,180p'
```

```text
   176	void cSelectYourNextConquestState::calculateOffset()
   177	{
   178	    offsetX = m_hdCampaignLayout.panel.getX();
   179	    offsetY = m_hdCampaignLayout.panel.getY();
   180	}
```

### Определение `cSelectYourNextConquestState::installWorld`

```sh
git grep -n -E '^(.*[ *&])?cSelectYourNextConquestState::installWorld\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:923:void cSelectYourNextConquestState::installWorld()
```

### cSelectYourNextConquestState::installWorld — src/gamestates/cSelectYourNextConquestState.cpp@acddd29:923-975

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '923,975p'
```

```text
   923	void cSelectYourNextConquestState::installWorld()
   924	{
   925	    // create regions
   926	    for (int i = 0; i < MAX_REGIONS; i++) {
   927	        delete world[i].bmpColor;
   928	        world[i].bmpColor = nullptr;
   929	        world[i].bSelectable = false;
   930	        world[i].iAlpha = 0;
   931	        world[i].iHouse = -1;
   932	        world[i].oldHouse = -2; // all <0 except iHouse = -1 (for cache)
   933	        world[i].iTile = -1;
   934	        world[i].x = -1;
   935	        world[i].y = -1;
   936	        world[i].bmp = nullptr;
   937	    }
   938	
   939	    // Now create the regions (x,y wise)
   940	
   941	    // FIRST ROW (EASY, SAME Y AXIS)
   942	    regionNew(16, 73, 1, -1, PIECE_DUNE_001);
   943	    regionNew(126, 73, 1, -1, PIECE_DUNE_002);
   944	    regionNew(210, 73, 1, -1, PIECE_DUNE_003);
   945	    regionNew(306, 73, 1, -1, PIECE_DUNE_004);
   946	    regionNew(438, 73, 1, -1, PIECE_DUNE_005);
   947	    regionNew(510, 73, 1, -1, PIECE_DUNE_006);
   948	
   949	    // SECOND ROW, HARDER FROM NOW ON (DIFFERENT Y AXIS ALL THE TIME)
   950	    regionNew(16, 91, 1, -1, PIECE_DUNE_007);
   951	    regionNew(158, 149, 1, -1, PIECE_DUNE_008);
   952	    regionNew(282, 135, 1, -1, PIECE_DUNE_009);
   953	    regionNew(362, 105, 1, -1, PIECE_DUNE_010);
   954	    regionNew(456, 117, 1, -1, PIECE_DUNE_011);
   955	    regionNew(544, 105, 1, -1, PIECE_DUNE_012);
   956	
   957	    // THIRD ROW
   958	    regionNew(16, 155, 1, -1, PIECE_DUNE_013);
   959	    regionNew(58, 165, 1, -1, PIECE_DUNE_014);
   960	    regionNew(190, 213, 1, -1, PIECE_DUNE_015);
   961	    regionNew(312, 163, 1, -1, PIECE_DUNE_016);
   962	    regionNew(388, 163, 1, -1, PIECE_DUNE_017);
   963	    regionNew(502, 167, 1, -1, PIECE_DUNE_018);
   964	    regionNew(576, 167, 1, -1, PIECE_DUNE_019);
   965	
   966	    // FOURTH ROW
   967	    regionNew(16, 237, 1, -1, PIECE_DUNE_020);
   968	    regionNew(62, 255, 1, -1, PIECE_DUNE_021);
   969	    regionNew(134, 245, 1, -1, PIECE_DUNE_022);
   970	    regionNew(282, 257, 1, -1, PIECE_DUNE_023);
   971	    regionNew(360, 253, 1, -1, PIECE_DUNE_024);
   972	    regionNew(406, 213, 1, -1, PIECE_DUNE_025);
   973	    regionNew(448, 269, 1, -1, PIECE_DUNE_026);
   974	    regionNew(514, 227, 1, -1, PIECE_DUNE_027);
   975	}
```

### Определение `cSelectYourNextConquestState::fastForwardUntilMission`

```sh
git grep -n -E '^(.*[ *&])?cSelectYourNextConquestState::fastForwardUntilMission\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:1049:void cSelectYourNextConquestState::fastForwardUntilMission(int missionNr, int house)
```

### cSelectYourNextConquestState::fastForwardUntilMission — src/gamestates/cSelectYourNextConquestState.cpp@acddd29:1049-1070

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '1049,1070p'
```

```text
  1049	void cSelectYourNextConquestState::fastForwardUntilMission(int missionNr, int house)
  1050	{
  1051	    fastForward = true;
  1052	    for (int m = 1; m < missionNr; m++) {
  1053	        regionSetupNextMission(m, house);
  1054	
  1055	        for (int i = 0; i < MAX_REGIONS; i++) {
  1056	            if (iRegionConquer[i] < 0) continue;
  1057	            int houseThatConquersTheRegion = iRegionHouse[i];
  1058	            if (houseThatConquersTheRegion < 0) continue;
  1059	
  1060	            int iRegNr = iRegionConquer[i];
  1061	
  1062	            cRegion &region = world[iRegNr];
  1063	
  1064	            region.iAlpha = 255;
  1065	            region.iHouse = houseThatConquersTheRegion;
  1066	
  1067	            iRegionConquer[i] = -1;
  1068	        }
  1069	    }
  1070	}
```

### Определение `cSelectYourNextConquestState::regionSetupNextMission`

```sh
git grep -n -E '^(.*[ *&])?cSelectYourNextConquestState::regionSetupNextMission\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:809:void cSelectYourNextConquestState::regionSetupNextMission(int iMission, int iHouse)
```

### cSelectYourNextConquestState::regionSetupNextMission — src/gamestates/cSelectYourNextConquestState.cpp@acddd29:809-841

```sh
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '809,841p'
```

```text
   809	void cSelectYourNextConquestState::regionSetupNextMission(int iMission, int iHouse)
   810	{
   811	    // The first mission, nothing is 'ready', as the pieces gets placed and taken by the houses.
   812	    // Later, after mission 2, the pieces are already taken. That's what this function takes care off
   813	    // making sure everything is 'there' to go on with. Hard-coded stuff.
   814	    m_drawManager->regionInit(offsetX, offsetY);
   815	
   816	    // make world pieces not selectable
   817	    for (int i = 0; i < MAX_REGIONS; i++) {
   818	        world[i].bSelectable = false;
   819	    }
   820	
   821	    // clear conquer stuff
   822	    std::fill(std::begin(iRegionConquer), std::end(iRegionConquer), -1);
   823	    std::fill(std::begin(iRegionHouse), std::end(iRegionHouse), -1);
   824	    for (auto &text : cRegionText) {
   825	        text.clear();
   826	    }
   827	
   828	    // Per mission assign:
   829	    // Every house has a different campaign, so...
   830	    m_cIni->loadRegionfile(world, iHouse, iMission, this);
   831	
   832	    selectNextConquestAlpha = 1;
   833	
   834	    // prepare players, so we know house index == player index (for colorizing region pieces)
   835	    for (int i = 1; i < FREMEN; i++) {
   836	        m_objects->getPlayer(i)->init(i, nullptr);
   837	        m_objects->getPlayer(i)->setHouse(i);
   838	    }
   839	
   840	    return;
   841	}
```

### Поля `m_dataCampaign`, `m_campaignProgress`, `m_creatorState`, `m_mentatFlow`, `m_missionFlow`

```sh
git grep -n -w -E 'm_dataCampaign|m_campaignProgress|m_creatorState|m_mentatFlow|m_missionFlow' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src/game/cGame.h src/gamestates/cChooseHouseState.h src/gamestates/cSelectMissionState.h
```

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:255:    std::unique_ptr<s_DataCampaign> m_dataCampaign;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:260:    std::unique_ptr<MentatFlow> m_mentatFlow;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:261:    std::unique_ptr<MissionFlow> m_missionFlow;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:268:    std::unique_ptr<cCreatorState> m_creatorState;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:269:    std::unique_ptr<CampaignProgress> m_campaignProgress;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cChooseHouseState.h:53:    MentatFlow* m_mentatFlow = nullptr;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectMissionState.h:51:    MissionFlow* m_missionFlow = nullptr;
```

