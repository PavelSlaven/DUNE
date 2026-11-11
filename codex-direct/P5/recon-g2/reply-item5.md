## RECON-P5G2R | Wed Nov 11 12:38:38 UTC 2026

Отчёты: [states.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/states.md), [RECON.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/RECON.md), [spotcheck.md](/srv/dune/worktrees/u13g/.tmp/p5g2r/spotcheck.md). В `RECON.md` добавлено число строк `states.md`. Остальные отчёты не менялись.

### Пункт 5 — `states.md`

`wc -l`: 1739 строк.

### Файлы — последняя строка `nl -ba`

- `src/gamestates/cMentatState.h@acddd29` — 71
- `src/gamestates/cTellHouseState.h@acddd29` — 57
- `src/gamestates/cCreatorState.h@acddd29` — 58
- `src/gamestates/cGameState.h@acddd29` — 88
- `src/gameobjects/mentat/AbstractMentat.cpp@acddd29` — 436
- `src/include/sDataCampaign.h@acddd29` — 24
- `src/include/sGameServices.h@acddd29` — 66
- `src/game/CampaignProgress.hpp@acddd29` — 51
- `src/game/MentatFlow.hpp@acddd29` — 52
- `src/game/MissionFlow.hpp@acddd29` — 71

### Функции

- `cMentatState::cMentatState` — `src/gamestates/cMentatState.cpp@acddd29:38-65`
- `cMentatState::~cMentatState` — `src/gamestates/cMentatState.cpp@acddd29:67-73`
- `cMentatState::getType` — `src/gamestates/cMentatState.cpp@acddd29:70-73`
- `cMentatState::prepareMentat` — `src/gamestates/cMentatState.cpp@acddd29:75-137`
- `cMentatState::thinkFast` — `src/gamestates/cMentatState.cpp@acddd29:139-142`
- `cMentatState::draw` — `src/gamestates/cMentatState.cpp@acddd29:144-149`
- `cMentatState::onNotifyMouseEvent` — `src/gamestates/cMentatState.cpp@acddd29:151-154`
- `cMentatState::onNotifyKeyboardEvent` — `src/gamestates/cMentatState.cpp@acddd29:156-159`
- `cMentatState::loadScenario` — `src/gamestates/cMentatState.cpp@acddd29:161-164`
- `cMentatState::loadBriefing` — `src/gamestates/cMentatState.cpp@acddd29:166-169`
- `cTellHouseState::cTellHouseState` — `src/gamestates/cTellHouseState.cpp@acddd29:34-54`
- `cTellHouseState::~cTellHouseState` — `src/gamestates/cTellHouseState.cpp@acddd29:56-62`
- `cTellHouseState::getType` — `src/gamestates/cTellHouseState.cpp@acddd29:59-62`
- `cTellHouseState::prepareMentat` — `src/gamestates/cTellHouseState.cpp@acddd29:64-91`
- `cTellHouseState::thinkFast` — `src/gamestates/cTellHouseState.cpp@acddd29:93-96`
- `cTellHouseState::draw` — `src/gamestates/cTellHouseState.cpp@acddd29:98-103`
- `cTellHouseState::onNotifyMouseEvent` — `src/gamestates/cTellHouseState.cpp@acddd29:105-108`
- `cTellHouseState::onNotifyKeyboardEvent` — `src/gamestates/cTellHouseState.cpp@acddd29:110-113`
- `cCreatorState::getOrCreateState` — `src/gamestates/cCreatorState.cpp@acddd29:66-75`
- `cCreatorState::getState` — `src/gamestates/cCreatorState.cpp@acddd29:62-64`
- `cCreatorState::hasState` — `src/gamestates/cCreatorState.cpp@acddd29:77-79`
- `cSelectYourNextConquestState::calculateOffset` — `src/gamestates/cSelectYourNextConquestState.cpp@acddd29:176-180`
- `cSelectYourNextConquestState::installWorld` — `src/gamestates/cSelectYourNextConquestState.cpp@acddd29:923-975`
- `cSelectYourNextConquestState::fastForwardUntilMission` — `src/gamestates/cSelectYourNextConquestState.cpp@acddd29:1049-1070`
- `cSelectYourNextConquestState::regionSetupNextMission` — `src/gamestates/cSelectYourNextConquestState.cpp@acddd29:809-841`

### Сверка пункта 5

Помощник 2 сверил четыре факта; все четыре совпали.

### Чтение

`answer-G2R-01.md` не найден в `/srv/dune`. Применено правило извлечения функций, приведённое в тексте дополнения.