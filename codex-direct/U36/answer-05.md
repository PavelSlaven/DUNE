## Ответ на DONE-U36-B1: часть Б, партия 2 — все записи пака в `.tmp/u36-b2/`

Сдача `DONE-U36-B1` принята. Выбор ведущего по листам (решение владельца — Р45):

| Здание | Источник новой картинки |
|---|---|
| Казармы, Стройплощадка, IX, Дворец, Хранилище, WOR | `.tmp/u36-fit/<ЗДАНИЕ>_a.png` |
| Лёгкий завод | `.tmp/u36-fit/LIGHTFACTORY_D2a.png` |
| Тяжёлый завод | `.tmp/u36-fit/HEAVYFACTORY_D2b.png` и машина в отсеке (шаг 8) |
| Завод переработки | `.tmp/u36-fit/REFINERY_a.png` после правила 2 (шаг 3) |
| Ремонт | `.tmp/u36-fit/REPAIR_a.png` после правила 2 и `.tmp/u36-fit/REPAIR_a_open.png` |
| Высокие технологии | кадры растяжки, трубы и открытый купол — скриптами ведущего (шаг 11); попытки `HIGHTECH_fix*` и `HIGHTECH_open6*` не используются |
| Космопорт, турели | выходы `.tmp/u36-b1/` |

Эта партия строит в `.tmp/u36-b2/` новую версию каждой из 52 записей таблицы «Записи пака» задания U36 под её именем `<ЗАПИСЬ>.png`. Исключение — `BUILD_HEAVYFACTORY` и `BUILD_HEAVYFACTORY_SHADOW`: три варианта машины в `.tmp/u36-b2/work/`, выбор ведущего — следующим ответом. Пак и мастер-файлы не меняются, правки — только в `.tmp/`. Установка — следующая партия.

## Шаги

1. **Диск.** `df -h /srv`; свободно меньше 5 GB — блок `## Q-U36-02` со строкой вывода и стоп.

2. **Скрипты ведущего.** Скопируй байт в байт из `/srv/dune/tasks/u36/b2-tools/` в `.tmp/u36-tools/` четыре файла: `flags.py`, `overlay_map.py`, `ht_fix0.py`, `ht_frames2.py`. Не меняй их. Запуск — `/srv/dune/venv/bin/python` из корня рабочей копии. Выведи sha256 четырёх копий.

3. **Правило 2 для двух картинок.** `defringe2.py .tmp/u36-fit/REFINERY_a.png .tmp/u36-b2/work/REFINERY_a.png` и `defringe2.py .tmp/u36-fit/REPAIR_a.png .tmp/u36-b2/work/REPAIR_a.png`; строки вывода — в сдачу. Ожидается: после очистки 0.

4. **Статичные здания.** Копии байт в байт: `.tmp/u36-fit/<B>_a.png` → `.tmp/u36-b2/BUILD_<B>.png` для B = `BARRACKS`, `CONSTYARD`, `IX`, `PALACE`, `SILO`, `WOR`; `.tmp/u36-fit/LIGHTFACTORY_D2a.png` → `.tmp/u36-b2/BUILD_LIGHTFACTORY.png`.

5. **Флаги.** `flags.py .tmp/u36-old .tmp/u36-b2` пишет `BUILD_<B>_FLAG.png` и `HM_BUILD_<B>_FLAG.png` для `BARRACKS`, `CONSTYARD`, `SILO`, `LIGHTFACTORY`, `WOR`, `IX`, `REFINERY`, `PALACE` и печатает по строке JSON на здание; строки — в сдачу. Копии байт в байт из `.tmp/u36-stretch/` в `.tmp/u36-b2/`: `BUILD_HIGHTECH_FLAG.png`, `HM_BUILD_HIGHTECH_FLAG.png`, `BUILD_STARPORT_FLAG.png`, `HM_BUILD_STARPORT_FLAG.png`.

6. **Накладки Лёгкого завода.** Две команды, строки JSON — в сдачу:
   - `overlay_map.py .tmp/u36-old/BUILD_LIGHTFACTORY_PRODUCTION.png .tmp/u36-b2/BUILD_LIGHTFACTORY_PRODUCTION.png 256 58.5 57.3 50.4 52.2 0.6923076923076923 0.7941176470588235`
   - `overlay_map.py .tmp/u36-old/BUILD_LIGHTFACTORY_FLASH.png .tmp/u36-b2/BUILD_LIGHTFACTORY_FLASH.png 256 58.5 57.3 50.4 52.2 0.6923076923076923 0.7941176470588235`

7. **Вспышка Тяжёлого завода.** `overlay_map.py .tmp/u36-old/BUILD_HEAVYFACTORY_FLASH.png .tmp/u36-b2/BUILD_HEAVYFACTORY_FLASH.png 256 160 152.5 169.5 103 1.8518518518518519 1.5`; строка JSON — в сдачу.

8. **Машина Тяжёлого завода.** Отсек P — прямоугольник x 254…328, y 29…161 включительно в кадре 384 × 256. Три варианта t = `a`, `b`, `old`.

   8.1. **Генерация `a`, `b`.** Помощник G10 (шаг «Организация работы»), промпт `HEAVYFACTORY-VEHICLE` (раздел «Промпты»), одна входная картинка — сырой результат `.tmp/u36-gen/HEAVYFACTORY_D2b.png`. Попытки `HEAVYFACTORY_VEH_a` и `HEAVYFACTORY_VEH_b` — два независимых вызова. Сырой результат — `.tmp/u36-gen/<имя попытки>.png`, журнал — `.tmp/u36-gen/log-G10.tsv`. Правила генерации задания U36 действуют целиком с двумя заменами: предел G10 — 4 вызова, повторы включены; плохая попытка в правилах 3 и 4 — та, у которой `vehicle_frames.py` (8.3) напечатал `"bad": true`.

   8.2. **Обработка `a`, `b`.** Доработай `.tmp/u36-tools/fit_box.py`: необязательный аргумент `--closed-fit <путь>`; если он задан, разность в поле `pixels_diff_gt24_from_closed` считается с этим файлом вместо `.tmp/u36-fit/REPAIR_<буква>.png`; без аргумента поведение прежнее. Команда для каждой попытки: `fit_box.py .tmp/u36-gen/HEAVYFACTORY_VEH_<t>.png .tmp/u36-gen/HEAVYFACTORY_D2b.png 0,208,1254,1044 .tmp/u36-fit/HEAVYFACTORY_VEH_<t> --closed-fit .tmp/u36-fit/HEAVYFACTORY_D2b.png` (рамка — поле `box` строки `HEAVYFACTORY_D2b` в `.tmp/u36-fit/attempts.jsonl`). Строки JSON — в сдачу.

   8.3. **`vehicle_frames.py`.** Напиши `.tmp/u36-tools/vehicle_frames.py`. Основа B — `.tmp/u36-fit/HEAVYFACTORY_D2b.png`. Выход — атлас 384 × 2816 из 11 кадров столбцом и одна строка JSON.
   - Режим `--edit <E.png>` (варианты `a`, `b`; E — `.tmp/u36-fit/HEAVYFACTORY_VEH_<t>.png`):
     - маска V: пиксели P, у которых максимум модуля разности RGB между E и B больше 24; из них — наибольшая связная область (соседство по сторонам); дыры заполнены (`scipy.ndimage.binary_fill_holes`); расширение на 1 крестом 3 × 3; затем только пиксели P;
     - y0 и y1 — наименьшая и наибольшая строка V; плохая попытка (`"bad": true`) — V меньше 1500 пикселей или V касается края P (наименьший x V равен 254, наибольший x равен 328, y0 равен 29 или y1 равен 161);
     - кадр 0 — B; кадр k (k = 1…10) — копия B, в которой пиксели V с y ≥ r(k) взяты из E, где r(k) = y1 + 1 − round((y1 − y0 + 1) · k / 10);
     - искры в кадрах 1…9: строка r(k); если в ней нет пикселей V — ближайшая строка ниже с пикселями V; xl и xr — наименьший и наибольший x V в этой строке. В каждой из точек (xl, строка) и (xr, строка) — крест: центр RGB (255, 240, 190), четыре соседа на расстоянии 1 по сторонам RGB (255, 170, 60), альфа 255; пиксели вне кадра пропускаются;
     - JSON: число пикселей V, рамка V, `bad` и причина, список r(1)…r(10).
   - Режим `--layer <L.png>` (вариант `old`): кадр k — B, на который по альфе наложен кадр k атласа L (`PIL.Image.alpha_composite`). JSON: рамка непрозрачных пикселей L по каждому кадру.
   - Атлас слоя `old`: `overlay_map.py .tmp/u36-out/HEAVYFACTORY_VEHICLE.png .tmp/u36-b2/work/HEAVYFACTORY_VEHICLE_old.png 256 297 119 291 95 1.56 1.56`.
   - Выходы: `.tmp/u36-b2/work/BUILD_HEAVYFACTORY_<t>.png` для t = `a`, `b`, `old`. Попытка пропущена или осталась плохой — её атлас всё равно строится, если есть файл E; строки JSON — в сдачу.

9. **Завод переработки.** Напиши `.tmp/u36-tools/refinery_anim.py`. Входы: старый атлас O = `.tmp/u36-old/BUILD_REFINERY.png` (кадры O0…O7), старая маска H = `.tmp/u36-old/HM_BUILD_REFINERY.png` (кадры H0…H7), новая картинка N = `.tmp/u36-b2/work/REFINERY_a.png`. Выходы: `.tmp/u36-b2/BUILD_REFINERY.png` и `.tmp/u36-b2/HM_BUILD_REFINERY.png` (по 384 × 2048, 8 кадров) и одна строка JSON.
   - Щели, рамки включительно (x0, y0, x1, y1), в порядке таблицы:

     | Щель | Старая рамка | Новая рамка |
     |---|---|---|
     | верхняя длинная | 225, 99, 309, 112 | 247, 40, 333, 50 |
     | левая верхняя | 200, 123, 237, 135 | 228, 60, 263, 71 |
     | правая верхняя | 297, 123, 335, 135 | 317, 60, 352, 71 |
     | центр | 242, 134, 292, 177 | 267, 70, 314, 111 |
     | левая нижняя | 200, 177, 237, 191 | 228, 110, 263, 122 |
     | правая нижняя | 298, 177, 335, 191 | 317, 110, 352, 122 |
     | нижняя длинная | 225, 204, 309, 222 | 247, 133, 333, 149 |

   - Для пикселя (x, y) нового кадра и щели s: qx = ox0 + (x − nx0) · (ox1 − ox0) / (nx1 − nx0), qy = oy0 + (y − ny0) · (oy1 − oy0) / (ny1 − ny0) (o — старая рамка s, n — новая); расстояние d_s = max(ox0 − qx, qx − ox1, oy0 − qy, qy − oy1, 0). Щель пикселя — s с наименьшим d_s, при равенстве — первая по таблице; дальше q и d — её.
   - Кадр k (k = 0…7): копия N; пиксели с d ≤ 3 получают RGB = round(RGB N + разность (Ok − O0) в точке q), ограниченное 0…255; альфа — из N. Разность в точке q — билинейная выборка поканальной разности RGB, координаты выборки ограничены кадром.
   - Маска кадра k: пиксели с d ≤ 8 получают RGBA кадра Hk в точке (round(qx), round(qy)); остальные — (0, 0, 0, 0).
   - JSON: по каждому кадру — число пикселей, отличных от N, и число пикселей маски с альфой больше 0; по каждому кадру H — число пикселей с альфой больше 0, у которых расстояние d до каждой старой рамки больше 8.

10. **Ремонт.** Напиши `.tmp/u36-tools/repair_anim.py`. Закрытые ворота C = `.tmp/u36-b2/work/REPAIR_a.png`, открытые Op = `.tmp/u36-fit/REPAIR_a_open.png`. Выход — `.tmp/u36-b2/BUILD_REPAIR.png` (384 × 2048, 8 кадров) и одна строка JSON.
    - Маска ворот M: наибольшая связная область (соседство по сторонам) пикселей, у которых максимум модуля разности RGB между C и Op больше 24, с заполненными дырами. Ожидаемая рамка — x 201…361, y 201…249; отличие больше чем на 4 пикселя по любой стороне — блок `## Q-U36-05` с рамкой и стоп.
    - y_top и y_bot — наименьшая и наибольшая строка M, h = y_bot − y_top + 1.
    - Кадр k (k = 0…7), подъём r = round(h · k / 7): копия C; пиксель (x, y) из M получает Op(x, y), если y > y_bot − r; иначе C(x, y + r), если (x, y + r) входит в M; иначе остаётся C(x, y). Кадр 0 равен C, в кадре 7 вся M — из Op.
    - JSON: рамка M, число пикселей M, список r по кадрам.

11. **Высокие технологии.** `ht_fix0.py .tmp/u36-stretch/BUILD_HIGHTECH.png .tmp/u36-b2/work/HIGHTECH_frame0.png`, затем `ht_frames2.py .tmp/u36-b2/work/HIGHTECH_frame0.png .tmp/u36-stretch/BUILD_HIGHTECH.png .tmp/u36-b2/BUILD_HIGHTECH.png`. Выведи sha256 обоих выходов.

12. **Космопорт и турели.** Копии байт в байт в `.tmp/u36-b2/`: `.tmp/u36-b1/BUILD_STARPORT.png`, `.tmp/u36-b1/BUILD_TURRET.png`, `.tmp/u36-b1/BUILD_TURRET_SHADOW.png`, `.tmp/u36-b1/BUILD_RTURRET.png`, `.tmp/u36-b1/BUILD_RTURRET_SHADOW.png`.

13. **Тени.** `angle.py shadow <атлас> <плита> <кадров> <выход>` для каждого атласа зданий:

    | Атлас | Плита | Кадров | Выход |
    |---|---|---|---|
    | `.tmp/u36-b2/BUILD_<B>.png`, B = `BARRACKS`, `CONSTYARD`, `IX`, `LIGHTFACTORY`, `SILO`, `WOR` | 2x2 | 1 | `.tmp/u36-b2/BUILD_<B>_SHADOW.png` |
    | `.tmp/u36-b2/BUILD_PALACE.png` | 3x3 | 1 | `.tmp/u36-b2/BUILD_PALACE_SHADOW.png` |
    | `.tmp/u36-b2/BUILD_REFINERY.png` | 3x2 | 8 | `.tmp/u36-b2/BUILD_REFINERY_SHADOW.png` |
    | `.tmp/u36-b2/BUILD_REPAIR.png` | 3x2 | 8 | `.tmp/u36-b2/BUILD_REPAIR_SHADOW.png` |
    | `.tmp/u36-b2/BUILD_HIGHTECH.png` | 3x2 | 7 | `.tmp/u36-b2/BUILD_HIGHTECH_SHADOW.png` |
    | `.tmp/u36-b2/BUILD_STARPORT.png` | 3x3 | 8 | `.tmp/u36-b2/BUILD_STARPORT_SHADOW.png` |
    | `.tmp/u36-b2/work/BUILD_HEAVYFACTORY_<t>.png`, t = `a`, `b`, `old` | 3x2 | 11 | `.tmp/u36-b2/work/BUILD_HEAVYFACTORY_<t>_SHADOW.png` |

14. **Проверки.**
    - Список: в `.tmp/u36-b2/` (без подпапки `work`) ровно 50 файлов `<ЗАПИСЬ>.png` — все записи `.tmp/u36-old/`, кроме `BUILD_HEAVYFACTORY` и `BUILD_HEAVYFACTORY_SHADOW`. Размер каждого файла равен размеру одноимённого файла `.tmp/u36-old/`. Выведи таблицу: запись, размер, совпадает ли, sha256 (первые 12 знаков). Расхождение — строка в «Не проверено», работа продолжается.
    - `angle.py check` для каждого атласа из таблицы шага 13 с его плитой и числом кадров; итог каждой проверки — в сдачу.

15. **Сдача.** Пришли `## DONE-U36-B2` по формату задания U36 и остановись. Сверх формата:
    - «### Числа»: sha256 шага 2 и шага 11; строки вывода шагов 3, 5–10; таблица и итоги `check` шага 14;
    - «### Генерация»: G10 — вызовы, повторы, отказы модерации, пропуски, плохие попытки с причинами.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт HEAVYFACTORY-VEHICLE:

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, seen from above with its front wall along the bottom, drawn on a flat magenta background. On the right side of the roof there is an empty octagonal assembly pit between two vertical rails. Draw one finished grey armoured combat tank inside this pit, seen from directly above from the same camera as the roof: the top of its hull and turret faces the viewer, its gun barrel points down towards the front wall, it stands on the floor of the pit, it is about two thirds as wide as the pit and about two thirds as long as the pit, and it stays inside the pit. Keep everything else exactly as it is: the same outline, camera angle, size and position of the building, the rails, the pit edges, every other part, and the same magenta areas. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

## Организация работы

- Порядок: шаги 1, 2 → сразу запуск G10 → корневая нить: шаги 3–7, 9–12, доработка `fit_box.py` и `vehicle_frames.py` → после G10 — шаг 8 для `a`, `b` → шаг 13 → шаг 14 → `## DONE-U36-B2` и стоп.
- Параллельно: G10 генерирует, пока корневая нить делает шаги 3–7 и 9–12; шаги 3–7, 9–12 не зависят друг от друга, кроме того, что шаги 9 и 10 идут после шага 3.
- Помощники: один — G10, `gpt-6-luna` `xhigh`, без вложенных. Бриф G10: шаг 8.1, промпт `HEAVYFACTORY-VEHICLE` дословно, раздел «Правила генерации» задания U36 с заменами шага 8.1, абзац раздела «Комментарии в коде» задания U36 дословно. Обработку попыток (8.2, 8.3) делает корневая нить; признак плохой попытки G10 получает от неё до решения о повторе.
- Остановки: только на `## DONE-U36-B2` и на блоках `## Q-U36-NN` задания и этого ответа (`Q-U36-05` — шаг 10).
- Рамка правок: только `.tmp/`; скрипты ведущего не меняются.
