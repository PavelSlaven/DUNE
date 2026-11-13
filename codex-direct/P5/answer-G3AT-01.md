## Приёмка P5G3AT

Приёмочные тесты части 3а приняты. Ведущий повторил `sha256sum -c .tmp/p5g3at/tests.sha256` (семь строк `OK`), сверил хэши двух скриптов с текстом задания, diff `tools/ui-audit/tests/test_port_changes.py` (три добавленные строки EXCLUSIONS), `git status --short` (три строки) и логи H, I и J (первая строка H с `'outcome-win'` и `; extra []`; в I по 24 строки `game exited with 2` и `ui-audit: unknown scene`; в J одно `FAIL: test_g_exclusions_text` и `FAILED (failures=1)`). Чтение пяти файлов из списка задания подтверждено скриптом. Коммит `0b7989c2` сделан ведущим.

Папку `.tmp/p5g3at` не удаляй: хэши нужны исполнителю кода части 3а.

Вызови `update_goal` со статусом `complete` и остановись. Других действий нет.
