## Ответ на DONE-U36-A2: часть Б, партия 1

Сдача `DONE-U36-A2` принята. Выбор тёмных вариантов Лёгкого и Тяжёлого заводов ещё за владельцем и придёт следующим ответом вместе с флагами, накладками заводов, установкой и тестами.

Решение владельца, 2026-11-05: Высокие технологии и Космопорт — растяжка старых кадров с исправлением недочётов; Завод переработки и Ремонт перерисовываются; турели сохраняют форму, правятся только недочёты кадров.

Эта партия:
- перерисовка Завода переработки и Ремонта (Ремонт — с закрытыми и открытыми воротами);
- правка труб Высоких технологий через ImageGen;
- скриптом: новая анимация купола Высоких технологий, новый кадр 7 Космопорта, пересборка кадров обеих турелей.

Пак и мастер-файлы не меняются, правки — только в `.tmp/`. Новые выходы — в `.tmp/u36-b1/`.

## Шаги

1. **Диск.** `df -h /srv`; свободно меньше 5 GB — блок `## Q-U36-02` со строкой вывода и стоп.

2. **Входы ImageGen** (`.tmp/u36-in/`, все — RGB без альфы, наложение по альфе на сплошной фон RGB (255, 0, 255), увеличение до 1536 × 1024 сжатием Lanczos, вставка в холст 1536 × 1536 цвета (255, 0, 255) в точку (0, 256)):
   - `refinery_src.png` — кадр 0 `.tmp/u36-old/BUILD_REFINERY.png`;
   - `repair_src.png` — кадр 0 `.tmp/u36-old/BUILD_REPAIR.png`;
   - `hightech_src.png` — кадр 0 `.tmp/u36-stretch/BUILD_HIGHTECH.png`;
   - `hightech6_src.png` — кадр 6 `.tmp/u36-stretch/BUILD_HIGHTECH.png`.

   Высота кадра всех трёх атласов — 256, ширина — 384.

3. **Генерация.** Одна попытка — один вызов ImageGen.

   | Попытка | Промпт | Картинки вызова по порядку | Обработка | Помощник |
   |---|---|---|---|---|
   | `REFINERY_a`, `REFINERY_b` | `REFINERY` | 1 — `refinery_src.png`, 2 — `guide_3x2.png` | `attempt.py`, плита 3x2, ориентир `guide_3x2.png` | G7 |
   | `REPAIR_a`, `REPAIR_b` | `REPAIR` | 1 — `repair_src.png`, 2 — `guide_3x2.png` | `attempt.py`, плита 3x2, ориентир `guide_3x2.png` | G8 |
   | `REPAIR_a_open` | `REPAIR-OPEN` | 1 — сырой результат `.tmp/u36-gen/REPAIR_a.png` | `fit_box.py` по рамке `REPAIR_a` (шаг 4) | G8, после `REPAIR_a` |
   | `REPAIR_b_open` | `REPAIR-OPEN` | 1 — сырой результат `.tmp/u36-gen/REPAIR_b.png` | `fit_box.py` по рамке `REPAIR_b` (шаг 4) | G8, после `REPAIR_b` |
   | `HIGHTECH_fixa`, `HIGHTECH_fixb` | `HIGHTECH-FIX` | 1 — `hightech_src.png` | `fix_compose.py` (шаг 5) | G9 |
   | `HIGHTECH_open6a`, `HIGHTECH_open6b` | `HIGHTECH-OPENFIX` | 1 — `hightech6_src.png` | `edit_back.py` (шаг 5) | G9 |

   - Сырой результат — `.tmp/u36-gen/<имя попытки>.png`. Копирование и журнал — по правилу 2 раздела «Правила генерации» задания U36; журналы — `log-G7.tsv`, `log-G8.tsv`, `log-G9.tsv`.
   - Правила генерации задания U36 действуют целиком, кроме пределов вызовов и с двумя уточнениями. Ссылки этих правил на шаг 5 задания означают таблицу этого шага. Правила 3 и 4 (плохая попытка и её повтор) применяются только к попыткам с обработкой `attempt.py`.
   - Пределы вызовов, повторы включены: G7 — 4, G8 — 8, G9 — 8.
   - Если `REPAIR_a` после повтора осталась плохой, `REPAIR_a_open` всё равно делается по её сырому результату; то же для `b`.

4. **`fit_box.py`.** Скрипт `.tmp/u36-tools/fit_box.py <сырой результат открытых ворот> <сырой результат закрытых ворот> <рамка> <выход без расширения>`. Рамка — поле «Рамка» строки `attempts.jsonl` закрытой попытки. Скрипт:
   - если размеры двух сырых результатов не равны, масштабирует картинку открытых ворот до размера закрытой сжатием Lanczos;
   - снимает фон тем же способом, что `attempt.py` (`key_largest`);
   - вырезает рамку закрытой попытки и уменьшает до 384 × 256 через `resize_premultiplied`;
   - сохраняет `<выход>.fit.png`, затем применяет правило 2 очистки каймы (`defringe2.py`) и сохраняет `<выход>.png`.

   Выходы — `.tmp/u36-fit/REPAIR_a_open` и `.tmp/u36-fit/REPAIR_b_open`. Скрипт печатает одну строку JSON: размеры сырых результатов, рамку, число пикселей каймы до и после, число пикселей, у которых максимум модуля разности RGBA с `.tmp/u36-fit/REPAIR_<t>.png` больше 24.

5. **`edit_back.py` и `fix_compose.py`.** Скрипт `.tmp/u36-tools/edit_back.py <сырой результат> <выход.png>` масштабирует сырой результат до 1536 × 1536 сжатием Lanczos, вырезает прямоугольник (0, 256)–(1536, 1280), уменьшает до 384 × 256 сжатием Lanczos и сохраняет RGB с альфой 255. Выходы для попыток `HIGHTECH_open6<t>` — `.tmp/u36-b1/HIGHTECH_open6<t>.png`.

   Скрипт `.tmp/u36-tools/fix_compose.py <сырой результат> <выход.png>`:
   - картинка правки E — результат `edit_back.py` для этого сырого результата (RGB);
   - исходный кадр O — кадр 0 `.tmp/u36-stretch/BUILD_HIGHTECH.png`;
   - выход — копия O, в которой RGB пикселей двух рамок взято из E, альфа — из O. Рамки включительно: B1 — x 14…96, y 40…66; B2 — x 108…128, y 56…80;
   - печатает по каждой рамке средний модуль разности RGB между E и O на полосе шириной 3 пикселя вдоль внутреннего края рамки.

   Выходы — `.tmp/u36-b1/HIGHTECH_fixa_frame0.png` и `.tmp/u36-b1/HIGHTECH_fixb_frame0.png`.

6. **Помощники.** Сразу после шага 2 запусти 3 помощника одновременно, `gpt-6-luna` `xhigh`, без вложенных помощников: G7, G8, G9 по таблице шага 3. Бриф помощника содержит:
   - строки таблицы шага 3 для его попыток;
   - его промпты из раздела «Промпты» дословно;
   - раздел «Правила генерации» задания U36 с уточнениями шага 3;
   - команды обработки его попыток (`attempt.py`, `fit_box.py`, `fix_compose.py` или `edit_back.py`);
   - абзац из раздела «Комментарии в коде» задания U36 дословно.

   До запуска G8 и G9 корневая нить пишет `fit_box.py`, `edit_back.py` и `fix_compose.py`. Пока помощники генерируют, корневая нить делает шаги 7–10.

7. **Высокие технологии, анимация купола.** Скрипт `.tmp/u36-tools/hightech_frames.py <кадр 0.png> <выход атласа.png> [--open-fix <картинка.png>]` строит атлас из 7 кадров 384 × 256, сложенных столбцом. Источники:
   - F0 — входной кадр 0;
   - S — атлас `.tmp/u36-stretch/BUILD_HIGHTECH.png` (кадры S0…S6).

   Области (координаты кадра, x вправо, y вниз):
   - купол D — пиксели с ((x − 186) / 80)² + ((y − 140) / 74)² ≤ 1;
   - проём P — пиксели с ((x − 189) / 71)² + ((y − 147) / 66)² ≤ 1;
   - кольцо Z — пиксели D, не входящие в P, у которых x ≤ 250 и y ≥ 78;
   - лампы — прямоугольники включительно: L1 x 251…283, y 71…94; L2 x 315…326, y 125…153; L3 x 358…383, y 71…88; L4 x 261…279, y 111…146; L5 x 316…325, y 4…28.

   Порядок:
   1. Открытое состояние O: копия F0; пиксели D — из S6. С `--open-fix`: пиксели Z получают RGB этой картинки, альфа в Z — 255.
   2. Кадр k (k = 1…6), сдвиг s = round(80 · k / 6):
      - начальная картинка — O;
      - пиксель (x, y) из D с x < 186 − s получает F0(x + s, y): левая створка уходит влево;
      - пиксель (x, y) из D с x ≥ 186 + s получает F0(x − s, y): правая створка уходит вправо;
      - остальные пиксели D остаются из O;
      - пиксели вне D внутри прямоугольников ламп получают S(k) того же пикселя.
   3. Кадр 0 — F0 без изменений.

   Запуски:
   - на кадре 0 `.tmp/u36-stretch/BUILD_HIGHTECH.png` без `--open-fix`, выход — `.tmp/u36-b1/BUILD_HIGHTECH_base.png`;
   - после G9 — на каждом из `.tmp/u36-b1/HIGHTECH_fix<t>_frame0.png` без `--open-fix`, выходы — `.tmp/u36-b1/BUILD_HIGHTECH_fix<t>.png`;
   - после G9 — на кадре 0 растяжки с `--open-fix .tmp/u36-b1/HIGHTECH_open6<t>.png`, выходы — `.tmp/u36-b1/BUILD_HIGHTECH_open6<t>.png`.

   Флаг и тень Высоких технологий не меняются.

8. **Космопорт, кадр 7.** Скрипт `.tmp/u36-tools/starport_f7.py`; источник — `.tmp/u36-stretch/BUILD_STARPORT.png`, 8 кадров 384 × 384, кадры S0…S7:
   - маска платформы M — наибольшая связная область (соседство по сторонам) пикселей, у которых максимум модуля разности RGBA между S7 и S0 больше 24, с заполненными дырами (`scipy.ndimage.binary_fill_holes`);
   - платформа — RGBA S7, у пикселей вне M альфа 0, вырезанная по рамке M; ожидаемая рамка — x 11…280, y 131…382; отличие больше чем на 4 пикселя по любой стороне — блок `## Q-U36-04` с рамкой и стоп;
   - масштаб m = min(236 / ширина рамки, 230 / высота рамки); платформа уменьшается через `resize_premultiplied` до (round(ширина · m), round(высота · m));
   - новый кадр 7 — копия S0, поверх которой по альфе наложена уменьшенная платформа с левым верхним углом в точке (16 + (236 − новая ширина) // 2, 137 + (230 − новая высота) // 2);
   - кадры 0…6 — из источника без изменений. Выход — `.tmp/u36-b1/BUILD_STARPORT.png`. Флаг и тень не меняются.

9. **Турели.** Скрипт `.tmp/u36-tools/turrets_v2.py`. Источники — `.tmp/u36-old/BUILD_TURRET.png` и `.tmp/u36-old/BUILD_RTURRET.png`, по 8 кадров 128 × 128, кадр k смотрит в направлении 45 · k градусов против часовой стрелки от востока (0 — восток, 2 — север). Выходы — `.tmp/u36-b1/BUILD_TURRET.png`, `.tmp/u36-b1/BUILD_RTURRET.png` и тени `.tmp/u36-b1/BUILD_TURRET_SHADOW.png`, `.tmp/u36-b1/BUILD_RTURRET_SHADOW.png`, построенные из новых кадров той же функцией и с теми же параметрами, что тени турелей части А.

   Общие правила:
   - **Правило 3 очистки каймы** — сначала, к каждому старому кадру: пиксель с альфой больше 0 и G < min(R, B) − 12 получает среднее RGB пикселей окна 5 × 5 вокруг него, у которых альфа больше 127 и которые сами не под это правило; таких нет — альфа 0. Один проход, соседи — из входного кадра. Дальше «кадр k» — старый кадр k после правила 3.
   - **Оливковый пиксель** — альфа больше 127, R − G > 2, G − B > 5 и R > 60.
   - **Сдвиги** — сдвиг купола и сдвиг плиты каждого кадра `BUILD_TURRET` из `.tmp/u36-out/turret_metrics.json` (поле `dome_and_plate_shifts_old`), применённые так же, как в `turrets.py` части А. Кадр, сдвинутый сдвигом купола, — Aᵈ(k); сдвигом плиты — Aᵖ(k). У `BUILD_RTURRET` сдвигов нет.
   - Связность — по сторонам; «расширение на 1» — `scipy.ndimage.binary_dilation` с крестом 3 × 3, один шаг.

   `BUILD_TURRET`:
   1. Купол Dm — наибольшая связная область пикселей, у которых во всех восьми кадрах Aᵈ(k) альфа больше 127 и пиксель не оливковый. Центр (cx, cy) — среднее координат пикселей Dm.
   2. Угол пикселя — atan2(cy − y, x − cx) в градусах. Сектор кадра k — пиксели, у которых разность угла и 45 · k, приведённая к −180…180, по модулю не больше 20.
   3. Ствол кадра k, Bar(k): пиксели Aᵈ(k) с альфой больше 0, не оливковые, лежащие в секторе кадра k и вне купола Dm, расширенного на 1; из них — связные области, касающиеся купола Dm, расширенного на 2; объединение этих областей расширяется на 1, затем от него оставляются только пиксели сектора кадра k, не входящие в Dm.
   4. Основа Bs — копия Aᵖ(0). Каждый пиксель Bar(0) получает пиксель первого кадра j из порядка 4, 2, 6, 1, 3, 5, 7, у которого Aᵖ(j) в этом пикселе оливковый; такого кадра нет — пиксель Aᵖ(4).
   5. Кадр k (k = 0…7) — копия Bs, в которой пиксели Bar(k) взяты из Aᵈ(k).

   `BUILD_RTURRET`:
   1. Чистая плита C: каждый пиксель — из первого кадра j из порядка 0, 4, 2, 6, 1, 3, 5, 7, у которого этот пиксель оливковый; такого кадра нет — поканальная медиана RGBA восьми кадров с округлением.
   2. Голова кадра k, H(k):
      - H0 — объединение связных областей не меньше 30 пикселей из пикселей, у которых максимум модуля разности RGBA кадра k и C больше 24;
      - G — пиксели кадра k с альфой больше 127, не оливковые и лежащие в H0, расширенной три раза квадратом 3 × 3;
      - H(k) — объединение H0 и G с заполненными дырами, расширенное на 1.
   3. Кадры 0, 2, 3, 5, 6, 7 — копия C, в которой пиксели H(k) взяты из кадра k.
   4. Отражение: x′ = x0 + x1 − x, где x0 и x1 — наименьший и наибольший x оливковых пикселей кадра 0; пиксели, у которых x′ выходит за 0…127, не переносятся.
   5. Кадр 1 — копия C, в которой пиксель (x′, y) для каждого пикселя (x, y) из H(3) взят из кадра 3 в точке (x, y). Кадр 4 — так же из H(0) и кадра 0.

10. **Листы** (`.tmp/u36-sheets/`, фон RGB (70, 68, 64), увеличение методом ближайшего соседа, подписи латиницей в полосах вне кадров):
    - `choice-REFINERY.png` (×2): `old` (кадр 0 `.tmp/u36-old/BUILD_REFINERY.png` с кадром 0 `.tmp/u36-old/BUILD_REFINERY_FLAG.png` поверх), `a`, `b`;
    - `choice-REPAIR.png` (×2): `old`, `a`, `a_open`, `b`, `b_open`;
    - `hightech-fix.png`: строка 1 (×2) — `stretch` (кадр 0 растяжки), `fixa`, `fixb`; строка 2 (×4) — рамки B1 и B2 этих трёх картинок;
    - `hightech-frames.png` (×1, по 4 ячейки в строке): кадры 0…6 `BUILD_HIGHTECH_base.png`;
    - `hightech-open.png`: строка 1 (×2) — кадр 6 каждого из атласов `BUILD_HIGHTECH_base.png`, `BUILD_HIGHTECH_open6a.png`, `BUILD_HIGHTECH_open6b.png`; строка 2 (×4) — прямоугольник x 100…256, y 70…220 этих трёх кадров;
    - `starport-f7.png` (×1): S0, старый S7, новый кадр 7;
    - `turrets-v2.png` (×3, 8 ячеек в строке): строки `TURRET old`, `TURRET new`, `RTURRET old`, `RTURRET new`;
    - `turret-masks-v2.png` (×3): те же строки `old`; в ячейке поверх кадра красным RGB (255, 0, 0) с непрозрачностью 40 % — Bar(k) у `TURRET`; H(k) у `RTURRET` для кадров 0, 2, 3, 5, 6, 7 и отражённые H(3), H(0) для кадров 1 и 4.
    - Пропущенная попытка — ячейка с заливкой RGB (128, 0, 0).

11. **Сдача.** Пришли `## DONE-U36-B1` по формату задания U36 и остановись. Сверх формата:
    - «### Листы» — пути листов шага 10;
    - «### Числа»:
      - таблица попыток `attempt.py` (как в `DONE-U36-A`) и строки JSON `fit_box.py` и `fix_compose.py`;
      - Высокие технологии: на каждом запуске по каждому кадру 1…6 — число пикселей вне D, отличных от входного кадра 0;
      - Космопорт: рамка M, новый размер платформы, точка вставки;
      - турели: центр купола и число пикселей Dm; по каждому кадру — число пикселей Bar(k) или H(k), наибольшее расстояние пикселя Bar(k) от центра купола, число пикселей, у которых максимум модуля разности RGBA со старым кадром больше 8, и число пикселей под правило 3 до и после очистки;
    - «### Генерация» — по помощникам: вызовы, повторы, отказы модерации, пропуски, плохие попытки с причинами.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт REFINERY:

> Edit image 1. Image 1 is a spice refinery from a real-time strategy game, drawn on a flat magenta background: a group of round grey storage tanks of different sizes with small red beacon masts, joined by thick pipes, and a square grey landing pad for harvesters with seven dark light slots: a long slot along the top, two short slots below it, an octagonal slot with a cross in the centre, two short slots below the centre and a long slot along the bottom. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the refinery as one solid building with exactly the outline, camera angle and faces of the grey block of image 2: the building fills the grey block from its left edge to its right edge and from its top edge to its bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, no side walls are visible, and nothing is drawn in the magenta bands above and below the block. Put these parts on the roof, seen from the same camera as the roof: the round storage tanks with their red beacon masts, joined by pipes, in the left half; the square landing pad in the right half, flat in the roof, with the same seven dark light slots in the same arrangement as in image 1. Give the front wall a closed hatch, small vents and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 in the bands above and below the block and in the two small cut corners at the top of the block, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт REPAIR:

> Edit image 1. Image 1 is a vehicle repair facility from a real-time strategy game, drawn on a flat magenta background: a large hangar with a curved silver roof and an arched vehicle gate, a lower workshop block with pipes and a round hatch, a small crane arm and orange crates. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the repair facility as one solid building with exactly the outline, camera angle and faces of the grey block of image 2: the building fills the grey block from its left edge to its right edge and from its top edge to its bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, no side walls are visible, and nothing is drawn in the magenta bands above and below the block. Put these parts on the roof, seen from the same camera as the roof: the large hangar with its curved silver roof in the right half; the lower workshop block with pipes and a round hatch, the small crane arm and a few orange crates in the left half. Give the front wall a wide closed vehicle gate below the hangar, made of horizontal metal slats in a frame, and small vents, lit windows and panel seams below the workshop block. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 in the bands above and below the block and in the two small cut corners at the top of the block, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт REPAIR-OPEN:

> Edit image 1. Image 1 is a vehicle repair facility from a real-time strategy game, drawn on a flat magenta background, with a wide closed vehicle gate made of horizontal metal slats in the front wall below the hangar. Open the gate: remove the slats of the gate completely and show the inside through the opening: an orange-lit repair platform floor, darker towards the top of the opening. Keep everything else exactly as it is: the same outline, camera angle, size and position of the building, the frame of the gate, every other part, and the same magenta areas. Do not add anything else: no vehicle, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт HIGHTECH-FIX:

> Edit image 1. Image 1 is a high-tech factory from a real-time strategy game, seen from above with its front wall along the bottom, drawn on a flat magenta background. Change only these three small details and keep everything else exactly as it is: the same outline, camera angle, layout, colours, and the size and position of every other part, and the same magenta areas. First: in the upper left part two vertical orange pipes run down from the long horizontal tank at the top across the light edge of the roof below the tank; draw the light roof edge as one unbroken line in front of both pipes, so that each pipe goes down from the tank, passes behind the roof edge and comes out below it. Second: on the far left a short orange pipe with a T-shaped top stands below the long tank, with a dark gap between its T-shaped top and the tank; connect the T-shaped top to the bottom of the tank with a short vertical orange pipe across the gap. Third: left of the large dome, near the step of the roof, a small loose orange pipe piece lies in a niche; remove it and draw the grey roof surface of the niche there. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт HIGHTECH-OPENFIX:

> Edit image 1. Image 1 is a high-tech factory from a real-time strategy game, seen from above with its front wall along the bottom, drawn on a flat magenta background, with a large open round pit with an orange floor in the middle of its roof. On the grey roof around the left and upper side of the pit there is a faint light curved line, the leftover outline of a dome. Remove this faint curved line and draw the plain grey roof surface there, matching the roof next to it. Keep everything else exactly as it is: the same outline, camera angle, layout, colours, the pit with its rim and orange floor, the size and position of every other part, and the same magenta areas. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

## Организация работы

- Порядок: шаг 1 → шаг 2 → `fit_box.py`, `edit_back.py`, `fix_compose.py` → запуск G7, G8, G9 (шаги 3, 6); корневая нить тем временем — шаги 7 (запуск на кадре растяжки), 8, 9 → после помощников — шаг 7 на результатах G9 → шаг 10 → `## DONE-U36-B1` и стоп.
- Параллельно: G7, G8 и G9 одновременно; шаги 7, 8, 9 корневой нити — во время генерации, независимо друг от друга.
- Помощники: G7, G8, G9 из шага 6, без вложенных.
- Остановки: только на `## DONE-U36-B1` и на блоках `## Q-U36-NN` задания и этого ответа.
- Рамка правок: только `.tmp/`.
- Журнал хода: `.tmp/progress-u36.md`, строка на законченный подпункт.
