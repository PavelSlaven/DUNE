```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 src/context/
src/context/AudioContext.cpp
src/context/AudioContext.hpp
src/context/ContextCreator.cpp
src/context/ContextCreator.hpp
src/context/GameContext.cpp
src/context/GameContext.hpp
src/context/GraphicsContext.hpp
src/context/MusicChoice.hpp
src/context/MusicJukeBox.cpp
src/context/MusicJukeBox.hpp
src/context/TextContext.cpp
src/context/TextContext.hpp
src/context/cGameObjectContext.cpp
src/context/cGameObjectContext.h
src/context/cGameObjectContextCreator.cpp
src/context/cGameObjectContextCreator.h
src/context/cInfoContext.cpp
src/context/cInfoContext.h
src/context/cInfoContextCreator.cpp
src/context/cInfoContextCreator.h
```
### src/game/cGame.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h | nl -ba
     1	/**
     2	 * @file cGame.h
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
    18	class cMouse;
    19	#include "controls/cKeyboard.h"
    20	#include "definitions.h"
    21	class cRectangle;
    22	#include "observers/cScenarioObserver.h"
    23	
    24	#include <memory>
    25	#include <string>
    26	#include <SDL3/SDL.h>
    27	#include <SDL3_mixer/SDL_mixer.h>
    28	
    29	class cGameControlsContext;
    30	class cGameObjectContext;
    31	class cInfoContext;
    32	class cGameState;
    33	class cPlayer;
    34	class cPlayers;
    35	class AudioContext;
    36	class cSDLSystem;
    37	class cHousesInfo;
    38	class cReinforcements;
    39	class cPreviewMaps;
    40	struct InitialGameSettings;
    41	class cGameSettings;
    42	class cTextDrawer;
    43	
    44	class cNotificationArea;
    45	class GuiConsole;
    46	
    47	class cStructureFactory;
    48	class cSideBarFactory;
    49	class cBuildingListFactory;
    50	
    51	class ContextCreator;
    52	class GameContext;
    53	class cScreenShake;
    54	class cFocusManager;
    55	class cGameConditionChecker;
    56	class cMissionStatsCollector;
    57	class cScreenFader;
    58	class SDLDrawer;
    59	class cMapCamera;
    60	class cDrawManager;
    61	class cTimeManager;
    62	class cStructureUtils;
    63	class Texture;
    64	class cIni;
    65	class cEventEmitter;
    66	class cCreatorState;
    67	class CampaignProgress;
    68	class GameStateTransition;
    69	class MentatFlow;
    70	class MissionFlow;
    71	class ScenarioFlow;
    72	class VideoFlow;
    73	
    74	struct s_DataCampaign;
    75	// struct s_PreviewMap;
    76	// Naming thoughts:
    77	// member variables, start with m_<camelCasedVariableName>
    78	//
    79	// functions are camelCased()
    80	// exceptions (for now):
    81	// think()
    82	// thinkFast_...()
    83	// thinkSlow_....() --> for now used to distinguish certain speed of "thinking" / invocations
    84	// state_...() --> because elegible for moving away
    85	
    86	struct sGameServices;
    87	
    88	class cGame : public cScenarioObserver, cInputObserver {
    89	    friend class UiAuditAccess;
    90	
    91	public:
    92	    cGame();
    93	    ~cGame();
    94	
    95	    void jumpToSelectYourNextConquestMission(int missionNr);
    96	
    97	    void setGameFilename(const std::string &filename) {
    98	        m_gameFilename = filename;
    99	    }
   100	
   101	    std::unique_ptr<cRectangle> m_mapViewport;
   102	    // TODO: move these to a another class that we can pass around, instead of having them as global variables.
   103	    // begin
   104	    std::unique_ptr<cMapCamera> m_mapCamera;
   105	    std::unique_ptr<cDrawManager> m_drawManager;
   106	    std::unique_ptr<cStructureUtils>   m_structureUtils;
   107	    std::unique_ptr<cReinforcements> m_reinforcements;
   108	    // end
   109	
   110	    //todo: this should get moved to private, but not yet.
   111	    std::unique_ptr<cGameObjectContext> m_gameObjectsContext;
   112	    
   113	    //todo: this should get moved to private, but not yet.
   114	    std::unique_ptr<cInfoContext> m_infoContext;
   115	
   116	    //todo: this should get moved to private, but not yet.
   117	    std::unique_ptr<cGameSettings> m_gameSettings;
   118	
   119	    // std::unique_ptr<cStructureFactory> m_structureFactory;
   120	    std::unique_ptr<cSideBarFactory> m_sideBarFactory;
   121	    std::unique_ptr<cBuildingListFactory> m_buildingListFactory;
   122	
   123	
   124	    // Initialization functions
   125	    void init();		            // initialize all game variables
   126	    void missionInit();             // initialize variables for mission loading only
   127	    void setupPlayers();            // initialize players only (combat state initialization)
   128	    bool setupGame();               // only call once, to initialize game object (TODO: in constructor?)
   129	    void shutdown();
   130	    // void loadSkirmishMaps() const;
   131	    void loadScenario();
   132	
   133	    void run();			            // run the game (MAIN LOOP)
   134	
   135	    void initiateFadingOut();        // fade out with current screen_bmp, this is a little game loop itself!
   136	    void prepareMentatForPlayer();
   137	
   138	    bool isState(int thisState) const;
   139	
   140	    // Use this instead
   141	    void setNextStateToTransitionTo(int newState);
   142	
   143	    // Game acts as a facade, delegates to sound player
   144	    void playSound(int sampleId); // Maximum volume
   145	    void playSound(int sampleId, int vol);
   146	
   147	    void playMusicByTypeForStateTransition(eMusicType iType);
   148	    bool playMusicByType(eMusicType iType, bool triggerWithVoice = false);
   149	
   150	    int getMaxVolume();
   151	
   152	    void setPlayerToInteractFor(cPlayer *pPlayer);
   153	    void setMousePosition(int w, int h);
   154	
   155	
   156	    // Event handling
   157	    void onNotifyGameEvent(const s_GameEvent &event) override;
   158	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
   159	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
   160	
   161	    void setMissionLost();
   162	    void setMissionWon();
   163	
   164	    void prepareMentatToTellAboutHouse(int house);
   165	
   166	    void thinkFast();
   167	    void thinkNormal();
   168	    void thinkSlow();
   169	    void thinkCache();
   170	
   171	    void applySettings(std::unique_ptr<InitialGameSettings> gs);
   172	    // the options as they are right now, including changes made while playing (music, fog of war, fullscreen, ...)
   173	    InitialGameSettings currentSettings() const;
   174	    void changeStateFromMentat();
   175	    void loadMapFromEditor(int map);
   176	
   177	    void takeBackGroundScreen();
   178	
   179	    void goingToWinLoseBrief(int value);
   180	
   181	    s_DataCampaign* getDataCampaign() const;
   182	
   183	    void checkMissionWinOrFail();
   184	
   185	private:
   186	    bool m_windowed;        			    // windowed
   187	    bool m_pauseWhenLosingFocus;            // pausing the game when losing focus
   188	    float m_cameraDragMoveSpeed;            // speed of camera when dragging mouse (default = 0.5f)
   189	    float m_cameraBorderOrKeyMoveSpeed;     // speed of camera when hitting mouse border or pressing keys (default = 0.5f)
   190	    bool m_cameraEdgeMove;                  // should move map camera when hitting edges of screen
   191	
   192	    std::string m_gameFilename;
   193	
   194	    std::unique_ptr<cSDLSystem> m_Screen;
   195	    std::unique_ptr<cFocusManager> m_focusManager;
   196	
   197	    AudioContext* m_audioContext = nullptr;
   198	
   199	    std::unique_ptr<InitialGameSettings> m_initialGameSettings;
   200	
   201	    // Non-owning shortcut to the players container (owned by m_gameObjectsContext)
   202	    cPlayers* m_players = nullptr;
   203	
   204	    std::unique_ptr<cMouse> m_mouse;
   205	    std::unique_ptr<cKeyboard> m_keyboard;
   206	    SDL_Window *window;
   207	    SDL_Renderer *renderer;
   208	    Texture *screenTexture=nullptr;
   209	    Texture *actualRenderer= nullptr;
   210	    cTextDrawer* m_textDrawer = nullptr;
   211	    cTimeManager* m_timeManager;
   212	    SDLDrawer *m_sdlDrawer = nullptr;
   213	
   214	    std::unique_ptr<cHousesInfo> m_Houses;
   215	    bool m_missionWasWon;               // hack: used for state transitioning :/
   216	
   217	    std::unique_ptr<cScreenShake> m_screenShake;
   218	    std::unique_ptr<cNotificationArea> m_notificationArea;
   219	    std::unique_ptr<GuiConsole> m_guiConsole;
   220	    cPlayer *m_controlledPlayer = nullptr;
   221	
   222	    void thinkFast_audio();
   223	    void thinkFast_fading();
   224	
   225	
   226	    int m_state; // TODO: Replace with enum, and later even remove with pointer to state
   227	    int m_nextState; // TODO: Replace with enum, and later even remove with pointer to state
   228	
   229	    cGameState *m_currentState;
   230	
   231	    void transitionStateIfRequired();
   232	    void setState(int newState);
   233	    void ensureFrameTargets();
   234	
   235	    void updateMouseAndKeyboardState();
   236	    bool shouldCaptureTextInput() const;
   237	    void syncTextInputState() const;
   238	    void drawState();
   239	
   240	    void shakeScreenAndBlitBuffer();
   241	
   242	    void saveCampaignProgress();
   243	
   244	    void saveBmpScreenToDisk();
   245	    void dispatchGameEvent(const s_GameEvent &event);
   246	
   247	    void onKeyDownGame(const cKeyboardEvent &event);
   248	    void onKeyPressedGame(const cKeyboardEvent &event);
   249	    void onKeyDownDebugMode(const cKeyboardEvent &event);
   250	
   251	    void fadeOutOrBlitScreenBuffer() const;
   252	
   253	    std::unique_ptr<GameContext> ctx;
   254	    std::unique_ptr<ContextCreator> context;
   255	    std::unique_ptr<s_DataCampaign> m_dataCampaign;
   256	    std::unique_ptr<cGameConditionChecker> m_gameConditionChecker;
   257	    std::unique_ptr<cMissionStatsCollector> m_missionStatsCollector;
   258	    std::unique_ptr<cScreenFader> m_cScreenFader;
   259	    std::unique_ptr<GameStateTransition> m_stateTransitions;
   260	    std::unique_ptr<MentatFlow> m_mentatFlow;
   261	    std::unique_ptr<MissionFlow> m_missionFlow;
   262	    std::unique_ptr<ScenarioFlow> m_scenarioFlow;
   263	    std::unique_ptr<VideoFlow> m_videoFlow;
   264	
   265	    std::unique_ptr<sGameServices> m_services;
   266	    std::unique_ptr<cIni> m_cIni;
   267	    std::unique_ptr<cEventEmitter> m_eventEmitter;
   268	    std::unique_ptr<cCreatorState> m_creatorState;
   269	    std::unique_ptr<CampaignProgress> m_campaignProgress;
   270	};
```
### src/context/AudioContext.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/AudioContext.hpp | nl -ba
     1	/**
     2	 * @file AudioContext.hpp
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
    19	#include "context/MusicChoice.hpp"
    20	
    21	#include <memory>
    22	
    23	class cSoundPlayer;
    24	class cGameSettings;
    25	class MusicJukeBox;
    26	
    27	class AudioContext {
    28	public:
    29	    AudioContext(std::unique_ptr<cSoundPlayer> soundPlayer, cGameSettings* settings);
    30	    ~AudioContext();
    31	
    32	    // Low-level escape hatch for UI that adjusts raw player state directly
    33	    // (volume sliders, instant mute) rather than going through game-level music logic.
    34	    [[nodiscard]] cSoundPlayer* getSoundPlayer() const;
    35	
    36	    void playSound(int sampleId) const; // Maximum volume
    37	    void playSound(int sampleId, int vol) const;
    38	    void playVoice(int sampleId, int house) const;
    39	    [[nodiscard]] int getMaxVolume() const;
    40	
    41	    void playMusicByTypeForStateTransition(eMusicType iType, int humanHouse);
    42	    bool playMusicByType(eMusicType iType, bool triggerWithVoice, bool isCurrentlyPlayingMission, int humanHouse);
    43	
    44	    void thinkFast();
    45	
    46	    void toggleMusic();
    47	    void setMusicEnabled(bool enabled);
    48	    void changeMusicVolume(int delta) const;
    49	
    50	private:
    51	    void startMusic(const MusicChoice &choice) const;
    52	
    53	    std::unique_ptr<cSoundPlayer> m_soundPlayer;
    54	    cGameSettings* m_settings = nullptr;
    55	
    56	    std::unique_ptr<MusicJukeBox> m_jukeBox;
    57	    MusicChoice m_newMusic;
    58	    int m_newMusicCountdown;
    59	};
```
### src/context/ContextCreator.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/ContextCreator.hpp | nl -ba
     1	/**
     2	 * @file ContextCreator.hpp
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
    18	#include <SDL3/SDL.h>
    19	#include <SDL3_ttf/SDL_ttf.h>
    20	#include <memory>
    21	
    22	class cFileValidator;
    23	class GraphicsContext;
    24	class Graphics;
    25	class TextContext;
    26	class cTextDrawer;
    27	class cGameSettings;
    28	class SDLDrawer;
    29	
    30	class ContextCreator {
    31	public:
    32	    ContextCreator(SDL_Renderer *renderer, cFileValidator *settingsValidator);
    33	    ContextCreator() = delete;
    34	    ~ContextCreator();
    35	
    36	    std::unique_ptr<GraphicsContext> createGraphicsContext();
    37	    std::unique_ptr<TextContext> createTextContext(cGameSettings *settings, SDLDrawer *renderer);
    38	
    39	private:
    40	    std::shared_ptr<Graphics> gfxmentat;
    41	    std::shared_ptr<Graphics> gfxworld;
    42	    std::shared_ptr<Graphics> gfxinter;
    43	    std::shared_ptr<Graphics> gfxdata;
    44	    std::shared_ptr<Graphics> gfxeditor;
    45	
    46	    TTF_Font *game_font = nullptr; 	// arrakeen.fon
    47	    TTF_Font *bene_font = nullptr;	// benegesserit font.
    48	    TTF_Font *small_font = nullptr;	// small font.
    49	};
```
### src/context/GameContext.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/GameContext.hpp | nl -ba
     1	/**
     2	 * @file GameContext.hpp
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
    18	#include <stdexcept>
    19	#include <memory>
    20	
    21	#include "context/GraphicsContext.hpp"
    22	#include "context/TextContext.hpp"
    23	#include "game/cGameSettings.h"
    24	
    25	class cTimeManager;
    26	class AudioContext;
    27	class SDLDrawer;
    28	class cLog;
    29	
    30	class GameContext {
    31	public:
    32	    GameContext() = default;
    33	    ~GameContext();
    34	
    35	    void setGraphicsContext(std::unique_ptr<GraphicsContext> graphicsContext);
    36	    GraphicsContext* getGraphicsContext() const;
    37	
    38	    void setTimeManager(std::unique_ptr<cTimeManager> timeManager);
    39	    cTimeManager* getTimeManager() const;
    40	
    41	    void setAudioContext(std::unique_ptr<AudioContext> audioContext);
    42	    AudioContext* getAudioContext() const;
    43	
    44	    void setTextContext(std::unique_ptr<TextContext> textContext);
    45	    TextContext* getTextContext() const;
    46	
    47	    void setSDLDrawer(std::unique_ptr<SDLDrawer> SDLDrawer);
    48	    SDLDrawer* getSDLDrawer() const;
    49	
    50	
    51	    void resetCache() const;
    52	private:
    53	    std::unique_ptr<GraphicsContext> m_graphicsContext;
    54	    std::unique_ptr<cTimeManager> m_timeManager;
    55	    std::unique_ptr<AudioContext> m_audioContext;
    56	    std::unique_ptr<TextContext> m_textContext;
    57	    std::unique_ptr<SDLDrawer> m_SDLDrawer;
    58	};
```
### src/context/GraphicsContext.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/GraphicsContext.hpp | nl -ba
     1	/**
     2	 * @file GraphicsContext.hpp
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
    18	#include <memory>
    19	class Graphics;
    20	
    21	class GraphicsContext {
    22	public:
    23	    std::shared_ptr<Graphics> gfxmentat;
    24	    std::shared_ptr<Graphics> gfxworld;
    25	    std::shared_ptr<Graphics> gfxinter;
    26	    std::shared_ptr<Graphics> gfxdata;
    27	    std::shared_ptr<Graphics> gfxeditor;
    28	};
```
### src/context/MusicChoice.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/MusicChoice.hpp | nl -ba
     1	/**
     2	 * @file MusicChoice.hpp
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
    18	#include <filesystem>
    19	#include <optional>
    20	
    21	// What to play for a music request: always an archive track (the fallback),
    22	// plus a file from the repertory directory when one was picked.
    23	struct MusicChoice {
    24	    int archiveTrack = 0;
    25	    std::optional<std::filesystem::path> file;
    26	};
```
### src/context/MusicJukeBox.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/MusicJukeBox.hpp | nl -ba
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
### src/context/TextContext.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/TextContext.hpp | nl -ba
     1	/**
     2	 * @file TextContext.hpp
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
    18	#include <memory>
    19	class cTextDrawer;
    20	
    21	class TextContext {
    22	
    23	public:
    24	    TextContext(
    25	        std::unique_ptr<cTextDrawer> smallTextDrawer,
    26	        std::unique_ptr<cTextDrawer> beneTextDrawer,
    27	        std::unique_ptr<cTextDrawer> gameTextDrawer
    28	    );
    29	    ~TextContext();
    30	
    31	    void resetCache() const;
    32	
    33	    [[nodiscard]] cTextDrawer* getSmallTextDrawer() const;
    34	    [[nodiscard]] cTextDrawer* getBeneTextDrawer() const;
    35	    [[nodiscard]] cTextDrawer* getGameTextDrawer() const;
    36	
    37	private:
    38	    std::unique_ptr<cTextDrawer> m_smallTextDrawer;
    39	    std::unique_ptr<cTextDrawer> m_beneTextDrawer;
    40	    std::unique_ptr<cTextDrawer> m_gameTextDrawer;
    41	};
```
### src/context/cGameObjectContext.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cGameObjectContext.h | nl -ba
     1	/**
     2	 * @file cGameObjectContext.h
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
    18	#include <stdexcept>
    19	#include <cstddef>
    20	#include <memory>
    21	class MapGeometry;
    22	
    23	class cBullets;
    24	class cPlayers;
    25	class cParticles;
    26	class cStructures;
    27	class cUnits;
    28	class cMap;
    29	class cPreviewMaps;
    30	class cPlayer;
    31	class cUnit;
    32	class cAbstractStructure;
    33	class cStructureFactory;
    34	
    35	struct sGameServices;
    36	
    37	class cGameObjectContext {
    38	public:
    39	    cGameObjectContext(
    40	        std::unique_ptr<cBullets> bullets,
    41	        std::unique_ptr<cPlayers> players,
    42	        std::unique_ptr<cParticles> particles,
    43	        std::unique_ptr<cStructures> structures,
    44	        std::unique_ptr<cUnits> units,
    45	        std::unique_ptr<cMap> map,
    46	        std::unique_ptr<cPreviewMaps> previewMaps,
    47	        std::unique_ptr<cStructureFactory> structureFactory);
    48	    ~cGameObjectContext();
    49	
    50	    cBullets& getBullets() const;
    51	    cMap* getMap() const;
    52	    MapGeometry* getMapGeometry() const;
    53	    cPlayers* getPlayers() const;
    54	    cParticles& getParticles() const;
    55	
    56	    cStructures& getStructures() const;
    57	    cAbstractStructure* getStructure(int index);
    58	    cPreviewMaps* getPreviewMaps() const;
    59	
    60	    cUnits* getUnits() const;
    61	    int getUnitsSize() const;
    62	    cUnit* getUnit(std::size_t index);
    63	    cUnit* getUnit(int index);
    64	
    65	    cPlayer* getPlayer(int index);
    66	    const cPlayer* getPlayer(int index) const;
    67	
    68	    cStructureFactory* getStructureFactory() const;
    69	
    70	    void serviceInit(sGameServices* services);
    71	private:
    72	    std::unique_ptr<cBullets> m_Bullets;
    73	    std::unique_ptr<cPlayers> m_Players;
    74	    std::unique_ptr<cParticles> m_particles;
    75	    std::unique_ptr<cStructures> m_pStructures;
    76	    std::unique_ptr<cUnits> m_Units;
    77	    std::unique_ptr<cMap> m_map;
    78	    std::unique_ptr<cPreviewMaps> m_previewMaps;
    79	    std::unique_ptr<cStructureFactory> m_structureFactory;
    80	};
```
### src/context/cGameObjectContextCreator.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cGameObjectContextCreator.h | nl -ba
     1	/**
     2	 * @file cGameObjectContextCreator.h
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
    18	#include <memory>
    19	
    20	class cGameObjectContext;
    21	
    22	class cGameObjectsContextCreator {
    23	public:
    24	    cGameObjectsContextCreator() = default;
    25	    ~cGameObjectsContextCreator() = default;
    26	
    27	    static std::unique_ptr<cGameObjectContext> create();
    28	};
```
### src/context/cInfoContext.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContext.h | nl -ba
     1	/**
     2	 * @file cInfoContext.h
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
    18	#include <stdexcept>
    19	#include <memory>
    20	
    21	#include "gameobjects/particles/cParticleInfos.h"
    22	#include "gameobjects/units/cUnitInfos.h"
    23	#include "gameobjects/structures/cStructureInfo.h"
    24	#include "gameobjects/projectiles/cBulletInfos.h"
    25	#include "gameobjects/cSpecialInfos.h"
    26	#include "gameobjects/cUpgradeInfo.h"
    27	#include "gameobjects/sTerrainInfo.h"
    28	#include "context/cInfoContextCreator.h"
    29	
    30	class SDLDrawer;
    31	
    32	class cInfoContext {
    33	public:
    34	    cInfoContext() = default;
    35	    ~cInfoContext();
    36	
    37	    void setParticleInfos(std::unique_ptr<cParticleInfos> particleInfos);
    38	    cParticleInfos* getParticleInfos() const;
    39	    void setStructureInfos(std::unique_ptr<cStructureInfos> structureInfos);
    40	    cStructureInfos* getStructureInfos() const;
    41	    void setBulletInfos(std::unique_ptr<cBulletInfos> bulletInfos);
    42	    cBulletInfos* getBulletInfos() const;
    43	    void setSpecialInfos(std::unique_ptr<cSpecialInfos> specialInfos);
    44	    cSpecialInfos* getSpecialInfos() const;
    45	    void setUpgradeInfos(std::unique_ptr<cUpgradeInfos> upgradeInfos);
    46	    cUpgradeInfos* getUpgradeInfos() const;
    47	    void setUnitInfos(std::unique_ptr<cUnitInfos> unitInfos);
    48	    cUnitInfos* getUnitInfos() const;
    49	    void setTerrainInfo(std::unique_ptr<s_TerrainInfo> terrainInfo);
    50	    s_TerrainInfo* getTerrainInfo() const;
    51	    void initializeDefaultInfos();
    52	
    53	    // Convenience getters for individual elements
    54	    s_ParticleInfo& getParticleInfo(int i) const;
    55	    s_StructureInfo& getStructureInfo(int i) const;
    56	    s_BulletInfo& getBulletInfo(int i) const;
    57	    s_SpecialInfo& getSpecialInfo(int i) const;
    58	    s_UpgradeInfo& getUpgradeInfo(int i) const;
    59	    s_UnitInfo& getUnitInfo(int i) const;
    60	
    61	private:
    62	    std::unique_ptr<cParticleInfos> m_particleInfos;
    63	    std::unique_ptr<cStructureInfos> m_structureInfos;
    64	    std::unique_ptr<cBulletInfos> m_bulletInfos;
    65	    std::unique_ptr<cSpecialInfos> m_specialInfos;
    66	    std::unique_ptr<cUpgradeInfos> m_upgradeInfos;
    67	    std::unique_ptr<cUnitInfos> m_unitInfos;
    68	    std::unique_ptr<s_TerrainInfo> m_terrainInfo;
    69	};
```
### src/context/cInfoContextCreator.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.h | nl -ba
     1	/**
     2	 * @file cInfoContextCreator.h
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
    18	#include <memory>
    19	
    20	class cParticleInfos;
    21	class cStructureInfos;
    22	class cBulletInfos;
    23	class cSpecialInfos;
    24	class cUpgradeInfos;
    25	class cUnitInfos;
    26	class cInfoContext;
    27	class cGameSettings;
    28	class Graphics;
    29	class GraphicsContext;
    30	struct SDL_Renderer;
    31	struct s_TerrainInfo;
    32	
    33	class cInfoContextCreator {
    34	public:
    35	    explicit cInfoContextCreator(GraphicsContext* graphicsContext);
    36	    ~cInfoContextCreator() = default;
    37	
    38	    std::unique_ptr<cParticleInfos> createParticleInfos();
    39	    std::unique_ptr<cStructureInfos> createStructureInfos();
    40	    std::unique_ptr<cBulletInfos> createBulletInfos();
    41	    std::unique_ptr<cSpecialInfos> createSpecialInfos();
    42	    std::unique_ptr<cUpgradeInfos> createUpgradeInfos(const cInfoContext* infoContext, const cGameSettings* settings);
    43	    std::unique_ptr<cUnitInfos> createUnitInfos();
    44	    std::unique_ptr<s_TerrainInfo> createTerrainInfos();
    45	
    46	    void installInfos(cInfoContext& infoContext);
    47	
    48	private:
    49	    void installTerrain(s_TerrainInfo* terrainInfo);
    50	    void initUnits(cUnitInfos& unitInfos);
    51	    void initStructures(cStructureInfos& structureInfos);
    52	    void initBullets(cBulletInfos& bulletInfos);
    53	    void initSpecials(cSpecialInfos& specialInfos);
    54	    void initParticles(cParticleInfos& particleInfos);
    55	    void initUpgrades(cUpgradeInfos& upgradeInfos, const cInfoContext* infoContext, const cGameSettings* settings);
    56	
    57	    Graphics* m_gfxdata = nullptr;
    58	};
```
### Путь по имени файла: cPlayer.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cPlayer.h$'
src/gameobjects/players/cPlayer.h
```
### src/gameobjects/players/cPlayer.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.h | nl -ba
     1	/**
     2	 * @file cPlayer.h
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
    18	
    19	#include "controls/mousestates/eMouseStates.h"
    20	#include "definitions.h"
    21	#include "observers/cScenarioObserver.h"
    22	#include "gameobjects/players/brains/cPlayerBrain.h"
    23	#include "include/enums/CombatEnums.h"
    24	#include "include/enums/HouseFlags.h"
    25	class cRectangle;
    26	#include "utils/Color.hpp"
    27	
    28	
    29	#include "gameobjects/cUpgradeInfo.h"
    30	#include "gameobjects/units/cUnitInfos.h"
    31	#include "utils/HouseColors.h"
    32	
    33	#include <set>
    34	#include <string>
    35	#include <vector>
    36	#include <array>
    37	#include <memory>
    38	
    39	class cItemBuilder;
    40	class cBuildingListUpdater;
    41	class cHousesInfo;
    42	class Texture;
    43	class cSideBar;
    44	class cPlayerDifficultySettings;
    45	class cOrderProcesser;
    46	class cGameControlsContext;
    47	class Graphics;
    48	class SDLDrawer;
    49	
    50	
    51	struct sEntityForDistance {
    52	    int distance = 9999;
    53	    int entityId = -1;
    54	
    55	    bool operator<(const sEntityForDistance &rhs) const {
    56	        return distance < rhs.distance;
    57	    }
    58	};
    59	
    60	struct s_PlaceResult {
    61	    bool success = false; // if true, all is ok
    62	
    63	    bool onlyMyUnitsBlock = false;  // if true, then it means when success=false,
    64	    // ONLY units block the placement, but they are the units of the requesting player.
    65	    // which can be fixed (by AI) to move them away.
    66	
    67	    // else, these are one of the reasons why it was not a success
    68	    bool badTerrain = false; // not valid to place
    69	
    70	    bool outOfBounds = false; // (one of the cells) is out of bounds
    71	
    72	    // these units block it
    73	    std::set<int> unitIds = std::set<int>();
    74	
    75	    // these structures block it
    76	    std::set<int> structureIds = std::set<int>();
    77	};
    78	
    79	struct sSelectedUnitTypes {
    80	    bool hasInfantry = false;
    81	    bool hasVehicles = false;
    82	};
    83	
    84	struct sGameServices;
    85	class cGameSettings;
    86	class cInfoContext;
    87	class cGameObjectContext;
    88	class cEventEmitter;
    89	class AudioContext;
    90	class cScreenFader;
    91	class cStructureUtils;
    92	class cLog;
    93	
    94	class cPlayer : public cScenarioObserver {
    95	
    96	public:
    97	    static constexpr int MAX_STRUCTURE_BMPS = MAX_STRUCTURETYPES*2;
    98	    cPlayer();
    99	
   100	    ~cPlayer();
   101	
   102	    /**
   103	     * Injects services that weren't available at construction time.
   104	     */
   105	    void serviceInit(sGameServices* services);
   106	
   107	    void init(int id, std::unique_ptr<brains::cPlayerBrain> brain);
   108	
   109	    void setBrain(std::unique_ptr<brains::cPlayerBrain> brain);
   110	
   111	    void setHousesInfo(cHousesInfo* housesInfo) {
   112	        d2tm_assert(housesInfo != nullptr);
   113	        m_HousesInfo = housesInfo;
   114	    }
   115	
   116	    void setAutoSlabStructures(bool value);
   117	
   118	    bool bEnoughPower() const;
   119	
   120	    bool bEnoughSpiceCapacityToStoreCredits() const;
   121	
   122	    bool hasAlmostReachMaxSpiceStorageCapacity() const;
   123	
   124	    bool bEnoughSpiceCapacityToStoreCredits(int threshold) const;
   125	
   126	    // credits
   127	    void substractCredits(float amount);
   128	    void setCredits(int credits);
   129	    void giveCredits(float amountToGive);
   130	    int getCredits() const;
   131	
   132	
   133	    // focus cell
   134	    void setFocusCell(int cll);
   135	    int getFocusCell() const {
   136	        return focusCell_;
   137	    }
   138	
   139	    // house
   140	    std::string getHouseName() const;
   141	    int getHouse() const {
   142	        return house;
   143	    }
   144	    bool isHouse(int houseId) const {
   145	        return house == houseId;
   146	    }
   147	    void setHouse(int iHouse);
   148	
   149	    // ---
   150	    void setItemBuilder(std::unique_ptr<cItemBuilder> theItemBuilder);
   151	
   152	    void setSideBar(cSideBar *theSideBar);
   153	
   154	    void setBuildingListUpdater(std::unique_ptr<cBuildingListUpdater> theBuildingListUpgrader);
   155	
   156	    void setTechLevel(int theTechLevel) {
   157	        techLevel = theTechLevel;
   158	    }
   159	
   160	    void setOrderProcesser(std::unique_ptr<cOrderProcesser> theOrderProcesser);
   161	
   162	    void setGameControlsContext(std::unique_ptr<cGameControlsContext> theGameControlsContext);
   163	
   164	    // get
   165	    cBuildingListUpdater *getBuildingListUpdater() const {
   166	        return buildingListUpdater.get();
   167	    }
   168	
   169	    cPlayerDifficultySettings *getDifficultySettings() const {
   170	        return difficultySettings.get();
   171	    }
   172	
   173	    cGameObjectContext *getObjects() const {
   174	        return m_objects;
   175	    }
   176	
   177	    cInfoContext *getInfos() const {
   178	        return m_infos;
   179	    }
   180	
   181	    cGameSettings *getSettings() const {
   182	        return m_settings;
   183	    }
   184	
   185	    cEventEmitter *getEventEmitter() const {
   186	        return m_eventEmitter;
   187	    }
   188	
   189	    cItemBuilder *getItemBuilder() const {
   190	        return itemBuilder.get();
   191	    }
   192	
   193	    cSideBar *getSideBar() const {
   194	        return sidebar;
   195	    }
   196	
   197	    cAbstractStructure *getSelectedStructure() const;
   198	
   199	    eHouseBitFlag getHouseBitFlag();
   200	
   201	    Color getHouseFadingColor() const;
   202	
   203	    Color getErrorFadingColor() const;
   204	
   205	    Color getPrimaryBuildingFadingColor() const;
   206	
   207	    Color getSelectFadingColor() const;
   208	
   209	    int getTechLevel() const {
   210	        return techLevel;
   211	    }
   212	
   213	    int getId() const {
   214	        return id;
   215	    }
   216	
   217	    cOrderProcesser *getOrderProcesser() const {
   218	        return orderProcesser.get();
   219	    }
   220	
   221	    cGameControlsContext *getGameControlsContext() const {
   222	        return gameControlsContext.get();
   223	    }
   224	
   225	    void setContextMouseState(eMouseState newState);
   226	
   227	    bool isContextMouseState(eMouseState state);
   228	
   229	    Color getMinimapColor() const {
   230	        return minimapColor;
   231	    }
   232	
   233	    Color getEmblemBackgroundColor() const {
   234	        return emblemBackgroundColor;
   235	    }
   236	
   237	    bool isHuman() const {
   238	        return m_Human;
   239	    }
   240	
   241	    int getAmountOfUnitsForType(int unitType) const;
   242	
   243	    int getAmountOfStructuresForType(int structureType) const;
   244	
   245	    int getAmountOfUnitsForType(const std::vector<int> &unitTypes) const;
   246	
   247	    bool hasRadarAndEnoughPower() const;
   248	
   249	    std::string asString() const;
   250	
   251	    Texture *getStructureBitmap(int index);
   252	
   253	    Texture *getStructureBitmapFlash(int index);
   254	
   255	    Texture *getFlagBitmap();
   256	
   257	    Texture *getFlagSmallBitmap();
   258	
   259	    Texture *getUnitBitmap(int index);
   260	
   261	    Texture *getUnitTopBitmap(int index);
   262	
   263	    Texture *getUnitShadowBitmap(int index);
   264	
   265	    void destroyAllegroBitmaps();
   266	
   267	    bool hasWor() const;
   268	
   269	    bool hasBarracks() const;
   270	
   271	    bool hasAtleastOneStructure(int structureType) const;
   272	
   273	    void decreaseStructureAmount(int structureType);
   274	
   275	    void increaseStructureAmount(int structureType);
   276	
   277	    bool hasEnoughPowerFor(int structureType) const;
   278	
   279	    bool hasEnoughCreditsFor(float requestedAmount) const;
   280	
   281	    bool hasEnoughCreditsForUnit(int unitType);
   282	
   283	    bool hasEnoughCreditsForStructure(int structureType);
   284	
   285	    bool hasEnoughCreditsForUpgrade(int upgradeType);
   286	
   287	    bool isPrimaryStructureForStructureType(int structureType, int structureId) const {
   288	        return getPrimaryStructureForStructureType(structureType) == structureId;
   289	    }
   290	
   291	    int getPrimaryStructureForStructureType(int structureType) const {
   292	        return iPrimaryBuilding[structureType];
   293	    }
   294	
   295	    void setPrimaryBuildingForStructureType(int structureType, int structureIndex) {
   296	        iPrimaryBuilding[structureType] = structureIndex;
   297	    }
   298	
   299	    int getStructureUpgradeLevel(int structureType) const {
   300	        return iStructureUpgradeLevel[structureType];
   301	    }
   302	
   303	    void increaseStructureUpgradeLevel(int structureType) {
   304	        if (structureType < 0) return;
   305	        if (structureType >= MAX_STRUCTURETYPES) return;
   306	        iStructureUpgradeLevel[structureType]++;
   307	    }
   308	
   309	    bool isUpgradeApplied(int upgradeIndex) const {
   310	        if (upgradeIndex < 0 || upgradeIndex >= MAX_UPGRADETYPES) {
   311	            return false;
   312	        }
   313	        return m_appliedUpgrades[upgradeIndex];
   314	    }
   315	
   316	    void setUpgradeApplied(int upgradeIndex) {
   317	        if (upgradeIndex < 0 || upgradeIndex >= MAX_UPGRADETYPES) {
   318	            return;
   319	        }
   320	        m_appliedUpgrades[upgradeIndex] = true;
   321	    }
   322	
   323	    void setTeam(int value) {
   324	        iTeam = value;
   325	    }
   326	
   327	    int getTeam() const {
   328	        return iTeam;
   329	    }
   330	
   331	
   332	    /**
   333	     * Returns all my units, but ordered by distance from cell param to unit location. (closest first)
   334	     *
   335	     * @param cell
   336	     * @return
   337	     */
   338	    std::vector<sEntityForDistance> getAllMyUnitsOrderClosestToCell(int cell);
   339	
   340	    /**
   341	     * Returns all my structures, but ordered by distance from cell param to structure location. (closest first)
   342	     *
   343	     * @param cell
   344	     * @return
   345	     */
   346	    std::vector<sEntityForDistance> getAllMyStructuresOrderClosestToCell(int cell);
   347	
   348	    std::vector<int> getAllMyUnits();
   349	
   350	    std::vector<int> getAllMyUnitsForType(int unitType) const;
   351	
   352	    std::vector<int> getInfantryUnitsOnMap() const;
   353	    std::vector<int> getInfantryUnitsOnViewport(const cRectangle &rect) const;
   354	
   355	    std::vector<int> getWheelUnitsOnMap() const;
   356	    std::vector<int> getWheelUnitsOnViewport(const cRectangle &rect) const;
   357	
   358	    std::vector<int> getTankUnitsOnMap() const;
   359	    std::vector<int> getTankUnitsOnViewport(const cRectangle &rect) const;
   360	
   361	    std::vector<int> getLauncherUnitsOnMap() const;
   362	    std::vector<int> getLauncherUnitsOnViewport(const cRectangle &rect) const;
   363	
   364	    std::vector<int> getHarvesterUnitsOnMap() const;
   365	    std::vector<int> getHarvesterUnitsOnViewport(const cRectangle &rect) const;
   366	
   367	    std::vector<int> getAttackingUnitsOnMap() const;
   368	
   369	    std::vector<int> getAllMyUnitsWithinViewportRect(const cRectangle &rect) const;
   370	
   371	    std::vector<int> getAllMyStructuresAsId();
   372	
   373	    std::vector<int> getAllMyStructuresAsIdForType(int structureType);
   374	
   375	    std::vector<int> getAllMyUnitsForGroupNr(const int groupId) const;
   376	
   377	    std::vector<int> getSelectedUnits() const;
   378	
   379	    bool isSameTeamAs(const cPlayer *pPlayer) const;
   380	
   381	    void update();
   382	
   383	    float getMaxCredits() const;
   384	
   385	    int getPowerProduced() const;
   386	
   387	    int getPowerUsage() const;
   388	
   389	    void dumpCredits(int amount);
   390	
   391	    void think();
   392	
   393	    /**
   394	     * Checks if the given unitType is available for producing; does not check if it is allowed to do so. Use
   395	     * canBuildUnit for that.
   396	     *
   397	     * @param iUnitType
   398	     * @return
   399	     */
   400	    bool canBuildUnitType(int iUnitType) const;
   401	
   402	    /**
   403	     * Checks if the given iType is available for producing; does not check if it is allowed to do so. Use
   404	     * canBuilSpecial for that.
   405	     *
   406	     * @param iType
   407	     * @return
   408	     */
   409	    bool canBuildSpecialType(int iType) const;
   410	
   411	    /**
   412	     * Check if we can build unit of type. Returns a reason when it can't. If the reason is NONE it means it can be built.
   413	     */
   414	    eCantBuildReason canBuildUnit(int iUnitType);
   415	
   416	    /**
   417	     * Returns true/false if this house could (ever) build this special type
   418	     * @param iType
   419	     * @return
   420	     */
   421	    bool couldBuildSpecial(int iType);
   422	
   423	    eCantBuildReason canBuildSpecial(int iType);
   424	
   425	    /**
   426	     * Returns true if the unit can be bought, takes not money into account, but all other rules do apply
   427	     * @param iUnitType
   428	     * @return
   429	     */
   430	    bool canBuildUnitBool(int iUnitType);
   431	
   432	    eCantBuildReason canBuildUnit(int iUnitType, bool checkIfAffordable);
   433	
   434	
   435	    /**
   436	     * Checks if the given structureType is available for producing (in list of constyard);
   437	     * does not check if it is allowed to do so. Use canBuildStructure for that.
   438	     *
   439	     * @param iStructureType
   440	     * @return
   441	     */
   442	    bool isStructureTypeAvailableForConstruction(int iStructureType) const;
   443	    /**
   444	     * Check if we can build structure of type. Returns a reason when it can't. If the reason is NONE it means it can be built.
   445	     */
   446	    eCantBuildReason canBuildStructure(int iStructureType);
   447	
   448	    int getStructureTypeBeingBuilt() const;
   449	    cBuildingListItem *getStructureBuildingListItemBeingBuilt() const;
   450	
   451	    int  findCellToPlaceStructure(int iStructureType);
   452	
   453	    /**
   454	     * Returns true if anything is built from ConstYard
   455	     */
   456	    bool isBuildingStructureAwaitingPlacement() const;
   457	    bool isSpecialAwaitingPlacement() const;
   458	    cBuildingListItem *getSpecialAwaitingPlacement() const;
   459	
   460	    cBuildingListItem *isUpgradeAvailableToGrantUnit(int iUnitType) const;
   461	    cBuildingListItem *isUpgradeAvailableToGrantStructure(int iStructureType) const;
   462	
   463	    cBuildingListItem *isUpgradingList(eListType listType, int sublistId) const;
   464	    cBuildingListItem *isUpgradingConstyard() const;
   465	    cBuildingListItem *isBuildingStructure() const;
   466	    bool isBuildingSomethingInSameListSubListAsUnitType(int iUnitType) const;
   467	
   468	    bool startBuildingUnit(int iUnitType) const;
   469	    bool startBuildingStructure(int iStructureType) const;
   470	    bool startBuildingSpecial(int iSpecialType) const;
   471	    bool startUpgrading(int iUpgradeType) const;
   472	
   473	    bool startUpgradingForUnitIfPossible(int iUpgradeType) const;
   474	
   475	    int findRandomUnitTarget(int playerIndexToAttack);
   476	    int findRandomStructureTarget(int iAttackPlayer);
   477	
   478	    /**
   479	     * Places structure (if allowed), source is building list item (ie something the gameobjects/players/AI built and wanted to place). Also
   480	     * takes care of the buildingList management after placement. The buildingList management is applied regardless if
   481	     * the structure got placed or not.
   482	     *
   483	     * @param destinationCell   where to put it
   484	     * @param itemToPlace       which building list item to use? (used to derive which kind of structure, etc)
   485	     * @return
   486	     */
   487	    cAbstractStructure *placeItem(int destinationCell, cBuildingListItem *itemToPlace);
   488	
   489	    /**
   490	     * Places structure, usually the source is somewhere else (a unit, MCV; or from map loading).
   491	     * @param destinationCell   where to put it
   492	     * @param iStructureTypeId structure type
   493	     * @param healthPercentage 0-100
   494	     * @return
   495	     */
   496	    cAbstractStructure *placeStructure(int destinationCell, int iStructureTypeId, int healthPercentage);
   497	
   498	    void onNotifyGameEvent(const s_GameEvent &event);
   499	
   500	    int getScoutingUnitType();
   501	    int getSpecialUnitType();
   502	
   503	    bool hasAnyUnitSelected();
   504	    sSelectedUnitTypes getSelectedUnitTypes() const;
   505	
   506	    static std::string getHouseNameForId(int house);
   507	
   508	    void logStructures();
   509	
   510	    void cancelBuildingListItem(cBuildingListItem *item);
   511	
   512	    void cancelStructureBuildingListItemBeingBuilt();
   513	
   514	    s_PlaceResult canPlaceStructureAt(int iCell, int iStructureType, int iUnitIDToIgnore);
   515	    s_PlaceResult canPlaceStructureAt(int iCell, int iStructureType);
   516	    s_PlaceResult canPlaceConcreteAt(int iCell);
   517	
   518	    void log(const std::string &txt) const;
   519	
   520	    void thinkFast();
   521	
   522	    int getSoldierType();
   523	
   524	    int getInfantryType();
   525	
   526	    int getSameOrSimilarUnitType(int requestedUnitType);
   527	
   528	    void setQuota(int value) {
   529	        spiceQuota = value;
   530	    }
   531	
   532	    bool hasMetQuota();
   533	
   534	    /**
   535	     * Checks if player has anything, if so, it returns true.
   536	     */
   537	    bool evaluateStillAlive();
   538	
   539	    bool isAlive() {
   540	        return alive;
   541	    }
   542	
   543	    // properties (for now public, should become private)
   544	    int selected_structure = -1;
   545	
   546	    void deselectStructure();
   547	
   548	    void deselectAllUnits();
   549	
   550	    bool selectUnitsFromGroup(int groupId);
   551	
   552	    void markUnitsForGroup(const int groupId) const;
   553	
   554	    /**
   555	     * Given this list of unit id's, select them. Also applies logic, to skip harvesters if non-harvesters
   556	     * are within this list of ID's. Also plays sound effects (reporting!) depending on infantry/non-infantry unit.
   557	     * @param ids
   558	     */
   559	    bool selectUnits(const std::vector<int> &ids) const;
   560	
   561	    /**
   562	     * Adds all non-airborn units in ids to the current selection without harvester filtering.
   563	     * Used when SHIFT is held to add units to an existing selection.
   564	     */
   565	    void selectAdditionalUnits(const std::vector<int> &ids) const;
   566	
   567	    void thinkSlow();
   568	
   569	    void deselectUnit(const int &unitId);
   570	
   571	    const HouseColors& getColors() const;
   572	
   573	private:
   574	    bool hasAliveStructure();
   575	    bool hasAliveUnit();
   576	
   577	    static int groupIdToIndex(int groupId);
   578	
   579	    cBuildingListItem *isUpgradeAvailableToGrant(eBuildType providesType, int providesTypeId) const;
   580	
   581	    void clearStructureTypeBitmaps();
   582	
   583	    void clearUnitTypeBitmaps();
   584	
   585	    Color getRGBColorForHouse(int houseId);
   586	
   587	    Color getEmblemBackgroundColorForHouse(int houseId);
   588	
   589	    bool isBuildingAnythingForListAndSublist(eListType listType, int subListId) const;
   590	
   591	    bool startBuilding(cBuildingListItem *pItem);
   592	
   593	    bool startBuilding(eBuildType buildType, int buildId);
   594	
   595	    void onEntityDiscovered(const CommonEvent &event);
   596	
   597	    void onMyUnitDestroyed(const CommonEvent &event);
   598	
   599	    void onMyStructureDestroyed(const CommonEvent &event);
   600	
   601	    bool m_Human = false;
   602	
   603	    // TODO: in the end this should be redundant.. perhaps remove it now/soon anyway?
   604	    // TODO: redundant? OBSOLETE. Since we're getting more properties for units and thereby
   605	    // can/should create units specific for houses.
   606	    std::unique_ptr<cPlayerDifficultySettings> difficultySettings;
   607	    // these have all state, and need to be recreated for each mission.
   608	    cSideBar *sidebar;            // each player has a sidebar (lists of what it can build)
   609	    std::unique_ptr<cItemBuilder> itemBuilder; // each player can build items
   610	    std::unique_ptr<cBuildingListUpdater> buildingListUpdater; // modifies list of sidebar on upgrades
   611	    std::unique_ptr<cOrderProcesser> orderProcesser; // process orders for starport
   612	    cHousesInfo* m_HousesInfo = nullptr;
   613	    std::unique_ptr<cGameControlsContext> gameControlsContext;
   614	
   615	    int techLevel = 0;        // technology level
   616	    int house = GENERALHOUSE;
   617	    Color minimapColor;            // color of this team on minimap;
   618	    Color emblemBackgroundColor;    // color of the emblem background
   619	    int id = -1;    // this id is the reference to the player array
   620	    int iTeam = -1;
   621	
   622	    cGameSettings *m_settings = nullptr;
   623	    cInfoContext *m_infos = nullptr;
   624	    cGameObjectContext *m_objects = nullptr;
   625	    cEventEmitter *m_eventEmitter = nullptr;
   626	    AudioContext *m_audioContext = nullptr;
   627	    cScreenFader *m_screenFader = nullptr;
   628	    cStructureUtils *m_structureUtils = nullptr;
   629	    cLog *m_log = nullptr;
   630	    Graphics *m_gfxdata = nullptr;
   631	    SDLDrawer *m_renderer = nullptr;
   632	
   633	    std::array<std::unique_ptr<Texture>, MAX_STRUCTURE_BMPS> bmp_structure;
   634	    Texture *bmp_flag;
   635	    Texture *bmp_flag_small;
   636	
   637	    std::array<std::unique_ptr<Texture>, MAX_UNITTYPES> bmp_unit; // the body of unit
   638	    std::array<std::unique_ptr<Texture>, MAX_UNITTYPES> bmp_unit_top; // optionally a 'top' of unit (barrel of tank, for example)
   639	
   640	    int iPrimaryBuilding[MAX_STRUCTURETYPES] = {};    // remember the primary ID (structure id) of each structure type
   641	    int iStructures[MAX_STRUCTURETYPES] = {}; // remember what is built for each type of structure
   642	    int iStructureUpgradeLevel[MAX_STRUCTURETYPES] = {}; // remember the upgrade level for each structure type
   643	    bool m_appliedUpgrades[MAX_UPGRADETYPES] = {}; // tracks which independent upgrades have been applied
   644	
   645	    int powerUsage_ = 0;      // total amount of power usage
   646	    int powerProduce_ = 0;      // total amount of power generated
   647	
   648	    float credits = 0;        // the credits this player has
   649	    float maxCredits_ = 1000;    // max credits a player can have (influenced by silo's)
   650	
   651	    int focusCell_ = 0;        // this is the cell that will be showed in the game centralized upon map loading
   652	
   653	    std::unique_ptr<brains::cPlayerBrain> brain_;
   654	
   655	    bool m_autoSlabStructures; // flag that will automatically place slabs beneath a structure when placed
   656	
   657	    // A condition to win the mission
   658	    int spiceQuota = 0;              // > 0 means this amount to harvest, (if win/lose flags set accordingly for game)
   659	
   660	    bool alive = false;
   661	
   662	    void reinforceHarvesterIfNeeded(int cell);
   663	};
```
### Путь по имени файла: cMapCamera.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cMapCamera.h$'
src/gameobjects/map/cMapCamera.h
```
### src/gameobjects/map/cMapCamera.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMapCamera.h | nl -ba
     1	/**
     2	 * @file cMapCamera.h
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
    16	/*
    17	 * cMapCamera.h
    18	 *
    19	 *  A map camera is 'looking' at the map. Using this camera (or viewport) we can determine
    20	 *  what to draw, how big, etc.
    21	 *
    22	 *  Using a camera technique we can easily adjust the drawing logic whenever the resolution
    23	 *  of the game changes.
    24	 *
    25	 */
    26	
    27	#pragma once
    28	
    29	// #include "cMap.h"
    30	
    31	#include "observers/cInputObserver.h"
    32	#include "utils/cRectangle.h"
    33	#include <array>
    34	#include <cmath>
    35	
    36	class cMap;
    37	class MapGeometry;
    38	class cGameSettings;
    39	class cMouse;
    40	
    41	class cMapCamera : cInputObserver {
    42	
    43	public:
    44	    cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse);
    45	
    46	    ~cMapCamera();
    47	
    48	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    49	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    50	
    51	    void thinkFast();
    52	
    53	    void resetZoom();
    54	
    55	    void setZoomLevel(float zoom);
    56	
    57	    void zoomOutToFit(const cRectangle& bounds);
    58	
    59	    void jumpTo(int theX, int theY);
    60	
    61	    void moveTo(int theX, int theY);
    62	
    63	    /**
    64	     * Returns the pixel coordinate on the window to draw onto. Use this function to convert absolute
    65	     * coordinates into window coordinates so you can draw something.
    66	     * @param absoluteXPosition
    67	     * @return
    68	     */
    69	    int getWindowXPosition(int absoluteXPosition) {
    70	        return getWindowXPositionWithOffset(absoluteXPosition, 0);
    71	    }
    72	
    73	    int getWindowYPosition(int absoluteYPosition) {
    74	        return getWindowYPositionWithOffset(absoluteYPosition, 0);
    75	    }
    76	
    77	    int getWindowXPositionFromCell(int cell) {
    78	        return getWindowXPositionFromCellWithOffset(cell, 0);
    79	    }
    80	
    81	    int getWindowYPositionFromCell(int cell) {
    82	        return getWindowYPositionFromCellWithOffset(cell, 0);
    83	    }
    84	
    85	    int getWindowXPositionFromCellWithOffset(int cell, int offset);
    86	    int getWindowYPositionFromCellWithOffset(int cell, int offset);
    87	
    88	    /**
    89	     * Translates an absolute X position into a position on the window. The offset is added after translating
    90	     * between absolute x coordinate to window coordinate. Zoom level is applied at last.
    91	     * @param absoluteXPosition
    92	     * @param offset
    93	     * @return
    94	     */
    95	    int getWindowXPositionWithOffset(int absoluteXPosition, int offset) {
    96	        return std::round(factorZoomLevel((absoluteXPosition - m_viewportStartX) + offset));
    97	    }
    98	
    99	    /**
   100	     * Translates an absolute Y position into a position on the window. The offset is added after translating
   101	     * between absolute x coordinate to window coordinate. Zoom level is applied at last.
   102	     * @param absoluteYPosition
   103	     * @param offset
   104	     * @return
   105	     */
   106	    int getWindowYPositionWithOffset(int absoluteYPosition, int offset) {
   107	        return std::round(factorZoomLevel((absoluteYPosition - m_viewportStartY) + offset) + m_heightOfTopBar);
   108	    }
   109	
   110	    // These methods need to use zoomfactor to properly calculate the position on the map
   111	    int getAbsMapMouseX(int mouseX) {
   112	        int iMouseX = divideByZoomLevel(mouseX);
   113	        return iMouseX + getViewportStartX();
   114	    }
   115	
   116	    int getAbsMapMouseY(int mouseY) {
   117	        int iMouseY = divideByZoomLevel(mouseY - m_heightOfTopBar);
   118	        return iMouseY + getViewportStartY();
   119	    }
   120	
   121	    int getViewportStartX() {
   122	        return m_viewportStartX;
   123	    }
   124	
   125	    int getViewportStartY() {
   126	        return m_viewportStartY;
   127	    }
   128	
   129	    int getViewportEndX() {
   130	        return m_viewportStartX + m_viewportWidth;
   131	    }
   132	
   133	    int getViewportEndY() {
   134	        return m_viewportStartY + m_viewportHeight;
   135	    }
   136	
   137	    int getViewportWidth() {
   138	        return m_viewportWidth;
   139	    }
   140	
   141	    int getViewportHeight() {
   142	        return m_viewportHeight;
   143	    }
   144	
   145	    int getViewportCenterX() {
   146	        return m_viewportStartX + (m_viewportWidth / 2);
   147	    }
   148	
   149	    int getViewportCenterY() {
   150	        return m_viewportStartY + (m_viewportHeight / 2);
   151	    }
   152	
   153	    void centerAndJumpViewPortToCell(int cell);
   154	
   155	    static constexpr int MaxViewportBookmarks = 5;
   156	
   157	    /**
   158	     * Saves the current viewport position and zoom level into the given bookmark slot (1-5).
   159	     */
   160	    void saveViewportBookmark(int bookmarkNumber);
   161	
   162	    /**
   163	     * Jumps to the viewport position and zoom level stored in the given bookmark slot (1-5).
   164	     * Does nothing if that slot has never been saved.
   165	     */
   166	    void jumpToViewportBookmark(int bookmarkNumber);
   167	
   168	    /**
   169	     * Clears all viewport bookmarks. Called when a new mission/skirmish starts.
   170	     */
   171	    void resetViewportBookmarks();
   172	
   173	    void trackToAbsPosition(float absX, float absY);
   174	
   175	    float getZoomedTileWidth() const {
   176	        return m_tileWidth;
   177	    }
   178	
   179	    float getZoomedTileHeight() const {
   180	        return m_tileHeight;
   181	    }
   182	
   183	    float factorZoomLevel(int value) {
   184	        return value * m_zoomLevel;
   185	    }
   186	
   187	    float factorZoomLevel(float value) {
   188	        return value * m_zoomLevel;
   189	    }
   190	
   191	    float divideByZoomLevel(int value) {
   192	        return value / m_zoomLevel;
   193	    }
   194	
   195	    float divideByZoomLevel(float value) {
   196	        return value / m_zoomLevel;
   197	    }
   198	
   199	    int getWindowWidth() {
   200	        return m_windowWidth;
   201	    }
   202	
   203	    int getWindowHeight() {
   204	        return m_windowHeight;
   205	    }
   206	
   207	    float getZoomLevel() {
   208	        return m_zoomLevel;
   209	    }
   210	
   211	    int getCellFromAbsolutePosition(int x, int y);
   212	    int getCellFromAbsolutePositionClamped(int x, int y);
   213	
   214	    void setViewportPosition(int x, int y);
   215	
   216	private:
   217	    // rendering coordinates, they are manipulated by zooming
   218	    float m_viewportStartX;
   219	    float m_viewportStartY;
   220	    int m_viewportWidth;
   221	    int m_viewportHeight;
   222	
   223	    // used for moving
   224	    float m_moveX;
   225	    float m_moveY;
   226	    float m_moveSpeedDrag;
   227	    float m_moveSpeedBorderOrKeys;
   228	    bool m_cameraEdgeMove;
   229	
   230	    bool m_keyPressedUp;
   231	    bool m_keyPressedDown;
   232	    bool m_keyPressedLeft;
   233	    bool m_keyPressedRight;
   234	
   235	    int m_heightOfTopBar;
   236	    int m_windowWidth;
   237	    int m_windowHeight;
   238	
   239	    // Zoom level, 1 == normal, > 1 is zooming in. < 1 is zooming out.
   240	    float m_zoomLevel;
   241	
   242	    // the calculated width and height, taking zoomlevel into account
   243	    float m_tileHeight;
   244	    float m_tileWidth;
   245	
   246	    // the map this camera is viewing
   247	    cMap *m_pMap;
   248	    MapGeometry *m_mapGeometry = nullptr;
   249	    cGameSettings *m_gameSettings;
   250	    cMouse *m_mouse;
   251	
   252	    void adjustViewport(float screenX, float screenY);
   253	
   254	    // Calculates viewport and tile width/height
   255	    void calibrate();
   256	
   257	    void keepViewportWithinReasonableBounds();
   258	
   259	    void zoomIn();
   260	    void zoomOut();
   261	
   262	    void onMouseMovedTo(const s_MouseEvent &event);
   263	
   264	    void onMouseRightButtonClicked(const s_MouseEvent &event);
   265	    void onMouseRightButtonPressed(const s_MouseEvent &event);
   266	
   267	    void setMoveX(float x, float moveSpeed);
   268	    void setMoveY(float y, float moveSpeed);
   269	
   270	    void onKeyHold(const cKeyboardEvent &event);
   271	    void onKeyPressed(const cKeyboardEvent &event);
   272	
   273	    struct sViewportBookmark {
   274	        bool isSet = false;
   275	        float x = 0.0f;
   276	        float y = 0.0f;
   277	        float zoomLevel = 1.0f;
   278	    };
   279	
   280	    std::array<sViewportBookmark, MaxViewportBookmarks> m_viewportBookmarks;
   281	};
```
### Путь по имени файла: cMap.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cMap.h$'
src/gameobjects/map/cMap.h
```
### src/gameobjects/map/cMap.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.h | nl -ba
     1	/**
     2	 * @file cMap.h
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
    19	#include "gameobjects/map/cCell.h"
    20	#include "gameobjects/map/FogMemory.hpp"
    21	#include "gameobjects/map/MapGeometry.hpp"
    22	#include "observers/cScenarioObserver.h"
    23	#include "sGameEvent.h"
    24	#include <map>
    25	#include <vector>
    26	#include <memory>
    27	
    28	#define TILESIZE_WIDTH_PIXELS 32
    29	#define TILESIZE_HEIGHT_PIXELS 32
    30	
    31	class cAbstractStructure;
    32	class cReinforcements;
    33	struct s_TerrainInfo;
    34	class GameContext;
    35	class cUnit;
    36	class cTextDrawer;
    37	struct sGameServices;
    38	
    39	class cGameSettings;
    40	class cInfoContext;
    41	class cGameObjectContext;
    42	class cScreenShake;
    43	class cEventEmitter;
    44	class cLog;
    45	class cPathFinder;
    46	class SDLDrawer;
    47	class Graphics;
    48	class cMapCamera;
    49	class cRectangle;
    50	
    51	/**
    52	 * Manages the game world grid and the state of every tile: terrain data, occupancy, passability,
    53	 * visibility and general map state. This is the main world-state container used by the game logic.
    54	 */
    55	class cMap : public cScenarioObserver {
    56	
    57	public:
    58	
    59	    cMap();
    60	    ~cMap();
    61	
    62	    void serviceInit(sGameServices* services);
    63	
    64	    void init(int width, int height);
    65	
    66	    virtual void onNotifyGameEvent(const s_GameEvent &event) override;
    67	
    68	    bool canDeployUnitAtCell(int iCell, int iUnitId);
    69	    bool canDeployUnitTypeAtCell(int iCell, int iUnitType);
    70	    bool occupiedByUnit(int iCell);
    71	    bool occupied(int iCell);
    72	    bool occupied(int iCll, int iUnitID);
    73	    bool occupiedInDimension(int iCell, int dimension);
    74	    bool occupiedByWallOrMountain(int iCell);
    75	    int findCloseMapBorderCellRelativelyToDestinationCel(int destinationCell);
    76	
    77	    int  mouse_draw_x(int mouseCell);
    78	    int  mouse_draw_y(int mouseCell);
    79	    void draw_units_2nd();
    80	    void draw_units();
    81	    void drawRememberedUnits();
    82	    void drawRevealedUnitsInFog();
    83	    void draw_bullets();
    84	
    85	    void smudge_increase(SmudgeType iType, int iCell);
    86	
    87	    void thinkFast();
    88	    void thinkNormal();
    89	    void thinkSlow();
    90	
    91	    void clear_all(int playerId);
    92	
    93	    /**
    94	     * Clear circular area, with `cell` as center and the circle being of `size` (in cells).
    95	     * Clears on map for playerId.
    96	     * @param cell
    97	     * @param size
    98	     * @param playerId
    99	     */
   100	    void clearShroud(int cell, int size, int playerId);
   101	
   102	    /**
   103	     * Clears shroud for all players at cell
   104	     * @param c
   105	     * @param size
   106	     */
   107	    void clearShroudForAllPlayers(int cell, int size);
   108	
   109	    /**
   110	     * returns pointer to cell or nullptr when not valid
   111	     * @param cellNr
   112	     * @return
   113	     */
   114	    [[nodiscard]] tCell *getCell(int cellNr) {
   115	        if (cellNr < 0) return nullptr;
   116	        if (cellNr >= m_mapGeometry->getMaxCells()) return nullptr;
   117	        return &m_cell[cellNr];
   118	    }
   119	
   120	    [[nodiscard]] int getCellType(int cellNr) {
   121	        tCell *pCell = getCell(cellNr);
   122	        if (pCell) return pCell->type;
   123	        return -1;
   124	    }
   125	
   126	    [[nodiscard]] std::vector<int> getAllCellsOfType(int cellType);
   127	
   128	    /**
   129	     * Returns ID at layer on cell. Returns -1 when layer or cell is not valid.
   130	     * @param cellNr
   131	     * @param idLayer
   132	     * @return
   133	     */
   134	    [[nodiscard]] int cellGetIdFromLayer(int cellNr, int idLayer) {
   135	        if (idLayer < 0 || idLayer >= 4) return -1; // safeguard layers
   136	        tCell *pCell = getCell(cellNr);
   137	        if (pCell) return pCell->id[idLayer];
   138	        return -1;
   139	    }
   140	
   141	    void cellSetIdForLayer(int cellNr, int idLayer, int id) {
   142	        if (idLayer < 0 || idLayer >= 4) return; // safeguard layers
   143	        tCell *pCell = getCell(cellNr);
   144	        if (!pCell) return;
   145	        pCell->id[idLayer] = id;
   146	    }
   147	
   148	    void cellResetIdFromLayer(int cellNr, int idLayer) {
   149	        if (idLayer < 0 || idLayer >= 4) return; // safeguard layers
   150	        tCell *pCell = getCell(cellNr);
   151	        if (!pCell) return;
   152	        pCell->id[idLayer] = -1;
   153	    }
   154	
   155	    [[nodiscard]] int getCellTile(int cellNr) {
   156	        tCell *pCell = getCell(cellNr);
   157	        if (pCell) return pCell->tile;
   158	        return -1;
   159	    }
   160	
   161	    [[nodiscard]] int getCellHealth(int cellNr) {
   162	        tCell *pCell = getCell(cellNr);
   163	        if (pCell) return pCell->health;
   164	        return -1;
   165	    }
   166	
   167	    [[nodiscard]] int getCellCredits(int cellNr) {
   168	        tCell *pCell = getCell(cellNr);
   169	        if (pCell) return pCell->credits;
   170	        return -1;
   171	    }
   172	
   173	    /**
   174	     * Returns if the cell is passable for non-infantry ground units
   175	     * @param cellNr
   176	     * @return
   177	     */
   178	    [[nodiscard]] bool isCellPassable(int cellNr) {
   179	        tCell *pCell = getCell(cellNr);
   180	        if (pCell) return pCell->passable;
   181	        return false;
   182	    }
   183	
   184	    /**
   185	     * Returns if the cell is passable for infantry ground units
   186	     * @param cellNr
   187	     * @return
   188	     */
   189	    [[nodiscard]] bool isCellPassableFoot(int cellNr) {
   190	        tCell *pCell = getCell(cellNr);
   191	        if (pCell) return pCell->passableFoot;
   192	        return false;
   193	    }
   194	
   195	    /**
   196	     * returns if id of layer units is filled (if so, a unit is recorded to be on this cell)
   197	     * @param cellNr
   198	     * @return
   199	     */
   200	    [[nodiscard]] int getCellIdUnitLayer(int cellNr) {
   201	        return cellGetIdFromLayer(cellNr, MAPID_UNITS);
   202	    }
   203	
   204	    /**
   205	     * returns if id of layer airborn units is filled (if so, an airborn unit is recorded to be on this cell)
   206	     * @param cellNr
   207	     * @return
   208	     */
   209	    [[nodiscard]] int getCellIdAirUnitLayer(int cellNr) {
   210	        return cellGetIdFromLayer(cellNr, MAPID_AIR);
   211	    }
   212	
   213	    /**
   214	     * returns if id of layer worms is filled (if so, a worm is recorded to be on this cell)
   215	     * @param cellNr
   216	     * @return
   217	     */
   218	    [[nodiscard]] int getCellIdWormsLayer(int cellNr) {
   219	        return cellGetIdFromLayer(cellNr, MAPID_WORMS);
   220	    }
   221	
   222	    /**
   223	     * returns if id of layer structures is filled (if so, a structure is recorded to be on this cell)
   224	     * @param cellNr
   225	     * @return
   226	     */
   227	    [[nodiscard]] int getCellIdStructuresLayer(int cellNr) {
   228	        return cellGetIdFromLayer(cellNr, MAPID_STRUCTURES);
   229	    }
   230	
   231	    [[nodiscard]] bool isCellPassableForFootUnits(int cellNr) {
   232	        bool isPassable = isCellPassableFoot(cellNr); // -> this will block for ALL units, so don't do this
   233	        int unitId = getCellIdUnitLayer(cellNr);
   234	        int strucId = getCellIdStructuresLayer(cellNr);
   235	        return isPassable && unitId < 0 && strucId < 0;
   236	    }
   237	
   238	    /**
   239	     * Finds the closest structure (compared to cell param) of required type, for player.
   240	     * It also checks if the structure is not occupied by any unit AND that no other unit is already heading towards the structure.
   241	     *
   242	     * Returns nullptr if none found.
   243	     *
   244	     * @return pointer to cAbstractStructure
   245	     */
   246	    [[nodiscard]] cAbstractStructure *findClosestAvailableStructureTypeWhereNoUnitIsHeadingTo(int cell, int structureType, cPlayer *pPlayer);
   247	
   248	    /**
   249	     * Finds the closest structure (compared to cell param) of required type, for player.
   250	     * It also checks if the structure is not occupied by any unit. It does not care if any other unit is already heading for this structure.
   251	     *
   252	     * Returns nullptr if none found.
   253	     *
   254	     * @return pointer to cAbstractStructure
   255	     */
   256	    [[nodiscard]] cAbstractStructure *findClosestAvailableStructureType(int cell, int structureType, cPlayer *pPlayer);
   257	
   258	    /**
   259	     * Finds the closest structure (compared to cell param) of required type, for player.
   260	     * It does not care if structure is occupied nor does it care if any other unit is already heading for this structure.
   261	     *
   262	     * Returns nullptr if none found.
   263	     *
   264	     * @return pointer to cAbstractStructure
   265	     */
   266	    [[nodiscard]] cAbstractStructure *findClosestStructureType(int cell, int structureType, cPlayer *player);
   267	
   268	    void cellTakeDamage(int cellNr, int damage);
   269	
   270	    void cellTakeCredits(int cellNr, int amount) {
   271	        tCell *pCell = getCell(cellNr);
   272	        if (pCell) pCell->credits -= amount;
   273	    }
   274	
   275	    void cellGiveHealth(int cellNr, int hp) {
   276	        tCell *pCell = getCell(cellNr);
   277	        if (pCell) pCell->health += hp;
   278	    }
   279	
   280	    void cellGiveCredits(int cellNr, int amount) {
   281	        tCell *pCell = getCell(cellNr);
   282	        if (pCell) pCell->credits += amount;
   283	    }
   284	
   285	    void cellChangeType(int cellNr, int type);
   286	
   287	    void cellChangeHealth(int cellNr, int value) {
   288	        tCell *pCell = getCell(cellNr);
   289	        if (pCell) pCell->health = value;
   290	    }
   291	
   292	    void cellChangeTile(int cellNr, int tile) {
   293	        tCell *pCell = getCell(cellNr);
   294	        if (pCell) pCell->tile = tile;
   295	    }
   296	
   297	    void cellChangeCredits(int cellNr, int value) {
   298	        tCell *pCell = getCell(cellNr);
   299	        if (pCell) pCell->credits = value;
   300	    }
   301	
   302	    void cellChangeSmudgeTile(int cellNr, int value) {
   303	        tCell *pCell = getCell(cellNr);
   304	        if (pCell) pCell->smudgetile = value;
   305	    }
   306	
   307	    void cellChangeSmudgeType(int cellNr, std::optional<SmudgeType> value) {
   308	        tCell *pCell = getCell(cellNr);
   309	        if (pCell) pCell->smudgetype = value;
   310	    }
   311	
   312	    void cellChangePassable(int cellNr, bool value) {
   313	        tCell *pCell = getCell(cellNr);
   314	        if (pCell) pCell->passable = value;
   315	    }
   316	
   317	    void cellChangePassableFoot(int cellNr, bool value) {
   318	        tCell *pCell = getCell(cellNr);
   319	        if (pCell) pCell->passableFoot = value;
   320	    }
   321	
   322	    void cellInit(int cellNr);
   323	
   324	    void remove_id(int iIndex, int iIDType);    // removes ID of IDtype (unit/structure), etc
   325	
   326	    [[nodiscard]] bool isVisible(int iCell, int iPlayer);
   327	
   328	    /**
   329	     * is Cell visible for player?
   330	     * @param iCell
   331	     * @param
   332	     */
   333	    [[nodiscard]] bool isVisible(int iCell, cPlayer *thePlayer);
   334	
   335	    /**
   336	     * Is cell within sight range of any unit/structure of player right now? When false, but the cell
   337	     * is visible, the cell is 'fogged' (discovered earlier, but not observed at this moment).
   338	     * @param iCell
   339	     * @param iPlayer
   340	     */
   341	    [[nodiscard]] bool isSeen(int iCell, int iPlayer);
   342	
   343	    /**
   344	     * What the player remembers of the terrain of a fogged cell (purely visual, never targetable).
   345	     * Only kept for the human player.
   346	     * @return nullptr when nothing is remembered: draw the live terrain then
   347	     */
   348	    [[nodiscard]] const s_RememberedTerrain *getRememberedTerrain(int iCell, int iPlayer) const;
   349	
   350	    /**
   351	     * The structure slice the player remembers on a fogged cell (purely visual, never targetable).
   352	     * Only kept for the human player.
   353	     * @return nullptr when no structure is remembered
   354	     */
   355	    [[nodiscard]] const s_RememberedStructure *getRememberedStructure(int iCell, int iPlayer) const;
   356	
   357	    /**
   358	     * The unit (base type, hull and turret) the player remembers on a fogged cell. Purely visual,
   359	     * never targetable or hoverable. Only kept for the human player.
   360	     * @return nullptr when no unit is remembered
   361	     */
   362	    [[nodiscard]] const s_RememberedUnit *getRememberedUnit(int iCell, int iPlayer) const;
   363	
   364	    /**
   365	     * Is this unit hidden from the human player because it stands in the fog of war? Units of the
   366	     * human player (and its allies) are never hidden.
   367	     * @param pUnit
   368	     */
   369	    [[nodiscard]] bool isHiddenByFogOfWar(cUnit *pUnit);
   370	
   371	    /**
   372	     * Is this structure hidden from the human player because none of its cells is in sight? Structures
   373	     * of the human player (and its allies) are never hidden. The player only sees the remembered
   374	     * structure (see getRememberedStructure) then.
   375	     * @param pStructure
   376	     */
   377	    [[nodiscard]] bool isHiddenByFogOfWar(cAbstractStructure *pStructure);
   378	
   379	    /**
   380	     * Makes cell visible for player (ID)
   381	     * @param iCell
   382	     * @param iPlayer
   383	     */
   384	    void setVisibleFor(int iCell, int iPlayer) {
   385	        setVisible(iCell, iPlayer, true);
   386	    }
   387	
   388	    /**
   389	     * Makes cell visible for player (pointer)
   390	     * @param iCell
   391	     * @param pPlayer
   392	     */
   393	    void setVisibleFor(int iCell, cPlayer *pPlayer);
   394	
   395	    /**
   396	     * Returns the amount of cells of a specific type
   397	     * @param cellType
   398	     * @return
   399	     */
   400	    [[nodiscard]] int getTotalCountCellType(int cellType);
   401	
   402	    /**
   403	     * Depending on terrain type, return amount of 'slow down' is experienced by ground unit (this assumes it is about
   404	     * ground units). 0 means no slow down (SLAB), the higher the more slow down. Default is 1 (slight slow down).
   405	     * @param i
   406	     * @return
   407	     */
   408	    [[nodiscard]] int getCellSlowDown(int i);
   409	
   410	    int getMaxCells() const {
   411	        return m_mapGeometry->getMaxCells();
   412	    }
   413	
   414	    void createCell(int cell, int terrainType, int tile);
   415	
   416	    void clearAllCells();
   417	
   418	    /**
   419	     * Finds the nearest spice Bloom near cell. If param <b>iCell</b> &lt; 0 then use middle of map.
   420	     * If no close cell is found
   421	     * a fall back of 'select any spice bloom randomly' is performed.
   422	     * @param iCell
   423	     * @return > -1 if found or < 0 upon failure
   424	     */
   425	    [[nodiscard]] int findNearestSpiceBloom(int iCell);
   426	
   427	    /**
   428	     * Returns true if a structure may be placed at this cell. This evaluates if terrain type allows placement AND
   429	     * if any other structure occupies this cell. It does *not* check if a unit is at this cell. If invalid cell
   430	     * is given this also returns false.
   431	     *
   432	     * @param cll
   433	     * @return
   434	     */
   435	    [[nodiscard]] bool isValidTerrainForStructureAtCell(int cell);
   436	
   437	    [[nodiscard]] int getRandomCellFromWithRandomDistanceValidForUnitType(int cell, int minRange, int maxRange, int unitType);
   438	
   439	    [[nodiscard]] bool isStructureVisible(cAbstractStructure *pStructure, int iPlayer);
   440	
   441	    [[nodiscard]] bool isStructureVisible(cAbstractStructure *pStructure, cPlayer *thePlayer);
   442	
   443	    [[nodiscard]] int findNearByValidDropLocation(int cell, int range, int unitTypeToDrop);
   444	    [[nodiscard]] int findNearByValidDropLocation(int cell, int minRange, int maxRange, int unitTypeToDrop);
   445	
   446	    [[nodiscard]] int findRandomCellToMoveToForSandworm();
   447	    [[nodiscard]] bool isCellPassableForWorm(int cell);
   448	
   449	    [[nodiscard]] bool isValidTerrainForConcreteAtCell(int cell);
   450	
   451	    void detonateSpiceBloom(int cell);
   452	
   453	    void setAutoDetonateSpiceBlooms(bool value) {
   454	        m_bAutoDetonateSpiceBlooms = value;
   455	    }
   456	
   457	    void setAutoSpawnSpiceBlooms(bool value) {
   458	        m_bAutoSpawnSpiceBlooms = value;
   459	    }
   460	
   461	    void setDesiredAmountOfWorms(int value);
   462	
   463	    void setReinforcements(cReinforcements* reinforcements);
   464	
   465	    [[nodiscard]] MapGeometry *getGeometry() const;
   466	
   467	    [[nodiscard]] cPathFinder *getPathFinder() const {
   468	        return m_pathFinder.get();
   469	    }
   470	
   471	    void setTerrainInfo(s_TerrainInfo* terrainInfo);
   472	private:
   473	    void setVisible(int iCell, int iPlayer, bool flag);
   474	
   475	    void updateFogOfWar();
   476	    void updateFogMemory();
   477	    std::optional<s_RememberedStructure> describeStructureOnCell(int iCell);
   478	    std::optional<s_RememberedUnit> describeUnitOnCell(int iCell);
   479	    void markSeen(int cell, int size, int playerId);
   480	
   481	    std::vector<tCell> m_cell;
   482	    std::vector<bool> m_wasSeen;  // human iSeen before the latest fog update (reused buffer)
   483	    FogMemory m_fogMemory;  // what the human player last saw of fogged cells
   484	    GameContext *m_ctx = nullptr;
   485	    cGameSettings *m_settings = nullptr;
   486	    cInfoContext *m_infos = nullptr;
   487	    cGameObjectContext *m_objects = nullptr;
   488	    cScreenShake *m_screenShake = nullptr;
   489	    cEventEmitter *m_eventEmitter = nullptr;
   490	    cMapCamera *m_mapCamera = nullptr;
   491	    cRectangle *m_mapViewport = nullptr;
   492	    cLog *m_log = nullptr;
   493	    cTextDrawer *m_textDrawer = nullptr;
   494	    SDLDrawer *m_sdlDrawer = nullptr;
   495	    Graphics *m_gfxdata = nullptr;
   496	
   497	    std::unique_ptr<MapGeometry> m_mapGeometry;
   498	    std::unique_ptr<cPathFinder> m_pathFinder;
   499	
   500	    // Spice Blooms related
   501	    bool m_bAutoSpawnSpiceBlooms;
   502	    bool m_bAutoDetonateSpiceBlooms;
   503	    int m_iTIMER_blooms;
   504	    std::map<int, int> m_mBloomTimers;
   505	
   506	    cReinforcements* m_reinforcements = nullptr;
   507	    s_TerrainInfo* m_terrainInfo = nullptr;
   508	    // Sandworms related
   509	    int m_iDesiredAmountOfWorms;
   510	    int m_iTIMER_respawnSandworms;
   511	
   512	    // Scrolling around map, timer based
   513	    int m_TIMER_scroll;
   514	    int m_iScrollSpeed;
   515	
   516	    void drawUnitDebug(cUnit *pUnit) const;
   517	
   518	    // thinking related
   519	    void thinkAutoDetonateSpiceBlooms();
   520	    void thinkAboutSpawningNewSpiceBlooms();
   521	    void thinkAboutRespawningWorms();
   522	
   523	    // event related
   524	    void onEntityDestroyed(const s_GameEvent &event);
   525	    void onEntityCreated(const s_GameEvent &event);
   526	
   527	    void setSandwormRespawnTimer();
   528	    void evaluateIfWeShouldSetTimerToRespawnWorm();
   529	};
```
### Путь по имени файла: cDrawManager.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cDrawManager.h$'
src/managers/cDrawManager.h
```
### src/managers/cDrawManager.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.h | nl -ba
     1	/**
     2	 * @file cDrawManager.h
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
    19	class cBuildingListDrawer;
    20	class cMapDrawer;
    21	class cMessageDrawer;
    22	class cMiniMapDrawer;
    23	class cMouseDrawer;
    24	class cOrderDrawer;
    25	class cParticleDrawer;
    26	class cPlaceItDrawer;
    27	class CreditsDrawer;
    28	//#include "drawers/cSideBarDrawer.h"
    29	#include "drawers/cStructureDrawer.h"
    30	
    31	#include "observers/cInputObserver.h"
    32	struct s_MouseEvent;
    33	
    34	#include <memory>
    35	
    36	class cPlayer;
    37	struct SDL_Surface;
    38	class Texture;
    39	class GameContext;
    40	class Graphics;
    41	class SDLDrawer;
    42	class cSideBarDrawer;
    43	class GameContext;
    44	class GameStateTransition;
    45	class cGameObjectContext;
    46	class cMapCamera;
    47	class cMouse;
    48	class cRectangle;
    49	class cGameSettings;
    50	class cStructureUtils;
    51	struct sGameServices;
    52	
    53	/**
    54	 * Candidate class for PlayingMissionState (draw function?), but also for SelectYourNextConquestState (drawing
    55	 * message bar is re-used there)
    56	 */
    57	class cDrawManager : cInputObserver {
    58	
    59	public:
    60	    explicit cDrawManager(GameContext *ctx, cPlayer *thePlayer, sGameServices *services);
    61	    ~cDrawManager();
    62	
    63	    void drawCombatState();
    64	
    65	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    66	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    67	
    68	    cMiniMapDrawer *getMiniMapDrawer() {
    69	        return m_miniMapDrawer.get();
    70	    }
    71	
    72	    cOrderDrawer *getOrderDrawer() {
    73	        return m_orderDrawer.get();
    74	    }
    75	
    76	    cMouseDrawer *getMouseDrawer() {
    77	        return m_mouseDrawer.get();
    78	    }
    79	
    80	    cPlaceItDrawer *getPlaceItDrawer() {
    81	        return m_placeitDrawer.get();
    82	    }
    83	
    84	    cBuildingListDrawer *getBuildingListDrawer();
    85	
    86	    void drawMouse();
    87	
    88	    void drawCombatMouse();
    89	
    90	    void setPlayerToDraw(cPlayer *playerToDraw);
    91	
    92	    void think();
    93	
    94	    void init();
    95	
    96	    void missionInit();
    97	
    98	    void thinkFast_statePlaying();
    99	
   100	    void thinkFast();
   101	
   102	    void drawMessageBar();
   103	
   104	    void setMessage(std::string msg, bool keepMessage = false);
   105	
   106	    [[nodiscard]] std::string getMessage() const;
   107	
   108	    void setKeepMessage(bool value);
   109	
   110	    void regionInit(int offsetX, int offsetY);
   111	
   112	    bool hasMessage();
   113	
   114	    void reset();
   115	protected:
   116	    void drawSidebar();
   117	
   118	    void drawCredits();
   119	
   120	    void drawStructurePlacing();
   121	
   122	    void drawMessage();
   123	
   124	    void drawRallyPoint();
   125	
   126	    void drawTopBarBackground();
   127	
   128	private:
   129	    void drawDebugInfoUsages() const;
   130	
   131	    // void drawNotifications();
   132	
   133	    // Properties:
   134	    std::unique_ptr<cSideBarDrawer> m_sidebarDrawer;
   135	    std::unique_ptr<CreditsDrawer> m_creditsDrawer;
   136	    std::unique_ptr<cOrderDrawer> m_orderDrawer;
   137	    std::unique_ptr<cMapDrawer> m_mapDrawer;
   138	    std::unique_ptr<cMiniMapDrawer> m_miniMapDrawer;
   139	    std::unique_ptr<cParticleDrawer> m_particleDrawer;
   140	    std::unique_ptr<cMessageDrawer> m_messageDrawer;
   141	    std::unique_ptr<cPlaceItDrawer> m_placeitDrawer;
   142	    std::unique_ptr<cStructureDrawer> m_structureDrawer;
   143	    Color m_sidebarColor;
   144	    bool m_drawToolTip = false;
   145	    // TODO: bullet/projectile drawer
   146	    cPlayer *m_player = nullptr;
   147	    GameContext *m_ctx = nullptr;
   148	    cTextDrawer *m_textDrawer = nullptr;
   149	    SDLDrawer* m_sdlDrawer = nullptr;
   150	    Graphics* m_gfxinter = nullptr;
   151	    Graphics* m_gfxdata = nullptr;
   152	    std::unique_ptr<cMouseDrawer> m_mouseDrawer;
   153	    GameStateTransition* m_stateTransitions = nullptr;
   154	    cMouse* m_mouse = nullptr;
   155	    cRectangle* m_mapViewport = nullptr;
   156	    cGameObjectContext* m_objects = nullptr;
   157	    cMapCamera* m_mapCamera = nullptr;
   158	    cGameSettings* m_gameSettings = nullptr;
   159	    cStructureUtils* m_structureUtils = nullptr;
   160	    sGameServices* m_services = nullptr;
   161	
   162	    void onKeyDown(const cKeyboardEvent &event);
   163	
   164	    void onKeyPressed(const cKeyboardEvent &event);
   165	};
```
### Путь по имени файла: cSideBar.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cSideBar.h$'
src/sidebar/cSideBar.h
```
### src/sidebar/cSideBar.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/cSideBar.h | nl -ba
     1	/**
     2	 * @file cSideBar.h
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
    16	/*
    17	 * cSideBar.h
    18	 *
    19	 * The sidebar consists out of several parts:
    20	 * - buildLists (the icons that represent them, and a list of icons of the
    21	 *   selected list)
    22	 * - a minimap
    23	 * - capacity indicators
    24	 *
    25	 *  Created on: Aug 1, 2009
    26	 *      Author: Stefan
    27	 */
    28	
    29	#pragma once
    30	
    31	#include "cBuildingList.h"
    32	#include "cBuildingListItem.h"
    33	#include "sGameEvent.h"
    34	#include "controls/sMouseEvent.h"
    35	
    36	class cPlayer;
    37	class cDrawManager;
    38	class cGameSettings;
    39	class AudioContext;
    40	class cEventEmitter;
    41	struct sGameServices;
    42	
    43	//// List ID's corresponding buttons
    44	//#define LIST_NONE        0
    45	//#define LIST_CONSTYARD    1
    46	//#define LIST_FOOT_UNITS    2 // infantry, soldier, trooper, troopers, etc.
    47	//#define LIST_UNITS        3 // quad, trike, tanks, air units
    48	//#define LIST_STARPORT    4 // special list to order stuff
    49	//#define LIST_PALACE        5 // REMOVE? (ie super weapon icon should always show top left/right?)
    50	//#define LIST_UPGRADES    6 // possible upgrades
    51	//#define LIST_MAX        7 // max amount of lists
    52	
    53	inline constexpr int SUBLIST_CONSTYARD = 0;  // structures
    54	inline constexpr int SUBLIST_LIGHTFCTRY = 1; // quad, trike, etc
    55	inline constexpr int SUBLIST_HEAVYFCTRY = 2; // tanks
    56	inline constexpr int SUBLIST_HIGHTECH = 3; // orni, carry-all
    57	
    58	inline constexpr int SUBLIST_INFANTRY = 4; // soldier, infantry
    59	inline constexpr int SUBLIST_TROOPERS = 5; // trooper, troopers
    60	
    61	/**
    62	 * Basically a container:
    63	 * - building lists
    64	 * - minimap
    65	 * - capacities (max spice, max power)
    66	 *
    67	 * NOTE: Use the cSideBarFactory to construct a cSideBar class.
    68	 *
    69	 */
    70	class cSideBar {
    71	
    72	public:
    73	    explicit cSideBar(cPlayer *thePlayer);
    74	
    75	    ~cSideBar();
    76	
    77	    cBuildingList *getList(int listId) {
    78	        return m_lists[listId];
    79	    }
    80	
    81	    cBuildingList *getList(eListType listType) {
    82	        return getList(eListTypeAsInt(listType));
    83	    }
    84	
    85	    bool startBuildingItemIfOk(eListType listType, int buildId) const;
    86	
    87	    void setList(eListType listType, cBuildingList *list);
    88	
    89	    int getSelectedListID() {
    90	        return m_selectedListID;
    91	    }
    92	    cBuildingListItem *getBuildingListItem(eListType listType, int buildId) const;
    93	
    94	    void think();    // timer based
    95	
    96	    // set
    97	    // no set Player, re-create Sidebar object instead if needed
    98	    void setSelectedListId(eListType value);
    99	
   100	    static const int LIST_MAX = 7;
   101	
   102	    static const int VerticalCandyBarWidth = 24;
   103	    inline static int SidebarWidthWithoutCandyBar = 200;
   104	    inline static int SidebarWidth = SidebarWidthWithoutCandyBar + VerticalCandyBarWidth;
   105	    static constexpr int TopBarHeight = 42;
   106	    static void configureLayout(int logicalWidth, int logicalHeight);
   107	    static const int HeightOfMinimap = 200 + 8;
   108	    static const int WidthOfMinimap = 200;
   109	    static const int PowerBarMarginHeight = 32; // for a power icon
   110	
   111	    // Horizontal candybar is below minimap
   112	    static const int HorizontalCandyBarHeight = 12;
   113	
   114	    static const int HeightOfListButton = 34;
   115	
   116	    static const int TotalHeightBeforePowerBarStarts =
   117	        TopBarHeight + HeightOfMinimap + HorizontalCandyBarHeight + PowerBarMarginHeight;
   118	
   119	    void serviceInit(sGameServices* services);
   120	
   121	    void onNotifyMouseEvent(const s_MouseEvent &event);
   122	
   123	    void cancelBuildingListItem(cBuildingListItem *item);
   124	
   125	    void onNotify(const s_GameEvent &event);
   126	
   127	    void findFirstActiveListAndSelectIt();
   128	
   129	private:
   130	    void onMouseAt(const s_MouseEvent &event);
   131	    void onMouseClickedLeft(const s_MouseEvent &event);
   132	    void onMouseClickedRight(const s_MouseEvent &event);
   133	
   134	    // the lists:
   135	    cBuildingList *m_lists[LIST_MAX];
   136	    cPlayer *m_player;
   137	    cDrawManager* m_drawManager = nullptr;
   138	    cGameSettings* m_settings = nullptr;
   139	    AudioContext* m_audioContext = nullptr;
   140	    cEventEmitter* m_eventEmitter = nullptr;
   141	
   142	    bool m_isMouseOverSidebarValue;
   143	
   144	    int m_selectedListID;
   145	
   146	    bool startBuildingItemIfOk(cBuildingListItem *item) const;
   147	
   148	    void drawMessageBarWithItemInfo(cBuildingListItem *item) const;
   149	
   150	    void thinkProgressAnimation();
   151	
   152	    cBuildingList *getSelectedList() const;
   153	
   154	    void onListBecameUnavailableEvent(const BuildingEvent *event);
   155	
   156	    void onListBecameAvailableEvent(const BuildingEvent *event);
   157	
   158	    void onSpecialReadyToDeployEvent(const BuildingEvent *event) const;
   159	
   160	    void onListItemReadyToPlaceEvent(const BuildingEvent *event) const;
   161	};
```
### Путь по имени файла: cBuildingList.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cBuildingList.h$'
src/sidebar/cBuildingList.h
```
### src/sidebar/cBuildingList.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/cBuildingList.h | nl -ba
     1	/**
     2	 * @file cBuildingList.h
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
    18	#include "cSideBar.h"
    19	#include "definitions.h"
    20	
    21	#include "sidebar/cBuildingListItem.h"
    22	
    23	#include <array>
    24	#include "utils/Color.hpp"
    25	
    26	class cItemBuilder;
    27	class cInfoContext;
    28	class cGameSettings;
    29	class cEventEmitter;
    30	class cScreenFader;
    31	struct sGameServices;
    32	
    33	/**
    34	 *
    35	 * This is a class, representing a list of icons that can be selected and built.
    36	 *
    37	 * Per list one item can be built at a time. Each list has therefore a timer.
    38	 *
    39	 * A list has also a corresponding icon the user can click on, in order to view the
    40	 * lists contents. (these are the icons left to the building list). Each list has the
    41	 * ID of the unpressed icon picture, and also the coordinates for this icon.
    42	 *
    43	 */
    44	class cBuildingList {
    45	public:
    46	    explicit cBuildingList(eListType listType);
    47	
    48	    ~cBuildingList();
    49	
    50	    cBuildingListItem *getItem(int i);    // return building list item in array at position.
    51	    cBuildingListItem *getFirstItemInSubList(int sublistId);
    52	    cBuildingListItem *getItemToPlace();        // return building list item with placeIt = true.
    53	    cBuildingListItem *getItemToDeploy();       // return building list item with deployIt = true.
    54	
    55	    bool removeItemFromList(cBuildingListItem *item);
    56	
    57	    bool removeItemFromList(int position);
    58	
    59	    bool removeItemFromListByBuildId(int type);
    60	
    61	    void addUpgradeToList(int structureTypeToUpgrade);
    62	
    63	    void addStructureToList(int structureType, int subList);
    64	
    65	    void addSpecialToList(int specialType, int subList);
    66	
    67	    void addUnitToList(int unitType, int subList);
    68	
    69	    bool addItemToList(cBuildingListItem *item);
    70	
    71	    bool isOverButton(int x, int y);
    72	
    73	    void removeAllItems();
    74	
    75	    bool isItemInList(cBuildingListItem *item);
    76	
    77	    // get
    78	    bool isSelected() {
    79	        return m_selected;
    80	    }
    81	
    82	    int getLastClickedId() {
    83	        return m_lastClickedId;
    84	    }
    85	
    86	    int getButtonIconIdPressed() {
    87	        return m_buttonIconIdPressed;
    88	    }
    89	
    90	    int getButtonIconIdUnpressed() {
    91	        return m_buttonIconIdUnpressed;
    92	    }
    93	
    94	    int getButtonDrawX() {
    95	        return m_buttonDrawX;
    96	    }
    97	
    98	    int getButtonDrawY() {
    99	        return m_buttonDrawY;
   100	    }
   101	
   102	    int getButtonWidth() const {
   103	        return m_buttonWidth;
   104	    }
   105	
   106	    int getButtonHeight() const {
   107	        return m_buttonHeight;
   108	    }
   109	
   110	    bool isAvailable() {
   111	        return m_maxItems > 0;
   112	    }
   113	
   114	    int getItemCount() const {
   115	        return m_maxItems;
   116	    }
   117	
   118	    std::array<int, 6> isBuildingItem();
   119	
   120	    cBuildingListItem *getItemByBuildId(int buildId);
   121	
   122	    // set
   123	    void setSelected(bool value) {
   124	        m_selected = value;
   125	    }
   126	
   127	    void setStatusPendingUpgrade(int subListId);
   128	
   129	    void setStatusPendingBuilding(int subListId);
   130	
   131	    void setStatusAvailable(int subListId);
   132	
   133	    void setButtonIconIdPressed(int iconId) {
   134	        m_buttonIconIdPressed = iconId;
   135	    }
   136	
   137	    void setButtonIconIdUnpressed(int iconId) {
   138	        m_buttonIconIdUnpressed = iconId;
   139	    }
   140	
   141	    void setButtonWidth(int value) {
   142	        m_buttonWidth = value;
   143	    }
   144	
   145	    void setButtonHeight(int value) {
   146	        m_buttonHeight = value;
   147	    }
   148	
   149	    void setButtonDrawX(int value) {
   150	        m_buttonDrawX = value;
   151	    }
   152	
   153	    void setButtonDrawY(int value) {
   154	        m_buttonDrawY = value;
   155	    }
   156	
   157	    void setLastClickedId(int value) {
   158	        m_lastClickedId = value;
   159	    }
   160	
   161	    /**
   162	    * type of list (see cSideBarFactory) , ie 0 = CONSTYARD, last is IX (sUpgradeInfo), etc.
   163	    * @param value
   164	    */
   165	    eListType getType() {
   166	        return m_listType;
   167	    }
   168	
   169	    [[nodiscard]] bool isType(const eListType type) const
   170	    {
   171	        return m_listType == type;
   172	    }
   173	
   174	    void removeAllSublistItems(int sublistId);
   175	
   176	    void clearList();
   177	
   178	    void resetTimesOrderedForAllItems();
   179	
   180	    void setItemBuilder(cItemBuilder *value);
   181	    void serviceInit(sGameServices* services);
   182	
   183	    void startFlashing();
   184	
   185	    bool isFlashing() {
   186	        return m_TIMER_flashing > 0;
   187	    }
   188	
   189	    Color getFlashingColor();
   190	
   191	    void think();
   192	
   193	    void stopFlashing();
   194	
   195	protected:
   196	    // nothing
   197	
   198	private:
   199	    int m_lastClickedId;    // last clicked item id
   200	    int m_buttonIconIdPressed;    // the button to draw at the left of the list when pressed (selected)
   201	    int m_buttonIconIdUnpressed;    // the button to draw at the left of the list when unpressed
   202	    int m_buttonDrawX;
   203	    int m_buttonDrawY;
   204	    int m_buttonWidth;
   205	    int m_buttonHeight;
   206	
   207	    int m_TIMER_flashing;
   208	
   209	    int m_maxItems;         // how many items have been set in the list?
   210	
   211	    bool m_selected;          // is this list selected at sidebar or not?
   212	
   213	    // the list of icons
   214	    cBuildingListItem *m_items[MAX_ITEMS];
   215	
   216	    cItemBuilder *m_itemBuilder;
   217	    cInfoContext* m_info = nullptr;
   218	    cGameSettings* m_settings = nullptr;
   219	    cEventEmitter* m_eventEmitter = nullptr;
   220	    cScreenFader* m_screenFader = nullptr;
   221	
   222	    int getFreeSlot();
   223	
   224	    eListType m_listType;
   225	};
```
### Путь по имени файла: cBuildingListItem.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cBuildingListItem.h$'
src/sidebar/cBuildingListItem.h
```
### src/sidebar/cBuildingListItem.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/cBuildingListItem.h | nl -ba
     1	/**
     2	 * @file cBuildingListItem.h
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
    16	/**
    17	 * a cListItem is  used within a BuildingList , it has a picture and any unit or
    18	 * structure ID attached. At the same time this item is responsible for 'building'
    19	 * the item it represents. It has therefor also other properties; progress a timer, etc.
    20	 *
    21	 *
    22	 */
    23	#pragma once
    24	
    25	#include <string>
    26	#include "include/enums/BuildEnums.h"
    27	#include "include/enums/ListEnums.h"
    28	
    29	class cBuildingList;
    30	class cInfoContext;
    31	class cGameSettings;
    32	struct s_SpecialInfo;
    33	struct s_UpgradeInfo;
    34	struct s_UnitInfo;
    35	struct s_StructureInfo;
    36	struct s_TerrainInfo;
    37	
    38	class cBuildingListItem {
    39	
    40	public:
    41	    ~cBuildingListItem();
    42	
    43	    // uber constructor
    44	    cBuildingListItem(eBuildType type, int buildId, int cost, int icon, cBuildingList *list, int subList, bool queuable);
    45	
    46	    // easier constructors (they have no LIST, this is intentional and assigned later to the item by add**toList functions in the cBuildingList.cpp class
    47	    cBuildingListItem(int theID, s_StructureInfo entry, int subList);
    48	    cBuildingListItem(int theID, s_SpecialInfo entry, int subList);
    49	    cBuildingListItem(int theID, s_UnitInfo entry, int subList);
    50	    cBuildingListItem(int theID, s_UpgradeInfo entry);
    51	
    52	    void serviceInit(cInfoContext* info, cGameSettings* settings);
    53	
    54	    static const int DefaultTimerCap = 35;
    55	    static const int DebugTimerCap = 2;
    56	
    57	    // getters
    58	    int getTotalBuildTimeInMs();
    59	    int getProgressBuildTimeInMs(); // how much time has passed for build item
    60	    int getIconId() {
    61	        return m_icon;
    62	    }
    63	    std::string getInfo();
    64	
    65	    std::string getTypeString();
    66	    std::string getNameString();
    67	
    68	    /**
    69	     * The buildId is the 'type', ie if eBuildType == STRUCTURE, then buildId refers to what *kind* of structure. Ie, the
    70	     * structure type. This could be WINDTRAP, REFINERY, etc. If eBuildType is UNIT, then buildId is for TANK, QUAD, etc.
    71	     *
    72	     * @return
    73	     */
    74	    int getBuildId() {
    75	        return m_buildId;
    76	    }
    77	
    78	    /**
    79	     * The index of the sublist
    80	     * @return
    81	     */
    82	    int getSubList() {
    83	        return m_subList;
    84	    }
    85	
    86	    eBuildType getBuildType() {
    87	        return m_type;
    88	    }
    89	    int getBuildCost() const {
    90	        return m_cost;
    91	    }
    92	    int getProgress() {
    93	        return m_progress;
    94	    }
    95	    bool isBuilding() {
    96	        return isState(eBuildingListItemState::BUILDING) || isState(eBuildingListItemState::PAUSED);
    97	    }
    98	    bool isPaused() {
    99	        return isState(eBuildingListItemState::PAUSED);
   100	    }
   101	    bool isState(eBuildingListItemState value) {
   102	        return m_state == value;
   103	    }
   104	
   105	    /**
   106	     * Returns if item is available to build, if not, then it won't be drawn
   107	     * @return
   108	     */
   109	    bool isAvailable() {
   110	        return isState(eBuildingListItemState::AVAILABLE) || isState(eBuildingListItemState::BUILDING);
   111	    }
   112	
   113	    /**
   114	     * Item is pending because upgrade is in progress (used for building items)
   115	     * @return
   116	     */
   117	    bool isPendingUpgrading() {
   118	        return isState(eBuildingListItemState::PENDING_UPGRADE);
   119	    }
   120	
   121	    /**
   122	     * Item is pending because building is in progress (used for upgrade items)
   123	     * @return
   124	     */
   125	    bool isPendingBuilding() {
   126	        return isState(eBuildingListItemState::PENDING_BUILDING);
   127	    }
   128	
   129	    int getTimesToBuild() {
   130	        return m_timesToBuild;
   131	    }
   132	    int getSlotId() {
   133	        return m_slotId;    // return index of items[] array (set after adding item to list, default is < 0)
   134	    }
   135	    int getTimesOrdered() {
   136	        return m_timesOrdered;
   137	    }
   138	
   139	    s_SpecialInfo &getSpecialInfo();
   140	    s_UpgradeInfo &getUpgradeInfo();
   141	    s_UnitInfo &getUnitInfo();
   142	    s_StructureInfo &getStructureInfo();
   143	
   144	    float getCreditsPerProgressTime() {
   145	        return m_creditsPerProgressTime;
   146	    }
   147	
   148	    float getRefundAmount();
   149	
   150	    bool shouldPlaceIt() {
   151	        return m_placeIt;
   152	    }
   153	    bool shouldDeployIt() {
   154	        return m_deployIt;
   155	    }
   156	    bool isQueuable() {
   157	        return m_queuable;
   158	    }
   159	
   160	    void pauseBuilding() {
   161	        m_state = eBuildingListItemState::PAUSED;
   162	    }
   163	    void resumeBuilding() {
   164	        m_state = eBuildingListItemState::BUILDING;
   165	    }
   166	    void cancelBuilding() {
   167	        m_state = eBuildingListItemState::AVAILABLE;
   168	        m_waitingForUnitSlot = false;
   169	        resetProgress();
   170	    }
   171	    void startBuilding() {
   172	        m_state = eBuildingListItemState::BUILDING;
   173	    }
   174	
   175	    // setters
   176	    void setIconId(int value) {
   177	        m_icon = value;
   178	    }
   179	    void setBuildCost(int value) {
   180	        m_cost = value;
   181	    }
   182	    void setStatusPendingUpgrade() {
   183	        m_state = eBuildingListItemState::PENDING_UPGRADE;
   184	    }
   185	    void setStatusAvailable() {
   186	        m_state = eBuildingListItemState::AVAILABLE;
   187	    }
   188	    void setStatusPendingBuilding() {
   189	        m_state = eBuildingListItemState::PENDING_BUILDING;
   190	    }
   191	    void increaseTimesToBuild() {
   192	        m_timesToBuild++;
   193	    }
   194	    void increaseTimesToBuildNTimes(int amount) {
   195	        if (m_queuable) {
   196	            m_timesToBuild += amount;
   197	        }
   198	        else {
   199	            m_timesToBuild = 1; // not queueable always means 1
   200	        }
   201	    }
   202	    void decreaseTimesToBuild() {
   203	        m_timesToBuild--;
   204	    }
   205	    void increaseTimesOrdered() {
   206	        m_timesOrdered++;
   207	    }
   208	    void decreaseTimesOrdered() {
   209	        m_timesOrdered--;
   210	    }
   211	    void setSlotId(int value) {
   212	        m_slotId = value;
   213	    }
   214	    void setPlaceIt(bool value) {
   215	        m_placeIt = value;
   216	    }
   217	    void setWaitingForUnitSlot(bool value) {
   218	        m_waitingForUnitSlot = value;
   219	    }
   220	    bool isWaitingForUnitSlot() const {
   221	        return m_waitingForUnitSlot;
   222	    }
   223	    void setDeployIt(bool value) {
   224	        m_deployIt = value;
   225	    }
   226	    void setList(cBuildingList *theList) {
   227	        m_myList = theList;
   228	    }
   229	
   230	    cBuildingList *getList() {
   231	        return m_myList;    // returns the list it belongs to
   232	    }
   233	
   234	    /**
   235	     * List type (integer)
   236	     * @return
   237	     */
   238	    eListType getListType();
   239	
   240	    void increaseProgress(int byAmount);
   241	
   242	    void resetProgress() {
   243	        m_progress = 0;
   244	        m_buildFrameToDraw = 0;
   245	        m_TIMER_progressFrame = 0.0f;
   246	    }
   247	
   248	    int getTotalBuildTime() const;
   249	
   250	    bool isDoneBuilding();
   251	
   252	    bool isTypeUpgrade();
   253	    bool isTypeSpecial();
   254	    bool isTypeUnit();
   255	    bool isTypeStructure();
   256	
   257	    void resetTimesOrdered();
   258	
   259	    void increaseBuildProgressFrame() {
   260	        m_buildFrameToDraw++;
   261	    }
   262	    int getBuildProgressFrame() {
   263	        return m_buildFrameToDraw;
   264	    }
   265	
   266	    int calculateBuildProgressFrameBasedOnBuildProgress();
   267	
   268	    void decreaseProgressFrameTimer();
   269	
   270	    float getProgressFrameTimer();
   271	
   272	    void resetProgressFrameTimer();
   273	
   274	    void setTimerCap(int i);
   275	
   276	    int getTotalBuildTimeInTicks() const;
   277	
   278	    static int getTotalBuildTimeInTicks(eBuildType type, int buildId, cInfoContext* info);
   279	    static int getListId(eBuildType type, int buildId, cInfoContext* info);
   280	    static bool isAutoBuild(eBuildType type, int buildId, cInfoContext* info);
   281	
   282	    bool isAutoBuild();
   283	
   284	    bool isFlashing();
   285	
   286	    void decreaseFlashingTimer();
   287	
   288	private:
   289	    cBuildingListItem(int theID, s_UpgradeInfo entry, int subList);
   290	
   291	    void setProgress(int value) {
   292	        m_progress = value;
   293	    }
   294	
   295	    int m_icon;				// the icon ID to draw (from datafile)
   296	    int m_buildId;			// the ID to build .. (ie TRIKE, or CONSTYARD)
   297	    eBuildType m_type;		// .. of this type of thing (ie, UNIT or STRUCTURE)
   298	    int m_cost;				// price
   299	    eBuildingListItemState m_state;
   300	    int m_progress;			// progress building this item
   301	    int m_buildFrameToDraw;   // for the progress drawing
   302	    int m_timesToBuild;		// the amount of times to build this item (queueing) (meaning, when building = true, this should be 1...)
   303	    int m_timesOrdered;		// the amount of times this item has been ordered (starport related)
   304	    int m_slotId;			 	// return index of items[] array (set after adding item to list, default is < 0)
   305	
   306	    float m_creditsPerProgressTime; // credits to pay for each progress point. (calculated at creation)
   307	    bool m_placeIt;			// when true, this item is ready for placement
   308	    bool m_waitingForUnitSlot;	// when true, this unit is done building but waits for a free unit slot
   309	    bool m_deployIt;			// when true, this item is ready for deployment (FYI, super weapons)
   310	    bool m_queuable;			// when true, this item can be ordered multiple times to build
   311	
   312	    int m_subList;            // subList id's allow us to distinguish built items within the same buildingList.
   313	
   314	    float m_TIMER_progressFrame; // timer used for progress drawing animation
   315	    int m_TIMER_flashing;        // if > 0 then this item is 'flashing'
   316	    int m_timerCap;           // passed in by item builder (determined by power outage, etc)
   317	
   318	    cBuildingList *m_myList;
   319	    cInfoContext* m_info = nullptr;
   320	    cGameSettings* m_settings = nullptr;
   321	
   322	    cBuildingListItem(int theID, s_StructureInfo entry, cBuildingList *list, int subList);
   323	    cBuildingListItem(int theID, s_UnitInfo entry, cBuildingList *list, int subList);
   324	    cBuildingListItem(int theID, s_UpgradeInfo entry, cBuildingList *list, int subList);
   325	    cBuildingListItem(int theID, s_SpecialInfo entry, cBuildingList *list, int subList);
   326	
   327	    bool isType(eBuildType value);
   328	
   329	    int getInTicks(int getTimeInTicks) const;
   330	};
```
### Путь по имени файла: cBuildingListDrawer.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cBuildingListDrawer.h$'
src/drawers/cBuildingListDrawer.h
```
### src/drawers/cBuildingListDrawer.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cBuildingListDrawer.h | nl -ba
     1	/**
     2	 * @file cBuildingListDrawer.h
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
    18	class cTextDrawer;
    19	class cGameObjectContext;
    20	#include "observers/cInputObserver.h"
    21	#include "sidebar/cBuildingList.h"
    22	#include "sidebar/HudLayout.hpp"
    23	
    24	#include <array>
    25	#include <string>
    26	
    27	class cPlayer;
    28	class GameContext;
    29	class Graphics;
    30	class SDLDrawer;
    31	class cInfoContext;
    32	class cGameSettings;
    33	class cMouse;
    34	struct sGameServices;
    35	
    36	class cBuildingListDrawer : cInputObserver {
    37	
    38	public:
    39	    explicit cBuildingListDrawer(const GameContext *ctx, cPlayer *player);
    40	
    41	    void serviceInit(sGameServices* services);
    42	
    43	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    44	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    45	
    46	    void drawList(cBuildingList *list, int listIDToDraw);
    47	    void drawButtonHoverRectangle(cBuildingList *list);
    48	    void drawButton(cBuildingList *list, bool pressed);
    49	
    50	    cBuildingListItem *isOverItemCoordinates(cBuildingList *list, int x, int y);
    51	
    52	    int getDrawX();
    53	    int getDrawY();
    54	
    55	    void setPlayer(cPlayer *player);
    56	
    57	protected:
    58	
    59	private:
    60	    // the list to draw
    61	    cTextDrawer* m_gameTextDrawer = nullptr;
    62	    cTextDrawer* m_smallTextDrawer = nullptr;
    63	    Graphics* m_gfxinter = nullptr;
    64	    SDLDrawer* m_sdlDrawer = nullptr;
    65	
    66	    cPlayer *m_player;
    67	    cInfoContext* m_infos = nullptr;
    68	    cGameSettings* m_settings = nullptr;
    69	    cMouse* m_mouse = nullptr;
    70	    cGameObjectContext *m_objects = nullptr;
    71	
    72	    bool m_renderListIds;
    73	    std::array<int, cSideBar::LIST_MAX> m_scrollRows{};
    74	    std::string m_readyLabel;
    75	
    76	    void drawStructureSize(int structureId, int x, int y);
    77	    void drawMaxBuilt(int x, int y, int width, int height);
    78	    void drawList(cBuildingList *list, bool shouldDrawStructureSize);
    79	    void drawListWithStructures(cBuildingList *list);		// used for const yard
    80	    void drawListWithUnitsOrAbilities(cBuildingList *list); // used for units or palace / starport
    81	
    82	    bool isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY);
    83	    [[nodiscard]] int getCardWidth() const;
    84	    [[nodiscard]] int getCardHeight() const;
    85	    void drawHdCard(cBuildingListItem *item, int x, int y);
    86	    void drawHdScrollbar(cBuildingList *list, const HudLayout &layout);
    87	    [[nodiscard]] HudLayout getLayout(cBuildingList *list = nullptr) const;
    88	    [[nodiscard]] int getScrollRow(cBuildingList *list) const;
    89	    void setScrollRow(cBuildingList *list, int row);
    90	    void scrollSelectedList(int rowDelta);
    91	
    92	    void onKeyHold(const cKeyboardEvent &event);
    93	
    94	    void onKeyPressed(const cKeyboardEvent &event);
    95	};
```
### Путь по имени файла: cSideBarDrawer.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cSideBarDrawer.h$'
src/drawers/cSideBarDrawer.h
```
### src/drawers/cSideBarDrawer.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cSideBarDrawer.h | nl -ba
     1	/**
     2	 * @file cSideBarDrawer.h
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
    18	#include "cBuildingListDrawer.h"
    19	#include "cTextDrawer.h"
    20	class cKeyboardEvent;
    21	#include "observers/cInputObserver.h"
    22	struct s_MouseEvent;
    23	
    24	#include <array>
    25	#include <string>
    26	
    27	class Texture;
    28	class cPlayer;
    29	class GameContext;
    30	class Graphics;
    31	class SDLDrawer;
    32	class cInfoContext;
    33	class cMouse;
    34	struct sGameServices;
    35	
    36	class cSideBarDrawer : cInputObserver {
    37	public:
    38	    explicit cSideBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services);
    39	    ~cSideBarDrawer() override;
    40	
    41	    void serviceInit(sGameServices* services);
    42	
    43	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    44	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    45	
    46	    void draw();
    47	
    48	    cBuildingListDrawer *getBuildingListDrawer() {
    49	        return &m_buildingListDrawer;
    50	    }
    51	
    52	    void setPlayer(cPlayer *pPlayer);
    53	
    54	private:
    55	    cPlayer *m_player;
    56	    Graphics *m_gfxinter;
    57	    SDLDrawer* m_sdlDrawer;
    58	    GameContext* m_ctx = nullptr;
    59	    cInfoContext* m_infos = nullptr;
    60	    cMouse* m_mouse = nullptr;
    61	    sGameServices* m_services = nullptr;
    62	    cBuildingListDrawer m_buildingListDrawer;
    63	    cSideBar *m_sidebar;
    64	    Color m_sidebarColor;
    65	    cTextDrawer* m_smallTextDrawer = nullptr;
    66	    std::array<Texture *, 3> m_houseCrests{};
    67	
    68	    void drawHdSidebar();
    69	    void drawHdBuildingLists();
    70	    void drawHdRadarPanel();
    71	    void drawHdCapacities();
    72	    void drawHdMeter(
    73	        const cRectangle &rect,
    74	        const std::string &label,
    75	        int value,
    76	        int maximum,
    77	        Color fill,
    78	        bool warning) const;
    79	    [[nodiscard]] Texture *getHouseCrest() const;
    80	    [[nodiscard]] std::string getHouseDisplayName() const;
    81	};
```
### Путь по имени файла: cMiniMapDrawer.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cMiniMapDrawer.h$'
src/drawers/cMiniMapDrawer.h
```
### src/drawers/cMiniMapDrawer.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cMiniMapDrawer.h | nl -ba
     1	/**
     2	 * @file cMiniMapDrawer.h
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
    16	/*
    17	 * cMiniMapDrawer.h
    18	 *
    19	 *  Created on: 20-okt-2010
    20	 *      Author: Stefan
    21	 */
    22	
    23	#pragma once
    24	
    25	// #include "gameobjects/map/cMap.h"
    26	// #include "gameobjects/map/cMapCamera.h"
    27	#include "utils/cRectangle.h"
    28	#include "utils/Color.hpp"
    29	#include "controls/sMouseEvent.h"
    30	
    31	
    32	class cMap;
    33	class MapGeometry;
    34	class cMapCamera;
    35	class cPlayer;
    36	class Texture;
    37	class GameContext;
    38	class cGameSettings;
    39	class Graphics;
    40	class SDLDrawer;
    41	class cGameObjectContext;
    42	class cInfoContext;
    43	class cMouse;
    44	class AudioContext;
    45	struct sGameServices;
    46	
    47	// the BuildingListItemState
    48	enum eMinimapStatus {
    49	    NOTAVAILABLE, // show logo / no radar available
    50	    POWERUP,      // powering up (radar available & enough power)
    51	    RENDERMAP,    // map is rendering (radar available & enough power)
    52	    POWERDOWN,    // powering down (radar available & not enough power)
    53	    LOWPOWER,     // map is not rendered (radar available & not enough power)
    54	};
    55	
    56	class cMiniMapDrawer {
    57	public:
    58	    explicit cMiniMapDrawer(GameContext *ctx, cGameSettings *settings, cMap *map, cPlayer *player, cMapCamera *mapCamera);
    59	    cMiniMapDrawer() = delete;
    60	    ~cMiniMapDrawer();
    61	
    62	    void draw();
    63	
    64	    // in-between solution until we have a proper combat state object
    65	    void init();
    66	
    67	    void think();
    68	
    69	    bool isMouseOver();
    70	
    71	    void setPlayer(cPlayer *thePlayer);
    72	
    73	    void onNotifyMouseEvent(const s_MouseEvent &event);
    74	
    75	    void serviceInit(sGameServices* services);
    76	
    77	protected:
    78	
    79	    void drawTerrain();
    80	    void drawViewPortRectangle();
    81	    void drawUnitsAndStructures(bool playerOnly) const;
    82	
    83	    Color getRGBColorForTerrainType(int terrainType);
    84	
    85	    int getMapHeightInPixels() const;
    86	    int getMapWidthInPixels() const;
    87	
    88	private:
    89	    void onMouseAt(const s_MouseEvent &event);
    90	    void onMousePressedLeft(const s_MouseEvent &event);
    91	    void onMousePressedRight(const s_MouseEvent &event);
    92	    void onMouseClickedLeft(const s_MouseEvent &event);
    93	    void updateMouseCursor();
    94	    void cleanDrawTerrain() const;
    95	    int getMouseCell(int mouseX, int mouseY);
    96	
    97	    bool m_isMouseOver;
    98	
    99	    //@mira : where is map ? Where is this initialisation ?
   100	    cMap *m_map = nullptr;	// the minimap drawer reads data from here
   101	    MapGeometry *m_mapGeometry = nullptr;
   102	    cPlayer *m_player = nullptr;	// the player used as 'context' (ie, for drawing the rectangle / viewport on the minimap)
   103	    cMapCamera *m_mapCamera = nullptr;
   104	    GameContext* m_ctx = nullptr;
   105	    cGameObjectContext* m_objects = nullptr;
   106	    cInfoContext* m_infos = nullptr;
   107	    cMouse* m_mouse = nullptr;
   108	    AudioContext* m_audioContext = nullptr;
   109	    cRectangle m_RectMinimap; // the minimap (map) itself
   110	    cRectangle m_RectFullMinimap; // the total space it could take
   111	    Texture *m_mipMapTex;
   112	    Graphics *m_gfxinter;
   113	    SDLDrawer *m_sdlDrawer;
   114	
   115	    eMinimapStatus m_status;
   116	
   117	    int m_iStaticFrame;
   118	
   119	    // the top left coordinates for the minimap
   120	    int m_drawX, m_drawY;
   121	    int m_centerX, m_centerY; // the center of the minimap
   122	
   123	    // bool isBigMap;
   124	    float m_factorZoom = 1.f; // factor to zoom the minimap, based on the map size and the minimap size
   125	};
```
### Путь по имени файла: cOrderDrawer.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cOrderDrawer.h$'
src/drawers/cOrderDrawer.h
```
### src/drawers/cOrderDrawer.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cOrderDrawer.h | nl -ba
     1	/**
     2	 * @file cOrderDrawer.h
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
    18	#include "controls/sMouseEvent.h"
    19	#include "utils/cRectangle.h"
    20	#include <memory>
    21	
    22	class cPlayer;
    23	struct SDL_Surface;
    24	class Texture;
    25	class GameContext;
    26	class SDLDrawer;
    27	struct sGameServices;
    28	
    29	class cOrderDrawer {
    30	public:
    31	    explicit cOrderDrawer(GameContext *ctx, cPlayer *player, sGameServices *services);
    32	
    33	    ~cOrderDrawer();
    34	
    35	    void drawOrderButton(cPlayer *thePlayer);
    36	
    37	    void onNotify(const s_MouseEvent &event);
    38	
    39	    void serviceInit(sGameServices*) {}
    40	
    41	    void setPlayer(cPlayer *pPlayer);
    42	
    43	private:
    44	    void drawRectangleOrderButton();
    45	
    46	    void onMouseAt(const s_MouseEvent &event);
    47	    void onMouseClickedLeft(const s_MouseEvent &event);
    48	
    49	    bool m_isMouseOverOrderButton;
    50	    GameContext *m_ctx;
    51	    SDLDrawer *m_sdlDrawer;
    52	    cPlayer *m_player;
    53	    cRectangle m_buttonRect;
    54	    std::unique_ptr<Texture> m_buttonBitmap;
    55	};
```
### Путь по имени файла: cMouse.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cMouse.h$'
src/controls/cMouse.h
```
### src/controls/cMouse.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/controls/cMouse.h | nl -ba
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
### Путь по имени файла: cStructureFactory.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cStructureFactory.h$'
src/gameobjects/structures/cStructureFactory.h
```
### src/gameobjects/structures/cStructureFactory.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cStructureFactory.h | nl -ba
     1	/**
     2	 * @file cStructureFactory.h
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
    18	#include <memory>
    19	
    20	class cAbstractStructure;
    21	
    22	class cGameObjectContext;
    23	class cInfoContext;
    24	class cMapCamera;
    25	class cGameSettings;
    26	class cStructureUtils;
    27	class cEventEmitter;
    28	class SDLDrawer;
    29	struct sGameServices;
    30	
    31	class cStructureFactory {
    32	public:
    33	    cStructureFactory();
    34	
    35	    ~cStructureFactory();
    36	
    37	    void serviceInit(sGameServices *services);
    38	
    39	    void deleteStructureInstance(cAbstractStructure *pStructure);
    40	
    41	    cAbstractStructure *createStructure(int iCell, int iStructureType, int iPlayer, int iPercent = 100);
    42	
    43	    // cAbstractStructure *createStructure(int iCell, int iStructureType, int iPlayer);
    44	
    45	    int getFreeSlot();
    46	
    47	    bool isStructureLimitReached();
    48	    static bool isModifyingTerrain(int buildId);
    49	
    50	    void deleteAllExistingStructures();
    51	
    52	    void clearFogForStructureType(int iCell, cAbstractStructure *str);
    53	
    54	    void clearFogForStructureType(int iCell, int iStructureType, int iSight, int iPlayer);
    55	
    56	    void createSlabForStructureType(int iCell, int iStructureType);
    57	
    58	    void updatePlayerCatalogAndPlaceNonStructureTypeIfApplicable(int iCell, int iStructureType, int iPlayer);
    59	
    60	    int getSlabStatus(int iCell, int iStructureType);
    61	
    62	    void slabStructure(int iCll, int iStructureType, int iPlayer);
    63	
    64	private:
    65	    cGameObjectContext *m_objects = nullptr;
    66	    cInfoContext *m_info = nullptr;
    67	    cMapCamera *m_mapCamera = nullptr;
    68	    cGameSettings *m_settings = nullptr;
    69	    cStructureUtils *m_structureUtils = nullptr;
    70	    cEventEmitter *m_eventEmitter = nullptr;
    71	    sGameServices *m_services = nullptr;
    72	    SDLDrawer *m_renderer = nullptr;
    73	
    74	    std::unique_ptr<cAbstractStructure> createStructureInstance(int type);
    75	};
```
### Путь по имени файла: cStructureUtils.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cStructureUtils.h$'
src/utils/cStructureUtils.h
```
### src/utils/cStructureUtils.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/utils/cStructureUtils.h | nl -ba
     1	/**
     2	 * @file cStructureUtils.h
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
    18	class cAbstractStructure;
    19	#include "sidebar/cBuildingListItem.h"
    20	
    21	class cPlayer;
    22	struct sGameServices;
    23	class cGameObjectContext;
    24	class cInfoContext;
    25	class cMapCamera;
    26	class cGameSettings;
    27	
    28	class cStructureUtils {
    29	public:
    30	    cStructureUtils();
    31	
    32	    ~cStructureUtils();
    33	
    34	    void serviceInit(sGameServices* services);
    35	
    36	    int findStructureToDeployUnit(cPlayer *pPlayer, int structureType);
    37	
    38	    int findStarportToDeployUnit(cPlayer *pPlayer);
    39	
    40	    int findHiTechToDeployAirUnit(cPlayer *pPlayer);
    41	
    42	    int findStructureBy(int iPlayer, int iType, bool bFreeAround);
    43	
    44	    int findStructureTypeByTypeOfList(cBuildingListItem *item);
    45	
    46	    int getHeightOfStructureTypeInCells(int structureType);
    47	
    48	    int getWidthOfStructureTypeInCells(int structureType);
    49	
    50	    void putStructureOnDimension(int dimensionId, cAbstractStructure *theStructure);
    51	
    52	    bool isStructureVisibleOnScreen(cAbstractStructure *structure);
    53	
    54	    bool isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY);
    55	
    56	    int getTotalPowerOutForPlayer(cPlayer *pPlayer);
    57	
    58	    int getTotalPowerUsageForPlayer(cPlayer *pPlayer);
    59	
    60	    int getTotalSpiceCapacityForPlayer(cPlayer *pPlayer);
    61	
    62	    int getStructureTypeByUnitBuildId(int unitBuildId) const;
    63	
    64	private:
    65	    cGameObjectContext* m_objects = nullptr;
    66	    cInfoContext* m_infos = nullptr;
    67	    cMapCamera* m_mapCamera = nullptr;
    68	    cGameSettings* m_settings = nullptr;
    69	};
```
### Путь по имени файла: cTimeManager.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cTimeManager.h$'
src/game/cTimeManager.h
```
### src/game/cTimeManager.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeManager.h | nl -ba
     1	/**
     2	 * @file cTimeManager.h
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
    17	#include <stdint.h>
    18	#include <string>
    19	#include <memory>
    20	#include <SDL3/SDL.h>
    21	
    22	class cGame;
    23	class cTimeCounter;
    24	
    25	/**
    26	  Time management is done in this class
    27	*/
    28	class cTimeManager {
    29	public:
    30	    explicit cTimeManager(cGame *game);
    31	    void processTime();
    32	
    33	    // returns the current FPS
    34	    int getFps() const;
    35	    // return time to wait for CPU
    36	    int getWaitingTime() const { return m_waitingTime; }
    37	    // wait for CPU to catch up
    38	    void waitForCPU();
    39	    // get after 1s the FPS
    40	    void capFps();
    41	    // adapt waiting time based on FPS
    42	    void adaptWaitingTime();
    43	    // change global speed
    44	    void setGlobalSpeed(int speed);
    45	    void setGlobalSpeedVariation(int variation);
    46	    // get global speed
    47	    uint16_t getGlobalSpeed() const { return m_timerGameTime.tickDuration; }
    48	    // get current local Time
    49	    std::string getCurrentTime() const;
    50	    // returns the stored timer value on time format
    51	    std::string getCurrentTimer() const;
    52	    // returns the stored timer value in seconds (pause-aware, see pauseTimer()/restartTimer())
    53	    uint64_t getElapsedSeconds() const;
    54	
    55	    // start timer control
    56	    void startTimer();
    57	    // take a pause
    58	    void pauseTimer();
    59	    // restart Timer
    60	    void restartTimer();
    61	
    62	    // freeze time when focus is lost, and catch up when focus is regained
    63	    void onWindowFocusLost();
    64	    // catch up time when focus is regained
    65	    void onWindowFocusGained();
    66	
    67	private:
    68	    // gametime timer is called every 5 ms, try to keep up with that.
    69	    void handleTimerFast();
    70	    // gametime timer is called every 100 ms, try to keep up with that.
    71	    void handleTimerNormal();
    72	    // gametime timer is called every 1000 ms, try to keep up with that.
    73	    void handleTimerSlow();
    74	    // system capping to avoid extremely high timers
    75	    void capTimers();
    76	    // start every 60000 ms
    77	    void handleTimerCache();
    78	    // reset or set the tick duration based on the global speed
    79	    void initTimers(int baseSpeed);
    80	
    81	    cGame *m_game;
    82	
    83	    struct Timer {
    84	        int count = 0;                  // number of cycles to process
    85	        uint64_t lastTick = 0;          // last tick processed
    86	        uint64_t tickDuration = 0;      // duration of a tick (in ms)
    87	    };
    88	
    89	    Timer m_timerUnits;
    90	    Timer m_timerGameTime;
    91	    Timer m_timerSecond;
    92	    Timer m_timerMinute;
    93	
    94	    int m_gameTime = 0;         // Definition of game time (= in seconds)
    95	    int m_fps = 0;			    // Frames per second
    96	    int m_frameCount = 0;	    // Frame count for FPS calculation
    97	    int m_waitingTime = 10;	    // Waiting time in ms, used to adapt FPS
    98	    Uint64 m_focusLostTime = 0;  // Time when focus was lost, used to calculate time to catch up when focus is regained
    99	
   100	    std::unique_ptr<cTimeCounter> m_timeCounter;
   101	};
```
### Путь по имени файла: cMessageDrawer.h

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/cMessageDrawer.h$'
src/drawers/cMessageDrawer.h
```
### src/drawers/cMessageDrawer.h@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cMessageDrawer.h | nl -ba
     1	/**
     2	 * @file cMessageDrawer.h
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
    19	#include "cTextDrawer.h"
    20	#include <string>
    21	
    22	struct SDL_Surface;
    23	class GameContext;
    24	class Graphics;
    25	class SDLDrawer;
    26	struct sGameServices;
    27	
    28	namespace messages {
    29	enum eMessageDrawerState {
    30	    COMBAT,
    31	    NEXT_CONQUEST
    32	};
    33	
    34	enum eMessageDrawerFadingState {
    35	    FADE_IN,
    36	    FADE_OUT
    37	};
    38	}
    39	
    40	class cMessageDrawer {
    41	public:
    42	    explicit cMessageDrawer(GameContext* ctx, sGameServices* services);
    43	    ~cMessageDrawer();
    44	
    45	    void serviceInit(sGameServices*) {}
    46	
    47	    void draw();
    48	
    49	    void thinkFast(); // timer based thinking to fade in/out message
    50	
    51	    void init();
    52	    void destroy();
    53	
    54	    void setKeepMessage(bool value);
    55	
    56	    void initRegionPosition(int offsetX, int offsetY);
    57	
    58	    void initCombatPosition();
    59	
    60	    void setMessage(const std::string &msg, bool keepMessage = false);
    61	    std::string getMessage() {
    62	        return m_message;
    63	    }
    64	    bool hasMessage() {
    65	        return !m_message.empty();
    66	    }
    67	
    68	protected:
    69	
    70	private:
    71	    std::string m_message;
    72	    bool m_keepMessage;
    73	    int m_TIMER_message;
    74	    int m_alpha;
    75	
    76	    cPoint m_position; // draw positions
    77	    SDL_Surface *m_bmpBar;
    78	    int m_timeMessageIsVisible;
    79	
    80	    messages::eMessageDrawerState m_state;
    81	    messages::eMessageDrawerFadingState m_fadeState;
    82	    cTextDrawer* m_textDrawer=nullptr;
    83	    SDLDrawer* m_sdlDrawer=nullptr;
    84	    GameContext* m_ctx;
    85	    Graphics* m_gfxinter;
    86	    sGameServices* m_services;
    87	
    88	    void createMessageBarBmp(int desiredWidth);
    89	};
```
### Путь по имени файла: HudLayout.h

нет файла

### Путь по имени файла: HudLayout.hpp

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | grep -E '/HudLayout.hpp$'
src/sidebar/HudLayout.hpp
```
### src/sidebar/HudLayout.hpp@acddd29

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/HudLayout.hpp | nl -ba
     1	#pragma once
     2	
     3	#include "utils/cRectangle.h"
     4	
     5	#include <algorithm>
     6	
     7	/**
     8	 * Immutable geometry for the combat HUD.
     9	 *
    10	 * HD drawing and hit testing must use this object instead of repeating sidebar
    11	 * arithmetic in several drawers.
    12	 */
    13	struct HudLayout {
    14	    static constexpr int TopBarHeight = 42;
    15	
    16	    int screenWidth = 0;
    17	    int screenHeight = 0;
    18	    int sidebarWidth = 224;
    19	    int columns = 3;
    20	    int cardGap = 3;
    21	    int cardWidth = 63;
    22	    int cardHeight = 47;
    23	
    24	    cRectangle topBar;
    25	    cRectangle battlefield;
    26	    cRectangle sidebar;
    27	    cRectangle credits;
    28	    cRectangle radarPanel;
    29	    cRectangle houseHeader;
    30	    cRectangle radarViewport;
    31	    cRectangle powerMeter;
    32	    cRectangle spiceMeter;
    33	    cRectangle tabs;
    34	    cRectangle catalog;
    35	    cRectangle cards;
    36	    cRectangle scrollbar;
    37	
    38	    static HudLayout create(
    39	        int logicalWidth,
    40	        int logicalHeight,
    41	        bool reserveStarportOrderArea = false)
    42	    {
    43	        HudLayout layout;
    44	        layout.screenWidth = logicalWidth;
    45	        layout.screenHeight = logicalHeight;
    46	        layout.sidebarWidth = logicalWidth < 960 ? 280 : 360;
    47	        layout.columns = logicalWidth < 960 ? 2 : 3;
    48	        layout.cardGap = 6;
    49	
    50	        const int sidebarX = logicalWidth - layout.sidebarWidth;
    51	        const int panelInset = 8;
    52	        const int panelWidth = layout.sidebarWidth - panelInset * 2;
    53	        const int catalogY = 302;
    54	        const int catalogBottom =
    55	            logicalHeight - (reserveStarportOrderArea ? 54 : 6);
    56	
    57	        layout.topBar = cRectangle(0, 0, logicalWidth, TopBarHeight);
    58	        layout.battlefield = cRectangle(
    59	            0,
    60	            TopBarHeight,
    61	            logicalWidth - layout.sidebarWidth,
    62	            logicalHeight - TopBarHeight
    63	        );
    64	        layout.sidebar = cRectangle(
    65	            sidebarX,
    66	            0,
    67	            layout.sidebarWidth,
    68	            logicalHeight
    69	        );
    70	        layout.credits = cRectangle(
    71	            sidebarX + panelInset,
    72	            4,
    73	            panelWidth,
    74	            34
    75	        );
    76	        layout.radarPanel = cRectangle(
    77	            sidebarX + panelInset,
    78	            TopBarHeight,
    79	            panelWidth,
    80	            208
    81	        );
    82	        layout.houseHeader = cRectangle(
    83	            layout.radarPanel.getX() + 5,
    84	            layout.radarPanel.getY() + 4,
    85	            layout.radarPanel.getWidth() - 10,
    86	            28
    87	        );
    88	        layout.radarViewport = cRectangle(
    89	            layout.radarPanel.getX() + 5,
    90	            layout.radarPanel.getY() + 34,
    91	            layout.radarPanel.getWidth() - 10,
    92	            138
    93	        );
    94	
    95	        const int meterGap = 5;
    96	        const int meterY = layout.radarPanel.getY() + 176;
    97	        const int meterWidth =
    98	            (layout.radarPanel.getWidth() - 10 - meterGap) / 2;
    99	        layout.powerMeter = cRectangle(
   100	            layout.radarPanel.getX() + 5,
   101	            meterY,
   102	            meterWidth,
   103	            27
   104	        );
   105	        layout.spiceMeter = cRectangle(
   106	            layout.powerMeter.getEndX() + meterGap,
   107	            meterY,
   108	            meterWidth,
   109	            27
   110	        );
   111	        layout.tabs = cRectangle(
   112	            sidebarX + panelInset,
   113	            TopBarHeight + 220,
   114	            panelWidth,
   115	            34
   116	        );
   117	        layout.catalog = cRectangle(
   118	            sidebarX + panelInset,
   119	            catalogY,
   120	            panelWidth,
   121	            std::max(0, catalogBottom - catalogY)
   122	        );
   123	        layout.scrollbar = cRectangle(
   124	            layout.catalog.getEndX() - 10,
   125	            layout.catalog.getY(),
   126	            10,
   127	            layout.catalog.getHeight()
   128	        );
   129	        layout.cards = cRectangle(
   130	            layout.catalog.getX(),
   131	            layout.catalog.getY(),
   132	            layout.catalog.getWidth() - 15,
   133	            layout.catalog.getHeight()
   134	        );
   135	
   136	        const int gapsWidth = (layout.columns - 1) * layout.cardGap;
   137	        layout.cardWidth =
   138	            (layout.cards.getWidth() - gapsWidth) / layout.columns;
   139	        const int imageHeight =
   140	            std::max(1, (layout.cardWidth - 4) * 3 / 4);
   141	        layout.cardHeight = imageHeight + 32;
   142	        return layout;
   143	    }
   144	
   145	    [[nodiscard]] int visibleRows() const
   146	    {
   147	        const int stride = cardHeight + cardGap;
   148	        return stride > 0
   149	            ? std::max(1, (cards.getHeight() + cardGap) / stride)
   150	            : 1;
   151	    }
   152	
   153	    [[nodiscard]] int totalRows(int itemCount) const
   154	    {
   155	        return itemCount <= 0 ? 0 : (itemCount + columns - 1) / columns;
   156	    }
   157	
   158	    [[nodiscard]] int maxScrollRow(int itemCount) const
   159	    {
   160	        return std::max(0, totalRows(itemCount) - visibleRows());
   161	    }
   162	
   163	    [[nodiscard]] cRectangle cardRect(
   164	        int itemIndex,
   165	        int scrollRow) const
   166	    {
   167	        const int row = itemIndex / columns - scrollRow;
   168	        const int column = itemIndex % columns;
   169	        return cRectangle(
   170	            cards.getX() + column * (cardWidth + cardGap),
   171	            cards.getY() + row * (cardHeight + cardGap),
   172	            cardWidth,
   173	            cardHeight
   174	        );
   175	    }
   176	
   177	    [[nodiscard]] cRectangle tabRect(int tabIndex, int tabCount = 6) const
   178	    {
   179	        const int width = tabs.getWidth() / tabCount;
   180	        const int x = tabs.getX() + tabIndex * width;
   181	        const int actualWidth =
   182	            tabIndex == tabCount - 1 ? tabs.getEndX() - x : width;
   183	        return cRectangle(x, tabs.getY(), actualWidth, tabs.getHeight());
   184	    }
   185	
   186	    [[nodiscard]] cRectangle scrollbarThumb(
   187	        int itemCount,
   188	        int scrollRow) const
   189	    {
   190	        if (maxScrollRow(itemCount) <= 0) {
   191	            return scrollbar;
   192	        }
   193	
   194	        const int total = std::max(1, totalRows(itemCount));
   195	        const int thumbHeight = std::max(
   196	            22,
   197	            scrollbar.getHeight() * visibleRows() / total
   198	        );
   199	        const int travel = scrollbar.getHeight() - thumbHeight;
   200	        const int thumbY = scrollbar.getY() +
   201	            travel * std::clamp(scrollRow, 0, maxScrollRow(itemCount)) /
   202	            maxScrollRow(itemCount);
   203	        return cRectangle(
   204	            scrollbar.getX(),
   205	            thumbY,
   206	            scrollbar.getWidth(),
   207	            thumbHeight
   208	        );
   209	    }
   210	};
```
