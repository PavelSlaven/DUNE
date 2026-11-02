## DONE-U12-R1 | 2026-11-02 15:10:48 UTC | HEAD 34d51060017e4766565857b95d325b2fa6a4c1b1

Все шесть пунктов исправлены. Полный прогон: **267 тестов, OK, пропусков 0**. Все пять неверных реализаций пойманы. Изменены только пять разрешённых файлов; коммитов не делал.

### Журнал хода

Строки U12-R1 из [.tmp/progress.md](/srv/dune/worktrees/u12/.tmp/progress.md):

```text
U12-R1 — Пункт 1: удалены проверка доступного места и запись тестовых журналов из _build; коммит: инструмент с тестами.
U12-R1 — Пункт 5: load_unit запрещает offset_shift при scale=fit, добавлен тест на ошибку ввода; коммит: инструмент с тестами.
2026-11-02T14:30:48.008094+00:00 — U12-R1: PLAN-OK получен; HEAD 34d51060017e4766565857b95d325b2fa6a4c1b1 и чистота копии подтверждены, аудит ведущего прочитан для справки; сохранены пять исходных файлов и список 74 существующих журналов u12-offset-*.log; начаты три параллельные группы правок.
2026-11-02T14:30:48.264991+00:00 — U12-R1 пункт 6: в share_corridor Осадного возвращена запись 0.10; только одна строка отличается от HEAD, значения JSON равны; коммит: форма описания Осадного.
U12-R1 п4: добавлен test_shift_outside_cell_is_rejected; заголовок коммита: тесты сборщика отрядов.
U12-R1 прогон: test_squad_compose_shift.py — 2 теста OK; лог .tmp/u12-r1-squad-tests.log.
U12-R1 — Целевой unittest tools.units3d.tests.test_redraw_offset_shift: Ran 6 tests, OK, code=0; лог .tmp/u12-r1-offset-tests.log; коммит: инструмент с тестами.
2026-11-02T14:33:41.073684+00:00 — U12-R1 пункт 2: два CLI-теста rotation создают ROOT/.tmp перед TemporaryDirectory; коммит: инструмент с тестами; проверка: отдельный запуск файла и последующий запуск в копии без .tmp.
2026-11-02T14:33:41.073684+00:00 — U12-R1 пункт 3: добавлены отдельные методы для общего отклонения всех направлений и опор по разные стороны итога; прежние расчётные методы тестов сохранены; коммит: инструмент с тестами.
2026-11-02T14:33:41.073684+00:00 — U12-R1 прогон rotation: Ran 13 tests in 0.854s, OK, код 0; коммит: инструмент с тестами; лог .tmp/u12-r1-rotation-tests.log.
U12-R1 мутант compose: test_shift_outside_cell_is_rejected ожидаемо упал с AssertionError: 0 == 0; CLI копии вернул код 0; лог .tmp/u12-r1-mutants/compose-final-cell/test.log.
2026-11-02T14:35:01Z — U12-R1 mutant support-normalisation: code=1, failures=1, errors=0; log .tmp/u12-r1-mutants/support-normalisation/tools/units3d/test.log; коммит: инструмент с тестами.
2026-11-02T14:35:05Z — U12-R1 mutant all-normalisation: code=1, failures=1, errors=0; log .tmp/u12-r1-mutants/all-normalisation/tools/units3d/test.log; коммит: инструмент с тестами.
2026-11-02T14:35:09Z — U12-R1 mutant agreement-direction: code=1, failures=1, errors=0; log .tmp/u12-r1-mutants/agreement-direction/tools/units3d/test.log; коммит: инструмент с тестами.
U12-R1 — Мутант fit вместе с offset_shift пойман: code=1, failures=1, errors=0, AssertionError: 0 != 2; полный лог .tmp/u12-r1-mutants/fit-combination/test.log; коммит: инструмент с тестами.
U12-R1 — Рабочая реализация без scale с offset_shift=[0,5]: code=0, all frames pass (16), выбран медианный scale 1.0000; лог .tmp/u12-r1-offset-no-scale.log; коммит: инструмент с тестами.
2026-11-02T14:36:52.980589+00:00 — U12-R1 прогон сумм: frozen.sha256 и ACCEPTANCE.sha256, все строки OK; коммиты: инструмент с тестами/тесты сборщика отрядов/форма описания Осадного; логи .tmp/u12-r1-frozen.log, .tmp/u12-r1-acceptance.log.
2026-11-02T14:36:53.523414+00:00 — U12-R1 прогон копии без .tmp, файл из 34d51060: ожидаемый code=1 и две FileNotFoundError; лог .tmp/u12-r1-copy-before.log; коммит: инструмент с тестами.
2026-11-02T14:36:54.790743+00:00 — U12-R1 прогон исправленного файла в копии без .tmp: code=0, OK; лог .tmp/u12-r1-copy-after.log; коммит: инструмент с тестами.
2026-11-02T14:38:14.511811+00:00 — U12-R1 начат полный Python-прогон с пределом 3600 с; df перед запуском показывает 13G; лог .tmp/u12-r1-unittest.log.
2026-11-02T15:07:11.995949+00:00 — U12-R1 полный Python-прогон завершён: Ran 267 tests in 1736.715s, OK, пропусков 0, code=0; журналов u12-offset-*.log до=74, после=74, новых=0; коммиты: инструмент с тестами/тесты сборщика отрядов/форма описания Осадного; логи .tmp/u12-r1-unittest.log и .tmp/u12-r1-full-check.log.
2026-11-02T15:08:33Z — U12-R1 самоаудит: разрешённые изменения, AST, JSON, логи и git-состояние подтверждены; HEAD 34d51060017e4766565857b95d325b2fa6a4c1b1; коммит: инструмент с тестами.
```

### Коммиты

Предлагаемый коммит 1:

```text
Уточнить проверки сдвига и поворота

Тест сборки больше не запускает df и не оставляет журналы.
Добавлены проверки нормализации, стороны отклонения и запуска rotation без .tmp.

Behavior changes: build запрещает offset_shift при scale="fit"; описание без scale продолжает использовать медианный масштаб.
```

Файлы:

```text
tools/units3d/redraw_common.py
tools/units3d/tests/test_redraw_offset_shift.py
tools/units3d/tests/test_redraw_rotation.py
```

Предлагаемый коммит 2:

```text
Проверить выход фигур отряда за границы после сдвига

Добавлен случай shift [0,120] и уточнено ожидаемое сообщение для недопустимых значений.

Behavior changes: none
```

Файл:

```text
tools/units3d/tests/test_squad_compose_shift.py
```

Предлагаемый коммит 3:

```text
Восстановить запись 0.10 в описании Осадного

Значения JSON сохранены, изменена только форма одной строки.

Behavior changes: none
```

Файл:

```text
tools/units3d/units/UNIT_SIEGEBASE/unit.json
```

### Проверки

Обе проверки сумм завершились успешно; все строки `OK`:

```text
R1_FROZEN: 49/49 OK
R1_ACCEPTANCE: 7/7 OK
```

Полные выводы: [frozen.sha256](/srv/dune/worktrees/u12/.tmp/u12-r1-frozen.log), [ACCEPTANCE.sha256](/srv/dune/worktrees/u12/.tmp/u12-r1-acceptance.log).

Полный заданный Python-прогон — [журнал](/srv/dune/worktrees/u12/.tmp/u12-r1-unittest.log):

```text
Ran 267 tests in 1736.715s

OK
```

Код выхода 0, пропусков 0. Перед запуском `df -BG /` показывал 13G доступно.

Отсутствие новых журналов — [сводка](/srv/dune/worktrees/u12/.tmp/u12-r1-full-check.log):

```text
FULL_PYTHON_EXIT: 0
OFFSET_LOGS: before=74 after=74 new=0
NEW_OFFSET_LOGS: []
```

Запуск в копии без `.tmp` — [сводка](/srv/dune/worktrees/u12/.tmp/u12-r1-copy-check.log):

```text
COPY_34d51060: exit=1, FileNotFoundError=2
FileNotFoundError: [Errno 2] No such file or directory: '/srv/dune/worktrees/u12/.tmp/u12-r1-copy/.tmp/tmp89r4lh4f'
FileNotFoundError: [Errno 2] No such file or directory: '/srv/dune/worktrees/u12/.tmp/u12-r1-copy/.tmp/tmpuugz98g9'
COPY_FIXED: exit=0
Ran 13 tests in 0.790s
OK
COPY_REMOVED: True
```

Рабочая реализация без поля `scale`, со сдвигом `[0,5]`, успешно использовала медианный масштаб — [журнал](/srv/dune/worktrees/u12/.tmp/u12-r1-offset-no-scale.log):

```text
code=0
scale 1.0000
all frames pass: 16
```

### Пять неверных реализаций

Каждая проверена в отдельной копии модуля. В каждом прогоне получен один провал утверждения, ошибок запуска нет.

| Неверная реализация | Тест | Фактическая строка провала |
|---|---|---|
| [Без нормализации опор](/srv/dune/worktrees/u12/.tmp/u12-r1-mutants/support-normalisation/tools/units3d/test.log) | `test_uniform_deviation_is_normalised` | `AssertionError: 1.1 != 1.0 within 0.001 delta (0.10000000000000009 difference)` |
| [Без нормализации опор и итога](/srv/dune/worktrees/u12/.tmp/u12-r1-mutants/all-normalisation/tools/units3d/test.log) | `test_uniform_deviation_is_normalised` | `AssertionError: 1.1 != 1.0 within 0.001 delta (0.10000000000000009 difference)` |
| [Подсчёт опор без учёта стороны](/srv/dune/worktrees/u12/.tmp/u12-r1-mutants/agreement-direction/tools/units3d/test.log) | `test_opposite_support_does_not_agree` | `AssertionError: 2 != 1` |
| [Сдвиг готовой клетки отряда](/srv/dune/worktrees/u12/.tmp/u12-r1-mutants/compose-final-cell/test.log) | `test_shift_outside_cell_is_rejected` | `AssertionError: 0 == 0` |
| [Отсутствие запрета fit со сдвигом](/srv/dune/worktrees/u12/.tmp/u12-r1-mutants/fit-combination/test.log) | `test_fit_scale_rejects_offset_shift` | `AssertionError: 0 != 2 : scale 1.0000` |

Копии сверены с рабочими модулями: каждая содержит только назначенную ошибку.

### Самоаудит

[Один круг самоаудита](/srv/dune/worktrees/u12/.tmp/u12-r1-audit.log) завершился успешно:

- изменены ровно пять разрешённых файлов;
- прежние методы тестов сохранены за исключением явно разрешённых правок;
- в `redraw_common.py` добавлен только запрет сочетания полей;
- в описании Осадного изменена только строка `0.1 → 0.10`, значения JSON равны HEAD;
- подтверждены все журналы, пять провалов и отсутствие новых offset-журналов;
- `git diff --check 34d51060` пуст, код 0.

Для Git использовались требуемый `PATH` и временный `lfs.storage` внутри `.tmp/`. Конфигурация репозитория не менялась.

### Не проверено

Запуски на Windows и macOS не выполнялись; проверки проведены в Linux. Сборку C++, CTest и пересборку пака не повторял: они не входят в возврат R1, соответствующие файлы сохранены.

### Рабочие места

Рабочая копия — `/srv/dune/worktrees/u12`, ветка `codex/u12-rotation`. Три субагента `gpt-6-luna`, `xhigh` завершили поручения; отдельных рабочих копий Git не создавали.

Артефакты находятся в `.tmp/u12-r1-*` и `.tmp/u12-r1-mutants/`. Папка `.tmp/u12-r1-copy` удалена. Активных тестовых процессов не осталось.

### git status --short

```text
 M tools/units3d/redraw_common.py
 M tools/units3d/tests/test_redraw_offset_shift.py
 M tools/units3d/tests/test_redraw_rotation.py
 M tools/units3d/tests/test_squad_compose_shift.py
 M tools/units3d/units/UNIT_SIEGEBASE/unit.json
```

### Владельцу

1. Исправлены все шесть пунктов возврата; проверки прошли.
2. Принятые пак, сборщик отрядов и остальные данные не менялись. Коммиты не созданы.
3. Нужны приёмка R1 и создание перечисленных коммитов ведущим. Цель оставлена активной до приёмки.