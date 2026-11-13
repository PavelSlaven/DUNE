# Пункты 1 и 4: интерфейс, включение и выходы

Основные таблицы: `.tmp/p5dr/api.tsv` и `.tmp/p5dr/entry.tsv`. Все строки кода ниже получены из `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566` либо из `PORT=7eb119b007c05f063fe6dacf2e93ae31ac135b33`; сокращённые ссылки в таблицах имеют вид `путь@9208dcf:строка` и `путь@7eb119b:строка`.

## 1. Интерфейс режима в FORK1

Таблица `api.tsv` содержит типы `GameKind`, `Rect`, `BoxScope`, `UiAuditAccess`, `Options`, `Scene`, объявленные функции, методы и наружную переменную `g_enabled`. Для каждой функции указано определение или пометка «в заголовке»; определения методов `UiAuditAccess` находятся в `src/debug/UiAuditAccess.cpp`, функции записи и кадрового цикла — в `src/debug/UiAuditCapture.cpp`, функции параметров — в `src/debug/UiAuditArguments.cpp`, функции каталога — в `src/debug/UiAuditScenes.cpp`.

Команда для списка исходников:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug src/main.cpp src/cGame_logic.cpp
```

Выдержка из вывода:

```text
src/cGame_logic.cpp
src/debug/UiAudit.hpp
src/debug/UiAuditAccess.cpp
src/debug/UiAuditArguments.cpp
src/debug/UiAuditArguments.hpp
src/debug/UiAuditCapture.cpp
src/debug/UiAuditScenes.cpp
src/debug/UiAuditScenes.hpp
src/main.cpp
```

Команда подсчёта строк:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | grep 'UiAudit.*\.[ch]pp$' | while read p; do printf '%s ' "$p"; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:"$p" | wc -l; done
```

Выдержка из вывода:

```text
src/debug/UiAudit.hpp 115
src/debug/UiAuditAccess.cpp 934
src/debug/UiAuditArguments.cpp 46
src/debug/UiAuditArguments.hpp 24
src/debug/UiAuditCapture.cpp 505
src/debug/UiAuditScenes.cpp 588
src/debug/UiAuditScenes.hpp 31
```

Команда чтения объявления интерфейса:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp | nl -ba | sed -n '16,115p'
```

Выдержка из вывода:

```text
    16 enum GameKind {
    17     Hud,
    18     Music,
    19     DamagedUnit,
    20     Harvester,
    21     Mcv,
    22     Structure,
    23     ListBuild,
    24     ListInfantry,
    25     ListVehicles,
    26     ListStarport,
    27     ListPalace,
    28     ListUpgrades,
    29     RadarNone,
    30     RadarNoPower,
    31     PlaceAllowed,
    32     PlaceForbidden,
    33     GroupSelect,
    34     Messages,
    35     ItemHover,
    36     ScrollEnd,
    37     Rally
    38 };
    40 struct Rect {
    41     int x;
    42     int y;
    43     int w;
    44     int h;
    45 };
    47 void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box = nullptr);
    48 void recordGui(const char *type, int x, int y, int w, int h);
    49 void recordArea(const char *name, int x, int y, int w, int h);
    50 void recordClick(const char *name, int x, int y, int w, int h);
    51 void recordCanvasClick(const char *name);
    52 void dropClicksUnderModal();
    53 void recordLabel(const char *kind, int obj, const char *type, int x, int y, int w, int h, const Rect &owner);
    54 void recordUnitLabel(const char *kind, int obj, int unitType, int x, int y, int w, int h, const Rect &owner);
    55 void beginLabelText();
    56 void endLabelText(const char *kind, int obj, int unitType, const Rect &owner);
    58 class BoxScope {
    59 public:
    60     BoxScope(int x, int y, int w, int h);
    61     ~BoxScope();
    62     BoxScope(const BoxScope &) = delete;
    63     BoxScope &operator=(const BoxScope &) = delete;
    64 };
    66 void setVerticalClipText(bool enabled);
    67 void recordCreditLine(const std::string &name, const std::string &text);
    69 bool handleEarlyExit(int &exitCode);
    70 void onSetupDone(cGame &game);
    71 void beginFrame(cGame &game);
    72 void onFramePresented(cGame &game);
    73 bool failed();
    74 void setHover(int x, int y);
    78 class UiAuditAccess {
    79 public:
    80     static int state(const cGame &game);
    81     static const cGameState *currentState(const cGame &game);
    82     static const AbstractMentat *mentat(const cGame &game);
    83     static SDL_Renderer *renderer(cGame &game);
    84     static int renderScale(const cGame &game);
    85     static int worldScale(const cGame &game);
    86     static bool mapViewport(const cGame &game, int &x, int &y, int &w, int &h);
    87     static void setState(cGame &game, int state);
    88     static void prepareTellHouse(cGame &game, int house);
    89     static bool mentatFreeze(cGame &game, bool awaiting);
    90     static bool prepareMentatScene(cGame &game, int house, int kind);
    91     static bool prepareSkirmish(cGame &game, int variant);
    92     static void missionOutcome(cGame &game, bool victory);
    93     static void writeSaves(cGame &game);
    94     static bool openMenuSaveDialog(cGame &game);
    95     static bool saveDialog(cGame &game, int action);
    96     static bool optionsPage(cGame &game, int page);
    97     static bool optionsBinding(cGame &game);
    98     static bool optionsStatus(cGame &game);
    99     static bool creditsScroll(cGame &game, int frame);
   100     static void recordCreditLines(cGame &game);
   101     static void regionOpen(cGame &game, int mission, bool jump);
   102     static void freezeClock(cGame &game);
   103     static void resumeClock(cGame &game);
   104     static void clearMouseClicks(cGame &game);
   105     static void stopCameraEdgeMove();
   106     static int regionState(const cGame &game);
   107     static int regionScene(const cGame &game);
   108     static int regionSceneAlpha(const cGame &game);
   109     static void recordSidebarClicks(cSideBarDrawer &drawer);
   110     static void recordCommandBarClicks(cCommandBarDrawer &drawer);
   111     static bool enterPlaying(cGame &game, int house, int region);
   112     static bool placeLabelUnits(cGame &game, int unitType);
   113     static bool placeStructure(cGame &game, int edge);
   114     static bool prepareGameScreen(cGame &game, int house, int kind);
   115 };
```

Команда чтения параметров и модели сцены:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.hpp | nl -ba | sed -n '7,22p'
```

Выдержка из вывода:

```text
     7 struct Options {
     8     bool list = false;
     9     std::string scales;
    10     std::string scene;
    11     std::string outDir;
    12 };
    14 extern bool g_enabled;
    16 void consumeArguments(int &argc, char **argv);
    17 const Options &options();
    19 inline bool isEnabled()
    20 {
    21     return g_enabled;
    22 }
```

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.hpp | nl -ba | sed -n '10,30p'
```

Выдержка из вывода:

```text
    10 struct Scene {
    11     const char *id;
    12     const char *group;
    13     const char *state;
    14     const char *screen;
    15     const char *house;
    16     bool hud;
    17     bool gameScreen;
    18     bool hdOnly;
    19     bool hover;
    20     int hoverX;
    21     int hoverY;
    22     const char *readiness;
    23     int settleFrames;
    24     bool (*prepare)(cGame &game);
    25     bool (*ready)(cGame &game);
    26 };
    28 const std::vector<Scene> &catalog();
    29 const Scene *findScene(const std::string &id);
```

Команда поиска определений методов доступа:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'UiAuditAccess::' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug/UiAuditAccess.cpp
```

Выдержка из вывода:

```text
src/debug/UiAuditAccess.cpp:42:int UiAuditAccess::state(const cGame &game)
src/debug/UiAuditAccess.cpp:47:const cGameState *UiAuditAccess::currentState(const cGame &game)
src/debug/UiAuditAccess.cpp:52:const AbstractMentat *UiAuditAccess::mentat(const cGame &game)
src/debug/UiAuditAccess.cpp:57:SDL_Renderer *UiAuditAccess::renderer(cGame &game)
src/debug/UiAuditAccess.cpp:62:void UiAuditAccess::setState(cGame &game, int state)
src/debug/UiAuditAccess.cpp:67:void UiAuditAccess::prepareTellHouse(cGame &game, int house)
src/debug/UiAuditAccess.cpp:72:bool UiAuditAccess::mentatFreeze(cGame &game, bool awaiting)
src/debug/UiAuditAccess.cpp:97:bool UiAuditAccess::prepareMentatScene(cGame &game, int house, int kind)
src/debug/UiAuditAccess.cpp:112:bool UiAuditAccess::prepareSkirmish(cGame &game, int variant)
src/debug/UiAuditAccess.cpp:131:void UiAuditAccess::missionOutcome(cGame &game, bool victory)
src/debug/UiAuditAccess.cpp:138:void UiAuditAccess::writeSaves(cGame &game)
src/debug/UiAuditAccess.cpp:149:bool UiAuditAccess::openMenuSaveDialog(cGame &game)
src/debug/UiAuditAccess.cpp:159:bool UiAuditAccess::saveDialog(cGame &game, int action)
src/debug/UiAuditAccess.cpp:181:bool UiAuditAccess::optionsPage(cGame &game, int page)
src/debug/UiAuditAccess.cpp:191:bool UiAuditAccess::optionsBinding(cGame &game)
src/debug/UiAuditAccess.cpp:202:bool UiAuditAccess::optionsStatus(cGame &game)
src/debug/UiAuditAccess.cpp:213:bool UiAuditAccess::creditsScroll(cGame &game, int frame)
src/debug/UiAuditAccess.cpp:261:void UiAuditAccess::recordCreditLines(cGame &game)
src/debug/UiAuditAccess.cpp:274:void UiAuditAccess::regionOpen(cGame &game, int mission, bool jump)
src/debug/UiAuditAccess.cpp:285:int UiAuditAccess::regionState(const cGame &game)
src/debug/UiAuditAccess.cpp:291:int UiAuditAccess::regionScene(const cGame &game)
src/debug/UiAuditAccess.cpp:297:int UiAuditAccess::regionSceneAlpha(const cGame &game)
src/debug/UiAuditAccess.cpp:303:void UiAuditAccess::freezeClock(cGame &game)
src/debug/UiAuditAccess.cpp:308:void UiAuditAccess::resumeClock(cGame &game)
src/debug/UiAuditAccess.cpp:313:void UiAuditAccess::stopCameraEdgeMove()
src/debug/UiAuditAccess.cpp:322:void UiAuditAccess::clearMouseClicks(cGame &game)
src/debug/UiAuditAccess.cpp:328:int UiAuditAccess::renderScale(const cGame &game)
src/debug/UiAuditAccess.cpp:333:int UiAuditAccess::worldScale(const cGame &game)
src/debug/UiAuditAccess.cpp:338:bool UiAuditAccess::mapViewport(const cGame &game, int &x, int &y, int &w, int &h)
src/debug/UiAuditAccess.cpp:350:void UiAuditAccess::recordSidebarClicks(cSideBarDrawer &drawer)
src/debug/UiAuditAccess.cpp:401:void UiAuditAccess::recordCommandBarClicks(cCommandBarDrawer &drawer)
src/debug/UiAuditAccess.cpp:536:bool UiAuditAccess::enterPlaying(cGame &game, int house, int region)
src/debug/UiAuditAccess.cpp:551:bool UiAuditAccess::placeLabelUnits(cGame &game, int unitType)
src/debug/UiAuditAccess.cpp:591:bool UiAuditAccess::placeStructure(cGame &game, int edge)
src/debug/UiAuditAccess.cpp:780:bool UiAuditAccess::prepareGameScreen(cGame &game, int house, int kind)
```

Команда поиска реализаций записи, цикла кадров и каталога:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E '^(void|bool|int|const std::|const Scene|Options|bool UiAudit|void UiAudit|int UiAudit|const .*UiAudit)' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug/UiAuditCapture.cpp src/debug/UiAuditScenes.cpp
```

Вывод для публичных функций:

```text
src/debug/UiAuditCapture.cpp:265:void setVerticalClipText(bool enabled)
src/debug/UiAuditCapture.cpp:270:void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box)
src/debug/UiAuditCapture.cpp:301:void recordGui(const char *type, int x, int y, int w, int h)
src/debug/UiAuditCapture.cpp:306:void recordArea(const char *name, int x, int y, int w, int h)
src/debug/UiAuditCapture.cpp:311:void recordClick(const char *name, int x, int y, int w, int h)
src/debug/UiAuditCapture.cpp:316:void recordCanvasClick(const char *name)
src/debug/UiAuditCapture.cpp:321:void dropClicksUnderModal()
src/debug/UiAuditCapture.cpp:328:void recordLabel(const char *kind, int obj, const char *type, int x, int y, int w, int h, const Rect &owner)
src/debug/UiAuditCapture.cpp:335:void recordUnitLabel(const char *kind, int obj, int unitType, int x, int y, int w, int h, const Rect &owner)
src/debug/UiAuditCapture.cpp:340:void beginLabelText()
src/debug/UiAuditCapture.cpp:346:void endLabelText(const char *kind, int obj, int unitType, const Rect &owner)
src/debug/UiAuditCapture.cpp:354:void recordCreditLine(const std::string &name, const std::string &text)
src/debug/UiAuditCapture.cpp:369:bool handleEarlyExit(int &exitCode)
src/debug/UiAuditCapture.cpp:424:void setHover(int x, int y)
src/debug/UiAuditCapture.cpp:430:void onSetupDone(cGame &game)
src/debug/UiAuditCapture.cpp:456:void beginFrame(cGame &game)
src/debug/UiAuditCapture.cpp:477:void onFramePresented(cGame &game)
src/debug/UiAuditCapture.cpp:500:bool failed()
src/debug/UiAuditScenes.cpp:573:const std::vector<Scene> &catalog()
src/debug/UiAuditScenes.cpp:578:const Scene *findScene(const std::string &id)
```

Команды точечного чтения тел, определяющих поведение таблицы API:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '42,110p'
```

Вывод:

```text
    42 int UiAuditAccess::state(const cGame &game)
    43 {
    44     return game.m_state;
    45 }
    47 const cGameState *UiAuditAccess::currentState(const cGame &game)
    48 {
    49     return game.m_currentState;
    50 }
    52 const AbstractMentat *UiAuditAccess::mentat(const cGame &game)
    53 {
    54     return game.m_mentat;
    55 }
    57 SDL_Renderer *UiAuditAccess::renderer(cGame &game)
    58 {
    59     return game.renderer;
    60 }
    62 void UiAuditAccess::setState(cGame &game, int state)
    63 {
    64     game.setState(state);
    65 }
    67 void UiAuditAccess::prepareTellHouse(cGame &game, int house)
    68 {
    69     game.prepareMentatToTellAboutHouse(house);
    70 }
    72 bool UiAuditAccess::mentatFreeze(cGame &game, bool awaiting)
    73 {
    74     AbstractMentat *mentat = game.m_mentat;
    75     if (mentat == nullptr) {
    76         return false;
    77     }
    78     if (awaiting) {
    79         mentat->state = AWAITING_RESPONSE;
    80         return true;
    81     }
    82     int bestPair = 0;
    83     size_t bestLength = 0;
    84     for (int pair = 0; pair <= 8; pair += 2) {
    85         const size_t length = std::strlen(mentat->sentence[pair]) + std::strlen(mentat->sentence[pair + 1]);
    86         if (length > bestLength) {
    87             bestLength = length;
    88             bestPair = pair;
    89         }
    90     }
    91     mentat->iMentatSentence = bestPair;
    92     mentat->TIMER_Speaking = 1 << 20;
    93     mentat->state = SPEAKING;
    94     return bestLength > 0;
    95 }
    97 bool UiAuditAccess::prepareMentatScene(cGame &game, int house, int kind)
    98 {
    99     players[HUMAN].setHouse(house);
   100     game.m_region = 1;
   101     if (kind == 0) {
   102         game.setNextStateToTransitionTo(GAME_BRIEFING);
   103         game.transitionStateIfRequired();
   104     }
   105     else {
   106         game.setState(kind == 1 ? GAME_WINBRIEF : GAME_LOSEBRIEF);
   107         game.createAndPrepareMentatForHumanPlayer(true);
   108     }
   109     return game.m_mentat != nullptr;
   110 }
```

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '131,210p'
```

Вывод:

```text
   131 void UiAuditAccess::missionOutcome(cGame &game, bool victory)
   132 {
   133     game.m_missionWasWon = victory;
   134     game.setState(victory ? GAME_WINNING : GAME_LOSING);
   135     game.takeBackGroundScreen();
   136 }
   138 void UiAuditAccess::writeSaves(cGame &game)
   139 {
   140     std::string error;
   141     std::filesystem::create_directories("saves");
   142     SaveGameManager::saveGame(game, 1, "", error);
   143     SaveGameManager::saveGame(game, 2, "A very long save name used to check how the slot row fits", error);
   144     SaveGameManager::saveGame(game, 5, "Before the final attack", error);
   145     std::ofstream(SaveGameManager::slotPath(3), std::ios::binary) << "not a save file";
   146     std::filesystem::create_directories(SaveGameManager::slotPath(6));
   147 }
   149 bool UiAuditAccess::openMenuSaveDialog(cGame &game)
   150 {
   151     auto *menu = dynamic_cast<cMainMenuState *>(game.m_currentState);
   152     if (menu == nullptr || menu->m_saveDialog == nullptr) {
   153         return false;
   154     }
   155     menu->m_saveDialog->open(false, false);
   156     return true;
   157 }
   159 bool UiAuditAccess::saveDialog(cGame &game, int action)
   160 {
   161     auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   162     if (options == nullptr || options->m_saveDialog == nullptr) {
   163         return false;
   164     }
   165     SaveSlotsDialog &dialog = *options->m_saveDialog;
   166     dialog.open(true, action == 1 || action == 2 || action == 4);
   167     if (action == 2) {
   168         dialog.selectSlot(2);
   169     }
   170     else if (action == 3) {
   171         dialog.selectSlot(3);
   172         dialog.loadSelected();
   173     }
   174     else if (action == 4) {
   175         dialog.selectSlot(6);
   176         dialog.saveSelected();
   177     }
   178     return true;
   179 }
   181 bool UiAuditAccess::optionsPage(cGame &game, int page)
   182 {
   183     auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   184     if (options == nullptr) {
   185         return false;
   186     }
   187     options->switchOptionsPage(static_cast<cOptionsState::OptionsPage>(page));
   188     return true;
   189 }
   191 bool UiAuditAccess::optionsBinding(cGame &game)
   192 {
   193     auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   194     if (options == nullptr) {
   195         return false;
   196     }
   197     options->m_bindingCapture = CommandBindingAction::Attack;
   198     options->refresh();
   199     return true;
   200 }
   202 bool UiAuditAccess::optionsStatus(cGame &game)
   203 {
   204     auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   205     if (options == nullptr || options->m_displayStatusLabel == nullptr) {
   206         return false;
   207     }
   208     options->m_displayStatusLabel->setText(
   209         localization::text("Saved. Restart the game.", "Сохранено. Перезапустите игру."));
   210     return true;
```

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '213,350p'
```

Вывод:

```text
   213 bool UiAuditAccess::creditsScroll(cGame &game, int frame)
   214 {
   215     auto *credits = dynamic_cast<cCreditsState *>(game.m_currentState);
   216     if (credits == nullptr) {
   217         return false;
   218     }
   219     credits->m_moveSpeed = 0;
   220     if (frame == 0) {
   221         credits->m_crawlerY = 64;
   222         return true;
   223     }
   224     const int fontHeight = credits->m_textDrawer->getFontHeight();
   225     const int limit = game.m_screenH - 128;
   226 ...
   260 ...
   261 void UiAuditAccess::recordCreditLines(cGame &game)
   262 {
   263     auto *credits = dynamic_cast<cCreditsState *>(game.m_currentState);
   264     if (credits == nullptr) {
   265         return;
   266     }
   267     for (const s_CreditLine &line : credits->m_lines) {
   268         if (!line.name.empty() || !line.txt.empty()) {
   269             uiaudit::recordCreditLine(line.name, line.txt);
   270         }
   271     }
   272 }
   274 void UiAuditAccess::regionOpen(cGame &game, int mission, bool jump)
   275 {
   276     if (jump) {
   277         game.jumpToSelectYourNextConquestMission(mission);
   278     }
   279     else {
   280         game.m_mission = mission;
   281     }
   282     game.setState(GAME_REGION);
   283 }
   285 int UiAuditAccess::regionState(const cGame &game)
   286 {
   287     auto *region = dynamic_cast<const cSelectYourNextConquestState *>(game.m_currentState);
   288     return region == nullptr ? -1 : static_cast<int>(region->state);
   289 }
   291 int UiAuditAccess::regionScene(const cGame &game)
   292 {
   293     auto *region = dynamic_cast<const cSelectYourNextConquestState *>(game.m_currentState);
   294     return region == nullptr ? -1 : static_cast<int>(region->regionSceneState);
   295 }
   297 int UiAuditAccess::regionSceneAlpha(const cGame &game)
   298 {
   299     auto *region = dynamic_cast<const cSelectYourNextConquestState *>(game.m_currentState);
   300     return region == nullptr ? -1 : region->iRegionSceneAlpha;
   301 }
   303 void UiAuditAccess::freezeClock(cGame &game)
   304 {
   305     game.m_timeManager->onWindowFocusLost();
   306 }
   308 void UiAuditAccess::resumeClock(cGame &game)
   309 {
   310     game.m_timeManager->onWindowFocusGained();
   311 }
   313 void UiAuditAccess::stopCameraEdgeMove()
   314 {
   315     if (mapCamera != nullptr) {
   316         mapCamera->m_cameraEdgeMove = false;
   317         mapCamera->m_moveX = 0.0f;
   318         mapCamera->m_moveY = 0.0f;
   319     }
   320 }
   322 void UiAuditAccess::clearMouseClicks(cGame &game)
   323 {
   324     game.m_mouse->leftButtonClicked = false;
   325     game.m_mouse->rightButtonClicked = false;
   326 }
   328 int UiAuditAccess::renderScale(const cGame &game)
   329 {
   330     return game.m_renderScalePercent;
   331 }
   333 int UiAuditAccess::worldScale(const cGame &game)
   334 {
   335     return game.m_worldScalePercent;
   336 }
   338 bool UiAuditAccess::mapViewport(const cGame &game, int &x, int &y, int &w, int &h)
   339 {
   340     if (game.m_mapViewport == nullptr) {
   341         return false;
   342     }
   343     x = game.m_mapViewport->getX();
   344     y = game.m_mapViewport->getY();
   345     w = game.m_mapViewport->getWidth();
   346     h = game.m_mapViewport->getHeight();
   347     return true;
   348 }
```

Это выдержка из вывода команды; промежуточные строки прокрутки титров опущены.

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '350,425p'
```

Выдержка из вывода:

```text
   350 void UiAuditAccess::recordSidebarClicks(cSideBarDrawer &drawer)
   352     cSideBar *sidebar = drawer.m_sidebar;
   353     if (sidebar == nullptr) {
   354         return;
   355     }
   356     const int selected = sidebar->getSelectedListID();
   357     for (int i = eListTypeAsInt(eListType::LIST_CONSTYARD); i < cSideBar::LIST_MAX; i++) {
   365         uiaudit::recordClick(("list-button:" + std::to_string(i)).c_str(),
   366                              list->getButtonDrawX(), list->getButtonDrawY(),
   367                              list->getButtonWidth(), list->getButtonHeight());
   370     if (selected >= 0 && selected < cSideBar::LIST_MAX) {
   373             cBuildingListDrawer &items = drawer.m_buildingListDrawer;
   374             const HudLayout layout = items.getLayout(list);
   375             const int scrollRow = items.getScrollRow(list);
   376             for (int i = 0; i < list->getItemCount(); ++i) {
   380                 const cRectangle card = layout.cardRect(i, scrollRow);
   384                 uiaudit::recordClick(("build-item:" + std::to_string(i)).c_str(),
   385                                      card.getX(), card.getY(), card.getWidth(), card.getHeight());
   387             uiaudit::recordClick("build-scrollbar", layout.scrollbar.getX(), layout.scrollbar.getY(),
   388                                  layout.scrollbar.getWidth(), layout.scrollbar.getHeight());
   392     cBuildingList *selectedList = selected >= 0 && selected < cSideBar::LIST_MAX ? sidebar->getList(selected) : nullptr;
   393     const bool starportOrdering = selectedList != nullptr && selectedList->isAvailable() &&
   394                                   selectedList->getType() == eListType::LIST_STARPORT;
   395     if (starportOrdering && drawManager != nullptr && drawManager->getOrderDrawer() != nullptr) {
   396         const cRectangle &rect = drawManager->getOrderDrawer()->m_buttonRect;
   397         uiaudit::recordClick("order-button", rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight());
   398     }
   401 void UiAuditAccess::recordCommandBarClicks(cCommandBarDrawer &drawer)
   403     for (const auto &button : drawer.m_buttons) {
   404         if (!button.enabled) {
   405             continue;
   406         }
   407         uiaudit::recordClick(("command:" + button.label).c_str(),
   408                              button.rect.getX(), button.rect.getY(), button.rect.getWidth(), button.rect.getHeight());
   410 }
```

Команда чтения параметров командной строки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp | nl -ba
```

Выдержка из вывода:

```text
     7 bool g_enabled = false;
    13 const Options &options()
    14 {
    15     return s_options;
    16 }
    18 void consumeArguments(int &argc, char **argv)
    19 {
    20     s_options = Options{};
    21     int kept = 1;
    22     for (int i = 1; i < argc; i++) {
    23         if (std::strcmp(argv[i], "--ui-audit-list") == 0) {
    24             s_options.list = true;
    26         else if (std::strcmp(argv[i], "--ui-audit-scales") == 0 && i + 1 < argc) {
    27             s_options.scales = argv[++i];
    29         else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {
    30             s_options.scene = argv[++i];
    32         else if (std::strcmp(argv[i], "--ui-audit-out") == 0 && i + 1 < argc) {
    33             s_options.outDir = argv[++i];
    35         else {
    36             argv[kept++] = argv[i];
    37         }
    39     for (int i = kept; i < argc; i++) {
    40         argv[i] = nullptr;
    41     }
    42     argc = kept;
    43     g_enabled = s_options.list || !s_options.scales.empty() || (!s_options.scene.empty() && !s_options.outDir.empty());
    44 }
```

## 4. Включение режима и выходные файлы

Аргументы режима разбираются только в `src/debug/UiAuditArguments.cpp@9208dcf:18-44`. Полный поиск в исходниках показывает ровно четыре строки разбора флагов `--ui-audit-*`; отдельной строки справки для них нет:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -- '--ui-audit-' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:23:        if (std::strcmp(argv[i], "--ui-audit-list") == 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:26:        else if (std::strcmp(argv[i], "--ui-audit-scales") == 0 && i + 1 < argc) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:29:        else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:32:        else if (std::strcmp(argv[i], "--ui-audit-out") == 0 && i + 1 < argc) {
```

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E -- '--ui-audit-(list|scales|scene|out)|ui-audit:|ui.audit' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug src/main.cpp
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:23:        if (std::strcmp(argv[i], "--ui-audit-list") == 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:26:        else if (std::strcmp(argv[i], "--ui-audit-scales") == 0 && i + 1 < argc) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:29:        else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp:32:        else if (std::strcmp(argv[i], "--ui-audit-out") == 0 && i + 1 < argc) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:142:    std::cerr << "ui-audit: " << message << '\n';
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:375:            std::cerr << "ui-audit: bad resolution " << options().scales << '\n';
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:417:        std::cerr << "ui-audit: unknown scene " << options().scene << '\n';
```

Переменных среды в `src` поиск не нашёл:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'getenv|SDL_getenv' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
```

Вывод команды пустой. Разбор ключей `settings.ini` в `consumeArguments` отсутствует: функция проходит `argv`, удаляет распознанные аргументы и активирует режим по `list`, непустой строке `scales` или паре `scene/outDir` (`src/debug/UiAuditArguments.cpp@9208dcf:18-44`).

Пути и форматы снимка записаны в `entry.tsv`. Команда создания файлов и геометрии:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | nl -ba | sed -n '155,261p'
```

Релевантная выдержка из вывода:

```text
   155 bool writeGeometry(cGame &game, const std::filesystem::path &path, int outputW, int outputH)
   157     std::ofstream file(path, std::ios::binary);
   161     file << "{\"k\":\"header\",\"scene\":\"" << escapeJson(g_scene->id) << "\",\"resolution\":\"" << outputW << 'x'
   162          << outputH << "\",\"language\":\"" << (localization::isEnglish() ? "en" : "ru") << "\",\"graphics\":\"hd\",\"canvas\":{\"w\":" << game.m_screenW
   163          << ",\"h\":" << game.m_screenH << "},\"game_screen\":" << (g_scene->gameScreen ? "true" : "false")
   164          << ",\"render_scale\":" << UiAuditAccess::renderScale(game)
   165          << ",\"world_scale\":" << UiAuditAccess::worldScale(game);
   170     if (g_scene->gameScreen && UiAuditAccess::mapViewport(game, viewX, viewY, viewW, viewH)) {
   171         file << ",\"map_viewport\":{" << rectJson({viewX, viewY, viewW, viewH}) << '}';
   173     file << ",\"version\":\"" << escapeJson(D2TM_VERSION) << "\"}\n";
   174     for (const Entry &entry : g_entries) {
   177                 file << "{\"k\":\"text\",\"s\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
   178                      << ",\"box\":";
   187                 file << "{\"k\":\"gui\",\"t\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
   191                 file << "{\"k\":\"area\",\"n\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
   195                 file << "{\"k\":\"label\",\"kind\":\"" << escapeJson(entry.label) << "\",\"obj\":" << entry.obj
   196                      << ",\"type\":\"" << escapeJson(entry.name) << "\"," << rectJson(entry.rect)
   197                      << ",\"owner\":{" << rectJson(entry.box) << "}}\n";
   200                 file << "{\"k\":\"click\",\"name\":\"" << escapeJson(entry.label) << "\"," << rectJson(entry.rect)
   204                 file << "{\"k\":\"credit\",\"name\":\"" << escapeJson(entry.name) << "\",\"s\":\""
   205                      << escapeJson(entry.label) << "\"}\n";
   213 bool writePng(SDL_Renderer *renderer, const std::filesystem::path &path, int &outputW, int &outputH)
   227             ok = IMG_SavePNG(surface, path.string().c_str()) == 0;
   235 void capture(cGame &game)
   238     const fs::path outDir(options().outDir);
   240     fs::create_directories(outDir, error);
   247     const fs::path png = outDir / (std::string(g_scene->id) + ".png");
   248     if (!writePng(UiAuditAccess::renderer(game), png, outputW, outputH)) {
   255     const fs::path log = outDir / (std::string(g_scene->id) + ".geometry.jsonl");
   256     if (!writeGeometry(game, log, outputW, outputH)) {
```

Функция `fail` выводит диагностику в stderr (`src/debug/UiAuditCapture.cpp@9208dcf:140-144`); отдельный файл журнала в этой функции захвата не открывается. Данные каталога и разрешений выдаются в stdout при раннем выходе (`src/debug/UiAuditCapture.cpp@9208dcf:369-421`). Пути тестовых игровых сохранений следуют из вызовов `writeSaves` (`src/debug/UiAuditAccess.cpp@9208dcf:138-147`) и формата слотов (`src/save/SaveGameManager.cpp@9208dcf:1349-1358`).

Команда и вывод для путей сохранений:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.cpp | nl -ba | sed -n '1349,1359p'
```

```text
  1349 std::filesystem::path SaveGameManager::slotPath(int slot)
  1350 {
  1351     if (!save_slot::isValidSlot(slot)) {
  1352         return {};
  1353     }
  1354     if (slot == 1) {
  1355         return std::filesystem::path("saves") / "quicksave.d2s";
  1356     }
  1357     return std::filesystem::path("saves") /
  1358            std::format("save{:02}.d2s", slot);
  1359 }
```

Команда и вывод мест вызова режима из `src/main.cpp`:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'uiaudit::|UiAudit|ui-audit' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/main.cpp src/cGame_logic.cpp
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:12:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:771:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:772:            uiaudit::beginFrame(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:780:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:781:            uiaudit::onFramePresented(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:25:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:86:    uiaudit::consumeArguments(argc, argv);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:88:    if (uiaudit::isEnabled() && uiaudit::handleEarlyExit(uiAuditExitCode)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:114:            if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:115:                uiaudit::onSetupDone(game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:132:    if (uiaudit::isEnabled() && (uiAuditError || uiaudit::failed())) {
```

Команда чтения аргументов игрового цикла:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '760,786p'
```

Выдержка из вывода:

```text
   764 const bool hdPresentationFrame = useHdPresentation();
   768 renderDrawer->beginDrawingToTexture(frameTarget);
   769 SDL_RenderSetLogicalSize(renderer, m_screenW, m_screenH);
   770 renderDrawer->renderClearToColor();
   771 if (uiaudit::isEnabled()) {
   772     uiaudit::beginFrame(*this);
   773 }
   774 drawState();
   775 transitionStateIfRequired();
   778 renderDrawer->endDrawingToTexture();
   779 presentFrame(frameTarget, hdPresentationFrame);
   780 if (uiaudit::isEnabled()) {
   781     uiaudit::onFramePresented(*this);
   782 }
```

В `PORT` таблица разбора — `cHandleArgument::optionStrings` в `src/utils/cHandleArgument.cpp@7eb119b:21-43`; функция — `handleArguments` в строках 45–136. В таблице 21 запись. Команда счёта вывела:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/utils/cHandleArgument.cpp | sed -n '21,43p' | grep -c '^[[:space:]]*{"'
```

```text
21
```

Команда с началом и концом определения функции разбора в `PORT`:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/utils/cHandleArgument.cpp | nl -ba | sed -n '45,70p;121,136p'
```

Вывод:

```text
    45 int cHandleArgument::handleArguments(int argc, char *argv[], InitialGameSettings *settings)
    46 {
    47     if (argc < 2) {
    48         return 0;
    49     }
    51     for (int i = 1; i < argc; i++) {
    52         std::string command = argv[i];
    53         auto itr = optionStrings.find(command);
    54         if (itr == optionStrings.end()) {
    55             std::cerr << "Unknown option " << command << ", use --help for instructions\n";
    56             throw std::runtime_error(std::format("invokes game with unknown option {}",command));
    59         switch (itr->second) {
    60             case Options::HELP:
    61                 printInstructions();
    62                 return HELP_REQUESTED;
    63             case Options::GAME:
    64                 if ((i + 1) < argc) {
    65                     i++;
    66                     settings->gameFilename = std::string(argv[i]);
    67                 } else {
    68                     throw std::runtime_error("invokes game but no value assigned");
    69                 }
    70                 break;
   121             case Options::USAGES:
   122                 settings->drawUsages = true;
   123                 break;
   124             case Options::PAUSE_WHEN_LOSING_FOCUS:
   125                 settings->pauseWhenLosingFocus = true;
   126                 break;
   127             case Options::FOG_OF_WAR:
   128                 settings->fogOfWarEnabled = true;
   129                 break;
   130             case Options::PREFERENCES:
   131                 // main loads the preferences before it handles the other arguments, so those win
   132                 break;
   133         }
   134     }
   135     return 0;
   136 }
```

Вызов разбора аргументов в `src/main.cpp@7eb119b:94` находится после загрузки `settings.ini` и пользовательских preferences. Команда и вывод:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/main.cpp | nl -ba | sed -n '91,107p'
```

```text
    91 // read command-line arguments, can override settings.ini
    92 cHandleArgument handleArg;
    93 try {
    94     int parseResult = handleArg.handleArguments(argc, argv, settings.get());
    95     if (parseResult == cHandleArgument::HELP_REQUESTED) {
    96         return 0;
    97     }
    98     if (parseResult < 0) {
    99         m_log->error(COMP_GAMERULES, "HandleArgument", "Incorrect arguments");
   100         return 1;
   101     }
   102 }
   103 catch (std::runtime_error &e) {
   104     m_log->error(eLogComponent::COMP_GAMERULES, "HandleArgument", "Runtime_error on parsing : {}", e.what());
   105     std::cerr << std::format("Error: {}\n\n", e.what());
   106     return 1;
   107 }
```
