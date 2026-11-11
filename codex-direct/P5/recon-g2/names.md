# Места имён

### HUMAN

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'HUMAN' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cMapDrawer.cpp:362:    if (playerId < HUMAN || playerId >= MAX_PLAYERS) return -1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cMouseDrawer.cpp:229:    if (theWindTrap->getOwner() == HUMAN) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cMouseDrawer.cpp:253:    if (theStructure->getOwner() == HUMAN) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cStructureDrawer.cpp:88:    if (!m_settings->isFogOfWarEnabled() || iPl != HUMAN) return;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cStructureDrawer.cpp:129:    cGameControlsContext *context = m_objects->getPlayer(HUMAN)->getGameControlsContext();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cStructureDrawer.cpp:456:        if (m_player->getId() == HUMAN && m_objects->getMap()->isHiddenByFogOfWar(theStructure)) continue;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.cpp:105:    if (m_unit.iPlayer == HUMAN) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:55:    cPlayer *humanPlayer = m_objects->getPlayer(HUMAN);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:98:        cPlayer *humanPlayer = m_objects->getPlayer(HUMAN);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:125:    cPlayer *humanPlayer = m_objects->getPlayer(HUMAN);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:127:        if (i == HUMAN || i == AI_WORM || i == AI_CPU5) continue; // do not evaluate these players
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:485:    m_audioContext->playVoice(SOUND_VOICE_07_ATR, m_gameObjectsContext->getPlayer(HUMAN)->getHouse());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:508:    m_audioContext->playVoice(SOUND_VOICE_08_ATR, m_gameObjectsContext->getPlayer(HUMAN)->getHouse());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:873:    cPlayer *humanPlayer = m_gameObjectsContext->getPlayer(HUMAN);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:931:    cPlayer *humanPlayer = m_gameObjectsContext->getPlayer(HUMAN);
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'HUMAN' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
80
```

### m_region

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_region' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_region' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### m_mission

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_mission' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_mission' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### GAME_REGION

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'GAME_REGION' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:963:            case GAME_REGION: mapped = eGameState::REGION; return true;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:988:        bool deleteOldState = (newState != GAME_REGION &&
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1006:        if (newState == GAME_REGION) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1058:            if (newState == GAME_REGION) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1063:                    // because `GAME_REGION` == if (existingStatePtr->getType() == GAMESTATE_SELECT_YOUR_NEXT_CONQUEST ||
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1122:            if (newState == GAME_REGION) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1349:        setNextStateToTransitionTo(GAME_REGION);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1360:            setNextStateToTransitionTo(GAME_REGION);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGameState.h:41:    GAMESTATE_SELECT_YOUR_NEXT_CONQUEST,    // #define GAME_REGION		  6	    // select a region / select your next conquest
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectMissionState.cpp:124:                highestUnlockedMission == CampaignProgress::FIRST_MISSION ? GAME_BRIEFING : GAME_REGION);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectMissionState.cpp:143:                m_stateTransitions->setNextStateWithFade(i == CampaignProgress::FIRST_MISSION ? GAME_BRIEFING : GAME_REGION);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/eGameState.cpp:40:        case GAME_REGION:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/eGameState.cpp:41:            return "GAME_REGION";
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/eGameState.h:54:inline constexpr int GAME_REGION = 6;		 // select a region / select your next conquest
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'GAME_REGION' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
14
```

### createAndPrepareMentatForHumanPlayer

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'createAndPrepareMentatForHumanPlayer' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'createAndPrepareMentatForHumanPlayer' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### prepareMentatToTellAboutHouse

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'prepareMentatToTellAboutHouse' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:164:    void prepareMentatToTellAboutHouse(int house);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:226:            prepareMentatToTellAboutHouse(house);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1257:void cGame::prepareMentatToTellAboutHouse(int house)
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'prepareMentatToTellAboutHouse' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
3
```

### m_mentat

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_mentat' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:84:                m_mentat = std::make_unique<AtreidesMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:86:                m_mentat = std::make_unique<HarkonnenMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:88:                m_mentat = std::make_unique<OrdosMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:90:                m_mentat = std::make_unique<SardaukarMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:92:                m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, humanPlayer, m_dataCampaign);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:95:            m_cIni->loadScenario(m_mentat.get(), m_reinforcements,m_dataCampaign);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:96:            m_cIni->loadBriefing(house, m_dataCampaign->region, eScenarioIniSection::BRIEFING, m_mentat.get());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:100:                m_mentat = std::make_unique<AtreidesMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:102:                m_mentat = std::make_unique<HarkonnenMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:104:                m_mentat = std::make_unique<OrdosMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:106:                m_mentat = std::make_unique<SardaukarMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:108:                m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, humanPlayer, m_dataCampaign);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:111:                m_mentat->loadScene("win01");
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:113:                m_mentat->loadScene("win02");
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:114:            m_cIni->loadBriefing(house, m_dataCampaign->region, eScenarioIniSection::WIN, m_mentat.get());
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_mentat' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
48
```

### iMentatSentence

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'iMentatSentence' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:55:    iMentatSentence = -1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:134:            iMentatSentence += 2; // makes 0, 2, etc.
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:137:            if (iMentatSentence > 8) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:143:            int iLength = static_cast<int>(sentence[iMentatSentence].size());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:144:            iLength += static_cast<int>(sentence[iMentatSentence + 1].size());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:293:        if (iMentatSentence >= 0) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:294:            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{0, 0, 0,255},sentence[iMentatSentence]);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:295:            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{255, 255, 255,255},sentence[iMentatSentence]);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:297:            m_textDrawer->drawText(offsetX + 17, offsetY + 37,Color{0, 0, 0,255},sentence[iMentatSentence+1]);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:298:            m_textDrawer->drawText(offsetX + 17, offsetY + 36,Color{255, 255, 255,255},sentence[iMentatSentence+1]);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:370:    iMentatSentence = -2; // ugh
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.h:96:    int iMentatSentence;  // = sentence to draw and speak with (-1 = not ready)
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'iMentatSentence' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
12
```

### TIMER_Speaking

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'TIMER_Speaking' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:57:    TIMER_Speaking = -1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:129:        if (TIMER_Speaking > 0) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:130:            TIMER_Speaking--;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:132:        else if (TIMER_Speaking == 0) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:152:            TIMER_Speaking = iLength * 12;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:225:        if (TIMER_Speaking > 0) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:368:    TIMER_Speaking = 0;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:412:            if (TIMER_Speaking > 0) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:413:                TIMER_Speaking = 1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.h:85:    int TIMER_Speaking;
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'TIMER_Speaking' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
10
```

### AWAITING_RESPONSE

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'AWAITING_RESPONSE' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:138:                state = AWAITING_RESPONSE;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:148:                state = AWAITING_RESPONSE;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:302:    if (state == AWAITING_RESPONSE) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:418:    if (state == AWAITING_RESPONSE) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.h:40:    AWAITING_RESPONSE,  // the mentat is done speaking, the user needs to click something (yes/no, proceed/repeat, etc)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/BeneMentat.cpp:94:    if (state == AWAITING_RESPONSE) {
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'AWAITING_RESPONSE' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
6
```

### SPEAKING

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'SPEAKING' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:128:    if (state == SPEAKING) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:291:    if (state == SPEAKING) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:371:    state = SPEAKING;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:407:    if (state == SPEAKING) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.h:39:    SPEAKING,           // the mentat is speaking about whatever
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'SPEAKING' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
5
```

### initSkirmish

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'initSkirmish' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'initSkirmish' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### loadSkirmishMaps

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'loadSkirmishMaps' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:130:    // void loadSkirmishMaps() const;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:528:// void cGame::loadSkirmishMaps() const
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:530://     m_gameObjectsContext->getPreviewMaps()->loadSkirmishMaps();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:823:    previewMaps->loadSkirmishMaps(); // load skirmish maps, so they are ready when we need them in the skirmish setup state
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cPreviewMaps.cpp:295:void cPreviewMaps::loadSkirmishMaps()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cPreviewMaps.h:49:    void loadSkirmishMaps();
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'loadSkirmishMaps' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
6
```

### iSkirmishMap

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'iSkirmishMap' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/ScenarioFlow.hpp:48:    void loadMapFromEditor(int iSkirmishMap) const {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/ScenarioFlow.hpp:49:        m_loadMapFromEditor(iSkirmishMap);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:268:        [this](int iSkirmishMap) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:269:            loadMapFromEditor(iSkirmishMap);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:138:    iSkirmishMap = -1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:349:                if (m_previewMaps->isValidMap(iSkirmishMap)) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:350:                    prepareSkirmishGameToPlayAndTransitionToCombatState(iSkirmishMap);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:396:                if (iSkirmishMap > -1) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:397:                    m_scenarioFlow->loadMapFromEditor(iSkirmishMap);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:518:    const bool selectedMap = iSkirmishMap > -1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:629:    if (iSkirmishMap == 0) { // random map selected
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:643:    if (iSkirmishMap > -1) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:644:        s_PreviewMap *selectedMap = m_previewMaps->getMap(iSkirmishMap);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:645:        PreviewMapView *selectedView = m_previewMaps->getView(iSkirmishMap);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:647:        if (iSkirmishMap > 0) {
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'iSkirmishMap' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
37
```

### startingPoints

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'startingPoints' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.cpp:33:void cRandomMapGenerator::generateRandomMap(int width, int height, int startingPoints, s_PreviewMap &randomMapEntry, cGameObjectContext* objects)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.cpp:39:    int a_spice = RNG::rnd((startingPoints * 8)) + (startingPoints * 12);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.cpp:40:    int a_rock = 32 + RNG::rnd(startingPoints * 3);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.cpp:60:    if (startingPoints == 2) iDistance = 32;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.cpp:61:    if (startingPoints == 3) iDistance = 26;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.cpp:62:    if (startingPoints == 4) iDistance = 22;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.cpp:93:            if (iSpot < startingPoints) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cRandomMapGenerator.h:24:    void generateRandomMap(int width, int height, int startingPoints, s_PreviewMap &randomMap, cGameObjectContext* objects);
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'startingPoints' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
8
```

### skirmishPlayer

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'skirmishPlayer' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:121:        s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[i];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:501:        const s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[p];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:857:        s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[p];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:876:                    int usedHouse = (skirmishPlayer[pl].iHouse > 0)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:877:                        ? skirmishPlayer[pl].iHouse
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:887:                        skirmishPlayer[0].iHouse, skirmishPlayer[1].iHouse,
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:888:                        skirmishPlayer[2].iHouse, skirmishPlayer[3].iHouse,
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:889:                        skirmishPlayer[4].iHouse);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:967:        s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[p];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:985:            s_SkirmishPlayer &pSkirmishPlayer = skirmishPlayer[p];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1015:        s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[p];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1130:            s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[p];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1203:            s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[p];
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1358:                    skirmishPlayer[p].bPlaying = false;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1405:        s_SkirmishPlayer &player = skirmishPlayer[p];
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'skirmishPlayer' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
18
```

### bPlaying

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'bPlaying' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:128:        sSkirmishPlayer.bPlaying = (i <= 1);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:579:        return sSkirmishPlayer.bPlaying ? colorSelectedRedFade : colorDisabledFade;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:586:    return sSkirmishPlayer.bPlaying ? Color::White : colorDisabled;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:865:            if (!sSkirmishPlayer.bPlaying) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:987:            if (!pSkirmishPlayer.bPlaying) continue; // skip non playing players
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1131:            if (!sSkirmishPlayer.bPlaying) continue;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1211:                    if (sSkirmishPlayer.bPlaying) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1212:                        sSkirmishPlayer.bPlaying = false;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1215:                        sSkirmishPlayer.bPlaying = true;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1220:            if (!sSkirmishPlayer.bPlaying) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1358:                    skirmishPlayer[p].bPlaying = false;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1406:        player.bPlaying = (p < iStartingPoints);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1410:    skirmishPlayer[HUMAN].bPlaying = true;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1607:        skirmishPlayer[p].bPlaying = false;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.h:52:    bool bPlaying;
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'bPlaying' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
15
```

### m_crawlerY

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_crawlerY' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:412:    m_crawlerY = m_settings->getScreenH() + 1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:429:    m_crawlerY -= m_moveSpeed;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:431:    int textCrawlY = m_crawlerY + m_titleHeight;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:448:    m_sdlDrawer->renderSprite(m_titleBmp, m_titleX, m_crawlerY);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:449:    int textCrawlY = m_crawlerY + m_titleHeight;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.h:63:    float m_crawlerY;
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_crawlerY' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
6
```

### m_moveSpeed

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_moveSpeed' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:45:    m_moveSpeed(0.15f)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:429:    m_crawlerY -= m_moveSpeed;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:476:        m_moveSpeed = 1.0f; // speed up
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:479:        m_moveSpeed = 0.15f; // restore
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.h:65:    float m_moveSpeed;
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_moveSpeed' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
5
```

### m_titleHeight

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_titleHeight' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:74:    m_titleHeight = m_titleBmp->h;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:431:    int textCrawlY = m_crawlerY + m_titleHeight;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:449:    int textCrawlY = m_crawlerY + m_titleHeight;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.h:66:    int m_titleHeight;
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_titleHeight' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
4
```

### m_lines

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_lines' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:98:    m_lines = std::vector<s_CreditLine>();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:115:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:121:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:127:    m_lines.push_back(spacer);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:128:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:134:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:141:    m_lines.push_back(spacer);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:143:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:149:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:155:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:161:        m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:167:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:173:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:179:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:185:    m_lines.push_back(s_CreditLine {
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_lines' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
56
```

### s_CreditLine

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 's_CreditLine' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:98:    m_lines = std::vector<s_CreditLine>();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:108:    auto spacer = s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:115:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:121:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:128:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:134:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:143:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:149:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:155:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:161:        m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:167:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:173:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:179:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:185:    m_lines.push_back(s_CreditLine {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:191:    m_lines.push_back(s_CreditLine {
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 's_CreditLine' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
50
```

### regionSceneState

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'regionSceneState' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:105:    regionSceneState = eRegionSceneState::SCENE_INIT;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:224:        if (regionSceneState == SCENE_INIT) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:229:        else if (regionSceneState == SCENE_THREE_HOUSES_COME_FOR_DUNE) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:235:        else if (regionSceneState == SCENE_TO_TAKE_CONTROL_OF_THE_LAND) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:241:        else if (regionSceneState == SCENE_THAT_HAS_BECOME_DIVIDED) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:677:    if (regionSceneState == SCENE_THREE_HOUSES_COME_FOR_DUNE) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:680:    else if (regionSceneState == SCENE_TO_TAKE_CONTROL_OF_THE_LAND ||
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:681:             regionSceneState == SCENE_THAT_HAS_BECOME_DIVIDED) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:685:    else if (regionSceneState == SCENE_SELECT_YOUR_NEXT_CONQUEST) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:990:    regionSceneState = newSceneState;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.h:133:    eRegionSceneState regionSceneState;
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'regionSceneState' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
11
```

### iRegionSceneAlpha

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'iRegionSceneAlpha' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:111:    iRegionSceneAlpha = 0;  // alpha for scene in introduction state
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:211:        if (iRegionSceneAlpha < 255) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:212:            iRegionSceneAlpha += 1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:215:        if (iRegionSceneAlpha > 255) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:216:            iRegionSceneAlpha = 255;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:230:            if (!hasMessage && iRegionSceneAlpha >= 255) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:236:            if (!hasMessage && iRegionSceneAlpha >= 255) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:242:            if (iRegionSceneAlpha >= 255) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:678:        drawHdMapBase(static_cast<Uint8>(iRegionSceneAlpha));
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:683:        drawHdMapBorders(static_cast<Uint8>(iRegionSceneAlpha));
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:991:    iRegionSceneAlpha = 0;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.h:134:    int iRegionSceneAlpha;          // scene alpha
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'iRegionSceneAlpha' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
12
```

### m_displayStatusLabel

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_displayStatusLabel' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_displayStatusLabel' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### switchOptionsPage

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'switchOptionsPage' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'switchOptionsPage' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### OptionsPage

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'OptionsPage' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'OptionsPage' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### m_bindingCapture

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_bindingCapture' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15

```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'm_bindingCapture' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
0
```

### friend

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'friend' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -15
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:89:    friend class UiAuditAccess;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameSettings.h:25:    friend class UiAuditAccess;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameSettings.h:202:    friend class cGame;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/units/cUnit.h:142:    friend class cUnit;
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'friend' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
4
```

### Прочее

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -h -o -E '\bREGSTATE_[A-Z_]+' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | sort | uniq -c
      5 REGSTATE_CONQUER_REGIONS
      4 REGSTATE_FADEOUT
      3 REGSTATE_INIT
      5 REGSTATE_INTRODUCTION
      7 REGSTATE_SELECT_NEXT_CONQUEST
```

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'Restart|Saved|restart' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src/gamestates src/gui src/game
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameSettings.h:42:    int getSavedRenderScalePercent() const {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameSettings.h:45:    int getSavedWorldScalePercent() const {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameSettings.h:48:    void setSavedScalePercents(int renderScalePercent, int worldScalePercent) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameSettings.h:168:    // written to preferences.ini; the running game keeps m_renderScalePercent and m_worldScalePercent until restart
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:306:    m_gameSettings->setSavedScalePercents(gs->renderScalePercent, gs->worldScalePercent);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:354:    gs.renderScalePercent = m_gameSettings->getSavedRenderScalePercent();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:355:    gs.worldScalePercent = m_gameSettings->getSavedWorldScalePercent();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1037:            m_timeManager->restartTimer();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeCounter.cpp:36:void cTimeCounter::restart()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeCounter.h:26:    void restart();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeManager.cpp:276:void cTimeManager::restartTimer()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeManager.cpp:278:    m_timeCounter->restart();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeManager.h:52:    // returns the stored timer value in seconds (pause-aware, see pauseTimer()/restartTimer())
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeManager.h:59:    // restart Timer
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cTimeManager.h:60:    void restartTimer();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:65:    m_selectedRenderScaleIndex = scaleChoiceIndex(m_renderScaleChoices, m_settings->getSavedRenderScalePercent());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:66:    m_selectedWorldScaleIndex = scaleChoiceIndex(m_worldScaleChoices, m_settings->getSavedWorldScalePercent());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:566:        renderScale != m_settings->getSavedRenderScalePercent() ||
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:567:        worldScale != m_settings->getSavedWorldScalePercent()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:578:        m_settings->setSavedScalePercents(renderScale, worldScale);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:579:        m_statusLabel->setText("Saved. Restart the game.");
```
