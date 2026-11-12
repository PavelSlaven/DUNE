## A-P9-01 — ответ на Q-P9-01

Да. В проверке 1 обе команды отдельного прогона случаев P9 получают `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib` перед `ctest`, как в проверках 7 и 8:

- `cd .tmp/out/build && LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib ctest -N -R '^P9 ' | tail -n 1` — `Total Tests: 9`;
- `mkdir -p .tmp/p9/tmp && cd .tmp/out/build && TMPDIR=$PWD/../../p9/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib ctest -R '^P9 ' --output-on-failure | tail -n 3` — строка `100% tests passed, 0 tests failed out of 9`.

Остальное в задании не меняется. Продолжай с проверки 1 (только эти две команды; сборку заново не запускай, если после неё код не менялся) и дальше по порядку проверок 2–9 до сдачи `## DONE-P9`.
