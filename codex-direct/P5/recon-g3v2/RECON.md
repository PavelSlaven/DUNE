## RECON-P5G3V2 | Wed Nov 11 20:47:22 UTC 2026

### Оглавление

- `.tmp/p5g3v2/screens.md` — 1072 строки (`wc -l`); пункт 1.
- `.tmp/p5g3v2/gui.md` — 754 строки (`wc -l`); пункт 2.
- `.tmp/p5g3v2/records.md` — 15 строк (`wc -l`); пункт 3.
- `.tmp/p5g3v2/data.md` — 600 строк (`wc -l`); пункт 4.
- `.tmp/p5g3v2/spotcheck.md` — 191 строка (`wc -l`); сверены восемь фактов, все восемь совпали.

### Отчёт

`.tmp/p5g3v2/RECON.md`

### Пункт 1: файлы и последний номер `nl`

- `src/gamestates/cNewmapEditorState.cpp@c583461` — весь файл; последний номер `nl`: 378.
- `src/gamestates/cScoringState.cpp@c583461` — весь файл; последний номер `nl`: 129.
- `src/gamestates/cEditorState.cpp@c583461:1-410` — последний номер `nl`: 410.
- `src/gamestates/cEditorState.cpp@c583461:605-735` — последний номер `nl`: 735.

### Пункт 2: файлы и последний номер `nl`

- `src/gui/GuiObject.h@c583461` — весь файл; последний номер `nl`: 98.
- `src/gui/GuiObject.cpp@c583461` — весь файл; последний номер `nl`: 70.
- `src/gui/GuiBar.h@c583461` — весь файл; последний номер `nl`: 59.
- `src/gui/GuiBar.cpp@c583461` — весь файл; последний номер `nl`: 92.
- `src/gui/GuiWindow.h@c583461` — весь файл; последний номер `nl`: 53.
- `src/gui/GuiWindow.cpp@c583461` — весь файл; последний номер `nl`: 89.
- `src/gui/GuiButton.h@c583461` — весь файл; последний номер `nl`: 196.

### Пункт 2: число строк вывода каждой команды

- `git show <REV>:src/gui/GuiObject.h | nl -ba` — 98 строк.
- `git show <REV>:src/gui/GuiObject.cpp | nl -ba` — 70 строк.
- `git show <REV>:src/gui/GuiBar.h | nl -ba` — 59 строк.
- `git show <REV>:src/gui/GuiBar.cpp | nl -ba` — 92 строки.
- `git show <REV>:src/gui/GuiWindow.h | nl -ba` — 53 строки.
- `git show <REV>:src/gui/GuiWindow.cpp | nl -ba` — 89 строк.
- `git show <REV>:src/gui/GuiButton.h | nl -ba` — 196 строк.
- `git grep -h -o -E '\bGui[A-Za-z]+\b' <REV> -- src/gamestates/cEditorState.cpp src/gamestates/cNewmapEditorState.cpp | sort | uniq -c` — 19 строк.
- `git grep -n -i 'audit' <REV> -- src/gui` — 25 строк.

### Пункт 3: число строк вывода каждой команды

- `git grep -n -E 'uiaudit::' <REV> -- src/gamestates/cEditorState.cpp src/gamestates/cNewmapEditorState.cpp src/gamestates/cScoringState.cpp src/gamestates/cWinLoseState.cpp src/gamestates/cVideoState.cpp` — 0 строк (пустой вывод).
- `git grep -n -E 'cScoringState|GAME_SCORING|GAME_EDITOR|GAME_NEW_MAP_EDITOR|cEditorState|cNewMapEditorState|outcome-win|outcome-lose' <REV> -- src/debug tools/ui-audit` — 2 строки.

### Пункт 4: файлы и последний номер `nl`

- `src/game/cMissionStatsCollector.h@c583461` — весь файл; последний номер `nl`: 38.
- `src/game/cMissionStatsCollector.cpp@c583461` — весь файл; последний номер `nl`: 163.
- `src/gamestates/cWinLoseState.cpp@c583461` — весь файл; последний номер `nl`: 145.
- `src/gameobjects/map/cPreviewMaps.h@c583461` — весь файл; последний номер `nl`: 74.
- `src/gamestates/cSetupSkirmishState.cpp@c583461:340-420` — последний номер `nl`: 420.

### Пункт 4: число строк вывода каждой команды

- `git show <REV>:src/game/cMissionStatsCollector.h | nl -ba` — 38 строк.
- `git show <REV>:src/game/cMissionStatsCollector.cpp | nl -ba` — 163 строки.
- `git show <REV>:src/gamestates/cWinLoseState.cpp | nl -ba` — 145 строк.
- `git show <REV>:src/gameobjects/map/cPreviewMaps.h | nl -ba` — 74 строки.
- `git show <REV>:src/gamestates/cSetupSkirmishState.cpp | nl -ba | sed -n '340,420p'` — 81 строка.
- `git grep -n -E 'missionStatsCollector|cMissionStatsCollector' <REV> -- src` — 24 строки.
- `git grep -n -E 'getPreviewMaps\(\)|loadMapFromEditor\(' <REV> -- src` — 16 строк.
- `git show <REV>:resources/bin/settings.ini | nl -ba | grep -i 'editor'` — 4 строки.
- `ls -la /srv/dune/worktrees/u34/.tmp/out/run/bin/data/sdl_gfxeditor.dat` — 1 строка.

### Чтение

Целиком, отдельными вызовами прочитаны `.tmp/p5g3v/headers.md` и `.tmp/p5g3v/functions.md`. В задании и прочитанных файлах не указаны дополнительные правила, нормы или контракты, необходимые для разведки; задание задаёт ревизию, команды, формат и рамку изменений.

### Не проверено

Сборка, CTest и запуск игры не выполнялись по запрету задания. Помощник 3 сверил восемь фактов; остальные строки исходных отчётов отдельно не сверялись.

### Рабочие места

Команда:

```text
python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3v2 --size
```

Вывод:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u35/.tmp/p5g3v2	dir	-	-	114809	-	-	-	-	0	0
```

`.tmp/p5g3v2` — оставить — разведка для ведущего.
