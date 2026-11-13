## DONE-U12-R2 | 2026-11-02 15:28:08 UTC | HEAD 34d51060017e4766565857b95d325b2fa6a4c1b1

Внесены только продиктованные изменения двух тестовых файлов. Остальные три незакоммиченных файла R1 сохранены побайтно. Коммитов нет.

### Журнал хода

Из [.tmp/progress.md](/srv/dune/worktrees/u12/.tmp/progress.md):

```text
R2 point 1: сохранён снимок до R2 в .tmp/u12-r2-before/ и добавлены две проверки len(results) == 8 в указанные методы test_redraw_rotation.py.
Пункт 2 внесён: проверяется строка ValueError с сообщением shift.
Пункт 3 внесён: проверяются mask и body с точной диагностикой ValueError.
R2 point 1 mutant: rotation-first-only отличается от продуктового tools/units3d/redraw_rotation.py только заменой return result на return result[:1]; два целевых теста упали с AssertionError: 1 != 8, exit code 1, лог сохранён в .tmp/u12-r2-mutants/rotation-first-only/case/test.log.
Прогон compose-keyerror завершён; лог сохранён в case/test.log.
Прогон compose-bounds-mask-only завершён; лог сохранён в case/test.log.
2026-11-02T15:28:08Z — U12-R2 рабочая версия: Ran 15 tests in 7.062s; OK; пропусков 0; code=0; лог .tmp/u12-r2-unittest.log.
2026-11-02T15:28:08Z — U12-R2 frozen.sha256: 49/49 OK; code=0; лог .tmp/u12-r2-frozen.log.
2026-11-02T15:28:08Z — U12-R2 ACCEPTANCE.sha256: 7/7 OK; code=0; лог .tmp/u12-r2-acceptance.log.
2026-11-02T15:28:08Z — U12-R2 git diff --check 34d51060: пустой вывод; code=0.
2026-11-02T15:28:08Z — U12-R2 сверка: оба тестовых файла побайтно соответствуют продиктованным заменам; остальные три файла R1 побайтно сохранены; все три копии мутантов содержат ровно заданную одиночную замену; лог .tmp/u12-r2-edits-check.log.
```

### Неверные реализации

Все три пойманы; каждый прогон завершился кодом 1.

- `rotation-first-only`: оба метода — `test_uniform_deviation_is_normalised` и `test_opposite_support_does_not_agree` — упали со строкой `AssertionError: 1 != 8`. [Лог](/srv/dune/worktrees/u12/.tmp/u12-r2-mutants/rotation-first-only/case/test.log).
- `compose-keyerror`: `test_shift_outside_cell_is_rejected` упал со строкой `AssertionError: False is not true : Traceback (most recent call last):`; вложенная трассировка заканчивается `KeyError: 'piece_id'`. [Лог](/srv/dune/worktrees/u12/.tmp/u12-r2-mutants/compose-keyerror/case/test.log).
- `compose-bounds-mask-only`: тот же тест упал со строкой `AssertionError: 0 == 0 : body`. [Лог](/srv/dune/worktrees/u12/.tmp/u12-r2-mutants/compose-bounds-mask-only/case/test.log).

Рабочая версия: [15 тестов, OK](/srv/dune/worktrees/u12/.tmp/u12-r2-unittest.log). Суммы: [49/49 OK](/srv/dune/worktrees/u12/.tmp/u12-r2-frozen.log), [7/7 OK](/srv/dune/worktrees/u12/.tmp/u12-r2-acceptance.log).

### Коммиты

Предложения для изменений R2; список R1 остаётся действующим.

```text
test(units3d): require eight rotation measurements
Behavior changes: none
```

Файл: `tools/units3d/tests/test_redraw_rotation.py`

```text
test(squads): verify exception types and bounds for body and mask
Behavior changes: none
```

Файл: `tools/units3d/tests/test_squad_compose_shift.py`

### Не проверено

Полный Python-прогон и CTest в этом ходе не запускались: REVIEW-U12-02 требует только два тестовых модуля.

### Рабочие места

Работа выполнена в `/srv/dune/worktrees/u12`. Два субагента `gpt-6-luna xhigh` завершили поручения. Копии мутантов и логи находятся в `.tmp/u12-r2-mutants/`.

### git status --short

```text
 M tools/units3d/redraw_common.py
 M tools/units3d/tests/test_redraw_offset_shift.py
 M tools/units3d/tests/test_redraw_rotation.py
 M tools/units3d/tests/test_squad_compose_shift.py
 M tools/units3d/units/UNIT_SIEGEBASE/unit.json
```

### Владельцу

1. Тесты проверяют все восемь направлений, тип исключения и выход за клетку для тела и маски.
2. Незакрытых пунктов REVIEW-U12-02 нет.
3. Требуется приёмка R2; правки оставлены в рабочей копии.