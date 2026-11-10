## RECON-P8AR1 | Tue Nov 10 18:09:49 UTC 2026

Полный отчёт: [`.tmp/p8ar1/RECON.md`](/srv/dune/worktrees/u13g/.tmp/p8ar1/RECON.md).

- **1. Размещение в FORK1:** единое правило `cPlayer::canPlaceBuildingListItemAt` добавлено в `src/player/cPlayer.cpp@9208dcf:2012`; отчёт включает изменения трёх коммитов, вызовы и тексты отказа.
- **2. Размещение в PORT:** условия проверки есть в `cMousePlaceState::mayPlaceIt@832c953:98-203`, `cPlaceItDrawer::drawStatusOfStructureAtCell@832c953:70-185` и методах `cPlayer`; AI-вызовы указаны для Campaign и Skirmish.
- **3. НПЗ:** `refineryHarvesterLayout@9208dcf:18-45` задаёт смещение и размер кадра; в PORT вход на НПЗ устанавливает клетку здания, а выход — найденную свободную клетку.
- **4. Радар:** FORK1 выбирает 32 кадра в `cOutPost::thinkFast@9208dcf:15-32`, PORT — 8 кадров; загрузка `BUILD_RADAR` в PORT указана в `cInfoContextCreator.cpp@832c953:1546`.
- **5. Тесты:** приведены проверки четырёх файлов, наличие символов и заголовков в PORT, читаемые файлы и регистрация CTest. `tests.tsv` содержит 39 строк проверок.

**Чтение:** целиком прочитан `PORT_PLAN.md` и выполнены три заданные команды с выводами. Дополнительно прочитаны `docs/PLAN_units_sega_upstream.md` (§§3.2, 5.3) и карточка запуска 27: задание ссылалось на них как на источник способа переноса и проверок.

Файлы `.tmp/p8ar1/`: `RECON.md`, `placement.tsv`, `port-placement.tsv`, `refinery.tsv`, `radar.tsv`, `tests.tsv`, `progress.md`.

### Не проверено

Сборки, CTest и запуск игры не выполнялись, как предписано заданием.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p8ar1 --size`:

```text
path                                      kind  branch  head_date  size    dirty  untracked  unpushed  worktrees  procs  refs
/srv/dune/worktrees/u13g/.tmp/p8ar1      dir   -       -          305236  -      -          -         -          0      0
```

`.tmp/p8ar1` — оставить — разведка для ведущего.