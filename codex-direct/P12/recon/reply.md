## RECON-P12R | Tue Nov 10 19:22:38 UTC 2026

Полный отчёт: [RECON.md](/srv/dune/worktrees/u13g/.tmp/p12r/RECON.md).

1. В FORK1 добавлен workflow выпуска Windows, Linux и macOS; сценарии упаковки FORK1 и PORT перечислены в [release-script.tsv](/srv/dune/worktrees/u13g/.tmp/p12r/release-script.tsv). В `CMakeLists.txt` найденный участок diff добавляет runtime UI-audit тесты.
2. В UP1 и PORT перечислены одинаковые четыре workflow; все четыре сравнения `git diff --stat` дали пустой вывод. Подробности, включая триггеры, задания, ОС, действия и секреты, — в [workflows.tsv](/srv/dune/worktrees/u13g/.tmp/p12r/workflows.tsv).
3. В FORK1 сценарий копирует HD4-паки, HD4-сцены и кампании; явного копирования классического `sdl_data.dat` нет. В PORT каталог `packaging` отсутствует; сценарий не указывает источник DLL.
4. В FORK1 добавлены пять PNG-снимков, указателей LFS нет; README содержит пять ссылок на галерею. Факты о заголовках, размерах и наличии файлов в PORT — в [gallery.tsv](/srv/dune/worktrees/u13g/.tmp/p12r/gallery.tsv). Помощник 4 сверил 12 фактов: 12 совпали.

### Чтение

Прочитан целиком `/srv/dune/tasks/load-check/PORT_PLAN.md` и фрагмент карты командой `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '769,789p'`. В задании не хватило дополнительных правил или контрактов, необходимых для выполненных действий.

### Файлы `.tmp/p12r/`

- [RECON.md](/srv/dune/worktrees/u13g/.tmp/p12r/RECON.md)
- [fork-packaging.tsv](/srv/dune/worktrees/u13g/.tmp/p12r/fork-packaging.tsv)
- [gallery.tsv](/srv/dune/worktrees/u13g/.tmp/p12r/gallery.tsv)
- [workflows.tsv](/srv/dune/worktrees/u13g/.tmp/p12r/workflows.tsv)
- [release-script.tsv](/srv/dune/worktrees/u13g/.tmp/p12r/release-script.tsv)
- [spotcheck.md](/srv/dune/worktrees/u13g/.tmp/p12r/spotcheck.md)
- [progress.md](/srv/dune/worktrees/u13g/.tmp/p12r/progress.md)

### Не проверено

Сборки, CI, CTest, запуск игры и сценарии упаковки не запускались: это запрещено заданием.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p12r --size`:

```text
path                              kind  branch  head_date  size   dirty  untracked  unpushed  worktrees  procs  refs
/srv/dune/worktrees/u13g/.tmp/p12r dir   -       -          47658  -      -          -         -          0      0
```

`/srv/dune/worktrees/u13g/.tmp/p12r` — оставить — разведка для ведущего.