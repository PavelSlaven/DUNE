# U14: пересборка Харвестера в масштабе 0,75

Рабочая копия `/srv/dune/worktrees/u12`, ветка `codex/u14-harvester`, HEAD `3f1829b81fe8183a7d02e60c3ca44a2ad460d908`. Пак до установки: `.tmp/out-c/pack-before.dat`, sha256 `263d6c6efeca8e1958dc12b2c4afebe738c47ab0cecb0bd6aa58fa440bc3f527`. Пак после: sha256 `700fd0a3dc13755d3c17649d1f369075c161c5c78d2964f4d6d06af217500eb4`.

## Входы и масштаб

- Входы: готовые изображения Харвестера из `units-gen/UNIT_HARVESTER` (генерация не запускалась). Пути рядов 1-3 в закоммиченном `unit.json` ведут в `units-gen/UNIT_HARVESTER/cut/...` (обрезка первой сборки), поэтому полную сборку шага 4 вёл временный `.tmp/u14/unit-full/unit.json`, у которого пути рядов 1-3 заменены на `.tmp/out-c/cut/`. Закоммиченный `unit.json` изменён одной строкой: `"scale": 1.057526` -> `"scale": 0.793144` (0,75 от прежнего).
- Остальные поля `unit.json` не менялись.

## Шаг 2: ряд 0

Сборка одного ряда 0 (`.tmp/u14/unit-row0/unit.json`, `"rows": 1`) в `.tmp/out-c/row0/`, код выхода 0, все кадры `ok`. `scale` 0.793144, `scale_median` 1.0093486521123278, сторона холста в кадре `s = round(320 x 0.793144) = 254`. Смещения `offset` (dx, dy): r0k0 (40, 1); r0k1 (36, -9); r0k2 (33, -32); r0k3 (32, -14); r0k4 (58, 0); r0k5 (43, -14); r0k6 (34, -20); r0k7 (32, -16).

## Шаг 3: обрезка шлейфа во входах

Правило: для каждой записи (r, k) рядов 1-3 и каждой попытки `a`, `b` пиксель холста 1024 x 1024 переводится в точку кадра x = (X + 0,5) * s / 1024 + dx - 0,5 (так же по y); d = min(x, y, 319 - x, 207 - y); множество Z - пиксели с d < 4, у которых пиксель выбранной попытки ряда 0 (pick из `params.json`) - фон (расстояние RGB от (255, 0, 255) не больше 60); эти пиксели закрашиваются (255, 0, 255). Скрипт - копия `codex-direct/U5/cut.py` в `.tmp/u14/cut.py`, отличие только в путях: `row0-b/params.json` -> `row0/params.json` и журнал скрипта `.tmp/progress-c.md` -> `.tmp/u14/script-progress.md` (diff в `.tmp/u14/cut.diff`).

Результат: 48 масок, 96 PNG в `.tmp/out-c/cut/`, s = 254. Число пикселей Z: 227328 у 42 записей, 226304 у шести записей k1 (r1k1, r2k1, r3k1, обе попытки). Z считается по всему холсту 1024 x 1024, включая пиксели, которые после уменьшения лежат за кадром, поэтому числа велики и почти одинаковы. Полный список - `.tmp/out-c/cut.log`.

## Шаг 4: полная сборка

`.tmp/out-c/build/`, код выхода 0, 32 кадра `ok`, ячейка iou 0.995..0.999, stray 0 везде. Строки `metrics.txt`:

```
row	k	pick	iou	share	old_share	stray	ok
0	0	a	0.998	0.459	0.482	0	True
0	1	a	0.998	0.421	0.489	0	True
0	2	b	0.999	0.485	0.537	0	True
0	3	a	0.996	0.423	0.495	0	True
0	4	a	0.998	0.467	0.475	0	True
0	5	b	0.998	0.428	0.523	0	True
0	6	b	0.998	0.499	0.582	0	True
0	7	a	0.995	0.452	0.503	0	True
1	0	a	0.998	0.392	0.414	0	True
1	1	b	0.999	0.361	0.416	0	True
1	2	a	0.999	0.413	0.477	0	True
1	3	a	0.997	0.354	0.400	0	True
1	4	a	0.998	0.395	0.459	0	True
1	5	a	0.998	0.362	0.461	0	True
1	6	b	0.999	0.452	0.478	0	True
1	7	b	0.996	0.399	0.454	0	True
2	0	a	0.998	0.380	0.412	0	True
2	1	b	0.999	0.361	0.411	0	True
2	2	b	0.999	0.416	0.485	0	True
2	3	b	0.997	0.365	0.417	0	True
2	4	b	0.998	0.391	0.447	0	True
2	5	a	0.998	0.360	0.465	0	True
2	6	b	0.999	0.457	0.499	0	True
2	7	b	0.996	0.401	0.454	0	True
3	0	a	0.998	0.381	0.398	0	True
3	1	b	0.999	0.362	0.409	0	True
3	2	b	0.999	0.410	0.465	0	True
3	3	a	0.997	0.365	0.405	0	True
3	4	a	0.998	0.396	0.446	0	True
3	5	b	0.998	0.361	0.464	0	True
3	6	b	0.999	0.449	0.481	0	True
3	7	b	0.996	0.396	0.447	0	True
corridor	0.34811	0.63164	set
all frames pass
```

## Шаг 5: затухание у края

Правило (принятое в первой сборке, ответ ведущего `codex-direct/U5/ANSWER-pack-02.md`): d = min(x, y, 319 - x, 207 - y); m = clip((d - 4) / 20, 0, 1); альфа тела A' = A, если H > 0 или d >= 24, иначе A' = round(A * m), где H - альфа тела кадра (0, k) в той же точке; RGB тела не меняется; альфа маски Дома = min(альфа маски, A'); тень кадра заново из нового тела по `shadow_rule` (сдвиг 7 px, RGB 7/5/3, альфа = round(A' * 51 / 255)); ряд 0 не меняется. Скрипт - копия `codex-direct/U5/fade.py` в `.tmp/u14/fade.py`, отличие только в пути журнала скрипта (diff в `.tmp/u14/fade.diff`). Результат - `.tmp/out-c/final/` (три атласа 2560 x 832 и `atlases.json`).

Сверки скрипта (`.tmp/out-c/fade.log`), все 0, итог PASS:

```
row0_pixel_differences: {"body": 0, "house_mask": 0, "shadow": 0}
row0_shadow_rebuild_pixel_differences: 0
rows1_3_alpha_formula_violations: 0
rows1_3_A_changed_where_H_positive_or_d_ge_24: 0
rows1_3_A_nonzero_for_d_lt_4_and_H_zero: 0
rows1_3_body_pixel_differences_at_d_ge_24: 0
rows1_3_body_RGB_differences: 0
rows1_3_mask_alpha_formula_violations: 0
rows1_3_mask_alpha_above_body: 0
final_png_roundtrip_pixel_differences: 0
result: PASS
```

Дополнительно, сверка старой формулировки «A' >= H всюду» (в ответе ведущего она заменена на «A' = A, где H > 0 или d >= 24»): в рядах 1-3 финального атласа 3221 пиксель с A' < H. Все они уже есть в сборке шага 4 (в составном кадре альфа ниже, чем в корпусе ряда 0); `fade.py` их не создаёт и по принятому правилу не трогает.

## Шаг 6: пак

`install.py --atlases .tmp/out-c/final --pack resources/bin/data/sdl_data_hd4.dat`, код выхода 0. Сверка скриптом `.tmp/u14/pack_verify.py` (лог `.tmp/u14/pack-verify.log`): 241 запись до и после, изменились ровно три записи, размеры атласов прежние (2560 x 832), остальные 238 записей совпадают байт в байт, имена уникальны, PASS. sha256 нагрузки трёх записей (нагрузка - PNG; новые хэши совпадают с `.tmp/out-c/final/atlases.json`):

| запись | было | стало |
|---|---|---|
| UNIT_HARVESTER | `3d1df72b2cf00b23b3c3e0b9bd5b516892efb8b46e9d4c52f13bc6d3cab9a2ed` | `32930763ad75bb10401129c987e52cf5e88703e8bb6c0a8385c37d666c2a52f6` |
| HM_UNIT_HARVESTER | `a8cfa86759e243671551280eb2391886cbc640362c691c230a9bb1683a703680` | `c77d86643194315bf668b927d4d39a4ac8ec5061cf14b14acebbe65174381019` |
| UNIT_HARVESTER_SHADOW | `4d6737a6637c0b0c3e7839283d7515ba837fa67aa9297f401405ee12e51e3c89` | `54196c1cc6c611fffcd4e1a96359fa3aa9a40f8c8a786c601cecc19880204be4` |

Размеры нагрузки в байтах (было -> стало): 2053416 -> 1328537, 338481 -> 248479, 107114 -> 94961.

## Шаг 7: проверки

7.1 Площадка: `/srv/dune/venv/bin/python /srv/dune/tasks/u14/pad_check.py resources/bin/data/sdl_data_hd4.dat .tmp/u14/pad-after.png`, код выхода 0:

```
body 103x151 at (229, 92, 331, 242); pad (186, 84, 362, 251); margins left,top,right,bottom (43, 8, 31, 9)
```

Корпус k6 был 136 x 199, стал 103 x 151; минимальный запас 8 px при требуемых 6.

7.2 Поворот: `redraw.py rotation` для `pack-before.dat` и нового пака (`.tmp/u14/rot-before.tsv`, `.tmp/u14/rot-after.tsv`, по 170 строк). Скрипт `.tmp/u14/rot_check.py`, код выхода 0: строки других юнитов (162) побайтно равны; у 8 строк `UNIT_HARVESTER` в новом файле нет флагов `size` и `middle`. Колонки: unit, k, classic, old, block, combined, agree, flag.

```
до:   UNIT_HARVESTER 6  1.055 1.037 1.063 1.054 2 size   (остальные k: флаг -)
после:
UNIT_HARVESTER	0	0.985	0.938	1.036	0.989	1	-
UNIT_HARVESTER	1	1.016	1.008	0.970	1.001	0	-
UNIT_HARVESTER	2	1.029	1.046	1.039	1.042	0	-
UNIT_HARVESTER	3	1.015	1.000	0.970	0.999	0	-
UNIT_HARVESTER	4	0.979	1.000	1.030	1.006	0	-
UNIT_HARVESTER	5	0.974	0.947	0.936	0.956	2	-
UNIT_HARVESTER	6	1.058	1.027	1.042	1.046	1	-
UNIT_HARVESTER	7	0.978	0.941	0.941	0.957	2	-
```

Полные строки до - в `.tmp/u14/rot-before.tsv`.

7.3 Размер: `.tmp/u14/size_check.py`, вывод `.tmp/u14/size-check.out`. Ограничивающий прямоугольник пикселей ряда 0 по альфе >= 1 (старый -> новый, отношения ширины и высоты):

```
k0 191x143 -> 145x108  0.759 0.755
k1 173x193 -> 132x146  0.763 0.756
k2 126x202 ->  96x153  0.762 0.757
k3 171x194 -> 130x148  0.760 0.763
k4 191x146 -> 145x112  0.759 0.767
k5 158x180 -> 120x138  0.759 0.767
k6 136x199 -> 103x151  0.757 0.759
k7 163x193 -> 124x146  0.761 0.756
```

По альфе >= 128 отношения 0.747-0.755. Кадров вне 0.70-0.80 нет.

7.4 Тесты C++: `cmake --build .tmp/u12-cpp-build -j 32`, код 0 (`.tmp/u14/cpp-build.rc`); `ctest --output-on-failure` (SDL dummy), код 0 (`.tmp/u14/ctest.rc`): `100% tests passed, 0 tests failed out of 25`.

7.5 Тесты инструмента (`tools/units3d/tests`, 275 тестов): `pytest` на сервере не установлен (`No module named pytest`, код 1), поэтому `unittest`.

- Одним процессом `python -m unittest discover -s tools/units3d/tests` тесты шли около 20 минут и до конца не дошли (каждый тест строит синтетический юнит; число завершённых тестов по логу не установлено); прогон остановлен командой `kill`, лог - `.tmp/u14/unittest-sequential-aborted.log`.
- Вместо него: идентификаторы всех 275 тестов получены загрузчиком `discover` (`.tmp/u14/test-ids.txt`), каждый запущен отдельным процессом `PYTHONPATH=tools/units3d/tests python -m unittest <id>`, по 16 процессов разом; логи и коды выхода - `.tmp/u14/tests/`.
- Прогон 1, без `D2TM_PACK_DIR`: 274 теста с кодом 0, один с кодом 1 - `test_siege_contract.SiegeContractAcceptanceTests.test_generator_and_checker_siege_geometry`, `KeyError: 'D2TM_PACK_DIR'` (тест Осадного юнита берёт копию пака из этой переменной и без неё падает, а не пропускается; это записано в `codex-direct/U9/AUDIT-tests.md`). Логи - `.tmp/u14/tests-pass1/`.
- Прогон 2, как предписано в `codex-direct/U9/TASK-impl.md`: `PYTHONPATH=tools/units3d/tests PYTHONDONTWRITEBYTECODE=1 TMPDIR=$PWD/.tmp/u14/tmp D2TM_PACK_DIR=$PWD/resources/bin/data`, тот же способ запуска: 275 из 275 с кодом 0, в каждом логе `OK`, слова `skipped` нет, 228 с. Тесты, читающие `resources/bin/data/sdl_data_hd4.dat`, в этом прогоне работают на новом паке.
- После обоих прогонов `git status --short` показывает те же два изменённых файла, лишнего нет.

## Листы

`.tmp/out-c/sheet-r0.png`, `.tmp/out-c/sheet-r2.png` (5350 x 2866; `redraw.py sheet`, шрифт `PTSansNarrow-Regular.ttf` в этой копии настоящий, обход не понадобился), `.tmp/out-c/plume.png` (2560 x 624: ряды 1-3; маска окрашена `_tint` цветом Харконненов, тень под телом, фон RGB (200, 160, 110), рамка 1 px; скрипт `.tmp/u14/plume.py`), `.tmp/u14/size-compare.png` (три строки по 8 кадров ряда 0: UNIT_MCV, UNIT_HARVESTER новый пак, UNIT_HARVESTER `pack-before.dat`; скрипт `.tmp/u14/size_compare.py`), `.tmp/u14/pad-after.png`.

## Отклонения

- Закоммиченный `unit.json` ссылается на `units-gen/UNIT_HARVESTER/cut/...` для рядов 1-3, а не на `.tmp/out-c/cut/`. Пересборка из закоммиченного файла даст прежние обрезки (старый масштаб входов), пока ведущий не обновит `/srv/dune/gen/UNIT_HARVESTER/cut` или не перенесёт обрезки в постоянное место.
- Пути `cut.py` и `fade.py` пришлось менять: копии в `.tmp/u14/`, diff приложены.
- Проверка «A' >= H всюду» не выполняется (3221 пиксель), см. шаг 5; принятое правило выполняется.
- `pytest` на сервере не установлен; вместо него `unittest`, но не одним процессом `discover` (слишком долго), а по одному процессу на тест, см. 7.5.

## Перенос вырезок (ведущий)

Вырезки рядов 1–3 скопированы ведущим из `.tmp/out-c/cut/` в `units-gen/UNIT_HARVESTER/cut-0.793144/` под теми же именами (96 PNG); прежняя папка `cut/` с вырезками масштаба 1.057526 не тронута. Описание `tools/units3d/units/UNIT_HARVESTER/unit.json` ссылается на новую папку (72 пути). Суммы всех 96 входов описания — `codex-direct/U14/gen/UNIT_HARVESTER.SHA256SUMS`, `sha256sum -c` из `units-gen/UNIT_HARVESTER` проходит. Сборка `redraw.py build tools/units3d/units/UNIT_HARVESTER` по закоммиченному описанию побайтно равна сборке `.tmp/out-c/build/` (`diff -r` без отличий, `all frames pass`); атласы пака — результат `fade.py` поверх этой сборки.
