# Выборочная сверка разведки P5TR (Haiku)

Ревизии: форк `9208dcf5a358f40afd95c99480e4e09f781ed566` (далее `$F`), порт `5e9059778bd59e486a58a899c9cf56f6758ed178` (далее `$P`).
Команды выполнены на servak: `ssh servak 'cd /srv/dune/worktrees/u13g && export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && <команда>'`, только чтение.

Оговорки:
- Факт 9: команда к полю «места в src/debug» в таблице не указана. Повторена как `git grep -n '"false"' $F -- src/debug`.
- Факт 15: для просмотра заголовка `scenes.tsv` один раз запущено `head -3 ... | cat -A | cut -c1-200`. `cat` и `cut` не входят в список разрешённых команд брифа. Команда только читает; вердикт опирается на `grep -cP`.
- Точная проверка строк: `git show $F:<путь> | sed -n Np | grep -Fxc '<текст из факта>'`; вывод `1` означает полное совпадение.
- Поля «функция» (факты 6–8, 11, 12) проверены по границам `def` и `class`: `git show $F:<путь> | grep -n "def \|^class "`.
- Класс импорта: `git cat-file -t $F:tools/ui-audit/<модуль>.py` и `/usr/bin/python3 -c 'import sys; print("<модуль>" in sys.stdlib_module_names)'` (через `ssh servak "..."`).
- Сокращения в выводах отмечены в тексте.

## Факт 1

Команды и выводы:
- `git show $F:tools/ui-audit/tests/test_check_options_geometry.py | sed -n 3p` → `import tempfile`. Модуль `tempfile` совпадает.
- `git cat-file -t $F:tools/ui-audit/tempfile.py` → `fatal: path 'tools/ui-audit/tempfile.py' does not exist in '9208dcf5a358f40afd95c99480e4e09f781ed566'`. Своего модуля нет.
- `ssh servak "/usr/bin/python3 -c 'import sys; print(\"tempfile\" in sys.stdlib_module_names)'"` → `True`. Класс «стандартный» совпадает.

Не проверено: «строк в файле: 137» (нет ссылки и команды), «/usr/bin/python3» и «venv» (пустые поля), строка 115 таблицы.

Итог: совпало.

## Факт 2

Команды и выводы:
- `git show $F:tools/ui-audit/run_all.py | sed -n 9p` → `from pathlib import Path`. Модуль `pathlib` совпадает.
- `git cat-file -t $F:tools/ui-audit/pathlib.py` → `fatal: path 'tools/ui-audit/pathlib.py' does not exist in '9208dcf5a358f40afd95c99480e4e09f781ed566'`. Своего модуля нет.
- `ssh servak "/usr/bin/python3 -c 'import sys; print(\"pathlib\" in sys.stdlib_module_names)'"` → `True`. Класс «стандартный» совпадает.

Не проверено: «строк в файле: 152» (нет ссылки и команды), «/usr/bin/python3» и «venv» (пустые поля), строка 70 таблицы.

Итог: совпало.

## Факт 3

Команды и выводы:
- `git show $F:tools/ui-audit/check_options_geometry.py | sed -n 101p | grep -Fxc '    plan.add_argument("--plan", help="audit-plan.json emitted by run_all.py")'` → `1`.
- Строка 101: `    plan.add_argument("--plan", help="audit-plan.json emitted by run_all.py")`. Совпадает с фактом дословно.

Не проверено: вид «аргумент» (нет ссылки и команды), строка 46 таблицы.

Итог: совпало.

## Факт 4

Команды и выводы:
- `git show $F:tools/ui-audit/build_sheets.py | sed -n 241p | grep -Fxc '    parser.add_argument("--order", help="order.json written by run_all.py")'` → `1`.
- Строка 241: `    parser.add_argument("--order", help="order.json written by run_all.py")`. Совпадает с фактом дословно.

Не проверено: вид «аргумент» (нет ссылки и команды), строка 22 таблицы.

Итог: совпало.

## Факт 5

Команды и выводы:
- `git show $F:tools/ui-audit/check_screens.py | sed -n 74p | grep -Fxc '    parser.add_argument("--exclusions", required=True)'` → `1`.
- Строка 74: `    parser.add_argument("--exclusions", required=True)`. Совпадает с фактом дословно.

Не проверено: вид «аргумент» (нет ссылки и команды), строка 60 таблицы.

Итог: совпало.

## Факт 6

Команды и выводы:
- `git show $F:tools/ui-audit/finalize_png.py | sed -n 20p | grep -Fxc '        have = {path.stem for path in png_dir.glob("*.png")} if png_dir.is_dir() else set()'` → `1`.
- `git show $F:tools/ui-audit/finalize_png.py | grep -n "def \|^class "` → `13:def plan_actions(out_root, flags, ordered_ids):`, `27:def main(argv=None):`. Строка 20 лежит между 13 и 27, то есть внутри `plan_actions`.

Не проверено: строка 42 таблицы.

Итог: совпало.

## Факт 7

Команды и выводы:
- `git show $F:tools/ui-audit/run_combo.py | sed -n 134p | grep -Fxc '            except subprocess.TimeoutExpired:'` → `1`.
- `git show $F:tools/ui-audit/run_combo.py | grep -n "def \|^class "` → `107:def run_combo(...)`, `152:def main(argv=None):`. Строка 134 лежит между 107 и 152, то есть внутри `run_combo`. Выписаны только две строки из 15 (сокращение).

Не проверено: строка 76 таблицы.

Итог: совпало.

## Факт 8

Команды и выводы:
- `git show $F:tools/ui-audit/check_credits.py | sed -n 9p | grep -Fxc '    records = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]'` → `1`.
- `git show $F:tools/ui-audit/check_credits.py | grep -n "def \|^class "` → `8:def load(path):`, `13:def line_covered(line, texts):`. Строка 9 лежит внутри `load`. Выписаны только две строки из 4 (сокращение).

Не проверено: строка 16 таблицы.

Итог: совпало.

## Факт 9

Команды и выводы:
- `git show $F:tools/ui-audit/run_combo.py | sed -n 58p` → `        "FullScreen": "false",`. Значение `false` есть в строке 58.
- `git grep -n '"false"' $F -- src/debug | head -20` → 3 строки (сокращено: вырезаны фрагменты вокруг литерала):
  - `src/debug/UiAuditCapture.cpp:163: ... << (g_scene->gameScreen ? "true" : "false")`
  - `src/debug/UiAuditCapture.cpp:405: ... + (scene.gameScreen ? "true" : "false") + ... + (scene.hud ? "true" : "false") +`
  - `src/debug/UiAuditCapture.cpp:406: ... + (scene.hdOnly ? "true" : "false") + ",\"hover\":";`

Сравнение: три места совпадают с фактом по номеру строки и тексту. В факте строки склеены разделителем `; `, поэтому видны лишние `;`.

Не проверено: строка 25 таблицы.

Итог: совпало.

## Факт 10

Команды и выводы:
- `git show $F:tools/ui-audit/run_combo.py | sed -n 135p` → `                message = "timeout"`. Значение `timeout` есть в строке 135.

Не проверено: «места в src/debug: нет» (нет команды), строка 98 таблицы.

Итог: совпало.

## Факт 11

Команды и выводы:
- `git show $F:tools/ui-audit/run_all.py | sed -n 22p` → `        result = subprocess.run([str(executable), "--ui-audit-scales", resolution], env=run_combo.game_environment(),`. Литерал `--ui-audit-scales` есть в строке 22.
- `git show $F:tools/ui-audit/run_all.py | grep -n "def \|^class "` → `19:def scales_for(executable, resolutions):`, `29:def interleave(chains):`. Строка 22 лежит внутри `scales_for`.

Не проверено: «значение: нет» (нет команды), строка 20 таблицы.

Итог: совпало.

## Факт 12

Команды и выводы:
- `git show $F:tools/ui-audit/finalize_png.py | sed -n 32p` → `    parser.add_argument("--out", required=True)`. Литерал `--out` есть в строке 32.
- `git show $F:tools/ui-audit/finalize_png.py | grep -n "def \|^class "` → `13:def plan_actions(...)`, `27:def main(argv=None):`. Строка 32 лежит внутри `main`.

Не проверено: «значение: нет» (нет команды), строка 12 таблицы.

Итог: совпало.

## Факт 13

Команды и выводы:
- `git show $F:tools/ui-audit/find_hit_tests.py | sed -n 8p` → `DIRECTORIES = ("src/gui", "src/drawers", "src/gamestates", "src/managers", "src/save", "src/sidebar", "src/mentat",`. Литерал `"src/managers"` есть в строке 8.
- `git cat-file -t $F:src/managers` → `tree`. Совпадает с FORK1 `tree`.
- `git cat-file -t $P:src/managers` → `tree`. Совпадает с PORT `tree`.

Не проверено: строка 9 таблицы.

Итог: совпало.

## Факт 14

Команды и выводы:
- `git show $F:tools/ui-audit/find_hit_tests.py | sed -n 9p` → `               "src/controls", "src/debug")`. Литерал `"src/debug"` есть в строке 9.
- `git cat-file -t $F:src/debug` → `tree`. Совпадает с FORK1 `tree`.
- `git cat-file -t $P:src/debug` → `fatal: path 'src/debug' exists on disk, but not in '5e9059778bd59e486a58a899c9cf56f6758ed178'`. В порте объекта нет, значит PORT «нет» совпадает.

Не проверено: строка 14 таблицы.

Итог: совпало.

## Факт 15

Команды и выводы:
- `git show $F:tools/ui-audit/check_options_geometry.py | sed -n 12p` → `    "options-menu-main",`. Значение есть в строке 12.
- `grep -cP '^options-menu-main\t' /srv/dune/worktrees/u13g/.tmp/p5dr/scenes.tsv` → `1`. Совпадение по первому столбцу (критерий «сцена»). Заголовок начинается с «сцена» и не совпадает. Всего строк в файле `sed -n '$='` → `158` (заголовок входит в эту цифру, в счёт не попадает).

Не проверено: строка 6 таблицы.

Итог: совпало.

---

Итог: совпало 15 из 15.
