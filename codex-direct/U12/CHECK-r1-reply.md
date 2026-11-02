## PLAN-U12-C

Проверить шесть пунктов возврата по `task-02.md` и шесть находок по строкам «Что ожидается» в `AUDIT.md`, учитывая согласованную рамку `task-03.md`. Три помощника `gpt-6-luna`, `xhigh` готовят независимые выписки по группам пунктов 1/5, 2/3 и 4; решения и вердикт принимает ведущий.

Прочитать документы, рабочий код и `git diff 34d51060`; проверить новые тесты на конкретных неверных реализациях рассуждением по коду. Использовать `git`, `rg`, `nl`, чтение AST и JSON. Файлы репозитория не менять; записывать только `.tmp/progress-u12c.md` и временное в `.tmp/u12c/`. Сборки, тесты и проверки ведущего не повторять. Завершить одним кругом самоаудита. Исполнение программы и визуальный результат проверка не охватывает.

## DONE-U12-C | 2026-11-02 15:20:10 UTC | HEAD 34d51060017e4766565857b95d325b2fa6a4c1b1

### Пункты

Обозначения: **Р** — пункт возврата `REVIEW-U12-01`, **А** — находка `AUDIT.md`.

| № | Решение | Доказательство |
|---|---|---|
| Р1 | закрыт | [_build:70](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_offset_shift.py:70) возвращает четыре результата без `df` и записи журнала; временная папка удаляется через cleanup на строке 21. |
| Р2 | закрыт | Перед обоими `TemporaryDirectory` добавлен `mkdir`: [строка 157](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_rotation.py:157), строка 166. |
| Р3 | **закрыт частично** | Входы, допуски и числовые утверждения соответствуют возврату. Однако [цикл на строке 90](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_rotation.py:90) и цикл на строке 104 не проверяют наличие восьми результатов. Ожидается проверка всех направлений 0–7; реализация, возвращающая только направление 0, проходит оба метода. Причина: **исполнитель**. |
| Р4 | закрыт | [Строка 159](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:159) проверяет требуемый текст; новый метод задаёт `[0,120]` на строке 171 и проверяет ненулевой код и `alpha вне клетки` на строках 197–198. |
| Р5 | закрыт | [redraw_common.py:247](/srv/dune/worktrees/u12/tools/units3d/redraw_common.py:247): запрет действует только для `build`, при наличии `offset_shift` и `scale == "fit"`. Ошибка начинается с `offset_shift:`; [redraw.py:57](/srv/dune/worktrees/u12/tools/units3d/redraw.py:57) возвращает код 2. Без `scale` сохраняется медианный масштаб: [redraw_build.py:127](/srv/dune/worktrees/u12/tools/units3d/redraw_build.py:127). Новый тест — [строка 224](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_offset_shift.py:224). |
| Р6 | закрыт | В [unit.json:138](/srv/dune/worktrees/u12/tools/units3d/units/UNIT_SIEGEBASE/unit.json:138) восстановлена запись `0.10`. |
| А1 | закрыт | [_build:70](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_offset_shift.py:70): проверка места и постоянные журналы удалены. |
| А2 | закрыт | [test_redraw_rotation.py:157](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_rotation.py:157), строка 166: родительская папка создаётся до временных каталогов. |
| А3 | закрыт | [Новые методы:86](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_rotation.py:86) используют медиану не 1 и опоры по разные стороны итога. Указанные неверные реализации нарушают утверждения на строках 92 и 102 соответственно. |
| А4 | **закрыт частично** | Случай выхода за клетку добавлен, но [строка 159](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:159) проверяет подстроку всего stderr. Предложенная в «Что ожидается» проверка начала сообщения `ValueError: shift:` отсутствует: подстрока может встретиться в исходной строке traceback. Ожидается проверка строки исключения. Причина: **исполнитель**. |
| А5 | закрыт | Выбран предусмотренный находкой запрет сочетания: [redraw_common.py:253](/srv/dune/worktrees/u12/tools/units3d/redraw_common.py:253). |
| А6 | закрыт | [unit.json:138](/srv/dune/worktrees/u12/tools/units3d/units/UNIT_SIEGEBASE/unit.json:138): исходная форма `0.10` восстановлена. |

### Новые находки

**Н1 — блокирует.** [test_redraw_rotation.py:90](/srv/dune/worktrees/u12/tools/units3d/tests/test_redraw_rotation.py:90), строка 104. Оба новых теста проходят при замене `return result` в `size_measurements` на `return result[:1]`: направление 0 правильно, циклы проверки остальных направлений пусты. Ожидается явная проверка `len(results) == 8` перед проверкой значений. Это основание частичного закрытия Р3. Причина: **исполнитель**.

**Н2 — не блокирует.** [test_squad_compose_shift.py:198](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:198). Новый тест может принять аварийное исключение за требуемую диагностику. Конкретная неверная реализация: в [compose.py:430](/srv/dune/worktrees/u12/codex-direct/U6/squads/compose.py:430) заменить `item['piece']` на отсутствующий `item['piece_id']`. Возникнет `KeyError`, но traceback напечатает исходную строку с `alpha вне клетки`; оба утверждения на строках 197–198 выполнятся. Ожидается проверка текста именно исключения `ValueError`. Причина: **исполнитель**.

**Н3 — не блокирует.** [test_squad_compose_shift.py:184](/srv/dune/worktrees/u12/tools/units3d/tests/test_squad_compose_shift.py:184). Выход за клетку проверяется только с `--mask`. Неверная реализация, выполняющая проверку границ лишь при `args.mask`, пройдёт новый тест; прежняя проверка тела использует допустимый сдвиг `[0,13]`. Для защиты обоих режимов ожидается случай `[0,120]` также без `--mask`. Причина: **исполнитель**.

Изменений поведения вне требований возврата в диффе не обнаружено.

### Вердикт

**ДОРАБОТКА:** Р3, А4 и блокирующая новая находка Н1.

### Коммиты

нет

### Не проверено

Сборки, тесты и мутанты не запускались по заданию. Выводы о неверных реализациях получены чтением кода. Проверки ведущего не повторялись. Один круг самоаудита выполнен; журнал — [.tmp/progress-u12c.md](/srv/dune/worktrees/u12/.tmp/progress-u12c.md).

### git status --short

```text
 M tools/units3d/redraw_common.py
 M tools/units3d/tests/test_redraw_offset_shift.py
 M tools/units3d/tests/test_redraw_rotation.py
 M tools/units3d/tests/test_squad_compose_shift.py
 M tools/units3d/units/UNIT_SIEGEBASE/unit.json
```

### Владельцу

Файлы репозитория не редактировал. Исполнителю требуется проверить наличие восьми результатов и уточнить проверку диагностического сообщения. Цель оставлена активной до приёмки ведущим.