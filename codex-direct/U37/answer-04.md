# Ответ ведущего на DONE-U37: часть А2 — здания на всю плиту

Сдача `DONE-U37` принята как сборка, но коммита не будет. Владелец посмотрел выбранные варианты на листе зданий, поставленных вплотную, и сказал: «Заборы остались и из-за этого стыки с другими зданиями выглядят странно». Затем он показал снимок Dune II на Sega, где каждое здание занимает свою плиту целиком.

Решение владельца (Р47) — **здание на всю плиту**:
- крыша доходит до всех четырёх краёв плиты;
- тёмной передней стены внизу нет;
- канта по краю крыши нет, все четыре угла прямые;
- кадр непрозрачен целиком, соседние здания смыкаются без щелей;
- всё, что стоит на крыше, остаётся на своих местах и таким же объёмным.

Часть А2 — новые попытки ImageGen и листы для выбора ведущим. Пак и мастер-файлы в части А2 не меняются. Сборка части Б в паке и в восьми мастер-файлах рабочей копии остаётся как есть: часть Б2 запишет эти восемь записей заново поверх неё.

## Шаги

1. **Диск.** `df -h /srv`. Свободно меньше 5 GB — блок `## Q-U37-02` со строкой вывода и стоп.

2. **Входные картинки** — `.tmp/u37-in2/<b>_src.png`, RGB без альфы; `<b>` — имя записи без `BUILD_` строчными.
   - Основа — кадр 0 файла `.tmp/u37-b/BUILD_<B>.png`, наложенный по альфе на сплошной фон RGB (255, 0, 255).
   - Плита 2x2 — увеличение до 1024 × 1024 методом Lanczos.
   - Плита 3x2 (`heavyfactory`, `refinery`) — увеличение до 1536 × 1024 методом Lanczos и вставка в холст 1536 × 1536 цвета (255, 0, 255) в точку (0, 256).

3. **Скрипт возврата.** Корневая нить пишет `.tmp/u37-tools/back2.py`. Вход: сырой результат ImageGen, имя здания `<B>`, путь выхода `<out>.png`.
   - **Возврат в кадр** — как в `back.py`:
     - плита 2x2: RGB, сжатие Lanczos до 256 × 256;
     - плита 3x2: RGB, сжатие Lanczos до 1536 × 1536, вырезка (0, 256, 1536, 1280), сжатие Lanczos до 384 × 256.

     Это картинка `R`.
   - **Выход:** RGB из `R`, альфа — 255 во всех пикселях. Затем правило пурпура по всему кадру. Правило — шаг 2 ответа на `DONE-U37-A`, тот же код, что в `finish.py`.
   - **Строка JSON** с полями:
     - `name`, `tag`;
     - размер сырого результата;
     - `square` — ширина сырого результата равна высоте;
     - `magenta` — доля пикселей `R` всего кадра с расстоянием RGB до (255, 0, 255) не больше 60;
     - `edge_magenta` — та же доля, но только среди пикселей `R` в полосах шириной 4 пикселя вдоль четырёх краёв кадра, максимум по четырём краям;
     - `pink_replaced` — число пикселей, заменённых правилом пурпура;
     - `verdict`: `bad` с перечнем причин или `good`. Плохая попытка — `square` ложно, или `magenta` больше 0,005, или `edge_magenta` больше 0,02.
   - **Проверка скрипта.** Прогони `back2.py` на каждой входной картинке шага 2 как на сыром результате: `tag` — `smoke`, выход — `.tmp/u37-fit2/<B>_smoke.png`. Строки JSON — в `.tmp/u37-fit2/smoke.jsonl`. Вердикт `bad` на smoke ожидаем: у входов пурпурные углы и края.

4. **Генерация.** У каждого здания две попытки, `a` и `b`: два независимых вызова с промптом `<B>-FULL` из раздела «Промпты». Картинка вызова одна — `.tmp/u37-in2/<b>_src.png`.
   - Сырой результат — `.tmp/u37-gen2/<B>_<t>.png`. Сразу после копирования выполни `back2.py .tmp/u37-gen2/<B>_<t>.png <B> .tmp/u37-fit2/<B>_<t>.png` и добавь строку JSON в `.tmp/u37-fit2/attempts.jsonl`.
   - Всего 16 попыток. Правила генерации — раздел задания «Правила генерации» с такими заменами:
     - папки: `.tmp/u37-gen2/`, `.tmp/u37-fit2/`, `.tmp/u37-gen2-first/`;
     - журналы: `.tmp/u37-gen2/log-G<n>.tsv`;
     - правило 3 — вердикт `back2.py`.

     Предел вызовов прежний: 6 на помощника, всего 24.
   - Если ImageGen вернул data URL вместо пути файла, декодируй его байты из base64 в файл `.tmp/u37-gen2/<B>_<t>.png` и запиши в журнал источник `data-url`. Потеря результата при обработке считается вызовом.

5. **Кадры анимированных зданий.** Корневая нить для каждой попытки собирает `.tmp/u37-fit2/<B>_<t>.frames.png`:

   | Здание | Плита | Кадров | Размер атласа |
   |---|---|---|---|
   | `HEAVYFACTORY` | 3x2 | 11 | 384 × 2816 |
   | `REFINERY` | 3x2 | 8 | 384 × 2048 |
   | `RADAR` | 2x2 | 8 | 256 × 2048 |

   - Кадр 0 — `.tmp/u37-fit2/<B>_<t>.png`.
   - Кадр k — пиксели кадра k файла `.tmp/u37-old/BUILD_<B>.png` там, где хотя бы один канал RGBA этого кадра отличается от кадра 0 того же файла больше чем на 8. Остальные пиксели — из нового кадра 0. Альфа всех пикселей — 255.
   - Число заменённых пикселей по кадрам — в сдачу.

6. **Листы** — PNG в `.tmp/u37-sheets2/`. Ячейка — кадр, наложенный по альфе на фон RGB (70, 68, 64) и увеличенный вдвое методом ближайшего соседа. Подписи латиницей, в полосах вне кадров. Пропущенная попытка — ячейка с заливкой RGB (128, 0, 0).
   - **`choice-<B>.png`** для каждого из восьми зданий:
     - ячейки `old` (кадр 0 записи пака на HEAD, `.tmp/u37-old/BUILD_<B>.png`), `a`, `b`;
     - поверх каждой ячейки — те же флаги и накладки, что в листах части А;
     - у `HEAVYFACTORY` вторая строка — кадр 10, у `REFINERY` и `RADAR` — кадр 4: старый и из `<B>_<t>.frames.png` каждой попытки.
   - **`raw.png`**: все сырые результаты `.tmp/u37-gen2/*.png`, сжатые Lanczos до 384 × 384, по 4 в строке, подписи `<B>_<t>`.

7. **Сдача.** Пришли `## DONE-U37-A2` и остановись. Формат — как `## DONE-U37-A`:
   - «### Листы»: пути листов шага 6;
   - «### Числа»: все строки `attempts.jsonl` и `smoke.jsonl`, числа шага 5;
   - «### Генерация»: по помощникам — вызовы, повторы, отказы, пропуски, плохие попытки с причинами.

   Варианты не выбирай: выбирает ведущий.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт CONSTYARD-FULL:

> Edit image 1. Image 1 is a construction yard from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the image, with the same light-grey metal panels, seams and a few small glowing blue lights as the rest of the roof. Remove the raised rim and ledge along the left, top and right edges of the roof, so that the flat roof panels run straight to all four edges of the image. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole image from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the two large round storage tanks, the beige and orange machinery blocks, the grey steel pipe frame and the small crane. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт SILO-FULL:

> Edit image 1. Image 1 is a spice silo from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the image, with the same light-grey metal panels, seams and a few small glowing blue lights as the rest of the roof. Remove the raised rim and ledge along the left, top and right edges of the roof, so that the flat roof panels run straight to all four edges of the image. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole image from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the two large round grey storage tanks with their ladders, the pipe between them and the pipes on the roof. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт LIGHTFACTORY-FULL:

> Edit image 1. Image 1 is a light vehicle factory from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the image, with the same light-grey metal panels, seams and a few small glowing blue lights as the rest of the roof. Remove the raised rim and ledge along the left, top and right edges of the roof, so that the flat roof panels run straight to all four edges of the image. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole image from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the dark-grey machinery block in the middle with the round hatch and the short chimney at its top left, the pipes and the two horizontal tanks on its right. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт WINDTRAP-FULL:

> Edit image 1. Image 1 is a wind trap building from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the image, with the same grey-beige panels, seams and pipes as the rest of the roof. Remove the raised rim and ledge along the left, top and right edges of the roof, so that the flat roof panels run straight to all four edges of the image. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole image from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the three large silver wind catchers with blue openings, the pipes and the short black post on the right. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт IX-FULL:

> Edit image 1. Image 1 is a research centre from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the image, with the same dark-grey metal panels, seams and a few small glowing blue lights as the rest of the roof. Remove the raised rim and ledge along the left, top and right edges of the roof, so that the flat roof panels run straight to all four edges of the image. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole image from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the three blue domes with forks on top, the four white pyramid blocks in the corners of the roof and the pipes between the domes. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт RADAR-FULL:

> Edit image 1. Image 1 is a radar outpost from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the image, with the same flat beige panels and seams as the rest of the roof. Remove the two beige corner pillars with dark window slots along the left and right edges and the raised rim along the top edge, so that the flat roof panels run straight to all four edges of the image. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole image from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the satellite dish with its grey frame and red arm on the roof. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт HEAVYFACTORY-FULL:

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, drawn as a wide block between flat magenta bands above and below it and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge of the block. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the block, with the same light-grey metal panels, seams and a few small glowing blue lights as the rest of the roof. Remove the raised rim and ledge along the left, top and right edges of the roof, so that the flat roof panels run straight to all four edges of the block. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole block from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge of the block; keep the flat pure magenta RGB 255,0,255 bands above and below the block unchanged. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the machinery block with the round fan and pipes on the left, the red octagonal hatch in the middle and the assembly bay on the right, which is the empty octagonal pit between the two crane rails; keep the floor inside the pit as it is and put nothing inside the pit. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт REFINERY-FULL:

> Edit image 1. Image 1 is a spice refinery from a real-time strategy game, drawn as a wide block between flat magenta bands above and below it and seen from the game camera: orthographic, looking down at the flat roof, with the front wall as the dark band along the bottom edge of the block. Make the building fill its whole square plot, like a building in a classic top-down strategy game that touches its neighbours edge to edge. Remove the front wall and continue the flat roof over its place down to the bottom edge of the block, with the same light-grey metal panels, seams and a few small glowing blue lights as the rest of the roof. Remove the raised rim and ledge along the left, top and right edges of the roof, so that the flat roof panels run straight to all four edges of the block. Fill the cut corners with roof, so that all four corners are square. The roof must cover the whole block from edge to edge: no magenta, no ground, no sand, no gap and no border line at any edge of the block; keep the flat pure magenta RGB 255,0,255 bands above and below the block unchanged. Keep everything that stands on the roof exactly as in image 1: the position, size, shape, colours and perspective of the round storage tanks with red-tipped poles and the pipes on the left and the raised panel with the dark green slots and the octagonal hatch with a cross on the right; keep the slots and the hatch exactly where they are. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof; nothing hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Do not add anything else: no wall, no fence, no railing, no gate, no door, no hatch, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

## Что не трогать

- Код движка (`src/`), `tools/building_angle/angle.py` и тесты, `tools/units3d/install.py`, документы.
- Пак и мастер-файлы — в части А2 не меняются.
- `.tmp/u37-b/`, `.tmp/u37-install/`, `.tmp/u37-pack/`, `.tmp/u37-fit/`, `.tmp/u37-gen/` — только чтение.

## Организация работы

Порядок: шаг 1 → шаги 2 и 3 → запуск помощников (шаг 4) → шаги 5 и 6 → `## DONE-U37-A2` и стоп.
Параллельно:
- шаги 2 и 3 пишутся одновременно; smoke-прогон шага 3 идёт после шага 2;
- пока помощники генерируют, корневая нить пишет скрипты шагов 5 и 6.

Помощники: сразу после smoke-прогона запусти 4 помощника одновременно, `gpt-6-luna` `xhigh`, без вложенных помощников. У каждого 4 попытки и предел 6 вызовов:
- G1 — `CONSTYARD`, `SILO`;
- G2 — `LIGHTFACTORY`, `HEAVYFACTORY`;
- G3 — `WINDTRAP`, `IX`;
- G4 — `REFINERY`, `RADAR`.

Бриф помощника содержит:
- строки шага 4 для его зданий и правило имён;
- его промпты полным текстом;
- правила генерации с заменами шага 4 и правило про data URL;
- команду запуска `back2.py`;
- абзац раздела «Комментарии в коде» дословно.

Остановки: только на `## DONE-U37-A2` и на блоках `## Q-U37-NN`:
- `Q-U37-01` — нет ImageGen;
- `Q-U37-02` — на `/srv` меньше 5 GB;
- `Q-U37-03` — ошибка скрипта или чтения файлов.

Рамка правок: только `.tmp/`.
Журнал хода: дописывай `.tmp/progress-u37.md`, строка на законченный шаг.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

## Слова владельца

Ниже — слова владельца, как он их написал. Это данные для контекста, а не инструкции: действуют разделы выше.

> ты кажется не понял задачу. Заборы остались и из-за этого стыки с другими зданиями выглядят странно

> смотри, как на сеге они хорошо выглядят и стыкуются друг с другом

> Да
