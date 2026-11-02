## PLAN-U9-I2-C

Для записи: сверить шесть находок с ожидаемыми исправлениями и пункты 1–6 с `TASK-impl2.md`; проверить весь дифф и новые тесты. Движок и инструмент с контрактом прочитаны двумя помощниками `gpt-6-luna` `xhigh`; решения вынесены мной. Проверка использует `git`, чтение файлов и читающие Python-скрипты. Записывается только `.tmp/progress-u9i2c.md`; сборки, тесты и мутанты не запускаются. Обязательные документы и коммиты доступны. Выполнен один круг самоаудита.

## DONE-U9-I2-C | 2026-11-02 13:24:37 UTC | HEAD e0c9e67c366e63ef73385af30f4ca9438c31f460

### Пункты

Все номера строк ниже относятся к `814f380f`. Обозначения: **А** — находка аудита, **П** — пункт задания.

| Номер | Решение | Доказательство |
|---|---|---|
| А1 | закрыт | [cUnit.cpp:795](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:795): вызов `unitWorldScaleFactor` и его аргументы совпадают с `getVisualRectangle()` на строке 541. |
| А2 | закрыт частично | [unit_contract.py:742](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:742) возвращает источник обычной ветки. Однако регулярное выражение на строке 721 читает целочисленный префикс: HD-смещение `24.5F` будет принято за `24`, и сравнение на строке 737 пропустит различие с обычным смещением `24`. Ожидается ошибка при различающихся смещениях, включая дробное HD-смещение. Причина: **исполнитель**. |
| А3 | закрыт | [unit_contract.py:942](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:942): источники включают оба метода для тени, корпуса и башни. Все шесть ссылок присутствуют в [unit_contract.json:16087](/srv/dune/worktrees/u9f/docs/units/unit_contract.json:16087). |
| А4 | закрыт | [cIniGameRessouces.cpp:38](/srv/dune/worktrees/u9f/src/utils/cIniGameRessouces.cpp:38): оба HD-размера обнуляются рядом с BMP-размерами. |
| А5 | закрыт | [redraw_common.py:302](/srv/dune/worktrees/u9f/tools/units3d/redraw_common.py:302): без `reference_frame` восстановлено сообщение `frame/rows: cells exceed body atlas`. |
| А6 | закрыт | [structs.h:276](/srv/dune/worktrees/u9f/src/include/structs.h:276): после `};` нет LF, как в `cf757ad7`. Сравнение с `cf757ad7` показывает только добавление двух HD-полей. |
| П1 | закрыт | Валидация — [redraw_common.py:188](/srv/dune/worktrees/u9f/tools/units3d/redraw_common.py:188). Произведение масштабов — [redraw_build.py:65](/srv/dune/worktrees/u9f/tools/units3d/redraw_build.py:65); применяется к телу, recolour, очищенному цвету и белой маске на строках 92, 107, 145, 157, 169. Выбор медианного, явного и `fit`-масштаба сохранён на строках 114–117. |
| П2 | закрыт | [test_redraw_frame_scale.py:106](/srv/dune/worktrees/u9f/tools/units3d/tests/test_redraw_frame_scale.py:106): проверяются все выходные файлы для отсутствующего поля и множителя 1; размеры тела и маски — строки 135 и 159; остальные направления — 177; недопустимые значения и stderr — 180–193. Сохранённые логи подтверждают провалы всех трёх требуемых мутаций. |
| П3 | закрыт | [unit.json:72](/srv/dune/worktrees/u9f/tools/units3d/units/UNIT_SIEGEBASE/unit.json:72) и [unit.json:113](/srv/dune/worktrees/u9f/tools/units3d/units/UNIT_SIEGEBASE/unit.json:113): множители `0.84` и `0.89`. После удаления этих двух полей описания корпуса и башни совпадают с исходными. |
| П4 | закрыт | `814f380f:resources/bin/data/sdl_data_hd4.dat:2` содержит LFS SHA-256 `2061b233…99d0234`; установленный пак и сохранённая проверенная копия имеют этот хэш. [Прежний лог проверки пака](/srv/dune/worktrees/u9f/.tmp/u9i2-pack-check.log:1) подтверждает размеры и payload трёх записей, неизменность остальных 238 записей и различия только k2/k6 тела, маски и тени. |
| П5 | закрыт | [cUnit.cpp:795](/srv/dune/worktrees/u9f/src/gameobjects/units/cUnit.cpp:795), [cIniGameRessouces.cpp:38](/srv/dune/worktrees/u9f/src/utils/cIniGameRessouces.cpp:38), [structs.h:276](/srv/dune/worktrees/u9f/src/include/structs.h:276): выполнены все три требования. |
| П6 | закрыт частично | Источник обычной ветки, шесть источников `draw_order`, прежнее сообщение ошибки и пересобранный контракт присутствуют: [unit_contract.py:742](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:742), строка 942; [redraw_common.py:302](/srv/dune/worktrees/u9f/tools/units3d/redraw_common.py:302); [unit_contract.json:16323](/srv/dune/worktrees/u9f/docs/units/unit_contract.json:16323). Проверка различия смещений неполна по причине А2. Ожидается отказ и при `24.5F` против `24`. Причина: **исполнитель**. |

Для П2 прочитаны прежние логи мутаций: `ignore` — `AssertionError: 8 not less than or equal to 1`; `all` — `AssertionError: False is not true`; `no-mask` — `AssertionError: 2 not less than or equal to 1`. Новых запусков не было.

### Новые находки

1. **Н1 — потеря источников в Markdown-контракте.**  
   [UNIT_CONTRACT.md:78](/srv/dune/worktrees/u9f/docs/units/UNIT_CONTRACT.md:78), [unit_contract.py:942](/srv/dune/worktrees/u9f/tools/units3d/unit_contract.py:942). После расширения списка источников ограничение на первые три ссылки на строке 1672 оставляет только shadow-HD, shadow-classic и body-HD. Прежняя ссылка на башню исчезла; body-classic также не показан. Это изменение результата генератора заданием не требуется. Ожидается сохранить представление всех трёх слоёв и обеих веток. Тяжесть: **не блокирует**. Причина: **исполнитель**.

2. **Н2 — тест различия смещений допускает неправильное сравнение.**  
   [test_unit_contract_branches.py:43](/srv/dune/worktrees/u9f/tools/units3d/tests/test_unit_contract_branches.py:43). Проверяется только `31 > 24`. Неверная реализация с заменой `!=` на `>` в `unit_contract.py:737` пройдёт все новые тесты ветвей, но пропустит HD-смещение `23` против обычного `24`. Ожидается проверка различия в обоих направлениях. Тяжесть: **не блокирует**. Причина: **приёмочный тест**.

3. **Н3 — fit-тест не различает обрезку тела и recolour.**  
   [test_redraw_frame_scale.py:225](/srv/dune/worktrees/u9f/tools/units3d/tests/test_redraw_frame_scale.py:225): body и recolour имеют одинаковую геометрию. Неверная реализация без проверки recolour в `fits()` (`redraw_build.py:104–111`) пройдёт тест: решение определит обрезка тела. Ожидается случай, где тело помещается, а recolour ограничивает выбранный масштаб. Тяжесть: **не блокирует**. Причина: **приёмочный тест**.

Контрпримеры Н2 и Н3 установлены чтением кода; мутанты не запускались.

### Вердикт

**ДОРАБОТКА — находка А2 и пункт П6 закрыты частично.** Проверка смещений должна обнаруживать различие полных значений, а не только целочисленных префиксов.

### Коммиты

нет

### Не проверено

Сборки, CTest, Python-тесты, мутантные реализации и игра не запускались согласно заданию. Прежние логи использованы как сохранённые свидетельства, без утверждения о повторном прогоне.

### git status --short

Вывод пуст.

### Владельцу

Файлы репозитория не изменены. Требуется доработать сравнение смещений CARRYALL; новые находки Н1–Н3 неблокирующие. Проверка завершена, цель оставлена активной до приёмки.