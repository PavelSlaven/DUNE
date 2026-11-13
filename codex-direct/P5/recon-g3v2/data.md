### src/game/cMissionStatsCollector.h@c583461

```text
git show c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.h | nl -ba
     1	/**
     2	 * @file cMissionStatsCollector.h
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
    18	#include "game/MissionStats.h"
    19	#include "include/enums/BuildEnums.h"
    20	
    21	struct s_GameEvent;
    22	class cPlayer;
    23	class cGameObjectContext;
    24	
    25	class cMissionStatsCollector {
    26	public:
    27	    explicit cMissionStatsCollector(cGameObjectContext *objects);
    28	    void onNotifyGameEvent(const s_GameEvent &event);
    29	    [[nodiscard]] MissionStats snapshot(uint64_t elapsedSeconds) const;
    30	
    31	private:
    32	    // Resolves who dealt damage/a killing blow, by id + kind. Returns nullptr when there was no
    33	    // attacker (self-destruct, sandworm, debug kill) or it no longer exists.
    34	    cPlayer *resolveOriginPlayer(int originId, eBuildType originType) const;
    35	
    36	    cGameObjectContext *m_objects;
    37	    std::array<PlayerMissionStats, MAX_PLAYERS> m_playerStats;
    38	};
```

### src/game/cMissionStatsCollector.cpp@c583461

```text
git show c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp | nl -ba
     1	/**
     2	 * @file cMissionStatsCollector.cpp
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
    16	#include "game/cMissionStatsCollector.h"
    17	
    18	#include "context/cGameObjectContext.h"
    19	#include "include/sGameEvent.h"
    20	#include "gameobjects/players/cPlayer.h"
    21	#include "gameobjects/structures/cAbstractStructure.h"
    22	#include "gameobjects/units/cUnit.h"
    23	#include "utils/Log.h"
    24	
    25	cMissionStatsCollector::cMissionStatsCollector(cGameObjectContext *objects) : m_objects(objects)
    26	{
    27	}
    28	
    29	cPlayer *cMissionStatsCollector::resolveOriginPlayer(int originId, eBuildType originType) const
    30	{
    31	    if (originId < 0) {
    32	        return nullptr;
    33	    }
    34	    if (originType == eBuildType::UNIT) {
    35	        cUnit *pUnit = m_objects->getUnit(originId);
    36	        return (pUnit != nullptr && pUnit->isValid()) ? pUnit->getPlayer() : nullptr;
    37	    }
    38	    if (originType == eBuildType::STRUCTURE) {
    39	        cAbstractStructure *pStructure = m_objects->getStructure(originId);
    40	        // isValid() guards iPlayer < 0: getPlayer() asserts (aborts) on that, so a slot that was
    41	        // cleared and not yet reassigned to a real owner must be checked first, not just
    42	        // whether the pointer itself is non-null.
    43	        return (pStructure != nullptr && pStructure->isValid()) ? pStructure->getPlayer() : nullptr;
    44	    }
    45	    return nullptr;
    46	}
    47	
    48	void cMissionStatsCollector::onNotifyGameEvent(const s_GameEvent &event)
    49	{
    50	    if (event.eventType == eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN) {
    51	        // Reset here, not at mission setup: the scenario's starting units/structures are placed
    52	        // between mission setup and this event, and must not be counted as player-built.
    53	        m_playerStats = {};
    54	        // Capture each player's house now, before any of them can be defeated: cGamePlaying
    55	        // resets a defeated player's house to GENERALHOUSE as part of elimination cleanup, so
    56	        // reading it live at scoring time would hide anyone the player actually beat.
    57	        for (int playerId = 0; playerId < MAX_PLAYERS; playerId++) {
    58	            const cPlayer *player = m_objects->getPlayer(playerId);
    59	            if (player != nullptr) {
    60	                m_playerStats[playerId].house = player->getHouse();
    61	                m_playerStats[playerId].minimapColor = player->getMinimapColor();
    62	            }
    63	        }
    64	        return;
    65	    }
    66	
    67	    if (event.eventType == eGameEventType::GAME_EVENT_DAMAGED) {
    68	        const auto *damagedEvent = std::get_if<DamagedEvent>(&event.data);
    69	        if (damagedEvent == nullptr) {
    70	            Logger::warn(COMP_GAME, "cMissionStatsCollector::onNotifyGameEvent", "GAME_EVENT_DAMAGED did not carry a DamagedEvent");
    71	            return;
    72	        }
    73	        cPlayer *attacker = resolveOriginPlayer(damagedEvent->originId, damagedEvent->originType);
    74	        if (attacker != nullptr && attacker->getId() >= 0 && attacker->getId() < MAX_PLAYERS) {
    75	            m_playerStats[attacker->getId()].damageDealt += damagedEvent->damage;
    76	        }
    77	        if (damagedEvent->player != nullptr) {
    78	            const int victimId = damagedEvent->player->getId();
    79	            if (victimId >= 0 && victimId < MAX_PLAYERS) {
    80	                m_playerStats[victimId].damageReceived += damagedEvent->damage;
    81	            }
    82	        }
    83	        return;
    84	    }
    85	
    86	    if (event.eventType == eGameEventType::GAME_EVENT_SPICE_HARVESTED) {
    87	        const auto *harvestedEvent = std::get_if<SpiceHarvestedEvent>(&event.data);
    88	        if (harvestedEvent == nullptr) {
    89	            Logger::warn(COMP_GAME, "cMissionStatsCollector::onNotifyGameEvent", "GAME_EVENT_SPICE_HARVESTED did not carry a SpiceHarvestedEvent");
    90	            return;
    91	        }
    92	        const int playerId = harvestedEvent->player.getId();
    93	        if (playerId >= 0 && playerId < MAX_PLAYERS) {
    94	            m_playerStats[playerId].spiceHarvested += harvestedEvent->amount;
    95	        }
    96	        return;
    97	    }
    98	
    99	    if (event.eventType != eGameEventType::GAME_EVENT_CREATED &&
   100	        event.eventType != eGameEventType::GAME_EVENT_DESTROYED) {
   101	        return;
   102	    }
   103	
   104	    const auto *commonEvent = std::get_if<CommonEvent>(&event.data);
   105	    if (commonEvent == nullptr) {
   106	        Logger::warn(COMP_GAME, "cMissionStatsCollector::onNotifyGameEvent", "GAME_EVENT_CREATED/GAME_EVENT_DESTROYED did not carry a CommonEvent");
   107	        return;
   108	    }
   109	
   110	    if (event.eventType == eGameEventType::GAME_EVENT_DESTROYED) {
   111	        cPlayer *killer = resolveOriginPlayer(commonEvent->originId, commonEvent->originType);
   112	        if (killer != nullptr && killer->getId() >= 0 && killer->getId() < MAX_PLAYERS) {
   113	            PlayerMissionStats &killerStats = m_playerStats[killer->getId()];
   114	            killerStats.damageDealt += commonEvent->damage;
   115	            if (commonEvent->entityType == eBuildType::UNIT) {
   116	                killerStats.unitsDestroyed++;
   117	            }
   118	            else if (commonEvent->entityType == eBuildType::STRUCTURE) {
   119	                killerStats.structuresDestroyed++;
   120	            }
   121	        }
   122	    }
   123	
   124	    if (commonEvent->player == nullptr) {
   125	        return;
   126	    }
   127	
   128	    const int playerId = commonEvent->player->getId();
   129	    if (playerId < 0 || playerId >= MAX_PLAYERS) {
   130	        return;
   131	    }
   132	
   133	    PlayerMissionStats &stats = m_playerStats[playerId];
   134	
   135	    if (event.eventType == eGameEventType::GAME_EVENT_CREATED) {
   136	        if (commonEvent->isReinforce) {
   137	            return; // reinforcements were not built by the player this mission
   138	        }
   139	        if (commonEvent->entityType == eBuildType::UNIT) {
   140	            stats.unitsBuilt++;
   141	        }
   142	        else if (commonEvent->entityType == eBuildType::STRUCTURE) {
   143	            stats.structuresBuilt++;
   144	        }
   145	    }
   146	    else { // GAME_EVENT_DESTROYED
   147	        stats.damageReceived += commonEvent->damage;
   148	        if (commonEvent->entityType == eBuildType::UNIT) {
   149	            stats.unitsLost++;
   150	        }
   151	        else if (commonEvent->entityType == eBuildType::STRUCTURE) {
   152	            stats.structuresLost++;
   153	        }
   154	    }
   155	}
   156	
   157	MissionStats cMissionStatsCollector::snapshot(uint64_t elapsedSeconds) const
   158	{
   159	    MissionStats stats;
   160	    stats.players = m_playerStats;
   161	    stats.elapsedSeconds = elapsedSeconds;
   162	    return stats;
   163	}
```

### src/gamestates/cWinLoseState.cpp@c583461

```text
git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cWinLoseState.cpp | nl -ba
     1	/**
     2	 * @file cWinLoseState.cpp
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
    16	#include "gamestates/cWinLoseState.h"
    17	
    18	#include "data/gfxinter.h"
    19	#include "drawers/SDLDrawer.hpp"
    20	#include "drawers/cTextDrawer.h"
    21	#include "utils/Graphics.hpp"
    22	#include "utils/HdUiTextureLoader.hpp"
    23	#include "utils/OutcomeScreenLayout.hpp"
    24	#include "context/GameContext.hpp"
    25	#include "game/GameStateTransition.hpp"
    26	#include "game/MissionFlow.hpp"
    27	#include "controls/cMouse.h"
    28	
    29	#include <SDL3/SDL.h>
    30	#include "include/cAssert.h"
    31	#include "game/cGameSettings.h"
    32	#include "gamestates/cGameState.h"
    33	#include "include/Texture.hpp"
    34	#include "include/sGameServices.h"
    35	#include "context/GraphicsContext.hpp"
    36	#include "include/eGameState.h"
    37	
    38	cWinLoseState::cWinLoseState(sGameServices* services, Outcome value) : 
    39	    cGameState(services),
    40	    m_settings(services->settings),
    41	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    42	    m_statement(value)
    43	{
    44	    d2tm_assert(services != nullptr);
    45	    d2tm_assert(m_settings != nullptr);
    46	
    47	    auto ctx = services->ctx;
    48	    m_missionFlow = services->missionFlow;
    49	    m_stateTransitions = services->stateTransitions;
    50	    d2tm_assert(m_missionFlow != nullptr);
    51	    d2tm_assert(m_stateTransitions != nullptr);
    52	    m_mouse = services->mouse;
    53	    d2tm_assert(m_mouse != nullptr);
    54	    auto gfxinter = ctx->getGraphicsContext()->gfxinter;
    55	    d2tm_assert(gfxinter != nullptr);
    56	
    57	    const char *outcomeFile = m_statement == Outcome::Lose
    58	        ? "outcome_defeat_en.png"
    59	        : "outcome_victory_en.png";
    60	    m_hdOutcomeTexture = loadHdUiTexture(
    61	        m_sdlDrawer->getRenderer(),
    62	        outcomeFile,
    63	        m_statement == Outcome::Lose ? "HD defeat screen" : "HD victory screen"
    64	    );
    65	
    66	    m_backgroundTexture = &services->screenTexture;
    67	    
    68	    if (m_statement == Outcome::Lose) {
    69	        m_tex = gfxinter->getTexture(BMP_LOSING);
    70	    } else {
    71	        m_tex = gfxinter->getTexture(BMP_WINNING);
    72	    }
    73	}
    74	
    75	cWinLoseState::~cWinLoseState()
    76	{
    77	    delete m_hdOutcomeTexture;
    78	}
    79	
    80	void cWinLoseState::thinkFast()
    81	{
    82	}
    83	
    84	void cWinLoseState::draw() const
    85	{
    86	    if (m_hdOutcomeTexture) {
    87	        const std::string prompt = "Click to continue";
    88	        const OutcomeScreenLayout layout = calculateOutcomeScreenLayout(
    89	            m_settings->getScreenW(),
    90	            m_settings->getScreenH(),
    91	            m_hdOutcomeTexture->pixelW,
    92	            m_hdOutcomeTexture->pixelH,
    93	            m_textDrawer->getTextLength(prompt)
    94	        );
    95	        m_sdlDrawer->renderStrechFullSprite(m_hdOutcomeTexture, layout.image);
    96	        m_textDrawer->drawTextScaledCenteredInBox(
    97	            prompt,
    98	            layout.prompt,
    99	            layout.promptTextScale,
   100	            Color{255, 224, 164, 255}
   101	        );
   102	    }
   103	    else {
   104	        if (m_backgroundTexture && *m_backgroundTexture) {
   105	            m_sdlDrawer->renderSprite(*m_backgroundTexture, 0, 0);
   106	        }
   107	
   108	        const int posW = (m_settings->getScreenW() - m_tex->w) / 2;
   109	        const int posH = (m_settings->getScreenH() - m_tex->h) / 2;
   110	        m_sdlDrawer->renderSprite(m_tex, posW, posH);
   111	    }
   112	
   113	    m_mouse->draw();
   114	}
   115	
   116	void cWinLoseState::onNotifyMouseEvent(const s_MouseEvent &event)
   117	{
   118	    switch (event.eventType) {
   119	        case MOUSE_LEFT_BUTTON_CLICKED:
   120	            onMouseLeftButtonClicked(event);
   121	            break;
   122	        default:
   123	            break;
   124	    }
   125	}
   126	
   127	eGameStateType cWinLoseState::getType()
   128	{
   129	    return GAMESTATE_WINLOSE;
   130	}
   131	
   132	void cWinLoseState::onNotifyKeyboardEvent(const cKeyboardEvent &)
   133	{
   134	}
   135	
   136	void cWinLoseState::onMouseLeftButtonClicked(const s_MouseEvent &) const
   137	{
   138	    if (m_statement == Outcome::Lose) {
   139	        m_missionFlow->goingToWinLoseBrief(GAME_LOSEBRIEF);
   140	    } else {
   141	        m_stateTransitions->setNextState(GAME_SCORING);
   142	    }
   143	    // FADE OUT
   144	    m_stateTransitions->fadeOut();
   145	}
```

### src/gameobjects/map/cPreviewMaps.h@c583461

```text
git show c5834615f8fc71789bba7108078a461018cc7d56:src/gameobjects/map/cPreviewMaps.h | nl -ba
     1	/**
     2	 * @file cPreviewMaps.h
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
    18	// #define MAX_SKIRMISHMAPS 100     // max of 100 skirmish maps
    19	
    20	#include <SDL3/SDL.h>
    21	#include <vector>
    22	#include <string>
    23	#include <array>
    24	#include <memory>
    25	
    26	#include "gameobjects/map/PreviewMap.hpp"
    27	
    28	class Texture;
    29	class SDLDrawer;
    30	
    31	// a preview map plus the SDL resources used to show it as a preview
    32	struct PreviewMapView {
    33	    s_PreviewMap map;
    34	    SDL_Surface *terrain = nullptr;      // terrain bitmap (for showing preview at top right)
    35	    Texture *previewTex = nullptr;       // texture for the map preview
    36	};
    37	
    38	class cPreviewMaps {
    39	public:
    40	    cPreviewMaps();
    41	
    42	    void setSDLDrawer(SDLDrawer *sdlDrawer);
    43	
    44	    // draws the terrain and start cells of a preview map onto a surface of the same size
    45	    void drawPreview(const s_PreviewMap &previewMap, SDL_Surface *surface) const;
    46	
    47	    ~cPreviewMaps() = default;
    48	
    49	    void loadSkirmishMaps();
    50	    void destroy();
    51	
    52	    s_PreviewMap *getMap(int i);
    53	    PreviewMapView *getView(int i);
    54	    bool isValidMap(int i) const;
    55	
    56	    std::string getMapSize(int i) const;
    57	    int getMapCount() const;
    58	
    59	    void createEmptyMap(const std::string &name, const std::string &author,
    60	            const std::string &desciption, int width, int height);
    61	
    62	    // replaces the map that loadMapFromEditor(-1) hands to the editor
    63	    void setEditorMap(s_PreviewMap &&map);
    64	
    65	    void loadSkirmish(const std::string &filename);
    66	    bool saveSkirmishMap(const s_PreviewMap &map, bool backup = false);
    67	private:
    68	    void initRandomMap();
    69	    void initPreviews();
    70	    std::unique_ptr<PreviewMapView> m_emptyMap;
    71	
    72	    std::vector<std::unique_ptr<PreviewMapView>> m_PreviewMap;
    73	    SDLDrawer * m_sdlDrawer = nullptr;
    74	};
```

### src/gamestates/cSetupSkirmishState.cpp@c583461:340-420

```text
git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cSetupSkirmishState.cpp | nl -ba | sed -n '340,420p'
   340	    int startButtonX = screen_x - startButtonWidth;
   341	    cRectangle startButtonRect = cRectangle(startButtonX, startButtonY, startButtonWidth, topBarHeight);
   342	    startButton = GuiButtonBuilder()
   343	            .withRect(startButtonRect)
   344	            .withLabel("Start")
   345	            .withTextDrawer(m_textDrawer)
   346	            .withRenderer(m_sdlDrawer)
   347	            .withTheme(GuiTheme::Remaster())
   348	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   349	            .onClick([this]() {
   350	                if (m_previewMaps->isValidMap(iSkirmishMap)) {
   351	                    prepareSkirmishGameToPlayAndTransitionToCombatState(iSkirmishMap);
   352	                }
   353	            })
   354	            .build();
   355	
   356	    int surpriseMeButtonWidth = m_textDrawer->getTextLength("Surprise me") + btnHPad;
   357	    int surpriseMeButtonX = startButtonX - btnGap - surpriseMeButtonWidth;
   358	    cRectangle surpriseMeButtonRect = cRectangle(surpriseMeButtonX, bottomY, surpriseMeButtonWidth, btnHeight);
   359	    surpriseMeButton = GuiButtonBuilder()
   360	            .withRect(surpriseMeButtonRect)
   361	            .withLabel("Surprise me")
   362	            .withTextDrawer(m_textDrawer)
   363	            .withRenderer(m_sdlDrawer)
   364	            .withTheme(GuiTheme::Remaster())
   365	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   366	            .onClick([this]() { surpriseMe(); })
   367	            .build();
   368	
   369	    // Center group: [New Map] [Modify]
   370	    int newMapButtonWidth = m_textDrawer->getTextLength("New Map") + btnHPad;
   371	    int modifyButtonWidth = m_textDrawer->getTextLength("Modify") + btnHPad;
   372	    int centerGroupWidth = newMapButtonWidth + btnGap + modifyButtonWidth;
   373	    int centerGroupX = screen_x / 2 - centerGroupWidth / 2;
   374	    cRectangle newMapButtonRect = cRectangle(centerGroupX, bottomY, newMapButtonWidth, btnHeight);
   375	    newMapButton = GuiButtonBuilder()
   376	            .withRect(newMapButtonRect)
   377	            .withLabel("New Map")
   378	            .withTextDrawer(m_textDrawer)
   379	            .withRenderer(m_sdlDrawer)
   380	            .withTheme(GuiTheme::Remaster())
   381	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   382	            .onClick([this]() {
   383	                m_stateTransitions->setNextStateWithFade(GAME_NEW_MAP_EDITOR);
   384	            })
   385	            .build();
   386	
   387	    int modifyButtonX = centerGroupX + newMapButtonWidth + btnGap;
   388	    cRectangle modifyButtonRect = cRectangle(modifyButtonX, bottomY, modifyButtonWidth, btnHeight);
   389	    modifyButton = GuiButtonBuilder()
   390	            .withRect(modifyButtonRect)
   391	            .withLabel("Modify")
   392	            .withTextDrawer(m_textDrawer)
   393	            .withRenderer(m_sdlDrawer)
   394	            .withTheme(GuiTheme::Remaster())
   395	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   396	            .onClick([this]() {
   397	                if (iSkirmishMap > -1) {
   398	                    m_scenarioFlow->loadMapFromEditor(iSkirmishMap);
   399	                    m_stateTransitions->fadeOut();
   400	                }
   401	            })
   402	            .build();
   403	}
   404	
   405	cSetupSkirmishState::~cSetupSkirmishState()
   406	{
   407	    // Smart pointers handle cleanup
   408	}
   409	
   410	bool cSetupSkirmishState::guiDrawFrame(int x, int y, int width, int height) const
   411	{
   412	    const cRectangle rect(x, y, width, height);
   413	    m_sdlDrawer->renderRectFillColor(rect, Color{25, 31, 35, 255});
   414	    m_sdlDrawer->renderRectColor(rect, Color{173, 125, 39, 255});
   415	    return mouse_within_rect(m_mouse, x, y, width, height);
   416	}
   417	
   418	bool cSetupSkirmishState::guiDrawFramePressed(int x1, int y1, int width, int height) const
   419	{
   420	    const cRectangle rect(x1, y1, width, height);
```

### git grep -n -E 'missionStatsCollector|cMissionStatsCollector' c5834615f8fc71789bba7108078a461018cc7d56 -- src

```text
git grep -n -E 'missionStatsCollector|cMissionStatsCollector' c5834615f8fc71789bba7108078a461018cc7d56 -- src
c5834615f8fc71789bba7108078a461018cc7d56:src/CMakeLists.txt:47:    game/cMissionStatsCollector.cpp
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame.h:56:class cMissionStatsCollector;
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame.h:257:    std::unique_ptr<cMissionStatsCollector> m_missionStatsCollector;
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:36:#include "game/cMissionStatsCollector.h"
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:202:    m_missionStatsCollector = std::make_unique<cMissionStatsCollector>(m_gameObjectsContext.get());
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:283:    m_services->missionStatsCollector = m_missionStatsCollector.get();
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:489:    const MissionStats stats = m_missionStatsCollector->snapshot(m_timeManager->getElapsedSeconds());
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:1420:    m_missionStatsCollector->onNotifyGameEvent(event);
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:2: * @file cMissionStatsCollector.cpp
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:16:#include "game/cMissionStatsCollector.h"
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:25:cMissionStatsCollector::cMissionStatsCollector(cGameObjectContext *objects) : m_objects(objects)
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:29:cPlayer *cMissionStatsCollector::resolveOriginPlayer(int originId, eBuildType originType) const
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:48:void cMissionStatsCollector::onNotifyGameEvent(const s_GameEvent &event)
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:70:            Logger::warn(COMP_GAME, "cMissionStatsCollector::onNotifyGameEvent", "GAME_EVENT_DAMAGED did not carry a DamagedEvent");
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:89:            Logger::warn(COMP_GAME, "cMissionStatsCollector::onNotifyGameEvent", "GAME_EVENT_SPICE_HARVESTED did not carry a SpiceHarvestedEvent");
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:106:        Logger::warn(COMP_GAME, "cMissionStatsCollector::onNotifyGameEvent", "GAME_EVENT_CREATED/GAME_EVENT_DESTROYED did not carry a CommonEvent");
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.cpp:157:MissionStats cMissionStatsCollector::snapshot(uint64_t elapsedSeconds) const
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.h:2: * @file cMissionStatsCollector.h
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.h:25:class cMissionStatsCollector {
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.h:27:    explicit cMissionStatsCollector(cGameObjectContext *objects);
c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cScoringState.cpp:11:#include "game/cMissionStatsCollector.h"
c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cScoringState.cpp:39:    m_stats = services->missionStatsCollector->snapshot(m_ctx->getTimeManager()->getElapsedSeconds());
c5834615f8fc71789bba7108078a461018cc7d56:src/include/sGameServices.h:30:class cMissionStatsCollector;
c5834615f8fc71789bba7108078a461018cc7d56:src/include/sGameServices.h:55:    cMissionStatsCollector *missionStatsCollector = nullptr;
```

### git grep -n -E 'getPreviewMaps\(\)|loadMapFromEditor\(' c5834615f8fc71789bba7108078a461018cc7d56 -- src

```text
git grep -n -E 'getPreviewMaps\(\)|loadMapFromEditor\(' c5834615f8fc71789bba7108078a461018cc7d56 -- src
c5834615f8fc71789bba7108078a461018cc7d56:src/context/cGameObjectContext.cpp:113:cPreviewMaps* cGameObjectContext::getPreviewMaps() const
c5834615f8fc71789bba7108078a461018cc7d56:src/context/cGameObjectContext.h:58:    cPreviewMaps* getPreviewMaps() const;
c5834615f8fc71789bba7108078a461018cc7d56:src/game/ScenarioFlow.hpp:36:          m_loadMapFromEditor(std::move(loadMapFromEditor)),
c5834615f8fc71789bba7108078a461018cc7d56:src/game/ScenarioFlow.hpp:48:    void loadMapFromEditor(int iSkirmishMap) const {
c5834615f8fc71789bba7108078a461018cc7d56:src/game/ScenarioFlow.hpp:49:        m_loadMapFromEditor(iSkirmishMap);
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame.h:175:    void loadMapFromEditor(int map);
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:269:            loadMapFromEditor(iSkirmishMap);
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:530://     m_gameObjectsContext->getPreviewMaps()->loadSkirmishMaps();
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:821:    auto previewMaps = m_gameObjectsContext->getPreviewMaps();
c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp:1735:void cGame::loadMapFromEditor(int map)
c5834615f8fc71789bba7108078a461018cc7d56:src/gameobjects/map/cPreviewMaps.h:62:    // replaces the map that loadMapFromEditor(-1) hands to the editor
c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cCreatorState.cpp:169:                m_services->objects->getPreviewMaps(),
c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cEditorState.cpp:69:    m_previewMaps(services->objects->getPreviewMaps())
c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cNewmapEditorState.cpp:57:    m_previewMap(services->objects->getPreviewMaps()),
c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cNewmapEditorState.cpp:274:            m_scenarioFlow->loadMapFromEditor(-1); // -1 means load the map from the editor, instead of loading a skirmish map
c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cSetupSkirmishState.cpp:398:                    m_scenarioFlow->loadMapFromEditor(iSkirmishMap);
```

### git show c5834615f8fc71789bba7108078a461018cc7d56:resources/bin/settings.ini | nl -ba | grep -i 'editor'

```text
git show c5834615f8fc71789bba7108078a461018cc7d56:resources/bin/settings.ini | nl -ba | grep -i 'editor'
    87	GFXEDITOR=sdl_gfxeditor.dat
   140	EDITOR_SAVE=Ctrl,S
   141	EDITOR_ZOOM_IN=Page Up
   142	EDITOR_ZOOM_OUT=Page Down
```

### ls -la /srv/dune/worktrees/u34/.tmp/out/run/bin/data/sdl_gfxeditor.dat

```text
ls -la /srv/dune/worktrees/u34/.tmp/out/run/bin/data/sdl_gfxeditor.dat
-rw-r--r-- 1 root root 77345 Nov 10 18:11 /srv/dune/worktrees/u34/.tmp/out/run/bin/data/sdl_gfxeditor.dat
```

