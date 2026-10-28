## PLAN-b0

Источники: закреплённые BASE/FORK/UP0, README_AI §1, история коммитов, исходники и тесты, план §3.2 и Б0–Б12.

Созданы четыре файла:

- [port_inventory.py](/srv/dune/worktrees/b0/tools/upstream/port_inventory.py): статусы, переименования, статистика, LFS, коммиты, коллизии ID и счётчик SDL2.
- [port_inventory.json](/srv/dune/worktrees/b0/docs/upstream/port_inventory.json): детерминированный инвентарь.
- [PORT_MAP.md](/srv/dune/worktrees/b0/docs/upstream/PORT_MAP.md): функции, носители, судьба файлов, тесты, классы переноса, зависимости, порядок Б3–Б12 и риски.
- [test_port_inventory.py](/srv/dune/worktrees/b0/tools/upstream/tests/test_port_inventory.py): воспроизводимость JSON, проверка пересечений и путей документа.

Механика делегирована `gpt-6-luna xhigh`; карта и итоговая сверка выполнены ведущим исполнителем. При расхождении числа файлов использован фактический diff. Коллизии `#define` не выдумывались: список пуст. Код игры и существующие инструменты не менялись; сборка, C++-тесты и перенос функций исключены.

## Q-b0-01 | 2026-10-28 16:04:14 UTC | HEAD 39a88806f4a4260b5b303a781448189e672f59f3

Работа заблокирована на записи коммитов. Первая команда `git add` получила:

```text
fatal: Unable to create '/srv/dune/worktrees/b0/.git/index.lock': Read-only file system
```

Журнал хода:

```text
Генератор и JSON готовы: 3076 путей, 118 пересечений; коммит не создан — .git доступен только для чтения; test_generator_output_matches_committed_inventory_byte_for_byte — OK.
Карта переноса готова: распределены 2341 путь форка, указаны преемники 20 файлов D/R и проверки функций; коммит не создан — .git доступен только для чтения; test_inline_file_paths_in_port_map_exist_in_fork_or_upstream — OK, итоговая сверка охвата — OK.
Тест unittest готов; коммит не создан — .git доступен только для чтения; полная команда unittest: Ran 3 tests in 4.440s, OK; git diff --check — код 0.
```

Полная команда проверки:

```text
/srv/dune/venv/bin/python -m unittest discover -s tools/upstream/tests -v
```

До создания реализации:

```text
Ran 3 tests in 0.001s
FAILED (failures=2, errors=1)
```

После реализации:

```text
Ran 3 tests in 4.440s
OK
```

### Не проверено

Сборка игры, C++-тесты, содержимое настоящих DAT-паков, работа функций после переноса и CI платформ. Эти проверки относятся к следующим шагам.

### git status --short

```text
?? docs/upstream/PORT_MAP.md
?? docs/upstream/port_inventory.json
?? tools/upstream/
```

### Владельцу

1. Карта и инвентарь готовы; Python-проверки прошли.
2. Коммиты не созданы из-за режима `.git` только для чтения.
3. Нужна доступная для записи `.git`, затем можно записать подготовленные подпункты в ветку. Порядок переноса ожидает утверждения ведущим.