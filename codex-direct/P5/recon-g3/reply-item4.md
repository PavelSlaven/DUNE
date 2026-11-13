## RECON-P5G3R | 2026-11-11 12:38:30 UTC

Обновлено оглавление [RECON.md](/srv/dune/worktrees/u35/.tmp/p5g3r/RECON.md). [drawers.md](/srv/dune/worktrees/u35/.tmp/p5g3r/drawers.md) содержит 953 строки по `wc -l`.

### Файлы пункта 4

Последний номер строки в выводе `nl -ba`:

| Путь | Строк |
|---|---:|
| `src/drawers/cUnitDrawer.h@acddd29` | 40 |
| `src/gamestates/cWinLoseState.h@acddd29` | 57 |
| `src/gamestates/cGamePlaying.h@acddd29` | 116 |

### Функции

| Функция | Определение в PORT |
|---|---|
| `cUnitDrawer::draw_spice` | `src/drawers/cUnitDrawer.cpp@acddd29:48-66` |
| `cUnitDrawer::draw_health` | `src/drawers/cUnitDrawer.cpp@acddd29:68-94` |
| `cUnitDrawer::draw_group` | `src/drawers/cUnitDrawer.cpp@acddd29:96-121` |
| `cUnitDrawer::draw_experience` | `src/drawers/cUnitDrawer.cpp@acddd29:123-156` |
| `cWinLoseState::cWinLoseState` | `src/gamestates/cWinLoseState.cpp@acddd29:38-73` |
| `cWinLoseState::~cWinLoseState` | `src/gamestates/cWinLoseState.cpp@acddd29:75-78` |
| `cWinLoseState::thinkFast` | `src/gamestates/cWinLoseState.cpp@acddd29:80-82` |
| `cWinLoseState::draw` | `src/gamestates/cWinLoseState.cpp@acddd29:84-114` |
| `cWinLoseState::onNotifyMouseEvent` | `src/gamestates/cWinLoseState.cpp@acddd29:116-125` |
| `cWinLoseState::getType` | `src/gamestates/cWinLoseState.cpp@acddd29:127-130` |
| `cWinLoseState::onNotifyKeyboardEvent` | `src/gamestates/cWinLoseState.cpp@acddd29:132-134` |
| `cWinLoseState::onMouseLeftButtonClicked` | `src/gamestates/cWinLoseState.cpp@acddd29:136-145` |
| `cDrawManager::drawCombatState` | `src/managers/cDrawManager.cpp@acddd29:119-175` |
| `cDrawManager::drawDebugInfoUsages` | `src/managers/cDrawManager.cpp@acddd29:177-215` |
| `cDrawManager::drawCredits` | `src/managers/cDrawManager.cpp@acddd29:217-220` |
| `cDrawManager::drawRallyPoint` | `src/managers/cDrawManager.cpp@acddd29:222-251` |
| `cDrawManager::drawSidebar` | `src/managers/cDrawManager.cpp@acddd29:253-259` |
| `cDrawManager::drawStructurePlacing` | `src/managers/cDrawManager.cpp@acddd29:264-274` |
| `cDrawManager::drawMessage` | `src/managers/cDrawManager.cpp@acddd29:276-281` |
| `cDrawManager::drawCombatMouse` | `src/managers/cDrawManager.cpp@acddd29:283-291` |
| `cDrawManager::drawMouse` | `src/managers/cDrawManager.cpp@acddd29:293-296` |
| `cDrawManager::drawTopBarBackground` | `src/managers/cDrawManager.cpp@acddd29:298-342` |
| `cDrawManager::drawMessageBar` | `src/managers/cDrawManager.cpp@acddd29:435-438` |
| `cGamePlaying::cGamePlaying` | `src/gamestates/cGamePlaying.cpp@acddd29:75-123` |
| `cGamePlaying::thinkFast` | `src/gamestates/cGamePlaying.cpp@acddd29:145-222` |
| `cGamePlaying::draw` | `src/gamestates/cGamePlaying.cpp@acddd29:300-315` |

### Сверка пункта 4

Помощник 2 проверил четыре факта; все четыре совпали. Команды и выводы добавлены в [spotcheck.md](/srv/dune/worktrees/u35/.tmp/p5g3r/spotcheck.md) под `## Пункт 4`.

### Чтение

Три входных TSV из первоначального задания были прочитаны полностью до начала разведки; для пункта 4 дополнительных входных файлов не было.

### Не проверено

Сборка, CTest и запуск игры не выполнялись: они запрещены заданием.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3r --size`:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u35/.tmp/p5g3r	dir	-	-	310707	-	-	-	-	0	0
```

`.tmp/p5g3r` — оставить — разведка для ведущего.