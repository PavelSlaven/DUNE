# Пункт 2. Функции дословно и вызовы режима
## Заданные функции
### cUnit::draw_experience — нет определения

нет определения

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cUnit::draw_experience\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```
### cUnit::draw_group — нет определения

нет определения

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cUnit::draw_group\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```
### cUnit::draw_health — нет определения

нет определения

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cUnit::draw_health\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```
### cUnit::draw_spice — нет определения

нет определения

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cUnit::draw_spice\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```
### cStructureDrawer::drawStructureHealthBar — src/drawers/cStructureDrawer.cpp@acddd29:477-510

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cStructureDrawer::drawStructureHealthBar\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cStructureDrawer.cpp:477:void cStructureDrawer::drawStructureHealthBar(int iStructure)
```
```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '477,510p'
   477	void cStructureDrawer::drawStructureHealthBar(int iStructure)
   478	{
   479	    if (iStructure < 0 || iStructure >= MAX_STRUCTURES) return;
   480	
   481	    cAbstractStructure *theStructure = m_objects->getStructures()[iStructure];
   482	
   483	    if (!theStructure) {
   484	        return;
   485	    }
   486	
   487	    // Draw structure health
   488	    int draw_x = theStructure->iDrawX() - 1;
   489	    int draw_y = theStructure->iDrawY() - 5;
   490	
   491	    int widthBmp = m_mapCamera->factorZoomLevel(theStructure->getStructureInfo().bmp_width);
   492	    int width_x = widthBmp - 1;
   493	
   494	    int height_y = 4;
   495	
   496	    float healthNormalized = theStructure->getHealthNormalized();
   497	
   498	    int w = healthNormalized * width_x;
   499	    int r = (1.1 - healthNormalized) * 255;
   500	    int g = healthNormalized * 255;
   501	
   502	    if (r > 255) r = 255;
   503	
   504	    // bar itself
   505	    m_sdlDrawer->renderRectFillColor(draw_x, draw_y, width_x+1, height_y+1, 0,0,0,255);
   506	    m_sdlDrawer->renderRectFillColor(draw_x, draw_y, (w-1), height_y, static_cast<Uint8>(r),static_cast<Uint8>(g),32,255);
   507	
   508	    // bar around it
   509	    m_sdlDrawer->renderRectColor(draw_x, draw_y, width_x, height_y, Color{255, 255, 255,255});
   510	}
```

### cGame::run — src/game/cGame_logic.cpp@acddd29:571-643

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cGame::run\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:571:void cGame::run()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/sGameServices.h:60:    Texture *screenTexture = nullptr; // set in cGame::run(), before any state transition
```
```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '571,643p'
   571	void cGame::run()
   572	{
   573	    ensureFrameTargets();
   574	    SDL_Event event;
   575	    while (m_gameSettings->m_playing) {
   576	        if (uiaudit::isEnabled() || m_focusManager->isGameWindowActive()) {
   577	            m_timeManager->processTime();
   578	        }
   579	        while (SDL_PollEvent(&event)) {
   580	            switch (event.type) {
   581	                case SDL_EVENT_QUIT:
   582	                    m_gameSettings->m_playing = false;
   583	                    break;
   584	                case SDL_EVENT_WINDOW_FOCUS_LOST:
   585	                case SDL_EVENT_WINDOW_MINIMIZED:
   586	                    m_focusManager->onWindowFocusLost();
   587	                    break;
   588	                case SDL_EVENT_WINDOW_FOCUS_GAINED:
   589	                case SDL_EVENT_WINDOW_RESTORED:
   590	                    m_focusManager->onWindowFocusGained();
   591	                    // macOS only hides the cursor while the window actually holds key focus, so if
   592	                    // focus wasn't granted at boot (e.g. the mouse moved during window creation), the
   593	                    // initial SDL_HideCursor() call in setupGame() is a no-op until focus is regained.
   594	                    SDL_HideCursor();
   595	                    break;
   596	                case SDL_EVENT_WINDOW_PIXEL_SIZE_CHANGED:
   597	                    m_Screen->onPixelSizeChanged();
   598	                    break;
   599	                case SDL_EVENT_KEY_DOWN:
   600	                case SDL_EVENT_KEY_UP:
   601	                case SDL_EVENT_TEXT_INPUT:
   602	                    m_keyboard->handleEvent(event);
   603	                    break;
   604	
   605	                case SDL_EVENT_MOUSE_BUTTON_DOWN:
   606	                case SDL_EVENT_MOUSE_BUTTON_UP:
   607	                case SDL_EVENT_MOUSE_MOTION:
   608	                case SDL_EVENT_MOUSE_WHEEL:
   609	                    m_mouse->handleEvent(event);
   610	                default:
   611	                    break;
   612	            }
   613	        }
   614	
   615	        if (!uiaudit::isEnabled() && !m_focusManager->isGameWindowActive()) {
   616	            m_timeManager->waitForCPU(); // wait for CPU to catch up, so we don't run too fast
   617	            continue; // skip the rest of the loop when we don't have focus
   618	        }
   619	
   620	        updateMouseAndKeyboardState();
   621	        m_currentState->update();
   622	        //Logger::print(LOG_INFO , COMP_NONE, "m_currentState", "m_currentState {}", gameStateToString(m_currentState->getType()));
   623	
   624	        ensureFrameTargets();
   625	        m_sdlDrawer->beginDrawingToTexture(actualRenderer);
   626	        m_sdlDrawer->renderClearToColor();
   627	        if (uiaudit::isEnabled()) {
   628	            uiaudit::beginFrame(*this);
   629	        }
   630	        drawState(); // run game state, includes interaction + drawing
   631	        transitionStateIfRequired();
   632	        shakeScreenAndBlitBuffer();
   633	
   634	        m_sdlDrawer->endDrawingToTexture();
   635	        m_sdlDrawer->renderClearToColor();  // SDL3 persists its intermediate texture between frames; clear before composite
   636	        m_sdlDrawer->renderSprite(actualRenderer, m_screenShake->getX(), m_screenShake->getY());
   637	        if (uiaudit::isEnabled()) {
   638	            uiaudit::onFramePresented(*this);
   639	        }
   640	        SDL_RenderPresent(renderer);
   641	        m_timeManager->waitForCPU(); // wait for CPU to catch up, so we don't run too fast
   642	    }
   643	}
```

### cGame::drawOutcomeScreen — нет определения

нет определения

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cGame::drawOutcomeScreen\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```
### cGame::takeBackGroundScreen — src/game/cGame_logic.cpp@acddd29:1708-1713

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cGame::takeBackGroundScreen\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1708:void cGame::takeBackGroundScreen()
```
```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '1708,1713p'
  1708	void cGame::takeBackGroundScreen()
  1709	{
  1710	    m_sdlDrawer->beginDrawingToTexture(screenTexture);
  1711	    SDL_RenderTexture(renderer, actualRenderer->tex.get(), nullptr, nullptr);
  1712	    m_sdlDrawer->endDrawingToTexture();
  1713	}
```

### cDrawManager::missionInit — src/managers/cDrawManager.cpp@acddd29:419-423

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cDrawManager::missionInit\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp:419:void cDrawManager::missionInit()
```
```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | nl -ba | sed -n '419,423p'
   419	void cDrawManager::missionInit()
   420	{
   421	    m_creditsDrawer->setCredits();
   422	    m_messageDrawer->initCombatPosition();
   423	}
```

### cDrawManager::draw — нет определения

нет определения

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cDrawManager::draw\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
```
### cSideBarDrawer::draw — src/drawers/cSideBarDrawer.cpp@acddd29:98-101

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cSideBarDrawer::draw\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cSideBarDrawer.cpp:98:void cSideBarDrawer::draw()
```
```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '98,101p'
    98	void cSideBarDrawer::draw()
    99	{
   100	    drawHdSidebar();
   101	}
```

### cStructureFactory::createStructure — src/gameobjects/structures/cStructureFactory.cpp@acddd29:119-225

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cStructureFactory::createStructure\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cStructureFactory.cpp:108:// cAbstractStructure *cStructureFactory::createStructure(int iCell, int iStructureType, int iPlayer)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cStructureFactory.cpp:119:cAbstractStructure *cStructureFactory::createStructure(int iCell, int iStructureType, int iPlayer, int iPercent)
```
```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cStructureFactory.cpp | nl -ba | sed -n '119,225p'
   119	cAbstractStructure *cStructureFactory::createStructure(int iCell, int iStructureType, int iPlayer, int iPercent)
   120	{
   121	    d2tm_assert(iPlayer >= 0);
   122	    d2tm_assert(iPlayer <= MAX_PLAYERS);
   123	
   124	    if (iPercent > 100) iPercent = 100;
   125	
   126	    updatePlayerCatalogAndPlaceNonStructureTypeIfApplicable(iCell, iStructureType, iPlayer);
   127	    clearFogForStructureType(iCell, iStructureType, 2, iPlayer);
   128	
   129	    // SLAB and WALL is not a real structure. The terrain is manipulated
   130	    // therefore quit here, as we won't place real structure.
   131	    if (iStructureType == SLAB1 || iStructureType == SLAB4 || iStructureType == WALL) {
   132	        return nullptr;
   133	    }
   134	
   135	    float fPercent = static_cast<float>(iPercent)/100; // divide by 100 (to make it 0.x)
   136	
   137	    s_StructureInfo &structureInfo = m_info->getStructureInfo(iStructureType);
   138	    int hp = structureInfo.hp;
   139	    if (hp < 0) {
   140	        Logger::info(COMP_STRUCTURES, "create structure", "Structure to create has no hp, aborting creation.");
   141	        return nullptr;
   142	    }
   143	
   144	    int iNewId = getFreeSlot();
   145	
   146	    // fail
   147	    if (iNewId < 0) {
   148	        Logger::info(COMP_STRUCTURES, "create structure", "No free slot available, returning nullptr");
   149	        return nullptr;
   150	    }
   151	
   152	    std::unique_ptr<cAbstractStructure> newStructure = createStructureInstance(iStructureType);
   153	
   154	    if (newStructure == nullptr) {
   155	        Logger::info(COMP_STRUCTURES, "create structure", "cannot create structure: createStructureInstance returned nullptr");
   156	        return nullptr; // fail
   157	    }
   158	
   159	    cAbstractStructure *str = newStructure.get();
   160	
   161	    cPoint absTopLeft = m_objects->getMapGeometry()->getAbsolutePositionFromCell(iCell);
   162	    cPlayer *player = m_objects->getPlayer(iPlayer);
   163	
   164	    for (auto flag : structureInfo.flags) {
   165	        cPoint pos = cPoint(
   166	                         absTopLeft.x + flag.relX,
   167	                         absTopLeft.y + flag.relY
   168	                     );
   169	
   170	        if (flag.big) {
   171	            str->addFlag(cFlag::createBigFlag(player, pos, m_mapCamera, m_settings, m_renderer));
   172	        }
   173	        else {
   174	            str->addFlag(cFlag::createSmallFlag(player, pos, m_mapCamera, m_settings, m_renderer));
   175	        }
   176	    }
   177	
   178	    // calculate actual health
   179	    float fHealth = hp * fPercent;
   180	
   181	    Logger::debug(COMP_STRUCTURES, "cStructureFactory", "Structure with id [{}] has [{}] hp , fhealth is [{}]", iStructureType, hp, fHealth);
   182	
   183	    int structureSize = structureInfo.bmp_width * structureInfo.bmp_height;
   184	
   185	    // assign to array
   186	    str->serviceInit(m_services);
   187	    m_objects->getStructures().place(iNewId, std::move(newStructure));
   188	
   189	    // Now set it up for location & player
   190	    str->setCell(iCell);
   191	    str->setOwner(iPlayer);
   192	    str->setBuildingFase(1); // prebuild
   193	    str->TIMER_prebuild = std::min(structureSize/16, 250); // prebuild timer. A structure of 64x64 will result in 256, bigger structure has longer timer
   194	    str->TIMER_decay = RNG::rnd(1000) + 100;
   195	    str->fConcrete = (1 - fPercent);
   196	    str->setHitPoints(static_cast<int>(fHealth));
   197	    str->setFrame(RNG::rnd(1)); // random start frame (flag)
   198	    str->setStructureId(iNewId);
   199	    str->setWidth(structureInfo.bmp_width / TILESIZE_WIDTH_PIXELS);
   200	    str->setHeight(structureInfo.bmp_height / TILESIZE_HEIGHT_PIXELS);
   201	
   202	    // clear fog around structure
   203	    clearFogForStructureType(iCell, str);
   204	
   205	    // additional forces: (UNITS)
   206	    if (iStructureType == REFINERY) {
   207	        REINFORCE(m_objects, m_info, m_eventEmitter, iPlayer, HARVESTER, iCell, -1);
   208	    }
   209	
   210	    m_structureUtils->putStructureOnDimension(MAPID_STRUCTURES, str);
   211	
   212	    // handle update
   213	    const s_GameEvent event {
   214	        .eventType = eGameEventType::GAME_EVENT_CREATED,
   215	        .data = CommonEvent {
   216	            .entityType = eBuildType::STRUCTURE,
   217	            .entityID = str->getStructureId(),
   218	            .player = str->getPlayer(),
   219	            .entitySpecificType = iStructureType
   220	        }
   221	    };
   222	    m_eventEmitter->emit(event);
   223	
   224	    return str;
   225	}
```

## Функции вызовов режима
Заголовков, удовлетворяющих фильтру, нет.

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^[A-Za-z_].*::[A-Za-z_]*([Pp]laying|[Bb]riefing|[Oo]utcome|[Ww]inning|[Ll]osing)[A-Za-z_]*\(' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src/game
```
## Вызовы создания юнита
```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '\b(UNIT_CREATE|createUnit|[Cc]reate[A-Za-z]*Unit)\b' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -30
```

## Контекст строк форка из hooks.tsv
### src/cGame_logic.cpp@9208dcf:12

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '9,15p'
     9	  2001 - 2022 (c) code by Stefan Hendriks
    10	
    11	*/
    12	#include "debug/UiAudit.hpp"
    13	#include "cGame.h"
    14	#include "audio/MusicController.h"
    15	#include "audio/MusicTransitionPolicy.hpp"
```

### src/cGame_logic.cpp@9208dcf:771

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '768,774p'
   768	        renderDrawer->beginDrawingToTexture(frameTarget);
   769	        SDL_RenderSetLogicalSize(renderer, m_screenW, m_screenH);
   770	        renderDrawer->renderClearToColor();
   771	        if (uiaudit::isEnabled()) {
   772	            uiaudit::beginFrame(*this);
   773	        }
   774	        drawState(); // run game state, includes interaction + drawing
```

### src/cGame_logic.cpp@9208dcf:772

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '769,775p'
   769	        SDL_RenderSetLogicalSize(renderer, m_screenW, m_screenH);
   770	        renderDrawer->renderClearToColor();
   771	        if (uiaudit::isEnabled()) {
   772	            uiaudit::beginFrame(*this);
   773	        }
   774	        drawState(); // run game state, includes interaction + drawing
   775	        transitionStateIfRequired();
```

### src/cGame_logic.cpp@9208dcf:780

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '777,783p'
   777	
   778	        renderDrawer->endDrawingToTexture();
   779	        presentFrame(frameTarget, hdPresentationFrame);
   780	        if (uiaudit::isEnabled()) {
   781	            uiaudit::onFramePresented(*this);
   782	        }
   783	        SDL_RenderPresent(renderer);
```

### src/cGame_logic.cpp@9208dcf:781

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '778,784p'
   778	        renderDrawer->endDrawingToTexture();
   779	        presentFrame(frameTarget, hdPresentationFrame);
   780	        if (uiaudit::isEnabled()) {
   781	            uiaudit::onFramePresented(*this);
   782	        }
   783	        SDL_RenderPresent(renderer);
   784	        m_timeManager->waitForCPU(); // wait for CPU to catch up, so we don't run too fast
```

### src/drawers/cStructureDrawer.cpp@9208dcf:7

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '4,10p'
     4	#include "controls/cGameControlsContext.h"
     5	#include "data/gfxdata.h"
     6	#include "d2tmc.h"
     7	#include "debug/UiAudit.hpp"
     8	#include "gameobjects/structures/cGunTurret.h"
     9	#include "gameobjects/structures/cRefinery.h"
    10	#include "gameobjects/structures/cRepairFacility.h"
```

### src/drawers/cStructureDrawer.cpp@9208dcf:1031

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '1028,1034p'
  1028	
  1029	    if (r > 255) r = 255;
  1030	
  1031	    if (uiaudit::isEnabled()) {
  1032	        uiaudit::recordLabel("structure-health", iStructure, "STRUCTURE", draw_x, draw_y, width_x + 1, height_y + 1,
  1033	                             uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
  1034	    }
```

### src/drawers/cStructureDrawer.cpp@9208dcf:1032

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '1029,1035p'
  1029	    if (r > 255) r = 255;
  1030	
  1031	    if (uiaudit::isEnabled()) {
  1032	        uiaudit::recordLabel("structure-health", iStructure, "STRUCTURE", draw_x, draw_y, width_x + 1, height_y + 1,
  1033	                             uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
  1034	    }
  1035	
```

### src/drawers/cStructureDrawer.cpp@9208dcf:1033

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '1030,1036p'
  1030	
  1031	    if (uiaudit::isEnabled()) {
  1032	        uiaudit::recordLabel("structure-health", iStructure, "STRUCTURE", draw_x, draw_y, width_x + 1, height_y + 1,
  1033	                             uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
  1034	    }
  1035	
  1036	    // bar itself
```

### src/gameobjects/units/cUnit.cpp@9208dcf:17

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '14,20p'
    14	
    15	#include "d2tmc.h"
    16	#include "data/gfxdata.h"
    17	#include "debug/UiAudit.hpp"
    18	#include "include/Texture.hpp"
    19	#include "drawers/SDLDrawer.hpp"
    20	#include "gameobjects/particles/cParticle.h"
```

### src/gameobjects/units/cUnit.cpp@9208dcf:581

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '578,584p'
   578	    int max = getUnitInfo().credit_capacity;
   579	    int w = healthBar(width_x, iCredits, max);
   580	
   581	    if (uiaudit::isEnabled()) {
   582	        uiaudit::recordUnitLabel("spice", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
   583	    }
   584	
```

### src/gameobjects/units/cUnit.cpp@9208dcf:582

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '579,585p'
   579	    int w = healthBar(width_x, iCredits, max);
   580	
   581	    if (uiaudit::isEnabled()) {
   582	        uiaudit::recordUnitLabel("spice", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
   583	    }
   584	
   585	    // bar itself
```

### src/gameobjects/units/cUnit.cpp@9208dcf:633

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '630,636p'
   630	
   631	    if (r > 255) r = 255;
   632	
   633	    if (uiaudit::isEnabled()) {
   634	        uiaudit::recordUnitLabel("health", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
   635	    }
   636	
```

### src/gameobjects/units/cUnit.cpp@9208dcf:634

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '631,637p'
   631	    if (r > 255) r = 255;
   632	
   633	    if (uiaudit::isEnabled()) {
   634	        uiaudit::recordUnitLabel("health", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
   635	    }
   636	
   637	    // bar itself
```

### src/gameobjects/units/cUnit.cpp@9208dcf:660

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '657,663p'
   657	    if (iGroup > 0 && iPlayer == HUMAN) {
   658	        // @mira I don't fix group name without acces to textDrawer: fixed on ctx branch
   659	        const int groupX = drawx + std::max(3, visual.getWidth() - 8);
   660	        if (uiaudit::isEnabled()) {
   661	            uiaudit::beginLabelText();
   662	        }
   663	        textDrawer->drawText(groupX, drawy - 11, Color::black(),std::format("{}",iGroup));
```

### src/gameobjects/units/cUnit.cpp@9208dcf:661

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '658,664p'
   658	        // @mira I don't fix group name without acces to textDrawer: fixed on ctx branch
   659	        const int groupX = drawx + std::max(3, visual.getWidth() - 8);
   660	        if (uiaudit::isEnabled()) {
   661	            uiaudit::beginLabelText();
   662	        }
   663	        textDrawer->drawText(groupX, drawy - 11, Color::black(),std::format("{}",iGroup));
   664	        textDrawer->drawText(groupX, drawy - 12, Color::white(),std::format("{}",iGroup));
```

### src/gameobjects/units/cUnit.cpp@9208dcf:665

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '662,668p'
   662	        }
   663	        textDrawer->drawText(groupX, drawy - 11, Color::black(),std::format("{}",iGroup));
   664	        textDrawer->drawText(groupX, drawy - 12, Color::white(),std::format("{}",iGroup));
   665	        if (uiaudit::isEnabled()) {
   666	            uiaudit::endLabelText("group", iID, iType, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
   667	        }
   668	    }
```

### src/gameobjects/units/cUnit.cpp@9208dcf:666

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '663,669p'
   663	        textDrawer->drawText(groupX, drawy - 11, Color::black(),std::format("{}",iGroup));
   664	        textDrawer->drawText(groupX, drawy - 12, Color::white(),std::format("{}",iGroup));
   665	        if (uiaudit::isEnabled()) {
   666	            uiaudit::endLabelText("group", iID, iType, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
   667	        }
   668	    }
   669	}
```

### src/gameobjects/units/cUnit.cpp@9208dcf:720

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '717,723p'
   717	    int drawx = visual.getX() + 3;
   718	    int drawy = visual.getY() - 19;
   719	
   720	    if (uiaudit::isEnabled()) {
   721	        const Texture *star = gfxdata->getTexture(OBJECT_STAR_01 + iStarType);
   722	        if (star != nullptr) {
   723	            uiaudit::recordUnitLabel("experience", iID, iType, drawx, drawy, (iStars - 1) * 9 + star->w, star->h, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
```

### src/gameobjects/units/cUnit.cpp@9208dcf:723

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '720,726p'
   720	    if (uiaudit::isEnabled()) {
   721	        const Texture *star = gfxdata->getTexture(OBJECT_STAR_01 + iStarType);
   722	        if (star != nullptr) {
   723	            uiaudit::recordUnitLabel("experience", iID, iType, drawx, drawy, (iStars - 1) * 9 + star->w, star->h, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
   724	        }
   725	    }
   726	
```

### src/managers/cDrawManager.cpp@9208dcf:5

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | nl -ba | sed -n '2,8p'
     2	
     3	#include "controls/cGameControlsContext.h"
     4	#include "d2tmc.h"
     5	#include "debug/UiAudit.hpp"
     6	#include "data/gfxdata.h"
     7	#include "data/gfxinter.h"
     8	#include "drawers/SDLDrawer.hpp"
```

## Поиск вызовов интерфейса
### FORK1

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E 'recordSidebarClicks|recordCommandBarClicks|mapViewport|stopCameraEdgeMove|clearMouseClicks|freezeClock|resumeClock|setHover' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src ':!src/debug/UiAuditAccess.cpp'
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h:113:    cRectangle *m_mapViewport;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:958:    delete m_mapViewport;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1161:    m_mapViewport = new cRectangle(0, cSideBar::TopBarHeight, game.m_screenW - cSideBar::SidebarWidth, game.m_screenH - cSideBar::TopBarHeight);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:74:void setHover(int x, int y);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:86:    static bool mapViewport(const cGame &game, int &x, int &y, int &w, int &h);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:102:    static void freezeClock(cGame &game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:103:    static void resumeClock(cGame &game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:104:    static void clearMouseClicks(cGame &game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:105:    static void stopCameraEdgeMove();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:109:    static void recordSidebarClicks(cSideBarDrawer &drawer);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp:110:    static void recordCommandBarClicks(cCommandBarDrawer &drawer);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:170:    if (g_scene->gameScreen && UiAuditAccess::mapViewport(game, viewX, viewY, viewW, viewH)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:424:void setHover(int x, int y)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:445:    UiAuditAccess::clearMouseClicks(game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:446:    UiAuditAccess::stopCameraEdgeMove();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:447:    UiAuditAccess::freezeClock(game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:449:    UiAuditAccess::resumeClock(game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:102:        UiAuditAccess::recordCommandBarClicks(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:70:        UiAuditAccess::recordSidebarClicks(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:57:    m_particleDrawer.determineParticlesToDraw(*game.m_mapViewport);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMap.cpp:556:        if (pUnit.isWithinViewport(game.m_mapViewport)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMap.cpp:572:        if (pUnit.isWithinViewport(game.m_mapViewport)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMap.cpp:590:        if (pUnit.isWithinViewport(game.m_mapViewport)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMap.cpp:614:        if (!pUnit.isWithinViewport(game.m_mapViewport)) continue;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMap.cpp:631:        if (pUnit.isWithinViewport(game.m_mapViewport)) {
```

### PORT

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E 'recordSidebarClicks|recordCommandBarClicks|mapViewport|stopCameraEdgeMove|clearMouseClicks|freezeClock|resumeClock|setHover' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src ':!src/debug/UiAuditAccess.cpp'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/controls/cGameControlsContext.cpp:83:    m_mapViewport = services->mapViewport;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/controls/cGameControlsContext.h:67:    cRectangle *getMapViewport() const { return m_mapViewport; }
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/controls/cGameControlsContext.h:158:    cRectangle *m_mapViewport = nullptr;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAudit.hpp:48:    static void freezeClock(cGame &game);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAudit.hpp:49:    static void resumeClock(cGame &game);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAuditCapture.cpp:287:    UiAuditAccess::freezeClock(currentGame);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/debug/UiAuditCapture.cpp:289:    UiAuditAccess::resumeClock(currentGame);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h:101:    std::unique_ptr<cRectangle> m_mapViewport;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:682:    m_mapViewport.reset();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:833:    m_mapViewport = std::make_unique<cRectangle>(0, cSideBar::TopBarHeight, m_gameSettings->getScreenW() - cSideBar::SidebarWidth, m_gameSettings->getScreenH() - cSideBar::TopBarHeight);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:875:    m_services->mapViewport = m_mapViewport.get();
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:102:    m_mapViewport = services->mapViewport;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:103:    d2tm_assert(m_mapViewport != nullptr);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:810:        if (!pUnit->isWithinViewport(m_mapViewport) || isHiddenByFogOfWar(pUnit)) continue;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:818:    auto *mapViewport = m_mapViewport;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:834:        if (pUnit->isWithinViewport(mapViewport) && !isHiddenByFogOfWar(pUnit)) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:850:        if (pUnit->isWithinViewport(mapViewport) && !isHiddenByFogOfWar(pUnit)) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:868:        if (pUnit->isWithinViewport(mapViewport) && !isHiddenByFogOfWar(pUnit)) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:888:    auto *mapViewport = m_mapViewport;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:895:        if (!pUnit->isWithinViewport(mapViewport)) continue;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.cpp:914:        if (pUnit->isWithinViewport(mapViewport) && !isHiddenByFogOfWar(pUnit)) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.h:491:    cRectangle *m_mapViewport = nullptr;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp:101:    m_mapViewport = services->mapViewport;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp:102:    d2tm_assert(m_mapViewport != nullptr);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp:281:    const cRectangle* battlefield = m_mapViewport;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.h:87:    cRectangle* m_mapViewport = nullptr;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/sGameServices.h:52:    cRectangle *mapViewport = nullptr;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp:69:    m_mapViewport(services->mapViewport),
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp:128:    m_particleDrawer->determineParticlesToDraw(*m_mapViewport);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.h:155:    cRectangle* m_mapViewport = nullptr;
```

