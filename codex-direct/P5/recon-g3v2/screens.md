### src/gamestates/cNewmapEditorState.cpp@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cNewmapEditorState.cpp | nl -ba
     1	/**
     2	 * @file cNewmapEditorState.cpp
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
    16	#include "gamestates/cNewMapEditorState.h"
    17	#include "game/GameStateTransition.hpp"
    18	#include "game/ScenarioFlow.hpp"
    19	#include "controls/cMouse.h"
    20	
    21	#include "gui/GuiButton.h"
    22	#include "gui/GuiWindow.h"
    23	#include "gui/GuiLabel.hpp"
    24	#include "gui/GuiTextInput.h"
    25	#include "gui/GuiCycleButton.h"
    26	#include "gui/GuiCheckBox.hpp"
    27	#include "context/GameContext.hpp"
    28	#include "context/cGameObjectContext.h"
    29	#include "drawers/cTextDrawer.h"
    30	#include "gameobjects/map/cPreviewMaps.h"
    31	#include "gameobjects/map/cRandomMapGenerator.h"
    32	#include "gameobjects/map/SeedMapLoader.hpp"
    33	#include "utils/ini.h"
    34	#include "utils/Log.h"
    35	
    36	#include "include/cAssert.h"
    37	#include "context/TextContext.hpp"
    38	#include "game/cGameSettings.h"
    39	#include "gamestates/cGameState.h"
    40	#include "include/sGameServices.h"
    41	#include "include/eGameState.h"
    42	#include <charconv>
    43	#include <chrono>
    44	#include <optional>
    45	
    46	static const int borderSize = 2;
    47	
    48	cNewMapEditorState::cNewMapEditorState(sGameServices* services, cIni* ini)
    49	    : cGameState(services),
    50	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    51	    m_settings(services->settings),
    52	    m_scenarioFlow(services->scenarioFlow),
    53	    m_stateTransitions(services->stateTransitions),
    54	    m_mouse(services->mouse),
    55	    m_guiWindow(nullptr),
    56	    m_objects(services->objects),
    57	    m_previewMap(services->objects->getPreviewMaps()),
    58	    m_cIni(ini)
    59	{
    60	    d2tm_assert(m_textDrawer != nullptr);
    61	    d2tm_assert(m_settings != nullptr);
    62	    d2tm_assert(m_scenarioFlow != nullptr);
    63	    d2tm_assert(m_stateTransitions != nullptr);
    64	    d2tm_assert(m_cIni != nullptr);
    65	    constructWindow();
    66	}
    67	
    68	void cNewMapEditorState::constructWindow()
    69	{
    70	    int margin = m_settings->getScreenH() * 0.3;
    71	    int mainMenuFrameX = margin;
    72	    int mainMenuFrameY = margin;
    73	    int mainMenuWidth = m_settings->getScreenW() - (margin * 2);
    74	    int mainMenuHeight = m_settings->getScreenH() - (margin * 2);
    75	
    76	    margin = 4;
    77	    int buttonHeight = (m_textDrawer->getFontHeight() + margin);
    78	    int buttonWidth = mainMenuWidth - 8;
    79	
    80	    const cRectangle &window = cRectangle(mainMenuFrameX, mainMenuFrameY, mainMenuWidth, mainMenuHeight);
    81	    m_guiWindow = std::make_unique<GuiWindow>(m_sdlDrawer, window, m_textDrawer);
    82	    m_guiWindow->setTheme(cGuiThemeBuilder().light().build());
    83	
    84	    // Title
    85	    m_guiWindow->setTitle("Map editor configuration");
    86	
    87	    int labelX = 55;
    88	    int labelY = 45;
    89	    int betweenY =30;
    90	
    91	    // name
    92	    const cRectangle &nameRect = m_guiWindow->getRelativeRect(labelX, labelY, 75, buttonHeight);
    93	    auto gui_NameLabel = GuiLabelBuilder()
    94	        .withLabel("Name your map:")
    95	        .withTextDrawer(m_textDrawer)
    96	        .withRenderer(m_sdlDrawer)
    97	        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
    98	        .withTextAlign(GuiTextAlignHorizontal::LEFT)
    99	        .withRect(nameRect)
   100	        .build();
   101	    m_guiWindow->addGuiObject(std::move(gui_NameLabel));
   102	
   103	    auto inputName = std::make_unique<GuiTextInput>( m_sdlDrawer,
   104	        m_guiWindow->getRelativeRect(labelX+200, labelY-2, 200, m_textDrawer->getFontHeight() + 4),
   105	        m_textDrawer);
   106	    inputName->setTheme(cGuiThemeBuilder().light().build()); 
   107	    m_inputName = inputName.get();
   108	    m_guiWindow->addGuiObject(std::move(inputName));
   109	
   110	    // author
   111	    const cRectangle &authorRect = m_guiWindow->getRelativeRect(labelX, labelY+betweenY, 75, buttonHeight);
   112	    auto gui_authorLabel = GuiLabelBuilder()
   113	        .withLabel("Name of author:")
   114	        .withTextDrawer(m_textDrawer)
   115	        .withRenderer(m_sdlDrawer)
   116	        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
   117	        .withTextAlign(GuiTextAlignHorizontal::LEFT)
   118	        .withRect(authorRect)
   119	        .build();
   120	    m_guiWindow->addGuiObject(std::move(gui_authorLabel));
   121	    
   122	    auto inputAuthor = std::make_unique<GuiTextInput>(m_sdlDrawer, 
   123	        m_guiWindow->getRelativeRect(labelX+200, labelY+betweenY-2, 200, m_textDrawer->getFontHeight() + 4),
   124	        m_textDrawer);
   125	    inputAuthor->setTheme(cGuiThemeBuilder().light().build());
   126	    m_inputAuthor = inputAuthor.get();
   127	    m_guiWindow->addGuiObject(std::move(inputAuthor));
   128	
   129	    // Description
   130	    const cRectangle &descriptionRect = m_guiWindow->getRelativeRect(labelX, labelY+betweenY*2, 75, buttonHeight);
   131	    auto gui_descriptionLabel = GuiLabelBuilder()
   132	        .withLabel("Description:")
   133	        .withTextDrawer(m_textDrawer)
   134	        .withRenderer(m_sdlDrawer)
   135	        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
   136	        .withTextAlign(GuiTextAlignHorizontal::LEFT)
   137	        .withRect(descriptionRect)
   138	        .build();
   139	    m_guiWindow->addGuiObject(std::move(gui_descriptionLabel));
   140	
   141	    auto inputDescription = std::make_unique<GuiTextInput>( m_sdlDrawer,
   142	        m_guiWindow->getRelativeRect(labelX+200, labelY+betweenY*2-2, 200, m_textDrawer->getFontHeight() + 4),
   143	        m_textDrawer);
   144	    inputDescription->setTheme(cGuiThemeBuilder().light().build());
   145	    m_inputDescription = inputDescription.get();
   146	    m_guiWindow->addGuiObject(std::move(inputDescription));
   147	
   148	    // width
   149	    const cRectangle &widthRect = m_guiWindow->getRelativeRect(labelX, labelY+betweenY*3, 75, buttonHeight);
   150	    auto gui_widthLabel = GuiLabelBuilder()
   151	        .withLabel("Width size:")
   152	        .withTextDrawer(m_textDrawer)
   153	        .withRenderer(m_sdlDrawer)
   154	        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
   155	        .withTextAlign(GuiTextAlignHorizontal::LEFT)
   156	        .withRect(widthRect)
   157	        .build();
   158	    m_guiWindow->addGuiObject(std::move(gui_widthLabel));
   159	
   160	    auto cycleWidth = GuiCycleButtonBuilder()
   161	        .withRect( m_guiWindow->getRelativeRect(labelX+200, labelY+betweenY*3, 50, buttonHeight) )
   162	        .withValues( m_sizesMap )
   163	        .withTextDrawer( m_textDrawer )
   164	        .withRenderer(m_sdlDrawer)
   165	        .withTheme(cGuiThemeBuilder().light().build())
   166	        .onChanged([this](int) {
   167	            updateRandomCheckBox();
   168	        })
   169	        .build();
   170	    m_cycleWidth = cycleWidth.get();
   171	    m_guiWindow->addGuiObject(std::move(cycleWidth));
   172	
   173	    // height
   174	    const cRectangle &heightRect = m_guiWindow->getRelativeRect(labelX, labelY+betweenY*4, 75, buttonHeight);
   175	    auto gui_heightLabel = GuiLabelBuilder()
   176	        .withLabel("Height size:")
   177	        .withTextDrawer(m_textDrawer)
   178	        .withRenderer(m_sdlDrawer)
   179	        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
   180	        .withTextAlign(GuiTextAlignHorizontal::LEFT)
   181	        .withRect(heightRect)
   182	        .build();
   183	    m_guiWindow->addGuiObject(std::move(gui_heightLabel));
   184	
   185	    auto cycleHeight = GuiCycleButtonBuilder()
   186	        .withRect( m_guiWindow->getRelativeRect(labelX+200, labelY+betweenY*4, 50, buttonHeight) )
   187	        .withValues( m_sizesMap )
   188	        .withTextDrawer( m_textDrawer )
   189	        .withRenderer(m_sdlDrawer)
   190	        .withTheme( cGuiThemeBuilder().light().build() )
   191	        .onChanged([this](int) {
   192	            updateRandomCheckBox();
   193	        })
   194	        .build();
   195	    m_cycleHeight = cycleHeight.get();
   196	    m_guiWindow->addGuiObject(std::move(cycleHeight));
   197	
   198	    // random map
   199	    const cRectangle &randomRect = m_guiWindow->getRelativeRect(labelX, labelY+betweenY*5, 75, buttonHeight);
   200	    auto gui_randomLabel = GuiLabelBuilder()
   201	        .withLabel("Random:")
   202	        .withTextDrawer(m_textDrawer)
   203	        .withRenderer(m_sdlDrawer)
   204	        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
   205	        .withTextAlign(GuiTextAlignHorizontal::LEFT)
   206	        .withRect(randomRect)
   207	        .build();
   208	    m_guiWindow->addGuiObject(std::move(gui_randomLabel));
   209	
   210	    auto checkRandom = GuiCheckBoxBuilder()
   211	        .withRect(m_guiWindow->getRelativeRect(labelX+200, labelY+betweenY*5, buttonHeight, buttonHeight))
   212	        .withRenderer(m_sdlDrawer)
   213	        .withTheme(cGuiThemeBuilder().light().build())
   214	        .onCheck([this]() {
   215	            m_randomChecked = true;
   216	        })
   217	        .onUnCheck([this]() {
   218	            m_randomChecked = false;
   219	        })
   220	        .build();
   221	    checkRandom->setChecked(m_randomChecked); // GuiCheckBox starts checked
   222	    m_checkRandom = checkRandom.get();
   223	    m_guiWindow->addGuiObject(std::move(checkRandom));
   224	    updateRandomCheckBox();
   225	
   226	    // Dune 2 seed
   227	    const cRectangle &seedRect = m_guiWindow->getRelativeRect(labelX, labelY+betweenY*6, 75, buttonHeight);
   228	    auto gui_seedLabel = GuiLabelBuilder()
   229	        .withLabel("Dune 2 seed: ")
   230	        .withTextDrawer(m_textDrawer)
   231	        .withRenderer(m_sdlDrawer)
   232	        .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
   233	        .withTextAlign(GuiTextAlignHorizontal::LEFT)
   234	        .withRect(seedRect)
   235	        .build();
   236	    m_guiWindow->addGuiObject(std::move(gui_seedLabel));
   237	
   238	    auto inputSeed = std::make_unique<GuiTextInput>(m_sdlDrawer,
   239	        m_guiWindow->getRelativeRect(labelX+200, labelY+betweenY*6-2, 200, m_textDrawer->getFontHeight() + 4),
   240	        m_textDrawer);
   241	    inputSeed->setTheme(cGuiThemeBuilder().light().build());
   242	    m_inputSeed = inputSeed.get();
   243	    m_guiWindow->addGuiObject(std::move(inputSeed));
   244	
   245	    // QUIT game
   246	    int quit = mainMenuHeight - (buttonHeight + margin);// 464
   247	    int width = (buttonWidth / 2);
   248	    const cRectangle &quitRect = m_guiWindow->getRelativeRect(margin, quit, width, buttonHeight);
   249	    auto gui_btn_Quit = GuiButtonBuilder()
   250	        .withRect(quitRect)        
   251	        .withLabel("Return to menu")
   252	        .withTextDrawer(m_textDrawer)
   253	        .withRenderer(m_sdlDrawer)
   254	        .withTextAlign(GuiTextAlignHorizontal::CENTER)
   255	        .withTheme(cGuiThemeBuilder().light().build())
   256	        .onClick([this]() {
   257	            m_stateTransitions->setNextStateWithFade(GAME_MENU);
   258	        })
   259	        .build();
   260	    m_guiWindow->addGuiObject(std::move(gui_btn_Quit));
   261	
   262	    // BACK to where we came from
   263	    int back = mainMenuHeight - (buttonHeight + margin);// 444
   264	    const cRectangle &backRect = m_guiWindow->getRelativeRect(margin + width + margin, back, (width - margin), buttonHeight);
   265	    
   266	    auto gui_btn_Back = GuiButtonBuilder()
   267	        .withRect(backRect)        
   268	        .withLabel("Create map")
   269	        .withTextDrawer(m_textDrawer)
   270	        .withRenderer(m_sdlDrawer)
   271	        .withTheme(cGuiThemeBuilder().light().build())
   272	        .onClick([this](){
   273	            this->constructEmptyMap();
   274	            m_scenarioFlow->loadMapFromEditor(-1); // -1 means load the map from the editor, instead of loading a skirmish map
   275	            m_stateTransitions->setNextStateWithFade(GAME_EDITOR);
   276	        })
   277	        .build();
   278	    m_guiWindow->addGuiObject(std::move(gui_btn_Back));
   279	}
   280	
   281	cNewMapEditorState::~cNewMapEditorState()
   282	{
   283	    // Smart pointers handle cleanup
   284	}
   285	
   286	void cNewMapEditorState::thinkFast()
   287	{
   288	
   289	}
   290	
   291	void cNewMapEditorState::draw() const
   292	{
   293	    m_guiWindow->draw();
   294	    m_mouse->draw();
   295	}
   296	
   297	void cNewMapEditorState::onNotifyMouseEvent(const s_MouseEvent &event)
   298	{
   299	    m_guiWindow->onNotifyMouseEvent(event);
   300	}
   301	
   302	eGameStateType cNewMapEditorState::getType()
   303	{
   304	    return GAMESTATE_NEW_MAP_EDITOR;
   305	}
   306	
   307	void cNewMapEditorState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
   308	{
   309	    m_guiWindow->onNotifyKeyboardEvent(event);
   310	}
   311	
   312	bool cNewMapEditorState::isKeyboardCapturedByUi() const
   313	{
   314	    return m_guiWindow && m_guiWindow->hasFocusedInput();
   315	}
   316	
   317	
   318	// random maps need room: only allowed for sizes of minRandomMapSize or bigger
   319	void cNewMapEditorState::updateRandomCheckBox()
   320	{
   321	    bool allowed = m_cycleWidth->getSelectedValue() >= minRandomMapSize &&
   322	                   m_cycleHeight->getSelectedValue() >= minRandomMapSize;
   323	    m_checkRandom->setEnabled(allowed);
   324	    if (!allowed) {
   325	        m_checkRandom->setChecked(false);
   326	        m_randomChecked = false;
   327	    }
   328	}
   329	
   330	void cNewMapEditorState::constructEmptyMap()
   331	{
   332	    // On récupère les valeurs localement pour être sûr
   333	    std::string name = m_inputName->getText();
   334	    if (name.empty()) {
   335	        auto now = std::chrono::system_clock::now();
   336	        name = std::format("New unnamed map {:%Y-%m-%d %H:%M:%S}", now);
   337	    }
   338	    std::string author = m_inputAuthor->getText();
   339	    if (author.empty()) {
   340	        author = "Unknown user";
   341	    }
   342	    std::string desc = m_inputDescription->getText();
   343	    if (desc.empty()) {
   344	        desc = "Made with D2TM: Internal Editor";
   345	    }
   346	
   347	    // a seed overrides the width and height settings
   348	    const std::string &seedText = m_inputSeed->getText();
   349	    if (!seedText.empty()) {
   350	        int seed = 0;
   351	        auto [ptr, ec] = std::from_chars(seedText.data(), seedText.data() + seedText.size(), seed);
   352	        if (ec == std::errc() && ptr == seedText.data() + seedText.size()) {
   353	            s_PreviewMap seedMap = SeedMapLoader::toPreviewMap(seed);
   354	            seedMap.name = name;
   355	            seedMap.author = author;
   356	            seedMap.description = desc;
   357	            m_previewMap->setEditorMap(std::move(seedMap));
   358	            return;
   359	        }
   360	        Logger::warn(COMP_MAP, "cNewMapEditorState", "Seed [{}] is not a number, using width and height instead", seedText);
   361	    }
   362	
   363	    int width = m_cycleWidth->getSelectedValue()+borderSize;
   364	    int height = m_cycleHeight->getSelectedValue()+borderSize;
   365	
   366	    // a valid seed wins over Random, because it is the more specific request
   367	    if (m_randomChecked) {
   368	        s_PreviewMap randomMap;
   369	        cRandomMapGenerator().generateRandomMap(width, height, 4, randomMap, m_objects);
   370	        randomMap.validMap = true;
   371	        randomMap.name = name;
   372	        randomMap.author = author;
   373	        randomMap.description = desc;
   374	        m_previewMap->setEditorMap(std::move(randomMap));
   375	        return;
   376	    }
   377	    m_previewMap->createEmptyMap(name, author, desc, width, height);
   378	}
```

### src/gamestates/cScoringState.cpp@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cScoringState.cpp | nl -ba
     1	#include "gamestates/cScoringState.h"
     2	
     3	#include "context/GameContext.hpp"
     4	#include "controls/cMouse.h"
     5	#include "drawers/SDLDrawer.hpp"
     6	#include "drawers/cTextDrawer.h"
     7	#include "game/GameStateTransition.hpp"
     8	#include "game/MissionFlow.hpp"
     9	#include "game/cScreenFader.h"
    10	#include "game/cGameSettings.h"
    11	#include "game/cMissionStatsCollector.h"
    12	#include "game/cTimeManager.h"
    13	#include "gameobjects/players/cPlayer.h"
    14	#include "include/cAssert.h"
    15	#include "include/definitions.h"
    16	#include "include/sGameServices.h"
    17	#include "context/TextContext.hpp"
    18	#include "include/eGameState.h"
    19	
    20	#include <format>
    21	
    22	cScoringState::cScoringState(sGameServices* services) :
    23	    cGameState(services),
    24	    m_settings(services->settings),
    25	    m_missionFlow(services->missionFlow),
    26	    m_stateTransitions(services->stateTransitions),
    27	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    28	    m_smallTextDrawer(m_ctx->getTextContext()->getSmallTextDrawer()),
    29	    m_mouse(services->mouse),
    30	    m_screenFader(services->screenFader)
    31	{
    32	    d2tm_assert(m_settings != nullptr);
    33	    d2tm_assert(m_missionFlow != nullptr);
    34	    d2tm_assert(m_stateTransitions != nullptr);
    35	    d2tm_assert(m_textDrawer != nullptr);
    36	    d2tm_assert(m_smallTextDrawer != nullptr);
    37	    d2tm_assert(m_screenFader != nullptr);
    38	
    39	    m_stats = services->missionStatsCollector->snapshot(m_ctx->getTimeManager()->getElapsedSeconds());
    40	}
    41	
    42	void cScoringState::continueToWinBrief() const
    43	{
    44	    m_missionFlow->goingToWinLoseBrief(GAME_WINBRIEF);
    45	    m_stateTransitions->fadeOut();
    46	}
    47	
    48	cScoringState::~cScoringState()
    49	{
    50	}
    51	
    52	void cScoringState::thinkFast()
    53	{
    54	}
    55	
    56	void cScoringState::draw() const
    57	{
    58	    m_sdlDrawer->renderClearToColor();
    59	
    60	    int lineHeight = m_textDrawer->getFontHeight() + 4;
    61	    int statLineHeight = m_smallTextDrawer->getFontHeight() + 2;
    62	    int y = 40;
    63	
    64	    m_textDrawer->drawTextCentered("MISSION REPORT", y, Color::Yellow);
    65	    y += lineHeight * 2;
    66	
    67	    uint64_t minutes = m_stats.elapsedSeconds / 60;
    68	    uint64_t seconds = m_stats.elapsedSeconds % 60;
    69	    m_textDrawer->drawTextCentered(std::format("Mission time: {:02}:{:02}", minutes, seconds), y, Color::White);
    70	    y += lineHeight * 2;
    71	
    72	    // AI_CPU5 (Fremen superweapon trigger) and AI_WORM are not real opponents, never shown here.
    73	    for (int playerId = HUMAN; playerId < AI_WORM - 1; playerId++) {
    74	        const PlayerMissionStats &playerStats = m_stats.players[playerId];
    75	        // Read from the mission-start snapshot, not the live player: cGamePlaying resets a
    76	        // defeated player's house to GENERALHOUSE as elimination cleanup, which would otherwise
    77	        // hide anyone the player actually beat during the mission.
    78	        bool isPlaying = playerId == HUMAN || playerStats.house != GENERALHOUSE;
    79	        if (!isPlaying) {
    80	            continue;
    81	        }
    82	
    83	        std::string label = playerId == HUMAN ? "YOU" : "ENEMY";
    84	        std::string playerName = std::format("{} - {}", label, cPlayer::getHouseNameForId(playerStats.house));
    85	        Color nameColor = m_screenFader->getColorFadeSelected(playerStats.minimapColor.r, playerStats.minimapColor.g, playerStats.minimapColor.b);
    86	
    87	        m_textDrawer->drawTextCentered(playerName, y, nameColor);
    88	        y += lineHeight;
    89	        m_smallTextDrawer->drawTextCentered(
    90	            std::format("Units built: {}   lost: {}   destroyed: {}",
    91	                playerStats.unitsBuilt, playerStats.unitsLost, playerStats.unitsDestroyed),
    92	            y, Color::White);
    93	        y += statLineHeight;
    94	        m_smallTextDrawer->drawTextCentered(
    95	            std::format("Structures built: {}   lost: {}   destroyed: {}",
    96	                playerStats.structuresBuilt, playerStats.structuresLost, playerStats.structuresDestroyed),
    97	            y, Color::White);
    98	        y += statLineHeight;
    99	        m_smallTextDrawer->drawTextCentered(
   100	            std::format("Damage dealt: {}   received: {}", playerStats.damageDealt, playerStats.damageReceived),
   101	            y, Color::White);
   102	        y += statLineHeight;
   103	        m_smallTextDrawer->drawTextCentered(
   104	            std::format("Spice harvested: {}", playerStats.spiceHarvested),
   105	            y, Color::White);
   106	        y += lineHeight * 2;
   107	    }
   108	
   109	    m_textDrawer->drawTextCentered("Click to continue", m_settings->getScreenH() - lineHeight - 8, Color::White);
   110	    m_mouse->draw();
   111	}
   112	
   113	void cScoringState::onNotifyMouseEvent(const s_MouseEvent &event)
   114	{
   115	    // Any left click continues, matching the WINNING screen's click-anywhere behavior the
   116	    // player just came from.
   117	    if (event.eventType == MOUSE_LEFT_BUTTON_CLICKED) {
   118	        continueToWinBrief();
   119	    }
   120	}
   121	
   122	void cScoringState::onNotifyKeyboardEvent(const cKeyboardEvent &)
   123	{
   124	}
   125	
   126	eGameStateType cScoringState::getType()
   127	{
   128	    return GAMESTATE_SCORING;
   129	}
```

### src/gamestates/cEditorState.cpp@c583461:1-410

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cEditorState.cpp | nl -ba | sed -n '1,410p'
     1	/**
     2	 * @file cEditorState.cpp
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
    16	#include "gamestates/cEditorState.h"
    17	#include "gamestates/cEditorState/cEditorCam.h"
    18	#include "gamestates/cEditorState/cEditorUndoRedoHistory.h"
    19	#include "controls/eKeyAction.h"
    20	#include "gui/GuiBar.h"
    21	#include "gui/GuiStateButton.h"
    22	#include "gui/GuiButton.h"
    23	#include "gui/GuiButtonGroup.h"
    24	#include "gui/GuiValueButton.h"
    25	#include "data/gfxdata.h"
    26	#include "drawers/SDLDrawer.hpp"
    27	#include "drawers/cTextDrawer.h"
    28	#include "utils/Graphics.hpp"
    29	#include "context/GameContext.hpp"
    30	#include "context/cGameObjectContext.h"
    31	#include "game/cEventEmitter.h"
    32	#include "game/GameStateTransition.hpp"
    33	#include "controls/cMouse.h"
    34	#include "gameobjects/map/cPreviewMaps.h"
    35	#include "include/gfxeditor.h"
    36	#include "include/sGameEvent.h"
    37	
    38	#include "include/cAssert.h"
    39	#include "context/GraphicsContext.hpp"
    40	#include "context/TextContext.hpp"
    41	#include "game/cGameSettings.h"
    42	#include "gamestates/cGameState.h"
    43	#include "include/sGameServices.h"
    44	#include "include/eGameState.h"
    45	#include <memory>
    46	
    47	const int heightBarSize = 48;
    48	const int heightButtonSize = 40;
    49	const int maxPenSize = 11; // must be odd to have a center
    50	const Color editorGridColor = Color{128, 128, 128, 180};
    51	const Color editorCenterLineColor = Color{32, 176, 32, 220};
    52	const Color editorHoveredCellFillColor = Color{255, 230, 64, 96};
    53	const Color editorHoveredCellBorderColor = Color{255, 230, 64, 220};
    54	const Color editorSelectionFillColor = Color{255, 255, 255, 40};
    55	const Color editorSelectionBorderColor = Color{255, 255, 255, 255};
    56	const Color editorPasteGhostFillColor = Color{64, 208, 255, 60};
    57	const Color editorPasteGhostBorderColor = Color{64, 208, 255, 220};
    58	
    59	
    60	cEditorState::cEditorState(sGameServices* services) 
    61	    : cGameState(services),
    62	    m_gfxdata(m_ctx->getGraphicsContext()->gfxdata.get()),
    63	    m_gfxeditor(m_ctx->getGraphicsContext()->gfxeditor.get()),
    64	    m_settings(services->settings),
    65	    m_eventEmitter(services->eventEmitter),
    66	    m_stateTransitions(services->stateTransitions),
    67	    m_mouse(services->mouse),
    68	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    69	    m_previewMaps(services->objects->getPreviewMaps())
    70	{
    71	    d2tm_assert(m_gfxdata != nullptr);
    72	    d2tm_assert(m_gfxeditor != nullptr);
    73	    d2tm_assert(m_settings != nullptr);
    74	    d2tm_assert(m_eventEmitter != nullptr);
    75	    d2tm_assert(m_stateTransitions != nullptr);
    76	    d2tm_assert(m_mouse != nullptr);
    77	    d2tm_assert(m_textDrawer != nullptr);
    78	
    79	    m_undoRedo = std::make_unique<cEditorUndoRedoHistory>();
    80	
    81	    const cRectangle &selectRect = cRectangle(0, 0, m_settings->getScreenW(), heightBarSize);
    82	    const cRectangle &modifRect = cRectangle(m_settings->getScreenW()-heightBarSize, heightBarSize, heightBarSize, m_settings->getScreenH()-heightBarSize);
    83	    mapSizeArea = cRectangle(0,heightBarSize,m_settings->getScreenW()-heightBarSize,m_settings->getScreenH()-heightBarSize);
    84	    m_editorCam = std::make_unique<cEditorCam>(mapSizeArea);
    85	    m_selectBar = std::make_unique<GuiBar>(m_sdlDrawer, selectRect,GuiBarPlacement::HORIZONTAL,heightButtonSize);
    86	    m_topologyBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    87	    m_startCellBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    88	    m_symmetricBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    89	
    90	    m_selectBar->setTheme(cGuiThemeBuilder().light().build());
    91	    m_selectBar->beginPlacement(heightBarSize);
    92	    m_topologyBar->setTheme(cGuiThemeBuilder().light().build());
    93	    m_topologyBar->beginPlacement(heightBarSize);
    94	    m_startCellBar->setTheme(cGuiThemeBuilder().light().build());
    95	    m_startCellBar->beginPlacement(heightBarSize);
    96	    m_symmetricBar->setTheme(cGuiThemeBuilder().light().build());
    97	    m_symmetricBar->beginPlacement(heightBarSize);
    98	
    99	    populateSelectBar();
   100	    populateTopologyBar();
   101	    populateStartCellBar();
   102	    populateSymmetricBar();
   103	    setCurrentBar(m_topologyBar.get());
   104	    startCells.fill({-1, -1});
   105	}
   106	
   107	cEditorState::~cEditorState()
   108	{
   109	}
   110	
   111	void cEditorState::populateSelectBar()
   112	{
   113	    m_selectGroup = std::make_unique<GuiButtonGroup>();
   114	    auto rectGui = cRectangle(0, 0, heightButtonSize, heightButtonSize);
   115	    auto guiButton = GuiStateButtonBuilder()
   116	            .withRect(rectGui)
   117	            .withTexture(m_gfxeditor->getTexture(STONELAYER))
   118	            .withRenderer(m_sdlDrawer)
   119	            .onClick([this]() {
   120	                setCurrentBar(m_topologyBar.get());
   121	            })
   122	            .build();
   123	    guiButton->setGroup(m_selectGroup.get());
   124	    m_selectGroup->updateStates(guiButton.get());
   125	    m_selectBar->addAutoGuiObject(std::move(guiButton));
   126	
   127	    guiButton = GuiStateButtonBuilder()
   128	            .withRect(rectGui)
   129	            .withTexture(m_gfxeditor->getTexture(STARTPOSITION))
   130	            .withRenderer(m_sdlDrawer)
   131	            .onClick([this]() {
   132	                setCurrentBar(m_startCellBar.get());
   133	            })
   134	            .build();
   135	    guiButton->setGroup(m_selectGroup.get());
   136	    m_selectBar->addAutoGuiObject(std::move(guiButton));
   137	
   138	    guiButton = GuiStateButtonBuilder()
   139	            .withRect(rectGui)
   140	            .withTexture(m_gfxeditor->getTexture(FLIPHORZ))
   141	            .withRenderer(m_sdlDrawer)
   142	            .onClick([this]() {
   143	                setCurrentBar(m_symmetricBar.get());
   144	            })
   145	            .build();
   146	    guiButton->setGroup(m_selectGroup.get());
   147	    m_selectBar->addAutoGuiObject(std::move(guiButton));
   148	
   149	    rectGui = cRectangle(m_settings->getScreenW()-heightButtonSize*3, (heightBarSize-heightButtonSize)/2, heightButtonSize, heightButtonSize);
   150	    // std::cout << "Save icon position: x=" << rectGui.getX() << " y=" << rectGui.getY() << " w= " << rectGui.getWidth() << " h= " << rectGui.getHeight() << std::endl;
   151	    auto guiIcon = GuiButtonBuilder()
   152	            .withRect(rectGui)
   153	            .withTexture(m_gfxeditor->getTexture(SAVEICON))
   154	            .withRenderer(m_sdlDrawer)
   155	            .withKind(GuiRenderKind::WITH_STRETCHED_TEXTURE)
   156	            .onClick([this]() {
   157	                if (saveMap()) {
   158	                    m_hasChanged = false;
   159	                }
   160	            })
   161	            .build();
   162	    m_selectBar->addGuiObject(std::move(guiIcon));
   163	}
   164	
   165	void cEditorState::populateTopologyBar()
   166	{
   167	    m_topologyGroup = std::make_unique<GuiButtonGroup>();
   168	    auto rectGui = cRectangle(0,0,heightButtonSize,heightButtonSize);
   169	    auto guiButton = GuiStateButtonBuilder()
   170	            .withRect(rectGui)
   171	            .withTexture(m_gfxeditor->getTexture(TERRAN_HILL))
   172	            .withRenderer(m_sdlDrawer)
   173	            .onClick([this]() {
   174	                idTerrainToMapModif = TERRAIN_HILL;
   175	            })
   176	            .build();
   177	    guiButton->setGroup(m_topologyGroup.get());
   178	    m_topologyBar->addAutoGuiObject(std::move(guiButton));
   179	
   180	    guiButton = GuiStateButtonBuilder()
   181	            .withRect(rectGui)
   182	            .withTexture(m_gfxeditor->getTexture(TERRAN_MOUNTAIN))
   183	            .withRenderer(m_sdlDrawer)
   184	            .onClick([this]() {
   185	                idTerrainToMapModif = TERRAIN_MOUNTAIN;
   186	            })
   187	            .build();
   188	    guiButton->setGroup(m_topologyGroup.get());
   189	    m_topologyBar->addAutoGuiObject(std::move(guiButton));
   190	
   191	    guiButton = GuiStateButtonBuilder()
   192	            .withRect(rectGui)
   193	            .withTexture(m_gfxeditor->getTexture(TERRAN_ROCK))
   194	            .withRenderer(m_sdlDrawer)
   195	            .onClick([this]() {
   196	                idTerrainToMapModif = TERRAIN_ROCK;
   197	            })
   198	            .build();
   199	    guiButton->setGroup(m_topologyGroup.get());
   200	    m_topologyBar->addAutoGuiObject(std::move(guiButton));
   201	
   202	    guiButton = GuiStateButtonBuilder()
   203	            .withRect(rectGui)
   204	            .withTexture(m_gfxeditor->getTexture(TERRAN_SAND))
   205	            .withRenderer(m_sdlDrawer)
   206	            .onClick([this]() {
   207	                idTerrainToMapModif = TERRAIN_SAND;
   208	            })
   209	            .build();
   210	    guiButton->setGroup(m_topologyGroup.get());
   211	    m_topologyGroup->updateStates(guiButton.get());
   212	    m_topologyBar->addAutoGuiObject(std::move(guiButton));
   213	
   214	    guiButton = GuiStateButtonBuilder()
   215	            .withRect(rectGui)
   216	            .withTexture(m_gfxeditor->getTexture(TERRAN_SPICE))
   217	            .withRenderer(m_sdlDrawer)
   218	            .onClick([this]() {
   219	                idTerrainToMapModif = TERRAIN_SPICE;
   220	            })
   221	            .build();
   222	    guiButton->setGroup(m_topologyGroup.get());
   223	    m_topologyBar->addAutoGuiObject(std::move(guiButton));
   224	
   225	    guiButton = GuiStateButtonBuilder()
   226	            .withRect(rectGui)
   227	            .withTexture(m_gfxeditor->getTexture(TERRAN_SPICEHILL))
   228	            .withRenderer(m_sdlDrawer)
   229	            .onClick([this]() {
   230	                idTerrainToMapModif = TERRAIN_SPICEHILL;
   231	            })
   232	            .build();
   233	    guiButton->setGroup(m_topologyGroup.get());
   234	    m_topologyBar->addAutoGuiObject(std::move(guiButton));
   235	
   236	    auto cursorSizeButton = GuiValueButtonBuilder()
   237	            .withRect(cRectangle(0, 0, heightButtonSize, heightButtonSize))
   238	            .withRenderer(m_sdlDrawer)
   239	            .withTextDrawer(m_textDrawer)
   240	            .withTheme(cGuiThemeBuilder().light().build())
   241	            .withLabel("size")
   242	            .withInitialValue(m_topologyCursorSize)
   243	            .withStepValue(2)
   244	            .withMinValue(1)
   245	            .withMaxValue(maxPenSize)
   246	            .onChanged([this](int value) {
   247	                setCursorSize(value);
   248	            })
   249	            .build();
   250	    m_topologyBar->addAutoGuiObject(std::move(cursorSizeButton));
   251	}
   252	
   253	void cEditorState::populateStartCellBar()
   254	{
   255	    m_startCellGroup = std::make_unique<GuiButtonGroup>();
   256	    auto rectGui = cRectangle(0, 0, heightButtonSize, heightButtonSize);
   257	    auto guiButton = GuiStateButtonBuilder()
   258	            .withRect(rectGui)
   259	            .withTexture(m_gfxeditor->getTexture(STARTPOSITION1))
   260	            .withRenderer(m_sdlDrawer)
   261	            .onClick([this]() {
   262	                idStartCellPlayer = 0;
   263	            })
   264	            .build();
   265	    guiButton->setGroup(m_startCellGroup.get());
   266	    m_startCellGroup->updateStates(guiButton.get());
   267	    m_startCellBar->addAutoGuiObject(std::move(guiButton));
   268	
   269	    guiButton = GuiStateButtonBuilder()
   270	            .withRect(rectGui)
   271	            .withTexture(m_gfxeditor->getTexture(STARTPOSITION2))
   272	            .withRenderer(m_sdlDrawer)
   273	            .onClick([this]() {
   274	                idStartCellPlayer = 1;
   275	            })
   276	            .build();
   277	    guiButton->setGroup(m_startCellGroup.get());
   278	    m_startCellBar->addAutoGuiObject(std::move(guiButton));
   279	
   280	    guiButton = GuiStateButtonBuilder()
   281	            .withRect(rectGui)
   282	            .withTexture(m_gfxeditor->getTexture(STARTPOSITION3))
   283	            .withRenderer(m_sdlDrawer)
   284	            .onClick([this]() {
   285	                idStartCellPlayer = 2;
   286	            })
   287	            .build();
   288	    guiButton->setGroup(m_startCellGroup.get());
   289	    m_startCellBar->addAutoGuiObject(std::move(guiButton));
   290	
   291	    guiButton = GuiStateButtonBuilder()
   292	            .withRect(rectGui)
   293	            .withTexture(m_gfxeditor->getTexture(STARTPOSITION4))
   294	            .withRenderer(m_sdlDrawer)
   295	            .onClick([this]() {
   296	                idStartCellPlayer = 3;
   297	            })
   298	            .build();
   299	    guiButton->setGroup(m_startCellGroup.get());
   300	    m_startCellBar->addAutoGuiObject(std::move(guiButton));
   301	
   302	    guiButton = GuiStateButtonBuilder()
   303	            .withRect(rectGui)
   304	            .withTexture(m_gfxeditor->getTexture(STARTPOSITION5))
   305	            .withRenderer(m_sdlDrawer)
   306	            .onClick([this]() {
   307	                idStartCellPlayer = 4;
   308	            })
   309	            .build();
   310	    guiButton->setGroup(m_startCellGroup.get());
   311	    m_startCellBar->addAutoGuiObject(std::move(guiButton));
   312	}
   313	
   314	void cEditorState::populateSymmetricBar()
   315	{
   316	    m_symmetricGroup = std::make_unique<GuiButtonGroup>();
   317	    auto rectGui = cRectangle(0, 0, heightButtonSize,heightButtonSize);
   318	    auto guiButton = GuiStateButtonBuilder()
   319	            .withRect(rectGui)
   320	            .withTexture(m_gfxeditor->getTexture(FLIPHORZLR))
   321	            .withRenderer(m_sdlDrawer)
   322	            .onClick([this]() {
   323	                // std::cout << "FLIPHORZLR" << std::endl;
   324	                modifySymmetricArea(Direction::right);
   325	            })
   326	            .build();
   327	    guiButton->setGroup(m_symmetricGroup.get());
   328	    m_symmetricBar->addAutoGuiObject(std::move(guiButton));
   329	
   330	    guiButton = GuiStateButtonBuilder()
   331	            .withRect(rectGui)
   332	            .withTexture(m_gfxeditor->getTexture(FLIPHORZRL))
   333	            .withRenderer(m_sdlDrawer)
   334	            .onClick([this]() {
   335	                // std::cout << "FLIPHORZRL" << std::endl;
   336	                modifySymmetricArea(Direction::left);
   337	            })
   338	            .build();
   339	    guiButton->setGroup(m_symmetricGroup.get());
   340	    m_symmetricBar->addAutoGuiObject(std::move(guiButton));
   341	
   342	    guiButton = GuiStateButtonBuilder()
   343	            .withRect(rectGui)
   344	            .withTexture(m_gfxeditor->getTexture(FLIPVERTBT))
   345	            .withRenderer(m_sdlDrawer)
   346	            .onClick([this]() {
   347	                // std::cout << "FLIPVERTBT" << std::endl;
   348	                modifySymmetricArea(Direction::top);
   349	            })
   350	            .build();
   351	    guiButton->setGroup(m_symmetricGroup.get());
   352	    m_symmetricBar->addAutoGuiObject(std::move(guiButton));
   353	
   354	    guiButton = GuiStateButtonBuilder()
   355	            .withRect(rectGui)
   356	            .withTexture(m_gfxeditor->getTexture(FLIPVERTTB))
   357	            .withRenderer(m_sdlDrawer)
   358	            .onClick([this]() {
   359	                // std::cout << "FLIPVERTTB" << std::endl;
   360	                modifySymmetricArea(Direction::bottom);
   361	            })
   362	            .build();
   363	    guiButton->setGroup(m_symmetricGroup.get());
   364	    m_symmetricBar->addAutoGuiObject(std::move(guiButton));
   365	
   366	    guiButton = GuiStateButtonBuilder()
   367	            .withRect(rectGui)
   368	            .withTexture(m_gfxeditor->getTexture(FLIPDIAGBL))
   369	            .withRenderer(m_sdlDrawer)
   370	            .onClick([this]() {
   371	                modifySymmetricArea(Direction::bottomLeft);
   372	            })
   373	            .build();
   374	    guiButton->setGroup(m_symmetricGroup.get());
   375	    m_symmetricBar->addAutoGuiObject(std::move(guiButton));
   376	
   377	    guiButton = GuiStateButtonBuilder()
   378	            .withRect(rectGui)
   379	            .withTexture(m_gfxeditor->getTexture(FLIPDIAGBR))
   380	            .withRenderer(m_sdlDrawer)
   381	            .onClick([this]() {
   382	                modifySymmetricArea(Direction::bottomRight);
   383	            })
   384	            .build();
   385	    guiButton->setGroup(m_symmetricGroup.get());
   386	    m_symmetricBar->addAutoGuiObject(std::move(guiButton));
   387	
   388	    guiButton = GuiStateButtonBuilder()
   389	            .withRect(rectGui)
   390	            .withTexture(m_gfxeditor->getTexture(FLIPDIAGTL))
   391	            .withRenderer(m_sdlDrawer)
   392	            .onClick([this]() {
   393	                modifySymmetricArea(Direction::topLeft);
   394	            })
   395	            .build();
   396	    guiButton->setGroup(m_symmetricGroup.get());
   397	    m_symmetricBar->addAutoGuiObject(std::move(guiButton)); 
   398	
   399	    guiButton = GuiStateButtonBuilder()
   400	            .withRect(rectGui)
   401	            .withTexture(m_gfxeditor->getTexture(FLIPDIAGTR))
   402	            .withRenderer(m_sdlDrawer)
   403	            .onClick([this]() {
   404	                modifySymmetricArea(Direction::topRight);
   405	            })
   406	            .build();
   407	    guiButton->setGroup(m_symmetricGroup.get());
   408	    m_symmetricBar->addAutoGuiObject(std::move(guiButton)); 
   409	}
   410	
```

### src/gamestates/cEditorState.cpp@c583461:605-735

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cEditorState.cpp | nl -ba | sed -n '605,735p'
   605	void cEditorState::loadMap(int mapIndex)
   606	{
   607	    s_PreviewMap* map = m_previewMaps->getMap(mapIndex);
   608	    //std::cout << "open |"<< map->name << "|" << std::endl;
   609	    m_mapData = std::make_unique<Matrix<int>>(map->terrainType, map->height, map->width);
   610	    m_mapAuthor = map->author;
   611	    m_mapDescription = map->description;
   612	    m_mapName = map->name;
   613	    startCells.fill({-1, -1});
   614	    for (int i=0; i<MAX_SKIRMISHMAP_PLAYERS; i++) {
   615	        if (map->iStartCell[i] !=-1) {
   616	            //std::cout << "startCell " << map->iStartCell[i] << std::endl;
   617	            int w = map->iStartCell[i] % map->width;
   618	            int h = map->iStartCell[i] / map->width;
   619	            startCells[i] = cPoint(w,h);
   620	        }
   621	    }
   622	    m_editorCam->reset();
   623	    m_editorCam->updateVisibleTiles(*m_mapData);
   624	    normalizeModifications();
   625	    m_displayGrid = false;
   626	    m_displayAxes = false;
   627	    m_displayPastPreview = false;
   628	    m_hasChanged = false;
   629	    m_hasSelection = false;
   630	    m_isDraggingSelection = false;
   631	    m_undoRedo->clear();
   632	}
   633	
   634	void cEditorState::setCursorSize(int value)
   635	{
   636	    int normalizedValue = std::max(1, value);
   637	    if (normalizedValue % 2 == 0) {
   638	        normalizedValue += 1;
   639	    }
   640	
   641	    normalizedValue = std::min(normalizedValue, maxPenSize);
   642	    if (normalizedValue % 2 == 0) {
   643	        normalizedValue -= 1;
   644	    }
   645	
   646	    m_topologyCursorSize = normalizedValue;
   647	    m_cursorSize = getActiveCursorSize();
   648	}
   649	
   650	void cEditorState::setCurrentBar(GuiBar* bar)
   651	{
   652	    m_currentBar = bar;
   653	    m_cursorSize = getActiveCursorSize();
   654	}
   655	
   656	int cEditorState::getActiveCursorSize() const
   657	{
   658	    if (m_currentBar == m_topologyBar.get()) {
   659	        return m_topologyCursorSize;
   660	    }
   661	
   662	    return 1;
   663	}
   664	
   665	void cEditorState::normalizeModifications()
   666	{
   667	    for (size_t j = 0; j < m_mapData->getRows(); j++) {
   668	        (*m_mapData)[j][0] = -1;
   669	        (*m_mapData)[j][m_mapData->getCols()-1] = -1;
   670	    }
   671	    for (size_t i = 0; i < m_mapData->getCols(); i++) {
   672	        (*m_mapData)[0][i] = -1;
   673	        (*m_mapData)[m_mapData->getRows()-1][i] = -1;
   674	    }
   675	}
   676	
   677	void cEditorState::drawMap() const
   678	{
   679	    if (m_mapData == nullptr) {
   680	        return;
   681	    }
   682	
   683	    const int cameraX = m_editorCam->getCameraX();
   684	    const int cameraY = m_editorCam->getCameraY();
   685	    const int tileLenSize = m_editorCam->getTileSize();
   686	    const int startX = m_editorCam->getStartX();
   687	    const int startY = m_editorCam->getStartY();
   688	    const size_t endX = m_editorCam->getEndX();
   689	    const size_t endY = m_editorCam->getEndY();
   690	    
   691	    int tileID;
   692	    int tile_world_x, tile_world_y;
   693	    int tile_screen_x, tile_screen_y;
   694	
   695	    cRectangle destRect;
   696	    cRectangle srcRect{0,0,32,32}; // we take the first full textured sprite
   697	    for (size_t j = static_cast<size_t>(startY); j < endY; j++) {
   698	        for (size_t i = static_cast<size_t>(startX); i < endX; i++) {
   699	            // Ideal position in pixels if the map started at (0,0)
   700	            tile_world_x = i * tileLenSize;
   701	            tile_world_y = j * tileLenSize;
   702	            // Rendering position on the screen (including camera offset)
   703	            tile_screen_x = tile_world_x - cameraX;
   704	            tile_screen_y = tile_world_y - cameraY;
   705	            
   706	            destRect= cRectangle(tile_screen_x, heightBarSize+tile_screen_y,tileLenSize,tileLenSize);
   707	           
   708	            tileID = (*m_mapData)[j][i];
   709	            switch (tileID)
   710	            {
   711	            case TERRAIN_SPICE:
   712	                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_SPICE), srcRect, destRect);
   713	                break;
   714	            case TERRAIN_SAND:
   715	                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_SAND), srcRect, destRect);
   716	                break;
   717	            case TERRAIN_MOUNTAIN:
   718	                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_MOUNTAIN), srcRect, destRect);
   719	                break;
   720	            case TERRAIN_ROCK:
   721	                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_ROCK), srcRect, destRect);
   722	                break;
   723	            case TERRAIN_SPICEHILL:
   724	                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_SPICEHILL), srcRect, destRect);
   725	                break;  
   726	            case TERRAIN_HILL:
   727	                m_sdlDrawer->renderStrechSprite(m_gfxdata->getTexture(TERRAIN_HILL), srcRect, destRect);
   728	                break;            
   729	            default:
   730	                break;
   731	            }
   732	        }
   733	    }
   734	}
   735	
```

