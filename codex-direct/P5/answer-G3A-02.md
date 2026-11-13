## Приёмка P5G3A

Код части 3а принят. Ведущий сверил `git diff` с `PLAN-P5G3A` и `PLAN-P5G3A-delta-1` по шагам 1–10 и повторил проверки: `sha256sum -c .tmp/p5g3at/tests.sha256` (семь строк `OK`), скрипты `ui_audit_part3a_catalog.py`, `ui_audit_part3a_scenes.py` и `ui_audit_part2_scenes.py` (у каждого `exit=0`), `unittest discover` (последняя строка `OK`), обе сверки `grep` по `src/debug` (пусто), друг `UiAuditAccess` в трёх заголовках (по 1), фильтр предупреждений (пусто), итог `ctest.log` (`100% tests passed, 0 tests failed out of 319`). Чтение файлов из списка задания подтверждено по rollout. Коммит `af6a2e1e` сделан ведущим.

Папку `.tmp/p5g3a` не удаляй: её логи нужны ведущему до слияния.

Вызови `update_goal` со статусом `complete` и остановись. Других действий нет.
