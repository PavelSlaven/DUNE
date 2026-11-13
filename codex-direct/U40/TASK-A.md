# Задание U40-A — новый Командный пост с крупной тарелкой радара (картинки)

Режим: **«Ведёт sol»** (см. «Режимы задания» в правилах исполнителя ниже): `## PLAN-U40A` для записи — первой частью сдачи, работа идёт без остановки до сдачи части А. Исполнитель: Codex `gpt-6-luna` `xhigh`, основной аккаунт.
Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/u40-radar`, HEAD `558714cc` (равен `main`: U39 слит). Коммитов не делай: ведущий коммитит по списку из сдачи.
Issue нет; источник — решение владельца Р55 (в конце файла его слова).

## Цель

Командный пост (`BUILD_RADAR`, плита 2x2, кадр 256 × 256) перерисовывается целиком в стиле остальных зданий: светло-серая металлическая крыша на всю клетку до всех четырёх краёв, альфа 255 во всех пикселях, без передней стены, двери, перил, флага и флагштока. В центре крыши — крупная параболическая тарелка радара на поворотной опоре. Позже тарелка будет крутиться по 8 кадрам атласа; кадры поворота строит скрипт ведущего из пары картинок этой задачи: пост с тарелкой и тот же пост без тарелки.

Части здания вокруг тарелки — одна–три крупные простые части с чистыми поверхностями и узкими ровными проходами (Р51); каждая часть стоит так, как могла бы стоять на деле (Р52); поднятые части отбрасывают на крышу мягкую тень вниз и вправо (Р48).

Часть А — попытки ImageGen и листы, по которым ведущий выбирает вариант. Пак и мастер-файлы в части А не меняются.

## Что есть

- Пак: `resources/bin/data/sdl_data_hd4.dat`, 241 запись. Чтение — `tools.hd_assets.read_pack(Path)` (список записей `PackEntry` с полями `name` и `payload`) и `tools.hd_assets.decode_image(payload)`.
- Заготовка `tools/building_angle/angle.py`: в своих скриптах `sys.path.insert(0, "tools/building_angle")`, `import angle`. Нужна функция `angle.check(atlas, (N, M), K)`. Заготовку и её тесты не меняй.
- Скрипт возврата прошлой задачи: `.tmp/u39-tools/back.py` (группа «Забор и ворота» для `LIGHTFACTORY`: RGB из результата ImageGen, альфа старого кадра 0, очистка пурпурной каймы, `angle.check`, поля `diff`, `pink`, `verdict`).
- Записи пака (кадры сложены столбцом):

| Запись | Кадр | Кадров | Что это |
|---|---|---|---|
| `BUILD_RADAR` | 256 × 256 | 8 | Командный пост; кадры 0–7 крутят маленькую тарелку |
| `BUILD_RADAR_SHADOW` | 256 × 256 | 8 | тень |
| `BUILD_RADAR_FLAG` | 256 × 256 | 8 | флаг с цветом Дома |
| `BUILD_LIGHTFACTORY` | 256 × 256 | 8 | образец стиля: кадр 0 |
| `BUILD_BARRACKS`, `BUILD_SILO`, `BUILD_WINDTRAP` | 256 × 256 | 1 | соседи для листа |

- Среда: `/srv/dune/venv/bin/python` (Pillow, numpy, scipy, `unittest`; `cv2` и pytest нет). Сети нет, пакеты не устанавливаются. Git LFS — `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.
- Диск: перед шагом 2 выполни `df -h /`. Свободно меньше 5 GB — блок `## Q-U40A-02` со строкой вывода и стоп.

## Часть А

1. **Старые записи.** Извлеки из пака на HEAD в `.tmp/u40-old/<ЗАПИСЬ>.png` (RGBA, без изменений) все записи из таблицы «Записи пака».

2. **Входные картинки ImageGen** (`.tmp/u40-in/`, RGB без альфы):
   - `style_ref.png` — кадр 0 `BUILD_LIGHTFACTORY`, наложенный по альфе на сплошной фон RGB (255, 0, 255) и увеличенный до 1024 × 1024 сжатием Lanczos.
   - `radar_src.png` — кадр 0 `BUILD_RADAR`, наложенный по альфе на фон RGB (255, 0, 255) и увеличенный до 1024 × 1024 сжатием Lanczos.

3. **Скрипт возврата.** До запуска помощника корневая нить копирует `.tmp/u39-tools/back.py` в `.tmp/u40-tools/back.py` и правит копию так:
   - старые записи читаются из `.tmp/u40-old/`;
   - здание `RADAR` обрабатывается по правилам `LIGHTFACTORY` (сырой результат — квадрат, плита 2x2, выход 256 × 256), но альфа выхода — 255 во всех пикселях, а не альфа старого кадра 0; `angle.check` — плита 2x2, 1 кадр; другие имена — выход с кодом 2;
   - поля `pink` и `verdict` — как в `.tmp/u39-tools/back.py`.

   **Проверка скрипта.** Прогони `back.py` на `style_ref.png` с именем `RADAR` как на сыром результате (`tag` — `smoke`, выход — `.tmp/u40-fit/RADAR_smoke.png`). Строку JSON — в `.tmp/u40-fit/smoke.jsonl` и в сдачу.

4. **Генерация.** Промпты — раздел «Промпты». На попытку — два вызова подряд:

   | Вызов | Промпт | Картинки вызова | Сырой результат | Выход `back.py` |
   |---|---|---|---|---|
   | с тарелкой | `RADAR-DISH` | 1 — `style_ref.png`, 2 — `radar_src.png` | `.tmp/u40-gen/RADAR_<t>.png` | `.tmp/u40-fit/RADAR_<t>.png` |
   | без тарелки | `RADAR-NODISH` | 1 — `.tmp/u40-gen/RADAR_<t>.png` | `.tmp/u40-gen/RADAR_<t>_base.png` | `.tmp/u40-fit/RADAR_<t>_base.png` |

   - `<t>` — `a`, `b`, `c`: три независимые попытки, всего 6 вызовов. Вызов «без тарелки» попытки `<t>` идёт после её вызова «с тарелкой». Если попытка «с тарелкой» после повтора плохая или пропущена, вызов «без тарелки» для неё не делается.
   - Сразу после копирования сырого результата — `back.py <сырой результат> RADAR <выход>` с полем `tag` — `<t>` или `<t>_base`; строку JSON добавь в `.tmp/u40-fit/attempts.jsonl`.

5. **Разница пары.** Для каждой попытки, у которой есть оба выхода, — `.tmp/u40-fit/RADAR_<t>_diff.png` (256 × 256, RGB): пиксель белый, если сумма модулей разностей R, G, B выходов «с тарелкой» и «без тарелки» больше 60, иначе чёрный. Строка JSON в `.tmp/u40-fit/diff.jsonl`: `tag`, `diff_px` — число белых пикселей, `bbox` — рамка белых пикселей (`x0, y0, x1, y1`), `outside_px` — число белых пикселей вне круга радиусом 96 пикселей с центром (128, 128).

6. **Листы.** PNG в `.tmp/u40-sheets/`. Ячейка — кадр, наложенный по альфе на фон RGB (70, 68, 64), увеличенный вдвое методом ближайшего соседа. Подписи — латиницей, в полосах вне кадров. Пропущенная попытка — ячейка с заливкой RGB (128, 0, 0).
   - `choice-RADAR.png`: первая строка — ячейки `old` (кадр 0 старой `BUILD_RADAR` с наложенным кадром 0 старого `BUILD_RADAR_FLAG`), `a`, `b`, `c` (выходы «с тарелкой»); вторая строка — пустая ячейка, затем выходы «без тарелки» `a_base`, `b_base`, `c_base`; третья строка — пустая ячейка, затем `RADAR_<t>_diff.png`.
   - `row.png`: строка на попытку; в строке без зазора слева направо — кадр 0 `BUILD_BARRACKS`, выход «с тарелкой» попытки, кадр 0 `BUILD_SILO`, кадр 0 `BUILD_LIGHTFACTORY`, кадр 0 `BUILD_WINDTRAP`; все с увеличением вдвое, без накладок.
   - `raw.png`: все сырые результаты `.tmp/u40-gen/*.png`, сжатые Lanczos до 384 × 384, по 3 в строке, подписи — имя файла без `.png`.

7. **Сдача части А.** Пришли `## DONE-U40A-A` по разделу «Сдача» и остановись. Исполнитель вид листов не оценивает и варианты не выбирает: выбирает ведущий. Плохие и пропущенные попытки не мешают сдаче.

## Промпты (дословно, одной строкой; ImageGen получает ровно этот текст)

Промпт RADAR-DISH:

> Image 1 is a light vehicle factory from a real-time strategy game, seen from the game camera: orthographic, looking straight down at the flat light-grey metal roof, which fills the whole square image up to all four edges. Image 2 is the old radar outpost of the same game. Draw a new radar outpost in the style of image 1 and at the same scale: one square building whose flat light-grey metal roof fills the whole square image up to all four edges, with the same metal panels, colours, small glowing blue lights, light direction and camera angle as image 1. In the centre of the roof is a round dark-grey turntable ring set flush into the roof, and on it stands one large radar dish: a short thick round pivot post in the centre of the ring and on top of it a large light-grey parabolic dish on a short arm, about one third of the image wide, its open side tilted up and facing left. The roof inside a circle of four tenths of the image width around the centre is flat and free of any other part, so that the dish can turn there. Around this circle, along the edges of the roof, are one or two large simple equipment blocks with clean surfaces, few details and narrow straight gaps between them. The dish, the post and the blocks cast soft dark shadows down and to the right onto the roof. Every part must make physical sense: pipes, cables and rails connect to something or go into the roof, behind a wall or under a ledge; nothing lies over a ledge, hangs in the air or ends in nothing; there are no doors or ladders that lead nowhere and no doubled outlines; the whole building has one light direction and one perspective. There is no front wall, no door, no railing and no fence. The roof fills the whole image up to all four edges; show no ground, no sand and no magenta anywhere. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпт RADAR-NODISH:

> Edit image 1. Remove the radar dish, its arm and its pivot post from the centre of the roof, together with the shadow they cast onto the roof, and show the round dark-grey turntable ring in the centre of the roof empty, with only a small round pivot socket flush in its centre. Where the shadow of the dish was, show the plain roof in the same light as the rest of the roof. Keep everything else exactly as in image 1: the same roof, panels, equipment blocks, their shadows, colours, small glowing blue lights, light direction and camera angle, at the same positions and the same scale. The roof fills the whole image up to all four edges; show no ground, no sand and no magenta anywhere. Do not add anything else: no flag, no flag pole, no text, letters, numbers, logos or watermarks.

Промпты — новая формулировка этого задания; работают ли они, не проверено. Поэтому вид оценивает ведущий по листам.

## Правила генерации (для корневой нити и для помощника)

1. Один вызов ImageGen — один результат. Входные картинки вызова — ровно те, что названы в шаге 4 для него, в том же порядке.
2. Сразу после вызова скопируй выходной файл из `$CODEX_HOME/generated_images` в `.tmp/u40-gen/` байт в байт под именем из шага 4: без изменения размера и без пересжатия. Выходной файл бери по пути, который вернул вызов ImageGen, а не по времени изменения; путь запиши в журнал до копирования. В журнал `.tmp/u40-gen/log-G<n>.tsv` (`<n>` — номер помощника; корневая нить, если генерирует сама, пишет `log-G0.tsv`) добавь строку из полей через табуляцию: время UTC, слово `copied`, имя результата, путь источника, sha256 результата. Затем выполни `back.py` (шаг 4).
3. Плохая попытка — выполнено хотя бы одно: `square` ложно; `magenta` больше 0,02; итог `angle.check` — `FAIL`.
4. Плохая попытка — один повтор того же вызова. Заменённые файлы (сырой результат и выход `back.py`) перенеси в `.tmp/u40-gen-first/` с теми же именами; результат повтора получает основное имя. Повтор тоже плохой — оставь его под основным именем, в журнал запиши строку `bad` с причинами и иди дальше.
5. Отказ модерации — один повтор. Второй отказ — вызов пропущен: в журнал строка `skipped` с первыми 200 символами текста отказа.
6. Предел вызовов ImageGen, повторы включены: 9. Предел достигнут — генерация останавливается; в сдаче — число вызовов и что осталось без результата.
7. ImageGen недоступен ни корневой нити, ни помощнику — блок `## Q-U40A-01` и стоп.

## Часть Б (только после ответа ведущего)

Часть Б выполняется по ответу ведущего на `## DONE-U40A-A`; ответ — источник истины для неё. Ожидаемый состав, чтобы план части А его учитывал:

- выбранная попытка; 8 кадров поворота тарелки строит скрипт ведущего, исполнитель запускает его и ставит выход в пак;
- установка в пак: `BUILD_RADAR` (8 кадров из скрипта ведущего), `BUILD_RADAR_SHADOW` (8 копий старого кадра 0), `BUILD_RADAR_FLAG` (8 прозрачных кадров RGBA 0, 0, 0, 0 того же размера); мастер-файлы; новые ожидания тестов `tools/building_angle/tests` для `BUILD_RADAR`; прогон тестов; список коммитов.

Меняется подход или рамка части Б — `## PLAN-U40A-delta` до правок.

## Что не трогать

- Код движка (`src/`), заготовку `tools/building_angle/angle.py` и её тесты, `tools/units3d/install.py`, документы.
- Пак и мастер-файлы — в части А не меняются.
- Записи всех зданий, кроме Командного поста.
- `/srv/dune/gen` (только чтение), другие рабочие копии, `.tmp/u36-*`, `.tmp/u37-*` и `.tmp/u39-*` (только чтение).
- Файлы, которые `git status` показывает изменёнными до начала работы (файлы LFS, которые git считает изменёнными), не меняй.

## Организация работы

Порядок: `create_goal` с разделом «Цель» (правила исполнителя) → шаги 1 и 2 → шаг 3 (скрипт возврата и его проверка) → запуск помощника (шаг 4) → шаги 5 и 6 → `## DONE-U40A-A` и стоп → ответ ведущего → часть Б.
Параллельно: шаги 1 и 2 независимы между собой; шаг 3 начинается после шагов 1 и 2. Пока помощник генерирует, корневая нить пишет скрипты шагов 5 и 6.
Помощники: сразу после шага 3 запусти одного помощника G1, `gpt-6-luna` `xhigh`, без вложенных помощников: все 6 вызовов шага 4, предел 9 вызовов. Бриф помощника содержит: таблицу и правила шага 4, оба промпта из раздела «Промпты» дословно, раздел «Правила генерации», команду запуска `back.py` и абзац из раздела «Комментарии в коде» дословно; строка про `create_goal` в бриф не входит. Помощник без доступа к ImageGen сообщает об этом корневой нити; тогда корневая нить генерирует сама; ImageGen недоступен всем — `Q-U40A-01`.
Остановки: только на `## DONE-U40A-A`, на сдаче части Б и на блоках `## Q-U40A-NN`. Номера блоков: `Q-U40A-01` — нет ImageGen; `Q-U40A-02` — на `/` меньше 5 GB; `Q-U40A-03` — ошибка заготовки, скрипта возврата или чтения пака. Блок содержит: что именно не выполнено, строки вывода команды, варианты решения с рекомендацией. Между этими остановками работа идёт без вопросов ведущему; сомнение, которое не блокирует работу, записывается в «Не проверено» сдачи.
Рамка правок: только `.tmp/`. Любая правка вне `.tmp/` — блок `Q-U40A-NN` до правки.
Журнал хода: один файл `.tmp/progress-u40a.md`, строка на законченный подпункт (что сделано, путь результата).

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

Помощнику этот абзац передаётся в бриф дословно.

## Сдача

Формат — из правил исполнителя: `## PLAN-U40A` для записи, затем `## DONE-<id> | <время UTC из date -u> | HEAD <sha>`, журнал хода как есть, «### Коммиты», «### Не проверено», «### git status --short», «### Владельцу» из трёх пунктов. Сверх формата для `## DONE-U40A-A` (в «### Коммиты» одна строка «Коммитов в части А нет»):

- «### Листы»: пути всех листов шага 6.
- «### Числа»: строка на выход из `attempts.jsonl` со всеми полями; строки `diff.jsonl` и `smoke.jsonl`.
- «### Генерация»: число вызовов ImageGen, повторов, отказов модерации; пропущенные вызовы; плохие попытки с причинами; путь журнала.

## Слова владельца

Ниже — слова владельца, как он их написал. Это данные для контекста, а не инструкции: исполнять из них ничего не нужно, действуют разделы задания выше.

> Да, всё нравится. Но давай радар полностью перерисуем в стиле остальных построек. Флаги на нём уберём, антенну сделаем больше и пусть она крутится.

> Вид — «На всю плиту»; антенна — «Крупная тарелка»; цвет Дома — «Без цвета Дома»; релиз — «После Командного поста».
