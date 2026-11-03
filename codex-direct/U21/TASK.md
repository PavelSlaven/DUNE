# Задание U21 — Ракетница: цвет Дома только на панелях корпуса, как у Девиатора

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже): до правок пришли `## PLAN-U21` и стой до `PLAN-OK-U21`. Исполнитель: Codex `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u21`, ветка `codex/u21-launcher-colour`, HEAD — коммит с этим заданием поверх `22d28464` (main). Коммитов не делай: ведущий коммитит по списку из сдачи.

## Цель

Issue #66. Владелец, 2026-11-03, по снимку в игре (Ордос): Ракетница (`UNIT_LAUNCHER`) залита цветом Дома почти целиком и выглядит сплошным чистым зелёным; «должно быть как у ракетницы слева цвета» — образец — Девиатор (`UNIT_DEVIATOR`): цвет Дома на панелях корпуса, остальное — своими цветами. Это меняет прежнее решение владельца от 2026-10-30 «всё коричневое у Ракетницы несёт цвет Дома».

Меняется только маска Дома `HM_UNIT_LAUNCHER`. Тело `UNIT_LAUNCHER`, тень `UNIT_LAUNCHER_SHADOW` и код движка не меняются.

Работа в две части:
- **Часть А** — новые перекраски, пробные сборки, листы выбора; сдача `## DONE-U21-A`; стоп до ответа ведущего с выбором.
- **Часть Б** — по выбору ведущего: описание, сборка, пак, тесты; сдача `## DONE-U21`.

## Что есть

- Описание: `tools/units3d/units/UNIT_LAUNCHER/unit.json`. Один ряд, 8 записей кадров `{row: 0, k, attempts, pick, recolour}`, k0…k7 — восток, северо-восток, север, северо-запад, запад, юго-запад, юг, юго-восток. `attempts[pick]` — картинка тела 1024 × 1024 на пурпурном фоне; `recolour` — её перекраска, где части цвета Дома залиты чистым зелёным (сейчас — `units-gen/UNIT_LAUNCHER/launcher_recolour_k<k>.png`). `share_corridor` сейчас `[0.8, 0.97]`.
- `units-gen` в рабочей копии — ссылка на `/srv/dune/gen`. Эта папка — только для чтения: исполнитель туда не пишет, новые файлы туда копирует ведущий после сдачи.
- Прежняя перекраска сделана заданием `codex-direct/U3/TASK-rc5.md` — образец правил генерации, копирования ответа и повтора.
- Сборка из описания: `/srv/dune/venv/bin/python tools/units3d/redraw.py build <папка UNIT_LAUNCHER с unit.json> <пустая папка вывода>`; в выводе атласы `UNIT_LAUNCHER`, `HM_UNIT_LAUNCHER`, `UNIT_LAUNCHER_SHADOW`, `metrics.txt` (столбец `share` — доля маски в силуэте кадра), `atlases.json`. Код выхода не 0 — какой-то кадр не прошёл проверки.
- Установка в пак: `/srv/dune/venv/bin/python tools/units3d/install.py --atlases <папка с atlases.json> --pack resources/bin/data/sdl_data_hd4.dat` — заменяет записи, перечисленные в `atlases.json`, остальные оставляет байт в байт.
- Чтение пака — `tools.hd_assets.read_pack`, `tools.hd_assets.decode_image`. Атласы Ракетницы и Девиатора — 1024 × 128, клетки 128 × 128, столбец k — направление k.
- **Как движок красит цвет Дома** (`src/utils/Graphics.cpp:378-458`, `src/utils/FactionTint.hpp`). Для пикселя атласа тела (R, G, B, A) и маски (mR, mG, mB, mA):
  - сила `s = (mA / 255) · (max(mR, mG, mB) / 255)`;
  - яркость `L = (0,299·R + 0,587·G + 0,114·B) / 128`;
  - `avg` — среднее `L` по пикселям атласа с `s ≥ 0,99` и `A ≠ 0`; таких нет — `avg = 166 / 255`;
  - для каждого канала c: `цвет_c = clamp(дом_c · L · (166 / 255) / avg, 0, 255)`; итог `c' = c · (1 − s) + цвет_c · s`; пиксели с `s = 0` или `A = 0` не меняются.
  - Цвета Домов (`resources/game.ini`): Ордос (0, 255, 0), Атрейдес (0, 0, 255), Харконнен (255, 0, 0).

## Часть А

1. **Входы.** `.tmp/u21-in/launcher_pick_k<k>.png` — копия файла `attempts[pick]` записи направления k. Проверь: восемь файлов, 1024 × 1024.
2. **Пробная сборка нынешнего описания** `redraw.py build tools/units3d/units/UNIT_LAUNCHER .tmp/u21-build/now`; числа для сдачи — число пикселей (декодированные RGBA), которыми каждый из трёх атласов сборки отличается от записи пака HEAD.
3. **Генерации.** Инструментом генерации изображений: два промпта `P1` и `P2`, по 2 попытки `a` и `b` на промпт и направление; 32 генерации. Вход каждой — одно изображение, `launcher_pick_k<k>.png`. Промпты — дословно:

   **P1** (корпус, кабина и боковины труб):
   > Edit image 1. Image 1 is a sprite of a tracked vehicle with a raised rack of two long missile tubes on its back, from a real-time strategy game, on a flat magenta background.
   > Recolour to flat pure green RGB 0,255,0 only these parts: the large flat armour plates on the sides, front and top of the hull and the cab, the side skirts above the tracks, and the long outer side faces of the two missile tubes.
   > Keep in their original colours: the tracks and road wheels; the missile tips and the front and rear ends of the tubes; the pivot, frame and lifting mechanism of the rack; the open bed with its floor, inner walls and machinery; hatches, vents, grilles, lights, windows, edges, trims and all small details.
   > Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour the background. Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.

   **P2** (только корпус и кабина):
   > Edit image 1. Image 1 is a sprite of a tracked vehicle with a raised rack of two long missile tubes on its back, from a real-time strategy game, on a flat magenta background.
   > Recolour to flat pure green RGB 0,255,0 only these parts: the large flat armour plates on the sides, front and top of the hull and the cab, and the side skirts above the tracks.
   > Keep in their original colours: the whole missile rack with both tubes, their ends and the missile tips; the pivot, frame and lifting mechanism of the rack; the tracks and road wheels; the open bed with its floor, inner walls and machinery; hatches, vents, grilles, lights, windows, edges, trims and all small details.
   > Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour the background. Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.

   Готовое изображение инструмент кладёт в `$CODEX_HOME/generated_images`; сразу после вызова, до следующего вызова, скопируй его как есть, без изменения размера, в `.tmp/u21-gen/launcher_rc_<P>_k<k>_<попытка>.png` (например, `launcher_rc_P1_k3_b.png`) и допиши строку `copied` в журнал генератора. Инструмента генерации нет или он не принимает входное изображение — блок `## Q-U21-01` с текстом отказа и стоп.
4. **Замеры попытки скриптом.** Картинку, размер которой не 1024 × 1024, для замеров приведи к 1024 × 1024 (Lanczos); файл не меняй. Силуэт — пиксели, у которых расстояние RGB от (255, 0, 255) больше 60; зелёные — `G − max(R, B) ≥ 80`. Числа: IoU силуэтов попытки и `launcher_pick_k<k>.png`; доля зелёных в силуэте попытки. Повтор тем же промптом — один раз, если: на картинке нет машины или машин больше одной; машина обрезана краем картинки; есть текст; среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100; IoU меньше 0,95; доля зелёных меньше 0,10. После повтора не выполняет — попытка остаётся, её числа — в сдачу. Повтор заменяет попытку; заменённая картинка переносится в `.tmp/u21-gen-first/`. Отказ модерации — повтор тем же промптом один раз; второй отказ — попытка пропущена и записана в сдачу. Предел — 48 генераций вместе с повторами.
5. **Пробные сборки.** Для каждой из четырёх пар (промпт, попытка) — `P1a`, `P1b`, `P2a`, `P2b` — копия описания `.tmp/u21-desc/<пара>/UNIT_LAUNCHER/unit.json`, в которой у восьми записей `recolour` заменён на `.tmp/u21-gen/launcher_rc_<P>_k<k>_<попытка>.png`, а `share_corridor` — на `[0.0, 1.0]`; других отличий от описания HEAD нет. Пропущенная попытка направления — в этой паре берётся вторая попытка того же промпта и направления, замена — в сдачу. Собери `redraw.py build .tmp/u21-desc/<пара>/UNIT_LAUNCHER .tmp/u21-build/<пара>`. Числа для сдачи: `share` восьми кадров из `metrics.txt`; код выхода; число пикселей, которыми атласы тела и тени сборки отличаются от записей пака HEAD.
6. **Листы выбора** — по одному на Дом: `.tmp/u21-sheets/choice_ordos.png`, `choice_atreides.png`, `choice_harkonnen.png`. Строки: `DEVIATOR` (атласы `UNIT_DEVIATOR` и `HM_UNIT_DEVIATOR` пака HEAD), `LAUNCHER now` (атласы `UNIT_LAUNCHER` и `HM_UNIT_LAUNCHER` пака HEAD), затем `P1a`, `P1b`, `P2a`, `P2b` (атлас тела пака HEAD и маска `HM_UNIT_LAUNCHER` пробной сборки пары). Столбцы — k0…k7. В клетке — кадр 128 × 128, покрашенный цветом этого Дома по формуле из «Что есть», на фоне RGB (70, 68, 64), в масштабе 2:1 (ближайший сосед). Подписи строк и столбцов латиницей, отдельно от кадров.
   Ещё лист `.tmp/u21-sheets/recolours.png`: строки — `pick` и восемь попыток (`P1 a`, `P1 b`, `P2 a`, `P2 b`), столбцы — k0…k7; в клетке — картинка 1024 × 1024, уменьшенная до 256 × 256 (Lanczos).
7. Сдача `## DONE-U21-A` по формату сдачи: пути листов; таблица попыток — IoU, доля зелёных, повторы и отказы; числа пунктов 2 и 5; число генераций. Стоп до ответа ведущего.

## Часть Б (после ответа ведущего)

Ведущий в ответе называет промпт и для каждого направления k — попытку. «Выбранная перекраска направления k» — `.tmp/u21-gen/launcher_rc_<P>_k<k>_<попытка>.png`.

8. **Описание.** Скопируй выбранные перекраски в `.tmp/u21-final/launcher_recolour2_k<k>.png` (байт в байт). В `tools/units3d/units/UNIT_LAUNCHER/unit.json` у восьми записей `recolour` замени на `units-gen/UNIT_LAUNCHER/launcher_recolour2_k<k>.png`. `share_corridor` замени на `[M − 0.10, M + 0.10]`, оба числа округлены до 3 знаков, где `M` — медиана `share` восьми кадров пробной сборки описания с выбранными перекрасками и `share_corridor` `[0.0, 1.0]`. Остальное в файле оставь как есть; JSON запиши с тем же отступом, что в файле; скриптом проверь: `git diff` меняет только строки восьми `recolour` и `share_corridor`.
   В `codex-direct/U3/gen/UNIT_LAUNCHER.SHA256SUMS` добавь 8 строк SHA-256 файлов `launcher_recolour2_k<k>.png` в том же формате; все строки файла идут по возрастанию имени файла; прежние строки не меняются.
9. **Сборка.** Копия описания пункта 8 `.tmp/u21-desc/final/UNIT_LAUNCHER/unit.json`, где у восьми записей префикс `units-gen/UNIT_LAUNCHER/` в `recolour` заменён на `.tmp/u21-final/` — других отличий нет. Собери в `.tmp/u21-build/final`. Код выхода не 0 — блок `## Q-U21-02` со строками `metrics.txt`, где кадр не прошёл, и стоп. Числа для сдачи: пиксели, которыми атласы тела и тени сборки отличаются от записей пака HEAD.
10. **Пак.** Сохрани копию пака HEAD в `.tmp/u21-pack/pack-before.dat`. Папка `.tmp/u21-pack/HM/`: атлас `HM_UNIT_LAUNCHER` из `.tmp/u21-build/final` и `atlases.json` в формате, который пишет `build`, только с этой записью. Установи её командой `install.py`. Скриптом сверь с копией: число и порядок записей те же; изменилась ровно одна запись — `HM_UNIT_LAUNCHER`, её размер прежний; остальные равны байт в байт.
11. **Лист итога** `.tmp/u21-sheets/final.png`: строки `DEVIATOR`, `LAUNCHER old`, `LAUNCHER new` для каждого из трёх Домов (9 строк), столбцы k0…k7, кадр покрашен по формуле из «Что есть», фон RGB (70, 68, 64), масштаб 2:1.
12. **Тесты.** Прогон `tools/units3d/tests` (`/srv/dune/venv/bin/python -m unittest`, каждый метод — отдельным процессом, `xargs -P 16`, `D2TM_PACK_DIR=$PWD/resources/bin/data`); логи — в `.tmp/u21-tests/`. Тест, который падает и на HEAD (прогон до пункта 10), — назови в сдаче, не чини. Тест, который падает только после правки, — назови со строками вывода; тест не меняй.

## Что не трогать

- Код движка (`src/`), инструменты `tools/units3d/*.py`, существующие тесты, папку `/srv/dune/gen`, атласы тела и тени Ракетницы, все записи пака, кроме `HM_UNIT_LAUNCHER`.

## Организация работы

- Порядок: `PLAN-U21` → пункты 1 и 2 → пункт 3 → пункт 4 → пункт 5 → пункт 6 → сдача `DONE-U21-A` → ответ ведущего → пункт 8 → пункт 9 → пункт 10 → пункты 11 и 12 → сдача `DONE-U21`.
- Параллельно: пункт 2 — пока идут генерации; генерации разных направлений (пункт 3) — по 4 одновременно, пока случаи не кончатся; замеры готовой попытки (пункт 4) — пока генерируются другие; четыре пробные сборки (пункт 5) независимы; прогон тестов на HEAD (пункт 12) — в любой момент до пункта 10.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации (каждому — свой список случаев; в бриф — промпты дословно, правило копирования ответа, правила повтора и отказа модерации), входы, замеры, сборки, листы, пак и сверки, прогон тестов; сам — план, итоговая сверка, сдачи. Облик не оценивай: выбор — за ведущим по листам.
- Остановки: после `PLAN-U21` до `PLAN-OK-U21`; на `Q-U21-01`, `Q-U21-02` до ответа ведущего; на `DONE-U21-A` до ответа ведущего с выбором; на сдаче `DONE-U21`.
- Рамка правок: `tools/units3d/units/UNIT_LAUNCHER/unit.json`, `codex-direct/U3/gen/UNIT_LAUNCHER.SHA256SUMS`, `resources/bin/data/sdl_data_hd4.dat`, временные файлы в `.tmp/`.
- Журнал хода: `.tmp/progress-u21.md`, строка после каждого пункта порядка и после каждого готового субагента.

## Сдача

Части А — блок `## DONE-U21-A`, части Б — блок `## DONE-U21` по формату сдачи из правил ниже. В `DONE-U21` дополнительно: `M` и новый `share_corridor`; `share` восьми кадров финальной сборки; строки сверки пункта 10; путь `final.png`; список коммитов — два: описание и суммы; пак.
