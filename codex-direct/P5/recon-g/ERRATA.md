# Поправка ведущего к разведке P5GR

Выборочная сверка Haiku (`SPOTCHECK.md`) — 13 из 15; сверка помощника 4 исполнителя (`spotcheck-executor.md`) — 12 из 12.

Столбец «первое вхождение» таблиц `access.tsv` и `access-helpers.tsv` местами указывает на соседнюю строку: в `access.tsv` (строка файла 229, функция `prepareGameScreen`) имя `HUMAN` впервые стоит в `src/debug/UiAuditAccess.cpp@9208dcf:794`, а не 793; в `access-helpers.tsv` (строка файла 119, функция `listForKind`) имя `LIST_UNITS` — в строке 770, а не 769. Ведущий проверил обе строки командой `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '768,771p;792,795p'`. Имена, объявления в `FORK1` и поиск в `PORT` в этих строках верны. Номер строки первого вхождения перед опорой на него сверять командой `git show`.

Полный отчёт исполнителя с командами и выводами (2,6 МБ) и рабочие файлы лежат на servak: `/srv/dune/worktrees/u13g/.tmp/p5gr/`.
