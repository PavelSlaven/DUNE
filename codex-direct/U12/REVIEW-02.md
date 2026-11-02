# REVIEW-U12-02

Твоя сдача `## DONE-U12-R1` проверена скриптами ведущего (пять файлов; строка Осадного равна `814f380f`; суммы OK; новых `u12-offset-*.log` нет; три изменённых тестовых файла — 21 тест OK) и отдельной нитью Codex `gpt-6.1-sol` по коду. Нить нашла три слабых места новых тестов. Пункты 1, 2, 5 и 6 прошлого возврата закрыты.

Режим этого хода: механические правки, продиктованные дословно, — план не нужен, начинай сразу. Рабочая копия та же, HEAD `34d51060`, правки R1 не закоммичены — оставь их. Не коммить.

## Что исправить

1. **Число направлений в новых тестах `rotation`.** `tools/units3d/tests/test_redraw_rotation.py`: в методе `test_uniform_deviation_is_normalised` сразу после строки `results = size_measurements(new_area, reference_areas)` и в методе `test_opposite_support_does_not_agree` сразу после строки `results = size_case((1.40, 1.00, 0.94))` вставь строку `self.assertEqual(len(results), 8)` с отступом тела метода. Других правок в файле нет. Неверная реализация, которую это ловит: `size_measurements` возвращает `result[:1]` вместо `result`.

2. **Проверка текста исключения в `compose`.** `tools/units3d/tests/test_squad_compose_shift.py:159`: замени строку

   ```python
                   self.assertIn("shift: ожидается", completed.stderr, invalid_shift)
   ```

   на

   ```python
                   self.assertTrue(
                       any(line.startswith("ValueError: shift: ожидается")
                           for line in completed.stderr.splitlines()),
                       completed.stderr,
                   )
   ```

   Причина: `compose.py` не перехватывает `ValueError`, и при любом другом исключении трассировка печатает исходную строку с тем же текстом; строка, начинающаяся с `ValueError: `, бывает только у самого исключения.

3. **Выход за клетку — с маской и без маски.** В методе `test_shift_outside_cell_is_rejected` того же файла замени весь блок от строки `completed = subprocess.run(` (строка 178) до строки `self.assertIn("alpha вне клетки", completed.stderr)` (строка 198) включительно на:

   ```python
               for mode, source, extra in (
                   ("mask", mask_source, ["--mask"]),
                   ("body", body_source, []),
               ):
                   completed = subprocess.run(
                       [
                           sys.executable, str(COMPOSE_PATH), "compose",
                           "--squad", "UNIT_SOLDIERS",
                           "--source", str(source),
                           "--body", str(body_source),
                           *extra,
                           "--placements", str(placements_path),
                           "--out-root", str(temporary / f"outside-{mode}-root"),
                           "--output", str(temporary / f"outside-{mode}.png"),
                           "--sheet", str(temporary / f"outside-{mode}-sheet.png"),
                           "--report", str(temporary / f"outside-{mode}-checks.json"),
                       ],
                       cwd=ROOT,
                       capture_output=True,
                       text=True,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                       check=False,
                   )
                   self.assertNotEqual(completed.returncode, 0, mode)
                   self.assertTrue(
                       any(line.startswith("ValueError: alpha вне клетки")
                           for line in completed.stderr.splitlines()),
                       completed.stderr,
                   )
   ```

   Отступ блока — как у заменяемых строк (внутри `with`). Сообщение `ValueError` из `codex-direct/U6/squads/compose.py:478` может быть многострочным, поэтому проверяется любая строка stderr, а не последняя.

## Чем проверить

- Три неверные реализации, каждая в своей копии модуля в `.tmp/u12-r2-mutants/<имя>/`; приложи строку провала каждой:
  - `rotation-first-only`: в `size_measurements` (`tools/units3d/redraw_rotation.py:70`) `return result[:1]` — должны упасть оба метода из пункта 1;
  - `compose-keyerror`: в `compose.py:430` `item['piece']` заменено на `item['piece_id']` — должен упасть `test_shift_outside_cell_is_rejected`;
  - `compose-bounds-mask-only`: строка `compose.py:428` заменена на `if args.mask and (moved[0] < 0 or moved[1] < 0 or moved[2] > CELL or moved[3] > CELL):` — скобки обязательны — должен упасть `test_shift_outside_cell_is_rejected` на режиме `body`.
- Рабочая версия: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.tmp/unittest-tmp" D2TM_PACK_DIR="$PWD/resources/bin/data" /srv/dune/venv/bin/python -m unittest tools/units3d/tests/test_redraw_rotation.py tools/units3d/tests/test_squad_compose_shift.py -v` — `OK`.
- `sha256sum -c /srv/dune/tasks/u12/frozen.sha256` и `sha256sum -c tools/units3d/tests/ACCEPTANCE.sha256` — все строки `OK`; `git diff --check 34d51060` — пусто.
- Полный прогон Python не нужен: этот ход меняет только два тестовых файла.

## Организация работы

- Порядок: пункты 1–3 → три неверные реализации → проверки → сдача `## DONE-U12-R2` по разделу «Сдача» правил задания.
- Параллельно: пункт 1 и неверная реализация `rotation-first-only` (`test_redraw_rotation.py`) не зависят от пунктов 2–3 и двух неверных реализаций `compose` (`test_squad_compose_shift.py`) — отдай их двум субагентам `gpt-6-luna` `xhigh` одновременно.
- Помощники: субагенты `gpt-6-luna` `xhigh` — правки по тексту пунктов, прогоны, выжимки логов; сверка с пунктами — твоя.
- Рамка правок: `tools/units3d/tests/test_redraw_rotation.py`, `tools/units3d/tests/test_squad_compose_shift.py`; временное — в `.tmp/`.
- Остановки — блок `## Q-U12-R2-NN` и стоп: рабочая версия не проходит тесты; неверная реализация проходит; вставка не ложится на строки, названные в пунктах.
- Журнал хода: `.tmp/progress.md`, строка после каждого пункта и каждого прогона.
- Git: перед командами `git` выполни `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.
- Комментарии в коде. Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.
