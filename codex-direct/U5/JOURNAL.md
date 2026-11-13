# Журнал U5-pack

## Входы и параметры

Черновик описания: /tmp/u5fit/UNIT_HARVESTER/unit.json. Входные изображения: units-gen/UNIT_HARVESTER/. Источник S: /srv/dune/out/u5/final/UNIT_HARVESTER/params.json, поле scale, значение 1.0093486521123278. Фактор D=1.0477307507593085 взят из codex-direct/U7/scale-D.tsv, строка UNIT_HARVESTER. Рабочий unit.json в tools/units3d/units/UNIT_HARVESTER/unit.json совпадает с черновиком после предписанной замены путей, задания scale и share_corridor. Вычисление масштаба: round(S × D, 6) = 1.057526. Итоговый коридор доли маски: [0.34811, 0.63164].

История исправлений: сначала жёсткая проверка ожидала 1.057 вместо вычисленного 1.057526; проверку поправили на round(S × D). Первая проба ряда 0 использовала коридор по старым долям [0.42458, 0.63164] и остановилась на кадрах r0k1 и r0k3, у каждого share=0.422. В рабочем описании задан расширенный коридор [0.34811, 0.63164], после чего все кадры прошли. Первая сверка fade оставила 3251 различие пикселей тела на расстоянии d ≥ 24 при прежней формуле max(H, round(A*m)); формулу заменили так, чтобы сохранять исходную альфу тела при H>0 или d≥24, и применять fade только в остальных точках. После исправления все проверки пункта 5 дали ноль.

## Пробы пункта 2

Сначала сборка с исходным коридором завершилась кодом 1: r0k1 и r0k3 не прошли проверку share. Проба scale=1.057526 в .tmp/out-c/row0-attempts/1.057526 завершилась тем же результатом. После задания коридора [0.34811, 0.63164] сборка .tmp/out-c/row0-b прошла с первой попытки, s=338, код выхода 0. Все полные строки метрик и stdout/stderr сохранены ниже вместе с путями логов.

### Первый вывод сборки и вывод Q — .tmp/out-c/point2.log

    $ /srv/dune/venv/bin/python tools/units3d/redraw.py build .tmp/out-c/row0-input .tmp/out-c/row0
    exit code: 1
    stdout:
    scale 1.0575
    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	False
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	False
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    corridor	0.42458	0.63164	old
    failed: r0k1, r0k3
    stderr:
    r0k1: share
    r0k3: share
    
    Q: P2 build failed for scale=1.057526, exit_code=1, reason=r0k1: share, r0k3: share

### Метрики первой сборки — .tmp/out-c/row0/metrics.txt

    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	False
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	False
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    corridor	0.42458	0.63164	old
    failed: r0k1, r0k3

### Метрики пробы масштаба 1.057526 — .tmp/out-c/row0-attempts/1.057526/metrics.txt

    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	False
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	False
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    corridor	0.42458	0.63164	old
    failed: r0k1, r0k3

### stdout пробы масштаба 1.057526 — .tmp/out-c/row0-attempts/1.057526/stdout.txt

    scale 1.0575
    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	False
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	False
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    corridor	0.42458	0.63164	old
    failed: r0k1, r0k3

### stderr пробы масштаба 1.057526 — .tmp/out-c/row0-attempts/1.057526/stderr.txt

    r0k1: share
    r0k3: share

### Полный лог успешной серии — .tmp/out-c/row0-b-series.log

    $ /srv/dune/venv/bin/python tools/units3d/redraw.py build .tmp/out-c/row0-b-input .tmp/out-c/row0-b --pack tools/units3d/data/sdl_data_hd4_source.dat
    scale: 1.057526
    exit code: 0
    stdout:
    scale 1.0575
    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	True
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	True
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    corridor	0.34811	0.63164	set
    all frames pass
    stderr:
    
    P2 PASS scale=1.057526 s=338 output=.tmp/out-c/row0-b; attempts=1; exit code 0

### Лог успешной сборки — .tmp/out-c/row0-b.log

    $ /srv/dune/venv/bin/python tools/units3d/redraw.py build .tmp/out-c/row0-b-input .tmp/out-c/row0-b --pack tools/units3d/data/sdl_data_hd4_source.dat
    scale: 1.057526
    exit code: 0
    stdout:
    scale 1.0575
    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	True
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	True
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    corridor	0.34811	0.63164	set
    all frames pass
    stderr:

### Метрики успешной сборки — .tmp/out-c/row0-b/metrics.txt

    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	True
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	True
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    corridor	0.34811	0.63164	set
    all frames pass

## Пункт 3: вырезание краевой маски

Для каждого k опорное изображение B — выбранный pick ряда 0; его RGB переводится в размер 1024×1024 фильтром LANCZOS. Смещения dx,dy берутся для соответствующего r0k из .tmp/out-c/row0-b/params.json. Координаты преобразуются по формулам x=(X+0.5)×338/1024+dx−0.5 и y=(Y+0.5)×338/1024+dy−0.5; d=min(x,y,319−x,207−y). Маска Z задаётся как (d<4) и RGBdistance(B,(255,0,255))≤60, где RGBdistance — евклидово расстояние в RGB. В каждом входе C и recolour пиксели, попавшие в Z, заменяются на (255,0,255). Маска одинакова для попыток a и b. Итог: 48 масок и 96 PNG, scale=1.057526, s=338. Полный построчный лог приведён ниже.

| Ряд | Направление | Z для a | Z для b |
|---:|---:|---:|---:|
| 1 | 0 | 480550 | 480550 |
| 1 | 1 | 480017 | 480017 |
| 1 | 2 | 480120 | 480120 |
| 1 | 3 | 480389 | 480389 |
| 1 | 4 | 501655 | 501655 |
| 1 | 5 | 480498 | 480498 |
| 1 | 6 | 480187 | 480187 |
| 1 | 7 | 480435 | 480435 |
| 2 | 0 | 480550 | 480550 |
| 2 | 1 | 480017 | 480017 |
| 2 | 2 | 480120 | 480120 |
| 2 | 3 | 480389 | 480389 |
| 2 | 4 | 501655 | 501655 |
| 2 | 5 | 480498 | 480498 |
| 2 | 6 | 480187 | 480187 |
| 2 | 7 | 480435 | 480435 |
| 3 | 0 | 480550 | 480550 |
| 3 | 1 | 480017 | 480017 |
| 3 | 2 | 480120 | 480120 |
| 3 | 3 | 480389 | 480389 |
| 3 | 4 | 501655 | 501655 |
| 3 | 5 | 480498 | 480498 |
| 3 | 6 | 480187 | 480187 |
| 3 | 7 | 480435 | 480435 |

### Все значения и выходы cut.log — .tmp/out-c/cut.log

    r1k0_a	Z=480550	harvester_r1k0_a.png	harvester_recolour_r1k0_a.png
    r1k0_b	Z=480550	harvester_r1k0_b.png	harvester_recolour_r1k0_b.png
    r1k1_a	Z=480017	harvester_r1k1_a.png	harvester_recolour_r1k1_a.png
    r1k1_b	Z=480017	harvester_r1k1_b.png	harvester_recolour_r1k1_b.png
    r1k2_a	Z=480120	harvester_r1k2_a.png	harvester_recolour_r1k2_a.png
    r1k2_b	Z=480120	harvester_r1k2_b.png	harvester_recolour_r1k2_b.png
    r1k3_a	Z=480389	harvester_r1k3_a.png	harvester_recolour_r1k3_a.png
    r1k3_b	Z=480389	harvester_r1k3_b.png	harvester_recolour_r1k3_b.png
    r1k4_a	Z=501655	harvester_r1k4_a.png	harvester_recolour_r1k4_a.png
    r1k4_b	Z=501655	harvester_r1k4_b.png	harvester_recolour_r1k4_b.png
    r1k5_a	Z=480498	harvester_r1k5_a.png	harvester_recolour_r1k5_a.png
    r1k5_b	Z=480498	harvester_r1k5_b.png	harvester_recolour_r1k5_b.png
    r1k6_a	Z=480187	harvester_r1k6_a.png	harvester_recolour_r1k6_a.png
    r1k6_b	Z=480187	harvester_r1k6_b.png	harvester_recolour_r1k6_b.png
    r1k7_a	Z=480435	harvester_r1k7_a.png	harvester_recolour_r1k7_a.png
    r1k7_b	Z=480435	harvester_r1k7_b.png	harvester_recolour_r1k7_b.png
    r2k0_a	Z=480550	harvester_r2k0_a.png	harvester_recolour_r2k0_a.png
    r2k0_b	Z=480550	harvester_r2k0_b.png	harvester_recolour_r2k0_b.png
    r2k1_a	Z=480017	harvester_r2k1_a.png	harvester_recolour_r2k1_a.png
    r2k1_b	Z=480017	harvester_r2k1_b.png	harvester_recolour_r2k1_b.png
    r2k2_a	Z=480120	harvester_r2k2_a.png	harvester_recolour_r2k2_a.png
    r2k2_b	Z=480120	harvester_r2k2_b.png	harvester_recolour_r2k2_b.png
    r2k3_a	Z=480389	harvester_r2k3_a.png	harvester_recolour_r2k3_a.png
    r2k3_b	Z=480389	harvester_r2k3_b.png	harvester_recolour_r2k3_b.png
    r2k4_a	Z=501655	harvester_r2k4_a.png	harvester_recolour_r2k4_a.png
    r2k4_b	Z=501655	harvester_r2k4_b.png	harvester_recolour_r2k4_b.png
    r2k5_a	Z=480498	harvester_r2k5_a.png	harvester_recolour_r2k5_a.png
    r2k5_b	Z=480498	harvester_r2k5_b.png	harvester_recolour_r2k5_b.png
    r2k6_a	Z=480187	harvester_r2k6_a.png	harvester_recolour_r2k6_a.png
    r2k6_b	Z=480187	harvester_r2k6_b.png	harvester_recolour_r2k6_b.png
    r2k7_a	Z=480435	harvester_r2k7_a.png	harvester_recolour_r2k7_a.png
    r2k7_b	Z=480435	harvester_r2k7_b.png	harvester_recolour_r2k7_b.png
    r3k0_a	Z=480550	harvester_r3k0_a.png	harvester_recolour_r3k0_a.png
    r3k0_b	Z=480550	harvester_r3k0_b.png	harvester_recolour_r3k0_b.png
    r3k1_a	Z=480017	harvester_r3k1_a.png	harvester_recolour_r3k1_a.png
    r3k1_b	Z=480017	harvester_r3k1_b.png	harvester_recolour_r3k1_b.png
    r3k2_a	Z=480120	harvester_r3k2_a.png	harvester_recolour_r3k2_a.png
    r3k2_b	Z=480120	harvester_r3k2_b.png	harvester_recolour_r3k2_b.png
    r3k3_a	Z=480389	harvester_r3k3_a.png	harvester_recolour_r3k3_a.png
    r3k3_b	Z=480389	harvester_r3k3_b.png	harvester_recolour_r3k3_b.png
    r3k4_a	Z=501655	harvester_r3k4_a.png	harvester_recolour_r3k4_a.png
    r3k4_b	Z=501655	harvester_r3k4_b.png	harvester_recolour_r3k4_b.png
    r3k5_a	Z=480498	harvester_r3k5_a.png	harvester_recolour_r3k5_a.png
    r3k5_b	Z=480498	harvester_r3k5_b.png	harvester_recolour_r3k5_b.png
    r3k6_a	Z=480187	harvester_r3k6_a.png	harvester_recolour_r3k6_a.png
    r3k6_b	Z=480187	harvester_r3k6_b.png	harvester_recolour_r3k6_b.png
    r3k7_a	Z=480435	harvester_r3k7_a.png	harvester_recolour_r3k7_a.png
    r3k7_b	Z=480435	harvester_r3k7_b.png	harvester_recolour_r3k7_b.png
    processed masks: 48; saved PNGs: 96; scale=1.057526; s=338

## Пункт 4: сборка

Полная сборка прошла с кодом 0. Полный лог находится в .tmp/out-c/full-build.log; все строки metrics.txt вставлены ниже.

### Полные метрики — .tmp/out-c/build/metrics.txt

    row	k	pick	iou	share	old_share	stray	ok
    0	0	a	0.998	0.458	0.482	0	True
    0	1	a	0.999	0.422	0.489	0	True
    0	2	b	0.997	0.480	0.537	0	True
    0	3	a	0.996	0.422	0.495	0	True
    0	4	a	0.998	0.474	0.475	0	True
    0	5	b	0.998	0.429	0.523	0	True
    0	6	b	0.999	0.504	0.582	0	True
    0	7	a	0.995	0.449	0.503	0	True
    1	0	a	0.999	0.391	0.414	0	True
    1	1	b	0.999	0.394	0.416	0	True
    1	2	a	0.997	0.473	0.477	2	True
    1	3	a	0.996	0.388	0.400	0	True
    1	4	a	0.998	0.418	0.459	0	True
    1	5	a	0.999	0.363	0.461	0	True
    1	6	b	0.999	0.482	0.478	0	True
    1	7	b	0.995	0.396	0.454	0	True
    2	0	a	0.999	0.380	0.412	0	True
    2	1	b	0.999	0.395	0.411	3	True
    2	2	b	0.997	0.474	0.485	0	True
    2	3	b	0.996	0.401	0.417	0	True
    2	4	b	0.998	0.422	0.447	0	True
    2	5	a	0.999	0.362	0.465	0	True
    2	6	b	0.999	0.485	0.499	0	True
    2	7	b	0.995	0.399	0.454	0	True
    3	0	a	0.999	0.381	0.398	0	True
    3	1	b	0.999	0.395	0.409	0	True
    3	2	b	0.997	0.473	0.465	0	True
    3	3	a	0.996	0.402	0.405	0	True
    3	4	a	0.998	0.427	0.446	0	True
    3	5	b	0.999	0.362	0.464	0	True
    3	6	b	0.999	0.483	0.481	0	True
    3	7	b	0.996	0.394	0.447	0	True
    corridor	0.34811	0.63164	set
    all frames pass

## Пункт 5: fade и сверка атласов

До исправления сохранённая строка красной сверки была rows1_3_body_pixel_differences_at_d_ge_24: 3251; остальные счётчики были 0. Причина — прежняя формула max(H, round(A*m)). Исправленная формула: A' = A, если H>0 или d≥24; иначе A' = round(A × m), где m=clip((d−4)/20, 0, 1), A — альфа тела, H — альфа тела соответствующего кадра ряда 0, используемая как опорный силуэт, d — минимальное расстояние пикселя кадра 320×208 до края. Альфа house_mask после fade равна min(исходная альфа house_mask, A'). Тень строится со сдвигом 7 px, RGB=(7,5,3), alpha=round(A'×51/255).

Итоговая проверка пункта 5: PASS; все счётчики равны 0, включая differences at d≥24, проверки формул, сохранения RGB, ограничение альфы маски и PNG roundtrip. RGB тела не менялись; все три атласа ряда 0 (body, house_mask, shadow) остались пиксельно неизменны.

### Точные результаты проверки 5 — .tmp/out-c/fade.log

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
    final atlases: .tmp/out-c/final

## Пункт 6: установка пака и проверка

Перед установкой текущий пак был скопирован в .tmp/out-c/pack-before.dat: 34628840 bytes. tools/units3d/install.py установил атласы из .tmp/out-c/final в resources/bin/data/sdl_data_hd4.dat; итоговый пак имеет размер 35129027 bytes. Проверка через read_pack сравнила число записей, полный список (index, name, порядок, extension) и payload. Совпали 241 запись по метаданным; изменились ровно UNIT_HARVESTER, UNIT_HARVESTER_SHADOW и HM_UNIT_HARVESTER; payload всех остальных записей байт в байт совпал. Размеры изображений до и после установки равны 2560×832. Все три новых payload совпали с файлами атласов из final.

Индексы и размеры payload целевых записей:

| Индекс | Имя | Расширение | Payload до, байт | Payload после, байт | Размер изображения |
|---:|---|---|---:|---:|---:|
| 137 | UNIT_HARVESTER | PNG | 1755753 | 2077632 | 2560×832 |
| 138 | UNIT_HARVESTER_SHADOW | PNG | 124021 | 107114 | 2560×832 |
| 168 | HM_UNIT_HARVESTER | PNG | 143266 | 338481 | 2560×832 |

### Вывод install.py — .tmp/out-c/pack-install.log

    replaced 3 entries in resources/bin/data/sdl_data_hd4.dat

### Точная сверка пакета — .tmp/out-c/pack-verify.log

    HM_UNIT_HARVESTER: old_size=(2560, 832); new_size=(2560, 832); dimensions_equal=True; atlas_payload_equal=True
    UNIT_HARVESTER: old_size=(2560, 832); new_size=(2560, 832); dimensions_equal=True; atlas_payload_equal=True
    UNIT_HARVESTER_SHADOW: old_size=(2560, 832); new_size=(2560, 832); dimensions_equal=True; atlas_payload_equal=True
    entries_before=241 entries_after=241
    changed_count=3 changed_names=['HM_UNIT_HARVESTER', 'UNIT_HARVESTER', 'UNIT_HARVESTER_SHADOW']
    metadata_signature_equal=True
    unique_names=True untouched_payloads_byte_identical=True
    PASS: pack verification

## Пункт 7: листы и plume

Исходные sheet-команды без дополнительных параметров завершились кодом 2: PTSansNarrow-Regular.ttf оказался 131-байтным Git LFS pointer, Pillow сообщил unknown file format. В итоговых листах сохранён тот же вызов redraw.py sheet с явным --pack .tmp/out-c/pack-before.dat, чтобы старые слои читались из пака до установки; в runtime wrapper задан установленный DejaVu Sans с кириллицей. Инструмент и unit.json не изменялись.

Листы: .tmp/out-c/sheet-r0.png и .tmp/out-c/sheet-r2.png, каждый 5350×2866. Plume построен из трёх установленных записей пака для рядов 1–3 и направлений 0–7. Размер 2560×624; каждый кадр 320×208, фон RGB(200,160,110), рамка RGB(120,120,120) толщиной 1 px. Маска окрашена функцией _tint из redraw_sheets.py цветом Харконненов RGB(255,0,0). Тень с исходной альфой наложена под телом прямым alpha composite, без дополнительного ослабления. Проверены размеры листов, размер plume и все 25248 пикселей рамок.

Точные команды по умолчанию завершились кодом 2. Успешные полные вызовы с runtime wrapper находятся в sheet-r0.log и sheet-r2.log; отказы по шрифту — в отдельных default-логах.

### Отказ команды row 0 без override — .tmp/out-c/sheet-r0-default.log

    /srv/dune/worktrees/u8/resources/bin/data/PTSansNarrow-Regular.ttf: unknown file format

### Отказ команды row 2 без override — .tmp/out-c/sheet-r2-default.log

    /srv/dune/worktrees/u8/resources/bin/data/PTSansNarrow-Regular.ttf: unknown file format

### Успешный лист row 0 — .tmp/out-c/sheet-r0.log

    runtime_font_override=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
    delegated_command=redraw.py sheet tools/units3d/units/UNIT_HARVESTER .tmp/out-c/final .tmp/out-c/sheet-r0.png --row 0 --pack .tmp/out-c/pack-before.dat
    saved (5350, 2866)

### Успешный лист row 2 — .tmp/out-c/sheet-r2.log

    runtime_font_override=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
    delegated_command=redraw.py sheet tools/units3d/units/UNIT_HARVESTER .tmp/out-c/final .tmp/out-c/sheet-r2.png --row 2 --pack .tmp/out-c/pack-before.dat
    saved (5350, 2866)

### Проверки размеров и рамок plume — .tmp/out-c/plume.log

    plume_size=(2560, 624) expected=(2560, 624) dimensions_ok=True
    grid=3x8 frame_size=(320, 208) background=(200, 160, 110) border=(120, 120, 120)
    composition=body-tinted-by-_tint-mask; direct-shadow-alpha-composite-below-body; attenuation=none
    checked_border_pixels=25248 borders_ok=True
    sheet_sizes={0: (5350, 2866), 2: (5350, 2866)} sheets_ok=True
    PASS: sheet and plume dimensions and plume borders

## Пункт 8: итоговые скрипты и пути

Финальные копии скриптов: codex-direct/U5/cut.py и codex-direct/U5/fade.py. Для cut.py минимально закреплён BASE=ROOT/.tmp/out-c; OUT, row0-b/params.json и cut.log разрешаются в рабочую папку из обоих мест. Логика обработки не менялась и пункт 3 повторно не запускался. fade.py скопирован без правок. Модули были импортированы без вызова main: все 10 проверок путей и совпадения копий прошли.

Итоговые артефакты: .tmp/out-c/pack-before.dat; .tmp/out-c/final/; установленный resources/bin/data/sdl_data_hd4.dat; .tmp/out-c/sheet-r0.png; .tmp/out-c/sheet-r2.png; .tmp/out-c/plume.png; сверки и логи в .tmp/out-c/.

SHA-256 листов и plume:

- sheet-r0.png: 1180746be936709b1acc8c842c9f608254d5ceaaa58d40f6082f2300f32594e1
- sheet-r2.png: 70da903b20b57964d8931e7addf6f66a56a149d1899298caad5ea3dcef8d8f3
- plume.png: d65c40efbd2cdbab3029f8f7d894570b8ccafada17993ab6c8dc83042ad2aae5

Не проверено: запуск игры и визуальная приёмка результата владельцем.

### Проверка переносимости скриптов без запуска main — .tmp/out-c/script-paths.log

    cut_root_resolves=True
    cut_output_resolves=True
    cut_params_resolve=True
    cut_log_resolves=True
    fade_root_resolves=True
    fade_base_resolves=True
    fade_build_resolves=True
    fade_final_resolves=True
    cut_copy_matches_working_script=True
    fade_copy_matches_working_script=True
    PASS: 10/10 path and copy checks; main was not run

## Входы в хранилище

Обрезанные входы рядов 1–3 перенесены ведущим из `.tmp/out-c/cut/` в `units-gen/UNIT_HARVESTER/cut/` под теми же именами; описание ссылается туда. Суммы всех 96 входов описания — `codex-direct/U5/gen/UNIT_HARVESTER.SHA256SUMS`. Сборка по описанию с новыми путями побайтно равна сборке `.tmp/out-c/build/`; атласы пака — результат `fade.py` поверх этой сборки.
