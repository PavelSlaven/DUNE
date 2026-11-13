## PRE-REVIEW-U33 | 2026-11-04 22:26:26 UTC | HEAD 0ce20a385fd6562bf277e2439de24a8c02874be9

Код и данные ветки не изменены, коммитов нет. `git status --short` до и после проверки пуст. [Отчёт, скрипты и результаты](/srv/dune/worktrees/u33/.tmp/pre-review-u33/report.md) сохранены только в `.tmp/pre-review-u33/`.

1. **Состав — чисто.** Ровно 20 разрешённых файлов. Подтверждение: `Diff paths match the 20 allowed files: True` в [structure-review.txt](/srv/dune/worktrees/u33/.tmp/pre-review-u33/structure-review.txt:2).

2. **Описание — чисто.** Старые поля и попытки сохранены; `body3`, `pick` и `recolour` правильны во всех восьми кадрах. Отступ — два пробела, diff ограничен разрешёнными участками. Медиана сборки `M=0.526`, коридор `[0.426, 0.626]`. Подтверждения: `indent_2_exact=True`, `all_other_json_fields_exact=True`, `corridor_matches=True`.

3. **Исходники и суммы — чисто.** Все 16 PNG побайтно совпали с выбранными B1a; хеши найдены в строках `copied`. В файле сумм 56 строк, 40 прежних сохранены, новые суммы верны, сортировка соблюдена. Подтверждение: `all 16 new file/log/hash checks=True`; пофайловые результаты — [structure-review.json](/srv/dune/worktrees/u33/.tmp/pre-review-u33/structure-review.json).

4. **Пак — чисто.** Хеши паков совпали с LFS-указателями соответствующих коммитов. Сборка завершилась с кодом 0, `all frames pass`. [Вывод сравнения](/srv/dune/worktrees/u33/.tmp/pre-review-u33/pack-audit-metrics.txt):

   ```text
   entry_count: base=241 head=241 equal=True
   entry_order_differences: 0; trailing_count_difference=0
   changed_payload_names: ['UNIT_LAUNCHER', 'HM_UNIT_LAUNCHER']
   payload_UNIT_LAUNCHER_SHADOW_identical: True
   build_vs_head_UNIT_LAUNCHER: size=(1024, 128) differing_pixels=0
   build_vs_head_HM_UNIT_LAUNCHER: size=(1024, 128) differing_pixels=0
   build_vs_head_UNIT_LAUNCHER_SHADOW: size=(1024, 128) differing_pixels=4591
   ```

   Отличие тени сборки ожидаемо.

5. **Числа — условия (а)–(г) выполнены; три находки.**

   | Атлас | eff | stdL_over_avg | clip для каждого из трёх Домов |
   |---|---:|---:|---:|
   | Ракетница HEAD | 0.502785340507 | 0.301964224288 | 0.006254815755 |
   | Девиатор HEAD | 0.315428576599 | 0.341433168345 | 0.030205514518 |

   `bbox_dev` по направлениям: `[1, 0, 0, 1, 0, 1, 0, 1]`. Пороги (б) и (г): `0.273146534676` и `0.080205514518`. Вывод независимого расчёта: `a_ok=True`, `b_ok=True`, `c_ok=True`, `d_ok=True`. Основные числа совпали со сдачей в пределах допуска.

   **F1.** [task.md:22](/srv/dune/tasks/u33/task.md:22) делит на `avg`, тогда как [FactionTint.hpp:14](/srv/dune/worktrees/u33/src/utils/FactionTint.hpp:14) использует `max(0.01F, averageLuminance)`. На проверенных атласах ограничение не активно: минимальный `avg=0.291625312238`, вывод `average_floor_active=False`.

   **F2.** [task.md:22](/srv/dune/tasks/u33/task.md:22) оставляет итоговую смесь вещественной. [Graphics.cpp:436](/srv/dune/worktrees/u33/src/utils/Graphics.cpp:436) преобразует смесь в `Uint8`, отсекая дробную часть. Остальные определения 3–6 совпали с движком. Влияние подтверждено строкой: `LAUNCHER_NEW ... cvY_literal=0.537186251528 cvY_engine=0.541285109260`.

   **F3.** [reply-03.txt:48](/srv/dune/tasks/u33/reply-03.txt:48), строки 48–52: все 15 значений `cvY` отличаются от расчёта по движку больше чем на `0.0005`. Причина — F2. Ниже перечислены все расхождения в формате «сдача → движок»:

   | Строка сдачи | Ордос | Атрейдес | Харконнен |
   |---|---|---|---|
   | 48, LAUNCHER_HEAD | 0.318509 → 0.320420 | 0.335468 → 0.339960 | 0.307814 → 0.310933 |
   | 49, LAUNCHER_NEW | 0.314115 → 0.315681 | 0.537186 → 0.541285 | 0.330761 → 0.332179 |
   | 50, DEVIATOR | 0.369006 → 0.370973 | 0.502816 → 0.506924 | 0.361524 → 0.364136 |
   | 51, TANKBASE | 0.293700 → 0.295208 | 0.402111 → 0.403875 | 0.287931 → 0.289891 |
   | 52, TANKTOP | 0.303385 → 0.305145 | 0.354218 → 0.356449 | 0.279605 → 0.282058 |

   Подтверждение: `engine_gt_0.0005_count=15/15 literal_gt_0.0005_count=0/15` в [numbers_results.txt](/srv/dune/worktrees/u33/.tmp/pre-review-u33/numbers_results.txt:115).

6. **Тест — ожидаемые результаты; одна находка.** Пороги правильны, Девиатор рассчитывается во время прогона. Метрики текущего пака совпали с независимыми: разницы `eff` и `clip` — ноль, разница `stdL_over_avg` не превышает `5.6e-17`.

   **F4.** [test_launcher_house_colour.py:39](/srv/dune/worktrees/u33/tools/units3d/tests/test_launcher_house_colour.py:39) рассчитывает `clip` без ограничения знаменателя `max(0.01, avg)`. Контрольный пример подтвердил отличие: `dark_probe avg=0.002335937500 test_clip=0.500000000000 engine_clip=0.000000000000`. На проверенных паках отличие не проявляется.

   Прогоны выполнены через `D2TM_PACK_DIR`, команда — `python -B -m unittest -v tools.units3d.tests.test_launcher_house_colour`.

   HEAD, [test-head.txt](/srv/dune/worktrees/u33/.tmp/pre-review-u33/test-head.txt):

   ```text
   Ran 3 tests in 1.069s
   OK
   exit_code=0
   ```

   База `40213771` из требуемого каталога `pack-before`, [test-before.txt](/srv/dune/worktrees/u33/.tmp/pre-review-u33/test-before.txt):

   ```text
   FAIL: test_launcher_effective_mask_is_between_045_and_055
   AssertionError: 0.41752351160481044 not greater than or equal to 0.45
   Ran 3 tests in 1.018s
   FAILED (failures=1)
   exit_code=1
   ```

   Методы `clip` и `luminance_ratio` прошли на обоих паках.

7. **Коммиты — три находки оформления.** Сообщения английские, последняя строка каждого — `Co-Authored-By`. Содержательные утверждения подтверждены диффами и измерениями во всех восьми направлениях.

   **F5.** Сообщение `4e7c144f:9`: предпоследняя физическая строка пустая, `Behavior changes:` находится выше. Подтверждение: `physical penultimate line 9=''`; [снимок сообщения:15](/srv/dune/worktrees/u33/.tmp/pre-review-u33/structure-commit-messages.txt:15).

   **F6.** Сообщение `e09af206:8`: предпоследняя физическая строка пустая. Дополнительно описание поведения перенесено на две строки: даже предпоследняя непустая строка начинается с `a larger area`, а не с `Behavior changes:`. Подтверждение: `physical penultimate line 8=''`, `behavior penultimate=False`; [снимок сообщения:29](/srv/dune/worktrees/u33/.tmp/pre-review-u33/structure-commit-messages.txt:29).

   **F7.** Сообщение `0ce20a38:9`: предпоследняя физическая строка пустая, `Behavior changes:` находится выше. Подтверждение: `physical penultimate line 9=''`; [снимок сообщения:48](/srv/dune/worktrees/u33/.tmp/pre-review-u33/structure-commit-messages.txt:48).

### Итог

**7 находок; F3 объединяет 15 перечисленных числовых расхождений одной причины. Блокирующих слияние находок нет.**

| Находка | Блокирует | Причина |
|---|---|---|
| F1 | Нет | Ограничение знаменателя не активно на проверенных атласах. |
| F2 | Нет | Неточность задания меняет справочный `cvY`, условия приёмки выполнены. |
| F3 | Нет | Ошибочны справочные числа сдачи, данные пака корректны. |
| F4 | Нет | Расхождение теста проявляется при `avg < 0.01`, чего нет в проверенных паках. |
| F5 | Нет | Нарушено только оформление сообщения коммита. |
| F6 | Нет | Нарушено только оформление сообщения коммита. |
| F7 | Нет | Нарушено только оформление сообщения коммита. |