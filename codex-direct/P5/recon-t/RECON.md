## RECON-P5TR | Wed Nov 11 10:16:37 UTC 2026

Разведка по FORK1 `9208dcf` и PORT `5e90597`; файлы таблиц, журналы команд и полный вывод прогонов приведены ниже. Таблицы ссылаются на строки исходников указанного коммита.

## Чтение

Полностью прочитан `.tmp/p5gr/runtime.tsv` отдельным вызовом `cat`. Полностью прочитан `.tmp/p5dr/scenes.tsv`: после усечённого начального вывода дочитан диапазонами `sed -n` до строки 158 включительно; файл содержит заголовок и 157 сцен. Дополнительные нормы, контракты или правила, необходимые для выполнения задания, в прочитанных материалах не обнаружены.

## 1. Импорты и интерфейс

Команды и выводы извлечения импортов, числа строк и проверки стороннего модуля:

#### lane1.commands.log

~~~~text
Command: python3 .tmp/p5tr/lane1.py
Output:
Инструментов: 14
Тестов инструментов: 15
Строк imports.tsv без заголовка: 174
Строк interface.tsv без заголовка: 101
Уникальных значений fields.tsv без заголовка: 107
Строк scene-refs.tsv без заголовка: 9
Сторонние модули: PIL
Строк сцен в scenes.tsv без заголовка: 157
Всего уникальных строковых значений по шаблону fields: 107
Всего строковых литералов в инструментах: 864

Detailed wc and third-party import command outputs: lane1.imports.log
Detailed git grep commands and outputs: lane1.gitgrep.log
~~~~

#### lane1.imports.log

~~~~text
Command: wc -l /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/build_sheets.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_completeness.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_credits.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_geometry.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_keys.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_options_geometry.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_scenes.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_screens.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/combos.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/extract_keys.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/finalize_png.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/find_hit_tests.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/run_all.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/run_combo.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_build_sheets.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_completeness.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_credits.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_geometry.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_keys.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_options_geometry.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_scenes.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_screens.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_combos.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_extra_rules.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_extract_keys.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_find_hit_tests.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_png_policy.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_png_policy_outputs.py /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_run_all.py
Command: /usr/bin/python3 -c 'import sys; print("\n".join(sys.stdlib_module_names))'
stdlib_module_names count=290
   261 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/build_sheets.py
    73 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_completeness.py
    53 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_credits.py
   251 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_geometry.py
   126 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_keys.py
   120 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_options_geometry.py
   132 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_scenes.py
    86 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/check_screens.py
   100 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/combos.py
    92 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/extract_keys.py
    59 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/finalize_png.py
    58 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/find_hit_tests.py
   152 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/run_all.py
   184 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/run_combo.py
   117 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_build_sheets.py
   139 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_completeness.py
    53 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_credits.py
   326 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_geometry.py
   173 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_keys.py
   137 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_options_geometry.py
   166 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_scenes.py
    97 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_check_screens.py
   170 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_combos.py
   203 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_extra_rules.py
    74 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_extract_keys.py
    70 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_find_hit_tests.py
    93 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_png_policy.py
    97 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_png_policy_outputs.py
    70 /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_run_all.py
  3732 total
Third-party import probes use the specified interpreter executable and -c import command.
Command: /usr/bin/python3 -c 'import PIL'
exit=0
first_stderr_line=(пусто)
stdout=(пусто)
stderr=(пусто)
Command: /srv/dune/venv/bin/python -c 'import PIL'
exit=0
first_stderr_line=(пусто)
stdout=(пусто)
stderr=(пусто)
~~~~

Таблицы: `imports.tsv` — 174 строки данных; `interface.tsv` — 101 строка данных. Единственный сторонний модуль — `PIL`; `/usr/bin/python3 -c 'import PIL'` и `/srv/dune/venv/bin/python -c 'import PIL'` завершились с кодом 0.

#### imports.tsv

~~~~text
файл	строк в файле	путь@9208dcf:строка	модуль	класс	/usr/bin/python3	venv
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:2	argparse	стандартный		
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:3	html	стандартный		
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:4	json	стандартный		
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:5	os	стандартный		
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:6	sys	стандартный		
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:7	pathlib	стандартный		
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:9	PIL	сторонний	0; (пусто)	0; (пусто)
tools/ui-audit/build_sheets.py	261	tools/ui-audit/build_sheets.py@9208dcf:12	combos	свой		
tools/ui-audit/check_completeness.py	73	tools/ui-audit/check_completeness.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/check_completeness.py	73	tools/ui-audit/check_completeness.py@9208dcf:2	json	стандартный		
tools/ui-audit/check_completeness.py	73	tools/ui-audit/check_completeness.py@9208dcf:3	sys	стандартный		
tools/ui-audit/check_completeness.py	73	tools/ui-audit/check_completeness.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/check_completeness.py	73	tools/ui-audit/check_completeness.py@9208dcf:7	combos	свой		
tools/ui-audit/check_credits.py	53	tools/ui-audit/check_credits.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/check_credits.py	53	tools/ui-audit/check_credits.py@9208dcf:2	json	стандартный		
tools/ui-audit/check_credits.py	53	tools/ui-audit/check_credits.py@9208dcf:3	sys	стандартный		
tools/ui-audit/check_credits.py	53	tools/ui-audit/check_credits.py@9208dcf:4	collections	стандартный		
tools/ui-audit/check_credits.py	53	tools/ui-audit/check_credits.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/check_geometry.py	251	tools/ui-audit/check_geometry.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/check_geometry.py	251	tools/ui-audit/check_geometry.py@9208dcf:2	json	стандартный		
tools/ui-audit/check_geometry.py	251	tools/ui-audit/check_geometry.py@9208dcf:3	sys	стандартный		
tools/ui-audit/check_geometry.py	251	tools/ui-audit/check_geometry.py@9208dcf:4	collections	стандартный		
tools/ui-audit/check_geometry.py	251	tools/ui-audit/check_geometry.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/check_keys.py	126	tools/ui-audit/check_keys.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/check_keys.py	126	tools/ui-audit/check_keys.py@9208dcf:2	csv	стандартный		
tools/ui-audit/check_keys.py	126	tools/ui-audit/check_keys.py@9208dcf:3	sys	стандартный		
tools/ui-audit/check_keys.py	126	tools/ui-audit/check_keys.py@9208dcf:4	collections	стандартный		
tools/ui-audit/check_keys.py	126	tools/ui-audit/check_keys.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/check_options_geometry.py	120	tools/ui-audit/check_options_geometry.py@9208dcf:2	argparse	стандартный		
tools/ui-audit/check_options_geometry.py	120	tools/ui-audit/check_options_geometry.py@9208dcf:3	json	стандартный		
tools/ui-audit/check_options_geometry.py	120	tools/ui-audit/check_options_geometry.py@9208dcf:4	sys	стандартный		
tools/ui-audit/check_options_geometry.py	120	tools/ui-audit/check_options_geometry.py@9208dcf:5	collections	стандартный		
tools/ui-audit/check_options_geometry.py	120	tools/ui-audit/check_options_geometry.py@9208dcf:6	pathlib	стандартный		
tools/ui-audit/check_options_geometry.py	120	tools/ui-audit/check_options_geometry.py@9208dcf:9	check_geometry	свой		
tools/ui-audit/check_scenes.py	132	tools/ui-audit/check_scenes.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/check_scenes.py	132	tools/ui-audit/check_scenes.py@9208dcf:2	sys	стандартный		
tools/ui-audit/check_scenes.py	132	tools/ui-audit/check_scenes.py@9208dcf:3	itertools	стандартный		
tools/ui-audit/check_scenes.py	132	tools/ui-audit/check_scenes.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/check_scenes.py	132	tools/ui-audit/check_scenes.py@9208dcf:7	check_geometry	свой		
tools/ui-audit/check_screens.py	86	tools/ui-audit/check_screens.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/check_screens.py	86	tools/ui-audit/check_screens.py@9208dcf:2	json	стандартный		
tools/ui-audit/check_screens.py	86	tools/ui-audit/check_screens.py@9208dcf:3	re	стандартный		
tools/ui-audit/check_screens.py	86	tools/ui-audit/check_screens.py@9208dcf:4	sys	стандартный		
tools/ui-audit/check_screens.py	86	tools/ui-audit/check_screens.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/combos.py	100	tools/ui-audit/combos.py@9208dcf:1	json	стандартный		
tools/ui-audit/combos.py	100	tools/ui-audit/combos.py@9208dcf:2	re	стандартный		
tools/ui-audit/extract_keys.py	92	tools/ui-audit/extract_keys.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/extract_keys.py	92	tools/ui-audit/extract_keys.py@9208dcf:2	re	стандартный		
tools/ui-audit/extract_keys.py	92	tools/ui-audit/extract_keys.py@9208dcf:3	sys	стандартный		
tools/ui-audit/extract_keys.py	92	tools/ui-audit/extract_keys.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/finalize_png.py	59	tools/ui-audit/finalize_png.py@9208dcf:2	argparse	стандартный		
tools/ui-audit/finalize_png.py	59	tools/ui-audit/finalize_png.py@9208dcf:3	json	стандартный		
tools/ui-audit/finalize_png.py	59	tools/ui-audit/finalize_png.py@9208dcf:4	subprocess	стандартный		
tools/ui-audit/finalize_png.py	59	tools/ui-audit/finalize_png.py@9208dcf:5	sys	стандартный		
tools/ui-audit/finalize_png.py	59	tools/ui-audit/finalize_png.py@9208dcf:6	collections	стандартный		
tools/ui-audit/finalize_png.py	59	tools/ui-audit/finalize_png.py@9208dcf:7	pathlib	стандартный		
tools/ui-audit/finalize_png.py	59	tools/ui-audit/finalize_png.py@9208dcf:10	combos	свой		
tools/ui-audit/find_hit_tests.py	58	tools/ui-audit/find_hit_tests.py@9208dcf:1	argparse	стандартный		
tools/ui-audit/find_hit_tests.py	58	tools/ui-audit/find_hit_tests.py@9208dcf:2	re	стандартный		
tools/ui-audit/find_hit_tests.py	58	tools/ui-audit/find_hit_tests.py@9208dcf:3	sys	стандартный		
tools/ui-audit/find_hit_tests.py	58	tools/ui-audit/find_hit_tests.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:2	argparse	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:3	json	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:4	subprocess	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:5	sys	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:6	time	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:7	concurrent.futures	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:8	itertools	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:9	pathlib	стандартный		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:12	combos	свой		
tools/ui-audit/run_all.py	152	tools/ui-audit/run_all.py@9208dcf:13	run_combo	свой		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:2	argparse	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:3	json	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:4	os	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:5	re	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:6	shutil	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:7	subprocess	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:8	sys	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:9	time	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:10	pathlib	стандартный		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:13	check_geometry	свой		
tools/ui-audit/run_combo.py	184	tools/ui-audit/run_combo.py@9208dcf:14	combos	свой		
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:7	PIL	сторонний	0; (пусто)	0; (пусто)
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:11	build_sheets	свой		
tools/ui-audit/tests/test_build_sheets.py	117	tools/ui-audit/tests/test_build_sheets.py@9208dcf:12	combos	свой		
tools/ui-audit/tests/test_check_completeness.py	139	tools/ui-audit/tests/test_check_completeness.py@9208dcf:1	sys	стандартный		
tools/ui-audit/tests/test_check_completeness.py	139	tools/ui-audit/tests/test_check_completeness.py@9208dcf:2	tempfile	стандартный		
tools/ui-audit/tests/test_check_completeness.py	139	tools/ui-audit/tests/test_check_completeness.py@9208dcf:3	unittest	стандартный		
tools/ui-audit/tests/test_check_completeness.py	139	tools/ui-audit/tests/test_check_completeness.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/tests/test_check_completeness.py	139	tools/ui-audit/tests/test_check_completeness.py@9208dcf:8	check_completeness	свой		
tools/ui-audit/tests/test_check_credits.py	53	tools/ui-audit/tests/test_check_credits.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_check_credits.py	53	tools/ui-audit/tests/test_check_credits.py@9208dcf:2	tempfile	стандартный		
tools/ui-audit/tests/test_check_credits.py	53	tools/ui-audit/tests/test_check_credits.py@9208dcf:3	unittest	стандартный		
tools/ui-audit/tests/test_check_credits.py	53	tools/ui-audit/tests/test_check_credits.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/tests/test_check_credits.py	53	tools/ui-audit/tests/test_check_credits.py@9208dcf:6	check_credits	свой		
tools/ui-audit/tests/test_check_geometry.py	326	tools/ui-audit/tests/test_check_geometry.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_check_geometry.py	326	tools/ui-audit/tests/test_check_geometry.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_check_geometry.py	326	tools/ui-audit/tests/test_check_geometry.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_check_geometry.py	326	tools/ui-audit/tests/test_check_geometry.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_check_geometry.py	326	tools/ui-audit/tests/test_check_geometry.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/tests/test_check_geometry.py	326	tools/ui-audit/tests/test_check_geometry.py@9208dcf:9	check_geometry	свой		
tools/ui-audit/tests/test_check_keys.py	173	tools/ui-audit/tests/test_check_keys.py@9208dcf:1	sys	стандартный		
tools/ui-audit/tests/test_check_keys.py	173	tools/ui-audit/tests/test_check_keys.py@9208dcf:2	tempfile	стандартный		
tools/ui-audit/tests/test_check_keys.py	173	tools/ui-audit/tests/test_check_keys.py@9208dcf:3	unittest	стандартный		
tools/ui-audit/tests/test_check_keys.py	173	tools/ui-audit/tests/test_check_keys.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/tests/test_check_keys.py	173	tools/ui-audit/tests/test_check_keys.py@9208dcf:8	check_keys	свой		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:5	contextlib	стандартный		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:6	io	стандартный		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:7	pathlib	стандартный		
tools/ui-audit/tests/test_check_options_geometry.py	137	tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:11	check_options_geometry	свой		
tools/ui-audit/tests/test_check_scenes.py	166	tools/ui-audit/tests/test_check_scenes.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_check_scenes.py	166	tools/ui-audit/tests/test_check_scenes.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_check_scenes.py	166	tools/ui-audit/tests/test_check_scenes.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_check_scenes.py	166	tools/ui-audit/tests/test_check_scenes.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_check_scenes.py	166	tools/ui-audit/tests/test_check_scenes.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/tests/test_check_scenes.py	166	tools/ui-audit/tests/test_check_scenes.py@9208dcf:9	check_scenes	свой		
tools/ui-audit/tests/test_check_screens.py	97	tools/ui-audit/tests/test_check_screens.py@9208dcf:1	sys	стандартный		
tools/ui-audit/tests/test_check_screens.py	97	tools/ui-audit/tests/test_check_screens.py@9208dcf:2	unittest	стандартный		
tools/ui-audit/tests/test_check_screens.py	97	tools/ui-audit/tests/test_check_screens.py@9208dcf:3	pathlib	стандартный		
tools/ui-audit/tests/test_check_screens.py	97	tools/ui-audit/tests/test_check_screens.py@9208dcf:7	check_screens	свой		
tools/ui-audit/tests/test_combos.py	170	tools/ui-audit/tests/test_combos.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_combos.py	170	tools/ui-audit/tests/test_combos.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_combos.py	170	tools/ui-audit/tests/test_combos.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_combos.py	170	tools/ui-audit/tests/test_combos.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_combos.py	170	tools/ui-audit/tests/test_combos.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/tests/test_combos.py	170	tools/ui-audit/tests/test_combos.py@9208dcf:9	check_completeness	свой		
tools/ui-audit/tests/test_combos.py	170	tools/ui-audit/tests/test_combos.py@9208dcf:10	combos	свой		
tools/ui-audit/tests/test_extra_rules.py	203	tools/ui-audit/tests/test_extra_rules.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_extra_rules.py	203	tools/ui-audit/tests/test_extra_rules.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_extra_rules.py	203	tools/ui-audit/tests/test_extra_rules.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_extra_rules.py	203	tools/ui-audit/tests/test_extra_rules.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_extra_rules.py	203	tools/ui-audit/tests/test_extra_rules.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/tests/test_extra_rules.py	203	tools/ui-audit/tests/test_extra_rules.py@9208dcf:9	check_geometry	свой		
tools/ui-audit/tests/test_extract_keys.py	74	tools/ui-audit/tests/test_extract_keys.py@9208dcf:1	sys	стандартный		
tools/ui-audit/tests/test_extract_keys.py	74	tools/ui-audit/tests/test_extract_keys.py@9208dcf:2	unittest	стандартный		
tools/ui-audit/tests/test_extract_keys.py	74	tools/ui-audit/tests/test_extract_keys.py@9208dcf:3	pathlib	стандартный		
tools/ui-audit/tests/test_extract_keys.py	74	tools/ui-audit/tests/test_extract_keys.py@9208dcf:7	extract_keys	свой		
tools/ui-audit/tests/test_find_hit_tests.py	70	tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:1	sys	стандартный		
tools/ui-audit/tests/test_find_hit_tests.py	70	tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:2	tempfile	стандартный		
tools/ui-audit/tests/test_find_hit_tests.py	70	tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:3	unittest	стандартный		
tools/ui-audit/tests/test_find_hit_tests.py	70	tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/tests/test_find_hit_tests.py	70	tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:8	find_hit_tests	свой		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:9	combos	свой		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:10	finalize_png	свой		
tools/ui-audit/tests/test_png_policy.py	93	tools/ui-audit/tests/test_png_policy.py@9208dcf:11	run_combo	свой		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:1	json	стандартный		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:2	sys	стандартный		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:3	tempfile	стандартный		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:4	unittest	стандартный		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:5	pathlib	стандартный		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:7	PIL	сторонний	0; (пусто)	0; (пусто)
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:11	build_sheets	свой		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:12	check_completeness	свой		
tools/ui-audit/tests/test_png_policy_outputs.py	97	tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:13	combos	свой		
tools/ui-audit/tests/test_run_all.py	70	tools/ui-audit/tests/test_run_all.py@9208dcf:1	sys	стандартный		
tools/ui-audit/tests/test_run_all.py	70	tools/ui-audit/tests/test_run_all.py@9208dcf:2	tempfile	стандартный		
tools/ui-audit/tests/test_run_all.py	70	tools/ui-audit/tests/test_run_all.py@9208dcf:3	unittest	стандартный		
tools/ui-audit/tests/test_run_all.py	70	tools/ui-audit/tests/test_run_all.py@9208dcf:4	pathlib	стандартный		
tools/ui-audit/tests/test_run_all.py	70	tools/ui-audit/tests/test_run_all.py@9208dcf:8	combos	свой		
tools/ui-audit/tests/test_run_all.py	70	tools/ui-audit/tests/test_run_all.py@9208dcf:9	run_all	свой		
~~~~

#### interface.tsv

~~~~text
файл	вид	путь@9208dcf:строка	строка дословно
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:14	PER_SHEET = 6
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:15	COLUMNS = 3
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:16	CELL_WIDTH = 640
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:17	CELL_IMAGE_MAX_HEIGHT = 480
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:18	CAPTION_LINES = 3
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:19	LINE_HEIGHT = 18
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:20	GAP = 8
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:21	"FONT_PATHS = (""/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"", ""C:/Windows/Fonts/arial.ttf"")"
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:22	COLOR_A = (230, 30, 30)
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:23	COLOR_B = (30, 90, 240)
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:24	BACKGROUND = (24, 24, 24)
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:25	TEXT = (235, 235, 235)
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:186	"INDEX_STYLE = """"""body{font:14px sans-serif;margin:16px;background:#181818;color:#eee}"
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:191	"INDEX_SCRIPT = """"""const rows=[...document.querySelectorAll('tbody tr')];"
tools/ui-audit/build_sheets.py	константа	tools/ui-audit/build_sheets.py@9208dcf:200	"COLUMN_NAMES = (""scene"", ""screen"", ""state"", ""house"", ""resolution"", ""language"", ""graphics"", ""render"", ""world"", ""flags"")"
tools/ui-audit/build_sheets.py	аргумент	tools/ui-audit/build_sheets.py@9208dcf:236	"    parser.add_argument(""--png-root"", required=True)"
tools/ui-audit/build_sheets.py	аргумент	tools/ui-audit/build_sheets.py@9208dcf:237	"    parser.add_argument(""--logs-root"", required=True)"
tools/ui-audit/build_sheets.py	аргумент	tools/ui-audit/build_sheets.py@9208dcf:238	"    parser.add_argument(""--catalog"", required=True)"
tools/ui-audit/build_sheets.py	аргумент	tools/ui-audit/build_sheets.py@9208dcf:239	"    parser.add_argument(""--flags"", help=""flags JSON from check_geometry.py"")"
tools/ui-audit/build_sheets.py	аргумент	tools/ui-audit/build_sheets.py@9208dcf:240	"    parser.add_argument(""--full"", action=""append"", default=[], help=""combination id with a full catalog sheet set"")"
tools/ui-audit/build_sheets.py	аргумент	tools/ui-audit/build_sheets.py@9208dcf:241	"    parser.add_argument(""--order"", help=""order.json written by run_all.py"")"
tools/ui-audit/build_sheets.py	аргумент	tools/ui-audit/build_sheets.py@9208dcf:242	"    parser.add_argument(""--out"", required=True)"
tools/ui-audit/check_completeness.py	константа	tools/ui-audit/check_completeness.py@9208dcf:9	"RESOLUTIONS = (""1024x768"", ""1280x720"", ""1366x768"", ""1600x900"", ""1920x1080"", ""2560x1440"")"
tools/ui-audit/check_completeness.py	константа	tools/ui-audit/check_completeness.py@9208dcf:10	"LANGUAGES = (""ru"", ""en"")"
tools/ui-audit/check_completeness.py	константа	tools/ui-audit/check_completeness.py@9208dcf:11	"GRAPHICS = (""hd"",)"
tools/ui-audit/check_completeness.py	аргумент	tools/ui-audit/check_completeness.py@9208dcf:52	"    parser.add_argument(""root"")"
tools/ui-audit/check_completeness.py	аргумент	tools/ui-audit/check_completeness.py@9208dcf:53	"    parser.add_argument(""--catalog"", required=True, help=""JSON printed by the game with --ui-audit-list"")"
tools/ui-audit/check_completeness.py	аргумент	tools/ui-audit/check_completeness.py@9208dcf:54	"    parser.add_argument(""--flags"", help=""JSON of flags written by check_geometry.py"")"
tools/ui-audit/check_completeness.py	аргумент	tools/ui-audit/check_completeness.py@9208dcf:55	"    parser.add_argument(""--order"", help=""order.json written by run_all.py: every combination in capture order"")"
tools/ui-audit/check_credits.py	аргумент	tools/ui-audit/check_credits.py@9208dcf:43	"    parser.add_argument(""logs_root"")"
tools/ui-audit/check_geometry.py	константа	tools/ui-audit/check_geometry.py@9208dcf:7	RULE_NAMES = {
tools/ui-audit/check_geometry.py	аргумент	tools/ui-audit/check_geometry.py@9208dcf:226	"    parser.add_argument(""logs_root"")"
tools/ui-audit/check_geometry.py	аргумент	tools/ui-audit/check_geometry.py@9208dcf:227	"    parser.add_argument(""--json"", dest=""json_out"")"
tools/ui-audit/check_geometry.py	аргумент	tools/ui-audit/check_geometry.py@9208dcf:228	"    parser.add_argument(""--txt"", dest=""txt_out"")"
tools/ui-audit/check_geometry.py	аргумент	tools/ui-audit/check_geometry.py@9208dcf:229	"    parser.add_argument(""--summary8"", dest=""summary8_out"")"
tools/ui-audit/check_keys.py	константа	tools/ui-audit/check_keys.py@9208dcf:7	"STATE_SEPARATOR = "" | """
tools/ui-audit/check_keys.py	константа	tools/ui-audit/check_keys.py@9208dcf:8	"BINDING_PREFIX = ""m_commandBindings."""
tools/ui-audit/check_keys.py	константа	tools/ui-audit/check_keys.py@9208dcf:9	"REBINDING_WORDS = ""переназначение без проверки занятости"""
tools/ui-audit/check_keys.py	аргумент	tools/ui-audit/check_keys.py@9208dcf:106	"    parser.add_argument(""--keys"", required=True)"
tools/ui-audit/check_keys.py	аргумент	tools/ui-audit/check_keys.py@9208dcf:107	"    parser.add_argument(""--raw"", required=True)"
tools/ui-audit/check_keys.py	аргумент	tools/ui-audit/check_keys.py@9208dcf:108	"    parser.add_argument(""--binding-check"")"
tools/ui-audit/check_keys.py	аргумент	tools/ui-audit/check_keys.py@9208dcf:109	"    parser.add_argument(""--out"")"
tools/ui-audit/check_options_geometry.py	константа	tools/ui-audit/check_options_geometry.py@9208dcf:11	OPTIONS_SCENES = (
tools/ui-audit/check_options_geometry.py	аргумент	tools/ui-audit/check_options_geometry.py@9208dcf:99	"    parser.add_argument(""logs_root"")"
tools/ui-audit/check_options_geometry.py	аргумент	tools/ui-audit/check_options_geometry.py@9208dcf:101	"    plan.add_argument(""--plan"", help=""audit-plan.json emitted by run_all.py"")"
tools/ui-audit/check_options_geometry.py	аргумент	tools/ui-audit/check_options_geometry.py@9208dcf:102	"    plan.add_argument(""--combos"", help=""one planned audit combo id per line"")"
tools/ui-audit/check_scenes.py	константа	tools/ui-audit/check_scenes.py@9208dcf:9	"UNIT_PREFIX = ""units-label-"""
tools/ui-audit/check_scenes.py	константа	tools/ui-audit/check_scenes.py@9208dcf:10	"HARVESTER_SCENE = UNIT_PREFIX + ""harvester"""
tools/ui-audit/check_scenes.py	константа	tools/ui-audit/check_scenes.py@9208dcf:11	"UNIT_KINDS = (""health"", ""group"", ""experience"")"
tools/ui-audit/check_scenes.py	константа	tools/ui-audit/check_scenes.py@9208dcf:26	"STRUCTURE_EDGES = {""structure-label-top"": (""top"", at_top), ""structure-label-right"": (""right"", at_right)}"
tools/ui-audit/check_scenes.py	аргумент	tools/ui-audit/check_scenes.py@9208dcf:113	"    parser.add_argument(""logs"", nargs=""+"")"
tools/ui-audit/check_scenes.py	аргумент	tools/ui-audit/check_scenes.py@9208dcf:114	"    parser.add_argument(""--out"")"
tools/ui-audit/check_screens.py	константа	tools/ui-audit/check_screens.py@9208dcf:7	"STATE_DEFINE = re.compile(r""(?m)^#define\s+(GAME_\w+)\s+-?\d+"")"
tools/ui-audit/check_screens.py	константа	tools/ui-audit/check_screens.py@9208dcf:8	"CLASS_DEFINITION = re.compile(r""(?m)^[ \t]*class\s+(\w+)[^;{]*\{"")"
tools/ui-audit/check_screens.py	константа	tools/ui-audit/check_screens.py@9208dcf:9	"CLASS_DIRECTORIES = (""src/gamestates"", ""src/mentat"")"
tools/ui-audit/check_screens.py	константа	tools/ui-audit/check_screens.py@9208dcf:10	"CLASS_FILES = (""src/save/SaveSlotsDialog.hpp"",)"
tools/ui-audit/check_screens.py	аргумент	tools/ui-audit/check_screens.py@9208dcf:72	"    parser.add_argument(""--catalog"", required=True)"
tools/ui-audit/check_screens.py	аргумент	tools/ui-audit/check_screens.py@9208dcf:73	"    parser.add_argument(""--root"", required=True)"
tools/ui-audit/check_screens.py	аргумент	tools/ui-audit/check_screens.py@9208dcf:74	"    parser.add_argument(""--exclusions"", required=True)"
tools/ui-audit/combos.py	константа	tools/ui-audit/combos.py@9208dcf:4	"FULL_RESOLUTIONS = (""1024x768"", ""1920x1080"")"
tools/ui-audit/combos.py	константа	tools/ui-audit/combos.py@9208dcf:5	"LANGUAGES = (""ru"", ""en"")"
tools/ui-audit/combos.py	константа	tools/ui-audit/combos.py@9208dcf:6	"GRAPHICS = (""hd"",)"
tools/ui-audit/extract_keys.py	константа	tools/ui-audit/extract_keys.py@9208dcf:6	"KEY_TOKEN = re.compile(r""SDLK_\w+|SDL_SCANCODE_\w+|m_commandBindings\.\w+|\bcommandBindings?\b"")"
tools/ui-audit/extract_keys.py	константа	tools/ui-audit/extract_keys.py@9208dcf:7	"SOURCE_SUFFIXES = ("".cpp"", "".h"", "".hpp"", "".c"", "".cc"")"
tools/ui-audit/extract_keys.py	аргумент	tools/ui-audit/extract_keys.py@9208dcf:80	"    parser.add_argument(""--root"", required=True)"
tools/ui-audit/extract_keys.py	аргумент	tools/ui-audit/extract_keys.py@9208dcf:81	"    parser.add_argument(""--out"", required=True)"
tools/ui-audit/finalize_png.py	аргумент	tools/ui-audit/finalize_png.py@9208dcf:30	"    parser.add_argument(""--exe"", required=True)"
tools/ui-audit/finalize_png.py	аргумент	tools/ui-audit/finalize_png.py@9208dcf:31	"    parser.add_argument(""--resources"", required=True)"
tools/ui-audit/finalize_png.py	аргумент	tools/ui-audit/finalize_png.py@9208dcf:32	"    parser.add_argument(""--out"", required=True)"
tools/ui-audit/finalize_png.py	аргумент	tools/ui-audit/finalize_png.py@9208dcf:33	"    parser.add_argument(""--flags"", required=True, help=""flags JSON from check_geometry.py"")"
tools/ui-audit/finalize_png.py	аргумент	tools/ui-audit/finalize_png.py@9208dcf:34	"    parser.add_argument(""--dry-run"", action=""store_true"")"
tools/ui-audit/find_hit_tests.py	константа	tools/ui-audit/find_hit_tests.py@9208dcf:6	"HIT = re.compile(r""\b(isWithin\w*|isOver\w*|isMouseOver\w*|isPointWithin\w*|isInside\w*|containsPoint\w*|pointInRect\w*)\s*\("")"
tools/ui-audit/find_hit_tests.py	константа	tools/ui-audit/find_hit_tests.py@9208dcf:7	"FUNCTION = re.compile(r""^[A-Za-z_][\w:<>,\s\*&~]*?\b([A-Za-z_~]\w*::[~\w]+)\s*\("")"
tools/ui-audit/find_hit_tests.py	константа	tools/ui-audit/find_hit_tests.py@9208dcf:8	"DIRECTORIES = (""src/gui"", ""src/drawers"", ""src/gamestates"", ""src/managers"", ""src/save"", ""src/sidebar"", ""src/mentat"","
tools/ui-audit/find_hit_tests.py	константа	tools/ui-audit/find_hit_tests.py@9208dcf:10	"RECORDS = (""uiaudit::recordClick"", ""uiaudit::recordCanvasClick"")"
tools/ui-audit/find_hit_tests.py	аргумент	tools/ui-audit/find_hit_tests.py@9208dcf:49	"    parser.add_argument(""--root"", required=True)"
tools/ui-audit/run_all.py	константа	tools/ui-audit/run_all.py@9208dcf:15	WORKERS = 16
tools/ui-audit/run_all.py	константа	tools/ui-audit/run_all.py@9208dcf:16	MIN_FREE_GB = 5
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:96	"    parser.add_argument(""--exe"", required=True)"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:97	"    parser.add_argument(""--resources"", required=True)"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:98	"    parser.add_argument(""--out"", required=True)"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:99	"    parser.add_argument(""--catalog"", required=True)"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:100	"    parser.add_argument(""--resolutions"", default=""1024x768,1280x720,1366x768,1600x900,1920x1080,2560x1440"")"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:101	"    parser.add_argument(""--limit"", type=int, help=""run only this many unfinished combinations of the plan"")"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:102	"    parser.add_argument(""--workers"", type=int, default=WORKERS)"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:103	"    parser.add_argument(""--min-free-gb"", type=float, default=MIN_FREE_GB)"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:104	"    parser.add_argument(""--only"", action=""append"", help=""run only this combination id (repeatable)"")"
tools/ui-audit/run_all.py	аргумент	tools/ui-audit/run_all.py@9208dcf:105	"    parser.add_argument(""--list"", action=""store_true"", help=""print the plan and exit"")"
tools/ui-audit/run_combo.py	константа	tools/ui-audit/run_combo.py@9208dcf:16	"RUNTIME_LINKS = (""campaign"", ""campaign_en"", ""data"", ""skirmish"", ""skirmish_en"")"
tools/ui-audit/run_combo.py	константа	tools/ui-audit/run_combo.py@9208dcf:17	"FULL_RESOLUTIONS = (""1024x768"", ""1920x1080"")"
tools/ui-audit/run_combo.py	константа	tools/ui-audit/run_combo.py@9208dcf:18	SCENE_TIMEOUT_SECONDS = 90
tools/ui-audit/run_combo.py	константа	tools/ui-audit/run_combo.py@9208dcf:19	SCENE_ATTEMPTS = 2
tools/ui-audit/run_combo.py	константа	tools/ui-audit/run_combo.py@9208dcf:20	MIN_FREE_GB = 5
tools/ui-audit/run_combo.py	константа	tools/ui-audit/run_combo.py@9208dcf:21	EXIT_LOW_DISK = 3
tools/ui-audit/run_combo.py	аргумент	tools/ui-audit/run_combo.py@9208dcf:154	"    parser.add_argument(""--exe"", required=True)"
tools/ui-audit/run_combo.py	аргумент	tools/ui-audit/run_combo.py@9208dcf:155	"    parser.add_argument(""--resources"", required=True)"
tools/ui-audit/run_combo.py	аргумент	tools/ui-audit/run_combo.py@9208dcf:156	"    parser.add_argument(""--out"", required=True)"
tools/ui-audit/run_combo.py	аргумент	tools/ui-audit/run_combo.py@9208dcf:157	"    parser.add_argument(""--combo"", required=True, help=""WxH/lang/gfx or WxH/lang/gfx/r<R>w<W>, for example 1024x768/ru/hd"")"
tools/ui-audit/run_combo.py	аргумент	tools/ui-audit/run_combo.py@9208dcf:158	"    parser.add_argument(""--scene"", action=""append"", help=""limit to these scene ids"")"
tools/ui-audit/run_combo.py	аргумент	tools/ui-audit/run_combo.py@9208dcf:159	"    parser.add_argument(""--flags"", help=""flags JSON: capture only the flagged scenes of this combination, with PNG"")"
tools/ui-audit/run_combo.py	аргумент	tools/ui-audit/run_combo.py@9208dcf:160	"    parser.add_argument(""--min-free-gb"", type=float, default=MIN_FREE_GB)"
~~~~

## 2. Чтение и запись файлов, внешние команды

Команда и вывод извлечения строк файловых операций:

#### io-extraction.log

~~~~text
files_scanned=14
rows=81
files:
tools/ui-audit/build_sheets.py
tools/ui-audit/check_completeness.py
tools/ui-audit/check_credits.py
tools/ui-audit/check_geometry.py
tools/ui-audit/check_keys.py
tools/ui-audit/check_options_geometry.py
tools/ui-audit/check_scenes.py
tools/ui-audit/check_screens.py
tools/ui-audit/combos.py
tools/ui-audit/extract_keys.py
tools/ui-audit/finalize_png.py
tools/ui-audit/find_hit_tests.py
tools/ui-audit/run_all.py
tools/ui-audit/run_combo.py
~~~~

Таблица `io.tsv`: 81 строка данных.

#### io.tsv

~~~~text
файл	функция	путь@9208dcf:строка	строка дословно
tools/ui-audit/build_sheets.py	find_pngs	tools/ui-audit/build_sheets.py@9208dcf:59	    return sorted(Path(png_root).rglob("*.png"))
tools/ui-audit/build_sheets.py	render_cell	tools/ui-audit/build_sheets.py@9208dcf:68	    image = Image.open(png_path).convert("RGB")
tools/ui-audit/build_sheets.py	make_sheet	tools/ui-audit/build_sheets.py@9208dcf:89	    Path(path).parent.mkdir(parents=True, exist_ok=True)
tools/ui-audit/build_sheets.py	build_catalog_sheets	tools/ui-audit/build_sheets.py@9208dcf:96	    by_scene = {path.stem: path for path in directory.glob("*.png")}
tools/ui-audit/build_sheets.py	canvas_factor	tools/ui-audit/build_sheets.py@9208dcf:112	    header = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
tools/ui-audit/build_sheets.py	canvas_factor	tools/ui-audit/build_sheets.py@9208dcf:113	    return Image.open(png_path).width / header["canvas"]["w"]
tools/ui-audit/build_sheets.py	build_index	tools/ui-audit/build_sheets.py@9208dcf:230	    Path(index_path).write_text(page, encoding="utf-8")
tools/ui-audit/build_sheets.py	main	tools/ui-audit/build_sheets.py@9208dcf:244	    meta = {scene["id"]: scene for scene in json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]}
tools/ui-audit/build_sheets.py	main	tools/ui-audit/build_sheets.py@9208dcf:245	    flags = json.loads(Path(args.flags).read_text(encoding="utf-8")) if args.flags else []
tools/ui-audit/build_sheets.py	main	tools/ui-audit/build_sheets.py@9208dcf:250	    order = json.loads(Path(args.order).read_text(encoding="utf-8")) if args.order else None
tools/ui-audit/check_completeness.py	check_combinations	tools/ui-audit/check_completeness.py@9208dcf:39	            for path in sorted(png_dir.glob("*.png")):
tools/ui-audit/check_completeness.py	main	tools/ui-audit/check_completeness.py@9208dcf:57	    scenes = json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]
tools/ui-audit/check_completeness.py	main	tools/ui-audit/check_completeness.py@9208dcf:58	    flags = json.loads(Path(args.flags).read_text(encoding="utf-8")) if args.flags else []
tools/ui-audit/check_completeness.py	main	tools/ui-audit/check_completeness.py@9208dcf:61	        order = json.loads(Path(args.order).read_text(encoding="utf-8"))
tools/ui-audit/check_credits.py	load	tools/ui-audit/check_credits.py@9208dcf:9	    records = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
tools/ui-audit/check_credits.py	check_credits	tools/ui-audit/check_credits.py@9208dcf:24	    for path in sorted(Path(logs_root).rglob("credits-*.geometry.jsonl")):
tools/ui-audit/check_geometry.py	load_log	tools/ui-audit/check_geometry.py@9208dcf:162	    lines = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
tools/ui-audit/check_geometry.py	check_tree	tools/ui-audit/check_geometry.py@9208dcf:214	    for path in sorted(Path(logs_root).rglob("*.geometry.jsonl")):
tools/ui-audit/check_geometry.py	main	tools/ui-audit/check_geometry.py@9208dcf:234	        Path(args.txt_out).write_text("".join(line + "\n" for line in lines), encoding="utf-8")
tools/ui-audit/check_geometry.py	main	tools/ui-audit/check_geometry.py@9208dcf:239	        Path(args.json_out).write_text(json.dumps(flags, ensure_ascii=False, indent=1), encoding="utf-8")
tools/ui-audit/check_geometry.py	main	tools/ui-audit/check_geometry.py@9208dcf:241	        summary_logs = [load_log(path) for path in sorted(Path(args.logs_root).rglob("*.geometry.jsonl"))]
tools/ui-audit/check_geometry.py	main	tools/ui-audit/check_geometry.py@9208dcf:242	        Path(args.summary8_out).write_text(
tools/ui-audit/check_keys.py	load_tsv	tools/ui-audit/check_keys.py@9208dcf:13	    with open(path, encoding="utf-8", newline="") as handle:
tools/ui-audit/check_keys.py	main	tools/ui-audit/check_keys.py@9208dcf:120	        Path(args.out).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
tools/ui-audit/check_options_geometry.py	planned_pairs	tools/ui-audit/check_options_geometry.py@9208dcf:65	        combos = [line.strip() for line in Path(combos_path).read_text(encoding="utf-8").splitlines()
tools/ui-audit/check_options_geometry.py	planned_pairs	tools/ui-audit/check_options_geometry.py@9208dcf:68	    entries = json.loads(Path(plan_path).read_text(encoding="utf-8"))
tools/ui-audit/check_options_geometry.py	check_tree	tools/ui-audit/check_options_geometry.py@9208dcf:83	    for path in sorted(Path(logs_root).rglob("*.geometry.jsonl")):
tools/ui-audit/check_scenes.py	main	tools/ui-audit/check_scenes.py@9208dcf:118	        for path in sorted(Path(root).rglob("*.geometry.jsonl")):
tools/ui-audit/check_scenes.py	main	tools/ui-audit/check_scenes.py@9208dcf:125	        Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
tools/ui-audit/check_screens.py	collect_code_names	tools/ui-audit/check_screens.py@9208dcf:59	    states = code_states((root / "src/include/definitions.h").read_text(encoding="utf-8", errors="replace"))
tools/ui-audit/check_screens.py	collect_code_names	tools/ui-audit/check_screens.py@9208dcf:62	        for path in sorted((root / directory).glob("*.h")) + sorted((root / directory).glob("*.hpp")):
tools/ui-audit/check_screens.py	collect_code_names	tools/ui-audit/check_screens.py@9208dcf:63	            sources.append(path.read_text(encoding="utf-8", errors="replace"))
tools/ui-audit/check_screens.py	collect_code_names	tools/ui-audit/check_screens.py@9208dcf:65	    dialog_classes = [name for name in code_classes([dialog.read_text(encoding="utf-8", errors="replace")])
tools/ui-audit/check_screens.py	main	tools/ui-audit/check_screens.py@9208dcf:76	    scenes = json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]
tools/ui-audit/check_screens.py	main	tools/ui-audit/check_screens.py@9208dcf:77	    exclusions, problems = load_exclusions(Path(args.exclusions).read_text(encoding="utf-8"))
tools/ui-audit/combos.py	parse_scales	tools/ui-audit/combos.py@9208dcf:10	    data = json.loads(text)
tools/ui-audit/extract_keys.py	extract_tree	tools/ui-audit/extract_keys.py@9208dcf:71	    for path in sorted((root / "src").rglob("*")):
tools/ui-audit/extract_keys.py	extract_tree	tools/ui-audit/extract_keys.py@9208dcf:74	            rows += extract(path.read_text(encoding="utf-8", errors="replace"), relative)
tools/ui-audit/extract_keys.py	main	tools/ui-audit/extract_keys.py@9208dcf:84	    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
tools/ui-audit/extract_keys.py	main	tools/ui-audit/extract_keys.py@9208dcf:85	    with open(args.out, "w", encoding="utf-8", newline="") as handle:
tools/ui-audit/finalize_png.py	plan_actions	tools/ui-audit/finalize_png.py@9208dcf:20	        have = {path.stem for path in png_dir.glob("*.png")} if png_dir.is_dir() else set()
tools/ui-audit/finalize_png.py	main	tools/ui-audit/finalize_png.py@9208dcf:37	    order = json.loads((out / "order.json").read_text(encoding="utf-8"))
tools/ui-audit/finalize_png.py	main	tools/ui-audit/finalize_png.py@9208dcf:38	    flags = json.loads(Path(args.flags).read_text(encoding="utf-8"))
tools/ui-audit/finalize_png.py	main	tools/ui-audit/finalize_png.py@9208dcf:44	        (out / "png" / identifier / f"{scene}.png").unlink()
tools/ui-audit/finalize_png.py	main	tools/ui-audit/finalize_png.py@9208dcf:54	        code = max(code, subprocess.run(command, check=False).returncode)
tools/ui-audit/find_hit_tests.py	scan	tools/ui-audit/find_hit_tests.py@9208dcf:39	        for path in sorted((root / directory).rglob("*.cpp")):
tools/ui-audit/find_hit_tests.py	scan	tools/ui-audit/find_hit_tests.py@9208dcf:40	            rows, records = scan_text(path.read_text(encoding="utf-8", errors="replace"))
tools/ui-audit/run_all.py	scales_for	tools/ui-audit/run_all.py@9208dcf:22	        result = subprocess.run([str(executable), "--ui-audit-scales", resolution], env=run_combo.game_environment(),
tools/ui-audit/run_all.py	run_one	tools/ui-audit/run_all.py@9208dcf:81	    log_path.parent.mkdir(parents=True, exist_ok=True)
tools/ui-audit/run_all.py	run_one	tools/ui-audit/run_all.py@9208dcf:85	    with open(log_path, "w", encoding="utf-8") as log:
tools/ui-audit/run_all.py	run_one	tools/ui-audit/run_all.py@9208dcf:86	        code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
tools/ui-audit/run_all.py	run_one	tools/ui-audit/run_all.py@9208dcf:89	        marker.parent.mkdir(parents=True, exist_ok=True)
tools/ui-audit/run_all.py	run_one	tools/ui-audit/run_all.py@9208dcf:90	        marker.write_text("ok\n", encoding="utf-8")
tools/ui-audit/run_all.py	main	tools/ui-audit/run_all.py@9208dcf:110	    Path(args.out).mkdir(parents=True, exist_ok=True)
tools/ui-audit/run_all.py	main	tools/ui-audit/run_all.py@9208dcf:119	    (Path(args.out) / "order.json").write_text(json.dumps([combos.combo_id(c) for c in generated]), encoding="utf-8")
tools/ui-audit/run_all.py	main	tools/ui-audit/run_all.py@9208dcf:120	    scenes = json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]
tools/ui-audit/run_all.py	main	tools/ui-audit/run_all.py@9208dcf:122	    (Path(args.out) / "audit-plan.json").write_text(
tools/ui-audit/run_all.py	main	tools/ui-audit/run_all.py@9208dcf:130	    with open(Path(args.out) / "free-space.txt", "a", encoding="utf-8") as journal:
tools/ui-audit/run_combo.py	free_gb	tools/ui-audit/run_combo.py@9208dcf:25	    return shutil.disk_usage(path).free / (1024 ** 3)
tools/ui-audit/run_combo.py	make_runtime	tools/ui-audit/run_combo.py@9208dcf:48	        shutil.rmtree(runtime)
tools/ui-audit/run_combo.py	make_runtime	tools/ui-audit/run_combo.py@9208dcf:49	    runtime.mkdir(parents=True)
tools/ui-audit/run_combo.py	make_runtime	tools/ui-audit/run_combo.py@9208dcf:50	    shutil.copy2(executable, runtime / "d2tm")
tools/ui-audit/run_combo.py	make_runtime	tools/ui-audit/run_combo.py@9208dcf:53	        os.symlink(bin_dir / name, runtime / name)
tools/ui-audit/run_combo.py	make_runtime	tools/ui-audit/run_combo.py@9208dcf:54	    shutil.copy2(Path(resources) / "game.ini", runtime / "game.ini")
tools/ui-audit/run_combo.py	make_runtime	tools/ui-audit/run_combo.py@9208dcf:55	    settings = apply_settings((bin_dir / "settings.ini").read_text(encoding="utf-8"), {
tools/ui-audit/run_combo.py	make_runtime	tools/ui-audit/run_combo.py@9208dcf:63	    (runtime / "settings.ini").write_text(settings, encoding="utf-8")
tools/ui-audit/run_combo.py	run_scene	tools/ui-audit/run_combo.py@9208dcf:79	    return subprocess.run(command, cwd=runtime, env=game_environment(), check=False,
tools/ui-audit/run_combo.py	list_scenes	tools/ui-audit/run_combo.py@9208dcf:84	    result = subprocess.run([str(executable), "--ui-audit-list"], env=game_environment(), check=True,
tools/ui-audit/run_combo.py	list_scenes	tools/ui-audit/run_combo.py@9208dcf:86	    return json.loads(result.stdout)["scenes"]
tools/ui-audit/run_combo.py	load_order	tools/ui-audit/run_combo.py@9208dcf:91	    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:113	    png_dir.mkdir(parents=True, exist_ok=True)
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:114	    log_dir.mkdir(parents=True, exist_ok=True)
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:123	            shutil.rmtree(scene_out)
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:124	        scene_out.mkdir(parents=True)
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:134	            except subprocess.TimeoutExpired:
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:141	        shutil.move(log, log_dir / log.name)
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:144	            shutil.move(png, png_dir / png.name)
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:146	            (png_dir / png.name).unlink()
tools/ui-audit/run_combo.py	run_combo	tools/ui-audit/run_combo.py@9208dcf:148	    shutil.rmtree(work, ignore_errors=True)
tools/ui-audit/run_combo.py	main	tools/ui-audit/run_combo.py@9208dcf:165	    Path(args.out).mkdir(parents=True, exist_ok=True)
tools/ui-audit/run_combo.py	main	tools/ui-audit/run_combo.py@9208dcf:174	        flagged = {f["scene"] for f in json.loads(Path(args.flags).read_text(encoding="utf-8"))
~~~~

## 3. Поля геометрии и каталога, имена сцен

Команда и вывод `git grep` по найденным строковым литералам:

#### lane1.gitgrep.log

~~~~text
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"a"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"action"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"actions"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"all"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"append"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"area"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"auto"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"b"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"bin"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"box"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"campaign"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"campaign_en"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"canvas"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"click"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"combo"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"command"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"credit"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"d2tm"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"data"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"done"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"dummy"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"en"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:162:         << outputH << "\",\"language\":\"" << (localization::isEnglish() ? "en" : "ru") << "\",\"graphics\":\"hd\",\"canvas\":{\"w\":" << game.m_screenW
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"experience"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"false"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:163:         << ",\"h\":" << game.m_screenH << "},\"game_screen\":" << (g_scene->gameScreen ? "true" : "false")
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:405:                    "\",\"game_screen\":" + (scene.gameScreen ? "true" : "false") + ",\"house\":\"" + escapeJson(scene.house) + "\",\"hud\":" + (scene.hud ? "true" : "false") +
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:406:                    ",\"hd_only\":" + (scene.hdOnly ? "true" : "false") + ",\"hover\":";
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"file"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"flags"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"function"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"game"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"game_screen"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"graphics"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"group"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"groups"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"gui"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"h"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"harvester"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"hd"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"header"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"health"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"house"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"hud"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"id"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"json_out"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"k"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"key"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"keys"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"kind"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"kinds"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"label"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"language"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"legacy"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"line"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"log"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"logs"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"logs_root"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"map_viewport"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"mods"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"n"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"name"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"names"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"no"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"obj"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"objects_intersecting"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"objects_total"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"other"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"out"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"owner"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"places"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"png"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"render"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"render_scale"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"replace"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"resolution"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"right"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"root"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"ru"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:162:         << outputH << "\",\"language\":\"" << (localization::isEnglish() ? "en" : "ru") << "\",\"graphics\":\"hd\",\"canvas\":{\"w\":" << game.m_screenW
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"rule"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"run"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"runtime"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"s"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"scene"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"scenes"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"scope"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"screen"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"sheets"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"skirmish"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"skirmish_en"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"software"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"spice"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"src"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"state"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"states"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"store_true"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"summary8_out"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"t"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"text"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"texts"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"timeout"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"top"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"txt_out"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"type"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"w"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"work"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"world"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"world_scale"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"x"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:379:        std::string json = "{\"resolution\":\"" + std::to_string(width) + "x" + std::to_string(height) +
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"y"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
Command: export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"yes"' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/debug | head -3
(нет)
~~~~

Таблицы: `fields.tsv` — 107 строк данных; `scene-refs.tsv` — 9 строк данных.

#### fields.tsv

~~~~text
значение	места в инструментах	места в src/debug@9208dcf
a	tools/ui-audit/build_sheets.py@9208dcf:118, tools/ui-audit/build_sheets.py@9208dcf:134, tools/ui-audit/check_geometry.py@9208dcf:57, tools/ui-audit/check_geometry.py@9208dcf:198, tools/ui-audit/run_all.py@9208dcf:130	нет
action	tools/ui-audit/check_keys.py@9208dcf:35, tools/ui-audit/check_keys.py@9208dcf:47, tools/ui-audit/check_keys.py@9208dcf:76	нет
actions	tools/ui-audit/check_keys.py@9208dcf:51, tools/ui-audit/check_keys.py@9208dcf:88	нет
all	tools/ui-audit/combos.py@9208dcf:21, tools/ui-audit/combos.py@9208dcf:44, tools/ui-audit/combos.py@9208dcf:55	нет
append	tools/ui-audit/build_sheets.py@9208dcf:240, tools/ui-audit/run_all.py@9208dcf:104, tools/ui-audit/run_combo.py@9208dcf:158	нет
area	tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:67, tools/ui-audit/check_geometry.py@9208dcf:71, tools/ui-audit/check_geometry.py@9208dcf:115, tools/ui-audit/check_geometry.py@9208dcf:174, tools/ui-audit/check_options_geometry.py@9208dcf:31	нет
auto	tools/ui-audit/build_sheets.py@9208dcf:41, tools/ui-audit/build_sheets.py@9208dcf:215	нет
b	tools/ui-audit/build_sheets.py@9208dcf:118, tools/ui-audit/build_sheets.py@9208dcf:134, tools/ui-audit/check_geometry.py@9208dcf:58, tools/ui-audit/check_geometry.py@9208dcf:198	нет
bin	tools/ui-audit/run_combo.py@9208dcf:51	нет
box	tools/ui-audit/check_geometry.py@9208dcf:101	нет
campaign	tools/ui-audit/run_combo.py@9208dcf:16	нет
campaign_en	tools/ui-audit/run_combo.py@9208dcf:16	нет
canvas	tools/ui-audit/build_sheets.py@9208dcf:113, tools/ui-audit/check_geometry.py@9208dcf:65, tools/ui-audit/check_geometry.py@9208dcf:181	нет
click	tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:123	нет
combo	tools/ui-audit/build_sheets.py@9208dcf:134, tools/ui-audit/build_sheets.py@9208dcf:138, tools/ui-audit/build_sheets.py@9208dcf:147, tools/ui-audit/build_sheets.py@9208dcf:150, tools/ui-audit/build_sheets.py@9208dcf:153, tools/ui-audit/build_sheets.py@9208dcf:167, tools/ui-audit/build_sheets.py@9208dcf:169, tools/ui-audit/build_sheets.py@9208dcf:175, tools/ui-audit/build_sheets.py@9208dcf:177, tools/ui-audit/build_sheets.py@9208dcf:206, tools/ui-audit/check_completeness.py@9208dcf:59, tools/ui-audit/check_geometry.py@9208dcf:56, tools/ui-audit/check_geometry.py@9208dcf:197, tools/ui-audit/check_options_geometry.py@9208dcf:73, tools/ui-audit/check_options_geometry.py@9208dcf:76, tools/ui-audit/combos.py@9208dcf:81, tools/ui-audit/combos.py@9208dcf:82, tools/ui-audit/combos.py@9208dcf:83, tools/ui-audit/combos.py@9208dcf:91, tools/ui-audit/combos.py@9208dcf:92, tools/ui-audit/combos.py@9208dcf:93, tools/ui-audit/run_all.py@9208dcf:47, tools/ui-audit/run_combo.py@9208dcf:175	нет
command	tools/ui-audit/check_keys.py@9208dcf:64, tools/ui-audit/check_keys.py@9208dcf:72, tools/ui-audit/check_keys.py@9208dcf:78, tools/ui-audit/check_keys.py@9208dcf:83, tools/ui-audit/check_keys.py@9208dcf:84	нет
credit	tools/ui-audit/check_credits.py@9208dcf:30	нет
d2tm	tools/ui-audit/run_combo.py@9208dcf:50, tools/ui-audit/run_combo.py@9208dcf:76	нет
data	tools/ui-audit/run_combo.py@9208dcf:16	нет
done	tools/ui-audit/run_all.py@9208dcf:54	нет
dummy	tools/ui-audit/run_combo.py@9208dcf:69	нет
en	tools/ui-audit/check_completeness.py@9208dcf:10, tools/ui-audit/combos.py@9208dcf:5	"9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:162:         << outputH << ""\"",\""language\"":\"""" << (localization::isEnglish() ? ""en"" : ""ru"") << ""\"",\""graphics\"":\""hd\"",\""canvas\"":{\""w\"":"" << game.m_screenW"
experience	tools/ui-audit/check_scenes.py@9208dcf:11	нет
false	tools/ui-audit/run_combo.py@9208dcf:58	"9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:163:         << "",\""h\"":"" << game.m_screenH << ""},\""game_screen\"":"" << (g_scene->gameScreen ? ""true"" : ""false""); 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:405:                    ""\"",\""game_screen\"":"" + (scene.gameScreen ? ""true"" : ""false"") + "",\""house\"":\"""" + escapeJson(scene.house) + ""\"",\""hud\"":"" + (scene.hud ? ""true"" : ""false"") +; 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:406:                    "",\""hd_only\"":"" + (scene.hdOnly ? ""true"" : ""false"") + "",\""hover\"":"";"
file	tools/ui-audit/check_keys.py@9208dcf:49, tools/ui-audit/check_keys.py@9208dcf:93, tools/ui-audit/extract_keys.py@9208dcf:58, tools/ui-audit/extract_keys.py@9208dcf:64	нет
flags	tools/ui-audit/build_sheets.py@9208dcf:200	нет
function	tools/ui-audit/check_keys.py@9208dcf:93, tools/ui-audit/extract_keys.py@9208dcf:58, tools/ui-audit/extract_keys.py@9208dcf:64	нет
game	tools/ui-audit/combos.py@9208dcf:25, tools/ui-audit/combos.py@9208dcf:55, tools/ui-audit/combos.py@9208dcf:59	нет
game_screen	tools/ui-audit/check_geometry.py@9208dcf:174, tools/ui-audit/combos.py@9208dcf:60	нет
graphics	tools/ui-audit/build_sheets.py@9208dcf:49, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:214, tools/ui-audit/check_credits.py@9208dcf:26, tools/ui-audit/check_geometry.py@9208dcf:41, tools/ui-audit/check_geometry.py@9208dcf:182, tools/ui-audit/combos.py@9208dcf:30, tools/ui-audit/combos.py@9208dcf:36	нет
group	tools/ui-audit/check_scenes.py@9208dcf:11, tools/ui-audit/check_scenes.py@9208dcf:35	нет
groups	tools/ui-audit/check_scenes.py@9208dcf:33, tools/ui-audit/check_scenes.py@9208dcf:36, tools/ui-audit/check_scenes.py@9208dcf:53	нет
gui	tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:67, tools/ui-audit/check_geometry.py@9208dcf:71, tools/ui-audit/check_geometry.py@9208dcf:174, tools/ui-audit/check_options_geometry.py@9208dcf:19, tools/ui-audit/check_options_geometry.py@9208dcf:31	нет
h	tools/ui-audit/build_sheets.py@9208dcf:64, tools/ui-audit/build_sheets.py@9208dcf:122, tools/ui-audit/check_geometry.py@9208dcf:22, tools/ui-audit/check_geometry.py@9208dcf:27, tools/ui-audit/check_geometry.py@9208dcf:33, tools/ui-audit/check_geometry.py@9208dcf:37, tools/ui-audit/check_geometry.py@9208dcf:65, tools/ui-audit/check_geometry.py@9208dcf:102, tools/ui-audit/check_geometry.py@9208dcf:181, tools/ui-audit/check_geometry.py@9208dcf:201, tools/ui-audit/check_scenes.py@9208dcf:15, tools/ui-audit/check_scenes.py@9208dcf:23	нет
harvester	tools/ui-audit/check_scenes.py@9208dcf:10	нет
hd	tools/ui-audit/check_completeness.py@9208dcf:11, tools/ui-audit/combos.py@9208dcf:6, tools/ui-audit/combos.py@9208dcf:22	нет
header	tools/ui-audit/check_geometry.py@9208dcf:163	нет
health	tools/ui-audit/check_scenes.py@9208dcf:11	нет
house	tools/ui-audit/build_sheets.py@9208dcf:48, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:213	нет
hud	tools/ui-audit/combos.py@9208dcf:100	нет
id	tools/ui-audit/build_sheets.py@9208dcf:47, tools/ui-audit/build_sheets.py@9208dcf:176, tools/ui-audit/build_sheets.py@9208dcf:212, tools/ui-audit/build_sheets.py@9208dcf:244, tools/ui-audit/check_completeness.py@9208dcf:29, tools/ui-audit/check_completeness.py@9208dcf:32, tools/ui-audit/check_completeness.py@9208dcf:44, tools/ui-audit/combos.py@9208dcf:98, tools/ui-audit/run_all.py@9208dcf:47, tools/ui-audit/run_combo.py@9208dcf:119, tools/ui-audit/run_combo.py@9208dcf:130, tools/ui-audit/run_combo.py@9208dcf:136, tools/ui-audit/run_combo.py@9208dcf:137, tools/ui-audit/run_combo.py@9208dcf:139, tools/ui-audit/run_combo.py@9208dcf:142, tools/ui-audit/run_combo.py@9208dcf:147	нет
json_out	tools/ui-audit/check_geometry.py@9208dcf:227	нет
k	tools/ui-audit/check_credits.py@9208dcf:30, tools/ui-audit/check_credits.py@9208dcf:34, tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:66, tools/ui-audit/check_geometry.py@9208dcf:67, tools/ui-audit/check_geometry.py@9208dcf:71, tools/ui-audit/check_geometry.py@9208dcf:74, tools/ui-audit/check_geometry.py@9208dcf:114, tools/ui-audit/check_geometry.py@9208dcf:145, tools/ui-audit/check_geometry.py@9208dcf:163, tools/ui-audit/check_geometry.py@9208dcf:175, tools/ui-audit/check_options_geometry.py@9208dcf:19, tools/ui-audit/check_options_geometry.py@9208dcf:31, tools/ui-audit/check_scenes.py@9208dcf:32, tools/ui-audit/check_scenes.py@9208dcf:50	нет
key	tools/ui-audit/check_keys.py@9208dcf:27, tools/ui-audit/check_keys.py@9208dcf:44, tools/ui-audit/check_keys.py@9208dcf:50, tools/ui-audit/check_keys.py@9208dcf:59, tools/ui-audit/check_keys.py@9208dcf:77, tools/ui-audit/check_keys.py@9208dcf:87, tools/ui-audit/check_keys.py@9208dcf:93, tools/ui-audit/extract_keys.py@9208dcf:58, tools/ui-audit/extract_keys.py@9208dcf:64	нет
keys	tools/ui-audit/check_keys.py@9208dcf:78, tools/ui-audit/check_keys.py@9208dcf:85	нет
kind	tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:121, tools/ui-audit/check_geometry.py@9208dcf:129, tools/ui-audit/check_geometry.py@9208dcf:152, tools/ui-audit/check_scenes.py@9208dcf:32, tools/ui-audit/check_scenes.py@9208dcf:34, tools/ui-audit/check_scenes.py@9208dcf:35	нет
kinds	tools/ui-audit/check_geometry.py@9208dcf:155, tools/ui-audit/check_scenes.py@9208dcf:33, tools/ui-audit/check_scenes.py@9208dcf:34, tools/ui-audit/check_scenes.py@9208dcf:67	нет
label	tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:117, tools/ui-audit/check_geometry.py@9208dcf:145, tools/ui-audit/check_scenes.py@9208dcf:32	нет
language	tools/ui-audit/build_sheets.py@9208dcf:49, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:214, tools/ui-audit/check_credits.py@9208dcf:26, tools/ui-audit/check_geometry.py@9208dcf:41, tools/ui-audit/check_geometry.py@9208dcf:182, tools/ui-audit/combos.py@9208dcf:30, tools/ui-audit/combos.py@9208dcf:36, tools/ui-audit/run_combo.py@9208dcf:61	нет
legacy	tools/ui-audit/check_completeness.py@9208dcf:31, tools/ui-audit/combos.py@9208dcf:32, tools/ui-audit/combos.py@9208dcf:37, tools/ui-audit/combos.py@9208dcf:100, tools/ui-audit/run_all.py@9208dcf:37, tools/ui-audit/run_all.py@9208dcf:40, tools/ui-audit/run_all.py@9208dcf:117, tools/ui-audit/run_all.py@9208dcf:140, tools/ui-audit/run_all.py@9208dcf:141, tools/ui-audit/run_combo.py@9208dcf:97	нет
line	tools/ui-audit/check_keys.py@9208dcf:49, tools/ui-audit/extract_keys.py@9208dcf:58, tools/ui-audit/extract_keys.py@9208dcf:64	нет
log	tools/ui-audit/check_geometry.py@9208dcf:218, tools/ui-audit/check_options_geometry.py@9208dcf:90	нет
logs	tools/ui-audit/check_scenes.py@9208dcf:113, tools/ui-audit/run_all.py@9208dcf:60, tools/ui-audit/run_combo.py@9208dcf:101, tools/ui-audit/run_combo.py@9208dcf:112	нет
logs_root	tools/ui-audit/check_credits.py@9208dcf:43, tools/ui-audit/check_geometry.py@9208dcf:226, tools/ui-audit/check_options_geometry.py@9208dcf:99	нет
map_viewport	tools/ui-audit/check_scenes.py@9208dcf:69, tools/ui-audit/check_scenes.py@9208dcf:80	нет
mods	tools/ui-audit/check_keys.py@9208dcf:44, tools/ui-audit/check_keys.py@9208dcf:50, tools/ui-audit/check_keys.py@9208dcf:86	нет
n	tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:72, tools/ui-audit/check_geometry.py@9208dcf:121	нет
name	tools/ui-audit/check_credits.py@9208dcf:30, tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:136	нет
names	tools/ui-audit/check_geometry.py@9208dcf:60, tools/ui-audit/combos.py@9208dcf:69	нет
no	tools/ui-audit/find_hit_tests.py@9208dcf:31	нет
obj	tools/ui-audit/check_geometry.py@9208dcf:127, tools/ui-audit/check_geometry.py@9208dcf:130, tools/ui-audit/check_geometry.py@9208dcf:147, tools/ui-audit/check_geometry.py@9208dcf:150, tools/ui-audit/check_geometry.py@9208dcf:153, tools/ui-audit/check_geometry.py@9208dcf:205, tools/ui-audit/check_scenes.py@9208dcf:33	нет
objects_intersecting	tools/ui-audit/check_geometry.py@9208dcf:155	нет
objects_total	tools/ui-audit/check_geometry.py@9208dcf:156	нет
other	tools/ui-audit/check_geometry.py@9208dcf:191, tools/ui-audit/check_geometry.py@9208dcf:202, tools/ui-audit/check_geometry.py@9208dcf:203	нет
out	tools/ui-audit/run_combo.py@9208dcf:121	нет
owner	tools/ui-audit/check_scenes.py@9208dcf:33, tools/ui-audit/check_scenes.py@9208dcf:41, tools/ui-audit/check_scenes.py@9208dcf:84	нет
places	tools/ui-audit/check_keys.py@9208dcf:51, tools/ui-audit/check_keys.py@9208dcf:88	нет
png	tools/ui-audit/check_completeness.py@9208dcf:37, tools/ui-audit/finalize_png.py@9208dcf:19, tools/ui-audit/finalize_png.py@9208dcf:44, tools/ui-audit/run_all.py@9208dcf:60, tools/ui-audit/run_combo.py@9208dcf:111	нет
render	tools/ui-audit/build_sheets.py@9208dcf:43, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:215, tools/ui-audit/combos.py@9208dcf:11, tools/ui-audit/combos.py@9208dcf:17, tools/ui-audit/combos.py@9208dcf:31, tools/ui-audit/combos.py@9208dcf:39, tools/ui-audit/run_all.py@9208dcf:25, tools/ui-audit/run_combo.py@9208dcf:59	нет
render_scale	tools/ui-audit/check_geometry.py@9208dcf:42	нет
replace	tools/ui-audit/check_screens.py@9208dcf:59, tools/ui-audit/check_screens.py@9208dcf:63, tools/ui-audit/check_screens.py@9208dcf:65, tools/ui-audit/extract_keys.py@9208dcf:74, tools/ui-audit/find_hit_tests.py@9208dcf:40	нет
resolution	tools/ui-audit/build_sheets.py@9208dcf:49, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:214, tools/ui-audit/check_credits.py@9208dcf:26, tools/ui-audit/check_geometry.py@9208dcf:41, tools/ui-audit/check_geometry.py@9208dcf:186, tools/ui-audit/combos.py@9208dcf:11, tools/ui-audit/combos.py@9208dcf:30, tools/ui-audit/combos.py@9208dcf:36, tools/ui-audit/combos.py@9208dcf:100, tools/ui-audit/run_all.py@9208dcf:41, tools/ui-audit/run_combo.py@9208dcf:40	нет
right	tools/ui-audit/check_scenes.py@9208dcf:26	нет
root	tools/ui-audit/check_completeness.py@9208dcf:52	нет
ru	tools/ui-audit/check_completeness.py@9208dcf:10, tools/ui-audit/combos.py@9208dcf:5	"9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:162:         << outputH << ""\"",\""language\"":\"""" << (localization::isEnglish() ? ""en"" : ""ru"") << ""\"",\""graphics\"":\""hd\"",\""canvas\"":{\""w\"":"" << game.m_screenW"
rule	tools/ui-audit/build_sheets.py@9208dcf:128, tools/ui-audit/build_sheets.py@9208dcf:134, tools/ui-audit/build_sheets.py@9208dcf:138, tools/ui-audit/build_sheets.py@9208dcf:163, tools/ui-audit/build_sheets.py@9208dcf:169, tools/ui-audit/check_geometry.py@9208dcf:54, tools/ui-audit/check_geometry.py@9208dcf:197, tools/ui-audit/check_geometry.py@9208dcf:244, tools/ui-audit/check_keys.py@9208dcf:50, tools/ui-audit/check_keys.py@9208dcf:78, tools/ui-audit/check_options_geometry.py@9208dcf:59, tools/ui-audit/check_options_geometry.py@9208dcf:111, tools/ui-audit/check_options_geometry.py@9208dcf:112, tools/ui-audit/combos.py@9208dcf:69	нет
run	tools/ui-audit/run_all.py@9208dcf:80	нет
runtime	tools/ui-audit/run_combo.py@9208dcf:116	нет
s	tools/ui-audit/check_credits.py@9208dcf:16, tools/ui-audit/check_credits.py@9208dcf:17, tools/ui-audit/check_credits.py@9208dcf:19, tools/ui-audit/check_credits.py@9208dcf:30, tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:72, tools/ui-audit/check_geometry.py@9208dcf:82, tools/ui-audit/check_geometry.py@9208dcf:98, tools/ui-audit/check_geometry.py@9208dcf:103, tools/ui-audit/check_scenes.py@9208dcf:55	нет
scene	tools/ui-audit/build_sheets.py@9208dcf:134, tools/ui-audit/build_sheets.py@9208dcf:138, tools/ui-audit/build_sheets.py@9208dcf:150, tools/ui-audit/build_sheets.py@9208dcf:167, tools/ui-audit/build_sheets.py@9208dcf:169, tools/ui-audit/build_sheets.py@9208dcf:176, tools/ui-audit/build_sheets.py@9208dcf:177, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:206, tools/ui-audit/check_completeness.py@9208dcf:59, tools/ui-audit/check_geometry.py@9208dcf:55, tools/ui-audit/check_geometry.py@9208dcf:147, tools/ui-audit/check_geometry.py@9208dcf:153, tools/ui-audit/check_geometry.py@9208dcf:181, tools/ui-audit/check_geometry.py@9208dcf:197, tools/ui-audit/check_options_geometry.py@9208dcf:55, tools/ui-audit/check_options_geometry.py@9208dcf:73, tools/ui-audit/check_options_geometry.py@9208dcf:75, tools/ui-audit/check_options_geometry.py@9208dcf:76, tools/ui-audit/check_options_geometry.py@9208dcf:85, tools/ui-audit/check_scenes.py@9208dcf:64, tools/ui-audit/check_scenes.py@9208dcf:83, tools/ui-audit/check_scenes.py@9208dcf:91, tools/ui-audit/check_scenes.py@9208dcf:102, tools/ui-audit/combos.py@9208dcf:69, tools/ui-audit/combos.py@9208dcf:93, tools/ui-audit/run_all.py@9208dcf:47, tools/ui-audit/run_combo.py@9208dcf:174	нет
scenes	tools/ui-audit/build_sheets.py@9208dcf:244, tools/ui-audit/check_completeness.py@9208dcf:57, tools/ui-audit/check_screens.py@9208dcf:76, tools/ui-audit/run_all.py@9208dcf:120, tools/ui-audit/run_combo.py@9208dcf:86	нет
scope	tools/ui-audit/combos.py@9208dcf:31, tools/ui-audit/combos.py@9208dcf:59	нет
screen	tools/ui-audit/build_sheets.py@9208dcf:48, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:213, tools/ui-audit/check_screens.py@9208dcf:42	нет
sheets	tools/ui-audit/build_sheets.py@9208dcf:249	нет
skirmish	tools/ui-audit/run_combo.py@9208dcf:16	нет
skirmish_en	tools/ui-audit/run_combo.py@9208dcf:16	нет
software	tools/ui-audit/run_combo.py@9208dcf:69	нет
spice	tools/ui-audit/check_scenes.py@9208dcf:60, tools/ui-audit/check_scenes.py@9208dcf:65	нет
src	tools/ui-audit/extract_keys.py@9208dcf:71	нет
state	tools/ui-audit/build_sheets.py@9208dcf:48, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:213, tools/ui-audit/check_keys.py@9208dcf:31, tools/ui-audit/check_keys.py@9208dcf:50, tools/ui-audit/check_keys.py@9208dcf:78, tools/ui-audit/check_keys.py@9208dcf:84, tools/ui-audit/check_keys.py@9208dcf:87, tools/ui-audit/check_screens.py@9208dcf:42	нет
states	tools/ui-audit/check_keys.py@9208dcf:64, tools/ui-audit/check_keys.py@9208dcf:73	нет
store_true	tools/ui-audit/finalize_png.py@9208dcf:34, tools/ui-audit/run_all.py@9208dcf:105	нет
summary8_out	tools/ui-audit/check_geometry.py@9208dcf:229	нет
t	tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:72, tools/ui-audit/check_options_geometry.py@9208dcf:19	нет
text	tools/ui-audit/check_credits.py@9208dcf:34, tools/ui-audit/check_geometry.py@9208dcf:49, tools/ui-audit/check_geometry.py@9208dcf:66, tools/ui-audit/check_geometry.py@9208dcf:71, tools/ui-audit/check_geometry.py@9208dcf:74, tools/ui-audit/check_geometry.py@9208dcf:174, tools/ui-audit/check_scenes.py@9208dcf:50	нет
texts	tools/ui-audit/build_sheets.py@9208dcf:127, tools/ui-audit/check_geometry.py@9208dcf:59, tools/ui-audit/check_geometry.py@9208dcf:206, tools/ui-audit/check_geometry.py@9208dcf:207	нет
timeout	tools/ui-audit/run_combo.py@9208dcf:135	нет
top	tools/ui-audit/check_scenes.py@9208dcf:26	нет
txt_out	tools/ui-audit/check_geometry.py@9208dcf:228	нет
type	tools/ui-audit/check_geometry.py@9208dcf:127, tools/ui-audit/check_geometry.py@9208dcf:131, tools/ui-audit/check_geometry.py@9208dcf:147, tools/ui-audit/check_geometry.py@9208dcf:150, tools/ui-audit/check_geometry.py@9208dcf:153, tools/ui-audit/check_geometry.py@9208dcf:155, tools/ui-audit/check_geometry.py@9208dcf:204, tools/ui-audit/check_geometry.py@9208dcf:205	нет
w	tools/ui-audit/build_sheets.py@9208dcf:64, tools/ui-audit/build_sheets.py@9208dcf:113, tools/ui-audit/build_sheets.py@9208dcf:122, tools/ui-audit/check_geometry.py@9208dcf:22, tools/ui-audit/check_geometry.py@9208dcf:26, tools/ui-audit/check_geometry.py@9208dcf:32, tools/ui-audit/check_geometry.py@9208dcf:37, tools/ui-audit/check_geometry.py@9208dcf:65, tools/ui-audit/check_geometry.py@9208dcf:102, tools/ui-audit/check_geometry.py@9208dcf:181, tools/ui-audit/check_geometry.py@9208dcf:201, tools/ui-audit/check_scenes.py@9208dcf:19, tools/ui-audit/extract_keys.py@9208dcf:85, tools/ui-audit/run_all.py@9208dcf:85	нет
work	tools/ui-audit/run_combo.py@9208dcf:115	нет
world	tools/ui-audit/build_sheets.py@9208dcf:43, tools/ui-audit/build_sheets.py@9208dcf:200, tools/ui-audit/build_sheets.py@9208dcf:215, tools/ui-audit/combos.py@9208dcf:11, tools/ui-audit/combos.py@9208dcf:24, tools/ui-audit/combos.py@9208dcf:31, tools/ui-audit/combos.py@9208dcf:39, tools/ui-audit/run_all.py@9208dcf:25, tools/ui-audit/run_combo.py@9208dcf:60	нет
world_scale	tools/ui-audit/check_geometry.py@9208dcf:42	нет
x	tools/ui-audit/build_sheets.py@9208dcf:63, tools/ui-audit/build_sheets.py@9208dcf:64, tools/ui-audit/build_sheets.py@9208dcf:121, tools/ui-audit/check_geometry.py@9208dcf:22, tools/ui-audit/check_geometry.py@9208dcf:26, tools/ui-audit/check_geometry.py@9208dcf:31, tools/ui-audit/check_geometry.py@9208dcf:32, tools/ui-audit/check_geometry.py@9208dcf:65, tools/ui-audit/check_geometry.py@9208dcf:201, tools/ui-audit/check_scenes.py@9208dcf:19, tools/ui-audit/run_combo.py@9208dcf:40	"9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp:379:        std::string json = ""{\""resolution\"":\"""" + std::to_string(width) + ""x"" + std::to_string(height) +"
y	tools/ui-audit/build_sheets.py@9208dcf:63, tools/ui-audit/build_sheets.py@9208dcf:64, tools/ui-audit/build_sheets.py@9208dcf:121, tools/ui-audit/check_credits.py@9208dcf:16, tools/ui-audit/check_credits.py@9208dcf:17, tools/ui-audit/check_geometry.py@9208dcf:22, tools/ui-audit/check_geometry.py@9208dcf:27, tools/ui-audit/check_geometry.py@9208dcf:31, tools/ui-audit/check_geometry.py@9208dcf:33, tools/ui-audit/check_geometry.py@9208dcf:65, tools/ui-audit/check_geometry.py@9208dcf:201, tools/ui-audit/check_scenes.py@9208dcf:15, tools/ui-audit/check_scenes.py@9208dcf:23	нет
yes	tools/ui-audit/find_hit_tests.py@9208dcf:31	нет
~~~~

#### scene-refs.tsv

~~~~text
значение	путь@9208dcf:строка	совпадение	число сцен
Check options-window logs with audit rules 3 and 9.	tools/ui-audit/check_options_geometry.py@9208dcf:98	префикс options-	13
credits-*.geometry.jsonl	tools/ui-audit/check_credits.py@9208dcf:24	префикс credits-	6
options-game-main-nosaves	tools/ui-audit/check_options_geometry.py@9208dcf:14	сцена	1
options-game-main-saves	tools/ui-audit/check_options_geometry.py@9208dcf:13	сцена	1
options-menu-main	tools/ui-audit/check_options_geometry.py@9208dcf:12	сцена	1
structure-health	tools/ui-audit/check_scenes.py@9208dcf:77	префикс structure-	2
structure-label-right	tools/ui-audit/check_scenes.py@9208dcf:26	сцена	1
structure-label-top	tools/ui-audit/check_scenes.py@9208dcf:26	сцена	1
units-label-	tools/ui-audit/check_scenes.py@9208dcf:9	префикс units-	18
~~~~

## 4. Запуск игры: форк и порт

Команды и выводы чтения функций, проверки аргументов, настроек, файлов, пользовательских настроек, загрузчика settings.ini, окружения сборки и Python/CTest:

#### launch-command-log.txt

~~~~text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_combo.py | nl -ba | sed -n '28,36p'
    28	def apply_settings(text, values):
    29	    for key, value in values.items():
    30	        pattern = re.compile(rf"^{key}\s*=.*$", re.MULTILINE)
    31	        line = f"{key}={value}"
    32	        if pattern.search(text):
    33	            text = pattern.sub(line, text, count=1)
    34	        else:
    35	            text = text.replace("[SETTINGS]", f"[SETTINGS]\n{line}", 1)
    36	    return text
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_combo.py | nl -ba | sed -n '44,64p'
    44	def make_runtime(executable, resources, directory, combo):
    45	    width, height = split_resolution(combo)
    46	    runtime = Path(directory)
    47	    if runtime.exists():
    48	        shutil.rmtree(runtime)
    49	    runtime.mkdir(parents=True)
    50	    shutil.copy2(executable, runtime / "d2tm")
    51	    bin_dir = Path(resources) / "bin"
    52	    for name in RUNTIME_LINKS:
    53	        os.symlink(bin_dir / name, runtime / name)
    54	    shutil.copy2(Path(resources) / "game.ini", runtime / "game.ini")
    55	    settings = apply_settings((bin_dir / "settings.ini").read_text(encoding="utf-8"), {
    56	        "ScreenWidth": width,
    57	        "ScreenHeight": height,
    58	        "FullScreen": "false",
    59	        "RenderScale": combo["render"],
    60	        "WorldScale": combo["world"],
    61	        "Language": combo["language"],
    62	    })
    63	    (runtime / "settings.ini").write_text(settings, encoding="utf-8")
    64	    return runtime
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_combo.py | nl -ba | sed -n '67,70p'
    67	def game_environment():
    68	    environment = dict(os.environ)
    69	    environment.update(SDL_VIDEODRIVER="dummy", SDL_RENDER_DRIVER="software", SDL_AUDIODRIVER="dummy")
    70	    return environment
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_combo.py | nl -ba | sed -n '73,80p'
    73	def run_scene(runtime, combo, scene_id, out_dir):
    74	    width, height = split_resolution(combo)
    75	    command = [
    76	        str(runtime / "d2tm"), "-windowed", "-screenWidth", str(width), "-screenHeight", str(height),
    77	        "--ui-audit-scene", scene_id, "--ui-audit-out", str(out_dir),
    78	    ]
    79	    return subprocess.run(command, cwd=runtime, env=game_environment(), check=False,
    80	                          capture_output=True, text=True, timeout=SCENE_TIMEOUT_SECONDS)
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_combo.py | nl -ba | sed -n '83,86p'
    83	def list_scenes(executable):
    84	    result = subprocess.run([str(executable), "--ui-audit-list"], env=game_environment(), check=True,
    85	                            capture_output=True, text=True, timeout=60)
    86	    return json.loads(result.stdout)["scenes"]
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_all.py | nl -ba | sed -n '19,26p'
    19	def scales_for(executable, resolutions):
    20	    scales = {}
    21	    for resolution in resolutions:
    22	        result = subprocess.run([str(executable), "--ui-audit-scales", resolution], env=run_combo.game_environment(),
    23	                                check=True, capture_output=True, text=True, timeout=60)
    24	        _, render, world = combos.parse_scales(result.stdout)
    25	        scales[resolution] = {"render": [value for value in render if value], "world": [value for value in world if value]}
    26	    return scales
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_all.py | nl -ba | sed -n '73,91p'
    73	def run_one(args, combo, journal):
    74	    identifier = combos.combo_id(combo)
    75	    free = run_combo.free_gb(args.out)
    76	    journal.write(f"{time.strftime('%F %T')} free {free:.1f} GB before {identifier}\n")
    77	    journal.flush()
    78	    if free < args.min_free_gb:
    79	        return identifier, 3
    80	    log_path = Path(args.out) / "run" / (identifier.replace("/", "_") + ".txt")
    81	    log_path.parent.mkdir(parents=True, exist_ok=True)
    82	    command = [sys.executable, str(Path(__file__).resolve().parent / "run_combo.py"), "--exe", args.exe,
    83	               "--resources", args.resources, "--out", args.out, "--combo", identifier,
    84	               "--min-free-gb", str(args.min_free_gb)]
    85	    with open(log_path, "w", encoding="utf-8") as log:
    86	        code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    87	    if code == 0:
    88	        marker = done_marker(args.out, combo)
    89	        marker.parent.mkdir(parents=True, exist_ok=True)
    90	        marker.write_text("ok\n", encoding="utf-8")
    91	    return identifier, code
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/finalize_png.py | nl -ba | sed -n '27,55p'
    27	def main(argv=None):
    28	    parser = argparse.ArgumentParser(
    29	        description="Leave PNG only for the first flag with a given key per resolution; capture the ones still missing.")
    30	    parser.add_argument("--exe", required=True)
    31	    parser.add_argument("--resources", required=True)
    32	    parser.add_argument("--out", required=True)
    33	    parser.add_argument("--flags", required=True, help="flags JSON from check_geometry.py")
    34	    parser.add_argument("--dry-run", action="store_true")
    35	    args = parser.parse_args(argv)
    36	    out = Path(args.out)
    37	    order = json.loads((out / "order.json").read_text(encoding="utf-8"))
    38	    flags = json.loads(Path(args.flags).read_text(encoding="utf-8"))
    39	    missing, extra = plan_actions(out, flags, order)
    40	    print(f"extra PNG: {len(extra)}; missing PNG: {len(missing)}")
    41	    if args.dry_run:
    42	        return 0
    43	    for identifier, scene in extra:
    44	        (out / "png" / identifier / f"{scene}.png").unlink()
    45	    by_combo = defaultdict(list)
    46	    for identifier, scene in missing:
    47	        by_combo[identifier].append(scene)
    48	    code = 0
    49	    for identifier, scenes in by_combo.items():
    50	        command = [sys.executable, str(Path(__file__).resolve().parent / "run_combo.py"), "--exe", args.exe,
    51	                   "--resources", args.resources, "--out", str(out), "--combo", identifier]
    52	        for scene in scenes:
    53	            command += ["--scene", scene]
    54	        code = max(code, subprocess.run(command, check=False).returncode)
    55	    return code
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--exe"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--resources"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--out"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--flags"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--dry-run"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--exe"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--resources"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--out"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--combo"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--scene"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--ui-audit-scales"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--exe"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--resources"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--out"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--combo"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--min-free-gb"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"-windowed"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/cHandleArgument.cpp:23:    {"-windowed",               Options::WINDOWED},
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"-screenWidth"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/cHandleArgument.cpp:34:    {"-screenWidth",            Options::SCREENX},
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"-screenHeight"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/cHandleArgument.cpp:35:    {"-screenHeight",           Options::SCREENY},
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--ui-audit-scene"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--ui-audit-out"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F -e '"--ui-audit-list"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -3
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^ScreenWidth='
3:ScreenWidth=1024
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"ScreenWidth"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:86:    if (section.hasValue("ScreenWidth")) {
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:87:        settings.screenW = section.getInt("ScreenWidth");
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:182:    set(ini, "ScreenWidth", std::to_string(settings.screenW));
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^ScreenHeight='
4:ScreenHeight=768
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"ScreenHeight"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:89:    if (section.hasValue("ScreenHeight")) {
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:90:        settings.screenH = section.getInt("ScreenHeight");
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:183:    set(ini, "ScreenHeight", std::to_string(settings.screenH));
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^FullScreen='
10:FullScreen=false
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"FullScreen"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:98:    if (section.hasValue("FullScreen")) {
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:99:        settings.windowed = !section.getBoolean("FullScreen");
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:186:    set(ini, "FullScreen", toText(!settings.windowed));
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^RenderScale='
12:RenderScale=0
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"RenderScale"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:104:    if (section.hasValue("RenderScale")) {
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:105:        settings.renderScalePercent = section.getInt("RenderScale");
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:188:    set(ini, "RenderScale", std::to_string(settings.renderScalePercent));
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:223:    set(ini, "RenderScale", std::to_string(renderScalePercent));
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:236:    if (section.hasValue("RenderScale")) {
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^WorldScale='
нет
[exit 1]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"WorldScale"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:107:    if (section.hasValue("WorldScale")) {
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:108:        settings.worldScalePercent = section.getInt("WorldScale");
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:189:    set(ini, "WorldScale", std::to_string(settings.worldScalePercent));
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:224:    set(ini, "WorldScale", std::to_string(worldScalePercent));
5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:239:    if (section.hasValue("WorldScale")) {
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^Language='
нет
[exit 1]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"Language"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/campaign resources/campaign
040000 tree 1d78e538bed17d2d408922fb68dce75446db2c64	resources/bin/campaign
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/campaign resources/campaign
040000 tree a7dd3ac6c95570c5f9b272ca8ab12161c9e39d4c	resources/bin/campaign
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/campaign_en resources/campaign_en
040000 tree e420c95958690e97845e94ab0036f9cf4c4ced7d	resources/bin/campaign_en
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/campaign_en resources/campaign_en
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/data resources/data
040000 tree 6c2458699107335c49177743addff0bacd54d5bf	resources/bin/data
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/data resources/data
040000 tree cc6cc1f3161f43e55e96d4878646d578509d57cc	resources/bin/data
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/skirmish resources/skirmish
040000 tree 8b97f75db2e891a72b376256fe4e8810b2236171	resources/bin/skirmish
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/skirmish resources/skirmish
040000 tree dca16b79fc302e4d16d2803153aeb8102cef6a57	resources/bin/skirmish
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/skirmish_en resources/skirmish_en
040000 tree 526906dc67dd8b566e08ae7db643ed161fb44a5d	resources/bin/skirmish_en
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/skirmish_en resources/skirmish_en
нет
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/game.ini resources/game.ini
100644 blob c45bc861a56cb964ad609877f05dd6eaa79a1efa	resources/game.ini
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/game.ini resources/game.ini
100644 blob 7feed737476e58f5645189c100cae77f4a8a0231	resources/game.ini
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/settings.ini resources/settings.ini
100644 blob 636898ad4ca47088d4374950f6e71ba802d5f431	resources/bin/settings.ini
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/settings.ini resources/settings.ini
100644 blob d3f475fc78e9416d32f6987633f5664c53f8e626	resources/bin/settings.ini
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp | nl -ba | grep '"'
    17	#include "game/Preferences.hpp"
    19	#include "utils/cIniFile.h"
    20	#include "utils/InitialGameSettings.hpp"
    25	constexpr const char *SECTION = "SETTINGS";
    36	    return value ? "true" : "false";
    48	        error = "No preferences file found at " + utf8FileName(file);
    53	        error = "Preferences file is unusable: " + utf8FileName(file);
    64	        error = "Could not create preferences directory: " + filesystemError.message();
    70	    tempPath += ".tmp";
    72	        error = "Could not write preferences file";
    77	        error = "Could not replace preferences file: " + filesystemError.message();
    86	    if (section.hasValue("ScreenWidth")) {
    87	        settings.screenW = section.getInt("ScreenWidth");
    89	    if (section.hasValue("ScreenHeight")) {
    90	        settings.screenH = section.getInt("ScreenHeight");
    92	    if (section.hasValue("CameraDragMoveSpeed")) {
    93	        settings.cameraDragMoveSpeed = section.getDouble("CameraDragMoveSpeed");
    95	    if (section.hasValue("CameraBorderOrKeyMoveSpeed")) {
    96	        settings.cameraBorderOrKeyMoveSpeed = section.getDouble("CameraBorderOrKeyMoveSpeed");
    98	    if (section.hasValue("FullScreen")) {
    99	        settings.windowed = !section.getBoolean("FullScreen");
   101	    if (section.hasValue("CameraEdgeMove")) {
   102	        settings.cameraEdgeMove = section.getBoolean("CameraEdgeMove");
   104	    if (section.hasValue("RenderScale")) {
   105	        settings.renderScalePercent = section.getInt("RenderScale");
   107	    if (section.hasValue("WorldScale")) {
   108	        settings.worldScalePercent = section.getInt("WorldScale");
   110	    if (section.hasValue("AllowRepeatingReinforcements")) {
   111	        settings.allowRepeatingReinforcements = section.getBoolean("AllowRepeatingReinforcements");
   113	    if (section.hasValue("AllTurretsDownOnLowPower")) {
   114	        settings.turretsDownOnLowPower = section.getBoolean("AllTurretsDownOnLowPower");
   116	    if (section.hasValue("ShowLowPowerIcon")) {
   117	        settings.showLowPowerIcon = section.getBoolean("ShowLowPowerIcon");
   119	    if (section.hasValue("RocketTurretsDownOnLowPower")) {
   120	        settings.rocketTurretsDownOnLowPower = section.getBoolean("RocketTurretsDownOnLowPower");
   122	    if (section.hasValue("GameRules")) {
   123	        settings.gameFilename = section.getStringValue("GameRules");
   125	    if (section.hasValue("NoAI")) {
   126	        settings.disableAI = section.getBoolean("NoAI");
   128	    if (section.hasValue("Debug")) {
   129	        settings.debugMode = section.getBoolean("Debug");
   131	    if (section.hasValue("playMusic")) {
   132	        settings.playMusic = section.getBoolean("playMusic");
   134	    if (section.hasValue("customMusic")) {
   135	        settings.customMusic = section.getBoolean("customMusic");
   137	    if (section.hasValue("playSound")) {
   138	        settings.playSound = section.getBoolean("playSound");
   140	    if (section.hasValue("playCreditsSound")) {
   141	        settings.playCreditsSound = section.getBoolean("playCreditsSound");
   143	    if (section.hasValue("drawUnitDebug")) {
   144	        settings.drawUnitDebug = section.getBoolean("drawUnitDebug");
   146	    if (section.hasValue("oneAi")) {
   147	        settings.oneAi = section.getBoolean("oneAi");
   149	    if (section.hasValue("disableWormAi")) {
   150	        settings.disableWormAi = section.getBoolean("disableWormAi");
   152	    if (section.hasValue("disableReinforcements")) {
   153	        settings.disableReinforcements = section.getBoolean("disableReinforcements");
   155	    if (section.hasValue("noAiRest")) {
   156	        settings.noAiRest = section.getBoolean("noAiRest");
   158	    if (section.hasValue("drawUsages")) {
   159	        settings.drawUsages = section.getBoolean("drawUsages");
   161	    if (section.hasValue("pauseWhenLosingFocus")) {
   162	        settings.pauseWhenLosingFocus = section.getBoolean("pauseWhenLosingFocus");
   164	    if (section.hasValue("fogOfWarEnabled")) {
   165	        settings.fogOfWarEnabled = section.getBoolean("fogOfWarEnabled");
   182	    set(ini, "ScreenWidth", std::to_string(settings.screenW));
   183	    set(ini, "ScreenHeight", std::to_string(settings.screenH));
   184	    set(ini, "CameraDragMoveSpeed", std::to_string(settings.cameraDragMoveSpeed));
   185	    set(ini, "CameraBorderOrKeyMoveSpeed", std::to_string(settings.cameraBorderOrKeyMoveSpeed));
   186	    set(ini, "FullScreen", toText(!settings.windowed));
   187	    set(ini, "CameraEdgeMove", toText(settings.cameraEdgeMove));
   188	    set(ini, "RenderScale", std::to_string(settings.renderScalePercent));
   189	    set(ini, "WorldScale", std::to_string(settings.worldScalePercent));
   190	    set(ini, "AllowRepeatingReinforcements", toText(settings.allowRepeatingReinforcements));
   191	    set(ini, "AllTurretsDownOnLowPower", toText(settings.turretsDownOnLowPower));
   192	    set(ini, "RocketTurretsDownOnLowPower", toText(settings.rocketTurretsDownOnLowPower));
   193	    set(ini, "ShowLowPowerIcon", toText(settings.showLowPowerIcon));
   194	    set(ini, "GameRules", settings.gameFilename);
   195	    set(ini, "NoAI", toText(settings.disableAI));
   196	    set(ini, "Debug", toText(settings.debugMode));
   197	    set(ini, "playMusic", toText(settings.playMusic));
   198	    set(ini, "customMusic", toText(settings.customMusic));
   199	    set(ini, "playSound", toText(settings.playSound));
   200	    set(ini, "playCreditsSound", toText(settings.playCreditsSound));
   201	    set(ini, "drawUnitDebug", toText(settings.drawUnitDebug));
   202	    set(ini, "oneAi", toText(settings.oneAi));
   203	    set(ini, "disableWormAi", toText(settings.disableWormAi));
   204	    set(ini, "disableReinforcements", toText(settings.disableReinforcements));
   205	    set(ini, "noAiRest", toText(settings.noAiRest));
   206	    set(ini, "drawUsages", toText(settings.drawUsages));
   207	    set(ini, "pauseWhenLosingFocus", toText(settings.pauseWhenLosingFocus));
   208	    set(ini, "fogOfWarEnabled", toText(settings.fogOfWarEnabled));
   223	    set(ini, "RenderScale", std::to_string(renderScalePercent));
   224	    set(ini, "WorldScale", std::to_string(worldScalePercent));
   236	    if (section.hasValue("RenderScale")) {
   237	        settings.renderScalePercent = section.getInt("RenderScale");
   239	    if (section.hasValue("WorldScale")) {
   240	        settings.worldScalePercent = section.getInt("WorldScale");
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -w 'loadSettingsFromIni' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src
5e9059778bd59e486a58a899c9cf56f6758ed178:src/main.cpp:72:    std::unique_ptr<InitialGameSettings> settings = loadSettingsFromIni("settings.ini");
5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/common.cpp:44:std::unique_ptr<InitialGameSettings> loadSettingsFromIni(const std::string& filename)
5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/common.cpp:50:        Logger::error(COMP_GAMERULES, "loadSettingsFromIni", "Expected to find [SETTINGS] in {}", filename);
5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/common.h:62:std::unique_ptr<InitialGameSettings> loadSettingsFromIni(const std::string& filename);
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/common.cpp | nl -ba | sed -n '44,64p'
    44	std::unique_ptr<InitialGameSettings> loadSettingsFromIni(const std::string& filename)
    45	{
    46	    std::shared_ptr<cIniFile> file = std::make_shared<cIniFile>(filename);
    47	    std::unique_ptr<InitialGameSettings> gameSettings = std::make_unique<InitialGameSettings>();
    48	
    49	    if (!file->hasSection("SETTINGS")) {
    50	        Logger::error(COMP_GAMERULES, "loadSettingsFromIni", "Expected to find [SETTINGS] in {}", filename);
    51	        return gameSettings;
    52	    }
    53	
    54	    const cSection &section = file->getSection("SETTINGS");
    55	    Preferences::readSettings(section, *gameSettings);
    56	
    57	    if (!section.hasValue("CameraEdgeMove")) {
    58	        // no explicit setting: default off when windowed (edge-scrolling fights
    59	        // with normal window interactions), on when fullscreen
    60	        gameSettings->cameraEdgeMove = !gameSettings->windowed;
    61	    }
    62	
    63	    return gameSettings;
    64	}
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'XDG|environ|LD_LIBRARY_PATH|SDL_' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- tests/ui_audit tools/upstream/build_upstream_linux.sh
5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:24:        environment = dict(os.environ)
5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:25:        environment.update(
5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:26:            SDL_VIDEODRIVER="dummy",
5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:27:            SDL_RENDER_DRIVER="software",
5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:28:            SDL_AUDIODRIVER="dummy",
5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:29:            XDG_DATA_HOME=str(self.xdg),
5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:34:            env=environment,
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:51:                -DSDL_INSTALL=ON -DSDL_SHARED=ON -DSDL_STATIC=OFF
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:52:                -DSDL_TEST_LIBRARY=OFF -DSDL_TESTS=OFF -DSDL_EXAMPLES=OFF
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:53:                -DSDL_AUDIO=ON -DSDL_VIDEO=ON -DSDL_RENDER=ON
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:54:                -DSDL_DUMMYAUDIO=ON -DSDL_DUMMYVIDEO=ON -DSDL_OFFSCREEN=ON
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:55:                -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF -DSDL_JACK=OFF
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:56:                -DSDL_PIPEWIRE=OFF -DSDL_SNDIO=OFF -DSDL_X11=OFF
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:57:                -DSDL_WAYLAND=OFF -DSDL_KMSDRM=OFF -DSDL_OPENGL=OFF
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:58:                -DSDL_OPENGLES=OFF -DSDL_VULKAN=OFF -DSDL_UNIX_CONSOLE_BUILD=ON
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:61:        SDL_image)
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:73:        SDL_ttf)
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:82:        SDL_mixer)
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:127:    if [[ "$name" == SDL_ttf ]]; then
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:140:        SDL_image|SDL_ttf|SDL_mixer)
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:160:    printf 'Команда: SDL_VIDEODRIVER=%s SDL_AUDIODRIVER=dummy XDG_DATA_HOME=%q timeout 20 ./d2tm\n' \
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:163:        SDL_VIDEODRIVER="$driver" SDL_AUDIODRIVER=dummy \
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:164:        XDG_DATA_HOME="$DUNE_OUT_DIR/xdg" timeout 20 ./d2tm) \
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:197:    printf '%s\0' SDL_image SDL_ttf SDL_mixer |
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:208:    export LD_LIBRARY_PATH="$library_dir"
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:210:    printf 'CPATH=%s\nLIBRARY_PATH=%s\nLD_LIBRARY_PATH=%s\n' "$CPATH" "$LIBRARY_PATH" "$LD_LIBRARY_PATH"
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:255:    for name in SDL SDL_image SDL_ttf SDL_mixer Catch2; do
5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:260:    printf 'Запуск: SDL_VIDEODRIVER=%s; код timeout=%s\n' "$selected_driver" "$game_status"
[exit 0]

$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -E 'python|unittest|pytest' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- .github CMakeLists.txt tests/CMakeLists.txt tools/upstream/build_upstream_linux.sh | head -40
5e9059778bd59e486a58a899c9cf56f6758ed178:.github/workflows/build_manual.yml:100:        uses: actions/setup-python@v3
5e9059778bd59e486a58a899c9cf56f6758ed178:.github/workflows/build_manual.yml:102:          python-version: "3.14"
[exit 0]
~~~~

#### launch-extraction.log

~~~~text
functions=8
dash_literals=22
settings_keys=6
runtime_links=5
rows=178
~~~~

#### fork-launch-run_combo.txt

~~~~text
    16	RUNTIME_LINKS = ("campaign", "campaign_en", "data", "skirmish", "skirmish_en")
    17	FULL_RESOLUTIONS = ("1024x768", "1920x1080")
    18	SCENE_TIMEOUT_SECONDS = 90
    19	SCENE_ATTEMPTS = 2
    20	MIN_FREE_GB = 5
    21	EXIT_LOW_DISK = 3
    22	
    23	
    24	def free_gb(path):
    25	    return shutil.disk_usage(path).free / (1024 ** 3)
    26	
    27	
    28	def apply_settings(text, values):
    29	    for key, value in values.items():
    30	        pattern = re.compile(rf"^{key}\s*=.*$", re.MULTILINE)
    31	        line = f"{key}={value}"
    32	        if pattern.search(text):
    33	            text = pattern.sub(line, text, count=1)
    34	        else:
    35	            text = text.replace("[SETTINGS]", f"[SETTINGS]\n{line}", 1)
    36	    return text
    37	
    38	
    39	def split_resolution(combo):
    40	    width, height = combo["resolution"].split("x")
    41	    return int(width), int(height)
    42	
    43	
    44	def make_runtime(executable, resources, directory, combo):
    45	    width, height = split_resolution(combo)
    46	    runtime = Path(directory)
    47	    if runtime.exists():
    48	        shutil.rmtree(runtime)
    49	    runtime.mkdir(parents=True)
    50	    shutil.copy2(executable, runtime / "d2tm")
    51	    bin_dir = Path(resources) / "bin"
    52	    for name in RUNTIME_LINKS:
    53	        os.symlink(bin_dir / name, runtime / name)
    54	    shutil.copy2(Path(resources) / "game.ini", runtime / "game.ini")
    55	    settings = apply_settings((bin_dir / "settings.ini").read_text(encoding="utf-8"), {
    56	        "ScreenWidth": width,
    57	        "ScreenHeight": height,
    58	        "FullScreen": "false",
    59	        "RenderScale": combo["render"],
    60	        "WorldScale": combo["world"],
    61	        "Language": combo["language"],
    62	    })
    63	    (runtime / "settings.ini").write_text(settings, encoding="utf-8")
    64	    return runtime
    65	
    66	
    67	def game_environment():
    68	    environment = dict(os.environ)
    69	    environment.update(SDL_VIDEODRIVER="dummy", SDL_RENDER_DRIVER="software", SDL_AUDIODRIVER="dummy")
    70	    return environment
    71	
    72	
    73	def run_scene(runtime, combo, scene_id, out_dir):
    74	    width, height = split_resolution(combo)
    75	    command = [
    76	        str(runtime / "d2tm"), "-windowed", "-screenWidth", str(width), "-screenHeight", str(height),
    77	        "--ui-audit-scene", scene_id, "--ui-audit-out", str(out_dir),
    78	    ]
    79	    return subprocess.run(command, cwd=runtime, env=game_environment(), check=False,
    80	                          capture_output=True, text=True, timeout=SCENE_TIMEOUT_SECONDS)
    81	
    82	
    83	def list_scenes(executable):
    84	    result = subprocess.run([str(executable), "--ui-audit-list"], env=game_environment(), check=True,
    85	                            capture_output=True, text=True, timeout=60)
    86	    return json.loads(result.stdout)["scenes"]
    87	
    88	
    89	def load_order(out_root):
    90	    path = Path(out_root) / "order.json"
    91	    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
    92	
    93	
    94	def has_new_flag(out_root, order, combo, scene_id, log_path):
    95	    flags = check_geometry.check_log(log_path)
~~~~

#### fork-launch-run_all.txt

~~~~text
    19	def scales_for(executable, resolutions):
    20	    scales = {}
    21	    for resolution in resolutions:
    22	        result = subprocess.run([str(executable), "--ui-audit-scales", resolution], env=run_combo.game_environment(),
    23	                                check=True, capture_output=True, text=True, timeout=60)
    24	        _, render, world = combos.parse_scales(result.stdout)
    25	        scales[resolution] = {"render": [value for value in render if value], "world": [value for value in world if value]}
    26	    return scales
    27	
    28	
    29	def interleave(chains):
    73	def run_one(args, combo, journal):
    74	    identifier = combos.combo_id(combo)
    75	    free = run_combo.free_gb(args.out)
    76	    journal.write(f"{time.strftime('%F %T')} free {free:.1f} GB before {identifier}\n")
    77	    journal.flush()
    78	    if free < args.min_free_gb:
    79	        return identifier, 3
    80	    log_path = Path(args.out) / "run" / (identifier.replace("/", "_") + ".txt")
    81	    log_path.parent.mkdir(parents=True, exist_ok=True)
    82	    command = [sys.executable, str(Path(__file__).resolve().parent / "run_combo.py"), "--exe", args.exe,
    83	               "--resources", args.resources, "--out", args.out, "--combo", identifier,
    84	               "--min-free-gb", str(args.min_free_gb)]
    85	    with open(log_path, "w", encoding="utf-8") as log:
    86	        code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    87	    if code == 0:
    88	        marker = done_marker(args.out, combo)
    89	        marker.parent.mkdir(parents=True, exist_ok=True)
    90	        marker.write_text("ok\n", encoding="utf-8")
    91	    return identifier, code
    92	
    93	
    94	def main(argv=None):
    95	    parser = argparse.ArgumentParser(description="Capture all combinations, 16 at a time, skipping finished ones.")
    96	    parser.add_argument("--exe", required=True)
    97	    parser.add_argument("--resources", required=True)
    98	    parser.add_argument("--out", required=True)
~~~~

#### fork-launch-finalize_png.txt

~~~~text
    13	def plan_actions(out_root, flags, ordered_ids):
    14	    needed = defaultdict(set)
    15	    for combo, scene in combos.png_required(flags, ordered_ids):
    16	        needed[combo].add(scene)
    17	    missing, extra = [], []
    18	    for identifier in ordered_ids:
    19	        png_dir = Path(out_root) / "png" / identifier
    20	        have = {path.stem for path in png_dir.glob("*.png")} if png_dir.is_dir() else set()
    21	        missing += [(identifier, scene) for scene in sorted(needed[identifier] - have)]
    22	        if identifier.count("/") != 2:
    23	            extra += [(identifier, scene) for scene in sorted(have - needed[identifier])]
    24	    return missing, extra
    25	
    26	
    27	def main(argv=None):
    28	    parser = argparse.ArgumentParser(
    29	        description="Leave PNG only for the first flag with a given key per resolution; capture the ones still missing.")
    30	    parser.add_argument("--exe", required=True)
    31	    parser.add_argument("--resources", required=True)
    32	    parser.add_argument("--out", required=True)
    33	    parser.add_argument("--flags", required=True, help="flags JSON from check_geometry.py")
    34	    parser.add_argument("--dry-run", action="store_true")
    35	    args = parser.parse_args(argv)
    36	    out = Path(args.out)
    37	    order = json.loads((out / "order.json").read_text(encoding="utf-8"))
    38	    flags = json.loads(Path(args.flags).read_text(encoding="utf-8"))
    39	    missing, extra = plan_actions(out, flags, order)
    40	    print(f"extra PNG: {len(extra)}; missing PNG: {len(missing)}")
    41	    if args.dry_run:
    42	        return 0
    43	    for identifier, scene in extra:
    44	        (out / "png" / identifier / f"{scene}.png").unlink()
    45	    by_combo = defaultdict(list)
    46	    for identifier, scene in missing:
    47	        by_combo[identifier].append(scene)
    48	    code = 0
    49	    for identifier, scenes in by_combo.items():
    50	        command = [sys.executable, str(Path(__file__).resolve().parent / "run_combo.py"), "--exe", args.exe,
    51	                   "--resources", args.resources, "--out", str(out), "--combo", identifier]
    52	        for scene in scenes:
    53	            command += ["--scene", scene]
    54	        code = max(code, subprocess.run(command, check=False).returncode)
    55	    return code
    56	
    57	
    58	if __name__ == "__main__":
~~~~

Таблица `launch.tsv`: 178 строк данных.

#### launch.tsv

~~~~text
что	путь@ревизия:строка или команда	значение
Функция apply_settings	tools/ui-audit/run_combo.py@9208dcf:28	"    28\tdef apply_settings(text, values):\n    29\t    for key, value in values.items():\n    30\t        pattern = re.compile(rf\"^{key}\\s*=.*$\", re.MULTILINE)\n    31\t        line = f\"{key}={value}\"\n    32\t        if pattern.search(text):\n    33\t            text = pattern.sub(line, text, count=1)\n    34\t        else:\n    35\t            text = text.replace(\"[SETTINGS]\", f\"[SETTINGS]\\n{line}\", 1)\n    36\t    return text"
Функция make_runtime	tools/ui-audit/run_combo.py@9208dcf:44	"    44\tdef make_runtime(executable, resources, directory, combo):\n    45\t    width, height = split_resolution(combo)\n    46\t    runtime = Path(directory)\n    47\t    if runtime.exists():\n    48\t        shutil.rmtree(runtime)\n    49\t    runtime.mkdir(parents=True)\n    50\t    shutil.copy2(executable, runtime / \"d2tm\")\n    51\t    bin_dir = Path(resources) / \"bin\"\n    52\t    for name in RUNTIME_LINKS:\n    53\t        os.symlink(bin_dir / name, runtime / name)\n    54\t    shutil.copy2(Path(resources) / \"game.ini\", runtime / \"game.ini\")\n    55\t    settings = apply_settings((bin_dir / \"settings.ini\").read_text(encoding=\"utf-8\"), {\n    56\t        \"ScreenWidth\": width,\n    57\t        \"ScreenHeight\": height,\n    58\t        \"FullScreen\": \"false\",\n    59\t        \"RenderScale\": combo[\"render\"],\n    60\t        \"WorldScale\": combo[\"world\"],\n    61\t        \"Language\": combo[\"language\"],\n    62\t    })\n    63\t    (runtime / \"settings.ini\").write_text(settings, encoding=\"utf-8\")\n    64\t    return runtime"
Функция game_environment	tools/ui-audit/run_combo.py@9208dcf:67	"    67\tdef game_environment():\n    68\t    environment = dict(os.environ)\n    69\t    environment.update(SDL_VIDEODRIVER=\"dummy\", SDL_RENDER_DRIVER=\"software\", SDL_AUDIODRIVER=\"dummy\")\n    70\t    return environment"
Функция run_scene	tools/ui-audit/run_combo.py@9208dcf:73	"    73\tdef run_scene(runtime, combo, scene_id, out_dir):\n    74\t    width, height = split_resolution(combo)\n    75\t    command = [\n    76\t        str(runtime / \"d2tm\"), \"-windowed\", \"-screenWidth\", str(width), \"-screenHeight\", str(height),\n    77\t        \"--ui-audit-scene\", scene_id, \"--ui-audit-out\", str(out_dir),\n    78\t    ]\n    79\t    return subprocess.run(command, cwd=runtime, env=game_environment(), check=False,\n    80\t                          capture_output=True, text=True, timeout=SCENE_TIMEOUT_SECONDS)"
Функция list_scenes	tools/ui-audit/run_combo.py@9208dcf:83	"    83\tdef list_scenes(executable):\n    84\t    result = subprocess.run([str(executable), \"--ui-audit-list\"], env=game_environment(), check=True,\n    85\t                            capture_output=True, text=True, timeout=60)\n    86\t    return json.loads(result.stdout)[\"scenes\"]"
Функция scales_for	tools/ui-audit/run_all.py@9208dcf:19	"    19\tdef scales_for(executable, resolutions):\n    20\t    scales = {}\n    21\t    for resolution in resolutions:\n    22\t        result = subprocess.run([str(executable), \"--ui-audit-scales\", resolution], env=run_combo.game_environment(),\n    23\t                                check=True, capture_output=True, text=True, timeout=60)\n    24\t        _, render, world = combos.parse_scales(result.stdout)\n    25\t        scales[resolution] = {\"render\": [value for value in render if value], \"world\": [value for value in world if value]}\n    26\t    return scales"
Функция run_one	tools/ui-audit/run_all.py@9208dcf:73	"    73\tdef run_one(args, combo, journal):\n    74\t    identifier = combos.combo_id(combo)\n    75\t    free = run_combo.free_gb(args.out)\n    76\t    journal.write(f\"{time.strftime('%F %T')} free {free:.1f} GB before {identifier}\\n\")\n    77\t    journal.flush()\n    78\t    if free < args.min_free_gb:\n    79\t        return identifier, 3\n    80\t    log_path = Path(args.out) / \"run\" / (identifier.replace(\"/\", \"_\") + \".txt\")\n    81\t    log_path.parent.mkdir(parents=True, exist_ok=True)\n    82\t    command = [sys.executable, str(Path(__file__).resolve().parent / \"run_combo.py\"), \"--exe\", args.exe,\n    83\t               \"--resources\", args.resources, \"--out\", args.out, \"--combo\", identifier,\n    84\t               \"--min-free-gb\", str(args.min_free_gb)]\n    85\t    with open(log_path, \"w\", encoding=\"utf-8\") as log:\n    86\t        code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False).returncode\n    87\t    if code == 0:\n    88\t        marker = done_marker(args.out, combo)\n    89\t        marker.parent.mkdir(parents=True, exist_ok=True)\n    90\t        marker.write_text(\"ok\\n\", encoding=\"utf-8\")\n    91\t    return identifier, code"
Функция main	tools/ui-audit/finalize_png.py@9208dcf:27	"    27\tdef main(argv=None):\n    28\t    parser = argparse.ArgumentParser(\n    29\t        description=\"Leave PNG only for the first flag with a given key per resolution; capture the ones still missing.\")\n    30\t    parser.add_argument(\"--exe\", required=True)\n    31\t    parser.add_argument(\"--resources\", required=True)\n    32\t    parser.add_argument(\"--out\", required=True)\n    33\t    parser.add_argument(\"--flags\", required=True, help=\"flags JSON from check_geometry.py\")\n    34\t    parser.add_argument(\"--dry-run\", action=\"store_true\")\n    35\t    args = parser.parse_args(argv)\n    36\t    out = Path(args.out)\n    37\t    order = json.loads((out / \"order.json\").read_text(encoding=\"utf-8\"))\n    38\t    flags = json.loads(Path(args.flags).read_text(encoding=\"utf-8\"))\n    39\t    missing, extra = plan_actions(out, flags, order)\n    40\t    print(f\"extra PNG: {len(extra)}; missing PNG: {len(missing)}\")\n    41\t    if args.dry_run:\n    42\t        return 0\n    43\t    for identifier, scene in extra:\n    44\t        (out / \"png\" / identifier / f\"{scene}.png\").unlink()\n    45\t    by_combo = defaultdict(list)\n    46\t    for identifier, scene in missing:\n    47\t        by_combo[identifier].append(scene)\n    48\t    code = 0\n    49\t    for identifier, scenes in by_combo.items():\n    50\t        command = [sys.executable, str(Path(__file__).resolve().parent / \"run_combo.py\"), \"--exe\", args.exe,\n    51\t                   \"--resources\", args.resources, \"--out\", str(out), \"--combo\", identifier]\n    52\t        for scene in scenes:\n    53\t            command += [\"--scene\", scene]\n    54\t        code = max(code, subprocess.run(command, check=False).returncode)\n    55\t    return code"
Литерал --exe в main	tools/ui-audit/finalize_png.py@9208dcf:30	нет
Литерал --resources в main	tools/ui-audit/finalize_png.py@9208dcf:31	нет
Литерал --out в main	tools/ui-audit/finalize_png.py@9208dcf:32	нет
Литерал --flags в main	tools/ui-audit/finalize_png.py@9208dcf:33	нет
Литерал --dry-run в main	tools/ui-audit/finalize_png.py@9208dcf:34	нет
Литерал --exe в main	tools/ui-audit/finalize_png.py@9208dcf:50	нет
Литерал --resources в main	tools/ui-audit/finalize_png.py@9208dcf:51	нет
Литерал --out в main	tools/ui-audit/finalize_png.py@9208dcf:51	нет
Литерал --combo в main	tools/ui-audit/finalize_png.py@9208dcf:51	нет
Литерал --scene в main	tools/ui-audit/finalize_png.py@9208dcf:53	нет
Литерал --ui-audit-scales в scales_for	tools/ui-audit/run_all.py@9208dcf:22	нет
Литерал --exe в run_one	tools/ui-audit/run_all.py@9208dcf:82	нет
Литерал --resources в run_one	tools/ui-audit/run_all.py@9208dcf:83	нет
Литерал --out в run_one	tools/ui-audit/run_all.py@9208dcf:83	нет
Литерал --combo в run_one	tools/ui-audit/run_all.py@9208dcf:83	нет
Литерал --min-free-gb в run_one	tools/ui-audit/run_all.py@9208dcf:84	нет
Литерал -windowed в run_scene	tools/ui-audit/run_combo.py@9208dcf:76	5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/cHandleArgument.cpp:23:    {"-windowed",               Options::WINDOWED},
Литерал -screenWidth в run_scene	tools/ui-audit/run_combo.py@9208dcf:76	5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/cHandleArgument.cpp:34:    {"-screenWidth",            Options::SCREENX},
Литерал -screenHeight в run_scene	tools/ui-audit/run_combo.py@9208dcf:76	5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/cHandleArgument.cpp:35:    {"-screenHeight",           Options::SCREENY},
Литерал --ui-audit-scene в run_scene	tools/ui-audit/run_combo.py@9208dcf:77	нет
Литерал --ui-audit-out в run_scene	tools/ui-audit/run_combo.py@9208dcf:77	нет
Литерал --ui-audit-list в list_scenes	tools/ui-audit/run_combo.py@9208dcf:84	нет
Ключ настроек ScreenWidth: settings.ini	git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^ScreenWidth='	3:ScreenWidth=1024
Ключ настроек ScreenWidth: строки в src	git grep -n -F '"ScreenWidth"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5	5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:86:    if (section.hasValue("ScreenWidth")) { | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:87:        settings.screenW = section.getInt("ScreenWidth"); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:182:    set(ini, "ScreenWidth", std::to_string(settings.screenW));
Ключ настроек ScreenHeight: settings.ini	git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^ScreenHeight='	4:ScreenHeight=768
Ключ настроек ScreenHeight: строки в src	git grep -n -F '"ScreenHeight"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5	5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:89:    if (section.hasValue("ScreenHeight")) { | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:90:        settings.screenH = section.getInt("ScreenHeight"); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:183:    set(ini, "ScreenHeight", std::to_string(settings.screenH));
Ключ настроек FullScreen: settings.ini	git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^FullScreen='	10:FullScreen=false
Ключ настроек FullScreen: строки в src	git grep -n -F '"FullScreen"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5	5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:98:    if (section.hasValue("FullScreen")) { | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:99:        settings.windowed = !section.getBoolean("FullScreen"); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:186:    set(ini, "FullScreen", toText(!settings.windowed));
Ключ настроек RenderScale: settings.ini	git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^RenderScale='	12:RenderScale=0
Ключ настроек RenderScale: строки в src	git grep -n -F '"RenderScale"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5	5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:104:    if (section.hasValue("RenderScale")) { | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:105:        settings.renderScalePercent = section.getInt("RenderScale"); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:188:    set(ini, "RenderScale", std::to_string(settings.renderScalePercent)); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:223:    set(ini, "RenderScale", std::to_string(renderScalePercent)); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:236:    if (section.hasValue("RenderScale")) {
Ключ настроек WorldScale: settings.ini	git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^WorldScale='	нет
Ключ настроек WorldScale: строки в src	git grep -n -F '"WorldScale"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5	5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:107:    if (section.hasValue("WorldScale")) { | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:108:        settings.worldScalePercent = section.getInt("WorldScale"); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:189:    set(ini, "WorldScale", std::to_string(settings.worldScalePercent)); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:224:    set(ini, "WorldScale", std::to_string(worldScalePercent)); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/Preferences.cpp:239:    if (section.hasValue("WorldScale")) {
Ключ настроек Language: settings.ini	git show 5e9059778bd59e486a58a899c9cf56f6758ed178:resources/bin/settings.ini | grep -n '^Language='	нет
Ключ настроек Language: строки в src	git grep -n -F '"Language"' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src | head -5	нет
Дерево campaign (9208dcf)	git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/campaign resources/campaign	040000 tree 1d78e538bed17d2d408922fb68dce75446db2c64\tresources/bin/campaign
Дерево campaign (5e90597)	git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/campaign resources/campaign	040000 tree a7dd3ac6c95570c5f9b272ca8ab12161c9e39d4c\tresources/bin/campaign
Дерево campaign_en (9208dcf)	git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/campaign_en resources/campaign_en	040000 tree e420c95958690e97845e94ab0036f9cf4c4ced7d\tresources/bin/campaign_en
Дерево campaign_en (5e90597)	git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/campaign_en resources/campaign_en	нет
Дерево data (9208dcf)	git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/data resources/data	040000 tree 6c2458699107335c49177743addff0bacd54d5bf\tresources/bin/data
Дерево data (5e90597)	git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/data resources/data	040000 tree cc6cc1f3161f43e55e96d4878646d578509d57cc\tresources/bin/data
Дерево skirmish (9208dcf)	git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/skirmish resources/skirmish	040000 tree 8b97f75db2e891a72b376256fe4e8810b2236171\tresources/bin/skirmish
Дерево skirmish (5e90597)	git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/skirmish resources/skirmish	040000 tree dca16b79fc302e4d16d2803153aeb8102cef6a57\tresources/bin/skirmish
Дерево skirmish_en (9208dcf)	git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/skirmish_en resources/skirmish_en	040000 tree 526906dc67dd8b566e08ae7db643ed161fb44a5d\tresources/bin/skirmish_en
Дерево skirmish_en (5e90597)	git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/skirmish_en resources/skirmish_en	нет
Дерево game.ini (9208dcf)	git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/game.ini resources/game.ini	100644 blob c45bc861a56cb964ad609877f05dd6eaa79a1efa\tresources/game.ini
Дерево game.ini (5e90597)	git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/game.ini resources/game.ini	100644 blob 7feed737476e58f5645189c100cae77f4a8a0231\tresources/game.ini
Дерево settings.ini (9208dcf)	git ls-tree 9208dcf5a358f40afd95c99480e4e09f781ed566 resources/bin/settings.ini resources/settings.ini	100644 blob 636898ad4ca47088d4374950f6e71ba802d5f431\tresources/bin/settings.ini
Дерево settings.ini (5e90597)	git ls-tree 5e9059778bd59e486a58a899c9cf56f6758ed178 resources/bin/settings.ini resources/settings.ini	100644 blob d3f475fc78e9416d32f6987633f5664c53f8e626\tresources/bin/settings.ini
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:17	    17\t#include "game/Preferences.hpp"
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:19	    19\t#include "utils/cIniFile.h"
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:20	    20\t#include "utils/InitialGameSettings.hpp"
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:25	    25\tconstexpr const char *SECTION = "SETTINGS";
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:36	    36\t    return value ? "true" : "false";
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:48	    48\t        error = "No preferences file found at " + utf8FileName(file);
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:53	    53\t        error = "Preferences file is unusable: " + utf8FileName(file);
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:64	    64\t        error = "Could not create preferences directory: " + filesystemError.message();
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:70	    70\t    tempPath += ".tmp";
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:72	    72\t        error = "Could not write preferences file";
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:77	    77\t        error = "Could not replace preferences file: " + filesystemError.message();
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:86	    86\t    if (section.hasValue("ScreenWidth")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:87	    87\t        settings.screenW = section.getInt("ScreenWidth");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:89	    89\t    if (section.hasValue("ScreenHeight")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:90	    90\t        settings.screenH = section.getInt("ScreenHeight");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:92	    92\t    if (section.hasValue("CameraDragMoveSpeed")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:93	    93\t        settings.cameraDragMoveSpeed = section.getDouble("CameraDragMoveSpeed");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:95	    95\t    if (section.hasValue("CameraBorderOrKeyMoveSpeed")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:96	    96\t        settings.cameraBorderOrKeyMoveSpeed = section.getDouble("CameraBorderOrKeyMoveSpeed");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:98	    98\t    if (section.hasValue("FullScreen")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:99	    99\t        settings.windowed = !section.getBoolean("FullScreen");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:101	   101\t    if (section.hasValue("CameraEdgeMove")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:102	   102\t        settings.cameraEdgeMove = section.getBoolean("CameraEdgeMove");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:104	   104\t    if (section.hasValue("RenderScale")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:105	   105\t        settings.renderScalePercent = section.getInt("RenderScale");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:107	   107\t    if (section.hasValue("WorldScale")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:108	   108\t        settings.worldScalePercent = section.getInt("WorldScale");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:110	   110\t    if (section.hasValue("AllowRepeatingReinforcements")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:111	   111\t        settings.allowRepeatingReinforcements = section.getBoolean("AllowRepeatingReinforcements");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:113	   113\t    if (section.hasValue("AllTurretsDownOnLowPower")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:114	   114\t        settings.turretsDownOnLowPower = section.getBoolean("AllTurretsDownOnLowPower");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:116	   116\t    if (section.hasValue("ShowLowPowerIcon")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:117	   117\t        settings.showLowPowerIcon = section.getBoolean("ShowLowPowerIcon");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:119	   119\t    if (section.hasValue("RocketTurretsDownOnLowPower")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:120	   120\t        settings.rocketTurretsDownOnLowPower = section.getBoolean("RocketTurretsDownOnLowPower");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:122	   122\t    if (section.hasValue("GameRules")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:123	   123\t        settings.gameFilename = section.getStringValue("GameRules");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:125	   125\t    if (section.hasValue("NoAI")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:126	   126\t        settings.disableAI = section.getBoolean("NoAI");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:128	   128\t    if (section.hasValue("Debug")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:129	   129\t        settings.debugMode = section.getBoolean("Debug");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:131	   131\t    if (section.hasValue("playMusic")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:132	   132\t        settings.playMusic = section.getBoolean("playMusic");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:134	   134\t    if (section.hasValue("customMusic")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:135	   135\t        settings.customMusic = section.getBoolean("customMusic");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:137	   137\t    if (section.hasValue("playSound")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:138	   138\t        settings.playSound = section.getBoolean("playSound");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:140	   140\t    if (section.hasValue("playCreditsSound")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:141	   141\t        settings.playCreditsSound = section.getBoolean("playCreditsSound");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:143	   143\t    if (section.hasValue("drawUnitDebug")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:144	   144\t        settings.drawUnitDebug = section.getBoolean("drawUnitDebug");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:146	   146\t    if (section.hasValue("oneAi")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:147	   147\t        settings.oneAi = section.getBoolean("oneAi");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:149	   149\t    if (section.hasValue("disableWormAi")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:150	   150\t        settings.disableWormAi = section.getBoolean("disableWormAi");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:152	   152\t    if (section.hasValue("disableReinforcements")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:153	   153\t        settings.disableReinforcements = section.getBoolean("disableReinforcements");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:155	   155\t    if (section.hasValue("noAiRest")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:156	   156\t        settings.noAiRest = section.getBoolean("noAiRest");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:158	   158\t    if (section.hasValue("drawUsages")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:159	   159\t        settings.drawUsages = section.getBoolean("drawUsages");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:161	   161\t    if (section.hasValue("pauseWhenLosingFocus")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:162	   162\t        settings.pauseWhenLosingFocus = section.getBoolean("pauseWhenLosingFocus");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:164	   164\t    if (section.hasValue("fogOfWarEnabled")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:165	   165\t        settings.fogOfWarEnabled = section.getBoolean("fogOfWarEnabled");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:182	   182\t    set(ini, "ScreenWidth", std::to_string(settings.screenW));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:183	   183\t    set(ini, "ScreenHeight", std::to_string(settings.screenH));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:184	   184\t    set(ini, "CameraDragMoveSpeed", std::to_string(settings.cameraDragMoveSpeed));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:185	   185\t    set(ini, "CameraBorderOrKeyMoveSpeed", std::to_string(settings.cameraBorderOrKeyMoveSpeed));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:186	   186\t    set(ini, "FullScreen", toText(!settings.windowed));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:187	   187\t    set(ini, "CameraEdgeMove", toText(settings.cameraEdgeMove));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:188	   188\t    set(ini, "RenderScale", std::to_string(settings.renderScalePercent));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:189	   189\t    set(ini, "WorldScale", std::to_string(settings.worldScalePercent));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:190	   190\t    set(ini, "AllowRepeatingReinforcements", toText(settings.allowRepeatingReinforcements));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:191	   191\t    set(ini, "AllTurretsDownOnLowPower", toText(settings.turretsDownOnLowPower));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:192	   192\t    set(ini, "RocketTurretsDownOnLowPower", toText(settings.rocketTurretsDownOnLowPower));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:193	   193\t    set(ini, "ShowLowPowerIcon", toText(settings.showLowPowerIcon));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:194	   194\t    set(ini, "GameRules", settings.gameFilename);
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:195	   195\t    set(ini, "NoAI", toText(settings.disableAI));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:196	   196\t    set(ini, "Debug", toText(settings.debugMode));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:197	   197\t    set(ini, "playMusic", toText(settings.playMusic));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:198	   198\t    set(ini, "customMusic", toText(settings.customMusic));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:199	   199\t    set(ini, "playSound", toText(settings.playSound));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:200	   200\t    set(ini, "playCreditsSound", toText(settings.playCreditsSound));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:201	   201\t    set(ini, "drawUnitDebug", toText(settings.drawUnitDebug));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:202	   202\t    set(ini, "oneAi", toText(settings.oneAi));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:203	   203\t    set(ini, "disableWormAi", toText(settings.disableWormAi));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:204	   204\t    set(ini, "disableReinforcements", toText(settings.disableReinforcements));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:205	   205\t    set(ini, "noAiRest", toText(settings.noAiRest));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:206	   206\t    set(ini, "drawUsages", toText(settings.drawUsages));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:207	   207\t    set(ini, "pauseWhenLosingFocus", toText(settings.pauseWhenLosingFocus));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:208	   208\t    set(ini, "fogOfWarEnabled", toText(settings.fogOfWarEnabled));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:223	   223\t    set(ini, "RenderScale", std::to_string(renderScalePercent));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:224	   224\t    set(ini, "WorldScale", std::to_string(worldScalePercent));
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:236	   236\t    if (section.hasValue("RenderScale")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:237	   237\t        settings.renderScalePercent = section.getInt("RenderScale");
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:239	   239\t    if (section.hasValue("WorldScale")) {
Preferences.cpp: строка с кавычкой	src/game/Preferences.cpp@5e90597:240	   240\t        settings.worldScalePercent = section.getInt("WorldScale");
Поиск loadSettingsFromIni	git grep -n -w 'loadSettingsFromIni' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- src	5e9059778bd59e486a58a899c9cf56f6758ed178:src/main.cpp:72:    std::unique_ptr<InitialGameSettings> settings = loadSettingsFromIni("settings.ini"); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/common.cpp:44:std::unique_ptr<InitialGameSettings> loadSettingsFromIni(const std::string& filename) | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/common.cpp:50:        Logger::error(COMP_GAMERULES, "loadSettingsFromIni", "Expected to find [SETTINGS] in {}", filename); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/utils/common.h:62:std::unique_ptr<InitialGameSettings> loadSettingsFromIni(const std::string& filename);
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:44	    44\tstd::unique_ptr<InitialGameSettings> loadSettingsFromIni(const std::string& filename)
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:45	    45\t{
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:46	    46\t    std::shared_ptr<cIniFile> file = std::make_shared<cIniFile>(filename);
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:47	    47\t    std::unique_ptr<InitialGameSettings> gameSettings = std::make_unique<InitialGameSettings>();
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:48	    48\t
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:49	    49\t    if (!file->hasSection("SETTINGS")) {
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:50	    50\t        Logger::error(COMP_GAMERULES, "loadSettingsFromIni", "Expected to find [SETTINGS] in {}", filename);
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:51	    51\t        return gameSettings;
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:52	    52\t    }
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:53	    53\t
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:54	    54\t    const cSection &section = file->getSection("SETTINGS");
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:55	    55\t    Preferences::readSettings(section, *gameSettings);
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:56	    56\t
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:57	    57\t    if (!section.hasValue("CameraEdgeMove")) {
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:58	    58\t        // no explicit setting: default off when windowed (edge-scrolling fights
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:59	    59\t        // with normal window interactions), on when fullscreen
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:60	    60\t        gameSettings->cameraEdgeMove = !gameSettings->windowed;
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:61	    61\t    }
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:62	    62\t
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:63	    63\t    return gameSettings;
Определение loadSettingsFromIni	src/utils/common.cpp@5e90597:64	    64\t}
Окружение тестов и сборки	git grep -n -E 'XDG|environ|LD_LIBRARY_PATH|SDL_' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- tests/ui_audit tools/upstream/build_upstream_linux.sh	5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:24:        environment = dict(os.environ) | 5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:25:        environment.update( | 5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:26:            SDL_VIDEODRIVER="dummy", | 5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:27:            SDL_RENDER_DRIVER="software", | 5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:28:            SDL_AUDIODRIVER="dummy", | 5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:29:            XDG_DATA_HOME=str(self.xdg), | 5e9059778bd59e486a58a899c9cf56f6758ed178:tests/ui_audit/ui_audit_runtime_support.py:34:            env=environment, | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:51:                -DSDL_INSTALL=ON -DSDL_SHARED=ON -DSDL_STATIC=OFF | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:52:                -DSDL_TEST_LIBRARY=OFF -DSDL_TESTS=OFF -DSDL_EXAMPLES=OFF | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:53:                -DSDL_AUDIO=ON -DSDL_VIDEO=ON -DSDL_RENDER=ON | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:54:                -DSDL_DUMMYAUDIO=ON -DSDL_DUMMYVIDEO=ON -DSDL_OFFSCREEN=ON | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:55:                -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF -DSDL_JACK=OFF | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:56:                -DSDL_PIPEWIRE=OFF -DSDL_SNDIO=OFF -DSDL_X11=OFF | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:57:                -DSDL_WAYLAND=OFF -DSDL_KMSDRM=OFF -DSDL_OPENGL=OFF | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:58:                -DSDL_OPENGLES=OFF -DSDL_VULKAN=OFF -DSDL_UNIX_CONSOLE_BUILD=ON | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:61:        SDL_image) | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:73:        SDL_ttf) | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:82:        SDL_mixer) | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:127:    if [[ "$name" == SDL_ttf ]]; then | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:140:        SDL_image|SDL_ttf|SDL_mixer) | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:160:    printf 'Команда: SDL_VIDEODRIVER=%s SDL_AUDIODRIVER=dummy XDG_DATA_HOME=%q timeout 20 ./d2tm\n' \ | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:163:        SDL_VIDEODRIVER="$driver" SDL_AUDIODRIVER=dummy \ | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:164:        XDG_DATA_HOME="$DUNE_OUT_DIR/xdg" timeout 20 ./d2tm) \ | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:197:    printf '%s\0' SDL_image SDL_ttf SDL_mixer | | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:208:    export LD_LIBRARY_PATH="$library_dir" | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:210:    printf 'CPATH=%s\nLIBRARY_PATH=%s\nLD_LIBRARY_PATH=%s\n' "$CPATH" "$LIBRARY_PATH" "$LD_LIBRARY_PATH" | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:255:    for name in SDL SDL_image SDL_ttf SDL_mixer Catch2; do | 5e9059778bd59e486a58a899c9cf56f6758ed178:tools/upstream/build_upstream_linux.sh:260:    printf 'Запуск: SDL_VIDEODRIVER=%s; код timeout=%s\n' "$selected_driver" "$game_status"
Python в CI и CTest	git grep -n -E 'python|unittest|pytest' 5e9059778bd59e486a58a899c9cf56f6758ed178 -- .github CMakeLists.txt tests/CMakeLists.txt tools/upstream/build_upstream_linux.sh | head -40	5e9059778bd59e486a58a899c9cf56f6758ed178:.github/workflows/build_manual.yml:100:        uses: actions/setup-python@v3 | 5e9059778bd59e486a58a899c9cf56f6758ed178:.github/workflows/build_manual.yml:102:          python-version: "3.14"
~~~~

## 5. Исходники, данные и прогоны без игры

Таблица `sources.tsv` содержит 43 строки данных: литералы путей `src/`, уникальные файлы из `keys.tsv` с количеством строк и имена из `exclusions.tsv` с результатами поиска в PORT.

#### sources.tsv

~~~~text
что	путь@9208dcf:строка или значение	FORK1	PORT
src/gamestates	tools/ui-audit/check_screens.py@9208dcf:9	tree	tree
src/mentat	tools/ui-audit/check_screens.py@9208dcf:9	tree	нет
src/save/SaveSlotsDialog.hpp	tools/ui-audit/check_screens.py@9208dcf:10	blob	нет
src/include/definitions.h	tools/ui-audit/check_screens.py@9208dcf:59	blob	blob
src/gui	tools/ui-audit/find_hit_tests.py@9208dcf:8	tree	tree
src/drawers	tools/ui-audit/find_hit_tests.py@9208dcf:8	tree	tree
src/gamestates	tools/ui-audit/find_hit_tests.py@9208dcf:8	tree	tree
src/managers	tools/ui-audit/find_hit_tests.py@9208dcf:8	tree	tree
src/save	tools/ui-audit/find_hit_tests.py@9208dcf:8	tree	нет
src/sidebar	tools/ui-audit/find_hit_tests.py@9208dcf:8	tree	tree
src/mentat	tools/ui-audit/find_hit_tests.py@9208dcf:8	tree	нет
src/controls	tools/ui-audit/find_hit_tests.py@9208dcf:9	tree	tree
src/debug	tools/ui-audit/find_hit_tests.py@9208dcf:9	tree	нет
keys.tsv:file	src/building/cItemBuilder.cpp	4	blob
keys.tsv:file	src/cGame_logic.cpp	47	нет
keys.tsv:file	src/controls/CommandBindings.hpp	19	нет
keys.tsv:file	src/controls/cKeyboardEvent.cpp	5	blob
keys.tsv:file	src/controls/cKeyboardEvent.h	13	blob
keys.tsv:file	src/controls/mousestates/cMouseNormalState.cpp	5	blob
keys.tsv:file	src/controls/mousestates/cMouseRepairState.cpp	1	blob
keys.tsv:file	src/controls/mousestates/cMouseUnitsSelectedState.cpp	10	blob
keys.tsv:file	src/drawers/cBuildingListDrawer.cpp	4	blob
keys.tsv:file	src/drawers/cCommandBarDrawer.cpp	6	нет
keys.tsv:file	src/gamestates/cChooseHouseState.cpp	1	blob
keys.tsv:file	src/gamestates/cCreditsState.cpp	1	blob
keys.tsv:file	src/gamestates/cMainMenuState.cpp	3	blob
keys.tsv:file	src/gamestates/cOptionsState.cpp	6	blob
keys.tsv:file	src/gamestates/cSelectYourNextConquestState.cpp	1	blob
keys.tsv:file	src/gamestates/cSetupSkirmishState.cpp	3	blob
keys.tsv:file	src/managers/cDrawManager.cpp	6	blob
keys.tsv:file	src/map/cMapCamera.cpp	8	нет
keys.tsv:file	src/save/SaveSlotsDialog.cpp	6	нет
keys.tsv:file	src/utils/GameSettings.hpp	1	нет
keys.tsv:file	src/utils/common.cpp	18	blob
exclusions.tsv:name	GAME_EDITING	—	нет
exclusions.tsv:name	GAME_INTRO	—	"5e9059778bd59e486a58a899c9cf56f6758ed178:src/gamestates/cGameState.h:55:// #define GAME_INTRO	     9 | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/include/eGameState.h:56:inline constexpr int GAME_INTRO = 9;"
exclusions.tsv:name	GAME_OVER	—	"5e9059778bd59e486a58a899c9cf56f6758ed178:src/gamestates/cGameState.h:51:// #define GAME_OVER         0      // game over | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/include/eGameState.cpp:26:        case GAME_OVER: | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/include/eGameState.cpp:27:            return ""GAME_OVER"";"
exclusions.tsv:name	GAME_INITIALIZE	—	5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/cGame_logic.cpp:392:    setState(GAME_INITIALIZE); | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/cGame_logic.cpp:840:    m_state = GAME_INITIALIZE; | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/cGame_logic.cpp:950:            case GAME_INITIALIZE: mapped = eGameState::INITIALIZE; return true;
exclusions.tsv:name	GAME_MAX_STATES	—	5e9059778bd59e486a58a899c9cf56f6758ed178:src/include/eGameState.h:69:inline constexpr int GAME_MAX_STATES = 22;
exclusions.tsv:name	cGameState	—	5e9059778bd59e486a58a899c9cf56f6758ed178:src/CMakeLists.txt:120:    gamestates/cGameState.cpp | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/cGame.h:32:class cGameState; | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/game/cGame.h:228:    cGameState *m_currentState;
exclusions.tsv:name	AbstractMentat	—	"5e9059778bd59e486a58a899c9cf56f6758ed178:src/CMakeLists.txt:61:    gameobjects/mentat/AbstractMentat.cpp | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/gameobjects/mentat/AbstractMentat.cpp:2: * @file AbstractMentat.cpp | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/gameobjects/mentat/AbstractMentat.cpp:16:#include ""AbstractMentat.h"""
exclusions.tsv:name	GAME_SKIRMISH	—	5e9059778bd59e486a58a899c9cf56f6758ed178:src/gamestates/cGameState.h:57:// #define GAME_SKIRMISH    15      // playing a skirmish mission! | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/include/eGameState.h:62:inline constexpr int GAME_SKIRMISH = 15;      // playing a skirmish mission!
exclusions.tsv:name	cRegion	—	5e9059778bd59e486a58a899c9cf56f6758ed178:src/gamestates/cSelectYourNextConquestState.cpp:251:            cRegion &regionPiece = world[i]; | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/gamestates/cSelectYourNextConquestState.cpp:274:            cRegion &region = world[iRegNr]; | 5e9059778bd59e486a58a899c9cf56f6758ed178:src/gamestates/cSelectYourNextConquestState.cpp:331:            cRegion &regionPiece = world[i];
~~~~

Таблицы прогонов: `runs.tsv` — 7 строк данных; `unittest-fork.tsv` — 15 строк данных.

#### runs.tsv

~~~~text
прогон	команда	exit	число строк лога	число строк файла --out	первые 20 строк лога через |
unittest-fork	cd .tmp/p5tr/fork/tools/ui-audit && TMPDIR=/srv/dune/worktrees/u13g/.tmp/p5tr/tmp /usr/bin/python3 -B -m unittest discover -s tests -v	0	224	—	"test_caption_names_screen_state_house_resolution_language_graphics_and_scales (test_build_sheets.HelpersTest.test_caption_names_screen_state_house_resolution_language_graphics_and_scales) ... ok | test_chunks_of_six (test_build_sheets.HelpersTest.test_chunks_of_six) ... ok | test_duplicate_flags_collapse (test_build_sheets.HelpersTest.test_duplicate_flags_collapse) ... ok | test_flag_rects_scale_by_factor_and_use_two_colors (test_build_sheets.HelpersTest.test_flag_rects_scale_by_factor_and_use_two_colors) ... ok | test_zero_scale_is_called_auto (test_build_sheets.HelpersTest.test_zero_scale_is_called_auto) ... ok | test_index_counts_flags_per_frame (test_build_sheets.IndexTest.test_index_counts_flags_per_frame) ... ok | test_index_links_every_png_and_has_filters (test_build_sheets.IndexTest.test_index_links_every_png_and_has_filters) ... ok | test_catalog_sheets_hold_six_frames_in_three_by_two_grid (test_build_sheets.SheetsTest.test_catalog_sheets_hold_six_frames_in_three_by_two_grid) ... /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_build_sheets.py:62: ResourceWarning: unclosed file <_io.BufferedReader name='/srv/dune/worktrees/u13g/.tmp/p5tr/tmp/tmpmkm9opci/out/1024x768_ru_hd/001.jpg'> |   width, height = Image.open(written[0]).size | ResourceWarning: Enable tracemalloc to get the object allocation traceback | ok | test_flag_sheet_draws_rectangles_over_the_frame (test_build_sheets.SheetsTest.test_flag_sheet_draws_rectangles_over_the_frame) ... /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/build_sheets.py:113: ResourceWarning: unclosed file <_io.BufferedReader name='/srv/dune/worktrees/u13g/.tmp/p5tr/tmp/tmp7l52qjn9/png/1024x768/ru/hd/s1.png'> |   return Image.open(png_path).width / header[""canvas""][""w""] | ResourceWarning: Enable tracemalloc to get the object allocation traceback | /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_build_sheets.py:82: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead. |   reddish = any(r > 180 and g < 80 and b < 80 for r, g, b in Image.open(written[0]).getdata()) | ok | test_flag_without_png_is_reported_missing (test_build_sheets.SheetsTest.test_flag_without_png_is_reported_missing) ... ok | test_frames_missing_from_png_folder_are_skipped (test_build_sheets.SheetsTest.test_frames_missing_from_png_folder_are_skipped) ... ok | test_empty_root_reports_every_expected_file (test_check_completeness.Completeness.test_empty_root_reports_every_expected_file) ... ok"
extract-fork	TMPDIR=/srv/dune/worktrees/u13g/.tmp/p5tr/tmp /usr/bin/python3 -B .tmp/p5tr/fork/tools/ui-audit/extract_keys.py --root .tmp/p5tr/fork --out .tmp/p5tr/keys-raw-fork.tsv	0	2	176	keys-raw rows: 175 | exit=0
check-keys-fork	TMPDIR=/srv/dune/worktrees/u13g/.tmp/p5tr/tmp /usr/bin/python3 -B .tmp/p5tr/fork/tools/ui-audit/check_keys.py --keys .tmp/p5tr/fork/tools/ui-audit/keys.tsv --raw .tmp/p5tr/keys-raw-fork.tsv --out .tmp/p5tr/check-keys-fork.txt	1	31	20	no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_LALT (x2) | no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_LSHIFT (x2) | no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_RALT (x2) | no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_RSHIFT (x2) | no annotation in keys.tsv: src/controls/CommandBindings.hpp trySetCommandBinding commandBinding (x1) | no annotation in keys.tsv: src/gamestates/cOptionsState.cpp bindingKeyName SDL_SCANCODE_LCTRL (x1) | no annotation in keys.tsv: src/gamestates/cOptionsState.cpp bindingKeyName SDL_SCANCODE_RCTRL (x1) | no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_LCTRL (x2) | no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_RCTRL (x2) | rule 10: state=game: debug mode; key=1; actions: debug-control-player-1 / select-group; places: src/cGame_logic.cpp:2417, src/controls/cKeyboardEvent.cpp:12 | rule 10: state=game: debug mode; key=2; actions: debug-control-player-2 / select-group; places: src/cGame_logic.cpp:2421, src/controls/cKeyboardEvent.cpp:15 | rule 10: state=game: debug mode; key=3; actions: debug-control-player-3 / select-group; places: src/cGame_logic.cpp:2425, src/controls/cKeyboardEvent.cpp:18 | rule 10: state=game: debug mode; key=D+TAB; actions: draw-without-shroud / show-list-ids; places: src/drawers/cBuildingListDrawer.cpp:1040, src/drawers/cBuildingListDrawer.cpp:1047, src/managers/cDrawManager.cpp:519, src/managers/cDrawManager.cpp:533 | rule 10: state=game: debug mode; key=F4; actions: debug-clear-shroud / debug-give-credits; places: src/cGame_logic.cpp:2066, src/cGame_logic.cpp:2441 | rule 10: state=game: debug mode; key=TAB+D; actions: draw-without-shroud / show-list-ids; places: src/drawers/cBuildingListDrawer.cpp:1040, src/drawers/cBuildingListDrawer.cpp:1047, src/managers/cDrawManager.cpp:519, src/managers/cDrawManager.cpp:533 | rule 10: state=game: structure selected; key=LCTRL; actions: create-group / rally; places: src/cGame_logic.cpp:2052, src/controls/CommandBindings.hpp:23 | rule 10: state=game: units selected; key=D; actions: deploy / unload; places: src/controls/CommandBindings.hpp:21, src/controls/CommandBindings.hpp:22 | rule 10: state=game: units selected; key=LCTRL; actions: attack / create-group; places: src/cGame_logic.cpp:2052, src/controls/CommandBindings.hpp:19, src/controls/mousestates/cMouseUnitsSelectedState.cpp:452 | rule 10: state=game: units selected; key=LSHIFT; actions: add-to-selection / build-multiplier; places: src/building/cItemBuilder.cpp:826, src/building/cItemBuilder.cpp:833, src/controls/mousestates/cMouseUnitsSelectedState.cpp:427, src/controls/mousestates/cMouseUnitsSelectedState.cpp:483 | rule 10: state=game: units selected; key=RSHIFT; actions: add-to-selection / build-multiplier; places: src/building/cItemBuilder.cpp:826, src/building/cItemBuilder.cpp:833, src/controls/mousestates/cMouseUnitsSelectedState.cpp:427, src/controls/mousestates/cMouseUnitsSelectedState.cpp:483
extract-port	TMPDIR=/srv/dune/worktrees/u13g/.tmp/p5tr/tmp /usr/bin/python3 -B .tmp/p5tr/fork/tools/ui-audit/extract_keys.py --root .tmp/p5tr/port --out .tmp/p5tr/keys-raw-port.tsv	0	2	161	keys-raw rows: 160 | exit=0
check-keys-port	TMPDIR=/srv/dune/worktrees/u13g/.tmp/p5tr/tmp /usr/bin/python3 -B .tmp/p5tr/fork/tools/ui-audit/check_keys.py --keys .tmp/p5tr/fork/tools/ui-audit/keys.tsv --raw .tmp/p5tr/keys-raw-port.tsv --out .tmp/p5tr/check-keys-port.txt	1	245	20	no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::containsActionKey SDL_SCANCODE_COUNT (x2) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_0 (x1) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_1 (x4) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_2 (x4) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_3 (x4) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_4 (x3) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_5 (x3) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_6 (x3) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_A (x2) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_BACKSLASH (x1) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_BACKSPACE (x1) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_C (x3) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_D (x2) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_DOWN (x1) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_ESCAPE (x2) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F (x2) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F1 (x2) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F10 (x1) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F11 (x1) | no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F12 (x1)
hit-tests-fork	TMPDIR=/srv/dune/worktrees/u13g/.tmp/p5tr/tmp /usr/bin/python3 -B .tmp/p5tr/fork/tools/ui-audit/find_hit_tests.py --root .tmp/p5tr/fork	0	87	—	file line function recorded_in_function records_in_file code | src/gui/GuiButton.cpp 244 GuiButton::onMouseMovedTo no 0 m_focus = m_rect.isPointWithin(event.coords); | src/gui/GuiCheckBox.cpp 138 GuiCheckBox::onMouseMovedTo no 0 m_focus = m_rect.isPointWithin(event.coords); | src/gui/GuiLabel.cpp 130 GuiLabel::onMouseMovedTo no 0 m_focus = m_rect.isPointWithin(event.coords); | src/gui/GuiSlider.cpp 65 GuiSlider::onNotifyMouseEvent no 0 if (m_rect.isPointWithin(event.coords)) { | src/drawers/cBuildingListDrawer.cpp 453 cBuildingListDrawer::drawList no 0 if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) { | src/drawers/cBuildingListDrawer.cpp 504 cBuildingListDrawer::isOverItemCoordinates_Boolean no 0 bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY) | src/drawers/cBuildingListDrawer.cpp 515 cBuildingListDrawer::isOverItemCoordinates no 0 cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y) | src/drawers/cBuildingListDrawer.cpp 520 cBuildingListDrawer::isOverItemCoordinates no 0 if (!layout.cards.isPointWithin(x, y)) { | src/drawers/cBuildingListDrawer.cpp 534 cBuildingListDrawer::isOverItemCoordinates no 0 if (card.isPointWithin(x, y)) { | src/drawers/cBuildingListDrawer.cpp 837 cBuildingListDrawer::onNotifyMouseEvent no 0 if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) { | src/drawers/cBuildingListDrawer.cpp 850 cBuildingListDrawer::onNotifyMouseEvent no 0 !layout.scrollbar.isPointWithin(event.coords.x, event.coords.y)) { | src/drawers/cCommandBarDrawer.cpp 69 cCommandBarDrawer::isMouseOver no 0 bool cCommandBarDrawer::isMouseOver(const cPoint &point) const | src/drawers/cCommandBarDrawer.cpp 71 cCommandBarDrawer::isMouseOver no 0 return m_panelRect.isPointWithin(point.x, point.y); | src/drawers/cCommandBarDrawer.cpp 259 cCommandBarDrawer::onNotifyMouseEvent no 0 if (m_buttons[i].rect.isPointWithin(event.coords.x, event.coords.y)) { | src/drawers/cCommandBarDrawer.cpp 267 cCommandBarDrawer::onNotifyMouseEvent no 0 if (button.enabled && button.rect.isPointWithin(event.coords.x, event.coords.y)) { | src/drawers/cMapDrawer.cpp 119 cMapDrawer::drawTerrain no 0 if (!m_map->isWithinBoundaries(iCell)) { | src/drawers/cMiniMapDrawer.cpp 167 cMiniMapDrawer::isMouseOver no 1 bool cMiniMapDrawer::isMouseOver() | src/drawers/cMiniMapDrawer.cpp 213 cMiniMapDrawer::drawTerrain no 1 if (!m_map->isWithinBoundaries(x, y)) { | src/drawers/cMiniMapDrawer.cpp 268 cMiniMapDrawer::drawUnitsAndStructures no 1 if (!m_map->isWithinBoundaries(x, y)) continue;
hit-tests-port	TMPDIR=/srv/dune/worktrees/u13g/.tmp/p5tr/tmp /usr/bin/python3 -B .tmp/p5tr/fork/tools/ui-audit/find_hit_tests.py --root .tmp/p5tr/port	0	90	—	file line function recorded_in_function records_in_file code | src/gui/GuiBar.cpp 75 GuiBar::onNotifyMouseEvent no 0 if (!event.coords.isWithinRectangle(&m_rect)) | src/gui/GuiButton.cpp 277 GuiButton::onMouseMovedTo no 0 m_focus = m_rect.isPointWithin(event.coords); | src/gui/GuiButton.cpp 315 GuiButton::onMouseLeftButtonClicked no 0 if (!m_rect.isPointWithin(event.coords) || !m_enabled) { | src/gui/GuiCheckBox.cpp 157 GuiCheckBox::onMouseMovedTo no 0 m_focus = m_rect.isPointWithin(event.coords); | src/gui/GuiCycleButton.cpp 48 GuiCycleButton::onNotifyMouseEvent no 0 if (!m_enabled || !m_rect.isPointWithin(event.coords.x, event.coords.y)) { | src/gui/GuiLabel.cpp 146 GuiLabel::onMouseMovedTo no 0 m_focus = m_rect.isPointWithin(event.coords); | src/gui/GuiSlider.cpp 125 GuiSlider::onNotifyMouseEvent no 0 if (m_rect.isPointWithin(event.coords)) { | src/gui/GuiSlider.cpp 132 GuiSlider::onNotifyMouseEvent no 0 if (m_rect.isPointWithin(event.coords) && m_onLeftMouseButtonClickedAction) { | src/gui/GuiSlider.cpp 146 GuiSlider::onNotifyMouseEvent no 0 if (m_rect.isPointWithin(event.coords) && m_onRightMouseButtonClickedAction) { | src/gui/GuiStateButton.cpp 73 GuiStateButton::onNotifyMouseEvent no 0 if (!event.coords.isWithinRectangle(&m_rect)) | src/gui/GuiTextInput.cpp 138 GuiTextInput::onNotifyMouseEvent no 0 m_focused = m_rect.isPointWithin(event.coords); | src/gui/GuiValueButton.cpp 43 GuiValueButton::onNotifyMouseEvent no 0 m_focus = m_rect.isPointWithin(event.coords); | src/gui/GuiValueButton.cpp 59 GuiValueButton::onNotifyMouseEvent no 0 m_pressed = m_rect.isPointWithin(event.coords); | src/gui/GuiValueButton.cpp 65 GuiValueButton::onNotifyMouseEvent no 0 if (m_rect.isPointWithin(event.coords)) { | src/gui/GuiValueButton.cpp 75 GuiValueButton::onNotifyMouseEvent no 0 if (m_rect.isPointWithin(event.coords)) { | src/drawers/cBuildingListDrawer.cpp 553 cBuildingListDrawer::drawList no 0 if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) { | src/drawers/cBuildingListDrawer.cpp 642 cBuildingListDrawer::isOverItemCoordinates_Boolean no 0 bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY) | src/drawers/cBuildingListDrawer.cpp 653 cBuildingListDrawer::isOverItemCoordinates no 0 cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y) | src/drawers/cBuildingListDrawer.cpp 657 cBuildingListDrawer::isOverItemCoordinates no 0 if (!layout.cards.isPointWithin(x, y)) {
~~~~

#### unittest-fork.tsv

~~~~text
файл тестов	ok	FAIL	ERROR	skipped
tests/test_build_sheets.py	9	0	0	0
tests/test_check_completeness.py	11	0	0	0
tests/test_check_credits.py	4	0	0	0
tests/test_check_geometry.py	44	0	0	0
tests/test_check_keys.py	23	0	0	0
tests/test_check_options_geometry.py	10	0	0	0
tests/test_check_scenes.py	22	0	0	0
tests/test_check_screens.py	9	0	0	0
tests/test_combos.py	18	0	0	0
tests/test_extra_rules.py	21	0	0	0
tests/test_extract_keys.py	8	0	0	0
tests/test_find_hit_tests.py	5	0	0	0
tests/test_png_policy.py	6	0	0	0
tests/test_png_policy_outputs.py	5	0	0	0
tests/test_run_all.py	9	0	0	0
~~~~

Журналы содержат команду, stdout/stderr и строку `exit=...` для каждого запрошенного прогона:

#### run-unittest-fork.log

~~~~text
test_caption_names_screen_state_house_resolution_language_graphics_and_scales (test_build_sheets.HelpersTest.test_caption_names_screen_state_house_resolution_language_graphics_and_scales) ... ok
test_chunks_of_six (test_build_sheets.HelpersTest.test_chunks_of_six) ... ok
test_duplicate_flags_collapse (test_build_sheets.HelpersTest.test_duplicate_flags_collapse) ... ok
test_flag_rects_scale_by_factor_and_use_two_colors (test_build_sheets.HelpersTest.test_flag_rects_scale_by_factor_and_use_two_colors) ... ok
test_zero_scale_is_called_auto (test_build_sheets.HelpersTest.test_zero_scale_is_called_auto) ... ok
test_index_counts_flags_per_frame (test_build_sheets.IndexTest.test_index_counts_flags_per_frame) ... ok
test_index_links_every_png_and_has_filters (test_build_sheets.IndexTest.test_index_links_every_png_and_has_filters) ... ok
test_catalog_sheets_hold_six_frames_in_three_by_two_grid (test_build_sheets.SheetsTest.test_catalog_sheets_hold_six_frames_in_three_by_two_grid) ... /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_build_sheets.py:62: ResourceWarning: unclosed file <_io.BufferedReader name='/srv/dune/worktrees/u13g/.tmp/p5tr/tmp/tmpmkm9opci/out/1024x768_ru_hd/001.jpg'>
  width, height = Image.open(written[0]).size
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_flag_sheet_draws_rectangles_over_the_frame (test_build_sheets.SheetsTest.test_flag_sheet_draws_rectangles_over_the_frame) ... /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/build_sheets.py:113: ResourceWarning: unclosed file <_io.BufferedReader name='/srv/dune/worktrees/u13g/.tmp/p5tr/tmp/tmp7l52qjn9/png/1024x768/ru/hd/s1.png'>
  return Image.open(png_path).width / header["canvas"]["w"]
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/tests/test_build_sheets.py:82: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead.
  reddish = any(r > 180 and g < 80 and b < 80 for r, g, b in Image.open(written[0]).getdata())
ok
test_flag_without_png_is_reported_missing (test_build_sheets.SheetsTest.test_flag_without_png_is_reported_missing) ... ok
test_frames_missing_from_png_folder_are_skipped (test_build_sheets.SheetsTest.test_frames_missing_from_png_folder_are_skipped) ... ok
test_empty_root_reports_every_expected_file (test_check_completeness.Completeness.test_empty_root_reports_every_expected_file) ... ok
test_every_problem_is_reported (test_check_completeness.Completeness.test_every_problem_is_reported) ... ok
test_extra_png_in_reduced_combo_is_refused (test_check_completeness.Completeness.test_extra_png_in_reduced_combo_is_refused) ... ok
test_flagged_scene_png_is_not_extra_in_its_combo_only (test_check_completeness.Completeness.test_flagged_scene_png_is_not_extra_in_its_combo_only) ... ok
test_full_set_succeeds (test_check_completeness.Completeness.test_full_set_succeeds) ... ok
test_missing_hud_png_in_reduced_combo_is_refused (test_check_completeness.Completeness.test_missing_hud_png_in_reduced_combo_is_refused) ... ok
test_missing_log_in_full_combo_is_refused (test_check_completeness.Completeness.test_missing_log_in_full_combo_is_refused) ... ok
test_missing_log_in_reduced_combo_is_refused (test_check_completeness.Completeness.test_missing_log_in_reduced_combo_is_refused) ... ok
test_missing_png_in_full_combo_is_refused (test_check_completeness.Completeness.test_missing_png_in_full_combo_is_refused) ... ok
test_missing_png_of_flagged_scene_is_refused (test_check_completeness.Completeness.test_missing_png_of_flagged_scene_is_refused) ... ok
test_png_of_unknown_scene_in_full_combo_is_refused (test_check_completeness.Completeness.test_png_of_unknown_scene_in_full_combo_is_refused) ... ok
test_all_lines_covered_across_scenes (test_check_credits.CheckCreditsTests.test_all_lines_covered_across_scenes) ... ok
test_log_without_notes_is_a_problem (test_check_credits.CheckCreditsTests.test_log_without_notes_is_a_problem) ... ok
test_missing_line_is_reported (test_check_credits.CheckCreditsTests.test_missing_line_is_reported) ... ok
test_name_and_text_must_share_a_row (test_check_credits.CheckCreditsTests.test_name_and_text_must_share_a_row) ... ok
test_button_inside_window_is_honest (test_check_geometry.ElementsOverlapRule.test_button_inside_window_is_honest) ... ok
test_buttons_touching_by_edges_are_honest (test_check_geometry.ElementsOverlapRule.test_buttons_touching_by_edges_are_honest) ... ok
test_gui_partially_overlapping_an_area_is_flagged (test_check_geometry.ElementsOverlapRule.test_gui_partially_overlapping_an_area_is_flagged) ... ok
test_identical_rectangles_are_honest (test_check_geometry.ElementsOverlapRule.test_identical_rectangles_are_honest) ... ok
test_partially_overlapping_buttons_are_flagged (test_check_geometry.ElementsOverlapRule.test_partially_overlapping_buttons_are_flagged) ... ok
test_clean_file_has_no_flags (test_check_geometry.LogFile.test_clean_file_has_no_flags) ... ok
test_file_with_overlapping_elements_is_flagged (test_check_geometry.LogFile.test_file_with_overlapping_elements_is_flagged) ... ok
test_file_without_header_is_rejected (test_check_geometry.LogFile.test_file_without_header_is_rejected) ... ok
test_area_below_canvas_is_flagged (test_check_geometry.OffCanvasRule.test_area_below_canvas_is_flagged) ... ok
test_gui_with_negative_origin_is_flagged (test_check_geometry.OffCanvasRule.test_gui_with_negative_origin_is_flagged) ... ok
test_rectangles_ending_exactly_on_the_edge_are_honest (test_check_geometry.OffCanvasRule.test_rectangles_ending_exactly_on_the_edge_are_honest) ... ok
test_text_beyond_right_edge_is_flagged (test_check_geometry.OffCanvasRule.test_text_beyond_right_edge_is_flagged) ... ok
test_wide_canvas_is_taken_from_the_header (test_check_geometry.OffCanvasRule.test_wide_canvas_is_taken_from_the_header) ... ok
test_different_canvas_is_not_compared (test_check_geometry.ResolutionDifferenceRule.test_different_canvas_is_not_compared) ... ok
test_different_graphics_is_not_compared (test_check_geometry.ResolutionDifferenceRule.test_different_graphics_is_not_compared) ... ok
test_different_language_is_not_compared (test_check_geometry.ResolutionDifferenceRule.test_different_language_is_not_compared) ... ok
test_different_scene_is_not_compared (test_check_geometry.ResolutionDifferenceRule.test_different_scene_is_not_compared) ... ok
test_extra_record_between_resolutions_is_flagged (test_check_geometry.ResolutionDifferenceRule.test_extra_record_between_resolutions_is_flagged) ... ok
test_game_screen_compares_gui (test_check_geometry.ResolutionDifferenceRule.test_game_screen_compares_gui) ... ok
test_game_screen_compares_texts (test_check_geometry.ResolutionDifferenceRule.test_game_screen_compares_texts) ... ok
test_game_screen_ignores_a_different_area (test_check_geometry.ResolutionDifferenceRule.test_game_screen_ignores_a_different_area) ... ok
test_identical_logs_are_honest (test_check_geometry.ResolutionDifferenceRule.test_identical_logs_are_honest) ... ok
test_menu_screen_compares_areas (test_check_geometry.ResolutionDifferenceRule.test_menu_screen_compares_areas) ... ok
test_moved_text_between_resolutions_is_flagged (test_check_geometry.ResolutionDifferenceRule.test_moved_text_between_resolutions_is_flagged) ... ok
test_record_order_does_not_matter (test_check_geometry.ResolutionDifferenceRule.test_record_order_does_not_matter) ... ok
test_text_covering_a_whole_button_is_flagged (test_check_geometry.TextAcrossElementRule.test_text_covering_a_whole_button_is_flagged) ... ok
test_text_crossing_a_button_edge_is_flagged (test_check_geometry.TextAcrossElementRule.test_text_crossing_a_button_edge_is_flagged) ... ok
test_text_crossing_an_area_is_flagged (test_check_geometry.TextAcrossElementRule.test_text_crossing_an_area_is_flagged) ... ok
test_text_inside_a_button_is_honest (test_check_geometry.TextAcrossElementRule.test_text_inside_a_button_is_honest) ... ok
test_text_inside_window_and_button_is_honest (test_check_geometry.TextAcrossElementRule.test_text_inside_window_and_button_is_honest) ... ok
test_text_inside_window_crossing_a_button_is_flagged (test_check_geometry.TextAcrossElementRule.test_text_inside_window_crossing_a_button_is_flagged) ... ok
test_text_outside_every_element_is_honest (test_check_geometry.TextAcrossElementRule.test_text_outside_every_element_is_honest) ... ok
test_text_touching_a_button_edge_is_honest (test_check_geometry.TextAcrossElementRule.test_text_touching_a_button_edge_is_honest) ... ok
test_overlapping_texts_are_flagged (test_check_geometry.TextOnTextRule.test_overlapping_texts_are_flagged) ... ok
test_separated_texts_are_honest (test_check_geometry.TextOnTextRule.test_separated_texts_are_honest) ... ok
test_texts_touching_by_edges_are_honest (test_check_geometry.TextOnTextRule.test_texts_touching_by_edges_are_honest) ... ok
test_text_of_exactly_the_box_size_is_honest (test_check_geometry.TextWiderThanBoxRule.test_text_of_exactly_the_box_size_is_honest) ... ok
test_text_smaller_than_its_box_is_honest (test_check_geometry.TextWiderThanBoxRule.test_text_smaller_than_its_box_is_honest) ... ok
test_text_taller_than_its_box_is_flagged (test_check_geometry.TextWiderThanBoxRule.test_text_taller_than_its_box_is_flagged) ... ok
test_text_wider_than_its_box_is_flagged (test_check_geometry.TextWiderThanBoxRule.test_text_wider_than_its_box_is_flagged) ... ok
test_text_without_a_box_is_not_compared_with_one (test_check_geometry.TextWiderThanBoxRule.test_text_without_a_box_is_not_compared_with_one) ... ok
test_flag_carries_scene_combo_rectangles_and_texts (test_check_geometry.WholeScene.test_flag_carries_scene_combo_rectangles_and_texts) ... ok
test_format_flag_is_one_line_with_every_part (test_check_geometry.WholeScene.test_format_flag_is_one_line_with_every_part) ... ok
test_window_with_buttons_labels_and_texts_is_honest (test_check_geometry.WholeScene.test_window_with_buttons_labels_and_texts_is_honest) ... ok
test_deploy_and_unload_selected_apart_is_honest (test_check_keys.KeyConflicts.test_deploy_and_unload_selected_apart_is_honest) ... ok
test_deploy_and_unload_selected_together_on_one_key_is_flagged (test_check_keys.KeyConflicts.test_deploy_and_unload_selected_together_on_one_key_is_flagged) ... ok
test_different_modifiers_are_different_keys (test_check_keys.KeyConflicts.test_different_modifiers_are_different_keys) ... ok
test_flag_line_names_state_key_and_actions (test_check_keys.KeyConflicts.test_flag_line_names_state_key_and_actions) ... ok
test_one_key_two_actions_in_one_state_is_flagged (test_check_keys.KeyConflicts.test_one_key_two_actions_in_one_state_is_flagged) ... ok
test_row_without_key_handling_is_not_a_conflict (test_check_keys.KeyConflicts.test_row_without_key_handling_is_not_a_conflict) ... ok
test_same_action_twice_is_honest (test_check_keys.KeyConflicts.test_same_action_twice_is_honest) ... ok
test_same_key_in_different_states_is_honest (test_check_keys.KeyConflicts.test_same_key_in_different_states_is_honest) ... ok
test_three_actions_on_one_key_are_one_flag (test_check_keys.KeyConflicts.test_three_actions_on_one_key_are_one_flag) ... ok
test_existing_check_removes_the_flags (test_check_keys.KeyRebinding.test_existing_check_removes_the_flags) ... ok
test_flag_line_has_state_command_words_and_keys (test_check_keys.KeyRebinding.test_flag_line_has_state_command_words_and_keys) ... ok
test_flag_lists_occupied_keys_of_the_state_once (test_check_keys.KeyRebinding.test_flag_lists_occupied_keys_of_the_state_once) ... ok
test_one_flag_per_command_and_state_pair (test_check_keys.KeyRebinding.test_one_flag_per_command_and_state_pair) ... ok
test_own_key_is_not_listed_as_occupied (test_check_keys.KeyRebinding.test_own_key_is_not_listed_as_occupied) ... ok
test_row_without_key_handling_is_not_listed_as_occupied (test_check_keys.KeyRebinding.test_row_without_key_handling_is_not_listed_as_occupied) ... ok
test_state_without_other_keys_still_gives_a_flag (test_check_keys.KeyRebinding.test_state_without_other_keys_still_gives_a_flag) ... ok
test_equal_tables_are_fresh (test_check_keys.KeyTableFreshness.test_equal_tables_are_fresh) ... ok
test_extra_row_in_the_table_is_a_problem (test_check_keys.KeyTableFreshness.test_extra_row_in_the_table_is_a_problem) ... ok
test_line_number_is_not_compared (test_check_keys.KeyTableFreshness.test_line_number_is_not_compared) ... ok
test_missing_row_in_the_table_is_a_problem (test_check_keys.KeyTableFreshness.test_missing_row_in_the_table_is_a_problem) ... ok
test_same_key_in_another_function_is_a_different_row (test_check_keys.KeyTableFreshness.test_same_key_in_another_function_is_a_different_row) ... ok
test_two_checks_of_one_key_in_one_function_are_two_rows (test_check_keys.KeyTableFreshness.test_two_checks_of_one_key_in_one_function_are_two_rows) ... ok
test_rows_are_read_by_the_header (test_check_keys.TsvLoading.test_rows_are_read_by_the_header) ... ok
test_button_contained_by_a_nonclickable_row_is_flagged (test_check_options_geometry.Rule3.test_button_contained_by_a_nonclickable_row_is_flagged) ... ok
test_button_covering_a_nonclickable_row_is_flagged (test_check_options_geometry.Rule3.test_button_covering_a_nonclickable_row_is_flagged) ... ok
test_button_covering_a_slider_is_flagged (test_check_options_geometry.Rule3.test_button_covering_a_slider_is_flagged) ... ok
test_button_inside_parent_window_is_not_flagged (test_check_options_geometry.Rule3.test_button_inside_parent_window_is_not_flagged) ... ok
test_nonbutton_nested_pair_keeps_the_general_rule (test_check_options_geometry.Rule3.test_nonbutton_nested_pair_keeps_the_general_rule) ... ok
test_checker_fails_on_flags_when_the_plan_matches (test_check_options_geometry.Rule9AndPlan.test_checker_fails_on_flags_when_the_plan_matches) ... ok
test_nonoptions_logs_are_outside_the_scoped_count (test_check_options_geometry.Rule9AndPlan.test_nonoptions_logs_are_outside_the_scoped_count) ... ok
test_plan_entries_are_filtered_to_the_three_options_scenes (test_check_options_geometry.Rule9AndPlan.test_plan_entries_are_filtered_to_the_three_options_scenes) ... ok
test_rule9_is_checked_independently_of_rule3 (test_check_options_geometry.Rule9AndPlan.test_rule9_is_checked_independently_of_rule3) ... ok
test_scoped_check_fails_for_missing_and_extra_planned_pairs (test_check_options_geometry.Rule9AndPlan.test_scoped_check_fails_for_missing_and_extra_planned_pairs) ... ok
test_line_has_scene_combination_and_result (test_check_scenes.OutputLines.test_line_has_scene_combination_and_result) ... ok
test_log_file_is_checked_and_formatted (test_check_scenes.OutputLines.test_log_file_is_checked_and_formatted) ... ok
test_log_file_of_an_unchecked_scene_gives_no_line (test_check_scenes.OutputLines.test_log_file_of_an_unchecked_scene_gives_no_line) ... ok
test_building_at_the_right_is_ok (test_check_scenes.StructureLabelScene.test_building_at_the_right_is_ok) ... ok
test_building_at_the_top_is_ok (test_check_scenes.StructureLabelScene.test_building_at_the_top_is_ok) ... ok
test_building_at_the_wrong_edge_fails (test_check_scenes.StructureLabelScene.test_building_at_the_wrong_edge_fails) ... ok
test_building_in_the_middle_fails (test_check_scenes.StructureLabelScene.test_building_in_the_middle_fails) ... ok
test_missing_health_record_fails (test_check_scenes.StructureLabelScene.test_missing_health_record_fails) ... ok
test_two_buildings_fail (test_check_scenes.StructureLabelScene.test_two_buildings_fail) ... ok
test_all_copies_at_the_top_fail (test_check_scenes.UnitLabelScenes.test_all_copies_at_the_top_fail) ... ok
test_copy_beyond_the_edge_is_allowed (test_check_scenes.UnitLabelScenes.test_copy_beyond_the_edge_is_allowed) ... ok
test_copy_not_at_an_edge_fails (test_check_scenes.UnitLabelScenes.test_copy_not_at_an_edge_fails) ... ok
test_correct_scene_is_ok (test_check_scenes.UnitLabelScenes.test_correct_scene_is_ok) ... ok
test_four_objects_fail (test_check_scenes.UnitLabelScenes.test_four_objects_fail) ... ok
test_harvester_needs_a_spice_label (test_check_scenes.UnitLabelScenes.test_harvester_needs_a_spice_label) ... ok
test_missing_group_label_fails (test_check_scenes.UnitLabelScenes.test_missing_group_label_fails) ... ok
test_other_types_do_not_need_spice (test_check_scenes.UnitLabelScenes.test_other_types_do_not_need_spice) ... ok
test_scene_name_with_underscore_type_is_ok (test_check_scenes.UnitLabelScenes.test_scene_name_with_underscore_type_is_ok) ... ok
test_scene_that_is_not_checked_gives_none (test_check_scenes.UnitLabelScenes.test_scene_that_is_not_checked_gives_none) ... ok
test_text_record_elsewhere_is_ok (test_check_scenes.UnitLabelScenes.test_text_record_elsewhere_is_ok) ... ok
test_text_record_inside_the_group_label_fails (test_check_scenes.UnitLabelScenes.test_text_record_inside_the_group_label_fails) ... ok
test_two_objects_fail (test_check_scenes.UnitLabelScenes.test_two_objects_fail) ... ok
test_classes_are_read_without_forward_declarations_and_enums (test_check_screens.CodeNames.test_classes_are_read_without_forward_declarations_and_enums) ... ok
test_game_state_constants_are_read_from_defines (test_check_screens.CodeNames.test_game_state_constants_are_read_from_defines) ... ok
test_code_name_without_a_scene_is_a_problem (test_check_screens.Coverage.test_code_name_without_a_scene_is_a_problem) ... ok
test_every_name_covered_by_a_scene_or_an_exclusion_is_complete (test_check_screens.Coverage.test_every_name_covered_by_a_scene_or_an_exclusion_is_complete) ... ok
test_exclusion_of_a_name_the_code_does_not_have_is_a_problem (test_check_screens.Coverage.test_exclusion_of_a_name_the_code_does_not_have_is_a_problem) ... ok
test_exclusion_with_an_empty_reason_is_a_problem (test_check_screens.Coverage.test_exclusion_with_an_empty_reason_is_a_problem) ... ok
test_scene_naming_an_unknown_state_is_not_a_problem (test_check_screens.Coverage.test_scene_naming_an_unknown_state_is_not_a_problem) ... ok
test_exclusion_without_a_reason_is_a_problem (test_check_screens.Exclusions.test_exclusion_without_a_reason_is_a_problem) ... ok
test_exclusions_are_read_with_reasons (test_check_screens.Exclusions.test_exclusions_are_read_with_reasons) ... ok
test_every_combination_is_unique (test_combos.CombinationCounts.test_every_combination_is_unique) ... ok
test_full_scope_hd_combinations_have_automatic_object_size (test_combos.CombinationCounts.test_full_scope_hd_combinations_have_automatic_object_size) ... ok
test_game_scale_variants_per_resolution_are_automatic_plus_manual (test_combos.CombinationCounts.test_game_scale_variants_per_resolution_are_automatic_plus_manual) ... ok
test_hd_has_46_full_and_184_game_only_combinations (test_combos.CombinationCounts.test_hd_has_46_full_and_184_game_only_combinations) ... ok
test_manual_object_sizes_cover_every_game_scale_variant (test_combos.CombinationCounts.test_manual_object_sizes_cover_every_game_scale_variant) ... ok
test_old_combinations_are_the_automatic_scales_of_hd (test_combos.CombinationCounts.test_old_combinations_are_the_automatic_scales_of_hd) ... ok
test_total_is_230_with_12_old_and_218_new (test_combos.CombinationCounts.test_total_is_230_with_12_old_and_218_new) ... ok
test_automatic_object_size_with_manual_game_scale (test_combos.CombinationNames.test_automatic_object_size_with_manual_game_scale) ... ok
test_new_combination_name_ends_with_the_scales (test_combos.CombinationNames.test_new_combination_name_ends_with_the_scales) ... ok
test_old_combination_keeps_the_old_name (test_combos.CombinationNames.test_old_combination_keeps_the_old_name) ... ok
test_logs_of_all_scenes_and_png_of_flagged_scenes_are_complete (test_combos.NewCombinationCompleteness.test_logs_of_all_scenes_and_png_of_flagged_scenes_are_complete) ... ok
test_missing_log_and_missing_flagged_png_are_reported (test_combos.NewCombinationCompleteness.test_missing_log_and_missing_flagged_png_are_reported) ... ok
test_png_of_an_unflagged_scene_is_extra (test_combos.NewCombinationCompleteness.test_png_of_an_unflagged_scene_is_extra) ... ok
test_game_output_is_parsed (test_combos.ScaleListParsing.test_game_output_is_parsed) ... ok
test_full_scope_hd_keeps_all_scenes (test_combos.ScenesAndPng.test_full_scope_hd_keeps_all_scenes) ... ok
test_game_scope_keeps_only_game_screen_scenes (test_combos.ScenesAndPng.test_game_scope_keeps_only_game_screen_scenes) ... ok
test_new_combination_keeps_png_only_of_flagged_scenes (test_combos.ScenesAndPng.test_new_combination_keeps_png_only_of_flagged_scenes) ... ok
test_old_combination_keeps_png_of_full_resolution_hud_and_flagged_scenes (test_combos.ScenesAndPng.test_old_combination_keeps_png_of_full_resolution_hud_and_flagged_scenes) ... ok
test_adjacent_zones_are_honest (test_extra_rules.ClickZonesRule.test_adjacent_zones_are_honest) ... ok
test_overlapping_zones_are_flagged (test_extra_rules.ClickZonesRule.test_overlapping_zones_are_flagged) ... ok
test_zone_inside_another_zone_is_flagged (test_extra_rules.ClickZonesRule.test_zone_inside_another_zone_is_flagged) ... ok
test_zone_of_the_whole_canvas_overlaps_every_other_zone (test_extra_rules.ClickZonesRule.test_zone_of_the_whole_canvas_overlaps_every_other_zone) ... ok
test_combination_without_scales_keeps_the_old_name (test_extra_rules.CombinationNameAndOutput.test_combination_without_scales_keeps_the_old_name) ... ok
test_manual_scales_are_part_of_the_name (test_extra_rules.CombinationNameAndOutput.test_manual_scales_are_part_of_the_name) ... ok
test_new_rules_have_names_and_one_line_format (test_extra_rules.CombinationNameAndOutput.test_new_rules_have_names_and_one_line_format) ... ok
test_tree_check_reports_extra_rules_and_counts_scale_combinations_apart (test_extra_rules.CombinationNameAndOutput.test_tree_check_reports_extra_rules_and_counts_scale_combinations_apart) ... ok
test_empty_clipped_label_is_not_flagged (test_extra_rules.LabelOverPanelRule.test_empty_clipped_label_is_not_flagged) ... ok
test_label_drawn_over_an_earlier_panel_is_flagged (test_extra_rules.LabelOverPanelRule.test_label_drawn_over_an_earlier_panel_is_flagged) ... ok
test_label_far_from_the_panel_is_honest (test_extra_rules.LabelOverPanelRule.test_label_far_from_the_panel_is_honest) ... ok
test_label_recorded_before_the_panel_is_not_flagged (test_extra_rules.LabelOverPanelRule.test_label_recorded_before_the_panel_is_not_flagged) ... ok
test_label_touching_the_panel_edge_is_honest (test_extra_rules.LabelOverPanelRule.test_label_touching_the_panel_edge_is_honest) ... ok
test_every_intersecting_pair_gives_its_own_flag (test_extra_rules.LabelsOfOneObjectRule.test_every_intersecting_pair_gives_its_own_flag) ... ok
test_intersecting_labels_of_one_object_are_flagged (test_extra_rules.LabelsOfOneObjectRule.test_intersecting_labels_of_one_object_are_flagged) ... ok
test_same_rectangles_of_different_objects_are_honest (test_extra_rules.LabelsOfOneObjectRule.test_same_rectangles_of_different_objects_are_honest) ... ok
test_separate_labels_of_one_object_are_honest (test_extra_rules.LabelsOfOneObjectRule.test_separate_labels_of_one_object_are_honest) ... ok
test_summary_counts_objects_with_a_crossing_pair_and_all_objects_of_the_type (test_extra_rules.LabelsOfOneObjectRule.test_summary_counts_objects_with_a_crossing_pair_and_all_objects_of_the_type) ... ok
test_extra_rules_ignore_the_old_record_kinds (test_extra_rules.NewRecordsStayOutsideRulesOneToSix.test_extra_rules_ignore_the_old_record_kinds) ... ok
test_label_and_click_records_do_not_change_the_flags_of_rules_one_to_six (test_extra_rules.NewRecordsStayOutsideRulesOneToSix.test_label_and_click_records_do_not_change_the_flags_of_rules_one_to_six) ... ok
test_resolution_comparison_ignores_label_and_click_records (test_extra_rules.NewRecordsStayOutsideRulesOneToSix.test_resolution_comparison_ignores_label_and_click_records) ... ok
test_comments_are_ignored (test_extract_keys.ExtractKeys.test_comments_are_ignored) ... ok
test_function_is_the_last_column_zero_definition_above (test_extract_keys.ExtractKeys.test_function_is_the_last_column_zero_definition_above) ... ok
test_one_row_per_key_token_in_order (test_extract_keys.ExtractKeys.test_one_row_per_key_token_in_order) ... ok
test_row_has_file_function_key_and_line (test_extract_keys.ExtractKeys.test_row_has_file_function_key_and_line) ... ok
test_text_without_keys_gives_no_rows (test_extract_keys.ExtractKeys.test_text_without_keys_gives_no_rows) ... ok
test_tsv_has_a_header_and_tab_separated_rows (test_extract_keys.ExtractKeys.test_tsv_has_a_header_and_tab_separated_rows) ... ok
test_two_uses_of_one_key_in_one_function_are_two_rows (test_extract_keys.ExtractKeys.test_two_uses_of_one_key_in_one_function_are_two_rows) ... ok
test_use_outside_any_function_has_a_dash (test_extract_keys.ExtractKeys.test_use_outside_any_function_has_a_dash) ... ok
test_comment_lines_are_ignored (test_find_hit_tests.ScanTextTest.test_comment_lines_are_ignored) ... ok
test_hit_test_in_function_with_record_is_marked_yes (test_find_hit_tests.ScanTextTest.test_hit_test_in_function_with_record_is_marked_yes) ... ok
test_hit_test_in_function_without_record_is_marked_no (test_find_hit_tests.ScanTextTest.test_hit_test_in_function_without_record_is_marked_no) ... ok
test_record_count_counts_both_kinds (test_find_hit_tests.ScanTextTest.test_record_count_counts_both_kinds) ... ok
test_only_listed_directories_are_scanned (test_find_hit_tests.ScanTreeTest.test_only_listed_directories_are_scanned) ... ok
test_other_resolution_does_not_count_as_earlier (test_png_policy.CaptureDecisionTest.test_other_resolution_does_not_count_as_earlier) ... ok
test_same_key_with_other_coordinates_gives_no_png_and_a_new_key_does (test_png_policy.CaptureDecisionTest.test_same_key_with_other_coordinates_gives_no_png_and_a_new_key_does) ... ok
test_scene_without_flags_gets_no_png (test_png_policy.CaptureDecisionTest.test_scene_without_flags_gets_no_png) ... ok
test_finalize_lists_extra_and_missing_png (test_png_policy.FinalSelectionTest.test_finalize_lists_extra_and_missing_png) ... ok
test_legacy_combination_always_keeps_flagged_scene (test_png_policy.FinalSelectionTest.test_legacy_combination_always_keeps_flagged_scene) ... ok
test_png_goes_to_the_first_combination_with_the_key (test_png_policy.FinalSelectionTest.test_png_goes_to_the_first_combination_with_the_key) ... ok
test_new_combination_with_repeated_key_needs_no_png (test_png_policy_outputs.CompletenessOrderTest.test_new_combination_with_repeated_key_needs_no_png) ... ok
test_new_key_without_png_is_reported_as_missing (test_png_policy_outputs.CompletenessOrderTest.test_new_key_without_png_is_reported_as_missing) ... ok
test_png_of_repeated_key_is_reported_as_extra (test_png_policy_outputs.CompletenessOrderTest.test_png_of_repeated_key_is_reported_as_extra) ... ok
test_flag_sheet_caption_names_the_source_combination (test_png_policy_outputs.DisplayFlagsTest.test_flag_sheet_caption_names_the_source_combination) ... /srv/dune/worktrees/u13g/.tmp/p5tr/fork/tools/ui-audit/build_sheets.py:113: ResourceWarning: unclosed file <_io.BufferedReader name='/srv/dune/worktrees/u13g/.tmp/p5tr/tmp/tmp5cs8f014/png/1280x720/ru/hd/s.png'>
  return Image.open(png_path).width / header["canvas"]["w"]
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_flag_with_own_png_keeps_its_own_combination (test_png_policy_outputs.DisplayFlagsTest.test_flag_with_own_png_keeps_its_own_combination) ... ok
test_flag_without_own_png_shows_the_first_combination_with_the_same_key (test_png_policy_outputs.DisplayFlagsTest.test_flag_without_own_png_shows_the_first_combination_with_the_same_key) ... ok
test_audit_log_plan_uses_scene_scope_from_the_plan (test_run_all.PlanTest.test_audit_log_plan_uses_scene_scope_from_the_plan) ... ok
test_interleave_takes_one_item_from_each_chain_in_turn (test_run_all.PlanTest.test_interleave_takes_one_item_from_each_chain_in_turn) ... ok
test_legacy_combinations_come_first (test_run_all.PlanTest.test_legacy_combinations_come_first) ... ok
test_new_combinations_alternate_between_resolutions (test_run_all.PlanTest.test_new_combinations_alternate_between_resolutions) ... ok
test_plan_keeps_every_combination_once (test_run_all.PlanTest.test_plan_keeps_every_combination_once) ... ok
test_combo_bytes_counts_logs_and_png (test_run_all.SizeTest.test_combo_bytes_counts_logs_and_png) ... ok
test_done_marker_path_has_no_slashes_in_name (test_run_all.SizeTest.test_done_marker_path_has_no_slashes_in_name) ... ok
test_forecast_scales_bytes_per_scene (test_run_all.SizeTest.test_forecast_scales_bytes_per_scene) ... ok
test_forecast_without_finished_scenes_is_zero (test_run_all.SizeTest.test_forecast_without_finished_scenes_is_zero) ... ok

----------------------------------------------------------------------
Ran 207 tests in 0.333s

OK
exit=0
~~~~

#### run-extract-fork.log

~~~~text
keys-raw rows: 175
exit=0
~~~~

#### run-check-keys-fork.log

~~~~text
no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_LALT (x2)
no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_LSHIFT (x2)
no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_RALT (x2)
no annotation in keys.tsv: src/controls/CommandBindings.hpp commandBindingKeysMatch SDL_SCANCODE_RSHIFT (x2)
no annotation in keys.tsv: src/controls/CommandBindings.hpp trySetCommandBinding commandBinding (x1)
no annotation in keys.tsv: src/gamestates/cOptionsState.cpp bindingKeyName SDL_SCANCODE_LCTRL (x1)
no annotation in keys.tsv: src/gamestates/cOptionsState.cpp bindingKeyName SDL_SCANCODE_RCTRL (x1)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_LCTRL (x2)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_RCTRL (x2)
rule 10: state=game: debug mode; key=1; actions: debug-control-player-1 / select-group; places: src/cGame_logic.cpp:2417, src/controls/cKeyboardEvent.cpp:12
rule 10: state=game: debug mode; key=2; actions: debug-control-player-2 / select-group; places: src/cGame_logic.cpp:2421, src/controls/cKeyboardEvent.cpp:15
rule 10: state=game: debug mode; key=3; actions: debug-control-player-3 / select-group; places: src/cGame_logic.cpp:2425, src/controls/cKeyboardEvent.cpp:18
rule 10: state=game: debug mode; key=D+TAB; actions: draw-without-shroud / show-list-ids; places: src/drawers/cBuildingListDrawer.cpp:1040, src/drawers/cBuildingListDrawer.cpp:1047, src/managers/cDrawManager.cpp:519, src/managers/cDrawManager.cpp:533
rule 10: state=game: debug mode; key=F4; actions: debug-clear-shroud / debug-give-credits; places: src/cGame_logic.cpp:2066, src/cGame_logic.cpp:2441
rule 10: state=game: debug mode; key=TAB+D; actions: draw-without-shroud / show-list-ids; places: src/drawers/cBuildingListDrawer.cpp:1040, src/drawers/cBuildingListDrawer.cpp:1047, src/managers/cDrawManager.cpp:519, src/managers/cDrawManager.cpp:533
rule 10: state=game: structure selected; key=LCTRL; actions: create-group / rally; places: src/cGame_logic.cpp:2052, src/controls/CommandBindings.hpp:23
rule 10: state=game: units selected; key=D; actions: deploy / unload; places: src/controls/CommandBindings.hpp:21, src/controls/CommandBindings.hpp:22
rule 10: state=game: units selected; key=LCTRL; actions: attack / create-group; places: src/cGame_logic.cpp:2052, src/controls/CommandBindings.hpp:19, src/controls/mousestates/cMouseUnitsSelectedState.cpp:452
rule 10: state=game: units selected; key=LSHIFT; actions: add-to-selection / build-multiplier; places: src/building/cItemBuilder.cpp:826, src/building/cItemBuilder.cpp:833, src/controls/mousestates/cMouseUnitsSelectedState.cpp:427, src/controls/mousestates/cMouseUnitsSelectedState.cpp:483
rule 10: state=game: units selected; key=RSHIFT; actions: add-to-selection / build-multiplier; places: src/building/cItemBuilder.cpp:826, src/building/cItemBuilder.cpp:833, src/controls/mousestates/cMouseUnitsSelectedState.cpp:427, src/controls/mousestates/cMouseUnitsSelectedState.cpp:483
rule 10: state=game: units selected; command=attack; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: units selected; command=deploy; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: structure selected; command=rally; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: structure selected; command=release; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: nothing selected; command=repair; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: structure selected; command=repair; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: repair mode; command=repair; переназначение без проверки занятости; keys already used in this state: BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: units selected; command=repair; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: units selected; command=unload; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
keys: freshness FAIL; rule 10 flags: 20
exit=1
~~~~

#### run-extract-port.log

~~~~text
keys-raw rows: 160
exit=0
~~~~

#### run-check-keys-port.log

~~~~text
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::containsActionKey SDL_SCANCODE_COUNT (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_0 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_1 (x4)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_2 (x4)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_3 (x4)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_4 (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_5 (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_6 (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_A (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_BACKSLASH (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_BACKSPACE (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_C (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_D (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_DOWN (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_ESCAPE (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F1 (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F10 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F11 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F12 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F2 (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F3 (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F4 (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F5 (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F6 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F7 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F8 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_F9 (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_G (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_H (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_I (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_KP_MINUS (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_KP_PLUS (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_L (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_LCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_LEFT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_LSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_M (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_MUTE (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_O (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_P (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_PAGEDOWN (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_PAGEUP (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_R (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_RCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_RETURN (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_RIGHT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_RSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_S (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_T (x3)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_UP (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_V (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_VOLUMEDOWN (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_VOLUMEUP (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_W (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_X (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_Y (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::loadDefaults SDL_SCANCODE_Z (x4)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_COUNT (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_LALT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_LCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_LSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_RALT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_RCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_RSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::matches SDL_SCANCODE_TAB (x2)
no annotation in keys.tsv: src/controls/cKeyBindings.cpp cKeyBindings::parseBinding SDL_SCANCODE_UNKNOWN (x1)
no annotation in keys.tsv: src/controls/cKeyBindings.h - SDL_SCANCODE_COUNT (x2)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::handleEvent SDL_SCANCODE_LALT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::handleEvent SDL_SCANCODE_LCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::handleEvent SDL_SCANCODE_LSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::handleEvent SDL_SCANCODE_RALT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::handleEvent SDL_SCANCODE_RCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::handleEvent SDL_SCANCODE_RSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::handleEvent SDL_SCANCODE_TAB (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp cKeyboard::updateState SDL_SCANCODE_COUNT (x3)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isModifierKey SDL_SCANCODE_LALT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isModifierKey SDL_SCANCODE_LCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isModifierKey SDL_SCANCODE_LSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isModifierKey SDL_SCANCODE_RALT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isModifierKey SDL_SCANCODE_RCTRL (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isModifierKey SDL_SCANCODE_RSHIFT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isPressed SDL_SCANCODE_COUNT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.cpp isValidScancode SDL_SCANCODE_COUNT (x1)
no annotation in keys.tsv: src/controls/cKeyboard.h - SDL_SCANCODE_COUNT (x3)
no annotation in keys.tsv: src/controls/cKeyboardEvent.cpp cKeyboardEvent::cKeyboardEvent SDL_SCANCODE_COUNT (x1)
no annotation in keys.tsv: src/controls/cKeyboardEvent.cpp cKeyboardEvent::hasKey SDL_SCANCODE_COUNT (x1)
no annotation in keys.tsv: src/controls/cKeyboardEvent.cpp cKeyboardEvent::isBackspace SDL_SCANCODE_BACKSPACE (x1)
no annotation in keys.tsv: src/controls/cKeyboardEvent.cpp cKeyboardEvent::isEnter SDL_SCANCODE_KP_ENTER (x1)
no annotation in keys.tsv: src/controls/cKeyboardEvent.cpp cKeyboardEvent::isEnter SDL_SCANCODE_RETURN (x1)
no annotation in keys.tsv: src/controls/cKeyboardEvent.cpp cKeyboardEvent::toString SDL_SCANCODE_COUNT (x1)
no annotation in keys.tsv: src/controls/cKeyboardEvent.h - SDL_SCANCODE_COUNT (x2)
no annotation in keys.tsv: src/game/cGame_logic.cpp isConsoleToggleKey SDL_SCANCODE_GRAVE (x1)
no annotation in keys.tsv: src/gamestates/cGamePlaying.cpp cGamePlaying::onKeyDownGamePlaying SDL_SCANCODE_TAB (x1)
no annotation in keys.tsv: src/managers/cDrawManager.cpp cDrawManager::onKeyDown SDL_SCANCODE_T (x1)
no annotation in keys.tsv: src/managers/cDrawManager.cpp cDrawManager::onKeyPressed SDL_SCANCODE_T (x1)
no such key use in the code: src/building/cItemBuilder.cpp cItemBuilder::onKeyHold SDL_SCANCODE_LSHIFT (x1)
no such key use in the code: src/building/cItemBuilder.cpp cItemBuilder::onKeyHold SDL_SCANCODE_RSHIFT (x1)
no such key use in the code: src/cGame_logic.cpp cGame::applySettings commandBindings (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_0 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_1 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_2 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_3 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_F2 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_F3 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_F4 (x2)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_F5 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_F6 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_F7 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_F8 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownDebugMode SDL_SCANCODE_LSHIFT (x2)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_C (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_F (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_F4 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_H (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_LCTRL (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_RCTRL (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_TAB (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyDownGamePlaying SDL_SCANCODE_Z (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_BACKSLASH (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_C (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_F (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_F5 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_F9 (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_H (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_KP_MINUS (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_KP_PLUS (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_LALT (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_LEFTBRACKET (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_LSHIFT (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_M (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_MUTE (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_O (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_P (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_RETURN (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_RIGHTBRACKET (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_RSHIFT (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_VOLUMEDOWN (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying SDL_SCANCODE_VOLUMEUP (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying m_commandBindings.deploy (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onKeyPressedGamePlaying m_commandBindings.release (x1)
no such key use in the code: src/cGame_logic.cpp cGame::onNotifyKeyboardEvent SDL_SCANCODE_F11 (x1)
no such key use in the code: src/controls/CommandBindings.hpp - SDL_SCANCODE_D (x3)
no such key use in the code: src/controls/CommandBindings.hpp - SDL_SCANCODE_LCTRL (x2)
no such key use in the code: src/controls/CommandBindings.hpp - SDL_SCANCODE_R (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBinding SDL_SCANCODE_UNKNOWN (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBinding commandBinding (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_KP_ENTER (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_LALT (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_LCTRL (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_LSHIFT (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_RALT (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_RCTRL (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_RETURN (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_RSHIFT (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingDisplayName SDL_SCANCODE_SPACE (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingFromIni SDL_SCANCODE_UNKNOWN (x1)
no such key use in the code: src/controls/CommandBindings.hpp commandBindingToIni SDL_SCANCODE_UNKNOWN (x1)
no such key use in the code: src/controls/cKeyboardEvent.cpp cKeyboardEvent::getGroupNumber SDL_SCANCODE_1 (x1)
no such key use in the code: src/controls/cKeyboardEvent.cpp cKeyboardEvent::getGroupNumber SDL_SCANCODE_2 (x1)
no such key use in the code: src/controls/cKeyboardEvent.cpp cKeyboardEvent::getGroupNumber SDL_SCANCODE_3 (x1)
no such key use in the code: src/controls/cKeyboardEvent.cpp cKeyboardEvent::getGroupNumber SDL_SCANCODE_4 (x1)
no such key use in the code: src/controls/cKeyboardEvent.cpp cKeyboardEvent::getGroupNumber SDL_SCANCODE_5 (x1)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_LALT (x2)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_LCTRL (x2)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_LSHIFT (x2)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_RALT (x2)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_RCTRL (x2)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_RSHIFT (x2)
no such key use in the code: src/controls/cKeyboardEvent.h - SDL_SCANCODE_UNKNOWN (x1)
no such key use in the code: src/controls/mousestates/cMouseNormalState.cpp cMouseNormalState::onKeyDown m_commandBindings.rally (x1)
no such key use in the code: src/controls/mousestates/cMouseNormalState.cpp cMouseNormalState::onKeyPressed SDL_SCANCODE_LCTRL (x1)
no such key use in the code: src/controls/mousestates/cMouseNormalState.cpp cMouseNormalState::onKeyPressed SDL_SCANCODE_RCTRL (x1)
no such key use in the code: src/controls/mousestates/cMouseNormalState.cpp cMouseNormalState::onKeyPressed m_commandBindings.rally (x1)
no such key use in the code: src/controls/mousestates/cMouseNormalState.cpp cMouseNormalState::onKeyPressed m_commandBindings.repair (x1)
no such key use in the code: src/controls/mousestates/cMouseRepairState.cpp cMouseRepairState::onNotifyKeyboardEvent m_commandBindings.repair (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyDown SDL_SCANCODE_LCTRL (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyDown SDL_SCANCODE_LSHIFT (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyDown SDL_SCANCODE_RCTRL (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyDown SDL_SCANCODE_RSHIFT (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyDown m_commandBindings.attack (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyPressed SDL_SCANCODE_LSHIFT (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyPressed SDL_SCANCODE_RSHIFT (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyPressed m_commandBindings.attack (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyPressed m_commandBindings.repair (x1)
no such key use in the code: src/controls/mousestates/cMouseUnitsSelectedState.cpp cMouseUnitsSelectedState::onKeyPressed m_commandBindings.unload (x1)
no such key use in the code: src/drawers/cCommandBarDrawer.cpp cCommandBarDrawer::rebuildLayout m_commandBindings.attack (x1)
no such key use in the code: src/drawers/cCommandBarDrawer.cpp cCommandBarDrawer::rebuildLayout m_commandBindings.deploy (x1)
no such key use in the code: src/drawers/cCommandBarDrawer.cpp cCommandBarDrawer::rebuildLayout m_commandBindings.rally (x1)
no such key use in the code: src/drawers/cCommandBarDrawer.cpp cCommandBarDrawer::rebuildLayout m_commandBindings.release (x1)
no such key use in the code: src/drawers/cCommandBarDrawer.cpp cCommandBarDrawer::rebuildLayout m_commandBindings.repair (x1)
no such key use in the code: src/drawers/cCommandBarDrawer.cpp cCommandBarDrawer::rebuildLayout m_commandBindings.unload (x1)
no such key use in the code: src/gamestates/cChooseHouseState.cpp cChooseHouseState::onNotifyKeyboardEvent SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/gamestates/cCreditsState.cpp cCreditsState::onNotifyKeyboardEvent SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/gamestates/cMainMenuState.cpp cMainMenuState::onNotifyKeyboardEvent SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/gamestates/cMainMenuState.cpp cMainMenuState::onNotifyKeyboardEvent SDL_SCANCODE_M (x1)
no such key use in the code: src/gamestates/cOptionsState.cpp cOptionsState::constructAdvancedWindow commandBinding (x1)
no such key use in the code: src/gamestates/cOptionsState.cpp cOptionsState::constructAdvancedWindow commandBindings (x2)
no such key use in the code: src/gamestates/cOptionsState.cpp cOptionsState::onNotifyKeyboardEvent SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/gamestates/cOptionsState.cpp cOptionsState::onNotifyKeyboardEvent SDL_SCANCODE_UNKNOWN (x1)
no such key use in the code: src/gamestates/cOptionsState.cpp cOptionsState::onNotifyKeyboardEvent commandBindings (x1)
no such key use in the code: src/gamestates/cSelectYourNextConquestState.cpp cSelectYourNextConquestState::onNotifyKeyboardEvent SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/gamestates/cSetupSkirmishState.cpp cSetupSkirmishState::onNotifyKeyboardEvent SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/gamestates/cSetupSkirmishState.cpp cSetupSkirmishState::onNotifyKeyboardEvent SDL_SCANCODE_LEFT (x1)
no such key use in the code: src/gamestates/cSetupSkirmishState.cpp cSetupSkirmishState::onNotifyKeyboardEvent SDL_SCANCODE_RIGHT (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyHold SDL_SCANCODE_DOWN (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyHold SDL_SCANCODE_LEFT (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyHold SDL_SCANCODE_RIGHT (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyHold SDL_SCANCODE_UP (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyPressed SDL_SCANCODE_DOWN (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyPressed SDL_SCANCODE_LEFT (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyPressed SDL_SCANCODE_RIGHT (x1)
no such key use in the code: src/map/cMapCamera.cpp cMapCamera::onKeyPressed SDL_SCANCODE_UP (x1)
no such key use in the code: src/save/SaveSlotsDialog.cpp SaveSlotsDialog::onKeyboardEvent SDL_SCANCODE_BACKSPACE (x1)
no such key use in the code: src/save/SaveSlotsDialog.cpp SaveSlotsDialog::onKeyboardEvent SDL_SCANCODE_DOWN (x1)
no such key use in the code: src/save/SaveSlotsDialog.cpp SaveSlotsDialog::onKeyboardEvent SDL_SCANCODE_ESCAPE (x1)
no such key use in the code: src/save/SaveSlotsDialog.cpp SaveSlotsDialog::onKeyboardEvent SDL_SCANCODE_KP_ENTER (x1)
no such key use in the code: src/save/SaveSlotsDialog.cpp SaveSlotsDialog::onKeyboardEvent SDL_SCANCODE_RETURN (x1)
no such key use in the code: src/save/SaveSlotsDialog.cpp SaveSlotsDialog::onKeyboardEvent SDL_SCANCODE_UP (x1)
no such key use in the code: src/utils/GameSettings.hpp - commandBindings (x1)
no such key use in the code: src/utils/common.cpp loadSettingsFromIni commandBindings (x12)
no such key use in the code: src/utils/common.cpp saveSettingsToIni commandBindings (x6)
rule 10: state=game: debug mode; key=1; actions: debug-control-player-1 / select-group; places: src/cGame_logic.cpp:2417, src/controls/cKeyboardEvent.cpp:12
rule 10: state=game: debug mode; key=2; actions: debug-control-player-2 / select-group; places: src/cGame_logic.cpp:2421, src/controls/cKeyboardEvent.cpp:15
rule 10: state=game: debug mode; key=3; actions: debug-control-player-3 / select-group; places: src/cGame_logic.cpp:2425, src/controls/cKeyboardEvent.cpp:18
rule 10: state=game: debug mode; key=D+TAB; actions: draw-without-shroud / show-list-ids; places: src/drawers/cBuildingListDrawer.cpp:1040, src/drawers/cBuildingListDrawer.cpp:1047, src/managers/cDrawManager.cpp:519, src/managers/cDrawManager.cpp:533
rule 10: state=game: debug mode; key=F4; actions: debug-clear-shroud / debug-give-credits; places: src/cGame_logic.cpp:2066, src/cGame_logic.cpp:2441
rule 10: state=game: debug mode; key=TAB+D; actions: draw-without-shroud / show-list-ids; places: src/drawers/cBuildingListDrawer.cpp:1040, src/drawers/cBuildingListDrawer.cpp:1047, src/managers/cDrawManager.cpp:519, src/managers/cDrawManager.cpp:533
rule 10: state=game: structure selected; key=LCTRL; actions: create-group / rally; places: src/cGame_logic.cpp:2052, src/controls/CommandBindings.hpp:23
rule 10: state=game: units selected; key=D; actions: deploy / unload; places: src/controls/CommandBindings.hpp:21, src/controls/CommandBindings.hpp:22
rule 10: state=game: units selected; key=LCTRL; actions: attack / create-group; places: src/cGame_logic.cpp:2052, src/controls/CommandBindings.hpp:19, src/controls/mousestates/cMouseUnitsSelectedState.cpp:452
rule 10: state=game: units selected; key=LSHIFT; actions: add-to-selection / build-multiplier; places: src/building/cItemBuilder.cpp:826, src/building/cItemBuilder.cpp:833, src/controls/mousestates/cMouseUnitsSelectedState.cpp:427, src/controls/mousestates/cMouseUnitsSelectedState.cpp:483
rule 10: state=game: units selected; key=RSHIFT; actions: add-to-selection / build-multiplier; places: src/building/cItemBuilder.cpp:826, src/building/cItemBuilder.cpp:833, src/controls/mousestates/cMouseUnitsSelectedState.cpp:427, src/controls/mousestates/cMouseUnitsSelectedState.cpp:483
rule 10: state=game: units selected; command=attack; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: units selected; command=deploy; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: structure selected; command=rally; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: structure selected; command=release; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: nothing selected; command=repair; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: structure selected; command=repair; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: repair mode; command=repair; переназначение без проверки занятости; keys already used in this state: BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: units selected; command=repair; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
rule 10: state=game: units selected; command=unload; переназначение без проверки занятости; keys already used in this state: 1, 2, 3, 4, 5, BACKSLASH, C, D, DOWN, ESCAPE, F, F5, F9, H, KP_MINUS, KP_PLUS, LALT, LCTRL, LEFT, LEFTBRACKET, LSHIFT, M, MUTE, O, P, R, RCTRL, RETURN, RIGHT, RIGHTBRACKET, RSHIFT, TAB, UP, VOLUMEDOWN, VOLUMEUP, Z
keys: freshness FAIL; rule 10 flags: 20
exit=1
~~~~

#### run-hit-tests-fork.log

~~~~text
file	line	function	recorded_in_function	records_in_file	code
src/gui/GuiButton.cpp	244	GuiButton::onMouseMovedTo	no	0	m_focus = m_rect.isPointWithin(event.coords);
src/gui/GuiCheckBox.cpp	138	GuiCheckBox::onMouseMovedTo	no	0	m_focus = m_rect.isPointWithin(event.coords);
src/gui/GuiLabel.cpp	130	GuiLabel::onMouseMovedTo	no	0	m_focus = m_rect.isPointWithin(event.coords);
src/gui/GuiSlider.cpp	65	GuiSlider::onNotifyMouseEvent	no	0	if (m_rect.isPointWithin(event.coords)) {
src/drawers/cBuildingListDrawer.cpp	453	cBuildingListDrawer::drawList	no	0	if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
src/drawers/cBuildingListDrawer.cpp	504	cBuildingListDrawer::isOverItemCoordinates_Boolean	no	0	bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)
src/drawers/cBuildingListDrawer.cpp	515	cBuildingListDrawer::isOverItemCoordinates	no	0	cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y)
src/drawers/cBuildingListDrawer.cpp	520	cBuildingListDrawer::isOverItemCoordinates	no	0	if (!layout.cards.isPointWithin(x, y)) {
src/drawers/cBuildingListDrawer.cpp	534	cBuildingListDrawer::isOverItemCoordinates	no	0	if (card.isPointWithin(x, y)) {
src/drawers/cBuildingListDrawer.cpp	837	cBuildingListDrawer::onNotifyMouseEvent	no	0	if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) {
src/drawers/cBuildingListDrawer.cpp	850	cBuildingListDrawer::onNotifyMouseEvent	no	0	!layout.scrollbar.isPointWithin(event.coords.x, event.coords.y)) {
src/drawers/cCommandBarDrawer.cpp	69	cCommandBarDrawer::isMouseOver	no	0	bool cCommandBarDrawer::isMouseOver(const cPoint &point) const
src/drawers/cCommandBarDrawer.cpp	71	cCommandBarDrawer::isMouseOver	no	0	return m_panelRect.isPointWithin(point.x, point.y);
src/drawers/cCommandBarDrawer.cpp	259	cCommandBarDrawer::onNotifyMouseEvent	no	0	if (m_buttons[i].rect.isPointWithin(event.coords.x, event.coords.y)) {
src/drawers/cCommandBarDrawer.cpp	267	cCommandBarDrawer::onNotifyMouseEvent	no	0	if (button.enabled && button.rect.isPointWithin(event.coords.x, event.coords.y)) {
src/drawers/cMapDrawer.cpp	119	cMapDrawer::drawTerrain	no	0	if (!m_map->isWithinBoundaries(iCell)) {
src/drawers/cMiniMapDrawer.cpp	167	cMiniMapDrawer::isMouseOver	no	1	bool cMiniMapDrawer::isMouseOver()
src/drawers/cMiniMapDrawer.cpp	213	cMiniMapDrawer::drawTerrain	no	1	if (!m_map->isWithinBoundaries(x, y)) {
src/drawers/cMiniMapDrawer.cpp	268	cMiniMapDrawer::drawUnitsAndStructures	no	1	if (!m_map->isWithinBoundaries(x, y)) continue;
src/drawers/cMiniMapDrawer.cpp	364	cMiniMapDrawer::onMouseAt	no	1	m_isMouseOver = m_RectMinimap.isPointWithin(event.coords.x, event.coords.y);
src/drawers/cMiniMapDrawer.cpp	369	cMiniMapDrawer::onMousePressedLeft	no	1	if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
src/drawers/cMouseDrawer.cpp	57	cMouseDrawer::getWidthToolTip	no	0	if (context->isMouseOverStructure()) {
src/drawers/cMouseDrawer.cpp	68	cMouseDrawer::getHeightToolTip	no	0	if (context->isMouseOverStructure()) {
src/drawers/cMouseDrawer.cpp	112	cMouseDrawer::drawToolTip	no	0	if (context->isMouseOverStructure()) {
src/drawers/cMouseDrawer.cpp	147	cMouseDrawer::drawToolTipBackground	no	0	if (context->isMouseOverStructure()) {
src/drawers/cOrderDrawer.cpp	86	cOrderDrawer::onMouseAt	no	0	m_isMouseOverOrderButton = m_buttonRect.isPointWithin(event.coords);
src/drawers/cParticleDrawer.cpp	14	cParticleDrawer::determineParticlesToDraw	no	0	if (!pParticle.isWithinViewport(viewport)) continue;
src/drawers/cPlaceItDrawer.cpp	59	cPlaceItDrawer::drawStatusOfStructureAtCell	no	0	if (!global_map.isWithinBoundaries(cellX, cellY)) {
src/drawers/cSideBarDrawer.cpp	395	cSideBarDrawer::drawHdBuildingLists	no	0	list->isOverButton(mouse->getX(), mouse->getY())) {
src/drawers/cStructureDrawer.cpp	48	cStructureDrawer::drawStructuresHealthBars	no	0	if (context->isMouseOverStructure()) {
src/gamestates/cChooseHouseState.cpp	319	cChooseHouseState::onMouseLeftButtonClicked	no	4	if (event.coords.isWithinRectangle(&houseAtreides)) {
src/gamestates/cChooseHouseState.cpp	325	cChooseHouseState::onMouseLeftButtonClicked	no	4	else if (event.coords.isWithinRectangle(&houseOrdos)) {
src/gamestates/cChooseHouseState.cpp	331	cChooseHouseState::onMouseLeftButtonClicked	no	4	else if (event.coords.isWithinRectangle(&houseHarkonnen)) {
src/gamestates/cChooseHouseState.cpp	337	cChooseHouseState::onMouseLeftButtonClicked	no	4	else if (event.coords.isWithinRectangle(backButtonRect)) {
src/gamestates/cChooseHouseState.cpp	345	cChooseHouseState::onMouseMoved	no	4	hoversOverBackButton = event.coords.isWithinRectangle(backButtonRect);
src/gamestates/cChooseHouseState.cpp	347	cChooseHouseState::onMouseMoved	no	4	if (event.coords.isWithinRectangle(&houseAtreides)) {
src/gamestates/cChooseHouseState.cpp	350	cChooseHouseState::onMouseMoved	no	4	else if (event.coords.isWithinRectangle(&houseOrdos)) {
src/gamestates/cChooseHouseState.cpp	353	cChooseHouseState::onMouseMoved	no	4	else if (event.coords.isWithinRectangle(&houseHarkonnen)) {
src/gamestates/cSelectYourNextConquestState.cpp	831	cSelectYourNextConquestState::regionOver	no	1	if (!mapRect.isPointWithin(mouseX, mouseY)) return -1;
src/gamestates/cSetupSkirmishState.cpp	582	cSetupSkirmishState::getTextColorForRect	no	1	if (rect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	625	cSetupSkirmishState::drawStartPoints	no	1	if (startPoints.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	662	cSetupSkirmishState::drawPreviewMapAndMore	no	1	if (previewMapRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	698	cSetupSkirmishState::drawDetonateBlooms	no	1	Color textColor = detonateBloomsRect.isPointWithin(mouse->getX(), mouse->getY()) ? Color::red() : Color::white
src/gamestates/cSetupSkirmishState.cpp	711	cSetupSkirmishState::drawBlooms	no	1	Color textColor = bloomsRect.isPointWithin(mouse->getX(), mouse->getY()) ? Color::red() : Color::white();
src/gamestates/cSetupSkirmishState.cpp	719	cSetupSkirmishState::drawWorms	no	1	Color textColor = wormsRect.isPointWithin(mouse->getX(), mouse->getY()) ? Color::red() : Color::white();
src/gamestates/cSetupSkirmishState.cpp	726	cSetupSkirmishState::drawTechLevel	no	1	Color textColor = techLevelRect.isPointWithin(mouse->getX(), mouse->getY()) ? Color::red() : Color::white();
src/gamestates/cSetupSkirmishState.cpp	1071	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	1	if (houseRec.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1091	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	1	if (creditsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1103	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	1	if (startingUnitsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1115	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	1	if (teamsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1151	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	1	if (brainRect.isPointWithin(mouse->getX(),mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1171	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	1	if (houseRec.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1192	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	1	if (creditsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1204	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	1	if (startingUnitsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1216	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	1	if (teamsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1229	cSetupSkirmishState::onMouseLeftButtonClickedAtDetonateBlooms	no	1	if (detonateBloomsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1237	cSetupSkirmishState::onMouseLeftButtonClickedAtSpawnBlooms	no	1	if (bloomsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1244	cSetupSkirmishState::onMouseLeftButtonClickedAtWorms	no	1	if (wormsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1255	cSetupSkirmishState::onMouseLeftButtonClickedAtStartPoints	no	1	if (startPointsRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1290	cSetupSkirmishState::onMouseLeftButtonClickedAtMapList	no	1	const bool mouseHoversOverMapTile = rect.isPointWithin(m_game.getMouse()->getMouseCoords());
src/gamestates/cSetupSkirmishState.cpp	1462	cSetupSkirmishState::onMouseRightButtonClickedAtStartPoints	no	1	if (startPointsRect.isPointWithin(mouse->getMouseCoords())) {
src/gamestates/cSetupSkirmishState.cpp	1476	cSetupSkirmishState::onMouseRightButtonClickedAtWorms	no	1	if (wormsRect.isPointWithin(mouse->getMouseCoords())) {
src/gamestates/cSetupSkirmishState.cpp	1487	cSetupSkirmishState::onMouseRightButtonClickedAtTechLevel	no	1	if (techLevelRect.isPointWithin(mouse->getMouseCoords())) {
src/gamestates/cSetupSkirmishState.cpp	1498	cSetupSkirmishState::onMouseLeftButtonClickedAtTechLevel	no	1	if (techLevelRect.isPointWithin(mouse->getX(), mouse->getY())) {
src/managers/cDrawManager.cpp	279	cDrawManager::drawTopBarBackground	yes	4	game.getMouse()->isOverRectangle(
src/managers/cDrawManager.cpp	377	cDrawManager::drawMusicControls	yes	4	const bool mouseOverSlider = mouse->isOverRectangle(
src/managers/cDrawManager.cpp	413	cDrawManager::drawMusicControls	yes	4	if (mouse->isOverRectangle(
src/managers/cDrawManager.cpp	417	cDrawManager::drawMusicControls	yes	4	else if (mouse->isOverRectangle(
src/save/SaveSlotsDialog.cpp	418	SaveSlotsDialog::onMouseEvent	no	5	if (m_slotRects[index].isPointWithin(
src/save/SaveSlotsDialog.cpp	425	SaveSlotsDialog::onMouseEvent	no	5	if (m_nameRect.isPointWithin(event.coords.x, event.coords.y)) {
src/save/SaveSlotsDialog.cpp	429	SaveSlotsDialog::onMouseEvent	no	5	if (m_saveRect.isPointWithin(event.coords.x, event.coords.y)) {
src/save/SaveSlotsDialog.cpp	433	SaveSlotsDialog::onMouseEvent	no	5	if (m_loadRect.isPointWithin(event.coords.x, event.coords.y)) {
src/save/SaveSlotsDialog.cpp	437	SaveSlotsDialog::onMouseEvent	no	5	if (m_closeRect.isPointWithin(event.coords.x, event.coords.y)) {
src/sidebar/cBuildingList.cpp	254	cBuildingList::isOverButton	no	0	bool cBuildingList::isOverButton(int x, int y)
src/sidebar/cBuildingList.cpp	256	cBuildingList::isOverButton	no	0	return cRectangle::isWithin(
src/sidebar/cSideBar.cpp	145	cSideBar::onMouseAt	no	0	cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
src/sidebar/cSideBar.cpp	165	cSideBar::onMouseClickedLeft	no	0	if (list->isOverButton(event.coords.x, event.coords.y)) {
src/sidebar/cSideBar.cpp	194	cSideBar::onMouseClickedLeft	no	0	cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
src/sidebar/cSideBar.cpp	234	cSideBar::onMouseClickedRight	no	0	cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
src/controls/cGameControlsContext.cpp	54	cGameControlsContext::updateMouseCell	no	0	if (drawManager->getCommandBarDrawer()->isMouseOver(coords)) {
src/controls/cGameControlsContext.cpp	60	cGameControlsContext::updateMouseCell	no	0	if (drawManager->getMiniMapDrawer()->isMouseOver()) {
src/controls/cMouse.cpp	185	cMouse::isOverRectangle	no	0	bool cMouse::isOverRectangle(int x, int y, int width, int height)
src/controls/cMouse.cpp	187	cMouse::isOverRectangle	no	0	return cRectangle::isWithin(getX(), getY(), x, y, width, height);
src/controls/cMouse.cpp	190	cMouse::isOverRectangle	no	0	bool cMouse::isOverRectangle(cRectangle *rectangle)
src/controls/cMouse.cpp	193	cMouse::isOverRectangle	no	0	return rectangle->isPointWithin(getX(), getY());
exit=0
~~~~

#### run-hit-tests-port.log

~~~~text
file	line	function	recorded_in_function	records_in_file	code
src/gui/GuiBar.cpp	75	GuiBar::onNotifyMouseEvent	no	0	if (!event.coords.isWithinRectangle(&m_rect))
src/gui/GuiButton.cpp	277	GuiButton::onMouseMovedTo	no	0	m_focus = m_rect.isPointWithin(event.coords);
src/gui/GuiButton.cpp	315	GuiButton::onMouseLeftButtonClicked	no	0	if (!m_rect.isPointWithin(event.coords) || !m_enabled) {
src/gui/GuiCheckBox.cpp	157	GuiCheckBox::onMouseMovedTo	no	0	m_focus = m_rect.isPointWithin(event.coords);
src/gui/GuiCycleButton.cpp	48	GuiCycleButton::onNotifyMouseEvent	no	0	if (!m_enabled || !m_rect.isPointWithin(event.coords.x, event.coords.y)) {
src/gui/GuiLabel.cpp	146	GuiLabel::onMouseMovedTo	no	0	m_focus = m_rect.isPointWithin(event.coords);
src/gui/GuiSlider.cpp	125	GuiSlider::onNotifyMouseEvent	no	0	if (m_rect.isPointWithin(event.coords)) {
src/gui/GuiSlider.cpp	132	GuiSlider::onNotifyMouseEvent	no	0	if (m_rect.isPointWithin(event.coords) && m_onLeftMouseButtonClickedAction) {
src/gui/GuiSlider.cpp	146	GuiSlider::onNotifyMouseEvent	no	0	if (m_rect.isPointWithin(event.coords) && m_onRightMouseButtonClickedAction) {
src/gui/GuiStateButton.cpp	73	GuiStateButton::onNotifyMouseEvent	no	0	if (!event.coords.isWithinRectangle(&m_rect))
src/gui/GuiTextInput.cpp	138	GuiTextInput::onNotifyMouseEvent	no	0	m_focused = m_rect.isPointWithin(event.coords);
src/gui/GuiValueButton.cpp	43	GuiValueButton::onNotifyMouseEvent	no	0	m_focus = m_rect.isPointWithin(event.coords);
src/gui/GuiValueButton.cpp	59	GuiValueButton::onNotifyMouseEvent	no	0	m_pressed = m_rect.isPointWithin(event.coords);
src/gui/GuiValueButton.cpp	65	GuiValueButton::onNotifyMouseEvent	no	0	if (m_rect.isPointWithin(event.coords)) {
src/gui/GuiValueButton.cpp	75	GuiValueButton::onNotifyMouseEvent	no	0	if (m_rect.isPointWithin(event.coords)) {
src/drawers/cBuildingListDrawer.cpp	553	cBuildingListDrawer::drawList	no	0	if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
src/drawers/cBuildingListDrawer.cpp	642	cBuildingListDrawer::isOverItemCoordinates_Boolean	no	0	bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)
src/drawers/cBuildingListDrawer.cpp	653	cBuildingListDrawer::isOverItemCoordinates	no	0	cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y)
src/drawers/cBuildingListDrawer.cpp	657	cBuildingListDrawer::isOverItemCoordinates	no	0	if (!layout.cards.isPointWithin(x, y)) {
src/drawers/cBuildingListDrawer.cpp	671	cBuildingListDrawer::isOverItemCoordinates	no	0	if (card.isPointWithin(x, y)) {
src/drawers/cBuildingListDrawer.cpp	945	cBuildingListDrawer::onNotifyMouseEvent	no	0	if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) {
src/drawers/cBuildingListDrawer.cpp	958	cBuildingListDrawer::onNotifyMouseEvent	no	0	!layout.scrollbar.isPointWithin(event.coords.x, event.coords.y)) {
src/drawers/cMapDrawer.cpp	206	cMapDrawer::drawTerrainCells	no	0	if (!m_mapGeometry->isWithinBoundaries(iCell)) {
src/drawers/cMiniMapDrawer.cpp	203	cMiniMapDrawer::isMouseOver	no	0	bool cMiniMapDrawer::isMouseOver()
src/drawers/cMiniMapDrawer.cpp	253	cMiniMapDrawer::drawTerrain	no	0	if (!m_mapGeometry->isWithinBoundaries(x, y)) {
src/drawers/cMiniMapDrawer.cpp	311	cMiniMapDrawer::drawUnitsAndStructures	no	0	if (!m_mapGeometry->isWithinBoundaries(x, y)) continue;
src/drawers/cMiniMapDrawer.cpp	412	cMiniMapDrawer::onMouseAt	no	0	m_isMouseOver = m_RectMinimap.isPointWithin(event.coords.x, event.coords.y);
src/drawers/cMiniMapDrawer.cpp	429	cMiniMapDrawer::onMouseClickedLeft	no	0	if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
src/drawers/cMiniMapDrawer.cpp	455	cMiniMapDrawer::onMousePressedLeft	no	0	if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
src/drawers/cMiniMapDrawer.cpp	469	cMiniMapDrawer::onMousePressedRight	no	0	if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
src/drawers/cMouseDrawer.cpp	81	cMouseDrawer::getWidthToolTip	no	0	if (context->isMouseOverStructure()) {
src/drawers/cMouseDrawer.cpp	92	cMouseDrawer::getHeightToolTip	no	0	if (context->isMouseOverStructure()) {
src/drawers/cMouseDrawer.cpp	136	cMouseDrawer::drawToolTip	no	0	if (context->isMouseOverStructure()) {
src/drawers/cMouseDrawer.cpp	171	cMouseDrawer::drawToolTipBackground	no	0	if (context->isMouseOverStructure()) {
src/drawers/cOrderDrawer.cpp	87	cOrderDrawer::onMouseAt	no	0	m_isMouseOverOrderButton = m_buttonRect.isPointWithin(event.coords);
src/drawers/cParticleDrawer.cpp	37	cParticleDrawer::determineParticlesToDraw	no	0	if (!pParticle.isWithinViewport(viewport)) continue;
src/drawers/cPlaceItDrawer.cpp	146	cPlaceItDrawer::drawStatusOfStructureAtCell	no	0	if (!m_objects->getMapGeometry()->isWithinBoundaries(cellX, cellY)) {
src/drawers/cSideBarDrawer.cpp	428	cSideBarDrawer::drawHdBuildingLists	no	0	list->isOverButton(m_mouse->getX(), m_mouse->getY())) {
src/drawers/cStructureDrawer.cpp	99	cStructureDrawer::drawRememberedStructures	no	0	if (!geometry->isWithinBoundaries(iCell)) continue;
src/drawers/cStructureDrawer.cpp	132	cStructureDrawer::drawStructuresHealthBars	no	0	if (context->isMouseOverStructure()) {
src/gamestates/cChooseHouseState.cpp	248	cChooseHouseState::onMouseLeftButtonClicked	no	0	if (event.coords.isWithinRectangle(&houseAtreides)) {
src/gamestates/cChooseHouseState.cpp	251	cChooseHouseState::onMouseLeftButtonClicked	no	0	else if (event.coords.isWithinRectangle(&houseOrdos)) {
src/gamestates/cChooseHouseState.cpp	254	cChooseHouseState::onMouseLeftButtonClicked	no	0	else if (event.coords.isWithinRectangle(&houseHarkonnen)) {
src/gamestates/cChooseHouseState.cpp	257	cChooseHouseState::onMouseLeftButtonClicked	no	0	else if (event.coords.isWithinRectangle(&houseSardaukar)) {
src/gamestates/cChooseHouseState.cpp	260	cChooseHouseState::onMouseLeftButtonClicked	no	0	else if (event.coords.isWithinRectangle(&backButtonRect)) {
src/gamestates/cChooseHouseState.cpp	267	cChooseHouseState::onMouseMoved	no	0	hoversOverBackButton = event.coords.isWithinRectangle(&backButtonRect);
src/gamestates/cEditorState.cpp	450	cEditorState::onNotifyMouseEvent	no	0	if (event.coords.isWithinRectangle(&mapSizeArea)) {
src/gamestates/cEditorState.cpp	748	cEditorState::drawHoveredCellHighlight	no	0	if (!mouseCoords.isWithinRectangle(&mapSizeArea)) {
src/gamestates/cEditorState.cpp	839	cEditorState::tryGetTileFromMouseCoords	no	0	if (!coords.isWithinRectangle(&mapSizeArea)) {
src/gamestates/cSelectYourNextConquestState.cpp	888	cSelectYourNextConquestState::regionOver	no	0	if (!mapRect.isPointWithin(mouseX, mouseY)) return -1;
src/gamestates/cSetupSkirmishState.cpp	576	cSetupSkirmishState::getTextColorForRect	no	0	if (rect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	630	cSetupSkirmishState::drawStartPoints	no	0	if (startPoints.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	667	cSetupSkirmishState::drawPreviewMapAndMore	no	0	if (previewMapRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	702	cSetupSkirmishState::drawDetonateBlooms	no	0	Color textColor = detonateBloomsRect.isPointWithin(m_mouse->getX(), m_mouse->getY()) ? Color::Red : Color::Whi
src/gamestates/cSetupSkirmishState.cpp	713	cSetupSkirmishState::drawBlooms	no	0	Color textColor = bloomsRect.isPointWithin(m_mouse->getX(), m_mouse->getY()) ? Color::Red : Color::White;
src/gamestates/cSetupSkirmishState.cpp	720	cSetupSkirmishState::drawWorms	no	0	Color textColor = wormsRect.isPointWithin(m_mouse->getX(), m_mouse->getY()) ? Color::Red : Color::White;
src/gamestates/cSetupSkirmishState.cpp	727	cSetupSkirmishState::drawTechLevel	no	0	Color textColor = techLevelRect.isPointWithin(m_mouse->getX(), m_mouse->getY()) ? Color::Red : Color::White;
src/gamestates/cSetupSkirmishState.cpp	1138	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	0	if (houseRec.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1151	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	0	if (creditsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1163	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	0	if (startingUnitsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1175	cSetupSkirmishState::onMouseRightButtonClickedAtPlayerList	no	0	if (teamsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1209	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	0	if (brainRect.isPointWithin(m_mouse->getX(),m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1229	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	0	if (houseRec.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1241	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	0	if (creditsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1253	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	0	if (startingUnitsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1265	cSetupSkirmishState::onMouseLeftButtonClickedAtPlayerList	no	0	if (teamsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1278	cSetupSkirmishState::onMouseLeftButtonClickedAtDetonateBlooms	no	0	if (detonateBloomsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1286	cSetupSkirmishState::onMouseLeftButtonClickedAtSpawnBlooms	no	0	if (bloomsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1293	cSetupSkirmishState::onMouseLeftButtonClickedAtWorms	no	0	if (wormsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1304	cSetupSkirmishState::onMouseLeftButtonClickedAtStartPoints	no	0	if (startPointsRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/gamestates/cSetupSkirmishState.cpp	1339	cSetupSkirmishState::onMouseLeftButtonClickedAtMapList	no	0	const bool mouseHoversOverMapTile = rect.isPointWithin(m_mouse->getMouseCoords());
src/gamestates/cSetupSkirmishState.cpp	1536	cSetupSkirmishState::onMouseRightButtonClickedAtStartPoints	no	0	if (startPointsRect.isPointWithin(m_mouse->getMouseCoords())) {
src/gamestates/cSetupSkirmishState.cpp	1550	cSetupSkirmishState::onMouseRightButtonClickedAtWorms	no	0	if (wormsRect.isPointWithin(m_mouse->getMouseCoords())) {
src/gamestates/cSetupSkirmishState.cpp	1561	cSetupSkirmishState::onMouseRightButtonClickedAtTechLevel	no	0	if (techLevelRect.isPointWithin(m_mouse->getMouseCoords())) {
src/gamestates/cSetupSkirmishState.cpp	1572	cSetupSkirmishState::onMouseLeftButtonClickedAtTechLevel	no	0	if (techLevelRect.isPointWithin(m_mouse->getX(), m_mouse->getY())) {
src/managers/cDrawManager.cpp	335	cDrawManager::drawTopBarBackground	no	0	m_mouse->isOverRectangle(
src/sidebar/cBuildingList.cpp	272	cBuildingList::isOverButton	no	0	bool cBuildingList::isOverButton(int x, int y)
src/sidebar/cBuildingList.cpp	274	cBuildingList::isOverButton	no	0	return cRectangle::isWithin(
src/sidebar/cSideBar.cpp	191	cSideBar::onMouseAt	no	0	cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
src/sidebar/cSideBar.cpp	211	cSideBar::onMouseClickedLeft	no	0	if (list->isOverButton(event.coords.x, event.coords.y)) {
src/sidebar/cSideBar.cpp	240	cSideBar::onMouseClickedLeft	no	0	cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
src/sidebar/cSideBar.cpp	283	cSideBar::onMouseClickedRight	no	0	cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
src/controls/cGameControlsContext.cpp	94	cGameControlsContext::updateMouseCell	no	0	if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {
src/controls/cMouse.cpp	223	cMouse::isOverRectangle	no	0	bool cMouse::isOverRectangle(int x, int y, int width, int height)
src/controls/cMouse.cpp	225	cMouse::isOverRectangle	no	0	return cRectangle::isWithin(getX(), getY(), x, y, width, height);
src/controls/cMouse.cpp	228	cMouse::isOverRectangle	no	0	bool cMouse::isOverRectangle(cRectangle *rectangle)
src/controls/cMouse.cpp	231	cMouse::isOverRectangle	no	0	return rectangle->isPointWithin(getX(), getY());
src/controls/mousestates/cMousePlaceState.cpp	173	cMousePlaceState::mayPlaceIt	no	0	if (!m_context->getObjects()->getMapGeometry()->isWithinBoundaries(cellX, cellY)) {
exit=0
~~~~


## Сверка помощником 4

Решено исполнителем: для дорожки 3 проверяемым фактом выбраны литерал пути из поля «что» и ссылка на строку инструмента; результаты `git cat-file` в колонках `FORK1` и `PORT` не включены в точечную проверку `git show`; файл: `.tmp/p5tr/spotcheck.md:170`; было → стало: проверка включала статусы наличия объектов, которые не подтверждаются строкой кода → проверяется литерал по строке исходника; основание: задание требует сверки факта из строки с ревизионной ссылкой командой `git show … | sed`.


#### spotcheck.md

~~~~text
# Сверка выбранных строк

Проверено ровно 12 строк: четыре из таблиц помощника 1, четыре из таблиц помощника 2 и четыре из `sources.tsv` помощника 3. Каждая команда ниже отдельно читает указанную строку фиксированной ревизии.

## Помощник 1

### 1. `imports.tsv`

**Выбранная строка:** файл `tools/ui-audit/build_sheets.py`, ссылка `tools/ui-audit/build_sheets.py@9208dcf:2`; модуль `argparse`, класс `стандартный`. Проверяемый факт — импорт `argparse`.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/build_sheets.py | sed -n '2p'
```

**Вывод:**

```text
import argparse
```

**Результат: совпало.** Строка импортирует указанный модуль.

### 2. `interface.tsv`

**Выбранная строка:** файл `tools/ui-audit/build_sheets.py`, ссылка `tools/ui-audit/build_sheets.py@9208dcf:14`; константа `PER_SHEET = 6).

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/build_sheets.py | sed -n '14p'
```

**Вывод:**

```text
PER_SHEET = 6
```

**Результат: совпало.** Строка содержит указанное значение константы.

### 3. `fields.tsv`

**Выбранная строка:** значение `en`; источник `src/debug/UiAuditCapture.cpp@9208dcf:162`. Проверяемый факт — значение `en` используется в поле языка при английской локализации.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | sed -n '162p'
```

**Вывод:**

```text
         << outputH << "\",\"language\":\"" << (localization::isEnglish() ? "en" : "ru") << "\",\"graphics\":\"hd\",\"canvas\":{\"w\":" << game.m_screenW
```

**Результат: совпало.** Выражение выбирает `en` при английской локализации.

### 4. `scene-refs.tsv`

**Выбранная строка:** значение `structure-label-top`; источник `tools/ui-audit/check_scenes.py@9208dcf:26`; таблица помечает его как сцену и указывает число сцен `1). Проверяемый факт — наличие этого имени в списке сцен.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/check_scenes.py | sed -n '26p'
```

**Вывод:**

```text
STRUCTURE_EDGES = {"structure-label-top": ("top", at_top), "structure-label-right": ("right", at_right)}
```

**Результат: совпало.** Строка содержит `structure-label-top` в списке. Число `1` в отдельном столбце этой строкой не подтверждается и в эту точечную проверку не включено.

## Помощник 2

### 5. `io.tsv`

**Выбранная строка:** функция `find_pngs`, источник `tools/ui-audit/build_sheets.py@9208dcf:59); возвращаемое значение — отсортированный рекурсивный поиск PNG-файлов.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/build_sheets.py | sed -n '59p'
```

**Вывод:**

```text
    return sorted(Path(png_root).rglob("*.png"))
```

**Результат: совпало.** Строка рекурсивно ищет файлы `*.png` и сортирует результат.

### 6. `io.tsv`

**Выбранная строка:** функция `canvas_factor`, источник `tools/ui-audit/build_sheets.py@9208dcf:112); первая строка журнала читается и разбирается как JSON.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/build_sheets.py | sed -n '112p'
```

**Вывод:**

```text
    header = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
```

**Результат: совпало.** Строка читает журнал, берёт первую строку и передаёт её в `json.loads`.

### 7. `launch.tsv`

**Выбранная строка:** функция `apply_settings`, источник `tools/ui-audit/run_combo.py@9208dcf:28); замена существующего ключа либо добавление его после `[SETTINGS]`.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_combo.py | sed -n '28,36p'
```

**Вывод:**

```text
def apply_settings(text, values):
    for key, value in values.items():
        pattern = re.compile(rf"^{key}\s*=.*$", re.MULTILINE)
        line = f"{key}={value}"
        if pattern.search(text):
            text = pattern.sub(line, text, count=1)
        else:
            text = text.replace("[SETTINGS]", f"[SETTINGS]\n{line}", 1)
    return text
```

**Результат: совпало.** Тело функции соответствует описанию строки таблицы.

### 8. `launch.tsv`

**Выбранная строка:** функция `run_scene`, источник `tools/ui-audit/run_combo.py@9208dcf:73); команда запуска включает оконный режим, размеры экрана и параметры UI-аудита.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/run_combo.py | sed -n '73,80p'
```

**Вывод:**

```text
def run_scene(runtime, combo, scene_id, out_dir):
    width, height = split_resolution(combo)
    command = [
        str(runtime / "d2tm"), "-windowed", "-screenWidth", str(width), "-screenHeight", str(height),
        "--ui-audit-scene", scene_id, "--ui-audit-out", str(out_dir),
    ]
    return subprocess.run(command, cwd=runtime, env=game_environment(), check=False,
                          capture_output=True, text=True, timeout=SCENE_TIMEOUT_SECONDS)
```

**Результат: совпало.** В строках команды присутствуют перечисленные параметры запуска.

## Помощник 3

Для каждой выбранной строки проверяемый факт — строковый литерал пути из поля «что» и ссылка на строку инструмента. Столбцы `FORK1` и `PORT` содержат отдельные результаты проверки наличия объектов и в этой сверке литералов не оцениваются.

### 9. `sources.tsv`

**Выбранная строка:** поле «что» — `src/gamestates`; источник литерала — `tools/ui-audit/check_screens.py@9208dcf:9`.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/check_screens.py | sed -n '9p'
```

**Вывод:**

```text
CLASS_DIRECTORIES = ("src/gamestates", "src/mentat")
```

**Результат: совпало.** Строка содержит литерал `src/gamestates`, указанный в поле «что».

### 10. `sources.tsv`

**Выбранная строка:** поле «что» — `src/save/SaveSlotsDialog.hpp`; источник литерала — `tools/ui-audit/check_screens.py@9208dcf:10`.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/check_screens.py | sed -n '10p'
```

**Вывод:**

```text
CLASS_FILES = ("src/save/SaveSlotsDialog.hpp",)
```

**Результат: совпало.** Строка содержит литерал `src/save/SaveSlotsDialog.hpp`, указанный в поле «что».

### 11. `sources.tsv`

**Выбранная строка:** поле «что» — `src/include/definitions.h`; источник литерала — `tools/ui-audit/check_screens.py@9208dcf:59`.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/check_screens.py | sed -n '59p'
```

**Вывод:**

```text
    states = code_states((root / "src/include/definitions.h").read_text(encoding="utf-8", errors="replace"))
```

**Результат: совпало.** Строка содержит литерал `src/include/definitions.h`, указанный в поле «что».

### 12. `sources.tsv`

**Выбранная строка:** поле «что» — `src/controls`; источник литерала — `tools/ui-audit/find_hit_tests.py@9208dcf:9`.

**Команда:**

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/find_hit_tests.py | sed -n '9p'
```

**Вывод:**

```text
               "src/controls", "src/debug")
```

**Результат: совпало.** Строка содержит литерал `src/controls`, указанный в поле «что».
~~~~
