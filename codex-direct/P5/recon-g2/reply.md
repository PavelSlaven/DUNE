## RECON-P5G2R | Wed Nov 11 12:20:59 UTC 2026

Отчёт: [.tmp/p5g2r/RECON.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/RECON.md)

### Пункт 1 — число строк исходных файлов

- `src/include/eGameState.h@acddd29` — 72 строки.
- `src/gamestates/cMainMenuState.h@acddd29` — 75 строк.
- `src/gamestates/cChooseHouseState.h@acddd29` — 81 строка.
- `src/gamestates/cSelectMissionState.h@acddd29` — 64 строки.
- `src/gamestates/cSetupSkirmishState.h@acddd29` — 217 строк.
- `src/gamestates/cOptionsState.h@acddd29` — 79 строк.
- `src/gamestates/cCreditsState.h@acddd29` — 80 строк.
- `src/gamestates/cSelectYourNextConquestState.h@acddd29` — 193 строки.
- `src/gameobjects/mentat/AbstractMentat.h@acddd29` — 127 строк.
- `src/debug/UiAudit.hpp@acddd29` — 51 строка.
- `src/debug/UiAuditScenes.hpp@acddd29` — 31 строка.
- `src/debug/UiAuditScenes.cpp@acddd29` — 61 строка.
- `src/debug/UiAuditAccess.cpp@acddd29` — 53 строки.

### Пункт 2 — функции

- `cGame::setState` — `src/game/cGame_logic.cpp@acddd29:942-1228`
- `cGame::transitionStateIfRequired` — `src/game/cGame_logic.cpp@acddd29:1489-1501`
- `cGame::setNextStateToTransitionTo` — `src/game/cGame_logic.cpp@acddd29:1503-1506`
- `cGame::jumpToSelectYourNextConquestMission` — `src/game/cGame_logic.cpp@acddd29:913-940`
- `cChooseHouseState::draw` — `src/gamestates/cChooseHouseState.cpp@acddd29:111-142`
- `cSelectMissionState::draw` — `src/gamestates/cSelectMissionState.cpp@acddd29:179-224`
- `cSetupSkirmishState::cSetupSkirmishState` — `src/gamestates/cSetupSkirmishState.cpp@acddd29:93-402`
- `cSetupSkirmishState::draw` — `src/gamestates/cSetupSkirmishState.cpp@acddd29:436-534`
- `cOptionsState::cOptionsState` — `src/gamestates/cOptionsState.cpp@acddd29:49-69`
- `cOptionsState::draw` — `src/gamestates/cOptionsState.cpp@acddd29:596-605`
- `cCreditsState::cCreditsState` — `src/gamestates/cCreditsState.cpp@acddd29:39-100`
- `cCreditsState::thinkFast` — `src/gamestates/cCreditsState.cpp@acddd29:427-439`
- `cCreditsState::draw` — `src/gamestates/cCreditsState.cpp@acddd29:441-469`
- `cSelectYourNextConquestState::cSelectYourNextConquestState` — `src/gamestates/cSelectYourNextConquestState.cpp@acddd29:78-174`
- `cSelectYourNextConquestState::thinkFast` — `src/gamestates/cSelectYourNextConquestState.cpp@acddd29:194-339`
- `cSelectYourNextConquestState::draw` — `src/gamestates/cSelectYourNextConquestState.cpp@acddd29:341-376`
- `AbstractMentat::AbstractMentat` — `src/gameobjects/mentat/AbstractMentat.cpp@acddd29:45-111`
- `AbstractMentat::thinkFast` — нет определения.
- `AbstractMentat::draw` — `src/gameobjects/mentat/AbstractMentat.cpp@acddd29:273-314`
- `CampaignProgress::nextMission` — `src/game/CampaignProgress.cpp@acddd29:155-158`
- `CampaignProgress::highestUnlockedMission` — `src/game/CampaignProgress.cpp@acddd29:160-164`
- `CampaignProgress::recordMissionVictory` — `src/game/CampaignProgress.cpp@acddd29:182-196`
- `cGameConditionChecker::missionInit` — `src/game/cGameConditionChecker.cpp@acddd29:35-39`
- `cGameConditionChecker::isMissionWon` — `src/game/cGameConditionChecker.cpp@acddd29:53-83`
- `cGameConditionChecker::isMissionFailed` — `src/game/cGameConditionChecker.cpp@acddd29:85-119`
- `cGame::missionInit` — `src/game/cGame_logic.cpp@acddd29:431-461`
- `cGame::setMissionWon` — `src/game/cGame_logic.cpp@acddd29:472-498`
- `cGame::setMissionLost` — `src/game/cGame_logic.cpp@acddd29:500-513`
- `cGame::prepareMentatForPlayer` — `src/game/cGame_logic.cpp@acddd29:1239-1255`
- `cGame::prepareMentatToTellAboutHouse` — `src/game/cGame_logic.cpp@acddd29:1257-1285`
- `cGame::changeStateFromMentat` — `src/game/cGame_logic.cpp@acddd29:1307-1374`
- `cGame::checkMissionWinOrFail` — `src/game/cGame_logic.cpp@acddd29:1720-1731`
- `cMissionStatsCollector::cMissionStatsCollector` — `src/game/cMissionStatsCollector.cpp@acddd29:25-27`

### Пункт 3 — число мест имён

| Имя | Мест |
|---|---:|
| `HUMAN` | 80 |
| `m_region` | 0 |
| `m_mission` | 0 |
| `GAME_REGION` | 14 |
| `createAndPrepareMentatForHumanPlayer` | 0 |
| `prepareMentatToTellAboutHouse` | 3 |
| `m_mentat` | 48 |
| `iMentatSentence` | 12 |
| `TIMER_Speaking` | 10 |
| `AWAITING_RESPONSE` | 6 |
| `SPEAKING` | 5 |
| `initSkirmish` | 0 |
| `loadSkirmishMaps` | 6 |
| `iSkirmishMap` | 37 |
| `startingPoints` | 8 |
| `skirmishPlayer` | 18 |
| `bPlaying` | 15 |
| `m_crawlerY` | 6 |
| `m_moveSpeed` | 5 |
| `m_titleHeight` | 4 |
| `m_lines` | 56 |
| `s_CreditLine` | 50 |
| `regionSceneState` | 11 |
| `iRegionSceneAlpha` | 12 |
| `m_displayStatusLabel` | 0 |
| `switchOptionsPage` | 0 |
| `OptionsPage` | 0 |
| `m_bindingCapture` | 0 |
| `friend` | 4 |

### Пункт 4

`git grep` нашёл 94 строки с `sardaukar`.

### Чтение

Полностью прочитаны `.tmp/p5gr/access.tsv` и `.tmp/p5gr/scene-functions.tsv`. Первый вывод был обрезан; файл дочитан частями. В задании не хватило дополнительных вводных документов: оно не ссылается на другие источники, нужные для разведки.

### Не проверено

Сборка, CTest и запуск игры не выполнялись по прямому запрету задания.

### Рабочие места

```text
$ python3 /srv/dune/tools/task-places.py inventory .tmp/p5g2r --size
path    kind    branch  head_date  size    dirty  untracked  unpushed  worktrees  procs  refs
/srv/dune/worktrees/u13g/.tmp/p5g2r    dir    -    -    221003    -    -    -    -    0    0
```

`.tmp/p5g2r` — оставить, разведка для ведущего.

Отчёты: [files.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/files.md), [functions.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/functions.md), [names.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/names.md), [houses.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/houses.md), [spotcheck.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/spotcheck.md). Помощник 4 проверил 12 фактов; все 12 совпали.