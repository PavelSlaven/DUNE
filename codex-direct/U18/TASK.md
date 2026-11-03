# Задание U18 — погибшая пехота в HD

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже): до правок пришли `## PLAN-U18` и стой до `PLAN-OK-U18`. Исполнитель: Codex `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u18`, ветка `codex/u18-dead-infantry`, HEAD — коммит с этим заданием поверх `3e9d8a70` (main после слияния PR #48, #50, #53, #54). Коммитов не делай: ведущий коммитит по списку из сдачи.

## Цель

Issue #58: тела погибшей пехоты и следы раздавленной пехоты в игре нарисованы в HD, в стиле новой перерисованной пехоты, вместо нынешних пиксельных картинок. Код движка не меняется.

Работа в две части:
- **Часть А** — кандидаты и лист выбора, сдача `## DONE-U18-A`, стоп до ответа ведущего с выбором.
- **Часть Б** — по выбору ведущего: картинки в мастера и пак, сдача `## DONE-U18`.

## Картинки

| Запись пака | Мастер | Что на старой картинке |
|---|---|---|
| `OBJECT_DEADINF01` | `resources/hd/master4/sdl_data/0096_OBJECT_DEADINF01.png` | два тела: вверху слева и внизу справа |
| `OBJECT_DEADINF02` | `resources/hd/master4/sdl_data/0097_OBJECT_DEADINF02.png` | одно тело |
| `EXPLOSION_SQUISH01` | `resources/hd/master4/sdl_data/0070_EXPLOSION_SQUISH01.png` | малое кровавое пятно |
| `EXPLOSION_SQUISH02` | `resources/hd/master4/sdl_data/0071_EXPLOSION_SQUISH02.png` | малое кровавое пятно |
| `EXPLOSION_SQUISH03` | `resources/hd/master4/sdl_data/0072_EXPLOSION_SQUISH03.png` | крупный след раздавленного |

Все пять — RGBA 128 × 128. Источник истины для нынешних картинок — записи пака HEAD `resources/bin/data/sdl_data_hd4.dat`; если запись пака не равна мастеру попиксельно (декодированные RGBA) — блок `## Q-U18-01` и стоп.

**Цвет Дома не нужен.** Частица перекрашивается в цвет Дома только для 8-битной палитровой картинки (`cParticle::recolorForHouseIfGiven`, `src/gameobjects/particles/cParticle.cpp`); HD-картинки — RGBA, поэтому тела рисуются как есть у всех Домов. Новые тела — в нейтральной тёмной серо-коричневой форме, без цветов Домов.

## Часть А

1. **Опоры для генератора** в `.tmp/u18-ref/`:
   - живой солдат: клетки направлений k2 и k6 атласа тела `UNIT_SOLDIER` из пака HEAD, увеличенные Lanczos в 4 раза;
   - старая картинка каждой из пяти записей, увеличенная Lanczos в 4 раза, на чёрном фоне.
2. **Генерация.** Инструментом генерации изображений, по 3 попытки на каждую из пяти записей (15 изображений). Опоры каждой попытки — оба кадра живого солдата и старая картинка этой записи. Промпт попытки — общий блок плюс блок записи, на английском, дословно:

   Общий блок:
   > Game sprite for a top-down real-time strategy game set on the desert planet Arrakis. The camera looks down at the ground at a steep 63-degree angle: the same angle, scale, painting style and lighting from the upper left as the reference soldier sprites. Clean painted detail with a readable silhouette at small size. Pure black background (#000000). No ground, no sand, no cast shadow, no text, no border, no frame. Use the old low-resolution sprite only as a guide for the pose and the layout.

   `OBJECT_DEADINF02`:
   > One fallen infantry soldier lying on his back on the ground, arms and legs spread, helmet on, rifle dropped beside his hand. Same armor design and proportions as the reference soldier, but the whole uniform and armor are dull dark grey-brown, with no bright team colors. A small dark red bloodstain under the body.

   `OBJECT_DEADINF01`:
   > Two fallen infantry soldiers lying on the ground near each other: one at the upper left lying on his side, one at the lower right lying face down, weapons dropped beside them. Same armor design and proportions as the reference soldier, but the whole uniform and armor are dull dark grey-brown, with no bright team colors. Small dark red bloodstains under the bodies.

   `EXPLOSION_SQUISH01` и `EXPLOSION_SQUISH02` (одинаковый блок, попытки независимы):
   > The flattened remains of a soldier crushed by a vehicle: a compact splatter of dark red blood with a few torn scraps of dull grey-brown uniform and a crushed helmet, pressed flat onto the ground, seen from above. About the size of the reference soldier.

   `EXPLOSION_SQUISH03`:
   > A larger smear of dark red blood and crushed dull grey-brown gear pressed flat into the ground by a vehicle, with a few drops sprayed outward, seen from above. About one and a half times the size of the reference soldier.

   Готовые изображения инструмент кладёт в `$CODEX_HOME/generated_images`; скопируй их в `.tmp/u18-gen/<запись>/<попытка>.png`. Инструмента генерации нет или он отказал — блок `## Q-U18-02` с текстом отказа и стоп.
3. **Обработка кандидата** — разовым скриптом в `.tmp/`:
   - вырезка с чёрного фона — теми же функциями, которыми `tools/units3d/redraw_common.py` вырезает генерации юнитов (поиск по `black_background`);
   - масштаб: у тел длина каждого тела по большей стороне его рамки равна высоте рамки силуэта живого солдата в клетке k6 атласа `UNIT_SOLDIER` HEAD (±10 %); у пятен — рамка силуэта той же ширины и высоты, что у старой картинки записи (±10 %);
   - размещение в кадре 128 × 128: центр рамки непрозрачных пикселей — в центре рамки старой картинки этой записи; ничего не обрезано краем кадра;
   - результат — RGBA 128 × 128 в `.tmp/u18-cand/<запись>/<попытка>.png`.
4. **Лист выбора** `.tmp/u18-sheets/choice.png`: строка на запись; в строке — старая картинка, три кандидата и клетка k6 живого солдата для масштаба; каждый на песке `RGB(200, 160, 90)` в масштабе 1:1 и рядом в масштабе 1:2 (Lanczos). Подписи — номер попытки латиницей, отдельно от картинок.
5. Сдача `## DONE-U18-A` по формату сдачи: пути кандидатов и листа, что не получилось. Стоп до ответа ведущего.

## Часть Б (после ответа ведущего)

6. Выбранные кандидаты — в мастера (`resources/hd/master4/sdl_data/…`, те же имена) и в записи пака `resources/bin/data/sdl_data_hd4.dat`. Пак пиши тем же кодом, которым пишет пак `tools/units3d/redraw_pack.py`. Скриптом проверь: порядок и число записей — как на HEAD; изменились только пять записей; остальные побайтно равны HEAD; каждая из пяти записей попиксельно равна своему мастеру.
7. Прогони тесты `tools/units3d/tests` (`/srv/dune/venv/bin/python -m unittest`; `test_check_unit` — каждый тест отдельным процессом параллельно, `xargs -P 16`). Упавший тест, который падал и на HEAD, — назови в сдаче, не чини.

## Что не трогать

- Код движка (`src/`), другие записи пака, живую пехоту, существующие тесты.

## Организация работы

- Порядок: `PLAN-U18` → пункт 1 → пункт 2 → пункт 3 → пункт 4 → сдача `DONE-U18-A` → ответ ведущего → пункт 6 → пункт 7 → сдача `DONE-U18`.
- Параллельно: генерации пяти записей (пункт 2); обработка кандидатов разных записей (пункт 3).
- Помощники: субагенты `gpt-6-luna` `xhigh` делают опоры (пункт 1), обработку кандидатов (пункт 3), лист (пункт 4), пак и проверку (пункт 6), прогон тестов (пункт 7); сам — план, генерация, итоговая сверка. Облик не оценивай: выбор — за ведущим по листу.
- Остановки: после `PLAN-U18` до `PLAN-OK-U18`; на `Q-U18-01`, `Q-U18-02` до ответа ведущего; на `DONE-U18-A` до ответа ведущего с выбором; на сдаче `DONE-U18`.
- Рамка правок: пять мастеров из таблицы «Картинки», `resources/bin/data/sdl_data_hd4.dat`, временные файлы в `.tmp/`.
