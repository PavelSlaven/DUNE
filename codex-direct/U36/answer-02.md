## Ответ на DONE-U36-A (1): доработка части А — тёмные заводы

Владелец, 2026-11-05: «Лёгкий и тяжёлый завод надо потемнее, по типу хранилища». Ведущий выбрал варианты: Хранилище — `SILO_a`, Лёгкий завод — `LIGHTFACTORY_S2a`, Тяжёлый завод — `HEAVYFACTORY_S1a`. Эта доработка делает для двух заводов тёмные варианты в цветах выбранного Хранилища. Часть Б не начинай: решения по остальным зданиям придут следующим ответом. Пак и мастер-файлы не меняются, правки — только в `.tmp/`.

## Шаги

1. **Диск.** `df -h /srv`; свободно меньше 5 GB — блок `## Q-U36-02` со строкой вывода и стоп.

2. **Входы** (`.tmp/u36-in/`, все — RGB без альфы, наложение по альфе на сплошной фон RGB (255, 0, 255)):
   - `silo_style.png` — `.tmp/u36-fit/SILO_a.png`, увеличенный до 1024 × 1024 сжатием Lanczos;
   - `lightfactory_light.png` — `.tmp/u36-fit/LIGHTFACTORY_S2a.png`, увеличенный до 1024 × 1024 сжатием Lanczos;
   - `heavyfactory_light.png` — `.tmp/u36-fit/HEAVYFACTORY_S1a.png`, увеличенный до 1536 × 1024 сжатием Lanczos и вставленный в холст 1536 × 1536 цвета (255, 0, 255) в точку (0, 256).

3. **Вариант M — скриптом, без ImageGen.** Для каждого завода (`LIGHTFACTORY` из `LIGHTFACTORY_S2a.png`, `HEAVYFACTORY` из `HEAVYFACTORY_S1a.png`) построй `.tmp/u36-fit/<B>_M.png`:
   - переведи выбранный вариант и `.tmp/u36-fit/SILO_a.png` в YCbCr (Pillow, `convert("YCbCr")`);
   - образец — значения Y пикселей Хранилища с альфой больше 127; источник — значения Y пикселей завода с альфой больше 127;
   - новое Y каждого пикселя завода — сопоставление гистограмм: квантиль значения Y в распределении источника переводится в значение Y с тем же квантилем в распределении образца (`np.interp` по 256 уровням накопленных долей);
   - Cb, Cr и альфа не меняются; обратный перевод в RGB, альфа — исходная;
   - затем `angle.check` (плита 2x2 или 3x2, 1 кадр) и очистка каймы по правилу шага 6.

4. **Генерация ImageGen.** Два промпта на завод, по две попытки (`a`, `b`) — два независимых вызова с одним промптом и одними входными картинками. Всего 8 попыток.

   | Попытка | Промпт | Картинки вызова по порядку | Ориентир для `attempt.py` | Плита |
   |---|---|---|---|---|
   | `LIGHTFACTORY_D1a`, `_D1b` | `D1-LIGHTFACTORY` | 1 — `lightfactory_light.png`, 2 — `silo_style.png` | `guide_square.png` | 2x2 |
   | `LIGHTFACTORY_D2a`, `_D2b` | `D2-LIGHTFACTORY` | 1 — `lightfactory_src.png`, 2 — `guide_square.png`, 3 — `silo_style.png` | `guide_square.png` | 2x2 |
   | `HEAVYFACTORY_D1a`, `_D1b` | `D1-HEAVYFACTORY` | 1 — `heavyfactory_light.png`, 2 — `silo_style.png` | `guide_3x2.png` | 3x2 |
   | `HEAVYFACTORY_D2a`, `_D2b` | `D2-HEAVYFACTORY` | 1 — `heavyfactory_src.png`, 2 — `guide_3x2.png`, 3 — `silo_style.png` | `guide_3x2.png` | 3x2 |

   - Имена, копирование, журнал и `attempt.py` — как в шаге 5 и разделе «Правила генерации» задания U36. Журналы — `log-G5.tsv` (Лёгкий завод) и `log-G6.tsv` (Тяжёлый завод).
   - Правила генерации задания U36 действуют целиком, кроме пределов вызовов: G5 — 6 вызовов, G6 — 6 вызовов, повторы включены. Ссылки этих правил на шаг 5 задания для попыток этого ответа означают таблицу шага 4 этого ответа.

5. **Помощники.** Сразу после шага 2 запусти 2 помощника одновременно, `gpt-6-luna` `xhigh`, без вложенных помощников: G5 — попытки Лёгкого завода, G6 — попытки Тяжёлого завода. Бриф помощника содержит: строки таблицы шага 4 для его завода, его промпты из раздела «Промпты» дословно, раздел «Правила генерации» задания U36 с пределом из шага 4, команду запуска `attempt.py` и абзац из раздела «Комментарии в коде» задания U36 дословно. Пока помощники генерируют, корневая нить делает шаги 3 и 6.

6. **Очистка каймы, правило 2.** Проверяющие нашли на выбранных вариантах тусклую пурпурную кайму, которую правило шага 4 задания не ловит: например (185, 135, 189), (161, 110, 160), (235, 214, 246), полупрозрачная нижняя строка Тяжёлого завода (112, 71, 128) с альфой 188. Новый скрипт `.tmp/u36-tools/defringe2.py <вход.png> <выход.png>`:
   - пиксель каймы — альфа больше 0, G < min(R, B) − 12 и пиксель лежит не дальше 2 пикселей (по максимуму из |dx|, |dy|) от пикселя с альфой не больше 127 или от края кадра;
   - соседи пикселя каймы — пиксели окна 7 × 7 с центром в нём, у которых альфа больше 127 и которые сами не пиксели каймы; есть хотя бы один сосед — RGB заменяется средним RGB соседей с округлением, альфа не меняется; соседей нет — альфа становится 0;
   - один проход, соседи берутся из входной картинки;
   - печатает число пикселей каймы до и после (после — повторный подсчёт по тому же правилу на выходе).

   Примени `defringe2.py` ко всем файлам `.tmp/u36-fit/*.png`, кроме `*.fit.png`, включая новые попытки и варианты M: выход записывается поверх входа. До первого запуска скопируй `.tmp/u36-fit/` целиком в `.tmp/u36-fit-v1/`. После очистки выполни `angle.check` по каждому файлу; итог, отличный от итога до очистки, запиши в сдачу с именем файла.

7. **Листы** (`.tmp/u36-sheets/`, фон RGB (70, 68, 64), увеличение вдвое методом ближайшего соседа, по 4 ячейки в строке, подписи латиницей в полосах вне кадров):
   - `choice-LIGHTFACTORY-dark.png`: `old` (кадр 0 старой записи `BUILD_LIGHTFACTORY` с кадром 0 старой записи `BUILD_LIGHTFACTORY_FLAG` поверх), `S2a`, `M`, `D1a`, `D1b`, `D2a`, `D2b`, `silo` (`.tmp/u36-fit/SILO_a.png`);
   - `choice-HEAVYFACTORY-dark.png`: `old` (кадр 0 старой записи `BUILD_HEAVYFACTORY`), `S1a`, `M`, `D1a`, `D1b`, `D2a`, `D2b`, `silo`.
   - Пропущенная попытка — ячейка с заливкой RGB (128, 0, 0).

8. **Сдача.** Пришли `## DONE-U36-A2` по формату задания U36 и остановись. Сверх формата:
   - «### Листы» — пути двух листов;
   - «### Числа» — таблица попыток шага 4 (как в `DONE-U36-A`), средний Y непрозрачных пикселей: Хранилища, выбранных светлых вариантов, вариантов M, всех новых попыток; число пикселей каймы до и после правила 2 по каждому файлу `.tmp/u36-fit/*.png`; итог `check` после очистки;
   - «### Генерация» — по помощникам: вызовы, повторы, отказы модерации, пропуски, плохие попытки с причинами.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт D1-LIGHTFACTORY:

> Edit image 1. Image 1 is a light vehicle factory from a real-time strategy game, drawn on a flat magenta background and seen from the target camera: its flat roof from above and its front wall as a band along the bottom. Image 2 is another building of the same game, a spice silo, drawn in the target colours. Keep image 1 exactly as it is: the same outline, camera angle, layout, and the same shapes, positions and sizes of every part, and the same magenta areas. Change only the materials and colours to match image 2: medium-grey and dark-grey metal like the silo tanks, darker grey panels, a khaki-olive floor between the parts on the roof like the floor of the silo, and the same small glowing blue lights as in image 1, with no white or very light surfaces and no gold or yellow parts. Do not add, remove or move anything: no new pipes, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт D1-HEAVYFACTORY:

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, drawn on a flat magenta background and seen from the target camera: its flat roof from above and its front wall as a band along the bottom. Image 2 is another building of the same game, a spice silo, drawn in the target colours. Keep image 1 exactly as it is: the same outline, camera angle, layout, and the same shapes, positions and sizes of every part, the empty assembly pit, and the same magenta areas, including the magenta bands above and below the building. Change only the materials and colours to match image 2: medium-grey and dark-grey metal like the silo tanks, darker grey panels, a khaki-olive floor between the parts on the roof like the floor of the silo, and the same small glowing blue lights and the same red hatch as in image 1, with no white or very light surfaces and no gold or yellow parts. Do not add, remove or move anything: no new pipes, nothing inside the assembly pit, no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт D2-LIGHTFACTORY:

> Edit image 1. Image 1 is a light vehicle factory from a real-time strategy game, drawn on a flat magenta background: a dark-grey metal block with machinery, a round hatch near the top left corner, a short chimney, gold robot arms and an entrance ramp. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Image 3 is another building of the same game drawn in the target style; use it only as an example of the materials and colours, and do not copy its shape or details. Redraw the light factory as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put a round hatch with a light rim near the top left corner, a short chimney, machinery blocks and pipes on the roof, seen from the same camera as the roof. Give the front wall a wide closed vehicle gate, small vents and panel seams. Use the materials and colours of image 3: medium-grey and dark-grey metal, darker grey panels, a khaki-olive floor between the parts on the roof and small glowing blue lights, with no white or very light surfaces, no black surfaces and no gold or yellow robot arms. Keep the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт D2-HEAVYFACTORY:

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, drawn on a flat magenta background: a dark-grey metal hall with a machinery block, a round fan, a red octagonal hatch, an assembly bay with two crane rails and gold robot arms, and conveyor lines along the bottom. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Image 3 is another building of the same game drawn in the target style; use it only as an example of the materials and colours, and do not copy its shape or details. Redraw the heavy factory as one solid building with exactly the outline, camera angle and faces of the grey block of image 2: the building fills the grey block from its left edge to its right edge and from its top edge to its bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, no side walls are visible, and nothing is drawn in the magenta bands above and below the block. Put these parts on the roof, seen from the same camera as the roof: a large open assembly bay in the right half, which is an empty octagonal pit between two parallel crane rails with nothing inside the pit; a red octagonal hatch in the middle; a machinery block with a round fan and pipes in the left half. Give the front wall a wide closed vehicle gate, small vents and panel seams. Use the materials and colours of image 3: medium-grey and dark-grey metal, darker grey panels, a khaki-olive floor between the parts on the roof and small glowing blue lights, with no white or very light surfaces, no black surfaces and no gold or yellow robot arms. Keep the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 in the bands above and below the block and in the two small cut corners at the top of the block, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

## Организация работы

- Порядок: шаг 1 → шаг 2 → запуск G5 и G6 (шаги 4, 5); корневая нить тем временем — шаги 3 и 6 для имеющихся файлов → после помощников шаг 6 для новых попыток → шаг 7 → `## DONE-U36-A2` и стоп.
- Параллельно: G5 и G6 одновременно; шаги 3 и 6 корневой нити — во время генерации.
- Помощники: G5 и G6 из шага 5, без вложенных.
- Остановки: только на `## DONE-U36-A2` и на блоках `## Q-U36-NN` задания (`Q-U36-01` — нет ImageGen или он не принимает две или три входные картинки; `Q-U36-02` — мало диска; `Q-U36-03` — ошибка заготовки).
- Рамка правок: только `.tmp/`.
- Журнал хода: `.tmp/progress-u36.md`, строка на законченный подпункт.
