# U16-F: генератор контракта юнитов после удаления классики (#49, PR #54)

## Цель

Итоговый аудит нашёл: после PR #54 генератор `tools/units3d/unit_contract.py` падает (`ValueError: HD4 density assignment was not found in cGame_logic.cpp`), потому что ищет в исходниках игры строки, которые #54 удалил. Привести генератор к коду ветки и перегенерировать контракт.

## Организация работы

- Порядок: чтение `tools/units3d/unit_contract.py` (функция `parse_density`, строки 300-304; якоря `world_scale_sources`, строки 800-810) и новых мест в `src/` → правка генератора → прогон генератора → тесты контракта → сдача.
- Параллельно: ничего, работа последовательная.
- Помощники: нет, работаешь один.
- Остановки — раздел `## Вопрос` в сдаче и конец работы: перегенерированный `docs/units/unit_contract.json` отличается от закоммиченного не только номерами строк в ссылках и правилами о плотности и масштабе мира; команда дважды подряд упала с одной и той же ошибкой окружения.
- Рамка правок: `tools/units3d/unit_contract.py`, `docs/units/unit_contract.json`, `docs/units/UNIT_CONTRACT.md`, папка `.tmp/` рабочей копии, файл сдачи. Команды `git add`, `git commit`, `git checkout`, `git switch`, `git stash`, `git clean`, `git reset`, `git restore` запрещены.
- Журнал: `.tmp/progress-u16f.md`, строка после каждого шага: что сделано, файлы, код выхода.

## Где

- Сервер: `ssh servak`. Рабочая копия: `/srv/dune/worktrees/u12`, ветка `codex/u16-hd-only`. Перед командами `git` — `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`. Python: `/srv/dune/venv/bin/python`, рабочая папка — корень рабочей копии.

## Что сделать

1. `parse_density` берёт плотность HD-ассетов из `cGame::kHdAssetDensity` в `src/cGame.h` (сейчас ищет `constexpr int density = N;` в `src/cGame_logic.cpp`, этой строки больше нет).
2. Якоря `world_scale_sources` (`return isHdGraphicsActive()` и `: 1.0F;` в `src/cGame.h`) заменить на строки нового тела `getWorldScaleFactor` в `src/cGame.h`; текст правила в контракте — без условия HD (HD всегда).
3. Скрипт в `.tmp/u16f/` проверяет: каждый якорь, который генератор ищет в `src/`, находится (число найденных и не найденных — в сдаче).
4. Перегенерировать: `/srv/dune/venv/bin/python tools/units3d/unit_contract.py --pack-dir resources/bin/data` — код 0.

## Проверки

1. Генератор — код 0, вывод его итоговой строки JSON.
2. `D2TM_PACK_DIR=$PWD/resources/bin/data PYTHONPATH=tools/units3d/tests /srv/dune/venv/bin/python -m unittest test_unit_contract` — `OK`.
3. Структурное сравнение старого и нового `unit_contract.json` (ссылки `файл:N` приведены к `файл`): список смысловых отличий — в сдаче.

## Сдача

Файл `C:\Users\Slaven\AppData\Local\Temp\claude\C--Users-Slaven-Projects-DUNE\22d0d3cf-a572-4607-9206-d93f8c915e9c\scratchpad\u16\done-fix.md`, по-русски, блок `## DONE-U16-F | время UTC | HEAD <sha>`: журнал хода как есть; `git diff --stat`; вывод проверок 1–3 и скрипта шага 3; предлагаемое сообщение коммита на английском, последняя строка `Behavior changes: none`; раздел «Не проверено» (обязателен); `git status --short`.

В ответе наверх — путь к файлу сдачи и до 10 строк.

Комментарии в коде. Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.
