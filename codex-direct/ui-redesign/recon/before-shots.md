# Снимки «до»: отладочный режим интерфейса на servak

Дата: 2026-11-11. Исполнитель: разведчик (Haiku 5.5). W = рабочая копия на ПК; S = /srv/dune/tasks/fable-ui-before; RUN = /srv/dune/worktrees/u34/.tmp/out/run/bin.

## Шаг 1. Место на servak

Команда: `ssh servak 'df -m /srv | tail -1'`
Вывод: `/dev/mapper/pve-root    112317 100311      6419  94% /`. Свободно 6419 МБ при пороге 5200, продолжаю.

Повторные проверки перед сочетаниями и после них (4-й столбец): 6417 (перед сочетанием 2, после удаления сочетания 1), 6416 (перед сочетанием 3), 5781 (финальная проверка). Минимум за время работ: 6168 (во время копирования сочетания 3). После последнего удаления сырых PNG было 6433, затем 5781. Снижение на ~650 МБ после моего последнего удаления не объяснено: мои файлы в S занимают 2 МБ, причину я не выяснял.

## Шаг 2. Инструменты на servak

Команды: `ssh servak 'mkdir -p /srv/dune/tasks/fable-ui-before/tools'`, затем `scp -r .../tools/ui-audit servak:/srv/dune/tasks/fable-ui-before/tools/`. scp exit=0. В S/tools/ui-audit лежат 13 файлов и каталог tests/.

## Шаг 3. Каталог сцен

Команда: `ssh servak 'cd S && ENV RUN/d2tm --ui-audit-list > catalog.json; echo exit=$?'`
Вывод: `exit=0`. Подсчёт: `108`. Размер catalog.json 23596 байт. Копия на ПК: W/.cache/ui-redesign/before/catalog.json, scp exit=0. Значение 108 входит в ожидаемые 107/108.

## Шаг 4. Масштабы

Вывод дословно:
```
--- 1024x768
{"resolution":"1024x768","render":[0,100,125],"world":[0,100,110,125,150]}
exit=0
--- 1920x1080
{"resolution":"1920x1080","render":[0,100,125,150,175],"world":[0,100,110,125,150]}
exit=0
```

## Шаг 5. Сочетания

Для каждого сочетания: проверка df, запуск `run_combo.py` с `--scene` для всех 108 сцен, проверка exit и FAILED, подсчёт PNG на servak, копирование tar на ПК, сверка числа файлов, удаление сырых PNG точным путём только при совпадении.

Запуск сочетаний 1 и 2 шёл в фоне (run_in_background), сочетание 3 ушло в фон после 180 с ожидания в обычном вызове. Ожидание обеспечивал Monitor по строке `exit=` в log-N.txt.

**1024x768/en/hd** (log-1.txt):
- Проверка: `tail -3` = сцены credits-4, credits-5, `exit=0`. Строк в логе 109 (108 сцен и exit). FAILED: 0. PNG на servak: 108.
- Копирование: `tar cf - png/1024x768/en/hd logs/1024x768/en/hd | tar xf -` в W/.cache/ui-redesign/before/. PNG на ПК 108, servak 108, logs 108 файлов. Совпало.
- Удаление: `rm -r .../out/png/1024x768/en/hd`, exit=0.

**1920x1080/en/hd/r100w0** (log-2.txt):
- Проверка: `exit=0`, 109 строк, FAILED: 0, PNG на servak: 108.
- PNG на ПК 108, servak 108, logs 108. Совпало.
- Удаление: `rm -r .../out/png/1920x1080/en/hd/r100w0`, exit=0.

**1920x1080/en/hd** (log-3.txt):
- Проверка: `exit=0`, 109 строк, FAILED: 0, PNG на servak: 108.
- Первая сверка показала 109 на ПК против 108 на servak. Причина: в каталоге png/1920x1080/en/hd на ПК лежит подкаталог r100w0 от сочетания 2. Подсчёт только файлов: на ПК 108, на servak 108, logs 108. Совпало.
- Удаление: `rm -r .../out/png/1920x1080/en/hd`, exit=0. На servak остались пустые родители out/png/1024x768 и out/png/1920x1080.

Сводка:

| сочетание | холст (main-menu) | сцен | PNG на ПК | FAILED | минут (≈сумма сценных времён) |
|---|---|---|---|---|---|
| 1024x768/en/hd | 800x600 | 108 | 108 | 0 | ≈10.6 (638.5 с) |
| 1920x1080/en/hd/r100w0 | 1920x1080 | 108 | 108 | 0 | ≈11.9 (715.6 с) |
| 1920x1080/en/hd | 1067x600 | 108 | 108 | 0 | ≈12.1 (723.0 с) |

Минуты — сумма значений «Xs» из строк сцен в логах, не реальное время запуска (замера не было).

## Шаг 6. Листы

Команда: `python -B tools/ui-audit/build_sheets.py --png-root ... --logs-root ... --catalog ... --full 1024x768/en/hd --full 1920x1080/en/hd/r100w0 --full 1920x1080/en/hd --out .cache/ui-redesign/before/sheets-out`
Вывод: `sheets: 54; flag sheets: 0; flagged without PNG: 0; index rows: 324`. exit=0.
Файлов в sheets-out/sheets: 54 (jpg, в трёх подкаталогах 1024x768_en_hd, 1920x1080_en_hd, 1920x1080_en_hd_r100w0). Раздельные счётчики по подкаталогам не снимались. Листы не просматривались.

## Шаг 7. Геометрия (только 1920x1080/en/hd)

По уточнению координатора. Для сочетаний 1 и 2 флаги не считались, и в W/.cache/ui-redesign/before/ нет flags.json, поэтому утверждение о проверке другим помощником я не подтвердил.

Команды: `python -B tools/ui-audit/check_geometry.py --help` (usage: logs_root, --json, --txt, --summary8), затем
`python -B tools/ui-audit/check_geometry.py .cache/ui-redesign/before/logs/1920x1080/en/hd --json .../flags-1920x1080-en-hd.json --txt ... --summary8 ...`

Вывод: `logs: 216; flags: 104; rule 1: 0, rule 2: 0, rule 3: 0, rule 4: 68, rule 5: 0, rule 6: 0, rule 7: 0, rule 8: 0, rule 9: 36`. exit=0.

Файл назван flags-1920x1080-en-hd.json (не flags.json, поскольку общий файл флагов не создавался). Пример флага: rule 9, сцена credits-1, пересечение с GuiButton:Back. В каталоге 108 jsonl-файлов, а инструмент печатает logs: 216. Причину не проверял.

## Шаг 8. Размер холста

Первая строка main-menu.geometry.jsonl (поля header):
- 1024x768/en/hd: окно 1024x768, холст 800x600, render_scale 0, world_scale 0.
- 1920x1080/en/hd/r100w0: окно 1920x1080, холст 1920x1080, render_scale 100, world_scale 0.
- 1920x1080/en/hd: окно 1920x1080, холст 1067x600, render_scale 0, world_scale 0.
Во всех трёх: game_screen false, version "unset".

## Шаг 9. Итог на servak

Команда: `ssh servak 'du -sm /srv/dune/tasks/fable-ui-before; df -m /srv | tail -1'`
Вывод: `2	/srv/dune/tasks/fable-ui-before`, `/dev/mapper/pve-root 112317 100949 5781 95% /`.

## Пути

- Листы: W/.cache/ui-redesign/before/sheets-out/sheets/
- Снимки: W/.cache/ui-redesign/before/png/ (3 сочетания по 108 файлов)
- Логи: W/.cache/ui-redesign/before/logs/ (3 сочетания по 108 jsonl)
- Каталог: W/.cache/ui-redesign/before/catalog.json
- Флаги: W/.cache/ui-redesign/before/flags-1920x1080-en-hd.json (+ .txt, -summary8.txt)

## Неопределённости

- Реальное время запуска сочетаний не замерено, в таблице сумма сценных времён.
- Флаги по сочетаниям 1 и 2 не считались.
- Расхождение 216 против 108 jsonl в check_geometry не объяснено.
- Совпадение PNG проверено по числу файлов, не по содержимому или хэшам. Листы не просматривались.
- Падение свободного места на ~650 МБ после последней очистки не объяснено.
- Пустые каталоги out/png/1024x768 и out/png/1920x1080 на servak оставлены.
- Расход токенов: оценка около 80 тысяч.
