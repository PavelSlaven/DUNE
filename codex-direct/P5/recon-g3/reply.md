## RECON-P5G3R | 2026-11-11 12:27:35 UTC

Отчёт: [.tmp/p5g3r/RECON.md](/srv/dune/worktrees/u35/.tmp/p5g3r/RECON.md).

В оглавлении указаны результаты `wc -l`: [headers.md](/srv/dune/worktrees/u35/.tmp/p5g3r/headers.md) — 4535 строк, [functions.md](/srv/dune/worktrees/u35/.tmp/p5g3r/functions.md) — 731, [names.tsv](/srv/dune/worktrees/u35/.tmp/p5g3r/names.tsv) — 219. В [spotcheck.md](/srv/dune/worktrees/u35/.tmp/p5g3r/spotcheck.md) помощник 4 сверил 12 фактов; все совпали.

### Пункт 1

Числа — последние номера строк в дословных выводах `nl -ba`.

| Путь в PORT | Строк |
|---|---:|
| `src/game/cGame.h@acddd29` | 270 |
| `src/context/AudioContext.hpp@acddd29` | 59 |
| `src/context/ContextCreator.hpp@acddd29` | 49 |
| `src/context/GameContext.hpp@acddd29` | 58 |
| `src/context/GraphicsContext.hpp@acddd29` | 28 |
| `src/context/MusicChoice.hpp@acddd29` | 26 |
| `src/context/MusicJukeBox.hpp@acddd29` | 42 |
| `src/context/TextContext.hpp@acddd29` | 41 |
| `src/context/cGameObjectContext.h@acddd29` | 80 |
| `src/context/cGameObjectContextCreator.h@acddd29` | 28 |
| `src/context/cInfoContext.h@acddd29` | 69 |
| `src/context/cInfoContextCreator.h@acddd29` | 58 |
| `src/gameobjects/players/cPlayer.h@acddd29` | 663 |
| `src/gameobjects/map/cMapCamera.h@acddd29` | 281 |
| `src/gameobjects/map/cMap.h@acddd29` | 529 |
| `src/managers/cDrawManager.h@acddd29` | 165 |
| `src/sidebar/cSideBar.h@acddd29` | 161 |
| `src/sidebar/cBuildingList.h@acddd29` | 225 |
| `src/sidebar/cBuildingListItem.h@acddd29` | 330 |
| `src/drawers/cBuildingListDrawer.h@acddd29` | 95 |
| `src/drawers/cSideBarDrawer.h@acddd29` | 81 |
| `src/drawers/cMiniMapDrawer.h@acddd29` | 125 |
| `src/drawers/cOrderDrawer.h@acddd29` | 55 |
| `src/controls/cMouse.h@acddd29` | 151 |
| `src/gameobjects/structures/cStructureFactory.h@acddd29` | 75 |
| `src/utils/cStructureUtils.h@acddd29` | 69 |
| `src/game/cTimeManager.h@acddd29` | 101 |
| `src/drawers/cMessageDrawer.h@acddd29` | 89 |
| `src/sidebar/HudLayout.hpp@acddd29` | 210 |

`HudLayout.h` — нет файла.

### Пункт 2

| Функция | Определение в PORT |
|---|---|
| `cUnit::draw_experience` | нет определения |
| `cUnit::draw_group` | нет определения |
| `cUnit::draw_health` | нет определения |
| `cUnit::draw_spice` | нет определения |
| `cStructureDrawer::drawStructureHealthBar` | `src/drawers/cStructureDrawer.cpp@acddd29:477-510` |
| `cGame::run` | `src/game/cGame_logic.cpp@acddd29:571-643` |
| `cGame::drawOutcomeScreen` | нет определения |
| `cGame::takeBackGroundScreen` | `src/game/cGame_logic.cpp@acddd29:1708-1713` |
| `cDrawManager::missionInit` | `src/managers/cDrawManager.cpp@acddd29:419-423` |
| `cDrawManager::draw` | нет определения |
| `cSideBarDrawer::draw` | `src/drawers/cSideBarDrawer.cpp@acddd29:98-101` |
| `cStructureFactory::createStructure` | `src/gameobjects/structures/cStructureFactory.cpp@acddd29:119-225` |

Поиск заголовков функций состояния, заданный в пункте 2, не дал определений.

### Пункт 3

В таблице 218 различных имён без заголовка; для 58 имён в столбце «объявления в PORT» указано «нет».

### Чтение

Полностью, отдельными вызовами прочитаны:

- `/srv/dune/worktrees/u13g/.tmp/p5gr/access.tsv`;
- `/srv/dune/worktrees/u13g/.tmp/p5gr/access-helpers.tsv`;
- `/srv/dune/worktrees/u13g/.tmp/p5dr/hooks.tsv`.

В исходном условии отбора строк `access.tsv` не было явно указано равенство имени функции без скобки. Владелец уточнил это условие в ответе на Q-P5G3R-01.

### Не проверено

Сборка, CTest и запуск игры не выполнялись: они запрещены заданием.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3r --size`:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u35/.tmp/p5g3r	dir	-	-	272093	-	-	-	-	0	0
```

`.tmp/p5g3r` — оставить — разведка для ведущего.