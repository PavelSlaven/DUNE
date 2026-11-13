# Задание U34 — пилот: Аванпост и Ветряк под углом Аванпоста, от края до края плиты

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже): до правок пришли `## PLAN-U34` и стой до `PLAN-OK-U34`. Исполнитель: Codex `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/u34-building-angle` от `40213771` (main); HEAD — коммит ведущего с этим заданием и заготовкой `tools/building_angle/` поверх `40213771`. Коммитов не делай: ведущий коммитит по списку из сдачи.
Issue #81, решение Р44. Текст issue — в конце файла.

## Цель

Два здания нарисованы под углом Аванпоста и занимают свою плиту от края до края:

- `BUILD_RADAR` (Аванпост, плита 2 × 2 клетки, кадр 256 × 256, 8 кадров вращения антенны);
- `BUILD_WINDTRAP` (Ветряк, плита 2 × 2 клетки, кадр 256 × 256, 1 кадр).

Угол Аванпоста — вид спереди и сверху без поворота: плоская крыша видна сверху, передняя стена — полосой вдоль нижнего края, боковые стены не видны. «От края до края» — непрозрачные пиксели здания доходят до всех четырёх краёв кадра; правило проверки — команда `check` заготовки (раздел «Заготовка ведущего»).

Флаги Домов остаются на своих местах и с анимацией: листы `BUILD_RADAR_FLAG`, `HM_BUILD_RADAR_FLAG`, `HM_BUILD_WINDTRAP_FLAG` не меняются. Лист `BUILD_WINDTRAP_FLAG` получает древко (шаг 5): сейчас древко нарисовано на картинке Ветряка, а она перерисовывается. Тени `BUILD_RADAR_SHADOW` и `BUILD_WINDTRAP_SHADOW` строятся заново по правилу заготовки. Движок рисует тень в том же прямоугольнике, что и здание, и до здания (`src/gameobjects/structures/cAbstractStructure.cpp`, строки 906–910), поэтому у здания во весь кадр тень закрыта зданием; это ожидаемо. Код движка не меняется.

Работа идёт в две части: часть А — растяжка Аванпоста, варианты Ветряка через ImageGen, древко, листы и числа для выбора ведущим; часть Б — установка выбранного варианта в пак и в мастер-файлы, новый тест и сдача.

## Заготовка ведущего

`tools/building_angle/angle.py` (тесты — `tools/building_angle/tests/test_angle.py`, 9 методов, зелёные на HEAD). Пропорции взяты с Аванпоста в паке: кадр 0 `BUILD_RADAR`, рамка непрозрачных пикселей x 23..232, y 12..247; передняя стена — нижние 27 % высоты, верхние углы срезаны на 5 %. Команды (запуск — `/srv/dune/venv/bin/python tools/building_angle/angle.py …`):

| Команда | Что делает |
|---|---|
| `guide WxH out.png` | направляющий кадр W × H: серый блок под углом Аванпоста во весь холст (крыша RGB 190, 190, 190; передняя стена 80, 80, 80; шов между ними 40, 40, 40; срезанные верхние углы — пурпурный 255, 0, 255) |
| `fit source.png NxM out.png` | убирает пурпурный фон (расстояние RGB до 255, 0, 255 не больше 60), оставляет самую большую связную область, обрезает по рамке непрозрачных пикселей и растягивает до кадра N·128 × M·128 сжатием Lanczos с премультипликацией |
| `stretch atlas.png NxM K out.png` | то же для атласа из K кадров, сложенных столбцом; одна рамка (объединение рамок кадров) на все кадры, чтобы анимация не сдвигалась |
| `shadow atlas.png NxM K out.png` | тень по правилу `build_shadow` из `tools/build_sega_imagegen_buildings.py`: альфа, размытие Гаусса 2,0, умножение на 0,22, цвет 5, 4, 3, сдвиг на 7, 7 |
| `check atlas.png NxM K` | для каждого кадра — доля покрытия каждого края: доля столбцов (для верхнего и нижнего края) или строк (для левого и правого), у которых в полосе 3 пикселя у края есть пиксель с альфой больше 127; печатает строку на кадр и итог `edge-to-edge: pass` или `FAIL`; код выхода 0 — у всех кадров все четыре доли не меньше 0,85 |

Заготовку не меняй. Ошибка в заготовке или её тестах — блок `## Q-U34-03` со строками вывода.

## Что есть

- Пак: `resources/bin/data/sdl_data_hd4.dat`, 241 запись. Чтение — `tools.hd_assets.read_pack` и `tools.hd_assets.decode_image` (как в `tools/units3d/tests/test_unit_contract.py`).
- Записи пака (ведущий измерил): `BUILD_RADAR` 256 × 2048 (8 кадров 256 × 256); `BUILD_RADAR_SHADOW` 256 × 2048; `BUILD_RADAR_FLAG` и `HM_BUILD_RADAR_FLAG` 256 × 2048; `BUILD_WINDTRAP` 256 × 256; `BUILD_WINDTRAP_SHADOW` 256 × 256; `BUILD_WINDTRAP_FLAG` и `HM_BUILD_WINDTRAP_FLAG` 256 × 2048 (8 кадров 256 × 256).
- Анимация Аванпоста: кадры 1–7 отличаются от кадра 0 только внутри прямоугольника x 134..209, y 22..97 (антенна).
- Флаги рисует движок поверх здания по прямоугольнику здания, 8 кадров по 125 мс: `src/drawers/cStructureDrawer.cpp`, строки 300–340 (`drawHdRadarFlag`) и 469–509 (`drawHdWindTrapFlag`). Цвет Дома флагу даёт лист `HM_*_FLAG`.
- Лист `BUILD_RADAR_FLAG` содержит и полотнище, и древко (рамка кадра 0 — x 8..71, y 148..242). Лист `BUILD_WINDTRAP_FLAG` содержит только полотнище: рамка непрозрачных пикселей в каждом из 8 кадров — x 172..213, y 117..143. Древко Ветряка нарисовано на самой картинке `BUILD_WINDTRAP`, под полотнищем. В `HM_BUILD_WINDTRAP_FLAG` нет пикселей с альфой больше 0 там, где у `BUILD_WINDTRAP_FLAG` альфа 0.
- Мастер-файлы: `resources/hd/master4/sdl_data/0026_BUILD_RADAR.png`, `0027_BUILD_RADAR_SHADOW.png`, `0040_BUILD_WINDTRAP.png`, `0041_BUILD_WINDTRAP_SHADOW.png` — попиксельно равны записям пака (ведущий сравнил: 0 отличающихся пикселей). `resources/hd/master4_extra_packs/sdl_data/BUILD_WINDTRAP_FLAG.png` — файл Git LFS; ведущий скачал его в рабочую копию до запуска.
- Установка в пак: `/srv/dune/venv/bin/python tools/units3d/install.py --atlases <папка> --pack resources/bin/data/sdl_data_hd4.dat` заменяет только записи, перечисленные в `<папка>/atlases.json`, остальные записи сохраняет байт в байт; размер новой картинки должен быть равен размеру старой. Формат `atlases.json`: `{"entries": {"<ИМЯ ЗАПИСИ>": {"file": "<имя PNG в папке>", "size": [<ширина>, <высота>]}}}`.
- Среда исполнителя: `/srv/dune/venv/bin/python` (Pillow, numpy, scipy, `unittest`; `cv2` и pytest нет). Сети нет, пакеты не скачиваются и не устанавливаются. Git LFS — `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.
- Диск: перед шагом 3 и перед шагом 9 выполни `df -h /srv`. Свободно меньше 5 GB — блок `## Q-U34-02` со строкой вывода и стоп.

## Часть А — Аванпост, варианты Ветряка, листы

1. **Аванпост.** Извлеки из пака `BUILD_RADAR` в `.tmp/u34-old/BUILD_RADAR.png`. Выполни `stretch .tmp/u34-old/BUILD_RADAR.png 2x2 8 .tmp/u34-out/BUILD_RADAR.png`, затем `check .tmp/u34-out/BUILD_RADAR.png 2x2 8` (ожидается `pass`) и `shadow .tmp/u34-out/BUILD_RADAR.png 2x2 8 .tmp/u34-out/BUILD_RADAR_SHADOW.png`. `check` дал `FAIL` — блок `## Q-U34-03` с выводом.
   - Сверка анимации: прямоугольник антенны x 134..209, y 22..97 пересчитай в координаты растянутого кадра по рамке, которую взяла `stretch`, и расширь на 4 пикселя с каждой стороны. Для каждого кадра k от 1 до 7 посчитай число пикселей вне этого прямоугольника, у которых хотя бы один канал RGBA отличается от кадра 0 больше чем на 8. Запиши числа в сдачу. Ожидается 0 в каждом кадре: одна рамка на все кадры и одинаковые пиксели вне антенны. Не ноль хотя бы в одном кадре — блок `## Q-U34-03` с числами.
2. **Сверка правила тени (справочно).** Выполни `shadow` на нынешних записях пака `BUILD_RADAR` (2x2, 8 кадров) и `BUILD_WINDTRAP` (2x2, 1 кадр) и сравни результат с записями `BUILD_RADAR_SHADOW` и `BUILD_WINDTRAP_SHADOW` пака: число пикселей, у которых хотя бы один канал RGBA отличается. Запиши числа в сдачу. Не ноль — строка в «Не проверено», работа продолжается.
3. **Входные картинки ImageGen.**
   - `.tmp/u34-in/windtrap_src.png`: запись `BUILD_WINDTRAP` пака, увеличенная до 1024 × 1024 сжатием Lanczos и наложенная по альфе на сплошной фон RGB (255, 0, 255); итог — RGB без альфы.
   - `.tmp/u34-in/guide_2x2.png`: `guide 1024x1024 .tmp/u34-in/guide_2x2.png`.
   - `.tmp/u34-in/outpost_example.png`: кадр 0 файла `.tmp/u34-out/BUILD_RADAR.png`, увеличенный до 1024 × 1024 сжатием Lanczos и наложенный по альфе на сплошной фон RGB (255, 0, 255); итог — RGB без альфы.
4. **Генерация Ветряка.** Два промпта из раздела «Промпты», по две попытки (a и b) — 4 вызова ImageGen. Попытки a и b — два независимых вызова с одним промптом и одними входными картинками.
   - Промпт W1: картинка 1 — `windtrap_src.png`, картинка 2 — `guide_2x2.png`. Результаты — `.tmp/u34-gen/windtrap_W1_a.png`, `.tmp/u34-gen/windtrap_W1_b.png`.
   - Промпт W2: картинка 1 — `windtrap_src.png`, картинка 2 — `guide_2x2.png`, картинка 3 — `outpost_example.png`. Результаты — `.tmp/u34-gen/windtrap_W2_a.png`, `.tmp/u34-gen/windtrap_W2_b.png`.
   - Каждый результат: `fit .tmp/u34-gen/windtrap_<P>_<x>.png 2x2 .tmp/u34-fit/BUILD_WINDTRAP_<P>_<x>.png`, затем `check .tmp/u34-fit/BUILD_WINDTRAP_<P>_<x>.png 2x2 1`.
   - Правила генерации — раздел «Правила генерации».
5. **Древко флага Ветряка.** Построй `.tmp/u34-out/BUILD_WINDTRAP_FLAG.png` из записи `BUILD_WINDTRAP_FLAG` пака (256 × 2048, 8 кадров). Координаты ниже — внутри кадра 256 × 256; в каждом из 8 кадров рисуй только в пиксели, у которых альфа записи `BUILD_WINDTRAP_FLAG` равна 0 (полотнище остаётся впереди древка и не меняется):
   - ствол: столбцы x = 208, 209, 210, 211, 212, 213; строки y от 112 до 183 включительно; цвет столбца — RGB пикселя (x, 175) записи `BUILD_WINDTRAP` пака на HEAD (ведущий прочитал: 35, 33, 37; 48, 47, 49; 25, 24, 26; 47, 46, 48; 36, 35, 35; 42, 42, 45), альфа 255;
   - навершие: строки y от 109 до 111, столбцы x от 207 до 214, цвет RGB (110, 108, 114), альфа 255;
   - основание: строки y от 180 до 183, столбцы x от 206 до 215, цвет RGB (30, 29, 32), альфа 255. Основание стоит на крыше: шов крыши и передней стены направляющей кадра 256 × 256 — строка y = 187.
   - Скрипт проверяет: пиксели, у которых альфа записи пака больше 0, равны пикселям пака байт в байт; все изменённые пиксели лежат в прямоугольнике x 206..215, y 109..183; в каждом кадре изменено одинаковое множество позиций или меньше (там, где полотнище перекрывает древко). Выведи число изменённых пикселей по кадрам.
6. **Листы.** Все листы — PNG в `.tmp/u34-sheets/`. Ячейка — кадр 256 × 256, увеличенный вдвое методом ближайшего соседа (512 × 512) и наложенный по альфе на фон RGB (70, 68, 64). Подписи — латиницей, в полосах вне кадров.
   - `choice.png`: строка 1 `old` — кадр 0 `BUILD_RADAR` пака с кадром 0 `BUILD_RADAR_FLAG` поверх; `BUILD_WINDTRAP` пака с кадром 0 `BUILD_WINDTRAP_FLAG` пака поверх. Строка 2 `new` — кадр 0 `.tmp/u34-out/BUILD_RADAR.png` с кадром 0 `BUILD_RADAR_FLAG` поверх; затем четыре ячейки `W1a`, `W1b`, `W2a`, `W2b` — `.tmp/u34-fit/BUILD_WINDTRAP_<P>_<x>.png` с кадром 0 `.tmp/u34-out/BUILD_WINDTRAP_FLAG.png` поверх. Флаги на листе — как в записях (без окраски цветом Дома).
   - `radar_frames.png`: одна строка, 8 кадров `.tmp/u34-out/BUILD_RADAR.png` с соответствующими кадрами `BUILD_RADAR_FLAG` поверх, подписи `f0` … `f7`.
   - `raw.png`: четыре сырых результата `.tmp/u34-gen/windtrap_<P>_<x>.png`, сжатые Lanczos до 512 × 512, подписи `W1a`, `W1b`, `W2a`, `W2b`.
7. **Числа.** Таблица на каждую из четырёх попыток: `check` (четыре доли и итог), рамка непрозрачных пикселей сырого результата до `fit` (x0, y0, x1, y1), коэффициенты растяжки `sx` = 256 / ширина рамки и `sy` = 256 / высота рамки, их отношение `max(sx, sy) / min(sx, sy)`, доля пурпурных пикселей сырого результата (расстояние RGB до 255, 0, 255 не больше 60). Та же строка для `old` Аванпоста, `new` Аванпоста и `old` Ветряка (у них `sx`, `sy` — по рамке записи пака).
8. **Сдача части А.** Пришли `## DONE-U34-A` по разделу «Сдача» и остановись. До ответа ведущего с выбором часть Б не начинай. Выбор ведущего — одна из попыток `W1a`, `W1b`, `W2a`, `W2b`. Исполнитель вид листов не оценивает и вариант не выбирает: выбирает ведущий. Все четыре попытки плохие или пропущены — `## DONE-U34-A` присылается так же, с листами и числами; что делать дальше, решает ведущий.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт W1:

> Edit image 1. Image 1 is a wind trap building from a real-time strategy game, drawn on a flat magenta background: three curved silver wind-catcher hoods with glowing blue vents and silver pipes on a grey concrete pad. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the wind trap as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put the three wind-catcher hoods with the blue vents and the silver pipes on the roof, seen from the same camera as the roof. Give the front wall a closed metal door, small vents and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт W2 (отличается от W1 добавленным предложением про картинку 3 перед словами «Redraw the wind trap»):

> Edit image 1. Image 1 is a wind trap building from a real-time strategy game, drawn on a flat magenta background: three curved silver wind-catcher hoods with glowing blue vents and silver pipes on a grey concrete pad. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Image 3 is another building of the same game already drawn from the target camera; use it only as an example of how the roof and the front wall look from this camera, and do not copy its shape, colours or details. Redraw the wind trap as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put the three wind-catcher hoods with the blue vents and the silver pipes on the roof, seen from the same camera as the roof. Give the front wall a closed metal door, small vents and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпты — новая формулировка этого задания; работают ли они, не проверено. Поэтому вид оценивает ведущий по листам.

## Правила генерации (для корневой нити и для каждого помощника)

1. Один вызов ImageGen — один результат. Входные картинки вызова — ровно те, что названы в шаге 4 для его промпта, в том же порядке.
2. Сразу после вызова скопируй выходной файл из `$CODEX_HOME/generated_images` в `.tmp/u34-gen/` байт в байт под именем из шага 4: без изменения размера и без пересжатия. Выходной файл бери по пути, который вернул вызов ImageGen, а не по времени изменения. В журнал `.tmp/u34-gen/log-G<n>.tsv` (`<n>` — номер помощника, корневая нить пишет `log-G0.tsv`, если работает сама) добавь строку из полей через табуляцию: время UTC, слово `copied`, имя результата, путь источника, sha256 результата.
3. Плохая попытка — выполнено хотя бы одно: картинка не квадратная; `check` после `fit` дал `FAIL`; отношение `max(sx, sy) / min(sx, sy)` из шага 7 больше 1,15; доля пурпурных пикселей сырого результата больше 0,10.
4. Плохая попытка — один повтор. Заменённую картинку перенеси в `.tmp/u34-gen-first/` с тем же именем; результат повтора получает основное имя. Повтор тоже плохой — оставь его под основным именем, в журнал запиши строку `bad` с причиной и иди дальше.
5. Отказ модерации — один повтор. Второй отказ — попытка пропущена: в журнал строка `skipped` с первыми 200 символами текста отказа; на листах ячейка попытки — заливка RGB (128, 0, 0).
6. Общий предел — 8 вызовов ImageGen, повторы включены. Предел достигнут — генерация останавливается, дальше идёт то, что есть; в сдаче — число вызовов и что осталось без результата.
7. ImageGen недоступен ни корневой нити, ни помощникам, или не принимает две или три входные картинки — блок `## Q-U34-01` и стоп.

## Часть Б — установка, тест (только после ответа ведущего с выбором)

9. **Файлы выбора.** Скопируй выбранный `.tmp/u34-fit/BUILD_WINDTRAP_<P>_<x>.png` байт в байт в `.tmp/u34-out/BUILD_WINDTRAP.png`. Выполни `shadow .tmp/u34-out/BUILD_WINDTRAP.png 2x2 1 .tmp/u34-out/BUILD_WINDTRAP_SHADOW.png`.
10. **Установка в пак.**
    - Скопируй пак `resources/bin/data/sdl_data_hd4.dat` в `.tmp/u34-pack/pack-before.dat`, затем `pack-before.dat` в `.tmp/u34-pack-before-dir/sdl_data_hd4.dat` (для красного прогона теста).
    - Создай `.tmp/u34-install/`: файлы `BUILD_RADAR.png`, `BUILD_RADAR_SHADOW.png`, `BUILD_WINDTRAP.png`, `BUILD_WINDTRAP_SHADOW.png`, `BUILD_WINDTRAP_FLAG.png` из `.tmp/u34-out/` и `atlases.json` с пятью записями этих имён (`file` — имя файла, `size` — его размер).
    - Выполни `/srv/dune/venv/bin/python tools/units3d/install.py --atlases .tmp/u34-install --pack resources/bin/data/sdl_data_hd4.dat`.
    - Скрипт проверки сравнивает `pack-before.dat` и новый пак через `read_pack`: одинаковое число записей и одинаковый порядок имён; ровно пять названных записей отличаются по содержимому, остальные побайтно равны (в том числе `BUILD_RADAR_FLAG`, `HM_BUILD_RADAR_FLAG`, `HM_BUILD_WINDTRAP_FLAG`); пиксели пяти новых записей после `decode_image` равны пикселям файлов `.tmp/u34-install/`. Выведи строки результата. Проверка не прошла — блок `## Q-U34-03` и стоп.
11. **Мастер-файлы.** Сначала сравни попиксельно `resources/hd/master4_extra_packs/sdl_data/BUILD_WINDTRAP_FLAG.png` с записью `BUILD_WINDTRAP_FLAG` файла `pack-before.dat`. Затем скопируй байт в байт: `.tmp/u34-out/BUILD_RADAR.png` → `resources/hd/master4/sdl_data/0026_BUILD_RADAR.png`; `BUILD_RADAR_SHADOW.png` → `0027_BUILD_RADAR_SHADOW.png`; `BUILD_WINDTRAP.png` → `0040_BUILD_WINDTRAP.png`; `BUILD_WINDTRAP_SHADOW.png` → `0041_BUILD_WINDTRAP_SHADOW.png`; `BUILD_WINDTRAP_FLAG.png` → `resources/hd/master4_extra_packs/sdl_data/BUILD_WINDTRAP_FLAG.png` (последнее — только если сравнение выше дало 0 отличающихся пикселей; иначе этот мастер не трогай и запиши число отличий в «Не проверено»). Файлы `HV_*`, `HM_HV_*`, `HOUSEMASK_*` этих зданий в `master4_extra_packs` не трогай.
12. **Новый тест.** Создай `tools/building_angle/tests/test_pilot_pack.py`.
    - Импорты, путь к паку и условие пропуска — как в `tools/building_angle/tests/test_angle.py`: `sys.path.insert` для `tools` и `tools/building_angle`, затем `import angle` и `from hd_assets import decode_image, read_pack`; путь к паку — `D2TM_PACK_DIR` или `resources/bin/data`; класс помечен `@unittest.skipUnless` тем же условием, что `OutpostPackTests` (файл пака есть и больше 1 000 000 байт). Тест — `unittest.TestCase`, в конце файла `if __name__ == "__main__": unittest.main()`.
    - Три метода: `BUILD_RADAR` (2x2, 8 кадров) проходит `angle.check`; `BUILD_WINDTRAP` (2x2, 1 кадр) проходит `angle.check`; у `BUILD_WINDTRAP_FLAG` в каждом из 8 кадров все пиксели столбцов x 208..213 в строках y 150..178 имеют альфу 255.
    - Прогони тест дважды и приведи строки вывода: с `D2TM_PACK_DIR=$PWD/.tmp/u34-pack-before-dir` (ожидается красный: падают все три метода) и с `D2TM_PACK_DIR=$PWD/resources/bin/data` (ожидается зелёный).
13. **Прогон наборов тестов.** До шага 10 на HEAD и после шага 12 на изменённой рабочей копии: `tools/building_angle/tests` и `tools/units3d/tests`, `/srv/dune/venv/bin/python -m unittest`, каждый метод отдельным процессом, `xargs -P 16`, `D2TM_PACK_DIR=$PWD/resources/bin/data`; логи — в `.tmp/u34-tests/head/` и `.tmp/u34-tests/after/`. Тест, который падает и на HEAD, назови в сдаче, не чини. Тест, который падает только после правки, назови со строками вывода; тест не меняй. Ожидаемо после правки пропускается (`skipped`) метод `test_current_outpost_leaves_margins` в `test_angle.py`: он проверяет старый пак.
14. **Список коммитов для сдачи.** Два коммита по порядку, сообщения на английском, последняя строка каждого — `Behavior changes: …`:
    1. файл `resources/bin/data/sdl_data_hd4.dat` и мастер-файлы шага 11; последняя строка перечисляет видимое изменение: Аванпост и Ветряк нарисованы под углом Аванпоста и занимают плиту от края до края, флаг Ветряка на прежнем месте, с анимацией и собственным древком;
    2. файл `tools/building_angle/tests/test_pilot_pack.py`; последняя строка `Behavior changes: none`.

## Что не трогать

- Код движка (`src/`), заготовку `tools/building_angle/angle.py` и `tools/building_angle/tests/test_angle.py`, `tools/units3d/install.py`, документы.
- Записи пака, кроме пяти названных в шаге 10.
- Мастер-файлы, кроме названных в шаге 11.
- `/srv/dune/gen` (только чтение).
- В коммиты шага 14 входят только файлы, названные в шаге 14. Другие файлы, которые `git status` показывает изменёнными или новыми (например, `tools/units3d/data/sdl_data_hd4_source.dat`, файлы LFS после загрузки ведущим, `.tmp/`), в коммиты не включай и не меняй.

## Организация работы

- **Порядок.** `create_goal` с разделом «Цель» (правила исполнителя) → `## PLAN-U34` и стоп → после `PLAN-OK-U34` шаги 1, 2, 3 → шаг 4 (генерация) → шаги 5, 6, 7 → `## DONE-U34-A` и стоп → ответ ведущего с выбором → шаги 9–14 → `## DONE-U34`. В плане, кроме состава из правил, назови: делёж вызовов ImageGen между помощниками и скрипты, которые пишет корневая нить.
- **Параллельно.** Шаги 1 и 2 независимы; шаг 3 начинается после шага 1 (картинка `outpost_example.png` берётся из результата шага 1). Пока помощники генерируют (шаг 4), корневая нить делает шаг 5, пишет скрипты листов и чисел (шаги 6, 7) и выполняет прогон наборов тестов на HEAD (шаг 13).
- **Помощники.** Сразу после шага 3 запускай 2 помощника одновременно, `gpt-6-luna` `xhigh`, без вложенных помощников. Делёж: G1 — промпт W1, попытки a и b; G2 — промпт W2, попытки a и b. Бриф помощника содержит: шаг 4 для его промпта, его промпт из раздела «Промпты» дословно, раздел «Правила генерации» и абзац из раздела «Комментарии в коде» дословно; строка про `create_goal` в бриф не входит. Помощник без доступа к ImageGen сообщает об этом корневой нити; тогда корневая нить генерирует его попытки сама; ImageGen недоступен всем — `Q-U34-01`.
- **Остановки.** Только после `## PLAN-U34` (до `PLAN-OK-U34`), на `## DONE-U34-A`, на `## DONE-U34` и на блоках `## Q-U34-NN`. Номера блоков: `Q-U34-01` — нет ImageGen или он не принимает две или три входные картинки; `Q-U34-02` — на `/srv` меньше 5 GB; `Q-U34-03` — ошибка заготовки, `check` дал `FAIL` на растянутом Аванпосте, сверка анимации шага 1 дала не ноль, или не прошла проверка установки шага 10. Блок содержит: что именно не выполнено, строки вывода команды, варианты решения с рекомендацией. Между этими остановками работа идёт без вопросов ведущему; сомнение, которое не блокирует работу, записывается в «Не проверено» сдачи.
- **Рамка правок.** Только пять записей пака из шага 10; мастер-файлы из шага 11; новый файл `tools/building_angle/tests/test_pilot_pack.py`; `.tmp/`. Любая другая правка вне `.tmp/` — блок `Q-U34-NN` до правки.
- **Журнал хода.** Один файл `.tmp/progress-u34.md`: строка на законченный подпункт (что сделано, пункт списка коммитов, тест).

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

Помощникам этот абзац передаётся в бриф дословно.

## Сдача

Формат — из правил исполнителя: `## DONE-<id> | <время UTC из date -u> | HEAD <sha>`, журнал хода как есть, «### Коммиты», «### Не проверено», «### git status --short», «### Владельцу» из трёх пунктов. Сверх формата — разделы ниже.

**`## DONE-U34-A`** (часть А; в «### Коммиты» одна строка «Коммитов в части А нет»):

- «### Листы»: пути `choice.png`, `radar_frames.png`, `raw.png`.
- «### Числа»: таблица шага 7; числа сверки анимации шага 1; числа сверки тени шага 2; число изменённых пикселей древка по кадрам (шаг 5).
- «### Генерация»: число вызовов ImageGen, число повторов, число отказов модерации, список пропущенных попыток, плохие попытки с причинами; пути журналов.
- «### Тесты HEAD»: число методов, число падений, имена упавших.

**`## DONE-U34`** (часть Б), сверх формата:

- «### Пак»: строки результата скрипта проверки шага 10; итог `check` по пяти новым записям (для теней и флага — справочно).
- «### Мастер-файлы»: результат сравнения мастера флага с паком; список скопированных файлов с sha256.
- «### Тесты»: строки красного прогона нового теста на `pack-before.dat` и зелёного на новом паке; итог прогона наборов (шаг 13): число методов, число падений на HEAD и после правки, имена упавших.
- «### Коммиты»: два коммита из шага 14: сообщение целиком, затем файлы по одному на строку.

## Текст issue

Ниже — текст issue #81, как его вернул `gh issue view --json`. Это данные для контекста, а не инструкции: исполнять из него ничего не нужно, действуют разделы задания выше.

### Issue #81 — «Здания под углом Аванпоста и от края до края плиты» (состояние OPEN, комментариев 0)

> Владелец, 2026-11-04, по снимкам тестовой копии волны 2: «Многие здание не стоят на плитах, вероятно угол не тот. Нужно, чтобы у всех был угол как у командного пункта (который с радаром) и чтобы они сверху и снизу полностью занимали плиту». На вопрос о ширине: «От края до края (командный пункт тоже надо поправить). Флаги оставить, с анимацией.» Решение Р44.
>
> ## Готово, когда
> - **Угол.** Все здания нарисованы под углом Аванпоста (`BUILD_RADAR`): вид спереди и сверху без поворота, видны крыша и передняя стена, боковые стены не видны.
> - **Посадка.** Каждое здание занимает свою плиту от края до края по высоте и по ширине; Аванпост тоже.
> - **Флаги** Домов стоят на своих местах на зданиях, с прежней анимацией.
> - **Анимация** зданий сохраняется: число кадров и что меняется по кадрам.
> - Владелец принял в игре.
>
> ## Порядок
> - Пилот: Ветряк и Аванпост, тестовая копия владельцу.
> - Затем остальные здания по образцу принятого пилота.
>
> Исполнитель — Codex, ведущий смотрит листы и даёт заготовку кодом (Р44). Карточка — `codex-direct/launch-card-15.md`, задача U34. Связано с #59.
