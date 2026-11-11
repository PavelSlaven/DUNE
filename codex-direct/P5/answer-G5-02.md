## Ответ на Q-P5G5-02 — PLAN-P5G5-delta-2

Причина: песочница нити закрывает на запись всё вне рабочей копии, а `ccache` по умолчанию пишет в `/root/.cache/ccache`. Кэш компилятора этой задаче не нужен: `make` и так пересобирает только изменённые файлы.

Поправка проверки 2 раздела «Проверки»: команда сборки получает префикс `CCACHE_DISABLE=1` и выглядит ровно так:

`CCACHE_DISABLE=1 DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5g5c/build.log 2>&1; echo exit=$?`

Ожидание проверки 2 не меняется: `exit=0`; итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of 319`. `CCACHE_DIR` не задавай: кэш занял бы место на диске сервера.

Перед новой сборкой переименуй `.tmp/p5g5c/build.log` в `.tmp/p5g5c/build-ccache-failed.log`. Шаги 1–5 не повторяй: их правки уже в рабочей копии. Дальше — проверка 2 с этой командой, затем проверки 3–9 и сдача по заданию.

Решения исполнителя из сдачи приняты: `TMPDIR=.tmp/p5g5c/tmp` для всех скриптов с `tempfile` и путь `/srv/dune/tools/task-places.py`.

Не отступай от плана, не переусложняй.
