## DONE-U9-I2-R1 | 2026-11-02 14:22:44 UTC | HEAD e0c9e67c366e63ef73385af30f4ca9438c31f460

Исправлены все четыре пункта возврата. Полный Python-набор прошёл: **254 теста, `OK`, пропусков 0**. Изменены ровно четыре разрешённых файла. Коммитов не создавал.

### Журнал хода

Полный [журнал](/srv/dune/worktrees/u9f/.tmp/progress.md) содержит все прогоны, исправления ошибок запуска, код скрипта сравнения Markdown и полный вывод до/после. Итоговые записи текущего возврата:

```text
2026-11-02 13:48:52 UTC — U9-I2-R1 итоговые доводки: lower-HD фикстура теперь использует `23`; Markdown-тест отдельно проверяет отсутствие повторов, число 6, порядок списка и целую строку draw_order. Целевой файл: exit 0, Ran 8, OK (.tmp/u9i2-r1-final-branches-green.log). Группа коммита «контракт».
2026-11-02 13:49:00 UTC — U9-I2-R1 финальная мутация lower_hd: exit 1, AssertionError подтверждён; лог .tmp/u9i2-r1-mutation-final-lower_hd.log. Группа коммита «контракт».
2026-11-02 13:49:01 UTC — U9-I2-R1 финальная мутация integer_only: exit 1, AssertionError подтверждён; лог .tmp/u9i2-r1-mutation-final-integer_only.log. Группа коммита «контракт».
2026-11-02 13:49:01 UTC — U9-I2-R1 финальная мутация always_float: exit 1, AssertionError подтверждён; лог .tmp/u9i2-r1-mutation-final-always_float.log. Группа коммита «контракт».
2026-11-02 13:49:02 UTC — U9-I2-R1 финальная мутация allow_fractional: exit 1, AssertionError подтверждён; лог .tmp/u9i2-r1-mutation-final-allow_fractional.log. Группа коммита «контракт».
2026-11-02 13:49:03 UTC — U9-I2-R1 финальная мутация keep_duplicates: exit 1, AssertionError подтверждён; лог .tmp/u9i2-r1-mutation-final-keep_duplicates.log. Группа коммита «контракт».
2026-11-02 13:49:03 UTC — U9-I2-R1 финальная мутация limit_three: exit 1, AssertionError подтверждён; лог .tmp/u9i2-r1-mutation-final-limit_three.log. Группа коммита «контракт».
2026-11-02 13:51:19 UTC | U9-I2-R1 | Целевой тест прошёл на правильном инструменте; проверка масштаба и all frames pass успешны | тест fit
2026-11-02 13:51:37 UTC | U9-I2-R1 | Мутант без проверки перекраски упал требуемой проверкой масштаба с AssertionError: False is not true : Подобранный масштаб должен ограничиваться перекраской | тест fit
2026-11-02 13:52:37 UTC — U9-I2-R1 пункт 3, генерация: exit 0; JSON побайтно равен e0c9e67c, Markdown сохраняет 123 строки и меняет только пять ячеек ссылок. Коммит: контракт.
2026-11-02 13:52:37 UTC — U9-I2-R1, скрипт сравнения строк: PYTHONDONTWRITEBYTECODE=1 /srv/dune/venv/bin/python .tmp/u9i2-r1-compare-contract.py; exit 0. Код скрипта и вывод до/после:
2026-11-02 13:53:26 UTC — U9-I2-R1 финальная проверка ACCEPTANCE: exit 0, 7/7 OK; git diff --check e0c9e67c: exit 0, вывод пуст. Коммиты: контракт, тест fit.
2026-11-02 14:21:24 UTC | U9-I2-R1 | Полный Python-прогон: exit=0, Ran 254 tests in 1681.779s, OK, skipped=0 | unittest discover tools/units3d/tests
2026-11-02 14:22:44 UTC — U9-I2-R1 самоаудит одним кругом: PASS; ровно четыре разрешённых файла, прежние методы тестов побайтно сохранены, шесть новых тестов, JSON равен HEAD, изменены только пять ячеек ссылок, независимый fit-scale 0.981112449799197 и семь мутаций подтверждены; Python 254 OK, skipped 0, ACCEPTANCE 7/7, diff check пуст. Коммиты: контракт, тест fit.
```

### Коммиты

1. Контракт и его тесты.

```text
Разбирать полные смещения CARRYALL и показывать все источники контракта

Behavior changes: генератор сравнивает полные числовые смещения, отклоняет одинаковые дробные значения и возвращает int для целых; Markdown сохраняет все уникальные ссылки в исходном порядке.
```

```text
tools/units3d/unit_contract.py
tools/units3d/tests/test_unit_contract_branches.py
docs/units/UNIT_CONTRACT.md
```

2. Проверка ограничения `fit` перекраской.

```text
Проверить ограничение fit геометрией перекраски

Behavior changes: none
```

```text
tools/units3d/tests/test_redraw_frame_scale.py
```

### Проверки

ACCEPTANCE, код выхода 0:

```text
tools/units3d/check_unit.py: OK
tools/units3d/tests/test_check_unit.py: OK
tools/units3d/tests/test_redraw.py: OK
tools/units3d/tests/test_siege_frame.py: OK
tools/units3d/tests/test_install_geometry.py: OK
tools/units3d/tests/test_siege_contract.py: OK
tools/units3d/tests/test_unit_contract.py: OK
```

Полный Python-прогон, код выхода 0:

```text
Ran 254 tests in 1681.779s
OK
```

Пропусков 0. Лог: [.tmp/u9i2-r1-python-full.log](/srv/dune/worktrees/u9f/.tmp/u9i2-r1-python-full.log).

`git diff --check e0c9e67c` — код выхода 0, вывод пуст. Git запускался с указанным в задании путём к `git-lfs`.

Самоаудит выполнен одним кругом:

```text
Single self-audit: PASS
```

Проверено побайтное сохранение всех прежних методов обоих тестовых файлов. Добавлены шесть новых методов тестов.

### Контракт и Markdown

```text
unit_contract.json: byte-for-byte identical to e0c9e67c; PASS
Markdown: 123 lines; 5 link cells changed; all other bytes preserved; PASS
```

Изменились только ячейки источников:

| Правило | Ссылок до → после |
|---|---:|
| `source_rectangle` | 3 → 10 |
| `draw_order` | 3 → 6 |
| `draw_destination` | 3 → 6 |
| `direction_columns` | 3 → 14 |
| `hd_house_masks` | 3 → 53 |

Порядок первых появлений сохранён, повторы исключены. [Скрипт сравнения](/srv/dune/worktrees/u9f/.tmp/u9i2-r1-compare-contract.py) и [полный вывод до/после](/srv/dune/worktrees/u9f/.tmp/u9i2-r1-compare-contract.log) также внесены в журнал.

### Неверные реализации

Каждая проверена отдельно в копии модуля внутри `.tmp/`. Все семь прогонов завершились кодом 1 из-за ожидаемого `AssertionError`.

| Неверная реализация | Тест | Фактическая строка провала |
|---|---|---|
| Сравнение `>` вместо `!=` | `test_carryall_rejects_lower_hd_offset` | `AssertionError: ValueError not raised` |
| Чтение только целой части | `test_carryall_rejects_fractional_hd_offset` | `AssertionError: ValueError not raised` |
| Возврат `float` для целого | `test_carryall_integral_float_literals_return_int` | `AssertionError: <class 'float'> is not <class 'int'>` |
| Разрешение одинаковых дробных смещений | `test_carryall_rejects_equal_fractional_offsets` | `AssertionError: ValueError not raised` |
| Сохранён предел трёх ссылок | `test_markdown_draw_order_keeps_all_unique_sources` | `AssertionError: 3 != 6` |
| Сохранены повторные ссылки | `test_markdown_draw_order_keeps_all_unique_sources` | `AssertionError: False is not true : Повторные ссылки должны быть исключены` |
| В `fits()` не проверяется обрезка перекраски | `test_fit_scale_is_limited_by_recolour_bounds` | `AssertionError: False is not true : Подобранный масштаб должен ограничиваться перекраской` |

В тесте `fit` ожидаемый масштаб независимо вычислен из геометрии фикстуры: **0,981112449799197**, 47 шагов. На выбранном масштабе размер холста — 512; на следующем — 513. Проверки подтверждают, что тело на следующем шаге помещается, а перекраска обрезается.

### Не проверено

Повторная сборка C++, CTest и визуальная проверка игры не выполнялись: этот возврат меняет генератор, Markdown и тесты. Пак, движок и алгоритм сборщика сохранены.

### Рабочие места

- Основная копия: `/srv/dune/worktrees/u9f`, ветка `codex/u9-frame`.
- Мутации контракта: `.tmp/u9i2-r1-mutants/`.
- Мутация `fit`: `.tmp/u9i2-r1-mutation-no-recolour/`.
- Логи: `.tmp/u9i2-r1-*.log`.
- [Итог самоаудита](/srv/dune/worktrees/u9f/.tmp/u9i2-r1-self-audit.log).

### git status --short

```text
 M docs/units/UNIT_CONTRACT.md
 M tools/units3d/tests/test_redraw_frame_scale.py
 M tools/units3d/tests/test_unit_contract_branches.py
 M tools/units3d/unit_contract.py
```

### Владельцу

1. Дробные различия смещений теперь обнаруживаются; Markdown показывает все источники; новый тест ловит пропуск проверки перекраски при `fit`.
2. Коммиты не создавались. Непроверенных требований этого возврата нет.
3. Нужны приёмка доработки и создание двух коммитов по списку. Цель оставлена активной до приёмки.