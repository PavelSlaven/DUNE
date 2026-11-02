## DONE-U12-C-R2 | 2026-11-02 15:34:16 UTC | HEAD 34d51060017e4766565857b95d325b2fa6a4c1b1

### Пункты

| № | Решение | Доказательство |
|---|---|---|
| Р3 | закрыт | [test_redraw_rotation.py:90](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_rotation.py:90), строка 99: оба метода требуют восемь результатов до проверки значений. Направления 1–7 больше нельзя пропустить возвратом `result[:1]`. |
| А4 | закрыт | [test_squad_compose_shift.py:159](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:159): проверяется строка с началом `ValueError: shift: ожидается`. Совпадения с подстрокой исходного кода в traceback недостаточно. |
| Н1 | закрыт | [test_redraw_rotation.py:90](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_rotation.py:90), строка 99: неверный возврат `result[:1]` нарушает оба утверждения длины. |
| Н2 | закрыт | [test_squad_compose_shift.py:206](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:206): требуется строка `ValueError: alpha вне клетки…`. Прямой `KeyError` от отсутствующего `piece_id` проверку не проходит. |
| Н3 | закрыт | [test_squad_compose_shift.py:182](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:182): случай `[0,120]` выполняется для `mask` и `body`. Проверка границ только при `args.mask` нарушит утверждение ненулевого кода на строке 205. |

### Новые находки

**Н4 — не блокирует.** [test_squad_compose_shift.py:160](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:160), строка 207.

Поиск подходящей строки во всём stderr может принять предыдущий `ValueError` из цепочки исключений за завершающее исключение.

Конкретная неверная реализация: добавить в `main` обработчик вокруг вызова `args.func(args)`:

```python
except ValueError as error:
    raise KeyError("piece_id") from error
```

Traceback сохранит строку исходного `ValueError`, затем завершится `KeyError`. Утверждения префикса и ненулевого кода пройдут. Ожидается проверка типа завершающего исключения с сохранением поддержки многострочного сообщения.

Причина: **задание** — конструкция `any(line.startswith(...))` продиктована в `task-04.md`. В текущем `compose.py` описанного обработчика нет.

Изменений поведения продукта от правок R2 не обнаружено.

### Вердикт

**OK.** Р3, А4, Н1, Н2 и Н3 закрыты. Новая находка Н4 неблокирующая.

### Не проверено

Сборки, тесты и дополнительные мутанты не запускались. Вывод о Н4 получен чтением тестов и реализации форматирования цепочек исключений Python. Проверки ведущего не повторялись.

Один круг самоаудита завершён. Журнал дополнен: [.tmp/progress-u12c.md](/srv/dune/worktrees/u12/.tmp/progress-u12c.md). Файлы репозитория не изменял, коммитов нет. Цель оставлена активной до приёмки.