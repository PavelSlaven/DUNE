# Задание U36 — раскатка угла Аванпоста на остальные здания и перерисовка заводов (часть А)

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже): до правок пришли `## PLAN-U36` и стой до `PLAN-OK-U36`. Исполнитель: Codex `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/u34-building-angle`, HEAD `ba8c17d0` (равен `main`; пилот U34 и его правки слиты). Коммитов не делай: ведущий коммитит по списку из сдачи.
Issue #81 (угол зданий) и #82 (стиль заводов), решение Р44. Тексты issue — в конце файла.

## Цель

Пилот U34 принят владельцем: Аванпост и Ветряк нарисованы под углом Аванпоста и занимают плиту от края до края. Это задание готовит то же для остальных зданий. Часть А — заготовки и листы, по которым ведущий выбирает варианты, а владелец решает судьбу анимированных зданий. Пак и мастер-файлы в части А не меняются.

Угол Аванпоста — вид спереди и сверху без поворота: плоская крыша видна сверху, передняя стена — полосой вдоль нижнего края, боковые стены не видны. «От края до края» — правило команды `check` заготовки.

| Группа | Записи пака | Что делается в части А |
|---|---|---|
| Перерисовка | `BUILD_BARRACKS`, `BUILD_CONSTYARD`, `BUILD_IX`, `BUILD_PALACE`, `BUILD_SILO`, `BUILD_WOR`, `BUILD_LIGHTFACTORY`, кадр 0 `BUILD_HEAVYFACTORY` | варианты ImageGen по старой картинке и серому бруску-ориентиру, как Ветряк пилота |
| Проба растяжки | `BUILD_REFINERY`, `BUILD_REPAIR`, `BUILD_STARPORT`, `BUILD_HIGHTECH`, `BUILD_HEAVYFACTORY` (все кадры) | растяжка всех кадров на плиту, как Аванпост пилота, вместе с листами флагов, масками и накладками |
| Турели | `BUILD_TURRET`, `BUILD_RTURRET` | форма остаётся; исправляются недочёты 24–27 (раздел «Турели») |

Лёгкий и тяжёлый заводы (#82) перерисовываются в стиле остальных зданий: светлый металл, светло-серые панели, голубые огни; без тёмного вида и без золотых манипуляторов.

## Заготовка ведущего

`tools/building_angle/angle.py` (тесты — `tools/building_angle/tests/test_angle.py` и `test_pilot_pack.py`, зелёные на HEAD). Запуск — `/srv/dune/venv/bin/python tools/building_angle/angle.py …`; в своих скриптах импортируй модуль (`sys.path.insert(0, "tools/building_angle")`, `import angle`) и вызывай его функции.

| Команда | Функция | Что делает |
|---|---|---|
| `guide WxH out.png` | `angle.guide((W, H))` | направляющий кадр W × H: серый брусок под углом Аванпоста во весь холст (крыша RGB 190, 190, 190; передняя стена 80, 80, 80 — нижние 27 % высоты; шов 40, 40, 40; срезанные верхние углы — пурпурный 255, 0, 255) |
| `fit source.png NxM out.png` | `angle.fit(image, (N, M))` | убирает пурпурный фон (расстояние RGB до 255, 0, 255 не больше 60, альфа не больше 127), оставляет самую большую связную область, обрезает по рамке непрозрачных пикселей и растягивает до N·128 × M·128 сжатием Lanczos с премультипликацией |
| `stretch atlas.png NxM K out.png` | `angle.stretch(atlas, (N, M), K)` | то же для атласа из K кадров столбцом; одна рамка — объединение рамок непрозрачных пикселей всех кадров |
| `shadow atlas.png NxM K out.png` | `angle.shadow(atlas, (N, M), K)` | тень: альфа, размытие Гаусса 2,0, умножение на 0,22, цвет 5, 4, 3, сдвиг на 7, 7 |
| `check atlas.png NxM K` | `angle.check(atlas, (N, M), K)` | для каждого кадра — доли покрытия краёв в полосе 3 пикселя (альфа больше 127) и касание всех четырёх краёв; итог `pass`, если у всех кадров все четыре доли не меньше 0,85 и касание есть; код выхода 0 при `pass` |

Вспомогательные функции: `angle.opaque_box(frame)` — рамка пикселей с альфой больше 127 (как `PIL.Image.getbbox`: x0, y0, x1, y1, правая и нижняя границы не включены); `angle.resize_premultiplied(image, (w, h))` — сжатие Lanczos с премультипликацией.

Заготовку и её тесты не меняй. Ошибка в заготовке — блок `## Q-U36-03` со строками вывода.

## Что есть

- Пак: `resources/bin/data/sdl_data_hd4.dat`, 241 запись. Чтение — `tools.hd_assets.read_pack` и `tools.hd_assets.decode_image` (как в `tools/building_angle/tests/test_pilot_pack.py`).
- Записи пака (ведущий измерил на HEAD; кадры сложены столбцом):

| Здание | Плита | Кадр | Кадров | Связанные записи |
|---|---|---|---|---|
| `BUILD_BARRACKS` | 2x2 | 256 × 256 | 1 | `BUILD_BARRACKS_SHADOW`; `BUILD_BARRACKS_FLAG`, `HM_BUILD_BARRACKS_FLAG` (8 кадров, два флага с древками в листе) |
| `BUILD_CONSTYARD` | 2x2 | 256 × 256 | 1 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров, только полотнище) |
| `BUILD_IX` | 2x2 | 256 × 256 | 1 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров, только полотнище) |
| `BUILD_LIGHTFACTORY` | 2x2 | 256 × 256 | 1 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров, только полотнище); накладки `BUILD_LIGHTFACTORY_PRODUCTION` (256 × 2048, 8 кадров, кольцо в рамке x 52..62, y 53..63) и `BUILD_LIGHTFACTORY_FLASH` (256 × 256, та же рамка) |
| `BUILD_PALACE` | 3x3 | 384 × 384 | 1 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (384 × 3072, 8 кадров; в листе полотнище и три мигающих красных огня шпилей, огни без маски Дома) |
| `BUILD_SILO` | 2x2 | 256 × 256 | 1 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров, только полотнище) |
| `BUILD_WOR` | 2x2 | 256 × 256 | 1 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (8 кадров, флаг с древком в листе) |
| `BUILD_HEAVYFACTORY` | 3x2 | 384 × 256 | 11 | `_SHADOW` (11 кадров); накладка `BUILD_HEAVYFACTORY_FLASH` (384 × 256, 1 кадр, рамка x 154..164, y 147..155); флага нет |
| `BUILD_REFINERY` | 3x2 | 384 × 256 | 8 | `_SHADOW`; маска Дома здания `HM_BUILD_REFINERY` (8 кадров); `_FLAG`, `HM_…_FLAG` (8 кадров) |
| `BUILD_REPAIR` | 3x2 | 384 × 256 | 8 | `_SHADOW`; флага нет |
| `BUILD_STARPORT` | 3x3 | 384 × 384 | 8 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (384 × 3072, 8 кадров; в листе есть и два купола здания) |
| `BUILD_HIGHTECH` | 3x2 | 384 × 256 | 7 | `_SHADOW`; `_FLAG`, `HM_…_FLAG` (384 × 2048, 8 кадров) |
| `BUILD_TURRET`, `BUILD_RTURRET` | 1x1 | 128 × 128 | 8 | `_SHADOW` (8 кадров); флагов нет |

- Анимация Тяжёлого завода: кадры 1–10 отличаются от кадра 0 только в рамке x 283..311, y 86..153 — в сборочном отсеке между двумя рельсами снизу вверх собирается машина.
- Движок рисует тень в том же прямоугольнике, что и здание, и до здания; флаги и накладки — поверх здания в том же прямоугольнике; флаг — 8 кадров по 125 мс; цвет Дома флагу даёт лист `HM_*_FLAG`. Код движка не меняется.
- Номер кадра турели: кадр 0 — восток (E), 1 — северо-восток (NE), 2 — север (N), 3 — северо-запад (NW), 4 — запад (W), 5 — юго-запад (SW), 6 — юг (S), 7 — юго-восток (SE).
- Мастер-файлы: `resources/hd/master4/sdl_data/<NNNN>_<ЗАПИСЬ>.png` (`<NNNN>` — номер записи в паке, например `0001_BUILD_BARRACKS.png`) и `resources/hd/master4_extra_packs/sdl_data/<ЗАПИСЬ>.png` для флагов, масок Дома и `BUILD_LIGHTFACTORY_PRODUCTION`. Ведущий скачал файлы LFS флагов и масок в рабочую копию до запуска. В части А мастер-файлы не меняются.
- Среда: `/srv/dune/venv/bin/python` (Pillow, numpy, scipy, `unittest`; `cv2` и pytest нет). Сети нет, пакеты не скачиваются и не устанавливаются. Git LFS — `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.
- Диск: перед шагом 3 выполни `df -h /srv`. Свободно меньше 5 GB — блок `## Q-U36-02` со строкой вывода и стоп.

## Часть А

1. **Старые записи.** Извлеки из пака на HEAD в `.tmp/u36-old/<ЗАПИСЬ>.png` (RGBA, без изменений) все записи из таблицы «Записи пака»: здания, тени, флаги, маски `HM_*`, накладки.

2. **Проба растяжки.** Для каждого здания из группы «Проба растяжки» (`REFINERY` 3x2 8 кадров, `REPAIR` 3x2 8, `STARPORT` 3x3 8, `HIGHTECH` 3x2 7, `HEAVYFACTORY` 3x2 11):
   - `stretch .tmp/u36-old/BUILD_<B>.png <плита> <кадров> .tmp/u36-stretch/BUILD_<B>.png`; затем `check` по результату и `shadow` в `.tmp/u36-stretch/BUILD_<B>_SHADOW.png`. `check` с итогом `FAIL` работу не останавливает: строки вывода идут в сдачу.
   - Рамка растяжки `box` — та, что взяла `stretch`: объединение `angle.opaque_box` всех кадров `BUILD_<B>`. Связанные записи растягиваются той же рамкой: каждый кадр — `angle.resize_premultiplied(кадр.crop(box), размер кадра)`, кадры складываются столбцом в прежнем порядке. Связанные записи: `BUILD_REFINERY_FLAG`, `HM_BUILD_REFINERY_FLAG`, `HM_BUILD_REFINERY`, `BUILD_STARPORT_FLAG`, `HM_BUILD_STARPORT_FLAG`, `BUILD_HIGHTECH_FLAG`, `HM_BUILD_HIGHTECH_FLAG`, `BUILD_HEAVYFACTORY_FLASH`. Результаты — `.tmp/u36-stretch/<ЗАПИСЬ>.png`, размер равен размеру записи пака.
   - Сверка анимации: область анимации здания — объединение рамок пикселей, у которых в старом кадре k (k от 1 до последнего) хотя бы один канал RGBA отличается от старого кадра 0 больше чем на 8. Пересчитай её в координаты растянутого кадра по `box` (x' = (x − x0) · W / (x1 − x0), y' = (y − y0) · H / (y1 − y0), W × H — размер кадра) и расширь на 4 пикселя с каждой стороны. Для каждого растянутого кадра k посчитай пиксели вне этой области, у которых хотя бы один канал отличается от растянутого кадра 0 больше чем на 8. Ожидается 0; не ноль — число в сдачу и строка в «Не проверено», работа продолжается.
   - Слой машины Тяжёлого завода (для части Б): `.tmp/u36-out/HEAVYFACTORY_VEHICLE.png`, 384 × 2816, 11 кадров. Кадр k — пиксели старого кадра k, у которых хотя бы один канал RGBA отличается от старого кадра 0 больше чем на 8; остальные пиксели — RGBA (0, 0, 0, 0). Кадр 0 — пустой.

3. **Входные картинки ImageGen** (`.tmp/u36-in/`, все — RGB без альфы):
   - `<b>_src.png` для каждого здания группы «Перерисовка» (`<b>` — имя записи без `BUILD_` строчными: `barracks`, `constyard`, `ix`, `palace`, `silo`, `wor`, `lightfactory`, `heavyfactory`): кадр 0 записи пака, наложенный по альфе на сплошной фон RGB (255, 0, 255). Плиты 2x2 и 3x3 — увеличение до 1024 × 1024 сжатием Lanczos. Плита 3x2 (`heavyfactory`) — увеличение до 1536 × 1024 сжатием Lanczos и вставка в холст 1536 × 1536 цвета (255, 0, 255) в точку (0, 256).
   - `guide_square.png`: `guide 1024x1024`.
   - `guide_3x2.png`: `angle.guide((1536, 1024))`, вставленный в холст 1536 × 1536 цвета (255, 0, 255) в точку (0, 256).
   - `style_example.png`: кадр 0 записи `BUILD_WINDTRAP` пака на HEAD (Ветряк пилота), наложенный по альфе на фон RGB (255, 0, 255) и увеличенный до 1024 × 1024 сжатием Lanczos.
   - Доля пурпурного каждого ориентира (`guide_square.png`, `guide_3x2.png`): доля пикселей с расстоянием RGB до (255, 0, 255) не больше 60. Числа — в сдачу и в скрипт шага 4.

4. **Скрипт попытки.** До запуска помощников корневая нить пишет `.tmp/u36-tools/attempt.py`: вход — сырой результат ImageGen, плита (`2x2`, `3x3` или `3x2`), путь ориентира этого здания, путь выхода без расширения `<stem>`. Скрипт:
   - выполняет `angle.fit` и сохраняет `<stem>.fit.png`;
   - очищает пурпурную кайму (правило ниже) и сохраняет `<stem>.png`;
   - выполняет `angle.check(<stem>.png, плита, 1)`;
   - считает рамку непрозрачных пикселей сырого результата до `fit` (та, по которой `fit` обрезает, — после ключа пурпурного), `sx` = ширина кадра / ширина рамки, `sy` = высота кадра / высота рамки, отношение `max(sx, sy) / min(sx, sy)`, долю пурпурного сырого результата (расстояние RGB до 255, 0, 255 не больше 60) и разность этой доли и доли пурпурного ориентира;
   - печатает одну строку JSON с этими числами, числом пикселей каймы до и после очистки и полем `verdict`: `bad` с перечнем причин по правилу 3 раздела «Правила генерации» или `good`.

   **Очистка пурпурной каймы** (и в шаге 6 для турелей). Пиксель каймы — альфа больше 0, R − G > 50, B − G > 50 и |R − B| < 90. Для каждого пикселя каймы соседи — пиксели окна 5 × 5 с центром в нём, у которых альфа больше 127 и которые сами не пиксели каймы. Есть хотя бы один сосед — RGB пикселя заменяется средним RGB соседей (с округлением), альфа не меняется; соседей нет — альфа становится 0. Один проход по копии исходной картинки: соседи берутся из исходной картинки.

5. **Генерация.** Промпты — раздел «Промпты». Две попытки (`a`, `b`) — два независимых вызова ImageGen с одним промптом и одними входными картинками.

   | Здание | Промпты | Картинки вызова по порядку | Ориентир для `attempt.py` | Плита |
   |---|---|---|---|---|
   | `barracks`, `constyard`, `ix`, `palace`, `silo`, `wor` | свой промпт здания | 1 — `<b>_src.png`, 2 — `guide_square.png` | `guide_square.png` | 2x2 (`palace` — 3x3) |
   | `lightfactory` | `LIGHTFACTORY-S1`; `LIGHTFACTORY-S2` | S1: 1 — `lightfactory_src.png`, 2 — `guide_square.png`; S2: те же и 3 — `style_example.png` | `guide_square.png` | 2x2 |
   | `heavyfactory` | `HEAVYFACTORY-S1`; `HEAVYFACTORY-S2` | S1: 1 — `heavyfactory_src.png`, 2 — `guide_3x2.png`; S2: те же и 3 — `style_example.png` | `guide_3x2.png` | 3x2 |

   - Имена: сырой результат — `.tmp/u36-gen/<B>_<t>.png`, где `<B>` — имя записи без `BUILD_` прописными, `<t>` — `a` или `b` для шести зданий и `S1a`, `S1b`, `S2a`, `S2b` для заводов. Сразу после копирования — `attempt.py .tmp/u36-gen/<B>_<t>.png <плита> <ориентир> .tmp/u36-fit/<B>_<t>`; строку JSON добавь в `.tmp/u36-fit/attempts.jsonl`.
   - Всего 20 попыток: 6 зданий × 2 и 2 завода × 4.

6. **Турели.** Раздел «Турели»: исправленные атласы `.tmp/u36-out/BUILD_TURRET.png` и `.tmp/u36-out/BUILD_RTURRET.png` (128 × 1024, 8 кадров), тени `shadow` в `.tmp/u36-out/BUILD_TURRET_SHADOW.png` и `.tmp/u36-out/BUILD_RTURRET_SHADOW.png`, числа проверок.

7. **Листы.** Все листы — PNG в `.tmp/u36-sheets/`. Ячейка — кадр, наложенный по альфе на фон RGB (70, 68, 64). Подписи — латиницей, в полосах вне кадров.
   - `choice-<B>.png` для каждого здания группы «Перерисовка»: увеличение вдвое методом ближайшего соседа; первая ячейка `old` — кадр 0 старой записи `BUILD_<B>` с кадром 0 старого `BUILD_<B>_FLAG` поверх (у Тяжёлого завода флага нет); затем ячейки попыток `.tmp/u36-fit/<B>_<t>.png` без флагов, подписи `<t>`. Пропущенная попытка — ячейка с заливкой RGB (128, 0, 0).
   - `raw.png`: все сырые результаты `.tmp/u36-gen/*.png`, сжатые Lanczos до 384 × 384, по 6 в строке, подписи `<B>_<t>`.
   - `stretch-<B>.png` для каждого здания пробы растяжки: два блока одного размера — `old` (кадры `.tmp/u36-old/BUILD_<B>.png`) и `new` (кадры `.tmp/u36-stretch/BUILD_<B>.png`); в ячейке кадра k — кадр здания и, у зданий с флагом, кадр k mod 8 листа флага того же блока поверх; масштаб 1:1, по 4 кадра в строке, подписи `f0` … `fN`.
   - `turrets.png`: четыре строки — `TURRET old`, `TURRET new`, `RTURRET old`, `RTURRET new`; в строке 8 кадров, увеличенных вдвое методом ближайшего соседа; подписи `f0 E`, `f1 NE`, `f2 N`, `f3 NW`, `f4 W`, `f5 SW`, `f6 S`, `f7 SE`.

8. **Числа** (в сдачу):
   - таблица попыток: строка на попытку из `attempts.jsonl` (четыре доли `check`, касание, итог, рамка, `sx`, `sy`, отношение, доля пурпурного, разность с ориентиром, кайма до и после, `verdict`);
   - таблица растяжки: строка на здание — `box`, `sx` = W / (x1 − x0), `sy` = H / (y1 − y0), итог `check`, наименьшая из четырёх долей по кадрам, число пикселей каймы (правило шага 4, без очистки) в растянутом атласе; числа сверки анимации по кадрам;
   - числа раздела «Турели»;
   - доли пурпурного ориентиров (шаг 3).

9. **Прогон наборов тестов на HEAD.** `tools/building_angle/tests` и `tools/units3d/tests`, `/srv/dune/venv/bin/python -m unittest`, каждый метод отдельным процессом, `xargs -P 16`, `D2TM_PACK_DIR=$PWD/resources/bin/data`; логи — в `.tmp/u36-tests/head/`. Число методов, число падений, имена упавших — в сдачу. Падения не чини.

10. **Сдача части А.** Пришли `## DONE-U36-A` по разделу «Сдача» и остановись. Исполнитель вид листов не оценивает и варианты не выбирает: выбирает ведущий, о судьбе анимированных зданий решает владелец. Плохие и пропущенные попытки не мешают сдаче: листы и числа присылаются как есть.

## Турели

Форма турелей остаётся. Исправляются четыре недочёта из обзора ведущего (текст обзора — дословно):

- 24, `BUILD_TURRET`: «Основание турели между направлениями прыгает на 1 px: в кадрах 1, 2, 3, 6 плита сдвинута влево (в кадре 6 ещё и вниз, передний край на 1 px толще), голова в кадрах 1, 2, 6, 7 — влево на 1 px, в кадре 3 — на 2 px. При повороте ствола плита и голова дрожат. Правка: Совместить плиту и голову во всех 8 кадрах с кадром 0 (одна общая плита, голова в одном месте).»
- 25, `BUILD_RTURRET`: «Кадр 1 (направление NE) нарисован вдоль оси NW–SE: контейнеры лежат «\», как в кадрах 3 (NW) и 7 (SE), а не «/», как в противоположном кадре 5 (SW). При наведении на северо-восток установка смотрит на северо-запад или юго-восток и при повороте N→NE→E переворачивается на 90°.»
- 26, `BUILD_RTURRET`: «Кадры 0 (E) и 4 (W) — не одна установка, развёрнутая на 180°. Ось с огнями стоит в обоих на x≈63, но в E контейнеры длиной ≈83 px (x 18–101) сдвинуты назад, а в W ≈73 px (x 15–88) выдвинуты вперёд, и сзади торчит корпус до x≈101. При повороте установка прыгает и меняет длину.»
- 27, `BUILD_RTURRET`: «По краям контейнеров в кадре 0 непрозрачные пурпурные пиксели (около 47 шт., до 218,27,221): столбик x=17, y 81–92, низ y=102, правые торцы x 98–102. Это остаток ключевого цвета.»

Что должно получиться:

- **Т4 (недочёт 27), первым.** Во всех кадрах обеих турелей очищена пурпурная кайма по правилу шага 4. Дальнейшие шаги и проверки берут очищенные кадры; «старый кадр» ниже — кадр до очистки.
- **Т1 (недочёт 24).** У `BUILD_TURRET` одна плита во всех 8 кадрах — плита кадра 0, и голова (восьмигранный купол) в каждом кадре стоит там же, где в кадре 0; ствол каждого кадра — свой. Кадр 0 меняется только очисткой каймы.
- **Т2 (недочёт 25).** Голова кадра 1 `BUILD_RTURRET` — голова кадра 3, отражённая по горизонтали (x → 127 − x), поверх плиты кадра 0.
- **Т3 (недочёт 26).** Голова кадра 4 `BUILD_RTURRET` — голова кадра 0, отражённая по горизонтали (x → 127 − x), поверх плиты кадра 0.
- Остальные кадры `BUILD_RTURRET` (0, 2, 3, 5, 6, 7) меняются только очисткой каймы.

Способ отделить голову от плиты и совместить кадры предложи в PLAN: правило маски головы, правило сдвига, чем заполняются пиксели плиты, которые в кадре 0 закрывает голова, а новая голова не закрывает. Поканальная медиана кадров как плита `BUILD_TURRET` не годится: по обзору четыре кадра из восьми сдвинуты.

Проверки (скриптом, числа в сдачу):

- `BUILD_TURRET`, для каждого нового кадра k от 1 до 7: число пикселей вне объединения масок головы нового кадра k и нового кадра 0, у которых хотя бы один канал RGBA отличается от нового кадра 0 больше чем на 8; ожидается 0;
- `BUILD_TURRET`, для каждого k от 1 до 7: целочисленный сдвиг (dx, dy) в пределах −3..3, при котором окно 48 × 48 с углом (40, 40) нового кадра k меньше всего отличается от того же окна нового кадра 0 (сумма модулей разности RGB); ожидается (0, 0); то же для старых кадров — для сравнения;
- `BUILD_RTURRET`, кадры 1 и 4: число пикселей вне объединения масок головы нового кадра и кадра 0, отличающихся от кадра 0 больше чем на 8 в каком-либо канале; ожидается 0. Число пикселей внутри маски новой головы, отличающихся от отражённого кадра-источника (кадр 3 для кадра 1, кадр 0 для кадра 4) больше чем на 8 в каком-либо канале; ожидается 0;
- число пикселей каймы в каждом кадре обеих турелей до и после очистки; после ожидается 0;
- кадр 0 `BUILD_TURRET` и кадры 0, 2, 3, 5, 6, 7 `BUILD_RTURRET`: число пикселей, отличающихся от старого кадра, и число очищенных пикселей каймы этого кадра; ожидаются равные числа.

Проверка не сходится с выбранным способом — блок `## Q-U36-04` с числами и вариантами.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт BARRACKS:

> Edit image 1. Image 1 is an infantry barracks from a real-time strategy game, drawn on a flat magenta background: three beige concrete blocks with low parapet walls, short grey cylindrical tanks on the roofs, rows of small dark windows, grey pipes and a stair entrance. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the barracks as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put two short grey cylindrical tanks, a few roof vents and grey pipes that run into the tanks or into the roof on the roof, seen from the same camera as the roof. Give the front wall a closed entrance door at ground level, a row of small dark windows and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт CONSTYARD:

> Edit image 1. Image 1 is a construction yard from a real-time strategy game, drawn on a flat magenta background: two large round dark-grey storage tanks, beige and orange machinery blocks, a grey steel frame of pipes and a small crane. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the construction yard as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put the two large round storage tanks, the beige and orange machinery blocks and the small crane, joined by the grey steel pipe frame, on the roof, seen from the same camera as the roof. Give the front wall a wide closed vehicle gate, small vents and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт IX:

> Edit image 1. Image 1 is a research centre from a real-time strategy game, drawn on a flat magenta background: three large blue glass domes with silver forked antennas on a dark-grey pad, with four white pyramid lights at the corners. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the research centre as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put the three blue glass domes with the silver forked antennas and four small white pyramid lights on the roof, seen from the same camera as the roof. Give the front wall a closed metal door, small glowing blue lights and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт PALACE:

> Edit image 1. Image 1 is a palace from a real-time strategy game, drawn on a flat magenta background: a large golden dome and four smaller golden domes on round white towers, thin black spires with small red lights on the dome tops, a curved white wall and a dark double door. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the palace as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put the large golden dome and the four smaller golden domes, each with a thin black spire and a small red light at its tip, on the roof, seen from the same camera as the roof. Give the front wall the dark double door, a row of small windows and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт SILO:

> Edit image 1. Image 1 is a spice silo from a real-time strategy game, drawn on a flat magenta background: two large round grey storage tanks with ladders on a concrete pad with a steel railing. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the spice silo as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put the two large round storage tanks with their ladders, joined by a pipe, on the roof, seen from the same camera as the roof. Give the front wall a closed hatch, small vents and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт WOR:

> Edit image 1. Image 1 is a heavy infantry training building from a real-time strategy game, drawn on a flat magenta background: golden-brown metal walls, two glass capsule pods and a round beige dome. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the training building as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put the two glass capsule pods and the round beige dome on the roof, seen from the same camera as the roof. Give the front wall a closed metal door, three small lit niches and panel seams. Keep the materials, colours, lighting and the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт LIGHTFACTORY-S1:

> Edit image 1. Image 1 is a light vehicle factory from a real-time strategy game, drawn on a flat magenta background: a dark-grey metal block with machinery, a round hatch near the top left corner, a short chimney, gold robot arms and an entrance ramp. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the light factory as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put a round hatch with a light rim near the top left corner, a short chimney, machinery blocks and pipes on the roof, seen from the same camera as the roof. Give the front wall a wide closed vehicle gate, small vents and panel seams. Do not keep the dark colours of image 1: draw the building in the style of the other buildings of the game, with light silver metal, light-grey panels and small glowing blue lights, with no dark or black surfaces and no gold or yellow robot arms. Keep the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт LIGHTFACTORY-S2 (отличается от S1 предложением про картинку 3 перед словами «Redraw the light factory» и предложением о цвете перед словами «Keep the painted»):

> Edit image 1. Image 1 is a light vehicle factory from a real-time strategy game, drawn on a flat magenta background: a dark-grey metal block with machinery, a round hatch near the top left corner, a short chimney, gold robot arms and an entrance ramp. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Image 3 is another building of the same game drawn in the target style; use it only as an example of the materials and colours, and do not copy its shape or details. Redraw the light factory as one solid building with exactly the outline, camera angle and faces of image 2: the building fills the whole canvas from the left edge to the right edge and from the top edge to the bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, and no side walls are visible. Put a round hatch with a light rim near the top left corner, a short chimney, machinery blocks and pipes on the roof, seen from the same camera as the roof. Give the front wall a wide closed vehicle gate, small vents and panel seams. Do not keep the dark colours of image 1: use the materials and colours of image 3, with light silver metal, light-grey panels and small glowing blue lights, with no dark or black surfaces and no gold or yellow robot arms. Keep the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 only in the two small cut corners at the top, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт HEAVYFACTORY-S1:

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, drawn on a flat magenta background: a dark-grey metal hall with a machinery block, a round fan, a red octagonal hatch, an assembly bay with two crane rails and gold robot arms, and conveyor lines along the bottom. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Redraw the heavy factory as one solid building with exactly the outline, camera angle and faces of the grey block of image 2: the building fills the grey block from its left edge to its right edge and from its top edge to its bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, no side walls are visible, and nothing is drawn in the magenta bands above and below the block. Put these parts on the roof, seen from the same camera as the roof: a large open assembly bay in the right half, which is an empty octagonal pit between two parallel crane rails with nothing inside the pit; a red octagonal hatch in the middle; a machinery block with a round fan and pipes in the left half. Give the front wall a wide closed vehicle gate, small vents and panel seams. Do not keep the dark colours of image 1: draw the building in the style of the other buildings of the game, with light silver metal, light-grey panels and small glowing blue lights, with no dark or black surfaces and no gold or yellow robot arms. Keep the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 in the bands above and below the block and in the two small cut corners at the top of the block, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт HEAVYFACTORY-S2 (отличается от S1 предложением про картинку 3 перед словами «Redraw the heavy factory» и предложением о цвете перед словами «Keep the painted»):

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, drawn on a flat magenta background: a dark-grey metal hall with a machinery block, a round fan, a red octagonal hatch, an assembly bay with two crane rails and gold robot arms, and conveyor lines along the bottom. Image 2 is a shape and camera guide: a plain grey block seen from the target camera, orthographic, looking down at its roof and at its front wall; the light-grey area is the flat roof, the dark-grey band along the bottom is the front wall that faces the viewer; the side walls are not visible from this camera. Image 3 is another building of the same game drawn in the target style; use it only as an example of the materials and colours, and do not copy its shape or details. Redraw the heavy factory as one solid building with exactly the outline, camera angle and faces of the grey block of image 2: the building fills the grey block from its left edge to its right edge and from its top edge to its bottom edge, its flat roof covers the light-grey area, its front wall covers the dark-grey band, no side walls are visible, and nothing is drawn in the magenta bands above and below the block. Put these parts on the roof, seen from the same camera as the roof: a large open assembly bay in the right half, which is an empty octagonal pit between two parallel crane rails with nothing inside the pit; a red octagonal hatch in the middle; a machinery block with a round fan and pipes in the left half. Give the front wall a wide closed vehicle gate, small vents and panel seams. Do not keep the dark colours of image 1: use the materials and colours of image 3, with light silver metal, light-grey panels and small glowing blue lights, with no dark or black surfaces and no gold or yellow robot arms. Keep the painted game-sprite look of image 1. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Use image 2 only for the outline, camera angle and faces, not for colours or materials. Show no ground, no concrete pad and no sand around the building. Keep flat pure magenta RGB 255,0,255 in the bands above and below the block and in the two small cut corners at the top of the block, as in image 2. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпты, кроме общей части пилота, — новая формулировка этого задания; работают ли они, не проверено. Поэтому вид оценивает ведущий по листам.

## Правила генерации (для корневой нити и для каждого помощника)

1. Один вызов ImageGen — один результат. Входные картинки вызова — ровно те, что названы в шаге 5 для его промпта, в том же порядке.
2. Сразу после вызова скопируй выходной файл из `$CODEX_HOME/generated_images` в `.tmp/u36-gen/` байт в байт под именем из шага 5: без изменения размера и без пересжатия. Выходной файл бери по пути, который вернул вызов ImageGen, а не по времени изменения. В журнал `.tmp/u36-gen/log-G<n>.tsv` (`<n>` — номер помощника; корневая нить, если генерирует сама, пишет `log-G0.tsv`) добавь строку из полей через табуляцию: время UTC, слово `copied`, имя результата, путь источника, sha256 результата. Затем выполни `attempt.py` (шаг 5).
3. Плохая попытка — выполнено хотя бы одно: `check` дал `FAIL`; отношение `max(sx, sy) / min(sx, sy)` больше 1,15; доля пурпурного сырого результата больше доли пурпурного ориентира этого здания на 0,10 или больше.
4. Плохая попытка — один повтор. Заменённые файлы (сырой результат и выходы `attempt.py`) перенеси в `.tmp/u36-gen-first/` с теми же именами; результат повтора получает основное имя. Повтор тоже плохой — оставь его под основным именем, в журнал запиши строку `bad` с причинами и иди дальше.
5. Отказ модерации — один повтор. Второй отказ — попытка пропущена: в журнал строка `skipped` с первыми 200 символами текста отказа.
6. Предел вызовов ImageGen, повторы включены: G1 — 9, G2 — 9, G3 — 5, G4 — 5 (всего 28). Предел достигнут — генерация помощника останавливается; в сдаче — число вызовов и что осталось без результата.
7. ImageGen недоступен ни корневой нити, ни помощникам, или не принимает две или три входные картинки — блок `## Q-U36-01` и стоп.

## Часть Б (только после ответа ведущего)

Часть Б выполняется по ответу ведущего на `## DONE-U36-A`; ответ — источник истины для неё. Ожидаемый состав, чтобы план части А его учитывал:

- выбранные попытки по зданиям и решение владельца по каждому зданию пробы растяжки;
- места флагов на новых картинках: сдвиг листа флага, древко там, где лист флага содержит только полотнище (как древко Ветряка в пилоте), места красных огней Дворца;
- сдвиг накладок `BUILD_LIGHTFACTORY_PRODUCTION` и `BUILD_LIGHTFACTORY_FLASH` на новую крышку, `BUILD_HEAVYFACTORY_FLASH` на новый люк; место слоя машины `HEAVYFACTORY_VEHICLE.png` в новом сборочном отсеке;
- точечные правки, которые ведущий найдёт на листах;
- установка через `tools/units3d/install.py`, мастер-файлы, тени по правилу `shadow`, новый тест пака, прогон наборов после правки, список коммитов.

Меняется подход или рамка части Б — `## PLAN-U36-delta` до правок.

## Что не трогать

- Код движка (`src/`), заготовку `tools/building_angle/angle.py` и её тесты, `tools/units3d/install.py`, документы.
- Пак и мастер-файлы — в части А не меняются.
- `/srv/dune/gen` (только чтение), другие рабочие копии.
- В часть А входят только файлы в `.tmp/`. Файлы, которые `git status` показывает изменёнными до начала работы (файлы LFS, которые git считает изменёнными), не меняй.

## Организация работы

- **Порядок.** `create_goal` с разделом «Цель» (правила исполнителя) → `## PLAN-U36` и стоп → после `PLAN-OK-U36` шаги 1 и 3 → шаг 4 (скрипт попытки) → запуск помощников (шаг 5) → шаги 7, 8 → `## DONE-U36-A` и стоп → ответ ведущего → часть Б. В плане, кроме состава из правил, назови: делёж вызовов ImageGen между помощниками, скрипты, которые пишет корневая нить, и способ раздела «Турели».
- **Параллельно.** Шаги 1 и 3 независимы между собой; шаг 4 начинается после шага 3. Пока помощники генерируют, корневая нить делает шаги 2, 6 и 9 и пишет скрипты листов и чисел (шаги 7, 8).
- **Помощники.** Сразу после шага 4 запусти 4 помощника одновременно, `gpt-6-luna` `xhigh`, без вложенных помощников:
  - G1 — `BARRACKS`, `CONSTYARD`, `IX` (6 попыток, предел 9 вызовов);
  - G2 — `PALACE`, `SILO`, `WOR` (6 попыток, предел 9);
  - G3 — `LIGHTFACTORY` S1a, S1b, S2a, S2b (предел 5);
  - G4 — `HEAVYFACTORY` S1a, S1b, S2a, S2b (предел 5).

  Бриф помощника содержит: строки таблицы шага 5 для его зданий и правило имён шага 5, его промпты из раздела «Промпты» дословно, раздел «Правила генерации», команду запуска `attempt.py` и абзац из раздела «Комментарии в коде» дословно; строка про `create_goal` в бриф не входит. Помощник без доступа к ImageGen сообщает об этом корневой нити; тогда корневая нить генерирует его попытки сама; ImageGen недоступен всем — `Q-U36-01`.
- **Остановки.** Только после `## PLAN-U36` (до `PLAN-OK-U36`), на `## DONE-U36-A`, на сдаче части Б и на блоках `## Q-U36-NN`. Номера блоков: `Q-U36-01` — нет ImageGen или он не принимает две или три входные картинки; `Q-U36-02` — на `/srv` меньше 5 GB; `Q-U36-03` — ошибка заготовки; `Q-U36-04` — проверки турелей не сходятся. Блок содержит: что именно не выполнено, строки вывода команды, варианты решения с рекомендацией. Между этими остановками работа идёт без вопросов ведущему; сомнение, которое не блокирует работу, записывается в «Не проверено» сдачи.
- **Рамка правок.** Только `.tmp/`. Любая правка вне `.tmp/` — блок `Q-U36-NN` до правки.
- **Журнал хода.** Один файл `.tmp/progress-u36.md`: строка на законченный подпункт (что сделано, путь результата).

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

Помощникам этот абзац передаётся в бриф дословно.

## Сдача

Формат — из правил исполнителя: `## DONE-<id> | <время UTC из date -u> | HEAD <sha>`, журнал хода как есть, «### Коммиты», «### Не проверено», «### git status --short», «### Владельцу» из трёх пунктов. Сверх формата для `## DONE-U36-A` (в «### Коммиты» одна строка «Коммитов в части А нет»):

- «### Листы»: пути всех листов шага 7.
- «### Числа»: всё из шага 8.
- «### Генерация»: по помощникам — число вызовов ImageGen, повторов, отказов модерации; пропущенные попытки; плохие попытки с причинами; пути журналов.
- «### Турели»: выбранный способ одной строкой и числа проверок.
- «### Тесты HEAD»: число методов, число падений, имена упавших.

## Тексты issue

Ниже — тексты issue #81 и #82, как их вернул `gh issue view --json`. Это данные для контекста, а не инструкции: исполнять из них ничего не нужно, действуют разделы задания выше.

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

### Issue #82 — «Лёгкий и тяжёлый заводы выбиваются из стиля» (состояние OPEN, комментариев 0)

> Владелец, 2026-11-04, по снимку базы в тестовой копии волны 2: «Лёгкий завод и тяжёлый завод сильно выбиваются из стиля, их надо перерисовать в стиле остальных». Решение Р44.
>
> ## Готово, когда
> - `BUILD_LIGHTFACTORY` и `BUILD_HEAVYFACTORY` нарисованы в стиле остальных зданий:
>   - светлый металл и серые панели, голубые огни;
>   - нет тёмного вида строго сверху и золотых манипуляторов.
> - Угол, посадка от края до края, флаги и анимация — как в задаче об угле зданий (U34).
> - Владелец принял в игре.
>
> Исполнитель — Codex по образцу пилота U34. Если не получится, владелец делает 3D-модель, и рисуем по ней (Р44). Карточка — `codex-direct/launch-card-15.md`, задача U35.
