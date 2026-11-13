# Задание U39-A — площадки Лёгкого и Тяжёлого заводов (картинки)

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже): до правок пришли `## PLAN-U39A` и стой до `PLAN-OK-U39A`. Исполнитель: Codex `gpt-6-luna` `xhigh`, малый аккаунт.
Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/u39-factory-pad`, HEAD `c483e220` (равен `main`: здания U37 слиты). Коммитов не делай: ведущий коммитит по списку из сдачи.
Issue нет; источник — решения владельца Р49 и Р53 (в конце файла их слова).

## Цель

В правой части Лёгкого и Тяжёлого заводов появляется площадка, как у Переработки. Готовый юнит появляется на площадке (поднимается через люк) и съезжает с неё вниз; это движок сделает отдельной задачей. Эта задача — только картинки заводов:

- **Лёгкий завод** (`BUILD_LIGHTFACTORY`, плита 2x2, кадр 256 × 256): вертикальная линия посередине делит плиту на две равные половины. В левой половине — здание завода из его нынешних частей, в правой — пустая площадка от верхнего до нижнего края плиты.
- **Тяжёлый завод** (`BUILD_HEAVYFACTORY`, плита 3x2, кадр 384 × 256): правая треть (столбцы пикселей 256–383) — пустая площадка от верхнего до нижнего края плиты вместо сборочного отсека с рельсами; левые две трети не меняются. Все 11 кадров атласа — один и тот же кадр с пустой площадкой: анимации сборки машины в отсеке больше нет.

Обе площадки — в духе площадки Переработки: ровная светло-серая металлическая плита с тонким кантом, тёмный восьмиугольный люк со светлым крестом в центре площадки, несколько тёмных щелей вокруг люка. На площадке ничего не стоит; между площадкой и нижним краем плиты ничего нет.

Плита по-прежнему закрыта целиком (Р47): крыша и площадка доходят до всех четырёх краёв, альфа 255 во всех пикселях. Части здания — одна–три крупные простые части с чистыми поверхностями и узкими ровными проходами (Р51); каждая часть стоит так, как могла бы стоять на деле (Р52); поднятые части отбрасывают на крышу мягкую тень вниз и вправо (Р48).

Часть А — попытки ImageGen и листы, по которым ведущий выбирает варианты. Пак и мастер-файлы в части А не меняются.

## Что есть

- Пак: `resources/bin/data/sdl_data_hd4.dat`, 241 запись. Чтение — `tools.hd_assets.read_pack(Path)` и `tools.hd_assets.decode_image` (как в `tools/building_angle/tests/test_pilot_pack.py`).
- Заготовка `tools/building_angle/angle.py`: в своих скриптах `sys.path.insert(0, "tools/building_angle")`, `import angle`. Нужны функции `angle.check(atlas, (N, M), K)` и `angle.shadow`. Заготовку и её тесты не меняй.
- Скрипт возврата прошлой задачи: `.tmp/u37-tools/back.py` (группа «Забор и ворота»: RGB из результата ImageGen, альфа старого кадра 0, очистка пурпурной каймы, `angle.check`, поле `diff`).
- Записи пака (ведущий измерил на HEAD; кадры сложены столбцом; рамка — `x0, y0, x1, y1` пикселей с альфой больше 20 в кадре 0):

| Запись | Кадр | Кадров | Рамка в кадре 0 | Что это |
|---|---|---|---|---|
| `BUILD_LIGHTFACTORY` | 256 × 256 | 1 | весь кадр | здание |
| `BUILD_LIGHTFACTORY_SHADOW` | 256 × 256 | 1 | — | тень |
| `BUILD_LIGHTFACTORY_FLAG`, `HM_BUILD_LIGHTFACTORY_FLAG` | 256 × 256 | 8 | 142, 11, 187, 38 | полотнище флага; висит на мачте здания у правого верхнего угла (столбец около 189) |
| `BUILD_LIGHTFACTORY_FLASH` | 256 × 256 | 1 | 38, 40, 60, 65 | огонь при выпуске юнита |
| `BUILD_LIGHTFACTORY_PRODUCTION` | 256 × 256 | 8 | 41, 7, 70, 63 | мигающий огонь при выпуске юнита |
| `BUILD_HEAVYFACTORY` | 384 × 256 | 11 | весь кадр | здание; в кадрах 1–10 в отсеке справа поднимается машина |
| `BUILD_HEAVYFACTORY_SHADOW` | 384 × 256 | 11 | — | тень |
| `BUILD_HEAVYFACTORY_FLASH` | 384 × 256 | 1 | 106, 57, 230, 144 | свечение красного восьмиугольного люка в средней трети |
| `BUILD_REFINERY` | 384 × 256 | 8 | весь кадр | образец площадки: правая часть кадра 0 |

- Движок рисует тень в том же прямоугольнике, что и здание, и до здания; флаги и накладки — поверх здания в том же прямоугольнике. Код движка в этой задаче не меняется.
- Среда: `/srv/dune/venv/bin/python` (Pillow, numpy, scipy, `unittest`; `cv2` и pytest нет). Сети нет, пакеты не устанавливаются. Git LFS — `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.
- Диск: перед шагом 2 выполни `df -h /srv`. Свободно меньше 5 GB — блок `## Q-U39A-02` со строкой вывода и стоп.

## Часть А

1. **Старые записи.** Извлеки из пака на HEAD в `.tmp/u39-old/<ЗАПИСЬ>.png` (RGBA, без изменений) все записи из таблицы «Записи пака».

2. **Входные картинки ImageGen** (`.tmp/u39-in/`, RGB без альфы):
   - `lightfactory_src.png` — кадр 0 `BUILD_LIGHTFACTORY`, наложенный по альфе на сплошной фон RGB (255, 0, 255) и увеличенный до 1024 × 1024 сжатием Lanczos.
   - `heavyfactory_src.png` — кадр 0 `BUILD_HEAVYFACTORY`, наложенный по альфе на фон RGB (255, 0, 255), увеличенный до 1536 × 1024 сжатием Lanczos и вставленный в холст 1536 × 1536 цвета (255, 0, 255) в точку (0, 256).
   - `pad_ref.png` — вырезка (200, 0, 384, 210) кадра 0 `BUILD_REFINERY`, наложенная по альфе на фон RGB (255, 0, 255), увеличенная вчетверо (736 × 840) сжатием Lanczos и вставленная в центр холста 1024 × 1024 цвета (255, 0, 255), в точку (144, 92).

3. **Скрипт возврата.** До запуска помощников корневая нить копирует `.tmp/u37-tools/back.py` в `.tmp/u39-tools/back.py` и правит копию так:
   - старые записи читаются из `.tmp/u39-old/`;
   - здания `LIGHTFACTORY` и `HEAVYFACTORY` обрабатываются по правилам группы «Забор и ворота»; другие имена — выход с кодом 2;
   - в строку JSON добавляется поле `pink` — число пикселей выхода с альфой больше 0, R − G > 25, B − G > 25 и |R − B| < 90;
   - поле `verdict` — `bad` с перечнем причин по правилу 3 раздела «Правила генерации», иначе `good`.

   **Проверка скрипта.** Прогони `back.py` на `lightfactory_src.png` и `heavyfactory_src.png` как на сыром результате (`tag` — `smoke`, выход — `.tmp/u39-fit/<B>_smoke.png`). Строки JSON — в `.tmp/u39-fit/smoke.jsonl` и в сдачу.

4. **Генерация.** Промпты — раздел «Промпты».

   | Здание | Попытки | Промпт | Картинки вызова |
   |---|---|---|---|
   | `LIGHTFACTORY` | `a`, `b`, `c` — три независимых вызова | `LIGHTFACTORY-PAD` | 1 — `lightfactory_src.png`, 2 — `pad_ref.png` |
   | `HEAVYFACTORY` | `a`, `b`, `c` — три независимых вызова | `HEAVYFACTORY-PAD` | 1 — `heavyfactory_src.png`, 2 — `pad_ref.png` |

   - Имена: сырой результат — `.tmp/u39-gen/<B>_<t>.png` (`<t>` — `a`, `b` или `c`). Сразу после копирования — `back.py .tmp/u39-gen/<B>_<t>.png <B> .tmp/u39-fit/<B>_<t>.png`; строку JSON добавь в `.tmp/u39-fit/attempts.jsonl`.
   - Всего 6 попыток: 2 здания × 3.

5. **Кадры Тяжёлого завода.** Для каждой попытки `HEAVYFACTORY_<t>` собери `.tmp/u39-fit/HEAVYFACTORY_<t>.frames.png` (384 × 2816): 11 одинаковых кадров, каждый — `.tmp/u39-fit/HEAVYFACTORY_<t>.png`.

6. **Листы.** PNG в `.tmp/u39-sheets/`. Ячейка — кадр, наложенный по альфе на фон RGB (70, 68, 64), увеличенный вдвое методом ближайшего соседа. Подписи — латиницей, в полосах вне кадров. Пропущенная попытка — ячейка с заливкой RGB (128, 0, 0).
   - `choice-LIGHTFACTORY.png`: ячейка `old` — кадр 0 старой записи, затем ячейки `a`, `b`, `c`. Поверх каждой ячейки — кадр 0 старых `BUILD_LIGHTFACTORY_FLAG`, `BUILD_LIGHTFACTORY_PRODUCTION` и `BUILD_LIGHTFACTORY_FLASH`. Вторая строка — те же ячейки без накладок.
   - `choice-HEAVYFACTORY.png`: ячейка `old` — кадр 0 старой записи, затем ячейки `a`, `b`, `c`; поверх каждой — кадр 0 старого `BUILD_HEAVYFACTORY_FLASH`. Вторая строка — те же ячейки без накладки.
   - `pair.png`: строка на попытку; в строке без зазора слева направо — кадр 0 `BUILD_REFINERY`, ячейка попытки Тяжёлого завода `<t>`, ячейка попытки Лёгкого завода `<t>`; все без накладок, с увеличением вдвое.
   - `raw.png`: все сырые результаты `.tmp/u39-gen/*.png`, сжатые Lanczos до 384 × 384, по 3 в строке, подписи `<B>_<t>`.

7. **Сдача части А.** Пришли `## DONE-U39A-A` по разделу «Сдача» и остановись. Исполнитель вид листов не оценивает и варианты не выбирает: выбирает ведущий. Плохие и пропущенные попытки не мешают сдаче.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт LIGHTFACTORY-PAD:

> Edit image 1. Image 1 is a light vehicle factory from a real-time strategy game, seen from the game camera: orthographic, looking straight down at the flat light-grey metal roof, which fills the whole square image up to all four edges. Image 2 shows, on a flat magenta background, the vehicle landing pad of a spice refinery from the same game. Rebuild the factory inside the same square so that a vertical line through the middle divides it into two halves of equal width. Left half: the factory building, made from the parts of image 1 at the same scale, the dark-grey machinery block with the round hatch, the short chimney, the thin antenna mast at its top right corner and the pipes, arranged as one or two large simple parts with clean surfaces, few details and narrow straight gaps between them. Right half: one empty landing pad in the style of image 2, reaching the top edge, the right edge, the bottom edge and the middle line: a flat light-grey metal plate with a thin raised rim, a dark octagonal lift hatch with a light cross in the centre of the pad and a few dark slots around the hatch. Nothing stands on the pad, and nothing lies between the pad and the bottom edge of the image. Keep the colours, the small glowing blue lights, the light direction and the camera angle of image 1; raised parts cast soft dark shadows down and to the right onto the roof. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. The roof and the pad fill the whole image up to all four edges; show no ground, no sand and no magenta anywhere. Do not add anything else: no flag, no text, letters, numbers, logos or watermarks.

Промпт HEAVYFACTORY-PAD:

> Edit image 1. Image 1 is a heavy vehicle factory from a real-time strategy game, drawn as a wide block between flat magenta bands above and below it and seen from the game camera: orthographic, looking straight down at the flat light-grey metal roof, which fills the whole block up to all four edges. The block is three equal parts wide. Image 2 shows, on a flat magenta background, the vehicle landing pad of a spice refinery from the same game. Change only the right third of the block, which now holds an assembly bay between two crane rails. Replace the whole right third, from the top edge to the bottom edge of the block, with one empty landing pad in the style of image 2: a flat light-grey metal plate with a thin raised rim, a dark octagonal lift hatch with a light cross in the centre of the pad and a few dark slots around the hatch. Nothing stands on the pad, and nothing lies between the pad and the bottom edge of the block; the pale panel at the bottom right of the block ends at the left edge of the pad. Keep the left two thirds of the block exactly as in image 1: the machinery block with the round fan and the pipes on the left, the red octagonal hatch in the middle, the pale panels at the bottom, the colours, the small glowing blue lights, the light direction and the camera angle; raised parts cast soft dark shadows down and to the right onto the roof. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. Show no ground and no sand anywhere. Keep the flat pure magenta RGB 255,0,255 of image 1 where it is, including the bands above and below the block. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпты — новая формулировка этого задания; работают ли они, не проверено. Поэтому вид оценивает ведущий по листам.

## Правила генерации (для корневой нити и для каждого помощника)

1. Один вызов ImageGen — один результат. Входные картинки вызова — ровно те, что названы в шаге 4 для его промпта, в том же порядке.
2. Сразу после вызова скопируй выходной файл из `$CODEX_HOME/generated_images` в `.tmp/u39-gen/` байт в байт под именем из шага 4: без изменения размера и без пересжатия. Выходной файл бери по пути, который вернул вызов ImageGen, а не по времени изменения. В журнал `.tmp/u39-gen/log-G<n>.tsv` (`<n>` — номер помощника; корневая нить, если генерирует сама, пишет `log-G0.tsv`) добавь строку из полей через табуляцию: время UTC, слово `copied`, имя результата, путь источника, sha256 результата. Затем выполни `back.py` (шаг 4).
3. Плохая попытка — выполнено хотя бы одно: `square` ложно; `magenta` больше 0,02; итог `angle.check` — `FAIL`.
4. Плохая попытка — один повтор. Заменённые файлы (сырой результат и выход `back.py`) перенеси в `.tmp/u39-gen-first/` с теми же именами; результат повтора получает основное имя. Повтор тоже плохой — оставь его под основным именем, в журнал запиши строку `bad` с причинами и иди дальше.
5. Отказ модерации — один повтор. Второй отказ — попытка пропущена: в журнал строка `skipped` с первыми 200 символами текста отказа.
6. Предел вызовов ImageGen, повторы включены: 5 на помощника, всего 10. Предел достигнут — генерация помощника останавливается; в сдаче — число вызовов и что осталось без результата.
7. ImageGen недоступен ни корневой нити, ни помощникам — блок `## Q-U39A-01` и стоп.

## Часть Б (только после ответа ведущего)

Часть Б выполняется по ответу ведущего на `## DONE-U39A-A`; ответ — источник истины для неё. Ожидаемый состав, чтобы план части А его учитывал:

- выбранные попытки по зданиям и точечные правки, которые ведущий найдёт на листах;
- сдвиг полотнища флага Лёгкого завода (`BUILD_LIGHTFACTORY_FLAG` и `HM_BUILD_LIGHTFACTORY_FLAG`, все 8 кадров) к мачте на новой картинке и сдвиги огней (`_FLASH`, `_PRODUCTION`), если части под ними сдвинулись, — целыми пикселями, по числам из ответа;
- установка в пак: `BUILD_LIGHTFACTORY`, `BUILD_HEAVYFACTORY` (11 одинаковых кадров), тени `BUILD_LIGHTFACTORY_SHADOW` и `BUILD_HEAVYFACTORY_SHADOW` по правилу `angle.shadow`, сдвинутые накладки; мастер-файлы; прогон тестов `tools/building_angle/tests`; список коммитов.

Меняется подход или рамка части Б — `## PLAN-U39A-delta` до правок.

## Что не трогать

- Код движка (`src/`), заготовку `tools/building_angle/angle.py` и её тесты, `tools/units3d/install.py`, документы.
- Пак и мастер-файлы — в части А не меняются.
- Записи всех зданий, кроме Лёгкого и Тяжёлого заводов.
- `/srv/dune/gen` (только чтение), другие рабочие копии, `.tmp/u36-*` и `.tmp/u37-*` (только чтение).
- Файлы, которые `git status` показывает изменёнными до начала работы (файлы LFS, которые git считает изменёнными), не меняй.

## Организация работы

Порядок: `create_goal` с разделом «Цель» (правила исполнителя) → `## PLAN-U39A` и стоп → после `PLAN-OK-U39A` шаги 1 и 2 → шаг 3 (скрипт возврата и его проверка) → запуск помощников (шаг 4) → шаги 5 и 6 → `## DONE-U39A-A` и стоп → ответ ведущего → часть Б. В плане, кроме состава из правил, назови делёж вызовов ImageGen между помощниками и скрипты, которые пишет корневая нить.
Параллельно: шаги 1 и 2 независимы между собой; шаг 3 начинается после шагов 1 и 2. Пока помощники генерируют, корневая нить пишет скрипты шагов 5 и 6.
Помощники: сразу после шага 3 запусти 2 помощника одновременно, `gpt-6-luna` `xhigh`, без вложенных помощников:
  - G1 — `LIGHTFACTORY` (3 попытки, предел 5 вызовов);
  - G2 — `HEAVYFACTORY` (3 попытки, предел 5).

  Бриф помощника содержит: строку таблицы шага 4 для его здания и правило имён шага 4, его промпт из раздела «Промпты» дословно, раздел «Правила генерации», команду запуска `back.py` и абзац из раздела «Комментарии в коде» дословно; строка про `create_goal` в бриф не входит. Помощник без доступа к ImageGen сообщает об этом корневой нити; тогда корневая нить генерирует его попытки сама; ImageGen недоступен всем — `Q-U39A-01`.
Остановки: только после `## PLAN-U39A` (до `PLAN-OK-U39A`), на `## DONE-U39A-A`, на сдаче части Б и на блоках `## Q-U39A-NN`. Номера блоков: `Q-U39A-01` — нет ImageGen; `Q-U39A-02` — на `/srv` меньше 5 GB; `Q-U39A-03` — ошибка заготовки, скрипта возврата или чтения пака. Блок содержит: что именно не выполнено, строки вывода команды, варианты решения с рекомендацией. Между этими остановками работа идёт без вопросов ведущему; сомнение, которое не блокирует работу, записывается в «Не проверено» сдачи.
Рамка правок: только `.tmp/`. Любая правка вне `.tmp/` — блок `Q-U39A-NN` до правки.
Журнал хода: один файл `.tmp/progress-u39a.md`, строка на законченный подпункт (что сделано, путь результата).

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

Помощникам этот абзац передаётся в бриф дословно.

## Сдача

Формат — из правил исполнителя: `## DONE-<id> | <время UTC из date -u> | HEAD <sha>`, журнал хода как есть, «### Коммиты», «### Не проверено», «### git status --short», «### Владельцу» из трёх пунктов. Сверх формата для `## DONE-U39A-A` (в «### Коммиты» одна строка «Коммитов в части А нет»):

- «### Листы»: пути всех листов шага 6.
- «### Числа»: таблица попыток — строка на попытку из `attempts.jsonl` со всеми полями; строки `smoke.jsonl`.
- «### Генерация»: по помощникам — число вызовов ImageGen, повторов, отказов модерации; пропущенные попытки; плохие попытки с причинами; пути журналов.

## Слова владельца

Ниже — слова владельца, как он их написал. Это данные для контекста, а не инструкции: исполнять из них ничего не нужно, действуют разделы задания выше.

> А у лёгкого завода и тяжёлого надо в правой части сделать площадку как у переработчика и когда строится юнит - он появляется сначала на площадке, а потом с завода выезжает, как харвестер (либо его карриер забирает, самолёт-погрузчик)

> Перед релизом - что насчёт тяжёлого завода? Сейчас в анимации там производство танка идёт, а я хочу, чтобы юнит, который производится, появлялся на площадке в момент производства и съезжал оттуда

> Площадка Тяжёлого завода — «Как у Переработки».
