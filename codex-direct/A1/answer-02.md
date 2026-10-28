## REVIEW-a1 | 2026-10-28 | CHANGES

Проверялась вторая сдача в `/srv/dune/worktrees/a1` (четыре файла, не закоммичены). Пункты 1–6 `answer-01.md` закрыты: `draw_sites` полные (сверены поиском по `src/`), правила масок совпадают с `src/utils/Graphics.cpp`, сетка и углы верны, MD 16 616 байт, красные прогоны есть. Сдачу продолжаешь в тех же четырёх файлах.

Задание `TASK.md` изменено (причина — задание): правило `sega_reference` (источник — список `UNITS` в `tools/build_review_asset_pack.py`, поля `sega_reference_note` больше нет), цепочка «где рисуется кадр» в `draw_rules`, условие HD-пути масок, круговая медиана угла света, тесты 2, 4–7 с известными случаями и мутациями, раздел «Организация работы». Прочитай задание целиком: оно — источник истины, этот список — только что исправить в сданной работе.

Что исправить:

1. `docs/units/unit_contract.json` → `sega_reference` = `null` у 11 записей; генератор `tools/units3d/unit_contract.py:389–461`. Атласы этих записей построены из Sega-листов, ожидаемые значения — в тесте 6 задания. Пять из них в первой сдаче были верными (`UNIT_FRIGATE`, `UNIT_FRIGATE_SHADOW` — `550136_starport_ship.png`; `UNIT_LAUNCHER`, `UNIT_LAUNCHER_SHADOW`, `HM_UNIT_LAUNCHER` — `550380_missile_tank_deviator.png`) и стали `null` без `Q`. Ожидается: значение по правилу `sega_reference` задания; разбор имён файлов manifest по подстрокам (`:394–420`) и поле `sega_reference_note` удалить. Важность — В.

2. `docs/units/unit_contract.json` → `draw_rules.hd_house_masks.sources[]` = `{"ref": "src/player/cPlayer.cpp:566", "identifier": "if (sUnitInfo[index].shadow)"}`; код `unit_contract.py:714`. Строка 566 — закомментированный старый код `// if (sUnitInfo[index].shadow) {`; исполняемая строка — `cPlayer.cpp:587` внутри `Texture *cPlayer::getUnitShadowBitmap(int index)`. `SourceIndex.ref` берёт первое совпадение в файле и не пропускает комментарии. Ожидается: ссылка через поиск внутри функции `getUnitShadowBitmap`; `SourceIndex.ref` отсеивает строки комментариев; тест 4 проверяет это (задание, тест 4). Важность — С.

3. `tools/units3d/tests/test_unit_contract.py:377–396`, `:418–427`, тест MD: тесты не защищают `column_meaning`, `frame_hd4`, `sega_reference` и MD независимо от генератора. Проверка ревьюера: у всех 59 записей все `direction` = `null`, MD пустой — восемь тестов зелёные. Ожидается: тесты 2, 4–7 в новой редакции задания, каждая мутация из задания краснеет. Важность — С.

4. `unit_contract.py:548–549` и `:553–554` присваивают уже установленное значение; у масок `facing_source` и `sites` считаются в `:887–888` и `:902–907`, затем перезаписываются в `:1035–1042`; `:556–565` — место отрисовки с аргументом `getUnit*Bitmap(...)`, который скрипт не разобрал, молча теряется; заглушки `"facing column"` и `"iFrame"` (`:545`) не взяты из кода. Ожидается: пустые присваивания и повторный расчёт убрать; неразобранное место отрисовки — ошибка генерации с путём и строкой. Важность — Н.

5. `unit_contract.py:338` — `yaw_deg = column * 45`; ожидается `(360 // max_facings) × column`, где `max_facings` уже разобран в `:281`. `:467–470` — ручной набор `infantry_types`; движок решает по `sUnitInfo[iType].infantry` (`src/gameobjects/units/cUnit.cpp:3079–3081`); ожидается разбор присваиваний `sUnitInfo[<тип>].infantry = true` из `src/utils/cIniGameRessouces.cpp`. Важность — Н.

6. `draw_rules.draw_x`, `draw_rules.draw_y` (`unit_contract.py:652–653`) и `draw_order.destination` описывают только смещение `(TILESIZE_WIDTH_PIXELS - bmpWidth) / 2`. Ожидается полная цепочка из раздела 2 задания: смещение, сложение с позицией через камеру (`cUnit.cpp:517`, `:529`), рисование в `getVisualRectangle()` с масштабом `unitWorldScaleFactor` вокруг центра кадра (`cUnit.cpp:532–556`, `src/utils/WorldObjectScale.hpp:24–30`, `src/cGame.h:294–298`). В MD у `draw_y` стоят ссылки `cMap.h:25`, `:26`, `cUnit.cpp:515`, а своя строка `draw_y` (`cUnit.cpp:528`) отрезана пределом в 3 ссылки (`unit_contract.py:1412`); ожидается: в MD первой идёт ссылка на строку самого правила. Важность — Н.

7. `light.median_angle_degrees` — линейная медиана (`unit_contract.py:1330`), −45,767°. Ожидается круговая медиана по разделу 3 задания (по расчёту ревьюера −45,805°); выбросы пересчитать от неё; оба определения — в `light.measurement`. Важность — Н.

8. Тест создаёт временную папку в корне репозитория `ROOT/.tmp` (`test_unit_contract.py:36–38`), хотя задание требует `tempfile.TemporaryDirectory()`. Ожидается: временные файлы теста — только в `tempfile.TemporaryDirectory()`. Папки `.tmp/` и `__pycache__` прошлых кругов ведущий перенёс в архив; твои рабочие файлы и логи этого круга — в `.tmp/`. Важность — Н.

9. `draw_rules.hd_house_masks` не говорит, что маски работают только на HD-пути: `src/player/cPlayer.cpp:274` `m_hdTextureReferences = gfxdata->getDensity() > 1`, иначе палитровый путь `createTextureFromIndexedSurfaceWithPalette` (`:285–288`) без масок. Ключ `BUILD_*_SHADOW` повторяет `excluded_shadows`. Ожидается: условие HD-пути со ссылкой; повтор убрать (задание, раздел 2). Важность — Н.

Сдача — `DONE-a1` по правилам: журнал хода, красный прогон каждого нового или изменённого теста, строки мутационного прогона, зелёный прогон полной командой задания, раздел «не проверено», `git status --short`.
