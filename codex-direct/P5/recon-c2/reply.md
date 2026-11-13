## RECON-P5CR2 | 2026-11-10 18:32:35 UTC

Полный отчёт с таблицами, командами и выводами: [`.tmp/p5cr2/RECON.md`](/srv/dune/worktrees/u13g/.tmp/p5cr2/RECON.md).

- **Пункт 1.** В таблице дорожки 1 — 42 участка: `CreditsDrawer.cpp` — 4, `CreditsDrawer.h` — 2, `cBuildingListDrawer.cpp` — 17, `cBuildingListDrawer.h` — 3, `cMessageDrawer.cpp` — 3, `cMessageDrawer.h` — 1, `cMiniMapDrawer.cpp` — 6, `cMiniMapDrawer.h` — 2, `cSideBarDrawer.cpp` — 2, `cSideBarDrawer.h` — 2. По шагам: П5в — 33, П5г — 5, П7 — 3, П8 — 0, П9 — 2, П10 — 0.

  В таблице дорожки 2 — 47 участков: `cDrawManager.cpp` — 10, `cDrawManager.h` — 6, `cMapCamera.cpp` — 8, `cMapCamera.h` — 5, `cBuildingList.cpp` — 2, `cBuildingList.h` — 1, `cBuildingListFactory.cpp` — 3, `cBuildingListItem.cpp` — 3, `cBuildingListItem.h` — 2, `cBuildingListUpdater.cpp` — 2, `cSideBar.cpp` — 3, `cSideBar.h` — 2; в трёх отфильтрованных файлах — 0. По шагам: П5в — 33, П5г — 2, П7 — 2, П8 — 2, П9 — 4, П10 — 9. Счётчики шагов могут пересекаться. Обе скриптовые сверки прошли.

- **Пункт 2.** Подходящих ветвлений `drawHd` не найдено; таблица содержит только заголовок.
- **Пункт 3.** Зафиксированы семь изображений HUD и два шаблона BMP для скриншотов. Пути, размеры LFS-блобов, наличие в PORT и поиск Sardaukar приведены в таблице и журнале команд.
- **Пункт 4.** Таблица содержит десять строк по FORK1 и PORT: камера, её создание, классификация координат мыши и ограничение выделения.

Сверка помощника 4 проверила 12 фактов: 10 вердиктов «совпало», 2 — «не совпало». После сверки было уточнено описание одного участка дорожки 1; по другому удаление `drawOptionBar()` подтверждает отдельный вывод diff. Исходные вердикты сохранены в `spotcheck.md`.

### Чтение

Полностью прочитан отдельным вызовом `/srv/dune/tasks/load-check/PORT_PLAN.md`, включая раздел 4 и описания П5, П5в, П5г, П7–П10. Дополнительных правил или контрактов, необходимых для этих пунктов разведки, не обнаружено.

### Файлы `.tmp/p5cr2/`

Таблицы: `fork-hunks-1.tsv`, `fork-hunks-2.tsv`, `hd-branches.tsv`, `hud-images.tsv`, `camera-mouse.tsv`. Основные материалы: `RECON.md`, `spotcheck.md`, `progress.md`, журналы `track1-`, `track2-`, `track3-evidence.md` и `track*-source-outputs.*`, скрипты сверки и подсчёта. Сырые данные находятся в каталогах `diffs/`, `source-outputs/`, `sources/` и `__pycache__/`. Полный рекурсивный список файлов: [`file-list.txt`](/srv/dune/worktrees/u13g/.tmp/p5cr2/file-list.txt).

### Не проверено

Сборки, CTest и запуск игры не выполнялись согласно заданию.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5cr2 --size`:

```text
path                                      kind  branch  head_date  size     dirty  untracked  unpushed  worktrees  procs  refs
/srv/dune/worktrees/u13g/.tmp/p5cr2      dir   -       -          2643321  -      -          -         -          0      0
```

`.tmp/p5cr2` — **оставить — разведка для ведущего**.