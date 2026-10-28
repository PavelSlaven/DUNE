## PLAN-a1

Создать [генератор](/srv/dune/worktrees/a1/tools/units3d/unit_contract.py), [тест](/srv/dune/worktrees/a1/tools/units3d/tests/test_unit_contract.py), [JSON-контракт](/srv/dune/worktrees/a1/docs/units/unit_contract.json) и [Markdown-документ](/srv/dune/worktrees/a1/docs/units/UNIT_CONTRACT.md).

Источники: паки через `read_pack`/`decode_image`; роли, типы и кадры из `sUnitInfo`; строки, направления и правила отрисовки из движка; Sega-файлы из манифеста. Отклонения размеров сохраняются без исправления. Свет вычисляется по кадру 0 каждой пары здания и тени. Markdown генерируется из JSON.

Механика передана субагентам luna; смысловая сверка и один самоаудит выполнены ведущим. Проверка — только заданная команда `unittest`. Рендер, модели, камера и изменения движка исключены из объёма.

## Q-a1-01 | 2026-10-28 16:07:07 UTC | HEAD 39a88806f4a4260b5b303a781448189e672f59f3

Файлы готовы, проверки прошли. Создание коммитов заблокировано средой:

```text
fatal: Unable to create '/srv/dune/worktrees/a1/.git/index.lock': Read-only file system
```

Журнал хода:

```text
Тест контракта создан до генератора; коммит не создан: .git доступен только для чтения; красный прогон: Ran 5 tests in 0.091s, FAILED (failures=1, errors=4).
Генератор и JSON/Markdown созданы: 59 записей, 9 исключений размеров, 20 измерений теней; коммит не создан: .git доступен только для чтения; полный unittest: Ran 6 tests in 2.861s, OK.
Один круг самоаудита завершён, исправлены единицы основания здания, порядок слоёв и полнота источников; коммит не создан: .git доступен только для чтения; полный unittest: Ran 6 tests in 2.861s, OK; git diff --check без замечаний.
```

Проверка выполнялась командой:

```bash
D2TM_PACK_DIR=/srv/dune/inputs/packs /srv/dune/venv/bin/python -m unittest discover -s tools/units3d/tests -v
```

Красный прогон до создания скрипта:

```text
Ran 5 tests in 0.091s
FAILED (failures=1, errors=4)
```

Итоговый зелёный прогон:

```text
Ran 6 tests in 2.861s
OK
```

### Не проверено

Режим пропуска без `D2TM_PACK_DIR` отдельно не запускался. Выполнена только заданная команда с паками.

### git status --short

```text
?? docs/units/UNIT_CONTRACT.md
?? docs/units/unit_contract.json
?? tools/units3d/
```

### Владельцу

1. Контракт содержит все записи юнитов, исключения размеров, правила отрисовки и измерения света; воспроизводимость проверена.
2. Коммиты не созданы из-за запрета записи в `.git`. Приёмка ведущим ещё не получена.
3. Для завершения требуется восстановить запись в `.git`, затем закоммитить подготовленные файлы и провести приёмку.