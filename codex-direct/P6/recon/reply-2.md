## RECON-P6R-2 | 2026-11-10 14:01:30 UTC

Полный отчёт: [`.tmp/p6r/RECON-2.md`](/srv/dune/worktrees/u34/.tmp/p6r/RECON-2.md).

1. Индекс содержит 241 запись в FORK1 и 242 в PORT. Имена семейств `HM_*` (без `HM_HV_*`), `BUILD_*_FLAG` и `TERRAIN_*_VAR_*` совпадают; единственная запись только в PORT — `EXPLOSION_CARRYALL`.
2. `cPack` предоставляет открытый поиск индекса по имени, но не имени по индексу.
3. В `SDLDrawer` есть `renderStrechFullSprite` — `src/drawers/SDLDrawer.hpp@0a33444:35`.
4. Все 92 текстуры с именами `UNIT_*`/`BUILD_*` в HD4-паке PORT — RGBA; код создаёт их без перекраски House-палитрой или маской.
5. В FORK1 найдено 13 вызовов `getHouseTexture`. В PORT отдельная HD-накладка осталась только для флага ветряка, причём без House-маски; остальные соответствуют общему флаговому пути.

Новые файлы: `.tmp/p6r/RECON-2.md`, `pack-fork.tsv`, `pack-port.tsv`, `pack_index.py`. В `.tmp/p6r/progress.md` добавлена строка о завершении P6R-2.

### Не проверено

Сборки, CTest и запуск игры не выполнялись. Рисование HD-текстур в запущенной игре не проверялось.

### Рабочие места

```text
path                                      kind  branch  head_date  size    dirty  untracked  unpushed  worktrees  procs  refs
/srv/dune/worktrees/u34/.tmp/p6r          dir   -       -          230616  -      -          -         -          0      0
```

`.tmp/p6r` — оставить: разведка для ведущего.

### git status --short

Вывод пустой. Коммитов нет.