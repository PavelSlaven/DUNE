### src/drawers/cUnitDrawer.h@acddd29

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.h | nl -ba
     1	/**
     2	 * @file cUnitDrawer.h
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
    18	class cUnit;
    19	class SDLDrawer;
    20	class Graphics;
    21	class cTextDrawer;
    22	
    23	class cUnitDrawer {
    24	public:
    25	    cUnitDrawer(cUnit &unit, SDLDrawer *renderer, Graphics *gfxdata);
    26	    ~cUnitDrawer() = default;
    27	
    28	    void draw();
    29	    void draw_health();
    30	    void draw_experience();
    31	    void draw_spice();
    32	    void draw_group(cTextDrawer *textDrawer);
    33	    void draw_path() const;
    34	    void draw_debug(cTextDrawer *textDrawer);
    35	
    36	private:
    37	    cUnit &m_unit;
    38	    SDLDrawer *m_renderer;
    39	    Graphics *m_gfxdata;
    40	};
```

### src/gamestates/cWinLoseState.h@acddd29

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.h | nl -ba
     1	/**
     2	 * @file cWinLoseState.h
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
    22	class Texture;
    23	
    24	class cGameSettings;
    25	class MissionFlow;
    26	class GameStateTransition;
    27	class cMouse;
    28	class cTextDrawer;
    29	
    30	enum class Outcome : char {Win, Lose};
    31	
    32	
    33	class cWinLoseState : public cGameState {
    34	public:
    35	    explicit cWinLoseState(sGameServices* services, Outcome value);
    36	    ~cWinLoseState() override;
    37	
    38	    void thinkFast() override;
    39	    void draw() const override;
    40	
    41	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    42	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    43	
    44	    eGameStateType getType() override;
    45	
    46	private:
    47	    cGameSettings* m_settings = nullptr;
    48	    cTextDrawer* m_textDrawer = nullptr;
    49	    MissionFlow* m_missionFlow = nullptr;
    50	    GameStateTransition* m_stateTransitions = nullptr;
    51	    cMouse* m_mouse = nullptr;
    52	    Texture *const *m_backgroundTexture = nullptr;
    53	    Texture *m_tex = nullptr;
    54	    Texture *m_hdOutcomeTexture = nullptr;
    55	    Outcome m_statement;
    56	    void onMouseLeftButtonClicked(const s_MouseEvent &event) const;
    57	};
```

### src/gamestates/cGamePlaying.h@acddd29

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.h | nl -ba
     1	/**
     2	 * @file cGamePlaying.h
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
    20	#include "controls/eKeyAction.h"
    21	#include "controls/sMouseEvent.h"
    22	#include <optional>
    23	#include <vector>
    24	#include <SDL3/SDL.h>
    25	
    26	class Texture;
    27	
    28	class cReinforcements;
    29	class cTextDrawer;
    30	class cTimeManager;
    31	class cMapCamera;
    32	class ScenarioFlow;
    33	class MissionFlow;
    34	class GameStateTransition;
    35	class cStructureFactory;
    36	class cDrawManager;
    37	class cPlayer;
    38	class cTextDrawer;
    39	class cInfoContext;
    40	class cStructureUtils;
    41	class cScreenFader;
    42	class cScreenShake;
    43	class cEventEmitter;
    44	class AudioContext;
    45	class cMouse;
    46	class cRectangle;
    47	struct CommonEvent;
    48	struct DeployUnitEvent;
    49	struct LaunchDeathHandEvent;
    50	class cGameObjectContext;
    51	class cGameSettings;
    52	
    53	class cGamePlaying : public cGameState {
    54	public:
    55	    explicit cGamePlaying(sGameServices* services);
    56	    ~cGamePlaying() override;
    57	
    58	    void thinkFast() override;
    59	    void thinkNormal() override;
    60	    void thinkSlow() override;
    61	    void draw() const override;
    62	    void update() override;
    63	
    64	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    65	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    66	    void onNotifyGameEvent(const s_GameEvent &event) override;
    67	
    68	    void onPlayerDefeated(cPlayer *player);
    69	
    70	    eGameStateType getType() override;
    71	
    72	    void missionInit();
    73	private:
    74	    void drawTextFps() const;
    75	    void drawTextTime() const;
    76	    cGameObjectContext* m_objects = nullptr;
    77	    cInfoContext *m_info = nullptr;
    78	    cGameSettings* m_settings = nullptr;
    79	    cStructureUtils *m_structureUtils = nullptr;
    80	    cReinforcements* m_reinforcements = nullptr;
    81	    ScenarioFlow* m_scenarioFlow = nullptr;
    82	    GameStateTransition* m_stateTransitions = nullptr;
    83	    MissionFlow* m_missionFlow = nullptr;
    84	    AudioContext* m_audioContext = nullptr;
    85	    cScreenFader* m_screenFader = nullptr;
    86	    cMapCamera* m_mapCamera = nullptr;
    87	    cRectangle* m_mapViewport = nullptr;
    88	    cMouse* m_mouse = nullptr;
    89	    cEventEmitter* m_eventEmitter = nullptr;
    90	    cScreenShake* m_screenShake = nullptr;
    91	    cStructureFactory* m_structureFactory = nullptr;
    92	    cDrawManager *m_drawManager = nullptr;
    93	    cPlayer *m_controlledPlayer = nullptr;
    94	    cTextDrawer* m_textDrawer = nullptr;
    95	    cTimeManager* m_timeManager = nullptr;
    96	    void evaluatePlayerStatus();
    97	    void drawCombatMouse() const;
    98	    int m_TIMER_evaluatePlayerStatus;
    99	    
   100	
   101	    void onKeyDownGamePlaying(const cKeyboardEvent &event);
   102	    void onKeyPressedGamePlaying(const cKeyboardEvent &event);
   103	    void onKeyDownDebugMode(const cKeyboardEvent &event);
   104	    void tryDebugSwitchToPlayer(int playerIndex);
   105	    void onEventEntityDestroyed(const CommonEvent &event);
   106	    void onEventCreateUnit(const DeployUnitEvent &event);
   107	    void onEventSpecialLaunch(const LaunchDeathHandEvent &event);
   108	
   109	    void centerCameraOnUnits(const std::vector<int>& unitIds);
   110	    void drawTrackingOverlays() const;
   111	
   112	    std::vector<int> m_trackedUnitIds;
   113	    int m_lastGroupKeyPressed = 0;
   114	    Uint32 m_lastGroupKeyPressedTick = 0;
   115	    std::optional<eKeyAction> m_lastDebugSwitchAction;
   116	};
```

### cUnitDrawer::draw_spice — src/drawers/cUnitDrawer.cpp@acddd29:48-66

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.cpp | nl -ba | sed -n '48,66p'
    48	void cUnitDrawer::draw_spice()
    49	{
    50	    float width_x = m_unit.getMapCamera()->factorZoomLevel(m_unit.getBmpWidth());
    51	    int height_y = m_unit.getMapCamera()->factorZoomLevel(4);
    52	    int drawx = m_unit.draw_x();
    53	    int drawy = m_unit.draw_y() - ((height_y * 2) + 2);
    54	
    55	    int max = m_unit.getUnitInfo().credit_capacity;
    56	    int w = healthBar(width_x, m_unit.iCredits, max);
    57	
    58	    // bar itself
    59	    m_renderer->renderRectFillColor(drawx, drawy, width_x, height_y, 0, 0, 0,ShadowTrans);
    60	    m_renderer->renderRectFillColor(drawx, drawy, w, height_y, 255, 91, 1,ShadowTrans);
    61	
    62	    // bar around it (only when it makes sense due zooming)
    63	    if (height_y > 2) {
    64	        m_renderer->renderRectColor(drawx, drawy,width_x, height_y, 255, 255, 255,ShadowTrans);
    65	    }
    66	}
```

### cUnitDrawer::draw_health — src/drawers/cUnitDrawer.cpp@acddd29:68-94

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.cpp | nl -ba | sed -n '68,94p'
    68	void cUnitDrawer::draw_health()
    69	{
    70	    if (m_unit.getHitPoints() < 0) return;
    71	
    72	    // draw units health
    73	    float width_x = m_unit.getMapCamera()->factorZoomLevel(m_unit.getBmpWidth());
    74	    int height_y = m_unit.getMapCamera()->factorZoomLevel(4);
    75	    int drawx = m_unit.draw_x();
    76	    int drawy = m_unit.draw_y() - (height_y + 2);
    77	
    78	    float healthNormalized = m_unit.getHealthNormalized();
    79	
    80	    int w = healthNormalized * width_x;
    81	    int r = (1.1 - healthNormalized) * 255;
    82	    int g = healthNormalized * 255;
    83	
    84	    if (r > 255) r = 255;
    85	
    86	    // bar itself
    87	    m_renderer->renderRectFillColor(drawx, drawy, width_x, height_y, 0, 0, 0,ShadowTrans);
    88	    m_renderer->renderRectFillColor(drawx, drawy, (w - 1), height_y, static_cast<Uint8>(r),static_cast<Uint8>(g), 32,ShadowTrans);
    89	
    90	    // bar around it (only when it makes sense due zooming)
    91	    if (height_y > 2) {
    92	        m_renderer->renderRectColor(drawx, drawy, width_x, height_y, 255, 255, 255,ShadowTrans);
    93	    }
    94	}
```

### cUnitDrawer::draw_group — src/drawers/cUnitDrawer.cpp@acddd29:96-121

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.cpp | nl -ba | sed -n '96,121p'
    96	void cUnitDrawer::draw_group(cTextDrawer* textDrawer)
    97	{
    98	    if (m_unit.getHitPoints() < 0) return;
    99	
   100	    int height_y = m_unit.getMapCamera()->factorZoomLevel(4);
   101	    int drawx = m_unit.draw_x();
   102	    int drawy = m_unit.draw_y() - (height_y + 2);
   103	    // draw group
   104	    // TODO: make text smaller depending on zoom factor?
   105	    if (m_unit.iPlayer == HUMAN) {
   106	        std::string groups;
   107	        for (int i = 0; i < MAX_UNIT_GROUPS; i++) {
   108	            if (m_unit.iGroups[i]) {
   109	                if (!groups.empty()) {
   110	                    groups += " ";
   111	                }
   112	                groups += std::to_string(i + 1);
   113	            }
   114	        }
   115	
   116	        if (!groups.empty()) {
   117	            textDrawer->drawText(drawx + 26, drawy - 11, Color::Black, groups);
   118	            textDrawer->drawText(drawx + 26, drawy - 12, Color::White, groups);
   119	        }
   120	    }
   121	}
```

### cUnitDrawer::draw_experience — src/drawers/cUnitDrawer.cpp@acddd29:123-156

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.cpp | nl -ba | sed -n '123,156p'
   123	void cUnitDrawer::draw_experience()
   124	{
   125	    int iStars = static_cast<int>(m_unit.fExperience);
   126	
   127	    if (iStars < 1)
   128	        return; // no stars to draw!
   129	
   130	    int iStarType = 0;
   131	
   132	    // twice correct and upgrade star type
   133	    if (iStars > 2) {
   134	        iStarType++;
   135	        iStars -= 3;
   136	    }
   137	
   138	    // red stars now, very much experience!
   139	    if (iStars > 2) {
   140	        iStarType++;
   141	        iStars -= 3;
   142	    }
   143	
   144	    // still enough experience! wow
   145	    if (iStars > 2) {
   146	        iStars = 3;
   147	    }
   148	
   149	
   150	    int drawx = m_unit.draw_x() + 3;
   151	    int drawy = m_unit.draw_y() - 19;
   152	    // 1 star = 1 experience
   153	    for (int i = 0; i < iStars; i++) {
   154	        m_renderer->renderSprite(m_gfxdata->getTexture(OBJECT_STAR_01 + iStarType), drawx + i * 9, drawy, ShadowTrans);
   155	    }
   156	}
```

### cWinLoseState::cWinLoseState — src/gamestates/cWinLoseState.cpp@acddd29:38-73

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '38,73p'
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
```

### cWinLoseState::~cWinLoseState — src/gamestates/cWinLoseState.cpp@acddd29:75-78

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '75,78p'
    75	cWinLoseState::~cWinLoseState()
    76	{
    77	    delete m_hdOutcomeTexture;
    78	}
```

### cWinLoseState::thinkFast — src/gamestates/cWinLoseState.cpp@acddd29:80-82

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '80,82p'
    80	void cWinLoseState::thinkFast()
    81	{
    82	}
```

### cWinLoseState::draw — src/gamestates/cWinLoseState.cpp@acddd29:84-114

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '84,114p'
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
```

### cWinLoseState::onNotifyMouseEvent — src/gamestates/cWinLoseState.cpp@acddd29:116-125

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '116,125p'
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
```

### cWinLoseState::getType — src/gamestates/cWinLoseState.cpp@acddd29:127-130

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '127,130p'
   127	eGameStateType cWinLoseState::getType()
   128	{
   129	    return GAMESTATE_WINLOSE;
   130	}
```

### cWinLoseState::onNotifyKeyboardEvent — src/gamestates/cWinLoseState.cpp@acddd29:132-134

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '132,134p'
   132	void cWinLoseState::onNotifyKeyboardEvent(const cKeyboardEvent &)
   133	{
   134	}
```

### cWinLoseState::onMouseLeftButtonClicked — src/gamestates/cWinLoseState.cpp@acddd29:136-145

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '136,145p'
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

### cDrawManager::drawCombatState — src/managers/cDrawManager.cpp@acddd29:119-175

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '119,175p'
   119	void cDrawManager::drawCombatState()
   120	{
   121	    // MAP
   122	    m_sdlDrawer->setClippingFor(0, cSideBar::TopBarHeight, m_mapCamera->getWindowWidth(), m_gameSettings->getScreenH());
   123	    m_mapDrawer->drawTerrain();
   124	
   125	    m_structureDrawer->drawStructuresFirstLayer();
   126	
   127	    // draw layer 1 (beneath units, on top of terrain)
   128	    m_particleDrawer->determineParticlesToDraw(*m_mapViewport);
   129	    m_particleDrawer->drawLowerLayer();
   130	
   131	    m_objects->getMap()->draw_units();
   132	
   133	    m_objects->getMap()->draw_bullets();
   134	
   135	    m_structureDrawer->drawStructuresSecondLayer();
   136	
   137	    m_objects->getMap()->draw_units_2nd();
   138	
   139	    m_particleDrawer->drawTopLayer();
   140	
   141	    // what was last seen of fogged cells covers anything live in the fog
   142	    m_mapDrawer->drawRememberedTerrain();
   143	    m_structureDrawer->drawRememberedStructures();
   144	    m_objects->getMap()->drawRememberedUnits();
   145	
   146	    m_structureDrawer->drawStructuresHealthBars();
   147	
   148	    m_mapDrawer->drawShroud();
   149	
   150	    // after the shroud: an attacker on a never explored cell would otherwise be painted over in black
   151	    m_objects->getMap()->drawRevealedUnitsInFog();
   152	
   153	    drawRallyPoint();
   154	
   155	    m_sdlDrawer->resetClippingFor();
   156	
   157	    // GUI
   158	    drawSidebar();
   159	
   160	    m_sdlDrawer->setClippingFor(0, cSideBar::TopBarHeight, m_mapCamera->getWindowWidth(), m_mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
   161	    drawStructurePlacing();
   162	    m_sdlDrawer->resetClippingFor();
   163	
   164	    drawTopBarBackground();
   165	    drawCredits();
   166	
   167	    // THE MESSAGE
   168	    drawMessage();
   169	
   170	    m_sdlDrawer->resetClippingFor();
   171	
   172	    if (m_gameSettings->isDrawUsages()) {
   173	        drawDebugInfoUsages();
   174	    }
   175	}
```

### cDrawManager::drawDebugInfoUsages — src/managers/cDrawManager.cpp@acddd29:177-215

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '177,215p'
   177	void cDrawManager::drawDebugInfoUsages() const
   178	{
   179	    int unitsUsed = 0;
   180	    for (int i = 0; i < m_objects->getUnitsSize(); i++) {
   181	        if (m_objects->getUnit(i)->isValid()) {
   182	            unitsUsed++;
   183	        }
   184	    }
   185	
   186	    int structuresUsed = 0;
   187	    for (int i = 0; i < MAX_STRUCTURES; i++) {
   188	        cAbstractStructure *pStructure = m_objects->getStructures()[i];
   189	        if (pStructure) {
   190	            structuresUsed++;
   191	        }
   192	    }
   193	
   194	    int bulletsUsed = 0;
   195	    for (const auto& bullet : m_objects->getBullets()) {
   196	        if (bullet.bAlive) {
   197	            bulletsUsed++;
   198	        }
   199	    }
   200	
   201	    int particlesUsed = 0;
   202	    for (const auto& particle : m_objects->getParticles()) {
   203	        if (particle.isValid()) {
   204	            particlesUsed++;
   205	        }
   206	    }
   207	
   208	    int startY = 74;
   209	    int height = 14;
   210	    m_textDrawer->drawText(0, startY, std::format("Units {}/{}", unitsUsed, m_objects->getUnitsSize()));
   211	    m_textDrawer->drawText(0, startY + (1*height), std::format("Structures {}/{}", structuresUsed, MAX_STRUCTURES));
   212	    m_textDrawer->drawText(0, startY + (2*height), std::format("Bullets {}/{}", bulletsUsed, m_objects->getBullets().size()));
   213	    m_textDrawer->drawText(0, startY + (3*height), std::format("Particles {}/{}", particlesUsed, cParticles::size()));
   214	    m_textDrawer->drawText(0, startY + (4*height), std::format("Visible particles BOTTOM: {}/ TOP: {}", m_particleDrawer->getParticlesLowerLayerAmount(), m_particleDrawer->getParticlesTopLayerAmount()));
   215	}
```

### cDrawManager::drawCredits — src/managers/cDrawManager.cpp@acddd29:217-220

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '217,220p'
   217	void cDrawManager::drawCredits()
   218	{
   219	    m_creditsDrawer->draw();
   220	}
```

### cDrawManager::drawRallyPoint — src/managers/cDrawManager.cpp@acddd29:222-251

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '222,251p'
   222	void cDrawManager::drawRallyPoint()
   223	{
   224	    if (m_player->selected_structure < 0) return;
   225	    cAbstractStructure *theStructure = m_objects->getStructures()[m_player->selected_structure];
   226	    if (!theStructure) return;
   227	    int rallyPointCell = theStructure->getRallyPoint();
   228	    if (rallyPointCell < 0) return;
   229	
   230	    int drawX = m_mapCamera->getWindowXPositionFromCell(rallyPointCell);
   231	    int drawY = m_mapCamera->getWindowYPositionFromCell(rallyPointCell);
   232	
   233	    Texture *mouseMoveBitmap = m_gfxdata->getTexture(MOUSE_MOVE);
   234	
   235	    int rallyPointWidthScaled = m_mapCamera->factorZoomLevel(mouseMoveBitmap->w);
   236	    int rallyPointHeightScaled = m_mapCamera->factorZoomLevel(mouseMoveBitmap->h);
   237	    cRectangle dest = {drawX, drawY, rallyPointWidthScaled, rallyPointHeightScaled};
   238	    m_sdlDrawer->renderStrechFullSprite(m_gfxdata->getTexture(MOUSE_MOVE), dest);
   239	
   240	    int startX = theStructure->iDrawX() + m_mapCamera->factorZoomLevel(theStructure->getWidthInPixels() / 2);
   241	    int startY = theStructure->iDrawY() + m_mapCamera->factorZoomLevel(theStructure->getHeightInPixels() / 2);
   242	
   243	    int offset = (mouseMoveBitmap->w/2);
   244	    drawX = m_mapCamera->getWindowXPositionFromCellWithOffset(rallyPointCell, offset);
   245	    drawY = m_mapCamera->getWindowYPositionFromCellWithOffset(rallyPointCell, offset);
   246	
   247	    int endX = drawX;
   248	    int endY = drawY;
   249	
   250	    m_sdlDrawer->renderLine( startX, startY, endX, endY, m_player->getMinimapColor());
   251	}
```

### cDrawManager::drawSidebar — src/managers/cDrawManager.cpp@acddd29:253-259

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '253,259p'
   253	void cDrawManager::drawSidebar()
   254	{
   255	    m_sdlDrawer->setClippingFor(m_gameSettings->getScreenW() - cSideBar::SidebarWidth, 0, m_gameSettings->getScreenW(), m_gameSettings->getScreenH());
   256	    m_sidebarDrawer->draw();
   257	    m_miniMapDrawer->draw();
   258	    m_sdlDrawer->resetClippingFor();
   259	}
```

### cDrawManager::drawStructurePlacing — src/managers/cDrawManager.cpp@acddd29:264-274

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '264,274p'
   264	void cDrawManager::drawStructurePlacing()
   265	{
   266	    // TODO: move drawing this into mouse state draw function ??
   267	    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) return;
   268	    if (!m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) return;
   269	
   270	    cBuildingListItem *itemToPlace = m_player->getSideBar()->getList(eListType::LIST_CONSTYARD)->getItemToPlace();
   271	    if (itemToPlace == nullptr) return;
   272	
   273	    m_placeitDrawer->draw(itemToPlace, m_player->getGameControlsContext()->getMouseCell());
   274	}
```

### cDrawManager::drawMessage — src/managers/cDrawManager.cpp@acddd29:276-281

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '276,281p'
   276	void cDrawManager::drawMessage()
   277	{
   278	    m_messageDrawer->draw();
   279	    // TODO: replace messageDrawer with drawMessageBar?
   280	    // messageBarDrawer->drawMessageBar();
   281	}
```

### cDrawManager::drawCombatMouse — src/managers/cDrawManager.cpp@acddd29:283-291

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '283,291p'
   283	void cDrawManager::drawCombatMouse()
   284	{
   285	    drawMouse();
   286	
   287	    cGameControlsContext *context = m_player->getGameControlsContext();
   288	    if (m_drawToolTip && context->isMouseOnBattleField() ) {
   289	        m_mouseDrawer->drawToolTip();
   290	    }
   291	}
```

### cDrawManager::drawMouse — src/managers/cDrawManager.cpp@acddd29:293-296

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '293,296p'
   293	void cDrawManager::drawMouse()
   294	{
   295	    m_mouseDrawer->draw();
   296	}
```

### cDrawManager::drawTopBarBackground — src/managers/cDrawManager.cpp@acddd29:298-342

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '298,342p'
   298	void cDrawManager::drawTopBarBackground()
   299	{
   300	    const Color panel{17, 21, 23, 255};
   301	    const Color border{151, 113, 43, 255};
   302	    const Color text{232, 222, 188, 255};
   303	    m_sdlDrawer->renderRectFillColor(
   304	        0,
   305	        0,
   306	        m_gameSettings->getScreenW(),
   307	        cSideBar::TopBarHeight,
   308	        panel
   309	    );
   310	    m_sdlDrawer->renderLine(
   311	        0,
   312	        cSideBar::TopBarHeight - 2,
   313	        m_gameSettings->getScreenW(),
   314	        cSideBar::TopBarHeight - 2,
   315	        border
   316	    );
   317	
   318	    const cRectangle optionsRect(7, 4, 126, 33);
   319	    m_sdlDrawer->renderRectFillColor(
   320	        optionsRect.getX(),
   321	        optionsRect.getY(),
   322	        optionsRect.getWidth(),
   323	        optionsRect.getHeight(),
   324	        Color{27, 31, 33, 255}
   325	    );
   326	    m_sdlDrawer->renderRectColor(
   327	        optionsRect.getX(),
   328	        optionsRect.getY(),
   329	        optionsRect.getWidth(),
   330	        optionsRect.getHeight(),
   331	        border
   332	    );
   333	    m_textDrawer->drawTextCenteredInBox("OPTIONS", optionsRect, text);
   334	    if (m_mouse->isLeftButtonClicked() &&
   335	        m_mouse->isOverRectangle(
   336	            optionsRect.getX(),
   337	            optionsRect.getY(),
   338	            optionsRect.getWidth(),
   339	            optionsRect.getHeight())) {
   340	        m_stateTransitions->setNextState(GAME_OPTIONS);
   341	    }
   342	}
```

### cDrawManager::drawMessageBar — src/managers/cDrawManager.cpp@acddd29:435-438

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '435,438p'
   435	void cDrawManager::drawMessageBar()
   436	{
   437	    m_messageDrawer->draw();
   438	}
```

### cGamePlaying::cGamePlaying — src/gamestates/cGamePlaying.cpp@acddd29:75-123

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp | nl -ba | sed -n '75,123p'
    75	cGamePlaying::cGamePlaying(sGameServices* services) :
    76	    cGameState(services),
    77	    m_objects(services->objects),
    78	    m_info(services->info),
    79	    m_settings(services->settings),
    80	    m_structureUtils(services->structureUtils)
    81	{
    82	    d2tm_assert(m_objects != nullptr);
    83	    d2tm_assert(m_info != nullptr);
    84	    d2tm_assert(m_settings != nullptr);
    85	    d2tm_assert(m_structureUtils != nullptr);
    86	    m_TIMER_evaluatePlayerStatus = 5;
    87	
    88	    //fix others pointers
    89	    m_scenarioFlow = services->scenarioFlow;
    90	    d2tm_assert(m_scenarioFlow != nullptr);
    91	    m_missionFlow = services->missionFlow;
    92	    d2tm_assert(m_missionFlow != nullptr);
    93	    m_stateTransitions = services->stateTransitions;
    94	    d2tm_assert(m_stateTransitions != nullptr);
    95	    m_audioContext = m_ctx->getAudioContext();
    96	    d2tm_assert(m_audioContext != nullptr);
    97	    m_screenFader = services->screenFader;
    98	    d2tm_assert(m_screenFader != nullptr);
    99	    m_mapCamera = services->mapCamera;
   100	    d2tm_assert(m_mapCamera != nullptr);
   101	    m_mapViewport = services->mapViewport;
   102	    d2tm_assert(m_mapViewport != nullptr);
   103	    m_mouse = services->mouse;
   104	    d2tm_assert(m_mouse != nullptr);
   105	    m_eventEmitter = services->eventEmitter;
   106	    d2tm_assert(m_eventEmitter != nullptr);
   107	    m_screenShake = services->screenShake;
   108	    d2tm_assert(m_screenShake != nullptr);
   109	    m_reinforcements = services->reinforcements;
   110	    d2tm_assert(m_reinforcements != nullptr);
   111	    m_structureFactory = services->objects->getStructureFactory();
   112	    d2tm_assert(m_structureFactory != nullptr);
   113	    m_drawManager = services->drawManager;
   114	    d2tm_assert(m_drawManager != nullptr);
   115	    m_textDrawer = m_ctx->getTextContext()->getBeneTextDrawer();
   116	    m_timeManager = m_ctx->getTimeManager();
   117	    d2tm_assert(m_textDrawer != nullptr);
   118	    d2tm_assert(m_timeManager != nullptr);
   119	
   120	    m_controlledPlayer = m_objects->getPlayer(HUMAN);
   121	    m_drawManager->setPlayerToDraw(m_controlledPlayer);
   122	    m_scenarioFlow->setPlayerToInteractFor(m_controlledPlayer);
   123	}
```

### cGamePlaying::thinkFast — src/gamestates/cGamePlaying.cpp@acddd29:145-222

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp | nl -ba | sed -n '145,222p'
   145	void cGamePlaying::thinkFast()
   146	{
   147	    m_drawManager->thinkFast_statePlaying();
   148	
   149	    m_mapCamera->thinkFast();
   150	
   151	    for (cPlayer* pPlayer : m_objects->getPlayers()) {
   152	        pPlayer->thinkFast();
   153	    }
   154	
   155	    // structures think
   156	    for (const auto &slot : m_objects->getStructures()) {
   157	        cAbstractStructure *pStructure = slot.get();
   158	        if (pStructure == nullptr) continue;
   159	        if (pStructure->isValid()) {
   160	            pStructure->thinkFast();       // think about actions going on
   161	            pStructure->think_animation(); // think about animating
   162	            pStructure->think_guard();     // think about 'guarding' the area (turrets only)
   163	        }
   164	
   165	        if (pStructure->isDead()) {
   166	            m_structureFactory->deleteStructureInstance(pStructure);
   167	        }
   168	    }
   169	
   170	    // structures that died since the last tick are no longer referenced
   171	    m_objects->getStructures().destroyDetached();
   172	
   173	    for (cPlayer* pPlayer : m_objects->getPlayers()) {
   174	        cItemBuilder *itemBuilder = pPlayer->getItemBuilder();
   175	        if (itemBuilder) {
   176	            itemBuilder->thinkFast();
   177	        }
   178	    }
   179	
   180	    m_objects->getMap()->thinkFast();
   181	
   182	    m_screenShake->reduce();
   183	
   184	    // units think (move only)
   185	    for (cUnit &cUnit : *m_objects->getUnits()) {
   186	        if (!cUnit.isValid()) continue;
   187	        cUnit.thinkFast();
   188	    }
   189	
   190	    for (cParticle &pParticle : m_objects->getParticles()) {
   191	        if (!pParticle.isValid()) continue;
   192	        pParticle.thinkFast();
   193	    }
   194	
   195	    // when not drawing the options, the game does all it needs to do
   196	    // bullets think
   197	    for (cBullet &cBullet : m_objects->getBullets()) {
   198	        if (!cBullet.bAlive) continue;
   199	        cBullet.thinkFast();
   200	    }
   201	
   202	    if (!m_trackedUnitIds.empty()) {
   203	        std::erase_if(m_trackedUnitIds, [&](int id) {
   204	            return !m_objects->getUnit(id)->isValid();
   205	        });
   206	        if (!m_trackedUnitIds.empty()) {
   207	            float sumX = 0, sumY = 0;
   208	            cExpandingRectangle bounds;
   209	            for (int id : m_trackedUnitIds) {
   210	                cUnit* u = m_objects->getUnit(id);
   211	                float px = u->getPosX(), py = u->getPosY();
   212	                sumX += px; sumY += py;
   213	                bounds.expand(px, py);
   214	            }
   215	            bounds.expandBy(3 * TILESIZE_WIDTH_PIXELS);
   216	            m_mapCamera->zoomOutToFit(bounds);
   217	
   218	            int count = static_cast<int>(m_trackedUnitIds.size());
   219	            m_mapCamera->trackToAbsPosition(sumX / count, sumY / count);
   220	        }
   221	    }
   222	}
```

### cGamePlaying::draw — src/gamestates/cGamePlaying.cpp@acddd29:300-315

```text
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp | nl -ba | sed -n '300,315p'
   300	void cGamePlaying::draw() const
   301	{
   302	    m_drawManager->drawCombatState();
   303	    drawTrackingOverlays();
   304	    if (m_settings->shouldDrawFps()) {
   305	        drawTextFps();
   306	    }
   307	
   308	    drawCombatMouse();
   309	
   310	    if (m_settings->shouldDrawTime()) {
   311	        drawTextTime();
   312	    }
   313	    // MOUSE
   314	    m_drawManager->drawCombatMouse();
   315	}
```

