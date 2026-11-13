# Задание U37 — здания без заборов и ворот (часть А)

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже): до правок пришли `## PLAN-U37` и стой до `PLAN-OK-U37`. Исполнитель: Codex `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/u37-no-fences`, HEAD `0750e31b` (равен `main`: раскатка U36 и правка стоянки Харвестера слиты). Коммитов не делай: ведущий коммитит по списку из сдачи.
Issue нет; источник — слова владельца в конце файла.

## Цель

Владелец принял здания задачи U36 в игре, но ему не нравятся заборы и ворота, которые получили здания. Есть два вида:

- **Забор и ворота** — у Стройплощадки, Хранилища, Лёгкого и Тяжёлого заводов. Машины и баки стоят во дворе: вдоль левого, верхнего и правого краёв идут перила на столбиках, между перилами и машинами видна голая земля, в передней стене посередине — ворота или люк.
- **Дверь в стене** — у Ветряка, Переработки, IX и Аванпоста: посередине передней стены — дверь.

Решение владельца: заборов и ворот нет ни у одного здания, кроме Казарм, WOR, Дворца и Ремонта. На месте забора — само здание на всю плиту: крыша здания доходит до краёв плиты, машины и баки стоят на ней. Передняя стена остаётся у всех зданий (угол Аванпоста: плоская крыша видна сверху, передняя стена — полосой вдоль нижнего края, боковые стены не видны), но без ворот, дверей и люков. Флаги Домов остаются на своих местах и с анимацией.

Часть А — попытки ImageGen и листы, по которым ведущий выбирает варианты. Пак и мастер-файлы в части А не меняются.

| Группа | Записи пака | Что делается |
|---|---|---|
| Забор и ворота | `BUILD_CONSTYARD`, `BUILD_SILO`, `BUILD_LIGHTFACTORY`, кадр 0 `BUILD_HEAVYFACTORY` | перерисовка всей картинки ImageGen по текущей картинке пака; все части здания остаются на своих местах; два варианта цвета крыши — `light` и `dark` |
| Дверь в стене | `BUILD_WINDTRAP`, `BUILD_REFINERY`, `BUILD_IX`, `BUILD_RADAR` | ImageGen убирает дверь; в результат идёт только полоса передней стены (строки от `y0` до низа кадра), крыша и анимация остаются прежними; две попытки — `a` и `b` |
| Не трогать | `BUILD_BARRACKS`, `BUILD_WOR`, `BUILD_PALACE`, `BUILD_REPAIR`, `BUILD_HIGHTECH`, `BUILD_STARPORT`, `BUILD_TURRET`, `BUILD_RTURRET` | ничего |

## Что есть

- Пак: `resources/bin/data/sdl_data_hd4.dat`, 241 запись. Чтение — `tools.hd_assets.read_pack(Path)` и `tools.hd_assets.decode_image` (как в `tools/building_angle/tests/test_pilot_pack.py`).
- Заготовка `tools/building_angle/angle.py`: в своих скриптах `sys.path.insert(0, "tools/building_angle")`, `import angle`. Нужны функции `angle.check(atlas, (N, M), K)` (доли покрытия краёв и касание; итог `pass`, если у всех кадров все четыре доли не меньше 0,85 и касание есть) и `angle.shadow`. Заготовку и её тесты не меняй.
- Записи пака (ведущий измерил на HEAD; кадры сложены столбцом):

| Здание | Плита | Кадр | Кадров | `y0` | Связанные записи |
|---|---|---|---|---|---|
| `BUILD_CONSTYARD` | 2x2 | 256 × 256 | 1 | — | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров) |
| `BUILD_SILO` | 2x2 | 256 × 256 | 1 | — | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров) |
| `BUILD_LIGHTFACTORY` | 2x2 | 256 × 256 | 1 | — | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров); накладки `BUILD_LIGHTFACTORY_PRODUCTION` (8 кадров) и `BUILD_LIGHTFACTORY_FLASH` (1 кадр) |
| `BUILD_HEAVYFACTORY` | 3x2 | 384 × 256 | 11 | — | `_SHADOW` (11 кадров); накладка `BUILD_HEAVYFACTORY_FLASH` (1 кадр); флага нет |
| `BUILD_WINDTRAP` | 2x2 | 256 × 256 | 1 | 202 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров) |
| `BUILD_REFINERY` | 3x2 | 384 × 256 | 8 | 191 | `_SHADOW`; маска Дома здания `HM_BUILD_REFINERY` (8 кадров); `_FLAG`, `HM_…_FLAG` (8 кадров) |
| `BUILD_IX` | 2x2 | 256 × 256 | 1 | 189 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров) |
| `BUILD_RADAR` | 2x2 | 256 × 256 | 8 | 193 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров) |

- `y0` — первая строка полосы передней стены, которая заменяется у зданий группы «Дверь в стене»: на 2–4 строки ниже нижнего края крыши, выше верха двери (ведущий проверил по вырезкам).
- Анимация Тяжёлого завода: в кадрах 1–10 в сборочном отсеке между двумя рельсами снизу вверх собирается машина. Анимация Переработки — огни в щелях на крыше, Аванпоста — вращение антенны на крыше; обе выше `y0`.
- Движок рисует тень в том же прямоугольнике, что и здание, и до здания; флаги и накладки — поверх здания в том же прямоугольнике. Код движка не меняется.
- Среда: `/srv/dune/venv/bin/python` (Pillow, numpy, scipy, `unittest`; `cv2` и pytest нет). Сети нет, пакеты не устанавливаются. Git LFS — `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.
- Диск: перед шагом 2 выполни `df -h /srv`. Свободно меньше 5 GB — блок `## Q-U37-02` со строкой вывода и стоп.

## Часть А

1. **Старые записи.** Извлеки из пака на HEAD в `.tmp/u37-old/<ЗАПИСЬ>.png` (RGBA, без изменений) все записи из таблицы «Записи пака»: здания, тени, флаги, маски `HM_*`, накладки.

2. **Входные картинки ImageGen** (`.tmp/u37-in/<b>_src.png`, RGB без альфы; `<b>` — имя записи без `BUILD_` строчными: `constyard`, `silo`, `lightfactory`, `heavyfactory`, `windtrap`, `refinery`, `ix`, `radar`): кадр 0 записи пака, наложенный по альфе на сплошной фон RGB (255, 0, 255). Плита 2x2 — увеличение до 1024 × 1024 сжатием Lanczos. Плита 3x2 (`heavyfactory`, `refinery`) — увеличение до 1536 × 1024 сжатием Lanczos и вставка в холст 1536 × 1536 цвета (255, 0, 255) в точку (0, 256).

3. **Скрипт возврата.** До запуска помощников корневая нить пишет `.tmp/u37-tools/back.py`. Вход: сырой результат ImageGen, имя здания `<B>` (имя записи без `BUILD_` прописными), путь выхода `<out>.png`. Скрипт:
   - **Возврат в кадр.** Сырой результат переводится в RGB. Плита 2x2: сжатие Lanczos до 256 × 256. Плита 3x2: сжатие Lanczos до 1536 × 1536, вырезка (0, 256, 1536, 1280), сжатие Lanczos до 384 × 256. Это картинка `R`.
   - **Группа «Забор и ворота».** Выход: RGB из `R`, альфа — альфа кадра 0 старой записи `.tmp/u37-old/BUILD_<B>.png`. Затем очистка пурпурной каймы (правило ниже) по всему кадру.
   - **Группа «Дверь в стене».** Выход: копия кадра 0 старой записи; в строках от `y0` до последней RGB заменяется RGB из `R`, альфа остаётся старой. Затем очистка пурпурной каймы только в строках от `y0` до последней.
   - Печатает одну строку JSON с полями: `name`, `tag`, размер сырого результата, `square` (ширина сырого результата равна высоте), `magenta` — доля пикселей `R` с расстоянием RGB до (255, 0, 255) не больше 60 среди пикселей, у которых альфа старого кадра 0 больше 127 (у группы «Дверь в стене» — только в строках от `y0`), число пикселей каймы до и после очистки; для группы «Забор и ворота» — итог и наименьшая доля `angle.check(<out>.png, плита, 1)` и `diff` — среднее по каналам RGB модуля разности `R` и старого кадра 0 по пикселям с альфой старого кадра больше 127; для группы «Дверь в стене» — `align` (то же среднее по строкам от `y0 − 40` до `y0 − 1`) и `band` (то же среднее по строкам от `y0` до последней); поле `verdict`: `bad` с перечнем причин по правилу 3 раздела «Правила генерации» или `good`.
   - **Проверка скрипта.** Прогони `back.py` на каждой входной картинке шага 2 как на сыром результате (`tag` — `smoke`, выход — `.tmp/u37-fit/<B>_smoke.png`). Строки JSON — в `.tmp/u37-fit/smoke.jsonl` и в сдачу: они показывают, какие `diff` и `align` даёт сам возврат без ImageGen.

   **Очистка пурпурной каймы** (то же правило, что в задании U36). Пиксель каймы — альфа больше 0, R − G > 50, B − G > 50 и |R − B| < 90. Для каждого пикселя каймы соседи — пиксели окна 5 × 5 с центром в нём, у которых альфа больше 127 и которые сами не пиксели каймы. Есть хотя бы один сосед — RGB пикселя заменяется средним RGB соседей (с округлением), альфа не меняется; соседей нет — альфа становится 0. Один проход по копии: соседи берутся из картинки до очистки.

4. **Генерация.** Промпты — раздел «Промпты».

   | Здание | Попытки и промпты | Картинка вызова |
   |---|---|---|
   | `CONSTYARD`, `SILO`, `LIGHTFACTORY`, `HEAVYFACTORY` | `light` — промпт `<B>-LIGHT`; `dark` — промпт `<B>-DARK` | 1 — `<b>_src.png` |
   | `WINDTRAP`, `REFINERY`, `IX`, `RADAR` | `a` и `b` — два независимых вызова с промптом `<B>-DOOR` | 1 — `<b>_src.png` |

   - Имена: сырой результат — `.tmp/u37-gen/<B>_<t>.png` (`<t>` — `light`, `dark`, `a` или `b`). Сразу после копирования — `back.py .tmp/u37-gen/<B>_<t>.png <B> .tmp/u37-fit/<B>_<t>.png`; строку JSON добавь в `.tmp/u37-fit/attempts.jsonl`.
   - Всего 16 попыток: 8 зданий × 2.

5. **Кадры Тяжёлого завода.** Для каждой попытки `HEAVYFACTORY_<t>` корневая нить собирает `.tmp/u37-fit/HEAVYFACTORY_<t>.frames.png` (384 × 2816, 11 кадров): кадр 0 — `.tmp/u37-fit/HEAVYFACTORY_<t>.png`; кадр k (1…10) — пиксели старого кадра k там, где хотя бы один канал RGBA старого кадра k отличается от старого кадра 0 больше чем на 8, остальные пиксели — из нового кадра 0. Число заменённых пикселей по кадрам — в сдачу.

6. **Маска Дома Переработки.** Для каждого кадра старого `HM_BUILD_REFINERY` посчитай пиксели в строках от 191 до 255, у которых альфа больше 0 и максимум RGB больше 0. Числа — в сдачу.

7. **Листы.** PNG в `.tmp/u37-sheets/`. Ячейка — кадр, наложенный по альфе на фон RGB (70, 68, 64), увеличенный вдвое методом ближайшего соседа. Подписи — латиницей, в полосах вне кадров. Пропущенная попытка — ячейка с заливкой RGB (128, 0, 0).
   - `choice-<B>.png` для каждого из восьми зданий: ячейка `old` — кадр 0 старой записи, затем ячейки попыток (`light`, `dark` или `a`, `b`). Поверх каждой ячейки — кадр 0 старого листа `BUILD_<B>_FLAG` (у Тяжёлого завода флага нет). У Лёгкого завода поверх ещё кадр 0 `BUILD_LIGHTFACTORY_PRODUCTION` и `BUILD_LIGHTFACTORY_FLASH`, у Тяжёлого — `BUILD_HEAVYFACTORY_FLASH`. У Тяжёлого завода вторая строка — кадр 10: старый и из `HEAVYFACTORY_<t>.frames.png` каждой попытки. У зданий группы «Дверь в стене» вторая строка — вырезка строк от `y0 − 24` до последней из тех же ячеек, увеличенная вчетверо методом ближайшего соседа.
   - `raw.png`: все сырые результаты `.tmp/u37-gen/*.png`, сжатые Lanczos до 384 × 384, по 4 в строке, подписи `<B>_<t>`.

8. **Сдача части А.** Пришли `## DONE-U37-A` по разделу «Сдача» и остановись. Исполнитель вид листов не оценивает и варианты не выбирает: выбирает ведущий. Плохие и пропущенные попытки не мешают сдаче.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Общая часть промптов группы «Забор и ворота» отличается только описанием здания и его частей; промпты `-LIGHT` и `-DARK` одного здания отличаются только словами `light-grey` и `dark-grey` в описании крыши.

Промпт CONSTYARD-LIGHT:

> Edit image 1. Image 1 is a construction yard from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof and at the front wall, which is the dark band along the bottom edge; the side walls are not visible. In image 1 the machinery stands in a fenced yard: a steel railing on short posts runs along the left, top and right edges, bare ground shows between the railing and the machinery, and the front wall has a wide closed vehicle gate with yellow and black stripes in its middle. Change only these things. Remove the railing and all its posts. Replace all bare ground with the flat roof of the building, made of light-grey metal panels with seams and a few small glowing blue lights, reaching the left, top and right edges of the building, so that the whole area above the front wall is the roof of the building and the machinery stands on it. Remove the gate from the front wall and continue the front wall across its place with the same dark panels, seams, small vents and small blue lights, so that the front wall has no gate, door or hatch. Keep everything else exactly as in image 1: the size and outline of the building, the camera angle, the height and top edge of the front wall, and the position, size, shape and colours of the two large round storage tanks, the beige and orange machinery blocks, the grey steel pipe frame and the small crane. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Show no ground, no concrete pad and no sand anywhere. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт CONSTYARD-DARK — промпт CONSTYARD-LIGHT, в котором слова `light-grey metal panels` заменены на `dark-grey metal panels`.

Промпт SILO-LIGHT:

> Edit image 1. Image 1 is a spice silo from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof and at the front wall, which is the dark band along the bottom edge; the side walls are not visible. In image 1 the storage tanks stand in a fenced yard: a steel railing on short posts runs along the left, top and right edges, bare ground shows between the railing and the tanks, and the front wall has a closed hatch in its middle. Change only these things. Remove the railing and all its posts. Replace all bare ground with the flat roof of the building, made of light-grey metal panels with seams and a few small glowing blue lights, reaching the left, top and right edges of the building, so that the whole area above the front wall is the roof of the building and the tanks stand on it. Remove the hatch from the front wall and continue the front wall across its place with the same dark panels, seams, small vents and small blue lights, so that the front wall has no gate, door or hatch. Keep everything else exactly as in image 1: the size and outline of the building, the camera angle, the height and top edge of the front wall, and the position, size, shape and colours of the two large round grey storage tanks with their ladders and of the pipe between them. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Show no ground, no concrete pad and no sand anywhere. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт SILO-DARK — промпт SILO-LIGHT, в котором слова `light-grey metal panels` заменены на `dark-grey metal panels`.

Промпт LIGHTFACTORY-LIGHT:

> Edit image 1. Image 1 is a light vehicle factory from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof and at the front wall, which is the dark band along the bottom edge; the side walls are not visible. In image 1 the machinery stands in a fenced yard: a steel railing on short posts runs along the left, top and right edges, bare ground shows between the railing and the machinery, and the front wall has a wide closed vehicle gate in its middle. Change only these things. Remove the railing and all its posts. Replace all bare ground with the flat roof of the building, made of light-grey metal panels with seams and a few small glowing blue lights, reaching the left, top and right edges of the building, so that the whole area above the front wall is the roof of the building and the machinery stands on it. Remove the gate from the front wall and continue the front wall across its place with the same dark panels, seams, small vents and small blue lights, so that the front wall has no gate, door or hatch. Keep everything else exactly as in image 1: the size and outline of the building, the camera angle, the height and top edge of the front wall, and the position, size, shape and colours of the dark-grey machinery block in the middle with the round hatch and the short chimney at its top left, of the pipes and of the two horizontal tanks on its right. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Show no ground, no concrete pad and no sand anywhere. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт LIGHTFACTORY-DARK — промпт LIGHTFACTORY-LIGHT, в котором слова `light-grey metal panels` заменены на `dark-grey metal panels`.

Промпт HEAVYFACTORY-LIGHT:

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, drawn as a wide block between flat magenta bands above and below it and seen from the game camera: orthographic, looking down at the flat roof and at the front wall, which is the dark band along the bottom edge of the block; the side walls are not visible. In image 1 the machinery stands in a fenced yard: a steel railing on short posts runs along the left, top and right edges of the block, bare ground shows between the railing and the machinery, and the front wall has a wide closed vehicle gate in its middle. Change only these things. Remove the railing and all its posts. Replace the bare ground outside the assembly pit with the flat roof of the building, made of light-grey metal panels with seams and a few small glowing blue lights, reaching the left, top and right edges of the block, so that the whole area above the front wall is the roof of the building and the machinery stands on it. Remove the gate from the front wall and continue the front wall across its place with the same dark panels, seams, small vents and small blue lights, so that the front wall has no gate, door or hatch. Keep everything else exactly as in image 1: the size and outline of the block, the camera angle, the height and top edge of the front wall, and the position, size, shape and colours of the machinery block with the round fan and pipes on the left, of the red octagonal hatch in the middle and of the assembly bay on the right, which is the empty octagonal pit between the two crane rails; keep the floor inside the pit as it is and put nothing inside the pit. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Show no ground, no concrete pad and no sand anywhere outside the pit. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is, including the bands above and below the block. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт HEAVYFACTORY-DARK — промпт HEAVYFACTORY-LIGHT, в котором слова `light-grey metal panels` заменены на `dark-grey metal panels`.

Промпт WINDTRAP-DOOR:

> Edit image 1. Image 1 is a wind trap building from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof and at the front wall, which is the dark band along the bottom edge; the side walls are not visible. The front wall has a closed metal door in a raised frame in its middle. Change only the front wall: remove the door and its frame and continue the front wall across their place with the same dark panels, seams, small vents and small lights, so that the front wall is one continuous wall with no door, gate or hatch. Keep everything else exactly as in image 1: the roof and everything on it, the size and outline of the building, the camera angle, and the height and top edge of the front wall. Every part must make physical sense: there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт REFINERY-DOOR:

> Edit image 1. Image 1 is a spice refinery from a real-time strategy game, drawn as a wide block between flat magenta bands above and below it and seen from the game camera: orthographic, looking down at the flat roof and at the front wall, which is the dark band along the bottom edge of the block; the side walls are not visible. The front wall has a closed octagonal double door with small blue lights in its middle. Change only the front wall: remove the door and its frame and continue the front wall across their place with the same dark panels, seams, small vents and small blue lights, so that the front wall is one continuous wall with no door, gate or hatch. Keep everything else exactly as in image 1: the roof and everything on it, the size and outline of the block, the camera angle, and the height and top edge of the front wall. Every part must make physical sense: there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is, including the bands above and below the block. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт IX-DOOR:

> Edit image 1. Image 1 is a research centre from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat roof and at the front wall, which is the dark band along the bottom edge; the side walls are not visible. The front wall has a closed metal double door in a raised frame with two small blue lights in its middle. Change only the front wall: remove the door, its frame and its two lights and continue the front wall across their place with the same dark panels, seams, small vents and small blue lights, so that the front wall is one continuous wall with no door, gate or hatch. Keep everything else exactly as in image 1: the roof and everything on it, the size and outline of the building, the camera angle, and the height and top edge of the front wall. Every part must make physical sense: there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт RADAR-DOOR:

> Edit image 1. Image 1 is a radar outpost from a real-time strategy game, drawn on a flat magenta background and seen from the game camera: orthographic, looking down at the flat beige roof and at the front wall, which is the darker band along the bottom edge between two beige corner pillars; the side walls are not visible. The front wall has a dark open doorway in a raised frame to the right of its middle. Change only the front wall: remove the doorway and its frame and continue the front wall across their place with the same panels, seams and small window slots, so that the front wall is one continuous wall with no door, doorway, gate or hatch. Keep everything else exactly as in image 1: the roof and everything on it, the two corner pillars, the size and outline of the building, the camera angle, and the height and top edge of the front wall. Every part must make physical sense: there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпты — новая формулировка этого задания; работают ли они, не проверено. Поэтому вид оценивает ведущий по листам.

## Правила генерации (для корневой нити и для каждого помощника)

1. Один вызов ImageGen — один результат. Входная картинка вызова — ровно та, что названа в шаге 4 для его промпта.
2. Сразу после вызова скопируй выходной файл из `$CODEX_HOME/generated_images` в `.tmp/u37-gen/` байт в байт под именем из шага 4: без изменения размера и без пересжатия. Выходной файл бери по пути, который вернул вызов ImageGen, а не по времени изменения. В журнал `.tmp/u37-gen/log-G<n>.tsv` (`<n>` — номер помощника; корневая нить, если генерирует сама, пишет `log-G0.tsv`) добавь строку из полей через табуляцию: время UTC, слово `copied`, имя результата, путь источника, sha256 результата. Затем выполни `back.py` (шаг 4).
3. Плохая попытка — выполнено хотя бы одно: `square` ложно; `magenta` больше 0,02; у группы «Забор и ворота» итог `angle.check` — `FAIL`.
4. Плохая попытка — один повтор. Заменённые файлы (сырой результат и выход `back.py`) перенеси в `.tmp/u37-gen-first/` с теми же именами; результат повтора получает основное имя. Повтор тоже плохой — оставь его под основным именем, в журнал запиши строку `bad` с причинами и иди дальше.
5. Отказ модерации — один повтор. Второй отказ — попытка пропущена: в журнал строка `skipped` с первыми 200 символами текста отказа.
6. Предел вызовов ImageGen, повторы включены: 6 на помощника, всего 24. Предел достигнут — генерация помощника останавливается; в сдаче — число вызовов и что осталось без результата.
7. ImageGen недоступен ни корневой нити, ни помощникам — блок `## Q-U37-01` и стоп.

## Часть Б (только после ответа ведущего)

Часть Б выполняется по ответу ведущего на `## DONE-U37-A`; ответ — источник истины для неё. Ожидаемый состав, чтобы план части А его учитывал:

- выбранные попытки по зданиям;
- у Переработки и Аванпоста полоса передней стены выбранной попытки ставится во все кадры здания, крыша кадров остаётся прежней; у Тяжёлого завода в пак идёт `HEAVYFACTORY_<t>.frames.png`;
- сдвиги флагов и накладок, если части здания на выбранной картинке сдвинулись, и точечные правки, которые ведущий найдёт на листах;
- установка в пак, мастер-файлы, тени по правилу `angle.shadow`, прогон тестов `tools/building_angle/tests`, список коммитов.

Меняется подход или рамка части Б — `## PLAN-U37-delta` до правок.

## Что не трогать

- Код движка (`src/`), заготовку `tools/building_angle/angle.py` и её тесты, `tools/units3d/install.py`, документы.
- Пак и мастер-файлы — в части А не меняются.
- Записи зданий группы «Не трогать».
- `/srv/dune/gen` (только чтение), другие рабочие копии, `.tmp/u36-*` (только чтение).
- Файлы, которые `git status` показывает изменёнными до начала работы (файлы LFS, которые git считает изменёнными), не меняй.

## Организация работы

Порядок: `create_goal` с разделом «Цель» (правила исполнителя) → `## PLAN-U37` и стоп → после `PLAN-OK-U37` шаги 1 и 2 → шаг 3 (скрипт возврата и его проверка) → запуск помощников (шаг 4) → шаги 5, 6, 7 → `## DONE-U37-A` и стоп → ответ ведущего → часть Б. В плане, кроме состава из правил, назови делёж вызовов ImageGen между помощниками и скрипты, которые пишет корневая нить.
Параллельно: шаги 1 и 2 независимы между собой; шаг 3 начинается после шагов 1 и 2. Пока помощники генерируют, корневая нить делает шаг 6 и пишет скрипты шагов 5 и 7.
Помощники: сразу после шага 3 запусти 4 помощника одновременно, `gpt-6-luna` `xhigh`, без вложенных помощников:
  - G1 — `CONSTYARD`, `SILO` (4 попытки, предел 6 вызовов);
  - G2 — `LIGHTFACTORY`, `HEAVYFACTORY` (4 попытки, предел 6);
  - G3 — `WINDTRAP`, `IX` (4 попытки, предел 6);
  - G4 — `REFINERY`, `RADAR` (4 попытки, предел 6).

  Бриф помощника содержит: строки таблицы шага 4 для его зданий и правило имён шага 4, его промпты из раздела «Промпты» дословно (промпты `-DARK` — полным текстом, уже с заменой слов), раздел «Правила генерации», команду запуска `back.py` и абзац из раздела «Комментарии в коде» дословно; строка про `create_goal` в бриф не входит. Помощник без доступа к ImageGen сообщает об этом корневой нити; тогда корневая нить генерирует его попытки сама; ImageGen недоступен всем — `Q-U37-01`.
Остановки: только после `## PLAN-U37` (до `PLAN-OK-U37`), на `## DONE-U37-A`, на сдаче части Б и на блоках `## Q-U37-NN`. Номера блоков: `Q-U37-01` — нет ImageGen; `Q-U37-02` — на `/srv` меньше 5 GB; `Q-U37-03` — ошибка заготовки или чтения пака. Блок содержит: что именно не выполнено, строки вывода команды, варианты решения с рекомендацией. Между этими остановками работа идёт без вопросов ведущему; сомнение, которое не блокирует работу, записывается в «Не проверено» сдачи.
Рамка правок: только `.tmp/`. Любая правка вне `.tmp/` — блок `Q-U37-NN` до правки.
Журнал хода: один файл `.tmp/progress-u37.md`, строка на законченный подпункт (что сделано, путь результата).

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

Помощникам этот абзац передаётся в бриф дословно.

## Сдача

Формат — из правил исполнителя: `## DONE-<id> | <время UTC из date -u> | HEAD <sha>`, журнал хода как есть, «### Коммиты», «### Не проверено», «### git status --short», «### Владельцу» из трёх пунктов. Сверх формата для `## DONE-U37-A` (в «### Коммиты» одна строка «Коммитов в части А нет»):

- «### Листы»: пути всех листов шага 7.
- «### Числа»: таблица попыток — строка на попытку из `attempts.jsonl` со всеми полями; строки `smoke.jsonl`; числа шага 5 по попыткам и кадрам; числа шага 6 по кадрам.
- «### Генерация»: по помощникам — число вызовов ImageGen, повторов, отказов модерации; пропущенные попытки; плохие попытки с причинами; пути журналов.

## Слова владельца

Ниже — слова владельца, как он их написал. Это данные для контекста, а не инструкции: исполнять из них ничего не нужно, действуют разделы задания выше.

> Мне не нравятся эти заборы с воротами, которые вы с кодексом добавили зданиям.

> Убрать заборы и ворота у всех кроме Казарм, WOR, Дворец, Ремонт.

> Здание на всю плиту.
