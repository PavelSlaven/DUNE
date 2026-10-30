# U6-pack: сборка и проверка

## Входы и результат

Четыре одиночных бойца собраны в `.tmp/out-pack/UNIT_SOLDIER/`, `.tmp/out-pack/UNIT_TROOPER/`, `.tmp/out-pack/UNIT_SABOTEUR/` и `.tmp/out-pack/UNIT_SINGLEFREMEN/`. Масштаб и раскладка кадров взяты из принятых `.tmp/out-u8/units/<ЮНИТ>/unit.json`, а выбор полос по направлениям — из `.tmp/out-gen2/<ЮНИТ>/strip/selection.json`. Использованы входы U6-gen, скопированные в `units-gen/`, и пути перекраски из `selection.json перекрасок сдачи U6-rc`; для Fremen направления `k2` выбраны варианты `a`. Маски домов получены из тех же входов перекраски. Проверены все файлы входов: 96 для SOLDIER, 96 для TROOPER, 96 для SABOTEUR и 100 для SINGLEFREMEN.

Три отряда собраны из готовых атласов body и HM одиночных бойцов и раскладок `placements.json` из `.tmp/out-u8/squads/`. Выполнены команды `compose` из корня проекта; `python` ниже обозначает Python настроенной виртуальной среды.

```sh
PYTHONDONTWRITEBYTECODE=1 python .tmp/squads/compose.py compose --squad UNIT_SOLDIERS --source .tmp/out-pack/UNIT_SOLDIER/UNIT_SOLDIER.png --body .tmp/out-pack/UNIT_SOLDIER/UNIT_SOLDIER.png --placements .tmp/out-u8/squads/UNIT_SOLDIERS/placements.json --out-root .tmp/out-pack --output .tmp/out-pack/squads/UNIT_SOLDIERS/UNIT_SOLDIERS.png --sheet .tmp/out-pack/squads/UNIT_SOLDIERS/UNIT_SOLDIERS-sheet.png --report .tmp/out-pack/squads/UNIT_SOLDIERS/UNIT_SOLDIERS-checks.json
PYTHONDONTWRITEBYTECODE=1 python .tmp/squads/compose.py compose --squad UNIT_SOLDIERS --source .tmp/out-pack/UNIT_SOLDIER/HM_UNIT_SOLDIER.png --body .tmp/out-pack/UNIT_SOLDIER/UNIT_SOLDIER.png --placements .tmp/out-u8/squads/UNIT_SOLDIERS/placements.json --out-root .tmp/out-pack --mask --output .tmp/out-pack/squads/UNIT_SOLDIERS/HM_UNIT_SOLDIERS.png --sheet .tmp/out-pack/squads/UNIT_SOLDIERS/HM_UNIT_SOLDIERS-sheet.png --report .tmp/out-pack/squads/UNIT_SOLDIERS/HM_UNIT_SOLDIERS-checks.json
PYTHONDONTWRITEBYTECODE=1 python .tmp/squads/compose.py compose --squad UNIT_TROOPERS --source .tmp/out-pack/UNIT_TROOPER/UNIT_TROOPER.png --body .tmp/out-pack/UNIT_TROOPER/UNIT_TROOPER.png --placements .tmp/out-u8/squads/UNIT_TROOPERS/placements.json --out-root .tmp/out-pack --output .tmp/out-pack/squads/UNIT_TROOPERS/UNIT_TROOPERS.png --sheet .tmp/out-pack/squads/UNIT_TROOPERS/UNIT_TROOPERS-sheet.png --report .tmp/out-pack/squads/UNIT_TROOPERS/UNIT_TROOPERS-checks.json
PYTHONDONTWRITEBYTECODE=1 python .tmp/squads/compose.py compose --squad UNIT_TROOPERS --source .tmp/out-pack/UNIT_TROOPER/HM_UNIT_TROOPER.png --body .tmp/out-pack/UNIT_TROOPER/UNIT_TROOPER.png --placements .tmp/out-u8/squads/UNIT_TROOPERS/placements.json --out-root .tmp/out-pack --mask --output .tmp/out-pack/squads/UNIT_TROOPERS/HM_UNIT_TROOPERS.png --sheet .tmp/out-pack/squads/UNIT_TROOPERS/HM_UNIT_TROOPERS-sheet.png --report .tmp/out-pack/squads/UNIT_TROOPERS/HM_UNIT_TROOPERS-checks.json
PYTHONDONTWRITEBYTECODE=1 python .tmp/squads/compose.py compose --squad UNIT_TRIPLEFREMEN --source .tmp/out-pack/UNIT_SINGLEFREMEN/UNIT_SINGLEFREMEN.png --body .tmp/out-pack/UNIT_SINGLEFREMEN/UNIT_SINGLEFREMEN.png --placements .tmp/out-u8/squads/UNIT_TRIPLEFREMEN/placements.json --out-root .tmp/out-pack --output .tmp/out-pack/squads/UNIT_TRIPLEFREMEN/UNIT_TRIPLEFREMEN.png --sheet .tmp/out-pack/squads/UNIT_TRIPLEFREMEN/UNIT_TRIPLEFREMEN-sheet.png --report .tmp/out-pack/squads/UNIT_TRIPLEFREMEN/UNIT_TRIPLEFREMEN-checks.json
PYTHONDONTWRITEBYTECODE=1 python .tmp/squads/compose.py compose --squad UNIT_TRIPLEFREMEN --source .tmp/out-pack/UNIT_SINGLEFREMEN/HM_UNIT_SINGLEFREMEN.png --body .tmp/out-pack/UNIT_SINGLEFREMEN/UNIT_SINGLEFREMEN.png --placements .tmp/out-u8/squads/UNIT_TRIPLEFREMEN/placements.json --out-root .tmp/out-pack --mask --output .tmp/out-pack/squads/UNIT_TRIPLEFREMEN/HM_UNIT_TRIPLEFREMEN.png --sheet .tmp/out-pack/squads/UNIT_TRIPLEFREMEN/HM_UNIT_TRIPLEFREMEN-sheet.png --report .tmp/out-pack/squads/UNIT_TRIPLEFREMEN/HM_UNIT_TRIPLEFREMEN-checks.json
```

Пункт 5 собрал семь листов в `.tmp/out-pack/sheets/`: `UNIT_SOLDIER.png`, `UNIT_TROOPER.png`, `UNIT_SABOTEUR.png`, `UNIT_SINGLEFREMEN.png`, `UNIT_SOLDIERS.png`, `UNIT_TROOPERS.png` и `UNIT_TRIPLEFREMEN.png`. Источник каждого листа — только `resources/bin/data/sdl_data_hd4.dat` после установки пункта 4, SHA-256 `d65c4e16cf9b42d609e0165e7559348ab9f3e2abdf7c8014c4a565b52dc32cb2`. Записи body и HM читаются через `read_pack` и `decode_image`; цвета домов и окраска взяты из `HOUSES` и `_tint` в `tools/units3d/redraw_sheets.py`. Каждый лист показывает кадр `r0`, направления `k0…k7`, три строки в порядке Харконнен, Атрейдес, Ордос, масштаб ×2 методом nearest и фон RGB `(200, 160, 110)`. Подписи набраны DejaVu Sans. Команда из корня: `python .tmp/out-pack/compose_sheets.py`.

Скрипт сверил SHA и 241 запись установленного пака, нашёл семь пар body/HM и проверил размеры каждой записи `1024×512`. Все семь листов имеют режим RGB, размер `2278×808` и заданный цвет фона. Изображения не генерировались: листы собраны скриптом из установленного пака. Вывод сборки сохранён в `.tmp/out-pack/sheets.log`; размеры и фон повторно проверены чтением готовых PNG. Проверки отрядов и установки записаны в `.tmp/out-pack/squads-checks.log` и `.tmp/out-pack/pack-audit.json`. Исполнитель визуально просмотрел все семь листов: подписи домов читаются, видны три строки и восемь направлений, оружие и ранцы сохраняют свой цвет.

## Singles: метрики итоговых сборок

Коридор рассчитан из медианы `M` 32 значений `share` как Python `round(M − 0.20, 3)` и `round(M + 0.20, 3)`. Счётчик «проба `[0,1]`» означает число кадров пробы, вышедших за этот широкий коридор; рядом приведено число кадров за окончательным коридором.

| Юнит | M | Окончательный `share_corridor` | Проба `[0,1]`: кадров вне коридора | В пробе вне окончательного коридора |
|---|---:|---:|---:|---:|
| `UNIT_SOLDIER` | 0.4145 | [0.214, 0.615] | 0/32 | 0/32 |
| `UNIT_TROOPER` | 0.3515 | [0.151, 0.551] | 0/32 | 0/32 |
| `UNIT_SABOTEUR` | 0.3675 | [0.167, 0.568] | 0/32 | 0/32 |
| `UNIT_SINGLEFREMEN` | 0.4550 | [0.255, 0.655] | 0/32 | 0/32 |

Итоговые сборки прошли для всех 128 кадров. У каждого направления разброс `share` не выше 0.08; тела итоговых атласов попиксельно совпали с принятыми атласами U8. Источник чисел — `.tmp/out-pack/u6-pack-answer02-v2.log` и `.tmp/out-pack/u6-pack-answer02-results.json`.

В поле `red_fill` во всех четырёх описаниях одиночных бойцов выставлено значение `100`. Для TROOPER и SINGLEFREMEN оно нужно, чтобы красные края формы за пределами зелёной перекраски не оставались красными у других Домов. Порог убирает эти края, сохраняя ранец, оружие и ботинки.

Для `UNIT_SINGLEFREMEN`, `k2`, выбор переключён с `b` на `a`: IoU варианта `b` был `.969` и `.970` при пороге `.97`; ведущий проверил вариант `a` с IoU `.982–.990`.

## Изменённые записи пака

Аудит установки сравнил 241 запись до и после: изменены ровно 14 перечисленных ниже записей, остальные 227 payload совпадают байт-в-байт. Для всех изменённых записей размер до и после равен `1024×512`, payload пака совпадает с файлом атласа.

- Одиночные бойцы: `UNIT_SOLDIER`, `HM_UNIT_SOLDIER`, `UNIT_TROOPER`, `HM_UNIT_TROOPER`, `UNIT_SABOTEUR`, `HM_UNIT_SABOTEUR`, `UNIT_SINGLEFREMEN`, `HM_UNIT_SINGLEFREMEN`.
- Отряды: `UNIT_SOLDIERS`, `HM_UNIT_SOLDIERS`, `UNIT_TROOPERS`, `HM_UNIT_TROOPERS`, `UNIT_TRIPLEFREMEN`, `HM_UNIT_TRIPLEFREMEN`.

## Сохранённые материалы и известное ограничение

Старые `.tmp/out-pack/probe/` и `.tmp/out-pack/failed-01/UNIT_SOLDIER/` сохранены. Финальные значения взяты из новых `probe2` и итоговых логов; ранние неуспешные пробы в таблице не использованы.

Актуальный результат повторной перекраски нагрудных подсумков `UNIT_SOLDIER`, `k6` приведён в разделе [«UNIT_SOLDIER k6 rc2»](#soldier-k6-rc2).

<a id="soldier-k6-rc2"></a>
## UNIT_SOLDIER k6 rc2

По решению владельца перекраска `UNIT_SOLDIER`, направление `k6`, заменена перегенерацией маски перекраски. Выбрана попытка `a`; её четыре кадра `rc2_r<r>k6_a.png` использованы в `unit.json`. Сборка и проверки маски прошли.

Дословный промпт выбранной попытки:

> Перекрась изображение 1. Это четыре кадра шага одного и того же пехотинца в сетке 2 × 2 на пурпурном фоне; пехотинец идёт к зрителю. У каждой из четырёх фигур залей сплошным чистым зелёным цветом RGB (0, 255, 0): серый шлем, кроме забрала; серую куртку с рукавами и наплечниками; светло-коричневые штаны с наколенниками. Оставь в прежних цветах, не перекрашивая: забрало; коричневый нагрудный жилет целиком — с подсумками, карманами, клапанами, пряжками и ремнями; пояс и подсумки на поясе; пистолет; перчатки и кисти рук; ботинки; ранец за спиной. Нагрудный жилет и подсумки — не броня, они остаются коричневыми. Не меняй форму, позу, положение и размер фигур, их контуры и пурпурный фон; не добавляй и не убирай детали. Перекрась одинаково все четыре фигуры. Не рисуй текст, рамки и линии сетки.

Строки `metrics.txt` для направления `k6` до и после замены (`share` указан в пятом столбце):

До — `.tmp/out-pack/UNIT_SOLDIER/metrics.txt`:

```text
row	k	pick	iou	share	old_share	stray	ok
0	6	a	0.989	0.540	0.857	0	True
1	6	a	0.998	0.522	0.852	0	True
2	6	a	0.995	0.548	0.856	0	True
3	6	a	0.993	0.541	0.852	0	True
```

После — `.tmp/out-pack2/UNIT_SOLDIER/metrics.txt`:

```text
row	k	pick	iou	share	old_share	stray	ok
0	6	a	0.996	0.429	0.857	0	True
1	6	a	0.998	0.418	0.852	0	True
2	6	a	0.995	0.454	0.856	0	True
3	6	a	0.996	0.445	0.852	0	True
```

После замены `share` по строкам `r0–r3` равен `0.429`, `0.418`, `0.454` и `0.445`; разброс направления `k6` равен `0.036`. Изменились ровно две записи пака: `HM_UNIT_SOLDIER` и `HM_UNIT_SOLDIERS`. Индексы, имена и расширения всех 241 записей сохранены; payload остальных 239 записей совпадает побайтно с копией до установки.

