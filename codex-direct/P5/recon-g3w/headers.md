### src/game/MissionFlow.hpp@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/MissionFlow.hpp | nl -ba
```

Вывод:
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

### src/game/GameStateTransition.hpp@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/GameStateTransition.hpp | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file GameStateTransition.hpp
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
    21	class GameStateTransition {
    22	public:
    23	    using TransitionCallback = std::function<void(int)>;
    24	    using FadeCallback = std::function<void()>;
    25	    using CurrentStateCallback = std::function<int()>;
    26	
    27	    GameStateTransition(TransitionCallback setNextState, TransitionCallback setNextStateWithFade, FadeCallback fadeOut, CurrentStateCallback getCurrentState)
    28	        : m_setNextState(std::move(setNextState)),
    29	          m_setNextStateWithFade(std::move(setNextStateWithFade)),
    30	          m_fadeOut(std::move(fadeOut)),
    31	          m_getCurrentState(std::move(getCurrentState)) {
    32	    }
    33	
    34	    void setNextState(int state) const {
    35	        m_setNextState(state);
    36	    }
    37	
    38	    void setNextStateWithFade(int state) const {
    39	        m_setNextStateWithFade(state);
    40	    }
    41	
    42	    void fadeOut() const {
    43	        m_fadeOut();
    44	    }
    45	
    46	    int getCurrentState() const {
    47	        return m_getCurrentState();
    48	    }
    49	
    50	private:
    51	    TransitionCallback m_setNextState;
    52	    TransitionCallback m_setNextStateWithFade;
    53	    FadeCallback m_fadeOut;
    54	    CurrentStateCallback m_getCurrentState;
    55	};
```

### src/game/ScenarioFlow.hpp@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/ScenarioFlow.hpp | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file ScenarioFlow.hpp
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
    21	class cPlayer;
    22	
    23	/**
    24	 * Narrow entry point to setting up a scenario (players, map, controlled player).
    25	 * Holds callbacks so it does not depend on cGame.
    26	 */
    27	class ScenarioFlow {
    28	public:
    29	    using Callback = std::function<void()>;
    30	    using IntCallback = std::function<void(int)>;
    31	    using PlayerCallback = std::function<void(cPlayer*)>;
    32	
    33	    ScenarioFlow(Callback setupPlayers, Callback loadScenario, IntCallback loadMapFromEditor, PlayerCallback setPlayerToInteractFor)
    34	        : m_setupPlayers(std::move(setupPlayers)),
    35	          m_loadScenario(std::move(loadScenario)),
    36	          m_loadMapFromEditor(std::move(loadMapFromEditor)),
    37	          m_setPlayerToInteractFor(std::move(setPlayerToInteractFor)) {
    38	    }
    39	
    40	    void setupPlayers() const {
    41	        m_setupPlayers();
    42	    }
    43	
    44	    void loadScenario() const {
    45	        m_loadScenario();
    46	    }
    47	
    48	    void loadMapFromEditor(int iSkirmishMap) const {
    49	        m_loadMapFromEditor(iSkirmishMap);
    50	    }
    51	
    52	    void setPlayerToInteractFor(cPlayer* player) const {
    53	        m_setPlayerToInteractFor(player);
    54	    }
    55	
    56	private:
    57	    Callback m_setupPlayers;
    58	    Callback m_loadScenario;
    59	    IntCallback m_loadMapFromEditor;
    60	    PlayerCallback m_setPlayerToInteractFor;
    61	};
```

### src/gameobjects/structures/cAbstractStructure.h@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cAbstractStructure.h
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
    18	class cFlag;
    19	#include "include/enums/ListEnums.h"
    20	#include "observers/cScenarioObserver.h"
    21	#include "gameobjects/structures/cStructureInfo.h"
    22	#include "include/enums/BuildEnums.h"
    23	#include "utils/cRectangle.h"
    24	
    25	#include <vector>
    26	#include <string>
    27	
    28	class cPlayer;
    29	class Texture;
    30	class cGameObjectContext;
    31	class cInfoContext;
    32	class cMapCamera;
    33	class cEventEmitter;
    34	class cScreenShake;
    35	class AudioContext;
    36	class cGameSettings;
    37	struct sGameServices;
    38	class SDLDrawer;
    39	
    40	class cAbstractStructure : public cScenarioObserver {
    41	
    42	private:
    43	    int armor;			// armor
    44	
    45	    int iHitPoints;     // HitPoints this structure has
    46	
    47	    int iCell;          // What cell it is (most upper left part of structure where drawing starts)
    48	
    49	    int iRallyPoint;    // rallypoint ...
    50	
    51	    bool bAnimate;      // Do its special animation? (unit leaving building, starport dropping something, etc)
    52	
    53	    bool dead;		    // set to true when die() is called, and thus this structure can be deleted.
    54	
    55	    int posX, posY;     // structures do not move, so these are calculated once and then simply returned.
    56	
    57	    int iUnitIDWithinStructure;        // >-1 means ID to unit that 'occupies' the building (ie, a harvester, or a unit to repair)
    58	
    59	    int iUnitIDEnteringStructure;      // >-1 means ID to unit that is entering this structure (it is in the process of occupying a cell of the structure)
    60	
    61	    int iUnitIDHeadingForStructure;    // >-1 means ID to unit that heads for this structure
    62	
    63	protected:
    64	    cGameObjectContext *m_objects = nullptr;
    65	    cInfoContext *m_info = nullptr;
    66	    cMapCamera *m_mapCamera = nullptr;
    67	    cGameSettings *m_settings = nullptr;
    68	    cEventEmitter *m_eventEmitter = nullptr;
    69	    cScreenShake *m_screenShake = nullptr;
    70	    AudioContext *m_audioContext = nullptr;
    71	    SDLDrawer *m_renderer = nullptr;
    72	
    73	    bool shouldAnimateWhenUnitHeadsTowardsStructure;
    74	    int id;				// the id within the structure[] array
    75	
    76	    int iWidth;			// width in cells (set by factory)
    77	    int iHeight;		// height in cells (set by factory)
    78	
    79	    int iFrame;         // Frame for animation (flag and other)
    80	
    81	    int iPlayer;        // owner
    82	
    83	    int iBuildFase;		// Building animation fases
    84	
    85	    // Repairing stuff
    86	    bool bRepair;       // repairing? (using timer + gives animation)
    87	
    88	    int frames;         // amount of frames to iterate over in default/flag mode (old behavior, default = 1)
    89	
    90	    // flags, if any
    91	    std::vector<std::unique_ptr<cFlag>> flags;
    92	
    93	    // draw structure with shadow
    94	    void drawWithShadow();
    95	
    96	public:
    97	
    98	    // Constructor & Destructor:
    99	    cAbstractStructure(); // default constructor
   100	
   101	    virtual ~cAbstractStructure();
   102	
   103	    void serviceInit(sGameServices *services);
   104	
   105	    float fConcrete;     // how much concrete is *not* beneath this building (percentage)?
   106	    // meaning, when 0% , it is all concrete. But if 10%, it means 10% of the building
   107	    // is not covered.
   108	
   109	    int m_smokeParticlesCreated;
   110	
   111	    // TIMERS that all structures use
   112	    int TIMER_repair;   // repairing timer
   113	    int TIMER_flag;     // flag animation
   114	    int TIMER_reduceSmoke; // reduce smoke created counter
   115	
   116	    int TIMER_decay;   // damaging stuff
   117	    int TIMER_prebuild; // prebuild timer
   118	
   119	    // -------------
   120	
   121	
   122	    // Filled in by derived classes
   123	    virtual void thinkFast()=0;       // think fast (every 5ms)
   124	    virtual void thinkSlow()=0;       // think slow (every second)
   125	    virtual void think_animation()=0; // think animation stuff
   126	    virtual void think_guard();       // think guard stuff
   127	
   128	    virtual int getType() const = 0;		  // implementation gives type of structure
   129	    void think_prebuild();            // prebuild animation
   130	    void think_repair();              // repair thinking
   131	    void think_decay();              // think about damaging through time
   132	    void think_flag();				  // think method for flag animation
   133	
   134	    void drawFlags();                   // draw all flags
   135	    void addFlag(std::unique_ptr<cFlag> flag);
   136	
   137	    int getSmokeChance();             // probability to create smoke particle
   138	
   139	    void die(int originId = -1, eBuildType originType = eBuildType::UNKNOWN, int killingDamage = 0); // die
   140	
   141	    // drawing
   142	    int iDrawX();
   143	    int iDrawY();
   144	    cRectangle getDrawRectangle();
   145	
   146	    // Functionality
   147	    int getNonOccupiedCellAroundStructure();
   148	
   149	    /**
   150	     * Returns all (valid!) cells that are around a structure. This only checks if the cell is within the
   151	     * playable map boundaries, but does not check if cells are occupied.
   152	     * @return
   153	     */
   154	    std::vector<int> getCellsAroundStructure();
   155	    std::vector<int> getCellsOfStructure();
   156	
   157	    // getters
   158	
   159	    // convenience get method, which should eventually only be used in rare cases as all properties should be
   160	    // TODO: copied from this struct to this class, so each structure can change the properties without
   161	    // changing the entire game rules.
   162	    s_StructureInfo getStructureInfo() const;
   163	    cPlayer *getPlayer();
   164	
   165	    // Really sure you need this? You can use getPlayer() ?
   166	    int getPlayerId() const {
   167	        return iPlayer;
   168	    }
   169	
   170	    Texture *getBitmap();
   171	    Texture *getShadowBitmap();
   172	
   173	    int pos_x();
   174	    int pos_y();
   175	
   176	    bool isDead() {
   177	        return dead;    // if set, then it is eligible for cleanup
   178	    }
   179	
   180	    int getArmor() {
   181	        return armor;
   182	    }
   183	    int getWidth() {
   184	        return iWidth;
   185	    }
   186	    int getHeight() {
   187	        return iHeight;
   188	    }
   189	    int getWidthInPixels();
   190	    int getHeightInPixels();
   191	    int getHitPoints() const {
   192	        return iHitPoints;
   193	    }
   194	    int getCell() {
   195	        return iCell;
   196	    }
   197	    int getOwner() {
   198	        return iPlayer;    // return the player id who owns this structure
   199	    }
   200	    int getRallyPoint() {
   201	        return canHaveRallyPoint() ? iRallyPoint : -1;
   202	    }
   203	    int getFrame() {
   204	        return iFrame;
   205	    }
   206	
   207	    /**
   208	     * Returns the ID within the structures array
   209	     * @return
   210	     */
   211	    int getStructureId() {
   212	        return id;
   213	    }
   214	
   215	    int getMaxHP();
   216	    int getCaptureHP();
   217	    int getSight();
   218	    int getRange();
   219	    int getPercentageNotPaved();
   220	    int getPowerUsage();
   221	    int getBuildingFase() {
   222	        return iBuildFase;
   223	    }
   224	
   225	    bool isAnimating() {
   226	        return bAnimate;
   227	    }
   228	    bool isPrimary();
   229	    bool isRepairing() {
   230	        return bRepair;
   231	    }
   232	
   233	    bool hasUnitWithin() const {
   234	        return iUnitIDWithinStructure > -1;
   235	    }
   236	    int getUnitIdWithin() const {
   237	        return iUnitIDWithinStructure;
   238	    }
   239	    void setUnitIdWithin(int unitId);
   240	
   241	    bool hasUnitHeadingTowards() const {
   242	        return iUnitIDHeadingForStructure > -1;
   243	    }
   244	    int getUnitIdHeadingTowards() const {
   245	        return iUnitIDHeadingForStructure;
   246	    }
   247	    void setUnitIdHeadingTowards(int unitId);
   248	
   249	    bool hasUnitEntering() const {
   250	        return iUnitIDEnteringStructure > -1;
   251	    }
   252	    int getUnitIdEntering() const {
   253	        return iUnitIDEnteringStructure;
   254	    }
   255	    void setUnitIdEntering(int unitId);
   256	
   257	    bool isValid();
   258	    bool needPowerToWork() const {
   259	        return getStructureInfo().needPowerToWork;
   260	    }
   261	    bool canAttackAirUnits() const {
   262	        return getStructureInfo().canAttackAirUnits;
   263	    }
   264	    bool canAttackGroundUnits() const {
   265	        return getStructureInfo().canAttackGroundUnits;
   266	    }
   267	
   268	    void setHeight(int height);
   269	    void setWidth(int width);
   270	    void setHitPoints(int hp);
   271	    void setCell(int cell);
   272	    void setOwner(int player); // set owner (player id) of structure
   273	    void setRallyPoint(int cell); // set rally point of structure
   274	    void setAnimating(bool value); // set animation on / off
   275	    virtual void startAnimating() = 0;
   276	    virtual void draw() = 0;
   277	    void setFrame(int frame);
   278	    void setStructureId(int theId) {
   279	        id = theId;
   280	    }
   281	    void setBuildingFase(int value) {
   282	        iBuildFase = value;
   283	    }
   284	    void setRepairing(bool value);
   285	
   286	    void damage(int hp, int originId, eBuildType originType = eBuildType::UNKNOWN);
   287	    void decay(int hp);
   288	    float getHealthNormalized() const;
   289	
   290	    bool isDamaged();
   291	
   292	    bool belongsTo(int playerId) const;
   293	    bool belongsTo(const cPlayer *other) const;
   294	
   295	    int getRandomPosX();
   296	    int getRandomPosY();
   297	
   298	    void getsCapturedBy(cPlayer *pPlayer);
   299	
   300	    void startRepairing();
   301	
   302	    void startEnteringStructure(int unitId);
   303	
   304	    void enterStructure(int unitId);
   305	
   306	    /**
   307	     * Makes current unitID within structure leave it, restoring it on the map next to a free cell.
   308	     * Making it also move to rally-point if set.
   309	     * @return
   310	     */
   311	    void unitLeavesStructure();
   312	
   313	    void unitHeadsTowardsStructure(int unitId);
   314	
   315	    int getRandomStructureCell();
   316	
   317	    bool isInProcessOfBeingEnteredOrOccupiedByUnit(int unitId);
   318	
   319	    void unitStopsHeadingTowardsStructure();
   320	
   321	    void unitStopsEnteringStructure();
   322	
   323	    void unitIsNoLongerInteractingWithStructure(int unitID);
   324	
   325	    void think_flag_new();
   326	
   327	    bool canSpawnUnits() const;
   328	
   329	    bool canHaveRallyPoint() const;
   330	
   331	    eListType getAssociatedListID() const;
   332	
   333	    std::string getDefaultStatusMessageBar() const;
   334	
   335	    virtual std::string getStatusForMessageBar() const = 0;
   336	
   337	};
```

### src/gameobjects/units/cUnit.h@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/units/cUnit.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cUnit.h
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
    19	#include "Facing.h"
    20	#include "include/cAssert.h"
    21	#include "include/enums/CombatEnums.h"
    22	#include "include/enums/BuildEnums.h"
    23	#include "gameobjects/units/cUnitInfos.h"
    24	#include "utils/cRectangle.h"
    25	#include "gameobjects/units/cTimer.h"
    26	
    27	#include <array>
    28	#include <memory>
    29	#include <string>
    30	
    31	static constexpr int MAX_PATH_SIZE = 512;
    32	static constexpr int MAX_WAYPOINTS_SIZE = 48;
    33	
    34	class cPlayer;
    35	class cAbstractStructure;
    36	struct sGameServices;
    37	
    38	class cGameSettings;
    39	class cInfoContext;
    40	class cGameObjectContext;
    41	class AudioContext;
    42	class cScreenShake;
    43	class cEventEmitter;
    44	class cMapCamera;
    45	class cMap;
    46	class cPathFinder;
    47	
    48	enum class eTransferType {
    49	    NONE,                               // nothing to transfer
    50	    NEW_STAY,                           // bring a new unit, and let the carryall stay
    51	    NEW_LEAVE,                          // bring a new unit, and let the carryall go back (and die)
    52	    PICKUP,                             // carry an existing unit, bring to new location
    53	    DIE,                                // will die when reaching goal-cell (added for proper animation)
    54	};
    55	
    56	enum class eActionType {
    57	    GUARD,                              // on guard (scanning for enemy activity)
    58	    MOVE,                               // moving
    59	    CHASE,                              // chasing a unit to attack
    60	    ATTACK_CHASE,                       // attacking (not moving), will chase when target is out of range
    61	    ATTACK,                             // attacking (not moving), will revert to GUARD when target is out of range
    62	};
    63	
    64	enum class eFindBestStructureResultReason {
    65	    FREE_STRUCTURE,                             // nobody is heading towards this structure, so we can freely occupy it
    66	    OTHER_UNIT_ALSO_HEADS_TOWARDS_STRUCTURE,    // the structure found is also being chased by another unit
    67	    OCCUPIED,                                   // structure is occupied (last resort, hoping it will become free soon)
    68	    NO_RESULT,                                  // nothing found...
    69	};
    70	
    71	/**
    72	 * A result when finding a best structure.
    73	 */
    74	struct sFindBestStructureResult {
    75	    cAbstractStructure *structure;
    76	    eFindBestStructureResultReason reason;
    77	};
    78	
    79	enum class eHeadTowardsStructureResult {
    80	    FAILED_NO_STRUCTURE_AVAILABLE,
    81	    SUCCESS_AWAITING_CARRYALL,
    82	    SUCCESS_RETURNING,
    83	    NOOP_ALREADY_BUSY,
    84	};
    85	
    86	
    87	inline std::string eActionTypeString(eActionType actionType)
    88	{
    89	    switch (actionType) {
    90	        case eActionType::GUARD:
    91	            return "GUARD";
    92	        case eActionType::ATTACK_CHASE:
    93	            return "ATTACK_CHASE";
    94	        case eActionType::ATTACK:
    95	            return "ATTACK";
    96	        case eActionType::MOVE:
    97	            return "MOVE";
    98	        case eActionType::CHASE:
    99	            return "CHASE";
   100	        default:
   101	            d2tm_assert(false);
   102	            break;
   103	    }
   104	    return "";
   105	}
   106	
   107	struct sMovement {
   108	    int iNextCell;      // where to move to (next cell)
   109	    int iGoalCell;      // the goal cell (goal of path)
   110	    int iPath[MAX_PATH_SIZE];    // path of unit
   111	    int waypointCells[MAX_WAYPOINTS_SIZE]; // the cells that are waypoints (ie, where unit needs to turn)
   112	    int iPathIndex;     // where are we?
   113	    int iPathFails;     // failed...
   114	    bool bCalculateNewPath;  // calculate new path?
   115	};
   116	
   117	struct sRendering {
   118	    Facing iBodyFacing;    // Body of tanks facing
   119	    Facing iHeadFacing;    // Head of tanks facing
   120	    Facing iBodyShouldFace;    // where should the unit body look at?
   121	    Facing iHeadShouldFace;    // where should the unit look at?
   122	    int iFrame;         // framed (animated stuff)
   123	    bool bHovered;      // mouse hovers over this unit or not?
   124	};
   125	
   126	struct sCombat {
   127	    int iAttackUnit;      // attacking unit id
   128	    int iAttackStructure; // attack structure id
   129	    int iAttackCell;      // attacking a cell (which is force attack)
   130	};
   131	
   132	class cPosition {
   133	public:
   134	    explicit cPosition(): iCell(0), iCellX(0), iCellY(0), posX(0), posY(0) {}
   135	private:
   136	    int iCell;          // cell of unit
   137	    int iCellX;         // my cell x
   138	    int iCellY;         // my cell y
   139	    // absolute x, y coordinates (pixel based). Do note, these are oriented at top left of cell, and
   140	    // thus are snapped to the grid.
   141	    float posX, posY;
   142	    friend class cUnit;
   143	};
   144	
   145	
   146	class cUnit {
   147	
   148	public:
   149	
   150	    cUnit();
   151	    ~cUnit();
   152	
   153	    void serviceInit(sGameServices* services);
   154	
   155	    float fExperience;	// experience gained by unit
   156	
   157	    int iID;            // index of unit in the unit array
   158	    int iType;          // type of unit
   159	    std::array<bool, MAX_UNIT_GROUPS> iGroups; // belongs to groups [0..MAX_UNIT_GROUPS-1]
   160	    int iPlayer;        // belongs to player
   161	
   162	    sMovement movement;
   163	
   164	    // carryall stuff
   165	    bool bCarryMe;		// carry this unit when moving it around?
   166	    int  iCarryAll;		// any carry-all that will pickup this unit... so this unit knows
   167	    // it should wait when moving, etc, etc
   168	
   169	    sCombat combat;
   170	
   171	    // Action given code
   172	    int iUnitID;        // Unit ID to attack/pickup, etc
   173	    int iStructureID;   // structure ID to attack/bring to (refinery)/capture
   174	
   175	    // Harvester specific
   176	    int iCredits;       // credits stored in this baby
   177	    int iHarvestCellMemory; // remembers the last spice cell this harvester was working on
   178	    bool m_stayAtGoalCell;  // ordered by the player to stop at a cell: a harvester does not look for spice by itself there
   179	
   180	    // Carry-All specific
   181	    // -1 = none, 0 = new (and stay), 1 = carrying existing unit , 2 = new (and leave)
   182	    // iUnitIDWithinStructure = unit we CARRY (when TransferType == 1)
   183	    // iTempHitPoints = hp of unit when transfertype = 1
   184	    eTransferType m_transferType;
   185	
   186	    int iBringTarget;	// Where to bring the carried unit (when iUnitIDWithinStructure > -1)
   187	    int iNewUnitType;	// new unit that will be brought, will be this type
   188	    int lastDroppedOffCell; // last cell where we dropepd off a unit
   189	
   190	    sRendering rendering;
   191	
   192	    void retreatToNearbyBase();
   193	    void retreatToMapEdge();
   194	    void deselect();
   195	    [[nodiscard]] bool isSelected() const;
   196	    void select();
   197	
   198	    float fExpDamage();	// experience damage by bullet (extra damage that is)
   199	
   200	    bool isWithinViewport(cRectangle *viewport) const;
   201	
   202	    // ------------
   203	    void init(int i);        // inits units
   204	
   205	    int draw_x();
   206	    int draw_x(int bmpWidth);
   207	    int draw_y();
   208	    int draw_y(int bmpHeight);
   209	
   210	    int pos_x();
   211	    int pos_y();
   212	
   213	    int pos_x_centered();
   214	    int pos_y_centered();
   215	
   216	    int center_draw_x();
   217	    int center_draw_y();
   218	
   219	    [[nodiscard]] cMapCamera *getMapCamera() const {
   220	        return m_mapCamera;
   221	    }
   222	
   223	    [[nodiscard]] bool isDrawUnitDebugEnabled() const;
   224	
   225	    [[nodiscard]] const cRectangle &getDimensions() const {
   226	        return dimensions;
   227	    }
   228	
   229	    [[nodiscard]] int getUnitsEaten() const {
   230	        return unitsEaten;
   231	    }
   232	
   233	    bool isValid() const;     // valid unit?
   234	
   235	    void shoot(int iTargetCell);  // shoot at goalcell
   236	    void revealWhenAttackingHumanUnitAt(int targetCell);
   237	
   238	    void die(bool bBlowUp, bool bSquish, int originId = -1, eBuildType originType = eBuildType::UNKNOWN, int killingDamage = 0); // die!
   239	
   240	    void updateCellXAndY();        // updateCellXAndY status
   241	
   242	    void think();
   243	
   244	    void thinkFast_move_airUnit();  // aircraft specific
   245	    void think_move_foot(); // soldiers specific
   246	    void thinkFast_move();  // thinking about movement (which is called upon a faster rate)
   247	    // for wheeled/tracked units
   248	    void think_attack();
   249	    void thinkFast_guard();
   250	
   251	    void log(const std::string &txt) const;
   252	
   253	    void think_hit(int iShotUnit, int iShotStructure);
   254	
   255	    int getNextCellToMoveTo(); // what is the next cell to move to
   256	
   257	    void move_to_enter_structure(cAbstractStructure *pStructure, eUnitActionIntent intent);
   258	    void move_to(int iGoalCell);
   259	    void move_to_and_stay(int iGoalCell); // player order: a harvester stays at the goal cell when it is not spice
   260	    void move_to(int iCll, int iStructureIdToEnter, int iUnitIdToPickup, eUnitActionIntent intent);
   261	    void move_to(int iCll, int iStructureIdToEnter, int iUnitIdToPickup);
   262	
   263	    /**
   264	     * Finds best structure type. This is based on distance and on availability.
   265	     *
   266	     * This function:
   267	     * - checks if there is any structure that no unit is heading towards to
   268	     * if failed:
   269	     * - checks if there is any structure with no unit in it
   270	     * if failed:
   271	     * - checks if there is any structure of structure type (closest)
   272	     *
   273	     * Returns pointer to found structure.
   274	     * @param structureType
   275	     * @return
   276	     */
   277	    sFindBestStructureResult findBestStructureCandidateToHeadTo(int structureType);
   278	
   279	    /**
   280	     * Finds structureType, and if found it will move unit towards it with the action intent given.
   281	     * If allowCarryallTransfer is given, this function will also check if there is a free carry-all and let the
   282	     * unit be transported via that way to the structure.
   283	     *
   284	     * Best structure candidate is based on distance towards unit. (closest == best)
   285	     *
   286	     * @param structureType
   287	     * @param allowCarryallTransfer
   288	     * @param actionIntent
   289	     * @return
   290	     */
   291	    eHeadTowardsStructureResult findBestStructureCandidateAndHeadTowardsItOrWait(int structureType, bool allowCarryallTransfer,
   292	            eUnitActionIntent actionIntent);
   293	
   294	    cAbstractStructure *findClosestAvailableStructureTypeWhereNoUnitIsHeadingTo(int structureType);
   295	    cAbstractStructure *findClosestAvailableStructureType(int structureType);
   296	    cAbstractStructure *findClosestStructureType(int structureType);
   297	
   298	    // carryall-functions:
   299	    void carryall_order(int iuID, eTransferType transferType, int iBring, int iTpe);
   300	
   301	    cTimer moveTimer;         // movement timer
   302	    cTimer movewaitTimer;     // wait for move think...
   303	    cTimer movedelayTimer;    // if given, it will delay movement
   304	    cTimer turnTimer;       // turning around
   305	    cTimer thinkwaitTimer;    // wait with normal thinking..
   306	    cTimer frameTimer;
   307	    cTimer harvestTimer;      // harvesting timer
   308	    cTimer guardTimer;        // guard scanning timer
   309	    cTimer boredTimer;        // how long are we bored?
   310	    cTimer attackTimer;       // when to shoot?
   311	    cTimer wormTrailTimer;    // when to spawn a trail when moving
   312	    cTimer revealTimer;       // think ticks left that this unit shows through the fog of war (it attacked a human unit)
   313	
   314	    s_UnitInfo &getUnitInfo() const;
   315	
   316	    /**
   317	     * Return current health normalized (between 0.0 and 1.0)
   318	     * @return
   319	     */
   320	    float getHealthNormalized();
   321	
   322	    /**
   323	     * Return temp health hitpoints normalized (between 0.0 and 1.0) (when unit is 'hidden')
   324	     * @return
   325	     */
   326	    float getTempHealthNormalized();
   327	
   328	    /**
   329	     * is this unit an airborn unit?
   330	     * @return
   331	     */
   332	    bool isAirbornUnit() const {
   333	        return getUnitInfo().airborn;
   334	    }
   335	
   336	    /**
   337	     * An air unit that may be attacked according to generic game rules, ie this does not say anything
   338	     * about if the unit *can* attack it. (use canAttackAirUnits function for that)
   339	     * @return
   340	     */
   341	    bool isAttackableAirUnit() {
   342	        return isType(ORNITHOPTER);
   343	    }
   344	
   345	    /**
   346	     * @deprecated
   347	     */
   348	    bool isHarvester() const {
   349	        return isType(HARVESTER);
   350	    }
   351	
   352	    bool isType(int value) const {
   353	        return iType == value;
   354	    }
   355	
   356	    /**
   357	     * @deprecated
   358	     */
   359	    bool isSandworm() const;
   360	    [[nodiscard]] bool isRevealedByAttack() const { return revealTimer.get() > 0; }
   361	
   362	    /**
   363	     * Can this unit attack air units?
   364	     * @return
   365	     */
   366	    bool canAttackAirUnits() {
   367	        return getUnitInfo().canAttackAirUnits;
   368	    }
   369	
   370	    /**
   371	     * Can this unit's weapon damage structures? (the Deviator cannot)
   372	     * @return
   373	     */
   374	    bool canDamageStructures() const {
   375	        return getUnitInfo().canDamageStructures;
   376	    }
   377	
   378	    bool isInfantryUnit() const;
   379	    bool isWheelUnit() const;
   380	    bool isTankUnit() const;
   381	    bool isLauncherUnit() const;
   382	
   383	    int getBmpWidth() const;
   384	
   385	    int getBmpHeight() const;
   386	
   387	    void recreateDimensions();
   388	
   389	    void thinkFast_position();
   390	
   391	    bool isMovingBetweenCells();
   392	
   393	    bool isIdle() {
   394	        return m_action == eActionType::GUARD;
   395	    }
   396	
   397	    void takeDamage(int damage, int unitWhoDealsDamage, int structureWhoDealsDamage);
   398	
   399	    void setHp(int hp) {
   400	        iHitPoints = hp;
   401	    }
   402	
   403	    bool isDead() {
   404	        return iHitPoints <= 0 && iTempHitPoints < 0;
   405	    }
   406	
   407	    bool isDamaged();
   408	
   409	    void restoreFromTempHitPoints();
   410	
   411	    void setMaxHitPoints();
   412	
   413	    void setCell(int cll);
   414	    int getCell() {
   415	        return position.iCell;
   416	    }
   417	    int getCellX() {
   418	        return position.iCellX;
   419	    }
   420	    int getCellY() {
   421	        return position.iCellY;
   422	    }
   423	    float getPosX() const { return position.posX; }
   424	    float getPosY() const { return position.posY; }
   425	
   426	    cPlayer *getPlayer();
   427	
   428	    void assignMission(int aMission);
   429	    void unAssignMission();
   430	    bool isAssignedAnyMission();
   431	    bool isAssignedMission(int aMission);
   432	
   433	    int getPlayerId() const;
   434	
   435	    /**
   436	     * Returns type of unit (ie QUAD, TANK, etc)
   437	     *
   438	     * @return
   439	     */
   440	    int getType() const;
   441	
   442	    static std::string eUnitActionIntentString(eUnitActionIntent intent);
   443	
   444	    bool isUnableToMove();
   445	
   446	    void attackUnit(int targetUnit);
   447	    void attackUnit(int targetUnit, bool chaseWhenOutOfRange);
   448	    void attackStructure(int targetStructure);
   449	    void attackCell(int cell);
   450	
   451	    /**
   452	     * Figures out if at cell is a unit, structure or nothing, and invokes the appropiate attackUnit/Structure/Cell function.
   453	     * Assumes unit should move closer (chase) to target
   454	     * @param cell
   455	     */
   456	    void attackAt(int cell);
   457	
   458	    /**
   459	     * Can squish infantry units
   460	     * @return
   461	     */
   462	    bool canSquishInfantry();
   463	
   464	    /**
   465	     * Returns true if this unit can be squished by other units
   466	     * @return
   467	     */
   468	    bool canBeSquished();
   469	
   470	    void carryAll_transferUnitTo(int unitIdToTransfer, int destinationCell);
   471	
   472	    void hideUnit();
   473	
   474	    void actionGuard();
   475	
   476	    bool belongsTo(const cPlayer *pPlayer) const;
   477	
   478	    bool isMarkedForRemoval();
   479	
   480	    void setBoundParticleId(int particleId);
   481	
   482	    int getHitPoints() {
   483	        return iHitPoints;
   484	    }
   485	
   486	    bool isEligibleForRepair();
   487	
   488	    void thinkFast();
   489	
   490	    bool isAttackingUnit();
   491	
   492	    std::string getUnitStatusForMessageBar();
   493	    std::string getHarvesterStatusForMessageBar();
   494	
   495	    bool isHidden();
   496	
   497	    bool isAlive() {
   498	        return isValid() && !isDead() && !isHidden();
   499	    }
   500	
   501	    bool requiresRepairing();
   502	
   503	    void repair(int hp);
   504	
   505	    bool canUnload();
   506	
   507	    static int findHarvestSpot(int id, cGameObjectContext* objects);
   508	    static int carryallTransfer(int iuID, int iGoal, cGameObjectContext* objects);
   509	    static int freeAroundMove(int iUnit, cGameObjectContext* objects);
   510	
   511	private:
   512	    cGameSettings *m_settings = nullptr;
   513	    cInfoContext *m_infos = nullptr;
   514	    cGameObjectContext *m_objects = nullptr;
   515	    AudioContext *m_audioContext = nullptr;
   516	    cScreenShake *m_screenShake = nullptr;
   517	    cEventEmitter *m_eventEmitter = nullptr;
   518	    cMapCamera* m_mapCamera = nullptr;
   519	    cMap* m_map = nullptr;
   520	    cPathFinder *m_pathFinder = nullptr;
   521	
   522	    eActionType m_action;
   523	    eUnitActionIntent intent;
   524	
   525	    int iTempHitPoints; // temp hold back for 'reinforced' / 'dumping' and 'repairing' units
   526	
   527	    int willBePickedUpBy;	// is unit picked up (by carry-all), if so by which one?
   528	    bool bPickedUp;     // did this unit pick up a unit? (this unit is a carry-all or frigate)
   529	
   530	    bool bRemoveMe; // if true, then this unit wants to be cleared (ie, is no longer valid)
   531	
   532	    int mission; // is this unit assigned to a mission?
   533	
   534	    int iHitPoints;     // hitpoints of unit
   535	
   536	    bool isReinforcement; // is this a 'real' reinforcement or not? (applies to Carry-All only)
   537	
   538	    int unitsEaten; // worm related
   539	
   540	    bool isSaboteur();
   541	    bool canAttackOnEnterStructure();
   542	
   543	    void forgetAboutCurrentPathAndPrepareToCreateNewOne(int timeToWait = 35);
   544	
   545	    void takeDamage(int damage);
   546	
   547	    bool m_bSelected;     // selected or not?
   548	
   549	    cPosition position;
   550	    void setPosX(float newVal);
   551	    void setPosY(float newVal);
   552	
   553	    int boundParticleId; // when a unit is damaged, it can spawn a particle on top of it (ie smoke)
   554	
   555	
   556	
   557	    eUnitMoveToCellResult moveToNextCellLogic();
   558	
   559	    cRectangle dimensions;
   560	
   561	    int getRange() const;
   562	
   563	    int getSight() const;
   564	
   565	    void think_turn_to_desired_body_facing();
   566	
   567	    void selectTargetForOrnithopter(cPlayer *pPlayer);
   568	
   569	    void think_carryAll();
   570	
   571	    void thinkActionAgnostic();       // thinking in general
   572	
   573	    Facing determineNewFacing(Facing currentFacing, Facing desiredFacing);
   574	
   575	    bool setAngleTowardsTargetAndFireBullets(int distance);
   576	
   577	    void startChasingTarget();
   578	
   579	    Facing getFaceAngleToCell(int cell) const;
   580	
   581	    void attack(int goalCell, int unitId, int structureId, int attackCell, bool chaseWhenOutOfRange);
   582	
   583	    int findNewDropLocation(int unitTypeToDrop, int cell) const;
   584	
   585	    /**
   586	     * Returns a pointer to a structure the unit wants to enter. If the unit wants to enter an invalid structure,
   587	     * this function will return nullptr.
   588	     * @return
   589	     */
   590	    cAbstractStructure *getStructureUnitWantsToEnter() const;
   591	
   592	    cUnit &getUnitToPickupOrDrop() const;
   593	
   594	    bool findAndOrderCarryAllToBringMeToStructureAtCell(cAbstractStructure *candidate, int destCell);
   595	
   596	    void awaitBeingPickedUpToBeTransferedByCarryAllToStructure(cAbstractStructure *candidate);
   597	
   598	    void unitWillNoLongerBeInteractingWithStructure() const;
   599	
   600	    void think_attack_sandworm();
   601	
   602	    void createExplosionParticle();
   603	
   604	    void createSquishedParticle();
   605	
   606	    void forgetAboutUnitToPickUp();
   607	
   608	    void tellCarryAllThatWouldPickMeUpToForgetAboutMe();
   609	
   610	    bool isAbleToGuard();
   611	
   612	    void thinkFast_guard_sandworm();
   613	
   614	    int findNearbyStructureToAttack(int range);
   615	
   616	    int findNearbyStructureThatCanDamageUnitsToAttack(int range);
   617	
   618	    int findNearbyGroundUnitToAttack(int range);
   619	
   620	    int findNearbyAirUnitToAttack(int range);
   621	
   622	
   623	    int getTurnSpeed();
   624	
   625	    void think_ornithopter();
   626	    void think_harvester();
   627	
   628	    void setAction(eActionType action);
   629	    void setGoalCell(int goalCell);
   630	
   631	    static int carryallFreeForTransfer(int iPlayer, cGameObjectContext* objects);
   632	};
```

### src/gameobjects/units/cUnits.h@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/units/cUnits.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cUnits.h
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
    19	#include "cUnit.h"
    20	
    21	struct sGameServices;
    22	class cInfoContext;
    23	class cGameObjectContext;
    24	class cEventEmitter;
    25	class cMap;
    26	class cLog;
    27	
    28	/**
    29	 * Manager class that encapsulates the global g_Unit array
    30	 * Provides safe access to units with bounds checking and convenient methods
    31	 */
    32	class cUnits {
    33	public:
    34	    /**
    35	     * Default constructor
    36	     */
    37	    cUnits();
    38	    void serviceInit(sGameServices* services);
    39	
    40	    /**
    41	     * Non-copyable
    42	     */
    43	    cUnits(const cUnits&) = delete;
    44	    cUnits& operator=(const cUnits&) = delete;
    45	
    46	    /**
    47	     * Access unit by index (compatible with array syntax)
    48	     */
    49	    cUnit* operator[](int index);
    50	    const cUnit* operator[](int index) const;
    51	
    52	    /**
    53	     * Safe access with bounds checking
    54	     * @param index The unit index
    55	     * @return Pointer to cUnit if valid, nullptr otherwise
    56	     */
    57	    cUnit* getUnit(int index);
    58	    const cUnit* getUnit(int index) const;
    59	
    60	    /**
    61	     * Shorthand for the "index > -1 and unit is valid" check
    62	     * @param index The unit index, -1 means no unit
    63	     * @return true when index refers to a valid unit
    64	     */
    65	    bool isValidUnit(int index) const;
    66	
    67	    /**
    68	     * Maximum number of units that can be in the game (the unit limit)
    69	     */
    70	    static constexpr int MAX_UNITS_CAPACITY = 300;
    71	
    72	    /**
    73	     * Extra slots on top of the unit limit (5% of it), used by carry-alls that are spawned to deliver a unit, but
    74	     * only when the regular slots are 90% used. The pool is shared by all players.
    75	     */
    76	    static constexpr int CARRYALL_RESERVE = MAX_UNITS_CAPACITY / 20;
    77	
    78	    /**
    79	     * Size of the unit array: the unit limit plus the carry-all reserve
    80	     */
    81	    static constexpr int TOTAL_SLOTS = MAX_UNITS_CAPACITY + CARRYALL_RESERVE;
    82	
    83	    /**
    84	     * Get the capacity (size of the unit array, including the carry-all reserve)
    85	     * @return The capacity
    86	     */
    87	    static constexpr int capacity() { return TOTAL_SLOTS; }
    88	
    89	    /**
    90	     * Get the number of units available (returns capacity)
    91	     * @return The size
    92	     */
    93	    static constexpr int size() { return TOTAL_SLOTS; }
    94	
    95	    /**
    96	     * Find the first available (invalid) unit slot (the carry-all reserve is not considered)
    97	     * @return Index of available unit, or -1 if none available
    98	     */
    99	    int findAvailableSlot() const;
   100	
   101	    /**
   102	     * All unit slots are in use, so no new unit can be created
   103	     * @return true when no slot is free
   104	     */
   105	    bool isUnitLimitReached() const { return findAvailableSlot() < 0; }
   106	
   107	    /**
   108	     * Count valid units
   109	     * @return Number of valid units
   110	     */
   111	    int getValidUnitsCount() const;
   112	
   113	    /**
   114	     * Begin iterator for range-based for loops
   115	     */
   116	    auto begin() { return m_units.begin(); }
   117	    auto begin() const { return m_units.begin(); }
   118	
   119	    /**
   120	     * End iterator for range-based for loops
   121	     */
   122	    auto end() { return m_units.end(); }
   123	    auto end() const { return m_units.end(); }
   124	
   125	    void move_to(int icell);
   126	
   127	    /**
   128	     * Creates a new unit, when bOnStart is true, it will prevent AI players from moving a unit immediately a bit.
   129	     * Assumes the creation of a unit is NOT a reinforcement.
   130	     *
   131	     * @param iCll
   132	     * @param unitType
   133	     * @param iPlayer
   134	     * @param bOnStart (if true, then AI will *not* move unit away immediately to a nearby random position)
   135	     * @return
   136	     */
   137	    // static int unitCreate(int iCll, int unitType, int iPlayer, bool bOnStart);
   138	    /**
   139	    * creates a unit, the isReinforcement flag is true when the unit is created for / by reinforcements. This
   140	    * flag will make sure to trigger a different event type (not CREATED, but REINFORCED) so that we can distinguish
   141	    * between them.
   142	    *
   143	    * @param iCll
   144	    * @param unitType
   145	    * @param iPlayer
   146	    * @param bOnStart
   147	    * @param isReinforcement
   148	    * @return
   149	    */
   150	    // static int unitCreate(int iCll, int unitType, int iPlayer, bool bOnStart, bool isReinforcement);
   151	    /**
   152	     * Creates a new unit, when bOnStart is true, it will prevent AI players from moving a unit immediately a bit.
   153	     *
   154	     *
   155	     * @param iCll
   156	     * @param unitType
   157	     * @param iPlayer
   158	     * @param bOnStart
   159	     * @param hpPercentage multiplies with hp of unit type for starting hp. 1.0 means 100% health
   160	     * @param isReinforement flag to set on event
   161	     * @param canUseCarryAllReserve when true, the unit may use the carry-all reserve slots once the regular slots are 90% used (for spawned carry-alls)
   162	     * @return
   163	     */
   164	    static int unitCreate(cGameObjectContext* objects, cInfoContext* infos, cEventEmitter* eventEmitter, int iCll, int unitType, int iPlayer, bool bOnStart, bool isReinforcement = false, float hpPercentage = 1.0f, bool canUseCarryAllReserve = false);
   165	
   166	
   167	private:
   168	    cInfoContext *m_infos = nullptr;
   169	    cGameObjectContext *m_objects = nullptr;
   170	    cMap* m_map = nullptr;
   171	    std::array<cUnit, TOTAL_SLOTS> m_units;
   172	};
```

### src/controls/cGameControlsContext.h@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cGameControlsContext.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cGameControlsContext.h
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
    20	// this class holds the game controls context. This means, the updateMouseAndKeyboardStateAndGamePlaying() method
    21	// will check how the mouse is positioned in this particular frame. It then updates any ids, or other relevant data.
    22	//
    23	// For instance, this class knows if a mouse is hovering above a structure, or a unit. The sidebar
    24	// or above the minimap. It also knows if an order has been issued (attack, move, repair, etc).
    25	//
    26	// a context belongs to a player
    27	
    28	#include "controls/mousestates/eMouseStates.h"
    29	#include "controls/cMouse.h"
    30	#include "observers/cInputObserver.h"
    31	#include "observers/cScenarioObserver.h"
    32	
    33	// Forward declarations for mouse states
    34	class cMouseNormalState;
    35	class cMouseUnitsSelectedState;
    36	class cMouseRepairState;
    37	class cMousePlaceState;
    38	class cMouseDeployState;
    39	
    40	class cAbstractStructure;
    41	class cGameObjectContext;
    42	class cMapCamera;
    43	class cGameSettings;
    44	class cDrawManager;
    45	class cRectangle;
    46	class cEventEmitter;
    47	class cStructureUtils;
    48	class cInfoContext;
    49	class AudioContext;
    50	struct sGameServices;
    51	
    52	class cGameControlsContext : public cInputObserver, cScenarioObserver {
    53	public:
    54	    explicit cGameControlsContext(cPlayer *player, cMouse *mouse);
    55	    ~cGameControlsContext() override;
    56	
    57	    void serviceInit(sGameServices *services);
    58	
    59	    cGameObjectContext *getObjects() const { return m_objects; }
    60	    cMapCamera *getMapCamera() const { return m_mapCamera; }
    61	    cGameSettings *getSettings() const { return m_settings; }
    62	    cDrawManager *getDrawManager() const { return m_drawManager; }
    63	    cEventEmitter *getEventEmitter() const { return m_eventEmitter; }
    64	    cStructureUtils *getStructureUtils() const { return m_structureUtils; }
    65	    cInfoContext *getInfos() const { return m_infos; }
    66	    AudioContext *getAudioContext() const { return m_audioContext; }
    67	    cRectangle *getMapViewport() const { return m_mapViewport; }
    68	
    69	    int getIdOfStructureWhereMouseHovers() const {
    70	        return m_mouseHoveringOverStructureId;
    71	    }
    72	    int getIdOfUnitWhereMouseHovers() const {
    73	        return m_mouseHoveringOverUnitId;
    74	    }
    75	
    76	    int getMouseCell() const {
    77	        return m_mouseCell;
    78	    }
    79	    int getMouseCellClamped() const {
    80	        return m_mouseCellClamped;
    81	    }
    82	
    83	    bool isMouseOverStructure() const {
    84	        return m_mouseHoveringOverStructureId > -1;
    85	    }
    86	    bool isMouseOverUnit() const {
    87	        return m_mouseHoveringOverUnitId > -1;
    88	    }
    89	
    90	    bool isMouseOnSidebar() const {
    91	        return m_mouseCell == MOUSE_CELL_HOVER_SIDEBAR;
    92	    }
    93	    bool isMouseOnTopBar() const {
    94	        return m_mouseCell == MOUSE_CELL_HOVER_TOPBAR;
    95	    }
    96	    bool isMouseOnMiniMap() const {
    97	        return m_mouseCell == MOUSE_CELL_HOVER_MINIMAP;
    98	    }
    99	    bool isMouseOnSidebarOrMinimap() const {
   100	        return isMouseOnSidebar() || isMouseOnMiniMap();
   101	    }
   102	
   103	    bool isMouseOnBattleField() const;
   104	
   105	    bool isMouseRightButtonPressed() const{
   106	        return m_mouse->isRightButtonPressed();
   107	    }
   108	
   109	    cAbstractStructure *getStructurePointerWhereMouseHovers() const;
   110	
   111	    int getMouseCellFromScreen(int mouseX, int mouseY) const;
   112	    int getMouseCellFromScreenClamped(int mouseX, int mouseY) const;
   113	
   114	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
   115	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
   116	    void onNotifyGameEvent(const s_GameEvent &event) override;
   117	
   118	    void setMouseState(eMouseState newState);
   119	
   120	    void toPreviousState();
   121	
   122	    bool isState(eMouseState other) const;
   123	
   124	    void onFocusMouseStateEvent();
   125	
   126	protected:
   127	    void determineHoveringOverStructureId();
   128	    void determineHoveringOverUnitId();
   129	
   130	private:
   131	    int m_mouseHoveringOverStructureId;
   132	    int m_mouseHoveringOverUnitId;
   133	    bool m_mouseOnBattleField;
   134	
   135	    // on what cell is the mouse hovering
   136	    int m_mouseCell;
   137	    int m_mouseCellClamped;
   138	
   139	    // context belongs to specific player
   140	    cPlayer *m_player;
   141	
   142	    // the state to direct events to
   143	    eMouseState m_state;
   144	    eMouseState m_prevState;             // used to switch back previous state (ie from Place, or Repair mode)
   145	    eMouseState m_prevStateBeforeRepair; // the state before repair mode only, used when Place/Repair mode is used
   146	    // in conjunction
   147	
   148	    cMouse *m_mouse;
   149	
   150	    cGameObjectContext *m_objects = nullptr;
   151	    cMapCamera *m_mapCamera = nullptr;
   152	    cGameSettings *m_settings = nullptr;
   153	    cDrawManager *m_drawManager = nullptr;
   154	    cEventEmitter *m_eventEmitter = nullptr;
   155	    cStructureUtils *m_structureUtils = nullptr;
   156	    cInfoContext *m_infos = nullptr;
   157	    AudioContext *m_audioContext = nullptr;
   158	    cRectangle *m_mapViewport = nullptr;
   159	
   160	    // the states, initialized once to save a lot of construct/destructs (and make it possible
   161	    // to switch between states without needing to restore 'state' within the state object)
   162	    std::unique_ptr<cMouseNormalState> m_mouseNormalState;
   163	    std::unique_ptr<cMouseUnitsSelectedState> m_mouseUnitsSelectedState;
   164	    std::unique_ptr<cMouseRepairState> m_mouseRepairState;
   165	    std::unique_ptr<cMousePlaceState> m_mousePlaceState;
   166	    std::unique_ptr<cMouseDeployState> m_mouseDeployState;
   167	
   168	    //
   169	    bool m_prevTickMouseAtBattleField;
   170	
   171	    // mouse state
   172	    void onNotifyMouseStateEvent(const s_MouseEvent &event);
   173	    void onBlurMouseStateEvent();
   174	    void onMouseMovedTo(const s_MouseEvent &event);
   175	    void updateMouseCell(const cPoint &coords);
   176	
   177	    static constexpr int MOUSE_CELL_HOVER_TOPBAR = -1;
   178	    static constexpr int MOUSE_CELL_HOVER_MINIMAP = -2;
   179	    static constexpr int MOUSE_CELL_HOVER_SIDEBAR = -3;
   180	};
```

### src/drawers/cTextDrawer.h@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cTextDrawer.h | nl -ba
```

Вывод:
```text
     1	/**
     2	 * @file cTextDrawer.h
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
    19	class Color;
    20	#include <SDL3_ttf/SDL_ttf.h>
    21	#include <string>
    22	#include <memory>
    23	
    24	class cTextTextureCache;
    25	class cGameSettings;
    26	class SDLDrawer;
    27	
    28	class cTextDrawer {
    29	public:
    30	    // Constructor, initializes the drawer with a TTF font and game settings
    31	    cTextDrawer(TTF_Font *theFont, cGameSettings *settings, SDLDrawer *renderer);
    32	    ~cTextDrawer();
    33	
    34	    // Draws text at (x, y) in white, with optional shadow
    35	    void drawText(int x, int y, const std::string &msg, bool applyShadow = true) const;
    36	    // Draws text at given coordinates, with color and optional shadow
    37	    void drawText(cPoint &coords, Color color, const std::string &msg, bool applyShadow = true) const;
    38	    // Draws text at (x, y) with color and optional shadow
    39	    void drawText(int x, int y, Color color, const std::string &msg, bool applyShadow = true) const;
    40	    // Draws centered text horizontally at line y, in white
    41	    void drawTextCentered(const std::string &msg, int y) const;
    42	    // Draws centered text horizontally at line y, with color
    43	    void drawTextCentered(const std::string &msg, int y, Color color) const;
    44	    // Draws centered text within a region (x, width) at line y, with color
    45	    void drawTextCentered(const std::string &msg, int x, int width, int y, Color color) const;
    46	
    47	    /**
    48	     * Draws the text within a 'box' (rectangle), positioned at X,Y. The width/height of the box determine
    49	     * how to center the text. When centering text, the height/width of the font is taken into account.
    50	    */
    51	    // Draws centered text inside a box (x, y, boxWidth, boxHeight), with color
    52	    void drawTextCenteredInBox(const std::string &msg, int x, int y, int boxWidth, int boxHeight, Color color) const;
    53	    // Draws centered text inside a rectangle, with color
    54	    void drawTextCenteredInBox(const std::string &msg, const cRectangle &rect, Color color) const;
    55	    // Draws centered text inside a rectangle, with color and offset
    56	    void drawTextCenteredInBox(const std::string &msg, const cRectangle &rect, Color color, int offsetX, int offsetY) const;
    57	    void drawTextScaledCenteredInBox(const std::string &msg, const cRectangle &rect, float scale, Color color, bool applyShadow = true) const;
    58	    void drawTextScaledOpticallyCenteredInBox(const std::string &msg, const cRectangle &rect, float scale, Color color, bool applyShadow = true) const;
    59	    // Draws text at the bottom right of the screen, in white, with margin
    60	    void drawTextBottomRight(const std::string &msg, int margin=0) const;
    61	    // Draws text at the bottom left of the screen, in white, with margin
    62	    void drawTextBottomLeft(const std::string &msg, int margin=0) const;
    63	    // Draws text at the bottom right of the screen, with color and margin
    64	    void drawTextBottomRight(Color color, const std::string &msg,int margin =0) const;
    65	    // Draws text at the bottom left of the screen, with color and margin
    66	    void drawTextBottomLeft(Color color, const std::string &msg,int margin =0) const;
    67	    // Returns the pixel length of the text
    68	    int getTextLength(const std::string &msg) const;
    69	    // Returns the font height in pixels
    70	    int getFontHeight() const;
    71	    // Clears the text texture cache
    72	    void resetCache() const;
    73	    // Returns a rectangle bounding the text at (x, y)
    74	    [[nodiscard]] cRectangle getRect(int x, int y, const std::string &msg) const;
    75	    // Returns a rectangle bounding the text at (x, y)
    76	    [[nodiscard]] cRectangle getAsRectangle(int x, int y, const std::string &msg) const;
    77	
    78	protected:
    79	
    80	private:
    81	    TTF_Font *m_font;
    82	    std::unique_ptr<cTextTextureCache> m_textCache;
    83	    cGameSettings* m_settings = nullptr;
    84	    SDLDrawer *m_renderer = nullptr;
    85	};
```

### src/include/sGameServices.h@dc6e5ff

Команда:
```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/include/sGameServices.h | nl -ba
```

Вывод:
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
