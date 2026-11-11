## RECON-P5G3V | Wed Nov 11 15:27:41 UTC 2026

Отчёт: [.tmp/p5g3v/RECON.md](/srv/dune/worktrees/u35/.tmp/p5g3v/RECON.md). Подробные отчёты: [headers.md](/srv/dune/worktrees/u35/.tmp/p5g3v/headers.md), [entries.md](/srv/dune/worktrees/u35/.tmp/p5g3v/entries.md), [functions.md](/srv/dune/worktrees/u35/.tmp/p5g3v/functions.md), [inputs.md](/srv/dune/worktrees/u35/.tmp/p5g3v/inputs.md).

**Пункт 1 — число строк исходных файлов по последним номерам `nl`:**

- `src/gamestates/cScoringState.h` — 40.
- `src/gamestates/cVideoState.h` — 51.
- `src/gamestates/cEditorState.h` — 138.
- `src/gamestates/cNewMapEditorState.h` — 79.
- `src/include/eGameState.h` — 72.

**Пункт 2:** вывод `git grep` — 45 строк; вне `src/include/eGameState.h` и `src/include/eGameState.cpp` — 29 строк.

**Пункт 3 — функции:**

- `cScoringState::cScoringState` — `src/gamestates/cScoringState.cpp@91416fb:22-40`; `draw` — `src/gamestates/cScoringState.cpp@91416fb:56-111`; `thinkFast` — `src/gamestates/cScoringState.cpp@91416fb:52-54`; `onNotifyMouseEvent` — `src/gamestates/cScoringState.cpp@91416fb:113-120`; `onNotifyKeyboardEvent` — `src/gamestates/cScoringState.cpp@91416fb:122-124`.
- `cVideoState::cVideoState` — `src/gamestates/cVideoState.cpp@91416fb:43-65`; `draw` — `src/gamestates/cVideoState.cpp@91416fb:91-99`; `thinkFast` — `src/gamestates/cVideoState.cpp@91416fb:76-78`; `onNotifyMouseEvent` — `src/gamestates/cVideoState.cpp@91416fb:101-106`; `onNotifyKeyboardEvent` — `src/gamestates/cVideoState.cpp@91416fb:108-113`.
- `cEditorState::cEditorState` — `src/gamestates/cEditorState.cpp@91416fb:60-105`; `draw` — `src/gamestates/cEditorState.cpp@91416fb:415-431`; `thinkFast` — `src/gamestates/cEditorState.cpp@91416fb:411-413`; `onNotifyMouseEvent` — `src/gamestates/cEditorState.cpp@91416fb:433-491`; `onNotifyKeyboardEvent` — `src/gamestates/cEditorState.cpp@91416fb:498-603`.
- `cNewMapEditorState::cNewMapEditorState` — `src/gamestates/cNewmapEditorState.cpp@91416fb:48-66`; `draw` — `src/gamestates/cNewmapEditorState.cpp@91416fb:291-295`; `thinkFast` — `src/gamestates/cNewmapEditorState.cpp@91416fb:286-289`; `onNotifyMouseEvent` — `src/gamestates/cNewmapEditorState.cpp@91416fb:297-300`; `onNotifyKeyboardEvent` — `src/gamestates/cNewmapEditorState.cpp@91416fb:307-310`.

**Пункт 4 — число строк вывода команд:** первая команда — 49, вторая — 1, третья — 0.

### Чтение

Целиком прочитаны `tools/ui-audit/check_screens.py` и `tools/ui-audit/exclusions.tsv`, каждый отдельным вызовом. В задании и этих файлах дополнительных ссылок на правила, нормы или контракты для чтения не обнаружено.

### Не проверено

Сборки, CTest и запуск игры не выполнялись: это запрещено заданием.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3v --size`:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u35/.tmp/p5g3v	dir	-	-	92051	-	-	-	-	0	0
```

`.tmp/p5g3v` — оставить — разведка для ведущего. Сверка помощника 3: все восемь выбранных фактов совпали; результат записан в [spotcheck.md](/srv/dune/worktrees/u35/.tmp/p5g3v/spotcheck.md).