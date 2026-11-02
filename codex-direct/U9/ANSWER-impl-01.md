# Задание U9-I, ход 01: ответ ведущего на Q-U9-I-01

Прочитай цель нити (`get_goal`) и работай по ней.

## Ответ на Q-U9-I-01

Пять ошибок — в заглушках юнита старых тестов, а не в инструменте. Классы `UnitFixture` в `tools/units3d/tests/test_redraw_shadow.py:17` и `tools/units3d/tests/test_redraw_sheets.py:15` подменяют класс описания юнита из `tools/units3d/redraw_common.py`. У настоящего класса появились свойства `reference_frame` и `anchor_shift`, а у заглушек их нет. Для описания без полей `reference_frame` и `reference_anchor` настоящий класс даёт `reference_frame` = `frame` и `anchor_shift` = (0, 0).

Разрешена одна правка тестов вне замороженного списка — заглушки получают эти значения по умолчанию:

1. `tools/units3d/tests/test_redraw_shadow.py`, конструктор `UnitFixture`: строка `self.reference_frame = frame` после `self.frame = frame`.
2. `tools/units3d/tests/test_redraw_sheets.py`, конструктор `UnitFixture`: строка `self.anchor_shift = (0, 0)` после `self.frame = frame`.

Других строк в этих двух файлах не меняй: ожидания тестов, вызовы `UnitFixture(...)` и данные остаются прежними. Код инструмента под заглушки не меняй: значение по умолчанию через `getattr` в `redraw_shadow.py` и `redraw_sheets.py` не добавлять.

## Чем проверить

- Прогон двух файлов: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.tmp/unittest-tmp" D2TM_PACK_DIR="$PWD/resources/bin/data" /srv/dune/venv/bin/python -m unittest discover -s tools/units3d/tests -p "test_redraw_s*.py" -v` — все тесты `OK`.
- Затем полный Python-прогон командой из задания — `OK`, пропущенных 0.
- `git diff -- tools/units3d/tests/test_redraw_shadow.py tools/units3d/tests/test_redraw_sheets.py` — ровно две добавленные строки; вывод — в сдаче.
- Суммы `sha256sum -c /srv/dune/tasks/u9-impl/frozen.sha256` и `sha256sum -c tools/units3d/tests/ACCEPTANCE.sha256` — все `OK`.

## Организация работы

- Порядок: правка двух заглушек → прогон двух файлов → полный Python-прогон → суммы → самоаудит одним кругом → сдача `DONE-U9-I` по разделу «Сдача» задания `/srv/dune/tasks/u9-impl/task.md`. Сборку и CTest не повторяй: код C++ после прошлого прогона не менялся.
- Параллельно: нет, шаги идут по очереди.
- Помощники: субагент `gpt-6-luna` `xhigh` — прогоны и выжимки логов.
- Остановки — блок `## Q-U9-I-NN` и стоп: после правки заглушек падает любой тест; остальные остановки — из задания.
- Журнал хода: строка в `.tmp/progress.md` после каждого шага.
- Рамка правок: две строки из раздела «Ответ»; остальное — рамка задания.
- Комментарии в коде. Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.
