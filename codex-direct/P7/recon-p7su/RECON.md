## RECON-P7SU | 2026-11-12 08:19:33 UTC

### Оглавление

- `.tmp/p7su/old-places.tsv` — 804 строки (`wc -l`, 803 строки данных и заголовок), пункт 1.
- `.tmp/p7su/places-map.tsv` — 804 строки (`wc -l`, 803 строки данных и заголовок), пункт 1.
- `.tmp/p7su/places-summary.txt` — 3 строки (`wc -l`), пункт 1.
- `.tmp/p7su/diff-stat.txt` — 5 строк (`wc -l`), пункт 2.

### Итог по статусам

- на месте — 758 мест.
- сдвиг — 41 место.
- изменена — 4 места.

### Сверка корневой нити

- Команда: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 405355e96f07a83da96b76cc2832a09c9c43e825:resources/bin/settings.ini | nl -ba | sed -n '84p'`. Вывод: `84    GFXWORLD=sdl_world_hd4.dat`. Совпало.
- Команда: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show b9f6b024246c47209f29259b676dd94512a51553:src/context/ContextCreator.cpp | nl -ba | sed -n '45p'`. Вывод: `45        gfxworld = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXWORLD), kHd4AssetDensity);`. Совпало.
- Команда: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 405355e96f07a83da96b76cc2832a09c9c43e825:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '728p'`. Вывод: `728        case uiaudit::GameKind::ListStarport: return eListType::LIST_STARPORT;`. Совпало.
- Команда: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show b9f6b024246c47209f29259b676dd94512a51553:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '403p'`. Вывод: `403            .withLabel("◄")`. Совпало.
- Команда: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show b9f6b024246c47209f29259b676dd94512a51553:src/utils/cIniUtils.cpp | nl -ba | sed -n '130p'`. Вывод: `130    {"Raider Trike", RAIDER},`. Совпало.

### Чтение

- `.tmp/p7gr/RECON.md` прочитан целиком отдельным вызовом как образец оглавления RECON.
- Не хватает в задании: ничего для этой разведки; дополнительные правила или контракты в образце не упомянуты.

### Не проверено

- Сборки, CTest и запуск игры не выполнялись, поскольку они запрещены заданием.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p7su --size`:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u35/.tmp/p7su	dir	-	-	250767	-	-	-	-	0	0
```

- `.tmp/p7su` — оставить — разведка для ведущего.
